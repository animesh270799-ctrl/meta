"""Study 324 - Nawaz A., Farooq M., Ahmad R., Basra S.M.A. & Lal R. 2016 Eur. J. Agron. 76:130-137 (ext 649): seed priming x NT / PT wheat after DSAR / PudTR."""
from common import base, notes

ST = dict(
    no=324, serial=324, authors='Nawaz A., Farooq M., Ahmad R., Basra S.M.A. & Lal R.', year=2016, journal='European Journal of Agronomy',
    ref=('Nawaz A., Farooq M., Ahmad R., Basra S.M.A. & Lal R. (2016) Seed priming improves stand establishment and productivity of no till wheat grown after direct '
         'seeded aerobic and transplanted flooded rice. European Journal of Agronomy 76:130-137, doi 10.1016/j.eja.2016.02.012.'),
    doi='10.1016/j.eja.2016.02.012',
    fert='Wheat Punjab-2011, 125 kg/ha seed, 22.5 cm rows, sown 26 / 28 Nov; 115 N - 90 P kg/ha (DAP + urea; full P + 1/3 N at sowing); 5 irrigations (406 mm); iodo-mesosulfuron 14.4 g a.i./ha',
    tmap=('RCBD split plot, 4 blocks, UAF Faisalabad, wheat 2012-13 and 2013-14. Main plots = rice-wheat systems: DSAR (rice drilled into soil pulverised by 4 cultivations to 30 cm, aerobic) or PudTR '
          '(4 cultivations + puddling, transplanted flooded) followed by PT wheat (2 cultivator passes + 2 plankings) or NT wheat (drilled into stubble). Coding as studies 147 / 238: '
          'PudTR-PT -> CT (row a), DSAR-PT -> CT (row b, rule 135); PudTR-NT -> pZT (row a), DSAR-NT -> pZT (row b) (tilled DSR / puddled rice + ZT wheat, rules 124 / 138). '
          'Residue not stated (stubble only) -> no residue (rule 104). Sub plots = seed priming (control, hydropriming, osmopriming CaCl2) -> one row per level (rule 33; cell means printed).'),
    details=('TREATMENTS IN PAPER: RWS main plots DSAR-NT, DSAR-PT, PudTR-NT, PudTR-PT x seed priming sub plots control / hydropriming (HP) / osmopriming (OP, CaCl2 -1.25 MPa, 12 h); RCBD split plot, 4 blocks, '
             'main 8 x 9.7 m, sub 1.8 x 7 m. || MAPPING: PudTR-PT -> CT (row a) [rice: puddled TPR; wheat: plough till; residue: No] | DSAR-PT -> CT (row b) [rice: dry DSR after 4 cultivations; wheat: plough till] | '
             'PudTR-NT -> pZT (row a) [rice: puddled TPR; wheat: no till into stubble] | DSAR-NT -> pZT (row b) [rice: tilled dry DSR; wheat: no till]'),
)
SITE = dict(country='Pakistan (Punjab)', site='Agronomic Research Area, University of Agriculture, Faisalabad', lat=31.8, lon=73.8, climate='TEMP', duration='0-3 Y', soil='LOAMY',
            **{'RAIN FALL': 300, 'ph (initial)': 7.05, 'soc (initial)': 5.2, 'MAX TEMP': 21, 'MIN TEMP': 6})
PR = ['Control', 'HP', 'OP']
PRN = {'Control': 'non-primed control', 'HP': 'hydropriming (aerated water 12 h)', 'OP': 'osmopriming (CaCl2, -1.25 MPa, 12 h)'}
# Table 3 / 4 cell values per year: system -> priming -> value ; order DSAR-PT, PudTR-PT, DSAR-NT, PudTR-NT
T = {
 'PH': {2012: {'DSAR-PT': (86.9, 91.0, 93.1), 'PudTR-PT': (89.3, 91.1, 89.6), 'DSAR-NT': (87.4, 87.4, 88.1), 'PudTR-NT': (85.1, 86.1, 85.6)},
        2013: {'DSAR-PT': (94.0, 97.6, 98.8), 'PudTR-PT': (95.4, 96.8, 96.3), 'DSAR-NT': (93.5, 94.1, 95.3), 'PudTR-NT': (91.9, 93.3, 92.8)}},
 'SPL': {2012: {'DSAR-PT': (8.23, 8.55, 8.25), 'PudTR-PT': (8.04, 8.32, 8.21), 'DSAR-NT': (8.07, 8.26, 8.56), 'PudTR-NT': (8.52, 8.55, 8.52)},
         2013: {'DSAR-PT': (8.75, 9.01, 9.14), 'PudTR-PT': (8.38, 8.95, 9.02), 'DSAR-NT': (8.68, 9.50, 9.13), 'PudTR-NT': (8.65, 9.60, 9.39)}},
 'TT': {2012: {'DSAR-PT': (409, 436, 455), 'PudTR-PT': (387, 425, 450), 'DSAR-NT': (359, 414, 390), 'PudTR-NT': (322, 344, 330)},
        2013: {'DSAR-PT': (397, 410, 425), 'PudTR-PT': (379, 401, 434), 'DSAR-NT': (373, 376, 418), 'PudTR-NT': (336, 372, 359)}},
 'PT': {2012: {'DSAR-PT': (330, 357, 338), 'PudTR-PT': (311, 334, 339), 'DSAR-NT': (330, 361, 360), 'PudTR-NT': (283, 292, 292)},
        2013: {'DSAR-PT': (324, 344, 349), 'PudTR-PT': (335, 331, 333), 'DSAR-NT': (341, 346, 370), 'PudTR-NT': (321, 329, 327)}},
 'GPS': {2012: {'DSAR-PT': (44.2, 47.8, 46.9), 'PudTR-PT': (42.6, 43.6, 43.5), 'DSAR-NT': (42.5, 43.6, 45.9), 'PudTR-NT': (41.0, 42.7, 43.8)},
         2013: {'DSAR-PT': (40.7, 46.6, 47.8), 'PudTR-PT': (40.4, 42.4, 41.0), 'DSAR-NT': (38.1, 39.7, 44.4), 'PudTR-NT': (37.1, 39.4, 42.4)}},
 'TGW': {2012: {'DSAR-PT': (34.6, 34.2, 36.1), 'PudTR-PT': (34.8, 34.5, 38.1), 'DSAR-NT': (31.6, 36.7, 37.2), 'PudTR-NT': (31.8, 34.5, 36.8)},
         2013: {'DSAR-PT': (29.3, 30.6, 33.4), 'PudTR-PT': (32.0, 32.3, 37.5), 'DSAR-NT': (31.3, 34.3, 34.2), 'PudTR-NT': (29.6, 33.1, 34.4)}},
 'BY': {2012: {'DSAR-PT': (10.2, 10.6, 12.2), 'PudTR-PT': (10.7, 10.7, 11.4), 'DSAR-NT': (9.0, 9.6, 10.0), 'PudTR-NT': (8.4, 8.6, 9.8)},
        2013: {'DSAR-PT': (11.8, 13.2, 14.5), 'PudTR-PT': (11.6, 13.1, 14.6), 'DSAR-NT': (12.2, 12.6, 12.7), 'PudTR-NT': (11.5, 11.9, 12.1)}},
 'GY': {2012: {'DSAR-PT': (4.09, 4.22, 4.81), 'PudTR-PT': (3.73, 4.00, 4.41), 'DSAR-NT': (4.27, 4.64, 5.23), 'PudTR-NT': (3.58, 3.59, 4.07)},
        2013: {'DSAR-PT': (3.84, 4.07, 4.36), 'PudTR-PT': (3.83, 4.04, 4.17), 'DSAR-NT': (4.05, 4.13, 4.52), 'PudTR-NT': (3.33, 3.78, 4.17)}},
 'HI': {2012: {'DSAR-PT': (40.1, 39.9, 39.6), 'PudTR-PT': (35.0, 37.6, 38.8), 'DSAR-NT': (47.6, 48.4, 52.4), 'PudTR-NT': (42.5, 42.0, 41.6)},
        2013: {'DSAR-PT': (32.8, 30.9, 30.1), 'PudTR-PT': (33.4, 31.0, 28.5), 'DSAR-NT': (33.3, 32.8, 35.7), 'PudTR-NT': (29.0, 31.8, 34.4)}},
 'WP': {2012: {'DSAR-PT': (8.05, 8.31, 9.49), 'PudTR-PT': (7.36, 7.89, 8.70), 'DSAR-NT': (8.42, 9.15, 10.31), 'PudTR-NT': (7.06, 7.08, 8.02)},
        2013: {'DSAR-PT': (7.23, 7.65, 8.21), 'PudTR-PT': (7.21, 7.60, 7.84), 'DSAR-NT': (7.61, 7.78, 8.50), 'PudTR-NT': (6.26, 7.12, 7.85)}},
 'SP': {2012: {'DSAR-PT': (1.66, 1.68, 1.75), 'PudTR-PT': (1.73, 1.75, 1.77), 'DSAR-NT': (1.74, 1.80, 1.83), 'PudTR-NT': (1.74, 1.73, 1.78)},
        2013: {'DSAR-PT': (1.67, 1.73, 1.75), 'PudTR-PT': (1.70, 1.77, 1.78), 'DSAR-NT': (1.80, 1.81, 1.80), 'PudTR-NT': (1.74, 1.81, 1.80)}},
}
EMER = {2012: {'DSAR-PT': (7.44, 6.28, 6.61), 'PudTR-PT': (7.57, 6.75, 6.63), 'DSAR-NT': (7.58, 6.59, 6.76), 'PudTR-NT': (8.10, 6.67, 7.26)},
        2013: {'DSAR-PT': (8.30, 6.45, 6.78), 'PudTR-PT': (8.38, 6.99, 6.92), 'DSAR-NT': (7.67, 5.80, 5.92), 'PudTR-NT': (7.86, 5.83, 6.03)}}
# Table 5 (2-yr mean): gross, total cost, net, BCR ; order Control HP OP
ECO = {'DSAR-PT': [(1376.1, 802.0, 574.1, 1.72), (1448.8, 812.6, 636.3, 1.78), (1614.7, 875.3, 739.4, 1.84)],
       'PudTR-PT': [(1334.1, 797.0, 537.1, 1.67), (1426.8, 808.8, 618.1, 1.76), (1530.9, 867.0, 663.9, 1.77)],
       'DSAR-NT': [(1409.7, 752.1, 657.7, 1.87), (1471.3, 763.5, 707.8, 1.93), (1611.8, 827.9, 783.9, 1.95)],
       'PudTR-NT': [(1214.9, 732.2, 482.7, 1.66), (1273.9, 744.0, 529.9, 1.71), (1414.0, 806.9, 607.0, 1.75)]}
VARC = {'DSAR-PT': (199.6, 210.2, 273.0), 'PudTR-PT': (194.6, 206.4, 264.7), 'DSAR-NT': (149.7, 161.1, 225.5), 'PudTR-NT': (129.9, 141.7, 204.6)}
ROWS = [('a', 'PudTR', 'PudTR-PT', 'PudTR-NT'), ('b', 'DSAR', 'DSAR-PT', 'DSAR-NT')]
M = ('Two 1 x 1 m quadrats per plot at harvest (tillers); 20 plants (height, spike length); 20 spikes (grains / spike); bundles sun-dried 1 wk (biological yield), mini-thresher (grain); '
     'HI = grain / biological; 3 x 1000-grain sub-samples; WP = grain / (irrigation + rain), kg/ha/mm.')
ME = 'CIMMYT (1998) partial budget: yields reduced 10 %; fixed cost 602.3 US$/ha + variable cost (tillage, priming, threshing); net = gross - total cost; BCR = gross / total cost (1 US$ = 98.5 PKR).'


def rows(B):
    st = ST; out = []

    def add(sheet, vals, body, y=1, unit=None, src=None, meth=M, crop=None, yd=None):
        obs, nt = notes(st, body, y=y)
        v = base(st, SITE, {'year of data collection/experiment': yd, 'YEAR OF DATA (duration)': yd})
        v.update(vals)
        v.update({'UNIT': unit, 'Crop/season of sampling': crop, 'Data source': src, 'Method used (from paper)': meth, 'Obs': obs, 'Rep': 4, 'Notes/Doubts': nt})
        out.append((sheet, B.add_row(sheet, v)))

    for yr in (2012, 2013):
        ys = f'{yr}-{str(yr + 1)[2:]}'
        for tag, rice, ct, pz in ROWS:
            for i, p in enumerate(PR):
                g = lambda k: (T[k][yr][ct][i], T[k][yr][pz][i])
                head = (f"ROW {tag} ({rice} rice), seed priming = {PRN[p]}: CT = {ct}, pZT = {pz} (rule 33 cell means). Wheat {ys}. Residue not stated (stubble only, rule 104). ")
                cs = f'Wheat {ys}, harvest; seed priming {p}'
                c, z = g('GY'); bc, bz = g('BY')
                add('YIELD', {'WYIELD_CT': c, 'WYIELD_pZT': z, 'W STRAW_CT': f'=ROUND({bc}-{c},2)', 'W STRAW_pZT': f'=ROUND({bz}-{z},2)'},
                    head + f'Table 4 grain yield; straw DERIVED = biological ({bc} / {bz}) - grain. System productivity (output / input value ratio, rice + wheat): CT {T["SP"][yr][ct][i]}, pZT {T["SP"][yr][pz][i]} - no sheet. '
                    f'Time to 50 % emergence (days): CT {EMER[yr][ct][i]}, pZT {EMER[yr][pz][i]} - no sheet.', unit='t/ha (Mg/ha)', src='Table 4 (straw DERIVED)', crop=cs, yd=ys)
                add('DRY MATTER', {'DM_WCT': f'=ROUND({bc}*1000,0)', 'DM_WpZT': f'=ROUND({bz}*1000,0)'}, head + 'Table 4 biological yield (Mg/ha x 1000).', unit='kg/ha above-ground biomass at harvest (biological yield)',
                    src='Table 4', crop=cs, yd=ys)
                c, z = g('HI')
                add('HARVEST INDEX', {'HI_WCT': f'=ROUND({c}/100,3)', 'HI_WpZT': f'=ROUND({z}/100,3)'}, head + 'Table 4 harvest index (printed %, / 100).', unit='ratio (printed % / 100)', src='Table 4', crop=cs, yd=ys)
                c, z = g('WP')
                add('WUE', {'WUE_WCT': c, 'WUE_WpZT': z}, head + 'Table 4 water productivity (irrigation 406 mm + rainfall).', unit='kg/ha/mm (grain / (irrigation + rainfall))', src='Table 4', crop=cs, yd=ys)
                c, z = g('PH')
                add('PLANT HEIGHT', {'PLH_WCT': c, 'PLH_WpZT': z}, head + 'Table 3 plant height.', unit='cm (wheat, at harvest)', src='Table 3', crop=cs, yd=ys)
                c, z = g('SPL')
                add('PANICLE-SPIKE LENGTH', {'SPL_WCT': c, 'SPL_WpZT': z}, head + 'Table 3 spike length.', unit='cm (wheat spike length)', src='Table 3', crop=cs, yd=ys)
                c, z = g('PT'); tc, tz = g('TT')
                add('PANICLE-SPIKE DENSITY', {'PSD_WCT': c, 'PSD_WpZT': z}, head + f'Table 3 PRODUCTIVE tillers per m2 (= spikes). Total tillers: CT {tc}, pZT {tz} - notes.', unit='no./m2 (productive tillers)', src='Table 3', crop=cs, yd=ys)
                c, z = g('GPS')
                add('GRAINS PER PANICLE', {'GPP_WCT': c, 'GPP_WpZT': z}, head + 'Table 3 grains per spike.', unit='grains per spike (wheat)', src='Table 3', crop=cs, yd=ys)
                c, z = g('TGW')
                add('1000-GRAIN WEIGHT', {'TGW_WCT': c, 'TGW_WpZT': z}, head + 'Table 4 1000-grain weight.', unit='g', src='Table 4', crop=cs, yd=ys)
    # economics, 2-yr mean (Table 5)
    for tag, rice, ct, pz in ROWS:
        for i, p in enumerate(PR):
            ec, ez = ECO[ct][i], ECO[pz][i]
            head = (f"ROW {tag} ({rice} rice), seed priming = {PRN[p]}: CT = {ct}, pZT = {pz}. Table 5 wheat economics, 2-YEAR MEAN (2012-14; yields reduced 10 %). "
                    f"Variable cost CT {VARC[ct][i]}, pZT {VARC[pz][i]}; fixed cost 602.3 US$/ha.")
            cs = f'Wheat 2012-13 and 2013-14 (2-yr mean); seed priming {p}'
            yd = '2012-13 to 2013-14 (2-yr mean)'
            add('GROSS RETURN', {'GR_WCT': ec[0], 'GR_WpZT': ez[0]}, head, y=2, unit='US$/ha (gross income)', src='Table 5', meth=ME, crop=cs, yd=yd)
            add('COST OF CULTIVATION', {'COST_WCT': ec[1], 'COST_WpZT': ez[1]}, head + ' Total cost = fixed + variable.', y=2, unit='US$/ha (total cost)', src='Table 5', meth=ME, crop=cs, yd=yd)
            add('NET RETURN', {'NR_WCT': ec[2], 'NR_WpZT': ez[2]}, head, y=2, unit='US$/ha (net benefits)', src='Table 5', meth=ME, crop=cs, yd=yd)
            add('BC ratio', {'BC_WCT': f'=ROUND({ec[3]}-1,2)', 'BC_WpZT': f'=ROUND({ez[3]}-1,2)'}, head + f' Printed BCR = gross / total cost ({ec[3]} / {ez[3]}) - 1 (rule 57).', y=2,
                unit='ratio (net / cost; printed gross / cost - 1)', src='Table 5 (converted)', meth=ME, crop=cs, yd=yd)
    return out


TM = [
    ('PudTR-PT', 'Puddled transplanted flooded rice (4 cultivations to 30 cm + puddling) + plough-till wheat (2 cultivator passes + 2 plankings)', 'Puddled TPR', 'Conventional (plough till)', 'Not stated (No)', None, 'CT (row a)', 'Conventional in both phases.', 'High', 'INCLUDED'),
    ('DSAR-PT', 'Direct-seeded aerobic rice drilled after 4 cultivations (30 cm) + plough-till wheat', 'Tilled dry DSR', 'Conventional (plough till)', 'Not stated (No)', None, 'CT (row b)', 'Dry DSR + conventional wheat = CT (rule 135; as 147).', 'High', 'INCLUDED'),
    ('PudTR-NT', 'Puddled TPR + no-till wheat drilled into stubble', 'Puddled TPR', 'No tillage', 'Not stated (No)', None, 'pZT (row a)', 'Puddled rice + ZT wheat (rule 124; as 147 / 238).', 'High', 'INCLUDED'),
    ('DSAR-NT', 'Tilled dry DSAR + no-till wheat', 'Tilled dry DSR', 'No tillage', 'Not stated (No)', None, 'pZT (row b)', 'Tilled DSR + ZT wheat -> pZT (rules 135 / 138; as 147 / 238).', 'High', 'INCLUDED'),
    ('Seed priming (control / HP / OP)', 'Sub-plot factor', 'n/a', 'n/a', 'n/a', None, 'One row per level', 'Non-tillage factor, cell means printed (rule 33).', 'High', 'INCLUDED'),
]
STUDY_INFO = dict(estab=2012, yeardata='Wheat 2012-13, 2013-14', years='2 (year-wise; economics 2-yr mean)', texture='Sandy loam (Lyallpur series, Ustalfic Haplargid)', rotation='Rice-wheat',
                  wheatvar='Punjab-2011', ricevar='Not reported (basmati implied)', N='115', P='90 (P as printed; DAP)', K='Not applied', residue='Not stated (NT drilled into stubble)',
                  irrigation='Wheat 5 irrigations (1645 m3, 406 mm); rice DSAR aerobic, PudTR flooded', treatments='4 RWS (main) x 3 seed priming (sub), RCBD split plot, 4 blocks',
                  params=('Wheat grain yield, straw (derived), biological yield, HI, water productivity, plant height, spike length, productive tillers, grains / spike, 1000-grain weight (year-wise, per priming level); '
                          'gross / total cost / net / B:C (2-yr mean) - CT vs pZT rows a (puddled) / b (DSAR)'),
                  supp='None referenced',
                  notes=('NEW serial 324 (ext\\649.pdf). Different trial from 147 (Nankana / Sheikhupura) and 238 (UAF, Sesbania / mulch). Coordinates as printed (31.8 N, 73.8 E, as study 238). '
                         'Not entered (no sheet): emergence time / T50 / MET / emergence index (Table 2), total tillers, system productivity ratio (Table 4). Soil EC 3.61-3.71 dS/m, total N 0.07-0.08 %, exch. K 176-178 ppm, avail. P 4.45-4.61 ppm.'))
SITES = [('UAF Agronomic Research Area, Faisalabad', '31.8 N', '73.8 E', 31.8, 73.8, 'Paper (as printed)', 'TEMP', None)]
