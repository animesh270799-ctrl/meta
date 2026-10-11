"""Build META_ANALYSIS_MASTER updated 140: ext 641-645."""
import copy
import sys
from openpyxl.styles import Font

sys.path.insert(0, sys.path[0])
from wblib import WB
import s319, s320, s321, s322

SRC, DST = sys.argv[1], sys.argv[2]
DATE = '2026-10-11'
B = WB(SRC)
wb = B.wb

STUDIES = [
    (s319, [('Ludhiana', 'PAU FMPE research farm, Ludhiana (Exp. 1-3)', "30 54' N", "75 48' E", 30.9, 75.8, 'Paper', 'TEMP', 'Exp. 1-2 Location 1; Exp. 3 location not stated (assumed)'),
            ('Ladhowal', 'PAU Seed Farm, Ladhowal (Exp. 2 Location 2)', 'not reported', 'not reported', 30.99, 75.74, 'Google Maps (approximate)', 'TEMP', '18 km from Location 1'),
            ('Punjab farms', "8 farmers' fields (Ludhiana, Sangrur, Kapurthala, Fatehgarh Sahib)", 'not reported', 'not reported', 30.95, 75.6, 'Approximate (centre of the districts)', 'TEMP', 'On-farm Exp. 4, 2020-21')],
     'India (Punjab)', 'PAU FMPE research farm, Ludhiana; PAU Seed Farm, Ladhowal; 8 farmers\' fields (Punjab)', 30.9, 75.8, "30 54' N", "75 48' E",
     'Reported in paper (Ludhiana); Ladhowal and farms approximate', 'TEMP', None, None),
    (s320, [('Karnal', 'ICAR-IIWBR research farm, Karnal', "29 43' N", "76 58' E", 29.717, 76.967, 'Paper', 'ST', None)],
     'India (Haryana)', s320.SITE['site'], 29.717, 76.967, "29 43' N", "76 58' E", 'Reported in paper', 'ST', 'LOAMY', None),
    (s321, [('Karnal', 'Taraori, Karnal (CCAFS climate-smart village trial)', "29 48' N", "76 55' E", 29.8, 76.917, 'Paper', 'ST', 'K1-K6, est. June 2012'),
            ('Samastipur', 'BISA farm, Pusa, Samastipur', "25 57' N", "85 40' E", 25.95, 85.667, 'Paper', 'ST', 'S1-S4, est. Nov 2012')],
     'India (Haryana, Bihar)', 'Taraori, Karnal (Haryana) and BISA farm, Pusa, Samastipur (Bihar) - two sites', 29.8, 76.917, "29 48' N / 25 57' N", "76 55' E / 85 40' E",
     'Reported in paper', 'ST', 'LOAMY', None),
    (s322, [('Jabalpur', 'DWSR research farm, Jabalpur', "23 09' 00\" N", "79 58' 00\" E", 23.15, 79.967, 'Paper', 'ST', None)],
     'India (Madhya Pradesh)', s322.SITE['site'], 23.15, 79.967, "23 09' N", "79 58' E", 'Reported in paper', 'ST', 'LOAMY', None),
]

# ---------------- Study_Info, LAT_LONG, Treatment_Mapping
for mod, sites, country, site, lat, lon, latr, lonr, csrc, clim, soil, _ in STUDIES:
    st = mod.ST; x = mod.STUDY_INFO_EXTRA if hasattr(mod, 'STUDY_INFO_EXTRA') else {}
    if mod is s321:
        x = dict(x, texture='Karnal loam (Anthraquic Haplustepts); Samastipur silty loam (Oxyaquic Haplustepts)',
                 notes=s321.NOTES_SI + ' ' + ' '.join(e['notes_extra'] for _, e in s321.SITE_ROWS))
    full = st['ref'].split(' doi ')[0].rstrip(',')
    v = {'No.': st['no'], 'SERIAL NO': st['serial'], 'Authors': st['authors'], 'Year': st['year'], 'Journal': st['journal'],
         'Full reference': st['ref'], 'DOI / link': 'https://doi.org/' + st['doi'], 'Country': country, 'Site/Location': site,
         'latitude': lat, 'longitude': lon, 'latitude (as reported)': latr, 'longitude (as reported)': lonr, 'Coordinates source': csrc,
         'CLIMATE': clim, 'Experiment established (year)': x.get('estab'), 'year of data collection/experiment': x.get('yeardata'),
         'Years of data reported': x.get('years'), 'DURATION': '4-10 Y' if mod is s321 else '0-3 Y', 'SOIL': soil, 'Texture as reported': x.get('texture'),
         'Crop rotation': x.get('rotation'), 'Wheat variety': x.get('wheatvar'), 'Rice variety': x.get('ricevar'),
         'N dose (kg/ha)': x.get('N'), 'P dose (kg/ha)': x.get('P'), 'K dose (kg/ha)': x.get('K'), 'Residue type & rate (t/ha)': x.get('residue'),
         'Irrigation / water management': x.get('irrigation'), 'Treatments in paper': x.get('treatments'), 'Parameters extracted': x.get('params'),
         'Supplementary data?': x.get('supp'), 'Notes/Doubts': x.get('notes')}
    if mod is s320:
        v.update({'sand': 63.1, 'silt': 26.7, 'CLAY': 10.2, 'ph (initial)': 7.3, 'soc (initial)': 4.2, 'Bdi': 1.47, 'MIN TEMP': 17.1, 'MAX TEMP': 29.9, 'AVG T': 23.5, 'RAIN FALL': 744})
    if mod is s322:
        v.update({'CLAY': 48.45, 'ph (initial)': 7.3, 'soc (initial)': 5.4, 'Bdi': 1.63, 'RAIN FALL': 1386})
    if mod is s321:
        v.update({'RAIN FALL': '670 (Karnal) / 1200 (Samastipur)', 'AVG T': '24 (Karnal) / 25.5 (Samastipur)'})
    B.add_row('Study_Info', v)
    for nm, sname, glat, glon, la, lo, src, cl, note in sites:
        B.add_row('LAT_LONG', {'No.': st['no'], 'SERIAL NO': st['serial'], 'Authors': st['authors'], 'Year': st['year'], 'Country': 'India',
                               'Site/Location': sname, 'latitude (as reported)': glat, 'longitude (as reported)': glon, 'latitude': la, 'longitude': lo,
                               'Coordinates source': src, 'CLIMATE': cl, 'Notes': note})
    for lab, desc, rice, wheat, res, rate, code, rat, conf, status in mod.TM:
        B.add_row('Treatment_Mapping', {'No.': st['no'], 'SERIAL NO': st['serial'], 'Authors': st['authors'], 'Year': st['year'],
                                        "Paper's treatment label (verbatim)": lab, 'Full description from paper': desc, 'Rice-phase tillage': rice,
                                        'Wheat-phase tillage': wheat, 'Residue retained?': res, 'Residue rate (t/ha)': rate, 'ASSIGNED CODE': code,
                                        'Rationale': rat, 'Confidence': conf, 'Status': status})

# ---------------- data rows
added = []
for mod, *_ in STUDIES:
    added += mod.rows(B)

# ---------------- EXCLUDED_rows: ext 645 = ext 299 (already excluded)
B.add_row('EXCLUDED_rows', {'Sheet': 'ALL', 'SERIAL NO': 'ext\\645.pdf = ext\\299 (not entered)', 'Authors': 'Mohanty M., Painuli D.K. & Mandal K.G.', 'Year': 2004,
                            'Reason for exclusion': ('REPEAT of an EXCLUDED paper (rule 136): Soil Tillage Res. 76:83-94 (doi 10.1016/j.still.2003.08.006) = ext\\299 - puddling-intensity trial in RICE only '
                                                     '(IISS Bhopal Vertisol, wet seasons 2000-01; field not cultivated to rice in previous years, no wheat phase; P0 no-puddling DSR vs P1 / P2 puddling by 4 / 8 power-tiller passes). '
                                                     'Rule 31 (rice-only trials excluded); rule 140 (puddling intensity) applies to rice-wheat trials only. Still excluded.'),
                            'Full row (header = value)': 'No rows.'})

# ---------------- Bibliography (insert alphabetically by first-author surname)
bib = wb['Bibliography']
def surname(t):
    return str(t).replace(',', ' ').split()[0].lower()
new_refs = [(m.ST['serial'], m.ST['ref'].replace(f", doi {m.ST['doi']}.", '.') + f" https://doi.org/{m.ST['doi']}", 'https://doi.org/' + m.ST['doi']) for m, *_ in STUDIES]
for serial, text, link in new_refs:
    last = bib.max_row
    while bib.cell(last, 3).value is None:
        last -= 1
    pos = last + 1
    for r in range(5, last + 1):
        if surname(bib.cell(r, 3).value) > surname(text):
            pos = r
            break
    tpl = 5
    bib.insert_rows(pos)
    for c in range(1, 5):
        s, d = bib.cell(tpl if tpl < pos else tpl + 1, c), bib.cell(pos, c)
        d.font = copy.copy(s.font); d.alignment = copy.copy(s.alignment); d.border = copy.copy(s.border); d.fill = copy.copy(s.fill)
    bib.cell(pos, 2).value = serial; bib.cell(pos, 3).value = text; bib.cell(pos, 4).value = link
last = bib.max_row
while bib.cell(last, 3).value is None:
    last -= 1
for i, r in enumerate(range(5, last + 1), 1):
    bib.cell(r, 1).value = i
bib['A2'].value = bib['A2'].value.replace('452 references', f'{last - 4} references')

# ---------------- README
rd = wb['README']
rr = rd.max_row
while rd.cell(rr, 1).value is None:
    rr -= 1
n = rr + 1
for c in range(1, 4):
    s, d = rd.cell(rr, c), rd.cell(n, c)
    d.font = copy.copy(s.font); d.alignment = copy.copy(s.alignment); d.fill = copy.copy(s.fill); d.border = copy.copy(s.border)
rd.cell(n, 1).value = f'ext 641-645 (updated 140, {DATE})'
rd.cell(n, 2).value = ('NEW 319 (641 Manpreet-Singh 2024 Sci Rep: PAU Smart Seeder PSS / Super Seeder SS = MTR rows a / b vs Happy Seeder = CA, + CT in 2020-21; '
                       'wheat yield, spike density (per m row -> per m2), spike length, grains / spike, TGW; on-farm PSS vs HS, Rep = 8 farms); '
                       'NEW 320 (642 Meena 2020 Agronomy, IIWBR Karnal: residue removed CT vs 4 t/ha retained CTR (ploughing implied - FLAG) x irrigation rows a-c: '
                       'yield, WUE, net return, B:C, derived cost / gross; main effects AGBM, straw, HI, tillers, TGW, grains / spike - Figs 3 / 5 digitised); '
                       'NEW 321 (643 Mishra A.K. 2024 FSUFS, Karnal CT / CTR / ZT / CA and Samastipur CT / CA, maize-bed treatments excluded: TOC, TN, POXC 0-5 / 5-15 cm at 3 and 5 yr, '
                       'TOC stocks, cPOM-C / fPOM-C / MOC / PON and BD / porosity derived, CL / LI / CPI / CMI derived, 5-yr yields, mungbean yield); '
                       'NEW 322 (644 Mishra J.S. & Singh 2012 STR, Jabalpur dry-seeded RW: ZT-ZT = ZT, CT-CT = CT, CT-ZT = pZT, ZT-CT excluded; yearly rice / wheat / system yield, '
                       '2008-09 system cost, net return, B:C, gross derived - tillage main effects, FLAG). Excluded: 645 (= ext 299, rice-only puddling trial). '
                       'Supplements of 641 / 643 not downloaded (permission).')
rd.cell(n, 3).value = 'Bibliography + 4. Next serial 323.'

# ---------------- index sheets
names = wb.sheetnames
data_sheets = names[names.index('LAT_LONG'):names.index('EXCLUDED_rows')]
cnt = {}
for nme in data_sheets:
    ws = wb[nme]; h = B.hdr(nme); bc = h['SERIAL NO']
    c = {}
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
        sp.cell(r, 4).value = sum(c.values())
        sp.cell(r, 5).value = len(c)
        sp.cell(r, 6).value = '; '.join(f'{k}: {v}' for k, v in c.items()) or 'NO DATA'
sp['A1'].value = sp['A1'].value.replace('(2026-10-11)', f'({DATE})')
ps = wb['PARAMETERS_BY_STUDY']
ps['A1'].value = ps['A1'].value.replace('(2026-10-11)', f'({DATE})')
lr = ps.max_row
while ps.cell(lr, 2).value is None:
    lr -= 1
tpl = lr
for mod, *_ in STUDIES:
    st = mod.ST; s = str(st['serial'])
    parts = [(nme, cnt[nme][s]) for nme in data_sheets if s in cnt[nme]]
    lr += 1
    for c in range(1, 11):
        a, d = ps.cell(tpl, c), ps.cell(lr, c)
        d.font = copy.copy(a.font); d.alignment = copy.copy(a.alignment); d.border = copy.copy(a.border); d.fill = copy.copy(a.fill)
    vals = [st['no'], st['serial'], st['authors'], st['year'], st['journal'], 'INCLUDED', sum(v for _, v in parts), len(parts),
            '; '.join(f'{k}: {v}' for k, v in parts), mod.STUDY_INFO_EXTRA['params']]
    for c, val in enumerate(vals, 1):
        ps.cell(lr, c).value = val

wb.calculation.fullCalcOnLoad = True
wb.save(DST)
from collections import Counter
print('rows added per sheet:', dict(Counter(s for s, _ in B.log)))
print('total data rows:', len(added))
