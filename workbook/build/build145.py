"""Post-step of updated 145: RULES row 143 (author decisions 2026-10-11) and STUDIES_BY_PARAMETER rebuilt in workbook order (new sheets ACTIVE / PASSIVE C POOL)."""
import copy
import sys
sys.path.insert(0, sys.path[0])
from wblib import WB
SRC, DST = sys.argv[1], sys.argv[2]
B = WB(SRC); wb = B.wb
ws = wb['RULES']
r = ws.max_row
while ws.cell(r, 1).value is None:
    r -= 1
n = r + 1
for c in range(1, 7):
    s, d = ws.cell(r, c), ws.cell(n, c)
    d.font = copy.copy(s.font); d.alignment = copy.copy(s.alignment); d.fill = copy.copy(s.fill); d.border = copy.copy(s.border)
vals = [143, 'Treatment codes / parameter-specific',
        ('AUTHOR DECISIONS 2026-10-11: (1) FIRBS / raised-bed planting of wheat (furrow-irrigated raised beds, even when the beds are formed after conventional seedbed preparation) is minimum / reduced '
         'tillage -> MT (applied to 330 (ext 668) FIRBS and 328 (ext 653) bed planting, previously excluded). (2) Properties measured WITHIN aggregate fractions are also entered at BULK-SOIL level: '
         'mass-weighted mean of the macro- and micro-aggregate values, weights = the paper\'s water-stable macro- / micro-aggregate proportions (applied to 1 (companion 5), ext 670: Chan fractions, TOC, '
         'DHA, cellulase, beta-glucosidase, Alk-P, EEG / TG glomalin). (3) New sheets ACTIVE C POOL (Chan Fract. 1 + 2) and PASSIVE C POOL (Fract. 3 + 4).'),
        'Bulk estimate assumes the unaggregated <0.053 mm fraction has the weighted-mean concentration (FLAG on each row). Earlier entries are not changed unless the author asks.',
        'Author 2026-10-11', 'IN FORCE (author)']
for c, v in enumerate(vals, 1):
    ws.cell(n, c).value = v
names = wb.sheetnames
data_sheets = names[names.index('LAT_LONG'):names.index('EXCLUDED_rows')]
cnt = {}
for nme in data_sheets:
    w = wb[nme]; bc = B.hdr(nme)['SERIAL NO']; c = {}
    for rr in range(2, w.max_row + 1):
        val = w.cell(rr, bc).value
        if val is None:
            continue
        k = str(val).strip(); c[k] = c.get(k, 0) + 1
    cnt[nme] = c
sp = wb['STUDIES_BY_PARAMETER']
units = {sp.cell(rr, 2).value: sp.cell(rr, 3).value for rr in range(4, sp.max_row + 1)}
units.update({'ACTIVE C POOL': 'g/kg', 'PASSIVE C POOL': 'g/kg'})
for i, nme in enumerate(data_sheets):
    rr = 4 + i
    for c in range(1, 7):
        s_, d_ = sp.cell(5, c), sp.cell(rr, c)
        d_.font = copy.copy(s_.font); d_.alignment = copy.copy(s_.alignment); d_.border = copy.copy(s_.border); d_.fill = copy.copy(s_.fill)
    c = cnt[nme]
    for j, v in enumerate([i + 1, nme, units.get(nme), sum(c.values()), len(c), '; '.join(f'{k}: {v}' for k, v in c.items()) or 'NO DATA'], 1):
        sp.cell(rr, j).value = v
# PARAMETERS_BY_STUDY: refresh every row (counts change for recoded / extended studies)
si = wb['Study_Info']; hs = B.hdr('Study_Info')
params = {str(si.cell(rr, hs['SERIAL NO']).value): si.cell(rr, hs['Parameters extracted']).value for rr in range(2, si.max_row + 1)}
ps = wb['PARAMETERS_BY_STUDY']
for rr in range(4, ps.max_row + 1):
    s = ps.cell(rr, 2).value
    if s is None:
        continue
    s = str(s).strip()
    parts = [(nme, cnt[nme][s]) for nme in data_sheets if s in cnt[nme]]
    if not parts:
        continue
    ps.cell(rr, 7).value = sum(v for _, v in parts); ps.cell(rr, 8).value = len(parts)
    ps.cell(rr, 9).value = '; '.join(f'{k}: {v}' for k, v in parts)
    if s in ('326', '328', '329', '330', '1 (companion 5)') and params.get(s):
        ps.cell(rr, 10).value = params[s]
wb.calculation.fullCalcOnLoad = True
wb.save(DST)
print('RULES row', n, '; SP rows', len(data_sheets))
