"""Driver for look.py: the tokens carry apostrophes, and bash eats them.

Usage: python l58.py <group>
"""
import sys, io, runpy
sys.stdout.reconfigure(encoding="utf-8")

GROUPS = {
    "lu":  ["gn'lu", "nsl'lu", "pn'mu", "n'mu", "nn'mu"],
    "a":   ["plilyes", "tityeq", "mptbagun", "mpad'gal", "mpaba'ba"],
    "b":   ["maidang", "luula", "lnnngat", "knqogo", "ttidyal"],
    "c":   ["sktadao", "s'xgun", "ptbnxani", "pstlmai", "pbl'xun"],
    "d":   ["mpslexlax", "knwuaan", "gqoaq", "dmnsuwai", "daxani"],
    "e":   ["xolao", "tsgsutun", "tkui", "sia", "poqe"],
    "f":   ["slap", "smilap", "sqti", "dlnai", "dmt'basyaq"],
    "g":   ["pausa", "pousal", "psaanak", "siipa", "tblae"],
    "h":   ["pbbagi", "xandolu", "upsk'la", "lxlixao", "tinalu"],
    "i":   ["ptlyaon", "psnnai", "lnglngan", "splan", "npamanu"],
}
sys.argv = ["look.py"] + GROUPS[sys.argv[1]]
runpy.run_path("look.py", run_name="__main__")
