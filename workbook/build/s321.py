"""Study 321 - Mishra A.K. et al. 2024 Front. Sustain. Food Syst. 8:1476292 (ext 643): CA at Karnal + Samastipur."""
from common import base, notes

ST = dict(
    no=321, serial=321,
    authors='Mishra A.K., Shinjo H., Jat H.S., Jat M.L., Jat R.K. & Funakawa S.',
    year=2024, journal='Frontiers in Sustainable Food Systems',
    ref=('Mishra A.K., Shinjo H., Jat H.S., Jat M.L., Jat R.K. & Funakawa S. (2024) Conservation agriculture enhances crop productivity '
         'and soil carbon fractions in Indo-Gangetic Plains of India. Frontiers in Sustainable Food Systems 8:1476292, doi 10.3389/fsufs.2024.1476292.'),
    doi='10.3389/fsufs.2024.1476292',
    tmap=('RBD, 3 reps, 350 m2 plots. KARNAL (Taraori, est. June 2012): K1 CTRW-R (puddled TPR: 3 harrow passes + 2 puddling passes + planking; wheat 1 rotavator pass + broadcast; 95 % residue removed) -> CT (single rotavator pass, depth not stated - rule 13 grey zone, kept CT as the paper, FLAG) ; '
          'K2 CTRW+R+MB (same tillage, rice residue 100 % / wheat 50 % / mungbean 100 % retained, ZT mungbean) -> CTR (mungbean in residue treatments only - rule 71, FLAG) ; '
          'K3 ZTRW-R (ZT DSR + ZT wheat with Turbo Happy Seeder, residue removed) -> ZT ; K4 ZTRW+R+MB -> CA (+ mungbean, rule 71) ; K5 PBMW-R and K6 PBMW+R+MB (permanent-bed maize-wheat) -> EXCLUDED (maize-wheat, rule 31). '
          'SAMASTIPUR (BISA farm, est. Nov 2012): S1 CTRW-R -> CT ; S2 ZTRW+R+MB -> CA ; S3 PBMW+R+MB, S4 PBMM+R+MB -> EXCLUDED (maize systems).'),
    details=('TREATMENTS IN PAPER: Karnal K1 CTRW-R, K2 CTRW+R+MB, K3 ZTRW-R, K4 ZTRW+R+MB, K5 PBMW-R, K6 PBMW+R+MB; Samastipur S1 CTRW-R, S2 ZTRW+R+MB, S3 PBMW+R+MB, S4 PBMM+R+MB (RBD, 3 reps, 350 m2). || MAPPING: '
             'K1 / S1 -> CT: puddled transplanted rice (harrow x 3, puddling x 2, planking; 15 x 20 cm), wheat after one rotavator pass, manual broadcast; 95 % residue removed [rice phase: puddled conventional; wheat phase: conventional (1 rotavator pass - FLAG); residue: No] | '
             'K2 -> CTR: as K1 + ZT mungbean, residue retained (rice 100 %, wheat 50 %, mungbean 100 %) [rice phase: puddled conventional; wheat phase: conventional; residue: Yes] | '
             'K3 -> ZT: ZT DSR + ZT wheat (Turbo Happy Seeder, 20 cm rows), 95 % residue removed [rice phase: zero-till DSR; wheat phase: zero tillage; residue: No] | '
             'K4 / S2 -> CA: ZT DSR + ZT wheat + ZT mungbean (multi-crop planter), residue retained (rice 100 %, wheat 50 % at Karnal / 100 % at Samastipur, mungbean 100 %) [rice phase: zero-till DSR; wheat phase: zero tillage; residue: Yes] | '
             'K5, K6, S3, S4 -> EXCLUDED: permanent raised beds with maize-wheat(-mungbean) or maize-mustard-mungbean - not rice-wheat (rule 31)'),
)
SK = dict(country='India (Haryana)', site='Farmer-participatory CA trial, Taraori, Karnal (CCAFS climate-smart village)',
          lat=29.8, lon=76.917, climate='ST', soil='LOAMY', **{'RAIN FALL': 670, 'AVG T': 24},
          fert='Recommended practices (doses not stated); rice / wheat / mungbean residue as per treatment; trial est. June 2012')
SS = dict(country='India (Bihar)', site='Borlaug Institute for South Asia (BISA) farm, Pusa, Samastipur',
          lat=25.95, lon=85.667, climate='ST', soil='LOAMY', **{'RAIN FALL': 1200, 'AVG T': 25.5},
          fert='Recommended practices (doses not stated); residue as per treatment; trial est. Nov 2012')
KC = ['CT', 'CTR', 'ZT', 'CA']   # K1 K2 K3 K4
SC = ['CT', 'CA']                # S1 S2

# TOC g/kg, TOC stock, TN g/kg, TN stock   (Tables 4-5)
T45 = {
    ('K', 2015, '0-5'): [(8.29, 6.66, 0.91, 0.73), (8.28, 6.64, 0.95, 0.76), (7.99, 6.16, 0.96, 0.74), (9.67, 10.8, 1.05, 0.82)],
    ('K', 2015, '5-15'): [(6.26, 10.6, 0.69, 1.17), (6.27, 10.6, 0.73, 1.23), (6.75, 11.2, 0.78, 1.28), (7.35, 12.2, 0.87, 1.44)],
    ('K', 2015, '0-15'): [(6.94, 17.3, 0.76, 1.90), (6.94, 17.2, 0.80, 1.99), (7.16, 17.4, 0.84, 2.02), (9.53, 23.0, 0.93, 2.26)],
    ('K', 2017, '0-5'): [(9.55, 7.66, 1.50, 1.21), (12.1, 9.67, 1.93, 1.55), (14.6, 11.2, 1.90, 1.49), (14.8, 11.6, 2.18, 1.68)],
    ('K', 2017, '5-15'): [(6.61, 11.2, 1.30, 2.19), (8.33, 14.2, 1.67, 2.84), (7.15, 11.9, 1.31, 2.17), (8.50, 14.1, 1.62, 2.69)],
    ('K', 2017, '0-15'): [(7.59, 18.9, 1.37, 3.40), (9.57, 23.8, 1.76, 4.39), (9.63, 23.1, 1.51, 3.66), (10.6, 25.7, 1.81, 4.37)],
    ('S', 2016, '0-5'): [(7.59, 6.78, 0.50, 0.44), (9.59, 8.38, 0.99, 0.87)],
    ('S', 2016, '5-15'): [(4.85, 8.38, 0.40, 0.69), (4.79, 8.05, 0.29, 0.48)],
    ('S', 2016, '0-15'): [(5.76, 15.2, 0.43, 1.13), (6.39, 16.4, 0.52, 1.35)],
    ('S', 2018, '0-5'): [(8.35, 7.45, 1.17, 0.91), (13.3, 11.6, 1.63, 1.46)],
    ('S', 2018, '5-15'): [(6.57, 11.4, 1.68, 2.90), (7.77, 13.0, 1.87, 3.14)],
    ('S', 2018, '0-15'): [(7.16, 18.9, 1.51, 3.81), (9.61, 24.6, 1.79, 4.60)],
}
# POXC mg/kg, POXC stock (Tables 6-7)
T67 = {
    ('K', 2015, '0-5'): [(325.2, 0.26), (340.5, 0.27), (387.8, 0.30), (416.2, 0.33)],
    ('K', 2015, '5-15'): [(321.9, 0.55), (331.9, 0.56), (322.1, 0.53), (343.3, 0.57)],
    ('K', 2015, '0-15'): [(323.0, 0.81), (334.7, 0.84), (344.0, 0.83), (367.6, 0.89)],
    ('K', 2017, '0-5'): [(331.6, 0.27), (378.2, 0.30), (400.7, 0.31), (478.0, 0.37)],
    ('K', 2017, '5-15'): [(299.2, 0.51), (346.6, 0.59), (264.9, 0.44), (391.5, 0.65)],
    ('K', 2017, '0-15'): [(310.0, 0.77), (357.2, 0.89), (310.2, 0.75), (420.3, 1.02)],
    ('S', 2016, '0-5'): [(153.4, 0.14), (209.5, 0.18)],
    ('S', 2016, '5-15'): [(146.8, 0.25), (192.7, 0.32)],
    ('S', 2016, '0-15'): [(149.0, 0.39), (198.2, 0.51)],
    ('S', 2018, '0-5'): [(175.8, 0.16), (351.0, 0.31)],
    ('S', 2018, '5-15'): [(157.8, 0.27), (249.9, 0.42)],
    ('S', 2018, '0-15'): [(163.8, 0.43), (283.6, 0.73)],
}
# POM fractions: mass % (c, f, OMF), TOC stock (c, f, OMF), TN stock (c, f, OMF)  (Tables 8-9)
T89 = {
    ('K', 2015, '0-5'): [((2.36, 40.5, 57.1), (0.60, 1.04, 3.28), (0.05, 0.40, 0.84)), ((2.74, 40.8, 56.5), (0.81, 1.16, 3.18), (0.07, 0.40, 0.76)),
                         ((2.65, 37.4, 60.0), (0.79, 1.21, 3.22), (0.06, 0.36, 0.63)), ((4.22, 42.4, 53.4), (1.45, 1.41, 3.08), (0.09, 0.35, 0.58))],
    ('K', 2017, '0-5'): [((2.36, 40.4, 57.3), (0.56, 0.53, 2.96), (0.04, 0.21, 0.32)), ((4.01, 39.5, 56.5), (1.33, 1.52, 3.30), (0.09, 0.22, 0.54)),
                         ((5.27, 37.0, 57.7), (1.71, 2.24, 3.57), (0.17, 0.24, 0.39)), ((9.21, 34.5, 56.3), (3.42, 1.29, 5.25), (0.37, 0.21, 0.73))],
    ('S', 2016, '0-5'): [((1.89, 23.6, 74.5), (0.71, 1.22, 2.56), (0.05, 0.15, 0.55)), ((6.02, 12.2, 81.8), (3.23, 1.74, 3.14), (0.16, 0.13, 0.91))],
    ('S', 2018, '0-5'): [((5.70, 24.0, 70.3), (1.56, 1.18, 1.93), (0.03, 0.30, 0.39)), ((10.0, 31.3, 58.7), (5.62, 2.12, 3.58), (0.26, 0.38, 0.76))],
    ('S', 2016, '5-15'): [((2.05, 23.6, 74.4), (0.85, 1.83, 3.13), (0.04, 0.31, 1.50)), ((2.71, 10.2, 87.5), (1.34, 1.16, 5.07), (0.05, 0.22, 1.85))],
    ('S', 2018, '5-15'): [((2.63, 21.8, 75.6), (1.88, 1.60, 2.21), (0.03, 0.82, 0.93)), ((3.16, 21.3, 75.6), (1.80, 2.89, 6.69), (0.19, 0.40, 1.80))],
}
YRS = {('K', 2015): (3, '0-3 Y'), ('K', 2017): (5, '4-10 Y'), ('S', 2016): (3, '0-3 Y'), ('S', 2018): (5, '4-10 Y')}
THICK = {'0-5': 5, '5-15': 10}
TABLES = {'K': ('Table 4', 'Table 6', 'Table 8'), 'S': ('Table 5', 'Table 7', 'Table 9')}
K4_FLAG = ('K4 (CA) 2015 0-5 cm TOC stock printed 10.8 Mg/ha implies BD 2.23 Mg/m3 (and the 0-15 cm TOC 9.53 g/kg does not equal the depth-weighted '
           '0-5 / 5-15 values, 8.12) - probable misprint; stock kept as printed (FLAG), derived BD / fraction concentrations for this cell left blank.')

M_TOC = 'TOC by improved chromic acid digestion (Tyurin 1966) on <2 mm soil; composite of 5 auger cores (5 cm dia.) per plot, 0-5 and 5-15 cm.'
M_TN = 'Total N by NC analyser (dry combustion, Vario Max CHN) - stated for fractions; bulk-soil TN method assumed the same (verify).'
M_POXC = 'POXC: 2.5 g soil + 20 mL 0.02 M KMnO4, shaken 2 min, settled 10 min, 1:50 dilution, absorbance 550 nm (Weil et al. 2003; Culman et al. 2012).'
M_POM = ('Physical fractionation: 20 g soil + 5 glass beads + 50 mL water shaken 16 h, wet-sieved into cPOM (2000-250 um), fPOM (250-53 um), OMF (<53 um); '
         'C in cPOM by NC analyser, fPOM and OMF by Tyurin; fraction stocks = SM x C % x mass %.')
M_BD = 'Core sampler (5 cm height x 5 cm dia.; Blake & Hartge 1986) - values not printed; DERIVED here from TOC stock / (TOC x thickness x 0.1).'


def site_of(s):
    return SK if s == 'K' else SS


def codes_of(s):
    return KC if s == 'K' else SC


def rows(B):
    st = ST
    out = []
    ref = {}   # (sheet, s, yr, layer) -> row

    def add(sheet, s, yr, vals, body, y=1, t=1, d=1, key=None):
        site = site_of(s)
        n, dur = YRS[(s, yr)]
        obs, nt = notes(st, body, y, t, d)
        v = base(st, site, {'DURATION': dur, 'year of data collection/experiment': yr,
                            'YEAR OF DATA (duration)': f'{n} yr (sampled {yr})'})
        v.update(vals)
        v.update({'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
        r = B.add_row(sheet, v)
        out.append((sheet, r))
        if key:
            ref[(sheet,) + key] = r
        return r

    def head(s, yr):
        n, _ = YRS[(s, yr)]
        if s == 'K':
            return (f'KARNAL {yr} ({n} yr after start): CT = K1, CTR = K2, ZT = K3, CA = K4; K5 / K6 (maize-wheat beds) excluded. '
                    'K1 wheat tillage = 1 rotavator pass (depth not stated) kept CT - FLAG; mungbean only in K2 / K4 (rule 71) - FLAG. '
                    'Sampling season not stated (assumed after wheat).')
        return (f'SAMASTIPUR {yr} ({n} yr after start): CT = S1, CA = S2 (ZT DSR + ZT wheat + ZT mungbean, residue retained; mungbean only in CA, rule 71 - FLAG); '
                'S3 / S4 (maize systems) excluded. Sampling season not stated (assumed after wheat).')

    def cvals(prefix, s, nums):
        return {f'{prefix}_{c}': x for c, x in zip(codes_of(s), nums) if x is not None}

    layers = [(s, yr, ly) for (s, yr, ly) in T45 if ly != '0-15']
    # ---- TOC, total N, POXC, BD, porosity per layer
    for s, yr, ly in layers:
        tab4, tab6, _ = TABLES[s]
        rws = T45[(s, yr, ly)]
        dd = {'DEPTH': '0-15 CM', 'DEPTH (as reported in paper)': f'{ly} cm', 'Crop/season of sampling': f'Soil {yr}, {YRS[(s, yr)][0]} yr after start (season not stated)'}
        w15 = T45[(s, yr, '0-15')]
        add('TOC', s, yr, dict(dd, **cvals('TOC', s, [r[0] for r in rws]), UNIT='g/kg (TOC, Tyurin chromic acid digestion)',
                               **{'Data source': tab4, 'Method used (from paper)': M_TOC}),
            head(s, yr) + f' {tab4} TOC {ly} cm. Paper 0-15 cm depth-weighted TOC (Eq. 3): ' + ', '.join(f'{c} {r[0]}' for c, r in zip(codes_of(s), w15)) +
            ' g/kg - not entered (layers entered).' + (' ' + K4_FLAG if (s, yr, ly) == ('K', 2015, '0-5') else ''), d=2, key=(s, yr, ly))
        add('total N', s, yr, dict(dd, **cvals('TN', s, [f'=ROUND({r[2]}*1000,0)' for r in rws]), UNIT='mg/kg (printed g/kg x 1000)',
                                   **{'Data source': tab4, 'Method used (from paper)': M_TN}),
            head(s, yr) + f' {tab4} total N {ly} cm (printed g/kg). TN stocks (Mg/ha): ' + ', '.join(f'{c} {r[3]}' for c, r in zip(codes_of(s), rws)) +
            '; 0-15 cm TN ' + ', '.join(f'{c} {r[2]}' for c, r in zip(codes_of(s), w15)) + ' g/kg / stock ' + ', '.join(f'{r[3]}' for r in w15) + ' Mg/ha - no sheet.', d=2, key=(s, yr, ly))
        px = T67[(s, yr, ly)]
        px15 = T67[(s, yr, '0-15')]
        add('POXC(KMnO4-C)', s, yr, dict(dd, **cvals('POXC', s, [p[0] for p in px]), UNIT='mg/kg',
                                         **{'Data source': tab6, 'Method used (from paper)': M_POXC}),
            head(s, yr) + f' {tab6} POXC {ly} cm. POXC stocks (Mg/ha): ' + ', '.join(f'{c} {p[1]}' for c, p in zip(codes_of(s), px)) +
            '; 0-15 cm POXC ' + ', '.join(f'{c} {p[0]}' for c, p in zip(codes_of(s), px15)) + ' mg/kg (stock ' + ', '.join(f'{p[1]}' for p in px15) + ') - not entered (no stock sheet / layers entered).',
            d=2, key=(s, yr, ly))
        th = THICK[ly]
        bd = []
        for i, r in enumerate(rws):
            if (s, yr, ly) == ('K', 2015, '0-5') and i == 3:
                bd.append(None)
            else:
                bd.append(f'=ROUND({r[1]}/({r[0]}*{th}*0.1),2)')
        rb = add('BD', s, yr, dict(dd, **cvals('BD', s, bd), UNIT='Mg/m3 (DERIVED = TOC stock / (TOC x thickness x 0.1))',
                                   **{'Data source': f'{tab4} (DERIVED)', 'Method used (from paper)': M_BD}),
                 head(s, yr) + f' BD measured (core) but NOT printed; DERIVED from the printed TOC concentration and stock of the same layer ({ly} cm; paper: soil mass = BD x 500 (0-5) or x 1000 (5-15)). FLAG.' +
                 (' ' + K4_FLAG if (s, yr, ly) == ('K', 2015, '0-5') else ''), d=2, key=(s, yr, ly))
        bdc = {c: B.letter('BD', f'BD_{c}') for c in codes_of(s)}
        por = {f'POROSITY_{c}': f'=ROUND((1-BD!{bdc[c]}{rb}/2.65)*100,2)' for c, x in zip(codes_of(s), bd) if x is not None}
        add('POROSITY', s, yr, dict(dd, **por, UNIT='% v/v (DERIVED; PD 2.65 Mg/m3 default - paper gives no PD; BD itself derived)',
                                    **{'Data source': f'BD sheet row {rb} (DERIVED)', 'Method used (from paper)': 'Porosity = (1 - BD / 2.65) x 100 (FORMULAS sheet; rule 131), live link to the derived BD row.'}),
            head(s, yr) + f' Total porosity DERIVED from the DERIVED BD (BD sheet row {rb}) with PD = 2.65 (no PD in paper). FLAG.', d=2, key=(s, yr, ly))

    # ---- C lability indices (Blair) from POXC and TOC of the same layer, CT reference
    for s, yr, ly in layers:
        rt = ref[('TOC', s, yr, ly)]; rp = ref[('POXC(KMnO4-C)', s, yr, ly)]
        L = {c: (B.letter('TOC', f'TOC_{c}'), B.letter('POXC(KMnO4-C)', f'POXC_{c}')) for c in codes_of(s)}

        def cl(c):
            lt, lp = L[c]
            return f"('POXC(KMnO4-C)'!{lp}{rp}/(TOC!{lt}{rt}*1000-'POXC(KMnO4-C)'!{lp}{rp}))"
        dd = {'DEPTH': '0-15 CM', 'DEPTH (as reported in paper)': f'{ly} cm', 'Crop/season of sampling': f'Soil {yr}, {YRS[(s, yr)][0]} yr after start (season not stated)'}
        src = f'TOC row {rt}, POXC row {rp} (DERIVED)'
        mth = 'Blair et al. (1995): CL = POXC / (TOC x 1000 - POXC); LI = CL / CL_CT; CPI = TOC / TOC_CT; CMI = CPI x LI x 100 (FORMULAS sheet); live links to the TOC and POXC rows.'
        body = head(s, yr) + f' DERIVED (Blair 1995) from POXC and TOC of the same layer ({ly} cm), CT (K1 / S1) as reference; TOC (Tyurin) used as total C (FLAG).'
        add('C liability', s, yr, dict(dd, **{f'CL_{c}': f'=ROUND({cl(c)},4)' for c in codes_of(s)}, UNIT='ratio (carbon lability, Blair; DERIVED)',
                                       **{'Data source': src, 'Method used (from paper)': mth}), body, d=2)
        add('LI', s, yr, dict(dd, **{f'LI_{c}': (f'=ROUND({cl(c)}/{cl("CT")},3)' if c != 'CT' else '=1') for c in codes_of(s)},
                              UNIT='index (lability index; reference CT; DERIVED)', **{'Data source': src, 'Method used (from paper)': mth}), body, d=2)
        add('CPI', s, yr, dict(dd, **{f'CPI_{c}': (f'=ROUND(TOC!{L[c][0]}{rt}/TOC!{L["CT"][0]}{rt},3)' if c != 'CT' else '=1') for c in codes_of(s)},
                               UNIT='index (carbon pool index; reference CT; DERIVED)', **{'Data source': src, 'Method used (from paper)': mth}), body, d=2)
        add('CMI', s, yr, dict(dd, **{f'CMI_{c}': (f'=ROUND(TOC!{L[c][0]}{rt}/TOC!{L["CT"][0]}{rt}*{cl(c)}/{cl("CT")}*100,2)' if c != 'CT' else '=100') for c in codes_of(s)},
                               UNIT='index (carbon management index; reference CT = 100; DERIVED)', **{'Data source': src, 'Method used (from paper)': mth}), body, d=2)

    # ---- SOC (TOC) stocks: 0-5 cm -> 0-10 CM class, 0-15 cm -> 0-20 CM class (cumulative)
    for (s, yr, ly), rws in T45.items():
        if ly == '5-15':
            continue
        cls = '0-10 CM' if ly == '0-5' else '0-20 CM'
        tab4 = TABLES[s][0]
        add('stock-SOC', s, yr, {'DEPTH': cls, 'DEPTH (as reported in paper)': f'{ly} cm', **cvals('SOCs', s, [r[1] for r in rws]),
                                 'UNIT': 'Mg C/ha (TOC stock as printed; Tyurin TOC x soil mass)',
                                 'Crop/season of sampling': f'Soil {yr}, {YRS[(s, yr)][0]} yr after start (season not stated)',
                                 'Data source': tab4, 'Method used (from paper)': 'Stock = soil mass (BD x 500 for 0-5 cm, x 1000 for 5-15 cm) x TOC; 0-15 cm = sum of layers (Eqs. 3-5).'},
            head(s, yr) + f' {tab4} TOC stock {ly} cm (printed). 5-15 cm layer stocks: ' +
            ', '.join(f'{c} {r[1]}' for c, r in zip(codes_of(s), T45[(s, yr, "5-15")])) + ' Mg/ha (in 0-15 cm sum).' +
            (' ' + K4_FLAG if (s == 'K' and yr == 2015) else ''))

    # ---- POM fractions (concentrations DERIVED per kg bulk soil)
    for (s, yr, ly), fr in T89.items():
        tab4, _, tab8 = TABLES[s]
        rws = T45[(s, yr, ly)]
        dd = {'DEPTH': '0-15 CM', 'DEPTH (as reported in paper)': f'{ly} cm', 'Crop/season of sampling': f'Soil {yr}, {YRS[(s, yr)][0]} yr after start (season not stated)'}

        def conc(i, j, scale=1, nd=3):
            vals = []
            for k, (r, f) in enumerate(zip(rws, fr)):
                if (s, yr, ly) == ('K', 2015, '0-5') and k == 3:
                    vals.append(None)
                    continue
                vals.append(f'=ROUND({f[i][j]}*{r[0]}/{r[1]}{"*" + str(scale) if scale != 1 else ""},{nd})')
            return vals
        mass = '; '.join(f'{c} {f[0][0]} / {f[0][1]} / {f[0][2]}' for c, f in zip(codes_of(s), fr))
        cst = '; '.join(f'{c} {f[1][0]} / {f[1][1]} / {f[1][2]}' for c, f in zip(codes_of(s), fr))
        nst = '; '.join(f'{c} {f[2][0]} / {f[2][1]} / {f[2][2]}' for c, f in zip(codes_of(s), fr))
        common = (head(s, yr) + f' {tab8} {ly} cm. Fraction concentrations per kg BULK soil DERIVED = fraction stock (Mg/ha) x TOC (g/kg) / TOC stock (Mg/ha) of the same layer '
                  f'(soil mass from the paper\'s own stock equation) - FLAG. Printed: mass % cPOM / fPOM / OMF {mass}; C stock (Mg C/ha) {cst}; N stock (Mg N/ha) {nst}. '
                  'Sum of fraction C stocks differs from the bulk TOC stock (different methods). ' + (K4_FLAG + ' ' if (s, yr, ly) == ('K', 2015, '0-5') else '') +
                  ('Karnal 5-15 cm fractions are in Supplementary Table S4 (not downloaded). ' if s == 'K' else ''))
        src = f'{tab8} + {tab4} (DERIVED)'
        add('cPOM-C', s, yr, dict(dd, **cvals('cPOMC', s, conc(1, 0)), UNIT='g/kg bulk soil (cPOM 2000-250 um C; DERIVED)', **{'Data source': src, 'Method used (from paper)': M_POM}), common, d=2)
        add('fPOM-C', s, yr, dict(dd, **cvals('fPOMC', s, conc(1, 1)), UNIT='g/kg bulk soil (fPOM 250-53 um C; DERIVED)', **{'Data source': src, 'Method used (from paper)': M_POM}), common, d=2)
        add('MOC', s, yr, dict(dd, **cvals('MOC', s, conc(1, 2)), UNIT='g/kg bulk soil (organo-mineral fraction <53 um C, Tyurin; DERIVED)', **{'Data source': src, 'Method used (from paper)': M_POM}), common, d=2)
        pon = []
        for k, (r, f) in enumerate(zip(rws, fr)):
            if (s, yr, ly) == ('K', 2015, '0-5') and k == 3:
                pon.append(None)
            else:
                pon.append(f'=ROUND(({f[2][0]}+{f[2][1]})*{r[0]}/{r[1]}*1000,0)')
        add('PON', s, yr, dict(dd, **cvals('PON', s, pon), UNIT='mg/kg bulk soil (PON = cPOM-N + fPOM-N, 2000-53 um; DERIVED)', **{'Data source': src, 'Method used (from paper)': M_POM}),
            common + ' PON = (cPOM N + fPOM N stock) / soil mass.', d=2)

    # ---- yields (Table 3, 5-yr means) and legume yield
    yk = [(6.71, 4.98, 11.9), (6.78, 5.05, 12.8), (6.69, 5.66, 12.5), (6.76, 5.72, 13.6)]
    ys = [(7.24, 4.91, 12.2), (7.55, 5.65, 15.0)]
    for s, data, per in (('K', yk, '2012-13 to 2016-17'), ('S', ys, '2013 to 2017-18 (5 yr from Nov 2012 start; years not listed)')):
        site = site_of(s)
        v = base(st, site, {'DURATION': '4-10 Y', 'year of data collection/experiment': per, 'YEAR OF DATA (duration)': f'5-yr mean ({per})'})
        for c, (ri, wh, sy) in zip(codes_of(s), data):
            v[f'RICE YIELD_{c}'] = ri; v[f'WYIELD_{c}'] = wh; v[f'SYS YIELD_{c}'] = sy
        obs, nt = notes(st, head(s, 2017 if s == 'K' else 2018).split(':', 1)[1].strip() +
                        ' Table 3: 5-YEAR MEAN rice, wheat and system yield (system = rice-equivalent yield incl. mungbean in residue treatments - SYS FLAG, rule 54). '
                        + ('Mungbean (third crop) yield on LEGUME YIELD sheet.' if s == 'K' else 'Mungbean in CA only (0.37 t/ha) - notes (one code).'), y=5)
        v.update({'UNIT': 't/ha (Mg/ha; 12-14 % moisture)', 'Crop/season of sampling': f'Rice and wheat, 5-yr mean ({per})', 'Data source': 'Table 3',
                  'Method used (from paper)': 'Combine-harvested; yield from 3 quadrats of 4 x 2.7 m per plot at 12-14 % moisture; REY = sum(yield x MSP / MSP rice).',
                  'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
        out.append(('YIELD', B.add_row('YIELD', v)))
    v = base(st, SK, {'DURATION': '4-10 Y', 'year of data collection/experiment': '2012-13 to 2016-17', 'YEAR OF DATA (duration)': '5-yr mean (2012-17)'})
    obs, nt = notes(st, 'KARNAL: CTR = K2 (CT rice-wheat-mungbean, residue retained), CA = K4 (ZT rice-wheat-mungbean). Table 3 mungbean grain yield, 5-yr mean; mungbean grown only in residue treatments (rule 71). Samastipur CA (S2) 0.37 t/ha - one code, notes only.', y=5)
    v.update({'LEGY_CTR': 0.26, 'LEGY_CA': 0.31, 'UNIT': 't/ha mungbean grain (pods hand-picked, biomass retained)', 'Crop/season of sampling': 'Mungbean (summer), 5-yr mean',
              'Data source': 'Table 3', 'Method used (from paper)': 'Mungbean pods picked manually; biomass retained in plots.', 'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
    out.append(('LEGUME YIELD', B.add_row('LEGUME YIELD', v)))
    return out


TM = [
    ('K1 CTRW-R', 'Karnal: puddled transplanted rice (harrow x 3, puddling x 2, planking) - wheat after one rotavator pass, manual broadcast; 95 % residue removed.',
     'Puddled transplanted (conventional)', 'Conventional (1 rotavator pass - depth not stated)', 'No (95 % removed)', '0', 'CT',
     'Conventional in both phases; single rotavator pass of unstated depth kept CT as the paper (rule 13 grey zone - FLAG).', 'Medium', 'INCLUDED'),
    ('K2 CTRW+R+MB', 'Karnal: as K1 + zero-till mungbean; residue retained (rice 100 %, wheat 50 %, mungbean 100 %).',
     'Puddled transplanted (conventional)', 'Conventional (1 rotavator pass)', 'Yes', 'rice 100 %, wheat 50 %', 'CTR',
     'Conventional + residue; mungbean only in residue treatments (rule 71, FLAG).', 'Medium', 'INCLUDED'),
    ('K3 ZTRW-R', 'Karnal: zero-till DSR + zero-till wheat (Turbo Happy Seeder, 20 cm rows); 95 % residue removed.',
     'Zero-till DSR', 'Zero tillage', 'No (95 % removed)', '0', 'ZT', 'Zero tillage in both phases, residue removed.', 'High', 'INCLUDED'),
    ('K4 ZTRW+R+MB', 'Karnal: ZT DSR + ZT wheat + ZT mungbean (multi-crop planter); residue retained (rice 100 %, wheat 50 %, mungbean 100 %).',
     'Zero-till DSR', 'Zero tillage', 'Yes', 'rice 100 %, wheat 50 %', 'CA', 'ZT + residue; mungbean is a supplementary condition (rule 71).', 'High', 'INCLUDED'),
    ('K5 PBMW-R', 'Karnal: permanent raised bed maize-wheat, residue removed.', 'n/a (maize)', 'Zero tillage on permanent beds', 'No', '0', 'EXCLUDED',
     'Maize-wheat system (rule 31).', 'High', 'EXCLUDED'),
    ('K6 PBMW+R+MB', 'Karnal: permanent raised bed maize-wheat-mungbean, residue retained.', 'n/a (maize)', 'Zero tillage on permanent beds', 'Yes', '50 %', 'EXCLUDED',
     'Maize-wheat system (rule 31).', 'High', 'EXCLUDED'),
    ('S1 CTRW-R', 'Samastipur: puddled TPR + conventional wheat (1 rotavator pass), residue removed.', 'Puddled transplanted (conventional)',
     'Conventional (1 rotavator pass)', 'No (95 % removed)', '0', 'CT', 'As K1 (FLAG rotavator depth).', 'Medium', 'INCLUDED'),
    ('S2 ZTRW+R+MB', 'Samastipur: ZT DSR + ZT wheat + ZT mungbean, residue 100 % retained.', 'Zero-till DSR', 'Zero tillage', 'Yes', '100 %', 'CA',
     'ZT + residue (rule 71 for mungbean).', 'High', 'INCLUDED'),
    ('S3 PBMW+R+MB', 'Samastipur: permanent bed maize-wheat-mungbean, residue retained.', 'n/a (maize)', 'Zero tillage on beds', 'Yes', '50 %', 'EXCLUDED',
     'Maize-wheat system (rule 31).', 'High', 'EXCLUDED'),
    ('S4 PBMM+R+MB', 'Samastipur: permanent bed maize-mustard-mungbean, residue retained.', 'n/a (maize)', 'n/a (mustard)', 'Yes', '100 %', 'EXCLUDED',
     'Not a rice-wheat system (rule 31).', 'High', 'EXCLUDED'),
]

STUDY_INFO_EXTRA = dict(
    estab=2012, yeardata='Karnal 2015 / 2017; Samastipur 2016 / 2018', years='2 soil samplings per site (3 and 5 yr); 5-yr mean yields',
    rotation='Rice-wheat (+ ZT mungbean in residue treatments); maize-based PB treatments excluded', wheatvar='Not reported', ricevar='Not reported',
    N='Recommended (not stated)', P='Recommended (not stated)', K='Recommended (not stated)',
    residue='Residue removed (95 %) in K1 / K3 / S1; retained rice 100 %, wheat 50 % (Karnal) or 100 % (Samastipur), mungbean 100 %',
    irrigation='Irrigated (recommended practices)',
    treatments='Karnal K1-K6, Samastipur S1-S4 (RBD, 3 reps, 350 m2 plots)',
    params=('5-yr mean rice / wheat / system (REY) yield, mungbean yield; TOC, total N, POXC at 0-5 and 5-15 cm (3 and 5 yr); TOC stock 0-5 / 0-15 cm; '
            'cPOM-C, fPOM-C, MOC (OMF-C), PON (derived from fraction stocks); BD and porosity (derived); CL, LI, CPI, CMI (derived)'),
    supp=('Supplementary Tables S1-S5 and Fig. S1 (crop residue C / N, plant C input, Karnal 5-15 and 0-15 cm fraction data) referenced - NOT downloaded '
          '(rule 7: author permission needed). frontiersin.org article page.'),
)
SITE_ROWS = [
    (SK, dict(texture='Loam (Anthraquic Haplustepts)', duration='4-10 Y', notes_extra='Karnal site. Possibly the same CCAFS / CSISA Taraori platform as studies 19 / 24 / 107 but a different treatment set (K3 ZT without residue, K5 / K6 beds) - entered as NEW serial; author to confirm.')),
    (SS, dict(texture='Silty loam (Oxyaquic Haplustepts)', duration='4-10 Y', notes_extra='Samastipur site (BISA farm, est. Nov 2012) - different trial from study 71 (RAU Pusa, est. 2006).')),
]
NOTES_SI = ('NEW serial 321 (ext\\643.pdf). Two sites (rows). CT coding of the single rotavator pass for wheat (depth not stated) - FLAG. '
            'Not entered (no sheet): TN stock, POXC stock, fraction mass proportions and fraction N stocks (in notes), correlation matrix (Table 10). '
            'Derived (flagged): BD (from TOC stock / TOC), porosity, fraction C / N concentrations, CL / LI / CPI / CMI. '
            'K4 2015 0-5 cm stock 10.8 Mg/ha looks misprinted (implies BD 2.23).')
