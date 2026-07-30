"""Last checks before batch 69: the candidates the rare-character index found.

  l'xqoi   糯米. dhquy 糯米 spk 3. Under his own conventions -- apostrophe schwa,
           x>h, o>u, i>y -- his word is lhquy against their dhquy, one initial
           letter, and the sdlut/slut alternation in batch 67 showed d~l is real
           in this dictionary. 5 occurrences, the highest-value green left.
  xg'xo    泉源/水塘. hghug 水井. His xg'xo is hghu, plus the final velar he drops
           (x'li>hrig, ayo>ayug) -- an exact match under two established rules.
  tyaqong  雉雞（山雞）. Is there a modern pheasant word at all beyond glaqung
           藍腹鷴, which his G'LAQ example already refuses?
  mskoto   起雞皮疙瘩. Search 疙瘩 rather than the 麻/雞 characters, which matched
           苧麻 and 雞 and nothing useful.
  tmago    自負的－驕傲的. dahu 自誇、自傲 spk 26 -- but does tmdahu exist, which
           would be his shape with their h for his g?
  biri     最後的. hili 最小的、老么 spk 2, d=2.
  teumuk   首領. thowlang 王、領袖或頭目 spk 457, d=7 -- almost certainly no.
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


def show(tok):
    v = MAP.get(tok)
    print("### %-12s -> %-13s %-3s" % (tok, v or "-- GREEN --", TIER.get(tok, "")))
    for hw, kind, f, g in his.get(tok, [])[:7]:
        print("    [%-11s] %-4s %-42s %s" % (hw[:11], kind, (f or "")[:42], (g or "")[:44]))
    if not his.get(tok):
        print("    (not a token of his)")


def om(pat, note=""):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI if rx.search(w)), reverse=True)
    print("--- omnibus /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:12]:
        print("    %-14s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:50]))


def gl(pat, note=""):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI
                  if any(rx.search(g) for g in OMNI[w])), reverse=True)
    print("--- gloss /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:12]:
        print("    %-14s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:50]))


print("======== L'XQOI -- glutinous rice")
for t in ("l'xqoi", "lxqoi", "dxqoi"):
    show(t)
om(r"dhquy|lhquy|hquy", "the glutinous root")
gl(r"\u7cef", "glosses containing 糯")

print("\n======== XG'XO -- spring / pond")
show("xg'xo")
om(r"hghug|hghu|^hru$|qsiya", "well / water source")

print("\n======== TYAQONG -- pheasant")
show("tyaqong")
gl(r"\u96c9|\u9dc7|\u5c71\u96de", "glosses 雉/鷴/山雞")
om(r"yaqung|ciyaq|tyaq", "his shape in modern")

print("\n======== MSKOTO -- goosebumps")
show("mskoto")
gl(r"\u7599\u7629|\u9ebb\u6728|\u51cd", "glosses 疙瘩/麻木/凍")

print("\n======== TMAGO -- proud")
for t in ("tmago", "mtmago"):
    show(t)
om(r"tmdahu|dahu|tmagu", "the pride root")

print("\n======== BIRI -- the last one")
show("biri")
om(r"^hili$|^biri$|^bili", "last/youngest")

print("\n======== TEUMUK -- chief")
show("teumuk")
gl(r"\u9996\u9818|\u982d\u76ee", "glosses 首領/頭目")
