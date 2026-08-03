"""Batch 57 on the page.

Same two assertions as dom56, made per CARD, and cards matched by POSITION -- in
modern mode the .hw element prints the MODERN headword, so keying on his spelling
matches almost nothing.

  brown  -- the card holding his token must paint the new value;
  banned -- and must NOT paint what it painted before, unless some OTHER token on
            the same card renders to that string for reasons of its own.

The difference from dom55 is that HOLD is no longer hand-written. The batch is
read out of `git show HEAD:site/modern_map.js` versus the working copy, so the
neighbour set is EVERY other token on every touched card, carrying the value it
had before the rebuild -- which is what a regression would have to move. Hand-
listing neighbours is how you miss the one you did not think to list.
"""
import json, io, sys, re, subprocess, os
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

H = "C:/dev/formosan/seediq/taroko-pecoraro/"
# read from the batch file itself -- never a second copy (see fixnew.py)
_b = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "b71.py"), encoding="utf-8").read()
_ns = {}
exec(_b[_b.index("FIX = {"):_b.index("\n}\n", _b.index("FIX = {")) + 3], _ns)
NEW = _ns["FIX"]

app = io.open(H + "site/app.js", encoding="utf-8").read()
PAIR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')


def table(name):
    i = app.index("var %s = {" % name)
    return dict(PAIR.findall(app[i:app.index("\n  };", i)]))


def parse_map(t):
    a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
    return json.loads(t[a:t.index("\n};", a) + 2])


OV, CL = table("WORD_OVERRIDES"), table("CLITIC_FORMS")
CJ = table("CLITIC_JOIN")            # "a sao" -> "asaw": the pair is ONE token
# his French apparatus and his abbreviations: FORM_PROSE/TAG_PROSE run before
# respellable(), so these are greyed and can never carry a w-mod span.
PROSE = set()
for _n in ("FORM_PROSE", "TAG_PROSE"):
    _i = app.index("var %s = {}" % _n)
    for _s in re.findall(r'"([^"]*)"', app[_i:app.index('.split(" ")', _i)]):
        PROSE |= set(_s.split())
MAP = parse_map(io.open(H + "site/modern_map.js", encoding="utf-8").read())
OLD = parse_map(subprocess.run(["git", "show", "HEAD:site/modern_map.js"],
                               cwd=H, capture_output=True).stdout.decode("utf-8"))
SM = {"x": "h", "o": "u", "l": "r"}


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


def val(w, m):
    k = key(w)
    for tb in (OV, m, CL):
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


cards, SWAL = [], []
for ent in E:
    fields = slots(ent)
    toks = {key(w) for f in fields for w in TOK.findall(f) if len(key(w)) > 1}
    # a token joinClitics eats is not a span of its own on THIS card
    eaten = set()
    for f in fields:
        ws = [key(w) for w in TOK.findall(f)]
        for a, b in zip(ws, ws[1:]):
            if a + " " + b in CJ:
                eaten.add(b)
    SWAL.append(eaten)
    cards.append((ent.get("hw") or "", toks,
                  {val(w, MAP).lower() for w in toks}))

# every sibling of a target, carrying the value it had BEFORE the rebuild
HOLD = []
for i, (_, toks, _) in enumerate(cards):
    if toks & set(NEW):
        for t in sorted(toks):
            # only tokens a curated table already knows: an unmapped token may be
            # French, or one of his abbreviations, and those are intercepted as
            # prose before respellable() ever sees them -- no w-mod span to test.
            # And the pair is (card, token), not the token alone: `mo` and `sao`
            # live on hundreds of cards, and holding them globally would test the
            # whole dictionary instead of the fifteen cards this batch moves.
            # ...and a token the page can actually paint. PARO's `page` is French
            # in FORM_PROSE, greyed before respellable() sees it; LOQ's `sao` is
            # swallowed by CLITIC_JOIN as part of `a sao` (app.js:228 says so),
            # so no bare `saw` span ever exists to hold.
            if t in PROSE or t in SWAL[i]:
                continue
            if t not in NEW and (t in OLD or t in OV):
                HOLD.append((i, t, val(t, OLD)))
TARGETS = [(i, k, NEW[k]) for i, (_, toks, _) in enumerate(cards)
           for k in sorted(toks & set(NEW))]
WAS = {k: val(k, OLD) for k in NEW}
print("%d targets in %d card-slots, %d neighbours held across %d cards"
      % (len(NEW), len(TARGETS), len(HOLD),
         sum(1 for _, t, _ in cards if t & set(NEW))))
missing = set(NEW) - {k for _, k, _ in TARGETS}
if missing:
    print("!! these keys are in no card: %s" % sorted(missing))

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
            // `.w-unv` is in this list although no log numbered below 74
            // knew the class: pale did not exist when these were written, so a
            // word that has since been de-verified vanished from the census
            // entirely and reported BROWN missing. It is still SPELLED the way
            // this file asserts, which is the only thing this file tests. The
            // GREEN check below is unaffected -- only `.w-raw` gets the `~`.
            a.querySelectorAll('.w-mod, .w-unv, .w-raw').forEach(
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

nb = ng = fail = 0
checked = set()
for name, want in (("batch 71 targets", TARGETS), ("neighbours held", HOLD)):
    print("\n--- %s (%d card-slots) ---" % (name, len(want)))
    for i, k, v in want:
        hw, toks, legit = cards[i]
        checked.add(i)
        spans = SPANS[i]
        nb += 1
        if v.lower() not in spans:
            print("  BROWN %-12s %-12s missing on [%s]  green there: %s" % (
                k, v, hw, sorted(x for x in spans if x.startswith("~"))[:5]))
            fail += 1
        # "is it green?" is only answerable when this token is the ONLY one on the
        # card that renders to that string. GIMAX carries both `mo` (brown, mu) and
        # `"mu` (green, MU), and the DOM gives text, not provenance.
        twin = any(t != k and val(t, MAP).lower() == v.lower() for t in toks)
        if "~" + v.lower() in spans and not twin:
            print("  GREEN %-12s %-12s painted GREEN on [%s]" % (k, v, hw))
            fail += 1
        bad = WAS.get(k, "").lower()
        if bad and bad != v.lower() and bad not in legit:
            ng += 1
            if bad in spans or "~" + bad in spans:
                print("  STALE %-12s [%s] still paints %s" % (k, hw, bad))
                fail += 1
nc = len(NEW) + len({k for _, k, _ in HOLD})

print("\n%d cards touched, %d keys, %d brown assertions, %d banned-form, FAILURES %d"
      % (len(checked), nc, nb, ng, fail))
