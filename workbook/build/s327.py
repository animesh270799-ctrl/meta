"""Study 327 - Puniya R. et al. 2023 Sci. Rep. 13:19311 (ext 652): zero-till wheat, rice residue x N x weed management, SKUAST-Jammu (Chatha)."""
from common import base, notes

ST = dict(
    no=327, serial=327,
    authors='Puniya R., Bazaya B.R., Kumar A., Sharma B.C., Nesar N.A., Bochalya R.S., Dwivedi M.C., Sharma N., Kumar R., Sharma J., Sharma A. & Mehta S.', year=2023, journal='Scientific Reports',
    ref=('Puniya R., Bazaya B.R., Kumar A., Sharma B.C., Nesar N.A., Bochalya R.S., Dwivedi M.C., Sharma N., Kumar R., Sharma J., Sharma A. & Mehta S. (2023) Effect of residue and weed management practices '
         'on weed flora, yield, energetics, carbon footprint, economics and soil quality of zero tillage wheat. Scientific Reports 13:19311, doi 10.1038/s41598-023-45488-3.'),
    doi='10.1038/s41598-023-45488-3',
    fert='Wheat HD 3086, 125 kg seed/ha; 100 kg N (100 % RDN) or 125 kg N (125 % RDN) + 50 P2O5 + 25 K2O kg/ha (1/3 N basal, 2 splits); 2 irrigations; herbicides at 30-35 DAS (weed factor pooled)',
    tmap=('Strip plot, 3 reps, AICRP-Weed Management farm SKUAST-Jammu (Chatha) rabi 2018-19 and 2019-20. ALL wheat zero-till drilled. Residue / N factor: 100 % RDN without residue (loose and standing residue removed) -> ZT ; '
          '100 % RDN + standing rice residue (combine-cut at 30-35 cm, loose residue removed) -> CA (row a) ; 125 % RDN + R -> CA (row b; EXTRA 25 % N - FLAG) ; 125 % RDN + R + waste decomposer -> CA (row c; extra N + WD - FLAG). '
          'Weed factor (sulfosulfuron + carfentrazone, clodinafop + metsulfuron, clodinafop + metribuzin, weedy control) POOLED (residue main effects; interaction NS - FLAG). '
          'Rice phase: direct-seeded rice, tillage not described - coded on the wheat phase (rule 23).'),
    details=('TREATMENTS IN PAPER: residue / N: 100 % RDN + R, 125 % RDN + R, 125 % RDN + R + WD, 100 % RDN (no residue) x weed management: sulfosulfuron + carfentrazone (25 + 20 g/ha), clodinafop-propargyl + metsulfuron '
             '(60 + 4 g/ha), clodinafop-propargyl + metribuzin (54 + 120 g/ha), control (strip plot, 3 reps). || MAPPING: 100 % RDN -> ZT: zero-till wheat, residue removed [rice phase: DSR, tillage not described; wheat: ZT; residue: No] | '
             '100 % RDN + R -> CA (row a) [wheat: ZT into 30-35 cm standing stubble; residue: Yes] | 125 % RDN + R -> CA (row b, +25 % N FLAG) | 125 % RDN + R + WD -> CA (row c, +25 % N + waste decomposer 500 l/ha FLAG)'),
)
SITE = dict(country='India (Jammu & Kashmir)', site='AICRP-Weed Management research farm, SKUAST-Jammu, Chatha', lat=32.667, lon=74.967, climate='ST', duration='0-3 Y', soil='LOAMY',
            **{'RAIN FALL': 1080, 'soc (initial)': 3.92, 'Bdi': 1.46})
# order: ZT (100 % RDN), CA a (100 % RDN + R), CA b (125 % RDN + R), CA c (125 % RDN + R + WD)
ROWS = (('a', 1, '100 % RDN + R'), ('b', 2, '125 % RDN + R (EXTRA 25 % N - FLAG)'), ('c', 3, '125 % RDN + R + WD (EXTRA 25 % N + waste decomposer - FLAG)'))
HEAD = ('ZT = 100 % RDN without residue; CA = {lab}. ZERO-TILL WHEAT into standing rice stubble (30-35 cm) vs residue removed. RESIDUE / N MAIN EFFECT pooled over 4 weed-management levels '
        '(3 herbicide mixtures + weedy control; interaction NS) - FLAG (rule 33). 2-yr mean (rabi 2018-19, 2019-20). Rice phase DSR, tillage not described (rule 23).')
YD = 'wheat 2018-19 and 2019-20 (2-yr mean)'
M_C = ('Growth on 60 DAS and at harvest; spikes / m2 before harvest; grains / spike from 10 spikes; 1000-grain weight; grain and straw from 5 x 3.4 m net plot (straw = biological - grain).')


def rows(B):
    st = ST; out = []

    def add(sheet, vals, body, tag, lab, unit, src, meth=M_C, crop='Wheat (rabi), 2-yr mean', soil=False):
        obs, nt = notes(st, f'ROW {tag}: ' + HEAD.format(lab=lab) + ' ' + body, y=2, t=4)
        v = base(st, SITE, {'year of data collection/experiment': '2018-2020', 'YEAR OF DATA (duration)': YD})
        if soil:
            v.update({'DEPTH': '0-15 CM', 'DEPTH (as reported in paper)': 'not stated (FLAG)'})
        v.update(vals)
        v.update({'UNIT': unit, 'Crop/season of sampling': crop, 'Data source': src, 'Method used (from paper)': meth, 'Obs': obs, 'Rep': 3, 'Notes/Doubts': nt})
        out.append((sheet, B.add_row(sheet, v)))

    def pair(pre, vals, fmt=None):
        # vals in paper order: [100 % RDN + R, 125 % RDN + R, 125 % RDN + R + WD, 100 % RDN]
        return lambda i: {f'{pre}ZT': (fmt.format(vals[3]) if fmt else vals[3]), f'{pre}CA': (fmt.format(vals[i - 1]) if fmt else vals[i - 1])}

    P = {
        'PLH60': ([41.15, 42.32, 42.37, 35.71], 'PLANT HEIGHT', 'PLH_W', None, 'cm (60 DAS)', 'Table 4 plant height at 60 DAS.', 'Wheat, 60 DAS (2-yr mean)'),
        'PLHH': ([117.24, 125.13, 126.26, 113.15], 'PLANT HEIGHT', 'PLH_W', None, 'cm (at harvest)', 'Table 4 plant height at harvest. Tillers / m2 (no sheet): 60 DAS 425.54 / 468.83 / 473.04 / 416.04, harvest 418.33 / 462.21 / 465.00 / 412.25 (RDN + R / 125 + R / 125 + R + WD / RDN).', 'Wheat at harvest (2-yr mean)'),
        'DM60': ([218.86, 245.46, 248.00, 203.55], 'DRY MATTER', 'DM_W', '=ROUND({}*10,1)', 'kg/ha (printed g/m2 x 10; 60 DAS)', 'Table 4 dry matter at 60 DAS (g/m2 x 10).', 'Wheat, 60 DAS (2-yr mean)'),
        'DMH': ([854.47, 902.37, 905.83, 823.17], 'DRY MATTER', 'DM_W', '=ROUND({}*10,1)', 'kg/ha (printed g/m2 x 10; at harvest)', 'Table 4 dry matter at harvest (g/m2 x 10).', 'Wheat at harvest (2-yr mean)'),
        'PSD': ([411.58, 452.17, 457.50, 399.33], 'PANICLE-SPIKE DENSITY', 'PSD_W', None, 'no. spikes/m2', 'Table 5 spikes per m2.', None),
        'GPP': ([34.25, 36.96, 36.92, 33.04], 'GRAINS PER PANICLE', 'GPP_W', None, 'grains per spike', 'Table 5 grains per spike.', None),
        'TGW': ([36.71, 38.58, 38.68, 36.46], '1000-GRAIN WEIGHT', 'TGW_W', None, 'g', 'Table 5 1000-grain weight.', None),
        'HI': ([43.66, 44.57, 44.88, 43.69], 'HARVEST INDEX', 'HI_W', '=ROUND({}/100,4)', 'ratio (printed % / 100)', 'Table 5 harvest index (printed %).', None),
    }
    for key, (vals, sheet, pre, fmt, unit, txt, crop) in P.items():
        for tag, i, lab in ROWS:
            add(sheet, pair(pre, vals, fmt)(i), txt, tag, lab, unit, 'Table 4' if key[:2] in ('PL', 'DM') else 'Table 5', crop=crop or 'Wheat (rabi), 2-yr mean')
    GY = [3804.21, 4238.13, 4267.42, 3518.46]; SY = [5433.10, 5970.06, 6010.32, 5228.63]
    for tag, i, lab in ROWS:
        add('YIELD', {'WYIELD_ZT': f'=ROUND({GY[3]}/1000,3)', 'WYIELD_CA': f'=ROUND({GY[i - 1]}/1000,3)', 'W STRAW_ZT': f'=ROUND({SY[3]}/1000,3)', 'W STRAW_CA': f'=ROUND({SY[i - 1]}/1000,3)'},
            'Table 5 wheat grain and straw yield (kg/ha / 1000). Weed main effects (pooled over residue): grain 4347.88 / 4269.08 / 4137.33 / control 3073.92 kg/ha.', tag, lab, 't/ha (printed kg/ha / 1000)', 'Table 5')
    # ---- carbon budget (Table 8; inventory carbon equivalents, Lal 2004 / West & Marland 2002)
    CI = [1382.24, 1416.58, 1418.50, 502.24]; CO = [4064.42, 4491.60, 4522.20, 3848.72]; CE = [2.94, 3.17, 3.19, 7.66]; CF = [0.37, 0.34, 0.34, 0.15]
    mcb = 'Carbon input = inputs (diesel, fertiliser, pesticide, water, RICE RESIDUE, seed, labour, machinery) x emission coefficients (Lal 2004; West & Marland 2002); C output = (grain + straw) x 0.44; CE = output / input; CF = input / grain yield.'
    for tag, i, lab in ROWS:
        nb = ' Residue C counted as an INPUT in CA (rice residue = 56 % of total C input) - FLAG.'
        add('C input', {'CIN_ZT': CI[3], 'CIN_CA': CI[i - 1]}, 'Table 8 total carbon input (inventory estimate - FLAG).' + nb, tag, lab, 'kg CE/ha per wheat season (inventory carbon equivalent, as printed)', 'Table 8', mcb)
        add('C output', {'COUT_ZT': CO[3], 'COUT_CA': CO[i - 1]}, 'Table 8 total carbon output (biomass x 0.44).', tag, lab, 'kg C/ha per wheat season (biomass x 0.44, as printed)', 'Table 8', mcb)
        add('CER', {'CER_ZT': CE[3], 'CER_CA': CE[i - 1]}, 'Table 8 carbon efficiency (output / input).' + nb, tag, lab, 'ratio (C output / C input, as printed)', 'Table 8', mcb)
        add('CSI', {'CSI_ZT': f'=ROUND(({CO[3]}-{CI[3]})/{CI[3]},2)', 'CSI_CA': f'=ROUND(({CO[i - 1]}-{CI[i - 1]})/{CI[i - 1]},2)'},
            'CSI DERIVED = (C output - C input) / C input from Table 8.' + nb, tag, lab, 'index ((C output - C input) / C input; DERIVED)', 'Table 8 (DERIVED)', mcb)
        add('GHG intensity', {'GHGI_ZT': f'=ROUND({CF[3]}*44/12,3)', 'GHGI_CA': f'=ROUND({CF[i - 1]}*44/12,3)'},
            f'Table 8 carbon footprint printed in kg CE/kg wheat ({CF[3]} vs {CF[i - 1]}) converted x 44/12 to kg CO2-eq/kg (DERIVED - FLAG; input-based estimate).' + nb, tag, lab,
            'kg CO2-eq/kg grain (printed kg CE/kg x 44/12; input-based estimate - FLAG)', 'Table 8 (DERIVED)', mcb)
    # ---- economics (Table 9, Rs/ha; B:C printed = net / cost)
    GR = [76571.5, 85300.5, 85889.0, 70825.5]; CC = [25379.5, 25679.5, 25729.5, 25379.5]; NR = [51192.0, 59621.0, 60160.0, 45446.0]; BC = [2.02, 2.32, 2.34, 1.79]
    me = 'Cost of cultivation at prevailing input prices; gross return = grain + straw value; net return = gross - cost; B:C = net / cost (check 51192 / 25379.5 = 2.02).'
    for tag, i, lab in ROWS:
        add('GROSS RETURN', {'GR_WZT': GR[3], 'GR_WCA': GR[i - 1]}, 'Table 9 gross return (2-yr average).', tag, lab, 'Rs/ha', 'Table 9', me)
        add('COST OF CULTIVATION', {'COST_WZT': CC[3], 'COST_WCA': CC[i - 1]}, 'Table 9 cost of cultivation.', tag, lab, 'Rs/ha', 'Table 9', me)
        add('NET RETURN', {'NR_WZT': NR[3], 'NR_WCA': NR[i - 1]}, 'Table 9 net return.', tag, lab, 'Rs/ha', 'Table 9', me)
        add('BC ratio', {'BC_WZT': BC[3], 'BC_WCA': BC[i - 1]}, 'Table 9 B:C as printed (= net / cost, rule 57 check).', tag, lab, 'ratio (net / cost, as printed)', 'Table 9', me)
    # ---- soil (Table 10; depth not stated; after wheat, 2-yr mean)
    SOIL = {'SOC(active C pool)': ('SOC_', [4.05, 4.06, 4.10, 3.94], 'g/kg (organic carbon; method not stated)', 'Table 10 organic carbon. Initial 3.92 g/kg.'),
            'N': ('N_', [233.23, 237.70, 239.37, 232.16], 'kg/ha (available N)', 'Table 10 available N. Initial 228.93.'),
            'P': ('P_', [14.38, 14.82, 14.98, 13.86], 'kg/ha (available P)', 'Table 10 available P. Initial 13.84.'),
            'K': ('K_', [144.45, 145.68, 146.36, 141.83], 'kg/ha (available K)', 'Table 10 available K. Initial 142.34.'),
            'BD': ('BD_', [1.45, 1.45, 1.44, 1.46], 'Mg/m3', 'Table 10 bulk density (g/cc). Initial 1.46.')}
    for sheet, (pre, vals, unit, txt) in SOIL.items():
        for tag, i, lab in ROWS:
            add(sheet, {f'{pre}ZT': vals[3], f'{pre}CA': vals[i - 1]}, txt + ' Sampling depth NOT STATED (entered as 0-15 CM - FLAG); differences NS.', tag, lab, unit, 'Table 10',
                'Not stated in paper', crop='Soil after wheat (2-yr mean)', soil=True)
    return out


TM = [
    ('100 % RDN (no residue)', 'Zero-till wheat after removal of loose and standing rice residue; 100 kg N/ha', 'DSR (tillage not described)', 'Zero tillage', 'No', '0', 'ZT', 'Wheat-phase coding (rule 23).', 'High', 'INCLUDED'),
    ('100 % RDN + R', 'Zero-till wheat into 30-35 cm standing rice stubble (loose residue removed); 100 kg N/ha', 'DSR (tillage not described)', 'Zero tillage', 'Yes (standing stubble)', None, 'CA (row a)',
     'ZT + retained standing residue.', 'High', 'INCLUDED'),
    ('125 % RDN + R', 'As above with 125 kg N/ha', 'DSR', 'Zero tillage', 'Yes', None, 'CA (row b) - FLAG', 'Extra 25 % N confounded with residue (flag; drop for N-matched sensitivity).', 'Medium', 'INCLUDED'),
    ('125 % RDN + R + WD', 'As above + waste decomposer 500 l/ha sprayed on residue after sowing', 'DSR', 'Zero tillage', 'Yes + decomposer', None, 'CA (row c) - FLAG', 'Extra N + microbial decomposer (flag).', 'Medium', 'INCLUDED'),
    ('Weed management (4 levels)', 'Sulfosulfuron + carfentrazone; clodinafop + metsulfuron; clodinafop + metribuzin; weedy control', 'n/a', 'n/a', 'n/a', None, 'Pooled', 'Residue main effects pooled over weed levels (T = 4, FLAG).', 'High', 'INCLUDED (pooled)'),
]
STUDY_INFO = dict(estab=2018, yeardata='Rabi 2018-19 and 2019-20', years='2 (pooled means)', texture='Sandy clay loam', rotation='Rice (DSR)-wheat', wheatvar='HD 3086', ricevar='Not reported',
                  N='100 or 125 (wheat)', P='50 (P2O5)', K='25 (K2O)', residue='Standing rice stubble 30-35 cm (combine-cut; loose residue removed) vs all residue removed',
                  irrigation='2 irrigations per season', treatments='4 residue / N x 4 weed management (strip plot, 3 reps)',
                  supp='Supplementary material (raw data file) referenced - not downloaded (permission needed)',
                  params=('Wheat (ZT vs CA rows a-c, residue main effects pooled over weed management): plant height and dry matter (60 DAS, harvest), spikes / m2, grains / spike, TGW, HI, grain and straw yield; '
                          'C input, C output, CER, CSI (derived), carbon footprint (GHG intensity, derived); gross / cost / net return, B:C; soil OC, available N / P / K, BD (depth not stated)'),
                  notes=('NEW serial 327 (ext\\652.pdf). All plots zero-till wheat: the contrast is residue retention (CA) vs removal (ZT); 125 % RDN rows b / c carry 25 % extra N (FLAG). '
                         'NOT ON A SHEET: weed density by species at 30 DAS and harvest, weed biomass and WCE (Tables 1-3); tillers / m2 (Table 4); energy budget (Tables 6-7: energy input RDN + R 42084, 125 + R 43615, '
                         '125 + R + WD 43688, RDN 15277 MJ/ha; output 123836 / 136926 / 137860 / 117079; EUE 2.94 / 3.14 / 3.16 / 7.66; energy productivity 0.09 / 0.10 / 0.10 / 0.23 kg/MJ). '
                         'Weed-management main effects pooled over residue (not a tillage contrast) in row notes only. Soil sampling depth not stated (0-15 CM assumed - FLAG). '
                         'Abstract misprints the carbon footprint of 100 % RDN as 7.66 (Table 8: 0.15).'))
SITES = [('AICRP-Weed Management farm, SKUAST-Jammu, Chatha', "32 40' N", "74 58' E", 32.667, 74.967, 'Paper', 'ST', None)]
