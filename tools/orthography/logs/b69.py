"""Batch 69: seven greens, found by generate-and-test instead of by distance --
and one clearance from batch 67 retracted, because it failed on a character
variant rather than on absence.

Two new detectors, both built on the batch 68 finding that his orthography is
partly KNOWN rather than merely close:

green_rule  expands each green through every combination of the correspondences
            his shipped, human-checked keys demonstrate -- x>h and x>x, l>r and
            keep-l, o>u, -ao>-aw, n>ng, y>i, apostrophe-schwa, and the final
            velar he drops -- and keeps only expansions that are ATTESTED modern
            words. A hit is then not "near" a modern word; it IS one, reached by
            rules he follows. 262 greens in, 17 out, 4 of them right.
green_uni   green_gloss's gloss index rebuilt on single characters carried by at
            most 12 spoken words. The bigram index cannot match 帳篷 against
            帳棚 or 鍋 against 锅, and that blind spot had already cost a
            clearance. One shared character is weak evidence only when the
            character is common; 篷, 糯, 屎, 獠 are not.

KINAL -> kingal 一 spk 1626. His own dictionary settles it: he writes kingal
   dozens of times (BALAE, BAXANG, BENGBANG, BETAK, BI...), already shipped on
   identity, and kinal exactly once -- Dsi ko kinal boxo taai mo 拿一枚錢幣來給我
   看看. One word, two spellings, and the difference is the n/ng of batch 68.

QABAN -> qabang spk 43. Same shape. He writes qabang seven times (Lbongi bi
   qabang 用毯子把它蓋上; Snpsalun mo ka qabang xxelao 我要把被子摺成雙層來蓋), and
   qaban once, in 你的被單（被子）又全濕了. pqabang 蓋毯子 spk 4 confirms the sense
   against the bare gloss 包. The dropped final velar, as x'li>hrig.

DMTABU -> dmtabug 餵養的人(複數) spk 0. Ga ino ka dmtabu kui? 養蠶的人在哪裡 --
   the people who raise silkworms. The modern word is glossed 餵養的人(複數),
   his phrase word for word, and the root is solid: tabug 飼養, tmabug 去餵食
   spk 26, mtabug 牧師 spk 26. Dropped final velar again, and the dm- plural
   agent prefix is theirs too.

TLOON -> tluung 坐 spk 125. Ya xmuya so bi mx'dyeq tloon kddiyax! 你為什麼老是
   獨自坐在一旁（退到一邊）呢 -- his sentence names the meaning. His oo for their
   uu, and the only rival shape, tlung 打 spk 1, is not it.

KOOBU -> kowbu 帳棚 spk 6. THIS RETRACTS A BATCH 67 CLEARANCE. That note says
   "the omnibus has no word glossed 帳篷 or 遮蔽 at all". It has kowbu 帳棚 spk 6
   and pkbuan 搭帳棚 -- I searched with 篷 and the dictionary writes 棚. The
   clearance was a character variant, not an absence, and the same fault had
   already made 鍋 return zero when I typed the simplified codepoint. His oo for
   their ow, as in his own KOOBU note: 只是把一條毯子往幾根樹枝上一搭而成 -- and
   pqbangi 讓…搭帳棚 puts the blanket root in the same frame.

L'XQOI -> dhquy 糯米 spk 3. The highest-value green left, 5 occurrences across
   three cards: 一種稻米，煮熟後變得黏糯 / 一種糯米品種, Payai l'xqoi 一種糯稻,
   Ptkanun so knuwan ka payai so l'xqoi 什麼時候要把你的糯米去殼. The modern word is
   dhquy 糯米 with a family behind it -- mgdhquy 像糯米, gmndhquy 專門割糯米,
   ddhquy 那些糯米. Under his own conventions his word is lhquy: apostrophe-schwa,
   x>h, o>u, i>y. One initial letter separates them, and d~l alternation is
   already in this dictionary -- batch 67's sl'dan rested on the modern root
   alternating sdlut/slut. green_near had flagged l'xqoi as a coincidence because
   it matched 不容易 on shape; searching the meaning finds the rice.

XG'XO -> hghug 水井 spk 0. His gloss carries his own question marks -- 泉源（？）
   －水塘（？）-- and the shape is exact under two established rules: x>h twice,
   o>u, plus the final velar he drops. hghu + g. The root is real and it is about
   getting water: tmhghug 專門打水, tmnhghug 打水過, smhhghug 很需要水井, tnhghug
   捲線的人 (the same root also winds thread). A well is not a spring, which is
   why his (？) matters: he was unsure what he had, and the word he wrote is one
   modern Truku still uses.

HELD, with the evidence, because a real word is not yet the right word:

BIRI -- two cards, one key, and a 2:2 tie. His BIRI is 最後的 (Biri bi ka yako
   我真的是最後一個) on one card and 濕透－浸濕 (Biri kana lukus mo 我的衣服全都濕透
   了) on another. The modern bili 很濕 spk 10 is the second card exactly, his r
   for their l. The first card has no candidate -- hili 最小的、老么 is not within
   reach of his shape. Two slots each: taking bili would fix two and make two
   positively wrong, replacing an honest green with a false assertion. The
   homograph rule sends the key to the bigger card and there is no bigger card.

TYAQONG -- shape says yes and gloss says no. cyaqung 烏鴉 spk 4 is two letters
   from his TYAQONG and carries a whole family (encyaqung 本來是烏鴉, dmptcyaqung
   專門抓烏鴉的人, stcyaqung 有烏鴉味). But he wrote 雉雞（山雞）on both of his
   TYAQONG cards, and a crow is not a pheasant. The modern pheasant is glaqung
   藍腹鷴 spk 14, nowhere near his shape.

TMAGO / MTMAGO -- gloss says yes and shape says no. His 自負的－驕傲的－高傲的 is
   dahu 自誇、自傲 spk 26 word for word, and his tm- prefix is theirs: tmdahu
   稱讚 spk 53. But his g for their h is not a correspondence anything else in
   this dictionary supports -- his h is written x throughout (xg'xo, x'li,
   xubao). One unestablished rule is one too many.

GLAQON -- the rule sweep's false positive, worth recording. glaqung 藍腹鷴 spk 14
   is one dropped velar from his glaqon, and his sentence is Klxangi bi aadi na
   glaqon lqlit ka milit so 千萬小心，別讓雲豹抓走你的山羊 -- glaqon is what the
   clouded leopard does to the goat, not a pheasant. Attestation plus a regular
   correspondence is still not enough on its own; the sentence decides.

'MU -- likewise. mu 我 spk 3047 is what charRules already prints for his 'mu, and
   it is the wrong word: his "MU card is 極細的粉－細塵, and "mu basao is BASAO 之粉.
   Modern 粉 candidates (amung 粉狀 spk 2, udung 麵粉 spk 1) are not near his
   shape. It stays green, which is the honest answer for all 6 occurrences.

Cleared as ABSENT on a corrected search: mskoto 麻木－起雞皮疙瘩－凍僵 (searching
   疙瘩/麻木/凍 returns mgmirit 麻木不仁, ptghuda 因下雪而凍死, shdaanay -- none
   within reach of MSKUTU), teumuk 首領－負責人 (modern is thowlang 王、領袖或頭目
   spk 457 and the bukung family, kkbukung 成為…首領; neither is his shape).
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # his n for their ng, and his own pages spell it kingal dozens of times
    "kinal": "kingal",     # WAS green;  kingal 一個；一頂 spk 1626
    # dropped final velar; he writes qabang 7x elsewhere, already id-mapped
    "qaban": "qabang",     # WAS green;  qabang spk 43, pqabang 蓋毯子 spk 4
    # dropped final velar; 養蠶的人 against 餵養的人(複數), word for word
    "dmtabu": "dmtabug",   # WAS green;  root tabug 飼養, tmabug 去餵食 spk 26
    # his oo for their uu; his sentence is 獨自坐在一旁
    "tloon": "tluung",     # WAS green;  tluung 坐;坐下 spk 125
    # his oo for their ow -- and this RETRACTS the batch 67 clearance of koobu,
    # which searched 帳篷 against a dictionary that writes 帳棚
    "koobu": "kowbu",      # WAS green;  kowbu 帳棚 spk 6, pkbuan 搭帳棚
    # apostrophe-schwa + x>h + o>u + i>y gives lhquy; d~l as in sdlut/slut
    "l'xqoi": "dhquy",     # WAS green 5x;  dhquy 糯米 spk 3, mgdhquy 像糯米
    # x>h twice, o>u, plus the final velar he drops: hghu + g
    "xg'xo": "hghug",      # WAS green;  hghug 水井, tmhghug 專門打水
}

LEXNULL = {}

NOTES = {
    "_green_rule": (
        "GREEN_RULE and GREEN_UNI, the two detectors written for batch 69, and why "
        "they beat everything before them. Every earlier sweep ranked candidates by "
        "edit distance or gloss overlap, and both rank string coincidences (nta "
        "against 他的, l'xqoi against 不容易) alongside real matches. green_rule "
        "inverts it: his orthography is partly KNOWN, because each correspondence "
        "below is carried by keys already shipped and human-checked -- x>h and x>x "
        "(modern Truku keeps x: uxul 暖和, sxlay), l>r and the 28-token keep-l "
        "guard, o>u, -ao>-aw (longao>lungaw, niyao>ngiyaw), n>ng (NYAO/NIYAO>"
        "ngiyaw, batch 68), y>i (pusyaq>pusiq), apostrophe-schwa, and the final "
        "velar he drops (x'li>hrig, ayo>ayug). Expand each green through every "
        "combination and keep only expansions that are ATTESTED. 262 greens in, 17 "
        "out, 4 right -- and the failures are informative rather than noisy, "
        "because each one is a real modern word his sentence refuses (glaqon, 'mu). "
        "green_uni rebuilt green_gloss's index on single characters carried by at "
        "most 12 spoken words: a bigram index cannot match 帳篷 to 帳棚, and that "
        "blind spot had already cost the koobu clearance."
    ),
    "_koobu": (
        "KOOBU 帳篷 -- CLEARED AS ABSENT IN BATCH 67, WRONGLY, AND CONVERTED IN "
        "BATCH 69 TO kowbu 帳棚 spk 6. The batch 67 note says the omnibus has no "
        "word glossed 帳篷 or 遮蔽 at all. It has kowbu 帳棚 and pkbuan 搭帳棚; I "
        "searched with 篷 and this dictionary writes 棚. The same fault had already "
        "made 鍋 return zero when I typed the simplified codepoint U+9505 at a "
        "traditional-character corpus, and 舔 return zero for U+8202. An absence "
        "proved with one spelling of one character is not an absence. His oo is "
        "their ow, and his own note describes the thing they name -- 只是把一條毯子"
        "往幾根樹枝上一搭而成 -- while pqbangi 讓…搭帳棚 puts the blanket root in the "
        "same frame. Rule: clearances are only as good as the character variants "
        "searched; prefer his gloss's own characters over any I type."
    ),
    "_l'xqoi": (
        "L'XQOI 糯米, 5 occurrences across three cards -- the highest-value green "
        "converted so far. Batch 69: l'xqoi>dhquy 糯米 spk 3, with mgdhquy 像糯米, "
        "gmndhquy 專門割糯米 and ddhquy 那些糯米 behind it. His cards are 一種稻米，"
        "煮熟後變得黏糯 and 一種糯米品種, his examples Payai l'xqoi 一種糯稻 and "
        "Ptkanun so knuwan ka payai so l'xqoi 什麼時候要把你的糯米去殼. Under his own "
        "conventions his word is lhquy -- apostrophe-schwa, x>h, o>u, i>y -- and one "
        "initial letter separates it from theirs. d~l alternation is already in this "
        "dictionary: batch 67's sl'dan>sltan rested on the modern root alternating "
        "sdlut/slut. green_near had dismissed l'xqoi as a coincidence because on "
        "SHAPE it matched 不容易; searching the MEANING found the rice. That is the "
        "whole argument for gloss-first search in one word."
    ),
    "_biri": (
        "BIRI -- HELD in batch 69, a 2:2 homograph tie with no bigger card. His BIRI "
        "is 最後的 on one card (Biri bi ka yako 我真的是最後一個) and 濕透－浸濕 on "
        "another (Mnda ko pskoyoc muda 'lu, Biri kana lukus mo 我在路上遇到雨,我的"
        "衣服全都濕透了). The modern bili 很濕 spk 10 IS the second card, his r for "
        "their l. The first has no candidate: hili 最小的、老么 is not within reach. "
        "Two slots each, so taking bili would fix two and make two positively wrong "
        "-- replacing an honest green with a false assertion. The homograph rule "
        "sends the key to the bigger card (pai 11:1, kyoxan 6:3, mnsa 48:4) and "
        "there is no bigger card here. Same family as lawa and luus: do not make "
        "the losing side wrong."
    ),
    "_tyaqong": (
        "TYAQONG 雉雞（山雞）-- HELD in batch 69. Shape says yes and gloss says no. "
        "cyaqung 烏鴉 spk 4 is two letters from his word and carries a real family "
        "(encyaqung 本來是烏鴉, dmptcyaqung 專門抓烏鴉的人, stcyaqung 有烏鴉味, "
        "empcyaqung 烏鴉將要). But he wrote 雉雞 on BOTH of his TYAQONG cards, and a "
        "crow is not a pheasant. The modern pheasant is glaqung 藍腹鷴 spk 14, "
        "nowhere near his shape, and no modern word is glossed 雉雞 or 山雞 at all. "
        "Revisit only if his French original turns out to say corbeau."
    ),
    "_tmago": (
        "TMAGO / MTMAGO 自負的－驕傲的－高傲的－傲慢的 -- HELD in batch 69, the "
        "mirror of TYAQONG: gloss says yes and shape says no. dahu 自誇、自傲 spk 26 "
        "is his gloss word for word, and his tm- prefix is theirs (tmdahu 稱讚 spk "
        "53, tndahu, stndahu 誇獎). But it needs his g to be their h, and that is "
        "not a correspondence anything else supports -- his h is written x "
        "throughout (x'li>hrig, xubao/xbagun>hbagun, xg'xo>hghug in this batch). "
        "One unestablished rule is one too many."
    ),
    "_glaqon": (
        "GLAQON -- green_rule's instructive false positive, batch 69. glaqung 藍腹鷴"
        "（飛禽名）spk 14 is exactly one dropped final velar from his glaqon, which "
        "is the correspondence that produced qaban>qabang and dmtabu>dmtabug in the "
        "same batch. And it is wrong: his sentence is Klxangi bi aadi na glaqon "
        "lqlit ka milit so 千萬小心，別讓雲豹抓走你的山羊 -- glaqon is what the clouded "
        "leopard does to the goat. Attestation plus a regular correspondence is not "
        "enough by itself; the sentence decides. Recorded so the next sweep that "
        "surfaces it does not have to re-derive the refusal. 'mu is the same story: "
        "charRules already prints MU, mu 我 spk 3047 is a real word, and his \"MU is "
        "極細的粉－細塵 (\"mu basao = BASAO 之粉). It stays green for all 6 slots."
    ),
    "_green_residue3": (
        "GREEN RESIDUE, third pass (batch 69), cleared on a CORRECTED search: mskoto "
        "麻木－起雞皮疙瘩－凍僵 (searching 疙瘩, 麻木 and 凍 returns mgmirit 麻木不仁, "
        "ptghuda 因下雪而凍死 and shdaanay 別使…凍著; none is within reach of MSKUTU, "
        "and his own LIMA example 雖然我蓋了五條被子,還是起雞皮疙瘩 gives no other "
        "handle), teumuk 首領－負責人－小王 (modern is thowlang 王、領袖或頭目 spk 457 "
        "and the bukung family -- kkbukung 成為…首領, emptbukung 首領的人 -- neither "
        "anywhere near his shape). Both were on the deferred list and are now closed."
    ),
}

lex = json.load(io.open(H + "lexical_map.json", encoding="utf-8"))
lex.update(NOTES)
lex.update(LEXNULL)
json.dump(lex, io.open(H + "lexical_map.json", "w", encoding="utf-8", newline="\n"),
          ensure_ascii=False, indent=1)
print("lexical_map: %d notes + %d nulls written (%d keys)"
      % (len(NOTES), len(LEXNULL), len(lex)))

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
