"""Batch 74: withdraw three keys, and correct a note that was wrong.

TWO CORRECTIONS OF MY OWN WORK, both from the same reading session.

1. The variant-spelling policy, decided: his parenthesised second spellings --
   (var. KAOBU), (PG'DGIT), (KILâ), (BQXOS), (ñilao) -- belong to the 1977
   typescript, not to the modernized text. Modern Truku has one standard
   spelling per word, so there is nothing for a 1977 variant to be modernized
   INTO; asserting kaobu>kowbu invents a modern variant that does not exist.
   Batch 73 shipped five of these. Three of them (kaobu, pg'dgit, kilâ) live
   only in tags with no root mark, which tagHtml renders as prose, so they never
   reached respellable() and were inert -- but an inert key is still a claim in
   the map, and it is the wrong claim. Withdrawn.

   The rule that falls out, and it is the right one to keep: A KEY FOR ANYTHING
   THAT RENDERS, NO KEY FOR ANYTHING THAT DOES NOT. bqxos KEEPS its key, because
   it is not only a tag -- it stands in a running sentence (Mngongo ko bi muda
   bqxos (bqlos) ka'man), where it is ordinary Truku text and must be modernized
   like any other word. ñilao keeps its key because its tag carries a root mark
   and therefore does render; without a key it would show as green niraw, a
   false alarm about a word we have in fact identified. So the two that reach
   the reader keep their values and the three that do not are withdrawn.

   The residual inconsistency is recorded rather than fixed: the tag gate keys
   on an incidental (R). (BQXOS) (R) and (ñilao) (R) are modernized; (var.
   KAOBU) and (PG'DGIT) are greyed. Same kind of content, different treatment,
   by accident of whether he happened to type the root mark. Fixing it properly
   means deciding whether root-marked variant tags should also grey, which
   changes what the page looks like, so it stays a flagged decision.

2. LQBUX>rqbux IS NOT SUSPECT. My batch 73 note said rqbux "is not a pangolin,
   it is doing work carelessly" and queued the value for withdrawal. That was
   wrong, and wrong because I stopped reading at the first gloss. The modern
   dictionary also has tmrqbux 專獵果子狸 -- to hunt rqbux. A tm- form meaning
   "specializes in hunting X" only exists where X is game, so rqbux IS a wild
   animal and the 不按部就班做工／不踏實地做事 senses are the derived figurative
   ones that happened to sort first. The value stands.

   What remains is a species discrepancy, not a spelling error: his card says
   穿山甲 (pangolin, which the modern dictionary calls arung spk 17) and the
   modern gloss behind rqbux is 果子狸 (masked palm civet). That is a folk-
   taxonomy identification wobble of exactly the kind a 1970s field dictionary
   is full of, and it is a note for the entry, not a reason to touch the map.
"""
import json, io, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

WITHDRAW = ["kaobu", "pg'dgit", "kil\u00e2"]

NOTES = {
    "_variant_spellings_stay_1977": (
        "VARIANT SPELLINGS BELONG TO THE 1977 TEXT, NOT THE MODERNIZED ONE -- policy "
        "decided in batch 74, and three keys withdrawn to match. Pecoraro prints a "
        "second spelling in parentheses beside many headwords: (var. KAOBU), "
        "(PG'DGIT), (KILâ), (BQXOS), (ñilao). These are artefacts of his ear and his "
        "typewriter in 1977. Modern Truku has ONE standard spelling per word, so "
        "there is nothing for a variant to be modernized into -- a key saying "
        "kaobu>kowbu asserts a modern variant that does not exist. The operative "
        "rule is now: A KEY FOR ANYTHING THAT RENDERS, NO KEY FOR ANYTHING THAT DOES "
        "NOT. kaobu, pg'dgit and kilâ live only in tags without a root mark, which "
        "tagHtml renders as prose, so they never reached respellable() and were "
        "inert -- withdrawn, because an inert key is still a claim and it is the "
        "wrong one. bqxos KEEPS its key: it also stands in a running sentence "
        "(Mngongo ko bi muda bqxos (bqlos) ka'man) where it is ordinary Truku and "
        "must be modernized. ñilao keeps its key: its tag carries a root mark and "
        "does render, so without a value it would show as a green niraw, a false "
        "alarm about a word we have identified. FLAGGED, not fixed: the tag gate "
        "keys on an incidental (R), so (BQXOS) (R) and (ñilao) (R) are modernized "
        "while (var. KAOBU) and (PG'DGIT) are greyed -- same content, different "
        "treatment, by accident of whether he typed the root mark. Settling it "
        "changes what the page looks like and is left as a decision."
    ),
    "_rqbux_not_suspect": (
        "LQBUX>rqbux STANDS -- this REPLACES the batch 73 note _rqbux_suspect, which "
        "was wrong. I wrote that rqbux 'is not a pangolin, it is doing work "
        "carelessly' and queued the tier-B value for withdrawal. The error was "
        "stopping at the first gloss. The modern dictionary also carries tmrqbux "
        "專獵果子狸 -- to hunt rqbux -- and a tm- form meaning 'specializes in hunting "
        "X' only exists where X is game. So rqbux IS a wild animal and the "
        "不按部就班做工;不踏實地做事 senses are derived figurative ones that merely "
        "sorted first in my output. What is left is a SPECIES discrepancy, not a "
        "spelling error: his card says 穿山甲, pangolin, which modern Truku calls "
        "arung spk 17, while the animal behind rqbux is 果子狸, masked palm civet. "
        "That is folk-taxonomy drift of the kind a 1970s field dictionary is full "
        "of, and it belongs in a note on the entry, not in the orthography map. "
        "General lesson, and the second time in two batches: a word's first gloss "
        "is not its meaning. kila looked right because its string was attested; "
        "rqbux looked wrong because its first gloss was figurative. Read the whole "
        "family -- especially the tm-, em- and -an derivatives, which disambiguate "
        "a root faster than any number of direct glosses."
    ),
}

lex = json.load(io.open(H + "lexical_map.json", encoding="utf-8"))
# the batch 73 note this supersedes -- replaced in place so the file has one story
lex.pop("_rqbux_suspect", None)
lex.update(NOTES)
json.dump(lex, io.open(H + "lexical_map.json", "w", encoding="utf-8", newline="\n"),
          ensure_ascii=False, indent=1)
print("lexical_map: %d notes written, 1 superseded note removed (%d keys)"
      % (len(NOTES), len(lex)))

p = H + "manual_map.json"
d = json.load(io.open(p, encoding="utf-8"))
before = len(d)
for k in WITHDRAW:
    if k in d:
        print("   withdrawing %-10s (was %s)" % (k, d[k]))
        d.pop(k)
    else:
        print("   !! %s not present" % k)
body = ",".join("%s:%s" % (json.dumps(k, ensure_ascii=False),
                           json.dumps(v, ensure_ascii=False))
                for k, v in sorted(d.items()))
io.open(p, "w", encoding="utf-8", newline="\n").write("{\n" + body + "\n}\n")
print("manual_map %d -> %d" % (before, len(d)))
