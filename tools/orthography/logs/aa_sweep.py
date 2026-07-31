"""HIS DOUBLED VOWEL WRITING AN APOSTROPHE.

mpaaso turned out to be his own mp'aso, which already ships empeasug on tier M
along with four more human-checked siblings -- p'aso>peasug, pp'aso>ppeasug,
mp'paso>emppeasug, kmp'aso>kmpeasug. He wrote the same word twice, once with the
elision mark and once with the vowel doubled instead, and only the apostrophe
spelling ever got a key.

Batch 70 hit the same thing from the other side: psaanak, pnaanak and paaanak
against his pnanak, snanak, psnanak. So this is not one token, it is a habit --
where his typescript has a mark he sometimes doubles the vowel instead, and the
two spellings land in different rows of a flat map.

So sweep it as a class rather than one at a time. For every green with a doubled
vowel, try the spellings he uses elsewhere for the same slot -- collapse the
double, replace it with an elision mark, replace it with mark+vowel -- and report
when the result is a token HE ALREADY HAS A KEY FOR. That is the strongest kind
of evidence in this dictionary: not that a modern word exists, but that his own
map already decided this very word under his other spelling of it.

Reported with the tier of the neighbour, because a hit on a human-checked key is
worth much more than a hit on a generated one.
"""
import io, sys, json, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
MM = json.load(io.open(H + "tools/orthography/modern_map.json", encoding="utf-8"))["map"]
MAP = {k: v["modern"] for k, v in MM.items()}
TIER = {k: v["tier"] for k, v in MM.items()}
HUMAN = {"M", "J", "N", "C-review", "A"}

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("['\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
his = collections.defaultdict(list)
for ent in E:
    hw = ent.get("hw") or ""
    slots = [(ent.get("hw"), ent.get("zh"), "hw")]
    slots += [(x.get("t"), x.get("zh"), "ex") for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        slots += [(s.get("form"), s.get("zh") or ent.get("zh"), "sub")]
        slots += [(x.get("t"), x.get("zh"), "ex") for x in s.get("examples", [])]
    for f, g, kind in slots:
        for w in TOK.findall(f or ""):
            his[key(w)].append((hw, kind, f, g))

DOUBLE = re.compile(r"(aa|ee|ii|oo|uu)")
greens = sorted({t for t in his if t not in MAP and len(t) > 2},
                key=lambda t: -len(his[t]))

hits = []
for t in greens:
    cands = set()
    for m in DOUBLE.finditer(t):
        i, j = m.span()
        v = t[i]
        for repl in (v, "'", "'" + v, v + "'", "e" + v, v + "e"):
            c = t[:i] + repl + t[j:]
            if c != t:
                cands.add(c)
    # also the reverse: a doubled vowel standing where he elsewhere writes nothing
    landed = [(c, MAP[c], TIER.get(c, "")) for c in cands if c in MAP and MAP[c]]
    if landed:
        landed.sort(key=lambda x: (x[2] not in HUMAN, x[0]))
        hits.append((len(his[t]), t, landed))

print("greens with a doubled vowel that his OWN map already decides: %d\n" % len(hits))
for n, t, landed in sorted(hits, reverse=True):
    hw, kind, f, g = his[t][0]
    print("%2dx %-14s [%-11s] %s" % (n, t, hw[:11], (g or "")[:54]))
    print("        his own: %s" % "   ".join("%s->%s(%s)" % L for L in landed[:4]))
    print("        slot: %s" % (f or "")[:74])
