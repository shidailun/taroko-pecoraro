# -*- coding: utf-8 -*-
"""Batch 124 — one adjectival 的 was hiding a wrong-word claim; and PUSA.

Two sources.

1. THE TAIL STRIP.  sharp122's test — "some attested near-shape carries one of
his gloss SEGMENTS whole" — is the sharp one (batch 123 cut 417 suspects to 73
with it), but it was failing on a single character.  HIS GLOSSES ARE ADJECTIVAL
WHERE THE OMNIBUS'S ARE BARE: his SDAMAT is 思念的 and csdamat is 思念, so the
whole-segment test said no and left a wrong dark claim standing.  sharp124 strips
a trailing [的地得者之過了]+ and keeps BOTH forms: 70 claims / 811 occurrences ->
77 / 834, and the seven new ones are exactly where the tail mattered.

Five of those seven are FALSE POSITIVES, all of one shape — THE OMNIBUS'S GLOSS
FOR A BARE ROOT RECORDS A HOMONYM OR A NARROW SENSE, NOT THE ROOT'S MEANING:
  banax  claims banah 人名（男）  — but embanah 183x 紅色的, kbanah 染紅,
         knbanah 紅的樣子, tnbanah 紅衣者.  banah IS the red root; the omnibus
         entry for the bare form happens to gloss the personal name Banah.
  nalox  claims narux 心傷        — but mnarux 271x 生病；病痛, pknarux 使…生病,
         empknarux 會生病.  His NALOX 疾病－生病的 is that root exactly.
  mgalu  claims mgealu 像…延長線一樣 — the cord homonym, but gnealu 50x 恩典慈愛,
         gmealu 25x 同情;疼惜, sgealu 23x 可憐, mggealu 7x 相愛 put the love
         sense on the same root, which is what batch 38 already settled.
  mqeta  claims mqita 視察 — correct: qita 56x 注視;看.
  tnlalae claims tnlealay 4x 已經先 — correct: his 實際上在先、在前者.
The lesson generalises: a bare-root omnibus gloss is one lexicographer's pick
among the root's senses, so it cannot refute a claim the root's FAMILY supports.
Only two survived — and both name a different EXISTING word, which is the class
worth fixing.

  sdamat -> csdamat 17x 思念;寂寞;哀傷;哀慟;哀思.  His SDAMAT is 思念的（？）－
         悲傷的（？）－沮喪的（？）－感動的（？）, word for word, and the map
         claimed sdamat 7x 菜；菜餚 — a side dish.  The damat root carries both
         senses and the modern family splits them cleanly: every s-form is food
         (sdamat 菜餚, sddamat 有…的菜味, smddamat 需要很多菜餚, spdamat 以…做
         菜餚) and the 思念 sense NEVER appears with bare s- (kdamat 想念;懷念,
         kmdamat 好想念, smdamat 懷念；想念, csdamat 思念, pcsdamat 使…寂寞,
         empkdamat 會懷念).  He flags the ambiguity himself, twice: under DAMAT
         「Sdamat（＝詞根？——詞根＝DAMAT？）」 and under SDAMAT 「若此詞並非
         源自詞根 DAMAT，則可能有歧義」.  His own Tsdamat -> csdamat was taken
         in batch 36, so the two converge; a convergence costs spans (modern
         total 44467 -> 44465) and is still better than a dark claim naming the
         wrong word.
  spiyan -> spian 2x 夢見.  The map had it on spiyan 3x 被…塞 — and Pecoraro has
         a SEPARATE entry SPIAN ＝阻塞、堵住（鼻子、管道、水管）－塞子, so the
         dictionary holds both words and the map had crossed them.  He settles
         it in his own hand: the SPI sub-form is headed 「Spian (spiyan)」 and
         the paradigm reads ° Smpi, spi, .?., spian(spiyan), spiun (spiyun).
         His -iyan is modern -ian (lesson www) even where -iyan is licit —
         licit is not the test, WHICH WORD IT IS is the test.  snpiyan follows
         to snpian, which verified.js then derives at level 2.
         `spian` itself is left alone: it is his dream sub-form AND his 阻塞
         headword, so it is a per-token conflict modernize() cannot see.

2. PUSA — a pale identity claim on a string with NO witness anywhere, beside a
108x word that is his gloss verbatim.  His USA family is otherwise fully
resolved (usa 326x, musa 1074x, saan 104x, kmusa 4x, and the suffixed causatives
psai 32x, psaan 75x 放；放置；裝置, psaun 34x), so the hole was conspicuous: only
the bare causative sat on pusa = 0x.  powsa is 108x 放…（放置;放走;放手／嫁出）
and his Pusa is 派遣－遣送－放置－擺放.  The paradigm fits without a remainder,
because modern powsa loses the -w- under suffixation exactly as his does:
powsa / psai / psaan / psaun.  empowsa 2x 放手（嫁出）and ppowsa 3x 放置 confirm
the prefixed stem, so mpusa -> empowsa replaces empusa 0x.  kmpusa -> kmpowsa is
blind — 0x, and T.licit says False — but it is the regular km- of a stem the
corpus has just proved, and his own kmusa is attested at 4x.  It stays PALE,
which is the honest slot for it.

NOT hand-written, and then written anyway BY THE BUILDER — which is the useful
finding.  I declined psdamat -> pcsdamat on the rule this project runs on: a
claim gets moved when it names the WRONG EXISTING WORD, and psdamat is 0x, so it
names no word at all and churning it trades a pale slot for a pale slot.  But
one manual key changes what the generated tiers can see, and after the rebuild
the derivation tiers had propagated the corrected stem on their own:
  psdamat  -> pcsdamat   2x 使…寂寞, his 使悲傷－使人鬱悶.  Level 1.
  mpsdamat -> empcsdamat  level 2.    msdamat -> mcsdamat  level 2.
A STEM FIX PAYS FORWARD THROUGH THE BUILDER, so the hand-written batch is a
floor on the repaint, not a ceiling — and the honest way to size a batch is to
rebuild and read the diff, not to count the keys.  (psdmati and psdmatan did NOT
follow; they are 0x on either stem, so the paradigm is split between pcs- and
ps- forms.  Left as is rather than hand-forced.)

And once, propagation went the WRONG WAY and had to be pinned back:
  sndamat.  The builder took it to cnsdamat 0x.  But sndamat is 4x attested
  speech AND a homograph in his own dictionary — under DAMAT it is 為菜餚起爭執
  (his sentence: 「他們到底在吵什麼？……是為了菜餚！」) and under SDAMAT it is
  曾經悲傷、思念.  The modern corpus attests the FOOD side, which is the side
  bare s- takes throughout this root, so sndamat is pinned to itself.  Fixing a
  stem does not license dragging that stem's homographs along with it.
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
                                       "attested_modern.json"),
                          encoding="utf-8")))

NEW = [("pusa", "powsa"), ("mpusa", "empowsa"), ("kmpusa", "kmpowsa"),
       ("spiyan", "spian"), ("snpiyan", "snpian"), ("sdamat", "csdamat"),
       ("sndamat", "sndamat")]
LIES = {"pusa": "0x everywhere — the hole in an otherwise resolved paradigm",
        "empusa": "0x, and empowsa 2x is the real one",
        "kmpusa": "0x, off the wrong stem",
        "spiyan": "3x 被…塞 — the blocking word, not the dream",
        "snpiyan": "off the same crossed stem",
        "sdamat": "7x 菜；菜餚 — a side dish, not 思念"}

print("-- the map")
for k, v in NEW:
    check(MAN.get(k) == v and MAP.get(k) == v,
          "%-9s -> %-9s (manual=%s map=%s)" % (k, v, MAN.get(k), MAP.get(k)))
check(len(MAN) == 1771, "manual_map 1764 -> 1771 (6 fixes + 1 pin): %d"
      % len(MAN))
for w in ("powsa", "empowsa", "spian", "csdamat"):
    check(w in A, "%-9s is listed — the claim is attested, not blind" % w)
check("kmpowsa" not in A,
      "kmpowsa is NOT listed, so it stays pale — the one honest blind slot")

print("\n-- every wrong value is unreferenced")
for w, why in sorted(LIES.items()):
    ks = sorted(k for k in MAP if MAP[k] == w)
    check(not ks, "%-9s (%s): %s" % (w, why, ks or "gone"))

print("\n-- the USA paradigm is unchanged around the fix")
for k, v in (("usa", "usa"), ("musa", "musa"), ("kmusa", "kmusa"),
             ("psai", "psai"), ("psaan", "psaan"), ("psaon", "psaun"),
             ("saan", "saan")):
    check(MAP.get(k) == v, "%-8s still -> %-8s (%s)" % (k, v, MAP.get(k)))

print("\n-- what must NOT have moved")
check(MAP.get("tsdamat") == "csdamat",
      "tsdamat still csdamat (batch 36) — sdamat converges onto it: %s"
      % MAP.get("tsdamat"))
check(MAP.get("spian", "spian") == "spian",
      "spian left alone — his dream sub-form AND his 阻塞 headword: %s"
      % MAP.get("spian", "spian"))
for k, v, why in (("banax", "banah", "banah IS the red root (embanah 183x)"),
                  ("nalox", "narux", "narux IS the sickness root (mnarux 271x)"),
                  ("mgalu", "mgealu",
                   "gealu IS the love root (gnealu 50x), batch 38"),
                  ("mqeta", "mqita", "mqita 8x 視察 is correct"),
                  ("tnlalae", "tnlealay", "tnlealay 4x 已經先 is correct")):
    check(MAP.get(k) == v, "%-8s still -> %-9s — %s (%s)"
          % (k, v, why, MAP.get(k)))

print("\n-- the stem fix paid forward through the builder, unasked")
for k, v, lvl in (("psdamat", "pcsdamat", 1), ("mpsdamat", "empcsdamat", 2),
                  ("msdamat", "mcsdamat", 2)):
    check(MAP.get(k) == v and V.get(v) == lvl,
          "%-9s -> %-11s level %s — no manual key for it (%s, %s)"
          % (k, v, lvl, MAP.get(k), V.get(V and v)))
for k in ("psdmati", "psdmatan", "sdmatan"):
    check(MAP.get(k, k) == k,
          "%-9s did NOT follow — 0x on either stem, left rather than forced: %s"
          % (k, MAP.get(k, k)))
check(MAP.get("sndamat") == "sndamat" and MAN.get("sndamat") == "sndamat",
      "sndamat PINNED back off cnsdamat 0x — 4x attested, and a homograph "
      "(為菜餚起爭執 under DAMAT, 曾經悲傷 under SDAMAT): %s"
      % MAP.get("sndamat"))
check(not [k for k in MAP if MAP[k] == "cnsdamat"],
      "cnsdamat is referenced by nothing")

print("\n-- verified.js")
L = collections.Counter(V.values())
check(len(V) == 4701, "verified 4698 -> 4701: %d" % len(V))
check(L[1] == 3894, "level 1 LISTED still 3894 — two merged out, pcsdamat in: "
      "%d" % L[1])
check([L[i] for i in (2, 3, 4, 5, 6, 7)] == [605, 54, 68, 38, 32, 10],
      "derived levels 602/54/68/38/32/10 -> %s"
      % [L[i] for i in (2, 3, 4, 5, 6, 7)])
check(V.get("snpian") == 2,
      "snpian derives at level 2 off spian — the stem fix pays twice: %s"
      % V.get("snpian"))
check(V.get("kmpowsa") is None, "kmpowsa unverified: %s" % V.get("kmpowsa"))

URL = "http://127.0.0.1:8765/?q=%CC%81"
SPANS = """(ws) => { const r = {};
  for (const n of document.querySelectorAll('span.w-mod,span.w-unv,span.w-raw')) {
    const t = n.textContent.trim().toLowerCase();
    if (ws.indexOf(t) < 0) continue;
    const s = n.className.indexOf('w-mod') >= 0 ? 'dark'
            : n.className.indexOf('w-unv') >= 0 ? 'PALE' : 'GREEN';
    (r[t] = r[t] || {})[s] = (r[t][s] || 0) + 1;
  } return r; }"""
WATCH = ["powsa", "empowsa", "kmpowsa", "spian", "snpian", "csdamat",
         "pusa", "empusa", "kmpusa", "spiyan", "snpiyan", "sdamat",
         "pcsdamat", "mcsdamat", "empcsdamat", "sndamat", "cnsdamat",
         "banah", "narux", "mgealu", "mqita", "tnlealay"]
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
check(cm == {"w-mod": 41077, "w-unv": 3356, "w-raw": 32},
      "modern 41067/3368/32 -> 41077/3356/32: %s" % cm)
check(tm == 44465 and abs(100.0 * cm["w-mod"] / tm - 92.3805) < 0.0005,
      "modern total 44467 -> 44465 (two convergences), dark 92.3539%% -> "
      "92.3805%%: %d %.4f" % (tm, 100.0 * cm["w-mod"] / tm))
check(co == {"w-mod": 41522, "w-unv": 3408, "w-raw": 32},
      "original 41510/3420/32 -> 41522/3408/32: %s" % co)
check(to == 44962, "original total still 44962 — his own spelling is "
      "unaffected by a convergence in the modern layer: %d" % to)
check(cm["w-raw"] == 32, "green still 32 — nothing fell out of the map")
check(dm == 1967 and do == 1967, "1967 cards: %d %d" % (dm, do))
check(not em and not eo, "no page errors: %d %d" % (em, eo))

print("\n-- the DOM")
EXP = {"powsa": {"dark": 6}, "empowsa": {"dark": 1},
       "kmpowsa": {"PALE": 3}, "spian": {"dark": 4},
       "snpian": {"dark": 1}, "csdamat": {"dark": 5},
       "pcsdamat": {"dark": 2}, "mcsdamat": {"dark": 2},
       "empcsdamat": {"dark": 1}, "sndamat": {"dark": 5}}
for w in sorted(EXP):
    check(seen.get(w) == EXP[w], "%-10s %s (got %s)" % (w, EXP[w], seen.get(w)))
for w in ("pusa", "empusa", "kmpusa", "spiyan", "snpiyan", "sdamat",
          "cnsdamat"):
    check(w not in seen, "%-10s absent from the page: %s" % (w, seen.get(w)))
for w in ("banah", "narux", "mqita", "tnlealay"):
    check(w in seen, "%-9s still on the page (rejected FP): %s"
          % (w, seen.get(w)))

print("\n%s  (%d failed)" % ("PASS" if not fail else "FAILURES", len(fail)))
for m in fail:
    print("   " + m)
sys.exit(1 if fail else 0)
