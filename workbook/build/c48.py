"""48 (companion 3) - Mondal S. et al. 2020 Eur. J. Soil Sci. 71:1076-1089 (ext 647): RCER Patna CSISA trial, 5 yr soil physics / C."""
from common import base, notes

ST = dict(
    no=48, serial='48 (companion 3)',
    authors='Mondal S., Poonia S.P., Mishra J.S., Bhatt B.P., Karnena K.R., Saurabh K., Kumar R. & Chakraborty D.', year=2020, journal='European Journal of Soil Science',
    ref=('Mondal S., Poonia S.P., Mishra J.S., Bhatt B.P., Karnena K.R., Saurabh K., Kumar R. & Chakraborty D. (2020) Short-term (5 years) impact of conservation agriculture '
         'on soil physical properties and organic carbon in a rice-wheat rotation in the Indo-Gangetic plains of Bihar. European Journal of Soil Science 71:1076-1089, doi 10.1111/ejss.12879.'),
    doi='10.1111/ejss.12879',
    fert='Recommended (not stated in this paper); TA residues removed; pCA1 1/3 rice residue mulch, wheat anchored residue incorporated, mungbean fully incorporated; fCA 1/3 rice and wheat residue as surface mulch, mungbean retained',
    tmap=('SAME CSISA trial as study 48 (ICAR-RCER Patna, est. Nov 2009; RCBD, 3 reps, 0.2 ha plots); soil sampled after the 2014 rice harvest (5th year). TA (PTR-CTW, residues removed, rice-wheat-fallow) -> CT ; '
          'pCA1 (PTR-NTW-CTMB; rice 1/3 residue as mulch, wheat anchored residue, mungbean incorporated) -> pCA (residue stated in Table 1; study 48 coded this scenario pCA, 48 (companion) pZT under rule 109 - FLAG) ; '
          'fCA (DSR-NTW-NTMB, 1/3 rice and wheat residue mulch) -> CA (mungbean in CA / pCA only, rule 71) ; pCA2 (UPTPR-CT potato + maize-NT mungbean) -> EXCLUDED (no wheat, rule 31).'),
    details=('TREATMENTS IN PAPER: TA = PTR-CTW (rice-wheat-fallow); pCA1 = PTR-NTW-CTMB; fCA = DSR-NTW-NTMB; pCA2 = UPTPR-CTP+M-NTMB (RCBD, 3 reps, 0.2 ha plots). || MAPPING: '
             'TA -> CT: puddled TPR + conventional broadcast wheat, residues removed [rice phase: puddled; wheat phase: conventional; residue: No] | '
             'pCA1 -> pCA: puddled TPR + no-till drilled wheat + CT mungbean; rice 1/3 residue mulch, wheat anchored residue [rice phase: puddled; wheat phase: no tillage; residue: Yes] | '
             'fCA -> CA: no-till DSR + no-till wheat + no-till mungbean, 1/3 rice and wheat residue as surface mulch [rice phase: no-till DSR; wheat phase: no tillage; residue: Yes] | '
             'pCA2 -> EXCLUDED: unpuddled TPR - CT potato + maize - NT mungbean (no wheat)'),
)
SITE = dict(country='India (Bihar)', site='ICAR Research Complex for Eastern Region, Patna (CSISA trial of study 48)', lat=25.617, lon=85.217, climate='ST', duration='4-10 Y', soil='CLAYEY',
            CLAY=41.4, sand=16.8, silt=41.8, **{'RAIN FALL': 1130})
C3 = ['CT', 'pCA', 'CA']
RED = 'RICE SEASON - soil sampled after the 2014 rice harvest (5th year)'
HEAD = 'CT = TA, pCA = pCA1 (FLAG vs 48 (companion) pZT), CA = fCA; pCA2 (no wheat) excluded - values in notes. RICE-SEASON ROW (whole row red; soil sampled after rice harvest 2014, rule 79).'
LAY = [('0-10', '0-15 CM', 1), ('10-20', '15-30 CM', 2), ('20-30', '15-30 CM', 2)]


def rows(B):
    st = ST; out = []

    def add(sheet, vals, body, depth=None, d=1, y=1, red=True, unit=None, src=None, meth=None, crop=RED, yd='2014 (5 yr)'):
        obs, nt = notes(st, HEAD + ' ' + body if red else body, y=y, d=d)
        v = base(st, SITE, {'year of data collection/experiment': '2014', 'YEAR OF DATA (duration)': yd})
        if depth:
            v.update({'DEPTH': depth[1], 'DEPTH (as reported in paper)': depth[0] + ' cm'})
        v.update(vals)
        v.update({'UNIT': unit, 'Crop/season of sampling': crop, 'Data source': src, 'Method used (from paper)': meth, 'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
        out.append((sheet, B.add_row(sheet, v, red=red)))

    def cv(pre, nums):
        return {f'{pre}_{c}': x for c, x in zip(C3, nums) if x is not None}

    # ---- BD (Fig. 1 digitised; TA 0-10 printed 1.44)
    BD = {'0-10': ([1.44, 1.507, 1.551], 1.523), '10-20': ([1.634, 1.632, 1.584], 1.618), '20-30': ([1.607, 1.565, 1.542], 1.571)}
    for ly, cls, d in LAY:
        x, p2 = BD[ly]
        add('BD', cv('BD', x), f'Figure 1 bulk density {ly} cm, digitised (raster, calibrated axis; TA 0-10 = 1.44 printed in text; fCA 10-20 = 1.58 in text). pCA2 {p2}. '
            'Check: printed OC x BD x 10 reproduces Table 5 stocks within 0.05 Mg/ha.', (ly, cls), d=d, unit='Mg/m3', src='Figure 1 (digitised)',
            meth='Core method (5 x 5 cm cores, triplicate, oven-dried 105 C; Blake & Hartge 1986) after rice harvest.')
    # ---- Table 3: pores, total porosity (printed, = BD / PD 2.65), IR
    T3 = {'0-10': [(10.6, 19.0, 16.2, 45.7), (8.0, 18.5, 16.6, 43.2), (4.1, 22.2, 15.2, 41.5), (6.3, 19.9, 16.2, 42.5)],
          '10-20': [(4.0, 18.1, 16.3, 38.3), (2.1, 20.4, 15.9, 38.4), (5.8, 17.4, 17.0, 40.2), (2.7, 20.0, 16.3, 39.0)],
          '20-30': [(2.6, 20.7, 16.1, 39.4), (4.5, 21.4, 15.0, 40.9), (3.5, 22.8, 15.4, 41.8), (3.2, 21.5, 15.9, 40.7)]}
    mp = 'Pressure plate (-10 to -1500 kPa) on 5 x 5 cm cores; macropores drained at -10 kPa, mesopores -10 to -1500 kPa, micropores > -1500 kPa (Table 3).'
    for ly, cls, d in LAY:
        t = T3[ly]
        for sheet, pre, i, nm in (('macro pore', 'MACROPORE', 0, 'macropore'), ('meso pore', 'MESOPORE', 1, 'mesopore'), ('micro pore', 'MICROPORE', 2, 'micropore')):
            add(sheet, cv(pre, [r[i] for r in t[:3]]), f'Table 3 {nm} volume {ly} cm. pCA2 {t[3][i]}.', (ly, cls), d=d, unit='% v/v (cm3/cm3 x 100)', src='Table 3', meth=mp)
        add('POROSITY', cv('POROSITY', [r[3] for r in t[:3]]), f'Table 3 total porosity {ly} cm (printed; the paper computed it from BD with PD 2.65). pCA2 {t[3][3]}.',
            (ly, cls), d=d, unit='% v/v (printed)', src='Table 3', meth='Total porosity from BD and particle density 2.65 g/cm3 (paper).')
    add('IR', cv('IR', [1.54, 1.52, 3.59]), 'Table 3 STEADY-STATE infiltration rate (after rice harvest 2014, double ring). pCA2 2.02 cm/h.', ('surface (double ring)', '0-15 CM'),
        unit='cm/hr (steady-state)', src='Table 3', meth='Double-ring infiltrometer, ponding method (Bouwer 1986), rings inserted 4-5 cm, 3 observations per plot.')
    # ---- Table 2 aggregates
    T2 = {'0-10': [(23.4, 43.0, 18.5, 15.1, 66.4, 84.9), (28.2, 47.3, 12.8, 11.7, 74.9, 87.7), (45.2, 38.5, 10.7, 5.6, 83.7, 94.4), (32.7, 40.7, 14.6, 12.0, 74.0, 88.6)],
          '10-20': [(25.7, 38.9, 20.2, 14.2, 65.4, 85.8), (29.6, 46.6, 16.8, 7.0, 76.2, 93.0), (43.4, 39.9, 13.0, 3.6, 83.3, 96.4), (39.2, 34.7, 16.5, 9.5, 74.0, 90.5)]}
    ma = 'Yoder wet sieving (2, 0.25, 0.053 mm sieves; 50 g <8 mm air-dried soil, capillary-wetted 10 min, 15 min at 35 cycles/min), sand-corrected.'
    LY2 = [('0-10', '0-15 CM', 1), ('10-20', '15-30 CM', 1)]
    for ly, cls, d in LY2:
        t = T2[ly]
        cls_txt = '; '.join(f'{c} {r[0]} / {r[1]} / {r[2]} / {r[3]}' for c, r in zip(C3 + ['pCA2'], t))
        add('MACRO', cv('MACRO', [r[4] for r in t[:3]]), f'Table 2 macroaggregates (8-2 + 2-0.25 mm) {ly} cm. Classes 8-2 / 2-0.25 / 0.25-0.053 / <0.053 (g/100 g): {cls_txt}. pCA2 {t[3][4]}.',
            (ly, cls), d=d, unit='% (g aggregates >0.25 mm / 100 g soil)', src='Table 2', meth=ma)
        add('MICRO', cv('MICRO', [r[2] for r in t[:3]]), f'Table 2 microaggregates 0.25-0.053 mm {ly} cm (silt + clay <0.053 mm excluded, rule 102). pCA2 {t[3][2]}.',
            (ly, cls), d=d, unit='% (g 0.25-0.053 mm aggregates / 100 g soil)', src='Table 2', meth=ma)
        add('WSA', cv('WSA', [f'=ROUND({r[5]}/100,3)' for r in t[:3]]), f'Table 2 WSA (macro + 0.25-0.053 mm) {ly} cm, printed % / 100 (rule 74). pCA2 {t[3][5]} %.',
            (ly, cls), d=d, unit='g/g (printed % / 100)', src='Table 2', meth=ma)
    # ---- Fig. 2 MWD / GMD
    MWD = {'0-10': ([1.69, 1.98, 2.71], 2.11, 'printed in text'), '10-20': ([1.787, 2.044, 2.643], 2.386, 'digitised from Fig. 2a (0-10 cm digitising reproduces the printed values within 0.02 mm)')}
    GMD = {'0-10': ([0.851, 0.964, 1.204], 0.977), '10-20': ([0.867, 1.010, 1.187], 1.034)}
    AS = {'0-10': '1.33 / 1.50 / 1.68 / 1.49', '10-20': '1.31 / 1.53 / 1.66 / 1.49'}
    AR = {'0-10': '3.6 / 6.2 / 7.9 / 5.1', '10-20': '3.2 / 4.7 / 7.9 / 4.6'}
    for ly, cls, d in LY2:
        x, p2, how = MWD[ly]
        add('MWD 1', cv('MWD', x), f'MWD {ly} cm ({how}). pCA2 {p2}. Aggregate stability (Fig. 2c, approx. TA / pCA1 / fCA / pCA2) {AS[ly]}; aggregate ratio (Fig. 2d) {AR[ly]} - no sheet.',
            (ly, cls), d=d, unit='mm (wet sieving)', src='Text + Figure 2a (digitised)' if ly == '10-20' else 'Text (Figure 2a)', meth=ma + ' MWD = sum(XiWi)/sum(Wi).')
        g, gp = GMD[ly]
        add('GMD 1', cv('GMD', g), f'GMD {ly} cm digitised from Fig. 2b (raster, calibrated). pCA2 {gp}.', (ly, cls), d=d, unit='mm', src='Figure 2b (digitised)',
            meth=ma + ' GMD = exp(sum(Wi log Xi)/sum(Wi)).')
    # ---- Table 4 aggregate C (g/100 g -> g/kg)
    T4 = {'0-10': [(0.72, 0.57, 0.49, 0.39, 0.65, 0.44, 0.55), (0.90, 0.74, 0.67, 0.42, 0.82, 0.55, 0.74), (0.94, 0.71, 0.63, 0.41, 0.83, 0.52, 0.74), (0.74, 0.71, 0.58, 0.59, 0.72, 0.59, 0.70)],
          '10-20': [(0.77, 0.53, 0.48, 0.42, 0.65, 0.45, 0.53), (0.71, 0.47, 0.50, 0.42, 0.59, 0.46, 0.54), (0.74, 0.42, 0.46, 0.37, 0.58, 0.41, 0.54), (0.55, 0.46, 0.44, 0.42, 0.50, 0.43, 0.49)]}
    mc = 'Aggregate-associated OC by Walkley-Black wet oxidation of each aggregate size class (Choudhury et al. 2014).'
    for ly, cls, d in LY2:
        t = T4[ly]
        allc = '; '.join(f'{c} MacOC {r[0]} MesOC {r[1]} MicOC {r[2]} SCOC {r[3]} tMicOC {r[5]} tAOC {r[6]}' for c, r in zip(C3 + ['pCA2'], t))
        add('macro c', cv('MACRO c', [f'=ROUND({r[4]}*10,2)' for r in t[:3]]), f'Table 4 total macroaggregate OC (tMacOC, >0.25 mm, proportion-weighted) {ly} cm, printed g/100 g x 10. All classes (g/100 g): {allc}.',
            (ly, cls), d=d, unit='g/kg (C in >0.25 mm aggregates; g/100 g x 10)', src='Table 4', meth=mc)
        add('micro c', cv('MICRO c', [f'=ROUND({r[2]}*10,2)' for r in t[:3]]), f'Table 4 microaggregate OC (MicOC, 0.25-0.053 mm; silt + clay class excluded, rule 102) {ly} cm, printed g/100 g x 10. pCA2 {t[3][2]}.',
            (ly, cls), d=d, unit='g/kg (C in 0.25-0.053 mm aggregates; g/100 g x 10)', src='Table 4', meth=mc)
    # ---- Table 5 SOC and stocks
    OC = {'0-10': [0.58, 0.59, 0.66, 0.59], '10-20': [0.31, 0.39, 0.39, 0.35], '20-30': [0.37, 0.31, 0.33, 0.33]}
    STK = {'0-10': [8.3, 8.9, 10.2, 8.9], '10-20': [5.1, 6.3, 6.1, 5.7], '20-30': [5.9, 4.9, 5.1, 5.3], '0-30': [19.3, 20.1, 21.4, 19.9]}
    for ly, cls, d in LAY:
        add('SOC(active C pool)', cv('SOC', [f'=ROUND({x}*10,2)' for x in OC[ly][:3]]), f'Table 5 organic C {ly} cm (Walkley-Black), printed g/100 g x 10. pCA2 {OC[ly][3]} g/100 g.',
            (ly, cls), d=d, unit='g/kg (Walkley-Black; g/100 g x 10)', src='Table 5', meth='Walkley-Black dichromate oxidation, <0.1 mm sieved composite bulk soil.')
    ms = 'C stock = SOC x BD x H / 10 (Eq. 5); BD from Fig. 1.'
    add('stock-SOC', cv('SOCs', STK['0-10'][:3]), f'Table 5 SOC stock 0-10 cm (printed). pCA2 {STK["0-10"][3]}.', ('0-10', '0-10 CM'), unit='Mg C/ha', src='Table 5', meth=ms)
    add('stock-SOC', cv('SOCs', [f'=ROUND({a}+{b},2)' for a, b in zip(STK['0-10'][:3], STK['10-20'][:3])]),
        'SOC stock 0-20 cm DERIVED = printed 0-10 + 10-20 cm layer stocks (Table 5). 10-20 cm layer: ' + ', '.join(f'{c} {x}' for c, x in zip(C3 + ['pCA2'], STK['10-20'])) + '.',
        ('0-20 (sum of layers)', '0-20 CM'), unit='Mg C/ha (DERIVED sum of layers)', src='Table 5 (DERIVED)', meth=ms)
    add('stock-SOC', cv('SOCs', STK['0-30'][:3]), 'Table 5 total SOC stock 0-30 cm (printed). 20-30 cm layer: ' + ', '.join(f'{c} {x}' for c, x in zip(C3 + ['pCA2'], STK['20-30'])) + f'. pCA2 0-30 {STK["0-30"][3]}.',
        ('0-30', '0-30 CM'), unit='Mg C/ha', src='Table 5', meth=ms)
    # ---- Fig. 4 yields (not red: crop yields)
    yb = 'CT = TA, pCA = pCA1 (FLAG vs 48 (companion) pZT), CA = fCA. Figure 4 digitised (raster, calibrated; error bars not read).'
    my = 'Combine-harvested; rice at 14 %, wheat at 12 % moisture; system productivity as rice-equivalent yield (MSP / local prices).'
    add('YIELD', {'WYIELD_CT': 4.075, 'WYIELD_pCA': 4.371, 'WYIELD_CA': 5.110, 'SYS YIELD_CT': 11.07, 'SYS YIELD_pCA': 14.89, 'SYS YIELD_CA': 17.10},
        yb + ' Wheat 2013-14 and system productivity 2013-14 (rice-equivalent incl. mungbean in pCA1 / fCA - SYS FLAG, rule 54). pCA2: wheat 4.20, system ~15.9. '
        'Wheat yields of this trial for 2013-16 are also in study 48 (Samal 2017) - possible DUPLICATE season (FLAG).', red=False, unit='t/ha', src='Figure 4 (digitised)', meth=my,
        crop='Wheat 2013-14; system 2013-14', yd='2013-14')
    add('YIELD', {'RICE YIELD_CT': 6.710, 'RICE YIELD_pCA': 6.587, 'RICE YIELD_CA': 7.498}, yb + ' Rice 2014. pCA2 5.97. Possible duplicate season with study 48 (FLAG).',
        red=False, unit='t/ha', src='Figure 4 (digitised)', meth=my, crop='Rice 2014', yd='2014')
    add('YIELD', {'WYIELD_CT': 4.691, 'WYIELD_pCA': 5.184, 'WYIELD_CA': 5.184, 'SYS YIELD_CT': 10.27, 'SYS YIELD_pCA': 15.99, 'SYS YIELD_CA': 15.50},
        yb + ' Wheat 2014-15 (text: 4.7-5.2 t/ha) and system productivity 2014-15 (SYS FLAG). pCA2: wheat 4.81, system 15.87. Possible duplicate season with study 48 (FLAG).',
        red=False, unit='t/ha', src='Figure 4 (digitised)', meth=my, crop='Wheat 2014-15; system 2014-15', yd='2014-15')
    add('YIELD', {'RICE YIELD_CT': 5.282, 'RICE YIELD_pCA': 5.971, 'RICE YIELD_CA': 5.602}, yb + ' Rice 2015. pCA2 6.22. Possible duplicate season with study 48 (FLAG).',
        red=False, unit='t/ha', src='Figure 4 (digitised)', meth=my, crop='Rice 2015', yd='2015')
    return out


TM = [
    ('TA (PTR-CTW)', 'Puddled transplanted rice + conventionally tilled broadcast wheat; rice and wheat residues removed; rice-wheat-fallow', 'Puddled TPR', 'Conventional', 'No', '0', 'CT', 'As 48 S1 / 48 (companion) TA.', 'High', 'INCLUDED'),
    ('pCA1 (PTR-NTW-CTMB)', 'Puddled TPR + no-till drilled wheat + CT mungbean; rice 1/3 residue as mulch, wheat anchored residue incorporated, mungbean fully incorporated', 'Puddled TPR', 'No tillage', 'Yes (1/3 rice residue)', None, 'pCA - FLAG',
     'Residue retention stated in Table 1 -> pCA (as study 48); 48 (companion) coded pZT under rule 109 (contradictory tables there).', 'Medium', 'INCLUDED'),
    ('fCA (DSR-NTW-NTMB)', 'No-till DSR + no-till wheat + no-till mungbean; 1/3 rice and wheat residue as surface mulch, mungbean retained', 'No-till DSR', 'No tillage', 'Yes', None, 'CA', 'Full CA (rule 71 for mungbean).', 'High', 'INCLUDED'),
    ('pCA2 (UPTPR-CTP+M-NTMB)', 'Unpuddled TPR + CT potato + maize + NT mungbean', 'Unpuddled TPR', 'n/a (no wheat)', 'Yes', None, 'EXCLUDED', 'No wheat (rule 31).', 'High', 'EXCLUDED'),
]
STUDY_INFO = dict(estab=2009, yeardata='Soil after rice 2014; yields 2013-14, 2014-15', years='Soil 1 sampling (5th yr); yields 2 years', texture='Silty clay (16.8 % sand, 41.8 % silt, 41.4 % clay), Typic Entisol',
                  rotation='Rice-wheat(-mungbean); pCA2 rice-potato + maize-mungbean excluded', wheatvar='Not reported', ricevar='Not reported', N='Not stated', P='Not stated', K='Not stated',
                  residue='TA removed; pCA1 1/3 rice residue mulch + wheat anchored; fCA 1/3 rice and wheat residue mulch; mungbean residue retained',
                  irrigation='TA / pCA1 rice continuous flooding 1 month then at hairline cracks / -20 to -30 kPa; fCA rice at -20 kPa; wheat at critical stages',
                  treatments='TA, pCA1, fCA, pCA2 (RCBD, 3 reps, 0.2 ha plots)',
                  params=('RED rows (after rice 2014): BD (Fig. 1, 3 layers), total / macro / meso / micro porosity (Table 3), steady-state IR, MACRO / MICRO / WSA, MWD, GMD (Fig. 2), '
                          'macro c / micro c (Table 4), SOC 3 layers and SOC stock 0-10 / 0-20 (derived) / 0-30 cm (Table 5); yields 2013-15 (Fig. 4)'),
                  supp='None referenced',
                  notes=('COMPANION 3 of study 48 (ext\\647.pdf; same CSISA RCER Patna trial, est. Nov 2009). pCA1 coded pCA (Table 1 states residue mulch; 48 (companion) coded pZT - FLAG). '
                         'Initial SOC printed as "80 and 57 g/kg" (0-15 / 15-30 cm) - evidently 8.0 / 5.7 g/kg (typo) - not entered. Yields 2013-15 may overlap study 48 (Samal 2017, yields 2013-16) - FLAG. '
                         'Not entered (no sheet): aggregate stability, aggregate ratio, % contribution of aggregate classes to AOC (Fig. 3).'))
SITES = [('ICAR-RCER research farm, Patna', "25 37' N", "85 13' E", 25.617, 85.217, 'Paper', 'ST', 'Trial of study 48')]
