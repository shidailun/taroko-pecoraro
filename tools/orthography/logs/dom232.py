# -*- coding: utf-8 -*-
"""[batch 232] Three sweeps that came back empty, and a refusal repaired.

    0 pairs. The metric HOLDS at 5346/5429 = 98.4712%.
    sole-blocked pairs 79 over 67 types, unchanged

Batch 231 gained two pairs with an instrument no token-keyed test can imitate:
a query for a MULTI-WORD string in an outside corpus. This batch generalises
that instrument, and two others beside it, and every one of the three returns
nothing. All three are kept, with their controls, so nobody rebuilds them --
as with `freezesweep.py`, `tail221.py` and `premise231.py`.

### 1. THE JOIN SWEEP, GENERALISED -- closed at two

135 of his tokens render pale. For each, at every split point: both halves >= 2
letters, both modernising to words in `attested_modern.json`, both written by
HIM standing alone, the SPLIT bigram present in the ILRDF parquets, the JOINED
string absent from them, and the joined token not one he CARDS (batch 231's
card exclusion). **0 candidates.**

The positive control is what makes that readable. Back the two batch-231
rulings out of the map and run the same sweep: `kasayang` (parquet 433) and
`isoka` (26) come back as its top two rows unaided. The sweep can see what it
is looking for; there is no third.

Widened past the pale list to all 7,378 of his tokens it returns 10, and the
other eight all render **DARK already** -- batch 222's rule, a correctness seam
worth zero pairs by construction. None is near batch 231's bar: `daxani` (76),
`tagaxan` (6), `puda` (4), and five at 1-2 against 403.

### 2. THE PARALLEL CORPUS, READ AS SENTENCES -- 1 proposal, and it is a refusal

Batch 183 read the parquets' Mandarin column for rows whose Truku side is ONE
word (8,875 of them) and refused the phrase rows **in writing**: `baga bubu`
母親的雙手 would gloss `baga` 手 and 母親 with equal confidence, and a shared
character cannot tell which half it matched. That reason is about building a
WORD -> GLOSS file and it is right. It is not a reason against a question that
never attributes a gloss to a word: take HIS example sentence and ITS Chinese,
find corpus sentences whose Chinese overlaps his, and ask which Truku word in
them is close in SHAPE to his pale token. Sentence against sentence is apples
to apples.

50,848 corpus rows carry Chinese; 85 of his example rows contain a pale token,
over 72 distinct values. **Containment, not Jaccard** -- his example glosses are
whole sentences and the corpus rows are frequently single words, so a union
denominator scores a perfect sense match at 0.1 and throws it away. That change
alone took the sweep from 3 raw hits to 13 deduped proposals.

Eleven of the thirteen are the failure mode batch 221 already documented: the
shared characters are pronouns and function words -- 有 `niqan`, 我的 `naku`,
你們的 `nnamu`, 你 `su`, 正在 `gaga`, 孩子們 `lqlaqi` -- and the shape match is
coincidence. `tbiran` 節慶盛裝 -> `birat` 用具的手把 and `mqlaq` 發癢 ->
`lqlaqi` 孩子們 are the shape of the whole class. **And the instrument's
strongest-looking hit is a trap already priced**: it proposes `yianu -> yamu` at
containment 1.00, which is precisely the collapse of two sub-forms batch 231
refused in writing on his own YAMO card. The thirteenth, `gaqat -> gakat`, is
the one adjudicable row and section 3 is its adjudication.

### 3. GAQAT -- the verdict stands, the PREMISE does not (batch 227)

`dom214.py:97` refuses it thus: "`gakat` 起身;站立 shares the SHAPE only, and his
`Tdoloi gakat (gaqat)` 腳踏車 is a second sense, so one key cannot serve both."
The second clause is the argument and it is sound. The first is false.

His own GAKAT card is glossed **蹲著——彎著——屈著**, and its example glosses the
bicycle **腳踏車(人蹲坐其上的車)** -- "the vehicle one squats on". The register's
`gakat` is 起身爲;站立. Both are posture roots and the etymology is his own note.
The shape is the least of what they share; scored on meaning it PASSES.

What actually refuses it is the homograph, and that is the stronger ground. He
cards GAKAT 蹲著 and GAQAT 冰塊、冰柱 **separately**. The register's ice word is
`huda`, with a family of its own -- `gmnhuda` 製冰塊, `gmhuda` 製冰的, `nhuda`
原來結冰, `smhhuda` 吃冰 -- and nothing anywhere near `gaqat`, so batch 204's
different-root test settles the ice card: the meaning lives elsewhere and there
is nothing to respell. Two of his three `gaqat` tokens are that ice sense and
one is the bicycle parenthetical, so a remap would paint two correct renders
wrong to fix one. Batch 205's DIMA/QALO verbatim.

And `CITE_SPELL` cannot rescue the good half: it fires only where `noLink` is
true, which is a render as a NAME, and **both** blocked sentences are running
text. The refuse-only hook has nothing to refuse here.

So batch 200's parenthetical rule is asked and answered: his `Tdoloi gakat
(gaqat)` really is testimony that two spellings are one word IN THE BICYCLE
SENSE -- his GAKAT card writes the compound with no parenthesis at all,
`Tdloi gakat` -- and the map still cannot act on it, because the same string is
a different word two cards away.

### 4. HIS BOOK AS ITS OWN SPELLCHECKER -- 40 shapes, 0 survivors

Batch 213 corrected `smuwan` by asking whether a string appearing once in a book
that repeats itself is even his. Run as a sweep: a token he writes at most twice
whose value is PALE, one edit from a token he writes five or more times whose
value is DARK. It returns 40 shapes, and **none survives the gloss test**. A
near-twin at one edit is what a language with this phonotactics looks like, not
a typo.

Two guards decide that zero, and both are the record's own rules rather than
this batch's taste. Batch 203's settled classes refuse a bare fragment: `sm`
scores twice on 你, a pronoun standing in the sentence, so a candidate must be
three letters. And batch 218 (a gloss score can land on the apparatus) plus
batch 221 (one common character is the whole noise mode, naming 著, 子, 一, 人)
refuse a score on a character that carries no meaning. The stoplist for that is
**DERIVED, not hand-picked** -- the commonest characters across the register's
own glosses -- and its depth is set by the record too: `STOP_MUST` requires the
derivation to reproduce all six characters the project already named as noise,
which happens at 30 (著 sits at rank 26, 717 rows, behind 是 17 and 子 18).

It is load-bearing and the amount is measurable: withdraw the stoplist entirely
and 3 shapes survive -- `ixol`/`mixol` on 不的, `olo`/`ole` on 是, `ubai`/`uxai`
on 人的. Cut it at 10 and 2 survive. At 30, none. Every one of those three is
scoring on a function word inside his sentence gloss, which is precisely what
batch 218 says is not agreement about MEANING.

    python tools/orthography/logs/dom232.py       (site served at :8765)
"""
import collections
import glob
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ORTH = os.path.dirname(HERE)
H = os.path.dirname(os.path.dirname(ORTH))
H = os.path.join(H, "taroko-pecoraro") if not os.path.exists(
    os.path.join(H, "site")) else H
SITE = os.path.join(H, "site")
PARQUET_ROOT = r"C:/dev/ILRDF/datasets"
URL = "http://127.0.0.1:8765/"

# ---- the pins -------------------------------------------------------------
FLOOR = 5346                      # pairs; batch 231's figure, HELD not raised
DENOM = 5429
AUDIO_IDS = 5134
SOLE_PAIRS, SOLE_TYPES = 79, 67

# GAQAT: refused, and the refusal is REPAIRED not overturned
REFUSED = "gaqat"
REFUSED_TO = "gakat"
HIS_CARDS = {"GAKAT": "蹲", "GAQAT": "冰"}       # he cards them separately
BICYCLE_NOTE = "人蹲坐其上的車"                    # his own etymology
ICE_ROOT = "huda"
ICE_FAMILY_MIN = 8                # register rows carrying 冰 on the huda root
HIS_GAQAT, HIS_GAKAT = 3, 4       # his own token counts
GAQAT_ICE, GAQAT_BIKE = 2, 1      # ...and how they split by sense
CITED = (("dom214.py", "shares the shape only"),)

# the three sweeps
JOIN_PALE = 0                     # candidates over the pale list
JOIN_CONTROL = ("kasayang", "isoka")   # ...and what the control recovers
JOIN_ALL_DARK = 8                 # the widened sweep's other rows, all dark
CORPUS_ROWS = 50000               # floor; parallel rows carrying Chinese
SENT_PROPOSALS = 13
SENT_LIVE = 0                     # ...that are not noise or already refused
SENT_TRAP = ("yianu", "yamu")     # its strongest hit is a written refusal
SPELL_SHAPES = 40
SPELL_LIVE = 0
# Batch 218 (a gloss score can land on the apparatus) and batch 221 (one common
# character at 2-4 edits is the whole noise mode, naming 著, 子, 一, 人) both
# say a shared Han character is only evidence if the character carries meaning.
# DERIVED, not hand-picked: the commonest characters across the register's own
# glosses. STOP_MUST is the control -- the derivation has to reproduce the six
# the record already named, or it is a list fitted to this batch. And the cut is
# not free either: N is the smallest value that reproduces all six. 25 misses
# 著, which sits at rank 26 (717 rows) behind 是 17 and 子 18, so the record's
# own naming sets the depth.
STOP_N = 30
STOP_MUST = set("的人是著子一")

HAN = re.compile(r"[一-鿿]")
TOK = re.compile(r"[A-Za-zÇçÀ-ſ'’ʼ\"]+")
fails = []


def ck(cond, msg):
    if not cond:
        fails.append(msg)
    return cond


# ---- readers --------------------------------------------------------------
def entries_json():
    s = io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()
    return json.loads(s[s.index("["):s.rindex("]") + 1])


def modern_map():
    t = io.open(os.path.join(SITE, "modern_map.js"), encoding="utf-8").read()
    a = t.index("window.MODERN_MAP = {")
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$',
                           t[a:t.index("\n};", a) + 2], re.M))


def verified():
    t = io.open(os.path.join(SITE, "verified.js"), encoding="utf-8").read()
    return dict((m.group(1), int(m.group(2)))
                for m in re.finditer(r'^  "(.+?)": (\d+),?$', t, re.M))


def sources():
    def L(n):
        return json.load(io.open(os.path.join(ORTH, n), encoding="utf-8"))
    return (set(L("attested_modern.json")), L("attested_gloss.json"),
            L("bible_gloss.json"), L("parquet_gloss.json"))


def gl(D, w):
    g = D.get(w) or []
    return g if isinstance(g, list) else [g]


def char_rules(w):
    k = re.sub("[’ʼ\"ʔ']", "", w.lower()).replace("ł", "l")
    return "".join({"x": "h", "o": "u", "l": "r"}.get(c, c) for c in k)


def ed(a, b):
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, y in enumerate(b, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (x != y))
    return d[-1]


def his_tokens():
    cnt = collections.Counter()

    def walk(n):
        for k in ("hw", "form", "t", "paradigm"):
            v = n.get(k)
            for s in ([v] if isinstance(v, str)
                      else (v or []) if isinstance(v, list) else []):
                for w in TOK.findall(s or ""):
                    cnt[w.lower().replace("’", "'").replace("ʼ", "'")] += 1
        for x in (n.get("examples") or []):
            walk(x)
        for sb in (n.get("subs") or []):
            walk(sb)
    for e in entries_json():
        walk(e)
    return cnt


def his_headwords():
    out = set()

    def walk(e):
        for k in ("hw", "form"):
            v = e.get(k)
            if isinstance(v, str):
                for w in TOK.findall(v):
                    out.add(w.lower().replace("’", "'").replace("ʼ", "'"))
        for sb in (e.get("subs") or []):
            walk(sb)
    for e in entries_json():
        walk(e)
    return out


def audio_ids():
    out = set()

    def walk(e):
        for x in (e.get("examples") or []):
            if x.get("a"):
                out.add(x["a"])
        for sb in (e.get("subs") or []):
            walk(sb)
    for e in entries_json():
        walk(e)
    return out


def corpus(with_zh=False):
    """Returns None if the datasets are not mounted -- a missing corpus is a
    skip, not a failure; the map is not wrong because a drive is unplugged."""
    if not os.path.isdir(PARQUET_ROOT):
        return None
    try:
        import pyarrow.parquet as pq
    except ImportError:
        return None
    out = []
    for d in sorted(glob.glob(os.path.join(PARQUET_ROOT, "*", "Truku"))):
        p = d.replace("\\", "/")
        tc, gc = (("formosan", "mandarin") if "ithuan_formosan_text" in p
                  else ("transcript", "translation"))
        for fp in sorted(glob.glob(os.path.join(d, "*.parquet"))):
            try:
                t = pq.read_table(fp, columns=([tc, gc] if with_zh else [tc]))
            except Exception:
                continue
            tr = t.column(tc).to_pylist()
            zh = t.column(gc).to_pylist() if with_zh else [None] * len(tr)
            for a, b in zip(tr, zh):
                out.append((re.findall(r"[A-Za-z']+", (a or "").lower()), b))
    return out


def measure():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        pg.goto(URL)
        pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
        pg.goto(URL + "?q=%CC%81")          # a query that matches every card
        pg.wait_for_timeout(22000)
        # dom231's harvester verbatim. It lowercases (`.hw` prints the modern
        # headword UPPERCASE -- batch 226), walks the `.truku` boxes for the
        # PAIR metric and the whole card for the CENSUS (batch 222), and does
        # not put a `.truku` prefix on a comma-separated selector (batch 216).
        d = pg.evaluate(r"""() => {
          const SEL = 'span.w-mod, span.w-unv, span.w-raw';
          let tot = 0, ok = 0;
          const seen = {}, unv = {}, raw = {}, inTruku = {}, sole = {};
          document.querySelectorAll('#results > article.entry').forEach(c => {
            c.querySelectorAll('.truku').forEach(b => {
              const sp = [...b.querySelectorAll(SEL)];
              if (!sp.length) return;
              tot++;
              if (sp.every(s => s.classList.contains('w-mod'))) ok++;
              else {
                const bad = [...new Set(sp.filter(s => !s.classList.contains('w-mod'))
                               .map(s => (s.textContent||'').trim().toLowerCase()))];
                if (bad.length === 1) sole[bad[0]] = (sole[bad[0]] || 0) + 1;
              }
            });
            c.querySelectorAll(SEL).forEach(s => {
              const t = (s.textContent || '').trim().toLowerCase();
              seen[t] = (seen[t] || 0) + 1;
              if (s.classList.contains('w-unv')) unv[t] = (unv[t] || 0) + 1;
              if (s.classList.contains('w-raw')) raw[t] = (raw[t] || 0) + 1;
              if (s.closest('.truku')) inTruku[t] = (inTruku[t] || 0) + 1;
            });
          });
          return {tot: tot, ok: ok, seen: seen, unv: unv, raw: raw,
                  inTruku: inTruku, sole: sole}; }""")
        b.close()
        return d


# ---- the batch ------------------------------------------------------------
def main():
    MM, VER = modern_map(), verified()
    AM, AG, BG, PG = sources()
    CNT, HEADS, ENT = his_tokens(), his_headwords(), entries_json()
    D = measure()
    # `seen` is EVERY span, not the dark ones -- dark is what is left when the
    # two pale classes come out. Reading it as dark makes a pale word its own
    # supporting evidence.
    PALE = set(D["unv"])
    DARK = set(D["seen"]) - PALE - set(D["raw"])

    def modern(w):
        k = re.sub("[’ʼ\"ʔ]", "'", w.lower()).replace("ł", "l")
        return MM.get(k) or char_rules(k)

    print("pairs %d/%d = %.4f%%   pale %d spans / %d types"
          % (D["ok"], D["tot"], 100.0 * D["ok"] / D["tot"],
             sum(D["unv"].values()), len(D["unv"])))

    # --- the metric HOLDS. Nothing was ruled, so equality is the claim here,
    # and a RISE is as much news as a fall: it would mean something moved that
    # this batch did not decide.
    ck(D["ok"] == FLOOR, "FLOOR %d pairs, got %d" % (FLOOR, D["ok"]))
    ck(D["tot"] == DENOM, "DENOM %d, got %d" % (DENOM, D["tot"]))
    ck(len(audio_ids()) == AUDIO_IDS,
       "audio ids %d, got %d" % (AUDIO_IDS, len(audio_ids())))
    sole = sum(D["sole"].values())
    ck(sole == SOLE_PAIRS and len(D["sole"]) == SOLE_TYPES,
       "sole-blocked %d/%d pairs/types, got %d/%d"
       % (SOLE_PAIRS, SOLE_TYPES, sole, len(D["sole"])))

    # === 3. GAQAT: the refusal, repaired ==================================
    ck(MM.get(REFUSED) != REFUSED_TO,
       "FAIL the map now sends %s to %s. It was refused because he cards GAKAT "
       "蹲著 and GAQAT 冰塊 separately and one key cannot serve both; if that "
       "changed, the refusal needs re-arguing, not deleting." % (REFUSED,
                                                                REFUSED_TO))
    ck(REFUSED in PALE, "%s no longer renders pale" % REFUSED)
    ck(REFUSED_TO in DARK and REFUSED_TO not in PALE,
       "%s is no longer dark -- the parenthetical has no dark side" % REFUSED_TO)
    ck(D["sole"].get(REFUSED) == 2,
       "%s sole-blocks %s pairs, expected 2" % (REFUSED, D["sole"].get(REFUSED)))

    # his two cards, and the POSITIVE half of the repair: his own GAKAT gloss
    # carries the posture, so `shares the shape only` is false.
    cards = dict((e.get("hw"), e) for e in ENT if e.get("hw") in HIS_CARDS)
    for hw, ch in HIS_CARDS.items():
        ck(hw in cards, "his %s card is gone" % hw)
        ck(ch in (cards.get(hw, {}).get("zh") or ""),
           "his %s card no longer glosses %s" % (hw, ch))
    ck(any(BICYCLE_NOTE in (x.get("zh") or "")
           for x in (cards.get("GAKAT", {}).get("examples") or [])),
       "his GAKAT example no longer carries the etymology %s" % BICYCLE_NOTE)
    reg = " ".join(str(x) for x in gl(AG, REFUSED_TO) + gl(PG, REFUSED_TO))
    ck("站" in reg or "身" in reg,
       "the register's %s is no longer a posture root: %s" % (REFUSED_TO, reg))

    # the NEGATIVE half, as a regex over the register rather than a list: if a
    # gaqat-shaped word ever carries 冰, that is the news that re-opens this.
    ice = [w for Dg in (AG, BG, PG) for w, g in Dg.items()
           if "冰" in str(g)]
    ck(len([w for w in ice if ICE_ROOT in w]) >= ICE_FAMILY_MIN,
       "the %s ice family fell below %d rows" % (ICE_ROOT, ICE_FAMILY_MIN))
    ck(not [w for w in ice if ed(w, REFUSED) <= 1],
       "a %s-shaped word now carries 冰: %s"
       % (REFUSED, [w for w in ice if ed(w, REFUSED) <= 1]))
    ck(CNT.get(REFUSED) == HIS_GAQAT and CNT.get(REFUSED_TO) == HIS_GAKAT,
       "his counts moved: %s %s / %s %s" % (REFUSED, CNT.get(REFUSED),
                                            REFUSED_TO, CNT.get(REFUSED_TO)))
    # ...and the split by sense, which is the whole price of a remap
    ice_n = bike_n = 0

    def sense(e, zh):
        nonlocal ice_n, bike_n
        z = e.get("zh") or zh
        for k in ("hw", "t"):
            v = e.get(k)
            if isinstance(v, str) and REFUSED in v.lower():
                if "冰" in (z or ""):
                    ice_n += 1
                elif "車" in (z or ""):
                    bike_n += 1
        for x in (e.get("examples") or []):
            sense(x, z)
        for sb in (e.get("subs") or []):
            sense(sb, z)
    for e in ENT:
        sense(e, e.get("zh") or "")
    ck(ice_n == GAQAT_ICE and bike_n == GAQAT_BIKE,
       "the sense split moved: ice %d bike %d" % (ice_n, bike_n))

    # the refusal this repairs must still be findable in the record
    for f, s in CITED:
        ck(s in io.open(os.path.join(HERE, f), encoding="utf-8").read(),
           "%s no longer carries the premise this batch repairs: %s" % (f, s))

    # === 1. the join sweep ================================================
    C = corpus()
    if C is None:
        print("parquets not mounted -- sweeps 1 and 2 SKIPPED")
    else:
        U, B = collections.Counter(), collections.Counter()
        for ws, _ in C:
            U.update(ws)
            B.update(" ".join(p) for p in zip(ws, ws[1:]))

        def joins(mp):
            def mo(w):
                k = re.sub("[’ʼ\"ʔ]", "'", w.lower()).replace("ł", "l")
                return mp.get(k) or char_rules(k)
            out = []
            for t in sorted(CNT):
                if t in HEADS or len(t) < 4 or mo(t) not in PALE_OR_ALL:
                    continue
                j = mo(t)
                if B.get(j) or U.get(j):
                    continue
                for i in range(2, len(t) - 1):
                    a, b = t[:i], t[i:]
                    ma, mb = mo(a), mo(b)
                    if ma in AM and mb in AM and CNT.get(a) and CNT.get(b) \
                            and B.get("%s %s" % (ma, mb), 0) >= 1:
                        out.append(t)
            return out

        PALE_OR_ALL = PALE
        ck(len(joins(MM)) == JOIN_PALE,
           "the join sweep found %d candidates over the pale list, expected %d: "
           "%s" % (len(joins(MM)), JOIN_PALE, joins(MM)))
        # POSITIVE CONTROL: back batch 231 out and the sweep must recover both
        back = dict(MM)
        for k in JOIN_CONTROL:
            back.pop(k, None)
        PALE_OR_ALL = set(U) | set(PALE) | set(back.values()) | \
            set(char_rules(k) for k in JOIN_CONTROL)
        got = set(joins(back))
        ck(set(JOIN_CONTROL) <= got,
           "the join sweep cannot see its own two known joins: got %s"
           % sorted(got))
        ck(len(got) == len(JOIN_CONTROL) + JOIN_ALL_DARK,
           "the widened join sweep returned %d rows, expected %d"
           % (len(got), len(JOIN_CONTROL) + JOIN_ALL_DARK))
        PALE_OR_ALL = PALE

        # === 2. the sentence sweep ========================================
        CZ = corpus(with_zh=True)
        rows = [(ws, set(HAN.findall(zh))) for ws, zh in CZ
                if zh and HAN.search(zh)]
        ck(len(rows) >= CORPUS_ROWS,
           "corpus rows with Chinese fell to %d, floor %d"
           % (len(rows), CORPUS_ROWS))
        byhan = collections.defaultdict(list)
        for i, (_, hs) in enumerate(rows):
            for h in hs:
                byhan[h].append(i)
        his_rows = []

        def ex(e):
            for x in (e.get("examples") or []):
                t, zh = x.get("t") or "", x.get("zh") or ""
                if t and zh and HAN.search(zh):
                    for w in TOK.findall(t):
                        if modern(w) in PALE:
                            his_rows.append((modern(w), set(HAN.findall(zh))))
            for sb in (e.get("subs") or []):
                ex(sb)
        for e in ENT:
            ex(e)
        props = set()
        for val, hs in his_rows:
            if not hs:
                continue
            cand = collections.Counter()
            for h in hs:
                for i in byhan.get(h, ()):
                    cand[i] += 1
            best = None
            for i, sh in cand.items():
                if sh < 2:
                    continue
                ws, chs = rows[i]
                c = sh / float(min(len(hs), len(chs)))
                if c < 0.60:
                    continue
                for w in ws:
                    if w == val or w in PALE or w not in AM:
                        continue
                    e2 = ed(val, w)
                    if e2 > 2 or e2 >= max(2, len(val) - 2):
                        continue
                    if best is None or (-e2, c) > best[0]:
                        best = ((-e2, c), val, w)
            if best:
                props.add((best[1], best[2]))
        ck(len(props) == SENT_PROPOSALS,
           "the sentence sweep returned %d proposals, expected %d"
           % (len(props), SENT_PROPOSALS))
        ck(SENT_TRAP in props,
           "the sentence sweep no longer proposes %s -> %s, the written "
           "refusal that prices the whole class" % SENT_TRAP)
        ck((REFUSED, REFUSED_TO) in props,
           "the sentence sweep no longer finds its one adjudicable row")

    # === 4. his book as its own spellchecker ==============================
    ctx = {}

    def cx(e, zh):
        z = e.get("zh") or zh
        for k in ("hw", "form", "t"):
            v = e.get(k)
            if isinstance(v, str):
                for w in TOK.findall(v):
                    ctx.setdefault(w.lower(), set()).update(
                        HAN.findall(z or ""))
        for x in (e.get("examples") or []):
            cx(x, z)
        for sb in (e.get("subs") or []):
            cx(sb, z)
    for e in ENT:
        cx(e, e.get("zh") or "")
    hf = collections.Counter()
    for w, g in AG.items():
        hf.update(set(HAN.findall(str(g))))
    STOP = set(c for c, _ in hf.most_common(STOP_N))
    ck(STOP_MUST <= STOP,
       "the derived stoplist misses characters the record already named as "
       "noise: %s" % sorted(STOP_MUST - STOP))

    freq = [w for w, c in CNT.items() if c >= 5]
    shapes, live = set(), []
    for w, c in CNT.items():
        # A bare fragment is not a spelling candidate. `sm` is refused by
        # construction in the record for exactly this reason, and left in it
        # scores twice on 你 -- a pronoun in the sentence, not a meaning.
        if c > 2 or len(w) < 3 or modern(w) not in PALE:
            continue
        for f in freq:
            if f == w or abs(len(f) - len(w)) > 1 or ed(w, f) != 1:
                continue
            fv = modern(f)
            if fv not in DARK or fv in PALE:
                continue
            shapes.add((w, f))
            g = set()
            for Dg in (AG, BG, PG):
                for x in gl(Dg, fv):
                    g.update(HAN.findall(str(x)))
            sh = (ctx.get(w, set()) & g) - STOP
            if sh:
                live.append((w, f, "".join(sorted(sh))))
    ck(len(shapes) == SPELL_SHAPES,
       "the spellcheck sweep returned %d shapes, expected %d"
       % (len(shapes), SPELL_SHAPES))
    ck(len(live) == SPELL_LIVE,
       "the spellcheck sweep has %d shapes surviving the gloss test, "
       "expected %d: %s" % (len(live), SPELL_LIVE, live))

    for f in fails:
        print("FAIL " + f)
    print("\n%d assertions failed" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
