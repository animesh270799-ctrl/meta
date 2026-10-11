"""Study 331 - Sidhu H.S. et al. 2019 Agric. Water Manage. 216:273-283 (ext 671): sub-surface drip fertigation x CA, BISA Ladhowal."""
from common import base, notes

ST = dict(
    no=331, serial=331, authors='Sidhu H.S., Jat M.L., Singh Y., Sidhu R.K., Gupta N., Singh P., Singh P., Jat H.S. & Gerard B.', year=2019, journal='Agricultural Water Management',
    ref=('Sidhu H.S., Jat M.L., Singh Y., Sidhu R.K., Gupta N., Singh P., Singh P., Jat H.S. & Gerard B. (2019) Sub-surface drip fertigation with conservation agriculture in a rice-wheat system: '
         'a breakthrough for addressing water and nitrogen use efficiency. Agricultural Water Management 216:273-283, doi 10.1016/j.agwat.2019.02.019.'),
    doi='10.1016/j.agwat.2019.02.019',
    fert='Scented rice Pusa 1509 (DSR / PTR), wheat; 26 P + 25 K kg/ha; N: flood PTR 60 kg (rice) / 120 (wheat), flood ZT-DSR 75 (rice) / 120 (wheat), drip treatments 80 % of recommended (60 rice / 96 wheat incl. DAP N) by weekly fertigation',
    tmap=('RCB, 4 reps (70.5 m2 plots), BISA-CIMMYT Ladhowal, rice 2014 / 2015, wheat 2014-15 / 2015-16. T8 CTRW-R + FI (puddled transplanted rice + conventional wheat, residues removed, flood) -> CT ; '
          'T7 ZTRW + R + FI (zero-till DSR + ZT wheat, 25 % wheat stubble + 100 % rice residue, flood) -> CA (row a; rice N 75 vs 60 kg - FLAG) ; SUB-SURFACE DRIP rows (all ZT-DSR + ZT wheat, 80 % N): '
          'T2 ZTRW-R + SSDF 33.75 cm / 15 cm -> ZT vs T3 ZTRW + R same laterals -> CA (row b) ; T5 ZTRW-R + SSDF 67.5 cm / 15 cm -> ZT vs T6 ZTRW + R -> CA (row c). '
          'T1 (surface drip, CA) and T4 (SSDF 33.75 cm at 20 cm, CA) have no same-irrigation contrast -> Notes.'),
    details=('TREATMENTS IN PAPER: T1 ZTRW + R + SDF33.75; T2 ZTRW-R + SSDF33.75-15; T3 ZTRW + R + SSDF33.75-15; T4 ZTRW + R + SSDF33.75-20; T5 ZTRW-R + SSDF67.5-15; T6 ZTRW + R + SSDF67.5-15; '
             'T7 ZTRW + R + FI; T8 CTRW-R + FI (RCB, 4 reps). || MAPPING: T8 -> CT [rice: puddled TPR; wheat: conventional; residue: removed; flood] | T7 -> CA (row a) [rice: ZT DSR; wheat: ZT; residue: yes; flood] | '
             'T2 / T5 -> ZT (rows b / c) [ZT DSR + ZT wheat, residue removed, sub-surface drip] | T3 / T6 -> CA (rows b / c) [same with residue mulch] | T1, T4 -> Notes (no contrast)'),
)
SITE = dict(country='India (Punjab)', site='BISA-CIMMYT research farm, Ladhowal, Ludhiana', lat=30.99, lon=75.44, climate='ST', duration='0-3 Y', soil='LOAMY',
            CLAY=20.0, sand=34.0, silt=46.0, **{'RAIN FALL': 734, 'ph (initial)': 8.3, 'soc (initial)': 7.4, 'Bdi': 1.47})
ROWS = {'a': ('CT = T8 CTRW-R + FI, CA = T7 ZTRW + R + FI (flood irrigation; rice N 60 vs 75 kg/ha - FLAG)', {'CT': 7, 'CA': 6}),
        'b': ('ZT = T2 ZTRW-R, CA = T3 ZTRW + R (sub-surface drip, laterals 33.75 cm apart at 15 cm; 80 % N)', {'ZT': 1, 'CA': 2}),
        'c': ('ZT = T5 ZTRW-R, CA = T6 ZTRW + R (sub-surface drip, laterals 67.5 cm apart at 15 cm; 80 % N)', {'ZT': 4, 'CA': 5})}
# T1..T8
Y = {'R14': [4.62, 4.57, 4.59, 4.72, 5.15, 4.79, 4.88, 4.71], 'R15': [4.79, 4.66, 4.85, 4.57, 4.83, 4.70, 4.67, 4.40],
     'W1': [5.60, 5.14, 5.51, 5.32, 5.40, 5.56, 5.07, 4.74], 'W2': [5.72, 5.79, 5.70, 5.23, 5.69, 5.48, 5.29, 4.38]}
# Figs 6-7 irrigation water productivity (kg grain / m3 irrigation), DIGITISED; Figs 4-5 irrigation (mm), DIGITISED (T7 / T8 printed in text)
WP = {'R14': [0.783, 0.756, 0.789, 0.840, 0.799, 0.766, 0.457, 0.365], 'R15': [0.864, 0.776, 0.842, 0.815, 0.788, 0.811, 0.464, 0.398],
      'W1': [3.32, 2.62, 3.31, 3.16, 2.71, 3.38, 1.71, 1.56], 'W2': [3.84, 2.93, 3.78, 3.30, 3.02, 3.29, 1.32, 1.24]}
IRR = {'R14': [596, 609, 586, 566, 649, 630, 1072, 1296], 'R15': [556, 604, 579, 563, 617, 582, 1010, 1109],
       'W1': [170, 198, 168, 170, 201, 166, 298, 306], 'W2': [149, 199, 152, 160, 189, 168, 403, 356]}
PFP = {'R': [78.4, 77.0, 78.7, 77.5, 83.2, 79.1, 63.7, 75.9], 'W': [59.0, 56.9, 58.4, 55.0, 57.8, 57.5, 43.2, 38.0], 'S': [66.5, 64.7, 66.2, 63.6, 67.5, 65.8, 51.1, 50.7]}
NAP = ('rice 60 / wheat 96 / system 156', 'rice 75 / wheat 120 / system 195', 'rice 60 / wheat 120 / system 180')
ECO = {'CR': [28.52, 25.54, 26.29, 26.03, 24.67, 25.03, 30.02, 36.64], 'CW': [28.23, 25.48, 25.89, 25.95, 24.21, 24.73, 25.28, 28.52],
       'GR': [151.87, 148.85, 152.45, 149.68, 160.89, 153.02, 153.86, 146.91], 'GW': [106.31, 102.21, 104.17, 99.29, 104.06, 104.34, 96.33, 84.69],
       'NR': [123.35, 123.31, 125.86, 123.65, 136.22, 127.99, 123.84, 110.27], 'NW': [78.08, 76.74, 78.28, 73.34, 79.85, 79.61, 71.05, 56.17],
       'NS': [201.43, 200.05, 204.14, 196.99, 216.07, 207.60, 194.89, 166.44]}
M = 'Grain from 10 m2 net plot (rice 14 %, wheat 12 % moisture); irrigation metered (flow meter); WPi = grain / irrigation water; PFPN = grain / N applied; partial budget at PAU input prices and MSP.'


def rows(B):
    st = ST; out = []

    def add(sheet, vals, body, tag, unit, src, crop, yd, y=1):
        obs, nt = notes(st, f'ROW {tag}: {ROWS[tag][0]}. ' + body, y=y)
        v = base(st, SITE, {'year of data collection/experiment': yd, 'YEAR OF DATA (duration)': yd})
        v.update(vals)
        v.update({'UNIT': unit, 'Crop/season of sampling': crop, 'Data source': src, 'Method used (from paper)': M, 'Obs': obs, 'Rep': 4, 'Notes/Doubts': nt})
        out.append((sheet, B.add_row(sheet, v)))

    def cv(tag, pre, vals, fmt=None):
        return {f'{pre}{c}': (fmt.format(vals[i]) if fmt else vals[i]) for c, i in ROWS[tag][1].items()}

    T14 = ' T1 (surface drip) / T4 (laterals at 20 cm), CA only - Notes: '
    for tag in ROWS:
        for ry, wy, rk, wk, yd in (('2014', '2014-15', 'R14', 'W1', 'rice 2014, wheat 2014-15'), ('2015', '2015-16', 'R15', 'W2', 'rice 2015, wheat 2015-16')):
            add('YIELD', {**cv(tag, 'RICE YIELD_', Y[rk]), **cv(tag, 'WYIELD_', Y[wk])},
                f'Table 3 grain yield, rice {ry} (14 %) and wheat {wy} (12 %).' + T14 + f'rice {Y[rk][0]} / {Y[rk][3]}, wheat {Y[wk][0]} / {Y[wk][3]} t/ha.',
                tag, 't/ha', 'Table 3', f'Rice {ry}; wheat {wy}', yd)
            ir = IRR
            add('WUE', {**cv(tag, 'WUE_R', WP[rk], '=ROUND({}*10,2)'), **cv(tag, 'WUE_W', WP[wk], '=ROUND({}*10,2)')},
                f'Figures 6-7 IRRIGATION water productivity (kg grain / m3 irrigation, DIGITISED x 10 -> kg/ha/mm), rice {ry} and wheat {wy}. Irrigation applied (Figs 4-5, mm; T7 / T8 printed): '
                f'rice T1-T8 {" / ".join(map(str, ir[rk]))}; wheat {" / ".join(map(str, ir[wk]))}.', tag, 'kg/ha/mm (irrigation water basis; digitised kg/m3 x 10)', 'Figures 6-7 (digitised)',
                f'Rice {ry}; wheat {wy}', yd)
        add('NUE', {**cv(tag, 'NUE_R', PFP['R']), **cv(tag, 'NUE_W', PFP['W']), **cv(tag, 'NUE_SYS', PFP['S'])},
            f'Table 4 PARTIAL FACTOR PRODUCTIVITY of applied N (PFPN, kg grain / kg N), pooled 2 years. N applied: drip {NAP[0]}, T7 {NAP[1]}, T8 {NAP[2]} kg/ha (N rates differ - FLAG).',
            tag, 'kg grain/kg N applied (PFPN)', 'Table 4', 'Rice, wheat and system (2-yr pooled)', '2014-2016 (2-yr pooled)', y=2)
        e = ECO
        k = lambda key: cv(tag, '', e[key])
        add('COST OF CULTIVATION', {**{f'COST_R{c}': f'=ROUND({x}*1000,0)' for c, x in k('CR').items()}, **{f'COST_W{c}': f'=ROUND({x}*1000,0)' for c, x in k('CW').items()},
                                    **{f'COST_SYS{c}': f'=ROUND(({e["CR"][i]}+{e["CW"][i]})*1000,0)' for c, i in ROWS[tag][1].items()}},
            'Table 5 VARIABLE cost of cultivation (Rs x 10^3 x 1000), pooled 2 years, drip cost with 80 % subsidy; system = rice + wheat (DERIVED).', tag, 'Rs/ha (variable cost; drip 80 % subsidised)',
            'Table 5', 'Rice, wheat and system (2-yr pooled)', '2014-2016 (2-yr pooled)', y=2)
        add('GROSS RETURN', {**{f'GR_R{c}': f'=ROUND({x}*1000,0)' for c, x in k('GR').items()}, **{f'GR_W{c}': f'=ROUND({x}*1000,0)' for c, x in k('GW').items()},
                             **{f'GR_SYS{c}': f'=ROUND(({e["GR"][i]}+{e["GW"][i]})*1000,0)' for c, i in ROWS[tag][1].items()}},
            'Table 5 gross returns (MSP; wheat incl. straw), pooled 2 years; system DERIVED (rice + wheat).', tag, 'Rs/ha', 'Table 5', 'Rice, wheat and system (2-yr pooled)', '2014-2016 (2-yr pooled)', y=2)
        add('NET RETURN', {**{f'NR_R{c}': f'=ROUND({x}*1000,0)' for c, x in k('NR').items()}, **{f'NR_W{c}': f'=ROUND({x}*1000,0)' for c, x in k('NW').items()},
                           **{f'NR_SYS{c}': f'=ROUND({x}*1000,0)' for c, x in k('NS').items()}},
            'Table 5 net returns over variable cost, pooled 2 years.', tag, 'Rs/ha (over variable cost)', 'Table 5', 'Rice, wheat and system (2-yr pooled)', '2014-2016 (2-yr pooled)', y=2)
        add('BC ratio', {**{f'BC_R{c}': f'=ROUND({e["NR"][i]}/{e["CR"][i]},2)' for c, i in ROWS[tag][1].items()}, **{f'BC_W{c}': f'=ROUND({e["NW"][i]}/{e["CW"][i]},2)' for c, i in ROWS[tag][1].items()},
                         **{f'BC_SYS{c}': f'=ROUND({e["NS"][i]}/({e["CR"][i]}+{e["CW"][i]}),2)' for c, i in ROWS[tag][1].items()}},
            'B:C DERIVED = net return / variable cost (Table 5; text: SSDF 3.55-4.42 vs CT 2.55 - reproduced).', tag, 'ratio (net / variable cost; DERIVED)', 'Table 5 (DERIVED)',
            'Rice, wheat and system (2-yr pooled)', '2014-2016 (2-yr pooled)', y=2)
    return out


TM = [
    ('T8 CTRW-R + FI', 'Puddled transplanted rice (2 discings + tyne + wet tillage) + conventional wheat; residues removed; flood irrigation', 'Puddled TPR', 'Conventional', 'No', '0', 'CT', 'Conventional both phases.', 'High', 'INCLUDED'),
    ('T7 ZTRW + R + FI', 'ZT DSR (Turbo Happy Seeder) + ZT wheat; 25 % wheat stubble + 100 % rice residue; flood', 'Zero-till DSR', 'Zero tillage', 'Yes', '6.0-6.5 (rice)', 'CA (row a)', 'Rice N 75 vs 60 kg in T8 - FLAG.', 'High', 'INCLUDED'),
    ('T2 / T5 ZTRW-R + SSDF', 'ZT DSR + ZT wheat, residues removed, sub-surface drip 33.75 / 67.5 cm laterals at 15 cm, 80 % N', 'Zero-till DSR', 'Zero tillage', 'No', '0', 'ZT (rows b / c)', 'Same irrigation as the CA partner.', 'High', 'INCLUDED'),
    ('T3 / T6 ZTRW + R + SSDF', 'As T2 / T5 with residue mulch', 'Zero-till DSR', 'Zero tillage', 'Yes', '6.0-6.5 (rice)', 'CA (rows b / c)', 'Residue contrast within drip layout.', 'High', 'INCLUDED'),
    ('T1 ZTRW + R + SDF33.75 / T4 ZTRW + R + SSDF33.75-20', 'Surface drip / laterals at 20 cm, CA', 'Zero-till DSR', 'Zero tillage', 'Yes', None, 'Notes', 'No partner with the same irrigation layout.', 'High', 'NOTES ONLY'),
]
STUDY_INFO = dict(estab=2014, yeardata='Rice 2014, 2015; wheat 2014-15, 2015-16', years='2 (year-wise yields; pooled NUE / economics)', texture='Silt loam (34 % sand, 46 % silt, 20 % clay)',
                  rotation='Scented rice-wheat', wheatvar='Not reported', ricevar='Pusa 1509', N='Rice 60-75 / wheat 96-120 (see rows)', P='26 (P)', K='25 (K)',
                  residue='CA: 25 % wheat stubble (1.5-2 t/ha) + 100 % rice residue (6.0-6.5 t/ha); others removed',
                  irrigation='Flood (T7, T8) vs surface / sub-surface drip fertigation (laterals 33.75 / 67.5 cm, 0 / 15 / 20 cm deep); SMP-based scheduling',
                  treatments='8 tillage x residue x irrigation-layout combinations (RCB, 4 reps)', supp='None',
                  params=('Rows a (CT vs CA, flood), b / c (ZT vs CA within sub-surface drip): rice and wheat yield per year, irrigation WPi per year (Figs 6-7 digitised), PFPN rice / wheat / system, '
                          'variable cost, gross and net return, B:C (derived) - rice, wheat and system'),
                  notes=('NEW serial 331 (ext\\671.pdf). Possibly the same BISA Ladhowal drip platform as study 134 (Rana et al. 2023, rice 2019-20; different treatments / years) - FLAG. '
                         'Irrigation amounts (Figs 4-5, digitised; T7 / T8 printed: rice 1072 / 1296 mm 2014, 1010 / 1109 mm 2015; wheat 298 / 306, 403 / 356 mm) given in WUE notes - no irrigation sheet. '
                         'T1 / T4 (CA-only drip layouts) in notes. Cover crop of wheat 2013-14 before treatments.'))
SITES = [('BISA-CIMMYT farm, Ladhowal', '30.99 N', '75.44 E', 30.99, 75.44, 'Paper', 'ST', None)]
