# -*- coding: utf-8 -*-
"""Can a paradigm-only token be LABELLED, and against what?

A label like "locative focus of KUGUS" is only honest if the slot is derivable.
inflection.py's inventory is the authority: -un PF, -an LF, -i/-ay/-aw/-ani
imperative, m-/-m- AF, p- causative, s- referential, n-/-n- preterite. Test each
paradigm-only token against the OTHER tokens on its own ° line -- the shortest
one is his citation form -- and report how many decompose.
"""
import io, json, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")

H = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
s = io.open(os.path.join(H, "site", "entries.js"), encoding="utf-8").read()
E = json.loads(s[s.index("["):s.rindex("]") + 1])

TOK = re.compile(r"[A-Za-z'’ʼʔ\"çÇłöÖäÄ]+")
def keys(t):
    out = []
    for m in TOK.findall(t or ""):
        k = re.sub(r"[’ʼʔ\"]", "'", m).lower().strip("'")
        if len(k) >= 2 and re.search(r"[a-z]", k):
            out.append(k)
    return out

SUF = [("aneyi", "imperative"), ("anay", "imperative"), ("ani", "imperative"),
       ("aan", "LF"), ("un", "PF"), ("an", "LF"),
       ("ay", "imperative"), ("aw", "imperative"), ("i", "imperative")]

forms = set()
for e in E:
    forms |= set(keys(e.get("hw")))
    for sb in e.get("subs") or []:
        forms |= set(keys(sb.get("form")))

# every ° line in the book, with the entry that prints it
lines = []
for i, e in enumerate(E):
    if e.get("paradigm"):
        lines.append((i, e["paradigm"]))
    for sb in e.get("subs") or []:
        if sb.get("paradigm"):
            lines.append((i, sb["paradigm"]))

def stem(tok):
    """His stem, as the -un/-an branch of inflection.py cuts it: the suffix may
    also have swallowed the root's final vowel."""
    for sf, name in SUF:
        if tok.endswith(sf) and len(tok) - len(sf) >= 2:
            yield tok[:-len(sf)], sf, name

labelled, unlabelled = collections.Counter(), []
seen = set()
for ei, line in lines:
    toks = keys(line)
    for t in toks:
        if t in forms or t in seen:
            continue
        seen.add(t)
        hit = None
        for base, sf, name in stem(t):
            # the base must be something on this same line, or in the book's
            # form index -- allowing for the vowel -un/-an swallow
            for c in toks + list(forms & {base, base + "a", base + "e",
                                          base + "i", base + "o", base + "u"}):
                if c == t:
                    continue
                if c == base or (len(c) == len(base) + 1 and c.startswith(base)):
                    hit = (name, c)
                    break
            if hit:
                break
        if hit:
            labelled[hit[0]] += 1
        else:
            unlabelled.append((t, E[ei]["hw"], line.strip()))

print("paradigm-only types seen on a ° line: %d" % len(seen))
print("labelled by slot, against a base on the same line or in the index:")
for k, n in labelled.most_common():
    print("   %-12s %4d" % (k, n))
print("   %-12s %4d" % ("(none)", len(unlabelled)))
print()
print("sample of the unlabelled:")
for t, hw, line in unlabelled[:15]:
    print("   %-14s %-22s %s" % (t, hw, line[:64]))
