# -*- coding: utf-8 -*-
"""Build the translator sheet, second pass: the same blocked words, asked as
TWO questions instead of one.

The b243 sheet asked "現代太魯閣語怎麼寫？" and got 71 answers, of which batch
242 could use 24. The other 47 were not mistakes and not evasions -- they were
answers to a question the sheet did not know it was also asking. Told that
`Kndoto` 手鐲 is written `sirug` today, the project learns the modern word for a
bracelet, which is true, useful, and buys nothing: it does not say his KNDOTO
survives. Batch 242's rule names the test (an answer is a RESPELLING only when
it is shape-continuous with his token under his own correspondences) and this
sheet moves that test to where it belongs -- into the question, before the
speaker answers, instead of into the adjudication afterwards.

So every row now asks:

  問一  his word, written with today's letters -- the same word, even if nobody
        says it any more. This is the only answer that can spell his page.
  問二  what you would say instead. Recorded as testimony about modern Truku,
        never used to respell him.

and shows what this informant already said, in whichever of the two columns it
actually answered, with the modern gloss of that answer where a source has one.
A speaker cannot be expected to keep two questions apart that the sheet itself
ran together, so the sheet says which one his last answer landed in.

Reads .scratch/b245/blocked.json (harvest.py) and .scratch/b245/prev.json
(prev.py). Writes .scratch/b245/translator.html. Prints a summary line only.
"""
import collections
import html
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
H = os.path.abspath(".")
SITE = os.path.join(H, "site")
ORTH = os.path.join(H, "tools", "orthography")
SRC = os.path.join(H, ".scratch", "b245", "blocked.json")
OUT = os.path.join(H, ".scratch", "b245", "translator.html")


def read(p):
    return io.open(p, encoding="utf-8").read()


def entries_json():
    s = read(os.path.join(SITE, "entries.js"))
    return json.loads(s[s.index("["):s.rindex("]") + 1])


def modern_map():
    t = read(os.path.join(SITE, "modern_map.js"))
    a = t.index("window.MODERN_MAP = {")
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$',
                           t[a:t.index("\n};", a) + 2], re.M))


def app_table(name):
    """a small object literal out of app.js — CLITIC_FORMS / WORD_OVERRIDES."""
    t = read(os.path.join(SITE, "app.js"))
    a = t.index("var " + name + " = {")
    b = t.index("\n  };", a)
    return dict((m.group(1), m.group(2)) for m in
                re.finditer(r'"([^"]+)"\s*:\s*"([^"]*)"', t[a:b]))


GL = [json.load(io.open(os.path.join(ORTH, n), encoding="utf-8"))
      for n in ("attested_gloss.json", "bible_gloss.json",
                "parquet_gloss.json")]
LEX = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"),
                            encoding="utf-8")))
KNOWN = set(LEX)
for D in GL:
    KNOWN |= set(D)


def glosses(w):
    out = []
    for D in GL:
        g = D.get(w) or []
        for x in (g if isinstance(g, list) else [g]):
            x = str(x).strip()
            if x and x not in out:
                out.append(x)
    return out


# What this informant already said, keyed on HIS token and sorted into the two
# questions by `prev.py`. Absent for a word he was never asked about, which is
# the normal case for a sheet built after a ruling changes the blocker list.
PREV = json.load(io.open(os.path.join(H, ".scratch", "b245", "prev.json"),
                         encoding="utf-8"))

ZH = re.compile(r"[㐀-鿿]")
MM = modern_map()
CLI = app_table("CLITIC_FORMS")
OV = app_table("WORD_OVERRIDES")


def wordKey(w):
    """app.js's own fold, copied verbatim — batch 219: absence in the wrong
    alphabet reads as pallor. It folds the elision marks and `ł` and NOTHING
    else; ç and the umlauts stay."""
    return re.sub(r"[’ʼ\"ʔ]", "'", (w or "").lower()).replace("ł", "l")


def charRules(w):
    return (wordKey(w).replace("o", "u").replace("l", "r").replace("x", "h"))


def val(w):
    """what the app displays for his token, and where it came from."""
    k = wordKey(w)
    if k in CLI:
        return k, "clitic"
    if k in OV:
        return OV[k], "override"
    if k in MM:
        return MM[k], "map"
    return charRules(k), "charrule"


# ---- his book -------------------------------------------------------------
ENT = entries_json()
TOK = re.compile(r"[A-Za-zÀ-ÿł'’ʼ\"]+")


def truku_fields(e):
    """every field of an entry that carries HIS Truku, and the sentences apart.

    His headword, his sub-form names and his ° paradigm slots are Truku too, so
    an occurrence count that reads only the examples under-reports the word the
    card is ABOUT."""
    heads, sents = [], []
    heads.append(e.get("hw") or "")
    for p in (e.get("paradigm") or []):
        heads.append(p if isinstance(p, str) else (p.get("form") or ""))
    for x in (e.get("examples") or []):
        sents.append((x.get("t") or "", x))
    for s in (e.get("subs") or []):
        heads.append(s.get("form") or "")
        for p in (s.get("paradigm") or []):
            heads.append(p if isinstance(p, str) else (p.get("form") or ""))
        for x in (s.get("examples") or []):
            sents.append((x.get("t") or "", x))
    return heads, sents


COUNT = collections.Counter()          # wordKey -> occurrences, book-wide
SPELL = collections.defaultdict(collections.Counter)   # wordKey -> his forms
DEFN = collections.defaultdict(list)   # wordKey -> [(entry, sub or None)]
SEEN = collections.defaultdict(list)   # wordKey -> [entry] (anywhere at all)
USES = collections.defaultdict(list)   # wordKey -> [(his sentence, example)]

for e in ENT:
    heads, sents = truku_fields(e)
    here = set()
    for f, s in ([(e.get("hw"), None)] +
                 [(x.get("form"), x) for x in (e.get("subs") or [])]):
        for t in TOK.findall(f or ""):
            DEFN[wordKey(t)].append((e, s))
    for f in heads:
        for t in TOK.findall(f):
            k = wordKey(t)
            COUNT[k] += 1
            SPELL[k][t] += 1
            here.add(k)
    for s, x in sents:
        for t in TOK.findall(s):
            k = wordKey(t)
            COUNT[k] += 1
            SPELL[k][t] += 1
            here.add(k)
    for k in here:
        SEEN[k].append(e)
    for s, x in sents:
        for k in set(wordKey(t) for t in TOK.findall(s)):
            USES[k].append((s, x))


# ---- the blocked rows -----------------------------------------------------
ROWS = json.load(io.open(SRC, encoding="utf-8"))


def his_token(r, pale):
    """HIS spelling behind a pale value, from the DOM where the two renders
    tokenise alike and by asking the chain where they do not (3 rows: modern
    mode runs joinClitics/collapseInline and his mode does not)."""
    if r["aligned"]:
        for (mt, mc), (ot, _) in zip(r["spans"], r["his"]):
            if "w-mod" not in mc.split() and mt.strip().lower() == pale:
                return ot.strip()
    for ot, _ in r["his"]:
        if val(ot.strip())[0] == pale:
            return ot.strip()
    return None


GROUPS = collections.OrderedDict()
unresolved = 0
for r in ROWS:
    for p in r["pale"]:
        t = his_token(r, p)
        if t is None:
            unresolved += 1
            continue
        g = GROUPS.setdefault(p, {"pale": p, "his": collections.Counter(),
                                  "rows": [], "sole": 0})
        g["his"][t] += 1
        g["rows"].append(r)
        if len(r["pale"]) == 1:
            g["sole"] += 1

assert not unresolved, "%d pale spans could not be traced to his token" % \
    unresolved


def letters(counter):
    """His spellings folded to LETTERS. Case is typography, not spelling: his
    headwords print uppercase, a sentence capitalises its first word, and
    running text is lower, so a raw count reports `Ksudan` / `KSUDAN` /
    `ksudan` as three spellings of a word he only ever spells one way. Nothing
    a translator can act on is in the case. `ç` survives the fold and has to:
    his ç/x is a real distinction (KOYOç 雨 against KOYOX 女人—妻子)."""
    out = collections.Counter()
    for f, c in counter.items():
        out[f.lower()] += c
    return out.most_common()


# ---- near misses ----------------------------------------------------------
def ed(a, b, cap=2):
    """Levenshtein, abandoned above cap."""
    if abs(len(a) - len(b)) > cap:
        return cap + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1,
                           prev[j - 1] + (ca != cb)))
        if min(cur) > cap:
            return cap + 1
        prev = cur
    return prev[-1]


def near(words, cap=2, lim=8):
    """listed modern words within `cap` edits of anything in `words`, glossed.

    Shape alone proposes far more wrong words than right ones — this project's
    own rule — so the list is presented to the translator as words ALREADY
    looked at and refused, never as candidates. Only glossed rows are shown:
    an unglossed near-miss gives a reader nothing to react to."""
    hits = {}
    for w in words:
        for c in KNOWN:
            if c == w or abs(len(c) - len(w)) > cap:
                continue
            d = ed(w, c, cap)
            if d <= cap:
                if c not in hits or d < hits[c]:
                    hits[c] = d
    out = []
    for c, d in sorted(hits.items(), key=lambda kv: (kv[1], kv[0])):
        # Two sources routinely carry the same gloss with different filler --
        # `用...圍成牆` beside `用。。。圍成牆` -- and joining them raw prints the
        # same answer twice. Dedupe on the Chinese alone.
        g, seen = [], set()
        for x in glosses(c):
            if not ZH.search(x):
                continue
            k = "".join(ZH.findall(x))
            if k in seen or any(k in s or s in k for s in seen):
                continue
            seen.add(k)
            g.append(x)
        if g:
            out.append((c, d, "／".join(g[:2])))
        if len(out) >= lim:
            break
    return out


# ---- page -----------------------------------------------------------------
def esc(s):
    return html.escape(s or "")


def marked(s):
    """⟦…⟧ → a highlight span, escaping only the parts BETWEEN the marks."""
    parts = re.split(r"⟦(.*?)⟧", s or "")
    out = ""
    for i, p in enumerate(parts):
        out += ("<mark>%s</mark>" % esc(p)) if i % 2 else esc(p)
    return out


ORDER = sorted(GROUPS.values(), key=lambda g: (-g["sole"], -len(g["rows"]),
                                               g["pale"]))
MAILTO = "shidailun@gmail.com"
BUILD_DATE = "2026-08-12"
NO_OTHER = []
HIS_SEEN = {}   # data-his -> question number; the answer sheet's join key
NO_ZH = []
FR_ONLY = []
PREV_SHOWN = []   # the kind of every previous answer this build prints
P = []
A = P.append
A('<title>Pecoraro 拼寫請教單 第二回</title>')
A('<style>%s</style>' % """
/* A philologist's query sheet, not a card deck. Cool paper and ink because the
   book is a 1977 typescript out of Paris and the reader is checking letters,
   not browsing; ONE colour on the page, the proofreader's red, and it means
   exactly one thing -- this is the word nobody has confirmed. His 1977 line and
   the modern line are set in the same monospace at the same size so they stack
   letter over letter, which is the comparison the whole sheet exists to make. */
:root{
  --paper:#f7f6f2; --panel:#fdfdfb; --ink:#1b1e23; --ink2:#646b76;
  --ink3:#8d949e; --rule:#dcdad2; --rule2:#eae8e1; --red:#b3352b;
  --redbg:#f4e3e0; --focus:#2e5c86;
}
@media (prefers-color-scheme:dark){:root{
  --paper:#111317; --panel:#171a1f; --ink:#e6e8ec; --ink2:#9aa2ad;
  --ink3:#767e8a; --rule:#2b3038; --rule2:#22262c; --red:#ff8574;
  --redbg:#3a2320; --focus:#8ab6e0;
}}
:root[data-theme=dark]{
  --paper:#111317; --panel:#171a1f; --ink:#e6e8ec; --ink2:#9aa2ad;
  --ink3:#767e8a; --rule:#2b3038; --rule2:#22262c; --red:#ff8574;
  --redbg:#3a2320; --focus:#8ab6e0;
}
:root[data-theme=light]{
  --paper:#f7f6f2; --panel:#fdfdfb; --ink:#1b1e23; --ink2:#646b76;
  --ink3:#8d949e; --rule:#dcdad2; --rule2:#eae8e1; --red:#b3352b;
  --redbg:#f4e3e0; --focus:#2e5c86;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);
 font:400 16px/1.8 "Noto Sans TC","PingFang TC","Microsoft JhengHei",
  "Hiragino Sans GB",system-ui,sans-serif;
 font-variant-numeric:tabular-nums}
.serif{font-family:"Noto Serif TC","Source Han Serif TC","Songti TC",
 "PMingLiU",Georgia,serif}
.mono,.tk,.w,.guess,.num,.toc,textarea,.near code{
 font-family:ui-monospace,"SF Mono","Cascadia Mono","DejaVu Sans Mono",
 Consolas,monospace}
a{color:var(--focus)}
:focus-visible{outline:2px solid var(--focus);outline-offset:2px}

.sheet{max-width:47rem;margin:0 auto;padding:3.5rem 1.25rem 7rem}

/* masthead */
header{border-bottom:3px double var(--rule);padding-bottom:1.4rem}
.eyebrow{font-size:.72rem;letter-spacing:.22em;color:var(--ink2);
 text-transform:uppercase;margin:0 0 .9rem}
h1{font-size:1.95rem;line-height:1.3;margin:0;font-weight:600;
 text-wrap:balance;letter-spacing:.02em}
.src{margin:.55rem 0 0;color:var(--ink2);font-size:.95rem;line-height:1.7}
.intro{display:flex;flex-direction:column;gap:1rem;margin:1.6rem 0 0;
 font-size:.97rem}
.intro p{margin:0}
.intro ol{margin:0;padding-inline-start:1.3rem;display:flex;
 flex-direction:column;gap:.4rem}
.intro b{font-weight:600}
.ask-big{border-inline-start:3px solid var(--red);padding:.1rem 0 .1rem .9rem}

.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(7.5rem,1fr));
 gap:1px;background:var(--rule);border:1px solid var(--rule);margin:1.9rem 0 0}
.stats div{background:var(--panel);padding:.75rem .9rem}
.stats b{display:block;font:600 1.5rem/1.2 ui-monospace,"SF Mono",Consolas,
 monospace;letter-spacing:-.02em}
.stats span{font-size:.76rem;letter-spacing:.1em;color:var(--ink2)}

.toc{margin:2.2rem 0 0;font-size:.85rem;line-height:2.1;color:var(--ink3)}
.toc a{color:var(--ink2);text-decoration:none;border-bottom:1px solid
 var(--rule)}
.toc a:hover{color:var(--red);border-bottom-color:var(--red)}

/* one query */
.q-item{display:grid;grid-template-columns:3.25rem 1fr;gap:0 1rem;
 border-top:1px solid var(--rule);padding:1.9rem 0 0;margin-top:2.2rem;
 scroll-margin-top:1rem}
.q-item:target .num{color:var(--red)}
.num{grid-column:1;font-size:.78rem;color:var(--ink3);letter-spacing:.04em;
 padding-top:.55rem}
.body{grid-column:2;min-width:0}
@media (max-width:33rem){
  .q-item{grid-template-columns:1fr}
  .num{grid-column:1;padding:0 0 .4rem}
  .body{grid-column:1}
}

.head{display:flex;align-items:baseline;gap:.55rem;flex-wrap:wrap}
.w{font-size:1.45rem;font-weight:600;color:var(--red);letter-spacing:-.01em}
.to{color:var(--ink3)}
.guess{font-size:1.05rem;color:var(--ink2);
 text-decoration:underline dotted 1.5px;text-underline-offset:.28em}
.same{font-size:.74rem;color:var(--ink3);border:1px solid var(--rule);
 border-radius:2px;padding:.1rem .35rem;letter-spacing:.06em;
 position:relative;top:-.15rem}
.count{margin-inline-start:auto;font-size:.78rem;color:var(--ink3);
 white-space:nowrap}

dl.facts{display:grid;grid-template-columns:auto 1fr;gap:.15rem .9rem;
 margin:.95rem 0 0;font-size:.88rem}
dl.facts dt{color:var(--ink3);white-space:nowrap}
dl.facts dd{margin:0;color:var(--ink2)}
dl.facts dd b{color:var(--ink);font-weight:600}

.lbl{font-size:.72rem;letter-spacing:.16em;color:var(--ink3);
 text-transform:uppercase;margin:1.5rem 0 .5rem}

.near-details{margin:1.5rem 0 0}
.near-details summary.lbl{cursor:pointer;margin:0}
.near-details summary.lbl::marker{color:var(--ink3)}
.near-details[open] summary.lbl{margin-bottom:.5rem}
.near-details .near{margin:0}

.cite{display:grid;grid-template-columns:2.6rem 1fr;gap:.1rem .6rem;
 margin:0 0 1.1rem;font-size:.9rem}
.cite dt{font-size:.7rem;letter-spacing:.08em;color:var(--ink3);
 padding-top:.28rem}
.cite dd{margin:0;min-width:0;overflow-x:auto}
.tk{font-size:.94rem;line-height:1.7;white-space:pre-wrap}
.tk.mod{color:var(--ink2)}
.gl{line-height:1.7}
.aside{grid-column:1/-1;font-size:.8rem;color:var(--ink3);margin:0 0 .3rem}
mark{background:var(--redbg);color:var(--red);font-weight:700;
 padding:.05em .18em;border-radius:2px}

.near{font-size:.86rem;color:var(--ink3);line-height:1.95}
.near code{color:var(--ink2);font-size:.88rem}

/* what he told us last time, and which of the two questions it answered. The
   panel is quiet -- it is not a correction and must not read as one. */
.prev{margin:1.35rem 0 0;padding:.75rem .95rem;border:1px solid var(--rule);
 background:var(--panel);font-size:.87rem;line-height:1.75;color:var(--ink2);
 border-radius:2px}
.prev b{color:var(--ink);font-weight:600}
.prev .said{font-family:ui-monospace,"SF Mono",Consolas,monospace;
 color:var(--red);font-weight:600}

.answer{margin-top:1.3rem;border-top:1px solid var(--rule2);padding-top:.85rem}
.answer label{display:block;font-size:.85rem;color:var(--ink2);
 margin-bottom:.45rem}
/* Two questions, and the eye must not be able to mistake one for the other:
   問一 carries the red rule because it is the only answer that can spell his
   page; 問二 is set back and grey, recorded but never load-bearing. */
.qq{margin-top:1.15rem}
.qq:first-child{margin-top:0}
.qq.one{border-inline-start:3px solid var(--red);padding-inline-start:.85rem}
.qq.two{border-inline-start:3px solid var(--rule);padding-inline-start:.85rem}
.qq label b{color:var(--ink);font-weight:600}
.qq .hint{font-size:.79rem;color:var(--ink3);margin:-.2rem 0 .45rem;
 line-height:1.7}
textarea{width:100%;min-height:2.9rem;padding:.55rem .7rem;
 border:1px solid var(--rule);background:var(--panel);color:var(--ink);
 font-size:.95rem;line-height:1.6;resize:vertical;border-radius:2px}
textarea:focus{border-color:var(--focus)}

.bar{position:fixed;inset-inline:0;bottom:0;background:var(--panel);
 border-top:1px solid var(--rule);padding:.65rem 1rem;display:flex;gap:.7rem;
 align-items:center;justify-content:center;flex-wrap:wrap;font-size:.85rem;
 color:var(--ink2)}
.bar b{color:var(--ink);font-weight:600}

/* the answered mark: a filled box has to be visible from the number gutter,
   so a reader scrolling back can see what is left without reading each one */
.q-item.done .num{color:var(--red)}
.q-item.done .num::after{content:"✓";display:block;font-size:.9rem}
/* 問二 answered and 問一 not: the row has given us something, and is still the
   row we are asking about. A different mark, not the same one. */
.q-item.part .num::after{content:"·";display:block;font-size:1.2rem;
 line-height:.7}

/* storage refused (private windows, some in-app browsers). Nothing else on
   the page can tell them their work will vanish, so it says so up front. */
.warn{border:1px solid var(--red);background:var(--redbg);color:var(--ink);
 padding:.8rem 1rem;margin:1.6rem 0;font-size:.92rem;border-radius:2px}

/* return panel. Three independent ways out and one of them is just TEXT on
   the page: if the clipboard, the mail client and the save prompt all fail,
   the answers are still sitting there to be selected, or photographed. */
#send{margin-top:3.2rem;border-top:3px double var(--rule);padding-top:1.5rem;
 scroll-margin-top:1rem}
#send h2{font-size:1.15rem;margin:0 0 .5rem;font-family:"Noto Serif TC",
 "Songti TC",serif;font-weight:600}
#send p{font-size:.9rem;color:var(--ink2);margin:.4rem 0 .9rem}
#out{min-height:9rem;font-size:.86rem;line-height:1.75;white-space:pre;
 overflow-wrap:normal;overflow-x:auto}
.acts{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:.8rem;
 align-items:center}
.acts .prim{border-color:var(--red);color:var(--red);font-weight:600}
.acts .quiet{margin-inline-start:auto;color:var(--ink3);border-color:
 transparent}
.acts .quiet:hover{color:var(--red)}
#msg{font-size:.85rem;color:var(--ink2);min-height:1.4em;margin:.55rem 0 0}
button{font:inherit;font-size:.85rem;padding:.4rem 1rem;border-radius:2px;
 border:1px solid var(--rule);background:var(--paper);color:var(--ink);
 cursor:pointer}
button:hover{border-color:var(--red);color:var(--red)}
footer{border-top:3px double var(--rule);margin-top:3rem;padding-top:1.2rem;
 font-size:.82rem;color:var(--ink3)}
@media print{
  /* the paper path: printed, every question has ruled space to answer by hand
     and the whole sheet can come back as a photograph. */
  .bar,.toc,.acts,#msg{display:none}
  body{background:#fff}
  .q-item{break-inside:avoid}
  textarea{min-height:3.4rem;background:#fff;border-bottom:1px solid #000}
  #send{break-before:page}
  #out{min-height:auto}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
""")
import hashlib as _h
# The digest identifies the QUESTION SET, and this sheet asks the same 46 words
# a different pair of questions -- so the word list alone would hash identical
# to b243's and an answer sheet coming back could not be told apart. The shape
# is part of the set.
QSET = _h.sha1(("2q|" + "|".join(
    "%s>%s" % (letters(g["his"])[0][0], g["pale"]) for g in ORDER)
).encode("utf-8")).hexdigest()[:7]
STAMP = BUILD_DATE

A('<div class="sheet" data-build="%s" data-qset="%s" data-mail="%s">'
  % (STAMP, QSET, esc(MAILTO)))
A('<header>')
A('<p class="eyebrow">請求協助 · 現代拼寫</p>')
A('<h1 class="serif">同樣這 %d 個詞 ── 這次分成兩個問題</h1>' % len(GROUPS))
A('<p class="src">Ferdinando Pecoraro 神父《太魯閣語—法語辭典》'
  '<span class="serif"><i>Essai de dictionnaire taroko-français</i></span>'
  '，SECMI，巴黎，1977 · 全書 398 頁數位化</p>')
A('</header>')

blocked = len(ROWS)
tot = 5429
A('<div class="intro">')
A('<p>非常謝謝您上次回的 71 條。其中有一部分直接幫我們定了拼法；'
  '其餘大多是告訴我們<b>「今天會說哪個詞」</b> ── 那是另一個問題的答案，'
  '一樣珍貴，但它沒辦法決定<b>他那個字</b>怎麼拼。所以這次每一個詞分開問兩格。</p>')
A('<p class="ask-big"><b>問一 ── 他這個字，用今天的拼法會怎麼寫？</b>'
  '就算現在沒有人這樣說了，也請照著他的字母寫寫看。<br>'
  '<b>問二 ── 這個意思，今天你們會說哪個詞？</b>'
  '（這一格我們會留著當紀錄，但不會拿它去改他的拼法。）<br>'
  '兩格都可以留白，也可以只填一格。'
  '全書 %s 句還剩 %d 句、%d 個詞查不到來源。'
  '（您填的內容只留在您自己的瀏覽器裡，不會自動送出。）</p>'
  % ("{:,}".format(tot), blocked, len(GROUPS)))
A('</div>')
A('<div class="stats">'
  '<div><b>%s</b><span>已完成例句</span></div>'
  '<div><b>%d</b><span>待確認例句</span></div>'
  '<div><b>%d</b><span>待確認詞</span></div>'
  '<div><b>%.2f%%</b><span>目前完成度</span></div></div>'
  % ("{:,}".format(tot - blocked), blocked, len(GROUPS),
     100.0 * (tot - blocked) / tot))
A('<nav class="toc" aria-label="全部待確認的詞">%s</nav>' % "　".join(
    '<a href="#w%d">%s</a>' % (n, esc(letters(g["his"])[0][0]))
    for n, g in enumerate(ORDER, 1)))

for n, g in enumerate(ORDER, 1):
    forms = [f for f, _ in g["his"].most_common()]
    key = wordKey(forms[0])
    # One value can be reached from more than one of his spellings -- `gnl'qan`
    # and `gnlqan` both send to `gnlqan` -- so the occurrence figure has to sum
    # over every key in the group, not over the commonest form's key alone.
    keys = sorted(set(wordKey(f) for f in forms))
    occ = sum(COUNT[k] for k in keys)
    sp = collections.Counter()
    for k in keys:
        sp.update(SPELL[k])
    allsp = letters(sp)
    head = allsp[0][0]
    ident = g["pale"] == wordKey(head)
    v, src = val(forms[0])
    A('<section class="q-item" id="w%d">' % n)
    A('<div class="num mono">%02d</div>' % n)
    A('<div class="body">')
    # An identity value is not an arrow: `ksudan → ksudan` reads as though the
    # change were the capital letter. Print the word once and say what it means.
    A('<div class="head"><span class="w mono">%s</span>%s'
      '<span class="count">全書出現 %d 次 · 擋住 %d 句</span></div>'
      % (esc(head),
         '<span class="same">未變動</span>' if ident else
         '<span class="to">→</span><span class="guess">%s</span>'
         % esc(g["pale"]),
         occ, len(g["rows"])))

    rowsh = []
    # Only where the LETTERS differ. Case is not a spelling (see `letters`),
    # and his two elision marks are: `gnl'qan` beside `gnlqan` is a real
    # variant and the one thing this row exists to show.
    if len(allsp) > 1:
        rowsh.append(("他的寫法", "、".join(
            "<b>%s</b>（%d 次）" % (esc(f), c) for f, c in allsp)))
    # An identity value is not a no-op and should not read like one: it says a
    # search was made and found nothing to change, which is a different thing
    # from a respelling nobody has confirmed.
    note = {"map": "由我們的對照表指定，但沒有任何現代來源收錄這個詞",
            "override": "由人工指定，但沒有任何現代來源收錄這個詞",
            "clitic": "由前接詞合寫而來，未經證實",
            "charrule": "沒有對照表條目，只是機械換字（o→u、l→r、x→h）"
                        "跑出來的結果，等於還沒有答案"}[src]
    if ident:
        note = ("和他的寫法完全一樣 ── 我們找不到需要改寫的地方，"
                "但也沒有任何現代來源收錄這個詞")
    rowsh.append(("我們的暫定", "<b>%s</b> ── %s" % (esc(g["pale"]),
                                                     esc(note))))

    # Where he DEFINES the word, with his own glosses. A sub-form carries its
    # own gloss and is the more precise answer when the token is one; prefer a
    # definition that actually has a gloss over one that does not.
    def gl_of(o):
        # Chinese only. His entries are French and the Chinese is our
        # translation of it, so dropping the French loses no sense -- except
        # where the Chinese is missing, which is counted rather than assumed.
        g = (o.get("zh") or "").strip()
        if not g and (o.get("fr") or "").strip():
            FR_ONLY.append(o.get("hw") or o.get("form"))
        # He leaves eleven headwords glossed `??` / `？？`. That is not a gap in
        # our transcription and should not read as one -- it is him saying he
        # could not establish the meaning, which is itself worth a translator's
        # attention.
        return "" if g and not re.sub(r"[?？／\s]", "", g) else g

    defs = sorted([d for k in keys for d in (DEFN.get(k) or [])],
                  key=lambda es: (not gl_of(es[1] or es[0]), es[1] is None))
    if defs:
        e, sub = defs[0]
        o = sub or e
        gl = gl_of(o)
        name = (o.get("form") if sub else o.get("hw")) or ""
        tag = (o.get("paradigm") if sub else o.get("tag")) or \
            (e.get("tag") if sub else "")
        rowsh.append(("他的詞條", "<b>%s</b>%s%s%s" % (
            esc(name), esc("（%s 條下）" % e.get("hw")) if sub else "",
            esc("　" + tag) if isinstance(tag, str) and tag else "",
            esc("　" + gl) if gl else
            ("　（他在這一條寫的是「%s」── 連他自己都沒查出意思）"
             % esc((o.get("zh") or o.get("fr") or "").strip())
             if (o.get("zh") or o.get("fr") or "").strip()
             else "　（這一條他沒有寫釋義）"))))
    elif any(SEEN.get(k) for k in keys):
        rowsh.append(("出處", "%s ── 他只在例句裡用過，沒有另立詞條"
                      % esc("、".join(sorted(set(x.get("hw") or ""
                                                 for k in keys
                                                 for x in SEEN.get(k, [])))
                                      [:4]))))
    A('<dl class="facts">')
    for a, b in rowsh:
        A('<dt>%s</dt><dd>%s</dd>' % (esc(a), b))
    A('</dl>')

    A('<p class="lbl">他書中用到這個詞的句子</p>')
    # He prints the same sentence twice on some cards -- two real boxes, so the
    # pair count above is right at 3 where the reader sees 2. Fold the display
    # and say the number, rather than showing a reader the same line twice.
    dedup = collections.OrderedDict()
    for r in g["rows"]:
        d = dedup.setdefault(r["orig"], [r, 0])
        d[1] += 1
    for r, times in dedup.values():
        A('<dl class="cite">')
        if times > 1:
            A('<p class="aside">這一句他在書中重複了 %d 次。</p>' % times)
        others = [p for p in r["pale"] if p != g["pale"]]
        if others:
            A('<p class="aside">這一句還同時卡在 %s 上 ── 兩個都確定了才算完成。'
              '</p>' % "、".join("<b>%s</b>" % esc(p) for p in others))
        A('<dt>1977</dt><dd class="tk mono">%s</dd>' % marked(r["orig"]))
        A('<dt>現代</dt><dd class="tk mono mod">%s</dd>' % marked(r["mod"]))
        # No French row: the reader of this sheet does not read French. It is
        # safe to drop rather than fall back to, because all 83 blocked
        # sentences carry a Chinese gloss -- asserted below, since a sentence
        # printed with no gloss at all would be worse than one in French.
        NO_ZH.append(bool(r["zh"].strip()))
        A('<dt>中</dt><dd class="gl">%s</dd>' % esc(r["zh"]))
        A('</dl>')

    # No "his other uses" section, and the reason is structural rather than a
    # measurement: a pale word blocks EVERY example it stands in, so the
    # sentences shown above are already all of them. `USES` is kept as the
    # control -- it returns 3,189 for `ka` and, for all 74, exactly the
    # sentences the group prints.
    NO_OTHER.append((len(set(re.sub(r"[⟦⟧]", "", r["orig"])
                             for r in g["rows"])),
                     len(set(s for k in keys for s, _ in USES.get(k, [])))))

    nm = near(sorted(set([g["pale"]] + [wordKey(f) for f in forms])))
    if nm:
        A('<details class="near-details"><summary class="lbl">形近詞 · '
          '已排除（%d）</summary>' % len(nm))
        A('<p class="near">%s</p>' % "、".join(
            "<code>%s</code> %s" % (esc(c), esc(t)) for c, d, t in nm))
        A('</details>')

    # `data-his` is the LETTER form, not the commonest raw token: the answer
    # sheet that comes back is keyed on it, and `Ksudan` there would be the
    # same capital-letter noise the 他的寫法 row had.
    #
    # It is now also the STORAGE key -- sheet.js saves under his spelling, not
    # under the question number, so that ruling one word out does not silently
    # re-attach every answer below it. That makes uniqueness load-bearing, so
    # assert it here rather than letting sheet.js degrade quietly.
    if head in HIS_SEEN:
        raise AssertionError(
            "two questions share data-his %r (q%02d and q%02d): the answer "
            "sheet is keyed on his spelling and they would collide"
            % (head, HIS_SEEN[head], n))
    HIS_SEEN[head] = n

    # ---- what he said last time, in the column it actually answered --------
    # Looked up over every spelling in the group and case-insensitively: the
    # b243 sheet keyed its questions on the LETTER form and the answers came
    # back against his raw token, so `Msyuling` and `msyuling` are one row.
    p = pk = None
    for f in list(g["his"]) + [head]:
        for cand in (f, f.lower(), f.capitalize()):
            if cand in PREV:
                p, pk = PREV[cand], cand
                break
        if p:
            break
    if p:
        PREV_SHOWN.append(pk)
        # The register's own gloss for the word he named, where a source has
        # one. This is a FACT printed beside his answer, not a verdict on it --
        # `rahuq` meaning 除了 is the reader's evidence, not our refusal.
        gw = [x for x in glosses(wordKey(p["word"] or "")) if ZH.search(x)]
        gtxt = ('　現代語料裡 <span class="said">%s</span> 的意思是「%s」。'
                % (esc(p["word"]), esc("；".join(gw[:2])[:40]))) if gw else \
               ('　（現代語料裡查不到 <span class="said">%s</span> 這個詞。）'
                % esc(p["word"]) if p["word"] else "")
        lead = '上次您回答「<span class="said">%s</span>」' % esc(p["ans"])
        if p["kind"] == "respell":
            body = ('%s ── 這是<b>同一個字</b>的寫法，正是問一要的那種答案。%s'
                    '我們還沒有辦法把它定案，想請您再確認一次：'
                    '這樣寫對嗎？還是另有寫法？' % (lead, gtxt))
        elif p["kind"] == "meaning":
            body = ('%s ── 這回答的是<b>問二</b>（今天的說法），我們已經記下來了。%s'
                    '想再請教<b>問一</b>：他<b>這個字本身</b>，'
                    '用今天的拼法會怎麼寫？' % (lead, gtxt))
        else:
            body = ('%s ── 知道這個詞現在沒人用了，對我們一樣有用。'
                    '不過還是想請您幫個忙：<b>就算沒人這樣說了</b>，'
                    '照著他寫的字母，用今天的拼法會寫成什麼樣子？' % lead)
        A('<p class="prev">%s</p>' % body)

    # ---- the two questions -------------------------------------------------
    A('<div class="answer">')
    A('<div class="qq one"><label for="a%d"><b>問一</b>　'
      '他這個字，用今天的拼法會怎麼寫？</label>'
      '<p class="hint">同一個詞、同一個音，只是換成今天的寫法。'
      '就算現在沒有人這樣說了，也請照著他的字母寫寫看。'
      '真的沒辦法，就寫「不確定」。</p>'
      '<textarea id="a%d" data-q="1" data-n="%02d" data-w="%s" data-his="%s" '
      'rows="1" placeholder="今天的拼法"></textarea></div>'
      % (n, n, n, esc("" if ident else g["pale"]), esc(head)))
    A('<div class="qq two"><label for="b%d"><b>問二</b>　'
      '這個意思，今天你們會說哪個詞？</label>'
      '<p class="hint">換一個詞也沒關係 ── 這一格我們會留著當紀錄，'
      '但不會拿它去改他的拼法。</p>'
      '<textarea id="b%d" data-q="2" data-n="%02d" data-w="" data-his="%s" '
      'rows="1" placeholder="今天的說法（可留白）"></textarea></div>'
      % (n, n, n, esc(head)))
    A('</div>')
    A('</div></section>')

A('<section id="send"><h2>填好之後，這樣回傳</h2>')
A('<p>下面這格會自動整理出您已經填的每一條。'
  '用哪一種方式都可以 ── 只要這些字回到我們手上就行：</p>')
A('<textarea id="out" rows="8" readonly '
  'aria-label="整理好的回答，可直接選取複製"></textarea>')
A('<div class="acts">'
  '<button id="copy" class="prim">複製</button>'
  '<button id="sel">全選</button>'
  '<button id="mail">用電子郵件寄回</button>'
  '<button id="dl" hidden>下載成檔案</button>'
  '<button id="clr" class="quiet">清除全部</button></div>')
A('<p id="msg" role="status" aria-live="polite"></p>')
A('<p>複製不了也沒關係：上面那格的字可以直接用手指或滑鼠選取，'
  '甚至截圖傳給我們，一樣看得懂。'
  '也可以把整份清單<b>列印</b>出來用手寫，寫完拍照回傳。</p>')
A('</section>')
A('<footer>這份清單由 Pecoraro 太魯閣語辭典數位化專案自動產生，'
  '對應目前站上 %s 個例句的拼寫狀態。<br>'
  '<span class="mono">版本 %s · 題組 %s</span></footer>'
  % ("{:,}".format(tot), STAMP, QSET))
A('</div>')
A('<div class="bar"><span id="cnt"></span>'
  '<button id="next">跳到下一個沒填的</button>'
  '<button id="go">回傳答案</button></div>')
# The old bare-key answers that belong in question TWO, and only those. A
# `respell` or `gone` answer is printed on the page instead of being restored
# into a box (see sheet.js) -- question one is what this sheet re-asks, and
# pre-filling it with an answer we did not accept would read as acceptance.
MIG2 = json.dumps(dict((h, "2") for h, d in sorted(PREV.items())
                       if d["kind"] == "meaning"), ensure_ascii=False,
                  sort_keys=True)
JS = read(os.path.join(H, '.scratch', 'b245', 'sheet.js'))
assert "MIGRATE2_TABLE" in JS, "sheet.js has no migration slot to fill"
A('<script>%s</script>' % JS.replace("MIGRATE2_TABLE", MIG2, 1))

# Every word carries BOTH boxes, and the page never asks one of them twice.
# The count is what the returned sheet is keyed on, so a build that silently
# emitted a word with a single box would come back unattributable.
_html = "\n".join(P)
assert _html.count('data-q="1"') == len(GROUPS), (
    "問一 boxes %d, words %d" % (_html.count('data-q="1"'), len(GROUPS)))
assert _html.count('data-q="2"') == len(GROUPS), (
    "問二 boxes %d, words %d" % (_html.count('data-q="2"'), len(GROUPS)))
# The previous answers reached the page. A join that silently missed would
# make this a reprint of the b243 sheet with two boxes, which is the one way
# this build could look right and be worthless.
# Case-folded, because `letters()` folds it: he writes `Loai` at the head of a
# sentence and `loai` inside one, the b243 sheet took an answer against each,
# and they are ONE word here. A case pair must not read as a missed join --
# but two answers that differ in more than case must, so fold and compare.
_shown = set(k.lower() for k in PREV_SHOWN)
assert _shown == set(k.lower() for k in PREV), (
    "%d previous answers, %d printed: the join by his spelling missed %s"
    % (len(PREV), len(_shown),
       sorted(set(k.lower() for k in PREV) - _shown)[:6]))
for _a, _b in ((a, b) for a in PREV for b in PREV
               if a != b and a.lower() == b.lower()):
    assert PREV[_a]["ans"] == PREV[_b]["ans"], (
        "%r and %r are one word here but carry different answers (%r / %r): "
        "folding them prints one and drops the other"
        % (_a, _b, PREV[_a]["ans"], PREV[_b]["ans"]))
assert len(PREV_SHOWN) == len(set(PREV_SHOWN)), (
    "one previous answer printed under two words: %s"
    % [k for k in PREV_SHOWN if PREV_SHOWN.count(k) > 1][:4])

assert all(a == b for a, b in NO_OTHER), (
    "a blocked word appears in an example this page does not print: %s"
    % [x for x in NO_OTHER if x[0] != x[1]])
assert all(NO_ZH), "%d sentences would print with no gloss at all once the " \
    "French comes out" % NO_ZH.count(False)
assert "français" not in "\n".join(P).replace(
    "Essai de dictionnaire taroko-français", ""), "stray French"
io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(P))
if FR_ONLY:
    print("entries with a French gloss and no Chinese: %d %s"
          % (len(FR_ONLY), sorted(set(FR_ONLY))[:6]))
print("previous answers printed %d/%d — respelling %d, meaning %d, gone %d"
      % (len(PREV_SHOWN), len(PREV),
         sum(1 for k in PREV_SHOWN if PREV[k]["kind"] == "respell"),
         sum(1 for k in PREV_SHOWN if PREV[k]["kind"] == "meaning"),
         sum(1 for k in PREV_SHOWN if PREV[k]["kind"] == "gone")))
print("words %d | blocked examples %d | sentences shown %d | near-miss rows %d"
      % (len(GROUPS), len(ROWS), sum(len(g["rows"]) for g in ORDER),
         sum(1 for g in ORDER
             if near(sorted(set([g["pale"]] +
                                [wordKey(f) for f in g["his"]]))))))
# The row this prices: how many of the 74 he really spells more than one way,
# once case comes out. Raw, every group with two casings looked like a variant.
RAWV = sum(1 for g in ORDER if len(set(
    f for k in sorted(set(wordKey(x) for x in g["his"])) for f in SPELL[k])) > 1)
LETV = sum(1 for g in ORDER if len(letters(collections.Counter(
    {f: c for k in sorted(set(wordKey(x) for x in g["his"]))
     for f, c in SPELL[k].items()}))) > 1)
print("spelling-variant rows: %d raw -> %d once case is folded" % (RAWV, LETV))
print("-> %s" % os.path.relpath(OUT, H))
