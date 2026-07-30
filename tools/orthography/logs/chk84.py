"""The two candidates from audit4 min-group 3, and a first look at a sharper
detector.

nique   his NGUSUL sub glossed 蝸牛, snail, on niqi 有… -- the have/exist word.
g'qani  his 收刀入鞘！ on glqani 拿去出草, go headhunting.

Then the third angle. audit2 reads tier id/B by frequency; audit4 reads card
coherence. Neither asks the question that actually matters for the ~2400 blind
browns: DOES THE OMNIBUS CONTAIN A BETTER WORD THAN THE ONE WE TOOK? Prototype
it here on these two -- search his gloss's content characters against every
omnibus gloss and rank candidates by spoken count.
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


for pat, label in (("\u8778\u725b", "snail"),
                   ("\u5165\u9798|\u5200\u9798|\u63d2\u5165", "sheathe"),
                   ("\u51fa\u8349|\u9996", "headhunt")):
    print("\n=== omnibus words glossed %s (%s) ===" % (label, pat))
    hits = sorted({(SPK.get(w, 0), w) for w, gs in OMNI.items()
                   for g in gs if re.search(pat, g)}, reverse=True)
    if not hits:
        print("   -- nothing --")
    for s, w in hits[:8]:
        show(w, "   ")

print("\n=== the two values, and their families ===")
for w in ("niqi", "niqan", "nique", "ngusul", "sngusul", "glqani", "gluq",
          "gmluq", "hgluq", "hmgluq"):
    show(w)

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
for target in ("nique", "g'qani"):
    print("\n########## every slot spelling %r  (now %s) ##########"
          % (target, MAP.get(target, "(green)")))
    n = 0
    for ent in E:
        hw = ent.get("hw") or ""
        slots = [(ent.get("hw"), ent.get("zh"), "hw"),
                 (ent.get("paradigm"), ent.get("zh"), "par")]
        slots += [(x.get("t"), x.get("zh"), "ex") for x in ent.get("examples", [])]
        for s in ent.get("subs", []):
            slots += [(s.get("form"), s.get("zh"), "sub")]
            slots += [(x.get("t"), x.get("zh"), "ex") for x in s.get("examples", [])]
        for f, g, kind in slots:
            if any(key(w) == target for w in TOK.findall(f or "")):
                n += 1
                if n <= 12:
                    print("   [%-14s] %-4s %-26s %s" % (hw[:14], kind, (f or "")[:26],
                                                        (g or "")[:46]))
    print("   (%d slots)" % n)

print("\n########## his NGUSUL card ##########")
for ent in E:
    hw = (ent.get("hw") or "")
    if not re.match(r"^NGUSUL|^NIQUE", hw.upper()):
        continue
    print("--- %s   %s" % (hw, (ent.get("zh") or "")[:70]))
    for s in ent.get("subs", [])[:9]:
        f = (s.get("form") or "")
        kk = key(TOK.findall(f)[0]) if TOK.findall(f) else ""
        print("    sub %-13s -> %-11s %s" % (f[:13], MAP.get(kk, "(green)"),
                                             (s.get("zh") or "")[:44]))
