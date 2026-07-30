"""The wrong-brown audit, aimed at the branch that actually produces them.

audit1 flagged 461 keys on zero shared gloss characters and was almost all noise,
for two reasons worth writing down. First, Chinese synonyms share no characters:
his 壞的－惡毒的 against modern 不好, his 何時 against 什麼時候, his 最近 against
上一次 -- all correct, all flagged. Character overlap cannot do semantics.
Second and worse, it EXCLUDED the very defect that motivated it: its guard
skipped any key whose value equals the charRules output, and ms'lut > msrut IS
the charRules output. S'LUT would never have appeared.

Reading build_modern_map.py says where these come from. Its step 1 is:

    # 1. identity
    if n in attested:
        result[t] = {"modern": ..., "tier": "id"}

-- his token, normalised, exists somewhere in modern Truku, therefore his word IS
that word. No gloss is consulted. That is 1070 keys. Tier B is 1311 more, "unique
attested candidate (no gloss available/needed)". Only tier A (467) required gloss
evidence, and it required gloss>=2 to get it.

So ~2400 brown keys assert a meaning nobody ever checked. That is the population,
and character overlap cannot filter it -- but I can read it. This prints it one
line per key, his definition against every modern sense, in frequency order,
so the judging is done by someone who can tell 不好 from 刀鋒鈍了.

Only keys with BOTH a definitional gloss of his and at least one modern gloss are
printed; the rest assert nothing checkable and belong to the blind-identity
problem, which is tracked separately.
"""
import io, sys, json, pickle, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
MM = json.load(io.open(H + "tools/orthography/modern_map.json", encoding="utf-8"))["map"]
OMNI = collections.defaultdict(list)
for w, g, _ in ROWS:
    if w and g:
        OMNI[w.lower()].append(g)

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


def clean(g):
    """his definitions carry his apparatus; the note and the cross-reference are
    not part of the meaning and they crowd out the meaning on a one-line report"""
    g = re.sub(r"\uff08\u8a3b[^\uff09]*\uff09?", "", g or "")
    g = re.sub(r"\u53c3\u898b.*$", "", g)
    return re.sub(r"\s+", " ", g).strip()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
cnt = collections.Counter()
gloss, card = {}, {}
for ent in E:
    hw, top = ent.get("hw") or "", ent.get("zh") or ""
    defs = [(ent.get("hw"), top), (ent.get("paradigm"), top)]
    for s in ent.get("subs", []):
        sg = s.get("zh") or top
        defs += [(s.get("form"), sg), (s.get("paradigm"), sg)]
    for f, g in defs:
        w = TOK.findall(f or "")
        if w and len(clean(g)) > len(gloss.get(key(w[0]), "")):
            gloss[key(w[0])], card[key(w[0])] = clean(g), hw
    every = defs + [(x.get("t"), "") for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        every += [(x.get("t"), "") for x in s.get("examples", [])]
    for f, _g in every:
        for w in TOK.findall(f or ""):
            cnt[key(w)] += 1

WANT = set(sys.argv[1].split(",")) if len(sys.argv) > 1 else {"id", "B"}
LO = int(sys.argv[2]) if len(sys.argv) > 2 else 0
HI = int(sys.argv[3]) if len(sys.argv) > 3 else 60
rows = []
for k, info in MM.items():
    if info.get("tier") not in WANT or k not in cnt:
        continue
    v = info["modern"]
    senses = list(dict.fromkeys(OMNI.get(v.lower()) or []))
    hg = gloss.get(k, "")
    if not senses or not hg:
        continue
    rows.append((cnt[k], k, v, info["tier"], hg, " | ".join(senses)))
rows.sort(reverse=True)
print("tiers %s: %d keys assert an unchecked meaning and can be checked\n"
      % ("/".join(sorted(WANT)), len(rows)))
for c, k, v, ti, hg, mg in rows[LO:HI]:
    print("x%-3d %-13s -> %-13s %-2s spk%-5s" % (c, k, v, ti, SPK.get(v.lower(), 0)))
    print("      his %s" % hg[:78])
    print("      mod %s" % mg[:78])
