# Pothi interior: drop cover pages, clean copyright page, pad to even page count
import sys, pymupdf
src, out = sys.argv[1], sys.argv[2]
d = pymupdf.open(src)
d.select(list(range(2, 85)))                      # PDF pages 3..85 (title page .. author bio)
cp = d[1]                                          # copyright page
# remove placeholder lines: ISBN, price, publisher, printer
for blk in cp.get_text('dict')['blocks']:
    for ln in blk.get('lines', []):
        t = ''.join(sp['text'] for sp in ln['spans'])
        if any(k in t for k in ('ISBN', '299', 'प्रकाशक', 'मुद्रक')):
            cp.add_redact_annot(pymupdf.Rect(ln['bbox']) + (-1, -1, 1, 1), fill=(1, 1, 1))
# underscores / blank lines for publisher & printer
for dr in cp.get_drawings():
    r = dr['rect']
    if r.height < 3 and r.width > 50: cp.add_redact_annot(r + (-1, -2, 1, 2), fill=(1, 1, 1))
cp.apply_redactions(graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED)
if len(d) % 2: d.new_page(width=d[0].rect.width, height=d[0].rect.height)
d.save(out, garbage=4, deflate=True)
print('pages', len(d))
