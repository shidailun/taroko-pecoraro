"""audit4's first page: four candidates, and the noise class it still has.

The detector works. Most of its top hits are legitimate morphophonemic syncope --
kndusan>kndsan, d'xqan>dhqan, gl'man>grman, glngani>grngani, kndlxan>qndrxan,
pxdagan>phdagan, dyagan>jyagan, dlnani>drnani, gguyan>geuyan, lqean>lqian -- where
the derived form drops a vowel the bare root keeps, so it fails a substring test
while being exactly right. That is the noise class, and it is recognisable on
sight, which is what matters.

xnigan>hnigan also clears: hnigan IS the body-shape word, and 一整頭;豬身 is one
of its senses, not a different word.

The four to check:
  skpax    his （sk'pax）用來工作的（工具、方法）on his K'PAX 工作 card, whose other
           eight slots are qpah/qmpah/mqpah/dmqpah -- and the value is skpax
           習慣放鞭炮, habitually setting off firecrackers.
  iyax     the card's other thirteen slots are the COME root (miyax>miyah,
           yaxan>yahan) and the headword is 中間.
  malax    on his BALAX 更新－使變新 card, whose slots are barah/embarah/mnbarah,
           and the value malax is 要放棄, abandon -- the opposite of renew.
  l'ndax   on his L'DAX 照亮 card (rdax/mrdax/knrdaxan/prdax), valued rndah
           更加的；反而更. Long-standing deferred item.

Both iyax and malax are shapes he uses on more than one card, so ownership is
printed before anything is proposed.
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
OMNI = collections.defaultdict(list)
for w, g, _ in ROWS:
    if w and g:
        OMNI[w.lower()].append(g)


def show(w, pad="   "):
    used = [x for x in MAP if MAP[x] == w]
    print("%s%-13s spk %-5d %-36s %s" % (
        pad, w, SPK.get(w, 0),
        " | ".join(dict.fromkeys(OMNI.get(w) or []))[:36] or "-- BLIND --",
        ("<= his " + ",".join(used[:3])) if used else ""))


print("=== work: the sq-/sk- slot of qpah ===")
for w in ("sqpah", "sqpahan", "ssqpah", "skpah", "spqpah", "qpah", "qmpah", "sqpahun"):
    show(w)
print("   -- omnibus words containing 'qpah' --")
for s, w in sorted({(SPK.get(w, 0), w) for w in OMNI if "qpah" in w}, reverse=True)[:10]:
    show(w, "      ")

print("\n=== come ===")
for w in ("iyah", "miyah", "yahan", "iyax", "meiyah", "empiyah"):
    show(w)

print("\n=== renew / abandon ===")
for w in ("barah", "mbarah", "embarah", "malax", "mlax", "smbarah", "pbarah"):
    show(w)

print("\n=== illuminate ===")
for w in ("rdax", "rndax", "rndah", "mrdax", "prdax", "knrdaxan"):
    show(w)

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
print("\n########## ownership ##########")
for target in ("skpax", "iyax", "malax", "l'ndax"):
    print("\n-- %s  (now %s) --" % (target, MAP.get(target, "(green)")))
    seen = []
    for ent in E:
        hw = ent.get("hw") or ""
        slots = [(ent.get("hw"), ent.get("zh"), "hw"),
                 (ent.get("paradigm"), ent.get("zh"), "par")]
        slots += [(x.get("t"), x.get("zh"), "ex") for x in ent.get("examples", [])]
        for s in ent.get("subs", []):
            slots += [(s.get("form"), s.get("zh"), "sub")]
            slots += [(x.get("t"), x.get("zh"), "ex") for x in s.get("examples", [])]
        for f, g, kind in slots:
            for w in TOK.findall(f or ""):
                if key(w) == target:
                    r = (hw[:17], kind, (g or "")[:46])
                    if r not in seen:
                        seen.append(r)
    for r in seen[:12]:
        print("   [%-17s] %-4s %s" % r)
    print("   (%d distinct slots)" % len(seen))
