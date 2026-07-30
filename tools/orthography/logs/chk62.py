"""Three more clusters, by occurrence, with the half-brown test.

   LIKUT   likut 2 + tnlikut 2 + mplikut 1 + mlikut 1 + nlikut 1 + nplikut 1 = 8
   覆蓋     sinbong 1 + npamuxul 1 (+ their card's siblings)
   MTMAGO  mtmago 2, 驕傲

The matcher scored all of these below 0.44, i.e. it found only a coincidental
gloss substring (`tnhadut` 送的人 for his tnlikut 找藉口的人 -- the shared string is
"的人"). That is exactly the case where the matcher is useless and the family is
not: print his card, his keys the map already answered, and the modern root by
gloss with the RIGHT search terms rather than by shape.
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
TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


CASES = [
    ("LIKUT 藉口/詭計", {"likut", "tnlikut", "mplikut", "mlikut", "nlikut",
                     "nplikut"}, r"likut", ("藉口", "推託", "詭計", "騙", "推諉")),
    ("覆蓋/塗抹", {"sinbong", "npamuxul", "pamuxul", "smbong"},
     r"sinbong|bong|muxul", ("塗抹", "覆蓋", "鋪開", "塗")),
    ("MTMAGO 驕傲", {"mtmago", "tmago", "ktmago"}, r"tmago|tmagu",
     ("驕傲", "自大", "傲慢", "自誇")),
]

for label, words, keypat, glosses in CASES:
    print("\n" + "=" * 74)
    print("== %s" % label)
    shown = set()
    for ent in E:
        hw = ent.get("hw") or ""
        slots = [(ent.get("hw"), ent.get("zh")), (ent.get("paradigm"), ent.get("zh"))]
        slots += [(x.get("t"), x.get("zh")) for x in ent.get("examples", [])]
        for s in ent.get("subs", []):
            slots += [(s.get("form"), s.get("zh")), (s.get("paradigm"), s.get("zh"))]
            slots += [(x.get("t"), x.get("zh")) for x in s.get("examples", [])]
        for f, g in slots:
            if f and ({key(w) for w in TOK.findall(f)} & words):
                sig = (hw, f[:40])
                if sig in shown:
                    continue
                shown.add(sig)
                print("   [%-14s] %-50s | %s" % (hw[:14], f[:50], (g or "")[:36]))
    print("   -- his keys already answered --")
    kp = re.compile(keypat)
    got = 0
    for k in sorted(MAP):
        if kp.search(k):
            print("      %-14s -> %-14s omni %-22s spk %s"
                  % (k, MAP[k], (OMNI.get(MAP[k]) or "-")[:22], SPK.get(MAP[k], 0)))
            got += 1
            if got > 14:
                print("      ...")
                break
    if not got:
        print("      (none -- the whole family is green)")
    blk = [k for k in LEX if kp.search(k) and not LEX[k]]
    if blk:
        print("      LEXNULL:", blk)
    print("   -- modern by gloss %s --" % "/".join(glosses))
    seen = set()
    for w, g, _ in ROWS:
        if w and g and any(z in g for z in glosses) and w.lower() not in seen:
            seen.add(w.lower())
            print("      %-16s %-34s spk %s" % (w, g[:34], SPK.get(w.lower(), 0)))
            if len(seen) >= 22:
                print("      ...")
                break
