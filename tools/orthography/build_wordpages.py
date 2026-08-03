# -*- coding: utf-8 -*-
"""site/wordpages.js — a page for the words he only ever used in a sentence.

THE GAP. `FORMS` indexes headwords and sub-forms; `SLOTS` adds the tokens he
printed on a ° line. A word that appears ONLY inside an example sentence is in
neither, so it renders on screen — dark, respelled, read by anybody using the
book — and leads nowhere. Measured from the DOM (`reach.py`): 1,835 dark
occurrences over 1,002 types have no reachable page, and 988 of those types are
in this state.

WHAT A GENERATED PAGE MAY CLAIM. A slot card can name the morphology because his
° line is positional; this one has no line to read. So the tokens are split by
how much assertion a card would have to make, and only the two groups that make
none are emitted:

  group 1 — `Inflection.roots()` finds exactly ONE candidate root and that root
            is already dark. The card links to it and names nothing else. No new
            claim: the root is claimed already, on its own page.
  group 3 — `roots()` finds nothing. The card carries the concordance and says
            so. A list of the sentences a word occurs in is not an assertion
            about its morphology.
  group 2 — two or more candidate roots, or a single one that is not dark.
            Choosing between `psapuh` and `sapuh` for `spsapox` is an
            adjudication, and an adjudication is not something a generator does.
            **Omitted entirely**, and app.js builds a page only for keys this
            file emits, so silence here is a refusal there.

The file is a TABLE, not a renderer. `""` means group 3; a non-empty value is the
modern spelling of the group-1 root. Reachability is re-tested at runtime by
app.js against `lookupWord()` and `slotByKey()`, which know about bracketed
aliases and variants this script does not — so over-generating here is harmless
and under-generating is not.
"""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
H = os.path.dirname(os.path.dirname(HERE))
H = os.path.join(H, "taroko-pecoraro") if not os.path.exists(
    os.path.join(H, "site")) else H
SITE = os.path.join(H, "site")
sys.path.insert(0, HERE)
from inflection import Inflection

TOKEN = re.compile(u"[A-Za-zÀ-ÿłŁʔ'’ʼ\"]+")
LETTER = re.compile(u"[A-Za-zÀ-ÿłŁ]")


def read(p):
    return io.open(p, encoding="utf-8").read()


def word_key(w):
    """app.js wordKey(), character for character."""
    return re.sub(u"[’ʼ\"ʔ]", "'", (w or "").lower()).replace(
        u"ł", "l")


def keys(text):
    out = []
    for m in TOKEN.finditer(text or ""):
        k = word_key(m.group(0))
        if len(k) >= 2 and LETTER.search(k):
            out.append(k)
    return out


def main():
    src = read(os.path.join(SITE, "entries.js"))
    E = json.loads(re.sub(r",(\s*[}\]])", r"\1",
                          src[src.index("["):src.rindex(";")]))
    m = read(os.path.join(SITE, "modern_map.js"))
    a = m.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
    mp = json.loads(m[a:m.index("\n};", a) + 2])
    v = read(os.path.join(SITE, "verified.js"))
    b = v.index("window.MODERN_VERIFIED = {") + len("window.MODERN_VERIFIED = ")
    dark = set(json.loads(re.sub(r",(\s*})", r"\1",
                                 v[b:v.index("\n};", b) + 2])))
    lex = set(json.load(io.open(os.path.join(HERE, "attested_modern.json"),
                                encoding="utf-8")))
    app = read(os.path.join(SITE, "app.js"))
    ob = app.index("WORD_OVERRIDES")
    ov = dict(re.findall(r"['\"]([^'\"]+)['\"]\s*:\s*['\"]([^'\"]+)['\"]",
                         app[ob:app.index("}", ob)]))
    inf = Inflection(lex, mp)

    # Everything the two existing indexes already claim. A ° cell counts even
    # when SLOTS refused it for ambiguity: two entries printing one token is a
    # conflict, and a generated page is the last place to guess.
    indexed, used = set(), collections.Counter()
    for e in E:
        indexed |= set(keys(e.get("hw"))) | set(keys(e.get("paradigm")))
        for x in e.get("examples") or []:
            used.update(keys(x.get("t")))
        for s in e.get("subs") or []:
            indexed |= set(keys(s.get("form"))) | set(keys(s.get("paradigm")))
            for x in s.get("examples") or []:
                used.update(keys(x.get("t")))

    def modern(t):
        x = ov.get(t, mp.get(t))
        if isinstance(x, dict):
            x = x.get("modern")
        return (x or t).strip().lower()

    out, counts = {}, collections.Counter()
    for t in sorted(set(used) - indexed):
        cands = sorted({c for c, _, _, _ in inf.roots(modern(t))})
        if not cands:
            out[t] = ""                       # group 3
            counts["3 concordance only"] += 1
        elif len(cands) == 1 and cands[0] in dark:
            out[t] = cands[0]                 # group 1
            counts["1 one dark root"] += 1
        else:
            counts["2 REFUSED (needs adjudication)"] += 1

    for k in sorted(counts):
        print("  %-34s %4d types" % (k, counts[k]))
    print("  emitted: %d of %d example-only types"
          % (len(out), len(set(used) - indexed)))

    f = io.open(os.path.join(SITE, "wordpages.js"), "w",
                encoding="utf-8", newline="\n")
    f.write(
        u"// Generated by tools/orthography/build_wordpages.py "
        u"— do not edit by hand.\n"
        u"// A page for the %d words he only ever used in a sentence: %d whose\n"
        u"// single candidate root is ALREADY dark (the value is that root), and\n"
        u"// %d that no affix analysis reaches at all (the value is empty, and\n"
        u"// the card carries only the concordance). Types needing an\n"
        u"// adjudication to choose a root are not here — app.js builds a page\n"
        u"// only for a key this file emits.\n"
        % (len(out), counts["1 one dark root"], counts["3 concordance only"]))
    f.write(u"window.WORD_PAGES = {\n")
    for k in sorted(out):
        f.write(u'  "%s": "%s",\n' % (k.replace('"', '\\"'), out[k]))
    f.write(u"};\n")
    f.close()
    print("wrote site/wordpages.js")


if __name__ == "__main__":
    main()
