# -*- coding: utf-8 -*-
"""Emit site/verified.js — which brown claims the modern dictionary confirms.

Brown used to mean one thing: a curated table holds a key for this word. That
is a statement about our tables, not about Truku, and it counted a value like
`nxa` — which still had an x in it, a letter modern Truku does not have — as
verified. This splits brown in two.

A modern value is VERIFIED two ways, and the file records which.

  1  LISTED. The exact string is one of the 40,760 types in
     attested_modern.json: every plain [a-z'] type of the modern Truku
     dictionary and the spoken-word list, PLUS every token of the 26,663 modern
     corpus sentences. The sentences matter -- the particle `o` is in 6,361 of
     them and in no headword list, so a headword-only snapshot called 517
     occurrences of it unverified.

     Widened here by parquet_truku_freq.json (build_parquet_attested.py), which
     reads the ILRDF datasets directly instead of through the xlsx export the
     spoken-word list was built from -- the export dropped a third of the text,
     361,630 tokens down to 272,150. Admitted at **frequency >= 2**: these are
     ASR transcripts, so a single hit is as likely to be a mis-hearing as a
     word, which is the same reason load_spoken() keeps counts at all. Taking
     hapax too would clear 109 more pale page occurrences on the strength of one
     transcriber's ear apiece (`tatu`, `murisaka`, `lqlqian`), and that is not
     what brown promises.

     The class this reaches is the one a wordlist has no reason to hold:
     personal names. `Sibal` is the biggest pale word on the page at 47
     occurrences and the xlsx has him nowhere, while the parquets write him
     `Awi Sibal` and `Sibal Watan` -- with the l that tier N froze against the
     l>r rule. Tier N's whole premise, confirmed from outside the book.

  2  A REGULAR INFLECTION of a listed root, per inflection.py: AF, PF, LF, the
     referential s-, the causative p-, the preterite -n-, the imperatives, and
     the stacks those build, with the root's modern gloss required to agree
     with his own Chinese for the word. The wordlist records the forms someone
     happened to write down, not every form of every word -- `qriban` is absent
     while its own siblings `qribun` 剪成 and `qribi` 要剪下 are there. That is a
     listing gap, and painting it as unverified told the reader the wrong
     thing.

Everything else is UNVERIFIED: a curated table proposed the word and no modern
source has it, nor is it a paradigm slot of anything that does. The reader is
entitled to know which of the three is on screen; app.js paints 1 and 2 alike
in the deep brown and leaves the rest pale.

A multi-word value is verified only if every word in it is, and at the weaker
of the two levels.

Run from tools/orthography/ after build_modern_map.py.
"""
import io, json, os, re
from inflection import Inflection

H = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
H = os.path.normpath(H)
SITE = os.path.join(H, "site")
PAIR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')
PQ_MIN = 2      # ASR hapax is as likely a mis-hearing as a word; see the docstring


def read(p):
    return io.open(p, encoding="utf-8").read()


def table(app, name):
    i = app.index("var %s = {" % name)
    return dict(PAIR.findall(app[i:app.index("\n  };", i)]))


def main():
    HERE = os.path.dirname(os.path.abspath(__file__))
    lex = set(json.load(io.open(os.path.join(HERE, "attested_modern.json"),
                                encoding="utf-8")))
    # The parquet corpus answers ONE question — does this exact string occur in
    # real modern Truku? — and it is not allowed to answer the other one, what
    # the roots of the language are. Handing it to Inflection as a root
    # inventory is what a raw ASR transcript is least fit for: it put `san` (65),
    # `sang` (5) and `ngay` (2) in as lexemes, and the analyser promptly re-cut
    # `spsangay` off 休息 `sangay` onto `sang`, where no gloss could agree — a
    # word that was verified before this batch came out of it unverified. Adding
    # evidence must never subtract a claim. So `seen` widens and `lex` does not.
    seen = set(lex)
    pqf = os.path.join(HERE, "parquet_truku_freq.json")
    if os.path.exists(pqf):
        pq = json.load(io.open(pqf, encoding="utf-8"))
        seen |= {w for w, c in pq.items() if c >= PQ_MIN}
        print("attested: %d listed + %d from the ILRDF parquets at freq>=%d"
              % (len(lex), len(seen) - len(lex), PQ_MIN))
    app = read(os.path.join(SITE, "app.js"))
    ov, cl = table(app, "WORD_OVERRIDES"), table(app, "CLITIC_FORMS")
    m = read(os.path.join(SITE, "modern_map.js"))
    a = m.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
    mp = json.loads(m[a:m.index("\n};", a) + 2])

    # Every value a brown span can display. CLITIC_FORMS hands the word back
    # unchanged, so there the key IS the value.
    vals = set(ov.values()) | set(mp.values()) | set(cl)

    inf = Inflection(lex, mp)

    def word(p):
        """2 listed, 1 regularly inflected, 0.5 vouched by its own paradigm,
        0.25 a regular inflection of a root vouched that way, 0.125 a slot the
        wordlist writes with two other suffixes, 0.0625 an inflection of a
        listed root that syncopates its own first vowel, 0.03125 an inflection
        of a root that is itself one step from a glossed one."""
        if p in seen:
            return 2
        if inf.regular(p):
            return 1
        if inf.vouched(p):
            return 0.5
        if inf.vouched_root(p):
            return 0.25
        if inf.sistered(p):
            return 0.125
        if inf.syncopated(p):
            return 0.0625
        if inf.chained(p):
            return 0.03125
        return 0

    def level(v):
        parts = v.split()
        if not parts:
            return 0
        w = [word(p) for p in parts]
        return min(w) if all(w) else 0

    # app.js's attested() splits a value on its spaces and asks about each word
    # separately, so a multi-word value has to put its own words in here too or
    # it can never be verified. One value has a space in it (`empaa su`, a
    # proclitic join), and `empaa` was reaching the page pale for want of a key.
    keys = set(vals)
    for v in vals:
        keys |= set(v.split())

    lv = {v: level(v) for v in keys}
    listed = sorted(v for v in keys if lv[v] == 2)
    infl = sorted(v for v in keys if lv[v] == 1)
    vouch = sorted(v for v in keys if lv[v] == 0.5)
    vroot = sorted(v for v in keys if lv[v] == 0.25)
    sistr = sorted(v for v in keys if lv[v] == 0.125)
    syncp = sorted(v for v in keys if lv[v] == 0.0625)
    chain = sorted(v for v in keys if lv[v] == 0.03125)
    good = sorted(listed + infl + vouch + vroot + sistr + syncp + chain)
    emit = {2: 1, 1: 2, 0.5: 3, 0.25: 4, 0.125: 5, 0.0625: 6, 0.03125: 7}

    out = io.open(os.path.join(SITE, "verified.js"), "w",
                  encoding="utf-8", newline="\n")
    out.write(
        "// Generated by tools/orthography/build_verified.py — do not edit by hand.\n"
        "// The modern spellings a modern source vouches for: %d of the %d distinct\n"
        "// values the curated tables can put on screen. 1 = a modern source lists\n"
        "// this exact word (%d). 2 = the wordlist does not list it, but it is a\n"
        "// regular inflection of a root the wordlist does list, and that root means\n"
        "// what he says the word means (%d) — a listing gap, not a lexical one.\n"
        "// 3 = the wordlist does not list it BARE, but it lists two or more of its\n"
        "// own inflections and one of them means what he says it means (%d) — a\n"
        "// citation form nobody wrote down, which is the same listing gap seen\n"
        "// from the other side.\n"
        "// 4 = 2 over 3: a regular inflection of a root the wordlist only vouches\n"
        "// for through ITS own inflections (%d). Neither the word nor its root is\n"
        "// listed, so the gloss agreement is taken against the root's attested\n"
        "// supporter and only against Chinese he attached to the word as a word.\n"
        "// 5 = a SISTER SLOT: the wordlist writes this same stem with two OTHER\n"
        "// paradigm suffixes and not with this one (%d). Most of a paradigm is\n"
        "// glossless, so 2, 3 and 4 cannot reach these — the claim is about\n"
        "// morphology rather than meaning, and the gate is his: the word must be\n"
        "// one he printed in a ° paradigm line, which is his own statement that it\n"
        "// is an inflectional slot and not a word in its own right.\n"
        "// 6 = 2 with the root's OWN first vowel syncopated (%d). Truku writes no\n"
        "// schwa, so a root loses that vowel under affixation — GAMIL 根 but\n"
        "// `Tgmilan` — and rule 2 can only ever delete a vowel at the end. Since\n"
        "// this inserts a letter he did not write, the gloss must be one he\n"
        "// attached to the word as a word, never an example sentence.\n"
        "// 7 = 2 over a root that is itself one step from a glossed root (%d):\n"
        "// the CV- reduplication that makes no new lexeme (`qqgu` on `qgu`), or a\n"
        "// second round of ordinary affixation (`swiwil` on `wiwil`). Rules 2-6\n"
        "// stop at the first listed root and ask its gloss, and most of a paradigm\n"
        "// is glossless. Two steps of inference, so the same slot-gloss gate as 4\n"
        "// and 6 — which here refuses every illicit spelling the rule would find.\n"
        "// app.js paints all seven in the deep brown; a value NOT in here is still\n"
        "// a proposal and stays pale.\n"
        "window.MODERN_VERIFIED = {\n"
        % (len(good), len(keys), len(listed), len(infl), len(vouch), len(vroot),
           len(sistr), len(syncp), len(chain)))
    for v in good:
        out.write('  "%s": %d,\n' % (v, emit[lv[v]]))
    out.write("};\n")
    out.close()
    print("listed: %d   regularly inflected: %d   vouched by its paradigm: %d   "
          "inflected off a vouched root: %d   sister slot: %d   syncopated root: "
          "%d   chained root: %d   unverified: %d   (of %d distinct)"
          % (len(listed), len(infl), len(vouch), len(vroot), len(sistr),
             len(syncp), len(chain), len(keys) - len(good), len(keys)))
    print("wrote site/verified.js")


if __name__ == "__main__":
    main()
