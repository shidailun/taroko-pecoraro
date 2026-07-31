"""Last checks before batch 70.

NTA is the one worth the most and the one pass 2 got wrong. nita 我們的 is a
genitive; his NTA card says 邀請前往 and every one of his twenty sentences is a
hortative -- Nta da! 走吧, Nta sapax da 我們回家吧, Nta mita da 我們去看看吧. He
also uses nita separately, and it already ships nita. So the question is not
whether nita is a word but whether the modern dictionary has a hortative particle,
which is a different search: look for 吧 / 走吧 / 我們去 in the glosses.

SYULING is the same shape of error in reverse. His headword says ??（意義不明）,
which reads as no gloss to check against -- but his own example, Syuling otoç, is
glossed 皮癬－濕疹－蕁麻疹. There IS a meaning; it is a skin disease, and siling 問
is not it.

Also: the spk figures for the landings that the omnibus has no entry for, since
those came from spoken_truku.json and I have been printing them second-hand.
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


def full(tok, n=6):
    """Untruncated forms -- sqoaqe's sentence was cut off exactly where it mattered."""
    print("### %-12s -> %-12s %-3s  (%d slots)"
          % (tok, MAP.get(tok) or "-- GREEN --", TIER.get(tok, ""), len(his.get(tok, ()))))
    for hw, kind, f, g in his.get(tok, [])[:n]:
        print("    [%s] %s" % (hw[:12], kind))
        print("        %s" % (f or ""))
        print("        %s" % (g or ""))


def gl(pat, note="", n=16):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI
                  if any(rx.search(g) for g in OMNI[w])), reverse=True)
    print("--- gloss /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:n]:
        print("    %-14s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:52]))


print("======== the landings the omnibus does not gloss: are they really spoken?")
for w in ("srngaw", "endwai", "dmtgsa", "singbung", "kiisug", "kiisog", "tmeego",
          "mtmeego", "pseanak", "pneanak", "peanak", "phpah", "tqrian", "cipiq",
          "qilug", "nita", "lita", "trapi", "trak"):
    print("    %-12s spk %-6s omnibus: %s"
          % (w, SPK.get(w, "-"), " | ".join(dict.fromkeys(OMNI.get(w, ["(no entry)"])))[:46]))

print("\n======== NTA -- is there a modern hortative?")
gl(r"\u5427$|\u8d70\u5427|\u6211\u5011\u53bb|\u4f86\u5427|\u9080\u8acb", "glosses 吧/走吧/我們去/來吧/邀請")
print("--- his LITA and NTA neighbours")
for t in ("lita", "nta", "nita", "ita", "ta"):
    print("    his %-8s %3dx -> %-12s %s"
          % (t, len(his.get(t, ())), MAP.get(t) or "GREEN", TIER.get(t, "")))

print("\n======== SYULING -- a skin disease, not a question")
full("syuling")
gl(r"\u7663|\u6fd5\u75b9|\u8354\u9ebb\u75b9|\u75b9", "glosses 癬/濕疹/蕁麻疹/疹")

print("\n======== SQOAQE -- the full sentence")
full("sqoaqe")
full("nlut")

print("\n======== PAAANAK -- the third -anak green")
full("paaanak")

print("\n======== TEPYAQ vs TIPYAQ -- one word or two?")
full("tepyaq", 4)
