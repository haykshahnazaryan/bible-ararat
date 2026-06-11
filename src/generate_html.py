#!/usr/bin/env python3
"""Generate armenian-bible-stone.html from bible_data.json, reusing the
   parchment/stone reading design with a books -> nested chapters sidebar."""
import json

data = json.load(open("bible_data.json", encoding="utf-8"))
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

HTML = r"""<!DOCTYPE html>
<html lang="hy" data-theme="light">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Աստուածաշունչ Մատեան — «Արարատ» թարգմանութիւն</title>
<meta name="description" content="Աստուածաշունչ Մատեան, «Արարատ» թարգմանութիւն — բոլոր գրքերը, գլուխներն ու համարները։" />

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600&family=Noto+Serif+Armenian:wght@400;500;600;700&family=Spectral:ital,wght@0,300;0,400;0,500;1,400&display=swap" rel="stylesheet" />

<style>
  :root {
    --bg:          #FFFFFF;
    --surface:     #FFFFFF;
    --sidebar:     #000000;
    --ink:         #2B2620;
    --ink-soft:    #6E6555;
    --lapis:       #1D4E79;
    --vermilion:   #7e9fd2;
    --gold:        #FFFFFF;
    --line:        rgba(43, 38, 32, 0.14);
    --line-strong: rgba(43, 38, 32, 0.28);
    --shadow:      rgba(43, 38, 32, 0.16);
    --selection:   rgba(29, 78, 121, 0.18);

    --font-display: "Cinzel", Georgia, serif;
    --font-body:    "Noto Serif Armenian", "Spectral", Georgia, serif;
    --font-numeral: "Noto Serif Armenian", "Cinzel", serif;

    --sidebar-w: 340px;
    --radius: 4px;
    --speed: 320ms;
    --ease: cubic-bezier(0.22, 0.61, 0.36, 1);
  }

  [data-theme="dark"] {
    --bg:          #000000;
    --surface:     #FFFFFF;
    --sidebar:     #000000;
    --ink:         #E9E1CF;
    --ink-soft:    #A99F8B;
    --lapis:       #6FAAcE;
    --vermilion:   #7e9fd2;
    --gold:        #FFFFFF;
    --line:        rgba(233, 225, 207, 0.12);
    --line-strong: rgba(233, 225, 207, 0.26);
    --shadow:      rgba(0, 0, 0, 0.55);
    --selection:   rgba(111, 170, 206, 0.22);
  }

  /* The sidebar and mobile top bar always use a black, light-on-dark palette,
     so they stay legible whether the page theme is light or dark. */
  .sidebar, .topbar {
    --bg:          #000000;
    --surface:     #FFFFFF;
    --sidebar:     #000000;
    --ink:         #E9E1CF;
    --ink-soft:    #A99F8B;
    --lapis:       #6FAACE;
    --vermilion:   #7e9fd2;
    --gold:        #FFFFFF;
    --line:        rgba(233, 225, 207, 0.12);
    --line-strong: rgba(233, 225, 207, 0.26);
    --selection:   rgba(111, 170, 206, 0.22);
  }

  *, *::before, *::after { box-sizing: border-box; }
  html { scroll-behavior: smooth; }
  body {
    margin: 0;
    font-family: var(--font-body);
    font-weight: 400;
    font-size: 1.05rem;
    line-height: 1.85;
    color: var(--ink);
    background-color: var(--bg);
    background-image:
      radial-gradient(circle at 20% 12%, rgba(154, 123, 46, 0.05), transparent 60%),
      radial-gradient(circle at 85% 80%, rgba(29, 78, 121, 0.05), transparent 55%);
    -webkit-font-smoothing: antialiased;
    transition: background-color var(--speed) var(--ease), color var(--speed) var(--ease);
  }
  ::selection { background: var(--selection); }
  a { color: var(--lapis); text-underline-offset: 3px; }
  :focus-visible { outline: 2px solid var(--lapis); outline-offset: 3px; border-radius: 2px; }

  /* LAYOUT */
  .sidebar {
    position: fixed; inset: 0 auto 0 0;
    width: var(--sidebar-w);
    display: flex; flex-direction: column;
    background: var(--sidebar);
    border-right: 1px solid var(--line);
    z-index: 40;
    transition: transform var(--speed) var(--ease), background-color var(--speed) var(--ease);
  }
  .content { margin-left: var(--sidebar-w); min-height: 100vh; padding: clamp(2rem, 5vw, 5.5rem) clamp(1.25rem, 5vw, 5rem); }
  .content-inner { max-width: 760px; margin: 0 auto; }

  /* SIDEBAR HEAD */
  .sidebar-head { padding: 1.6rem 1.5rem 1.1rem; border-bottom: 1px solid var(--line); }
  .brand-eyebrow {
    font-family: var(--font-display);
    font-size: 0.6rem; letter-spacing: 0.3em; text-transform: uppercase;
    color: var(--gold); margin: 0 0 0.5rem;
  }
  .brand-title {
    font-family: var(--font-numeral); font-weight: 700;
    font-size: 1.35rem; line-height: 1.25; margin: 0; color: var(--ink);
  }
  .brand-title .accent { color: var(--vermilion); }

  /* SEARCH */
  .search-wrap { padding: 1rem 1.25rem 0.5rem; }
  .search-field { position: relative; }
  .search-field svg { position: absolute; left: 0.7rem; top: 50%; transform: translateY(-50%); width: 16px; height: 16px; color: var(--ink-soft); pointer-events: none; }
  .search-input {
    width: 100%; font-family: var(--font-body); font-size: 0.92rem; color: var(--ink);
    background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius);
    padding: 0.55rem 0.7rem 0.55rem 2.1rem;
    transition: border-color var(--speed) var(--ease), box-shadow var(--speed) var(--ease);
  }
  .search-input::placeholder { color: var(--ink-soft); }
  .search-input:focus { outline: none; border-color: var(--lapis); box-shadow: 0 0 0 3px var(--selection); }

  /* NAV */
  .chapter-nav { flex: 1 1 auto; overflow-y: auto; padding: 0.4rem 0.6rem 1rem; }
  .testament-head {
    font-family: var(--font-display); font-size: 0.66rem; letter-spacing: 0.26em;
    text-transform: uppercase; color: var(--gold);
    margin: 1rem 0.75rem 0.4rem; padding-bottom: 0.3rem; border-bottom: 1px solid var(--line);
  }
  /* Book + chapter tile grids (hairline-separated cells, like the source app) */
  .book-grid, .chap-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(58px, 1fr));
    margin: 0.25rem 0.4rem 0.85rem;
    border-top: 1px solid var(--line-strong);
    border-left: 1px solid var(--line-strong);
    border-radius: var(--radius);
    overflow: hidden;
  }
  .chap-grid { grid-template-columns: repeat(auto-fill, minmax(46px, 1fr)); }

  .book-tile, .chap-btn {
    display: flex; align-items: center; justify-content: center;
    min-height: 46px; padding: 0.4rem 0.25rem;
    background: var(--sidebar);
    border: 0;
    border-right: 1px solid var(--line-strong);
    border-bottom: 1px solid var(--line-strong);
    color: var(--ink-soft); cursor: pointer;
    font-family: var(--font-numeral); font-size: 0.84rem; line-height: 1.15;
    text-align: center; word-break: break-word;
    transition: background-color 150ms var(--ease), color 150ms var(--ease);
  }
  .book-tile:hover, .chap-btn:hover { background: var(--selection); color: var(--ink); }
  .book-tile[aria-current="true"], .chap-btn[aria-current="true"] {
    background: var(--vermilion); color: #fff; font-weight: 600;
  }
  .book-tile.is-hidden { display: none; }

  /* Chapters drill-down view */
  #chaptersView[hidden], #booksView[hidden] { display: none; }
  .chap-view-head { display: flex; align-items: center; gap: 0.6rem; margin: 0.5rem 0.4rem 0.1rem; }
  .back-btn {
    display: inline-flex; align-items: center; gap: 0.3rem;
    background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius);
    padding: 0.42rem 0.75rem; color: var(--ink); cursor: pointer;
    font-family: var(--font-body); font-size: 0.86rem;
    transition: border-color 150ms var(--ease);
  }
  .back-btn:hover { border-color: var(--lapis); }
  .chap-view-title { font-family: var(--font-numeral); font-weight: 700; font-size: 1.02rem; color: var(--ink); margin: 0.55rem 0.5rem 0.3rem; }

  .search-empty { padding: 0.75rem 1.1rem; color: var(--ink-soft); font-style: italic; font-size: 0.9rem; }
  .search-empty[hidden] { display: none; }

  /* FOOTER */
  .sidebar-foot { border-top: 1px solid var(--line); padding: 0.85rem 1.25rem; display: flex; align-items: center; justify-content: space-between; gap: 0.75rem; }
  .foot-label { font-family: var(--font-display); font-size: 0.58rem; letter-spacing: 0.22em; text-transform: uppercase; color: var(--ink-soft); }
  .theme-toggle { display: inline-flex; align-items: center; gap: 0.5rem; background: var(--surface); border: 1px solid var(--line); border-radius: 999px; padding: 0.4rem 0.75rem; color: var(--ink); font-family: var(--font-body); font-size: 0.85rem; cursor: pointer; transition: border-color 200ms var(--ease); }
  .theme-toggle:hover { border-color: var(--lapis); }
  .theme-toggle svg { width: 16px; height: 16px; }
  .theme-toggle .icon-moon { display: none; }
  .theme-toggle .icon-sun  { display: inline; }
  [data-theme="dark"] .theme-toggle .icon-moon { display: inline; }
  [data-theme="dark"] .theme-toggle .icon-sun  { display: none; }

  /* MOBILE TOP BAR */
  .topbar { display: none; position: sticky; top: 0; z-index: 30; align-items: center; gap: 0.85rem; padding: 0.7rem 1rem; background: var(--sidebar); border-bottom: 1px solid var(--line); }
  .menu-btn { display: inline-flex; align-items: center; justify-content: center; width: 42px; height: 42px; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); color: var(--ink); cursor: pointer; }
  .menu-btn svg { width: 20px; height: 20px; }
  .topbar-title { font-family: var(--font-numeral); font-size: 0.98rem; font-weight: 700; color: var(--ink); }
  .backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.45); opacity: 0; visibility: hidden; z-index: 35; transition: opacity var(--speed) var(--ease), visibility var(--speed) var(--ease); }
  .backdrop.is-open { opacity: 1; visibility: visible; }

  /* CHAPTER ARTICLE */
  .chapter-eyebrow { font-family: var(--font-display); font-size: 0.7rem; letter-spacing: 0.26em; text-transform: uppercase; color: var(--gold); margin: 0 0 0.75rem; }
  .chapter-title { font-family: var(--font-numeral); font-weight: 700; font-size: clamp(2rem, 5vw, 3rem); line-height: 1.12; margin: 0 0 0.4rem; color: var(--ink); }
  .chapter-subtitle { font-style: italic; font-size: 1.12rem; color: var(--ink-soft); margin: 0 0 1.4rem; }
  .divider { display: block; width: 220px; height: 26px; margin: 0 0 2rem; color: var(--gold); }

  .chapter-body p.v { margin: 0 0 1.05rem; text-align: justify; }
  .chapter-body h3 { font-family: var(--font-numeral); font-weight: 600; font-size: 1.15rem; margin: 1.9rem 0 0.8rem; color: var(--lapis); }
  .vn { font-family: var(--font-display); font-size: 0.66em; font-weight: 600; color: var(--vermilion); margin-right: 0.28em; vertical-align: 0.35em; }
  .fn { color: var(--gold); font-size: 0.7em; cursor: help; vertical-align: 0.4em; padding: 0 0.05em; }

  .footnotes { margin-top: 2.5rem; padding-top: 1.2rem; border-top: 1px solid var(--line); }
  .footnotes h4 { font-family: var(--font-display); font-size: 0.66rem; letter-spacing: 0.24em; text-transform: uppercase; color: var(--gold); margin: 0 0 0.6rem; }
  .fn-list { margin: 0; padding: 0; list-style: none; font-size: 0.84rem; color: var(--ink-soft); line-height: 1.6; }
  .fn-list li { margin: 0 0 0.2rem; }
  .fn-ref { color: var(--vermilion); font-family: var(--font-display); font-size: 0.78em; margin-right: 0.5em; }

  .chapter-nav-foot { display: flex; justify-content: space-between; gap: 1rem; margin-top: 2.5rem; padding-top: 1.2rem; border-top: 1px solid var(--line); }
  .nav-prev, .nav-next { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 0.6rem 1rem; color: var(--ink); cursor: pointer; font-family: var(--font-body); font-size: 0.9rem; transition: border-color 180ms var(--ease); }
  .nav-prev:hover, .nav-next:hover { border-color: var(--lapis); }
  .nav-prev[disabled], .nav-next[disabled] { opacity: 0.35; cursor: default; }

  .chapter-article { animation: rise var(--speed) var(--ease); }
  @keyframes rise { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }

  @media (max-width: 860px) {
    .topbar { display: flex; }
    .sidebar { transform: translateX(-100%); box-shadow: 4px 0 24px var(--shadow); }
    .sidebar.is-open { transform: translateX(0); }
    .content { margin-left: 0; padding-top: clamp(1.5rem, 6vw, 2.5rem); }
  }
  @media (prefers-reduced-motion: reduce) {
    html { scroll-behavior: auto; }
    *, *::before, *::after { animation-duration: 0.001ms !important; transition-duration: 0.001ms !important; }
  }

  /* --surface is now #fff in every theme, so controls drawn on it use dark
     text/icons to stay legible. */
  .search-input, .back-btn, .theme-toggle, .menu-btn,
  .nav-prev, .nav-next { color: #1c1a17; }
  .search-input::placeholder { color: #6b6256; }
  .search-field svg, .theme-toggle svg, .menu-btn svg { color: #1c1a17; }

  /* Light theme: the former-gold accents in the white reading pane use dark
     ink so they stay visible (in dark theme they remain #fff on black). */
  [data-theme="light"] .divider,
  [data-theme="light"] .footnotes h4,
  [data-theme="light"] .fn { color: var(--ink); }
  [data-theme="light"] .chapter-eyebrow { color: #000000; }
</style>
</head>

<body>
  <header class="topbar">
    <button class="menu-btn" id="menuBtn" aria-label="Բացել գրքերի ցանկը" aria-expanded="false" aria-controls="sidebar">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
        <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
      </svg>
    </button>
    <span class="topbar-title">Աստուածաշունչ Մատեան</span>
  </header>

  <div class="backdrop" id="backdrop" hidden></div>

  <aside class="sidebar" id="sidebar" aria-label="Գրքեր">
    <div class="sidebar-head">
      <p class="brand-eyebrow">«Արարատ» թարգմանութիւն</p>
      <h1 class="brand-title">Աստուածաշունչ<br><span class="accent">Մատեան</span></h1>
    </div>
    <div class="search-wrap">
      <div class="search-field">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
          <circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.5" y2="16.5"/>
        </svg>
        <input type="search" id="searchInput" class="search-input" placeholder="Որոնել գիրք…" autocomplete="off" aria-label="Որոնել գիրք" />
      </div>
    </div>
    <nav class="chapter-nav" aria-label="Գրքերի ցանկ">
      <div id="booksView"></div>
      <div id="chaptersView" hidden>
        <div class="chap-view-head">
          <button class="back-btn" id="backBtn" type="button">‹ Գրքերը</button>
        </div>
        <h3 class="chap-view-title" id="chapViewTitle"></h3>
        <div class="chap-grid" id="chapGrid"></div>
      </div>
      <p class="search-empty" id="searchEmpty" hidden>Համընկնում չգտնուեց։</p>
    </nav>
    <div class="sidebar-foot">
      <span class="foot-label">Ընթերցանութեան լոյս</span>
      <button class="theme-toggle" id="themeToggle" aria-pressed="false" aria-label="Անցնել մուգ ձեւին">
        <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
          <circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5L19 19M19 5l-1.5 1.5M6.5 17.5L5 19"/>
        </svg>
        <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
          <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>
        </svg>
        <span class="toggle-text">Մուգ</span>
      </button>
    </div>
  </aside>

  <main class="content" id="mainContent" aria-live="polite">
    <div class="content-inner" id="chapterContainer"></div>
  </main>

<script id="bibleData" type="application/json">__PAYLOAD__</script>
<script>
const DATA = JSON.parse(document.getElementById("bibleData").textContent);

/* flat index of chapters for prev/next + lookup */
const flat = [];
DATA.forEach(t => t.books.forEach(b => b.chapters.forEach(c => {
  flat.push({ tname: t.testament, bname: b.name, bid: b.id, n: c.n, num: c.num,
              sub: c.sub, body: c.body, fn: c.fn,
              key: "b" + b.id + "-" + c.n });
})));
const byKey = {};
flat.forEach((c, i) => { c.idx = i; byKey[c.key] = c; });

const els = {
  booksView: document.getElementById("booksView"),
  chaptersView: document.getElementById("chaptersView"),
  chapGrid: document.getElementById("chapGrid"),
  chapViewTitle: document.getElementById("chapViewTitle"),
  backBtn: document.getElementById("backBtn"),
  container: document.getElementById("chapterContainer"),
  main: document.getElementById("mainContent"),
  search: document.getElementById("searchInput"),
  searchEmpty: document.getElementById("searchEmpty"),
  themeToggle: document.getElementById("themeToggle"),
  toggleText: document.querySelector(".toggle-text"),
  sidebar: document.getElementById("sidebar"),
  menuBtn: document.getElementById("menuBtn"),
  backdrop: document.getElementById("backdrop"),
  html: document.documentElement
};

const DIVIDER_SVG = `
  <svg class="divider" viewBox="0 0 220 26" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true">
    <line x1="0" y1="13" x2="86" y2="13"/><line x1="134" y1="13" x2="220" y2="13"/>
    <path d="M110 3 L120 13 L110 23 L100 13 Z"/><path d="M110 7 L110 19 M104 13 L116 13"/>
    <circle cx="92" cy="13" r="2.2" fill="currentColor" stroke="none"/>
    <circle cx="128" cy="13" r="2.2" fill="currentColor" stroke="none"/>
  </svg>`;

/* ---- compact book abbreviations for the tile grid ---- */
const ABBR = {
  "ԾՆՆԴՈՑ":"Ծննդ","ԵԼԻՑ":"Ել","ՂԵՒՏԱՑՈՑ":"Ղև","ԹՈՒՈՑ":"Թվ","ԵՐԿՐՈՐԴ ՕՐԻՆԱՑ":"2Օր",
  "ԴԱՏԱՒՈՐԱՑ":"Դատ","ՀՌՈՒԹ":"Հռութ","Ա ԹԱԳԱՒՈՐԱՑ":"1Թագ","Բ ԹԱԳԱՒՈՐԱՑ":"2Թագ",
  "Գ ԹԱԳԱՒՈՐԱՑ":"3Թագ","Դ ԹԱԳԱՒՈՐԱՑ":"4Թագ","Ա ՄՆԱՑՈՐԴԱՑ":"1Մնաց","Բ ՄՆԱՑՈՐԴԱՑ":"2Մնաց",
  "ԵԶՐԱՍ":"Եզր","ՆԷԵՄԻԱ":"Նեեմ","ԵՍԹԵՐ":"Եսթ","ՍԱՂՄՈՍ":"Սաղ","ԱՌԱԿԱՑ":"Առակ",
  "ԺՈՂՈՎՈՂ":"Ժող","ԵՐԳ ԵՐԳՈՑ":"Երգ","ՅՈԲ":"Յոբ","ԵՍԱՅԻԱ":"Եսայ","ՈՎՍԷԷ":"Ովս",
  "ԱՄՈՎՍ":"Ամովս","ՄԻՔԻԱ":"Միք","ՅՈՎԷԼ":"Յովէլ","ԱԲԴԻԱ":"Աբդ","ՅՈՎՆԱՆ":"Յովն",
  "ՆԱՈՒՄ":"Նաում","ԱՄԲԱԿՈՒՄ":"Ամբ","ՍՈՓՈՆԻԱ":"Սոփ","ԱՆԳԷ":"Անգ","ԶԱՔԱՐԻԱ":"Զաք",
  "ՄԱՂԱՔԻԱ":"Մաղ","ԵՐԵՄԻԱ":"Երեմ","ԵՐԵՄԻԱՅԻ ՈՂԲԵՐԸ":"Ողբ","ԴԱՆԻԷԼ":"Դան","ԵԶԵԿԻԷԼ":"Եզեկ",
  "ՄԱՏԹԷՈՍ":"Մատ","ՄԱՐԿՈՍ":"Մարկ","ՂՈՒԿԱՍ":"Ղուկ","ՅՈՎՀԱՆՆԷՍ":"Յովհ","ԳՈՐԾՔ ԱՌԱՔԵԼՈՑ":"Գործ",
  "ԹՈՒՂԹ ԱՌ ՀՌՈՎՄԱՅԵՑԻՍ":"Հռոմ","Ա ԹՈՒՂԹ ԱՌ ԿՈՐՆԹԱՑԻՍ":"1Կոր","Բ ԹՈՒՂԹ ԱՌ ԿՈՐՆԹԱՑԻՍ":"2Կոր",
  "ԹՈՒՂԹ ԱՌ ԳԱՂԱՏԱՑԻՍ":"Գաղ","ԹՈՒՂԹ ԱՌ ԵՓԵՍԱՑԻՍ":"Եփես","ԹՈՒՂԹ ԱՌ ՓԻԼԻՊՊԵՑԻՍ":"Փիլիպ",
  "ԹՈՒՂԹ ԱՌ ԿՈՂՈՍԱՑԻՍ":"Կող","Ա ԹՈՒՂԹ ԱՌ ԹԵՍԱՂՈՆԻԿԵՑԻՍ":"1Թես","Բ ԹՈՒՂԹ ԱՌ ԹԵՍԱՂՈՆԻԿԵՑԻՍ":"2Թես",
  "Ա ԹՈՒՂԹ ԱՌ ՏԻՄՈԹԷՈՍ":"1Տիմ","Բ ԹՈՒՂԹ ԱՌ ՏԻՄՈԹԷՈՍ":"2Տիմ","ԹՈՒՂԹ ԱՌ ՏԻՏՈՍ":"Տիտ",
  "ԹՈՒՂԹ ԱՌ ՓԻԼԻՄՈՆ":"Փիլիմ","ԹՈՒՂԹ ԱՌ ԵԲՐԱՅԵՑԻՍ":"Եբր","ՅԱԿՈԲՈՍ":"Յակ","Ա ՊԵՏՐՈՍ":"1Պետ",
  "Բ ՊԵՏՐՈՍ":"2Պետ","Ա ՅՈՎՀԱՆՆԷՍ":"1Յովհ","Բ ՅՈՎՀԱՆՆԷՍ":"2Յովհ","Գ ՅՈՎՀԱՆՆԷՍ":"3Յովհ",
  "ՅՈՒԴԱ":"Յուդ","ՅԱՅՏՆՈՒԹԻՒՆ":"Յայտ"
};
function abbr(name) { return ABBR[name] || name.split(" ")[0].slice(0, 5); }
function bookById(id) {
  for (const t of DATA) for (const b of t.books) if (String(b.id) === String(id)) return b;
  return null;
}

let activeKey = null, activeBid = null, view = "books";

/* ---- books grid (two testament sections of abbreviation tiles) ---- */
function renderBooks() {
  let h = "";
  DATA.forEach(t => {
    h += `<h2 class="testament-head">${t.testament}</h2><div class="book-grid">`;
    t.books.forEach(b => {
      h += `<button class="book-tile" type="button" data-book="${b.id}"
        data-name="${(b.name + " " + abbr(b.name)).toLowerCase()}"
        title="${b.name} — ${b.chapters.length} գլուխ">${abbr(b.name)}</button>`;
    });
    h += `</div>`;
  });
  els.booksView.innerHTML = h;
  highlightActiveBook();
}

function highlightActiveBook() {
  els.booksView.querySelectorAll(".book-tile").forEach(t =>
    t.setAttribute("aria-current", t.dataset.book === String(activeBid) ? "true" : "false"));
}

function showBooks() {
  view = "books";
  els.chaptersView.hidden = true;
  els.booksView.hidden = false;
  highlightActiveBook();
}

function showChapters(bid, { highlight = true } = {}) {
  const b = bookById(bid);
  if (!b) return;
  view = "chapters";
  els.chapViewTitle.textContent = b.name;
  els.chapGrid.innerHTML = b.chapters.map(c =>
    `<button class="chap-btn" type="button" data-key="b${b.id}-${c.n}" title="Գլուխ ${c.n}">${c.n}</button>`).join("");
  els.booksView.hidden = true;
  els.chaptersView.hidden = false;
  els.searchEmpty.hidden = true;
  if (highlight) highlightActiveChapter();
}

function highlightActiveChapter() {
  els.chapGrid.querySelectorAll(".chap-btn").forEach(b =>
    b.setAttribute("aria-current", b.dataset.key === activeKey ? "true" : "false"));
  const a = els.chapGrid.querySelector('.chap-btn[aria-current="true"]');
  if (a) a.scrollIntoView({ block: "nearest" });
}

/* ---- render one chapter ---- */
function renderChapter(c) {
  const prev = flat[c.idx - 1], next = flat[c.idx + 1];
  els.container.innerHTML = `
    <article class="chapter-article">
      <header>
        <p class="chapter-eyebrow">${c.tname} · ${c.bname}</p>
        <h2 class="chapter-title">ԳԼՈՒԽ ${c.n}</h2>
        ${c.sub ? `<p class="chapter-subtitle">${c.sub}</p>` : ""}
        ${DIVIDER_SVG}
      </header>
      <div class="chapter-body">${c.body}</div>
      ${c.fn || ""}
      <div class="chapter-nav-foot">
        <button class="nav-prev" ${prev ? `data-key="${prev.key}"` : "disabled"}>‹ ${prev ? prev.bname + " " + prev.n : ""}</button>
        <button class="nav-next" ${next ? `data-key="${next.key}"` : "disabled"}>${next ? next.bname + " " + next.n : ""} ›</button>
      </div>
    </article>`;
  const a = els.container.firstElementChild;
  a.style.animation = "none"; void a.offsetWidth; a.style.animation = "";
}

function openChapter(key, { updateHash = true, scroll = true } = {}) {
  const c = byKey[key] || flat[0];
  renderChapter(c);
  activeKey = c.key; activeBid = c.bid;

  if (view === "chapters") {
    const first = els.chapGrid.firstElementChild;
    const gridBid = first ? first.dataset.key.split("-")[0] : null;  // "b<id>"
    if (gridBid !== "b" + c.bid) showChapters(c.bid, { highlight: false });
    highlightActiveChapter();
  }
  highlightActiveBook();

  if (updateHash) history.replaceState(null, "", "#" + c.key);
  if (scroll) window.scrollTo({ top: 0, behavior: "smooth" });
  closeSidebar();
}

/* ---- events ---- */
els.booksView.addEventListener("click", e => {
  const tile = e.target.closest(".book-tile");
  if (tile) showChapters(tile.dataset.book);
});
els.chapGrid.addEventListener("click", e => {
  const chap = e.target.closest(".chap-btn");
  if (chap) openChapter(chap.dataset.key);
});
els.backBtn.addEventListener("click", () => {
  els.search.value = "";
  filterBooks("");
  showBooks();
});

els.container.addEventListener("click", e => {
  const nav = e.target.closest(".nav-prev, .nav-next");
  if (nav && nav.dataset.key) openChapter(nav.dataset.key);
});

window.addEventListener("hashchange", () => {
  const key = location.hash.replace("#", "");
  if (key && byKey[key]) openChapter(key, { updateHash: false });
});

/* ---- search (filter book tiles by name or abbreviation) ---- */
function filterBooks(term) {
  let visible = 0;
  els.booksView.querySelectorAll(".book-tile").forEach(tile => {
    const match = tile.dataset.name.includes(term);
    tile.classList.toggle("is-hidden", !match);
    if (match) visible++;
  });
  els.booksView.querySelectorAll(".testament-head").forEach(h => {
    const grid = h.nextElementSibling;
    const any = grid && [...grid.children].some(t => !t.classList.contains("is-hidden"));
    h.style.display = any ? "" : "none";
  });
  els.searchEmpty.hidden = visible !== 0;
}
els.search.addEventListener("input", () => {
  if (view !== "books") showBooks();
  filterBooks(els.search.value.trim().toLowerCase());
});

/* ---- theme ---- */
function setTheme(theme) {
  els.html.setAttribute("data-theme", theme);
  const isDark = theme === "dark";
  els.themeToggle.setAttribute("aria-pressed", String(isDark));
  els.themeToggle.setAttribute("aria-label", isDark ? "Անցնել բաց ձեւին" : "Անցնել մուգ ձեւին");
  els.toggleText.textContent = isDark ? "Բաց" : "Մուգ";
  try { localStorage.setItem("bibleTheme", theme); } catch (e) {}
}
els.themeToggle.addEventListener("click", () =>
  setTheme(els.html.getAttribute("data-theme") === "dark" ? "light" : "dark"));

/* ---- mobile drawer ---- */
function openSidebar() { els.sidebar.classList.add("is-open"); els.backdrop.hidden = false; requestAnimationFrame(() => els.backdrop.classList.add("is-open")); els.menuBtn.setAttribute("aria-expanded", "true"); }
function closeSidebar() { els.sidebar.classList.remove("is-open"); els.backdrop.classList.remove("is-open"); els.menuBtn.setAttribute("aria-expanded", "false"); setTimeout(() => { els.backdrop.hidden = true; }, 320); }
els.menuBtn.addEventListener("click", () => els.sidebar.classList.contains("is-open") ? closeSidebar() : openSidebar());
els.backdrop.addEventListener("click", closeSidebar);
document.addEventListener("keydown", e => { if (e.key === "Escape") closeSidebar(); });

/* ---- init ---- */
function init() {
  renderBooks();
  let saved = null;
  try { saved = localStorage.getItem("bibleTheme"); } catch (e) {}
  const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  setTheme(saved === "dark" || saved === "light" ? saved : (prefersDark ? "dark" : "light"));
  const start = location.hash.replace("#", "");
  // Render the starting chapter in the main pane; sidebar shows the book grid.
  openChapter(byKey[start] ? start : flat[0].key, { scroll: false });
}
init();
</script>
</body>
</html>
"""

out = HTML.replace("__PAYLOAD__", payload)
with open("armenian-bible-stone.html", "w", encoding="utf-8") as f:
    f.write(out)
print("Wrote armenian-bible-stone.html", len(out.encode("utf-8")), "bytes")
