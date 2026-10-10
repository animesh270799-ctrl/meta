"""Study 328 - Sharma M.K., Sharma R.P. & Kumar R. 2007 J. Appl. Biol. 17(1-2):56-60 (ext 653): rice establishment x wheat tillage, BAC Sabour."""
from common import base, notes

ST = dict(
    no=328, serial=328, authors='Sharma M.K., Sharma R.P. & Kumar R.', year=2007, journal='Journal of Applied Biology',
    ref=('Sharma M.K., Sharma R.P. & Kumar R. (2007) Productivity and economics of rice-wheat cropping system as affected by crop establishment methods and tillage practices. '
         'Journal of Applied Biology 17(1-2):56-60.'),
    doi=None,
    fert='Rice MTU 7029: 100 N + 40 P2O5 + 20 K2O kg/ha; wheat HD 2733: 120 N + 60 P2O5 + 40 K2O kg/ha; butachlor in rice, isoproturon + 2 hand weedings; wheat rows 20 cm (CT), 18 cm (ZT / strip), 12 cm (beds)',
    tmap=('Split plot, 3 reps, BAC Sabour 2003-04 to 2005-06. Main: rice establishment (direct dry sowing by zero-till drill; wet seeding of sprouted seed on PUDDLED soil by drum seeder; manual transplanting; '
          'self-propelled transplanter (SPT) - both puddled); sub (after rice): wheat conventional (2 harrowings + 2 cultivator passes + planking), zero-till drill, strip-till drill, bed planting. '
          'Only MAIN EFFECTS printed (interaction NS). Zero-till drill -> pZT and strip-till drill -> pMT (pooled over 3 puddled + 1 zero-till DSR rice methods; majority puddled, rule 124 - FLAG). '
          'Conventional-wheat main effect NOT ENTERED: pooled over the excluded zero-till DSR + conventional wheat combination (rule 65) - Notes. Bed planting (beds made after the conventional '
          'preparation) EXCLUDED (planting-geometry treatment; same tillage as CT). Rice-establishment main effects -> Notes (ZT-DSR pooled over conventional wheat, rule 65).'),
    details=('TREATMENTS IN PAPER: rice (main) direct dry sowing by ZT drill / drum-seeder wet seeding on puddled soil / manual transplanting / SPT transplanting x wheat (sub) conventional / zero-till drill / '
             'strip-till drill / bed planting (split plot, 3 reps). || MAPPING: zero-till drill -> pZT [rice phase: pooled 3 puddled + 1 ZT-DSR; wheat: ZT drill; residue: not stated] | '
             'strip-till drill -> pMT [rice phase: pooled; wheat: strip till; residue: not stated] | conventional -> CT NOT ENTERED (rule 65) | bed planting -> EXCLUDED | rice methods -> Notes'),
)
SITE = dict(country='India (Bihar)', site='Research farm, Bihar Agricultural College, Sabour, Bhagalpur', lat=25.233, lon=87.067, climate='ST', duration='0-3 Y', soil='LOAMY',
            **{'ph (initial)': 7.8, 'soc (initial)': 4.7})
HEAD = ('pZT = zero-till drill wheat, pMT = strip-till drill wheat. WHEAT-TILLAGE MAIN EFFECTS pooled over 4 rice establishment methods (ZT-DSR, puddled drum-seeded, manual and SPT puddled transplanting) - '
        'FLAG (rule 33; partial codes because 3 of 4 rice methods are puddled - FLAG). Conventional wheat NOT entered (pooled over excluded ZT-DSR + CT wheat cell, rule 65): ')
YD = '3-yr mean (2003-04 to 2005-06)'
M = 'Grain and straw yields from net plot; rice-equivalent yield, net return and B:C on 3-yr pooled data; NPK uptake (grain + straw).'


def rows(B):
    st = ST; out = []

    def add(sheet, vals, body, unit, src, crop):
        obs, nt = notes(st, HEAD + body, y=3, t=4)
        v = base(st, SITE, {'year of data collection/experiment': '2003-2006', 'YEAR OF DATA (duration)': YD})
        v.update(vals)
        v.update({'UNIT': unit, 'Crop/season of sampling': crop, 'Data source': src, 'Method used (from paper)': M, 'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
        out.append((sheet, B.add_row(sheet, v)))

    # order: CT, ZT, strip, bed
    W = {'PSD': ([333, 315, 361, 354], 'PANICLE-SPIKE DENSITY', 'PSD_W', 'no./m2 (effective tillers = spikes)', 'Table 3 wheat effective tillers per m2'),
         'GPP': ([45.1, 42.8, 46.3, 46.0], 'GRAINS PER PANICLE', 'GPP_W', 'filled grains per spike', 'Table 3 wheat filled grains per spike'),
         'TGW': ([37.22, 36.18, 37.80, 37.74], '1000-GRAIN WEIGHT', 'TGW_W', 'g', 'Table 3 wheat 1000-grain weight')}
    R = {'PSD': ([311, 305, 318, 312], 'PSD_R', 'Table 2 rice effective tillers per m2'),
         'GPP': ([130.4, 127.8, 133.4, 131.1], 'GPP_R', 'Table 2 rice filled grains per panicle'),
         'TGW': ([19.87, 19.77, 20.55, 20.52], 'TGW_R', 'Table 2 rice 1000-grain weight')}
    RNOTE = (' RICE values = rice grown on the wheat-tillage sub plots (residual effect; the first rice season preceded the wheat treatments - FLAG). Wheat-tillage effects on rice NS.')
    for k, (v_, sheet, pre, unit, txt) in W.items():
        rv, rpre, rtxt = R[k]
        add(sheet, {f'{pre}pZT': v_[1], f'{pre}pMT': v_[2], f'{rpre}pZT': rv[1], f'{rpre}pMT': rv[2]},
            f'CT {v_[0]} (rice {rv[0]}), bed planting {v_[3]} (rice {rv[3]}). {txt} and {rtxt}.' + RNOTE, unit if k != 'GPP' else 'grains per spike (wheat) / panicle (rice)', 'Tables 2-3',
            'Wheat and rice, 3-yr mean')
    GYW = [41.02, 36.73, 45.31, 43.24]; SYW = [56.66, 51.14, 62.06, 59.00]; GYR = [56.35, 55.37, 57.39, 57.16]; SYR = [78.20, 76.37, 78.91, 79.59]; REY = [111.48, 105.36, 118.02, 115.14]
    add('YIELD', {**{f'WYIELD_{c}': f'=ROUND({GYW[i]}/10,3)' for c, i in (('pZT', 1), ('pMT', 2))}, **{f'W STRAW_{c}': f'=ROUND({SYW[i]}/10,3)' for c, i in (('pZT', 1), ('pMT', 2))},
                  **{f'RICE YIELD_{c}': f'=ROUND({GYR[i]}/10,3)' for c, i in (('pZT', 1), ('pMT', 2))}, **{f'RSTRAW_{c}': f'=ROUND({SYR[i]}/10,3)' for c, i in (('pZT', 1), ('pMT', 2))},
                  **{f'SYS YIELD_{c}': f'=ROUND({REY[i]}/10,3)' for c, i in (('pZT', 1), ('pMT', 2))}},
        f'CT: wheat grain {GYW[0]}, straw {SYW[0]}; rice grain {GYR[0]}, straw {SYR[0]}; REY {REY[0]} q/ha. Bed planting: wheat {GYW[3]} / {SYW[3]}, rice {GYR[3]} / {SYR[3]}, REY {REY[3]} q/ha. '
        'Tables 2-4 grain and straw yields (q/ha / 10); SYS = rice-equivalent yield of the system (Table 4; rule 54 FLAG).' + RNOTE, 't/ha (printed q/ha / 10)', 'Tables 2-4', 'Wheat, rice and system, 3-yr mean')
    GR = [71721, 68014, 75632, 74768]; NR = [40807, 39072, 45619, 43872]; BC = [1.32, 1.35, 1.52, 1.42]
    eco = f' CT gross {GR[0]}, net {NR[0]}, B:C {BC[0]}; bed planting {GR[3]}, {NR[3]}, {BC[3]}.'
    add('GROSS RETURN', {'GR_SYSpZT': GR[1], 'GR_SYSpMT': GR[2]}, 'Table 4 system gross return.' + eco, 'Rs/ha (rice-wheat system)', 'Table 4', 'System, 3-yr mean')
    add('NET RETURN', {'NR_SYSpZT': NR[1], 'NR_SYSpMT': NR[2]}, 'Table 4 system net return.' + eco, 'Rs/ha (rice-wheat system)', 'Table 4', 'System, 3-yr mean')
    add('COST OF CULTIVATION', {'COST_SYSpZT': f'={GR[1]}-{NR[1]}', 'COST_SYSpMT': f'={GR[2]}-{NR[2]}'}, 'System cost of cultivation DERIVED = gross - net return (Table 4).' + eco,
        'Rs/ha (rice-wheat system; DERIVED gross - net)', 'Table 4 (DERIVED)', 'System, 3-yr mean')
    add('BC ratio', {'BC_SYSpZT': BC[1], 'BC_SYSpMT': BC[2]}, 'Table 4 B:C as printed (= net / cost: 39072 / (68014 - 39072) = 1.35, rule 57 check).' + eco, 'ratio (net / cost, as printed)', 'Table 4',
        'System, 3-yr mean')
    UP = {'N uptake': ('NU_SYS', [194.0, 184.8, 212.2, 198.2], 'kg N/ha (rice + wheat)'), 'P uptake': ('PU_SYS', [40.2, 38.3, 46.1, 44.0], 'kg/ha (rice + wheat; P or P2O5 basis not stated)'),
          'K uptake': ('KU_SYS', [246.0, 233.8, 275.1, 261.9], 'kg/ha (rice + wheat; K or K2O basis not stated)')}
    for sheet, (pre, v_, unit) in UP.items():
        add(sheet, {f'{pre}pZT': v_[1], f'{pre}pMT': v_[2]}, f'Table 4 system (rice + wheat) {sheet}. CT {v_[0]}, bed planting {v_[3]}.', unit, 'Table 4', 'System, 3-yr mean')
    return out


TM = [
    ('Direct dry sowing by zero-till drill (rice)', 'Dry seeding with ZT drill, 60 kg/ha', 'Zero-till DSR', 'Wheat sub plots', 'Not stated', None, 'Pooled (rice main plot)', 'Rice factor; ZT-DSR + CT wheat would be excluded (rule 65).', 'High', 'INCLUDED (pooled)'),
    ('Wet seeding on puddled soil by drum seeder', 'Sprouted seed, drum seeder, puddled soil', 'Puddled wet DSR', 'Wheat sub plots', 'Not stated', None, 'Pooled (rice main plot)', 'Puddled (rule 135).', 'High', 'INCLUDED (pooled)'),
    ('Manual transplanting', '25-day seedlings, 20 x 10 cm, puddled', 'Puddled TPR', 'Wheat sub plots', 'Not stated', None, 'Pooled (rice main plot)', 'Puddled.', 'High', 'INCLUDED (pooled)'),
    ('Transplanting by self-propelled transplanter (SPT)', '18-day mat seedlings, puddled', 'Puddled machine TPR', 'Wheat sub plots', 'Not stated', None, 'Pooled (rice main plot)', 'Puddled.', 'High', 'INCLUDED (pooled)'),
    ('Conventional tillage (wheat)', '2 harrowings + 2 cultivator passes + 1 planking', 'Pooled rice methods', 'Conventional', 'Not stated', None, 'NOT ENTERED (rule 65)',
     'Main effect pooled over the excluded ZT-DSR + conventional wheat combination; values in Notes.', 'High', 'NOTES ONLY'),
    ('Zero-till drill (wheat)', 'Direct drilling without land preparation', 'Pooled (3 puddled + ZT-DSR)', 'Zero tillage', 'Not stated', None, 'pZT - FLAG', 'Majority puddled rice (rule 124); pooled main effect.', 'Medium', 'INCLUDED'),
    ('Strip-till drill (wheat)', 'Strip-till drill without land preparation', 'Pooled (3 puddled + ZT-DSR)', 'Strip tillage', 'Not stated', None, 'pMT - FLAG', 'Strip till after puddled rice (rule 124); pooled main effect.', 'Medium', 'INCLUDED'),
    ('Bed planting (wheat)', 'Beds after 2 harrowings + 2 cultivator passes + planking, 12 cm rows', 'Pooled', 'Conventional + beds', 'Not stated', None, 'EXCLUDED',
     'Planting geometry change on conventionally tilled land (as study 6 flat beds); values in Notes.', 'Medium', 'EXCLUDED'),
]
STUDY_INFO = dict(estab=2003, yeardata='2003-04 to 2005-06', years='3 (pooled means)', texture='Clay loam', rotation='Rice-wheat', wheatvar='HD 2733', ricevar='MTU 7029',
                  N='100 rice / 120 wheat', P='40 / 60 (P2O5)', K='20 / 40 (K2O)', residue='Not stated', irrigation='Not detailed',
                  treatments='4 rice establishment (main) x 4 wheat tillage / sowing (sub), split plot, 3 reps', supp='None',
                  params=('Wheat-tillage main effects pZT (zero-till drill) vs pMT (strip-till drill): wheat and rice effective tillers, grains, TGW, grain and straw yield; system REY, gross / net return, '
                          'cost (derived), B:C, system N / P / K uptake (flagged)'),
                  notes=('NEW serial 328 (ext\\653.pdf, scanned CABI copy read from page images). Only main effects printed. CONVENTIONAL WHEAT not entered (rule 65: pooled over the excluded zero-till DSR + '
                         'conventional wheat cell) - author may prefer entering CT flagged. Bed planting excluded (beds on conventionally tilled land). '
                         'RICE ESTABLISHMENT MAIN EFFECTS (Notes only; ZT-DSR / drum seeding on puddled soil / manual TPR / SPT): rice tillers 285 / 304 / 321 / 328 per m2, grains 128.4 / 132.2 / 137.9 / 136.2, '
                         'TGW 19.98 / 20.26 / 21.27 / 20.61 g, grain 52.34 / 54.73 / 59.75 / 59.48 q/ha, straw 71.76 / 74.52 / 81.33 / 81.04 q/ha; following wheat tillers 348 / 330 / 343 / 346, grains 45.2 / 44.8 / 45.0 / 45.3, '
                         'TGW 37.71 / 36.64 / 36.70 / 37.89 g, grain 42.51 / 40.95 / 41.49 / 42.25 q/ha, straw 58.93 / 56.77 / 57.33 / 58.51 q/ha; REY 109.75 / 110.14 / 115.49 / 116.23 q/ha; gross 69120 / 70292 / 74370 / 74871, '
                         'net 40908 / 41484 / 42035 / 44559 Rs/ha, B:C 1.45 / 1.44 / 1.30 / 1.47; system uptake N 185.7 / 189.7 / 204.2 / 205.3, P 39.3 / 39.2 / 44.5 / 44.9, K 189.9 / 245.6 / 261.1 / 267.7 kg/ha. '
                         'Rice durations: DSR 148, manual TPR 153, SPT 154 days; wheat ZT / strip sown 20-22 Nov (134 d) vs CT / beds 1-4 Dec (129 d) - sowing date confounded with tillage (FLAG). '
                         'Soil clay loam, OC 0.47 %, available N 168, P2O5 24.2, K2O 115 kg/ha, pH 7.8.'))
SITES = [('Bihar Agricultural College research farm, Sabour', 'not reported', 'not reported', 25.233, 87.067, 'As study 165 (BAU Sabour)', 'ST', None)]
