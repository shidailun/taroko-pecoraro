# -*- coding: utf-8 -*-
"""Crop a scan page region at N x, so a disputed glyph can be read beside a
known one FROM THE SAME LINE (standing rule).

  python crop.py 246 0.10 0.55 0.60 0.06 6      page  x  y  w  h  zoom   (fractions)
"""
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.dirname(os.path.abspath(__file__))

pg = sys.argv[1]
x, y, w, h = (float(v) for v in sys.argv[2:6])
z = float(sys.argv[6]) if len(sys.argv) > 6 else 6.0

p = os.path.join(ROOT, "scans", "full", "page_%s.png" % pg.zfill(3))
im = Image.open(p)
W, H = im.size
box = (int(x * W), int(y * H), int((x + w) * W), int((y + h) * H))
c = im.crop(box)
c = c.resize((int(c.width * z), int(c.height * z)), Image.LANCZOS)
f = os.path.join(OUT, "crop_%s.png" % pg)
c.save(f)
print("page %s %sx%s -> %s  (%s)" % (pg, W, H, f, c.size))
