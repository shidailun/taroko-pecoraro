# -*- coding: utf-8 -*-
"""Negative control for dom223.py: tamper, confirm it refuses."""
import io, os, sys, importlib.util
sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location(
    "dom223", os.path.join("tools", "orthography", "logs", "dom223.py"))
d = importlib.util.module_from_spec(spec); spec.loader.exec_module(d)

def run(label, patch, expect):
    saved = {k: getattr(d, k) for k in patch}
    for k, v in patch.items(): setattr(d, k, v)
    buf = io.StringIO(); old = sys.stdout; sys.stdout = buf
    try: rc = d.main()
    finally:
        sys.stdout = old
        for k, v in saved.items(): setattr(d, k, v)
    out = buf.getvalue()
    hit = expect in out
    print("%-34s rc=%d  %s  %s" % (label, rc, "REFUSED" if rc else "passed",
                                   "OK" if (hit and rc) else "*** CONTROL BROKEN ***"))
    for ln in out.splitlines():
        if ln.startswith("FAIL"): print("      " + ln[:118])

real_mm = d.modern_map
run("1 map reverted to pttui",
    {"modern_map": lambda: dict(real_mm(), **{"pt'tui": "pttui"})},
    "not 'pteetui'")
run("2 audio id lost",
    {"audio_ids": lambda: set(list(d.__dict__["audio_ids"].__self__ if 0 else [])) or
                          set(range(d.AUDIO_IDS - 1))},
    "attached audio ids")
real_reg = d.register_text
run("3 register lists the bare root",
    {"register_text": lambda: real_reg() + '\n"puhir"\n'},
    "negative half of the POXEL refusal")
run("4 floor raised above the metric",
    {"FLOOR": 5332}, "FLOOR 5332")
