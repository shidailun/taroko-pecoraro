# -*- coding: utf-8 -*-
"""Truku running text straight from the ILRDF parquet datasets.

`load_spoken()` in build_modern_map.py reads `C:/dev/ILRDF/ILRDF_texts.xlsx`,
which is a flattened export of these same collections — and it lost a third of
them on the way: 272,150 tokens in the xlsx against **361,630** in the parquets
the export was made from, 54,457 utterances against 47,517. 2,172 types in here
are ones `attested_modern.json` has never seen.

The class that gap falls hardest on is the one a dictionary never lists anyway:
personal names. `Sibal` is the largest single pale word on the page (47
occurrences) and the xlsx has him nowhere; the parquets have him three times,
twice unmistakably as a man — *"Hangan na o Awi Sibal"* (名叫 Awi Sibal) and
*"bukung alang Skahing Sibal Watan"* (該社領袖 Sibal Watan), given name plus
father's name, capitalized mid-sentence. That is what verifies tier N's freeze:
the community writes him with the l his own `l>r` rule would have taken away.

Eight Truku datasets, text column only — the audio is 7 GB and irrelevant here.
`ithuan_formosan_text` names its columns `formosan`/`mandarin`; the rest use
`transcript`/`translation`.

Frequency is kept and it is load-bearing. These are ASR transcripts, so a hapax
is as likely to be a mis-hearing as a word — the same reason `load_spoken()`
keeps counts. Consumers gate on it; see build_verified.py, which takes >= 2.

Run: python build_parquet_attested.py   (writes parquet_truku_freq.json)
"""
import collections, glob, io, json, os, re, sys

ROOT = "C:/dev/ILRDF/datasets"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parquet_truku_freq.json")

# Same tokenization as attested_modern.json: plain [a-z'] types. NOT norm() —
# that strips the apostrophe, and the modern values this vouches for keep it.
TOK = re.compile(r"[^A-Za-z']+")


def main():
    import pyarrow.parquet as pq

    freq = collections.Counter()
    rows = 0
    for d in sorted(glob.glob(os.path.join(ROOT, "*", "Truku"))):
        col = "formosan" if "ithuan_formosan_text" in d.replace("\\", "/") else "transcript"
        for fp in sorted(glob.glob(os.path.join(d, "*.parquet"))):
            t = pq.read_table(fp, columns=[col])
            for v in t.column(col).to_pylist():
                if not v:
                    continue
                rows += 1
                for w in TOK.split(str(v).lower()):
                    if len(w) >= 2:
                        freq[w] += 1
        print("  %-40s %6d utterances so far" % (os.path.basename(os.path.dirname(d)), rows))

    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dict(freq.most_common()), f, ensure_ascii=False)
    print("utterances %d  tokens %d  types %d  (freq>=2: %d)"
          % (rows, sum(freq.values()), len(freq),
             sum(1 for c in freq.values() if c >= 2)))
    print("wrote %s" % os.path.basename(OUT))


if __name__ == "__main__":
    main()
