"""266 (companion) - Sidhu H.S. et al. 2015 Field Crops Res. 184:201-212 (ext 672): Turbo Happy Seeder development + on-farm trials (Punjab), partial repeat of study 266."""
from common import base, notes

ST = dict(
    no=266, serial='266 (companion)', authors='Sidhu H.S., Singh M., Singh Y., Blackwell J., Lohan S.K., Humphreys E., Jat M.L., Singh V. & Singh S.', year=2015, journal='Field Crops Research',
    ref=('Sidhu H.S., Singh M., Singh Y., Blackwell J., Lohan S.K., Humphreys E., Jat M.L., Singh V. & Singh S. (2015) Development and evaluation of the Turbo Happy Seeder for sowing wheat into heavy '
         'rice residues in NW India. Field Crops Research 184:201-212, doi 10.1016/j.fcr.2015.07.025.'),
    doi='10.1016/j.fcr.2015.07.025',
    fert='Farmer-managed on-farm trials (fertiliser as farmer practice); Turbo Happy Seeder sowing into combine-harvested rice residue',
    tmap=('On-farm paired comparisons in Punjab (as study 266, rule 23: rice phase not described): Turbo Happy Seeder (zero-till drilling into loose + anchored rice residue) -> CA ; '
          'farmer practice (stubble shaver + burning + pre-sowing irrigation + 2 disc + 2 tyne passes + planking + drill) -> CT (burnt = no residue, rule 116).'),
    details=('TREATMENTS IN PAPER: Exp. 1 9-row Turbo Happy Seeder v.1 vs farmer practice (2007-08, 4 districts); Exp. 2 7-row vs 9-row Turbo Happy Seeder (Ludhiana 2008-09, 3 sites); '
             'Exp. 3 7-row Turbo Happy Seeder vs farmer practice (Sangrur 2008-09, 7 farms); Exp. 4 9-row Turbo Happy Seeder v.2 vs conventional (2008-10, 11 districts). || MAPPING: '
             'Turbo Happy Seeder -> CA [wheat: ZT into rice residue] | farmer practice -> CT [residue burnt, conventional tillage]'),
)
SITE = dict(country='India (Punjab)', site="Farmers' fields, Punjab (Turbo Happy Seeder trials)", lat=30.25, lon=75.84, climate='ST', duration='0-3 Y', soil='LOAMY')
M = 'Grain from 3 x 10 m2 per field (air-dry); paired t-test; 1 farm = 1 replicate.'


def rows(B):
    st = ST; out = []
    obs, nt = notes(st, ('ROW a: CA = 7-row Turbo Happy Seeder (25.7 cm rows), CT = farmer practice (residue burnt + 4-6 tractor passes + drill). Table 7 wheat grain yield, mean of 7 farms in district Sangrur '
                         '(ranges FP 4.5-6.13, HS 4.12-5.75 t/ha); HS 4.6 % lower (wider rows). PARTIAL REPEAT (rule 136): Tables 5 and 8 (THS v.1 / v.2 vs farmer practice by district, 2007-10) are '
                         'identical to study 266 - not re-entered. Table 6 (7-row vs 9-row HS, both CA) - no tillage contrast.'))
    v = base(st, dict(SITE, site="Farmers' fields, Sangrur district", lat=30.25, lon=75.84), {'year of data collection/experiment': '2008-09', 'YEAR OF DATA (duration)': 'wheat 2008-09'})
    v.update({'WYIELD_CA': 4.98, 'WYIELD_CT': 5.21, 'UNIT': 't/ha (air-dry)', 'Crop/season of sampling': 'Wheat 2008-09', 'Data source': 'Table 7', 'Method used (from paper)': M,
              'Obs': obs, 'Rep': 7, 'Notes/Doubts': nt})
    out.append(('YIELD', B.add_row('YIELD', v)))
    obs, nt = notes(st, ('ROW a: CA = 9-row Turbo Happy Seeder v.2 (2.03 m, 506 kg, 33.6 kW tractor), CT = seed-cum-fertiliser drill used after conventional seedbed preparation. Table 4 EFFECTIVE FIELD CAPACITY of the '
                         'sowing machine (sowing operation only; CT seedbed operations: disc harrow 0.71, cultivator 0.70, planker 0.71, stubble shaver 0.59 ha/h; no-till drill 0.62 ha/h) - FLAG. '
                         'Fuel use (l/ha): THS 11.63, seed drill 5.56, disc 4.93, cultivator 5.00, planker 4.93, stubble shaver 5.94. Energy for establishment (Table 9): THS 1584 vs farmer practice 9217 MJ/ha (83 % saving) - no sheet.'))
    v = base(st, SITE, {'year of data collection/experiment': '2008-10', 'YEAR OF DATA (duration)': 'machine evaluation'})
    v.update({'EFC_CA': 0.30, 'EFC_CT': 0.63, 'UNIT': 'ha/h (effective field capacity of the sowing machine)', 'Crop/season of sampling': 'Wheat sowing', 'Data source': 'Table 4',
              'Method used (from paper)': 'EFC = S x W / 10 x field efficiency (Kepner et al. 1980).', 'Obs': obs, 'Rep': 1, 'Notes/Doubts': nt})
    out.append(('MACHINE FIELD CAPACITY', B.add_row('MACHINE FIELD CAPACITY', v)))
    return out


TM = [
    ('Turbo Happy Seeder (7-row / 9-row v.1 / v.2)', 'Zero-till drilling of wheat into combine-harvested rice residue', 'Not described (farmer fields)', 'Zero tillage', 'Yes', None, 'CA', 'As study 266 (rule 23).', 'High', 'INCLUDED'),
    ('Farmer practice', 'Stubble shaver, burning, pre-sowing irrigation, 2 disc + 2 tyne passes + planking, drill', 'Not described', 'Conventional', 'Burnt', '0', 'CT', 'Burnt = no residue (rule 116).', 'High', 'INCLUDED'),
]
STUDY_INFO = dict(estab=2007, yeardata='Wheat 2007-08 to 2009-10 (on-farm)', years='Year-wise district means', texture='Loamy sand to clay loam (farm sites)', rotation='Rice-wheat',
                  wheatvar='Not reported', ricevar='Not reported', N='Farmer practice', P='Farmer practice', K='Farmer practice', residue='Rice residue retained (HS) vs burnt (FP)',
                  irrigation='Farmer practice (pre-sowing irrigation in FP only)', treatments='Happy Seeder versions vs farmer practice (on-farm, farms = replicates)', supp='None',
                  params='Wheat yield Sangrur 2008-09 (Table 7, 7-row HS vs FP); sowing-machine effective field capacity (Table 4) - new data only',
                  notes=('COMPANION of study 266 (ext\\672.pdf) - PARTIAL REPEAT (rule 136): district yields of Tables 5 and 8 = study 266 rows (identical values), not re-entered. '
                         'NOT ON A SHEET: energy budget (Table 9), canopy temperature (FP 32.3 vs HS 30.4 C, March 2010), machine design data (Tables 1-2). '
                         'Table 6 7-row vs 9-row HS (both CA): loamy sand 3.71 / 4.17, sandy loam 3.93 / 4.55, clay loam 5.03 / 4.93 t/ha - no contrast.'))
SITES = [("Farmers' fields, Sangrur district", 'not reported', 'not reported', 30.25, 75.84, 'Geocoded (district HQ) - FLAG', 'ST', 'Exp. 3 (Table 7)')]
