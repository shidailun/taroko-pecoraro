"""Batch 64: the audit4 sweep's first harvest -- four cards where the map took an
attested-but-unrelated word for one slot and the regular derivation for the rest.

audit2 read row-by-row in frequency order was down to x5-x6 yield, and all four
of batch 63's defects had shared ONE mechanically detectable shape: the map
already accepts the right modern root for a NEIGHBOURING key of his, and leaves
this one on a different word. audit4 detects that shape directly -- per card, the
substring the most values share, then the values that lack it -- with no
morphology and no gloss reading. 142 outlier slots over all 1967 cards, ranked by
(fewest outliers, biggest majority). These are its first four decisions.

Note what kind of write this is. In every case the replacement is BLIND (spk 0),
and in every case that is not a guess: it is the regular derivation of a root the
map has ALREADY shipped for the card's other slots, several of which are equally
blind and were accepted on exactly that basis. The thing being removed is an
attested word that means something else. An attested wrong word is worse than a
blind right one -- and the tier-`id` rule that produced all of these ("his token
exists somewhere in modern Truku, therefore his word IS that word") is precisely
the rule that prefers the former.

ALAX 圍火取暖 -- warming yourself at a fire.
   His P'alax 使人取暖 IS ALREADY SHIPPED as palah, and modern malah 烤火 spk 6 /
   palah 烤火 spk 2 are the attested pair. So the card is the alah root and the
   map already knows it for the p-form.
   alax    -> alah    WAS alax 放棄 spk 25, the abandon word. The key occurs on
                      exactly ONE slot in the whole dictionary -- his own ALAX
                      headword, glossed 圍火取暖 -- so there is no homograph and
                      nothing is lost. alah is spk 0 but it is the root of the
                      two attested forms, and his own card supplies it.
   m'alax  -> malah   one slot, his M'alax (或:malax) 同上之動詞形.
   malax   -> malah   WAS malax 要放棄 spk 49. Five slots: ALAX ex 我們來你的火邊取暖,
                      MISAN ex 樂於在火邊取暖, TAXOT ex 來烤火取暖 -- and BALAX sub
                      Malax 更新 plus its example. HOMOGRAPH, stated: the BALAX
                      slot wants the barah root (his Mbalax is already embarah),
                      and 要放棄 served it no better. Three fire slots against
                      two, and the card that owns the shape is ALAX.

K'PAX 工作 -- work.
   The card ships qmpah, mqpah, dmqpah, qnpahan, pqpah, spqpah, qpahun. Four of
   those are themselves blind. Only the s-slot walked off.
   skpax   -> sqpah   WAS skpax 習慣放鞭炮 spk 2 -- habitually setting off
                      firecrackers -- on a slot he glosses （sk'pax－skapax）
                      用來工作的（工具、方法）. sqpah is s- + qpah, formed exactly
                      as his pkpax>pqpah and spkpax>spqpah already were. Note
                      this was CHOSEN, not a respelling: charRules would print
                      skpah. Tier id preferred an attested unrelated word over
                      the form its own card was built from.

KOYOX 女人—妻子 -- woman/wife.
   Seven of the card's eight subs are already kuyuh derivations -- kykuyuh,
   dkuyuh, skkuyuh, nkuyuh, snkuyuh, tnkuyuh, empakuyuh -- most of them blind,
   over a root at spk 1196.
   kyoxan  -> kuyuhan WAS kyuhan 已擦傷, the rub/scrape root, which serves neither
                      card the shape sits on. Nine slots, and they split 6 woman
                      (IMAX 婦女們, KOYOX sub 對女人們, KOYOX ex 對那些女人, L'XLAX
                      婦人, QADA 妻子, SNAO 妻子) to 3 rain (KOYOC sub 雨天, KOYOC
                      ex 大雨, SIPA 淋了雨). HOMOGRAPH, stated: his KOYOC 雨 card
                      carries the same spelling and wants a quyux form; his
                      Kmoyoc>qmuyux and Pskoyoc>psquyux are already right there.
                      The bigger card takes the key, as with pai.

Cleared by audit4, not defects:
   l'ndax -- CLOSED from the long-standing deferred list. audit4 flagged it
             against his L'DAX 照亮 card (rdax/mrdax/prdax), but he has a
             SEPARATE headword L'NDAX (LNDAX) 變本加厲－更加厲害－更強烈, and rndah
             更加的；反而更 spk 2 matches it exactly. Correct as shipped; audit4
             had quoted the neighbouring 照亮 sub's gloss.
   iyax   -- HELD. 43 slots, and his own headword merges 來 and 間隙: iyah 來 spk
             179 and iyax 中間 spk 115 are both real words and both his. Not a
             defect, an unsplittable key. _iyax.
   The detector's remaining noise class is legitimate morphophonemic syncope,
   where the derived form drops a vowel the root keeps and so fails a substring
   test while being exactly right: kndusan>kndsan, d'xqan>dhqan, gl'man>grman,
   glngani>grngani, kndlxan>qndrxan, pxdagan>phdagan, dyagan>jyagan,
   dlnani>drnani, gguyan>geuyan, lqean>lqian. Recognisable on sight.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # ALAX: the fire-warming root, which his own P'alax > palah already established
    "alax": "alah",        # WAS alax 放棄 spk 25;  alah = root of malah/palah 烤火
    "m'alax": "malah",     # WAS malax 要放棄 spk 49;  malah 烤火 spk 6
    "malax": "malah",      # WAS malax 要放棄 spk 49;  3 of 5 slots are 取暖
    # K'PAX: the s-form his own card is built for
    "skpax": "sqpah",      # WAS skpax 習慣放鞭炮 spk 2;  s- + qpah, cf. pqpah/spqpah
    # KOYOX: the oblique of kuyuh, whose seven siblings are already shipped
    "kyoxan": "kuyuhan",   # WAS kyuhan 已擦傷;  kuyuh spk 1196 + -an, 6 of 9 slots
}

NOTES = {
    "_alax": (
        "ALAX 圍火取暖. Batch 64, from audit4. His P'alax 使人取暖 was ALREADY "
        "shipped as palah, and modern malah 烤火 spk 6 / palah 烤火 spk 2 are the "
        "attested pair, so the card is the alah root and the map already knew it "
        "for the p-form. The shipped alax 放棄 spk 25 was the ABANDON word. The key "
        "alax occurs on exactly one slot in the whole dictionary -- his own "
        "headword -- so there is no homograph. alah itself is spk 0, but it is the "
        "root of the two attested forms and his own card supplies it: a blind right "
        "word beats an attested wrong one."
    ),
    "_malax": (
        "MALAX. Batch 64: malax>malah and m'alax>malah, off malax 要放棄 spk 49. "
        "Five slots, three of them plainly 取暖 -- ALAX ex 我們來你的火邊取暖, MISAN "
        "ex 樂於在火邊取暖, TAXOT ex 來烤火取暖. HOMOGRAPH, stated: his BALAX card "
        "has a sub Malax 更新-使變新, which wants the barah root (his Mbalax is "
        "already embarah) and which 要放棄 served no better than 烤火 does. Three "
        "slots against two, and the shape belongs to the ALAX card. See _alax."
    ),
    "_skpax": (
        "SKPAX （sk'pax－skapax）用來工作的（工具、方法）. Batch 64: skpax>sqpah. The "
        "shipped value was skpax 習慣放鞭炮 spk 2, habitually setting off "
        "firecrackers, on his K'PAX 工作 card whose other seven slots are qmpah, "
        "mqpah, dmqpah, qnpahan, pqpah, spqpah, qpahun -- four of them blind. sqpah "
        "is s- + qpah, formed exactly as his pkpax>pqpah and spkpax>spqpah already "
        "were. This value was CHOSEN, not a respelling: charRules would print "
        "skpah. It is the clearest single instance of what tier id does -- prefer "
        "an attested unrelated word over the form the card is built from."
    ),
    "_kyoxan": (
        "KYOXAN. Batch 64: kyoxan>kuyuhan, off kyuhan 已擦傷 (the rub/scrape root), "
        "which served neither card the shape sits on. Nine slots, splitting 6 woman "
        "(IMAX 婦女們, KOYOX sub 對女人們, KOYOX ex, L'XLAX 婦人, QADA 妻子, SNAO "
        "妻子) to 3 rain (KOYOC sub 雨天, KOYOC ex 大雨, SIPA 淋了雨). kuyuhan is "
        "kuyuh spk 1196 + -an, and seven of the KOYOX card's eight subs are already "
        "kuyuh derivations, most of them equally blind: kykuyuh, dkuyuh, skkuyuh, "
        "nkuyuh, snkuyuh, tnkuyuh, empakuyuh. HOMOGRAPH, stated: his KOYOC 雨 card "
        "spells its 雨天 sub the same way and wants a quyux form -- his Kmoyoc>"
        "qmuyux and Pskoyoc>psquyux are already right there. The bigger card takes "
        "the key, as with pai in batch 63."
    ),
    "_iyax": (
        "IYAX. HELD, batch 64, and not a defect. audit4 flags it because thirteen "
        "of the card's slots are the COME root (miyax>miyah, yaxan>yahan) while the "
        "headword is 中間. But HIS OWN headword merges the two: iyah 來 spk 179 and "
        "iyax 中間 spk 115 are both real modern words and both of them are his. 43 "
        "slots on an unsplittable key. A flat map cannot help this one."
    ),
    "_l'ndax": (
        "L'NDAX. CLOSED, batch 64, from the long-standing deferred list -- correct "
        "as shipped. audit4 flagged lndax>rndah against his L'DAX 照亮 card "
        "(rdax/mrdax/prdax), but he has a SEPARATE headword L'NDAX (LNDAX) = "
        "變本加厲－更加厲害－更強烈, and rndah 更加的；反而更 spk 2 matches it exactly. "
        "audit4 had quoted the neighbouring 照亮 sub's gloss, which is its known "
        "failure mode when one shape serves two of his cards."
    ),
    "_ngali": (
        "NGALI 剩餘－多出的. HELD, batch 64, though it has the pax signature. His "
        "nngali>nngari 剩餘的 and sngali>sngari 剩餘 are already shipped, so the map "
        "does accept the ngari 剩餘;結餘 spk 31 root for the derived forms while the "
        "bare key sits on ngali 拿走；拿取 spk 27, the TAKE word. But the ownership "
        "count goes the other way: 6 take-slots on his ANGAL card against 2 surplus "
        "slots, and his own MASPAT note glosses MANGALI as MA+NGALI＝拿！, so the "
        "take word is real and his. The current value serves the majority. Unlike "
        "pai, the minority here is the headword's own card -- recorded so that if "
        "the homograph problem is ever solved structurally, this is a first case."
    ),
    "_btaqan": (
        "BTAQAN 腿、大腿. HELD, batch 64. Modern 大腿 is btriq spk 23, which is "
        "already the value of his btelyaq -- so moving btaqan there would MERGE two "
        "of his headwords onto one key, losing the distinction he drew. No separate "
        "-an form is on record. Left as shipped."
    ),
    "_lodo": (
        "LODO 巢窩、刀鞘 and Q'LOT 鋸子. HELD, batch 64. Both were checked against "
        "the omnibus for their meanings (巢|鞘, 鋸) and NOTHING in it carries them "
        "at any spoken count. There is no alternative to propose, so the existing "
        "respellings rudu and qrut stand unverified rather than being replaced by a "
        "guess. Distinct from the alax class, where the card itself supplied the "
        "answer."
    ),
}

lex = json.load(io.open(H + "lexical_map.json", encoding="utf-8"))
lex.update(NOTES)
json.dump(lex, io.open(H + "lexical_map.json", "w", encoding="utf-8", newline="\n"),
          ensure_ascii=False, indent=1)
print("lexical_map: notes %s written (%d keys)" % (sorted(NOTES), len(lex)))

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
