"""kyoxan: same derivation shape as skpax and alax, but it sits on two cards.

His koyox 女人 is shipped kuyuh (spk 1196) and dkoyox is shipped dkuyuh. The
regular oblique kuyuh+-an = kuyuhan. Shipped instead is kyuhan 已擦傷, the
rub/scrape root, which serves neither the 女人 card nor the 雨 card. Count the
slots on each card before proposing, and check what his rain forms map to.
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
for w, g, _ in ROWS:
    if w and g:
        OMNI[w.lower()].append(g)


def show(w, pad="   "):
    used = [x for x in MAP if MAP[x] == w]
    print("%s%-13s spk %-5d %-34s %s" % (
        pad, w, SPK.get(w, 0),
        " | ".join(dict.fromkeys(OMNI.get(w) or []))[:34] or "-- BLIND --",
        ("<= his " + ",".join(used[:3])) if used else ""))


print("=== woman / rain ===")
for w in ("kuyuh", "kuyuhan", "kyuhan", "dkuyuh", "quyux", "quyuxan", "qmuyux",
          "kuxul", "knkuyuh"):
    show(w)

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
for target in ("kyoxan", "koyoc\u0327", "koyox"):
    print("\n########## every slot spelling %r  (now %s) ##########"
          % (target, MAP.get(target, "(green)")))
    n = 0
    for ent in E:
        hw = ent.get("hw") or ""
        slots = [(ent.get("hw"), ent.get("zh"), "hw"), (ent.get("paradigm"), ent.get("zh"), "par")]
        slots += [(x.get("t"), x.get("zh"), "ex") for x in ent.get("examples", [])]
        for s in ent.get("subs", []):
            slots += [(s.get("form"), s.get("zh"), "sub")]
            slots += [(x.get("t"), x.get("zh"), "ex") for x in s.get("examples", [])]
        for f, g, kind in slots:
            if any(key(w) == target for w in TOK.findall(f or "")):
                n += 1
                if n <= 16:
                    print("   [%-15s] %-4s %-28s %s" % (hw[:15], kind, (f or "")[:28], (g or "")[:44]))
    print("   (%d slots)" % n)

print("\n########## his rain card ##########")
for ent in E:
    hw = (ent.get("hw") or "")
    if not re.match(r"^KOYO", hw.upper()):
        continue
    print("--- %s   %s" % (hw, (ent.get("zh") or "")[:60]))
    for s in ent.get("subs", [])[:8]:
        f = (s.get("form") or "")
        kk = key(TOK.findall(f)[0]) if TOK.findall(f) else ""
        print("    sub %-13s -> %-11s %s" % (f[:13], MAP.get(kk, "(green)"), (s.get("zh") or "")[:40]))
