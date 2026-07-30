"""Card-level root coherence: find the pax pattern mechanically.

Every real defect found by reading audit2 in frequency order had the SAME
signature, and it is not a semantic judgment -- it is the map contradicting
itself on a single card of his:

   PAX     his pnax  > pnaah  (right)  while pax   > pax   (an onomatopoeia)
   LOAN    his lowan > ruwan  (right)  while loan  > ruan
   NGALI   his nngali> nngari (right)  while ngali > ngali (the take word)
   PS'LO   his ps'lo > psru   (right)  while psloon> psluun (steam)

In each case one card's slots agree on a modern root and one slot walks off to a
different root. That is checkable without reading a gloss, so it can be run over
all 1967 cards instead of the 70 rows an evening of reading covers.

Method. For each card, take every token in its definitional slots (headword,
paradigm, subs -- NOT examples, which bring in whole sentences of other words),
map each through the shipped map, and reduce each VALUE to its consonant
skeleton with the modern affixes stripped. Affixes here are the productive Truku
ones his own paradigms are built from. If >=3 slots agree on one skeleton and at
least one slot has a different skeleton, that slot is the outlier and gets
printed with its gloss and the majority's.

This over-flags by construction -- a card can legitimately hold two roots (his
cross-references, his 參見 forms, compound entries), and the majority skeleton
can be an artefact of stripping. It is a WORK LIST, not a verdict; every hit
still has to be read. What it buys is that the reading is aimed.
"""
import io, sys, json, pickle, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
MM = json.load(io.open(H + "tools/orthography/modern_map.json", encoding="utf-8"))["map"]
MAP = {k: v["modern"] for k, v in MM.items()}
TIER = {k: v["tier"] for k, v in MM.items()}
OMNI = collections.defaultdict(list)
for w, g, _ in ROWS:
    if w and g:
        OMNI[w.lower()].append(g)

# productive affixes, longest first so em- is tried before m-
PRE = ["empke", "empte", "empge", "empse", "emp", "emp", "kmp", "smn", "tmn", "pn",
       "sn", "gn", "kn", "mn", "tn", "dm", "gm", "km", "sm", "tm", "pk", "sk", "tg",
       "mp", "ms", "mt", "mk", "mq", "mg", "em", "m", "p", "s", "k", "t", "g", "d", "n"]
SUF = ["anay", "away", "un", "an", "ay", "i", "aw"]


def skel(v):
    """strip productive affixes, then drop vowels -- what is left is the root's
    consonant frame, which is what "the same word" looks like across a paradigm"""
    w = v.lower()
    for p in PRE:
        if w.startswith(p) and len(w) - len(p) >= 2:
            w = w[len(p):]
            break
    for s in SUF:
        if w.endswith(s) and len(w) - len(s) >= 2:
            w = w[:-len(s)]
            break
    w = re.sub(r"(.)\1+", r"\1", w)          # geminates
    return re.sub(r"[aeiou]", "", w) or w


TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


def clean(g):
    g = re.sub(r"\uff08\u8a3b[^\uff09]*\uff09?", "", g or "")
    return re.sub(r"\s+", " ", re.sub(r"\u53c3\u898b.*$", "", g)).strip()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
MINGROUP = int(sys.argv[1]) if len(sys.argv) > 1 else 3
hits = []
for ent in E:
    hw = ent.get("hw") or ""
    slots = [(ent.get("hw"), ent.get("zh"))]
    if ent.get("paradigm"):
        slots.append((ent.get("paradigm"), ent.get("zh")))
    for s in ent.get("subs", []):
        slots.append((s.get("form"), s.get("zh") or ent.get("zh")))
    seen = {}
    for f, g in slots:
        for w in TOK.findall(f or ""):
            k = key(w)
            if k in MAP and k not in seen:
                seen[k] = (MAP[k], clean(g))
    if len(seen) < MINGROUP + 1:
        continue
    groups = collections.Counter(skel(v) for v, _ in seen.values())
    top, n = groups.most_common(1)[0]
    if n < MINGROUP or len(groups) < 2:
        continue
    maj = [k for k, (v, _) in seen.items() if skel(v) == top]
    for k, (v, g) in seen.items():
        if skel(v) == top:
            continue
        # a value that IS attested with a substantive gloss is a claim; a blind
        # one asserts nothing and belongs to the separate blind-identity problem
        if not OMNI.get(v.lower()):
            continue
        hits.append((n, hw, k, v, TIER.get(k, "?"), SPK.get(v.lower(), 0),
                     g, " | ".join(dict.fromkeys(OMNI[v.lower()]))[:40],
                     ", ".join("%s>%s" % (a, seen[a][0]) for a in maj[:4])))

hits.sort(key=lambda r: (-r[0], r[1]))
print("%d outlier slots on cards whose other slots agree on one modern root "
      "(min group %d)\n" % (len(hits), MINGROUP))
LO = int(sys.argv[2]) if len(sys.argv) > 2 else 0
HI = int(sys.argv[3]) if len(sys.argv) > 3 else 60
for n, hw, k, v, ti, spk, g, mg, maj in hits[LO:HI]:
    print("[%-16s] %-13s -> %-13s %-2s spk%-5d  (%d slots agree)" % (
        hw[:16], k, v, ti, spk, n))
    print("      his %s" % g[:74])
    print("      mod %s" % mg[:74])
    print("      maj %s" % maj[:74])
