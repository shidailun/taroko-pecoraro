# -*- coding: utf-8 -*-
"""batch 241 — one sentence, two acts: a misread glyph and a stem ruled.

His XNUK card's last example is

    § Mxnuk bi ka qouni, ini na txey ka snuk
      Le bois est tres tendre (mou), les clous ne tiennent pas.
      這木頭很軟（鬆），釘子釘不牢。

and it was one of batch 230's four two-type rows: blocked by `snuk` AND by
`thiy` at once, so it appears in no sole-blocker ranking. Both blockers are now
gone, for two DIFFERENT reasons, which is why the row sat unmoved for eleven
batches — every instrument that reached it asked one question of both words.

THE INSTRUMENT THAT FOUND IT is the single-insertion sweep: for every pale
value, insert one letter at every position and ask whether the result is a
listed modern word or a dark value already in the book. Batch 219 (`tglgli`,
`mtlgli`) and batch 229 (`pqeli`) were all found by hand; this is the first time
the shape has been asked mechanically. Over the 74 pale blocking types it
returns 21 values with a candidate, 18 of them landing on a listed word, and it
put `snuk` beside `smuk` on the first pass.

1. `snuk` IS NOT HIS WORD — batch 213, the third instance of one fault class
-----------------------------------------------------------------------------
The cheap test first, before any register question: `snuk` occurred exactly
ONCE in a book that repeats itself. He CARDS `SMUK` (R) 釘子；榫、栓 / "Clou -
fiche … servant a fixer" with two examples and the sub-forms `Psmuk`, `Sm'kan`,
`Pnsm'kan` — batch 235's rule, that a word he gives a headword to is a word he
asserts exists, and four independent writings of the stem leave no glyph in
doubt on THAT side.

The scan was read at page 374 by batch 202's protocol — a known `n` and a known
`m` cropped from the SAME line at 8x, because the typewriter is MONOSPACED and
width discriminates nothing. The `n` of `na`, four cells earlier, shows two legs
and one arch; the `m` of his French `(mou)` shows three legs, two arches and a
notched middle leg; the disputed glyph is the `m` shape. The whole page's French
carries the same fault ("neuble" for meuble, "narche" for marche, "Comne" for
Comme), which is the standing observation that his French `m` renders n-like at
page resolution.

So the fix goes in `entries.js` and NOT in the map (batch 212: a slip is
corrected in the source, a reading the page really carries is respelled in the
map). `smuk -> smuk` was already dark; the correction cost no map entry at all.

THE AUDIO ID KEEPS THE MISREADING ON PURPOSE. An id is a URL (batch 229), so
`ex_mxnuk_bi_ka_qouni_ini_na_txey_ka_snuk` is pinned BY NAME below and the clip
joins the known-stale set. `build_entries.py` was NOT re-run — batch 219: it no
longer reproduces the audio wiring, and the assertion that matters is
`lost=[] new=[]` over the 5,134 attached ids, which held.

The map entry `snuk -> snuk` is now ORPHANED and is left alone: no token reaches
it, it renders zero spans, and it is the same inert class as batch 234's ten
French map values. Asserted as zero rather than deleted.

DOM230'S REFUSAL OF `snuk` IS NOT OVERTURNED. It reads "釘 is carried by the
`samu` family, a different root at 3 edits" (`dom230.py:80`, pinned at :161),
and it is correct — as an answer to "what modern word respells `snuk`?" It never
asked whether the string was his, which is the question batch 213 says to ask
FIRST. Re-asserted below, both halves, so it can still fail.

2. `thiy` — TWO written refusals retired, both premises wrong from the start
-----------------------------------------------------------------------------
`txey` reads cleanly on the same line (four clean cells), so it IS his, and the
question is a spelling one. Batch 219 requires any ruling that contradicts a
written refusal to cite it and say what retires it. There are two.

REFUSAL A — `dom217.py:203`, also `batch-log.md:5016`:

    "his Txey sits on the XNUK 軟／便宜 card, not on TOXOI; thiyan 和…在一起 is
     TOXOI's word and following it would cross two cards"

Its single leg describes where the token is PRINTED, not which headword it
belongs to. That sentence is RUNNING TEXT under XNUK, not a paradigm slot on it,
and running text is where a book uses words off other cards. Mechanically:
`smuk` and `qouni` in that very sentence are dark off SMUK and QOUNI, two other
cards, and no one has called those crossings. What the refusal saw correctly is
that `thiyan` is TOXOI's word — and TOXOI is the card this stem comes off, so
that observation is the argument FOR the value.

REFUSAL B — `dom230.py:84`, pinned at :171:

    "`they` 釘不牢緊 -- 牢 has ONE carrier, `hmkan`, at 5 edits"

This is batch 231's rule arriving a second time: a refusal that scores a gloss
against a token the gloss is not about. The 釘不牢 is the SENTENCE's Chinese —
`txey` has no headword gloss of its own, so the instrument fell back to the
example's, which batch 221 says to mark and discount (`tail221.py`, where doing
so emptied the whole tail). His `ini na txey ka smuk` is literally *the nail
does not accompany it*; the 牢 is the predicate of the whole clause, not the
meaning of this word. The 牢 fact itself is untouched and re-asserted below:
`hmkan` 關（被關；坐牢）is still its only carrier, and still 5 edits away.

3. WHAT RULES IT — his own card, then the register
--------------------------------------------------
HIS TOXOI (R) 散步、遊逛－與…在一起－同時－伴隨－拜訪 carries the sub-form
`Txeyan` 陪伴－同伴 and `Ptxeyun`, so `txey` is a stem he himself derives on that
root. NINE slots of the family already render DARK — toxoi>tuhuy,
txeyan>thiyan, ptxeyun>pthiyun, tgoxoi>tghuy, ttgoxoi>ttguhuy, stgoxoi>stghuy,
ptoxoi>ptuhuy, dtxeyan>dthiyan, snxey>snhiyi — and the bare stem was the only
pale one. That is batch 216's tier-M shape (a pale slot beside ruled siblings,
needing no new evidence, only the family that arrived since) and batch 219's
`tglgli` shape (his own inflected slot spelling the stem).

BATCH 224'S TEST — which listed forms spell the stem WHOLE? Eleven:
`thiya`, `thiyan`, `thiyi`, `thiyun`, `tthiya`, `tthiyi`, `tthiyu`, `kmthiyun`,
`mnegthiyi`, `pthiyi`, `spthiyi`. So `thiy` is a root and not a peel artefact,
even though `thiy` bare is NOT itself listed — which is why it needed
`HAND_RULED` and not a rung of the ladder.

BATCH 221'S REQUIREMENT — name the form whose OWN gloss carries his character:
`thiyan` is glossed 和…在一起, which is his head's 與…在一起 and his `Txeyan`
陪伴 verbatim; `kmthiyun` 和…一起 is a second, independent row (batch 200: the
family, not one row).

THE RIVAL SHAPE IS NAMED AND REFUSED. Eight further listed forms contain the
string `thiy` and are a different root — `thiyaq` 遠 (mgthiyaq, msthiyaq,
pgthiyaq, psthiyaq, smthiyaq, sthiyaq, tmthiyaq). Far is the opposite of his
gloss and the shape needs a final `q` his `txey` does not have. Asserted, so a
shape-only reader cannot mistake one for the other.

THE NEGATIVE HALF, as a property of the carriers (batch 229): of the 58 register
forms glossed 陪 / 在一起 / 同行 / 相伴 / 跟隨, exactly FIVE spell his stem —
`thiyan`, `tuhuy`, `tneguhuy`, `emptuhuy`, `emptghuy` — and every one of them is
his own TOXOI family, `tuhuy` being that card's head value. No carrier off a
different root spells his stem: `tqnay`, `msupu`, `msnegul`, `ggasig`,
`mddulus` are other roots, unreachable from his letters by any correspondence he
uses. If a carrier off a different root ever spells `thiy`, that is the news
that re-opens this.

4. WHAT IT COST, AND WHAT IT DID NOT
-------------------------------------
`txey` is the only token in the book rendering `thiy`, so the ruling darkens
exactly ONE span, and it is inside a `.truku` box. Pairs 5347 -> **5348** of
5429 (98.5080%); book-wide pale TYPES 137 -> 135, two removed at once — `thiy`
ruled and `snuk` no longer rendering at all. The two-type tier goes 4 -> 3 and
the sole tier 79 -> 78, which is the shape batch 235 pinned, moving as predicted
rather than as hoped.

AN INCIDENTAL CORRECTNESS FINDING, RECORDED AND NOT ACTED ON. The register
glosses `smuk` **金鋼樹（樹木名）** — a tree — while his SMUK card is 釘子. Modern
釘子 is `samu`, a different root, so batch 204 says there is no respelling to
find; and the map value is his own letters unchanged, so nothing displays wrong.
It is not a homograph freeze (nothing was mapped ONTO the tree word), and the
transcription fix in section 1 does not depend on it either way — batch 212.
Pinned below so a later batch does not re-derive it.

    python tools/orthography/logs/dom241.py       # site served at :8765
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

FLOOR = 5348
DENOM = 5429
MAP_KEYS = 7371
VER_KEYS = 6327
PALE_TYPES = 135

# --- section 1: the transcription -------------------------------------------
HIS = "Mxnuk bi ka qouni, ini na txey ka smuk"     # corrected
SLIP = "snuk"                                       # the misread string
SLIP_OCCURS = 0                                     # ...nowhere in his Truku now
STEM_OCCURS = 4                                     # `smuk`, 3 before + this one
STALE_ID = "ex_mxnuk_bi_ka_qouni_ini_na_txey_ka_snuk"   # an id is a URL
ID_COUNT = 5134
SMUK_CARD = ("SMUK", "(R)", "釘子", ["Psmuk", "Sm'kan", "Pnsm'kan"])
ORPHAN = ("snuk", "snuk")        # inert map entry, left alone (batch 234)

# dom230's refusal of `snuk`, re-asserted rather than quoted
SAMU = ("samu", "釘子")          # POSITIVE: the different root that carries 釘

# --- section 2: the two refusals retired ------------------------------------
REFUSAL_A = ("dom217.py", "thiy")
REFUSAL_A_TEXT = "his Txey sits on the XNUK"
REFUSAL_B = ("dom230.py", "牢")
LAO_CARRIER = ("hmkan", "牢")    # dom230's fact, untouched and re-aimed
#  the refusal's premise: `smuk` and `qouni` are dark off OTHER cards in the
#  same running-text sentence, so "it sits on the XNUK card" convicts nothing
OFF_OTHER_CARDS = ("smuk", "qhuni")

# --- section 3: what rules it ------------------------------------------------
RULING = ("txey", "thiy")
FAMILY = {"toxoi": "tuhuy", "txeyan": "thiyan", "ptxeyun": "pthiyun",
          "tgoxoi": "tghuy", "ttgoxoi": "ttguhuy", "stgoxoi": "stghuy",
          "ptoxoi": "ptuhuy", "dtxeyan": "dthiyan", "snxey": "snhiyi"}
# batch 224: the listed forms that spell the stem WHOLE
WHOLE = ("thiya", "thiyan", "thiyi", "thiyun", "tthiya", "tthiyi", "tthiyu",
         "kmthiyun", "mnegthiyi", "pthiyi", "spthiyi")
BARE_LISTED = False              # `thiy` itself is not listed — hence HAND_RULED
# batch 221: the form whose OWN gloss carries his character
GLOSSED = {"thiyan": "和…在一起", "kmthiyun": "和…一起"}
HIS_ZH = "與…在一起"             # his TOXOI head
# the rival root that shares the string and must not be mistaken for it
RIVAL = "thiyaq"
RIVAL_FORMS = 8
# batch 229: the negative half, as a property of the carriers
ACCOMPANY = ("陪", "在一起", "同行", "相伴", "跟隨")
CARRIERS = 58
HIS_STEM = ("emptghuy", "emptuhuy", "thiyan", "tneguhuy", "tuhuy")
STEMS = ("thiy", "tuhuy", "guhuy", "tghuy")

# --- section 4: the DOM ------------------------------------------------------
#  word -> (dark, pale, inTruku)
DOM = {"thiy": (1, 0, 1), "smuk": (4, 0, 3), "tuhuy": (20, 0, 17),
       "thiyan": (7, 0, 5)}
SENT = "ini na thiy ka smuk"     # as the page renders it, modern
SENT_SPANS = 9                   # ...every one of them dark

# --- the incidental finding, pinned so it is not re-derived ------------------
SMUK_ROW = ("smuk", "金鋼樹")     # the register's word is a tree; his is a nail

fails = []


def ck(cond, msg):
    if not cond:
        fails.append(msg)
    return cond


# ---- readers ---------------------------------------------------------------
def entries_json():
    s = io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()
    return json.loads(s[s.index("["):s.rindex("]") + 1])


def entries_raw():
    return io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()


def modern_map():
    """Each file's own indentation (batch 207)."""
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


def attested():
    p = os.path.join(ORTH, "attested_modern.json")
    A = json.load(io.open(p, encoding="utf-8"))
    return set(A if isinstance(A, list) else A.keys())


def his_text(E):
    """His Truku fields only — batch 229: parse, walk, join. Never the raw
    string, which is JSON-escaped and carries every corrected-away reading
    inside the audio ids."""
    out = []
    for e in E:
        out += [e.get("hw") or "", e.get("paradigm") or ""]
        out += [x.get("t") or "" for x in e.get("examples") or []]
        for sb in e.get("subs") or []:
            out += [sb.get("form") or "", sb.get("paradigm") or ""]
            out += [x.get("t") or "" for x in sb.get("examples") or []]
    return out


def count(E, w):
    """Word-boundary BOTH sides (batch 229) and over his Truku only."""
    rx = re.compile(r"(?i)\b%s\b" % re.escape(w))
    return sum(len(rx.findall(t)) for t in his_text(E))


def carriers(G, pats):
    return sorted(w for w in G if any(p in " ".join(G[w]) for p in pats))


# ---- the DOM ---------------------------------------------------------------
def measure():
    from playwright.sync_api import sync_playwright
    words = sorted(set(list(DOM) + [SLIP] + list(FAMILY.values())))
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page()
        pg.goto(URL)
        pg.evaluate(
            "localStorage.setItem('taroko_pecoraro_spelling_v1','modern')")
        pg.goto(URL + "?q=%CC%81")
        pg.wait_for_timeout(24000)
        d = pg.evaluate(r"""(A) => {
          const [W, NEEDLE] = A;
          const SEL = 'span.w-mod, span.w-unv, span.w-raw';
          const w = {}, pale = {};
          let tot = 0, ok = 0, sent = null;
          document.querySelectorAll('#results > article.entry').forEach(c => {
            c.querySelectorAll('.truku').forEach(box => {
              const sp = [...box.querySelectorAll(SEL)];
              if (!sp.length) return;
              tot++;
              const all = sp.every(s => s.classList.contains('w-mod'));
              if (all) ok++;
              const t = (box.textContent || '').replace(/🔊/g, '').trim();
              if (t.indexOf(NEEDLE) >= 0)
                sent = {t: t, all: all, n: sp.length};
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
          return {tot: tot, ok: ok, w: w, pale: Object.keys(pale).length,
                  sent: sent};
        }""", [words, SENT])
        b.close()
    return d


def checks(E, MM, VER, G, A, raw):
    """Every assertion that does NOT need the browser, as a list of
    (name, failure-message-or-None).

    main() consumes this and so does `.scratch/b241/control241.py`, so a
    control leg cannot pass against a different implementation than the one
    that runs — batch 234's rule about legs that are free.
    """
    global fails
    fails = []

    # ---- 1. the transcription ---------------------------------------------
    ck(any(HIS in t for t in his_text(E)),
       "his corrected sentence %r is not in entries.js" % HIS)
    ck(count(E, SLIP) == SLIP_OCCURS,
       "`%s` occurs %d times in his Truku, expected %d — the correction has "
       "been undone or a second instance has arrived (batch 213: a hapax in a "
       "book that repeats itself is a candidate for the scan)"
       % (SLIP, count(E, SLIP), SLIP_OCCURS))
    ck(count(E, "smuk") >= STEM_OCCURS,
       "`smuk` occurs %d times, floor %d" % (count(E, "smuk"), STEM_OCCURS))

    #  batch 229: the id keeps the misreading BY NAME, and the count cannot see
    #  a re-mint, so pin the string itself
    ck(STALE_ID in raw,
       "the audio id %s is gone — an id is a URL, and re-minting it unhooks a "
       "clip already recorded (batch 229)" % STALE_ID)
    ck(len(re.findall(r'"a": "(ex_[a-z0-9_]+)"', raw)) == ID_COUNT,
       "attached ids %d, pinned %d"
       % (len(re.findall(r'"a": "(ex_[a-z0-9_]+)"', raw)), ID_COUNT))

    #  his SMUK card: four independent writings of the stem (batch 235)
    hw, tag, zh, subs = SMUK_CARD
    card = [e for e in E if (e.get("hw") or "").strip() == hw]
    ck(len(card) == 1, "his %s card is not in entries.js" % hw)
    if card:
        c = card[0]
        ck((c.get("tag") or "").strip() == tag,
           "his %s tag is %r, expected %r" % (hw, c.get("tag"), tag))
        ck(zh in str(c.get("zh") or ""),
           "his %s gloss is %r, expected to carry %s" % (hw, c.get("zh"), zh))
        got = [sb.get("form") for sb in c.get("subs") or []]
        ck(got == subs, "his %s sub-forms are %s, expected %s"
           % (hw, got, subs))

    #  dom230's refusal of `snuk`, both halves
    ck(any(SAMU[1] in g for g in G.get(SAMU[0], [])),
       "register row %s is %r, expected to carry %s — dom230 refused a "
       "respelling of `snuk` because a DIFFERENT root carries 釘, and that "
       "refusal is not overturned here" % (SAMU[0], G.get(SAMU[0]), SAMU[1]))
    ck(not any(w.startswith("snuk") for w in A),
       "a listed word now spells `snuk` — dom230's refusal was written when "
       "none did")

    # ---- 2. the two refusals retired, and the fact one of them owns --------
    for fn, needle in (REFUSAL_A, REFUSAL_B):
        src = io.open(os.path.join(HERE, fn), encoding="utf-8").read()
        ck(needle in src,
           "%s no longer contains %r — batch 241 cites this refusal, and a "
           "citation that has drifted is not a citation" % (fn, needle))
    src217 = io.open(os.path.join(HERE, "dom217.py"), encoding="utf-8").read()
    ck(REFUSAL_A_TEXT in src217,
       "dom217's refusal sentence has changed; batch 241 quotes it verbatim")
    #  dom230's 牢 fact: still exactly one carrier, still not about this token
    lao = carriers(G, [LAO_CARRIER[1]])
    ck(lao == [LAO_CARRIER[0]],
       "carriers of %s are %s, expected only [%s] — dom230's fact is untouched "
       "here, only re-aimed" % (LAO_CARRIER[1], lao, LAO_CARRIER[0]))

    # ---- 3. what rules it --------------------------------------------------
    k, v = RULING
    ck(MM.get(k) == v, "MAP %s -> %s, expected %s" % (k, MM.get(k), v))
    ck(sorted(t for t, val in MM.items() if val == v) == [k],
       "keys sending to %s are %s, expected only [%s] — the ruling darkens ONE "
       "token and the cost argument rests on that"
       % (v, sorted(t for t, val in MM.items() if val == v), k))
    ck(v in VER, "%s left verified.js — the ruling has been undone" % v)
    ck(MM.get(*ORPHAN) == ORPHAN[1],
       "the orphaned map entry %s -> %s has moved; it is inert and left alone "
       "(batch 234), not deleted" % ORPHAN)

    for t, val in FAMILY.items():
        ck(MM.get(t) == val, "his TOXOI family moved: %s -> %s, expected %s"
           % (t, MM.get(t), val))
        ck(val in VER, "%s left verified.js — the sibling the ruling leans on "
                       "has gone pale (batch 199: run the gloss test on the "
                       "neighbour you are leaning on)" % val)

    missing = [w for w in WHOLE if w not in A]
    ck(not missing,
       "listed forms spelling the stem whole are missing: %s — batch 224's "
       "test is what makes `thiy` a root and not a peel artefact" % missing)
    ck(("thiy" in A) == BARE_LISTED,
       "`thiy` bare is %s in attested_modern; pinned %s. If it becomes listed "
       "the HAND_RULED entry is redundant and the value earns a ladder code"
       % ("now" if "thiy" in A else "not", BARE_LISTED))

    for w, gl in GLOSSED.items():
        ck(any(gl in g for g in G.get(w, [])),
           "register row %s is %r, expected to carry %s — batch 221: the form "
           "whose OWN gloss carries his character" % (w, G.get(w), gl))
    ck(set(HIS_ZH) & set("".join(G.get("thiyan", []))),
       "his %s no longer overlaps thiyan's gloss %r"
       % (HIS_ZH, G.get("thiyan")))

    rival = sorted(w for w in A if RIVAL in w)
    ck(len(rival) >= RIVAL_FORMS,
       "the rival root %s has %d listed forms, floor %d — it is named so a "
       "shape-only reader cannot mistake it for the stem"
       % (RIVAL, len(rival), RIVAL_FORMS))
    ck(RIVAL not in [v], "the ruling value has become the rival root")

    carr = carriers(G, ACCOMPANY)
    ck(len(carr) >= CARRIERS,
       "carriers of %s are %d, floor %d" % ("/".join(ACCOMPANY), len(carr),
                                            CARRIERS))
    mine = sorted(w for w in carr if any(s in w for s in STEMS))
    ck(mine == sorted(HIS_STEM),
       "carriers spelling his stem are %s, expected %s — a carrier off a "
       "DIFFERENT root spelling his stem is the news that re-opens this "
       "(batch 229)" % (mine, sorted(HIS_STEM)))

    ck(len(MM) == MAP_KEYS, "MAP keys %d, pinned %d" % (len(MM), MAP_KEYS))
    ck(len(VER) == VER_KEYS, "VERIFIED keys %d, pinned %d"
       % (len(VER), VER_KEYS))

    # ---- the incidental finding, pinned so it is not re-derived ------------
    w, gl = SMUK_ROW
    ck(any(gl in g for g in G.get(w, [])),
       "register row %s is %r, expected to carry %s — his SMUK is 釘子 and the "
       "register's is a tree; different roots, nothing to respell (batch 204), "
       "and the map value is his own letters so nothing displays wrong"
       % (w, G.get(w), gl))

    return list(fails), {"carriers": carr, "his_stem": mine}


def main():
    E, MM, VER, G, A = (entries_json(), modern_map(), verified(), register(),
                        attested())
    raw = entries_raw()
    fs, info = checks(E, MM, VER, G, A, raw)
    fails.extend(fs)
    carr, mine = info["carriers"], info["his_stem"]
    d = measure()

    # ---- 4. the DOM --------------------------------------------------------
    ck(d["tot"] == DENOM, "denominator %d, pinned %d" % (d["tot"], DENOM))
    ck(d["ok"] >= FLOOR, "FLOOR %d — pairs %d/%d" % (FLOOR, d["ok"], d["tot"]))
    ck(d["pale"] <= PALE_TYPES,
       "book-wide pale TYPES %d, ceiling %d" % (d["pale"], PALE_TYPES))
    for w, (dk, pl, intru) in DOM.items():
        got = d["w"].get(w) or {"dark": 0, "pale": 0, "green": 0, "inTruku": 0}
        ck(got["dark"] >= dk and got["pale"] == pl,
           "DOM %s dark %d pale %d, expected dark >=%d pale %d"
           % (w, got["dark"], got["pale"], dk, pl))
        ck(got["inTruku"] >= intru,
           "DOM %s inTruku %d, floor %d" % (w, got["inTruku"], intru))
    ck(not d["w"].get(SLIP),
       "`%s` renders %s spans — his token was corrected away and the leftover "
       "map entry is supposed to be unreachable" % (SLIP, d["w"].get(SLIP)))

    s = d["sent"]
    ck(s is not None, "the sentence %r does not render at all" % SENT)
    if s:
        ck(s["all"], "the sentence still has a pale span: %r" % s["t"])
        ck(s["n"] == SENT_SPANS,
           "the sentence renders %d spans, pinned %d — a span and a word are "
           "not the same unit (batch 208)" % (s["n"], SENT_SPANS))

    print("batch 241 — %d/%d pairs (%.4f%%), map %d keys, verified %d"
          % (d["ok"], d["tot"], 100.0 * d["ok"] / d["tot"], len(MM), len(VER)))
    print("  slip      snuk -> smuk in entries.js; id %s kept" % STALE_ID)
    print("  ruled     txey -> thiy; %d listed forms spell the stem whole, "
          "%d carriers, %d of them his" % (len(WHOLE), len(carr), len(mine)))
    print("  retired   dom217:203 (where it is PRINTED) and dom230:84 (the "
          "SENTENCE's gloss, batch 231)")
    print("  cost      +1 pair, pale types %d" % d["pale"])
    for f in fails:
        print("FAIL", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
