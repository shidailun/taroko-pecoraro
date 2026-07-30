"""Confirm before writing. Three questions, each of which could sink a fix.

1. TABE. If tabe>sakur and ptabe>psakur go in, the card's EXISTING browns become
   the odd ones out: tbian>tbiyan and tbiyan>tbiyan, where modern tbiyan means
   下來 "come down". Before calling those wrong I have to know they are only his
   plough word -- if some OTHER card of his also spells a descend-word tbian, the
   flat map cannot serve both and the current value may be right for that card.
   So: every card that contains any tbi- token, printed with its gloss.

2. T"TO. lexical_map nulls ttuun and ttuon, and its note gives the reason: "the
   modern root is teetu, but its OWN DERIVED SLOTS are the OTHER teetu" -- i.e.
   it looked for cut-sense derivatives and found only the uphill homonym. That
   premise is what chk64 just falsified: ttui 切、剁 spk 2 is a cut-sense
   derivative, with his exact gloss. Print the omnibus row for ttui verbatim, and
   every ttu-shaped word in either corpus, before touching a reasoned null.

3. S'LUT. Modern 黏 returned only the agil family, which is 黏液/黏稠 "viscous,
   slimy" -- a property of honey, not a relation between a house and a cliff. His
   sense is 黏著於 "adhere TO, abut, follow the shape of". Try the other way in:
   his own example glosses (貼近, 貼在, 接合) as search terms, and the whole agil
   root, to see whether either actually reaches his meaning. If neither does, the
   three browns on that card are wrong and unfixable, which is a lexical_map
   null, not a batch entry.
"""
import io, sys, json, pickle, re
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
OMNI, RAW = {}, {}
for w, g, x in ROWS:
    if w:
        OMNI.setdefault(w.lower(), g)
        RAW.setdefault(w.lower(), (w, g, x))
ALL = sorted(set(OMNI) | set(SPK))
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


print("== 1. every card of his containing a tbi-/tabe token ==")
pat = re.compile(r"^p?n?t['\"]?b(i|iy|ia)")
for ent in E:
    hw = ent.get("hw") or ""
    slots = [(ent.get("hw"), ent.get("zh")), (ent.get("paradigm"), ent.get("zh"))]
    slots += [(x.get("t"), x.get("zh")) for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        slots += [(s.get("form"), s.get("zh")), (s.get("paradigm"), s.get("zh"))]
        slots += [(x.get("t"), x.get("zh")) for x in s.get("examples", [])]
    hits = sorted({key(w) for f, g in slots if f for w in TOK.findall(f)
                   if pat.match(key(w))})
    if hits:
        print("   [%-14s %-22s] %s" % (hw[:14], (ent.get("zh") or "-")[:22],
                                       " ".join(hits[:9])))

print("\n== 2. ttui verbatim, and every ttu-shaped modern word ==")
if "ttui" in RAW:
    print("   omnibus row: %s" % (RAW["ttui"],))
print("   spk ttui = %s" % SPK.get("ttui", 0))
for w in ALL:
    if re.search(r"ttu", w) and len(w) <= 10:
        print("   %-16s %-34s spk %s" % (w, (OMNI.get(w) or "-")[:34], SPK.get(w, 0)))

print("\n== 3. the adhere hunt: his own gloss words, then the agil root ==")
for terms in [("\u8cbc\u8fd1", "\u8cbc\u5728", "\u63a5\u5408", "\u9ecf\u624b",
               "\u7dca\u8cbc", "\u4f9d\u9644", "\u9760")]:
    seen = set()
    for w, g, _ in ROWS:
        if w and g and any(z in g for z in terms) and w.lower() not in seen:
            seen.add(w.lower())
            print("   %-18s %-36s spk %s" % (w, g[:36], SPK.get(w.lower(), 0)))
            if len(seen) >= 20:
                print("   ...")
                break
    if not seen:
        print("   (nothing for %s)" % "/".join(terms))
print("   -- the agil root, bare-ish forms --")
for w in ALL:
    if re.match(r"^(m|p|s|)?(n)?e?agil", w):
        print("   %-18s %-36s spk %s" % (w, (OMNI.get(w) or "-")[:36], SPK.get(w, 0)))
print("   -- what the map already does with his s'lut / sl'd keys --")
for k in sorted(MAP):
    if re.search(r"s'?l[ru][td]|sl'd", k):
        print("   %-14s -> %-14s omni %-26s spk %s"
              % (k, MAP[k], (OMNI.get(MAP[k]) or "-")[:26], SPK.get(MAP[k], 0)))
