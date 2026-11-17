# Extract logical-order Unicode Hindi from the XeTeX book PDF (glyphs are in visual order).
import sys, re, json, pdfplumber
C = '[\u0915-\u0939\u0958-\u095F]'
CL = f'(?:{C}़?्)*{C}़?'          # consonant cluster
M = '[ािीुूृॅेैॉोौंःँ]'
def fix(s):
    s = re.sub(r'\(cid:\d+\)', '', s)
    s = s.replace('ि्ं', 'िं').replace('इर्', 'ई')
    # i-matra (with optional anusvara) appears before its cluster
    s = re.sub(f'ि([ंँ]?)(र्)?({CL})', lambda m: ('\ue001' if m.group(2) else '') + m.group(3) + 'ि' + m.group(1), s)
    # reph glyph comes after the syllable it belongs to: move it in front
    s = re.sub(f'({CL})({M}*)र्({M}*)', lambda m: 'र्'+m.group(1)+m.group(2)+m.group(3), s)
    s = s.replace('\ue001', 'र्')
    s = re.sub(f'ि्ं({C})', r'\1िं', s)
    for a, b in [('ाे','ो'),('ाै','ौ'),('अा','आ'),('एे','ऐ'),('आे','ओ'),('आै','औ'),('अो','ओ'),('अौ','औ')]:
        s = s.replace(a, b)
    s = re.sub('([ंँ])([ािीुूृेैोौ]+)', r'\2\1', s)
    s = s.replace('ाे', 'ो').replace('ाै', 'ौ')
    s = re.sub(' ([,।?!)])', r'\1', s)
    return s

pdf = pdfplumber.open(sys.argv[1])
first, last = int(sys.argv[2]), int(sys.argv[3])
lines = []
for pno in range(first-1, last):
    page = pdf.pages[pno]
    chars = page.chars  # keep content-stream (glyph) order
    rows = []
    for c in chars:
        if rows and abs(rows[-1][0]['top'] - c['top']) < 7: rows[-1].append(c)
        else: rows.append([c])
    for r in rows:
        txt = ''; right = None
        for c in r:
            if right is not None and c['x0'] - right > 1.2 and c['x1'] > c['x0']: txt += ' '
            txt += c['text']
            right = max(right or 0, c['x1'])
        size = max(c['size'] for c in r)
        bold = any('Bold' in c['fontname'] or 'SemiBold' in c['fontname'] for c in r)
        lines.append(dict(page=pno+1, top=r[0]['top'], bottom=r[0]['bottom'], x0=r[0]['x0'], x1=right,
                          size=round(size,1), bold=bold, text=fix(txt)))
json.dump(lines, open(sys.argv[4], 'w'), ensure_ascii=False, indent=0)
