# -*- coding: utf-8 -*-
"""Batch 112: a regular inflection of an attested root is verified.

The change is not to a spelling but to what the deep brown CLAIMS, so the
assertions are about paint rather than about text. Three things have to hold.

  1  Every level-2 value in verified.js -- the ones the wordlist does not list
     but inflection.py derives from a root it does -- is painted w-mod wherever
     it reaches the page, and never w-unv. That is the change.

  2  The names are still pale. This rule's one way of being badly wrong is to
     verify a personal name as an inflection of some unrelated root (talan, a
     man, decomposes perfectly as tali + -an), so every frozen name asserted
     here must still be w-unv. If this section passes and section 1 passes, the
     rule fired where it was meant to and nowhere else.

  3  The green set is untouched -- same 22 types, same 26 occurrences. Nothing
     about this change reaches an unmapped word, and if green moved, something
     else did too.

Assertions are over spans only, no card locators.
"""
import collections, io, json, re
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/?q=%CC%81"
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
fail = []


def check(cond, msg):
    if not cond:
        fail.append(msg)
    print(("  ok   " if cond else "  FAIL ") + msg)


V = dict((m.group(1), int(m.group(2))) for m in re.finditer(
    r'^  "(.*)": (\d),$', io.open(H + "site/verified.js", encoding="utf-8").read(),
    re.M))
LISTED = sorted(k for k in V if V[k] == 1)
INFL = sorted(k for k in V if V[k] == 2)

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

print("modern", M["counts"], "original", O["counts"])
print("verified.js: %d listed, %d regularly inflected" % (len(LISTED), len(INFL)))

print("\n--- the totals, measured not computed")
check(M["counts"]["w-mod"] == 40617, "w-mod 40617 (got %d)" % M["counts"]["w-mod"])
check(M["counts"]["w-unv"] == 3832, "w-unv 3832 (got %d)" % M["counts"]["w-unv"])
check(M["counts"]["w-raw"] == 26, "w-raw 26 (got %d)" % M["counts"]["w-raw"])
check(sum(M["counts"].values()) == 44475, "44475 words on screen (got %d)"
      % sum(M["counts"].values()))

print("\n--- every level-2 value on screen is deep brown, none of them pale")
seen = [v for v in INFL if ALL.get(v, 0)]
wrong = [v for v in seen if M["unv"].get(v, 0)]
check(len(seen) >= 500, "%d of the %d inflected values reach the page" % (len(seen), len(INFL)))
check(not wrong, "none is painted pale (%s)" % (wrong[:8] or "none"))
occ = sum(M["mod"].get(v, 0) for v in seen)
check(occ >= 1100, "they carry %d occurrences of deep brown" % occ)

print("\n--- a hand-read sample of what turned dark")
for v, root, slot in [("nkuxul", "kuxul", "preterite n-"),
                      ("qnthuran", "qthur", "LF -an with the -n- infix"),
                      ("qriban", "qribi", "LF -an, root vowel swallowed"),
                      ("grigan", "grig", "LF -an"),
                      ("snkukul", "kukul", "sn-"),
                      ("kuyuhan", "kuyuh", "LF -an"),
                      ("mdalih", "dalih", "AF m-"),
                      ("msikul", "sikul", "AF m-")]:
    check(M["mod"].get(v, 0) > 0 and not M["unv"].get(v, 0),
          "%-10s deep brown, %s of %s" % (v, slot, root))

# The doubled onset was admitted while this was being written and then
# withdrawn: mm-/pp-/tt-/ss- are live modern PREFIXES (batch 20), so a doubled
# initial is only sometimes a reduplication. rramil is what that costs, and it
# is asserted here so the class cannot creep back in unnoticed.
check(M["unv"].get("rramil", 0) > 0 and not M["mod"].get("rramil", 0),
      "rramil     still pale -- the doubled onset is NOT a paradigm slot")

print("\n--- the names did NOT turn dark, which is the way this rule fails")
for n in ["sibal", "liwis", "mikat", "ingay", "lauken", "tatu", "talan",
          "banan", "lubyaq", "sikat", "imin", "timin", "tain", "pilin",
          "tagahan"]:
    got = M["unv"].get(n, 0)
    check(got > 0 and not M["mod"].get(n, 0),
          "%-9s still pale (%d occurrences)" % (n, got))
for n in ["sibal", "liwis", "mikat", "talan"]:
    check(n not in V, "%-9s is absent from verified.js altogether" % n)

print("\n--- the listed half is unharmed")
lseen = [v for v in LISTED if ALL.get(v, 0)]
lwrong = [v for v in lseen if M["unv"].get(v, 0)]
check(not lwrong, "no listed value went pale (%s)" % (lwrong[:8] or "none"))

print("\n--- green is exactly where it was")
GREEN22 = set("""curuphun diram dpnah dubut gaugan gryeq kmrnu kruheng meq
mkruheng mngusyeh ndiyan pa paaaq r remarque req ryeq skrt sruweq supyeh
upskra""".split())
check(set(M["raw"]) == GREEN22, "the same 22 green types (%s)"
      % (set(M["raw"]) ^ GREEN22 or "identical"))
check(O["counts"]["w-raw"] == M["counts"]["w-raw"], "green identical in both modes")
check(O["counts"]["w-mod"] > M["counts"]["w-mod"],
      "Pecoraro mode still shows more deep brown (%d vs %d)"
      % (O["counts"]["w-mod"], M["counts"]["w-mod"]))

print("\n%d failures" % len(fail))
for f in fail:
    print("  " + f)
