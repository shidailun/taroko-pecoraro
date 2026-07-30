"""Batch 66: the first batch found by asking the dictionary instead of the corpus.

audit2 reads the never-gloss-checked tiers in frequency order; audit4 checks each
card for internal coherence. audit5 asks the question the whole review keeps
coming back to -- LOOK IT UP IN THE MODERN DICTIONARY. For every key on a tier
that never consulted a gloss: take HIS gloss, take the shipped value's omnibus
gloss, and if they share no two-character Chinese word, hunt the omnibus for a
word that IS within a length-scaled edit distance of what charRules would print
for his token AND does share one AND is better attested.

Two design corrections made it work. His meaning has to come from headword and
sub slots only -- in an example slot the gloss is the whole sentence's translation,
so da, ko, na, ni inherited the sentence's vocabulary and matched anything; that
alone was the top six rows of the first run. And the edit cap has to scale with
length, because at two edits a two-letter particle is within reach of half the
dictionary. With both, 96 keys at >=3 slots, and the top of the list is signal.

Nine keys, 44 slots, and no homograph cost anywhere: every slot on every card
carries the sense the new value has.

SKAWAS 17x -- 去年, last year, on an identity that is not a word.
   The value was his own spelling unchanged, spk 0 and unglossed. shkawas 去年
   spk 19 is the modern form -- and the map ALREADY ships it, for his OTHER
   spelling of the same word, sxkawas. The self-contradiction signature again:
   pax/pnax, loan/lowan, ngali/nngali, mnsa/mnusa. All 17 slots across 14 cards
   are 去年 without exception (Mntöting skawas ka laqe Libix 去年出生, Mqudi ko
   pax skawas 我從去年起頭髮就白了). The series is consistent too: his s'xiga is
   already shipped shiga 昨天 spk 150.

ML'BU 12x -- 早晨, morning, on mrbu spk 1.
   He spells it three ways -- ml'bu (8), m'lbu (2), mlbu (2) -- and all three land
   on mrbu, which is spoken once and glossed nowhere. mgrbu 早上;早晨 spk 256 is
   the word, and the omnibus confirms the root: rbu 早上（破曉至黎明）. Every one
   of the twelve slots is morning (Musa gm'xap ml'bu 播種的人早上去播種, Mlbu balae
   ka knddaxan 他們出發得很早). Same class as pk'lu>pklug in batch 65 -- his
   transcription dropped a segment the modern word keeps.

MBUYAS 8x -- 肚子, belly, on embuyas spk 0.
   The em- rule that produced it is real: his mbiyax is embiyax spk 227. But
   embuyas is spoken zero times and glossed nowhere, while nbuyas 肚子 sits at spk
   13, and his own sub gloss is 一）有肚子——長出肚子。二）肚子——腹部——腹, whose
   second sense is the bare noun. Six of the eight slots are that noun (kui mbuyas
   肚子裡的蟲, Paro mbuyas 懷孕了, MBUYAS hw 肚子——大腹便便的人). The family is
   attested around it: buyas spk 7, smbuyas 拉肚子 spk 9.

MNSWAI 7x -- 兄弟姊妹, on an identity spoken twice.
   mnswayi 兄弟姊妹（複數）spk 347, and the map already ships it for FOUR other
   spellings of his -- dmnsuwai, dmnswai, mnsuai, mnsuwai. Only this variant was
   left behind. All seven slots are the sibling sense (Mnswai ta ka ita 我們是兄弟,
   Kana ita mnswai 我們全是兄弟).

AYO 5x -- 小溪, stream, on ayu spk 4 and unglossed.
   ayug 小溪/山谷 spk 100. His AYO headword is 「小溪——水溝——水道。」and all five
   slots are a stream (Ga mqole xlaan xedao ka ayo 溪流在東邊, Pstlilun mo ayo
   我想讓孩子跳過那條小溪). Same dropped final as ml'bu. Note his AYUS 界線 and his
   ayong>ayung 傭人 are different words on their own keys and are untouched.

SBIYAN 5x -- 傍晚, on an identity spoken zero times.
   His GBIYAN card says it outright: SBIYAN is 過去的某個傍晚(較常用的形式,意義與前
   兩者 SGBIYAN、SKBIYAN 相同) -- the same word as the other two. The map already
   sends both of those to sgbiyan 昨天傍晚. sbiyan is spoken zero times and glossed
   nowhere, so the third synonym joins the two.

USUK 3x -- 袖子, sleeve, on an identity spoken zero times.
   usux 袖子 spk 4, matching his USUK 衣服的袖子 exactly, and both slots on both
   cards are a sleeve. The x is not a disqualification: 1893 omnibus words contain
   x and 332 are spoken, among them jiyax 749, dxgal 662, utux 406, maxal 348.
   charRules folds x to h, which is right for most words and wrong here.

Cleared on inspection -- the value is right and audit5 was reading homophony:
   lading CLOSED from the long-standing deferred list. rajing is glossed 不夠;不足
          against his 開始－起頭, which looks like the alax class -- but his
          plading>prajing 開始 spk 72 is ALREADY shipped, so rajing is genuinely
          the root of the begin word and 不夠 is a homophone row.
   mqleqo his leqo>riqu 不容易 spk 16 is already shipped, and 不容易 is his 困難
          exactly. mqriqu and mkriqu are the regular mq- and mk- forms of that
          root. The candidate msriqu 困難 spk 35 is a different affix on the same
          root, not a better word -- a sibling, which is what most of the blind
          rows below the top turn out to be.
   lobong rbung 深坑 is a covered pit, which serves both his 覆蓋 and his 陷阱, and
          his l'bong/lbuong already share the key. His separate lobang>rubang
          陷阱套 spk 12 carries the trap sense on its own key.

HELD, and the one homograph this batch found:
   lawa   his LAWA card is two headwords -- 呼喚－叫喊 and 籃子－筐子 -- on one
          string. The basket sense wants rawa 背簍、籃子 spk 44; the call sense
          wants lawa, which is right as it stands, because his mlawa>mlawa 打；招呼
          spk 79 shows lawa is the bound root of the calling verb. 3 slots basket
          against 2 call: too thin to move, and unlike the batch-63/64 homographs
          the losing side here would be made WRONG rather than left wrong. Held
          with the reasoning recorded.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # SKAWAS: the sh- form the map already ships for his other spelling, sxkawas
    "skawas": "shkawas",   # WAS skawas (identity) spk 0 blind;  shkawas 去年 spk 19
    # ML'BU: morning. All three of his spellings, all on mrbu spk 1 unglossed
    "ml'bu": "mgrbu",      # WAS mrbu spk 1 blind;  mgrbu 早上;早晨 spk 256
    "m'lbu": "mgrbu",      # same word, his variant spelling
    "mlbu": "mgrbu",       # same word, his variant spelling
    # MBUYAS: the belly noun most of his slots carry
    "mbuyas": "nbuyas",    # WAS embuyas spk 0 blind;  nbuyas 肚子 spk 13
    # MNSWAI: the plural the map already ships for four other spellings of his
    "mnswai": "mnswayi",   # WAS mnswai (identity) spk 2 blind;  mnswayi 兄弟姊妹 spk 347
    # AYO: the stream word, with the final his transcription dropped
    "ayo": "ayug",         # WAS ayu spk 4 blind;  ayug 小溪/山谷 spk 100
    # SBIYAN: his own card declares it synonymous with SGBIYAN and SKBIYAN
    "sbiyan": "sgbiyan",   # WAS sbiyan (identity) spk 0 blind;  sgbiyan 昨天傍晚
    # USUK: sleeve
    "usuk": "usux",        # WAS usuk (identity) spk 0 blind;  usux 袖子 spk 4
}

NOTES = {
    "_skawas": (
        "SKAWAS 去年, 17x. Batch 66, and the first key found by audit5 -- the "
        "detector that asks whether the omnibus holds a word matching HIS gloss "
        "better than the one we took. The value was tier T, his own spelling "
        "unchanged, spoken zero times and glossed nowhere. shkawas 去年 spk 19 is "
        "the modern form and the map ALREADY ships it for his other spelling of "
        "the same word, sxkawas -- the self-contradiction signature of pax/pnax, "
        "mnsa/mnusa, mnswai/mnswayi. All 17 slots across 14 cards are 去年 without "
        "exception. The series is consistent: his s'xiga>shiga 昨天 spk 150."
    ),
    "_ml'bu": (
        "ML'BU 早晨, 12x across three spellings of his -- ml'bu (8), m'lbu (2), "
        "mlbu (2). Batch 66: all three to mgrbu. They were on mrbu, spoken once "
        "and glossed nowhere; mgrbu 早上;早晨 is spk 256 and the omnibus confirms "
        "the root separately as rbu 早上（破曉至黎明）. Every slot is morning "
        "(Musa gm'xap ml'bu 播種的人早上去播種, Mlbu balae ka knddaxan 他們出發得很早, "
        "Malu ko bi ka ml'bu 我早上很好). Same class as pk'lu>pklug in batch 65: "
        "his transcription dropped a segment the modern word keeps. NOT touched: "
        "his knlbuan, where the AN card glosses the same root 短的特質 as well as "
        "「晨性」, and no kngrbuan exists to move it to."
    ),
    "_mbuyas": (
        "MBUYAS 肚子, 8x. Batch 66: mbuyas>nbuyas, off embuyas. The em- rule that "
        "produced the old value is a real Truku alternation -- his mbiyax is "
        "embiyax spk 227 -- so this is not a bad rule, just a bad output: embuyas "
        "is spoken zero times and glossed nowhere, while nbuyas 肚子 is spk 13 and "
        "the family around it is attested (buyas spk 7, smbuyas 拉肚子 spk 9). His "
        "sub gloss is 一）有肚子——長出肚子。二）肚子——腹部——腹, and six of the eight "
        "slots are that second, bare-noun sense: kui mbuyas 肚子裡的蟲, Paro mbuyas "
        "懷孕了, MBUYAS hw 肚子——大腹便便的人."
    ),
    "_mnswai": (
        "MNSWAI 兄弟姊妹, 7x. Batch 66: mnswai>mnswayi 兄弟姊妹（複數）spk 347. The "
        "value was the identity at spk 2, glossed nowhere. The map already ships "
        "mnswayi for FOUR other spellings of his -- dmnsuwai, dmnswai, mnsuai, "
        "mnsuwai -- so only this variant was left behind; the same shape as "
        "skawas/sxkawas in this batch. All seven slots are the sibling sense "
        "(Mnswai ta ka ita 我們是兄弟, Kana ita mnswai 我們全是兄弟, Xbalao bi "
        "mnswai 有很多弟兄在等你)."
    ),
    "_ayo": (
        "AYO 小溪, 5x. Batch 66: ayo>ayug 小溪/山谷 spk 100, off ayu spk 4 and "
        "unglossed. His headword is 「小溪——水溝——水道。」and all five slots are a "
        "stream (Ga mqole xlaan xedao ka ayo 溪流在東邊, Mksiyao bi ayo 沿著溪流的岸邊, "
        "Pstlilun mo ayo 跳過那條小溪). Dropped final, like ml'bu and pk'lu. His "
        "AYUS 界線 and his ayong>ayung 傭人 are different words on their own keys "
        "and are untouched."
    ),
    "_sbiyan": (
        "SBIYAN 傍晚, 5x. Batch 66: sbiyan>sgbiyan. He states the identification "
        "himself on the GBIYAN card -- SBIYAN is 過去的某個傍晚(較常用的形式,意義與前"
        "兩者 SGBIYAN、SKBIYAN 相同) -- and the map already sends both of those to "
        "sgbiyan 昨天傍晚. The value was the identity, spoken zero times and glossed "
        "nowhere, so the third synonym now joins the other two."
    ),
    "_usuk": (
        "USUK 衣服的袖子, 3x. Batch 66: usuk>usux 袖子 spk 4, off an identity spoken "
        "zero times. The x is not a disqualification even though charRules folds x "
        "to h: 1893 omnibus words contain x and 332 are spoken, among them jiyax "
        "749, dxgal 662, utux 406, maxal 348, qsurux 282. The fold is right for "
        "most words and wrong for this one. Both slots on both cards are a sleeve."
    ),
    "_lawa": (
        "LAWA. HELD, batch 66 -- a homograph too thin to move, recorded rather "
        "than acted on. His LAWA card carries TWO headwords on one string: 呼喚－"
        "叫喊 and 籃子－筐子. The basket sense wants rawa 背簍、籃子 spk 44; the call "
        "sense wants lawa exactly as it stands, because his mlawa>mlawa 打；招呼 "
        "spk 79 shows lawa is the bound root of the calling verb and the omnibus "
        "glosses the bare form 人名（女）only because a bound root is not used alone. "
        "3 slots basket (LAWA hw 籃子, LAWA ex 把蛋放進籃子裡, BLEX ex 我忘了拿籃子) "
        "against 2 call. Unlike pai 11:1, kyoxan 6:3 or mnsa 48:4, moving it would "
        "make the losing side WRONG rather than leave it wrong, and 3:2 is not "
        "enough to buy that."
    ),
    "_lading": (
        "LADING 開始－起頭. CLOSED, batch 66, from the long-standing deferred list. "
        "The value rajing is glossed 不夠;不足, which reads like the alax class -- a "
        "real word meaning something else. It is not: his plading>prajing 開始 spk "
        "72 is already shipped, so rajing is genuinely the root of the begin word "
        "and 不夠 is a homophone row in the omnibus. Nothing to write."
    ),
    "_mqleqo": (
        "MQLEQO 困難的－複雜的. CLEARED, batch 66. audit5 offered msriqu 困難 spk 35 "
        "against mqriqu spk 1, but his leqo>riqu 不容易 spk 16 is already shipped "
        "and 不容易 is his 困難 exactly. mqriqu and mkriqu are the regular mq- and "
        "mk- forms of that root; msriqu is a different affix on the same root, a "
        "sibling rather than a better word. This is the dominant false-positive "
        "class below the top of audit5's list."
    ),
    "_lobong": (
        "LOBONG 覆蓋/陷阱. CLEARED, batch 66. rbung 深坑 is a covered pit, which "
        "serves both of his headwords, and his l'bong and lbuong already share the "
        "key. His separate lobang>rubang 陷阱套 spk 12 carries the trap sense on "
        "its own key, and qlubung 套腳陷阱器 spk 52 is a different snare."
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
