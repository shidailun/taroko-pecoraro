"""Batch 73: six, from fields no sweep in this review has ever looked at.

The census counts the rendered page and finds 223 unverified types. Every sweep
built in seventy-two batches walks entries.js and finds 203. That gap is not
rounding: entries carry tag, paradigm and crossRef, and subs carry paradigm and
crossRef, and NOTHING has ever tokenised them. They hold his variant spellings
(the parenthesised second form he prints beside a headword), his full inflection
paradigms, and his cross-reference targets -- 104 green types across 874
occurrences, most of it the metadata labels the app already greys, but with real
Truku underneath that has been invisible this whole time.

Compounding it, the census reports what charRules PRINTS, not what he wrote, so
a green in the census cannot be looked up in his text at all -- srhqun, rngut,
hru and musa are outputs, not tokens. reconcile.py walks every field, applies
the fallback, and groups by what lands on screen, which is the first worklist in
this review that matches what the reader actually sees.

Two of the six carry his own parenthetical, which is the strongest evidence this
dictionary produces -- he wrote both spellings himself, side by side:

BQXOS -> bqrus 屍體 spk 11. His BQLOS card is tagged (BQXOS), and his sentence
   under NGONGO spells it out: Mngongo ko bi muda bqxos (bqlos) ka'man 我很害怕
   晚上經過墓地. He put the other spelling in brackets beside it. bqlos>bqrus is
   already tier A, human-checked, and the modern family is large and unambiguous
   -- bqrus 屍體, tnbqrus 墳墓的主人, tmnbqrus 整理過墓地, ttbqrus 經常做墓地.

KILA -> kla, and KILÂ -> kla 知道 spk 297. His card is explicit past any doubt:
   知道。(註:此詞有時以這種雙音節形式 KILA 出現,似乎確是 K'LA 的異常變體...)。
   在絕大多數情況下,幾乎所有發音人都以 K'LA 的形式使用這個表「知道」的詞。參見
   K'LA. And again he writes it himself in a sentence -- Ini kila (k'la) kmpax
   ka lisao. His k'la>kla already ships. This is a CORRECTION: kila was mapped
   to itself, and the string kila IS attested in modern Truku -- as the root of
   smkila 適應, sklaan 適應的地方. Attested, and the wrong word. Exactly the trap
   kmalu 正在梳 set in batch 72, one batch later and in the opposite direction:
   there the shape-nearest word was wrong, here the shape-IDENTICAL word is.

ÑILAO -> ngiraw 香菇 spk 6. His NILAQ card is tagged (ñilao), and nilao>ngiraw
   is already tier M. The only thing separating this token from the mapped one
   is the tilde he put on the n, which the fallback strips to nilao -- a string
   that then has no key of its own.

KAOBU -> kowbu. His KOOBU card is tagged (var. KAOBU) in his own words, and
   koobu>kowbu is tier M. The koobu entry is the one whose gloss cost a search
   earlier in this review (帳篷/帳棚); its variant has sat green beside it since.

PG'DGIT -> pgdgit 咬牙切齒生氣狀 spk 2. His PGDGIT card is tagged (PG'DGIT), and
   pgdgit>pgdgit ships on tier id. Worth noting that this one UPGRADES the
   identity claim rather than trusting it: pgdgit is attested with his meaning
   (his card is 使牙齒磨動－磨牙, and dgit 咬牙切齒聲；磨牙聲 sits behind it), so
   the blind identity happens to be right and is now checked.

HELD, with the evidence recorded because these are new territory:

L'QBUÇ / LQBUX 穿山甲 -- and this one turns up a SUSPECT SHIPPED VALUE. His
   lqbux>rqbux is tier B, and rqbux is attested -- glossed 不按部就班做工;不踏實
   地做事, working carelessly. That is not a pangolin. The modern word for 穿山甲
   is arung spk 17, unreachable from his shape by any rule. So the B value looks
   like the attested-string-wrong-meaning trap again, and l'qbuç is NOT shipped
   to match it; matching would have propagated the error to a second key.

SL'XQE / SL'XQAN / SL'XQON 舔 -- his own slxoqe>srhuqi, slxoqan>srhuqan and
   slxoqon>srhuqun are tier B, and these are the same three paradigm slots under
   his elision-mark spelling instead of his o spelling. Normally that is enough.
   Held because NONE of srhuqi, srhuqan, srhuqun is attested anywhere, so
   shipping would extend an unverified projection onto three more keys rather
   than resolve anything. The inconsistency -- one spelling brown, the other
   green, same word -- is real and is flagged for the tier-B audit.

KTII -- his KTUI paradigm is Kmtui, ktui, ktii, ktian, ktiun, and four of the
   five are mapped (kmtui>kmtuy M, ktui>ktuy M, ktian>kciyan A, ktiun>kciyun B).
   The ti>ciy correspondence in ktian/ktiun predicts kciyi or kcii for the
   imperative and neither is attested. Held for want of a form, not a meaning --
   the meaning is settled, kmtuy 收割 spk 42.

PSNNAI -- the NAMA paradigm, his psnama>psnama on tier id, and psnama IS
   attested (預備 spk 2). psnnai is its imperative and psnnai is not attested.
   Same shape of hold as ktii.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

FIX = {
    # he wrote both spellings himself: "muda bqxos (bqlos)"; bqlos>bqrus is tier A
    "bqxos": "bqrus",        # WAS green 2x;  bqrus 屍體 spk 11, tnbqrus 墳墓的主人
    # his tag (ñilao) on the NILAQ card; nilao>ngiraw is tier M
    "\u00f1ilao": "ngiraw",  # WAS green;  ngiraw 香菇 spk 6
    # his tag (var. KAOBU) on the KOOBU card; koobu>kowbu is tier M
    "kaobu": "kowbu",        # WAS green;  his own variant, in his own words
    # his tag (PG'DGIT) on the PGDGIT card; the id claim is attested and now checked
    "pg'dgit": "pgdgit",     # WAS green;  pgdgit 咬牙切齒生氣狀 spk 2, dgit 磨牙聲
    # his card: 似乎確是 K'LA 的異常變體 ... 參見 K'LA; and "Ini kila (k'la) kmpax"
    "kil\u00e2": "kla",      # WAS green;  kla 知道 spk 297, mkla 知道 spk 671
    "kila": "kla",           # WAS kila (id) -- attested, but glossed 適應, not 知道
}

LEXNULL = {}

NOTES = {
    "_never_swept_fields": (
        "TAG, PARADIGM AND CROSSREF WERE NEVER TOKENISED -- found in batch 73, after "
        "seventy-two batches. entries.js entries carry hw, tag, fr, en, zh, examples, "
        "subs, paradigm, crossRef, and subs carry form, fr, en, zh, examples, "
        "paradigm, crossRef. Every sweep this review has built walks hw, examples, "
        "subs and sub-examples. It walks four of the nine. The missing fields hold "
        "104 green types across 874 occurrences: mostly the metadata labels the app "
        "greys anyway (name 270, emprunt 121, jap 121, chin 121, plant 67, animal 64) "
        "and French prose, but underneath that his VARIANT SPELLINGS -- the "
        "parenthesised second form he prints beside a headword, (BQXOS), (ñilao), "
        "(var. KAOBU), (PG'DGIT), (KILâ) -- his full inflection PARADIGMS, and his "
        "cross-reference targets. Five of batch 73's six came from tag alone. The "
        "gap was visible the whole time as a discrepancy between the DOM census (223 "
        "green types) and the entries.js sweeps (203) and was written off as tag/"
        "paradigm noise instead of being opened. Measure the instrument, not just "
        "the thing: a sweep that silently covers 4/9 of the data reports zero "
        "candidates for the other five and looks exactly like a sweep that found "
        "nothing."
    ),
    "_display_is_not_a_token": (
        "THE CENSUS REPORTS OUTPUT, NOT INPUT -- and that has been quietly wasting "
        "effort. Green words reach the screen through charRules (x>h, o>u, l>r, "
        "word-final -ao>-aw, marks and diacritics stripped), so what the census "
        "lists is what the FALLBACK printed, not what Pecoraro wrote. srhqun, rngut, "
        "hru, musa, qtqut and bqhus are not tokens in his dictionary and cannot be "
        "looked up in it. Every one has to be traced back through the rules before "
        "it can be checked, and reconcile.py now does that -- walking all nine "
        "fields, applying the fallback, and grouping by what lands on screen, which "
        "is the first worklist in this review that matches what the reader sees. "
        "Related: charhit.py asks whether the fallback's output is ITSELF an "
        "attested modern word, which would mean the guess is already right and only "
        "the verification is missing. Over the entries.js greens that is true of "
        "only 2, so the fallback is not accidentally correct at any scale -- but the "
        "question had never been asked."
    ),
    "_kila_attested_wrong_word": (
        "KILA>kla 知道 spk 297 -- batch 73, and the sharpest instance yet of a trap "
        "this review keeps meeting from new directions. kila was brown on tier id, "
        "mapped to itself, and the string kila IS attested in modern Truku: it is "
        "the root of smkila 適應 and sklaan 適應的地方. Attested, and the wrong word. "
        "His card leaves no room -- 知道。(註:此詞有時以這種雙音節形式 KILA 出現,似乎"
        "確是 K'LA 的異常變體...)。在絕大多數情況下,幾乎所有發音人都以 K'LA 的形式使"
        "用這個表「知道」的詞。參見 K'LA -- and he writes the answer inside his own "
        "example: Ini kila (k'la) kmpax ka lisao. One batch earlier knmlaan showed "
        "the same fault with the shape-NEAREST word (kmalu, 正在梳, a comb). Here it "
        "is the shape-IDENTICAL word. So attestation alone never licenses a value, "
        "in either direction: the gloss decides, and an identity mapping is a claim "
        "that must clear the same bar as any other."
    ),
    "_rqbux_suspect": (
        "LQBUX>rqbux IS SUSPECT -- surfaced in batch 73 while checking his L'QBUÇ "
        "variant, and left unshipped rather than propagated. His card is 穿山甲, "
        "pangolin. rqbux is attested, which is presumably why it shipped on tier B, "
        "but it is glossed 不按部就班做工;不踏實地做事 -- doing work carelessly. The "
        "modern word for 穿山甲 is arung spk 17, and arung is unreachable from his "
        "spelling by any rule in the derived table. So this is the attested-string-"
        "wrong-meaning trap, the same one kila fell into, and matching l'qbuç to it "
        "would have put the error on a second key. Queued for the tier-B audit "
        "alongside malun>malun (batch 72) and the srhuq- paradigm below."
    ),
    "_srhuq_paradigm": (
        "THE SL'XEQ 舔 PARADIGM, held in batch 73 and flagged for the tier-B audit. "
        "His slxoqe>srhuqi, slxoqan>srhuqan, slxoqon>srhuqun are tier B; sl'xqe, "
        "sl'xqan and sl'xqon are the same three paradigm slots under his elision-"
        "mark spelling instead of his o spelling, and sit green beside them. "
        "Normally his own key deciding the same word under his other spelling is "
        "enough to ship -- it is what carried smoa, mpaaso, bqxos and kaobu. Held "
        "here because none of srhuqi, srhuqan, srhuqun is attested anywhere, so "
        "shipping would extend an unverified projection across three more keys "
        "instead of resolving anything, and because sl'xeq itself ships shik 吻 on "
        "tier X, which is a large shape change and does not obviously belong to the "
        "same word. The one-spelling-brown-one-spelling-green inconsistency is real "
        "and should be settled by auditing the B values, not by copying them."
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
