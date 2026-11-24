"""Collect every output of the hold-out analyses (70:30, 80:20) and their comparison with LORO into numbered step folders, each with a README,
and zip them: outputs/ASD_2025-26_validation_comparison_step_by_step(.zip)."""
import os, shutil, json, glob, zipfile
T = '/home/user/meta/thesis_build/'; OUTP = T + 'outputs/'; TOP = OUTP + 'ASD_2025-26_validation_comparison_step_by_step/'
DES = [('LORO', T + 'asd26/', 'ASD_2025-26_'), ('70-30', T + 'asd7030/', 'ASD_2025-26_70-30_'), ('80-20', T + 'asd8020/', 'ASD_2025-26_80-20_')]
DES = [d for d in DES if os.path.exists(d[1] + 'data/metrics_all.csv')]
if os.path.exists(TOP): shutil.rmtree(TOP)
def put(step, sub, files, src):
    dst = TOP + step + ('/' + sub if sub else '') + '/'; os.makedirs(dst, exist_ok=True); n = 0
    for f in files:
        for p in glob.glob(src + f):
            if os.path.isfile(p): shutil.copy(p, dst + os.path.basename(p)); n += 1
    return n
README = {}
STEPS = [
 ('01_Data_and_quality_control', 'The 2330 leaf spectra (ASD contact probe, 4 dates, 48 plots, L3/L5/LL) with plot, treatment and grade; counts and checks. Same data in all three designs.',
  [('', ['data/meta.csv', 'data/disease_progress.csv', 'data/weather_covariates.csv', 'fig/f01_dataset.png', 'fig/f15_weather_progress.png'], 0)]),
 ('02_Validation_designs', 'How the leaves were divided: LORO (3 folds by replication, healthy plots rotated) and the grouped, stratified 70:30 and 80:20 hold-out splits (whole plots; split_lib.py, seed 2026). split_plots.csv lists every plot with its set; split.json gives the test plots and leaf counts.',
  [('70-30', ['data/split.json', 'data/split_plots.csv', 'fig/f35_split_map.png', 'split_lib.py', 'split_cfg.py'], 1), ('80-20', ['data/split.json', 'data/split_plots.csv', 'fig/f35_split_map.png', 'split_cfg.py'], 2)]),
 ('03_Objective1_spectral_response', 'Spectral response to white rust on all leaves (mean and derivative spectra, correlation, NDSI/RSI maps, SHAP-CARS, WRI, ReliefF, VIF). Descriptive, therefore identical in all designs.',
  [('', ['data/o1_results.json', 'data/o1_mean_spectra.csv', 'data/o1_corr_curves.csv', 'data/o1_relief.csv', 'fig/f0[2-9]_*.png', 'fig/f1[0-4]_*.png', 'fig/f30_*.png'], 1)]),
 ('04_Feature_selection_on_training_plots', 'Objective 1 selection repeated on the training part only (no test leaves): optimal wavelengths, best NDSI/RSI, WRI, ReliefF indices and the disease-specific feature set of each training set.',
  [('LORO', ['data/fold_selection.json'], 0), ('70-30', ['data/fold_selection.json', 'data/selection_stability.csv', 'fig/f29_stability.png'], 1), ('80-20', ['data/fold_selection.json', 'data/selection_stability.csv', 'fig/f29_stability.png'], 2)]),
 ('05_Machine_learning_models', 'SVM, RF, XGBoost, k-NN, PLS-DA/PLSR with SFFS and grid search (inner GroupKFold by plot): chosen features and parameters, test predictions.',
  [(k, ['data/ml_selection.csv', 'data/ml_predictions.csv'], i) for i, k in enumerate(['LORO', '70-30', '80-20'])]),
 ('06_Deep_learning_models', 'DNN-F1, DT-EDNet, EfficientNet-B0, ResNet18, ConvNeXt V2-Atto (early stopping on one third of the training plots): run summaries, configuration and ablation.',
  [(k, ['data/dl_runs.csv', 'data/dl_summary_config.csv', 'data/dl_summary_ablation.csv', 'fig/f21_*.png', 'fig/f22_*.png', 'fig/f23_*.png'], i) for i, k in enumerate(['LORO', '70-30', '80-20'])]),
 ('07_Metrics_and_best_models', 'Test metrics of all models, best models, confusion matrices, ROC, predicted vs observed, strata.',
  [(k, ['data/metrics_all.csv', 'data/best_models.json', 'data/all_predictions.csv', 'data/strata_metrics.csv', 'fig/f1[6-9]_*.png', 'fig/f20_*.png', 'fig/f2[4-8]_*.png'], i) for i, k in enumerate(['LORO', '70-30', '80-20'])]),
 ('08_Covariate_baseline', 'Models without spectra (crop age, timing, variety, stage, weather) vs spectra vs spectra + covariates on the unsprayed leaves; gains with plot-bootstrap intervals and DeLong tests.',
  [(k, ['data/cov2_*.csv', 'data/cov2_summary.json', 'fig/f3[1-4]_*.png'], i) for i, k in enumerate(['LORO', '70-30', '80-20'])]),
 ('09_Model_files', 'Saved models with the prediction script. LORO: refitted on all leaves. 70:30 and 80:20: exactly the tested models, trained on the training plots only. CNN weights are in the separate _CNN_weights zip.',
  []),
 ('10_Comparison_LORO_vs_70-30_vs_80-20', 'Is the accuracy improving? Side by side, same test leaves (paired plot bootstrap), 20 repeated splits per ratio, leakage check with random leaf-level splits, feature overlap. Per-design files: cmp_*.csv; three-way: cmp3_*.csv.',
  [('70-30', ['data/cmp_*.csv', 'data/cmp_summary.json', 'fig/f3[6-9]_*.png'], 1), ('80-20', ['data/cmp_*.csv', 'data/cmp_summary.json', 'fig/f3[6-9]_*.png'], 2)]),
 ('11_Reports', 'Word reports (+ PDF), Excel workbooks and slides: LORO (earlier), 70:30, 80:20 and the three-way comparison. Every table and figure is in all three formats.', [])]
SRC = {d[0]: d[1] for d in DES}; keys = [d[0] for d in DES]
for step, desc, items in STEPS:
    os.makedirs(TOP + step, exist_ok=True); n = 0
    for sub, files, i in items:
        k = ['LORO', '70-30', '80-20'][i] if sub == '' else sub
        if k not in SRC: continue
        n += put(step, sub, files, SRC[k])
    README[step] = (desc, n)
# models
for k, d, pre in DES:
    for z in glob.glob(OUTP + pre + 'models*.zip'):
        if k == 'LORO' and ('70-30' in z or '80-20' in z): continue
        os.makedirs(TOP + '09_Model_files/' + k, exist_ok=True); shutil.copy(z, TOP + '09_Model_files/' + k + '/')
# comparison
n = put('10_Comparison_LORO_vs_70-30_vs_80-20', 'three-way', ['out/cmp3_*', 'fig/c0*.png', 'c1_repeat.py', 'c2_compare.py'], T + 'splitcmp/') + put('10_Comparison_LORO_vs_70-30_vs_80-20', 'three-way', ['c1_repeat.py'], T + 'asd7030/')
for k in ('70-30', '80-20'):
    if k in SRC: put('10_Comparison_LORO_vs_70-30_vs_80-20', k, ['data/cmp_repeat_runs.csv', 'data/cmp_repeat_selection.csv'], SRC[k])
# reports
for k, d, pre in DES:
    put('11_Reports', k, [pre + 'leaf_analysis_white_rust.xlsx', pre + 'leaf_analysis_white_rust_report.docx', pre + 'leaf_analysis_white_rust_report.pdf', pre + 'leaf_analysis_seminar.pptx'], OUTP)
put('11_Reports', 'comparison', ['ASD_2025-26_validation_comparison_LORO_70-30_80-20*'], OUTP)
# READMEs
order = ['Read in this order. Each folder is one step of the analysis; sub-folders LORO / 70-30 / 80-20 hold the same files for each validation design.', '']
for step, (desc, _) in README.items():
    open(TOP + step + '/README.txt', 'w').write(step.replace('_', ' ') + '\n' + '=' * len(step) + '\n\n' + desc + '\n\nFiles:\n' + '\n'.join('  ' + os.path.relpath(p, TOP + step) for p in sorted(glob.glob(TOP + step + '/**/*', recursive=True)) if os.path.isfile(p) and not p.endswith('README.txt')) + '\n')
    order.append('%s\n    %s' % (step, desc))
S = json.load(open(T + 'splitcmp/out/cmp3_summary.json')) if os.path.exists(T + 'splitcmp/out/cmp3_summary.json') else {}
order += ['', 'Answer (from step 10):'] + ['  %s: %s' % (k, v['verdict']) for k, v in S.items()]
open(TOP + '00_README.txt', 'w').write('White rust leaf models, ASD spectra IARI 2025-26 – hold-out splits 70:30 and 80:20 compared with leave-one-replication-out (LORO)\n\n' + '\n'.join(order) + '\n')
z = OUTP + 'ASD_2025-26_validation_comparison_step_by_step.zip'
with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as Z:
    for p in sorted(glob.glob(TOP + '**/*', recursive=True)):
        if os.path.isfile(p): Z.write(p, os.path.relpath(p, OUTP))
print('folders', len(STEPS), 'files', sum(1 for p in glob.glob(TOP + '**/*', recursive=True) if os.path.isfile(p)), 'zip MB %.1f' % (os.path.getsize(z) / 2 ** 20))
