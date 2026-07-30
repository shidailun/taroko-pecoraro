"""Three questions left before batch 68 is writable.

1. xbagun -- his XUBAO example spells the root himself: xbagun against modern
   hbagun 會被…割傷. Is that key already mapped, and what else on the card is?
2. nilao -> ngiraw is one letter (an inserted g) and fits his 栽培/樹幹 note, but
   he writes ng in 15 headwords, so he would have written NGILAO. That is a
   DECIDABLE question: take every one of his n-initial headwords and ask whether
   the value the map already ships for it begins with ng. If his n never stands
   for a modern ng anywhere else, nilao->ngiraw dies.
3. nuxul -- confirm nothing else on the LUKUS card depends on the nuhur reading,
   and that muxul/meuxul is the settled value for the same word elsewhere.
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

print("======== 1. XBAGUN and the rest of the XUBAO example")
for t in ("xbagun", "klxangi", "aadi", "btunuc", "xei"):
    v = MAP.get(t)
    print("    %-12s -> %-14s %-3s  %s"
          % (t, v or "GREEN", TIER.get(t, ""),
             " | ".join(dict.fromkeys(OMNI.get((v or "").lower()) or []))[:40]))
print("    modern hbagun:", OMNI.get("hbagun"), "spk", SPK.get("hbagun", 0))

print("\n======== 2. does his n- EVER stand for a modern ng-?")
nn = ng = 0
rows = []
for ent in E:
    hw = ent.get("hw") or ""
    if not re.match(r"^N[A-Z']", hw):
        continue
    k = key(hw)
    v = MAP.get(k)
    if not v:
        continue
    nn += 1
    if v.startswith("ng"):
        ng += 1
    rows.append((v.startswith("ng"), hw, v, TIER.get(k, "")))
for flag, hw, v, t in sorted(rows, reverse=True)[:24]:
    print("    %s %-12s -> %-14s %s" % ("NG!" if flag else "   ", hw, v, t))
print("    his n-initial headwords with a value: %d, of which modern ng-: %d" % (nn, ng))
print("    and the reverse -- his NG- headwords, do they ship ng-?")
for ent in E:
    hw = ent.get("hw") or ""
    if re.match(r"^NG", hw):
        k = key(hw)
        print("        %-12s -> %-14s %s" % (hw, MAP.get(k, "GREEN"), TIER.get(k, "")))

print("\n======== 3. LUKUS card, the nuxul slot in context")
for ent in E:
    if (ent.get("hw") or "") != "LUKUS":
        continue
    for x in ent.get("examples", []):
        t = x.get("t") or ""
        if "nuxul" in t.lower():
            print("    %s" % t)
            print("    %s" % (x.get("zh") or ""))
            for w in TOK.findall(t):
                k = key(w)
                print("        %-12s -> %-14s %s" % (k, MAP.get(k, "GREEN"), TIER.get(k, "")))
print("    muxul ships:", MAP.get("muxul"), TIER.get("muxul"), "| occurrences:", len(his.get("muxul", [])))
print("    nuxul ships:", MAP.get("nuxul"), TIER.get("nuxul"), "| occurrences:", len(his.get("nuxul", [])))
print("    meuxul in omnibus:", OMNI.get("meuxul"), "spk", SPK.get("meuxul", 0))
