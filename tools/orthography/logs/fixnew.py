"""Replace dom57.py's hand-copied NEW dict with a read of b57.py's FIX.

The batch changed six times while I was chasing why five keys would not land, and
a transcribed copy of it silently kept asserting the withdrawn ones. A checker that
holds its own copy of the batch is a checker that can pass the wrong batch.
"""
import io, re
p = "dom57.py"
s = io.open(p, encoding="utf-8").read()
i, j = s.index("NEW = {"), s.index("\n}\n", s.index("NEW = {")) + 3
s = s[:i] + (
    '# read from the batch file itself -- never a second copy (see fixnew.py)\n'
    '_b = io.open("b57.py", encoding="utf-8").read()\n'
    '_ns = {}\n'
    'exec(_b[_b.index("FIX = {"):_b.index("\\n}\\n", _b.index("FIX = {")) + 3], _ns)\n'
    'NEW = _ns["FIX"]\n') + s[j:]
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("dom57.py now reads FIX from b57.py")
