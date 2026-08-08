"""Batch 57: the half-brown card, ranked.

halfbrown.py turns CLAUDE.md finding (4) into a work list. For every green token
it finds the brown sibling on the SAME card whose key shares the longest run of
letters, and prints what the map already believes about it. 147 of the 385 green
types have such a sibling; this batch takes the ones where the sibling settles the
question, in three kinds.

1. THE SIBLING NAMES THE WORD. His two spellings of one slot, or one suffix away:
   mpanamo is empaamanu 能成什麼 (mpananu, his other spelling, was mapped long
   ago); mpn'mu is empnmu beside
   mpnmuon>empnmuun; gn'lyeq is gneeliq beside sn'lyeq>sneeliq, the same class as
   gn'lu>gneelug. Attested outright: mqbahang, hjyali 找到, swayi 474x 同輩,
   psryuun.

2. THE SIBLING NAMES THE ROOT, and the green slot is a suffix on it. pkploon and
   pkploan follow sploon>spruun and sploan>spruan; tnblxan follows tblaxan>tbrahan
   and tblaxon>tbrahun; ptqoe follows ptqoon>ptquwun; psplqe follows
   psplqan>psprqan, with his final -e imperative becoming -i as in batch 55's
   klwaxe>krwahi.

3. THE SIBLING SAYS LEAVE IT ALONE, and the char rules disagree. This is the half
   of the batch that actually changes what you see. A frozen family with one green
   slot left over does not render neutrally -- charRules still runs, so the slot
   prints a fake word while its brown siblings print his: QRUQ beside lqloq,
   TQQRANG beside qqlang, PTRUKAN beside btlukan, TRAWA beside mtlawa, PTQRIYUN
   beside tqliyan, SNUHER beside msnoxel, PRRGUN beside pllgi. Freezing the slot
   is not a claim that his spelling is modern; it is the claim the card already
   made, applied to the slot it skipped.

WITHDRAWN AFTER THE REBUILD, and the reason is the method rather than the words.
Six keys were written, applied, and never reached site/modern_map.js: sl'xqe /
sl'xqan / sl'xqon and t'tuan / ttuan / ttuun. All are nulls in lexical_map.json
(or, for bare ttuan, covered by the same note), and `adjudicated = (manual|llm) -
lex_block` subtracts them by design -- a null there is itself a human decision to
stay green, and manual_map is not allowed to overrule it silently. The notes say
so outright: _sl'xqan "shik has no locative, patient or imperative on record, so
there is nothing to substitute", and _ttuun "well formed is not attested ...
naming ttuun or ttuan would be my construction, not a lookup. (Claimed twice now
-- b48 ttuun, b49 t'tuan -- and reverted both times.)" This was the third claim.
The card therefore keeps printing SRHQE/SRHQAN/SRHQUN and TTUAN, which is the
half-brown defect surviving on purpose: green there means the family's own root
does not reach the slot, and inventing a shape to cover it is not respelling.
Verify against the BUILT map (landed.py), never against manual_map.json.

AND THE BUILDER HAS BEEN SAYING SO EVERY RUN. Chasing the six turned up a line of
build output I had never read: "curated keys that never landed [DEAD]: 20". A dead
key is one that matches no token in entries.js at all. dead.py resolves every one,
and the reassuring half is that none of them costs a green word:

 - TEN are a mark-fold apart from a live twin that is ALREADY brown with the same
   value -- d'xo'/d'xo, d'yax/dyax, dxyaq/d'xyaq, knudus/kn'udus, mpkudus/mpk'udus,
   pkudus/pk'udus, sa so/sa'so, sdxyaq/sd'xyaq, slosi/slösi, and mpkuda/mpkuda'.
   That last one is this batch's: his raw token is `Mpkudaʔ`, with U+0294 GLOTTAL
   STOP, which tkey folds to `'` -- so the key is `mpkuda'`, and it was already
   empkudaw at HEAD, reached by a tier before I ever wrote the entry. My key was
   never the fix. (rawtok.py hid this: its token class omitted U+0294, so it
   reported a bare `Mpkuda` the census does not have. Fixed.)
 - EIGHT match nothing at all, and they are residue of the typewriter repair
   (memory: his m reads as n) -- stana>stama, smtana, pstana, nani>nami. The
   transcription was corrected at source, which is the right fix and which orphans
   the map key by design. byequn, mnudus, ska'nan, tibilaq the same. Two more live
   in llm_map.json (qeuni>qhuni, sanao>snaw) and are left for a pass over that file.

All eighteen manual ones are deleted here. The point is not the cleanup, which
changes nothing on the page -- it is that twenty lines of standing noise is why the
alarm went unread for fifty batches. With them gone, the next DEAD line means
something. The map diff after deleting them is asserted empty, because tier V reads
`manual` membership to overrule a machine twin, so a dead key is not provably inert
until measured.

imp.py: 22 newly impossible, and sibgram.py clears all but one. Fourteen are class-3
identity freezes, where being unwritable in modern Truku is the whole point -- the
value is HIS spelling, frozen so charRules stops printing a fake word beside its
brown siblings. Of the constructed values, every solo dead 4-gram has a
well-witnessed core (prq 18, pkp 8, nss 9, mga 61, nm 75), which is batch 56's
sparse-population signature and not a phonotactic violation. The exception, flagged
and NOT fixed here: `pshmqun`'s `hmq` has **zero** witnesses at the trigram, which is
the `adag` signature of a real violation -- but the shipped `psxm'qan`>`pshmqan`
already carries it, so this batch is being consistent with a claim an earlier batch
made, not making a new one. The PSXM'Q stem needs its own look.

Held from the same list: nta (20x, the documented hold), banasi and tbilan and
kmubui and mpeidang (the sibling shares three letters by accident -- kasi, alang,
kmux, ldanan), MASPAT (mnaspat absent), TBAKO (tbako>lumak is a substitution and
slumak does not exist), TIPYAQ (no shipped sibling to follow, unlike BASYAQ).
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # 1. the sibling names the word
    "mkbaxang": "mqbahang",          # kbaxang>qbahang; mqbahang attested
    "mpanamo": "empaamanu",          # his own mpananu, mapped long ago
    "xdyali": "hjyali",              # xdyalan>hjyalan; hjyali 找到
    "suwai": "swayi",                # mnsuwai>mnswayi; swayi 474x
    "pslyuwun": "psryuun",           # pslyuwan>psryuan; psryuun 2x
    "gn'lyeq": "gneeliq",            # sn'lyeq>sneeliq
    "mpn'mu": "empnmu",              # mpnmuon>empnmuun
    # 2. the sibling names the root
    "pkploon": "pkpruun", "pkploan": "pkpruan",      # sploon>spruun
    "tnblxan": "tnbrahan",                           # tblaxan>tbrahan
    "ptqoe": "ptquwi",                               # ptqoon>ptquwun
    "psplqe": "psprqi",                              # psplqan>psprqan
    "plyuxai": "pryuxi",                             # plyuxan>pryuxan; pryuxi 2x
    "pnoxon": "pnuxun",                              # noxon>nuxun, keeps x
    "tlqelan": "trqilan",                            # tnlqelan>tnrqilan
    "mgangax": "mgangah",                            # ngangax>ngangah
    "psxm'qun": "pshmqun",                           # psxm'qan>pshmqan
    "slngiyun": "srngiyun",                          # pslngiyun>psrngiyun
    "snqlawax": "snkrawah",                          # his own Snklawax, mapped
    "knss'gan": "knssgan",                           # ks'gan>ksgan
    # 3. the sibling says leave it alone -- and charRules disagrees
    "q'loq": "qloq",                 # lqloq;  was printing QRUQ
    "tqq'lang": "tqqlang",           # qq'lang>qqlang;  was TQQRANG
    "ptlukan": "ptlukan",            # btlukan;  was PTRUKAN
    "tlawa": "tlawa",                # mtlawa;  was TRAWA
    "ptqliyun": "ptqliyun",          # tqliyan;  was PTQRIYUN
    "snoxel": "snoxel", "snxelan": "snxelan",        # msnoxel;  was SNUHER
    "pllgun": "pllgun", "llgun": "llgun",            # pllgi;  was PRRGUN
    "btudan": "btudan", "btudun": "btudun", "pntudan": "pntudan",   # bntudan
    "basyaq": "basyaq", "tibasyaq": "tibasyaq",      # tbasyaq
    "psyangi": "psyangi", "psyangan": "psyangan",    # psyangun, knsyangan
    "tnppngan": "tnppngan",          # tnpngan
    "dup": "dup",                    # mdup
    REDACTED,          # sayang
    "pspdagi": "pspdagi",            # pspdagun, batch 56
    "psttuy": "psttuy",              # psttui
}

# withdrawn after imp.py: knrsan (knrs and nrsa both dead, and knruusan does not
# exist either, so the -an of knruus is simply unknown); kmpstruung / kmpstrngun
# (truu is dead, and his loong is tluung 坐 elsewhere in the dictionary -- the
# shipped kmstloon>kmstruun may itself be wrong, so this is not a card to follow).
DROP = ["knl'san", "knlsan", "kmpstloong", "kmpstlngun",
        # the lex_block six -- see the docstring; removed from manual_map so the
        # file stops asserting something the builder is designed to discard.
        "sl'xqe", "sl'xqan", "sl'xqon", "t'tuan", "ttuan", "ttuun",
        # the eighteen DEAD keys -- no token in entries.js matches them
        "byequn", "d'xo'", "d'yax", "dxyaq", "knudus", "mnudus", "mpkuda",
        "mpkudus", "nani", "pkudus", "pstana", "sa so", "sdxyaq", "ska'nan",
        "slosi", "smtana", "stana", "tibilaq"]

p = H + "manual_map.json"
d = json.load(io.open(p, encoding="utf-8"))
for k in DROP:
    d.pop(k, None)
before = len(d)
clash = {k: (d[k], v) for k, v in FIX.items() if k in d and d[k] != v}
if clash:
    print("overriding %d earlier manual keys:" % len(clash))
    for k, (o, n) in sorted(clash.items()):
        print("   %-10s %s -> %s" % (k, o, n))
d.update(FIX)
body = ",".join("%s:%s" % (json.dumps(k, ensure_ascii=False),
                           json.dumps(v, ensure_ascii=False))
                for k, v in sorted(d.items()))
io.open(p, "w", encoding="utf-8", newline="\n").write("{\n" + body + "\n}\n")
print("manual_map %d -> %d  (batch touches %d keys)" % (before, len(d), len(FIX)))
