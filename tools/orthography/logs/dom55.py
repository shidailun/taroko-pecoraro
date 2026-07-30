"""Batch 55 on the page.

Two assertions per key, made per CARD rather than globally, because a page-wide
string test cannot tell a fix from a coincidence -- QALO's card legitimately shows
KALU because it carries a crossRef, which is what made dom24c subtract every form
the card's own tokens render to before banning anything. Same here.

  brown  -- the card that holds his token must paint the new value;
  banned -- and must NOT paint what it used to paint, unless some OTHER token on
            the same card renders to that string for reasons of its own.

The HOLD set is the load-bearing half: every neighbour these twenty-one keys sit
beside, read out of the map before the rebuild. A batch that fixes its own targets
and drags a sibling off its root is a regression, and only the neighbours catch it.
"""
import json, io, sys, re, collections
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

H = "C:/dev/formosan/seediq/taroko-pecoraro/"

NEW = {
    "p'lu": "peelug", "snlluwan": "sneelugan", "l'pun": "lpun",
    "sqdgi": "sqdugi", "sqdgan": "sqdugan", "sqdgun": "sqdugun",
    "mpnyeqon": "empniqun", "mn'gui": "gmneeguy", "kmbibil": "kmblbil",
    "pnmaxan": "pnmaxan", "klwaxe": "krwahi", "klwaxan": "krwahan",
    "glixo": "glihug", "gmlixo": "gmlihug", "pglixo": "pglihug",
    "plxgun": "plhgun", "plx'gun": "plhgun", "pglxgun": "pglhgun",
    "pklay": "pkray", "pklayan": "pkrayan", "pklayun": "pkrayun",
}
HOLD = {
    "bbil": "blbil", "bbilan": "blbilan", "bbilun": "blbilun",
    "gimax": "gimax", "gmaxan": "gmaxan",
    "nyeqan": "niqan", "nnyeqan": "nniqan", "pnyeqan": "pniqan",
    "mnagwi": "gmneeguy", "klawax": "krawah", "klwaxon": "krwahun",
    "mk'lae": "mkray", "knklayan": "knkrayan", "k'lae": "klai",
    "l'pi": "lpi", "l'pan": "lpan", "snqdgan": "snqdugan",
    "s'lu": "seelug", "snluwan": "sneelugan",
    "smqdo": "smqdug", "ssqdo": "ssqdug",
}
# what each key used to render as, i.e. what must be gone now
WAS = {"p'lu": "pru", "snlluwan": "snrruwan", "l'pun": "rpun",
       "sqdgi": "sqdgi", "sqdgan": "sqdgan", "sqdgun": "sqdgun",
       "mpnyeqon": "mpnyequn", "mn'gui": "mngui", "kmbibil": "kmbibir",
       "klwaxe": "krwahe", "klwaxan": "klwaxan",
       "glixo": "grihu", "gmlixo": "gmrihu", "pglixo": "pgrihu",
       "plxgun": "prhgun", "plx'gun": "prhgun", "pglxgun": "pgrhgun",
       "pklay": "pkray", "pklayan": "pklayan", "pklayun": "pklayun"}

app = io.open(H + "site/app.js", encoding="utf-8").read()
PAIR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')


def table(name):
    i = app.index("var %s = {" % name)
    return dict(PAIR.findall(app[i:app.index("\n  };", i)]))


OV, CL = table("WORD_OVERRIDES"), table("CLITIC_FORMS")
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
SM = {"x": "h", "o": "u", "l": "r"}


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


def val(w):
    k = key(w)
    for tb in (OV, MAP, CL):
        if k in tb:
            return tb[k]
    return "".join(SM.get(c, c) for c in re.sub("['\u2019\u02bc\"\u0294]", "", k))


TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])


def slots(ent):
    out = [ent.get("hw"), ent.get("paradigm")]
    out += [x.get("t") for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        out += [s.get("form"), s.get("paradigm")]
        out += [x.get("t") for x in s.get("examples", [])]
    return [x for x in out if x]


# Cards are matched by POSITION, not by headword text: in modern mode the .hw
# element prints the MODERN spelling, so keying on his headword silently matches
# almost nothing -- dom19's lesson, arriving from the other side. entries.js order
# is the render order when the filter returns everything.
cards = []
for ent in E:
    toks = {key(w) for f in slots(ent) for w in TOK.findall(f) if len(key(w)) > 1}
    cards.append((ent.get("hw") or "", toks, {val(w).lower() for w in toks}))

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.context.add_init_script(
        "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
    pg.context.new_cdp_session(pg).send("Network.setCacheDisabled",
                                        {"cacheDisabled": True})
    pg.goto("http://127.0.0.1:8765/?q=%CC%81", wait_until="networkidle")
    pg.wait_for_timeout(2500)
    dom = pg.evaluate("""() => {
        const out = [];
        document.querySelectorAll('article.entry').forEach(a => {
            const hw = a.querySelector('.hw') ? a.querySelector('.hw').textContent : '';
            const w = [];
            a.querySelectorAll('.w-mod, .w-raw').forEach(
                s => w.push(s.className.indexOf('w-raw') >= 0
                            ? '~' + s.textContent.trim()
                            : s.textContent.trim()));
            out.push([hw, w]);
        });
        return out;
    }""")
    b.close()

print("%d cards rendered, %d in entries.js" % (len(dom), len(cards)))
if len(dom) != len(cards):
    print("!! positional match is unsafe -- counts differ")
    sys.exit(1)
SPANS = [set(w.lower() for w in ws) for _, ws in dom]

nb = ng = nc = fail = 0
checked = set()
for name, want in (("batch 55 targets", NEW), ("neighbours held", HOLD)):
    print("\n--- %s ---" % name)
    for k, v in sorted(want.items()):
        hits = [i for i, (_, toks, _) in enumerate(cards) if k in toks]
        if not hits:
            print("  ?     %-12s his token is in no card" % k)
            fail += 1
            continue
        for i in hits:
            hw, _, legit = cards[i]
            checked.add(i)
            spans = SPANS[i]
            nb += 1
            if v.lower() not in spans:
                print("  BROWN %-12s %-12s missing on [%s]  green there: %s" % (
                    k, v, hw, sorted(x for x in spans if x.startswith("~"))[:5]))
                fail += 1
            if "~" + v.lower() in spans:
                print("  GREEN %-12s %-12s painted GREEN on [%s]" % (k, v, hw))
                fail += 1
            bad = WAS.get(k, "").lower()
            # subtract what the card's OTHER tokens legitimately render to
            if bad and bad != v.lower() and bad not in legit:
                ng += 1
                if bad in spans or "~" + bad in spans:
                    print("  STALE %-12s [%s] still paints %s" % (k, hw, bad))
                    fail += 1
        nc += 1

print("\n%d cards touched, %d keys, %d brown assertions, %d banned-form, FAILURES %d"
      % (len(checked), nc, nb, ng, fail))
