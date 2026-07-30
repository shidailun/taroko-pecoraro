"""The green tokens whose char-rule output IS a modern word.

charRules is a guess: x>h, o>u, l>r, marks dropped. It runs on every green token,
which is why green words can already look modern -- and why nobody has checked
them. So check them: take each token the lookup chain still leaves green, run the
rules, and ask the omnibus and the spoken corpus whether that string is a word,
with a gloss to read against his.

The inventory is taken from entries.js through the same chain respellable() uses,
NOT from green2.json -- that file is missing tokens (ptuxan, sgxway, tsaon are all
green in the map and absent from it), so anything ranked off it under-reports.

A hit here is not automatically a key. The rules can land on a real word that means
something else (his tbian/tbiyan homograph), so the gloss still has to be read. But
a hit is the cheapest evidence there is: the render does not change at all, only
its colour, from rule-guessed to verified.
"""
import json, io, sys, re, pickle, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"

SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
O = pickle.load(open("omni.pkl", "rb"))
G, ALL = {}, set()
for w, g, _ in O[0]:
    ALL.add(w.lower())
    if g:
        G.setdefault(w.lower(), g)
ALL |= set(SPK)

app = io.open(H + "site/app.js", encoding="utf-8").read()


def table(name):
    i = app.index("var %s = {" % name)
    j = app.index("\n  };", i)
    out = {}
    for m in re.finditer(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"', app[i:j]):
        out[m.group(1)] = m.group(2)
    return out


OV, CL = table("WORD_OVERRIDES"), table("CLITIC_FORMS")
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
LX = json.load(io.open(H + "tools/orthography/lexical_map.json", encoding="utf-8"))


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


def brown(k):
    return k in OV or k in MAP or k in CL


TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])

cnt = collections.Counter()
where = {}
for ent in E:
    hw = ent.get("hw")
    fields = [ent.get("hw"), ent.get("paradigm")]
    for x in ent.get("examples", []):
        fields.append(x.get("t"))
    for s in ent.get("subs", []):
        fields += [s.get("form"), s.get("paradigm")]
        for x in s.get("examples", []):
            fields.append(x.get("t"))
    gl = ent.get("zh") or ent.get("fr") or ""
    for f in fields:
        for w in TOK.findall(f or ""):
            if len(w) < 2:
                continue
            k = key(w)
            if brown(k) or k in LX:
                continue
            cnt[k] += 1
            where.setdefault(k, (hw, gl))

SM = {"x": "h", "o": "u", "l": "r"}


def cr(w):
    return "".join(SM.get(c, c) for c in re.sub("['\u2019\u02bc\"\u0294]", "", w))


MINC = int(sys.argv[1]) if len(sys.argv) > 1 else 1
GLOSSED = "glossed" in sys.argv

hits, miss = [], []
for k, c in cnt.items():
    if c < MINC:
        continue
    m = cr(k)
    if m in ALL and (m in G or not GLOSSED):
        hits.append((c, k, m, SPK.get(m, 0), where[k], G.get(m) or ""))
    else:
        miss.append((c, k))

hits.sort(key=lambda r: (-r[0], -r[3]))
for c, k, m, sp, (hw, gl), mg in hits:
    print("%2dx %-14s -> %-14s %4sx  [%s] %-24s || %s"
          % (c, k, m, sp, hw, (gl or "")[:24], mg[:36]))
print("\n%d green types (%d occ). %d land on a real word, %d do not."
      % (len(cnt), sum(cnt.values()), len(hits), len(miss)))
