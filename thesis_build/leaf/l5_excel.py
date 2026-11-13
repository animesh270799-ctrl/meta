"""Step-by-step Excel workbook of the leaf-level analysis with editable (native) charts and live formulas."""
import numpy as np, pandas as pd, json, os, re
from openpyxl import Workbook
from openpyxl.chart import ScatterChart, BarChart, LineChart, Reference, Series
from openpyxl.chart.label import DataLabelList
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.utils import get_column_letter as CL
B = os.path.dirname(os.path.abspath(__file__)) + '/'; D = B + 'data/'
OUT = B + '../outputs/Leaf_ASD_analysis_stepwise.xlsx'
Z = np.load(D + 'prep.npz'); M = pd.read_csv(D + 'meta_leaf2.csv'); P = pd.read_csv(D + 'plot_table.csv')
F = pd.read_csv(D + 'feat_leaf_wri.csv'); Fp = pd.read_csv(D + 'feat_plot_wri.csv'); info = json.load(open(D + 'prep_info.json'))
R1 = json.load(open(D + 'res1.json')); RS = R1['RES']; R2 = json.load(open(D + 'res2.json'))
wl = Z['b5']; y = M.grade.values; G6 = [0, 1, 3, 5, 7, 9]
FONT = 'Arial'; HF = Font(name=FONT, bold=True, color='FFFFFF'); HFILL = PatternFill('solid', fgColor='00695C'); BF = Font(name=FONT, size=10)
TF = Font(name=FONT, bold=True, size=14, color='00695C'); NF = Font(name=FONT, size=9, italic=True, color='555555')
thin = Side(style='thin', color='BBBBBB'); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
wb = Workbook(); wb.remove(wb.active)

def sheet(name, title, note):
    ws = wb.create_sheet(name); ws['A1'] = title; ws['A1'].font = TF; ws['A2'] = note; ws['A2'].font = NF; ws.sheet_view.showGridLines = False
    return ws
def table(ws, r0, c0, df, fmt=None, widths=None):
    for j, c in enumerate(df.columns):
        cell = ws.cell(r0, c0 + j, str(c)); cell.font = HF; cell.fill = HFILL; cell.alignment = Alignment(wrap_text=True, vertical='center'); cell.border = BOX
    for i, row in enumerate(df.itertuples(index=False)):
        for j, v in enumerate(row):
            if isinstance(v, (np.floating, float)) and not np.isfinite(v): v = None
            elif isinstance(v, np.generic): v = v.item()
            cell = ws.cell(r0 + 1 + i, c0 + j, v); cell.font = BF; cell.border = BOX
            if fmt and isinstance(v, float): cell.number_format = fmt
    if widths:
        for j, w in enumerate(widths): ws.column_dimensions[CL(c0 + j)].width = w
    return r0 + 1, r0 + len(df)            # first and last data row
def note(ws, r, c, text):
    ws.cell(r, c, text).font = NF
def scatter(ws, anchor, title, xt, yt, xref, yrefs, names, lines=True, w=24, h=11, colors=None):
    ch = ScatterChart(); ch.title = title; ch.x_axis.title = xt; ch.y_axis.title = yt; ch.style = 13; ch.width = w; ch.height = h
    for k, (yr, nm) in enumerate(zip(yrefs, names)):
        s = Series(yr, xref, title=nm)
        if lines: s.marker.symbol = 'none'; s.smooth = False
        else: s.marker.symbol = 'circle'; s.marker.size = 4; s.graphicalProperties.line.noFill = True
        if colors: s.graphicalProperties.line.solidFill = colors[k % len(colors)]; s.marker.graphicalProperties.solidFill = colors[k % len(colors)] if not lines else None
        ch.series.append(s)
    ch.x_axis.delete = False; ch.y_axis.delete = False; ws.add_chart(ch, anchor); return ch
def bar(ws, anchor, title, yt, cats, datas, horizontal=False, w=20, h=10, stacked=False, labels=False):
    ch = BarChart(); ch.type = 'bar' if horizontal else 'col'; ch.title = title; ch.y_axis.title = yt; ch.style = 10; ch.width = w; ch.height = h
    for d in datas: ch.add_data(d, titles_from_data=True)
    ch.set_categories(cats); ch.x_axis.delete = False; ch.y_axis.delete = False
    if stacked: ch.grouping = 'stacked'; ch.overlap = 100
    if labels: ch.dataLabels = DataLabelList(); ch.dataLabels.showVal = True
    ws.add_chart(ch, anchor); return ch
GC = ['2E7D32', '9CCC65', 'FDD835', 'FB8C00', 'E53935', '7B1FA2']

# ===================== README =====================
ws = sheet('README', 'Leaf-level ASD analysis of white rust in mustard — step-by-step workbook', 'Each sheet is one step of the proposed methodology. Charts are native Excel charts (editable). Blue cells = inputs from the data; black = formulas; grey italic = notes.')
rows = [['Sheet', 'Step', 'Method (reference)'],
        ['0_Leaf_data', 'Tier 0: leaf metadata, grades, folds and leaf features', 'Leaf grade 0–9 key (Conn et al., 1990)'],
        ['0_Plot_PDI', 'Tier 0: plot PDI computed with formulas from leaf scores', 'PDI = Σ score/(9 n) × 100 (Wheeler, 1969; Conn et al., 1990)'],
        ['0_Grade_counts', 'Tier 0: leaves per grade and date (COUNTIFS)', '—'],
        ['1_Preprocessing', 'Splice correction, band range, water bands, Savitzky–Golay, derivatives', 'Hueni and Bialek (2017); Savitzky and Golay (1964); Tsai and Philpot (1998)'],
        ['1_Mean_spectra', 'Grade-mean reflectance and first derivative', '—'],
        ['1_Index_formulas', 'Tier 1: 48 indices + red edge computed by formulas on plot-mean reflectance', 'Formulas and references in the definition table'],
        ['2_Scalogram', 'Tier 2: correlation scalogram R, FD, SD vs plot PDI', 'Shukla et al. (2024); Cheng et al. (2010)'],
        ['2_ReliefF', 'Tier 2: ReliefF weights for six leaf grades', 'Robnik-Šikonja and Kononenko (2003); Mahlein et al. (2013)'],
        ['2_Band_lists', 'Tier 2: one band per correlated region; robust / regression / classification lists', 'Tian et al. (2021)'],
        ['3_WRI', 'Tier 3: White Rust Index search (VNIR and SWIR)', 'Mahlein et al. (2013)'],
        ['4_ANOVA', 'Tier 4: one-way ANOVA, Tukey HSD, Pearson r with PDI', 'Tukey (1949); Mahlein et al. (2019)'],
        ['5_CDA', 'Tier 5: VIF < 10 and two-step stepwise CDA', 'Bhattacharya and Chattopadhyay (2013); Klecka (1980)'],
        ['6_Boruta', 'Tier 6: Boruta DSF pools (classification and regression)', 'Kursa and Rudnicki (2010); Mustafa et al. (2023)'],
        ['7_SFFS', 'Objective 2: ML-SFFS optimum feature combinations per fold and model', 'Pudil et al. (1994); Tian et al. (2021)'],
        ['8_Models', 'Objective 2: model comparison (nested leave-one-replication-out)', 'Cortes and Vapnik (1995); Breiman (2001); Wold et al. (2001)'],
        ['8_Confusion', 'Objective 2: confusion matrix with metric formulas', 'Cohen (1960); Sokolova and Lapalme (2009)'],
        ['8_Obs_vs_pred', 'Objective 2: PDI observed vs predicted with R², RMSE, RPD formulas', 'Liu et al. (2024)'],
        ['8_By_date_variety', 'Objective 2: performance per date and variety', '—'],
        ['References', 'Full references', '—']]
table(ws, 4, 1, pd.DataFrame(rows[1:], columns=rows[0]), widths=[20, 70, 70])

# ===================== 0 Leaf data =====================
ws = sheet('0_Leaf_data', 'Tier 0 — leaf metadata, grade, fold and leaf features', 'One row per leaf spectrum (2339). fold = test replication in leave-one-replication-out (0 = R1, 1 = R2, 2 = R3; control plots split by variety). Features computed from the smoothed leaf spectrum (see 1_Index_formulas for formulas).')
LD = pd.concat([M[['date', 'plot', 'variety', 'rep', 'inoc', 'stage', 'leaf', 'grade', 'diseased', 'fold']], F.round(6)], axis=1)
r1, r2 = table(ws, 4, 1, LD)
for c in range(1, LD.shape[1] + 1): ws.column_dimensions[CL(c)].width = 11
ws.freeze_panes = 'B5'; LEAF_LAST = r2; leaf_col = {c: CL(i + 1) for i, c in enumerate(LD.columns)}

# ===================== 0 Plot PDI (formulas) =====================
ws = sheet('0_Plot_PDI', 'Tier 0 — plot-level disease severity (PDI) computed from leaf scores', 'n leaves = COUNTIFS, Σ score = SUMIFS over 0_Leaf_data; PDI = Σ score / (9 × n) × 100 (formula as in the field sheets).')
hdr = ['date', 'plot', 'variety', 'rep', 'inoculation', 'fold', 'n leaves', 'Σ score', 'PDI (%)']
for j, h in enumerate(hdr): c = ws.cell(4, j + 1, h); c.font = HF; c.fill = HFILL
dc, pc, gc = leaf_col['date'], leaf_col['plot'], leaf_col['grade']
for i, r in enumerate(P.itertuples()):
    rr = 5 + i
    for j, v in enumerate([r.date, r.plot, r.variety, r.rep, r.inoc, r.fold]): ws.cell(rr, j + 1, v).font = Font(name=FONT, size=10, color='0000FF')
    ws.cell(rr, 7, "=COUNTIFS('0_Leaf_data'!$%s$5:$%s$%d,A%d,'0_Leaf_data'!$%s$5:$%s$%d,B%d)" % (dc, dc, LEAF_LAST, rr, pc, pc, LEAF_LAST, rr))
    ws.cell(rr, 8, "=SUMIFS('0_Leaf_data'!$%s$5:$%s$%d,'0_Leaf_data'!$%s$5:$%s$%d,A%d,'0_Leaf_data'!$%s$5:$%s$%d,B%d)" % (gc, gc, LEAF_LAST, dc, dc, LEAF_LAST, rr, pc, pc, LEAF_LAST, rr))
    ws.cell(rr, 9, '=IF(G%d>0,H%d/(9*G%d)*100,"")' % (rr, rr, rr)).number_format = '0.0'
PLOT_LAST = 4 + len(P)
ws.cell(4, 11, 'Summary').font = Font(name=FONT, bold=True)
for k, d in enumerate(sorted(P.date.unique())):
    ws.cell(5 + k, 11, d); ws.cell(5 + k, 12, '=AVERAGEIFS(I$5:I$%d,A$5:A$%d,K%d)' % (PLOT_LAST, PLOT_LAST, 5 + k)).number_format = '0.0'
ws.cell(4, 12, 'Mean PDI').font = Font(name=FONT, bold=True)
bar(ws, 'N4', 'Mean plot PDI by date', 'PDI (%)', Reference(ws, min_col=11, min_row=5, max_row=8), [Reference(ws, min_col=12, min_row=4, max_row=8)], w=14, h=8, labels=True)
for c, w in zip('ABCDEFGHI', [11, 6, 8, 6, 10, 6, 9, 9, 9]): ws.column_dimensions[c].width = w

# ===================== 0 Grade counts =====================
ws = sheet('0_Grade_counts', 'Tier 0 — number of leaves per grade and date', 'COUNTIFS over 0_Leaf_data.')
dates = sorted(M.date.unique())
ws.cell(4, 1, 'Date').font = HF; ws.cell(4, 1).fill = HFILL
for j, g in enumerate(G6): c = ws.cell(4, 2 + j, 'Grade %d' % g); c.font = HF; c.fill = HFILL
ws.cell(4, 8, 'Total').font = HF; ws.cell(4, 8).fill = HFILL
for i, d in enumerate(dates + ['All dates']):
    rr = 5 + i; ws.cell(rr, 1, d)
    for j, g in enumerate(G6):
        crit = ("'0_Leaf_data'!$%s$5:$%s$%d,%d" % (gc, gc, LEAF_LAST, g)) + ((",'0_Leaf_data'!$%s$5:$%s$%d,$A%d" % (dc, dc, LEAF_LAST, rr)) if d != 'All dates' else '')
        ws.cell(rr, 2 + j, '=COUNTIFS(%s)' % crit)
    ws.cell(rr, 8, '=SUM(B%d:G%d)' % (rr, rr))
ch = bar(ws, 'A12', 'Leaves per grade and date', 'Number of leaves', Reference(ws, min_col=1, min_row=5, max_row=8), [Reference(ws, min_col=2 + j, min_row=4, max_row=8) for j in range(6)], stacked=True, w=20, h=10)
for s, c in zip(ch.series, GC): s.graphicalProperties.solidFill = c

# ===================== 1 Preprocessing =====================
ws = sheet('1_Preprocessing', 'Pre-processing of the ASD leaf spectra', 'Applied to every leaf spectrum before feature extraction.')
pp = [['1', 'Splice correction at the VNIR/SWIR1 detector join', 'Offset at 1001 nm removed from 1001–1800 nm (mean step %.4f ± %.4f reflectance)' % (info['splice_mean'], info['splice_sd']), 'Hueni and Bialek (2017)'],
      ['2', 'Spectral range', '400–2400 nm kept (350–399 nm noisy; > 2400 nm low signal)', 'Shukla et al. (2024)'],
      ['3', 'Water-vapour bands removed', '1350–1450 nm and 1800–1950 nm', 'Thenkabail et al. (2004)'],
      ['4', 'Smoothing', 'Savitzky–Golay filter, window 11 nm, 2nd-order polynomial', 'Savitzky and Golay (1964)'],
      ['5', 'Derivatives', 'First (FD) and second (SD) derivatives from the same Savitzky–Golay fit', 'Tsai and Philpot (1998)'],
      ['6', 'Band sampling for band-level analysis', '5 nm steps → 349 bands × (R, FD, SD) = 1047 band features', 'Mahlein et al. (2013)'],
      ['7', 'Plot spectrum', 'Mean of the leaf spectra of each plot-date (192 plot-dates)', 'Liu et al. (2024)']]
table(ws, 4, 1, pd.DataFrame(pp, columns=['No.', 'Step', 'Setting', 'Reference']), widths=[5, 40, 70, 28])
sp = Z['splice']; hist, edges = np.histogram(sp, bins=15)
r1, r2 = table(ws, 14, 1, pd.DataFrame({'Splice step (bin centre)': np.round((edges[:-1] + edges[1:]) / 2, 4), 'Number of leaves': hist}))
bar(ws, 'E14', 'Distribution of the 1000 nm splice step', 'Leaves', Reference(ws, min_col=1, min_row=r1, max_row=r2), [Reference(ws, min_col=2, min_row=r1 - 1, max_row=r2)], w=16, h=8)

# ===================== 1 Mean spectra =====================
ws = sheet('1_Mean_spectra', 'Grade-mean leaf reflectance and first derivative (5 nm bands)', 'Mean over all leaves of each grade; water bands are absent from the table, so the lines join across the gaps.')
MS = pd.DataFrame({'wavelength_nm': wl})
for g in G6: MS['R grade %d' % g] = Z['R'][y == g].mean(0)
for g in G6: MS['FD grade %d' % g] = Z['FD'][y == g].mean(0)
r1, r2 = table(ws, 4, 1, MS.round(5))
scatter(ws, 'O4', 'Mean reflectance by grade', 'Wavelength (nm)', 'Reflectance', Reference(ws, min_col=1, min_row=r1, max_row=r2), [Reference(ws, min_col=2 + k, min_row=r1, max_row=r2) for k in range(6)], ['grade %d' % g for g in G6], colors=GC)
scatter(ws, 'O28', 'Mean first derivative by grade', 'Wavelength (nm)', 'FD (×10⁻³ nm⁻¹)', Reference(ws, min_col=1, min_row=r1, max_row=r2), [Reference(ws, min_col=8 + k, min_row=r1, max_row=r2) for k in range(6)], ['grade %d' % g for g in G6], colors=GC)

# ===================== 1 Index formulas (live) =====================
ws = sheet('1_Index_formulas', 'Tier 1 — vegetation indices computed by Excel formulas on plot-mean reflectance', 'Columns R415 … R1982 hold the plot-mean smoothed reflectance; every index column is a live formula. Definition table with references at the right.')
need = sorted({int(w) for w in re.findall(r'R(\d{3,4})', ' '.join(['R415 R430 R435 R445 R450 R470 R500 R531 R534 R550 R554 R570 R635 R650 R651 R670 R675 R677 R680 R691 R698 R700 R704 R712 R732 R750 R752 R760 R761 R780 R800 R819 R820 R850 R860 R900 R970 R1068 R1148 R1175 R1240 R1301 R1560 R1600 R1649 R1660 R1982']))})
Rp1 = Z['Rp1nm']
base = pd.DataFrame({'date': P.date, 'plot': P['plot'], 'PDI': P.PDI.round(2)})
for w in need: base['R%d' % w] = Rp1[:, w - 350].round(6)
r1, r2 = table(ws, 4, 1, base)
col = {c: CL(i + 1) for i, c in enumerate(base.columns)}
DEF = [('NDVI780', '(R780-R670)/(R780+R670)', 'Raun et al. (2001)'), ('NDVI850', '(R850-R650)/(R850+R650)', 'Raun et al. (2001)'), ('NDVI761', '(R761-R651)/(R761+R651)', 'Raun et al. (2001)'),
       ('SR900', 'R900/R680', 'Jordan (1969)'), ('SR850', 'R850/R680', 'Jordan (1969)'), ('SR761', 'R761/R651', 'Jordan (1969)'), ('GNDVI', '(R850-R550)/(R850+R550)', 'Gitelson et al. (1996)'),
       ('RDVI', '(R800-R670)/SQRT(R800+R670)', 'Roujean and Bréon (1995)'), ('MSR', '(R800/R670-1)/SQRT(R800/R670+1)', 'Chen (1996)'),
       ('TVI', '0.5*(120*(R750-R550)-200*(R670-R550))', 'Broge and Leblanc (2001)'), ('MTVI1', '1.2*(1.2*(R800-R550)-2.5*(R670-R550))', 'Haboudane et al. (2004)'),
       ('MTVI2', '1.5*(1.2*(R800-R550)-2.5*(R670-R550))/SQRT((2*R800+1)^2-(6*R800-5*SQRT(R670))-0.5)', 'Haboudane et al. (2004)'),
       ('MCARI1', '1.2*(2.5*(R800-R670)-1.3*(R800-R550))', 'Haboudane et al. (2004)'), ('TCARI', '3*((R700-R670)-0.2*(R700-R550)*(R700/R670))', 'Haboudane et al. (2002)'),
       ('VIgreen', '(R550-R670)/(R550+R670)', 'Gitelson et al. (2002)'), ('GI', 'R554/R677', 'Guo et al. (2021)'), ('RR', '1/R700', 'Mustafa et al. (2023)'),
       ('PSSRa', 'R800/R680', 'Blackburn (1998)'), ('PSSRb', 'R800/R635', 'Blackburn (1998)'), ('PSSRc', 'R800/R470', 'Blackburn (1998)'),
       ('RARSa', 'R675/R700', 'Chappelle et al. (1992)'), ('RARSb', 'R675/(R700*R650)', 'Chappelle et al. (1992)'), ('RARSc', 'R760/R500', 'Chappelle et al. (1992)'),
       ('SIPI', '(R800-R445)/(R800-R680)', 'Peñuelas et al. (1995)'), ('NPCI', '(R680-R430)/(R680+R430)', 'Peñuelas et al. (1994)'), ('PSRI', '(R680-R500)/R750', 'Merzlyak et al. (1999)'),
       ('ARI', '1/R550-1/R700', 'Gitelson et al. (2001)'), ('PPR', '(R550-R450)/(R550+R450)', 'Metternicht (2003)'), ('NRI', '(R570-R670)/(R570+R670)', 'Bausch and Duke (1996)'),
       ('PRI', '(R531-R570)/(R531+R570)', 'Gamon et al. (1992)'), ('NPQI', '(R415-R435)/(R415+R435)', 'Barnes et al. (1992)'), ('RVSI', '(R712+R752)/2-R732', 'Merton and Huntington (1999)'),
       ('HI', '(R534-R698)/(R534+R698)-0.5*R704', 'Mahlein et al. (2013)'), ('WI', 'R900/R970', 'Peñuelas et al. (1997)'), ('NWI-2', '(R970-R850)/(R970+R850)', 'Babar et al. (2006)'),
       ('DWSI-1', 'R800/R1660', 'Apan et al. (2004)'), ('DWSI-4', 'R550/R680', 'Apan et al. (2004)'), ('ROTI', 'R1175/(R1982+R691)', 'Bhattacharya and Chattopadhyay (2013)'),
       ('DWSI-2', 'R1660/R550', 'Apan et al. (2004)'), ('DWSI-3', 'R1660/R680', 'Apan et al. (2004)'), ('DWSI-5', '(R800+R550)/(R1660+R680)', 'Apan et al. (2004)'),
       ('NDWI', '(R860-R1240)/(R860+R1240)', 'Gao (1996)'), ('MSI', 'R1600/R820', 'Hunt and Rock (1989)'), ('NDII', '(R819-R1649)/(R819+R1649)', 'Hardisky et al. (1983)'),
       ('RBI_M', 'R1148/R1301', 'Mandal et al. (2023)'), ('NDBI', '(R1148-R1301)/(R1148+R1301)', 'Mandal et al. (2023)'), ('RBI_R', '(R1068-R1560)/(R1068+R1560)', 'Ramalingam et al. (2026)')]
c0 = base.shape[1] + 1
for j, (nm, fx, ref) in enumerate(DEF):
    c = ws.cell(4, c0 + j, nm); c.font = HF; c.fill = PatternFill('solid', fgColor='AD1457')
    for i in range(len(P)):
        rr = 5 + i; ws.cell(rr, c0 + j, '=' + re.sub(r'R(\d{3,4})', lambda m: '%s%d' % (col['R' + m.group(1)], rr), fx)).number_format = '0.0000'
INDEX_COL = {nm: CL(c0 + j) for j, (nm, _, _) in enumerate(DEF)}
cd = c0 + len(DEF) + 1
dd = pd.DataFrame([[nm, fx.replace('*', '×'), 'SWIR disease index' if nm in info['swir9'] else 'Base index', ref] for nm, fx, ref in DEF], columns=['Index', 'Formula (R = reflectance at nm)', 'Group', 'Reference'])
table(ws, 4, cd, dd)
ws.cell(4 + len(DEF) + 2, cd, 'Red-edge parameters (computed in Python from the first derivative): REP = wavelength of max FD in 680–750 nm; Dr = max FD; SDr = area of FD over 680–750 nm (Horler et al., 1983; Filella and Peñuelas, 1994).').font = NF
ws.freeze_panes = 'D5'

# ===================== 2 Scalogram =====================
ws = sheet('2_Scalogram', 'Tier 2 — correlation scalogram (plot level, n = 192): Pearson r of R, FD, SD with PDI', 'Candidates: p < 0.01 and top 5% |r| in each spectrum type, then one band per correlated region (see 2_Band_lists). Method: Shukla et al. (2024).')
S = pd.read_csv(D + 't_scalogram.csv'); r1, r2 = table(ws, 4, 1, S.round(5))
scatter(ws, 'I4', 'Correlation scalogram vs plot PDI', 'Wavelength (nm)', 'Pearson r', Reference(ws, min_col=1, min_row=r1, max_row=r2), [Reference(ws, min_col=c, min_row=r1, max_row=r2) for c in (2, 4, 6)], ['R', 'FD', 'SD'], colors=['2E7D32', '1565C0', 'AD1457'], w=26, h=12)

# ===================== 2 ReliefF =====================
ws = sheet('2_ReliefF', 'Tier 2 — ReliefF weights for six leaf grades (n = 2339, k = 10, same-plot neighbours excluded)', 'Candidates: top 5% of the 1047 weights, then one band per correlated region. Method: Robnik-Šikonja and Kononenko (2003).')
W = pd.read_csv(D + 't_relieff.csv'); r1, r2 = table(ws, 4, 1, W.round(6))
scatter(ws, 'F4', 'ReliefF weights (six grades)', 'Wavelength (nm)', 'ReliefF weight', Reference(ws, min_col=1, min_row=r1, max_row=r2), [Reference(ws, min_col=c, min_row=r1, max_row=r2) for c in (2, 3, 4)], ['R', 'FD', 'SD'], colors=['2E7D32', '1565C0', 'AD1457'], w=26, h=12)

# ===================== 2 Band lists =====================
ws = sheet('2_Band_lists', 'Tier 2 — candidate bands (one per correlated region) and the three band lists', 'Common region or within ±10 nm in both lists → robust band (both tasks); scalogram-only → regression list; ReliefF-only → classification list (Tian et al., 2021).')
cand = pd.read_csv(D + 't_band_candidates.csv'); r1, r2 = table(ws, 4, 1, cand.round(4), widths=[18, 10, 14, 10, 24])
t2 = RS['tier2']; L = max(len(t2['robust']), len(t2['regonly']), len(t2['clsonly']))
lists = pd.DataFrame({'Robust (both tasks)': t2['robust'] + [''] * (L - len(t2['robust'])), 'Regression only': t2['regonly'] + [''] * (L - len(t2['regonly'])), 'Classification only': t2['clsonly'] + [''] * (L - len(t2['clsonly']))})
table(ws, 4, 8, lists, widths=[20, 18, 20])
summ = pd.DataFrame([['Correlated regions (r ≥ 0.95): R / FD / SD', '%d / %d / %d' % (t2['n_regions']['R'], t2['n_regions']['FD'], t2['n_regions']['SD'])],
                     ['Median r between adjacent 5 nm reflectance bands', round(t2['median_adjacent_r'], 4)],
                     ['Scalogram candidates → one per region', '%d → %d' % (t2['n_scal_cand'], t2['n_scal_reg'])], ['ReliefF candidates → one per region', '%d → %d' % (t2['n_rel_cand'], t2['n_rel_reg'])],
                     ['Max |r| (band): R / FD / SD', ' / '.join('%.2f (%d nm)' % tuple(t2['max_r'][t]) for t in ('R', 'FD', 'SD'))]], columns=['Quantity', 'Value'])
table(ws, 6 + L, 8, summ, widths=[20, 18, 20])

# ===================== 3 WRI =====================
ws = sheet('3_WRI', 'Tier 3 — White Rust Index (WRI) search: WRI = ND(λ1, λ2) + w × R(λ3)', 'Healthy (grade 0) vs diseased leaves; bands at 6 nm; ReliefF top 25% of bands and normalised differences (≥ 50 nm apart); weights w ∈ {−1, −0.5, 0, 0.5, 1}; 8-fold plot-grouped CV of the threshold (Mahlein et al., 2013).')
t3 = RS['tier3']
sm = pd.DataFrame([['VNIR (450–950 nm)', t3['vnir']['n_bands'], t3['vnir']['n_pairs'], t3['vnir']['n_cand'], t3['vnir']['formula'], round(t3['vnir']['best']['ba_cv'], 3)],
                   ['SWIR (1000–2400 nm)', t3['swir']['n_bands'], t3['swir']['n_pairs'], t3['swir']['n_cand'], t3['swir']['formula'], round(t3['swir']['best']['ba_cv'], 3)]],
                  columns=['Region', 'Bands', 'ND pairs', 'Candidates', 'Best index', 'Balanced accuracy (CV)'])
table(ws, 4, 1, sm, widths=[22, 8, 10, 12, 34, 14])
r1, r2 = table(ws, 9, 1, pd.read_csv(D + 't_wri_vnir_top.csv').round(4).head(10))
note(ws, r2 + 1, 1, 'Top 10 VNIR candidates (screened on all leaves, accuracy from 8-fold plot-grouped CV).')
r1b, r2b = table(ws, r2 + 3, 1, pd.read_csv(D + 't_wri_swir_top.csv').round(4).head(10))
note(ws, r2b + 1, 1, 'Top 10 SWIR candidates.')
ws.cell(4, 9, 'Grade').font = HF; ws.cell(4, 9).fill = HFILL; ws.cell(4, 10, 'Mean WRI_VNIR').font = HF; ws.cell(4, 10).fill = HFILL; ws.cell(4, 11, 'Mean WRI_SWIR').font = HF; ws.cell(4, 11).fill = HFILL
for k, g in enumerate(G6):
    ws.cell(5 + k, 9, g)
    for cc, fn in ((10, 'WRI_VNIR'), (11, 'WRI_SWIR')):
        ws.cell(5 + k, cc, "=AVERAGEIFS('0_Leaf_data'!$%s$5:$%s$%d,'0_Leaf_data'!$%s$5:$%s$%d,I%d)" % (leaf_col[fn], leaf_col[fn], LEAF_LAST, gc, gc, LEAF_LAST, 5 + k)).number_format = '0.0000'
bar(ws, 'M4', 'Mean VNIR WRI by leaf grade', 'WRI', Reference(ws, min_col=9, min_row=5, max_row=10), [Reference(ws, min_col=10, min_row=4, max_row=10)], w=14, h=8)
ws.cell(12, 9, 'r (WRI_VNIR, PDI) at plot level').font = Font(name=FONT, bold=True); ws.cell(12, 12, round(t3['r_pdi'] if t3['chosen'] == 'VNIR' else float(np.corrcoef(Fp.WRI_VNIR, P.PDI)[0, 1]), 3))

# ===================== 4 ANOVA =====================
ws = sheet('4_ANOVA', 'Tier 4 — univariate response: one-way ANOVA across six grades (leaves), Tukey HSD and Pearson r with PDI (plots)', 'F, p, η² = SS_between/SS_total; r_PDI_plot from plot-mean features (n = 192); rho_score_leaf = Spearman ρ with leaf grade. Sorted by F. p-values describe leaves within plots (not independent) and are used only to rank features (Mahlein et al., 2019).')
A = pd.read_csv(D + 't_anova.csv'); A2 = A[['Feature', 'Group', 'F', 'p', 'eta2', 'r_PDI_plot', 'rho_score_leaf'] + ['mean_g%d' % g for g in G6]]
r1, r2 = table(ws, 4, 1, A2.round(4)); ws.column_dimensions['A'].width = 14
bar(ws, 'P4', 'Top 15 features by ANOVA F', 'F', Reference(ws, min_col=1, min_row=r1, max_row=r1 + 14), [Reference(ws, min_col=3, min_row=r1 - 1, max_row=r1 + 14)], w=18, h=10)
lt = RS['tier4']['letters']; TL = pd.DataFrame([[k] + [lt[k][str(g)] for g in G6] for k in lt], columns=['Feature'] + ['Grade %d' % g for g in G6])
table(ws, 26, 16, TL); note(ws, 26 + len(TL) + 1, 16, 'Tukey HSD letters (α = 0.05): grades sharing a letter do not differ (Tukey, 1949).')

# ===================== 5 CDA =====================
ws = sheet('5_CDA', 'Tier 5 — VIF < 10 and two-step stepwise canonical discriminant analysis (six leaf grades)', 'Step 1: classification band list; step 2: 48 indices + REP, Dr, SDr + VIF-free WRI. Forward entry by Wilks\' lambda (p < 0.001, at most 10 variables). Accuracy: LDA with equal priors, leave-one-replication-out (Bhattacharya and Chattopadhyay, 2013).')
row = 4
for lab, st in (('Step 1 (bands)', RS['tier5']['step1']), ('Step 2 (indices + red edge + WRI)', RS['tier5']['step2'])):
    ws.cell(row, 1, lab).font = Font(name=FONT, bold=True, size=11, color='AD1457'); row += 1
    s = pd.DataFrame([['Variables in', st['n_in']], ['After VIF < 10', st['n_vif']], ['Selected by stepwise CDA', len(st['selected'])], ['Canonical r (functions 1–3)', ', '.join('%.3f' % v for v in st['cancor'][:3])],
                      ['Share of discriminating variance, function 1', '%.1f%%' % (100 * st['share'][0])], ["Wilks' lambda (final)", round(st['wilks'], 4)], ['LORO accuracy', round(st['acc'], 3)], ['LORO macro-F1', round(st['macro_f1'], 3)], ['±1-grade accuracy', round(st['adj'], 3)]], columns=['Quantity', 'Value'])
    a, b = table(ws, row, 1, s, widths=[40, 22]); row = b + 2
    stp = pd.DataFrame(st['steps']).round(4); a, b = table(ws, row, 1, stp); row = b + 2
    cf = pd.DataFrame({'Variable': st['selected'], 'Std. coefficient F1': [c[0] for c in st['std_coef']], 'Std. coefficient F2': [c[1] for c in st['std_coef']], 'Structure r F1': [c[0] for c in st['struct']], 'Structure r F2': [c[1] for c in st['struct']]}).round(3)
    a, b = table(ws, row, 1, cf); row = b + 2
    ce = pd.DataFrame({'Grade': G6, 'Centroid F1': [c[0] for c in st['centroids']], 'Centroid F2': [c[1] for c in st['centroids']]}).round(3)
    a, b = table(ws, row, 1, ce)
    scatter(ws, 'H%d' % (a - 1), 'Grade centroids — ' + lab, 'Canonical function 1', 'Canonical function 2', Reference(ws, min_col=2, min_row=a, max_row=b), [Reference(ws, min_col=3, min_row=a, max_row=b)], ['centroids'], lines=False, w=14, h=8)
    row = b + 12

# ===================== 6 Boruta =====================
ws = sheet('6_Boruta', 'Tier 6 — Boruta disease-specific feature (DSF) pools', 'Random forest, alpha = 0.01, up to 100 iterations; classification on leaves (six grades), regression on plots (PDI). Importance = RF mean decrease in impurity (Kursa and Rudnicki, 2010).')
for k, (nm, c0) in enumerate((('boruta_cls', 1), ('boruta_reg', 7))):
    T = pd.read_csv(D + 't_%s.csv' % nm).round(4); a, b = table(ws, 4, c0, T, widths=[14, 12, 6, 11])
    bar(ws, '%s%d' % (CL(13 if k == 0 else 13), 4 if k == 0 else 26), 'Boruta importance — ' + ('classification' if k == 0 else 'regression') + ' (top 20)', 'RF importance', Reference(ws, min_col=c0, min_row=a, max_row=a + 19), [Reference(ws, min_col=c0 + 3, min_row=a - 1, max_row=a + 19)], horizontal=True, w=16, h=11)

# ===================== 7 SFFS =====================
ws = sheet('7_SFFS', 'Objective 2 — nested selection per training fold: Tier 2 → Boruta → VIF → ML-SFFS (optimum feature combination, OFC)', 'Inner grouped 3-fold CV inside the training replications; criterion macro-F1 (classification) or RMSE (regression); smallest subset within 0.01 (2% for RMSE) of the best (Pudil et al., 1994; Tian et al., 2021).')
rows = []
for f in R2['folds']:
    for mname, o in f['ofc'].items():
        rows.append([f['test_rep'], 'Regression' if mname.startswith('R_') else 'Classification', mname.replace('R_', ''), len(o['features']), ', '.join(o['features']), json.dumps(o['params'])])
a, b = table(ws, 4, 1, pd.DataFrame(rows, columns=['Test replication', 'Task', 'Model', 'n features', 'Optimum feature combination', 'Tuned parameters']), widths=[12, 14, 8, 10, 80, 34])
fs = pd.DataFrame([[f['test_rep'], f['n_cls_bands'], f['n_reg_bands'], f['boruta_cls'], f['boruta_reg'], len(f['vif_cls']), len(f['vif_reg'])] for f in R2['folds']],
                  columns=['Test replication', 'Class. bands (Tier 2)', 'Regr. bands (Tier 2)', 'Boruta confirmed (class.)', 'Boruta confirmed (regr.)', 'After VIF (class.)', 'After VIF (regr.)'])
a2, b2 = table(ws, b + 3, 1, fs)
cu = R2['folds'][0]['ofc']; ks = sorted({int(k) for nm in ('SVM', 'RF', 'k-NN') for k in cu[nm]['curve']})
cur = pd.DataFrame({'n features': ks, **{nm: [cu[nm]['curve'].get(str(k)) for k in ks] for nm in ('SVM', 'RF', 'k-NN')}})
a3, b3 = table(ws, b2 + 3, 1, cur.round(4))
scatter(ws, 'H%d' % (b2 + 3), 'ML-SFFS curves, classification (fold R1 training)', 'Number of features', 'Inner-CV macro-F1', Reference(ws, min_col=1, min_row=a3, max_row=b3), [Reference(ws, min_col=c, min_row=a3, max_row=b3) for c in (2, 3, 4)], ['SVM', 'RF', 'k-NN'], w=16, h=9)

# ===================== 8 Models =====================
ws = sheet('8_Models', 'Objective 2 — model comparison (nested leave-one-replication-out)', 'Classification: leaves, six grades. Regression: plot PDI. Baselines without the methodology\'s selection: PLS-DA/PLSR on the full 349-band spectrum (Shukla et al., 2024) and RF on all 53 features.')
rc = R2['cls']; mc = pd.DataFrame([[k, v['oa'], v['kappa'], v['macro_f1'], v['adj'], v['detection_acc']] + v['fold_mf1'] for k, v in rc.items()], columns=['Model', 'Overall accuracy', 'Kappa', 'Macro-F1', '±1-grade accuracy', 'Healthy vs diseased accuracy', 'Macro-F1 R1', 'Macro-F1 R2', 'Macro-F1 R3']).round(3)
a, b = table(ws, 4, 1, mc, widths=[30, 10, 8, 9, 10, 12, 9, 9, 9])
bar(ws, 'K4', 'Six-grade classification: macro-F1 and ±1-grade accuracy', 'Score', Reference(ws, min_col=1, min_row=a, max_row=b), [Reference(ws, min_col=4, min_row=a - 1, max_row=b), Reference(ws, min_col=5, min_row=a - 1, max_row=b)], w=18, h=9)
rr_ = R2['reg']; mr = pd.DataFrame([[k, v['r2'], v['rmse'], v['nrmse'], v['rpd']] + v['fold_r2'] for k, v in rr_.items()], columns=['Model', 'R²', 'RMSE (PDI %)', 'NRMSE', 'RPD', 'R² R1', 'R² R2', 'R² R3']).round(3)
a2, b2 = table(ws, b + 4, 1, mr)
bar(ws, 'K%d' % (b + 4), 'PDI regression: R²', 'R²', Reference(ws, min_col=1, min_row=a2, max_row=b2), [Reference(ws, min_col=2, min_row=a2 - 1, max_row=b2)], w=18, h=9)

# ===================== 8 Confusion (formulas) =====================
ws = sheet('8_Confusion', 'Objective 2 — confusion matrix of the best classifier (%s) with metric formulas' % R2['best']['cls'], 'Counts (blue) from the held-out predictions; OA, precision, recall, F1, macro-F1, kappa and ±1-grade accuracy are formulas (Cohen, 1960; Sokolova and Lapalme, 2009).')
cm = np.array(rc[R2['best']['cls']]['cm'])
ws.cell(4, 1, 'Observed \\ Predicted').font = HF; ws.cell(4, 1).fill = HFILL
for j, g in enumerate(G6): c = ws.cell(4, 2 + j, g); c.font = HF; c.fill = HFILL; c2 = ws.cell(5 + j, 1, g); c2.font = HF; c2.fill = HFILL
for i in range(6):
    for j in range(6): ws.cell(5 + i, 2 + j, int(cm[i, j])).font = Font(name=FONT, color='0000FF')
ws.conditional_formatting.add('B5:G10', ColorScaleRule(start_type='min', start_color='FFFFFF', end_type='max', end_color='2E7D32'))
for j, h in enumerate(['Row total', 'Recall', 'Precision', 'F1']): c = ws.cell(4, 8 + j, h); c.font = HF; c.fill = HFILL
cols = 'BCDEFG'
for i in range(6):
    rr = 5 + i; dg = '%s%d' % (cols[i], rr)
    ws.cell(rr, 8, '=SUM(B%d:G%d)' % (rr, rr)); ws.cell(rr, 9, '=%s/H%d' % (dg, rr)).number_format = '0.000'
    ws.cell(rr, 10, '=%s/SUM(%s5:%s10)' % (dg, cols[i], cols[i])).number_format = '0.000'
    ws.cell(rr, 11, '=IF(I%d+J%d>0,2*I%d*J%d/(I%d+J%d),0)' % ((rr,) * 6)).number_format = '0.000'
lab = [('N', '=SUM(B5:G10)'), ('Overall accuracy', '=(B5+C6+D7+E8+F9+G10)/B13'), ('Macro-F1', '=AVERAGE(K5:K10)'),
       ('Expected agreement pe', '=SUMPRODUCT(H5:H10,TRANSPOSE(B11:G11))/B13^2'), ('Kappa', '=(B14-B16)/(1-B16)'),
       ('±1-grade accuracy', '=(SUM(B5:C5)+SUM(B6:D6)+SUM(C7:E7)+SUM(D8:F8)+SUM(E9:G9)+SUM(F10:G10))/B13'),
       ('Healthy vs diseased accuracy', '=(B5+SUM(C6:G10))/B13')]
for j in range(6): ws.cell(11, 2 + j, '=SUM(%s5:%s10)' % (cols[j], cols[j]))
ws.cell(11, 1, 'Column total').font = Font(name=FONT, bold=True)
for k, (l, fx) in enumerate(lab):
    ws.cell(13 + k, 1, l).font = Font(name=FONT, bold=True); c = ws.cell(13 + k, 2, fx); c.number_format = '0.000'
ws['B16'] = '=SUMPRODUCT(H5:H10,B11:G11*0+0)'  # placeholder replaced below
ws['B16'] = '=(H5*B11+H6*C11+H7*D11+H8*E11+H9*F11+H10*G11)/B13^2'
ws.column_dimensions['A'].width = 26
bar(ws, 'M4', 'F1 per grade', 'F1', Reference(ws, min_col=1, min_row=5, max_row=10), [Reference(ws, min_col=11, min_row=4, max_row=10)], w=14, h=8)

# ===================== 8 Obs vs pred (formulas) =====================
ws = sheet('8_Obs_vs_pred', 'Objective 2 — plot PDI: observed vs predicted on the held-out replications', 'R² = 1 − SSE/SST, RMSE, NRMSE = RMSE/mean, RPD = SD/RMSE are formulas over the columns (Liu et al., 2024).')
pr = pd.read_csv(D + 'pred_reg.csv'); keepc = ['date', 'plot', 'variety', 'fold', 'observed_PDI'] + [c for c in pr.columns if c.startswith('pred_')]
a, b = table(ws, 4, 1, pr[keepc].round(3))
for j, c in enumerate(keepc[5:]):
    cc = CL(6 + j); rr0 = b + 2
    ws.cell(rr0, 6 + j, '=1-SUMXMY2(E%d:E%d,%s%d:%s%d)/DEVSQ(E%d:E%d)' % (a, b, cc, a, cc, b, a, b)).number_format = '0.000'
    ws.cell(rr0 + 1, 6 + j, '=SQRT(SUMXMY2(E%d:E%d,%s%d:%s%d)/COUNT(E%d:E%d))' % (a, b, cc, a, cc, b, a, b)).number_format = '0.00'
    ws.cell(rr0 + 2, 6 + j, '=%s%d/AVERAGE(E%d:E%d)' % (cc, rr0 + 1, a, b)).number_format = '0.000'
    ws.cell(rr0 + 3, 6 + j, '=STDEVP(E%d:E%d)/%s%d' % (a, b, cc, rr0 + 1)).number_format = '0.00'
for k, l in enumerate(['R²', 'RMSE', 'NRMSE', 'RPD']): ws.cell(b + 2 + k, 5, l).font = Font(name=FONT, bold=True)
best_c = keepc.index('pred_' + R2['best']['reg']) + 1; bu_c = [i + 1 for i, c in enumerate(keepc) if c.startswith('pred_Bottom')][0]
scatter(ws, '%s4' % CL(len(keepc) + 2), 'Observed vs predicted PDI', 'Observed PDI (%)', 'Predicted PDI (%)', Reference(ws, min_col=5, min_row=a, max_row=b),
        [Reference(ws, min_col=best_c, min_row=a, max_row=b), Reference(ws, min_col=bu_c, min_row=a, max_row=b)], [R2['best']['reg'], 'Bottom-up from leaf grades'], lines=False, w=16, h=11, colors=['AD1457', '00695C'])

# ===================== 8 By date / variety =====================
ws = sheet('8_By_date_variety', 'Objective 2 — performance of the best models per date and variety', 'Best classifier: %s; best regressor: %s.' % (R2['best']['cls'], R2['best']['reg']))
bd = pd.DataFrame([[d, v['oa'], v['macro_f1'], v['r2'], v['rmse']] for d, v in R2['by_date'].items()], columns=['Date', 'Overall accuracy', 'Macro-F1', 'R² (PDI)', 'RMSE (PDI)']).round(3)
a, b = table(ws, 4, 1, bd, widths=[12, 12, 10, 10, 10])
bar(ws, 'H4', 'Macro-F1 and R² by date', 'Score', Reference(ws, min_col=1, min_row=a, max_row=b), [Reference(ws, min_col=3, min_row=a - 1, max_row=b), Reference(ws, min_col=4, min_row=a - 1, max_row=b)], w=16, h=8)
bv = pd.DataFrame([[v, q['macro_f1'], q['r2']] for v, q in R2['by_variety'].items()], columns=['Variety', 'Macro-F1', 'R² (PDI)']).round(3)
table(ws, b + 3, 1, bv)

# ===================== References =====================
ws = sheet('References', 'References', 'Methods cited in this workbook.')
refs = json.load(open(D + 'refs_used.json')) if os.path.exists(D + 'refs_used.json') else []
for i, r in enumerate(refs): ws.cell(4 + i, 1, r).font = BF
ws.column_dimensions['A'].width = 160
wb.save(OUT); print('saved', OUT)
