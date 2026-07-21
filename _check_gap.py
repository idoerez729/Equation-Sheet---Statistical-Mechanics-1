import fitz
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
doc = fitz.open("Statmech.pdf")
print("pages", doc.page_count)
out = Path("_layout_check")
out.mkdir(exist_ok=True)
for i, page in enumerate(doc):
    w = page.rect.width
    h = page.rect.height
    for col, xmin, xmax in [("L", 0, w * 0.45), ("R", w * 0.45, w)]:
        ys = [17.0]
        n = 0
        for b in page.get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            x0, y0, x1, y1 = b["bbox"]
            if xmin <= x0 < xmax:
                ys.extend([y0, y1])
                n += 1
        ys.append(h - 17)
        ys = sorted(ys)
        gaps = sorted([b - a for a, b in zip(ys, ys[1:]) if b - a > 40], reverse=True)[
            :3
        ]
        print(f"p{i+1} {col} blocks={n:3d} gaps={[round(g) for g in gaps]}")
    pix = page.get_pixmap(matrix=fitz.Matrix(1.2, 1.2), alpha=False)
    pix.save(out / f"page{i+1}.png")
