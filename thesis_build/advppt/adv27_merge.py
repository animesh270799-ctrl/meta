"""Insert the user's own slides (taken unchanged from their edited deck) into the generated 2026-27 advisory deck.
usage: python3 adv27_merge.py generated.pptx user_deck.pptx out.pptx AFTER_TITLE user_slide_numbers...
The user slides are placed, in order, right after the generated slide whose title starts with AFTER_TITLE.
Media are copied, the layout is mapped to the generated DEFAULT layout, notes are dropped, and the slide ids are
registered in presentation.xml, its relationships, the content types and the section that holds the anchor slide."""
import sys, os, re, shutil, zipfile, tempfile
gen, user, out, anchor_title = sys.argv[1:5]; nums = [int(x) for x in sys.argv[5:]]
T = tempfile.mkdtemp(); G, U = os.path.join(T, 'g'), os.path.join(T, 'u')
for src, dst in ((gen, G), (user, U)): zipfile.ZipFile(src).extractall(dst)
os.makedirs(os.path.join(G, 'ppt/media'), exist_ok=True)
rd = lambda p: open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)
def order(D):
    pres = rd(os.path.join(D, 'ppt/presentation.xml')); rels = rd(os.path.join(D, 'ppt/_rels/presentation.xml.rels'))
    rm = {re.search(r'Id="(rId\d+)"', r).group(1): re.search(r'Target="([^"]+)"', r).group(1) for r in re.findall(r'<Relationship [^>]*/>', rels)}
    return [(sid, rid, rm[rid]) for sid, rid in re.findall(r'<p:sldId id="(\d+)" r:id="(rId\d+)"/>', pres)]
def title(D, target):
    x = rd(os.path.join(D, 'ppt', target)); t = re.findall(r'<a:t>([^<]*)</a:t>', x); return t[0] if t else ''
go, uo = order(G), order(U)
anchor = next(i for i, (sid, rid, tg) in enumerate(go) if title(G, tg).startswith(anchor_title))
anchor_id = go[anchor][0]
nslide = max(int(re.search(r'slide(\d+)\.xml', tg).group(1)) for _, _, tg in go)
pres = rd(os.path.join(G, 'ppt/presentation.xml')); prel = rd(os.path.join(G, 'ppt/_rels/presentation.xml.rels')); ct = rd(os.path.join(G, '[Content_Types].xml'))
maxid = max(int(sid) for sid, _, _ in go); maxrid = max(int(x) for x in re.findall(r'Id="rId(\d+)"', prel))
new_ids = []
for k, n in enumerate(nums):
    sid, rid, tg = uo[n - 1]; src = os.path.join(U, 'ppt', tg); nslide += 1; name = 'slide%d.xml' % nslide
    shutil.copy(src, os.path.join(G, 'ppt/slides', name))
    rels = rd(os.path.join(U, 'ppt/slides/_rels', os.path.basename(tg) + '.rels'))
    out_rels = []
    for r in re.findall(r'<Relationship [^>]*/>', rels):
        typ = re.search(r'Type="[^"]*/([A-Za-z]+)"', r).group(1); tgt = re.search(r'Target="([^"]+)"', r).group(1)
        if typ == 'notesSlide': continue
        if typ == 'slideLayout': r = r.replace(tgt, '../slideLayouts/slideLayout1.xml')
        elif typ == 'image':
            mname = 'user%d_%s' % (n, os.path.basename(tgt)); shutil.copy(os.path.normpath(os.path.join(os.path.dirname(src), tgt)), os.path.join(G, 'ppt/media', mname))
            r = r.replace(tgt, '../media/' + mname); ext = mname.rsplit('.', 1)[1].lower()
            if 'Extension="%s"' % ext not in ct:
                ct = ct.replace('<Default ', '<Default Extension="%s" ContentType="image/%s"/><Default ' % (ext, 'jpeg' if ext in ('jpg', 'jpeg') else ext), 1)
        out_rels.append(r)
    wr(os.path.join(G, 'ppt/slides/_rels', name + '.rels'), '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + ''.join(out_rels) + '</Relationships>')
    ct = ct.replace('</Types>', '<Override PartName="/ppt/slides/%s" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/></Types>' % name)
    maxrid += 1; maxid += 1; new_ids.append(str(maxid))
    prel = prel.replace('</Relationships>', '<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/%s"/></Relationships>' % (maxrid, name))
    prev = anchor_id if k == 0 else new_ids[-2]
    pres = re.sub(r'(<p:sldId id="%s" r:id="rId\d+"/>)' % prev, r'\1<p:sldId id="%d" r:id="rId%d"/>' % (maxid, maxrid), pres, count=1)
    pres = re.sub(r'(<p14:sldId id="%s"/>)' % prev, r'\1<p14:sldId id="%d"/>' % maxid, pres, count=1)
wr(os.path.join(G, 'ppt/presentation.xml'), pres); wr(os.path.join(G, 'ppt/_rels/presentation.xml.rels'), prel); wr(os.path.join(G, '[Content_Types].xml'), ct)
app = os.path.join(G, 'docProps/app.xml')
if os.path.exists(app):
    a = rd(app); n_all = len(re.findall(r'<p:sldId ', pres)); wr(app, re.sub(r'<Slides>\d+</Slides>', '<Slides>%d</Slides>' % n_all, a))
if os.path.exists(out): os.remove(out)
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(G):
        for f in files:
            p = os.path.join(root, f); arc = os.path.relpath(p, G)
            z.write(p, arc, compress_type=zipfile.ZIP_STORED if arc == 'mimetype' else zipfile.ZIP_DEFLATED)
shutil.rmtree(T); print('merged', len(nums), 'user slides after', repr(anchor_title), '->', out, '; total slides', len(re.findall(r'<p:sldId ', pres)))
