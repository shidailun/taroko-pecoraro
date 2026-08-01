# -*- coding: utf-8 -*-
"""Batch 108, second pass: the seven keys the first pass dragged.

Changing PUSAL and M'XALAN moved five of their relatives without being asked,
because the automatic tiers derive a paradigm from whatever its head currently
maps to. Two fell out of the map entirely and went green (n'xalan, pnpsalan)
and three fell from an identity claim to a blind character-rule claim that puts
an r inside an attested root (spsalan -> spsaran). Two more had the numeral
prefix em- grafted into a verb paradigm (spusal -> sempusal).

So the family is pinned by hand:

  n'xalan  -> kmxalan   His own numeral slot: Maspat n'xalan 八十, Mataro
                        n'xalan 六十, Spat n'xalan 四十 -- exactly what his
                        m'xalan does, and modern kmxalan 十的倍數 spk 81 is the
                        word (mpitu kmxalan 七十). The m/n alternation is the
                        typewriter class. NOT knxalan, which is 時代.

  pnpsalan -> pnpusalan Undo his schwa syncope only. Modern keeps the root
                        whole -- empusal 二十 spk 142, mnempusal 4, npusal 再次
                        -- so the l is root-internal and the character rule's
                        r was wrong. Unattested, and pale brown says so.
  spsalan  -> spusalan
  spsali   -> spusali
  spsalun  -> spusalun

  spusal   -> spusal    Pinned to stop the drag. His paradigm here is the verb
  snpusal  -> snpusal   更新－重新開始－重做, not the numeral; em- belongs to
                        empusal 二十 and has no business in it. s-/sn- on the
                        attested root pusal is the regular shape.
"""
import io, json

P = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/manual_map.json"

NEW = {
    "n'xalan":  "kmxalan",
    "pnpsalan": "pnpusalan",
    "spsalan":  "spusalan",
    "spsali":   "spusali",
    "spsalun":  "spusalun",
    "spusal":   "spusal",
    "snpusal":  "snpusal",
}

A1 = '  "spat\'l": "spatul",'
A2 = '  "mkudus": "mkeudus",'
ANCH = {
    "n'xalan":  A1,
    "pnpsalan": A1,
    "spsalan":  A1,
    "spsali":   A1,
    "spsalun":  A1,
    "spusal":   A2,
    "snpusal":  A2,
}

s = io.open(P, encoding="utf-8").read()
before = json.loads(s)
for k in NEW:
    assert k not in before, "already present: %s" % k
for a in set(ANCH.values()):
    assert s.count(a) == 1, "anchor not unique: %s" % a

for k, v in NEW.items():
    a = ANCH[k]
    s = s.replace(a, a + '\n  %s: %s,' % (json.dumps(k), json.dumps(v)), 1)

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
    print("  + %-10s -> %s" % (k, v))
