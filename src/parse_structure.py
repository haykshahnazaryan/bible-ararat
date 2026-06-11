#!/usr/bin/env python3
"""Parse the biblesociety.am page into a testament -> book -> chapters tree."""
import re, json, html

with open("gen_page.html", encoding="utf-8") as f:
    page = f.read()

# Find the two testament headers and their positions
t1 = page.find('id="testament1"')
t2 = page.find('id="testament2"')

# Regex for a book <li ...> NAME </li>
book_re = re.compile(
    r'<li class="book-select[^"]*"[^>]*book-id="(\d+)"[^>]*>(.*?)</li>',
    re.DOTALL,
)
# Regex for chapter buttons belonging to a book block
chap_re = re.compile(
    r'book-id="(\d+)"\s+chapter-id="(\d+)"\s*>(\d+)</button>'
)

# Build chapter map: book_id -> list of (chapter_number, chapter_id) in order
chapters_by_book = {}
for m in chap_re.finditer(page):
    bid, cid, num = m.group(1), int(m.group(2)), int(m.group(3))
    chapters_by_book.setdefault(bid, []).append((num, cid))

structure = []  # list of testaments
for tname, start, end in [
    ("Հին Կտակարան", t1, t2),
    ("Նոր Կտակարան", t2, len(page)),
]:
    segment = page[start:end]
    books = []
    for bm in book_re.finditer(segment):
        bid = bm.group(1)
        raw_name = re.sub(r"<[^>]+>", "", bm.group(2))
        name = html.unescape(raw_name).strip()
        chaps = chapters_by_book.get(bid, [])
        if not name or not chaps:
            continue  # skip empty placeholder books
        books.append({"book_id": bid, "name": name,
                      "chapters": [{"n": n, "cid": c} for n, c in chaps]})
    structure.append({"testament": tname, "books": books})

with open("structure.json", "w", encoding="utf-8") as f:
    json.dump(structure, f, ensure_ascii=False, indent=2)

# Report
total_books = sum(len(t["books"]) for t in structure)
total_chaps = sum(len(b["chapters"]) for t in structure for b in t["books"])
print(f"Testaments: {len(structure)}")
for t in structure:
    print(f"  {t['testament']}: {len(t['books'])} books")
print(f"Total books: {total_books}, total chapters: {total_chaps}")
print("First book:", structure[0]["books"][0]["name"],
      "chapters", len(structure[0]["books"][0]["chapters"]))
