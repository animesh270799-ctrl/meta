"""Study 329 - Saharawat Y.S. et al. 2010 Field Crops Res. 116:260-267 (ext 654): tillage x rice establishment, CCSHAU College of Agriculture farm, Kaul (Kaithal)."""
from common import base, notes

ST = dict(
    no=329, serial=329, authors='Saharawat Y.S., Singh B., Malik R.K., Ladha J.K., Gathala M., Jat M.L. & Kumar V.', year=2010, journal='Field Crops Research',
    ref=('Saharawat Y.S., Singh B., Malik R.K., Ladha J.K., Gathala M., Jat M.L. & Kumar V. (2010) Evaluation of alternative tillage and crop establishment methods in a rice-wheat rotation in North Western IGP. '
         'Field Crops Research 116:260-267, doi 10.1016/j.fcr.2010.01.003.'),
    doi='10.1016/j.fcr.2010.01.003',
    fert='Rice HKR-126: 160 N + 26 P + 50 K + 25 ZnSO4 kg/ha; wheat PBW-343 (100 kg seed/ha, 20 cm rows): 150 N + 26 P + 50 K kg/ha; glyphosate before no-till seeding; plots kept weed-free',
    tmap=('RCB, 3 reps (17 x 8.5 m), CCSHAU College of Agriculture farm, Kaul, rice 2005 / 2006, wheat 2005-06 / 2006-07. T1 puddled transplanted rice (2 dry harrowings + 2 plankings + 2 wet rotavator passes) '
          '+ conventional drill-sown wheat (2 harrowings + 3 cultivator ploughings + planking) -> CT ; T2 REDUCED-TILLED (2 harrowings + 2 plankings, no puddling) transplanted rice + no-till wheat -> MT '
          '(rule 127: the paper calls it reduced tillage - FLAG, rule 138 would give pZT) ; T3 no-till transplanted rice + no-till wheat -> ZT (row a) ; T4 puddled drum-seeded wet DSR + no-till wheat -> pZT ; '
          'T5 no-till drill-seeded dry DSR + no-till wheat -> ZT (row b). Residue not described (crops cut 15 cm above ground) -> no residue codes (rule 104).'),
    details=('TREATMENTS IN PAPER: T1 CT puddled TPR - CT wheat; T2 reduced-tilled unpuddled TPR - ZT wheat; T3 no-till TPR - ZT wheat; T4 CT puddled drum-seeded rice - ZT wheat; T5 no-till drill-seeded rice - ZT wheat '
             '(RCB, 3 reps). || MAPPING: T1 -> CT [rice: puddled TPR; wheat: conventional; residue: not stated] | T2 -> MT [rice: reduced-tilled unpuddled TPR; wheat: no-till; rule 127 - FLAG] | '
             'T3 -> ZT (row a) [rice: no-till TPR; wheat: no-till] | T4 -> pZT [rice: puddled wet drum-seeded DSR; wheat: no-till] | T5 -> ZT (row b) [rice: no-till dry DSR; wheat: no-till]'),
)
SITE = dict(country='India (Haryana)', site='CCS HAU College of Agriculture research farm, Kaul (Kaithal)', lat=29.850, lon=76.683, climate='ST', duration='0-3 Y', soil='LOAMY',
            **{'RAIN FALL': 750, 'ph (initial)': 7.8, 'soc (initial)': 4.1, 'Bdi': 1.58})
TAGS = {'a': ('CT = T1, MT = T2, ZT = T3, pZT = T4', {'CT': 0, 'MT': 1, 'ZT': 2, 'pZT': 3}), 'b': ('CT = T1, ZT = T5 (CT repeated)', {'CT': 0, 'ZT': 4})}
M_Y = 'Central 100 m2 harvested; rice grain at 14 %, wheat at 12 % moisture; straw oven-dry; yield components from 1 m2 quadrats at 3 places.'


def rows(B):
    st = ST; out = []

    def add(sheet, vals, body, tag, unit, src, crop, yd, y=1, meth=M_Y):
        obs, nt = notes(st, f'ROW {tag}: {TAGS[tag][0]}. ' + body, y=y)
        v = base(st, SITE, {'year of data collection/experiment': yd, 'YEAR OF DATA (duration)': yd})
        v.update(vals)
        v.update({'UNIT': unit, 'Crop/season of sampling': crop, 'Data source': src, 'Method used (from paper)': meth, 'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
        out.append((sheet, B.add_row(sheet, v)))

    def cv(tag, pre, vals, fmt=None):
        return {f'{pre}{c}': (fmt.format(vals[i]) if fmt else vals[i]) for c, i in TAGS[tag][1].items() if vals[i] is not None}

    YR = (('2005', '2005-06', 'Year 1: rice 2005, wheat 2005-06'), ('2006', '2006-07', 'Year 2: rice 2006, wheat 2006-07'))
    T2 = {0: ([7.28, 7.23, 7.16, 6.73, 6.67], [4.93, 5.14, 5.32, 5.32, 5.33], [12.21, 12.37, 12.48, 12.05, 12.00]),
          1: ([7.06, 6.92, 6.86, 6.61, 6.52], [4.74, 4.81, 4.92, 4.86, 4.92], [11.80, 11.73, 11.78, 11.47, 11.44])}
    T3 = {0: dict(PAN=[253, 249, 244, 274, 269], TGW=[26.8, 26.8, 26.7, 26.2, 26.1], GPP=[117.6, 117.3, 116.8, 108.0, 105.3], HIR=[48, 48, 47, 45, 45], HIW=[42, 43, 43, 43, 43]),
          1: dict(PAN=[242, 236, 238, 266, 260], TGW=[27.2, 27.1, 26.8, 26.9, 26.5], GPP=[121.0, 121.2, 119.2, 116.2, 111.8], HIR=[47, 47, 47, 45, 44], HIW=[42, 43, 43, 43, 43])}
    T4 = {0: dict(GDR=[144, 144, 144, 139, None], GDW=[155, 155, 155, 155, None], PER=[64, 63, 63, 48, None], PEW=[32, 33, 34, 34, None]),
          1: dict(GDR=[140, 140, 140, 134, None], GDW=[151, 151, 151, 151, None], PER=[64, 63, 62, 49, None], PEW=[31, 32, 32, 32, None])}
    T5 = {0: dict(R=[2.41, 2.39, 2.43, 1.80, 2.45], W=[15.31, 16.74, 18.67, 16.94, 19.04], S=[3.66, 3.71, 3.86, 2.98, 4.00]),
          1: dict(R=[2.16, 2.04, 2.10, 1.69, 2.27], W=[16.34, 16.76, 19.37, 17.74, 19.84], S=[3.32, 3.20, 3.35, 2.74, 3.66])}
    IRR = {0: ('3018 / 3024 / 2945 / 3732 / 2718', '322 / 307 / 285 / 314 / 280', '3340 / 3331 / 3230 / 4046 / 2998'),
           1: ('3263 / 3384 / 3264 / 3916 / 2878', '290 / 287 / 254 / 274 / 248', '3553 / 3671 / 3518 / 4190 / 3126')}
    for k, (ry, wy, lab) in enumerate(YR):
        yd = f'rice {ry}, wheat {wy}'
        for tag in ('a', 'b'):
            r, w, s = T2[k]
            add('YIELD', {**cv(tag, 'RICE YIELD_', r), **cv(tag, 'WYIELD_', w), **cv(tag, 'SYS YIELD_', s)},
                f'Table 2 grain yields, {lab} (rice 14 %, wheat 12 % moisture; system = rice + wheat grain).', tag, 'Mg/ha (= t/ha)', 'Table 2', f'Rice {ry}; wheat {wy}; system', yd)
            t3 = T3[k]
            add('PANICLE-SPIKE DENSITY', cv(tag, 'PSD_R', t3['PAN']), f'Table 3 rice panicles per m2, {ry}.', tag, 'no. panicles/m2 (rice)', 'Table 3', f'Rice {ry}', yd)
            add('1000-GRAIN WEIGHT', cv(tag, 'TGW_R', t3['TGW']), f'Table 3 rice 1000-grain weight, {ry}.', tag, 'g (rice)', 'Table 3', f'Rice {ry}', yd)
            add('GRAINS PER PANICLE', cv(tag, 'GPP_R', t3['GPP']), f'Table 3 rice grains per panicle, {ry}. Spikelet sterility 4-6 % transplanted vs 8-10 % direct-seeded (text).', tag,
                'grains per panicle (rice)', 'Table 3', f'Rice {ry}', yd)
            add('HARVEST INDEX', {**cv(tag, 'HI_R', t3['HIR'], '=ROUND({}/100,2)'), **cv(tag, 'HI_W', t3['HIW'], '=ROUND({}/100,2)')},
                f'Table 3 harvest index (printed %, / 100), rice {ry} and wheat {wy}.', tag, 'ratio (printed % / 100)', 'Table 3', f'Rice {ry}; wheat {wy}', yd)
            t5 = T5[k]; ir = IRR[k]
            add('WUE', {**cv(tag, 'WUE_R', t5['R']), **cv(tag, 'WUE_W', t5['W']), **cv(tag, 'WUE_SYS', t5['S'])},
                f'Table 5 IRRIGATION water-use efficiency (grain / irrigation water applied), {lab}. Irrigation applied T1-T5 (mm): rice {ir[0]}; wheat {ir[1]}; system {ir[2]}. '
                f'Rainfall rice {"544" if k == 0 else "277"} mm, wheat {"53" if k == 0 else "64"} mm.', tag, 'kg/ha/mm (irrigation water basis)', 'Table 5', f'Rice {ry}; wheat {wy}; system', yd,
                meth='Irrigation measured with water meter (PVC pipes); IWUE = grain yield / irrigation water applied (Bhushan et al. 2007).')
            if tag == 'a':
                t4 = T4[k]
                add('DAYS TO MATURITY', {**cv(tag, 'DTM_R', t4['GDR']), **cv(tag, 'DTM_W', t4['GDW'])},
                    f'Table 4 GROWTH duration (seed to seed; rice incl. nursery for T1-T3 - FLAG), rice {ry} / wheat {wy}. T5 not printed in Table 4 (row b not available). '
                    f'Main-field duration rice T1-T4 {"114 / 114 / 114 / 139" if k == 0 else "110 / 110 / 110 / 134"} days.', tag, 'days (seed-to-seed growth duration)', 'Table 4', f'Rice {ry}; wheat {wy}', yd)
                add('PRODUCTION EFFICIENCY', {**cv(tag, 'PE_R', t4['PER']), **cv(tag, 'PE_W', t4['PEW'])},
                    f'Table 4 grain production efficiency (kg grain/ha/day), rice {ry} / wheat {wy}. T5 not printed. Biomass production efficiency (kg/ha/day) rice T1-T4 '
                    f'{"133 / 132 / 131 / 106" if k == 0 else "136 / 133 / 132 / 110"}, wheat {"74 / 77 / 80 / 80" if k == 0 else "73 / 74 / 75 / 75"} - no sheet.', tag,
                    'kg grain/ha/day', 'Table 4', f'Rice {ry}; wheat {wy}', yd)
    # wheat effective tillers (Table 3: both columns headed 2005-2006 with identical values)
    for tag in ('a', 'b'):
        add('PANICLE-SPIKE DENSITY', cv(tag, 'PSD_W', [411, 432, 456, 469, 472]),
            'Table 3 wheat effective tillers per m2. Both printed columns are headed "2005-2006" and carry identical values (header misprint / duplicate - FLAG); entered once as year 1.', tag,
            'no. effective tillers/m2 (wheat)', 'Table 3', 'Wheat 2005-06 (column duplicated - FLAG)', 'wheat 2005-06')
    # net returns (Table 7, 2-yr average, US$/ha)
    NR = dict(R=[330, 341, 348, 324, 340], W=[356, 371, 373, 380, 380], S=[686, 712, 721, 704, 720])
    for tag in ('a', 'b'):
        add('NET RETURN', {**cv(tag, 'NR_R', NR['R']), **cv(tag, 'NR_W', NR['W']), **cv(tag, 'NR_SYS', NR['S'])},
            'Table 7 average net returns (2-yr average). Gross return at MSP (rice US$ 172.2 / Mg, wheat US$ 214.2 / Mg) minus total cost (inputs, labour, machine hire).', tag,
            'US$/ha', 'Table 7', 'Rice, wheat and system (2-yr average)', '2005-2007 (2-yr average)', y=2,
            meth='Cost of cultivation at CCSHAU approved rates (seed, fertiliser, biocide, labour, machine hire, irrigation); gross return at government support prices; net = gross - cost.')
    return out


TM = [
    ('T1 CT puddled TPR - CT wheat', 'Rice: 2 dry harrowings + 2 plankings + 2 wet rotavator passes, transplanted; wheat: 2 harrowings + 3 cultivator ploughings + 1 planking, drill seeded',
     'Puddled TPR', 'Conventional', 'Not stated', None, 'CT', 'Conventional in both phases.', 'High', 'INCLUDED'),
    ('T2 reduced-tilled unpuddled TPR - ZT wheat', 'Rice: 2 harrowings + 2 plankings (dry), no puddling, transplanted; wheat no-till drill', 'Reduced-till unpuddled TPR', 'No tillage', 'Not stated', None,
     'MT - FLAG', 'Paper calls it reduced tillage (rule 127); rule 138 alternative = pZT.', 'Medium', 'INCLUDED'),
    ('T3 no-till TPR - ZT wheat', 'Rice transplanted into no-till soil (glyphosate); wheat no-till drill', 'No-till TPR', 'No tillage', 'Not stated', None, 'ZT (row a)', 'No tillage in both phases.', 'High', 'INCLUDED'),
    ('T4 puddled drum-seeded rice - ZT wheat', 'Rice: dry harrowings + 2 wet rotavator passes, sprouted seed by drum seeder; wheat no-till drill', 'Puddled wet DSR', 'No tillage', 'Not stated', None, 'pZT',
     'Puddled rice + ZT wheat (rules 124 / 135).', 'High', 'INCLUDED'),
    ('T5 no-till DSR - ZT wheat', 'Rice dry-seeded with no-till drill; wheat no-till drill', 'No-till dry DSR', 'No tillage', 'Not stated', None, 'ZT (row b)', 'No-till DSR + ZT wheat (rule 138).', 'High', 'INCLUDED'),
]
STUDY_INFO = dict(estab=2005, yeardata='Rice 2005, 2006; wheat 2005-06, 2006-07', years='2 (year-wise)', texture='Clay loam (0-15 cm), BD 1.58', rotation='Rice-wheat',
                  wheatvar='PBW-343', ricevar='HKR-126', N='160 rice / 150 wheat', P='26 / 26 (P)', K='50 / 50 (K)', residue='Not stated (crops cut 15 cm above ground)',
                  irrigation='Rice continuous flooding (T1-T4), T5 irrigation at hairline cracks; wheat 4 irrigations (Z20, Z29, Z36, Z83); water metered',
                  treatments='5 tillage x rice establishment treatments (T1-T5), RCB, 3 reps',
                  supp='None',
                  params=('Year-wise rice, wheat and system grain yield; rice panicles / m2, grains / panicle, TGW; rice and wheat HI; irrigation WUE (rice / wheat / system); growth duration and grain production efficiency '
                          '(T1-T4 only); wheat effective tillers (year 1); net returns (2-yr average) - rows a (CT / MT / ZT / pZT) and b (CT / ZT)'),
                  notes=('NEW serial 329 (ext\\654.pdf). Kaul (Kaithal) on-station trial - not one of the Modipuram / Karnal trials already entered (checked studies 15, 158, 175, 195, 199). '
                         'T2 coded MT under rule 127 (paper: "reduced tilled (unpuddled) transplanted rice") - FLAG (rule 138 alternative pZT). '
                         'NOT ON A SHEET: irrigation water applied and per-day water use (Table 5, given in WUE notes), machine / human labour and biocide use (Table 6: machine labour rice T1-T5 14.2 / 12.0 / 7.2 / 14.8 / 7.6 h/ha, '
                         'wheat 11.5 / 6.5 / 6.5 / 6.5 / 6.5; human labour rice 64 / 65 / 58 / 67 / 56, wheat 15 / 14 / 14 / 14 / 14 day/ha; biocide rice 14.5 x 4 / 22.5, wheat 2.5 kg/ha), biomass production efficiency, field duration. '
                         'Soil 0-15 cm: BD 1.58, pH 7.8, EC 0.24, OC 0.41 %, KMnO4-N 141, Olsen P 25, NH4OAc-K 301 kg/ha. Long-term rainfall 750 mm.'))
SITES = [('CCSHAU College of Agriculture farm, Kaul (Kaithal)', "29 51' N", "76 41' E", 29.850, 76.683, 'Paper', 'ST', None)]
