"""audit2 rows 105-175: three candidates, and one pending item closed.

The block is dominated by a THIRD false-positive class, now named: the omnibus
files a personal name on the same shape and audit2 quotes it. rungay 猴子 comes
back 人名（男）, lungaw 瓶子 人名, harung 松樹 人名, pisaw 麻雀 人名, gasil 繩子
加希爾(男子名), biyuq 汁液 人名, sipaw 對面 西寶(地名). All correct as shipped.

CLOSED, and it was on the open list: bare tana 11x was suspected of being tama
with the typewriter m read as n. It is not. His gloss is 複合人稱代名詞＝我們與他
and modern tana spk 11 is 我們;他對我們 -- the same pronoun, exactly.

Still to check:
  pai  14x  his 祖母／外婆 -- value pai spk 1 is glossed 去揹. Truku's grandmother
            word looks like payi, and his own baki 祖父 is already shipped right.
  mali 13x  his 買、賣 -- value mali spk 2 is glossed 加多.
  loan 10x  his 內部－在…裡 -- value ruan spk 16. Is the modern shape ruan or ruwan?
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


def show(w):
    used = [x for x in MAP if MAP[x] == w]
    print("   %-12s spk %-5d %-40s %s" % (
        w, SPK.get(w, 0), " | ".join(dict.fromkeys(OMNI.get(w) or []))[:40] or "-- BLIND --",
        ("<= his " + ",".join(used[:3])) if used else ""))


print("=== grandmother ===")
for w in ("pai", "payi", "payiq", "bubu", "baki"):
    show(w)
print("   -- omnibus rows glossed 祖母/外婆/婆婆 --")
for s, w in sorted({(SPK.get(w, 0), w) for w, gs in OMNI.items()
                    for g in gs if re.search("\u7956\u6bcd|\u5916\u5a46|\u5a46\u5a46", g)},
                   reverse=True)[:8]:
    show(w)

print("\n=== buy / sell ===")
for w in ("mali", "mari", "marig", "mbarig", "brigan", "barig"):
    show(w)

print("\n=== inside ===")
for w in ("ruan", "ruwan", "loan", "truan"):
    show(w)
print("   -- omnibus rows glossed 裡面 --")
for s, w in sorted({(SPK.get(w, 0), w) for w, gs in OMNI.items()
                    for g in gs if "\u88e1\u9762" in g}, reverse=True)[:8]:
    show(w)

TOK = re.compile(r"[A-Za-z\u00c7\u00e7\u00c0-\u017f'\u2019\u02bc\"]+")


def key(w):
    return re.sub("[\u2019\u02bc\"\u0294]", "'", w).replace("\u0142", "l").lower()


e = io.open(H + "site/entries.js", encoding="utf-8").read()
E = json.loads(e[e.index("["):e.rindex("]") + 1])
LOOK = {"pai", "mali", "loan"}
print("\n########## his cards ##########")
for ent in E:
    hw = ent.get("hw") or ""
    ws = TOK.findall(hw)
    if not ws or key(ws[0]) not in LOOK:
        continue
    print("\n--- %s  %s" % (hw, (ent.get("zh") or "")[:80]))
    for x in ent.get("examples", [])[:3]:
        print("      ex  %-42s %s" % ((x.get("t") or "")[:42], (x.get("zh") or "")[:40]))
    for s in ent.get("subs", [])[:8]:
        f = (s.get("form") or "")
        k = key(TOK.findall(f)[0]) if TOK.findall(f) else ""
        print("      sub %-12s -> %-10s %s" % (f[:12], MAP.get(k, "(green)"),
                                               (s.get("zh") or "")[:40]))
print("\n-- lexical_map on these --")
for k in sorted(LEX):
    if k.lstrip("_") in LOOK:
        print("   %-10s = %s" % (k, json.dumps(LEX[k], ensure_ascii=False)[:250]))
