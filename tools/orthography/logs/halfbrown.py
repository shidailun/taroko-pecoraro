"""The half-brown card, ranked -- CLAUDE.md finding (4) turned into a work list.

For every GREEN token, look at the card it sits on and find the brown sibling
whose KEY shares the longest run with it. If a card has already decided its root,
the green slot is not a research problem: it is a slot the family skipped, and
the sibling shows what the map already believes. Cards where no sibling shares
three letters are dropped -- those are the ones that need a dictionary, not a
card.

Prints:  <green key>  ->  what it paints now   |   <sibling key> -> <its value>
"""
import json, io, sys, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"

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
PROSE = set()
for name in ("FORM_PROSE", "TAG_PROSE"):
    i = app.index("var %s = {}" % name)
    j = app.index('.split(" ")', i)
    for s in re.findall(r'"([^"]*)"', app[i:j]):
        PROSE |= set(s.split())


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


def raw(w):
    return "".join(SM.get(c, c) for c in re.sub("['\u2019\u02bc\"\u0294]", "", w))


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


def run(a, b):
    """longest common substring length -- cheap, the strings are short"""
    best = 0
    for i in range(len(a)):
        for j in range(i + best + 1, len(a) + 1):
            if a[i:j] in b:
                best = j - i
            else:
                break
    return best


CNT = collections.Counter()
BEST = {}
for ent in E:
    toks = [key(w) for f in slots(ent) for w in TOK.findall(f)]
    toks = [w for w in toks if len(w) > 1 and w not in PROSE]
    green = [w for w in set(toks) if w not in OV and w not in MAP and w not in CL]
    brown = [w for w in set(toks) if w in MAP or w in OV]
    for g in green:
        CNT[g] += toks.count(g)
        for b in brown:
            n = run(g, b)
            if n >= 3 and n > BEST.get(g, (0,))[0]:
                BEST[g] = (n, b, OV.get(b) or MAP.get(b), ent.get("hw") or "")

lim = int(sys.argv[1]) if len(sys.argv) > 1 else 60
rows = [(CNT[g], BEST[g][0], g) for g in BEST]
for n, r, g in sorted(rows, reverse=True)[:lim]:
    _, sib, sv, hw = BEST[g]
    print("%2dx %-14s %-14s | %-14s -> %-16s [%s]" % (n, g, raw(g), sib, sv, hw))
print("\n%d green types have a brown sibling sharing 3+ letters (of %d)"
      % (len(BEST), len(CNT)))
