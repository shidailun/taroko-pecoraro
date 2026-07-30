"""The gloss-first sweep's second wave: things with names.

A gloss like 詞根 or 動詞 is his own metalanguage and matches the omnibus'
metalanguage, which is why the singleton list is mostly noise. What is left is the
rows where his gloss NAMES something -- 瓶子, 帳篷, 發霉, 花苞, 犬齒, 公開 -- and a
name is exactly what a dictionary can be asked for.

  luula   公開地－公然地   -- ura 公開、清白; and his ntluula ALREADY ships as ntreura
  dobut   瓶子
  koobu   帳篷
  kmupan  發霉的－腐壞的
  moxong  （植物的）芽、花苞  -- and snwakat 長出插枝（嫩芽）, waqat -> waqit 芽 spk 8
  kluxeng 為了美觀而刻意敲斷犬齒
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


def om(pat, note=""):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI if rx.search(w)), reverse=True)
    print("--- omnibus /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:12]:
        print("    %-14s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:54]))


def gl(pat, note=""):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI
                  if any(rx.search(g) for g in OMNI[w])), reverse=True)
    print("--- gloss /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:12]:
        print("    %-14s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:54]))


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("['\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


back = collections.defaultdict(set)
for ent in E:
    for f in [ent.get("hw"), ent.get("paradigm")] + \
             [s.get("form") for s in ent.get("subs", [])]:
        for w in TOK.findall(f or ""):
            back[key(w)].add(ent.get("hw") or "")


def card(hw):
    seen = False
    for ent in E:
        if (ent.get("hw") or "").upper() != hw.upper():
            continue
        seen = True
        print("=== CARD %s   %s" % (ent.get("hw"), (ent.get("zh") or "")[:70]))
        if ent.get("paradigm"):
            print("    par  %s" % ent["paradigm"])
        for x in ent.get("examples", []):
            print("    ex   %-40s %s" % ((x.get("t") or "")[:40], (x.get("zh") or "")[:42]))
        for s in ent.get("subs", []):
            print("    sub  %-40s %s" % ((s.get("form") or "")[:40], (s.get("zh") or "")[:42]))
        for w in sorted({key(w) for f in [ent.get("hw"), ent.get("paradigm")] +
                         [s.get("form") for s in ent.get("subs", [])]
                         for w in TOK.findall(f or "")}):
            v = MAP.get(w)
            extra = "   <= his %s" % sorted(back[w]) if len(back[w]) > 1 else ""
            print("    KEY  %-14s %-14s %-3s %-30s%s"
                  % (w, v or "-- GREEN --", TIER.get(w, ""),
                     (" | ".join(dict.fromkeys(OMNI.get((v or "").lower()) or []))[:30]),
                     extra))
        print()
    if not seen:
        print("=== CARD %s NOT FOUND\n" % hw)


print("############ LUULA -- ntluula already ships as ntreura")
card("LUULA")
card("LUUS")
om(r"ura$|eura|ruura", "ura shapes")
gl(r"\u516c\u958b|\u516c\u7136", "glosses 公開/公然")
gl(r"\u7368\u81ea|\u55ae\u8eab|\u5b64\u55ae", "glosses 獨自/單身/孤單")

print("############ DOBUT -- bottle")
card("DOBUT")
gl(r"\u74f6", "glosses containing 瓶")
om(r"^d.?b|lung|rung", "dobut/longao shapes")

print("############ KOOBU -- tent")
card("KOOBU")
gl(r"\u5e33\u7be7|\u906e\u853d", "glosses 帳篷/遮蔽")
om(r"^k.?[uo]b", "koobu shapes")

print("############ KMUPAN -- mouldy")
card("KMUPAN")
gl(r"\u767c\u9709|\u9709", "glosses containing 霉")
om(r"kupa|qupa|kmup", "kmupan shapes")

print("############ MOXONG -- bud / sprout")
card("MOXONG")
gl(r"\u82bd|\u82b1\u82de", "glosses 芽/花苞")
om(r"muhu|mhun|huhu", "moxong shapes")

print("############ WAKAT / WAQAT -- canine tooth, and the sprout analogy")
card("WAKAT")
card("SLIYU")
gl(r"\u72ac\u9f52", "glosses containing 犬齒")
om(r"waq[ai]|wakat", "waqat shapes")

print("############ KLUXENG -- knocking the canines out")
card("KLUXENG")
om(r"kruh|kluh|qruh", "kluxeng shapes")
