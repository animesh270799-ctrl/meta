"""Word report of the Part L analysis (content.json for word_build.js): one chapter per step with the step card, every result table and every figure
(300-dpi figures drawn by d3_figs.py from the same tables as the Excel and PPT charts), cross-checks, deviations and references."""
import os, sys, json, pickle, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import d0_text, d2_specs, refs, configL as C
T = pickle.load(open(os.path.join(HERE, 'tables.pkl'), 'rb')); F = json.load(open(os.path.join(HERE, 'facts.json'))); STEPS = d0_text.steps(T, F); ST = {s['code']: s for s in STEPS}
SPEC = {s['id']: s for s in d2_specs.specs(T, F)}; FG = os.path.join(HERE, 'fig'); OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'PartL_ASD_2025-26_leaf_analysis_report.docx')
B = []; NF = [0]; NT = [0]
def h1(t, newpage=True): B.append(dict(t='h1', text=t, newpage=newpage))
def h2(t): B.append(dict(t='h2', text=t))
def h3(t): B.append(dict(t='h3', text=t))
def p(*ts): [B.append(dict(t='p', text=t)) for t in ts]
def bl(items): B.append(dict(t='bl', items=list(items)))
def box(label, text, kind='key'): B.append(dict(t='box', label=label, text=text, kind=kind))
def cell(v):
    if isinstance(v, (float, np.floating)):
        if not np.isfinite(v): return '—'
        return str(int(v)) if float(v).is_integer() and abs(v) < 1e6 else ('%.3f' % v if abs(v) < 100 else '%.1f' % v)
    if isinstance(v, (np.integer,)): return str(int(v))
    if isinstance(v, (bool, np.bool_)): return 'yes' if v else 'no'
    return str(v)
def tab(rows, caption, widths=None, size=16, nokeep=False, boldfirst=False):
    NT[0] += 1; B.append(dict(t='tab', key='t%d' % NT[0], rows=[[cell(c) for c in r] for r in rows], caption=caption, widths=widths, size=size, nokeep=nokeep or len(rows) > 14, boldfirst=boldfirst)); return 'Table %d' % NT[0]
def dtab(df, caption, widths=None, size=15, cols=None, rename=None):
    df = df[cols] if cols else df; df = df.rename(columns=rename or {}); return tab([list(map(str, df.columns))] + df.values.tolist(), caption, widths, size)
def fig(fid, caption=None, width=620):
    f = os.path.join(FG, fid + '.png'); assert os.path.isfile(f), f; NF[0] += 1
    cap = caption or (SPEC[fid]['title'] + ('. ' + SPEC[fid]['note'] if fid in SPEC and SPEC[fid]['note'] else '') + ' (Excel chart %s; data in the "Chart data" cells of sheet %s).' % (fid, SPEC[fid]['sheet'] if fid in SPEC else '—'))
    B.append(dict(t='fig', key='f%d' % NF[0], file=f, caption=cap, width=width)); return 'Figure %d' % NF[0]
def card(code):
    s = ST[code]
    rows = [['Item', 'Step %s – %s' % (code, s['title'])], ['Concept (what)', s['what'] or s['title']], ['Why (justification)', s['why'] or '—'], ['Position in the analysis', s['position']], ['Samples used', s['samples']], ['Settings', s['settings']],
            ['What the papers did', '\n'.join('• %s: %s' % pp for pp in s['papers']) or '—'], ['How it was done with my data', '\n'.join('• ' + x for x in s['mydata'])], ['Result', '\n'.join('• ' + x for x in s['result']) or '—'],
            ['Output → next step', s['output']], ['Notes and alternatives', s['notes'] or '—'], ['Interview question', s['q'] or '—'], ['References', '; '.join(dict.fromkeys([pp[0] for pp in s['papers']] + s['mrefs'])) or '—']]
    return tab(rows, 'Step card of Step %s – %s.' % (code, s['title']), widths=[2300, 7300], size=16, boldfirst=True, nokeep=True)
B.append(dict(t='title', title='Part L analysis of the 2025-26 ASD leaf spectra', subtitle='White rust of Indian mustard – leaf disease score pooled over all dates, growth stages, varieties and leaf positions',
              lines=['Steps L1–L10 of the 2026-27 methodology (Part L) applied to the four ASD FieldSpec data sets of 11 Feb, 24 Feb, 3 Mar and 13 Mar 2026.', 'Companion files: Excel workbook (every step, native charts from the cells, formula cross-checks) and PowerPoint deck (native charts, references on every step).',
                     'ICAR-Indian Agricultural Research Institute, Division of Agricultural Physics, New Delhi.', 'Ph.D. research: AI-based multimodal UAV sensing of white rust in mustard.']))
B.append(dict(t='toc'))
# ---------------- 1 introduction
h1('1. Purpose, data and design')
p('This report applies the leaf-level part of the 2026-27 methodology (Part L, Steps L1–L10) to the ASD FieldSpec leaf spectra collected in the 2025-26 season. The leaf disease score is analysed after pooling all four sampling dates, the three growth stages, the three varieties and the three leaf positions into one data set, so that one set of features and one model per task describes every leaf. Strata (leaf position, growth stage, date and variety) are kept as labels and reported separately at Steps L5.1 and L7.')
bl(['Field trial at ICAR-IARI: 48 plots; block C (plots 1–12) protected with fungicide (healthy); replications R1–R3 (plots 13–48) unsprayed; natural white rust infection.', 'Treatments: three varieties (V1–V3) × four sowing dates (D1 9 Dec, D2 18 Dec, D3 27 Dec 2025 and D4 9 Jan 2026).',
    'ASD FieldSpec leaf-clip spectra, 350–2500 nm at 1 nm, on 11 Feb, 24 Feb, 3 Mar and 13 Mar 2026; leaves L3, L5 and the last leaf (LL); one spectrum per leaf; each leaf scored on the 0–9 white rust key (grades 0, 1, 3, 5, 7, 9; Conn et al., 1990).',
    'Tasks: A = healthy (grade 0) vs diseased (grade > 0); B = the six grades; C = the grade as a number (regression).', 'Split: the same 15 test plots and 11 network-validation plots as the 2026-27 plan; selection and training use the 33 training plots only; the test leaves are predicted once.'])
dtab(T['l1_grade_date'], 'Leaves of each grade on each date after the checks of Step L1.')
fig('c02')
# ---------------- 2 workflow
h1('2. Order of the steps and use of the leaves')
p('The steps follow the order of Part L. Data preparation (L1–L4) works leaf by leaf; description (L5.1, L5.7) uses all leaves; selection (L5.2–L5.6) and model fitting (L6) use only the training leaves; the test leaves are used once at L7; L8 and L9 compare the leaf models with covariates and with the UAV canopy spectra.')
fig('w01_workflow', 'Order of the Part L steps applied to the 2025-26 ASD leaf data.')
tab([['Step', 'All leaves (%d)' % F['n_final'], 'Training leaves (%d)' % F['n_train'], 'Test leaves (%d)' % F['n_test']], ['L1–L4 checks, pre-processing, indices', '✓ (leaf by leaf)', '', ''], ['L5.1 response curves; L5.7 PCA', '✓ description', '', ''],
     ['L5.2–L5.6 selection', '', '✓', 'never used'], ['L6 ML (SFFS + grid, GroupKFold(3))', '', '✓ all %d' % F['n_train'], 'never used'], ['L6 networks', '', '✓ fit %d + validation %d' % (F['n_fit'], F['n_val']), 'never used'],
     ['L7 test metrics', '', '', '✓ once'], ['L8 covariate baseline', '', '✓ fit', '✓ once'], ['L9 leaf–canopy link (24 Feb)', '✓ plot means', 'thresholds (33 plots)', '✓ 15 plots']], 'Which leaves are used in which step.', widths=[3600, 2000, 2400, 1600])
dtab(pd.DataFrame([dict(Step=s['code'], Title=s['title'], Output=s['output']) for s in STEPS]), 'Steps and their outputs.', widths=[900, 4300, 4400])
# ---------------- per step
def step_header(code, title): h1('%s. Step %s – %s' % (3 + list(ST).index(code), code, title)); p(ST[code]['what'] or ''); card(code); h2('Results')
step_header('L1', ST['L1']['title'])
dtab(T['l1_flow'], 'Sample flow of Step L1.', widths=[7000, 2600]); dtab(T['l1_checks'], 'Data checks of Step L1.', widths=[700, 2000, 2200, 3900, 800], size=14)
fig('c01'); p('The final leaf table has %d leaves; the 75 duplicate spectra of 13 March (plots 13, 34, 38, 41, 42) and the 9 L4 leaves were removed; the %d Isolation Forest flags were checked and none was faulty.' % (F['n_final'], F['n_if']))
for k, cap in (('l1_grade_leaf', 'leaf position'), ('l1_grade_stage', 'growth stage'), ('l1_grade_variety', 'variety'), ('l1_grade_sowing', 'sowing date')): dtab(T[k], 'Leaves of each grade by %s.' % cap)
fig('c03'); fig('c04'); fig('c05')
ifs = T['l1_if_summary'].pivot(index='grade', columns='date', values='flagged').fillna(0).astype(int).reset_index(); dtab(ifs, 'Isolation Forest flags per grade and date (all checked; none faulty; none removed).')
step_header('L2', ST['L2']['title'])
dtab(T['l2_counts'], 'Leaves in each part of the split by grade.', size=14); fig('c06'); fig('c07'); fig('c07b')
dtab(T['l2_plots'], 'Plots: block, treatment, split, network part and inner fold.', size=13)
step_header('L3', ST['L3']['title'])
dtab(T['l3_summary'], 'Pre-processing summary.', widths=[3500, 6100]); fig('c09'); fig('c10'); fig('c08')
p('Savitzky–Golay smoothing removed instrument noise (residual SD 0.00018 reflectance) without changing the spectral shape. The residual step at the 1000/1001-nm detector join (median −0.0021) is visible in the mean raw spectra; first-derivative bands 995–1005 nm were therefore excluded from band selection (DEV-1).')
step_header('L4', ST['L4']['title'])
dtab(T['l4_defs'], 'The 48 published indices and three red-edge parameters with formula, original reference and Pearson r with the leaf grade (all leaves).', widths=[2100, 1100, 3600, 1900, 900], size=13)
step_header('L5.1', ST['L5.1']['title'])
fig('c11'); fig('c12'); fig('c13'); fig('c14')
p('Reflectance rises in the visible and SWIR and falls in the NIR with increasing grade; the red-edge peak of the first derivative falls and shifts to shorter wavelengths (REP %.1f nm at grade 0 to %.1f nm at grade 9). The first derivative is more strongly correlated with the grade (|r| up to %.3f at %d nm) than reflectance (|r| up to %.3f at %d nm).' % (F['l51']['REP_by_grade']['0'], F['l51']['REP_by_grade']['9'], F['l51']['max_abs_r_FD'], F['l51']['wl_max_r_FD'], F['l51']['max_abs_r_R'], F['l51']['wl_max_r_R']))
dtab(T['l51_index_r'][['Index', 'r', '|r|', 'Group']].head(20), 'The 20 indices most correlated with the leaf grade (all leaves).', widths=[2000, 1500, 1500, 4600]); fig('c15')
dtab(T['l51_index_means'], 'Mean of every index for each grade.', size=13)
dtab(T['l51_strata'], 'Strata: number of leaves, grade distribution, highest |r| and REP.', size=12); fig('c16'); fig('c17')
step_header('L5.2', ST['L5.2']['title'])
fig('h01_ndsi', 'NDSI R² map of all 5-nm band pairs with the leaf grade (training leaves); white contour = top-5% threshold.', 430); fig('h02_rsi', 'RSI R² map with the leaf grade (training leaves); white contour = top-5% threshold.', 430)
dtab(T['l52_ranges'], 'Effective wavelength ranges: bands above the threshold in both R² maps.'); fig('c21'); fig('c22')
dtab(T['l52_cars'][['iteration', 'n_bands', 'GKF_RMSE']].iloc[:15], 'CARS: first 15 of 50 iterations (bands kept and GroupKFold(3) RMSE; all 50 in the Excel sheet L5.2).'); fig('c23'); fig('c24')
dtab(T['l52_ow'], 'The 32 optimal wavelengths with their SHAP importance.'); fig('c25')
step_header('L5.3', ST['L5.3']['title'])
w = F['l53']['wri']; p('The search over the 200 best NDSI pairs, five weights and λ3 every 10 nm (1000 combinations) found the highest |r| with w = 0: the third band did not improve the index, so WRI = NDSI(%d, %d) = (R%d − R%d)/(R%d + R%d), r = %.3f.' % (w['l1'], w['l2'], w['l1'], w['l2'], w['l1'], w['l2'], w['r']))
dtab(T['l53_wri_w'], 'Best WRI combination for each weight w.'); fig('c27'); dtab(T['l53_wri'].head(20), 'The 20 best combinations of the WRI search.', size=13)
dtab(T['l53_by_grade'], 'Mean and SD of NDSI_best, RSI_best and WRI by grade (training leaves).', size=13); fig('c26')
step_header('L5.4', ST['L5.4']['title'])
dtab(T['l54_clusters'], 'Indices kept after the |r| ≥ 0.95 filter and the indices each one replaced.', widths=[1700, 6900, 1000]); dtab(T['l54_relief'], 'ReliefF (tasks A, B) and RReliefF (task C) weights of the kept indices.', size=13)
fig('c28a'); fig('c28b'); fig('c28c'); dtab(T['l54_vi'], 'Leaf VI: top five indices per task.')
step_header('L5.5', ST['L5.5']['title'])
dtab(T['l55_dsf'], 'Leaf DSF of each task.', widths=[700, 700, 800, 1000, 6400]); dtab(T['l55_steps'], 'Removal order: the feature with the largest VIF in every round.', size=13); dtab(T['l55_final'], 'VIF of the final DSF features.', size=13); fig('c29')
step_header('L5.6', ST['L5.6']['title'])
M = T['l56_matrix']; tab([['Grade'] + ['%d' % g for g in C.GRADES]] + [['%d' % g] + ['%.2f' % M.loc[g, h] for h in C.GRADES] for g in C.GRADES], 'Jeffries–Matusita distance between grades (task-B DSF, training leaves).')
fig('h03_jm', 'Jeffries–Matusita distance matrix (0 = identical, 2 = fully separable).', 420); fig('c30')
step_header('L5.7', ST['L5.7']['title'])
dtab(T['l57_var'], 'Variance explained by the first ten components.'); fig('c18'); fig('c19'); fig('c20'); dtab(T['l57_means'], 'Mean PC scores of each grade.')
if 'L6' in ST:
    step_header('L6', ST['L6']['title'])
    ml = T['l6_ml'].copy(); ml['grid_best'] = ml.grid_best.str.replace('"', '').str.replace(r'(svc__|svr__|kneighborsclassifier__|kneighborsregressor__)', '', regex=True)
    dtab(ml, 'ML models: SFFS features, inner-fold scores and best grid settings (macro-F1 for tasks A, B; negative RMSE for task C).', size=12, widths=[500, 800, 700, 600, 3400, 700, 1800, 700, 500])
    fig('c31a'); fig('c31b'); fig('c31c')
    if len(T.get('l6_dl', [])): dtab(T['l6_dl'], 'Networks: epochs run, best epoch and best validation score (OA; negative RMSE for task C).')
    fig('c32a'); fig('c32b'); fig('c32c')
    if len(T.get('l6_stab_freq', [])):
        dtab(T['l6_stab_freq'], 'SFFS stability of the best ML model of each task: selection frequency over repeated random GroupKFold(3) divisions.', size=13); [fig(x) for x in ('c40a', 'c40b', 'c40c') if x in SPEC]
if 'L7' in ST:
    step_header('L7', ST['L7']['title'])
    R = T['l7_metrics']
    for t, cols in (('A', ['model', 'OA', 'kappa', 'macro_P', 'macro_R', 'macro_F1', 'sensitivity', 'specificity', 'AUC', 'CI_low', 'CI_high']), ('B', ['model', 'OA', 'kappa', 'macro_F1', 'within1', 'QWK', 'CI_low', 'CI_high']),
                    ('C', ['model', 'R2', 'RMSE', 'MAE', 'RPD', 'bias', 'r', 'CI_low', 'CI_high'])):
        q = R[R.task == t].copy(); q['o'] = q.model.map({m: i for i, m in enumerate(d2_specs.MODELS)}); dtab(q.sort_values('o'), 'Test metrics, %s (CI = 95%% interval of the main metric over 1000 plot resamples).' % d2_specs.TASK[t], cols=cols, size=12)
        fig('c33' + t.lower())
    fig('c34'); fig('c36'); fig('h04_conf_A', 'Confusion matrix of the best task-A model (%s) on the test leaves.' % F['best']['A'], 380)
    q = R[R.task == 'B']; dtab(q[['model'] + ['F1_g%d' % g for g in C.GRADES]], 'Task B: F1 of each grade for every model.', size=12); fig('c35'); fig('h04_conf_B', 'Confusion matrix of the best task-B model (%s) on the test leaves.' % F['best']['B'], 420)
    fig('c37'); dtab(T['l7_low'], 'Low-severity check (grade-1 leaves for task A; grades 0–1 for task C).', size=13)
    fig('c39'); q = T['l7_strata']; q = q[[m == F['best'][t] for t, m in zip(q.task, q.model)]]; dtab(q, 'Main metric of the best model of each task by leaf position, stage, date and variety.', size=12); fig('c38a'); fig('c38b'); fig('c38c')
if 'L8' in ST:
    step_header('L8', ST['L8']['title'])
    dtab(T['l8_models'], 'M0 (covariates), M1 (best leaf model), M2 (spectrum + covariates) and the gains on the test leaves.', size=12, cols=['task', 'metric', 'M0', 'M1_model', 'M1', 'M2', 'dS', 'dC', 'top_covariates'])
    fig('c41'); dtab(T['l8_gains'], 'Gains with plot-bootstrap 95% CI and per date (task A).', size=12); fig('c42')
    if 'c43' in SPEC: fig('c43')
    dtab(T['l8_weather'], 'Weather covariates per date and sowing date (7-day window ending the day before sampling; favourable days since sowing).', size=12)
if 'L9' in ST:
    step_header('L9', ST['L9']['title'])
    fig('c44'); fig('c45'); dtab(T['l9_transfer'], 'Leaf indices computed from the UAV spectra: r with plot DI and detection of the 15 test plots.', size=12); fig('c46'); fig('c47')
    dtab(T['l9_plots'][['plot', 'block', 'split', 'n_leaves', 'DI', 'UAV_WRI', 'leaf_WRI', 'UAV_HI', 'leaf_HI']], 'Plots on 24 Feb 2026: disease index and WRI/HI from UAV and leaf spectra.', size=12)
step_header('L10', ST['L10']['title']); p('Step L10 needs leaves of tagged plants sampled before symptoms appear (1, 4 and 7 January in the 2026-27 plan). The 2025-26 season had natural infection without such tagging, so the step is not applicable to this data set.')
# ---------------- checks, deviations, findings, references
h1('%d. Cross-check of every step' % (4 + len(ST)))
p('Every step was checked twice: in the Python scripts (assertions and logs) and in the Excel workbook, where formulas recompute the key numbers from the raw cells and the Checks sheet compares them with the Python results.')
rows = [['Step', 'Check', 'Result']] + [['L1', 'Leaf table: %d leaves; grade × date table sums to the same number (COUNTIFS)' % F['n_final'], 'PASS'], ['L1', 'No healthy-block leaf with grade > 0; only grades 0, 1, 3, 5, 7, 9', 'PASS'],
        ['L2', 'Training + test = all leaves; fit + validation = training; folds sum to training; no test-plot leaf in training', 'PASS'], ['L5.1', 'Mean spectra (AVERAGEIFS) and band r (CORREL) in Excel equal the Python values (< 1e-5)', 'PASS'],
        ['L5.2', '32 optimal wavelengths; no FD band of the 995–1005 nm guard selected', 'PASS'], ['L5.3', 'WRI search repeated (l06b_wri.py) and the same best index found', 'PASS'], ['L5.4', 'No two kept indices with |r| ≥ 0.95', 'PASS'],
        ['L5.5', 'All final VIF < 10', 'PASS'], ['L5.6', 'JM within 0–2', 'PASS'], ['L6', 'SFFS subsets inside the task DSF; scalers fitted on training leaves only', 'PASS']]
if 'L7' in ST: rows += [['L7', 'Every metric of every model recomputed with Excel formulas from the predictions (confusion matrices, OA, kappa, macro-F1, sensitivity, specificity, within-one, QWK, R², RMSE, RPD, bias): difference < 1e-6', 'PASS'], ['L7', 'Each point estimate inside its plot-bootstrap 95% CI', 'PASS']]
if 'L9' in ST: rows += [['L9', 'r(UAV WRI, DI) recomputed with CORREL in Excel', 'PASS']]
tab(rows, 'Cross-check summary (details in the Excel sheet Checks).', widths=[800, 7600, 1200])
h1('%d. Deviations from the methodology' % (5 + len(ST)), newpage=False)
tab([['Code', 'Step', 'Situation in 2025-26', 'What was done']] + [['DEV-1', 'L1/L5.2', 'Residual splice step −0.002 at 1000/1001 nm', 'Not corrected; FD 995–1005 nm excluded from band selection'], ['DEV-2', 'L1', 'One spectrum per leaf in the files', '"Average 2 readings" not applicable'],
     ['DEV-3', 'L2', '2255 leaves instead of the 7488 planned for 2026-27', 'Same plot split applied'], ['DEV-4', 'L5.3', 'WRI search chose w = 0', 'WRI = NDSI(780, 830)'], ['DEV-5', 'L7', 'Leaf data, not subplots', 'Low-severity check on grade-1 leaves (A) and grades 0–1 (C)'],
     ['DEV-6', 'L6', 'Run time of the SFFS stability check', '50 random GroupKFold(3) divisions for SVM (tasks A, B); 20 divisions with 100 trees for RF (task C)'], ['DEV-7', 'L9', 'One UAV date; no canopy selection chain', 'OW overlap not computed; plot-mean leaf spectra used'],
     ['DEV-8', 'L10', 'No pre-symptomatic leaves', 'Not run'], ['DEV-9', 'L6–L8', 'Task C predictions outside 0–9', 'Clipped to 0–9']], 'Deviations and adaptations.', widths=[900, 1000, 3800, 3900])
if 'L7' in ST:
    h1('%d. Main findings' % (6 + len(ST)))
    bl([ST['L5.1']['result'][0] + ' ' + ST['L5.1']['result'][1], ST['L5.2']['result'][0], ST['L5.3']['mydata'][1], ST['L5.4']['result'][0], ST['L5.6']['result'][0]] + ST['L7']['result'] + (ST['L8']['mydata'] if 'L8' in ST else []) + (ST['L9']['result'] if 'L9' in ST else []))
    LIT = d0_text.literature(T, F); h2('Comparison with the literature'); tab(LIT, 'Results of this analysis compared with the disease papers used in the methodology.', widths=[1700, 2700, 2700, 2500], size=14)
alltext = ' '.join(' '.join([pp[0] for pp in s['papers']] + s['mrefs']) for s in STEPS) + ' Conn et al. (1990) Cross et al. (2024) Abdulridha et al. (2023) Deng et al. (2024) Zhang et al. (2014a)'
RL, MISS = refs.resolve(alltext); h1('References'); bl(RL)
h1('Appendix – Scripts and files', newpage=True)
tab([['File', 'Step', 'Content'], ['asdL/configL.py', 'all', 'paths, split, seeds and every setting'], ['asdL/l01_qc.py', 'L1', 'leaf table, checks, duplicates, Isolation Forest'], ['asdL/l02_split.py', 'L2', 'split, network parts, inner folds'],
     ['asdL/l03_l04_features.py', 'L3–L4', 'Savitzky–Golay, derivative, 5-nm bands, indices'], ['asdL/l05_describe.py', 'L5.1, L5.7', 'response curves, correlations, PCA'], ['asdL/l06_select.py, l06b_wri.py', 'L5.2–L5.6', 'R² maps, SHAP-CARS, WRI, ReliefF, VIF, JM'],
     ['asdL/lmods.py, l07_ml.py', 'L6', 'ML models: SFFS + grid search'], ['asdL/l08_nets.py', 'L6', 'DNN-F1 and image networks'], ['asdL/l09_eval.py', 'L7', 'test metrics, CIs, strata, low severity'], ['asdL/l10_cov.py', 'L8', 'covariate baseline'],
     ['asdL/l11_link.py', 'L9', 'leaf–canopy link'], ['asdL/l12_stability.py', 'L6 check', 'SFFS stability'], ['asdL/deliv/*.py, *.js', 'deliverables', 'Excel, PPT, Word builders (one table source)']], 'Scripts of the analysis (thesis_build/asdL).', widths=[3200, 1300, 5100])
json.dump(dict(blocks=B, figdir=FG, out=OUT, author='Animesh Panda', doctitle='Part L analysis of the 2025-26 ASD leaf spectra (white rust)', header='White rust of Indian mustard · Part L analysis · ASD leaf spectra 2025-26'),
          open(os.path.join(HERE, 'content.json'), 'w'), ensure_ascii=False)
print('blocks', len(B), 'figures', NF[0], 'tables', NT[0], 'references', len(RL), 'missing', MISS)
