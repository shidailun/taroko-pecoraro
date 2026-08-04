# -*- coding: utf-8 -*-
"""Is this unlisted value a regular inflection of a listed root?

The verified test used to be literal: a modern value counts only if that exact
string is one of the 40,760 types in attested_modern.json. That treats the
modern dictionary as if it listed every form of every word, and it does not —
it lists the forms someone happened to record. `qriban` is absent while its own
siblings `qribun` 剪成 and `qribi` 要剪下 are present; that is a LISTING gap, not
a lexical gap, and calling it unverified tells the reader the wrong thing.

So a value is also verified when it is an attested root wearing one of the
paradigm slots every Truku verb has:

  AF          m- prefix, or the -m- infix after the first consonant
  PF          -un
  LF          -an
  referential s-
  causative   p-
  preterite   n- prefix, or the -n- infix after the first consonant
  imperative  -i -ay -aw -ani -anay -aneyi

and the stacks those build (pn-, sn-, mn-, sp-, psn-, emp-). The suffixes -un
and -an swallow a root-final vowel, so that is allowed for as well.

Nothing else. Not kn-, not tm-, not two prefixes from outside the list — those
are derivation, and a derived word can mean something its root does not. The
doubled onset is excluded for the same reason even though it looks like the
obvious next class: batch 20 measured that mm-, pp-, tt- and ss- are live
modern PREFIXES, so a doubled initial is only sometimes a reduplication
(`ssapah` is "all the houses", not "a house"), and modern marks the human
plural with d- anyway (`dseejiq` 288×).

**Shape alone is not enough, and this is the whole reason the module reads
glosses.** His SISUN is SAIS 縫, to sew — and it decomposes perfectly as
`sisi`+`-un`, where `sisi` is 用來濾酒的工具, a rattan wine strainer. Same
letters, unrelated word, and calling the value verified would assert that an
invention is real modern Truku. So the root's modern gloss must agree with HIS
Chinese for the word: one shared two-character run, or one shared single
character that is not a structural particle. Agreement is deliberately loose —
his Chinese is a 1977 French dictionary rendered into Chinese and will not use
the modern dictionary's wording — but it kills the coincidences: `smisu` off
the pronoun `misu` 你, `ingay` and `banan` off glossless fragments.

Names and loans are excluded outright. A name has no modern dictionary entry to
be missing from, so "regular inflection of an attested root" is not a statement
anyone can make about one — `talan` is a man, and shape alone verified him as
`tali`+`-an` [靠]. Tiers N and J are frozen populations everywhere else in the
generator; this rule is no different.
"""
import collections, io, json, os, re

D = os.path.dirname(os.path.abspath(__file__))
H = os.path.normpath(os.path.join(D, "..", ".."))
TOK = re.compile(r"[A-Za-zÀ-ÿłŁʔ'’\"]+")
HAN = re.compile(r"[一-鿿]+")
# [batch 165] A romanized token inside one of his Chinese glosses — the shape
# of a cross-reference. See crossref() on why the scan may be this loose.
LATIN_TOK = re.compile(r"[A-Za-z][A-Za-z'’ç]{2,}")
# A gloss that says "same as above" rather than saying anything. 61 pale slot
# occurrences ride on one -- 38 of them on 同上之動詞形 alone -- and regular()
# tests his Chinese against the listed root's own gloss, so a pointer has no
# content character to test with and refuses a form it should accept. The parent
# entry's zh is what the pointer points AT, so it is fed IN ADDITION, never
# instead: three of these carry real content beside the pointer (同上之動詞形－
# 閒聊, 即將成為同上者（源頭、基礎……）) and the long S 前綴 grammar note matches
# 上述 as a pure false positive, so a replacement would destroy content.
POINT = re.compile(r"同上|同前|見上|如上|上列|上述|前條|同該|同此")
NAMETAG = re.compile(r"name\s*\(|emprunt|\(J")
VOW = "aeiou"

# Every level from 1 to 7 reaches a root by stripping one of these, so a prefix
# that is missing here makes its whole class unverifiable at ANY level, however
# good the evidence. The list started as the m-/p-/s-/n- series and had none of
# the k-, t-, d-, g- ones -- so kn- degree (knqrinutan 貧窮 <- qrinut 窮), tn-
# possessor (tnkuyuh 女人的所有者), km- desiderative (kmbuway 想要給), d- human
# collective (dmkdaya 住在高處的那些人), mk- locative (mkrbagan 夏季期間) and the
# ma- prospective (mabubu 即將成為母親) were all unreachable. Adding 33 of them
# is 257 values / 489 occurrences newly verified with ZERO de-verification; see
# logs/ver128.py.
#
# Two things this list must NOT grow into. The CV- reduplications (tt kk gg ss
# mm) are deliberately absent: they already reach level 7, whose gate is the
# strict slot-gloss one, and putting them here would hand them regular()'s
# single-shared-character gate instead. A reduplication is not a prefix. And
# `sq` was measured and rejected -- it yields one value, and it steals sqrasan
# off `qras` 快樂 onto `rasa` on a shared 間. Price a candidate BOTH singly and
# in combination: regular() takes the least affixation, so a newly-legal short
# prefix can outbid a longer correct one.
#
# The last 16 are round two, priced against the base 128 left behind: the vein
# is much thinner (32 values / 54 occurrences) because the derived series of a
# prefix could not be a candidate until its own base was legal. `tm`, deferred
# out of 128 rather than rejected, is here now and unblocks four of the long-
# standing paux59 leads through tmriya 旋轉 and tmabuy 下坡. Eleven candidates
# were rejected and the re-cut column, not the gain column, is what convicted
# most of them: `png` moves pngsaan off his PESA 請願－請求 family onto `saan`
# 去; `dn` moves tgmilan off `gamil` 根, which his own sub-form glosses 生根的
# 事實、地點、時間; `psm`, `ptn` and `qm` likewise trade a real root for a
# suffixed form. `gmb` buys one value by vouching the mushroom `nilaq` with
# `mnilaq` 起屑 on the 起 of 令人想起海藻. `dq` is not a morpheme at all --
# dqqrinut is d- collective on a qq- REDUPLICATION, the same error as tt/kk
# above wearing a collective's clothes. `empg`, `kms`, `pnt` and `psg` gain
# nothing and can therefore only do damage.
PRE = ["", "m", "em", "n", "mn", "p", "pn", "s", "sn", "sp", "spn", "ps", "psn",
       "pp", "emp", "mnp", "snp", "np", "smn", "pm",
       "ma", "maa", "t", "tn", "tg", "k", "kn", "km", "kmn", "g", "gm", "gn",
       "d", "mk", "mt", "ms", "mg", "pk", "pt", "pg", "sm", "sk", "skn", "sg",
       "mq", "kns", "tmn", "gmn", "mtg", "mpt", "empt", "empk", "emps",
       "tm", "tmg", "tk", "kmp", "mkm", "mkn", "msn", "nk", "ns",
       "pnk", "pns", "psk", "snk", "sns", "dm", "qn",
       "empa", "pkp", "spk", "sps", "npk", "dmp", "emb",
       # Batch 157. Priced the way the note above demands: 0 re-cuts, 0 roots
       # stolen, and it buys nothing by itself — it exists so `tqliwaq`
       # 發光的；閃耀的 can be a SUPPORTER in derived(), the exact parallel of
       # `mq`, which has been legal since 128 and yields `mqliwaq`.
       "tq"]
# [batch 130] SUF had never been priced. Adding each candidate alone and reading
# the re-cut column refuses nearly all of them, and refuses the biggest number in
# the batch: `n` bought 10 types / 23 occurrences and took `mkmisan` off `misan`
# 冬天 for `kisa` 真, `ptungun` off `putung` 火柴, `pgnnakan` off `nak` 為己 for
# `naka` 分. It is not a suffix. It is what `-an`/`-un` LOOKS like after a
# vowel-final root, which roots() already knows through its swallowed vowel — so
# putting it here corrupts regular(), the level with the most authority. `a` is
# the same error (it gains by cutting a root's OWN final vowel: `trima` 洗澡 →
# `trim`). `on en in ung ang ni ci han gan nay wi way yi yay yaw` gain nothing,
# or gain only by inflating derived() past its `len(set(...)) < 2` gate — a bogus
# suffix manufacturing its own support. `iyun`/`iyan` are strictly worse than the
# glides: iyun cuts `pktngiyun` to `ktng` at level 4 where `yun` cuts it to the
# LISTED `pktngi` 讓…吃飽 at level 1, his gloss 使…吃飽 exactly.
#
# Two admitted. `yun` is the glide a vowel-final root writes before -un
# (`pktngi` + `un` = `pktngiyun`); it gains 5 types and its one re-cut is a
# promotion, `spiyun` sistered → regular on `spi` 夢. `aan` is the long slot
# CLAUDE.md already documents for the PXAAL family (`phli`, `phlan`, `phlun`,
# `phlaan`), and `p'xlaan` is exactly what it gains.
#
# `yan` is REFUSED although it is the same morphology as `yun`, and the reason is
# the standing rule that a brown claim naming the WRONG EXISTING WORD is the
# worst state available: its unique level-1 gain is `sghuwayan` 謝意－感激 read as
# `sg` + `huwa` 疑問句結屃詞…如何？ + `yan`, agreeing on 何 from an example
# sentence. His word is `huway` 慷慨 — `mhuway` is how Truku says thank you, and
# `sghuway` 靠…慷慨 is listed. What blocks the true reading is that 謝意 shares no
# character with the modern gloss 慷慨, i.e. a dictionary gap, not a morphology
# gap. A GLIDE GATE (y only after i, w only after u — a glide is the consonant
# form of a high vowel) admits `yan` safely and kills `huwa`, which ends in a; it
# has to touch all five SUF loops, so it is its own batch.
BASE_SUF = ["", "un", "an", "i", "ay", "aw", "ani", "anay", "aneyi", "aan"]

# [batch 131, round two] The glide is not a suffix, so it is not listed as one.
# Every vowel-initial suffix has a y-form and a w-form, because that is what its
# opening vowel becomes after a root that already ends in one — so generate them
# rather than enumerate them, and let the gate below decide where each may land.
# Enumerating cost `yaneyi`/`waneyi`, which nobody would have thought to type.
SUF = BASE_SUF + [g + s for s in BASE_SUF if s and s[0] in VOW for g in "yw"]

_SUF_LONG = sorted([s for s in SUF if s], key=len, reverse=True)


def _core(x):
    """x with one paradigm suffix peeled, if that leaves a root-sized string."""
    for sf in _SUF_LONG:
        if x.endswith(sf) and len(x) - len(sf) >= 3:
            return x[:-len(sf)]
    return x


def root_groups(cands):
    """Partition candidate roots into the LEXEMES they belong to.

    The wordlist files a paradigm's cells as separate headwords, so a value can
    reach `blaq`, `blaqa`, `blaqan`, `blaqi`, `sblaqa`, `sblaqan` and `sblaqi`
    and have found ONE root seven times over. Two candidates are the same
    lexeme when either contains the other, before or after a suffix is peeled
    off either side. See no_chinese(): the ambiguity guard is about which ROOT
    the value is built on, and two spellings of one root are not a tie.
    """
    # [batch 165] The sort key is (len, x) and not len, and the second field is
    # not cosmetic. The grouping below is GREEDY — x joins the first group it
    # touches — so its result depends on the order it walks the candidates, and
    # `cands` arrives as a set. Sorting by length alone leaves every tie among
    # equal-length candidates to be broken by the set's iteration order, which
    # Python varies per process. `mngahan` reaches `mngaha`, `mngahi`,
    # `ngahan`, `ngaha`, `ngahi`, `ngaho`, `ngahu` — six of them tied at two
    # lengths — and fell into one group or two depending on the run, so
    # no_chinese()'s one-group gate passed or failed and the word came out
    # verified in three builds out of four. Found by rebuilding twice with no
    # change and diffing. Every rule that reads this gate — no_chinese() is
    # 194 values — was that unstable, and a dom log asserting such a word was
    # asserting a coin flip.
    groups = []
    for x in sorted(cands, key=lambda x: (len(x), x)):
        for g in groups:
            if any(a in b or b in a for y in g
                   for a, b in ((x, y), (_core(x), _core(y)),
                                (x, _core(y)), (_core(x), y))):
                g.append(x)
                break
        else:
            groups.append([x])
    return groups


# The suffixes that end in a vowel of their own — see vouched()'s fourth guard.
# Not regenerated: every glide form ends with the form it was built from, and
# this tuple is only ever asked `.endswith()`.
VSUF = ("i", "ay", "aw", "ani", "anay", "aneyi")

# [batch 131] THE GLIDE GATE, which is what let `yan` in above.
#
# A glide is the consonant form of a high vowel: y is what i becomes before
# another vowel, w is what u becomes. So the glide a vowel-final root writes
# before a vowel-initial suffix is not free — it is DETERMINED by that root's
# own last vowel, and a root ending in a, e or o writes no glide at all. That
# makes `-yun`/`-yan` legal on `pktngi`, `srngi`, `dngi`, `tqri`, `spi`, `bki`
# and illegal on `huwa`, which is the entire reason `yan` was refused in 130:
# ungated, its unique level-1 gain was `sghuwayan` 謝意－感激 analysed as
# sg + `huwa` 疑問詞…如何？ + yan, a brown claim naming the wrong existing word
# (his is `huway` 慷慨, cf. `mhuway`, `sghuway` 靠…慷慨). The gate kills that
# one analysis BY RULE rather than by hand-list, which is the only reason to
# prefer it to another entry in HAND_NOT_ROOTED.
#
# Read at call time, so pricing empties it. Applied at all five SUF loops
# (roots, derived, vouched_root, sistered, syncopated) — a gate at four of
# them is not a gate, since the levels do not share a splitter (lesson mmmmm).
GLIDE = {"y": "i", "w": "u"}


def glide_ok(root, sf):
    """Whether `root` may take `sf`, when sf opens with a glide."""
    need = GLIDE.get(sf[:1])
    return not need or root[-1:] == need

# Characters that carry no meaning on their own, so sharing one is not
# agreement. Without this, 的 and 是 confirm anything against anything.
#
# 子 is here for the same reason and it is not obvious: it is the noun
# classifier of 種子 seed, 果子 fruit, 釘子 nail, 日子 day, 梳子 comb, 李子 plum
# and 卵子 ovum, so on its own it confirms anything against anything too. It
# alone was holding up four claims — `snkmalu` and `spkmalu` decomposed onto
# `kalu` 梳子 when his word is `malu` 好, and `stmaqun` matched 刀子砍樹的聲音
# against his 把你的李子壓碎.
#
# 已 joined them in batch 114: it is the perfective marker and nothing else, so
# 已知道的 "already known" confirmed his （已完成的）攀登 "(completed) climbing"
# against `gnkla` 知道 to know, two words with no sense in common at all.
#
# 沒 joined them in batch 116, beside the 不 that was here from the start: it is
# a negation and carries no more sense than one. `tatuk` 什麼都沒有 was verifying
# his `ttoqe` 敲打 on the 沒 of 我沒碰撞瓶子.
#
# 大 and 小 LEFT in batch 142, and they never belonged: the test this list
# states is "carries no meaning on its own", and big and small are meanings.
# They were swept in with the function words and then silently refused the two
# adjectives a Formosan wordlist glosses most often — `paru` IS 大的 and `bilaq`
# IS 小 — so his 使自己變小者 could not agree with 小. Measured alone: +10 values,
# 0 de-verified, 0 relevelled, of which 8 are his own word for big or small
# (`mkparu` 長大, `msbilaq` 使自己變小, `tbilaq` 確實小, `skparu` 用以使…長大) and
# 2 are coincidences pinned below.
#
# 人 was tested the same way in the same batch and REFUSED, though it fails the
# same "carries meaning" test: in these two wordlists it is overwhelmingly a
# FRAME rather than a word — 使人X "make someone X" and X的人 "one who Xs", the
# agent nominalizer. Dropping it buys 9 and the first one read is the proof:
# `pngraq` 使人變傻 "make a fool of someone" agreeing with `ngraq` 比女人陰蒂的手勢
# on the 人 of 女人. 上 likewise (+13, but `mtama` 當上父親的人 agreeing with
# `tama` 上帝 on the 上 of a verbal complement, and it would let `mttama` and
# `tmtama` back in through a second door the batch before had just shut).
# 下 and 中 alone buy nothing at all and are left where they are.
STOP = set("的了是我你他她們個很不一有在要中上下人這那和與或也就都再又只之"
           "為所以及者其於由對從把被讓使做作用能會可時樣事物子已沒")

# Both wordlists talk ABOUT words, and that metalanguage is not meaning: his
#「這會是 MIYAQ 的詞根嗎？」and the modern「為「empmiyak 要忙家務事」的詞根」share
# the run 的詞 and the character 根 while sharing no sense at all. These are
# EXCISED from a gloss before its characters are read, rather than subtracted
# from the result — dropping the bigram alone leaves a bare 根 behind, and
# putting 根 in STOP would take it away from 根源 and 樹根, where it is the
# whole meaning (it was holding up `snpusu` 根基 by itself).
#
# Two more in batch 116, both the same kind of frame. 人名 labels a word instead
# of glossing it — `tuqul` is 人名（男）and nothing else, and it was verifying
# `emptquli` on the 名. Excising rather than stopping is again what makes it
# safe: `suyang` is 人名（男）; 美麗, and the excision leaves the 美麗 standing.
# 用來 says how a word is deployed, not what it means — `ruyu` 水蟲用來當魚餌的,
# a water insect USED AS fish bait, was verifying his `psryui` 使突出 on the 來.
# 369 modern glosses carry the run and excising it costs no existing claim; his
# own 用來品嚐的東西 still says 品嚐, which is the gloss it must not break.
BOILER = re.compile("的詞根|詞根|動詞形|動詞|名詞|同上|之詞|形式|參見|前項|衍生|詞形"
                    "|用來|人名")

# Ruled out of scope by hand over batches 100–109. The tier logs cover names
# the digitization tagged, but a name reached only through an example sentence
# never got a tag — OTUN 秋（Otun）家 and TAOLAN 陶蘭 are in his sentences only.
HAND_NAMES = """sibal liwis mikat ingay lauken tatu talan banan lobyaq lubyaq
opic upih sikat imin timin tain pilin akit dloan lautan hidi eku tsay puti
stbaku mici dcristu tensu semento kodyo kaityo diko diku cristo yordan xelyo
xatso xaibyo tanso tenso tagahan murisaka mkmurisaka sitang efunang aman atwi
atuh denki banasi otun utun taolan taulan""".split()

# SPOKEN FOR BY THE INFORMANT — a fifth kind of evidence, and the only one on
# this page that is not a document (batch 159).
#
# The speaker shortlist exists because some questions no corpus can answer, and
# the agreed workflow for it is "we'll go one by one". This is the set where his
# answers land. It widens `seen` and never `lex`, like the parquets, the Bible
# and the names before it: a word vouched for by a speaker is an attestation,
# not a root the affix analyser may cut other words onto.
#
# It is kept separate from everything else and printed separately so that no
# later reader can mistake one of these for a wordlist hit. That is the whole
# point of the category. A corpus miss is recorded next to each entry, because
# the miss is real and stays true — what changes is what it MEANS.
#
#   nta   his NTA (R. = ?) 邀請前往（唯一使用的形式，與 LITA 並用）, 20
#         occurrences, the largest pale word left on the page by a factor of
#         three. `Nta da ! ... Kia ! Lita da !` 來吧，來！……好！我們走吧！
#         **Batch 146 called it Toda and not Truku, and that was bad
#         reasoning.** Klokah listing a form under 都達 says where Klokah
#         happened to record it; it cannot say where the word is absent, and it
#         is not evidence against a Truku dictionary that prints the word with a
#         usage note. The corpus miss is real and was re-measured here — 0 hits
#         in the 40,760-word wordlist, 0 in the 2,058 types of the Truku Bible,
#         0 in 14,600 parquet types, 0 in 11,820 spoken types, against `nita` 5
#         and `nnita` 25 for the genitive 我們的, which is a different word. What
#         a miss across four written sources shows is that no modern Truku TEXT
#         we hold spells it; his own note — 唯一使用的形式 — says why, because a
#         hortative interjection is exactly what a Bible and a wordlist have no
#         slot for. The informant says it is Truku. He is the authority the
#         shortlist was addressed to.
HAND_SPOKEN = """nta""".split()

# RULED ON BY THE INFORMANT WHERE THE GATE HAD ALREADY AGREED — batch 180. Kept
# apart from HAND_SPOKEN, which answers a different question. There the corpus is
# silent about whether a word is Truku at all; here the corpus has already said
# yes to every part of the word, and the ONE test that refuses is gloss
# agreement, whose instrument is a shared Han character and which therefore
# cannot see two synonyms.
#
#   ppdsun  his `ppd'sun`, in § Ongat ko bi ana manu ppd'sun mo tmaan diyan
#           under ADAS / Pp'adas 用來寄送之物. roots() finds THREE analyses and
#           every root of all three is already dark: `p-` + pdsun
#           「…(人)將會帶去(未來式)」, `pp-` + dsun 「要帶」, `p-` + pdsi 「帶去」
#           + `-un`. The wordlist itself calls pdsun the future, and pp- is a
#           live modern prefix (batch 20, with mm-, tt-, ss-). The informant's
#           ruling — "ppdsun is fut pf" — names the same slot the wordlist does.
#
#           WHY THE GATE REFUSED, exactly: he never glossed the word AS a word,
#           so the only Chinese `regular()` holds for it is the sentence
#           translation 我實在沒有任何東西可以捎給(送給)Djian 的父親, and 捎/送
#           share no character with 帶 or 拿走. Synonyms, invisible to character
#           overlap. The word-level gloss that would have served sits one line
#           up, on the sub-form the sentence lives under, and `_his_glosses()`
#           drops it: examples are fed `x.zh or szh`, an OR, so a sentence
#           carrying its own translation shadows its parent entirely.
#
#           THE GENERAL FIX WAS PRICED AND NOT TAKEN. Letting a token borrow its
#           parent form's gloss — restricted to tokens sharing a 3-character run
#           with the parent form, or every function word in the sentence
#           inherits it — over all 549 blocked sentences frees 3 types and 3
#           pairs (`empabgu`, `pnsdahung`, `empnhmadan`), and does not reach this
#           word anyway: 用來寄送之物 shares no character with 帶 either.
#
#           THE FAMILY ACQUITS. Of the 59 distinct tokens in the ADAS entry —
#           headword, nine sub-forms, both ° lines and every example — 58 are
#           already dark. This is the last pale word in a family that otherwise
#           agrees with itself throughout, which is the same evidence read the
#           direction that clears rather than convicts.
#   tksaw   his `Tksao`/`tksao`, first of blockers.md at 4 pairs. Two analyses,
#           both onto listed and glossed roots: `tk-` + saw 像；如此；那樣 and
#           `t-` + ksaw 像這樣；如此. His own gloss for the form is 模仿－假裝－
#           裝作 (SAO › Tksao, "Imiter - faire semblant - faire comme"), and the
#           gate refused on that and nothing else: 模仿/假裝/裝作 share no
#           character with 像/如此/那樣. "Make like" and "imitate" are one word,
#           and character overlap is the one instrument that cannot see it.
#
#           THE FAMILY ACQUITS, twice. `tksao` is the ONLY pale token in SAO (45
#           of 46 dark) and the only one in KPOXEL (25 of 26), the second entry
#           it appears in. Two families that agree with themselves throughout
#           and disagree about the same single word is the same evidence that
#           cleared ppdsun, read in the direction that clears.
#
#           Note where blockers.md found it: under KPOXEL, in the sentence about
#           playing deaf. The form's own home is four sentences away under SAO,
#           which is why rule.py prints every sentence and the ranking prints
#           one — see batch 181b.
HAND_RULED = """ppdsun tksaw""".split()

# Batch 144. The name POPULATION is his own `name (m/f)` tags plus tier N, and
# tier N's test is "capitalized mid-sentence, never lowercase anywhere" — which
# at midcap=1 is a single capital letter, as likely to be sentence-initial or a
# heading as a person. While the population was intersected with the ILRDF
# registry that cost nothing, because none of these is a Truku given name.
# Ungated, they are what comes in with the names, and they are read one by one:
#
#   grand grandeur beau vivant   FRENCH, out of his own glosses — "Beau père",
#   cunnaissance ruugeur         "1) Grand père", "= Grandeur - taille",
#                                "Vivant - mobile". Then respelled by the o>u
#                                rules, which is where `ruugeur` (rougeur) and
#                                `cunnaissance` (connaissance) come from — the
#                                spelling is the proof they are not Truku.
#   mpa                          his own PREFIX card: "Ce préfixe composé MPA".
#   byeqay   Byeqai nako munan "J'aimerais bien vous donner" — a verb, first
#            word of the sentence.
#   qlap     Qlap ! "attrape-le !" — an imperative after a semicolon.
#   yianu    his own sub-form label `Yiano` "Pour vous - à vous", a pronoun.
#   mnttlaqel  Mntlaqel (Mnttlaqel?) — a queried variant in parentheses.
#   mpsqlul    Mpsklol (Mpsq'lol ?) kia! — the same, 翻動 to stir.
#   tbasyaq    tibasyaq (Tbasyaq) — the same.
#   tsaleh     "(= Ts'alex) Misanthrope - pas sociable" — the same.
#   yiyah      iyax daxa ( Yiyax daxa) — the same.
#   pnsdahung  ka Pnsdaxong dq'las laqe mo "the one who caused those bruises" —
#              a nominalized verb, and his own headword sense 造成瘀傷.
#
# `takux` and `mpsklul`'s neighbours are NOT here: TAKOX is a card of his own
# headed `"tag": "name (m)"`, which is the strong half of the population.
HAND_NOT_NAMES = set("""beau byeqay cunnaissance grand grandeur mnttlaqel mpa
mpsqlul pnsdahung qlap ruugeur tbasyaq tsaleh vivant yianu yiyah""".split())

# no_chinese()'s pins — the six of its 139 whose single root candidate is the
# wrong word, read one by one against the sentence he puts them in. Every one is
# the SISUN shape: the letters fit, the meaning does not, and here there is no
# gloss of his to catch it, which is exactly why the rule needs a hand read.
#
#   slungan     `slung` 毛線 wool. His own note names the root: Ma so lmngao
#               slongan! 你怎麼對著大海說話呢? **(Silong=海)** — it is the SEA.
#   drnai       `drna` 鹿鞭. The card is DULUN: Dlnai ta tmaan xo? 我們去求爸爸 —
#               d<l>ulun, the imperative of 求.
#   ggitan      `gitu` 枇杷 a loquat. The card is GIGIT: Tayai bi ka g'gitan so!
#               你真是纏人! and he adds 含有…糾纏的意思.
#   empslangan  `langu` 湖 a lake. The card is his own headword SLANGAN:
#               adi biyao mpslangan ka kia! 很快就會被鏽蝕掉 — emp- on SLANGAN.
#   mtgtmaq     `tmaq` 水桶樹. The card is TMAQ/**Tgtmaq**, and the sentence is
#               mxa mtgtmaq d'xgal 全都趴倒在地 — the tree is a homograph.
#   narung      `arung` 穿山甲 a pangolin. Xea ka mnangal nalong 得獎的是他.
HAND_NOT_NC = set("""slungan drnai ggitan empslangan mtgtmaq narung
    mslangan snpsaran snpsarun sbuwai shnkan psnluun tmukan
    tnaga""".split())
# [batch 164] `tnaga` is batch 161's, and dom161 is what caught it. The gloss-
# hole fallback below reaches it through `taga` 等 and would colour it verified
# — but batch 161 refused it deliberately and the refusal was epistemic, not a
# missing rule. It belongs to the C-n- infix class, where `<n>` perfective and
# `<m>` actor-focus share a slot, so `tnaga` is either t-n-aga on `taga` or his
# typewriter's n for the m of `tmaga`, and nothing on the card decides which.
# Verifying it would assert the answer that batch 161 declined to give.
# [batch 164] The price of the second prefix peel. Each of these six reaches a
# listed root only through a stacked prefix, and in each the root it reaches is
# a coincidence rather than his word — so the refusal belongs to the peel and
# not to any one rung, and this set is read inside roots() itself.
#   dmtsapat    `sapat` 舖（舖床）. His SAPAT family is 放蕩 — `msapat` is
#               沉溺於放蕩的人, `tsapat` 真正放蕩的. Bed-spreading is a homograph.
#   empkduriq   emp-k-duriq is right, but the peel lands on `uriq` 肚子痛的聲音
#               through the swallowed vowel. His word is `qduriq` 逃跑, which
#               `mmqduriq` in this same batch reaches correctly.
#   empnalu     his 將會變好、康復、健康 — that is `malu` 好, the root batch 161
#               already refused `mnalu` over, not `alu` 陷阱線 a snare line.
#   ntnring     `ring` 常笑;愛笑. Its sibling `mtnring` is his 流汗－滿身大汗,
#               so `nring` is sweat and the laughing root is a homograph.
#   mtkkrang    `krang` is 碗掉下來破碎的聲音, an onomatopoeion; his `kkrang`
#               and `mkkrang` are 發抖－打顫, shivering. Not the same word.
#   spsdharun   sps+dharun reaching `hari` 一點（比較級） is a substring
#               accident with no morphology behind it.
HAND_NOT_STACK = set("""dmtsapat empkduriq empnalu ntnring mtkkrang
    spsdharun""".split())
# [batch 165] The two rungs below read evidence the other eleven never look at,
# so each needs its own refusal list; a pin on a rung above cannot reach them.
#   HAND_NOT_XREF — A POINTER INSIDE A QUESTION IS NOT A CITATION. He marks his
#   own uncertainty with ？ and he is scrupulous about it, so the punctuation is
#   evidence and it is his. `tbowyak` is （詞根 BOYAQ？）＝痛得打滾 — he is
#   asking whether the root is BOYAQ, and `bowyak` is 山豬 a wild boar, which
#   is not rolling on the ground in pain but is spelled the same. `empsibus` is
#   （Pksibus?）加糖: its sibling `pksibus` carries 參見 Psibus with no question
#   mark and is admitted, and the two together are the distinction drawn as
#   sharply as he draws it.
#   `mnalu` is batch 161's homograph refusal and `pauxun` is the PAUX family
#   the SYN note refuses by name at 15 occurrences. Both are reachable through
#   a pointer, and neither refusal was ever for want of a link.
HAND_NOT_XREF = set("""tbowyak empsibus mnalu pauxun""".split())
#   HAND_NOT_FAMILY — his family agrees with itself about the wrong root, or
#   an earlier batch pinned the word on a ground this rung cannot see.
#   `psiisi`, `psiisan`, `psiisun` are the second kind, and they are the reason
#   the regression suite exists. Batch 153 respelled his SISI/SISAN/SISUN
#   paradigm to `siisi`/`siisan`/`siisun` on a Truku speaker's ruling, and wrote
#   down the tripwire in the same breath: the causatives are NOT listed, so
#   "if these ever go dark without a speaker or a listing behind them, the
#   respelling has been allowed to carry verification with it, which it must
#   never do." This rung is exactly that failure. It fires because `siisan` is
#   now in the wordlist — but it is in the wordlist because WE respelled it, and
#   his own cards then agree with each other about a root only our hand map
#   gave him. Six occurrences, refused. dom153 caught it; nothing else would
#   have.
HAND_NOT_FAMILY = set("""psiisi psiisan psiisun""".split())
# [batch 163] The second six, found the same way as the first six and read
# against the sentence he prints them in. `mslangan` is `empslangan`'s own
# sibling — it stands in BMBANG 鐵皮－鐵桶, rust on tin, which is his SLANGAN
# 鏽蝕 and not `langu` 湖. `snpsaran`/`snpsarun` are under PUSAL 更新／成雙－加倍,
# his TWO root, not `sari` 芋頭. `sbuwai` is 把書交給 handing a book over, not
# `buwa` 氣泡; `sapah shnkan` is 監獄 in his own sentence, not `hnka` 便宜;
# `psnluun` is 把好消息傳遍各處 under SN'LO 傳達, not `luun` 將會省著用.
# `tmukan` stands in TUYOQ 唾液－吐口水, 他們全都朝他的臉吐了口水 — spitting,
# against `tuki` 抵銷／點鐘；小時, which is the Japanese 時計 homograph tier J
# was built around ("the more often it turns up, the more confident the wrong
# answer looked"). It is the only one of the seven the group collapse reached
# rather than the old one-candidate guard, and it is the price of that widening.

# A gloss that says "this is a personal name" is not a meaning, so it cannot be
# the meaning a suffixed form inherits: `ksudan` <- `sudu` 人名（男）, `nputuh` <-
# `putuh` 人名, `empsbiyuq` <- `biyuq` 人名 were all reached this way. Tested with
# all(), not any(), so `suyang` 人名（男）/美麗 keeps its second sense.
NAMEGL = re.compile(r"人名|名字|地名")

# Read one by one out of vouched()'s whole output — 56 values, which is small
# enough to check by hand and too important not to. Two survived the gloss gate
# on a character that is doing no work:
#   tbuur   his 黃瓜 a cucumber, vouched by `emptbuur` 專找地瓜皮的人 — 地瓜 is a
#           sweet potato, and 瓜 alone is the same kind of classifier as 子.
#   tcingi  his 掉落－下降－出生, vouched by `tcingan` 打鐵店 — `tucing` carries
#           both 打 to strike and 掉落 to fall, and the blacksmith's shop says
#           nothing about the falling sense his entry is about.
HAND_NOT_VOUCHED = set("tbuur tcingi".split())

# vouched_root()'s whole output read the same way — 69 values, batch 114. Three
# are wrong and no gate reaches them, because the defect is in the ROOT, not in
# the gloss:
#   nnalu   his 好、良善（過去式）. The root `nalu` is a phantom: `nmalu` is the
#   empnalu preterite of `malu` 好 and `snalu` the perfective of `smalu` 做, two
#           different words that happen to strip to the same four letters, so
#           the two-supporter guard was satisfied by conflating them.
#   nilaq   his entry is the edible tree mushroom, and it agreed with `mnilaq`
#           起屑 to flake only on the 起 of 令人想起海藻 "recalls seaweed".
#
# [batch 130] Six pinned when the swallowed vowel was added below, because the
# patch reaches them and the root it then names is wrong.
#   tbuyun  all land on `buyu`/`nbuyu`, agreeing on the 去 of `gnbuyu` 去打獵
#   tbuyan  against his 下去－奔下. But `buyu` is the grass/hunting root
#   ptbuyun (`bbuyu` 打獵, `kmnbuyu` 看成…草) and batch 129 settled this family on
#   ptbuyan `abuy` 下坡, from `tmabuy` 走下坡 — his gloss exactly. `abuy` is
#   tnbuyan structurally unreachable here: the syncope helper restores a root's
#           FINAL vowel, never an initial one, and these are prefix + (a)buy + un.
#   ptungun the patch takes it off `putung` 火柴（起火用）, a LISTED word, for the
#           hypothesis `ungu` vouched by `sungu` 加木材加火. Verified either way —
#           the display is binary — but that is the defect `-n` was convicted for
#           one paragraph above, and the record should name the right word.
#
# [batch 131] One more, and the glide gate is what exposed it: enlarging SUF
# with `yan` grew derived('tmai') past its gate and bought `tntmaan` — root
# `tmai`, supporter `tmayan` 進入的地方, agreeing with his 曾經坐過的地方 on 地方,
# which is the locative-slot word EVERY -an nominalization shares and therefore
# no agreement at all. `tmayan` is `tmay` 進入、進來 + an, and that whole paradigm
# is listed (`mtmay` 進入, `tmayi`, `tmayun`, `stmay`, `kmtmay` 想進去) — his own
# TMAI entry is 進入－穿入, a DIFFERENT entry from the TTAMA 坐 this word belongs
# to. Its real analysis is t + `-n-` + `ttmaan`, and `ttmaan` is attested; what
# stops regular() reaching it is that `ttmaan` carries no gloss, which is the
# listing gap, not a morphology gap. Pinned rather than repaired.
HAND_NOT_ROOTED = set(
    "nnalu empnalu nilaq "
    "tbuyun tbuyan ptbuyun ptbuyan tnbuyan ptungun "
    "tntmaan".split())

# unglossed_root()'s whole output read the same way — 26 values, batch 141. The
# rule agrees against a SUPPORTER, so the way it goes wrong is the one way that
# kind of agreement can: the shared character is not a word but a particle, and
# no gate can see the difference because a particle is a character like any
# other.
#   psqpahan his （主動）地黏貼－使黏附, to paste, agreeing with `qmpahan` 工作的地
#   psqpahi  on 地 — the ADVERBIAL 地 of 主動地 against the 地 that means ground.
#   psqpahun He has two roots here and they are not the same root: QPAH 工作 and
#            SQPAX 黏貼. This is the SISUN shape exactly — right letters, wrong
#            word — and it is the reason the doctrine exists.
#   mttama   his 坐著的人－靠著休息的人 against `pttama` 守著, agreeing on 著, the
#   tmtama   verbal aspect marker. Every one of the three glosses wears it and
#            none of them means it. The reading may well be right; the EVIDENCE
#            is a particle, and a particle is not evidence.
#   mrbuq    his 呈凹陷－形成凹穴 against `trbuq` 形容坑洞深, agreeing on the 形 of
#            形容 — the head the wordlist writes in front of a gloss that
#            DESCRIBES rather than names, the same class as the 用來 already in
#            BOILER. Here the two readings do agree (both are hollows), which is
#            why this one is pinned and not remapped: the answer is right and
#            the argument for it is worthless.
#
# Requiring a two-character run instead of a hand list was measured and refused:
# it costs 14 of the 26 to save these 6, including `qnriqani` 恨, `trgrig` 舞,
# `smbrinah` 回 and the three `pllg-` 動, every one of which is a single
# character that IS a word.
# `psqpahan psqpahi psqpahun` were the first three members of this set and
# are gone from it [batch 155]. They were pinned because they resolved onto
# `qpah`/`qpahan`/`qpahi`, all glossed 工作, and his gloss is 黏貼－使黏附.
# A speaker ruled that qapah is *stick* and is NOT qpah — the two roots
# differ by a vowel his typewriter dropped — so manual_map now respells them
# psqapahan/psqapahi/psqapahun and they resolve onto psqapah / sqapah /
# qapah instead. The pin is not weakened, it is unreachable: nothing emits
# those strings any more, and a pin on a string nothing emits is the vacuous
# assertion logs/dom152.py refused to leave standing.
HAND_NOT_UNGLOSSED = set("mttama tmtama mrbuq".split())

# The two coincidences 大/小 let into regular() when they left STOP in batch
# 142. Both are the same shape as the six above — the shared character is real
# but the pairing is nonsense — except that here the character IS a word, which
# is why nothing but a hand reading catches them.
#   knslaan  his 饑餓虛脫－精疲力竭, hunger and exhaustion, against `sla` 大外衣, a
#            large outer garment. Nothing in common but the 大.
#   mkpakaw  his 位於荊棘叢中的, in the thorn thicket, against `pak`+`-aw`
#            老鷹抓小雞的動作, the hawk-and-chicks game, on the 小 of 小雞. The
#            RIGHT root is sitting beside it — `pakaw` 有刺的野草, the thorny weed,
#            his gloss exactly — and shares no character with him at all, which
#            is the whole reason `_agrees` is a proxy and not a measure.
HAND_NOT_REGULAR = set("knslaan".split())

# The same shape once more, one rule further down [batch 154]. `tnbusan` is his
# 簸揚的對象，或（過去的）方式 — the thing winnowed, or the (past) manner — and
# the root `tbus` is glossed 篩榖, sifting grain, with `ptbus` 使被篩去 and
# `tmbus` 篩去… as its two supporters. They agree on 去, and the 去 in his gloss
# is the one inside 過去, the past. Winnowing and sifting grain ARE the same
# word, so the rule's answer is right; its argument is a particle. Pinned rather
# than remapped, exactly as `mrbuq` was in batch 141: **the answer being right
# does not make a worthless argument worth keeping.**
#
# `mhmadan` is the same trap with a wrong answer under it, which is the worse
# half. His 成為親戚——變成親戚, to become a relative, lands on the root `hada` 熟,
# ripe, whose `phada` 使…成熟 and `tghada` 較成熟 agree with him on 成 — the 成 of
# 成為, "become", against the 成 of 成熟, "ripen". Becoming kin is not ripening
# and the root is not his. 成 is not going into STOP for it: it carries meaning
# perfectly well, and it is only worthless here because it is the frame verb of
# a 成為X gloss — the same shape as the 人 of 使人X that batch 142 measured and
# refused to drop.
# Batch 170 respelled `tnbusan` to `tnbsan` — the wordlist's own slot is `tbsan`
# with the vowel dropped, and the n-perfectives of CCVC roots take the dropped
# shape 22 times to 1. The pin has to follow the word or it dies silently, so
# BOTH spellings are listed. What batch 154 refused is the 去 argument, and that
# refusal still stands; `tnbsan` goes dark through the SYN line above instead,
# off the listed slot `tbsan`, which is a different and better route.
HAND_NOT_OUTVOTED = set("tnbusan tnbsan mhmadan".split())

# ---- SYNONYMY, the third tier of _agrees [batch 148] ----------------------
# `mkpakaw` came off the line above to sit here instead, because the note that
# refused it states this batch's premise outright: the right root `pakaw`
# 有刺的野草 is "his gloss exactly — and shares no character with him at all,
# which is the whole reason `_agrees` is a proxy and not a measure."
#
# Character overlap is a proxy for sameness of MEANING, and Chinese lets you
# write one meaning two ways with nothing in common. 房子 and 家 are the same
# thing and share nothing; so are 不容易 and 困難, 取代 and 頂替, 不露面 and
# 躲藏, 警戒 and 守衛. Every one of those pairs is sitting in this dictionary
# with his gloss on one side and the modern wordlist's on the other, and 432
# well-formed inflections were pale because of it.
#
# So a third tier, after the bigram and the character: a hand-written table of
# Chinese expressions that name ONE concept. It is a table and not a measure —
# every line was read off an actual refused pair and says which one.
#
# **Every member is at least two characters, and that is the guard, not a
# style.** It is STOP's lesson in another form. 一 is in STOP because it is in
# everything, which is why `kingal` 一個 could never reach his 單一的; the
# two-character 一個/單一/一次 give that back without giving back the bare 一,
# and 家 stays out while 住屋 and 房子 do the work. A one-character member
# would match inside 大家, 國家, 家人 and hand this rule the SISUN failure.
#
# A line groups expressions that are interchangeable, not merely associated.
# `paux` 犁田 against his KPAUX 翻轉 is NOT here and is worth 15 occurrences:
# ploughing does turn the soil over, but 犁田 and 翻轉 are not the same word,
# and "related if you think about it" is exactly the reasoning SISUN punishes.
SYN = [
    # 房子 / 家 — `sapah` 住屋；家/戶家 against his EMPASAPAH 將會變成房子.
    "房子 住屋 家屋 房屋",
    # `kuyuh` 女性;女人;太太;婦女 against his EMPAKUYUH 將成為妻子.
    "妻子 太太 婦女 女人 女性",
    # `riqu` 不容易 against his MKRIQU 困難的－複雜的.
    "困難 不容易 難處",
    # `ririh` 取代 against his RNIRIH 頂替……的位置－繼承.
    "取代 頂替 代替 繼承 接替",
    # `liing` 不露面 against his MTLIING 採取行動躲藏－處於隱蔽的位置.
    "躲藏 隱蔽 不露面 隱藏 藏匿",
    # `gdadak` 去警戒 against his DMPGDADAK 守衛們——守望者們.
    "守衛 守望 警戒 看守 站崗",
    # `rbnaw` 嬰孩 against his MRBNAW 柔嫩、年幼、未成熟者.
    "嬰孩 年幼 幼小 柔嫩 幼兒",
    # `biyax` 力量 against his DMBIYAX 壯年人的群體，正值壯年者.
    "壯年 力量 強壯 有力",
    # `kingal` 一個；一頂 against his SNKINGAL 單一的——單層的——一次的 and
    # MSKINGAL 同心協力—團結—合而為一. See the two-character rule above.
    "單一 一個 一次 合而為一 團結 專一",
    # `keeman` 夜晚；午夜/晚上 and `kman` 晚上 against his 變暗－處於黑暗中的,
    # 天將黑, 將被遮暗、變得昏暗.
    "黑暗 變暗 昏暗 天黑 夜晚 晚上 午夜 遮暗",
    # `kuwax` 挪開 against his MKUWAX 退避者－遠離者 and PKUWAX 使遠離－驅趕.
    "挪開 遠離 退避 驅趕 走開",
    # `rbung` 深坑, the covered pit. Two lines, not one: he uses it for the
    # burial (MTRBUNG 被掩埋、覆蓋、埋葬者) and for the deadfall (MKRBUNG 設下
    # 陷阱－張設圈套), and a grave is not a snare even though the hole is.
    "深坑 掩埋 埋葬 覆蓋",
    "深坑 陷阱 圈套",
    # `trbuq` 形容坑洞深 against his TRBUQI 凹陷者－挖掘－挖出凹穴.
    "坑洞 凹穴 凹陷 挖掘",
    # `pkrdax` 使有光 and `rdax` 光線 against his 天將亮 and 想要照亮.
    # Batch 157 widened this line by three. His `pkliwaq` 使其變得明亮 and the
    # glossary's `tqliwaq` 發光的；閃耀的 name one thing and share no character
    # at all, so the tier below could not see between them.
    "光線 有光 明亮 照亮 天亮 發亮 發光 閃耀 閃光",
    # `sblus` 不鹹;不甜 against his PSBLUS 使變淡－去除味道.
    "變淡 不鹹 不甜 清淡",
    # `kbuyu` 都是草叢 against his PKBUYU 使荒蕪——遮蔭.
    "草叢 荒蕪 雜草",
    # `cipiq` 不多 and `nbilaq` 原來小的 against his 每次一點點 and 一次一點點.
    "一點點 不多 小的 少許 一小份 變小 減少",   # + spcipiq 使其變小，數量減少
    # `tgxal` 團聚、相聚 against his STGXAL 為了成為同伴、夥伴 and KMTGXAL
    # 想與……組隊.
    "團聚 相聚 同伴 夥伴 組隊",
    # `qrngul` 空氣汙染 against his MQRNGUL 多煙的——被煙燻滿的.
    "多煙 煙燻 冒煙 空氣汙染",
    # `luan` 教…省點用 against his NLUAN 被存起來的—積蓄.
    "積蓄 省點 省下 存起",
    # `shmu` 小便 against his SHMUAN 尿桶（廁所）－排尿的器官.
    "小便 排尿 尿桶 小解",
    # `qdqut` 鍊條;鐵鍊 against his QDQUTAN 束縛 — 鐐銬 — 桎梏.
    "鍊條 鐵鍊 鐐銬 捆綁 束縛",
    # `squwaq` 吵鬧 against his MSQUWAQ 愛說話的人－愛閒聊的人.
    "吵鬧 愛說話 閒聊 多話",
    # `lhlih` 欺侮 against his LHLIHAN 誹謗——希望某人遭殃——傷害某人.
    "欺侮 誹謗 傷害 欺負",
    # `pakaw` 有刺的野草 against his MKPAKAW 位於荊棘叢中的 — the case that
    # named this batch.
    "荊棘 有刺 刺人",
    # Batch 150. A second reading of the same bucket, after the Bible glossary
    # had already taken the pairs that were a WRONG GLOSS rather than a
    # different wording. What is left is the genuine article: one concept, two
    # ways of writing it, no character in common.
    "矯正 扶正 改正 修直 弄直 拉直",     # empslagu 矯正－扶正 / slguan 要…修直
    "能夠 可以 有辦法 辦得到",           # tduwaan 能夠－有辦法 / tduwa 可以
    "寬恕 諒解 原諒 饒恕",              # spsruwa 寬恕 / psruwa 使被諒解
    "傳染 沾到 沾染 感染",              # smru 傳染 / mru 沾到…
    "滾燙 熱水 燒水 沸騰",              # pkdngdang 使其滾燙 / dngdang 燒水
    "搬運 扛起 抬起 扛抬 搬走",          # pkudaw 使搬運 / kudaw 抬起或扛起
    "鄙視 輕看 輕視 看不起",            # snlhkah 鄙視 / lhkah 輕看別人
    "解開 鬆開 拆開 脫落 卸下",          # lhlahan 解開－鬆開 / lhlah 脫落
    "下坡 下來 下去 下山",              # pntabuy 一路下坡 / tabuy 下來
    "養肥 變肥 肥胖 胖子",              # ptbnaw 養肥 / tbnaw 胖子
    "說服 相信 信服",                  # spsnhiyi 說服 / psnhiyi 使相信
    "源頭 起源 根本 基礎",              # spusu 源頭、起源 / pusu 主要的，根本的
    # Batch 151. Four more, read off the biggest surviving items in the same
    # bucket. Three of the four agree only because batch 149 gave the root its
    # second gloss — `lutut` is 連結 in the wordlist and 宗族血統；後裔 in the
    # glossary, `tqnay` and `ttama` are glossed by the glossary alone — so
    # these are the two mechanisms working together rather than either one.
    "親屬 親戚 宗族 血統 後裔 家族",      # mslutut 確實是親屬 / lutut 宗族血統
    "作伴 陪同 跟隨 相伴 同行 結伴 在一起",  # stqnay 作伴 / tqnay 跟隨；陪同
    "欺騙 愚弄 錯亂 迷惑 受騙",          # pneutuxan 免得受騙 / peutux 使...錯亂
    "坐著 停住 棲息 坐下",              # mttama 坐著的人 / ttama 停住（在上方）
    "記號 標示 指示 標記 符號",          # empskraya 指示－標示 / pskraya 記號
    "抓住 捕捉 逮住 釣到 捉住",          # ttjiyal 牢牢被抓住 / tjiyal 捕捉;釣到
    "就這樣 是這樣 那樣 一樣 這樣",       # snhaya 跟以前一樣 / shaya 就這樣
    # Batch 155. 粘 and 黏 are one morpheme in two hands, which is why the
    # character tier could not see across them: his 黏附 and the wordlist's
    # `msqapah` 粘起來 share nothing to compare. Every member is still two
    # characters and they are interchangeable, not associated — this is the
    # weakest line in the table and the one closest to being a spelling.
    "黏住 粘起 黏附 黏貼 黏著 黏在",      # sqapah 黏住（在） / mqapah 黏附的
    # Batch 170. His TBUS 簸揚 against the wordlist's `tbus` 篩榖 / `tbsan`
    # 篩穀子的地方 / `tmbus` 篩去… / `stubs` 為…篩去. Batch 154 had already read
    # this pair and said outright that "winnowing and sifting grain ARE the same
    # word" — then pinned it, because the only agreement `outvoted()` could find
    # was the 去 of 過去, a particle. The answer was right and the argument was
    # worthless. This line is the argument.
    #
    # It does not rest on my reading of two glosses. HIS CARD NAMES THE TOOL:
    # TBUS is 使用簸箕（＝Bluxeng）在混合物, and `Bluxeng` is modern `bluhing`
    # 簸箕 — listed, 5x in the parquets, with `smbluhing` 用…簸箕 and `kbluhing`
    # 做成簸箕 behind it. He points at the winnowing tray; the wordlist writes
    # the act you do with it. One concept, two hands, no character in common.
    #
    # **The tool is deliberately NOT a member.** Putting 簸箕 on this line would
    # let his card agree with the 43-word `giya` 小簸箕 family, which is a
    # different and smaller tray and a different root. Members are the ACT only.
    # Blast radius measured before writing: 簸揚 occurs in exactly one of his
    # entries and 篩 in one, so this line can reach one card.
    "簸揚 篩榖 篩穀 篩去",              # tnbsan 簸揚的對象 / tbsan 篩穀子的地方
]
SYN = [s.split() for s in SYN]
assert all(len(m) >= 2 for s in SYN for m in s), "SYN members must be >= 2 chars"

# sistered()'s whole output read the same way — batch 115. The rule reads no
# gloss at all, so the way it goes wrong is the homonym: his word is a
# different word that happens to wear the same letters as a slot of an
# attested paradigm.
#   qurun   his Q'QOL 挖鑿－雕刻 to gouge, sistered by `quri` 有關 and `quray`,
#   quran   which are the paradigm of a word about being ABOUT something. The
#           whole family was on the wrong stem — modern 開鑿;雕刻 is `gmqur`,
#           with a g — and batch 115 remaps it rather than verifying it.
HAND_NOT_SISTERED = set("qurun quran".split())


def _read(p):
    return io.open(p, encoding="utf-8").read()


def wkey(w):
    return w.lower().replace('"', "'").replace("’", "'")


class Inflection(object):
    def __init__(self, lex, mp):
        """lex: the attested type set. mp: MODERN_MAP, his key -> modern value."""
        self.lex = lex
        self.gl = json.load(io.open(os.path.join(D, "attested_gloss.json"),
                                    encoding="utf-8"))
        # A SECOND OPINION ON WHAT A ROOT MEANS [batch 149].
        #
        # Batch 147 admitted the Truku scripture readers to `seen` and nothing
        # else, on the rule that a TEXT can say a string occurs but can never
        # say what it means. This file is the other thing: dict_truku_bible,
        # 2,033 headwords with Chinese and English definitions, edited and
        # published for the same dialect. A glossary is allowed to speak to
        # meaning, which is the one question a corpus is not allowed to answer.
        #
        # It is ADDITIVE and never replaces. A root keeps every gloss the
        # wordlist gives it and this one is appended, so the rule can only turn
        # a refusal into an agreement — nothing already dark can be argued pale
        # by it.
        #
        # It answers the failure bucket D was full of: the wordlist gives ONE
        # sense and it is the wrong one, or it is a name tag instead of a gloss.
        # `tama` 上帝 -> 父親；天父 (his SKTAMA 已故的父親 is 11 occurrences by
        # itself), `pajiq` 人名（女）-> 蔬菜；青菜, `kari` 挖掘 -> 話語；言語,
        # `lutut` 連結 -> 宗族血統；後裔, `rusuq` 卵子 -> 水滴；淚珠. And 830 of
        # its headwords are roots the wordlist never glossed AT ALL, which is
        # the hole unglossed_root() was built around.
        #
        # **It cannot reopen the SISUN trap or the `paux` family.** It glosses
        # neither `sisi` nor `paux`. That is not a promise about this rule, it
        # is a property of the file, and dom149 asserts it from the DOM.
        #
        # Its grammatical labels — 處所格, 過去式, 複數, 受格, 被動, 地名,
        # 大寫時指 — are stripped when bible_gloss.json is written, NOT by
        # adding them to BOILER: BOILER is read against the wordlist too, and
        # widening it there could de-verify a word that is already dark.
        self.bgl = json.load(io.open(os.path.join(D, "bible_gloss.json"),
                                     encoding="utf-8"))
        # **A voice is not a spelling.** `self.lex` licenses a spelling: a
        # word is in it because the dictionary may PRINT it, and that is why
        # the standing rule is that seen widens and lex never does. Being
        # evidence is a different job. Batch 149 made the glossary an
        # additive gloss SOURCE but left its headwords out of the population
        # `derived()` sweeps, so a word the glossary glosses could be read
        # and could never vote — `smqdug` 控告 sits on his own roots
        # sqdug/qdug and was invisible to every paradigm rule [batch 156].
        # `voices` is used by derived() and NOWHERE else. Nothing here can
        # become a modern spelling; it can only agree or fail to agree.
        # THE ILRDF ONLINE DICTIONARY — batch 182, fetched word by word by
        # fetch_edictionary.py and cached. It joins on exactly the Bible
        # glossary's terms and for one job only.
        #
        # What the first 611 lookups established, and it is worth stating
        # plainly because it decides how this file may be used: 165 hits, and
        # **not one of them is a word attested_modern.json does not already
        # hold**. It attests NOTHING new. Nor does it reach a single one of the
        # 378 blocked types — `tksaw` and `gmquwaq` come back 無搜尋結果 while
        # their roots are there in full, because it indexes headwords and the
        # derived forms live in the printed Patas pusu kari Truku, which is not
        # online. Anyone tempted to widen `seen` from here should read that
        # sentence again: there is nothing here to widen it WITH.
        #
        # What it does hold is GLOSSES for roots the wordlist lists bare: 17 of
        # the 85 glossless roots under the blocked pairs, `bsrat` 吝嗇, `siisan`
        # 縫補, `qqrinut` 貧窮, `tbrnahi` 忘恩, `brnux` 平地. That is the same
        # hole unglossed_root() was built around, filled with somebody's
        # published Chinese instead of an inference.
        self.edg = {w: d["glosses"] for w, d in json.load(
            io.open(os.path.join(D, "edictionary_trv.json"), encoding="utf-8")
        ).items() if d and d.get("glosses")}
        # Not in `voices`, and the omission is the point: derived() sweeps
        # voices as a POPULATION of words that may vote, and every word here is
        # in `lex` already, so adding them would change nothing except to
        # suggest this file licenses spellings. It does not.
        self.voices = set(lex) | set(self.bgl)
        self.inv = collections.defaultdict(list)
        for k, v in mp.items():
            self.inv[v].append(k)
        s = _read(os.path.join(H, "site", "entries.js"))
        entries = json.loads(s[s.index("["):s.rindex("]") + 1])
        self.his = self._his_glosses(entries)
        self.slot = self._his_glosses(entries, slots_only=True)
        self.par = self._paradigm_tokens(entries)
        self.frozen = self._frozen(entries, mp)
        # [batch 165] crossref() cites in his orthography; his_family() needs
        # his paradigm the way derived() gives the wordlist's. Both are read
        # only by those two rungs — neither widens `lex`, and neither can
        # become a modern spelling.
        self.raw2mod = {k.lower(): val for k, val in mp.items()}
        self.fam = collections.defaultdict(set)
        for val in self.inv:
            if not self.slot or not self._his(val, slots_only=True):
                continue
            for c, _, _, _ in self.roots(val):
                if c in self.lex:
                    self.fam[c].add(val)

    @staticmethod
    def _paradigm_tokens(entries):
        """Every token he printed in a ° paradigm line — the slots he himself
        declares are one word's inflections. sistered()'s gate."""
        out = set()
        for e in entries:
            for f in [e.get("paradigm")] + [sb.get("paradigm")
                                            for sb in e.get("subs", [])]:
                for m in TOK.finditer(f or ""):
                    out.add(wkey(m.group(0)))
        return out

    # ---- his Chinese, per token, from every field that reaches the screen ---
    def _his_glosses(self, entries, slots_only=False):
        """slots_only drops the example sentences, keeping only the Chinese he
        attached to a word AS a word — a headword, sub-form or paradigm gloss.

        A sentence gloss describes a whole clause and shares a character with
        almost anything, which is tolerable when the rest of the evidence chain
        is short and not when it is long: see vouched_root()."""
        his = collections.defaultdict(set)

        def feed(txt, zh):
            if txt and zh:
                for m in TOK.finditer(txt):
                    his[wkey(m.group(0))].add(zh)

        for e in entries:
            zh = e.get("zh") or ""
            for f in ("hw", "paradigm", "crossRef"):
                feed(e.get(f), zh)
            for x in ([] if slots_only else e.get("examples", [])):
                feed(x.get("t"), x.get("zh") or zh)
            for sb in e.get("subs", []):
                szh = sb.get("zh") or zh
                feed(sb.get("form"), szh)
                feed(sb.get("paradigm"), szh)
                if sb.get("zh") and POINT.search(sb["zh"]) and zh:
                    feed(sb.get("form"), zh)
                    feed(sb.get("paradigm"), zh)
                for x in ([] if slots_only else sb.get("examples", [])):
                    feed(x.get("t"), x.get("zh") or szh)
        return his

    def _frozen(self, entries, mp):
        out = set(HAND_NAMES)
        for log in ("tier_n_log.txt", "tier_j_log.txt"):
            for ln in io.open(os.path.join(D, log), encoding="utf-8"):
                p = ln.split()
                if len(p) >= 2 and not ln.startswith("#"):
                    out.add(p[1])
        for e in entries:
            if not NAMETAG.search(e.get("tag") or ""):
                continue
            forms = [e.get("hw")] + [sb.get("form") for sb in e.get("subs", [])]
            for f in forms:
                for m in TOK.finditer(f or ""):
                    k = wkey(m.group(0))
                    if k in mp:
                        out.add(mp[k])
        return out

    # ---- gloss agreement ---------------------------------------------------
    @staticmethod
    def _chars(zhs):
        one, two = set(), set()
        for z in zhs:
            for run in HAN.findall(z):
                for seg in BOILER.split(run):
                    one |= set(seg) - STOP
                    two |= {seg[j:j + 2] for j in range(len(seg) - 1)}
        return one, two

    def _gloss(self, root):
        """Every gloss anyone gives this root: the wordlist's, then the Bible
        glossary's, then the ILRDF online dictionary's. Additive — see self.bgl
        and self.edg in __init__."""
        rg = list(self.gl.get(root) or [])
        if root in self.bgl:
            rg.append(self.bgl[root])
        rg.extend(self.edg.get(root) or ())
        return rg

    def _agrees(self, his_zhs, root):
        rg = self._gloss(root)
        if not rg or not his_zhs:
            return None
        h1, h2 = self._chars(his_zhs)
        r1, r2 = self._chars(rg)
        if h2 & r2:
            return sorted(h2 & r2)[0]
        if h1 & r1:
            return sorted(h1 & r1)[0]
        return self._syn(his_zhs, rg)

    @staticmethod
    def _syn(his_zhs, rg):
        """The SYN table — one concept written two ways. See SYN's note.

        The metalanguage goes first, for the same reason `_chars` excises it:
        「同上之動詞形」is about a word, not a meaning, and a synset member
        hiding inside it would be an agreement about nothing.
        """
        hz = "".join("".join(BOILER.split(z)) for z in his_zhs)
        rz = "".join("".join(BOILER.split(z)) for z in rg)
        for s in SYN:
            a = [m for m in s if m in hz]
            b = [m for m in s if m in rz]
            if a and b:
                return "%s=%s" % (a[0], b[0])
        return None

    # ---- the paradigm ------------------------------------------------------
    def roots(self, v, _stack=True):
        """(root, prefix, suffix, slot) for every attested root inflecting to v."""
        out = []
        for p in PRE:
            if not v.startswith(p):
                continue
            b0 = v[len(p):]
            if len(b0) < 3:
                continue
            stems = [(b0, False)]
            if len(b0) > 3 and b0[0] not in VOW and b0[1] in "mn":
                stems.append((b0[0] + b0[2:], True))       # the -m-/-n- infix
            # [batch 130] The branch above strips exactly ONE letter, so the
            # two-letter preterite-AF `-mn-` was unreachable at every level: his
            # `smnais` is s-mn-ais on `sais` 縫, and one-letter stripping turns it
            # into `snais`, a different word. Priced alone it gains only
            # `rmnngat` (← the listed `rngat` 呻吟), but both its re-cuts are
            # promotions onto the true root — `smnais` from vouched_root(`mais`)
            # to regular(`sais` 縫), `smnkagul` from vouched_root(`kagul`) to
            # regular(`skagul` 遣), both of them standing leads. `nm` is refused:
            # it gains nothing and only re-labels `mnmataru` 六 / `mnmngari` 九
            # with the same root either way. `um` and `in` gain nothing at all.
            if len(b0) > 4 and b0[0] not in VOW and b0[1:3] == "mn":
                stems.append((b0[0] + b0[3:], True))
            for st, infixed in stems:
                for sf in SUF:
                    if sf and not st.endswith(sf):
                        continue
                    r = st[:len(st) - len(sf)] if sf else st
                    if len(r) < 3 or not glide_ok(r, sf):
                        continue
                    cands = [r]
                    if sf in ("un", "an", "ani", "anay", "aneyi"):
                        cands += [r + c for c in VOW]      # the swallowed vowel
                    for c in cands:
                        if c in self.lex and c != v:
                            slot = "-".join(x for x in (
                                p, "infix" if infixed else "", sf) if x)
                            out.append((c, p, sf, slot or "bare"))
        if out or not _stack or v in HAND_NOT_STACK:
            return out
        # [batch 164] One prefix, and only one. A value that carries two —
        # `dmtqsurux` is dm+t+qsurux 魚, `kmspusu` is km+s+pusu 根本 — comes
        # back from the loop above with an EMPTY candidate list, so it is
        # invisible not to one rung but to all eleven at once: every rung
        # begins by asking roots() for something to read. 465 of the 807 pale
        # types decompose to nothing at all, 665 occurrences, and that is the
        # largest single block left in the census.
        #
        # The peel is a fallback and not a widening, and the distinction is
        # what makes it safe. no_chinese() refuses a value whose candidates
        # fall into more than one root group, so handing an extra candidate to
        # a value that already has some could turn a clean one-group reading
        # into an ambiguous one and DE-verify it — the one direction the rung
        # invariant does not protect. Firing only on an empty list makes that
        # impossible by construction: nothing that decomposes today can gain a
        # candidate, so nothing that reads today can stop reading.
        #
        # Depth stops at two. Three prefixes on a listed root is not a shape
        # his paradigms show, and each extra peel multiplies the substring
        # coincidences the gloss gates then have to catch.
        for p1 in PRE:
            if not p1 or not v.startswith(p1) or len(v) - len(p1) < 4:
                continue
            for c, p2, sf, slot in self.roots(v[len(p1):], _stack=False):
                if c != v:
                    out.append((c, p1 + p2, sf, slot))
        return out

    def _his(self, v, slots_only=False):
        src = self.slot if slots_only else self.his
        out = set()
        for k in self.inv.get(v) or []:
            out |= src.get(k, set())
        return out

    def regular(self, v):
        """(root, prefix, suffix, slot, the character the two glosses share),
        or None. Picks the analysis with the least affixation."""
        if v in self.frozen or v in HAND_NOT_REGULAR:
            return None
        his = self._his(v)
        best = None
        for c, p, sf, slot in self.roots(v):
            sh = self._agrees(his, c)
            if not sh:
                continue
            cost = len(p) + len(sf)
            if best is None or cost < best[0]:
                best = (cost, (c, p, sf, slot, sh))
        return best[1] if best else None

    def no_chinese(self, v):
        """(root, prefix, suffix, slot) or None — regular() where he wrote no
        gloss for the word AS a word.

        regular() verifies a form by making his Chinese and the root's modern
        gloss agree on a character. For 264 pale values that test never runs on
        anything, because the only Chinese anywhere near the word belongs to an
        EXAMPLE SENTENCE. `nsping` sits inside a clause about someone dressing
        up; `sping` is glossed 化妝; the clause translation is free to say
        打扮 or 漂亮 or nothing at all, and when it does, regular() reads a
        disagreement and refuses a form whose morphology is not in question.

        **This is vouched_root()'s own argument, run the other way.** That rule
        already refuses to ACCEPT a sentence gloss as evidence — "a sentence
        gloss describes a whole clause and shares a character with almost
        anything", the `sktama` 已故的父親 / `kmtama` 信奉上帝 case. If a
        whole-clause translation is too loose to license an agreement, it is
        equally too loose to license a REFUSAL: a translator rendering
        「我們去求爸爸」has no obligation to put the dictionary meaning of every
        stem into it. So the entry condition is `slots_only` — he attached no
        Chinese to this word — and inside it there is no gloss test at all,
        which is why the guards have to hold the whole weight:

          * the root is LISTED in the modern wordlist **and glossed there**, so
            an outside source vouches for both its spelling and its meaning;
          * four letters minimum, batch 141's floor — below that the string is
            inside everything;
          * its gloss is not only 人名/地名 (`NAMEGL`), because "this is a name"
            is not a meaning a suffixed form can inherit;
          * and **exactly one root candidate**. With no gloss to choose between
            analyses there is nothing to break a tie with, so a tie is a
            refusal. This is the guard that does the most work.

        SISUN cannot reach it: he glosses SISUN 縫 himself, so the entry
        condition throws it out before the morphology is ever looked at. What
        the guards cannot catch is a value whose ONE candidate is simply the
        wrong word, and six of the 139 were — they are pinned in HAND_NOT_NC,
        read one at a time against the sentence he prints them in.
        """
        if v in self.frozen or v in HAND_NOT_NC:
            return None
        if self._his(v, slots_only=True):
            return None
        cands = [(c, p, sf, sl) for c, p, sf, sl in self.roots(v)
                 if c in self.lex and self.gl.get(c) and len(c) >= 4
                 and not all(NAMEGL.search(g) for g in self.gl[c])]
        # NOT self._gloss() here, though `pajiq` 人名（女）/蔬菜 is exactly the
        # root NAMEGL was wrong about. This rule refuses on AMBIGUITY — "with no
        # gloss to choose between analyses there is nothing to break a tie with,
        # so a tie is a refusal" — so a second gloss source does not only admit
        # candidates, it creates ties, and routing this gate through it turned
        # 10 dark words pale (`mtbrinah`, `mkphing`, `mnksaw`, `tnklai` …) to
        # buy 7 occurrences. The second opinion is allowed to say what a root
        # means; it is not allowed to make this rule less sure which root it is.
        # **A tie needs two ROOTS, and these are two SPELLINGS.** The wordlist
        # files paradigm slots as separate headwords, so `pnsblaqan`'s seven
        # candidates (`blaq blaqa blaqan blaqi sblaqa sblaqan sblaqi`) are one
        # lexeme's cells, not seven analyses — whichever is picked the answer is
        # the same word, and the guard was refusing to break a tie that does not
        # exist. Candidates are grouped by containment and by containment after
        # a suffix is peeled (a suffix difference is a SLOT difference, not a
        # root difference); the rule needs exactly one GROUP and takes its
        # shortest member. Genuine ambiguity still refuses, which is the
        # load-bearing half: `kngusan` [kgus, ngus] and `stmaqun` [taqi, tmaq]
        # really are two roots apiece and stay pale.
        # [batch 164] Where the glossed path finds NOTHING, ask the paradigm.
        # unglossed_root() needs his Chinese to compare a glossless root
        # against; this rule needs a glossed root because he gives no Chinese
        # at all. A value that has NEITHER — no Chinese of his, and a root the
        # wordlist lists but never glossed — falls between the two and no rule
        # in the file can see it. `nglngu` is the shape: `lngu` is listed,
        # bare, and carries thirteen inflections in the wordlist.
        #
        # That hole is the gloss TABLE's, not the word's, and this file has
        # convicted it twice already — unglossed_root()'s own docstring says so
        # by name ("a hole in the GLOSS TABLE, and this file has already
        # convicted that hole twice"). The witness is the one that rule uses,
        # minus the comparison there is nothing to compare: a four-letter root
        # floor, unfrozen, its derived() yielding at least two DISTINCT affixes,
        # and the whole-or-VSUF final-vowel test. A root the wordlist inflects
        # a dozen ways is a word whether or not anyone wrote down what it means.
        #
        # It runs only when `cands` is empty, and that ordering is the safety.
        # Widening the candidate set itself would hand new members to values
        # that already read cleanly and could split a one-group reading into a
        # tie — `stmaqun` is exactly that risk, since its glossed candidates
        # `taqi`/`tmaq` are two real roots that must keep refusing while its
        # unglossed `stmaqi`/`tmaqi` are one group. Falling through only on an
        # empty list leaves every such judgement untouched.
        if not cands:
            # The floor is three and not four, as batch 163 set outvoted()'s,
            # and it is spelled with the guard the number was standing in for:
            # a root has to be pronounceable. Four letters keeps `hng` out by
            # accident; requiring a vowel keeps it out for the reason — Truku
            # writes no schwa, so a listed form with no vowel at all is a
            # consonant cluster the wordlist filed, not a syllable anyone says.
            # `pix` (batch 163) and `sma` are CVC roots and pass either way.
            for c, p, sf, sl in self.roots(v):
                if (c not in self.lex or self.gl.get(c) or len(c) < 3
                        or not any(x in VOW for x in c)
                        or c in self.frozen):
                    continue
                d = self.derived(c)
                if len(set(d.values())) < 2:
                    continue
                if not c.endswith(VSUF) and not any(w[2] for w in d.values()):
                    continue
                cands.append((c, p, sf, sl))
        if len(root_groups({c for c, _, _, _ in cands})) != 1:
            return None
        return min(cands, key=lambda r: (len(r[0]), len(r[1]) + len(r[2])))

    # ---- the inverse: a root nobody wrote down bare -------------------------
    def derived(self, v):
        """{attested word: (prefix, suffix, whether v's last vowel survived)}.

        Every attested word that is v wearing one paradigm affix, or a stack.
        Reads `self.voices` — the wordlist PLUS the Bible glossary's own
        headwords — not `self.lex`. See voices' note: a supporter is
        evidence, not a licensed spelling, and this is the only reader.
        The third field matters because the -un/-an branch drops v's own final
        vowel, so such a supporter witnesses the STEM and says nothing about the
        vowel the value ends in.
        """
        out = {}
        for p in PRE:
            for s in SUF:
                if not p and not s:
                    continue
                if not glide_ok(v, s):
                    continue
                for w, whole in (
                        (p + v + s, True),
                        # the -m-/-n- infix goes inside a consonant-initial root
                        ((v[0] + p + v[1:] + s, True)
                         if p in ("m", "n") and v[:1] not in VOW else (None, 0)),
                        # -un/-an swallow the root's last vowel. A glide and a
                        # swallowed vowel are alternatives, never both: the
                        # truncated stem ends in a consonant, so glide_ok()
                        # would refuse it anyway — it is refused above.
                        ((p + v[:-1] + s, False)
                         if s and v[-1:] in VOW else (None, 0))):
                    if w and w in self.voices:
                        out.setdefault(w, (p, s, whole))
        return out

    def vouched(self, v):
        """(supporting word, the shared character), or None.

        regular() verifies a form by finding its ROOT in the wordlist. This is
        the mirror case, and `xal` is the clean one: the citation form is 0×
        — his own headword note says so, 從未見過此簡單形式 — while `pxal` 147×,
        `msxal`, `smxal`, `snxal`, `pnxal` and `sxali` are all there. A root
        that only ever surfaces affixed is a listing gap of the purest kind,
        and a paradigm around it is stronger evidence than one bare listing.

        Same three guards as regular(), for the same reasons. Two supporters
        wearing DIFFERENT affixes, because one is a substring coincidence
        waiting to happen; four characters minimum, because a three-letter
        string is inside everything; and the gloss must agree, which is what
        separates `nasu` — vouched on shape alone by the conjunction `nasi`
        如果 — from the real ones.

        The agreement may come from any ONE supporter. Most of a paradigm is
        glossless in the wordlist, so requiring all of them would be requiring
        the listing gap not to exist.

        A fourth guard, and it is the one this rule can go wrong without.
        Supporters reached by the -un/-an branch have dropped the value's own
        final vowel, so they witness the STEM and are silent about the vowel the
        value ends in. That vowel needs a witness of one kind or the other:

          either a supporter carries v WHOLE — `mkmpeysa` for `kmpeysa`,
          `qmnaya` for `qnaya`, `tmnbru` for `tnbru` — which is what licenses
          their swallowed supporters `kmpeysun` / `qnayun` / `tnbraw`, since a
          root ending in -a really does lose it before a suffix;

          or the final vowel is itself a paradigm suffix, and then the sister
          slots replacing it is the morphology rather than a coincidence:
          `paqi` beside `paqan` / `paqun` / `paqaw`, `ltudi` beside `ltudan`.
          An imperative can have no whole supporter — nothing affixes an
          imperative — so requiring one would throw away the clearest claims
          the rule makes.

        With neither, nothing attests the value's last letter and the paradigm
        on offer is as likely to belong to another word: `biyu` was vouched by
        `biyaw` 109×, `sbiyaw` 281×, `nbiyaw` 快速樣子 and `pbiyi`, which are
        the paradigm of `biyaw` 快 — the word his sentence actually uses
        (你的傷口很快就會痊癒), and now what the map says for `biyo`.

        [batch 146] THE FOUR-LETTER FLOOR MADE THIS DOCSTRING'S OWN EXAMPLE
        UNREACHABLE. `xal` is three letters, so `len(v) < 4` refused it before
        anything above was ever asked, and so were `niq` 存在－居住, `rut`
        重壓於上, `hdu` 完成, `yup` 吹, `pru` 引起傳染 and `muk` — every one of
        them a root his book says is a root and the modern wordlist writes an
        entire paradigm of.

        The floor is borrowed reasoning. Everywhere else it guards a root found
        INSIDE a longer string, where three letters are inside everything; here
        the root is the whole word and the supporters are built by affixing it,
        so the shape can only over-generate the way `len(set(d.values())) >= 2`
        already refuses. What a shorter root does cost is anchoring, so at three
        letters the gloss must be his STRONGEST kind — Chinese he attached to
        the word as a word, never an example sentence, the same tightening
        vouched_root(), syncopated() and chained() take for the same reason.
        `rih` and `nta` are what that gate is for: `rih` 幾乎－接近 agreed with
        `krih` only on the 工作 of a sentence about throwing money away, and
        `nta` 邀請前往 only through `ptntun`, which is not its paradigm at all —
        his NTA is n- on the two-letter `ta` 我們, the frame of `lita`, and two
        letters is below any floor this book can honestly set.
        """
        if v in self.frozen or v in HAND_NOT_VOUCHED or len(v) < 3 or v in self.lex:
            return None
        d = self.derived(v)
        if len(set(d.values())) < 2:
            return None
        if not v.endswith(VSUF) and not any(w[2] for w in d.values()):
            return None
        his = self._his(v, slots_only=len(v) < 4)
        for w in sorted(d, key=lambda w: (len(w), w)):
            sh = self._agrees(his, w)
            if sh:
                return (w, sh)
        return None

    # ---- the two composed: a regular slot of a root nobody wrote down bare --
    def vouched_root(self, v):
        """(root, prefix, suffix, supporter, shared char) or None.

        regular() over a root that vouched() would accept rather than one the
        wordlist lists. `pspuhun` is the shape: `spuh` is never listed bare, but
        `spuhun`, `spuhan`, `spuhi`, `snpuhan`, `pspuhan` 醫院 and `pnspuhan`
        被治療過 are, and his gloss for the value is 使人施行醫治 — the -un
        sister of a slot the wordlist does list, off a root it does not. `natas`
        (n- on `atas`, which batch 113 vouched through `matas` 寫字) and
        `prijil` (p- on `rijil`, through `mrijil` 使彎曲) are the same.

        The evidence chain is one step longer than either rule alone: neither
        the value nor its root is listed, and the gloss agreement has to be
        taken against a SUPPORTER, because an unlisted root has no gloss of its
        own to agree with. So the gate is tighter at the other end — his Chinese
        must be a gloss he attached to the word AS a word, never one belonging
        to an example sentence. A sentence gloss describes a whole clause and
        shares a character with almost anything: it is what let `sktama`
        已故的父親 agree with `kmtama` 信奉上帝 on the 信 of an unrelated
        sentence, when the real morphology is `sk-` 'the late' on `tama` 父.

        The root is held to vouched()'s guards 1, 2 and 4 and to its four-letter
        floor, which is what keeps `snaah` out — the case that prompted the rule
        and does not survive it, since `naah` reaches only `pnaah`.
        """
        if v in self.frozen or v in HAND_NOT_ROOTED:
            return None
        his = self._his(v, slots_only=True)
        if not his:
            return None
        best = None
        for p in PRE:
            if not p or not v.startswith(p):
                continue
            b0 = v[len(p):]
            if len(b0) < 4:
                continue
            stems = [b0]
            if len(b0) > 4 and b0[0] not in VOW and b0[1] in "mn":
                stems.append(b0[0] + b0[2:])
            for st in stems:
                for sf in SUF:
                    if sf and not st.endswith(sf):
                        continue
                    # [batch 130] THE LEVELS DO NOT SHARE A MORPHOLOGY. This
                    # method splits for itself, and until now it split without
                    # the thing roots() does two hundred lines up: -un/-an
                    # SWALLOW a vowel-final root's last vowel, so `pspaan` is
                    # p + `spai` + an and `pspa` is not a root at all. roots()
                    # restores that vowel; this did not, which made a vowel-final
                    # UNLISTED root unreachable at level 4 however good its
                    # evidence — the same chokepoint argument as PRE, one level
                    # down. Found by asking why `-n` appeared to buy anything:
                    # it was not roots() gaining, it was this splitter mistaking
                    # `-an` for `-a` + `-n`. Priced alone: +17 types / 38
                    # occurrences, 0 de-verified, 3 re-cuts of which 2 are
                    # promotions. Six values are pinned out of it by hand above.
                    c0 = st[:len(st) - len(sf)] if sf else st
                    if not glide_ok(c0, sf):
                        continue
                    cands = [c0]
                    if sf in ("un", "an", "ani", "anay", "aneyi"):
                        cands += [c0 + x for x in VOW]     # the swallowed vowel
                    for c in cands:
                        if (len(c) < 4 or c in self.lex or c in self.frozen
                                or c == v):
                            continue
                        d = self.derived(c)
                        if len(set(d.values())) < 2:
                            continue
                        if (not c.endswith(VSUF)
                                and not any(w[2] for w in d.values())):
                            continue
                        for w in sorted(d, key=lambda w: (len(w), w)):
                            sh = self._agrees(his, w)
                            if sh:
                                cost = len(p) + len(sf)
                                if best is None or cost < best[0]:
                                    best = (cost, (c, p, sf, w, sh))
                                break
        return best[1] if best else None

    # ---- the root is listed; nobody ever glossed it
    def unglossed_root(self, v):
        """(root, prefix, suffix, slot, supporter, shared char) or None.

        regular() over a root the wordlist DOES list but never glossed, with
        the gloss agreement taken against one of that root's own inflections.

        `regular()` asks two questions of a root and needs both: is it listed,
        and does its gloss agree with his Chinese. For 138 types the first
        answer is yes and the second cannot be asked at all, because
        `attested_gloss.json` holds no gloss for the root. That is not a
        judgement against the word — it is a hole in the GLOSS TABLE, and this
        file has already convicted that hole twice by name: `qriban`, and
        `ttmaan` in the HAND_NOT_ROOTED note above ("what stops regular()
        reaching it is that `ttmaan` carries no gloss, which is the listing
        gap, not a morphology gap"). Most of a paradigm is glossless; the
        wordlist glosses the citation form and leaves the slots bare.

        So ask the paradigm instead. `ptbgi` is the shape: `tbgi` is listed and
        bare, but `tbgan` 養家畜的地方 is listed too, and his gloss for the value
        is 託人餵養－使人餵養, agreeing on 養. The root's own inflection says what
        the root means.

        This does NOT reopen the SISUN trap. SISUN's root `sisi` HAS a gloss —
        用來濾酒的工具, the wine strainer — so `regular()` reads it, refuses it,
        and the value never arrives here at all. This rule fires only where
        there is nothing to read.

        The chain is the same length as vouched_root()'s — one affix step to a
        root, one paradigm step from the root to a supporter that speaks for it
        — and so it carries vouched_root()'s guard set verbatim: his Chinese
        must be attached to the word AS a word (`slots_only`), a four-letter
        root floor, the root unfrozen, the root's `derived()` yielding at least
        two DISTINCT affixes, and the whole-or-VSUF final-vowel witness. Its one
        respect in which the evidence is STRONGER is the reason it sits a level
        above: vouched_root()'s root is a hypothesis, and this one is a word the
        wordlist prints.

        Six of the 26 are pinned by hand above; the note there is the reading.
        """
        if v in self.frozen or v in HAND_NOT_UNGLOSSED:
            return None
        his = self._his(v, slots_only=True)
        if not his:
            return None
        best = None
        for c, p, sf, slot in self.roots(v):
            if self.gl.get(c) or len(c) < 4 or c in self.frozen:
                continue                    # regular() already had its chance
            d = self.derived(c)
            if len(set(d.values())) < 2:
                continue
            if not c.endswith(VSUF) and not any(w[2] for w in d.values()):
                continue
            for w in sorted(d, key=lambda w: (len(w), w)):
                sh = self._agrees(his, w)
                if sh:
                    cost = len(p) + len(sf)
                    if best is None or cost < best[0]:
                        best = (cost, (c, p, sf, slot, w, sh))
                    break
        return best[1] if best else None

    # ---- the root is glossed, and its own paradigm says otherwise
    def outvoted(self, v):
        """(root, prefix, suffix, slot, [(supporter, shared)]) or None.

        `unglossed_root()` without its precondition that the root be unglossed
        — and therefore a different claim, which is why it is a separate rule
        and a level below. There the gloss table was SILENT and the paradigm
        was asked in its place. Here the gloss table SPEAKS, `regular()` has
        read it, and it disagrees with his Chinese. The paradigm is asked
        anyway, and where it answers clearly the paradigm wins.

        It wins because the two are not equal evidence. A citation gloss is one
        editor's choice of one sense to print for a headword; a paradigm is
        that same wordlist writing the root out across its slots, and it cannot
        keep a wrong sense up for long. `paux` is the case the whole rule is
        for. The wordlist glosses it 犁田, to plough, and batch 148 refused the
        family on those grounds — 犁田 is not 翻轉 and no synonym line was
        going to make it so. That refusal was right on the evidence it had. But
        the same wordlist also prints `mknpaux` 反過來 and `mspaux` 會翻, and
        his own values are 翻轉（前後）and 使…被翻轉. Ploughing is turning soil
        over; 犁田 was the narrow sense, not the meaning. **The pin comes down
        because new evidence overturned it, not because the rule that set it
        was weakened** — `paux` is still not in SYN, and 犁田 is still not 翻轉.

        `qdriq` shows the same shape without a narrow sense: his 逃跑的人 —
        逃走 is not the wordlist's `qdriq` 床底 at all, it is the syncopated
        stem of `qduriq` to flee, and the supporter `qndriqan` 逃跑 is what
        says so. Two homographs told apart, as `kray` was in batch 149.

        **It does not reopen the SISUN trap, and for a reason that is now
        threefold.** `sisi` is glossed 用來濾酒的工具; that gloss disagrees with
        his SISUN 縫, so this rule is reached; and then NO inflection of `sisi`
        in the wordlist agrees with 縫 either. The paradigm is asked and
        declines. A trap that survives being asked directly is a stronger
        result than one that was never reached, and the log asserts it.

        Guards are `unglossed_root()`'s verbatim — his Chinese attached to the
        word AS a word, four-letter root floor, root unfrozen, `derived()`
        yielding at least two distinct affixes, whole-or-VSUF final-vowel
        witness — and then one more, because overriding a gloss needs better
        evidence than filling a hole:

        TWO independent supporters must agree, or one must agree on a whole
        two-character word. One supporter sharing one character with his gloss
        is how `qdriq` also matched 的人 out of 住在Driq 的人, and how `taril`
        matched 方 out of 地方 — a bigram of STOP characters, and a fragment of
        a fragment. Requiring a second voice or a real word cut 37 candidate
        roots to 13, and the 24 it dropped were the coincidences.

        **The bar counted the wrong thing for one batch [batch 154].** It was
        written `len(agree) < 2` — the number of distinct agreement STRINGS —
        which is not what "two independent supporters" means and is not what
        logs/dom152.py says in writing. Where three inflections all agree on
        the same character the set holds one item, so the rule scored 1 and
        refused: `siyang` 肉 had `ksiyang` 肥, `msiyang` 很肥;結實 and
        `pksiyangay` 使肥大 all answering his 養肥, which is the strongest
        evidence the rule has ever been shown, and it was thrown out for being
        unanimous. Counting supporters instead admits 12 roots / 24 further
        occurrences. **The coincidences the bar exists to catch are unaffected**,
        because a coincidence is one voice agreeing once — `taril` on the 方 of
        地方 has exactly one supporter however you count.
        """
        if v in self.frozen or v in HAND_NOT_UNGLOSSED:
            return None
        if v in HAND_NOT_OUTVOTED:
            return None
        his = self._his(v, slots_only=True)
        if not his:
            return None
        best = None
        for c, p, sf, slot in self.roots(v):
            if not self._gloss(c) or len(c) < 3:
                continue                    # unglossed_root() covers the rest
            # **The freeze gates SPELLING, and this rule asks about MEANING.**
            # `self.frozen` is the NAME freeze: it exists so l→r cannot rename
            # a man (`Sapah Sibar`), and tier N in build_modern_map.py is what
            # enforces that on the page. Nothing here can respell anybody — the
            # root is being asked what it MEANS, and a citation gloss reading
            # only 人名 is the one case where the paradigm cannot be outvoted
            # by it, because "this is a name" is not a sense a derived form
            # inherits. `banah` is the textbook case: cited 人名（男）, and 27
            # derived forms glossed 紅 (`embanah` 紅色的, `kbanah` 染紅,
            # `knbanah`, `gmbanah`) against his `mabanah` 將要變紅. Same
            # distinction as batch 156's `lex` (may be printed) against
            # `voices` (may be heard), one level further out.
            if c in self.frozen and not all(
                    NAMEGL.search(g) for g in self._gloss(c)):
                continue
            # The floor is 3, not 4. Elsewhere it guards a root found INSIDE a
            # longer string; here over-generation is already refused by the
            # two-distinct-affix and supporter bars, and the same borrowed
            # reasoning cost `vouched()` its own docstring example in batch 146.
            # It buys `pix` 壓 — `mapix` 壓在其上－按壓, `empapix` 被壓垮的,
            # supporters `pixi`/`mnpix`/`pixan` all on 壓.
            d = self.derived(c)
            if len(set(d.values())) < 2:
                continue
            if not c.endswith(VSUF) and not any(w[2] for w in d.values()):
                continue
            sup = []
            for w in sorted(d, key=lambda w: (len(w), w)):
                sh = self._agrees(his, w)
                if sh and not all(ch in STOP for ch in sh):
                    sup.append((w, sh))
            agree = {sh for _, sh in sup}
            strong = [a for a in agree if len(a) >= 2 and "=" not in a]
            if len(sup) < 2 and not strong:
                continue
            cost = len(p) + len(sf)
            if best is None or cost < best[0]:
                best = (cost, (c, p, sf, slot, sup))
        return best[1] if best else None

    # ---- the sister slots: a paradigm the wordlist writes with other suffixes
    def sistered(self, v):
        """(prefix, stem, suffix, [the sisters]) or None.

        `lmuan` is the case, and it is the one shape the four rules above
        cannot state. It is the -an slot of his LAMU 收集 paradigm — his own
        line reads °Lmamu, lamu, lmui, lmuan, lmuon — and the wordlist lists
        `lmui` and `lmuun`, the -i and -un slots of that same stem, but not it.
        regular() reaches it, because `lmu` IS listed, and then refuses on the
        gloss: the listed `lmu` is 碎粒 a crumb, a homonym, and the two sisters
        that would settle it carry no gloss at all. Most of a paradigm is
        glossless, so that is not an accident of this word — it is the normal
        state of the evidence.

        The claim here is about morphology and not about meaning: a stem the
        wordlist writes with two different paradigm suffixes takes the third.
        Two supporters wearing DIFFERENT suffixes under the SAME prefix,
        because one is a substring coincidence waiting to happen.

        No gloss gate — there is usually no gloss to read — so the guard is at
        the other end, and it is his: **the value must be a word he printed in
        a ° paradigm line**. That is his own statement that it is an
        inflectional slot rather than a word in its own right, and it is what
        keeps the nouns out. `sapi` 小鋤頭, a small hoe, decomposes as
        `sap`+`-i` beside the attested `sapan` and `sapaw` 舖床 — a hoe
        verified as the imperative of spreading a bed. His SAPE is a headword
        and appears in nobody's paradigm, so the gate refuses it; so are
        `ptasaw` (his 使沉澱澄清, against the paradigm of `ptas` 寫;紋面) and
        `srciqun`.

        The gate is not sufficient by itself — a slot of his can still be a
        homonym of a slot of theirs, which is what HAND_NOT_SISTERED is for —
        but 11 of the 49 shapes this rule finds are refused by it outright, and
        every one of the 11 is either a noun or a different root.
        """
        if v in self.frozen or v in HAND_NOT_SISTERED or v in self.lex:
            return None
        if not any(k in self.par for k in (self.inv.get(v) or [])):
            return None
        best = None
        for p in PRE:
            if not v.startswith(p):
                continue
            b = v[len(p):]
            for sf in SUF:
                if not sf or not b.endswith(sf) or len(b) - len(sf) < 3:
                    continue
                st = b[:len(b) - len(sf)]
                if not glide_ok(st, sf):
                    continue
                sis = sorted(p + st + s2 for s2 in SUF
                             if s2 and s2 != sf and glide_ok(st, s2)
                             and p + st + s2 in self.lex)
                if len(sis) < 2:
                    continue
                cost = len(p) + len(sf)
                if best is None or cost < best[0]:
                    best = (cost, (p, st, sf, sis))
        return best[1] if best else None

    # ---- the root's own vowel, syncopated ----------------------------------
    def awag(self, v):
        """(stem, suffix, shared char) or None. A root ending -aw writes -ag-
        before a suffix.

        The wordlist settles this on its own, 76 pairs to 2: `bglaw` gives
        `bglagan`, `bglagaw`, `bglagay`, `bglagi`, `bglagun`; `bhraw` gives
        `bhragan` … `bhragun`; `bgbaw` gives `bgbagi`, `bgbagun`. The two
        counterexamples are `smkaw`/`smkaway` and `mnegeaw`/`mnegeaway`, which
        keep the -aw and take -ay on top of it. So a suffixed form in -ag- is an
        ordinary paradigm slot whose citation form no rule above can find,
        because every one of them looks for the letters he actually wrote.

        His SPADAO family is the case that found it. p. 228 is about giving
        presents — 贈送－無償給予－送禮, 所贈送之物, and the example `Daxa wawa
        lodoç ka pnspdagan daxa` 他們送的（禮物）是兩隻小雞 — and modern Truku has
        the whole thing: `pspadaw` 慷慨（不計價的送人）, `pnpadaw` 送過的禮物,
        `emppadaw` 將…作為禮物. The map already wrote his unsuffixed forms onto it
        (`pspadao` -> `pspadaw`, `mpspadao` -> `empspadaw`). The four SUFFIXED
        slots fell through every rung and `roots()` then found `dagi` 要煮飯
        sitting inside `pspdagi`. Nothing was misspelled: his `pspdagun` IS the
        modern slot, and the dictionary was simply unable to say so.

        Two guards, both learned elsewhere in this file.

        The stem is restored by INSERTING a vowel, which is batch 166's syncope
        run backwards and carries the same burden: the gloss must be one he
        attached to the word AS a word, and the candidates are walked longest
        first in a deterministic order — batch 165's lesson that a greedy pass
        over an unordered set is a sample, not a rule. Longest first is what
        reaches `pspadaw` 慷慨 rather than bare `padaw`, and that matters here
        more than usual: the wordlist files `padaw` as 是「spadaw 不可靠的人」的
        詞根（無意義詞）, an entry its own derivatives refute. Landing on the
        prefixed stem is landing on the gloss somebody actually wrote.

        It refuses more than it takes. `pkagi` reaches `pakaw` 有刺的野草 against
        his 上鎖, `pnslhagan` has no gloss of his at all, and `knsrhagan`
        鬆弛、鬆開的狀態 against `ruhaw` 不緊 is the same word in two vocabularies
        with no character in common — right, and refused, because a rule that
        inserts letters may not also guess at synonymy."""
        if v in self.frozen or v in self.lex:
            return None
        his = self._his(v, slots_only=True)
        if not his:
            return None
        for sf in sorted(SUF, key=len, reverse=True):
            if not sf or not v.endswith(sf):
                continue
            st = v[:len(v) - len(sf)]
            if not st.endswith("ag") or len(st) < 5:
                continue
            bases = {st[:-2] + "aw"}
            for b in list(bases):                 # <n> is an infix, not a letter
                for i in (1, 2):
                    if b[i:i + 1] == "n":
                        bases.add(b[:i] + b[i + 1:])
            cands = set()
            for b in bases:
                cands.add(b)
                for i in range(1, min(5, len(b))):
                    for c in VOW:
                        cands.add(b[:i] + c + b[i:])
            for r in sorted(cands, key=lambda x: (-len(x), x)):
                if r not in self.lex or r == v or r in self.frozen:
                    continue
                a = self._agrees(his, r)
                if a:
                    return (r, sf, a)
        return None

    def syncopated(self, v):
        """(root, prefix, suffix, shared char) or None.

        regular() peels affixes off a value and asks whether what is left is
        listed. It can delete a vowel at the END — the one -un/-an swallow —
        and nowhere else, so a root that loses its FIRST vowel under
        affixation is invisible to it. His TONGOX 品嚐 is the case: the root
        `tunguh` is listed, his own paradigm line reads °Tmongox, tongox,
        tngoxe, tngoxan, tngoxon, and modern writes those slots on the
        syncopated stem — `ptnguhi` 給…品嚐 is in the wordlist, which is
        p + tnguh + i. So `tnguhi`, `tnguhan` and `tnguhun` are ordinary slots
        of a listed root and no rule above can see them.

        That syncope is already documented in CLAUDE.md running the other way:
        GAMIL 根 is the root, and "where it took root" is `Tgmilan`, never
        *Tgamilan. Truku writes no schwa, so the root's first vowel goes the
        moment anything is prefixed. This is the same process read backwards —
        re-insert a vowel after the first consonant and take the reading only
        if THAT is the listed word.

        Inserting a letter he did not write is a weaker inference than peeling
        off one he did, so the gloss burden is heavier than regular()'s, and it
        is the burden vouched_root() already carries for the same reason: his
        Chinese must be a gloss he attached to the word AS a word. A clause
        gloss shares a character with almost anything, and here it is what put
        his `nta` on `nita` 我們的, his 塵土 `empnmu` on `namu` 你們的, and his
        使變肥 `psyangi` on `sayang` 今天；現在 — three pronouns and a calendar
        word reached through example sentences. The gate refuses all of them.

        It costs six correct claims that have no slot gloss to offer — `hlingan`
        off `huling` 狗, `mritan` off `mirit` 山羊, `pttuyun` off `tutuy` 起來,
        `shngi` off `hungi` 健忘, `mswiwil`, `psyangun` — and they stay pale.
        That is the right way round: most of a paradigm is glossless, so a rule
        this speculative should fail closed.
        """
        if v in self.frozen or v in self.lex:
            return None
        his = self._his(v, slots_only=True)
        if not his:
            return None
        best = None
        for p in PRE:
            if not v.startswith(p):
                continue
            b0 = v[len(p):]
            if len(b0) < 3:
                continue
            for sf in SUF:
                if sf and not b0.endswith(sf):
                    continue
                st = b0[:len(b0) - len(sf)] if sf else b0
                # Nothing was syncopated unless the first two letters are both
                # consonants — that cluster is the whole signal.
                if len(st) < 3 or st[0] in VOW or st[1] in VOW:
                    continue
                if not glide_ok(st, sf):
                    continue
                for c in VOW:
                    r = st[0] + c + st[1:]
                    if r not in self.lex or r == v or r in self.frozen:
                        continue
                    sh = self._agrees(his, r)
                    if not sh:
                        continue
                    cost = len(p) + len(sf)
                    if best is None or cost < best[0]:
                        best = (cost, (r, p, sf, sh))
        return best[1] if best else None

    # ---- the root's root: a glossless root one step from a glossed one ------
    def chained(self, v):
        """(root, base, prefix, suffix, how, shared char) or None.

        Every rule above stops at the first LISTED root and asks its gloss.
        Most of a paradigm is glossless, so that question often comes back
        empty even when the root is exactly right — `qnqgu` is q-n- on `qqgu`,
        which regular() reaches through the infix branch and then abandons,
        because `qqgu` is a corpus token nobody glossed.

        But a glossless root is often one obvious step from a glossed one, and
        it is the same regular morphology roots() already knows:

          the reduplication  `qqgu` is CV- on `qgu` 公雞叫聲, `sskuxul` on
          `skuxul` 喜歡, `kkhnuk` on `khnuk` 要軟. CLAUDE.md's tier D says a
          CV- reduplication makes no new lexeme, so the base's gloss IS the
          reduplicate's gloss. PRE has no doubling entry and never will — a
          doubled initial is not a prefix — so nothing else can reach these.

          the second step  the root is itself a regular inflection: `swiwil`
          off `wiwil` 垂, `psriyux` off `riyux` 換, `psupu` off `upu` 共. Five
          of the ten are `ms-` reciprocals sitting on an `s-` form, which is
          ordinary Truku morphology twice over.

        `kkhnuk` shows why the fallback earns its keep even when the root IS
        glossed: it is listed and glossed 使...便宜, only the price sense, while
        his Pkkhnuk is 為了使（某物）更鬆軟. The base `khnuk` 要軟;要便宜 carries
        both, so the base recovers a sense the reduplicate's own listing
        dropped.

        Two steps of inference is one more than vouched_root() and syncopated()
        take, so it carries their gate and for the same reason: his Chinese must
        be Chinese he attached to the word AS a word. That gate is not
        decoration here — it is the whole difference between the rule and a
        coincidence. Ungated this finds 16 shapes; the gate refuses six, and
        those six are every illicit spelling in the set (`nniyah`, `nslikaw`,
        `spsqrinut`) plus `msneanak` and `ssdhaun`. Everything it admits is
        licit.

        What survives the gate on a pronoun is `msdeita`, his Msdita 善於交際的
        ——友好的——與我們來往的, off `deita` 我們. Batch 116 refused `nta` twice
        on that same character, so the distinction has to be stated: 我們 is
        junk when the claim is WHICH pronoun — `nta` and `nita` both mean 我們的
        and the character cannot choose between them — and it is evidence when
        the claim is a derivation OF the pronoun, which is what his own gloss
        says in words. The modern dictionary settles it from the other side:
        its whole sociable-associate vocabulary is `msixal`, `mssixal`,
        `sixal`, `mrrawiq`, `ggdangi`, and not one of them is shaped remotely
        like Msdita, while `msd-` + a listed root is a pattern with 33 siblings
        (`msdalih` off `dalih`, `msdara` off `dara`, `msdrudan` off `rudan`).
        """
        if v in self.frozen or v in self.lex:
            return None
        his = self._his(v, slots_only=True)
        if not his:
            return None
        best = None
        for c, p, sf, slot in self.roots(v):
            if len(c) > 3 and c[0] == c[1] and c[0] not in VOW:
                b = c[1:]
                if b in self.lex and b != v and b not in self.frozen:
                    sh = self._agrees(his, b)
                    if sh:
                        cost = len(p) + len(sf)
                        if best is None or cost < best[0]:
                            best = (cost, (c, b, p, sf, "redup", sh))
            for c2, p2, sf2, slot2 in self.roots(c):
                if c2 == v or c2 == c or c2 in self.frozen:
                    continue
                sh = self._agrees(his, c2)
                if not sh:
                    continue
                cost = len(p) + len(sf) + len(p2) + len(sf2)
                if best is None or cost < best[0]:
                    best = (cost, (c, c2, p + "|" + p2, sf + "|" + sf2,
                                   "step", sh))
        return best[1] if best else None

    # ---- his own paradigm, where the wordlist has nothing to say ------------
    def his_family(self, v):
        """(root, prefix, suffix, [his supporters], shared bigram) or None.

        `unglossed_root()` fires where the wordlist lists a root and never
        glossed it, and asks the root's own modern PARADIGM in the gloss's
        place. That works while some slot of the paradigm carries a gloss. For
        eleven types it does not: the root is bare, and every slot the wordlist
        prints for it is bare too. The wordlist is not disagreeing with him —
        it is silent from end to end, and `_agrees` returns None for want of
        anything at all to read.

        So ask HIS paradigm. `ngangah` is the shape. The modern wordlist lists
        it and glosses neither it nor any of its three slots; Pecoraro has four
        separate cards on it — `pnngangah` 表現得像啞巴、像白痴, `mnngangah`
        白痴——笨蛋——傻子——啞巴, `nngangah` 從（原本）啞、痴的狀態而來,
        `pngangah` — and they agree with each other on 啞巴 and on 痴 across
        entries he typed at different times. Four independent statements about
        one root are a gloss for it, and they are the only gloss there is.

        The distinction from the SISUN trap is the same one `unglossed_root()`
        draws: this fires ONLY into silence. Where the paradigm speaks and
        disagrees — `msilung` against `silung` 海, `snulu` against `sulu` 屁股
        — the disagreement is evidence and the value stays pale. Measured,
        that is the larger half of the bucket and it is left alone.

        Two guards carry the weight. The agreement must be a BIGRAM and not a
        single character: two glosses of his own share 的 and 使 and 人 by the
        nature of his prose, and a one-character match between two entries by
        the same author at the same desk is worth much less than between two
        independent sources. And it takes TWO supporters, not one, because one
        cross-referencing card is a restatement and not a corroboration —
        `pnkltudan` and `pkltudan` carry the same sentence and would otherwise
        vouch for each other in a circle.
        """
        if v in self.frozen or v in HAND_NOT_FAMILY:
            return None
        his = self._his(v, slots_only=True)
        if not his:
            return None
        best = None
        for c, p, sf, slot in self.roots(v):
            if (c not in self.lex or self._gloss(c) or len(c) < 4
                    or c in self.frozen):
                continue
            d = self.derived(c)
            if len(set(d.values())) < 2:
                continue
            if not c.endswith(VSUF) and not any(w[2] for w in d.values()):
                continue
            if any(self._gloss(w) for w in d):
                continue          # the paradigm speaks; unglossed_root() owns it
            sup = []
            for w in sorted(self.fam.get(c) or ()):
                if w == v:
                    continue
                sh = self._bigram(his, self._his(w, slots_only=True))
                if sh:
                    sup.append((w, sh))
            if len(sup) < 2:
                continue
            cost = len(p) + len(sf)
            if best is None or cost < best[0]:
                best = (cost, (c, p, sf, [w for w, _ in sup], sup[0][1]))
        return best[1] if best else None

    def _bigram(self, a_zhs, b_zhs):
        """Two Chinese glosses sharing a two-character run. `_agrees` reads a
        gloss out of the tables; this compares two glosses given directly, and
        it takes only the bigram tier — see his_family()'s note on why."""
        if not a_zhs or not b_zhs:
            return None
        _, h2 = self._chars(a_zhs)
        _, r2 = self._chars(b_zhs)
        return sorted(h2 & r2)[0] if h2 & r2 else None

    # ---- he names the word himself -----------------------------------------
    def crossref(self, v):
        """(the word he names, root, shared char or None) or None.

        Every rung above reads his gloss as a MEANING. Sometimes it is not one.
        `rnjingan`'s entire gloss is （ldingan 的過去式）, `mritan`'s is
        MILIT 的斜格形, `ktbnaw`'s is MTBNAO 的否定形, `hlingan`'s is
        XEULING 的斜格形式 — grammar and a name, with no semantic content
        whatever. `_agrees` cannot fail on these so much as it has nothing to
        weigh: the Han characters left after the pointer is removed are 的過去
        式, which agree with everything and therefore with nothing.

        But the pointer is better evidence than any gloss. Every other rule in
        this file INFERS a root by peeling affixes and then argues the
        inference is right. Here he states it. `rnjingan` is `ldingan`'s past
        tense because he wrote that down, and `ldingan` is the `rjingan` 開始
        that the morphology independently proposed.

        Two shapes:
          (a) the token he names IS a listed root the morphology found. His
              statement and the affix analysis agree, and nothing else is
              needed.
          (b) the token names a word that decomposes to that same root — he
              points at a sibling rather than at the root itself.

        Both require the pointer to land on the root the affix rules FOUND,
        and that requirement is the whole of the rule's safety. A third shape
        was written and measured and is deliberately absent: where the
        morphology finds no listed root at all, the pointer could be allowed
        to supply the only candidate, with a gloss agreement demanded in
        exchange. It gains ten types and every one of them is wrong in the
        same way. His 參見 and his 較常說 are SEE-ALSO notes — `loai` 外部
        carries 較常說：NGANGOT, and `nilaq`, a mushroom, cross-references
        another mushroom — so the pointer names a synonym, not a form. The
        gloss then agrees for the obvious reason that synonyms mean the same
        thing, and what comes out is `loai`'s spelling certified by a modern
        word that is not `loai`. A cross-reference is evidence about the root
        of a word he is analysing, never about the spelling of a word he is
        merely comparing.

        The Latin-token scan is loose on purpose and (a)/(b) are what make it
        safe: he writes French and Italian in his notes, but a foreign word
        cannot pass unless it coincides with the root the affix rules already
        found. HAND_NOT_XREF holds the four it still reaches wrongly.
        """
        if v in self.frozen or v in HAND_NOT_XREF:
            return None
        his = self._his(v, slots_only=True)
        if not his:
            return None
        ptr = self._pointers(v)
        if not ptr:
            return None
        cands = {c for c, _, _, _ in self.roots(v) if c in self.lex}
        hit = sorted(cands & ptr)
        if hit:
            return (hit[0], hit[0], None)
        for t in sorted(ptr):
            for c, _, _, _ in self.roots(t):
                if c in cands:
                    return (t, c, None)
        return None

    def _pointers(self, v):
        """Every romanized token in his gloss, in modern spelling where the
        map knows it. He cites in his own orthography and in caps."""
        out = set()
        for z in (self._his(v, slots_only=True) or ()):
            for t in LATIN_TOK.findall(str(z)):
                t = t.lower().replace("ç", "").replace("’", "'")
                if not t or t == v:
                    continue
                out.add(t)
                if t in self.raw2mod:
                    out.add(self.raw2mod[t])
        out.discard(v)
        return out
