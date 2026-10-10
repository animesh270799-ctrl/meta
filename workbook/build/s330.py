"""Study 330 - Sharma R.K., Srinivasa Babu K., Chhokar R.S. & Sharma A.K. 2004 Crop Prot. 23:1049-1054 (ext 668): rice tillage x wheat tillage, DWR Karnal."""
from common import base, notes

ST = dict(
    no=330, serial=330, authors='Sharma R.K., Srinivasa Babu K., Chhokar R.S. & Sharma A.K.', year=2004, journal='Crop Protection',
    ref=('Sharma R.K., Srinivasa Babu K., Chhokar R.S. & Sharma A.K. (2004) Effect of tillage on termites, weed incidence and productivity of spring wheat in rice-wheat system of North Western '
         'Indian plains. Crop Protection 23:1049-1054, doi 10.1016/j.cropro.2004.03.008.'),
    doi='10.1016/j.cropro.2004.03.008',
    fert='Wheat PBW 343, 100 kg seed/ha, sown 7 / 10 Nov; fertiliser not stated; weed-free plots for yield (weedy check strips for weed counts)',
    tmap=('Split plot, 3 reps (20 m2 sub plots), DWR Karnal rabi 2000-01 and 2001-02. Rice main plots: PH puddling harrow (2 disc harrowings + 2 cultivator + 2 harrowings in ponded water + planking; '
          'high-intensity puddling, CT rice) ; DH dry harrow (2 harrowings + 2 cultivator + ponding + planking, unpuddled tilled rice) ; DR dry rotavator (single rotary pass, unpuddled; reduced) ; '
          'PR puddling rotavator (single rotary pass in ponded water; LOW-intensity puddling, rule 140 = MT rice). Wheat sub plots: conventional (10 operations) -> CT ; zero-till ferti-seed drill -> pZT '
          '(after tilled rice, rules 124 / 138) ; rotary till ferti-seed drill (single pass) -> pMT after PH / DH (CT-tilled rice) and MT after DR / PR (reduced-till rice, rules 13 / 135 / 140 - FLAG) ; '
          'FIRBS (raised beds after conventional preparation) -> EXCLUDED (planting geometry on conventionally tilled land, as 653 / study 6). '
          '2000-01: cell means (Table 5, interaction significant); 2001-02: wheat-tillage main effects pooled over rice tillage (interaction NS) - FLAG.'),
    details=('TREATMENTS IN PAPER: rice tillage (main) puddling rotavator / puddling harrow / dry rotavator / dry harrow x wheat tillage (sub) zero tillage / rotary tillage / FIRBS / conventional (split plot, 3 reps). '
             '|| MAPPING: conventional -> CT [rice: any; wheat: 10 tractor operations] | zero tillage -> pZT [rice: tilled (puddled or dry-tilled); wheat: ZT drill] | rotary tillage -> pMT [rice: PH / DH] or MT '
             '[rice: DR / PR reduced] [wheat: single-pass rotary till drill] | FIRBS -> EXCLUDED [beds after conventional preparation]'),
)
SITE = dict(country='India (Haryana)', site='Directorate of Wheat Research farm, Karnal', lat=29.717, lon=76.967, climate='ST', duration='0-3 Y', soil='LOAMY',
            CLAY=3.7, sand=63.0, silt=33.3, **{'ph (initial)': 8.7, 'soc (initial)': 3.9})
RICE = (('PR', 'puddling rotavator (low-intensity puddling - MT rice, rule 140)', 'MT'), ('PH', 'puddling harrow (intensive puddling)', 'pMT'),
        ('DR', 'dry rotavator (single dry rotary pass, unpuddled - reduced)', 'MT'), ('DH', 'dry harrow (dry harrowing / cultivation, unpuddled)', 'pMT'))
# Table 5 wheat yield 2000-01 (t/ha): [ZT, rotary, FIRBS, CT] per rice tillage (PR, PH, DR, DH)
T5 = {'PR': (5.97, 6.07, 5.57, 6.32), 'PH': (5.92, 6.06, 5.18, 6.17), 'DR': (5.87, 6.12, 5.21, 6.33), 'DH': (6.03, 6.47, 5.57, 5.85)}
M = 'Weed-free plots; whole-plot harvest; termite-damaged tillers removed / threshed with the plot harvest.'


def rows(B):
    st = ST; out = []

    def add(vals, body, src, crop, yd, t=1):
        obs, nt = notes(st, body, t=t)
        v = base(st, SITE, {'year of data collection/experiment': yd, 'YEAR OF DATA (duration)': yd,
                            'RAIN FALL': 69.0 if yd.startswith('2000') else 80.3})
        v.update(vals)
        v.update({'UNIT': 't/ha', 'Crop/season of sampling': crop, 'Data source': src, 'Method used (from paper)': M, 'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
        out.append(('YIELD', B.add_row('YIELD', v)))

    for k, (rk, rdesc, rot) in enumerate(RICE):
        zt, ro, fi, ct = T5[rk]
        add({'WYIELD_CT': ct, 'WYIELD_pZT': zt, f'WYIELD_{rot}': ro},
            f'ROW {"abcd"[k]}: rice {rk} = {rdesc}; CT = conventional wheat, pZT = zero-till wheat, {rot} = rotary-till wheat (single pass). Table 5 wheat grain yield CELL MEANS 2000-01 '
            f'(interaction significant). FIRBS (excluded) {fi} t/ha. Termite-damaged tillers / 20 m2 (Table 4, no sheet): ZT / rotary / FIRBS / CT see Study_Info.',
            'Table 5', 'Wheat 2000-01', '2000-01')
    add({'WYIELD_CT': 6.31, 'WYIELD_pZT': 6.41, 'WYIELD_pMT': 6.72},
        'ROW e: CT = conventional, pZT = zero tillage, pMT = rotary tillage. Table 3 wheat yield 2001-02, WHEAT-TILLAGE MAIN EFFECTS pooled over the 4 rice tillage options (interaction NS) - FLAG; '
        'rotary coded pMT although 2 of 4 rice options (DR / PR) would make it MT - FLAG. FIRBS (excluded) 6.04 t/ha. 2000-01 main effects (ZT 5.95, rotary 6.18, FIRBS 5.38, CT 6.17) not entered (cells used).',
        'Table 3', 'Wheat 2001-02', '2001-02', t=4)
    return out


TM = [
    ('Puddling rotavator (rice)', 'Ponding + single rotary pass', 'Low-intensity puddling (MT, rule 140)', 'Sub plots', 'Not stated', None, 'Rice phase of rows a', 'Rule 140.', 'Medium', 'INCLUDED'),
    ('Puddling harrow (rice)', '2 disc harrowings + 2 cultivator passes, ponding, 2 harrowings in ponded water + planking', 'Intensive puddling (CT)', 'Sub plots', 'Not stated', None, 'Rice phase of rows b', 'Puddled.', 'High', 'INCLUDED'),
    ('Dry rotavator (rice)', 'Single dry rotary pass, ponding (no puddling)', 'Reduced-till unpuddled', 'Sub plots', 'Not stated', None, 'Rice phase of rows c', 'Single-pass rotary = MT (rule 13).', 'Medium', 'INCLUDED'),
    ('Dry harrow (rice)', '2 harrowings + 2 cultivator passes dry, ponding + planking', 'Tilled unpuddled', 'Sub plots', 'Not stated', None, 'Rice phase of rows d', 'Tilled rice (rule 138).', 'High', 'INCLUDED'),
    ('Conventional tillage (wheat)', '10 tractor operations (4 harrow, 4 cultivator, 2 planking)', 'All rice options', 'Conventional', 'Not stated', None, 'CT', 'Conventional.', 'High', 'INCLUDED'),
    ('Zero tillage (wheat)', 'Zero-till ferti-seed drill with inverted-T openers', 'All rice options (tilled)', 'Zero tillage', 'Not stated', None, 'pZT', 'Tilled / puddled rice + ZT wheat (rules 124 / 138).', 'High', 'INCLUDED'),
    ('Rotary tillage (wheat)', 'Rotary till ferti-seed drill, single tractor pass', 'PH / DH -> pMT ; DR / PR -> MT', 'Single-pass rotary', 'Not stated', None, 'pMT / MT - FLAG',
     'Single-pass rotary till drill = MT family (rule 13); partial after CT-tilled rice (rule 124), MT after reduced-till rice (rules 135 / 140).', 'Medium', 'INCLUDED'),
    ('FIRBS (wheat)', 'Raised beds made after conventional field preparation; bed planter', 'All rice options', 'Conventional + beds', 'Not stated', None, 'EXCLUDED',
     'Planting geometry on conventionally tilled land (as 653 bed planting / study 6); values in Notes.', 'Medium', 'EXCLUDED'),
]
STUDY_INFO = dict(estab=2000, yeardata='Wheat 2000-01, 2001-02', years='2 (year-wise)', texture='Deep alluvial silty loam (63 % sand, 33.3 % silt, 3.7 % clay as printed)', rotation='Rice-wheat',
                  wheatvar='PBW 343', ricevar='Not reported', N='Not stated', P='Not stated', K='Not stated', residue='Not stated', irrigation='Flood irrigation (FIRBS furrow irrigated)',
                  treatments='4 rice tillage (main) x 4 wheat tillage (sub), split plot, 3 reps',
                  supp='None',
                  params='Wheat grain yield: 2000-01 cell means (rows a-d: CT / pZT / MT or pMT per rice tillage), 2001-02 wheat-tillage main effects (row e, flagged)',
                  notes=('NEW serial 330 (ext\\668.pdf). FIRBS excluded (beds on conventionally prepared land). NOT ON A SHEET: termite-damaged tillers per 20 m2 (Table 3 wheat tillage 2000-01 / 2001-02: '
                         'ZT 9.67 / 6.33, rotary 19.67 / 4.33, FIRBS 82.33 / 37.67, CT 12.33 / 10.25; Table 2 rice tillage PR 19.67 / 7.17, PH 30.67 / 17.08, DR 24.08 / 15.25, DH 49.58 / 19.08; Table 4 cells), '
                         'weed dry weight / Rumex population (Fig. 3). Rice-tillage main effects on wheat yield (Table 2: PR 5.98 / 6.38, PH 5.83 / 6.38, DR 5.88 / 6.31, DH 5.98 / 6.40 t/ha; NS) - Notes. '
                         'Rice crop establishment not stated (transplanting implied by ponding) and rice yields not reported. Initial soil OC 3.9 g/kg, pH 8.7, Olsen P 18.9, NH4OAc-K 157.8 kg/ha, IR 3.0 mm/h. '
                         'Wheat-season rainfall 69.0 mm (2000-01) and 80.3 mm (2001-02).'))
SITES = [('Directorate of Wheat Research farm, Karnal', "29 43' N", "76 58' E", 29.717, 76.967, 'Paper', 'ST', None)]
EXCLUDED = [
    {'Sheet': 'ALL', 'SERIAL NO': 'ext\\666.pdf = 211 (companion) (not re-entered)', 'Authors': 'Shahzad M., Hussain M., Farooq M., Farooq S., Jabran K. & Nawaz A.', 'Year': 2017,
     'Reason for exclusion': ('COMPLETE REPEAT (rule 136; third submission): Shahzad et al. (2017) Environ. Sci. Pollut. Res. 24:24634-24643, doi 10.1007/s11356-017-0136-6 = the paper already entered as '
                              '211 (companion) (wheat straw, cost, gross / net return, B:C of the rice-wheat system); other cropping systems are not rice-wheat; marginal-rate-of-return analysis has no sheet.'),
     'Full row (header = value)': 'No rows.'},
    {'Sheet': 'ALL', 'SERIAL NO': 'ext\\667.pdf = 72 (excluded) (not re-entered)', 'Authors': 'Tripathi R.P., Sharma P. & Singh S.', 'Year': 2007,
     'Reason for exclusion': ('COMPLETE REPEAT (rule 136; fourth copy): Tripathi et al. (2007) Soil Tillage Res. 92:221-226, doi 10.1016/j.still.2006.03.008 = study 72 (excluded: rice-season values pooled over the ZT / CT '
                              'wheat sub plots and wheat-season values are ZT vs CT marginal means over all rice tillage x residue treatments, incl. the DSWP + CT wheat mismatch - rule 65). Not re-entered; the trial\'s '
                              'cell values are in 72 (companion).'),
     'Full row (header = value)': 'No rows.'},
]
