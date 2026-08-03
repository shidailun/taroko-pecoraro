# -*- coding: utf-8 -*-
"""Worksheets for the words only a speaker can settle — asked per ROOT.

**What is actually left.** Of 1,123 pale occurrences: 612 reach no listed root
under any analysis, and there is no proposal to put in front of anybody for
those. 307 reach a root the wordlist glosses and the two glosses **disagree**.
122 reach a root the wordlist **lists and never glosses**, so `_agrees` returns
None for want of anything to read. 81 have no gloss of his to test with.

The last computational idea was measured and refused. `_his_glosses` gives a SUB
the parent card's gloss only when the sub's own gloss is a pointer (參見, 的過去
式), so a sub with a gloss of its own is judged with the root card he wrote it on
invisible — `Skdolox` 直－真誠－誠實 weighed without `KDOLOX` 牆—整齊排列的堆疊
standing over it. That looked like the structural gap behind the whole bucket. It
buys **zero** occurrences: 135 candidates have no parent gloss to read, and for
the other 192 the parent disagrees exactly as the sub did. The gap is real and it
is not load-bearing. Feeding in more of HIS Chinese cannot settle a question that
turns on what the modern word means.

**So the unit of adjudication is the ROOT, not the word.** Asking 300-odd times
whether a word comes from a root is the expensive question; asking once per root
is the cheap one, and one answer unlocks a paradigm — `dagi` alone holds
`pspdagi`, `pspdagun`, `pspdagan` and `pnspdagan`, ten occurrences.

Two kinds of row, because there are two kinds of silence:

- **The wordlist glosses the root and says something else.** His `Tnbuyan` is 餵
  and `buya` is not that. Print both glosses and ask which is right — he may be
  wrong, the wordlist may be a homograph, or the word may not be that root.
- **The wordlist lists the root and glosses nothing.** Nobody has said what
  `dagi` means. Print his Chinese as a PROPOSAL and ask for the meaning.

His Chinese is never the answer, only the proposal. A speaker contradicting him
is the most valuable outcome on the sheet and the one that keeps a wrong spelling
off the page.

A NO is as good as a YES. A root ruled out stays pale for a reason that gets
written down, which is what every PIN in the logs is. Nothing here should be
scored until it is ruled — the census moves on the respelling, not on the sheet.

`python build_worksheets.py <pale.json>`; writes `worksheets/sheetNN.md`.
"""
import sys
import io
import os
import re
import json
import glob
import collections

sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
os.chdir(H)
sys.path.insert(0, H)
from inflection import Inflection, TOK, wkey  # noqa: E402

B = os.path.join(H, "..", "..")
PER_SHEET = 15


def his_cards():
    """raw token key -> (page, headword, its gloss, sub line, its gloss, example)"""
    out = collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(B, "data", "batch_*.json"))):
        d = json.load(io.open(f, encoding="utf-8"))
        lo, hi = d["pages"][0], d["pages"][-1]
        n = max(1, len(d["entries"]))

        def ex(o):
            for x in (o.get("examples") or []):
                if x.get("t") and x.get("zh"):
                    return (x["t"], x["zh"])
            return None

        for i, e in enumerate(d["entries"]):
            pg = lo + int(round((hi - lo) * i / float(n)))
            hw, zh = e.get("hw") or "", e.get("zh") or ""
            for fld in ("hw", "paradigm"):
                for mm in TOK.finditer(e.get(fld) or ""):
                    out[wkey(mm.group(0))].append((pg, hw, zh, None, None, ex(e)))
            for sb in e.get("subs", []):
                for fld in ("form", "paradigm"):
                    for mm in TOK.finditer(sb.get(fld) or ""):
                        out[wkey(mm.group(0))].append(
                            (pg, hw, zh, sb.get("form"), sb.get("zh") or "",
                             ex(sb) or ex(e)))
    return out


def main(palepath):
    lex = set(json.load(io.open("attested_modern.json", encoding="utf-8")))
    src = io.open(os.path.join(B, "site", "modern_map.js"), encoding="utf-8").read()
    mp = dict(re.findall(r'"([^"]+)"\s*:\s*"([^"]*)"', src))
    inf = Inflection(lex, mp)
    cards = his_cards()
    pale = json.load(io.open(palepath, encoding="utf-8"))

    def txt(g):
        return "／".join(str(x.get("zh") or "") if isinstance(x, dict) else str(x)
                         for x in (g if isinstance(g, (list, set, tuple)) else [g]))

    grp = collections.defaultdict(lambda: [0, {}])
    for w, n in pale.items():
        rs = {a[0] for a in (inf.roots(w) or [])}
        if not rs:
            continue                      # nothing to propose; not a sheet row
        his = inf._his(w, slots_only=True)
        for r in rs:
            g = inf.gl.get(r)
            if g and his and inf._agrees(his, r):
                continue                  # agrees; it is pale for another reason
            grp[r][0] += n
            grp[r][1][w] = n
    rows = sorted(grp.items(), key=lambda kv: (-kv[1][0], kv[0]))

    od = os.path.join(H, "worksheets")
    if not os.path.isdir(od):
        os.mkdir(od)
    for old in glob.glob(os.path.join(od, "sheet*.md")):
        os.remove(old)

    ns = 0
    for s in range(0, len(rows), PER_SHEET):
        ns += 1
        chunk = rows[s:s + PER_SHEET]
        with io.open(os.path.join(od, "sheet%02d.md" % ns), "w",
                     encoding="utf-8") as fh:
            fh.write("# 太魯閣語詞根確認表 %02d\n\n" % ns)
            fh.write("表裡的中文是 Pecoraro 神父 1977 年寫的，只是**參考**，不一定對。\n"
                     "有兩種問題：詞典有解釋的，問哪一個對；詞典沒有解釋的，問是什麼意思。\n"
                     "答「不是」「沒有這個詞根」跟答「是」一樣有用。\n\n")
            for i, (root, (occ, ws)) in enumerate(chunk, 1):
                dictgl = txt(inf.gl.get(root) or "")
                fh.write("### %d. 詞根 **`%s`**%s　（%d 個詞／%d 處）\n\n"
                         % (s + i, root,
                            ("　現代詞典：**%s**" % dictgl[:40]) if dictgl
                            else "　現代詞典**收了這個詞，但沒有寫意思**", len(ws), occ))
                fh.write("| 現代拼法 | 他的拼法 | 他的詞條 | 他的中文 |\n"
                         "|---|---|---|---|\n")
                seen_ex, pgs = [], []
                for w in sorted(ws, key=lambda x: -ws[x]):
                    raws = sorted(inf.inv.get(w) or [])
                    rec = None
                    for k in raws:
                        if cards.get(k):
                            rec = cards[k][0]
                            break
                    if not rec:
                        continue
                    pg, hw, zh, form, szh, ex = rec
                    pgs.append(pg)
                    fh.write("| `%s` ×%d | %s | %s %s | %s |\n"
                             % (w, ws[w], "、".join(raws)[:26], hw,
                                ("／" + zh[:18]) if zh else "",
                                (szh or zh or "（無）")[:30]))
                    if ex and len(seen_ex) < 2 and ex not in seen_ex:
                        seen_ex.append(ex)
                for t, z in seen_ex:
                    fh.write("\n> %s\n> 　%s\n" % (t, z))
                pg = min(pgs) if pgs else "?"
                if dictgl:
                    fh.write("\n**上面這些詞，是不是 `%s`（%s）？**　（約 p.%s）\n\n"
                             "　□ 是，神父的中文寫錯了　□ 不是，是別的詞根：__________\n"
                             "　□ 是同音異義（兩個 `%s`）　說明：____________________\n\n"
                             % (root, dictgl[:20], pg, root))
                else:
                    fh.write("\n**`%s` 是什麼意思？**　（約 p.%s）\n\n"
                             "　意思：____________________　"
                             "□ 神父說的對　□ 沒有這個詞根\n\n" % (root, pg))
        print("sheet%02d.md  %2d roots  %3d occ" % (ns, len(chunk),
                                                    sum(c[1][0] for c in chunk)))
    # A word with two candidate roots appears on two rows, so the per-row
    # occurrence counts do not add up to coverage. Report both, and report the
    # curve: nothing is dropped, but the sheets are steeply front-loaded and a
    # speaker should know that before starting sheet 20.
    cov = {w: n for _, (_, ws) in rows for w, n in ws.items()}
    print("%d roots over %d sheets; they cover %d pale types / %d occurrences"
          % (len(rows), ns, len(cov), sum(cov.values())))
    run, half = 0, sum(cov.values()) / 2.0
    for i, (_, (o, _)) in enumerate(rows, 1):
        run += o
        if run >= half:
            print("  front-loaded: the first %d roots (sheets 1-%d) are worth "
                  "about half of it" % (i, (i + PER_SHEET - 1) // PER_SHEET))
            break
    print("  the tail is 1-occurrence roots; no rows are dropped, they are ranked")
    print("pale total %d types / %d occ; %d types (%d occ) reach no listed root "
          "at all and get no row" % (len(pale), sum(pale.values()),
                                     sum(1 for w in pale if not (inf.roots(w) or [])),
                                     sum(n for w, n in pale.items()
                                         if not (inf.roots(w) or []))))


if __name__ == "__main__":
    main(sys.argv[1])
