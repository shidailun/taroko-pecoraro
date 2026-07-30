"""What the corpus says about each -ao residue slot. One query per family.

Word-final -ao is 1 type in 38,687 (dhdahao, 2 tokens) -- so every identity claim
keeping it is asserting a shape the orthography does not write. That does NOT tell
us the value; the family does. Each block below prints the modern family his card
points at, plus his own keys on that card, so the answer is read off a paradigm
rather than off the ending.
"""
import io, sys, json, pickle, re
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
OMNI = {}
for w, g, _ in ROWS:
    if w:
        OMNI.setdefault(w.lower(), g)
ALL = sorted(set(OMNI) | set(SPK))


def shape(label, pat):
    print("\n-- %s  /%s/ --" % (label, pat))
    r = re.compile(pat)
    n = 0
    for w in ALL:
        if r.search(w):
            print("   %-16s %-38s spk %s"
                  % (w, (OMNI.get(w) or "-")[:38], SPK.get(w, 0)))
            n += 1
            if n > 24:
                print("   ...")
                break
    if not n:
        print("   (nothing)")


def gloss(label, *zh):
    print("\n-- %s  gloss %s --" % (label, "/".join(zh)))
    seen = set()
    for w, g, _ in ROWS:
        if not w or not g or any(c not in g for c in ()) :
            pass
        if w and g and any(z in g for z in zh) and w.lower() not in seen:
            seen.add(w.lower())
            print("   %-16s %-38s spk %s" % (w, g[:38], SPK.get(w.lower(), 0)))
            if len(seen) > 22:
                print("   ...")
                break


shape("LB'NAO 嬌弱: the rbnaw family", r"rbnaw|rbnaa|brnaw")
gloss("LB'NAO by gloss", "嬌", "柔嫩", "撒嬌")

shape("BUBAO 劈開: bbag / bgbag / bubaw", r"^b.?bag|bubaw|^bbag")
gloss("BUBAO by gloss", "劈開", "剝開", "裂開")

shape("KSOLOÇ 洗網: sinaw / sminaw", r"sinaw|sminaw|ssino")
gloss("KSOLOÇ by gloss", "洗")

shape("KALIP 頭髮亂: rudaw / mrudaw / mdrudu", r"rudaw|drudu[^a]|mdrud")
gloss("KALIP by gloss", "亂蓬", "蓬鬆", "凌亂")

shape("QL'XAO 涉水: kraaw / qlhaw / qrhaw", r"kraaw|qlhaw|qrhaw|rhaw$|raaw")
gloss("QL'XAO by gloss", "涉水", "渡河", "過溪", "過河")

shape("SAPOX 藥: pspuhan / spuhan / puhan", r"spuha|^puhan|smapuh")
