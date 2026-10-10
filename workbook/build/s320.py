"""Study 320 - Meena R.P. et al. 2020 Agronomy 10:434 (ext 642): rice residue retention x irrigation x foliar K."""
from common import base, notes

ST = dict(
    no=320, serial=320,
    authors='Meena R.P., Venkatesh K., Khobra R., Tripathi S.C., Prajapat K., Sharma R.K. & Singh G.P.',
    year=2020, journal='Agronomy',
    ref=('Meena R.P., Venkatesh K., Khobra R., Tripathi S.C., Prajapat K., Sharma R.K. & Singh G.P. (2020) Effect of rice residue '
         'retention and foliar application of K on water productivity and profitability of wheat in North West India. '
         'Agronomy 10(3):434, doi 10.3390/agronomy10030434.'),
    doi='10.3390/agronomy10030434',
    fert='150 kg N + 60 kg P2O5 + 30 kg K2O/ha (P, K and part N as 12:32:16 broadcast and incorporated with the last ploughing; rest N top-dressed); HD 2967, ~250 plants/m2, Bhopal drill, 20 cm rows; sown 20 Nov 2015, 22 Nov 2016, 29 Nov 2017',
    tmap=('Split-split plot, 3 reps, 8 x 2 m plots, ICAR-IIWBR Karnal, wheat 2015-16 to 2017-18. Main plot: rice residue retention (RRR, 4 t/ha anchored residue left by the combine) vs control (residue removed). '
          'Field prepared by ploughing (P and K incorporated with the last ploughing) and sown with the Bhopal seed drill -> residue removed = CT ; RRR = CTR (FLAG: tillage only implied by the fertiliser-incorporation sentence; if the author reads RRR wheat as no-till, recode CT/CTR -> ZT/CA). '
          'Irrigation (ICS / ICS+IFS / IAS) = rows a / b / c; foliar K (2 % K2SO4 vs none) pooled (R x K NS, no cell means). Rice phase not described (rule 23).'),
    details=('TREATMENTS IN PAPER: main plot residue: RRR (rice residue retained, 4 t/ha anchored) vs residue removal (control); sub plot irrigation: ICS (1 irrigation at CRI, Zadoks 21), ICS + IFS (CRI + flowering, Zadoks 60), '
             'IAS (6 irrigations: CRI, late tillering, late jointing, flowering, milking, dough); sub-sub plot: foliar K (2 % K2SO4 at Zadoks 40 and 60, 400 L/ha) vs no spray; split-split plot, 3 reps. || MAPPING: '
             'Residue removal -> CT: conventional field preparation (ploughing), rice residue removed [rice phase: not described; wheat phase: conventional (ploughing implied); residue: No] | '
             'RRR -> CTR: same field preparation with 4 t/ha anchored rice residue retained [rice phase: not described; wheat phase: conventional (ploughing implied) - FLAG; residue: Yes, 4 t/ha anchored] | '
             'Irrigation levels ICS / ICS+IFS / IAS -> rows a / b / c (non-tillage factor, rule 33) | Foliar K vs control -> pooled (R x K NS; no R x K cell means printed)'),
)
SITE = dict(country='India (Haryana)', site='ICAR-Indian Institute of Wheat and Barley Research research farm, Karnal',
            lat=29.717, lon=76.967, climate='ST', duration='0-3 Y', soil='LOAMY',
            CLAY=10.2, sand=63.1, silt=26.7, **{'RAIN FALL': 744, 'AVG T': 23.5, 'MIN TEMP': 17.1, 'MAX TEMP': 29.9,
                                                 'ph (initial)': 7.3, 'soc (initial)': 4.2, 'Bdi': 1.47})
YD = {'year of data collection/experiment': '2015-16 to 2017-18', 'YEAR OF DATA (duration)': 'wheat 2015-16 to 2017-18 (3-yr pooled)'}
RICE_NOT = 'Rice phase not described (rule 23).'
TILL_FLAG = 'CT / CTR coding: tillage only implied (P, K incorporated with the last ploughing) - FLAG.'

IRR = [('a', 'ICS (1 irrigation at CRI)'), ('b', 'ICS + IFS (CRI + flowering)'), ('c', 'IAS (6 irrigations)')]
#           GY CTR,  GY CT,   WUE CTR, WUE CT, NR CTR, NR CT, BCg CTR, BCg CT
CELLS = {'a': (4.807, 4.156, 3.51, 2.99, 522.0, 365.5, 1.53, 1.387),
         'b': (4.888, 4.694, 2.478, 2.395, 544.8, 526.4, 1.540, 1.544),
         'c': (5.972, 5.690, 1.358, 1.296, 797.7, 756.3, 1.755, 1.743)}
SRC = {'a': 'GY, WUE, net return and B:C of residue retention printed in text (4807 / 4156 kg/ha; WUE 3.51 / 2.99; NR 522 US$; B:C 1.53); residue-removal NR and B:C digitised from Fig. 5',
       'b': 'all values digitised from Fig. 5 (raster, calibrated axis; printed-text checks reproduce within 1-2 %)',
       'c': 'GY printed in text (5972 / 5690 kg/ha); WUE, NR and B:C digitised from Fig. 5'}


def rows(B):
    st = ST
    out = []

    def add(sheet, vals, body, y=3, t=2, d=1, **kw):
        obs, nt = notes(st, body, y, t, d)
        v = base(st, SITE, kw)
        v.update(vals)
        v.update({'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
        r = B.add_row(sheet, v)
        out.append((sheet, r))
        return r

    for tag, irr in IRR:
        gy1, gy0, w1, w0, nr1, nr0, bc1, bc0 = CELLS[tag]
        head = (f"ROW {tag}: CT = residue removed, CTR = rice residue retained (4 t/ha), irrigation {irr} (rule 33 cell means of the "
                f"R x I interaction, pooled over foliar K and 3 years). {TILL_FLAG} {RICE_NOT}")
        cs = f'Wheat 2015-16 to 2017-18, irrigation {irr}, harvest (3-yr mean)'
        add('YIELD', {'WYIELD_CT': gy0, 'WYIELD_CTR': gy1, 'UNIT': 't/ha (printed kg/ha / 1000, 14 % moisture)',
                      'Crop/season of sampling': cs, 'Data source': 'Text + Figure 5 (digitised)',
                      'Method used (from paper)': 'Grain yield on 11.2 m2 net plot (1.6 x 7 m) hand-harvested at Zadoks 92, adjusted to 14 % moisture.'},
            head + f' {SRC[tag]}. Residue main effect (Fig. 3, pooled): GY 4858 (CT, digitised) vs 5224 (CTR, text) kg/ha - not entered (cell means used).', **YD)
        add('WUE', {'WUE_WCT': f'=ROUND({w0}*10,2)', 'WUE_WCTR': f'=ROUND({w1}*10,2)',
                    'UNIT': 'kg/ha/mm (printed kg/m3 x 10; water = irrigation + rainfall + soil water at sowing)',
                    'Crop/season of sampling': cs, 'Data source': 'Text + Figure 5 (digitised)',
                    'Method used (from paper)': 'WUE = GY / Q, Q = irrigation (Cutthroat Parshall flume) + rainfall + available soil water at sowing (m3/ha).'},
            head + f' WUE printed in kg/m3: CTR {w1}, CT {w0}; {SRC[tag]}. RWC (flag leaf, relative water content) in Fig. 5 - no sheet (rule 59).', **YD)
        add('NET RETURN', {'NR_WCT': nr0, 'NR_WCTR': nr1, 'UNIT': 'US$/ha (INR converted at 68.8 INR/US$)',
                           'Crop/season of sampling': cs, 'Data source': 'Text + Figure 5 (digitised)',
                           'Method used (from paper)': 'Net return = gross (grain x 267.4 + straw x 36.3 US$/t) - cost of cultivation (inputs, rental value of land, interest, depreciation).'},
            head + f' {SRC[tag]}.', **YD)
        add('BC ratio', {'BC_WCT': f'=ROUND({bc0}-1,3)', 'BC_WCTR': f'=ROUND({bc1}-1,3)', 'UNIT': 'ratio (net / cost; printed gross / cost - 1, rule 57)',
                         'Crop/season of sampling': cs, 'Data source': 'Text + Figure 5 (digitised; converted)',
                         'Method used (from paper)': 'B:C printed as gross monetary returns / cost of cultivation; converted to net / cost (rule 57).'},
            head + f' Printed B:C (gross / cost): CTR {bc1}, CT {bc0}; {SRC[tag]}.', **YD)
        add('COST OF CULTIVATION', {'COST_WCT': f'=ROUND({nr0}/({bc0}-1),1)', 'COST_WCTR': f'=ROUND({nr1}/({bc1}-1),1)',
                                    'UNIT': 'US$/ha (DERIVED: cost = net return / (gross-B:C - 1))', 'Crop/season of sampling': cs,
                                    'Data source': 'Figure 5 (DERIVED)', 'Method used (from paper)': 'Derived from net return and printed gross / cost B:C.'},
            head + ' Cost DERIVED = NR / (B:C - 1) from digitised / printed NR and B:C (small B:C reading errors inflate the cost - FLAG).', **YD)
        add('GROSS RETURN', {'GR_WCT': f'=ROUND({nr0}+{nr0}/({bc0}-1),1)', 'GR_WCTR': f'=ROUND({nr1}+{nr1}/({bc1}-1),1)',
                             'UNIT': 'US$/ha (DERIVED: gross = net return + cost)', 'Crop/season of sampling': cs,
                             'Data source': 'Figure 5 (DERIVED)', 'Method used (from paper)': 'Gross = grain x 267.4 + straw x 36.3 US$/t; here derived as NR + cost.'},
            head + ' Gross return DERIVED = NR + NR / (B:C - 1) (FLAG).', **YD)

    # ---- residue main effects (Fig. 3 / text): no R x I cell means for these traits
    mh = (f"MAIN EFFECT of residue (pooled over 3 irrigation levels x 2 foliar-K levels x 3 years; R x I and R x K interactions NS for this trait, "
          f"no cell means printed - rule 33, FLAG). CT = residue removed, CTR = residue retained. {TILL_FLAG} {RICE_NOT}")
    cs = 'Wheat 2015-16 to 2017-18, harvest / physiological maturity (3-yr mean, main effect)'
    m_comp = 'Recorded at harvest: AGBM sun-dried (t/ha); HI = GY / AGBM; TGW by seed counter (Contador); tillers per m2 at physiological maturity; grains per spike calculated (Gomez method ref. [39]).'
    add('DRY MATTER', {'DM_WCT': 11300, 'DM_WCTR': 11900, 'UNIT': 'kg/ha above-ground biomass (AGBM) at harvest (printed 11.3 / 11.9 t/ha)',
                       'Crop/season of sampling': cs, 'Data source': 'Text (Figure 3)', 'Method used (from paper)': m_comp},
        mh + ' AGBM printed in text (11.3 vs 11.9 t/ha; difference NS).', t=6, **YD)
    add('YIELD', {'W STRAW_CT': '=ROUND(11.3-4.858,2)', 'W STRAW_CTR': '=ROUND(11.9-5.224,2)',
                  'UNIT': 't/ha straw (DERIVED = AGBM - grain yield, main effects)', 'Crop/season of sampling': cs,
                  'Data source': 'Text + Figure 3 (DERIVED)', 'Method used (from paper)': 'Straw = above-ground biomass - grain yield (FORMULAS sheet).'},
        mh + ' STRAW-ONLY ROW: straw DERIVED = AGBM (11.3 / 11.9 t/ha, text) - main-effect grain yield (4.858 digitised / 5.224 text). Grain yield entered as R x I cells in rows a-c.', t=6, **YD)
    add('HARVEST INDEX', {'HI_WCT': 0.433, 'HI_WCTR': 0.440, 'UNIT': 'ratio (GY / AGBM)', 'Crop/season of sampling': cs,
                          'Data source': 'Figure 3 (digitised)', 'Method used (from paper)': m_comp},
        mh + ' HI digitised from Fig. 3 (NS).', t=6, **YD)
    add('PANICLE-SPIKE DENSITY', {'PSD_WCT': 454.8, 'PSD_WCTR': 469, 'UNIT': 'no./m2 (TILLERS per m2 at physiological maturity - FLAG)',
                                  'Crop/season of sampling': cs, 'Data source': 'Text + Figure 3 (digitised)', 'Method used (from paper)': m_comp},
        mh + ' Tillers per m2 (TPM): CTR 469 printed in text, CT digitised 454.8. GrPMS (grains per m2: 12670 CT digitised vs 13917 CTR text) - no sheet.', t=6, **YD)
    add('1000-GRAIN WEIGHT', {'TGW_WCT': 38.40, 'TGW_WCTR': 37.48, 'UNIT': 'g', 'Crop/season of sampling': cs,
                              'Data source': 'Figure 3 (digitised)', 'Method used (from paper)': m_comp},
        mh + ' TGW digitised from Fig. 3 (NS).', t=6, **YD)
    add('GRAINS PER PANICLE', {'GPP_WCT': 28.04, 'GPP_WCTR': 29.95, 'UNIT': 'grains per spike (wheat)', 'Crop/season of sampling': cs,
                               'Data source': 'Figure 3 (digitised)', 'Method used (from paper)': m_comp},
        mh + ' Grains per spike digitised from Fig. 3. SPAD at flowering (49.7 CT vs 52.2 CTR) and flag-leaf RWC (90.8 vs 93.8) - no sheet.', t=6, **YD)
    return out


TM = [
    ('Residue removal (control)', 'Rice residue removed; field prepared by ploughing (P and K incorporated with the last ploughing); wheat sown with Bhopal seed drill.',
     'Not described', 'Conventional (ploughing implied)', 'No', '0', 'CT', 'Conventional tillage without residue; rice phase not described (rule 23).', 'Medium', 'INCLUDED'),
    ('RRR (rice residue retention)', '4 t/ha rice residue (equivalent to anchored residue left by the combine) retained; same field preparation and seed drill.',
     'Not described', 'Conventional (ploughing implied) - FLAG', 'Yes', '4', 'CTR',
     'Residue retained under the same (ploughed) field preparation -> CTR. FLAG: tillage only implied; if no-till -> CA (and removal -> ZT).', 'Medium', 'INCLUDED'),
    ('ICS / ICS+IFS / IAS', 'Irrigation sub-plots: 1 (CRI), 2 (CRI + flowering) or 6 irrigations.', 'n/a', 'n/a', 'n/a', None,
     'Rows a / b / c', 'Non-tillage factor -> one row per level (rule 33; R x I cell means in Fig. 5).', 'High', 'INCLUDED'),
    ('Foliar K vs no spray', '2 % K2SO4 foliar spray at Zadoks 40 and 60 vs control (sub-sub plot).', 'n/a', 'n/a', 'n/a', None,
     'Pooled', 'R x K interaction NS and no R x K cell means printed -> pooled (T = 2 in Obs).', 'High', 'INCLUDED (pooled)'),
]

STUDY_INFO_EXTRA = dict(
    estab=2015, yeardata='2015-16 to 2017-18', years='3 (pooled)', texture='Sandy loam (sand 63.1, silt 26.7, clay 10.2 %)',
    rotation='Rice-wheat (rice tillage not described)', wheatvar='HD 2967', ricevar='Not reported', N='150', P='60 P2O5', K='30 K2O (+ foliar 2 % K2SO4 in K sub-sub plots)',
    residue='Rice residue 4 t/ha (anchored, combine-harvested) retained vs removed',
    irrigation='ICS (1), ICS + IFS (2) or IAS (6) irrigations of ~60 mm, measured with a Cutthroat Parshall flume; annual rainfall 744 mm',
    treatments='2 residue (main) x 3 irrigation (sub) x 2 foliar K (sub-sub), split-split plot, 3 reps, 8 x 2 m plots',
    params=('Wheat grain yield, WUE, net return, B:C (net/cost), derived cost and gross return - R x I cells rows a-c; main effects (flagged): AGBM (DRY MATTER), '
            'straw (derived), HI, tillers per m2, TGW, grains per spike'),
    supp='None (MDPI open access; no supplementary files)',
    notes=('NEW serial 320 (ext\\642.pdf). Tillage coded CT / CTR (ploughing implied) - FLAG, author to confirm. Rice phase not described (rule 23). Fig. 3 / Fig. 5 raster figures digitised with calibrated axes '
           '(checks: GY 5224, AGBM 11.9, TPM 469, WUE 2.45, NR 622 vs printed 624.4). Not entered (no sheet): RWC, SPAD, grains per m2, water available (Fig. 2), weather (Fig. 1). '
           'Foliar-K and I x K effects (Figs. 4, 6) - no tillage contrast. Initial soil 0-15 cm: EC 0.23 dS/m, OC 0.42 %, avail. N 198, P 18.2, K 232 kg/ha; BD 1.47 Mg/m3 (0-1 m); FC 21.87 %, PWP 10.94 % (site level, notes only); '
           'stored soil moisture at sowing 17.02 / 18.20 / 17.30 %.'),
)
