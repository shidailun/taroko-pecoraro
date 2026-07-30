"""audit4 rows 70-140: three more of the alax class, and the ones that clear.

Clearing (the value string is right, the omnibus gloss belongs to a homophone or
the majority is a syncopated -an stem so the bare root is the "outlier"):
  x'mlo>hmru   the m-infix of hru is exactly his 動詞形; 水源 is a homophone row
  kala>kala    mgkala/pgkala prove the bare root is kala; 「來」的詞根 is another
  adop/madop/p'adop, adas d'si/d'san/d'sun, tabu tmabu/mtabu/ptabu, spu/smpu,
  xolit>hurit, oqon>uqun, ssagan, klwaan, daan, ddaon, ks'gun, tiyan, bxoi/bxoon,
  snd'xgan, saan -- all correct
  g'loq>gluq   CLOSED from the deferred list: his xmgloq 出鞘 is already shipped
               hmgluq 抽;拔, an exact match, so the gluq root is his and 污垢 is
               the homophone. The G'LOQ "split family" needs nothing.

The three to check, all the same shape as alax -- the card agrees on a root and
one slot holds an attested word from elsewhere:
  l'pi     his own gloss is "D'pi ＝ 關！（命令式）" -- he says it IS d'pi -- and
           the value lpi is 無米粒的稻穀, empty rice husk. His d'pan>dpan 關門 is
           already shipped on the same card.
  tmquli   his TKULI 倒入；使容納, where his other spelling tmkuli is already
           shipped tmquri 已裝、倒. The value tmquli is 撫養, to raise a child.
  mnsa     his 已去過, the past of go, on his USA card where mnusa>mnusa is
           already shipped. The value mnsa is 如此說…, the past of SAY -- a
           different verb that happens to look like his shortened spelling.
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


GROUPS = [
    ("close (duk)", ["dpi", "dpan", "dpun", "lpi", "enduk", "mduk", "smduk", "duk"]),
    ("pour in (tquri)", ["tmquri", "tmquli", "tqriun", "tqrian", "quri", "tquri"]),
    ("go (usa)", ["musa", "mnusa", "mnsa", "usa", "saan", "msa", "mha", "nusa"]),
]
for name, ws in GROUPS:
    print("\n=== %s ===" % name)
    for w in ws:
        show(w)

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
for target in ("l'pi", "tmquli", "mnsa", "psloon", "sdxalan", "pk'lu"):
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
                    print("   [%-15s] %-4s %-26s %s" % (hw[:15], kind, (f or "")[:26],
                                                        (g or "")[:46]))
    print("   (%d slots)" % n)
