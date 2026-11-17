# Extract paragraphs from Kruti Dev docx, convert to Unicode. Output: one paragraph per line, prefixed with alignment.
import sys, zipfile, re
from lxml import etree
sys.path.insert(0, __file__.rsplit('/',1)[0])
from kruti2uni import convert
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
MC='{http://schemas.openxmlformats.org/markup-compatibility/2006}'
z=zipfile.ZipFile(sys.argv[1])
root=etree.fromstring(z.read('word/document.xml'))
# drop Fallback branches (duplicates of textboxes)
for fb in root.iter(MC+'Fallback'):
    pass
for fb in list(root.iter(MC+'Fallback')):
    fb.getparent().remove(fb)
styles=etree.fromstring(z.read('word/styles.xml'))
deffont='Kruti Dev 010'
out=[]
for p in root.iter(W+'p'):
    # skip paragraphs that contain nested paragraphs' text (textbox container) - handle only direct runs
    jc=p.find(W+'pPr/'+W+'jc')
    align=jc.get(W+'val') if jc is not None else ''
    segs=[]
    for r in p.iter(W+'r'):
        # only runs whose nearest ancestor paragraph is p
        a=r.getparent()
        while a.tag!=W+'p': a=a.getparent()
        if a is not p: continue
        f=r.find(W+'rPr/'+W+'rFonts')
        font=(f.get(W+'ascii') or f.get(W+'hAnsi')) if f is not None else None
        font=font or deffont
        for t in r:
            if t.tag==W+'t': txt=t.text or ''
            elif t.tag==W+'tab': txt='\t'
            elif t.tag in (W+'br',W+'cr'): txt='\n'
            else: continue
            segs.append(('K' if 'Kruti' in font else 'O', txt))
    # merge Kruti segs, protect others with PUA placeholders
    prot=[]; s=''
    for k,txt in segs:
        if k=='K': s+=txt
        else:
            for ch in txt:
                if ch in '\t\n ': s+=ch; continue
                prot.append(ch); s+=chr(0xE000+len(prot)-1)
    u=convert(s)
    u=re.sub('[-]', lambda m: prot[ord(m.group())-0xE000], u)
    u=u.replace('‌','')
    out.append(f"{align}|{u}")
open(sys.argv[2],'w').write('\n'.join(out))
