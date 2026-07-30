"""Last two questions before batch 62.

A. S'LUT. chk65's adhere sweep threw up one word that fits his THREE examples --
   a chicken coop too close to the kitchen, a house stuck onto a cliff, a bathroom
   joined to the main house -- better than anything in the 黏液 slime family:
   smdlut 依靠著 "leaning against". That is sm- on a root dlut, and his own
   headword line already confesses he does not know his root: "S'LUT (= R. ? -
   R. = LUT ?)". So: the entire dlut root, both corpora, with glosses. If it is
   an adhesion/abutment root the three wrong browns on that card have an answer;
   if it is one isolated spk-0 form, they do not and this is a null.

B. T"TO. I need to know WHICH of the cut-stem forms are actually green keys in
   his text before writing values for them, and what each one's count and card is
   -- ttui is the one that matters most, because his imperative "Ttui xei lodoç"
   你把雞（肉）切開 and modern ttui 切、剁 are the same word, same slot, same gloss.
"""
import io, sys, json, pickle, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
OMNI = {}
for w, g, _ in ROWS:
    if w:
        OMNI.setdefault(w.lower(), g)
ALL = sorted(set(OMNI) | set(SPK))
GREEN = json.load(io.open("green_work.json", encoding="utf-8"))
e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


print("== A. the dlut root, everything ==")
n = 0
for w in ALL:
    if re.search(r"dlut|dlud", w):
        print("   %-18s %-36s spk %s" % (w, (OMNI.get(w) or "-")[:36], SPK.get(w, 0)))
        n += 1
print("   (%d forms)" % n)
print("   -- and every modern word glossed 依靠/靠近/緊貼/黏著 --")
seen = set()
for w, g, _ in ROWS:
    if w and g and re.search(r"^\u4f9d\u9760$|\u9760\u8fd1|\u7dca\u8cbc|\u9ecf\u8457", g) \
            and w.lower() not in seen:
        seen.add(w.lower())
        print("   %-18s %-36s spk %s" % (w, g[:36], SPK.get(w.lower(), 0)))

print("\n== B. the cut stem: which of his forms are green, where, how often ==")
want = {"ttui", "ttuun", "ttuon", "t'tuan", "tn'tuan", "t'ntuan", "sttuan",
        "sttuun", "ttuan", "tm'to", "t'to", "tma'to"}
for ent in E:
    hw = ent.get("hw") or ""
    slots = [(ent.get("hw"), ent.get("zh")), (ent.get("paradigm"), ent.get("zh"))]
    slots += [(x.get("t"), x.get("zh")) for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        slots += [(s.get("form"), s.get("zh")), (s.get("paradigm"), s.get("zh"))]
        slots += [(x.get("t"), x.get("zh")) for x in s.get("examples", [])]
    for f, g in slots:
        for w in TOK.findall(f or ""):
            k = key(w)
            if k in want:
                st = ("GREEN x%-2d" % GREEN.get(k, 0)) if k in GREEN \
                    else ("brown ->%s" % MAP.get(k, "?"))
                print("   %-10s %-12s [%-10s] %-42s %s"
                      % (k, st, hw[:10], (f or "")[:42], (g or "")[:26]))
                want.discard(k)
print("   never seen: %s" % sorted(want))

print("\n== C. every value I mean to write, priced ==")
for v in ("sakur", "psakur", "msakur", "spsakur", "msqsiya", "ttui", "ttuan",
          "ttuun", "sttuan", "knttuun"):
    used = [k for k in MAP if MAP[k] == v]
    print("   %-10s omni %-24s spk %-4s already the value of: %s"
          % (v, (OMNI.get(v) or "-")[:24], SPK.get(v, 0), used or "-"))
