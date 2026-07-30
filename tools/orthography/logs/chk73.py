"""Ownership pre-flight for batch 63: 'loan, and what MALI actually is.

pai and loan both landed, and both are the pax pattern -- the map already accepts
the right modern word for a NEIGHBOURING key of his while leaving this one on an
unrelated word:
   his LOAN's own headword reads "LOAN (LOWAN ?)", and his lowan is ALREADY
   shipped as ruwan 內部，裡面 spk 379, while loan sits on ruan 要…弄 spk 16.
   his PAI 祖母／外婆／岳母 against payi 女性長輩(祖母；外婆；岳母) spk 357, gloss for
   gloss, while the shipped pai spk 1 means 去揹. His baki 祖父 is already right.

Two things to settle before writing:
  1. 'loan shares the value ruan. Which card owns it -- is it the same word with
     his elision mark, or something else that would be collateral damage?
  2. MALI printed with an EMPTY headword gloss, so audit2's 買、賣（動詞形）came
     from some other entry's slot. Find who defines it before touching it. His
     buy root is BLI (bligan > brigan brig-), which mali does not fit.
"""
import io, sys, json, pickle, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
LEX = json.load(io.open(H + "tools/orthography/lexical_map.json", encoding="utf-8"))
MAN = json.load(io.open(H + "tools/orthography/manual_map.json", encoding="utf-8"))
OMNI = collections.defaultdict(list)
for w, g, _ in ROWS:
    if w and g:
        OMNI[w.lower()].append(g)
TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])

WATCH = {"'loan", "loan", "mali", "pai", "pax", "npax", "mpax"}
OWN = collections.defaultdict(list)
for ent in E:
    hw = ent.get("hw") or ""
    slots = [(ent.get("hw"), ent.get("zh"), "hw"), (ent.get("paradigm"), ent.get("zh"), "par")]
    slots += [(x.get("t"), x.get("zh"), "ex") for x in ent.get("examples", [])]
    for s in ent.get("subs", []):
        slots += [(s.get("form"), s.get("zh"), "sub"), (s.get("paradigm"), s.get("zh"), "sub")]
        slots += [(x.get("t"), x.get("zh"), "ex") for x in s.get("examples", [])]
    for f, g, kind in slots:
        for w in TOK.findall(f or ""):
            k = key(w)
            if k in WATCH:
                OWN[k].append((hw, kind, (g or "")[:46]))

for k in ("'loan", "loan", "mali"):
    print("\n=== %s  -> %s ===" % (k, MAP.get(k, "(green)")))
    seen = set()
    for hw, kind, g in OWN[k]:
        if (hw, kind, g) in seen:
            continue
        seen.add((hw, kind, g))
        print("   [%-14s] %-4s %s" % (hw[:14], kind, g))

print("\n=== full MALI entry ===")
for ent in E:
    hw = ent.get("hw") or ""
    if key(TOK.findall(hw)[0] if TOK.findall(hw) else "") != "mali":
        continue
    print(json.dumps(ent, ensure_ascii=False, indent=1)[:1400])

print("\n=== his buy family, as shipped ===")
for ent in E:
    hw = ent.get("hw") or ""
    if not re.match(r"^(BLI|MALI|BLIGAN|MLI)", hw.upper()):
        continue
    print("\n--- %s  %s" % (hw, (ent.get("zh") or "")[:70]))
    for s in ent.get("subs", [])[:10]:
        f = (s.get("form") or "")
        kk = key(TOK.findall(f)[0]) if TOK.findall(f) else ""
        print("   sub %-12s -> %-10s %s" % (f[:12], MAP.get(kk, "(green)"),
                                            (s.get("zh") or "")[:44]))

print("\n=== value attestation for the batch ===")
for k, v in (("pai", "payi"), ("loan", "ruwan"), ("'loan", "ruwan"),
             ("pax", "paah"), ("npax", "npaah"), ("mpax", "empaah")):
    o = OMNI.get(v)
    print("   %-8s %-10s -> %-10s spk %-5d %-30s %s%s" % (
        k, MAP.get(k, "(green)"), v, SPK.get(v, 0),
        (" | ".join(dict.fromkeys(o))[:30] if o else "-- BLIND --"),
        "LEXNULL " if (k in LEX and not LEX[k]) else "",
        ("manual=" + MAN[k]) if k in MAN else ""))
