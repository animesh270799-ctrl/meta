"""Study 319 - Manpreet-Singh et al. 2024 Sci Rep 14:11747 (ext 641): PAU Smart Seeder."""
from common import base, notes

ST = dict(
    no=319, serial=319,
    authors='Manpreet-Singh, Chaleka A.T., Goyal R., Gupta N., Singh A., Singh M., Sharma S., Dixit A.K., Malik A., Al-Ansari N. & Mattar M.A.',
    year=2024, journal='Scientific Reports',
    ref=('Manpreet-Singh, Chaleka A.T., Goyal R., Gupta N., Singh A., Singh M., Sharma S., Dixit A.K., Malik A., '
         'Al-Ansari N. & Mattar M.A. (2024) PAU Smart Seeder: a novel way forward for rice residue management in '
         'North-west India. Scientific Reports 14:11747, doi 10.1038/s41598-024-62337-z.'),
    doi='10.1038/s41598-024-62337-z',
    fert='120 kg N/ha (urea top-dressed in 2 splits before 1st and 2nd irrigation) + 60 kg P2O5/ha as DAP at sowing; seed 120 kg/ha; PAU package of practices',
    tmap=('Rice (combine-harvested with Super SMS; rice tillage NOT described -> rule 23, wheat phase decides). '
          'HS (Turbo Happy Seeder, zero-till drilling into full rice residue, surface mulch) -> CA ; '
          'PSS (PAU Smart Seeder: strip-till rotor tills 75 mm strips ahead of disc openers, inter-row residue left as mulch) -> MTR (row a; rule 16 strip till) ; '
          'SS (Super Seeder: single-pass rotavator-seeder incorporating 80-90 % of residue) -> MTR (row b; rules 13 / 69 Super Seeder = MT/MTR - FLAG: study 273 coded a Super Seeder treatment CTR) ; '
          'CT (Exp. 3 only: conventional till sowing after rice straw removal) -> CT.'),
    details=('TREATMENTS IN PAPER: Exp. 1 PSS x straw load (4.2 / 5.2 / 6.0 t/ha) x speed index (R1-R3), RCBD 3 reps (PSS only - no tillage contrast, not entered); '
             'Exp. 2 PSS vs SS vs HS at Location 1 (PAU FMPE farm, Ludhiana, straw 6.0 t/ha, PBW 725, sown 9 Nov 2019) and Location 2 (PAU Seed Farm Ladhowal, straw 5.9 t/ha, PBW 1-Zn, sown 18 Nov 2019), 3 reps; '
             'Exp. 3 (2020-21) PSS, HS, SS and CT (after straw removal), loamy sand, straw 7.1 t/ha, PBW 725 sown 11 Nov 2020, CRD within block, 3 reps; '
             'Exp. 4 on-farm 2020-21: PSS vs HS (8 farms) and PSS vs SS (2 farms). || MAPPING: '
             'HS -> CA: Turbo Happy Seeder, zero-till drill into anchored + loose rice residue retained as mulch [rice phase: not described; wheat phase: zero tillage; residue: Yes - full rice straw 5.9-7.1 t/ha] | '
             'PSS -> MTR (row a): strip-till rotor (J blades, 188 rpm) tills 75 mm strips, paired passive disc openers, furrow-closing roller; inter-row residue as mulch [rice phase: not described; wheat phase: strip tillage (32.5-37.5 % of width); residue: Yes] | '
             'SS -> MTR (row b): Super Seeder, rotavator (LJF blades) + seed drill, single pass, incorporates 80-90 % of straw [rice phase: not described; wheat phase: single-pass rotary (Super Seeder) - rule 13 MT family; residue: Yes, incorporated] | '
             'CT -> CT: conventional till sowing after rice straw removal (Exp. 3) [rice phase: not described; wheat phase: conventional; residue: No - removed]'),
)

FERT = ST['fert']
S_LDH = dict(country='India (Punjab)', site='PAU Dept. Farm Machinery & Power Engineering research farm, Ludhiana',
             lat=30.9, lon=75.8, climate='TEMP', duration='0-3 Y', soil=None)
S_LAD = dict(country='India (Punjab)', site='PAU Seed Farm, Ladhowal (Ludhiana)', lat=30.99, lon=75.74,
             climate='TEMP', duration='0-3 Y', soil=None)
S_EXP3 = dict(S_LDH, soil='SANDY', site='PAU, Ludhiana (Exp. 3 field; location not stated - assumed PAU research farm, FLAG)')
S_FARM = dict(country='India (Punjab)', site='Farmers\' fields, 8 locations (Ludhiana, Sangrur, Kapurthala, Fatehgarh Sahib districts)',
              lat=30.95, lon=75.6, climate='TEMP', duration='0-3 Y', soil=None)

SITES = [S_LDH, S_LAD, S_FARM]
RICE_NOT = 'Rice phase not described (rule 23; wheat-phase coding).'


def rows(B):
    st = ST
    out = []

    def add(sheet, site, vals, body, y=1, t=1, d=1, rep=3, **kw):
        obs, nt = notes(st, body, y, t, d)
        v = base(st, site, kw)
        v.update(vals)
        v['Obs'] = obs
        v['Rep'] = rep
        v['Notes/Doubts'] = nt
        out.append((sheet, B.add_row(sheet, v)))

    yd19 = {'year of data collection/experiment': '2019-20', 'YEAR OF DATA (duration)': 'wheat 2019-20'}
    yd20 = {'year of data collection/experiment': '2020-21', 'YEAR OF DATA (duration)': 'wheat 2020-21'}
    m_yield = 'Grain yield at maturity (t/ha) from replicated plots; harvest area and moisture basis not stated.'

    # ---- Exp 2 Location 1 (PAU Ludhiana) - Table 4 yield
    for tag, mtr, mlab, se in (('a', 5.03, 'PSS', '0.093'), ('b', 4.39, 'SS', '0.107')):
        add('YIELD', S_LDH, {'WYIELD_CA': 4.08, 'WYIELD_MTR': mtr, 'UNIT': 't/ha',
                             'Crop/season of sampling': 'Wheat 2019-20 (sown 9 Nov 2019, harvest)',
                             'Data source': 'Table 4', 'Method used (from paper)': m_yield,
                             'Fertilizer dose & other management': FERT + '; rice PR 121 combine-harvested with Super SMS, straw load 6.0 t/ha; wheat PBW 725; plots 50 m2'},
            f"ROW {tag}: CA = HS, MTR = {mlab}. Exp. 2 Location 1 (PAU FMPE farm). Table 4 grain yield (mean +/- SE: PSS 5.03 +/- 0.093, SS 4.39 +/- 0.107, HS 4.08 +/- 0.031). "
            f"{RICE_NOT} SS coded MTR under the rotary rule (Super Seeder) - FLAG. Seedling emergence, weed density / biomass, fuel and field capacity (Tables 3-4): no sheet.",
            t=2, **yd19)
    # ---- Exp 2 Location 2 (Ladhowal) - Table 5
    lad_fert = FERT + '; rice genotype RYT 3468 combine-harvested, straw 5.9 t/ha; wheat PBW 1-Zn sown 18 Nov 2019; subplots 200 m2'
    t5 = {'PSS': dict(psd=97, rs=0.22, spl=10.9, gps=46.0, tgw=40.0, gy=4.84),
          'SS': dict(psd=82, rs=0.225, spl=11.6, gps=48.0, tgw=39.0, gy=4.68),
          'HS': dict(psd=83, rs=0.225, spl=10.6, gps=57.0, tgw=39.2, gy=4.43)}
    for tag, m in (('a', 'PSS'), ('b', 'SS')):
        h, x = t5['HS'], t5[m]
        body = (f"ROW {tag}: CA = HS, MTR = {m}. Exp. 2 Location 2 (PAU Seed Farm Ladhowal). {RICE_NOT} "
                "SS coded MTR under the rotary rule (Super Seeder) - FLAG.")
        add('YIELD', S_LAD, {'WYIELD_CA': h['gy'], 'WYIELD_MTR': x['gy'], 'UNIT': 't/ha',
                             'Crop/season of sampling': 'Wheat 2019-20 (sown 18 Nov 2019, harvest)', 'Data source': 'Table 5',
                             'Method used (from paper)': m_yield, 'Fertilizer dose & other management': lad_fert},
            body + ' Table 5 grain yield (+/- SE: PSS 0.22, SS 0.07, HS 0.29; differences NS).', t=2, **yd19)
        add('PANICLE-SPIKE DENSITY', S_LAD, {
            'PSD_WCA': f"=ROUND({h['psd']}/{h['rs']},1)", 'PSD_WMTR': f"=ROUND({x['psd']}/{x['rs']},1)",
            'UNIT': 'no./m2 (DERIVED: printed spikes per m row length / row spacing in m - HS / SS 0.225 m, PSS 0.22 m, Table 9)',
            'Crop/season of sampling': 'Wheat 2019-20, at harvest', 'Data source': 'Table 5 (DERIVED unit conversion)',
            'Method used (from paper)': 'Spike density counted per m row length at harvest; converted with the machine row spacing (Table 9).',
            'Fertilizer dose & other management': lad_fert},
            body + f" Spike density printed per m row length: HS {h['psd']}, {m} {x['psd']} (+/- SE PSS 1.1, SS 2.1, HS 2.5) - converted to per m2 (DERIVED, FLAG).", t=2, **yd19)
        add('PANICLE-SPIKE LENGTH', S_LAD, {'SPL_WCA': h['spl'], 'SPL_WMTR': x['spl'], 'UNIT': 'cm (wheat spike length)',
                                             'Crop/season of sampling': 'Wheat 2019-20, at harvest', 'Data source': 'Table 5',
                                             'Method used (from paper)': 'Spike length measured at harvest (method not detailed).',
                                             'Fertilizer dose & other management': lad_fert},
            body + ' Table 5 spike length (+/- SE PSS 0.3, SS 0.4, HS 0.2; NS).', t=2, **yd19)
        add('GRAINS PER PANICLE', S_LAD, {'GPP_WCA': h['gps'], 'GPP_WMTR': x['gps'], 'UNIT': 'grains per spike (wheat)',
                                           'Crop/season of sampling': 'Wheat 2019-20, at harvest', 'Data source': 'Table 5',
                                           'Method used (from paper)': 'Grains per spike counted at harvest (method not detailed).',
                                           'Fertilizer dose & other management': lad_fert},
            body + ' Table 5 grains per spike (+/- SE PSS 1.9, SS 5.5, HS 6.1; NS).', t=2, **yd19)
        add('1000-GRAIN WEIGHT', S_LAD, {'TGW_WCA': h['tgw'], 'TGW_WMTR': x['tgw'], 'UNIT': 'g',
                                          'Crop/season of sampling': 'Wheat 2019-20, at harvest', 'Data source': 'Table 5',
                                          'Method used (from paper)': '1000-grain weight at harvest (method not detailed).',
                                          'Fertilizer dose & other management': lad_fert},
            body + ' Table 5 1000-grain weight (+/- SE PSS 0.3, SS 0.0, HS 0.2).', t=2, **yd19)

    # ---- Exp 3 (2020-21) - Table 7: CT, HS, SS, PSS
    e3fert = FERT + '; rice straw load 7.1 t/ha; wheat PBW 725 sown 11 Nov 2020, harvested 2nd week April 2021; loamy sand'
    t7 = {'HS': (55.2, 383, 41.8, 4.78), 'SS': (58.8, 369, 39.0, 4.36), 'PSS': (61.8, 365, 39.4, 4.73), 'CT': (56.8, 396, 40.8, 4.28)}
    for tag, m in (('a', 'PSS'), ('b', 'SS')):
        h, x, c = t7['HS'], t7[m], t7['CT']
        body = (f"ROW {tag}: CT = conventional till after straw removal, CA = HS, MTR = {m}. Exp. 3 (2020-21; field location not stated - "
                f"assumed PAU Ludhiana, loamy sand, FLAG). {RICE_NOT} SS coded MTR under the rotary rule (Super Seeder) - FLAG.")
        add('YIELD', S_EXP3, {'WYIELD_CT': c[3], 'WYIELD_CA': h[3], 'WYIELD_MTR': x[3], 'UNIT': 't/ha',
                              'Crop/season of sampling': 'Wheat 2020-21, harvest (April 2021)', 'Data source': 'Table 7',
                              'Method used (from paper)': m_yield, 'Fertilizer dose & other management': e3fert},
            body + ' Table 7 grain yield (+/- SE: HS 0.01, SS 0.07, PSS 0.33, CT 0.10).', t=2, **yd20)
        add('GRAINS PER PANICLE', S_EXP3, {'GPP_WCT': c[0], 'GPP_WCA': h[0], 'GPP_WMTR': x[0], 'UNIT': 'grains per spike (wheat)',
                                            'Crop/season of sampling': 'Wheat 2020-21, at maturity', 'Data source': 'Table 7',
                                            'Method used (from paper)': 'Yield contributing characters recorded at maturity (method not detailed).',
                                            'Fertilizer dose & other management': e3fert},
            body + ' Table 7 grains per spike (+/- SE: HS 4.4, SS 3.7, PSS 1.9, CT 4.6).', t=2, **yd20)
        add('PANICLE-SPIKE DENSITY', S_EXP3, {'PSD_WCT': c[1], 'PSD_WCA': h[1], 'PSD_WMTR': x[1],
                                               'UNIT': 'no./m2 (TILLER density printed - FLAG, taken as productive tillers / spikes at maturity)',
                                               'Crop/season of sampling': 'Wheat 2020-21, at maturity', 'Data source': 'Table 7',
                                               'Method used (from paper)': 'Tiller density (per m2) recorded at maturity (method not detailed).',
                                               'Fertilizer dose & other management': e3fert},
            body + ' Table 7 tiller density per m2 (+/- SE: HS 14.7, SS 27.1, PSS 12.4, CT 28.9) - entered as spike density (FLAG).', t=2, **yd20)
        add('1000-GRAIN WEIGHT', S_EXP3, {'TGW_WCT': c[2], 'TGW_WCA': h[2], 'TGW_WMTR': x[2], 'UNIT': 'g',
                                           'Crop/season of sampling': 'Wheat 2020-21, at maturity', 'Data source': 'Table 7',
                                           'Method used (from paper)': '1000-grain weight at maturity (method not detailed).',
                                           'Fertilizer dose & other management': e3fert},
            body + ' Table 7 1000-grain weight (+/- SE: HS 0.5, SS 0.9, PSS 0.7, CT 1.0).', t=2, **yd20)

    # ---- Exp 4 on-farm (Table 8): PSS vs HS, 8 farms
    farms = ('Samrala PSS 5.04 / HS 5.04; Kheri 5.13 / 4.90; Surkhpur 5.50 / 5.38; Teerewal 5.63 / 5.50; Jaitowal 4.61 / 4.55; '
             'Mehsampur 4.45 / 4.89; Thablan 5.25 / 5.21; Rajoan 5.36 / 5.31')
    add('YIELD', S_FARM, {'WYIELD_CA': 5.10, 'WYIELD_MTR': 5.12, 'UNIT': 't/ha',
                          'Crop/season of sampling': 'Wheat 2020-21 on-farm (sown 31 Oct - 10 Nov 2020)', 'Data source': 'Table 8',
                          'Method used (from paper)': 'On-farm paired strips (0.2-6.6 ha); wheat yield per farm (method not detailed).',
                          'Fertilizer dose & other management': 'Farmers\' management; varieties PBW 677, DBW 187, HD 3086, PBW 725, Unnat PBW 343'},
        f"ROW a: CA = HS, MTR = PSS. ON-FARM paired trials (rule 117: farms = replicates, Rep = 8; paper's stated mean of n = 8). Farm values (PSS / HS, t/ha): {farms}. "
        f"PSS vs SS on 2 farms (Kedi Bhamal 4.67 / 4.47; Kattu 5.13 / 4.94; mean 4.90 vs 4.71) NOT entered - both MTR, no code contrast. {RICE_NOT}",
        rep=8, **yd20)
    return out


TM = [  # label, description, rice, wheat, residue, rate, code, rationale, confidence, status
    ('HS (Happy Seeder)', 'Turbo Happy Seeder zero-till drilling of wheat into combine-harvested rice residue (anchored + loose, Super SMS), residue retained as surface mulch.',
     'Not described (combine-harvested rice)', 'Zero tillage (Happy Seeder)', 'Yes - surface mulch', '5.9-7.1', 'CA',
     'Zero-till wheat with full residue retention; rice phase not described -> wheat phase decides (rule 23).', 'High', 'INCLUDED'),
    ('PSS (PAU Smart Seeder)', 'Strip-till rotor with J blades tills 75 mm strips ahead of paired passive disc openers (32.5-37.5 % of width); straw in strips incorporated, inter-row straw left as mulch.',
     'Not described', 'Strip tillage', 'Yes - partly incorporated, mostly mulch', '5.9-7.1', 'MTR (row a)',
     'Strip / zone tillage with residue -> MTR (rule 16; study 41 / 273 Smart Seeder = MTR).', 'High', 'INCLUDED'),
    ('SS (Super Seeder)', 'Super Seeder: rotavator (LJF blades) with seed drill, single pass, complete tillage of the machine width incorporating 80-90 % of the straw.',
     'Not described', 'Single-pass rotary seeder (Super Seeder)', 'Yes - incorporated', '5.9-7.1', 'MTR (row b) - FLAG',
     'Rules 13 / 69: Super Seeder = MT family (MTR with residue). FLAG: study 273 coded a Super Seeder treatment CTR; author to confirm.', 'Medium', 'INCLUDED'),
    ('CT (conventional till, Exp. 3)', 'Conventional till sowing after rice straw removal (2020-21 experiment only).',
     'Not described', 'Conventional tillage', 'No - removed', '0', 'CT', 'Conventional tillage without residue.', 'High', 'INCLUDED'),
    ('Exp. 1 PSS x straw load x speed index', 'PSS evaluated at 3 straw loads x 3 speed indices (fuel, field capacity, slip, emergence, weeds, yield - Tables 1-2).',
     'Not described', 'Strip tillage (PSS only)', 'Yes (4.2 / 5.2 / 6.0 t/ha)', '4.2-6.0', 'NOT CODED',
     'Single machine - no tillage-code contrast (straw load is a residue-amount factor within MTR).', 'High', 'NOT ENTERED'),
    ('Exp. 4 PSS vs SS (2 farms)', 'On-farm comparison PSS vs Super Seeder at 2 farms (Table 8).',
     'Not described', 'Strip till vs Super Seeder', 'Yes', None, 'NOT CODED', 'Both MTR - no code contrast; values in YIELD notes.', 'High', 'NOT ENTERED'),
]

STUDY_INFO_EXTRA = dict(
    estab=2019, yeardata='2019-20, 2020-21', years='2 wheat seasons (2019-20 Exp. 1-2; 2020-21 Exp. 3-4)',
    texture='Loamy sand (Exp. 3 field only; Exp. 2 soils not described)', rotation='Rice-wheat (rice tillage not described)',
    wheatvar='PBW 725 (Exp. 1-3), PBW 1-Zn (Exp. 2 Ladhowal); farms PBW 677, DBW 187, HD 3086, PBW 725, Unnat PBW 343',
    ricevar='PR 121 (Exp. 1-2 Location 1), RYT 3468 (Ladhowal)', N='120', P='60 P2O5', K='Not reported',
    residue='Rice straw (combine + Super SMS) 6.0 t/ha (Loc. 1), 5.9 t/ha (Loc. 2), 7.1 t/ha (Exp. 3); retained in HS / PSS / SS; removed in CT',
    irrigation='Irrigated (PAU recommendations)',
    treatments='Exp. 2: PSS, SS, HS (3 reps, 2 locations); Exp. 3: PSS, HS, SS, CT (3 reps); Exp. 4: on-farm PSS vs HS (8) / SS (2); Exp. 1: PSS x straw load x speed (machine test)',
    params=('Wheat grain yield (Exp. 2 both locations, Exp. 3, on-farm mean); spike density (per m row -> per m2, derived), spike length, grains per spike, 1000-grain weight (Ladhowal); '
            'grains per spike, tiller density, 1000-grain weight (Exp. 3) - HS = CA vs PSS / SS = MTR rows a / b; CT in Exp. 3'),
    supp='Supplementary Fig. 1s (emergence photographs) referenced - not downloaded (author permission needed); no data tables',
    notes=('NEW serial 319 (ext\\641.pdf). Machine-evaluation paper: emergence count, weed density / biomass, fuel consumption, field capacity, wheel slip and energy budget (Tables 1-4, 6): no sheet. '
           'Exp. 1 (PSS only) not entered. Super Seeder coded MTR under rules 13 / 69 (FLAG vs study 273 CTR coding). Soil, climate and initial soil properties not reported. '
           'Rep = 3 (stated); on-farm Rep = 8 farms (rule 117). 2 PSS vs SS farms in notes only (both MTR).'),
)
