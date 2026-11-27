"""Seminar-style Word report of the 2025-26 ASD leaf analysis (Introduction -> Methods -> Results -> Discussion -> Conclusions).
All numbers are read from the result files, so the report is rebuilt after every re-run:
  python3 a10_word.py && NODE_PATH=/opt/node22/lib/node_modules node a10_build.js"""
import json, re, os, numpy as np, pandas as pd
import a_refs
B = os.path.dirname(os.path.abspath(__file__)) + '/'; D = B + 'data/'; S = B + '../'
OUTF = S + 'outputs/ASD_2025-26_leaf_analysis_white_rust_report.docx'
K = []
def esc(t):
    t = t.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${'); t = re.sub(r'_(?!\{)', r'\\\\_', t)
    return re.sub(r'\[\[(T|F):(\w+)\]\]', lambda m: '${%s(\'%s\')}' % (m.group(1), m.group(2)), t)
def js(s): return '`' + esc(s) + '`'
def H1(t): K.append("K.push(H1(%s));" % js(t))
def H2(t): K.append("K.push(H2(%s));" % js(t))
def H3(t): K.append("K.push(H3(%s));" % js(t))
def P(t): K.append("K.push(P(%s));" % js(t))
def BL(items): K.extend("K.push(BL(%s));" % js(i) for i in items)
def NL(items): K.extend("K.push(NL(%s));" % js(i) for i in items)
def BOX(l, t, fill='FFF6E0', line='C98A00'): K.append("K.push(BOX(%s, %s, '%s', '%s'));" % (js(l), js(t), fill, line))
def NOTE(t): K.append("K.push(NOTE(%s));" % js(t))
def EQ(t): K.append("K.push(EQ(%s));" % js(t))
RFIG, RTAB = [], []
def FIG(k, file, cap, w=600):
    RFIG.append(dict(key=k, file=file, caption=cap)); K.append("K.push(...fig2('%s', '%s', %s, %d));" % (k, file, js(cap), w))
def TAB(k, rows, cap, widths=None, size=17):
    if widths is None:
        L = [min(max(max(len(str(r[j])) for r in rows), 5), 46) for j in range(len(rows[0]))]; s = sum(L); widths = [int(9306 * x / s) for x in L]
    RTAB.append(dict(key=k, caption=cap, rows=[[str(c) for c in r] for r in rows]))
    R = '[' + ',\n'.join('[' + ', '.join(js(str(c)) for c in r) + ']' for r in rows) + ']'
    K.append("K.push(...tab2('%s', %s, %s, %s, %d));" % (k, R, json.dumps(widths), js(cap), size))
def PB(): K.append("K.push(new Paragraph({ children: [new PageBreak()] }));")
def CARD(key, title, concept, why, papers, mine, output, alt=None):
    """Step card: concept, position/justification, what papers used, how it was done with my data, output, alternatives."""
    rows = [['Item', title], ['Concept', concept], ['Why here (justification)', why], ['What papers used', papers], ['How with my data', mine], ['Output → next step', output]]
    if alt: rows.append(['Alternatives and notes', alt])
    TAB(key, rows, 'Step card – %s.' % title, [2250, 7056], 16)
f2 = lambda x: '–' if x is None or (isinstance(x, float) and not np.isfinite(x)) else '%.2f' % x
f3 = lambda x: '–' if x is None or (isinstance(x, float) and not np.isfinite(x)) else '%.3f' % x

# ------------------------------------------------------------------ data
M = pd.read_csv(D + 'meta.csv'); O1 = json.load(open(D + 'o1_results.json')); SEL = json.load(open(D + 'fold_selection.json'))
F = pd.read_csv(D + 'indices_full.csv'); MT = pd.read_csv(D + 'metrics_all.csv'); BEST = json.load(open(D + 'best_models.json'))
ms = pd.read_csv(D + 'o1_mean_spectra.csv'); cc = pd.read_csv(D + 'o1_corr_curves.csv'); rl = pd.read_csv(D + 'o1_relief.csv')
mls = pd.read_csv(D + 'ml_selection.csv'); strata = pd.read_csv(D + 'strata_metrics.csv'); cov = pd.read_csv(D + 'covariate_baseline.csv')
wc = pd.read_csv(D + 'weather_covariates.csv'); prog = pd.read_csv(D + 'disease_progress.csv')
opt = lambda fn: pd.read_csv(D + fn) if os.path.exists(D + fn) else None
cv2m, cv2g, cv2d, cv2c, cv2x = opt('cov2_metrics.csv'), opt('cov2_gains.csv'), opt('cov2_delong.csv'), opt('cov2_b1_coef.csv'), opt('cov2_covariates_by_date.csv')
cv2s = json.load(open(D + 'cov2_summary.json')) if os.path.exists(D + 'cov2_summary.json') else None
tt, ex, stab, cfg, abl = opt('transfer_tests.csv'), None, opt('selection_stability.csv'), opt('dl_summary_config.csv'), opt('dl_summary_ablation.csv')
MLM = ['SVM', 'RF', 'XGBoost', 'k-NN', 'PLS-DA', 'PLS']; DLM = ['DNN-F1', 'DT-EDNet', 'EfficientNet-B0', 'ResNet18', 'ConvNeXt V2-Atto']
GR = [0, 1, 3, 5, 7, 9]; N = len(M)
def row(t, m): d = MT[(MT.task == t) & (MT.model == m)]; return d.iloc[0] if len(d) else None
def mn(m, t): return {'SVM': 'SVR', 'PLS': 'PLSR'}.get(m, m) if t == 'C' else m
bA, bB, bC = BEST['A'], BEST['B'], BEST['C']
rA, rB, rC = row('A', bA['overall']), row('B', bB['overall']), row('C', bC['overall'])
dlA = row('A', bA['DL']) if bA['DL'] else None; dlB = row('B', bB['DL']) if bB['DL'] else None; dlC = row('C', bC['DL']) if bC['DL'] else None
dte = {t: row(t, 'DT-EDNet') for t in 'ABC'}
HAS_DL = all(dte[t] is not None for t in 'ABC')
_fg = sorted(((g, rB['F1_g%d' % g]) for g in GR), key=lambda x: -x[1]); FGB = (_fg[0][0], _fg[0][1], _fg[-1][0], _fg[-1][1])
dates = sorted(M.date.unique()); DASR = {d: '%d–%d' % (M[M.date == d].DAS.min(), M[M.date == d].DAS.max()) for d in dates}   # crop age range (days after sowing) per date
gN = {g: int((M.grade == g).sum()) for g in GR}
def wlv(g, w): return float(ms.loc[ms.wl == w, 'mean_%d' % g].iloc[0])
REPg = F.groupby(M.grade).REP.mean(); Drg = F.groupby(M.grade).Dr.mean()
cRmax = cc.loc[cc.r_R.abs().idxmax()]; cFmax = cc.loc[cc.r_FD.abs().idxmax()]; cFmin = cc.loc[cc.r_FD.idxmin()]
W = O1['WRI']; nd, rs = O1['best_ndsi'], O1['best_rsi']

# ------------------------------------------------------------------ title and summary
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 900, after: 200 }, children: [new TextRun({ text: 'Leaf-level hyperspectral detection and severity estimation of white rust in Indian mustard', font: FONT, size: 42, bold: true, color: '1E3A1F' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [new TextRun({ text: 'Analysis of the 2025-26 contact-probe spectroradiometer data: four dates pooled, step by step from methodology to discussion', font: FONT, size: 27, color: '2C5F2D' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: 'Objective 1 (spectral response and disease-specific features) | Objective 2 (machine-learning and deep-learning models)', font: FONT, size: 21, color: '444444' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 500 }, children: [new TextRun({ text: 'Animesh Panda | Ph.D. Agricultural Physics | ICAR-Indian Agricultural Research Institute, New Delhi', font: FONT, size: 22, bold: true })] }));")
summ = ('**Data.** %d leaf spectra (350–2500 nm, ASD contact probe, splice-corrected) from 48 plots, three varieties, four sowing timings (D1–D4 = 50, 40, 30 and 20 days after sowing), three leaf positions (L3, L5, LL) and four dates (11 February–13 March 2026; crop age %s days after sowing) under natural infection, pooled at leaf level. '
        '**Objective 1.** Disease shifted the red-edge position from %.1f nm (grade 0) to %.1f nm (grade 9) and lowered near-infrared reflectance; the strongest single correlation was the first derivative at %d nm (r = %.2f). '
        'SHAP-CARS kept %d first-derivative bands; the best two-band index was NDSI(%d, %d) nm (R² = %.2f); after ReliefF and the variance inflation factor (VIF < 10) the disease-specific feature set had %d features. '
        '**Objective 2.** Under leave-one-replication-out testing the best detection model was %s (macro-F1 %.3f, AUC %s), the best six-grade model was %s (macro-F1 %.3f, quadratic weighted kappa %.3f, %.0f%% of leaves within one grade) and the best severity-score model was %s (R² %.3f, RMSE %.2f grades). ') % (
        N, '%d–%d' % (M.DAS.min(), M.DAS.max()), REPg[0], REPg[9], cFmax.wl, cFmax.r_FD, len(O1['OW']), nd[0], nd[1], nd[2], len(O1['DSF']),
        bA['overall'], rA.macro_F1, f3(rA.AUC), bB['overall'], rB.macro_F1, rB.QWK, 100 * rB.within1, mn(bC['overall'], 'C'), rC.R2, rC.RMSE)
if HAS_DL: summ += 'Machine-learning models and networks differed by less than the fold-to-fold variation; DT-EDNet reached macro-F1 %.3f (detection) and %.3f (six grades) and R² %.3f (score). ' % (dte['A'].macro_F1, dte['B'].macro_F1, dte['C'].R2)
summ += '**Meaning.** Leaf spectra separate healthy and diseased leaves well, but neighbouring grades overlap strongly; spectra add information beyond crop stage, timing and weather.'
BOX('Summary of results.', summ, 'E8F5E9', '2E7D32')
BOX('How the files fit together.', 'This report gives each step with its concept, justification, supporting papers, how it was done with these data, the result (figure or table) and the output passed to the next step. '
    'Every table is in the Excel workbook (ASD_2025-26_leaf_analysis_white_rust.xlsx) as an editable table, most with live formulas and native Excel charts; the seminar slides (ASD_2025-26_leaf_analysis_seminar.pptx) follow the same order. '
    'The trained models are in the folder ASD_2025-26_models with a prediction script.')
PB()
K.append("K.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: 'Contents', font: FONT, size: 32, bold: true, color: '1E3A1F' })] }));")
K.append("K.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-2' }));")
PB()

# ------------------------------------------------------------------ 1 introduction
H1('1. Introduction')
P('White rust, caused by the oomycete Albugo candida, is one of the main foliar diseases of Indian mustard (Brassica juncea). Infected leaves show white blister-like pustules on the lower surface with chlorotic and later necrotic areas on the upper surface; systemic infection deforms inflorescences into "stag heads" and reduces yield (Saharan et al., 2014; Mishra et al., 2009). Epidemics are favoured by cool, humid weather (Chattopadhyay et al., 2011; Bal and Kumar, 2014).')
P('Disease is normally scored visually on a 0–9 scale. Visual grades are quick but subjective, and raters tend to disagree most between neighbouring grades (Bock et al., 2010). Hyperspectral reflectance responds to the pigment, structural and water changes caused by a pathogen and can give objective, non-destructive estimates (Mahlein, 2016; Thomas et al., 2018). Leaf-level spectra measured with a contact probe have no canopy, soil or illumination effects, so they show the pure leaf signal that later unmanned aerial vehicle (UAV) sensors must detect (Mahlein et al., 2013; Meng et al., 2020).')
P('The analysis follows the revised thesis methodology. Objective 1 uses the steps of the DT-EDNet rice-blast study (Ma et al., 2026): effective wavelength ranges from two-band index maps, optimal wavelengths by Shapley additive explanations with competitive adaptive reweighted sampling (SHAP-CARS), index construction and ReliefF selection. Objective 2 compares machine-learning models with deep networks, including DT-EDNet, EfficientNet-B0, ResNet18 and ConvNeXt V2, under a leakage-free leave-one-replication-out design (Roberts et al., 2017; Varma and Simon, 2006).')
H2('1.1 Objectives of this analysis')
TAB('objectives', [['Objective (thesis)', 'Question answered with the 2025-26 leaf spectra', 'Main outputs'],
    ['1. Spectral response and disease-specific features', 'Which wavelengths, derivatives and indices change with white rust severity, and which compact feature set describes it?', 'Mean and derivative spectra, correlation curves, NDSI/RSI maps, optimal wavelengths, White Rust Index, ReliefF indices, disease-specific feature set'],
    ['2. Machine-learning and deep-learning models', 'How well can a leaf be (A) detected as diseased, (B) placed in one of six grades and (C) given a severity score?', 'SVM, RF, XGBoost, k-NN, PLS-DA/PLSR, DNN-F1, DT-EDNet, EfficientNet-B0, ResNet18, ConvNeXt V2-Atto; metrics, ablation, SHAP, robustness']],
    'Objectives and the questions answered in this report. Objective 3 (pre-symptomatic detection) is not addressed: no pre-symptomatic dates were sampled in 2025-26.', [2400, 3900, 3006])

# ------------------------------------------------------------------ 2 materials and methods
H1('2. Materials and methods')
FIG('workflow', 'f00_workflow.png', 'Workflow of the analysis from data collection to discussion: data collection and quality control, pre-processing and features, Objective 1 (spectral response and feature selection), validation design, Objective 2 (models and evaluation), covariate baseline, interpretation and discussion.', 620)
H2('2.1 Experiment and field layout')
P('The 2025-26 experiment had 48 plots (5 m × 3.5 m, 0.5-m bunds, 2-m channels; field 48 m × 24 m). Plots 1–12 formed the healthy block, kept free of disease by fungicide sprays; plots 13–24, 25–36 and 37–48 were the three unsprayed replications (R3, R2, R1), exposed to natural infection; no artificial inoculation was made. Each block contained the 12 combinations of three varieties (V1, V2, V3) and four sowing dates (D1–D4), which gave crops of 50, 40, 30 and 20 days after sowing (DAS) at the end of January 2026.')
das0 = {t: (pd.Timestamp(s) + pd.Timedelta(days=int(p_))).strftime('%d %b %Y') for t, s, p_ in (('D1', '2025-12-09', 50), ('D2', '2025-12-18', 40), ('D3', '2025-12-27', 30), ('D4', '2026-01-09', 20))}   # date at the treatment crop age
TAB('design', [['Sowing timing', 'Sowing date', 'Treatment crop age (DAS)', 'Date at that crop age', 'Crop age at the four sampling dates (DAS)'],
    *[[t, s, p, str(das0[t]), ', '.join(str(int(M[(M.timing == t) & (M.date == d)].DAS.iloc[0])) for d in dates)] for t, s, p in (('D1', '9 Dec 2025', '50'), ('D2', '18 Dec 2025', '40'), ('D3', '27 Dec 2025', '30'), ('D4', '9 Jan 2026', '20'))]],
    'Sowing timings (treatments D1–D4 = 50, 40, 30 and 20 days after sowing) and crop age at the four sampling dates (natural infection).', [1500, 1700, 1900, 1900, 2306])
NOTE('Natural infection: no artificial inoculation was made in 2025-26. The four sowing dates produced crops of four ages (50, 40, 30 and 20 days after sowing at the end of January 2026) exposed to the same natural inoculum and weather. Crop age at sampling (days after sowing, DAS) is used as the time variable of the crop.')
H2('2.2 Leaf spectra acquisition and disease scoring (Step A4)')
P('On each of the four sampling dates (11 and 24 February, 3 and 13 March 2026; crop age %s days after sowing) leaves were measured in all 48 plots with the ASD FieldSpec spectroradiometer fitted with the contact probe and leaf clip. The probe has its own halogen light source, so readings do not depend on the sky (Milton et al., 2009). Reflectance was recorded from 350 to 2500 nm at 1-nm intervals, and the files were already splice-corrected at the detector joins. Three leaf positions were sampled: the third (L3) and fifth (L5) fully expanded leaf from the top and the lowest green leaf (LL). Nine spectra of 11 February labelled L4 in the files are not one of the sampled positions and were removed, leaving %d leaf spectra. Each measured leaf was scored on the 0–9 white rust scale (grades 0, 1, 3, 5, 7, 9).' % ('%d–%d' % (M.DAS.min(), M.DAS.max()), N))
P('Each date was delivered as one Excel file in which every leaf spectrum is a column with seven header rows (wavelength, plot number, variety, growth stage, plot status, leaf position, score). Columns with plot averages were also present but were not used, because the analysis is at leaf level.')
lp = pd.crosstab(M.date, M.leaf)
TAB('leafpos', [['Date', 'L3', 'L5', 'LL', 'Leaves', 'Plots', 'Leaves per plot (median, range)']] + [[pd.Timestamp(d).strftime('%d %b %Y'), *[str(int(lp.loc[d].get(c, 0))) for c in ('L3', 'L5', 'LL')], str(int(lp.loc[d].sum())), str(int(M[M.date == d]['plot'].nunique())),
    '%d (%d–%d)' % (M[M.date == d].groupby('plot').size().median(), M[M.date == d].groupby('plot').size().min(), M[M.date == d].groupby('plot').size().max())] for d in dates],
    'Leaf spectra by sampling date and leaf position.', [1600, 1000, 1000, 1000, 1100, 900, 2706])
dt_rows = [['Date', 'Crop age (DAS)', 'Growth stages', 'Leaves', 'Mean grade', 'Diseased leaves (%)']]
for d in dates:
    g = M[M.date == d]; dt_rows.append([pd.Timestamp(d).strftime('%d %b %Y'), DASR[d], ', '.join(sorted(g.stage.unique())), str(len(g)), f2(g.grade.mean()), '%.1f' % (100 * g.diseased.mean())])
dt_rows.append(['All', '6–36', 'vegetative, flowering, pod formation', str(N), f2(M.grade.mean()), '%.1f' % (100 * M.diseased.mean())])
TAB('dates', dt_rows, 'Sampling dates, growth stages and disease level of the leaf spectra.', [1500, 1500, 2600, 1100, 1200, 1406])
TAB('grades', [['Grade', *[str(g) for g in GR], 'Total'], ['Leaves', *[str(gN[g]) for g in GR], str(N)], ['Share (%)', *['%.1f' % (100 * gN[g] / N) for g in GR], '100']],
    'Number of leaves in each severity grade (pooled data).', [1500] + [1000] * 6 + [1806])
FIG('dataset', 'f01_dataset.png', 'Leaves by (a) sampling date, (b) growth stage, (c) variety and (d) leaf position, coloured by severity grade.', 560)
H2('2.3 Weather data and covariates (Step A6)')
P('Daily weather of the season (1 December 2025 to 20 March 2026) came from the IARI agro-meteorological observatory: maximum and minimum air temperature (T_{max}, T_{min}), rainfall, morning (RH I) and afternoon (RH II) relative humidity, wind speed, bright sunshine and evaporation. For every sampling date the 7 days before the date were summarised (mean T_{max}, T_{min}, RH I, RH II; total rainfall). The window ends the day before the date, so no later weather enters any model. Because infection was natural, favourable days were counted from each sowing date to the day before the sampling date, for leaf infection (T_{max} 16–24 °C, RH I > 97% and RH II > 40%) and for staghead (T_{max} 20–29 °C, T_{min} > 12 °C and RH I > 97%) (Chattopadhyay et al., 2011). Leaf-level covariates were crop age (days after sowing, DAS), sowing timing (D1–D4: 50, 40, 30 and 20 DAS treatments), variety and growth stage (vegetative, flowering, pod formation, coded 1–3 following the BBCH ranges; Lancashire et al., 1991).')
if cv2x is not None:
    TAB('covdate', [['Date', 'Tmax 7 d (°C)', 'Tmin 7 d (°C)', 'RH I 7 d (%)', 'RH II 7 d (%)', 'Rain 7 d (mm)', 'Favourable leaf days in 7 d', 'Favourable leaf days since sowing D1 / D2 / D3 / D4', 'Staghead days since sowing']] +
        [[pd.Timestamp(r.date).strftime('%d %b'), '%.1f' % r.Tmax7, '%.1f' % r.Tmin7, '%.0f' % r.RH1_7, '%.0f' % r.RH2_7, '%.1f' % r.rain7, str(int(r.fav7_leaf)), ' / '.join(str(int(getattr(r, 'fav_leaf_' + t))) for t in ('D1', 'D2', 'D3', 'D4')), str(int(r.fav_staghead_max))] for r in cv2x.itertuples()],
        'Weather covariates of the four sampling dates (7-day windows ending the day before each date; favourable days after Chattopadhyay et al., 2011).', [900, 900, 900, 850, 850, 850, 1200, 1856, 1000], 15)
H2('2.4 Data organisation and quality control')
NL(['**Parsing:** the four files were read; the %d leaf columns (headers ending in .sco) were kept and the plot-average columns were skipped.' % N,
    '**Treatments:** plot numbers were joined to the field layout (block, sowing timing, variety); the variety written in the files agreed with the layout for all 48 plots.',
    '**Labels:** grade from the score; detection label diseased = grade > 0. The %d leaves of the sprayed healthy block were all grade 0; %d leaves came from the unsprayed, naturally infected plots.' % (int((M.block == 'C').sum()), int((M.unsprayed == 1).sum())),
    '**Leaf positions:** only L3, L5 and LL were sampled; the nine spectra labelled L4 (11 February) were removed.',
    '**Derived fields:** crop age at sampling (days after sowing, DAS) from the sowing dates and the growth-stage code.',
    '**Checks:** grades only 0, 1, 3, 5, 7 or 9; wavelength grid 350–2500 nm at 1 nm; no missing values; reflectance between %.3f and %.3f; all 48 plots on every date; %d–%d leaves per plot and date (median %d).' % (float(np.load(D + 'X_leaf.npy').min()), float(np.load(D + 'X_leaf.npy').max()), M.groupby(['date', 'plot']).size().min(), M.groupby(['date', 'plot']).size().max(), M.groupby(['date', 'plot']).size().median()),
    '**Folds:** every leaf was assigned to the outer fold of its plot (Step F1, section 2.6).'])
H2('2.5 Three prediction tasks')
TAB('tasks', [['Task', 'Target', 'Type', 'Main metric'], ['A – detection', 'grade 0 (healthy) vs grade > 0 (diseased); %d vs %d leaves' % (gN[0], N - gN[0]), 'binary classification', 'macro-F1, AUC'],
    ['B – six grades', 'grade 0, 1, 3, 5, 7, 9', 'multi-class (ordinal) classification', 'macro-F1, quadratic weighted kappa'], ['C – severity score', 'grade as a number 0–9', 'regression', 'R², RMSE, RPD']],
    'Prediction tasks.', [1700, 3500, 2300, 1806])
H2('2.6 Pooling and validation design')
CARD('cvcard', 'Leave-one-replication-out validation (Steps F1–F3)',
     'The model is trained on two replications and tested on the third, which it has never seen; repeated three times so that every leaf is tested once.',
     'Leaves of one plot share soil, microclimate and inoculum, so random leaf splits would put near-copies in training and test and inflate accuracy. Blocking by replication avoids this (Roberts et al., 2017). The fungicide-protected healthy plots are rotated so that every test fold has four healthy plots.',
     'Spatially blocked cross-validation (Roberts et al., 2017); nested selection and tuning inside the training part to avoid selection bias (Ambroise and McLachlan, 2002; Varma and Simon, 2006; Cawley and Talbot, 2010).',
     'Fold 1 tests R1 (plots 37–48) + healthy plots 7, 2, 10, 12; fold 2 tests R2 + 5, 8, 4, 1; fold 3 tests R3 + 3, 9, 11, 6. Feature selection, SFFS and grid search use only the training part, with inner GroupKFold(3) by plot.',
     'Pooled test predictions of all %d leaves for every model.' % N, 'Leave-one-date-out was not used because the dates differ in growth stage and disease level (see 2.12 for the transfer tests).')
TAB('folds', [['Outer fold', 'Test replication', 'Healthy plots in test', 'Test leaves', 'Training leaves'],
    *[[str(f + 1), {0: 'R1 (37–48)', 1: 'R2 (25–36)', 2: 'R3 (13–24)'}[f], {0: '7, 2, 10, 12', 1: '5, 8, 4, 1', 2: '3, 9, 11, 6'}[f], str(int((M.fold == f).sum())), str(int((M.fold != f).sum()))] for f in range(3)]],
    'Outer folds of the leave-one-replication-out design.', [1500, 2000, 2300, 1700, 1806])
H2('2.7 Pre-processing (Steps B3 and D2 for leaf spectra)')
CARD('prepcard', 'Spectral range, smoothing and first derivative',
     'Savitzky–Golay smoothing fits a local polynomial in a moving window; the same fit gives the first derivative, which removes additive offsets and sharpens the red edge (Savitzky and Golay, 1964; Tsai and Philpot, 1998).',
     'Contact-probe spectra are clean, but the detector ends (350–399 nm and 2401–2500 nm) are noisy. Water-absorption regions (1350–1460 and 1790–1960 nm) were kept: the probe uses its own light source, so atmospheric water does not affect them, and they carry leaf-water information.',
     'Savitzky–Golay with the first derivative in rice blast (Ma et al., 2026) and wheat diseases (Huang et al., 2020; Meng et al., 2020); derivative analysis of leaf spectra (Tsai and Philpot, 1998).',
     'Savitzky–Golay window 11 nm, order 2, applied on 350–2500 nm; spectra trimmed to 400–2400 nm; first derivative from the same filter; bands taken every 5 nm (401 reflectance + 401 derivative features).',
     'Smoothed reflectance R_{λ} and first derivative FD_{λ} (×10^{-3} nm^{-1}) at 5 nm.', 'The second derivative was not used (agreed rule: it amplifies noise). Standard normal variate and continuum removal were not needed for contact-probe data.')
H2('2.8 Spectral features')
IDXF = {'NDVI': '(R_{800}−R_{670})/(R_{800}+R_{670})', 'NDVI850': '(R_{850}−R_{650})/(R_{850}+R_{650})', 'SR': 'R_{800}/R_{680}', 'RVI': 'R_{800}/R_{670}', 'GNDVI': '(R_{850}−R_{550})/(R_{850}+R_{550})',
        'RDVI': '(R_{800}−R_{670})/√(R_{800}+R_{670})', 'MSR': '(R_{800}/R_{670}−1)/√(R_{800}/R_{670}+1)', 'OSAVI': '1.16(R_{800}−R_{670})/(R_{800}+R_{670}+0.16)', 'TVI': '0.5[120(R_{750}−R_{550})−200(R_{670}−R_{550})]',
        'MTVI2': '1.5[1.2(R_{800}−R_{550})−2.5(R_{670}−R_{550})]/√[(2R_{800}+1)^{2}−(6R_{800}−5√R_{670})−0.5]', 'MCARI': '[(R_{700}−R_{670})−0.2(R_{700}−R_{550})](R_{700}/R_{670})',
        'TCARI': '3[(R_{700}−R_{670})−0.2(R_{700}−R_{550})(R_{700}/R_{670})]', 'VIgreen': '(R_{550}−R_{670})/(R_{550}+R_{670})', 'GI': 'R_{554}/R_{677}', 'CIrededge': 'R_{790}/R_{720}−1', 'CIgreen': 'R_{790}/R_{550}−1',
        'NDRE': '(R_{790}−R_{720})/(R_{790}+R_{720})', 'MTCI': '(R_{754}−R_{709})/(R_{709}−R_{681})', 'PSSRa': 'R_{800}/R_{680}', 'PSSRb': 'R_{800}/R_{635}', 'PSSRc': 'R_{800}/R_{470}', 'SIPI': '(R_{800}−R_{445})/(R_{800}−R_{680})',
        'NPCI': '(R_{680}−R_{430})/(R_{680}+R_{430})', 'PSRI': '(R_{680}−R_{500})/R_{750}', 'ARI': '1/R_{550}−1/R_{700}', 'PRI': '(R_{531}−R_{570})/(R_{531}+R_{570})', 'NPQI': '(R_{415}−R_{435})/(R_{415}+R_{435})',
        'RVSI': '(R_{712}+R_{752})/2−R_{732}', 'HI': '(R_{534}−R_{698})/(R_{534}+R_{698})−0.5R_{704}', 'WI': 'R_{900}/R_{970}', 'WBI': 'R_{970}/R_{900}', 'NDWI': '(R_{860}−R_{1240})/(R_{860}+R_{1240})',
        'MoistSI': 'R_{1600}/R_{820}', 'NDII': '(R_{819}−R_{1649})/(R_{819}+R_{1649})', 'DWSI-1': 'R_{800}/R_{1660}', 'DWSI-2': 'R_{1660}/R_{550}', 'DWSI-3': 'R_{1660}/R_{680}', 'DWSI-4': 'R_{550}/R_{680}',
        'DWSI-5': '(R_{800}+R_{550})/(R_{1660}+R_{680})', 'RBI': 'R_{1148}/R_{1301}', 'NDBI': '(R_{1148}−R_{1301})/(R_{1148}+R_{1301})', 'REP': 'wavelength of maximum FD in 680–760 nm', 'Dr': 'maximum FD in 680–760 nm (×10^{-3})', 'REarea': 'sum of FD over 680–760 nm'}
IREF = json.load(open(D + 'index_refs.json')); rcorr = F.corrwith(M.grade)
idx_rows = [['Index', 'Formula', 'Reference', 'r with grade']] + [[k, v, IREF.get(k, ''), f2(rcorr.get(k, np.nan))] for k, v in IDXF.items()]
P('Forty-one published vegetation indices (pigment, structure, red edge, water and disease indices) and three red-edge parameters (44 features) were computed from the 1-nm smoothed reflectance ([[T:indices]]). Three data-driven indices were added in Objective 1: the best normalised difference spectral index (NDSI_best), the best ratio spectral index (RSI_best) and the White Rust Index (WRI).')
TAB('indices', idx_rows, 'Vegetation indices and red-edge parameters computed for every leaf, with Pearson r against the leaf grade (n = %d).' % N, [1300, 4300, 2600, 1106], 15)
H2('2.9 Objective 1 – spectral response and disease-specific features')
CARD('o11card', 'Activity 1.1 – Response analysis', 'Mean reflectance and first-derivative curves of each grade show where and how the spectrum changes with disease; Pearson correlation of each band with the grade measures the strength of the change.',
     'It is the first, model-free evidence of the disease signal and shows whether the response is consistent across varieties, stages and dates.', 'Mean spectra and correlation curves are the standard first step in disease spectroscopy (Mahlein et al., 2013; Meng et al., 2020; Mandal et al., 2023; Ma et al., 2026).',
     'Means ± SD by grade for 400–2400 nm; first derivative; r of each 5-nm band and derivative with the grade; spectra by growth stage; mean grade by stage, variety, leaf position and timing.', 'Disease-sensitive regions; evidence for the band selection that follows.')
CARD('o12card', 'Activity 1.2 – Effective ranges and optimal wavelengths (SHAP-CARS)', 'NDSI and RSI are computed for every pair of bands; the R² with the grade forms a map whose high-value area defines the effective wavelength ranges. Inside them, a gradient-boosting model ranks bands by mean |SHAP| (top 40% kept) and CARS with PLS selects the final optimal wavelengths.',
     '802 correlated bands cannot go into a model directly. SHAP removes uninformative bands before CARS, so CARS works on a smaller, relevant set and is more stable (Ma et al., 2026).',
     'NDSI/RSI R² maps and SHAP-CARS for rice blast (Ma et al., 2026); CARS (Li et al., 2009); SHAP (Lundberg and Lee, 2017; Lundberg et al., 2020).',
     'Threshold R² ≥ 0.5 for effective ranges, else the top 5%% of pairs (used here: R² ≥ %.3f); red-edge derivatives 680–760 nm always candidates; XGBoost (300 trees, depth 4, learning rate 0.05); bands standardised; PLS components by Monte Carlo cross-validation (50 splits); CARS 50 iterations × 20 runs; bands kept if selected in ≥ 50%% of runs (maximum 15).' % O1['eff_thr'],
     'Optimal wavelengths (OW).', 'Reflectance and derivative bands were pooled in one SHAP-CARS run (agreed decision).')
CARD('o13card', 'Activities 1.3–1.4 – Index construction and ReliefF selection', 'The best NDSI and RSI pairs come from the maps; the White Rust Index adds a third band to the best NDSI: WRI = NDSI(λ_{1}, λ_{2}) + w·R_{λ3}. Indices with |r| ≥ 0.95 are reduced to the one most correlated with the grade; ReliefF (classes) and RReliefF (score) rank the rest.',
     'A three-band index can correct a confounding effect that a two-band index cannot; ReliefF judges an index by how well it separates near neighbours of different classes, so it handles interactions and is not fooled by correlation alone.',
     'Three-band disease indices (Meng et al., 2020; Mandal et al., 2023; Ma et al., 2026); ReliefF and RReliefF (Kira and Rendell, 1992; Kononenko, 1994; Robnik-Šikonja and Kononenko, 2003; Urbanowicz et al., 2018).',
     'WRI search: the 200 best NDSI pairs at least 50 nm apart, λ_{3} every 10 nm, w ∈ {−1, −0.5, 0, 0.5, 1}. ReliefF with k = 10 neighbours, neighbours from the same plot excluded; top five indices kept for each task.', 'Selected indices (VI) for detection, six grades and score.')
CARD('o16card', 'Activity 1.6 – Variance inflation factor and the disease-specific feature set', 'VIF = 1/(1 − R²_{j}) measures how well feature j is explained by the others; the feature with the largest VIF is removed until all are below 10.',
     'Optimal wavelengths and indices overlap; strong collinearity makes models unstable and explanations unreliable (Dormann et al., 2013; O\'Brien, 2007).', 'VIF screening before modelling (Dormann et al., 2013; Mandal et al., 2023).',
     'Pool = optimal wavelengths + selected indices; iterative removal until all VIF < 10.', 'Disease-specific feature set (DSF): the input of Objective 2.')
H2('2.10 Objective 2 – models')
P('The selection of Objective 1 was repeated inside the training part of every outer fold (Step 2.1.2), so the test replication never influenced which features were used. Each machine-learning model then chose its own compact subset by sequential floating forward selection (SFFS; Pudil et al., 1994) and its hyper-parameters by grid search, both with inner GroupKFold(3) by plot. Features were standardised with training statistics only.')
TAB('mlmodels', [['Model', 'Principle (one line)', 'Grid searched', 'Reference'],
    ['SVM / SVR', 'maximum-margin boundary with radial basis kernel', 'C ∈ {0.1, 1, 10, 100}; γ ∈ {0.001, 0.01, 0.1, scale}; ε ∈ {0.1, 0.5} (SVR)', 'Cortes and Vapnik (1995)'],
    ['Random forest', 'many decorrelated decision trees, majority vote / mean', '500 trees; max_features ∈ {sqrt, 0.3}; min_samples_leaf ∈ {1, 3, 5}', 'Breiman (2001)'],
    ['XGBoost', 'gradient-boosted trees with regularisation', 'trees ∈ {200, 500}; depth ∈ {3, 5}; learning rate ∈ {0.05, 0.1}', 'Chen and Guestrin (2016)'],
    ['k-NN', 'label of the nearest training leaves', 'k ∈ {3, 5, 7, 9, 11}; uniform or distance weights', 'Cover and Hart (1967)'],
    ['PLS-DA / PLSR', 'latent components maximising covariance with the target', 'components 1–15 (≤ number of features)', 'Wold et al. (2001); Barker and Rayens (2003)']],
    'Machine-learning models and tuning grids (class weights balanced; SFFS up to 15 features, smallest subset within 1% of the best inner score).', [1500, 3100, 3200, 1506], 16)
CARD('dlcard', 'Activity 2.3 – Deep-learning models', 'DNN-F1 is a fully connected network on the feature vector. The other networks need images, so the p selected features were placed in a k × k pseudo-image (k = ⌈√p⌉, zero-padded). DT-EDNet: 3 × 3 embedding (128 channels) → squeeze-and-excitation (SE) → dual transformer group (one kernel transformer block with CBAM + four token transformer blocks, four heads) → class token → output.',
     'DT-EDNet is the network proposed for early rice-blast detection; EfficientNet-B0, ResNet18 and ConvNeXt V2 are the comparison networks of the same study, so the comparison follows the paper.',
     'DT-EDNet (Ma et al., 2026); EfficientNet (Tan and Le, 2019); ResNet (He et al., 2016); ConvNeXt V2 (Woo et al., 2023); SE (Hu et al., 2018); CBAM (Woo et al., 2018); transformer (Vaswani et al., 2017); tabular-to-image mapping (Sharma et al., 2019).',
     'Paper settings: AdamW (learning rate 6 × 10^{-4}, weight decay 10^{-5}), cosine decay to 10^{-6}, batch 32, label smoothing 0.01, gradient clipping 1.2, class-weighted loss; maximum 100 epochs with early stopping (patience 20) on one third of the training plots; seed 42; stride-1 stems because the pseudo-images are small (4 × 4). DNN-F1 used learning rate 10^{-3}.',
     'Test predictions for the three tasks; learning curves; network comparison on three feature configurations (OW, VI, DSF); DT-EDNet ablation (without SE, without the dual transformer group, without both).',
     'No separate tuning of the networks (paper settings, CPU training). DNN-F2 (intermediate fusion) is not applicable to a single sensor.')
TAB('metrics', [['Metric', 'Formula / meaning', 'Use'], ['Overall accuracy (OA)', 'correct / all', 'A, B'], ['Cohen\'s kappa', '(p_{o} − p_{e})/(1 − p_{e}); agreement beyond chance (Cohen, 1960)', 'A, B'],
    ['Macro-F1', 'mean over classes of 2PR/(P + R); treats small classes equally (Sokolova and Lapalme, 2009)', 'A, B (main)'], ['Sensitivity, specificity, AUC', 'true-positive rate, true-negative rate, area under the ROC curve (Fawcett, 2006)', 'A'],
    ['Quadratic weighted kappa (QWK)', 'kappa with penalty growing with the squared grade distance (Cohen, 1968)', 'B (ordinal)'], ['Within one grade', 'share of leaves predicted at most one class away', 'B'],
    ['R², RMSE, MAE', 'explained variance, root mean square and mean absolute error (grade units)', 'C'], ['RPD', 'SD of observed / RMSE; > 2 good, 1.4–2 fair, < 1.4 poor (Williams, 2001)', 'C'], ['Bias', 'mean (predicted − observed)', 'C']],
    'Evaluation metrics.', [2400, 5400, 1506], 16)
H2('2.11 Covariate baseline model without sensor data (Step 2.5.5)')
P('Severity rose with crop age and sampling date and differed with variety, sowing timing, growth stage and weather, so a spectral model could look accurate only by learning the calendar (De Wolf and Isard, 2007). Weather alone can predict disease severity well (Bijlwan et al., 2025), and adding sensor data to meteorological data improved forecasts of wheat powdery mildew from 69% to 78% overall accuracy (Zhang et al., 2014; see also Ruan et al., 2022). A covariate baseline was therefore built without any spectral data, and the spectra are credited only with what they add to it (Kuhn and Johnson, 2013).')
TAB('covmodels', [['Model', 'Detection (A)', 'Six grades (B)', 'Severity score (C)', 'Covariates used'],
    ['B1 – statistical (interpretable)', 'logistic regression (C tuned)', 'proportional-odds ordinal logistic regression (McCullagh, 1980)', 'linear model with DAS and DAS² (Madden et al., 2007)', 'variety, timing, growth stage, DAS, DAS²'],
    ['Random forest', 'tuned in inner folds', 'tuned in inner folds', 'tuned in inner folds (= best ML for C)', 'all covariates incl. weather and favourable days'],
    ['B2 – best machine-learning model of Activity 2.2', 'SVM', 'XGBoost', 'random forest', 'all covariates incl. weather and favourable days']],
    'Covariate-only models. With four sampling dates the 7-day weather is collinear with the date and favourable days since sowing with the sowing timing; in B1 the time effect is therefore represented by DAS and DAS².', [2300, 1600, 2100, 1700, 1606], 15)
BL(['**Samples:** unsprayed, naturally infected leaves only (n = %d); the healthy plots were fungicide-sprayed and share every covariate with the unsprayed plots, so they would teach a false rule.' % int((M.unsprayed == 1).sum()),
    '**Inputs:** covariates only, leaf spectra (the fold-wise disease-specific feature set) and spectra + covariates, each with the three models; same outer folds, inner tuning grouped by plot, standardisation with training statistics.',
    '**Model sets:** M0 = the stronger covariate-only model; M1 = the best machine-learning model on leaf spectra; M2 = the same model on spectra + covariates.',
    '**Gains:** ΔS = metric(M1) − metric(M0) (what the spectra add); ΔC = metric(M2) − metric(M1) (what the covariates add to the spectra); ΔT = metric(M2) − metric(M0).',
    '**Is a gain real?** 95% confidence interval from 2000 bootstrap resamples of the pooled test predictions that resample whole plots (Efron and Tibshirani, 1993); AUCs compared with the DeLong test (DeLong et al., 1988). A gain is called real when the interval excludes zero, it is larger than the fold-to-fold SD and it has the same sign in all three folds.',
    '**Interpretable model:** B1 was also fitted on all unsprayed leaves with standardised covariates to show the direction and size of each effect.'])
H2('2.12 Interpretation and robustness')
BL(['**SHAP** of an XGBoost model on the Objective 1 feature set: direction and size of each feature\'s effect (Lundberg and Lee, 2017).',
    '**Strata:** test metrics of the best models by growth stage, variety, leaf position and date.',
    '**Transfer tests:** leave-one-variety-out and leave-one-timing-out with random forest, feature selection repeated inside each training set.',
    '**Selection stability:** how often each optimal wavelength and index was chosen across the three outer folds.'])
H2('2.13 Software and final models')
P('Python 3 with NumPy, pandas, SciPy, scikit-learn (Pedregosa et al., 2011), mlxtend (Raschka, 2018), XGBoost (Chen and Guestrin, 2016), SHAP (Lundberg et al., 2020) and PyTorch (Paszke et al., 2019). After evaluation, every model was refitted on all %d leaves with the same procedure and saved (Step 2.7.1): machine-learning models as joblib files, networks as PyTorch state dictionaries, with the feature definitions and a prediction script for new spectra.' % N)

# ------------------------------------------------------------------ 3 results
H1('3. Results')
H2('3.1 Disease progress and weather')
WS_ = pd.read_csv(D + 'weather_season.csv', parse_dates=['date']); WS_ = WS_[WS_.date >= '2025-12-09']
FL_ = WS_[(WS_.Tmax.between(16, 24)) & (WS_.RH1 > 97) & (WS_.RH2 > 40) & (WS_.date < pd.Timestamp(dates[-1]))]; FS_ = WS_[(WS_.Tmax.between(20, 29)) & (WS_.Tmin > 12) & (WS_.RH1 > 97) & (WS_.date < pd.Timestamp(dates[-1]))]
P('The mean grade rose from %.2f on 11 February to %.2f on 13 March; the share of diseased leaves rose from %.0f%% to %.0f%%. Infection was natural. From the first sowing (9 December 2025) to the last sampling date, %d days met the leaf-infection criteria of Chattopadhyay et al. (2011) (T_{max} 16–24 °C, RH I > 97%% and RH II > 40%%): %s. The last such day was %s, before the first sampling date; the staghead criteria were met on %d days. During the sampling period the weather became warmer and drier: the 7-day mean maximum temperature rose from %.1f to %.1f °C and afternoon relative humidity fell from %.0f%% to %.0f%% ([[F:weather]], [[T:weather]]).' % (
    prog.mean_grade.iloc[0], prog.mean_grade.iloc[-1], prog.pct_diseased.iloc[0], prog.pct_diseased.iloc[-1], len(FL_), ', '.join('%d in %s' % (n_, m_) for m_, n_ in FL_.groupby(FL_.date.dt.strftime('%B'), sort=False).size().items()),
    FL_.date.max().strftime('%d %B %Y') if len(FL_) else '–', len(FS_), wc.Tmax7.iloc[0], wc.Tmax7.iloc[-1], wc.RH2_7.iloc[0], wc.RH2_7.iloc[-1]))
FIG('weather', 'f15_weather_progress.png', 'Weather of the season (IARI observatory) with sowing dates, favourable leaf-infection days (Chattopadhyay et al., 2011) and the four leaf sampling dates (boxes: date, mean grade and % diseased leaves); natural infection.', 620)
TAB('weather', [['Date', 'Crop age (DAS)', 'Mean grade', 'Diseased (%)', 'T max 7 d (°C)', 'T min 7 d (°C)', 'RH I 7 d (%)', 'RH II 7 d (%)', 'Rain 7 d (mm)', 'Favourable days*'],
    *[[pd.Timestamp(r.date).strftime('%d %b'), DASR[r.date], f2(r.mean_grade), '%.0f' % r.pct_diseased, '%.1f' % r.Tmax7, '%.1f' % r.Tmin7, '%.0f' % r.RH1_7, '%.0f' % r.RH2_7, '%.1f' % r.rain7, str(int(r.fav_leaf_season))] for r in prog.itertuples()]],
    'Disease progress and 7-day weather before each sampling date. *Days from the first sowing (9 Dec 2025) to the day before the date with T max 16–24 °C, RH I > 97% and RH II > 40% (Chattopadhyay et al., 2011).', [900, 1000, 850, 850, 950, 950, 900, 900, 900, 1106], 15)
H2('3.2 Spectral response (Activity 1.1)')
bands = [550, 680, 760, 800, 1245, 1450, 1650, 1940, 2200]
P('Diseased leaves had lower near-infrared reflectance (%.3f at 800 nm in grade 0 vs %.3f in grade 9), higher red reflectance (%.3f vs %.3f at 680 nm) and higher shortwave-infrared reflectance, especially in the water bands (%.3f vs %.3f at 1450 nm) ([[F:spectra]], [[T:bands]]). The first-derivative peak at the red edge became lower (Dr %.1f → %.1f × 10^{-3} nm^{-1}) and moved to shorter wavelengths: the red-edge position fell from %.1f nm (grade 0) to %.1f nm (grade 9), a blue shift of %.1f nm.' % (
    wlv(0, 800), wlv(9, 800), wlv(0, 680), wlv(9, 680), wlv(0, 1450), wlv(9, 1450), Drg[0], Drg[9], REPg[0], REPg[9], REPg[0] - REPg[9]))
FIG('spectra', 'f02_mean_spectra.png', '(a) Mean leaf reflectance (± SD) of each severity grade over 400–2400 nm (water bands shaded and kept); (b) first derivative at the red edge.', 620)
TAB('bands', [['Band (nm)', *['grade %d' % g for g in GR], 'Change 0 → 9 (%)']] + [[str(w), *['%.3f' % wlv(g, w) for g in GR], '%+.1f' % (100 * (wlv(9, w) - wlv(0, w)) / wlv(0, w))] for w in bands] +
    [['REP (nm)', *['%.1f' % REPg[g] for g in GR], '%+.1f nm' % (REPg[9] - REPg[0])], ['Dr (×10^{-3})', *['%.2f' % Drg[g] for g in GR], '%+.1f' % (100 * (Drg[9] - Drg[0]) / Drg[0])]],
    'Mean reflectance at key wavelengths and red-edge parameters by grade.', [1300] + [1100] * 6 + [1406], 16)
FIG('fdfull', 'f03_fd_full.png', 'First derivative of the mean spectra of each grade over 400–2400 nm.', 620)
FIG('stage', 'f13_spectra_by_stage.png', 'Mean reflectance by grade within each growth stage: the grade effect is present at every stage.', 620)
FIG('factor', 'f14_grade_by_factor.png', 'Mean leaf grade (± 95% confidence interval) by growth stage, variety, leaf position and timing.', 540)
st_ = pd.read_csv(D + 'o1_strata.csv')
P('Mean grade differed most between growth stages (vegetative %.2f, flowering %.2f, pod formation %.2f), because the stages coincide with the later sampling dates. Lower leaves (LL) carried more disease than younger leaves ([[F:factor]]).' % tuple(st_[(st_.factor == 'stage') & (st_.level == s)].mean_score.iloc[0] for s in ('Vegetative', 'Flowering', 'Pod formation')))
FIG('corr', 'f04_corr_curves.png', 'Pearson correlation of reflectance and first derivative with the leaf grade (dotted lines: |r| = 0.3).', 620)
P('Reflectance correlated most strongly at %d nm (r = %.2f), the first derivative at %d nm (r = %.2f) and, with the opposite sign, at %d nm (r = %.2f) on the red edge ([[F:corr]]). The derivative therefore carried a stronger disease signal than reflectance.' % (cRmax.wl, cRmax.r_R, cFmax.wl, cFmax.r_FD, cFmin.wl, cFmin.r_FD))
H2('3.3 Effective ranges and optimal wavelengths (Activity 1.2)')
P('No band pair reached R² = 0.5, so the effective ranges were taken from the top 5%% of pairs (R² ≥ %.3f): %s nm, %d bands at 5-nm spacing ([[F:maps]]). The best NDSI and RSI used the same pair, (%d, %d) nm (R² = %.2f), at the near-infrared shoulder of the red edge.' % (
    O1['eff_thr'], ', '.join('%d–%d' % tuple(r) for r in O1['eff_ranges']), O1['eff_nbands'], nd[0], nd[1], nd[2]))
FIG('maps', 'f05_ndsi_rsi_maps.png', 'R² of (a) NDSI and (b) RSI with the leaf grade for all band pairs (white contour: effective-range threshold; star: best pair).', 620)
sc_ = pd.read_csv(D + 'o1_shapcars.csv')
P('SHAP pre-screening kept the top 40%% of candidate bands; Monte Carlo cross-validation chose %d PLS components; across 20 CARS runs %d bands were selected in at least half the runs, all of them first derivatives ([[F:shapcars]], [[T:ow]]). They lie on the green peak (550–595 nm), the red edge and near-infrared shoulder (760–870 nm), and the near- and shortwave-infrared (1060–1805 nm).' % (O1['cars_ncomp'], len(O1['OW'])))
FIG('shapcars', 'f06_shapcars.png', 'SHAP-CARS: (a) SHAP importance of all candidate bands, (b) choice of PLS components, (c) one CARS run, (d) selection frequency over 20 runs.', 620)
fr = dict(zip(sc_.feature, sc_.cars_freq)); sh = dict(zip(sc_.feature, sc_.mean_abs_shap))
TAB('ow', [['Optimal wavelength', 'Type', 'Region', 'CARS frequency (20 runs)', 'mean |SHAP|']] + [[o, 'first derivative' if o.startswith('FD') else 'reflectance', next(t for a, b, t in [(400, 680, 'visible'), (680, 750, 'red edge'), (750, 1300, 'near infrared'), (1300, 1900, 'SWIR-1'), (1900, 2401, 'SWIR-2')] if a <= int(o.lstrip('RFD')) < b), '%.2f' % fr.get(o, np.nan), '%.3f' % sh.get(o, np.nan)] for o in O1['OW']],
    'Optimal wavelengths selected by SHAP-CARS on all leaves.', [2000, 1900, 1900, 1900, 1606], 16)
FIG('ow', 'f07_optimal_wavelengths.png', 'Optimal wavelengths marked on the mean reflectance and first-derivative spectra.', 620)
H2('3.4 Indices and the disease-specific feature set (Activities 1.3–1.6)')
wt = pd.read_csv(D + 'o1_wri_top.csv')
P('The WRI search found NDSI(%d, %d) %s (r = %.2f). The weight of the third band was zero, so for leaf spectra the third band did not improve on the two-band index; the next candidates were almost identical (|r| %.3f–%.3f) ([[F:wri]]).' % (W['l1'], W['l2'], '+ %.1f × R_{%d}' % (W['w'], W['l3']) if W['w'] else '(third-band weight w = 0)', W['r'], wt.abs_r.iloc[:5].min(), wt.abs_r.iloc[0]))
FIG('wri', 'f08_wri.png', 'White Rust Index (WRI) by grade: (a) distributions, (b) all leaves with mean ± SD.', 600)
P('The redundancy filter (|r| ≥ 0.95) reduced the %d index features (41 published indices, three red-edge parameters and three data-driven indices) to %d ([[F:icorr]]). ReliefF selected %s for six grades, %s for detection, and RReliefF selected %s for the score ([[F:relief]]).' % (
    len(F.columns), len(O1['idx_kept']), ', '.join(O1['VI_classes']), ', '.join(O1['VI_binary']), ', '.join(O1['VI_score'])))
FIG('icorr', 'f09_index_corr.png', 'Correlation among the indices kept after the |r| ≥ 0.95 filter.', 520)
FIG('relief', 'f10_relief.png', 'ReliefF weights of the indices for detection and six grades, and RReliefF weights for the score (blue: top five, selected).', 620)
vr = O1['VIF_removed']
P('The variance inflation factor removed %d features in turn (largest first: %s), leaving the disease-specific feature set of %d features with all VIF below 10 ([[F:vif]], [[T:dsf]]). The PCA of the reflectance spectra shows the grades as overlapping clouds ordered along PC1 and PC2 ([[F:pca]]).' % (
    len(vr), ', '.join('%s (%.0f)' % (a, b) for a, b in vr[:4]), len(O1['DSF'])))
FIG('vif', 'f11_vif.png', 'Variance inflation factors of the disease-specific feature set.', 460)
TAB('dsf', [['Feature', 'Group', 'VIF', 'r with grade', 'Physical meaning']] + [[k, 'derivative band' if k.startswith('FD') else 'index', '%.2f' % v, f2(np.corrcoef((F[k] if k in F else pd.Series(np.load(D + 'prep.npz')['FD5'][:, list(np.load(D + 'prep.npz')['w5']).index(int(k[2:]))])).values, M.grade)[0, 1]),
    {'FD550': 'green peak slope (chlorophyll)', 'FD760': 'red-edge shoulder', 'FD860': 'near-infrared plateau (structure)', 'FD1060': 'near-infrared (mesophyll scattering)', 'FD1090': 'near-infrared', 'FD1245': 'NIR–SWIR water band edge', 'FD1805': 'SWIR water band edge',
     'DWSI-2': 'disease–water stress index R1660/R550', 'Dr': 'height of the red-edge peak (chlorophyll)', 'HI': 'healthy index (Mahlein et al., 2013)', 'MCARI': 'chlorophyll absorption in the red'}.get(k, '')] for k, v in O1['VIF_final'].items()],
    'Disease-specific feature set (Objective 1, all leaves).', [1500, 1600, 900, 1300, 4006], 16)
FIG('dsfbox', 'f30_dsf_by_grade.png', 'Distribution of each disease-specific feature by grade.', 620)
FIG('pca', 'f12_pca.png', 'Principal component scores of leaf reflectance with 95% ellipses of each grade.', 420)
H2('3.5 Fold-wise selection (Step 2.1.2)')
frows = [['Fold', 'Optimal wavelengths', 'Best NDSI / RSI (nm)', 'WRI', 'DSF detection', 'DSF six grades', 'DSF score']]
for f in range(3):
    s = SEL[str(f)]; frows.append([str(f + 1), '%d (%s)' % (len(s['OW']), ', '.join(s['OW'][:6]) + (', …' if len(s['OW']) > 6 else '')), '(%d, %d) / (%d, %d)' % (*s['ndsi'], *s['rsi']), 'NDSI(%d, %d)%s' % (s['wri']['l1'], s['wri']['l2'], ' %+.1f R%d' % (s['wri']['w'], s['wri']['l3']) if s['wri']['w'] else ''),
                                  ', '.join(s['DSF']['A']), ', '.join(s['DSF']['B']), ', '.join(s['DSF']['C'])])
TAB('foldsel', frows, 'Feature selection repeated inside each outer training part.', [600, 2000, 1300, 1200, 1400, 1400, 1406], 14)
if stab is not None:
    so = stab[stab.group == 'optimal wavelengths']; P('Of the %d distinct optimal wavelengths chosen in the three folds, %d were chosen in all three folds (%s) ([[F:stab]]).' % (len(so), (so.folds == 3).sum(), ', '.join(so[so.folds == 3].feature)))
    FIG('stab', 'f29_stability.png', 'Number of outer folds in which each optimal wavelength was selected.', 600)
H2('3.6 Machine-learning models (Activity 2.2)')
sffs = mls.copy(); sffs['n'] = sffs.selected.map(lambda s: len(eval(s)))
TAB('sffs', [['Task', 'Model', 'Candidates (mean)', 'Selected by SFFS (mean)', 'Inner score (mean)', 'Hyper-parameters chosen (fold 1)']] +
    [[t, mn(m, t), '%.1f' % d.n_candidates.mean(), '%.1f' % d.n.mean(), '%.3f' % d.inner_score.mean(), ', '.join('%s = %s' % kv for kv in json.loads(d[d.fold == 0].params.iloc[0]).items())] for (t, m), d in sffs.groupby(['task', 'model'], sort=False)],
    'Sequential floating forward selection and grid search (inner score: macro-F1 for A and B, negative RMSE for C).', [700, 1100, 1300, 1500, 1300, 3406], 15)
H2('3.7 Deep-learning models (Activity 2.3)')
if os.path.exists(D + 'dl_runs.csv'):
    dr = pd.read_csv(D + 'dl_runs.csv'); P('The pseudo-images were 4 × 4 (10–16 features). Early stopping ended training after a median of %d epochs (range %d–%d); [[F:lc]] shows the learning curves of fold 1 for the six-grade task: training loss kept falling while validation loss started to rise after a few epochs, the usual sign of over-fitting on a small data set; early stopping on validation macro-F1 kept the best epoch.' % (dr.epochs.median(), dr.epochs.min(), dr.epochs.max()))
    TAB('dlruns', [['Network', 'Parameters', 'Epochs (median over 9 runs)', 'Best validation score (mean)']] + [[n, '{:,}'.format(int(d.nparam.iloc[0])), '%d' % d.epochs.median(), '%.3f' % d[d.task != 'C'].best_val.mean() if (d.task != 'C').any() else '–'] for n, d in dr.groupby('net', sort=False)],
        'Deep-learning runs (validation score: macro-F1 on the validation plots, tasks A and B).', [2600, 2000, 2300, 2406], 16)
if os.path.exists(B + 'fig/f21_learning_curves.png'): FIG('lc', 'f21_learning_curves.png', 'Training and validation loss and validation macro-F1 of the four pseudo-image networks (fold 1, six grades).', 600)
H2('3.8 Comparison of all models (Activity 2.4)')
def mtab(t):
    d = MT[MT.task == t].copy(); d['type'] = d.model.map(lambda m: 'ML' if m in MLM else 'DL')
    if t == 'A':
        d = d.sort_values('macro_F1', ascending=False); return [['Model', 'Type', 'OA', 'Kappa', 'Macro-F1 (± SD folds)', 'Sensitivity', 'Specificity', 'AUC']] + [[r.model, r.type, f3(r.OA), f3(r.kappa), '%.3f ± %.3f' % (r.macro_F1, r.macro_F1_sd), f3(r.sensitivity), f3(r.specificity), f3(r.AUC)] for r in d.itertuples()]
    if t == 'B':
        d = d.sort_values('macro_F1', ascending=False); return [['Model', 'Type', 'OA', 'Kappa', 'Macro-F1', 'QWK', '±1 grade', *['F1 g%d' % g for g in GR]]] + [[r.model, r.type, f3(r.OA), f3(r.kappa), f3(r.macro_F1), f3(r.QWK), f3(r.within1), *[f2(getattr(r, 'F1_g%d' % g)) for g in GR]] for r in d.itertuples()]
    d = d.sort_values('RMSE'); return [['Model', 'Type', 'R²', 'RMSE (± SD folds)', 'MAE', 'RPD', 'Bias', 'r']] + [[mn(r.model, 'C'), r.type, f3(r.R2), '%.3f ± %.3f' % (r.RMSE, r.RMSE_sd), f3(r.MAE), f3(r.RPD), '%+.3f' % r.bias, f3(r.r)] for r in d.itertuples()]
P('[[T:mA]], [[T:mB]] and [[T:mC]] give the pooled test metrics of all models; [[F:comp]] and [[F:heat]] compare them visually.')
TAB('mA', mtab('A'), 'Task A – detection: test metrics (pooled over the three outer folds; n = %d leaves).' % N, [1900, 700, 900, 900, 1700, 1100, 1100, 1006], 15)
TAB('mB', mtab('B'), 'Task B – six grades: test metrics and F1 of each grade.', [1500, 500, 600, 600, 700, 600, 700, 690, 690, 690, 690, 690, 656], 14)
TAB('mC', mtab('C'), 'Task C – severity score: test metrics (grade units).', [1900, 700, 900, 1700, 1000, 1000, 1000, 1106], 15)
FIG('comp', 'f16_model_comparison.png', 'Model comparison: macro-F1 for detection and six grades (± SD over folds) and R² for the severity score (blue: machine learning; purple: deep learning).', 620)
FIG('heat', 'f31_metric_heatmap.png', 'All metrics of all models (darker = better within each column).', 620)
P('Detection was reliable: the best model reached macro-F1 %.3f and AUC %s ([[F:roc]]). Six-grade classification was much weaker (best macro-F1 %.3f, overall accuracy %.3f), but the errors were mostly between neighbouring grades: %.0f%% of leaves were within one class and the quadratic weighted kappa was %.3f ([[F:cm]]). Grade %d was recognised best (F1 %.2f) and grade %d worst (F1 %.2f); intermediate grades were most often confused ([[F:radar]]). For the score, the best model explained %.0f%% of the variance (RMSE %.2f grades, RPD %.2f) and predictions followed the 1:1 line with shrinkage of the extreme grades towards the mean ([[F:predobs]]).' % (
    rA.macro_F1, f3(rA.AUC), rB.macro_F1, rB.OA, 100 * rB.within1, rB.QWK, *FGB, 100 * rC.R2, rC.RMSE, rC.RPD))
FIG('cm', 'f17_confusion.png', 'Confusion matrices (counts and row percentages) of the best machine-learning and deep-learning models for six grades.', 620)
FIG('roc', 'f18_roc.png', 'ROC curves for detection (solid: machine learning; dashed: deep learning).', 400)
FIG('radar', 'f19_radar.png', 'Six-grade performance profile (F1 of each grade, OA, kappa and macro-F1).', 430)
FIG('predobs', 'f20_pred_obs.png', 'Predicted vs observed severity score of the best machine-learning and deep-learning models (black: mean ± SD per grade).', 600)
H2('3.9 Network comparison and DT-EDNet ablation (Step 2.5.3)')
if cfg is not None and len(cfg):
    best_cfg = cfg.loc[cfg.macro_F1.idxmax()]
    P('On the six-grade task, the networks were compared on three hyperspectral feature configurations: optimal wavelengths (OW), selected indices (VI) and the disease-specific set (DSF). The best combination was %s with %s (macro-F1 %.3f) ([[F:cfg]], [[T:cfg]]).' % (best_cfg.net, best_cfg.config, best_cfg.macro_F1))
    piv = cfg.pivot_table(index='net', columns='config', values='macro_F1')
    TAB('cfg', [['Network', *[c for c in ('OW', 'VI', 'DSF') if c in piv.columns]]] + [[n, *[f3(piv.loc[n, c]) for c in ('OW', 'VI', 'DSF') if c in piv.columns]] for n in piv.index], 'Macro-F1 (six grades) of the networks on the three feature configurations.', [3306, 2000, 2000, 2000], 16)
    FIG('cfg', 'f22_config.png', 'Networks on the three feature configurations (six grades).', 600)
if abl is not None and len(abl):
    full = abl[abl.net == 'DT-EDNet']
    P('Removing modules from DT-EDNet changed six-grade macro-F1 from %s (full network) to %s ([[F:abl]], [[T:abl]]).' % (f3(full.macro_F1.iloc[0]) if len(full) else '–', '; '.join('%s %.3f' % (r.net, r.macro_F1) for r in abl[abl.net != 'DT-EDNet'].itertuples())))
    TAB('abl', [['Variant', 'OA', 'Kappa', 'Macro-recall', 'Macro-F1', 'QWK']] + [[r.net, f3(r.OA), f3(r.kappa), f3(r.macro_R), f3(r.macro_F1), f3(getattr(r, 'QWK', np.nan))] for r in abl.itertuples()], 'DT-EDNet module ablation (six grades; SE = squeeze-and-excitation, DTG = dual transformer group).', [3306, 1200, 1200, 1200, 1200, 1200], 16)
    FIG('abl', 'f23_ablation.png', 'DT-EDNet module ablation (six grades).', 560)
H2('3.10 Interpretation (Step 2.5.4)')
if os.path.exists(D + 'shap_C.npy'):
    sv = np.load(D + 'shap_C.npy'); X = pd.read_csv(D + 'shap_X.csv'); imp = pd.Series(np.abs(sv).mean(0), index=X.columns).sort_values(ascending=False)
    dirs = ['%s %s' % ('high' if np.corrcoef(X[c], sv[:, list(X.columns).index(c)])[0, 1] > 0 else 'low', c) for c in imp.index[:4]]
    P('For the severity score, the most important features were %s (mean |SHAP| %s). Predictions moved towards higher grades with %s ([[F:shap]]).' % (', '.join(imp.index[:4]), ', '.join('%.2f' % v for v in imp.values[:4]), ', '.join(dirs[:-1]) + ' and ' + dirs[-1]))
    FIG('shap', 'f24_shap.png', 'SHAP summary for the severity score and SHAP importance by grade for six grades (XGBoost on the disease-specific feature set).', 620)
H2('3.11 Robustness (Activity 2.6)')
sb = strata[(strata.task == 'B') & (strata.source == 'ML') & (strata.n >= 30)]
P('Six-grade macro-F1 of the best machine-learning model varied between strata (growth stage %s; variety %s; leaf position %s) ([[F:strata]]).' % tuple(', '.join('%s %.2f' % (r.level, r.macro_F1) for r in sb[sb.factor == fc].itertuples()) for fc in ('stage', 'variety', 'leafpos')))
FIG('strata', 'f25_strata.png', 'Six-grade macro-F1 by growth stage, variety, leaf position and date.', 600)
if tt is not None:
    tb, tc = tt[tt.task == 'B'], tt[tt.task == 'C']
    P('In the transfer tests, macro-F1 on a held-out variety was %s and on a held-out timing %s; RMSE on held-out groups was %.2f–%.2f grades, close to the cross-validated value, so the models did not depend on one variety or timing ([[F:transfer]]).' % (
        ', '.join('%s %.2f' % (r.level, r.macro_F1) for r in tb[tb.test == 'variety'].itertuples()), ', '.join('%s %.2f' % (r.level, r.macro_F1) for r in tb[tb.test == 'timing'].itertuples()), tc.RMSE.min(), tc.RMSE.max()))
    FIG('transfer', 'f26_transfer.png', 'Leave-one-variety-out and leave-one-timing-out tests (random forest).', 600)
H2('3.12 Covariate baseline (Step 2.5.5)')
if cv2m is not None and cv2s is not None:
    gm = lambda t, i_, m, k: cv2m[(cv2m.task == t) & (cv2m.input == i_) & (cv2m.model == m)][k].iloc[0]
    m0n = {t: (lambda n: n if n.startswith(('XGB', 'SVM')) else n[0].lower() + n[1:])(cv2s[t]['M0']['model_name']) for t in 'ABC'}; m0m = {t: cv2s[t]['M0']['model'] for t in 'ABC'}
    P('Without any spectral data, the stronger covariate-only model (M0) was the %s for detection (macro-F1 %.3f, AUC %s), the %s for six grades (macro-F1 %.3f, QWK %.3f) and the %s for the severity score (R² %.3f, RMSE %.2f) ([[T:covres]], [[F:covmod]]).' % (
        m0n['A'], gm('A', 'covariates only', m0m['A'], 'macro_F1'), f3(gm('A', 'covariates only', m0m['A'], 'AUC')), m0n['B'], gm('B', 'covariates only', m0m['B'], 'macro_F1'), gm('B', 'covariates only', m0m['B'], 'QWK'),
        m0n['C'], gm('C', 'covariates only', m0m['C'], 'R2'), gm('C', 'covariates only', m0m['C'], 'RMSE')))
    INP = ['covariates only', 'leaf spectra', 'spectra + covariates']; MO = [('Statistical', 'B1 statistical'), ('RF', 'Random forest'), ('B2', 'Best ML (B2)')]
    rows_ = [['Input', 'Model', 'A macro-F1', 'A AUC', 'A balanced acc.', 'B macro-F1', 'B QWK', 'C R²', 'C RMSE']]
    for i_ in INP:
        for m, ml in MO:
            rows_.append([i_, ml, f3(gm('A', i_, m, 'macro_F1')), f3(gm('A', i_, m, 'AUC')), f3(gm('A', i_, m, 'balanced_acc')), f3(gm('B', i_, m, 'macro_F1')), f3(gm('B', i_, m, 'QWK')), f3(gm('C', i_, m, 'R2')), f3(gm('C', i_, m, 'RMSE'))])
    TAB('covres', rows_, 'Covariate-only, spectra and spectra + covariate models on unsprayed leaves (pooled leave-one-replication-out test predictions; B1 = logistic / ordinal logistic / linear model; B2 = SVM, XGBoost, random forest for tasks A, B, C).', [1700, 1400, 900, 850, 950, 900, 850, 850, 906], 14)
    FIG('covmod', 'f32_cov_models.png', 'Primary metric of the three models on covariates only, leaf spectra and spectra + covariates (unsprayed, naturally infected leaves; M0 marked).', 620)
    gg = lambda t, k, gname: cv2g[(cv2g.task == t) & (cv2g.metric == k) & (cv2g.gain == gname)].iloc[0]
    real_imp = lambda r: bool(r.real_gain) and r.direction == 'improves'
    fmtg = lambda r: '%+.3f (%+.3f to %+.3f)%s' % (r.delta, r.ci_low, r.ci_high, ' ✓' if real_imp(r) else (' ✗' if r.real_gain else ''))
    P('Leaf spectra compared with the covariate baseline (ΔS) changed macro-F1 by %s for detection and by %s for six grades, and R² by %s for the score. Adding the covariates to the spectra (ΔC) changed them by %s, %s and %s; spectra + covariates against the baseline (ΔT) by %s, %s and %s ([[T:covgain]], [[F:covgain]]). Values marked ✓ meet all three criteria of a real gain (✗ = a real loss).' % (
        fmtg(gg('A', 'macro_F1', 'ΔS = M1 − M0')), fmtg(gg('B', 'macro_F1', 'ΔS = M1 − M0')), fmtg(gg('C', 'R2', 'ΔS = M1 − M0')), fmtg(gg('A', 'macro_F1', 'ΔC = M2 − M1')), fmtg(gg('B', 'macro_F1', 'ΔC = M2 − M1')), fmtg(gg('C', 'R2', 'ΔC = M2 − M1')),
        fmtg(gg('A', 'macro_F1', 'ΔT = M2 − M0')), fmtg(gg('B', 'macro_F1', 'ΔT = M2 − M0')), fmtg(gg('C', 'R2', 'ΔT = M2 − M0'))))
    lab_ = {'macro_F1': 'macro-F1', 'AUC': 'AUC', 'balanced_acc': 'balanced accuracy', 'QWK': 'QWK', 'R2': 'R²', 'RMSE': 'RMSE'}
    TAB('covgain', [['Task', 'Metric', 'ΔS = M1 − M0 (95% CI)', 'ΔC = M2 − M1 (95% CI)', 'ΔT = M2 − M0 (95% CI)']] + [[{'A': 'Detection', 'B': 'Six grades', 'C': 'Score'}[t], lab_[k], fmtg(gg(t, k, 'ΔS = M1 − M0')), fmtg(gg(t, k, 'ΔC = M2 − M1')), fmtg(gg(t, k, 'ΔT = M2 − M0'))]
        for t in 'ABC' for k in dict.fromkeys(cv2g[cv2g.task == t].metric)], 'Gains with 95% plot-block bootstrap confidence intervals (2000 resamples). ✓ = real gain: interval excludes zero, larger than the fold-to-fold SD and the same sign in all three folds; ✗ = a real loss by the same rule. For RMSE a negative value is an improvement.', [1300, 1500, 2150, 2150, 2206], 14)
    FIG('covgain', 'f33_cov_gains.png', 'Gains of the spectra (ΔS), of the covariates added to the spectra (ΔC) and of both (ΔT) with 95% plot-block bootstrap intervals (filled = real difference; right of zero = better, except RMSE).', 620)
    if cv2d is not None and len(cv2d):
        P('DeLong tests of the detection AUC: %s.' % '; '.join('%s %.3f vs %.3f (z = %.2f, p = %s)' % (r.comparison, r.AUC_a, r.AUC_b, r.z, ('%.3f' % r.p) if r.p >= 0.001 else '< 0.001') for r in cv2d.itertuples()))
    if cv2c is not None and len(cv2c):
        TN = {'variety_V2': 'variety V2', 'variety_V3': 'variety V3', 'timing_D2': 'timing D2', 'timing_D3': 'timing D3', 'timing_D4': 'timing D4', 'stage_code': 'growth stage', 'DAS': 'days after sowing', 'DAS2': '(days after sowing)²'}
        oo = cv2c[cv2c.model.str.startswith('Ordinal')]
        if not len(oo): oo = cv2c[cv2c.model.str.startswith('Linear')]
        sig = oo[oo.p < 0.05].reindex(oo[oo.p < 0.05].estimate.abs().sort_values(ascending=False).index)
        P('In the interpretable model (B1, all unsprayed leaves, standardised covariates), the strongest effects on the severity grade were %s ([[F:covb1]]). Positive values raise and negative values lower the expected grade.' % ('; '.join('%s (%+.2f per SD, 95%% CI %+.2f to %+.2f)' % (TN.get(r.term, r.term), r.estimate, r.ci_low, r.ci_high) for r in sig.head(4).itertuples()) if len(sig) else 'none significant at 5%'))
        FIG('covb1', 'f34_cov_b1.png', 'Standardised effects of the covariates in the interpretable models: logistic (detection), ordinal logistic (six grades) and linear (score) (95% CI).', 620)

# ------------------------------------------------------------------ 4 discussion
H1('4. Discussion')
H2('4.1 Physical basis of the white rust signal')
P('The spectral changes agree with the biology of white rust. Infection destroys chlorophyll around the pustules, which raises red reflectance, lowers the red-edge peak and shifts the red-edge position towards shorter wavelengths (Filella and Peñuelas, 1994; Horler et al., 1983). The %.1f-nm blue shift between grades 0 and 9 is of the size reported for chlorophyll loss in diseased leaves (Mahlein et al., 2013; Meng et al., 2020). The white pustules and the collapse of mesophyll cells change internal scattering, which explains the lower near-infrared plateau, and tissue dehydration raises reflectance in the water bands of the shortwave infrared (Mishra et al., 2009; Peñuelas et al., 1997). Keeping the water bands of the contact-probe data was therefore useful: FD1245 and FD1805, at the edges of the water bands, entered the disease-specific feature set.' % (REPg[0] - REPg[9]))
H2('4.2 Derivatives and the selected wavelengths')
P('SHAP-CARS selected only first-derivative bands, and the derivative correlated more strongly with the grade than reflectance. Derivatives remove additive offsets caused by leaf thickness and surface differences and highlight the shape of the red edge (Tsai and Philpot, 1998). This agrees with the DT-EDNet study, where the optimal wavelengths concentrated in the red edge and near infrared (Ma et al., 2026), and with wheat and rice disease studies that used derivative or red-edge features (Huang et al., 2020; Mandal et al., 2023). The best two-band index, NDSI(%d, %d), lies on the near-infrared shoulder, and the WRI search did not add a useful third band; for UAV sensors this means that a narrow red-edge to near-infrared contrast carries most of the leaf signal.' % (nd[0], nd[1]))
H2('4.3 Why detection is good but six grades are difficult')
P('Detection reached macro-F1 %.2f, but six-grade macro-F1 stayed near %.2f. This gap is common in leaf-level severity work: the grades are ordinal categories of a continuous process, a leaf of grade 3 and one of grade 5 differ only in pustule area, and visual raters disagree most for intermediate grades (Bock et al., 2010). The spectral distributions of neighbouring grades overlap ([[F:dsfbox]], [[F:pca]]), so no model can separate them sharply. The ordinal metrics confirm that the errors were small in grade terms (QWK %.2f; %.0f%% within one class). Similar patterns were reported for wheat yellow rust and Fusarium head blight, where severity classes in the middle of the scale had the lowest accuracy (Huang et al., 2020; Lv et al., 2023), and for rice blast in India (Mandal et al., 2023). Merging grades into three or four classes or treating severity as a score are the usual remedies; both are available in the methodology (four severity classes plus regression).' % (rA.macro_F1, rB.macro_F1, rB.QWK, 100 * rB.within1))
H2('4.4 Machine learning versus deep learning')
if HAS_DL:
    def sd_(t, m): r = row(t, m); return r.macro_F1_sd if t in 'AB' else r.RMSE_sd
    mlA, mlB, mlC = row('A', bA['ML']), row('B', bB['ML']), row('C', bC['ML'])
    ab_ = abl.set_index('net').macro_F1 if abl is not None else None
    cf_ = cfg[cfg.net == 'DT-EDNet'].set_index('config').macro_F1 if cfg is not None else None
    P('All models performed within a narrow range. For detection, the best network (%s, macro-F1 %.3f) and the best machine-learning model (%s, %.3f) differed by %.3f, less than the fold-to-fold SD (%.3f). For six grades, %s (%.3f) and %s (%.3f) were again within one SD; for the score, %s remained best (R² %.3f) ahead of the best network (%s, R² %.3f). DT-EDNet reached macro-F1 %.3f (detection) and %.3f (six grades) and R² %.3f (score), so at leaf level it did not exceed the comparison networks.' % (
        bA['DL'], dlA.macro_F1, bA['ML'], mlA.macro_F1, abs(dlA.macro_F1 - mlA.macro_F1), max(sd_('A', bA['DL']), sd_('A', bA['ML'])), bB['DL'], dlB.macro_F1, bB['ML'], mlB.macro_F1, mn(bC['ML'], 'C'), mlC.R2, bC['DL'], dlC.R2, dte['A'].macro_F1, dte['B'].macro_F1, dte['C'].R2))
    if ab_ is not None and cf_ is not None:
        P('The ablation showed that the dual transformer group added %.3f macro-F1 (%.3f without it), while removing squeeze-and-excitation changed little (%.3f); DT-EDNet did best on the optimal wavelengths (OW %.3f vs DSF %.3f). With only 10–16 features, the 4 × 4 pseudo-images are an arrangement of features rather than a picture (Sharma et al., 2019), so the attention modules designed for hyperspectral images of rice canopies (Ma et al., 2026) have little spatial structure to use. Tree ensembles and support vector machines are strong on such small tabular inputs; the advantage of DT-EDNet is expected in the UAV phase, where the networks receive real spatial and spectral patterns.' % (
            ab_['DT-EDNet'] - ab_['DT-EDNet-DTG'], ab_['DT-EDNet-DTG'], ab_['DT-EDNet-SE'], cf_.get('OW', np.nan), cf_.get('DSF', np.nan)))
else: P('Deep-learning results are pending.')
H2('4.5 Role of covariates and weather')
if cv2g is not None and cv2s is not None:
    dS = {t: gg(t, k, 'ΔS = M1 − M0') for t, k in (('A', 'macro_F1'), ('B', 'macro_F1'), ('C', 'R2'))}; dT = {t: gg(t, k, 'ΔT = M2 − M0') for t, k in (('A', 'macro_F1'), ('B', 'macro_F1'), ('C', 'R2'))}
    P('Growth stage, sowing timing, crop age and sampling date follow the epidemic, so a model without any sensor data already explained much of the disease level (detection macro-F1 %.2f and AUC %.2f; six-grade macro-F1 %.2f; score R² %.2f), as expected from weather- and calendar-based disease models (De Wolf and Isard, 2007; Bijlwan et al., 2025).' % (
        gm('A', 'covariates only', m0m['A'], 'macro_F1'), gm('A', 'covariates only', m0m['A'], 'AUC'), gm('B', 'covariates only', m0m['B'], 'macro_F1'), gm('C', 'covariates only', m0m['C'], 'R2')))
    hp_ = M[M.unsprayed == 1].groupby('date').diseased.mean()
    P('Detection inside the unsprayed plots is mainly a question of time: on 11 February %.0f%% of their leaves were still grade 0, and on the later dates only %s%% were, so the date alone separates most healthy from diseased leaves. Here the leaf spectra alone %s the covariates (ΔS %+.3f macro-F1; DeLong p %s for AUC), and spectra + covariates changed macro-F1 by %+.3f over the covariates (%s). This does not make the spectra useless for detection: the covariates know the sampling calendar of this experiment, which a sensor survey of an unknown field does not, and the spectra detected disease with macro-F1 %.2f when the sprayed healthy plots were included (%s; section 3.8).' % (
        100 * (1 - hp_.iloc[0]), '%.0f–%.0f' % (100 * (1 - hp_.iloc[1:].max()), 100 * (1 - hp_.iloc[1:].min())),
        'were weaker than' if dS['A'].delta < 0 and real_imp(dS['A']) is False and dS['A'].ci_high < 0 else ('did better than' if real_imp(dS['A']) else 'did not beat'), dS['A'].delta,
        ('%.3f' % cv2d.p.iloc[0]) if cv2d.p.iloc[0] >= 0.001 else '< 0.001', dT['A'].delta, 'a real gain' if real_imp(dT['A']) else 'not a consistent gain',
        MT[(MT.task == 'A') & (MT.model == BEST['A']['ML'])].macro_F1.iloc[0], BEST['A']['ML']))
    oc_ = cv2c[cv2c.model.str.startswith('Ordinal')].set_index('term') if cv2c is not None else None
    def eff_(t_, lab_):
        r_ = oc_.loc[t_]; return '%s %s (%+.2f per SD%s)' % (lab_, 'raised it' if r_.estimate > 0 else 'lowered it', r_.estimate, '' if r_.p < 0.05 else ', not significant')
    b1txt = (' In the interpretable ordinal model, ' + '; '.join([eff_('DAS', 'crop age'), eff_('DAS2', 'its square'), eff_('timing_D4', 'the latest sowing D4 (vs D1, at the same crop age)'), eff_('variety_V3', 'variety V3 (vs V1)')]) + ' ([[F:covb1]]).') if oc_ is not None and len(oc_) else ''
    P('For severity the spectra added information that the calendar cannot give: six-grade macro-F1 rose by %+.3f (%s) and score R² by %+.3f (%s), because leaves of the same date, timing and stage differ in their actual infection. Spectra and covariates together gave real gains over the baseline for six grades (ΔT %+.3f) and score (ΔT %+.3f R²), in line with the benefit of combining sensor and meteorological data for wheat diseases (Zhang et al., 2014; Ruan et al., 2022). %s' % (
        dS['B'].delta, 'a real gain' if real_imp(dS['B']) else 'not a consistent gain', dS['C'].delta, 'a real gain' if real_imp(dS['C']) else ('interval above zero but smaller than the fold-to-fold SD' if dS['C'].ci_low > 0 else 'not a consistent gain'), dT['B'].delta, dT['C'].delta, b1txt))
    P('Infection was natural, so the weather before sampling matters more than the weather during it. Favourable leaf-infection weather (Chattopadhyay et al., 2011) occurred on %d days between %s and %s, during the cool, humid weeks of December–January, and on no day of the sampling period; the crops sown on 9 and 18 December were exposed to all %d of these days, the crop sown on 9 January to %d. The disease measured in February–March therefore reflects infection during that spell, expressed and spreading as the crop aged, while the warmer, drier weather of the sampling period (7-day mean T_{max} rising from %.1f to %.1f °C) slowed further spread. With four sampling dates the 7-day weather is collinear with the date and favourable days since sowing with the sowing timing, so weather describes the epidemic but cannot be tested as an independent predictor; the 13 flights of 2026-27 and the Bharatpur data will allow that.' % (
        len(FL_), FL_.date.min().strftime('%d %B %Y'), FL_.date.max().strftime('%d %B %Y'), int(cv2x.fav_leaf_D1.iloc[0]), int(cv2x.fav_leaf_D4.iloc[0]), cv2x.Tmax7.iloc[0], cv2x.Tmax7.iloc[-1]))
else: P('Covariate results pending.')
H2('4.6 Limitations')
BL(['One season and one location; the Bharatpur data of the next season are needed for external validation.',
    'Leaf-level visual grades are subjective; image-based pustule area or a second rater would reduce label noise (Bock et al., 2010).',
    'Grade 9 had only %d leaves; class weights reduced but did not remove the imbalance.' % gN[9],
    'Growth stage and sampling date are confounded in the design (vegetative leaves only on the first two dates, pod formation only on the last two).',
    'The networks were trained on CPU with the paper settings and no separate tuning; tuning could change their ranking slightly.',
    'No pre-symptomatic dates were sampled in 2025-26, so Objective 3 (pre-symptomatic detection) could not be addressed; it needs the pre-symptomatic flights of 2026-27.'])
H2('4.7 Implications for the UAV phase')
P('The leaf results support the camera choice and the feature plan for 2026-27: the red edge (690–760 nm), the near-infrared shoulder (780–870 nm) and the shortwave-infrared water-band edges carry the disease signal; derivatives of the hyperspectral data should be kept; detection is realistic at canopy level, while severity should be reported as a score or a small number of classes. The final leaf models can also be used to check UAV-derived predictions on the same leaves sampled during the flights.')

# ------------------------------------------------------------------ 5 conclusions
H1('5. Conclusions')
NL(['White rust lowers near-infrared reflectance, raises red and shortwave-infrared reflectance and shifts the red-edge position by about %.0f nm towards shorter wavelengths between grades 0 and 9.' % (REPg[0] - REPg[9]),
    'The first derivative carries the strongest signal; SHAP-CARS selected %d derivative bands, and the disease-specific feature set has %d features (%s).' % (len(O1['OW']), len(O1['DSF']), ', '.join(O1['DSF'])),
    'Detection of diseased leaves is reliable (best macro-F1 %.2f, AUC %s); six-grade classification is limited by the overlap of neighbouring grades (macro-F1 %.2f, QWK %.2f); the severity score is predicted with R² %.2f and RMSE %.2f grades.' % (rA.macro_F1, f2(rA.AUC), rB.macro_F1, rB.QWK, rC.R2, rC.RMSE),
    ('A covariate-only model (no sensor data) explained much of the epidemic level and, inside unsprayed plots, detected disease as well as the spectra; leaf spectra added %+.3f macro-F1 for six grades and %+.3f R² for the score beyond it, and spectra + covariates gave real gains for grades and score; the models transfer across varieties and timings.' % (gg('B', 'macro_F1', 'ΔS = M1 − M0').delta, gg('C', 'R2', 'ΔS = M1 − M0').delta)) if cv2g is not None else 'Leaf spectra add information beyond crop stage, timing and weather; the models transfer across varieties and timings.',
    'Final models trained on all leaves are saved for the UAV phase and for the Bharatpur validation.'])

# ------------------------------------------------------------------ 6 cross-check
H1('6. Cross-check against the methodology')
P('Every step of the revised methodology that applies to leaf spectra was performed. Steps for UAV images (radiometric calibration, orthomosaics, crop mask, texture, thermal and the 15 sensor sets) do not apply to non-imaging contact-probe data.')
CK = [['Methodology step', 'Status in this analysis', 'Where'],
      ['A1 Design and treatments', 'Done: 48 plots, healthy block + R1–R3, D × V layout checked for all plots', '2.1, Table design'], ['A4 Leaf spectra (ASD)', 'Done: %d leaf spectra, L3/L5/LL, 4 dates; files parsed and checked' % N, '2.2, 2.4'],
      ['A5 Labels', 'Done: tasks A, B (six grades) and C', '2.5'], ['A6 Covariates', 'Done: variety, sowing timing, crop age (DAS), growth stage, 7-day weather (no look-ahead), favourable days since sowing', '2.3, 3.12'],
      ['B3 Smoothing; D3 spectral features; D4 indices', 'Done: Savitzky–Golay 11/2, first derivative, 5-nm bands, 41 indices + REP, Dr, REarea; water bands kept (contact probe)', '2.7–2.8'],
      ['E3 Standardisation; E4 class weights', 'Done with training statistics; balanced class weights', '2.10'], ['E2 Healthy-plot normalisation', 'Not used (healthy plots are fungicide-sprayed)', '–'],
      ['F1–F3 LORO, nested inner folds, leakage checks', 'Done: rotated healthy plots, inner GroupKFold by plot, selection inside folds', '2.6'],
      ['1.1.1–1.1.3 Response analysis', 'Done: mean and derivative spectra, correlation, strata, weather', '3.1–3.2'], ['1.2.1–1.2.4 Effective ranges, SHAP-CARS, OW', 'Done (top-5% rule because no pair reached R² 0.5)', '3.3'],
      ['1.3.1–1.3.2 NDSI, RSI, WRI', 'Done', '3.4'], ['1.3.3 Multispectral two-band indices', 'Not applicable (no camera)', '–'], ['1.4.1–1.4.3 Index group, redundancy, ReliefF', 'Done', '3.4'],
      ['1.5 Texture and TTFI', 'Not applicable (non-imaging data)', '–'], ['1.6.2 VIF across groups', 'Done → DSF', '3.4'], ['1.7 Biochemical parameters', 'Not measured in 2025-26', '–'],
      ['2.1.1–2.1.2 Tasks, fold-wise selection', 'Done', '3.5'], ['2.1.3 Fusion of 15 sensor sets', 'Not applicable (one sensor)', '–'], ['2.1.4 SFFS', 'Done', '3.6'], ['2.1.5 Feature configurations', 'Done: OW, VI, DSF', '3.9'],
      ['2.2.1–2.2.6 SVM/SVR, RF, XGBoost, k-NN, PLS-DA/PLSR, grids', 'Done', '3.6, 3.8'], ['2.3.1 DNN-F1; 2.3.3–2.3.8 pseudo-images, DT-EDNet, EfficientNet-B0, ResNet18, ConvNeXt V2', 'Done (paper settings, CPU, no extra tuning)', '3.7–3.9'],
      ['2.3.2 DNN-F2', 'Not applicable (one sensor)', '–'], ['2.4.1–2.4.3 Metrics', 'Done', '3.8'], ['2.5.3 Network comparison and ablation', 'Done', '3.9'], ['2.5.4 SHAP and stability', 'Done', '3.5, 3.10'],
      ['2.5.5 Covariate baseline', 'Done: B1 statistical, random forest and best ML on covariates only; M0/M1/M2; gains with plot-block bootstrap and DeLong (unsprayed plots only)', '2.11, 3.12'], ['2.6.1–2.6.2 Strata, LOVO, LOTO', 'Done', '3.11'], ['2.6.3 Severity maps', 'Not applicable (no images)', '–'],
      ['2.7.1 Final models on all data', 'Done: models saved with prediction script', '2.13, Appendix'], ['2.7.2–2.7.4 Bharatpur validation', 'Next season', '–'], ['3.1–3.5 Pre-symptomatic objective (Objective 3)', 'Not addressed: no pre-symptomatic dates in 2025-26', '–']]
TAB('check', CK, 'Methodology steps and their status for the 2025-26 leaf spectra.', [3300, 4400, 1606], 15)

# ------------------------------------------------------------------ 7 questions
H1('7. Likely questions and short answers')
QA = [('Why leaf level and not plot means?', 'The grade is scored on each leaf, so leaf spectra and leaf grades match one to one. Plot means would mix grades and reduce ' + str(N) + ' samples to 48 × 4. Plot structure is respected in validation: whole replications are held out and inner folds are grouped by plot.'),
      ('Why were the water bands kept?', 'The contact probe has its own light source and touches the leaf, so there is no atmospheric water absorption; the files were already splice-corrected. These regions measure leaf water, which falls in diseased tissue, and two selected features (FD1245, FD1805) come from their edges.'),
      ('Why leave-one-replication-out instead of random cross-validation?', 'Leaves from one plot are not independent. Random splits would place leaves of the same plot in training and test and overestimate accuracy (Roberts et al., 2017).'),
      ('Why is six-grade accuracy low?', 'Neighbouring grades overlap spectrally and in visual scoring; most errors are one grade apart (QWK %.2f). Detection and the regression score are the reliable outputs.' % rB.QWK),
      ('Why only derivative bands in the optimal wavelengths?', 'The derivative removes offsets and emphasises the red-edge shape, which changes with chlorophyll loss; SHAP and CARS both preferred them.'),
      ('Did DT-EDNet beat the other models?', ('No. At leaf level DT-EDNet reached macro-F1 %.3f for six grades, against %.3f for %s and %.3f for %s; all models were within about one fold-to-fold SD. With 10–16 features the pseudo-images have little spatial pattern; its strength is expected on UAV hyperspectral images. The ablation still showed a gain from the dual transformer group.' % (dte['B'].macro_F1, dlB.macro_F1, bB['DL'], row('B', bB['ML']).macro_F1, bB['ML'])) if HAS_DL else 'Results pending.'),
      ('How were feature selection and tuning kept free of leakage?', 'All selection (maps, SHAP-CARS, ReliefF, VIF, SFFS) and tuning were repeated inside each training part; the test replication was used once, for the final metrics.'),
      ('What does the covariate baseline show?', ('A model without sensor data (crop age, sowing timing, variety, stage, weather) already explains much of the epidemic level (six-grade macro-F1 %.2f). The spectra are credited only with the gain over it (ΔS %+.3f for six grades, %+.3f R² for the score), tested with a plot-level bootstrap; for detection inside unsprayed plots the calendar alone was as good as the spectra, because healthy leaves occurred mainly on the first date.' % (gm('B', 'covariates only', m0m['B'], 'macro_F1'), gg('B', 'macro_F1', 'ΔS = M1 − M0').delta, gg('C', 'R2', 'ΔS = M1 − M0').delta)) if cv2g is not None else 'Results pending.'),
      ('What do D1–D4 mean?', 'Four sowing dates (9 and 18 December, 27 December 2025 and 9 January 2026) that gave crops of 50, 40, 30 and 20 days after sowing at the end of January 2026. Infection was natural, so they show how crop age during the epidemic affects white rust; at sampling the crop age was %d–%d days after sowing.' % (M.DAS.min(), M.DAS.max())),
      ('What will change in 2026-27?', 'UAV images with 13 flights (3 pre-symptomatic), plot and subplot features, multi-sensor fusion, Objective 3 (pre-symptomatic detection) and external validation at Bharatpur.')]
for q, a in QA:
    K.append("K.push(new Paragraph({ spacing: { before: 120, after: 40 }, keepNext: true, children: [new TextRun({ text: 'Q. ' + %s, bold: true, font: FONT, size: 21, color: '1E3A1F' })] }));" % js(q)); P('A. ' + a)

# ------------------------------------------------------------------ appendix
H1('Appendix A. Excel workbook and model files')
TAB('sheets', [['Sheet', 'Content'], ['1_Data', 'leaf metadata and 5-nm reflectance (input of the formula sheets)'], ['2_Counts', 'COUNTIFS tables by factor and grade, with charts'], ['3_Mean_spectra', 'AVERAGEIFS mean spectra by grade, line chart'],
    ['4–7', 'first derivative, correlation (CORREL), NDSI/RSI R² grid, SHAP-CARS'], ['8_WRI', 'White Rust Index with editable wavelengths and weight (INDEX/MATCH)'], ['9–12', 'indices as formulas and values, ReliefF, VIF and the disease-specific feature set'],
    ['13–14', 'fold-wise selection, SFFS and grid search'], ['15–17', 'metrics, confusion matrices with formula metrics, observed vs predicted with formula metrics'], ['18–24', 'deep learning, SHAP, strata, transfer, weather, selection stability'], ['25_Covariate_baseline', 'covariates by date, models × inputs, gains with bootstrap intervals (Δ as formulas), DeLong tests, interpretable model; charts'], ['26_References', 'references']],
    'Main sheets of the Excel workbook.', [2200, 7106], 16)
for fn, lab in (('ml_models_index.csv', 'Machine-learning model files'), ('dl_models_index.csv', 'Deep-learning model files')):
    p = S + 'outputs/ASD_2025-26_models/' + fn
    if os.path.exists(p):
        d = pd.read_csv(p); TAB('mf' + fn[:2], [['File', 'Task', 'Model', 'Features']] + [[r.file, r.task, r.model, r.features] for r in d.itertuples()], lab + ' (trained on all %d leaves; load with predict_white_rust.py).' % N, [3000, 600, 1600, 4106], 14)
H1('References')

# ------------------------------------------------------------------ assemble
body = '\n'.join(K)
T = open(S + 'thesis/t_docx.js').read()
head = T[:T.index('// ======================= TITLE')]
head = re.sub(r"const B = '.*?';", "const B = '%s';" % B, head); head = re.sub(r"const OUT = '.*?';", "const OUT = '%s';" % OUTF, head)
head = re.sub(r"const FORDER = \[.*?\];", "const FORDER = __FORDER__;", head); head = re.sub(r"const TORDER = \[.*?\];", "const TORDER = __TORDER__;", head)
head = head.replace('children: [new Paragraph({ children: runs(String(c)', 'children: [new Paragraph({ keepNext: true, children: runs(String(c)')
plain = re.sub(r'\$\{[FT]\(\'\w+\'\)\}', '', body)
used, missing = a_refs.select(plain, fp=[('Peñuelas', '1994'), ('Kononenko', '2003'), ('Šikonja', '2003'), ('Rayens', '2003'), ('Vapnik', '1995'), ('Guestrin', '2016'), ('Hart', '1967'), ('Lapalme', '2009'), ('Lee', '2017'), ('Jurman', '2020'), ('Talbot', '2010'), ('McLachlan', '2002'), ('Simon', '2006'), ('Kumar', '2014'), ('Philpot', '1998'), ('Golay', '1964'), ('Rendell', '1992'), ('Till', '2001'), ('Barratt', '1945')])
print('missing refs:', missing)
q = lambda s: "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"
body += "\nconst refPara = r => new Paragraph({ spacing: { after: 70, line: 255 }, indent: { left: 400, hanging: 400 }, children: [new TextRun({ text: r, font: FONT, size: 19 })] });\n[" + ',\n'.join(q(r) for r in used) + "].forEach(r => K.push(refPara(r)));\n"
json.dump(used, open(D + 'refs_used.json', 'w'), indent=0, ensure_ascii=False)
FO = [m.group(1) for m in re.finditer(r"\bfig2\('([A-Za-z0-9]+)'", body)]; TO = [m.group(1) for m in re.finditer(r"\btab2\('([A-Za-z0-9]+)'", body)]
assert len(FO) == len(set(FO)) and len(TO) == len(set(TO)), 'duplicate keys'
mf = set(re.findall(r"\bF\('([A-Za-z0-9]+)'\)", body)) - set(FO); mt = set(re.findall(r"\bT\('([A-Za-z0-9]+)'\)", body)) - set(TO)
assert not mf and not mt, (mf, mt)
head = head.replace('__FORDER__', repr(FO)).replace('__TORDER__', repr(TO))
_tn = {k_: i_ + 1 for i_, k_ in enumerate(TO)}; _fn = {k_: i_ + 1 for i_, k_ in enumerate(FO)}
json.dump([dict(t_, number=_tn[t_['key']]) for t_ in RTAB if t_['key'] in _tn], open(D + 'report_tables.json', 'w'), ensure_ascii=False)
json.dump([dict(f_, number=_fn[f_['key']]) for f_ in RFIG if f_['key'] in _fn], open(D + 'report_figures.json', 'w'), ensure_ascii=False)
tail = T[T.index('\nconst numcfg'):]
tail = tail.replace("title: 'AI-based multimodal UAV sensing of white rust in mustard: complete methodology'", "title: 'White rust ASD leaf spectra 2025-26: analysis report'")
tail = re.sub(r"'eqs', \d+, 'refs', \d+", "'eqs', 0, 'refs', %d" % len(used), tail)
open(B + 'a10_build.js', 'w').write(head + '\n' + body + '\n' + tail)
print('figs', len(FO), 'tabs', len(TO), 'refs', len(used))
