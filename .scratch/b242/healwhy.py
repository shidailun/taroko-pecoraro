# -*- coding: utf-8 -*-
"""Why did each of the nine rows stop failing? Evidence, not a guess."""
import io
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(
    __file__))))
sys.path.insert(0, os.path.join(ROOT, "tools", "orthography"))
import suite as S                                                # noqa: E402

MAP = S.load_map()
VER = S.load_ver()
print("live MAP keys      %d" % len(MAP))
print("live VERIFIED keys %d" % len(VER))

old = subprocess.run(["git", "show", "HEAD:site/modern_map.js"], cwd=ROOT,
                     capture_output=True, text=True, encoding="utf-8").stdout
OLD = dict(re.findall(r'^"(.+?)":"(.+?)"', old, re.M))
print("HEAD MAP keys      %d" % len(OLD))
newk = sorted(set(MAP) - set(OLD))
lostk = sorted(set(OLD) - set(MAP))
print("keys ADDED vs HEAD %d %s" % (len(newk), newk))
print("keys LOST vs HEAD  %d %s" % (len(lostk), lostk))

for t in ("bsqan", "snuk", "smuk", "sloweq", "sruweq"):
    print("  %-8s map=%-10s HEAD=%-10s ver=%s" % (
        t, MAP.get(t), OLD.get(t), VER.get(MAP.get(t, ""))))
print("  bsekan verified=%s" % VER.get("bsekan"))

# what each log actually prints now
for f in ("dom232.py", "dom236.py", "dom237.py", "dom238.py"):
    _, txt, rc = S.run(f)
    print("\n=== %s rc=%d" % (f, rc))
    for line in txt.splitlines():
        if line.strip():
            print("   " + line[:150])
