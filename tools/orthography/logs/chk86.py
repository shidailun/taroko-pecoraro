"""Second pass: the variants of the batch-66 candidates, and four maybes.

The morning word is spelled three ways by him (ml'bu, m'lbu, mlbu) and all three
land on mrbu, spk 1 and unglossed. Check they are all his morning word before any
of them moves.

The sk- past-time series is the same shape as skawas: his SBIYAN card says in so
many words that SBIYAN, SGBIYAN and SKBIYAN mean the same thing, and the map
already sends two of the three to sgbiyan 昨天傍晚.

And the maybes: lading (val 不夠 against his 開始), lobong (val 深坑 against his
覆蓋/陷阱), mqleqo/mkleqo (val mqriqu spk 1 against msriqu 困難 spk 35), usuk.

usuk needs one extra check. charRules folds x to h, so an omnibus word ending in
x looks foreign to the modern orthography -- but iyax 中間 sits at spk 115, so x
words ARE in the spoken Truku data and usux 袖子 is not disqualified by its shape.
Count the x words to be sure that is a class and not one stray row.
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
for r in ROWS:
    if r[0] and r[1]:
        OMNI[r[0].lower()].append(r[1])


def show(w, pad="   "):
    used = [x for x in MAP if MAP[x] == w]
    print("%s%-13s spk %-5d %-40s %s" % (
        pad, w, SPK.get(w, 0),
        " | ".join(dict.fromkeys(OMNI.get(w) or []))[:40] or "-- BLIND --",
        ("<= his " + ",".join(used[:4])) if used else ""))


print("=== x-final words in SPOKEN Truku: is x a live letter, or one stray row? ===")
xw = sorted(((SPK.get(w, 0), w) for w in OMNI if "x" in w), reverse=True)[:12]
for s, w in xw:
    show(w)
print("   %d omnibus words contain x; %d of them are spoken at all"
      % (sum(1 for w in OMNI if "x" in w), sum(1 for w in OMNI if "x" in w and SPK.get(w, 0))))

print("\n=== the evening series ===")
for w in ("sbiyan", "sgbiyan", "skbiyan", "gbiyan", "kbiyan", "psgbiyan"):
    show(w)

print("\n=== 開始 ===")
for w in ("rajing", "prajing", "mprajing", "lading", "rading", "tprajing"):
    show(w)

print("\n=== 覆蓋 / 陷阱 ===")
for w in ("rbung", "rubung", "rubang", "qlubung", "rmbung", "trbung", "lobong"):
    show(w)

print("\n=== 困難 ===")
for w in ("mqriqu", "msriqu", "sriqu", "mkriqu", "riqu", "mqleqo"):
    show(w)

print("\n=== sleeve ===")
for w in ("usux", "usuk", "smusux", "musux"):
    show(w)

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("['\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
for target in ("m'lbu", "mlbu", "sbiyan", "usuk", "lading", "lobong", "mqleqo",
               "mkleqo"):
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
                if n <= 10:
                    print("   [%-14s] %-4s %-28s %s" % (hw[:14], kind, (f or "")[:28],
                                                        (g or "")[:46]))
    print("   (%d slots across %d cards: %s)"
          % (n, len(cards), ", ".join("%s x%d" % c for c in cards.most_common(5))))
