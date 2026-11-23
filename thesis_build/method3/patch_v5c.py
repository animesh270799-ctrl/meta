"""Revision 5 (part c): mf3_obj.py – Objective 1 at two stages with new Activity 1.8 (pre-symptomatic characterisation, 576 samples per camera),
tasks from the disease index, detailed covariate baseline (Step 2.5.5), independent testing at Bharatpur (Activity 2.7), Objective 3 dates."""
def patch(f, reps):
    s = open(f).read()
    for a, b in reps:
        n = s.count(a); assert n == 1, (f, n, a[:100]); s = s.replace(a, b)
    open(f, 'w').write(s)
s = open('mf3_obj.py').read()
KEY = "P('Objective 1 describes how each camera sees white rust and selects the features that carry disease information. It uses the 1920 post-symptomatic samples of each camera."
if KEY in s:
  i = s.index(KEY); j = s.index("\n", i)
  s = s[:i] + "P('Objective 1 describes how each camera sees white rust and selects the features that carry disease information, at two stages. At the post-symptomatic stage it uses the 1920 post-symptomatic samples of each camera with the disease index as target (Activities 1.1–1.7). At the pre-symptomatic stage it uses the 576 pre-symptomatic samples of each camera with later-infected vs healthy as target (Activity 1.8). For description and interpretation the steps are run on all samples of a stage; for prediction (Objectives 2 and 3) exactly the same steps are repeated inside the training part of every fold (Step F2), so the test replication never influences the selection.')" + s[j:]
open('mf3_obj.py', 'w').write(s)
patch('mf3_obj.py', [
 ("FIG('obj1', 'g05_obj1.png', 'Flow chart of Objective 1 (Activities 1.1–1.6).', 540)", "FIG('obj1', 'g05_obj1.png', 'Flow chart of Objective 1 (Activities 1.1–1.8).', 540)"),
 ("    ['1.7 Biochemical and biophysical basis', '1.7.1–1.7.6', 'paired comparisons, analysis of variance, within-date correlation', 'disease effect by date and growth stage; parameter–feature links']],",
  "    ['1.7 Biochemical and biophysical basis', '1.7.1–1.7.6', 'paired comparisons, analysis of variance, within-date correlation', 'disease effect by date and growth stage; parameter–feature links'],\n    ['1.8 Pre-symptomatic characterisation', '1.8.1–1.8.5', 'the same steps with the label later-infected vs healthy (576 samples per camera)', 'pre-symptomatic response; earliest-responding features; pre-symptomatic feature set']],"),
 # Task definitions
 ("['Task A, detection: healthy (grade 0) vs diseased (grade above 0).', 'Task B, severity classes: grades 0, 1, 3, 5, 7, 9 (merged if a class has fewer than 5% of samples).', 'Task C, regression: severity score.',",
  "['Task A, detection: healthy (DI = 0) vs diseased (DI above 0).', 'Task B, severity classes: DI classes 0, 1, 3, 5, 7, 9 (merged if a class has fewer than 5% of samples).', 'Task C, regression: disease index DI (%).',"),
 ("['2.7 Second-stage validation at Bharatpur', '2.7.1–2.7.4', 'accuracy of frozen models on independent research-farm and farmers\\' field data; farm maps']]", "['2.7 Independent testing at Bharatpur', '2.7.1–2.7.4', 'accuracy of frozen models on independent research-farm and farmers\\' field data; farm maps']]"),
 # Step 2.5.5
 ("""     ['Covariate-only model: the best machine-learning model (Activity 2.2) with days after inoculation, variety, inoculation timing, growth stage and the weather summaries as the only inputs, for Tasks A, B and C.',
      'Sensor models (main results, Activities 2.2–2.3): a sensor set is reported as useful only if it is better than the covariate-only model.',
      'Sensor + covariate models: the best three sensor sets with the covariates added (one-hot variety and inoculation timing, ordinal growth stage, numeric days after inoculation and weather), to show whether known context improves prediction.',
      'Report all three side by side for every task; label models that contain weather as "within-season" (Step A6).'],""",
  """     ['Samples: inoculated, unsprayed subplots only; the healthy plots are fungicide-protected and share every covariate with their inoculated plots, so they would teach a false rule. Weather windows end the day before each flight (no look-ahead).',
      'B1 – interpretable epidemiological model: logistic regression (Task A), proportional-odds ordinal logistic regression (Task B; McCullagh, 1980) and a linear model of the disease index with days after inoculation and its square (Task C; disease-progress shape, Madden et al., 2007), with variety, inoculation timing and growth stage.',
      'B2 – machine-learning baseline: the best model of Activity 2.2 (for example random forest; Breiman, 2001) with all covariates, including the weather summaries and favourable days, tuned with the same inner grid search as the sensor models.',
      'M0 = the stronger of B1 and B2 (covariates only); M1 = the sensor models of each sensor set (Activities 2.2–2.3); M2 = the best three sensor sets + covariates (one-hot variety and timing, ordinal growth stage, numeric days after inoculation and weather), labelled "within-season".',
      'Gains: ΔS = metric(M1) − metric(M0) (what the cameras add); ΔC = metric(M2) − metric(M1) (what known context adds); ΔT = metric(M2) − metric(M0). Metrics: macro-F1 and AUC (Task A), macro-F1 and quadratic-weighted kappa (Task B), R² and RMSE (Task C).',
      'Is a gain real? 95% confidence interval from 2000 bootstrap resamples of the pooled test predictions that resample whole plots (Efron and Tibshirani, 1993); AUCs of M1 and M0 compared with the DeLong test (DeLong et al., 1988). A gain is real only if the interval excludes zero, it is larger than the fold-to-fold standard deviation and it has the same sign in all three folds.',
      'The coefficients of B1, fitted on all inoculated subplots with standardised covariates, show the direction and size of each known effect (for example later sowing or variety).'],"""),
 ("'Combining weather with remote sensing compared with a weather-only model: Zhang et al. (2014); weather-based white rust forecasting: Chattopadhyay et al. (2011); stage-dependent disease signals: Blasch et al. (2023); simple baseline models as a reference for predictive models: Kuhn and Johnson (2013).')",
  "'Calendar effect in disease prediction: De Wolf and Isard (2007); weather-only machine learning for disease severity: Bijlwan et al. (2025); combining weather with remote sensing compared with a weather-only model: Zhang et al. (2014), Ruan et al. (2022); weather-based white rust forecasting: Chattopadhyay et al. (2011); simple baseline models as a reference for predictive models: Kuhn and Johnson (2013); bootstrap and DeLong test: Efron and Tibshirani (1993), DeLong et al. (1988).')"),
 ("TAB('covex', [['Model (dummy results, Task B)', 'Inputs', 'Macro-F1', 'Gain over covariate model'], ['Covariate-only', 'days after inoculation, variety, timing, stage, weather', '0.41', '—'], ['Hyperspectral (S1)', 'S1 fused features', '0.66', '+0.25'],\n    ['Hyperspectral + thermal (S7)', 'S7 fused features', '0.69', '+0.28'], ['Hyperspectral + thermal + covariates', 'S7 features + covariates', '0.71', '+0.30 (within-season)']],\n    'Worked example (dummy data): how the covariate baseline is used to show what the cameras add.', [2700, 3200, 1300, 2106])",
  "TAB('covex', [['Model set (dummy results, Task B)', 'Inputs', 'Macro-F1', 'Gain (95% bootstrap interval)'], ['M0 – covariate baseline (stronger of B1, B2)', 'days after inoculation, variety, timing, stage, weather', '0.41', '—'], ['M1 – hyperspectral (S1)', 'S1 fused features', '0.66', 'ΔS = +0.25 (+0.18 to +0.31): real'],\n    ['M1 – hyperspectral + thermal (S7)', 'S7 fused features', '0.69', 'ΔS = +0.28 (+0.21 to +0.34): real'], ['M2 – hyperspectral + thermal + covariates', 'S7 features + covariates', '0.71', 'ΔC = +0.02 (−0.02 to +0.06): not real; within-season']],\n    'Worked example (dummy data): how the covariate baseline and the bootstrap intervals show what the cameras add.', [2900, 2700, 1100, 2606])"),
 # Activity 2.7 wording
 ("H2('Activity 2.7 – Second-stage validation at Bharatpur')\nP('The first-stage validation (Activity F, leave-one-replication-out inside the IARI field) chooses the models and estimates their accuracy on new plots of the same field. The second stage tests the final models on independent data from research farms and farmers\\' fields at Bharatpur (Step A7), with other soils, varieties, management and a natural epidemic ([[F:twostage]]).')\nFIG('twostage', 'g28_twostage.png', 'Two-stage validation: first stage inside the IARI field, second stage on independent Bharatpur data with frozen models.', 560)",
  "H2('Activity 2.7 – Independent testing at Bharatpur')\nP('The validation (Activity F, leave-one-replication-out inside the IARI field) chooses the models and estimates their accuracy on new plots of the same field. Independent testing then applies the frozen final models once to data from research farms and farmers\\' fields at Bharatpur (Step A7), with other soils, varieties, management and a natural epidemic ([[F:twostage]]). This is a test, not a validation: nothing is selected, tuned or retrained on the Bharatpur data.')\nFIG('twostage', 'g28_twostage.png', 'Internal validation inside the IARI field and independent testing on Bharatpur data with frozen models.', 560)"),
 ("     'Second-stage accuracy tables and the loss of accuracy from stage 1 to stage 2 → conclusions on transferability.',", "     'Independent test accuracy tables and the loss of accuracy from the internal validation to the independent test → conclusions on transferability.',"),
 ("'Report the results for research farms and farmers\\' fields separately, by variety and by growth stage, and the difference from the first-stage accuracy.',", "'Report the results for research farms and farmers\\' fields separately, by variety and by growth stage, and the difference from the accuracy of the internal validation.',"),
 ("     ['Repeat feature selection and tuning on all IARI data with grouped inner cross-validation (folds by plot), exactly as in the first stage.',", "     ['Repeat feature selection and tuning on all IARI data with grouped inner cross-validation (folds by plot), exactly as in the internal validation.',"),
 ("     'The validation data must pass through exactly the same processing, otherwise differences in processing would look like model errors.',", "     'The test data must pass through exactly the same processing, otherwise differences in processing would look like model errors.',"),
 ("TAB('twostaget', [['Item', 'First stage (internal)', 'Second stage (independent)'],", "TAB('twostaget', [['Item', 'Validation (internal, IARI field)', 'Independent testing (Bharatpur)'],"),
 ("['Infection', 'artificial inoculation (10 January 2027)', 'natural epidemic'],", "['Infection', 'artificial inoculation (30 December 2026)', 'natural epidemic'],"),
 ("    'The two validation stages.', [2000, 3600, 3706])", "    'Internal validation and independent testing.', [2000, 3600, 3706])"),
 # Objective 3 dates and wording
 ("STEP('3.1.2', 'Physiological changes before symptoms (18 January 2027)',", "STEP('3.1.2', 'Physiological changes before symptoms (7 January 2027)',"),
 ("'Biochemical and biophysical parameters of 18 January (Step A8); later severity of the same plots.',", "'Biochemical and biophysical parameters of 7 January (Step A8); later severity of the same plots.',"),
 ("'Correlate the pre-symptomatic parameters of the inoculated plots with their percent disease index on 28 January (first post-symptomatic sampling date).',", "'Correlate the pre-symptomatic parameters of the inoculated plots with their disease index on 18 January (first post-symptomatic sampling date of Step A8).',"),
 ("['Classification: healthy = subplots of the 12 healthy plots; infected = inoculated subplots that show pustules later; inoculated subplots that never show symptoms are excluded from the infected class.', 'Regression: target = severity score of the same subplot on the first post-symptomatic date.',",
  "['Classification: healthy = subplots of the 12 healthy plots; infected = inoculated subplots that show pustules later; inoculated subplots that never show symptoms are excluded from the infected class (the same labels as Activity 1.8).', 'Regression: target = disease index of the same subplot on the first post-symptomatic date.',"),
 ("['Repeat the one-method-per-type selection with the pre-symptomatic labels:", "['Start from the pre-symptomatic feature sets of Activity 1.8 and repeat the one-method-per-type selection with the pre-symptomatic labels inside every training fold:"),
 ("TAB('earlyex', [['Pre-symptomatic flight (days after inoculation)', '12 Jan (2)', '15 Jan (5)', '18 Jan (8)'],", "TAB('earlyex', [['Pre-symptomatic flight (days after inoculation)', '1 Jan (2)', '4 Jan (5)', '7 Jan (8)'],"),
 ("'Worked example (dummy data): the hyperspectral + thermal set reaches 0.70 on 18 January (earliest detection day = 8 days after inoculation),", "'Worked example (dummy data): the hyperspectral + thermal set reaches 0.70 on 7 January (earliest detection day = 8 days after inoculation),"),
 ("'Report the sensor models and the best sensor set + covariates next to it, as in Step 2.5.5.'],", "'Report the sensor models and the best sensor set + covariates next to it, with the same B1/B2 baselines, bootstrap intervals and real-gain rule as in Step 2.5.5.'],"),
 ("STEP('3.5.4', 'Second-stage validation of the pre-symptomatic models',", "STEP('3.5.4', 'Independent testing of the pre-symptomatic models',"),
 ("     'Second-stage accuracy of the pre-symptomatic models, where the data allow → conclusions on early warning.',", "     'Independent test accuracy of the pre-symptomatic models, where the data allow → conclusions on early warning.',"),
 ("where no early flight or healthy reference exists, the pre-symptomatic models are validated in the first stage only, and this is stated.'],", "where no early flight or healthy reference exists, the pre-symptomatic models are evaluated with the internal validation only, and this is stated.'],"),
])
# ---------------- new Activity 1.8 (after Activity 1.7, before the satellite box)
s = open('mf3_obj.py').read(); a = "BOX('Link to satellite monitoring (optional extension, not part of the six-month plan).',"
assert s.count(a) == 1
A18 = r"""# ---------------------------------------------------------------- 1.8
H2('Activity 1.8 – Characterisation of the pre-symptomatic stage')
P('Activities 1.1–1.7 describe white rust after symptoms appear. Activity 1.8 repeats the characterisation before symptoms, with the 576 pre-symptomatic subplot samples of each camera (3 flights × 192 subplots). No grade exists yet, so the target is later-infected vs healthy: the label of an inoculated subplot is taken from its later status (Step A5). The result is the pre-symptomatic feature set of each camera and a list of the earliest-responding wavelengths, indices, texture and thermal features, which feed the prediction models of Objective 3 ([[F:presym]]).')
FIG('presym', 'g31_presym.png', 'Activity 1.8 – characterisation of the pre-symptomatic stage (Steps 1.8.1–1.8.5).', 540)
TAB('presymn', [['Flight', 'Days after inoculation', 'Healthy subplots', 'Inoculated subplots', 'Total'], ['1 Jan 2027', '2', '48', '144', '192'], ['4 Jan 2027', '5', '48', '144', '192'], ['7 Jan 2027', '8', '48', '144', '192'], ['All', '', '144', '432 (later-infected subplots only are used)', '576']],
    'Pre-symptomatic samples per camera.', [1800, 1800, 1600, 2600, 1506], 16)
STEP('1.8.1', 'Pre-symptomatic response curves',
     'Shows whether and where the spectrum, temperature and texture of later-infected subplots already differ from healthy subplots.',
     'Pre-symptomatic features of all cameras; later-status labels.', 'Mean curves and percentage differences by date → Steps 1.8.2–1.8.5.',
     ['Mean reflectance, first derivative, indices, texture and thermal features of later-infected and healthy subplots on each pre-symptomatic date (± 1 standard deviation).', 'Percentage difference from healthy: Δ% = (x_{infected} − x_{healthy}) / x_{healthy} × 100, per feature and date.', 'Separate curves for each variety and inoculation timing.'],
     'Pre-symptomatic spectral and thermal changes: Zarco-Tejada et al. (2018), Calderón et al. (2013), Zhu et al. (2017); early changes in rusts and mildews: Terentev et al. (2023).')
STEP('1.8.2', 'Univariate tests with plot means and effect sizes',
     'Gives a simple statistical answer to which features differ before symptoms, without pseudo-replication.',
     'Plot means of every feature (unit = plot) on each pre-symptomatic date.', 'Effect size and adjusted p-value of every feature and date → interpretation; Step 1.8.4.',
     ['Average the subplots of each plot so that the plot is the experimental unit (Hurlbert, 1984).', 'Welch t-test (or Mann–Whitney U test for skewed features) between later-infected inoculated plots and healthy plots for every feature and date.', 'Report the effect size (Hedges g) with its 95% confidence interval and control false discoveries with the Benjamini–Hochberg procedure (5%).'],
     'Hurlbert (1984); Sullivan and Feinn (2012); Benjamini and Hochberg (1995).')
STEP('1.8.3', 'Pre-symptomatic effective ranges and optimal wavelengths',
     'The wavelengths that respond earliest may differ from those that respond after symptoms.',
     'Reflectance and first derivative; binary later-status label (training part).', 'Pre-symptomatic effective ranges and optimal wavelengths → Step 1.8.4 and Objective 3.',
     ['NDSI and RSI maps with the binary label (area under the curve or point-biserial r^{2} of each band pair).', 'SHAP-CARS with partial least squares discriminant analysis on the binary label (Activity 1.2 settings).', 'Run inside the training part of every fold when used for prediction.'],
     'Ma et al. (2026); Li et al. (2009); Lundberg and Lee (2017); Zhu et al. (2017).')
STEP('1.8.4', 'Indices, texture and thermal features before symptoms',
     'Small early changes are easier to see after removing date, weather and variety effects.',
     '48 published indices, red-edge parameters, texture and thermal features; healthy plots of the same date and variety.', 'Pre-symptomatic feature set of each camera (variance inflation factor below 10) → Objective 3 (Activity 3.3).',
     ['Healthy-plot normalisation (Step E2) of every feature.', 'Indices: ReliefF with the two classes; texture: mRMR; thermal: canopy minus air temperature, normalised relative canopy temperature, crop water stress index and difference from healthy plots.', 'Pool the survivors and keep features with a variance inflation factor below 10.'],
     'Oerke et al. (2006); Calderón et al. (2014); Robnik-Šikonja and Kononenko (2003); Peng et al. (2005); Dormann et al. (2013).')
STEP('1.8.5', 'Earliest-responding features',
     'Shows how early and with which feature type white rust can be seen.',
     'Effect sizes and selected features of the three pre-symptomatic dates.', 'Earliest date on which each feature differs from healthy, by variety and timing; physiological explanation with Step 3.1.2.',
     ['For every selected feature, find the first date (2, 5 or 8 days after inoculation) on which the effect size is significant and larger than 0.8.', 'Compare the earliest features with the pre-symptomatic biochemical and biophysical parameters of 7 January (Step 3.1.2).'],
     'Mahlein et al. (2019); Zarco-Tejada et al. (2018); Sullivan and Feinn (2012).')

"""
s = s.replace(a, A18 + a); open('mf3_obj.py', 'w').write(s)
print('part c ok')
