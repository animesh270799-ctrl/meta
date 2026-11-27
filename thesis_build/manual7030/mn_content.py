"""Content of the step-by-step analysis manual. Script listings are read from thesis_build/wrguide, so the manual always shows the real code."""
from dsl import *
import os, re
G = '/home/user/meta/thesis_build/wrguide/'
BOX = '☐ '


def listing(fn, title=None):
    lines = open(G + fn).read().rstrip('\n').split('\n')
    p('**%s** – %s (%d lines). The same file is in the scripts folder; do not retype it.' % (fn, title or 'full script', len(lines)))
    for k in range(0, len(lines), 20): code(*lines[k:k + 20])


def checks(*items): bl(*[BOX + t for t in items])


def files(rows): tab('files_%d' % len(B), rows=[['File written', 'Contents']] + rows, caption='Files written by this step (in the out folder).', widths=[3200, 6400], size=16)


def step(n, title, goal, method, before, do, does, settings, check, out, fail, script):
    h1('Step %s – %s' % (n, title))
    box('Goal.', goal + ' (Methodology: %s.)' % method, kind='method')
    h3('Before you start'); checks(*before)
    h3('Do'); nl(*do)
    cmds = re.findall(r'python \S+\.py(?: (?:main|config|ablation|--search|\S+\.xlsx))?', ' '.join(do))
    if cmds: p('Commands to type in the Anaconda Prompt (inside the scripts folder):'); code(*cmds)
    h3('What the script does'); nl(*does)
    if settings: h3('Settings used (config.py)'); bl(*settings)
    h3('Check before you continue'); checks(*check)
    h3('Files written'); files(out)
    h3('If something goes wrong'); bl(*fail)
    h3('The script'); listing(script)


def add():
    B.append(dict(t='title', title='White rust leaf spectra 2025-26: step-by-step analysis manual',
                  subtitle='Follow the boxes in order and tick each one. Every step gives the command, what the script does, what you must see before you continue and the files it writes – from the raw ASD files to the delivered models.',
                  lines=['Animesh Panda · Ph.D. (Agricultural Physics) · ICAR-Indian Agricultural Research Institute, New Delhi',
                         'Companion to: Detailed methodology with references (grouped 70:30 design). Step codes in brackets (A5, C2, D5 …) refer to that document.',
                         'Scripts: folder wrguide (13 step scripts, 5 library files, run_all.bat). Tested end to end on the 2025-26 files.']))
    B.append(dict(t='toc'))

    h1('How to use this manual')
    nl('**Do the steps in order.** Each step reads the files written by the steps before it. The master checklist (next page) shows the order.',
       '**Tick every box.** A step is finished only when every box under "Check before you continue" is ticked. If a check fails, stop and fix it before the next step.',
       '**Run a quick test first.** Set WR_FAST=1 and run all steps once with small settings (about 20 minutes). It shows that the software and files are in order. Never use quick-test results in the thesis.',
       '**Then run the full analysis** with WR_FAST unset. Keep its out folder unchanged as the record of the analysis.',
       '**Change settings only in config.py,** never inside a step script, and write every change in your notebook.',
       '**Three rules protect the result:** (1) never change the test plots (config.TEST_PLOTS); (2) never use the Objective 1 feature lists (Step 5) as model inputs – the models use Step 6 only; (3) do not go back and change features or settings after you have seen the test metrics of Step 9.')
    box('What you need.', ['A computer with Windows 10/11 (or Linux/macOS), 8 GB RAM or more, about 5 GB free disk space.',
                           'The four ASD Excel exports of 2025-26 and the IARI daily weather file.',
                           'The scripts folder wrguide (sent with this manual as a zip file).'], kind='key')
    rows = [['Step', 'Approximate time (full run, 4-core laptop)'], ['1–4', 'a few minutes'], ['5, 6', '20–60 minutes each'], ['7', '1–3 hours'], ['8', '3–8 hours (main, config, ablation)'],
            ['9', '5–15 minutes'], ['10', '3–6 hours (transfer tests and stability repeat the selection 14 times)'], ['11', '10–30 minutes'], ['12', '5–10 hours (29 light pipelines)'], ['13', 'seconds']]
    tab('times', rows=rows, caption='Approximate running times. They vary with the computer.', widths=[1500, 8100], size=16)

    h1('Master checklist')
    rows = [['Done', 'Step', 'Script / command', 'Reads', 'Writes', 'Main check'],
            [BOX, '0 Set-up', 'install Python and packages; edit config.py', '–', '–', 'quick test runs without error'],
            [BOX, '1 Load files', 'python s01_load.py', 'raw Excel files', '01_meta_raw.csv, 01_X_raw.npy', '2339 leaf spectra, 2151 bands'],
            [BOX, '2 Quality control', 'python s02_qc.py', '01_*', '02_meta.csv, 02_X.npy, 02_qc_report.txt', '9 L4 + 75 duplicates removed → 2255 leaves'],
            [BOX, '3 Split', 'python s03_split.py', '02_meta.csv', '03_meta_split.csv, 03_split.json', 'TRAIN 1571 / TEST 684 leaves'],
            [BOX, '4 Features', 'python s04_features.py', '02_X.npy', '04_spectra.npz, 04_indices.csv, 04_continuum.csv, 04_cwt.npy', '2001 + 401 bands, 44 indices, 16 continuum features'],
            [BOX, '5 Objective 1', 'python s05_obj1.py', '03, 04', '05_* tables, figures, 05_obj1_selection.json', 'DSF of each task listed'],
            [BOX, '6 Selection on TRAIN', 'python s06_select_train.py', '03, 04', '06_selection_train.json, 06_model_features.csv', '"selection used 1571 training leaves"'],
            [BOX, '7 Machine learning', 'python s07_ml.py', '03, 06', '07_ml_models, 07_ml_predictions.csv', '15 models; 684 predictions each'],
            [BOX, '8 Deep learning', 'python s08_dl.py main / config / ablation', '03, 06', '08_dl_models, 08_dl_predictions_*.csv', '15 networks; 16 + 4 extra runs'],
            [BOX, '9 Evaluation', 'python s09_evaluate.py', '07, 08', '09_test_metrics.csv, 09_dl_config_ablation_metrics.csv, figures', '30 models + 20 extra runs scored'],
            [BOX, '10 Interpretation', 'python s10_interpret.py', '05–09', '10_shap, strata, transfer, stability', '22 transfer rows'],
            [BOX, '11 Covariate baseline', 'python s11_covariate.py', '03, 06, weather', '11_covariate_models, gains, delong', 'unsprayed 1319 / 558 leaves'],
            [BOX, '12 Design check', 'python s12_design_check.py', '03, 04', '12_design_runs.csv, 12_paired_LORO_vs_7030.csv', '27 runs'],
            [BOX, '13 Deliver models', 'python s13_deliver.py', '06–08', 'deliver folder', '15 + 15 model files']]
    tab('master', rows=rows, caption='Master checklist – tick each row when every check of that step is ticked.', widths=[600, 1500, 2200, 1300, 2500, 1900], size=15)
    myfig('order', 'mn_order.png', 'Run order of the scripts and the files that pass from one step to the next.')

    # ---------------------------------------------------------------- set-up
    h1('Step 0 – Set-up (once)')
    h3('0.1 Install Python and the packages')
    nl('Install Anaconda (Python 3.11 or newer) from anaconda.com and open the **Anaconda Prompt**.',
       'Go to the scripts folder, for example: cd "C:\\Users\\BDI LAB\\Desktop\\wrguide"',
       'Install PyTorch for the CPU: pip install torch --index-url https://download.pytorch.org/whl/cpu',
       'Install the other packages: pip install -r requirements.txt',
       'Check: python -c "import numpy, pandas, sklearn, mlxtend, xgboost, shap, statsmodels, torch; print(\'ok\')" must print ok.')
    code(*open(G + 'requirements.txt').read().rstrip('\n').split('\n'))
    h3('0.2 Put the input files in place')
    nl('Inside the scripts folder create a folder **raw**.',
       'Copy the four ASD Excel exports into raw and give them exactly these names (or change the names in config.py, RAW_FILES): asd__data_complete_labelled_110226_scored.xlsx, …_240226_…, …_030326_…, …_130326_…',
       'Copy the weather file into raw as IARI_daily_weather_2025-26.csv with the columns date, Tmax, Tmin, rain, wind, …, RH1, RH2, BSS, evap (one row per day, 1 December 2025 – 20 March 2026).',
       'Open config.py and check the PATHS block. Nothing else needs to be edited for the 2025-26 data.')
    h3('0.3 Quick test, then the full run')
    nl('Quick test: in the Anaconda Prompt type  set WR_FAST=1  and then  run_all.bat . It runs every step with small settings (about 20–30 minutes). Every step must end with its CHECK lines and no error.',
       'Delete the out and deliver folders made by the quick test.',
       'Full run: type  set WR_FAST=  (empty) and run the steps one by one as described in this manual, ticking the checks, or run  run_all.bat  and check each step afterwards. The full run can take one to two days on a 4-core laptop; Steps 7, 8, 10 and 12 take most of the time.',
       'Keep the out folder of the full run unchanged; copy it with the date in its name.')
    checks('Packages installed and the import test prints ok.', 'raw contains the four Excel files and the weather file with the expected names.', 'Quick test finished with "ALL STEPS FINISHED".', 'Quick-test out and deliver folders deleted before the full run.')

    step('1', 'Load the ASD files', 'Read the four Excel exports into one leaf table (one row per leaf) and one spectra matrix (one row per leaf, 2151 bands).', 'A2',
         ['raw contains the four Excel files named as in config.RAW_FILES.'],
         ['In the Anaconda Prompt, inside the scripts folder: python s01_load.py', 'Read the CHECK lines and the table of leaves by date and leaf position.'],
         ['Opens each file; column 1 is the wavelength (350–2500 nm).', 'Keeps every column whose first header ends with .sco (one leaf); plot-average columns are skipped.',
          'Reads the 7 header rows of each leaf: name, plot, variety, growth stage, healthy/diseased, leaf level, score.', 'Writes the leaf table, the spectra and the wavelength vector.'],
         None,
         ['Leaf columns per file: 428 (11 Feb), 540 (24 Feb), 648 (3 Mar), 723 (13 Mar).', 'CHECK line: total leaf spectra 2339 | bands 2151 | range 350.0 – 2500.0 nm | missing values 0.',
          'The table shows 9 spectra labelled L4 on 11 February (they are removed in Step 2).'],
         [['01_meta_raw.csv', 'one row per leaf: date, file column, plot, variety, stage, status, leaf position, score'], ['01_X_raw.npy', 'spectra, 2339 × 2151 (raw reflectance)'], ['01_wl.npy', 'wavelengths 350–2500 nm']],
         ['"No such file": check the folder raw and the file names in config.py.', '"wavelength grid differs": one file was exported with another resolution; export all files at 1 nm.'],
         's01_load.py')
    step('2', 'Quality control', 'Make one checked leaf table: correct plots and labels, no wrong leaf positions, no duplicated spectra, no detector step.', 'A1, A3, A5, A6',
         ['Step 1 finished; 01_meta_raw.csv and 01_X_raw.npy exist.'],
         ['python s02_qc.py', 'Open out/02_qc_report.txt and compare it with the checks below.'],
         ['Joins every plot to the plot plan (block, sowing date, variety) and stops if a variety differs from the plan.', 'Removes spectra whose leaf position is not L3, L5 or LL.',
          'Finds spectra that are identical at every wavelength and keeps the first copy; the removed columns are listed in 02_removed_duplicates.csv.',
          'Detector joins: compares the jump at 1000/1001 and 1800/1801 nm with the local slope; where the median excess is larger than 0.0005, shifts the bands above the join so that the jump equals the slope (Hueni and Bialek, 2017).',
          'Adds grade, diseased (grade > 0), unsprayed (blocks R1–R3), sowing date, crop age (DAS) and stage code; checks grades, missing values and that every date has 48 plots.'],
         ['SPLICE_JOINS = [1000, 1800]; SPLICE_MIN_STEP = 0.0005', 'LEAF_POSITIONS = L3, L5, LL; GRADES = 0, 1, 3, 5, 7, 9'],
         ['plots whose variety differs from the plan: 0', 'spectra with a leaf position other than L3/L5/LL removed: 9 (L4)', 'duplicated spectra removed: 75 (13 March 2026; plots 13, 34, 38, 41, 42)',
          'join 1000/1001 nm: corrected (median excess about −0.002 → 0)', 'join 1800/1801 nm: no step, unchanged', 'healthy-block leaves with grade > 0: 0',
          'leaves after quality control: 2255', 'grades 0/1/3/5/7/9: 552 / 389 / 409 / 501 / 278 / 126', 'dates: 419 / 540 / 648 / 648 leaves'],
         [['02_meta.csv', 'checked leaf table with labels and covariates'], ['02_X.npy', 'corrected spectra, 2255 × 2151'], ['02_qc_report.txt', 'every number of the checks'], ['02_removed_duplicates.csv', 'the 75 removed duplicate columns']],
         ['"variety differs from the plan": correct the plot number or variety in the Excel file, never in the code.', '"unknown growth stage label": a stage is spelled differently; correct it in the Excel file or add it to STAGE_CODE in config.py.'],
         's02_qc.py')
    step('3', 'The 70:30 split', 'Assign every plot to TRAIN (33 plots) or TEST (15 plots), and define the inner folds (machine learning) and the validation plots (networks).', 'B1, B2, B3',
         ['Step 2 finished; 02_meta.csv exists.', 'config.TEST_PLOTS = 1, 4, 5, 8, 13, 14, 18, 25, 27, 31, 35, 37, 44, 46, 48 (never change it).'],
         ['python s03_split.py', 'Optional, to show how the plots were chosen: python s03_split.py --search (re-runs the 5000-candidate search; the fixed plots are still used).'],
         ['Marks fold = 0 for leaves of the test plots and fold = 1 for all other leaves.', 'Chooses the 11 network validation plots at random from the training plots (seed 42).',
          'Defines the three inner GroupKFold folds of the training plots (whole plots per fold).', 'Writes the counts and plot lists to 03_split.json.'],
         ['TEST_PLOTS (fixed); SEED = 42; INNER_FOLDS = 3', 'TEST_FRAC = 0.30, SEED_SPLIT = 2026, N_CAND = 5000 (only for --search)'],
         ['TRAIN plots 33, leaves 1571 | TEST plots 15, leaves 684 (30.3%)', 'network fit / validation leaves 1045 / 526; validation plots 6, 7, 11, 19, 24, 26, 28, 30, 36, 39, 41', 'no plot on both sides: True',
          'TEST has 126 healthy-block leaves and 558 unsprayed leaves'],
         [['03_meta_split.csv', 'leaf table with the column fold (0 = TEST, 1 = TRAIN)'], ['03_split.json', 'test plots, counts, network validation plots, inner-fold plots']],
         ['"no plot on both sides: False" can only happen if the plot numbers in the files are wrong; check Step 2.'],
         's03_split.py')
    step('4', 'Pre-processing and features', 'Compute, for every leaf, the smoothed spectra, derivatives, 5-nm bands, indices, red-edge parameters, continuum-removal features and wavelet coefficients.', 'C1–C10',
         ['Step 2 finished; 02_X.npy exists.'],
         ['python s04_features.py'],
         ['Savitzky–Golay smoothing (window 11, order 2) and first derivative on 350–2500 nm; trims to 400–2400 nm (water bands kept).', '5-nm bands: mean of the five 1-nm values around each 5-nm wavelength (400, 405 … 2400).',
          '41 published indices and REP, Dr, REarea from the 1-nm spectra (Appendix A of the methodology).', 'Continuum removal over 530–760, 1080–1280, 1300–1650 and 1840–2150 nm: depth, width, area and position.',
          'Mexican-hat wavelet transform at scales 2, 4, 8, 16, 32 and 64.'],
         ['SG_WINDOW = 11, SG_ORDER = 2; WL_MIN–WL_MAX = 400–2400; BAND_STEP = 5', 'CR_FEATURES (four windows); CWT_SCALES = 2–64'],
         ['1-nm bands 2001 (400–2400 nm) | 5-nm bands 401 | indices 44 | continuum features 16', 'wavelet array (2255, 6, 2001)', 'missing values in features: 0 | REP between about 690 and 720 nm'],
         [['04_spectra.npz', 'w1, R1, FD1 (1 nm) and w5, R5, FD5 (5 nm)'], ['04_indices.csv', '41 indices + REP, Dr, REarea'], ['04_continuum.csv', '16 continuum-removal features'], ['04_cwt.npy', 'wavelet coefficients, leaves × scales × bands']],
         ['Memory error: close other programs; the wavelet array needs about 110 MB.'],
         's04_features.py')
    step('5', 'Objective 1 – description on all leaves', 'Describe how white rust changes the spectrum and which features describe it. These lists are for the thesis chapter on Objective 1; they are NOT model inputs.', 'D1–D12',
         ['Steps 3 and 4 finished.'],
         ['python s05_obj1.py', 'Open 05_obj1_log.txt and the figures 05_D1, 05_D2 and 05_D4.'],
         ['D1–D3: mean ± SD spectra by grade and difference from grade 0; correlation of every band with the grade; strata table.',
          'D4: R² maps of NDSI and RSI for all 5-nm band pairs; effective ranges (R² ≥ 0.5, else top 5% of pairs); join zones excluded.',
          'D5: SHAP-CARS – XGBoost SHAP keeps the top 40% of candidates; Monte Carlo CV (by plot) chooses the PLS components; CARS 50 iterations × 20 runs; bands in ≥ 50% of runs (≤ 15) = optimal wavelengths.',
          'D6: best NDSI and RSI; White Rust Index search. D7: |r| ≥ 0.95 filter of indices and continuum features. D8: ReliefF/RReliefF (k = 10, same-plot neighbours excluded), top 5 per task.',
          'D9: wavelet screening (separability, top 5%, regions, ReliefF top 5). D10: VIF < 10 on OW + VI + WF → DSF of each task. D11: JM distances between grades. D12: PCA.'],
         ['R2_THR = 0.5, TOP_FRAC = 0.05; SHAP_FRAC = 0.40; MCCV_SPLITS = 50; CARS_RUNS = 20, CARS_ITER = 50, CARS_KEEP = 0.5, MAX_OW = 15', 'CORR_THR = 0.95; RELIEF_K = 10; N_TOP = 5; WAVELET_TOP = 0.05; REGION_GAP = 10; VIF_THR = 10'],
         ['The log lists, in this order: D4 threshold and number of bands; D5 optimal wavelengths (at most 15); D6 best NDSI, RSI and WRI; D7 number of index features kept; D8–D10 VI, WF and DSF of tasks A, B and C; D11 JM distances.',
          'No optimal wavelength lies in 990–1010 nm or 1790–1835 nm.', 'Each DSF has about 5–15 features and every VIF of the DSF is below 10 (the chain removes features until this is true).',
          'Figures 05_D1_mean_spectra.png, 05_D2_correlation.png and 05_D4_maps.png open and show six grade curves, two correlation curves and two maps.'],
         [['05_D1_mean_spectra.csv / .png', 'mean, SD and difference spectra by grade'], ['05_D2_correlation.csv / .png', 'r of every band with the grade'], ['05_D3_strata.csv', 'mean grade and % diseased by stage, variety, leaf, date, timing'],
          ['05_D4_maps.png', 'NDSI and RSI R² maps'], ['05_D12_pca_scores.csv', 'PCA scores with grade'], ['05_obj1_selection.json', 'effective ranges, OW, NDSI/RSI/WRI, VI, WF, DSF, JM, PCA variance'], ['05_obj1_log.txt', 'the log']],
         ['XGBoost or SHAP error: reinstall them with pip (pip install --upgrade xgboost shap).', 'Very slow: it is normal (SHAP-CARS runs 20 CARS runs); run it overnight.'],
         's05_obj1.py')
    step('6', 'Feature selection on the training plots', 'Repeat the whole selection chain of Step 5 on the 1571 training leaves only. Its DSF of each task is the only input of the models.', 'E2',
         ['Steps 3 and 4 finished (Step 5 is not needed for this step).'],
         ['python s06_select_train.py', 'Open 06_select_log.txt.'],
         ['Runs exactly the same chain as Step 5 (D4–D10) on the training leaves.', 'Computes the index values of all leaves (also TEST) with the wavelengths chosen on TRAIN.',
          'Writes the selection and a table with every candidate model input for all leaves.'],
         ['Same as Step 5.'],
         ['Last line: "selection used 1571 training leaves" followed by the DSF of tasks A, B and C.', 'No optimal wavelength or wavelet window in a detector-join zone.', '06_model_features.csv has 2255 rows.'],
         [['06_selection_train.json', 'the model inputs: OW, VI, WF and DSF of each task'], ['06_model_features.csv', 'values of all selected features for all leaves'], ['06_select_log.txt', 'the log']],
         ['If the DSF of a task has fewer than 3 features, check the log of D8–D10; usually the VIF step removed many collinear derivative bands, which is acceptable.'],
         's06_select_train.py')
    step('7', 'Machine-learning models', 'Train SVM/SVR, random forest, XGBoost, k-NN and PLS-DA/PLSR for the three tasks inside the training plots, and predict the test leaves once.', 'E3–E5',
         ['Step 6 finished; 06_selection_train.json and 06_model_features.csv exist.'],
         ['python s07_ml.py', 'Watch one line per model: task, model, number of features kept, inner score, time.'],
         ['Builds a pipeline (standardisation + model) so that scaling is fitted inside each inner fold.', 'SFFS in inner GroupKFold(3) by plot: best subset of every size up to 15; keeps the smallest subset within 1% of the best inner score.',
          'Grid search on that subset with the same inner folds; refits the best setting on all training leaves (XGBoost classifiers with balanced sample weights).', 'Predicts the 684 test leaves once and saves model and predictions.'],
         ['SFFS_MAX = 15; SFFS_TOL = 0.01; INNER_FOLDS = 3; grids in s07_ml.py (models function)', 'Scoring: macro-F1 (tasks A, B); negative RMSE (task C)'],
         ['15 lines printed (5 models × 3 tasks).', '07_ml_models contains 15 .joblib files.', '07_ml_predictions.csv has 15 × 684 = 10 260 rows.', 'Inner scores: macro-F1 between 0 and 1 for A and B; negative RMSE (for example −2.0) for C.'],
         [['07_ml_models/*.joblib', 'the 15 trained models with their feature lists and settings'], ['07_ml_predictions.csv', 'test predictions (task, model, leaf, observed, predicted, score)'], ['07_ml_selection.csv', 'features kept by SFFS, settings and inner score of each model']],
         ['A model takes hours: reduce n_jobs only if the computer freezes; the result does not change.'],
         's07_ml.py')
    step('8', 'Deep-learning models', 'Train DNN-F1, DT-EDNet, EfficientNet-B0, ResNet18 and ConvNeXt V2-Atto on 22 training plots with early stopping on 11 validation plots; then the feature configurations and the DT-EDNet ablation.', 'E6–E7',
         ['Step 6 finished.'],
         ['python s08_dl.py main', 'python s08_dl.py config', 'python s08_dl.py ablation'],
         ['Scales the features with the mean and SD of the 22 fitting plots.', 'DNN-F1 uses the feature vector; the image networks use a k × k pseudo-image (k = max(3, ⌈√p⌉)).',
          'AdamW (6 × 10^{−4}, weight decay 10^{−5}), cosine schedule to 10^{−6}, batch 32, label smoothing 0.01, gradient clipping 1.2, dropout 0.03, seed 42; class-weighted loss.',
          'After every epoch scores the validation plots (macro-F1 or −RMSE); stops after 20 epochs without improvement (maximum 100); keeps the best epoch; predicts the test leaves once.',
          'config: four image networks on OW, VI, WF and DSF (task B). ablation: DT-EDNet without SE, without the dual transformer group, without both (task B).'],
         ['DL settings: lr 6e-4, weight_decay 1e-5, lr_min 1e-6, epochs 100, patience 20, min_delta 5e-5, batch 32, label_smoothing 0.01, clip 1.2, drop 0.03'],
         ['main: 15 lines; 08_dl_models has 15 .pt files; 08_dl_predictions_main.csv has 15 × 684 rows.', 'config: 16 runs; ablation: 4 runs.', 'Each line shows the number of epochs (≤ 100) and the best validation score.'],
         [['08_dl_models/*.pt', 'the 15 networks (weights, features, scaler, best epoch)'], ['08_dl_predictions_main.csv', 'test predictions of the 15 networks'], ['08_dl_predictions_config.csv / _ablation.csv', 'test predictions of the extra runs']],
         ['PyTorch not found: install the CPU version (Step 0.1).', 'Out of memory: close other programs; networks are small but run on the CPU.'],
         's08_dl.py')
    step('9', 'Evaluation on the test plots', 'Compute every metric of every model on the 684 test leaves with a bootstrap of whole test plots.', 'F1–F4',
         ['Steps 7 and 8 (main, config and ablation) finished.'],
         ['python s09_evaluate.py', 'Open 09_test_metrics.csv, 09_model_comparison.png and 09_roc.png.'],
         ['Task A: OA, kappa, macro-F1, sensitivity, specificity, balanced accuracy, AUC. Task B: OA, kappa, macro-F1, QWK, within one class, F1 of each grade. Task C: R², RMSE, MAE, RPD, bias, r.',
          'Bootstrap: draws the 4 healthy and the 11 unsprayed test plots with replacement 1000 times and recomputes the main metric → standard error and 95% interval.', 'Writes confusion matrices and two figures.',
          'Scores the 16 configuration runs and 4 ablation runs of Step 8 (task B: OA, kappa, macro-F1, QWK, within one class, with the same plot bootstrap).'],
         ['N_BOOT = 1000; SEED = 42'],
         ['09_test_metrics.csv has 30 rows (10 models × 3 tasks) with boot_SE, CI_low and CI_high.', 'Task-A rows have AUC; task-B rows have QWK and within1; task-C rows have R², RMSE and RPD.', 'CHECK line: 20 configuration / ablation runs scored (09_dl_config_ablation_metrics.csv has 20 rows).', 'From this point do not change any earlier step.'],
         [['09_test_metrics.csv', 'all metrics, bootstrap SE and 95% interval'], ['09_confusion_matrices.csv', 'confusion matrices of tasks A and B'], ['09_model_comparison.png', 'main metric of every model'], ['09_roc.png', 'ROC curves of task A'], ['09_dl_config_ablation_metrics.csv', 'metrics of the 16 configuration and 4 ablation runs']],
         ['A model missing from the table: its predictions file is missing; re-run Step 7 or 8.'],
         's09_evaluate.py')
    step('10', 'Interpretation and robustness', 'SHAP importance, metrics by stratum, transfer to a held-out variety, sowing date and sampling date, and stability of the optimal wavelengths.', 'F5–F7',
         ['Steps 5 and 9 finished.'],
         ['python s10_interpret.py'],
         ['F5: XGBoost on the Objective 1 DSF of task C (all leaves) and mean |SHAP| of every feature.', 'F6a: macro-F1 of the best ML and best DL six-grade models by stage, variety, leaf position, date and sowing date (test leaves).',
          'F6b: for each variety, sowing date and sampling date: selection chain on all other leaves, random forest (500 trees), test on the held-out group.', 'F7: optimal wavelengths of TRAIN and of the three LORO training parts; number of sets that chose each band.'],
         ['LORO_TEST (three folds); random forest 500 trees'],
         ['10_transfer.csv has 22 rows (3 varieties + 4 sowing dates + 4 dates, × tasks B and C).', '10_stability.csv lists every optimal wavelength with n_sets between 1 and 4.', '10_strata.csv has one row per level of each factor for two models.'],
         [['10_shap_importance.csv', 'mean |SHAP| per feature'], ['10_strata.csv', 'macro-F1 by stratum'], ['10_transfer.csv', 'held-out group results'], ['10_stability.csv', 'selection frequency of each optimal wavelength']],
         ['Long running time is normal (the selection chain runs 14 times).'],
         's10_interpret.py')
    step('11', 'Covariate baseline', 'Measure what crop age, sowing date, variety, stage and weather explain without any sensor, and what the spectra add.', 'G1–G3',
         ['Step 6 finished; the weather file is in raw.'],
         ['python s11_covariate.py'],
         ['Builds the covariates per leaf: 7-day weather ending the day before sampling, favourable leaf-infection and staghead days since sowing (Chattopadhyay et al., 2011), DAS (and DAS²), stage, variety and sowing date.',
          'Uses only unsprayed leaves of the same split; fits B1 (logistic / ordinal logistic / linear), random forest and the best ML model on covariates, spectra (DSF) and both.',
          'M0 = the stronger covariate-only model; M1 = best ML model on spectra; M2 = the same on spectra + covariates; gains with 2000 paired bootstrap resamples; DeLong test for the AUCs.', 'Fits the ordinal model on all unsprayed leaves to show the effect of each covariate.'],
         ['N_BOOT_GAIN = 2000; INNER_FOLDS = 3'],
         ['CHECK line: unsprayed leaves TRAIN 1319 / TEST 558.', '11_covariate_models.csv has 27 rows (3 tasks × 3 inputs × 3 models).', '11_gains.csv has 9 rows with the 95% interval and real = True/False.', '11_delong.csv has 3 rows.'],
         [['11_covariate_models.csv', 'main metric of all 27 models'], ['11_gains.csv', 'ΔS, ΔC, ΔT with intervals'], ['11_delong.csv', 'DeLong tests of task A'], ['11_ordinal_effects.csv', 'covariate effects (ordinal model)']],
         ['KeyError on a weather column: rename the columns of the weather file as in Step 0.2.'],
         's11_covariate.py')
    step('12', 'Check of the validation design', 'Show how much the test accuracy depends on which plots were drawn, how much a leaf-level split would inflate it, and compare with LORO on the same leaves.', 'H1–H3',
         ['Steps 3 and 4 finished.'],
         ['python s12_design_check.py (the longest step; run it overnight)'],
         ['Light pipeline: selection chain (10 CARS runs) on the training part; SVM (A), random forest (B), XGBoost (C) tuned in 3 inner folds; test once.',
          'Runs it under LORO (3 folds), the main 70:30 split, 20 other grouped 70:30 splits and 5 random leaf-level 70:30 splits.', 'Compares the main split with the LORO predictions of exactly the same test leaves (2000 bootstrap resamples).'],
         ['N_REPEAT_SPLITS = 20 (seed 7); N_LEAF_SPLITS = 5'],
         ['12_design_runs.csv has 27 rows: LORO 1, main 1, grouped 20, leaf-level 5.', '12_paired_LORO_vs_7030.csv has 3 rows (tasks A, B, C) with the 95% interval of the difference.'],
         [['12_design_runs.csv', 'main metric of every run'], ['12_paired_LORO_vs_7030.csv', 'paired comparison on the same test leaves']],
         ['If it stops halfway, run it again; it starts from the beginning (no partial files are used).'],
         's12_design_check.py')
    step('13', 'Deliver the models', 'Collect the tested models (trained on TRAIN only) with the selection, so that new spectra can be predicted.', 'I1',
         ['Steps 7 and 8 finished.'],
         ['python s13_deliver.py', 'To predict new spectra (same Excel format): python predict_new.py new_spectra.xlsx'],
         ['Copies the 15 ML and 15 DL models and 06_selection_train.json into the folder deliver.', 'predict_new.py applies Steps 2 (splice correction), 4 (features) and every model to the new file and writes <file>_predictions.csv.'],
         None,
         ['CHECK line: 15 ML and 15 DL models in deliver.', 'Test: python predict_new.py raw\\asd__data_complete_labelled_110226_scored.xlsx writes a predictions file with one row per column of the file.'],
         [['deliver/ml, deliver/dl', 'the 30 delivered models'], ['deliver/selection_train.json', 'the selected wavelengths and features'], ['<file>_predictions.csv', 'predictions of predict_new.py']],
         ['predict_new.py predicts every column of the new file, including plot-average columns if present; remove them first or ignore those rows.'],
         's13_deliver.py')
    listing('predict_new.py', 'prediction script for new spectra')

    h1('Final checks and where each output goes in the thesis')
    checks('Every row of the master checklist is ticked.', 'The out folder of the full run is copied with the date in its name.', 'config.py of the full run is saved with the out folder.',
           'The package versions are recorded: pip freeze > out/package_versions.txt')
    rows = [['Output file', 'Thesis item'], ['02_qc_report.txt', 'Methods: data and quality control (numbers of leaves, removed spectra, splice correction)'], ['03_split.json', 'Methods: split table (training and test plots and leaves)'],
            ['05_D1, 05_D2, 05_D4 figures and csv', 'Objective 1: mean spectra, correlation curves, NDSI/RSI maps'], ['05_obj1_selection.json', 'Objective 1: effective ranges, optimal wavelengths, WRI, selected indices, wavelet features, DSF, JM table, PCA'],
            ['06_selection_train.json', 'Objective 2: model inputs (DSF per task)'], ['07_ml_selection.csv', 'Objective 2: SFFS and grid-search table'], ['09_test_metrics.csv and figures', 'Objective 2: detection, six-grade and score tables; comparison and ROC figures'],
            ['09_dl_config_ablation_metrics.csv', 'Objective 2: network configurations and ablation'], ['10_*.csv', 'SHAP, strata, transfer and stability'], ['11_*.csv', 'Covariate baseline tables'],
            ['12_*.csv', 'Check of the validation design'], ['deliver/', 'Model files and prediction script (appendix)']]
    tab('thesis', rows=rows, caption='Where each output is used.', widths=[3400, 6200], size=16)

    h1('Appendix – library files')
    for fn, t in (('config.py', 'every setting'), ('lib_spec.py', 'pre-processing and features'), ('lib_select.py', 'feature selection chain'), ('lib_metrics.py', 'metrics and bootstrap'),
                  ('split_lib.py', 'split rules and candidate search'), ('lib_nets.py', 'network definitions'), ('run_all.bat', 'run every step in order (Windows)')):
        h2(fn); listing(fn, t)
