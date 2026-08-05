# -*- coding: utf-8 -*-
"""batch 202: the affix137 test, at length 3. Verdict lines only."""
import io, json, sys
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/"
G = json.load(io.open(H+"tools/orthography/attested_gloss.json", encoding="utf-8"))
T = set(G)
def score(p):
    return sum(1 for w in T if w.startswith(p) and w[len(p):] in T)
print("modern types: %d" % len(T))
print("--- his own prefix card ---")
print("  mpa  %d" % score("mpa"))
print("--- the single letters his cards head (the affix137 baseline) ---")
for p in "adgikmnopst": print("  %-4s %d" % (p, score(p)), end="")
print()
print("--- three-letter controls: shapes that head NO card of his ---")
ctl = ["mqa","mba","mda","mga","mka","mla","mra","msa","mta","mya","bpa","tpa",
       "kpa","spa","npa","gpa","mpi","mpu","mpe","mpo"]
for p in sorted(ctl, key=lambda x: -score(x))[:10]:
    print("  %-4s %d" % (p, score(p)), end="")
print()
print("--- the real modern reflex? his MPA = future + causative ---")
for p in ["empa","mha","mpa","emp"]:
    print("  %-5s %d  (listed as a word: %s)" % (p, score(p), p in T))
