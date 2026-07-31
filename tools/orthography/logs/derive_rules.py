"""Derive his spelling correspondences from the pairs already shipped, instead of
hand-listing the ones I happen to have noticed.

green_rule's rule table was assembled by memory -- x>h, l>r, o>u, n>ng, y>i, the
dropped final velar -- each one added the day some key forced it. That is how the
n>ng rule sat unused until batch 68 even though NYAO>ngiyaw had been in the map
for months. The map now holds 5249 pairs where his spelling and the modern one
differ, ~1360 of them written by hand and checked, so the correspondences can be
counted rather than recalled.

Aligned with difflib and reported per position class, because his rules are
positional: the final velar he drops is a WORD-END rule, and folding it into a
general "delete g" would generate nonsense everywhere else.

tools/orthography/derive_correspondence_rules.py does something similar but reads
a scratchpad path from a dead session, and it scored candidate pairs rather than
shipped ones.
"""
import io, sys, json, re, collections, difflib
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/dev/formosan/seediq/taroko-pecoraro/tools/orthography/"
MM = json.load(io.open(H + "modern_map.json", encoding="utf-8"))["map"]
HUMAN = {"M", "J", "N", "C-review", "A"}

pairs = [(k, v["modern"], v["tier"]) for k, v in MM.items()
         if v["modern"] and v["modern"].lower() != k.lower()]
hum = [p for p in pairs if p[2] in HUMAN]
print("pairs where the spelling changes: %d   of which human-tier: %d" % (len(pairs), len(hum)))


def norm(w):
    return re.sub(r"[^a-z']", "", w.lower())


def rules(ps):
    sub, ins, dele = collections.Counter(), collections.Counter(), collections.Counter()
    for a, b, _ in ps:
        a, b = norm(a), norm(b)
        if not a or not b:
            continue
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            # position class: where in HIS word the edit happens
            pos = "init" if i1 == 0 else ("fin" if i2 >= len(a) else "med")
            if tag == "replace":
                sa, sb = a[i1:i2], b[j1:j2]
                if len(sa) == len(sb):
                    for n, (ca, cb) in enumerate(zip(sa, sb)):
                        p = "init" if i1 + n == 0 else ("fin" if i1 + n == len(a) - 1 else "med")
                        sub[(ca, cb, p)] += 1
                else:
                    sub[(sa, sb, pos)] += 1
            elif tag == "insert":
                ins[(b[j1:j2], pos)] += 1
            else:
                dele[(a[i1:i2], pos)] += 1
    return sub, ins, dele


for name, ps in (("ALL SHIPPED", pairs), ("HUMAN-TIER ONLY", hum)):
    sub, ins, dele = rules(ps)
    print("\n======== %s (%d pairs)" % (name, len(ps)))
    print("--- substitutions his -> modern (count >= 4)")
    for (ca, cb, p), n in sub.most_common(40):
        if n >= 4:
            print("    %-6s -> %-6s  %-5s %d" % (repr(ca), repr(cb), p, n))
    print("--- insertions: the modern word has a char his does not (count >= 4)")
    for (s, p), n in ins.most_common(24):
        if n >= 4:
            print("    +%-6s %-5s %d" % (repr(s), p, n))
    print("--- deletions: his word has a char the modern one does not (count >= 4)")
    for (s, p), n in dele.most_common(24):
        if n >= 4:
            print("    -%-6s %-5s %d" % (repr(s), p, n))
