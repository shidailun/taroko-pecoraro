"""Card-level root coherence, done without a morphology guess.

audit3 stripped productive affixes off each value and compared consonant frames.
That flooded: the stripper cannot tell an affix from a root-initial consonant, so
paru lost its p- and became "r" while mkparu kept it and became "pr", and the
PARO card -- entirely correct -- came out as three defects. Every high-ranked hit
was that artefact.

So drop morphology altogether. Truku derivation is affixing, not stem mutation,
which means the slots of one card share a literal substring: adas/madas/mnadas/
nadas/dsun all carry "as", huqil/mhuqil/hqilan/hhuqil carry "qil". Find, per card,
the substring of length>=3 that the most values contain; the values that do NOT
contain it are the outliers. No affix list, nothing to get wrong.

That is exactly the signature every real defect in this review had:

   PAX     pnax > pnaah  carries "aah"   while pax > pax     does not
   LOAN    lowan> ruwan  carries "uwa"   while loan> ruan    does not
   NGALI   nngali>nngari carries "gari"  while ngali>ngali   does not
   PS'LO   ps'lo> psru   carries "sru"   while psloon>psluun does not

Still a work list, not a verdict. Legitimate reasons for an outlier exist -- his
cross-references, suppletive forms, compound entries, and cards where he filed
two words together. Every hit is read before anything is written. The value is
that the reading is aimed at 1967 cards instead of 1290 rows.

Only outliers whose value is ATTESTED with a substantive gloss are printed: a
blind value asserts nothing about meaning and belongs to the separate
blind-identity problem, already tracked.
"""
import io, sys, json, pickle, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
MM = json.load(io.open(H + "tools/orthography/modern_map.json", encoding="utf-8"))["map"]
MAP = {k: v["modern"] for k, v in MM.items()}
TIER = {k: v["tier"] for k, v in MM.items()}
LEX = json.load(io.open(H + "tools/orthography/lexical_map.json", encoding="utf-8"))
OMNI = collections.defaultdict(list)
for w, g, _ in ROWS:
    if w and g:
        OMNI[w.lower()].append(g)
TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


def clean(g):
    g = re.sub(r"\uff08\u8a3b[^\uff09]*\uff09?", "", g or "")
    return re.sub(r"\s+", " ", re.sub(r"\u53c3\u898b.*$", "", g)).strip()


MINSUB = 3
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
MINGROUP = int(sys.argv[1]) if len(sys.argv) > 1 else 4
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
                seen[k] = (MAP[k].lower(), clean(g))
    if len(seen) < MINGROUP + 1:
        continue
    # the substring the most values share
    cand = collections.Counter()
    for v, _ in seen.values():
        for L in range(MINSUB, min(len(v), 7) + 1):
            for i in range(len(v) - L + 1):
                cand[v[i:i + L]] += 1
    if not cand:
        continue
    best = max(cand, key=lambda c: (cand[c], len(c)))
    n = cand[best]
    if n < MINGROUP:
        continue
    out = [k for k, (v, _) in seen.items() if best not in v]
    if not out or len(out) > len(seen) - n:
        pass
    maj = [k for k, (v, _) in seen.items() if best in v]
    for k in out:
        v, g = seen[k]
        if not OMNI.get(v):
            continue
        hits.append((n, len(out), hw, k, v, TIER.get(k, "?"), SPK.get(v, 0), best,
                     g, " | ".join(dict.fromkeys(OMNI[v]))[:38],
                     ", ".join("%s>%s" % (a, seen[a][0]) for a in maj[:4])))

# rank: cards with a big agreeing majority and ONE dissenter are the strongest
hits.sort(key=lambda r: (r[1], -r[0], r[2]))
print("%d outlier slots (majority >= %d slots sharing one substring)\n"
      % (len(hits), MINGROUP))
LO = int(sys.argv[2]) if len(sys.argv) > 2 else 0
HI = int(sys.argv[3]) if len(sys.argv) > 3 else 40
for n, no, hw, k, v, ti, spk, best, g, mg, maj in hits[LO:HI]:
    print("[%-15s] %-13s -> %-13s %-2s spk%-5d  (%d share %r, %d outlier)%s" % (
        hw[:15], k, v, ti, spk, n, best, no,
        "  !!LEXNULL!!" if (k in LEX and not LEX[k]) else ""))
    print("      his %s" % g[:72])
    print("      mod %s" % mg[:72])
    print("      maj %s" % maj[:72])
