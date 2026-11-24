"""Excel workbook of the 2025-26 ASD leaf analysis: one sheet per step, live formulas where Excel can compute the step,
native (editable) charts, and static tables for the steps computed in Python (machine learning, deep learning)."""
import numpy as np, pandas as pd, os, json
from split_cfg import FOLDS, TAG, LABEL
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as CL
from openpyxl.chart import LineChart, BarChart, ScatterChart, Reference, Series
from openpyxl.formatting.rule import ColorScaleRule
B = os.path.dirname(os.path.abspath(__file__)) + '/'; D = B + 'data/'
OUT = B + '../outputs/ASD_2025-26_80-20_leaf_analysis_white_rust.xlsx'
P = np.load(D + 'prep.npz'); w5, R5, FD5 = P['w5'], P['R5'], P['FD5']
M = pd.read_csv(D + 'meta.csv'); O1 = json.load(open(D + 'o1_results.json')); F = pd.read_csv(D + 'indices_full.csv'); REF = json.load(open(D + 'index_refs.json'))
GR = [0, 1, 3, 5, 7, 9]
AR = 'Arial'; HF = Font(name=AR, bold=True, color='FFFFFF'); HFILL = PatternFill('solid', fgColor='1F3864'); TF = Font(name=AR, bold=True, size=13, color='1F3864'); NF = Font(name=AR, size=10)
NOTEF = Font(name=AR, italic=True, size=9, color='555555'); thin = Side(style='thin', color='BBBBBB')
wb = Workbook(); wb.remove(wb.active)
def sheet(name, title, note=None):
    ws = wb.create_sheet(name); ws['A1'] = title; ws['A1'].font = TF
    if note: ws['A2'] = note; ws['A2'].font = NOTEF
    return ws
def header(ws, r, c, cols):
    for j, h in enumerate(cols):
        cell = ws.cell(r, c + j, h); cell.font = HF; cell.fill = HFILL; cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
def table(ws, r, c, df, fmt=None):
    header(ws, r, c, list(df.columns))
    for i, row in enumerate(df.itertuples(index=False), 1):
        for j, v in enumerate(row):
            v = None if (isinstance(v, float) and np.isnan(v)) else (float(v) if isinstance(v, (np.floating,)) else (int(v) if isinstance(v, np.integer) else v))
            cell = ws.cell(r + i, c + j, v); cell.font = NF
            if fmt and isinstance(v, float): cell.number_format = fmt
    return r + len(df)
def style_chart(ch, title, xt=None, yt=None, w=24, h=11):
    ch.title = title; ch.roundedCorners = False; ch.width = w; ch.height = h
    if ch.legend is not None: ch.legend.overlay = False; ch.legend.position = 'b'
    if hasattr(ch, 'x_axis'):
        ch.x_axis.delete = False; ch.y_axis.delete = False
        if xt: ch.x_axis.title = xt
        if yt: ch.y_axis.title = yt
    return ch
def widths(ws, w=14, first=None):
    for j in range(1, ws.max_column + 1): ws.column_dimensions[CL(j)].width = w
    if first: ws.column_dimensions['A'].width = first

# ------------------------------------------------------------------ 0 Contents
ws = sheet('0_Contents', 'White rust of Indian mustard – ASD leaf spectra 2025-26: step-by-step analysis workbook',
           'Leaf level; 4 dates, 3 growth stages, 3 varieties and leaf positions pooled. Blue cells = data; black = formulas; tables marked "static" were computed in Python (scripts in thesis_build/asd%s). Validation: grouped, stratified %s hold-out of whole plots; comparison with the earlier LORO analysis in sheets 29–33.' % (TAG.replace('-', ''), LABEL))
rows = [('1_Data', 'Common Activity A', 'leaf metadata and smoothed reflectance at 5 nm (400–2400 nm, water bands kept)'),
        ('2_Counts', 'Step A5', 'leaves by date, stage, variety, leaf position, sowing timing and block × grade (COUNTIFS formulas, charts)'),
        ('3_Mean_spectra', 'Step 1.1.1', 'mean reflectance by grade (AVERAGEIFS formulas, line chart)'),
        ('4_First_derivative', 'Step 1.1.1', 'mean first derivative by grade (static, line chart)'),
        ('5_Correlation', 'Step 1.1.2', 'Pearson r of every 5-nm band with leaf grade (CORREL formulas; derivative r static; chart)'),
        ('6_NDSI_RSI', 'Step 1.2.1 / 1.3.1', 'R² maps (20 nm grid with colour scale), best pairs, effective ranges'),
        ('7_SHAP_CARS', 'Steps 1.2.2–1.2.4', 'Shapley importance, PLS components (MCCV), CARS iterations, selection frequency, optimal wavelengths'),
        ('8_WRI', 'Step 1.3.2', 'White Rust Index formula for every leaf (Excel formula), top candidates, mean by grade'),
        ('9_Indices_formulas', 'Step D4 / 1.4.1', 'twelve indices as Excel formulas from the 5-nm data'),
        ('10_Indices_values', 'Step D4', 'all 41 indices, 3 red-edge parameters and 3 data-driven indices (exact 1-nm values, static) with references'),
        ('11_ReliefF', 'Steps 1.4.2–1.4.3', 'redundancy filter and ReliefF / RReliefF weights'),
        ('12_VIF_DSF', 'Step 1.6.2', 'variance inflation factors and the disease-specific feature set'),
        ('13_Fold_selection', 'Step 2.1.2', 'features selected on the %s training plots (and, for comparison, in the three LORO training parts)' % LABEL),
        ('14_ML_SFFS', 'Steps 2.1.4, 2.2', 'features and hyper-parameters chosen by floating forward selection and grid search'),
        ('15_Metrics', 'Activity 2.4', 'metrics of all models and tasks (static) with charts'),
        ('16_Confusion', 'Step 2.4.1', 'confusion matrices with formula-based OA, kappa, recall, precision and F1'),
        ('17_Regression', 'Step 2.4.2', 'observed vs predicted scores with formula-based R², RMSE and RPD; scatter chart'),
        ('18_DL_training', 'Step 2.3.8', 'learning curves and run information of the networks'),
        ('19_DL_config_ablation', 'Steps 2.1.5, 2.5.3', 'feature configurations and DT-EDNet module ablation'),
        ('20_SHAP', 'Step 2.5.4', 'Shapley importance of the best tree model'),
        ('21_Strata', 'Activity 2.6', 'results by stage, variety, leaf position, date and timing'),
        ('22_Transfer', 'Step 2.6.2', 'leave-one-variety-out and leave-one-timing-out tests'),
        ('23_Weather_covariates', 'Step A6', 'daily weather, 7-day summaries and disease progress'),
        ('24_Stability', 'Step 2.5.4', 'optimal wavelengths chosen in the %s training set and the three LORO training parts' % LABEL),
        ('25_Covariate_baseline', 'Step 2.5.5', 'covariates by date, models × inputs, M0/M1/M2 gains (formulas) with plot-block bootstrap intervals, DeLong tests, interpretable model; charts'),
        ('26_References', '—', 'references of the methods'), ('29_Split', 'Steps F1–F3', 'the %s split: test and training plots, leaves, grade and date balance, how the split was chosen' % LABEL), ('30_Cmp_side', 'Comparison', 'every metric of every model: LORO vs %s (vs the other ratio), difference by formula' % LABEL), ('31_Cmp_paired', 'Comparison', 'same test leaves: LORO vs %s with 95%% plot-bootstrap intervals; verdict by formula' % LABEL), ('32_Cmp_repeat', 'Comparison', '20 other %s splits vs LORO (light pipeline); summary by formulas; leakage check with random leaf-level splits' % LABEL), ('33_Split_types', 'Comparison', 'types of train/test split in plant-disease studies with references; train/validation/test explained'), ('27_R_Tables', 'Report', 'every table of the Word report (same numbering)'), ('28_R_Figures', 'Report', 'every figure of the Word report (same numbering)')]
table(ws, 4, 1, pd.DataFrame(rows, columns=['Sheet', 'Methodology step', 'Content']))
ws['A34'] = 'Assumptions and settings'; ws['A34'].font = Font(name=AR, bold=True)
notes = ['Plot plan from the field layout (healthy block plots 1–12; R3 13–24; R2 25–36; R1 37–48; treatment codes D×V) – confirmed by the user.',
         'Natural infection (no artificial inoculation). Sowing D1 9 Dec, D2 18 Dec, D3 27 Dec 2025, D4 9 Jan 2026 = 50, 40, 30, 20 days after sowing (DAS) at the end of January 2026 (user). Column DAS of 1_Data = crop age at sampling.',
         'Leaf positions L3, L5 and LL only; the nine spectra labelled L4 (11 Feb 2026) were removed (user).',
         'Contact-probe spectra, already splice corrected; water-absorption bands kept; 350–399 and 2401–2500 nm trimmed (detector-edge noise).',
         'Savitzky–Golay smoothing (11 nm window, 2nd order); first derivative from the same filter; 5-nm bands for band-level analysis.',
         'Validation: grouped, stratified %s hold-out – whole plots in either the training or the test set (healthy and unsprayed plots split separately; unsprayed test plots from different treatments, spread over replications, varieties and timings; seed 2026); inner folds grouped by plot; uncertainty by a plot bootstrap of the test set.' % LABEL,
         'Deep learning on CPU: Ma et al. (2026) settings (AdamW 6e-4, weight decay 1e-5, cosine annealing, batch 32, label smoothing 0.01, gradient clip 1.2) with maximum 100 epochs, patience 20, seed 42.']
for i, n in enumerate(notes): ws.cell(35 + i, 1, n).font = NF
ws['A43'] = 'Workflow from data collection to discussion (where each step is in this workbook and in the Word report)'; ws['A43'].font = Font(name=AR, bold=True)
WF = [('1', 'Field experiment', '48 plots: healthy (fungicide-sprayed) block + R1–R3 unsprayed; 3 varieties × 4 sowing dates (50, 40, 30, 20 DAS); natural infection', '—', '2.1'),
      ('2', 'Leaf spectra and scoring', 'ASD contact probe on L3, L5, LL leaves of all 48 plots on 11 Feb, 24 Feb, 3 Mar, 13 Mar 2026; 0–9 grade of every leaf', '1_Data, 2_Counts', '2.2'),
      ('3', 'Weather and covariates', 'IARI observatory daily weather; 7-day windows ending the day before each date; favourable days since sowing; crop age (DAS), timing, variety, stage', '23_Weather_covariates, 25_Covariate_baseline', '2.3'),
      ('4', 'Data organisation and QC', 'parse four files, join layout, labels, derived fields, range and missing-value checks, training/test set of each plot', '1_Data, 2_Counts', '2.4'),
      ('5', 'Tasks and validation', 'A detection, B six grades, C score; grouped %s hold-out of whole plots; inner folds by plot' % LABEL, '29_Split, 13_Fold_selection', '2.5–2.6'),
      ('6', 'Pre-processing and features', 'Savitzky–Golay, first derivative, 5-nm bands, 41 indices + red-edge parameters', '3_Mean_spectra, 4_First_derivative, 9_Indices_formulas, 10_Indices_values', '2.7–2.8'),
      ('7', 'Objective 1', 'spectral response, NDSI/RSI maps, SHAP-CARS, WRI, ReliefF, VIF → disease-specific features', '5_Correlation to 12_VIF_DSF', '2.9, 3.1–3.7'),
      ('8', 'Objective 2', 'SFFS + tuned machine learning, deep learning (DT-EDNet and others), metrics', '14_ML_SFFS to 19_DL_config_ablation', '2.10, 3.8–3.10'),
      ('9', 'Covariate baseline', 'models without sensor data vs spectra vs spectra + covariates; gains with bootstrap and DeLong', '25_Covariate_baseline', '2.11, 3.12'),
      ('10', 'Interpretation and robustness', 'SHAP, strata, transfer tests, selection stability', '20_SHAP, 21_Strata, 22_Transfer, 24_Stability', '2.12, 3.11'),
      ('11', 'Comparison with LORO', 'side by side, same test leaves (paired bootstrap), 20 repeated splits, leakage check', '30_Cmp_side to 33_Split_types', '4'), ('12', 'Discussion and conclusions', 'physical basis, grade overlap, ML vs DL, role of covariates, limitations, UAV implications', '—', '5, 6')]
header(ws, 44, 1, ['Step', 'Stage', 'What was done', 'Workbook sheets', 'Word report section'])
for i, r_ in enumerate(WF):
    for j, v in enumerate(r_): c_ = ws.cell(45 + i, 1 + j, v); c_.font = NF; c_.alignment = Alignment(wrap_text=True, vertical='top')
widths(ws, 60, 24); ws.column_dimensions['B'].width = 26; ws.column_dimensions['D'].width = 40; ws.column_dimensions['E'].width = 20

# ------------------------------------------------------------------ 1 Data (5 nm)
ws = sheet('1_Data', 'Leaf metadata and smoothed reflectance (5-nm bands, 400–2400 nm)', 'One row per leaf (n = %d; L3, L5, LL).' % len(M) + ' Reflectance after Savitzky–Golay smoothing. Values in blue are data.')
meta_cols = ['leaf_id', 'date', 'DAS', 'plot', 'block', 'set', 'variety', 'timing', 'stage', 'leaf', 'grade', 'diseased']
Md = M.copy(); Md['leaf_id'] = np.arange(1, len(M) + 1); Md['set'] = np.where(M.fold == 0, 'test', 'train')
hdr = meta_cols + ['R%d' % w for w in w5]; header(ws, 4, 1, hdr)
blue = Font(name=AR, size=9, color='0000FF')
for i in range(len(M)):
    r = 5 + i
    for j, c in enumerate(meta_cols): ws.cell(r, 1 + j, (Md[c].iloc[i].item() if hasattr(Md[c].iloc[i], 'item') else Md[c].iloc[i])).font = blue
    for j in range(len(w5)): ws.cell(r, 1 + len(meta_cols) + j, round(float(R5[i, j]), 5))
ws.freeze_panes = 'M5'; NROW = 4 + len(M); GCOL = CL(meta_cols.index('grade') + 1)
colw = {w: CL(1 + len(meta_cols) + j) for j, w in enumerate(w5)}
def rng(w): return "'1_Data'!$%s$5:$%s$%d" % (colw[w], colw[w], NROW)
GRANGE = "'1_Data'!$%s$5:$%s$%d" % (GCOL, GCOL, NROW)

# ------------------------------------------------------------------ 2 Counts
ws = sheet('2_Counts', 'Leaves by factor and grade (COUNTIFS formulas)', 'Change the data in 1_Data and these counts update.')
r0 = 4
for fac in ['date', 'stage', 'variety', 'leaf', 'timing', 'block']:
    fc = CL(meta_cols.index(fac) + 1); FR = "'1_Data'!$%s$5:$%s$%d" % (fc, fc, NROW); levels = sorted(M[fac].astype(str).unique())
    header(ws, r0, 1, [fac] + ['grade %d' % g for g in GR] + ['total', 'mean grade'])
    for i, lev in enumerate(levels):
        rr = r0 + 1 + i; ws.cell(rr, 1, lev).font = NF
        for j, g in enumerate(GR): ws.cell(rr, 2 + j, '=COUNTIFS(%s,"%s",%s,%d)' % (FR, lev, GRANGE, g))
        ws.cell(rr, 8, '=SUM(B%d:G%d)' % (rr, rr)); ws.cell(rr, 9, '=SUMPRODUCT(B%d:G%d,{0,1,3,5,7,9})/H%d' % (rr, rr, rr)).number_format = '0.00'
    tr = r0 + 1 + len(levels); ws.cell(tr, 1, 'total').font = Font(name=AR, bold=True)
    for j in range(2, 9): ws.cell(tr, j, '=SUM(%s%d:%s%d)' % (CL(j), r0 + 1, CL(j), tr - 1))
    ch = BarChart(); ch.type = 'col'; ch.grouping = 'stacked'; ch.overlap = 100
    ch.add_data(Reference(ws, min_col=2, max_col=7, min_row=r0, max_row=r0 + len(levels)), titles_from_data=True); ch.set_categories(Reference(ws, min_col=1, min_row=r0 + 1, max_row=r0 + len(levels)))
    ws.add_chart(style_chart(ch, 'Leaves by %s and grade' % fac, fac, 'leaves', 14, 7), 'K%d' % r0)
    r0 = tr + 12
widths(ws, 11, 16)

# ------------------------------------------------------------------ 3 Mean spectra (formulas)
ws = sheet('3_Mean_spectra', 'Mean reflectance by grade (AVERAGEIFS on 1_Data)', 'Each cell averages the 5-nm reflectance of all leaves with that grade.')
header(ws, 4, 1, ['wavelength (nm)'] + ['grade %d' % g for g in GR] + ['all leaves'])
for i, w in enumerate(w5):
    r = 5 + i; ws.cell(r, 1, int(w))
    for j, g in enumerate(GR): ws.cell(r, 2 + j, '=AVERAGEIFS(%s,%s,%d)' % (rng(w), GRANGE, g)).number_format = '0.0000'
    ws.cell(r, 8, '=AVERAGE(%s)' % rng(w)).number_format = '0.0000'
ch = LineChart(); ch.add_data(Reference(ws, min_col=2, max_col=7, min_row=4, max_row=4 + len(w5)), titles_from_data=True); ch.set_categories(Reference(ws, min_col=1, min_row=5, max_row=4 + len(w5)))
for s in ch.series: s.smooth = False; s.graphicalProperties.line.width = 15000
ch.x_axis.tickLblSkip = 40; ws.add_chart(style_chart(ch, 'Mean leaf reflectance by severity grade', 'wavelength (nm)', 'reflectance'), 'J4'); widths(ws, 11)

# ------------------------------------------------------------------ 4 First derivative (static)
fs = pd.read_csv(D + 'o1_mean_fd.csv'); ws = sheet('4_First_derivative', 'Mean first derivative by grade (×10⁻³ nm⁻¹; static, Python)')
fs.columns = ['wavelength (nm)'] + ['grade %d' % g for g in GR]; table(ws, 4, 1, fs, '0.000')
ch = LineChart(); ch.add_data(Reference(ws, min_col=2, max_col=7, min_row=4, max_row=4 + len(fs)), titles_from_data=True); ch.set_categories(Reference(ws, min_col=1, min_row=5, max_row=4 + len(fs)))
for s in ch.series: s.smooth = False
ch.x_axis.tickLblSkip = 40; ws.add_chart(style_chart(ch, 'First derivative of the mean spectra', 'wavelength (nm)', 'first derivative (×10⁻³ nm⁻¹)'), 'J4'); widths(ws, 11)

# ------------------------------------------------------------------ 5 Correlation
cc = pd.read_csv(D + 'o1_corr_curves.csv'); ws = sheet('5_Correlation', 'Correlation of each band with the leaf grade', 'Column B: CORREL formula on 1_Data (reflectance). Column C: first-derivative r (static).')
header(ws, 4, 1, ['wavelength (nm)', 'r reflectance (formula)', 'r first derivative (static)'])
for i, w in enumerate(w5):
    r = 5 + i; ws.cell(r, 1, int(w)); ws.cell(r, 2, '=CORREL(%s,%s)' % (rng(w), GRANGE)).number_format = '0.000'; ws.cell(r, 3, round(float(cc.r_FD.iloc[i]), 4))
ch = LineChart(); ch.add_data(Reference(ws, min_col=2, max_col=3, min_row=4, max_row=4 + len(w5)), titles_from_data=True); ch.set_categories(Reference(ws, min_col=1, min_row=5, max_row=4 + len(w5)))
ch.x_axis.tickLblSkip = 40; ws.add_chart(style_chart(ch, 'Correlation curves with leaf grade', 'wavelength (nm)', 'Pearson r'), 'E4'); widths(ws, 16)

# ------------------------------------------------------------------ 6 NDSI / RSI
Nm = np.load(D + 'o1_ndsi_r2.npy'); Sm = np.load(D + 'o1_rsi_r2.npy'); ws = sheet('6_NDSI_RSI', 'NDSI and RSI R² with leaf grade (all 80 200 band pairs at 5 nm; shown on a 20-nm grid)',
    'Best pairs and effective ranges computed in Python. Grid: rows λ₂, columns λ₁ (upper triangle filled symmetrically). Colour scale is editable (conditional formatting).')
info = pd.DataFrame([('best NDSI (nm)', '%d, %d' % tuple(O1['best_ndsi'][:2]), O1['best_ndsi'][2]), ('best RSI (nm)', '%d, %d' % tuple(O1['best_rsi'][:2]), O1['best_rsi'][2]),
                     ('effective-range threshold R²', 'top 5% of pairs (no pair reached 0.5)', O1['eff_thr']), ('bands in effective ranges', str(O1['eff_nbands']) + ' of 401', None)], columns=['item', 'value', 'R²'])
table(ws, 4, 1, info, '0.000')
ws.cell(10, 1, 'Effective ranges (nm)').font = Font(name=AR, bold=True); ws.cell(11, 1, '; '.join('%d–%d' % tuple(x) for x in O1['eff_ranges'])).font = NF
step = 4; gw = w5[::step]; Nf = np.fmax(Nm, Nm.T); Sf = np.fmax(Sm, Sm.T)
for title, A, r0 in (('NDSI R²', Nf, 14), ('RSI R²', Sf, 14 + len(gw) + 4)):
    ws.cell(r0 - 1, 1, title).font = Font(name=AR, bold=True)
    for j, w in enumerate(gw): ws.cell(r0, 2 + j, int(w)).font = Font(name=AR, bold=True, size=8)
    for i, w in enumerate(gw):
        ws.cell(r0 + 1 + i, 1, int(w)).font = Font(name=AR, bold=True, size=8)
        for j in range(len(gw)):
            v = A[i * step, j * step]; ws.cell(r0 + 1 + i, 2 + j, None if not np.isfinite(v) else round(float(v), 3)).font = Font(name=AR, size=7)
    ws.conditional_formatting.add('%s%d:%s%d' % (CL(2), r0 + 1, CL(1 + len(gw)), r0 + len(gw)), ColorScaleRule(start_type='num', start_value=0, start_color='313695', mid_type='percentile', mid_value=50, mid_color='FFFFBF', end_type='max', end_color='A50026'))
for j in range(2, 2 + len(gw)): ws.column_dimensions[CL(j)].width = 4.5
ws.column_dimensions['A'].width = 28; ws.column_dimensions['B'].width = 6

# ------------------------------------------------------------------ 7 SHAP-CARS
ws = sheet('7_SHAP_CARS', 'SHAP-CARS optimal wavelengths (Steps 1.2.2–1.2.4; static, Python)', 'Reflectance (R) and first derivative (FD) pooled; bands standardised before CARS; red-edge FD 680–760 nm always candidates; 20 CARS runs × 50 iterations; kept if selected in ≥ 50% of runs.')
sc = pd.read_csv(D + 'o1_shapcars.csv').sort_values('cars_freq', ascending=False); mc = pd.read_csv(D + 'o1_mccv.csv'); chh = pd.read_csv(D + 'o1_cars_hist.csv')
e = table(ws, 4, 1, sc.head(40).rename(columns={'feature': 'band (R/FD + nm)', 'mean_abs_shap': 'mean |SHAP|', 'cars_freq': 'CARS frequency'}), '0.000')
ch = BarChart(); ch.add_data(Reference(ws, min_col=3, min_row=4, max_row=4 + min(40, len(sc))), titles_from_data=True); ch.set_categories(Reference(ws, min_col=1, min_row=5, max_row=4 + min(40, len(sc))))
ws.add_chart(style_chart(ch, 'CARS selection frequency (20 runs)', 'band', 'frequency', 20, 9), 'F4')
table(ws, 4, 30, mc.rename(columns={'ncomp': 'PLS components', 'rmse': 'RMSE (MCCV)'}), '0.000')
ch = LineChart(); ch.add_data(Reference(ws, min_col=31, min_row=4, max_row=4 + len(mc)), titles_from_data=True); ch.set_categories(Reference(ws, min_col=30, min_row=5, max_row=4 + len(mc)))
ws.add_chart(style_chart(ch, 'Choice of PLS components', 'components', 'RMSE', 14, 8), 'F24')
table(ws, 4, 34, chh.rename(columns={'iteration': 'CARS iteration', 'n_vars': 'variables kept', 'rmsecv': 'RMSECV'}), '0.000')
ch = LineChart(); ch.add_data(Reference(ws, min_col=36, min_row=4, max_row=4 + len(chh)), titles_from_data=True); ch.set_categories(Reference(ws, min_col=34, min_row=5, max_row=4 + len(chh)))
ws.add_chart(style_chart(ch, 'CARS run 1: RMSECV by iteration', 'iteration', 'RMSECV', 14, 8), 'F41')
ws.cell(46, 1, 'Optimal wavelengths (OW)').font = Font(name=AR, bold=True); ws.cell(47, 1, ', '.join(O1['OW'])).font = NF
ws.cell(48, 1, 'Reflectance bands: %d; first-derivative bands: %d; PLS components: %d' % (O1['OW_n_R'], O1['OW_n_FD'], O1['cars_ncomp'])).font = NF
widths(ws, 13, 18)

# ------------------------------------------------------------------ 8 WRI (formula per leaf)
W = O1['WRI']; ws = sheet('8_WRI', 'White Rust Index = NDSI(λ₁, λ₂) + w × R(λ₃) (Step 1.3.2)', 'Edit λ₁, λ₂, λ₃ (5-nm steps) and w in the yellow cells: the index of every leaf and the summary update.')
yl = PatternFill('solid', fgColor='FFFF00')
for i, (k, v) in enumerate((('λ1 (nm)', W['l1']), ('λ2 (nm)', W['l2']), ('w', W['w']), ('λ3 (nm)', W['l3']))):
    ws.cell(4 + i, 1, k).font = Font(name=AR, bold=True); c = ws.cell(4 + i, 2, v); c.fill = yl; c.font = Font(name=AR, color='0000FF')
ws.cell(9, 1, 'r with grade').font = Font(name=AR, bold=True)
datarow0 = 14; header(ws, datarow0, 1, ['leaf_id', 'grade', 'WRI'])
first_band_col = 1 + len(meta_cols)
def colexpr(cellref): return "INDEX('1_Data'!$%s$5:$%s$%d,ROW()-%d,MATCH(%s,'1_Data'!$%s$4:$%s$4,0))" % (CL(first_band_col), CL(first_band_col + len(w5) - 1), NROW, datarow0, '"R"&' + cellref, CL(first_band_col), CL(first_band_col + len(w5) - 1))
for i in range(len(M)):
    r = datarow0 + 1 + i; ws.cell(r, 1, "='1_Data'!A%d" % (5 + i)); ws.cell(r, 2, "='1_Data'!%s%d" % (GCOL, 5 + i))
    a = colexpr('$B$4'); b = colexpr('$B$5'); c3 = colexpr('$B$7')
    ws.cell(r, 3, '=(%s-%s)/(%s+%s)+$B$6*%s' % (a, b, a, b, c3)).number_format = '0.0000'
last = datarow0 + len(M); ws['B9'] = '=CORREL(C%d:C%d,B%d:B%d)' % (datarow0 + 1, last, datarow0 + 1, last); ws['B9'].number_format = '0.000'
header(ws, 4, 5, ['grade', 'mean WRI', 'n'])
for i, g in enumerate(GR):
    ws.cell(5 + i, 5, g); ws.cell(5 + i, 6, '=AVERAGEIFS($C$%d:$C$%d,$B$%d:$B$%d,%d)' % (datarow0 + 1, last, datarow0 + 1, last, g)).number_format = '0.0000'; ws.cell(5 + i, 7, '=COUNTIF($B$%d:$B$%d,%d)' % (datarow0 + 1, last, g))
ch = BarChart(); ch.add_data(Reference(ws, min_col=6, min_row=4, max_row=10), titles_from_data=True); ch.set_categories(Reference(ws, min_col=5, min_row=5, max_row=10)); ws.add_chart(style_chart(ch, 'Mean WRI by grade', 'grade', 'WRI', 12, 7), 'I4')
top = pd.read_csv(D + 'o1_wri_top.csv').head(15); table(ws, 20, 9, top, '0.000'); widths(ws, 12)

# ------------------------------------------------------------------ 9 Indices as formulas
ws = sheet('9_Indices_formulas', 'Twelve indices computed with Excel formulas from the 5-nm data (nearest band)', 'Exact 1-nm values used in the analysis are in 10_Indices_values; small differences come from the 5-nm rounding.')
IDX = [('NDVI', lambda c: '(%s-%s)/(%s+%s)' % (c(800), c(670), c(800), c(670))), ('GNDVI', lambda c: '(%s-%s)/(%s+%s)' % (c(850), c(550), c(850), c(550))),
       ('NDRE', lambda c: '(%s-%s)/(%s+%s)' % (c(790), c(720), c(790), c(720))), ('CIrededge', lambda c: '%s/%s-1' % (c(790), c(720))), ('CIgreen', lambda c: '%s/%s-1' % (c(790), c(550))),
       ('PSSRb', lambda c: '%s/%s' % (c(800), c(635))), ('PSRI', lambda c: '(%s-%s)/%s' % (c(680), c(500), c(750))), ('ARI', lambda c: '1/%s-1/%s' % (c(550), c(700))),
       ('PRI', lambda c: '(%s-%s)/(%s+%s)' % (c(530), c(570), c(530), c(570))), ('NDWI', lambda c: '(%s-%s)/(%s+%s)' % (c(860), c(1240), c(860), c(1240))),
       ('MoistSI', lambda c: '%s/%s' % (c(1600), c(820))), ('DWSI-5', lambda c: '(%s+%s)/(%s+%s)' % (c(800), c(550), c(1660), c(680)))]
header(ws, 4, 1, ['leaf_id', 'grade'] + [n for n, _ in IDX])
for i in range(len(M)):
    r = 5 + i; src = 5 + i; ws.cell(r, 1, "='1_Data'!A%d" % src); ws.cell(r, 2, "='1_Data'!%s%d" % (GCOL, src))
    c = lambda w: "'1_Data'!%s%d" % (colw[w], src)
    for j, (n, fn) in enumerate(IDX): ws.cell(r, 3 + j, '=' + fn(c)).number_format = '0.0000'
widths(ws, 11)

# ------------------------------------------------------------------ 10 Indices values
ws = sheet('10_Indices_values', 'All indices and red-edge parameters (exact 1-nm values; static)')
iv = F.copy(); iv.insert(0, 'grade', M.grade); iv.insert(0, 'leaf_id', np.arange(1, len(M) + 1)); table(ws, 5, 1, iv.round(5))
for j, c in enumerate(iv.columns[2:]): ws.cell(4, 3 + j, REF.get(c, 'this study')).font = Font(name=AR, size=7, italic=True)
widths(ws, 11)

# ------------------------------------------------------------------ 11 ReliefF
rl = pd.read_csv(D + 'o1_relief.csv'); ws = sheet('11_ReliefF', 'Index selection: |r| ≥ 0.95 filter, then ReliefF (classes, detection) and RReliefF (score)', 'k = 10 nearest neighbours; neighbours from the same plot excluded. Top five kept for each task.')
table(ws, 4, 1, rl.round(4))
for k, col in enumerate(['ReliefF_binary', 'ReliefF_classes', 'RReliefF_score']):
    ch = BarChart(); ch.type = 'bar'; ch.add_data(Reference(ws, min_col=2 + ['ReliefF_classes', 'ReliefF_binary', 'RReliefF_score'].index(col), min_row=4, max_row=4 + len(rl)), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=1, min_row=5, max_row=4 + len(rl))); ws.add_chart(style_chart(ch, col.replace('_', ' '), None, 'weight', 12, 10), '%s4' % CL(8 + k * 8))
ws.cell(6 + len(rl), 1, 'Selected (top 5): detection %s; six classes %s; score %s' % (', '.join(O1['VI_binary']), ', '.join(O1['VI_classes']), ', '.join(O1['VI_score']))).font = NF
widths(ws, 14)

# ------------------------------------------------------------------ 12 VIF
ws = sheet('12_VIF_DSF', 'Variance inflation factor across groups and the disease-specific feature set (DSF)', 'Pool = optimal wavelengths + selected indices; the feature with the largest VIF removed until all VIF < 10.')
table(ws, 4, 1, pd.DataFrame(list(O1['VIF_final'].items()), columns=['feature in DSF', 'VIF']), '0.00')
table(ws, 4, 4, pd.DataFrame(O1['VIF_removed'], columns=['removed feature', 'VIF at removal']), '0.0')
ch = BarChart(); ch.type = 'bar'; ch.add_data(Reference(ws, min_col=2, min_row=4, max_row=4 + len(O1['VIF_final'])), titles_from_data=True); ch.set_categories(Reference(ws, min_col=1, min_row=5, max_row=4 + len(O1['VIF_final'])))
ws.add_chart(style_chart(ch, 'VIF of the disease-specific feature set', None, 'VIF', 14, 8), 'H4'); widths(ws, 18)

# ------------------------------------------------------------------ 13 Fold selection
SEL = json.load(open(D + 'fold_selection.json')); ws = sheet('13_Fold_selection', 'Feature selection on the %s training plots (first row; no test data used) and in the three LORO training parts (earlier analysis, for comparison)' % LABEL)
fr = []
for f in FOLDS:
    s = SEL[str(f)]; fr.append(dict(training_set=LABEL + ' training plots', effective_threshold=s['eff_thr'], bands_in_ranges=s['eff_n'], OW=', '.join(s['OW']), best_NDSI='%d, %d' % tuple(s['ndsi']), best_RSI='%d, %d' % tuple(s['rsi']),
                                     WRI='NDSI(%d,%d) %+g R%d' % (s['wri']['l1'], s['wri']['l2'], s['wri']['w'], s['wri']['l3']), VI_A=', '.join(s['VI']['A']), VI_B=', '.join(s['VI']['B']), VI_C=', '.join(s['VI']['C']),
                                     DSF_A=', '.join(s['DSF']['A']), DSF_B=', '.join(s['DSF']['B']), DSF_C=', '.join(s['DSF']['C'])))
LSEL_ = json.load(open(D + '../../asd26/data/fold_selection.json')) if os.path.exists(D + '../../asd26/data/fold_selection.json') else {}
for f_ in sorted(LSEL_):
    s = LSEL_[f_]; fr.append(dict(training_set='LORO fold %d (earlier)' % (int(f_) + 1), effective_threshold=s['eff_thr'], bands_in_ranges=s['eff_n'], OW=', '.join(s['OW']), best_NDSI='%d, %d' % tuple(s['ndsi']), best_RSI='%d, %d' % tuple(s['rsi']),
                                     WRI='NDSI(%d,%d) %+g R%d' % (s['wri']['l1'], s['wri']['l2'], s['wri']['w'], s['wri']['l3']), VI_A=', '.join(s['VI']['A']), VI_B=', '.join(s['VI']['B']), VI_C=', '.join(s['VI']['C']),
                                     DSF_A=', '.join(s['DSF']['A']), DSF_B=', '.join(s['DSF']['B']), DSF_C=', '.join(s['DSF']['C'])))
table(ws, 4, 1, pd.DataFrame(fr), '0.000'); widths(ws, 30, 8)

# ------------------------------------------------------------------ 14 ML SFFS
mls = pd.read_csv(D + 'ml_selection.csv'); ws = sheet('14_ML_SFFS', 'Sequential floating forward selection and grid search (inner grouped folds)')
mls['selected'] = mls.selected.map(lambda s: ', '.join(eval(s))); mls = mls.drop(columns='fold'); table(ws, 4, 1, mls, '0.000'); widths(ws, 16); ws.column_dimensions['E'].width = 70; ws.column_dimensions['F'].width = 50

# ------------------------------------------------------------------ 15 Metrics
MT = pd.read_csv(D + 'metrics_all.csv'); ws = sheet('15_Metrics', 'Test metrics of all models on the test plots of the %s split (static; _sd = plot-bootstrap SE, _lo/_hi = 95%% interval)' % LABEL)
r = 4
for t, cols, ttl in (('A', ['model', 'OA', 'kappa', 'sensitivity', 'specificity', 'balanced_acc', 'F1', 'macro_F1', 'macro_F1_sd', 'AUC'], 'Task A – detection (grade 0 vs > 0)'),
                     ('B', ['model', 'OA', 'kappa', 'QWK', 'macro_P', 'macro_R', 'macro_F1', 'macro_F1_sd', 'within1'] + ['F1_g%d' % g for g in GR], 'Task B – six severity classes'),
                     ('C', ['model', 'R2', 'RMSE', 'RMSE_sd', 'MAE', 'RPD', 'bias', 'r'], 'Task C – severity score (regression)')):
    ws.cell(r, 1, ttl).font = Font(name=AR, bold=True, color='1F3864'); d = MT[MT.task == t][[c for c in cols if c in MT.columns]]
    e = table(ws, r + 1, 1, d, '0.000')
    ch = BarChart(); key = 'macro_F1' if t != 'C' else 'RMSE'; kc = list(d.columns).index(key) + 1
    ch.add_data(Reference(ws, min_col=kc, min_row=r + 1, max_row=e), titles_from_data=True); ch.set_categories(Reference(ws, min_col=1, min_row=r + 2, max_row=e))
    ws.add_chart(style_chart(ch, ttl + ': ' + key, None, key, 16, 7), '%s%d' % (CL(len(d.columns) + 3), r)); r = e + 14
widths(ws, 12, 18)

# ------------------------------------------------------------------ 16 Confusion (formulas)
cms = np.load(D + 'confusion.npy', allow_pickle=True).item(); best = json.load(open(D + 'best_models.json'))
ws = sheet('16_Confusion', 'Confusion matrices with formula-based metrics', 'Rows = observed grade, columns = predicted grade. Edit counts to see the metrics change.')
r = 4
for t, src in (('B', 'ML'), ('B', 'DL'), ('A', 'ML'), ('A', 'DL')):
    mname = best[t][src]; key = '%s|%s' % (t, mname)
    if mname is None or key not in cms: continue
    cm = cms[key]; K = cm.shape[0]; labs = GR if K == 6 else ['healthy', 'diseased']
    ws.cell(r, 1, 'Task %s – %s (%s)' % (t, mname, src)).font = Font(name=AR, bold=True, color='1F3864')
    header(ws, r + 1, 1, ['observed \\ predicted'] + [str(l) for l in labs] + ['total', 'recall'])
    for i in range(K):
        rr = r + 2 + i; ws.cell(rr, 1, str(labs[i])).font = Font(name=AR, bold=True)
        for j in range(K): ws.cell(rr, 2 + j, int(cm[i, j])).font = Font(name=AR, color='0000FF')
        ws.cell(rr, 2 + K, '=SUM(%s%d:%s%d)' % (CL(2), rr, CL(1 + K), rr)); ws.cell(rr, 3 + K, '=%s%d/%s%d' % (CL(2 + i), rr, CL(2 + K), rr)).number_format = '0.000'
    tr = r + 2 + K; ws.cell(tr, 1, 'total').font = Font(name=AR, bold=True)
    for j in range(K + 1): ws.cell(tr, 2 + j, '=SUM(%s%d:%s%d)' % (CL(2 + j), r + 2, CL(2 + j), tr - 1))
    pr = tr + 1; ws.cell(pr, 1, 'precision').font = Font(name=AR, bold=True)
    for j in range(K): ws.cell(pr, 2 + j, '=IFERROR(%s%d/%s%d,0)' % (CL(2 + j), r + 2 + j, CL(2 + j), tr)).number_format = '0.000'
    f1 = pr + 1; ws.cell(f1, 1, 'F1').font = Font(name=AR, bold=True)
    for j in range(K): ws.cell(f1, 2 + j, '=IFERROR(2*%s%d*%s%d/(%s%d+%s%d),0)' % (CL(2 + j), pr, CL(3 + K), r + 2 + j, CL(2 + j), pr, CL(3 + K), r + 2 + j)).number_format = '0.000'
    diag = '+'.join('%s%d' % (CL(2 + i), r + 2 + i) for i in range(K)); N = '%s%d' % (CL(2 + K), tr)
    pe = '+'.join('%s%d*%s%d' % (CL(2 + K), r + 2 + i, CL(2 + i), tr) for i in range(K))
    sm = f1 + 1
    for lab, fml in (('overall accuracy', '=(%s)/%s' % (diag, N)), ('chance agreement pe', '=(%s)/%s^2' % (pe, N)), ('kappa', '=(B%d-B%d)/(1-B%d)' % (sm, sm + 1, sm + 1)), ('macro-F1', '=AVERAGE(B%d:%s%d)' % (f1, CL(1 + K), f1))):
        ws.cell(sm, 1, lab).font = Font(name=AR, bold=True); ws.cell(sm, 2, fml).number_format = '0.000'; sm += 1
    r = sm + 2
widths(ws, 12, 22)

# ------------------------------------------------------------------ 17 Regression (formulas)
allp = pd.read_csv(D + 'all_predictions.csv'); ws = sheet('17_Regression', 'Observed and predicted severity score (Task C) with formula-based metrics')
c0 = 1
for src in ('ML', 'DL'):
    mname = best['C'][src]
    if mname is None: continue
    d = allp[(allp.task == 'C') & (allp.model == mname)].sort_values('leaf')
    ws.cell(4, c0, '%s (%s)' % (mname, src)).font = Font(name=AR, bold=True, color='1F3864'); header(ws, 5, c0, ['leaf_id', 'observed', 'predicted'])
    for i, rr in enumerate(d.itertuples()):
        ws.cell(6 + i, c0, int(rr.leaf) + 1); ws.cell(6 + i, c0 + 1, float(rr.y)).font = Font(name=AR, color='0000FF'); ws.cell(6 + i, c0 + 2, round(float(rr.pred), 3)).font = Font(name=AR, color='0000FF')
    last = 5 + len(d); O = '%s6:%s%d' % (CL(c0 + 1), CL(c0 + 1), last); Pp = '%s6:%s%d' % (CL(c0 + 2), CL(c0 + 2), last)
    for k, (lab, fml) in enumerate((('R²', '=1-SUMXMY2(%s,%s)/DEVSQ(%s)' % (O, Pp, O)), ('RMSE', '=SQRT(SUMXMY2(%s,%s)/COUNT(%s))' % (O, Pp, O)), ('RPD', '=STDEV(%s)/%s%d' % (O, CL(c0 + 5), 7)), ('bias', '=AVERAGE(%s)-AVERAGE(%s)' % (Pp, O)), ('r', '=CORREL(%s,%s)' % (O, Pp)))):
        ws.cell(6 + k, c0 + 4, lab).font = Font(name=AR, bold=True); ws.cell(6 + k, c0 + 5, fml).number_format = '0.000'
    ch = ScatterChart(); ch.style = 13; s = Series(Reference(ws, min_col=c0 + 2, min_row=6, max_row=last), Reference(ws, min_col=c0 + 1, min_row=6, max_row=last), title='leaves')
    s.marker.symbol = 'circle'; s.marker.size = 3; s.graphicalProperties.line.noFill = True; ch.series.append(s)
    ws.add_chart(style_chart(ch, 'Predicted vs observed – %s' % mname, 'observed grade', 'predicted score', 14, 9), '%s12' % CL(c0 + 4)); c0 += 12
widths(ws, 12)

# ------------------------------------------------------------------ 18 DL training
ws = sheet('18_DL_training', 'Deep-learning runs: learning curves (six classes; early stopping on one third of the training plots) and run information')
if os.path.exists(D + 'dl_main.json'):
    R = json.load(open(D + 'dl_main.json')); c0 = 1
    for net in ['DT-EDNet', 'EfficientNet-B0', 'ResNet18', 'ConvNeXt V2-Atto', 'DNN-F1']:
        rr = [x for x in R if x['net'] == net and x['task'] == 'B' and x['fold'] == 0]
        if not rr: continue
        h = pd.DataFrame(rr[0]['hist'], columns=['epoch', 'training loss', 'validation loss', 'validation macro-F1'])
        ws.cell(4, c0, net).font = Font(name=AR, bold=True, color='1F3864'); e = table(ws, 5, c0, h, '0.000')
        ch = LineChart(); ch.add_data(Reference(ws, min_col=c0 + 1, max_col=c0 + 3, min_row=5, max_row=e), titles_from_data=True); ch.set_categories(Reference(ws, min_col=c0, min_row=6, max_row=e))
        ws.add_chart(style_chart(ch, net + ' learning curve', 'epoch', 'loss / macro-F1', 12, 7), '%s%d' % (CL(c0), 110)); c0 += 6
    if os.path.exists(D + 'dl_runs.csv'): ws.cell(4, c0 + 1, 'Run information').font = Font(name=AR, bold=True); table(ws, 5, c0 + 1, pd.read_csv(D + 'dl_runs.csv'), '0.000')
widths(ws, 11)

# ------------------------------------------------------------------ 19 DL config + ablation
ws = sheet('19_DL_config_ablation', 'Network comparison on feature configurations and DT-EDNet module ablation (six classes)')
r = 4
for fn, ttl in (('dl_summary_config.csv', 'Configurations (OW = optimal wavelengths, VI = indices, DSF = OW + VI after VIF)'), ('dl_summary_ablation.csv', 'DT-EDNet ablation')):
    if os.path.exists(D + fn):
        d = pd.read_csv(D + fn); ws.cell(r, 1, ttl).font = Font(name=AR, bold=True, color='1F3864'); e = table(ws, r + 1, 1, d, '0.000')
        ch = BarChart(); ch.add_data(Reference(ws, min_col=list(d.columns).index('macro_F1') + 1, min_row=r + 1, max_row=e), titles_from_data=True); ch.set_categories(Reference(ws, min_col=1, max_col=2, min_row=r + 2, max_row=e))
        ws.add_chart(style_chart(ch, ttl, None, 'macro-F1', 16, 8), '%s%d' % (CL(len(d.columns) + 3), r)); r = e + 18
widths(ws, 16)

# ------------------------------------------------------------------ 20 SHAP
ws = sheet('20_SHAP', 'Shapley additive explanations of XGBoost on the disease-specific feature set')
if os.path.exists(D + 'shap_C.npy'):
    sv = np.load(D + 'shap_C.npy'); X = pd.read_csv(D + 'shap_X.csv'); imp = pd.DataFrame({'feature': X.columns, 'mean |SHAP| score model': np.abs(sv).mean(0)}).sort_values('mean |SHAP| score model', ascending=False)
    e = table(ws, 4, 1, imp, '0.0000'); ch = BarChart(); ch.type = 'bar'; ch.add_data(Reference(ws, min_col=2, min_row=4, max_row=e), titles_from_data=True); ch.set_categories(Reference(ws, min_col=1, min_row=5, max_row=e))
    ws.add_chart(style_chart(ch, 'SHAP importance – severity score', None, 'mean |SHAP|', 14, 8), 'E4')
    ib = pd.read_csv(D + 'shap_B_importance.csv'); ib.columns = ['feature'] + ['grade %s' % g for g in GR][:len(ib.columns) - 1]; table(ws, 22, 1, ib, '0.0000')
widths(ws, 14)

# ------------------------------------------------------------------ 21-25 tables with charts
for name, fn, ttl, key in (('21_Strata', 'strata_metrics.csv', 'Results by stratum (best ML and best DL model; test leaves of the %s split)' % LABEL, None),
                           ('22_Transfer', 'transfer_tests.csv', 'Leave-one-variety-out and leave-one-timing-out (random forest; selection repeated in each training set)', None),
                           ('24_Stability', 'selection_stability.csv', 'Selection frequency: %s training set + three LORO training parts (folds = number of the 4 training sets; in_split = chosen in the %s training set); SFFS rows = chosen by each model' % (LABEL, LABEL), None)):
    ws = sheet(name, ttl)
    if os.path.exists(D + fn):
        d = pd.read_csv(D + fn); e = table(ws, 4, 1, d, '0.000')
        if key: ch = BarChart(); ch.add_data(Reference(ws, min_col=list(d.columns).index(key) + 1, min_row=4, max_row=e), titles_from_data=True); ch.set_categories(Reference(ws, min_col=list(d.columns).index('model') + 1, min_row=5, max_row=e)); ws.add_chart(style_chart(ch, ttl[:60], None, key, 14, 8), '%s4' % CL(len(d.columns) + 3))
    widths(ws, 14)
ws = wb['22_Transfer'] if '22_Transfer' in wb.sheetnames else None

# ------------------------------------------------------------------ 23 Weather and covariates
ws = sheet('23_Weather_covariates', 'Weather (IARI observatory), 7-day summaries and disease progress', 'The covariate baseline model (Step 2.5.5) is in sheet 25_Covariate_baseline.')
if os.path.exists(D + 'weather_season.csv'):
    Wd = pd.read_csv(D + 'weather_season.csv')[['date', 'Tmax', 'Tmin', 'rain', 'RH1', 'RH2', 'wind', 'BSS', 'evap']]; Wd['date'] = Wd.date.str[:10]
    e = table(ws, 4, 1, Wd, '0.0'); ch = LineChart(); ch.add_data(Reference(ws, min_col=2, max_col=3, min_row=4, max_row=e), titles_from_data=True); ch.set_categories(Reference(ws, min_col=1, min_row=5, max_row=e)); ch.x_axis.tickLblSkip = 14
    ws.add_chart(style_chart(ch, 'Daily maximum and minimum temperature', 'date', '°C', 18, 8), 'L4')
    ch = LineChart(); ch.add_data(Reference(ws, min_col=5, max_col=6, min_row=4, max_row=e), titles_from_data=True); ch.set_categories(Reference(ws, min_col=1, min_row=5, max_row=e)); ch.x_axis.tickLblSkip = 14
    ws.add_chart(style_chart(ch, 'Morning and afternoon relative humidity', 'date', '%', 18, 8), 'L22')
    wc = pd.read_csv(D + 'weather_covariates.csv'); ws.cell(4, 22, '7-day weather before each sampling date').font = Font(name=AR, bold=True); e2 = table(ws, 5, 22, wc, '0.00')
    ws.cell(e2 + 2, 22, 'Disease progress (formulas on 1_Data)').font = Font(name=AR, bold=True); header(ws, e2 + 3, 22, ['date', 'leaves', 'mean grade', '% diseased leaves'])
    DC = CL(meta_cols.index('date') + 1); DR = "'1_Data'!$%s$5:$%s$%d" % (DC, DC, NROW); DSR = "'1_Data'!$%s$5:$%s$%d" % (CL(meta_cols.index('diseased') + 1), CL(meta_cols.index('diseased') + 1), NROW)
    for i, dt in enumerate(sorted(M.date.unique())):
        rr = e2 + 4 + i; ws.cell(rr, 22, dt); ws.cell(rr, 23, '=COUNTIF(%s,V%d)' % (DR, rr)); ws.cell(rr, 24, '=AVERAGEIFS(%s,%s,V%d)' % (GRANGE, DR, rr)).number_format = '0.00'; ws.cell(rr, 25, '=AVERAGEIFS(%s,%s,V%d)' % (DSR, DR, rr)).number_format = '0.0%'
    ws.cell(e2 + 10, 22, 'Covariate baseline (Step 2.5.5): see sheet 25_Covariate_baseline').font = Font(name=AR, bold=True)
widths(ws, 11)

# ------------------------------------------------------------------ 26 Covariate baseline
if os.path.exists(D + 'cov2_metrics.csv'):
    ws = sheet('25_Covariate_baseline', 'Covariate baseline model without sensor data (Step 2.5.5) – unsprayed, naturally infected leaves only',
               'Static values were computed in Python (a11_covariate.py); black cells are Excel formulas. Weather windows end the day before each date (no look-ahead). Favourable days after Chattopadhyay et al. (2011).')
    BF = Font(name=AR, bold=True, size=11, color='1F3864')
    # 1. covariates by date
    cx = pd.read_csv(D + 'cov2_covariates_by_date.csv'); cx.insert(1, 'DAS (range)', ['%d–%d' % (M[M.date == d].DAS.min(), M[M.date == d].DAS.max()) for d in cx.date])
    cx.columns = ['date', 'DAS (range)', 'Tmax 7 d (°C)', 'Tmin 7 d (°C)', 'RH I 7 d (%)', 'RH II 7 d (%)', 'rain 7 d (mm)', 'favourable leaf days in 7 d', 'fav. leaf days since sowing D1', 'D2', 'D3', 'D4', 'staghead days since sowing']
    ws.cell(4, 1, '1. Weather covariates of the four sampling dates').font = BF; e = table(ws, 5, 1, cx, '0.0')
    # 2. metrics: models x inputs
    mt = pd.read_csv(D + 'cov2_metrics.csv'); KEYS = ['macro_F1', 'AUC', 'balanced_acc', 'QWK', 'R2', 'RMSE', 'fold_sd']
    r0 = e + 3; ws.cell(r0 - 1, 1, '2. Test metrics (unsprayed test leaves of the %s split): three models on three inputs' % LABEL).font = BF
    mtab = mt[['task', 'input', 'model', 'model_name'] + KEYS].copy(); e = table(ws, r0, 1, mtab, '0.000'); ROWOF = {(r.task, r.input, r.model): r0 + 1 + i for i, r in enumerate(mtab.itertuples())}
    COLOF = {k: CL(5 + j) for j, k in enumerate(KEYS)}
    ws.cell(e + 1, 1, 'fold_sd = plot-bootstrap SD (500 resamples of the test plots) of macro-F1 (tasks A, B) or RMSE (task C). B2 = best ML model of Activity 2.2 (A SVM, B XGBoost, C random forest; for C, B2 = random forest).').font = NOTEF
    # 3. M0 / M1 / M2 with formula gains and bootstrap CIs
    SU = json.load(open(D + 'cov2_summary.json')); G = pd.read_csv(D + 'cov2_gains.csv')
    r1 = e + 4; ws.cell(r1 - 1, 1, '3. Gains: ΔS = M1 − M0 (spectra), ΔC = M2 − M1 (covariates added), ΔT = M2 − M0; values linked to table 2, Δ and flag are formulas').font = BF
    header(ws, r1, 1, ['task', 'metric', 'M0 model', 'M0', 'M1', 'M2', 'gain', 'Δ (formula)', 'CI low', 'CI high', 'bootstrap SD', 'p (bootstrap)', 'real? (formula)'])
    rr = r1 + 1; GROWS = {}
    for t in 'ABC':
        for k in dict.fromkeys(G[G.task == t].metric):
            cells = {mk: "=%s%d" % (COLOF[k], ROWOF[(t, SU[t][mk]['input'], SU[t][mk]['model'])]) for mk in ('M0', 'M1', 'M2')}
            for gname, a, b_ in (('ΔS = M1 − M0', 'E', 'D'), ('ΔC = M2 − M1', 'F', 'E'), ('ΔT = M2 − M0', 'F', 'D')):
                g_ = G[(G.task == t) & (G.metric == k) & (G.gain == gname)].iloc[0]
                vals = [t, k, SU[t]['M0']['model_name'], cells['M0'], cells['M1'], cells['M2'], gname, '=%s%d-%s%d' % (a, rr, b_, rr), float(g_.ci_low), float(g_.ci_high), float(g_.boot_sd), float(g_.p_boot),
                        '=IF(OR(I{0}>0,J{0}<0),IF((H{0}>0)=(B{0}<>"RMSE"),"real gain","real loss"),"not real")'.format(rr)]
                for j, v in enumerate(vals):
                    c_ = ws.cell(rr, 1 + j, v); c_.font = NF
                    if j in (3, 4, 5, 7, 8, 9, 10, 11): c_.number_format = '0.000'
                GROWS[(t, k, gname)] = rr; rr += 1
    ws.cell(rr, 1, 'Real gain = 95% plot-block bootstrap interval (2000 resamples of whole test plots; Efron and Tibshirani, 1993) excludes 0 (one test set: the fold rules of the LORO analysis cannot be applied). For RMSE a negative Δ is an improvement.').font = NOTEF
    # 4. DeLong
    r2 = rr + 3
    if os.path.exists(D + 'cov2_delong.csv'):
        ws.cell(r2 - 1, 1, '4. DeLong test of the detection AUC (DeLong et al., 1988)').font = BF; dl = pd.read_csv(D + 'cov2_delong.csv'); e = table(ws, r2, 1, dl, '0.0000')
        c_ = ws.cell(r2, 6, 'ΔAUC (formula)'); c_.font = HF; c_.fill = HFILL
        for i in range(len(dl)): ws.cell(r2 + 1 + i, 6, '=B%d-C%d' % (r2 + 1 + i, r2 + 1 + i)).number_format = '0.000'
        r2 = e + 3
    # 5. interpretable model B1
    if os.path.exists(D + 'cov2_b1_coef.csv'):
        ws.cell(r2 - 1, 1, '5. Interpretable model B1 on all unsprayed leaves (standardised covariates: effect per SD); odds ratio = EXP(estimate) as formula').font = BF
        cf = pd.read_csv(D + 'cov2_b1_coef.csv')[['model', 'term', 'estimate', 'ci_low', 'ci_high', 'p']]; e = table(ws, r2, 1, cf, '0.000')
        c_ = ws.cell(r2, 7, 'odds ratio (formula)'); c_.font = HF; c_.fill = HFILL
        for i, r_ in enumerate(cf.itertuples()):
            ws.cell(r2 + 1 + i, 6).number_format = '0.0000'
            if 'ogistic' in r_.model: ws.cell(r2 + 1 + i, 7, '=EXP(C%d)' % (r2 + 1 + i)).number_format = '0.00'
        ws.cell(e + 1, 1, 'B1 models: logistic regression (A), proportional-odds ordinal logistic regression (B; McCullagh, 1980), linear model with DAS and DAS² (C; Madden et al., 2007).').font = NOTEF
    # 6. chart tables (formulas) + native charts
    cr = 5; cc = 16
    for t, k, ttl in (('A', 'macro_F1', 'Detection: macro-F1'), ('B', 'macro_F1', 'Six grades: macro-F1'), ('C', 'R2', 'Severity score: R²')):
        mods = ['Statistical', 'RF'] + ([] if t == 'C' else ['B2'])
        header(ws, cr, cc, ['input'] + [mt[(mt.task == t) & (mt.model == m_)].model_name.iloc[0] for m_ in mods])
        for i, inp in enumerate(['covariates only', 'leaf spectra', 'spectra + covariates']):
            ws.cell(cr + 1 + i, cc, inp).font = NF
            for j, m_ in enumerate(mods): ws.cell(cr + 1 + i, cc + 1 + j, '=%s%d' % (COLOF[k], ROWOF[(t, inp, m_)])).number_format = '0.000'
        ch = BarChart(); ch.type = 'col'; ch.add_data(Reference(ws, min_col=cc + 1, max_col=cc + len(mods), min_row=cr, max_row=cr + 3), titles_from_data=True); ch.set_categories(Reference(ws, min_col=cc, min_row=cr + 1, max_row=cr + 3))
        ch.y_axis.scaling.min = 0; ws.add_chart(style_chart(ch, ttl, None, k.replace('_', '-'), 16, 7.5), '%s%d' % (CL(cc + 5), cr)); cr += 16
    header(ws, cr, cc, ['gain (primary metric)', 'A macro-F1', 'B macro-F1', 'C R²'])
    for i, gname in enumerate(['ΔS = M1 − M0', 'ΔC = M2 − M1', 'ΔT = M2 − M0']):
        ws.cell(cr + 1 + i, cc, gname).font = NF
        for j, (t, k) in enumerate((('A', 'macro_F1'), ('B', 'macro_F1'), ('C', 'R2'))): ws.cell(cr + 1 + i, cc + 1 + j, '=H%d' % GROWS[(t, k, gname)]).number_format = '0.000'
    ch = BarChart(); ch.type = 'col'; ch.add_data(Reference(ws, min_col=cc + 1, max_col=cc + 3, min_row=cr, max_row=cr + 3), titles_from_data=True); ch.set_categories(Reference(ws, min_col=cc, min_row=cr + 1, max_row=cr + 3))
    ws.add_chart(style_chart(ch, 'Gains in the primary metric', None, 'Δ', 16, 7.5), '%s%d' % (CL(cc + 5), cr))
    widths(ws, 13); ws.column_dimensions['A'].width = 16; ws.column_dimensions['B'].width = 20; ws.column_dimensions['C'].width = 26; ws.column_dimensions['D'].width = 24; ws.column_dimensions['M'].width = 18; ws.column_dimensions['P'].width = 22

# ------------------------------------------------------------------ 27 References
ws = sheet('26_References', 'References of the methods used in this workbook')
refs = json.load(open(D + 'refs_used.json')) if os.path.exists(D + 'refs_used.json') else []
for i, rf in enumerate(refs): ws.cell(3 + i, 1, rf).font = NF
ws.column_dimensions['A'].width = 180

# ------------------------------------------------------------------ 29-33 the split and the comparison with LORO
import split_cfg as SC_
BF = Font(name=AR, bold=True, size=11, color='1F3864')
SPJ = json.load(open(D + 'split.json')); SPP = pd.read_csv(D + 'split_plots.csv'); OTHER = {'70:30': '80:20', '80:20': '70:30'}[LABEL]; CMPD = B + '../splitcmp/out/'
ws = sheet('29_Split', 'The grouped, stratified %s hold-out split (Steps F1–F3)' % LABEL,
           'Whole plots go to one side only (Roberts et al., 2017). Healthy (sprayed) and unsprayed plots were split separately; unsprayed test plots come from different treatments and are spread evenly over replications, varieties and timings; '
           'among the candidate splits the one closest to the target leaf share and to the overall grade and date distribution was chosen (split_lib.py). Counts are COUNTIFS formulas on 1_Data (column "set").')
SCOL = CL(meta_cols.index('set') + 1); SRANGE = "'1_Data'!$%s$5:$%s$%d" % (SCOL, SCOL, NROW); DCOL = CL(meta_cols.index('date') + 1); DRANGE = "'1_Data'!$%s$5:$%s$%d" % (DCOL, DCOL, NROW)
info = [('Split', LABEL), ('Target test fraction', SC_.TEST_FRAC), ('Seed of the split search', SC_.SEED), ('Candidate splits that met the rules', SPJ['n_candidates']), ('Distance of the chosen split from the target', SPJ['score']),
        ('Median distance of all candidates', SPJ['score_median']), ('Test plots', ', '.join(map(str, SPJ['test_plots']))), ('Healthy test plots', ', '.join(map(str, SPJ['test_healthy_plots']))), ('Unsprayed test plots', ', '.join(map(str, SPJ['test_unsprayed_plots'])))]
header(ws, 4, 1, ['Item', 'Value'])
for i, (a_, b_) in enumerate(info): ws.cell(5 + i, 1, a_).font = NF; c_ = ws.cell(5 + i, 2, b_); c_.font = Font(name=AR, size=10, color='0000FF')
r = 5 + len(info) + 2; ws.cell(r - 1, 1, 'Leaves by set and grade (formulas)').font = BF
header(ws, r, 1, ['set'] + ['grade %d' % g for g in GR] + ['total', 'share of leaves', 'mean grade', 'diseased (%)'])
for i, st_ in enumerate(('train', 'test')):
    rr = r + 1 + i; ws.cell(rr, 1, st_).font = NF
    for j, g in enumerate(GR): ws.cell(rr, 2 + j, '=COUNTIFS(%s,"%s",%s,%d)' % (SRANGE, st_, GRANGE, g))
    ws.cell(rr, 8, '=SUM(B%d:G%d)' % (rr, rr)); ws.cell(rr, 9, '=H%d/SUM($H$%d:$H$%d)' % (rr, r + 1, r + 2)).number_format = '0.0%'
    ws.cell(rr, 10, '=SUMPRODUCT(B%d:G%d,{0,1,3,5,7,9})/H%d' % (rr, rr, rr)).number_format = '0.00'; ws.cell(rr, 11, '=1-B%d/H%d' % (rr, rr)).number_format = '0.0%'
r2 = r + 5; ws.cell(r2 - 1, 1, 'Share of each grade and date within the set (formulas) – the split keeps them alike').font = BF
dts = sorted(M.date.unique()); header(ws, r2, 1, ['set'] + ['grade %d' % g for g in GR] + list(dts))
for i, st_ in enumerate(('train', 'test')):
    rr = r2 + 1 + i; ws.cell(rr, 1, st_).font = NF
    for j, g in enumerate(GR): ws.cell(rr, 2 + j, '=%s%d/$H$%d' % (CL(2 + j), r + 1 + i, r + 1 + i)).number_format = '0.0%'
    for j, d_ in enumerate(dts): ws.cell(rr, 8 + j, '=COUNTIFS(%s,"%s",%s,"%s")/$H$%d' % (SRANGE, st_, DRANGE, d_, r + 1 + i)).number_format = '0.0%'
r3 = r2 + 5; ws.cell(r3 - 1, 1, 'Plots (field layout) and their set').font = BF; table(ws, r3, 1, SPP.rename(columns={'n': 'leaves'}))
from openpyxl.chart import Series as _Ser
ch = BarChart(); ch.type = 'col'
for i in range(2): s_ = _Ser(Reference(ws, min_col=2, max_col=7, min_row=r2 + 1 + i), title=('train', 'test')[i]); ch.series.append(s_)
ch.set_categories(Reference(ws, min_col=2, max_col=7, min_row=r2)); ws.add_chart(style_chart(ch, 'Grade distribution of training and test leaves', None, 'share of leaves', 16, 8), 'N4'); widths(ws, 13, 34)
if os.path.exists(CMPD + 'cmp3_side.csv'):
    S3 = pd.read_csv(CMPD + 'cmp3_side.csv'); ws = sheet('30_Cmp_side', 'Every metric of every model: LORO (earlier analysis, all %d leaves) vs %s (test plots)%s' % (len(M), LABEL, (' vs ' + OTHER) if OTHER in S3 else ''),
        'LORO and split values are data (blue); differences and "better?" are formulas. Lower is better for RMSE and MAE. Different designs test different leaves – see 31_Cmp_paired for the fair comparison on the same leaves.')
    cols_ = ['task', 'model', 'type', 'metric', 'LORO', LABEL] + ([OTHER] if OTHER in S3 else [])
    header(ws, 4, 1, cols_ + ['Δ %s − LORO' % LABEL] + (['Δ %s − LORO' % OTHER] if OTHER in S3 else []) + ['%s better?' % LABEL])
    for i, rw in enumerate(S3.itertuples(index=False)):
        rr = 5 + i; d_ = rw._asdict()
        for j, c in enumerate(cols_):
            v = S3.iloc[i][c]; c_ = ws.cell(rr, 1 + j, None if (isinstance(v, float) and np.isnan(v)) else (float(v) if isinstance(v, (float, np.floating)) else v)); c_.font = Font(name=AR, size=10, color='0000FF') if j >= 4 else NF
            if j >= 4: c_.number_format = '0.000'
        k_ = len(cols_) + 1; ws.cell(rr, k_, '=F%d-E%d' % (rr, rr)).number_format = '+0.000;-0.000;0.000'
        if OTHER in S3: ws.cell(rr, k_ + 1, '=G%d-E%d' % (rr, rr)).number_format = '+0.000;-0.000;0.000'; k_ += 1
        ws.cell(rr, k_ + 1, '=IF(OR(D{0}="RMSE",D{0}="MAE"),IF({1}{0}<0,"yes","no"),IF({1}{0}>0,"yes","no"))'.format(rr, CL(len(cols_) + 1)))
    e_ = 4 + len(S3); rr = e_ + 2; ws.cell(rr, 1, 'Summary (formulas): models better with %s than LORO on the main metric' % LABEL).font = BF
    for i, (t_, k_) in enumerate((('A', 'macro_F1'), ('B', 'macro_F1'), ('C', 'R2'))):
        ws.cell(rr + 1 + i, 1, t_).font = NF; ws.cell(rr + 1 + i, 2, k_).font = NF
        bc = CL(len(cols_) + (3 if OTHER in S3 else 2)); dc = CL(len(cols_) + 1)
        ws.cell(rr + 1 + i, 3, '=COUNTIFS($A$5:$A$%d,A%d,$D$5:$D$%d,B%d,$%s$5:$%s$%d,"yes")' % (e_, rr + 1 + i, e_, rr + 1 + i, bc, bc, e_))
        ws.cell(rr + 1 + i, 4, '=COUNTIFS($A$5:$A$%d,A%d,$D$5:$D$%d,B%d)' % (e_, rr + 1 + i, e_, rr + 1 + i))
        ws.cell(rr + 1 + i, 5, '=AVERAGEIFS($%s$5:$%s$%d,$A$5:$A$%d,A%d,$D$5:$D$%d,B%d)' % (dc, dc, e_, e_, rr + 1 + i, e_, rr + 1 + i)).number_format = '+0.000;-0.000'
    header(ws, rr, 3, ['better (n)', 'models (n)', 'mean Δ']); widths(ws, 14, 8); ws.column_dimensions['B'].width = 18
if os.path.exists(D + 'cmp_paired_all.csv'):
    CPa = pd.read_csv(D + 'cmp_paired_all.csv'); ws = sheet('31_Cmp_paired', 'Same test leaves: LORO predictions of the %d %s test leaves vs %s predictions (Step: fair comparison)' % (int(CPa.n_leaves.iloc[0]), LABEL, LABEL),
        'Each leaf was tested once in LORO, so both designs can be scored on exactly the same leaves. CI = 95% plot-bootstrap interval of the difference (2000 resamples of whole test plots, healthy and unsprayed separately; Field and Welsh, 2007). Δ and verdict are formulas.')
    header(ws, 4, 1, ['task', 'model', 'type', 'metric', 'leaves', 'plots', 'LORO (same leaves)', LABEL, 'Δ (formula)', 'CI low', 'CI high', 'p (bootstrap)', 'verdict (formula)'])
    for i, rw in enumerate(CPa.itertuples()):
        rr = 5 + i; vals = [rw.task, rw.model, rw.type, rw.metric, int(rw.n_leaves), int(rw.n_plots), float(rw.LORO_same), float(rw.split), '=H%d-G%d' % (rr, rr), float(rw.ci_low), float(rw.ci_high), float(rw.p_boot),
                            '=IF(AND(J{0}<=0,K{0}>=0),"no real difference",IF((J{0}>0)=(D{0}<>"RMSE"),"higher with {1}","lower with {1}"))'.format(rr, LABEL)]
        for j, v in enumerate(vals):
            c_ = ws.cell(rr, 1 + j, v); c_.font = NF
            if j in (6, 7, 8, 9, 10, 11): c_.number_format = '0.000'
    e_ = 4 + len(CPa); rr = e_ + 2; ws.cell(rr, 1, 'Summary on the main metrics (macro-F1 for A and B, R² for C) – COUNTIFS formulas').font = BF
    header(ws, rr + 1, 1, ['verdict', 'A (macro_F1)', 'B (macro_F1)', 'C (R2)'])
    for i, vd in enumerate(('higher with %s' % LABEL, 'lower with %s' % LABEL, 'no real difference')):
        ws.cell(rr + 2 + i, 1, vd).font = NF
        for j, (t_, k_) in enumerate((('A', 'macro_F1'), ('B', 'macro_F1'), ('C', 'R2'))): ws.cell(rr + 2 + i, 2 + j, '=COUNTIFS($A$5:$A$%d,"%s",$D$5:$D$%d,"%s",$M$5:$M$%d,$A%d)' % (e_, t_, e_, k_, e_, rr + 2 + i))
    widths(ws, 13, 8); ws.column_dimensions['B'].width = 18; ws.column_dimensions['M'].width = 22
if os.path.exists(D + 'cmp_repeat_runs.csv'):
    RR = pd.read_csv(D + 'cmp_repeat_runs.csv'); ws = sheet('32_Cmp_repeat', 'How much does the answer depend on the split? 20 other grouped %s splits, LORO and random leaf-level splits (light pipeline)' % LABEL,
        'Light pipeline, identical in every scheme: selection on the training part (effective ranges, SHAP-CARS 10 runs, NDSI/RSI, WRI, ReliefF, VIF < 10), A SVM, B random forest, C XGBoost, grid search in 3 inner folds (no SFFS). The summary uses AVERAGEIFS / COUNTIFS formulas on the run table.')
    cols_ = ['scheme', 'run', 'task', 'n_test', 'macro_F1', 'OA', 'AUC', 'QWK', 'R2', 'RMSE']; RR = RR.reindex(columns=cols_); e0 = table(ws, 4, 1, RR, '0.000')
    sr = lambda c: '$%s$5:$%s$%d' % (c, c, e0)
    rr = 4; ws.cell(rr - 1, 13, 'Summary (formulas)').font = BF
    header(ws, rr, 13, ['task', 'metric', 'LORO', 'main %s' % LABEL, 'grouped mean', 'grouped SD', 'grouped min', 'grouped max', 'splits above LORO', 'leaf-level mean', 'inflation (leaf − grouped)'])
    for i, (t_, k_, cc) in enumerate((('A', 'macro_F1', 'E'), ('A', 'AUC', 'G'), ('B', 'macro_F1', 'E'), ('B', 'QWK', 'H'), ('C', 'R2', 'I'), ('C', 'RMSE', 'J'))):
        r_ = rr + 1 + i; G_ = '"grouped %s"' % LABEL
        ws.cell(r_, 13, t_).font = NF; ws.cell(r_, 14, k_).font = NF
        ws.cell(r_, 15, '=AVERAGEIFS(%s,%s,"LORO",%s,"%s")' % (sr(cc), sr('A'), sr('C'), t_))
        ws.cell(r_, 16, '=AVERAGEIFS(%s,%s,"main %s",%s,"%s")' % (sr(cc), sr('A'), LABEL, sr('C'), t_))
        ws.cell(r_, 17, '=AVERAGEIFS(%s,%s,%s,%s,"%s")' % (sr(cc), sr('A'), G_, sr('C'), t_))
        ws.cell(r_, 18, '=SQRT(SUMPRODUCT((%s=%s)*(%s="%s")*(%s-Q%d)^2)/(COUNTIFS(%s,%s,%s,"%s")-1))' % (sr('A'), G_, sr('C'), t_, sr(cc), r_, sr('A'), G_, sr('C'), t_))
        ws.cell(r_, 19, '=_xlfn.MINIFS(%s,%s,%s,%s,"%s")' % (sr(cc), sr('A'), G_, sr('C'), t_)); ws.cell(r_, 20, '=_xlfn.MAXIFS(%s,%s,%s,%s,"%s")' % (sr(cc), sr('A'), G_, sr('C'), t_))
        ws.cell(r_, 21, '=COUNTIFS(%s,%s,%s,"%s",%s,"%s"&O%d)' % (sr('A'), G_, sr('C'), t_, sr(cc), '<' if k_ == 'RMSE' else '>', r_))
        ws.cell(r_, 22, '=AVERAGEIFS(%s,%s,"leaf %s",%s,"%s")' % (sr(cc), sr('A'), LABEL, sr('C'), t_))
        ws.cell(r_, 23, '=%s' % ('Q%d-V%d' % (r_, r_) if k_ == 'RMSE' else 'V%d-Q%d' % (r_, r_)))
        for c__ in range(15, 24):
            if c__ != 21: ws.cell(r_, c__).number_format = '0.000'
    ch = BarChart(); ch.type = 'col'
    for c__, nm_ in ((15, 'LORO'), (17, 'grouped %s (mean of 20)' % LABEL), (22, 'random leaf-level %s' % LABEL)): ch.series.append(_Ser(Reference(ws, min_col=c__, min_row=rr + 1, max_row=rr + 6), title=nm_))
    ch.set_categories(Reference(ws, min_col=14, min_row=rr + 1, max_row=rr + 6)); ws.add_chart(style_chart(ch, 'LORO vs grouped and leaf-level %s splits (light pipeline)' % LABEL, None, 'metric', 20, 9), 'M13'); widths(ws, 12)
ws = sheet('33_Split_types', 'Types of training / validation / test split in plant-disease studies, and what suits this data set', 'References are in 26_References and in the Word report.')
TY = [('Random hold-out 80:20', 'images, leaves or pixels drawn at random; 80% train, 20% test', 'Mohanty et al. (2016): 80–20 to 20–80 random splits of PlantVillage images; Ferentinos (2018): 17,548 of 87,848 images held out (about 80:20)'),
      ('Random hold-out 70:30', 'as above, 70% train, 30% test, often stratified by class', 'rule of thumb of 20–30% for testing (Gholamy et al., 2018); no theoretical basis, optimal ratio √p : 1 proposed by Joseph (2022)'),
      ('Train : validation : test (e.g. 70:15:15)', 'train = fit; validation = choose hyper-parameters, features, early-stopping epoch; test = used once at the end', 'Ripley (1996); Hastie et al. (2009, §7.2: e.g. 50:25:25); Goodfellow et al. (2016, §5.3); common in deep-learning leaf-image studies'),
      ('Repeated random hold-out', 'the split repeated many times and averaged', 'Cross et al. (2024): wheat stripe rust spectra, 80:20 repeated 100 times'),
      ('k-fold / leave-one-out cross-validation', 'every sample tested once; small data sets', 'Wang et al. (2016): wheat rusts, leave-one-out plus external validation; Kohavi (1995); Molinaro et al. (2005)'),
      ('Grouped / blocked (plot, field, replication)', 'all samples of a group stay on one side', 'Roberts et al. (2017); Kattenborn et al. (2022): random hold-outs overestimated accuracy by up to 28% compared with spatial blocks'),
      ('Independent test (season, site)', 'model applied to data collected elsewhere', 'Mohanty et al. (2016): 99.35% on the random hold-out, 31.4% on images taken under other conditions'),
      ('This study – LORO', 'grouped cross-validation by replication (healthy plots rotated) + inner GroupKFold by plot', 'every leaf tested once; follows the experimental design (each replication = all 12 treatments); recommended main estimate (Varma and Simon, 2006; Cawley and Talbot, 2010; Vabalas et al., 2019)'),
      ('This study – %s' % LABEL, 'grouped, stratified hold-out of whole plots; validation inside the training plots (inner GroupKFold(3) for ML, one third of the training plots for early stopping of the networks)', 'tests %d plots once; compared with LORO on the same leaves and over 20 other splits (sheets 30–32)' % SPJ['n_test_plots'])]
header(ws, 4, 1, ['Split type', 'How it works', 'Examples and references'])
for i, rw in enumerate(TY):
    for j, v in enumerate(rw): c_ = ws.cell(5 + i, 1 + j, v); c_.font = NF; c_.alignment = Alignment(wrap_text=True, vertical='top')
ws.cell(16, 1, 'Recommendation for this data set').font = BF
for i, t_ in enumerate(['Main accuracy estimate: LORO with nested, plot-grouped inner cross-validation (every leaf tested once; small sample of 48 plots).',
                        'A fixed 70:15:15 split by plots would leave about 7 test plots and 7 validation plots: too few for a stable estimate; the validation role is better served by inner grouped cross-validation.',
                        'Hold-out models (%s) are deployable models; their single-split accuracy must be read together with the repeated-split range (sheet 32).' % LABEL,
                        'The strongest test is an independent season or site (2026-27, Bharatpur).']): ws.cell(17 + i, 1, '%d. %s' % (i + 1, t_)).font = NF
ws.column_dimensions['A'].width = 34; ws.column_dimensions['B'].width = 60; ws.column_dimensions['C'].width = 90
_tr = (M.fold != 0).values; _pt = np.unique(M['plot'].values[_tr]); _rg = np.random.default_rng(42); _vp = set(_rg.choice(_pt, len(_pt) // 3, replace=False)); _va = _tr & M['plot'].isin(_vp).values; _fi = _tr & ~_va
ws.cell(23, 1, 'Which models need train : validation : test and which need only train : test (this analysis)').font = BF
header(ws, 24, 1, ['Model / step', 'What is chosen from the data', 'Validation used', 'Split it needs'])
VR = [('SVM / SVR, random forest, XGBoost, k-NN, PLS-DA / PLSR', 'hyper-parameters (grid) and SFFS feature subset', 'inner GroupKFold(3) by plot inside the training plots; refit on all training plots', 'train (+ inner CV) : test'),
      ('DNN-F1, DT-EDNet, EfficientNet-B0, ResNet18, ConvNeXt V2-Atto', 'stopping epoch (other settings fixed from Ma et al., 2026)', 'separate validation set = one third of the training plots, checked after every epoch (Prechelt, 1998; Goodfellow et al., 2016)',
       'train : validation : test = %d : %d : %d leaves (%d : %d : %d plots)' % (_fi.sum(), _va.sum(), (~_tr).sum(), len(_pt) - len(_vp), len(_vp), SPJ['n_test_plots'])),
      ('Logistic regression (covariate B1, detection)', 'penalty C', 'inner GroupKFold(3)', 'train (+ inner CV) : test'),
      ('Ordinal logistic and linear regression (covariate B1)', 'nothing (no hyper-parameters)', 'none', 'train : test'),
      ('Objective 1 steps (maps, SHAP-CARS, ReliefF, VIF)', 'bands and indices', 'training plots only (CARS: Monte Carlo CV for PLS components)', 'train : test')]
for i, rw in enumerate(VR):
    for j, v in enumerate(rw): c_ = ws.cell(25 + i, 1 + j, v); c_.font = NF; c_.alignment = Alignment(wrap_text=True, vertical='top')
ws.column_dimensions['D'].width = 50
# ------------------------------------------------------------------ 27-28 every table and figure of the Word report
import re as _re
_cl = lambda t: _re.sub(r'\[\[(T|F):(\w+)\]\]', lambda m: {'T': 'Table ', 'F': 'Figure '}[m.group(1)] + str((_TN if m.group(1) == 'T' else _FN).get(m.group(2), m.group(2))), str(t)).replace('**', '')
_RT = json.load(open(D + 'report_tables.json')) if os.path.exists(D + 'report_tables.json') else []
_RF = json.load(open(D + 'report_figures.json')) if os.path.exists(D + 'report_figures.json') else []
_TN = {t['key']: t['number'] for t in _RT}; _FN = {f['key']: f['number'] for f in _RF}
ws = sheet('27_R_Tables', 'Every table of the Word report (same numbering)', 'Tables exactly as in the report; the live-formula versions of the main tables are in sheets 1-26.')
r = 4
for t in _RT:
    ws.cell(r, 1, 'Table %d. %s' % (t['number'], _cl(t['caption']))).font = Font(name=AR, bold=True, size=11, color='1F3864'); r += 1
    for j, h in enumerate(t['rows'][0]):
        c = ws.cell(r, 1 + j, _cl(h)); c.font = HF; c.fill = HFILL; c.alignment = Alignment(wrap_text=True, vertical='center'); c.border = Border(left=thin, right=thin, top=thin, bottom=thin)
    r += 1
    for row_ in t['rows'][1:]:
        for j, v in enumerate(row_):
            c = ws.cell(r, 1 + j, _cl(v)); c.font = NF; c.alignment = Alignment(wrap_text=True, vertical='top'); c.border = Border(left=thin, right=thin, top=thin, bottom=thin)
            if isinstance(c.value, str) and c.value.startswith('='): c.data_type = 's'
        ws.row_dimensions[r].height = 15 * max(1, max(len(str(v)) // 40 + 1 for v in row_)); r += 1
    r += 2
for c_ in range(1, 15): ws.column_dimensions[CL(c_)].width = 20
from openpyxl.drawing.image import Image as _XLI
from PIL import Image as _PI
ws = sheet('28_R_Figures', 'Every figure of the Word report (same numbering)', 'Static 300-dpi images; native Excel charts of the same data are in the analysis sheets.')
r = 4
for f in _RF:
    p_ = B + 'fig/' + f['file']
    if not os.path.exists(p_): continue
    ws.cell(r, 1, 'Figure %d. %s' % (f['number'], _cl(f['caption']))).font = Font(name=AR, bold=True, size=11, color='1F3864'); r += 1
    im = _XLI(p_); w0, h0 = _PI.open(p_).size; sc = 900 / w0; im.width, im.height = int(w0 * sc), int(h0 * sc); ws.add_image(im, 'A%d' % r); r += int(im.height / 20) + 3
for w_ in wb.worksheets: w_.sheet_view.zoomScale = 90
wb._sheets.sort(key=lambda s: int(s.title.split("_")[0])); wb.active = 0
wb.calculation.fullCalcOnLoad = True
wb.save(OUT); print('saved', OUT)
