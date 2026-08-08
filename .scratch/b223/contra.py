# -*- coding: utf-8 -*-
"""Per-card char-rule contradiction sweep (batch 201's rule, book-wide).

For each of his cards, take every token's map value. If the values of ONE card
disagree about a letter the char rules touch (l/r, x/h, o/u) at the same place in
the same stem, the fallback has overreached on one slot -- or, as in batch 223's
tqqlang, a head was re-ruled and a slot pinned to track it was left behind.
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
