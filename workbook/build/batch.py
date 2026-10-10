"""Generic batch builder: python3 batch.py SRC DST DATE 'README label' 'README text' 'README C' module1 module2 ..."""
import copy
import importlib
import sys
sys.path.insert(0, sys.path[0])
from wblib import WB

SRC, DST, DATE, RLABEL, RTEXT, RC = sys.argv[1:7]
MODS = [importlib.import_module(m) for m in sys.argv[7:]]
B = WB(SRC)
wb = B.wb


def copy_style(ws, src_r, dst_r, ncol):
    for c in range(1, ncol + 1):
        s, d = ws.cell(src_r, c), ws.cell(dst_r, c)
        d.font = copy.copy(s.font); d.alignment = copy.copy(s.alignment); d.border = copy.copy(s.border); d.fill = copy.copy(s.fill)


for mod in MODS:
    st, si, site = mod.ST, mod.STUDY_INFO, mod.SITE
    s0 = mod.SITES[0]
    v = {'No.': st['no'], 'SERIAL NO': st['serial'], 'Authors': st['authors'], 'Year': st['year'], 'Journal': st['journal'], 'Full reference': st['ref'],
         'DOI / link': ('https://doi.org/' + st['doi']) if st.get('doi') else 'Not available', 'Country': site['country'], 'Site/Location': site['site'],
         'latitude': site['lat'], 'longitude': site['lon'], 'latitude (as reported)': s0[1], 'longitude (as reported)': s0[2], 'Coordinates source': s0[5],
         'CLIMATE': site['climate'], 'Experiment established (year)': si.get('estab'), 'year of data collection/experiment': si.get('yeardata'),
         'Years of data reported': si.get('years'), 'DURATION': site.get('duration'), 'SOIL': site.get('soil'), 'Texture as reported': si.get('texture'),
         'Crop rotation': si.get('rotation'), 'Wheat variety': si.get('wheatvar'), 'Rice variety': si.get('ricevar'), 'N dose (kg/ha)': si.get('N'),
         'P dose (kg/ha)': si.get('P'), 'K dose (kg/ha)': si.get('K'), 'Residue type & rate (t/ha)': si.get('residue'), 'Irrigation / water management': si.get('irrigation'),
         'Treatments in paper': si.get('treatments'), 'Parameters extracted': si.get('params'), 'Supplementary data?': si.get('supp'), 'Notes/Doubts': si.get('notes')}
    for k in ('sand', 'silt', 'CLAY', 'ph (initial)', 'soc (initial)', 'Bdi', 'MIN TEMP', 'MAX TEMP', 'AVG T', 'RAIN FALL'):
        if site.get(k) is not None:
            v[k] = site[k]
    B.add_row('Study_Info', v)
    for sname, glat, glon, la, lo, src, cl, note in mod.SITES:
        B.add_row('LAT_LONG', {'No.': st['no'], 'SERIAL NO': st['serial'], 'Authors': st['authors'], 'Year': st['year'], 'Country': site['country'].split(' (')[0],
                               'Site/Location': sname, 'latitude (as reported)': glat, 'longitude (as reported)': glon, 'latitude': la, 'longitude': lo,
                               'Coordinates source': src, 'CLIMATE': cl, 'Notes': note})
    for lab, desc, rice, wheat, res, rate, code, rat, conf, status in mod.TM:
        B.add_row('Treatment_Mapping', {'No.': st['no'], 'SERIAL NO': st['serial'], 'Authors': st['authors'], 'Year': st['year'],
                                        "Paper's treatment label (verbatim)": lab, 'Full description from paper': desc, 'Rice-phase tillage': rice,
                                        'Wheat-phase tillage': wheat, 'Residue retained?': res, 'Residue rate (t/ha)': rate, 'ASSIGNED CODE': code,
                                        'Rationale': rat, 'Confidence': conf, 'Status': status})

added = []
for mod in MODS:
    added += mod.rows(B)

for ex in getattr(MODS[0], 'EXCLUDED', []):
    pass
EXTRA_EXCL = []
for mod in MODS:
    EXTRA_EXCL += getattr(mod, 'EXCLUDED', [])
for e in EXTRA_EXCL:
    B.add_row('EXCLUDED_rows', e)

# Bibliography (alphabetical by first-author surname)
bib = wb['Bibliography']
def surname(t):
    return str(t).replace(',', ' ').split()[0].lower()
nb = 0
for mod in MODS:
    st = mod.ST
    text = st['ref'].replace(f", doi {st['doi']}.", '.') + (f" https://doi.org/{st['doi']}" if st.get('doi') else '')
    link = ('https://doi.org/' + st['doi']) if st.get('doi') else 'N/A'
    last = bib.max_row
    while bib.cell(last, 3).value is None:
        last -= 1
    pos = last + 1
    for r in range(5, last + 1):
        if surname(bib.cell(r, 3).value) > surname(text):
            pos = r; break
    bib.insert_rows(pos)
    copy_style(bib, 5 if pos > 5 else 6, pos, 4)
    bib.cell(pos, 2).value = st['serial']; bib.cell(pos, 3).value = text; bib.cell(pos, 4).value = link
    nb += 1
last = bib.max_row
while bib.cell(last, 3).value is None:
    last -= 1
for i, r in enumerate(range(5, last + 1), 1):
    bib.cell(r, 1).value = i
import re
bib['A2'].value = re.sub(r'\d+ references', f'{last - 4} references', bib['A2'].value)

# README
rd = wb['README']
rr = rd.max_row
while rd.cell(rr, 1).value is None:
    rr -= 1
copy_style(rd, rr, rr + 1, 3)
rd.cell(rr + 1, 1).value = RLABEL; rd.cell(rr + 1, 2).value = RTEXT; rd.cell(rr + 1, 3).value = RC

# index sheets
names = wb.sheetnames
data_sheets = names[names.index('LAT_LONG'):names.index('EXCLUDED_rows')]
cnt = {}
for nme in data_sheets:
    ws = wb[nme]; bc = B.hdr(nme)['SERIAL NO']; c = {}
    for r in range(2, ws.max_row + 1):
        val = ws.cell(r, bc).value
        if val is None:
            continue
        k = str(val).strip(); c[k] = c.get(k, 0) + 1
    cnt[nme] = c
sp = wb['STUDIES_BY_PARAMETER']
for r in range(4, sp.max_row + 1):
    nme = sp.cell(r, 2).value
    if nme in cnt:
        c = cnt[nme]
        sp.cell(r, 4).value = sum(c.values()); sp.cell(r, 5).value = len(c)
        sp.cell(r, 6).value = '; '.join(f'{k}: {v}' for k, v in c.items()) or 'NO DATA'
ps = wb['PARAMETERS_BY_STUDY']
lr = ps.max_row
while ps.cell(lr, 2).value is None:
    lr -= 1
tpl = lr
for mod in MODS:
    st = mod.ST; s = str(st['serial'])
    parts = [(nme, cnt[nme][s]) for nme in data_sheets if s in cnt[nme]]
    lr += 1
    copy_style(ps, tpl, lr, 10)
    for c, val in enumerate([st['no'], st['serial'], st['authors'], st['year'], st['journal'], 'INCLUDED', sum(v for _, v in parts), len(parts),
                             '; '.join(f'{k}: {v}' for k, v in parts), mod.STUDY_INFO['params']], 1):
        ps.cell(lr, c).value = val
for sh in (sp, ps):
    sh['A1'].value = re.sub(r'\(\d{4}-\d{2}-\d{2}\)', f'({DATE})', sh['A1'].value)

wb.calculation.fullCalcOnLoad = True
wb.save(DST)
from collections import Counter
print('rows added per sheet:', dict(Counter(s for s, _ in B.log)))
print('data rows:', len(added), 'bibliography +', nb)
