# -*- coding: utf-8 -*-
"""Batch 221's cheapest cut, applied to the seam sweep's 48 rows.

For each candidate value and for his own token, grep the whole record -- the
batch log, the notes, and EVERY log family (dom*, b*, ver*, chk*, lg*, freeze*)
-- and report the rows with NO prior mention. Those are the only ones worth
working; everything else is already ruled or refused in writing."""
import glob
import io
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
PZ = json.load(io.open(".scratch/b230/pale_zh.json", encoding="utf-8"))

body = []
for pat in (".claude/notes/*.md", "tools/orthography/logs/*.py", "CLAUDE.md"):
    for f in glob.glob(pat):
        body.append((f, io.open(f, encoding="utf-8", errors="ignore").read()))

rows = []
for ln in io.open(".scratch/b230/seam.log", encoding="utf-8").read().splitlines()[1:]:
    m = re.match(r"\s+(\S+)\s+->\s+(\S+)\s+d=(\d)", ln)
    if m:
        rows.append((m.group(1), m.group(2), int(m.group(3)), ln))

for val, cand, d, ln in rows:
    toks = PZ.get(val, {}).get("toks", [])
    keys = set([val, cand] + toks)
    hits = {}
    for f, t in body:
        for k in keys:
            if re.search(r"[^A-Za-z]" + re.escape(k) + r"[^A-Za-z]", t):
                hits.setdefault(f.split("/")[-1], set()).add(k)
    tag = "NEW " if not hits else "seen"
    where = ",".join(sorted(hits)[:4])
    print("%s %-13s -> %-13s d=%d  %-22s %s"
          % (tag, val, cand, d, PZ.get(val, {}).get("hw", "")[:20], where[:70]))
