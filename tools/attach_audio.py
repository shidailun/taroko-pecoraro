"""Attach TTS audio ids to site/entries.js.

Each headword / sub-form / example in entries.js is matched against
tts_full/items.json by (headword, exact Pecoraro text) and gets an `a` field
holding the clip id. The app plays  R2_PUBLIC_URL + "/" + a + ".mp3".

Run standalone to (re)inject into the current entries.js:
    python tools/attach_audio.py
build_entries.py also calls attach() so a rebuild keeps the ids.

Match is exact-text within a headword; identical repeated texts are consumed in
order. The 12 single-letter section-divider clips synthesized as silence are
skipped, so no dead play button appears on them.
"""
import json
import pathlib
from collections import defaultdict, deque

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENTRIES_JS = ROOT / "site" / "entries.js"
ITEMS = ROOT.parents[1] / "ilrdf" / "tts_full" / "items.json"

# Single-letter A–Z section headers that came out of TTS as silence
# (verified: non-lexical dividers, 0 near-silent among real content).
SILENT = {
    "hw_a", "hw_d", "hw_g", "hw_i", "hw_k", "hw_m",
    "hw_n", "hw_n_2", "hw_o", "hw_p", "hw_s", "hw_t",
}


def _index(items):
    """hw -> {'hw': id, 'form': {text: deque(ids)}, 'ex': {text: deque(ids)}}"""
    idx = defaultdict(lambda: {"hw": None, "form": defaultdict(deque), "ex": defaultdict(deque)})
    for it in items:
        g = idx[it["hw"]]
        if it["kind"] == "hw":
            g["hw"] = it["id"]
        else:
            g[it["kind"]][it["pecoraro"]].append(it["id"])
    return idx


def _take(bucket, text):
    q = bucket.get(text)
    if q:
        return q.popleft()
    return None


def attach(entries, items=None):
    """Mutate entries in place, adding `a` clip-id fields. Returns coverage counts."""
    if items is None:
        items = json.loads(ITEMS.read_text(encoding="utf-8"))
    idx = _index(items)
    n = defaultdict(int)

    def use(cid, node):
        if cid and cid not in SILENT:
            node["a"] = cid
            return True
        node.pop("a", None)  # keep idempotent: drop stale/silent ids
        return False

    # Examples only: headwords and sub-forms deliberately get NO audio button
    # (bare words came out unnatural; sentences sound right). We still pop any
    # stale `a` off hw/form so a rebuild removes old word buttons.
    for e in entries:
        g = idx.get(e["hw"])
        e.pop("a", None)
        for ex in e.get("examples", []):
            if g and use(_take(g["ex"], ex.get("t", "")), ex):
                n["ex"] += 1
        for s in e.get("subs", []):
            s.pop("a", None)
            for ex in s.get("examples", []):
                if g and use(_take(g["ex"], ex.get("t", "")), ex):
                    n["ex"] += 1
    return n


HEADER = ENTRIES_JS.read_text(encoding="utf-8").split("window.ENTRIES =")[0] + "window.ENTRIES = "


def main():
    src = ENTRIES_JS.read_text(encoding="utf-8")
    data = json.loads(src[src.index("["):src.rindex("]") + 1])
    n = attach(data)
    out = HEADER + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    ENTRIES_JS.write_text(out, encoding="utf-8")
    print(f"attached audio ids: hw={n['hw']} forms={n['form']} examples={n['ex']} "
          f"(skipped {len(SILENT)} silent letter clips) -> {ENTRIES_JS}")


if __name__ == "__main__":
    main()
