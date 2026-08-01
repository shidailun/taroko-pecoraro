# -*- coding: utf-8 -*-
"""Batch 123 — three families whose dark claim named the wrong existing word.

Sourced by sharpening the claim audit twice.  claimaudit.py collects a token's
governing gloss from EXAMPLE SENTENCES as well as form slots, so its 852
suspects are dominated by tokens attached to whole-clause translations (`kari`
x120 @ALANG "claims 挖掘" against four sentences about talking) — the same
evidence batches 121 and 122 had to discard by hand.  claimaudit2.py takes the
gloss from hw / paradigm / sub form / sub paradigm ONLY: 417 suspects.  Those
were re-ranked by real page occurrences (rank122.py — claimaudit2 counts only
glossing slots and comes out flat at x1-x4), and then filtered by the test that
made boyaq obvious: not "shares >=2 Han characters" but **some attested
near-shape carries one of his gloss SEGMENTS whole**.  417 -> 73.

  boyaq   -> bowyak   242x 山豬.  His BOYAQ is 山豬／野豬 and the map claimed
                      buyak 動物肢解 — the butchering of the animal, not the
                      animal.  All 12 sentence occurrences are the boar
                      (ADOP 你要獵什麼…山豬, WAKAT 山豬的獠牙, XNUK 山豬肉).
  mtboyaq -> mtbowyak 4x 掙扎.  His sub Tboyaq 痛得打滾－在地上翻滾 he flags
                      himself: 「詞根 BOYAQ？」.  The corpus vindicates the
                      guess — 掙扎 is his own 翻來覆去 sentence about Tenong
                      not sleeping.  tbowyak stays PALE: blind, but regular
                      off a stem the corpus has now proved.
  qalang  -> karang   36x 螃蟹.  The idtrap pattern exactly: an identity claim
                      (qalang is 柵欄) blocking a char-ruled form that is
                      attested speech and whose gloss agrees with the entry.
  mqalang -> mkarang  2x, and mqqalang -> mkkarang 7x 爬行 — his Mqqalang is
                      像螃蟹一樣爬行 and his sentence is 他用四肢爬行.
  lbangan -> lbangan  was rbangan 做陷阱的地方 against his 寬度－尺寸.
  plabang -> plabang  was prabang 做標靶 against his 加寬－增大－擴建.
  plbangan/mplabang follow the same stem (emplabang: empl is 14 types / 40
                      tokens, so the schwa branch is licit).

LABANG is the 寬闊/誇大 split batch 43 left open, and the omnibus settles it by
gloss, not by shape: EVERY word glossing 寬 is on the l side — labang 3x 寬,
llabang 16x, knlabang 2x 寬度, knlbangan 11x 寬度, klbangan 寬廣, mslabang
已經寬, slbangun 使成寬的 — and not one r-form glosses 寬 (rabang 較多, rmabang
得的多, prabang 做標靶, rbangan 做陷阱的地方).  lbangan is not attested alone but
sits inside knlbangan 11x and klbangan whole.

KEPT deliberately: lmabang -> rmabang 得的多.  His Lmabang is 增加－添加－加寬
and his sentence is 那會增添好處 — the 過多 half of his own headword gloss
寬闊－過多, which is the r side.  Also untouched: mk'alang -> mkealang, the
部落 word tier S was warned about, which shares no key with QALANG 螃蟹.

NOT TAKEN, and the reason matters because his ° line flags it:
  TUTWI's paradigm reads ° Tmutwi, tutwi, ttui, ttuyan, ttuyun — four members
  on ttuy- and one on ttui, which is 切、剁.  But ttui is also TA'TO's word
  (his cut root), where 切、剁 is RIGHT, and modernize() takes one word with no
  entry context.  Ninth per-token conflict, after IYAX, LAWA, NGALI, ULAE,
  K'LAE, QALO, TABU, kmalao.
  tlawai @TLAWAI 蝴蝶 claims tlaway 箭步如飛 with klaway 54x 蝴蝶 sitting
  beside it — refused, because batch 22 already adjudicated KLAWAI/TLAWAI
  ("54x and 28x, both real") and a gloss-shape hit does not overturn that.
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

NEW = [("boyaq", "bowyak"), ("tboyaq", "tbowyak"), ("mtboyaq", "mtbowyak"),
       ("qalang", "karang"), ("mqalang", "mkarang"), ("mqqalang", "mkkarang"),
       ("lbangan", "lbangan"), ("plabang", "plabang"),
       ("plbangan", "plbangan"), ("mplabang", "emplabang")]
LIES = {"buyak": "動物肢解 — the butchering, not the boar",
        "mtbuyak": "off the same wrong stem",
        "rbangan": "做陷阱的地方 — not 寬度",
        "prabang": "做標靶 — not 加寬",
        "prbangan": "the same stem",
        "emprabang": "the same stem",
        "mqarang": "l>r on a q- root that is really k-"}

print("-- the map")
for k, v in NEW:
    check(MAN.get(k) == v and MAP.get(k) == v,
          "%-9s -> %-10s (manual=%s map=%s)" % (k, v, MAN.get(k), MAP.get(k)))
check(len(MAN) == 1764, "manual_map 1754 -> 1764: %d" % len(MAN))
for w in ("bowyak", "mtbowyak", "karang", "mkarang", "mkkarang"):
    check(w in A, "%-9s is listed — the claim is attested, not blind" % w)
check("tbowyak" not in A,
      "tbowyak is NOT listed, so it stays pale — the one honest blind slot")

print("\n-- every wrong value is unreferenced")
for w, why in sorted(LIES.items()):
    ks = sorted(k for k in MAP if MAP[k] == w)
    check(not ks, "%-10s (%s): %s" % (w, why, ks or "gone"))

print("\n-- the l side of LABANG holds together")
for k, v in (("labang", "labang"), ("llabang", "llabang"),
             ("mlabang", "mlabang"), ("slabang", "slabang"),
             ("mslabang", "mslabang"), ("knlbangan", "knlbangan"),
             ("plbangi", "plbangi"), ("plbangun", "plbangun")):
    check(MAP.get(k) == v, "%-10s still -> %-10s (%s)" % (k, v, MAP.get(k)))
check(MAP.get("lmabang") == "rmabang",
      "lmabang stays rmabang 得的多 — his 增加－添加 is the 過多 half: %s"
      % MAP.get("lmabang"))

print("\n-- the two words that must NOT have moved")
check(MAP.get("mk'alang") == "mkealang",
      "mk'alang is alang 部落, not karang 蟹 (tier S's own warning): %s"
      % MAP.get("mk'alang"))
check(MAP.get("ttui") == "ttui",
      "ttui stays — TA'TO 切、剁 owns it too, so TUTWI's ° line cannot be "
      "honoured: %s" % MAP.get("ttui"))
check(MAP.get("tlawai") != "klaway",
      "tlawai is not moved onto klaway — batch 22 adjudicated it: %s"
      % MAP.get("tlawai"))

print("\n-- verified.js")
L = collections.Counter(V.values())
check(len(V) == 4698, "verified 4694 -> 4698: %d" % len(V))
check(L[1] == 3894, "level 1 LISTED still 3894: %d" % L[1])
check([L[i] for i in (2, 3, 4, 5, 6, 7)] == [602, 54, 68, 38, 32, 10],
      "derived levels 600/54/67/38/31/10 -> %s" % [L[i] for i in (2, 3, 4, 5, 6, 7)])

URL = "http://127.0.0.1:8765/?q=%CC%81"
SPANS = """(ws) => { const r = {};
  for (const n of document.querySelectorAll('span.w-mod,span.w-unv,span.w-raw')) {
    const t = n.textContent.trim().toLowerCase();
    if (ws.indexOf(t) < 0) continue;
    const s = n.className.indexOf('w-mod') >= 0 ? 'dark'
            : n.className.indexOf('w-unv') >= 0 ? 'PALE' : 'GREEN';
    (r[t] = r[t] || {})[s] = (r[t][s] || 0) + 1;
  } return r; }"""
WATCH = ["bowyak", "buyak", "tbowyak", "mtbowyak", "mtbuyak", "karang",
         "qalang", "mkarang", "mkkarang", "mqarang", "lbangan", "rbangan",
         "plabang", "prabang", "plbangan", "prbangan", "emplabang",
         "emprabang", "rmabang", "mkealang"]
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
check(cm == {"w-mod": 41067, "w-unv": 3368, "w-raw": 32},
      "modern 41063/3372/32 -> 41067/3368/32: %s" % cm)
check(tm == 44467 and abs(100.0 * cm["w-mod"] / tm - 92.3539) < 0.0005,
      "modern total still 44467, dark 92.3449%% -> 92.3539%%: %d %.4f"
      % (tm, 100.0 * cm["w-mod"] / tm))
check(co == {"w-mod": 41510, "w-unv": 3420, "w-raw": 32},
      "original 41506/3424/32 -> 41510/3420/32: %s" % co)
check(to == 44962, "original total still 44962: %d" % to)
check(41067 - 41063 == 4 and 3372 - 3368 == 4,
      "modern deltas: dark +4, pale -4, green 0, total 0 — no bracket collapsed")
check(dm == 1967 and do == 1967, "1967 cards: %d %d" % (dm, do))
check(not em and not eo, "no page errors: %d %d" % (em, eo))

print("\n-- the DOM: 26 wrong-word occurrences repainted")
EXP = {"bowyak": {"dark": 14}, "mtbowyak": {"dark": 1},
       "tbowyak": {"PALE": 1}, "karang": {"dark": 3},
       "mkarang": {"dark": 1}, "mkkarang": {"dark": 1},
       "lbangan": {"dark": 2}, "plabang": {"dark": 2},
       "plbangan": {"dark": 1}, "emplabang": {"dark": 1}}
for w in sorted(EXP):
    check(seen.get(w) == EXP[w], "%-10s %s (got %s)" % (w, EXP[w], seen.get(w)))
for w in ("buyak", "mtbuyak", "qalang", "mqarang", "rbangan", "prabang",
          "prbangan", "emprabang"):
    check(w not in seen, "%-10s absent from the page: %s" % (w, seen.get(w)))
check(seen.get("rmabang") == {"dark": 2},
      "rmabang kept x2 (his 過多 half): %s" % seen.get("rmabang"))
check(seen.get("mkealang") == {"dark": 7},
      "mkealang untouched x7: %s" % seen.get("mkealang"))

print("\n%s  (%d failed)" % ("PASS" if not fail else "FAILURES", len(fail)))
for m in fail:
    print("   " + m)
sys.exit(1 if fail else 0)
