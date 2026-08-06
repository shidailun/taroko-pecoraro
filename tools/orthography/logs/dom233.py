# -*- coding: utf-8 -*-
"""batch 233 — PSAANAK ruled, and the tag furniture closed as a class.

Batch 225 re-parsed his COMPOUND tags with every parenthetical and batch 223's
tag-shape rule applied, and left the sweep with two live pale-side rows and five
"GREEN-side" ones it called a different question. This batch rules the first of
the two, and then measures the whole class the sweep was drawn from. The class
closes: after the ruling there is not one live row of that shape left in 1,967
entries, and the five green ones were never a spelling claim at all.

**0 pairs, by construction.** Every one of the book's 341 tag spans sits outside
every `.truku` box, so a ruling there cannot move the denominator (batch 223).
The assertion `TAG_TRUKU == 0` is in this log so that a later batch does not read
the flat metric as a failed seam and re-price it.

1. PSAANAK — his own parenthetical, and the last of its shape that was live
------------------------------------------------------------------------------
His card is

    PSAANAK (PSAANAQ ?) (R. = ?? - = R. PSANYAQ ?)  擱置一旁－歧視、隔離

and his two spellings of the HEADWORD went to different values of which exactly
one was dark: `psaanak → pseanak` (tier M, batch 70, 偏見, 16 speakers) against a
tier-M identity pin `psaanaq → psaanaq`. Batch 200: the pale side renders what
the dark side renders. Five things had to hold first, and all five do.

* **Only the FIRST parenthetical is testimony.** `(R. = ?? - = R. PSANYAQ ?)`
  posits a root and carries his own question mark, which batch 223's tag-shape
  rule excludes. It renders `PSANIQ` in the same tag, off its own card, and it
  is already dark — correctly: bare `psaniq` is glossed 女人陰部, but `gmpsaniq`
  and `ppsaniq` carry 禁忌, which is his SANYAQ card's gloss. Batch 221's rule,
  name the form whose OWN gloss carries the character, run on the neighbour
  before leaning on it (batch 199).
* **The dark side passes the gloss test** — batch 200's own caveat, which
  refused 7 of its 17 rows. His 擱置一旁－歧視、隔離 against `pseanak` 偏見
  (parquet 區別), with `seanak` 看輕；輕視；瞧不起 sharing his 視 and `ptgeanak`
  隔開 sharing his 隔. That is batch 70's family, not a homograph.
* **There is nothing else for `psaanaq` to be.** The string is in none of the
  four sources; `edictionary_trv.json` carries it explicitly null. Exactly one
  register word stands within one edit, `psranaq` 促使起火焰, and batch 204's
  different-root test refuses it: 火焰 is a different root and there is no
  discrimination sense anywhere near this shape.
* **The pin it replaces had aged.** It is batch 89's green-list re-key
  (commit 586c261), an identity claim with no comment and no argument beside it.
  Batch 216: a tier-M identity pin is the one map entry that ages, because it
  records a search that FAILED — and his own head was ruled one batch later.
* **The scan was read before the map was touched.** `scans/full/page_226.png` is
  book page 205; its bottom half at 1.6× plainly writes `PSAANAK (PSAANAQ ?)`.
  The `q` is his, `entries.js` is faithful, and the fix belongs in the map, which
  is display-only (batch 212).

`q↔k` is excluded from the char rules, so only a map entry can carry this;
`charRules('psaanaq')` is `psaanaq` unaided, which means DELETING the pin would
return the span to green rather than to his letters. It was load-bearing for
colour and its replacement is too (batch 227).

2. A variant ruling REMOVES a span; it does not darken one
------------------------------------------------------------------------------
The obvious assertion — "the tag span goes dark" — is false, and a log that made
it would fail. `tagHtml()` (`app.js:1332`) modernises every variant in the tag
and, when they all agree with the modernised headword, returns the root mark
ALONE. So his `(PSAANAQ ?)` does not turn brown: it stops being printed, and the
card now reads `√ (= PSANIQ?)`. The app already knew what to do with a variant
that agrees with the head; the ruling is what let it.

Measured as a colour that is the same win — one pale span off the book — but it
arrives as a DELETION. Any probe waiting for `psaanaq` to render `w-mod` will
wait forever.

3. The five "GREEN-side" rows were never a claim
------------------------------------------------------------------------------
Batch 225 left LQBUX, PGDGIT, SLAP, XK'LAO and XNU as green-side rows needing
their own spelling argument. They need none. `tagHtml()` line 1324:

    if (!ROOT_MARK.test(tag)) return '<span class="tag">' + esc(tag) + "</span>";

A tag that does not carry his standalone `R` / `R.` is escaped and printed RAW —
no spans, no modernisation, no claim. All five are that shape, and each renders
**zero** spans in its tag. 558 of his 1,850 tags are in that class. The "green"
reading came from asking the MAP what those tokens modernise to, which is batch
219's standing rule arriving in a new place: the map is never evidence about
colour; only the DOM is.

4. The class, measured whole
------------------------------------------------------------------------------
1,850 tags; 1,292 carry the root mark and so enter the spelling pipeline; 86
variant-shape parentheticals sit beside a root mark and therefore render. After
the ruling the book has **321 dark tag spans, 15 pale and 5 green**, and every
non-dark row has a class or a written refusal:

* **15 are batch 223's posited-root shape** `(R. = X ?)` — BIL, DUX, QLOQ,
  EYDANG, EYSA, PSUQIH, PUXIR, IKAXA, BASYAQ, TAMUX, IYAK, GGAR, REQ, GRYEQ,
  RYEQ. He posits a root and marks it with his own question mark; naming the
  class is not a door to clear it, and four of them (`dux`, `eydang`, `eysa`,
  `iyak`) are named as that class in CLAUDE.md already.
* **2 are variant-shape and both are settled**: SAMUL `(SMUL?)`, which batch 227
  deliberately reverted to pale and explained; and SKRUT `(SKRT)`, which is
  vowelless and dropped by the generator's own invariant, so it renders green by
  design.
* **2 are not parentheticals at all**: LUNGUT's crossref arrow → RNGUT, refused
  in writing at batch 204 (懷孕 is `mshjil`, a different root), and TBNAW's bare
  `R`, which is the letter named inside his French *le R étant…* — batch 207's
  metalinguistic class, not a Truku word.

Zero live rows. The sweep batch 225 opened is closed by measurement, not by
exhaustion of patience.

    python tools/orthography/logs/dom233.py     # site served at :8765
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
SOLE_PAIRS, SOLE_TYPES = 79, 67

# the ruling
RULED, RULED_TO = "psaanaq", "pseanak"
HIS_CARD = "PSAANAK"
MODERN_CARD = "PSEANAK"   # `.hw` prints the MODERN head, uppercase (b226)
HIS_TAG = "(PSAANAQ ?) (R. = ?? - = R. PSANYAQ ?)"
HIS_ZH = "擱置一旁－歧視、隔離"
HIS_OCCURRENCES = 1               # in the whole of entries.js, and it is the tag
# the family, and the character of HIS gloss each one carries
FAMILY = {"seanak": "視", "ptgeanak": "隔", "pseanak": None}
NEAR = ("psranaq",)               # the register at edit <= 1, refused (b204)
NEIGHBOUR = "psaniq"              # the tag's OTHER span; dark, and sound
NEIGHBOUR_FAMILY = ("gmpsaniq", "ppsaniq")     # ...they carry his 禁忌
CHARRULE_ID = "psaanaq"           # so deleting the pin returns it to GREEN

# the class
TAGS = 1850
TAGS_RENDERED = 1292              # ...carrying his root mark (app.js:1324)
VARIANT_BESIDE_ROOT = 86
TAG_DARK, TAG_PALE, TAG_GREEN = 321, 15, 5
TAG_TRUKU = 0                     # 0 pairs BY CONSTRUCTION (batch 223)
SHAPES = {"root": 15, "variant": 2, "?": 2}
B225_GREEN = ("LQBUX", "PGDGIT", "SLAP", "XK'LAO", "XNU")

HAN = re.compile(r"[一-鿿]")
TOK = re.compile(r"[A-Za-zÇçÀ-ſ'’ʼ\"]+")
UPPER = re.compile(r"[A-ZÇÖÀ-Ý'\"’]{3,}")
# app.js:1222 verbatim -- his standalone root mark
ROOT_MARK = re.compile(r"(^|[\s(=-])R\.?(?=$|[\s)?=.-])")
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


def manual_map():
    return json.load(io.open(os.path.join(ORTH, "manual_map.json"),
                             encoding="utf-8"))


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


def key(w):
    return re.sub("[’ʼ\"ʔ]", "'", (w or "").lower()).replace("ł", "l")


def ed(a, b):
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, y in enumerate(b, 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (x != y))
    return d[-1]


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


def measure():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        pg.goto(URL)
        pg.evaluate("localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
        pg.goto(URL + "?q=%CC%81")          # a query that matches every card
        pg.wait_for_timeout(22000)
        # dom232's harvester, plus the tag furniture. `.hw` prints the MODERN
        # headword in UPPERCASE (batch 226), so cards are keyed on what the DOM
        # shows and not on his spelling.
        d = pg.evaluate(r"""() => {
          const SEL = 'span.w-mod, span.w-unv, span.w-raw';
          let tot = 0, ok = 0;
          const seen = {}, unv = {}, raw = {}, inTruku = {}, sole = {};
          const tags = [];
          document.querySelectorAll('#results > article.entry').forEach(c => {
            const hw = ((c.querySelector('.hw')||{}).textContent||'').trim();
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
            c.querySelectorAll('.tag').forEach(g => {
              const txt = g.textContent.trim();
              const sp = [...g.querySelectorAll(SEL)].map(s => [
                (s.textContent||'').trim(), s.className.trim(),
                !!s.closest('.truku')]);
              tags.push([hw, txt, sp]);
            });
          });
          return {tot: tot, ok: ok, seen: seen, unv: unv, raw: raw,
                  inTruku: inTruku, sole: sole, tags: tags}; }""")
        b.close()
        return d


# ---- the batch ------------------------------------------------------------
def main():
    MM, MAN, VER = modern_map(), manual_map(), verified()
    AM, AG, BG, PG = sources()
    ENT = entries_json()
    D = measure()
    # `seen` is EVERY span, not the dark ones (batch 232).
    PALE = set(D["unv"])
    DARK = set(D["seen"]) - PALE - set(D["raw"])

    # ---- 0. the metric, which this batch must not move ---------------------
    pairs, denom = D["ok"], D["tot"]
    print("PAIRS %d / %d = %.4f%%   FLOOR %d"
          % (pairs, denom, 100.0 * pairs / max(denom, 1), FLOOR))
    ck(denom == DENOM, "the denominator is %d, expected %d" % (denom, DENOM))
    ck(pairs >= FLOOR, "FLOOR %d: the metric FELL to %d" % (FLOOR, pairs))
    ids = audio_ids()
    ck(len(ids) == AUDIO_IDS,
       "the audio id set is %d, expected %d" % (len(ids), AUDIO_IDS))
    sole = D["sole"]
    ck(sum(sole.values()) <= SOLE_PAIRS and len(sole) <= SOLE_TYPES,
       "sole blockers rose to %d pairs over %d types, pinned at %d/%d"
       % (sum(sole.values()), len(sole), SOLE_PAIRS, SOLE_TYPES))

    # ---- 1. the ruling -----------------------------------------------------
    ck(MM.get(RULED) == RULED_TO,
       "the map sends %s to %r, expected %r" % (RULED, MM.get(RULED), RULED_TO))
    ck(MAN.get(RULED) == RULED_TO,
       "manual_map.json no longer carries the ruling: %r" % MAN.get(RULED))
    # An unargued manual entry is the metric deciding the spelling (batch 219),
    # so the paragraph beside it is asserted, not assumed.
    arg = [v for k, v in MAN.items()
           if k.startswith("_") and RULED in str(v) and "b233" in str(v)]
    ck(len(arg) == 1 and len(arg[0]) > 900,
       "the ruling's argument is missing or too thin to be one: %d comment(s)"
       % len(arg))
    for b in ("200", "204", "212", "216", "227"):
        ck(any(("batch %s" % b) in a for a in arg),
           "the argument does not cite batch %s" % b)
    ck(RULED_TO in VER,
       "%s is not in verified.js, so the ruling renders pale" % RULED_TO)

    # his own letters, and where they occur
    card = [e for e in ENT if e.get("hw") == HIS_CARD]
    ck(len(card) == 1 and (card[0].get("tag") or "").strip() == HIS_TAG,
       "his tag is not what this batch read: %r"
       % (card[0].get("tag") if card else None))
    ck(HIS_ZH in str(card[0].get("zh") if card else ""),
       "his Chinese is not %s" % HIS_ZH)
    occ = sum(len(re.findall(RULED, json.dumps(e, ensure_ascii=False), re.I))
              for e in ENT)
    ck(occ == HIS_OCCURRENCES,
       "%s occurs %d times in entries.js, expected %d -- a second occurrence is "
       "news, because this ruling was priced on the tag alone"
       % (RULED, occ, HIS_OCCURRENCES))

    # the gloss test, on HIS characters and the family's own rows
    his = set(HAN.findall(HIS_ZH))
    for w, ch in FAMILY.items():
        rows = gl(AG, w) + gl(BG, w) + gl(PG, w)
        ck(rows, "%s has no register gloss at all" % w)
        if ch:
            ck(any(ch in str(r) for r in rows) and ch in his,
               "%s no longer carries %s, which is the character of his gloss it "
               "was ruled on: %s" % (w, ch, rows))
    ck(RULED_TO in AM, "%s left attested_modern" % RULED_TO)

    # nothing else for his string to be -- and the negative half as a MEASURE,
    # not a list: any register word within one edit that carries a character of
    # his gloss is the news that re-opens this.
    ck(not any(RULED in D_ for D_ in (AM, AG, BG, PG)),
       "%s is now listed somewhere: the ruling should be re-read" % RULED)
    near = sorted(w for w in AM if abs(len(w) - len(RULED)) <= 1
                  and ed(w, RULED) <= 1)
    # Batch 209: assert a floor, never equality. A word LEAVING this
    # neighbourhood changes the premise of the refusal that was written against
    # it; a word arriving is only news if it carries his meaning, which the next
    # assertion is what measures.
    ck(set(NEAR) <= set(near),
       "%s left the edit<=1 neighbourhood of %s, which is what batch 204's "
       "different-root test was run against: now %s"
       % (sorted(set(NEAR) - set(near)), RULED, near))
    rival = [w for w in near
             if set(HAN.findall(str(gl(AG, w) + gl(BG, w) + gl(PG, w)))) & his]
    ck(not rival,
       "a register word one edit from %s now carries his meaning: %s -- batch "
       "204's different-root test has to be re-run" % (RULED, rival))
    ck(char_rules(RULED) == CHARRULE_ID,
       "charRules(%s) is now %r, not %r: the pin's load-bearingness changed"
       % (RULED, char_rules(RULED), CHARRULE_ID))

    # the tag's OTHER span, checked before being leaned on (batch 199/221)
    ck(NEIGHBOUR in AM and all(
        any("禁忌" in str(r) for r in gl(AG, w) + gl(BG, w) + gl(PG, w))
        for w in NEIGHBOUR_FAMILY),
       "%s's family no longer carries 禁忌, so the dark span beside the ruling "
       "is no longer vouched" % NEIGHBOUR)

    # ---- 2. the ruling REMOVES the span, it does not darken it -------------
    tags = D["tags"]
    mine = [t for t in tags if t[0] == MODERN_CARD]
    ck(mine, "his card does not render as PSEANAK: the DOM prints the modern "
             "headword uppercase (batch 226), so a probe keyed on his spelling "
             "sees nothing")
    ck(not any(RULED.upper() in t[1].upper() for t in mine),
       "his %s parenthetical is still printed: tagHtml() should have collapsed "
       "it to the root mark" % RULED.upper())
    ck(RULED not in D["seen"] and RULED not in PALE,
       "%s still renders somewhere in the book" % RULED)
    ck(sorted(s[0].lower() for t in mine for s in t[2]) == [NEIGHBOUR],
       "the card's tag spans are %s, expected only %s"
       % (sorted(s[0] for t in mine for s in t[2]), NEIGHBOUR))

    # ---- 3. the five that were never a claim -------------------------------
    byhw = collections.defaultdict(list)
    for hw, txt, sp in tags:
        byhw[hw].append((txt, sp))
    for e in ENT:
        if e.get("hw") in B225_GREEN:
            tag = e.get("tag") or ""
            ck(tag and not ROOT_MARK.search(tag),
               "%s's tag %r now carries his root mark, so it DOES enter the "
               "spelling pipeline and is a claim after all" % (e["hw"], tag))
    # ...and the DOM agrees: their tags render no spans at all
    hits = [(hw, txt) for hw, txt, sp in tags if sp and any(
        g in txt.upper() for g in ("L'QBU", "PG'DGIT", "SILAP", "XQ'LAO",
                                   "X'NU"))]
    ck(not hits, "a batch-225 green-side tag now renders spans: %s" % hits[:3])

    # ---- 4. the class, measured whole --------------------------------------
    n_tag = n_root = n_var = 0
    shape = {}
    for e in ENT:
        tag = e.get("tag") or ""
        if not tag:
            continue
        n_tag += 1
        if not ROOT_MARK.search(tag):
            continue
        n_root += 1
        for seg in re.findall(r"\(([^()]*)\)", tag):
            toks = [t for t in UPPER.findall(seg) if t not in ("R", "VR")]
            if not toks:
                continue
            kind = "root" if ROOT_MARK.search(seg) else "variant"
            if kind == "variant":
                n_var += 1
            for t in toks:
                if key(t) == key(e.get("hw")):
                    continue
                v = MM.get(key(t)) or char_rules(key(t))
                shape.setdefault(v, set()).add(kind)
    ck(n_tag == TAGS, "entries with a tag: %d, pinned %d" % (n_tag, TAGS))
    ck(n_root == TAGS_RENDERED,
       "tags carrying his root mark: %d, pinned %d" % (n_root, TAGS_RENDERED))
    ck(n_var == VARIANT_BESIDE_ROOT,
       "variant-shape parentheticals beside a root mark: %d, pinned %d"
       % (n_var, VARIANT_BESIDE_ROOT))

    dark = pale = green = 0
    nondark = []
    for hw, txt, sp in tags:
        for t, cl, inT in sp:
            c = cl.split()
            ck(not inT, "a tag span is inside a .truku box (%s %s): the class "
                        "is no longer 0 pairs by construction" % (hw, t))
            if "w-mod" in c:
                dark += 1
            else:
                nondark.append((hw, t, "pale" if "w-unv" in c else "green"))
                if "w-unv" in c:
                    pale += 1
                else:
                    green += 1
    print("TAGS %d rendered %d | spans dark %d pale %d green %d | inTruku %d"
          % (n_tag, n_root, dark, pale, green,
             sum(1 for _, _, sp in tags for s in sp if s[2])))
    ck((dark, pale, green) == (TAG_DARK, TAG_PALE, TAG_GREEN),
       "the tag census is %s, pinned %s"
       % ((dark, pale, green), (TAG_DARK, TAG_PALE, TAG_GREEN)))
    ck(sum(1 for _, _, sp in tags for s in sp if s[2]) == TAG_TRUKU,
       "tag spans inside a .truku box: expected %d" % TAG_TRUKU)

    got = collections.Counter()
    for hw, t, col in sorted(set(nondark)):
        got["/".join(sorted(shape.get(t.lower(), set()))) or "?"] += 1
    ck(dict(got) == SHAPES,
       "the non-dark tag rows split %s by shape, pinned %s"
       % (dict(got), SHAPES))
    ck(got["variant"] == SHAPES["variant"],
       "a variant-shape tag row is live again: %d, pinned %d"
       % (got["variant"], SHAPES["variant"]))

    for f in fails:
        print("FAIL " + f)
    print("\n%d assertions failed" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
