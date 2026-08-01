# -*- coding: utf-8 -*-
"""Batch 122 — two more claims that named the wrong existing word.

Both came off the same test as batch 121, widened: rank every DARK headword
or paradigm claim whose modern gloss shares nothing with the entry it heads,
then read the top by hand.  Example sentences are excluded from the evidence —
a sentence may legitimately use any word at all, so its gloss says nothing
about the token.

  qlian -> qrian  被圍繞   QALI is 挖掘.  Its own siblings are kmari 挖 (33),
                          kari 挖掘 (868), krii, kriun 要挖的 (12); qrian
                          belongs to the 圍 root.  His bracketed twin qliyan
                          was already pale on kriyan, which is not listed —
                          krian is, so both spellings go there.
  skui  -> skuy   冷;涼    SKU is 收放－存放－儲存－埋葬.  smku/sku/skuan/skuun
                          are all right; only the imperative slot had drifted
                          onto 冷.  skui is itself listed (6 spoken).

THREE flagged and DELIBERATELY NOT TAKEN, each for a stated reason:

  gumuk   GMUK 蓋子 is glossed 嘟嘴生悶氣 in the omnibus, but the lexicon
          carries a whole family off it — dmgumuk 專門做蓋子的人, empeegumuk
          做成蓋子, knegumuk 蓋子好的樣子.  The word does mean 蓋子; the
          omnibus simply recorded another sense.  Correct as it stands.
  liwaq   LIWAK 驅趕 vs liwaq 化妝, but lmiwaq 趕走 (12) is the AF of exactly
          this root.  Correct as it stands.
  gluq    G'LOQ 放入鞘中 vs gluq 污垢, but gmluq and hmgluq are both listed
          and glqi/glqan/glqun are level 5.  The stem holds together.

TWO homograph casualties, which cannot be fixed at all: modernize() takes ONE
WORD WITH NO ENTRY CONTEXT, so a key used by two entries that mean different
things gets one value and one of them is wrong.
  tabu   TABU 餵養/飼養 wants tabug 飼養 (x3), but a second TABU is a
         [emprunt jap./chin.] tree name that is correctly tabu (x1).
  kmalao KALAO 攀上 wants mkaraw 爬上(去), but KMALAO 整理、淨化 wants
         kmaraw 清理 (44), and both entries use the token.
Measured: 57 headword keys are shared by entries with no gloss overlap at
all, covering 215 token occurrences — so this ceiling is real but small, and
most of the 57 are harmless (Truku ngungu genuinely is both 尾巴 and 膽小).
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
A = set(json.load(io.open(os.path.join(H, "tools", "orthography",
                                       "attested_modern.json"), encoding="utf-8")))

NEW = [("qlian", "krian"), ("qliyan", "krian"),
       ("skui", "skui"), ("skwi", "skui")]
LIES = {"qrian": "被圍繞 — the 圍 root, not 挖掘",
        "skuy": "冷;涼 — not 儲存"}
KEPT = {"gumuk": "g'muk", "liwaq": "liwak", "gluq": "g'loq"}

print("-- the map")
for k, v in NEW:
    check(MAN.get(k) == v and MAP.get(k) == v,
          "%-8s -> %-7s (manual=%s map=%s)" % (k, v, MAN.get(k), MAP.get(k)))
check(len(MAN) == 1754, "manual_map 1750 -> 1754: %d" % len(MAN))
check("krian" in A and "kriyan" not in A,
      "krian is listed and kriyan is not — that is why both go to krian")
check("skui" in A, "skui is itself listed, so the slot stays dark and is right")

print("\n-- the two lies are unreferenced")
for w, why in sorted(LIES.items()):
    ks = sorted(k for k in MAP if MAP[k] == w)
    check(not ks, "%-6s (%s): %s" % (w, why, ks or "gone"))

print("\n-- the three deliberate keeps are untouched")
for v, k in sorted(KEPT.items()):
    check(MAP.get(k) == v, "%-8s still -> %-7s (%s)" % (k, v, MAP.get(k)))

print("\n-- the two homograph casualties are left alone")
check(MAP.get("tabu") == "tabu",
      "tabu stays tabu — the second TABU is a jap./chin. tree loan: %s"
      % MAP.get("tabu"))
check(MAP.get("kmalao") == "kmaraw",
      "kmalao stays kmaraw — KMALAO 整理 owns it too: %s" % MAP.get("kmalao"))

print("\n-- verified.js")
L = collections.Counter(V.values())
check(len(V) == 4694, "verified 4693 -> 4694: %d" % len(V))
check(L[1] == 3894, "level 1 LISTED 3893 -> 3894: %d" % L[1])
check([L[i] for i in (2, 3, 4, 5, 6, 7)] == [600, 54, 67, 38, 31, 10],
      "derived levels unmoved: %s" % [L[i] for i in (2, 3, 4, 5, 6, 7)])

URL = "http://127.0.0.1:8765/?q=%CC%81"
SPANS = """(ws) => { const r = {};
  for (const n of document.querySelectorAll('span.w-mod,span.w-unv,span.w-raw')) {
    const t = n.textContent.trim().toLowerCase();
    if (ws.indexOf(t) < 0) continue;
    const s = n.className.indexOf('w-mod') >= 0 ? 'dark'
            : n.className.indexOf('w-unv') >= 0 ? 'PALE' : 'GREEN';
    (r[t] = r[t] || {})[s] = (r[t][s] || 0) + 1;
  } return r; }"""
WATCH = ["krian", "kriyan", "qrian", "skui", "skuy", "tabu", "kmaraw",
         "gumuk", "liwaq", "gluq"]
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
        res[mode] = ({k: pg.evaluate(
            '()=>document.querySelectorAll("span.%s").length' % k)
            for k in ("w-mod", "w-unv", "w-raw")},
            len(errs),
            pg.evaluate('()=>document.querySelectorAll("article.entry").length'))
        if mode == "modern":
            seen = pg.evaluate(SPANS, WATCH)
        ctx.close()
    b.close()

(cm, em, dm), (co, eo, do) = res["modern"], res["original"]
tm, to = sum(cm.values()), sum(co.values())

print("\n-- the census")
check(cm == {"w-mod": 41063, "w-unv": 3372, "w-raw": 32},
      "modern 41060/3377/32 -> 41063/3372/32: %s" % cm)
check(tm == 44467 and abs(100.0 * cm["w-mod"] / tm - 92.34) < 0.005,
      "modern total 44469 -> 44467, dark 92.33%% -> 92.34%%: %d %.4f"
      % (tm, 100.0 * cm["w-mod"] / tm))
check(co == {"w-mod": 41506, "w-unv": 3424, "w-raw": 32},
      "original 41501/3429/32 -> 41506/3424/32: %s" % co)
check(to == 44962, "original total still 44962: %d" % to)
check(41063 - 41060 == 3 and 3377 - 3372 == 5 and 3 - 5 == -2,
      "modern deltas: dark +3, pale -5, green 0, total -2")
check(dm == 1967 and do == 1967, "1967 cards: %d %d" % (dm, do))
check(not em and not eo, "no page errors: %d %d" % (em, eo))
check(seen.get("krian") == {"dark": 5},
      "the -2 is QALI: his qlian and qliyan converge on krian x5: %s"
      % seen.get("krian"))

print("\n-- the DOM")
for w in ("qrian", "skuy", "kriyan"):
    check(w not in seen, "%-7s absent: %s" % (w, seen.get(w)))
check(seen.get("skui") == {"dark": 6}, "skui dark x6: %s" % seen.get("skui"))
for w in ("gumuk", "liwaq", "gluq"):
    check(w in seen, "%-7s still on the page (kept on purpose): %s"
          % (w, seen.get(w)))

print("\n%s  (%d failed)" % ("PASS" if not fail else "FAILURES", len(fail)))
for m in fail:
    print("   " + m)
sys.exit(1 if fail else 0)
