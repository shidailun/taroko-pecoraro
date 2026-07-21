"""Merge data/batch_*.json into site/entries.js.

Batches are ordered by first page. A batch's `leadin` (continuation text at the
top of its first page) is merged into the previous batch's final entry:
running fr/en/zh text is appended, examples/subs are extended.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "site" / "entries.js"

# Pages with no dictionary content (section dividers, blank pages) that are
# legitimately absent from every batch. Checked against scans/full/page_NNN.png
# before being added here — don't add a page just to silence a warning.
KNOWN_EMPTY_PAGES = {389}  # "APPENDICES" title page + table of contents, no entries

HEADER = """\
// Pecoraro Taroko dictionary — full digitization.
// Source: Ferdinando Pecoraro, Essai de dictionnaire taroko-français (SECMI, Paris, 1977).
// Truku forms and French glosses transcribed from the 398-page scan; English and
// Chinese translated from the French (draft, pending native-speaker review).
window.ENTRIES = """


def merge_leadin(prev_entry, leadin):
    for key in ("fr", "en", "zh"):
        cont = (leadin.get(key) or "").strip()
        if cont:
            base = (prev_entry.get(key) or "").rstrip()
            joiner = " " if base and not base.endswith("-") else ""
            prev_entry[key] = (base + joiner + cont).strip()
    tail = prev_entry["subs"][-1] if prev_entry.get("subs") else prev_entry
    tail.setdefault("examples", []).extend(leadin.get("examples") or [])
    prev_entry.setdefault("subs", []).extend(leadin.get("subs") or [])
    prev_entry.pop("truncated", None)


def main():
    batches = []
    for f in sorted(DATA.glob("batch_*.json")):
        with open(f, encoding="utf-8") as fh:
            b = json.load(fh)
        b["_file"] = f.name
        batches.append(b)
    batches.sort(key=lambda b: b["pages"][0])

    # coverage check
    for a, b in zip(batches, batches[1:]):
        missing = set(range(a["pages"][1] + 1, b["pages"][0]))
        if missing and missing <= KNOWN_EMPTY_PAGES:
            print(f"NOTE: {a['_file']}/{b['_file']} skip known-empty page(s) {sorted(missing)}")
        elif b["pages"][0] != a["pages"][1] + 1:
            print(f"WARNING: gap/overlap between {a['_file']} (ends {a['pages'][1]}) "
                  f"and {b['_file']} (starts {b['pages'][0]})")

    # Boundary audit: a batch whose last entry is truncated should be followed
    # by a batch with a leadin. Flag mismatches so they can be eyeballed.
    for a, b in zip(batches, batches[1:]):
        a_trunc = bool(a["entries"] and a["entries"][-1].get("truncated"))
        b_lead = b.get("leadin") is not None
        if a_trunc and not b_lead:
            print(f"BOUNDARY: {a['_file']} ends truncated ({a['entries'][-1]['hw']}) "
                  f"but {b['_file']} has NO leadin — verify p{b['pages'][0]} top")
        if b_lead and not a_trunc:
            print(f"BOUNDARY: {b['_file']} has a leadin but {a['_file']} last entry "
                  f"({a['entries'][-1]['hw'] if a['entries'] else '?'}) not marked truncated — "
                  f"usually fine (leadin = extra subs) but check")

    entries = []
    for b in batches:
        lead = b.get("leadin")
        if lead and entries:
            merge_leadin(entries[-1], lead)
        elif lead:
            print(f"WARNING: {b['_file']} has leadin but no previous entry")
        for e in b["entries"]:
            e.setdefault("tag", "")
            e.setdefault("examples", [])
            e.setdefault("subs", [])
            entries.append(e)

    # A truncated flag on a non-final entry is only meaningful if the following
    # batch supplied a leadin to merge; after merging, clear all stray flags.
    for e in entries:
        e.pop("truncated", None)

    for e in entries:
        e.pop("_file", None)

    # Re-attach TTS audio-clip ids (a) matched from tts_full/items.json so a
    # rebuild never drops the play buttons. See tools/attach_audio.py.
    try:
        from attach_audio import attach
        n = attach(entries)
        print(f"attached audio: hw={n['hw']} forms={n['form']} examples={n['ex']}")
    except Exception as ex:  # audio manifest optional; build still succeeds without it
        print(f"note: audio not attached ({ex})")

    js = HEADER + json.dumps(entries, ensure_ascii=False, indent=2) + ";\n"
    OUT.write_text(js, encoding="utf-8")
    n_subs = sum(len(e["subs"]) for e in entries)
    n_ex = sum(len(e["examples"]) + sum(len(s.get("examples", [])) for s in e["subs"])
               for e in entries)
    print(f"{len(entries)} root entries, {n_subs} sub-forms, {n_ex} examples "
          f"-> {OUT}")
    heads = [e["hw"] for e in entries]
    disorder = [(a, b) for a, b in zip(heads, heads[1:])
                if re.sub(r"[^A-Za-z]", "", a).lower() > re.sub(r"[^A-Za-z]", "", b).lower()]
    if disorder:
        print(f"note: {len(disorder)} adjacent pairs out of alphabetical order "
              f"(first few: {disorder[:5]}) — usually fine (Pecoraro's own ordering)")


if __name__ == "__main__":
    main()
