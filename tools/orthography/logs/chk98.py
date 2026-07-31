"""Batch 70 pre-flight: what the derived-rule pass turned up.

  p'pax    phpah 花 spk 198. His slot is a sentence about watering the flowers
           we planted. ' -> h and x -> h are both established; phpah is the
           commonest flower word in the modern dictionary. p'pax has sat on the
           hold list for a long time.
  psaanak  pseanak 偏見 spk 16 against his 擱置一旁－歧視、隔離. His aa for their
           ea, and PNAANAK on another card gives pneanak by the same rule -- a
           self-consistent pair, which is the signature that has been right
           before (pax/pnax, loan/lowan).
  qelo     qilug 後腦 spk 4 against his 後頸、頸背. Check whether the modern
           dictionary has a nearer word for the nape before taking 後腦.
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
CARD = collections.defaultdict(set)
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
            CARD[key(w)].add(hw)


def show(tok):
    v = MAP.get(tok)
    print("### %-12s -> %-13s %-3s   cards: %s"
          % (tok, v or "-- GREEN --", TIER.get(tok, ""), sorted(CARD.get(tok, ()))[:6]))
    for hw, kind, f, g in his.get(tok, [])[:8]:
        print("    [%-11s] %-4s %-40s %s" % (hw[:11], kind, (f or "")[:40], (g or "")[:46]))
    if not his.get(tok):
        print("    (not a token of his)")


def om(pat, note=""):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI if rx.search(w)), reverse=True)
    print("--- omnibus /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:14]:
        print("    %-14s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:52]))


def gl(pat, note=""):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI
                  if any(rx.search(g) for g in OMNI[w])), reverse=True)
    print("--- gloss /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:14]:
        print("    %-14s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:52]))


def sibs(pat, note=""):
    """His own tokens matching a shape, with what they ship -- the neighbour test."""
    rx = re.compile(pat)
    print("--- HIS tokens /%s/ %s" % (pat, note))
    for t in sorted(his, key=lambda t: -len(his[t])):
        if rx.search(t):
            print("    %-14s %2dx -> %-13s %s" % (t, len(his[t]), MAP.get(t) or "GREEN", TIER.get(t, "")))


print("======== P'PAX -- flowers")
for t in ("p'pax", "ppax", "pax", "pnax", "'pax"):
    show(t)
om(r"^p.?hpah$|^phpah$|^pah$|^hpah$", "the flower root")
gl(r"^\u82b1|\u6f86", "glosses 花 / 澆")

print("\n======== PSAANAK / PNAANAK -- setting apart")
for t in ("psaanak", "pnaanak", "saanak", "naanak", "anak"):
    show(t)
om(r"anak", "the alone/self root")
sibs(r"aanak|anak", "his own -anak words")

print("\n======== QELO -- nape of the neck")
show("qelo")
sibs(r"^q'?el|^qil", "his q-e-l shapes")
om(r"^qilug$|^qulu|^qelu", "head/nape")
gl(r"\u5f8c\u9838|\u9838\u80cc|\u5f8c\u8166|\u8393\u5b50", "glosses 後頸/頸背/後腦")
