# Build Pothi print-ready wraparound cover (300 DPI, 0.2" bleed, soft cover)
# usage: make_cover.py front.jpg back.jpg pages out.pdf
import sys
from PIL import Image, ImageOps, ImageDraw
import numpy as np
front, back, pages, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
DPI = 300; BLEED = int(0.2 * DPI)
TW, TH = 1749, 2480                              # A5 trim at 300 dpi
spine = round(pages * 0.001968 * DPI)            # Pothi soft-cover spine formula
f = Image.open(front).convert('RGB').resize((TW, TH), Image.LANCZOS)
b = Image.open(back).convert('RGB').resize((TW, TH), Image.LANCZOS)
# remove placeholder ISBN barcode + price: leave clean white box for the real barcode
ImageDraw.Draw(b).rectangle((1335, 1940, 1705, 2268), fill='white')
def pad(img, left, right):                       # stretch edge pixels into the bleed (no mirrored text)
    a = np.asarray(img)
    a = np.pad(a, ((BLEED, BLEED), (left, right), (0, 0)), mode='edge')
    return Image.fromarray(a)
b = pad(b, BLEED, 0); f = pad(f, 0, BLEED)
W = b.width + spine + f.width; H = TH + 2 * BLEED
c = Image.new('RGB', (W, H), (92, 26, 22))       # maroon spine (matches title colour)
c.paste(b, (0, 0)); c.paste(f, (b.width + spine, 0))
c.save(out, 'PDF', resolution=DPI)
c.save(out.replace('.pdf', '.jpg'), quality=95, dpi=(DPI, DPI))
print(f'spine {spine}px = {spine/DPI:.3f}in; cover {W}x{H}px = {W/DPI:.3f}x{H/DPI:.3f}in')
