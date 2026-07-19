import json, difflib, collections, unicodedata, re

SCRATCH = r"C:/Users/user/AppData/Local/Temp/claude/C--dev-formosan-seediq/c9019950-6676-4f9c-827b-5410d342331e/scratchpad"
pairs = json.load(open(SCRATCH + "/gloss_pairs_close.json", encoding="utf-8"))

def norm(w):
    w = unicodedata.normalize("NFD", w)
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    w = w.lower().replace("'", "")
    return re.sub(r"[^a-z]", "", w)

sub_counts = collections.Counter()
ins_counts = collections.Counter()
del_counts = collections.Counter()

for hw, word, d, zc in pairs:
    a, b = norm(hw), norm(word)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        elif tag == "replace":
            sa, sb = a[i1:i2], b[j1:j2]
            if len(sa) == len(sb):
                for ca, cb in zip(sa, sb):
                    sub_counts[(ca, cb)] += 1
            else:
                sub_counts[(sa, sb)] += 1
        elif tag == "insert":
            ins_counts[b[j1:j2]] += 1
        elif tag == "delete":
            del_counts[a[i1:i2]] += 1

print("=== substitutions (pecoraro -> modern), count>=3 ===")
for (ca, cb), n in sub_counts.most_common(50):
    if n >= 3:
        print(f"{ca!r:8} -> {cb!r:8}  {n}")

print()
print("=== insertions (modern has extra char, count>=3) ===")
for s, n in ins_counts.most_common(20):
    if n >= 3:
        print(repr(s), n)

print()
print("=== deletions (pecoraro has extra char, count>=3) ===")
for s, n in del_counts.most_common(20):
    if n >= 3:
        print(repr(s), n)
