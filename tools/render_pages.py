"""Render pecoraro_full.pdf to 200dpi PNGs in scans/full/."""
import pathlib
import fitz

ROOT = pathlib.Path(__file__).resolve().parents[1]
PDF = ROOT / "scans" / "pecoraro_full.pdf"
OUT = ROOT / "scans" / "full"
OUT.mkdir(parents=True, exist_ok=True)

doc = fitz.open(PDF)
for i, page in enumerate(doc, 1):
    out = OUT / f"page_{i:03d}.png"
    if out.exists():
        continue
    page.get_pixmap(dpi=200).save(out)
    if i % 20 == 0 or i == doc.page_count:
        print(f"{i}/{doc.page_count}", flush=True)
print("done", flush=True)
