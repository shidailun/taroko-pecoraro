"""Batch 68 pre-flight. Five questions, each of which can kill its candidate.

  x'li / xm'li   is hmrig attested as the bare actor-focus form, and does his card
                 read as one root doing 倒入 and 倒出?
  xubao / xnubao his pair looks like the modern hbag- / hnbag- pair exactly, but
                 the bare root may not be attested -- only the -an/-un/-i forms.
  nilao          ngiraw 香菇 spk 6 fits his description (cultivated, on tree
                 trunks) but he writes ng in 15 other headwords, so he would have
                 written NGILAO. Meanwhile a modern nilaw root DOES exist (qnilaw
                 煮爛的食物, 豬食) -- wrong meaning. Read his card before deciding.
  pusyaq         bare pusiq is attested but glossed 人名; the 眼屎 sense lives only
                 in mnspusiq and mnegpusiq. Does his card need the bare form?
  nuxul/tnoxol   nuxul ships nuhur 豪雨 and his only slot is 穿暖和一點. The uxul
                 warmth family is right there at spk 40. What else on that card
                 and on TNOXOL is already brown, and would fall with it?
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
MARKS = "['\u2019\u02bc\"\u0294]"
SMALL = {"x": "h", "o": "u", "l": "r"}


def key(w):
    return re.sub(MARKS, "'", w).replace("\u0142", "l").lower()


def cr(w):
    w = re.sub(MARKS, "", w).replace("\u0142", "l")
    w = re.sub(r"a[oO]$", "aw", w)
    return "".join(SMALL.get(c, c) for c in w)


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
    print("### %-12s -> %-13s %-3s spk %-4s %s"
          % (tok, v or "GREEN prints " + cr(tok).upper(), TIER.get(tok, ""),
             SPK.get((v or "").lower(), 0) if v else "",
             " | ".join(dict.fromkeys(OMNI.get((v or "").lower()) or []))[:38] if v else ""))
    for hw, kind, f, g in his.get(tok, [])[:7]:
        print("    [%-11s] %-4s %-40s %s" % (hw[:11], kind, (f or "")[:40], (g or "")[:44]))
    if not his.get(tok):
        print("    (not a token of his)")


def card(name):
    """Every key on a card, with its shipped value -- what would fall together."""
    for ent in E:
        if (ent.get("hw") or "").upper() != name.upper():
            continue
        print("--- CARD %s   %s" % (ent.get("hw"), (ent.get("zh") or "")[:60]))
        forms = [(ent.get("hw"), "hw", ent.get("zh"))]
        forms += [(s.get("form"), "sub", s.get("zh")) for s in ent.get("subs", [])]
        for f, kind, g in forms:
            if not f:
                continue
            print("    %-4s %-26s %s" % (kind, f[:26], (g or "")[:44]))
            for w in TOK.findall(f):
                k = key(w)
                print("         %-13s -> %-13s %s" % (k, MAP.get(k, "GREEN " + cr(k).upper()),
                                                      TIER.get(k, "")))
        for x in ent.get("examples", []):
            print("    ex   %-40s %s" % ((x.get("t") or "")[:40], (x.get("zh") or "")[:42]))
        for s in ent.get("subs", []):
            for x in s.get("examples", []) or []:
                print("    sex  %-40s %s" % ((x.get("t") or "")[:40], (x.get("zh") or "")[:42]))


def om(pat, note=""):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI if rx.search(w)), reverse=True)
    print("--- omnibus /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:15]:
        print("    %-13s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:50]))


print("======== X'LI")
card("X'LI")
for t in ("x'li", "xm'li"):
    show(t)
om(r"^hmrig|^hrig$|^phrig|^hrgan", "the bare pouring forms")

print("\n======== XUBAO")
card("XUBAO")
for t in ("xubao", "xnubao"):
    show(t)
om(r"^hbag|^hmbag|^hbg|^hnbag", "is any bare hbag form attested")

print("\n======== NILAO")
card("NILAO")
show("nilao")
om(r"^ngiraw|^nilaw|^riwa", "fungus vs pig-feed")

print("\n======== PUSYAQ")
card("PUSYAQ")

print("\n======== NUXUL / TNOXOL -- the storm that is really warmth")
for t in ("nuxul", "tnoxol", "mtnoxol", "noxol", "uxul", "muxul"):
    show(t)
om(r"uxul|^xul", "the warmth root")
