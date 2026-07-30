"""The tail of the gloss-first sweep: ten greens that name a thing or an action.

  x'li/xm'li  倒入（液體、穀粒、沙子）  -- hmrig 倒出來 spk 3, a dropped final g
  tnoxol      猛烈暴風雨               -- nuhur 豪雨, and his OTHER spelling nuxul
                                          already ships as nuhur
  supyex      大鍋－大煮鍋
  sdongan     架子
  ssiban      吸吮－舔食
  xubao       割－撕裂（用不鋒利的工具）
  nilao       菇類（牛舌菌）
  pusyaq      眼屎
  tyapan      陶土鍋
  t'lap/tlap  太魯閣族的頭帶

Each printed with every slot it fills and the modern family around it, because a
value has to serve the whole card and a root has to be attested rather than
well formed.
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
    slots = [(ent.get("hw"), ent.get("zh"), "hw"),
             (ent.get("paradigm"), ent.get("zh"), "par")]
    slots += [(x.get("t"), x.get("zh"), "ex") for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        slots += [(s.get("form"), s.get("zh") or ent.get("zh"), "sub")]
        slots += [(x.get("t"), x.get("zh"), "ex") for x in s.get("examples", [])]
    for f, g, kind in slots:
        for w in TOK.findall(f or ""):
            his[key(w)].append((hw, kind, f, g))


def show(tok):
    v = MAP.get(tok)
    print("### %-12s -> %-13s %-3s %s"
          % (tok, v or "-- GREEN --", TIER.get(tok, ""),
             " | ".join(dict.fromkeys(OMNI.get((v or "").lower()) or []))[:38] if v else ""))
    for hw, kind, f, g in his.get(tok, [])[:6]:
        print("    [%-12s] %-4s %-38s %s" % (hw[:12], kind, (f or "")[:38], (g or "")[:46]))
    if not his.get(tok):
        print("    (not a token of his)")


def om(pat, note=""):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI if rx.search(w)), reverse=True)
    print("--- omnibus /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:13]:
        print("    %-13s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:50]))


def gl(pat, note=""):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI
                  if any(rx.search(g) for g in OMNI[w])), reverse=True)
    print("--- gloss /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:13]:
        print("    %-13s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:50]))


print("======== X'LI -- pour in")
for t in ("x'li", "xm'li", "xli", "px'li"):
    show(t)
om(r"hrig|hmrig|hrgan", "the pouring root")

print("\n======== TNOXOL -- the sudden storm; nuxul already ships as nuhur")
for t in ("tnoxol", "mtnoxol", "nuxul", "noxol"):
    show(t)
om(r"nuhur|tnuhur|nhur", "the storm root")

print("\n======== SUPYEX -- big cooking pot")
show("supyex")
om(r"supi|sup[iy]h|liwas", "pot shapes")
gl(r"\u9505", "glosses containing 鍋")

print("\n======== SDONGAN -- shelf/rack")
show("sdongan")
om(r"sdung|sdngan|paga", "rack shapes")
gl(r"\u67b6\u5b50", "glosses containing 架子")

print("\n======== SSIBAN -- to suck / lick")
for t in ("ssiban", "smiban", "siban"):
    show(t)
om(r"sibus|smib|hmup|smpu", "suck shapes")
gl(r"\u5438\u5410|\u5438\u98df|\u8202", "glosses 吸/舔")

print("\n======== XUBAO -- to slash with a blunt tool")
for t in ("xubao", "xnubao"):
    show(t)
om(r"hubaw|hbaw|hbagan", "slash shapes")
gl(r"\u6495\u88c2|\u6293\u50b7", "glosses 撕裂/抓傷")

print("\n======== NILAO -- fungus")
show("nilao")
gl(r"\u83c7|\u8611", "glosses 菇/蘑")

print("\n======== PUSYAQ -- eye discharge")
show("pusyaq")
gl(r"\u773c\u5c4e|\u773c\u57a2", "glosses 眼屎")

print("\n======== TYAPAN -- clay pot")
show("tyapan")
gl(r"\u9676|\u58fa", "glosses 陶/壺")

print("\n======== T'LAP -- the Truku headband")
for t in ("t'lap", "tlap"):
    show(t)
gl(r"\u982d\u5e36|\u984d\u5e36", "glosses 頭帶/額帶")
