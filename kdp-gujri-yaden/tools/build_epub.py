# Build Kindle EPUB from extracted lines.json
import json, sys, html, re, subprocess, os
L = json.load(open(sys.argv[1])); out_dir = sys.argv[2]
H = lambda t: html.escape(t)
lines = [l for l in L if l['page'] >= 5 and l['size'] > 10.5 and not re.fullmatch(r'\d+', l['text'].strip())]
# page geometry
geo = {}
for l in L:
    if l['size'] == 12.0:
        g = geo.setdefault(l['page'], [999, 0]); g[0] = min(g[0], l['x0']); g[1] = max(g[1], l['x1'])
md = []; para = None; prev = None; mode = 'body'
def flush():
    global para
    if para: md.append('<p>' + H(para) + '</p>')
    para = None
for l in lines:
    t = l['text'].strip(); left, right = geo.get(l['page'], (43, 349))
    if l['size'] >= 18:
        flush(); md.append(f'\n# {t}\n'); mode = 'dedic' if t == 'समर्पण' else 'body'; prev = None; continue
    if t == '❖': continue
    if t.replace(' ', '') == '❖❖❖':
        if prev and prev.get('sep'): continue
        flush(); md.append('<p class="sep">❖ ❖ ❖</p>'); prev = {'sep': 1}; continue
    if mode == 'dedic' and l['size'] == 14.3:
        flush(); md.append(f'<p class="center">{H(t)}</p>'); prev = l; continue
    if l['x0'] > left + 120:   # right-aligned (signatures, letter headers)
        flush(); md.append(f'<p class="right">{H(t)}</p>'); prev = l; continue
    newp = (para is None or l['x0'] > left + 8 or
            (prev and 'x1' in prev and prev['x1'] < geo.get(prev['page'], (0, 349))[1] - 15))
    if newp:
        flush(); para = t
    else:
        para += ' ' + t
    prev = l
flush()
body = '\n'.join(md)
# author bio: put photo after heading
body = body.replace('# लेखक परिचय\n', '# लेखक परिचय\n\n<p class="center"><img src="author.jpg" alt="अब्दुल अजीज" /></p>\n')
front = '''<div class="copyright">
<p><strong>गुजरी यादें</strong> (उपन्यास)<br/>लेखक : अब्दुल अजीज (प्र. शि.)<br/>© अब्दुल अजीज<br/>प्रथम संस्करण : 2026</p>
<p>सर्वाधिकार सुरक्षित। लेखक की लिखित अनुमति के बिना इस पुस्तक के किसी भी अंश का पुनर्प्रकाशन, प्रतिलिपि या किसी भी रूप में उपयोग वर्जित है।</p>
</div>
'''
body = body.replace('<p>अब्दुल अजीज</p>\n<p class="right">(प्र. शि.)</p>', '<p class="center"><strong>अब्दुल अजीज</strong><br/>(प्र. शि.)</p>')
open(os.path.join(out_dir, 'book.md'), 'w').write(front + '\n' + body + '\n')
