# -*- coding: utf-8 -*-
"""Can the modern lexicon confirm an AFFIX?

Twelve of his cards are headed by a single letter -- A, D, G, I, K, M, N(1),
N(2), O, P, S, T -- and they are not word entries at all. They are his short
grammars of the particles and the productive affixes, and D, G, M, N, P and S
render PALE while A, I, K, O and T render dark. The split is not a judgement
anyone made: the dark five happen to occur as standalone tokens somewhere in a
modern source, and no lexicon has a headword `p`.

The claim on those cards is `p -> p`: an identity, written by hand into
WORD_OVERRIDES. So the pale wash is expressing doubt about a respelling that
does not exist, and expressing it inconsistently across twelve sibling cards.

An affix cannot be LISTED, but it can be confirmed the way an affix exists: as a
productive process over words that are listed. This measures exactly that -- how
many attested modern types are (this letter) + (another attested modern type) --
and checks that the test discriminates, by running it on letters that are not
affixes in his account.
"""
import io, json, os, sys, collections
sys.stdout.reconfigure(encoding="utf-8")

ORTH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
att = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"),
                            encoding="utf-8")))
gloss = json.load(io.open(os.path.join(ORTH, "attested_gloss.json"),
                          encoding="utf-8"))

# His own affix cards, and controls: letters that head no affix entry.
HIS = list("dgmnpst") + list("ak")
CONTROL = list("bcefhijoruvwxyz") + ["q", "l"]


def productive(ch):
    """Attested types of the form ch + stem where the stem is itself attested."""
    hits = [w for w in att
            if len(w) > len(ch) and w.startswith(ch) and w[len(ch):] in att]
    return hits


rows = []
for ch in sorted(set(HIS + CONTROL)):
    h = productive(ch)
    rows.append((len(h), ch, ch in HIS, sorted(h)[:4]))

rows.sort(reverse=True)
print("%-4s %-6s %8s   %s" % ("ch", "his?", "derived", "examples"))
for n, ch, his, ex in rows:
    print("%-4s %-6s %8d   %s" % (ch, "AFFIX" if his else "-", n, ", ".join(ex)))

print()
print("his affix letters, lowest first:")
mine = sorted((n, ch) for n, ch, his, _ in rows if his)
for n, ch in mine:
    print("   %-3s %6d" % (ch, n))
ctrl = sorted((n, ch) for n, ch, his, _ in rows if not his)
print("controls, highest first:")
for n, ch in reversed(ctrl[-6:]):
    print("   %-3s %6d" % (ch, n))
