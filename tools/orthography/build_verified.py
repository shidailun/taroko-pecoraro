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

     Widened a second time by ilrdf_names.json, and this one is aimed at that
     class rather than reaching it by luck: the Council of Indigenous Peoples'
     name registry (indigenous-name.ilrdf.org.tw), 1,792 Truku names, each with
     its 男名/女名/男女共名 type and a recording. A transcript mentions the
     people who happened to be talked about; the registry is the list. It is
     what tier N never had -- the tier exists precisely because "nothing attests
     a name and no tier above reaches it", so every name it froze stayed pale
     forever, and pale is not a verdict a person's name can ever shed.

     GATED TO THE NAME POPULATION (name_population.json), and the gate is the
     whole of the care here. The registry answers "is this string a Truku
     name?", not "is this string the modern spelling of his word", and those
     part company the moment a name is homographic with a word: `aku`, `aman`,
     `mici`, `taya`, `urang`, `tabu` are all somebody's name AND ordinary
     vocabulary, and verifying the common noun on the strength of the person
     would be the raki/laqi trap with a new source. Ungated the registry clears
     82 pale types; gated it clears 67, and the 15 it drops are exactly that
     homograph class. So a value is admitted here only when the token it came
     from is one his own `name (m)`/`name (f)` tag declares, or one the tier-N
     capitalisation test admitted -- i.e. only where the claim being made about
     the string IS "this is how the name is written".

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
from inflection import HAND_NAMES, HAND_NOT_NAMES, HAND_SPOKEN, Inflection

H = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
H = os.path.normpath(H)
SITE = os.path.join(H, "site")
PAIR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*"((?:[^"\\]|\\.)*)"')
PQ_MIN = 2      # ASR hapax is as likely a mis-hearing as a word; see the docstring

# The hapaxes read one at a time and let through anyway (batch 162).
#
# PQ_MIN throws away every type the parquets saw exactly once, and for the bulk
# case that is right. But it throws them away UNREAD, and 15 of them are words
# on this page — which means each already has a second witness: Pecoraro typed
# it in 1977. **That coincidence is the evidence.** A 2020s acoustic model
# mis-hearing a word cannot land on a string a French priest typed fifty years
# earlier by accident; the two witnesses have no path to each other. So the
# hapax gate is not loosened, it is ANSWERED, per word, by a second source that
# was always sitting there.
#
# The coincidence argument has one failure mode and it is length: at three or
# four letters chance can reach a real string. So the short ones are refused
# even where the sense fits, and `rih` is the case that proves the rule is
# costing something real — 6 occurrences, the largest single gain left on the
# page, and his 幾乎－接近－有點像 fits the parquet's `qhuqil kana rih saw
# psahug dhyaan` ("killed them all, almost as a punishment to them") rather
# well. It stays pale. Batch 146 pinned it because a three-letter root needs
# his word-level Chinese and not a sentence gloss, and batch 159 showed the
# honest way out: `nta` was the fourth pinned member and went dark because **a
# person spoke for it**, not because a gate moved. One ASR token is not a
# person. `kn` is refused twice over — two letters, and its single occurrence
# is inside `Fu-kn-su`, the romanized Japanese 撫墾署 split on its hyphens.
#
# Like every corpus source here this widens `seen` and never `lex`, and like
# every corpus source it vouches for a SPELLING and not for his gloss:
# `brnahan` is admitted as modern Truku orthography while his 後退 reading of
# it stays his own business.
PARQUET_HAPAX = {
    "mlilug",    # 起義軍佔領霧社 ~ his Mlilu 移動－活動 (LILU)
    "tntmaan",   # kari muda matas tntmaan ta seuxal 口傳/經文 ~ his Tntmaan (TTAMA)
    "brnahan",   # brnahan smalu kari paah isil 其他的創作 ~ his Blnaxan (BLENAX)
    "mskrut",    # duma mskrut ni duma mslhkah 時鬆時緊 — paired against mslhkah
    "pnlwaan",   # pnyahan seejiq o pnlwaan 呼喚而出 ~ his "tu m'as fait appeler"
    "pniq",      # pniq kingal qpuring mrata 駐紮 ~ his Pnyeq 使留下－使存在
    "ppkmalu",   # 醫病趕鬼 ~ his "te remettre la tete en place"
    "mknsat",    # 派出所上班 ~ his Mkensat 當警察 (a Japanese loan, no homograph)
    "dnrunan",   # 老師交代的功課 ~ his "ce qu'ils ont demande"
    "pgmaxun",   # 族語融合 ~ his "melanger du sucre a cette farine"
    "pkhwayun",  # 優待入山工作人員 ~ his Pkxwayun
    "mnlamu",    # plealay strung mnlamu ~ his "autrefois je recueillais l'argent"
    "emptaril",  # 準備登陸攻擊 ~ his Ptaril 使越到對岸 (TALIL)
}
AFFIX_MIN = 400   # see affix(); his six affix letters score 453-3,223, best non-affix 347


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
        # The adjudicated hapaxes. Asserted, not trusted: if a later parquet
        # rebuild lifts one of these to freq>=2 it is already in and the entry
        # is dead weight, and if one vanishes the corpus no longer says it.
        hx = {w for w in PARQUET_HAPAX if pq.get(w, 0) == 1}
        assert hx == PARQUET_HAPAX, (
            "PARQUET_HAPAX out of step with the corpus: %s"
            % sorted(PARQUET_HAPAX ^ hx))
        seen |= hx
        print("  + %d hapaxes read one at a time (see PARQUET_HAPAX)" % len(hx))

    # THE TRUKU BIBLE — 175,260 tokens of published modern Truku prose, the
    # largest body of it that exists. It enters on exactly the parquets' terms
    # and for the opposite reason. The parquets are gated at freq>=2 because an
    # ASR hapax is as likely a mis-hearing as a word; the Bible is EDITED and
    # TYPESET, so a hapax in it is a spelling somebody stood behind. But it is
    # still a text and not a wordlist, so it widens `seen` and never `lex` —
    # nothing here becomes a root the analyser may cut a word onto.
    #
    # Its glossary is separate and does the same job: 2,035 headwords with
    # Chinese, 425 of them the modern wordlist has never listed.
    #
    # **What was refused alongside it.** The Kaldi decoder lexicon at
    # C:/dev/ILRDF/kaldi_formosan_250514_Truku/graph/words.txt is 13,351 types
    # and 2,040 of them are new here — and 1,918 of those 2,040 do not occur in
    # the parquets at all, because it was built from a dirtier transcript set
    # than the cleaned datasets. Its new types are `alagn`, `alnag` and `aalng`
    # for alang, and `amerika`/`amerrika`/`amrika` side by side. A decoding
    # inventory is not an attestation; it is required to hold every string the
    # acoustic model might emit. Admitting it would have listed `alagn` as
    # modern Truku for 25 pale words' worth of credit.
    for src, why in ((os.path.join(HERE, "bible_truku_freq.json"), "Truku Bible"),
                     (os.path.join(HERE, "bible_glossary.json"), "Bible glossary")):
        if not os.path.exists(src):
            continue
        d = json.load(io.open(src, encoding="utf-8"))
        add = set(d) - seen
        seen |= add
        print("  + %d types from the %s" % (len(add), why))
    # The informant. Printed on its own line, never folded into a source count,
    # because this is the one attestation on the page that is a person and not a
    # document — see HAND_SPOKEN in inflection.py.
    spoken = set(HAND_SPOKEN) - seen
    seen |= spoken
    print("  + %d types spoken for by the informant (not in any corpus): %s"
          % (len(spoken), " ".join(sorted(spoken))))
    app = read(os.path.join(SITE, "app.js"))
    ov, cl = table(app, "WORD_OVERRIDES"), table(app, "CLITIC_FORMS")
    m = read(os.path.join(SITE, "modern_map.js"))
    a = m.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
    mp = json.loads(m[a:m.index("\n};", a) + 2])

    # The NAME POPULATION — see the docstring. Like the parquets it widens
    # `seen` and never `lex`: a name is not a root, and handing names to the
    # affix analyser as lexemes is the same mistake that re-cut `spsangay` onto
    # `sang`.
    #
    # Batch 144 drops the `& reg` intersection that used to stand here, and the
    # registry now only REPORTS. The gate that matters is the population, and it
    # always was: `aku`, `taya`, `urang`, `tabu` are kept out because they are
    # not in the population, not because the registry refused them. Asking the
    # registry a second question — "and is this the modern spelling?" — is a
    # test three whole classes of name can never pass, because no register of
    # Truku given names will ever hold `denki` 電気, `banasi` 話, `stbaku` 煙草,
    # the place name `tagahan`, or `dcristu`. Their modern spelling comes from
    # the same o>u, x>h rules that spell every other word on this page, and the
    # claim being made about a population token IS "this is how the name is
    # written". HAND_NAMES joins it: those are names reached only through an
    # example sentence, so his tagger never saw them and tier N never fired.
    nf = os.path.join(HERE, "ilrdf_names.json")
    pf = os.path.join(HERE, "name_population.json")
    if os.path.exists(pf):
        pop = set(json.load(io.open(pf, encoding="utf-8")))
        named = {v for v in (mp.get(t) for t in pop) if v} | \
                {ov[t] for t in pop if t in ov}
        named = ({v.strip().lower() for v in named} | set(HAND_NAMES)) \
                - HAND_NOT_NAMES
        if os.path.exists(nf):
            R = json.load(io.open(nf, encoding="utf-8"))
            reg = {n.strip().lower() for s in R.values() for n in s}
            print("names: %d values from the %d-token name population + %d "
                  "hand-ruled; %d of them the ILRDF registry also lists"
                  % (len(named), len(pop), len(HAND_NAMES), len(named & reg)))
        seen |= named

    # The LOAN POPULATION — the same argument the name block makes two
    # paragraphs up, applied to the class that block already names. `denki`
    # 電気, `banasi` 話, `stbaku` 煙草 are cited there as names no register of
    # Truku given names can ever hold, and the answer given is that their modern
    # spelling comes from the same o>u, l>r, x>h rules that spell every other
    # word on the page. A Japanese or Chinese loan is in exactly that position:
    # no Truku wordlist will ever list `abura` 油 or `budosyu` 葡萄酒, so the
    # attestation test is not a test it can fail — it is a test it cannot sit.
    # Leaving it pale does not report doubt about the respelling; it reports the
    # absence of a source that was never going to exist.
    #
    # Gated to the population for the same reason names are: the claim being
    # made about a loan token IS "this is how the loan is written". Tier J is
    # the tagger's own verdict that the word came in from Japanese or Chinese,
    # so the population is the set of tokens that verdict covers, and nothing
    # widens `lex` — a loan is not a root, and must never reach the affix
    # analyser as one.
    lf = os.path.join(HERE, "loan_population.json")
    if os.path.exists(lf):
        loans = set(json.load(io.open(lf, encoding="utf-8")))
        loaned = {v for v in (mp.get(t) for t in loans) if v} | \
                 {ov[t] for t in loans if t in ov}
        loaned = {v.strip().lower() for v in loaned}
        print("loans: %d values from the %d-token loan population"
              % (len(loaned), len(loans)))
        seen |= loaned

    # Every value a brown span can display. CLITIC_FORMS hands the word back
    # unchanged, so there the key IS the value.
    vals = set(ov.values()) | set(mp.values()) | set(cl)

    inf = Inflection(lex, mp)

    def affix(p):
        """An AFFIX LETTER, confirmed the only way an affix can be.

        Twelve of his cards are headed by a single letter — A, D, G, I, K, M,
        N(1), N(2), O, P, S, T — and they are not word entries at all. They are
        his short grammars of the particles and of the productive affixes. Six of
        them rendered PALE while the other five rendered dark, and the split was
        nobody's judgement: `a`, `i`, `k`, `o` and `t` happen to occur as
        standalone tokens in a modern source, and no lexicon has a headword `p`.
        The claim on those cards is `p -> p`, a hand-written identity in
        WORD_OVERRIDES, so the pale wash was doubting a respelling that does not
        exist — and doubting it inconsistently across twelve sibling cards.

        An affix cannot be LISTED. It can be attested as a process over words
        that are: how many modern types are this letter plus another modern type.
        Measured (affix137.py), his six score 453 (`d`) to 3,223 (`s`), against
        347 for the best letter that heads no affix card of his (`q`), then 300
        `h`, 289 `b`. The identity gate is what actually selects — only the six
        reach this at all — and the threshold is a guard, so that a single-letter
        override added later cannot inherit the verdict for free.
        """
        if len(p) != 1 or ov.get(p) != p:
            return False
        return sum(1 for w in lex if len(w) > 1 and w[0] == p
                   and w[1:] in lex) >= AFFIX_MIN

    def word(p):
        """2 listed, 1 regularly inflected, 0.5 vouched by its own paradigm,
        0.375 a regular inflection of a LISTED root the wordlist never glossed,
        spoken for by that root's own paradigm, 0.34375 the same where the root
        IS glossed and the gloss disagrees, outvoted by two of the root's own
        inflections, 0.3125 a regular inflection of a
        listed and glossed root for which he wrote no Chinese at all, 0.25 a
        regular inflection of a
        root vouched by a paradigm, 0.125 a slot the wordlist writes with two
        other suffixes, 0.0625 an inflection of a listed root that syncopates
        its own first vowel, 0.03125 an inflection of a root that is itself one
        step from a glossed one, 0.015625 an affix letter."""
        if p in seen:
            return 2
        if inf.regular(p):
            return 1
        if inf.vouched(p):
            return 0.5
        if inf.unglossed_root(p):
            return 0.375
        if inf.outvoted(p):
            return 0.34375
        if inf.no_chinese(p):
            return 0.3125
        if inf.vouched_root(p):
            return 0.25
        if inf.sistered(p):
            return 0.125
        if inf.syncopated(p):
            return 0.0625
        if inf.awag(p):
            return 0.046875
        if inf.chained(p):
            return 0.03125
        if affix(p):
            return 0.015625
        if inf.his_family(p):
            return 0.0078125
        if inf.crossref(p):
            return 0.00390625
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
    ungl = sorted(v for v in keys if lv[v] == 0.375)
    outv = sorted(v for v in keys if lv[v] == 0.34375)
    nochi = sorted(v for v in keys if lv[v] == 0.3125)
    vroot = sorted(v for v in keys if lv[v] == 0.25)
    sistr = sorted(v for v in keys if lv[v] == 0.125)
    syncp = sorted(v for v in keys if lv[v] == 0.0625)
    awag = sorted(v for v in keys if lv[v] == 0.046875)
    chain = sorted(v for v in keys if lv[v] == 0.03125)
    afx = sorted(v for v in keys if lv[v] == 0.015625)
    famly = sorted(v for v in keys if lv[v] == 0.0078125)
    xref = sorted(v for v in keys if lv[v] == 0.00390625)
    good = sorted(listed + infl + vouch + ungl + outv + nochi + vroot + sistr
                  + syncp + awag + chain + afx + famly + xref)
    emit = {2: 1, 1: 2, 0.5: 3, 0.375: 4, 0.34375: 5, 0.3125: 6, 0.25: 7,
            0.125: 8, 0.0625: 9, 0.046875: 10, 0.03125: 11, 0.015625: 12,
            0.0078125: 13, 0.00390625: 14}

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
        "// 4 = a regular inflection of a root the wordlist LISTS but never\n"
        "// GLOSSED, spoken for by that root's own paradigm (%d). Rule 2 asks two\n"
        "// things of a root and needs both, and for these the second cannot be\n"
        "// asked at all: the gloss table holds nothing for the root. That is a\n"
        "// hole in the table, not a verdict on the word — most of a paradigm is\n"
        "// glossless — so the root's own attested inflection answers for it\n"
        "// (`ptbgi` off the bare `tbgi`, through `tbgan` 養家畜的地方, against his\n"
        "// 託人餵養). It cannot re-open the trap rule 2 exists to shut: a root that\n"
        "// HAS a gloss is read and refused by rule 2 and never arrives here.\n"
        "// 5 = 4 where the root IS glossed and the gloss DISAGREES, outvoted by\n"
        "// two of the root's own inflections (%d). Rule 4 asks the paradigm where\n"
        "// the gloss table is silent; this asks it where the gloss table SPEAKS and\n"
        "// rule 2 has already refused what it said. A citation gloss is one sense\n"
        "// an editor chose to print for a headword, and the same wordlist writing\n"
        "// that root out across its slots is the better witness. `paux` is glossed\n"
        "// 犁田 to plough, and batch 148 refused his 翻轉 family on those grounds;\n"
        "// but `mknpaux` 反過來 and `mspaux` 會翻 are the SAME wordlist saying the\n"
        "// word means turn over. Ploughing is turning soil over: 犁田 was the narrow\n"
        "// sense, not the meaning. Rule 4's guards verbatim, and one more, because\n"
        "// overriding a gloss needs better evidence than filling a hole — TWO\n"
        "// independent inflections must agree, or one must agree on a whole\n"
        "// two-character word. His SISUN 縫 IS reached here, since `sisi` is glossed\n"
        "// the wine strainer and that gloss disagrees; and then no inflection of\n"
        "// `sisi` agrees with 縫 either. The paradigm is asked, and declines.\n"
        "// 6 = a regular inflection of a listed and GLOSSED root, for a word HE\n"
        "// never glossed (%d). Rule 2 makes his Chinese and the root's gloss agree\n"
        "// on a character; for these the only Chinese anywhere near the word\n"
        "// belongs to an EXAMPLE SENTENCE, and rule 7 below already holds that a\n"
        "// sentence gloss is too loose to license an agreement. Then it is too\n"
        "// loose to license a REFUSAL: a translator rendering 我們去求爸爸 owes no\n"
        "// stem its dictionary meaning. So there is no gloss test here and the\n"
        "// guards carry it — the root listed AND glossed, four letters, not a\n"
        "// 人名/地名 gloss, and EXACTLY ONE root candidate, since with no gloss\n"
        "// nothing can break a tie. His SISUN 縫 cannot arrive: he glossed it, so\n"
        "// rule 2 reads it and refuses it.\n"
        "// 7 = 2 over 3: a regular inflection of a root the wordlist only vouches\n"
        "// for through ITS own inflections (%d). Neither the word nor its root is\n"
        "// listed, so the gloss agreement is taken against the root's attested\n"
        "// supporter and only against Chinese he attached to the word as a word.\n"
        "// Rules 4 and 7 run a chain of the same length and carry the same\n"
        "// guards; 4 sits above 7 because its root is a word the wordlist prints\n"
        "// and 6's is a hypothesis.\n"
        "// 8 = a SISTER SLOT: the wordlist writes this same stem with two OTHER\n"
        "// paradigm suffixes and not with this one (%d). Most of a paradigm is\n"
        "// glossless, so 2, 3, 4, 5, 6 and 7 cannot reach these — the claim is about\n"
        "// morphology rather than meaning, and the gate is his: the word must be\n"
        "// one he printed in a ° paradigm line, which is his own statement that it\n"
        "// is an inflectional slot and not a word in its own right.\n"
        "// 9 = 2 with the root's OWN first vowel syncopated (%d). Truku writes no\n"
        "// schwa, so a root loses that vowel under affixation — GAMIL 根 but\n"
        "// `Tgmilan` — and rule 2 can only ever delete a vowel at the end. Since\n"
        "// this inserts a letter he did not write, the gloss must be one he\n"
        "// attached to the word as a word, never an example sentence.\n"
        "// 10 = an -aw ~ -ag- SLOT (%d). A root ending -aw writes -ag- before a\n"
        "// suffix, and the wordlist settles that on its own, 76 pairs to 2:\n"
        "// `bglaw` gives `bglagan` … `bglagun`, `bhraw` gives `bhragan` …\n"
        "// `bhragun`. So these are ordinary slots whose citation form no rule\n"
        "// above can find, because every one of them looks for the letters he\n"
        "// actually wrote. His SPADAO family is the case: p. 228 is about giving\n"
        "// presents and modern Truku has the whole thing — `pspadaw`\n"
        "// 慷慨（不計價的送人）, `pnpadaw` 送過的禮物, `emppadaw` 將…作為禮物 — and the\n"
        "// map had already written his UNsuffixed forms onto it. The four\n"
        "// suffixed slots fell through everything, and `roots()` then found\n"
        "// `dagi` 要煮飯 sitting inside `pspdagi`. Nothing was misspelled: his\n"
        "// `pspdagun` IS the modern slot. Restoring the stem inserts a vowel, so\n"
        "// the same slot-gloss gate as 4, 7, 9 and 11, and the candidates are\n"
        "// walked longest first — that reaches `pspadaw` 慷慨 rather than bare\n"
        "// `padaw`, which the wordlist files as 無意義詞, an entry its own\n"
        "// derivatives refute.\n"
        "// 11 = 2 over a root that is itself one step from a glossed root (%d):\n"
        "// the CV- reduplication that makes no new lexeme (`qqgu` on `qgu`), or a\n"
        "// second round of ordinary affixation (`swiwil` on `wiwil`). Rules 2-9\n"
        "// stop at the first listed root and ask its gloss, and most of a paradigm\n"
        "// is glossless. Two steps of inference, so the same slot-gloss gate as 4,\n"
        "// 7 and 9 — which here refuses every illicit spelling the rule would find.\n"
        "// 12 = an AFFIX LETTER (%d). Twelve of his cards are headed by one letter\n"
        "// and are his grammars of the particles and the productive affixes, not\n"
        "// word entries; their claim is `p` -> `p`, an identity, so there is no\n"
        "// respelling to doubt. No lexicon lists an affix, so the evidence is that\n"
        "// it is productive over words the lexicon DOES list.\n"
        "// 13 = HIS OWN PARADIGM, where the wordlist has none (%d). Rule 4 asks a\n"
        "// listed-but-unglossed root's modern paradigm what the root means. For\n"
        "// these the paradigm is glossless too, end to end — the wordlist is not\n"
        "// disagreeing, it is silent — so his own cards on that root are asked\n"
        "// instead. Two of them, agreeing on a two-character run: one card is a\n"
        "// restatement, and a single shared character between two glosses by the\n"
        "// same hand is his prose style, not corroboration. Where the paradigm\n"
        "// SPEAKS and disagrees, the disagreement is evidence and the value stays\n"
        "// pale.\n"
        "// 14 = HE NAMES THE WORD (%d). Some glosses are not meanings but\n"
        "// pointers — `rnjingan` is （ldingan 的過去式）and nothing else — so there\n"
        "// is nothing for rules 2-13 to weigh. A stated root beats an inferred\n"
        "// one: where the token he cites IS the root the affix rules found — or a\n"
        "// sibling built on it — his statement and the analysis agree, and that is\n"
        "// the whole evidence. The pointer must land on a root the morphology\n"
        "// found; it may never supply one, because his 參見 notes cite synonyms as\n"
        "// well as forms and a synonym says nothing about how THIS word is spelt.\n"
        "// app.js paints all fourteen in the deep brown; a value NOT in here is\n"
        "// still a proposal and stays pale.\n"
        "window.MODERN_VERIFIED = {\n"
        % (len(good), len(keys), len(listed), len(infl), len(vouch), len(ungl),
           len(outv), len(nochi), len(vroot), len(sistr), len(syncp), len(awag), len(chain),
           len(afx), len(famly), len(xref)))
    for v in good:
        out.write('  "%s": %d,\n' % (v, emit[lv[v]]))
    out.write("};\n")
    out.close()
    print("listed: %d   regularly inflected: %d   vouched by its paradigm: %d   "
          "unglossed listed root: %d   outvoted gloss: %d   "
          "no Chinese of his: %d   "
          "inflected off a vouched root: %d   "
          "sister slot: %d   syncopated root: "
          "%d   -aw~-ag- slot: %d   chained root: %d   affix letter: %d   his own paradigm: %d   "
          "he names the word: %d   unverified: %d   "
          "(of %d distinct)"
          % (len(listed), len(infl), len(vouch), len(ungl), len(outv),
             len(nochi),
             len(vroot), len(sistr),
             len(syncp), len(awag), len(chain), len(afx), len(famly), len(xref),
             len(keys) - len(good), len(keys)))
    print("wrote site/verified.js")


if __name__ == "__main__":
    main()
