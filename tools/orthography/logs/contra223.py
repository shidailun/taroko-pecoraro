# -*- coding: utf-8 -*-
"""[batch 223] Batch 201's char-rule contradiction test, run per CARD, book-wide.

Batch 201's rule is that where `l->r` or `x->h` fires on one slot of a card whose
other slots keep the letter, the char rule has overreached -- or, as batch 223
found, a head was re-ruled and a slot pinned to TRACK it was left behind. That
rule had only ever been applied to a card someone was already looking at. This
runs it over all 1,967 entries.

THE RESULT IS NEARLY A NEGATIVE ONE, and that is the point of keeping it. Cards
where his own `l` (or `x`) renders BOTH ways and the minority side is PALE:

    before this batch: 2 rows, both the same card -- XOIL (XOWIL ?) 舀小米酒的杓子
    after `xoil -> huwir` landed: 0 rows in 1,967 entries

The zero is the self-check, not a broken query: the one card it ever found is the
one this batch ruled. Re-run it and expect 0; a NON-zero is the news.

Generalised to the shape that does not depend on which letter it is -- every
headword `X (Y)` / `X (Y ?)` / `X (vl. Y)` whose two sides map to different
values of which exactly ONE is dark -- it returns ONE row in 1,967 entries, the
same card. Batch 200 worked the sub-form parentheticals; batch 223 ruled this
one (`xoil -> huwir`), and the shape is now exhausted at headword level.

So: don't rebuild this expecting a queue. Re-run it after a batch that re-rules a
HEAD, because that is the event which manufactures a stale tracking pin -- that
is exactly how `tqq'lang` came to keep an `l` its whole card had given up.

It reads the map and `verified.js`, so its colour column is an APPROXIMATION and
a candidate generator only. Confirm from the DOM before ruling anything
(CLAUDE.md: the map is never evidence about colour).

    python tools/orthography/logs/contra223.py      # no browser needed
"""
import io, json, re, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
t = io.open('site/modern_map.js', encoding='utf-8').read()
a = t.index('window.MODERN_MAP = {'); b = t.index('\n};', a) + 2
MP = dict(re.findall(r'^"(.+?)":"(.+?)",?$', t[a:b], re.M))
s = io.open('site/entries.js', encoding='utf-8').read()
E = json.loads(s[s.index('['):s.rindex(']') + 1])
V = dict((m.group(1), int(m.group(2))) for m in re.finditer(
    r'^  "(.+?)": (\d+),?$', io.open('site/verified.js', encoding='utf-8').read(), re.M))

def key(w): return re.sub(r'[’ʼ"ʔ]', "'", w.lower()).replace('ł', 'l')
PAIRS = [('l', 'r'), ('x', 'h')]

def names(e):
    out = [e.get('hw', '')] + [x.get('form', '') for x in e.get('subs', [])]
    if e.get('paradigm'): out.append(e['paradigm'])
    return out

rows = []
for e in E:
    toks, seen = [], set()
    for nm in names(e):
        for tok in re.findall(r"[A-Za-z'\"’]+", nm or ''):
            k = key(tok)
            if k in seen or len(k) < 3 or k not in MP: continue
            seen.add(k); toks.append((tok, k, MP[k]))
    for lo, hi in PAIRS:
        has_lo = [t for t in toks if lo in t[2]]
        has_hi = [t for t in toks if hi in t[2]]
        if not has_lo or not has_hi: continue
        # only interesting if his OWN letters were the same on both sides
        hl = [t for t in has_lo if lo in t[1]]
        hh = [t for t in has_hi if lo in t[1]]   # his `l`, rendered `r`
        if not hl or not hh: continue
        pale = [t for t in hl if t[2] not in V]
        if not pale: continue
        rows.append((len(hh), e.get('hw', '')[:26],
                     [(t[0], t[2]) for t in pale][:3],
                     [(t[0], t[2]) for t in hh][:3], lo + '/' + hi))

rows.sort(key=lambda r: -r[0])
print("cards where his %s renders BOTH ways and the minority side is PALE: %d"
      % ('l/r,x/h', len(rows)))
for n, hw, pale, dark, kind in rows[:14]:
    print("  %-26s %s  PALE %s  vs %d dark %s" % (hw, kind, pale, n, dark))
