"""Batch 63: the highest-frequency wrong brown in the review, and two more like it.

These came out of audit2, which lists the 1290 keys whose tier is `id` or `B` --
the two branches of build_modern_map.py that never consult a gloss. Tier `id` is
literally "his token, normalised, exists somewhere in modern Truku, therefore his
word IS that word"; tier B is "unique attested candidate (no gloss needed)". They
have been brown, i.e. claiming to be verified, the whole review. Rows 0-175 read
in frequency order; these are what survived.

All three share one shape, and it is the shape that makes them safe to write: THE
MAP ALREADY ACCEPTS THE RIGHT MODERN WORD FOR A NEIGHBOURING KEY OF HIS, and left
this one on an unrelated word. That is the same internal contradiction that
justified lifting the ttuun null in batch 62 -- ttui shipped brown while ttuun was
nulled -- and it is evidence from the map's own behaviour, not from my judgment.

PAX 103x -- the big one.
   His card 1 is 從——自——由…起——時間、地點的起點, with "Pax Morisaka betak
   Tyakang" 從 Morisaka 到 Tsiakang, and across the dictionary it does exactly
   that job: 孩子從昨晚起 (AKAI), 有來自上面的命令 (BALAO), 自從跌倒以後 (BIYAX),
   自古以來 (BLAEQ).
   The shipped value pax is 打人的聲音（擬聲詞）-- the sound of hitting someone --
   at spk 0. It is a pure accident of his x=h convention. charRules would print
   pah, which is not a word either.
   Modern paah is 求 | 從, spk 591, and NOTHING in the map pointed at it. The
   paradigm is fully on record: pnaah 已從…地方。| 自；從 spk 187, empaah 將從…
   地方 spk 13, npaah spk 2, sgnaah spk 8, spaah spk 2.
   And his pnax > pnaah IS ALREADY SHIPPED AND CORRECT. The map has been
   accepting the paah root for the n-form while leaving the headword on an
   onomatopoeia.
   npax  -> npaah   his 源自…之物的一部分; blind gloss but spk 2, and it is the
                    regular n-form of a root now established. WAS npax, blind.
   mpax  -> empaah  his 帶來者——由…出發者 against 將從…地方 spk 13. WAS empax, blind.
   NOT written: snax, which keeps its charRules snah. His own note asks 詞根＝PAX？
   and the answer is yes, but the s-form is not on record: snaah spk 0 blind,
   and sgnaah spk 8 / spaah spk 2 are different prefixes, not his slot. Well
   formed is not attested. Held and recorded in _snax.
   Homograph, stated: his PAX card 2 is 拿來！給！, a different word on the same
   key, and mpax sits on card 2 with his own note that it answers to both senses.
   A flat map cannot split a key across two cards. Card 1 is the one with the
   headword, the paradigm and the 103 occurrences.

PAI 14x.
   His card is 1) 祖母／外婆。2) 岳母／婆婆。3) 對年長婦女的尊稱, and modern payi is
   女性長輩(祖母；外婆；岳母) | 阿嬤 at spk 357 -- his three numbered senses, in
   order, in one gloss. The shipped pai is 去揹 at spk 1.
   His baki 祖父 is already shipped correctly as baki 外公 spk 488; this is the
   other half of that pair, and it was wrong.
   Collateral, named rather than hidden: his APA paradigm line reads
   "° Mapa, apa, pai, paan, paon." -- the carry-imperative, and the shipped
   value pai 去揹 is right for THAT token. One token in one paradigm line against
   a headword, three of its own examples, and six uses on other cards (BLAEQ
   祖父祖母, DALEX 岳母, DAOLYAQ 婆婆, LUBWI 祖母, TATAQ 岳母, TINUN 祖母), plus
   spk 357 against spk 1. The bigger card wins and _pai records what it costs.

LOAN 10x.
   His headword is written "LOAN (LOWAN ?)" -- he is asking whether it is LOWAN,
   and his lowan IS ALREADY SHIPPED as ruwan 內部，裡面 spk 379. Meanwhile loan
   sits on ruan 要…弄 spk 16, a different word. He answered his own question and
   the map took the answer for one spelling only.
   Every occurrence is the same word: 真正痛的是在裡面, 我們進裡躲一躲, and the
   household sense 一個家庭 / 全家 / 我家, which is the inside of a house.
   NOT written: 'loan, which shares the value ruan today. The ownership check
   says it belongs to his "LO card -- 傳染, contagion -- not to this one, so it
   is left alone. Recorded in _loan.

Held, with reasons, from the same rows:
   mali 13x  audit2 showed his 買、賣（動詞形）against mali 加多. But the MALI
             entry is tag "name (f)" -- a female name -- and the verb slot lives
             on his BALI card. Two cards, one key, and one of them is a name, so
             the identity value is the only value that serves either. _mali.
   Cleared on inspection, not defects: sinao (pnsinaw/ptgsinaw/ksinaw carry the
   wine sense), tasil (tmtasil 專取岩石), ita and nita and ksa (two-card
   homographs where the shipped value serves the bigger card), bbuyo (audit2
   quoted a sub; the headword 荒地——山野 is bbuyu exactly), toxoi (nothing else
   in the corpus carries 陪 above spk 0), and the whole personal-name class where
   the omnibus files 人名 on the same shape as the real word -- rungay 猴子,
   lungaw 瓶子, harung 松樹, pisaw 麻雀, gasil 繩子, biyuq 汁液, sipaw 對面.
   CLOSED from the open list: bare tana 11x was suspected of being tama with the
   typewriter m read as n. It is not -- his 複合人稱代名詞＝我們與他 against modern
   tana 我們;他對我們 spk 11 is the same pronoun.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # PAX: 從/自, the root the map already used for his pnax
    "pax": "paah",        # WAS pax 打人的聲音（擬聲詞）spk 0;  paah 求|從 spk 591
    "npax": "npaah",      # WAS npax (blind);  npaah spk 2
    "mpax": "empaah",     # WAS empax (blind);  empaah 將從…地方 spk 13
    # PAI: the other half of the baki pair
    "pai": "payi",        # WAS pai 去揹 spk 1;  payi 祖母；外婆；岳母 spk 357
    # LOAN: the spelling his own headword offers, already shipped for lowan
    "loan": "ruwan",      # WAS ruan 要…弄 spk 16;  ruwan 內部，裡面 spk 379
}

NOTES = {
    "_pax": (
        "PAX 從——自——由…起, 103x, the highest-frequency wrong brown found in the "
        "review. The shipped value was pax 打人的聲音（擬聲詞）spk 0, an accident of "
        "his x=h convention; charRules prints pah, also not a word. Modern paah "
        "求|從 spk 591 is his gloss, and the paradigm is on record: pnaah spk 187, "
        "empaah spk 13, npaah spk 2, sgnaah spk 8, spaah spk 2. The decisive point "
        "is that his pnax>pnaah was ALREADY shipped and correct -- the map accepted "
        "the root for the n-form while leaving the headword on an onomatopoeia. "
        "HOMOGRAPH, stated: his PAX card 2 is 拿來！給！, a different word on the "
        "same key, and mpax sits on card 2 with his own note that it answers to "
        "both senses. A flat map cannot split it; card 1 has the headword, the "
        "paradigm and the occurrences."
    ),
    "_snax": (
        "SNAX 以…為出發點. HELD, batch 63, while the rest of the paah family moved. "
        "His own note asks 詞根＝PAX？ and the answer is now yes, but his s-n- slot "
        "is not on record: snaah is spk 0 and blind, and sgnaah spk 8 / spaah spk 2 "
        "are different prefixes, not his form. It keeps the charRules snah, which "
        "asserts nothing. Well formed is not attested."
    ),
    "_pai": (
        "PAI 祖母／外婆／岳母. Batch 63: pai>payi, 女性長輩(祖母；外婆；岳母)|阿嬤 spk "
        "357, which is his three numbered senses in order; the shipped pai was 去揹 "
        "spk 1. His baki 祖父 was already correct, so this is the other half of that "
        "pair. COLLATERAL, deliberately accepted and recorded: his APA paradigm "
        "line is \"\u00b0 Mapa, apa, pai, paan, paon.\", where pai is the "
        "carry-imperative and the OLD value was the right one. That is one token in "
        "one paradigm line, against a headword, three of its own examples and six "
        "uses on other cards (BLAEQ, DALEX, DAOLYAQ, LUBWI, TATAQ, TINUN), all "
        "grandmother. The bigger card wins; this note is the cost."
    ),
    "_loan": (
        "LOAN 內部－在…裡. Batch 63: loan>ruwan. His headword is written \"LOAN "
        "(LOWAN ?)\" -- he asks whether it is LOWAN -- and his lowan was ALREADY "
        "shipped as ruwan 內部，裡面 spk 379 while loan sat on ruan 要…弄 spk 16. He "
        "answered his own question and the map took the answer for one spelling "
        "only. The household uses (一個家庭, 全家, 我家) are the same word, the "
        "inside of a house. NOT TOUCHED: 'loan, which shares the old value ruan. "
        "The ownership check puts it on his \"LO card -- 傳染, contagion -- so it "
        "is a different word and keeps its respelling."
    ),
    "_mali": (
        "MALI. HELD, batch 63, and it cannot be fixed by a flat map. audit2 showed "
        "his 買、賣（動詞形）against mali 加多 spk 2, but the MALI entry is tag "
        "\"name (f)\", a woman's name, and the buy/sell verb slot lives on his BALI "
        "card. Modern buy is marig spk 172 / brigan spk 25 (already his bligan). "
        "One key, two cards, one of them a name: the identity value is the only "
        "value that serves either, so it stays."
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
