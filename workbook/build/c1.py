"""1 (companion 5) - Sharma S., Vashisht B.B., Singh P. & Singh Y. 2023 Biomass Convers. Biorefin. 13:13977-13994 (ext 670): PAU CA trial of study 1, April 2017 sampling."""
from common import base, notes

ST = dict(
    no=1, serial='1 (companion 5)', authors='Sharma S., Vashisht B.B., Singh P. & Singh Y.', year=2023, journal='Biomass Conversion and Biorefinery',
    ref=('Sharma S., Vashisht B.B., Singh P. & Singh Y. (2023) Changes in soil aggregate-associated organic carbon, enzymatic activity, and biological pools under conservation agriculture '
         'based practices in rice-wheat system. Biomass Conversion and Biorefinery 13:13977-13994, doi 10.1007/s13399-021-02144-y.'),
    doi='10.1007/s13399-021-02144-y',
    fert='As study 1 (recommended NPK); rice main plots: wheat stubble 0 / 25 % and Sesbania green manure (GM) - pooled',
    tmap=('SAME PAU 2011 trial as study 1 (split plot, 3 reps). Wheat sub plots coded as the study-1 companions: CTWR0 (2 disc harrow + 2 tyne + planking, rice residue removed) -> CT ; '
          'ZTWR0 (zero-till drill, residue removed) -> pZT ; ZTWR100 (Turbo Happy Seeder into 100 % rice residue) -> pCA (puddled transplanted rice in every main plot, rule 124). '
          'Only MAIN EFFECTS printed (interaction NS): wheat values pooled over the 4 rice main plots CTRW0 / CTRW25 / CTRW0 + GM / CTRW25 + GM (FLAG, T = 4). Rice main-plot effects (no tillage contrast) -> Notes.'),
    details=('TREATMENTS IN PAPER: rice main plots CTRW0, CTRW25 (25 % anchored wheat stubble), CTRW0 + GM, CTRW25 + GM (all puddled transplanted) x wheat sub plots CTWR0, ZTWR0, ZTWR100. || MAPPING: '
             'CTWR0 -> CT [rice: puddled TPR; wheat: conventional; residue: removed] | ZTWR0 -> pZT [rice: puddled TPR; wheat: zero-till drill; residue: removed] | '
             'ZTWR100 -> pCA [rice: puddled TPR; wheat: Turbo Happy Seeder; residue: 100 % rice residue mulch] | rice main plots -> pooled / Notes'),
)
SITE = dict(country='India (Punjab)', site='PAU research farm, Ludhiana (trial of study 1)', lat=30.933, lon=75.867, climate='TEMP', duration='4-10 Y', soil='LOAMY',
            CLAY=13.5, sand=70.5, silt=16.0, **{'RAIN FALL': 759, 'ph (initial)': 7.81, 'soc (initial)': 3.51})
HEAD = ('CT = CTWR0, pZT = ZTWR0, pCA = ZTWR100. WHEAT MAIN EFFECTS pooled over 4 rice main plots (wheat stubble 0 / 25 % x +/- Sesbania GM; interaction NS) - FLAG (T = 4). '
        'Soil sampled April 2017 after the 6th wheat. ')
SAMP = 'Soil after wheat harvest, April 2017 (6th cycle)'
YD = 'April 2017 (6 yr)'
MA = 'Wet sieving of 100 g <8 mm aggregates through 2.0 / 1.0 / 0.5 / 0.25 / 0.11 / 0.053 mm sieves (capillary wetting 10 min, 5 min at 35 oscillations/min); MWD / GMD (van Bavel); AR = macro / micro.'


def rows(B):
    st = ST; out = []

    def add(sheet, vals, body, unit, src, meth, depth=('0-15 cm', '0-15 CM'), crop=SAMP, yd=YD, extra=None):
        obs, nt = notes(st, HEAD + body, t=4)
        v = base(st, SITE, {'year of data collection/experiment': yd, 'YEAR OF DATA (duration)': yd})
        if depth:
            v.update({'DEPTH': depth[1], 'DEPTH (as reported in paper)': depth[0]})
        v.update(extra or {})
        v.update(vals)
        v.update({'UNIT': unit, 'Crop/season of sampling': crop, 'Data source': src, 'Method used (from paper)': meth, 'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
        out.append((sheet, B.add_row(sheet, v)))

    def cv(pre, x):
        return {f'{pre}CT': x[0], f'{pre}pZT': x[1], f'{pre}pCA': x[2]}

    RICE = ' Rice main plots CTRW0 / CTRW25 / CTRW0 + GM / CTRW25 + GM: {}.'
    BD = (1.55, 1.55, 1.44)
    add('BD', cv('BD_', BD), 'Table 2 bulk density (0-15 cm, core method).' + RICE.format('1.56 / 1.55 / 1.54 / 1.49'), 'Mg/m3', 'Table 2', 'Core method (7.2 cm cores, 105 C).')
    add('IR', cv('IR_', (0.49, 0.73, 1.26)), 'Table 2 infiltration rate (double ring).' + RICE.format('0.70 / 0.83 / 0.73 / 1.00'), 'cm/hr (double-ring infiltration rate; steady-state assumed - FLAG)', 'Table 2',
        'Double-ring infiltrometer in situ.', depth=('surface (double ring)', '0-15 CM'))
    add('HC', cv('HC_', (1.57, 3.32, 5.40)), 'Table 2 saturated hydraulic conductivity (constant head, undisturbed cores).' + RICE.format('2.26 / 4.36 / 3.45 / 4.99'), 'cm/hr', 'Table 2',
        'Constant-head method on saturated undisturbed cores.')
    FC = (10.8, 12.0, 14.3); PWP = (2.45, 2.49, 2.75); AWC = (8.3, 9.6, 11.6)
    mw = 'Pressure plate at 0.33 bar (FC) and 15 bar (PWP) on saturated ring samples; volumetric water content (m3/m3 printed as %).'
    add('FC (weight basis)', {f'FC_{c}': f'=ROUND({f}/{b},2)' for c, f, b in zip(('CT', 'pZT', 'pCA'), FC, BD)},
        f'Table 2 volumetric FC (-33 kPa) {FC[0]} / {FC[1]} / {FC[2]} % v/v converted to % w/w = FCv / BD (Table 2 BD) - DERIVED.' + RICE.format('10.2 / 11.3 / 12.6 / 13.5 % v/v'),
        '% w/w (DERIVED: printed % v/v / BD)', 'Table 2 (DERIVED)', mw)
    add('PWP (weight basis)', {f'PWP_{c}': f'=ROUND({f}/{b},2)' for c, f, b in zip(('CT', 'pZT', 'pCA'), PWP, BD)},
        f'Table 2 volumetric PWP (-1500 kPa) {PWP[0]} / {PWP[1]} / {PWP[2]} % v/v converted / BD - DERIVED. Printed AWC (8.3 / 9.6 / 11.6) is not FC - PWP (8.35 / 9.51 / 11.55) exactly - rounding.' + RICE.format('2.1 / 2.6 / 2.2 / 3.0 % v/v'),
        '% w/w (DERIVED: printed % v/v / BD)', 'Table 2 (DERIVED)', mw)
    add('AWC (volume basis)', cv('AWCV_', AWC), 'Table 2 available water content (0.33-15 bar).' + RICE.format('8.1 / 8.7 / 10.4 / 10.5'), '% v/v', 'Table 2', mw)
    add('AWC (weight basis)', {f'AWCW_{c}': f'=ROUND({a}/{b},2)' for c, a, b in zip(('CT', 'pZT', 'pCA'), AWC, BD)}, 'AWC % w/w DERIVED = printed AWC (% v/v) / BD (Table 2).',
        '% w/w (DERIVED: AWCv / BD)', 'Table 2 (DERIVED)', mw)
    cls = 'CT 3.1 / 3.5 / 12.1 / 18.4 / 26.3 / 4.3; pZT 4.2 / 4.5 / 14.9 / 20.2 / 24.8 / 5.1; pCA 5.2 / 5.6 / 17.0 / 22.9 / 22.7 / 6.3'
    add('MACRO', cv('MACRO_', (37.1, 43.8, 50.7)), f'Table 3 total water-stable macroaggregates (>0.25 mm). Classes >2 / 1-2 / 0.5-1 / 0.25-0.5 / 0.11-0.25 / 0.053-0.11 mm (%): {cls}.'
        + RICE.format('35.7 / 37.9 / 41.2 / 46.3'), '% (>0.25 mm water-stable aggregates)', 'Table 3', MA)
    add('MICRO', cv('MICRO_', (30.7, 29.9, 29.0)), 'Table 3 total micro-aggregates 0.25-0.053 mm (0.11-0.25 + 0.053-0.11 mm; rule 102).' + RICE.format('29.2 / 29.1 / 28.2 / 27.8'),
        '% (0.25-0.053 mm)', 'Table 3', MA)
    add('WSA', {f'WSA_{c}': f'=ROUND({x}/100,3)' for c, x in zip(('CT', 'pZT', 'pCA'), (67.7, 73.7, 79.7))}, 'Table 3 total water-stable aggregates, printed % / 100 (rule 74).'
        + RICE.format('64.9 / 67.0 / 69.4 / 74.1 %'), 'g/g (printed % / 100)', 'Table 3', MA)
    add('MWD 1', cv('MWD_', (0.389, 0.449, 0.489)), 'Table 4 mean weight diameter.' + RICE.format('0.396 / 0.423 / 0.432 / 0.485'), 'mm (wet sieving)', 'Table 4', MA)
    add('GMD 1', cv('GMD_', (0.246, 0.312, 0.330)), 'Table 4 geometric mean diameter.' + RICE.format('0.250 / 0.279 / 0.298 / 0.357'), 'mm', 'Table 4', MA)
    add('AGGREGATE RATIO', cv('AR_', (1.21, 1.46, 1.75)), 'Table 4 aggregate ratio (macro / micro).' + RICE.format('1.22 / 1.30 / 1.46 / 1.67'), 'ratio (% macro / % micro aggregates)', 'Table 4', MA)
    mc = 'TOC of each aggregate class by wet digestion (1 N K2Cr2O7, 150 C, 1 h); Chan fractions by 12 / 18 / 24 N H2SO4 (modified Walkley-Black).'
    add('macro c', cv('MACRO c_', (4.26, 4.67, 5.47)), 'Table 5 TOC of MACRO-aggregates (>0.25 mm). Chan fractions in macro-aggregates F1 / F2 / F3 / F4 (g/kg): CT 0.43 / 0.59 / 0.92 / 2.32; '
        'pZT 0.44 / 0.70 / 0.98 / 2.55; pCA 0.53 / 0.72 / 1.21 / 3.01 (no aggregate-fraction sheet).' + RICE.format('TOC 4.22 / 4.35 / 4.45 / 4.73'), 'g/kg (C in >0.25 mm aggregates)', 'Table 5', mc)
    add('micro c', cv('MICRO c_', (3.70, 4.02, 4.93)), 'Table 5 TOC of MICRO-aggregates (<0.25 mm). Chan fractions F1 / F2 / F3 / F4 (g/kg): CT 0.35 / 0.44 / 0.73 / 2.18; pZT 0.36 / 0.49 / 0.79 / 2.38; '
        'pCA 0.44 / 0.55 / 0.96 / 2.78.' + RICE.format('TOC 3.69 / 3.81 / 4.20 / 4.54'), 'g/kg (C in <0.25 mm aggregates)', 'Table 5', mc)
    ENZ = ('Other aggregate enzymes (Table 6; no aggregate-specific sheet): DHA (ug TPF/g/h) macro 33.0 / 46.3 / 50.8, micro 25.7 / 26.3 / 30.2; cellulase (ug glucose/g/h) macro 30.6 / 33.0 / 47.8, '
           'micro 20.7 / 24.5 / 32.8; beta-glucosidase (ug pNP/g/h) macro 16.7 / 21.1 / 24.2, micro 12.8 / 15.5 / 19.6 (CT / pZT / pCA).')
    for sc, lab, x in (('>0.25 mm', 'macro-aggregates (>0.25 mm)', (17.7, 20.9, 21.4)), ('<0.25 mm', 'micro-aggregates (<0.25 mm)', (16.7, 18.4, 20.1))):
        add('AGG-ALKP', cv('ALP_', x), f'Table 6 alkaline phosphatase in {lab}. ' + ENZ, 'ug p-nitrophenol/g aggregate/h', 'Table 6',
            'p-nitrophenyl phosphate assay on field-moist aggregates (Tabatabai).', extra={'Aggregate size class': sc})
    add('YIELD', {'WYIELD_CT': 5.73, 'WYIELD_pZT': 5.35, 'WYIELD_pCA': 6.26, 'W STRAW_CT': 6.82, 'W STRAW_pZT': 6.71, 'W STRAW_pCA': 7.05},
        'Figure 6 wheat grain (10 % moisture) and straw yield, DIGITISED (vector figure rendered at 300 dpi, calibrated axes). Season not stated (presumably 2016-17, before the April 2017 sampling - FLAG). '
        'Text: CT ~9 % and ZTWR0 ~17 % lower than ZTWR100 (digitised 8 / 15 %). Rice main plots grain 5.15 / 5.64 / 5.95 / 6.37, straw 6.69 / 6.80 / 6.91 / 7.04 t/ha.',
        't/ha (DIGITISED)', 'Figure 6 (digitised)', 'Net plot 2 x 9 m harvested; grain at 10 % moisture, straw oven-dry.', depth=None, crop='Wheat (season not stated, presumably 2016-17)', yd='wheat 2016-17 (presumed)')
    add('SQI', cv('SQI_', (1.43, 1.38, 1.48)), 'Figure 8 soil quality index (stacked MDS contributions FC, TG <0.25 mm, non-labile C >0.25 mm, WSA, PWP), DIGITISED stack tops (calibrated 0-1.6 axis). '
        'Scale exceeds 1 (sum of weighted scores) - compare within the row only.' + RICE.format('1.50 / 1.47 / 1.50 / 1.53 (digitised; x-axis labels of the 3rd / 4th rice bars both misprinted "CTRW25+GM")'), 'index (PCA / MDS weighted; as plotted)', 'Figure 8 (digitised)',
        'SQI = sum(Wi x Si) over MDS indicators (PCA).')
    return out


TM = [
    ('CTWR0', 'Rice residue removed; 2 disc harrow + 2 tyne plough + planking, pre-sowing irrigation, 2 tyne + planking; seed drill', 'Puddled TPR (all main plots)', 'Conventional', 'No', '0', 'CT', 'As study 1.', 'High', 'INCLUDED'),
    ('ZTWR0', 'Rice residue removed; zero-till drill', 'Puddled TPR', 'Zero tillage', 'No', '0', 'pZT', 'As study 1 (rule 124).', 'High', 'INCLUDED'),
    ('ZTWR100', 'All rice residue retained; Turbo Happy Seeder', 'Puddled TPR', 'Zero tillage (Happy Seeder)', 'Yes', '100 %', 'pCA', 'As study 1 (rule 124).', 'High', 'INCLUDED'),
    ('CTRW0 / CTRW25 / CTRW0 + GM / CTRW25 + GM (rice main plots)', 'Puddled TPR with 0 / 25 % anchored wheat stubble, +/- Sesbania green manure', 'Puddled TPR', 'Sub plots', 'Wheat stubble 0 / 25 %', None,
     'Pooled / Notes', 'Not a tillage contrast (as study 1).', 'High', 'INCLUDED (pooled)'),
]
STUDY_INFO = dict(estab=2011, yeardata='Soil April 2017 (after 6th wheat); wheat yield (season not stated)', years='1 sampling', texture='Sandy loam (13.5 % clay, 16.0 % silt, 70.5 % sand), Typic Ustochrept',
                  rotation='Rice-wheat (+/- Sesbania GM)', wheatvar='Not reported', ricevar='Not reported', N='As study 1', P='As study 1', K='As study 1',
                  residue='Wheat: rice residue removed / 100 % retained (Happy Seeder); rice: 0 / 25 % wheat stubble', irrigation='Not detailed', treatments='4 rice main plots x 3 wheat sub plots (split plot, 3 reps)',
                  supp='Supplementary Tables 1-2 (PCA loadings) - not downloaded (permission needed); no treatment means',
                  params=('Wheat main effects CT / pZT / pCA (pooled over rice main plots): BD, IR, Ks, FC and PWP (w/w derived), AWC (v/v and w/w), MACRO, MICRO, WSA, MWD, GMD, aggregate ratio, '
                          'macro / micro aggregate TOC, aggregate alkaline phosphatase, wheat grain and straw yield (Fig. 6 digitised), SQI (Fig. 8 digitised)'),
                  notes=('COMPANION 5 of study 1 (ext\\670.pdf; April 2017 sampling - companions 1-4 hold 2015-16 / 2016 data). '
                         'NOT ON A SHEET: Chan C fractions within aggregates (in macro c / micro c notes), aggregate DHA / cellulase / beta-glucosidase (AGG-ALKP notes), glomalin EEG / TG in aggregates '
                         '(Fig. 5, read by eye - approximate: EEG >0.25 / <0.25 mm: CT 7.0 / 10.1, pZT 8.0 / 12.1, pCA 9.9 / 14.4; TG 6.4 / 5.8, 7.4 / 6.9, 8.7 / 8.5 g/kg), active / non-labile C in aggregates (Fig. 2; = F1 + F2 / F3 + F4 of Table 5), '
                         'aggregate-class change (Fig. 1), PCA (Figs 7, 9-10, Table 7). Rice main-plot effects in row notes.'))
SITES = [('PAU research farm, Ludhiana', "30 56' N", "75 52' E", 30.933, 75.867, 'Paper', 'TEMP', 'Trial of study 1')]
