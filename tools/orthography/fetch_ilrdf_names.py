# -*- coding: utf-8 -*-
"""Harvest ilrdf_names.json from the ILRDF 原住民族人名資料庫.

    https://indigenous-name.ilrdf.org.tw/#/searchView?zuqunId=13&zuName=太魯閣族

The Council of Indigenous Peoples' name registry, digitized: 1,802 Truku names
and 546 Seediq ones, each with its 男名 / 女名 / 男女共名 type and an mp3 of a
speaker saying it. It is a Vue SPA over a JSON API; the page itself holds no
data, so this posts to the API the page posts to.

    POST /api/api/EthnicLanguageData/GetFirsrWordList
         {FirstWord, EthnicGroupId, page, pageSize, NameTypes}

EthnicGroupId 13 = 太魯閣族, 10 = 賽德克族; the ids and the per-language alphabets
are hard-coded in the bundle's `keyboardFirstName`, which is where LETTERS comes
from — Truku's is p b t d k g q c j s x h m n ng r l w y + i e a u o. There is no
"all names" call, so the harvest walks the initial-letter index and pages through
each; `o`, `x` and `ʼ` return nothing for Truku, which is the alphabet's own
answer and not a gap.

`NameTypes: []` means every type, and for Truku every type is three: 男名 928,
女名 614, 男女共名 258, distinct 1,792. Asking for 氏族名 (3) and 屋名 (4)
explicitly returns **zero rows on every initial** — the register simply does not
hold Truku clan or house names, so an empty result here is completeness, not a
filter left switched on, and his clan names will never be settled from this
source.

Why this file exists at all: **no wordlist has a reason to hold a personal
name**, which is why tier N has always been the one population where every
spelling was a guess and every word stayed pale. This is the outside source that
settles them. `build_verified.py` widens `seen` with it at level 1 (LISTED), the
same level as the parquets, and must never widen `lex` — a name is not a root.

Re-run only to refresh; the output is committed, and the build must not depend
on the network.
"""
import io, json, os, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
API = ("https://indigenous-name.ilrdf.org.tw/api/api/"
       "EthnicLanguageData/GetFirsrWordList")
GROUPS = [(13, "太魯閣族"), (10, "賽德克族")]
LETTERS = list("abcdeghijklmnopqrstuwxy") + ["ng", "ʼ"]
PAGE = 200


def post(payload):
    req = urllib.request.Request(
        API, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Origin": "https://indigenous-name.ilrdf.org.tw",
                 "Referer": "https://indigenous-name.ilrdf.org.tw/",
                 "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as fh:
        return json.loads(fh.read().decode("utf-8"))


def harvest(gid):
    seen = {}
    for w in LETTERS:
        page = 1
        while True:
            r = post({"FirstWord": w, "EthnicGroupId": gid, "page": page,
                      "pageSize": PAGE, "NameTypes": []})
            if r.get("code") != 200:
                raise SystemExit("%s p%d: %s" % (w, page, r.get("message")))
            d = r.get("data") or {}
            rows = (d.get("FuzzyList") or {}).get("list") or []
            for rec in rows:
                seen[rec["Id"]] = rec
            total = d.get("FuzzyCount") or 0
            if page * PAGE >= total or not rows:
                break
            page += 1
            time.sleep(0.3)
        time.sleep(0.3)
    return seen


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    out = {}
    for gid, label in GROUPS:
        recs = harvest(gid)
        # name -> sorted list of its types. A name can be registered twice with
        # different types (男名 and 男女共名), and both are the registry's answer.
        names = {}
        for r in recs.values():
            names.setdefault(r["Name"].strip(), set()).add(r["NameTypeStr"])
        out[label] = {k: sorted(v) for k, v in sorted(names.items(),
                                                     key=lambda kv: kv[0].lower())}
        print("%s (id %d): %d records, %d distinct names"
              % (label, gid, len(recs), len(names)))
    p = os.path.join(HERE, "ilrdf_names.json")
    io.open(p, "w", encoding="utf-8", newline="\n").write(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    print("wrote %s" % p)


if __name__ == "__main__":
    main()
