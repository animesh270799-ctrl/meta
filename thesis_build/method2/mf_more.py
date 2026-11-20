# Additional sections inserted into mf_body.py (kept separate for readability).
ABBR = r"""
H1('Abbreviations')
TAB('abbr', [['Abbreviation', 'Meaning', 'Abbreviation', 'Meaning'],
 ['AUC', 'area under the ROC curve', 'MNF', 'minimum noise fraction'], ['CT, CTD', 'canopy temperature; CT minus air temperature', 'mRMR', 'minimum redundancy maximum relevance'], ['CWSI', 'crop water stress index', 'MS', 'multispectral'],
 ['DAI', 'days after inoculation', 'NDSI', 'normalised difference spectral index'], ['DL, ML', 'deep learning; machine learning', 'NRCT', 'normalised relative canopy temperature'], ['DNN-F1, DNN-F2', 'deep neural network with input- and intermediate-level feature fusion', 'OFC', 'optimum feature combination'],
 ['DSF', 'disease-specific feature', 'PLS-DA, PLSR', 'partial least squares discriminant analysis; regression'], ['FD, SD', 'first and second derivative of reflectance', 'PPI', 'pixel purity index'], ['GLCM', 'grey-level co-occurrence matrix (texture)', 'R', 'reflectance'],
 ['HS', 'hyperspectral', 'REP', 'red-edge position'], ['k-NN', 'k-nearest neighbours', 'RF, RFR', 'random forest classification; regression'], ['LORO', 'leave-one-replication-out', 'RGB', 'red–green–blue camera'],
 ['RMSE', 'root-mean-square error', 'RPD', 'ratio of performance to deviation'], ['SAM', 'spectral angle mapper', 'SE', 'squeeze-and-excitation attention'], ['SFFS', 'sequential floating forward selection', 'SHAP', 'Shapley additive explanations'],
 ['SVM, SVR', 'support vector machine; regression', 'TIR', 'thermal infrared'], ['VI', 'vegetation index', 'VIF', 'variance inflation factor'], ['WRI', 'White Rust Index', 'XGBoost', 'extreme gradient boosting']],
 'Abbreviations used in this document.', [1500, 3150, 1500, 3156], 16)
"""
LIT = r"""
H2('1.1 Published studies on which the methodology is built')
P('Every step of this methodology was chosen because it has been used and tested for crop-disease sensing or for the specific data problem it solves. Table [[T:literature]] lists the main disease studies and the steps they support; the methodological references (validation, selection, models) are given in each step.')
TAB('literature', [['Study', 'Crop and disease', 'Sensors and data', 'What it showed', 'Steps supported'],
 ['Mahlein et al. (2013)', 'sugar beet; Cercospora, rust, powdery mildew', 'leaf hyperspectral', 'ReliefF bands combined into disease-specific indices', 'O1-3, O1-4'],
 ['Huang et al. (2014)', 'wheat; powdery mildew, yellow rust', 'leaf and canopy hyperspectral', 'ReliefF bands; new optimised indices transferred to canopy', 'O1-3, O1-4'],
 ['Shukla et al. (2024)', 'mustard; aphid stress', 'ground hyperspectral', 'correlation scalogram to find sensitive regions', 'O1-3, Stage 2'],
 ['Tian et al. (2021)', 'rice; leaf blast', 'spectra 350–2500 nm', 'disease-specific features, VIF → SFFS, asymptomatic stage', 'Stage 1, 3, 4; O3-1'],
 ['Mustafa et al. (2023)', 'wheat; Fusarium head blight', 'fluorescence + hyperspectral', 'Boruta and ML-SFFS; k-NN and SVM', 'O1-6, Stage 4'],
 ['Feng et al. (2022)', 'wheat; powdery mildew', 'hyperspectral + thermal + RGB', 'feature-level fusion of indices, thermal and texture; PLSR, SVR, RFR', 'F3, F4, fusion, O2-3'],
 ['Liu et al. (2024)', 'wheat; powdery mildew', 'UAV multispectral + thermal', 'red-edge indices and thermal features; RF; maps', 'F2, F4, O2-7'],
 ['Guo et al. (2021)', 'wheat; yellow rust', 'UAV hyperspectral', 'vegetation indices + texture; common resolution; masks', 'P5, P6, F3'],
 ['Maimaitijiang et al. (2020)', 'soybean yield', 'UAV RGB + multispectral + thermal', 'DNN with input- and intermediate-level fusion', 'O2-4'],
 ['Ma et al. (2026)', 'rice; blast', 'UAV hyperspectral', 'group-wise selection, texture index, SE attention, ablation', 'Stage 2, O2-4, O2-6'],
 ['Abdulridha et al. (2023)', 'wheat; stem rust', 'UAV hyperspectral, 960 plots', 'RF for severity classes and binary detection', 'O2-1, O2-3'],
 ['Mahlein et al. (2019)', 'wheat; Fusarium head blight', 'hyperspectral + thermal + fluorescence', 'sensor comparison and earliest detection day', 'O1-7, O3-5'],
 ['Zhu et al. (2017)', 'tobacco; mosaic virus', 'hyperspectral imaging', 'pre-symptomatic detection with retrospective labels', 'O3-1, O3-4'],
 ['Zarco-Tejada et al. (2018)', 'olive; Xylella fastidiosa', 'airborne hyperspectral + thermal', 'pre-visual detection and maps', 'O3-2, O3-5'],
 ['Yu et al. (2025)', 'rice; sheath blight', 'spectra + physiology', 'dual-branch fusion at the pre-symptomatic stage', 'O3-4'],
 ['Oerke et al. (2006)', 'cucumber; downy mildew', 'thermal imaging', 'temperature changes with disease and with environment', 'F4, O3-2'],
 ['Deng et al. (2024)', 'wheat; stripe rust', 'UAV multimodal', 'deep fusion for disease-index maps', 'O2-7']],
 'Main disease studies and the steps of this methodology they support.', [1750, 1700, 1750, 2500, 1606], 15)
"""
PRE_TAB = r"""
H2('3.9 Pre-processing of each sensor at a glance')
TAB('presensor', [['Step', 'Hyperspectral', 'Multispectral', 'RGB', 'Thermal'],
 ['P1 Calibration', 'panels → reflectance', 'panels + sunlight sensor → reflectance', 'fixed exposure; digital numbers', 'emissivity 0.98, air T, RH → °C'],
 ['P2 Mosaic', 'georectified push-broom cube', 'orthomosaic', 'orthomosaic', 'orthomosaic'],
 ['P3 Quality', '613 → 483 bands; segment-wise smoothing', 'band alignment check', '—', 'warm-up and drift check'],
 ['P4 Registration', 'reference image', 'to HS, RMSE < 1 pixel', 'to HS, RMSE < 1 pixel', 'to HS with markers'],
 ['P5 Resampling', 'reference grid (2.2 cm)', 'bilinear', 'pixel aggregate; texture before resampling', 'nearest neighbour'],
 ['P6 Mask', 'made here (hourglass + SAM)', 'HS mask applied', 'HS mask applied', 'HS mask + extra edge check'],
 ['P7 Polygons', '192 subplots', 'same', 'same', 'same'],
 ['P8 Values', 'mean per band', 'mean per band', 'colour means, texture', 'statistics, normalised temperatures']],
 'Pre-processing applied to each sensor.', [1700, 2000, 1900, 1900, 1806], 15)
"""
SCHEMA = r"""
H2('4.5 The feature table')
P('All later steps read the same table layout, one table per sensor, joined by the identifier columns for fusion. Keeping one row per subplot-date and the same identifiers for all sensors makes the 15 sensor sets simple joins of these tables.')
TAB('schema', [['Column block', 'Columns', 'Used for'], ['Identifiers', 'date, DAI, plot, subplot, replication, treatment, variety, inoculation timing, fold', 'joining sensors; validation folds; treatment-wise results'],
 ['Labels', 'severity score, severity class, healthy/diseased; for Objective 3: infected/healthy and later score', 'model targets'], ['Covariates', 'flower %, canopy cover %, vegetation pixel count', 'checks of confounding; quality flags'],
 ['Features', 'all features of the sensor, grouped (prefix R_, FD_, SD_, VI_, TX_, TH_)', 'selection and models']], 'Layout of the feature table of each sensor.', [1800, 4600, 2906])
"""
LEAK = r"""
H2('5.4 Leakage checklist and fold sizes')
TAB('leak', [['Step', 'Uses labels?', 'Where it is run'], ['Pre-processing, mask, feature extraction', 'no', 'once, on all data'], ['Stage 1 (correlation clusters)', 'no', 'training part of each outer fold'], ['Thermal and control normalisation', 'no (uses healthy plots)', 'training healthy plots for training data; same reference applied to test data'],
 ['Stage 2 (scalogram, ReliefF, Boruta, mRMR), index search', 'yes', 'inner folds only'], ['Stage 3 (VIF) and fusion', 'no', 'training part'], ['Stage 4 (SFFS), hyper-parameter tuning, early stopping', 'yes', 'inner folds only'], ['Final evaluation', 'yes', 'test replication, once']],
 'Where each step is run so that no information from the test replication enters the model.', [3900, 1700, 3706])
TAB('foldsize', [['Dataset', 'Training part per outer fold', 'Test part per outer fold', 'Inner folds'], ['Post-symptomatic (1536 per sensor)', '≈ 1024 samples (two replications + their healthy plots)', '≈ 512 samples', '3, grouped by plot'], ['Pre-symptomatic (576 per sensor)', '≈ 384 samples', '≈ 192 samples', '3, grouped by plot']],
 'Approximate sizes of the training and test parts.', [2600, 2800, 1900, 2006])
P('With about 1024 training samples and at most 15 selected features, every model keeps more than 60 samples per feature, well above the ratio at which the Hughes effect becomes important (Hughes, 1968; Guyon and Elisseeff, 2003). The pre-symptomatic models (≈ 384 training samples) are limited to 10 features.')
"""
SENS_O1 = r"""
H2('6.8 What each sensor is expected to show and what to report')
P('The expected responses below are hypotheses derived from plant physiology and the published studies; Objective 1 tests them with the field data.')
H3('Hyperspectral')
BL(['Expected: higher visible reflectance and lower red-edge slope from chlorophyll loss and chlorosis; a shift of the red-edge position to shorter wavelengths; lower NIR reflectance from mesophyll damage around pustules; higher SWIR reflectance from leaf water loss at higher severity (Horler et al., 1983; Carter and Knapp, 2001; Apan et al., 2004). The leaf-level ASD analysis of this study already pointed to red-edge derivatives and a VNIR index combining the NIR plateau, the 970 nm water shoulder and red-edge reflectance.',
    'Report: mean spectra and first derivatives by class; scalogram and ReliefF curves; robust band list; WRI formula with its balanced accuracy; top indices with ANOVA groups; Boruta pools.'])
H3('Multispectral')
BL(['Expected: the 717 nm red-edge and 840 nm NIR bands and red-edge indices (NDRE, CIrededge, MTCI) respond most; red-edge indices were the most consistent multispectral indicators of powdery mildew (Liu et al., 2024).', 'Report: band means by class; ranking of the 12 indices and 10 NDSI; texture response; Boruta pools; comparison of each MS index with its hyperspectral equivalent.'])
H3('RGB')
BL(['Expected: lower greenness (ExG, NGRDI, GLI) with chlorosis; brighter, whiter patches with pustules; higher texture contrast and entropy and lower homogeneity as the canopy surface becomes heterogeneous (Meyer and Neto, 2008; Ma et al., 2026).', 'Report: colour-index and texture responses by class; whether RGB features follow flower % (they should be checked at flowering).'])
H3('Thermal')
BL(['Expected: changes in canopy temperature relative to healthy plots and higher within-subplot temperature variability as infection disturbs transpiration; the direction must be established from the data because environmental conditions also change canopy temperature (Oerke et al., 2006; Jones et al., 2009).', 'Report: ΔT, CTD, NRCT and temperature SD by class and date; correlation of thermal features with SWIR water indices.'])
"""
SETS = r"""
H2('7.8 Specification of the 15 sensor sets')
P('For every set the input is the union of the fold-wise DSF sets of its sensors (Stage 3), reduced again by VIF < 10; machine-learning models then select their own subset by ML-SFFS, and the deep-learning models use the fused pool. DNN-F2 is used whenever the set contains two or more sensors. The paragraphs below state what each set is expected to contribute and what comparison it answers.')
for s_, t_ in [('S1 – hyperspectral alone', 'Input: robust bands, derivatives, red-edge parameters, indices and the WRI. Expected to be the strongest single sensor because it covers pigment, structure and water features; it sets the reference against which all fusion gains are judged (Feng et al., 2022; Ma et al., 2026). Models: all ML models and DNN-F1.'),
 ('S2 – multispectral alone', 'Input: five bands, red-edge and chlorophyll indices, NDSI and texture. Answers whether a low-cost, satellite-like sensor captures most of the hyperspectral information; compare its best index with the WRI and with S1 (Liu et al., 2024).'),
 ('S3 – RGB alone', 'Input: colour indices and texture. Tests whether a consumer camera is sufficient for visible symptoms; expected to be weaker at low severity, where colour change is small (Guo et al., 2021; Ma et al., 2026).'),
 ('S4 – thermal alone', 'Input: normalised temperature features and thermal texture. Tests the physiological (transpiration) signal on its own; expected to be weaker for severity classes but potentially useful for early change (Mahlein et al., 2019; Liu et al., 2024).'),
 ('S5 – HS + MS', 'Tests whether multispectral texture and bands add anything to the hyperspectral spectrum; a small gain is expected because the spectral information overlaps, which shows whether the cheaper MS sensor can replace HS.'),
 ('S6 – HS + RGB', 'Combines detailed spectra with high-resolution canopy texture; tests the spectral + texture fusion found useful for powdery mildew and rice blast (Feng et al., 2022; Ma et al., 2026).'),
 ('S7 – HS + TIR', 'Combines spectral (pigment, structure, water) and thermal (transpiration) information; tests the hyperspectral + thermal fusion that improved Fusarium head blight detection (Mahlein et al., 2019).'),
 ('S8 – MS + RGB', 'An all-optical low-cost pair: red-edge spectra plus fine texture.'),
 ('S9 – MS + TIR', 'Low-cost spectral + thermal pair, the combination used for powdery mildew severity by Liu et al. (2024); a practical candidate for routine monitoring.'),
 ('S10 – RGB + TIR', 'The cheapest pair; shows how far colour, texture and temperature go without narrow bands.'),
 ('S11 – HS + MS + RGB', 'All optical sensors; tests whether thermal is needed at all.'),
 ('S12 – HS + MS + TIR', 'All spectral sensors with thermal; tests whether RGB texture is needed.'),
 ('S13 – HS + RGB + TIR', 'Hyperspectral, texture and thermal: the three types of information that Feng et al. (2022) fused; tests whether MS is redundant when HS is present.'),
 ('S14 – MS + RGB + TIR', 'All low-cost sensors; the main practical alternative to a hyperspectral system.'),
 ('S15 – all four sensors', 'The full multimodal system; used for the drop-one-sensor ablation that measures the contribution of each sensor.')]:
    P('**' + s_ + '.** ' + t_)
"""
ROBUST = r"""
STEP('O2-8', 'Treatment-wise performance and robustness',
     'A model may work for one variety or crop age and fail for another; treatments must be considered in the evaluation.',
     'Test predictions with variety, inoculation timing and date codes.',
     'Performance by treatment and transfer results → conclusions on robustness.',
     ['Report all metrics separately for each variety (V1–V3), each inoculation timing (D1–D4) and each date.', 'Leave-one-variety-out test: train on two varieties and test on the third (mainly V1 ↔ V2, because the resistant variety has few diseased samples).', 'Leave-one-inoculation-timing-out test: train on three timings and test on the fourth, to check transfer across crop ages.', 'Use these tests for the best ML and best DL model of the best three sensor sets only, to limit computation.'],
     'Blocked tests that leave out a whole group show whether a model extrapolates to new conditions; treatment-wise results show whether the selected features are variety-specific.',
     'Blocked cross-validation for extrapolation: Roberts et al. (2017); performance by variety and growth stage: Liu et al. (2024), Feng et al. (2022); independent-site testing: Ma et al. (2026).')
"""
TEMPL = r"""
H2('7.9 Result tables to be produced')
TAB('templateA', [['Sensor set', 'Best ML model', 'Macro-F1', 'Weighted kappa', 'Best DL model', 'Macro-F1', 'Weighted kappa'], ['S1 HS', '…', '…', '…', '…', '…', '…'], ['S2 MS', '…', '…', '…', '…', '…', '…'], ['…', '…', '…', '…', '…', '…', '…'], ['S15 all', '…', '…', '…', '…', '…', '…']],
 'Template: severity-class results of the 15 sensor sets (one table each for Tasks A, B and C).', [1600, 1500, 1100, 1300, 1500, 1100, 1206])
TAB('templateB', [['Removed sensor (from S15)', 'Macro-F1 without it', 'Change', 'R² without it', 'Change'], ['HS', '…', '…', '…', '…'], ['MS', '…', '…', '…', '…'], ['RGB', '…', '…', '…', '…'], ['TIR', '…', '…', '…', '…']],
 'Template: drop-one-sensor ablation.', [2600, 1800, 1200, 1800, 1906])
"""
PRE3 = r"""
H2('8.6 Sensor-specific expectations at the pre-symptomatic stage')
BL(['Hyperspectral: small red-edge and pigment-index changes may appear before pustules, as reported for wheat leaf rust and tobacco mosaic virus (Terentev et al., 2023; Zhu et al., 2017).', 'Thermal: transpiration changes can precede visible symptoms; thermal imaging detected Fusarium head blight later than hyperspectral imaging in one study but added to fusion (Mahlein et al., 2019), so its value is tested here.', 'Multispectral: the red-edge band may carry part of the hyperspectral early signal.', 'RGB: colour and texture are expected to respond only after visible symptoms; RGB-only sets serve as a negative control for the pre-symptomatic stage.', 'Treatments: inoculation timing changes crop age at infection; earliest detection days are therefore reported separately for each inoculation timing and variety.'])
"""
CHAIN = r"""
H2('9.1 Input–output chain of all steps')
TAB('chain', [['Step', 'Input', 'Output (to next step)'], ['D1–D4', 'field design, scores', 'labelled subplot list; post- and pre-symptomatic datasets'], ['P1–P2', 'raw images, panels, GCPs', 'calibrated, georeferenced mosaics'], ['P3', 'HS cube', 'clean 483-band cube'], ['P4–P5', 'mosaics of all sensors', 'aligned layers on the HS grid'],
 ['P6', 'HS cube, training regions', 'vegetation mask'], ['P7–P8', 'masked layers, polygons', 'subplot tables per date and sensor'], ['F1–F4', 'subplot tables', 'feature groups per sensor'], ['V1–V2', 'labelled feature tables', 'outer and inner folds'],
 ['S1–S3', 'feature groups (training part)', 'sensor DSF sets'], ['S4', 'DSF sets of a combination', 'fused pool'], ['S5', 'fused pool', 'optimum feature combinations'], ['O1-1 to O1-7', 'post-symptomatic feature groups', 'DSF pools, WRI, response figures'],
 ['O2-1 to O2-8', 'fold-wise features, labels', 'models, metrics, best sensor set, contributions, maps'], ['O3-1 to O3-5', 'pre-symptomatic features, later labels', 'pre-symptomatic models, earliest detection day, risk maps']],
 'Input and output of every step.', [1700, 3700, 3906])
"""
