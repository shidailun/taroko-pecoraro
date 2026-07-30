"""Batch 56 on the page.

Same two assertions as dom55, made per CARD, and cards matched by POSITION -- in
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
import json, io, sys, re, subprocess
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

H = "C:/dev/formosan/seediq/taroko-pecoraro/"
NEW = {
    "ptgimax": "ptgimax",
    "x'lyex": "lhlih", "xm'lyex": "lmhlih", "mx'lyex": "mlhlih",
    "xlyexan": "lhlihan", "xlyexon": "lhlihun",
    "pspdagun": "pspdagun", "pnspdagan": "pnspdagan",
    "saisai": "seysay", "stabu": "stabug", "tnabu": "tnabug",
    "nyao": "ngiyaw", "niyao": "ngiyaw",
    "ddyali": "dgyali", "ddyalan": "dgyalan", "ddyalun": "dgyalun",
    "plnglngun": "plnglungun",
}

app = io.open(H + "site/app.js", encoding="utf-8").read()
PAIR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')


def table(name):
    i = app.index("var %s = {" % name)
    return dict(PAIR.findall(app[i:app.index("\n  };", i)]))


def parse_map(t):
    a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
    return json.loads(t[a:t.index("\n};", a) + 2])


OV, CL = table("WORD_OVERRIDES"), table("CLITIC_FORMS")
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


cards = []
for ent in E:
    toks = {key(w) for f in slots(ent) for w in TOK.findall(f) if len(key(w)) > 1}
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

nb = ng = fail = 0
checked = set()
for name, want in (("batch 56 targets", TARGETS), ("neighbours held", HOLD)):
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
