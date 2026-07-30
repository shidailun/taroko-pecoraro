"""Five sib.py rows whose brown sibling I have never actually looked up.

The point of the half-brown test is that a mapped sibling has already decided the
root -- but only if the SIBLING'S OWN VALUE is attested. A blind identity claim in
the brown column decides nothing, and half the rows below may be exactly that. So
for each: his card, every key of his the map answered, and then the crucial column
-- is the shipped value itself attested, in the omnibus or the spoken corpus?

 TABE     tbian>tbiyan and tnbiyan>tnbiyan are brown, so the map already believes
          in a tbi- root. If tbiyan is attested, tabe>tabi stops being blind.
 TBAKO    tbako>lumak is a LEXICAL substitution (tobacco), so stbako 有菸味 cannot
          be spelled out by rule -- it has to be s- + whatever lumak takes.
 T"TO     five brown keys all on teetu; t"tuan is the -an nominal of that.
 S'LUT    the brown column DISAGREES WITH ITSELF: s'lut>slut keeps the l,
          ms'lut>msrut and ps'lut>psrut turn it into r. One of those is wrong.
 KSIA     four brown keys on qsiya; pksyaon 想要液化之物 is the -un irrealis.
"""
import io, sys, json, pickle, re
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
LEX = json.load(io.open(H + "tools/orthography/lexical_map.json", encoding="utf-8"))
OMNI = {}
for w, g, _ in ROWS:
    if w:
        OMNI.setdefault(w.lower(), g)
ALL = sorted(set(OMNI) | set(SPK))
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])


def att(v):
    """the column that matters: is the shipped value a real modern word?"""
    o, s = OMNI.get(v), SPK.get(v, 0)
    if o:
        return "OMNI %-24s spk %d" % (o[:24], s)
    return "-- BLIND --%s" % ("  spk %d" % s if s else "")


CASES = [
    ("TABE 犁", r"^TABE", r"^p?m?p?t?ab?[ei]|tbi", r"tbiy|tabi|sakur|tmabu"),
    ("TBAKO 菸草", r"^TBAKO", r"tbako|lumak", r"lumak|tbaku|tabaku"),
    ("T\"TO / TA'TO 切", r"^T[\"']?TO|^TA'TO", r"t'to|ta'to|t\"tu|ttuu|teetu", r"teetu|ttu"),
    ("S'LUT 黏", r"^S'LUT|^SL'D", r"s'lut|sl'd", r"^p?m?s[lr]ut|sldan|srudan"),
    ("KSIA 水", r"^KSIA", r"ksia|ksya", r"qsiya"),
]

for label, cardpat, keypat, shape in CASES:
    print("\n" + "=" * 76)
    print("== %s" % label)
    cp = re.compile(cardpat)
    for ent in E:
        if not cp.match((ent.get("hw") or "").upper()):
            continue
        print("   hw %s %s  |  %s"
              % (ent.get("hw"), ent.get("tag") or "", (ent.get("zh") or "-")[:52]))
        for x in ent.get("examples", []):
            print("   \u00a7 %-46s %s" % (x.get("t", "")[:46], (x.get("zh") or "")[:34]))
        for s in ent.get("subs", []):
            print("   - %-18s %s" % (s.get("form", ""), (s.get("zh") or "")[:44]))
            for x in s.get("examples", []):
                print("       \u00a7 %-42s %s"
                      % (x.get("t", "")[:42], (x.get("zh") or "")[:32]))
    print("   -- his keys already answered, WITH the value's own attestation --")
    kp = re.compile(keypat)
    got = 0
    for k in sorted(MAP):
        if kp.search(k):
            print("      %-14s -> %-14s %s" % (k, MAP[k], att(MAP[k])))
            got += 1
    if not got:
        print("      (none)")
    blk = [k for k in LEX if kp.search(k) and not LEX[k]]
    if blk:
        print("      LEXNULL:", blk)
    print("   -- modern by shape /%s/ --" % shape)
    r, n = re.compile(shape), 0
    for w in ALL:
        if r.search(w):
            print("      %-18s %-32s spk %s"
                  % (w, (OMNI.get(w) or "-")[:32], SPK.get(w, 0)))
            n += 1
            if n >= 24:
                print("      ...")
                break
    if not n:
        print("      (nothing)")
