"""Study 325 - Pandey B.P. & Kandel T.P. 2020 Agronomy 10:1734 (ext 650): rice CT (puddled TPR) vs ZT DSR x wheat residue x weeding, NWRP Bhairahawa."""
from common import base, notes

ST = dict(
    no=325, serial=325, authors='Pandey B.P. & Kandel T.P.', year=2020, journal='Agronomy',
    ref=('Pandey B.P. & Kandel T.P. (2020) Response of rice to tillage, wheat residue and weed management in a rice-wheat cropping system. '
         'Agronomy 10(11):1734, doi 10.3390/agronomy10111734.'),
    doi='10.3390/agronomy10111734',
    fert='Rice Sabitri, 20 x 20 cm; 100:30:30 N:P:K kg/ha (half N + full P, K at planting; N splits 25 and 45 DAT/DAS); glyphosate 1 kg a.i./ha before ZT sowing; 3-5 irrigations',
    tmap=('Nested split-split plot, 3 reps (4 x 4 m), NWRP Bhairahawa, rice 2014-2016. Main: CT = rice transplanted on puddled field after conventional tillage ; ZT = rice direct-seeded on zero-tilled soil. '
          'Sub: wheat residue whole (WR, chopped mulch) / partial (PR, 20 cm stubble) / none (NR); sub-sub: manual vs chemical (bispyribac-sodium) weeding. '
          'Only MAIN EFFECTS printed: tillage CT vs ZT pooled over residue (incl. WR / PR residue in both) and weeding (FLAG, rule 33). Wheat phase NOT described - rice-phase coding (FLAG, as study 318).'),
    details=('TREATMENTS IN PAPER: tillage CT (puddled TPR) / ZT (zero-till DSR) x wheat residue WR / PR / NR x weed management MW / CW (12 combinations, 3 reps). || MAPPING: '
             'CT -> CT: conventional tillage and puddling, transplanted rice [rice phase: puddled TPR; wheat phase: not described; residue: pooled over WR / PR / NR] | '
             'ZT -> ZT: direct seeding into zero-tilled soil [rice phase: zero-till DSR; wheat phase: not described; residue: pooled] | residue and weeding main effects pooled over tillage -> notes'),
)
SITE = dict(country='Nepal', site='National Wheat Research Program (NWRP) farm, Bhairahawa, Rupandehi', lat=27.530, lon=83.460, climate='ST', duration='0-3 Y', soil='LOAMY',
            **{'ph (initial)': 7.9, 'soc (initial)': 14.5, 'MAX TEMP': 33.8, 'MIN TEMP': 24.0})
YRS = {1: '2014', 2: '2015', 3: '2016'}
RAIN = {1: 1234, 2: 870, 3: 1684}
# CT, ZT per year
D = {
 'PLH': ([98.4, 105.5, 106.0], [97.6, 104.1, 104.8], 'Table 2 plant height at physiological maturity', 'PLANT HEIGHT', 'cm (rice, at physiological maturity)'),
 'PSD': ([261.4, 329.8, 289.8], [244.5, 288.8, 271.2], 'Table 2 effective tillers per m2 at physiological maturity (= panicles)', 'PANICLE-SPIKE DENSITY', 'no./m2 (effective tillers = panicles, rice)'),
 'DTF': ([112.0, 113.3, 109.3], [112.4, 113.8, 109.4], 'Table 3 days to HEADING (75 % of plants; CT counted from seed soaking, ZT from sowing - FLAG; heading entered as flowering)', 'DAYS TO FLOWERING', 'days to heading (rice; CT from seed soaking, ZT from sowing)'),
 'DTM': ([140.8, 140.4, 139.1], [141.2, 141.1, 140.1], 'Table 3 days to physiological maturity (CT from seed soaking, ZT from sowing - FLAG)', 'DAYS TO MATURITY', 'days to physiological maturity (rice)'),
 'SPL': ([21.0, 21.2, 21.6], [21.4, 21.7, 22.5], 'Table 4 ear-head (panicle) length', 'PANICLE-SPIKE LENGTH', 'cm (rice panicle length)'),
 'GPP': ([113.4, 157.2, 121.4], [119.9, 158.9, 122.5], 'Table 4 grains per ear-head (panicle)', 'GRAINS PER PANICLE', 'grains per panicle (rice)'),
 'TGW': ([21.6, 19.0, 22.1], [22.0, 19.9, 22.8], 'Table 5 1000-grain weight', '1000-GRAIN WEIGHT', 'g'),
}
GY = ([4.8, 4.6, 5.0], [4.3, 4.3, 4.5])
AVG = {'PLH': (103.3, 102.1), 'PSD': (293.7, 268.2), 'DTF': (111.5, 111.9), 'DTM': (140.1, 140.8), 'SPL': (21.3, 21.9), 'GPP': (130.7, 133.8), 'TGW': (20.9, 21.6), 'GY': (4.8, 4.4)}
RES = {'GY': 'WR 4.9 / 4.7 / 5.1, PR 4.6 / 4.5 / 4.8, NR 4.3 / 4.2 / 4.4 t/ha', 'PLH': 'WR 98.8 / 106.4 / 106.6, PR 98.0 / 104.9 / 105.2, NR 97.2 / 103.0 / 104.4 cm'}
HEAD = ('CT = puddled transplanted rice (conventional tillage), ZT = zero-till direct-seeded rice. TILLAGE MAIN EFFECT pooled over wheat-residue levels (WR / PR / NR) and weeding (MW / CW) - FLAG (rule 33; no cell means printed). '
        'RICE-SEASON ROW (whole row red; rice-only paper of a rice-wheat system, rule 31 exception). WHEAT PHASE NOT DESCRIBED - rice-phase coding (FLAG, as study 318).')
M = 'Phenology on 50 marked plants; height, panicle length and grains / panicle on 10 plants at maturity; effective tillers in 1 m2; grain from 9.6 m2 net plot at 14 % moisture; 1000-grain weight.'


def rows(B):
    st = ST; out = []
    for k in (1, 2, 3):
        yr = YRS[k]
        cs = f'RICE SEASON {yr} (Year-{k}; June-November)'
        for key, (ct, zt, txt, sheet, unit) in D.items():
            pre = {'PLH': 'PLH_R', 'PSD': 'PSD_R', 'DTF': 'DTF_R', 'DTM': 'DTM_R', 'SPL': 'SPL_R', 'GPP': 'GPP_R', 'TGW': 'TGW_R'}[key]
            body = HEAD + f' {txt}, Year-{k} ({yr}); 3-yr average CT {AVG[key][0]}, ZT {AVG[key][1]} (notes).' + (f' Residue main effect (pooled over tillage) years 1-3: {RES[key]}.' if key in RES else '')
            obs, nt = notes(st, body, t=6)
            v = base(st, SITE, {'year of data collection/experiment': yr, 'YEAR OF DATA (duration)': f'rice {yr}', 'RAIN FALL': RAIN[k]})
            v.update({f'{pre}CT': ct[k - 1], f'{pre}ZT': zt[k - 1], 'UNIT': unit, 'Crop/season of sampling': cs, 'Data source': txt.split(' ')[0] + ' ' + txt.split(' ')[1],
                      'Method used (from paper)': M, 'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
            out.append((sheet, B.add_row(sheet, v, red=True)))
        body = HEAD + f' Table 6 rice grain yield (14 % moisture), Year-{k} ({yr}); 3-yr average CT 4.8, ZT 4.4. Residue main effect (pooled over tillage): {RES["GY"]}; weeding MW 4.6 / 4.5 / 4.9 vs CW 4.5 / 4.4 / 4.7 t/ha.'
        obs, nt = notes(st, body, t=6)
        v = base(st, SITE, {'year of data collection/experiment': yr, 'YEAR OF DATA (duration)': f'rice {yr}', 'RAIN FALL': RAIN[k]})
        v.update({'RICE YIELD_CT': GY[0][k - 1], 'RICE YIELD_ZT': GY[1][k - 1], 'UNIT': 't/ha (14 % moisture)', 'Crop/season of sampling': cs, 'Data source': 'Table 6',
                  'Method used (from paper)': M, 'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
        out.append(('YIELD', B.add_row('YIELD', v, red=True)))
    return out


TM = [
    ('CT (conventional tillage, puddled TPR)', 'Rice transplanted (2-3 seedlings / hill, 20 x 20 cm) on puddled field after conventional tillage', 'Puddled TPR', 'Not described', 'Pooled (WR / PR / NR)', None, 'CT', 'Rice-phase coding; wheat phase not described (FLAG, as 318).', 'Medium', 'INCLUDED'),
    ('ZT (zero tillage DSR)', 'Rice direct-seeded on zero-tilled soil after glyphosate', 'Zero-till DSR', 'Not described', 'Pooled', None, 'ZT', 'No-till DSR; residue levels pooled (FLAG).', 'Medium', 'INCLUDED'),
    ('WR / PR / NR wheat residue', 'Whole residue as mulch / 20 cm stubble / removed (sub plots)', 'n/a', 'n/a', 'Yes / partial / No', None, 'Pooled', 'Only main effects printed (no tillage x residue cells) - residue effects in notes.', 'Medium', 'INCLUDED (pooled)'),
    ('MW / CW weeding', 'Manual vs bispyribac-sodium (sub-sub plots)', 'n/a', 'n/a', 'n/a', None, 'Pooled', 'Pooled (T = 6 cells per tillage mean).', 'High', 'INCLUDED (pooled)'),
]
STUDY_INFO = dict(estab=2014, yeardata='Rice 2014, 2015, 2016', years='3 (year-wise)', texture='Silt loam to silty clay loam', rotation='Rice-wheat (wheat phase not described)', wheatvar='Not reported',
                  ricevar='Sabitri', N='100', P='30 (P)', K='30 (K)', residue='Wheat residue WR (chopped mulch) / PR (20 cm stubble) / NR', irrigation='3-5 flood irrigations (5-7 cm) per season',
                  treatments='2 tillage x 3 residue x 2 weeding, nested split-split plot, 3 reps', supp='Supplementary Table S1 (field operation timelines) and Fig. S1 (weather) - not downloaded (permission needed); no outcome data',
                  params='RED rice rows 2014-16: grain yield, plant height, effective tillers, days to heading and maturity, panicle length, grains / panicle, 1000-grain weight - CT vs ZT tillage main effects (flagged)',
                  notes=('NEW serial 325 (ext\\650.pdf). Rice-season-only paper; wheat phase not described (rice-phase coding, FLAG). Tillage main effects only (pooled over residue and weeding). '
                         'Soil: SOM 2.5 % (SOC 14.5 g/kg derived / 1.724), total N 0.14 %, pH 7.9. Growing-season rainfall 1234 / 870 / 1684 mm (long-term 1550).'))
SITES = [('NWRP farm, Bhairahawa', "27 31' 49\" N", "83 27' 36\" E", 27.530, 83.460, 'Paper', 'ST', None)]
