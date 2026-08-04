# -*- coding: utf-8 -*-
"""The ILRDF online dictionary, asked one word at a time, cached to disk.

    POST https://e-dictionary.ilrdf.org.tw/wsReDictionary.htm
         FMT=1  account=E201606002  TribesCode=33  qw=<word>  page=1

This is the same call web.klokah.tw/multiSearch makes; the account code is in
its own index.js, served to every visitor. TribesCode 33 is 太魯閣語, read off
the <option> in that page.

WHAT IT RETURNS, AND WHY IT IS WORTH A NEW SOURCE. `saw` comes back with nine
Chinese glosses, a Note, and **Frequency 1370** — an occurrence count from their
own corpus, not ours. Two of the three things a decision here needs (is the word
Truku, what does it mean, how common is it) in one answer, from a body that is
neither the omnibus nor the parquets nor the Bible.

WHAT IT IS NOT. It answers about HEADWORDS. `tksaw` and `gmquwaq` both come back
無搜尋結果 while their roots are there in full, so this is not the derived-form
inventory the printed Patas pusu kari Truku is (1,267 roots, 29,788 derived) and
it cannot settle a paradigm form on its own. Its use is the other half of the
gate: a root the omnibus lists without Chinese is a root this can gloss.

RULES OF USE, so this stays a lookup and not a scrape:
  - Every answer is cached in edictionary_trv.json, including the misses. A word
    is asked once, ever.
  - Sequential, one connection, DELAY between calls.
  - A miss is a miss. `status 2 無搜尋結果` is recorded as a null and must never
    be retried in a loop hoping for a different answer.

    python tools/orthography/fetch_edictionary.py word1 word2 ...
    python tools/orthography/fetch_edictionary.py --file words.txt
"""
import io
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "edictionary_trv.json")
URL = "https://e-dictionary.ilrdf.org.tw/wsReDictionary.htm"
DELAY = 0.7
TRUKU = "33"


def load():
    if os.path.exists(CACHE):
        return json.load(io.open(CACHE, encoding="utf-8"))
    return {}


def save(d):
    with io.open(CACHE, "w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, ensure_ascii=False, indent=0, sort_keys=True)


def ask(word):
    """{'glosses': [...], 'freq': int|None, 'note': str} or None for a miss."""
    body = urllib.parse.urlencode({
        "FMT": "1", "account": "E201606002", "TribesCode": TRUKU,
        "qw": word, "page": "1"}).encode("utf-8")
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "pecoraro-taroko lexical check"})
    with urllib.request.urlopen(req, timeout=40) as r:
        j = json.loads(r.read().decode("utf-8"))
    g = j.get("GenericData") or {}
    if (g.get("Message") or {}).get("status") != "0" or not g.get("DATA"):
        return None
    d = g["DATA"]
    if isinstance(d, list):                       # never seen, but cheap
        d = d[0] if d else {}
    # Explanation is a list of {"chinese": ...} EXCEPT when it holds one gloss,
    # where the service sends the bare string instead. Seven of the first 611
    # words came back that way — `tuk`, `uli`, `uqu` … — and every one of them
    # was a HIT lost to a parse error, which is the failure this file's own rule
    # about misses is meant to prevent: a miss that is really a crash reads as
    # "the dictionary does not have it" and gets cached as one.
    ex = d.get("Explanation") or []
    if isinstance(ex, (str, dict)):
        ex = [ex]
    return {"name": d.get("Name") or word,
            "glosses": [e if isinstance(e, str) else e.get("chinese")
                        for e in ex
                        if (e if isinstance(e, str) else e.get("chinese"))],
            "freq": int(d["Frequency"]) if str(d.get("Frequency") or "").isdigit()
                    else None,
            "note": d.get("Note") or ""}


def fetch(words, cache=None):
    c = load() if cache is None else cache
    todo = [w for w in dict.fromkeys(words) if w and w not in c]
    for i, w in enumerate(todo):
        try:
            c[w] = ask(w)
        except Exception as e:                     # a network fault is not a miss
            print("  ! %s: %s" % (w, e))
            continue
        if (i + 1) % 25 == 0:
            save(c)
            print("  %d/%d asked" % (i + 1, len(todo)))
        time.sleep(DELAY)
    save(c)
    hit = [w for w in words if c.get(w)]
    print("asked %d new; %d of %d words are in the dictionary"
          % (len(todo), len(hit), len(set(words))))
    return c


def main():
    args = sys.argv[1:]
    if "--file" in args:
        p = args[args.index("--file") + 1]
        words = [x.strip().lower() for x in io.open(p, encoding="utf-8")
                 if x.strip()]
    else:
        words = [a.lower() for a in args if not a.startswith("--")]
    if not words:
        print(__doc__)
        return
    c = fetch(words)
    for w in words[:12]:
        r = c.get(w)
        print("  %-14s %s" % (w, (u"／".join(r["glosses"])[:60] +
                                  ("  [freq %s]" % r["freq"] if r["freq"] else ""))
                              if r else u"—"))


if __name__ == "__main__":
    main()
