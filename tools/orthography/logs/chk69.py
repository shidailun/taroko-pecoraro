"""Round two on the four that did not clear.

sinao is answered and dropped: pnsinaw 被用來…釀酒, ptgsinaw 因酒而死, ksinaw 好酒
all sit on that root, so sinaw carries the wine sense and the 洗;清潔 row is just
the other half of a homograph he himself flags on the card.

Left: tasil (石頭 vs 因壓扁而硬), ita/nita (root of "see" vs 我們), ksa (你說！ vs 走),
bbuyo (黑暗 vs 打獵), toxoi (my search string was mistyped -- 陪, not 陳).

This prints every omnibus row on the stem, so the question is not "what is the
first gloss" but "does this shape do this job anywhere", and then his own card
slots and examples so the homograph risk is visible before anything is written.
"""
import io, sys, json, pickle, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
OMNI = collections.defaultdict(list)
for w, g, _ in ROWS:
    if w and g:
        OMNI[w.lower()].append(g)

STEMS = ["tasil", "ita", "ksa", "bbuyu", "tuhuy"]
for st in STEMS:
    print("\n=== omnibus rows whose word contains %r ===" % st)
    hits = sorted(((SPK.get(w, 0), w) for w in OMNI if st in w), reverse=True)
    for s, w in hits[:14]:
        used = [x for x in MAP if MAP[x] == w]
        print("   %-14s spk %-5d %-38s %s" % (
            w, s, " | ".join(dict.fromkeys(OMNI[w]))[:38],
            ("<= his " + ",".join(used[:3])) if used else ""))

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
LOOK = {"ita", "nita", "ksa", "bbuyo", "toxoi", "tasil"}
print("\n\n########## his own cards ##########")
for ent in E:
    hw = ent.get("hw") or ""
    if key(TOK.findall(hw)[0] if TOK.findall(hw) else "") not in LOOK:
        continue
    print("\n--- %s  %s" % (hw, (ent.get("zh") or "")[:100]))
    for x in ent.get("examples", [])[:4]:
        print("      ex  %-46s %s" % ((x.get("t") or "")[:46], (x.get("zh") or "")[:44]))
    for s in ent.get("subs", [])[:6]:
        print("      sub %-16s %s" % ((s.get("form") or "")[:16], (s.get("zh") or "")[:52]))

print("\n########## where the loose tokens actually occur ##########")
for target in ["ita", "nita", "ksa"]:
    print("\n-- %s --" % target)
    n = 0
    for ent in E:
        rows = [(x.get("t"), x.get("zh")) for x in ent.get("examples", [])]
        for s in ent.get("subs", []):
            rows += [(x.get("t"), x.get("zh")) for x in s.get("examples", [])]
        for f, g in rows:
            if target in [key(w) for w in TOK.findall(f or "")]:
                print("   [%-10s] %-42s %s" % ((ent.get("hw") or "")[:10],
                                               (f or "")[:42], (g or "")[:40]))
                n += 1
                if n >= 9:
                    break
        if n >= 9:
            break
