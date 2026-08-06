# -*- coding: utf-8 -*-
"""[batch 231] The clitic-join seam: two of his words typed as one.

    2 joins split (+2 pairs), 3 refusals, and a premise sweep that came back empty
    pairs 5344/5429 = 98.4343%  ->  5346/5429 = 98.4712%   (+2)
    pale  217 -> 215 spans, 142 -> 140 types (book-wide)
    sole-blocked pairs 81 -> 79 over 69 -> 67 types

### 1. KASAYANG -- his typewriter, not his language

His SLIYU example writes `Malu kasayang da; ma" ga smliyu sayang ka xedao da`
「現在天氣好了；看，太陽出來了！」 -- and his OWN SECOND CLAUSE writes `ka xedao`
split. The scan was read first (page 284 = book 263): it plainly writes the
first one joined, so the transcription is faithful and the fix belongs in the
map, which is display-only (batch 212).

`b57.py:127` pinned it to his own letters, `"kasayang": "kasayang",  # sayang`.
That is a **tier-M identity pin**, which batch 216 names as the one map entry
that ages, because it records a search that FAILED rather than evidence found.
What retires it is an OUTSIDE voice: in the ILRDF parquets (54,457 utterances)
`ka sayang` occurs 403 times and joined `kasayang` **zero**, fifteen of them in
his very frame -- `Malu karat ka sayang.` 今天是晴朗的天氣 against his `Malu
kasayang da`. Both halves are listed and verified, `ka` 主格標記 and `sayang`
今天；現在, and a two-word value is supported end to end (`attested()` splits on
the space, `build_verified.py:424` takes the min over the parts).

**His own book says the same thing, and says it mechanically.** Take every token
he writes that begins `ka`, whose remainder is a word he ALSO writes on its own
at least 20 times, and **which he does not CARD** -- a word he gives a headword
to is a word he is asserting exists, not a slip. Over his whole book the answer
is a set of size one: `kasayang`. `ka` stands alone 3,596 times. The join is a
slip of the typewriter, and it is the only one of its kind on that word.

The card exclusion is doing real work and is not a fitted parameter: without it
the `ka` test also returns `kana` 全部 (which he writes 435 times) and `kaya`
蚊帳, whose tag reads `[emprunt jap./chin.]` -- a Japanese loan and a hapax, so
the frequency guard alone would not have caught it. Both are headwords. Neither
is `ka` + a word.

### 2. ISOKA -- he writes BOTH spellings on the one line

    Lmobong ko payai mo sayang, iso ka (isoka) npkoyoç

Batch 200's parenthetical rule, with the direction reversed from the usual: here
his RUNNING TEXT is the split form and the PARENTHESIS is the join, so this is
not even a choice between two readings of his. The two sides go to different map
values of which exactly one is dark -- `iso -> isu` (code 1) and `ka -> ka`
(code 1), against a pale `isuka`. The pale side renders what the dark side
renders. The same `ka`+word test as above, run on `iso`, again returns a set of
size one.

**This overturns a written refusal, and names it** (batch 219): `dom219.py:233`,
`"isuka": "蓋住 is spuy, 覆蓋 is bbungan; different roots"`. What retires it is
that the refusal scored the LOBONG CARD's gloss against a token that is not the
card's word. The 蓋住 is on `Lmobong`; `isoka` is a pronoun plus a case marker.
That is batch 203's rule -- a sentence gloss is not the word's gloss -- so the
different-root test was run on the wrong left-hand side and never had a
candidate to find. The verdict is not being outvoted; the premise is being
corrected (batch 227).

Both entries are LOAD-BEARING and neither is a no-op (batch 227): `charRules`
unaided gives `kasayang` and `isuka`, so deleting either key does not return the
word to his letters, it returns a GREEN span of the same joined string.

### 3. The three refusals, both halves each (batch 221)

`yianu` -- his YAMO card's `Yiano` 為你們—給你們—願它歸你們所有. POSITIVE: the
register spells that whole paradigm, `yamu` `namu` `nnamu` `munan` `jyamu`
`knyamu` `empeenamu`. NEGATIVE: the only `y`/`jy`+`amu` shapes it holds are
`yamu` and `jyamu`, and the map ALREADY sends his `Yamo` to `yamu` -- so
respelling `Yiano` there would collapse two sub-forms his card distinguishes.
The scan was read (batch 213: a shape appearing once in a book that repeats
itself is a candidate for the glyph): page 383 at 9x, against the `m` of `namo`
on the SAME LINE, `Yiano` has two legs and `namo` has three. His `n` is real and
`entries.js` is untouched.

`urang` -- his ULANG 反覆發生的（？）－週期性的（？）－慣常的（？）. 週期 and 慣常
have ZERO carriers in any of the three gloss files; 反覆 has eight, and the
nearest of them to his letters is `nrrui` at four edits. Batch 204's
different-root test: the meaning lives elsewhere and there is nothing to respell.

`sruweq` -- his SLOWEQ, and this one is a LIMIT, not a refusal. The card is
tagged `(R. = ??)` with `fr = "??"` and `zh = "？？"`: **he could not gloss it
himself.** The gloss test needs a gloss on HIS side too, and the project's only
non-circular instrument over an unattested word (batch 204) is exactly that
test, so there is no question to ask. `sruweq` has no map entry at all and
renders GREEN, and batch 216's rule applies -- a green span's fix is a new map
entry, which is itself a spelling claim. It was already priced, in the batch log:
"Sruweq has no map entry and no attested neighbour (`sruwaq` 不滿 differs in the
vowel)."

He leaves **11** headwords unglossed. Eight of them already render dark; the
three that sole-block pairs are SDANGAN (1), SLOWEQ (1) and TBILAN (3). That is
the whole price of the class -- five pairs, none of them reachable by the gloss
test. Naming the limit is not opening a door to clear it (batch 203).

### 4. The premise sweep -- a NEGATIVE result, kept

Batch 230 repaired two false premises by hand, which reads like a seam. Run
mechanically over the whole record (`logs/premise231.py`) the class is empty:
132 anchored token-absence claims of which 31 name a word that IS listed today,
34 gloss-absence claims of which 7 name a Han string that HAS carriers -- and
all 38 are the regex binding the wrong side of the sentence, because a refusal
of this project's usual shape names the absent thing and the present alternative
in one breath. Keep the negative result; don't rebuild it.

    python tools/orthography/logs/dom231.py      # site served at :8765
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SITE = os.path.join(ROOT, "site")
ORTH = os.path.join(ROOT, "tools", "orthography")
BASE = "http://127.0.0.1:8765/"
PARQUET_ROOT = "C:/dev/ILRDF/datasets"

FLOOR = 5346
DENOM = 5429
AUDIO_IDS = 5134

# --- the rulings: his key -> the value the map must emit
RULED = {
    "kasayang": "ka sayang",    # 1. his typewriter joined them; his book did not
    "isoka": "isu ka",          # 2. he writes both spellings on the one line
}
# every part of a multi-word value has to be verified on its own, which is what
# makes the value dark -- attested() splits on the space and so does
# build_verified.py:424. Assert the PARTS, not just the whole string.
PART_CODE = {"ka": 1, "sayang": 1, "isu": 1}
GONE_VALUES = ("kasayang", "isuka")     # ... must render nowhere at all
# [batch 227] What charRules does unaided. Neither entry is a no-op: deleting it
# gives back the joined string as a GREEN span, not his letters.
CHAR_INERT = {"kasayang": "kasayang", "isoka": "isuka"}

# --- his own book. Floors, because a count is a snapshot (batch 209); the two
# joins are asserted exactly, because a hapax growing is itself the news.
HIS_FLOORS = {"ka": 3596, "sayang": 176, "iso": 153}
HIS_EXACT = {"kasayang": 1, "isoka": 1, "yiano": 2}
# The join test, run over his whole book: a token beginning with the clitic whose
# remainder he also writes standing alone at least 20 times, and which he does
# NOT card. A word he gives a headword to is a word he asserts exists -- without
# that leg the `ka` test also returns his `kana` 全部 and his `kaya` 蚊帳
# `[emprunt jap./chin.]`, a hapax that no frequency guard would have caught.
JOIN_ALONE = 20
JOINS = {"ka": {"kasayang"}, "iso": {"isoka"}}
JOIN_NOT_CARDED = ("kana", "kaya")      # ... the two the exclusion removes

SENTENCES = (
    'Malu kasayang da; ma" ga smliyu sayang ka xedao da',
    "Lmobong ko payai mo sayang, iso ka (isoka) npkoyoç",
)
PARENTHETICAL = "iso ka (isoka)"        # 2. both spellings, his own hand

# --- the record this batch overturns or supersedes, cited by file and string
# (batch 219: a ruling that contradicts a written refusal must cite it).
CITED = (
    ("dom219.py", '"isuka": "蓋住 is spuy'),
    ("b57.py", '"kasayang": "kasayang"'),
)

# --- the outside voice. Counted over the ILRDF Truku parquets, sentence-padded
# and stripped to [a-z' ]. Skipped, not failed, if the datasets are not mounted.
PQ_FLOOR = {"ka sayang": 400, "isu ka": 25}
PQ_ZERO = ("kasayang", "isuka")
PQ_FRAME = ("malu", "ka sayang", 15)    # his own frame: Malu karat ka sayang.

# --- the refusals
STILL_PALE = ("yianu", "urang")
STILL_GREEN = ("sruweq",)               # no map entry at all; batch 216
PARADIGM_2PL = ("yamu", "namu", "nnamu", "munan", "jyamu", "knyamu",
                "empeenamu")
AMU_SHAPES = re.compile(r"^j?y?[iy]?a[mn]u$")
AMU_LISTED = {"jyamu", "yamu"}          # NEGATIVE: no y..nu form of that stem
YAMO_ALREADY = ("yamo", "yamu")         # ... and his Yamo already holds `yamu`
ULANG_ZERO = ("週期", "慣常")            # NEGATIVE: nothing carries them
ULANG_MEANING = ("反覆", 8, 4)           # POSITIVE: 8 carriers, nearest 4 edits
UNGLOSSED = ("??", "？？")               # SLOWEQ: he could not gloss it himself
UNGLOSSED_HEADS = 11                    # ... and he does that 11 times in 1,967
SLOWEQ_SOLE = 1

JS = r"""() => {
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
          inTruku: inTruku, sole: sole}; }"""


def entries_json():
    s = io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()
    return json.loads(s[s.index("["):s.rindex("]") + 1])


def entries_strings():
    out = []

    def walk(e):
        for k in ("hw", "form", "fr", "en", "zh", "t", "tag", "crossRef"):
            v = e.get(k)
            if isinstance(v, str):
                out.append(v)
            elif isinstance(v, list):
                out.extend(x for x in v if isinstance(x, str))
        for x in (e.get("examples") or []):
            walk(x)
        for sb in (e.get("subs") or []):
            walk(sb)
    for e in entries_json():
        walk(e)
    return "\n".join(out)


def his_tokens():
    import collections
    TOK = re.compile(r"[A-Za-zÇçÀ-ſ'’ʼ\"]+")
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
    """Every word he CARDS, headword and sub-form name. A word he gives an
    entry to is a word he is asserting exists; it cannot be a typing slip."""
    TOK = re.compile(r"[A-Za-zÇçÀ-ſ'’ʼ\"]+")
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
        p = d[0]
        d[0] = i
        for j, y in enumerate(b, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (x != y))
    return d[-1]


def parquet_counts():
    """The outside voice. Returns None if the datasets are not mounted -- a
    missing corpus is a skip, not a failure; the map is not wrong because a
    drive is unplugged."""
    import glob
    if not os.path.isdir(PARQUET_ROOT):
        return None
    try:
        import pyarrow.parquet as pq
    except ImportError:
        return None
    import collections
    c = collections.Counter()
    for d in sorted(glob.glob(os.path.join(PARQUET_ROOT, "*", "Truku"))):
        col = ("formosan" if "ithuan_formosan_text" in d.replace("\\", "/")
               else "transcript")
        for fp in sorted(glob.glob(os.path.join(d, "*.parquet"))):
            try:
                t = pq.read_table(fp, columns=[col])
            except Exception:
                continue
            for s in t.column(col).to_pylist():
                if not s:
                    continue
                s = " " + re.sub(r"[^A-Za-z' ]", " ", s).lower() + " "
                s = re.sub(r"\s+", " ", s)
                for k in list(PQ_FLOOR) + list(PQ_ZERO):
                    if " %s " % k in s:
                        c[k] += 1
                head, tail, _ = PQ_FRAME
                if re.search(r" %s\b[^ ]{0,20}( [^ ]+){0,3} %s "
                             % (head, tail), s):
                    c["frame"] += 1
    return c


def measure():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(BASE)
        pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
        pg.goto(BASE + "?q=%CC%81")
        pg.wait_for_timeout(22000)
        d = pg.evaluate(JS)
        b.close()
    return d


def main():
    bad = []

    def fail(msg):
        bad.append(msg)
        print("FAIL " + msg)

    d = measure()
    tot, ok = d["tot"], d["ok"]
    seen, unv, raw = d["seen"], d["unv"], d["raw"]
    itk, sole = d["inTruku"], d["sole"]
    print("pairs %d/%d = %.4f%%" % (ok, tot, 100.0 * ok / tot))
    print("pale span types %d   pale spans %d   sole-blocked pairs %d over %d"
          % (len(unv), sum(unv.values()), sum(sole.values()), len(sole)))

    # --- 1. the metric
    if tot != DENOM:
        fail("DENOM %d got %d" % (DENOM, tot))
    if ok < FLOOR:
        fail("FLOOR %d got %d" % (FLOOR, ok))

    MM, V = modern_map(), verified()
    AM, AG, BG, PG = sources()
    text = entries_strings()
    cnt = his_tokens()

    # --- 2. the map says what the batch ruled, and the value is two words
    for k, v in RULED.items():
        if MM.get(k) != v:
            fail("MAP %s -> %s got %s" % (k, v, MM.get(k)))
        if " " not in (MM.get(k) or ""):
            fail("MAP %s is no longer a two-word value (%s). The whole ruling "
                 "is that his typewriter joined two words" % (k, MM.get(k)))
        for part in v.split():
            if part not in V:
                fail("%s is a part of the value %s and has left verified.js -- "
                     "attested() splits on the space, so one pale part pales "
                     "the whole span" % (part, v))
    for part, code in PART_CODE.items():
        if V.get(part) != code:
            fail("%s is code %s, was %d -- the parts are what make a two-word "
                 "value dark" % (part, V.get(part), code))
    for w in GONE_VALUES:
        if seen.get(w):
            fail("%s renders %d time(s); the join was ruled away" % (w, seen[w]))
    for k, v in CHAR_INERT.items():
        if char_rules(k) != v:
            fail("char_rules(%s) should give %s unaided, got %s -- that is what "
                 "makes the map entry load-bearing rather than a no-op "
                 "(batch 227)" % (k, v, char_rules(k)))

    # --- 3. the colours the rulings bought
    for v in sorted(set(RULED.values())):
        if not seen.get(v):
            fail("%s renders nowhere at all" % v)
        if unv.get(v) or raw.get(v):
            fail("%s renders pale %s / green %s -- a two-word value has to be "
                 "dark on every part" % (v, unv.get(v, 0), raw.get(v, 0)))
        if sole.get(v):
            fail("%s still sole-blocks %d pairs" % (v, sole[v]))
        if not itk.get(v):
            fail("%s is in no .truku box, so it cannot have bought a pair -- "
                 "the +2 this batch claims would be furniture (batch 223)" % v)

    # --- 4. his book. The join test is the argument, not the raw count.
    for w, n in HIS_FLOORS.items():
        if cnt.get(w, 0) < n:
            fail("he writes `%s` %d times, floor %d -- a count that FALLS is "
                 "the news (batch 209)" % (w, cnt.get(w, 0), n))
    for w, n in HIS_EXACT.items():
        if cnt.get(w, 0) != n:
            fail("he writes `%s` %d times, was %d -- these are hapaxes and the "
                 "whole ruling is priced on their being alone" % (w, cnt.get(w, 0), n))
    heads = his_headwords()
    for clitic, want in JOINS.items():
        got = set(w for w in cnt
                  if w.startswith(clitic) and len(w) - len(clitic) >= 2
                  and cnt.get(w[len(clitic):], 0) >= JOIN_ALONE
                  and w not in heads)
        if got != want:
            fail("the %s+word join test returns %s, batch 231 measured %s -- "
                 "the ruling rests on the join being the ONLY one of its kind "
                 "in his book" % (clitic, sorted(got), sorted(want)))
    for w in JOIN_NOT_CARDED:
        if w not in heads:
            fail("`%s` is no longer one of his headwords. The join test's card "
                 "exclusion is what removes it, and without that leg the test "
                 "returns three rows, not one" % w)
    for s in SENTENCES:
        if s not in text:
            fail("his sentence has changed: %s" % s)
    if PARENTHETICAL not in text:
        fail("his own %r is gone from entries.js -- batch 200's rule needs BOTH "
             "spellings on the page, and it is the whole argument for the "
             "ISOKA ruling" % PARENTHETICAL)

    # --- 5. the record. A ruling that contradicts a refusal cites it (b219).
    for base, needle in CITED:
        p = os.path.join(HERE, base)
        if not os.path.exists(p):
            fail("%s is gone; this batch overturns a pin recorded in it and the "
                 "citation has to stay readable" % base)
        elif needle not in io.open(p, encoding="utf-8").read():
            fail("%s no longer contains %r -- the refusal this batch retired "
                 "must stay on the record, or the supersession is unreadable"
                 % (base, needle))

    # --- 6. the outside voice
    pq = parquet_counts()
    if pq is None:
        print("(ILRDF parquets not mounted -- the corpus half is skipped)")
    else:
        for k, n in PQ_FLOOR.items():
            if pq.get(k, 0) < n:
                fail("the parquets carry `%s` %d times, floor %d -- that split "
                     "count is the outside voice the rulings rest on"
                     % (k, pq.get(k, 0), n))
        for k in PQ_ZERO:
            if pq.get(k, 0):
                fail("NEGATIVE the parquets now carry the JOINED `%s` %d times. "
                     "The ruling rests on the join occurring nowhere but his "
                     "typewriter" % (k, pq[k]))
        if pq.get("frame", 0) < PQ_FRAME[2]:
            fail("`%s ... %s` occurs %d times, floor %d -- his own frame is "
                 "what makes the split a reading of HIS sentence and not just "
                 "a corpus fact" % (PQ_FRAME[0], PQ_FRAME[1],
                                    pq.get("frame", 0), PQ_FRAME[2]))

    # --- 7. the refusals hold, and are still the colour they were refused at
    for w in STILL_PALE:
        if not unv.get(w):
            fail("%s no longer renders pale; a refused word going dark is a "
                 "ruling nobody wrote" % w)
    for w in STILL_GREEN:
        if not raw.get(w):
            fail("%s no longer renders GREEN. Green means no map entry fired, "
                 "and the refusal was that supplying one is itself a spelling "
                 "claim (batch 216)" % w)
        if w in MM.values() or any(k for k in MM if MM[k] == w):
            fail("%s is now a map value; that IS the spelling claim the "
                 "refusal declined to make" % w)

    # --- 8. YAMO. The register spells the paradigm; it does not spell his slot.
    for w in PARADIGM_2PL:
        if w not in AM:
            fail("POSITIVE %s has left the register -- the refusal of `yianu` "
                 "rests on the 2pl paradigm being spelled in full" % w)
    got = set(w for w in AM if AMU_SHAPES.match(w))
    if got != AMU_LISTED:
        fail("NEGATIVE the y/jy+amu shapes listed are %s, batch 231 measured "
             "%s -- a new one arriving is exactly the news that re-opens the "
             "`yianu` refusal" % (sorted(got), sorted(AMU_LISTED)))
    if "yianu" in AM:
        fail("POSITIVE `yianu` is now listed; it was refused on its absence")
    if MM.get(YAMO_ALREADY[0]) != YAMO_ALREADY[1]:
        fail("his Yamo maps to %s, was %s -- the refusal is that sending Yiano "
             "there too would collapse two sub-forms his card distinguishes"
             % (MM.get(YAMO_ALREADY[0]), YAMO_ALREADY[1]))

    # --- 9. ULANG. Batch 204's different-root test, both halves.
    ALL = set(AG) | set(BG) | set(PG)

    def carriers(ch):
        return sorted(w for w in ALL
                      if any(ch in g for g in gl(AG, w) + gl(BG, w) + gl(PG, w)))
    for ch in ULANG_ZERO:
        c = carriers(ch)
        if c:
            fail("NEGATIVE %s now has carriers %s -- ULANG was refused on there "
                 "being none" % (ch, c[:4]))
    ch, floor, near = ULANG_MEANING
    c = carriers(ch)
    if len(c) < floor:
        fail("%s is carried by %d forms, floor %d -- the refusal of `urang` "
             "named that carrier set" % (ch, len(c), floor))
    if c and min(ed("urang", w) for w in c) < near:
        fail("%s now has a carrier %d edits from `urang` (was %d) -- a carrier "
             "coming within reach is what re-opens the refusal"
             % (ch, min(ed("urang", w) for w in c), near))
    for w in ("urang", "ulang"):
        if w in AM:
            fail("POSITIVE %s is now listed; ULANG was refused on its absence" % w)

    # --- 10. SLOWEQ, and the limit it names: he could not gloss it himself.
    E = entries_json()
    slo = [e for e in E if (e.get("hw") or "") == "SLOWEQ"]
    if not slo:
        fail("SLOWEQ is not a headword any more")
    elif (slo[0].get("fr") or "").strip() != UNGLOSSED[0] \
            or (slo[0].get("zh") or "").strip() != UNGLOSSED[1]:
        fail("SLOWEQ now carries a gloss (fr=%r zh=%r). The refusal was that "
             "the gloss test has no left-hand side; a gloss of his is exactly "
             "what re-opens it" % (slo[0].get("fr"), slo[0].get("zh")))
    n = len([e for e in E if (e.get("fr") or "").strip() in ("??", "?", "???")])
    if n != UNGLOSSED_HEADS:
        fail("he leaves %d headwords unglossed, was %d -- that class is the "
             "price of the limit and it is named, not opened (batch 203)"
             % (n, UNGLOSSED_HEADS))
    if sole.get("sruweq", 0) != SLOWEQ_SOLE:
        fail("`sruweq` sole-blocks %d pairs, was %d -- the limit was priced at "
             "that number" % (sole.get("sruweq", 0), SLOWEQ_SOLE))

    # --- 11. audio. Blocked pending a voice; an id is a URL (batch 219).
    # entries.js was NOT touched this batch: the two fixes are display-only.
    ids = audio_ids()
    if len(ids) != AUDIO_IDS:
        fail("AUDIO ids %d, pinned at %d" % (len(ids), AUDIO_IDS))

    print("\n%d assertions failed" % len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
