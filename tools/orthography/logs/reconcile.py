"""WHAT THE READER ACTUALLY SEES AS UNVERIFIED -- reconciled back to its source.

The census counts the DOM: 223 green types. Every sweep in this review walks
entries.js and finds 203. The gap is not rounding, it is a set of fields nothing
has ever looked at -- tag, paradigm and crossRef, on both entries and subs. Those
carry his cross-reference targets (real Truku headwords: qtqot, bsq'lol, q'lox,
ggal) alongside the metadata labels the app greys (name, emprunt, jap, chin,
plant, animal) and French prose.

Worse, the DOM shows the charRules OUTPUT, so a green in the census is not a
token you can look up in his text at all -- srhqun, rngut, hru and musa are
things the fallback printed, not things he wrote. Every one of them has to be
traced back to the token that produced it before it can be checked.

This does both: walks EVERY field, applies charRules, and groups by what lands
on screen. The output is the real worklist -- display form, the source tokens
behind it, how often, and where to read it.
"""
import io, sys, json, re, collections, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
MM = json.load(io.open(H + "tools/orthography/modern_map.json", encoding="utf-8"))["map"]
MAP = {k: v["modern"] for k, v in MM.items()}

SPELLING = {"x": "h", "o": "u", "l": "r"}


def charrules(w):
    out = w.replace("\u00e7", "\u0001").replace("\u00c7", "\u0001")
    out = out.replace("\u0142", "l").replace("\u0141", "l")
    out = re.sub("['\u2019\u02bc\"\u0294]", "", out)
    out = "".join(c for c in unicodedata.normalize("NFD", out)
                  if not unicodedata.combining(c))
    out = out.lower()
    out = re.sub(r"ao$", "aw", out)
    out = "".join(SPELLING.get(c, c) for c in out)
    return out.replace("\u0001", "x")


TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("['\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


# what the app greys before respellable() ever runs
META = set("""name emprunt jap chin plant animal note var cf syn ant lit fig""".split())
FRENCH = set("""qui est bien plus meme même souvent porter parfois bouche vie
suite entendu rouge produit contraction vouloir bonte bonté beaute beauté hotte
remarque probable serait avec dérivé dérivée précédent variante une chinois
terme image sans doute pluriel travers tordu inconnue très peu aurait parentée
crâne relation scie peau taroko""".split())

e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])

src = collections.defaultdict(collections.Counter)   # display -> Counter(source token)
where = {}                                           # source token -> (hw, field, text, gloss)
for ent in E:
    hw = ent.get("hw") or ""
    fields = [("hw", ent.get("hw"), ent.get("zh")),
              ("tag", ent.get("tag"), ent.get("zh")),
              ("paradigm", ent.get("paradigm"), ent.get("zh")),
              ("crossRef", ent.get("crossRef"), ent.get("zh"))]
    fields += [("ex", x.get("t"), x.get("zh")) for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        g = s.get("zh") or ent.get("zh")
        fields += [("sub", s.get("form"), g),
                   ("sub.paradigm", s.get("paradigm"), g),
                   ("sub.crossRef", s.get("crossRef"), g)]
        fields += [("ex", x.get("t"), x.get("zh")) for x in s.get("examples", [])]
    for fld, txt, gloss in fields:
        for w in TOK.findall(txt or ""):
            k = key(w)
            if k in MAP or len(k) < 3 or k in META or k in FRENCH:
                continue
            src[charrules(k)][k] += 1
            where.setdefault(k, (hw, fld, txt, gloss))

print("GREEN display forms: %d types, %d occurrences\n"
      % (len(src), sum(sum(c.values()) for c in src.values())))

NEW = {"tag", "paradigm", "crossRef", "sub.paradigm", "sub.crossRef"}
never = [(d, c) for d, c in src.items()
         if all(where[t][1] in NEW for t in c)]
print("=== of those, NEVER SWEPT (live only in tag/paradigm/crossRef): %d ===\n"
      % len(never))
for d, c in sorted(never, key=lambda x: -sum(x[1].values())):
    for t, n in c.most_common():
        hw, fld, txt, gloss = where[t]
        print("%2dx %-13s <- %-13s [%-10s] %-12s %s"
              % (n, d, t, hw[:10], fld, (txt or "")[:34]))
        print("        %s" % (gloss or "")[:70])

print("\n=== the whole worklist, by occurrence ===")
for d, c in sorted(src.items(), key=lambda x: -sum(x[1].values()))[:45]:
    n = sum(c.values())
    toks = " ".join("%s(%d)" % (t, m) for t, m in c.most_common(3))
    hw = where[c.most_common(1)[0][0]][0]
    print("%3dx %-14s <- %-30s [%s]" % (n, d, toks, hw[:12]))
