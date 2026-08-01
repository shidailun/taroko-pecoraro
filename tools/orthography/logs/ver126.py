# -*- coding: utf-8 -*-
"""Batch 126 — HIS OWN ° PARADIGM LINE CAN CONTAIN THE ANSWER TO ITS OWN STRAGGLER.

Two keys, and the first is the shape worth the paragraph.

1. pgiai -> pgyai 要守住.  His GAYA 習俗——規範——傳統——禁忌 carries the paradigm line

       ° Mpgaya, pgaya, pgiai, pgyaan, pgyaon.

   and the map had already adjudicated two of its three suffixed slots onto the
   SHORTENED stem: pgyaan (曾忌諱地) stands as he wrote it, and pgyaon -> pgyaun
   要遵守禁忌.  So the stem question was settled inside the entry — the -iya- of
   his pgiai is the -ya- of his own pgyaan sitting two words to the right — and
   pgiai was simply the slot nobody came back for.  It was mapped to pgiyai, 0x
   everywhere, against pgyai 2x, whose two sentences are

       Pgyai bi muda ka gaya.                              要守住律法。
       Tthlmadan namu hlmadan nami o pgyai bi ka yamu       ...你們男孩子一定
       laqi snaw ha.                                       要有禮貌。

   — his 使之成為法規、習俗 in the imperative, twice.  The half-brown card again
   (GALANG, DUI, XBUI, SKUI): where a family has already committed, the straggler
   is not a research question, it is an unfinished edit.  The novelty here is only
   that the committed members are printed IN THE SAME LINE as the straggler, which
   is as local as this evidence ever gets.

2. knsxeaan -> knshyaan 味道.  His Knsxeaan is glossed 味道－香氣－風味 and
   knshyaan is 4x in speech; the two occurrences that come with a Chinese sentence
   are

       Knshyaan bgu rudux o ana ima smkuxul mimah.     雞湯的味道無論誰都愛喝。
       Mgmeenu knshyaan ka qsiya gsilung?              海水是什麼味道？

   His word for word.  It was on knshiyaan, 0x, while its own family is already
   right beside it — knsxea -> knshiya 17x 甘甜 (his 味道的濃度、品質) and
   sxea -> shiya 30x 好吃；好喝；美味的.  Same one-slot residue as (1), one
   morpheme further out.

REFUSED, and it is the more interesting half.  tdoaon -> tdwaun looked like the
same shortening: tduwa 515x 可以 is his TDOA 能夠 exactly, and the shortened stem
is real — tdwani 要做朋友, tdwanay 不要…做朋友, ptdwai 瞧不起 are all attested.
But every one of them means 做朋友, not 能夠.  The bare stem carries his sense and
the SUFFIXED stem carries a different one, so the correspondence holds and the word
is still not his; tdoaon keeps the long-stem tduwaun, which is a blind suffixation
of a root the corpus proves 515 times rather than a claim on a word that means
something else.  A real shortening can still name the wrong word — batch 124's
lesson arriving from the opposite direction.

Left alone and noted: pngyaan -> pngyaan is an identity claim on a form that is 0x,
and pnegyaan (the schwa reading) is 0x and unlisted too.  There is nothing to move
it to, so the claim stays where it is rather than being traded for a different
0x string.
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

NEW = [("pgiai", "pgyai"), ("knsxeaan", "knshyaan")]
LIES = {"pgiyai": "0x — the unshortened stem his own paradigm line abandons",
        "knshiyaan": "0x — beside knshiya 17x and shiya 30x"}

print("-- the map")
for k, v in NEW:
    check(MAN.get(k) == v and MAP.get(k) == v,
          "%-9s -> %-9s (manual=%s map=%s)" % (k, v, MAN.get(k), MAP.get(k)))
check(len(MAN) == 1777, "manual_map 1775 -> 1777: %d" % len(MAN))
for w in ("pgyai", "knshyaan"):
    check(w in A and V.get(w) == 1,
          "%-9s is LISTED at level 1 — attested speech, not a blind claim (%s)"
          % (w, V.get(w)))
for w in ("pgiyai", "knshiyaan"):
    check(w not in A and w not in V,
          "%-10s is in no wordlist at all — the value we moved off was never a "
          "modern word" % w)

print("\n-- every value we moved off is unreferenced")
for w, why in sorted(LIES.items()):
    ks = sorted(k for k in MAP if MAP[k] == w)
    check(not ks, "%-10s (%s): %s" % (w, why, ks or "gone"))

print("\n-- the two committed members that decided (1), unmoved")
for k, v in (("pgyaon", "pgyaun"), ("pgyaan", "pgyaan")):
    check(MAP.get(k) == v,
          "%-8s -> %-8s — already on the shortened stem before this batch (%s)"
          % (k, v, MAP.get(k)))
check(V.get("pgyaun") == 1 and V.get("pgyaan") == 1,
      "both are LISTED (要遵守禁忌 / 曾忌諱地): %s %s"
      % (V.get("pgyaun"), V.get("pgyaan")))
check(MAP.get("pgaya") == "pgaya" and V.get("pgaya") == 1,
      "pgaya unchanged and listed — the bare slot needs no shortening (%s %s)"
      % (MAP.get("pgaya"), V.get("pgaya")))

print("\n-- the family that decided (2), unmoved")
for k, v in (("sxea", "shiya"), ("knsxea", "knshiya")):
    check(MAP.get(k) == v, "%-9s -> %-9s (%s)" % (k, v, MAP.get(k)))
check(V.get("shiya") == 1 and V.get("knshiya") == 1,
      "shiya 30x 好吃；好喝；美味的 and knshiya 17x 甘甜 are both LISTED: %s %s"
      % (V.get("shiya"), V.get("knshiya")))

print("\n-- the refusal, and the thing left alone")
check(MAP.get("tdoaon") == "tduwaun",
      "tdoaon still -> tduwaun, NOT tdwaun — the shortened stem's attested "
      "suffixed forms all mean 做朋友, not his 能夠 (%s)" % MAP.get("tdoaon"))
check("tdwaun" not in MAP.values(), "tdwaun reaches the page nowhere")
for k in ("tdwani", "tdwanay", "ptdwai"):
    check(k not in MAP, "%-8s is not a key of his — it is only the corpus "
          "evidence the refusal was read off" % k)
check(MAP.get("pngyaan") == "pngyaan" and "pnegyaan" not in A,
      "pngyaan keeps its identity claim: pnegyaan is unlisted too, so there is "
      "nothing to move it to (%s)" % MAP.get("pngyaan"))

print("\n-- verified.js")
L = collections.Counter(V.values())
check(len(V) == 4709, "verified 4707 -> 4709: %d" % len(V))
check([L[i] for i in range(1, 8)] == [3899, 606, 54, 70, 38, 32, 10],
      "levels 3897/606/54/70/38/32/10 -> %s (both new values are LISTED, so the "
      "whole move is in level 1)" % [L[i] for i in range(1, 8)])

URL = "http://127.0.0.1:8765/?q=%CC%81"
SPANS = """(ws) => { const r = {};
  for (const n of document.querySelectorAll('span.w-mod,span.w-unv,span.w-raw')) {
    const t = n.textContent.trim().toLowerCase();
    if (ws.indexOf(t) < 0) continue;
    const s = n.className.indexOf('w-mod') >= 0 ? 'dark'
            : n.className.indexOf('w-unv') >= 0 ? 'PALE' : 'GREEN';
    (r[t] = r[t] || {})[s] = (r[t][s] || 0) + 1;
  } return r; }"""
WATCH = ["pgyai", "pgiai", "pgiyai", "knshyaan", "knsxeaan", "knshiyaan",
         "pgyaan", "pgyaun", "knshiya", "shiya", "pgaya"]
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
check(cm == {"w-mod": 41093, "w-unv": 3340, "w-raw": 32},
      "modern 41090/3343/32 -> 41093/3340/32: %s" % cm)
check(tm == 44465 and abs(100.0 * cm["w-mod"] / tm - 92.4165) < 0.0005,
      "modern total still 44465, dark 92.4098%% -> 92.4165%%: %d %.4f"
      % (tm, 100.0 * cm["w-mod"] / tm))
check(co == {"w-mod": 41538, "w-unv": 3392, "w-raw": 32},
      "original 41535/3395/32 -> 41538/3392/32: %s" % co)
check(to == 44962, "original total still 44962: %d" % to)
check(cm["w-raw"] == 32 and co["w-raw"] == 32,
      "green still 32 in both modes — nothing fell out of the map")
check(dm == 1967 and do == 1967, "1967 cards: %d %d" % (dm, do))
check(not em and not eo, "no page errors: %d %d" % (em, eo))

print("\n-- the DOM")
EXP = {"pgyai": {"dark": 1}, "knshyaan": {"dark": 2},
       "pgyaan": {"dark": 1}, "pgyaun": {"dark": 3},
       "knshiya": {"dark": 4}, "shiya": {"dark": 2}, "pgaya": {"dark": 3}}
for w in sorted(EXP):
    check(seen.get(w) == EXP[w], "%-10s %s (got %s)" % (w, EXP[w], seen.get(w)))
for w in ("pgiai", "pgiyai", "knsxeaan", "knshiyaan"):
    check(w not in seen, "%-10s absent from the page: %s" % (w, seen.get(w)))

print("\n%s  (%d failed)" % ("PASS" if not fail else "FAILURES", len(fail)))
for m in fail:
    print("   " + m)
sys.exit(1 if fail else 0)
