"""audit5's first six: the shipped value is unattested or means something else,
and the omnibus holds a near-spelling that says exactly what HE says.

  skawas  17x  his 去年              val skawas  spk 0     cand shkawas 去年   spk 19
  ml'bu    8x  his 早晨              val mrbu    spk 1     cand mgrbu   早晨   spk 256
  mbuyas   8x  his 肚子              val embuyas spk 0     cand nbuyas  肚子   spk 13
  mnswai   7x  his 兄弟姊妹           val mnswai  spk 2     cand mnswayi 兄弟姊妹 spk 347
  lawa     6x  his 呼喚/籃子          val lawa    人名（女）  cand rawa    籃子   spk 44
  ayo      5x  his 小溪－水溝          val ayu     spk 4     cand ayug    小溪   spk 100

Before anything is written: ownership. A key is one row in a flat map, so if a
second card spells the same token in a different sense, correcting it here breaks
it there. Print every card that uses the key and every slot's gloss.

Also check the SOURCE of each candidate row. The omnibus is not Truku alone, and
a form like usux carrying an x could be a Seediq entry, in which case it is not
evidence about modern Truku spelling at all.
"""
import io, sys, json, pickle, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
ROWS = pickle.load(io.open("omni.pkl", "rb"))[0]
SPK = json.load(io.open(H + "tools/orthography/spoken_truku.json", encoding="utf-8"))
t = io.open(H + "site/modern_map.js", encoding="utf-8").read()
a = t.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
MAP = json.loads(t[a:t.index("\n};", a) + 2])
OMNI = collections.defaultdict(list)
SRC = collections.defaultdict(set)
for r in ROWS:
    w, g = r[0], r[1]
    if w and g:
        OMNI[w.lower()].append(g)
        SRC[w.lower()].add(str(r[2])[:22] if len(r) > 2 else "?")


def show(w, pad="   "):
    used = [x for x in MAP if MAP[x] == w]
    print("%s%-13s spk %-5d %-40s %s" % (
        pad, w, SPK.get(w, 0),
        " | ".join(dict.fromkeys(OMNI.get(w) or []))[:40] or "-- BLIND --",
        ("<= his " + ",".join(used[:4])) if used else ""))


print("=== the sk-/sh- past-time series (skawas sits in it) ===")
for w in ("skawas", "shkawas", "sngkawas", "kawas", "shiga", "sbiyan", "sgbiyan",
          "skbiyan", "gbiyan", "shkuxul", "sknuwan"):
    show(w)
print("   sources: shkawas=%s  skawas=%s" % (SRC.get("shkawas"), SRC.get("skawas")))

print("\n=== morning: his ml'bu / knlbuan ===")
for w in ("mrbu", "mgrbu", "grbu", "rbu", "kngrbuan", "knrbuan", "knlbuan",
          "mgrbuan", "sgrbu"):
    show(w)

print("\n=== belly ===")
for w in ("embuyas", "mbuyas", "nbuyas", "buyas", "smbuyas", "knbuyas", "tbuyas"):
    show(w)
print("   sources: nbuyas=%s" % (SRC.get("nbuyas"),))

print("\n=== siblings ===")
for w in ("mnswai", "mnswayi", "swayi", "mswayi", "dmnswayi", "qbsuran"):
    show(w)

print("\n=== call / basket ===")
for w in ("lawa", "rawa", "mlawa", "mrawa", "lmawa", "rmawa", "brunguy", "towkan"):
    show(w)

print("\n=== stream ===")
for w in ("ayu", "ayug", "yayung", "qsiya", "ayung"):
    show(w)
print("   sources: ayug=%s  ayu=%s" % (SRC.get("ayug"), SRC.get("ayu")))

print("\n=== sleeve (usux carries an x -- whose dictionary is it?) ===")
for w in ("usuk", "usux", "usuh", "usug"):
    show(w)
    print("        src %s" % (SRC.get(w) or "--"))

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("['\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
for target in ("skawas", "ml'bu", "mbuyas", "mnswai", "lawa", "ayo"):
    print("\n########## every slot spelling %r  (now %s) ##########"
          % (target, MAP.get(target, "(green)")))
    n = 0
    cards = collections.Counter()
    for ent in E:
        hw = ent.get("hw") or ""
        slots = [(ent.get("hw"), ent.get("zh"), "hw"),
                 (ent.get("paradigm"), ent.get("zh"), "par")]
        slots += [(x.get("t"), x.get("zh"), "ex") for x in ent.get("examples", [])]
        for s in ent.get("subs", []):
            slots += [(s.get("form"), s.get("zh") or ent.get("zh"), "sub")]
            slots += [(x.get("t"), x.get("zh"), "ex") for x in s.get("examples", [])]
        for f, g, kind in slots:
            if any(key(w) == target for w in TOK.findall(f or "")):
                n += 1
                cards[hw] += 1
                if n <= 14:
                    print("   [%-14s] %-4s %-30s %s" % (hw[:14], kind, (f or "")[:30],
                                                        (g or "")[:44]))
    print("   (%d slots across %d cards: %s)"
          % (n, len(cards), ", ".join("%s x%d" % c for c in cards.most_common(6))))
