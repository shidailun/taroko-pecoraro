"""Batch 72 pre-flight, second pass. The sweep's top landing was wrong twice
here, and both times the CARD said so:

  mpiaka  the sweep offered empika 一跛一跛. But his sentence glosses it
          多少次 -- how many TIMES -- so this is the piya 幾/多少 family, not
          the limping one. Check piya.
  mp'alex his own alex>alix (A), m'alex>malix (M), p'alex>pealix (M) settle the
          stem; only the em- shape is in question.
  pausa   his PA card is explicit: Pusa ko 我派遣 -> Pausa ko 我將派遣. So the
          question is what his MAUSA (=musa + future) already ships.
  esa     root of PESA 請求－乞求. Search the begging glosses.
  n'loq   戳破屋頂. His n'lo>nru, gnloq>gnluq, pnloqex>pnluqih already ship.
  damu    variant of the root LAMU 收集－逐一撿拾.
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
    print("### %-12s -> %-13s %-3s  (%d slots)"
          % (tok, MAP.get(tok) or "-- GREEN --", TIER.get(tok, ""), len(his.get(tok, ()))))
    for hw, kind, f, g in his.get(tok, [])[:n]:
        print("    [%s] %-4s %s" % (hw[:12], kind, (f or "")[:76]))
        print("                %s" % (g or "")[:76])


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


print("======== MPIAKA -- 'no matter how many times', not 'limping'")
sibs(r"^piya|^mpiya|^piaka|^piax", "his piya shapes")
om(r"^piya$|^mpiya|^piyax|^piyaka|^empiya", "the how-many root")
gl(r"\u591a\u5c11|\u5e7e\u6b21|\u5e7e\u500b", "glosses 多少/幾次/幾個")

print("\n======== MP'ALEX -- em- + pealix")
om(r"^empealix|^mpealix|^pealix|^alix|^malix", "the alix set")
gl(r"\u9b27\u5f46\u626d|\u92b7\u8072\u533f\u8de1|\u4e0d\u4f86\u5f80", "glosses 鬧彆扭")

print("\n======== PAUSA -- the future of pusa")
sibs(r"^mausa|^musa|^mpusa|^pausa|^pusa", "his musa/pusa shapes")
om(r"^empusa|^musa$|^empeusa|^mausa", "the go/send future")

print("\n======== ESA / PESA -- to beg, to request")
sibs(r"^esa$|^pesa|^mesa|^mpesa|^pngsa|^kmpesa", "his pesa shapes")
om(r"^mgspung|^pgspung|^spung", "spung?")
gl(r"\u8acb\u6c42|\u4e5e\u6c42|\u4e5e\u8a0e|\u8981\u6c42", "glosses 請求/乞求/乞討/要求")

print("\n======== N'LOQ -- pierced the roof")
sibs(r"loq|luq", "his -loq shapes")
gl(r"\u6233|\u7a7f\u6d1e|\u6253\u6d1e|\u7834\u6d1e|\u523a", "glosses 戳/穿洞/刺")

print("\n======== DAMU -- variant of LAMU 收集")
sibs(r"^damu|^lamu|^dmamu|^lmamu|^dyamu", "his damu/lamu shapes")
om(r"^ramu|^rmamu|^lamu|^lmamu|^jyamu", "the gather root")
gl(r"\u64bf\u62fe|\u6536\u96c6|\u62fe\u7a57|\u4e00\u4e00\u64bf", "glosses 撿拾/收集/拾穗")
