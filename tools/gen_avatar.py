#!/usr/bin/env python3
"""Render the 500x500 matrix-style "NS" avatar. Run: python3 tools/gen_avatar.py"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).resolve().parent.parent / "assets" / "avatar.png"
S = 1000  # draw at 2x, downscale for clean edges
random.seed(7)

GREEN = (0, 255, 65)
mono = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 330, index=1)  # Menlo Bold
small = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 26)
kana = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", 30)
GLYPHS = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワン0123456789"

# background: deep green radial falloff
bg = Image.new("RGB", (S, S), (0, 0, 0))
px = bg.load()
for y in range(S):
    for x in range(S):
        d = math.hypot(x - S / 2, y - S / 2) / (S / 1.4)
        v = max(0.0, 1 - d)
        px[x, y] = (0, int(22 * v * v), int(8 * v * v))

# matrix rain: columns fading from bright head to dark tail
rain = Image.new("RGBA", (S, S), (0, 0, 0, 0))
dr = ImageDraw.Draw(rain)
for x in range(10, S, 34):
    head = random.randint(-200, S + 200)
    length = random.randint(8, 22)
    for k in range(length):
        y = head - k * 34
        if not -40 < y < S:
            continue
        a = int(255 * (1 - k / length) ** 1.6)
        col = (210, 255, 220, a) if k == 0 else (0, 255, 65, int(a * 0.8))
        dr.text((x, y), random.choice(GLYPHS), font=kana, fill=col)
rain = rain.filter(ImageFilter.GaussianBlur(0.6))
img = Image.alpha_composite(bg.convert("RGBA"), Image.eval(rain, lambda v: v))
# dim the rain so the monogram reads
dim = Image.new("RGBA", (S, S), (0, 0, 0, 120))
img = Image.alpha_composite(img, dim)

# HUD ring with ticks and arc segments
hud = Image.new("RGBA", (S, S), (0, 0, 0, 0))
dh = ImageDraw.Draw(hud)
c, R = S / 2, 400
for i in range(120):
    ang = math.radians(i * 3)
    r1 = R - (22 if i % 10 == 0 else 10)
    dh.line([(c + r1 * math.cos(ang), c + r1 * math.sin(ang)), (c + R * math.cos(ang), c + R * math.sin(ang))],
            fill=GREEN + (200 if i % 10 == 0 else 90,), width=3 if i % 10 == 0 else 2)
for start, end in ((200, 250), (290, 340), (20, 70), (110, 160)):
    dh.arc([c - R - 26, c - R - 26, c + R + 26, c + R + 26], start, end, fill=GREEN + (230,), width=6)
dh.ellipse([c - 330, c - 330, c + 330, c + 330], outline=GREEN + (70,), width=2)
dh.text((c, c - 262), "NETSPHERE//SYS", font=small, fill=GREEN + (190,), anchor="mm")
dh.text((c, c + 262), "> online", font=small, fill=GREEN + (190,), anchor="mm")

# monogram with glow
mono_layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
dm = ImageDraw.Draw(mono_layer)
dm.text((c, c + 8), "NS", font=mono, fill=(234, 255, 240, 255), anchor="mm")
glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
dg = ImageDraw.Draw(glow)
dg.text((c, c + 8), "NS", font=mono, fill=GREEN + (255,), anchor="mm")
glow = glow.filter(ImageFilter.GaussianBlur(22))
# chromatic offset for a subtle glitch
red = Image.new("RGBA", (S, S), (0, 0, 0, 0))
ImageDraw.Draw(red).text((c - 7, c + 10), "NS", font=mono, fill=(255, 46, 136, 110), anchor="mm")
cyan = Image.new("RGBA", (S, S), (0, 0, 0, 0))
ImageDraw.Draw(cyan).text((c + 7, c + 6), "NS", font=mono, fill=(0, 229, 255, 110), anchor="mm")

for layer in (Image.eval(hud.filter(ImageFilter.GaussianBlur(5)), lambda v: v), hud, glow, glow, red, cyan, mono_layer):
    img = Image.alpha_composite(img, layer)

# scanlines
scan = Image.new("RGBA", (S, S), (0, 0, 0, 0))
ds = ImageDraw.Draw(scan)
for y in range(0, S, 6):
    ds.line([(0, y), (S, y)], fill=(0, 0, 0, 70), width=2)
img = Image.alpha_composite(img, scan)

img.convert("RGB").resize((500, 500), Image.LANCZOS).save(OUT, optimize=True)
print(OUT, OUT.stat().st_size // 1024, "KB")
