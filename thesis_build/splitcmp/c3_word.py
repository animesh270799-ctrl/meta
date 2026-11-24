"""Word report: comparison of the validation designs (LORO vs grouped 70:30 vs grouped 80:20) for the 2025-26 ASD leaf data.
All numbers are read from c2_compare.py outputs and from the three pipelines.
  python3 c3_word.py && NODE_PATH=/opt/node22/lib/node_modules node c3_build.js && python3 ../satmet/to_pdf.py <docx> <pdf>"""
import json, re, os, sys, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'; S = HERE + '../'; O = HERE + 'out/'; L = S + 'asd26/data/'
sys.path.insert(0, S + 'asd7030'); import a_refs
OUTF = S + 'outputs/ASD_2025-26_validation_comparison_LORO_70-30_80-20_report.docx'
K = []; TABLES = []; FIGS = []
def esc(t):
    t = t.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${'); t = re.sub(r'_(?!\{)', r'\\\\_', t)
    return re.sub(r'\[\[(T|F):(\w+)\]\]', lambda m: '${%s(\'%s\')}' % (m.group(1), m.group(2)), t)
def js(s): return '`' + esc(s) + '`'
def H1(t): K.append("K.push(H1(%s));" % js(t))
def H2(t): K.append("K.push(H2(%s));" % js(t))
def P(t): K.append("K.push(P(%s));" % js(t))
def BL(items): K.extend("K.push(BL(%s));" % js(i) for i in items)
def NL(items): K.extend("K.push(NL(%s));" % js(i) for i in items)
def BOX(l, t, fill='FFF6E0', line='C98A00'): K.append("K.push(BOX(%s, %s, '%s', '%s'));" % (js(l), js(t), fill, line))
def FIG(k, file, cap, w=620):
    FIGS.append(dict(key=k, file=file, caption=cap)); K.append("K.push(...fig2('%s', '%s', %s, %d));" % (k, file, js(cap), w))
def TAB(k, rows, cap, widths=None, size=16):
    if widths is None:
        Lw = [min(max(max(len(str(r[j])) for r in rows), 5), 46) for j in range(len(rows[0]))]; s = sum(Lw); widths = [int(9306 * x / s) for x in Lw]
    TABLES.append(dict(key=k, caption=cap, rows=[[str(c) for c in r] for r in rows]))
    R = '[' + ',\n'.join('[' + ', '.join(js(str(c)) for c in r) + ']' for r in rows) + ']'
    K.append("K.push(...tab2('%s', %s, %s, %s, %d));" % (k, R, json.dumps(widths), js(cap), size))
def PB(): K.append("K.push(new Paragraph({ children: [new PageBreak()] }));")
def CARD(key, title, concept, why, papers, mine, output, alt=None):
    rows = [['Item', title], ['Concept', concept], ['Why (justification)', why], ['What papers used', papers], ['How with my data', mine], ['Output → next step', output]]
    if alt: rows.append(['Alternatives and notes', alt])
    TAB(key, rows, 'Step card – %s.' % title, [2250, 7056], 16)
f2 = lambda x: '–' if x is None or (isinstance(x, float) and not np.isfinite(x)) else '%.2f' % x
f3 = lambda x: '–' if x is None or (isinstance(x, float) and not np.isfinite(x)) else '%.3f' % x
sg = lambda x: '–' if x is None or (isinstance(x, float) and not np.isfinite(x)) else '%+.3f' % x
opt = lambda f: pd.read_csv(f) if os.path.exists(f) else None

# ---------------- data
M = pd.read_csv(L + 'meta.csv'); N = len(M)
DES = [('70:30', '70-30', S + 'asd7030/'), ('80:20', '80-20', S + 'asd8020/')]
DES = [d for d in DES if os.path.exists(d[2] + 'data/metrics_all.csv')]
LABS = ['LORO'] + [d[0] for d in DES]
S3 = pd.read_csv(O + 'cmp3_side.csv'); CP = opt(O + 'cmp3_paired.csv'); CR = opt(O + 'cmp3_repeat.csv'); CL_ = opt(O + 'cmp3_leak.csv'); SUMM = json.load(open(O + 'cmp3_summary.json'))
SPJ = {lab: json.load(open(d + 'data/split.json')) for lab, _, d in DES}
BEST = {'LORO': json.load(open(L + 'best_models.json')), **{lab: json.load(open(d + 'data/best_models.json')) for lab, _, d in DES}}
MT = {'LORO': pd.read_csv(L + 'metrics_all.csv'), **{lab: pd.read_csv(d + 'data/metrics_all.csv') for lab, _, d in DES}}
G = {'LORO': opt(L + 'cov2_gains.csv'), **{lab: opt(d + 'data/cov2_gains.csv') for lab, _, d in DES}}
MAINK = {'A': 'macro_F1', 'B': 'macro_F1', 'C': 'R2'}; TASKN = {'A': 'A – detection', 'B': 'B – six grades', 'C': 'C – severity score'}
MLM = ['SVM', 'RF', 'XGBoost', 'k-NN', 'PLS-DA', 'PLS']
mn = lambda m, t: {'SVM': 'SVR', 'PLS': 'PLSR'}.get(m, m) if t == 'C' else m
MK = {'macro_F1': 'macro-F1', 'R2': 'R²', 'AUC': 'AUC', 'QWK': 'QWK', 'OA': 'OA', 'RMSE': 'RMSE'}
def mt(lab, t, m, k): d = MT[lab][(MT[lab].task == t) & (MT[lab].model == m)]; return float(d[k].iloc[0]) if len(d) else np.nan
def dl_parts(te):
    tr = ~te; pt = np.unique(M['plot'].values[tr]); rg = np.random.default_rng(42); vp = set(rg.choice(pt, len(pt) // 3, replace=False)); va = tr & M['plot'].isin(vp).values; return int((tr & ~va).sum()), int(va.sum()), int(te.sum()), len(pt) - len(vp), len(vp), int(M[te]['plot'].nunique())
TEST = {'LORO': None, **{lab: M['plot'].isin(SPJ[lab]['test_plots']).values for lab in SPJ}}

# ---------------- title and summary
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 900, after: 200 }, children: [new TextRun({ text: 'Does a 70:30 or 80:20 split improve the accuracy?', font: FONT, size: 42, bold: true, color: '1E3A1F' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [new TextRun({ text: 'Comparison of three validation designs – leave-one-replication-out (LORO), grouped 70:30 and grouped 80:20 hold-out – for leaf-level white rust models (ASD spectra, IARI 2025-26)', font: FONT, size: 26, color: '2C5F2D' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 500 }, children: [new TextRun({ text: 'Animesh Panda | Ph.D. Agricultural Physics | ICAR-Indian Agricultural Research Institute, New Delhi', font: FONT, size: 22, bold: true })] }));")
ans = ' '.join(SUMM[lab]['verdict'] for lab in SUMM)
BOX('Answer in short.', ' '.join('**%s.** %s' % (lab, SUMM[lab]['summary_sentence']) for lab in SUMM) + ' LORO, which tests all %d leaves once and follows the replication structure of the experiment, remains the main accuracy estimate; the hold-out models are deployable models whose single-split accuracy must be read with the split-to-split range.' % N, 'E8F5E9', '2E7D32')
BOX('How the files fit together.', 'This report compares the designs. The full analyses are in the three reports ASD_2025-26_leaf_analysis_white_rust_report (LORO), ASD_2025-26_70-30_… and ASD_2025-26_80-20_… with their Excel workbooks, slides and model folders. '
    'Every table of this report is in the Excel workbook ASD_2025-26_validation_comparison_LORO_70-30_80-20.xlsx with live formulas, and in the slides of the same name. The folder ASD_2025-26_validation_comparison_step_by_step holds all outputs in numbered step folders.')
PB(); K.append("K.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: 'Contents', font: FONT, size: 32, bold: true, color: '1E3A1F' })] }));")
K.append("K.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-2' }));"); PB()

# ---------------- 1 introduction
H1('1. Introduction')
P('The leaf-level white rust models of the 2025-26 ASD data were first evaluated with leave-one-replication-out (LORO) cross-validation: the models were trained on two replications and tested on the third, three times, so that each of the %d leaves was tested once. A common alternative in plant-disease studies is a single hold-out split, most often 70:30 or 80:20 (Mohanty et al., 2016; Ferentinos, 2018). This report asks whether such a split gives a higher – and equally trustworthy – accuracy on the same data.' % N)
P('A validation design does not change the model; it changes how its accuracy is estimated. A hold-out estimate depends on which samples happen to be in the test set, and with few test units its variance is large; cross-validation averages over several test sets and uses every sample for testing (Kohavi, 1995; Molinaro et al., 2005; Vabalas et al., 2019; Xu and Goodacre, 2018). Leaves of one plot are not independent, so every design here keeps whole plots apart (Roberts et al., 2017).')
H2('1.1 Questions')
NL(['Does the grouped 70:30 or 80:20 split give higher test accuracy than LORO for the same models and features?', 'Is a difference real on the same test leaves, or only a result of testing different leaves?', 'How much does the hold-out accuracy change from one possible split to another?',
    'How much would a random split of leaves (plots ignored), as used in many papers, inflate the accuracy?', 'Which design should be reported and used for the thesis models?'])

# ---------------- 2 designs
H1('2. Validation designs')
H2('2.1 Types of split used in plant-disease studies')
TAB('splittypes', [['Split type', 'How it works', 'Example in plant-disease studies'],
    ['Random hold-out 80:20', 'images, leaves or pixels drawn at random; 80% train, 20% test', 'PlantVillage images: 80–20 to 20–80 random splits (Mohanty et al., 2016); 17,548 of 87,848 images held out, about 80:20 (Ferentinos, 2018)'],
    ['Random hold-out 70:30', 'as above with 70% train, 30% test, often stratified by class', 'rule of thumb of 20–30% for testing (Gholamy et al., 2018); 80:20 has no theoretical basis, √p : 1 proposed (Joseph, 2022)'],
    ['Train : validation : test (e.g. 70:15:15)', 'train fits, validation chooses hyper-parameters, features or epochs, test is used once', 'Ripley (1996); Hastie et al. (2009, §7.2); Goodfellow et al. (2016, §5.3)'],
    ['Repeated random hold-out', 'the random split repeated many times and averaged', 'wheat stripe rust spectra: 80:20 repeated 100 times (Cross et al., 2024)'],
    ['k-fold or leave-one-out cross-validation', 'every sample tested once; small data sets', 'wheat stripe and leaf rust: leave-one-out plus external validation (Wang et al., 2016)'],
    ['Grouped / blocked split', 'all samples of a plot, field or replication stay on one side', 'Roberts et al. (2017); random hold-outs overestimated accuracy by up to 28% compared with spatial blocks (Kattenborn et al., 2022)'],
    ['Independent test', 'model applied to another season, site or condition', 'PlantVillage model: 99.35% on the random hold-out, 31.4% on images taken under other conditions (Mohanty et al., 2016)']],
    'Types of training/test split in plant-disease detection studies.', [2300, 3000, 4006], 15)
H2('2.2 The three designs on this data set')
rows_ = [['Design', 'Test sets', 'Test plots (healthy + unsprayed)', 'Test leaves', 'Training leaves', 'Leaves tested', 'Inner validation']]
rows_.append(['LORO', '3 folds (R1, R2, R3 + 4 rotated healthy plots each)', '16 per fold (4 + 12)', '%d–%d per fold' % tuple(sorted([(M.fold == f).sum() for f in range(3)])[::2]), '%d–%d' % tuple(sorted([(M.fold != f).sum() for f in range(3)])[::2]), 'all %d, once' % N, 'GroupKFold(3) by plot; networks: 1/3 of training plots'])
for lab in SPJ:
    j = SPJ[lab]; rows_.append([lab, '1 grouped, stratified split', '%d (%d + %d)' % (j['n_test_plots'], len(j['test_healthy_plots']), len(j['test_unsprayed_plots'])), str(j['n_test_leaves']), str(j['n_train_leaves']), '%d (%.0f%%), once' % (j['n_test_leaves'], 100 * j['test_leaf_fraction']), 'GroupKFold(3) by plot; networks: 1/3 of training plots'])
TAB('designs', rows_, 'The three validation designs. All keep whole plots apart; all repeat feature selection, SFFS and tuning on the training plots only.', [900, 2300, 1600, 1200, 1200, 1300, 1806], 14)
FIG('designs', 'c01_designs.png', 'Test plots of the three designs on the field layout (plot number and treatment code; healthy block 1–12, unsprayed replications R3, R2, R1).', 620)
H2('2.3 How the 70:30 and 80:20 splits were chosen')
P('Healthy (fungicide-sprayed) and unsprayed plots were split separately, round(fraction × plots) of each going to the test set (70:30: 4 healthy + 11 unsprayed; 80:20: 2 + 7). The unsprayed test plots come from different treatments (sowing timing × variety) and are spread as evenly as possible over the three replications, varieties and timings; the healthy test plots have different varieties and timings. Among 5000 random candidate splits that met these rules, the one closest to the target share of leaves and to the overall grade and date distribution was chosen (seed 2026; split_lib.py). This is a grouped, stratified hold-out (Kuhn and Johnson, 2013; Roberts et al., 2017).')
rows_ = [['Design', 'Set', *['Grade %d (%%)' % g for g in (0, 1, 3, 5, 7, 9)], 'Leaves']]
for lab in SPJ:
    te = TEST[lab]
    for nm, msk in (('training', ~te), ('test', te)): rows_.append([lab, nm, *['%.1f' % (100 * (M.grade[msk] == g).mean()) for g in (0, 1, 3, 5, 7, 9)], str(int(msk.sum()))])
TAB('balance', rows_, 'Grade distribution of the training and test leaves of each split.', [900, 1100] + [1000] * 6 + [1306], 15)
H2('2.4 Train : validation : test – which models need which')
rows_ = [['Model / step', 'What is chosen from the data', 'Validation used', 'Split it needs']]
rows_ += [['SVM / SVR, RF, XGBoost, k-NN, PLS-DA / PLSR', 'hyper-parameters and the SFFS feature subset', 'inner GroupKFold(3) by plot in the training plots; then refit on all training plots', 'train (+ inner CV) : test'],
          ['DNN-F1, DT-EDNet, EfficientNet-B0, ResNet18, ConvNeXt V2-Atto', 'stopping epoch (settings fixed from Ma et al., 2026)', 'separate validation set: one third of the training plots, checked every epoch (Prechelt, 1998; Goodfellow et al., 2016)', 'train : validation : test'],
          ['Logistic regression (covariate B1)', 'penalty C', 'inner GroupKFold(3)', 'train (+ inner CV) : test'], ['Ordinal logistic and linear regression (covariate B1)', 'nothing', 'none', 'train : test'],
          ['Objective 1 steps (maps, SHAP-CARS, ReliefF, VIF)', 'bands and indices', 'training plots only', 'train : test']]
TAB('valroles', rows_, 'Which models need a validation part (Hastie et al., 2009; Varma and Simon, 2006; Cawley and Talbot, 2010).', [2600, 2000, 2900, 1806], 14)
rows_ = [['Design', 'Fit : validation : test leaves', 'Plots', 'Share of all leaves (%)']]
for f in range(3): a = dl_parts((M.fold == f).values); rows_.append(['LORO fold %d' % (f + 1), '%d : %d : %d' % a[:3], '%d : %d : %d' % a[3:], '%.0f : %.0f : %.0f' % tuple(100 * np.array(a[:3]) / N)])
for lab in SPJ: a = dl_parts(TEST[lab]); rows_.append([lab, '%d : %d : %d' % a[:3], '%d : %d : %d' % a[3:], '%.0f : %.0f : %.0f' % tuple(100 * np.array(a[:3]) / N)])
TAB('dlparts', rows_, 'Effective train : validation : test parts of the networks in each design (whole plots; seed 42).', [1800, 2600, 2200, 2706], 15)
P('The networks therefore already work as a train : validation : test design (70:30 ≈ 47 : 23 : 30), and the machine-learning models as train : test with nested validation. A separate fixed 70:15:15 split by plots would leave only about 7 test plots and add nothing.')

# ---------------- 3 methods of comparison
H1('3. How the designs were compared')
CARD('cside', 'Step 1 – all models side by side', 'Every metric of every model and task under each design, from the full analyses.', 'The first, raw look at the question.', 'Standard reporting of model metrics (Sokolova and Lapalme, 2009).',
     'Ten models (five ML, five DL) × three tasks; macro-F1, AUC, QWK, R², RMSE and the other metrics of each analysis.', 'Differences design − LORO; best model of each design.', 'The designs test different leaves, so these differences mix the design with the test set.')
CARD('cpair', 'Step 2 – same test leaves (paired comparison)', 'In LORO every leaf was tested once, so the LORO predictions of exactly the hold-out test leaves can be compared with the hold-out predictions of the same leaves.',
     'Removes the effect of testing different leaves; what remains is the effect of the training set and the design.', 'Paired comparison of classifiers on the same test set (Dietterich, 1998); cluster bootstrap for dependent samples (Field and Welsh, 2007; Efron and Tibshirani, 1993).',
     'For each split, model and metric: difference split − LORO on the split test leaves; 2000 bootstrap resamples of whole test plots (healthy and unsprayed separately) → 95% interval. Verdict "higher" or "lower" only when the interval excludes zero.', 'Counts of real gains and losses.')
CARD('crep', 'Step 3 – split-to-split variability (repeated splits)', 'The same light pipeline is run on LORO, on the main split and on 20 other rule-conforming grouped splits of each ratio.',
     'One split is one draw; the range over many draws shows whether the main split is typical and whether a hold-out is systematically higher than LORO (Kohavi, 1995; Vabalas et al., 2019).', 'Repeated hold-out (Cross et al., 2024; Xu and Goodacre, 2018).',
     'Light pipeline, identical everywhere: selection on the training part (effective ranges, SHAP-CARS 10 runs, NDSI/RSI, WRI, ReliefF, VIF < 10), A SVM, B random forest, C XGBoost with grid search in three inner folds (no SFFS, to keep 49 runs affordable).', 'Mean, SD, range and number of splits above LORO.')
CARD('cleak', 'Step 4 – leakage check', 'Five random 70:30 and 80:20 splits of LEAVES, stratified by grade, with inner folds also by leaf – the usual practice in many papers.',
     'Shows how much accuracy is gained only because leaves of the same plot are in training and test (Roberts et al., 2017; Kattenborn et al., 2022; Kapoor and Narayanan, 2023).', 'Spatial vs random cross-validation (Roberts et al., 2017; Kattenborn et al., 2022).',
     'Same light pipeline as Step 3.', 'Inflation = leaf-level − grouped accuracy.')
CARD('cov', 'Step 5 – selection overlap', 'Jaccard similarity |A ∩ B| / |A ∪ B| of the optimal wavelengths and of the disease-specific feature set chosen in each training set.', 'Shows whether the design changes which spectral features are chosen.', 'Stability of feature selection (Kalousis et al., 2007).',
     'All leaves (Objective 1), three LORO training parts, 70:30 and 80:20 training plots.', 'Similarity matrix.')

# ---------------- 4 results
H1('4. Results')
H2('4.1 All models side by side')
rows_ = [['Task', 'Model', 'Type', *LABS, *['%s − LORO' % l for l in LABS[1:]]]]
for t in 'ABC':
    d = S3[(S3.task == t) & (S3.metric == MAINK[t])].sort_values('LORO', ascending=False)
    for i_, r in d.iterrows(): rows_.append([t, mn(r.model, t), r.type, *[f3(float(r[l])) for l in LABS], *[sg(float(r['d_' + l])) for l in LABS[1:]]])
TAB('side', rows_, 'Main metric of every model under each design (macro-F1 for A and B, R² for C). All metrics are in the Excel workbook (sheet 2).', None, 14)
mdel = {l: {t: S3[(S3.task == t) & (S3.metric == MAINK[t])]['d_' + l].mean() for t in 'ABC'} for l in LABS[1:]}
nup = {l: int((S3[S3.metric == S3.task.map(MAINK)]['d_' + l] > 0).sum()) for l in LABS[1:]}
P('; '.join('Under %s, %d of the 30 model–task results were higher than LORO (mean difference %s macro-F1 for detection, %s for six grades, %s R² for the score)' % (l, nup[l], sg(mdel[l]['A']), sg(mdel[l]['B']), sg(mdel[l]['C'])) for l in LABS[1:]) + ' ([[T:side]], [[F:side]]).')
FIG('side', 'c02_side.png', 'Main metric of every model under LORO (grey), 70:30 (blue) and 80:20 (orange).', 620)
rows_ = [['Task', 'Role', *LABS]]
for t in 'ABC':
    for role in ('overall', 'ML', 'DL'):
        rows_.append([t, role, *['%s (%s)' % (mn(BEST[l][t][role], t), f3(mt(l, t, BEST[l][t][role], MAINK[t]))) if BEST[l][t].get(role) else '–' for l in LABS]])
TAB('best', rows_, 'Best model of each design (main metric in brackets).', [700, 1000] + [int(7606 / len(LABS))] * len(LABS), 14)
if CP is not None:
    H2('4.2 Same test leaves')
    for lab in LABS[1:]:
        P_ = CP[(CP.design == lab) & (CP.metric == CP.task.map(MAINK))]
        rows_ = [['Task', 'Model', 'LORO (same leaves)', lab, 'Difference', '95% interval', 'Verdict']] + [[r.task, mn(r.model, r.task), f3(r.LORO_same), f3(r.split), sg(r.delta), '%s to %s' % (sg(r.ci_low), sg(r.ci_high)), r.verdict] for r in P_.itertuples()]
        TAB('pair' + lab.replace(':', ''), rows_, 'Paired comparison on the %d %s test leaves (%d plots): LORO predictions of the same leaves vs %s predictions.' % (int(P_.n_leaves.iloc[0]), lab, int(P_.n_plots.iloc[0]), lab), [600, 1700, 1500, 1100, 1100, 1900, 1406], 14)
        P(SUMM[lab]['summary_sentence'])
    for lab, _, d in DES:
        bt = opt(d + 'data/cmp_blocktype_summary.csv')
        if bt is None: continue
        TAB('block' + lab.replace(':', ''), [['Task', 'Test leaves from', 'Metric', 'Leaves', 'LORO (same leaves)', lab, 'Difference']] + [[r.task, r.plots, r.metric, str(int(r.n)), f3(r.LORO_same), f3(r.split), sg(r.delta)] for r in bt.itertuples()],
            'Paired difference by type of test plot, %s (overall accuracy for A and B, RMSE for C; mean of the ten models).' % lab, [700, 1700, 900, 900, 1700, 1500, 1906], 15)
        if SUMM[lab].get('diag_sentence'): P(SUMM[lab]['diag_sentence'])
    FIG('pair', 'c03_paired.png', 'Difference split − LORO on the same test leaves with 95% plot-bootstrap intervals (green: really higher, red: really lower, grey: no real difference).', 620)
if CR is not None:
    H2('4.3 Split-to-split variability')
    rows_ = [['Design', 'Task', 'Metric', 'LORO (all leaves)', 'Main split', '20 other splits: mean ± SD (range)', 'Above LORO (all leaves)', 'Same leaves: mean difference', 'Same leaves: better than LORO']]
    for r in CR[CR.metric == CR.task.map(MAINK)].itertuples(): rows_.append([r.design, r.task, MK[r.metric], f3(r.LORO_light), f3(r.main_light), '%s ± %s (%s – %s)' % (f3(r.rep_mean), f3(r.rep_sd), f3(r.rep_min), f3(r.rep_max)), '%d of %d' % (r.rep_above, r.rep_n),
                                                                             '%s ± %s' % (sg(r.paired_mean), f3(r.paired_sd)) if hasattr(r, 'paired_mean') else '–', '%d of %d' % (r.paired_better, r.rep_n) if hasattr(r, 'paired_better') else '–'])
    TAB('rep', rows_, 'Light pipeline under LORO, the main split and 20 other grouped splits of each ratio. "Same leaves" compares each split with the LORO predictions of exactly its test leaves. AUC, QWK and RMSE are in the Excel workbook.', [700, 500, 800, 1000, 900, 1900, 1100, 1300, 1106], 13)
    for lab in LABS[1:]:
        if SUMM[lab].get('repeat_sentence'): P(SUMM[lab]['repeat_sentence'])
    FIG('rep', 'c04_repeat.png', 'Test accuracy of the light pipeline over 20 grouped splits of each ratio (dots and box) with LORO (dashed line) and the main split (diamond).', 620)
if CL_ is not None:
    H2('4.4 Leakage check')
    rows_ = [['Design', 'Task', 'Metric', 'Grouped (mean of 20)', 'Random leaf-level (mean of 5)', 'Inflation']] + [[r.design, r.task, MK[r.metric], f3(r.grouped), f3(r.leaf), sg(r.inflation)] for r in CL_[CL_.metric == CL_.task.map(MAINK)].itertuples()]
    TAB('leak', rows_, 'Grouped (whole plots) vs random leaf-level splits with the same light pipeline.', [1000, 700, 1000, 2200, 2400, 2006], 15)
    for lab in LABS[1:]:
        if SUMM[lab].get('leak_sentence'): P(SUMM[lab]['leak_sentence'])
    FIG('leak', 'c05_leak.png', 'Grouped vs random leaf-level splits: the leaf-level accuracy is inflated by plot leakage.', 560)
H2('4.5 Do the designs choose the same features?')
FIG('ov', 'c06_overlap.png', 'Jaccard similarity of the optimal wavelengths and of the six-grade disease-specific feature set chosen in each training set.', 620)
sets = pd.read_csv(O + 'cmp3_sets.csv')
TAB('sets', [['Training set', 'Optimal wavelengths', 'Disease-specific feature set (six grades)']] + [[r.set, r.OW, r.DSF_B] for r in sets.itertuples()], 'Features chosen in each training set.', [2000, 4000, 3306], 13)
if all(G[l] is not None for l in LABS):
    H2('4.6 Is the value of the spectra over the covariates the same under each design?')
    rows_ = [['Task', 'Metric', *['%s ΔS (95%% CI)' % l for l in LABS]]]
    for t, k in (('A', 'macro_F1'), ('B', 'macro_F1'), ('C', 'R2')):
        cells = []
        for l in LABS:
            g = G[l][(G[l].task == t) & (G[l].metric == k) & (G[l].gain == 'ΔS = M1 − M0')]
            cells.append('%s (%s to %s)%s' % (sg(g.delta.iloc[0]), sg(g.ci_low.iloc[0]), sg(g.ci_high.iloc[0]), ' ✓' if bool(g.real_gain.iloc[0]) else '') if len(g) else '–')
        rows_.append([t, MK[k], *cells])
    TAB('gains', rows_, 'Gain of the leaf spectra over the covariate-only baseline (ΔS = M1 − M0) on the unsprayed leaves under each design; ✓ = real gain by the rule of that design (LORO: interval excludes 0, larger than the fold SD, same sign in all folds; hold-out: interval excludes 0).', [700, 1000] + [int(7606 / len(LABS))] * len(LABS), 14)

# ---------------- 5 discussion
H1('5. Discussion')
H2('5.1 Is the accuracy improving?')
for lab in LABS[1:]: P('**%s.** %s' % (lab, SUMM[lab]['answer']))
H2('5.2 Why a single split can look better or worse')
P('A hold-out accuracy is the accuracy of one test set. With 15 (70:30) or 9 (80:20) test plots, the result depends strongly on which plots are drawn, as the range over 20 other splits shows; this is the known high variance of single train/test splits in small data sets (Kohavi, 1995; Molinaro et al., 2005; Vabalas et al., 2019). LORO averages three test sets that together contain every plot, so its estimate is more stable. A larger training share (80% vs about 67% in LORO) helps only if the models are still data-limited; the paired comparison on the same leaves isolates this effect.')
P('Splitting leaves instead of plots inflates the accuracy because leaves of the same plot share soil, microclimate, inoculum and sampling date; the model then partly recognises the plot rather than the disease (Roberts et al., 2017; Kattenborn et al., 2022; Kapoor and Narayanan, 2023). Many published disease studies split images or leaves at random (Mohanty et al., 2016; Ferentinos, 2018), so their accuracies are not directly comparable with the grouped estimates of this thesis.')
H2('5.3 Which design to report')
BL(['**Main accuracy estimate:** LORO with nested, plot-grouped inner cross-validation – every leaf tested once, the replication structure of the experiment respected, selection and tuning inside the training part (Varma and Simon, 2006; Cawley and Talbot, 2010).',
    '**Hold-out (70:30, 80:20):** useful as deployable models trained on a fixed set of plots and as a check; report their accuracy together with the repeated-split range, never as a single number alone.',
    '**Strongest test:** an independent season or site (2026-27 UAV season, Bharatpur), because spatial and temporal dependence are only fully broken there (Mohanty et al., 2016).'])
H2('5.4 Limitations')
BL(['The repeated-split analysis uses a light pipeline (no SFFS, no networks) to keep 49 runs affordable; its absolute values are therefore slightly different from the full analyses, but it is identical across the designs.', 'Only 48 plots: every design has few independent test units.', 'One season and one site.'])

# ---------------- 6 conclusions and questions
H1('6. Conclusions')
NL([SUMM[l]['verdict'] for l in LABS[1:]] + ['Random leaf-level splits inflate the accuracy; whole plots must be kept apart.', 'LORO remains the main accuracy estimate of the thesis; the hold-out models are kept as deployable models with their test-plot accuracy.'])
H1('7. Likely questions and short answers')
QA = [('Why not simply report the 70:30 or 80:20 accuracy?', 'Because it is the accuracy of one set of %d or %d test plots; Chapter 4.3 shows how much it changes with the split. LORO tests all 48 plots once.' % (SPJ.get('70:30', {}).get('n_test_plots', 15), SPJ.get('80:20', {}).get('n_test_plots', 9))),
      ('Which split do most disease papers use?', 'Random 80:20 or 70:30 splits of images or leaves (Mohanty et al., 2016; Ferentinos, 2018); grouped or independent tests are recommended when samples are dependent (Roberts et al., 2017; Kattenborn et al., 2022).'),
      ('How does 70:15:15 work and do I need it?', 'Train fits, validation tunes or stops training, test is used once (Ripley, 1996; Hastie et al., 2009). The networks already have a validation set (one third of the training plots); the machine-learning models use inner cross-validation. A fixed 70:15:15 split would leave about 7 test plots.'),
      ('Is the higher number of a split a real improvement?', ' '.join(SUMM[l]['verdict'] for l in LABS[1:])),
      ('Why is the leaf-level split so much better?', 'Leakage: leaves of the same plot end up in training and test (Roberts et al., 2017).')]
for q_, a_ in QA:
    K.append("K.push(new Paragraph({ spacing: { before: 120, after: 40 }, keepNext: true, children: [new TextRun({ text: 'Q. ' + %s, bold: true, font: FONT, size: 22 })] }));" % js(q_)); P('A. ' + a_)
H1('References')

# ---------------- assemble
body = '\n'.join(K)
Tt = open(S + 'thesis/t_docx.js').read(); head = Tt[:Tt.index('// ======================= TITLE')]
head = re.sub(r"const B = '.*?';", "const B = '%s';" % HERE, head); head = re.sub(r"const OUT = '.*?';", "const OUT = '%s';" % OUTF, head)
head = re.sub(r"const FORDER = \[.*?\];", "const FORDER = __FORDER__;", head); head = re.sub(r"const TORDER = \[.*?\];", "const TORDER = __TORDER__;", head)
head = head.replace('children: [new Paragraph({ children: runs(String(c)', 'children: [new Paragraph({ keepNext: true, children: runs(String(c)')
plain = re.sub(r'\$\{[FT]\(\'\w+\'\)\}', '', body)
POOL = a_refs.pool(); c_ = a_refs.cites(plain); used, seen = [], set()
for r in POOL:
    k = a_refs.rk(r)
    if k in c_ and k not in seen: seen.add(k); used.append(r)
used.sort(key=lambda r: r.lower())
print('missing refs:', sorted(x for x in c_ if x not in seen and x[0] not in a_refs.SKIP and 1900 < int(x[1]) < 2028))
q = lambda s: "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"
body += "\nconst refPara = r => new Paragraph({ spacing: { after: 70, line: 255 }, indent: { left: 400, hanging: 400 }, children: [new TextRun({ text: r, font: FONT, size: 19 })] });\n[" + ',\n'.join(q(r) for r in used) + "].forEach(r => K.push(refPara(r)));"
json.dump(used, open(O + 'refs_used.json', 'w'), indent=0, ensure_ascii=False)
FO = [mm.group(1) for mm in re.finditer(r"\bfig2\('([A-Za-z0-9]+)'", body)]; TO = [mm.group(1) for mm in re.finditer(r"\btab2\('([A-Za-z0-9]+)'", body)]
assert len(FO) == len(set(FO)) and len(TO) == len(set(TO))
mf = set(re.findall(r"\bF\('([A-Za-z0-9]+)'\)", body)) - set(FO); mt_ = set(re.findall(r"\bT\('([A-Za-z0-9]+)'\)", body)) - set(TO); assert not mf and not mt_, (mf, mt_)
head = head.replace('__FORDER__', repr(FO)).replace('__TORDER__', repr(TO))
tail = Tt[Tt.index('\nconst numcfg'):]
tail = tail.replace("title: 'AI-based multimodal UAV sensing of white rust in mustard: complete methodology'", "title: 'Validation design comparison: LORO vs 70:30 vs 80:20'")
tail = re.sub(r"'eqs', \d+, 'refs', \d+", "'eqs', %d, 'refs', %d" % (len(re.findall(r'K.push\(EQ\(', body)), len(used)), tail)
open(HERE + 'c3_build.js', 'w').write(head + '\n' + body + '\n' + tail)
tn = {k: i + 1 for i, k in enumerate(TO)}; fn = {k: i + 1 for i, k in enumerate(FO)}
json.dump([dict(t, number=tn[t['key']]) for t in TABLES], open(O + 'tables.json', 'w'), indent=0, ensure_ascii=False)
json.dump([dict(f, number=fn[f['key']]) for f in FIGS], open(O + 'figures.json', 'w'), indent=0, ensure_ascii=False)
print('figs', len(FO), 'tabs', len(TO), 'refs', len(used))
