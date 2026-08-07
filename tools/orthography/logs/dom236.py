# -*- coding: utf-8 -*-
"""batch 236 — the loan he names in prose, and the freeze his note was hiding.

**+1 pair.** 5,346 → **5,347 / 5,429 = 98.4896%**. `entries.js` is untouched and
the audio id set stands at 5,134; `modern_map.js` keeps 7,371 keys with three
values changed and none gained or lost, and `verified.js` goes 6,325 → 6,326.

1. `towmuk` — three refusals that all searched the same blind file
------------------------------------------------------------------------------
His TEUMUK 首領－負責人－小王 sole-blocked one pair:

    Qole sao teumuk dga, kika pusu balae sao ngalan ta kari da

It was refused three times — `b69.py:101`, `chk97.py:16`, `dom221.py:36` — on
batch 204's different-root test: the register's 首領 is `bukung` 校長；首長 and
`thowlang` 王、領袖或頭目, neither reachable from his letters, so there is no
respelling to find. Sound reasoning. Batch 230's rule is to ask what a refusal
SEARCHED, not what it concluded, and all three searched the gloss files.

**`towmuk` is glossed in none of them, and cannot be.** It is in
`attested_modern`, and its single corpus row is

    towmuk mklawa kngkingal alang ga        [formosan_org_train_clean]

whose translation column is EMPTY. That is why no gloss file carries it: the one
row that attests the word has no Chinese for a gloss file to have been built
from. The three refusals were asking a question the corpus could not answer, and
a zero from a gloss file is not a zero from the register.

The sense comes from the row itself: `mklawa` is 侍衛；看守 and `kngkingal alang`
is *every village*, so a `towmuk` is what watches over every village — his
負責人 exactly. The pin below is the negative half stated as a test: **a gloss
arriving for `towmuk` in any of the three files is news**, because it is the one
thing that would have let those three refusals see the word.

2. His own prose is the etymology, and it is checkable on its OTHER half
------------------------------------------------------------------------------
The evidence that this is a loan is his, not ours. On the TXOULANG card he
writes that the term is from Hokkien *T'eou* 頭 + *Lang* 人 = 頭人 = chief, and
then, of TEUMUK, *que les japonais ont sans doute introduit* — 頭目, tōmoku.

An etymology is testimony, so it is tested on the half that can be: TXOULANG ←
頭人 predicts `thowlang`, which the register lists and glosses 王、領袖或頭目 at
552 parquet tokens. The half that can be checked is right, which is what licenses
the half that cannot.

His `eu` for a Japanese long ō is not invented for this word either. TEUXU is
豆腐 tōfu, tagged `[emprunt jap./chin.]` in his own hand — same digraph, same
vowel, and the map already carries it. (The caveat stays on the record: his
WAWA guess, `?`-marked, is refuted by PAN *wawa, so his etymologies are evidence
and not verdicts. This one is checked, that one was not.)

`teumuk` therefore joins `HAND_LOANS`. **The generator could never have found
it**: it reads his `tag` for the loan verdict (batch 199), and his TEUMUK tag is
`(= R. ? - R. = Chinois ?)` — no `emprunt`, no `[J`. He wrote the loan into the
prose of a DIFFERENT card. The tag assertion below keeps that blindness
discoverable rather than silently repaired.

The value emits **code 1, not 16**. `class_only` (`build_verified.py:339`) is
`(named | loaned | onom | spec) - seen_before_class`, and `towmuk` is
independently in `attested_modern` through the corpus-sentence leg — the one leg
the `>= 2` bar does not gate. The `HAND_LOANS` entry is still load-bearing, on
batch 227's grounds: it is what says *attestation is not a test this word can
sit*, and it is what holds the word if that single corpus row ever moves. Hence
the freq floor at 1.

3. The TXOULANG freeze — 0 pairs, and his head was dark on a word with no gloss
------------------------------------------------------------------------------
Reading that note found the head under it wrong. His TXOULANG 當局－首領們 sat on
`thulang`: listed, 4 parquet tokens, and glossed **nowhere in any of the three
files** — a homograph freeze painting dark AND wrong, invisible to every colour
metric because the span was already dark. The register's own answer is next
door: `thlangan` is glossed 主（**Thowlang** 的斜格形式）, and his `Txlangan` is
glossed 同上詞的斜格形式 — the same statement in two languages.

Decided slot by slot, because a homophone exists:

* head `txoulang → thowlang` — 552 tokens, 王、領袖或頭目, his own gloss.
* `Txlangan → thlangan` — 86 tokens, the oblique, both sides agreeing it is one.
* `Mpatxoulang` 將成為當權者 → `empthowlang` 要作主宰（救主）, listed, where
  `empathulang` is listed **nowhere**. It leaves `HAND_RULED` for that reason.
* `Stxoulang` / `Mstxoulang` 自負 **HELD** on batch 197's pride stem. Batch 197
  argued those two and argued them well (`psthulang` 自大 is his 自負的), and
  they are a different sense of a shared shape. They are PINNED in
  `manual_map.json` at the values they already had, so that moving the head
  could not drag them — batch 223's rule that a ruling stopping at the form the
  map happened to show is half a ruling, applied in the other direction.

Batch 197 is narrowed, not overturned. Its pride reading survives on the two
slots it was about; what moves is the head it had been tracking.

This section buys **0 pairs by construction** — a head, three sub-form names and
one oblique are card furniture, and his two running-text examples were all-dark
before and after. It is a correctness ruling, and the assertions below say so
rather than leaving a later batch to read a flat metric as a failed seam.
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
FLOOR = 5347                      # pairs; +1 on batch 235's 5346
DENOM = 5429
AUDIO_IDS = 5134
MAP_KEYS = 7371                   # unchanged: three values moved, no key did

# the shape of what is left (batch 235's measurement, one row lighter)
SOLE_TYPES = 66
SOLE_PAIRS = 78
TWO_TYPE = 4
THREE_PLUS = 0
TWO_CLUSTERS = (("dmtbasyaq", "dmtsapat"), ("krikut", "nrikut"),
                ("snuk", "thiy"), ("tbasyaq", "tibasyaq"))

# section 1 -- towmuk
HIS, VAL = "teumuk", "towmuk"
HIS_CARD = "TEUMUK"
HIS_TAG = "(= R. ? - R. = Chinois ?)"       # no `emprunt`, no `[J`
LOAN_MARK = re.compile(r"emprunt|\[\s*[Jj]ap|jap\.", re.I)
PQ_FLOOR = 1                      # the single corpus row; a drop is news
CORPUS_ROW = "towmuk mklawa kngkingal alang ga"
RIVALS = {"bukung": "首長", "thowlang": "領"}   # the different-root refusal

# section 2 -- the etymology, tested on its other half
LOAN_TWIN = ("TEUXU", "emprunt")  # his own tagged Japanese loan, same `eu`
NOTE_CARD = "TXOULANG"
NOTE_BITS = ("japonais", "TEUMUK")

# the ORTHOGRAPHIC half, stated against itself (batch 215's instrument). His
# `eu` is regularly `u` and only twice `ow`, so this ruling takes the MINORITY
# correspondence -- which is survivable only because the majority one has
# nothing to offer. If any of these shapes ever turns up, it IS the rival.
RIVAL_SHAPES = ("tumuk", "tmuk", "tomuk", "tuwmuk")
EU_TO_U = 16                      # floor: the regular answer
EU_TO_OW = ("qeulit", "sqeulit")  # the one root that already does what this does
# His French is IN the map and inert (batch 234); `grandeur`/`rougeur` carry the
# digraph and are not his language. The `-eun` suffix is a different
# environment entirely -- `pqleun -> pqriun`, `ptqeun -> ptqiun` -- so counting
# it as evidence about a stem vowel is batch 203's affix fault one level down.
EU_NOT = ("grandeur", "rougeur", "teuxu")

# section 3 -- the TXOULANG card, slot by slot
RULED = {"txoulang": "thowlang", "txlangan": "thlangan",
         "mpatxoulang": "empthowlang"}
HELD = {"stxoulang": "sthulang", "mstxoulang": "msthulang"}
FROZEN = "thulang"                # dark, listed, glossed nowhere
DROPPED = "empathulang"           # left HAND_RULED; listed nowhere
OBLIQUE = re.compile(r"[Tt]howlang")     # thlangan's gloss names its head
FURNITURE_PAIRS = 0               # this section moves no box

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
    """every gloss string the three files carry for w. Batch 230: a zero from
    ONE file is not a zero from the register, so §1's negative half has to ask
    all three or it re-runs the very search that missed the word."""
    out = []
    for D in S[1:]:
        g = D.get(w) or []
        out += [str(x) for x in (g if isinstance(g, list) else [g])]
    return out


def pq_freq():
    return json.load(io.open(os.path.join(ORTH, "parquet_truku_freq.json"),
                             encoding="utf-8"))


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


def card(E, hw):
    for e in E:
        if (e.get("hw") or "") == hw:
            return e
    return None


# ---- the DOM --------------------------------------------------------------
WATCH = ("towmuk", "thowlang", "thlangan", "empthowlang",
         "sthulang", "msthulang", "thulang", "empathulang")


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
        d = pg.evaluate(r"""(WATCH) => {
          const SEL = 'span.w-mod, span.w-unv, span.w-raw';
          let tot = 0, ok = 0;
          const blocked = [], W = {}, T = {};
          const bump = (o, k, dark) => {
            o[k] = o[k] || [0, 0];
            o[k][dark ? 0 : 1]++;
          };
          document.querySelectorAll('#results > article.entry').forEach(c => {
            c.querySelectorAll('.truku').forEach(box => {
              const sp = [...box.querySelectorAll(SEL)];
              if (!sp.length) return;
              tot++;
              if (sp.every(s => s.classList.contains('w-mod'))) ok++;
              else blocked.push([...new Set(sp
                    .filter(s => !s.classList.contains('w-mod'))
                    .map(s => (s.textContent || '').trim().toLowerCase()))]
                  .sort());
              sp.forEach(s => {
                const t = (s.textContent || '').trim().toLowerCase();
                if (WATCH.indexOf(t) >= 0)
                  bump(T, t, s.classList.contains('w-mod'));
              });
            });
            // book-wide, unscoped: his card furniture is in no .truku box
            c.querySelectorAll(SEL).forEach(s => {
              const t = (s.textContent || '').trim().toLowerCase();
              if (WATCH.indexOf(t) >= 0)
                bump(W, t, s.classList.contains('w-mod'));
            });
          });
          return {tot: tot, ok: ok, blocked: blocked, wide: W, truku: T};
        }""", list(WATCH))
        b.close()
    return d


def main():
    d = measure()
    MM, VER, S = modern_map(), verified(), sources()
    E, PQ = entries_json(), pq_freq()
    att = S[0]

    print("PAIRS %d / %d = %.4f%%   FLOOR %d"
          % (d["ok"], d["tot"], 100.0 * d["ok"] / d["tot"], FLOOR))
    ck(d["ok"] >= FLOOR, "FLOOR %d: the metric fell to %d" % (FLOOR, d["ok"]))
    ck(d["tot"] == DENOM, "the denominator is %d, pinned %d"
       % (d["tot"], DENOM))
    ck(len(audio_ids()) == AUDIO_IDS, "the audio id set is %d, expected %d"
       % (len(audio_ids()), AUDIO_IDS))
    ck(len(MM) == MAP_KEYS, "the map has %d keys, pinned %d: this batch moved "
       "three VALUES and no key" % (len(MM), MAP_KEYS))

    # --- 0. the shape of the loss, one row lighter than batch 235
    sole, two, deep = {}, [], 0
    for b in d["blocked"]:
        if len(b) == 1:
            sole[b[0]] = sole.get(b[0], 0) + 1
        elif len(b) == 2:
            two.append(tuple(b))
        else:
            deep += 1
    print("SHAPE sole %d pairs over %d types | two-type %d | three-plus %d"
          % (sum(sole.values()), len(sole), len(two), deep))
    ck(len(sole) <= SOLE_TYPES, "the sole-blocker types rose to %d from %d"
       % (len(sole), SOLE_TYPES))
    ck(sum(sole.values()) <= SOLE_PAIRS,
       "the sole-blocked pairs rose to %d from %d"
       % (sum(sole.values()), SOLE_PAIRS))
    ck(len(two) == TWO_TYPE and sorted(set(two)) == sorted(TWO_CLUSTERS),
       "the two-type seam moved: %d rows, %s. Batch 230 confirmed all four "
       "refusals; a NEW row of this shape is a pair the sole-blocker ranking "
       "cannot see." % (len(two), sorted(set(two))))
    ck(deep == THREE_PLUS,
       "%d pair(s) are now held by three or more pale types. Batch 235 pinned "
       "that tier EMPTY; a row here would be the first of its shape this "
       "project has had, and no ranking in the repo reports it." % deep)

    # --- 1. towmuk: the ruling, and the blindness that hid it
    ck(MM.get(HIS) == VAL, "the map no longer sends %s to %s (it says %s)"
       % (HIS, VAL, MM.get(HIS)))
    ck(VER.get(VAL) == 1, "%s is no longer code 1 in verified.js (it is %s). "
       "It is code 1 and not 16 because class_only subtracts what another leg "
       "already saw, and the corpus-sentence leg saw this one."
       % (VAL, VER.get(VAL)))
    ck(VAL in att, "%s has left attested_modern: the corpus-sentence leg is "
       "the ONLY thing attesting it, so this is the whole ruling" % VAL)
    ck(PQ.get(VAL, 0) >= PQ_FLOOR,
       "the parquet count for %s fell to %s from %d. The word rests on ONE "
       "row (%s); if it goes, HAND_LOANS is carrying the value alone and the "
       "ruling has to be re-read, not silently held up by the class."
       % (VAL, PQ.get(VAL), PQ_FLOOR, CORPUS_ROW))

    # the negative half, stated as a test (batch 221/229)
    g = glosses(S, VAL)
    ck(not g, "FAIL %s is now GLOSSED (%s). It was refused three times "
       "(b69.py:101, chk97.py:16, dom221.py:36) on the different-root test, "
       "and all three searched the gloss files, where its single corpus row "
       "carries no Chinese to have been built from. A gloss arriving is "
       "exactly the evidence those refusals were asking for -- re-read them "
       "against it." % (VAL, "; ".join(g[:3])))
    for w, ch in sorted(RIVALS.items()):
        ck(any(ch in x for x in glosses(S, w)),
           "the 首領 rival %s has lost its %s gloss: the different-root half "
           "of the three refusals cited above can no longer be re-read, so "
           "the reason this ruling had to OVERTURN them is gone" % (w, ch))

    # the generator's blindness, kept discoverable (batch 199)
    c = card(E, HIS_CARD)
    ck(c is not None, "his %s card is gone from entries.js" % HIS_CARD)
    ck(c and (c.get("tag") or "") == HIS_TAG,
       "his %s tag now reads %r, pinned %r" % (HIS_CARD, c and c.get("tag"),
                                               HIS_TAG))
    ck(c and not LOAN_MARK.search(c.get("tag") or ""),
       "his %s tag now carries a loan mark. The generator reads the TAG for "
       "the loan verdict, so if he had marked it there this would never have "
       "needed HAND_LOANS -- and the entry should be re-priced, not kept."
       % HIS_CARD)
    print("TOWMUK map %s->%s code %s | att %s | pq %s | glossed %d | tag %r"
          % (HIS, MM.get(HIS), VER.get(VAL), VAL in att, PQ.get(VAL), len(g),
             c and c.get("tag")))

    # --- 2. the etymology is his, and its other half is checkable
    tw = card(E, LOAN_TWIN[0])
    ck(tw is not None and LOAN_TWIN[1] in (tw.get("tag") or ""),
       "his %s card no longer carries %r in its tag: it is the CONTROL for "
       "the `eu` reading -- a Japanese loan he DID mark, with the same "
       "digraph for the same long vowel" % (LOAN_TWIN[0], LOAN_TWIN[1]))
    nc = card(E, NOTE_CARD)
    ck(nc is not None, "his %s card is gone: it carries the prose that names "
       "TEUMUK a Japanese import, which is the whole evidence" % NOTE_CARD)
    miss = [b for b in NOTE_BITS if b not in (nc.get("fr") or "")] if nc else []
    ck(not miss, "his %s note has lost %s. The ruling rests on HIS testimony; "
       "if the transcription of that note changed, the testimony has to be "
       "re-read from the scan before the ruling stands."
       % (NOTE_CARD, ", ".join(miss)))
    # the orthographic half, stated against itself
    rivals = [w for w in RIVAL_SHAPES
              if w in att or glosses(S, w) or PQ.get(w, 0)]
    ck(not rivals,
       "FAIL %s now exists (%s). His `eu` is regularly `u` and only twice "
       "`ow`, so %s takes the MINORITY correspondence; that was survivable "
       "ONLY because the regular one produced nothing. A rival on the "
       "majority correspondence has to be weighed against it, on the gloss."
       % (", ".join(rivals), ", ".join(rivals), VAL))
    eu = [(k, v) for k, v in sorted(MM.items())
          if "eu" in k and k != HIS and k not in EU_NOT
          and not k.endswith("eun")]
    to_u = [k for k, v in eu if "ow" not in v]
    ck(len(to_u) >= EU_TO_U,
       "the regular `eu` -> `u` correspondence fell to %d keys from %d: the "
       "sentence 'this ruling takes the minority correspondence' is a "
       "measurement, and it has moved" % (len(to_u), EU_TO_U))
    for k in EU_TO_OW:
        ck(MM.get(k, "").find("ow") >= 0,
           "%s no longer answers `ow` (%s): it is the ONE gloss-verified root "
           "(qowlit 田鼠) where his `eu` already does what %s does, and "
           "without it that correspondence has no precedent at all"
           % (k, MM.get(k), VAL))
    print("EU keys %d | -> u %d | -> ow %s | rival shapes listed %d"
          % (len(eu), len(to_u), [MM.get(k) for k in EU_TO_OW], len(rivals)))

    ck(PQ.get(RULED["txoulang"], 0) >= 500,
       "the parquet count for %s fell to %s: it is the CHECKABLE half of his "
       "etymology (TXOULANG < 頭人), and it is what licenses believing the "
       "half about TEUMUK that cannot be checked"
       % (RULED["txoulang"], PQ.get(RULED["txoulang"])))

    # --- 3. the TXOULANG card, slot by slot
    for k, v in sorted(RULED.items()):
        ck(MM.get(k) == v, "the map no longer sends %s to %s (it says %s)"
           % (k, v, MM.get(k)))
        ck(VER.get(v) == 1, "%s is no longer code 1 (it is %s)"
           % (v, VER.get(v)))
        ck(v in att, "%s has left attested_modern" % v)
    ck(not glosses(S, FROZEN),
       "FAIL %s is now glossed (%s). His head sat on it while it was glossed "
       "NOWHERE -- dark and wrong, the homograph freeze no colour metric can "
       "see. A gloss arriving is the news that re-opens whether moving the "
       "head to %s was right." % (FROZEN, "; ".join(glosses(S, FROZEN)[:2]),
                                  RULED["txoulang"]))
    ck(any(OBLIQUE.search(x) for x in glosses(S, RULED["txlangan"])),
       "%s's gloss no longer names %s as its head. That naming is the "
       "register saying in its own words what his `Forme oblique de d°` says "
       "in his -- the two sources agreeing is why the oblique moved with the "
       "head" % (RULED["txlangan"], RULED["txoulang"]))
    ck(DROPPED not in att and not glosses(S, DROPPED),
       "FAIL %s is now attested or glossed. It was dropped from HAND_RULED "
       "because it is listed NOWHERE while %s is listed and glossed 要作主宰; "
       "if it has arrived, batch 197's value is defensible again and the slot "
       "is a genuine tie." % (DROPPED, RULED["mpatxoulang"]))

    # the HELD slots: pinned so the head could not drag them (batch 223)
    for k, v in sorted(HELD.items()):
        ck(MM.get(k) == v,
           "the map sends %s to %s, not %s: batch 197's PRIDE reading has "
           "been dragged off its stem by the head ruling. Those two slots are "
           "a different sense of a shared shape (psthulang 自大 is his 自負的) "
           "and were pinned in manual_map.json for exactly this reason."
           % (k, MM.get(k), v))
        ck(VER.get(v) == 1, "%s is no longer code 1 (it is %s). It is not in "
           "attested_modern, so its darkness comes from HAND_RULED alone -- "
           "leaving that list pales it." % (v, VER.get(v)))

    # --- 4. what colour each watched value actually renders (the DOM decides)
    wide, tru = d["wide"], d["truku"]
    for v in sorted(set(list(RULED.values()) + list(HELD.values()) + [VAL])):
        dark, pale = wide.get(v, [0, 0])
        ck(pale == 0 and dark > 0,
           "%s renders %d dark / %d pale spans book-wide: a ruled value that "
           "renders pale is the ruling failing to reach the page"
           % (v, dark, pale))
    for v in sorted(set([FROZEN, DROPPED])):
        ck(v not in wide, "%s still renders %s span(s). It should appear "
           "nowhere on the page: the map no longer emits it."
           % (v, wide.get(v)))
    print("SPANS book-wide %s" % {k: wide.get(k) for k in sorted(wide)})
    print("SPANS in .truku  %s" % {k: tru.get(k) for k in sorted(tru)})

    # §3 is furniture; assert it bought nothing (batch 223)
    ck(all(tru.get(v, [0, 0])[1] == 0
           for v in list(RULED.values()) + list(HELD.values())),
       "a TXOULANG-card value renders PALE inside a .truku box, so §3 is no "
       "longer the 0-pair correctness ruling it is written up as")
    ck(VAL in tru, "%s renders in NO .truku box: the +1 pair is his TEUMUK "
       "example, and if the value is not in a Truku box the gain came from "
       "somewhere else and this batch is mis-attributed" % VAL)
    ck(not [b for b in d["blocked"] if VAL in b or
            any(x in b for x in RULED.values())],
       "a value ruled this batch is blocking a pair again")

    for f in fails:
        print("FAIL " + f)
    print("\n%d assertions failed" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
