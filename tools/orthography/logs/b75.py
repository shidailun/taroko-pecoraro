"""Batch 75: the first words ever taken out of the never-swept fields.

Four keys, from tag / paradigm / crossRef -- fields no sweep in seventy-four
batches had read. Three are the self-contradiction signature (the right modern
word already sitting on his OTHER spelling of the same word, on the same card),
and one is an overturn of a hand-entered value that was never attested.

p'ngao>pungaw. His PONGAO card is 甲蟲－金龜子－鞘翅類昆蟲 and pongao>pungaw is
already tier A; the tag on that card is (P'NGAO) (R), the same word with his
elision mark. pungaw 金龜子（昆蟲名）spk 20, with gmpungaw 專找金龜子 and
empeepungaw behind it. Nothing to weigh.

qdoan>qduan, a CORRECTION, and the third human-tier value this review has
overturned after knmlaan and kila. qdoan was hand-mapped to qdugan. His card is
腋下, and 腋下 in modern Truku is qduan, with sqduan 腋下味 and sknqduan 把腋下當成
confirming it. qdugan is not attested at all -- the only qdug- word is qdug 欺騙.
The error is legible: a +g glide (the derived table has +g/fin at 54) papering
over the o-a hiatus in qdoan, which is exactly the kind of rule that fires where
the real word simply has no glide. His tag (QDOWAN?) (R) is the same word again
and gets the same value.

silwi>xiluy. His SILWI card reads （或：XILWI?）鐵—鐵絲 -- both spellings in his own
hand, on the same card -- and xilwi>xiluy is already tier B. xiluy is attested at
spk 36, and the family settles the sense: psxiluy 做鐵器, mtxiluy 鐵匠, tmxiluy
專找鐵料, maaxiluy 看鐵的質. Its headline gloss 鋼筋 looked narrow next to his
鐵－鐵絲, so the alternative was qnawal, which emptqnawal 鐵絲工人 does gloss as
wire -- but qnawal on its own is 電話 spk 61, the telephone, wire having moved on.
xiluy is the iron word.

q'tqot>qdqut and qtqot>qdqut. His Q'TQOT card is 手銬－捆綁犯人的繩索 and modern
qdqut is 鍊條;鐵鍊, with qdqji 要…鎖住 beside it. The t/d looks like a stretch until
you notice HE writes it both ways himself: his QDQDAN card, 束縛－鐐銬－桎梏, carries
crossRef QTQOT. Two spellings of one root in his own cross-reference, and modern
Truku settles on the d.

HELD, and the inconsistency is deliberate:

sq'tqot 3x stays green beside a brown qdqut on the same card. Its gloss
用來捆綁－鏈條－繩索－束縛 is the s- instrument form of exactly the word being
shipped, and sqdqut would be well formed -- but it is not attested, and the whole
point of the colour is that well formed is not attested. The modern dictionary
records no derivative of qdqut at all beyond qdqji.

ikaxa. His SNKAXA card is 前天 and its tag claims the root is IKAXA. snkaxa>sngkaxa
is tier M and sngkaxa 前天 is attested, so the card itself is settled; but the
modern root is kaxa (glossed only as the root of mkaxa 後天, pkaxa 延誤, pxaan
使…久等), and ikaxa with its initial i is attested nowhere. Held for want of a
form. Worth noting the root is direction-neutral -- 前天 and 後天 are both built
on it -- so his 前天 gloss is no obstacle.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # his own tag (P'NGAO) (R) on the PONGAO card; pongao>pungaw is tier A
    "p'ngao": "pungaw",      # WAS green;  pungaw 金龜子（昆蟲名）spk 20
    # CORRECTION of a hand-entered value: qdugan is attested nowhere
    "qdoan": "qduan",        # WAS qdugan (M);  qduan 腋下, sqduan 腋下味
    "qdowan": "qduan",       # WAS green;  his tag (QDOWAN?) (R), same word
    # his SILWI card says （或：XILWI?）in his own hand; xilwi>xiluy is tier B
    "silwi": "xiluy",        # WAS green;  xiluy spk 36, mtxiluy 鐵匠, psxiluy 做鐵器
    # his QDQDAN card cross-refs QTQOT -- he writes the root with d AND with t
    "q'tqot": "qdqut",       # WAS green 2x;  qdqut 鍊條;鐵鍊, qdqji 要…鎖住
    "qtqot": "qdqut",        # WAS green 2x;  same word in the QDQDAN tag/crossRef
}

NOTES = {
    "_qdugan_never_existed": (
        "QDOAN>qduan OVERTURNS A HAND-ENTERED qdugan -- the third human-tier value "
        "this review has had to correct, after knmlaan (mapped to itself, string "
        "absent from modern Truku) and kila (attested, wrong word). His card is 腋下. "
        "Modern 腋下 is qduan, and the family confirms it: sqduan 腋下味, sknqduan "
        "把腋下當成. qdugan is attested NOWHERE; the only qdug- word in the dictionary "
        "is qdug 欺騙. The error is legible and worth keeping: a +g glide -- the "
        "derived correspondence table carries +g/fin at 54 occurrences -- papering "
        "over the o-a hiatus in qdoan. That rule is real, it just does not fire "
        "here, and a rule that is real most of the time is precisely the kind that "
        "gets hand-copied onto a key where the actual word has no glide. Whenever a "
        "value differs from the attested word by one inserted segment, suspect the "
        "insertion rule before believing the value."
    ),
    "_sqtqot_held_well_formed": (
        "SQ'TQOT 3x HELD GREEN beside a brown qdqut on the same card, and the "
        "inconsistency is the point. q'tqot 手銬 ships to qdqut 鍊條;鐵鍊 because the "
        "target is attested. sq'tqot 用來捆綁－鏈條－繩索－束縛 is the s- instrument form "
        "of that same word and sqdqut would be perfectly well formed -- the modern "
        "dictionary simply does not record it, or any other derivative of qdqut "
        "beyond qdqji 要…鎖住. Shipping it would put the colour brown on a form "
        "nobody has attested, which is exactly what brown is supposed to rule out. "
        "A reader seeing qdqut brown and sqtqut green on one card is being told the "
        "truth: we know the noun, we are guessing the derivative."
    ),
    "_qtqot_he_writes_both_d_and_t": (
        "Q'TQOT>qdqut rests on HIS OWN cross-reference, not on a t>d rule. The t/d "
        "correspondence is not in the derived table and a shape argument alone would "
        "not carry it. What carries it is that he writes the root both ways himself: "
        "his QDQDAN card (束縛－鐐銬－桎梏) has crossRef QTQOT, so the d spelling and the "
        "t spelling are one word in his own apparatus, and modern Truku settles on "
        "the d -- qdqut 鍊條;鐵鍊, qdqji 要…鎖住. Same shape of evidence as smoa/smloa, "
        "bqxos/bqlos and kila/k'la: when he prints both spellings, the pair decides "
        "what no single correspondence rule could."
    ),
    "_ikaxa_root_is_kaxa": (
        "IKAXA HELD -- for want of a form, not a meaning. His SNKAXA card is 前天 and "
        "its tag claims the root is IKAXA. The card itself is already settled "
        "(snkaxa>sngkaxa tier M, and sngkaxa 前天 is attested). The modern root is "
        "kaxa, glossed in the dictionary only by what it builds -- 「mkaxa 後天」、"
        "「pkaxa 延誤、費時」、「pxaan 使…久等」-- and ikaxa with its initial i is "
        "attested nowhere. Note the root is DIRECTION-NEUTRAL: 前天 and 後天 are both "
        "built on kaxa, so the gap between his 前天 and mkaxa's 後天 is no obstacle "
        "and should not be recorded as one. What is missing is the i-, and dropping "
        "a segment to reach an attested word is a bigger claim than the evidence "
        "here supports."
    ),
}

lex = json.load(io.open(H + "lexical_map.json", encoding="utf-8"))
lex.update(NOTES)
json.dump(lex, io.open(H + "lexical_map.json", "w", encoding="utf-8", newline="\n"),
          ensure_ascii=False, indent=1)
print("lexical_map -> %d keys" % len(lex))

p = H + "manual_map.json"
d = json.load(io.open(p, encoding="utf-8"))
before = len(d)
for k, v in FIX.items():
    old = d.get(k)
    print("   %-10s %-10s -> %s" % (k, old or "(green)", v))
    d[k] = v
body = ",".join("%s:%s" % (json.dumps(k, ensure_ascii=False),
                           json.dumps(v, ensure_ascii=False))
                for k, v in sorted(d.items()))
io.open(p, "w", encoding="utf-8", newline="\n").write("{\n" + body + "\n}\n")
print("manual_map %d -> %d" % (before, len(d)))
