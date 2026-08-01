# -*- coding: utf-8 -*-
"""Batch 127 — HIS HEADWORD DROPS A FINAL -g, AND THE MAP FOLLOWED IT.

This batch came out of a failed proposal, which is the part worth recording.

The proposal was an EIGHTH verification level: promote a pale value when its
stem's FAMILY carries his sense.  It priced well at first — 105 fires over 936
pale glossed non-name values, 205 occurrences, against a shuffled null of 2.0%,
lift 5.7x.  But a family here is a substring search over the omnibus and its
gloss union grows with it, so the null has to be SIZE-MATCHED, and once it is,
the lift collapses as the family grows:

    famsize   pop   real   null    lift
    2-3       172     23    0.5   46.00x
    4-9       138     36    2.4   15.32x
    10-29      53     15    3.5    4.29x
    30-99      42     26    8.8    2.95x
    100+       10      5    2.5    2.04x

A gloss test over a family is largely measuring the SIZE of the gloss union.
Gated at family <= 9 it is ~95% precision, 59 types / 109 occurrences — so I
read all 59 by hand before writing the level, and the reading killed it: almost
every survivor is a LICIT MORPHOLOGICAL GAP, the class this file already paints
dark from the root (tmbiyax beside mtbiyax 48x, mkingal beside kingal 1626x,
smnkagul beside smkagul, ptasaw beside mtasaw 19x).  A family-gloss level would
mostly re-find what vouched_root is already for, at a much looser gloss test,
and would promote 46 IDENTITY claims — the state where a wrong dark does the
most damage.  So: no eighth level.

What the reading DID find is three entries of a shape no sweep had asked about,
and generalizing THAT is the batch.  The test is as sharp as evidence gets here
— not a family union but the word itself plus one final consonant, with that
word's own gloss against his Chinese:

    value 0x and unglossed, value+C attested, value+C means what he says.

Seven fires in the whole book, and all seven are the same consonant, -g:

    LUNO  地震        -> runu  0x   but runug 地震, mrunug 4x 震動
    TANGO 嫩芽        -> tangu 0x   but tangug 新芽, ptangug 使長芽, tmangug 2x 在長芽
    QOLO  圓的－球     -> quru  0x   but qurug 162x 球, mqurug 4x 圓形的
    BLIKU 耳墜——耳環  -> briku 0x   but brikug 女用耳環
    SBAAN 打盹－午睡   -> sbaan 0x   but sbaang 4x 稍作躺下休息
    TABU  餵養、飼養   -> tabu  0x   but tabug 1x 飼養         <- refused, below

QOLO is the one that was actively wrong on screen.  `quru` is not merely 0x —
it is an ATTESTED WORD MEANING 反而, and it was painted DARK at level 1, i.e.
the map asserted a verified modern spelling and named the wrong existing word,
the worst state in this file.  `mqolo` was dark too, on `mquru` at level 2.  The
reduplicated slot went the same way: modern `qquri` 2x 指示方向 is the plural of
THAT word, so `qquru` was reaching into the wrong family entirely, while his
Qqolo 圓形物、球、圓圈（複數）is exactly the shape `qqhuni` 樹（很多）/ `qqpatur`
青蛙（很多）— 76 qq- forms in the lexicon — takes on `qurug`.

SBAAN is the half-brown card at its most local, after batch 126's paradigm line:
**his own example sentence spells the word with the g.**  Under SBAAN he writes
`Nasi so kmsbaang o, usa sbaang xngali xali` 你若想小睡一下，就到稍微遠一點的
地方去睡吧, and his sub-form is Msbaang.  `sbaang` was ALREADY a map value, from
that sentence and that sub-form; the headword was the one slot still without it,
and it had been pinned to itself by hand in manual_map.  Nothing had to be
researched — the entry contradicted its own headword in its own example.

REFUSED: tabu -> tabug.  His TMABU paradigm line `°Tmabu, tabu, tbui, tbuan,
tbuon (vl. Tb'gi, tb'gan, tb'gun)` puts the bare token in the feeding paradigm,
and every other member of it is already on the -g stem (tmabug 26x, mtabug 26x,
tbgan 22x, tnbgan 23x, ptabug 使托養) — batch 126's lesson pointing straight at
it.  But `tabu` is a THREE-way homograph: a second TABU entry is 不太適合加工的
闊葉木材, a broadleaf timber, and SKA's example carries a third sense.  modernize()
takes one word with no entry context, so 4 right occurrences would be bought with
1 dark-and-wrong one.  Deferred for the third time, and the reason is unchanged.

Two values go in blind, and deliberately: `qqurug` and `pqurug` are 0x and
unlisted, so they stay PALE — reduplication and causative p- on a root the corpus
proves 162 times.  They are not claims that those words are attested; they are
claims that the STEM is qurug and not quru, which is the only thing this batch
asserts anywhere.
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

NEW = [("luno", "runug"), ("mluno", "mrunug"),
       ("tango", "tangug"), ("mtango", "mtangug"), ("tmango", "tmangug"),
       ("qolo", "qurug"), ("mqolo", "mqurug"), ("qqolo", "qqurug"),
       ("pqolo", "pqurug"), ("bliku", "brikug"), ("sbaan", "sbaang")]
# every value moved off, with what it actually was
LIES = {"runu": "0x and unglossed",
        "mrunu": "0x — beside mrunug 4x 震動",
        "tangu": "0x — beside tangug 新芽",
        "mtangu": "0x", "tmangu": "0x — beside tmangug 2x 在長芽",
        "quru": "AN ATTESTED WORD MEANING 反而, and it was painted DARK",
        "mquru": "0x, and it was painted DARK at level 2",
        "qquru": "0x — its real plural qquri 2x is 指示方向, another word",
        "pquru": "0x", "briku": "0x — beside brikug 女用耳環",
        }

print("-- the map")
for k, v in NEW:
    check(MAN.get(k) == v and MAP.get(k) == v,
          "%-8s -> %-9s (manual=%s map=%s)" % (k, v, MAN.get(k), MAP.get(k)))
check(len(MAN) == 1787, "manual_map 1777 -> 1787: %d" % len(MAN))
check(MAN.get("sbaan") == "sbaang",
      "sbaan was a hand-written IDENTITY pin and is overturned — his own "
      "example sentence spells it sbaang (%s)" % MAN.get("sbaan"))

print("\n-- nine of the eleven values are LISTED; two are blind on purpose")
for _k, v in NEW:
    if v in ("qqurug", "pqurug"):
        check(v not in A and v not in V,
              "%-8s is unlisted and stays PALE — reduplication / causative p- on "
              "a stem the corpus proves 162x, not a claim of attestation" % v)
    else:
        check(v in A and V.get(v) == 1,
              "%-8s is LISTED at level 1 (%s)" % (v, V.get(v)))

print("\n-- every value we moved off is unreferenced now")
for w, why in sorted(LIES.items()):
    ks = sorted(k for k in MAP if MAP[k] == w)
    check(not ks, "%-7s (%s): %s" % (w, why, ks or "gone"))
check("quru" not in V and "mquru" not in V,
      "the two DARK wrong claims are out of verified.js entirely: %s %s"
      % (V.get("quru"), V.get("mquru")))

print("\n-- the evidence each fix was read off, unmoved")
check(MAP.get("sbaang") == "sbaang" and V.get("sbaang") == 1,
      "sbaang was ALREADY a map value before this batch — from his own example "
      "and his Msbaang sub-form; only the headword lacked the g (%s)"
      % MAP.get("sbaang"))
check(MAP.get("msbaang") == "msbaang" and V.get("msbaang") == 1,
      "msbaang -> msbaang 4x 躺一下, listed (%s %s)"
      % (MAP.get("msbaang"), V.get("msbaang")))
for w in ("qurug", "mqurug", "runug", "mrunug", "tmangug"):
    check(w in A, "%-8s is in attested_modern.json — the -g forms are the words, "
          "not inventions" % w)

print("\n-- the refusal")
check(MAP.get("tabu") == "tabu",
      "tabu still claims itself, NOT tabug — three entries share the token "
      "(feeding, a broadleaf timber, and SKA's example) and modernize() takes "
      "one word with no entry context (%s)" % MAP.get("tabu"))
for k, v in (("tmabu", "tmabug"), ("mtabu", "mtabug"), ("tbuan", "tbgan"),
             ("ptabu", "ptabug")):
    check(MAP.get(k) == v,
          "%-7s -> %-8s — the rest of his paradigm is already on the -g stem, "
          "which is what makes the bare token a refusal and not an oversight (%s)"
          % (k, v, MAP.get(k)))

print("\n-- verified.js")
L = collections.Counter(V.values())
check(len(V) == 4715, "verified 4709 -> 4715: %d" % len(V))
check([L[i] for i in range(1, 8)] == [3906, 605, 54, 70, 38, 32, 10],
      "levels 3899/606/54/70/38/32/10 -> %s — eight new LISTED values less quru, "
      "and mquru leaves level 2 (sbaang was already a value)"
      % [L[i] for i in range(1, 8)])

URL = "http://127.0.0.1:8765/?q=%CC%81"
SPANS = """(ws) => { const r = {};
  for (const n of document.querySelectorAll('span.w-mod,span.w-unv,span.w-raw')) {
    const t = n.textContent.trim().toLowerCase();
    if (ws.indexOf(t) < 0) continue;
    const s = n.className.indexOf('w-mod') >= 0 ? 'dark'
            : n.className.indexOf('w-unv') >= 0 ? 'PALE' : 'GREEN';
    (r[t] = r[t] || {})[s] = (r[t][s] || 0) + 1;
  } return r; }"""
WATCH = ["runug", "runu", "mrunug", "mrunu", "tangug", "tangu", "mtangug",
         "tmangug", "tmangu", "qurug", "quru", "mqurug", "mquru", "qqurug",
         "qquru", "pqurug", "pquru", "brikug", "briku", "sbaang", "sbaan"]
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
check(cm == {"w-mod": 41103, "w-unv": 3330, "w-raw": 32},
      "modern 41093/3340/32 -> 41103/3330/32: %s" % cm)
check(tm == 44465 and abs(100.0 * cm["w-mod"] / tm - 92.4390) < 0.0005,
      "modern total still 44465, dark 92.4165%% -> 92.4390%%: %d %.4f"
      % (tm, 100.0 * cm["w-mod"] / tm))
check(co == {"w-mod": 41548, "w-unv": 3382, "w-raw": 32},
      "original 41538/3392/32 -> 41548/3382/32: %s" % co)
check(to == 44962, "original total still 44962: %d" % to)
check(cm["w-raw"] == 32 and co["w-raw"] == 32,
      "green still 32 in both modes — nothing fell out of the map")
check(dm == 1967 and do == 1967, "1967 cards: %d %d" % (dm, do))
check(not em and not eo, "no page errors: %d %d" % (em, eo))

print("\n-- the DOM")
EXP = {"runug": {"dark": 1}, "mrunug": {"dark": 2},
       "tangug": {"dark": 1}, "mtangug": {"dark": 2}, "tmangug": {"dark": 2},
       "qurug": {"dark": 1}, "mqurug": {"dark": 2},
       "brikug": {"dark": 1}, "sbaang": {"dark": 2},
       "qqurug": {"PALE": 1}, "pqurug": {"PALE": 1}}
for w in sorted(EXP):
    check(seen.get(w) == EXP[w], "%-8s %s (got %s)" % (w, EXP[w], seen.get(w)))
for w in ("runu", "mrunu", "tangu", "tmangu", "quru", "mquru", "qquru",
          "pquru", "briku", "sbaan"):
    check(w not in seen, "%-7s absent from the page: %s" % (w, seen.get(w)))

print("\n%s  (%d failed)" % ("PASS" if not fail else "FAILURES", len(fail)))
for m in fail:
    print("   " + m)
sys.exit(1 if fail else 0)
