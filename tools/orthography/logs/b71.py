"""Batch 71: eight more, from the derived table applied as REWRITES.

green_rule2 expanded per character, which can express x>h but cannot express
ye>i, 'lo>ru, lye>ri or dya>ji -- and those are not marginal in the checked
pairs: 'lo>ru is counted 26 times, ye>i 35, '>ee 40, d>j 46. A per-character
table cannot see a multi-letter rule no matter how many single-letter rules are
added to it, so every green whose spelling turned on one was unreachable. green_
rule3 derives the table the same way and then searches breadth-first, applying
one rule at a time, with positional rules anchored (the velar he drops is a
word-END rule and would be nonsense as a general one). Five of the eight below
are multi-letter or word-final rules that the earlier sweeps could not reach.

Four of the eight are the self-contradiction signature -- his own map already
carrying the right modern word on a sibling key:

NGLAUN -> ngalun 拿來當；用來做 spk 45. He writes ngalun thirty-two times and it
   has always shipped ngalun; nglaun once, with the two letters swapped. Nglaun
   mo tnd'xgan sapax ka tasil nii 我要拿這塊石頭來加固房子 -- take this stone to
   use for strengthening the house, which is the modern gloss word for word.

QALIP -> qrip. His own card says 參見 KALIP, and kalip>qrip, mkalip>mqrip and
   pkalip>pqrip are all tier M, human-checked, while qalip sat green beside
   them. k>q initial is 47 in the checked pairs; qmarik 剪掉 spk 7 and qribun
   剪成 spk 4 hold the root against his 剪、裁.

TNAI -> tmay 進入、進來 spk 19. NOT a spelling rule at all -- this is the
   typewriter defect, his m read as n, the same fault that made nuxul out of
   muxul. His tmai already ships tmay on tier A, mtmai>mtmay on A and ptmai>
   ptmay, so the word was never in doubt; only this one token was misread. And
   his sentence names it: Xmuya ka ini so tnai sapax! 你為什麼不進屋裡. The rule
   sweep offered tngay 滿 instead, which fits the SECOND clause (裡面連一點點空位
   都沒有了) and not the word.

DYUDIKA -> jiyujika 十字架. A Japanese loan, 十字架 juujika, and his gloss is
   Btaqe dyudika 釘上十字架!. d>j is 46 in the checked pairs -- the rule the
   per-character table could not hold -- and his own sosidyu>susidyu is already
   tier J. Recorded also as a near-miss of my own: searching for jyujika and
   juujika returned nothing, and the dictionary writes jiyujika. Same fault as
   the koobu 帳篷/帳棚 clearance; search the gloss, not the spelling you expect.

LAGAP -> ragak, LMAGAP -> rmagak 下對流雨 spk 2. One entry, noun and verb: his
   LAGAP is 傾盆、連續、驟然而至、無雷雨的大雨 and his LMAGAP is 同上之動詞形. A
   thunderless downpour is a convective shower, which is what 對流雨 names, and
   smragak 下對流雨的季節 puts a third form behind it. l>r plus his word-final
   p>k, which is counted 10 times in the checked pairs and which I had never
   once used before this batch.

QODAP -> qudak, PTQODAP -> ptqudak 使…漸弱. Word-final p>k again, with o>u. His
   QODAP is 熄滅（火、生命）－自行熄滅 and his example is L'pi do, sqmaon na ini
   ptqodap taxot da 他要在不滅的火中把它燒掉 -- a fire that never ptqodap. The
   modern set is qudak (風)減弱, ptqudak 使…漸弱, mtqudak 漸弱: dying down rather
   than being put out. Taken with that reservation stated, since the modern word
   for extinguishing a fire is phing (emphing 去熄滅, mnegphing 被熄滅), which is
   nowhere near his shape, and his own example is precisely about a fire that
   will not die down.

HELD:

TQODAP -- 3 slots, the biggest of the QODAP family, and tqudak is not attested;
   only mtqudak is. Left green rather than invented, though tier P will very
   likely project it now that qodap is mapped -- see _tier_p_projection.

QDAPAN / KDAPAN -- his own card asks 是否與 KDAPAN＝鰥夫、寡婦有關聯, and a
   widower is not an extinguished fire. No candidate either way.

TYAQONG and GLAQON -- both refused in batch 69 and both refused again, but with
   something new to record: the exact d1 landings cyaqong spk 8 and glaqong spk
   11 DO exist in the spoken corpus, distinct from cyaqung 烏鴉 spk 4 and
   glaqung 藍腹鷴 spk 14. Neither is glossed anywhere, so neither can be
   asserted -- but it means the batch 69 refusals were refusing the wrong word.
   His 雉雞 may well be cyaqong rather than the crow. Revisit if a gloss appears.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # his own ngalun ships ngalun 32x on identity; this is the same word, letters swapped
    "nglaun": "ngalun",      # WAS green;  ngalun 拿來當；用來做 spk 45
    # his card says 參見 KALIP and kalip>qrip is tier M; k>q initial, 47 in checked pairs
    "qalip": "qrip",         # WAS green;  qmarik 剪掉 spk 7, qribun 剪成 spk 4
    # the typewriter m read as n -- his own tmai>tmay is tier A
    "tnai": "tmay",          # WAS green;  tmay 進入、進來 spk 19; 你為什麼不進屋裡
    # Japanese 十字架 juujika; d>j, 46 in the checked pairs; his sosidyu>susidyu is J
    "dyudika": "jiyujika",   # WAS green;  jiyujika 十字架
    # l>r plus word-final p>k; a thunderless downpour is a convective shower
    "lagap": "ragak",        # WAS green;  root of rmagak 下對流雨, smragak 下對流雨的季節
    "lmagap": "rmagak",      # WAS green;  rmagak 下對流雨 spk 2 -- his 同上之動詞形
    # word-final p>k and o>u; his own example is a fire that never dies down
    "qodap": "qudak",        # WAS green;  qudak (風)減弱, mtqudak 漸弱
    "ptqodap": "ptqudak",    # WAS green 2x;  ptqudak 使…漸弱
}

LEXNULL = {}

NOTES = {
    "_green_rule3": (
        "GREEN_RULE3, batch 71: the derived table applied as REWRITES rather than as "
        "per-character alternatives, which is what finally let the multi-letter rules "
        "fire. green_rule2 could express x>h but not ye>i, 'lo>ru, lye>ri or dya>ji, "
        "and those are not marginal in the checked pairs -- 'lo>ru 26, ye>i 35, '>ee "
        "40, d>j 46. No number of extra single-letter rules can reach a multi-letter "
        "one, so every green whose spelling turned on one was structurally invisible. "
        "green_rule3 searches breadth-first from each green, applying one derived rule "
        "at a time to depth D, with positional rules anchored: a rule counted only "
        "word-finally is applied only word-finally, because the velar he drops is a "
        "word-END rule and would generate nonsense as a general one. Depth is printed "
        "beside every landing, since a depth-3 hit is much weaker evidence than a "
        "depth-1 hit and the sentence still decides. Five of batch 71's eight turned "
        "on a multi-letter or word-final rule, including word-final p>k -- counted 10 "
        "times in the checked pairs and never once used before this batch."
    ),
    "_tnai": (
        "TNAI>tmay 進入、進來 spk 19 -- batch 71, and NOT a spelling correspondence. "
        "This is the typewriter defect: his m read as n, the same fault that produced "
        "nuxul for muxul. His tmai already ships tmay on tier A, mtmai>mtmay on A, "
        "ptmai>ptmay on P -- the word was never in doubt, only this one token was "
        "misread. His sentence settles which clause the token belongs to: Xmuya ka ini "
        "so tnai sapax! ... Ongat bi ana kingal yax ka loan da! 你為什麼不進屋裡……"
        "裡面連一點點空位都沒有了！ The rule sweep offered tngay 滿（與thngay 同義）, "
        "which matches the SECOND clause and not the word -- a good reminder that a "
        "sentence can contain the gloss of a word that is not the one being checked. "
        "Add tnai to the transcription-repair list (nuxul, ilnabao, upsk'la, ukwi, "
        "umyaq, dnqpax, mnnaspat): these are misreadings of his typescript, not "
        "features of his orthography, and mapping them one at a time is a stopgap."
    ),
    "_dyudika": (
        "DYUDIKA>jiyujika 十字架 -- batch 71, and my own near-miss worth recording. "
        "Japanese 十字架 juujika, his Btaqe dyudika 釘上十字架!, and d>j is 46 in the "
        "checked pairs -- the very rule the per-character sweep could not express. His "
        "sosidyu>susidyu is already tier J so the pattern was in the map. I searched "
        "the omnibus for jyujika, juujika, jujika and kurusu and got zero; the "
        "dictionary writes jiyujika. That is the koobu 帳篷/帳棚 fault again in a "
        "different alphabet: an absence proved with the spelling I expected is not an "
        "absence. Searching the GLOSS -- 十字 -- returned it immediately, first try."
    ),
    "_qodap": (
        "THE QODAP FAMILY, batch 71: qodap>qudak, ptqodap>ptqudak 使…漸弱, on his "
        "word-final p>k plus o>u. Stated with its reservation: his gloss is 熄滅"
        "（火、生命）－自行熄滅 and the modern glosses are all 漸弱/減弱, dying down "
        "rather than being put out, with qudak specifically noted (風). Two things "
        "carry it anyway. The modern word for extinguishing a fire is phing (emphing "
        "去熄滅, mnegphing 被熄滅, empkphing 會熄滅), nowhere near his shape, so there "
        "is no rival. And his own example is exactly about a fire that will not die "
        "down: L'pi do, sqmaon na ini ptqodap taxot da 他要在不滅的火中把它燒掉. "
        "TQODAP is HELD at 3 slots -- the biggest of the family -- because tqudak is "
        "not attested and only mtqudak is; QDAPAN/KDAPAN is held because his own card "
        "asks 是否與 KDAPAN＝鰥夫、寡婦有關聯 and a widower is not a dead fire."
    ),
    "_tier_p_projection": (
        "TIER P PROJECTION, flagged in batch 70 and again in 71. When a hand-checked "
        "root lands, the builder's projection tier immediately carries it to his "
        "derivatives -- tipyaq>cipiq produced stipyaq>scipiq, sptipyaq>spcipiq and "
        "pntipyaq>pncipiq, none of them attested anywhere (no spoken count, no omnibus "
        "entry), and qodap>qudak will very likely do the same to tqodap. That is tier "
        "P behaving exactly as designed (991 keys, 46 of them attested) and it is "
        "defensible when the root is confirmed and the prefixes are his own. But it "
        "means one checked key silently makes several UNCHECKED brown assertions, "
        "which is the same mechanism that put ~2400 unverified browns in this map via "
        "tier id. Recorded here rather than patched, because the question -- should P "
        "project onto unattested strings at all, or should it mark them for review -- "
        "is a policy decision about the whole dictionary and should not be settled as "
        "a side effect of whichever batch happens to touch a productive root."
    ),
    "_cyaqong": (
        "TYAQONG and GLAQON -- refused in batch 69, refused again in 71, but the "
        "batch 69 notes were refusing the WRONG WORD and that is worth fixing. The "
        "exact one-rule landings do exist in the spoken corpus: cyaqong spk 8 (his "
        "tyaqong under t>c, nothing else) and glaqong spk 11 (his glaqon under the "
        "final velar). Both are distinct from the words batch 69 argued against -- "
        "cyaqung 烏鴉 spk 4 and glaqung 藍腹鷴 spk 14 -- and neither is glossed "
        "anywhere in the omnibus. So the refusals stand, but on the correct ground: "
        "not 'a crow is not a pheasant' but 'the word his spelling actually points at "
        "has no recoverable meaning'. His 雉雞 may well be cyaqong. Revisit the moment "
        "either gets a gloss."
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
