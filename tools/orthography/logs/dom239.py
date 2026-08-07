# -*- coding: utf-8 -*-
"""batch 239 — the QBOLONG freeze, removed; and `kbowlung` refused in writing.

His QBOLONG is a card of its own: `tag: "animal"`, `fr: "Sauterelle."`,
`zh: "蚱蜢。"` — a grasshopper. The map painted it `qburung` 收割, *to harvest*.
Dark AND wrong: the homograph-freeze shape CLAUDE.md says only the gloss test
can find, because the span is already brown and every colour metric scores it
as a win. It surfaced out of batch 238's own unit-scoped sweep, whose `burung`
row is about his OTHER card (the bare root BOLONG); tracing that row to its
units reached QBOLONG, which no instrument in this project had ever asked about.

Origin: `map-history.md:387`, where batch 22 swept `kbolong`, `qbolong`,
`kmbolong` and `mkbolong` onto the harvest family by family SHAPE, and never
asked what the QBOLONG card glosses. That is the fault batch 238's rule names —
a shape hit plus a plausible family is not evidence; only the gloss is.

1. WHY THE FREEZE IS A FREEZE
-----------------------------
His 蚱蜢 and the register's `qburung` 收割 share **no character at all**, and
the harvest sense is not a stray row: `qburung` heads a whole family in the
register (`qbrungaw` 要…收割, `qbrungun` 要收割, `qmburung` 都去收割,
`qnbrungan` 收割過後), which is batch 200's rule — a single gloss row is not the
register's answer, the family is. The family is unanimous and it is about grain.

His own book keeps the two apart, and does so consistently: BOLONG 收割
(tagged `( = R.?) (vr. KBOLONG)`), KBOLONG 收割－收成 with three sub-forms, and
QBOLONG 蚱蜢 with none. `kbolong → qburung` is CORRECT and is untouched here.

2. WHY `kbowlung` IS REFUSED — batch 215, both legs, over populated cells
------------------------------------------------------------------------
The obvious repair is the register's own grasshopper word. The gloss side of it
is as strong as this project ever gets:

  * `kbowlung` 蚱蜢 is the **sole carrier** of 蚱 and of 蜢 in the whole
    register — batch 230's rare-character gate at its limit, and batch 221's
    "name the form whose OWN gloss carries the character" satisfied exactly.
  * it is attested (parquet 12, spoken 10), it is in neither the name nor the
    loan population, and it is morphologically clean: root `bowlung` 跳躍而走
    with a 27-member family, `k-` productive on it.
  * batch 205 costs nothing — his `qbolong` occurs exactly ONCE, as the
    headword, no sub-form and no example, so no correct sentence is repainted.

It is refused anyway, and batch 215 is what refuses it: count his cluster, count
the map's correspondence for it, and check the crossing does not already occur.
Asked in that form — what does HE write for the modern shape? — both legs come
back with a positive correspondence pointing the other way, and both cells are
POPULATED, so this is not batch 217's empty candidate list:

  * modern word-initial `kb-`: **16** map values, and he spells **15 of them
    `kb`** (the sixteenth `ku`). Not one is `qb`. So his correspondence for
    modern initial `kb` is `kb` — and the string `KBOLONG` is one he actually
    wrote, on the other card, for 收割. Had the grasshopper been `kbowlung` he
    would have collided with his own harvest head; instead he wrote Q.
  * modern `-owl-`: **5** map values, and he spells every one `oul`/`eul`
    (`qoulit → qowlit`, `qeulit → qowlit`, `sqeulit → sqowlit`,
    `txoulang → thowlang`, `mpatxoulang → empthowlang`). His correspondence for
    modern `owl` is not bare `ol`. He wrote QBOLONG, not *QBOULONG.

A coarser query says the opposite and is the wrong query: his `q-` → modern
`k-` fires 44 times (35 of them before a consonant), so "his q can be a modern
k" is true in general and settles nothing about this word. Batch 215 asks about
the SHAPE, and the shape is spoken for twice over.

The scan question was opened and closed on his side, not the register's: page
394 reads QBOLONG among his QOYO and QPATOL, with his K plain in KLOBAO, KUI,
KDAYO, KLADAO and KUXENG on the same page, and his alphabetical order puts the
card among the QB- words (batch 230 — his own ordering is testimony about a
letter). `entries.js` is correct and is untouched; the fix belongs in the map,
which is display-only (batch 212).

3. WHY THE PIN IS AN IDENTITY, AND WHY IT IS LOAD-BEARING
---------------------------------------------------------
`charRules("qbolong")` = **`qburung`** — o→u, l→r, letter for letter, the freeze
value exactly. So DELETING the map entry does not return the word to his
letters; it repaints the same wrong string as a green span. This is batch 227's
rule arriving inverted: there the pin spelled what the char rules already
spelled and was still load-bearing; here the pin exists precisely to BLOCK what
they spell. A later tidy-up reading `qbolong → qbolong` as a no-op would
reinstate the freeze without anyone deciding to.

It is a tier-M identity pin, which CLAUDE.md calls the one map entry that ages:
it records a search that FAILED. Two things retire it — a q-initial grasshopper
word entering the register (there are **0** today), or evidence that his bare
`ol` alternates with modern `owl` somewhere. Both are asserted below as regexes
(batch 229) so they can honestly fail when the evidence arrives.

It is NOT a settled class (batch 203). A grasshopper looks like wild fauna, but
the class is defined by the register having no reason to carry the word, and the
register carries it: `kbowlung` is listed and glossed. That is a test this word
can SIT, and it sits it — batch 204. The pallor is correct and it is honest.

4. WHAT IT COST
---------------
Nothing in pairs, by construction (batch 223): his QBOLONG head renders in
`.hw`, in no `.truku` box, and the string occurs once in the whole book. The
measurement: pairs 5347/5429 before and after, `qburung` 4 dark spans → 3,
`qbolong` 0 → 1 pale, `inTruku` 0 on both, book-wide pale TYPES 136 → 137.
Removing a freeze can only ever look like a regression (batch 218); this one is
the cheapest the project has had, because the wrongness sat entirely on
furniture.

    python tools/orthography/logs/dom239.py       # site served at :8765
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
ROOT = os.path.dirname(os.path.dirname(ORTH))
SITE = os.path.join(ROOT, "site")
URL = "http://127.0.0.1:8765/index.html"

FLOOR = 5347                 # unmoved: the freeze sat entirely on furniture
DENOM = 5429
MAP_KEYS = 7371
VER_KEYS = 6326
PALE_TYPES = 137             # 136 before; the revert adds exactly one

RULING = ("qbolong", "qbolong")      # the tier-M identity pin
KEEP = ("kbolong", "qburung")        # his harvest card, correct, untouched
REFUSED = "kbowlung"                 # the register's grasshopper word

# batch 227, inverted: the pin BLOCKS what the char rules spell
CHAR_RULE_OUTPUT = "qburung"

# the two cards, re-read rather than quoted (batch 221)
CARDS = {"QBOLONG": ("蚱蜢", "animal"), "KBOLONG": ("收割", None),
         "BOLONG": ("收割", None)}

# the gloss rows the argument rests on
ROWS = {"kbowlung": "蚱蜢", "qburung": "收割", "bowlung": "跳躍而走"}
UNIQUE_CHARS = "蚱蜢"        # kbowlung is their only carrier in the register

# batch 215, as counts over the live map: what does HE write for the shape?
KB_VALUES = 16               # modern values starting kb-
KB_HIS_QB = 0                # ...of which he spells qb-
OWL_VALUES = 5               # modern values containing owl
OWL_HIS_BARE_OL = 0          # ...of which he spells with a bare ol

# batch 229: the negative halves, as regexes so they can fail honestly
NO_Q_HOPPER = re.compile(r"^q")          # over carriers of 蚱/蜢
HIS_OWL = re.compile(r"[oe]u")           # his spelling for modern owl

# the DOM deltas: before, after, inTruku
DELTA = {"qburung": (4, 3, 0), "qbolong": (0, 1, 0)}

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
    """Each file's own indentation (batch 207): the map writes keys with no
    leading spaces, verified.js with two. A reader copied across files reports
    every change as no change."""
    t = io.open(os.path.join(SITE, "modern_map.js"), encoding="utf-8").read()
    a = t.index("window.MODERN_MAP = {")
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$',
                           t[a:t.index("\n};", a) + 2], re.M))


def verified():
    t = io.open(os.path.join(SITE, "verified.js"), encoding="utf-8").read()
    return dict((m.group(1), int(m.group(2)))
                for m in re.finditer(r'^  "(.+?)": (\d+),?$', t, re.M))


def register():
    """batch 230: a zero from ONE file is not a zero from the register."""
    G = collections.defaultdict(list)
    for p in ("attested_gloss.json", "bible_gloss.json"):
        f = os.path.join(ORTH, p)
        if not os.path.exists(f):
            continue
        for k, v in json.load(io.open(f, encoding="utf-8")).items():
            G[k] += [str(x) for x in (v if isinstance(v, list) else [v])]
    return G


def plain(s):
    return s.replace("ç", "x").replace("'", "").replace('"', "").lower()


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
        d = pg.evaluate(r"""(W) => {
          const SEL = 'span.w-mod, span.w-unv, span.w-raw';
          const w = {}, pale = {};
          let tot = 0, ok = 0;
          document.querySelectorAll('#results > article.entry').forEach(c => {
            c.querySelectorAll('.truku').forEach(box => {
              const sp = [...box.querySelectorAll(SEL)];
              if (!sp.length) return;
              tot++;
              if (sp.every(s => s.classList.contains('w-mod'))) ok++;
            });
            // the pallor census is book-wide and UNSCOPED (batch 222)
            c.querySelectorAll(SEL).forEach(s => {
              const t = (s.textContent || '').trim().toLowerCase();
              const k = s.classList.contains('w-mod') ? 'dark'
                      : (s.classList.contains('w-unv') ? 'pale' : 'green');
              if (k === 'pale') pale[t] = (pale[t] || 0) + 1;
              if (W.indexOf(t) < 0) return;
              w[t] = w[t] || {dark: 0, pale: 0, green: 0, inTruku: 0};
              w[t][k]++;
              if (s.closest('.truku')) w[t].inTruku++;
            });
          });
          return {tot: tot, ok: ok, w: w, pale: Object.keys(pale).length};
        }""", list(DELTA) + [REFUSED])
        b.close()
    return d


# ---- the batch 215 legs, measured over the live map ------------------------
def cluster_legs(MM):
    """What does HE write for modern initial `kb-` and for modern `-owl-`?

    Returns (kb_total, kb_spelled_qb, owl_total, owl_spelled_bare_ol). Both
    cells must be non-empty for the refusal to mean anything (batch 217).
    """
    kb = [(k, v) for k, v in MM.items() if plain(v).startswith("kb")]
    kb_qb = [k for k, _ in kb if plain(k).startswith("qb")]
    owl = [(k, v) for k, v in MM.items() if "owl" in plain(v)]
    owl_ol = [k for k, _ in owl if not HIS_OWL.search(plain(k))]
    return len(kb), len(kb_qb), len(owl), len(owl_ol)


def main():
    E, MM, VER, G = entries_json(), modern_map(), verified(), register()
    d = measure()

    # ---- 1. the map moved exactly one value, to itself --------------------
    ck(len(MM) == MAP_KEYS, "MAP keys %d, pinned %d" % (len(MM), MAP_KEYS))
    ck(len(VER) == VER_KEYS, "VERIFIED keys %d, pinned %d"
       % (len(VER), VER_KEYS))
    k, v = RULING
    ck(MM.get(k) == v, "MAP %s -> %s, expected the identity %s"
       % (k, MM.get(k), v))
    ck(v not in VER, "%s is in verified.js — the identity pin has stopped "
                     "being an honest pallor" % v)
    kk, kv = KEEP
    ck(MM.get(kk) == kv, "his harvest card moved: %s -> %s, expected %s"
       % (kk, MM.get(kk), kv))
    ck(kv in VER, "%s left verified.js — his correct card has gone pale" % kv)
    ck(sorted(t for t, val in MM.items() if val == kv) == [kk],
       "keys sending to %s are %s, expected only [%s]"
       % (kv, sorted(t for t, val in MM.items() if val == kv), kk))

    # ---- 2. the pin is load-bearing (batch 227, inverted) -----------------
    cr = plain(k).replace("o", "u").replace("l", "r").replace("x", "h")
    ck(cr == CHAR_RULE_OUTPUT,
       "charRules(%s) = %s, expected %s — the whole reason the identity pin "
       "exists is that deleting it repaints the freeze" % (k, cr,
                                                           CHAR_RULE_OUTPUT))

    # ---- 3. the gloss test that convicts the freeze -----------------------
    cards = {}
    for e in E:
        hw = (e.get("hw") or "").strip()
        if hw in CARDS:
            cards[hw] = (str(e.get("zh") or ""), e.get("tag"))
    for hw, (zh, tag) in CARDS.items():
        ck(hw in cards, "his %s card is no longer in entries.js" % hw)
        if hw not in cards:
            continue
        ck(zh in cards[hw][0], "his %s gloss is %r, expected to carry %s"
           % (hw, cards[hw][0], zh))
        if tag:
            ck((cards[hw][1] or "").strip() == tag,
               "his %s tag is %r, expected %r" % (hw, cards[hw][1], tag))
    if "QBOLONG" in cards:
        his = set(cards["QBOLONG"][0])
        reg = set("".join(G.get(kv, [])))
        ck(not (his & reg),
           "his QBOLONG gloss now shares %s with %s — the freeze argument "
           "rested on a zero overlap" % (sorted(his & reg), kv))

    for w, gl in ROWS.items():
        ck(any(gl in g for g in G.get(w, [])),
           "register row %s is %r, expected to carry %s" % (w, G.get(w), gl))

    # ---- 4. the positive half of the refusal, and its uniqueness ----------
    carr = sorted(w for w in G if any(c in " ".join(G[w])
                                      for c in UNIQUE_CHARS))
    ck(carr == [REFUSED],
       "carriers of %s are %s, expected only [%s] — a second carrier changes "
       "the candidate and re-opens the refusal" % (UNIQUE_CHARS, carr, REFUSED))

    # the negative half, as a regex: a q-initial grasshopper word re-opens it
    q_hop = [w for w in carr if NO_Q_HOPPER.match(w)]
    ck(not q_hop,
       "a q-initial word is now glossed with %s (%s) — the identity pin was "
       "written because there were none" % (UNIQUE_CHARS, q_hop))

    # ---- 5. batch 215, both legs, over populated cells --------------------
    kbn, kbq, own, owo = cluster_legs(MM)
    ck(kbn >= KB_VALUES,
       "modern kb- values %d, floor %d — the refusal needs a populated cell "
       "(batch 217: an empty candidate list is not a refusal)" % (kbn,
                                                                  KB_VALUES))
    ck(kbq == KB_HIS_QB,
       "he now spells modern kb- as qb- in %d values, expected %d — that "
       "crossing is exactly what %s would require" % (kbq, KB_HIS_QB, REFUSED))
    ck(own >= OWL_VALUES,
       "modern owl values %d, floor %d — cell must stay populated"
       % (own, OWL_VALUES))
    ck(owo == OWL_HIS_BARE_OL,
       "he now spells modern owl with a bare ol in %d values, expected %d — "
       "the second crossing %s would require" % (owo, OWL_HIS_BARE_OL, REFUSED))

    # ---- 6. his own book writes the string, on the other card -------------
    n = 0
    for e in E:
        txts = [e.get("hw") or ""] + [x.get("t") or ""
                                      for x in e.get("examples") or []]
        for sb in e.get("subs") or []:
            txts += [sb.get("form") or ""] + [x.get("t") or ""
                                              for x in sb.get("examples") or []]
        for t in txts:
            n += len(re.findall(r"(?i)\bqbolong\b", t))
    ck(n == 1,
       "his qbolong occurs %d times, expected 1 — batch 205's cost is "
       "measured on that 1, and a second occurrence re-prices the pin" % n)

    # ---- 7. the DOM: what it cost ----------------------------------------
    ck(d["tot"] == DENOM, "denominator %d, pinned %d" % (d["tot"], DENOM))
    ck(d["ok"] >= FLOOR, "FLOOR %d — pairs %d/%d" % (FLOOR, d["ok"], d["tot"]))
    ck(d["pale"] == PALE_TYPES,
       "book-wide pale TYPES %d, pinned %d" % (d["pale"], PALE_TYPES))
    for w, (_, after, intru) in DELTA.items():
        got = d["w"].get(w) or {"dark": 0, "pale": 0, "green": 0, "inTruku": 0}
        want_dark, want_pale = (after, 0) if w == kv else (0, after)
        ck(got["dark"] == want_dark and got["pale"] == want_pale,
           "DOM %s dark %d pale %d, expected dark %d pale %d"
           % (w, got["dark"], got["pale"], want_dark, want_pale))
        ck(got["inTruku"] == intru,
           "DOM %s inTruku %d, expected %d — a furniture ruling buys 0 pairs "
           "BY CONSTRUCTION and the assertion is what records it (batch 223)"
           % (w, got["inTruku"], intru))
    ck(not d["w"].get(REFUSED),
       "%s now renders in the book — it was refused in writing (batch 215, "
       "both legs); a ruling that overturns this must cite section 2 and say "
       "what retires it" % REFUSED)

    print("batch 239 — %d/%d pairs (%.4f%%), map %d keys, verified %d"
          % (d["ok"], d["tot"], 100.0 * d["ok"] / d["tot"], len(MM), len(VER)))
    print("  freeze    qbolong 蚱蜢 was painted qburung 收割; identity-pinned")
    print("  refused   %s — his kb-/owl correspondences, %d and %d values"
          % (REFUSED, kbn, own))
    print("  cost      0 pairs (furniture), pale types %d" % d["pale"])
    for f in fails:
        print("FAIL", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
