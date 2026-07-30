"""Batch 62: three cards where the BROWN was wrong, not the green.

This batch came out of adding one column to the half-brown report -- not "is this
key mapped" but "is the value it was given a real modern word, and does it mean
what his card means". Three cards failed that immediately, and they had been
sitting brown, i.e. claiming to be verified, the whole time.

S'LUT 黏附 -- six keys, and every one of them was pointed at the wrong root.
   s'lut, slut  -> slut   剛開始肥  "just starting to get fat"
   ms'lut,mslut -> msrut  刀鋒鈍了  "the blade has gone blunt"
   ps'lut,pslut -> psrut  很不鋒利  "very blunt"
   Not one of those has anything to do with adhesion. They are shape matches on a
   card whose own examples are a chicken coop too close to the kitchen, a house
   stuck onto a cliff, a bathroom joined to the main house, and glutinous rice
   cake sticking to your hands. The real root is dlut, and it is a whole
   paradigm: dlut 黏, sdlut 黏上 (spk 2), msdlut 黏上, psdlut 使…黏住,
   tgsdlut 最黏著, smdlut 依靠著, tmnsdlut 電焊. His ps'lut 使黏附於 and modern
   psdlut 使…黏住 are the same gloss word for word.
   His own headword confesses the root: "S'LUT (= R. ? - R. = LUT ?)", and his
   separate LUT card says 黏附－用以黏附。（詞根＝LUT？－＝LöT？－＝S'LUT？）-- he
   is asking whether LUT and S'LUT are one word. They are, and the answer is
   dlut, which is why bare slut and prefixed s'lut can take the same value.
   Not written: Sl'dan 黏附；被黏合之物 (green x2). Modern sltan 被黏著 and
   sltani 被黏著 (spk 2 each) are the right gloss and the right slot, but his d
   against their t is a consonant he wrote and they do not, and this card has
   just shown what happens when a shape is trusted over a gloss. Held, named.

TABE 犁 -- his own card gives the answer in its first line: 犁（同義詞＝SAKOL）.
   Modern has exactly one plough word, sakur 犁 (spk 4) with psakur 犁田 (spk 4),
   msakur, spsakur -- and sakur is ALREADY the value of his own saqol, psakur of
   his psaqol. So this is the tbako>lumak move: his TABE is a word that did not
   survive (tabe, tabi, ptabe, ptabi are absent from every corpus), the language
   kept the synonym he himself names, and his two attested slots take it.
   His ptabe 犁田－使用犁 and modern psakur 犁田 are the same gloss.
   NOT touched, and this is the honest ugly part: the card's other six slots
   (tbian/tbiyan 可以犁田的地方, tnbiyan 犁過的田, tbiun/tbiyun, tbii, ptbian,
   ptbiun, ptbii) keep their current values, so the headword changes lexically
   while its own derivatives do not. Those values are regular respellings of his
   shapes (his -ia- > modern -iya-), which is a real rule here; they are not
   claims that the modern word means 犁, and the locative/irrealis of sakur
   (skuran, skurun, snakur, skuri) is attested nowhere. Recorded as an open
   inconsistency rather than papered over with four invented forms. Note also
   that modern tbiyan happens to mean 下來 -- an accident of shape, not evidence.

TA'TO / T"TO 切割 -- reversing a lexical_map null, with the reason.
   ttuun / ttuon / ttuan / t"tuan have been claimed twice (b48, b49) and reverted
   twice, and the standing note gives a good reason: the modern root looked like
   teetu, whose own derived slots (steetu 上坡, steetuan 上坡路) turned out to be
   the uphill homonym, so only knttuun 1x and sttuan 3x were on record and a bare
   geminate tt- form would have been my construction.
   What that note never saw is ttui 切、剁 -- a BARE geminate cut form, in the
   omnibus, spk 2, with his exact gloss, filling his exact slot: his own example
   is "Ttui xei lodoç" 你把雞（肉）切開. The map already ships ttui>ttui as brown.
   So the map has been asserting the geminate cut stem in the imperative while
   nulling it in the -un and -an, which cannot both be right. With ttui bare,
   sttuan 3x for the -an and knttuun 1x for the -un, the paradigm is on record.
   And these four keys ALREADY RENDER CORRECTLY -- charRules strips his mark and
   folds o>u, so t"tuan and ttuon print TTUAN and TTUUN with or without a map
   entry. Nothing on the page moves. The only thing that changes is the colour,
   from "unverified" to "verified", which is now the true statement.

KSIA -- mksia 變成水—液化 had the blind mqsiya, while msqsiya 溶化成水（液體）
   spk 4 is attested, is his gloss word for word, and is already the value of his
   own msksia. Well formed is not attested; this replaces one with the other.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # S'LUT / LUT: the dlut root, replacing "getting fat" and "blunt blade"
    "s'lut": "sdlut",     # WAS slut 剛開始肥;  sdlut 黏上 spk 2
    "slut": "sdlut",      # WAS slut;  his LUT card, same word, his own 詞根＝S'LUT？
    "ms'lut": "msdlut",   # WAS msrut 刀鋒鈍了;  msdlut 黏上
    "mslut": "msdlut",    # WAS msrut
    "ps'lut": "psdlut",   # WAS psrut 很不鋒利;  psdlut 使…黏住 = his 使黏附於
    "pslut": "psdlut",    # WAS psrut
    # TABE: the synonym his own headword names
    "tabe": "sakur",      # 犁 spk 4; already the value of his saqol
    "ptabe": "psakur",    # 犁田 spk 4 = his 犁田－使用犁; already his psaqol's
    # the geminate cut stem, unblocked -- see the docstring and _ttuun
    "ttuun": "ttuun",     # knttuun 1x; renders identically either way
    "ttuon": "ttuun",     # his -on = modern -un throughout
    "ttuan": "ttuan",     # sttuan 3x
    "t'tuan": "ttuan",    # his T"tuan 切成的塊, the same form with his mark
    # KSIA: attested beats well formed
    "mksia": "msqsiya",   # WAS mqsiya (blind); 溶化成水（液體）spk 4
}

# --- the veto, and the deliberate lifting of three of them -------------------
UNBLOCK = {"ttuun", "ttuon", "t'tuan"}
NOTE = (
    "TA'TO / T\"TO, to cut. NULL LIFTED, batch 62. The reason for the null was "
    "that the modern root looked like teetu, whose own derived slots turned out "
    "to be the uphill homonym (steetu 9x 上坡, steetuan 上坡路), leaving only "
    "knttuun 1x and sttuan 3x on record -- so a bare geminate tt- form would have "
    "been a construction, and it was claimed and reverted twice (b48 ttuun, b49 "
    "t'tuan). What that reasoning never had in front of it is ttui 切、剁, "
    "omnibus, spk 2: a BARE geminate cut form, his exact gloss, his exact slot "
    "(\"Ttui xei lodoç\" 你把雞（肉）切開), and already shipped brown as ttui>ttui. "
    "The map was asserting the geminate stem in the imperative while nulling it "
    "in the -un and -an. With ttui bare, sttuan 3x for the -an and knttuun 1x for "
    "the -un, the paradigm is on record and the null is no longer the honest "
    "position. Note that all four keys render identically with or without a map "
    "entry -- charRules strips his mark and folds o>u -- so this changes the "
    "colour, not the page."
)

lex = json.load(io.open(H + "lexical_map.json", encoding="utf-8"))
lifted = sorted(k for k in UNBLOCK if k in lex and not lex[k])
for k in lifted:
    del lex[k]
lex["_ttuun"] = NOTE
lex["_tabe"] = (
    "TABE, the ard-plough. His first line names the answer -- 犁（同義詞＝SAKOL）"
    "-- and modern has exactly one plough word: sakur 犁 spk 4, psakur 犁田 spk 4, "
    "msakur, spsakur. His own shape did not survive (tabe, tabi, ptabe, ptabi are "
    "absent from every corpus), so tabe>sakur and ptabe>psakur are the tbako>lumak "
    "move, and both values are already what his own saqol and psaqol point at. "
    "OPEN, deliberately: the card's other slots (tbian/tbiyan, tnbiyan, tbiun, "
    "tbii, ptbian, ptbiun, ptbii) keep the regular respellings of HIS shapes, "
    "because the locative and irrealis of sakur -- skuran, skurun, snakur, skuri "
    "-- are attested nowhere, and four invented forms would be a worse lie than "
    "an uneven card. Modern tbiyan 下來 is a shape accident, not evidence."
)
json.dump(lex, io.open(H + "lexical_map.json", "w", encoding="utf-8", newline="\n"),
          ensure_ascii=False, indent=1)
print("lexical_map: lifted %s; notes _ttuun,_tabe written (%d keys)"
      % (lifted, len(lex)))

still = sorted(k for k in FIX if k in lex and not lex[k])
if still:
    print("!! lex_block would discard these -- withdrawing: %s" % still)
    for k in still:
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
