#!/usr/bin/env python3
"""Clean fetched chapters and build the final armenian-bible-stone.html."""
import re, json, html, os

# ---- Armenian numeral generation (1..9999) ---------------------------------
_AM = [
    (9000,"Ք"),(8000,"Փ"),(7000,"Ւ"),(6000,"Ց"),(5000,"Ր"),(4000,"Տ"),(3000,"Վ"),(2000,"Ս"),(1000,"Ռ"),
    (900,"Ջ"),(800,"Պ"),(700,"Չ"),(600,"Ո"),(500,"Շ"),(400,"Ն"),(300,"Յ"),(200,"Մ"),(100,"Ճ"),
    (90,"Ղ"),(80,"Ձ"),(70,"Հ"),(60,"Կ"),(50,"Ծ"),(40,"Խ"),(30,"Լ"),(20,"Ի"),(10,"Ժ"),
    (9,"Թ"),(8,"Ը"),(7,"Է"),(6,"Զ"),(5,"Ե"),(4,"Դ"),(3,"Գ"),(2,"Բ"),(1,"Ա"),
]
def arm_numeral(n):
    out=[]
    for val,ch in _AM:
        while n>=val:
            out.append(ch); n-=val
    return "".join(out)

# ---- cleaning a single chapter file ----------------------------------------
ARM = r"Ա-Ֆա-ևՙ"
fn_anchor_re = re.compile(r'<a\b[^>]*rel="ftn(\d+)"[^>]*>\s*<sup>\*</sup>\s*</a>', re.DOTALL)
fn_div_re = re.compile(r'<div class="balloonstyle"[^>]*id="ftn(\d+)"[^>]*>(.*?)</div>', re.DOTALL)
p_re = re.compile(r'<p\b[^>]*>(.*?)</p>', re.DOTALL)
vn_re = re.compile(r'(?<!\d)(\d+)(?=[' + ARM + r']|<a )')
tag_re = re.compile(r'<[^>]+>')

def strip_tags(s):
    return html.unescape(tag_re.sub('', s)).strip()

def clean_chapter(raw):
    # isolate the content region: drop leading <style>, breadcrumb nav, trailing script/totop
    m = re.search(r'</nav>(.*)', raw, re.DOTALL)
    region = m.group(1) if m else raw
    region = re.split(r'<div class="totop|<script', region)[0]

    # footnote map
    notes = {}
    for fm in fn_div_re.finditer(region):
        notes[fm.group(1)] = strip_tags(fm.group(2))
    # remove footnote divs from the verse region
    region = fn_div_re.sub('', region)

    subtitle = ""
    parts = []
    for pm in p_re.finditer(region):
        inner = pm.group(1).strip()
        if not inner:
            continue
        text = strip_tags(inner)
        if not text:
            continue
        is_heading = not text[:1].isdigit()
        if is_heading:
            if not subtitle and not parts:
                subtitle = text          # first heading => chapter subtitle
            else:
                parts.append(('h', text))  # mid-chapter section heading
            continue
        # verse paragraph: wrap verse numbers, then resolve footnote markers
        body = vn_re.sub(r'<sup class="vn">\1</sup>', inner)
        def repl(a):
            note = notes.get(a.group(1), "")
            t = html.escape(note, quote=True)
            return f'<sup class="fn" title="{t}">*</sup>'
        body = fn_anchor_re.sub(repl, body)
        parts.append(('v', body))

    # assemble body html
    chunks = []
    for kind, val in parts:
        if kind == 'h':
            chunks.append(f'<h3>{val}</h3>')
        else:
            chunks.append(f'<p class="v">{val}</p>')
    body_html = "\n".join(chunks)

    # footnotes block
    fn_html = ""
    if notes:
        items = "".join(
            f'<li><span class="fn-ref">{html.escape(k)}</span>{html.escape(v)}</li>'
            for k, v in sorted(notes.items(), key=lambda x: int(x[0]))
        )
        fn_html = ('<div class="footnotes"><h4>Ծանօթագրութիւններ</h4>'
                   f'<ol class="fn-list">{items}</ol></div>')
    return subtitle, body_html, fn_html

# ---- build the data tree ----------------------------------------------------
structure = json.load(open("structure.json", encoding="utf-8"))
data = []
missing = []
for t in structure:
    tnode = {"testament": t["testament"], "books": []}
    for b in t["books"]:
        bnode = {"name": b["name"], "id": b["book_id"], "chapters": []}
        for c in b["chapters"]:
            path = f"chapters/{c['cid']}.html"
            if not os.path.exists(path) or os.path.getsize(path) < 200:
                missing.append(c["cid"]);
                bnode["chapters"].append({"n": c["n"], "num": arm_numeral(c["n"]),
                                          "sub": "", "body": "<p class=\"v\">(բովանդակութիւնը հասանելի չէ)</p>", "fn": ""})
                continue
            raw = open(path, encoding="utf-8").read()
            sub, body, fn = clean_chapter(raw)
            bnode["chapters"].append({"n": c["n"], "num": arm_numeral(c["n"]),
                                      "sub": sub, "body": body, "fn": fn})
        tnode["books"].append(bnode)
    data.append(tnode)

print("Books:", sum(len(t["books"]) for t in data),
      "Chapters:", sum(len(b["chapters"]) for t in data for b in t["books"]),
      "Missing:", len(missing))
if missing:
    print("Missing cids:", missing[:30])

json.dump(data, open("bible_data.json", "w", encoding="utf-8"), ensure_ascii=False)
print("Wrote bible_data.json", os.path.getsize("bible_data.json"), "bytes")
