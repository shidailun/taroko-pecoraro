"""Batch 59: the marriage root, and three would-be defects the pre-flight killed.

THE FIND: his `-stlo(o)ng-` is modern `strung` 相遇/結婚, and one shipped brown
value was on the wrong root. IYUX's three slots are all glossed marriage --
"Kmstloon ko bi ka yako" 我啊，很想結婚 / "Kmpstlngun na bi laqe na ka Iwal"
Iwal 很想讓兒子成婚 / "Ana ko kmpstloong laqe o, ongat içan" 儘管我想讓兒子成婚…
-- and no form of the SIT root (his tloong, modern tluung 125x) carries a marriage
sense anywhere in the omnibus. The MEET root does, in his exact words:
`pnstrngan` 成婚;相遇的地方 18x, `pstrung` 相遇（結婚;打戰）4x, `mstrung` 相遇 58x,
`strung` 去聚會所見面 25x, `strngan` 13x, `strngun` 2x, `pstrngun` 2x, `empstrung`
9x. And the map ALREADY ships stlong>strung, mstlong>mstrung, mpstlong>empstrung
-- so the family had committed to str- everywhere except these three. `kmstloon`
was brown as `kmstruun`, i.e. on the sit stem, and is corrected here; his final
single n is his dropped ng, as everywhere else.

THREE KILLED BEFORE THE WRITE, which is what the pre-flight is for:
 - `ttuun`/`ttuon`/`t'tuan`/`stbako` are `lexical_map.json` NULLS, and the builder
   discards a null key after the manual write ((manual|llm) - lex_block). _ttuun's
   own note reads "Claimed twice now -- b48 ttuun, b49 t'tuan -- and reverted both
   times… Null: left green until a real form turns up." A third attempt on a
   twice-reverted decision is not evidence. `ttuan` was dropped with them rather
   than leave the TA'TO family half-claimed. NEW EVIDENCE, recorded not acted on:
   `ttui` IS attested (omnibus 切、剁, spk 2), which the note's reckoning did not
   include -- it only weighed teetu-shapes and read the ttuy- forms as TUTWI's.
   With `knttuun` 1x and `sttuan` 3x named in the note itself, the geminate ttu-
   cut stem now has three witnesses. Amend the note, don't unblock yet.
 - `mpkuda` is a DEAD key. The real token is `mpkuda'` (his Mpkudaʔ, ʔ folded to
   '), and it is already mapped to `empkudaw`.
 - `ilnabao` is a TRANSCRIPTION defect, not a spelling one: PADYAQ's "Taan ta
   ilnabao qouni dgiyaq o" 觀看山上樹木的葉子 is his own `lnabao`>`rnabaw` 葉子
   123x with a scan-joined `i`. Mapping it would delete a character silently.
   Same class as upsk'la / ukwi / umyaq -- fix the transcription, upstream.

THE REST, by kind.

1. HIS OWN PARENTHETICAL, which makes the equation his and not mine:
   `tbiun(tbiyun) (ptbiun ?)` on TABE, beside shipped tbiyun / tbian>tbiyan /
   ptbian>ptbiyan; `Ida ms"lu (nsl"lu) ko bi ka yako` on "LU, beside
   psl'lu>psleelug; `Nbaxang bi bilat mo o (bnaxang bi bilat mo o)` on L'NGAT,
   with nbaxang>qnbahang already shipped on that same line (`qnbahang` 13x).

2. THE SIBLING NAMES THE ROOT: `mptsadyaq`>emptseejiq from KSOLOÇ's
   "Mptksoloç ka iso… mptsadyaq so da" 你要成為得人的漁夫, beside
   mptksoloç>emptqsurux and sadyaq>seejiq 2623x. `pkloi`>pkrui from PARO's
   paradigm "Mpkparo, pkparo, pkloi, pkploan, pkploon" beside the parallel
   SMPARO's sploi>sprui 9x. `patuxun`>peeutuxun from OTOç's own split -- his
   pa- forms take the double e (paotoç>peeutux, ppaotoç>ppeeutux) where the
   bare p- forms take one (ptuxi/ptuxan/ptuxun>peutux-). `gqoaq`>gquwaq from
   GQOAQ 搖頭's three shipped siblings (qoaq>quwaq, sqoaq>squwaq,
   gmqoaq>gmquwaq); charRules would print gquaq, so this is a real change.
   `kmttg'xal`>kmttgxal from SAPAT's "kmttg'xal balae" 他們很喜歡湊在一起, and
   `tgxal` is glossed 團聚 4x -- this one OVERRIDES charRules' x>h, which modern
   Truku declines in 793 spoken types.

3. THE OMNIBUS NAMES IT BY GLOSS: the DAO card 隱藏——保守祕密 against `daaw`
   隱瞞事情, `dmdaaw` 很會隱瞞, `ddaaw` 對…隱瞞 -- word for word. `spngao`>spngaw
   from SM"LU's "Spngao ta otoç… ima ka sn"lu kmpaxan nii" 我們來抽籤看這塊田會歸誰:
   a hortative, and word-final -ao is -aw (267 of the 280 mapped -ao keys, and
   2,407 modern types in -aw against 4 in -au).

FROZEN, the b57/b58 kind -- the family is frozen and the claim only changes the
colour: `dmbasyaq` beside its own shipped dmt'basyaq>dmtbasyaq on the same SAPAT
line, and `siba`, whose card reads 草坪（日語詞）in his own hand -- Japanese 芝,
tier J's business, not a Truku respelling.

NOTE: `dao`/`dmao`/`mdao` still need the map even after this session's charRules
edit, because the rule produces `daw` and the word is `daaw`. `spngao` and `pkloi`
are confirm-only (charRules now prints exactly the value); they are written to
turn a correct guess into a stated claim, which is the whole difference between
green and brown.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # the marriage root -- one correction and two greens
    "kmstloon": "kmstrung",          # WAS kmstruun, the sit stem
    "kmpstloong": "kmpstrung",
    "kmpstlngun": "kmpstrngun",      # strngun 2x, pstrngun 2x
    # 1. his own parenthetical
    "tbiun": "tbiyun", "ptbiun": "ptbiyun",   # tbiun(tbiyun) (ptbiun ?)
    "nsl'lu": "nsleelug",            # Ida ms"lu (nsl"lu); psl'lu>psleelug
    "bnaxang": "qnbahang",           # Nbaxang (bnaxang); 13x
    # 2. the sibling names the root
    "mptsadyaq": "emptseejiq",       # mptksoloç>emptqsurux; sadyaq 2623x
    "pkloi": "pkrui",                # sploi>sprui 9x on SMPARO
    "patuxun": "peeutuxun",          # paotoç>peeutux, his pa- takes double e
    "gqoaq": "gquwaq",               # qoaq>quwaq, sqoaq>squwaq, gmqoaq>gmquwaq
    "kmttg'xal": "kmttgxal",         # tgxal 團聚 4x; keeps the x deliberately
    # 3. the omnibus names it by gloss
    "dao": "daaw", "dmao": "dmaaw", "mdao": "mdaaw",   # 隱瞞事情
    "spngao": "spngaw",              # 我們來抽籤; -ao is -aw word-finally
    # frozen
    "dmbasyaq": "dmbasyaq",          # beside dmt'basyaq>dmtbasyaq
    "siba": "siba",                  # 草坪（日語詞）-- Japanese 芝
}
# refuse to write anything lexical_map.json has already vetoed -- the b57 lesson:
# adjudicated = (manual|llm) - lex_block, so a null there silently discards the key
lex = json.load(io.open(H + "lexical_map.json", encoding="utf-8"))
blocked = sorted(k for k in FIX if k in lex and not lex[k])
if blocked:
    print("!! lex_block would discard these -- withdrawing: %s" % blocked)
    for k in blocked:
        FIX.pop(k)

p = H + "manual_map.json"
d = json.load(io.open(p, encoding="utf-8"))
before = len(d)
clash = {k: (d[k], v) for k, v in FIX.items() if k in d and d[k] != v}
if clash:
    print("overriding %d earlier manual keys:" % len(clash))
    for k, (o, n) in sorted(clash.items()):
        print("   %-12s %s -> %s" % (k, o, n))
d.update(FIX)
body = ",".join("%s:%s" % (json.dumps(k, ensure_ascii=False),
                           json.dumps(v, ensure_ascii=False))
                for k, v in sorted(d.items()))
io.open(p, "w", encoding="utf-8", newline="\n").write("{\n" + body + "\n}\n")
print("manual_map %d -> %d  (batch touches %d keys)" % (before, len(d), len(FIX)))
