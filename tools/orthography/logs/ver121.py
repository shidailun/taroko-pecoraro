# -*- coding: utf-8 -*-
"""Batch 121 — his own ° paradigm line, used as an auditor.

WHAT THIS BATCH IS.  A ° line is his statement that these words are one
paradigm.  Where some members are already verified, they name the stem; a
member whose value disagrees with them is not a listing gap, it is a map bug.
78 such members exist.  Four of them were DARK on a real but WRONG word —
the worst class there is — and his own text says so:

  xlisi   -> hrisi    去開斜坡   XEULIS is 笑; hlisi  嘲笑   is the word
  xlisun  -> hrisun   要開斜坡              hlisun 會嘲笑
  sdxali  -> sdxali   把…在地上  SDAXAL is 倚靠; sdahar 依靠著 is the root
  sdxalun -> sdxalun  要用泥土
  pk'lae  -> pklai    the kla 知道 family;  K'LAE is 硬/昂貴 = kray

His SDAXAL tag reads "(R. = DAXAL ?)" — he flagged the resemblance to DAXAL
土地 himself, and the modernizer walked straight into it.  In XEULIS the two
spellings sat side by side in one paradigm: xlisan was already right on
hlisan 笑 while its own sisters xlisi/xlisun were dark on 開斜坡.

TWO RULES REJECTED THIS ROUND, both measured before being dropped.

(1) A gloss-free level — regular() 's shape with sistered() 's ° gate — would
    have moved 273 pale values / 482 occurrences.  Read by hand it ships
    plqi where the line says pruq, and bhuwan where the line says bhui/bhuun.
    Those are map bugs; a gloss-free rule would have painted them dark.

(2) "charRules() over-applies l>r" — true, but tiny: 6 unverified values,
    14 occurrences.  And two of the six are traps.  gliq- IS attested as a
    full paradigm (gliqan 出草的地方, gliqun 要殺) but that is headhunting,
    not his G'LEQ 轉動/tordu — for which griq 扭曲 is exactly right.  bili
    很濕 matches BIRI 濕透 but there are TWO BIRI entries and the other is
    最後的; modernize() sees one word with no entry context, so mapping it
    would break the other.  Neither was taken.

WHAT MOVED.  92.29% -> 92.33%.  Dark +16, pale -18, green 0, total -2 (the
two SX'MUK brackets collapsing as his psxm'qan/psxm'qun converge with his own
psxm'kan/psxm'kun).  Three of the five retired lies came back dark on the
right word; K'LAE's pkray is pale, which is the correct trade — a right
unverified value beats a wrong verified one.
"""
import collections, io, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

H = r"C:\dev\formosan\seediq\taroko-pecoraro"
fail = []


def check(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        fail.append(msg)


V = dict((m.group(1), int(m.group(2))) for m in re.finditer(
    r'^  "(.*)": (\d),$', io.open(os.path.join(H, "site", "verified.js"),
                                  encoding="utf-8").read(), re.M))
MAN = json.load(io.open(os.path.join(H, "tools", "orthography",
                                     "manual_map.json"), encoding="utf-8"))
t = io.open(os.path.join(H, "site", "modern_map.js"), encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])

# key -> value, and the wrong value each one retires
NEW = [
    ("xlisi", "hlisi", "hrisi"), ("xlisun", "hlisun", "hrisun"),
    ("pxlisi", "phlisi", "phrisi"), ("sxlisi", "shlisi", "shrisi"),
    ("sxlisun", "shlisun", "shrisun"), ("psxlisi", "pshlisi", "pshrisi"),
    ("sdxali", "sdhari", "sdxali"), ("sdxalun", "sdharun", "sdxalun"),
    ("psdxali", "psdhari", "psdxali"), ("psdxalun", "psdharun", "psdxalun"),
    ("spsdxalun", "spsdharun", "spsdxalun"),
    ("pk'lae", "pkray", "pklai"), ("mpk'lae", "empkray", "empklai"),
    ("tkk'lae", "tkkray", "tkklai"),
    ("pqlqeli", "pqrqili", "pqlqeli"), ("pqlqelun", "pqrqilun", "pqlqelun"),
    ("sloaon", "srwaun", "sloaon"), ("p'lkox", "plkuh", "prkuh"),
    ("qlagun", "kragun", "qlagun"),
    ("plqe", "prqi", "plqi"), ("pl'qe", "prqi", "plqi"),
    ("bxoan", "bhuan", "bhuwan"),
    ("psxm'qan", "pshmkan", "pshmqan"), ("psxm'qun", "pshmkun", "pshmqun"),
]
# the five that were DARK on a real but wrong word
LIES = {"hrisi": "去開斜坡", "hrisun": "要開斜坡", "sdxali": "把…在地上",
        "sdxalun": "要用泥土", "pklai": "the kla 知道 family"}
# rejected — must NOT appear as a map value
BANNED = ["gliqan", "gliqun", "gliqi", "bili", "klaaw", "prkuh"]

print("-- the map")
for k, v, _ in NEW:
    check(MAN.get(k) == v and MAP.get(k) == v,
          "%-12s -> %-11s (manual=%s map=%s)" % (k, v, MAN.get(k), MAP.get(k)))
check(len(MAN) == 1750, "manual_map keys == 1750 (was 1731): %d" % len(MAN))

print("\n-- the five retired lies are no longer any key's value")
for w, gl in sorted(LIES.items()):
    ks = sorted(k for k in MAP if MAP[k] == w)
    check(not ks, "%-9s (%s) unreferenced: %s" % (w, gl, ks or "yes"))

print("\n-- the two rejected rules left no trace")
for w in BANNED:
    ks = sorted(k for k in MAP if MAP[k] == w)
    check(not ks, "%-9s never used as a value: %s" % (w, ks or "yes"))
check(MAP.get("g'leq") == "griq",
      "G'LEQ 轉動 still griq 扭曲, not the gliq- 出草 paradigm: %s"
      % MAP.get("g'leq"))
check(MAP.get("biri") == "biri",
      "BIRI left on itself — two entries, 最後的 and 濕透, one key: %s"
      % MAP.get("biri"))

print("\n-- verified.js")
LEVELS = collections.Counter(V.values())
check(len(V) == 4693, "verified 4678 -> 4693: %d" % len(V))
check(LEVELS[1] == 3893, "level 1 LISTED 3888 -> 3893: %d" % LEVELS[1])
check(LEVELS[2] == 600, "level 2 regular 596 -> 600: %d" % LEVELS[2])
check(LEVELS[3] == 54, "level 3 vouched 53 -> 54: %d" % LEVELS[3])
check(LEVELS[4] == 67, "level 4 vouched_root 65 -> 67: %d" % LEVELS[4])
check(LEVELS[5] == 38, "level 5 sistered 36 -> 38: %d" % LEVELS[5])
check(LEVELS[6] == 31, "level 6 syncopated 30 -> 31: %d" % LEVELS[6])
check(LEVELS[7] == 10, "level 7 chained unmoved at 10: %d" % LEVELS[7])
check(sum(LEVELS[i] for i in (2, 3, 4, 5, 6, 7)) == 800,
      "a corrected value DECOMPOSES: derived levels 590 -> 800? %d"
      % sum(LEVELS[i] for i in (2, 3, 4, 5, 6, 7)))

# ---------------------------------------------------------------- the DOM
URL = "http://127.0.0.1:8765/?q=%CC%81"
COUNT = """() => {
  const c = {};
  for (const k of ['w-mod','w-unv','w-raw'])
    c[k] = document.querySelectorAll('span.'+k).length;
  return {counts:c, cards: document.querySelectorAll('article.entry').length};
}"""
SPANS = """(ws) => { const r = {};
  for (const n of document.querySelectorAll('span.w-mod,span.w-unv,span.w-raw')) {
    const t = n.textContent.trim().toLowerCase();
    if (ws.indexOf(t) < 0) continue;
    const s = n.className.indexOf('w-mod') >= 0 ? 'dark'
            : n.className.indexOf('w-unv') >= 0 ? 'PALE' : 'GREEN';
    (r[t] = r[t] || {})[s] = (r[t][s] || 0) + 1;
  } return r; }"""
WATCH = sorted({v for _, v, _ in NEW} | set(LIES) |
               {"prkuh", "plqi", "bhuwan", "phrisi", "shrisi", "shrisun"})

res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for mode in ("modern", "original"):
        ctx = b.new_context()
        ctx.add_init_script(
            "localStorage.setItem('taroko_pecoraro_spelling_v1','%s')" % mode)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL)
        pg.wait_for_timeout(9000)
        res[mode] = pg.evaluate(COUNT)
        res[mode]["errors"] = errs
        if mode == "modern":
            seen = pg.evaluate(SPANS, WATCH)
        ctx.close()
    b.close()

M, O = res["modern"], res["original"]
tm = sum(M["counts"].values())
to = sum(O["counts"].values())

print("\n-- the census")
check(M["counts"] == {"w-mod": 41060, "w-unv": 3377, "w-raw": 32},
      "modern 41044/3395/32 -> 41060/3377/32: %s" % M["counts"])
check(tm == 44469 and abs(100.0 * 41060 / tm - 92.33) < 0.005,
      "modern total 44471 -> 44469, dark 92.29%% -> 92.33%%: %d %.4f"
      % (tm, 100.0 * M["counts"]["w-mod"] / tm))
check(O["counts"] == {"w-mod": 41501, "w-unv": 3429, "w-raw": 32},
      "original 41481/3449/32 -> 41501/3429/32: %s" % O["counts"])
check(to == 44962 and to - tm == 493,
      "original total unmoved at 44962; modern is 493 shorter: %d %d"
      % (to, to - tm))
check(41060 - 41044 == 16 and 3395 - 3377 == 18 and 16 - 18 == -2,
      "modern deltas: dark +16, pale -18, green 0, total -2")
check(41501 - 41481 == 20 and 3449 - 3429 == 20,
      "original deltas: dark +20, pale -20, total 0 (no bracket in his own)")
check(M["cards"] == 1967 and O["cards"] == 1967,
      "1967 cards both modes: %d %d" % (M["cards"], O["cards"]))
check(not M["errors"] and not O["errors"],
      "no page errors: %s %s" % (M["errors"], O["errors"]))

print("\n-- the -2: only SX'MUK's brackets collapse")
check(seen.get("pshmkan") == {"dark": 3} and seen.get("pshmkun") == {"dark": 2},
      "his psxm'qan/psxm'qun now converge on pshmkan x3 / pshmkun x2: %s %s"
      % (seen.get("pshmkan"), seen.get("pshmkun")))

print("\n-- the lies are off the page")
for w in sorted(LIES):
    check(w not in seen, "%-9s absent from the DOM: %s" % (w, seen.get(w)))
for w in ("phrisi", "shrisi", "shrisun", "prkuh", "plqi", "bhuwan"):
    check(w not in seen, "%-9s absent from the DOM: %s" % (w, seen.get(w)))

print("\n-- what the corrections are painted")
EXPECT = {
    "hlisi": {"dark": 1}, "hlisun": {"dark": 1}, "phlisi": {"dark": 2},
    "shlisi": {"dark": 1}, "shlisun": {"dark": 1}, "pshlisi": {"PALE": 1},
    "sdhari": {"dark": 2}, "sdharun": {"dark": 1},
    "psdhari": {"dark": 2}, "psdharun": {"dark": 2},
    "spsdharun": {"PALE": 1},
    "pkray": {"PALE": 4}, "empkray": {"PALE": 1}, "tkkray": {"PALE": 2},
    "pqrqili": {"dark": 1}, "pqrqilun": {"dark": 1}, "srwaun": {"dark": 1},
    "plkuh": {"dark": 1}, "kragun": {"dark": 3}, "prqi": {"dark": 2},
    "bhuan": {"dark": 4}, "pshmkan": {"dark": 3}, "pshmkun": {"dark": 2},
}
for w, e in sorted(EXPECT.items()):
    check(seen.get(w) == e, "%-11s %s" % (w, e if seen.get(w) == e
                                          else "got %s want %s" % (seen.get(w), e)))

print("\n-- K'LAE is the honest trade: a right pale beats a wrong dark")
check(seen.get("pkray") == {"PALE": 4} and "pklai" not in seen,
      "pkray pale x4, pklai gone: %s / %s"
      % (seen.get("pkray"), seen.get("pklai")))

print("\n%s  (%d checks failed)" % ("PASS" if not fail else "FAILURES", len(fail)))
for m in fail:
    print("   " + m)
sys.exit(1 if fail else 0)
