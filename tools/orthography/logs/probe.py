"""One card, everything needed to decide it.

Half-brown cards are the highest-yield pattern in this book (CLAUDE.md finding
(4)), so the first thing to print is the card's OWN tokens with their map values:
if the siblings already committed to a stem, the green slot is not a research
question. Then, and only then, the corpus -- searched by his Chinese gloss, which
is the thing that catches a lexical substitution wearing a spelling defect's
clothes, and never by shape alone.

usage:  python probe.py TOKEN [TOKEN ...]      -- by green token
        python probe.py -c HEADWORD [...]      -- by card
"""
import json, io, sys, re, pickle, collections
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

MARKS = "['\u2019\u02bc\"\u0294]"
SM = {"x": "h", "o": "u", "l": "r"}


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


def val(w):
    k = key(w)
    for tb, nm in ((OV, "OV"), (MAP, "M"), (CL, "CL")):
        if k in tb:
            return tb[k], nm
    return "".join(SM.get(c, c) for c in re.sub(MARKS, "", k)), "green"


TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])

# corpora: the membership set must be the UNION -- many attested forms carry no
# gloss at all (qrapan, ptuhan, sttuan), and a glossed-only set hides them.
O = pickle.load(open("omni.pkl", "rb"))
GLOSS = collections.defaultdict(list)
for w, g, _ in O[0]:
    if g:
        GLOSS[w.lower()].append(g)
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
CNT = SPK if isinstance(SPK, dict) else collections.Counter(SPK)
ALL = {w.lower() for w, g, _ in O[0]} | set(CNT)


def cite(w):
    n = CNT.get(w, 0)
    g = "; ".join(dict.fromkeys(GLOSS.get(w, [])))[:60]
    return "%s %s%s" % (w, ("%dx " % n) if n else "", g or ("(0x, no gloss)"
                                                           if w not in ALL else ""))


def bygloss(zh, limit=14):
    """which modern words carry his meaning -- the only test that sees a
    lexical substitution."""
    chars = [c for c in zh if "\u4e00" <= c <= "\u9fff"]
    hits = collections.Counter()
    for w, gs in GLOSS.items():
        g = " ".join(gs)
        s = sum(1 for c in set(chars) if c in g)
        if s >= 2:
            hits[w] = s * 100 + CNT.get(w, 0)
    return [cite(w) for w, _ in hits.most_common(limit)]


def slots(ent):
    out = [("hw", ent.get("hw")), ("para", ent.get("paradigm"))]
    out += [("ex", x.get("t")) for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        out += [("form", s.get("form")), ("para", s.get("paradigm"))]
        out += [("ex", x.get("t")) for x in s.get("examples", [])]
    return [(k, v) for k, v in out if v]


def card(ent):
    print("\n" + "=" * 78)
    print("%s  %s" % (ent.get("hw"), ent.get("tag") or ""))
    print("   zh: %s" % (ent.get("zh") or ""))
    print("   fr: %s" % (ent.get("fr") or "")[:110])
    if ent.get("crossRef"):
        print("   -> %s" % ent["crossRef"])
    seen = set()
    for kind, txt in slots(ent):
        marks = []
        for w in TOK.findall(txt):
            if len(key(w)) < 2:
                continue
            v, tier = val(w)
            marks.append("%s[%s%s]" % (w, v, "" if tier != "green" else " GREEN"))
        print("   %-5s %s" % (kind, " ".join(marks)))
    for s in ent.get("subs", []):
        if s.get("zh"):
            print("      · %-22s %s" % (s.get("form", "")[:22], s["zh"][:56]))
    print("   -- corpus by gloss --")
    for c in bygloss(ent.get("zh") or ""):
        print("      %s" % c)


want, bycard = sys.argv[1:], False
if want and want[0] == "-c":
    want, bycard = want[1:], True
want = [w.lower() for w in want]
for ent in E:
    if bycard:
        if (ent.get("hw") or "").lower().split()[0].strip("(),") in want:
            card(ent)
    else:
        toks = {key(w) for _, txt in slots(ent) for w in TOK.findall(txt)}
        if toks & set(want):
            card(ent)
