# -*- coding: utf-8 -*-
"""Batch 128 — THE MISSING PREFIXES.  257 values, 489 occurrences, 0 de-verified.

Every level from 1 to 7 in `build_verified.py` reaches a root by stripping one of
the strings in `inflection.py`'s `PRE`.  So a prefix that is not in that list makes
its whole morphological class unverifiable **at any level, however good the
evidence** — the gloss can agree perfectly and nothing will ever ask.  `PRE` was
the m-/p-/s-/n- series and nothing else: no k-, no t-, no d-, no g-, and no
`ma`/`maa`.  Whole classes of exactly the morphology the brief names ("obvious
morphological things like AF PF LF and s- and causative p- and preterite -n-, even
if that form of the word is not in the dictionary") were unreachable:

    tdalih      非常近的          <- dalih  近         t-   intensifier
    tnkuyuh     女人的所有者       <- nkuyuh 女人的      t-   on his own n- form
    kmbuway     想要給            <- buway  給         km-  desiderative
    dmkdaya     住在高處的那些人   <- mkdaya            d-   human collective
    knqrinutan  貧窮              <- qrinut 窮         kn- -an degree
    mabubu      即將成為母親       <- bubu   母親       ma-  prospective
    mkrbagan    夏季期間          <- rbagan 夏天       mk-  locative
    tngamil     已生根            <- gamil  根         tn-  preterite
    skina       已故的媳婦         <- ina    媳婦       sk-  'the late'

`skina` is worth its own line: sk- 'the late' verified at level 1 off `ina` 媳婦 is
the corpus agreeing with his own reading of the morpheme, and with the remark that
skBoxil is the deceased Boxil.  The d- collective comes in as a whole series —
`dtruku`, `dpais` 敵人（泛指）, `druru` 鴨, `drudux` 雞, `dquyu` 蛇, `dnihung` 日本,
`dphpah`, `dqrinut`, `dbsukan`, `djyamu`.

33 prefixes added: 257 values / 489 occurrences newly verified, **zero
de-verified**, dark 92.4390% -> 93.5140%.  That is 20x a normal batch, and it is
not new evidence — it is evidence the tool was never allowed to look at.

THREE THINGS THIS LIST MUST NOT GROW INTO, each measured rather than assumed.

**`sq` was priced and rejected.**  Singly it was clean; in combination it steals
`sqrasan` off `qras` 快樂 and onto `rasa` on a shared 間, and it yields one value.
`regular()` takes the analysis with the LEAST affixation (`cost = len(p) + len(sf)`),
so a newly-legal SHORT prefix can outbid a longer CORRECT one.  Price a candidate
both singly and in combination or this class of regression is invisible.

**The CV- reduplications `tt kk gg ss mm` are deliberately absent.**  They already
reach level 7, whose gate is the strict slot-gloss one; putting them in `PRE` would
hand them `regular()`'s single-shared-character gate instead.  A reduplication is
not a prefix.

**`tm` is deferred, not rejected.**  3 types / 5 occurrences singly, a genuine AF
prefix already partly covered by the `-m-` infix logic in `roots()`.  It was not in
the combined set and is not in `PRE`; price it in combination before adding it.

THE RE-CUT LIST IS WHERE A PREFIX BATCH PROVES ITSELF.  37 values keep their paint
and change their evidence, and 36 of the 37 are improvements — `mkmisan` had been
resting on `kisa`+m+an agreeing on 真, which is junk, and now cuts `mk`+`misan`
冬天; `tdha` moves to `t`+`dha` 兩, `msskuxul` to `ms`+`skuxul`, `pkkhnuk` to
`pk`+`khnuk` 軟, `pthungul` to `pt`+`hungul` 鋒.  `pklabu` lands on `labu` 包東西,
which also retires the old `klabu` 蜂名 mis-analysis.  Three sistered claims
(`tcingi`, `tbyaxi`, `glaan`) are promoted to vouched_root, which is why sistered
falls 38 -> 35.

ALL 257 WERE READ.  Five blemishes, ~2%, and **not one is a wrong claim on screen**
— the display is binary on verification, so the value painted is right in every
case and only the internal root record is weak:

    knuwaan [5] / knuwa [2]  cut k+nuwa+an on the NAME `nuwa` 人名（女）rather than
                             kn+uwa+an on `uwa` 少女 — bare `k` costs 3 against
                             `kn`'s 4 and outbids it.  Bare `k` is worth 28 types /
                             53 occurrences, so it stays.
    mspitay [3]              agrees on 發 alone (root `pit` 鳥叫聲 vs his 發臭的)
    lwaqi   [5]              vouched via `tglwaqan` 充滿閃亮 against his 驅趕
    tbuur   [1]              on `buur` 皮（煮熟地瓜或芋頭的皮）vs his 黃瓜, agreeing
                             on 瓜 out of 地瓜
    msrudan [5]              on `rudu` 心亂 rather than `rudan` 老人

A weak root record is a blemish in the audit trail, not a wrong word on the page,
and it is weighed against the prefix's whole yield — none of these is worth losing
`k`, `ms` or `t` over.
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


PAIR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')


def read(p):
    return io.open(p, encoding="utf-8").read()


def table(app, name):
    i = app.index("var %s = {" % name)
    return dict(PAIR.findall(app[i:app.index("\n  };", i)]))


V = dict((m.group(1), int(m.group(2))) for m in re.finditer(
    r'^  "(.*)": (\d),$', read(os.path.join(H, "site", "verified.js")), re.M))
A = set(json.load(io.open(os.path.join(D, "attested_modern.json"),
                          encoding="utf-8")))
app = read(os.path.join(H, "site", "app.js"))
t = read(os.path.join(H, "site", "modern_map.js"))
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
INF = Inflection(A, MAP)

# the 33 adopted, with the class each one carries
ADDED = ["ma", "maa", "t", "tn", "tg", "k", "kn", "km", "kmn", "g", "gm", "gn",
         "d", "mk", "mt", "ms", "mg", "pk", "pt", "pg", "sm", "sk", "skn", "sg",
         "mq", "kns", "tmn", "gmn", "mtg", "mpt", "empt", "empk", "emps"]

print("-- PRE, the chokepoint every level runs through")
for p in ADDED:
    check(p in inflection.PRE, "%-5s is in PRE" % p)
check(len(inflection.PRE) == 53, "PRE 20 -> 53 entries: %d" % len(inflection.PRE))
check("sq" not in inflection.PRE,
      "sq is REFUSED — it yields one value and steals sqrasan off qras 快樂 onto "
      "rasa on a shared 間, because regular() takes the least affixation")
for p in ("tt", "kk", "gg", "ss", "mm"):
    check(p not in inflection.PRE,
          "%-3s stays OUT — a reduplication is not a prefix; it already reaches "
          "level 7, whose gloss gate is the strict slot-gloss one" % p)
check("tm" not in inflection.PRE,
      "tm is deferred, not adopted — 3 types singly, and it was never priced in "
      "combination")

print("\n-- the prefix classes, each verified off its own root")
NEW = [("tdalih", "dalih", "t"), ("tnkuyuh", "nkuyuh", "t"),
       ("kmbuway", "buway", "km"), ("dmkdaya", "mkdaya", "d"),
       ("knqrinutan", "qrinut", "kn"), ("mabubu", "bubu", "ma"),
       ("skina", "ina", "sk"), ("tngamil", "gamil", "tn"),
       ("mkrbagan", "rbagan", "mk"), ("dtruku", "truku", "d"),
       ("drudux", "rudux", "d"), ("dpais", "pais", "d")]
for w, root, pre in NEW:
    r = INF.regular(w)
    check(V.get(w) == 2 and r and r[0] == root and r[1] == pre,
          "%-11s v%s = %-3s + %-7s %s" % (w, V.get(w), pre, root, r))
check(V.get("skina") == 2 and INF.regular("skina")[0] == "ina",
      "sk- is 'the late': skina 已故的媳婦 off ina 媳婦, which is the corpus "
      "agreeing with his own reading of the morpheme (skBoxil = the late Boxil)")

print("\n-- the re-cuts: same paint, better evidence")
RECUT = [("mkmisan", "misan", "mk"), ("tdha", "dha", "t"),
         ("msskuxul", "skuxul", "ms"), ("pkkhnuk", "khnuk", "pk"),
         ("pthungul", "hungul", "pt"), ("pklabu", "labu", "pk")]
for w, root, pre in RECUT:
    r = INF.regular(w)
    check(r and r[0] == root and r[1] == pre,
          "%-9s now %-3s + %-7s %s" % (w, pre, root, r))
check(INF.regular("mkmisan")[0] == "misan",
      "mkmisan had been resting on kisa+m+an agreeing on 真 — a change that does "
      "not move the paint can still fix the evidence")

print("\n-- the refusal, checked where it would have shown")
r = INF.vouched_root("sqrasan")
check(V.get("sqrasan") == 4 and r and r[0] == "qras",
      "sqrasan still rests on qras 快樂 at level 4, NOT on rasa: %s" % (r,))

print("\n-- the five blemishes, recorded rather than hidden")
BLEM = [("knuwaan", "nuwa", "the NAME 人名（女）, not uwa 少女 — bare k costs 3 "
                            "against kn's 4 and outbids the right analysis"),
        ("knuwa", "nuwa", "same cut as knuwaan"),
        ("mspitay", "pit", "agrees on 發 alone (鳥叫聲 vs his 發臭的)"),
        ("tbuur", "buur", "皮（煮熟地瓜或芋頭的皮）vs his 黃瓜, on 瓜 out of 地瓜"),
        ("msrudan", "rudu", "心亂 rather than rudan 老人")]
for w, root, why in BLEM:
    r = INF.regular(w)
    check(V.get(w) and r and r[0] == root,
          "%-8s v%s on %-6s — %s" % (w, V.get(w), root, why))
r = INF.vouched("lwaqi")
check(V.get("lwaqi") == 3 and r and r[0] == "tglwaqan",
      "lwaqi v3 vouched via tglwaqan 充滿閃亮 against his 驅趕: %s" % (r,))
check(len(BLEM) + 1 == 6 and all(V.get(w) for w, _r, _y in BLEM),
      "six weak root records over 257 values — every one of them is a value whose "
      "PAINT is right, because the display is binary on verification; the blemish "
      "is in the audit trail, not on screen")

print("\n-- verified.js")
L = collections.Counter(V.values())
check(len(V) == 4970, "verified 4715 -> 4970: %d" % len(V))
check([L[i] for i in range(1, 8)] == [3906, 798, 59, 120, 35, 38, 14],
      "levels 3906/605/54/70/38/32/10 -> %s — regular +193, vouched_root +50, and "
      "sistered FALLS 38 -> 35 because tcingi/tbyaxi/glaan are promoted"
      % [L[i] for i in range(1, 8)])
check(L[1] == 3906,
      "LISTED is unchanged at 3906 — this batch adds no attested word, only "
      "analyses of words already on screen")

URL = "http://127.0.0.1:8765/?q=%CC%81"
SPANS = """(ws) => { const r = {};
  for (const n of document.querySelectorAll('span.w-mod,span.w-unv,span.w-raw')) {
    const t = n.textContent.trim().toLowerCase();
    if (ws.indexOf(t) < 0) continue;
    const s = n.className.indexOf('w-mod') >= 0 ? 'dark'
            : n.className.indexOf('w-unv') >= 0 ? 'PALE' : 'GREEN';
    (r[t] = r[t] || {})[s] = (r[t][s] || 0) + 1;
  } return r; }"""
WATCH = [w for w, _r, _p in NEW] + [w for w, _r, _p in RECUT] + \
        ["sqrasan", "qurug", "quru", "mqurug", "runug", "sbaang", "sbaan"]
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
check(cm == {"w-mod": 41581, "w-unv": 2852, "w-raw": 32},
      "modern 41103/3330/32 -> 41581/2852/32: %s" % cm)
check(tm == 44465 and abs(100.0 * cm["w-mod"] / tm - 93.5140) < 0.0005,
      "modern total still 44465, dark 92.4390%% -> 93.5140%% — a full point in one "
      "batch, and 478 pale occurrences gone: %d %.4f"
      % (tm, 100.0 * cm["w-mod"] / tm))
check(co == {"w-mod": 42033, "w-unv": 2897, "w-raw": 32},
      "original 41548/3382/32 -> 42033/2897/32: %s" % co)
check(to == 44962, "original total still 44962: %d" % to)
check(cm["w-raw"] == 32 and co["w-raw"] == 32,
      "green still 32 in both modes — a verification batch moves pale to dark and "
      "must never touch the map")
check(dm == 1967 and do == 1967, "1967 cards: %d %d" % (dm, do))
check(not em and not eo, "no page errors: %d %d" % (em, eo))

print("\n-- the DOM")
for w, _r, _p in NEW + RECUT:
    g = seen.get(w) or {}
    check(g.get("dark") and not g.get("PALE") and not g.get("GREEN"),
          "%-11s renders DARK on the page: %s" % (w, g or "ABSENT"))
check((seen.get("sqrasan") or {}).get("dark"),
      "sqrasan is dark too — the refusal costs no paint, it only keeps the "
      "evidence on the right root: %s" % seen.get("sqrasan"))
for w in ("qurug", "mqurug", "runug", "sbaang"):
    check((seen.get(w) or {}).get("dark"),
          "%-8s (batch 127) still dark: %s" % (w, seen.get(w)))
for w in ("quru", "sbaan"):
    check(w not in seen, "%-6s still absent from the page: %s" % (w, seen.get(w)))

print("\n%s  (%d failed)" % ("PASS" if not fail else "FAILURES", len(fail)))
for m in fail:
    print("   " + m)
sys.exit(1 if fail else 0)
