# -*- coding: utf-8 -*-
"""One blocker's dossier, printed for a ruling.

    python tools/orthography/logs/rule.py tksaw
    python tools/orthography/logs/rule.py --next 3      (top of blockers.md)

blockers.md ranks; this reads. The two are deliberately separate, because the
ranking is a fact about how many pairs a word blocks and the dossier is the
evidence for what the word IS — and the second is the only one a ruling may be
made on. A row that says "4 pairs" is a reason to look first, never a reason to
say yes.

WHAT IS PRINTED, AND WHY EACH PART. His own spelling and his own gloss for the
form, because the claim being ruled on is "this is how that word is written
today" and the gloss is what identifies which word it is. Every sentence the
token stands in, not just the one blockers.md samples — a paradigm form often
occurs three or four times and one context can mislead where four do not. The
analyses with the root's modern gloss, because that is exactly what the gate
saw. And the count it would free, last, so it is read after the evidence.

Nothing here proposes a verdict. `regular()` already refused; if the refusal was
right the row is a no, and the shape of the row cannot tell you which.
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ORTH = os.path.dirname(HERE)
H = os.path.dirname(os.path.dirname(ORTH))
SITE = os.path.join(H, "site")
sys.path.insert(0, ORTH)
os.chdir(ORTH)
from inflection import HAND_RULED, Inflection

TOKEN = re.compile(u"[A-Za-zÀ-ÿłŁʔ'’ʼ\"]+")


def read(p):
    return io.open(p, encoding="utf-8").read()


def wkey(w):
    return re.sub(u"[’ʼ\"ʔ]", "'", (w or "").lower()).replace(u"ł", "l")


def main():
    src = read(os.path.join(SITE, "entries.js"))
    E = json.loads(re.sub(r",(\s*[}\]])", r"\1",
                          src[src.index("["):src.rindex(";")]))
    m = read(os.path.join(SITE, "modern_map.js"))
    a = m.index("window.MODERN_MAP = {") + len("window.MODERN_MAP = ")
    mp = json.loads(m[a:m.index("\n};", a) + 2])
    app = read(os.path.join(SITE, "app.js"))
    ob = app.index("var WORD_OVERRIDES")
    ov = dict(re.findall(r"['\"]([^'\"]+)['\"]\s*:\s*['\"]([^'\"]+)['\"]",
                         app[ob:app.index("\n  };", ob)]))
    lex = set(json.load(io.open(os.path.join(ORTH, "attested_modern.json"),
                                encoding="utf-8")))
    inf = Inflection(lex, mp)

    def modern(t):
        x = ov.get(t, mp.get(t))
        if isinstance(x, dict):
            x = x.get("modern")
        return (x or t).strip().lower()

    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    if "--next" in sys.argv:
        n = int(args[0]) if args else 1
        md = read(os.path.join(HERE, "blockers.md"))
        cut = md.index("## gloss disagrees")
        # Skip what has already been decided, in either direction. Without this
        # the queue hands back the top of the list forever: a refusal does not
        # change blockers.md, because a refused word still blocks its pairs.
        done = set(HAND_RULED)
        rf = os.path.join(HERE, "refused.txt")
        if os.path.exists(rf):
            done |= {l.split()[0] for l in io.open(rf, encoding="utf-8")
                     if l.strip() and not l.startswith("#")}
        args = [w for w in re.findall(r"^### (\S+) ", md[cut:], re.M)
                if w not in done][:n]

    for want in args:
        want = want.lower()
        # Everywhere his text has a token that renders as this value. A ruling is
        # about the VALUE, so all of his spellings that reach it come along.
        hits = []
        for e in E:
            def scan(x, where, gl):
                for mm in TOKEN.finditer(x.get("t") or ""):
                    if modern(wkey(mm.group(0))) == want:
                        hits.append((mm.group(0), where, gl, x))
                        return
            for x in e.get("examples") or []:
                scan(x, e["hw"], e)
            for s in e.get("subs") or []:
                for x in s.get("examples") or []:
                    scan(x, e["hw"] + u" › " + s["form"], s)

        print(u"\n" + u"═" * 70)
        print(u"  %s   — %d sentence%s"
              % (want, len(hits), "" if len(hits) == 1 else "s"))
        print(u"═" * 70)
        spell = sorted({h[0] for h in hits})
        print(u"  his spelling%s: %s"
              % ("" if len(spell) == 1 else "s", u", ".join(spell)))
        for c, p, sf, slot in inf.roots(want)[:5]:
            g = u"／".join(sorted(inf._gloss(c))) or u"(no modern gloss)"
            print(u"  %-22s root %-10s %s"
                  % (u"%s%s%s" % (p + "-" if p else "", c,
                                  "-" + sf if sf else ""), c, g))
        if not inf.roots(want):
            print(u"  no analysis reaches a listed root")
        seen_form = set()
        for tok, where, gl, x in hits:
            if where not in seen_form:
                seen_form.add(where)
                print(u"\n  ── %s" % where)
                for k, lab in (("fr", "FR"), ("zh", "中")):
                    if gl.get(k):
                        print(u"     %s %s" % (lab, gl[k].strip()))
            print(u"\n     § %s" % (x.get("t") or "").strip())
            for k, lab in (("fr", "FR"), ("zh", "中")):
                if x.get(k):
                    print(u"       %s %s" % (lab, x[k].strip()))
    print("")


if __name__ == "__main__":
    main()
