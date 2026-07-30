"""Batch 56's rule, applied: a dead n-gram in a new value is CHANCE if the value I
am following already ships with it, and a REAL violation if the gram's core has
zero witnesses anywhere (the `adag` signature).

For each (new value, sibling value the batch cites), print which dead grams the
sibling shares, and how many modern types witness each gram's core.
"""
import json, io, sys, re, collections
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"

omni = __import__("pickle").load(io.open("omni.pkl", "rb"))
spoken = json.load(io.open(H + "spoken_truku.json", encoding="utf-8"))
TYPES = {w.lower() for w, g, _ in omni[0] if w} | {w.lower() for w in spoken}
GRAM = collections.Counter()
for w in TYPES:
    s = "^" + w + "$"
    for n in (2, 3, 4):
        for i in range(len(s) - n + 1):
            GRAM[s[i:i + n]] += 1


def dead(v):
    s = "^" + v + "$"
    return [s[i:i + n] for n in (3, 4) for i in range(len(s) - n + 1)
            if not GRAM[s[i:i + n]]]


PAIRS = [("ptquwi", "ptquwun"), ("psprqi", "psprqan"), ("pshmqun", "pshmqan"),
         ("pkpruun", "spruun"), ("pkpruan", "spruan"), ("empnmu", "empnmuun"),
         ("knssgan", "ksgan"), ("mgangah", "ngangah"), ("pnuxun", "nuxun")]
for new, sib in PAIRS:
    dn, ds = dead(new), dead(sib)
    shared = [g for g in dn if g in ds]
    solo = [g for g in dn if g not in ds]
    print("%-9s vs %-10s" % (new, sib))
    if shared:
        print("      shared with sibling: %s  -> chance" % ", ".join(shared))
    for g in solo:
        core = g.strip("^$")[:-1] if g.endswith("$") else g.strip("^$")[:len(g) - 1]
        print("      SOLO %-6s core %-5s witnesses %d" % (g, core, GRAM[core]))
    if not dn:
        print("      no dead gram")
