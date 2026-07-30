"""Generic look.py driver: tokens carry apostrophes and bash eats them, so the
list lives here and is chosen by index.

  python lg.py 0
"""
import sys, runpy
sys.stdout.reconfigure(encoding="utf-8")

TOK = """tepyaq lmngut lngutan lngut plngut
tqodap ptqodap siba mskoto dmao
mdao tao m'eq kdapan likut
tnlikut bsqlol kmubui ayoq kndoto
waqat s'lno snoqo olo pisux
dilam kakox mtmoxong mngusyex psqexon
ptabe ptatwi pntipyaq sq'tqot q'tqot
swatan biri ksudan tbilan lex""".split("\n")
sys.argv = ["look.py"] + TOK[int(sys.argv[1])].split()
runpy.run_path("look.py", run_name="__main__")
