# -*- coding: utf-8 -*-
"""Batch 125 — A STEM CAN SHORTEN BEFORE ITS SUFFIX, which overturns batch 19.

Three fixes, and the third is a finding rather than a word.

1. xpuyan -> puyan 廚房.  15 occurrences, and it was mapped to hpuyan 34x 要為…煮,
   which is the verbal slot his paradigm asks for.  THE SENTENCES DECIDE: eleven
   of his thirteen sentence occurrences are the kitchen, nine of them in the
   fixed phrase `sapax xpuyan`, and only two are verbal.  puyan is 20x 廚房.
   Both values are level 1, so the census does not move at all — this is a
   correctness fix and nothing else, which is exactly the class most likely to be
   left undone because no counter rewards it.

2. PEIDANG — his suffixed forms are 0x on a stem the modern language does not
   build.  The root is eydang: meydang 29x 迷路, mneydang 10x, empeydang 3x
   會迷路.  His Pgdangun / Pgdangi / Pgdangan were identity-ish claims on
   pgdang-, which is 0x everywhere, while the modern suffixed stem is prdang-:
   prdangun 3x 遺失；弄丟；丟了 is his gloss word for word.  It is the ONLY
   attested member — prdangi and prdangan are 0x, and derive at level 4 off it
   rather than being claimed outright, which is the honest slot for them: they
   are regular suffixations of a stem the corpus proves once, against forms on a
   stem the corpus does not write at all.  (His bare peidang -> peydang 49x is
   glossed 人名（男）and was
   left alone: that is the batch-124 shape, a bare-root omnibus gloss recording a
   homonym, and the family says nothing against the road it is already on.)

3. KLUI — batch 19's identity pins on kluyun / skluyun / pskluyun, OVERTURNED.
   Their stated basis is in CLAUDE.md: "There is no modern -un form of any -uwi
   root on record, so pskluwiun would be an invention."  The finding was true as
   written and false as reasoned, because THE STEM SHORTENS BEFORE THE SUFFIX.
   kluwi + un is not kluwiun, it is klwiun — 1x — and sklwiun is 22x 奇妙.
   Nobody found them because everybody, myself included, searched for the
   unshortened shape and read the silence as evidence about the language.  The
   correspondence was already half-written in the map: mklui -> mkluwi,
   sklui -> skluwi, msklui -> mskluwi were adjudicated batches ago, so the -uy-
   / -wi- pairing was never in doubt; only the suffixed shape was.

   That is why this is worth a paragraph rather than a line.  An identity pin is
   a verdict, and a verdict reached from a corpus search is only as good as the
   shape that was searched for.  klwiun and sklwiun are attested speech, so the
   three pins were asserting his spelling was already modern about strings the
   modern language does write — differently.

Two more shapes of the same kind were probed and refused (shapevar.py, which
applies uy>wi, uwa>wa, iya>ya and the schwa alternations to every pale value with
no witness and asks whether the RESULT is attested).  The class is nearly
exhausted: three rows in the whole dictionary, and one of them is a trap —
tdoaon -> tdwaun looks right (tduwa 515x 可以 is his TDOA 能夠 exactly) and is
not, because the only attested tdwa- suffixed forms are tdwani 要做朋友 and
tdwanay 不要…做朋友.  The bare stem carries his sense and the suffixed stem
carries a different one, so the shortening is real and the word is not his.
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

NEW = [("xpuyan", "puyan"),
       ("pgdangun", "prdangun"), ("pgdangi", "prdangi"),
       ("pgdangan", "prdangan"),
       ("kluyun", "klwiun"), ("skluyun", "sklwiun"),
       ("pskluyun", "psklwiun")]
LIES = {"hpuyan": "34x 要為…煮 — the verbal slot, but 11 of his 13 are the kitchen",
        "pgdangun": "0x — a stem the modern language does not build",
        "pgdangi": "0x", "pgdangan": "0x",
        "kluyun": "batch 19's pin, on a string the language writes klwiun",
        "skluyun": "ditto, against sklwiun 22x 奇妙",
        "pskluyun": "ditto"}

print("-- the map")
for k, v in NEW:
    check(MAN.get(k) == v and MAP.get(k) == v,
          "%-9s -> %-9s (manual=%s map=%s)" % (k, v, MAN.get(k), MAP.get(k)))
check(len(MAN) == 1775, "manual_map 1772 -> 1775 (three pins overwritten, so "
      "the count moves by the four new keys only): %d" % len(MAN))
for w in ("puyan", "prdangun", "klwiun", "sklwiun"):
    check(w in A, "%-9s is listed — attested, not blind" % w)
for w, lvl in (("psklwiun", 2), ("prdangi", 4), ("prdangan", 4)):
    check(w not in A and V.get(w) == lvl,
          "%-9s is NOT listed — it DERIVES, at level %d (%s).  prdangun is the "
          "only attested member of its family; these two are regular "
          "suffixations of it, not claims" % (w, lvl, V.get(w)))

print("\n-- every value we moved off is unreferenced")
for w, why in sorted(LIES.items()):
    ks = sorted(k for k in MAP if MAP[k] == w)
    check(not ks, "%-9s (%s): %s" % (w, why, ks or "gone"))

print("\n-- batch 19 is overturned on evidence, so its premise must be false")
check(V.get("klwiun") == 1 and V.get("sklwiun") == 1,
      "klwiun and sklwiun are both LISTED — there IS a modern -un form of a "
      "-uwi root, which is the whole of batch 19's reasoning: %s %s"
      % (V.get("klwiun"), V.get("sklwiun")))
check(V.get("psklwiun") == 2,
      "psklwiun derives at level 2 off the stem the corpus just proved: %s"
      % V.get("psklwiun"))
for k, v in (("klui", "kluwi"), ("mklui", "mkluwi"), ("sklui", "skluwi"),
             ("msklui", "mskluwi")):
    got = MAP.get(k) or "(WORD_OVERRIDES)"
    check(got in (v, "(WORD_OVERRIDES)"),
          "%-8s still resolves on the long stem %-8s — the shortening is a fact "
          "about the SUFFIXED slot only (%s)" % (k, v, got))

print("\n-- the eydang family around the fix")
for k, v in (("peidang", "peydang"), ("meidang", "meydang")):
    check(MAP.get(k) == v, "%-9s still -> %-9s (%s)" % (k, v, MAP.get(k)))
check(V.get("prdangun") == 1,
      "prdangun LISTED — 3x 遺失；弄丟；丟了, his gloss verbatim: %s"
      % V.get("prdangun"))

print("\n-- xpuyan, and what it must NOT have dragged")
check(V.get("puyan") == 1, "puyan LISTED (20x 廚房): %s" % V.get("puyan"))
check("hpuyan" not in MAP.values(),
      "hpuyan is off the page entirely — he has no other slot wanting it")
check(MAP.get("tdoaon", "tdoaon") == "tdoaon" or
      MAP.get("tdoaon") == "tduwaun",
      "tdoaon NOT moved to tdwaun — the shortened stem carries 做朋友, not his "
      "能夠 (%s)" % MAP.get("tdoaon"))

print("\n-- verified.js")
L = collections.Counter(V.values())
check(len(V) == 4707, "verified 4701 -> 4707: %d" % len(V))
check([L[i] for i in range(1, 8)] == [3897, 606, 54, 70, 38, 32, 10],
      "levels 3894/605/54/68/38/32/10 -> %s" % [L[i] for i in range(1, 8)])

URL = "http://127.0.0.1:8765/?q=%CC%81"
SPANS = """(ws) => { const r = {};
  for (const n of document.querySelectorAll('span.w-mod,span.w-unv,span.w-raw')) {
    const t = n.textContent.trim().toLowerCase();
    if (ws.indexOf(t) < 0) continue;
    const s = n.className.indexOf('w-mod') >= 0 ? 'dark'
            : n.className.indexOf('w-unv') >= 0 ? 'PALE' : 'GREEN';
    (r[t] = r[t] || {})[s] = (r[t][s] || 0) + 1;
  } return r; }"""
WATCH = ["prdangun", "prdangi", "prdangan", "klwiun", "sklwiun", "psklwiun",
         "puyan", "pgdangun", "pgdangi", "pgdangan", "kluyun", "skluyun",
         "pskluyun", "xpuyan", "hpuyan", "peydang", "meydang"]
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
check(cm == {"w-mod": 41090, "w-unv": 3343, "w-raw": 32},
      "modern 41077/3356/32 -> 41090/3343/32: %s" % cm)
check(tm == 44465 and abs(100.0 * cm["w-mod"] / tm - 92.4098) < 0.0005,
      "modern total still 44465 (no convergence this time), dark 92.3805%% -> "
      "92.4098%%: %d %.4f" % (tm, 100.0 * cm["w-mod"] / tm))
check(co == {"w-mod": 41535, "w-unv": 3395, "w-raw": 32},
      "original 41522/3408/32 -> 41535/3395/32: %s" % co)
check(to == 44962, "original total still 44962: %d" % to)
check(cm["w-raw"] == 32 and co["w-raw"] == 32,
      "green still 32 in both modes — nothing fell out of the map")
check(dm == 1967 and do == 1967, "1967 cards: %d %d" % (dm, do))
check(not em and not eo, "no page errors: %d %d" % (em, eo))

print("\n-- the DOM")
EXP = {"prdangun": {"dark": 3}, "prdangi": {"dark": 2},
       "prdangan": {"dark": 1}, "klwiun": {"dark": 3},
       "sklwiun": {"dark": 2}, "psklwiun": {"dark": 2},
       "puyan": {"dark": 15}}
for w in sorted(EXP):
    check(seen.get(w) == EXP[w], "%-10s %s (got %s)" % (w, EXP[w], seen.get(w)))
for w in ("pgdangun", "pgdangi", "pgdangan", "kluyun", "skluyun", "pskluyun",
          "xpuyan", "hpuyan"):
    check(w not in seen, "%-10s absent from the page: %s" % (w, seen.get(w)))
for w in ("peydang", "meydang"):
    check(w in seen, "%-9s still on the page: %s" % (w, seen.get(w)))

print("\n%s  (%d failed)" % ("PASS" if not fail else "FAILURES", len(fail)))
for m in fail:
    print("   " + m)
sys.exit(1 if fail else 0)
