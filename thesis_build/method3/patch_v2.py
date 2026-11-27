"""Revision 2 of the methodology sources: covariates, removal of E1/E4, SHAP-CARS settings, model matrix,
multi-camera pseudo-images, variety names and corrected drawbacks. Each replacement must match exactly once."""
import re
def patch(f, reps):
    s = open(f).read()
    for a, b in reps:
        n = s.count(a)
        assert n == 1, (f, n, a[:90])
        s = s.replace(a, b)
    open(f, 'w').write(s)

# ============================================================== mf3_body.py
B = []
B.append(("BOX('What is new in this revision.', '(1) The methods", "BOX('What is new in this revision.', '(1) The methods"))  # anchor check
B.append(("(6) Each technique has a method card.')",
          "(6) Each technique has a method card. (7) Covariates are days after inoculation, variety, inoculation timing, growth stage and weather; they are used for a covariate-only baseline and for sensor + covariate models, not as disease features. (8) Healthy plots are rotated across the folds so that every fold contains healthy plots of all three varieties. (9) SHAP-CARS standardises the bands and always keeps the red-edge first derivative. (10) All models, including DT-EDNet and the comparison networks, are built for every single camera and every camera combination, for classification and regression.')"))
# abbreviations
B.append((" ['AUC', 'area under the receiver operating characteristic curve', 'mRMR', 'minimum redundancy maximum relevance'],",
          " ['AUC', 'area under the receiver operating characteristic curve', 'mRMR', 'minimum redundancy maximum relevance'],\n ['BBCH', 'decimal scale of plant growth stages (Biologische Bundesanstalt, Bundessortenamt und Chemische Industrie)', 'RH', 'relative humidity'],"))
B.append((" ['XGBoost', 'extreme gradient boosting', '', '']],", " ['XGBoost', 'extreme gradient boosting', 'T_{max}, T_{min}', 'daily maximum and minimum air temperature']],"))
# rules
B.append(("    'All normalisation constants (means, standard deviations, healthy-plot references) are computed on the training part and then applied to the test part.',",
          "    'All normalisation constants (means, standard deviations, healthy-plot references) are computed on the training part and then applied to the test part.',\n    'Severity increases with time, so every sensor model is compared with a covariate-only model (days after inoculation, variety, inoculation timing, growth stage, weather); a sensor model is useful only if it is better than this baseline.',"))
# dataset table: varieties
B.append(("['Label of every sample', 'canopy severity score of the subplot (0–9 grade key) recorded on the flight day'],",
          "['Label of every sample', 'canopy severity score of the subplot (0–9 grade key) recorded on the flight day'], ['Varieties', 'V1 = PM 26, V2 = Pusa Vijay, V3 = PM 37'], ['Covariates', 'days after inoculation, variety, inoculation timing, growth stage, weather (T_{max}, T_{min}, RH, rainfall)'],"))
# common activities table
B.append(("['A. Field experiment, ground truth and datasets', 'A1–A4', 'labelled subplot list; post- and pre-symptomatic datasets']",
          "['A. Field experiment, ground truth and datasets', 'A1–A5', 'labelled subplot list; covariates; post- and pre-symptomatic datasets']"))
B.append(("['E. Normalisation and data preparation', 'E1–E6', 'normalised, screened and standardised features']",
          "['E. Normalisation and data preparation', 'E1–E4', 'normalised and standardised features; class weights']"))
# A1 varieties
B.append(("      'Three varieties of different susceptibility (V1 highly susceptible, V2 moderately susceptible, V3 resistant; names as recorded in the field book).',",
          "      'Three varieties: V1 = PM 26, V2 = Pusa Vijay, V3 = PM 37.',"))
B.append(("'Each plot carries a code (treatment, replication, plot number) that is stored with every sample.'],\n     'Staggered sowing",
          "'Each plot carries a code (treatment, replication, plot number) that is stored with every sample.'],\n     'Staggered sowing"))
# A5 covariates after the class example table
B.append(("    'How one score gives the three labels (dummy class counts).', [2500, 1134, 1134, 1134, 1134, 1134, 1136])",
          """    'How one score gives the three labels (dummy class counts).', [2500, 1134, 1134, 1134, 1134, 1134, 1136])
STEP('A5', 'Covariates: days after inoculation, variety, inoculation timing, growth stage and weather',
     'Disease severity changes with time, crop stage, variety and weather. These known factors must be recorded so that their effect can be separated from what the cameras add.',
     'Field book (sowing, inoculation and flight dates; variety; growth stage on each flight date); daily weather from the IARI agrometeorological observatory.',
     'Covariate table with one row per subplot-date → response analysis (Step 1.1.3), covariate baseline and sensor + covariate models (Steps 2.5.5 and 3.5.3), results by stage and treatment.',
     ['Days after inoculation (DAI): flight date minus inoculation date (numeric).',
      'Variety: V1 = PM 26, V2 = Pusa Vijay, V3 = PM 37 (categorical, one-hot coded in models).',
      'Inoculation timing: D1–D4, also expressed as crop age at inoculation in days (numeric).',
      'Growth stage of each plot on each flight date, read with the BBCH scale and coded as 1 = vegetative (BBCH 10–59), 2 = flowering (BBCH 60–69), 3 = pod formation (BBCH 70–79 and later) (ordinal).',
      'Weather: daily maximum and minimum air temperature (T_{max}, T_{min}), morning and afternoon relative humidity (RH I, RH II) and rainfall, summarised as the mean (rainfall: total) of the 7 days before each flight, plus the number of favourable days since inoculation (T_{max} 16–24 °C, RH I > 97% and RH II > 40%, the conditions reported to favour white rust on leaves).',
      'Covariates are not features of any camera and are not used in feature selection; they enter only the covariate models and the stratified results.'],
     'Weather conditions that favour white rust of Indian mustard and weather-based forecasting: Chattopadhyay et al. (2011), Saharan et al. (2014); BBCH growth stages: Lancashire et al. (1991), Meier (2018); stage-dependent spectral disease signals: Blasch et al. (2023), Liu et al. (2024); combining weather with remote sensing improved disease forecasts over weather alone: Zhang et al. (2014); days after inoculation in early detection: Mahlein et al. (2019), Zhu et al. (2017).')
TAB('covtab', [['Covariate', 'Type and coding', 'Varies between subplots on one date?', 'Main use'],
    ['Days after inoculation', 'numeric (days)', 'no (same inoculation date)', 'time trend; baseline model'],
    ['Variety (V1 PM 26, V2 Pusa Vijay, V3 PM 37)', 'categorical, one-hot', 'yes', 'baseline; stratified results; transfer test'],
    ['Inoculation timing (D1–D4)', 'categorical, or crop age at inoculation (days)', 'yes', 'baseline; stratified results; transfer test'],
    ['Growth stage (1 vegetative, 2 flowering, 3 pod formation)', 'ordinal from BBCH', 'yes (staggered sowing)', 'baseline; results by stage; flowering check'],
    ['Weather (T_{max}, T_{min}, RH I, RH II, rainfall; favourable days)', 'numeric, 7-day summaries', 'no (one value per date)', 'interpretation; baseline (time effect only)']],
    'Covariates recorded for every subplot-date. Weather is the same for all subplots on a date, so it can explain differences between dates but not between subplots.', [2900, 2200, 1900, 2306])
NOTE('Weather has only one value per flight date (eight values in the post-symptomatic period), so in a single season it cannot be separated from the date itself. It is therefore used for interpretation and inside the covariate baseline, and results of models that contain weather are labelled "within-season"; their transfer to another season must be tested with data of that season (Zhang et al., 2014; Ma et al., 2026).')"""))
# D2 subplot mean spectra without pixel counts / flower % / canopy cover
B.append(("     'One mean spectrum (and mean band values) per subplot, date and camera; vegetation pixel count, flower % and canopy cover % → Steps D3–D7 and Activity E.',\n     ['Average the masked vegetation pixels inside each subplot for every band of every camera.', 'Save the number of vegetation pixels, the flower % and the canopy cover % (from the class map) as quality and confounding checks.'],",
          "     'One mean spectrum (and mean band values) per subplot, date and camera → Steps D3–D7 and Activity E.',\n     ['Average the masked vegetation pixels inside each subplot for every band of every camera.', 'Join the covariates of Step A5 by the subplot code and date.'],"))
B.append(("'Normalised thermal features (Step E2): canopy minus air temperature", "'Normalised thermal features (Step E1): canopy minus air temperature"))
B.append(("labels (score, class, detection label), covariates (vegetation pixel count, flower %, canopy cover %) and features",
          "labels (score, class, detection label), covariates (days after inoculation, variety, inoculation timing, growth stage, weather summaries) and features"))
B.append(("['Covariates', 'flower %, canopy cover %, vegetation pixel count, days after inoculation, variety, inoculation timing', 'not used as disease features']",
          "['Covariates', 'days after inoculation, variety, inoculation timing, growth stage, weather (T_{max}, T_{min}, RH, rainfall)', 'not used as disease features']"))
# Activity E: remove E1 and E4, renumber
a = "P('Normalisation removes effects that are not caused by the disease"
B.append(("P('Normalisation removes effects that are not caused by the disease (illumination, weather, date, variety, units) and prepares the features for the models (Figure [[F:normal]]). Steps E1–E2 and E4 are done once on all data because they do not use the labels; Steps E3, E5 and E6 use statistics that are computed on the training part of each fold only.')\nFIG('normal', 'g25_normalisation.png', 'Flow chart of Activity E (Steps E1–E6).', 540)",
          "P('Normalisation removes effects that are not caused by the disease (weather, date, variety, units) and prepares the features for the models (Figure [[F:normal]]). Step E1 is done once on all data because it does not use the labels; Steps E2–E4 use statistics that are computed on the training part of each fold only. Date-to-date consistency of reflectance relies on the calibration panels flown on every date (Step B1).')\nFIG('normal', 'g25_normalisation.png', 'Flow chart of Activity E (Steps E1–E4).', 540)"))
e1s = s_e1 = None
B.append(("STEP('E1', 'Radiometric consistency between dates',", "STEP('E0', 'REMOVED',"))
B.append(("STEP('E2', 'Thermal normalisation',", "STEP('E1', 'Thermal normalisation',"))
B.append(("      'Difference from healthy plots of the same date and variety (Step E3).'],", "      'Difference from healthy plots of the same date and variety (Step E2).'],"))
B.append(("STEP('E3', 'Healthy-plot normalisation',", "STEP('E2', 'Healthy-plot normalisation',"))
B.append(("     'Features of all subplots; features of the healthy plots of the same date and variety (training replications only).',",
          "     'Features of all subplots; features of the healthy plots of the same date and variety in the training part (two or three plots of different inoculation timings, Step F1).',"))
B.append(("     ['For every feature, date and variety, compute the mean and standard deviation of the healthy plots of the training replications.',",
          "     ['For every feature, date and variety, compute the mean and standard deviation of the healthy subplots of that variety in the training part (8–12 subplots).',"))
B.append(("STEP('E4', 'Sample quality screening',", "STEP('E9', 'REMOVED',"))
B.append(("STEP('E5', 'Standardisation (z-score) with training statistics',", "STEP('E3', 'Standardisation (z-score) with training statistics',"))
B.append(("STEP('E6', 'Class weights',", "STEP('E4', 'Class weights',"))
# F1 healthy-plot rotation
B.append(("      'The 12 healthy plots are divided by variety (V1 → fold 1, V2 → fold 2, V3 → fold 3) so that every test fold contains healthy samples.',",
          "      'The 12 healthy plots are rotated so that every fold contains one healthy plot of each inoculation timing and at least one of each variety (Table [[T:healthyrot]]). Every training part then holds two or three healthy plots of every variety, which the healthy-plot normalisation (Step E2) needs, and every test fold contains healthy samples of all three varieties.',"))
B.append(("FIG('validation', 'g09_validation.png', 'Leave-one-replication-out outer folds and the inner cross-validation used for selection and tuning.', 520)",
          """TAB('healthyrot', [['Outer fold', 'Inoculated plots tested', 'Healthy plots tested (variety–timing)'], ['1', 'replication R1 (12 plots)', 'V1-D1, V2-D2, V3-D3, V1-D4'], ['2', 'replication R2 (12 plots)', 'V2-D1, V3-D2, V1-D3, V2-D4'], ['3', 'replication R3 (12 plots)', 'V3-D1, V1-D2, V2-D3, V3-D4']],
    'Rotation of the 12 healthy plots across the outer folds: each fold has every inoculation timing once and every variety at least once.', [1500, 3300, 4506])
FIG('validation', 'g09_validation.png', 'Leave-one-replication-out outer folds with the rotated healthy plots, and the inner cross-validation used for selection and tuning.', 520)"""))
B.append(("'Grouped (blocked) cross-validation: Roberts et al. (2017); spatial validation",
          "'Grouped (blocked) cross-validation: Roberts et al. (2017); healthy references of the same variety needed for normalisation: Oerke et al. (2006), Zarco-Tejada et al. (2018); spatial validation"))
# leakage table
B.append(("['E1–E2 (date consistency, thermal normalisation)', 'no', 'once, on all data'],", "['E1 (thermal normalisation)', 'no', 'once, on all data'],"))
B.append(("    ['E3 (healthy-plot normalisation)', 'no (uses healthy plots)', 'training healthy plots → applied to test data'], ['E5–E6 (standardisation, class weights)', 'no (statistics)', 'training part of each fold'],",
          "    ['E2 (healthy-plot normalisation)', 'no (uses healthy plots)', 'training healthy plots → applied to test data'], ['E3–E4 (standardisation, class weights)', 'no (statistics)', 'training part of each fold'], ['Covariate coding (Step A5)', 'no', 'once; standardised with training statistics'],"))
patch('mf3_body.py', B)

# remove the two REMOVED steps (E0 = old E1 with its text; E9 = old E4) as whole blocks
s = open('mf3_body.py').read()
i = s.index("STEP('E0', 'REMOVED',"); j = s.index("STEP('E1', 'Thermal normalisation',"); s = s[:i] + s[j:]
i = s.index("STEP('E9', 'REMOVED',"); j = s.index("STEP('E3', 'Standardisation (z-score)"); s = s[:i] + s[j:]
open('mf3_body.py', 'w').write(s)

# ============================================================== mf3_obj.py
O = []
O.append(("STEP('1.1.3', 'Response by variety, inoculation timing and days after inoculation',\n     'A feature may respond in one variety or crop age and not in another; treatments must be considered.',\n     'Responsive features; treatment codes.',",
          "STEP('1.1.3', 'Response by variety, inoculation timing, growth stage, days after inoculation and weather',\n     'A feature may respond in one variety, crop age or growth stage and not in another; treatments, stage and weather must be considered.',\n     'Responsive features; covariates (Step A5).',"))
O.append(("     ['Plot the main features against days after inoculation for each variety (V1–V3) and inoculation timing (D1–D4).', 'Compare inoculated plots with their healthy plot of the same treatment on every date.'],\n     'Treatment-wise disease response: Liu et al. (2024), Blasch et al. (2023), Feng et al. (2022).')",
          "     ['Plot the main features against days after inoculation for each variety (V1 PM 26, V2 Pusa Vijay, V3 PM 37) and inoculation timing (D1–D4).', 'Draw the response curves separately for the three growth stages (vegetative, flowering, pod formation), because yellow flowers and pods change canopy reflectance.', 'Compare inoculated plots with healthy plots of the same variety on every date.', 'Plot the disease progress (mean severity per date) together with the 7-day weather summaries and the favourable days since inoculation.'],\n     'Treatment-wise and stage-wise disease response: Liu et al. (2024), Blasch et al. (2023), Feng et al. (2022); flowering effects on Brassica canopy spectra: Sulik and Long (2016); weather and white rust development: Chattopadhyay et al. (2011).')"))
# SHAP-CARS settings
O.append(("     'Reflectance and first-derivative bands inside the effective ranges (training part).',\n     'Top 40% of bands by mean absolute Shapley value → Step 1.2.3.',",
          "     'Reflectance and first-derivative bands inside the effective ranges, plus the first-derivative bands of the red edge (680–760 nm), which are always kept as candidates (training part).',\n     'Top 40% of bands by mean absolute Shapley value → Step 1.2.3.',"))
O.append(("     ['Train a tree ensemble (extreme gradient boosting, 300 trees, depth 4, learning rate 0.05) to predict the severity score from the bands.',",
          "     ['Put the reflectance and first-derivative bands in one pool, because they are two forms of the same spectral information (one feature type); label each band as R_{λ} (reflectance) or FD_{λ} (first derivative).',\n      'Add the red-edge first-derivative bands (680–760 nm) even if the effective ranges miss part of the red edge, because the red-edge shift is a known disease indicator.',\n      'Train a tree ensemble (extreme gradient boosting, 300 trees, depth 4, learning rate 0.05) to predict the severity score from the bands; tree models do not need standardised inputs.',"))
O.append(("'Shapley values: Lundberg and Lee (2017), Lundberg et al. (2020); SHAP-based band selection: Ma et al. (2026).')",
          "'Shapley values: Lundberg and Lee (2017), Lundberg et al. (2020); SHAP-based band selection: Ma et al. (2026); red edge as a disease indicator: Filella and Peñuelas (1994), Yu et al. (2021).')"))
O.append(("     ['Choose the number of partial least squares (PLS) components (1–15) by Monte Carlo cross-validation (MCCV: 50 random 80/20 splits of the training plots).',",
          "     ['Standardise every pre-screened band (mean 0 and standard deviation 1 on the training part). CARS ranks bands by the size of their PLS coefficients, which depend on units: reflectance is about 0–0.6, first-derivative values about 0.001–0.01 nm^{−1}; without standardising, one form would be favoured for numerical, not biological, reasons.',\n      'Choose the number of partial least squares (PLS) components (1–15) by Monte Carlo cross-validation (MCCV: 50 random 80/20 splits of the training plots).',"))
O.append(("'50 iterations; 80% sampling per iteration; PLS components by MCCV (50 splits, maximum 15); CARS repeated 20 times with different random seeds.'",
          "'Bands standardised before PLS; 50 iterations; 80% sampling per iteration; PLS components by MCCV (50 splits, maximum 15); CARS repeated 20 times with different random seeds.'"))
O.append(("     ['Count how often each wavelength is selected over the 20 runs; keep those selected in at least 50%.', 'If more than 15 remain, keep the 15 most frequent.', 'Link each wavelength to a known absorption feature (chlorophyll, red edge, water, structure) for interpretation.'],",
          "     ['Count how often each wavelength is selected over the 20 runs; keep those selected in at least 50%.', 'If more than 15 remain, keep the 15 most frequent.', 'Report every selected wavelength with its label (R_{λ} or FD_{λ}) and the number of each type, so that it is clear which form carries the white rust signal.', 'Link each wavelength to a known absorption feature (chlorophyll, red edge, water, structure) for interpretation.'],"))
# 1.6.3 flowering check by growth stage
O.append(("'Check that selected features do not simply follow flower % or canopy cover (correlation with the covariates).'],",
          "'Check that the selected features respond within each growth stage (vegetative, flowering, pod formation), so that they are not only flowering or stage effects.'],"))
# Objective 2 intro
O.append(("P('Objective 2 builds and compares predictive models on the 1536 post-symptomatic samples of each camera. Three tasks are modelled: (A) healthy vs diseased, (B) severity classes and (C) severity score. Two comparisons are made: (1) all 15 sensor sets with machine learning, feature-fusion neural networks and the pseudo-image networks; (2) on the hyperspectral feature groups, DT-EDNet against EfficientNet, ResNet18 and ConvNeXt V2, repeating the design of Ma et al. (2026) with plot-grouped validation.')",
          "P('Objective 2 builds and compares predictive models on the 1536 post-symptomatic samples of each camera. For every single camera and for every combination of cameras (15 sensor sets), classification models (Task A, healthy vs diseased; Task B, severity classes) and regression models (Task C, severity score) are developed with all model families, so that the performance of every camera and every combination can be compared on the same folds (Table [[T:modelmatrix]]). In combinations, thermal, multispectral and red–green–blue features are added to the hyperspectral features by feature-level fusion for all models, including DT-EDNet and the comparison networks. A second comparison repeats the design of Ma et al. (2026) on the hyperspectral feature groups, with plot-grouped validation.')"))
O.append(("     ['Single camera (S1–S4): its disease-specific feature set is the input.', 'Combination (S5–S15): concatenate the feature sets of its cameras and apply the variance inflation factor rule (below 10) again across cameras.', 'Standardise with training statistics (Step E5).'],",
          "     ['Single camera (S1–S4): its disease-specific feature set is the input.', 'Combination (S5–S15): concatenate the feature sets of its cameras (thermal, multispectral and red–green–blue features added to the hyperspectral features) and apply the variance inflation factor rule (below 10) again across cameras.', 'Standardise with training statistics (Step E3).', 'The same fused set is the input of every model: machine learning, DNN-F1, DNN-F2 and the pseudo-image networks.'],"))
O.append(("'Class weights (Step E6) for all classifiers; macro-averaged metrics.'", "'Class weights (Step E4) for all classifiers; macro-averaged metrics.'"))
O.append(("    'The 15 sensor sets.', [900, 3600, 4806])",
          """    'The 15 sensor sets.', [900, 3600, 4806])
TAB('modelmatrix', [['Model family', 'Models', 'Sensor sets', 'Classification (Tasks A, B)', 'Regression (Task C)'],
    ['Machine learning', 'support vector machine / regression, random forest, extreme gradient boosting, k-nearest neighbours, partial least squares (discriminant analysis / regression)', 'all 15', 'yes', 'yes'],
    ['Feature-fusion networks', 'DNN-F1', 'all 15', 'yes', 'yes'],
    ['', 'DNN-F2 (one branch per camera)', 'the 11 combinations (S5–S15)', 'yes', 'yes'],
    ['Pseudo-image networks', 'DT-EDNet, EfficientNet-B0, ResNet18, ConvNeXt V2-Atto', 'all 15 (fused features of all cameras in the set)', 'yes', 'yes (linear output)'],
    ['Covariate models (Step 2.5.5)', 'best machine-learning model', 'covariates only; best sensor sets + covariates', 'yes', 'yes']],
    'Every model is built for every sensor set and task on the same folds, so that single cameras and combinations can be compared directly.', [1800, 3200, 1800, 1300, 1206])"""))
# 2.3.3 multi-camera layout
O.append(("     ['Order the features by group and, within the spectral group, by wavelength (optimal wavelengths, indices, texture, TTFI, then other cameras), so that neighbouring pixels hold related features.',\n      'Choose k = the smallest integer with k² ≥ number of features (minimum 3); fill the k × k grid row by row.',",
          "     ['Order the features by camera (hyperspectral, multispectral, red–green–blue, thermal) and, within the hyperspectral camera, by group and wavelength (optimal wavelengths, indices, texture, TTFI), so that neighbouring pixels hold related features.',\n      'Choose k so that the k × k grid holds all features when every camera starts on a new row (minimum 3); fill the grid row by row. A small group such as the thermal features then stays together in one row and is not split.',"))
O.append(("      'Example: 22 features → 5 × 5 image with 3 padded pixels (Figure [[F:pseudo]]).'],",
          "      'Example (hyperspectral only): 22 features → 5 × 5 image with 3 padded pixels (Figure [[F:pseudo]]). Example (S7, hyperspectral + thermal): 16 hyperspectral features fill three rows of six, the 6 thermal features fill the fourth row and two empty rows complete a 6 × 6 image.'],"))
O.append(("     'Pseudo-two-dimensional input of spectral features: Ma et al. (2026); arranging non-image features as images for convolutional networks: Sharma et al. (2019).')",
          "     'Pseudo-two-dimensional input of spectral features: Ma et al. (2026); arranging non-image features as images for convolutional networks: Sharma et al. (2019); attention relates features regardless of their position: Vaswani et al. (2017).',\n     note='Ma et al. (2026) used DT-EDNet with hyperspectral features only. Its use with thermal, multispectral and red–green–blue features is an extension made in this study; whether it helps is shown by comparing each fused set with the hyperspectral set (S1) and with DNN-F2, which processes each camera in its own branch.')"))
# 2.3.8 tune once
O.append(("      'Tuning: learning rate ∈ {3 × 10^{−4}, 6 × 10^{−4}, 1 × 10^{−3}} and dropout ∈ {0.03, 0.1, 0.3}, same grid for all four networks.',",
          "      'Tuning: learning rate ∈ {3 × 10^{−4}, 6 × 10^{−4}, 1 × 10^{−3}} and dropout ∈ {0.03, 0.1, 0.3}, same grid for all four networks. To keep the computing load feasible (about 34 000 runs if every case were tuned), each network is tuned once, on outer fold 1, sensor set S15 and Task B with one seed, and the chosen values are then used for all sensor sets, tasks and folds (about 3800 runs).',"))
# 2.6.2 transfer test without resistance assumption + season limitation
O.append(("     ['Train on two varieties and test on the third (mainly V1 ↔ V2, because the resistant variety has few diseased samples).', 'Train on three inoculation timings and test on the fourth.'],",
          "     ['Train on two varieties and test on the third, for each variety in turn (V1 PM 26, V2 Pusa Vijay, V3 PM 37); a variety with very few diseased samples is used only for the detection task.', 'Train on three inoculation timings and test on the fourth.', 'All results come from one season; transfer to another season needs an independent test with data of that season, as done across years by Ma et al. (2026).'],"))
# Objective 3 healthy normalisation step renumber
O.append(("     ['Apply Step E3 to every feature: z_{h} = (x − mean_{healthy}) / SD_{healthy}, with the healthy plots of the same date and variety in the training replications.', 'Apply the same reference to the test samples.'],",
          "     ['Apply Step E2 to every feature: z_{h} = (x − mean_{healthy}) / SD_{healthy}, with the healthy plots of the same date and variety in the training part (rotated healthy plots, Table [[T:healthyrot]]).', 'Apply the same reference to the test samples.'],"))
# new Step 2.5.5 covariate models, after 2.5.4 card (insert before Activity 2.6 heading)
O.append(("H2('Activity 2.6 – Robustness and maps')",
          """STEP('2.5.5', 'Covariate baseline and sensor + covariate models',
     'Severity rises with days after inoculation and differs with variety, inoculation timing, growth stage and weather; a sensor model could look accurate only because it learns time or stage. The cameras must add information beyond these known factors.',
     'Covariates (Step A5); fused feature sets of the sensor sets; same folds.',
     'Accuracy of the covariate-only model, of the sensor models and of the sensor + covariate models → evidence of what the cameras add.',
     ['Covariate-only model: the best machine-learning model (Activity 2.2) with days after inoculation, variety, inoculation timing, growth stage and the weather summaries as the only inputs, for Tasks A, B and C.',
      'Sensor models (main results, Activities 2.2–2.3): a sensor set is reported as useful only if it is better than the covariate-only model.',
      'Sensor + covariate models: the best three sensor sets with the covariates added (one-hot variety and inoculation timing, ordinal growth stage, numeric days after inoculation and weather), to show whether known context improves prediction.',
      'Report all three side by side for every task; label models that contain weather as "within-season" (Step A5).'],
     'Combining weather with remote sensing compared with a weather-only model: Zhang et al. (2014); weather-based white rust forecasting: Chattopadhyay et al. (2011); stage-dependent disease signals: Blasch et al. (2023); simple baseline models as a reference for predictive models: Kuhn and Johnson (2013).')
TAB('covex', [['Model (dummy results, Task B)', 'Inputs', 'Macro-F1', 'Gain over covariate model'], ['Covariate-only', 'days after inoculation, variety, timing, stage, weather', '0.41', '—'], ['Hyperspectral (S1)', 'S1 fused features', '0.66', '+0.25'],
    ['Hyperspectral + thermal (S7)', 'S7 fused features', '0.69', '+0.28'], ['Hyperspectral + thermal + covariates', 'S7 features + covariates', '0.71', '+0.30 (within-season)']],
    'Worked example (dummy data): how the covariate baseline is used to show what the cameras add.', [2700, 3200, 1300, 2106])
H2('Activity 2.6 – Robustness and maps')"""))
# Objective 3: covariate baseline step
O.append(("FIG('earliest', 'g23_dummy_earliest.png',",
          """STEP('3.5.3', 'Covariate baseline for the pre-symptomatic stage',
     'Before symptoms, infection depends strongly on weather after inoculation and on variety; the cameras must be shown to detect more than these factors.',
     'Covariates (Step A5) of the pre-symptomatic dates; pre-symptomatic models.',
     'Accuracy of the covariate-only model compared with the sensor models → evidence that the early signal comes from the plants.',
     ['Fit the best machine-learning model with days after inoculation, variety, inoculation timing, growth stage and the weather summaries only.', 'Report the sensor models and the best sensor set + covariates next to it, as in Step 2.5.5.'],
     'Zhang et al. (2014); Chattopadhyay et al. (2011); Zhu et al. (2017).')
FIG('earliest', 'g23_dummy_earliest.png',"""))
patch('mf3_obj.py', O)

# ============================================================== mf3_end.py
E = []
E.append((" ['A1–A4', 'field design, scores', 'labelled subplot list; post- and pre-symptomatic datasets', 'D8, F1, all objectives'],",
          " ['A1–A4', 'field design, scores', 'labelled subplot list; post- and pre-symptomatic datasets', 'D8, F1, all objectives'],\n ['A5', 'field book, weather records', 'covariate table (days after inoculation, variety, timing, growth stage, weather)', 'D2, 1.1.3, 2.5.5, 3.5.3'],"))
E.append((" ['D1–D2', 'masked layers, polygons', 'subplot mean spectra and band values; pixel counts', 'D3–D7, E4'],", " ['D1–D2', 'masked layers, polygons', 'subplot mean spectra and band values joined with covariates', 'D3–D7'],"))
E.append((" ['D3–D7', 'subplot values', 'spectral, index, texture, colour and thermal groups', 'D8, E2'],", " ['D3–D7', 'subplot values', 'spectral, index, texture, colour and thermal groups', 'D8, E1'],"))
E.append((" ['E1–E2', 'reflectance and temperatures', 'date-consistent reflectance; normalised thermal features', 'D, Objective 1'],\n ['E3', 'features, healthy plots', 'healthy-normalised features', 'Objective 3; thermal difference features'],\n ['E4–E6', 'feature tables', 'clean samples; standardised features; class weights', 'all models'],",
          " ['E1', 'temperatures', 'normalised thermal features', 'D7, Objective 1'],\n ['E2', 'features, healthy plots (rotated across folds)', 'healthy-normalised features', 'Objective 3; thermal difference features'],\n ['E3–E4', 'feature tables', 'standardised features; class weights', 'all models'],"))
E.append((" ['F1–F3', 'clean labelled tables', 'outer and inner folds; tuning plan; leakage checklist', 'Objectives 2–3'],", " ['F1–F3', 'labelled tables', 'outer and inner folds with rotated healthy plots; tuning plan; leakage checklist', 'E2, Objectives 2–3'],"))
E.append((" ['2.5.1–2.5.4', 'metric tables, models', 'best sensor set and model; contributions; ablation; explanation', '2.6, conclusions'],",
          " ['2.5.1–2.5.5', 'metric tables, models, covariates', 'best sensor set and model; contributions; ablation; explanation; gain over the covariate baseline', '2.6, conclusions'],"))
E.append((" ['Normalise thermal values against healthy plots or air temperature on each date', 'Steps E2 and E3', 'included'],", " ['Normalise thermal values against healthy plots or air temperature on each date', 'Steps E1 and E2', 'included'],"))
E.append((" ['Endmember extraction', 'one step', 'Activity C with eight steps', 'clarity; user request'],",
          " ['Endmember extraction', 'one step', 'Activity C with eight steps', 'clarity; user request'],\n ['Covariates', 'flower %, canopy cover %, vegetation pixel count', 'days after inoculation, variety, inoculation timing, growth stage, weather', 'user request; covariate baseline'],\n ['Radiometric consistency between dates; sample quality screening', 'Steps E1 and E4', 'not performed', 'user request; panels on every flight (Step B1)'],\n ['Varieties', 'V1 susceptible, V2 moderately susceptible, V3 resistant (assumed)', 'V1 PM 26, V2 Pusa Vijay, V3 PM 37 (no susceptibility assumed)', 'field record'],"))
E.append(("H1('7. Definitions of indices and features')",
          """H2('6.5 Drawbacks found and corrected in this version')
TAB('drawbacks', [['Drawback in the previous version', 'Correction', 'Supporting studies'],
 ['Healthy plots were assigned to folds by variety (V1 → fold 1, …), so the training part of each fold had no healthy plots of the test variety. Healthy-plot normalisation with the same variety was then impossible, and healthy samples of the test variety were never seen in training.', 'Healthy plots rotated across folds: every fold has each inoculation timing once and every variety at least once (Table [[T:healthyrot]]).', 'Roberts et al. (2017); Oerke et al. (2006); Zarco-Tejada et al. (2018)'],
 ['Severity rises with time and stage, so a model could appear accurate by learning days after inoculation or growth stage instead of disease.', 'Covariate-only baseline and sensor + covariate models (Steps 2.5.5 and 3.5.3); results by growth stage.', 'Zhang et al. (2014); Blasch et al. (2023); Kuhn and Johnson (2013)'],
 ['Flowering effects were checked with flower %, which mixes flowers with disease-related colour changes.', 'Growth stage recorded with the BBCH scale; responses and results reported for each stage.', 'Lancashire et al. (1991); Meier (2018); Sulik and Long (2016)'],
 ['Pooled reflectance and first-derivative bands in CARS without standardisation would favour one form for numerical reasons; the effective ranges could miss the red edge.', 'Bands standardised before PLS; red-edge first derivative always kept; bands labelled R_{λ} or FD_{λ}.', 'Li et al. (2009); Mehmood et al. (2012); Filella and Peñuelas (1994); Yu et al. (2021)'],
 ['Multi-camera pseudo-images could split a small camera group (thermal) across rows.', 'Each camera starts on a new row of the pseudo-image.', 'Sharma et al. (2019); Ma et al. (2026)'],
 ['Tuning every network for every case needed about 34 000 runs.', 'Tune once (fold 1, S15, Task B, one seed) and reuse the settings: about 3800 runs.', 'Ma et al. (2026); Cawley and Talbot (2010)'],
 ['Weather has one value per date and cannot be separated from the date in one season.', 'Weather used for interpretation and in covariate models labelled "within-season".', 'Zhang et al. (2014); Chattopadhyay et al. (2011)'],
 ['A variety was assumed to be resistant without field evidence.', 'Variety names from the field record; transfer test run for each variety in turn.', 'Blasch et al. (2023)'],
 ['All results come from one season.', 'Stated as a limitation; leave-one-variety-out and leave-one-timing-out tests used as internal transfer tests.', 'Ma et al. (2026); Roberts et al. (2017)']],
 'Drawbacks of the previous version and how they are corrected.', [3500, 3500, 2306], 15)

H1('7. Definitions of indices and features')"""))
E.append(("    ('Why are flowers kept in the subplot spectrum?', 'The canopy score includes the inflorescence and staghead; flower % is recorded and checked so that selected features are not only flowering effects (Sulik and Long, 2016).'),",
          "    ('Why are flowers kept in the subplot spectrum?', 'The canopy score includes the inflorescence and staghead; the growth stage (vegetative, flowering, pod formation) is recorded with the BBCH scale and results are reported for each stage, so that selected features are not only flowering effects (Sulik and Long, 2016; Meier, 2018).'),\n    ('How are weather and other covariates used?', 'Days after inoculation, variety, inoculation timing, growth stage and weather form a covariate-only baseline; a camera is useful only if it beats this baseline. Weather has one value per date, so models that contain it are labelled within-season (Zhang et al., 2014; Chattopadhyay et al., 2011).'),"))
E.append(("    ['2', 'Activities D–F: features, normalisation, folds; Activity 1.1', 'feature tables; response curves'],",
          "    ['2', 'Activities D–F: features, covariates, normalisation, folds; Activity 1.1', 'feature and covariate tables; response curves'],"))
patch('mf3_end.py', E)
print('patched')
