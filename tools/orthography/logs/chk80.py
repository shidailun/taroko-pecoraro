"""audit4 rows 4-34: the four that are not the syncope noise class.

Twenty-two of the thirty are either legitimate syncope (dhqan, grman, grngani,
qndrxan, phdagan, jyagan, drnani, geuyan, lqian, htran, hmkan, knhmtan, kndrmtan,
gnhpan) or values that are simply right and fail the substring test by accident
(smli 收集 = his 聚集, qyaan 被擋住 = his 障礙, sryuan 出口 = his 超出, smpi 晚上做夢
= his 做夢, lbuan 包紮 = his 包裹, ta 我們, do 的話). Those need nothing.

These four look like the alax class -- the card agrees on a root and one slot
holds an attested word from somewhere else:

  psloon   PS'LO 該挨打的; card is psru/msru/empsru/psruan (打), value psluun 蒸.
  sdxalan  SDAXAL 椅背－倚靠處; card is sdahar/smdahar/msdahar/psdahar,
           value sdxalan (identity) which the omnibus glosses 很髒.
  pk'lu    LU card is elug/meelug/gmeelug/peelug (road), his pk'lu 當…的時候,
           value pklu 剛好.
  klagan   KALAO 攀登; card is karaw/kmaraw/mkaraw/pkaraw, value kragan 整理.
           This one may be honest syncope with a homograph gloss, so the -an
           form of karaw has to be found before anything is said.
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
    ("beat (psru)", ["psru", "psruun", "psruan", "psluun", "msru", "empsru",
                     "sruun", "pnsru"]),
    ("lean/support (sdahar)", ["sdahar", "sdaharan", "sdharan", "sdxalan",
                               "smdahar", "psdahar", "sdhalan", "dahar"]),
    ("road (elug)", ["elug", "pklu", "peelug", "pnklug", "eelug", "klug",
                     "meelug", "pklug"]),
    ("climb (karaw)", ["karaw", "kragan", "karagan", "kmaraw", "pkaraw",
                       "krawan", "knkaraw"]),
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
for target in ("psloon", "sdxalan", "pk'lu", "klagan"):
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
                if n <= 14:
                    print("   [%-15s] %-4s %-28s %s" % (hw[:15], kind, (f or "")[:28],
                                                        (g or "")[:44]))
    print("   (%d slots)" % n)

print("\n########## his LU card ##########")
for ent in E:
    hw = (ent.get("hw") or "")
    if not re.match(r"^LU$|^'LU|^LU ", hw.upper()):
        continue
    print("--- %s   %s" % (hw, (ent.get("zh") or "")[:70]))
    for s in ent.get("subs", [])[:10]:
        f = (s.get("form") or "")
        kk = key(TOK.findall(f)[0]) if TOK.findall(f) else ""
        print("    sub %-13s -> %-11s %s" % (f[:13], MAP.get(kk, "(green)"),
                                             (s.get("zh") or "")[:44]))
