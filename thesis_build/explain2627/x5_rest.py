from dsl import *
from x1_intro import stage_head


def add():
    # ---------------------------------------------------------------- chapter 13
    h1('13. Stage 13 – Objective 3: predicting white rust before symptoms')
    stage_head('Stages 1–5 and the rules of Stage 7 (same split, folds and validation plots).', 'the answers of Objective 3.', 'the 576 pre-symptomatic subplot-dates per camera (1, 4 and 7 January; 2, 5 and 8 DAI): at most 396 training and 180 test samples.')
    box('In short', 'The pre-symptomatic dates get a binary label from the later status of each subplot. The spectra are aligned to a healthy baseline, the groups are described, features are selected for each camera with the binary label on the training plots, the models are trained and tested once, and the earliest day of detection is found.', kind='key')
    p('The steps run in this order:')
    h3('Step 13.1 – Labels (3.1)')
    p('Healthy = subplots of the healthy plots; later-infected = inoculated subplots whose DI becomes > 0 on a later date; inoculated subplots that never show pustules are left out. The label therefore uses the later survey, as Zhu et al. (2017) and Tian et al. (2021) labelled leaves that later showed lesions as infected. The numbers of healthy and later-infected samples are counted in the training and test plots.')
    h3('Step 13.2 – Healthy-baseline normalisation (3.2)')
    p('Before symptoms the disease signal is small, and differences between dates (sun, crop growth) can be larger. For each variety, the baseline is the mean reflectance of the healthy training plots on 1 January 2027. For each later pre-symptomatic date and variety:')
    eq('ratio(λ) = baseline(λ) / mean healthy reflectance of the date(λ)     normalised R(λ) = R(λ) × ratio(λ)')
    p('Every subplot spectrum of that date and variety (healthy and inoculated, training and test) is multiplied by ratio(λ), and indices and derivatives are computed from the normalised spectra; thermal features are used in their normalised forms (Chapter 6). This is the healthy-baseline normalisation of Lv et al. (2023); healthy references were also used by Oerke et al. (2006), Calderón et al. (2013) and Zarco-Tejada et al. (2018). The constants come only from healthy training plots. Because the same ratio is applied to all subplots of a date and variety, comparisons within a date are not changed.')
    box('Worked example', 'Variety PM 26, 7 January, 800 nm: baseline (1 January) = 0.420; healthy mean of 7 January = 0.400 → ratio = 1.05. A later-infected subplot with R_{800} = 0.380 becomes 0.399, a healthy one with 0.402 becomes 0.422; their difference is kept, but the date effect is removed.', kind='note')
    h3('Step 13.3 – Description (1.8.1)')
    p('On each of the three dates the mean spectra and features of later-infected and healthy subplots are compared, and a t-test of plot means (the plot is the unit) is done for every feature (all 48 plots; description only). Zhu et al. (2017), Terentev et al. (2023), Gold et al. (2020) and Zhang et al. (2024) found such differences before visible symptoms; Gold et al. (2020) and Zhang et al. (2024) found water-related and shortwave-infrared bands important at this stage.')
    h3('Step 13.4 – Selection for each camera (1.8.2)')
    p('The chain of Stage 7 is run again with the binary label on the training samples: NDSI/RSI maps with R² of the binary label and SHAP-CARS with a classification model for the HS bands; filter + ReliefF for indices and for the MS, RGB and thermal groups; mRMR + TTFI for texture; VIF < 10 within each camera → the pre-symptomatic DSF of each camera (Tian et al., 2021, selected features separately for the asymptomatic stage).')
    h3('Step 13.5 – Fusion and models (3.3–3.4)')
    p('The pre-symptomatic DSFs are joined for the 15 sensor sets (VIF < 10); SVM, random forest, k-NN and PLS-DA, each with SFFS (at most 10 features, because there are fewer samples) and grid search by GroupKFold(3), DNN-F1 for all sets and DNN-F2 for the 11 fused sets are trained exactly as in Stages 9–10. The pseudo-image networks are not used here because the data set is small.')
    h3('Step 13.6 – Test, earliest day and maps (3.5, 1.8.3, 3.6)')
    nl('The 180 test samples are predicted once; sensitivity, specificity, OA, kappa, macro-F1 and AUC are computed for each date and pooled.',
       'The earliest detection day of a sensor set is the first DAI on which the predicted scores of later-infected and healthy test subplots differ significantly (t-test, p < 0.05). Mahlein et al. (2019) compared the day on which each sensor first detected Fusarium head blight; Gold et al. (2020) reported accuracy for each day.',
       'For every DSF feature, the first date with a significant difference (Step 13.3) is recorded – which camera and feature responds first (1.8.3).',
       'The covariate-only model is the reference, and the probability of later infection is mapped per subplot for each date (risk maps; Zarco-Tejada et al., 2018).')
    myfig('presym', 'g15_presym_demo.png', 'Demo of the pre-symptomatic output: (a) difference of one feature between later-infected and healthy subplots; (b) AUC by date.')

    # ---------------------------------------------------------------- chapter 14
    h1('14. Stage 14 – The ASD leaf analysis, step by step')
    stage_head('Stage 4 (the same plot split); runs in parallel with the UAV analysis.', 'the leaf results and the leaf–canopy link.', '7488 leaves (centre plant, L3, L5, LL, 13 dates): 5148 training leaves (network fitting 3432, validation 1716) and 2340 test leaves, divided by plot.')
    box('In short', 'The leaf analysis is the same chain as the UAV analysis, with one "camera" (the ASD spectrum at 1 nm) and one sample per leaf: build a clean leaf table, use the same plot split, smooth and reduce the spectra, compute indices, describe on all leaves, select on training leaves, model, test once, compare with covariates and link to the canopy.', kind='key')
    myfig('leafchain', 'g14_leaf_chain.png', 'Order of the leaf analysis (Steps L1–L10).')
    rows = [['Order', 'Step', 'What is done', 'Leaves used', 'References'],
            ['1', 'L1 Leaf table and checks', 'read files; join to plot, subplot, leaf, date, grade; average the 2 readings (flag if they differ by > 0.02 reflectance); keep L3, L5, LL; remove exact duplicates; Isolation Forest outlier screening within date × grade, remove only faulty spectra', 'all', 'Chen et al. (2023); Selvaprakash et al. (2026)'],
            ['2', 'L2 Same split', 'copy the plot split of D1 to every leaf; same folds and validation plots', 'defines sets', 'Ma et al. (2026)'],
            ['3', 'L3 Pre-processing', 'Savitzky–Golay (window 11, order 2) on 350–2500 nm; trim to 400–2400 nm, water bands kept; first derivative; 5-nm band means for the searches', 'all (no labels)', 'Selvaprakash et al. (2026); Chen et al. (2023)'],
            ['4', 'L4 Indices', '48 published indices and REP, D_{r}, SD_{r} at 1 nm', 'all (no labels)', 'Zhang et al. (2012); Mandal et al. (2023)'],
            ['5', 'L5.1 Description', 'mean ± SD spectra by grade, % difference from grade 0, r curves; by leaf position, stage, variety, date', 'all 7488', 'Mandal et al. (2023); Cross et al. (2024)'],
            ['6', 'L5.7 PCA', 'PCA of standardised 5-nm reflectance; score plots with grade ellipses', 'all 7488', 'Selvaprakash et al. (2026)'],
            ['7', 'L5.2 Bands', 'NDSI/RSI maps of about 80 000 pairs; effective ranges; SHAP-CARS → leaf OW', '5148 training', 'Ma et al. (2026)'],
            ['8', 'L5.3 Leaf indices', 'best NDSI, RSI; leaf WRI', '5148 training', 'Mahlein et al. (2013)'],
            ['9', 'L5.4 Index ranking', '|r| ≥ 0.95 filter; ReliefF / RReliefF top five', '5148 training', 'Lv et al. (2023)'],
            ['10', 'L5.5 Leaf DSF', 'OW + VI → VIF < 10', '5148 training', 'Lv et al. (2023); Tian et al. (2021)'],
            ['11', 'L5.6 Separability', 'Jeffries–Matusita distance between all grade pairs on the leaf DSF', '5148 training', 'Mandal et al. (2023)'],
            ['12', 'L6 Leaf models', 'SVM/SVR, random forest, k-NN, PLS-DA/PLSR (SFFS + grid, GroupKFold(3)); DNN-F1; four pseudo-image networks (A, B)', 'fit / validation within training', 'Tian et al. (2021); Martínez-Martínez et al. (2018)'],
            ['13', 'L7 Test', 'all metrics of Step 12.1 on the test leaves; by leaf position and stage', '2340 test', 'Ma et al. (2026); Cross et al. (2024)'],
            ['14', 'L8 Covariate baseline', 'M0, M1, M2 with leaf data; ΔS, ΔC', 'training / test', 'Zhang et al. (2014a)'],
            ['15', 'L9 Leaf–canopy link', 'leaf vs canopy OW and VI; mean leaf spectrum of the centre plant resampled to the Headwall bands vs the UAV spectrum; leaf WRI on UAV spectra vs subplot DI', 'test plots for the WRI check', 'Liu et al. (2026); Bohnenkamp et al. (2019)'],
            ['16', 'L10 Pre-symptomatic leaves', 'leaves of 1, 4, 7 January labelled by the later status of the tagged plant; healthy-baseline normalisation; selection, models, test by date', 'same split', 'Lv et al. (2023); Gold et al. (2020)']]
    tab('leaf', rows=rows, caption='The leaf analysis in the order in which it is run.', widths=[650, 1700, 3900, 1400, 1950], size=14, nokeep=True)
    p('Three differences from the UAV analysis need attention:')
    nl('**Resolution.** Leaf spectra are at 1 nm; the band searches use 5-nm means to reduce the number of pairs, but the chosen indices are computed at 1 nm.',
       '**Water bands are kept**, because the leaf clip has its own lamp and no atmosphere is involved (Chen et al., 2023, used the full 350–2500 nm range).',
       '**One "camera".** There is no fusion step; the leaf DSF goes directly to the models. A leaf data set of this size per date is enough for leaf models (Selvaprakash et al., 2026, used 800 leaves).')
    box('Worked example', 'The JM distance on the leaf DSF of Task B: JM = 2(1 − e^{−B}), with B the Bhattacharyya distance between two grades. JM near 2 means the grades are separable; Mandal et al. (2023) found almost all rice blast levels separable except two neighbouring levels.', kind='note')

    # ---------------------------------------------------------------- chapter 15
    h1('15. Repeating the analysis on a new data set')
    h2('15.1 Two different situations')
    rows = [['Situation', 'What it means', 'What is repeated', 'What is reused'],
            ['A – a new data set analysed on its own (for example season 2027-28)', 'the new data must answer the same objectives by themselves', 'everything: Stages 1–14, with a new plot split, new selection, new models', 'only the procedure and settings of this document'],
            ['B – testing the frozen 2026-27 models on new data (for example Bharatpur or another field)', 'the new data check whether the 2026-27 models work elsewhere', 'Stages 1–3 (processing, features, labels) and Stage 11 (prediction and metrics)', 'the 2026-27 DSF wavelengths and formulas, scaling constants, healthy references (where needed) and frozen models; no selection, tuning or refitting']]
    tab('situations', rows=rows, caption='Two ways of using a new data set.', widths=[2400, 2400, 2500, 2300], size=15)
    h2('15.2 Checklist for situation A, in order')
    nl('Collect the data of Chapter 2 with the same protocols (plot, subplot and date codes on every record).',
       'Process the images (Stage 1): calibration, mosaics, HS cleaning and smoothing, co-registration, one grid, ROI means.',
       'Compute the features of each camera (Stage 2) and build the four camera tables.',
       'Compute the DI, DI classes, labels and covariates (Stage 3); merge rare classes.',
       'Make the plot-wise split before looking at the data: 30% of the plots of each block type as test plots, covering all treatments; fix GroupKFold(3) and the network validation plots (one third of the training plots) (Stage 4).',
       'Normalise thermal data and fix all scaling rules with training-plot constants (Stage 5).',
       'Describe the response on all plots (Stage 6).',
       'Select features for each camera on the training plots and get the DSFs (Stage 7).',
       'Build the 15 sensor sets with VIF (Stage 8).',
       'Train the ML models with SFFS, grid search and refit (Stage 9) and the networks with the validation plots (Stage 10); freeze everything.',
       'Predict the test plots once and compute the metrics (Stage 11).',
       'Compare, ablate, explain, run the covariate baseline, report by stratum and draw maps (Stage 12).',
       'Run the pre-symptomatic chain (Stage 13) and the leaf chain (Stage 14).')
    h2('15.3 Checklist for situation B')
    nl('Process the new images and compute features exactly as in Stages 1–2 (same bands, formulas, GLCM settings).',
       'Compute only the features of the frozen DSFs, with the 2026-27 wavelengths, triplets and formulas.',
       'Apply the frozen pipelines (they contain the 2026-27 scaling constants); thermal ΔT uses the healthy plots of the new site if present, otherwise CTD, CTR and NRCT only.',
       'Compute the metrics of Step 12.1 with the new survey; report by site type and variety; draw maps. Do not refit, re-tune or re-select (Ma et al., 2026).')
    h2('15.4 Files to keep')
    rows = [['File', 'Content', 'Made in'],
            ['plot_table.xlsx', 'plot, block, replication, variety, sowing date, split (TRAIN/TEST), validation plot flag', 'Stage 4'],
            ['roi_means_<camera>.csv', 'one row per subplot-date: identifiers and the ROI mean of every band', 'Stage 1'],
            ['features_<camera>.csv', 'identifiers, labels, covariates and all features of the camera', 'Stages 2–3'],
            ['folds.csv', 'plot → GroupKFold round; network validation plots', 'Stage 4'],
            ['dsf_<camera>_<task>.json', 'selected features with their wavelengths, formulas and triplets', 'Stage 7'],
            ['inputs_<set>_<task>.csv', 'input table of each sensor set after VIF', 'Stage 8'],
            ['model_<model>_<set>_<task>.joblib / .pt', 'frozen pipeline (scaler + model) or network weights, with the SFFS subset and settings', 'Stages 9–10'],
            ['predictions_test.csv, metrics_test.csv', 'test predictions and all metrics', 'Stage 11'],
            ['settings_log.txt', 'seeds, software versions, every setting, bands removed', 'all stages']]
    tab('files', rows=rows, caption='Files to keep so that the analysis can be repeated or audited.', widths=[3000, 4900, 1700], size=15)
    h2('15.5 Software for each stage')
    rows = [['Stage', 'Software and functions'],
            ['1 Image processing', 'Agisoft Metashape (mosaics); ENVI or Python (GDAL, rasterio) for calibration, registration, resampling and ROI statistics'],
            ['2 Features', 'numpy, scipy.signal.savgol_filter (smoothing, derivatives), scikit-image graycomatrix / graycoprops (GLCM), scikit-learn PCA'],
            ['4 Split', 'pandas (split column), scikit-learn GroupKFold'],
            ['7 Selection', 'scikit-learn RandomForestRegressor, shap TreeExplainer, PLSRegression (CARS loop), ReliefF (skrebate), mrmr-selection, statsmodels variance_inflation_factor'],
            ['9 Machine learning', 'scikit-learn Pipeline, StandardScaler, SVC/SVR, RandomForest, KNeighbors, PLSRegression, GridSearchCV; mlxtend SequentialFeatureSelector (floating = True)'],
            ['10 Networks', 'PyTorch (AdamW, CosineAnnealingLR, early stopping)'],
            ['11–12 Metrics', 'scikit-learn metrics (accuracy, cohen_kappa_score, f1_score, roc_auc_score, r2_score, mean_squared_error)']]
    tab('software', rows=rows, caption='Software for each stage (Python packages: Pedregosa et al., 2011; Raschka, 2018).', widths=[2200, 7400], size=15)
    p('Fix the random seed (42) everywhere, and store the split, folds and validation plots as files that every script reads, so that each camera, sensor set and model uses exactly the same division.')

    # ---------------------------------------------------------------- chapter 16
    h1('16. Questions you may be asked about the order and the data')
    qa('Why is the split made before feature selection?', 'Feature selection learns from the labels. If it saw the test plots, the selected features would already fit them and the test accuracy would be too high (Ambroise and McLachlan, 2002). So the split comes first (Stage 4) and selection uses only the training plots (Stage 7).')
    qa('Why are descriptive analyses done on all plots?', 'Curves, correlations, physiology and stability only describe the data; nothing from them decides a model input or a setting. Using all plots gives the most complete description without making the test optimistic.')
    qa('Why GroupKFold for machine learning but fixed validation plots for networks?', 'Machine-learning models are fast, so each choice can be scored in three rounds and averaged. Networks need one validation set during training to decide when to stop; repeating training three times for every network would add little. Both use only training plots, divided by whole plots.')
    qa('Why is SFFS done after Objective 1 selection, and is that not selecting twice?', 'Objective 1 gives each camera a compact, non-redundant feature set that is the same for every model. SFFS then lets each model pick the subset that suits it best from that set (Tian et al., 2021; Lv et al., 2023; Mustafa et al., 2023). Both use only the training plots.')
    qa('Why is VIF applied again after the cameras are joined?', 'Features of different cameras can repeat each other (for example a multispectral red-edge index and a hyperspectral red-edge band). VIF inside each camera cannot see this; it appears only when the cameras are joined (Step 2.2).')
    qa('What is frozen before the test, and what is computed on the test plots?', 'Frozen: the split, the DSF wavelengths and formulas, the VIF-kept features, the SFFS subsets, the settings, the scaling constants, the healthy references and the model weights. Computed on the test plots: only the features (with the frozen formulas), the predictions and the metrics.')
    qa('How many models are trained?', '4 machine-learning models × 15 sensor sets × 3 tasks = 180; DNN-F1 for 15 sets × 3 tasks = 45; DNN-F2 for 11 sets × 3 tasks = 33; four pseudo-image networks for Tasks A and B on the HS configurations and the 15 sets; plus the pre-symptomatic and leaf models.')
    qa('What changes if a DI class is too rare?', 'A class with fewer than 5% of the samples is merged with its neighbour before modelling (Step A5), and the merge is reported; the task then has fewer classes.')
    qa('How would you analyse a new season?', 'Repeat Stages 1–14 with a new plot-wise split made before any analysis (Chapter 15, situation A). To test the 2026-27 models elsewhere, compute only the frozen features and apply the frozen models (situation B).')

    h1('Glossary')
    rows = [['Term', 'Meaning'],
            ['Subplot-date', 'one subplot on one flight date – the sample of the UAV analysis'],
            ['Training plots / test plots', '33 plots used to learn everything / 15 plots used once to measure accuracy'],
            ['Inner fold, fitting part, scoring part', 'a GroupKFold round inside the training plots: 22 plots fit, 11 plots score'],
            ['Validation plots', 'the 11 fixed training plots on which networks are stopped early'],
            ['Effective ranges', 'wavelength regions whose band pairs reach R² > 0.5 with the DI'],
            ['OW', 'optimal wavelengths chosen by SHAP-CARS'],
            ['VI', 'the five indices kept by ReliefF'],
            ['TF, TTFI', 'the six texture features kept by mRMR; the Tri-band Texture Fusion Index made from three of them'],
            ['DSF', 'disease-specific feature set: the features of one camera and task left after VIF'],
            ['Sensor set', 'one camera or a combination of cameras whose DSFs are joined'],
            ['Feature-level fusion', 'joining the features of several cameras into one input vector'],
            ['SFFS', 'sequential floating forward selection of a feature subset for one model'],
            ['Freezing', 'saving a model with everything it needs, after which nothing is changed']]
    tab('gloss', rows=rows, caption='Glossary of the terms used in this document.', widths=[2800, 6800], size=15)
