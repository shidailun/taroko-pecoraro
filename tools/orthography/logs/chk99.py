"""Batch 70 verification. The derived-rule sweep produced more candidates in one
run than the last four batches together, so every one gets the same three tests:
does the shape follow rules already shipped, does the modern word exist and get
spoken, and does HIS OWN SENTENCE say what the gloss says. glaqung passed the
first two and failed the third.

  s'lno     srngaw spk 31 -- his 報告－告知－分享. ' drop, l>r, n>ng, o>aw: four
            established rules and no residue. Wants the rngaw root confirmed.
  tqlyaan   tqrian 裝填 against his 用來裝稻穀 -- to fill a sack with grain.
  tlap      trapi 要戴頭巾 against his Truku headband tied round the head.
  kiiso     kiisug -- his sentence is 別怕, and ksug is the fear root. His o for
            their ug is the ayo>ayug rule.
  ndoai     endwai 好好的 -- his 要努力互相教導. +e initial and o>w, both derived.
  dmtgisa   dmtgsa -- his 召集所有老師, and gsa is the teaching root.
  sinbong   singbung -- his sentence pastes NEWSPAPER on the walls. Japanese
            shinbun. The modern entry has no gloss, so the loan has to be argued.
  tipyaq    cipiq 不多 against his 少－小量. t>c is 28 in the checked pairs.
  nta       nita 我們的 -- 20 slots, the biggest green in the book. Held for a
            long time because green_near matched it to 他的 on shape alone.
  qelo      qilug 後腦 against his 後頸、頸背.
  tmago     tmeego -- the shape objection that made me hold it may be answered by
            his a for their ee rather than by g>h.
  sqoaqe    sqowaq -- the quwaq mouth root, his card is about speaking.
  syuling   siling 問 -- his own card says the meaning is unknown, so there is no
            gloss to agree with. That may be disqualifying on its own.
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


def show(tok, n=8):
    v = MAP.get(tok)
    print("### %-12s -> %-13s %-3s  (%d slots)"
          % (tok, v or "-- GREEN --", TIER.get(tok, ""), len(his.get(tok, ()))))
    for hw, kind, f, g in his.get(tok, [])[:n]:
        print("    [%-11s] %-4s %-40s %s" % (hw[:11], kind, (f or "")[:40], (g or "")[:46]))
    if not his.get(tok):
        print("    (not a token of his)")


def om(pat, note="", n=14):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI if rx.search(w)), reverse=True)
    print("--- omnibus /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:n]:
        print("    %-14s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:52]))


def gl(pat, note="", n=14):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI
                  if any(rx.search(g) for g in OMNI[w])), reverse=True)
    print("--- gloss /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:n]:
        print("    %-14s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:52]))


def sibs(pat, note=""):
    rx = re.compile(pat)
    print("--- HIS tokens /%s/ %s" % (pat, note))
    for t in sorted(his, key=lambda t: -len(his[t]))[:400]:
        if rx.search(t):
            print("    %-14s %2dx -> %-13s %s" % (t, len(his[t]), MAP.get(t) or "GREEN", TIER.get(t, "")))


print("======== S'LNO -- to report / tell")
for t in ("s'lno", "sl'no", "msl'no"):
    show(t)
om(r"rngaw|srngaw|mrngaw", "the telling root")

print("\n======== TQLYAAN -- to fill a sack")
show("tqlyaan")
sibs(r"tqli|tqlya|qlya", "his tqli- shapes")
om(r"^tqri|^qri[aiu]|^mqri", "the filling root")

print("\n======== TLAP -- the headband")
for t in ("tlap", "t'lap"):
    show(t)
om(r"^trap|^tarap|^rapi$", "the headcloth root")
gl(r"\u982d\u5dfe|\u982d\u5e36|\u7e8f", "glosses 頭巾/頭帶/纏")

print("\n======== KIISO -- fear")
for t in ("kiiso", "isoka", "kiisoka", "ksoan"):
    show(t)
om(r"kiisug|^ksug|miisug|ksug", "the fear root")

print("\n======== NDOAI -- properly")
for t in ("ndoai", "ndwai", "mdoai"):
    show(t)
om(r"endwai|^dwai|mndwai|ndwai", "the do-well root")

print("\n======== DMTGISA -- the teachers")
for t in ("dmtgisa", "dmptgsa", "mtgisa"):
    show(t)
om(r"^dmtgsa|^dmptgsa|^tmgsa|^msapuh", "the teaching root")

print("\n======== SINBONG -- newspaper")
show("sinbong")
om(r"singbung|sinbun|^patas$", "the newspaper loan")
gl(r"\u5831\u7d19|\u65b0\u805e", "glosses 報紙/新聞")

print("\n======== TIPYAQ -- few / small")
for t in ("tipyaq", "stipyaq", "sptipyaq", "pntipyaq", "tepyaq"):
    show(t, 4)
om(r"^cipiq|^scipiq|^ptcipiq|^kncipiq", "the few root")

print("\n======== NTA -- our  (20 slots)")
show("nta", 14)
sibs(r"^n?ta$|^nita$|^nami$|^nnita$", "his pronoun shapes")
om(r"^nita$|^nnita$|^ita$|^ta$", "the 1pl-inclusive pronouns")

print("\n======== QELO / TMAGO / SQOAQE / SYULING")
for t in ("qelo", "tmago", "mtmago", "sqoaqe", "syuling", "qui"):
    show(t, 4)
om(r"^tmeego|^mtmeego|^teego|^meego", "the tmeego family")
om(r"^sqowaq|^squwaq|^quwaq", "the mouth root")
om(r"^siling|^msiling|^smiling", "the ask root")
