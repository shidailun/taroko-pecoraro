"""Batch 56: half-brown cards, and one word batch 37 got wrong.

PTGIMAX. Batch 37 mapped `ptgimax` to `ptgimah` 因喝…而死, matching shape and
attestation and never reading the card. The token occurs exactly once, on GIMAX
混合, in a sub-form glossed 使其混合 -- mixing, not drinking. IMAX 喝 is a
different headword and its own slots (pimax, spimax, mpimax) really are on it.
Batch 55 established that this family keeps the x (gmaxan 5x, gmaxun 3x, gimax,
gmimax), so the identity is the fix: brown, and the right word.

X'LYEX 誹謗. The gloss is a dead end -- 誹謗, 毀謗 and 中傷 are glossed nowhere in
the modern lexicon -- but 欺侮 is the same act and it has a whole paradigm:
lmhlih 15x 在欺侮, lhlih 4x, mlhlih 2x, slhlih 2x, plhlih, pplhlih, lhlihay. His
Xm'lyex is lmhlih segment for segment: X' is lh (CLAUDE.md finding (1) -- his l'x
and x'l are lh/rh, never dh), the m infix sits in the same slot, lyex is lih. The
two suffixed slots are regular -- lhlihay is written without syncope, so lhlihan
and lhlihun are the -an and -un of the same stem. Thirteen occurrences, and the
whole card was green.

PSPADAO 贈送. Half-brown: pspadaw, empspadaw and pnspadaw are all mapped, the root
is confirmed by pnpadaw 2x 送過的禮物, and `Pspdagun` was the one green token. The
obvious move -- restore the vowel he syncopated, as batch 55 did for SQDO -- is
wrong here, and imp.py caught it: `adag` occurs in NO modern type, while -agan and
-agun endings are everywhere (rngagan 143x, thdagan 23x, jyagun 15x). They are all
CCag-, never Vdag-. The alternation is written on 太陽: hidaw > thdagan 被太陽曬,
pnhdagan 15x, phdagun 2x -- final -aw becomes -ag- AND the stem vowel drops. So
padaw behaves as pdag-, and HIS spelling is already the modern one. `pspdagun` is
an identity, and the same correction is owed to `pnspdagan`, which an earlier
batch expanded to the impossible `pnspadagan`.

SAISAI 穗. `seysay` 6x 縠類的穗 -- his word with modern vowels (mseysay 2x 出結穗,
smeysay, enseysay, pgssayun). His whole example is "Saisai maso" = a millet ear.

TABU 餵養. His Tmabu>tmabug, Ptabu>ptabug, Tbuan>tbgan, Tnb'gan>tnbgan were all
restored long ago; two slots that live on OTHER cards were not. `stabu` is
`stabug`, attested and glossed 為…而餵, and both of his sentences are exactly that
-- stabu mo lodoç (for my chickens), stabu mo kui (for my silkworms). `tnabu` is
the -n- infixed stem, which keeps its vowel in the bare form the way tmabug does
and only syncopates before a suffix (tnbgan 23x).

NYAO 貓. He heads the card NYAO (NIYAO ?), unsure himself. Modern is `ngiyaw`:
the 171x entry is the 眼睛睜開 homograph, but mgngiyaw 像貓 carries the cat sense,
and no other candidate exists.

DDIYAL 戰勝. He writes the answer in his own headword -- "(var. = DGIYAL)" -- and
the card is already brown on it: ddiyal>dgiyal, dmdiyal>dmgiyal, mddiyal>mdgiyal,
dndyalan>dnegyalan. Only the three suffixed slots kept his l, and two of the three
are attested outright: dgyalan 贏過, dgyalun 1x 會打敗.

L'NGLONG 思考. lnglungan 383x, lnglungun 64x, lmnglung 220x, llnglung, lnglungi --
the card is brown throughout. `plnglngun` is the causative slot, and plnglung 5x
使…想 is the stem it is built on.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # GIMAX -- undo batch 37: the card is 混合, not 喝
    "ptgimax": "ptgimax",
    # X'LYEX -- the lhlih 欺侮 family
    "x'lyex": "lhlih", "xm'lyex": "lmhlih", "mx'lyex": "mlhlih",
    "xlyexan": "lhlihan", "xlyexon": "lhlihun",
    # PSPADAO -- his own syncope is the modern one (cf. hidaw > phdagun)
    "pspdagun": "pspdagun", "pnspdagan": "pnspdagan",
    # SAISAI
    "saisai": "seysay",
    # TABU -- the two slots that sit on other cards
    "stabu": "stabug", "tnabu": "tnabug",
    # NYAO
    "nyao": "ngiyaw", "niyao": "ngiyaw",
    # DDIYAL -- his own variant headword
    "ddyali": "dgyali", "ddyalan": "dgyalan", "ddyalun": "dgyalun",
    # L'NGLONG
    "plnglngun": "plnglungun",
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
