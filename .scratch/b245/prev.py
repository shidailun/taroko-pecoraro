# -*- coding: utf-8 -*-
"""Sort the informant's 71 answers into the two questions the b243 sheet asked
as one, and join them to the live blocker list.

Batch 242's rule: an answer is a RESPELLING only when it is shape-continuous
with his token under HIS OWN correspondences (`o->u`, `l->r`, `x->h`, `ç` for
`x`, `'`/`"` for the schwa, final `-e` for `-i`, `q` for modern `k`); otherwise
it names the MEANING, which is a different claim and cannot spell his word.
`fold()` is that rule written as an equivalence class, so the test is one edit
distance rather than a judgement.

Prints counts and a table. Writes `.scratch/b245/prev.json` for the builder.
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
H = os.path.abspath(".")
CJK = re.compile(r"[㐀-鿿　-〿＀-￯]")
# His own status words. They are ANSWERS -- a speaker saying a word is gone is
# attesting something -- but they are answers to neither question, so they get
# their own bucket rather than being counted as meaning-answers.
GONE = re.compile(r"不用|沒有?人?用|不再|沒聽過|沒看過|不知道|不確定|不清楚|無|沒有這")


def fold(s):
    """his letters and today's, mapped onto one alphabet."""
    s = (s or "").lower().strip()
    s = re.sub(r"[（(].*?[)）]", " ", s)          # his own parenthetical gloss
    s = re.sub(r"[^a-zÀ-ſ'\"’ʼ\- ]", " ", s)
    s = s.replace("ç", "x").replace("’", "").replace("ʼ", "")
    s = re.sub(r"['\"\-]", "", s)
    for a, b in (("o", "u"), ("l", "r"), ("x", "h"), ("k", "q"), ("e", "i")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()


def ed(a, b):
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1,
                           prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def classify(his, ans):
    """-> (kind, the word part of the answer). Three kinds, no fourth."""
    if not (ans or "").strip():
        return "none", ""
    if GONE.search(ans) and not re.search(r"[a-z]", ans, re.I):
        return "gone", ""
    words = re.findall(r"[A-Za-zÀ-ſ'\"’ʼ]{2,}", ans)
    if not words:
        return "gone" if CJK.search(ans) else "none", ""
    fh = fold(his)
    best = min(words, key=lambda w: ed(fh, fold(w)))
    d = ed(fh, fold(best))
    # scale with the word: one edit in a 4-letter stem is a different word,
    # three in a 10-letter one is his schwa and his `l` showing up as writing.
    return ("respell" if d <= max(1, len(fh) // 3) else "meaning"), best


rows = json.loads(io.open(os.path.join(H, ".scratch/b245/blocked.json"),
                          encoding="utf-8").read())
ans = json.loads(io.open(os.path.join(H, ".scratch/b242/answers.json"),
                         encoding="utf-8").read())
BY = {}
for a in ans:
    BY.setdefault((a.get("raw") or "").strip().lower(), a)

live = set()
for r in rows:
    if r.get("aligned"):
        for (m, _c), (o, _c2) in zip(r["spans"], r["his"]):
            if m.lower() in r["pale"]:
                live.add(o.strip())

out, counts = {}, {"respell": 0, "meaning": 0, "gone": 0, "none": 0}
for h in sorted(live):
    a = BY.get(h.lower())
    if not a:
        continue
    kind, word = classify(h, a.get("ans", ""))
    counts[kind] += 1
    out[h] = {"n": a.get("n"), "ans": a.get("ans", "").strip(),
              "kind": kind, "word": word}

print("live blocker tokens %d | with a previous answer %d" % (len(live),
                                                              len(out)))
print("  respelling %d | meaning %d | \"no longer used\" %d | blank %d"
      % (counts["respell"], counts["meaning"], counts["gone"], counts["none"]))
for h in sorted(out, key=lambda k: out[k]["kind"]):
    d = out[h]
    print("  %-10s %-8s %s" % (h, d["kind"], d["ans"][:44]))

# The whole sheet, not only the live rows: this is the split batch 242 read by
# hand, re-derived mechanically, and its 24/47 is the number to reproduce.
whole = {"respell": 0, "meaning": 0, "gone": 0, "none": 0}
for a in ans:
    whole[classify(a.get("raw", ""), a.get("ans", ""))[0]] += 1
print("all %d answers: respelling %d | meaning %d | gone %d | blank %d"
      % (len(ans), whole["respell"], whole["meaning"], whole["gone"],
         whole["none"]))
io.open(os.path.join(H, ".scratch/b245/prev.json"), "w",
        encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
