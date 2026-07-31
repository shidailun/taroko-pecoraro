"""Batch 72 pre-flight -- the unexamined tail of the depth-3 rewrite sweep.

  mpiaka   empika 一跛一跛 / maapika 成了跛腳. Read HIS headword, not the
           example gloss the sweep printed.
  mp'alex  empealax. His 你幾乎都不到我們家露面了 reads like "you have given up
           on us" -- alax 放棄 is the obvious root and modern keeps the x.
  pausa    "我將派遣／寄送" under the PA card. p+usa = cause to go = send.
  damu     his card says 詞根 LAMU 之變體, so check the LAMU root, not damu.
  esa      his card says 參見 PESA. Read PESA.
  n'loq    戳破屋頂. Search the piercing glosses.
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
CARD = {}
for ent in E:
    hw = ent.get("hw") or ""
    CARD[key(hw)] = ent
    slots = [(ent.get("hw"), ent.get("zh"), "hw")]
    slots += [(x.get("t"), x.get("zh"), "ex") for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        slots += [(s.get("form"), s.get("zh") or ent.get("zh"), "sub")]
        slots += [(x.get("t"), x.get("zh"), "ex") for x in s.get("examples", [])]
    for f, g, kind in slots:
        for w in TOK.findall(f or ""):
            his[key(w)].append((hw, kind, f, g))


def full(tok, n=8):
    print("### %-12s -> %-13s %-3s  (%d slots)"
          % (tok, MAP.get(tok) or "-- GREEN --", TIER.get(tok, ""), len(his.get(tok, ()))))
    for hw, kind, f, g in his.get(tok, [])[:n]:
        print("    [%s] %-4s %s" % (hw[:12], kind, (f or "")[:76]))
        print("                %s" % (g or "")[:76])


def card(hw):
    """His whole card -- headword gloss included, which the sweep does not print."""
    ent = CARD.get(key(hw))
    if not ent:
        print("### card %s -- NOT A HEADWORD" % hw)
        return
    print("### CARD %s   %s" % (ent.get("hw"), (ent.get("zh") or "")[:66]))
    for x in ent.get("examples", [])[:3]:
        print("      ex  %s" % (x.get("t") or "")[:72])
        print("          %s" % (x.get("zh") or "")[:72])
    for s in ent.get("subs", [])[:6]:
        print("      sub %-14s %s" % (s.get("form"), (s.get("zh") or "")[:56]))


def om(pat, note="", n=12):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI if rx.search(w)), reverse=True)
    print("--- omnibus /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:n]:
        print("    %-14s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:50]))


def gl(pat, note="", n=12):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI
                  if any(rx.search(g) for g in OMNI[w])), reverse=True)
    print("--- gloss /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:n]:
        print("    %-14s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:50]))


def sibs(pat, note=""):
    rx = re.compile(pat)
    print("--- HIS tokens /%s/ %s" % (pat, note))
    for t in sorted(his, key=lambda t: -len(his[t])):
        if rx.search(t):
            print("    %-14s %2dx -> %-13s %s"
                  % (t, len(his[t]), MAP.get(t) or "GREEN", TIER.get(t, "")))


print("======== MPIAKA -- lame?")
card("KLUULUS")
full("mpiaka")
sibs(r"piaka|pika", "his pika shapes")
om(r"^empika$|^mapika$|^maapika$|^pika$|^mpika$", "the limp root")
gl(r"\u8ddb|\u9a45\u6563|\u8b8a\u672c\u52a0\u5389", "glosses 跛/驅散")

print("\n======== MP'ALEX -- to give up on")
full("mp'alex")
sibs(r"alex|alax|'alex", "his alax shapes")
om(r"^alax$|^mealax$|^empealax$|^malax$|^pealax$", "the give-up root")
gl(r"^\u653e\u68c4|\u96e2\u68c4|\u9b27\u5f46\u626d", "glosses 放棄/離棄")

print("\n======== PAUSA -- I will send")
card("PA")
full("pausa")
sibs(r"pausa|peusa|pusa|^usa", "his usa shapes")
om(r"^peusa$|^pusa$|^empeusa$|^pusai$|^pusan$", "the send root")
gl(r"\u6d3e\u9063|\u5bc4\u9001|\u4f7f\u2026\u53bb|\u8b93\u2026\u53bb", "glosses 派遣/寄送")

print("\n======== DAMU -- variant of the root LAMU?")
card("DAMU")
card("LAMU")
sibs(r"^damu|^lamu|^dyamu", "his damu/lamu shapes")
om(r"^ramu$|^rmamu$|^lamu$|^jyamu$|^dyamu$", "the LAMU root")

print("\n======== ESA -- see PESA")
card("ESA")
card("PESA")
full("esa")
om(r"^eusa$|^usa$|^peusa$|^esa$", "the go root")

print("\n======== N'LOQ -- pierced the roof")
card("L'NGO")
full("n'loq")
sibs(r"n'lo|nloq|l'ngo", "his n'lo shapes")
gl(r"\u6233|\u7a7f\u6d1e|\u925...", "glosses 戳/穿洞")
gl(r"\u6233\u7834|\u7a7f\u5b54|\u6253\u6d1e", "glosses 戳破/穿孔/打洞")
