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
#
# Three more in batch 197, and all three carry one of his prefixes, which is why
# no tagger caught them and why name_population.json — a generated file, not a
# place to write by hand — could not hold them. § Mksipao ka dTome 「Tomé 和他的
#家人住在對面」: d- is his collective, the man plus his household, and the corpus
# writes the bare name tumi 16 times. § Saon namo smku knuwan ka skBoxil 「你們
# 什麼時候要去埋葬 Borhil 的遺體？」 and § SkTadao 「已故的 Tadao」: sk- is glossed
# on his own SK card as the second sense, *feu*, the late — a prefix he says is
# reserved for humans named or titled. boxil is already in the population as a
# bare name and the ILRDF registry lists both bowxil and tadaw. A name with a
# prefix on it is still a name, and no wordlist will ever list the prefixed form.
#
# Two more of the same kind. § Ongat xeni ka dBiyang da; wada tx'dil da! 「Biyang
# 一家不在這裡了；他們已經搬走了。」 — biyang is in the population and the registry
# both, and this is the collective d- again, the family of. § N'ima ka libul nii?
# NDiyan xo? … Adi! N'yako! 「這些褲子是誰的？是 Djian 的嗎？……不！是我的！」 — n-
# is the possessive his YAKO card is written to explain, and Djian is the man his
# GALUP card names as the one who made the peace. Neither prefixed form is
# listed, and neither ever will be.
#
# ndiyan was written here and taken out again, and the reason is worth keeping.
# It is not pale — the DOM says w-raw, green, because his spelling contains no
# o, l or x and the char rules hand it straight back with no map entry at all.
# A name in HAND_NAMES that is not a map value is inert, so the only way to
# colour it would be an identity entry in manual_map, and that entry would be a
# claim: that the modern spelling of his Diyan is diyan. His French writes the
# man Djian, and the modern register spells that sound with c or j as often as
# with d. One occurrence is not worth a spelling verdict we cannot back.
#
# nkmurisaka and dmurisaka finish a job this list started: murisaka and
# mkmurisaka were ruled names long ago, and the other two prefixed forms of the
# same place were left pale. His own MK card translates it — § Mkmorisaka ka
# yako 「我是森坂人。」 — so Morisaka is 森坂, the Japanese-era name of the village,
# and he uses it as one: alang Morisaka, mkMorisaka the people of it, nkMorisaka
# whose it is, ddCristo mkMorisaka its Christians. mk-, nk- and dm- over a place
# name are three slots of the same word, and a wordlist lists none of them.
HAND_NAMES = """sibal liwis mikat ingay lauken tatu talan banan lobyaq lubyaq
opic upih sikat imin timin tain pilin akit dloan lautan hidi eku tsay puti
stbaku mici dcristu tensu semento kodyo kaityo diko diku cristo yordan xelyo
xatso xaibyo tanso tenso tagahan murisaka mkmurisaka sitang efunang aman atwi
atuh denki banasi otun utun taolan taulan
dtumi sktadaw skbowxil dbiyang nkmurisaka dmurisaka
daman mkefunang ddcristu put""".split()

# HAND_LOANS is to loan_population.json what HAND_NAMES is to the name
# population: the file is REGENERATED by build_modern_map.py on every map build,
# so a hand edit to it vanishes (batch 197 learned this on the name side, batch
# 199 on the loan side). The generator reads his `tag` for "emprunt"/"(J" and
# catches 123 entries; it cannot see a verdict he wrote into the gloss instead.
# `siba` is one: SIBA "Gazon (terme japonais)." 草坪（日語詞）— 芝生. Widening the
# tag test to a gloss regex was measured and rejected: eleven entries say
# japonais/chinois in a gloss and only this one is a borrowing. The others are
# QOLIT "Cyprès-japonais" (a native name for a tree), PILA on the Ami language,
# L'QNUX on the deer. A rule that tagged those would publish four native words
# as loans to darken one, which is the trade CLAUDE.md refuses.
# `handulu` joins it on the same footing (batch 200): G'LEQ 轉動 § Pgleqon mu ka
# xandolu (=Volant) 我來轉方向盤 — he glosses it himself with the French for a
# steering wheel, and it is Japanese ハンドル handoru. The verdict is in his gloss,
# where the tagger cannot see it, so the file cannot hold it.
HAND_LOANS = """siba handulu""".split()

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
#   gmquwaq his `gmqowaq`, second of blockers.md at 3 pairs, in § Ana khaya ka
#           quwaq dha, ga su gmquwaq tunux ka isu inu squwaq 「當別人高聲大談，
#           你只是搖著頭，一句話也不說」. One analysis, `gm-` + quwaq, and the
#           root is listed. The informant: "quwaq is mouth so gm- seems
#           reasonable".
#
#           WHY THE GATE REFUSED. His gloss for the form is 搖頭——把頭轉來轉去,
#           and the omnibus glosses quwaq 洞口 — the mouth of a sack, of a lid,
#           of a hole. No character in 搖/頭/轉 is in 洞/口. What makes the
#           refusal visibly an artefact rather than a doubt is that the ILRDF
#           online dictionary, fetched this same batch, prints quwaq as 嘴／
#           龍鬚菜／麻袋口／蓋口／洞口／嘴巴 at frequency 125: the wordlist
#           printed the derived sense and left the primary one out. Even so
#           嘴 does not share a character with 搖頭, because the sentence is
#           about what the mouth is NOT doing — `gmquwaq tunux`, mouthing with
#           the head instead of speaking. A gloss test cannot read that.
#   snkrawah his `snklawax`/`snqlawax`, third of blockers.md at 3 pairs, in
#           KLAWAX › Snklawax 處於不利——被犧牲, again under LUDAN › Msludan, and
#           a third time as his own headword SNQLAWAX — which he glossed
#           「？？－悲傷（？）－孤獨（？）－可憐（？）」, question marks and all.
#           He did not know this word. We can tell him what it is.
#
#           THE ROOT HAS TWO SENSES AND THE WORDLIST PRINTS ONE. `rawah` is
#           打開蓋子 in the omnibus, which is why the gate refused: 處於不利/被
#           犧牲/可憐 shares no character with 打開蓋子. The ILRDF dictionary
#           prints the entry with its Truku definitions attached, and the sense
#           list is not all about doors: `mangal gnumuk` 打開蓋子 and `beytaq
#           brhug` 鑰匙, yes, but also `ini qbqan` 婉惜 and `malu kuxul` 情緒穩定.
#           An open lid and an open heart are the same word.
#
#           THE K-FORMS ARE THE EMOTIONAL SENSE, AND THEY ARE ATTESTED WITH IT.
#           `smkrawah` 可惜 (freq 5) and `kmrawah` 捨不得（因需要不肯割愛）／愛惜
#           (freq 16); `mtrawah` is 心情開朗（輕鬆）. His form is the s<n>
#           perfective of the first of those, mechanically — `smkrawah` is in
#           attested_modern.json and s<m>/s<n> is the ordinary alternation — and
#           可惜 landing on a person IS 可憐. The 16-member `rawah` family in the
#           wordlist convicts nothing and acquits here: every k-form of it that
#           anyone has glossed is glossed with regret.
#
#           `snkrawah` itself is a miss in the online dictionary, as `tksaw` and
#           `gmquwaq` were: it indexes headwords, and this is a derived form.
#   mnalu   his `Mnalu`, in MALU › Mnalu 和睦相處——彼此相愛. m<n>alu is the
#           ordinary perfective of `malu` 好, which the online dictionary gives
#           at frequency 661 — the second most common word we have asked it
#           about. The gate refused on synonymy for the third time this run:
#           和睦/相愛 shares no character with 好, and "being good together" is
#           what 和睦 IS. His own note under the entry names MKMALU as the
#           frequent equivalent, and `mkmalu` is in attested_modern.json.
#
#           THE SPELLING IS THE CLAIM, AND IT IS HIS OWN LETTERS. m-n-a-l-u
#           unchanged; the map already holds the identity, because `l→r` would
#           otherwise make *mnaru of a word modern Truku writes with l (malu,
#           smalu, snalu). Verifying moves the colour, not a letter.
#
#           HIS SECOND `Mnalu` IS A DIFFERENT WORD and this ruling does not
#           claim otherwise. NALU › Mnalu is 頂替——代替——以…之名, and modern
#           Truku's 代替 is `nirih`; neither `nalu` nor `naru` is listed, so
#           that card's root has no modern reflex under either letter. What
#           carries across to it is only the orthography, which is unchanged.
#   pnguwan his `Pngoan`/`pngoan`, 3 pairs, in PONGO › Pngoan 綁紮——已打好的結
#           and twice more under SLOXAO, both times about a knot that will not
#           come undone.
#
#           THIS ONE WAS NEVER A GLOSS PROBLEM. `roots()` reached `pgu` 藜 —
#           goosefoot, the plant — and nothing else, so the gate was ruling on
#           an analysis nobody would defend. The word is `pungu` + `-an`, and
#           `pungu` is 膝關節／繩結／關節／膝蓋 at frequency 26. His 已打好的結
#           and its 繩結 share 結 outright: had the analysis reached the root,
#           the ordinary gloss test would have passed it without a hand at all.
#           The wordlist has `pnpungu` 做繩結 as well, so the knot sense is in
#           both sources. A knee is the knot of a leg; it is one word.
#
#           A RUNG WAS PRICED FIRST AND REFUSED. `awag()` exists because a root
#           in -aw writes -ag- before a suffix, and the wordlist settled that
#           76 pairs to 2. The parallel claim — a root in -u writes -uw- — has
#           121 forms of the right shape in the wordlist and 23 where a vowel
#           can be restored to a listed root, which looks like support until the
#           23 are read: `huway` 慷慨, `buwan`, `ruway` are roots in their own
#           right, so `gmhuway` is `gm-huway` and not `gmihu-ay`. After that
#           only `mktru` -> `mktruwan` survives inspection. One supporter is not
#           two, and a rule built on it would be a shape test with a story.
#           `mktruwan` does do one job here, which is the narrow one it can do:
#           it shows the glide is WRITTEN, so the suffixed form of a u-final
#           stem is `pnguwan` and not `pnguan`.
#   embqru  his `mbq'lo`/`mbqlo`, BQ'LO › Mbq'lo 滿是凹凸與高低不平——崎嶇不平,
#           and in BALAE › Mtbalae about levelling a road: 把凸起的地方鏟平.
#           `bqru` is 肉瘤／痛風；關節石 — a lump on a body — and the gate refused
#           because a bumpy road shares no character with a tumour.
#
#           THE FAMILY HAS ALREADY MADE THE EXTENSION. 89 members in the
#           wordlist, and two of them settle it: `dmpsbqru` 採樹瘤者, a gatherer
#           of TREE burls, and `sbqru` 長很多肉瘤, covered in them. A lump is not
#           confined to flesh in this word's own family, and a road full of
#           lumps is what he wrote.
#
#           `em-` + a listed root is routine here rather than a favour: 116
#           verified em- words are absent from the wordlist, mapped by the tier-W
#           schwa rule and verified off their roots. `embqru` is not in the 89
#           either, and this is the one thing the count cannot decide — a family
#           that large makes absence look like evidence, when what it shows is
#           that the wordlist files this root's em- forms as `empeebqru` and
#           `embbqru`. His word is the stative and it is spelled the way the
#           other 116 are.
#   pnsmkan his `pnsm'kan`, SMUK › Pnsm'kan 已釘之物；釘的動作（已完成）, and
#           again under D'XO about reinforcing a stake somebody drove yesterday.
#           p<n>-smuk-an, and the wordlist glosses `smuk` 金鋼樹（樹木名）: a
#           tree. The ILRDF entry prints 金鋼樹（樹木名）／**釘子**／蘇穆克（地名）
#           ／**鐵釘** at frequency 7 — the nail sense and the tree sense in one
#           entry, and the wordlist kept the tree. His 已釘之物 shares 釘 with it
#           outright.
#
#           The analysis is what failed, again: `roots()` offered `smka` 一半,
#           `smku` 保存, `mkan` 吃 and `psmkan` 讓…金鋼樹, because reaching `smuk`
#           needs the root's own u restored. That is the same shape as `pnguwan`
#           two batches ago and the same lesson — a refusal in the "gloss
#           disagrees" bucket is not always a claim about meaning; sometimes the
#           gate never saw the word.
#
#           His apostrophe is the evidence for the syncopated spelling: he wrote
#           `pnsm'kan`, a mark where the u had been.
#   snkiya  Batch 189. His `Snkia`, KIA › Snkia 關於同一件事, and the SN card —
#           one of his twelve affix cards — states the analysis itself: "Préfixe
#           composé indiquant le plus souvent: à propos de quoi … le S qui est
#           porteur du sens de cause, d'instrument, de but, suivi du N qui
#           indique le passé". So the word is SN- over KIA by his own account,
#           and every piece of it is modern: `kiya` 那／這樣／就是 at parquet
#           frequency 2,429 and ILRDF 681, `nkiya` 就是這樣 at 67 and ILRDF 16 —
#           the stem written with its y under a prefix, which is the only letter
#           in dispute — and s- productive over 3,218 modern types.
#
#           The gloss test cannot be passed here and the reason is structural,
#           not evidential: 關於 is what the PREFIX means. He says so on the SN
#           card. A gate that asks his whole gloss to share a character with the
#           root's is asking the root to carry meaning the affix supplies, and
#           `kiya` will never gloss 關於 because it does not mean it.
#
#           And the form is generated twice over. `roots()` offers `skiya` 飛
#           first, because s-n-kiya is also the ordinary preterite of the verb to
#           fly — a homograph, and the 飛 that looks like a disagreement is a
#           different word, not an argument against this spelling. Two
#           independent derivations landing on one string is why the corpus's
#           silence about `snkiya` is a listing gap: neither reading is rare, and
#           no wordlist prints every slot of every stem.
#   mskutu  Batch 190. His `Mskoto`, SKOTO › Mskoto 麻木的－起雞皮疙瘩的－凍僵的.
#           `roots()` finds the root on the first try — `ms-kutu`, and `kutu` is
#           listed, ILRDF frequency 56, glossed **因濕冷而發抖** with the note
#           `詞意：hnigan pkkran pnsbili` (the body shivering from cold damp). His
#           two sentences are about nothing else: five blankets and still 起雞皮
#           疙瘩, and 受了很多寒 … 都凍僵了.
#
#           The gate refused it on ZERO CHARACTER OVERLAP between two glosses
#           that mean the same thing. 因濕冷而發抖 and 麻木／雞皮疙瘩／凍僵 share
#           not one Han character, and no widening of the shape rules could ever
#           reach this: the disagreement is between two translators' vocabulary,
#           not between two words. This is the failure mode `_agrees` cannot see
#           from the inside, and the only instrument that catches it is reading
#           the two glosses.
#
#           The derivation is modern on both ends. `empskkutu` 會發抖 is in the
#           ILRDF dictionary — the same stem under emp-sk-, so the stem takes s-
#           prefixation in the shivering sense today — and his own root card is
#           SKOTO, i.e. s-kutu, which is the same statement made in 1977.
#   mritan  Batch 190. His `mlitan`, MILIT › Mlitan 「MILIT 的斜格形」. His head
#           MILIT is 山羊 and the map has had it as `mirit` 山羊／羊 all along,
#           parquet frequency 260. What was in doubt is only the oblique, and the
#           wordlist settles its shape without being asked: on a disyllabic CVCVC
#           root, -an is written with the first vowel GONE, **155 pairs to 1** —
#           `barah` → `brahan`, `barig` → `brigan`, `batul` → `btulan`. `mirit`
#           + -an under that rule is `mritan`, which is what the generator wrote;
#           and `mrit`, the bare syncopated stem, is in the lex too.
#
#           IT NEEDS TWO RUNGS AT ONCE, AND THE LADDER OFFERS ONE AT A TIME. The
#           morphology never reached `mirit` — it offered `mrit`, unglossed, and
#           `rit`, the sound a mouse makes eating — so the vowel has to go back
#           before anything can be read, which is rung 11. But rung 11 needs a
#           word-level Chinese to agree with, and his gloss here is a POINTER: it
#           names MILIT and states no meaning at all. Pointers are rung 15, and
#           rung 15 requires the pointer to land on a root the morphology found.
#           Each rung supplies exactly what the other is missing, and a cascade
#           of single steps cannot take two.
#   knsbusan
#           Batch 190. His SIBUS › Knsbusan 甜味—甜—甜或鹹的品質. kn-…-an is the
#           abstract-quality nominaliser, and the wordlist writes it over a
#           syncopated CVCVC root **18 to 1**: `busuk` 醉 → `knbsukan`, `biyax`
#           → `knbyaxan`, `dakil` → `kndkilan`. His root is `sibus` 甘蔗（作物
#           名）, ILRDF frequency 180 and 28 parquet tokens, and kn-sibus-an under
#           that rule is `knsbusan` — `busuk` → `knbsukan` is the same shape, the
#           same affix and the same "the degree of being X".
#
#           Zero character overlap for the second time in this batch: 甜味 against
#           甘蔗 shares nothing, while the ILRDF's own Truku definition of `sibus`
#           is `hangan pnegalang ngalan qmsiya` — the plant sugar is taken FROM.
#           The morphology predicts his gloss; the character test cannot see it.
#           `roots()` meanwhile offered `bus`, the sound escaping steam makes.
#   tnglaan Batch 190. His TG’LA › Tnglaan 逗留的時間, and his second sentence is a
#           man delaying in the temple while the crowd waits. Found by searching
#           the MEANING and not the letters: the ILRDF entry for `gila` is
#           nothing but a list of its own derivations — 「sgila 因…耽誤」、「sglaan
#           讓…耽誤」、「sglai 使…耽誤」、「mgila 耽誤」 — and `sglaan` carries
#           frequency 6. `tgila` is itself an attested modern type, which is his
#           TG’LA with the apostrophe standing where the i went. The -an form of
#           this stem syncopates in the family already (`sgila` → `sglaan`), so
#           `tgila` under the tn-…-an preterite nominaliser is `tnglaan`, his
#           spelling unchanged.
#
#           The refusal was a REAL HOMOGRAPH and not a bad analysis. `tgla` is a
#           modern word — 鷀, ILRDF note `詞意：sapuh ssalu sinaw`, the yeast
#           cake wine is made with. `roots()` found a word; it was not his.
#   pngraq  Batch 190. His `png’laq`, NG’LAQ › Png’laq 使人變傻／把人當白痴. The
#           root is listed and its ILRDF note states the sense outright:
#           `詞意：ungat pnegaya ni ungat knkla` 無知 — without manners and
#           without knowledge. That IS his 傻／白痴, and once again it shares no
#           character with it. The other sense the entry carries is 比女人陰蒂的
#           手勢, and it is the one the flat gloss list leads with, so the gate
#           weighed a rude gesture against his page about fools.
#
#           He supplies the confirmation himself: the facing sub-form is
#           `Pnng’laq`, and he writes `(= Ya bi pnng’laq !)` in his own example.
#           `pnngraq` IS an attested modern type, and so are `mngraq` (parquet
#           31), `mnngraq`, `maamngraq`, `pqngraqay`. The paradigm is in the
#           wordlist end to end; the bare causative is the slot nobody wrote.
#   ptudu   Batch 190. His `ptudo`, TUDO › Ptudo 培土－築田埂 — *butter —
#           construire les diguettes*. The root is listed, ILRDF frequency 51
#           and 11 parquet tokens, glossed 主幹, and the corpus says what that
#           is in use: `hiyi tudu` 脊椎, `tudu tgbaraw yayung` the upper reach
#           of a river, `tudu dgiyaq Cung-yang-san` along the Central Range.
#           `tudu` is the ridge, the spine, the axis; his causative MAKES one,
#           and a 田埂 is a ridge. Zero character overlap once more (主幹 against
#           培土／田埂), so the gate had nothing to weigh. The stem takes this
#           affixation already — `mntudu`, `pntgtudu`, `pltudun`, `ltudun` are
#           all attested and the bare causative is the unwritten slot.
#   pkngalan
#           Batch 190. His ANGAL › Pkngalan 被除去之物——除去時的情形, over a
#           sentence about slicing a man’s ear off. BOTH SISTER SLOTS ARE
#           ATTESTED: `pkngali` 讓他拿 and `pkngalun` are modern types, and this
#           is the -an slot of that same paradigm; `pkngatan`/`pkngatun` write
#           the pk-…-an shape out on a neighbouring stem. Underneath, `angal`
#           拿 is parquet 430 / ILRDF 35 and `ngalan` 收到；拿來當 is 136 / 193.
#           Rung 8 exists for exactly this and could not take it: it asks that
#           the word be one he printed in a ° paradigm line, and he printed this
#           one as a sub-form. His 除去 against the wordlist’s 拿 is one
#           translator’s word against another’s — no shared character, on a word
#           whose whole paradigm is in the wordlist.
#   embbuway
#           Batch 190. His `Mbboai`, BOAI › Mbboai 互相贈與. The confirmation is a
#           parallel carrying HIS EXACT FOUR CHARACTERS: `embbgay` is in the
#           ILRDF dictionary glossed 互相贈與, off `bgay`, the common word for
#           give. So emb- over a give-root means what he says his word means.
#           His own root is the rarer synonym — `buway` 給, ILRDF frequency 2
#           with a corpus sentence to itself (`ini buway. ini gealu utux ga.`) —
#           and emb- + root is the plainest derivation the wordlist has:
#           `embbaga`, `embbais`, `embbanah`, `embbarah`, `embbeytaq`, `embbgay`.
#
#           One trap avoided by asking: `embbeyway` looks like the same word and
#           is not. `beyway` is 彎曲的；心術不正, so `embbeyway` is 全都成彎曲的.
#   mtdahu  Batch 190. His `mtdaxo`, DAXO › Mtdaxo 尊敬者——仰慕者, over `Xbalao
#           bi troko ka mtdaxo sunan` 仰慕你的太魯閣人很多. `dahu` is listed at
#           ILRDF frequency 101 and 26 parquet tokens, `詞意：mqaras quri
#           spruun` 讚美, with a culture note that reads like a gloss of his
#           card: 在太魯閣部落有作為的人，會受到部落族人的誇獎. His 尊敬／仰慕
#           against 讚美／稱讚 is the same act in two translators’ words — and
#           not one shared character, the sixth time in this batch.
#
#           The t- stem is written across its whole paradigm: `ptdahu` 會讓…驕傲,
#           `kntdahu`, `emptdahu`, `dmptdahu`, `emptndahu`. `mtdahu` is the plain
#           AF slot — the one form of the set nobody printed.
# ddngusun — batch 191. His DUNGUS (R) card reads 理所當然——相稱——合宜,
# with Msdungus 盡心盡力地 and Mpsdungus 將是公正的. ILRDF has dngusun 目標；對象
# (freq 12) and, decisively, the imperatives dngusa 別專注 / dngusi 去專注於 — so the
# root verb is "focus on, aim at". That is precisely what yields his 盡心盡力, and
# ddngusun (reduplicant + -un) is "what one aims at", hence 被視為理所當然的事.
# regular() refuses because 被視為理所當然的事 and 目標；對象 share no character —
# the batch-190 pattern exactly. No respelling is involved: dngusun is attested as
# written, and the dd- reduplicant is his own (DDngusun).
# stgtgut — batch 191. The analyser stops at tgtgut 最邊, but that is itself
# tg- (superlative) over gtgut 鄰居 (ILRDF freq 8, 4 corpus sentences). His card
# is 毗鄰的——鄰近的——相鄰的 with Ggtgut 非常近；鄰居們 — 鄰 in both, an
# outright gloss match, and he flags the root himself as "(R. = GUT ? (inconnue !)".
# stgtgut is s- (purposive) + tg- + gtgut, degeminated: "in order to be right next
# to", which is his 為了真正靠近 with 真正 carrying the tg-. The refusal is on the
# half-peeled root: 最邊 shares no character with 為了真正靠近. Spelling unchanged.
# kkrang (his kk'lang) — batch 191. Root krang/kran 碗掉下來破碎的聲音（擬聲詞）,
# ILRDF freq 14 (it returns the one entry for both kran and krang). The bridge to
# his 發抖——打顏 is attested on the same root: krkran 發抖, pkrkran 發抖 — clatter
# becomes shiver-until-you-rattle. Found by searching the lexicon for 發抖, not by
# shape. His card KK'LANG (R. ?) marks the root unknown and carries Mkk'lang
# 因寒冷或恐懼而顏抖的 / Tkk'lang 全身發抖的, so the reduplication is his base.
# Modern reduplicates the root as krkran, not kkrang; that is a cognate, and a
# cognate explains a word but never spells one. No pin — the char rule form stands.
# mkkrang (his Mkk'lang) is the m- slot of that same card and rides the same note.
# krhun (his K'lxon) — batch 191. The analyser roots it in krhi 烤 (roast); the
# root is kruh 旱地, which shares 旱 with his K'LOX 乾——乾旱——荒漠般的 outright,
# and krhan 烤乹 shares 乾 with his K'lxan 乾旱——貧瘦. krhun is kruh + -un with the
# vowel syncopated. One homophone off, not a spelling fault.
#   Near-miss worth keeping: he tags the card "(Q'LOX ? — parentée avec QOLOX =
#   crâne ?)", and quluh really is 光禿的山和不長毛髮的頭／骷骳／貧瘦地 — one lemma
#   holding both his 頭骨 and his 荒漠般的. I repinned the whole K'LOX family to it
#   and the build answered LOST 3: kruh, krhan, mkruh were already dark, on
#   attested spellings, with the right glosses. His tag carried a question mark;
#   attestation outranks it. The QOLOX card keeps quluh, the K'LOX card keeps kruh.
# knslaan — batch 191. His headword KSLAAN is the modern lemma letter for letter:
# kslaan, ILRDF freq 5, 缺乛. His card reads 饣餓虛脫－精疲力竭, which is what
# lacking food and strength is; no character is shared, and no respelling is
# involved on this card at all. Knslaan is that word in the accomplished form,
# kn- + kslaan, and his own gloss for it is the pointer "d° dans la forme
# accomplie" — a gloss with no content for the test to read, the mritan shape.
# His proposed root "(R. = KSUL ?)" is in no register; it stays his question.
# empraqat (his Mplaqat) — batch 192. laqat is attested nowhere, raqat is
# (三叉的箭頭／電塔), so l→r is unopposed and every part of the word is attested:
# emp- + raqat. The gloss test refuses because 耀田 shares nothing with 三叉的箭頭.
# The link is the object, and both notes describe it the same way: ILRDF glosses
# raqat as "aga leesug" 三叉的箭頭 and "qra samaw" 電塔 — the fork-shape word —
# while his own LAQAT (R) note says the 耀 was made of branches arranged in a fan
# (呈扇形排列的樹枝). Recorded as an inference from the object, not a character match;
# no web source confirms the tool sense.
# mrbuq (his Ml'boq) — batch 192. Root rbuq 深, 23 corpus sentences, one of them
# a definition in the language: "Qnrbqan aji dhqun qmita o kisa balay bi rbuq"
# 看不見的深才是真正的深. His L'BOQ (R) is 洞－凹穴－車轍溝痕 and Ml'boq is
# 呈凹陷－形成凹穴, which shares no character with 深 — but his own sibling Mtl'boq
# reads 被挖空、凹陷者－下陷者－深. Same card, same root: one slot passes the test
# and the other fails on nothing but which synonym he reached for.
# pnrikit (his Pnlikit) — batch 192. likit is attested nowhere; rikit is, glossed
# 不去打獵／搵一次米糕的量／易跌倒／瘁 — and 瘁 is exactly his LIKIT (R)
# 殘廃的－畑形的－小兒麻痺, with no character in common. mrikit is attested too and
# renders his Mlikit 殘廃的人, so the register already carries another slot of the
# same card. pn- + rikit, "to act the cripple".
# empklutut (his Mpklutut) — batch 192. His LUTUT (R) 親屬－有關聯－相連 is
# lutut 親戚／連結, which matches on 親 and 連, so the head passes the test; and
# pklutut is itself attested (繼續). The refusal is confined to the pk- branch,
# where his gloss drifts to 慕藉－強身 — to knit a person back together — and
# touches neither 親戚 nor 繼續. emp- + pk- + lutut, every part attested.
# knluusan (his Knlsan / knl'san) — batch 192. The sub carries no gloss at all,
# and the root luus is glossed 成熟的人, which does not obviously mean his LUUS (R)
# 獨自－孤獨－單身. The ILRDF Note decides it: luus is defined in Truku as
# "mqsuqi knwauwa ni knrisaw" — past girlhood and past young-manhood (uwa the
# unmarried girl, risaw the young man, mqsuqi gone beyond). That is not maturity
# in general but staying single past the age for it, which is his card, and it is
# what his sentence says: it is your unmarried state that leaves you carefree.
# kn- + luus + -an, the vowel restored from his knl'san.
# pknluun (his Pknluon) — batch 192. The analyser offers klui (no gloss) and nlu
# 從…省下; the verb is pkmalu 使……有益的, ILRDF freq 56, which is the slot above
# it on his own MALU card: Pkmalu 治好——修復——改善——修理 and Pknluon
# 想要、應當改善的事物 — 改善 in both, his own gloss making the link.
# malu syncopates its ma- in derived verbs (kmluun 醫治；痊癒, smluun 修理／造出,
# pskmluun), and the nlu...un shape his spelling gives is itself attested in
# snluun / snluan. No -un form of pkmalu is attested in any spelling, so nothing
# outranks the char-rule form and the pair is his -un of pkmalu.
# penduk (his Pnduk) — batch 192. Root enduk 門;橫隔膜, the vowel restored from
# his pnduk. His NDUK head is 門——關閉的 — 門 in both, so the head passes — and
# mnduk 曾關門 is attested, carrying his Mnduk. Only the p- slot fails, because
# there he wrote 使之關閉 instead. A door and a diaphragm are both what closes an
# opening; p- + enduk is to make it so.
# empngpung (his Mpnpong, which he also spells mpngpong) — batch 192. Root
# pngpung 山崗 is attested and has six corpus sentences, every one of them a rise
# of ground — 高山斜稜, 山頂, 奇萊山南峰. His head PNPONG is 山頂＝隆起一個包
# and shares 山 with it; the refusal falls only on the sub, where he wrote
# 起伏的－隆起成小丘 — 小丘 and 山崗 are the same hillock with no character in
# common. I first read his two spellings as two modern words and repinned the
# slot to mpngpung; tier W had already answered that. ^mp is one type in 38,687,
# modern writes the schwa, and his transcription drops it exactly as it does
# word-internally. The map was consistent at render time and only the source
# keys looked split. No prefixed form is in ILRDF — mpngpung, mngpung, pkpngpung,
# pnkpngpung all return nothing — so the register carries the root alone.
# haduri (his Xdoli) - batch 193. A homophone decided by the sentence. His
# letters read two ways: hduri, the imperative of hdur 不同意／反對, which matches
# his vowels exactly with nothing dropped; or haduri, the imperative of hadur
# 獵首筵席, which needs the first schwa restored. The example is Mark 1:44 —
# 要按真正的禮儀獻祭，好給他們以此為見證 — and "oppose it according to the true
# rite, as a testimony" is not a sentence. Dropping a schwa is his standing
# habit (xnglyeq → hnegliq, mpnpong → empngpung), so the shape argument that
# favours hdur is the weaker one.
#
# The hadur family is one of the deepest in the register and it is unanimous:
# mhadur, phadur, pnhadur, hnadur all 舉行馘首宴, beside emphadur, dmphadur,
# gmhadur, ghadur, hhadur, khadur, knhadur, ptghadur, sghadur — some 25 forms.
# -i is the ordinary imperative. The refusal is the character test alone:
# 獵首筵席／貪吃 shares nothing with 獻祭, though the ritual feast is exactly what
# the verse asks be offered.
# qmapah (his Qmapax) - batch 193, 2 pairs. The register glosses the bare root
# qapah 不穩定, which is why the gate refused his 塗抹、鋪開、覆蓋. But that is the
# derived sense, and sgqapah says so on its face: 不穩定（引申「容易被動搖」）.
# The core is adhesion — sqapah 貼 with six corpus sentences, every one of them
# sticking (剝芋頭的皮容易沾黏在手上, 米飯黏在他的嘴巴上, 左手指就黏在竹棒上),
# and msqapah 粘起來. His own two examples are pasting: cow dung spread over a
# drying-yard, and 糊上報紙 newspaper pasted round the walls of a sleeping place.
# q<m>apah is the ordinary AF infix on that root and the slot is simply
# unwritten. 貼 and 塗抹 share no character, which is the whole of the refusal.
#
# tpssagan (his tpssagan, unchanged) - batch 193. His card head SASAO is sasaw
# 蔭涼（有遮蔭的地方乘涼）and his own gloss is 可以去乘涼的地點 — 乘涼 in both, so
# the head is confirmed by character match. The blocker is only the derived
# place-noun: root ssagan 被遮住 is attested, and so are the siblings tssagan,
# cssagan, ssagi, ssagon, ssagun, ptsasaw, csasaw, tsasaw. tp- on a passive to
# make a place-of noun is regular, and 被遮住 shares nothing with 涼爽 — the
# shade and the coolness are one thing named twice.
# sdmatan (his Sdmatan) - batch 193. Another homophone the analyser lost: it
# offered dmatan 用…配菜 for a card glossed 悲傷、鬱悶、思念的地點、時間, because
# the register glosses bare damat 菜 and sdamat 菜；菜餚. But the same root
# carries a second sense across six independent forms — csdamat 思念;寂寞;哀傷;
# 哀慟, csdamatay 思念, kdamat 想念;懷念, kmdamat 好想念, empkdamat 會懷念,
# smdamat 久仰／想念 — and tnsdamat 悲傷；憂傷 shows sdamat itself takes it as a
# stem. His head SDAMAT shares 思念 with csdamat outright.
#
# The -an is the locative/temporal, which is what his card says it is (的地點、
# 時間) and what his sentence uses: 去年是非常悲傷的一年, a year that was a time
# of sadness. sdamat + an syncopating to sdmatan is the patas → ptasan 學校
# pattern, regular and attested; his spelling needs no correction at all.
# psnegulun (his psn'gulun) - batch 193, one map pin and one ruling. Every
# other form on his SNUGUL card was already on the right family: snugul→snegul
# 跟／跟隨, psnugul→psnegul 是跟隨, mpsnugul→empsnegul 要跟隨, msnugul→msnegul,
# mssnugul→mssnegul, smnugul→smnegul, all dark. Only the apostrophe form fell
# through the lexical match to the blind char rules, which took his gul to gur
# and dropped the schwa his apostrophe is marking — giving psngurun, a word
# whose offered roots are ngur 石頭堆積狀 and gur 成群來到的聲音（擬聲詞）.
#
# One form of a root escaping to a different spelling is exactly what the
# consistency rule is for. Pinned to psnegulun and ruled: psnegul 是跟隨 is
# attested, -un is the ordinary patient suffix, and his sentence is a causative
# patient — 讓所有學童都跟在Djiro後面, make them all follow.
# knsupu (his Knsopu) - batch 193. His own gloss names the construction:
# 團結、親密、和睦的強烈程度 — a degree, which is what kn- makes. Root supu 一起
# is attested, with msupu 在一起, mnsupu and psupu beside it, and kn- is fully
# productive across the register (knhdur 反對, knhadur, knbtut, knslaan). The
# refusal is the character test alone: 團結／親密／和睦 and 一起 name one thing
# twice with nothing in common. His sentence is the degree read plainly —
# 看到他們如此融洽，任誰都會羨慕.
# the STA"TO card (smteetu, steetuun, knsteetuan) - batch 193, seven pins and
# three rulings. The whole card was unmapped: his " marks a long vowel and the
# lexical match never saw through it, so every form fell through to itself and
# sat pale. Modern writes that vowel ee — steetu 上坡, 11 corpus sentences
# (無論爬坡或下坡, 爬坡時還會滑下來) — and his head gloss is 斜坡上－上坡, sharing
# 上坡 outright. msteetu and snteetu are attested and take his Msta"to and
# Snta"to; steetuan 上坡路 is attested and shares 上坡 with his Knsttoan 上坡－斜坡.
#
# Three slots the register does not write. smteetu is the <m> AF beside attested
# snteetu, the same slot in the other aspect. steetuun is steetu + the patient
# -un, concatenated exactly as attested steetuan concatenates -an. knsteetuan is
# kn- on that attested -an noun. All three shapes were checked the tier-W way,
# against what modern types really look like: 110 types end -uun, 138 end -uan,
# 109 are kn-…-an. Four sentence pairs on one card, and the refusal throughout
# was the same character test — 攀登 shares nothing with 上坡.
# batch 194 — the TG'LA card, decided against an attested value.
# His head is TG'LA 逗留－慢慢來, with the note 某些說話者清楚地讀成 TGI…, and a
# sub spelled "Tmg'la (tngila)" — he records the vowel his apostrophe elides.
# The map had the card split: mtgila dark with the vowel, tgla/mtgla/tnglaan dark
# without it. tgla is attested, but its gloss is 麴 (yeast) — a homophone, not his
# word. The register writes this root with the vowel: gila is glossed 「tggila
# 拖拖拉拉」的詞根, tggila is attested and runs in text (tggila mtutuy kdjiyax ka
# swayi snaw 弟弟常常賴床), and tgila is attested. Not one vowelless inflection
# (mtgla tmgla tnglaan kntglaan) is attested or occurs in any corpus sentence.
# So the unsuffixed slots are pinned onto the vowel — tgila, tmgila, mtgila, and
# his own parenthetical tngila. An attested value can still be a wrong value;
# only the gloss catches it.
#
# The -an slots are NOT. I pinned tnglaan and kntglaan to the vowel too and had
# to take both back: the batch-190 note above already held the evidence, and I
# had not read it. The register syncopates this vowel before a suffix — sglaan
# 讓…耽誤 (freq 6) and sglai 使…耽誤 are attested, sgilaan and sgilai are not.
# So his Tnglaan and Kntglaan are the register-consistent shapes and were right
# as written; only kntglaan needed ruling (tnglaan was ruled in batch 190). They
# needed identity pins, not no pin: with the head pinned to tgila, root
# projection respells every slot on the card off it, so a slot the projection
# must not reach has to say so out loud. A
# root can be consistent and still take two shapes, if the split is conditioned.
#
# batch 194 — mtudu, on a standing finding rather than a fresh derivation.
# Batch 190 settled what tudu is: the ridge, the spine, the axis, glossed 主幹
# against his 培土／田埂 with zero character overlap. His Mtudo 凹凸不平的－變成隆起
# is the stative of that — ground that has become ridges — and the register
# attests mntudu, the ⟨n⟩ perfective of this exact word, alongside pltudun,
# ltudun and pntgtudu. The strongest supporter a slot can have is its own
# perfective.
#
# batch 194 — sghuwayan, where the sense is attested one slot away.
# His XOAI (XOWAI ?) › Sgxoayan (Sgxwayan ?) 謝意－感激, and his own parenthetical
# spells the w the map restores. sghuway 靠…慷慨 is attested and carries the
# affixation; huway and ghuway 分享 are attested; and mhuway is glossed 恩慈／
# 感謝／慷慨／謝謝 — the thanks sense his card is about, on this very root, in a
# sister slot. The gate saw only 謝意 against 慷慨 and refused.
# batch 194 — ptkanun, and the root that changes shape between slots.
# TIKAN 去殼－舂（穀物）renders split in the register: the head is cikan and the
# causative is pcikan (both dark, ti→ci), but every suffixed slot keeps tkan- —
# tkanan, tnkanan and the attested tkanun 杵, which runs in text as dmux o tkanun
# ni skuu 以備舂米或保存用, exactly his faire décortiquer. Ptkanun is p- on that
# -un stem, so its two supporters are on the same card and they agree: pcikan
# vouches for the causative slot, tkanun for the stem. The gate refused only
# because the sub-gloss 使去殼 drops the 舂 his own head gloss carries.
#
# batch 194 — mtkumax and tmkumax, ruled on shape where the gloss will not help.
# TKUMAX 翻天覆地－翻倒－陷入混亂 has four slots; TKUMAX→tkumax and Ptkumax→ptkumax
# 使...不準 (freq 12) are attested dark, so the register writes this root with
# these exact letters and takes the causative on it. m- and tm- are the two
# remaining slots and neither changes a letter of his spelling. The ILRDF gloss
# 不準；沒有命中 shares nothing with 顛倒, but its one corpus sentence is a deadfall
# trap being tripped — 整塊石板被動快速壓下 — which is his renversé, not a miss.
# Pecoraro marks the tm- slot "Tmkumax (?)" and writes "(tkumax ?)" in its
# example: his doubt is whether the form exists, not how it is spelt, and the
# sister slot Tmikan on the TIKAN card above shows tm- is a real slot here.
# batch 194 — slungan, a word he names himself.
# His slongan blocks two sentences, on the AN card and on XOAI › Kxoai, and the
# AN card carries his own gloss for it: parler à la mer (Silong = mer) 對著大海
# 說話. The register attests silung 海 and gsilung 海, the latter with 222 corpus
# sentences (qsurux gsilung 海魚); his silong already renders silung dark. The
# -an form syncopates the penult, the same conditioning just established on the
# TG'LA card by sglaan against sgilaan — silung + -an gives slungan, which is
# what the map already proposed. Nothing here was in doubt except the suffixed
# shape, and the card above had already settled that.
# batch 194 — msilung, the second slot of the sea root.
# His "SILONG › M"silong 變成水窪、水塘, the house that will 變成一片水. silung 海 and
# gsilung 海 are attested and his own head silong already renders silung dark, so
# this is m- on an attested stem. The gate saw 海 against 水窪、水塘 and refused on
# zero character overlap — the same refusal it makes every time a stative names
# what the noun becomes rather than what it is.
# batch 194 — ptbnagun, where the analyser had the wrong root and the family
# had the right one. His TBNAO 豐滿－胖嘟嘟 card is in the register almost slot for
# slot: tbnaw 胖子, mtbnaw 胖, kntbnaw 胖, and ptbnaw 使胖的, which is his Ptbnao
# 使肥胖 word for word. Only his -un form ptbnuon broke away, and it broke to
# ptbnuun off the analyser's root tbnuun 要堆壓 — a shape hit on a root that
# means to pile and press, not to fatten. The root ends in -aw and this root's
# own -an form shows what happens under a suffix: kntbnagan is attested, w→g.
# The register does it everywhere else too — bgbaw/bgbagun, bglaw/bglagun,
# bhraw/bhragun, bkraw/bkragun, btraw/btragun, dhaw/dhagun. So ptbnaw + -un is
# ptbnagun, and the card now renders one root instead of two.
#
# batch 194 — ntlawa, ruled off its sister and not off its root.
# TLAWA › Mtlawa 1° 水深之處 2° 呈藍色、紫色的, two sentences: the deep sea to cast
# nets in, and a face gone blue. mtlawa is attested and glossed 藍色 — his second
# sense exactly, sharing the character. The bare root tlawa is not attested, so
# the gate had nothing to test and fell back on lawa 呼叫／等一等, which is a
# different word. No letter of his ntlawa changes.
# batch 194 — maabgu and empaabgu, and a prefix the map was writing too short.
# BUGO › Mabugo 快要變成湯（粥）的, with Ana qoqo mpabugo! The root is not in doubt:
# bgu 湯 is attested with a full family — tmbbgu 喝湯, tnbgu 湯的主人, tgbgu, ttbgu.
# The prefix was. The map had mabugo→mabgu (dark by rung, not by attestation) and
# mpabugo→empabgu, but the register does not write the inchoative that way: maa-
# has 468 attested types and empaa- 51, while ma- before a consonant cluster is
# absent and the seven bare empa- types are all emp- on an a-initial root
# (empatas, empajiq). maabagu 形成焦黑 is the same shape on a b-initial CCV root.
# So his devenir soupe is maabgu and his sur le point de is empaabgu. This drops
# mabgu, which was dark on a rung that spelt the prefix short; one root, one
# prefix, and the card now says the same thing twice instead of two things once.
# batch 194 — msska, where the root gloss names a place and the word names what
# happens there. RUNUG: Mrunug do, asi msska ka ana bbtunux da 發生地震時，連岩石
# 都會裂開. ska is attested 中間／當中／裡面 and the gate stopped at 中間 against
# 裂開. But the register itself takes this root to the splitting sense — skaun is
# glossed 切成半粒, cut into halves — and the rest of the family is there too:
# cska, kska 其中, mgska 在中間, pgska 使放中間, gmska. The prefix is ms-, with 67
# attested types, and the doubled s is what ms- does before an s-initial root:
# mssaang from saang, mssbarux 相互換工 from sbarux. A rock that msska splits
# down its middle, which is the root's own meaning applied to itself.
# batch 195 — three cards, each dark but for one slot.
#
#   pnsdahung  His DAXONG › Psdaxong 造成瘀傷, and the card renders dahung,
#              mtdahung, msdahung, psdahung all dark. Only the ⟨n⟩ perfective of
#              the sub-head was left, on a root the register glosses 吸血草 for
#              the plant and 瘀血 for the bruise, with sdahung 很多瘀血 beside it.
#              The word is his own sub head with an infix.
#
#   drnai      DULUN › Dmulun, Dlnai ta tmaan xo? 我們去求爸爸. The analyser's root
#              was drna 鹿鞭, a homophone the sentence rules out; the card itself
#              holds the answer, since Dlnani → drnani 向…禱告 is already dark and
#              is this exact stem one suffix over. durun 傳話 and dmurun 祈求 are
#              attested, drnanay 向神祈禱 shows the same syncopated drna- stem, and
#              -i on such a stem is attested in sglai. Decide slot by slot when a
#              homophone exists: 鹿鞭 does not ask a father for anything.
#
#   ggitan     GIGIT, whose gloss he leaves as ？？ — the French says intervention
#              souvent répétée pour demander, 纏人. gigit 固執 is attested and
#              carries fourteen derivations (smgigit 堅持地, tggigit 都堅持的,
#              pnegigit 有堅持的, sknegigit), every one of them keeping the vowel
#              because none of them suffixes. His g'gitan does suffix, and his
#              apostrophe stands exactly where the syncope falls — the same
#              conditioning batch 194 established with sglaan against sgilaan.
# batch 195 — pnmaxan, whose supporter is the next word in the sentence.
# GIMAX › Gmimax 相混, § Pnmaxan daxa sinao gnmaxan paxong 他們給人喝了摻膽汁的酒.
# gnmaxan is attested and already dark — the same syncopated max- stem with the
# same -an, differing only in the prefix, standing two words away in his own
# example. gimax 混合, pgimax 使混合；配著 and gmimax 配 are attested besides. The
# analyser had root max 手掌擊打聲, an onomatopoeia, because the syncope hides the
# gi- that the card head shows.
# batch 195 — kmpstrngun and empkslaan, two prefixes on two attested stems.
#
#   kmpstrngun IYUX 堅持要——極其渴望, § Kmpstlngun na bi laqe na ka Iwal, Iwal 很想
#              讓兒子成婚. The stem is not in doubt once the gloss is read the right
#              way round: strung is 相遇；遭遇, and pstrung — making two people meet
#              — is glossed 婚姻 outright. pstrngun is attested as well, and kmp-
#              carries 26 attested types. The analyser's strngun 對抗；交戰的對象 is
#              the same stem seen from the battlefield rather than the wedding.
#
#   empkslaan  KSLAAN 饑餓虛脫－精疲力竭, § …aadi so mpkslaan muda "lu da 免得半路上餓
#              昏了. kslaan is attested, empk- has 91 attested types, and his mp-
#              is the schwa tier W restores. Nothing here needed deciding except
#              that 缺乏 and 饑餓虛脫 are one word — running out, and running out
#              of what keeps you walking.
# batch 195 — shnkan, where the register glosses the homophone, and mnpunu.
#
#   shnkan   LATAT > Lntadan, § Ga tloong sapax sxnkan ka Iboq, Iboq est en prison.
#            The gate saw hnkan and read the register's gloss for it: 把…便宜, from
#            hnuk 便宜. Wrong root. His own book has the right one — XMUK "enfermé -
#            clos - fermé", i.e. hmuk 關；封住 attested, with the sub-form Sxmuk =
#            shmuk 關著, also attested. The register's word for a prison is built on
#            it: hmkan 關（被關；坐牢）, and the corpus says kolo hmkan outright for
#            監獄. So hnkan is two words, and only one of them is cheap.
#
#            The letters need no change at all beyond x->h. The shape is his own
#            perfective locative, and the proof is in the same sentence: Lntadan,
#            which his paradigm line derives as ltadan -> l<n>tadan. Infix <n> after
#            the stem's first consonant, prefix s- in front — hkan -> h<n>kan ->
#            shnkan, the house one has been shut up in. Snlaqe and Pnlwaan on these
#            same two pages are the same derivation. I checked the m against the
#            scan before ruling, because the whole case turns on one stroke: page
#            147 has a two-stroke n, not hmkan's m, and his nk never answers to a
#            modern mk anywhere in the map (0 of 41).
#
#   mnpunu   L'BONG > L'mbong, § Mnpuno nxoqel ka lodoç so, ta poule est morte du
#            choléra. punu is attested, but the register glosses it as a personal
#            name — which is a fact about the name, not about the word. His card
#            PUNO 霍亂－精神錯亂 is the word, and modern empunu is attested: his own
#            Mpuno "avoir le choléra" under tier W. mn- carries 1259 attested types.
# batch 195 — two shrinking garments, a hole in a roof, and a want the corpus
# never happens to express.
#
#   nslbu    L'BU > Msl'bu, § Wada nsl'bu pax bnxoan mo dngdang ka lukus, the coat
#   empslbu  shrank after I washed it in boiling water; and § Mxa mpsl'bu ka n'iso,
#            yours will shrink too. His root card L'BU is 短－簡短－不高 and modern
#            lbu is attested as 不長 — the same word, sharing not one character with
#            the card's 變短－縮水－縮短. That is the standard refusal here: synonyms
#            with no Han in common. ns- carries 40 attested types of exactly this
#            build, ns- on a plain root (nsburaw, nsbiyaw, nsdangi), and pslbu is
#            attested for the causative, which is his Psl'bu and gives empslbu its
#            stem under tier W.
#
#   nruq     L'NGO > Kl'ngo, § Ma so niyax n'loq dnamux ..., why come and pierce the
#            roof right over my bed. Same trap as shnkan one card earlier: ruq is
#            attested and glossed 吞食聲, a swallowing noise, which is a homophone
#            and not this word. His card LOQ says 洞－被刺穿的－破裂的 and lists Mloq
#            and Ploq — modern mruq 破 and pruq 洞, both attested, both his. The bare
#            n- prefix sits on 613 attested stems, so nothing here is a new shape.
#
#   kmkmalu  MALU > Mkmalu, § Mkmalu so bi ka iso o, ini ko kmkmalu ka yako, you'd
#            like to get well, I wouldn't. Not one kmkm string occurs in the whole
#            ILRDF corpus, which is a fact about this word and not about its class:
#            kmk- is attested 8 times over and every gloss is a want — kmkdudux 想率
#            先, kmkeisil 想到別處, kmkjiyah 想…旁邊, kmkla 好希望會. It is the k-form
#            of mkm-, which is his own Mkmalu, attested. The one register word that
#            looks like an answer is not one: kkmalu occurs 8 times and is the
#            purposive, 為了…好 — dudug knan kkmalu, guide me toward good. Wanting to
#            recover and being led to goodness are two forms, and only one is his.
# batch 195 — the other half of a homophone split, and a form he spelled the way
# the rule predicts.
#
#   nrbu         NGOLOQ > Msngoloq, § Msngoloq pax nl'bu ka laqe, the child has been
#                bleeding from the nose since this morning. His nl'bu was being sent
#                to lbu 不長, which is the short root — and this is the morning one.
#                The split was already half made: ml'bu is pinned to mgrbu, because
#                his L'BU card carries a sub-form "Ml'bu (M'lbu ?) (R. = L'BU ?)
#                Matin", the query mark his own. Modern rbu is attested and glossed
#                早上（破曉至黎明）, l->r is the plain char rule, and bare n- sits on
#                613 attested stems — paah nrbu, since the morning that was, exactly
#                as nsbiyaw is the time that was. Pinned, because the head projects.
#
#   empsneanak   NANAK > Psnanak, § Xnut mpsnanak sdyaqon ka xea, our teacher sets
#                some people aside. sneanak 另外保留 is attested and is his 擱置一旁;
#                seanak 看輕；輕視；瞧不起 is the same card's other half, which is his
#                "il fait des différences entre personnes". The build is attested
#                whole one word over: empsnegul 要跟隨 is emp- on snegul, exactly as
#                this is emp- on sneanak.
#
#   snguli       NUGUL > Snugul, § Xmuya ka ini so snugul tmaan (ini so snguli ka
#                tama)? Why do you not follow your father? snugul is already pinned
#                to snegul 跟隨, attested, with smnegul, msnegul, psnegul and
#                empsnegul all in the register behind it. What was left was the -i
#                slot, and it needed no deciding: the antepenultimate vowel drops
#                before a suffix — sgila -> sglai, silung -> slungan, gigit ->
#                ggitan — so snegul + -i gives snguli. That is his spelling, letter
#                for letter. The rule and the man who heard it agree, and his own §
#                puts both voices on one line for the paradigm.
# batch 195 — the whole PADYAQ card, which the register knew as a vegetable.
#
#   kpajiq     PADYAQ > Mpadyaq, "généralement employé pour désigner la couleur
#   knpajiq    verte", 一般用來表示綠色. § Ini kpadyaq ka n'iso, yours is not green;
#   spkpajiq   § Ngalun so manu spkpadyaq galyeq so, what do you dye your cloth
#              green with; § lala bi ini kdka knpadyaq daxa, the greens of the
#              mountain leaves differ greatly.
#
#              pajiq is attested many times over and glossed 菜, 蔬菜, 青菜 — and a
#              woman's name, and a village in Xiulin. Not one of those shares a
#              character with 綠色, which is the whole refusal. His card had already
#              explained the connection in one line, and the register confirms it
#              without needing him: empajiq is glossed 綠色 and mgpajiq 綠色的. The
#              colour and the vegetable are one word here, as green and greens are
#              one word in English.
#
#              Three slots, three prefixes, all attested classes: k- on 3149 types
#              (ini k-, the negated stative), kn- on 691 (the quality of, which is
#              precisely his 色調 — how green a leaf is), spk- on 9 (spkdahang,
#              spkeekan, spkguraw — what one uses to make a thing so).
# batch 195 — a knot that is also a joint, and the word for a hospital.
#
#   pnpnguan  PONGO > Ppongo 打結, § Ya bi pnpngoan ima ka nii? Who tied this knot?
#             The analyser offered pgu 藜, goosefoot, which is not it. His own card
#             head reads "Noeud - articulation", 結－關節, and the e-dictionary's
#             pungu, freq 26, glosses as 膝關節／繩結／關節／膝蓋 — both his senses in
#             one entry, the knot and the joint. A knee is a knot. His sub-form
#             Pngoan "ligature - noeud qui est fait" already shows the syncope this
#             needs: pungu loses its first vowel before -an, as sgila and gigit do,
#             giving pngu-an, and he wrote it that way himself.
#
#   pspuhaw   SAPOX > Smapox, § Ida bi mnqan sapox ka Sikat! PSpoxao ta n'xali da!
#             Sikat may be poisoned — quick, let us get her treated. The register
#             has the whole family: sapuh 藥, smapuh 擦藥 and also 祭；祭典, which is
#             his card's "rite liturgique" exactly; psapuh 看病, msapuh 醫生. And it
#             has this very stem one suffix over — pspuhan is glossed 醫院, the place
#             where one is treated. pspuhaw is the same word said to the person you
#             are carrying there.
# batch 195 — sugarcane, and a rope the char rule spelled with the wrong letter.
#
#   ssbusun  SIBUS > Ssibus, § Ssbusun mo idao ka kia, I will use this to sweeten
#            the rice. sibus 甘蔗 is attested and so is the card head itself:
#            ssibus, glossed 甜, which is his "1) très sucré; 2) pour sucrer" word
#            for word. Sugar in this language is the cane it comes from. The -un
#            slot syncopates as everything else does, sibus -> sbus before the
#            suffix, and he wrote it that way.
#
#   sgulan   SLOXAO > Msloxao 鬆的, § Sai mita ka kating s"gulan adi msloxao xo, go
#            and see whether the buffalo's tether has worked loose. This one was
#            pinned to sguran, which is the blind l->r rule and nothing more. The
#            root has an l and the register is unanimous about it: seegul 綁住,
#            enegul 綁著, negul 繫有, empeegul 要…綁住, egul, eegul, emptegul 抓著.
#            The r was never there to find. His " is the schwa he never writes —
#            the same fact that turned xnglyeq into hnegliq back in the map work.
#
#            Which leaves long or short, and that was already answered on this very
#            page of the notes: the S'LYEQ family takes the long stem bare and the
#            short stem suffixed, seeliq and smeeliq against sliqan and sliqi. So
#            seegul bare, sgulan suffixed — and his spelling is the short one.
# psmkun (b196). His SMUK card is glossed 釘；打入榫栓 and the § reads Ini toko!
# Psm'kun mo kingal dole 「這不夠；我還要再釘一塊。」 — he will nail one more plank.
# The analyser could not reach it: it offered smka 一半, smku 保存／放置 and a
# glossless smko, none of them about nailing, and the gloss table's own entry for
# smuk gives one sense only, 金鋼樹（樹木名）, a tree. The e-dictionary carries the
# word's other two senses, 釘子 and a Truku place name, and 釘子 is his 釘 exactly.
# So the gate refused on a gloss table that holds one of the word's three meanings,
# not on any disagreement about the word.
#
# The shape is the corpus's, not a reconstruction: psmkani 讓他在那山坡地種植金鋼樹林
# is p- + smuk + -ani with the u syncopated away, and his apostrophe in Psm'kun
# stands on precisely that vowel. That the corpus sentence is about planting smuk
# TREES and his is about driving in a nail does not matter here — what it attests
# is that modern Truku writes p+smuk+SUFFIX as psmk-, which is the one thing his
# spelling needed. psmkun = p- + smuk + -un.
#
# snka (b196). Under SPONG › Spngan 被測量的, § T'lo bi spngan ni snka 「只有三量半」
# — three measures and a half. The analyser resolved it to ska 中間／當中／裡面,
# which is the right root and the wrong sense, and 中間 shares no character with
# 半, so regular() refused. The half word is smka 一半 (f21, listed), s⟨m⟩ka; his
# snka is the same stem with ⟨n⟩ for ⟨m⟩. Both derived slots are listed and the
# corpus glosses one of them for us: snkaan in 半粒小米煮進鍋子裡會變成滿滿的
# — half a grain of millet — and snkana twice in a discussion of 以一概全, taking
# a part for the whole. The bare snka is what those two are built on.
#
# stmaqun (b196). His ST'MAQ › Mst'maq 壓碎－被壓碎者, § Stmaqun mo (stmaqon mo)
# kia ka bnuöl so 「我稍後會把你的李子壓碎。」 — he gives the variant himself.
# Every part is listed: stmaq 已爛了（外力）(f25) is the root, mstmaq 打爛 is his
# own Mst'maq, and the corpus has the imperative stmaqi in 看到蟑螂時，媽媽，趕快
# 踩死蟑螂啊！ — stomp the cockroach flat. 壓碎 and 已爛了（外力）are the same
# event described from its two ends, the crushing and the crushed, and they share
# no character, which is the whole of the refusal. stmaqun = stmaq + -un.
# muli (b196). His UMUL 含在口中吸吮 has two sub-forms, Mumul 吸吮－使其在口中融化 and
# Mulun, and the § is the imperative: Muli binao! Malu bi oqon! 「就讓它在你口中融化吧！
# 很好吃！」 The analyser read m-uli and offered uli 綁住…, to tie — a different word
# that happens to fit the letters. The right word is listed: mumul 含在嘴裡不咬碎, which
# is his head gloss almost character for character. mumul is m⟨um⟩ul, so the root is
# mul, and his own Mulun is that same stem in the patient slot; muli is the imperative
# of the pair, exactly as stmaqi stands to stmaqun. Neither bare mul nor muli is listed
# on its own — the parquets have no mumul either — so this is his family and one modern
# attestation of the stem, which is why it could not come through regular(): 含在嘴裡
# and 吸吮 share no character.
# pneydang (b196). Under HJIYAL, § Wada su hnjiyal ka pneydang su pila hu?
# 「你把弄丟的（並在尋找的）錢找回來了嗎？」 The root is listed twice over and the
# gloss table shows only half of it: peydang is 人名（男）there, and the e-dictionary
# adds the sense the sentence needs, 迷路, to get lost. The whole family is in the
# wordlist — meydang, mneydang 已迷路過, empeydang, ppeydang — so both halves of his
# form have modern witnesses: ppeydang is the p- causative of the root, mneydang the
# ⟨n⟩ preterite of it, and pneydang is the two together, the money that was got lost.
# 迷路 and 弄丟 share no character with each other or with the card's 找到, which is
# the whole of the refusal; the card is about finding because the finding is the
# question, and the lost money is what it is asked about.
#
# psnruun (b196). His Sn'lo 使人宣布－使人傳達－使人知曉 was already resolved to snru
# 敘述所聽到的 — the map has carried sn'lo→snru — but the slot in the § had fallen
# through to the blind rules and was printing psnluun with his l. Psn"loon (he offers
# psnloon himself in brackets) is p- + snru + -un: 「我想把這個好消息傳遍各處。」 The
# family is listed around it — smnru 講, psnru 被敘述, snruan, snruway, mssnru — and
# psnru is his own Psn'lo exactly, so the pin psn'loon→psnruun is the r his own head
# already has. Nothing lists the -un slot; every morph in it is listed. 敘述 and 宣布
# are one act described with two words, and they share no character, which is why
# regular() could not take it.
#
# pklilug (b196). KUDUS 活的－會動的 § Ini kudus ka tlangan, adi tdoa pklilu, and
# LILU › Pklilu (Plilu ?) 使它動 § Dyagi ko pklilu tdoloi mo nii — two sentences, one
# word. The root is in the register in two reduplications, klilug listed with no gloss
# and klglug glossed 要動, beside lglug 不安靜, mlglug 動／搖擺 and slglug 使之搖動;
# the map had already ruled his LILU onto lilug and klilu onto klilug on the strength
# of the listing. What was missing was the causative, and modern Truku builds it with
# pk- on exactly this shape: pkeuwit 使其疲累 stands to uwit 疲累 as pklilug stands to
# klilug. The unglossed twin is what stopped the gate — a root with no gloss cannot be
# agreed with — and the glossed twin one syncope away says 要動, which is his 使它動.
# ciyusun (b196, 2 pairs). His TYUSUN 烤－煎（炸）, and the contrast is in his own §:
# Uxai tyusun ka xei samat nii, doxon! 「這塊野味不是拿來炙烤的！是要拿來燒烤的。」 —
# tyusun is what doxon is not, pan-cooking against grilling. The root came through the
# map as ciyus and IS listed, with no gloss of its own, which is what stopped the gate;
# but its family is glossed all the way round and says one thing: dmciyus 炒菜者,
# emciyus 要炒, pnciyus 炒過的, pciyus 當…炒, mgciyus 像…炒的一樣. emciyus 要炒 is the
# same slot as his -un, so ciyusun is 要炒 with the other voice. 炒 and 煎 share no
# character, and a root with no gloss cannot be agreed with; both halves of the refusal
# are about the tables, not about the word.
#
# ppskngalun (b196). GALUP › Pgalup 使結合－使和好－使聯合, § Ndoa bi pgalup dxeaan
# ppskngalun so lnglongan daxa 「盡你所能使他們和好，好叫他們同心合一。」 The analyser
# offered skngali, unglossed, and never reached the word this is built on: pskingal
# 合一；成為一致 is listed, and it is his 使聯合 exactly. Modern Truku writes this root
# in both shapes — the full pskingal and the syncopated kngalun, also listed — so the
# stem skngal- of his form is the register's own, and kingal 一 and skingal 專一 stand
# behind both. What his doubled pp- adds is the second causative, one heart made of two.
# nskkuyuh (b197). KOYOX › Skkoyox 亡妻——已故的（妻子）, § Nskkoyox mo ka lukus gaga
# 「那些衣服是我亡妻的。」 Both parts are the register's. `kuyuh` is listed at 1,357 and
# glossed 女性;女人;女生;太太;婦女, `kkuyuh` is listed as its reduplication, and `ns-` is
# productive over the whole wordlist in exactly his sense — nsbiyaw 以前的, nshiga 昨天的,
# nsgbiyan 昨天傍晚的, 34 forms of it. The gate refused on characters alone: his 妻子
# against their 太太 is the same woman spelt with different Han, and the 亡 that makes the
# word is carried by the prefix, which no lexicon glosses because no lexicon lists an
# affix. Nothing here is a question about Truku.
# mrangah, nrangah (b197). LANGAX › Mlangax 大開的、敞開的 — *grand ouvert, béant* —
# § Mlangax bi ka l'xngun sapax na 「他家的門大開著。」 and § Ida nlangax ka npaqan daxa
# baga mo 「他們在我手上弄出的傷口還敞開著。」 `rangah` is listed at 15 and glossed by no
# table at all, which is the whole block; the corpus glosses it in sentences instead, ten
# of them, and they agree: 樹洞, 坑, 大空穴, 洞. A hollow is what béant describes from the
# other side — his door stands open like a cavity and his wound is one. Searched from the
# meaning as well as the letter: nothing of the shape langa-/mlanga- exists in modern
# Truku, and the words that carry 張開／敞開 are a different root end to end (ngaha 開口,
# kngaha 在張開, msaqa 張開), none of which his letters can reach. One root, attested,
# with the sense read off the corpus rather than off a gloss table that never wrote one.
# nsrijil, pnsrijil (b197). LIDIL › Mslidil 歪斜地站著的人 and › Pslidil 使之變歪、變扭曲.
# `srijil` and `psrijil` are both listed and both unglossed; the glossed member of the
# family is `mrijil` 使彎曲, which is his 使之變歪 with 曲 shared outright and the causative
# in the same place. The homophone is real and is decided slot by slot: `qrijil` 女人,
# `mkmqrijil` 成為某人的太太, `tmqrijil` 好女人 are a q- root about wives, and his card is
# about a beam nobody wanted crooked.
# mnspruq (b197). LOQ › Msploq 會爆裂的－會爆炸的, § Mnsploq s'xiga ka txoan mo 「我的爐灶
# 昨天爆炸了。」 `mspruq` is listed and unglossed, so the gate had nothing to agree with;
# its own family says the word twice over, and the two supporters are independent —
# pnspruq 被爆破 shares his 爆 and qqpruq 快破裂了 shares his 裂, one a passive and one an
# imminent. Behind them pruq 洞 and empruq 破洞: what bursts leaves a hole.
# pnskngalan (b197). KINGAL › Pskngalan （促成的）重新合一——被聚合起來的事物, and his
# own parenthesis names the sibling: Snkngalan = the spontaneous one. § Pnskngalan
# Pexo ka kana xxei alang ta 「我們村裡所有的人都被佩霍凝聚在一起。」 The analyser stops
# at skngali — listed, freq 2, glossed nowhere — exactly as it did on ppskngalun last
# batch, and for the same reason: it never reaches pskingal 合一；成為一致, which is
# listed at 16 and glossed in the Bible glossary. His 重新合一 and that 合一 are the same
# two characters, not a shared one. kngalun is listed too, so the syncopated stem
# skngal- is the register's own shape and not our contraction, and kingal 一 / skingal
# 專一 stand behind both. pn- -an is the ordinary past locative of the p- causative: what
# was made one. One slot over from a word this file already ruled.
# mnpgealuk (b197). GALUP › Mpgaluk (mpgalup) 作為橋樑的人——致力促成合一、建立團體的人,
# § Diyan ka mnpgalup dxeaan 「是 Djian 使他們和好的。」 with his own note that the word
# designates a Catholic priest. The p→k is HIS: he prints Mpgaluk beside mpgalup and a
# tag that names the fuller form is evidence, not a guess. The register writes the p-
# shapes of this root with the schwa — pgealuk 2, pggealuk 6 in the spoken corpus — so
# the map's value is the modern spelling of exactly the shape he wrote; what it is not
# is glossed, and that is the whole block. The gloss sits on the other side of the same
# root: empgaluk 神父, which is his ethnographic note verbatim, beside mgaluk 要連接,
# mggaluk 相互連絡 and pneggaluk 建立邦交 for his 促成合一、建立團體. galuk itself is
# glossed 衣扣, a button — the fastener sense of the same join — and a head glossed on
# one narrow sense is what batch 148 refused to let outvote its own family. mn- is the
# past of the m-/p- pair, a slot and not a new lexeme.
# pnkltudan (b197). LUTUT › Pkltudan (Pnkltudan ?) 被慰藉、恢復元氣的狀態, § Biyoq onoç
# nilit ka suyang bi pnkltudan 「羊奶是極佳的補品。」 and § Sinao ! Kia ka ngalun daxa
# pnkltudan 「酒！那就是他們尋求慰藉的地方！」 Two sentences on one form, which is why it
# was worth the reading. The analyser reaches ltudan — listed, freq 1, glossed nowhere —
# and stops there. Every part of the word is the register's own and glossed around it:
# lutut 連結／親戚 at 70 is his own head gloss 親屬（親戚關係）－有關聯－相連 in the same
# two characters, ltudun 接着, pltudun 接；連接 and pltudaw 讓…接上 gloss the syncopated
# stem, pltudan is listed at 2 and pnltudan at 24 — his exact slot, one k short. That k
# is his causative and it is the register's too: pklutut is listed at 12, and this file
# already hand-ruled empklutut off it. What the -an locative names here is where the
# joining lands on a person, which is his card's whole argument — 相連 is what family is,
# and being held together is what comforts. Nothing in the word is ours.
# kmpspusu (b197). PUSU › Snpusu 奠立－作為源頭、根源、起源、根基, § Adi so kmspusu
# (kmpspusu (?)) bulax kdusan ta xo? 「你難道不願意樹立我們新生活的榜樣嗎？」 His own
# parenthesis is the hesitation of a man writing down what he heard twice; both shapes
# are on the page and the map renders the one he printed. pspusu is listed at 2 and
# glossed nowhere — the block — while pusu itself is listed at 958 and glossed 主要的，
# 根本的, sharing 根 with his 根源 and 根基 outright. km- over a p- causative is the
# ordinary "become / act as", which is precisely his 使自己成為…核心.
# sshgan (b197). SAXOG › Ss'xgan 用來舀取的－供舀取用, § Blaxao so bi, byeqe ko ana manu
# ss'xgan mo bugo 「請給我個能舀湯的東西。」 The analyser offers shgi, listed at 4 and
# glossed nowhere, and gets no further. The root is glossed one syllable away: sahug
# 水瓢(舀水用) is the dipper itself, smahug its actor voice, and shgi / shgani are the
# register's own syncopated slots of the same word — sa·hug losing its first vowel is
# what his elision mark writes. His 舀 is in their 舀水用 literally. The reduplicated s-
# is the instrumental of instruments, which is why his gloss says 用來舀取的 and not 舀.
# Checked the homophone before ruling: sahu 毒害 is a different root and no part of this.
# ndmpatas (b197). SADYAQ › Mpsado 工人－受薪者, § Uxai nami ndmpatas ka yami; dmpsado
# yami ka yami 「我們不是讀書人，我們只是（勞力）受薪者而已。」 The word he needed for the
# contrast is the one the gate cannot see: dmpatas is listed at 4 and glossed nowhere,
# and n- is his negated-attributive slot. patas 信 at 737 and empatas 在…讀書 at 105 are
# the same root read as document and as schooling, with mkmpatas 想讀書 and sppatas 要讀書
# behind them; dm- is the register's own agentive plural — dmpatas is those people, and
# his French says *intellectuels* while his Chinese says 讀書人, which is 讀書 with a man
# on the end. A sentence that exists to deny a class still names it.
# smhngi (b197). SISIL — the omen bird — § Taya knsuyang sisil ta! Ilil xa, sisil ta!
# Smx'nge so? 「我們的 SISIL 對我們多麼有利啊！牠在左邊，對吧！你還記得嗎（＝你忘了嗎）？」
# The analyser cuts sm-hng-i and hng is nobody's root. The register writes this word nine
# times and glosses it every time: shngii 忘記 41, shngiun 忘記 22, shngian 忘記了 26,
# shngiaw 要忘掉, shngia 不要忘, shngiay 要忘, beside shngiyan, shngiyun, snhngian and
# phngi 16. Those are the s- forms; his is the same stem with the actor infix, which is
# the one slot of it no wordlist happens to print. The agreement is his own sentence
# gloss, and this is the shape pdrut was refused for — so it is worth saying why it is
# not that shape: there the shared 去 was an incidental verb of motion in a long clause
# about millstones. Here the clause IS the word, a two-word question whose only verb is
# this one, and his parenthesis translates it 忘了 against a family glossed 忘記 nine
# times. A gloss that thin can still be the whole sentence.
# snsikan (b197). SSIK 掃帚－掃地的動作, § Snalu so manu ka ssik so? Tayal knmalu ka
# snsikan na! 「你的掃帚是用什麼材料做的？它掃得真好！」 sika is listed at 1 and glossed
# nowhere, and siku is the other reading the analyser offers. The gloss is in the corpus
# instead of the table: smsik is listed at 18 and its sentences say 我在掃地 and 我掃好了,
# which is his 掃地的動作 character for character. snksikan 3 and sngksikan are the
# register's own sn-…-an of the same root — his exact slot with the k of the causative —
# and sksikay 讓…清理 sits behind them. What was swept, and where.
# dtduling (b197). TDOLING 指頭（手指與腳趾）, § Kana dtdoling o, tama ka mq'tol balae
# 「在所有手指當中，拇指最粗。」 This one the register settles by naming him: tluling is
# listed at 30 and glossed 腳趾（與tduling 同義） — the gloss itself says his spelling is
# the synonym, so the word is not a respelling of ours but a variant the wordlist prints.
# tduling is listed too, at 1, with no gloss of its own, which is the only reason the gate
# stopped. stduling 大手指 is the thumb, which is what his sentence is about, and
# pstluling 善用手指 and tmtluling 專修手指 stand round it. d- is the collective his card
# uses for a set of people or parts — kana dtdoling, all the fingers there are.
# mtru (b197). T'LO › Mt'lo 第三次（現在）, § Mt'lo sayang da; adi ko bi da! 「現在已經
# 是第三次了；我真的不能再接受了！」 The map had been restoring the vowel his elision mark
# says is absent and landing on `taru`, listed at 10 — and all 31 of that token's corpus
# sentences are Ta-ru, a syllable of the transliterated 大陸 in a history text. Not a
# Truku word at all, which makes the old value the batch 171 freeze exactly: a homograph
# holding a slot. Respelled to mtru in manual_map: tru 三；三個 is listed at 497 and is
# his 第三次 with the character shared outright, l→r is his commonest correspondence, and
# the register writes m- over this very numeral in mtrul 三十 at 108. Hand-ruled because
# mtru is the bare count and the wordlist prints only the decade.
# msthulang (b197). TXOULANG › Stxoulang 自負的－裝作首領、上司的樣子, § Xmut so
# mstxoulang ka iso 「你只不過是個自負的人（愛逞能）。」 thulang is listed at 4 and glossed
# nowhere, which is the block; the one gloss the root has anywhere is psthulang 自大, and
# it is his letters exactly with the other causative. Found by searching from the meaning
# rather than the letter: asked which modern words carry 驕傲|傲慢|自大|自負 and got twelve,
# eleven of them dahu, sparu and smpraw shapes, and this one. 自大 and 自負 are the same
# vice with a different second character — the nskkuyuh case, where 妻子 and 太太 were the
# same woman — and the shared 自 is the head of both compounds, not an incidental hit.
# dtanah (b197). XKE — his sentence-final particle card — § Mngongo ka dtanax tunuç!
# Nasi mk'la tunuç ka llisao troko dga … 「日本人心裡不安！若太魯閣的年輕人受了教育…」
# tanah is listed at 5 and glossed by no table, and the sentence gloss says 日本人, which
# agrees with nothing because it is not a translation of the word. The corpus has the
# phrase itself: 「Tanah tunux」 glossed 「紅頭」, red heads, which is what Truku calls the
# Japanese and what his dtanax tunuç is. So the word is 紅 and the ethnonym is the phrase,
# and d- is the collective this batch has now ruled three times — dtdoling all the
# fingers, dTome the household, dBiyang the family. The people with the red heads.
# empkmalux (b197). XEDAO › Txedao 出太陽－曬太陽, § Ya usa txedao da! Mpkmalox so kia!
# 「別再去曬太陽了！你會把自己弄病的！」 The map had l→r and produced empkmarux, whose root
# is listed at 0 with no gloss and no corpus sentence at all; the analyser then cut it to
# lux and reached nothing. Searched from the meaning — 生病|病痛|得病 returns fourteen
# forms, thirteen of them narux shapes and one that is not: mnalux 生病, listed at 4, with
# two corpus sentences that translate it 你已經病了一週了 and 生病的爸爸. That is his malox
# with the l standing, and batch 168 measured this letter — 1,151 of his l become r and
# 1,275 stay, a coin flip no rule can call, so the gloss calls it. Respelled in
# manual_map to empkmalux; pk- is the causative pknarux 使…生病 uses on the other sickness
# root, and his sentence is that causative exactly: the sun will make you ill.
# treura (b197). The largest single pale word left on the page, 13 occurrences, and it
# came off the census rather than off the blocker list — blockers.py ranks by sentence
# pairs, and this one is spent on headwords, sub-forms and crossrefs. LUULA › Tluula
# 公開地－眾所周知－在眾人目睹與知悉之下, with its own TLUULA card repeating the gloss and
# § Manu ka saan so ngangot? Ya bi tluula mksa da! The stem is the register's, and the
# alignment is exact: his Mtluula against mtreura 明顯, listed at 7 — mt-l-uu-l-a to
# mt-r-eu-r-a, both his l become r, his uu is their eu. Around it the same root is
# glossed four more times: mteura 公開的 3, pteura 很明顯的 19, steura 清楚的, pnteura 4,
# and his 公開 is the first of those character for character while his 眾所周知 is the
# rest of them. The t- form he writes is the one slot no wordlist prints, which is the
# only reason the gate never saw it.
# Batch 199. The lone pale slot on an otherwise-dark card. Batch 198 priced the
# pale by what the ANALYSER could say about each word and found the seam nearly
# spent; this batch asked a different question -- not "what is this word?" but
# "what is every other slot on its card?" -- and found 53 cards carrying 139 pale
# occurrences beside three or more dark ones. His card IS a paradigm, so the odd
# slot out is either a generator slip or a gap the family already answers.
#
# Seven map values came down, and six of them were tier-M hand entries. An M
# identity claim is a verdict reached at a particular time and may be overturned
# when the family turns up attested -- here the family was attested all along and
# was sitting on the same card:
#   kalip/qalip qrip -> qrib, kmalip qmrib, mkalip mqrib, pkalip pqrib.
#     His KALIP 剪 paradigm is °Kmalip, kalip, klibi, kliban, klibun, and the map
#     ALREADY rendered klibi/kliban/klibun as qribi/qriban/qribun, of which qribi
#     要剪下 and qribun 剪成 are attested. Only the bare form kept his final <p>.
#     Batch 197 refused qrip after searching qrip/qlip/klib/qalip and finding
#     "zero forms" -- a shape search, and the final stop is exactly what a French
#     ear devoices. Searching the GLOSS 剪 finds qribun at once. His l is their r
#     and his k their q, in his own paradigm, four slots deep.
#   pkl'xlax pkhlah -> pklhlah. Every other slot on L'XLAX is dark (lmhlah,
#     plhlah, splhlah, mtlhlah); the generator dropped the l on this one.
#   pdxleqan pdhliqan -> pdhriqan. Its own sibling pdxleqe is dark as pdhriqi:
#     l->r applied on every slot of D'XLEQ except this one.
#   snblayan snbrayan -> snblayan (identity, which blocks charRules and is meant
#     to): knsblayan on the same card is dark with the l standing.
#   mpsq'lol -> empsqrul, matching bsqlol -> bsqrul on BSQLOL 在鍋裡燒焦的食物
#     and the attested sqrul 燒焦.
#   pqatai -> pkatay. QATAI 破損 is dark as katay, mkatay, tkatay; only his
#     Pqatai kept the q the generator had already ruled against three times.
#
# The rest are gaps the family answers. Each is the only pale slot on its card,
# and the count of dark slots beside it is the argument:
#   19D LUTUT bntudan (ltudan, pltudan dark) | 17D XDO hmdu, hduun (qhduun dark)
#   16D L'XLAX | 13D BAXANG kmkbahang 想要聽 (embahang 167, qbahang 97 dark)
#   13D D'XLEQ | 11D TAQE qtaqi < his Ktaqe (sktaqi, ptaqi, tqian dark; the k->q
#   this generator applies on Kxdo->qhdu) | 10D DAXO dhuan, kntdhuan (tdhuan
#   dark) | 8D SB'LÖS knsblsan (psblsan dark) | 7D SLOXAO knsrhagan (psrhagan
#   dark) | 6D SBU" psbui, psbuan, psbuun -- the intersection of two dark sets,
#   psbu and sbui/sbuan/sbuun | 5D L'BAI sklbai | 4D MAXAL mnnaxal, pnnaxal
#   (mnaxal, mknaxal dark) | 4D NGONGO knngnguan 膽怯 (mngungu 害怕 dark) |
#   4D LIBAQ rbaqi, rbaqan, rnbaqan (ribaq, rmibaq, mribaq dark) | 3D ISIL
#   mksiisil | 3D L'XAN emplxan (mlxan dark; Mpl'- -> empl- on every card) |
#   IYAX yiyahun < his Yiaxon, beside a dark yahun | LILU lilug, emplilug |
#   MALU empnalu < his Mp'nalu 將會變好 (mnalu, gnalu, knalu dark) | BSQLOL
#   bsqrul, the attested sqrul 燒焦 and his own § "免得燒焦" | psdmati, qqurug,
#   the last two siblings of batch 198's rulings.
#
# Refused. yianu, his Yiano 為你們 on YAMO: the card's dark members are all
# yamu/namu-shaped and his is neither, so o->u alone would be the whole argument.
# nilit, twice in a LUTUT example (羊奶讓我恢復了元氣) with no analysis at all.
# thrdu < his tx'ldo, one occurrence and no slot to hang it on.
#
# And naru stayed pale for the third time, but the pin is now better than it was.
# Asked what nalu actually IS, the book answers twice: NALU 代替、頂替 is one
# headword, and the seven other tokens are the 好 word -- his MALU card carries
# Gnalu 關愛, Mnalu 和睦相處, Knalu 要好起來, Mpanalu 將會變好, a whole paradigm
# built on the n-form, and gnalu is the modern gnealu 憐憫 with his schwa unwritten.
# The eight tokens sit on six page ranges from 150 to 357 while malu was read
# correctly 166 times, so this is his morphology, not a slip of the transcription.
# One key cannot serve both, and seven of the eight would publish as "replace".
#
# SECOND PASS, and 99% cleared: 43,810 dark + 684 class of 44,943 spans, 99.0010%,
# and 5,208 of 5,435 example pairs fully dark (95.82%, from 95.07%). Fifty rulings
# and eleven map values, and the reason it went this far is that the gloss test was
# run on every one BEFORE it was written, not after. It killed a third of the queue:
#   tbiyan is 下來, and his whole TABE tbi- family was leaning on it -- eight
#     occurrences that looked like clean -un/-i gaps beside a dark -an slot. An
#     attested value can still be a wrong value, and it can hold up six others.
#   sapat 舖（舖床） against his 行為不檢; qrut 啃骨聲 against his LOT 梁; shik 吻
#     against his Sl'xeq 舔; mqraq 抓（seize）against his QLAQ 發癢, where the
#     register's 癢 is ghguh / kaguh and nothing qraq-shaped means it.
#   rangi 不遵守習俗（犯忌）on the LANGI card whose gloss is 剩下的. The register's
#     剩餘 is sngari / ngari / msngari. A card head that is dark for the wrong
#     reason licenses nothing standing beside it.
# and it CONFIRMED the ones that went in: pixan 用…壓住 for APIX, kayagan 不是睡
# 覺的時間 for KAYAO, ltadan 外出 for LATAT, pskan 咀嚼 for PSKAN, ranaq 火焰 for
# LANAQ, ramil 拖鞋 for LAMIL, hmadan 表堂姊妹 for XMADAN 姻親, siling 問 for
# SILING, empusal 二十 for his PUSAL 成雙－加倍, drut 用手揉起來 for DLUT 磨碎.
#   PAKOX is the case for deciding slot by slot: pakux is glossed 老鼠 -- a
# homophone -- but makux 翻動 on the same card meets his 翻轉 exactly, so the card's
# root is right and its six empty slots (pkuxi, pkuxun, empkpakux, pkpkuxi/an/un)
# are gaps, not proposals.
#   REDUPLICATION, again, and this time as a seam rather than a caveat. roots()
# still cannot see it, so the analyser reports no root for every CC- form; stripping
# the doubled onset by hand and asking whether the base is dark ON THE SAME CARD
# found rramil < ramil 拖鞋, rranaq < ranaq 火焰, hhmadan < hmadan, llabis < labis
# 蚊子, ppitay < pitay, qqiri < qiri 彎向. Nine forms, of which the gloss test
# refused two (ssapat, qqrut) -- the same test, applied to the same evidence.
#
# TWO GENERATOR FACTS, both learned by breaking something.
#   A manual entry whose value is the key plus a letter feeds back into the
# consonant-strip rule: psilin -> psiling made mpsiling -> empsilingg AND
# psiling -> psilingg, because the rule strips the final g, finds the manual value,
# and re-appends. The LOST check caught it (gained 10, LOST 1) and the fix is to pin
# both shapes in manual_map. Any X -> X+C entry should be assumed to do this.
#   loan_population.json is REGENERATED by build_modern_map.py, exactly as
# name_population.json is (batch 197). siba was hand-added to it and vanished on the
# next map build. HAND_LOANS now exists for the same reason HAND_NAMES does.
# Batch 198. Sixty-one at once, and the reason is not that the bar moved: it is that
# the pale list was read by BUCKET for the first time instead of word by word. Run the
# analyser over all 447 pale types and they fall in three heaps — 91 types whose root is
# attested AND glossed, 28 whose root is listed but glossed by nobody, and 328 that reach
# no root at all. The first two heaps are 144 occurrences and they are the only part of
# the page that a morphological argument can still reach; the third is 493 occurrences of
# honest hole. Everything below comes out of the first two, plus one seam the analyser
# cannot see at all.
#   THE SIBLING SEAM. Half of these were decided years-of-batches ago and nobody carried
# the verdict across the paradigm. `empraqat` (his Mplaqat) is already in this list, so
# his Plaqat is `praqat` by the same ruling; `knluusan` is here, so `knluus`; `pknluun`,
# so `pknluan`; `sdmatan`, so `psdmatan`; `pklilug`, so `plilug`; `kkrang` and `mkkrang`,
# so `tkkrang`; `ptkanun`, so `ptkanan`; `qmapah`, `haduri`, `pnrikit`, `empklutut`,
# `empngpung`, `mtudu`, `msilung`, `psnegulun` — each one licenses the slot beside it.
# A ruling that stops at the form the map happened to show is half a ruling.
#   But a sibling is only a sibling if it is the same card. `pngraq` is in this list and
# it is NOT evidence for his G'LAQ 拿取——奪取: it comes off NG'LAQ 愚蠢——白痴, a different
# entry that happens to share four letters. graq / gmraq / graqun stay pale. A label is
# not an argument, and neither is a neighbouring string.
#   THE REDUPLICATION SEAM. roots() has no reduplication rule, so every CC- and VV- form
# lands in the unreachable heap with a root of "". Strip the doubled onset by hand and
# the stem underneath is one of the most frequent words in the register: uuyas < uyas
# 唱歌 216 (his own tag prints it, OYES (OYAS？)), llihaw < lihaw 32 for his LIXAO
# 玻璃－鏡子, ssiisil < isil 另一邊 215 for his Ssiisil 來自四面八方, klkari < kari 1608
# for his Klkari 眾多話語（＝複數形）— his gloss says plural and reduplication is how
# Truku says plural. iisu < isu 你 508, kiima < ima 誰 525 (he analyses it himself:
# ki'ima = kii + ima). qqsahur < qsahur 內臟 33, where both his sentences translate
# kksaxol as 心 and the organ is the metaphor. Nineteen occurrences the census listed as
# hopeless.
#   THE MAP WAS WRONG IN FIVE PLACES, and pale was reporting it faithfully. `glani` is
# his GALU 憐憫 imperative and the register lists `gleani` 去關愛 outright — that one
# needed no ruling at all, only the right value. `sktaqe` had been given sq- for sk- when
# the root is `mtaqi` 睡 250 and his prefix is sk-. `tmt'lo` had a vowel restored onto
# taru, the transliterated 大陸 syllable batch 197 caught under `mt'lo`, and is `tmtru`
# 分成三份 off tru 三 497. `psn'gulan` and `psn'guli` had l→r applied to snegul 跟隨 46,
# whose l stands — and `psnegulun`, already ruled in this list, spells it that way.
#   The rest, one line each. msrahuq: his LAXOQ 除了 IS rahuq 除了這些還有 92, and the
# slot gloss 愛漏掉者 is what a man who leaves things out is called. empsibus < psibus
# 種甘蔗 off sibus 甘蔗 28. dkaran/dkari/dkarun: his DAQAL 禁止 is mdakar 禁止 9, exact.
# mqatar < qatar 兩腳張開 15 for his 跨步. msndngux < dngux 沈睡 for his 深沉.
# pqurug < qurug 球 182 for his QOLO 圓的－球. psqrinutan < qrinut 窮 54 for his QLINUT
# 貧窮的. spdawi < dawi 懶惰 20, exact. tuyuqi/tuyuqun < tuyuq 痰 4 for his 唾液－吐口水.
# tbowyak < bowyak 山豬 257 — he questions the etymology himself and the spelling does
# not depend on it. tslabang < labang 寬 3 for his 逾越界限者. psbiyuq/sbiyuq: the
# wordlist calls biyuq a personal name, the e-dictionary calls it 淚滴／果樹汁, and
# msbiyuq 流汁 settles it against his BIYOQ 汁液. pkrikit: rikit is 瘸／易跌倒 in the
# e-dictionary, his LIKIT 殘廢－小兒麻痺. pqapah: qapah is 黏／不穩定, his QAPAX 黏附.
# pkrci/pkrtun/pkrtan < krci, krtun, krtan 切 for his Q'LöT 鋸子. nsntug < sntug 說八卦
# for his SNTO 談論. mtnring/tnring < mring 汗水 19, his M'LING 汗 exactly. hadurun:
# hadur is 貪吃 in the wordlist and 獵首筵席 in the e-dictionary, and mhadur 舉行馘首宴
# is his XADOL 禮儀性的獻祭. gquwaq < quwaq 199. gmnaliq < gnaliq 取過首級 6, and his one
# sentence is a beheading. sttui: the paradigm sibling sttuan is listed outright.
# empathulang/sthulang < thulang, the pride root batch 197 ruled msthulang on.
# pkltudan: batch 197's pnkltudan, one slot over. khngun/knhngun < hng, and mhing 熄火 8
# is his XENG 熄滅. psqrasaw < qaras 喜樂 46, exact. knkrnaan < mrana 逐漸增多 103 for his
# LANA 增加. psilung < gsilung 海 420, and he writes the g himself: "SILONG (＝GSILONG).
# pkpngpung < pngpung 山崗 8 for his PNPONG 山頂. ddjilun < dmijil 提著 18 for his DIDIL
# 用手提. nngangah < ngangah for his NGANGAX 啞巴. ssiban < sibu. mglngu < lngu for his
# L'NGO 瞄準線. emppaya < paya/ppaya. pntudan < tuda 17 on his BTUDAN card.
#   Refused in the same pass and written to refused.txt: the TABE 犁 family (8 occurrences
# over five slots — the register's plough is sakur, which he NAMES as his own synonym on
# that card, and no t-b-i shape carries it), tbiran (4, re-priced; the batch-193 refusal
# stands), sapat (5), knluus's neighbour luus 成熟的人 notwithstanding, kdapan (2, 寡婦 is
# kmptuhan), slangan/mslangan/empslangan (3, 生鏽 is skringan), snpusal/snpsaran/snpsarun
# (5, pusal is not listed at all — the register's twenty is elsewhere), prjilun (2, 傾斜
# is the riqi root), ppitay, kmupan, empkpakux, emburung, kblungi.
#   And `naru` was re-priced and LEFT PALE, which is the whole method in one word. Eight
# occurrences, the largest single lever on the board, and the shape is defensible: `nruan`
# 代替者 is listed and it is his NALU 代替 by syncope. But batch 114 already weighed this
# and chose pale deliberately — seven of those eight tokens sit in sentences whose Chinese
# says 好, because his nalu is a homograph of malu that the token-keyed map cannot split,
# and darkening them would queue seven spans to be harvested as the word for "good".
# A pin comes down when evidence overturns it, not when the metric wants it to.
#
# Batch 200 (last two lines: skarabi … pdmati) worked the PAIR ranking — pale words
# that alone block an example sentence — and not the occurrence ranking. Ten of the
# fourteen came from his own parenthetical, `X (Y)` / `X (vl. Y)` / `X (Y ?)`, where he
# has already testified two spellings are one word and the map sent them to two values
# of which exactly one was dark; those go in manual_map, not here. What is here:
#   snpsalan/snpsalun — NOT a new ruling but a GENERATOR BUG. The l→r char rule fired
# inside the root `pusal` (empusal 二十 is listed with its l, and spusalan was hand-ruled
# with its l in 199), so these two came out snpsaran/snpsarun while every sibling on the
# card kept the l. Identity-pinned in manual_map to block charRules(); ruled here so the
# gloss agreement carries. This is the same family the note above refused at 5 occurrences
# for want of a listed `pusal`; batch 199 overturned that on empusal, and this is its tail.
#   npghiyi — the same shape. xei→hiyi, mgxei→mghiyi 結果實, pgxei→pghiyi are all dark;
# one token slipped to `hii`. Sized the seam BEFORE fixing it: one token, not a class.
#   empaamalu/npaamalu < maamalu 變好, and empaa- is fully productive (empaadxgal 會變成塵土,
# empaababuy 變成豬, 12+ forms), with npaabuqa attested for the n-. His three sentences say
# 好看, 痊癒, 舒服些. skarabi < karabi/skarabi 昨晚. csgsutun < sgsut 摩擦. knsdraan < sdaran.
#   pdmati is the one worth remembering. The gloss table's ONLY row for `damat` reads
# 恢復原狀, which would have refused it outright. The family overrules the row: dmatan
# 用…配菜, dmatun 要用…做菜餚, dmaci 要配菜吃, dmamat 配菜, ddamat 要吃的菜餚 — and his DAMAT
# card is 菜餚——佐料. A single gloss row is not the register's answer; the family is.
HAND_RULED = """treura msthulang dtanah empkmalux
                smhngi snsikan dtduling mtru
                pnkltudan kmpspusu sshgan ndmpatas
                pnskngalan mnpgealuk nskkuyuh mrangah nrangah nsrijil pnsrijil mnspruq ppdsun tksaw gmquwaq snkrawah mnalu pnguwan embqru
                pnsmkan snkiya mskutu mritan knsbusan tnglaan
                pngraq ptudu pkngalan embbuway mtdahu ddngusun stgtgut kkrang mkkrang krhun knslaan empraqat mrbuq pnrikit empklutut knluusan pknluun penduk empngpung haduri qmapah tpssagan sdmatan psnegulun knsupu smteetu steetuun knsteetuan
                tmgila tngila kntglaan
                ptkanun mtkumax tmkumax mtudu sghuwayan slungan msilung ptbnagun ntlawa maabgu empaabgu msska pnsdahung drnai ggitan pnmaxan kmpstrngun empkslaan shnkan mnpunu nslbu empslbu nruq kmkmalu nrbu empsneanak snguli kpajiq knpajiq spkpajiq pnpnguan pspuhaw ssbusun sgulan psmkun snka stmaqun muli pneydang psnruun pklilug ciyusun ppskngalun
                msrahuq empsibus dkaran dkari dkarun mqatar msndngux pqurug psqrinutan
                ptkanan spdawi tuyuqi tuyuqun tbowyak tslabang psbiyuq sbiyuq pkrikit
                pqapah pkrci pkrtun pkrtan nsntug mtnring tnring hadurun gquwaq gmnaliq
                sttui empathulang sthulang pkltudan khngun knhngun psqrasaw knkrnaan
                psilung pkpngpung ddjilun nngangah ssiban mglngu emppaya pntudan
                uuyas llihaw ssiisil klkari iisu kiima qqsahur
                sktaqi tmtru psnegulan psneguli
                praqat knluus pknluan psdmatan plilug tkkrang
                qrib qmrib mqrib pqrib pklhlah pdhriqan snblayan empsqrul
                kmkbahang knngnguan bsqrul rbaqi rbaqan rnbaqan psbui
                psbuan psbuun hmdu hduun dhuan kntdhuan mnnaxal pnnaxal
                yiyahun bntudan qtaqi knsblsan lilug emplilug mksiisil
                psdmati qqurug empnalu sklbai knsrhagan emplxan pkatay
apix papix hlingan mhuling mqburung qbrungi pdrut prjilun prjili msrijil empalaqi kayagi kayagun kmkspahung ltadun mqudak pbuway pkmalu pskngalu qqiri rjingun slap smilap snlui sqaai bskanun btudun pkuxun pkuxi empkpakux pkpkuxi pkpkuxan pkpkuxun hhmadan rramil rranaq llabis ppitay
snpusal smpusal spusal spusalan spusali spusalun drci qluhan kmbuyu qdakan psiling
skarabi snpsalan snpsalun npghiyi empaamalu npaamalu
csgsutun knsdraan nay pdmati
""".split()

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
# `pdrut` is the third, and it is the pin from batch 171 coming due [batch 196].
# That batch respelled his DLUT family onto `drut` and handed `pdrut` BACK to
# pale — dark at rank 1 on a 黏 homograph before, and after the respelling no
# gloss agreed through `p-`. dom171.py pinned it pale with an instruction on the
# pin: if this ever goes dark, check that it did so on a gloss and not on another
# `id` freeze. It is dark now, and the check the pin asked for is what refuses
# it. Not a freeze — rule 2, agreeing on 去.
#   pdrut    his 使人碾磨;請人碾磨, to have something ground, against `drut`
#            用手揉起來 / 輾過去. Those two glosses share nothing. The character
#            the analyser found is the 去 of his EXAMPLE sentence,
#            我沒時間去請人磨小米 — I have no time to go and have millet ground —
#            against the 去 of 輾過去. A man who has no time *to go* and a
#            millstone that rolls *over* are not the same 去, and neither one is
#            about grinding. His own word gloss, the one that would settle it,
#            agrees with the root on nothing at all.
#
# Whether this is a rung or a hand list was measured, not assumed (share196.py).
# Of 1,068 code-2 values, 593 distinct characters carry the agreements and 223
# reach it only through a sentence-shaped string of his — but 72 of those agree
# on a RUN (燒焦, 呻吟, 上面, 先走), which no coincidence supplies, and of the 151
# single-character ones only NINE agree on a character thin enough to mean
# nothing: empsparu 大, kdagun 來, mkatan 來, pdrut 去, pngalun 來, psagan 來,
# spkmalu 好, tnklaun 到, tnqtaan 到. Nine is a list to read one at a time, not a
# rule to rewrite — the same finding batch 142 made about 大/小, and the same
# answer. The other eight are the queue; this one had a pin on it.
HAND_NOT_REGULAR = set("knslaan pdrut".split())

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
        # THE PARQUETS' MANDARIN SIDE — batch 183, build_parquet_gloss.py. The
        # same eight datasets build_parquet_attested.py counts tokens in, read
        # for their `translation`/`mandarin` column this time: 8,875 rows whose
        # Truku side is ONE word, 1,420 words, 2,315 glosses, 328 of the words
        # carrying no gloss in the wordlist at all.
        #
        # Phrases are refused at the builder and the reason belongs here too,
        # because this is where the temptation lands: `baga bubu` 母親的雙手
        # would gloss `baga` 手 and 母親 with equal confidence, and _agrees()
        # reads a shared character and cannot tell which half it matched. The
        # corpus has tens of thousands of phrase rows and they stay unread.
        self.pqg = json.load(io.open(os.path.join(D, "parquet_gloss.json"),
                                     encoding="utf-8"))
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
        rg.extend(self.pqg.get(root) or ())
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

    # ---- the word's own vowel, put back -------------------------------------
    def restored(self, v):
        """(candidate, root, prefix, suffix) or None. The word with ONE vowel
        put back before it is analysed.

        `awag()` restores a vowel too, but only the one the -aw/-ag- alternation
        predicts. This is the general case and it was found the same way: three
        rulings in batches 186-188 — `pnguwan` off `pungu` 繩結, `pnsmkan` off
        `smuk` 鐵釘, `tknayun` alongside them — were filed by the report under
        "gloss disagrees" when the gate had never reached the root at all.
        Truku drops a root's first vowel under affixation and `roots()` looks
        for the letters that are there.

        WHAT IT MAY NOT DO. It may not guess at synonymy: `_agrees` still has to
        find a shared character between his own word-level gloss and the
        restored root's, which is the guard `awag` states and the reason it
        refuses `knsrhagan` against `ruhaw`. Inserting letters and then reading
        meanings loosely is two liberties, and either one alone is enough.

        MEASURED BEFORE IT WAS WRITTEN. Over all 589 unverified map values it
        fires on 17, and it cannot subtract: every rung is an OR, so a word that
        is verified stays verified. Three of the 17 are one paradigm —
        `pqdrxan`, `pqdrxi`, `pqdrxun` onto `qdrux` 石牆 — which is the shape a
        real syncope rule leaves behind, and not the shape a coincidence does.

        The most specific root wins, by length then alphabetically, for batch
        165's reason: a greedy pass over an unordered set is a sample, not a
        rule."""
        if v in self.frozen or v in self.lex:
            return None
        his = self._his(v, slots_only=True)
        if not his:
            return None
        best = []
        for i in range(1, len(v)):
            for vw in "aeiou":
                c = v[:i] + vw + v[i:]
                for root, p, sf, _ in self.roots(c):
                    if self._gloss(root) and self._agrees(his, root):
                        best.append((-len(root), root, c, p, sf))
        if not best:
            return None
        _, root, c, p, sf = sorted(best)[0]
        return (c, root, p, sf)

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
