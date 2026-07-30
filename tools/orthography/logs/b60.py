"""Batch 60: word-final -ao, the brown half.

The charRules edit in this session settled the GREEN half -- an unmapped token
ending -ao now prints -aw instead of the -au the o>u rule was producing. That fix
also exposed the brown half, because after it exactly ONE span in all 1,967 cards
still ended -au, and it was brown: `psqrasau`. A brown claim is a stated one, so
charRules cannot reach it; only the map can.

THE MEASUREMENT that turns one span into a class. Across 38,687 modern types:
   -aw   2,406 types  12,163 spoken tokens
   -au       4 types       13 spoken tokens
   -ao       1 type         2 spoken tokens   (dhdahao)
Word-final -ao is not a shape this orthography writes. Yet of the 284 mapped keys
ending -ao, 271 give -aw and 13 do not -- and seven of those 13 are IDENTITY
claims, i.e. brown assertions that this word is the one place Truku does it. Two
of the 13 earn their exception and are deliberately left alone: `nnamao`>nnamu
(namu 你們的 12x, a genuine -u word) and `q'nao`>qusul (the tier-X substitution).
The other eleven are here, plus one green that falls out of the same card.

Every entry below except `pbbagi` is a CORRECTION of a shipped value, so each
needs the old value shown wrong as well as the new one priced.

QALAS -- his line is a hortative and the family is solidly qras:
   "N'xali! Psqlasao ta tityex ka dpnax isil alang" 快！我們來稍微款待…（外人）
`ta` is the 1pl.incl the hortative takes, exactly as in SM"LU's Spngao ta (b59).
qrasun 79x, qrasan 55x, qrasi 13x, qrason 6x, pqrasi 4x, psqrasun 1x -- and the
-aw hortative is attested IN THIS FAMILY: qrasaw spk 1, pdqrasaw 出面, drasaw,
brasaw, tdrasaw. psqrasau was right about the stem and wrong about one letter.

SAPOX -- the same construction, and the current value is in the wrong SLOT:
   "Ida bi mnqan sapox ka Sikat !PSpoxao ta n'xali da!" 快！我們趕緊去讓她就醫
`pspuhan` 醫院 is a locative noun -- and it is already the value of his own
`pspoxan` on the same card, so two different slots were landing on one word. The
paradigm is fully productive around it (spuhi, spuhun, spuhan, pspuhun, pspuhi,
pnspuhan), and -aw is the slot his -ao occupies in it.

KSOLOÇ -- `ssino` keeps his o, which no modern word ends in, and is 0x anywhere:
   "Mntöting pax aso ka mptksoloç ssinao daxa slaxo" 漁夫們下了船去洗他們的網
sinaw 洗;清潔 137x, sminaw 洗 81x, msinaw 洗 8x. (The same shape also carries a
liquor sense -- empsinaw 釀酒的人, ksinaw 好酒, ptgsinaw 因酒而死 -- which is a
homonym, not a rival reading: nothing on this card is about drink.)

LB'NAO -- the b-spellings sit INSIDE the Mlb'nao sub-form's own example
(我來在你面前撒嬌), so they are that sub-form written twice, and the head's value
is already mrbnaw. rbnaw 嬰孩 spk 72, mnrbnaw 向…撒嬌 1x, srbnaw 撒嬌的原因 2x,
embrbnaw 嫩嫩的 -- his gloss word for word. Same move as b58's Qnqogo (knqogo):
the parenthetical takes the head's value.

BUBAO -- the root loses a segment in his spelling, the documented TABU>tabug /
"LU>elug class, and his own suffixed forms already gave it away: bbagun>bgbagun
is SHIPPED. bgbaw 要剝開 2x, embgbaw 裂開, bgbagi 讓它剝開 2x, bgbagon 2x. His
paradigm bubao / Pbbagi / bbagun is the modern bgbaw ~ bgbag- alternation, and
his doubled initial is the reduplication modern writes with the consonant copy
(batch 20's finding). pbubao/pbbagi are regular p- causatives on that stem.

QL'XAO -- HIS OWN TAG asks "Serait ce une variante de QLAAO ?", qlaao>kraaw sits
on the same card, and the omnibus answers with the gloss: mkraaw 涉水而過 spk 4
against his Mql'xao 涉水穿越溪流. Two independent lines agreeing. The current
qlxao/mqlxao keeps his l AND his x AND his -ao and is wrong on all three.

KALIP -- the smallest claim here, and made as small as possible on purpose. His
own line pairs the two forms: "Ma mdludao (mludao) kana ka tunux so!" 你的頭髮真
是亂蓬蓬的 -- and the map gave the two sides of one labelled pair DIFFERENT values
(mdrudu vs mrudaw), one of them blind and ending -u. Unify on the shipped, attested
side rather than invent mdrudaw. Recorded, not acted on: mrrudaw 混亂 fits 亂蓬蓬
better than mrudaw 拆毀者 does, but changing that would be a second claim about a
key this batch is not otherwise touching.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # the hortatives -- his -ao slot, in two families that show it
    "psqlasao": "psqrasaw",   # WAS psqrasau, the last -au on the page
    "pspoxao": "pspuhaw",     # WAS pspuhan 醫院, a locative noun in a hortative slot
    # the o that cannot end a word
    "ssinao": "ssinaw",       # WAS ssino; sinaw 洗;清潔 137x
    # the parenthetical takes the head's value
    "mlb'bao": "mrbnaw",      # WAS mlbbao; = his own Mlb'nao
    "nplb'bao": "nprbnaw",    # WAS nplbbao
    # the root loses a segment; bbagun>bgbagun already shipped
    "bubao": "bgbaw",         # WAS bubao (identity); 要剝開 2x
    "mbubao": "embgbaw",      # WAS embubao; 裂開
    "pbubao": "pbgbaw",       # WAS pbubao (identity)
    "pbbagi": "pbgbagi",      # green; bgbagi 讓它剝開 2x
    # his own tag names the variant, the omnibus names the gloss
    "mql'xao": "mkraaw",      # WAS mqlxao; 涉水而過 4x
    "ql'xao": "kraaw",        # WAS qlxao; = his own QLAAO
    # make his labelled pair agree with itself
    "mdludao": "mrudaw",      # WAS mdrudu; mludao>mrudaw on the same line
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
