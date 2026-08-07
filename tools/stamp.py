# -*- coding: utf-8 -*-
"""Stamp the site with a build id, and hang that id off every asset URL.

Why this exists: `index.html` loaded `app.js`, `entries.js`, `style.css` and the
rest at bare names. Netlify serves them `max-age=0, must-revalidate`, which is
correct and is still not enough -- a phone, a webview or a back/forward
navigation will hand back the copy it already has, so a deploy can be live on
the CDN and invisible in the browser looking at it. There was also nothing on
the page that said which build you were reading, so the only way to find out was
to notice a change you were expecting.

A query string fixes both halves: the URL itself changes, so it is a different
resource and has to be fetched, and the same string is written into `app.js` as
BUILD and printed at the foot of the about sheet.

    python tools/stamp.py           # stamp with the current UTC minute
    python tools/stamp.py --check   # exit 1 if the stamp is missing or split

Run it before deploying. It is idempotent in shape -- re-running only moves the
id -- and it asserts that every asset carries the SAME id, because a half-
stamped page is worse than an unstamped one: it looks updated and is not.
"""
import argparse
import datetime
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "site", "index.html")
APP = os.path.join(ROOT, "site", "app.js")

# Local assets only. A `?v=` on an off-site URL would be someone else's cache to
# reason about, and the favicons are left alone deliberately: browsers re-fetch
# them on their own schedule and a changing icon URL makes tabs flicker.
ASSET = re.compile(
    r'((?:src|href)=")(?!https?:|//|data:)([A-Za-z0-9_./-]+\.(?:js|css))'
    r'(?:\?v=[0-9A-Za-z.-]+)?(")')
BUILD_LINE = re.compile(r'(var BUILD = ")([^"]*)(";)')
SKIP = ("favicon",)


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)


def stamped(html):
    """Every build id found on an asset URL in the html, in order."""
    out = []
    for m in ASSET.finditer(html):
        if any(s in m.group(2) for s in SKIP):
            continue
        q = re.search(r'\?v=([0-9A-Za-z.-]+)', m.group(0))
        out.append((m.group(2), q.group(1) if q else None))
    return out


def apply(html, bid):
    def sub(m):
        if any(s in m.group(2) for s in SKIP):
            return m.group(0)
        return "%s%s?v=%s%s" % (m.group(1), m.group(2), bid, m.group(3))
    return ASSET.sub(sub, html)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--id", default=None, help="use this build id verbatim")
    a = ap.parse_args()

    html, app = read(HTML), read(APP)
    if not BUILD_LINE.search(app):
        sys.exit("app.js has no `var BUILD = \"...\";` line to write into")

    if a.check:
        found = stamped(html)
        ids = set(v for _, v in found)
        bad = [f for f, v in found if v is None]
        cur = BUILD_LINE.search(app).group(2)
        ok = not bad and len(ids) == 1 and ids == {cur}
        print("assets %d | ids %s | app.js BUILD %s%s"
              % (len(found), sorted(x for x in ids if x) or "none", cur or "none",
                 "" if ok else "  <-- MISMATCH: " + (
                     "unstamped %s" % bad if bad else "html and app.js differ")))
        sys.exit(0 if ok else 1)

    bid = a.id or datetime.datetime.now(
        datetime.timezone.utc).strftime("%Y%m%d-%H%M")
    out = apply(html, bid)
    n = len([1 for _, v in stamped(out) if v == bid])
    if not n:
        sys.exit("matched no assets -- has index.html changed shape?")
    write(HTML, out)
    write(APP, BUILD_LINE.sub(lambda m: m.group(1) + bid + m.group(3), app))
    print("build %s stamped on %d assets and in app.js" % (bid, n))


if __name__ == "__main__":
    main()
