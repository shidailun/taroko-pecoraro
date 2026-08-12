
    # === batch 242 -- the informant's answer sheet. A native Truku speaker
    # answered 71 pale words on a printed sheet; 23 map values changed and ten
    # words entered `HAND_SPOKEN`. 81 blocked pairs -> 53. Every row below is one
    # of those rulings landing on a pin, and the pins are overwhelmingly written
    # REFUSALS -- which is the shape this batch has, because an informant is the
    # one source that can retire a refusal resting on "nothing attests it".
    #
    # The discriminator the batch runs on, argued in full in the batch log: an
    # answer is a RESPELLING only where it is shape-continuous with his token
    # under his own correspondences (`o->u`, `l->r`, `x->h`, `'`/`"` as schwa,
    # `c,` for `x`, final `-e` for `-i`, `q` for modern `k`). Otherwise it names
    # the MEANING and is a translation, not evidence about his letters. Four
    # answers landed on modern HOMOGRAPHS and were refused on that ground
    # (`rqraq` 砍倒, `basiq` 太魯閣石櫟, `rangi` 犯忌, `pgagu` 笛子 -- the last
    # being literally the freeze batch 219 reverted, so it doubles as the
    # batch's control).
    ('dom218.py',
     'FAIL mqlaq no longer renders anywhere on the page. It was refused '
     'because zero of the # register words glossing 癢 are q-initial or '
     'contain raq; the modern itch root is krak/ghguh and mqraq is 抓. Tier X '
     'to mkrak was refused too -- batch # ruled that a lexeme modern Truku '
     'replaced is not a settled class -- if the transcription or the map '
     'changed, the refusal needs re-arguing, not deleting.'):
        ('ruled', ('mqlaq', 'mrkrak'),
         'batch 242 ruled it off the informant sheet: he answered `rkrak` for '
         '`qlaq` -- 生芋…引起的搔癢, his 搔癢 verbatim -- and `srkrak` for `sqlaq`, '
         'two independent answers about one root, so the third answer `rqraq` '
         '砍倒 is a homograph landing and is overruled. All three of his QLAQ '
         'sentences are about itching. This is the evidence batch 218 said '
         'was missing when it paid 3 pairs to remove the `mqraq` freeze'),
    ('dom218.py',
     'FAIL mqlaq maps to mrkrak, not to itself. The identity pin is '
     'load-bearing: charRules(mqlaq) spells mqraq on its own, so deleting the '
     'entry restores the freeze rather than removing it.'):
        ('ruled', ('mqlaq', 'mrkrak'),
         'batch 242 replaced the identity pin with a value. The pin was '
         'load-bearing for exactly the reason it states -- charRules(mqlaq) '
         'spells `mqraq` unaided -- and `mrkrak` blocks it just as well while '
         'also being the word'),
    ('dom218.py',
     'FAIL qlaq no longer renders anywhere on the page. It was refused '
     'because same refusal as mqlaq: there is no q-shaped itch word to find '
     '-- if the transcription or the map changed, the refusal needs '
     're-arguing, not deleting.'):
        ('ruled', ('qlaq', 'rkrak'),
         'batch 242 ruled it off the informant sheet: he answered `rkrak` for '
         '`qlaq` -- 生芋…引起的搔癢, his 搔癢 verbatim -- and `srkrak` for `sqlaq`, '
         'two independent answers about one root, so the third answer `rqraq` '
         '砍倒 is a homograph landing and is overruled. All three of his QLAQ '
         'sentences are about itching. This is the evidence batch 218 said '
         'was missing when it paid 3 pairs to remove the `mqraq` freeze'),
    ('dom218.py',
     'FAIL qlaq maps to rkrak, not to itself. The identity pin is '
     'load-bearing: charRules(qlaq) spells qraq on its own, so deleting the '
     'entry restores the freeze rather than removing it.'):
        ('ruled', ('qlaq', 'rkrak'),
         'batch 242 replaced the identity pin with a value; charRules(qlaq) '
         'still spells `qraq` unaided, so the entry is still load-bearing'),
    ('dom221.py',
     'FAIL map mqlaq -> mrkrak. Batch # reverted the tier-B freeze onto mqraq '
     '抓 at a cost of # pairs -- his head is 發癢, the two share no character, '
     'and zero of the # register words glossing 癢 are q-shaped. The identity '
     'pin is what stops charRules spelling mqraq on its own.'):
        ('ruled', ('mqlaq', 'mrkrak'),
         'batch 242 ruled it off the informant sheet: he answered `rkrak` for '
         '`qlaq` -- 生芋…引起的搔癢, his 搔癢 verbatim -- and `srkrak` for `sqlaq`, '
         'two independent answers about one root, so the third answer `rqraq` '
         '砍倒 is a homograph landing and is overruled. All three of his QLAQ '
         'sentences are about itching. This is the evidence batch 218 said '
         'was missing when it paid 3 pairs to remove the `mqraq` freeze'),
    ('dom218.py',
     'FAIL only # row(s) blocked by mqlaq, batch # measured #. A FALL is the '
     'news: it means something darkened the word again.'):
        ('shape', ((0, None, None), 'mqlaq', 'mrkrak'),
         'batch 242 darkened it, so it blocks nothing. The log calls a FALL '
         'news and it is right to -- this is that news, and the ceiling is '
         'set at 0 so the word blocking a row again re-opens the question'),
    ('dom65.py',
     'BROWN mqlaq mqlaq missing on [QLAQ]'):
        ('map', 'mrkrak',
         'batch 242 ruled the itch card off the informant sheet'),
    ('dom65.py',
     'BROWN qlaq qlaq missing on [QLAQ]'):
        ('map', 'rkrak',
         'batch 242 ruled the itch card off the informant sheet'),
    ('dom65.py',
     'BROWN sqlaq sqlaq missing on [QLAQ]'):
        ('map', 'srkrak',
         'batch 242 ruled the itch card off the informant sheet'),
    ('dom217.py',
     'FAIL qloq no longer renders anywhere on the page. It was refused '
     'because the neighbours qloqon and qloqi are unglossed, so the card '
     'offers nothing to read the slot against -- if the transcription or the '
     'map changed, the refusal needs re-arguing, not deleting.'):
        ('ruled', ("q'loq", 'rkruk'),
         'batch 242 ruled it, and it is the weakest of the four and marked as '
         'such in the batch log: `rkruk` is listed but unglossed, and what '
         'carries it is the exact vowel-parallel to the `qlaq`/`rkrak` pair '
         "the gloss did confirm. The refusal's own reason -- the neighbours "
         'qloqon and qloqi are unglossed, so the card offers nothing to read '
         'the slot against -- is retired by a speaker, which is a source the '
         'card does not have'),
    ('dom57.py',
     "BROWN q'loq qloq missing on [Q'LOQ]"):
        ('map', 'rkruk',
         "batch 242 ruled his Q'LOQ 煤煙 slot to `rkruk`"),
    ('dom57.py',
     "BROWN q'loq qloq missing on [SLöS]"):
        ('map', 'rkruk',
         "batch 242 ruled his Q'LOQ 煤煙 slot to `rkruk`"),
    ('dom217.py',
     'FAIL dmbasyaq no longer renders anywhere on the page. It was refused '
     'because his BASYAQ 暴飲暴食; 貪吃 sits on hadur / msqnaniq / dmhiqur, all '
     'different roots -- if the transcription or the map changed, the refusal '
     'needs re-arguing, not deleting.'):
        ('ruled', ('dmbasyaq', 'dmbsiyak'),
         'batch 242 ruled the gluttony root to `bsiyak`, and the refusal is '
         'retired by the fourth answer rather than the first three: for '
         '`tibasyaq` he wrote `tbsiyak`, and `bsiyak` heads a 40-form family '
         'whose `sbsiyak` is 搶著吃, scrambling to eat, against his TIBASYAQ '
         '行為像貪吃鬼的人. `tbsiyakaw` is listed and spells this exact stem '
         'suffixed. The other three answers were `basiq` 太魯閣石櫟, a stone-oak '
         "tree -- a homograph landing of the `pg'go -> pgagu` shape"),
    ('dom217.py',
     'FAIL dmtbasyaq no longer renders anywhere on the page. It was refused '
     'because his BASYAQ 暴飲暴食; 貪吃 sits on hadur / msqnaniq / dmhiqur, all '
     'different roots -- if the transcription or the map changed, the refusal '
     'needs re-arguing, not deleting.'):
        ('ruled', ("dmt'basyaq", 'dmptbsiyak'),
         'batch 242 ruled the gluttony root to `bsiyak`, and the refusal is '
         'retired by the fourth answer rather than the first three: for '
         '`tibasyaq` he wrote `tbsiyak`, and `bsiyak` heads a 40-form family '
         'whose `sbsiyak` is 搶著吃, scrambling to eat, against his TIBASYAQ '
         '行為像貪吃鬼的人. `tbsiyakaw` is listed and spells this exact stem '
         'suffixed. The other three answers were `basiq` 太魯閣石櫟, a stone-oak '
         "tree -- a homograph landing of the `pg'go -> pgagu` shape"),
    ('dom217.py',
     'FAIL tbasyaq no longer renders anywhere on the page. It was refused '
     'because his BASYAQ 暴飲暴食; 貪吃 sits on hadur / msqnaniq / dmhiqur, all '
     'different roots -- if the transcription or the map changed, the refusal '
     'needs re-arguing, not deleting.'):
        ('ruled', ('tbasyaq', 'tbsiyak'),
         'batch 242 ruled the gluttony root to `bsiyak`, and the refusal is '
         'retired by the fourth answer rather than the first three: for '
         '`tibasyaq` he wrote `tbsiyak`, and `bsiyak` heads a 40-form family '
         'whose `sbsiyak` is 搶著吃, scrambling to eat, against his TIBASYAQ '
         '行為像貪吃鬼的人. `tbsiyakaw` is listed and spells this exact stem '
         'suffixed. The other three answers were `basiq` 太魯閣石櫟, a stone-oak '
         "tree -- a homograph landing of the `pg'go -> pgagu` shape"),
    ('dom217.py',
     'FAIL tibasyaq no longer renders anywhere on the page. It was refused '
     'because his BASYAQ 暴飲暴食; 貪吃 sits on hadur / msqnaniq / dmhiqur, all '
     'different roots -- if the transcription or the map changed, the refusal '
     'needs re-arguing, not deleting.'):
        ('ruled', ('tibasyaq', 'tbsiyak'),
         'batch 242 ruled the gluttony root to `bsiyak`, and the refusal is '
         'retired by the fourth answer rather than the first three: for '
         '`tibasyaq` he wrote `tbsiyak`, and `bsiyak` heads a 40-form family '
         'whose `sbsiyak` is 搶著吃, scrambling to eat, against his TIBASYAQ '
         '行為像貪吃鬼的人. `tbsiyakaw` is listed and spells this exact stem '
         'suffixed. The other three answers were `basiq` 太魯閣石櫟, a stone-oak '
         "tree -- a homograph landing of the `pg'go -> pgagu` shape"),
    ('dom144.py',
     'PIN tbasyaq: want 1 pale'):
        ('absent', '',
         'batch 242 ruled `tbasyaq -> tbsiyak`; the old value is nowhere on '
         'the page'),
    ('dom57.py',
     'BROWN tibasyaq tibasyaq missing on [BASYAQ]'):
        ('map', 'tbsiyak',
         'batch 242 ruled the gluttony root to `bsiyak`'),
    ('dom57.py',
     'BROWN tibasyaq tibasyaq missing on [TIBASYAQ]'):
        ('map', 'tbsiyak',
         'batch 242 ruled the gluttony root to `bsiyak`'),
    ('dom57.py',
     'BROWN tbasyaq tbasyaq missing on [BASYAQ]'):
        ('map', 'tbsiyak',
         'batch 242 ruled the gluttony root to `bsiyak`'),
    ('dom58.py',
     "BROWN dmt'basyaq dmtbasyaq missing on [SAPAT]"):
        ('map', 'dmptbsiyak',
         'batch 242 ruled the gluttony root to `bsiyak`'),
    ('dom58.py',
     'BROWN dmbasyaq dmbasyaq missing on [SAPAT]'):
        ('map', 'dmbsiyak',
         'batch 242 ruled the gluttony root to `bsiyak`'),
    ('dom59.py',
     'BROWN dmbasyaq dmbasyaq missing on [SAPAT]'):
        ('map', 'dmbsiyak',
         'batch 242 ruled the gluttony root to `bsiyak`'),
    ('dom59.py',
     "BROWN dmt'basyaq dmtbasyaq missing on [SAPAT]"):
        ('map', 'dmptbsiyak',
         'batch 242 ruled the gluttony root to `bsiyak`'),
    ('dom215.py',
     'FAIL mslangan is no longer pale. Batch # refused it: he never writes a '
     "gr cluster in # pages and uses gl/g'l for modern gr, so sgrangan 生銹 "
     'would have been sglangan in his hand. If evidence arrived, retire this '
     'pin in writing — do not delete the assertion.'):
        ('ruled', ('mslangan', 'skringan'),
         "batch 242 retires HALF of it, and batch 230's rule is why: check "
         'what a refusal SEARCHED. Every word of the `gr` cluster count '
         'stands -- he never writes `gr` in 398 pages and his correspondence '
         "for it is `gl`/`g'l` -- and it refuses `srangan -> sgrangan`, a "
         'different word with a different cluster. The informant wrote '
         '`skringan` 生鏽'),
    ('dom145.py',
     'PIN empslangan: want 1 pale'):
        ('absent', '',
         'batch 242 ruled `mslangan -> skringan` and `mpslangan -> '
         'empskringan`; the old values are nowhere on the page'),
    ('dom163.py',
     'PIN mslangan: want 1 pale'):
        ('absent', '',
         'batch 242 ruled `mslangan -> skringan` and `mpslangan -> '
         'empskringan`; the old values are nowhere on the page'),
    ('dom164.py',
     'PIN empslangan: want 1 pale'):
        ('absent', '',
         'batch 242 ruled `mslangan -> skringan` and `mpslangan -> '
         'empskringan`; the old values are nowhere on the page'),
    ('dom164.py',
     'PIN mslangan: want 1 pale'):
        ('absent', '',
         'batch 242 ruled `mslangan -> skringan` and `mpslangan -> '
         'empskringan`; the old values are nowhere on the page'),
    ('dom215.py',
     'FAIL rngiyan is no longer pale. Batch # refused it: no attested modern '
     'counterpart; the register carries 剩下來的東西 on nngari/nengari, which is '
     "his separate NGALI card's root. If evidence arrived, retire this pin in "
     'writing — do not delete the assertion.'):
        ('ruled', ('lngiyan', 'rngian'),
         'batch 242: batch 220 said in writing what would re-open these -- '
         '"if an -an form ever enters the register, that is exactly the '
         'news". It has not entered the register. It entered from a speaker, '
         'which is the other way news arrives, and it is the same speaker '
         'whose answer for `pnslngiyan` (`psrngian`) supplies the shape. Both '
         'went into `HAND_SPOKEN`, so this row also re-asserts that the '
         'testimony is still there: drop it and the value leaves verified.js '
         'and the refusal is back'),
    ('dom220.py',
     'FAIL rngiyan no longer renders anywhere. It was refused because the '
     'register has no -an form of this root in the syncopated stem at all; '
     'its 剩下的東西 is nngari/nengari, off the FULL stem, which is his OTHER '
     "card's root -- if the map changed, the refusal needs re-arguing, not "
     'deleting.'):
        ('ruled', ('lngiyan', 'rngian'),
         'batch 242: batch 220 said in writing what would re-open these -- '
         '"if an -an form ever enters the register, that is exactly the '
         'news". It has not entered the register. It entered from a speaker, '
         'which is the other way news arrives, and it is the same speaker '
         'whose answer for `pnslngiyan` (`psrngian`) supplies the shape. Both '
         'went into `HAND_SPOKEN`, so this row also re-asserts that the '
         'testimony is still there: drop it and the value leaves verified.js '
         'and the refusal is back'),
    ('dom220.py',
     'FAIL pnsrngiyan no longer renders anywhere. It was refused because '
     "same: the register's 使留一些 is pnsngari, built on the full stem. "
     'Inventing pnsrngian to tidy the paradigm would be the metric deciding '
     'the spelling -- if the map changed, the refusal needs re-arguing, not '
     'deleting.'):
        ('ruled', ('pnslngiyan', 'pnsrngian'),
         'batch 242: batch 220 said in writing what would re-open these -- '
         '"if an -an form ever enters the register, that is exactly the '
         'news". It has not entered the register. It entered from a speaker, '
         'which is the other way news arrives, and it is the same speaker '
         'whose answer for `pnslngiyan` (`psrngian`) supplies the shape. Both '
         'went into `HAND_SPOKEN`, so this row also re-asserts that the '
         'testimony is still there: drop it and the value leaves verified.js '
         'and the refusal is back'),
    ('dom57.py',
     'BROWN pnslngiyan pnsrngiyan missing on [SLANGI]'):
        ('map', 'pnsrngian',
         'batch 242 ruled the -an slot on testimony'),
    ('dom230.py',
     'FAIL HOLD snxelan -> snxelan got snhiran -- nothing in this batch '
     'reached that slot'):
        ('ruled', ('snxelan', 'snhiran'),
         'batch 242 reached the slot batch 230 left: he wrote `snhiran` AND '
         '`uhir` beside it, and the second word is what makes the answer '
         'usable -- it names the root and rules out the `hir` 氣喘 homograph '
         'the bare shape would otherwise reach'),
    ('dom230.py',
     'FAIL snxelan no longer renders pale; a refused word going dark is a '
     'ruling nobody wrote'):
        ('ruled', ('snxelan', 'snhiran'),
         'batch 242 wrote the ruling: `snxelan -> snhiran`, `HAND_SPOKEN`, '
         'completing the card batch 230 ruled two slots of'),
    ('dom57.py',
     'BROWN snxelan snxelan missing on [SNOXEL]'):
        ('map', 'snhiran',
         'batch 242 ruled the third slot of the jealousy root'),
    ('dom221.py',
     'FAIL smmul no longer renders anywhere. It was refused because his '
     "SA'MUL 抱在懷裡 is carried by kmeabuh, verbatim, off abuh; the nearest "
     'samul-shaped words are smulus 拉著 and smuling 汙辱 -- if the map changed, '
     'the refusal needs re-arguing, not deleting.'):
        ('ruled', ("sm'mul", 'seemur'),
         "batch 242 ruled it: he wrote `seemur` for `sm'mul` -- 像兩腿交叉擁抱, his "
         '抱在懷裡 -- and the `<n>` slot `sneemur` is spelled for this stem by '
         'the listed `msneemur` 為了和…共寢 and `mnsneemur`. Batch 227 had already '
         'repaired the premise of the second refusal (the card was NOT pale '
         'head included); this is the evidence that was missing then'),
    ('dom221.py',
     'FAIL snmul no longer renders anywhere. It was refused because same card '
     'as smmul, and the whole card is pale head included -- there is no dark '
     'sibling to reason from -- if the map changed, the refusal needs '
     're-arguing, not deleting.'):
        ('ruled', ("sn'mul", 'sneemur'),
         "batch 242 ruled it: he wrote `seemur` for `sm'mul` -- 像兩腿交叉擁抱, his "
         '抱在懷裡 -- and the `<n>` slot `sneemur` is spelled for this stem by '
         'the listed `msneemur` 為了和…共寢 and `mnsneemur`. Batch 227 had already '
         'repaired the premise of the second refusal (the card was NOT pale '
         'head included); this is the evidence that was missing then'),
    ('dom227.py',
     'FAIL CARD snmul renders nowhere; the map entry is not firing'):
        ('ruled', ("sn'mul", 'sneemur'),
         "batch 242 ruled it: he wrote `seemur` for `sm'mul` -- 像兩腿交叉擁抱, his "
         '抱在懷裡 -- and the `<n>` slot `sneemur` is spelled for this stem by '
         'the listed `msneemur` 為了和…共寢 and `mnsneemur`. Batch 227 had already '
         'repaired the premise of the second refusal (the card was NOT pale '
         'head included); this is the evidence that was missing then'),
    ('dom227.py',
     'FAIL REFUSED snmul now has # .truku occurrences, pinned at #'):
        ('shape', ((0, None), "sn'mul", 'sneemur'),
         'batch 242 respelled the token, so the refused string has left the '
         'page entirely. Ceiling 0: the string coming back is what wants a '
         'new row'),
    ('dom215.py',
     'FAIL ksudan is no longer pale. Batch # refused it: his card is (R. = ?) '
     'with no head gloss; the modern shuttle is gikus, a different root, and '
     'there is no shape candidate. If evidence arrived, retire this pin in '
     'writing — do not delete the assertion.'):
        ('ruled', ('ksudan', 'kusutan'),
         'batch 242: he wrote `kusut (kusut-an)`, naming the slot himself, '
         'against the listed `kusut` 線綜棒 on a card glossed 織布用的梭子. The '
         'refusal searched for a shuttle and found `gikus`, a different root, '
         'and said so correctly -- what it could not search is a speaker. +3 '
         'pairs, the largest single card in the batch'),
    ('dom216.py',
     'FAIL graqun no longer renders anywhere on the page. It was refused '
     'because graqil/grqilun are the 賤價 root; the word that fits the sentence '
     "is qrapun, which is his own separate K'LAP card -- if the transcription "
     'or the map changed, the refusal needs re-arguing, not deleting.'):
        ('ruled', ('glaqon', 'glkun'),
         'batch 242: `glkun` is the syncopated -un of the `geeluk` 搶奪 he '
         "wrote on the neighbouring row, and his G'LAQ sentence is 別讓雲豹抓走你的山羊 "
         "-- don't let the clouded leopard SNATCH your goat. The refusal is "
         'right that `graqil`/`grqilun` are the 賤價 root; the word was neither '
         'of them'),
    ('dom217.py',
     'FAIL graqun no longer renders anywhere on the page. It was refused '
     'because graqil/grqilun are the 賤價 root; the word that fits the sentence '
     "is qrapun, which is his own separate K'LAP card -- if the transcription "
     'or the map changed, the refusal needs re-arguing, not deleting.'):
        ('ruled', ('glaqon', 'glkun'),
         'batch 242 ruled it to `glkun`, the syncopated -un of his `geeluk` '
         '搶奪'),
    ('dom216.py',
     'FAIL shmqan no longer renders anywhere on the page. It was refused '
     'because his GMALYEQ card is headed 詞根不明; 監獄/監牢 return # and the sole 牢 '
     'hit hmkan is a verb off another root -- if the transcription or the map '
     'changed, the refusal needs re-arguing, not deleting.'):
        ('ruled', ('sxmqan', 'shmuk'),
         'batch 242: he wrote `shmuk` 關著 against his sentence 他們進了監獄. The '
         'refusal searched 監獄/監牢 and the register carries the sense on 關, '
         'which is what the speaker supplied'),
    ('dom217.py',
     'FAIL shmqan no longer renders anywhere on the page. It was refused '
     'because his GMALYEQ card is headed 詞根不明; 監獄/監牢 return # and the sole 牢 '
     'hit hmkan is a verb off another root -- if the transcription or the map '
     'changed, the refusal needs re-arguing, not deleting.'):
        ('ruled', ('sxmqan', 'shmuk'),
         'batch 242 ruled it to `shmuk` 關著'),
    ('dom217.py',
     'FAIL hlakuh no longer renders anywhere on the page. It was refused '
     'because his card is 盾牌; hlak is 肉片 and hlaka 展翅, neither a shield -- if '
     'the transcription or the map changed, the refusal needs re-arguing, not '
     'deleting.'):
        ('ruled', ('xlakux', 'hlakuk'),
         'batch 242: `hlakuk` 用包狀物包起來 is listed and carries a 30-form '
         'covering family, against his 盾牌－保護之物. The refusal searched `hlak` '
         '肉片 and `hlaka` 展翅 and correctly found neither a shield; it did not '
         'reach the covering sense'),
    ('dom217.py',
     'FAIL qlap no longer renders anywhere on the page. It was refused '
     'because his card is 品嚐－親吻; the only qlap- gloss is qlapan 不能生育的女人 -- if '
     'the transcription or the map changed, the refusal needs re-arguing, not '
     'deleting.'):
        ('ruled', ('qlap', 'qrak'),
         "batch 242: `qrak` 抓 is one edit from the char rules' own `qrap`, in "
         'a sentence glossed 抓住他. The refusal is right that `qlapan` 不能生育的女人 '
         'is the only qlap- gloss -- and that is a fact about the LETTER, '
         'which is what a respelling changes'),
    ('dom231.py',
     'FAIL urang no longer renders pale; a refused word going dark is a '
     'ruling nobody wrote'):
        ('ruled', ('ulang', 'ulan'),
         'batch 242: `ulan` 久病纏身（被病纏身）against his ULANG 反覆發生的－週期性的－慣常的 and '
         "his own sentence about a chronic disease. Batch 230's rule about "
         "what a refusal SEARCHED, applied to batch 230's own refusal: it "
         'searched 週期, 慣常 and 反覆 and never searched 久病 or 疾'),
    ('dom138.py',
     'KEEP urang: want 2 pale'):
        ('absent', '',
         'batch 242 ruled `ulang -> ulan`; `urang` was the char-rule value '
         'and is nowhere on the page now'),
    ('dom144.py',
     'PIN qlap: want 1 pale'):
        ('absent', '',
         'batch 242 ruled `qlap -> qrak`; the old value is nowhere on the '
         'page'),
    ('dom217.py',
     'FAIL rikut renders # time(s) and NONE is pale. It was refused because '
     'his LIKUT 藉口－詭計; 詭計 sits on rnqdug and 欺騙 on qdug, a different root'):
        ('ruled', ('likut', 'rikut'),
         'batch 242, and the weakest entry in it, kept and labelled: he wrote '
         '`rikut`, 口語才部份有，大都用 rabih, qrbling -- "colloquially it partly '
         'exists". Partly exists is still exists, and it is asserted about '
         'the BARE root only, so the four derived slots got nothing and stay '
         'pale. The map never moved: `likut -> rikut` is unchanged and what '
         "darkened is the attestation. That is exactly what this row's second "
         'leg checks -- drop `rikut` from `HAND_SPOKEN` and it leaves '
         'verified.js and the refusal is back'),
    ('dom217.py',
     'FAIL sapi renders # time(s) and NONE is pale. It was refused because '
     'his SAPE is 小鋤頭; the sister sapaw is 舖（舖床、舖葉等）, and the modern word for '
     'a small hoe is parih (# spk) -- a different root, so there is no '
     'respelling of his to find'):
        ('ruled', ('sape', 'sapi'),
         'batch 242 retires ONE leg of a three-leg refusal and leaves the '
         'other two standing. The three-hoe system (`parih`, `bkaruh`) and '
         'the absence of any `sap-` hoe in the register are both still true '
         'and neither is retired. What the refusal ALSO said is that nothing '
         'attests the word at all, and his answer is 是否為借詞，有在用 -- "loanword '
         'or not, it IS in use", the one claim no document could make. The '
         'map value is unchanged; the word went from unattested to attested '
         'by a person'),
    ('dom231.py',
     'FAIL sruweq no longer renders GREEN. Green means no map entry fired, '
     'and the refusal was that supplying one is itself a spelling claim '
     '(batch #)'):
        ('ruled', ('sloweq', 'sruwaq'),
         'batch 242 ruled `sloweq -> sruwaq`. Batch 231 closed the class of '
         '11 headwords he could not gloss himself on the ground that the '
         'gloss test needs a gloss on HIS side too, and that limit is real -- '
         'four of the eleven are on this sheet and exactly ONE is ruled. It '
         'is ruled by SHAPE, never by the informant supplying a meaning: '
         'charRules already prints `sruweq` and `sruwaq` is one vowel from '
         'it, so the answer is shape-continuous and needs no gloss on either '
         'side. The other three were refused'),
    ('dom231.py',
     'FAIL `sruweq` sole-blocks # pairs, was # -- the limit was priced at '
     'that number'):
        ('shape', ((0, None), 'sloweq', 'sruwaq'),
         'batch 242 ruled it, so it blocks nothing. Ceiling 0 -- the pair '
         'coming back is the news'),
    ('dom216.py',
     "FAIL green moved to # spans, batch # measured # (['Mngusyeh|SIRAS "
     "(NGUSYEX)']). Green means no map entry fired; a rise is a generator "
     'regression, a fall wants a ledger row.'):
        ('shape', ((1, None, None), 'sloweq', 'sruwaq'),
         'batch 242: `sloweq` had no map entry at all, so it rendered GREEN, '
         'and ruling it gave it one. That is the whole of the green fall, 2 '
         '-> 1, and dom231 above proves it independently by failing on '
         '`sruweq` specifically. The ceiling is set at the new measurement, '
         'so a RISE is still the generator regression these logs are watching '
         'for'),
    ('dom217.py',
     "FAIL green moved to # spans, batch # measured # (['Mngusyeh|SIRAS "
     "(NGUSYEX)']). Green means no map entry fired; a rise is a generator "
     'regression, a fall wants a ledger row.'):
        ('shape', ((1, None, None), 'sloweq', 'sruwaq'),
         'batch 242: `sloweq` had no map entry at all, so it rendered GREEN, '
         'and ruling it gave it one. That is the whole of the green fall, 2 '
         '-> 1, and dom231 above proves it independently by failing on '
         '`sruweq` specifically. The ceiling is set at the new measurement, '
         'so a RISE is still the generator regression these logs are watching '
         'for'),
    ('dom218.py',
     "FAIL green moved to # spans, batch # measured # (['Mngusyeh|SIRAS "
     "(NGUSYEX)']). Green means no map entry fired; a rise is a generator "
     'regression, a fall wants a ledger row.'):
        ('shape', ((1, None, None), 'sloweq', 'sruwaq'),
         'batch 242: `sloweq` had no map entry at all, so it rendered GREEN, '
         'and ruling it gave it one. That is the whole of the green fall, 2 '
         '-> 1, and dom231 above proves it independently by failing on '
         '`sruweq` specifically. The ceiling is set at the new measurement, '
         'so a RISE is still the generator regression these logs are watching '
         'for'),
    ('dom219.py',
     "FAIL green moved to # spans, batch # measured # (['Mngusyeh|SIRAS "
     "(NGUSYEX)']). Green means no map entry fired; a rise is a generator "
     'regression, a fall wants a ledger row.'):
        ('shape', ((1, None, None), 'sloweq', 'sruwaq'),
         'batch 242: `sloweq` had no map entry at all, so it rendered GREEN, '
         'and ruling it gave it one. That is the whole of the green fall, 2 '
         '-> 1, and dom231 above proves it independently by failing on '
         '`sruweq` specifically. The ceiling is set at the new measurement, '
         'so a RISE is still the generator regression these logs are watching '
         'for'),
    ('dom220.py',
     "FAIL green moved to # spans, batch # measured # (['Mngusyeh|SIRAS "
     "(NGUSYEX)']). Green means no map entry fired; a rise is a generator "
     'regression, a fall wants a ledger row.'):
        ('shape', ((1, None, None), 'sloweq', 'sruwaq'),
         'batch 242: `sloweq` had no map entry at all, so it rendered GREEN, '
         'and ruling it gave it one. That is the whole of the green fall, 2 '
         '-> 1, and dom231 above proves it independently by failing on '
         '`sruweq` specifically. The ceiling is set at the new measurement, '
         'so a RISE is still the generator regression these logs are watching '
         'for'),
    ('dom221.py',
     "FAIL green moved to # spans, batch # measured # (['Mngusyeh|SIRAS "
     "(NGUSYEX)']). Green means no map entry fired; a rise is a generator "
     'regression, a fall wants a ledger row.'):
        ('shape', ((1, None, None), 'sloweq', 'sruwaq'),
         'batch 242: `sloweq` had no map entry at all, so it rendered GREEN, '
         'and ruling it gave it one. That is the whole of the green fall, 2 '
         '-> 1, and dom231 above proves it independently by failing on '
         '`sruweq` specifically. The ceiling is set at the new measurement, '
         'so a RISE is still the generator regression these logs are watching '
         'for'),
    ('dom222.py',
     "FAIL green spans: #, expected # ['Mngusyeh|SIRAS (NGUSYEX)']"):
        ('shape', ((1, None), 'sloweq', 'sruwaq'),
         'batch 242: `sloweq` had no map entry at all, so it rendered GREEN, '
         'and ruling it gave it one. That is the whole of the green fall, 2 '
         '-> 1, and dom231 above proves it independently by failing on '
         '`sruweq` specifically. The ceiling is set at the new measurement, '
         'so a RISE is still the generator regression these logs are watching '
         'for'),
    ('dom233.py',
     'FAIL the tag census is (#, #, #), pinned (#, #, #)'):
        ('shape', ((None, 14, 5, None, None, None), "q'loq", 'rkruk'),
         "batch 242 darkened ONE tag span: his LQLOQ tag reads (R. = Q'LOQ = "
         "suie ?) and `q'loq -> rkruk` paints the variant brown. 321/15/5 -> "
         '322/14/5, total held at 341. Only the pale and green halves carry '
         'ceilings -- a DARK rise is the project working, and putting a '
         'ceiling on it would make the row bookkeeping (batch 241)'),
    ('dom233.py',
     "FAIL the non-dark tag rows split {'root': #, '?': #, 'variant': #} by "
     "shape, pinned {'root': #, 'variant': #, '?': #}"):
        ('shape', ((14, 2, 2, None, None, None), "q'loq", 'rkruk'),
         'the same one span, seen by shape: root 15 -> 14, `?` and `variant` '
         'unmoved. Batch 233 closed this class -- every non-dark tag row is a '
         'settled class or a written refusal -- and a row LEAVING it does not '
         're-open it'),
    ('dom235.py',
     'FAIL a two-type cluster this batch pinned has left the book '
     '(tbasyaq+tibasyaq; dmtbasyaq+dmtsapat; snuk+thiy): batch # confirmed '
     'all four as refusals, so one healing is news'):
        ('shape', ((None,), 'tibasyaq', 'tbsiyak'),
         'batch 242 cleared it: `tibasyaq -> tbsiyak` and `tbasyaq -> '
         "tbsiyak` took both blockers of one two-type row, and `dmt'basyaq -> "
         'dmptbsiyak` took one of another. The list this key names is the '
         'batch-241 row plus the two this batch cleared, so the head re-keys '
         'whenever another one goes -- which is the assertion working. The '
         'only number in the line is the batch it cites, which is source code '
         'and not a measurement'),
    ('dom235.py',
     'FAIL only # of # sole blockers are rare, where this batch measured #. '
     'Rarity was pinned as a property of the whole seam; if it has become '
     "discriminating, batch #'s test can rank the pale after all."):
        ('shape', ((37, 44, None, None), 'tibasyaq', 'tbsiyak'),
         'batch 242 took 23 types out of the sole-blocker list, so both '
         'halves of the fraction fell: 55 of 67 -> 37 of 44. The PROPORTION '
         'is what batch 235 pinned and it is unmoved (82% -> 84%), so the '
         'finding stands -- rarity still does not discriminate. Ceilings on '
         'both counts, because a blocker coming back is the news'),
    ('dom236.py',
     "FAIL the two-type seam moved: # rows, [('krikut', 'nrikut')]. Batch # "
     'confirmed all four refusals; a NEW row of this shape is a pair the '
     'sole-blocker ranking cannot see.'):
        ('shape', ((1, None), 'tibasyaq', 'tbsiyak'),
         'batch 242 cleared it: `tibasyaq -> tbsiyak` and `tbasyaq -> '
         "tbsiyak` took both blockers of one two-type row, and `dmt'basyaq -> "
         'dmptbsiyak` took one of another, leaving one row, `krikut+nrikut` '
         '-- and `rikut` is in this batch too, as the deliberately weak '
         'HAND_SPOKEN entry that buys the BARE root and none of the four '
         'derived slots. Ceiling 1: a NEW row of this shape is still a pair '
         'the sole-blocker ranking cannot see'),
    ('dom241.py',
     'FAIL VERIFIED keys #, pinned #'):
        ('grew', ((6350, None), 'tibasyaq', 'tbsiyak'),
         'batch 242 added 23 verified values, 6327 -> 6350. `grew`, not '
         '`shape`: a verified key DISAPPEARING is the shape a ruling being '
         'silently lost would take. dom241.py prints this failure twice per '
         'run (its own pre-existing double-`extend` bug), and one row '
         'adjudicates both copies'),
    ('dom237.py',
     'FAIL the sweep no longer reaches shmqan; it is the positive control on '
     'the instrument, and losing it means the sweep is blind, not that the '
     'record is clean'):
        ('ruled', ('sxmqan', 'shmuk'),
         'batch 242 ruled `sxmqan -> shmuk`, and the log is right that this '
         'leaves the sweep without its positive control -- the control was a '
         'PALE value, and the sweep iterates over pale values, so darkening '
         'it is exactly what removes it. That is a real cost and it is '
         "recorded rather than excused: batch 237's instrument needs a new "
         'control before it is trusted again, and this row re-asserts that '
         'the ruling which took the old one is still standing in both tables'),
