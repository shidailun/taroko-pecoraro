"""Render the app icons by cropping the palm off Pecoraro's own cover.

The icon IS the cover's palm -- site/cover.png, cropped, not redrawn. An earlier
version of this script drew a stylised palm to survive 32px; it was a redesign,
and his cover is the record here exactly as his spelling is on the page. So the
art is a straight crop and the only choices left are where the frame sits and
how it is scaled down.

    CROP is square, sits below the "CAHIER D'ARCHIPEL 7" line and stops above the
    stilt house's roof, so the palm is alone in it and the trunk bleeds off the
    bottom edge the way it does on the cover.

Corners are rounded into the PNG at r = 19% of size, the fleet convention; the
maskable icon stays square because the OS shapes that one itself, and its art is
inset so a circular launcher mask cannot eat a frond tip.

    python tools/make_icon.py            # writes the five site/ icons
    python tools/make_icon.py --preview  # also writes .scratch/icon-preview.png
"""
import os
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
COVER = os.path.join(SITE, "cover.png")

CROP = (0, 170, 640, 810)   # left, top, right, bottom on the 941x1672 cover
COVER_SIZE = (941, 1672)    # asserted: a re-rendered cover would move the crop
PAPER = (247, 236, 211)     # the cover's own paper, sampled at its corner

RADIUS = 0.19    # corner radius, fraction of size
SS = 4           # supersample factor for the corner mask
MASK_INSET = 0.80  # maskable art scale, so the crown stays inside the safe zone


def art(size):
    """The cover's palm, square, at `size` px.

    Below ~64px a plain LANCZOS reduction greys the pinnae into a smudge -- the
    frame is unchanged, the fronds just stop having enough pixels to be dark. A
    little unsharp and contrast puts the blades back without altering the art;
    it is the same palm, printed small.
    """
    im = Image.open(COVER).convert("RGB")
    assert im.size == COVER_SIZE, "cover.png is %s, not %s -- re-check CROP" % (
        im.size, COVER_SIZE)
    assert CROP[2] - CROP[0] == CROP[3] - CROP[1], "CROP is not square"
    out = im.crop(CROP).resize((size, size), Image.LANCZOS)
    if size <= 64:
        out = ImageEnhance.Contrast(out).enhance(1.15)
        out = out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=160, threshold=0))
    return out


def render(size, rounded=True, inset=1.0):
    tile = Image.new("RGB", (size, size), PAPER)
    if inset >= 1.0:
        tile = art(size)
    else:
        inner = max(1, int(round(size * inset)))
        off = (size - inner) // 2
        tile.paste(art(inner), (off, off))

    out = tile.convert("RGBA")
    if rounded:
        m = Image.new("L", (size * SS, size * SS), 0)
        ImageDraw.Draw(m).rounded_rectangle(
            [0, 0, size * SS - 1, size * SS - 1],
            radius=RADIUS * size * SS, fill=255)
        out.putalpha(m.resize((size, size), Image.LANCZOS))
    return out


def main():
    out = [("favicon.png", 180, True, 1.0),
           ("favicon-32.png", 32, True, 1.0),
           ("icon-192.png", 192, True, 1.0),
           ("icon-512.png", 512, True, 1.0),
           ("icon-512-maskable.png", 512, False, MASK_INSET)]
    for name, size, rounded, inset in out:
        render(size, rounded, inset).save(os.path.join(SITE, name))
        print("wrote site/%-22s %4dx%-4d %s" % (
            name, size, size,
            "rounded" if rounded else "square (maskable, art at %d%%)" % (inset * 100)))

    if "--preview" in sys.argv:
        d = os.path.join(ROOT, ".scratch")
        os.makedirs(d, exist_ok=True)
        sheet = Image.new("RGBA", (180 + 64 + 32 + 60, 180), (140, 140, 140, 255))
        for im, x, y in ((render(180), 0, 0), (render(64), 196, 58),
                         (render(32), 276, 74)):
            sheet.paste(im, (x, y), im)
        sheet.save(os.path.join(d, "icon-preview.png"))
        print("wrote .scratch/icon-preview.png")


if __name__ == "__main__":
    main()
