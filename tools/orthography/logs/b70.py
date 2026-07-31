"""Batch 70: twelve greens, from a correspondence table that was COUNTED rather
than recalled.

green_rule's rule list was assembled by memory -- each rule added the day some key
forced it. derive_rules.py instead aligns the 1788 human-checked pairs already in
the map with difflib and counts what his spelling actually does, by position. Most
of the list I had. These I did not, and every one of them is commoner in the
checked pairs than rules I was already generating on:

    e > i  115      k > q  59 / q > k 13      d > j  46      t > c  28
    a > e   29      p > k fin 10             ' > e/ee/h/u  131
    +e 113   +g fin 54   +y 42   +w 28   +u 16   +a 19

The insertions are why substitution-only expansion kept missing: the modern word
often carries a vowel his transcription has no letter for at all. So the sweep
runs in two passes -- substitutions alone, then one further edit from the derived
insertion set against SPOKEN landings only. 255 greens in, 21 + 51 out, 12 right.

That is the largest yield of the review, and the reason is worth stating plainly:
for sixty-odd batches I ranked candidates by how they LOOK, and a metric cannot
tell 不容易 from 糯米. Reading his rules off his own checked pairs and then
generating from them replaces the ranking with an argument.

P'PAX -> phpah 花 spk 198. It spells out letter for letter: his apostrophe is
   their h (' > h, 16 in the checked pairs), his x is their h. p-h-p-a-h. And the
   sentence is Nasi so musa pxolyaq nxnaan ta p'pax o 如果你要去澆我們種的花 --
   the flowers we planted, being watered. phpah is the ordinary modern word for
   flower and the commonest landing this review has produced.

PSAANAK -> pseanak 偏見 spk 16, PNAANAK -> pneanak 單獨做過, PAAANAK -> peanak
   另外單獨分. His own map already carries the rule on six sibling keys, four of
   them human-checked: pnanak>pneanak (M), snanak>sneanak (M), psnanak>psneanak,
   pnnanak>pnneanak, msnanak>msneanak, mpsnanak>empsneanak. His -anak is their
   -eanak; these three merely double the a. And the glosses agree exactly --
   his PSAANAK card is 擱置一旁－歧視、隔離 against pseanak 偏見, with seanak
   看輕；輕視；瞧不起 behind it, and his PAAANAK sentence is 至少你不會因人而異地歧視
   別人.

S'LNO -> srngaw. Exact, with no residue at all, under four rules already shipped:
   apostrophe drop, l>r, n>ng (batch 68), o>aw. s + r + ng + aw. His card is
   報告－告知－分享 and his example Ana mk'la ka sadyaq o, ini bi s'lno 即使人們知道
   了，他們也完全不告訴別人. The root is unmistakable -- rngaw 說話 spk 68, prngaw
   向…說, empprngaw 討論 -- and the s- derivation is theirs: sprngaw 為…使說話.

TQLYAAN -> tqrian 裝填 spk 7. Ndoa bi snapang llubwi tqlyaan payai 要好好把袋子補好，
   用來裝稻穀 -- mend the sack to FILL with rice, and tqrian is glossed 裝填. l>r,
   y>i, and his doubled aa for their single a, the same doubling as PSAANAK. The
   family confirms it: tqrii 要裝 spk 10, qrian 被圍繞.

KIISO -> keisug 要怕. His own slot settles this one: Ya kiso (kiiso), adi biyao
   mpanalu ka pa 別怕！你的腳很快就會好！ He gives two spellings of one word in one
   line, and kiso ALREADY SHIPS keisug on tier M, human-checked, while kiiso sat
   green beside it. The modern phrase is Iya keisug 別怕, which is his sentence.

NDOAI -> endwai 好好的 spk 17. Ana ongat ka mtgisa ta da o, ndoai bi mtisa
   雖然我們已經沒有老師了，你們要努力互相教導 -- teach each other WELL. Two derived
   rules and nothing else: the initial e he drops (+e initial, 45 in the checked
   pairs) and o>w.

DMTGISA -> dmtgsa. His own mtgisa>mtgsa is tier M with ten slots; this is the same
   word under the dm- plural agent prefix, which is theirs (dmptgsak). Psliyun mo
   saman ka dmtgisa 我明天要召集所有老師 -- the teachers, plural. tmgsa 教 spk 97.

SINBONG -> singbung. A Japanese loan, and the sentence names the object: Qmapax ko
   sinbong kana mtqeli tqean mo 我在睡覺的地方四周（牆壁）都糊上報紙 -- newspaper
   pasted round the walls for warmth. 新聞 shinbun > singbung, spk 3. Shape exact
   under two shipped rules, n>ng and o>u, with no residue. The omnibus has no word
   glossed 報紙 or 新聞 at all, so this one rests on the loan and the sentence
   rather than on a gloss.

TIPYAQ -> cipiq 不多 spk 6. His card is 少－小量－身材小 and his example Ana qoqo!
   Tipyaq bi nimax mo 沒關係！我只會喝一點點. t>c is 28 in the checked pairs and is
   the ordinary Truku reflex before a front vowel -- the same alternation that
   makes his TYAQONG look like cyaqung.

QELO -> qilug 後腦 spk 4. e>i and his o for their ug, the ayo>ayug rule. The
   omnibus has no other word in the region -- 後頸 and 頸背 return nothing, and
   qilug carries tgqlganay 從後腦打 and ptgqilug behind it. Taken with the
   reservation that his l stays l here rather than going to r; that is the 28-token
   keep-l guard, and 後腦 is one bone from his 後頸.

HELD, with the evidence, because a real word is not yet the right word:

NTA -- 20 slots, the biggest green in the book, and pass 2's most seductive wrong
   answer. nita 我們的 spk 5 is a GENITIVE. His NTA is a hortative: his card says
   邀請前往（唯一使用的形式，與 LITA 並用）and all twenty sentences are Nta da! 走吧,
   Nta sapax da 我們回家吧, Nta mita da 我們去看看吧, Nta smbu lapit 我們去射飛鼠.
   He also writes nita twenty times separately, and that key already ships nita.
   No modern word is glossed 走吧 or 來吧, and modern Truku has no nta at all.

SYULING -- his headword says ??（意義不明）, which reads as "no gloss to check
   against". It is not: his own example gives one. Syuling otoç 皮癬－濕疹－蕁麻疹
   is a skin disease, so siling 問 spk 8 is refuted by the card that looked empty.
   Nothing in the omnibus is glossed 癬 or 濕疹 or 疹 at all.

T'LAP / TLAP -- the headband. trapi 要戴頭巾 spk 2 is his shape (l>r, +i) and his
   semantic field, and it is an inflected imperative where his is a noun; the
   modern noun is trak 毛巾、頭巾 spk 6 with tmrak 戴頭巾 and mnegtrak behind it,
   and trak is not his shape. Recorded because this is the first real evidence
   that a t-r-p headcloth root exists at all.

TMAGO / MTMAGO -- held again, but the objection has moved. Batch 69 held it
   because dahu 自誇、自傲 needed his g to be their h. The rule sweep found
   tmeego spk 2 and mtmeego spk 2 -- exactly his pair, keeping his g, needing only
   a>ee, which the checked pairs support 9 times. So the shape objection has
   dissolved. What is left is that neither landing is glossed anywhere, and the
   root has no glossed relative either: the omnibus has no teego, meego or eego.
   An attested string with no recoverable meaning cannot be asserted as his.

SQOAQE -- the sentence agrees and the shape does not quite. Asi nlut (m'lut ?)
   xeaan ka Awi adi na bi sqoaqe 必須由 Awi 出面（對他施壓），他才不會說話 -- so
   sqoaqe is speaking, and squwaq 吵鬧 spk 19 sits on quwaq 洞口/mouth. But it
   needs his final e to vanish, and e>nothing word-finally is not in the derived
   table (his final e goes to i or y).

TEPYAQ -- four slots, all Kui tepyaq 蟯蟲, and his own headword gloss is ？？.
   If tipyaq is cipiq 不多 then kui tepyaq reads as "little worm", which is what a
   pinworm is. That etymology is mine, not his, and he marked the word unknown.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # ' > h and x > h: p-h-p-a-h, in a sentence about watering the flowers
    "p'pax": "phpah",        # WAS green;  phpah 花 spk 198
    # his -anak is their -eanak on six sibling keys, two of them tier M
    "psaanak": "pseanak",    # WAS green;  pseanak 偏見 spk 16, seanak 輕視
    "pnaanak": "pneanak",    # WAS green;  pneanak 單獨做過; his pnanak>pneanak is M
    "paaanak": "peanak",     # WAS green;  peanak 另外單獨分; 因人而異地歧視別人
    # apostrophe drop + l>r + n>ng + o>aw, no residue; root rngaw 說話 spk 68
    "s'lno": "srngaw",       # WAS green 2x;  srngaw spk 31, cf. sprngaw 為…使說話
    # l>r, y>i, his doubled aa; 用來裝稻穀 against 裝填
    "tqlyaan": "tqrian",     # WAS green;  tqrian 裝填 spk 7, tqrii 要裝 spk 10
    # his own line gives both spellings and kiso already ships keisug on tier M
    "kiiso": "keisug",       # WAS green;  keisug 要怕 spk 16; his sentence is 別怕
    # the initial e he drops + o>w; 要努力互相教導 = teach each other WELL
    "ndoai": "endwai",       # WAS green;  endwai 好好的 spk 17
    # his own mtgisa>mtgsa is tier M; this is the dm- plural of it
    "dmtgisa": "dmtgsa",     # WAS green;  dmtgsa spk 5, tmgsa 教 spk 97
    # Japanese 新聞 shinbun; n>ng and o>u, exact; his sentence pastes NEWSPAPER
    "sinbong": "singbung",   # WAS green;  singbung spk 3
    # t>c before a front vowel, 28 in the checked pairs; 少－小量 against 不多
    "tipyaq": "cipiq",       # WAS green 2x;  cipiq 不多 spk 6
    # e>i and his o for their ug (the ayo>ayug rule); nothing else in the region
    "qelo": "qilug",         # WAS green;  qilug 後腦 spk 4, tgqlganay 從後腦打
}

LEXNULL = {}

NOTES = {
    "_derive_rules": (
        "DERIVE_RULES, batch 70, and why it produced more than the four batches "
        "before it together. green_rule's correspondence table was assembled by "
        "memory -- each rule added on the day some key forced it -- which is how the "
        "n>ng rule sat unused until batch 68 although NYAO>ngiyaw had been in the map "
        "for months. derive_rules aligns the 1788 HUMAN-CHECKED pairs already in the "
        "map with difflib and counts what his spelling does, by position, because his "
        "rules are positional (the velar he drops is a word-END rule and would be "
        "nonsense as a general one). Rules I did not have, each commoner in the "
        "checked pairs than rules I was already generating on: e>i 115, k>q 59 and "
        "q>k 13, d>j 46, t>c 28, a>e 29, p>k word-final 10, and the apostrophe "
        "spelling out as e/ee/h/u 131 times rather than as schwa alone. And the "
        "insertions, which substitution-only expansion could never reach: +e 113, "
        "+g final 54, +y 42, +w 28, +u 16, +a 19 -- the modern word often carries a "
        "vowel his transcription has no letter for. So the sweep now runs twice: "
        "substitutions alone, then ONE further edit from the derived insertion set "
        "against spoken landings only, since one free edit is enough slack to reach a "
        "lot of strings by accident. 255 greens in, 21 + 51 out, 12 right. The "
        "general lesson is the one this review keeps relearning: read his rules off "
        "his own checked pairs instead of ranking candidates by how they look."
    ),
    "_p'pax": (
        "P'PAX 花 -- batch 70, and the cleanest conversion in the review. It spells "
        "out letter for letter: his apostrophe is their h (' > h, 16 times in the "
        "checked pairs) and his x is their h, giving p-h-p-a-h against phpah 花 spk "
        "198, the commonest landing this review has produced. His sentence is Nasi so "
        "musa pxolyaq nxnaan ta p'pax o 如果你要去澆我們種的花，要讓它們的土全都澆透. "
        "Worth recording because it sat green through every earlier sweep: on shape "
        "alone p'pax looks like his very frequent pax>paah 從, and every distance "
        "metric put it there."
    ),
    "_psaanak": (
        "THE -ANAK FAMILY, batch 70: psaanak>pseanak 偏見 spk 16, pnaanak>pneanak "
        "單獨做過, paaanak>peanak 另外單獨分. The self-contradiction signature at its "
        "clearest -- his own map already carried the rule on six sibling keys, two of "
        "them human-checked: pnanak>pneanak (M), snanak>sneanak (M), psnanak>"
        "psneanak, pnnanak>pnneanak, msnanak>msneanak, mpsnanak>empsneanak. His -anak "
        "is their -eanak, and these three keys merely double the a, which he also "
        "does in tqlyaan. The glosses agree without straining: his PSAANAK card is "
        "擱置一旁－歧視、隔離 against pseanak 偏見, with seanak 看輕；輕視；瞧不起 and "
        "anak 分開 behind it, and his PAAANAK example is 至少你不會因人而異地歧視別人."
    ),
    "_kiiso": (
        "KIISO>keisug 要怕 -- batch 70. His own line gives both spellings of one "
        "word: Ya kiso (kiiso), adi biyao mpanalu ka pa 別怕！你的腳很快就會好！ and "
        "kiso ALREADY SHIPPED keisug on tier M, human-checked, while kiiso sat green "
        "beside it in the same sentence. The modern phrase is Iya keisug 別怕, which "
        "is his sentence exactly; miisug 害怕 spk 8 and ksugi 要敬畏 carry the root. "
        "Note kiisug spk 10 also exists in the spoken corpus but is unglossed -- "
        "keisug wins because it is glossed AND because it is what the human check on "
        "his other spelling already chose. When two spellings of one word sit in one "
        "slot, the one already decided settles the other."
    ),
    "_nta": (
        "NTA -- 20 slots, the biggest green in the book, HELD in batch 70 and the "
        "most seductive wrong answer the rule sweep has produced. nita 我們的 spk 5 "
        "is a GENITIVE and his NTA is a hortative. His card: 邀請前往（唯一使用的形式，"
        "與 LITA 並用）. All twenty sentences are invitations -- Nta da! ... Kia! Lita "
        "da! 來吧，來！……好！我們走吧, Nta sapax da 我們回家吧, Nta mita da 我們去看看吧, "
        "Nta smbu lapit 我們去射飛鼠, Nta da tloong ska sapax da 我們進屋裡坐吧. He "
        "also writes nita twenty times as a separate token and THAT key already ships "
        "nita. Modern Truku has no nta at all (spoken count zero) and nothing is "
        "glossed 走吧 or 來吧; the nearest is lita 一起 spk 48, which is his own LITA. "
        "Recorded at length so the next sweep that surfaces nita does not take it."
    ),
    "_syuling": (
        "SYULING -- HELD in batch 70, and a reminder that an empty-looking card may "
        "not be empty. His headword gloss is ??（意義不明）, which reads as 'no gloss "
        "to check a candidate against'. But his own example supplies one: Syuling "
        "otoç 皮癬－濕疹－蕁麻疹. So syuling is a skin disease, and siling 問（請教所不知"
        "道的）spk 8 -- which the rule sweep offered on a one-letter edit -- is "
        "refuted by the card that looked blank. Nothing in the omnibus is glossed 癬, "
        "濕疹, 蕁麻疹 or 疹 at all, so it stays green. Rule: before treating a ?? card "
        "as gloss-free, read its examples."
    ),
    "_tlap": (
        "T'LAP / TLAP 頭帶 -- HELD in batch 70, but with the first real evidence in "
        "this review that the root exists. His card: 太魯閣族特有的頭帶，寬 4 至 6 公分，"
        "繫於頭上，自前額上方繞至後頸底部. trapi 要戴頭巾 spk 2 is his shape under l>r "
        "plus the +i the derived table supports, and it is his semantic field. It is "
        "also an inflected imperative where his word is a noun, and the modern NOUN "
        "in that field is trak 毛巾、頭巾 spk 6 (tmrak 戴頭巾, mnegtrak 喜歡戴頭巾, "
        "hmapung 綁頭巾), which is not his shape. Do not map a noun onto an imperative "
        "to close a green."
    ),
    "_tmago": (
        "TMAGO / MTMAGO 自負的－驕傲的－高傲的－傲慢的 -- HELD AGAIN in batch 70, but "
        "the objection has MOVED and the batch 69 note above is superseded. That note "
        "held it because dahu 自誇、自傲 spk 26 needed his g to be their h, which "
        "nothing supports. The derived rule sweep instead found tmeego spk 2 and "
        "mtmeego spk 2 -- exactly his pair, tmago/mtmago, keeping his g and needing "
        "only his a for their ee, which the checked pairs support 9 times. The shape "
        "objection has therefore dissolved, and the parallel of two forms matching "
        "two forms is not the sort of thing that happens by accident. What blocks it "
        "now is meaning: neither landing is glossed anywhere in the omnibus, and "
        "neither is any relative -- there is no teego, meego or eego to read a sense "
        "off. An attested string with no recoverable meaning cannot be asserted as "
        "his word. Take it the moment a gloss for tmeego turns up."
    ),
    "_green_residue4": (
        "GREEN RESIDUE, fourth pass (batch 70). SQOAQE: his sentence agrees and his "
        "shape does not quite -- Asi nlut (m'lut ?) xeaan ka Awi adi na bi sqoaqe "
        "必須由 Awi 出面（對他施壓），他才不會說話, so sqoaqe is speaking, and squwaq "
        "吵鬧 spk 19 / sqowaq spk 8 sit on quwaq 洞口 (mouth). But it needs his final "
        "e to vanish, and word-finally his e goes to i or y in the checked pairs, "
        "never to nothing. TEPYAQ: four slots, every one Kui tepyaq 蟯蟲, and his own "
        "headword gloss is ？？. If tipyaq is cipiq 不多 then kui tepyaq reads as "
        "'little worm', which is what a pinworm is -- but that etymology is mine and "
        "he marked the word unknown, so tipyaq converts and tepyaq does not. QUI: not "
        "a Truku word at all. Its one slot is inside his French, R. = NGUSUL ? = qui "
        "produit de... -- correctly green as apparatus, and kuwi 蟲 spk 62 is a trap "
        "for any sweep that does not look at the slot. One consequence of tipyaq to "
        "record honestly: the builder's projection tier immediately carried it to his "
        "three derivatives, stipyaq>scipiq, sptipyaq>spcipiq and pntipyaq>pncipiq, "
        "none of which is attested anywhere -- no spoken count, no omnibus entry. "
        "That is tier P behaving as it always does (991 keys, 46 of them attested), "
        "and it is defensible when the root is confirmed and the prefixes are his "
        "own s-, sp- and pn-. But it means one hand-checked root silently produced "
        "three more blind brown assertions, which is the same mechanism that put "
        "~2400 unchecked browns in this map in the first place. Flagged, not fixed: "
        "the fix is a policy decision about tier P across the whole dictionary, not "
        "something to settle inside one batch."
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
