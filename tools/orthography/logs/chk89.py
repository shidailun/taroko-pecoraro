"""The gloss-first sweep's four candidates, checked against their whole card.

  sl'dan  [S'LUT]  黏附；被黏合之物   -- sltan 被黏著 spk 2, two edits
  bsqlol  [BSQLOL] 在鍋裡燒焦的食物   -- sqrul 燒焦, psqrlan 使...燒焦
  psqexon [PSQEXON] 被人強迫、被人強制 -- pskixan 強迫 spk 3, pskyxay 讓…強制
  swatan  [KMPOLING] the Truku name for the Bunun

Each needs the same three things before it can be written: what the rest of his
card spells (a value has to serve every slot, not the one that turned up), what
the modern root actually is (so the value is that root's real form and not a
well-formed guess), and whether the string is a homograph of something else of his.
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
    hit = [(SPK.get(w, 0), w) for w in OMNI if rx.search(w)]
    hit.sort(reverse=True)
    print("--- omnibus /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:14]:
        print("    %-14s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:56]))


def gl(pat, note=""):
    rx = re.compile(pat)
    hit = [(SPK.get(w, 0), w) for w in OMNI
           if any(rx.search(g) for g in OMNI[w])]
    hit.sort(reverse=True)
    print("--- gloss /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:14]:
        print("    %-14s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:56]))


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("['\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


back = collections.defaultdict(set)
for ent in E:
    for f in [ent.get("hw"), ent.get("paradigm")] + \
             [x.get("t") for x in ent.get("examples", [])] + \
             [s.get("form") for s in ent.get("subs", [])] + \
             [x.get("t") for s in ent.get("subs", []) for x in s.get("examples", [])]:
        for w in TOK.findall(f or ""):
            back[key(w)].add(ent.get("hw") or "")


def card(hw):
    for ent in E:
        if (ent.get("hw") or "").upper() != hw:
            continue
        print("=== CARD %s   %s" % (ent.get("hw"), (ent.get("zh") or "")[:64]))
        if ent.get("paradigm"):
            print("    par  %s" % ent["paradigm"])
        for x in ent.get("examples", []):
            print("    ex   %-42s %s" % ((x.get("t") or "")[:42], (x.get("zh") or "")[:44]))
        for s in ent.get("subs", []):
            print("    sub  %-42s %s" % ((s.get("form") or "")[:42], (s.get("zh") or "")[:44]))
            for x in s.get("examples", []):
                print("      ex %-40s %s" % ((x.get("t") or "")[:40], (x.get("zh") or "")[:44]))
        for w in sorted({key(w) for f in [ent.get("hw"), ent.get("paradigm")] +
                         [s.get("form") for s in ent.get("subs", [])]
                         for w in TOK.findall(f or "")}):
            v = MAP.get(w)
            print("    KEY  %-14s %-14s %-3s %s"
                  % (w, v or "-- GREEN --", TIER.get(w, ""),
                     (" | ".join(dict.fromkeys(OMNI.get((v or "").lower()) or []))[:40]
                      if v else ""))
                  + ("   <= his %s" % sorted(back[w])[:4] if len(back[w]) > 1 else ""))
        print()


print("################ 1. SL'DAN -- the sticking card")
card("S'LUT")
om(r"^s.?l.?[td]", "s-l-t/d shapes")
gl(r"\u9ecf", "glosses containing 黏")

print("################ 2. BSQLOL -- burnt food in the pot")
card("BSQLOL")
om(r"sqr[uw]l|sqlul|bsq", "burnt shapes")
gl(r"\u71d2\u7126", "glosses containing 燒焦")

print("################ 3. PSQEXON -- forced")
card("PSQEXON")
om(r"psk?[iy]x|sqix|kyx", "force shapes")
gl(r"\u5f37\u8feb|\u5f37\u5236", "glosses 強迫/強制")

print("################ 4. SWATAN -- the Bunun")
for hw in ("KMPOLING",):
    card(hw)
gl(r"\u5e03\u8fb2", "glosses containing 布農")
om(r"^s.?wa|swat|sbut", "swatan shapes")
