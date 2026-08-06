# -*- coding: utf-8 -*-
"""batch 235 — the loss is measured, and the scan-first test does not rank it.

Batch 234 left the seam with a standing test saying every blocked pair is held
by a written refusal, and returning 0. That answers "is anything unworked" and
not "what SHAPE is what is left". This batch measures the shape, runs the two
instruments that could still have found a pair over it, and repairs the premises
of three refusals that survive the repair.

**0 pairs.** The metric HOLDS at 5,346 / 5,429 = 98.4712%. No file that ships
changed: `entries.js`, `modern_map.js` and `verified.js` are untouched and the
audio id set stands at 5,134.

1. The remaining loss, by shape: 79 + 4 + 0
------------------------------------------------------------------------------
Of the 83 pairs still blocked, **79 are held by a single pale type, 4 by exactly
two, and none by three or more.** The four two-type rows are batch 230's four
confirmed refusals, unchanged; that batch found six, ruled two, and the seam it
opened is now empty. There is no third tier behind it — which is worth pinning,
because the Target section's standing warning is that a ranking hides the pairs
it cannot see, and this says there is nothing left of that shape to hide.

2. Rarity is a property of the whole seam, not a signal
------------------------------------------------------------------------------
Batch 213's test — "a token appearing once in a book that repeats itself is a
candidate for the scan, not for the register" — is cheap per row and paid four
times in batch 229. Asked as a RANKING over what is left, it collapses: **56 of
the 67 sole-blocker types have his tokens totalling two occurrences or fewer**,
holding 58 of the 79 pairs. A pale blocker is a derived slot he wrote once;
being rare is what the class IS. Sorting by it sorts nothing.

(Two of the 67 are reached by no map key at all — `mngusyeh` and `sruweq`, both
GREEN, `sruweq` being the one batch 231 named. A map-only join drops those
silently, so they are counted out loud rather than left to shrink the
denominator quietly: batch 230's rule about the eleven pale values a map-only
lookup cannot see.)

What does discriminate is the crossing batch 229 actually used — a rare token of
his one edit, or one glyph, from a token he writes ten times or more. Over the
sole blockers that returns 14 rows in 8 types, and every one already carries a
written refusal, exactly as batch 234's classifier predicted. Two of those
refusals were written before batch 213 existed and had never read the page, so
they are the two this batch re-opens (§3, §4). Both survive.

3. `narung` — the refusal said "no candidate", and his own card is one
------------------------------------------------------------------------------
His `nalong` is a hapax, sole blocker of one pair, on the XETI card:

    Xea ka mnangal nalong, mxeti ko bi ka yako
    C'est lui qui a obtenu le prix ; moi, je venais bien après.
    得獎的是他；我嘛，排在他後面很多。

It was refused as "no card, no candidate". **The card exists.** His MALONG, 76
pages away, is tagged `(R)` and glossed "Décoration (?)" with a note that reads
like the sentence's own commentary: *une rondelle d'ivoire rare et très prisée
… marquant le mérite — et donc l'autorité — suite à un acte de bravoure*. That
IS "le prix". Batch 229's rule about searching the root's slots book-wide rather
than the neighbouring ones, arriving as a repair instead of as a ruling.

So the premise is false and the verdict still holds, on three legs:

* **The page reads `n`.** Scan 364 is book page 343; at 20× the initial of
  `nalong` has two legs, identical to the `n` of `ngal` in `mnangal` on the same
  line and unlike its `m`. Batch 212 decides where the fix goes: this is a
  reading the page really carries, so `entries.js` is untouched.
* **Darkening it means swapping his initial `n` for an `m`.** Batch 216 refuses
  exactly that — his initial consonant takes a modern reflex, never another
  consonant — and batch 234 refused the same move on `kyoqan → tuyuqan`.
* **There is nothing to swap TO.** `narung` is in no source. The register has
  **zero** rows glossed 象牙, and of the listed words within two edits of
  `narung` not one carries the sense: `arung` 穿山甲, `marung` and `harung`
  人名（男）, `sarung` 苦瓜臉. His MALONG head is already dark on `marung`, which
  is glossed only as a name — correct under batch 225, and 0 pairs either way,
  since that card has no examples and its head is furniture.

4. `kahui` — a word he CARDS cannot be a slip
------------------------------------------------------------------------------
His `kaxoi` is the other pre-213 refusal, and the scan question closes without a
crop. Batch 231: **a word he gives a headword to is a word he asserts exists.**
KAXOI is a headword, `( = R. Taroko ?)`, glossed *Fille de joie - prostituée* /
風塵女子－妓女, with a sub-form `Mkaxoi` 淪為妓女 and a sentence under each. The
register side is unchanged and stated as a property: 妓, 娼, 嫖 and 賣春/賣身/
風塵 return **0 rows across all three gloss files**, nothing at all sits within
one edit of `kahui`, and the two 淫 rows are `mngeangal` 淫亂 and `sgsapat` 姦淫
— different roots, so batch 204 leaves nothing to respell.

5. `shkun` — what the refusal searched, stated
------------------------------------------------------------------------------
The largest sole blocker (2 pairs) is his `Sl'xqon`/`Slx'qon` 舔. Batch 214
repointed it to the `-un` slot of `shik` and left it pale because "nothing
decides between `shkun` and `shikun`". Batch 230 says to check what a refusal
searched, and batch 220 shows the search that would decide it: ask the register
which forms of the syncopated stem it spells. Run over all three files, the
`shik` family is there — `shik` 吻, `pshik` 被…吻, `msshik` 互吻, `smhik` 在吻 —
and **not one suffixed slot of it is listed, in either stem**: `shkun`,
`shikun`, `shkan`, `shikan`, `shki`, `shiki` are all absent. Batch 224 is why
that is a tie and not a verdict: silence is evidence where the slot is spelled
for the same stem, and here it is spelled for neither candidate. The refusal
stands with its search now written down.

6. The SPLIT sweep — the mirror of batch 231, closed at zero
------------------------------------------------------------------------------
Batch 231 found the JOIN direction: his typewriter fusing a clitic to its host,
where the map value has to be two words. The split direction had no mention
anywhere in the record — two adjacent tokens of his whose values, concatenated,
are a listed modern word, with at least one side pale. If that were real the
pale side would not be a spelling question at all.

Over the 5,367 `.truku` boxes holding two or more spans it returns **0**. That
is a controlled zero, from the data side (batch 232): dropping only the pale
requirement, the same sweep finds **1,440** adjacent all-dark joins, so the
instrument sees joins and the emptiness is about the pale, not about the code.
Kept as a negative result with the standing of `freezesweep.py`, `tail221.py`
and `premise231.py`.

    python tools/orthography/logs/dom235.py       # site served at :8765
"""
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
URL = "http://127.0.0.1:8765/"

# ---- the pins -------------------------------------------------------------
FLOOR = 5346                      # pairs; HELD, this batch buys none
DENOM = 5429
AUDIO_IDS = 5134

# section 1 -- the shape of the loss
SOLE_TYPES = 67
SOLE_PAIRS = 79
TWO_TYPE = 4                      # batch 230's four confirmed refusals
THREE_PLUS = 0                    # there is no tier behind them
TWO_CLUSTERS = (("tbasyaq", "tibasyaq"), ("krikut", "nrikut"),
                ("dmtbasyaq", "dmtsapat"), ("snuk", "thiy"))

# section 2 -- rarity does not rank
RARE_MAX = 2                      # "a book that repeats itself" (batch 213)
RARE_FLOOR = 55                   # of 67; pinned as a floor, not equality
NO_MAP_KEY = ("mngusyeh", "sruweq")      # green: no map entry fires at all

# section 3 -- narung
HIS, VAL = "nalong", "narung"
HIS_N = 1                         # a hapax; a second occurrence is news
CARD, CARD_VAL = "malong", "marung"      # his MALONG (R), already dark
IVORY = re.compile(r"象牙")
SENSE = re.compile(r"象牙|裝飾|飾品|首飾|徽章|功績|英勇")

# section 4 -- kahui
HIS2, VAL2 = "kaxoi", "kahui"
CARD2, SUB2 = "KAXOI", "Mkaxoi"
WHORE = re.compile(r"妓|娼|嫖|賣春|賣身|風塵")
RIVALS = ("mngeangal", "sgsapat")        # the 淫 rows: different roots

# section 5 -- shkun
LICK_FAMILY = ("shik", "pshik", "msshik", "smhik")
LICK_SLOTS = ("shkun", "shikun", "shkan", "shikan", "shki", "shiki")

# section 6 -- the split sweep
SPLIT_BOXES = 5367                # floor
JOIN_PALE = 0
JOIN_ANY_FLOOR = 1000             # measured 1440; the positive control

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


def glosses(S, w):
    out = []
    for D in S[1:]:
        g = D.get(w) or []
        out += [str(x) for x in (g if isinstance(g, list) else [g])]
    return out


def known(S):
    """every word the register knows, across ALL sources -- batch 230: a zero
    from one gloss file is not a zero from the register. `attested_modern`
    alone would miss `sgsapat`, which is bible-only and is the word batch 204
    ruled."""
    out = set(S[0])
    for D in S[1:]:
        out |= set(D)
    return out


def carriers(S, pat):
    """every word any of the three files glosses with pat."""
    return sorted(w for w in known(S) if any(pat.search(g)
                                             for g in glosses(S, w)))


def audio_ids():
    ids = set()

    def walk(n):
        for x in (n.get("examples") or []):
            if x.get("a"):
                ids.add(x["a"])
        for s in (n.get("subs") or []):
            walk(s)
    for e in entries_json():
        walk(e)
    return ids


def his_fields(E):
    for e in E:
        hw = e.get("hw") or ""
        yield hw, "HEAD", hw, e.get("fr")
        for x in e.get("examples") or []:
            yield hw, "EX", x.get("t"), x.get("fr")
        for sb in e.get("subs") or []:
            yield hw, "SUB", sb.get("form"), sb.get("fr")
            for x in sb.get("examples") or []:
                yield hw, "SUBEX", x.get("t"), x.get("fr")


def counts(E):
    """every Truku token he writes, with its occurrence count."""
    c = {}
    for _, _, t, _ in his_fields(E):
        for w in re.findall(r"[a-zA-Zç'\"À-ü]+", str(t or "")):
            w = w.lower()
            c[w] = c.get(w, 0) + 1
    return c


def ed(a, b):
    if abs(len(a) - len(b)) > 2:
        return 9
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        d[i][0] = i
    for j in range(len(b) + 1):
        d[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1,
                          d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    return d[len(a)][len(b)]


# ---- the DOM --------------------------------------------------------------
def measure():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        pg.goto(URL)
        pg.evaluate(
            "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
        pg.goto(URL + "?q=%CC%81")
        pg.wait_for_timeout(22000)
        d = pg.evaluate(r"""() => {
          const SEL = 'span.w-mod, span.w-unv, span.w-raw';
          let tot = 0, ok = 0;
          const unv = {}, blocked = [], seq = [];
          document.querySelectorAll('#results > article.entry').forEach(c => {
            c.querySelectorAll('.truku').forEach(box => {
              const sp = [...box.querySelectorAll(SEL)];
              if (!sp.length) return;
              tot++;
              const pairs = sp.map(s => [(s.textContent||'').trim()
                                           .toLowerCase(),
                                         s.classList.contains('w-mod')?1:0]);
              if (sp.length > 1) seq.push(pairs);
              if (sp.every(s => s.classList.contains('w-mod'))) ok++;
              else blocked.push([...new Set(pairs.filter(p => !p[1])
                                                 .map(p => p[0]))].sort());
            });
            c.querySelectorAll(SEL).forEach(s => {
              if (!s.classList.contains('w-unv')) return;
              const t = (s.textContent || '').trim().toLowerCase();
              unv[t] = (unv[t] || 0) + 1;
            });
          });
          return {tot: tot, ok: ok, unv: unv, blocked: blocked, seq: seq};
        }""")
        b.close()
    return d


def main():
    d = measure()
    MM, VER, S = modern_map(), verified(), sources()
    E = entries_json()
    att, KNOWN = S[0], known(S)

    print("PAIRS %d / %d = %.4f%%   FLOOR %d"
          % (d["ok"], d["tot"], 100.0 * d["ok"] / d["tot"], FLOOR))
    ck(d["ok"] >= FLOOR, "FLOOR %d: the metric fell to %d" % (FLOOR, d["ok"]))
    ck(d["tot"] == DENOM, "the denominator is %d, pinned %d"
       % (d["tot"], DENOM))
    ck(len(audio_ids()) == AUDIO_IDS, "the audio id set is %d, expected %d"
       % (len(audio_ids()), AUDIO_IDS))

    # --- 1. the shape of the loss
    sole = {}
    two = {}
    deep = 0
    for bad in d["blocked"]:
        if len(bad) == 1:
            sole[bad[0]] = sole.get(bad[0], 0) + 1
        elif len(bad) == 2:
            two[tuple(bad)] = two.get(tuple(bad), 0) + 1
        else:
            deep += 1
    print("BLOCKED %d = sole %d types/%d pairs | two-type %d | 3+ %d"
          % (len(d["blocked"]), len(sole), sum(sole.values()),
             sum(two.values()), deep))
    ck(len(sole) == SOLE_TYPES, "sole-blocker types %d, pinned %d"
       % (len(sole), SOLE_TYPES))
    ck(sum(sole.values()) == SOLE_PAIRS, "sole-blocked pairs %d, pinned %d"
       % (sum(sole.values()), SOLE_PAIRS))
    ck(sum(two.values()) == TWO_TYPE, "two-type blocked pairs %d, pinned %d"
       % (sum(two.values()), TWO_TYPE))
    ck(deep == THREE_PLUS,
       "%d pair(s) are now blocked by THREE or more types, where this batch "
       "measured none. A third tier has appeared behind the two-type seam and "
       "no ranking in the project reports it." % deep)
    missing = [c for c in TWO_CLUSTERS if tuple(sorted(c)) not in two]
    ck(not missing,
       "a two-type cluster this batch pinned has left the book (%s): batch "
       "230 confirmed all four as refusals, so one healing is news"
       % "; ".join("+".join(c) for c in missing))

    # --- 2. rarity does not rank
    C = counts(E)
    inv = {}
    for k, v in MM.items():
        inv.setdefault(v, []).append(k)
    rare, nomap = [], []
    for w in sole:
        if not inv.get(w):
            nomap.append(w)
            continue
        n = sum(C.get(h, 0) for h in inv[w])
        if 0 < n <= RARE_MAX:
            rare.append(w)
    print("RARE sole blockers (his tokens <= %dx): %d of %d types, %d of %d "
          "pairs | unjoinable %d %s"
          % (RARE_MAX, len(rare), len(sole),
             sum(sole[w] for w in rare), sum(sole.values()),
             len(nomap), ",".join(sorted(nomap))))
    ck(set(nomap) <= set(NO_MAP_KEY),
       "a sole blocker has appeared that no map key reaches (%s). A map-only "
       "join drops those silently (batch 230), so the rare/frequent split "
       "below is measured over fewer types than it reports."
       % ", ".join(sorted(set(nomap) - set(NO_MAP_KEY))))
    ck(len(rare) >= RARE_FLOOR,
       "only %d of %d sole blockers are rare, where this batch measured %d. "
       "Rarity was pinned as a property of the whole seam; if it has become "
       "discriminating, batch 213's test can rank the pale after all."
       % (len(rare), len(sole), RARE_FLOOR))

    # --- 3. narung
    n_his = sum(len(re.findall(r"(?i)(?<![a-z])%s(?![a-z])" % HIS, str(t or "")))
                for _, _, t, _ in his_fields(E))
    ck(n_his == HIS_N,
       "his %s occurs %d times, pinned %d: a second occurrence is a second "
       "reading of the scan" % (HIS, n_his, HIS_N))
    ck(MM.get(HIS) == VAL, "his %s maps to %s, pinned %s"
       % (HIS, MM.get(HIS), VAL))
    ck(VAL not in VER,
       "FAIL %s is DARK now. It was refused because the page reads an n, "
       "darkening it needs his initial swapped for an m (batch 216), and no "
       "listed word carries the sense anyway. A value that goes dark "
       "overturns that, so say what attested it." % VAL)
    ck(d["unv"].get(VAL, 0) > 0,
       "%s renders no pale span: the row this batch refused has left the book"
       % VAL)
    ck(sole.get(VAL, 0) >= 1, "%s is no longer a sole blocker" % VAL)
    # the repaired premise: his own card IS the candidate
    card = [e for e in E if (e.get("hw") or "").lower() == CARD]
    ck(card and "ivoire" in str(card[0].get("fr", "")).lower(),
       "his MALONG card has lost its ivory note: that note is the whole "
       "repair -- the refusal said 'no card, no candidate' and the card is "
       "the candidate")
    ck(MM.get(CARD) == CARD_VAL and CARD_VAL in VER,
       "his %s is no longer dark on %s: the head the pale hapax would have "
       "to follow" % (CARD, CARD_VAL))
    # the negative half, as a property of the register (batch 229)
    ck(not carriers(S, IVORY),
       "the register now glosses a word 象牙 (%s): there is a candidate for "
       "his merit disc where this batch measured none"
       % ", ".join(carriers(S, IVORY)[:4]))
    near = [w for w in KNOWN if ed(VAL, w) <= 2 and any(
        SENSE.search(g) for g in glosses(S, w))]
    ck(not near,
       "a listed word within two edits of %s now carries the ornament sense "
       "(%s): the refusal's third leg is gone and the pair can be re-priced"
       % (VAL, ", ".join(sorted(near)[:4])))
    print("NARUNG hapax %d | %s -> %s dark %s | 象牙 rows %d | near-sense %d"
          % (n_his, CARD, CARD_VAL, CARD_VAL in VER,
             len(carriers(S, IVORY)), len(near)))

    # --- 4. kahui
    kx = [e for e in E if (e.get("hw") or "") == CARD2]
    ck(len(kx) == 1, "his %s card is gone: batch 231's rule is what closes "
                     "the scan question here -- a word he cards is not a slip"
       % CARD2)
    ck(kx and any((sb.get("form") or "") == SUB2 for sb in kx[0].get("subs")
                  or []), "his %s sub-form is gone from the %s card"
       % (SUB2, CARD2))
    ck(MM.get(HIS2) == VAL2 and VAL2 not in VER,
       "FAIL %s is no longer pale on %s. It was refused because 妓/娼/嫖 "
       "return no register row at all and nothing sits within one edit of it; "
       "a value that goes dark overturns that, so say what attested it."
       % (HIS2, VAL2))
    ck(not carriers(S, WHORE),
       "the register now glosses a word 妓/娼/嫖/賣春 (%s): the sense the "
       "refusal says is absent has arrived"
       % ", ".join(carriers(S, WHORE)[:4]))
    one = [w for w in KNOWN if ed(VAL2, w) <= 1]
    ck(not one, "a listed word now sits within one edit of %s (%s)"
       % (VAL2, ", ".join(sorted(one)[:4])))
    ck(all(any("淫" in g for g in glosses(S, w)) for w in RIVALS),
       "a 淫 rival root (%s) has lost its gloss: the different-root half of "
       "the refusal (batch 204) must be re-read. Both are bible-only, so "
       "this leg has to read all three files and not attested_modern."
       % ", ".join(w for w in RIVALS
                   if not any("淫" in g for g in glosses(S, w))))
    print("KAHUI card %s + %s | 妓/娼/嫖 rows %d | within 1 edit %d"
          % (CARD2, SUB2, len(carriers(S, WHORE)), len(one)))

    # --- 5. shkun
    gone = [w for w in LICK_FAMILY if w not in KNOWN]
    ck(not gone,
       "the shik family has lost %s: batch 214's root is what makes this a "
       "tie between two spellings of one slot rather than an empty candidate "
       "list (batch 217)" % ", ".join(gone))
    listed = [w for w in LICK_SLOTS if w in KNOWN]
    ck(not listed,
       "FAIL the register now spells a suffixed slot of the shik stem (%s). "
       "It was refused because neither shkun nor shikun is listed and batch "
       "224's silence cannot break a tie it applies to both; one of them "
       "appearing is exactly the news that decides it." % ", ".join(listed))
    print("SHKUN family listed %d/%d | suffixed slots listed %d/%d"
          % (len(LICK_FAMILY) - len(gone), len(LICK_FAMILY),
             len(listed), len(LICK_SLOTS)))

    # --- 6. the split sweep, with its positive control
    pale = any_ = 0
    rows = []
    for sp in d["seq"]:
        for i in range(len(sp) - 1):
            (a, da), (b, db) = sp[i], sp[i + 1]
            if " " in a or " " in b or not a or not b:
                continue
            j = re.sub(r"[^a-z']", "", a + b)
            if len(j) < 4 or j not in att:
                continue
            any_ += 1
            if not (da and db):
                pale += 1
                rows.append("%s+%s=%s" % (a, b, j))
    print("SPLIT boxes %d | joins listed: any %d, pale-side %d"
          % (len(d["seq"]), any_, pale))
    ck(len(d["seq"]) >= SPLIT_BOXES, "the multi-span box count fell to %d "
       "from %d: the sweep is looking at less of the book"
       % (len(d["seq"]), SPLIT_BOXES))
    ck(any_ >= JOIN_ANY_FLOOR,
       "the positive control fell to %d all-dark joins from %d: an empty "
       "sweep and a broken sweep have the same output (batch 232), and this "
       "leg is what separates them" % (any_, JOIN_ANY_FLOOR))
    ck(pale == JOIN_PALE,
       "%d adjacent pale-side span pair(s) now join into a listed word (%s): "
       "the split direction has a row and the pale side may not be a spelling "
       "question at all" % (pale, ", ".join(sorted(set(rows))[:4])))

    for f in fails:
        print("FAIL " + f)
    print("\n%d assertions failed" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
