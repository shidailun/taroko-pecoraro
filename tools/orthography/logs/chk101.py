"""Batch 71 pre-flight -- what the REWRITE sweep found that the per-character one
could not reach.

  nglaun    ngalun 拿來當；用來做 spk 45, against his 我要拿這塊石頭來加固房子.
            On the hold list for a long time.
  dyudika   jyujika. His gloss is 釘上十字架 and Japanese 十字架 is juujika. d>j
            is 46 in the checked pairs and is exactly the rule the per-character
            table lacked.
  lagap     ragak / rmagak 下對流雨. His LAGAP is 傾盆、連續、驟然而至、無雷雨的大雨
  lmagap    and his LMAGAP is 同上之動詞形 -- one entry, noun and verb, and the
            modern pair is the same shape under l>r and his word-final p>k.
  tnai      tngay 滿（與thngay 同義）. His sentence is 裡面連一點點空位都沒有了 --
            no space left, i.e. full. n>ng and i>y word-final, both top rules.
  qodap     qudak (風)減弱 and ptqudak 使…漸弱, against his 熄滅－終止. Word-final
  ptqodap   p>k is counted 10 times in the checked pairs and I had never used it.
  qalip     qarik. Shape yes under l>r and p>k; gloss is 毛瑟槍, his is 剪、裁.
            Search the cutting glosses before believing or refusing it.
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
    print("### %-12s -> %-12s %-3s  (%d slots)"
          % (tok, MAP.get(tok) or "-- GREEN --", TIER.get(tok, ""), len(his.get(tok, ()))))
    for hw, kind, f, g in his.get(tok, [])[:n]:
        print("    [%s] %-4s %s" % (hw[:12], kind, (f or "")[:78]))
        print("                %s" % (g or "")[:78])


def om(pat, note="", n=14):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI if rx.search(w)), reverse=True)
    print("--- omnibus /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:n]:
        print("    %-14s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:50]))


def gl(pat, note="", n=14):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI
                  if any(rx.search(g) for g in OMNI[w])), reverse=True)
    print("--- gloss /%s/ %s -> %d" % (pat, note, n and len(hit)))
    for s, w in hit[:n]:
        print("    %-14s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:50]))


def sibs(pat, note=""):
    rx = re.compile(pat)
    print("--- HIS tokens /%s/ %s" % (pat, note))
    for t in sorted(his, key=lambda t: -len(his[t])):
        if rx.search(t):
            print("    %-14s %2dx -> %-13s %s" % (t, len(his[t]), MAP.get(t) or "GREEN", TIER.get(t, "")))


print("======== NGLAUN -- take (a stone) to use")
full("nglaun")
sibs(r"ngal|nglau|angal", "his ngal- shapes")
om(r"^ngalun$|^angal$|^ngali$|^nglaun$", "the take root")

print("\n======== DYUDIKA -- the cross")
full("dyudika")
sibs(r"dyu|jyu|dika", "his dy- shapes")
om(r"jyujika|juujika|jujika|kurusu", "the loan")
gl(r"\u5341\u5b57", "glosses 十字")

print("\n======== LAGAP / LMAGAP -- torrential rain")
for t in ("lagap", "lmagap", "lgapan", "plagap"):
    full(t)
om(r"^ragak|^rmagak|^rmnagak|^ragan", "the rain root")
gl(r"\u5c0d\u6d41\u96e8|\u50be\u76c6|\u5927\u96e8", "glosses 對流雨/傾盆/大雨")

print("\n======== TNAI -- full, no space left")
full("tnai")
om(r"^tngay$|^thngay|^tnngay|^mtngay", "the full root")
gl(r"^\u6eff|\u88dd\u6eff", "glosses 滿")

print("\n======== QODAP / PTQODAP -- to go out, die down")
for t in ("qodap", "ptqodap", "tqodap", "qdapan", "kdapan"):
    full(t, 4)
om(r"^qudak|^ptqudak|^qdak|^mqudak", "the weaken root")
gl(r"\u7184\u6ec5|\u6f38\u5f31|\u6e1b\u5f31", "glosses 熄滅/漸弱/減弱")

print("\n======== QALIP -- to cut, to tailor")
full("qalip")
sibs(r"qalip|kalip|qarik", "his qalip/kalip shapes")
gl(r"^\u526a|\u88c1|\u526a\u5200", "glosses 剪/裁")
