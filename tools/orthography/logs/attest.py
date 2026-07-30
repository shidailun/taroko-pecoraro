"""Every remaining green token whose rule-consistent modern shape is ATTESTED.

look.py answers this one token at a time ("candidates attested"). This runs the
same question over all 300 green types at once, which is the sweep the one-at-a-time
loop keeps approximating: generate the shapes his orthography licenses, and keep the
ones a corpus actually holds. Attestation is not adjudication -- a real word is not
yet the right word -- so it prints the gloss beside each hit for the read-through.
"""
import json, io, sys, re, collections, pickle, itertools
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
app = io.open(H + "site/app.js", encoding="utf-8").read()
PAIR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')


def table(n):
    i = app.index("var %s = {" % n)
    return dict(PAIR.findall(app[i:app.index("\n  };", i)]))


OV, CL = table("WORD_OVERRIDES"), table("CLITIC_FORMS")
PROSE = set()
for n in ("FORM_PROSE", "TAG_PROSE"):
    i = app.index("var %s = {}" % n)
    for s in re.findall(r'"([^"]*)"', app[i:app.index('.split(" ")', i)]):
        PROSE |= set(s.split())
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])

ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
OMNI = {}
for w, g, _ in ROWS:
    if w:
        OMNI.setdefault(w.lower(), g)

TOK = re.compile("[A-Za-z\u00c0-\u00ff\u0142\u0141\u0294'\u2019\u02bc\"]+")
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


cnt, card, gloss = collections.Counter(), {}, {}
for ent in E:
    zh = ent.get("zh") or ""
    fs = [(ent.get("hw"), zh), (ent.get("paradigm"), zh)]
    fs += [(x.get("t"), x.get("zh") or zh) for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        sz = s.get("zh") or zh
        fs += [(s.get("form"), sz), (s.get("paradigm"), sz)]
        fs += [(x.get("t"), x.get("zh") or sz) for x in s.get("examples", [])]
    for f, z in fs:
        if not f:
            continue
        for w in TOK.findall(f):
            k = key(w)
            if len(k) > 1 and k not in MAP and k not in OV and k not in CL and k not in PROSE:
                cnt[k] += 1
                card.setdefault(k, (ent.get("hw") or "").split(" ")[0])
                gloss.setdefault(k, z)

# the shapes his orthography licenses: x>h always; o>u; l>r or l kept; final ao>aw;
# apostrophe dropped or realised as a repeated vowel (his elision mark)
def shapes(k):
    base = k.replace("x", "h")
    outs = set()
    for lr in (base.replace("l", "r"), base):
        for ao in ({lr[:-2] + "aw"} if lr.endswith("ao") else set()) | {lr}:
            s = ao.replace("o", "u")
            outs.add(s.replace("'", ""))
            outs.add(s.replace("'", "e"))
            m = re.sub(r"([aeiou])'", r"\1\1", s)
            outs.add(m.replace("'", ""))
    return {o for o in outs if o and o != k}


rows = []
for k, n in cnt.items():
    hits = [(s, OMNI.get(s), SPK.get(s, 0)) for s in sorted(shapes(k))
            if s in OMNI or SPK.get(s, 0)]
    if hits:
        rows.append((n, k, hits))
rows.sort(key=lambda r: -r[0])
print("green types: %d   with an ATTESTED rule-consistent shape: %d"
      % (len(cnt), len(rows)))
for n, k, hits in rows:
    print("\n%3dx %-14s [%s] %s" % (n, k, card[k], (gloss[k] or "")[:44]))
    for s, g, sp in hits:
        print("       %-14s speech %-5s %s" % (s, sp, (g or "-- speech only")[:46]))
