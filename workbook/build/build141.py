"""Build META_ANALYSIS_MASTER updated 141 from updated 140: author requests on ext 641 / 643 + 643 supplement."""
import copy
import sys
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

sys.path.insert(0, sys.path[0])
from wblib import WB
from common import base, notes
import s319, s321

SRC, DST = sys.argv[1], sys.argv[2]
DATE = '2026-10-11'
B = WB(SRC)
wb = B.wb
STYLE_SRC = {}  # new sheet -> (template sheet, template data row)

# ---------------------------------------------------------------- new sheets
def new_sheet(name, tpl, after, rename, drop=(), unit='', depth_list=None):
    t = wb[tpl]
    ws = wb.create_sheet(name, wb.sheetnames.index(after) + 1)
    keep = [c for c in range(1, t.max_column + 1) if t.cell(1, c).value not in drop]
    for k, c in enumerate(keep, 1):
        s, d = t.cell(1, c), ws.cell(1, k)
        v = s.value
        for old, new in rename:
            if isinstance(v, str) and v.startswith(old):
                v = new + v[len(old):]
        d.value = v
        d.font = copy.copy(s.font); d.fill = copy.copy(s.fill); d.alignment = copy.copy(s.alignment); d.border = copy.copy(s.border)
        ws.column_dimensions[get_column_letter(k)].width = t.column_dimensions[get_column_letter(c)].width
    ws.row_dimensions[1].height = t.row_dimensions[1].height
    ws.freeze_panes = 'D2'
    last = get_column_letter(len(keep))
    if t.auto_filter.ref:
        ws.auto_filter.ref = f'A1:{last}1'
    # unit note (orange) in row 2 of the last column, as on every sheet
    s2 = t.cell(2, t.max_column)
    ws.cell(2, len(keep)).value = unit
    ws.cell(2, len(keep)).font = copy.copy(s2.font)
    hdr = {ws.cell(1, k).value: get_column_letter(k) for k in range(1, len(keep) + 1)}
    lists = {'CLIMATE': '"ST,TEMP"', 'SOIL': '"LOAMY,SANDY,CLAYEY"', 'DURATION': '"0-3 Y,4-10 Y,>10 Y"'}
    if depth_list:
        lists['DEPTH'] = depth_list
    for h, f in lists.items():
        dv = DataValidation(type='list', formula1=f, allow_blank=True)
        dv.add(f'{hdr[h]}2:{hdr[h]}1002')
        ws.add_data_validation(dv)
    STYLE_SRC[name] = (tpl, B.template_row(tpl), keep)
    return ws

CUM = '"0-10 CM,0-20 CM,0-30 CM,0-40 CM,0-50 CM,0-60 CM"'
new_sheet('stock-TN', 'stock-SOC', 'stock-SOC', [('SOCs_', 'TNs_')], drop=('initial', 'change ca', 'change ct'),
          unit='Mg N/ha (soil total N stock, cumulative depth from the surface; STOCK = TN (g/kg) x BD x D(cm) x 0.1)', depth_list=CUM)
new_sheet('stock-POXC', 'stock-TN', 'stock-TN', [('TNs_', 'POXCs_')],
          unit='Mg C/ha (permanganate-oxidisable C stock, cumulative depth from the surface; POXC (mg/kg) x BD x D(cm) x 1e-4)', depth_list=CUM)
new_sheet('MACHINE FIELD CAPACITY', 'C input', 'NET ECONOMIC BENEFIT', [('CIN_', 'EFC_')], drop=('N APPLIED (kg/ha)',),
          unit='ha/h (EFFECTIVE field capacity of the sowing / tillage machine = area covered per hour of operation; not soil field capacity)')
# hdr cache was built for C input / stock-SOC templates only; new sheets get fresh caches
B._hdr.pop('stock-TN', None); B._hdr.pop('stock-POXC', None); B._hdr.pop('MACHINE FIELD CAPACITY', None)

# style rows of new sheets from the template's last data row (column-mapped)
_orig_add = B.add_row
def add_row(sheet, vals, red=False):
    r = _orig_add(sheet, vals, red)
    if sheet in STYLE_SRC:
        tpl, tr, keep = STYLE_SRC[sheet]
        t, ws = wb[tpl], wb[sheet]
        if sheet == 'stock-POXC':  # template is itself new: use stock-SOC mapping
            t = wb['stock-SOC']; tr = B.template_row('stock-SOC'); keep = STYLE_SRC['stock-TN'][2]
        for k, c in enumerate(keep, 1):
            s, d = t.cell(tr, c), ws.cell(r, k)
            d.border = copy.copy(s.border); d.alignment = copy.copy(s.alignment); d.number_format = s.number_format
            d.font = copy.copy(s.font); d.fill = copy.copy(s.fill)
        h = B.hdr(sheet)
        ws.cell(r, h['Notes/Doubts']).fill = copy.copy(wb['TOC'].cell(B.template_row('TOC'), B.hdr('TOC')['Notes/Doubts']).fill)
    return r
B.add_row = add_row

# ---------------------------------------------------------------- 641: machine effective field capacity (Table 3)
st = s319.ST
for tag, m, val, se in (('a', 'PSS', 0.38, '0.025'), ('b', 'SS', 0.25, '0.002')):
    obs, nt = notes(st, f"ROW {tag}: CA = Happy Seeder (HS), MTR = {m} (Smart Seeder PSS row a / Super Seeder SS row b, rotary rule - FLAG). Exp. 2 Location 1 (PAU FMPE farm, straw 6.0 t/ha). "
                        f"Table 3 EFFECTIVE FIELD CAPACITY of the sowing machine (mean +/- SE: PSS 0.38 +/- 0.025, SS 0.25 +/- 0.002, HS 0.38 +/- 0.008 ha/h). "
                        f"Fuel consumption (PSS 5.72 / SS 6.77 / HS 4.50 l/h; 14.98 / 19.54 / 11.88 l/ha) - no sheet. Exp. 1 (PSS only, Table 1: 0.30-0.46 ha/h by speed index) - no contrast. "
                        f"Author request 2026-10-11 (new sheet). Rice phase not described (rule 23).", t=2)
    v = base(st, s319.S_LDH, {'year of data collection/experiment': '2019-20', 'YEAR OF DATA (duration)': 'wheat sowing 2019-20'})
    v.update({'EFC_CA': 0.38, 'EFC_MTR': val, 'UNIT': 'ha/h (effective field capacity)', 'Crop/season of sampling': 'Wheat sowing, 9 Nov 2019',
              'Data source': 'Table 3', 'Method used (from paper)': 'Effective field capacity = area sown / total operating time (ha/h), John Deere 5310 (50 hp) tractor; 3 reps, 50 m2 plots.',
              'Fertilizer dose & other management': s319.FERT + '; rice PR 121, straw 6.0 t/ha', 'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
    B.add_row('MACHINE FIELD CAPACITY', v)

# ---------------------------------------------------------------- 643: TN and POXC stocks, supplement data
st = s321.ST
SUPP = 'SUPP DATA\\643.docx (author-supplied 2026-10-11)'
UPD = f'UPDATE {DATE} (updated 141): '

def srow(sheet, s, yr, vals, body, y=1, t=1, d=1):
    site = s321.site_of(s); n, dur = s321.YRS[(s, yr)]
    obs, nt = notes(st, body, y, t, d)
    v = base(st, site, {'DURATION': dur, 'year of data collection/experiment': yr, 'YEAR OF DATA (duration)': f'{n} yr (sampled {yr})'})
    v.update(vals); v.update({'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
    return B.add_row(sheet, v)

def head(s, yr):
    n, _ = s321.YRS[(s, yr)]
    return (f'KARNAL {yr} ({n} yr): CT = K1, CTR = K2, ZT = K3, CA = K4 (K1 1 rotavator pass kept CT - FLAG; mungbean only in K2 / K4, rule 71).' if s == 'K' else
            f'SAMASTIPUR {yr} ({n} yr): CT = S1, CA = S2 (mungbean only in CA, rule 71).') + ' Sampling season not stated.'

for (s, yr, ly), rws in s321.T45.items():
    if ly == '5-15':
        continue
    cls = '0-10 CM' if ly == '0-5' else '0-20 CM'
    tab4, tab6, _ = s321.TABLES[s]
    codes = s321.codes_of(s)
    mid = s321.T45[(s, yr, '5-15')]
    k4 = (' K4 2015 0-5 cm TOC stock looks misprinted (BD 2.23 implied) - TN stock kept as printed.' if (s, yr) == ('K', 2015) else '')
    srow('stock-TN', s, yr, {'DEPTH': cls, 'DEPTH (as reported in paper)': f'{ly} cm', **{f'TNs_{c}': r[3] for c, r in zip(codes, rws)},
                             'UNIT': 'Mg N/ha (TN stock as printed)', 'Crop/season of sampling': f'Soil {yr}', 'Data source': tab4,
                             'Method used (from paper)': 'TN stock = soil mass (BD x 500 for 0-5 cm, x 1000 for 5-15 cm) x TN; 0-15 cm = sum of layers (Eqs. 3-5); TN by NC analyser.'},
         head(s, yr) + f' {tab4} TN stock {ly} cm (printed). 5-15 cm layer TN stocks: ' + ', '.join(f'{c} {r[3]}' for c, r in zip(codes, mid)) +
         ' Mg/ha (in the 0-15 cm sum). NEW SHEET (author request 2026-10-11).' + k4)
    px = s321.T67[(s, yr, ly)]; pmid = s321.T67[(s, yr, '5-15')]
    srow('stock-POXC', s, yr, {'DEPTH': cls, 'DEPTH (as reported in paper)': f'{ly} cm', **{f'POXCs_{c}': p[1] for c, p in zip(codes, px)},
                               'UNIT': 'Mg C/ha (POXC stock as printed)', 'Crop/season of sampling': f'Soil {yr}', 'Data source': tab6,
                               'Method used (from paper)': 'POXC stock = POXC concentration x BD x soil depth (paper section 2.7); POXC by 0.02 M KMnO4 (Culman et al. 2012).'},
         head(s, yr) + f' {tab6} POXC stock {ly} cm (printed). 5-15 cm layer POXC stocks: ' + ', '.join(f'{c} {p[1]}' for c, p in zip(codes, pmid)) +
         ' Mg/ha. NEW SHEET (author request 2026-10-11).')

# Karnal 5-15 cm POM fractions (Supplementary Table S3)
S3 = {2015: [((1.35, 42.6, 56.1), (0.64, 1.17, 5.27), (0.08, 0.59, 1.14)), ((1.59, 38.9, 59.2), (0.58, 1.38, 5.65), (0.06, 0.52, 1.30)),
             ((1.51, 42.3, 56.2), (0.71, 1.55, 6.35), (0.07, 0.83, 0.61)), ((1.61, 40.8, 57.8), (0.77, 2.16, 6.28), (0.08, 0.72, 0.87))],
      2017: [((2.02, 39.2, 58.1), (0.84, 1.50, 4.91), (0.11, 0.56, 0.71)), ((2.01, 39.1, 58.9), (1.02, 1.69, 6.92), (0.14, 0.56, 1.15)),
             ((2.47, 37.6, 57.8), (1.23, 1.61, 6.58), (0.08, 0.59, 0.83)), ((2.99, 38.9, 58.6), (1.52, 2.41, 9.01), (0.08, 0.91, 1.21))]}
M_POM = s321.M_POM
for yr, fr in S3.items():
    rws = s321.T45[('K', yr, '5-15')]
    codes = s321.KC
    dd = {'DEPTH': '0-15 CM', 'DEPTH (as reported in paper)': '5-15 cm', 'Crop/season of sampling': f'Soil {yr}'}
    mass = '; '.join(f'{c} {f[0][0]} / {f[0][1]} / {f[0][2]}' for c, f in zip(codes, fr))
    cst = '; '.join(f'{c} {f[1][0]} / {f[1][1]} / {f[1][2]}' for c, f in zip(codes, fr))
    nst = '; '.join(f'{c} {f[2][0]} / {f[2][1]} / {f[2][2]}' for c, f in zip(codes, fr))
    body = (head('K', yr) + f' Supplementary Table S3 ({SUPP}) Karnal 5-15 cm. Fraction concentrations per kg BULK soil DERIVED = fraction stock x TOC / TOC stock of the 5-15 cm layer (Table 4) - FLAG. '
            f'Printed: mass % cPOM / fPOM / OMF {mass}; C stock (Mg C/ha) {cst}; N stock (Mg N/ha) {nst}. Differences among treatments NS (all "a").')
    src = f'Supplementary Table S3 + Table 4 (DERIVED)'
    for sheet, pre, i, unit in (('cPOM-C', 'cPOMC', 0, 'g/kg bulk soil (cPOM 2000-250 um C; DERIVED)'), ('fPOM-C', 'fPOMC', 1, 'g/kg bulk soil (fPOM 250-53 um C; DERIVED)'),
                                ('MOC', 'MOC', 2, 'g/kg bulk soil (organo-mineral fraction <53 um C, Tyurin; DERIVED)')):
        srow(sheet, 'K', yr, dict(dd, **{f'{pre}_{c}': f'=ROUND({f[1][i]}*{r[0]}/{r[1]},3)' for c, r, f in zip(codes, rws, fr)}, UNIT=unit,
                                  **{'Data source': src, 'Method used (from paper)': M_POM}), body, d=2)
    srow('PON', 'K', yr, dict(dd, **{f'PON_{c}': f'=ROUND(({f[2][0]}+{f[2][1]})*{r[0]}/{r[1]}*1000,0)' for c, r, f in zip(codes, rws, fr)},
                              UNIT='mg/kg bulk soil (PON = cPOM-N + fPOM-N; DERIVED)', **{'Data source': src, 'Method used (from paper)': M_POM}),
         body + ' PON = (cPOM N + fPOM N stock) / soil mass.', d=2)

# C input (Supplementary Table S2, annual plant-derived C returned to soil)
S2 = {'K': [(0.57, 0.53, 0.00, 1.10), (2.12, 1.84, 0.43, 4.38), (0.59, 0.64, 0.00, 1.16), (2.19, 1.96, 0.48, 4.63)],
      'S': [(0.48, 0.48, 0.00, 0.96), (2.42, 2.06, 0.84, 5.32)]}
for s, data in S2.items():
    codes = s321.codes_of(s)
    site = s321.site_of(s)
    comp = '; '.join(f'{c}: rice {a} + wheat {b} + mungbean {m} = {t}' for c, (a, b, m, t) in zip(codes, data))
    obs, nt = notes(st, ('KARNAL: CT = K1, CTR = K2, ZT = K3, CA = K4.' if s == 'K' else 'SAMASTIPUR: CT = S1, CA = S2.') +
                    f' Supplementary Table S2 ({SUPP}): ANNUAL plant-derived C input (straw + stubble + root) returned to soil, Mg C/ha x 1000. '
                    f'Components (Mg C/ha): {comp}. Averaging period not stated (assumed trial mean - FLAG). Residue C / N contents (Table S1, % C 35-47, % N 0.39-1.84) - no sheet. '
                    'Crop input, not a soil sampling (rule 120).')
    v = base(st, site, {'DURATION': '4-10 Y', 'year of data collection/experiment': '2012-2017' if s == 'K' else '2012-2018', 'YEAR OF DATA (duration)': 'annual mean (period not stated)'})
    v.update({f'CIN_{c}': f'=ROUND({t}*1000,0)' for c, (a, b, m, t) in zip(codes, data)})
    v.update({'UNIT': 'kg C/ha/yr (plant-derived C input: straw + stubble + root; printed Mg C/ha x 1000)', 'Crop/season of sampling': 'Annual (rice + wheat + mungbean)',
              'Data source': 'Supplementary Table S2', 'Method used (from paper)': 'Residue, stubble (0.5 x 0.5 m quadrats) and root (0-15 cm) biomass x C content (NC analyser, dry combustion).',
              'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
    B.add_row('C input', v)

# ---------------------------------------------------------------- notes / Study_Info updates on existing 319 / 321 rows
def fix_notes(sheet, serial, old, new, prefix=None):
    ws = wb[sheet]; h = B.hdr(sheet); n = 0
    for r in range(2, ws.max_row + 1):
        if str(ws.cell(r, h['SERIAL NO']).value) != serial:
            continue
        c = ws.cell(r, h['Notes/Doubts'])
        if c.value and old in c.value:
            c.value = (prefix or '') + c.value.replace(old, new); n += 1
    return n

cnt = 0
cnt += fix_notes('cPOM-C', '321', 'Karnal 5-15 cm fractions are in Supplementary Table S4 (not downloaded). ', 'Karnal 5-15 cm fractions entered from Supplementary Table S3. ', UPD + 'supplement supplied. ')
for sh in ('fPOM-C', 'MOC', 'PON'):
    cnt += fix_notes(sh, '321', 'Karnal 5-15 cm fractions are in Supplementary Table S4 (not downloaded). ', 'Karnal 5-15 cm fractions entered from Supplementary Table S3. ', UPD + 'supplement supplied. ')
cnt += fix_notes('total N', '321', 'Mg/ha - no sheet.', 'Mg/ha - stocks now on the stock-TN sheet.', UPD + 'TN stocks entered on the new stock-TN sheet. ')
cnt += fix_notes('POXC(KMnO4-C)', '321', ' - not entered (no stock sheet / layers entered).', ' - POXC stocks now on the stock-POXC sheet (0-15 cm concentration not entered; layers entered).', UPD + 'POXC stocks entered on the new stock-POXC sheet. ')
cnt += fix_notes('YIELD', '319', 'fuel and field capacity (Tables 3-4): no sheet.', 'fuel (Tables 3-4): no sheet; machine field capacity on MACHINE FIELD CAPACITY (updated 141).')
print('notes updated:', cnt)

si = wb['Study_Info']; h = B.hdr('Study_Info')
for r in range(2, si.max_row + 1):
    sv = str(si.cell(r, h['SERIAL NO']).value)
    if sv == '321':
        si.cell(r, h['Supplementary data?']).value = ('Yes - ' + SUPP + ': Fig. S1 layout; Table S1 residue C / N % (no sheet); Table S2 annual C inputs (C input sheet); '
                                                      'Table S3 Karnal 5-15 cm POM fractions (entered); Tables S4-S5 0-15 cm fraction totals (notes only - layers entered).')
        si.cell(r, h['Parameters extracted']).value += ('; [updated 141] TN stock (stock-TN) and POXC stock (stock-POXC) 0-5 / 0-15 cm; Karnal 5-15 cm cPOM-C, fPOM-C, MOC, PON (Suppl. Table S3); '
                                                        'annual plant C input (Suppl. Table S2)')
        si.cell(r, h['Notes/Doubts']).value = UPD + 'author supplied the supplement (643.docx) and asked for N and POXC stocks (new sheets stock-TN, stock-POXC). ' + si.cell(r, h['Notes/Doubts']).value
    if sv == '319':
        si.cell(r, h['Parameters extracted']).value += '; [updated 141] machine effective field capacity (MACHINE FIELD CAPACITY sheet, Table 3)'
        si.cell(r, h['Notes/Doubts']).value = UPD + 'machine effective field capacity entered on the new MACHINE FIELD CAPACITY sheet (author request). ' + si.cell(r, h['Notes/Doubts']).value
# Treatment_Mapping unchanged.

# ---------------------------------------------------------------- README
rd = wb['README']
rr = rd.max_row
while rd.cell(rr, 1).value is None:
    rr -= 1
n = rr + 1
for c in range(1, 4):
    s_, d_ = rd.cell(rr, c), rd.cell(n, c)
    d_.font = copy.copy(s_.font); d_.alignment = copy.copy(s_.alignment); d_.fill = copy.copy(s_.fill); d_.border = copy.copy(s_.border)
rd.cell(n, 1).value = f'Author requests on ext 641 / 643 + 643.docx (updated 141, {DATE})'
rd.cell(n, 2).value = ('NEW SHEETS (user request): stock-TN (TNs_, Mg N/ha) and stock-POXC (POXCs_, Mg C/ha) after stock-SOC (cumulative depth classes 0-10 ... 0-60 CM); '
                       'MACHINE FIELD CAPACITY (EFC_, ha/h effective field capacity of sowing machines, after NET ECONOMIC BENEFIT - not soil field capacity). '
                       '319 (641): Table 3 effective field capacity, HS = CA vs PSS / SS = MTR rows a / b. 321 (643): TN and POXC stocks 0-5 / 0-15 cm (Tables 4-7); '
                       'author-supplied SUPP DATA\\643.docx: Table S3 Karnal 5-15 cm cPOM-C / fPOM-C / MOC / PON (derived), Table S2 annual plant C input (C input sheet); '
                       'Tables S4-S5 (0-15 cm fraction totals) and S1 (residue C / N %) in notes.')
rd.cell(n, 3).value = 'Bibliography + 0. Next serial 323.'

# ---------------------------------------------------------------- index sheets (rebuilt in workbook order)
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
units = {sp.cell(r, 2).value: sp.cell(r, 3).value for r in range(4, sp.max_row + 1)}
units['stock-TN'] = 'Mg N/ha'; units['stock-POXC'] = 'Mg C/ha'; units['MACHINE FIELD CAPACITY'] = 'ha/h'
tpl = 5
for i, nme in enumerate(data_sheets):
    r = 4 + i
    for c in range(1, 7):
        s_, d_ = sp.cell(tpl, c), sp.cell(r, c)
        d_.font = copy.copy(s_.font); d_.alignment = copy.copy(s_.alignment); d_.border = copy.copy(s_.border); d_.fill = copy.copy(s_.fill)
    c = cnt[nme]
    vals = [i + 1, nme, units.get(nme), sum(c.values()), len(c), '; '.join(f'{k}: {v}' for k, v in c.items()) or 'NO DATA']
    for j, v in enumerate(vals, 1):
        sp.cell(r, j).value = v
ps = wb['PARAMETERS_BY_STUDY']
for r in range(4, ps.max_row + 1):
    s = str(ps.cell(r, 2).value)
    if s in ('319', '321'):
        parts = [(nme, cnt[nme][s]) for nme in data_sheets if s in cnt[nme]]
        ps.cell(r, 7).value = sum(v for _, v in parts); ps.cell(r, 8).value = len(parts)
        ps.cell(r, 9).value = '; '.join(f'{k}: {v}' for k, v in parts)
        for rr2 in range(2, si.max_row + 1):
            if str(si.cell(rr2, h['SERIAL NO']).value) == s:
                ps.cell(r, 10).value = si.cell(rr2, h['Parameters extracted']).value

# restore the orange unit note style in row 2 of the new sheets
for nm, (tpl_, _, keep_) in STYLE_SRC.items():
    ws = wb[nm]; t = wb['stock-SOC'] if nm == 'stock-POXC' else wb[tpl_]
    s2 = t.cell(2, t.max_column); d2 = ws.cell(2, len(keep_) if nm != 'stock-POXC' else len(STYLE_SRC['stock-TN'][2]))
    d2.font = copy.copy(s2.font); d2.fill = copy.copy(s2.fill); d2.alignment = copy.copy(s2.alignment); d2.border = copy.copy(s2.border)
wb.calculation.fullCalcOnLoad = True
wb.save(DST)
from collections import Counter
print('rows added per sheet:', dict(Counter(s for s, _ in B.log)))
