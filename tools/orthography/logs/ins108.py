# -*- coding: utf-8 -*-
"""Batch 108 map inserts: the tens series and the word for sand.

Six new manual_map keys. None of them existed in any curated file -- all six
were whatever the automatic builder produced, and all six were identity or
near-identity claims that no modern source supports. Five of the six replacements
are attested; the sixth (mkbnaqig) is not, but it is the same root as the fifth
and leaving it on the old root would split the family.

manual_map.json is NOT plain-sorted, so this inserts by text anchor and asserts
that nothing else moved.
"""
import io, json

P = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/manual_map.json"

NEW = {
    "pusal":    "empusal",     # 二十, spk 142; his own mpusal already -> empusal
    "mnpusal":  "mnempusal",   # 二十次（過去發生的）, attested 4x
    "m'xalan":  "kmxalan",     # 十的倍數, spk 81 -- "Pito m'xalan" = 七十
    "spatwil":  "spatul",      # 四十; his own note: "Spatwil (或：Spat'l - spatul)"
    "bnaqe":    "bnaqig",      # 沙, 16x, cf. bbnaqig 沙子, emptbnaqig 砂石業
    "mkbnaqig": None,          # placeholder, replaced below
}
del NEW["mkbnaqig"]
NEW["mkbnaqe"] = "mkbnaqig"    # 沙質的 -- unattested, but the same root as bnaqig

ANCH = {
    "pusal":    '  "spat\'l": "spatul",',
    "mnpusal":  '  "spat\'l": "spatul",',
    "m'xalan":  '  "spat\'l": "spatul",',
    "spatwil":  '  "spat\'l": "spatul",',
    "bnaqe":    '  "mkudus": "mkeudus",',
    "mkbnaqe":  '  "mkudus": "mkeudus",',
}

s = io.open(P, encoding="utf-8").read()
before = json.loads(s)
for k in NEW:
    assert k not in before, "already present: %s" % k
for k, a in ANCH.items():
    assert s.count(a) == 1, "anchor not unique: %s" % a

for k, v in NEW.items():
    a = ANCH[k]
    s = s.replace(a, a + '\n  "%s": "%s",' % (k, v), 1)

after = json.loads(s)
assert len(after) == len(before) + len(NEW), (len(after), len(before))
moved = {k: (before.get(k), after.get(k)) for k in set(before) | set(after)
         if before.get(k) != after.get(k)}
assert set(moved) == set(NEW), moved
for k, v in NEW.items():
    assert moved[k] == (None, v), moved[k]

io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("manual_map.json %d -> %d keys" % (len(before), len(after)))
for k, v in sorted(NEW.items()):
    print("  + %-12s -> %s" % (k, v))
