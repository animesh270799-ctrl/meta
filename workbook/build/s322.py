"""Study 322 - Mishra J.S. & Singh V.P. 2012 Soil Tillage Res. 123:11-20 (ext 644): tillage sequence x weed control, dry-seeded rice-wheat, Jabalpur."""
from common import base, notes

ST = dict(
    no=322, serial=322, authors='Mishra J.S. & Singh V.P.', year=2012, journal='Soil & Tillage Research',
    ref=('Mishra J.S. & Singh V.P. (2012) Tillage and weed control effects on productivity of a dry seeded rice-wheat system on a Vertisol '
         'in Central India. Soil & Tillage Research 123:11-20, doi 10.1016/j.still.2012.02.003.'),
    doi='10.1016/j.still.2012.02.003',
    fert=('Rice: 120 N + 60 P2O5 + 40 K2O kg/ha (1/3 N + full P, K basal by drill, rest N at 35 and 60 DAS); dry-seeded rice Kranti, 80 kg/ha seed, 3rd week June; '
          'wheat: 120 N + 60 P2O5 + 40 K2O (1/2 N basal at 10 cm), WH 147 at 120 kg/ha, 3rd week Nov, 5 irrigations; glyphosate 1.0 kg/ha 1 week before seeding in ZT plots'),
    tmap=('Split plot, 3 reps, 4.5 x 10 m sub-plots, DWSR Jabalpur, est. June 2006. Main plots = tillage sequence (rice-wheat): ZT-ZT (zero-till dry-seeded rice with Pant zero-till drill + zero-till wheat) -> ZT ; '
          'CT-CT (tilled to 15 cm: 2 cultivator + 1 disc harrow + 1 rototiller pass, then drilled dry-seeded rice + same tillage for wheat) -> CT ; '
          'CT-ZT (tilled dry-seeded rice + zero-till wheat) -> pZT (rules 124 / 135 / 138: tilled DSR + ZT wheat) ; ZT-CT (zero-till rice + conventional wheat) -> EXCLUDED (reverse mismatch, rule 68). '
          'Residue not described for any treatment (manual harvest at 10-15 cm / 5-7 cm) -> no residue (rule 104). Sub-plots: weedy check, recommended herbicide, herbicide + 1 hand weeding - '
          'tillage MAIN EFFECTS only printed (pooled over the 3 weed-control levels incl. weedy check; no tillage x weed cell means) - rule 33 FLAG.'),
    details=('TREATMENTS IN PAPER: main plots ZT-ZT, CT-CT, ZT-CT, CT-ZT (rice-wheat tillage sequence); sub plots weedy check, recommended herbicide (pendimethalin 1.0 fb 2,4-D 0.5 kg/ha in rice; clodinafop 0.06 fb 2,4-D 0.5 in wheat), '
             'herbicide + 1 hand weeding (30 DAS rice / 35 DAS wheat); split plot, 3 reps. || MAPPING: '
             'ZT-ZT -> ZT: dry seeds drilled without tillage (Pant zero-till ferti-drill, inverted-T openers) in rice and wheat; glyphosate burndown [rice phase: zero-till dry-seeded; wheat phase: zero tillage; residue: not stated - No] | '
             'CT-CT -> CT: 2 field-cultivator passes + 1 disc harrow + 1 vertical-tine rototiller pass to 15 cm before both crops, conventional seed drill [rice phase: tilled dry-seeded (unpuddled); wheat phase: conventional; residue: No] | '
             'CT-ZT -> pZT: tilled dry-seeded rice + zero-till wheat [rice phase: tilled dry-seeded; wheat phase: zero tillage; residue: No] | '
             'ZT-CT -> EXCLUDED: zero-till rice + conventional wheat (RNT-WCT reverse mismatch) [rice phase: zero tillage; wheat phase: conventional; residue: No]'),
)
SITE = dict(country='India (Madhya Pradesh)', site='Directorate of Weed Science Research farm, Jabalpur', lat=23.15, lon=79.967, climate='ST',
            duration='0-3 Y', soil='LOAMY', CLAY=48.45, **{'RAIN FALL': 1386, 'ph (initial)': 7.3, 'soc (initial)': 5.4, 'Bdi': 1.63})
HEAD = ('Tillage MAIN EFFECT (pooled over weedy check, recommended herbicide and herbicide + 1 hand weeding - no tillage x weed cell means printed; rule 33 FLAG). '
        'ZT = ZT-ZT, CT = CT-CT, pZT = CT-ZT (tilled dry-seeded rice + ZT wheat); ZT-CT excluded (values in notes). Residue not described (rule 104).')
M_Y = 'Grain yield from 8 m2 in the centre of each plot at 14 % moisture; system productivity = rice + wheat grain yield of each year.'
M_E = 'Economics for 2008-09 (system): total variable cost (fixed costs excluded); gross return at MSP (rice 188.9, wheat 240 US$/Mg, main product only); net = gross - cost; B:C = gross / cost.'

# year: (rice yr, wheat yr), rice ZT, CT, pZT(CT-ZT), ZT-CT ; wheat ... ; system ...
Y = [('2006-07', (1.06, 1.31, 1.31, 1.06), (2.725, 1.910, 2.373, 1.850), (3.79, 3.22, 3.68, 2.91)),
     ('2007-08', (1.84, 2.26, 2.10, 2.16), (3.72, 3.80, 3.98, 3.92), (5.56, 6.06, 6.09, 6.08)),
     ('2008-09', (2.94, 2.35, 2.47, 2.59), (4.45, 3.86, 3.31, 3.62), (7.39, 6.21, 5.78, 6.21))]


def rows(B):
    st = ST
    out = []

    def add(sheet, vals, body, y=1, t=3, d=1, **kw):
        obs, nt = notes(st, body, y, t, d)
        v = base(st, SITE, kw)
        v.update(vals)
        v.update({'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
        out.append((sheet, B.add_row(sheet, v)))

    for yr, ri, wh, sy in Y:
        ryr = '20' + yr[2:4]
        add('YIELD', {'RICE YIELD_ZT': ri[0], 'RICE YIELD_CT': ri[1], 'RICE YIELD_pZT': ri[2],
                      'WYIELD_ZT': wh[0], 'WYIELD_CT': wh[1], 'WYIELD_pZT': wh[2],
                      'SYS YIELD_ZT': sy[0], 'SYS YIELD_CT': sy[1], 'SYS YIELD_pZT': sy[2],
                      'UNIT': 't/ha (Mg/ha, 14 % moisture)', 'Crop/season of sampling': f'Rice {ryr} (dry-seeded) + wheat {yr}; system = rice + wheat',
                      'Data source': 'Table 8', 'Method used (from paper)': M_Y},
            HEAD + f' Table 8 year {yr}. ZT-CT (excluded): rice {ri[3]}, wheat {wh[3]}, system {sy[3]} Mg/ha.'
            + (' Post-flowering drought in 2006 lowered rice yields.' if yr == '2006-07' else ''),
            **{'year of data collection/experiment': yr, 'YEAR OF DATA (duration)': yr})
    cs = 'Rice-wheat system 2008-09 (3rd year, end of experiment)'
    yd = {'year of data collection/experiment': '2008-09', 'YEAR OF DATA (duration)': '2008-09 (3rd year)'}
    cost = (537.3, 583.9, 545.9, 577.5); net = (1086.7, 786.1, 709.9, 780.5); bc = (2.97, 2.33, 2.27, 2.33)
    add('COST OF CULTIVATION', {'COST_SYSZT': cost[0], 'COST_SYSCT': cost[1], 'COST_SYSpZT': cost[2], 'UNIT': 'US$/ha (total VARIABLE cost; fixed cost excluded)',
                                'Crop/season of sampling': cs, 'Data source': 'Table 10', 'Method used (from paper)': M_E},
        HEAD + f' Table 10 total variable cost of the rice-wheat system. ZT-CT (excluded) {cost[3]}.', **yd)
    add('NET RETURN', {'NR_SYSZT': net[0], 'NR_SYSCT': net[1], 'NR_SYSpZT': net[2], 'UNIT': 'US$/ha (net income over variable cost)',
                       'Crop/season of sampling': cs, 'Data source': 'Table 10', 'Method used (from paper)': M_E},
        HEAD + f' Table 10 net income of the rice-wheat system. ZT-CT (excluded) {net[3]}.', **yd)
    add('GROSS RETURN', {'GR_SYSZT': f'=ROUND({cost[0]}+{net[0]},1)', 'GR_SYSCT': f'=ROUND({cost[1]}+{net[1]},1)', 'GR_SYSpZT': f'=ROUND({cost[2]}+{net[2]},1)',
                         'UNIT': 'US$/ha (DERIVED = variable cost + net income)', 'Crop/season of sampling': cs, 'Data source': 'Table 10 (derived)', 'Method used (from paper)': M_E},
        HEAD + ' Gross return DERIVED = cost + net income (gross / cost from it = 3.02 / 2.35 / 2.30 vs printed B:C 2.97 / 2.33 / 2.27).', **yd)
    add('BC ratio', {'BC_SYSZT': f'=ROUND({bc[0]}-1,2)', 'BC_SYSCT': f'=ROUND({bc[1]}-1,2)', 'BC_SYSpZT': f'=ROUND({bc[2]}-1,2)',
                     'UNIT': 'ratio (net / cost; printed gross / cost - 1, rule 57)', 'Crop/season of sampling': cs, 'Data source': 'Table 10 (converted)', 'Method used (from paper)': M_E},
        HEAD + f' Printed B:C (gross / cost) {bc[0]} / {bc[1]} / {bc[2]} (ZT-CT {bc[3]}); net / cost from cost and net income would be 2.02 / 1.35 / 1.30.', **yd)
    return out


TM = [
    ('ZT-ZT', 'Zero-till dry-seeded rice (Pant zero-till ferti-drill) followed by zero-till wheat; glyphosate 1.0 kg/ha one week before seeding.',
     'Zero-till dry-seeded', 'Zero tillage', 'Not stated (No)', None, 'ZT', 'No tillage in both phases; residue not described (rule 104).', 'High', 'INCLUDED'),
    ('CT-CT', 'Soil tilled to 15 cm (2 field-cultivator passes, 1 disc harrow, 1 vertical-tine rototiller pass) before drilling dry-seeded rice and again before wheat.',
     'Tilled dry-seeded (unpuddled)', 'Conventional', 'Not stated (No)', None, 'CT', 'Conventional tillage in both phases (rule 135: dry DSR + conventional wheat = CT).', 'High', 'INCLUDED'),
    ('CT-ZT', 'Tilled dry-seeded rice followed by zero-till wheat.', 'Tilled dry-seeded', 'Zero tillage', 'Not stated (No)', None, 'pZT',
     'Tilled DSR + ZT wheat = partial code pZT (rules 124 / 135 / 138).', 'High', 'INCLUDED'),
    ('ZT-CT', 'Zero-till dry-seeded rice followed by conventionally tilled wheat.', 'Zero-till dry-seeded', 'Conventional', 'Not stated (No)', None, 'EXCLUDED',
     'Reverse mismatch (no-till rice + conventional wheat, RNT-WCT) stays excluded (rule 68).', 'High', 'EXCLUDED'),
    ('Weed control (3 levels)', 'Weedy check, recommended herbicide, herbicide + 1 hand weeding (sub plots).', 'n/a', 'n/a', 'n/a', None, 'Pooled',
     'Only tillage main effects printed (pooled over weed control incl. weedy check) - rule 33 FLAG; T = 3 in Obs.', 'Medium', 'INCLUDED (pooled)'),
]

STUDY_INFO_EXTRA = dict(
    estab=2006, yeardata='2006-07 to 2008-09', years='3 (year-wise yields; economics 2008-09)', texture='Clay loam 0-15 cm (48.45 % clay; Typic Chromusterts), clay 15-75 cm',
    rotation='Dry-seeded rice-wheat', wheatvar='WH 147', ricevar='Kranti', N='120 rice / 120 wheat', P='60 P2O5 / 60 P2O5', K='40 K2O / 40 K2O',
    residue='Not described (manual harvest; rice cut at 10-15 cm, wheat at 5-7 cm)', irrigation='Rice rainfed + 2 irrigations at reproductive stage; wheat 5 irrigations (20, 40, 70, 90, 110 DAS)',
    treatments='4 tillage sequences (main) x 3 weed control (sub), split plot, 3 reps, 4.5 x 10 m',
    params='Rice, wheat and system grain yield per year 2006-09; system variable cost, net income, B:C (net/cost), gross return (derived) 2008-09 - tillage main effects (flagged)',
    supp='None referenced',
    notes=('NEW serial 322 (ext\\644.pdf). Only tillage main effects printed (pooled over weed control incl. weedy check) - FLAG. ZT-CT excluded (reverse mismatch). Not entered (no sheet): weed density / dry weight (Tables 4-7), '
           'weed seedbank by depth (Table 9), energy input / output (Table 10: ZT 33906 / 108672 MJ/ha, ratio 3.18; CT 38187 / 91272, 2.38; CT-ZT 35979 / 84961, 2.35; ZT-CT 35979 / 91287, 2.53). '
           'Yield attributes measured but not shown (data not shown). Initial soil 0-15 cm (Table 2): EC 0.22 dS/m, CEC 43 meq/100 g, avail. N 238, P 16.5, K 342 kg/ha, infiltration rate 1.85 mm/h, '
           'Ks 0.278 cm/h, FC 26.3 %, PWP 20.5 %, available water 5.8 % (site level, notes only). Weather Table 1.'),
)
