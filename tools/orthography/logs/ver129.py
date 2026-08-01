# -*- coding: utf-8 -*-
"""Batch 129 — PREFIXES, ROUND TWO.  32 values, 54 occurrences, 0 de-verified.

Batch 128 added 33 prefixes and changed the base under everything that had ever
been measured against the old one, in two ways.  A prefix's own DERIVED series
could not be a candidate until the base was legal — `pnk`, `snk`, `mkn`, `pns`
only mean anything once `pk`, `sk`, `mk`, `ps` are in `PRE` — and `tm` had been
deferred rather than rejected, pending exactly the combined pricing that 128's
own log demanded.  So round two is a real sweep, not a scraping.

It is also much thinner, and that is the finding: **the vein 128 opened is now
mostly worked out.**  60+ candidates priced singly, and the best is six types.
16 adopted, 32 values / 54 occurrences, zero de-verification, dark 93.5140% ->
93.6332%.

    tmgakat     蹲下——趴成四肢著地   <- akat    via pgakat   tmg-
    kmpskgulun  想要派去的人         <- skgul   via skgulan  kmp-  desiderative
    snkmalu     ——                  <- malu 好              snk-
    mtriya      滾動的－旋轉的       <- riya    via tmriya   mt-
    ptabuy      使下坡－使下去       <- abuy    via tmabuy   pt-
    tktrul      第三次               <- trul    via mtrul    tk-
    mkmuyux     天氣轉雨——快要下雨   <- uyux    via mquyux   mkm-
    mknaxal     歷時十天、十個時段    <- axal    via maxal 十  mkn-
    snsinaw     關於酒—與酒有關的事  <- inaw    via pnsinaw  sns-
    msneanak    脫離群體的－自我孤立的 <- eanak 獨           msn-
    qnqmi       仔細地（幾乎閉上眼睛） <- qmi 閉眼           qn-

`tm` earns its place twice over.  It unblocks four items that have been on the
`paux59` lead list for weeks — `mtriya`/`ptriya` off `riya` 旋轉 through
`tmriya`, and `ptabuy`/`emptabuy` off `abuy` 下坡 through `tmabuy` — because
those roots are witnessed by a tm- form and nothing else.  And `qn-` is the
batch-28 finding arriving as morphology: modern Truku puts the degree
nominalizer INSIDE a q-initial root (`qn-` 181 types / 949 tokens), and his own
slot is written `Knq'mi (Qnq'mi)`, both spellings, in his own hand.

ELEVEN REJECTED, AND THE RE-CUT COLUMN CONVICTED MOST OF THEM.  A candidate that
gains nothing is not free — the only thing left for it to do is move an existing
analysis, and four of the eight zero-gain candidates move one for the worse:

    png   REGRESSION.  Pngsaan is a sub of PESA, glossed 請願－請求－祈求, so the
          old cut p+`ngsa` vouched by `dngsani` 願 is his own family.  png+`saan`
          去 is a different word.  Buys 1 occurrence.
    dn    moves tgmilan off `gamil` 根 — whose own sub-form he glosses
          生根的事實、地點、時間, and which this file documents as the syncope
          exemplar — onto `gilan` 地.  Gains nothing.
    psm   moves psmyahan off `miyah` 來 onto `yahan`, itself a suffixed form.
    ptn   moves tnguhi off `tunguh` 嚐 onto `guhi`.
    qm    moves knbliqan off `bliq` 幸福 onto `bliqan` 財富.
    empg  moves empgrahul off the real root `grahul` 聚集 onto `rahul`.
    dq    NOT A MORPHEME.  dqqrinut is the d- human collective on a qq-
          REDUPLICATION of `qrinut` 窮 — DAYAO's own example reads
          「Mddayao bi ka dqqlinut」窮人們確實互相幫助.  Right root, wrong cut, and
          the same error as the tt/kk/gg/ss/mm exclusion wearing a collective's
          clothes.  1 occurrence.
    gmb   buys one value by vouching `nilaq` — a MUSHROOM, 可食用的菇類 — with
          `mnilaq` 起屑 on the 起 of 令人想起海藻.  Junk agreement.
    kms, pnt, psg   gain nothing; their re-cuts are neutral.

PRICED SINGLY AND IN COMBINATION, which is the lesson 128's log wrote down after
`sq` stole `sqrasan` off `qras` 快樂 in combination while measuring clean alone.
This set is full of short prefixes (`nk`, `ns`, `tk`, `dm`, `qn`) sitting beside
longer ones they could outbid, so it mattered — and it came back clean: the
per-candidate totals sum to 32 and the combined run yields exactly 32, with no
value lost and nothing stolen.

THE FIVE RE-CUTS ARE ALL PROMOTIONS, which no earlier prefix batch managed.  Four
move off level 7 (`chained`, the weakest thing the tool can say) onto level 1:
`qnqgu` and `qnqguan` were a chained reduplication and are now `qn`+`qgu` 公雞 on
the same root; `pnsupu` was a chained step and is now `pns`+`upu` 共; `tmsasaw`
was chained through `tsasaw` and is now `tm`+`sasaw` 涼.  The fifth, `nslikaw`,
moves from vouched to regular on `likaw` 快.  Levels: vouched 59 -> 58 and chained
14 -> 11 are those five leaving, not anything being lost.

`snkmalu` is worth its own line, because this file has a note about it from a much
earlier batch: it used to decompose onto `kalu` 梳子 (comb) and was one of the four
claims the 子 STOP character was added to kill.  It has been unverifiable ever
since — the honest state, but a dead end.  With `snk` legal it verifies at level 1
off `malu` 好, which is his word.
"""
import collections, io, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

H = r"C:\dev\formosan\seediq\taroko-pecoraro"
D = os.path.join(H, "tools", "orthography")
sys.path.insert(0, D)
import inflection
from inflection import Inflection

fail = []


def check(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        fail.append(msg)


def read(p):
    return io.open(p, encoding="utf-8").read()


V = dict((m.group(1), int(m.group(2))) for m in re.finditer(
    r'^  "(.*)": (\d),$', read(os.path.join(H, "site", "verified.js")), re.M))
A = set(json.load(io.open(os.path.join(D, "attested_modern.json"),
                          encoding="utf-8")))
t = read(os.path.join(H, "site", "modern_map.js"))
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
INF = Inflection(A, MAP)

ADDED = ["tm", "tmg", "tk", "kmp", "mkm", "mkn", "msn", "nk", "ns",
         "pnk", "pns", "psk", "snk", "sns", "dm", "qn"]

print("-- PRE, round two")
for p in ADDED:
    check(p in inflection.PRE, "%-4s is in PRE" % p)
check(len(inflection.PRE) == 69, "PRE 53 -> 69 entries: %d" % len(inflection.PRE))
check("tm" in inflection.PRE,
      "tm was DEFERRED by 128, not rejected — priced in combination now, and it "
      "unblocks riya 旋轉 and abuy 下坡, whose only witnesses are tm- forms")
REJECT = [("png", "moves pngsaan off his PESA 請願－請求 family onto saan 去"),
          ("dn", "moves tgmilan off gamil 根 onto gilan 地, for no gain"),
          ("psm", "moves psmyahan off miyah 來 onto the suffixed yahan"),
          ("ptn", "moves tnguhi off tunguh 嚐 onto guhi"),
          ("qm", "moves knbliqan off bliq 幸福 onto bliqan 財富"),
          ("empg", "moves empgrahul off the real root grahul 聚集 onto rahul"),
          ("dq", "dqqrinut is d- collective on a qq- REDUPLICATION of qrinut, "
                 "not a dq- prefix — the tt/kk exclusion in other clothes"),
          ("gmb", "its one value vouches the mushroom nilaq with mnilaq 起屑 on "
                  "the 起 of 令人想起海藻"),
          ("kms", "zero gain"), ("pnt", "zero gain"), ("psg", "zero gain")]
for p, why in REJECT:
    check(p not in inflection.PRE, "%-5s REFUSED — %s" % (p, why))
check("sq" not in inflection.PRE, "sq is still out (128's refusal)")
for p in ("tt", "kk", "gg", "ss", "mm"):
    check(p not in inflection.PRE, "%-3s still out — a reduplication is not a prefix" % p)

print("\n-- the 16 classes, each verified off its own root")
NEW = [("tmgakat", "akat", "tmg", 4), ("kmpskgulun", "skgul", "kmp", 4),
       ("snkmalu", "malu", "snk", 2), ("mtriya", "riya", "mt", 4),
       ("ptriya", "riya", "pt", 4), ("ptabuy", "abuy", "pt", 4),
       ("emptabuy", "abuy", "empt", 4), ("tktrul", "trul", "tk", 4),
       ("mkmuyux", "uyux", "mkm", 4), ("mknaxal", "axal", "mkn", 4),
       ("snsinaw", "inaw", "sns", 4), ("pskngalan", "ngal", "psk", 4),
       ("pskngali", "ngal", "psk", 4), ("msneanak", "eanak", "msn", 2),
       ("msnrima", "rima", "msn", 2), ("kmpuqun", "uqun", "kmp", 2),
       ("kmpama", "ama", "kmp", 2), ("kmpgrig", "grig", "kmp", 2),
       ("kmpniqan", "niqa", "kmp", 2), ("kmptgxalun", "tgxala", "kmp", 2),
       ("mkmpspruq", "pspruq", "mkm", 2), ("mkmdhuq", "dhuq", "mkm", 2),
       ("tksuraw", "suraw", "tk", 2), ("nktru", "tru", "nk", 2),
       ("nkyayung", "yayung", "nk", 2), ("nksasaw", "sasaw", "nk", 2),
       ("nslubuy", "lubuy", "ns", 2), ("pnsbabaw", "babaw", "pns", 2),
       ("pnkmalu", "malu", "pnk", 2), ("pnkusa", "usa", "pnk", 2),
       ("qnqmi", "qmi", "qn", 2)]
for w, root, pre, lv in NEW:
    r = INF.regular(w) if lv == 2 else INF.vouched_root(w)
    check(V.get(w) == lv and r and r[0] == root and r[1] == pre,
          "%-11s v%-4s = %-4s + %-7s %s" % (w, V.get(w), pre, root, r))
check(V.get("dmpsramal") == 7 and INF.chained("dmpsramal"),
      "dmpsramal 先驅者－先知們 v7 on psramal 準備 — dm- reaches it only through "
      "the chained level, which is the weakest thing the tool says: %s"
      % (INF.chained("dmpsramal"),))
check(len(NEW) + 1 == 32,
      "32 values in all, 54 occurrences — a twentieth of what 128 moved, which "
      "is what a worked-out vein looks like")
r = INF.regular("qnqmi")
check(r and r[0] == "qmi",
      "qn- is batch 28's infix arriving as morphology: his slot is written "
      "Knq'mi (Qnq'mi) in his own hand, and modern qn- is 181 types / 949 "
      "tokens: %s" % (r,))
r = INF.regular("snkmalu")
check(r and r[0] == "malu",
      "snkmalu used to decompose onto kalu 梳子 and was one of the four claims "
      "the 子 STOP character was added to kill; it has been unverifiable ever "
      "since, and snk- lands it on his own malu 好: %s" % (r,))

print("\n-- the re-cuts, and every one of them is a PROMOTION")
RECUT = [("qnqgu", "qgu", "qn"), ("qnqguan", "qgu", "qn"),
         ("pnsupu", "upu", "pns"), ("tmsasaw", "sasaw", "tm"),
         ("nslikaw", "likaw", "ns")]
for w, root, pre in RECUT:
    r = INF.regular(w)
    check(V.get(w) == 2 and r and r[0] == root and r[1] == pre,
          "%-9s v2 = %-4s + %-7s %s" % (w, pre, root, r))
check(all(V.get(w) == 2 for w, _r, _p in RECUT),
      "four move off level 7 (chained) and one off level 3 (vouched) onto level "
      "1 — the vouched and chained counts fall because of THESE, not because "
      "anything was lost")

print("\n-- the eleven refusals, checked where they would have shown")
KEEP = [("pngsaan", 4, "ngsa", "his PESA family, vouched by dngsani 願 — png "
                                "would have put it on saan 去"),
        ("tgmilan", 6, "gamil", "the syncope exemplar this file documents — dn "
                                "would have put it on gilan 地"),
        ("psmyahan", 6, "miyah", "psm would have put it on the suffixed yahan"),
        ("tnguhi", 6, "tunguh", "ptn would have put it on guhi"),
        ("knbliqan", 4, "bliq", "qm would have put it on bliqan 財富"),
        ("empgrahul", 4, "grahul", "empg would have put it on rahul"),
        ("sqrasan", 4, "qras", "128's refusal, still standing")]
for w, lv, root, why in KEEP:
    r = (INF.vouched_root(w) if lv == 4 else
         INF.syncopated(w) if lv == 6 else None)
    check(V.get(w) == lv and r and r[0] == root,
          "%-10s v%d still on %-7s — %s" % (w, lv, root, why))
for w, why in (("nilaq", "the mushroom stays unverified rather than take "
                         "mnilaq 起屑 on a 起 borrowed from 令人想起海藻"),
               ("dqqrinut", "d- collective on a qq- reduplication; the right "
                            "root by the wrong cut is not a verification")):
    check(not V.get(w), "%-9s UNVERIFIED — %s" % (w, why))

print("\n-- verified.js")
L = collections.Counter(V.values())
check(len(V) == 5002, "verified 4970 -> 5002: %d" % len(V))
check([L[i] for i in range(1, 8)] == [3906, 822, 58, 132, 35, 38, 11],
      "levels 3906/798/59/120/35/38/14 -> %s — regular +24 (19 new plus the "
      "five promotions), vouched_root +12, and vouched/chained fall only by the "
      "promotions" % [L[i] for i in range(1, 8)])
check(L[1] == 3906,
      "LISTED unchanged at 3906 — a prefix batch adds no attested word, only "
      "analyses of words already on screen")
check(L[3] == 58 and L[7] == 11,
      "vouched 59 -> 58 and chained 14 -> 11: nslikaw promoted out of one, "
      "qnqgu/qnqguan/pnsupu/tmsasaw out of the other against dmpsramal coming "
      "in, so 14 - 4 + 1 = 11")

URL = "http://127.0.0.1:8765/?q=%CC%81"
SPANS = """(ws) => { const r = {};
  for (const n of document.querySelectorAll('span.w-mod,span.w-unv,span.w-raw')) {
    const t = n.textContent.trim().toLowerCase();
    if (ws.indexOf(t) < 0) continue;
    const s = n.className.indexOf('w-mod') >= 0 ? 'dark'
            : n.className.indexOf('w-unv') >= 0 ? 'PALE' : 'GREEN';
    (r[t] = r[t] || {})[s] = (r[t][s] || 0) + 1;
  } return r; }"""
WATCH = [w for w, _r, _p, _l in NEW] + [w for w, _r, _p in RECUT] + \
        ["dmpsramal", "nilaq", "dqqrinut"] + [w for w, _l, _r, _y in KEEP] + \
        ["tdalih", "skina", "mkrbagan", "qurug", "quru", "sbaang", "sbaan"]
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
check(cm == {"w-mod": 41634, "w-unv": 2799, "w-raw": 32},
      "modern 41581/2852/32 -> 41634/2799/32: %s" % cm)
check(tm == 44465 and abs(100.0 * cm["w-mod"] / tm - 93.6332) < 0.0005,
      "modern total still 44465, dark 93.5140%% -> 93.6332%%: %d %.4f"
      % (tm, 100.0 * cm["w-mod"] / tm))
check(co == {"w-mod": 42088, "w-unv": 2842, "w-raw": 32},
      "original 42033/2897/32 -> 42088/2842/32: %s" % co)
check(to == 44962, "original total still 44962: %d" % to)
check(cm["w-raw"] == 32 and co["w-raw"] == 32,
      "green still 32 in both modes — a verification batch moves pale to dark "
      "and must never touch the map")
check(dm == 1967 and do == 1967, "1967 cards: %d %d" % (dm, do))
check(not em and not eo, "no page errors: %d %d" % (em, eo))

print("\n-- the DOM")
for w, _r, _p, _l in NEW:
    g = seen.get(w) or {}
    check(g.get("dark") and not g.get("PALE") and not g.get("GREEN"),
          "%-11s renders DARK on the page: %s" % (w, g or "ABSENT"))
for w, _r, _p in RECUT:
    g = seen.get(w) or {}
    check(g.get("dark") and not g.get("PALE"),
          "%-9s was already dark and stays dark — a promotion moves the "
          "evidence, not the paint: %s" % (w, g or "ABSENT"))
check((seen.get("dmpsramal") or {}).get("dark"),
      "dmpsramal dark: %s" % seen.get("dmpsramal"))
for w, _l, _r, _y in KEEP:
    check((seen.get(w) or {}).get("dark"),
          "%-10s dark — a refusal costs no paint, it only keeps the evidence on "
          "the right root: %s" % (w, seen.get(w)))
for w in ("nilaq", "dqqrinut"):
    g = seen.get(w) or {}
    check(not g.get("dark"),
          "%-9s is NOT dark — the refusal is visible on the page: %s"
          % (w, g or "ABSENT"))
for w in ("tdalih", "skina", "mkrbagan"):
    check((seen.get(w) or {}).get("dark"),
          "%-9s (batch 128) still dark: %s" % (w, seen.get(w)))
for w in ("qurug", "sbaang"):
    check((seen.get(w) or {}).get("dark"),
          "%-8s (batch 127) still dark: %s" % (w, seen.get(w)))
for w in ("quru", "sbaan"):
    check(w not in seen, "%-6s still absent from the page: %s" % (w, seen.get(w)))

print("\n%s  (%d failed)" % ("PASS" if not fail else "FAILURES", len(fail)))
for m in fail:
    print("   " + m)
sys.exit(1 if fail else 0)
