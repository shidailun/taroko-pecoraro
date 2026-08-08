# -*- coding: utf-8 -*-
"""[batch 233 probe] PSAANAK -- the last live pale-side row of batch 225's
compound-tag sweep. Verdicts only."""
import io, json, os, re, sys, importlib.util
sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location("dom232", "tools/orthography/logs/dom232.py")
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)

MM = M.modern_map(); AM, AG, BG, PG = M.sources(); CNT = M.his_tokens()
ENT = M.entries_json()
def modern(w):
    k = re.sub("[’ʼ\"ʔ]", "'", w.lower()).replace("ł", "l")
    return MM.get(k) or M.char_rules(k)

for t in ("psaanak", "psaanaq", "pseanak", "psaanaqx"):
    print("%-10s map=%-10s modern=%-10s his=%-3s attested=%s"
          % (t, MM.get(t), modern(t), CNT.get(t), modern(t) in AM))

print("\n-- register rows near the two values")
for w in sorted(set(list(AG) + list(BG) + list(PG))):
    if re.search(r"anak$|anaq$", w) and ("an" in w) and len(w) >= 6:
        g = (M.gl(AG, w) or M.gl(BG, w) or M.gl(PG, w) or ["-"])[0]
        print("  %-14s %s" % (w, str(g)[:44]))

print("\n-- anything glossed with a q-final saanaq shape")
hits = [w for D in (AG, BG, PG) for w in D if w.endswith("anaq")]
print("  q-final -anaq rows:", sorted(set(hits))[:12])

print("\n-- his card")
for e in ENT:
    if (e.get("hw") or "").upper().startswith("PSAANA"):
        print("  hw=%s tag=%s" % (e.get("hw"), e.get("tag")))
        print("  zh=%s" % (e.get("zh") or "")[:80])
        print("  fr=%s" % (e.get("fr") or "")[:80])
        print("  subs=%d examples=%d"
              % (len(e.get("subs") or []), len(e.get("examples") or [])))
        for s in (e.get("subs") or []):
            print("    sub %-12s -> %-12s zh=%s"
                  % (s.get("form"), modern(s.get("form") or ""), (s.get("zh") or "")[:30]))

print("\n-- gloss of the dark side")
for nm, D in (("attested", AG), ("bible", BG), ("parquet", PG)):
    print("  %-9s pseanak: %s" % (nm, [str(x)[:40] for x in M.gl(D, "pseanak")][:3]))
    print("  %-9s seanak : %s" % (nm, [str(x)[:40] for x in M.gl(D, "seanak")][:3]))
