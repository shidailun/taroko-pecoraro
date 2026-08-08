# -*- coding: utf-8 -*-
"""Negative control for dom230.py (batch 209's rule: a check that cannot fail is
a list of excuses).

Measures the DOM ONCE, then replays main() against tampered copies of the DOM
reading and of every table the log consults. Each case names the assertion it
attacks; a case that does not raise the failure count is itself a failure."""
import copy
import io
import importlib.util
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
spec = importlib.util.spec_from_file_location(
    "dom230", "tools/orthography/logs/dom230.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

REAL = M.measure()
BASE = {"measure": lambda: copy.deepcopy(REAL),
        "modern_map": M.modern_map, "verified": M.verified,
        "sources": M.sources, "entries_strings": M.entries_strings,
        "his_tokens": M.his_tokens, "audio_ids": M.audio_ids,
        "entries_json": M.entries_json}


def run(**over):
    for k, v in BASE.items():
        setattr(M, k, v)
    for k, v in over.items():
        setattr(M, k, v)
    buf, old = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        rc = M.main()
    finally:
        sys.stdout = old
    return rc, buf.getvalue()


def mm(**edit):
    d = M.modern_map()
    for k, v in edit.items():
        if v is None:
            d.pop(k, None)
        else:
            d[k] = v
    return lambda: d


def ver(**edit):
    d = M.verified()
    for k, v in edit.items():
        if v is None:
            d.pop(k, None)
        else:
            d[k] = v
    return lambda: d


def src(drop=(), addgloss=(), dropgloss=()):
    AM, AG, BG = M.sources()
    AM = set(AM) - set(drop)
    AG, BG = dict(AG), dict(BG)
    for w, g in addgloss:
        AG[w] = g
        AM.add(w)
    for w in dropgloss:
        AG.pop(w, None)
        BG.pop(w, None)
    return lambda: (AM, AG, BG)


def dom(**edit):
    d = copy.deepcopy(REAL)
    for k, v in edit.items():
        sect, word = k.split("__")
        if v is None:
            d[sect].pop(word, None)
        else:
            d[sect][word] = v
    return lambda: d


# capture the real values BEFORE any override, or a lambda that reads M.<name>
# recurses into its own replacement
_TEXT, _CNT, _IDS = M.entries_strings(), M.his_tokens(), M.audio_ids()

CASES = [
    # (name, must-fail?, overrides)
    ("baseline -- untampered, must PASS", False, {}),
    ("metric falls below the 5344 floor", True,
     {"measure": lambda: dict(REAL, ok=5343)}),
    ("denominator moves off 5429", True, {"measure": lambda: dict(REAL, tot=5428)}),
    ("a ruling drifts to a third spelling", True, {"modern_map": mm(snoxel="snuhir")}),
    ("the deleted pdaqi key comes back", True, {"modern_map": mm(pdaqi="pdai")}),
    ("a HOLD slot is 'made consistent'", True,
     {"modern_map": mm(snxelan="sneuhiran")}),
    ("the XUBAO hold is overturned quietly", True, {"modern_map": mm(xubao="hibaw")}),
    ("a ruled value leaves verified.js", True, {"verified": ver(sneuhir=None)}),
    ("pnspngan stops being an id-tier hit", True, {"verified": ver(pnspngan=7)}),
    ("a ruled value renders pale", True, {"measure": dom(unv__pdai=2)}),
    ("a refused value goes dark with nobody deciding", True,
     {"measure": dom(unv__snuk=None)}),
    ("furniture turns up inside a .truku box", True,
     {"measure": dom(inTruku__hubaw=1)}),
    ("the gloss that ruled sneuhir leaves", True, {"sources": src(dropgloss=("sneuhir",))}),
    ("the bare root uhir leaves the register", True, {"sources": src(drop=("uhir",))}),
    ("bible_gloss stops carrying 試探 -- batch 201's refusal returns", True,
     {"sources": src(dropgloss=("pnspngan", "pspngan", "empspung", "pspngi"))}),
    ("an -an of the uhir stem enters the register", True,
     {"sources": src(addgloss=(("sneuhiran", ["嫉妒的原因"]),))}),
    ("a refused word becomes listed", True,
     {"sources": src(addgloss=(("snuk", ["釘子"]),))}),
    ("饕 acquires a carrier", True,
     {"sources": src(addgloss=(("basiyaq", ["饕餮"]),))}),
    ("牢 acquires a second carrier", True,
     {"sources": src(addgloss=(("theyan", ["釘不牢"]),))}),
    ("hibaw leaves -- batch 68's premise would be true again", True,
     {"sources": src(drop=("hibaw",))}),
    ("his sentence is edited under the log", True,
     {"entries_strings": lambda: "nothing"}),
    ("the corrected reading pdaqi returns to his text", True,
     {"entries_strings": lambda: _TEXT + "\nYa nami bi pdaqi"}),
    ("his own count of pstui moves", True,
     {"his_tokens": lambda: dict(_CNT, pstui=2)}),
    ("an audio id is re-minted", True, {"audio_ids": lambda: _IDS - {
        "ex_ya_nami_bi_pdaqi_pspngan_ni_pstui_nami_p"}}),
    ("the audio id count moves", True,
     {"audio_ids": lambda: _IDS | {"ex_fake"}}),
]

worst = 0
for name, must, over in CASES:
    rc, out = run(**over)
    good = (rc != 0) if must else (rc == 0)
    print("%-4s %-58s rc=%d %s" % ("ok" if good else "BAD", name, rc,
                                   "" if good else out.strip()[:150]))
    if not good:
        worst = 1
print("\ncontrol %s" % ("PASSED" if not worst else "FAILED"))
sys.exit(worst)
