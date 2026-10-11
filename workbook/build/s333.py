"""Study 333 - Singh A., Phogat V.K., Dahiya R. & Batra S.D. 2014 Soil Tillage Res. 140:98-105 (ext 673): 15-yr ZT wheat vs CT on 3 farm sites, Haryana."""
from common import base, notes
from d673 import SOC, BD, WDC, KS, FC, AP, EST

ST = dict(
    no=333, serial=333, authors='Singh A., Phogat V.K., Dahiya R. & Batra S.D.', year=2014, journal='Soil & Tillage Research',
    ref=('Singh A., Phogat V.K., Dahiya R. & Batra S.D. (2014) Impact of long-term zero till wheat on soil physical properties and wheat productivity under rice-wheat cropping system. '
         'Soil & Tillage Research 140:98-105, doi 10.1016/j.still.2014.03.002.'),
    doi='10.1016/j.still.2014.03.002',
    fert='Farmer-managed; wheat PBW 550 (2011-12); rice puddled every kharif in both fields',
    tmap=('Paired long-term (since 1996-97, 15 yr) farmer fields (0.4 ha) at 3 sites: ZT wheat drilled into combine-harvested rice residue left on the surface after PUDDLED rice -> pCA (rule 122: stubble mulch = '
          'residue retention; puddled rice, rule 124) ; adjoining CT wheat (rice residue manually removed, 2 discings to 0.1 m + planking) -> CT. Unreplicated fields; 5 random 1 m2 plots per field (Rep = 5) - FLAG.'),
    details=('TREATMENTS IN PAPER: conventional tillage (CT, 2 harrowings / discings + cultivator + planking, residue removed) vs zero tillage (ZT, direct drilling into rice residue) of wheat, '
             'puddled rice in both, at Pirthala (sandy loam), Uchana (loam) and Teek (clay loam). || MAPPING: CT -> CT [rice: puddled; wheat: conventional; residue: removed] | '
             'ZT -> pCA [rice: puddled; wheat: zero-till; residue: combine-harvested rice residue on the surface]'),
)
SITES_D = {'SL': dict(country='India (Haryana)', site='Farmer field, Pirthala village, Fatehabad (sandy loam)', lat=29.50, lon=75.43, climate='ST', duration='>10 Y', soil='LOAMY',
                      CLAY=16.6, sand=70.6, silt=12.8, **{'ph (initial)': 7.8, 'soc (initial)': 4.5}),
           'L': dict(country='India (Haryana)', site='Farmer field, Uchana (loam)', lat=29.47, lon=76.18, climate='ST', duration='>10 Y', soil='LOAMY',
                     CLAY=18.6, sand=61.3, silt=20.1, **{'ph (initial)': 8.0, 'soc (initial)': 5.8}),
           'CL': dict(country='India (Haryana)', site='Farmer field, Teek village, Kaithal (clay loam)', lat=29.87, lon=76.48, climate='ST', duration='>10 Y', soil='LOAMY',
                      CLAY=31.4, sand=46.7, silt=21.9, **{'ph (initial)': 8.1, 'soc (initial)': 6.6})}
SITE = dict(SITES_D['L'], site='Farmer fields at Pirthala (Fatehabad), Uchana and Teek (Kaithal), Haryana')
NAME = {'SL': 'Pirthala sandy loam', 'L': 'Uchana loam', 'CL': 'Teek clay loam'}
LAYERS = [('0-5', '0-15 CM', 3), ('5-10', '0-15 CM', 3), ('10-15', '0-15 CM', 3), ('15-20', '15-30 CM', 3), ('20-25', '15-30 CM', 3), ('25-30', '15-30 CM', 3), ('30-35', '30-45 CM', 2), ('35-40', '30-45 CM', 2)]
DIG = ('DIGITISED depth profile (raster figure, calibrated axis frame and ticks; open / filled circle markers detected automatically - SOC x BD reproduces the printed 0-40 cm C stocks within 1.3 %). ')
MS = 'Bulk and core samples at 0.05 m intervals to 0.4 m at wheat harvest 2011-12 (5 random plots per field).'


def rows(B):
    st = ST; out = []

    def add(sheet, vals, body, s, unit, src, meth=MS, depth=None, d=1, crop='Soil at wheat harvest 2011-12', rep=5):
        obs, nt = notes(st, f'{NAME[s]}: CT = conventional wheat, pCA = 15-yr zero-till wheat into rice residue (puddled rice in both). ' + body, d=d)
        v = base(st, SITES_D[s], {'year of data collection/experiment': '2011-12', 'YEAR OF DATA (duration)': '15 yr (sampled 2011-12)'})
        if depth:
            v.update({'DEPTH': depth[1], 'DEPTH (as reported in paper)': depth[0]})
        v.update(vals)
        v.update({'UNIT': unit, 'Crop/season of sampling': crop, 'Data source': src, 'Method used (from paper)': meth, 'Obs': obs, 'Rep': rep, 'Notes/Doubts': nt})
        out.append((sheet, B.add_row(sheet, v)))

    def est(key, s, i):
        return ' Point read by eye where the CT and ZT markers overlap / panel text was mis-detected - FLAG.' if (s, 0, i) in [tuple(e) for e in EST.get(key, [])] else ''

    P = (('SOC(active C pool)', 'SOC_', SOC, 'SOC', 'g/kg (Walkley-Black)', 'Figure 1', 'Walkley-Black.', None),
         ('BD', 'BD_', BD, 'BD', 'Mg/m3', 'Figure 2', 'Core method (Blake & Hartge 1986).', None),
         ('HC', 'HC_', KS, 'KS', 'cm/hr (printed cm/day / 24)', 'Figure 4', 'Saturated hydraulic conductivity of cores (cm/day as printed).', '=ROUND({}/24,3)'),
         ('FC (weight basis)', 'FC_', FC, 'FC', '% w/w (field water capacity at -33 kPa, pressure plate)', 'Figure 5', 'Pressure plate at 33 kPa (Richards 1954).', None),
         ('macro pore', 'MACROPORE_', AP, 'AP', '% v/v (AERATION porosity = air-filled pores at 0.5 m suction (-5 kPa) - taken as macroporosity, FLAG)', 'Figure 6',
          'Saturated cores equilibrated on a hanging water column at 0.5 m suction; volume of water released / soil volume.', None))
    for s in ('SL', 'L', 'CL'):
        for sheet, pre, data, key, unit, fig, meth, fmt in P:
            for i, (ly, cls, d) in enumerate(LAYERS):
                ct, zt = data[s][0][i], data[s][1][i]
                f = (lambda x: fmt.format(x)) if fmt else (lambda x: x)
                wdc = f' Water-dispersible silt + clay (Fig. 3, no sheet): CT {WDC[s][0][i]}, ZT {WDC[s][1][i]} %.' if key == 'SOC' else ''
                add(sheet, {f'{pre}CT': f(ct), f'{pre}pCA': f(zt)}, f'{fig} {key} {ly} cm. ' + DIG + est(key, s, i) + wdc, s, unit, f'{fig} (digitised)', meth, (f'{ly} cm', cls), d)
    STK = {'SL': (18.75, 22.32, 0.24), 'L': (19.84, 26.73, 0.46), 'CL': (23.83, 33.07, 0.62)}
    IR = {'SL': (3.374, 3.951), 'L': (3.037, 3.597), 'CL': (2.323, 2.965)}
    RB = {'SL': (983, 1663), 'L': (876, 1575), 'CL': (848, 1200)}
    ROOT = {'SL': ('54.8 / 26.2 / 14.9 / 1.1 / 0.9 / 0.7 / 0.5 / 0.6', '40.4 / 27.6 / 18.5 / 6.7 / 4.3 / 1.3 / 0.7 / 0.5'),
            'L': ('60.0 / 24.9 / 12.2 / 1.0 / 0.7 / 0.6 / 0.3 / 0.3', '40.9 / 28.4 / 17.3 / 6.9 / 4.2 / 1.1 / 0.6 / 0.5'),
            'CL': ('54.4 / 28.2 / 15.2 / 1.0 / 0.5 / 0.4 / 0.1 / 0.2', '41.1 / 27.8 / 20.2 / 5.3 / 3.8 / 1.0 / 0.5 / 0.3')}
    W = {'SL': ((83.1, 83.7), (71.6, 70.9), (62.2, 62.1), (35.6, 36.3), (5.98, 6.04)), 'L': ((83.4, 83.6), (73.0, 72.2), (62.2, 61.5), (35.5, 36.6), (6.08, 6.13)),
         'CL': ((82.7, 83.0), (70.6, 71.0), (64.3, 61.1), (35.6, 37.2), (6.10, 6.21))}
    for s in ('SL', 'L', 'CL'):
        a, b, r = STK[s]
        add('stock-SOC', {'SOCs_CT': a, 'SOCs_pCA': b}, f'Table 2 SOC stock 0-0.4 m (printed). C sequestration rate ZT over CT {r} Mg C/ha/yr (difference rate, not a per-treatment rate - c sequestration sheet not used).',
            s, 'Mg C/ha (0-40 cm, as printed)', 'Table 2', 'Stock = SOC x BD x layer depth summed over 0.05 m layers.', ('0-40 cm', '0-40 CM'))
        add('IR', {'IR_CT': f'=ROUND({IR[s][0]}/24,4)', 'IR_pCA': f'=ROUND({IR[s][1]}/24,4)'},
            f'Figure 7 water intake (infiltration) rate, DIGITISED (cm/day {IR[s][0]} / {IR[s][1]}, / 24); clay loam +28 % in text reproduced.', s, 'cm/hr (printed cm/day / 24)', 'Figure 7 (digitised)',
            'Infiltrometers (Bouwer 1986).', ('surface (infiltrometer)', '0-15 CM'))
        add('RMD(mg-cm3)', {'RMD_WCT': f'=ROUND({RB[s][0]}/100,2)', 'RMD_WpCA': f'=ROUND({RB[s][1]}/100,2)'},
            f'Figure 8 wheat root biomass density 0-0.4 m (mg/100 cm3 / 100): CT DIGITISED {RB[s][0]}, ZT printed {RB[s][1]} (digitised ZT within 0.7 % of the printed values). '
            f'Whether a profile mean or the sum of the eight 5-cm layers is not stated - FLAG. Root distribution by layer (% of total, Table 3): CT {ROOT[s][0]}; ZT {ROOT[s][1]}.', s,
            'mg/cm3 (printed mg/100 cm3 / 100; 0-40 cm)', 'Figure 8 (digitised) + text', 'Roots washed from 0.05 m core samples, oven-dried and weighed.', ('0-40 cm', '0-40 CM (profile)'), crop='Wheat roots at harvest 2011-12')
        ph, ti, gs, tw, gy = W[s]
        mw = 'Effective tillers per m row at 10 places; 20 plants for grains / spike and 1000-grain weight; yield = tillers x grains x test weight per m row (22.5 cm rows) x 0.85.'
        add('PLANT HEIGHT', {'PLH_WCT': ph[0], 'PLH_WpCA': ph[1]}, 'Table 4 plant height (NS).', s, 'cm', 'Table 4', mw, crop='Wheat 2011-12')
        add('PANICLE-SPIKE DENSITY', {'PSD_WCT': f'=ROUND({ti[0]}/0.225,1)', 'PSD_WpCA': f'=ROUND({ti[1]}/0.225,1)'}, f'Table 4 effective tillers per m ROW ({ti[0]} / {ti[1]}) / 0.225 m row spacing (DERIVED).', s,
            'no./m2 (DERIVED from per m row)', 'Table 4 (DERIVED)', mw, crop='Wheat 2011-12')
        add('GRAINS PER PANICLE', {'GPP_WCT': gs[0], 'GPP_WpCA': gs[1]}, 'Table 4 grains per spike.', s, 'grains per spike', 'Table 4', mw, crop='Wheat 2011-12')
        add('1000-GRAIN WEIGHT', {'TGW_WCT': tw[0], 'TGW_WpCA': tw[1]}, 'Table 4 mass of 1000 grains.', s, 'g', 'Table 4', mw, crop='Wheat 2011-12')
        add('YIELD', {'WYIELD_CT': gy[0], 'WYIELD_pCA': gy[1]}, 'Table 4 wheat grain yield ESTIMATED from yield components (85 % of the computed value) - FLAG.', s, 't/ha (estimated from components)', 'Table 4', mw,
            crop='Wheat 2011-12')
    return out


TM = [
    ('CT', 'Rice residue manually removed; 2 discings to 0.1 m + planking (abstract: 2 harrowings, 1 cultivator, planking); puddled rice', 'Puddled TPR', 'Conventional', 'No', '0', 'CT', 'Conventional both phases.', 'High', 'INCLUDED'),
    ('ZT', 'Wheat drilled with a zero-till machine into combine-harvested rice residue left on the surface, for 15 years; puddled rice', 'Puddled TPR', 'Zero tillage', 'Yes (combine residue)', None, 'pCA',
     'Rules 122 / 124: residue left on the surface + puddled rice.', 'Medium', 'INCLUDED'),
]
STUDY_INFO = dict(estab=1996, yeardata='Soil and wheat 2011-12 (15th year)', years='1 sampling', texture='Sandy loam / loam / clay loam (3 sites), Typic Haplustepts',
                  rotation='Rice-wheat', wheatvar='PBW 550', ricevar='Not reported', N='Farmer practice', P='Farmer practice', K='Farmer practice', residue='ZT: combine-harvested rice residue on the surface; CT: removed',
                  irrigation='Farmer practice', treatments='CT vs ZT wheat in paired farmer fields at 3 sites (5 sampling plots each)', supp='None',
                  params=('Per site, CT vs pCA: SOC, BD, saturated hydraulic conductivity, field capacity, aeration porosity (macro pore sheet) for eight 5-cm layers 0-40 cm (Figs 1-6 digitised); '
                          'SOC stock 0-40 cm; infiltration rate; root biomass density; wheat height, spikes, grains / spike, TGW, yield (estimated)'),
                  notes=('NEW serial 333 (ext\\673.pdf). Paired farmer fields (not randomised) - FLAG. Site coordinates not given (state range only) - villages geocoded approximately (FLAG); paper places Uchana in Karnal. '
                         'NOT ON A SHEET: water-dispersible silt + clay (Fig. 3; in SOC row notes), C sequestration rate ZT over CT (0.24 / 0.46 / 0.62 Mg C/ha/yr; difference only), root distribution by depth (Table 3, in RMD notes).'))
SITES = [(f'{NAME[s]} farm', 'not reported', 'not reported', SITES_D[s]['lat'], SITES_D[s]['lon'], 'Geocoded (village) - FLAG', 'ST', 'Site range in paper 27 39-30 55 N, 74 27-77 36 E') for s in ('SL', 'L', 'CL')]
