# -*- coding: utf-8 -*-
"""batch 234 — the last unworked sole blocker, found by pricing a label.

The Target section says every blocker tier is closed and the 83 pairs still
blocked are held by words with a written refusal, so the next gain has to come
from new evidence. Two things follow from that and both are done here: the one
outside instrument that might still hold new evidence is measured and closed,
and the claim "they all have a written refusal" is priced instead of repeated.
Pricing it found exactly one row where it was false.

**0 pairs.** The metric HOLDS at 5,346 / 5,429. Nothing was ruled; one row was
refused, two sweeps are closed with negative results, and one new standing test
is added.

1. The ILRDF e-dictionary is closed AT THE PALE, by measurement
------------------------------------------------------------------------------
Batch 182 established that the online dictionary "attests NOTHING new" over its
first 611 lookups. That was a statement about the lookups made. Asked of the
pale specifically — the only place an attestation could still buy a pair — it
is sharper: of the **146 map values that render on a pale key, 131 have already
been asked and every one is a miss. Not one hit, anywhere in the pale.**

The 15 never asked are not a queue either:

* **10 are FRENCH** — `grand`, `grandeur`, `beau`, `savoir`, `vivant`,
  `volant`, and the char rules' own output on his French: `connaissance →
  cunnaissance`, `matin → macin`, `pour → puur`, `rougeur → ruugeur`. Section 3.
* **5 are Truku and every one already has a written record**: `knbuyu` (batch
  225's KUBWI), `mqlaq` (batch 218's reverted freeze, and the 3 pairs it cost),
  `rngiyan` (batch 220's refusal off the register's silence), `shkun`,
  `smul` (batch 227's reverted freeze). All five are DERIVED forms, and the
  instrument indexes HEADWORDS — `tksaw` and `gmquwaq` come back 無搜尋結果
  while their roots are there in full. It cannot reach them by construction.

So there was never a lookup to make. This is a negative result and it is kept,
with the standing of `freezesweep.py`, `tail221.py` and `premise231.py`: the
assertion here is `ASKED_HITS == 0` and that no NEW pale value appears unasked,
which is the news that would re-open it.

2. `kyuqan` — the one sole blocker whose only mention was a parenthesis
------------------------------------------------------------------------------
Every one of the 67 sole-blocker types has a prior mention somewhere in the
record. That reads as "all worked", and it is a LABEL (batch 228). Classify the
mentions by whether any of them sits in a refusal-shaped context and exactly one
type comes back unworked: `kyuqan`, his `kyoqan`, sole blocker of one pair,
mentioned once ever — inside a list of words a batch had NOT re-derived, as the
parenthesis "(his crachats; the register spits with halus)".

His row is one sentence, on the SA'SO card:

    Wada na kxdoon kyoqan ka bobo na! Sa'so bi !
    Il a couvert sa mère de crachats ! C'est honteux !   他朝母親吐了滿臉口水！

**The scan first** (batch 213/229: a token appearing once in a book that repeats
itself is a candidate for the scan, and it costs one crop). Scan page 264 is
book page 243; the SA'SO line is the last on the page, and at 6× the initial is
the same `k` as `kxdoon` and `ka` on that same line — arms, no crossbar. The
page carries `kyoqan`. `entries.js` is faithful and is untouched.

**His own book supplies the meaning, so this is not a gloss question.** His
TUYOQ card is "Salive - cracher" and its sub-form `Tyoqan` is "Crachoir -
crachat - action de cracher" — the hapax's sense exactly. `tuyuq` is attested
and glossed 痰; `tyoqan → tuyuqan` is already DARK at code 2. What is in doubt
is only his `k-`, and three routes out of it are each refused:

* **`kyoqan → tuyuqan`** — swapping his `k` for a `t` is a lexical substitution
  wearing a respelling's clothes (batch 216, where dropping the L of `lg'loq`
  was refused although `gluq` carried his gloss verbatim). His initial consonant
  takes a modern reflex, never another consonant.
* **`kyoqan → ktuyuqan`**, restoring the syncopated `tu` as batch 219 restored
  the `g` of `tglgli` — but that `g` was written by eight dark slots of his own
  card, and no slot anywhere writes this. `ktuyuqan` is in no source, so the
  span would stay pale: a new spelling claim that buys nothing.
* **Leaving it and calling the pallor a gap** — refused by batch 224's sister
  test, which is what makes silence evidence. The register spells the `k…an`
  slot for other stems (`kbyuan` 讓…雜草叢生, `kyuhan` 已擦傷), and spells no
  `k-` form of this one. The negative half stated as batch 229 requires it —
  as a property of the carriers, not as a list: of the 58 register words whose
  gloss carries 口水/唾/痰, the `tuyuq` family is there in full and **not one
  member of it takes a `k-`**. What the register does have for "covered in
  saliva" is `khalus` 沾滿唾液, off `halus` — a different root (batch 204), and
  a `k-` word, which is the point: the slot exists and this stem is not in it.
  There is no respelling to find.

So `kyuqan` stays pale, the pair stays blocked, and the refusal is written down
where the next batch will grep it.

3. His French inside a Truku field earns a map entry, and it is INERT
------------------------------------------------------------------------------
Ten map values are French words. They are not a defect to clean: every one
renders **zero spans**, and the reason is already in the app. Six come from the
`t == fr` demonstration rows of his AN (3) card (`Paro = Grand; Knplaan =
Grandeur`), which `metaLine()` renders with no spans at all — the six rows the
denominator already excludes. The other two come from his parentheticals,
`xandolu (=Volant)` on G'LEQ and `Pqboan (= contraction pour: …)` on QBOBO,
which the page files as apparatus (batch 208).

The consequence is a measurement one, and it is why they are pinned here: a
pale census taken from the MAP counts ten values the DOM does not have, so the
real pale-value seam is 136 and not 146. Batch 219's rule arriving in the
cheapest possible place — the map is never evidence about colour.

4. The classification is left behind as a standing test
------------------------------------------------------------------------------
`unworked()` re-runs section 2's cut at suite time: every sole blocker, every
map key that reaches it, against CLAUDE.md, the three notes files,
`manual_map.json` and every log. After this batch it returns **0**. It fires
when a sole blocker turns up whose record contains no refusal-shaped sentence —
either a new one arriving from a ruling elsewhere, or this batch's own refusal
being deleted. That is the guard the "every tier is closed" claim never had.

    python tools/orthography/logs/dom234.py       # site served at :8765
"""
import collections
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
SOLE_TYPES = 67

# section 1 -- the e-dictionary at the pale
ASKED_HITS = 0                    # the durable claim: no pale value is listed
NEVER_ASKED = ("beau", "cunnaissance", "grand", "grandeur", "knbuyu", "macin",
               "mqlaq", "puur", "rngiyan", "ruugeur", "savoir", "shkun",
               "smul", "vivant", "volant")

# section 3 -- the French leakage
FRENCH = ("beau", "cunnaissance", "grand", "grandeur", "macin", "puur",
          "ruugeur", "savoir", "vivant", "volant")
TFR_ROWS = 6                      # his AN (3) demonstration rows, t == fr

# section 2 -- the refusal
HIS = "kyoqan"
VAL = "kyuqan"
HIS_OCCURRENCES = 1               # a hapax; a second occurrence is news
SIB, SIB_VAL = "tyoqan", "tuyuqan"   # his Tyoqan, DARK at code 2
ROOT, ROOT_ZH = "tuyuq", "痰"
SLOT_SISTERS = ("kbyuan", "kyuhan")  # the k...an slot, spelled for other stems
RIVAL, RIVAL_ZH = "khalus", "沾滿唾液"
SPIT = re.compile(r"口水|唾|痰")
KSTEM = re.compile(r"^k.*yuq")       # a k- form of his root: the negative half

# section 4 -- the standing test
UNWORKED = 0
REFUSAL = re.compile(
    r"refus|different root|settled class|no candidate|nothing to respell|"
    r"stays pale|keeps? the inferred|cannot|is correct and|reverted|"
    r"deliberat|no source|silence", re.I)

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


def edictionary():
    return json.load(io.open(os.path.join(ORTH, "edictionary_trv.json"),
                             encoding="utf-8"))


def record():
    """CLAUDE.md, the notes, manual_map.json and every log, as lines."""
    out = []
    for p in ("CLAUDE.md", ".claude/notes/batch-log.md",
              ".claude/notes/map-history.md", ".claude/notes/app-behaviour.md",
              "tools/orthography/manual_map.json"):
        f = os.path.join(H, p)
        if os.path.exists(f):
            out.append((p, io.open(f, encoding="utf-8",
                                   errors="replace").read().splitlines()))
    for n in sorted(os.listdir(HERE)):
        if n.endswith(".py"):
            out.append((n, io.open(os.path.join(HERE, n), encoding="utf-8",
                                   errors="replace").read().splitlines()))
    return out


def gl(D, w):
    g = D.get(w) or []
    return g if isinstance(g, list) else [g]


def glosses(S, w):
    """every gloss string any of the three files carries for w."""
    return [str(x) for D in S[1:] for x in gl(D, w)]


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
    """(headword, where, truku, fr) for every field of his that carries text."""
    for e in E:
        hw = e.get("hw") or ""
        yield hw, "HEAD", hw, e.get("fr")
        for x in e.get("examples") or []:
            yield hw, "EX", x.get("t"), x.get("fr")
        for sb in e.get("subs") or []:
            yield hw, "SUB", sb.get("form"), sb.get("fr")
            for x in sb.get("examples") or []:
                yield hw, "SUBEX", x.get("t"), x.get("fr")


def unworked(sole, MM):
    """sole blockers with no refusal-shaped sentence anywhere in the record."""
    inv = collections.defaultdict(list)
    for k, v in MM.items():
        inv[v].append(k)
    DOC = record()
    out = []
    for w in sorted(sole):
        names = [w] + sorted(inv.get(w, []))
        pat = re.compile("|".join(r"(?<![a-z])" + re.escape(x) + r"(?![a-z])"
                                  for x in names))
        seen = False
        for _, lines in DOC:
            for i, ln in enumerate(lines):
                if pat.search(ln) and REFUSAL.search(
                        "\n".join(lines[max(0, i - 6):i + 7])):
                    seen = True
                    break
            if seen:
                break
        if not seen:
            out.append(w)
    return out


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
          const seen = {}, unv = {}, raw = {}, sole = {};
          document.querySelectorAll('#results > article.entry').forEach(c => {
            c.querySelectorAll('.truku').forEach(box => {
              const sp = [...box.querySelectorAll(SEL)];
              if (!sp.length) return;
              tot++;
              if (sp.every(s => s.classList.contains('w-mod'))) ok++;
              else {
                const bad = [...new Set(sp.filter(
                    s => !s.classList.contains('w-mod'))
                  .map(s => (s.textContent||'').trim().toLowerCase()))];
                if (bad.length === 1) sole[bad[0]] = (sole[bad[0]] || 0) + 1;
              }
            });
            c.querySelectorAll(SEL).forEach(s => {
              const t = (s.textContent || '').trim().toLowerCase();
              seen[t] = (seen[t] || 0) + 1;
              if (s.classList.contains('w-unv')) unv[t] = (unv[t] || 0) + 1;
              if (s.classList.contains('w-raw')) raw[t] = (raw[t] || 0) + 1;
            });
          });
          return {tot: tot, ok: ok, seen: seen, unv: unv, raw: raw, sole: sole};
        }""")
        b.close()
    return d


def main():
    d = measure()
    MM, VER, S, ED = modern_map(), verified(), sources(), edictionary()
    E = entries_json()
    att = S[0]

    print("PAIRS %d / %d = %.4f%%   FLOOR %d"
          % (d["ok"], d["tot"], 100.0 * d["ok"] / d["tot"], FLOOR))
    ck(d["ok"] >= FLOOR, "FLOOR %d: the metric fell to %d" % (FLOOR, d["ok"]))
    ck(d["tot"] == DENOM, "the denominator is %d, pinned %d"
       % (d["tot"], DENOM))
    ck(len(audio_ids()) == AUDIO_IDS, "the audio id set is %d, expected %d"
       % (len(audio_ids()), AUDIO_IDS))
    ck(len(d["sole"]) == SOLE_TYPES, "sole-blocker types %d, pinned %d"
       % (len(d["sole"]), SOLE_TYPES))

    # --- 1. the e-dictionary, at the pale
    pale_vals = sorted(set(MM.values()) - set(VER))
    hits = [w for w in pale_vals if ED.get(w)]
    never = [w for w in pale_vals if w not in ED]
    print("E-DICT pale values %d | asked %d | HITS %d | never asked %d"
          % (len(pale_vals), len(pale_vals) - len(never), len(hits),
             len(never)))
    ck(len(hits) == ASKED_HITS,
       "the e-dictionary now LISTS a pale value (%s): batch 182's negative "
       "result is re-opened and the word may be attested"
       % ", ".join(hits[:4]))
    ck(set(never) <= set(NEVER_ASKED),
       "a pale value has appeared that was never asked of the e-dictionary: %s"
       % ", ".join(sorted(set(never) - set(NEVER_ASKED))[:6]))

    # --- 3. the French leakage is inert
    rendered = [w for w in FRENCH if d["seen"].get(w)]
    ck(not rendered, "a French map value renders as a span (%s): it is no "
                     "longer inert and the pale census must count it"
       % ", ".join(rendered))
    ck(all(w in set(MM.values()) for w in FRENCH),
       "a French map value left the map: the leakage this log prices has "
       "changed shape")
    tfr = [t for _, _, t, fr in his_fields(E)
           if t and fr and str(t).strip().rstrip(".!? ")
           == str(fr).strip().rstrip(".!? ")]
    ck(len(tfr) == TFR_ROWS, "the t == fr rows number %d, pinned %d"
       % (len(tfr), TFR_ROWS))
    print("FRENCH %d values, %d rendering | t==fr rows %d"
          % (len(FRENCH), len(rendered), len(tfr)))

    # --- 2. the refusal
    ck(MM.get(HIS) == VAL, "his %s maps to %s, pinned %s"
       % (HIS, MM.get(HIS), VAL))
    ck(VAL not in VER,
       "FAIL %s is DARK now. It was refused because the register spells no "
       "k- form of his stem while spelling that slot for other stems, and "
       "the 口水 family is the different root halus. A value that goes dark "
       "overturns the refusal, so say what attested it." % VAL)
    ck(d["unv"].get(VAL, 0) > 0, "%s renders no pale span at all: the row "
       "this batch refused has left the book" % VAL)
    ck(d["sole"].get(VAL, 0) >= 1, "%s is no longer a sole blocker; the "
       "refusal was written against one blocked pair" % VAL)
    # his page: a hapax, beside a sibling that carries the sense
    n_his = sum(len(re.findall(r"(?i)(?<![a-z])%s(?![a-z])" % HIS, str(t or "")))
                for _, _, t, _ in his_fields(E))
    ck(n_his == HIS_OCCURRENCES,
       "his %s occurs %d times, pinned %d: a second occurrence is a second "
       "reading of the scan" % (HIS, n_his, HIS_OCCURRENCES))
    sib = [fr for _, _, t, fr in his_fields(E)
           if str(t or "").strip().lower() == SIB]
    ck(any("crachat" in str(x).lower() for x in sib),
       "his %s no longer glosses as a crachat: the sense the refusal leans "
       "on has moved" % SIB)
    ck(MM.get(SIB) == SIB_VAL and SIB_VAL in VER,
       "his %s is no longer dark on %s -- the positive half of the refusal, "
       "that the meaning is settled and only his k- is in doubt"
       % (SIB, SIB_VAL))
    ck(ROOT in att and any(ROOT_ZH in g for g in glosses(S, ROOT)),
       "%s lost its %s gloss: his TUYOQ card's root is what makes this a "
       "question about a prefix and not about a meaning" % (ROOT, ROOT_ZH))
    # batch 224: silence refuses only where the slot is spelled for others
    miss = [w for w in SLOT_SISTERS if w not in att]
    ck(not miss, "the k...an slot is no longer spelled for other stems (%s "
                 "gone): the register's silence about his stem stops being "
                 "evidence and becomes an empty candidate list" % ", ".join(miss))
    # batch 229: the negative half, as a regex over the whole register
    carriers = sorted(w for w in att
                      if any(SPIT.search(g) for g in glosses(S, w)))
    spells = [w for w in carriers if KSTEM.search(w)]
    ck(not spells,
       "a 口水/唾/痰 word now spells a k- form of his root (%s): the register "
       "has stopped being silent about the slot and the pair can be re-priced"
       % ", ".join(spells[:4]))
    ck(any(w.startswith(ROOT) for w in carriers),
       "the %s family has left the 口水/唾/痰 carriers: the refusal's positive "
       "half -- that the meaning is settled on his own root -- is gone" % ROOT)
    ck(RIVAL in att and any(RIVAL_ZH in g for g in glosses(S, RIVAL)),
       "%s lost its %s gloss: the rival root the refusal names must be read "
       "off its own row (batch 221)" % (RIVAL, RIVAL_ZH))
    print("KYOQAN hapax %d | %s dark %s | 口水 carriers %d, none matching %s"
          % (n_his, SIB_VAL, SIB_VAL in VER, len(carriers), KSTEM.pattern))

    # --- 4. the standing test
    open_rows = unworked(d["sole"], MM)
    print("UNWORKED sole blockers with no refusal in the record: %d"
          % len(open_rows))
    ck(len(open_rows) == UNWORKED,
       "%d sole blocker(s) have no refusal-shaped sentence anywhere in the "
       "record: %s. Every blocked pair is supposed to be held by a written "
       "refusal; price the row before believing the tier is closed."
       % (len(open_rows), ", ".join(open_rows[:6])))

    for f in fails:
        print("FAIL " + f)
    print("\n%d assertions failed" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
