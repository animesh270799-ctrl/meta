from k0_lib import *


def add():
    B.append(dict(t='title', title='White rust of Indian mustard: the grouped 70:30 leaf analysis, step by step',
                  subtitle='Which step comes after which, which leaves each step uses, how each step is done, what every table and figure shows, and how to repeat the analysis on a new data set',
                  lines=['Prepared for presentation to the Chairman, Advisory Committee',
                         'Animesh Panda · Ph.D. (Agricultural Physics) · ICAR-Indian Agricultural Research Institute, New Delhi',
                         'Companion to the report ~~Leaf-level hyperspectral detection and severity estimation of white rust in Indian mustard – grouped 70:30 hold-out~~, its Excel workbook and the seminar slides ASD_2025-26_70-30_leaf_analysis_seminar.pptx',
                         'Data: 2330 leaf spectra (ASD FieldSpec, contact probe), 48 plots, 4 dates (11 February – 13 March 2026), natural infection']))
    B.append(dict(t='toc'))

    h1('How to use this document')
    p('This document is a protocol. It describes the 70:30 analysis of the 2025-26 leaf spectra in the exact order in which it was run, from the raw files to the '
      'delivered models. For every step it says which leaves were used, what was done with them, with which settings, what came out and which step used that output next. '
      'Every one of the 46 tables and 38 figures of the 70:30 report is reproduced and explained, and four new figures show the data flow, the split search and the inner folds.')
    p('The analysis has 16 steps. Chapter 1 shows all of them on one page, with a diagram of the data flow and a matrix of which leaves each step uses. '
      'Chapters 2 to 9 then go through the steps one by one. Each step has the same parts:')
    bl('**Step card** – a table with the purpose, the data used (which leaves and plots), the input, the procedure as numbered sub-steps, the settings, the output and the next step, '
       'the script, the references, the matching seminar slides, and what to change on a new data set.',
       '**Tables and figures** of the report that belong to the step. After each one an explanation panel gives: ~~What it shows~~, ~~How to read it~~, ~~What we found~~, '
       '~~What it means~~ and ~~Say to the chairman~~.',
       '**Notes** on choices, alternatives and possible questions.')
    p('Captions give the number of the item in the 70:30 report (for example "report Table 9"), so the report, the slides and this document can be used side by side. '
      'Chapter 10 is a checklist for repeating the whole analysis on another data set (another season, another site or UAV plot spectra), with every setting in one table and the scripts in run order.')

    box('Names of the data subsets used in this document.', [
        '**ALL** – all 2330 leaf spectra of the 48 plots and four dates.',
        '**TRAIN** – the 1631 leaves of the 33 training plots (70.0% of the leaves). Every step that learns anything uses only these leaves.',
        '**TEST** – the 699 leaves of the 15 test plots (30.0%). They are locked away and used once, at the end, to measure accuracy.',
        '**Inner folds** – for the machine-learning models TRAIN is cut three times by plot (GroupKFold(3)): each time 22 plots fit a candidate model and 11 plots score it.',
        '**DL-FIT / DL-VAL** – for the networks TRAIN is cut once: 22 plots (1090 leaves) fit the weights and 11 plots (541 leaves) decide when to stop training.',
        '**UNS-TRAIN / UNS-TEST** – the unsprayed (naturally infected) leaves of the training plots (1379 leaves, 25 plots) and of the test plots (573 leaves, 11 plots); used by the covariate baseline.',
        '**Other splits** – the LORO predictions of the earlier analysis, 20 other grouped 70:30 splits and 5 random leaf-level 70:30 splits; used only to compare designs (Step 15).'], kind='method')

    h1('Summary of the 70:30 analysis')
    h3('What was done')
    p('White rust developed naturally in 48 plots at IARI, New Delhi, in 2025-26: one fungicide-sprayed healthy block (plots 1–12) and three unsprayed replications (R3 13–24, R2 25–36, '
      'R1 37–48), each with three varieties and four sowing dates. On four dates, 2330 single leaves were measured with an ASD contact probe (350–2500 nm) and scored on the 0–9 scale.')
    p('The leaves were divided once into a **training set** and a **test set** by whole plots: 33 training plots with 1631 leaves and 15 test plots with 699 leaves. The 15 test plots were '
      'chosen by fixed rules (4 healthy + 11 unsprayed plots, all 11 from different treatments, spread over replications, varieties and timings) and, among 5000 candidates, the one closest '
      'to 30% of the leaves and to the overall grade and date mix (seed 2026). All feature selection, model choice, tuning and training used the training plots only. '
      'The test plots were used once, at the end. This design is called a **grouped, stratified 70:30 hold-out** (Roberts et al., 2017; Kuhn and Johnson, 2013).')
    h3('What was found')
    nl('**Detection** of a diseased leaf (task A) was reliable: SVM reached macro-F1 0.826 and AUC 0.930 on the 699 test leaves.',
       '**Six grades** (task B) remained difficult: the best model (random forest) reached macro-F1 0.374, but 77% of the leaves were placed within one grade and the quadratic weighted kappa was 0.657.',
       '**Severity score** 0–9 (task C): random forest reached R² 0.517 and RMSE 1.92 grades.',
       '**Machine learning and deep learning** were within one plot-bootstrap standard error of each other; DT-EDNet reached 0.808 (A), 0.313 (B) and R² 0.473 (C).',
       '**Spectra versus calendar**: inside the unsprayed plots a model without spectra (crop age, timing, variety, stage, weather) detected disease as well as the spectra, but the spectra added '
       '+0.072 macro-F1 for six grades and +0.102 R² for the score (both real gains: 95% plot-bootstrap interval above zero).',
       '**70:30 versus LORO**: on the same 699 test leaves the 70:30 models were really better in 17 of 30 model–task comparisons, never really worse. Over 20 other 70:30 splits, however, '
       'they beat LORO on the same leaves in only 43% of the cases. The gain depends on which plots are drawn, so the honest answer is "only partly".')
    h3('How to present it')
    p('Present the 70:30 split as the main design because it is simple to explain and it delivers models whose accuracy was measured on plots they never saw. '
      'Add two sentences of caution: one split gives one test set of 15 plots, so the accuracy carries the uncertainty shown by the plot bootstrap and by the 20 repeated splits; and the '
      'decisive test is an independent season or site (2026-27, Bharatpur).')

    box('Corrections to the report and the slides found while writing this protocol.', [
        '**Which leaves trained the delivered models.** Report Tables 45–46 captions, Conclusion 5 and Table 43 (row 2.7.1), and seminar slides 18 and 69 say "trained on all (2330) leaves" or '
        '"refitted on all leaves". This is a slip copied from the LORO report. The delivered 70:30 models are exactly the tested models, trained on the 1631 leaves of the 33 training plots and '
        'never refitted (code a9_final.py; README of the model folder; report section 2.13 and slide 67 are correct). The captions are corrected in this document.',
        '**Rule for a real gain in the covariate baseline.** Report section 3.12 says that values marked ✓ "meet all three criteria", and slide 21 lists "larger than the fold SD and same sign in all three folds". '
        'With one test set there are no folds; the rule actually applied (code a11_covariate.py, caption of report Table 35) is only "the 95% plot-bootstrap interval excludes zero".',
        '**Transfer tests.** Report section 3.11 compares the transfer results with "the cross-validated value". The leave-one-variety-out and leave-one-timing-out tests do not depend on the '
        'train/test split; they were run on all 2330 leaves and are the same numbers as in the LORO report. They should be compared with the 70:30 test value (score RMSE 1.92–2.10).',
        '**Two feature sets with the same name.** Conclusion 2 lists the disease-specific feature set of Objective 1, computed on all leaves to describe the disease. The models use the sets selected '
        'on the training plots (report Table 26). Both are correct; Chapter 4 explains the difference.',
        '**Report Table 4**: the crop age of the "All" row is 33–94 days after sowing, not 6–36 (corrected here). None of these points changes a result.'], kind='caution')


def overview():
    h1('1. The whole analysis on one page')
    p('The 16 steps of the analysis are listed below in the order in which they were run. The first four describe the experiment and the data. Step 5 divides the plots into training and test '
      'plots. Steps 6 and 7 do not learn anything that the models use: pre-processing works leaf by leaf, and the Objective 1 description summarises how the disease changes the spectrum. '
      'Steps 8 to 10 learn from the training plots only. Step 11 opens the test plots once. Steps 12 to 16 explain, check and deliver the results.')
    rows = [['Step', 'What is done', 'Leaves used', 'Main output (→ used by)', 'Script', 'Report / slides'],
            ['1', 'Field experiment: 48 plots, healthy block + R1–R3, 3 varieties × 4 sowing dates', '–', 'design table (→ 4, 5)', '–', '2.1 / 8'],
            ['2', 'Leaf spectra (ASD contact probe) and 0–9 grade of the same leaf, 4 dates', 'ALL', '2330 spectra + grades (→ 4)', 'a0_load.py', '2.2 / 9'],
            ['3', 'Daily weather; 7-day windows; favourable days; crop age (DAS)', 'ALL', 'covariates (→ 14)', 'a5_extra.py', '2.3 / 10'],
            ['4', 'Join layout, labels (tasks A, B, C), quality checks', 'ALL', 'meta.csv (→ 5, 6)', 'a1_prep.py', '2.4–2.5 / 11–13'],
            ['5', 'Grouped, stratified 70:30 split of whole plots', 'ALL (plot level)', 'fold column: 33 TRAIN / 15 TEST plots (→ 8–16)', 'split_lib.py, a1_prep.py', '2.6 / 13'],
            ['6', 'Smoothing, 400–2400 nm, first derivative, 5-nm bands, 47 index features', 'ALL (leaf by leaf)', 'prep.npz, indices.csv (→ 7, 8)', 'a1_prep.py', '2.7–2.8 / 14'],
            ['7', 'Objective 1 description: response, maps, SHAP-CARS, WRI, ReliefF, VIF, PCA', 'ALL', 'o1_*.csv, Tables 22–25 (→ discussion)', 'a2_obj1.py', '2.9, 3.1–3.4 / 15, 22–35'],
            ['8', 'Feature selection repeated for the models', 'TRAIN', 'fold_selection.json: OW, VI, DSF per task (→ 9, 10, 14)', 'a3_select.py', '3.5 / 35'],
            ['9', 'ML: scaler, SFFS and grid search in inner GroupKFold(3), refit', 'TRAIN (inner folds)', '15 ML models + test predictions (→ 11, 16)', 'a3_ml.py', '2.10, 3.6 / 16, 37'],
            ['10', 'DL: pseudo-images, early stopping on validation plots', 'DL-FIT / DL-VAL', '15 networks + test predictions (→ 11, 16)', 'a4_dl.py', '2.10, 3.7 / 16–17, 44'],
            ['11', 'Test evaluation once; plot bootstrap (1000)', 'TEST', 'metrics_all.csv, Tables 29–31 (→ 15)', 'a5_metrics.py', '3.8 / 38–43'],
            ['12', 'Feature configurations (OW, VI, DSF); DT-EDNet ablation', 'DL-FIT / DL-VAL → TEST', 'Tables 32–33', 'a4_dl.py', '3.9 / 45–46'],
            ['13', 'SHAP; strata; transfer LOVO/LOTO; selection stability', 'ALL / TEST', 'Figures 29–31, 19', 'a5_extra.py', '3.10–3.11 / 47–49'],
            ['14', 'Covariate baseline M0, M1, M2; gains with plot bootstrap (2000)', 'UNS-TRAIN / UNS-TEST', 'Tables 34–35', 'a11_covariate.py', '2.11, 3.12 / 19–21, 50–52'],
            ['15', 'Comparison with LORO: side by side, paired, 20 splits, leakage', 'TEST + other splits', 'Tables 38–42', 'c1_repeat.py, c2_compare.py', '4 / 53–60'],
            ['16', 'Deliverables: tested models, Excel, Word, slides; methodology check', 'TRAIN (models)', 'model folder, Tables 43–46', 'a9_final.py', '7, App. A / 68–69']]
    tab('master', rows=rows, caption='Master list of the 16 steps in run order, with the leaves each step uses, its output and the step that uses the output.', widths=[500, 3000, 1450, 2350, 1300, 1050], size=15)
    read(shows='The complete protocol in one table: what is done in each step, on which leaves, what comes out, and where it is in the scripts, the report and the slides.',
         how='Read from top to bottom: each row can only start when the rows above it have produced their output. "Leaves used" uses the subset names of the box at the start of the document; '
             'the arrow in the output column names the later step that uses it.',
         found='Only Steps 8, 9, 10 and 14 learn from data that the final models depend on, and all of them use training plots only. TEST appears for the first time in Step 11.',
         means='This is the property that makes the test accuracy honest: nothing the models know – not the features, not the hyper-parameters, not the stopping epoch – was chosen while looking at the test plots (Varma and Simon, 2006; Cawley and Talbot, 2010).',
         say='"The analysis has 16 steps. Everything that learns uses the 33 training plots; the 15 test plots are opened once, in Step 11."')
    myfig('flow', 'p01_dataflow.png', 'Data flow of the 70:30 analysis: which leaves go into which step. Blue = training plots only; dark = test plots (locked until Step 11); green = per-leaf processing and description on all leaves; purple = separate analyses on the same split.')
    read(shows='How the 2330 leaves move through the analysis.',
         how='Start at the top box. Arrows show "output used by". The red arrows mark the only route by which the test plots are touched: the 30 trained models predict them once in Step 11.',
         found='Pre-processing (Step 6) and the Objective 1 description (Step 7) use all leaves; Step 5 sends 33 plots to TRAIN and 15 to TEST; Steps 8–10 work inside TRAIN; the deep-learning step '
               'further divides TRAIN into 22 fitting and 11 validation plots; the covariate baseline (Step 14) uses only the unsprayed leaves of the same split.',
         means='Steps 6 and 7 can safely use all leaves because they do not choose anything the models use: smoothing and derivatives are computed for each leaf alone, and the Objective 1 results '
               'are a description of the disease. Every model input is chosen again in Step 8 from TRAIN only.',
         say='"Here is the data flow: all leaves are processed the same way, then the plots are split once, and everything that learns stays inside the training plots."')
    myfig('matrix', 'p04_step_data_matrix.png', 'Which leaves each step uses. D = describe, L = learn or fit, E = evaluate only.')
    read(shows='A matrix of steps (rows) and data subsets (columns).',
         how='A blue L means that something is chosen or fitted from those leaves; an orange E means that predictions are only scored; a green D means a description without a predictive model.',
         found='The TEST column contains only E. The TRAIN column contains all the L marks of the delivered models (Steps 8, 9, 10, 16). Transfer tests (13c) and the comparison runs (15c) learn on '
               'their own training parts, which are different splits of ALL; they are separate checks and do not feed the delivered models.',
         means='Anyone can check from this matrix that the test plots never influenced the models.',
         say='"The test column has only evaluation marks: the test plots were scored, never used to learn."')
    h2('1.1 The scripts in run order')
    p('The analysis is a chain of Python scripts in the folder asd7030. The shell script run_all.sh runs them in this order; each finished step leaves a marker file, so the chain can be restarted.')
    rows = [['Order', 'Script', 'Step', 'Reads', 'Writes'],
            ['1', 'a0_load.py', '2', 'four Excel files of the ASD export', 'meta_raw.csv, X_leaf.npy (1-nm spectra)'],
            ['2', 'a1_prep.py (+ split_lib.py, split_cfg.py)', '4, 5, 6', 'meta_raw, X_leaf', 'meta.csv (with fold), split.json, prep.npz, indices.csv'],
            ['3', 'a2_obj1.py', '7', 'prep.npz, indices.csv, meta.csv', 'o1_*.csv, o1_results.json'],
            ['4', 'a3_select.py', '8', 'prep.npz, indices.csv, meta.csv (fold)', 'fold_selection.json, fold0_indices.csv'],
            ['5', 'a3_ml.py (+ a3_ml_models.py)', '9', 'fold_selection.json', 'ml_models/*.joblib, ml_predictions.csv, ml_selection.csv'],
            ['6', 'run_dl.sh → a4_dl.py / a4_par.py', '10, 12', 'fold_selection.json', 'dl_models/*.pt, dl_main.json, dl_config.json, dl_ablation.json'],
            ['7', 'a5_extra.py (+ a5_metrics.py)', '3, 11, 13', 'all predictions, weather file', 'metrics_all.csv, strata, SHAP, stability, weather tables'],
            ['8', 'a6_figs.py', '–', 'all outputs', 'fig/f00–f34'],
            ['9', 'a11_covariate.py, a12_figs_cov.py', '14', 'meta.csv, weather, fold_selection.json', 'cov2_*.csv, f32–f34'],
            ['10', 'a9_final.py ml / dl, a13_cov_models.py, a9_readme.py', '16', 'trained models', 'model folder with README and predict_white_rust.py'],
            ['11', 'c1_repeat.py, splitcmp/c2_compare.py', '15', 'LORO and 70:30 predictions', 'cmp_*.csv, f35–f39'],
            ['12', 'a7_excel.py, a10_word.py, a8_ppt.js', '–', 'everything', 'Excel workbook, Word/PDF report, seminar slides']]
    tab('scripts', rows=rows, caption='Scripts of the 70:30 pipeline in run order (folder asd7030; the comparison scripts are in splitcmp).', widths=[600, 2700, 800, 2500, 3000], size=15)
    read(shows='Which program does which step, what it reads and what it writes.',
         how='The output of one row is the input of a later row. The settings that define the split are in split_cfg.py (TEST_FRAC = 0.30, SEED = 2026).',
         means='To repeat the analysis on new data, the raw files are replaced and the chain is run again from the top; Chapter 10 lists what has to be checked before each script.',
         say='"The whole analysis is reproducible: twelve scripts in a fixed order, with the split fixed by a seed."')
