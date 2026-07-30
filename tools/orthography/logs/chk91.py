"""Ownership and attestation pre-flight for batch 67.

  wakat/waqat  犬齒, and his Mwakat 有犬齒的－長出嫩芽的 -- the modern waqit does
               the same two jobs: waqit 芽, swaqit 大獠牙. Same polysemy, and his
               own example already spells it waqat.
  sl'dan       黏附 -- sltan 被黏著, the -an form of the sdlut his card ships.
  luula        公開地 -- his pluula/tluula/ptluula/ptllaani ALL ship with -eura
               inside. Which bare form does the omnibus actually attest: ura,
               eura or reura?
  longao       his DOBUT card names LONGAO as the synonym for 瓶子, and the
               omnibus has plungaw 直接用瓶子喝. Is longao a key, and is lungaw
               attested as a headword rather than only inside derived forms?
  bsqlol       his sqlol IS sqrul letter for letter once l>r and o>u are applied
               -- except charRules also folds the FINAL l to r and prints BSQRUR.
  knluus       LUUS ships knluus>knruus 偷偷地去 against his 孤獨的程度, and
               luus>luus id against his 獨自－孤獨－單身. A blind brown that
               contradicts the card.

Every slot of every token, so a value is checked against the whole card and not
against the row that turned up.
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
    print("### %-12s -> %-14s %-3s spk %-4s %s"
          % (tok, v or "-- GREEN --", TIER.get(tok, ""),
             SPK.get((v or "").lower(), 0) if v else "",
             " | ".join(dict.fromkeys(OMNI.get((v or "").lower()) or []))[:40] if v else ""))
    for hw, kind, f, g in his.get(tok, []):
        print("    [%-12s] %-4s %-40s %s" % (hw[:12], kind, (f or "")[:40], (g or "")[:46]))
    if not his.get(tok):
        print("    (no slots -- not a token of his)")


def om(pat, note=""):
    rx = re.compile(pat)
    hit = sorted(((SPK.get(w, 0), w) for w in OMNI if rx.search(w)), reverse=True)
    print("--- omnibus /%s/ %s -> %d" % (pat, note, len(hit)))
    for s, w in hit[:16]:
        print("    %-14s spk %-5d %s" % (w, s, " | ".join(dict.fromkeys(OMNI[w]))[:52]))


print("======== WAKAT family")
for t in ("wakat", "waqat", "mwakat", "snwakat"):
    show(t)
om(r"waqit|waqat", "the tusk/sprout word")

print("\n======== SL'DAN")
for t in ("sl'dan", "sldan"):
    show(t)
om(r"^slt|sdlut|^slut", "the sticking root")

print("\n======== LUULA -- which bare form is attested")
for t in ("luula", "tluula", "pluula"):
    show(t)
for pat in (r"^ura$", r"^eura$", r"^reura$", r"eura", r"^ura"):
    om(pat)

print("\n======== LONGAO / bottle")
for t in ("longao", "longaw", "dobut"):
    show(t)
om(r"lungaw|lngaw", "bottle")

print("\n======== BSQLOL")
for t in ("bsqlol", "mbsqlol", "sqlol"):
    show(t)
om(r"sqrul|sqrl|bsqr", "burnt")

print("\n======== LUUS -- the blind browns that contradict the card")
for t in ("luus", "knluus", "knlsan", "knl'san"):
    show(t)
om(r"ruus|luus|burux", "solitude")
