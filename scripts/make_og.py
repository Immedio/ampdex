"""Generate the OG / social-share image for ampdex (1200x630 PNG).
Light paper, ink type, hairline rule. Mirrors the site's typographic system.

Run from repo root:  python3 scripts/make_og.py
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "public" / "og.png"

W, H = 1200, 630
PAPER = (245, 242, 236)  # #f5f2ec
INK = (10, 10, 10)  # #0a0a0a
MUTED = (107, 107, 102)  # #6b6b66

PAD_X = 64
PAD_Y = 56


def find_font(candidates: list[str], size: int) -> ImageFont.FreeTypeFont:
    # Try Geist if installed, else system Helvetica/Arial-Black, else fc-match
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    try:
        out = subprocess.run(
            ["fc-match", "-f", "%{file}", candidates[0] if candidates else "sans"],
            check=True, capture_output=True, text=True,
        )
        if out.stdout and Path(out.stdout).exists():
            return ImageFont.truetype(out.stdout, size)
    except Exception:
        pass
    # Last resort: PIL default (bitmap, not scalable) — caller should pick differently
    return ImageFont.load_default()


# macOS system fonts (this dev env). Geist isn't system-installed; use Helvetica.
HEAVY = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial Black.ttf",
    "/System/Library/Fonts/Supplemental/Arial Black.ttf",
]
MONO = [
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Monaco.ttf",
]

font_display = find_font(HEAVY, 124)
font_sub = find_font(HEAVY, 28)
font_mono = find_font(MONO, 22)


def main() -> int:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Top kicker
    d.text(
        (PAD_X, PAD_Y),
        "AMPDEX  /  AXE-FX III · FM9 · FM3",
        font=font_mono,
        fill=MUTED,
    )

    # Hairline under kicker
    d.line(
        [(PAD_X, PAD_Y + 44), (W - PAD_X, PAD_Y + 44)],
        fill=INK,
        width=1,
    )

    # Display headline — wrapped manually at "amplifier"
    line1 = "331 amplifier"
    line2 = "models. One field."
    y = PAD_Y + 90
    d.text((PAD_X, y), line1, font=font_display, fill=INK)
    d.text((PAD_X, y + 130), line2, font=font_display, fill=INK)

    # Subtitle near the bottom
    sub_y = H - PAD_Y - 90
    d.line(
        [(PAD_X, sub_y - 28), (W - PAD_X, sub_y - 28)],
        fill=INK,
        width=1,
    )
    d.text(
        (PAD_X, sub_y),
        "Searchable Fractal Audio amp library",
        font=font_sub,
        fill=INK,
    )
    d.text(
        (PAD_X, sub_y + 36),
        "rinkashimikito.github.io/ampdex",
        font=font_mono,
        fill=MUTED,
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    size_kb = os.path.getsize(OUT) / 1024
    print(f"wrote {OUT.relative_to(REPO)}  ({size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
