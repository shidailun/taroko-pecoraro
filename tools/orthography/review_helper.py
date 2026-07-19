"""Build review_queue.json — the 149 unresolved tokens from modern_map.json's
"review" key, enriched with dictionary context and omnibus candidate glosses,
sorted by display frequency so high-impact words come first.

Each item carries a status ("pending" until adjudicated in-session); decisions
land in manual_map.json and the generator is rerun, so this file is a worksheet,
not a source of truth.
"""
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_modern_map as g

HERE = os.path.dirname(os.path.abspath(__file__))
QUEUE = os.path.join(HERE, "review_queue.json")


def entry_contexts(entries, wanted):
    """norm(token) -> up to 4 places it appears, with glosses."""
    ctx = collections.defaultdict(list)

    def hit(text, kind, hw, gloss_en, gloss_zh, sent=None):
        for t in g.TOKEN_RE.findall(text or ""):
            n = g.norm(t)
            if n in wanted and len(ctx[n]) < 4:
                ctx[n].append({
                    "raw": t, "kind": kind, "entry": hw,
                    "en": (gloss_en or "")[:120], "zh": (gloss_zh or "")[:60],
                    "sent": sent,
                })

    for e in entries:
        hw = e.get("hw", "")
        hit(hw, "headword", hw, e.get("en"), e.get("zh"))
        hit(e.get("paradigm"), "paradigm", hw, e.get("en"), e.get("zh"))
        for x in e.get("examples", []):
            hit(x.get("t"), "example", hw, x.get("en"), x.get("zh"), x.get("t"))
        for s in e.get("subs", []):
            hit(s.get("form"), "sub-form", hw, s.get("en"), s.get("zh"))
            hit(s.get("paradigm"), "paradigm", hw, s.get("en"), s.get("zh"))
            for x in s.get("examples", []):
                hit(x.get("t"), "example", hw, x.get("en"), x.get("zh"), x.get("t"))
    return ctx


def main():
    data = json.load(open(os.path.join(HERE, "modern_map.json"), encoding="utf-8"))
    review = data["review"]

    src = open(g.ENTRIES, encoding="utf-8").read()
    src = src[src.index("window.ENTRIES =") + len("window.ENTRIES ="):].strip().rstrip(";")
    entries = json.loads(src)

    wanted = {g.norm(t) for t in review}
    ctx = entry_contexts(entries, wanted)
    word_raw, word_gloss, sent_best = g.load_omnibus()

    queue = []
    for tok, info in review.items():
        n = g.norm(tok)
        cands = []
        for c in info.get("cands", []):
            cn = g.norm(c["cand"])
            cands.append({
                "cand": c["cand"],
                "attested": "Words" if c.get("words") else ("Sentences" if cn in sent_best else "no"),
                "omnibus_zh": sorted(word_gloss.get(cn, []))[:4],
                "dist": c.get("dist"),
            })
        queue.append({
            "token": tok,
            "freq": info.get("freq", 0),
            "contexts": ctx.get(n, []),
            "candidates": cands,
            "status": "pending",
            "decision": None,
        })

    queue.sort(key=lambda q: (-q["freq"], q["token"]))
    json.dump(queue, open(QUEUE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"wrote {QUEUE}: {len(queue)} items, "
          f"{sum(1 for q in queue if q['status'] == 'pending')} pending")


if __name__ == "__main__":
    main()
