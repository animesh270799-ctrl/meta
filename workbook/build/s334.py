"""Study 334 - Singh G., Jalota S.K. & Sidhu B.S. 2005 Soil Use Manage. 21:17-21 (ext 674): rice-straw incorporated / burnt / removed, PAU Ludhiana, soil physics."""
from common import base, notes

ST = dict(
    no=334, serial=334, authors='Singh G., Jalota S.K. & Sidhu B.S.', year=2005, journal='Soil Use and Management',
    ref=('Singh G., Jalota S.K. & Sidhu B.S. (2005) Soil physical and hydraulic properties in a rice-wheat cropping system in India: effects of rice-straw management. '
         'Soil Use and Management 21:17-21, doi 10.1079/SUM2004285.'),
    doi='10.1079/SUM2004285',
    fert='Not stated; puddled rice; rice straw incorporated / burnt / removed before wheat',
    tmap=('CRBD, 4 reps, PAU Ludhiana long-term trial started 1996 (sandy loam). Rice-straw treatments before wheat: straw INCORPORATED (SI) -> CTR ; straw REMOVED (SR) -> CT (row a) ; straw BURNT (SB) -> CT (row b, '
          'rule 116). Wheat tillage not described - incorporation implies conventional tillage (FLAG); rice puddled in all plots. Soil sampled after the 5th rice and the 5th wheat crop.'),
    details=('TREATMENTS IN PAPER: rice straw incorporated (SI), burnt (SB) or removed (SR) before wheat (CRBD, 4 reps). || MAPPING: SR -> CT (row a) [rice: puddled; wheat: tillage implied; residue: removed] | '
             'SB -> CT (row b) [residue burnt, rule 116] | SI -> CTR [straw incorporated]'),
)
SITE = dict(country='India (Punjab)', site='Department of Soils research farm, PAU Ludhiana', lat=30.933, lon=75.867, climate='ST', duration='4-10 Y', soil='LOAMY')
LAY = [('0-5', 0), ('5-10', 1), ('10-15', 2)]
# per season: 'R' after rice harvest, 'W' after wheat harvest; values [SR, SB, SI] per layer
D = {
 'OC': {'R': ([0.44, 0.42, 0.39], [0.51, 0.47, 0.41], [0.62, 0.56, 0.48]), 'W': ([0.45, 0.43, 0.39], [0.49, 0.44, 0.40], [0.56, 0.51, 0.46])},
 'MWD': {'R': ([0.353, 0.222, 0.205], [0.526, 0.229, 0.202], [0.595, 0.276, 0.237]), 'W': ([0.227, 0.253, 0.205], [0.293, 0.257, 0.193], [0.332, 0.318, 0.254])},
 'AS': {'R': ([10.8, 6.8, 6.3], [18.6, 4.3, 7.1], [26.0, 9.6, 9.1]), 'W': ([7.4, 10.3, 7.8], [11.6, 8.9, 8.8], [16.7, 10.7, 10.1])},
 'TP': {'R': ([0.363, 0.366, 0.371], [0.378, 0.370, 0.356], [0.431, 0.399, 0.373]), 'W': ([0.377, 0.379, 0.374], [0.394, 0.384, 0.375], [0.414, 0.393, 0.383])},
 'BD': {'R': ([1.68, 1.69, 1.71], [1.65, 1.67, 1.71], [1.51, 1.59, 1.66]), 'W': ([1.65, 1.65, 1.66], [1.61, 1.63, 1.66], [1.55, 1.61, 1.63])},
 'DR': {'R': ([0.24, 0.25, 0.27], [0.20, 0.22, 0.26], [0.14, 0.18, 0.24]), 'W': ([0.19, 0.22, 0.24], [0.17, 0.20, 0.24], [0.14, 0.17, 0.22])},
 'MOR': {'R': ([8.43, 8.61, 8.77], [8.03, 8.50, 8.45], [6.27, 7.16, 7.98]), 'W': ([7.61, 7.74, 7.81], [7.43, 7.65, 8.03], [6.51, 7.16, 7.98])},
 'MAC': {'R': ([2.8, 1.5, 1.5], [1.7, 2.5, 3.2], [3.7, 3.1, 1.5]), 'W': ([6.5, 3.6, 4.1], [4.3, 2.5, 4.8], [8.6, 4.2, 7.6])},
 'MES': {'R': ([14.1, 8.8, 8.3], [12.0, 13.0, 6.2], [15.5, 10.6, 8.8]), 'W': ([1.9, 1.7, 4.0], [1.8, 2.9, 2.0], [8.1, 9.8, 9.6])},
 'MIC': {'R': ([19.4, 26.3, 27.3], [24.1, 21.5, 26.2], [23.9, 26.2, 27.0]), 'W': ([29.3, 32.6, 29.3], [33.3, 33.0, 30.7], [24.7, 25.3, 21.1])},
}
IR = {'R': (0.34, 0.34, 0.41), 'W': (0.72, 0.48, 0.73)}
AEV = {'R': (0.21, 0.20, 0.19), 'W': (0.13, 0.13, 0.11)}
ROWS = (('a', 0, 'CT = straw removed (SR), CTR = straw incorporated (SI)'), ('b', 1, 'CT = straw burnt (SB, rule 116), CTR = straw incorporated (SI)'))
MS = 'Clods (khurpa) at 5-cm increments for aggregation, BD, OC, dispersion ratio and modulus of rupture; cores (7.0 x 4.5 cm) for water retention; methods of Jalota et al. (1998).'


def rows(B):
    st = ST; out = []

    def add(sheet, vals, body, season, unit, src, depth, d=3, meth=MS):
        red = season == 'R'
        lab = 'after the 5th RICE harvest (RICE-SEASON ROW, whole row red, rule 79)' if red else 'after the 5th WHEAT harvest'
        obs, nt = notes(st, body + f' Soil sampled {lab}. Wheat tillage not described (incorporation implies tillage) - FLAG.', d=d, t=1)
        yd = 'after rice 2000 (5th crop; year inferred - FLAG)' if red else 'after wheat 2000-01 (5th crop; year inferred - FLAG)'
        v = base(st, SITE, {'year of data collection/experiment': yd, 'YEAR OF DATA (duration)': '5 yr'})
        v.update({'DEPTH': depth[1], 'DEPTH (as reported in paper)': depth[0]})
        v.update(vals)
        v.update({'UNIT': unit, 'Crop/season of sampling': ('RICE SEASON - soil after the 5th rice harvest' if red else 'Soil after the 5th wheat harvest'), 'Data source': src,
                  'Method used (from paper)': meth, 'Obs': obs, 'Rep': 4, 'Notes/Doubts': nt})
        out.append((sheet, B.add_row(sheet, v, red=red)))

    P = (('SOC(active C pool)', 'SOC_', 'OC', '=ROUND({}*10,2)', 'g/kg (Walkley-Black; printed % x 10)', 'Table 1', 'Table 1 organic carbon'),
         ('MWD 1', 'MWD_', 'MWD', None, 'mm (wet sieving)', 'Table 1', 'Table 1 mean weight diameter'),
         ('AGGREGATE STABILITY', 'AS_', 'AS', None, '% (aggregate stability = (water-stable aggregates >0.25 mm - sand >0.25 mm) / (sample - sand >0.25 mm) x 100)', 'Table 1', 'Table 1 aggregate stability'),
         ('POROSITY', 'POROSITY_', 'TP', '=ROUND({}*100,1)', '% v/v (printed fraction x 100; 1 - BD / PD)', 'Table 2', 'Table 2 total porosity'),
         ('BD', 'BD_', 'BD', None, 'Mg/m3', 'Table 2', 'Table 2 bulk density (clods)'),
         ('macro pore', 'MACROPORE_', 'MAC', None, '% (macropores >0.1 mm, from water retention)', 'Table 3', 'Table 3 macropores (>0.1 mm)'),
         ('meso pore', 'MESOPORE_', 'MES', None, '% (mesopores 0.1-0.03 mm)', 'Table 3', 'Table 3 mesopores (0.1-0.03 mm)'),
         ('micro pore', 'MICROPORE_', 'MIC', None, '% (micropores <0.03 mm)', 'Table 3', 'Table 3 micropores (<0.03 mm)'))
    for season in ('R', 'W'):
        for tag, ci, lab in ROWS:
            for sheet, pre, key, fmt, unit, src, txt in P:
                for ly, i in LAY:
                    ct = D[key][season][ci][i]; ctr = D[key][season][2][i]
                    f = (lambda x: fmt.format(x)) if fmt else (lambda x: x)
                    extra = ''
                    if key == 'OC':
                        extra = (f' Dispersion ratio (no sheet) SR / SB / SI {D["DR"][season][0][i]} / {D["DR"][season][1][i]} / {D["DR"][season][2][i]}; modulus of rupture (10^-4 kPa as printed, no sheet) '
                                 f'{D["MOR"][season][0][i]} / {D["MOR"][season][1][i]} / {D["MOR"][season][2][i]}.')
                    add(sheet, {f'{pre}CT': f(ct), f'{pre}CTR': f(ctr)}, f'ROW {tag}: {lab}. {txt}, {ly} cm.' + extra, season, unit, src, (f'{ly} cm', '0-15 CM'))
            add('IR', {'IR_CT': IR[season][ci], 'IR_CTR': IR[season][2]},
                f'ROW {tag}: {lab}. Table 4 infiltration rate after 5 h (double ring). Air entry value (no sheet) SR / SB / SI {AEV[season][0]} / {AEV[season][1]} / {AEV[season][2]} m.',
                season, 'cm/hr (rate after 5 h, double ring)', 'Table 4', ('surface (double ring)', '0-15 CM'), d=1, meth='Double-ring infiltrometer in situ (Bertrand 1965).')
    return out


TM = [
    ('SR (straw removed)', 'Rice straw removed before wheat', 'Puddled', 'Not described (tillage implied)', 'No', '0', 'CT (row a)', 'Residue removed.', 'Medium', 'INCLUDED'),
    ('SB (straw burnt)', 'Rice straw burnt before wheat', 'Puddled', 'Not described', 'Burnt', '0', 'CT (row b)', 'Burnt = no residue (rule 116).', 'Medium', 'INCLUDED'),
    ('SI (straw incorporated)', 'Rice straw incorporated before wheat', 'Puddled', 'Tillage incorporating straw (implied)', 'Yes (incorporated)', None, 'CTR', 'Incorporation implies tillage - FLAG.', 'Medium', 'INCLUDED'),
]
STUDY_INFO = dict(estab=1996, yeardata='After the 5th rice and 5th wheat crop (c. 2000 / 2000-01)', years='2 samplings', texture='Sandy loam, Typic Ustochrept', rotation='Rice-wheat',
                  wheatvar='Not reported', ricevar='Not reported', N='Not stated', P='Not stated', K='Not stated', residue='Rice straw incorporated / burnt / removed', irrigation='Not stated',
                  treatments='3 rice-straw managements (CRBD, 4 reps)', supp='None',
                  params=('Rows a (SR) / b (SB) CT vs CTR (SI), 0-5 / 5-10 / 10-15 cm, after rice (red) and after wheat: SOC, MWD, aggregate stability, total porosity, BD, macro / meso / micro pores; '
                          'infiltration rate'),
                  notes=('NEW serial 334 (ext\\674.pdf). Wheat tillage not described (straw incorporation implies conventional tillage) - FLAG. Sampling years inferred from "after the fifth crop" (trial since 1996). '
                         'NOT ON A SHEET: dispersion ratio and modulus of rupture (in SOC notes), air-entry value (in IR notes), water-retention curves (Fig. 1) and cumulative infiltration curves (Fig. 2).'))
SITES = [('PAU Department of Soils farm, Ludhiana', "30 56' N", "75 52' E", 30.933, 75.867, 'Paper', 'ST', None)]
