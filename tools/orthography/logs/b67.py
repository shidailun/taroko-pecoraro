"""Batch 67: the first batch that converts GREENS.

Batches 64, 65 and 66 all corrected words that already claimed to be verified, and
green held at 272 types / 399 occurrences through all three. Green is the unknown
count, so this batch goes after it -- and the way in was to stop searching by
shape and search by MEANING.

Three sweeps, in order. audit6 asked audit5's question of unmapped tokens (a
neighbour within two edits that ALSO shares a gloss bigram): 10 of 272 types
produced any candidate at all, five of them his French-apparatus letter entries.
green_near dropped the gloss test and printed the neighbourhood: 4 of the 57 types
at >=2 slots have no modern word within two edits at all, and the rest are string
coincidences -- nta against 他的, banasi against 如果, dilam 斑鳩 against 怕丟臉.
green_gloss inverted it: take HIS gloss, find every spoken modern word sharing a
two-character Chinese word with it, and print the edit distance instead of gating
on it, because ayo>ayug was 2 and ml'bu>mgrbu was 3 -- distance is evidence to
weigh, not a filter. Restricted to distinctive glosses (a bigram carried by more
than 40 words is register, not a name for a thing), that is 36 types at >=2 slots.

Four keys, and the sweep also caught one wrong brown on the same card as a green.

WAKAT 4x -- 犬齒, and the sprout metaphor is his own.
   All four of his forms are green: wakat, his variant waqat, mwakat, snwakat.
   The modern word is waqit, spk 8, glossed 芽 -- and the omnibus carries exactly
   his polysemy: swaqit 大獠牙, smwaqit 長芽. His card is 犬齒（牙齒）, his example
   is Waqat (wakat) boyaq 山豬的獠牙, his sub Mwakat is 有犬齒的－長出嫩芽的, and
   his SLIYU example spells out the metaphor: Ga psliyu waqat na ka bonga p'xpax
   花的球莖開始發芽（長出它們的牙齒（＝嫩芽）). Two dictionaries a century apart
   independently record the same word doing teeth and buds. His own spelling waqat
   is one letter from waqit.

SL'DAN 2x -- 黏附, and his own card had already decided it.
   The S'LUT card ships s'lut>sdlut 黏上, ms'lut>msdlut and ps'lut>psdlut, all
   three tier M and human-checked. The fourth key was left green, when the omnibus
   holds sltan 被黏著（引申為受青睞）spk 2 -- that root's -an form, and his gloss
   黏附；被黏合之物 word for word. The self-contradiction signature (pax/pnax,
   skawas/sxkawas) pointed at a green instead of at a wrong brown. sltani 被黏著
   confirms the paradigm; the containment test misses it only because the modern
   root alternates sdlut/slut and sltan syncopates the vowel.

LUULA 1x -- 公開地, the bare root under four forms the map already ships.
   His LUULA card ships pluula>preura, tluula>treura, ptluula>ptreura and
   ptllaani>ptreurani -- every derived form on the -eura stem, tier M and P -- and
   leaves the headword green. He asks the question himself in the note: 這真的是
   詞根嗎？還是 TLUULA 的簡化形？ The omnibus answers it. Bare eura and reura are
   both unattested; ura is attested, spk 2, glossed 公開、清白 -- his 公開地－公然地
   exactly. The stem is confirmed around it: pteura 很明顯的 spk 12, mtreura 明顯
   spk 4, mteura 公開的 spk 2, steura 清楚的.

LUUS -- a wrong brown, nulled rather than moved, because there is nowhere to move it.
   His LUUS card is 獨自－孤獨－單身 (Luus ko bi! Ongat bais mo da! 我好孤單!我再也
   沒有朋友了!). The map ships knluus>knruus 偷偷地去;暗暗地去 on tier B, from the
   modern root ruus 秘密 -- a real word, a different word, and a blind assertion
   that contradicts the card. Modern 獨自 is the burux family (burux 單獨 spk 4,
   emburux 獨自 spk 8), which is nowhere near his shape, so there is no better
   value: LEXNULL, which is what green is for.
   NOT nulled: luus>luus, which is the identity. It is equally blind and equally
   contradicted -- modern luus is the 成熟 root, tgluus 成熟 spk 44 -- but charRules
   folds l to r, so nulling it would print RUUS, which IS the 秘密 word. Leaving
   the identity leaves his own spelling on screen; nulling it would put a wrong
   modern word there. Same reasoning as lawa in batch 66: do not make it wrong.

Cleared as ABSENT -- the green residue is bounded by what modern Truku contains,
and these were read one at a time to prove it rather than assumed:
   koobu 帳篷 -- the omnibus has no word glossed 帳篷 or 遮蔽 at all. His own note
         says the Truku knew only the blanket-over-branches shelter.
   dobut 瓶子 -- his card names the synonym itself (同義詞＝LONGAO) and that one is
         already correctly brown: longao>lungaw. There is no second bottle word.
   kmupan 發霉 -- modern 發霉 is the tapung and rabung families; the only shapes
         near his are kupan 板嘴 and qupang 性慾衝動. From the deferred list.
   swatan 布農 -- the omnibus has no word glossed 布農 anywhere. An ethnonym his
         neighbours used and the modern dictionary does not record.
   moxong 芽/花苞 -- 芽 is waqit (see WAKAT), 花苞 is the ngrut and rungut families.
         None is within reach of MUHUNG.
   bsqlol 燒焦 -- the root IS found: his sqlol is sqrul letter for letter once l>r
         and o>u apply, and sqrul 燒焦 spk 1 with psqrlan 使...燒焦 confirms it. But
         no b- form is attested, and every bsqr- word in the omnibus belongs to a
         different root (bsqar 射擊, bsqur 勒死). Well formed is not attested.
   knlsan/knl'san 獨自 -- same card as LUUS above, same absence.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # WAKAT: 犬齒 and 嫩芽, the same polysemy the modern waqit carries
    "wakat": "waqit",      # WAS green;  waqit 芽 spk 8, swaqit 大獠牙, smwaqit 長芽
    "waqat": "waqit",      # his own variant spelling, one letter off already
    # SL'DAN: the -an form of the sdlut his own card ships three times over
    "sl'dan": "sltan",     # WAS green;  sltan 被黏著 spk 2 (sltani 被黏著 confirms)
    # LUULA: the bare root under preura / treura / ptreura / ptreurani
    "luula": "ura",        # WAS green;  ura 公開、清白 spk 2
}

# a null forces the key GREEN on every tier: an honest unknown in place of a
# blind brown that names a different word
LEXNULL = {
    "knluus": None,        # WAS knruus 偷偷地去 (root ruus 秘密) vs his 孤獨的程度
}

NOTES = {
    "_wakat": (
        "WAKAT 犬齒, 4x, all four of his forms green -- wakat, waqat, mwakat, "
        "snwakat. Batch 67, and the first green converted in four batches. The "
        "modern word is waqit spk 8, glossed 芽, and the omnibus carries HIS "
        "polysemy beside it: swaqit 大獠牙, smwaqit 長芽. He spells out the "
        "metaphor himself on SLIYU -- Ga psliyu waqat na ka bonga p'xpax 花的球莖"
        "開始發芽（長出它們的牙齒（＝嫩芽）) -- and his sub Mwakat is 有犬齒的－"
        "長出嫩芽的, his Snwakat 長出犬齒－長出插枝（嫩芽）. Two dictionaries a "
        "century apart record one word doing teeth and buds. His own variant "
        "spelling waqat is a single letter from waqit; the headword takes the same "
        "value. mwakat and snwakat are left to the generative tiers, as ayo's "
        "m- and mpa- forms were in batch 66."
    ),
    "_sl'dan": (
        "SL'DAN 黏附, 2x. Batch 67. Its own card had already decided it: S'LUT "
        "ships s'lut>sdlut 黏上, ms'lut>msdlut and ps'lut>psdlut, all tier M and "
        "human-checked, and left the fourth key green. sltan 被黏著（引申為受青睞）"
        "spk 2 is that root's -an form and his gloss 黏附；被黏合之物 word for word; "
        "sltani 被黏著 confirms the paradigm. This is the self-contradiction "
        "signature -- pax/pnax, skawas/sxkawas, mnswai/mnswayi -- found on a GREEN "
        "for the first time rather than on a wrong brown. The card-sibling detector "
        "missed it because it tested containment: the modern root alternates "
        "sdlut/slut and sltan syncopates the vowel, so sltan does not contain sdlut."
    ),
    "_luula": (
        "LUULA 公開地－公然地, 1x. Batch 67: luula>ura. Every derived form on his "
        "card was already shipped on the -eura stem -- pluula>preura, tluula>treura, "
        "ptluula>ptreura, ptllaani>ptreurani, tiers M and P -- while the headword "
        "itself stayed green. He asks the question in his own note: 這真的是詞根嗎？"
        "還是 TLUULA 的簡化形？ The omnibus answers it. Bare eura and bare reura are "
        "unattested; ura is attested at spk 2 and glossed 公開、清白, which is his "
        "headword exactly. The stem is confirmed around it: pteura 很明顯的 spk 12, "
        "mtreura 明顯 spk 4, mteura 公開的 spk 2, steura 清楚的."
    ),
    "_luus": (
        "LUUS 獨自－孤獨－單身. Batch 67: knluus LEXNULLED, luus left alone, and the "
        "difference between the two is the point. knluus shipped knruus 偷偷地去;"
        "暗暗地去 on tier B -- a real modern word, from the root ruus 秘密, and "
        "nothing to do with his 孤獨的程度. A blind brown that names a different "
        "word is worse than an honest green, and there is nowhere better to send it: "
        "modern 獨自 is the burux family (burux 單獨 spk 4, emburux 獨自 spk 8), not "
        "within reach of his shape. So it is nulled, and green rises by one on "
        "purpose. luus>luus is equally blind and equally contradicted -- modern luus "
        "is the 成熟 root, tgluus 成熟 spk 44, against his Luus ko bi! Ongat bais mo "
        "da! 我好孤單 -- but it is the IDENTITY, and charRules folds l to r, so "
        "nulling it would make the reader print RUUS, which is the 秘密 word. "
        "Leaving it leaves his own spelling on screen. Same rule as lawa in batch "
        "66: do not make the losing side wrong. His knlsan/knl'san stay green for "
        "the same absence."
    ),
    "_green_residue": (
        "THE GREEN RESIDUE IS ABSENCE, NOT NEGLECT -- measured in batch 67, and the "
        "reason the unknown count stops where it does. Three sweeps over the 272 "
        "green types. audit6 (a neighbour within two edits that also shares a gloss "
        "bigram): 10 types produced any candidate at all, five of them his French-"
        "apparatus letter entries o, a, k, m, g, which are correctly green. "
        "green_near (drop the gloss test, print the whole neighbourhood): of the 57 "
        "types at >=2 slots, 4 have no modern word within two edits at ALL, and the "
        "rest are string coincidences -- nta against 他的/我們, banasi against 如果, "
        "lex against 進入洞的聲音, dilam 斑鳩 against 怕丟臉, l'xqoi 糯米 against "
        "不容易. green_gloss (his gloss first, distance printed rather than gated): "
        "36 types at >=2 slots, and reading them yielded this batch's four. What is "
        "left is words modern Truku does not contain: koobu 帳篷 (no word glossed "
        "帳篷 or 遮蔽 anywhere), swatan 布農 (no word glossed 布農 anywhere), dobut "
        "瓶子 (his own card gives the synonym LONGAO, already brown as lungaw), "
        "kmupan 發霉 (modern is the tapung/rabung families), moxong 芽/花苞 (芽 is "
        "waqit, 花苞 the ngrut/rungut families), bsqlol (root sqrul 燒焦 confirmed, "
        "but no b- form attested and every bsqr- word is a different root). Green is "
        "bounded below by the modern dictionary, not by how long anyone looks."
    ),
    "_psqexon": (
        "PSQEXON 被人強迫. Batch 67, NOT written -- the nearest thing to a fifth key "
        "and the reason it was refused. The modern force root is there: pskixan "
        "強迫 spk 3, pskyxay 讓…強制 spk 2, pskixi 讓...勉強 spk 2, pskyux 強制. But "
        "his q is not their k -- q and k are separate phonemes in Truku, and the "
        "one psq- word in the omnibus, psqixan, is glossed 被雨淋. His -on/-un would "
        "want pskixun or pskyxun and neither is attested. Well formed is not "
        "attested; a real word is not yet the right word."
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
