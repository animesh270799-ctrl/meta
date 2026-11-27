// Three slides: covariate (sensor-free) baseline model, Steps 2.5.5 / 3.5.3, season 2026-27
const { pres, F, FS, C, THEME, S, sec, T, BL, box, arr, chain, tb, refline } = require('./adv_lib.js');
const { applyTheme } = require(process.env.SKILL_DIR + '/scripts/apply_theme.js');
const OUT = __dirname + '/../outputs/Covariate_baseline_model_3slides.pptx';
const REFS = [
  'Bijlwan, A., Ranjan, R., Singh, M., Purohit, R., Nath, A.J., Chakravarty, S. (2025). Predicting crop disease severity using real time weather variability through machine learning algorithms. Scientific Reports 15, 34767. https://doi.org/10.1038/s41598-025-18613-7',
  'Breiman, L. (2001). Random forests. Machine Learning 45(1), 5–32.',
  'Chattopadhyay, C., et al. (2011). Epidemiology and development of forecasting models for white rust of Brassica juncea in India. Archives of Phytopathology and Plant Protection 44(8), 751–763. https://doi.org/10.1080/03235400903458571',
  'DeLong, E.R., DeLong, D.M., Clarke-Pearson, D.L. (1988). Comparing the areas under two or more correlated receiver operating characteristic curves: a nonparametric approach. Biometrics 44(3), 837–845.',
  'De Wolf, E.D., Isard, S.A. (2007). Disease cycle approach to plant disease prediction. Annual Review of Phytopathology 45, 203–220. https://doi.org/10.1146/annurev.phyto.44.070505.143329',
  'Efron, B., Tibshirani, R.J. (1993). An Introduction to the Bootstrap. Chapman & Hall, New York.',
  'Kuhn, M., Johnson, K. (2013). Applied Predictive Modeling. Springer, New York.',
  'Lancashire, P.D., et al. (1991). A uniform decimal code for growth stages of crops and weeds. Annals of Applied Biology 119(3), 561–601.',
  'Madden, L.V., Hughes, G., van den Bosch, F. (2007). The Study of Plant Disease Epidemics. APS Press, St. Paul.',
  'McCullagh, P. (1980). Regression models for ordinal data. Journal of the Royal Statistical Society B 42(2), 109–142.',
  'Roberts, D.R., et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. Ecography 40(8), 913–929.',
  'Ruan, C., et al. (2022). Integrating remote sensing and meteorological data to predict wheat stripe rust. Remote Sensing 14(5), 1221. https://doi.org/10.3390/rs14051221',
  'Zhang, J., Pu, R., Yuan, L., Huang, W., Nie, C., Yang, G. (2014). Integrating remotely sensed and meteorological observations to forecast wheat powdery mildew at a regional scale. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing 7(11), 4328–4339. https://doi.org/10.1109/JSTARS.2014.2315875'];
const NOTE_REFS = '\n\nReferences:\n' + REFS.join('\n');
sec('Covariate baseline');
let s;
// ---------------------------------------------------------------- slide 1: purpose and inputs
s = S('Covariate baseline model: purpose and inputs', 'Step 2.5.5',
  'A covariate baseline is a model built WITHOUT any sensor data. It uses only what is known about the plot and the season: days after inoculation, crop age at inoculation, variety, growth stage and weather. Every sensor model must beat it.' + NOTE_REFS);
box(s, 0.45, 1.2, 6.05, 0.5, null, '**Why a model without sensor data?**', C.blue, C.lblue);
BL(s, ['**Calendar effect:** severity rises with days after inoculation and differs with variety, crop age, growth stage and weather; a camera model can look accurate only by learning the calendar (De Wolf and Isard, 2007).',
  '**Weather alone can be strong:** machine learning on weather variables predicted yellow rust and powdery mildew severity of wheat (Bijlwan et al., 2025).',
  '**Sensors add to weather:** combining reflectance with meteorological data raised accuracy from 69% to 78% for wheat powdery mildew (Zhang et al., 2014); remote sensing + meteorological features predicted stripe rust (Ruan et al., 2022).',
  '**Rule:** a sensor set is reported as useful only if it beats the covariate-only model (Kuhn and Johnson, 2013).'], 0.45, 1.8, 6.05, 4.3);
tb(s, [['Covariate (no sensor data)', 'Coding'], ['Days after inoculation (DAI)', 'numeric: flight date − 10 Jan 2027'], ['Inoculation timing (D1–D4)', 'one-hot; or crop age at inoculation (52, 44, 36, 28 days)'],
  ['Variety (PM 26, Pusa Vijay, PM 37)', 'one-hot'], ['Growth stage (Lancashire et al., 1991)', 'BBCH → 1 vegetative, 2 flowering, 3 pod formation'],
  ['Weather, 7 days before each flight', 'mean Tmax, Tmin, RH I, RH II; total rainfall'], ['Favourable days since inoculation (Chattopadhyay et al., 2011)', 'leaf: Tmax 16–24 °C, RH I > 97%, RH II > 40%; staghead: Tmax 20–29 °C, Tmin > 12 °C, RH I > 97%']],
  6.75, 1.2, 6.13, [2.75, 3.38]);
box(s, 6.75, 4.6, 6.13, 1.25, null, ['**Samples:** inoculated, unsprayed plots only – healthy plots are fungicide-protected and share every covariate with their inoculated twins.', '**No look-ahead:** weather windows end the day before each flight.'], C.gold, C.lgold, { align: 'left' });
refline(s, 'De Wolf and Isard (2007); Zhang et al. (2014); Ruan et al. (2022); Bijlwan et al. (2025); Chattopadhyay et al. (2011); Lancashire et al. (1991); Kuhn and Johnson (2013).', 6.35, 0.65);
// ---------------------------------------------------------------- slide 2: model building and comparison design
s = S('Covariate baseline: model building and comparison design', 'Step 2.5.5',
  'Two baselines are fitted on covariates only: an interpretable epidemiological model and the best machine-learning model. The stronger one is the reference. Sensor models and sensor + covariate models are fitted on the same folds and scored with the same metrics.' + NOTE_REFS);
chain(s, [{ h: '1. Covariate table', b: 'one row per subplot-date' }, { h: '2. Coding and scaling', b: 'one-hot, ordinal; z-score with training statistics' }, { h: '3. Two baselines', b: 'B1 statistical; B2 machine learning', c: C.purple, f: C.lpurple },
  { h: '4. Same folds', b: '3 outer LORO folds; inner 3 folds grouped by plot', c: C.gold, f: C.lgold }, { h: '5. Reference', b: 'the stronger of B1 and B2' }], 0.45, 1.2, 12.43, 1.25, 0.28, C.blue, C.lblue);
box(s, 0.45, 2.7, 6.1, 1.6, 'B1 – Interpretable epidemiological model', ['• Task A: logistic regression (healthy vs diseased)', '• Task B: proportional-odds ordinal logistic regression (McCullagh, 1980)', '• Task C: linear model of the score with DAI and DAI² (disease-progress shape; Madden et al., 2007)'], C.purple, 'FFFFFF', { align: 'left', valign: 'top' });
box(s, 6.78, 2.7, 6.1, 1.6, 'B2 – Machine-learning baseline', ['• best model of Activity 2.2 (e.g., random forest; Breiman, 2001)', '• same grid search in the inner folds as the sensor models', '• weather-based random forests predicted wheat rust severity (Bijlwan et al., 2025)'], C.purple, 'FFFFFF', { align: 'left', valign: 'top' });
tb(s, [['Model set', 'Inputs', 'Question answered'], ['M0 – covariate baseline', 'covariates only (no sensor data)', 'how much do time, stage, variety and weather explain?'],
  ['M1 – sensor model', 'each of the 15 sensor sets (fused features)', 'what do the cameras achieve alone?'], ['M2 – sensor + covariates', 'best 3 sensor sets + covariates', 'does known context add to the cameras? (labelled "within-season")']],
  0.45, 4.55, 12.43, [2.8, 4.1, 5.53], { firstCol: true });
refline(s, 'McCullagh (1980); Madden et al. (2007); Breiman (2001); Bijlwan et al. (2025); Roberts et al. (2017); Kuhn and Johnson (2013).', 6.45);
// ---------------------------------------------------------------- slide 3: evaluation and interpretation
s = S('Covariate baseline: gain of the sensors and interpretation', 'Step 2.5.5',
  'The gain of the sensors is the metric of the sensor model minus the metric of the covariate baseline. Because there are only three outer folds, the gain is tested by a block bootstrap of the pooled test predictions that resamples whole plots; AUCs are compared with the DeLong test. The illustration uses the 2025-26 ASD leaf data (inoculated leaves, random forest).' + NOTE_REFS);
box(s, 0.45, 1.2, 6.1, 1.55, 'Gain', ['ΔS (sensor gain) = metric(M1) − metric(M0)', 'ΔC (context gain) = metric(M2) − metric(M1)', 'A: macro-F1, AUC;  B: macro-F1, QWK;  C: R², RMSE'], C.blue, C.lblue);
box(s, 0.45, 2.9, 6.1, 1.9, 'Is the gain real?', ['• block bootstrap of pooled test predictions, resampling plots (2000 times) → 95% CI of Δ (Efron and Tibshirani, 1993)', '• AUC of M1 vs M0: DeLong test (DeLong et al., 1988)', '• real gain: CI excludes 0, Δ > fold SD, same sign in all 3 folds'], C.blue, 'FFFFFF', { align: 'left' });
tb(s, [['Outcome', 'Meaning'], ['M1 > M0 (CI above 0)', 'cameras detect disease beyond the calendar and growth stage'], ['M1 ≈ M0', 'sensor features mainly track time or stage; check results within each stage'],
  ['M2 > M1', 'known context adds information; reported as within-season only'], ['M0 high for detection only', 'epidemic level follows time; sensor value lies in severity grading']], 6.78, 1.2, 6.1, [2.3, 3.8], { firstCol: true });
T(s, '**Illustration – 2025-26 ASD leaf data (inoculated leaves, random forest)**', 0.45, 4.95, 12.43, 0.35, { color: C.g });
tb(s, [['Model set', 'Detection macro-F1', 'Six grades macro-F1', 'Score R²'], ['M0 covariates only', '0.763', '0.298', '0.331'], ['M1 leaf spectra', '0.747', '0.368', '0.405'], ['M2 spectra + covariates', '0.817', '0.414', '0.445']],
  0.45, 5.3, 7.2, [2.4, 1.6, 1.6, 1.6], { firstCol: true });
BL(s, ['**Pre-symptomatic (Step 3.5.3):** healthy vs later-infected cannot be separated by covariates; the baseline is used for the later severity score.', '**Bharatpur (Step 2.7.3):** covariate models re-tested with local weather – first out-of-site test.'], 7.85, 5.0, 5.03, 1.65);
refline(s, 'Efron and Tibshirani (1993); DeLong et al. (1988); Zhang et al. (2014); Chattopadhyay et al. (2011); Kuhn and Johnson (2013).', 6.72, 0.3);
pres.writeFile({ fileName: OUT }).then(async f => { await applyTheme(OUT, THEME); console.log('saved', f); });
