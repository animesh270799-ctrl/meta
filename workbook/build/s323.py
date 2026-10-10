"""Study 323 - Mohanty M., Painuli D.K., Misra A.K. & Ghosh P.K. 2007 Soil Tillage Res. 92:243-250 (ext 646): puddling x wheat tillage x residue, Bhopal Vertisol - SQI."""
from common import base, notes

ST = dict(
    no=323, serial=323, authors='Mohanty M., Painuli D.K., Misra A.K. & Ghosh P.K.', year=2007, journal='Soil & Tillage Research',
    ref=('Mohanty M., Painuli D.K., Misra A.K. & Ghosh P.K. (2007) Soil quality effects of tillage and residue under rice-wheat cropping on a '
         'Vertisol in India. Soil & Tillage Research 92:243-250, doi 10.1016/j.still.2006.03.005.'),
    doi='10.1016/j.still.2006.03.005',
    fert='Rice IR 36: 90 N + 13 P + 22 K kg/ha; wheat C 306: 100 N + 26 P + 33 K kg/ha; residue 30-cm stubble retained in Rr plots (~6 t/ha after rice, ~4 t/ha after wheat)',
    tmap=('Split plot, 3 reps, IISS Bhopal Vertisol, 2000-2002 (after summer ploughing with a duck-foot cultivator). Rice main plot: P0 no puddling, dry direct line seeding into tilled soil; '
          'P1 puddling with 4 passes of a 5 hp power tiller (10.9 cm) and transplanting; P2 puddling with 8 passes (14.5 cm). Wheat: CT (1 disc harrow + 2 duck-foot cultivator passes) or ZT (Pantnagar zero-till drill). '
          'Residue: Rr (30 cm rice and wheat stubble retained) vs R0 (removed). Coding: tilled rice (P0 dry-tilled DSR, P1 / P2 puddled - rule 140: 4 and 8 passes = CT) + CT wheat -> CT (R0) / CTR (Rr); '
          '+ ZT wheat -> pZT (R0) / pCA (Rr) (rules 124 / 135 / 138). Rows a / b / c = P0 / P1 / P2.'),
    details=('TREATMENTS IN PAPER: rice P0 (direct line seeding, no puddling), P1 (puddling 4 passes, TPR), P2 (puddling 8 passes, TPR) x wheat CT / ZT x residue Rr / R0 (split plot, 3 reps, 4 x 8 m subplots). || MAPPING: '
             'PxCTR0 -> CT: tilled / puddled rice + CT wheat (disc harrow + 2 duck-foot cultivator passes), residue removed [rice phase: P0 dry-tilled DSR / P1 / P2 puddled TPR; wheat phase: conventional; residue: No] | '
             'PxCTRr -> CTR: same + 30 cm stubble retained [residue: Yes, ~6 t/ha after rice + ~4 t/ha after wheat] | '
             'PxZTR0 -> pZT: tilled / puddled rice + zero-till wheat (Pantnagar ZT drill), residue removed | PxZTRr -> pCA: same + stubble retained. Rows a / b / c = P0 / P1 / P2.'),
)
SITE = dict(country='India (Madhya Pradesh)', site='Indian Institute of Soil Science experimental farm, Bhopal', lat=23.3, lon=77.4, climate='ST', duration='0-3 Y', soil='CLAYEY',
            CLAY=56.6, sand=4.5, silt=38.9, **{'soc (initial)': 5.9, 'Bdi': 1.38})
# printed regression lines SQI = a + b t (Fig. 4), t = 0.5 ... 3 yr (6 samplings)
EQ = {'P0': {'CT': (-0.0074, 0.908), 'CTR': (-0.0029, 0.91), 'pZT': (0.0114, 0.8833), 'pCA': (0.0063, 0.924)},
      'P1': {'CT': (-0.0063, 0.8927), 'CTR': (-0.0029, 0.8967), 'pZT': (0.0011, 0.8813), 'pCA': (0.004, 0.8913)},
      'P2': {'CT': (-0.0063, 0.8627), 'CTR': (-0.0005, 0.8644), 'pZT': (0.0073, 0.8403), 'pCA': (0.008, 0.8593)}}
SUST = {'P0': 'P0CTR0 6 yr, P0CTRr 15 yr', 'P1': 'P1CTR0 5 yr, P1CTRr 11 yr', 'P2': 'P2CTR0 1 yr, P2CTRr 8 yr'}
RICE = {'P0': 'P0 no puddling (dry direct line seeding after tillage)', 'P1': 'P1 puddling 4 passes + TPR', 'P2': 'P2 puddling 8 passes + TPR'}


def rows(B):
    st = ST; out = []
    for tag, p in zip('abc', ('P0', 'P1', 'P2')):
        e = EQ[p]
        vals = {f'SQI_{c}': f'=ROUND({a}+({b})*1.75,3)' for c, (b, a) in e.items()}
        body = (f"ROW {tag}: rice {RICE[p]}; CT = {p}CTR0, CTR = {p}CTRr, pZT = {p}ZTR0, pCA = {p}ZTRr. SQI (0-15 cm; BD, PR, WSA, OM weighted by R2 of their yield regressions) "
                f"sampled 15 d after transplanting rice / sowing wheat at t = 0.5, 1, 1.5, 2, 2.5, 3 yr (Fig. 4). Scatter markers overlap (not digitised); the printed OLS line of each treatment "
                f"evaluated at the mean sampling time (t = 1.75 yr) EQUALS the mean of its 6 observations - entered as the 3-yr MEAN SQI (DERIVED exactly, FLAG). Equations: " +
                '; '.join(f'{c}: {b:+} t + {a}' for c, (b, a) in e.items()) +
                f". Rice- and wheat-season SQI (different weights: SQIr = 0.31 BD + 0.22 WSA + 0.36 PR + 0.11 OM; SQIw = 0.24 BD + 0.26 WSA + 0.27 PR + 0.23 OM) pooled in the series - FLAG. "
                f"Predicted sustainable time: {SUST[p]}. Individual BD, PR, WSA, OM values only as pooled scatter vs yield (Figs 1-2, no treatment labels) - not extractable. "
                "Rice phase coded tilled (rules 135 / 138 / 140).")
        obs, nt = notes(st, body, y=3)
        v = base(st, SITE, {'year of data collection/experiment': '2000-2002', 'YEAR OF DATA (duration)': '3 yr (6 samplings, mean)'})
        v.update(vals)
        v.update({'DEPTH': '0-15 CM', 'DEPTH (as reported in paper)': '0-15 cm', 'UNIT': 'index 0-1 (SQI; 3-yr mean DERIVED from printed regression line)',
                  'Crop/season of sampling': 'Mean of 6 samplings (15 d after rice transplanting / wheat sowing, 2000-2002; rice and wheat seasons pooled - FLAG)',
                  'Data source': 'Figure 4 (printed regression equations; DERIVED)',
                  'Method used (from paper)': 'SQI = sum of weighted scores (Wymore / Karlen scoring; thresholds Table 3) of BD (core), PR (Bush penetrometer), WSA (Yoder wet sieving, 4-8 mm aggregates), OM (Walkley-Black OC x 1.724), 0-15 cm.',
                  'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
        out.append(('SQI', B.add_row('SQI', v)))
    return out


TM = [
    ('P0 CT R0 / R0 Rr', 'Dry direct line-seeded rice (no puddling, after duck-foot cultivator tillage) + CT wheat; residue removed / 30 cm stubble retained', 'Tilled dry DSR', 'Conventional', 'No / Yes', '0 / ~10', 'CT / CTR (row a)', 'Dry-tilled DSR + CT wheat = CT family (rule 135).', 'Medium', 'INCLUDED'),
    ('P0 ZT R0 / Rr', 'Dry direct line-seeded rice + zero-till wheat; residue removed / retained', 'Tilled dry DSR', 'Zero tillage', 'No / Yes', '0 / ~10', 'pZT / pCA (row a)', 'Tilled DSR + ZT wheat -> partial codes (rules 124 / 135 / 138).', 'Medium', 'INCLUDED'),
    ('P1 CT R0 / Rr', 'Puddling 4 passes of 5 hp power tiller (10.9 cm) + TPR, CT wheat', 'Puddled TPR (4 passes)', 'Conventional', 'No / Yes', '0 / ~10', 'CT / CTR (row b)', 'Rule 140: 4 passes = CT.', 'High', 'INCLUDED'),
    ('P1 ZT R0 / Rr', 'Puddling 4 passes + TPR, ZT wheat', 'Puddled TPR', 'Zero tillage', 'No / Yes', '0 / ~10', 'pZT / pCA (row b)', 'Puddled rice + ZT wheat (rule 124).', 'High', 'INCLUDED'),
    ('P2 CT R0 / Rr', 'Puddling 8 passes (14.5 cm) + TPR, CT wheat', 'Puddled TPR (8 passes)', 'Conventional', 'No / Yes', '0 / ~10', 'CT / CTR (row c)', 'Rule 140: high intensity = CT.', 'High', 'INCLUDED'),
    ('P2 ZT R0 / Rr', 'Puddling 8 passes + TPR, ZT wheat', 'Puddled TPR', 'Zero tillage', 'No / Yes', '0 / ~10', 'pZT / pCA (row c)', 'Puddled rice + ZT wheat (rule 124).', 'High', 'INCLUDED'),
]
STUDY_INFO = dict(estab=2000, yeardata='2000-2002 (rice 2000-02, wheat 2000-01 to 2002-03)', years='3 (6 samplings; SQI mean derived)', texture='Clay (Vertisol; 56.6 % clay 0-15 cm)',
                  rotation='Rice-wheat', wheatvar='C 306', ricevar='IR 36', N='90 rice / 100 wheat', P='13 / 26 (P)', K='22 / 33 (K)', residue='30 cm stubble retained (~6 t/ha after rice, ~4 t/ha after wheat) vs removed',
                  irrigation='Rice flooded 5 cm; wheat pre-sowing 6 cm + CRI, tillering, flowering', treatments='P0 / P1 / P2 (rice) x CT / ZT (wheat) x Rr / R0, split plot, 3 reps',
                  params='Soil quality index (SQI, 0-15 cm), 3-yr mean per treatment derived exactly from the printed regression lines of Fig. 4 - rows a-c (CT / CTR / pZT / pCA)',
                  supp='None referenced',
                  notes=('NEW serial 323 (ext\\646.pdf). Treatment-level BD, PR, WSA, OM and yields are NOT reported (only pooled yield-property regressions, Figs 1-3) - not extractable. '
                         'SQI means derived from the printed treatment regressions (exact means of the plotted points). Same IISS Bhopal P0 / P1 / P2 puddling trial as ext\\299 / ext\\645 (Mohanty et al. 2004, '
                         'rice 2000-01 only) - that paper was excluded as "no wheat phase"; this paper shows the trial was rice-wheat: author to decide whether 299 / 645 is re-entered as 323 (companion). '
                         'Initial soil 0-15 cm: OM 10.17 g/kg, BD 1.38 Mg/m3 (profile Table 1 to 105 cm).'))
SITES = [('IISS experimental farm, Bhopal', "23 18' N", "77 24' E", 23.3, 77.4, 'Paper', 'ST', None)]
