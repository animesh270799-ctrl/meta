// Slides 21-50: Objectives 1-3, outputs, work plan, references
const { pres, F, FS, C, S, sec, T, BL, box, arr, line, chain, tb, circ, refline } = require('./adv_lib.js');
const fs = require('fs');
let s;
// 21 ------------------------------------------------------------------ Obj1 overview
sec('Objective 1');
s = S('Objective 1: Characterisation of white rust (overview)', 'Objective 1', 'Eight activities at two stages. Post-symptomatic stage: 1920 subplot samples per camera with the severity grade and score as target (Activities 1.1–1.7). Pre-symptomatic stage: 576 subplot samples per camera with later-infected vs healthy as target (Activity 1.8). For prediction, the same steps are repeated inside each training fold. Feature selection follows four stages with one method per feature type, as in the DT-EDNet study.');
box(s, 0.45, 1.2, 6.1, 0.85, 'Post-symptomatic stage (Activities 1.1–1.7)', '1920 subplot samples per camera; 10 flights, 12–75 days after inoculation; target = DI class and DI (%)', C.g, C.lt, { fs: 13 });
box(s, 6.78, 1.2, 6.1, 0.85, 'Pre-symptomatic stage (Activity 1.8)', '576 subplot samples per camera; 3 flights, 2–8 days after inoculation; target = later-infected vs healthy', C.red, C.lred, { fs: 13 });
const o1 = [['1.1 Response analysis', 'mean spectra, derivative, correlation'], ['1.2 Optimal wavelengths', 'NDSI/RSI maps → SHAP-CARS'], ['1.3 Index construction', 'best NDSI, RSI; White Rust Index'], ['1.4 Index selection', 'redundancy filter → ReliefF'],
  ['1.5 Texture and TTFI', 'PCA texture → mRMR → TTFI'], ['1.6 Disease-specific sets', 'all cameras; VIF < 10'], ['1.7 Physiological basis', '11 parameters vs features'], ['1.8 Pre-symptomatic stage', 'same steps, binary target']];
o1.slice(0, 4).forEach((o, i) => { const x = 0.45 + i * 3.15; box(s, x, 2.25, 2.9, 0.85, o[0], o[1], C.g, C.lt, { fs: 13 }); if (i < 3) arr(s, x + 2.92, 2.67, x + 3.13, 2.67); });
arr(s, 11.9, 3.12, 11.9, 3.3);
o1.slice(4).forEach((o, i) => { const x = 9.9 - i * 3.15; const red = i === 3, teal = i === 2; box(s, x, 3.32, 2.9, 0.85, o[0], o[1], red ? C.red : (teal ? C.teal : C.g), red ? C.lred : (teal ? C.lteal : C.lt), { fs: 13 }); if (i < 3) arr(s, x - 0.02, 3.74, x - 0.23, 3.74); });
tb(s, [['Selection stage', 'What is done', 'Labels'], ['0 Groups', 'physically meaningful groups (no second derivative)', 'no'], ['1 Redundancy', 'drop near-constant; one per cluster with |r| ≥ 0.95', 'no'],
  ['2 Selection', 'one method per feature type (right)', 'inner folds'], ['3 Across groups', 'pool survivors; VIF < 10', 'no'], ['4 Final set', 'SFFS with each machine-learning model (Objective 2)', 'inner folds']], 0.45, 4.35, 7.6, [1.75, 4.6, 1.25], { fs: 12, firstCol: true });
tb(s, [['Feature type', 'Selection method'], ['Spectral bands (R, FD)', 'SHAP-CARS'], ['Vegetation indices', 'ReliefF (RReliefF for score)'], ['Texture features', 'mRMR'], ['Constructed indices', 'exhaustive search'], ['Thermal, MS bands', 'kept (small groups)']], 8.3, 4.35, 4.58, [2.2, 2.38], { fs: 12, firstCol: true });
refline(s, 'Guyon and Elisseeff (2003); Dormann et al. (2013); Ghamisi et al. (2019); Ma et al. (2026).', 6.62, 0.35);
// 23 ------------------------------------------------------------------ 1.1
s = S('Activity 1.1: Response analysis (Steps 1.1.1–1.1.3)', 'Objective 1', 'Model-free description of how each camera responds to severity, treatment, stage and weather.');
const a11 = [['Step 1.1.1', 'Mean spectra and first-derivative curves by DI class', ['Mean subplot spectra of DI classes 0–9 with ± 1 SD', 'First derivative of the red edge (680–760 nm)', 'Expected: visible rise (chlorophyll loss), red-edge blue shift, NIR fall (leaf damage), SWIR rise (water loss)']],
  ['Step 1.1.2', 'Correlation of each feature with the severity score', ['Pearson r of every feature with the score', 'Correlation curves of reflectance and first derivative against wavelength', 'r reported with sign; p-values not used for selection (subplots of a plot are related)']],
  ['Step 1.1.3', 'Response by variety, timing, growth stage, DAI and weather', ['Features against DAI for each variety and timing', 'Separate curves for vegetative, flowering and pod-formation stages (flowers and pods change reflectance)', 'Inoculated vs healthy plots of the same variety; disease progress with 7-day weather']]];
a11.forEach((a, i) => { const x = 0.45 + i * 4.2; box(s, x, 1.3, 4.0, 1.0, a[0], a[1], C.g, C.lt); BL(s, a[2], x, 2.45, 4.0, 3.6); if (i < 2) arr(s, x + 4.02, 1.8, x + 4.18, 1.8); });
refline(s, 'Mahlein et al. (2013); Guo et al. (2021); Ma et al. (2026); red-edge shift: Horler et al. (1983), Filella and Peñuelas (1994); flowering: Sulik and Long (2016); weather: Chattopadhyay et al. (2011).', 6.1, 0.65);
// 24 ------------------------------------------------------------------ 1.2.1
s = S('Step 1.2.1: Effective ranges from NDSI and RSI maps', 'Objective 1', 'Exhaustive two-band search narrows the spectrum to disease-sensitive regions.');
box(s, 0.45, 1.3, 6.0, 1.3, 'Two-band indices for every band pair (λ1, λ2)', ['NDSI(λ1, λ2) = (Rλ1 − Rλ2) / (Rλ1 + Rλ2)', 'RSI(λ1, λ2) = Rλ1 / Rλ2'], C.g, C.lt);
chain(s, [{ h: 'All pairs', b: '483 bands → 116 403 pairs per index' }, { h: 'R² maps', b: 'R² of each index with severity score' }, { h: 'Effective ranges', b: 'regions in pairs with R² ≥ 0.5 (else top 5%)' }], 0.45, 2.9, 6.0, 1.5, 0.3, C.g, 'FFFFFF');
BL(s, ['**Purpose:** many spectral regions carry no disease information; searching all bands adds noise and computation.', '**Rule:** threshold R² ≥ 0.5 as in Ma et al. (2026); ranges kept at least ≈ 20 nm wide.',
  '**Run on:** the training part only (inner folds for prediction).', '**Outputs:** effective ranges → SHAP pre-screening (Step 1.2.2); best NDSI and RSI pairs → Step 1.3.1.', '**Why:** finds disease-sensitive band combinations without prior assumptions and links directly to index construction.'], 6.75, 1.25, 6.13, 4.6);
refline(s, 'Ma et al. (2026); optimised two-band indices for wheat diseases: Huang et al. (2014).', 6.2);
// 25 ------------------------------------------------------------------ SHAP-CARS
s = S('Steps 1.2.2–1.2.4: Optimal wavelengths by SHAP-CARS', 'Objective 1', 'SHAP removes clearly unimportant bands; CARS with PLS selects a small complementary set; stability over 20 runs.');
chain(s, [{ h: 'Candidates', b: 'R and FD bands in effective ranges + red-edge FD (680–760 nm)' }, { h: 'SHAP pre-screening', b: 'XGBoost (300 trees, depth 4, lr 0.05); keep top 40% by mean |SHAP|' }, { h: 'Standardise', b: 'mean 0, SD 1 (R and FD on one scale)' },
  { h: 'PLS components', b: '1–15 by Monte Carlo CV (50 splits, 80/20 of plots)' }, { h: 'CARS × 20 runs', b: '50 iterations each; min RMSECV subset' }, { h: 'Optimal wavelengths', b: 'selected in ≥ 50% of runs; ≤ 15 bands' }], 0.45, 1.3, 12.43, 1.75, 0.22, C.g, C.lt);
box(s, 0.45, 3.3, 6.1, 2.1, 'CARS iteration (Li et al., 2009)', ['1. Fit PLS on a random 80% of samples', '2. Weight bands by |PLS regression coefficient|', '3. Remove bands by an exponentially decreasing function', '4. Adaptive reweighted sampling of the remaining bands', '5. Record RMSECV; keep the subset with minimum RMSECV'], C.g, 'FFFFFF', { align: 'left', valign: 'top' });
BL(s, ['**SHAP:** contribution of a band averaged over all orders of adding features; exact and fast for trees (Lundberg and Lee, 2017; Lundberg et al., 2020).', '**Why standardise:** PLS coefficients depend on units; R ≈ 0–0.6 vs FD ≈ 0.001–0.01 nm⁻¹.',
  '**Stability rule:** wavelengths selected in ≥ 50% of 20 runs; each labelled R_λ or FD_λ and linked to chlorophyll, red edge, water or structure (Meinshausen and Bühlmann, 2010).'], 6.8, 3.25, 6.08, 2.8);
refline(s, 'Ma et al. (2026); Li et al. (2009); Mehmood et al. (2012); Lundberg and Lee (2017); Nogueira et al. (2018).', 6.2);
// 26 ------------------------------------------------------------------ 1.3
s = S('Activity 1.3: Spectral index construction (Steps 1.3.1–1.3.3)', 'Objective 1', 'Single, interpretable disease indices from the maps and a three-band search.');
box(s, 0.45, 1.3, 4.0, 2.2, 'Step 1.3.1 Best NDSI and RSI', ['Pair with the highest R² from each map', 'Pairs closer than 10 nm are avoided (noise rather than a spectral feature)', '(Ma et al., 2026; Huang et al., 2014)'], C.g, C.lt, { valign: 'top' });
box(s, 4.65, 1.3, 4.0, 2.2, 'Step 1.3.2 White Rust Index (WRI)', ['WRI = NDSI(λ1, λ2) + w·Rλ3', 'w ∈ {−1, −0.5, 0, 0.5, 1}; bands at 6 nm steps; λ1, λ2 ≥ 50 nm apart', 'scored by r with severity and balanced accuracy (inner folds)'], C.purple, C.lpurple, { valign: 'top' });
box(s, 8.85, 1.3, 4.03, 2.2, 'Step 1.3.3 Multispectral two-band indices', ['All 10 normalised differences of the 5 bands', 'Ranked by R² with severity', 'Best compared with the White Rust Index (Liu et al., 2024)'], C.blue, C.lblue, { valign: 'top' });
BL(s, ['**Why a three-band index:** two bands may not capture both the pigment and the structural change caused by white rust; the third band adds independent information.', '**Leakage control:** the WRI search is repeated inside the training part of every fold for prediction.',
  '**Output:** best NDSI, RSI and WRI join the index group (Activity 1.4) and the inputs of Objectives 2 and 3.'], 0.45, 3.75, 12.43, 1.6);
refline(s, 'disease-specific indices: Mahlein et al. (2013); three-band yellow rust index: Zheng et al. (2018); ground-to-UAV index: Liu et al. (2026).', 6.2);
// 27 ------------------------------------------------------------------ 1.4 ReliefF
s = S('Activity 1.4: Vegetation index selection with ReliefF', 'Objective 1', 'Index group → redundancy filter → ReliefF / RReliefF.');
chain(s, [{ h: '1.4.1 Index group', b: '≈ 48 published indices + red-edge parameters + NDSI, RSI, WRI (≈ 55)' }, { h: '1.4.2 Redundancy filter', b: 'remove near-constant; |r| ≥ 0.95 clusters → keep the one most correlated with severity' }, { h: '1.4.3 ReliefF / RReliefF', b: 'k = 10 neighbours; same-plot neighbours excluded; top 5 (3–8 checked)' }], 0.45, 1.3, 12.43, 1.6, 0.35, C.g, C.lt);
box(s, 0.45, 3.15, 6.4, 1.6, 'ReliefF weight update (Robnik-Šikonja and Kononenko, 2003)', ['W_j ← W_j − diff(j, x, H)/m + Σ_(c≠class(x)) [P(c) / (1 − P(class(x)))] · diff(j, x, M_c)/m'], C.g, 'FFFFFF');
BL(s, ['**H:** nearest hit (same class); **M_c:** nearest miss of class c; **diff:** absolute difference of feature j.', 'A feature gains weight when it differs between classes and loses weight when it differs within a class.', '**RReliefF:** regression version for the severity score.'], 7.05, 3.1, 5.83, 1.8);
BL(s, ['**Why ReliefF:** handles several overlapping, ordered classes and feature interactions; fast; used for vegetation indices in the DT-EDNet study and for disease indices in hyperspectral studies.', '**Output:** 5–8 selected indices (VI) → VIF (Step 1.6.2) and the "VI" network configuration (Step 2.1.5).'], 0.45, 4.95, 12.43, 1.2);
refline(s, 'Kira and Rendell (1992); Urbanowicz et al. (2018); Mahlein et al. (2013); Huang et al. (2014); Dormann et al. (2013); Ma et al. (2026).', 6.2);
// 28 ------------------------------------------------------------------ 1.5 texture
s = S('Activity 1.5: Texture selection and TTFI', 'Objective 1', 'Principal-component texture → redundancy filter → mRMR → TTFI.');
chain(s, [{ h: '1.5.1 PCA texture', b: 'first 3 components (> 95% variance) × 8 GLCM measures = 24' }, { h: '1.5.2 Redundancy filter', b: '|r| ≥ 0.95 (e.g., contrast vs dissimilarity)' }, { h: '1.5.3 mRMR', b: 'mutual information; top 6 texture features (TF1–TF6)' }, { h: '1.5.4 TTFI', b: '120 ordered triplets × 3 formulas = 360 candidates' }], 0.45, 1.3, 12.43, 1.55, 0.3, C.g, C.lt);
box(s, 0.45, 3.1, 6.1, 1.25, 'mRMR criterion (Peng et al., 2005)', ['next feature = arg max_j [ I(f_j; y) − (1/|S|) Σ_(s∈S) I(f_j; f_s) ]'], C.g, 'FFFFFF');
box(s, 6.78, 3.1, 6.1, 1.25, 'Tri-band Texture Fusion Indices (Ma et al., 2026)', ['TTFI1 = (TF1 + TF2) / TF3;  TTFI2 = TF1 × TF2 / TF3', 'TTFI3 = TF1 × (TF1 + TF2) / (TF2 + TF3)'], C.purple, 'FFFFFF');
BL(s, ['**Why texture:** white pustules and chlorotic patches make the canopy heterogeneous – a spatial pattern that spectra do not record (Guo et al., 2021).', '**mRMR:** relevance to severity minus mean redundancy with features already chosen; k-NN mutual-information estimator (k = 3).',
  '**TTFI:** best candidate by |r| with severity; in rice blast, TTFI3 was more strongly related to disease than any single texture feature (Ma et al., 2026).'], 0.45, 4.55, 12.43, 1.6);
refline(s, 'Haralick et al. (1973); Hall-Beyer (2017); Jolliffe and Cadima (2016); Peng et al. (2005); Yuan et al. (2025); Ma et al. (2026).', 6.2);
// 29 ------------------------------------------------------------------ 1.6
s = S('Activity 1.6: Disease-specific feature set of each camera', 'Objective 1', 'Same rules for all cameras; variance inflation factor across groups; complementarity.');
tb(s, [['Camera', 'Selection (Step 1.6.1)'], ['Hyperspectral', 'optimal wavelengths (1.2) + selected indices (1.4) + selected texture and TTFI (1.5)'], ['Multispectral', '5 bands kept; indices and normalised differences: filter → ReliefF (top 5); texture: filter → mRMR (top 4)'],
  ['Red–green–blue', 'colour indices and means: filter → ReliefF (top 4); texture: filter → mRMR (top 4)'], ['Thermal', 'all thermal features kept after the redundancy filter (≈ 10)']], 0.45, 1.25, 7.4, [1.8, 5.6], { firstCol: true });
box(s, 8.1, 1.25, 4.78, 1.55, 'Step 1.6.2 Variance inflation factor', ['VIF_j = 1 / (1 − R_j²)', 'remove the highest VIF until all < 10'], C.blue, C.lblue);
BL(s, ['**Output:** disease-specific feature set of each camera (≈ 10–25 features) → Objective 2.', '**Step 1.6.3:** selected features against DAI by variety and timing; correlation matrix between cameras; response within each growth stage (not only a flowering effect).'], 8.1, 2.95, 4.78, 3.1);
BL(s, ['**Why VIF:** survivors of different groups can still be collinear (e.g., a red-edge wavelength and a red-edge index); collinearity makes models and importance values unstable (Dormann et al., 2013; O\'Brien, 2007).'], 0.45, 4.35, 7.4, 1.4);
refline(s, 'Ma et al. (2026); Feng et al. (2022); Liu et al. (2024); Tian et al. (2021); Mustafa et al. (2023); Mahlein et al. (2019); Maimaitijiang et al. (2020); Sulik and Long (2016).', 6.15, 0.65);
// 30 ------------------------------------------------------------------ 1.7 stats
s = S('Activity 1.7: Physiological basis of camera responses', 'Objective 1', 'Parameters are not model inputs; the plot (designated subplot) is the experimental unit. Steps 1.7.1–1.7.6 and the expected links between parameters and camera features.');
BL(s, ['**1.7.1 Preparation:** average technical replicates; per g fresh weight; join by date, plot, subplot.', '**1.7.2 Effect of white rust:** 12 inoculated–healthy pairs per date; paired t-test or Wilcoxon; mean difference, 95% CI, effect size.',
  '**1.7.3 Variety and timing:** two-way ANOVA (RBD), LSD at 5%.', '**1.7.4 Growth stages:** disease effect by stage; ANOVA or Kruskal–Wallis; Tukey.',
  '**1.7.5 Severity:** Pearson r with plot DI and subplot DI, per date.', '**1.7.6 Camera features:** within-date and within-stage correlations; Benjamini–Hochberg FDR 5%.'], 0.45, 1.2, 5.2, 5.2, { lead: C.teal, ps: 5 });
tb(s, [['Parameter', 'Expected camera features', 'Why'],
  ['Chlorophyll a, b', 'REP, CIrededge, MTCI, NDRE, PSSR, WRI', 'chlorophyll sets the red edge'], ['Carotenoids', 'PRI, PSRI', 'carotenoid/chlorophyll ratio changes'], ['Anthocyanin', 'ARI', 'absorbs green light near 550 nm'],
  ['Relative water content', 'NDWI, NDII, WI; canopy − air temperature', 'water absorption; water loss warms canopy'], ['Stomatal conductance, transpiration', 'CTD, NRCT, CWSI', 'transpiration cools the leaves'],
  ['Net photosynthesis', 'PRI, chlorophyll indices', 'PRI follows xanthophyll changes'], ['Membrane stability index', 'NIR plateau, texture', 'tissue damage around pustules'], ['Leaf area index', 'NDVI, OSAVI, MSR, texture', 'canopy size controls NIR scattering']],
  5.85, 1.2, 7.03, [2.05, 2.6, 2.38], { fs: 12, firstCol: true, head: C.teal });
refline(s, 'Gomez and Gomez (1984); Sullivan and Feinn (2012); Benjamini and Hochberg (1995); Gitelson et al. (2003); Gamon et al. (1992); Gao (1996); Jones et al. (2009); Calderón et al. (2013); Haboudane et al. (2004).', 6.3, 0.65);
require('./adv_pre.js')();
// 32 ------------------------------------------------------------------ Obj2 overview
sec('Objective 2');
s = S('Objective 2: Detection and severity discrimination (overview)', 'Objective 2', 'Seven activities on the 1920 post-symptomatic samples; every model for every sensor set and task on the same folds.');
const o2 = [['2.1 Tasks and inputs', 'three tasks; fold-wise selection; 15 sensor sets; SFFS'], ['2.2 Machine learning', 'SVM/SVR, RF, XGBoost, k-NN, PLS-DA/PLSR'], ['2.3 Deep learning', 'DNN-F1, DNN-F2; DT-EDNet, EfficientNet, ResNet18, ConvNeXt V2'], ['2.4 Evaluation', 'OA, kappa, weighted kappa, macro-F1, AUC; R², RMSE, RPD'],
  ['2.5 Comparison', 'ranking; fusion gain; ablation; SHAP; covariate baseline'], ['2.6 Robustness, maps', 'by treatment; LOVO/LOTO; severity maps'], ['2.7 Independent testing', 'frozen models at Bharatpur; farm maps']];
o2.slice(0, 4).forEach((o, i) => { const x = 0.45 + i * 3.15; box(s, x, 1.3, 2.9, 1.3, o[0], o[1], C.purple, C.lpurple); if (i < 3) arr(s, x + 2.92, 1.95, x + 3.13, 1.95); });
arr(s, 11.9, 2.62, 11.9, 2.93);
o2.slice(4).forEach((o, i) => { const x = 9.9 - i * 3.15; box(s, x, 2.95, 2.9, 1.3, o[0], o[1], i === 2 ? C.gold : C.purple, i === 2 ? C.lgold : C.lpurple); if (i < 2) arr(s, x - 0.02, 3.6, x - 0.23, 3.6); });
BL(s, ['**Three tasks:** A – detection (DI = 0 vs DI > 0); B – severity classes from the disease index (0, 1, 3, 5, 7, 9); C – severity score = disease index DI (%) (regression).', '**Two comparisons:** (i) 15 sensor sets × all model families; (ii) the DT-EDNet design of Ma et al. (2026) on hyperspectral feature groups, with plot-grouped validation.',
  '**Fusion:** thermal, multispectral and red–green–blue features added to the hyperspectral features at feature level for all models, including DT-EDNet and the comparison networks.'], 0.45, 4.5, 12.43, 1.9);
// 33 ------------------------------------------------------------------ 2.1 sensor sets
s = S('Activity 2.1: Tasks, selection and fusion of 15 sensor sets', 'Objective 2', 'Selection repeated in every fold; camera feature sets concatenated for combinations.');
const cams = [['HS', C.g], ['MS', C.blue], ['RGB', C.gold], ['TIR', C.red]];
const sets = [['S1', [0]], ['S2', [1]], ['S3', [2]], ['S4', [3]], ['S5', [0, 1]], ['S6', [0, 2]], ['S7', [0, 3]], ['S8', [1, 2]], ['S9', [1, 3]], ['S10', [2, 3]], ['S11', [0, 1, 2]], ['S12', [0, 1, 3]], ['S13', [0, 2, 3]], ['S14', [1, 2, 3]], ['S15', [0, 1, 2, 3]]];
T(s, '**15 sensor sets: 4 single cameras, 6 pairs, 4 triples, all four**', 0.45, 1.15, 7.0, 0.35);
sets.forEach((st_, i) => { const col = i % 5, row = Math.floor(i / 5), x = 0.45 + col * 1.42, y = 1.6 + row * 1.25; s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 1.32, h: 1.1, fill: { color: 'FFFFFF' }, line: { color: '9AA79C', width: 1 }, rectRadius: 0.05 });
  T(s, '**' + st_[0] + '**', x, y + 0.02, 1.32, 0.3, { align: 'center' }); st_[1].forEach((c, j) => { const cx = x + 0.06 + (j % 2) * 0.62, cy = y + 0.38 + Math.floor(j / 2) * 0.34; s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: cx, y: cy, w: 0.58, h: 0.3, fill: { color: cams[c][1] }, line: { color: cams[c][1] }, rectRadius: 0.04 }); T(s, cams[c][0], cx, cy, 0.58, 0.3, { align: 'center', valign: 'middle', color: 'FFFFFF', bold: true, fontSize: FS, margin: 0 }); }); });
BL(s, ['**Step 2.1.1 Tasks:** A detection (DI = 0 vs > 0); B six DI classes (merged if < 5%); C DI (%); class weights and macro metrics.', '**Step 2.1.2 Fold-wise selection:** Activities 1.2–1.6 repeated on the training part of every outer fold and task; selected features stored (stability).',
  '**Step 2.1.3 Fusion:** single camera → its own set; combination → concatenate camera sets, apply VIF < 10 again across cameras, standardise with training statistics.', '**Same fused input** for machine learning, DNN-F1, DNN-F2 and the pseudo-image networks.'], 7.7, 1.15, 5.18, 4.9);
refline(s, 'Feng et al. (2022); Liu et al. (2024); Ghamisi et al. (2019); Maimaitijiang et al. (2020); Ambroise and McLachlan (2002); Varma and Simon (2006).', 6.2);
// 34 ------------------------------------------------------------------ 2.1.4-2.1.5 + model matrix
s = S('Steps 2.1.4–2.1.5: SFFS, configurations, model matrix', 'Objective 2', 'Final compact set for machine learning; six hyperspectral configurations for the network comparison.');
box(s, 0.45, 1.25, 6.1, 1.65, 'Step 2.1.4 Sequential floating forward selection (SFFS)', ['1. Add the feature that most improves the inner score', '2. After each addition, try removing earlier features ("floating")', '3. Stop at 15 features; keep the smallest subset within 1% of best', 'criterion: macro-F1 (classes) or RMSE (score) (Pudil et al., 1994)'], C.purple, 'FFFFFF', { align: 'left', valign: 'top' });
box(s, 6.78, 1.25, 6.1, 1.65, 'Step 2.1.5 Hyperspectral configurations (Ma et al., 2026)', ['OW: optimal wavelengths;  VI: selected indices;  TF: selected texture', 'OW + VI;  OW + TTFI;  OW + VI + TTFI', 'four pseudo-image networks + best machine-learning model'], C.purple, 'FFFFFF', { align: 'left', valign: 'top' });
tb(s, [['Model family', 'Models', 'Sensor sets', 'Tasks A, B / C'], ['Machine learning', 'SVM/SVR, RF, XGBoost, k-NN, PLS-DA/PLSR', 'all 15', 'yes / yes'], ['Feature-fusion networks', 'DNN-F1; DNN-F2 (one branch per camera)', 'all 15; S5–S15 for DNN-F2', 'yes / yes'],
  ['Pseudo-image networks', 'DT-EDNet, EfficientNet-B0, ResNet18, ConvNeXt V2-Atto', 'all 15', 'yes / yes (linear output)'], ['Covariate models', 'best machine-learning model', 'covariates only; best sets + covariates', 'yes / yes']], 0.45, 3.2, 12.43, [2.6, 4.6, 3.3, 1.93], { firstCol: true });
// 35 ------------------------------------------------------------------ 2.2 ML
s = S('Activity 2.2: Machine-learning models and tuning grids', 'Objective 2', 'Kernel, bagging, boosting, instance-based and latent-variable families; grid search in inner folds.');
tb(s, [['Model', 'Principle', 'Hyper-parameters tuned (inner CV)', 'Reference'],
  ['SVM / SVR', 'maximum-margin boundary (ε-tube for regression); RBF kernel; class weights', 'C ∈ {0.1, 1, 10, 100}; γ ∈ {0.001, 0.01, 0.1, scale}; ε ∈ {0.1, 0.5}', 'Cortes and Vapnik (1995); Mountrakis et al. (2011)'],
  ['Random forest', 'many decorrelated trees on bootstrap samples; vote or mean', '500 trees; features per split ∈ {√p, 0.3p}; min. leaf ∈ {1, 3, 5}', 'Breiman (2001)'],
  ['XGBoost', 'trees added sequentially to correct errors; regularised', 'trees ∈ {200, 500}; depth ∈ {3, 5}; learning rate ∈ {0.05, 0.1}; subsample 0.8', 'Chen and Guestrin (2016)'],
  ['k-NN', 'class or mean of the k most similar training samples', 'k ∈ {3, 5, 7, 9, 11}; uniform or distance weights', 'Cover and Hart (1967)'],
  ['PLS-DA / PLSR', 'latent variables with maximum covariance with the target', 'latent variables 1–15', 'Wold et al. (2001); Barker and Rayens (2003)']], 0.45, 1.25, 12.43, [1.7, 4.0, 4.1, 2.63], { firstCol: true });
BL(s, ['**Input:** SFFS subset of the fused set (standardised); class weights for classifiers; the same three outer folds for all models.', '**Choice:** hyper-parameters with the best mean inner score; model retrained on the whole training part; one prediction of the test replication.'], 0.45, 4.35, 12.43, 1.0);
refline(s, 'Kuhn and Johnson (2013); Cawley and Talbot (2010); disease applications: Tian et al. (2021); Mustafa et al. (2023); Yuan et al. (2025).', 6.2);
// 36 ------------------------------------------------------------------ DNN-F1/F2
s = S('Steps 2.3.1–2.3.2: Feature-fusion networks DNN-F1, DNN-F2', 'Objective 2', 'Input-level fusion vs intermediate fusion with camera attention.');
T(s, '**DNN-F1 (input-level fusion)**', 0.45, 1.15, 6.0, 0.35, { color: C.purple });
chain(s, [{ h: 'Fused vector', b: 'all cameras' }, { h: 'Dense 64', b: 'BN, ReLU, dropout' }, { h: 'Dense 32', b: 'BN, ReLU, dropout' }, { h: 'Output', b: 'softmax / linear' }], 0.45, 1.6, 6.0, 1.2, 0.22, C.purple, C.lpurple);
T(s, '**DNN-F2 (intermediate fusion, sets with ≥ 2 cameras)**', 6.78, 1.15, 6.1, 0.35, { color: C.purple });
['HS', 'MS', 'RGB', 'TIR'].forEach((c, i) => { const y = 1.6 + i * 0.6; box(s, 6.78, y, 1.3, 0.5, null, c, C.purple, C.lpurple); arr(s, 8.1, y + 0.25, 8.4, y + 0.25); box(s, 8.42, y, 1.55, 0.5, null, 'branch 16–32', C.purple, 'FFFFFF'); arr(s, 9.99, y + 0.25, 10.3, 2.8); });
box(s, 10.32, 2.25, 1.15, 1.1, null, 'SE camera weights', C.red, C.lred); arr(s, 11.49, 2.8, 11.7, 2.8); box(s, 11.72, 2.25, 1.16, 1.1, null, 'Dense 32 → output', C.purple, C.lpurple);
BL(s, ['**Training:** Adam (learning rate 0.001, weight decay 10⁻⁴), batch 32, up to 500 epochs, early stopping (patience 30) on inner validation plots; five seeds averaged.', '**Tuning:** first-layer units ∈ {32, 64}; dropout ∈ {0.2, 0.3, 0.4} in the inner folds; loss: class-weighted cross-entropy or mean squared error.',
  '**Why:** compact enough for ≈ 1000 samples; intermediate fusion was better than input fusion for multi-sensor UAV data, and DNN-F2 shows which camera the model relies on (Maimaitijiang et al., 2020).'], 0.45, 4.25, 12.43, 1.8);
refline(s, 'Maimaitijiang et al. (2020); Kingma and Ba (2015); Srivastava et al. (2014); Ioffe and Szegedy (2015); Hu et al. (2018).', 6.2);
// 37 ------------------------------------------------------------------ pseudo-image
s = S('Steps 2.3.3–2.3.4: Pseudo-image and DT-EDNet architecture', 'Objective 2', 'The feature vector is reshaped into a small one-channel image; DT-EDNet = convolution embedding, squeeze-and-excitation, kernel transformer block with CBAM and four token transformer blocks.');
chain(s, [{ h: 'Pseudo-image', b: 'k × k, 1 channel' }, { h: 'Embedding', b: '3 × 3 conv, stride 1, 128 ch.' }, { h: 'SE block', b: 'channel re-weighting', c: C.red, f: C.lred }, { h: 'Tokens', b: 'k² + class token + position' },
  { h: 'Kernel TB', b: 'conv + CBAM attention', c: C.blue, f: C.lblue }, { h: '4 Token TBs', b: 'LN → MHSA (4 heads) → FFN', c: C.blue, f: C.lblue }, { h: 'Head', b: 'LN(class token) → linear' }], 0.45, 1.2, 12.43, 1.3, 0.2, C.purple, C.lpurple, { fs: 13 });
T(s, 'Dual Transformer Group (DTG)', 7.1, 2.52, 3.6, 0.32, { align: 'center', italic: true, color: C.blue });
T(s, '**Pseudo-image, e.g. S7 (HS + TIR), 6 × 6**', 0.45, 2.85, 4.2, 0.32, { fontSize: 13 });
for (let r = 0; r < 6; r++) for (let c = 0; c < 6; c++) { const idx = r * 6 + c; let col = 'FFFFFF', lc = 'B0B0B0'; if (r < 3 && idx < 16) { col = C.lt; lc = C.g; } else if (r === 3) { col = C.lred; lc = C.red; } s.addShape(pres.shapes.RECTANGLE, { x: 0.7 + c * 0.42, y: 3.25 + r * 0.42, w: 0.4, h: 0.4, fill: { color: col }, line: { color: lc, width: 1 } }); }
T(s, 'green = 16 HS features; red = 6 thermal features; white = zero padding', 0.45, 5.85, 3.5, 0.6, { fontSize: 12 });
BL(s, ['**Ordering:** by camera, then by group and wavelength, so neighbouring pixels hold related features.', '**Grid:** k = ⌈√p⌉ (≥ 3); padding = 0 (training mean after standardisation).', '**Extension:** Ma et al. (2026) used hyperspectral features only; thermal, MS and RGB features are added here and tested against S1 and DNN-F2.'], 3.85, 2.85, 4.1, 3.6, { box: { fontSize: 13 } });
box(s, 8.15, 2.95, 4.73, 1.1, 'Self-attention (Vaswani et al., 2017)', ['softmax(Q Kᵀ / √d) V; d = 128 / 4 heads = 32'], C.blue, 'FFFFFF', { fs: 13 });
BL(s, ['**Why:** relates local neighbours (convolution, CBAM) and distant features (attention).', '**Settings:** embedding 128; dropout 0.03; trained from scratch; output softmax (A, B) or linear (C).', '**Published:** best for rice blast (OA 95.25%, OW + VI + TTFI) (Ma et al., 2026).'], 8.15, 4.15, 4.73, 2.3, { box: { fontSize: 13 } });
refline(s, 'Ma et al. (2026); Sharma et al. (2019); Hu et al. (2018); Woo et al. (2018); Vaswani et al. (2017); Dosovitskiy et al. (2021).', 6.55, 0.35);
// 39 ------------------------------------------------------------------ comparison networks + protocol
s = S('Steps 2.3.5–2.3.8: Comparison networks and training', 'Objective 2', 'Same comparison set and training settings as Ma et al. (2026), adapted to small pseudo-images.');
tb(s, [['Network', 'Main design', 'Change for small pseudo-images', 'Reference'], ['EfficientNet-B0', 'mobile inverted bottleneck blocks; depthwise convolution; squeeze-and-excitation', '3 × 3 stem, stride 1, one input channel', 'Tan and Le (2019)'],
  ['ResNet18', 'four stages of two basic residual blocks with identity shortcuts', '3 × 3 stem, stride 1, no max-pooling', 'He et al. (2016)'], ['ConvNeXt V2-Atto', '7 × 7 depthwise convolution, layer normalisation, global response normalisation (≈ 3.7 M parameters)', 'stride-1 stem', 'Woo et al. (2023)']], 0.45, 1.25, 12.43, [2.0, 5.1, 3.0, 2.33], { firstCol: true });
tb(s, [['Training setting (all four networks)', 'Value'], ['Optimiser; learning rate schedule', 'AdamW, 6 × 10⁻⁴, weight decay 10⁻⁵; cosine annealing to 10⁻⁶ over 300 epochs; batch 32'], ['Loss', 'cross-entropy, label smoothing 0.01, class weights (classes); mean squared error (score)'],
  ['Regularisation and stopping', 'gradient clipping (max. norm 1.2); early stopping, patience 60, min. improvement 5 × 10⁻⁵, on inner validation plots'], ['Tuning', 'learning rate ∈ {3, 6, 10} × 10⁻⁴ and dropout ∈ {0.03, 0.1, 0.3}, tuned once (fold 1, S15, Task B), then fixed'], ['Seeds', 'five random seeds; mean ± SD reported']], 0.45, 3.5, 12.43, [3.6, 8.83], { firstCol: true });
refline(s, 'Ma et al. (2026); Loshchilov and Hutter (2017, 2019); Szegedy et al. (2016); Müller et al. (2019); Pascanu et al. (2013).', 6.35);
// 40 ------------------------------------------------------------------ 2.4 metrics
s = S('Activities 2.4–2.5: Evaluation, comparison and interpretation', 'Objective 2', 'Metrics suited to unequal, ordered classes and to the regression of the disease index; then the comparisons that show which sensor set, model, camera and module contribute, and whether the cameras add beyond known factors.');
box(s, 0.45, 1.2, 5.95, 2.05, 'Classification (Tasks A and B)', ['OA = correct / N;  F1 = 2 × precision × recall / (precision + recall)', 'precision = TP / (TP + FP);  recall = TP / (TP + FN)', 'κ = (pₒ − pₑ) / (1 − pₑ);  κw = 1 − Σ wᵢⱼ Oᵢⱼ / Σ wᵢⱼ Eᵢⱼ, wᵢⱼ = (i − j)² / (k − 1)²'], C.purple, 'FFFFFF', { fs: 13 });
box(s, 0.45, 3.35, 5.95, 1.05, 'Regression (Task C: DI, %)', ['R² = 1 − Σ(y − ŷ)² / Σ(y − ȳ)²;  RMSE = √[(1/n) Σ(y − ŷ)²];  RPD = SD_y / RMSE'], C.purple, 'FFFFFF', { fs: 13 });
BL(s, ['**A:** OA, sensitivity, specificity, F1, AUC.  **B:** OA, κ, quadratic-weighted κ, macro recall and macro-F1, per-class F1, confusion matrix, share within one class.  **C:** R², RMSE, RPD.',
  '**Reporting:** pooled predictions of the three test replications and per fold; mean ± SD over folds and seeds; all metrics of Ma et al. (2026).'], 0.45, 4.5, 5.95, 1.95, { box: { fontSize: 13 }, ps: 3 });
const a25 = [['2.5.1 Ranking', 'rank 15 sets by AUC (A), macro-F1 (B), RMSE (C); a difference is real only if larger than the fold SD and seen in all folds'], ['2.5.2 Fusion gain', 'combination minus best single camera; drop-one-camera from S15; DNN-F2 camera weights'],
  ['2.5.3 Networks, ablation', 'four networks + best ML on six configurations; DT-EDNet without SE, without DTG, without both'], ['2.5.4 SHAP, stability', 'mean |SHAP| per feature and camera; links to Activity 1.7; features kept if selected in ≥ 2 of 3 folds'],
  ['2.5.5 Covariate baseline', 'covariate-only models (B1, B2) vs sensor models vs sensor + covariates (next two slides)']];
a25.forEach((a, i) => { const y = 1.2 + i * 1.05; box(s, 6.65, y, 1.95, 0.92, null, '**' + a[0] + '**', C.purple, C.lpurple, { fs: 13 }); box(s, 8.7, y, 4.18, 0.92, null, a[1], C.purple, 'FFFFFF', { align: 'left', fs: 13 }); });
refline(s, 'Cohen (1960, 1968); Sokolova and Lapalme (2009); Fawcett (2006); Feng et al. (2022); Maimaitijiang et al. (2020); Lundberg and Lee (2017); Kuhn and Johnson (2013).', 6.5, 0.5);
require('./adv_cov2.js')();
// 42 ------------------------------------------------------------------ 2.6 + 2.7
s = S('Activities 2.6–2.7: Robustness, maps and independent testing', 'Objective 2', 'Transfer tests and maps; frozen final models applied once to independent Bharatpur data (independent testing, not validation).');
BL(s, ['**2.6.1 By treatment:** metrics for each variety, inoculation timing and date.', '**2.6.2 Transfer:** leave-one-variety-out (train on two varieties, test the third) and leave-one-timing-out (train on three timings, test the fourth) (Roberts et al., 2017).', '**2.6.3 Maps:** detection, class and score of every subplot and date with the best model of each task.'], 0.45, 1.2, 5.9, 3.1);
chain(s, [{ h: '2.7.1 Freeze', b: 'selection + tuning on all IARI data; best models stored' }, { h: '2.7.2 Same processing', b: 'Activities B, D unchanged; IARI scaling constants' }], 6.6, 1.3, 6.28, 1.45, 0.3, C.gold, C.lgold);
chain(s, [{ h: '2.7.3 Apply once', b: 'no retraining; same metrics; farms and fields separately' }, { h: '2.7.4 Farm maps', b: 'quadrat-sized cells; scored quadrats overlaid' }], 6.6, 3.0, 6.28, 1.45, 0.3, C.gold, C.lgold);
arr(s, 12.0, 2.77, 12.0, 2.98);
tb(s, [['Item', 'Validation (internal, IARI)', 'Independent testing (Bharatpur)'], ['Data', 'IARI field, 48 plots, 13 dates', 'Bharatpur research farms and farmers\' fields'], ['Infection', 'artificial (30 Dec 2026)', 'natural epidemic'], ['Design', 'leave-one-replication-out, nested', 'frozen models applied once']], 0.45, 4.6, 12.43, [2.4, 4.8, 5.23]);
// 43 ------------------------------------------------------------------ Obj3 overview
sec('Objective 3');
s = S('Objective 3: Pre-symptomatic prediction (overview)', 'Objective 3', 'Uses the 576 pre-symptomatic samples per camera; machine learning and feature-fusion networks only.');
chain(s, [{ h: '3.1 Samples and labels', b: 'labels from later status; physiology on 7 Jan' }, { h: '3.2 Normalisation', b: 'healthy plots of same date and variety' }, { h: '3.3 Selection', b: 'one method per type with pre-symptomatic labels' },
  { h: '3.4 Models', b: 'ML + DNN-F1, DNN-F2 for 15 sets' }, { h: '3.5 Evaluation', b: 'AUC; earliest detection day; risk maps' }], 0.45, 1.3, 12.43, 1.5, 0.25, C.red, C.lred);
T(s, '**How pre-symptomatic samples are labelled**', 0.45, 3.0, 8, 0.35);
line(s, 0.8, 4.25, 12.6, 4.25, '555555', 2);
[['1 Jan (2 d)', 1.6], ['4 Jan (5 d)', 3.2], ['7 Jan (8 d)', 4.8]].forEach(f => { s.addShape(pres.shapes.OVAL, { x: f[1], y: 4.13, w: 0.24, h: 0.24, fill: { color: C.blue }, line: { color: C.blue } }); T(s, f[0], f[1] - 0.6, 3.65, 1.45, 0.4, { align: 'center', color: C.blue }); });
s.addShape(pres.shapes.OVAL, { x: 7.2, y: 4.13, w: 0.24, h: 0.24, fill: { color: C.purple }, line: { color: C.purple } }); T(s, '11 Jan → 15 Mar: symptoms scored', 6.2, 3.65, 3.6, 0.4, { align: 'center', color: C.purple });
arr(s, 7.2, 4.55, 3.4, 4.55, C.red, 2); T(s, 'label taken back from the later status of the same subplot', 7.45, 4.38, 5.4, 0.35, { color: C.red, italic: true });
BL(s, ['**Healthy** = subplots of the 12 healthy plots; **infected** = inoculated subplots that show pustules later; inoculated subplots that never show symptoms are excluded.', '**Regression target:** score of the same subplot on the first post-symptomatic date. Pseudo-image networks are not used (≈ 384 training samples per fold).'], 0.45, 5.1, 12.43, 1.1);
refline(s, 'Zhu et al. (2017); Tian et al. (2021); Mahlein et al. (2019); Yu et al. (2021).', 6.3);
// 44 ------------------------------------------------------------------ 3.1-3.4
s = S('Activities 3.1–3.4: Labels, normalisation, selection, models', 'Objective 3', 'Early signals are small; healthy-plot normalisation and stricter limits are needed.');
const a3 = [['3.1.2 Physiology before symptoms (7 Jan)', 'paired comparison of 12 inoculated–healthy pairs for every parameter; correlation of pre-symptomatic parameters with plot PDI on 18 Jan; effect sizes and 95% CI'],
  ['3.2.1 Healthy-plot normalisation', 'z_h = (x − mean_healthy) / SD_healthy for every feature; healthy plots of the same date and variety in the training part; same reference for the test samples'],
  ['3.3.1 Pre-symptomatic selection', 'SHAP-CARS (bands), ReliefF/RReliefF (indices), mRMR (texture), TTFI search, redundancy filter, VIF; SFFS limited to 10 features'],
  ['3.4.1 Models for 15 sensor sets', 'SVM, RF, XGBoost, k-NN, PLS-DA/PLSR; DNN-F1 and DNN-F2 with smaller layers (32, 16 units) and dropout 0.4; same folds as Objective 2']];
a3.forEach((a, i) => { const col = i % 2, row = Math.floor(i / 2), x = 0.45 + col * 6.3, y = 1.25 + row * 2.3; box(s, x, y, 6.13, 2.05, a[0], a[1], C.red, row ? 'FFFFFF' : C.lred); });
refline(s, 'Zarco-Tejada et al. (2018); Calderón et al. (2013); Oerke et al. (2006); Poblete et al. (2023); Terentev et al. (2023); Zhu et al. (2017); Srivastava et al. (2014).', 6.0, 0.65);
// 45 ------------------------------------------------------------------ 3.5
s = S('Activity 3.5: Earliest detection day and risk maps', 'Objective 3', 'How early, with which sensor set and with what reliability can white rust be predicted?');
chain(s, [{ h: '3.5.1 Metrics', b: 'sensitivity, specificity, balanced accuracy, AUC; R², RMSE of later score' }, { h: 'Earliest detection day', b: 'first date with balanced accuracy ≥ 0.70 (0.65, 0.75 checked); per variety and timing' },
  { h: '3.5.2 Risk maps', b: 'predicted infection probability of every subplot; compared with later severity' }, { h: '3.5.3 Covariate baseline', b: 'DAI, variety, timing, stage, weather only vs sensor models' }, { h: '3.5.4 Independent testing', b: 'Bharatpur quadrats flown before symptoms, labelled later; protected healthy strip' }], 0.45, 1.3, 12.43, 2.1, 0.22, C.red, C.lred);
box(s, 0.45, 3.7, 6.1, 1.5, 'Receiver operating characteristic (Fawcett, 2006)', ['AUC = probability that an infected subplot scores higher than a healthy one; independent of class balance and threshold'], C.red, 'FFFFFF');
BL(s, ['**Why a covariate baseline:** before symptoms, infection depends strongly on weather after inoculation and on variety; the cameras must detect more than these factors (Zhang et al., 2014).', '**Where data do not allow** an early Bharatpur flight or a healthy reference, the pre-symptomatic models are evaluated with the internal validation only, and this is stated.'], 6.78, 3.65, 6.1, 2.4);
refline(s, 'Fawcett (2006); Mahlein et al. (2019); Zarco-Tejada et al. (2018); Chattopadhyay et al. (2011); Zhu et al. (2017); Ma et al. (2026).', 6.2);
// 46 ------------------------------------------------------------------ outputs
sec('Conclusion');
s = S('Expected outcomes, outputs and six-month work plan', 'Outputs', 'Expected outcome of each objective (bold), the outputs that support it, the month-wise plan of the analysis and the software used.');
box(s, 0.45, 1.2, 4.0, 2.55, 'Objective 1', ['**Outcome:** sensitive spectral ranges, signatures and indices of white rust for lab (leaf) and field (UAV) conditions across crop stages and severity levels, for large-scale application', '• optimal wavelengths, White Rust Index, indices, TTFI', '• disease-specific and pre-symptomatic feature sets; physiological basis'], C.g, C.lt, { valign: 'top', align: 'left', fs: 12 });
box(s, 4.65, 1.2, 4.0, 2.55, 'Objective 2', ['**Outcome:** the best sensor or fusion of sensors for detection and monitoring of white rust throughout the crop growth stages', '• accuracy of 15 sensor sets; DT-EDNet vs comparison networks', '• camera contribution; gain over covariates; maps; Bharatpur test'], C.purple, C.lpurple, { valign: 'top', align: 'left', fs: 12 });
box(s, 8.85, 1.2, 4.03, 2.55, 'Objective 3', ['**Outcome:** early pre-symptomatic detection, so that appropriate preventive measures can be taken in time', '• pre-symptomatic models; earliest detection day', '• physiological changes before symptoms (7 Jan); risk maps'], C.red, C.lred, { valign: 'top', align: 'left', fs: 12 });
const wp = [['A–B: calibration, mosaics, co-registration, vegetation pixels', 0, 1, C.blue], ['D–F: features, indices, covariates, normalisation, folds; 1.1', 1, 1, C.blue], ['1.2–1.8: selection inside folds; pre-symptomatic stage; physiology', 2, 1, C.g],
  ['Objective 2: machine learning and feature-fusion networks (15 sets)', 3, 1, C.purple], ['Objective 2: DT-EDNet, comparison networks, ablation, SHAP, maps', 4, 1, C.purple], ['Objective 3; independent testing (Bharatpur); synthesis, writing', 5, 1, C.red]];
const gx = 6.85, gw = 1.0;
['M1', 'M2', 'M3', 'M4', 'M5', 'M6'].forEach((m, i) => T(s, '**' + m + '**', gx + i * gw, 3.82, gw, 0.28, { align: 'center', fontSize: 13 }));
wp.forEach((w, i) => { const y = 4.1 + i * 0.39; T(s, w[0], 0.45, y, 6.3, 0.38, { valign: 'middle', fontSize: 13 }); for (let k = 0; k < 6; k++) s.addShape(pres.shapes.RECTANGLE, { x: gx + k * gw, y: y + 0.03, w: gw, h: 0.33, fill: { color: 'FAFAFA' }, line: { color: 'DDDDDD', width: 0.5 } });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: gx + w[1] * gw + 0.05, y: y + 0.07, w: w[2] * gw - 0.1, h: 0.25, fill: { color: w[3] }, line: { color: w[3] }, rectRadius: 0.05 }); });
T(s, [{ text: 'Software: ', options: { bold: true, color: C.g } }, { text: 'ENVI or Python (GDAL, rasterio) for images; NumPy, pandas, scikit-learn (Pedregosa et al., 2011), XGBoost (Chen and Guestrin, 2016), SHAP (Lundberg and Lee, 2017), mlxtend (Raschka, 2018); PyTorch (Paszke et al., 2019) on a GPU.' }], 0.45, 6.5, 12.43, 0.52, { fontSize: 12 });
// 48-49  ------------------------------------------------------------------ references
const R = JSON.parse(fs.readFileSync(__dirname + '/../method3/mf3_refs_used.json', 'utf8')).concat(JSON.parse(fs.readFileSync(__dirname + '/pool.json', 'utf8')));
const keys = [['Ma, J', '2026'], ['Saharan', '2014'], ['Chattopadhyay', '2011'], ['Kumar, S., Kalha', '2005'], ['Mishra', '2009'], ['Conn', '1990'], ['Bock, C.H., Poole', '2010'], ['Mahlein, A.-K. (2016)', '2016'], ['Maimaitijiang', '2020'],
  ['Feng, Z', '2022'], ['Guo, A', '2021'], ['Mahlein, A.-K., Rumpf', '2013'], ['Roberts', '2017'], ['Varma', '2006'], ['Li, H', '2009'], ['Lundberg, S.M., Lee', '2017'], ['Robnik', '2003'],
  ['Peng, H', '2005'], ['Haralick', '1973'], ['Dormann', '2013'], ['Pudil', '1994'], ['Cortes', '1995'], ['Breiman', '2001'], ['Chen, T', '2016'], ['He, K', '2016'], ['Tan, M', '2019'], ['Woo, S., Debnath', '2023'],
  ['Woo, S., Park', '2018'], ['Hu, J', '2018'], ['Vaswani', '2017'], ['Zhu, H', '2017'], ['Zarco', '2018'], ['Wellburn', '1994'], ['Gomez', '1984'],
  ['Bijlwan', '2025'], ['De Wolf', '2007'], ['DeLong', '1988'], ['Efron', '1993'], ['Madden', '2007'], ['McCullagh', '1980'], ['Zhang, J., Pu, R., Yuan', '2014'], ['Kuhn, M', '2013'], ['Ruan', '2022'], ['Benjamini', '1995'], ['Terentev', '2023']];
const refs = keys.map(([k, y]) => R.find(r => r.startsWith(k) && r.includes('(' + y))).filter(Boolean).map(r => r.replace(/ https?:\/\/\S+$/, ''));
refs.sort((a, b) => a.localeCompare(b)); const half = Math.ceil(refs.length / 2);
[refs.slice(0, half), refs.slice(half)].forEach((part, i) => {
  s = S('Key references (' + (i + 1) + '/2)', 'References', 'Key references; full references of the 48 published indices are on the two index slides (Step D4); the complete list is in the methodology document.');
  const runs = part.map((r, j) => ({ text: r, options: { breakLine: j < part.length - 1, paraSpaceAfter: 2 } }));
  s.addText(runs, { x: 0.45, y: 1.15, w: 12.43, h: 5.85, fontFace: F, fontSize: 10, color: C.dk, valign: 'top', isTextBox: true, margin: 0.05 });
});
// 50 ------------------------------------------------------------------ thank you
s = pres.addSlide({ masterName: 'TITLE', sectionTitle: 'Conclusion' });
s.addText('Thank you', { placeholder: 'title' });
s.addText([{ text: 'Suggestions of the Advisory Committee are welcome', options: { breakLine: true } }, { text: ' ', options: { breakLine: true } }, { text: 'Animesh Panda | Ph.D. (Agricultural Physics) | ICAR-IARI, New Delhi' }], { placeholder: 'body' });
if (refs.length !== keys.length) console.log('WARNING: references not found:', keys.filter(([k, y]) => !R.find(r => r.startsWith(k) && r.includes('(' + y))).map(k => k.join(' ')).join('; '));
module.exports = { nrefs: refs.length };
