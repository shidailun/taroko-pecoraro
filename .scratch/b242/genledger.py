# -*- coding: utf-8 -*-
"""Emit the batch-242 LEDGER block from the exact heads sig() computed.

Keys are never hand-typed (batch 241): they are read back out of keys.txt, so a
row that matches nothing is impossible by construction.
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(
    __file__))))
sys.path.insert(0, os.path.join(ROOT, "tools", "orthography"))
import suite as S                                                # noqa: E402

txt = io.open(os.path.join(ROOT, ".scratch", "b242", "keys.txt"),
              encoding="utf-8").read().splitlines()
cur, recs, i = None, [], 0
while i < len(txt):
    l = txt[i]
    if l.startswith("--- "):
        cur = l[4:].split()[0]
    elif l.startswith("HEAD "):
        recs.append((cur, eval(l[5:])))
    i += 1
need = [r for r in recs if r not in S.LEDGER]
seen = set()
need = [r for r in need if not (r in seen or seen.add(r))]

BANNER = """
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
"""

SEC = {}


def rule(f, mark, kind, arg, why, sec=None):
    SEC.setdefault(sec, []).append((f, mark, kind, arg, why))


# --- the itch card, QLAQ. Two answers out of three about one root outvote the
# third (batch 203's independence rule, arriving as testimony).
ITCH = ('batch 242 ruled it off the informant sheet: he answered `rkrak` for '
        '`qlaq` -- 生芋…引起的搔癢, his 搔癢 verbatim -- and `srkrak` for '
        '`sqlaq`, two independent answers about one root, so the third answer '
        '`rqraq` 砍倒 is a homograph landing and is overruled. All three of his '
        'QLAQ sentences are about itching. This is the evidence batch 218 said '
        'was missing when it paid 3 pairs to remove the `mqraq` freeze')
for f in ('dom218.py',):
    rule(f, 'FAIL mqlaq no longer renders', 'ruled', ('mqlaq', 'mrkrak'), ITCH,
         'itch')
    rule(f, 'FAIL mqlaq maps to mrkrak', 'ruled', ('mqlaq', 'mrkrak'),
         'batch 242 replaced the identity pin with a value. The pin was load-'
         'bearing for exactly the reason it states -- charRules(mqlaq) spells '
         '`mqraq` unaided -- and `mrkrak` blocks it just as well while also '
         'being the word', 'itch')
    rule(f, 'FAIL qlaq no longer renders', 'ruled', ('qlaq', 'rkrak'), ITCH,
         'itch')
    rule(f, 'FAIL qlaq maps to rkrak', 'ruled', ('qlaq', 'rkrak'),
         'batch 242 replaced the identity pin with a value; charRules(qlaq) '
         'still spells `qraq` unaided, so the entry is still load-bearing',
         'itch')
rule('dom221.py', 'FAIL map mqlaq -> mrkrak', 'ruled', ('mqlaq', 'mrkrak'),
     ITCH, 'itch')
rule('dom218.py', 'FAIL only # row(s) blocked by mqlaq', 'shape',
     ((0, None, None), 'mqlaq', 'mrkrak'),
     "batch 242 darkened it, so it blocks nothing. The log calls a FALL news "
     "and it is right to -- this is that news, and the ceiling is set at 0 so "
     "the word blocking a row again re-opens the question", 'itch')
for card in ('mqlaq mqlaq', 'qlaq qlaq', 'sqlaq sqlaq'):
    tok = card.split()[0]
    rule('dom65.py', 'BROWN %s missing on [QLAQ]' % card, 'map',
         {'mqlaq': 'mrkrak', 'qlaq': 'rkrak', 'sqlaq': 'srkrak'}[tok],
         'batch 242 ruled the itch card off the informant sheet', 'itch')
rule('dom217.py', 'FAIL qloq no longer renders', 'ruled', ("q'loq", 'rkruk'),
     "batch 242 ruled it, and it is the weakest of the four and marked as such "
     "in the batch log: `rkruk` is listed but unglossed, and what carries it is "
     "the exact vowel-parallel to the `qlaq`/`rkrak` pair the gloss did "
     "confirm. The refusal's own reason -- the neighbours qloqon and qloqi are "
     "unglossed, so the card offers nothing to read the slot against -- is "
     "retired by a speaker, which is a source the card does not have", 'itch')
for c in ("[Q'LOQ]", '[SLöS]'):
    rule('dom57.py', "BROWN q'loq qloq missing on %s" % c, 'map', 'rkruk',
         'batch 242 ruled his Q\'LOQ 煤煙 slot to `rkruk`', 'itch')

# --- the gluttony card. Three of four answers were the homograph `basiq`.
GLUT = ('batch 242 ruled the gluttony root to `bsiyak`, and the refusal is '
        'retired by the fourth answer rather than the first three: for '
        '`tibasyaq` he wrote `tbsiyak`, and `bsiyak` heads a 40-form family '
        'whose `sbsiyak` is 搶著吃, scrambling to eat, against his TIBASYAQ '
        '行為像貪吃鬼的人. `tbsiyakaw` is listed and spells this exact stem '
        'suffixed. The other three answers were `basiq` 太魯閣石櫟, a stone-oak '
        'tree -- a homograph landing of the `pg\'go -> pgagu` shape')
for f, mark, tok, val in (
        ('dom217.py', 'FAIL dmbasyaq no longer renders', 'dmbasyaq',
         'dmbsiyak'),
        ('dom217.py', 'FAIL dmtbasyaq no longer renders', "dmt'basyaq",
         'dmptbsiyak'),
        ('dom217.py', 'FAIL tbasyaq no longer renders', 'tbasyaq', 'tbsiyak'),
        ('dom217.py', 'FAIL tibasyaq no longer renders', 'tibasyaq',
         'tbsiyak')):
    rule(f, mark, 'ruled', (tok, val), GLUT, 'glut')
rule('dom144.py', 'PIN tbasyaq: want 1 pale', 'absent', '',
     'batch 242 ruled `tbasyaq -> tbsiyak`; the old value is nowhere on the '
     'page', 'glut')
for f, mark, val in (
        ('dom57.py', 'BROWN tibasyaq tibasyaq missing on [BASYAQ]', 'tbsiyak'),
        ('dom57.py', 'BROWN tibasyaq tibasyaq missing on [TIBASYAQ]',
         'tbsiyak'),
        ('dom57.py', 'BROWN tbasyaq tbasyaq missing on [BASYAQ]', 'tbsiyak'),
        ('dom58.py', "BROWN dmt'basyaq dmtbasyaq missing on [SAPAT]",
         'dmptbsiyak'),
        ('dom58.py', 'BROWN dmbasyaq dmbasyaq missing on [SAPAT]', 'dmbsiyak'),
        ('dom59.py', 'BROWN dmbasyaq dmbasyaq missing on [SAPAT]', 'dmbsiyak'),
        ('dom59.py', "BROWN dmt'basyaq dmtbasyaq missing on [SAPAT]",
         'dmptbsiyak')):
    rule(f, mark, 'map', val, 'batch 242 ruled the gluttony root to `bsiyak`',
         'glut')

# --- SLANGAN. Batch 215's refusal is intact and was never about this word.
RUST = ('batch 242 retires HALF of it, and batch 230\'s rule is why: check '
        'what a refusal SEARCHED. Every word of the `gr` cluster count stands '
        '-- he never writes `gr` in 398 pages and his correspondence for it is '
        '`gl`/`g\'l` -- and it refuses `srangan -> sgrangan`, a different word '
        'with a different cluster. The informant wrote `skringan` 生鏽')
rule('dom215.py', 'FAIL mslangan is no longer pale', 'ruled',
     ('mslangan', 'skringan'), RUST, 'rust')
for f, mark, val in (('dom145.py', 'PIN empslangan: want 1 pale',
                      'empskringan'),
                     ('dom163.py', 'PIN mslangan: want 1 pale', 'skringan'),
                     ('dom164.py', 'PIN empslangan: want 1 pale',
                      'empskringan'),
                     ('dom164.py', 'PIN mslangan: want 1 pale', 'skringan')):
    rule(f, mark, 'absent', '',
         'batch 242 ruled `mslangan -> skringan` and `mpslangan -> '
         'empskringan`; the old values are nowhere on the page', 'rust')

# --- the two -an slots batch 220 refused, and named the news that re-opens them
NGARI = ('batch 242: batch 220 said in writing what would re-open these -- '
         '"if an -an form ever enters the register, that is exactly the news". '
         'It has not entered the register. It entered from a speaker, which is '
         'the other way news arrives, and it is the same speaker whose answer '
         'for `pnslngiyan` (`psrngian`) supplies the shape. Both went into '
         '`HAND_SPOKEN`, so this row also re-asserts that the testimony is '
         'still there: drop it and the value leaves verified.js and the '
         'refusal is back')
rule('dom215.py', 'FAIL rngiyan is no longer pale', 'ruled',
     ('lngiyan', 'rngian'), NGARI, 'ngari')
rule('dom220.py', 'FAIL rngiyan no longer renders', 'ruled',
     ('lngiyan', 'rngian'), NGARI, 'ngari')
rule('dom220.py', 'FAIL pnsrngiyan no longer renders', 'ruled',
     ('pnslngiyan', 'pnsrngian'), NGARI, 'ngari')
rule('dom57.py', 'BROWN pnslngiyan pnsrngiyan missing on [SLANGI]', 'map',
     'pnsrngian', 'batch 242 ruled the -an slot on testimony', 'ngari')

# --- the jealousy root's third slot
rule('dom230.py', 'FAIL HOLD snxelan -> snxelan', 'ruled',
     ('snxelan', 'snhiran'),
     'batch 242 reached the slot batch 230 left: he wrote `snhiran` AND `uhir` '
     'beside it, and the second word is what makes the answer usable -- it '
     'names the root and rules out the `hir` 氣喘 homograph the bare shape '
     'would otherwise reach', 'jeal')
rule('dom230.py', 'FAIL snxelan no longer renders pale', 'ruled',
     ('snxelan', 'snhiran'),
     'batch 242 wrote the ruling: `snxelan -> snhiran`, `HAND_SPOKEN`, '
     'completing the card batch 230 ruled two slots of', 'jeal')
rule('dom57.py', 'BROWN snxelan snxelan missing on [SNOXEL]', 'map', 'snhiran',
     'batch 242 ruled the third slot of the jealousy root', 'jeal')

# --- SA'MUL
MUL = ('batch 242 ruled it: he wrote `seemur` for `sm\'mul` -- 像兩腿交叉擁抱, '
       'his 抱在懷裡 -- and the `<n>` slot `sneemur` is spelled for this stem by '
       'the listed `msneemur` 為了和…共寢 and `mnsneemur`. Batch 227 had already '
       'repaired the premise of the second refusal (the card was NOT pale head '
       'included); this is the evidence that was missing then')
rule('dom221.py', 'FAIL smmul no longer renders', 'ruled',
     ("sm'mul", 'seemur'), MUL, 'mul')
rule('dom221.py', 'FAIL snmul no longer renders', 'ruled',
     ("sn'mul", 'sneemur'), MUL, 'mul')
rule('dom227.py', 'FAIL CARD snmul renders nowhere', 'ruled',
     ("sn'mul", 'sneemur'), MUL, 'mul')
rule('dom227.py', 'FAIL REFUSED snmul now has # .truku occurrences', 'shape',
     ((0, None), "sn'mul", 'sneemur'),
     'batch 242 respelled the token, so the refused string has left the page '
     'entirely. Ceiling 0: the string coming back is what wants a new row',
     'mul')

# --- the singles
for f, mark, tok, val, why in (
    ('dom215.py', 'FAIL ksudan is no longer pale', 'ksudan', 'kusutan',
     'batch 242: he wrote `kusut (kusut-an)`, naming the slot himself, against '
     'the listed `kusut` 線綜棒 on a card glossed 織布用的梭子. The refusal '
     'searched for a shuttle and found `gikus`, a different root, and said so '
     'correctly -- what it could not search is a speaker. +3 pairs, the largest '
     'single card in the batch'),
    ('dom216.py', 'FAIL graqun no longer renders', 'glaqon', 'glkun',
     'batch 242: `glkun` is the syncopated -un of the `geeluk` 搶奪 he wrote on '
     'the neighbouring row, and his G\'LAQ sentence is 別讓雲豹抓走你的山羊 -- '
     'don\'t let the clouded leopard SNATCH your goat. The refusal is right '
     'that `graqil`/`grqilun` are the 賤價 root; the word was neither of them'),
    ('dom217.py', 'FAIL graqun no longer renders', 'glaqon', 'glkun',
     'batch 242 ruled it to `glkun`, the syncopated -un of his `geeluk` 搶奪'),
    ('dom216.py', 'FAIL shmqan no longer renders', 'sxmqan', 'shmuk',
     'batch 242: he wrote `shmuk` 關著 against his sentence 他們進了監獄. The '
     'refusal searched 監獄/監牢 and the register carries the sense on 關, which '
     'is what the speaker supplied'),
    ('dom217.py', 'FAIL shmqan no longer renders', 'sxmqan', 'shmuk',
     'batch 242 ruled it to `shmuk` 關著'),
    ('dom217.py', 'FAIL hlakuh no longer renders', 'xlakux', 'hlakuk',
     'batch 242: `hlakuk` 用包狀物包起來 is listed and carries a 30-form covering '
     'family, against his 盾牌－保護之物. The refusal searched `hlak` 肉片 and '
     '`hlaka` 展翅 and correctly found neither a shield; it did not reach the '
     'covering sense'),
    ('dom217.py', 'FAIL qlap no longer renders', 'qlap', 'qrak',
     'batch 242: `qrak` 抓 is one edit from the char rules\' own `qrap`, in a '
     'sentence glossed 抓住他. The refusal is right that `qlapan` 不能生育的女人 '
     'is the only qlap- gloss -- and that is a fact about the LETTER, which is '
     'what a respelling changes'),
    ('dom231.py', 'FAIL urang no longer renders pale', 'ulang', 'ulan',
     'batch 242: `ulan` 久病纏身（被病纏身）against his ULANG 反覆發生的－週期性的'
     '－慣常的 and his own sentence about a chronic disease. Batch 230\'s rule '
     'about what a refusal SEARCHED, applied to batch 230\'s own refusal: it '
     'searched 週期, 慣常 and 反覆 and never searched 久病 or 疾'),
    ('dom138.py', 'KEEP urang: want 2 pale', None, None, None),
    ('dom144.py', 'PIN qlap: want 1 pale', None, None, None),
):
    if tok is None:
        continue
    rule(f, mark, 'ruled', (tok, val), why, 'singles')
rule('dom138.py', 'KEEP urang: want 2 pale', 'absent', '',
     'batch 242 ruled `ulang -> ulan`; `urang` was the char-rule value and is '
     'nowhere on the page now', 'singles')
rule('dom144.py', 'PIN qlap: want 1 pale', 'absent', '',
     'batch 242 ruled `qlap -> qrak`; the old value is nowhere on the page',
     'singles')

# --- the two HAND_SPOKEN-only rulings: the map did not move, the ATTESTATION
# did. `ruled` is still the right kind and its second leg is the whole point.
rule('dom217.py', 'FAIL rikut renders # time(s)', 'ruled', ('likut', 'rikut'),
     'batch 242, and the weakest entry in it, kept and labelled: he wrote '
     '`rikut`, 口語才部份有，大都用 rabih, qrbling -- "colloquially it partly '
     'exists". Partly exists is still exists, and it is asserted about the BARE '
     'root only, so the four derived slots got nothing and stay pale. The map '
     'never moved: `likut -> rikut` is unchanged and what darkened is the '
     'attestation. That is exactly what this row\'s second leg checks -- drop '
     '`rikut` from `HAND_SPOKEN` and it leaves verified.js and the refusal is '
     'back', 'spoken')
rule('dom217.py', 'FAIL sapi renders # time(s)', 'ruled', ('sape', 'sapi'),
     'batch 242 retires ONE leg of a three-leg refusal and leaves the other '
     'two standing. The three-hoe system (`parih`, `bkaruh`) and the absence of '
     'any `sap-` hoe in the register are both still true and neither is '
     'retired. What the refusal ALSO said is that nothing attests the word at '
     'all, and his answer is 是否為借詞，有在用 -- "loanword or not, it IS in '
     'use", the one claim no document could make. The map value is unchanged; '
     'the word went from unattested to attested by a person', 'spoken')

# --- SLOWEQ: the one unglossed headword that retires, and the green span
SRUW = ('batch 242 ruled `sloweq -> sruwaq`. Batch 231 closed the class of 11 '
        'headwords he could not gloss himself on the ground that the gloss '
        'test needs a gloss on HIS side too, and that limit is real -- four of '
        'the eleven are on this sheet and exactly ONE is ruled. It is ruled by '
        'SHAPE, never by the informant supplying a meaning: charRules already '
        'prints `sruweq` and `sruwaq` is one vowel from it, so the answer is '
        'shape-continuous and needs no gloss on either side. The other three '
        'were refused')
rule('dom231.py', 'FAIL sruweq no longer renders GREEN', 'ruled',
     ('sloweq', 'sruwaq'), SRUW, 'sruwaq')
rule('dom231.py', 'FAIL `sruweq` sole-blocks # pairs', 'shape',
     ((0, None), 'sloweq', 'sruwaq'),
     'batch 242 ruled it, so it blocks nothing. Ceiling 0 -- the pair coming '
     'back is the news', 'sruwaq')
GREEN = ('batch 242: `sloweq` had no map entry at all, so it rendered GREEN, '
         'and ruling it gave it one. That is the whole of the green fall, 2 -> '
         '1, and dom231 above proves it independently by failing on `sruweq` '
         'specifically. The ceiling is set at the new measurement, so a RISE is '
         'still the generator regression these logs are watching for')
for f in ('dom216.py', 'dom217.py', 'dom218.py', 'dom219.py', 'dom220.py',
          'dom221.py'):
    rule(f, 'FAIL green moved to # spans', 'shape',
         ((1, None, None), 'sloweq', 'sruwaq'), GREEN, 'green')
rule('dom222.py', 'FAIL green spans: #', 'shape', ((1, None), 'sloweq',
                                                   'sruwaq'), GREEN, 'green')

# --- the censuses that moved
rule('dom233.py', 'FAIL the tag census is', 'shape',
     ((None, 14, 5, None, None, None), "q'loq", 'rkruk'),
     'batch 242 darkened ONE tag span: his LQLOQ tag reads (R. = Q\'LOQ = suie '
     '?) and `q\'loq -> rkruk` paints the variant brown. 321/15/5 -> 322/14/5, '
     'total held at 341. Only the pale and green halves carry ceilings -- a '
     'DARK rise is the project working, and putting a ceiling on it would make '
     'the row bookkeeping (batch 241)')
rule('dom233.py', 'FAIL the non-dark tag rows split', 'shape',
     ((14, 2, 2, None, None, None), "q'loq", 'rkruk'),
     'the same one span, seen by shape: root 15 -> 14, `?` and `variant` '
     'unmoved. Batch 233 closed this class -- every non-dark tag row is a '
     'settled class or a written refusal -- and a row LEAVING it does not '
     're-open it')

# --- the loss-shape logs
SHAPE242 = ('batch 242 cleared it: `tibasyaq -> tbsiyak` and `tbasyaq -> '
            'tbsiyak` took both blockers of one two-type row, and `dmt\'basyaq '
            '-> dmptbsiyak` took one of another')
rule('dom235.py', 'FAIL a two-type cluster this batch pinned has left the book',
     'shape', ((None,), 'tibasyaq', 'tbsiyak'),
     SHAPE242 + '. The list this key names is the batch-241 row plus the two '
     'this batch cleared, so the head re-keys whenever another one goes -- '
     'which is the assertion working. The only number in the line is the batch '
     'it cites, which is source code and not a measurement')
rule('dom235.py', 'FAIL only # of # sole blockers are rare', 'shape',
     ((37, 44, None, None), 'tibasyaq', 'tbsiyak'),
     'batch 242 took 23 types out of the sole-blocker list, so both halves of '
     'the fraction fell: 55 of 67 -> 37 of 44. The PROPORTION is what batch 235 '
     'pinned and it is unmoved (82% -> 84%), so the finding stands -- rarity '
     'still does not discriminate. Ceilings on both counts, because a blocker '
     'coming back is the news')
rule('dom236.py', 'FAIL the two-type seam moved:', 'shape',
     ((1, None), 'tibasyaq', 'tbsiyak'),
     SHAPE242 + ', leaving one row, `krikut+nrikut` -- and `rikut` is in this '
     'batch too, as the deliberately weak HAND_SPOKEN entry that buys the BARE '
     'root and none of the four derived slots. Ceiling 1: a NEW row of this '
     'shape is still a pair the sole-blocker ranking cannot see')
rule('dom241.py', 'FAIL VERIFIED keys #, pinned #', 'grew',
     ((6350, None), 'tibasyaq', 'tbsiyak'),
     'batch 242 added 23 verified values, 6327 -> 6350. `grew`, not `shape`: a '
     'verified key DISAPPEARING is the shape a ruling being silently lost would '
     'take. dom241.py prints this failure twice per run (its own pre-existing '
     'double-`extend` bug), and one row adjudicates both copies')

# --- the positive control a ruling took away
rule('dom237.py', 'FAIL the sweep no longer reaches shmqan', 'ruled',
     ('sxmqan', 'shmuk'),
     'batch 242 ruled `sxmqan -> shmuk`, and the log is right that this leaves '
     'the sweep without its positive control -- the control was a PALE value, '
     'and the sweep iterates over pale values, so darkening it is exactly what '
     'removes it. That is a real cost and it is recorded rather than excused: '
     'batch 237\'s instrument needs a new control before it is trusted again, '
     'and this row re-asserts that the ruling which took the old one is still '
     'standing in both tables')

def pystr(s, ind):
    """Emit `s` as adjacent string literals, wrapped to the file's width."""
    words, out, cur = s.split(" "), [], ""
    for w in words:
        cand = cur + w + " "
        if cur and len(repr(cand)) + ind > 79:
            out.append(cur)
            cur = w + " "
        else:
            cur = cand
    if cur:
        out.append(cur)
    out[-1] = out[-1].rstrip(" ")
    return ("\n" + " " * ind).join(repr(c) for c in out if c)


lines = [BANNER.rstrip("\n")]
by = {}
for f, h in need:
    by[(f, h)] = None
out, used = [], set()
order = ['itch', 'glut', 'rust', 'ngari', 'jeal', 'mul', 'singles', 'spoken',
         'sruwaq', 'green', None]
for sec in order:
    for f, mark, kind, arg, why in SEC.get(sec, []):
        hits = [h for (ff, h) in need if ff == f and mark in h]
        if len(hits) != 1:
            print("!! %s %r -> %d hits" % (f, mark, len(hits)), file=sys.stderr)
            continue
        h = hits[0]
        if (f, h) in used:
            print("!! duplicate %s %r" % (f, h), file=sys.stderr)
        used.add((f, h))
        lines.append("    (%r,\n     %s):\n        (%r, %r,\n         %s)," % (
            f, pystr(h, 5), kind, arg, pystr(why, 9)))
missing = [r for r in need if r not in used]
for r in missing:
    print("!! UNCOVERED %r" % (r,), file=sys.stderr)
print("covered %d of %d" % (len(used), len(need)), file=sys.stderr)
io.open(os.path.join(ROOT, ".scratch", "b242", "block.py"), "w",
        encoding="utf-8").write("\n".join(lines) + "\n")
