"""Batch 72: five, including the first correction of a hand-checked value.

Two of them are the self-contradiction signature at its cleanest -- his own map
already carrying the right modern word on a neighbouring key of his:

SMOA -> smruwa 已同意 spk 21. He wrote both spellings ON THE SAME LINE, with his
   own variant marker between them: Nasi so smoa (vl. smloa) o 你若允許我. And
   smloa>smruwa is already tier B, as is sloa>sruwa 同意 spk 35. So the word was
   decided; the parenthesis he put beside it was not. Exactly the KIISO/KISO
   signature of batch 70 -- a variant he flagged himself, left green because a
   flat map has no way to follow a vl. note.

MPAASO -> empeasug 要分. His mp'aso>empeasug is tier M, and four more of the
   family are human-checked with it: p'aso>peasug, pp'aso>ppeasug, mp'paso>
   emppeasug, kmp'aso>kmpeasug. This is the same word with the elision mark
   written as a doubled vowel instead -- his habit, first seen from the other
   side in batch 70 (psaanak, pnaanak, paaanak against his pnanak/snanak). Root
   confirmed by masug 分(東西) spk 11 and asug 分配, and his sentence is 他把他的
   麵包掰開，分給孩子們. Note mpaso>empaa su (M) is a DIFFERENT key -- two words
   with a space -- and must not be read as a rival value for this one.

PNTA'TO -> pnteetu. His knta'to>knteetu is tier M carrying 22 slots and
   snta'to>snteetu is projected from it, so his -ta'to is their -teetu on
   human authority. What the -ta'to means is settled by pteetu 立碑 spk 2, and
   all three of his pnta'to sentences are that verb and nothing else: 你立起來的
   竹子有點歪, 你豎立的那塊石頭上下顛倒了, 你種的那棵樹. Stated with its one
   reservation: pnteetu itself is not in the omnibus. What carries it is that
   the base IS, with exactly the right gloss, and that the <n> perfective is
   regular -- 1193 pnX forms are attested and 434 of them sit beside their own
   pX. The only other word glossed 立起 in the whole dictionary is phyigun
   要掛；要立起, which is nowhere near his shape.

And two that correct the map rather than fill a gap:

KNMLAAN -> knmalu 好的 spk 47. This one was already brown, on tier M, mapped to
   ITSELF -- a human-checked claim that knmlaan is modern Truku. It is not: the
   string appears nowhere in the omnibus, and nothing in the spoken corpus is
   built on it. His own card gives the gloss in two languages -- Malu = Beau,
   bien; Knmlaan = beauté, bonté / Malu＝美、好；Knmlaan＝美、善 -- so this is
   the nominal of malu 好 spk 568, and the modern dictionary has exactly one
   word for it, knmalu 好的 spk 47. His l for the syncopated u is the same
   spelling he uses throughout.

KMLAAN -> knmalu. Green, one slot, and the same nominal: Tayai bi ka kmlaan
   trabus so! 你的花生品質（好處）真是非凡！ -- the goodness of your peanuts.
   Shipped with knmlaan because it is his other spelling of it, not a separate
   word; note that kmalu IS attested but glosses 正在梳, combing, so the
   shape-nearest modern word is the wrong one and the gloss is what decides.

HELD / RECORDED:

MIYAQ -- carried on the suspect list for several batches because miyak looked
   unattested. It is attested, as a cross-reference entry rather than a headword
   (empmiyak 要忙家務事, mmiyak 忙家務事, mnegmiyak 在忙家務事), and his card is
   田間播種與收割以外的農活 -- weeding, hoeing, gathering odd crops. Same word.
   miyaq>miyak is CORRECT. Removed from the suspect list.

MALUN -> malun, tier M, is now the same shape of doubt knmlaan was: malun is not
   among the sixteen malu-shaped words in the omnibus. Not touched here because
   his slots have not been read; queued.

SIIPA -- the only other member of the doubled-vowel class, and it does not work
   the way mpaaso does. His own sipa ships on identity, which decides nothing,
   and his sentence (siipa kana xei so da 冷得直發抖) is not the sipa card's
   meaning. The class is now exhausted at two members.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # he wrote both spellings on one line with his own vl. marker; smloa>smruwa is B
    "smoa": "smruwa",        # WAS green;  smruwa 已同意 spk 21, sruwa 同意 spk 35
    # his doubled vowel writing the elision mark; mp'aso>empeasug is tier M
    "mpaaso": "empeasug",    # WAS green;  empeasug 要分, masug 分(東西) spk 11
    # his knta'to>knteetu is M at 22 slots; the base pteetu 立碑 is attested
    "pnta'to": "pnteetu",    # WAS green 3x;  pteetu 立碑 spk 2 -- 你立起來的竹子
    # CORRECTIONS of an unattested tier-M identity claim -- the nominal of malu
    "knmlaan": "knmalu",     # WAS knmlaan (M, unattested);  knmalu 好的 spk 47
    "kmlaan": "knmalu",      # WAS green;  his other spelling of the same nominal
}

LEXNULL = {}

NOTES = {
    "_knmlaan": (
        "KNMLAAN>knmalu 好的 spk 47 -- batch 72, and the first time this review has "
        "overturned a value that was already brown on a HUMAN tier rather than filling "
        "a green. knmlaan was mapped to itself on tier M, which asserts that his "
        "spelling is already modern Truku. It is not: the string is absent from the "
        "omnibus, absent from the spoken corpus, and nothing is built on it. His own "
        "card gives the meaning twice over -- Malu = Beau, bien; Knmlaan = beaute, "
        "bonte, and in Chinese Malu=美、好；Knmlaan=美、善 -- so it is the nominal of "
        "malu 好 spk 568 and the modern dictionary has exactly one word for that, "
        "knmalu. His green kmlaan (你的花生品質（好處）真是非凡) is the same nominal "
        "under his other spelling and ships with it. Two lessons worth keeping: an "
        "identity mapping is a CLAIM, not the absence of one, and it is the claim "
        "least likely to be checked because it never looks like a change; and the "
        "shape-nearest modern word here is kmalu, which is attested but glosses 正在梳 "
        "-- searching the gloss found the right word, searching the shape found a "
        "comb. Audit the rest of the human-tier identity claims the same way: does the "
        "string he kept actually exist in modern Truku at all?"
    ),
    "_pnteetu": (
        "PNTA'TO>pnteetu -- batch 72, shipped on a base plus a regular infix rather "
        "than on attestation of the form itself, which is a weaker footing than this "
        "review normally accepts and is recorded as such. What holds it: his own "
        "knta'to>knteetu is tier M and carries 22 slots, so a human already decided "
        "that his -ta'to is their -teetu; the base pteetu 立碑 spk 2 is attested with "
        "exactly the meaning all three of his sentences have (你立起來的竹子有點歪 / "
        "你豎立的那塊石頭上下顛倒了 / 你種的那棵樹); and the <n> perfective is "
        "productive rather than lexical -- 1193 pnX forms in the omnibus, 434 of them "
        "sitting beside their own attested pX. The one rival, phyigun 要掛；要立起, is "
        "unreachable from his shape. Withdraw if pnteetu ever turns up glossed as "
        "something else."
    ),
    "_miyaq_cleared": (
        "MIYAQ>miyak is CORRECT -- removed from the suspect list in batch 72. It sat "
        "there because miyak returned nothing from the searches that ask for a "
        "headword gloss: it is present only as a cross-reference entry, glossed by "
        "listing its own derivatives (為「empmiyak 要忙家務事」;「mmiyak 忙家務事」;"
        "「mnegmiyak 在忙家務事」的). His card is 田間播種與收割以外的農活（＝除草、"
        "鋤地、收集零星的作物）, farm work other than sowing and harvesting. Same word. "
        "The general point: a modern word can be attested WITHOUT a direct gloss, so "
        "'no gloss found' is not 'not attested', and a suspect list built from gloss "
        "searches alone will hold correct values indefinitely."
    ),
    "_french_leak": (
        "FRENCH METALANGUAGE IN THE TRUKU TOKEN STREAM -- measured this session and "
        "found to be already handled by the app, but NOT by my worklists. His "
        "typescript puts French inside otherwise-Truku fields: Malu = Beau, bien / "
        "Mbanax = Rouge; Knbnaxan = Rougeur / Mapa blongoi (porter la hotte) / Pqaya "
        "(Est-ce de la R. QAYA ?) / Biyoq qouni (var. qoni). A same-slot shadow test "
        "against each slot's own fr field, plus a whole-dictionary read, finds 21 "
        "genuine French tokens: qui est bien plus meme souvent porter parfois bouche "
        "vie suite entendu rouge produit var contraction vouloir bonte beaute hotte "
        "remarque. FORM_PROSE/TAG_PROSE/metaAbbr already grey 20 of the 21 in the "
        "rendered page, so the reader is fine and the green census is fine; remarque "
        "is the one that slips through, as a section-heading headword. The damage was "
        "to the sweeps, which treated all 21 as unverified Truku and generated "
        "candidates for them -- qui was repeatedly offered kuwi 蟲 spk 62, and hotte "
        "got a landing this week. Exclude the list from future worklists. Note atas is "
        "NOT one of them: it appears three times in French text but is his own Truku "
        "headword (這會是 Patas 的詞根嗎?)."
    ),
    "_depth4_cap": (
        "THE DEPTH-4 REWRITE SWEEP IS NOT A SEARCH -- recorded so it is not mined as "
        "if it were. green_rule3 at depth 4 blew its 40000-string frontier cap on 228 "
        "greens out of 228, i.e. every single one, so the 137 'landings' it reported "
        "are whatever happened to fall inside a truncated breadth-first frontier and "
        "carry no information about what is reachable and what is not. An absence in "
        "that output is meaningless and a presence is an accident of ordering. Depth 3 "
        "completes and is the last honest depth for this rule set. This is the same "
        "failure mode as the koobu absence and the jiyujika absence: a search that "
        "cannot cover its space still returns a confident-looking list."
    ),
    "_gloss_first": (
        "GLOSS-FIRST SEARCH, built this session -- the inverse of the rewrite sweeps "
        "and the instrument the review lacked for seventy batches. Every sweep so far "
        "went shape-first: generate strings that look like his token, keep the "
        "attested ones, then read the gloss. That can only reach a word whose SHAPE is "
        "reachable, so it fails exactly where his transcription is worst -- the "
        "typewriter m read as n, the run-together words, the letters he had no key "
        "for -- and it cannot be asked to look for a meaning. gloss_first.py indexes "
        "the omnibus by 2-4 character Chinese gloss runs (71323 distinct), takes the "
        "gloss of the slot each green stands in, and asks which modern words carry "
        "that meaning; shape is then used only to RANK. Runs carried by more than 60 "
        "words are dropped as 的/了 noise. It is what found 兔唇=siras, 發芽=tngrut, "
        "腺=biqir, 蒜=qusul and 比喻=speangal -- every one of them a word no rewrite of "
        "his spelling could ever have produced, and every one of them a HOLD, because "
        "knowing the modern word for his gloss is exactly how you prove his token "
        "cannot be reached rather than guessing that it can."
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
