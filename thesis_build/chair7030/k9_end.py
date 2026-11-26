from k0_lib import *
import re

import os
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'report_refs.txt')   # reference list of the 70:30 report (pandoc text)
EXTRA_REFS = [
    'Dietterich, T.G. (1998). Approximate statistical tests for comparing supervised classification learning algorithms. Neural Computation 10(7), 1895–1923. https://doi.org/10.1162/089976698300017197',
    'Jacquemoud, S., Ustin, S. (2019). Leaf Optical Properties. Cambridge University Press, Cambridge. https://doi.org/10.1017/9781108686457',
    'Karasiak, N., Dejoux, J.-F., Monteil, C., Sheeren, D. (2022). Spatial dependence between training and test sets: another pitfall of classification accuracy assessment in remote sensing. Machine Learning 111, 2715–2740. https://doi.org/10.1007/s10994-021-05972-1',
    'Sun, X., Xu, W. (2014). Fast implementation of DeLong\'s algorithm for comparing the areas under correlated receiver operating characteristic curves. IEEE Signal Processing Letters 21(11), 1389–1393. https://doi.org/10.1109/LSP.2014.2337313',
]


def fix_t43(r):
    for row in r:
        if row[0].startswith('2.7.1'):
            row[0] = '2.7.1 Final models'; row[1] = 'Done: the 30 tested models (trained on the 1631 training leaves, never refitted) saved with feature definitions and prediction script'
    return r


def add():
    h1('10. Step 16 and how to repeat the analysis on a new data set')
    h2('10.1 Step 16 – Deliverables and methodology check')
    card('card16', '16', 'Deliverable models, workbook, report and slides (Step 2.7.1)',
         'Hand over models that can be applied to new spectra, with an accuracy that was measured honestly, and document everything.',
         'The models are those of Steps 9, 10 and 14 – trained on TRAIN (or UNS-TRAIN) only. Nothing is refitted on the test plots or on all leaves.',
         'ml_models/*.joblib, dl_models/*.pt, covariate models, fold_selection.json.',
         steps('Copy the 15 ML and 15 DL model files; reload each and check that it reproduces its own test predictions exactly.',
               'Save the 11 covariate-baseline models.',
               'Write feature_selection.json (wavelengths of NDSI_best, RSI_best, WRI; DSF per task), wr_features.py (pre-processing and indices), wr_networks.py and predict_white_rust.py.',
               'Write the README with the test accuracy of every file.',
               'Build the Excel workbook (live formulas), Word/PDF report and seminar slides; cross-check every methodology step.'),
         'The reported test accuracy is the expected accuracy of exactly these files (hold-out practice: Kuhn and Johnson, 2013).',
         'Folder ASD_2025-26_70-30_models (+ zip), workbook, report, slides.',
         'a9_final.py, a13_cov_models.py, a9_readme.py, a7_excel.py, a10_word.py, a8_ppt.js.',
         'Kuhn and Johnson (2013); Pedregosa et al. (2011); Paszke et al. (2019).',
         '67–69; appendix 125–130',
         'For external validation (2026-27, Bharatpur) apply these files with predict_white_rust.py and score the predictions; do not retrain.')
    tab('check', 43, widths=[3200, 5000, 1400], size=15, fix=fix_t43)
    read(shows='Every step of the thesis methodology and whether it was done for the leaf spectra.',
         found='All steps that apply to non-imaging leaf spectra were done; image steps (orthomosaics, crop mask, texture, thermal, 15-sensor fusion), maps, Bharatpur validation and Objective 3 do not apply or come next season.',
         caution='Row 2.7.1 of the report said "Final models on all data"; corrected here: the delivered models are the tested models trained on the training plots.',
         say='"Every step that applies to leaf spectra was performed; the rest belongs to the UAV phase."')
    tab('sheets', 44, widths=[2600, 7000], size=16)
    read(shows='The sheets of the Excel workbook.',
         means='Every table of the report is in the workbook, most with live formulas (counts, mean spectra, correlation, WRI with editable wavelengths, confusion and regression metrics), so the numbers can be checked by hand.',
         say='"All numbers can be recomputed in the Excel workbook."')
    tab('mfml', 45, caption='Machine-learning model files (the tested models, trained on the 1631 leaves of the 33 training plots; load with predict_white_rust.py). Caption corrected: the report said "trained on all 2330 leaves"', widths=[3600, 700, 1200, 4100], size=15)
    tab('mfdl', 46, caption='Deep-learning model files (the tested networks, trained on the 22 fitting plots with early stopping on 11 validation plots; load with predict_white_rust.py). Caption corrected: the report said "trained on all 2330 leaves"', widths=[3600, 700, 1500, 3800], size=15)
    read(shows='The 30 delivered model files and the features each uses.',
         how='Machine-learning models use their own SFFS subset; networks use the whole DSF of the task. The README lists the test accuracy of every file.',
         means='Because the files are the tested models, their accuracy on new plots of the same kind is expected to be close to the test values of Step 11 – with the range shown by the repeated splits.',
         say='"These are exactly the models whose accuracy I reported."')

    h2('10.2 Two ways to use a new data set')
    rows = [['Goal', 'What you do', 'What you get', 'When to use it'],
            ['External validation of the 2025-26 models', 'Pre-process the new spectra with predict_white_rust.py (same filter, bands, indices) and apply the saved models; compare with the visual grades', 'The real accuracy of the existing models on a new season or site', '2026-27 season, Bharatpur – the decisive test'],
            ['Repeat the whole analysis', 'Run Steps 2–16 on the new data with the same scripts and settings', 'New features, new models and a new test accuracy for that data set', 'A different crop stage, sensor or design; or pooling seasons']]
    tab('twoways', rows=rows, caption='Two ways to use a new data set.', widths=[2200, 3600, 2300, 1500], size=16)
    read(shows='The difference between testing the existing models and building new ones.',
         means='External validation answers "do my models work elsewhere?"; repeating the analysis answers "what would the analysis find in these data?". For the thesis, external validation is the stronger evidence.',
         say='"Next season I will first test the existing models on new data, without retraining."')

    h2('10.3 Checklist for repeating the analysis')
    nl('**Organise the data** as in Steps 2–4: one spectrum per sample (1-nm, 350–2500 nm), with plot, block, treatment, date, sample position and grade. Run the checks of a1_prep.py; stop if any check fails.',
       '**Decide the group and the strata before looking at any result**: the group is the unit whose samples are related (here the plot); the strata are the block types (here sprayed vs unsprayed).',
       '**Fix the split once** (Step 5): set TEST_FRAC and a seed in split_cfg.py, run the split, save split.json, and never draw a new split after seeing model results. If the design has no healthy block, split only the unsprayed blocks; if there are fewer than about 30 plots, prefer LORO or repeated grouped splits.',
       '**Run pre-processing and the description** (Steps 6–7) unchanged.',
       '**Run the selection on the training plots** (Step 8). Never pass the all-leaf features of Step 7 to the models.',
       '**Train inside the training plots** (Steps 9–10): inner GroupKFold(3) by plot for SFFS and grid search; a third of the training plots for early stopping.',
       '**Open the test plots once** (Step 11). Report every model, including the weak ones; do not change any model afterwards.',
       '**Explain and check** (Steps 12–13), **build the covariate baseline** (Step 14) and **measure the split luck** with 20 repeated grouped splits (Step 15).',
       '**Deliver the tested models** (Step 16) with their test accuracy and the repeated-split range.')
    rows = [['Setting', 'Value used', 'Where to change it'],
            ['Test share; seed; candidates', '0.30; 2026; 5000', 'split_cfg.py; split_lib.best_split'],
            ['Split rules', 'whole plots; healthy and unsprayed separately; different treatments; even over replications, varieties, timings', 'split_lib.candidates'],
            ['Smoothing; range; grid', 'Savitzky–Golay 11/2; 400–2400 nm (water bands kept); 5 nm', 'a1_prep.py, wr_features.py'],
            ['Effective ranges', 'R² ≥ 0.5, else top 5% of band pairs; FD 680–760 nm always candidates', 'alib.effective_ranges; a3_select.py'],
            ['SHAP pre-screen', 'XGBoost 300 trees, depth 4, rate 0.05; top 40%', 'alib.shap_prescreen'],
            ['PLS / CARS', 'MCCV 50 splits, ≤ 15 components; CARS 50 iterations × 20 runs; kept if chosen in ≥ 50% of runs; ≤ 15 bands', 'alib.mccv_ncomp, cars, shap_cars'],
            ['Best pair; WRI', 'pair ≥ 10 nm apart; WRI from 200 best NDSI pairs ≥ 50 nm apart, λ3 every 10 nm, w ∈ {−1, −0.5, 0, 0.5, 1}', 'alib.best_pair, wri_search'],
            ['Index filter; ReliefF; VIF', '|r| ≥ 0.95; k = 10, same-plot neighbours excluded, top 5; VIF < 10', 'alib.corr_filter, relieff, vif_filter'],
            ['Inner folds; SFFS', 'GroupKFold(3) by plot; ≤ 15 features; smallest subset within 1% of the best', 'a3_ml.py'],
            ['ML grids; class weights', 'report Table 18; balanced', 'a3_ml_models.py'],
            ['Networks', 'validation = 1/3 of training plots (seed 42); AdamW 6 × 10^{−4}, weight decay 10^{−5}, cosine to 10^{−6}; batch 32; ≤ 100 epochs; patience 20; dropout 0.03; clipping 1.2; label smoothing 0.01; pseudo-image k = max(3, ⌈√p⌉)', 'a4_dl.py'],
            ['Bootstrap', '1000 resamples (Step 11); 2000 (Steps 14–15); whole plots, healthy and unsprayed separately', 'a5_metrics.py; a11_covariate.py; c2_compare.py'],
            ['Weather', '7-day windows ending the day before sampling; favourable-day criteria of Chattopadhyay et al. (2011)', 'a5_extra.py; a11_covariate.py'],
            ['Repeated splits', '20 rule-conforming grouped splits (seed 7, score ≤ median); 5 random leaf-level splits', 'c1_repeat.py']]
    tab('settings', rows=rows, caption='Every setting of the analysis in one table, with the place where it is set.', widths=[2200, 4900, 2500], size=15)
    read(shows='All the numbers that define the analysis.',
         how='To repeat the analysis exactly, keep every value; to adapt it, change only the value and the file named in the last column, and record the change.',
         means='With these settings and the seeds, a re-run on the same data reproduces the same split, the same features and the same models (the split search itself was re-run while writing this document and reproduced split.json exactly).',
         say='"Every setting is fixed and written down, so the analysis can be repeated exactly."')
    h3('Commands in order')
    code('cd thesis_build/asd7030',
         'bash run_all.sh                              # Steps 2-14 and 16 (resumable; markers in data/steps/)',
         'for i in 0 1 2 3; do python3 c1_repeat.py worker $i 4 & done; wait',
         'python3 c1_repeat.py merge                   # Step 15 (3)-(4): 20 grouped + 5 leaf-level splits',
         'python3 ../splitcmp/c2_compare.py            # Step 15 (1)-(2): side by side and paired comparison',
         'python3 a7_excel.py; python3 a10_word.py; node a8_ppt.js    # workbook, report, slides',
         '',
         '# external validation of the delivered models on new spectra (no retraining)',
         'cd ../outputs/ASD_2025-26_70-30_models',
         'python predict_white_rust.py new_spectra.xlsx               # column 1 = wavelength, one column per leaf')
    h3('The core of the protocol in a few lines of Python')
    p('The listing shows the order of the essential operations of Steps 5, 8, 9 and 11 for one task and one model. It is a summary of the scripts, not a replacement for them.')
    code('import numpy as np, pandas as pd, split_lib as SL',
         'from alib import r2_maps, effective_ranges, shap_cars, corr_filter, relieff, vif_filter',
         'from sklearn.model_selection import GroupKFold, GridSearchCV',
         'from mlxtend.feature_selection import SequentialFeatureSelector as SFS',
         '',
         'M = pd.read_csv("meta.csv")                                  # one row per leaf (Steps 2-4)',
         'test_plots, info = SL.best_split(M, 0.30, seed=2026, n_cand=5000)   # Step 5',
         'te = M["plot"].isin(test_plots).values; tr = ~te           # TEST is locked from here on',
         '',
         '# Step 8 - selection on TRAIN only',
         'Nm, Sm = r2_maps(R5[tr], y[tr]); used, thr = effective_ranges(Nm, Sm, w5)',
         'ow = shap_cars(cand_bands[tr], y[tr], names, runs=20, n_iter=50, seed=42)["names"]',
         'kept = corr_filter(IDX[tr], y[tr], 0.95)',
         'w = relieff(IDX[kept].values[tr], y[tr], M["plot"].values[tr]); vi = top5(kept, w)',
         'dsf = vif_filter(pd.concat([BANDS[ow], IDX[vi]], axis=1)[tr], 10.0)[0]',
         '',
         '# Step 9 - inner folds, SFFS, grid search, refit (TRAIN only)',
         'X = ALL[dsf].values; mu, sd = X[tr].mean(0), X[tr].std(0); Xs = (X - mu) / sd',
         'inner = list(GroupKFold(3).split(Xs[tr], groups=M["plot"].values[tr]))',
         'sfs = SFS(est, k_features=(1, 15), forward=True, floating=True, scoring="f1_macro", cv=inner).fit(Xs[tr], y[tr])',
         'idx = smallest_subset_within_1pct(sfs.subsets_)',
         'gs = GridSearchCV(est, grid, scoring="f1_macro", cv=inner).fit(Xs[tr][:, idx], y[tr])',
         'model = gs.best_estimator_.fit(Xs[tr][:, idx], y[tr])',
         '',
         '# Step 11 - the only use of TEST',
         'pred = model.predict(Xs[te][:, idx])')
    box('Five rules that keep the analysis honest.', [
        '1. Split by the unit whose samples are related (the plot), never by leaf.',
        '2. Fix the split before any model is built, and never re-draw it after seeing results.',
        '3. Everything that is chosen – features, subsets, settings, epochs, scaling – is chosen on the training plots.',
        '4. Open the test plots once and report all models.',
        '5. Report the uncertainty of the single split (plot bootstrap) and its luck (repeated splits), and test on an independent season or site.'], kind='key')

    # ---------------------------------------------------------------- discussion, Q&A, references
    h1('11. What the 70:30 analysis shows')
    nl('**The disease signal is physical.** White rust lowers NIR reflectance, raises red and SWIR reflectance and moves the red-edge position 7.7 nm to shorter wavelengths (709.0 → 701.3 nm). '
       'The selected features sit on the green peak, the red edge, the NIR shoulder and the water-band edges.',
       '**Detection is reliable on new plots** (SVM macro-F1 0.826, AUC 0.930); **six grades are limited** by the overlap of neighbouring grades (macro-F1 0.374, but 77% within one grade); '
       '**the score** explains half of the variation (R² 0.517, RMSE 1.92).',
       '**Machine learning and deep learning perform alike** at leaf level; DT-EDNet and its attention modules have no spatial structure to use in a 4 × 4 pseudo-image.',
       '**The spectra add severity information beyond the calendar** (+0.072 macro-F1, +0.102 R², real gains), while detection inside unsprayed plots is largely a matter of date.',
       '**The design matters.** Grouped splitting is necessary (a leaf-level split would inflate six-grade macro-F1 by 0.055). The 70:30 models beat LORO on the same test leaves, '
       'partly because they saw plots of the same replication and partly because the main split was a favourable draw; over 20 splits the two designs are equal on average.')
    p('Limitations: one season and one site; subjective leaf grades; grade 9 small (132 leaves); growth stage confounded with date; networks trained with paper settings on CPU; '
      'no pre-symptomatic dates (Objective 3 not addressed). For the UAV phase the results support sensors covering the red edge (690–760 nm), the NIR shoulder (780–870 nm) and the SWIR '
      'water-band edges, keeping derivative features, and reporting detection plus a severity score or a few classes.')

    h1('12. Questions the chairman may ask')
    qa('Which leaves were used to choose the features of the models?', 'Only the 1631 leaves of the 33 training plots (Step 8). The feature lists of Objective 1 (Step 7) were computed on all leaves to describe the disease; the models never received them.')
    qa('Is this a plot hold-out or a replication hold-out?', 'A plot hold-out: 15 whole plots (4 healthy, 11 unsprayed spread over R1–R3) are test plots. LORO, the earlier design, held out whole replications. Both keep the leaves of one plot together.')
    qa('Why 70:30 and not 80:20?', '70:30 gives 15 test plots and 699 test leaves, enough for a plot bootstrap. 80:20 would leave only 9 test plots (2 healthy), so the estimate would be much less stable. A 20–30% test share is the usual rule (Gholamy et al., 2018).')
    qa('How were the 15 test plots chosen? Could you have picked easy plots?', 'By fixed rules and a score based only on leaf counts, grades and dates – never on spectra or model results. Among 5000 rule-conforming candidates the most balanced one was taken (seed 2026). The repeated-split analysis shows that the chosen split happened to be a favourable one, and this is reported.')
    qa('Where was the validation set for tuning?', 'Inside the training plots: inner GroupKFold(3) by plot for the machine-learning models (11 plots scored each time) and 11 validation plots for the early stopping of the networks. Effectively 47 : 23 : 30% for the networks.')
    qa('Were the final models refitted on all data?', 'No. The delivered models are exactly the tested ones, trained on the training plots only, so their reported test accuracy applies to the files. (Some captions of the report said "all leaves"; this is corrected.)')
    qa('Why is the uncertainty given as a bootstrap and not as a fold SD?', 'With one test set there are no folds. Whole test plots were resampled 1000 times (healthy and unsprayed separately), which keeps the leaves of a plot together (Field and Welsh, 2007).')
    qa('Is 70:30 better than LORO?', 'On the same 699 leaves yes (17 of 30 comparisons really higher, none lower), but over 20 other 70:30 splits the two designs are equal on average. The 70:30 test plots have training plots of their own replication, which LORO does not allow.')
    qa('What would you change if you repeated the analysis?', 'Use a pipeline object so that scaling is fitted inside each inner fold, a stratified grouped inner split, grouped splits also inside CARS, and report the repeated-split range together with the main split from the start.')
    qa('How will you validate the models?', 'By applying the saved files, without retraining, to the 2026-27 leaf and UAV data and to the Bharatpur site, and comparing with the visual grades.')

    h1('Glossary')
    for term, d in [('Hold-out', 'one division of the data into a training set and a test set.'), ('Grouped split', 'a split in which all samples of a group (here a plot) go to the same side.'),
                    ('Stratified split', 'a split that keeps the proportions of important classes (block types, grades, dates) in both sets.'),
                    ('LORO', 'leave-one-replication-out: train on two replications, test on the third, three times.'), ('Inner folds', 'divisions of the training plots used to choose settings without touching the test plots.'),
                    ('SFFS', 'sequential floating forward selection: adds features one at a time and may drop one after each addition.'), ('Early stopping', 'ending network training when the validation score stops improving.'),
                    ('Plot bootstrap', 'resampling whole test plots with replacement to estimate the uncertainty of a metric.'), ('Macro-F1', 'mean F1 of all classes; every class counts equally.'),
                    ('QWK', 'quadratic weighted kappa; agreement that gives partial credit to near misses.'), ('RPD', 'SD of the observed values divided by RMSE.'),
                    ('Leakage', 'information from the test data reaching the model, making accuracy look better than it is.'), ('DSF', 'disease-specific feature set: optimal wavelengths + selected indices after VIF < 10.')]:
        p('**%s** – %s' % (term, d))


def references():
    refs = [l.strip() for l in open(S).read().splitlines() if l.strip()] + EXTRA_REFS
    clean = sorted(set(r.replace("\\'", "'").replace('--', '–').replace('\\', '') for r in refs), key=lambda s: s.lower())
    return clean


def add_refs(text):
    """only the references cited in the document: first author's surname and year must both appear in the text"""
    h1('References')
    n = 0
    for r in references():
        m = re.match(r"\s*([^,(]+?),.*?\((\d{4})[a-z]?\)", r)
        if not m: continue
        sur, yr = m.group(1).strip(), m.group(2)
        if re.search(r'\b' + re.escape(sur) + r'(?: et al\.| and [^\s,();]+(?: [^\s,();]+)?)?,? \(?(?:\d{4}[a-z]?, )*' + yr, text):
            B.append(dict(t='p', text=r)); n += 1
    return n
