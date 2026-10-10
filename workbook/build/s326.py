"""Study 326 - Parihar S.S. 2004 Indian J. Agron. 49(1):1-5 (ext 651): rice establishment x irrigation, wheat tillage x N, Bilaspur."""
from common import base, notes

ST = dict(
    no=326, serial=326, authors='Parihar S.S.', year=2004, journal='Indian Journal of Agronomy',
    ref=('Parihar S.S. (2004) Effect of crop-establishment method, tillage, irrigation and nitrogen on production potential of rice (Oryza sativa)-wheat (Triticum aestivum) '
         'cropping system. Indian Journal of Agronomy 49(1):1-5.'),
    doi=None,
    fert='Rice Mahamaya 100:50:30 N:P2O5:K2O kg/ha (1/2 N basal, 2 splits); wheat HD 2285, 80 (N1) or 120 (N2) kg N + 60 P2O5 + 40 K2O kg/ha; wheat irrigated at 0.9 IW:CPE (6 cm per irrigation)',
    tmap=('Split-split plot, 3 reps, IGKV Bilaspur 1999-2002. Rice main plots M1 puddled transplanted, M2 puddled line-sown sprouted seed, M3 line-sown sprouted seed WITHOUT puddling (x 4 irrigation schedules); '
          'wheat after rice: 4 tillage levels in sub plots x 2 N levels. T4 cultivator twice + harrowing once + planking twice -> CT (row a) ; T3 cultivator twice + rotavator once -> CT (row b) ; '
          'T2 cultivator + rotavator once each -> CT (row c; 2 passes, rotary rule 13 - FLAG: paper groups T1 / T2 as zero and minimum tillage) ; T1 zero-till drill -> pZT (after puddled M1 / M2 rice, rule 124; '
          'M3 unpuddled rice, tillage before sowing not stated -> pZT FLAG, rule 138). Rice main effects (no tillage contrast in the codes) -> Notes.'),
    details=('TREATMENTS IN PAPER: rice M1 (puddling + transplanting), M2 (puddling + line sowing of sprouted seed), M3 (line sowing of sprouted seed without puddling) x I1-I4 irrigation 1 / 3 / 5 / 7 days after '
             'disappearance of ponded water; wheat T1 no-tillage (zero-till drill), T2 cultivator + rotavator once each, T3 cultivator twice + rotavator once, T4 cultivator twice + harrowing once + planking twice '
             'x N1 80 / N2 120 kg N/ha. || MAPPING: T4 -> CT (row a) [rice phase: M1 / M2 puddled or M3 unpuddled; wheat: conventional; residue: not stated] | T3 -> CT (row b) [wheat: 3 passes incl. rotavator] | '
             'T2 -> CT (row c) [wheat: cultivator + rotavator = 2 passes, rule 13 - FLAG] | T1 -> pZT [rice: puddled (M1 / M2) or unpuddled (M3, tillage not stated - FLAG); wheat: zero-till drill; residue: not stated, rule 104]'),
)
SITE = dict(country='India (Chhattisgarh)', site='Research farm, TCB College of Agriculture and Research Station (IGKV), Bilaspur', lat=22.08, lon=82.14, climate='ST', duration='0-3 Y',
            soil='LOAMY')
MN = ('M1', 'M2', 'M3')
RD = {'M1': 'puddling + manual transplanting', 'M2': 'puddling + line sowing of sprouted seed', 'M3': 'line sowing of sprouted seed WITHOUT puddling (tillage before sowing not stated - pZT FLAG)'}
# Table 6 wheat grain yield (kg/ha), 3-yr mean, pooled over N: tillage T1..T4 x M1..M3
T6 = {'T1': (2554, 2590, 2906), 'T2': (2900, 2995, 3250), 'T3': (3200, 3240, 3325), 'T4': (3265, 3310, 3465)}
ROWS = (('a', 'T4', 'cultivator twice + harrowing once + planking twice'), ('b', 'T3', 'cultivator twice + rotavator once'),
        ('c', 'T2', 'cultivator + rotavator once each (2 passes, rotary rule - FLAG)'))
M_Y = 'Manual harvest; grain yield from net plot (kg/ha, moisture basis not stated); 3-yr mean (1999-2000 to 2001-02).'
YRS = 'wheat 1999-2000 to 2001-02 (3-yr mean)'


def rows(B):
    st = ST; out = []

    def add(sheet, vals, body, y=3, t=1, unit=None, src=None, meth=M_Y, crop='Wheat (rabi), 3-yr mean'):
        obs, nt = notes(st, body, y=y, t=t)
        v = base(st, SITE, {'year of data collection/experiment': '1999-2002', 'YEAR OF DATA (duration)': YRS})
        v.update(vals)
        v.update({'UNIT': unit, 'Crop/season of sampling': crop, 'Data source': src, 'Method used (from paper)': meth, 'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
        out.append((sheet, B.add_row(sheet, v)))

    # ---- Table 6 cell means (rice establishment x wheat tillage), pooled over N
    for i, m in enumerate(MN):
        for tag, tl, desc in ROWS:
            add('YIELD', {'WYIELD_CT': f'=ROUND({T6[tl][i]}/1000,3)', 'WYIELD_pZT': f'=ROUND({T6["T1"][i]}/1000,3)'},
                f'ROW {m}-{tag}: rice {m} ({RD[m]}); CT = {tl} ({desc}), pZT = T1 (zero-till drill). Table 6 wheat grain yield CELL MEANS (rice establishment x wheat tillage), 3-yr mean, '
                f'pooled over N 80 / 120 kg/ha (FLAG, T = 2). kg/ha / 1000. Row means T1-T4 2683 / 3048 / 3255 / 3347 kg/ha.', t=2, unit='t/ha (printed kg/ha / 1000)', src='Table 6')
    # ---- tillage main effects (pooled over rice establishment and N) - parameters without cell means
    HEAD = ('TILLAGE MAIN EFFECT pooled over rice establishment M1 / M2 / M3 and N 80 / 120 (FLAG, rule 33; no excluded level: M1-M3 + T4 = CT, M1-M3 + T1 = pZT). '
            'pZT = T1 zero-till drill; ')
    TM2 = {'T1': (71.69, 35.00, 42.0, 3612, 0.42, 65.53, 13.22, 79.67, 71.64), 'T2': (77.32, 36.45, 41.4, 3980, 0.43, 71.70, 14.58, 86.30, 80.32),
           'T3': (77.85, 36.80, 41.2, 4275, 0.43, 78.20, 14.82, 92.22, 85.16), 'T4': (78.90, 36.00, 41.4, 4395, 0.43, 81.30, 15.28, 94.01, 87.18)}
    for tag, tl, desc in ROWS:
        h = HEAD + f'CT = {tl} ({desc}) - ROW {tag}.'
        z, c = TM2['T1'], TM2[tl]
        add('PANICLE-SPIKE DENSITY', {'PSD_WCT': f'=ROUND({c[0]}/0.23,1)', 'PSD_WpZT': f'=ROUND({z[0]}/0.23,1)'},
            h + f' Table 2 effective tillers per m ROW LENGTH ({c[0]} vs {z[0]}) converted to per m2 with the 23 cm row spacing (DERIVED, / 0.23 - FLAG).', t=6,
            unit='no./m2 (effective tillers per m row / 0.23 m row spacing; DERIVED)', src='Table 2 (DERIVED)', meth='Effective tillers per m row length; 23 cm rows.')
        add('GRAINS PER PANICLE', {'GPP_WCT': c[1], 'GPP_WpZT': z[1]}, h + ' Table 2 grains per panicle (spike).', t=6, unit='grains per spike (wheat)', src='Table 2')
        add('1000-GRAIN WEIGHT', {'TGW_WCT': c[2], 'TGW_WpZT': z[2]}, h + ' Table 2 1000-grain weight.', t=6, unit='g', src='Table 2')
        add('YIELD', {'W STRAW_CT': f'=ROUND({c[3]}/1000,3)', 'W STRAW_pZT': f'=ROUND({z[3]}/1000,3)'},
            h + f' Table 2 wheat STRAW yield (kg/ha / 1000). Grain yield main effects (T1-T4 2683 / 3048 / 3255 / 3347) not entered - cell means in Table 6 rows. N main effect: grain 2742 vs 3426, straw 3820 vs 4320 kg/ha.',
            t=6, unit='t/ha (printed kg/ha / 1000)', src='Table 2')
        add('HARVEST INDEX', {'HI_WCT': c[4], 'HI_WpZT': z[4]}, h + ' Table 2 harvest index (printed ratio).', t=6, unit='ratio', src='Table 2')
        mu = 'Micro-Kjeldahl N; vanado-molybdo-phosphoric yellow colour P; flame photometer K (Jackson 1973); uptake = concentration x grain + straw yield.'
        add('N uptake', {'NU_CT': c[5], 'NU_pZT': z[5]}, h + ' Table 4 wheat N uptake (grain + straw).', t=6, unit='kg N/ha (wheat)', src='Table 4', meth=mu)
        add('P uptake', {'PU_CT': c[6], 'PU_pZT': z[6]}, h + ' Table 4 wheat P uptake (text speaks of P2O5 uptake - oxide vs element basis not stated, FLAG).', t=6,
            unit='kg/ha (wheat; P or P2O5 basis not stated)', src='Table 4', meth=mu)
        add('K uptake', {'KU_CT': c[7], 'KU_pZT': z[7]}, h + ' Table 4 wheat K uptake (text speaks of K2O uptake - basis not stated, FLAG).', t=6,
            unit='kg/ha (wheat; K or K2O basis not stated)', src='Table 4', meth=mu)
        add('WUE', {'WUE_WCT': f'=ROUND({c[8]}/10,3)', 'WUE_WpZT': f'=ROUND({z[8]}/10,3)'},
            h + f' Table 8 wheat water-use efficiency on TOTAL water use (irrigation 30 cm + profile contribution + effective rain; printed kg/ha-cm / 10). Total water use T1-T4 37.45 / 37.95 / 38.22 / 38.39 cm; profile contribution 5.90 / 6.40 / 6.67 / 6.84 cm.',
            t=6, unit='kg/ha/mm (total water use; printed kg/ha-cm / 10)', src='Table 8', meth='WUE = grain yield / total consumptive water use (irrigation + profile contribution + effective rain).')
    return out


TM = [
    ('M1 (puddling + transplanting)', 'Puddling, 27-day seedlings at 20 x 10 cm', 'Puddled TPR', 'T1-T4', 'Not stated', None, 'Rice phase of CT / pZT', 'Puddled rice (rule 124).', 'High', 'INCLUDED'),
    ('M2 (puddling + line-sown sprouted seed)', 'Wet direct seeding in rows on puddled soil', 'Puddled wet DSR', 'T1-T4', 'Not stated', None, 'Rice phase of CT / pZT', 'Puddled (rule 135).', 'High', 'INCLUDED'),
    ('M3 (line-sown sprouted seed without puddling)', 'Sprouted seed line-sown on unpuddled soil; tillage before sowing not stated', 'Unpuddled DSR (tillage not stated)', 'T1-T4', 'Not stated', None,
     'Rice phase of CT / pZT - FLAG', 'Unpuddled; ZT only if sown without tillage (rule 138) - not stated, pZT kept with FLAG.', 'Medium', 'INCLUDED'),
    ('T4 cultivator x2 + harrow + planking x2', 'Conventional seedbed', 'M1-M3', 'Conventional', 'Not stated', None, 'CT (row a)', 'Full conventional tillage.', 'High', 'INCLUDED'),
    ('T3 cultivator x2 + rotavator x1', 'Three passes incl. rotavator', 'M1-M3', 'Conventional (3 passes)', 'Not stated', None, 'CT (row b)', 'Rotary rule 13 (>= 2 passes).', 'High', 'INCLUDED'),
    ('T2 cultivator + rotavator once each', 'Two passes', 'M1-M3', 'Two passes', 'Not stated', None, 'CT (row c) - FLAG', 'Rotary rule 13 (2 passes = CT); paper refers to zero and minimum tillage - author may prefer pMT.', 'Medium', 'INCLUDED'),
    ('T1 no-tillage (zero-till drill)', 'Zero-till drill, wheat sown 10-12 days earlier', 'M1-M3', 'Zero tillage', 'Not stated', None, 'pZT', 'Puddled / unpuddled tilled rice + ZT wheat (rules 124 / 138).', 'Medium', 'INCLUDED'),
    ('I1-I4 irrigation schedules (rice)', 'Irrigation 1 / 3 / 5 / 7 days after disappearance of ponded water', 'n/a', 'n/a', 'n/a', None, 'Pooled', 'Rice factor; wheat values pooled over it.', 'High', 'INCLUDED (pooled)'),
    ('N1 80 / N2 120 kg N/ha (wheat)', 'Wheat N levels (sub-sub plots)', 'n/a', 'n/a', 'n/a', None, 'Pooled', 'Only pooled tillage values printed (FLAG).', 'High', 'INCLUDED (pooled)'),
]
STUDY_INFO = dict(estab=1999, yeardata='1999-2000 to 2001-02', years='3 (pooled means)', texture='Clay loam', rotation='Rice-wheat', wheatvar='HD 2285', ricevar='Mahamaya',
                  N='100 rice / 80 or 120 wheat', P='50 / 60 (P2O5)', K='30 / 40 (K2O)', residue='Not stated (manual harvest)',
                  irrigation='Rice: irrigation 1 / 3 / 5 / 7 days after disappearance of ponded water; wheat 0.9 IW:CPE, 6 cm per irrigation (5 irrigations, 30 cm)',
                  treatments='3 rice establishment x 4 irrigation (rice); 3 rice establishment x 4 wheat tillage x 2 N (wheat); split-split plot, 3 reps',
                  supp='None',
                  params=('Wheat grain yield cell means (rice establishment x tillage, Table 6) - CT (T4 / T3 / T2 rows a-c) vs pZT (T1) per rice method; tillage main effects: effective tillers (per m2 derived), '
                          'grains / spike, 1000-grain weight, straw yield, HI, N / P / K uptake, WUE (flagged)'),
                  notes=('NEW serial 326 (ext\\651.pdf). Single author S.S. Parihar. Site coordinates not reported - IGKV Bilaspur geocoded (FLAG). Soil low OC / N, medium P / K (values not printed). '
                         'RICE DATA NOT ON SHEETS (rice establishment M1 puddled TPR / M2 puddled line-sown / M3 unpuddled line-sown carry no tillage-code contrast; pooled over wheat tillage): '
                         'Table 1 effective tillers 277.0 / 276.3 / 269.4 per m2, filled grains 114.0 / 112.2 / 105.6, TGW 28.0 / 28.5 / 29.4 g, grain 5325 / 5149 / 4764, straw 5965 / 6065 / 5835 kg/ha, HI 0.47 / 0.46 / 0.45; '
                         'Table 3 rice uptake N 105.09 / 103.71 / 98.68, P 18.54 / 18.75 / 17.42, K 112.37 / 114.33 / 109.07 kg/ha; Table 5 grain yield M x irrigation; Table 7 water use 105.35 / 105.35 / 114.47 cm, '
                         'WUE 50.44 / 48.78 / 41.51 kg/ha-cm. Wheat by rice method (Table 2): grain 2980 / 3034 / 3236, straw 3935 / 4062 / 4212 kg/ha; uptake (Table 4) N 71.43 / 73.00 / 76.94; WUE (Table 8) 79.11 / 80.58 / 83.51. '
                         'Wheat T2 (cultivator + rotavator) coded CT under the rotary rule (2 passes) - FLAG.'))
SITES = [('TCB College of Agriculture research farm, Bilaspur', 'not reported', 'not reported', 22.08, 82.14, 'Geocoded (institution) - FLAG', 'ST', None)]
