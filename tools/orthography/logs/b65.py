"""Batch 65: audit4 rows 4-140, and the second-biggest find of the review.

The detector's precision falls as the outlier count rises -- a card with one
dissenting slot is a strong signal, a card with three or four usually just means
the majority substring came from a syncopated -an stem, so the bare roots look
like outliers. Rows 0-34 (one outlier) gave four writes in batch 64 and three
here; rows 34-140 (two to four outliers) gave one, and it is the big one.

MNSA 53x -- the past of GO, sitting on the modern past of SAY.
   His MNSA is a sub of his USA card, glossed 已去過, and the dictionary uses it
   that way throughout: Mnsa ko mali timu 我去買了鹽, Mnsa ko bbuyo 我到森林裡去,
   Mnsa ko mkt'lo 我去了那裡三天, Mnsa ko mlata 我去當兵時.
   The shipped value mnsa is 如此說…。at spk 72 -- mn- + msa 說, the past of SAY,
   which in modern Truku is exactly that shape. His own msa>msa 他這樣說的 is
   already shipped for the say verb, so the two verbs are distinct in his
   dictionary and collide in the modern one.
   mnsa -> mnusa 去過 spk 21, and his mnusa>mnusa was ALREADY shipped -- the same
   self-contradiction as pax/pnax: the map accepted the go-form for the full
   spelling and left his contracted spelling on a different verb.
   HOMOGRAPH, measured rather than asserted: all 53 slots were classified by
   gloss. 48 are unambiguously GO, 3 are SAY (LAXOL 對人群說, MSA 我昨天說了,
   XOAI 我對母親說), 1 has both words (QELI 我到…去宣布), 1 is neither (ULUS,
   where mnsa is inside a longer narrative clause). 48 against 4. Same call as
   pai (11 grandmother slots against 1 carry) in batch 63 and kyoxan (6 against
   3) in batch 64, and by a much wider margin.

PSLOON -- his 該挨打的－將要挨打的人, on his PS'LO card.
   The card ships psru 打（用手打）, msru 打, empsru 要打, psruan. Only the -un
   slot walked off, to psluun 蒸, to steam. All three of its slots are the beating
   sense, including the XANGAN example 我會再處罰你. psruun is blind, but it is
   the regular -un form of a root the card is built on, and his psloan>psruan is
   the equally blind -an form already shipped.

SDXALAN -- his 椅背－扶手－倚靠處－支撐物, on his SDAXAL card.
   The card ships sdahar 依靠著… spk 6, psdahar 使…靠著 spk 4, dahar 靠著. The
   value was the IDENTITY sdxalan, which the omnibus glosses 很髒 -- a soil word,
   nothing to do with leaning. All three slots are the backrest sense (你的椅子有
   椅背嗎？/ 沒有可以倚靠的地方). sdharan is sdahar with the regular -an syncope,
   the same alternation the corpus shows in durux>drxan.

PK'LU -- his 當…的時候, on his "LU card.
   Not a wrong word so much as the wrong spelling of one: the card is elug/
   peelug/meelug/gmeelug, all with the g, and only this slot lost it, to pklu
   剛好 spk 2. pklug 正好;正時 spk 34 is the same sense, seventeen times more
   attested, and consistent with every other slot on the card. 正時 is his 當…的
   時候 exactly.

Cleared on inspection -- the value is right and audit4 was reading the wrong card:
   l'pi   10 slots and he has TWO L'PI headwords -- 關！（命令語氣）and 穀糠－穀穗
          －穗上不含穀粒的部分. The value lpi 無米粒的稻穀 is the second one, word
          for word. Four slots each way; the shipped value serves one card
          exactly, which is the best a flat map can do. _l'pi.
   tmquli 4 slots, and three of them are his QULI/TQULI cards -- 領養一個孩子,
          撫養. The value tmquli 撫養 is exactly right. Only his TKULI sub is the
          pour sense, and he wrote it "Tmkuli (Tmquli ?)", querying it himself.
   g'loq  CLOSED from the long-standing deferred list ("split families ... G'LOQ").
          audit4 flagged three LOQ slots as outliers against the ruq majority, but
          his xmgloq 出鞘 is already shipped hmgluq 抽;拔 -- an exact match -- so
          the gluq root is genuinely his and 污垢 is a homophone row. The card
          simply holds two families, LOQ and G'LOQ, and both are mapped right.
   klagan his KALAO 攀登. Modern has two homophonous karaw families -- climb
          (karaw 爬;越, blind) and clean/tidy (kmaraw 清理 spk 44, kragan 整理).
          The -an form of the climb one has the same shape, so the string is
          right and only the omnibus gloss belongs to the other family.
   x'mlo  hmru is the m-infix of hru, exactly his 動詞形; 水源 is a homophone.
   kala   mgkala/pgkala prove the bare root is kala; 「來」的詞根 is another word.
   And the bulk of rows 34-140, where the value is simply correct and fails a
   substring test by accident: tqian 睡覺的地方, kdagan 擔架, hmaan 種植, thiyan
   和…在一起, hurit 挽留, uqun 吃, biqan 給, hyaan/dhyaan 他/他們, nhdaan 結束,
   smnguhi 忘記, knskiyan 冷得, qtaan 看, ksgun 害怕, ssagan 被遮住, klwaan 國家.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # MNSA: the past of GO, which the map already knew as his mnusa
    "mnsa": "mnusa",       # WAS mnsa 如此說…。spk 72 (past of SAY);  mnusa 去過 spk 21
    # PS'LO: the -un slot of the beating root the card is built on
    "psloon": "psruun",    # WAS psluun 蒸;  psru 打 spk 0/msru 打 spk 1, cf. psruan
    # SDAXAL: the -an form of the leaning root
    "sdxalan": "sdharan",  # WAS sdxalan (identity) 很髒;  sdahar 依靠著… spk 6
    # "LU: the same word, with the g every other slot on the card keeps
    "pk'lu": "pklug",      # WAS pklu 剛好 spk 2;  pklug 正好;正時 spk 34
}

NOTES = {
    "_mnsa": (
        "MNSA 已去過, 53x -- the second-biggest find of the review after pax. Batch "
        "65: mnsa>mnusa. The shipped value mnsa is 如此說…。spk 72, mn- + msa 說, "
        "the past of SAY, which in modern Truku has exactly his spelling; his own "
        "msa>msa 他這樣說的 is already shipped for that verb. His MNSA is a sub of "
        "his USA card glossed 已去過 and the dictionary uses it that way throughout "
        "(Mnsa ko mali timu 我去買了鹽, Mnsa ko bbuyo 我到森林裡去, Mnsa ko mkt'lo "
        "我去了那裡三天). His mnusa>mnusa 去過 spk 21 was ALREADY shipped, so this is "
        "the pax/pnax signature again -- the map took the go-form for the full "
        "spelling and left the contracted one on a different verb. HOMOGRAPH, "
        "MEASURED: all 53 slots classified by gloss give 48 GO, 3 SAY (LAXOL, MSA, "
        "XOAI), 1 both (QELI 我到…去宣布), 1 neither (ULUS). 48 against 4 -- a wider "
        "margin than pai or kyoxan. The four are the cost and this note is the "
        "record of it."
    ),
    "_psloon": (
        "PSLOON 該挨打的－將要挨打的人. Batch 65: psloon>psruun, off psluun 蒸 (to "
        "steam). His PS'LO card ships psru 打（用手打）, msru 打 spk 1, empsru 要打 "
        "and psruan, and all three of psloon's slots are the beating sense "
        "(including XANGAN 我會再處罰你). psruun is blind, but it is the regular -un "
        "form of the card's own root and his psloan>psruan is the equally blind "
        "-an form already shipped on the same evidence."
    ),
    "_sdxalan": (
        "SDXALAN 椅背－扶手－倚靠處－支撐物. Batch 65: sdxalan>sdharan. The shipped "
        "value was the IDENTITY -- tier id, his spelling unchanged -- because "
        "sdxalan happens to exist in modern Truku glossed 很髒, a soil word. His "
        "SDAXAL card ships sdahar 依靠著… spk 6, psdahar 使…靠著 spk 4 and dahar "
        "靠著, and all three slots are the backrest sense (你的椅子有椅背嗎？, "
        "沒有可以倚靠的地方). sdharan is sdahar with the regular -an syncope, the "
        "alternation the corpus already shows in durux>drxan."
    ),
    "_pk'lu": (
        "PK'LU 當…的時候. Batch 65: pk'lu>pklug. Less a wrong word than the wrong "
        "spelling of one -- his \"LU card is elug/peelug/meelug/gmeelug, all with "
        "the g, and only this slot lost it, to pklu 剛好 spk 2. pklug 正好;正時 spk "
        "34 is the same sense, seventeen times more attested, consistent with every "
        "other slot on the card, and 正時 is his 當…的時候 exactly."
    ),
    "_l'pi": (
        "L'PI. CLEARED, batch 65 -- not a defect. audit4 flagged it on his NDUK "
        "card, where his own gloss says \"D'pi ＝ 關！（命令式）\" and the value lpi "
        "is 無米粒的稻穀. But he has TWO L'PI headwords: 關！（命令語氣）and 穀糠－"
        "穀穗，或穗上不含穀粒的部分 -- and lpi 無米粒的稻穀 is the second one word for "
        "word. Ten slots, four the closing sense (L'PI hw, L'PI ex, NDUK sub, NDUK "
        "ex) and four the husk sense (L'PI hw, L'PI ex, L'XKAX ex, QODAP ex). The "
        "value serves one card exactly, which is the most a flat map can do; his "
        "d'pi>dpi 關門 spk 16 already carries the closing sense on its own key."
    ),
    "_g'loq": (
        "G'LOQ. CLOSED, batch 65, from the long-standing deferred list of split "
        "families -- both halves are mapped right and nothing is needed. audit4 "
        "flagged g'loq>gluq 污垢, gnloq>gnluq and xmgloq>hmgluq as outliers against "
        "his LOQ card's ruq majority. But hmgluq is glossed 抽;拔 and his xmgloq is "
        "出鞘－從套中取出 -- an exact match -- so the gluq root is genuinely his and "
        "污垢 is a homophone row in the omnibus. The card holds two families, LOQ "
        "(ruq) and G'LOQ (gluq), which is why it looks incoherent to a "
        "substring test."
    ),
    "_klagan": (
        "KLAGAN 攀登的時間、地點. CLEARED, batch 65. The value kragan is glossed 整理 "
        "and his gloss is 攀登, which looks like the alax class, but modern Truku "
        "has TWO homophonous karaw families: climb (karaw 爬;越, blind) and "
        "clean/tidy (kmaraw 清理 spk 44, kragan 整理 spk 2). The -an form of the "
        "climb one has the same shape, so the string is right and only the "
        "omnibus gloss belongs to the other family. Nothing to write."
    ),
    "_tmquli": (
        "TMQULI. CLEARED, batch 65. audit4 flagged it on his TKULI 倒入；使容納 "
        "card against the tquri majority, with the value tmquli 撫養. But of its "
        "four slots three are his QULI and TQULI cards -- 領養一個孩子, 撫養 -- so "
        "the value is exactly right for the majority, and the one pour-sense slot "
        "is written \"Tmkuli (Tmquli ?)\", where he is querying the spelling "
        "himself. His tmkuli>tmquri 已裝、倒 carries the pour sense on its own key."
    ),
}

lex = json.load(io.open(H + "lexical_map.json", encoding="utf-8"))
lex.update(NOTES)
json.dump(lex, io.open(H + "lexical_map.json", "w", encoding="utf-8", newline="\n"),
          ensure_ascii=False, indent=1)
print("lexical_map: notes %s written (%d keys)" % (sorted(NOTES), len(lex)))

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
