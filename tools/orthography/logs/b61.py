"""Batch 61: four greens their own cards had already answered.

Method note, because it is the point of this batch. greenmatch2 scores every green
token on shape x gloss against the whole modern lexicon, and its top rows are
mostly noise -- it offered psmrata 軍隊 for his swatan (a Japanese loan), kmptuhan
寡婦 for his kdapan (a value already spoken for by his KPTOXAN, batch 32), and
tnhadut 送的人 for his tnlikut 找藉口的人 on the strength of the shared string
"的人". Not one of the four written here came from that ranking. All four came
from the SIBLING test -- a mapped key on the same card, where the root has already
been decided and the green form only has to join it.

x'lyeq > hgliq
   His own card says it: "撕裂的——撕碎的。參見 XG'LYEQ 及其派生詞（意義相同）" --
   see XG'LYEQ and its derivatives, SAME MEANING. xg'lyeq>hgliq is shipped, with
   44 keys of that family already mapped (hmgliq 撕開 3x, hgliqi 撕開 2x,
   hgliqan 撕裂了, hnegliq 撕裂的, mhgliq 裂開). His cross-reference is evidence
   in his own hand, the QL'XAO move again.

lnbu > rnbug
   On LMBU (LMBUG ?) 浸泡（在水裡）: "Saon mo lnbu ksia ka lukus mo" 我要把我的衣
   服泡在水裡. lmbug>rmbug 浸泡 2x is shipped on that card, so the root is rbug --
   and rnbug 醃漬或悶過的 is attested, the n-form his lnbu is. His dropped final g
   is the same drop his own lmbu shows against lmbug.

maidang > meydang
   On the PEIDANG card, in "Maidang tunuç" 心不在焉 -- a head that is lost. That
   card's own meidang>meydang 迷路 29x is shipped, with mneidang>mneydang 10x and
   peidang>peydang 49x beside it. His ai/ei is one vowel written two ways; the
   value is the card's. NOT mridang 遺失, which is what the matcher wanted on the
   card's headword gloss: 0x, and it would split one root across two answers.

lmobo > rmudu
   On LODO 巢－窩: "Pusu qliyut bukwi sapax mo, kika yaxan bi lmobo" 鳥兒最喜歡到我
   家後面的桑樹上築巢. The sub-form is Lmodo and lmodo>rmudu is already shipped, as
   is mlodo>mrudu 做窩者 3x. His b-for-d inside his own sub-form's example is the
   same slip batch 60 fixed on LB'NAO (mlb'bao inside Mlb'nao's example), and the
   value is that sub-form's.

HELD, with the evidence recorded rather than acted on -- each fails a different
test, and saying which is the point:
 - BSQLOL 在鍋裡燒焦的食物. sqrul 燒焦 and msqrul are attested (1x each) and the
   gloss is exact, but his b is in the headword, the parenthetical (BSQ'LOL) AND
   the example, so it is his and not a scan artifact. Reaching msqrul means
   deleting a consonant he wrote three times; keeping it means inventing bsqrul.
   Note for later: charRules prints bsqrur, and the modern root ends -ul, so the
   final letter is wrong today whatever the b turns out to be.
 - PTLYAON 使旋轉. The root is certain -- triya 陀螺 2x, pstryai 使旋轉 2x,
   mstriya 旋轉, striya -- but the map is already inconsistent about how his tlya
   spells out: pntlyaan>pntriyan (with the i, and attested 8x 婚宴) against
   psklyaon>pskryaun (without it, blind). Picking either shape for ptlyaon would
   deepen a disagreement instead of settling it. Suspect-value item.
 - mnnaspat 八次. maspat 八 150x is the only form of this numeral in the corpus;
   there is no mn- reflex. But `mnnaspat` is more likely a TRANSCRIPTION defect
   than a spelling one -- mn-maspat with the second m read as n is exactly the
   ~250-token typewriter class, and the rule there is to fix the transcription
   upstream, not to write the misreading into the map. Same bucket as ilnabao.
 - npamuxul (QAPAX, "kika npamuxul da" 這樣就會很暖和). The ROOT is settled and
   already shipped -- muxul>meuxul 很暖和 40x, uxul>uxul -- which means charRules
   is printing npamuhur today and destroying both an x and an l that modern keeps.
   But his n-pa- prefix has no clean modern counterpart (empmuuxul 2x, pkeuxul 2x,
   smeuxul 1x all differ), so every candidate is blind on the prefix.
 - sinbong (QAPAX, 糊上報紙). IDENTIFIED, not written: it is Japanese 新聞
   shinbun, tier J's business, not a Truku respelling. The corpus has no word for
   報紙 at all. Worth recording because charRules prints sinbung -- his -ong is
   -ung everywhere else (bobong>bubung) -- where a loan from shinbun should end
   -n. Do not let the general rule decide a loan.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    "x'lyeq": "hgliq",      # his own 參見 XG'LYEQ（意義相同）; xg'lyeq>hgliq shipped
    "lnbu": "rnbug",        # lmbug>rmbug on the same card; rnbug 醃漬或悶過的
    "maidang": "meydang",   # PEIDANG's own meidang>meydang 迷路 29x
    "lmobo": "rmudu",       # b-for-d inside Lmodo's example; lmodo>rmudu shipped
}
# refuse to write anything lexical_map.json has already vetoed -- the b57 lesson:
# adjudicated = (manual|llm) - lex_block, so a null there silently discards the key
lex = json.load(io.open(H + "lexical_map.json", encoding="utf-8"))
blocked = sorted(k for k in FIX if k in lex and not lex[k])
if blocked:
    print("!! lex_block would discard these -- withdrawing: %s" % blocked)
    for k in blocked:
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
