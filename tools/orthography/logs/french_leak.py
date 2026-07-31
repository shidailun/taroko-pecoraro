"""FRENCH METALANGUAGE LEAKING INTO THE TRUKU TOKEN STREAM.

The app already greys French apparatus -- FORM_PROSE, TAG_PROSE and metaAbbr run
before respellable(), so a field that is entirely prose is never asked for a
modern spelling. But they work on whole fields, and Pecoraro's typescript puts
French INSIDE otherwise-Truku fields:

    t = "Malu = Beau, bien"                     -> bien, beau
    t = "Mbanax = Rouge; Knbnaxan = Rougeur"    -> rouge
    t = "Mapa blongoi (porter la hotte)"        -> hotte, porter
    form = "Pqaya (Est-ce de la R. QAYA ?)"     -> est
    form = "Pngusul (R. = NGUSUL ? = qui ...)"  -> qui
    t = "Biyoq qouni (var. qoni)"               -> var
    t = "... (suite de la page precedente)"     -> suite

Every one of those is counted as an unverified Truku word. They are not Truku at
all, they can never be respelled, and they actively mislead the sweeps -- qui
was offered kuwi 62 and hotte was offered a landing this week.

The test uses the field the dictionary already carries. Every slot has a French
`fr` beside its Truku `t`/`form`/`hw`. A token that appears in the Truku field of
a slot AND in that same slot's French text is a token the French sentence also
uses; if that holds for EVERY slot the token appears in, it is not a Truku word
that happens to look French, it is French.

The "every slot" requirement is what makes it safe. A real Truku word quoted
inside its own French gloss -- which happens constantly, "var. qoni" -- is
shadowed in that slot but stands unshadowed in the slots where it is used as
Truku, so it is never flagged.

Prints the evidence per token so each can be read before anything is changed.
"""
import io, sys, json, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
MM = json.load(io.open(H + "tools/orthography/modern_map.json", encoding="utf-8"))["map"]
MAP = {k: v["modern"] for k, v in MM.items()}

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("['\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])

slots = []          # (headword, kind, truku text, french text)
for ent in E:
    hw = ent.get("hw") or ""
    slots.append((hw, "hw", ent.get("hw"), ent.get("fr")))
    for x in ent.get("examples", []):
        slots.append((hw, "ex", x.get("t"), x.get("fr")))
    for s in ent.get("subs", []):
        slots.append((hw, "sub", s.get("form"), s.get("fr")))
        for x in s.get("examples", []):
            slots.append((hw, "ex", x.get("t"), x.get("fr")))

occ = collections.defaultdict(list)     # token -> [(hw, kind, truku, shadowed?)]
for hw, kind, t, fr in slots:
    frtok = {key(w) for w in TOK.findall(fr or "")}
    for w in TOK.findall(t or ""):
        k = key(w)
        occ[k].append((hw, kind, t or "", k in frtok))

greens = {t for t in occ if t not in MAP and len(t) > 2}
flagged = []
for t in sorted(greens, key=lambda t: -len(occ[t])):
    rec = occ[t]
    if all(sh for _, _, _, sh in rec):
        flagged.append(t)

print("green types (len>2): %d" % len(greens))
print("FULLY SHADOWED BY THE FRENCH OF THEIR OWN SLOT: %d\n" % len(flagged))
tot = 0
for t in flagged:
    rec = occ[t]
    tot += len(rec)
    print("%2dx %-12s" % (len(rec), t))
    for hw, kind, txt, _ in rec[:3]:
        print("      [%-10s] %-4s %s" % (hw[:10], kind, txt[:70]))
print("\noccurrences: %d" % tot)

# and the near-misses: mostly shadowed, but not entirely
print("\n--- PARTIALLY shadowed (read these, do not act on them blind) ---")
for t in sorted(greens, key=lambda t: -len(occ[t])):
    rec = occ[t]
    sh = sum(1 for _, _, _, s in rec if s)
    if sh and sh < len(rec):
        print("%2d/%-2d %-12s  %s" % (sh, len(rec), t, rec[0][2][:56]))
