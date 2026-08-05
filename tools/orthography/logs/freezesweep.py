# -*- coding: utf-8 -*-
"""The gloss test, run over every headword the map renders dark.

A homograph freeze is a raw token mapped onto a same-shaped modern word with an
unrelated gloss (CLAUDE.md). It is invisible to every colour metric because the
span is already dark; only the gloss can find it. Batch 201 found seven by hand,
batch 205 two more from a pairing file. This asks the whole book at once.

Summary line only, plus the ranked candidates. Never prints card bodies.
"""
import sys, json, re, io, unicodedata, collections
sys.stdout.reconfigure(encoding="utf-8")

R = "C:/dev/formosan/seediq/taroko-pecoraro/"
s = io.open(R + "site/entries.js", encoding="utf-8").read()
E = json.loads(s[s.index("=") + 1:].rstrip().rstrip(";"))
mm = io.open(R + "site/modern_map.js", encoding="utf-8").read()
i = mm.index("window.MODERN_MAP = {")
j = mm.index(chr(10) + "};", i)
M = json.loads(mm[i + len("window.MODERN_MAP = "):j + 1] + "}")
VER = set(m.group(1) for m in re.finditer(
    r'^  "(.+?)":', io.open(R + "site/verified.js", encoding="utf-8").read(), re.M))
AG = json.load(open(R + "tools/orthography/attested_gloss.json", encoding="utf-8"))
PF = json.load(open(R + "tools/orthography/parquet_truku_freq.json", encoding="utf-8"))

# Characters that carry no lexical weight: they make two unrelated glosses look
# related, which is the one failure mode this sweep cannot afford.
STOP = set("的了是在和與或有不無人事物：；，。、（）()？?！!－-—…《》「」"
           "一二三四五六七八九十個之其他某這那要會能所為用做作上下中大小多少"
           "0123456789 ")


def chars(g):
    return set(g) - STOP


def key(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return t.replace("ç", "x").replace('"', "'").replace("\u2019", "'")


def reg(w):
    v = AG.get(w)
    return "；".join(v) if isinstance(v, list) else (v or "")


# --- walk every card and sub-form: his gloss vs the register's, on the value
#     the map actually renders there ---
rows = []
seen_pairs = set()
for e in E:
    for form, zh in ([(e["hw"], e.get("zh") or "")] +
                     [(sb.get("form", ""), sb.get("zh") or "")
                      for sb in e.get("subs", [])]):
        form = re.sub(r"\(.*?\)", " ", form)          # drop his parentheticals
        toks = [t for t in re.findall(r"[A-Za-z\u00c7\u00e7'\u2019\"]+", form) if len(t) > 2]
        if len(toks) != 1 or not zh:
            continue                                  # multi-word heads have no single key
        k = key(toks[0])
        v = M.get(k)
        if not v or v not in VER:
            continue                                  # only dark spans can be dark AND wrong
        g = reg(v)
        if not g:
            continue                                  # no register gloss = nothing to test
        if (k, v) in seen_pairs:
            continue
        seen_pairs.add((k, v))
        hc, gc = chars(zh), chars(g)
        if not hc or not gc:
            continue
        if hc & gc:
            continue                                  # they agree; not a freeze
        rows.append((k, v, zh, g, PF.get(v, 0)))

print("dark single-token headwords tested: %d" % len(seen_pairs))
print("his gloss shares NO character with the register's: %d" % len(rows))

# --- rank: a freeze is worth more when the frozen-onto word is COMMON (so the
#     collision is real, not a rare homograph) ---
rows.sort(key=lambda r: -r[4])
print("\nranked by how common the word it froze onto is:")
for k, v, zh, g, f in rows[:40]:
    print("  %-13s -> %-13s pq=%-5d his=%-20s reg=%s"
          % (k, v, f, zh[:20], g[:26]))
json.dump(rows, open(sys.argv[1], "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
