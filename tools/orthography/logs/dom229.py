# -*- coding: utf-8 -*-
"""[batch 229] Nine pale blockers, and four of them were reading mistakes.

The seam `blockers.py` handed this batch was nine types nobody had worked. It
read like an orthography problem. It was mostly a TRANSCRIPTION problem: four of
the nine (`k'aon`, `mman`, `olo`, `rqeli`) were glyphs read wrong off the scan,
and two more (`iniko`, `sml'lu`) were his own typing that the map had to absorb
rather than anything to respell. Only one needed a spelling argument at all, and
one was refused.

    6 ruled, 1 refused, 2 needed no map change
    pairs 5331/5429 = 98.1949%  ->  5340/5429 = 98.3607%   (+9)
    pale  235 -> 226 spans, 153 -> 146 types (book-wide)
    sole-blocked pairs 91 -> 83

### 1. `k'aon` -> `klaon` -- his own spelling elsewhere (ruled before this session)

### 2. `nagui` / `n'gui` -> `gneeguy`, and the `nguy` freeze reverted

`nguy` is 哭聲 in the register and his card is 偷. The freeze painted dark AND
wrong (the standing shape). Reverting it costs colour and buys correctness;
`gneeguy` 偷了 carries his gloss. His `nagwi -> ngeuyan` slot on the same card is
a DIFFERENT form and did not move -- assert that, or a later tidy-up will
"finish" the ruling onto a slot the evidence never reached.

### 3. `qntqdan` -- REFUSED, and both halves are asserted (batch 221)

NEGATIVE: the register spells no `-an` of that syncopated stem. That silence
counts, because batch 224's test passes -- the same `qn-...-an` shape IS spelled
for the sister stem, `qntqitan`. POSITIVE: his 捆綁 is carried by 39 register
forms, every one off `bkuy` or `haut`, different roots unreachable from his
letters. So there is no respelling to find and the pallor is correct. A `tqd`
`-an` form ever entering the register is the news that re-opens this.

### 4. `iniko` -> `ini ku` -- the fourth two-word map value

His sentence is `... kika iniko sk'la tdoloi da`, "I did not catch the train",
and `tdoloi -> tdruy` 車 was already dark on the same line. `iniko` is TWO words,
the `Mpaso -> Empaa su` shape (batch 208). Page 294 at 8x: the letter pitch
inside `iniko` matches that inside `kika` and both inter-word gaps are a full
blank cell wider -- the page really prints it joined, so `entries.js` is
untouched and the MAP absorbs it (batch 212 decides where the fix goes). He
writes `ini ko` spaced 119+ times and joined exactly once.

### 5. `mman` -> `maan` -- a slip that landed one letter from his own headword

Page 300 at 8x shows four cells `m-a-a-n`, both `a`s matching the `a` of `ana` on
the same line; the second is light-struck, which is what got read into the `m`.
`Maan` is his OWN headword -- the IMA card's oblique, "a qui? - pour qui?" -- and
he writes `ana maan` for *personne* in five other sentences. `maan -> emaan` 是誰
was already pinned, so the correction cost nothing. The unreachable `mman`
identity pin was deleted; batch 227's rule says assert the char rules, and
`char_rules("mman")` is `mman` unaided, so the pin was inert either way.

### 6. `sml'lu` -> `smalu` -- batch 200's parenthetical, in his own notation

    Sm"lu (sml'lu) ko musa saman da

Dark side `sm"lu -> smalu`, code 1. The precedent is on this same card in this
same notation: `b55.py:11`, "he writes the slot twice on the same paradigm line,
so the two spellings are one word". Batch 200's gloss caveat passes because the
register puts BOTH senses on the one root -- `sluun` is 要被製作 and, in the
bible, 盼望；希望; `snluan` is 希望/願望, which is his own `Snluwan`. Batch 204
finds no rival: across three gloss files only `tddungus` and `psramal` carry
計劃 at all and neither is reachable. `smmlalu` was refused -- listed but bare,
and it needs an `m` his page does not write.

### 7. `pk'kax` -> `pqlqah` -- a dropped letter inside a MANUAL pin (batch 219)

Seven of his eight K'KAX slots were pinned onto the QLQAH paradigm carrying the
`l`; the eighth read `pkkah` with none. `build_verified.py` then derived the
fixed value on its own at **code 6** -- the rung that runs NO gloss test by
construction -- so the gloss was checked by hand instead: the root `qlqah` is
glossed 踏 and his sentence is 我被水牛踩到. 踏/踩 agree.

### 8. `olo` -> `ole` -- a faded crossbar

Page 315 at 22x: `mo`'s `o` and the word-initial `o` are closed rings; the final
glyph is open on the right with a C aperture, an `e` whose crossbar faded. He
writes `ole` 67x for 也/*aussi* and `olo` never. Fixed in `entries.js`; `ole ->
uri` was already code 1. The `olo -> uru` pin STAYS -- it is now reachable only
from his OLO headword, which is furniture, so it buys 0 pairs by construction
(batch 223) and that is asserted below, not assumed.

### 9. `rqeli` -> `pqeli` -> `phqili` -- two defects stacked

Page 317 at 26x: the first glyph has a full descender with a serifed foot and a
bowl -- a `p`, not an `r` -- and pitch-checked against `bi`/`ka` the word is
exactly five cells, `p q e l i`. So `entries.js` takes the `p` and the map key
`rqeli` became unreachable and was deleted. Then his own dropped `x`: fifteen
slots of his XOQEL 死亡 card write it, including `Pxoqel` "Tuer" -> `pxqeli ->
phqili`, and this one running-text token 21 pages away lacks it. `phqili` is
把…死 / 打個半死；把……打死 against his French "tuer". The near-miss `pqlqeli ->
pqrqili` (QLAQEL 受苦) is REFUSED on the gloss -- the whole `rqil` family is
受虐待/使受苦/辛苦, not 殺 -- and that refusal is asserted from the register, not
from memory. His own `xqeli(?)` question mark on that very slot (batch 224)
predicted a second, differently-spelled attempt.

    python tools/orthography/logs/dom229.py      # site served at :8765
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

FLOOR = 5340
DENOM = 5429
AUDIO_IDS = 5134

# --- the six rulings: his key -> the value the map must emit
RULED = {
    "klaon": "klaun",      # 1. the slip corrected before this session
    "nagui": "gneeguy",    # 2. ... and its bracketed variant, below
    "iniko": "ini ku",     # 4. two words, the Mpaso shape
    "maan": "emaan",       # 5. already pinned; the SLIP was in entries.js
    "sml'lu": "smalu",     # 6. his parenthetical
    "pk'kax": "pqlqah",    # 7. the dropped l, inside a manual pin
    "ole": "uri",          # 8. ... the slip was in entries.js again
    "pqeli": "phqili",     # 9. ... and again
}
ALSO_DARK = {"n'gui": "gneeguy", "sm'lu": "smalu", "pxqeli": "phqili"}
# values that must be dark on the page. `ini ku` is checked word by word.
DARK_VALUES = ("klaun", "gneeguy", "emaan", "smalu", "pqlqah", "uri", "phqili")

# --- keys that must be GONE. A deleted key is a ruling too.
DELETED = {
    "mman": "the slip is corrected in entries.js; the pin was inert anyway",
    "rqeli": "the page reads pqeli; the key is unreachable",
}
CHAR_INERT = {"mman": "mman"}   # batch 227: assert what charRules does unaided

# --- slots that must NOT move. A ruling that spreads is half a ruling.
HOLD = {
    "nagwi": "ngeuyan",     # a different form of the GUY card; nothing reached it
    "olo": "uru",           # his OLO headword only -- furniture, 0 pairs
    "pqlqeli": "pqrqili",   # QLAQEL 受苦, refused on the gloss
}
FURNITURE_ONLY = ("uru",)   # batch 223: assert inTruku == 0, never assume it

# --- the freeze this batch reverted. Dark AND wrong is still wrong.
FREEZE_OUT = "nguy"         # 哭聲, on his 偷 card

# --- the refusal, both halves (batch 221)
REFUSED = "qntqdan"
SYNC_STEM = re.compile(r"^qn.?tqd.*an$")    # NEGATIVE: no -an of that stem
SISTER_SLOT = "qntqitan"                    # ... and the slot IS spelled elsewhere
HIS_CHARS = "捆綁"
BKUY_FLOOR = 30                             # POSITIVE: 39 forms carry it ...
HIS_STEM = re.compile(r"tqd|qtd")           # ... and none of them spells his stem

# --- glosses the rulings rest on. A gloss leaving is the news.
GLOSS = {
    "qlqah": "踏",      # rung 6 runs no gloss test; this is the hand check
    "phqili": "死",
    "emaan": "誰",
    "gneeguy": "偷",
    "uri": "也",
    "smalu": "製作",
}
BIBLE_HOPE = ("sluun", "希望")      # the second sense, on the same root
NO_RIVAL_KILL = re.compile(r"rqil")  # his 受苦 family must carry no 殺

# --- his sentences, verbatim. Three were patched; assert what the scan gave.
SENTENCES = (
    "sapax Laotan kika iniko sk'la tdoloi da",
    "Ini ko bi stama ana maan ka yako",
    "Sm\"lu (sml'lu) ko musa saman da",
    "Adi biyao matama ka Wilang mo ole",
    "Ya bi pqeli ka tatat so!",
)
GONE = ("k'aon", "mman", "mo olo", "rqeli")   # the readings that were wrong
SPACED_FLOOR = 119                            # he writes `ini ko` spaced
# ... and the four ids that still SPELL the wrong reading, on purpose. An id is
# a URL: re-minting one unhooks a clip already recorded, so a corrected example
# keeps its old id and joins the known-stale set. That is why the GONE check has
# to run over his TEXT and not over the raw file, which carries these strings.
STALE_IDS = (
    "ex_ida_ta_k_aon_balae_ka_ana_manu_knqnqoan_",
    "ex_ini_ko_bi_stama_ana_mman_ka_yako",
    "ex_adi_biyao_matama_ka_wilang_mo_olo",
    "ex_ya_bi_rqeli_ka_tatat_so_nasi_so_smoa_vl_",
)

JS = r"""() => {
  const SEL = 'span.w-mod, span.w-unv, span.w-raw';
  let tot = 0, ok = 0;
  const seen = {}, unv = {}, inTruku = {}, sole = {};
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
      if (s.closest('.truku')) inTruku[t] = (inTruku[t] || 0) + 1;
    });
  });
  return {tot: tot, ok: ok, seen: seen, unv: unv, inTruku: inTruku,
          sole: sole}; }"""


def entries_text():
    return io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()


def entries_strings():
    """His text, parsed -- NOT the raw file. `Sm"lu` is escaped on disk and the
    audio ids carry the pre-correction spellings, so a raw search both misses
    his sentences and finds readings that are gone from the book."""
    s = entries_text()
    E = json.loads(s[s.index("["):s.rindex("]") + 1])
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
    for e in E:
        walk(e)
    return "\n".join(out)


def audio_ids():
    s = entries_text()
    E = json.loads(s[s.index("["):s.rindex("]") + 1])
    out = set()

    def walk(e):
        for x in (e.get("examples") or []):
            if x.get("a"):
                out.add(x["a"])
        for sb in (e.get("subs") or []):
            walk(sb)
    for e in E:
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
    L = lambda n: json.load(io.open(os.path.join(ORTH, n), encoding="utf-8"))
    return set(L("attested_modern.json")), L("attested_gloss.json"), \
        L("bible_gloss.json")


def gloss(D, w):
    g = D.get(w) or []
    return g if isinstance(g, list) else [g]


def char_rules(w):
    k = re.sub("[’ʼ\"ʔ']", "", w.lower()).replace("ł", "l")
    return "".join({"x": "h", "o": "u", "l": "r"}.get(c, c) for c in k)


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
    seen, unv, itk, sole = d["seen"], d["unv"], d["inTruku"], d["sole"]
    print("pairs %d/%d = %.4f%%" % (ok, tot, 100.0 * ok / tot))
    print("pale span types %d   pale spans %d   sole-blocked pairs %d"
          % (len(unv), sum(unv.values()), sum(sole.values())))

    # --- 1. the metric. Nine pairs were bought; the floor moves to 5340
    if tot != DENOM:
        fail("DENOM %d got %d" % (DENOM, tot))
    if ok < FLOOR:
        fail("FLOOR %d got %d" % (FLOOR, ok))

    MM, V = modern_map(), verified()
    AM, AG, BG = sources()
    text = entries_strings()

    # --- 2. the map says what the batch ruled, including the parenthetical's
    # dark side and the XOQEL slot the pqeli ruling was taken from
    for k, v in list(RULED.items()) + list(ALSO_DARK.items()):
        if MM.get(k) != v:
            fail("MAP %s -> %s got %s" % (k, v, MM.get(k)))
    for k, why in DELETED.items():
        if k in MM:
            fail("MAP %s is back (-> %s); it was deleted because %s"
                 % (k, MM[k], why))
    for k, v in CHAR_INERT.items():
        if char_rules(k) != v:
            fail("char_rules(%s) should give %s unaided, got %s -- the deleted "
                 "pin was inert on that fact (batch 227)" % (k, v, char_rules(k)))

    # --- 3. the colours. Every ruled value is dark, in verified.js, and none of
    # them sole-blocks anything any more.
    for w in DARK_VALUES:
        if w not in V:
            fail("%s left verified.js; the ruling no longer renders dark" % w)
        if unv.get(w):
            fail("%s renders pale %d times" % (w, unv[w]))
        if not seen.get(w):
            fail("%s renders nowhere at all" % w)
        if sole.get(w):
            fail("%s still sole-blocks %d pairs" % (w, sole[w]))
    # the two-word value is coloured word by word AND joined (batch 208 shape)
    for w in ("ini", "ku", "ini ku"):
        if w not in V:
            fail("%s missing from verified.js -- the two-word value is coloured "
                 "per word and joined; both are needed" % w)

    # --- 4. the code-6 hand check. Rung 6 runs no gloss test by construction,
    # so the gloss that licensed pqlqah is asserted here or nowhere.
    if V.get("pqlqah") != 6:
        fail("pqlqah is code %s, was derived at 6 -- a rung change is news, "
             "because 6 is the rung that skips the gloss test" % V.get("pqlqah"))
    for w, ch in GLOSS.items():
        if w not in AM:
            fail("%s has left the register; the ruling that cited it is gone" % w)
        if not any(ch in g for g in gloss(AG, w) + gloss(BG, w)):
            fail("%s no longer carries %s -- the gloss test that ruled it is gone"
                 % (w, ch))
    w, ch = BIBLE_HOPE
    if not any(ch in g for g in gloss(BG, w) + gloss(AG, w)):
        fail("%s no longer carries %s; batch 200's gloss caveat on sml'lu passed "
             "because BOTH senses sit on the one root" % (w, ch))

    # --- 5. the refusal, both halves (batch 221)
    if REFUSED in AM:
        fail("POSITIVE %s is now listed -- the refusal was made on its absence"
             % REFUSED)
    if not unv.get(REFUSED):
        fail("%s no longer renders pale; a refused word going dark is a ruling "
             "nobody wrote" % REFUSED)
    hit = sorted(w for w in AM if SYNC_STEM.match(w))
    if hit:
        fail("NEGATIVE an -an of that syncopated stem is now spelled: %s -- the "
             "silence the refusal rests on is over" % hit[:4])
    if SISTER_SLOT not in AM:
        fail("%s has left the register; without the sister the silence is batch "
             "217's empty candidate list, not evidence" % SISTER_SLOT)
    carriers = sorted(w for w in AM
                      if any(HIS_CHARS in g for g in gloss(AG, w)))
    if len(carriers) < BKUY_FLOOR:
        fail("%s is carried by %d register forms, floor %d"
             % (HIS_CHARS, len(carriers), BKUY_FLOOR))
    # the different-root test in the only form that can honestly fail: his 捆綁
    # is spelled by roots that share no stem with his word (bkuy, haut, kuy,
    # krut, bsqur). A carrier spelling `tqd`/`qtd` is a respelling to find.
    stray = [w for w in carriers if HIS_STEM.search(w)]
    if stray:
        fail("NEGATIVE %s is now carried by %s, which spells his own stem -- "
             "that is a respelling for qntqdan and the refusal re-opens"
             % (HIS_CHARS, stray[:4]))
    kill = sorted(w for w in AM if NO_RIVAL_KILL.search(w)
                  and any("殺" in g for g in gloss(AG, w) + gloss(BG, w)))
    if kill:
        fail("NEGATIVE his 受苦 family now carries 殺: %s -- pqlqeli -> pqrqili "
             "was refused on exactly that not being so" % kill[:4])

    # --- 6. the freeze stays reverted. Dark and wrong scores as a win on the
    # colour metric, so only an assertion keeps it out (batch 218).
    if FREEZE_OUT in V:
        fail("%s is back in verified.js -- 哭聲 on his 偷 card is the freeze this "
             "batch paid to revert" % FREEZE_OUT)
    if seen.get(FREEZE_OUT):
        fail("%s renders %d times; it should render nowhere" % (FREEZE_OUT,
                                                               seen[FREEZE_OUT]))

    # --- 7. the slots that must not move
    for k, v in HOLD.items():
        if MM.get(k) != v:
            fail("HOLD %s -> %s got %s -- nothing in this batch reached that slot"
                 % (k, v, MM.get(k)))
    for w in FURNITURE_ONLY:
        if itk.get(w):
            fail("%s is in %d .truku boxes; it is furniture and buys 0 pairs by "
                 "construction (batch 223)" % (w, itk[w]))

    # --- 8. his page. Three sentences were patched in entries.js because the
    # SCAN was read; the readings that were wrong must not come back.
    for s in SENTENCES:
        if s not in text:
            fail("his sentence has changed: %s" % s)
    for g in GONE:
        # BOTH boundaries: `mman` unanchored on the right matches his French
        # `commandements`, and a check that fires on the gloss language proves
        # nothing about the Truku
        if re.search(r"\b" + re.escape(g) + r"\b", text, re.I):
            fail("the corrected reading `%s` is back in entries.js" % g)
    spaced = len(re.findall(r"\bini ko\b", text, re.I))
    joined = len(re.findall(r"\biniko\b", text, re.I))
    if spaced < SPACED_FLOOR:
        fail("he writes `ini ko` spaced %d times, floor %d -- that count is the "
             "argument that iniko is two words" % (spaced, SPACED_FLOOR))
    if joined != 1:
        fail("`iniko` occurs %d times, was 1 -- the map absorbed the ONE joined "
             "spelling; a second is a transcription question" % joined)

    # --- 9. audio. Blocked pending a voice; an id is a URL (batch 219). The
    # four corrected examples KEEP the id that spells the wrong reading.
    ids = audio_ids()
    if len(ids) != AUDIO_IDS:
        fail("AUDIO ids %d, pinned at %d" % (len(ids), AUDIO_IDS))
    for i in STALE_IDS:
        if i not in ids:
            fail("AUDIO id %s was re-minted; a corrected example keeps its old "
                 "id or the clip already recorded is unhooked" % i)

    print("\n%d assertions failed" % len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
