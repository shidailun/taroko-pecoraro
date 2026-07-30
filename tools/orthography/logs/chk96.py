"""Batch 69 pre-flight: the four survivors of the rule-driven sweep.

All four are reachable from his spelling by rules already established and
human-checked, and all four land on an ATTESTED modern word rather than near one:

  kinal   -> kingal 一 spk 1626   his n for their ng -- the batch 68 rule
  tloon   -> tluung 坐 spk 125    his oo for their uu
  qaban   -> qabang spk 43        dropped final velar -- the x'li>hrig class
  dmtabu  -> dmtabug 餵養的人(複數) dropped final velar again

Printed with every slot each token fills and the whole card around it, because a
value has to serve the card and not only the sentence that turned it up. The
sentence is the check that matters here: each of these four sits in a Chinese
gloss that names the modern word's meaning outright.
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
    print("### %-12s -> %-13s %-3s spk %-5s %s"
          % (tok, v or "-- GREEN --", TIER.get(tok, ""),
             SPK.get((v or "").lower(), 0) if v else "",
             " | ".join(dict.fromkeys(OMNI.get((v or "").lower()) or []))[:36] if v else ""))
    for hw, kind, f, g in his.get(tok, [])[:8]:
        print("    [%-11s] %-4s %-42s %s" % (hw[:11], kind, (f or "")[:42], (g or "")[:44]))
    if not his.get(tok):
        print("    (not a token of his)")


def om(pat, note=""):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI if rx.search(w)), reverse=True)
    print("--- omnibus /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:12]:
        print("    %-14s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:50]))


def sibs(tok):
    """What his own card already ships for the tokens beside this one."""
    for hw, kind, f, g in his.get(tok, [])[:1]:
        print("    -- card %s ships:" % hw)
        for ent in E:
            if (ent.get("hw") or "") != hw:
                continue
            seen = set()
            for f2 in ([ent.get("hw")] + [s.get("form") for s in ent.get("subs", [])]
                       + [x.get("t") for x in ent.get("examples", [])]):
                for w in TOK.findall(f2 or ""):
                    k = key(w)
                    if k in seen:
                        continue
                    seen.add(k)
                    print("        %-13s -> %-13s %s" % (k, MAP.get(k, "GREEN"), TIER.get(k, "")))


print("======== KINAL -- 一, his n for their ng")
show("kinal")
om(r"^kingal$|^kigal|^kinal$", "the numeral one")
print("    how his OTHER spellings of one are handled:")
for t in ("kingal", "kngal", "kigal"):
    show(t)

print("\n======== TLOON -- 坐")
show("tloon")
om(r"^tluung|^tlung|^tluun", "the sitting root")
sibs("tloon")

print("\n======== QABAN -- 被子")
show("qaban")
om(r"^qabang|^qaban$", "blanket")

print("\n======== DMTABU -- 餵養的人")
show("dmtabu")
om(r"^dmtabug|^tabug|^tmabug|^mtabug", "the feeding root")

print("\n======== GLAQON -- the false positive, recorded")
show("glaqon")
om(r"^glaq|^gmlaq", "snatch vs pheasant")

print("\n======== EKO / KO -- is his 1sg already handled")
for t in ("eko", "ko", "'mu", "mu"):
    show(t)
