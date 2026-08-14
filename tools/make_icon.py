"""Render site/favicon.png and site/favicon-32.png.

The subject is the palm crown from Pecoraro's own cover (site/cover.png), not a
generic book: the SECMI cover puts a palm over a stilt house, and the palm is the
half that survives being shrunk to 32px. Drawn, not cropped -- the cover's
pinnate fronds turn to mush below ~64px, so the fronds here are solid blades with
scalloped edges that read as pinnae when large and as a blade when small.

Palette is the app's own (style.css): --truku #14544a ground, --paper cream art.
Corners are rounded into the PNG at r = 19% of size, the fleet convention.

    python tools/make_icon.py            # writes site/favicon.png, favicon-32.png
    python tools/make_icon.py --preview  # also writes .scratch/icon-preview.png
"""
import math
import os
import sys

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")

GROUND = (20, 84, 74, 255)      # --truku  #14544a
ART = (247, 242, 232, 255)      # --paper  #f7f2e8
TRUNK = (201, 184, 146, 255)    # cover-ish tan, so the crown reads first

SS = 8            # supersample factor
N = 1024          # nominal art size
RADIUS = 0.19     # corner radius, fraction of size

CX, CY = 0.500, 0.395   # crown node, fraction of the tile
# (degrees from +x axis, length, droop) -- droop bends the tip downward
FRONDS = [
    (90, 0.270, 0.020),
    (50, 0.310, 0.100),
    (130, 0.310, 0.100),
    (16, 0.340, 0.200),
    (164, 0.340, 0.200),
    (-20, 0.295, 0.235),
    (200, 0.295, 0.235),
]
FROND_W = 0.052   # half-width of a frond at its widest
PINNAE = 9        # scallops per edge


def bez(p0, p1, p2, t):
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])


def frond(deg, length, droop):
    """Outline polygon of one frond, in tile fractions."""
    a = math.radians(deg)
    dx, dy = math.cos(a), -math.sin(a)
    p0 = (CX, CY)
    p1 = (CX + dx * length * 0.55, CY + dy * length * 0.55 - length * 0.10)
    p2 = (CX + dx * length, CY + dy * length + droop)

    pts = [bez(p0, p1, p2, i / 120) for i in range(121)]
    up, dn = [], []
    for i, (x, y) in enumerate(pts):
        t = i / 120
        nx, ny = pts[min(i + 1, 120)]
        px, py = pts[max(i - 1, 0)]
        tx, ty = nx - px, ny - py
        m = math.hypot(tx, ty) or 1
        tx, ty = tx / m, ty / m
        # taper: nothing at the node, widest at 45%, a point at the tip
        taper = math.sin(math.pi * t) ** 0.55 * (1 - t * 0.35)
        scallop = 0.62 + 0.38 * abs(math.sin(math.pi * PINNAE * t))
        w = FROND_W * taper * scallop
        up.append((x - ty * w, y + tx * w))
        dn.append((x + ty * w, y - tx * w))
    return up + dn[::-1]


def trunk():
    """Tapered trunk from the crown node off the bottom edge."""
    p0, p1, p2 = (CX, CY), (CX - 0.012, CY + 0.32), (CX + 0.030, 1.06)
    up, dn = [], []
    for i in range(61):
        t = i / 60
        x, y = bez(p0, p1, p2, t)
        w = 0.017 + 0.016 * t          # narrow at the crown, thicker at the base
        up.append((x - w, y))
        dn.append((x + w, y))
    return up + dn[::-1]


def render(size, rounded=True):
    px = size * SS
    img = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if rounded:
        d.rounded_rectangle([0, 0, px - 1, px - 1], radius=RADIUS * px, fill=GROUND)
    else:
        d.rectangle([0, 0, px - 1, px - 1], fill=GROUND)   # maskable: the OS shapes it

    def scale(poly):
        return [(x * px, y * px) for x, y in poly]

    d.polygon(scale(trunk()), fill=TRUNK)
    for deg, length, droop in FRONDS:
        d.polygon(scale(frond(deg, length, droop)), fill=ART)
    # crown node, so seven blades meet in something rather than in a seam
    r = 0.030 * px
    d.ellipse([CX * px - r, CY * px - r, CX * px + r, CY * px + r], fill=ART)

    return img.resize((size, size), Image.LANCZOS)


def safe_zone():
    """Maskable icons are cropped to a circle of r = 40% by some launchers.

    The crown has to sit inside it or a launcher eats a frond. The trunk is
    allowed out -- it bleeds off the bottom edge by design.
    """
    worst = 0.0
    for deg, length, droop in FRONDS:
        for x, y in frond(deg, length, droop):
            worst = max(worst, math.hypot(x - 0.5, y - 0.5))
    return worst


def main():
    assert safe_zone() <= 0.40, "crown leaves the maskable safe zone: %.3f" % safe_zone()

    out = [("favicon.png", 180, True), ("favicon-32.png", 32, True),
           ("icon-192.png", 192, True), ("icon-512.png", 512, True),
           ("icon-512-maskable.png", 512, False)]
    for name, size, rounded in out:
        render(size, rounded).save(os.path.join(SITE, name))
        print("wrote site/%-22s %4dx%-4d %s" % (
            name, size, size, "rounded" if rounded else "square (maskable)"))
    print("crown reaches %.3f of the maskable safe zone's 0.400" % safe_zone())

    if "--preview" in sys.argv:
        d = os.path.join(ROOT, ".scratch")
        os.makedirs(d, exist_ok=True)
        sheet = Image.new("RGBA", (180 + 64 + 32 + 40, 180), (140, 140, 140, 255))
        sheet.paste(render(180), (0, 0), render(180))
        sheet.paste(render(64), (196, 58), render(64))
        sheet.paste(render(32), (276, 74), render(32))
        sheet.save(os.path.join(d, "icon-preview.png"))
        print("wrote .scratch/icon-preview.png")


if __name__ == "__main__":
    main()
