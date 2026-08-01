# -*- coding: utf-8 -*-
"""Batch 108: verify the tens series, the word for sand, and the family that
the first pass dragged, straight off the rendered page.

Assertions are over spans only -- no card locators. For each key we assert both
directions: the new value appears with the right paint and the exact expected
count, and the old value appears nowhere at all in modern mode. The dragged
family is asserted too, because its wrong values (sempusal, spsaran) were the
whole reason for the second pass.
"""
import collections
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"
fail = []


def check(cond, msg):
    if not cond:
        fail.append(msg)
    print(("  ok   " if cond else "  FAIL ") + msg)


PROBE = """() => {
  const out = {mod: {}, unv: {}, raw: {}, counts: {}};
  for (const c of ['w-mod','w-unv','w-raw']) {
    const b = out[c.slice(2)];
    const ns = document.querySelectorAll('span.'+c);
    out.counts[c] = ns.length;
    for (const n of ns) {
      const t = n.textContent.trim().toLowerCase();
      b[t] = (b[t] || 0) + 1;
    }
  }
  return out;
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    res = {}
    for mode in ("modern", "original"):
        ctx = b.new_context()
        ctx.add_init_script(
            "localStorage.setItem('taroko_pecoraro_spelling_v1','%s')" % mode)
        pg = ctx.new_page()
        pg.goto(URL)
        pg.wait_for_timeout(6000)
        res[mode] = pg.evaluate(PROBE)
        ctx.close()
    b.close()

M, O = res["modern"], res["original"]
ALL = collections.Counter()
for k in ("mod", "unv", "raw"):
    ALL.update(M[k])
ALLO = collections.Counter()
for k in ("mod", "unv", "raw"):
    ALLO.update(O[k])

print("modern", M["counts"], "original", O["counts"])

# ---- what the batch changed: (his key, new value, paint, his occurrences)
NEW = [
    ("pusal",    "empusal",   "mod", 5),
    ("mnpusal",  "mnempusal", "mod", 2),
    ("m'xalan",  "kmxalan",   "mod", 7),
    ("n'xalan",  "kmxalan",   "mod", 5),
    ("spatwil",  "spatul",    "mod", 2),
    ("bnaqe",    "bnaqig",    "mod", 5),
    ("mkbnaqe",  "mkbnaqig",  "unv", 1),
    ("pnpsalan", "pnpusalan", "unv", 2),
    ("spsalan",  "spusalan",  "unv", 1),
    ("spsali",   "spusali",   "unv", 1),
    ("spsalun",  "spusalun",  "unv", 1),
    ("spusal",   "spusal",    "unv", 1),
    ("snpusal",  "snpusal",   "unv", 2),
]
# never to be seen again in modern mode
DEAD = ["pusal", "mnpusal", "mxalan", "nxalan", "spatwil", "bnaqi", "mkbnaqi",
        "pnpsalan", "spsaran", "spsari", "spsarun", "sempusal", "snempusal",
        "pnpsaran"]

print("\n--- his spellings are still his in Pecoraro mode")
for k, v, paint, n in NEW:
    got = ALLO.get(k.replace("'", "'"), 0)
    check(got >= 1, "%-10s appears %d times unmodernised" % (k, got))

print("\n--- the new values, painted and counted")
tot_v = collections.Counter()
for k, v, paint, n in NEW:
    tot_v[v] += n
# values his OTHER keys already shipped before this batch, which land on the
# same span text and so must be added to the expected count
tot_v["empusal"] += 4        # mpusal, pousal
tot_v["spatul"] += 2         # spat'l
for v in sorted(set(v for _, v, _, _ in NEW)):
    paint = [p for _, x, p, _ in NEW if x == v][0]
    want = tot_v[v]
    got = M[paint].get(v, 0)
    other = sum(M[q].get(v, 0) for q in ("mod", "unv", "raw") if q != paint)
    check(got == want, "%-10s %s x%d (got %d)" % (v, paint, want, got))
    check(other == 0, "%-10s is not painted any other way (%d)" % (v, other))

print("\n--- the values the batch retired")
for d in DEAD:
    if d in ("pusal", "spusal", "snpusal"):      # spusal/snpusal are pinned to
        continue                                  # themselves; pusal is his key
    check(ALL.get(d, 0) == 0, "%-10s gone from modern mode (%d)" % (d, ALL.get(d, 0)))
check(ALL.get("pusal", 0) == 0, "pusal gone as a standalone modern word")

print("\n--- nothing else moved")
check(M["counts"]["w-mod"] == 39443, "w-mod 39443 (got %d)" % M["counts"]["w-mod"])
check(M["counts"]["w-unv"] == 5006, "w-unv 5006 (got %d)" % M["counts"]["w-unv"])
check(M["counts"]["w-raw"] == 26, "w-raw 26 (got %d)" % M["counts"]["w-raw"])
check(sum(M["counts"].values()) == 44475, "44475 words on screen")
GREEN22 = set("""curuphun diram dpnah dubut gaugan gryeq kmrnu kruheng meq
mkruheng mngusyeh ndiyan pa paaaq r remarque req ryeq skrt sruweq supyeh
upskra""".split())
check(set(M["raw"]) == GREEN22,
      "green is the same 22 types as before the batch (%s)"
      % (set(M["raw"]) ^ GREEN22 or "identical"))
check(O["counts"]["w-raw"] == M["counts"]["w-raw"], "green identical in both modes")

print("\n%d failures" % len(fail))
for f in fail:
    print("  " + f)
