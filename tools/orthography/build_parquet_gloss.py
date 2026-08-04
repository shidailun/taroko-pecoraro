# -*- coding: utf-8 -*-
"""The Mandarin side of the ILRDF datasets, which we had been throwing away.

`build_parquet_attested.py` reads the same eight Truku datasets and keeps only
the tokens: it answers "does this string occur in real modern Truku". Every one
of those datasets also carries a Mandarin column — `translation` on the audio
sets at 90-100% coverage, `mandarin` on `ithuan_formosan_text` at 100% — and
that half was never read at all.

WHAT IS TAKEN, AND WHAT IS REFUSED. Only rows whose Truku side is ONE token.
Those are word-gloss pairs and nothing else: `smkla` 趕上, `steetu` 上坡. A
two-word row is a phrase, and splitting its Chinese across both words is exactly
the instrument that failed for ppdsun — `baga bubu` 母親的雙手 would gloss
`baga` as 母親 as readily as 雙手, and a gate that reads a shared Han character
cannot tell which half it matched. The corpus is enormous and the temptation to
take the phrases is real; 5,000 clean pairs that mean what they say are worth
more than 30,000 that might.

Nothing here widens `seen` or `lex`. Every one of these words is a token from a
corpus already counted for attestation by build_parquet_attested.py; the only
new thing on this pass is what it MEANS.

A gloss is kept once per (word, Chinese) pair no matter how many datasets carry
it — klokah_asr and klokah_tts are the same utterances recorded twice, and
counting a gloss twice would make a doubled corpus look like a second opinion.

Run: python build_parquet_gloss.py     (writes parquet_gloss.json)
"""
import collections
import glob
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = "C:/dev/ILRDF/datasets"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "parquet_gloss.json")

# Same as build_parquet_attested.py: plain [a-z'] types, apostrophe kept.
STRIP = re.compile(r"[^A-Za-z']")
HAN = re.compile(u"[\u4e00-\u9fff]")
# Chinese that is not a gloss: an utterance-length translation, or one that is
# mostly punctuation and numerals. 14 characters is generous for a word.
MAXLEN = 14


def main():
    import pyarrow.parquet as pq

    pairs = collections.defaultdict(set)
    rows = seen = 0
    for d in sorted(glob.glob(os.path.join(ROOT, "*", "Truku"))):
        p = d.replace("\\", "/")
        tc, gc = (("formosan", "mandarin") if "ithuan_formosan_text" in p
                  else ("transcript", "translation"))
        for fp in sorted(glob.glob(os.path.join(d, "*.parquet"))):
            t = pq.read_table(fp, columns=[tc, gc])
            for a, b in zip(t.column(tc).to_pylist(), t.column(gc).to_pylist()):
                rows += 1
                if not a or not b:
                    continue
                w = str(a).strip().split()
                if len(w) != 1:
                    continue
                w = STRIP.sub("", w[0]).lower()
                z = str(b).strip()
                # A gloss must be Chinese, short, and not a bare number or
                # a punctuation fragment left by the transcriber.
                if len(w) < 2 or len(z) > MAXLEN or not HAN.search(z):
                    continue
                pairs[w].add(z)
                seen += 1
        print("  %-28s %7d rows read" % (os.path.basename(os.path.dirname(d)),
                                         rows))

    out = {w: sorted(z) for w, z in sorted(pairs.items())}
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=0, sort_keys=True)
    print("rows %d | one-word gloss rows %d | %d words, %d distinct glosses"
          % (rows, seen, len(out), sum(len(v) for v in out.values())))
    print("wrote %s" % os.path.basename(OUT))


if __name__ == "__main__":
    main()
