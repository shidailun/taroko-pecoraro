# -*- coding: utf-8 -*-
"""Where does he write about ONE card inside ANOTHER card's prose?

batch 236 ruled `teumuk` on evidence that was not on the TEUMUK card at all:
his TXOULANG note says, of TEUMUK, *que les japonais ont sans doute introduit*.
No instrument in this project looks for that. Every sweep so far reads a card
against the register, or a card against its own family; this reads his book
against ITSELF, asking which cards he cross-references in running prose.

The join is his own spelling in CAPITALS inside a `fr` or `zh` field, matched
against the headword list. Output is a candidate list only -- colour is decided
from the DOM afterwards (the map is never evidence about colour), and a hit is
a place to READ, not a ruling.

    python .scratch/b236/crossnote.py            # every cross-reference
    python .scratch/b236/crossnote.py --pale     # only those touching a pale value
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
ORTH = os.path.join(ROOT, "tools", "orthography")
SITE = os.path.join(ROOT, "site")


def entries():
    s = io.open(os.path.join(SITE, "entries.js"), encoding="utf-8").read()
    return json.loads(s[s.index("["):s.rindex("]") + 1])


def modern_map():
    t = io.open(os.path.join(SITE, "modern_map.js"), encoding="utf-8").read()
    a = t.index("window.MODERN_MAP = {")
    return dict(re.findall(r'^"(.+?)":"(.+?)",?$',
                           t[a:t.index("\n};", a) + 2], re.M))


def verified():
    t = io.open(os.path.join(SITE, "verified.js"), encoding="utf-8").read()
    return set(m.group(1) for m in re.finditer(r'^  "(.+?)": \d+,?$', t, re.M))


def char_rules(w):
    """app.js charRules(), the fallback when no map entry fires."""
    w = re.sub(r"[’ʼ\"ʔ]", "'", w)
    return w.replace("ł", "l").replace("ç", "x") \
            .replace("o", "u").replace("l", "r").replace("x", "h")


def word_key(w):
    """app.js wordKey(): folds ONLY the elision marks and l-slash (batch 219).
    It does NOT fold c-cedilla and does NOT strip the umlauts."""
    return re.sub(r"[’ʼ\"ʔ]", "'", w).lower()


# His prose is French and Chinese; a run of capitals is his own Truku. Require
# two letters so his `R`, `PA` tags and French initials do not join.
CAPS = re.compile(r"\b([A-ZÇ'\"][A-ZÇ'\"À-Ü]{1,})\b")
# French words that are legitimately capitalised in his prose and are NOT Truku
STOP = set("""R PA NB SECMI MEP TAROKO TROKO SEEDIQ TRUKU ATAYAL BUNUN
JAPON JAPONAIS CHINE CHINOIS FORMOSE TAIWAN DIEU JESUS CHRIST
LE LA LES DE DU ET OU EST CE IL ELLE ON SI NE PAS QUE QUI
CF VOIR IDEM SYN VL EMPRUNT REMARQUE NOTE""".split())


def main():
    pale_only = "--pale" in sys.argv
    E = entries()
    MM, VER = modern_map(), verified()
    heads = {}
    for e in E:
        hw = (e.get("hw") or "").strip()
        if hw:
            heads.setdefault(hw.upper(), []).append(e)

    def value(tok):
        k = word_key(tok)
        return MM.get(k) or char_rules(k)

    def looks_pale(e):
        """Offline approximation: any Truku token on this card whose value is
        not in verified.js. Confirmed from the DOM before anything is ruled --
        WORD_OVERRIDES and CITE_SPELL are invisible here (batch 230)."""
        toks = []
        hw = e.get("hw") or ""
        toks.append(hw)
        for x in e.get("examples") or []:
            toks += re.findall(r"[a-zA-Zç'\"À-ü]+",
                               str(x.get("t") or ""))
        for sb in e.get("subs") or []:
            toks.append(sb.get("form") or "")
            for x in sb.get("examples") or []:
                toks += re.findall(r"[a-zA-Zç'\"À-ü]+",
                                   str(x.get("t") or ""))
        out = []
        for t in toks:
            if not t:
                continue
            v = value(t)
            if v and all(p in VER for p in v.split()):
                continue
            out.append((t.lower(), v))
        return out

    rows, seen = [], set()
    for e in E:
        src = (e.get("hw") or "").strip()
        prose = " ".join(str(e.get(f) or "") for f in ("fr", "zh"))
        for sb in e.get("subs") or []:
            prose += " " + " ".join(str(sb.get(f) or "") for f in ("fr", "zh"))
        for m in CAPS.finditer(prose):
            tgt = m.group(1)
            if tgt in STOP or tgt == src.upper() or tgt not in heads:
                continue
            key = (src, tgt)
            if key in seen:
                continue
            seen.add(key)
            ctx = prose[max(0, m.start() - 60):m.end() + 60].replace("\n", " ")
            rows.append((src, tgt, ctx))

    print("%d cross-references, %d distinct source cards"
          % (len(rows), len(set(r[0] for r in rows))))

    hot = []
    for src, tgt, ctx in rows:
        sp = [p for e in heads.get(src.upper(), []) for p in looks_pale(e)]
        tp = [p for e in heads[tgt] for p in looks_pale(e)]
        if sp or tp:
            hot.append((src, tgt, sp, tp, ctx))
    print("%d touch a card with at least one unverified value" % len(hot))

    if pale_only:
        for src, tgt, sp, tp, ctx in hot:
            print("\n%s -> %s" % (src, tgt))
            if sp:
                print("   src pale: %s" % sorted(set(sp))[:5])
            if tp:
                print("   tgt pale: %s" % sorted(set(tp))[:5])
            print("   ...%s..." % ctx.strip()[:150])
    return 0


if __name__ == "__main__":
    sys.exit(main())
