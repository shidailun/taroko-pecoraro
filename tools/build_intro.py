import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
SITE = os.path.join(ROOT, "site")
SCANS = os.path.join(ROOT, "scans", "full")
IMG_DIR = os.path.join(SITE, "intro-images")

sections = []
for name in ["intro_part1.json", "intro_part2.json"]:
    path = os.path.join(DATA, name)
    with open(path, encoding="utf-8") as f:
        sections.extend(json.load(f))

sections.sort(key=lambda s: s["page"])

os.makedirs(IMG_DIR, exist_ok=True)
copied = []
for s in sections:
    img = s.get("image")
    if img:
        shutil.copyfile(os.path.join(SCANS, img), os.path.join(IMG_DIR, img))
        copied.append(img)

out_path = os.path.join(SITE, "intro.js")
with open(out_path, "w", encoding="utf-8") as f:
    f.write("window.INTRO = ")
    json.dump(sections, f, ensure_ascii=False, indent=2)
    f.write(";\n")

print(f"{len(sections)} intro sections -> {out_path}")
print(f"images copied: {copied}")
