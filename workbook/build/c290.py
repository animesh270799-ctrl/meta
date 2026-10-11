"""290 (companion) - Sharma S., Singh P. & Kumar S. 2020 Front. Sustain. Food Syst. 4:532704 (ext 669): PAU N x rice-straw incorporation trial of study 290."""
from common import base, notes

ST = dict(
    no=290, serial='290 (companion)', authors='Sharma S., Singh P. & Kumar S.', year=2020, journal='Frontiers in Sustainable Food Systems',
    ref=('Sharma S., Singh P. & Kumar S. (2020) Responses of soil carbon pools, enzymatic activity, and crop yields to nitrogen and straw incorporation in a rice-wheat cropping system '
         'in north-western India. Frontiers in Sustainable Food Systems 4:532704, doi 10.3389/fsufs.2020.532704.'),
    doi='10.3389/fsufs.2020.532704',
    fert='Fertiliser N 0 / 90 / 120 / 150 kg N/ha to rice and wheat (urea, 3 splits); rice 10 kg Zn/ha; wheat 60 P2O5 + 30 K2O kg/ha; rice PR 118 puddled transplanted; wheat zero-till drilled after straw rotavation',
    tmap=('SAME PAU trial as study 290 (est. 2010, RBD 4 reps; 4 N rates x 4 rice-straw rates). Coded as 290: rice straw chopped and incorporated with a ROTAVATOR (~3 weeks before wheat) -> CTR ; '
          'RS0 (straw removed) -> CT (rotavation of RS0 plots assumed - FLAG, as 290). Per N rate (N0 / N90 / N120 / N150 = separate rows): CT = RS0, CTR = RS5.0 (row a) / RS7.5 (row b) / RS10.0 (row c). '
          'Puddled transplanted rice in all plots; wheat zero-till drilled into the rotavated plots.'),
    details=('TREATMENTS IN PAPER: fertiliser N 0 / 90 / 120 / 150 kg N/ha x rice straw incorporation 0 / 5.0 / 7.5 / 10.0 Mg/ha (16 treatments, RBD, 4 reps). || MAPPING: RS0 -> CT [rice: puddled TPR; wheat: '
             'zero-till drill after (assumed) rotavation; residue: removed] | RS5.0 / RS7.5 / RS10.0 -> CTR rows a / b / c [rice: puddled TPR; wheat: straw rotavated in, zero-till drill; residue: 5 / 7.5 / 10 Mg/ha] | '
             'N rates -> separate rows'),
)
SITE = dict(country='India (Punjab)', site='Research farm, Punjab Agricultural University, Ludhiana (trial of study 290)', lat=30.933, lon=75.867, climate='ST', duration='4-10 Y', soil='LOAMY',
            CLAY=12.8, sand=71.5, silt=15.5, **{'RAIN FALL': 700, 'ph (initial)': 6.6, 'soc (initial)': 3.91})
NL = ('N0', 'N90', 'N120', 'N150')
RS = ('RS5.0', 'RS7.5', 'RS10.0')
SAMP = 'Soil after wheat, last week of April 2016 (6th rice-wheat cycle)'
M_SOIL = 'Core samples (7.2 cm) at 0-7.5 and 7.5-15 cm, April 2016; enzymes / MBC on field-moist soil, C pools on air-dried soil (Appendix I).'
# 16 treatments in table order: N0 (RS0, RS5, RS7.5, RS10), N90 (...), N120 (...), N150 (...)
T1 = dict(GR=[4.87, 5.52, 5.63, 5.58, 5.55, 5.92, 6.04, 5.86, 5.69, 6.20, 6.41, 6.07, 5.58, 6.09, 6.28, 6.08],
          GW=[2.01, 1.98, 2.18, 1.93, 4.80, 4.58, 4.89, 4.72, 5.52, 5.76, 5.75, 5.45, 5.36, 5.43, 5.54, 5.39],
          SR=[6.12, 7.17, 7.63, 7.09, 7.03, 8.29, 8.64, 8.51, 7.72, 8.64, 8.86, 8.46, 7.47, 8.38, 8.76, 8.52],
          SW=[2.83, 2.84, 3.15, 3.07, 6.58, 6.94, 7.38, 7.28, 7.22, 7.82, 8.26, 8.07, 7.16, 7.92, 8.08, 8.00],
          HR=[0.443, 0.435, 0.425, 0.441, 0.441, 0.416, 0.411, 0.408, 0.424, 0.418, 0.420, 0.418, 0.428, 0.421, 0.418, 0.417],
          HW=[0.415, 0.411, 0.409, 0.386, 0.422, 0.397, 0.399, 0.393, 0.433, 0.424, 0.410, 0.403, 0.428, 0.407, 0.407, 0.402])
CIN = [(0.00, 0.87, 0.71, 1.76, 3.34), (2.00, 0.97, 0.75, 1.94, 5.67), (3.00, 1.03, 0.79, 2.06, 6.88), (4.00, 0.98, 0.80, 1.96, 7.74),
       (0.00, 1.22, 1.04, 2.66, 4.92), (2.00, 1.33, 1.12, 2.86, 7.30), (3.00, 1.39, 1.18, 2.99, 8.56), (4.00, 1.36, 1.15, 2.93, 9.44),
       (0.00, 1.33, 1.14, 2.90, 5.36), (2.00, 1.45, 1.22, 3.15, 7.83), (3.00, 1.49, 1.28, 3.25, 9.02), (4.00, 1.43, 1.21, 3.11, 9.75),
       (0.00, 1.30, 1.09, 2.84, 5.23), (2.00, 1.42, 1.23, 3.09, 7.73), (3.00, 1.46, 1.27, 3.18, 8.91), (4.00, 1.43, 1.24, 3.11, 9.78)]
# per depth: surface 0-7.5 / sub-surface 7.5-15
S = {
 'TOC': ([4.37, 4.69, 4.88, 5.66, 4.56, 4.65, 5.06, 5.94, 4.69, 5.61, 5.94, 6.44, 4.97, 6.26, 6.58, 6.37],
         [3.50, 3.59, 4.05, 4.56, 3.68, 3.96, 4.05, 4.79, 4.37, 4.42, 4.51, 5.20, 4.60, 5.38, 5.75, 5.98]),
 'WEOC': ([24.8, 27.0, 27.5, 32.0, 25.9, 25.5, 28.1, 33.7, 26.7, 31.8, 33.6, 36.2, 28.5, 35.4, 36.5, 39.7],
          [19.7, 20.4, 22.5, 24.3, 21.7, 22.3, 23.9, 26.1, 24.9, 25.2, 25.7, 28.2, 26.1, 30.7, 32.7, 34.3]),
 'HWC': ([223.5, 231.9, 242.7, 294.6, 225.3, 232.1, 257.3, 293.5, 230.7, 278.2, 292.7, 318.9, 249.2, 293.0, 333.3, 373.6],
         [177.6, 177.4, 202.7, 227.8, 185.2, 201.5, 214.1, 241.0, 216.5, 222.2, 222.4, 253.0, 232.3, 245.1, 290.9, 297.3]),
 'MBC': ([243.9, 253.5, 267.6, 319.2, 246.9, 254.3, 282.0, 288.1, 247.7, 304.2, 310.2, 347.3, 275.3, 321.2, 373.6, 408.1],
         [193.6, 194.9, 222.2, 249.6, 202.2, 220.1, 234.6, 263.0, 237.3, 243.6, 243.4, 277.3, 254.3, 265.9, 314.7, 325.1]),
 'BSR': ([0.178, 0.189, 0.196, 0.205, 0.187, 0.196, 0.208, 0.204, 0.190, 0.196, 0.206, 0.214, 0.169, 0.187, 0.196, 0.200],
         [0.135, 0.143, 0.151, 0.156, 0.139, 0.149, 0.158, 0.161, 0.135, 0.151, 0.165, 0.160, 0.130, 0.149, 0.155, 0.160]),
 'QCO2': ([4.34, 4.80, 5.27, 6.55, 4.61, 4.99, 5.84, 5.88, 4.71, 5.97, 6.37, 7.43, 4.67, 6.03, 7.32, 8.18],
          [2.62, 2.79, 3.35, 3.89, 2.81, 3.29, 3.70, 4.25, 3.21, 3.68, 4.02, 4.46, 3.29, 3.97, 4.87, 5.22]),
 'QMIC': ([0.559, 0.542, 0.550, 0.566, 0.547, 0.552, 0.560, 0.491, 0.531, 0.543, 0.524, 0.539, 0.558, 0.514, 0.568, 0.559],
          [0.554, 0.545, 0.551, 0.551, 0.552, 0.567, 0.582, 0.552, 0.543, 0.551, 0.541, 0.536, 0.554, 0.498, 0.549, 0.546]),
 'KMN': ([0.43, 0.46, 0.48, 0.56, 0.45, 0.46, 0.50, 0.59, 0.46, 0.55, 0.59, 0.64, 0.50, 0.62, 0.65, 0.72],
         [0.31, 0.32, 0.36, 0.40, 0.33, 0.35, 0.36, 0.43, 0.39, 0.39, 0.40, 0.46, 0.41, 0.48, 0.51, 0.53]),
 'NLC': ([3.94, 4.23, 4.40, 5.10, 4.11, 4.19, 4.56, 5.35, 4.23, 5.06, 5.35, 5.81, 4.46, 5.64, 5.93, 6.59],
         [3.19, 3.27, 3.69, 4.15, 3.35, 3.61, 3.69, 4.36, 3.98, 4.02, 4.11, 4.74, 4.19, 4.91, 5.24, 5.45]),
 'CMI': ([None, 107, 112, 130, 104, 107, 117, 136, 108, 130, 136, 149, 117, 144, 152, 167],
         [None, 103, 116, 131, 106, 113, 116, 137, 124, 126, 129, 149, 132, 154, 165, 172]),
 'DHA': ([8.3, 10.3, 9.7, 9.5, 11.3, 10.3, 11.2, 12.4, 13.7, 10.8, 13.6, 13.1, 8.0, 11.1, 9.9, 16.6],
         [7.0, 7.6, 6.5, 7.2, 5.1, 6.5, 9.6, 8.0, 3.9, 6.5, 8.0, 6.9, 3.7, 5.2, 6.9, 8.2]),
 'FDA': ([0.82, 0.93, 0.97, 0.99, 0.99, 1.09, 1.17, 1.19, 1.00, 1.11, 1.18, 1.21, 0.86, 0.94, 1.07, 1.10],
         [0.64, 0.91, 0.94, 0.96, 0.77, 1.06, 1.11, 1.15, 0.93, 1.09, 1.23, 1.25, 0.61, 0.77, 0.80, 0.81]),
 'ALKP': ([34.2, 38.6, 39.6, 45.7, 41.2, 41.5, 51.2, 56.5, 35.1, 40.3, 50.7, 58.8, 35.4, 37.4, 40.3, 43.6],
          [20.5, 25.4, 26.0, 27.8, 20.3, 31.9, 30.5, 33.1, 25.7, 27.8, 28.2, 32.5, 18.5, 21.7, 26.7, 28.3]),
 # Fig. 2 bulk density and Fig. 3 TOC stock - DIGITISED (raster, calibrated axis ticks, bar-fill tops + 2 px outline)
 'BD': ([1.65, 1.71, 1.56, 1.47, 1.47, 1.57, 1.60, 1.58, 1.57, 1.55, 1.45, 1.52, 1.64, 1.50, 1.48, 1.39],
        [1.60, 1.60, 1.40, 1.60, 1.60, 1.67, 1.54, 1.68, 1.45, 1.34, 1.54, 1.35, 1.34, 1.40, 1.45, 1.44]),
 'STK': ([5.43, 5.74, 5.70, 6.38, 6.38, 5.69, 6.03, 7.18, 5.50, 6.52, 6.83, 7.32, 5.37, 6.85, 7.10, 7.73],
         [4.06, 4.10, 4.41, 4.94, 4.94, 4.51, 4.58, 5.55, 4.93, 4.93, 4.88, 5.65, 4.74, 5.45, 5.86, 6.07]),
}
SQI = [0.831, 0.910, 0.908, 0.934, 0.893, 0.892, 0.911, 0.941, 0.919, 0.929, 0.924, 0.942, 0.909, 0.911, 0.923, 0.931]
LAY = (('0-7.5', 0), ('7.5-15', 1))


def rows(B):
    st = ST; out = []

    def add(sheet, vals, body, unit, src, meth=M_SOIL, crop=SAMP, depth=None, d=1, y=1, yd='April 2016 (6th cycle)'):
        obs, nt = notes(st, body, y=y, d=d)
        v = base(st, SITE, {'year of data collection/experiment': yd, 'YEAR OF DATA (duration)': yd})
        if depth:
            v.update({'DEPTH': depth[1], 'DEPTH (as reported in paper)': depth[0]})
        v.update(vals)
        v.update({'UNIT': unit, 'Crop/season of sampling': crop, 'Data source': src, 'Method used (from paper)': meth, 'Obs': obs, 'Rep': 4, 'Notes/Doubts': nt,
                  'Fertilizer dose & other management': f'{n_lab} kg N/ha to rice and wheat (urea, 3 splits); ' + st['fert']})
        out.append((sheet, B.add_row(sheet, v)))

    def head(n, j):
        return f'ROW {"abc"[j]}: CT = RS0, CTR = {RS[j]} ({NL[n]}). '

    for n in range(4):
        n_lab = NL[n][1:]
        b = 4 * n
        for j in range(3):
            i = b + j + 1
            hd = head(n, j)
            # ---- yields and HI (4-yr pooled)
            add('YIELD', {'RICE YIELD_CT': T1['GR'][b], 'RICE YIELD_CTR': T1['GR'][i], 'WYIELD_CT': T1['GW'][b], 'WYIELD_CTR': T1['GW'][i],
                          'RSTRAW_CT': T1['SR'][b], 'RSTRAW_CTR': T1['SR'][i], 'W STRAW_CT': T1['SW'][b], 'W STRAW_CTR': T1['SW'][i]},
                hd + 'Table 1 rice and wheat grain and straw yield, POOLED 4 years (text: 2012-2015). OVERLAPPING SEASONS with study 290 (3-yr pool 2014-16) - FLAG (possible duplicate; drop for sensitivity). '
                'Straw incorporated before wheat (rice values = residual effect). Sustainable yield index (Fig. 1) - no sheet.',
                't/ha (rice 14 %, wheat 10 % moisture; straw oven-dry)', 'Table 1', 'Combine / manual harvest of 10 m2 net plot; plot thresher.',
                crop='Rice and wheat, 4-yr pooled (2012-2015)', y=4, yd='2012-2015 (4-yr pooled)')
            add('HARVEST INDEX', {'HI_RCT': T1['HR'][b], 'HI_RCTR': T1['HR'][i], 'HI_WCT': T1['HW'][b], 'HI_WCTR': T1['HW'][i]},
                hd + 'Table 1 harvest index (grain / total above-ground biomass), 4-yr pooled. Overlapping seasons with study 290 - FLAG.', 'ratio', 'Table 1',
                'HI = grain / (grain + straw).', crop='Rice and wheat, 4-yr pooled (2012-2015)', y=4, yd='2012-2015 (4-yr pooled)')
            ci, cc = CIN[b], CIN[i]
            add('C input', {'CIN_CT': f'=ROUND({ci[4]}*1000,0)', 'CIN_CTR': f'=ROUND({cc[4]}*1000,0)'},
                hd + f'Table 3 mean annual total C input to the 0-15 cm plough layer (straw + root + stubble + rhizodeposition C; ESTIMATED from biomass and C contents), Mg C/ha/yr x 1000. '
                f'Components (straw / root / stubble / rhizodeposition): RS0 {ci[0]} / {ci[1]} / {ci[2]} / {ci[3]}; {RS[j]} {cc[0]} / {cc[1]} / {cc[2]} / {cc[3]} Mg C/ha/yr.',
                'kg C/ha/yr (plant-derived C input, printed Mg C/ha/yr x 1000; ESTIMATED)', 'Table 3',
                'Root C 41.2 % (rice) / 39.1 % (wheat); shoot C 31.8 % / 35.2 % (Majumder et al. 2007); rhizodeposition 15 % / 12.6 % of above-ground biomass (Bronson et al. 1998).',
                crop='Annual (rice + wheat), mean of trial', yd='mean annual (period not stated)')
            add('SQI', {'SQI_CT': SQI[b], 'SQI_CTR': SQI[i]},
                hd + 'Figure 6 soil quality index (stacked KMnO4-C + FDA + BSR contributions; PCA-weighted MDS), DIGITISED stack tops (raster, calibrated 0.4-1.0 axis). CK 0.831 and RS0 N90 0.893 '
                'agree with the text (0.831 / 0.897); the text\'s "0.831 to 0.844" range contradicts its own values and the figure - FLAG.', 'index (0-1, PCA / MDS weighted)', 'Figure 6 (digitised)',
                'SQI = sum(Wi x Si) over MDS indicators KMnO4-C, FDA, BSR (PCA weights).', depth=('0-15 cm (0-7.5 / 7.5-15 cm data)', '0-15 CM'))
            for ly, k in LAY:
                dp = (f'{ly} cm', '0-15 CM')
                lh = hd + f'{ly} cm layer (D = 2 in the 0-15 CM class). '
                v = lambda key: (S[key][k][b], S[key][k][i])
                add('TOC', {'TOC_CT': v('TOC')[0], 'TOC_CTR': v('TOC')[1]}, lh + 'Table 4 total organic C (wet digestion, Snyder & Trofymow 1984 - total C by dichromate with external heat).',
                    'g/kg', 'Table 4', depth=dp, d=2)
                add('WSC', {'WSC_CT': v('WEOC')[0], 'WSC_CTR': v('WEOC')[1]}, lh + 'Table 4 WATER-EXTRACTABLE organic C (WEOC). Hot-water C of the same samples in the next WSC row (HWC).',
                    'mg/kg (WEOC, cold-water extractable)', 'Table 4', depth=dp, d=2)
                add('WSC', {'WSC_CT': v('HWC')[0], 'WSC_CTR': v('HWC')[1]}, lh + 'Table 4 HOT-WATER extractable C (HWC) - different extraction from WEOC (separate row; do not pool with WEOC rows - FLAG).',
                    'mg/kg (HWC, hot-water extractable C)', 'Table 4', depth=dp, d=2)
                kt, kc = v('KMN'); tt, tc = v('TOC')
                add('POXC(KMnO4-C)', {'POXC_CT': f'=ROUND({kt}*1000,0)', 'POXC_CTR': f'=ROUND({kc}*1000,0)'},
                    lh + 'Table 6 KMnO4-oxidisable C, printed g/kg x 1000 (sub-surface header misprinted "mg/kg" - values are g/kg, FLAG).', 'mg/kg (printed g/kg x 1000)', 'Table 6', depth=dp, d=2)
                nt_, nc_ = v('NLC')
                add('C liability', {'CL_CT': f'=ROUND({kt}/{nt_},3)', 'CL_CTR': f'=ROUND({kc}/{nc_},3)'},
                    lh + f'Carbon lability L DERIVED = KMnO4-C / non-labile C (Table 6, printed non-labile C {nt_} / {nc_} g/kg = TOC - KMnO4-C).', 'ratio (L = labile / non-labile C; DERIVED)', 'Table 6 (DERIVED)', depth=dp, d=2)
                add('CPI', {'CPI_CT': 1, 'CPI_CTR': f'=ROUND({tc}/{tt},3)'}, lh + 'CPI DERIVED with the row\'s CT (RS0 at the same N rate) as reference (workbook rule; the paper uses CK RS0 N0).',
                    'index (TOC / TOC of CT; DERIVED)', 'Table 4 (DERIVED)', depth=dp, d=2)
                add('LI', {'LI_CT': 1, 'LI_CTR': f'=ROUND(({kc}/{nc_})/({kt}/{nt_}),3)'}, lh + 'LI DERIVED = L(CTR) / L(CT), L = KMnO4-C / non-labile C (Table 6).',
                    'index (L / L of CT; DERIVED)', 'Table 6 (DERIVED)', depth=dp, d=2)
                cm = v('CMI')
                add('CMI', {'CMI_CT': 100, 'CMI_CTR': f'=ROUND(({tc}/{tt})*(({kc}/{nc_})/({kt}/{nt_}))*100,1)'},
                    lh + f'CMI DERIVED = CPI x LI x 100 with CT (RS0 at the same N) as reference (workbook rule). Printed CMI (reference CK RS0 N0): RS0 {cm[0] if cm[0] else "100 (reference)"}, {RS[j]} {cm[1]}.',
                    'index (CT = 100; DERIVED)', 'Tables 4 + 6 (DERIVED)', depth=dp, d=2)
                add('MBC', {'MBC_CT': v('MBC')[0], 'MBC_CTR': v('MBC')[1]}, lh + 'Table 5 microbial biomass C.', 'mg/kg', 'Table 5', depth=dp, d=2)
                add('RESP', {'RESP_CT': v('BSR')[0], 'RESP_CTR': v('BSR')[1]}, lh + 'Table 5 basal soil respiration (as printed).', 'ug C-CO2/g soil/h (as printed)', 'Table 5', depth=dp, d=2)
                add('qCO2', {'QCO2_CT': v('QCO2')[0], 'QCO2_CTR': v('QCO2')[1]}, lh + 'Table 5 respiratory quotient qCO2 (as printed).', 'ug C-CO2/h per ug biomass C x 10^3 (as printed)', 'Table 5', depth=dp, d=2)
                mt_, mc_ = v('MBC'); qm = v('QMIC')
                add('MICROBIAL QUOTIENT', {'QMB_CT': f'=ROUND({mt_}/({tt}*10),2)', 'QMB_CTR': f'=ROUND({mc_}/({tc}*10),2)'},
                    lh + f'Microbial quotient DERIVED = MBC / TOC x 100 (Tables 4-5). Printed "qmic" {qm[0]} / {qm[1]} (= MBC / TOC x 10 - different scaling, FLAG).', '% (MBC / TOC x 100; DERIVED)', 'Tables 4-5 (DERIVED)', depth=dp, d=2)
                add('DHA', {'DHA_CT': v('DHA')[0], 'DHA_CTR': v('DHA')[1]}, lh + 'Table 7 dehydrogenase activity, printed unit "g/kg" (implausible; probably ug TPF/g soil/h - FLAG).', 'as printed ("g/kg" - FLAG)', 'Table 7', depth=dp, d=2)
                add('FDA', {'FDA_CT': v('FDA')[0], 'FDA_CTR': v('FDA')[1]}, lh + 'Table 7 fluorescein diacetate hydrolysis, printed unit "mg/kg" (time basis not printed - FLAG).', 'mg fluorescein/kg (as printed)', 'Table 7', depth=dp, d=2)
                add('ALKP', {'ALP_CT': v('ALKP')[0], 'ALP_CTR': v('ALKP')[1]}, lh + 'Table 7 alkaline phosphatase, printed unit "mg/kg" (time basis not printed - FLAG).', 'mg p-nitrophenol/kg (as printed)', 'Table 7', depth=dp, d=2)
                add('BD', {'BD_CT': v('BD')[0], 'BD_CTR': v('BD')[1]}, lh + 'Figure 2 bulk density, DIGITISED (raster, calibrated 1.0-2.0 axis; bar-fill tops).', 'Mg/m3', 'Figure 2 (digitised)',
                    'Core method (7.2 cm inner diameter cores).', depth=dp, d=2)
            sk = (S['STK'][0][b], S['STK'][0][i]); sb = (S['STK'][1][b], S['STK'][1][i])
            add('stock-SOC', {'SOCs_CT': sk[0], 'SOCs_CTR': sk[1]}, hd + 'Figure 3 TOC stock 0-7.5 cm, DIGITISED (raster, calibrated 3-8 axis; caption says "Mg m-3", axis Mg C/ha).',
                'Mg C/ha', 'Figure 3 (digitised)', 'TOC stock = TOC x BD x depth.', depth=('0-7.5 cm', '0-10 CM'))
            add('stock-SOC', {'SOCs_CT': f'=ROUND({sk[0]}+{sb[0]},2)', 'SOCs_CTR': f'=ROUND({sk[1]}+{sb[1]},2)'},
                hd + f'TOC stock 0-15 cm DERIVED = digitised 0-7.5 + 7.5-15 cm layer stocks (Figure 3). 7.5-15 cm layer: RS0 {sb[0]}, {RS[j]} {sb[1]} Mg C/ha.',
                'Mg C/ha (DERIVED sum of layers)', 'Figure 3 (digitised, DERIVED)', 'TOC stock = TOC x BD x depth.', depth=('0-15 cm (sum of layers)', '0-20 CM'))
    return out


TM = [
    ('RS0 (straw removed)', 'Rice straw removed; wheat zero-till drilled (rotavation of RS0 plots not stated)', 'Puddled TPR', 'ZT drill (rotavation assumed)', 'No', '0', 'CT - FLAG', 'As study 290.', 'Medium', 'INCLUDED'),
    ('RS5.0 / RS7.5 / RS10.0', 'Chopped rice straw incorporated with a rotavator ~3 weeks before zero-till drilled wheat', 'Puddled TPR', 'Rotavator incorporation + ZT drill', 'Yes', '5.0 / 7.5 / 10.0', 'CTR rows a / b / c',
     'As study 290 (rotary incorporation).', 'Medium', 'INCLUDED'),
    ('N0 / N90 / N120 / N150', 'Fertiliser N to rice and wheat', 'n/a', 'n/a', 'n/a', None, 'Separate rows', 'Non-tillage factor (rule 33).', 'High', 'INCLUDED'),
]
STUDY_INFO = dict(estab=2010, yeardata='Yields 2012-2015 (4-yr pooled); soil April 2016', years='Yields 4-yr pooled; soil 1 sampling', texture='Sandy loam (12.8 % clay, 15.5 % silt, 71.5 % sand), Typic Ustochrept',
                  rotation='Rice-wheat', wheatvar='Not reported', ricevar='PR 118', N='0 / 90 / 120 / 150 (both crops)', P='60 P2O5 (wheat)', K='30 K2O (wheat)', residue='Rice straw 0 / 5.0 / 7.5 / 10.0 Mg/ha rotavated in',
                  irrigation='Rice flooded 15 d then 50 mm 2 d after ponded water disappears; wheat 4 x 75 mm', treatments='4 N x 4 straw rates (RBD, 4 reps)', supp='Appendices I-V (methods, PCA, correlations) - in the paper',
                  params=('Per N rate, CT (RS0) vs CTR (RS5 / 7.5 / 10, rows a-c): rice / wheat grain and straw yield and HI (4-yr pooled, overlap FLAG); annual C input; SQI (Fig. 6 digitised); '
                          '0-7.5 and 7.5-15 cm: TOC, WEOC and HWC (WSC sheet), KMnO4-C, C lability, CPI, LI, CMI (derived, CT reference), MBC, BSR, qCO2, microbial quotient (derived), DHA, FDA, Alk-P, '
                          'BD (Fig. 2 digitised); TOC stock 0-7.5 / 0-15 cm (Fig. 3 digitised)'),
                  notes=('COMPANION of study 290 (ext\\669.pdf; same PAU 2010 N x rice-straw trial). PARTIAL REPEAT (rule 136): new parameters entered; yields are a different (2012-15) pool overlapping 290\'s 2014-16 pool - FLAG. '
                         'NOT ON A SHEET: sustainable yield index (Fig. 1), PCA (Fig. 5, Appendices), TOC vs C-input regression (Fig. 4: TOC stock = 0.298 x C input + 3.414, R2 0.729). '
                         'Printed enzyme units questionable (DHA "g/kg") - entered as printed, flagged.'))
SITES = [('PAU research farm, Ludhiana', "30 56' N", "75 52' E", 30.933, 75.867, 'Paper', 'ST', 'Trial of study 290')]
