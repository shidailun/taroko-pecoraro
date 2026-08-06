# -*- coding: utf-8 -*-
"""[batch 230] Two cards ruled, and a meaning sweep that returned nothing.

The multi-blocker list -- pairs held by two pale types at once, which the sole-
blocker ranking cannot see -- had six rows and had never been worked. Two of the
six were rulings and both needed a written refusal retired first.

    2 cards ruled (+4 pairs), 8 refusals confirmed or newly made
    pairs 5340/5429 = 98.3607%  ->  5344/5429 = 98.4343%   (+4)
    pale  226 -> 217 spans, 146 -> 142 types (book-wide)
    sole-blocked pairs 83 -> 81

### 1. SPUNG -- three defects in one Lord's Prayer sentence

    Ya nami bi pdaai pnspngan ni, pstui nami pax knnaqex

`pdaqi` and `pspngan` were TRANSCRIPTION slips and were fixed in `entries.js`
(batch 212 decides where the fix goes). Page 297 at 18x: two flat-bottomed `a`
bowls with no descender, against the obvious descender on `knnaqex`'s `q`. His
own book writes `Pdai bi kana biyax lnglongan` (NDOA) and `Ya bi pdai tnbiyan ka
kacing` (TABE) -- the SAME `Ya ... bi pda-i` negative imperative. `pnspngan` the
page plainly prints `pns-`. `pstui` is HIS spelling, faithful at 22x -- five
glyphs, single `t`, no `w` -- so THAT one went in the map, alongside the three
sibling spellings (`psttui`, `psttuy`, `pstutwi`) already pinned to `pstutuy`.

**Batch 201 refused this card, and the premise it named has gone false**
(batch 227). Its reason was that 試探 and 拯救 "return 0 register rows". Today
試探 returns **0 in `attested_gloss.json` and 4 in `bible_gloss.json`** --
`empspung`, `pnspngan`, `pspngan`, `pspngi`. `git show f355b6b:bible_gloss.json`
carries 考驗；試探 on `pnspngan` at batch 201's own commit, and the file was added
at 753302a, an ancestor. The zero came from searching ONE gloss file.

### 2. SNOXEL -- the register has a SECOND jealousy root

`snoxel -> sneuhir` 忌妒;吃味;容不下人 and `msnoxel -> msneuhir`, both code 1.
Three written refusals go with it: `b57.py:120` froze both to identity to
suppress the char rules' "SNUHER" as a fake word; `map-history.md:779` and batch
204 both said the modern root is `hkrig`, "a different root".

**Why all three missed it, measured.** Searching the STRING of his card, 嫉妒,
returns 38 rows of which 34 are `hkrig`-family and the only `uhir` hit is
`ssneuhir`, unattested. Searching the single character **妒** puts `sneuhir` at
edit distance 2, top of the list. And `snuher` is not a fake word -- it is two
edits from a listed one, the gap being the epenthetic schwa the char rules cannot
supply. His `xel` <-> modern `hir` is an established correspondence in 12 map
values, five of them `oxel -> uhir` on his own KPOXEL card.

`snxelan` HOLDS pale. No `-an` of either stem is listed, and batch 224's sister
test passes -- the `sn-...-an` shape IS spelled for 91 other stems -- so the
silence is evidence and not an empty candidate list.

### 3. The meaning sweep the SNOXEL ruling licensed -- a NEGATIVE result

The fingerprint that found `sneuhir`: a pale value whose card's Chinese carries a
RARE character that some LISTED word carries, within 2 edits. Run over all 131
pale values joined to his Chinese, with batch 218's metalinguistic strip on both
sides and gates at 120 carriers / 2 edits, it yields **48 rows**. Batch 221's
grep of the whole record leaves **4 with no prior mention**, and none is a
ruling: `msapang` 補破舊物品 scores on his 品行不端's 品, `rmuhug` 炒花生 on his
花苞's 花, `nmanu` 為何 on his 為了成為什麼 (and it is a different SLOT -- the
register spells no s-form of that root). Positive control: fed the pre-ruling
state, the sweep returns `snuher -> sneuhir` d=2 on 妒. **Keep the negative
result; don't rebuild it** -- as with `freezesweep.py` and `tail221.py`.

### 4. XUBAO -- batch 68's premise repaired, its verdict kept

Batch 68 held this card because "no bare form is attested". That is now false:
`hibaw` 刀鋒 and `hnibaw` 被割傷 are both listed, both bare, and they match his
XUBAO / XNUBAO pair slot for slot -- same `-n-` infix, and his `-ao` is their
`-aw`, settled by `longao>lungaw`. Repairing the premise does not overturn the
verdict (batch 227). His vowel is `u` and theirs is `i`, and **`u -> i` occurs
0 times in 7,371 map pairs** while `o -> u` fires 1,804 and even `u -> e` fires
17 -- batch 215's instrument, and it returns zero. His own alphabetical order
puts it beyond dispute: XUBAO sits between X'TOL and XUGUT on the page, where an
XIBAO could not. Both spans are furniture and buy 0 pairs by construction
(batch 223), asserted below.

### 5. The other multi-blocker refusals, positive halves named (batch 221)

`snuk` 釘子 -- 釘 is carried by the `samu` family, a different root at 3 edits.
`nrikut` 藉口 -- 詭 has ONE carrier, `rnqdug`, unreachable from his letters.
`basyaq` 饕餮 -- 饕 and 餮 have ZERO carriers in either gloss file.
`dmtsapat` / `msapat` 放蕩 -- 蕩 has 4 carriers, nearest `tkakak` at 5 edits.
`they` 釘不牢緊 -- 牢 has ONE carrier, `hmkan`, at 5 edits.

    python tools/orthography/logs/dom230.py      # site served at :8765
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

FLOOR = 5344
DENOM = 5429
AUDIO_IDS = 5134

# --- the rulings: his key -> the value the map must emit
RULED = {
    "pdaai": "pdai",        # 1. the corrected reading, his own spelling twice over
    "pstui": "pstutuy",     # 1. HIS spelling; the fix is display-only
    "snoxel": "sneuhir",    # 2. the second jealousy root
    "msnoxel": "msneuhir",
}
# `pnspngan` needed no map entry -- the generator emitted it at the id tier,
# which is the whole point: the word was listed all along and only the
# transcription stood between his page and it.
DERIVED = ("pnspngan",)
DARK_VALUES = ("pdai", "pstutuy", "pnspngan", "sneuhir", "msneuhir")

# --- keys that must be GONE. A deleted key is a ruling too.
DELETED = {"pdaqi": "the page reads pdaai; the key is unreachable"}
CHAR_INERT = {"pdaqi": "pdaqi"}     # batch 227: what charRules does unaided

# --- slots that must NOT move. A ruling that spreads is half a ruling.
HOLD = {
    "snxelan": "snxelan",   # 2. no -an of either stem is listed
    "sttui": "sttui",       # 1. STA"TO 斜坡上 -- a different card entirely
    "xubao": "hubaw",       # 4. batch 68's HOLD, kept on the vowel
    "xnubao": "hnubaw",
}
FURNITURE_ONLY = ("hubaw", "hnubaw")    # batch 223: assert inTruku == 0

# --- glosses the rulings rest on. A gloss leaving is the news.
GLOSS = {
    "pdai": "經過",
    "pstutuy": "扶",
    "pnspngan": "試探",
    "sneuhir": "妒",
    "uhir": "妒",           # the bare root, which is what makes it a family
}

# --- batch 201's refusal, and the premise that retires it. Its stated reason
# was that 試探 returns 0 register rows; it returns 0 in ONE file and 4 in the
# other, which existed at that commit. If the bible file ever stops carrying it,
# the refusal comes back and this ruling has to be re-argued.
RETIRED = "試探"
RETIRED_AG = 0              # ... 0 in attested_gloss.json, which is what was read
RETIRED_BG = 4              # ... and 4 in bible_gloss.json, which was not

# --- the SNOXEL refusal for the -an slot, both halves (batch 220 / 224)
REFUSED_AN = "snxelan"
AN_STEM = re.compile(r"^sn.*hir.*an$")      # NEGATIVE: no -an of either stem
SISTER_FLOOR = 80                           # ... and the slot IS spelled: 91 stems
SISTER_SHAPE = re.compile(r"^sn.{2,}an$")

# --- the correspondence that carried the SNOXEL ruling
XEL_FLOOR, OXEL_FLOOR = 12, 5

# --- the refusals, positive halves. Each names the form whose OWN gloss carries
# his character, and asserts it is a DIFFERENT root (batch 204 / 221).
REFUSALS = (
    # pale value, his character, the carrier that has it, expected carrier count
    ("snuk", "釘", "samu", 15),
    ("nrikut", "詭", "rnqdug", 1),
    ("dmtsapat", "蕩", "tkakak", 4),
    ("msapat", "蕩", "tkakak", 4),
    ("snanu", "為", None, 1500),    # a different SLOT, not a different spelling;
    #   and 為 at 1569 carriers is far past any gate -- assert that too, or the
    #   seam sweep's own rarity gate reads as an argument it never made
    ("tmuhung", "炒", "rmuhug", 37),  # his card is 花苞; the 花 is 花生
)
ZERO_CARRIERS = ("饕", "餮")        # basyaq 饕餮 -- nothing in either file
ONE_CARRIER = {"牢": "hmkan"}       # they 釘不牢緊
STILL_PALE = ("snxelan", "snuk", "nrikut", "basyaq", "dmtsapat", "msapat",
              "snanu", "tmuhung", "hubaw", "hnubaw")

# --- XUBAO: batch 68's premise repaired, its verdict kept
BARE_NOW_LISTED = ("hibaw", "hnibaw")   # POSITIVE: the premise that went false
UI_CROSSINGS = 0                        # NEGATIVE: his u never becomes a modern i
OU_FLOOR = 1500                         # ... measured against a rule that DOES fire
ALPHA = ("X'TOL", "XUBAO", "XUGUT")     # his own order puts the vowel beyond doubt

# --- his page, verbatim
SENTENCES = ("Ya nami bi pdaai pnspngan ni, pstui nami pax knnaqex",)
GONE = ("pdaqi",)
HIS_COUNTS = {"pstui": 1, "pstutwi": 6, "psttui": 1, "psttuy": 1,
              "xubao": 1, "xnubao": 1}
# the id still spells the wrong reading, on purpose: an id is a URL and the clip
# is already recorded. Audio is blocked pending a voice; this joins the stale set.
STALE_IDS = ("ex_ya_nami_bi_pdaqi_pspngan_ni_pstui_nami_p",)

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


def entries_json():
    s = entries_text()
    return json.loads(s[s.index("["):s.rindex("]") + 1])


def entries_strings():
    """His text, parsed -- NOT the raw file. The audio id carries the
    pre-correction spelling, so a raw search finds a reading that is gone."""
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
    return set(L("attested_modern.json")), L("attested_gloss.json"), \
        L("bible_gloss.json")


def gl(D, w):
    g = D.get(w) or []
    return g if isinstance(g, list) else [g]


def char_rules(w):
    k = re.sub("[’ʼ\"ʔ']", "", w.lower()).replace("ł", "l")
    return "".join({"x": "h", "o": "u", "l": "r"}.get(c, c) for c in k)


def align_subs(x, y):
    """Every substitution on the cheapest edit path from his key to the value."""
    n, m = len(x), len(y)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1,
                          d[i - 1][j - 1] + (x[i - 1] != y[j - 1]))
    i, j, out = n, m, []
    while i > 0 and j > 0:
        if d[i][j] == d[i - 1][j - 1] + (x[i - 1] != y[j - 1]):
            if x[i - 1] != y[j - 1]:
                out.append((x[i - 1], y[j - 1]))
            i -= 1
            j -= 1
        elif d[i][j] == d[i - 1][j] + 1:
            i -= 1
        else:
            j -= 1
    return out


def his_tokens():
    """Every Truku token he writes, counted. His own book is evidence."""
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

    # --- 1. the metric
    if tot != DENOM:
        fail("DENOM %d got %d" % (DENOM, tot))
    if ok < FLOOR:
        fail("FLOOR %d got %d" % (FLOOR, ok))

    MM, V = modern_map(), verified()
    AM, AG, BG = sources()
    text = entries_strings()
    cnt = his_tokens()

    # --- 2. the map says what the batch ruled
    for k, v in RULED.items():
        if MM.get(k) != v:
            fail("MAP %s -> %s got %s" % (k, v, MM.get(k)))
    for k, why in DELETED.items():
        if k in MM:
            fail("MAP %s is back (-> %s); it was deleted because %s"
                 % (k, MM[k], why))
    for k, v in CHAR_INERT.items():
        if char_rules(k) != v:
            fail("char_rules(%s) should give %s unaided, got %s (batch 227)"
                 % (k, v, char_rules(k)))
    for k, v in HOLD.items():
        if MM.get(k) != v:
            fail("HOLD %s -> %s got %s -- nothing in this batch reached that slot"
                 % (k, v, MM.get(k)))

    # --- 3. the colours
    for w in DARK_VALUES:
        if w not in V:
            fail("%s left verified.js; the ruling no longer renders dark" % w)
        if unv.get(w):
            fail("%s renders pale %d times" % (w, unv[w]))
        if not seen.get(w):
            fail("%s renders nowhere at all" % w)
        if sole.get(w):
            fail("%s still sole-blocks %d pairs" % (w, sole[w]))
    for w in DERIVED:
        if V.get(w) != 1:
            fail("%s is code %s, was derived at 1 -- the id tier is the whole "
                 "argument: the word was listed and only the transcription stood "
                 "between his page and it" % (w, V.get(w)))
    for w in STILL_PALE:
        if not unv.get(w):
            fail("%s no longer renders pale; a refused word going dark is a "
                 "ruling nobody wrote" % w)
    for w in FURNITURE_ONLY:
        if itk.get(w):
            fail("%s is in %d .truku boxes; it is furniture and buys 0 pairs by "
                 "construction (batch 223)" % (w, itk[w]))

    # --- 4. the glosses
    for w, ch in GLOSS.items():
        if w not in AM:
            fail("%s has left the register; the ruling that cited it is gone" % w)
        if not any(ch in g for g in gl(AG, w) + gl(BG, w)):
            fail("%s no longer carries %s -- the gloss test that ruled it is gone"
                 % (w, ch))

    # --- 5. batch 201's refusal and the premise that retires it (batch 227)
    a = len([w for w in AG if any(RETIRED in g for g in gl(AG, w))])
    b = len([w for w in BG if any(RETIRED in g for g in gl(BG, w))])
    if a != RETIRED_AG:
        fail("%s now has %d carriers in attested_gloss.json, was %d -- batch 201 "
             "read that file and got zero, which is why its refusal stood"
             % (RETIRED, a, RETIRED_AG))
    if b < RETIRED_BG:
        fail("%s has %d carriers in bible_gloss.json, floor %d -- that file is "
             "the evidence that retired batch 201's refusal" % (RETIRED, b,
                                                                RETIRED_BG))

    # --- 6. the -an refusal, both halves (batch 220 / 224)
    hit = sorted(w for w in AM if AN_STEM.match(w))
    if hit:
        fail("NEGATIVE an -an of that stem is now spelled: %s -- the silence "
             "%s rests on is over" % (hit[:4], REFUSED_AN))
    sis = len([w for w in AM if SISTER_SHAPE.match(w)])
    if sis < SISTER_FLOOR:
        fail("the sn-...-an shape is spelled for %d stems, floor %d -- without "
             "the sisters the silence is batch 217's empty candidate list, not "
             "evidence (batch 224)" % (sis, SISTER_FLOOR))

    # --- 7. the correspondence the SNOXEL ruling rode on
    xel = [(k, v) for k, v in MM.items() if "xel" in k and "hir" in v]
    oxel = [(k, v) for k, v in xel if "oxel" in k and "uhir" in v]
    if len(xel) < XEL_FLOOR or len(oxel) < OXEL_FLOOR:
        fail("his xel -> modern hir stands at %d pairs (%d of them oxel -> uhir),"
             " floors %d/%d -- that correspondence is what made snoxel a "
             "respelling and not a substitution"
             % (len(xel), len(oxel), XEL_FLOOR, OXEL_FLOOR))

    # --- 8. the refusals, positive halves named (batch 221)
    for val, ch, carrier, floor in REFUSALS:
        if val in AM:
            fail("POSITIVE %s is now listed -- it was refused on its absence"
                 % val)
        cs = sorted(w for w in set(AG) | set(BG)
                    if any(ch in g for g in gl(AG, w) + gl(BG, w)))
        if len(cs) < floor:
            fail("%s is carried by %d register forms, floor %d -- the refusal of "
                 "%s named that carrier set" % (ch, len(cs), floor, val))
        if carrier and carrier not in cs:
            fail("%s no longer carries %s; the refusal of %s named it as the "
                 "different root that does" % (carrier, ch, val))
    for ch in ZERO_CARRIERS:
        cs = [w for w in set(AG) | set(BG)
              if any(ch in g for g in gl(AG, w) + gl(BG, w))]
        if cs:
            fail("NEGATIVE %s now has carriers %s -- basyaq 饕餮 was refused on "
                 "there being none" % (ch, cs[:4]))
    for ch, only in ONE_CARRIER.items():
        cs = sorted(w for w in set(AG) | set(BG)
                    if any(ch in g for g in gl(AG, w) + gl(BG, w)))
        if cs != [only]:
            fail("NEGATIVE %s is carried by %s, was only %s -- the refusal rests "
                 "on there being one and it being unreachable" % (ch, cs[:4], only))

    # --- 9. XUBAO. Batch 68 held it because no bare form was attested; that
    # premise has gone false and the verdict still stands on the vowel.
    for w in BARE_NOW_LISTED:
        if w not in AM:
            fail("POSITIVE %s has left the register -- batch 68's premise (no "
                 "bare form attested) would be true again and this batch's "
                 "repair of it is void" % w)
    ui = ou = 0
    for k, v in MM.items():
        kk = re.sub(r"['’ʼ\"]", "", k)
        if abs(len(kk) - len(v)) > 2:
            continue
        for p in align_subs(kk, v):
            if p == ("u", "i"):
                ui += 1
            elif p == ("o", "u"):
                ou += 1
    if ui != UI_CROSSINGS:
        fail("his u -> modern i now occurs %d times in the map, was %d -- that "
             "zero is the whole ground of the XUBAO refusal" % (ui, UI_CROSSINGS))
    if ou < OU_FLOOR:
        fail("o -> u fires %d times, floor %d -- the zero above means nothing "
             "without a rule that DOES fire to measure it against" % (ou, OU_FLOOR))
    hws = [(e.get("hw") or "").upper() for e in entries_json()]
    try:
        i = hws.index(ALPHA[1])
        if hws[i - 1] != ALPHA[0] or hws[i + 1] != ALPHA[2]:
            fail("XUBAO no longer sits between %s and %s (%s / %s) -- his own "
                 "alphabetical order is what puts the vowel beyond dispute"
                 % (ALPHA[0], ALPHA[2], hws[i - 1], hws[i + 1]))
    except ValueError:
        fail("XUBAO is not a headword any more")

    # --- 10. his page, and his own counts
    for s in SENTENCES:
        if s not in text:
            fail("his sentence has changed: %s" % s)
    for g in GONE:
        if re.search(r"\b" + re.escape(g) + r"\b", text, re.I):
            fail("the corrected reading `%s` is back in entries.js" % g)
    for w, n in HIS_COUNTS.items():
        if cnt.get(w, 0) != n:
            fail("he writes `%s` %d times, was %d -- his own book is the "
                 "evidence these rulings were priced on" % (w, cnt.get(w, 0), n))

    # --- 11. audio. Blocked pending a voice; an id is a URL (batch 219).
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
