"""THE FALLBACK MAY ALREADY BE RIGHT -- and nobody has ever checked.

Green means UNVERIFIED, not unchanged. An unmapped word still reaches the screen
in modern dress, because charRules rewrites it: x>h, o>u, l>r, word-final -ao>
-aw, every elision mark and diacritic stripped. That output is a guess. But the
green tail of the census is full of strings that are not guesses at all --
musa, hru, rngut, qtqut, srhqun -- real modern Truku words, sitting green.

So ask the question the review has never asked: for each green, is the string
charRules ALREADY PUTS ON SCREEN an attested modern word? If it is, and the
gloss agrees with his slot, then the fallback got this one right by luck and the
only thing missing is the verification. Converting it changes nothing visible --
the reader sees the same letters before and after -- and moves the word from
"we have no opinion" to "checked, and correct".

That is the cheapest class of win left in the dictionary, and it is invisible to
every sweep built so far, because they all GENERATE candidates that differ from
the display form and rank them; a candidate identical to what is already shown
scores as a non-event.

The gloss is still what decides. A green whose charRules output happens to
collide with an unrelated modern word is the dangerous case -- kmalu 正在梳 is
exactly that -- so his slot gloss and the omnibus gloss are printed side by side
and nothing is asserted here.

Usage: python charhit.py [MINSLOT]
"""
import io, sys, json, pickle, re, collections, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
MM = json.load(io.open(H + "tools/orthography/modern_map.json", encoding="utf-8"))["map"]
MAP = {k: v["modern"] for k, v in MM.items()}
OMNI = collections.defaultdict(list)
for w, g, _ in ROWS:
    if w and g:
        OMNI[w.lower()].append(g)

SPELLING = {"x": "h", "o": "u", "l": "r"}


def charrules(w):
    """The app's fallback, mirrored. ç parks as x and is restored last."""
    out = w.replace("\u00e7", "\u0001").replace("\u00c7", "\u0001")
    out = out.replace("\u0142", "l").replace("\u0141", "l")
    out = re.sub("['\u2019\u02bc\"\u0294]", "", out)
    out = "".join(c for c in unicodedata.normalize("NFD", out)
                  if not unicodedata.combining(c))
    out = out.lower()
    out = re.sub(r"a o$".replace(" ", ""), "aw", out)
    out = "".join(SPELLING.get(c, c) for c in out)
    return out.replace("\u0001", "x")


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

FRENCH = set("""qui est bien plus meme même souvent porter parfois bouche vie
suite entendu rouge produit var contraction vouloir bonte bonté beaute beauté
hotte remarque""".split())

MIN = int(sys.argv[1]) if len(sys.argv) > 1 else 1
greens = sorted({t for t in his if t not in MAP and len(t) > 2 and t not in FRENCH},
                key=lambda t: -len(his[t]))

hits, miss = [], []
for t in greens:
    if len(his[t]) < MIN:
        continue
    d = charrules(t)
    (hits if d in OMNI else miss).append((len(his[t]), t, d))

print("greens checked: %d" % len([t for t in greens if len(his[t]) >= MIN]))
print("THE FALLBACK'S OUTPUT IS AN ATTESTED MODERN WORD: %d" % len(hits))
print("not attested (the genuinely unreachable tail): %d\n" % len(miss))

for n, t, d in sorted(hits, reverse=True):
    hw, kind, f, g = his[t][0]
    same = " (unchanged)" if d == t else ""
    print("%2dx %-13s -> %-13s spk %-5d%s" % (n, t, d, SPK.get(d, 0), same))
    print("      THEIRS %s" % " | ".join(dict.fromkeys(OMNI[d]))[:64])
    print("      HIS    [%-10s] %s" % (hw[:10], (g or "")[:60]))
    print("      slot   %s" % (f or "")[:70])
