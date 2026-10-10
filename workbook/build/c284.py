"""284 (companion 2) - Nandan R., Singh V., Singh S.S., Hazra K.K. & Nath C.P. 2018 J. Crop Weed 14(2):65-71 (ext 648): RCER Patna T&CE x residue, rice yields."""
from common import base, notes

ST = dict(
    no=284, serial='284 (companion 2)', authors='Nandan R., Singh V., Singh S.S., Hazra K.K. & Nath C.P.', year=2018, journal='Journal of Crop and Weed',
    ref=('Nandan R., Singh V., Singh S.S., Hazra K.K. & Nath C.P. (2018) Performance of crop residue management with different tillage and crop establishment practices on '
         'weed flora and crop productivity in rice-wheat cropping system of eastern Indo-Gangetic plains. Journal of Crop and Weed 14(2):65-71.'),
    doi=None,
    fert='Rice: 120-40-40 N-P2O5-K2O + 25 kg ZnSO4 (hybrid Arize Tez); wheat HD 2967: 120-60-40; residue ~33 % retained vs removed',
    tmap=('SAME ICAR-RCER Patna trial as study 284 (data 2013-14 = 4th and 2014-15 = 5th year; split plot, residue removal / ~33 % retention x 4 T&CE). Coded as 284: CTTPR-CT (2 dry harrowings + 2 puddlings + planking; '
          'wheat broadcast after 2 harrowing + 2 tillage + planking) -> CT ; UPTPR-ZT (dry tillage + planking, no puddling; Happy Seeder ZT wheat) -> pZT (rule 138) ; ZTTPR-ZT (zero-till transplanting into flooded soil) -> ZT (row a) ; '
          'ZTDSR-ZT (zero-till drill DSR) -> ZT (row b). Values = T&CE main effects pooled over residue removal / retention (FLAG, as 284).'),
    details=('TREATMENTS IN PAPER: residue removal vs retention (~33 %) (main) x CTTPR-CT, UPTPR-ZT, ZTTPR-ZT, ZTDSR-ZT (sub), split plot. || MAPPING: '
             'CTTPR-CT -> CT [rice phase: puddled TPR; wheat phase: conventional; residue: pooled] | UPTPR-ZT -> pZT [rice phase: dry-tilled unpuddled TPR; wheat phase: Happy Seeder ZT; residue: pooled] | '
             'ZTTPR-ZT -> ZT (row a) [rice: zero-till TPR; wheat: ZT] | ZTDSR-ZT -> ZT (row b) [rice: zero-till DSR; wheat: ZT]'),
)
SITE = dict(country='India (Bihar)', site='ICAR-RCER research farm, Patna (trial of study 284)', lat=25.617, lon=85.217, climate='ST', duration='4-10 Y', soil='CLAYEY',
            CLAY=44.0, sand=15.0, silt=41.0, **{'RAIN FALL': 1130, 'ph (initial)': 7.11, 'soc (initial)': 4.9, 'Bdi': 1.44})
# rice grain yield (t/ha): CTTPR, UPTPR, ZTTPR, ZTDSR ; source note
RICE = {2013: ((4.47, 4.594, 4.94, 5.39), 'CTTPR 4.47, ZTTPR 4.94, ZTDSR 5.39 printed in text; UPTPR digitised 4.59'),
        2014: ((4.06, 4.465, 4.75, 5.21), 'CTTPR 4.06, ZTTPR 4.75, ZTDSR 5.21 printed in text; UPTPR digitised 4.47')}
WHEAT = {2013: '4.59 / 5.07 / 5.33 / 5.62 (= 284 Table 8: 4.586 / 5.071 / 5.341 / 5.621)', 2014: '4.68 / 5.51 / 5.63 / 5.73 (= 284: 4.676 / 5.512 / 5.625 / 5.734)'}
RES = {2013: 'rice 4.60 vs 5.08, wheat 5.02 vs 5.29', 2014: 'rice 4.43 vs 4.81, wheat 5.12 vs 5.66'}


def rows(B):
    st = ST; out = []
    for yr, (r, src) in RICE.items():
        for tag, zt, zl in (('a', r[2], 'ZTTPR-ZT'), ('b', r[3], 'ZTDSR-ZT')):
            vals = {'RICE YIELD_CT': r[0], 'RICE YIELD_ZT': zt}
            if tag == 'a':
                vals['RICE YIELD_pZT'] = r[1]
            body = (f"ROW {tag}: CT = CTTPR-CT, " + ('pZT = UPTPR-ZT, ' if tag == 'a' else '') + f"ZT = {zl}. Fig. 1 rice grain yield {yr} ({yr - 2009}th year), T&CE MAIN EFFECT pooled over residue removal / ~33 % retention (FLAG). "
                    f"{src}. PARTIAL REPEAT (rule 136): wheat grain yields of the same figure (CT / pZT / ZTTPR / ZTDSR {WHEAT[yr]}) are already in study 284 - not re-entered. "
                    f"Residue main effect (pooled over T&CE, removal vs retention, digitised): {RES[yr]}. Weed density / biomass (Tables 3-6) - no sheet.")
            obs, nt = notes(st, body, t=2)
            v = base(st, SITE, {'year of data collection/experiment': f'rice {yr}', 'YEAR OF DATA (duration)': f'rice {yr}'})
            v.update(vals)
            v.update({'UNIT': 't/ha', 'Crop/season of sampling': f'Rice {yr} (kharif)', 'Data source': 'Text + Figure 1 (digitised)',
                      'Method used (from paper)': 'Combine-harvested, power-thresher; grain yield from net plot.', 'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
            out.append(('YIELD', B.add_row('YIELD', v)))
    return out


TM = [
    ('CTTPR-CT', '2 dry harrowings + 2 puddlings + planking, manual TPR; wheat broadcast after 2 harrowing + 2 tillage + planking', 'Puddled TPR', 'Conventional', 'Pooled', None, 'CT', 'As 284.', 'High', 'INCLUDED'),
    ('UPTPR-ZT', 'Dry tillage + planking, no puddling, TPR; wheat ZT Happy Seeder', 'Dry-tilled unpuddled TPR', 'Zero tillage', 'Pooled', None, 'pZT', 'As 284 (rule 138).', 'High', 'INCLUDED'),
    ('ZTTPR-ZT', 'Zero-till transplanting into soil flooded 1 day before; wheat ZT Happy Seeder', 'Zero-till TPR', 'Zero tillage', 'Pooled', None, 'ZT (row a)', 'As 284.', 'High', 'INCLUDED'),
    ('ZTDSR-ZT', 'Zero-till drill DSR (hybrid Arize Tez); wheat ZT Happy Seeder', 'Zero-till DSR', 'Zero tillage', 'Pooled', None, 'ZT (row b)', 'As 284.', 'High', 'INCLUDED'),
    ('Residue removal / retention (~33 %)', 'Main plots', 'n/a', 'n/a', 'No / ~33 %', None, 'Pooled', 'Only T&CE main effects pooled over residue printed (FLAG; T = 2).', 'Medium', 'INCLUDED (pooled)'),
]
STUDY_INFO = dict(estab=None, yeardata='Rice 2013, 2014 (4th and 5th year)', years='2', texture='Silty clay (15 % sand, 41 % silt, 44 % clay), Typic Ustochrept', rotation='Rice-wheat',
                  wheatvar='HD 2967', ricevar='Arize Tez (hybrid)', N='120 rice / 120 wheat', P='40 / 60 P2O5', K='40 / 40 K2O', residue='~33 % retained vs removed (pooled)',
                  irrigation='Not detailed', treatments='2 residue x 4 T&CE (split plot)',
                  params='Rice grain yield 2013 and 2014 per T&CE (pooled over residue) - CT / pZT / ZT rows a-b; wheat yields = repeat of 284 (notes)',
                  supp='None',
                  notes=('COMPANION 2 of study 284 (ext\\648.pdf; same RCER Patna trial). PARTIAL REPEAT (rule 136): wheat yields = study 284; only rice yields new. '
                         'Weed density / dry weight by category (Tables 3-6) - no sheet. Initial soil: pH 7.11, EC 0.38 dS/m, OC 0.49 %, BD 1.44, PR 1.75 MPa, avail. N 135.2, P 35.2, K 239.2 kg/ha, DTPA Zn 0.83, Fe 19.9, Mn 25.5, Cu 2.59 ppm. '
                         'Paper says the experiment was "initiated during 2013-14" yet calls 2013-14 the 4th year (284: trial 2009/10) - FLAG.'))
SITES = [('ICAR-RCER research farm, Patna', 'not reported', 'not reported', 25.617, 85.217, 'As study 284', 'ST', 'Trial of study 284')]
