"""Green tokens that are already modern words AS HE SPELLED THEM.

charRules rewrites x>h, o>u, l>r on every green token. Truku orthography keeps x
(dxgal, utux, briqax), so that rule is not a repair on those words -- it is damage,
and it is invisible because the token stays green either way. Same for any token
whose spelling already matches the modern lexicon.

So: for each green token, ask the corpora about the string he actually wrote, and
report what charRules turns it into. Where the two differ the reader is currently
printing a non-word over a correct one, and an identity key both fixes the render
and marks the slot verified.
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


TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])

cnt, where = collections.Counter(), {}
for ent in E:
    hw, gl = ent.get("hw"), (ent.get("zh") or ent.get("fr") or "")
    fields = [(ent.get("hw"), gl), (ent.get("paradigm"), gl)]
    for x in ent.get("examples", []):
        fields.append((x.get("t"), gl))
    for s in ent.get("subs", []):
        sg = s.get("zh") or s.get("fr") or gl
        fields += [(s.get("form"), sg), (s.get("paradigm"), sg)]
        for x in s.get("examples", []):
            fields.append((x.get("t"), sg))
    for f, g2 in fields:
        for w in TOK.findall(f or ""):
            if len(w) < 2:
                continue
            k = key(w)
            if k in OV or k in MAP or k in CL or k in LX:
                continue
            cnt[k] += 1
            where.setdefault(k, (hw, g2))

SM = {"x": "h", "o": "u", "l": "r"}


def cr(w):
    return "".join(SM.get(c, c) for c in re.sub("['\u2019\u02bc\"\u0294]", "", w))


rows = []
for k, c in cnt.items():
    if k in ALL and cr(k) != k:
        rows.append((c, SPK.get(k, 0), k, cr(k), where[k], G.get(k) or ""))
rows.sort(key=lambda r: (-r[0], -r[1]))
for c, sp, k, m, (hw, gl), g in rows:
    print("%2dx %-14s %4sx  now prints %-14s [%s] %-22s || %s"
          % (c, k, sp, m, hw, (gl or "")[:22], g[:34]))
print("\n%d green types attested exactly as written (of %d green types, %d occ)"
      % (len(rows), len(cnt), sum(cnt.values())))
