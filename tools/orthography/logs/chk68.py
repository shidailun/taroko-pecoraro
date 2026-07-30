"""audit2 rows 45-105: the seven that survived a first reading.

Everything else in that block was one of the two false-positive classes already
identified -- synonym wording (his 剛才 vs modern 今天) or an incomplete omnibus
row (masu 小米 filed under 人名（男）, asu 船 under 阿叔). These seven are the ones
where the modern word may simply be a different word:

  sinao 49x  酒, millet wine  -- value sinaw is glossed 洗;清潔, and HE HIMSELF
             asks 是否為有別於 SINAO＝洗 的另一詞根? So he knew there were two.
  tasil 35x  石頭 -- value glossed 因壓扁而硬
  ita   35x  the root of "see" -- value glossed 我們
  nita  20x  我過去之所見 -- value glossed 我們的.  same collision
  ksa   22x  （你）說！ -- value glossed 走
  bbuyo 25x  黑暗 -- value bbuyu is the hunting/scrub word
  toxoi 20x  陪伴、同行 -- value tuhuy glossed 男女性行為

For each: every omnibus sense of the current value, its spoken count, and the
same for whatever else in the omnibus carries his meaning.
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

KEYS = ["sinao", "tasil", "ita", "nita", "ksa", "bbuyo", "toxoi"]
# what the meaning ought to look like in the omnibus, searched by gloss
WANT = {
    "sinao": "\u9152",          # wine
    "tasil": "\u77f3",          # stone
    "ita": "\u770b",            # see
    "nita": "\u770b",
    "ksa": "\u8aaa",            # say
    "bbuyo": "\u9ed1\u6697",    # dark
    "toxoi": "\u9673\u4f34",    # accompany
}


def senses(w):
    return list(dict.fromkeys(OMNI.get(w.lower()) or []))


for k in KEYS:
    v = MAP.get(k, "(green)")
    print("\n=== %-7s -> %-10s spk %-5s %s" % (
        k, v, SPK.get(v.lower(), 0), "!!LEXNULL!!" if (k in LEX and not LEX[k]) else ""))
    for g in senses(v)[:8]:
        print("      value sense  %s" % g[:70])
    # who else in the omnibus means what he means
    need = WANT[k]
    hits = [(SPK.get(w, 0), w, g) for w, gs in OMNI.items() for g in gs if need in g]
    hits.sort(reverse=True)
    seen = set()
    print("   -- omnibus words glossed with %s --" % need)
    for s, w, g in hits[:12]:
        if w in seen:
            continue
        seen.add(w)
        used = [x for x in MAP if MAP[x] == w]
        print("      %-14s spk %-5d %-34s %s" % (
            w, s, g[:34], ("<= his " + ",".join(used[:4])) if used else ""))
