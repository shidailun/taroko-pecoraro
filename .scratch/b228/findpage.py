# -*- coding: utf-8 -*-
"""Which scan page carries a token? Reads data/batch_*.json's own page list."""
import glob
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOK = (sys.argv[1] if len(sys.argv) > 1 else "xxtlan").lower()

for p in sorted(glob.glob(os.path.join(ROOT, "data", "batch_*.json"))):
    d = json.load(io.open(p, encoding="utf-8"))
    blob = json.dumps(d.get("entries"), ensure_ascii=False).lower()
    if TOK not in blob:
        continue
    print("%s  pages %s" % (os.path.basename(p), d.get("pages")))
    for e in d["entries"]:
        s = json.dumps(e, ensure_ascii=False)
        if TOK in s.lower():
            print("  under %-10s %s" % (e.get("hw"), (e.get("fr") or "")[:46]))
            for m in re.finditer(r'"t": "([^"]*%s[^"]*)"' % TOK, s, re.I):
                print("    § %s" % m.group(1))
