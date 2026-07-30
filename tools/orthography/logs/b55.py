"""Batch 55: the green work list, ranked by frequency, after the counter was fixed.

green3.py was still ranking his French editorial words as work to do, because it
subtracts the three curated tables but not FORM_PROSE / TAG_PROSE. green6.py
subtracts those too. What is left at the top of the list is Truku, and most of it
is CLAUDE.md finding (4): a slot skipped when its family was mapped.

"LU. The road root, fixed in batches 34/35, and two slots were left behind.
`p'lu` is `peelug`, attested and glossed 有…的路徑, which is his sentence exactly
(P"lu ko bi musa dopan = on the way to the hunting ground); the family is
unanimous -- gmeelug, pneelug, meelug, seelug, smeelug. And `snlluwan` is his own
doubled-l spelling of Snluwan, which batch 35 hand-corrected to `sneelugan`; he
writes the slot twice on the same paradigm line, so the two spellings are one word.

L'PAN. `l'pun` was claiming `rpun` -- 48x, and glossed 大肚子, a big belly, on a
card about shutting a door. The batch-33 lesson: an ATTESTED value can be a WRONG
value, and no shape test sees it. His own family keeps the l (l'pi>lpi,
l'pan>lpan), so the keep-l identity is what the card already says.

SQDO. `smrqdug` 控告 is his gloss word for word, and modern never syncopates the
root -- rqdug 3x, rmqdug 4x, prqdug 8x, ssqdug, and his own Snqdgan is already
`snqdugan` with the u. The three suffixed slots kept his syncope.

NIQ. `mpnyeqon` is `empniqun`, attested, and the rest of the family was mapped
long ago: nyeqan>niqan 2170x, nnyeqan>nniqan 202x, pnyeqan>pniqan 25x, nyeq>niq.
The emp- schwa is batch 26's class.

GEEGUY. `mn'gui` is `gmneeguy` 2x 偷竊過 -- and the map already had it, under his
OTHER spelling of the same slot: SQDO's example line reads "mnagwi mn'gui", both
words for the one act, and only `mnagwi` had ever been adjudicated.

BBIL. blbil 拉 15x with twenty derivatives, every one keeping the l, and the map
converts his doubled initial to it throughout (bbil>blbil, bbilan>blbilan,
bbilun>blbilun). `kmbibil` was rendering KMBIBIR.

GIMAX. The family is attested WITH the x -- gmaxan 5x, gmaxun 3x, gmaxi, gimax,
gmimax -- so `pnmaxan` rendering PNMAHAN is the char rule contradicting the card.
Modern Truku keeps x; that is a word-by-word question, never a blanket one.

KLAWAX. smkrawah 11x, pkrawah 8x, kkrawah 4x settle the root, and four slots were
already on it. `klwaxan` was an identity keeping BOTH his l and his x against
them, and `klwaxe` was green.

GLIXO 穿透——刺穿. The root is `lihug` 刺 -- his x is h and his lost final g is the
same class as TABU>tabug and "LU>elug. `pglihug` is attested and is his Pglixo
letter for letter; tklihug 13x 瞬間穿過, pklihug 2x, klihug, slihug 用來穿,
mkmlihug 想穿針線 are the rest of the paradigm, every one with the l his card was
turning into r. The suffixed shape is not a guess either: **`lhgan` 2x is glossed
穿過**, so the syncope is written, and his Plxgun is that stem with x for h.

K'LAE. Batch 19 established that this family wants the l->r rule (mkray 40x 硬;貴,
knklayan>knkrayan) -- the green PKRAY was already correct. `pklayan` was the one
slot claiming otherwise, and `pklayan` occurs nowhere but this paradigm line, so
the K'LA 知道 homograph that protects `k'lae` and `pk'lae` does not reach it.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # "LU -- the road, and his plan built on it
    "p'lu": "peelug",
    "snlluwan": "sneelugan",
    # L'PAN -- stop claiming 大肚子
    "l'pun": "lpun",
    # SQDO -- the root keeps its u
    "sqdgi": "sqdugi", "sqdgan": "sqdugan", "sqdgun": "sqdugun",
    # NIQ
    "mpnyeqon": "empniqun",
    # GEEGUY -- his own already-mapped twin
    "mn'gui": "gmneeguy",
    # BBIL
    "kmbibil": "kmblbil",
    # GIMAX -- the family keeps the x
    "pnmaxan": "pnmaxan",
    # KLAWAX
    "klwaxe": "krwahi", "klwaxan": "krwahan",
    # GLIXO -- lihug, and lhgan for the suffixed stem
    "glixo": "glihug", "gmlixo": "gmlihug", "pglixo": "pglihug",
    "plxgun": "plhgun", "plx'gun": "plhgun", "pglxgun": "pglhgun",
    # K'LAE -- one paradigm, one letter
    "pklay": "pkray", "pklayan": "pkrayan", "pklayun": "pkrayun",
}

p = H + "manual_map.json"
d = json.load(io.open(p, encoding="utf-8"))
before = len(d)
clash = {k: (d[k], v) for k, v in FIX.items() if k in d and d[k] != v}
if clash:
    print("overriding %d earlier manual keys:" % len(clash))
    for k, (o, n) in sorted(clash.items()):
        print("   %-10s %s -> %s" % (k, o, n))
d.update(FIX)
body = ",".join("%s:%s" % (json.dumps(k, ensure_ascii=False),
                           json.dumps(v, ensure_ascii=False))
                for k, v in sorted(d.items()))
io.open(p, "w", encoding="utf-8", newline="\n").write("{\n" + body + "\n}\n")
print("manual_map %d -> %d  (batch touches %d keys)" % (before, len(d), len(FIX)))
