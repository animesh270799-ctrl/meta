# Objectives 1-3 (executed inside mf3_body.py)
# =====================================================================================
H1('3. Objective 1 – Characterisation of white rust through multimodal UAV sensing')
P('Objective 1 describes how each camera sees white rust and selects the features that carry disease information. It uses the 1536 post-symptomatic samples of each camera. For description and interpretation the steps are run on all post-symptomatic samples; for prediction (Objectives 2 and 3) exactly the same steps are repeated inside the training part of every fold (Step F2), so the test replication never chooses a feature.')
FIG('obj1', 'g05_obj1.png', 'Flow chart of Objective 1 (Activities 1.1–1.6).', 540)
TAB('o1act', [['Activity', 'Steps', 'Technique (one per feature type)', 'Output'],
    ['1.1 Response analysis', '1.1.1–1.1.3', 'mean spectra, first derivative, Pearson correlation', 'response figures; responsive regions'],
    ['1.2 Optimal wavelengths', '1.2.1–1.2.4', 'NDSI/RSI maps → SHAP-CARS', '10–15 optimal wavelengths (OW)'],
    ['1.3 Spectral index construction', '1.3.1–1.3.3', 'exhaustive two-band and three-band search', 'best NDSI, RSI and White Rust Index (WRI)'],
    ['1.4 Vegetation index selection', '1.4.1–1.4.3', 'redundancy filter → ReliefF / RReliefF', '5–8 selected indices'],
    ['1.5 Texture selection and TTFI', '1.5.1–1.5.4', 'principal-component texture → mRMR → TTFI', '6 texture features + best TTFI'],
    ['1.6 Disease-specific feature sets', '1.6.1–1.6.4', 'same rules for other cameras → variance inflation factor', 'feature set of each camera; treatment response']],
    'Activities of Objective 1.', [2400, 1100, 3000, 2806])
H2('The feature-selection rule: one method for each type of feature')
P('Pooling all features (about 1150 for the four cameras) and selecting from one big pool would be unstable, would keep many near-duplicates and would let the hundreds of spectral bands swamp the small thermal and texture groups (Hughes, 1968; Guyon and Elisseeff, 2003; Dormann et al., 2013; Ghamisi et al., 2019). Selection is therefore done in four stages, and in Stage 2 one method is used for each type of feature, the method that best suits the nature of that type and that was used for the same type in the DT-EDNet study (Ma et al., 2026) (Figure [[F:selection]]).')
TAB('stages', [['Stage', 'What is done', 'Uses labels?', 'Where in this document'],
    ['0. Build groups', 'calculate features with physical meaning (no second derivative)', 'no', 'Activity D'],
    ['1. Redundancy within groups', 'remove near-constant features; keep one feature of every cluster with |r| ≥ 0.95 (indices, texture, thermal, multispectral and colour groups)', 'no', 'Steps 1.4.2, 1.5.3, 1.6.1'],
    ['2. Selection within groups (one method per type)', 'spectral bands: SHAP-CARS; vegetation indices: ReliefF (RReliefF for the score); texture: mRMR; constructed indices: exhaustive search; thermal and multispectral bands: kept', 'yes', 'Activities 1.2–1.5'],
    ['3. Redundancy across groups', 'pool the survivors; variance inflation factor below 10', 'no', 'Step 1.6.2'],
    ['4. Final compact set (machine learning only)', 'sequential floating forward selection with each model, at most 15 features', 'yes', 'Step 2.1.4']],
    'The four selection stages.', [2200, 4400, 1100, 1606])
FIG('selection', 'g08_selection.png', 'One feature-selection method for each feature type, run inside the training part of each fold.', 540)

# ---------------------------------------------------------------- 1.1
H2('Activity 1.1 – Response analysis')
STEP('1.1.1', 'Mean spectra and first-derivative curves by severity grade',
     'Shows how the spectrum changes with severity before any selection and gives the physiological basis for later results.',
     'Subplot mean reflectance and first derivative (post-symptomatic).',
     'Response figures (Figure [[F:dummyspec]]) and a list of responsive regions → Activities 1.2–1.3 (interpretation).',
     ['Average the subplot spectra of each grade (0, 1, 3, 5, 7, 9) and plot them with ± one standard deviation.', 'Plot the first derivative in the red edge (680–760 nm) for each grade.', 'Describe the changes: visible rise from chlorophyll loss, shift of the red edge to shorter wavelengths, near-infrared fall from leaf damage, short-wave-infrared rise from water loss.'],
     'Spectral response by severity level: Mahlein et al. (2013), Guo et al. (2021), Ma et al. (2026); red-edge shift under stress: Horler et al. (1983), Filella and Peñuelas (1994).')
STEP('1.1.2', 'Correlation of each feature with the severity score',
     'Quantifies how strongly each feature follows severity and gives the direction of the response.',
     'All features of each camera.',
     'Correlation table and correlation curves → interpretation; used again in Steps 1.3 and 1.5.',
     ['Compute the Pearson correlation coefficient r between each feature and the severity score.', 'Plot r against wavelength for reflectance and first derivative (correlation curve).', 'Report r with its sign; p-values are not used for selection because subplots of one plot are related.'],
     'Correlation of indices and texture with severity: Ma et al. (2026), Guo et al. (2021); univariate feature screening: Liu et al. (2020).')
STEP('1.1.3', 'Response by variety, inoculation timing and days after inoculation',
     'A feature may respond in one variety or crop age and not in another; treatments must be considered.',
     'Responsive features; treatment codes.',
     'Treatment-wise response figures → Step 1.6.3 and Objective 2 robustness (Activity 2.6).',
     ['Plot the main features against days after inoculation for each variety (V1–V3) and inoculation timing (D1–D4).', 'Compare inoculated plots with their healthy plot of the same treatment on every date.'],
     'Treatment-wise disease response: Liu et al. (2024), Blasch et al. (2023), Feng et al. (2022).')

# ---------------------------------------------------------------- 1.2
H2('Activity 1.2 – Optimal wavelengths with Shapley additive explanations and competitive adaptive reweighted sampling (SHAP-CARS)')
P('The hyperspectral camera gives 483 reflectance bands and 483 first-derivative bands. Activity 1.2 reduces them to 10–15 optimal wavelengths (OW) in two stages: first the effective ranges are found from two-band index maps, then Shapley additive explanations combined with competitive adaptive reweighted sampling (SHAP-CARS) select the optimal wavelengths inside these ranges (Ma et al., 2026).')
STEP('1.2.1', 'Effective wavelength ranges from normalised difference spectral index (NDSI) and ratio spectral index (RSI) maps',
     'Many regions of the spectrum carry no disease information; searching all bands wastes time and adds noise.',
     'Subplot reflectance (training part).',
     'Effective wavelength ranges (regions where index pairs relate strongly to severity) → Step 1.2.2; the best pairs → Step 1.3.1.',
     ['For every pair of bands (λ_{1}, λ_{2}) compute the normalised difference spectral index NDSI and the ratio spectral index RSI (equations below); with 483 bands there are 116 403 pairs for each index.',
      'Compute the coefficient of determination R² between each index and the severity score and draw R² contour maps (Figure [[F:dummyndsi]]).',
      'Effective ranges = the wavelength regions that take part in pairs with R² ≥ 0.5 (as in Ma et al., 2026); if no pair reaches 0.5, use the regions of the top 5% of pairs.'],
     'Two-band NDSI and RSI searches and R² contour maps: Ma et al. (2026); optimised two-band indices for wheat diseases: Huang et al. (2014).')
EQ('NDSI(λ_{1}, λ_{2}) = (R_{λ1} − R_{λ2}) / (R_{λ1} + R_{λ2});      RSI(λ_{1}, λ_{2}) = R_{λ1} / R_{λ2}')
P('**Worked example (dummy data).** With R_{760} = 0.45 and R_{550} = 0.09, NDSI(760, 550) = (0.45 − 0.09) / (0.45 + 0.09) = 0.667 and RSI(760, 550) = 5.0. In a diseased subplot with R_{760} = 0.38 and R_{550} = 0.11 the values fall to 0.551 and 3.45.')
FIG('dummyndsi', 'g14_dummy_ndsi.png', 'Dummy example of an R² contour map of NDSI(λ₁, λ₂) against the severity score. The star marks the best pair; the bright regions define the effective ranges.', 400)
CARD('ndsi', 'Exhaustive two-band index search (NDSI and RSI maps)', 'Every pair of bands is turned into a normalised difference and a ratio; the relation of each index with severity is mapped, which shows which band combinations carry disease information.',
     'Finds disease-sensitive band combinations without prior assumptions and narrows the search for later selection.', 'All 116 403 pairs of the 483 bands; R² with the severity score on the training part; threshold R² ≥ 0.5.',
     'Threshold for the effective ranges (0.5, from Ma et al., 2026); checked so that the ranges are not narrower than about 20 nm.', 'Hyperspectral data with a continuous target (severity score).',
     'Simple, visual and directly linked to index construction (Step 1.3.1).', 'Ma et al. (2026); Huang et al. (2014)')
STEP('1.2.2', 'Shapley additive explanations (SHAP) pre-screening of the bands',
     'Inside the effective ranges there are still hundreds of correlated bands; a quick, model-based ranking removes clearly unimportant bands before the slower CARS step.',
     'Reflectance and first-derivative bands inside the effective ranges (training part).',
     'Top 40% of bands by mean absolute Shapley value → Step 1.2.3.',
     ['Train a tree ensemble (extreme gradient boosting, 300 trees, depth 4, learning rate 0.05) to predict the severity score from the bands.',
      'Compute the Shapley additive explanation (SHAP) value of every band for every training sample with the tree explainer.',
      'Rank bands by the mean absolute SHAP value and keep the top 40% (Figure [[F:dummyshap]]a).'],
     'Shapley values: Lundberg and Lee (2017), Lundberg et al. (2020); SHAP-based band selection: Ma et al. (2026).')
CARD('shap', 'Shapley additive explanations (SHAP)', 'From cooperative game theory: the contribution of a feature is its average effect on the prediction over all possible orders in which features are added to the model; for tree models it is computed exactly and quickly.',
     'Ranks bands by their real contribution to a non-linear model, including interactions, which simple correlation misses.', 'Tree explainer on an extreme gradient boosting model trained on the training part; ranking by mean |SHAP|; top 40% kept.',
     'Model settings (300 trees, depth 4, learning rate 0.05) fixed, because the model is only used for ranking; the kept share (30–50%) checked in the inner folds.', 'Tabular data with many correlated features and non-linear relations.',
     'Consistent and model-agnostic importance; used in this exact role by Ma et al. (2026).', 'Lundberg and Lee (2017); Lundberg et al. (2020); Ma et al. (2026)')
STEP('1.2.3', 'Competitive adaptive reweighted sampling (CARS) with partial least squares (PLS)',
     'The pre-screened bands are still strongly collinear; a small set of complementary wavelengths is needed.',
     'Pre-screened bands (training part).',
     'Optimal wavelength subset with the lowest cross-validated error → Step 1.2.4.',
     ['Choose the number of partial least squares (PLS) components (1–15) by Monte Carlo cross-validation (MCCV: 50 random 80/20 splits of the training plots).',
      'Run competitive adaptive reweighted sampling (CARS) for 50 iterations: in each iteration, fit PLS on a random 80% of the samples, weight every band by the absolute value of its PLS regression coefficient, remove bands by an exponentially decreasing function and then by adaptive reweighted sampling.',
      'After every iteration compute the root-mean-square error of cross-validation (RMSECV); the subset with the minimum RMSECV is the optimal subset (Figure [[F:dummyshap]]b, c).'],
     'CARS: Li et al. (2009); variable selection in PLS: Mehmood et al. (2012); SHAP-CARS with MCCV for the PLS components: Ma et al. (2026).')
FIG('dummyshap', 'g15_dummy_shapcars.png', 'Dummy example of SHAP-CARS: (a) Shapley pre-screening; (b) number of wavelengths kept in each CARS iteration; (c) the iteration with the minimum cross-validated error defines the optimal wavelengths.', 560)
CARD('cars', 'Competitive adaptive reweighted sampling (CARS) with partial least squares (PLS)', 'Imitates "survival of the fittest": bands with large PLS regression coefficients survive, bands with small coefficients are removed step by step; the subset with the lowest cross-validated error is kept. PLS itself projects correlated bands onto a few latent components that best predict the target.',
     'Selects a small set of non-redundant, informative wavelengths from highly collinear spectra.', '50 iterations; 80% sampling per iteration; PLS components by MCCV (50 splits, maximum 15); CARS repeated 20 times with different random seeds.',
     'Number of PLS components (by MCCV) and number of iterations (50); because results vary between runs, wavelengths selected in at least 50% of the 20 runs are kept (stability rule).', 'Spectra with many correlated bands and a continuous target.',
     'Designed for spectra, fast and the best of the three band-selection methods in the DT-EDNet study (Ma et al., 2026); the Shapley pre-screening adds a non-linear view.', 'Li et al. (2009); Mehmood et al. (2012); Ma et al. (2026)')
STEP('1.2.4', 'Optimal wavelengths (OW) and their stability',
     'The final wavelength set must be stable and physiologically interpretable.',
     'Optimal subsets of the 20 CARS runs.',
     'Optimal wavelengths (OW, 10–15 bands of reflectance and first derivative) → Activity 1.3, fused inputs of Objective 2 and the network configurations (Step 2.1.5).',
     ['Count how often each wavelength is selected over the 20 runs; keep those selected in at least 50%.', 'If more than 15 remain, keep the 15 most frequent.', 'Link each wavelength to a known absorption feature (chlorophyll, red edge, water, structure) for interpretation.'],
     'Stability of selection: Meinshausen and Bühlmann (2010), Nogueira et al. (2018); optimal wavelengths for rice blast: Ma et al. (2026).')

# ---------------------------------------------------------------- 1.3
H2('Activity 1.3 – Spectral index construction')
STEP('1.3.1', 'Best normalised difference spectral index (NDSI) and ratio spectral index (RSI)',
     'A single disease-related index is simpler and more transferable than many bands.',
     'NDSI and RSI maps (Step 1.2.1).',
     'Best NDSI and best RSI (highest R² with the severity score) → Activity 1.4 (index group).',
     ['Take the pair with the highest R² from each map.', 'Avoid pairs closer than 10 nm (they measure noise rather than a spectral feature).'],
     'Ma et al. (2026); Huang et al. (2014).')
STEP('1.3.2', 'White Rust Index (WRI), a three-band index',
     'Two bands may not capture both the pigment change and the structural change caused by white rust.',
     'Reflectance and the best normalised differences (training part).',
     'White Rust Index (WRI) formula → Activity 1.4 and Objectives 2–3.',
     ['Search WRI = NDSI(λ_{1}, λ_{2}) + w × R(λ_{3}) with w ∈ {−1, −0.5, 0, 0.5, 1}, using bands at 6 nm steps and λ_{1} and λ_{2} at least 50 nm apart.',
      'Score each candidate by its correlation with the severity score and by the balanced accuracy of healthy vs diseased in grouped inner cross-validation.',
      'Keep the best formula; repeat the search inside the training part of every fold for prediction.'],
     'Disease-specific indices from a normalised difference plus a single band: Mahlein et al. (2013); three-band disease index for yellow rust: Zheng et al. (2018); ground-to-UAV disease index for powdery mildew: Liu et al. (2026).')
EQ('WRI = NDSI(λ_{1}, λ_{2}) + w R_{λ3},      w ∈ {−1, −0.5, 0, 0.5, 1}')
CARD('wri', 'Disease-specific index search (White Rust Index)', 'Combines the most informative normalised difference with a third band that carries extra information; the weight w sets how much the third band contributes.',
     'Creates one interpretable index specific to white rust instead of a general vegetation index.', 'Bands at 6 nm steps inside the effective ranges; five weights; correlation and balanced accuracy in grouped inner folds.',
     'The weight w (five values) and the band positions; chosen in the inner folds only.', 'Hyperspectral data from which a cheaper sensor or a satellite band set may later be designed.',
     'The same form gave disease-specific indices for sugar beet diseases (Mahlein et al., 2013); the three-band idea was also used for yellow rust (Zheng et al., 2018).', 'Mahlein et al. (2013); Zheng et al. (2018)')
STEP('1.3.3', 'Two-band indices of the multispectral camera',
     'The multispectral camera has only five bands; its best band combination must be known.',
     'Five multispectral bands.',
     'Ranked ten normalised differences → Step 1.6.1.',
     ['Compute all ten normalised differences of the five bands.', 'Rank them by R² with the severity score and compare the best with the White Rust Index.'],
     'Ma et al. (2026); multispectral red-edge indices for powdery mildew: Liu et al. (2024).')

# ---------------------------------------------------------------- 1.4
H2('Activity 1.4 – Vegetation index selection with ReliefF')
STEP('1.4.1', 'Index group',
     'Collects all index-type features into one group.',
     'Published indices and red-edge parameters (Step D4); best NDSI, RSI and WRI (Activity 1.3).',
     'Index group of about 55 features → Step 1.4.2.',
     ['Join the published indices, the three red-edge parameters and the constructed indices.'],
     'Ma et al. (2026); Mahlein et al. (2013).')
STEP('1.4.2', 'Within-group redundancy filter',
     'Many indices are nearly identical (for example several NDVI versions), which wastes the selection on duplicates.',
     'Index group (training part).',
     'Thinned index group → Step 1.4.3.',
     ['Remove near-constant indices (standard deviation close to zero).', 'Group indices with |r| ≥ 0.95 and keep one per group (the one with the strongest correlation with the severity score).'],
     'Correlation clustering before selection: Dormann et al. (2013); high correlation among vegetation indices: Ma et al. (2026).')
CARD('corr', 'Correlation-cluster redundancy filter', 'Features whose pairwise |r| is at least 0.95 measure almost the same thing; one representative per cluster keeps the information.',
     'Removes duplicates before relevance selection, which makes ReliefF and mRMR more stable.', 'Pearson |r| ≥ 0.95; representative = the member with the strongest correlation with the severity score.',
     'Threshold 0.95 (fixed; 0.90 tested as a check).', 'Groups of derived features (indices, texture, thermal statistics).',
     'Label-free (no leakage), simple and transparent.', 'Dormann et al. (2013)')
STEP('1.4.3', 'ReliefF ranking of the indices',
     'The indices that best separate overlapping severity classes must be chosen.',
     'Thinned index group, standardised (training part).',
     'Top five to eight indices (number chosen in the inner folds) → Step 1.6.2 and the "VI" group of Step 2.1.5.',
     ['Classes: run ReliefF with k = 10 nearest neighbours on standardised indices; neighbours from the same plot are excluded so that a subplot is not compared with its own plot.',
      'Severity score: run RReliefF, the regression version, in the same way.',
      'Rank the indices by their weight and keep the top five (as in Ma et al., 2026); check 3–8 in the inner folds (Figure [[F:dummyrelief]]a).'],
     'ReliefF and RReliefF: Robnik-Šikonja and Kononenko (2003), Urbanowicz et al. (2018); ReliefF for disease indices: Mahlein et al. (2013), Huang et al. (2014); Relief for vegetation indices in rice blast: Ma et al. (2026).')
EQ('W_{j} ← W_{j} − diff(j, x, H)/m + Σ_{c≠class(x)} [P(c)/(1 − P(class(x)))] diff(j, x, M_{c})/m')
P('For each sampled subplot x, H is its nearest neighbour of the same class (nearest hit) and M_{c} its nearest neighbour of another class c (nearest miss); diff is the absolute difference of feature j. A feature gains weight when it differs between classes and loses weight when it differs within a class. **Worked example (dummy data):** for one sample, index A differs by 0.05 from its hit and by 0.40 from its misses, so its weight rises by about (0.40 − 0.05)/m; index B differs by 0.30 from both and gains nothing.')
FIG('dummyrelief', 'g16_dummy_relief_mrmr.png', 'Dummy example: (a) ReliefF weights of the indices (top six kept); (b) cumulative variance of the principal components of the cube (three kept); (c) mRMR ranking of the texture features (top six kept).', 560)
CARD('relief', 'ReliefF (classes) and RReliefF (severity score)', 'For each sample, compares its feature values with its nearest neighbours of the same class and of other classes; features that separate classes but are stable within classes gain weight. RReliefF does the same with the probability that predictions differ for a continuous target.',
     'Ranks features by their ability to separate overlapping, ordered severity classes, including effects that appear only together with other features.', 'k = 10 neighbours; all training samples used; standardised features; neighbours from the same plot excluded; top five kept.',
     'k (5, 10, 20) and the number kept (3–8) checked in the inner folds; k = 10 is the usual default.', 'Classification with several overlapping classes and moderate numbers of features (tens to hundreds).',
     'Handles several classes and interactions, is fast and was used for vegetation indices in the DT-EDNet study and for disease indices in hyperspectral studies.', 'Robnik-Šikonja and Kononenko (2003); Urbanowicz et al. (2018); Ma et al. (2026)')

# ---------------------------------------------------------------- 1.5
H2('Activity 1.5 – Texture selection and the Tri-band Texture Fusion Index (TTFI)')
STEP('1.5.1', 'Principal component analysis (PCA) texture of the hyperspectral cube',
     'Texture of 483 bands would give almost 4000 redundant features.',
     'Masked hyperspectral cube (Step D5).',
     '24 texture features (8 measures × 3 principal components, for example PC2-Dis = dissimilarity of component 2) → Step 1.5.2.',
     ['Fit principal component analysis on vegetation pixels of the training data and keep the first three components (cumulative variance above 95%; Figure [[F:dummyrelief]]b).', 'Compute the eight GLCM measures on each component image (Step D5) and average them over the vegetation pixels of each subplot.'],
     'Texture from principal-component images: Guo et al. (2021), Ma et al. (2026); GLCM: Haralick et al. (1973), Hall-Beyer (2017).')
STEP('1.5.2', 'Within-group redundancy filter',
     'Some texture measures are almost identical (for example contrast and dissimilarity).',
     '24 texture features (training part).', 'Thinned texture group → Step 1.5.3.',
     ['Apply the correlation-cluster filter (|r| ≥ 0.95), as in Step 1.4.2.'],
     'Dormann et al. (2013); Hall-Beyer (2017) on the strong correlation of contrast and dissimilarity.')
STEP('1.5.3', 'Minimum redundancy maximum relevance (mRMR) selection of texture',
     'Texture features are correlated with each other; the selected set should be informative and non-redundant.',
     'Thinned texture group (training part).',
     'Top six texture features (TF1–TF6) → Step 1.5.4 and the "TF" group of Step 2.1.5.',
     ['Estimate the relevance of each texture feature as its mutual information with the severity class (or score).',
      'Select features one at a time: the next feature is the one with the largest relevance minus its mean mutual information with the features already selected (Figure [[F:dummyrelief]]c).',
      'Stop at six features (as in Ma et al., 2026); check 4–8 in the inner folds.'],
     'mRMR: Peng et al. (2005); mRMR for texture features of rice blast: Ma et al. (2026); mRMR for UAV and satellite disease features: Yuan et al. (2025).')
EQ('next feature = arg max_{j} [ I(f_{j}; y) − (1/|S|) Σ_{s∈S} I(f_{j}; f_{s}) ]')
TAB('mrmrex', [['Texture feature (dummy)', 'Relevance I(f; y)', 'Mean redundancy with selected set', 'mRMR score', 'Decision'], ['PC2-Dis', '0.62', '— (first pick)', '0.62', 'selected 1st'],
    ['PC2-Con', '0.60', '0.55 (with PC2-Dis)', '0.05', 'not selected now'], ['PC3-Mea', '0.41', '0.08', '0.33', 'selected 2nd'], ['PC2-Hom', '0.52', '0.30', '0.22', 'selected 3rd']],
    'Worked example (dummy data): the first picks of mRMR. A strongly relevant but redundant feature (PC2-Con) is delayed in favour of a less relevant but new one (PC3-Mea).', [2200, 1500, 2300, 1300, 2006])
CARD('mrmr', 'Minimum redundancy maximum relevance (mRMR)', 'Greedy forward selection that balances two quantities measured with mutual information: relevance to the target and redundancy with the features already chosen.',
     'Selects a compact, complementary set from correlated texture features.', 'Mutual information estimated with a k-nearest-neighbour estimator (k = 3) on standardised features; difference criterion (relevance minus redundancy); six features.',
     'Number of features (4–8) checked in the inner folds; k of the estimator fixed at 3.', 'Groups of correlated features with non-linear relations to the target.',
     'Removes redundancy and selects relevance in one step; used for texture in the DT-EDNet study and for disease features by Yuan et al. (2025).', 'Peng et al. (2005); Ma et al. (2026); Yuan et al. (2025)')
STEP('1.5.4', 'Construction of the Tri-band Texture Fusion Index (TTFI)',
     'Single texture features describe only one aspect of the lesion pattern; a combination of three can describe roughness, heterogeneity and structure together.',
     'Selected texture features TF1–TF6 (training part).',
     'Best TTFI (strongest correlation with severity) → Step 1.6.2 and the network configurations (Step 2.1.5).',
     ['Form all ordered triplets (TF1, TF2, TF3) of the six texture features: 6 × 5 × 4 = 120 triplets.',
      'For every triplet compute the three Tri-band Texture Fusion Indices (equations below), giving 360 candidates.',
      'Compute the correlation of every candidate with the severity score; keep the best candidate of each formula for description (Figure [[F:dummyttfi]]) and the overall best TTFI as the texture index used in modelling.'],
     'Tri-band Texture Fusion Index: Ma et al. (2026).')
EQ('TTFI1 = (TF1 + TF2) / TF3;      TTFI2 = TF1 × TF2 / TF3;      TTFI3 = TF1 × (TF1 + TF2) / (TF2 + TF3)')
P('**Worked example (dummy data).** With TF1 = 0.8, TF2 = 1.2 and TF3 = 0.5: TTFI1 = (0.8 + 1.2) / 0.5 = 4.00; TTFI2 = 0.8 × 1.2 / 0.5 = 1.92; TTFI3 = 0.8 × (0.8 + 1.2) / (1.2 + 0.5) = 0.94. Texture values are used on their original (positive) scale; a small constant is added to a denominator that can approach zero.')
FIG('dummyttfi', 'g17_dummy_ttfi.png', 'Dummy example: correlation of the best triplet of each TTFI formula with severity, compared with the best single texture feature and the best index.', 460)
CARD('ttfi', 'Tri-band Texture Fusion Index (TTFI)', 'Combines three texture features in sums, products and ratios so that their joint behaviour (for example rising dissimilarity with falling homogeneity) is captured in one number.',
     'Gives one strong, interpretable texture variable instead of several weak ones.', 'Six mRMR-selected features; 120 ordered triplets × 3 formulas; best by |r| with the severity score on the training part.',
     'No hyper-parameters; the triplet is chosen in the inner folds only.', 'High-resolution texture from canopies with spotty lesions.',
     'In rice blast, TTFI3 was more strongly related to disease (|r| = 0.75) than any single texture feature and improved all networks when fused with the optimal wavelengths (Ma et al., 2026).', 'Ma et al. (2026)')

# ---------------------------------------------------------------- 1.6
H2('Activity 1.6 – Disease-specific feature sets of each camera')
STEP('1.6.1', 'Selection for the multispectral, red–green–blue and thermal cameras',
     'The other cameras must be treated with the same rule so that the cameras can be compared fairly.',
     'Feature groups of the three cameras (training part).',
     'Selected features of each camera → Step 1.6.2.',
     ['Multispectral: keep the five bands (small group); indices and normalised differences: redundancy filter → ReliefF (RReliefF for the score), top five; texture: redundancy filter → mRMR, top four.',
      'Red–green–blue: colour indices and colour means: redundancy filter → ReliefF, top four; texture: redundancy filter → mRMR, top four.',
      'Thermal: keep all thermal features after the redundancy filter (group of about 10).'],
     'One selection approach per group: Ma et al. (2026); thermal features kept as their own group: Feng et al. (2022), Liu et al. (2024).')
STEP('1.6.2', 'Variance inflation factor (VIF) across groups',
     'Survivors of different groups can still be correlated (for example a red-edge wavelength and a red-edge index).',
     'Pooled survivors of all groups of one camera (training part).',
     'Disease-specific feature set of the camera (about 10–25 features) → Objective 2 (Step 2.1.2) and discussion.',
     ['Pool the selected features of all groups of the camera.', 'Compute the variance inflation factor (VIF) of every feature; remove the feature with the highest VIF and repeat until all VIF values are below 10.'],
     'Dormann et al. (2013); variance inflation factor before feature-combination search in disease studies: Tian et al. (2021), Mustafa et al. (2023).')
EQ('VIF_{j} = 1 / (1 − R_{j}^{2})')
P('Here R_{j}^{2} is the coefficient of determination of feature j regressed on all other features. **Worked example:** a feature explained 90% by the others (R_{j}^{2} = 0.90) has VIF = 1 / 0.10 = 10, which is the removal limit.')
CARD('vif', 'Variance inflation factor (VIF)', 'Measures how much of a feature can be predicted from the other features; a large value means the feature is redundant with the rest.',
     'Removes multicollinearity across feature groups, which makes models and importance values stable.', 'Iterative removal of the feature with the largest VIF until all are below 10.',
     'Threshold 10 (the usual limit; 5 tested as a check).', 'Pooled sets of correlated predictors.',
     'Label-free, simple and widely used in disease-feature selection.', 'Dormann et al. (2013); Tian et al. (2021)')
STEP('1.6.3', 'Response by treatment and complementarity of cameras',
     'Shows whether the selected features behave the same in all varieties and inoculation timings and whether the cameras carry different information.',
     'Disease-specific feature sets; treatment codes.',
     'Treatment-wise response figures; correlation matrix between the cameras → Objective 2 interpretation.',
     ['Plot the selected features against days after inoculation for each variety and inoculation timing.', 'Compute the correlation matrix between the selected features of the four cameras (for example thermal difference vs short-wave-infrared water indices).', 'Check that selected features do not simply follow flower % or canopy cover (correlation with the covariates).'],
     'Sensor complementarity: Mahlein et al. (2019), Maimaitijiang et al. (2020); flowering effects in Brassica: Sulik and Long (2016).')
STEP('1.6.4', 'Outputs of Objective 1',
     'Summarises what Objective 1 delivers to the other objectives.',
     'Results of Activities 1.1–1.6.',
     'Feature lists and figures → Objectives 2 and 3; Objective 1 chapter of the thesis.',
     ['Response curves by grade, variety and inoculation timing.', 'Optimal wavelengths (OW) with their stability.', 'Best NDSI, RSI and the White Rust Index.', 'Selected vegetation indices, selected texture features and the best TTFI.', 'Disease-specific feature set of each camera and the correlation between cameras.'],
     'Ma et al. (2026); Mahlein et al. (2013).')
BOX('Link to satellite monitoring (optional extension, not part of the six-month plan).', 'The subplot hyperspectral spectra can be convolved with the relative spectral response functions of Sentinel-2 and Resourcesat LISS-IV to simulate satellite band reflectance, and the selected wavelengths and indices can then be tested with these simulated bands. This approach was used for yellow rust with Sentinel-2 (Zheng et al., 2018) and for rice bacterial leaf blight with LISS-IV (Das et al., 2015); UAV data have also been used to bridge field and satellite scales (Revill et al., 2020; Blasch et al., 2023; Poblete et al., 2023; Yuan et al., 2025).', 'EEF3E8', '2C5F2D')

# =====================================================================================
H1('4. Objective 2 – Detection and severity discrimination through AI-based multimodal data fusion')
P('Objective 2 builds and compares predictive models on the 1536 post-symptomatic samples of each camera. Three tasks are modelled: (A) healthy vs diseased, (B) severity classes and (C) severity score. Two comparisons are made: (1) all 15 sensor sets with machine learning, feature-fusion neural networks and the pseudo-image networks; (2) on the hyperspectral feature groups, DT-EDNet against EfficientNet, ResNet18 and ConvNeXt V2, repeating the design of Ma et al. (2026) with plot-grouped validation.')
FIG('obj2', 'g06_obj2.png', 'Flow chart of Objective 2 (Activities 2.1–2.6).', 540)
TAB('o2act', [['Activity', 'Steps', 'Main output'], ['2.1 Tasks and inputs', '2.1.1–2.1.5', 'task labels; fused feature sets of 15 sensor sets; hyperspectral feature-group configurations'],
    ['2.2 Machine-learning models', '2.2.1–2.2.6', 'tuned support vector machine, random forest, extreme gradient boosting, k-nearest neighbours and partial least squares models'],
    ['2.3 Deep-learning models', '2.3.1–2.3.8', 'feature-fusion networks and pseudo-image networks (DT-EDNet, EfficientNet, ResNet18, ConvNeXt V2)'],
    ['2.4 Evaluation', '2.4.1–2.4.3', 'metric tables'], ['2.5 Comparison, ablation and interpretation', '2.5.1–2.5.4', 'best sensor set and model; contribution of each camera; module ablation; Shapley explanation'],
    ['2.6 Robustness and maps', '2.6.1–2.6.3', 'results by treatment; transfer tests; severity maps']], 'Activities of Objective 2.', [2900, 1300, 5106])

# ---------------------------------------------------------------- 2.1
H2('Activity 2.1 – Tasks and inputs')
STEP('2.1.1', 'Three tasks and class balance',
     'Defines the three prediction problems and handles unequal class sizes.',
     'Post-symptomatic dataset with labels (Step A4).',
     'Three labelled task datasets → all models.',
     ['Task A, detection: healthy (grade 0) vs diseased (grade above 0).', 'Task B, severity classes: grades 0, 1, 3, 5, 7, 9 (merged if a class has fewer than 5% of samples).', 'Task C, regression: severity score.', 'Class weights (Step E6) for all classifiers; macro-averaged metrics.'],
     'Detection, severity classes and regression together: Tian et al. (2021), Feng et al. (2022), Abdulridha et al. (2023); three-class healthy, mild and severe classification: Yuan et al. (2025).')
STEP('2.1.2', 'Fold-wise feature selection for each camera',
     'Features must be selected without the test replication.',
     'Feature groups of each camera; outer and inner folds (Activity F).',
     'Disease-specific feature set of each camera for every fold and task → Step 2.1.3.',
     ['For every outer fold and task, repeat Activities 1.2–1.6 on the training part (label-based steps inside the inner folds).', 'Store the selected features of every fold (they are used for the stability analysis in Step 2.5.4).'],
     'Nested selection: Ambroise and McLachlan (2002), Varma and Simon (2006).')
STEP('2.1.3', 'Feature-level fusion for the 15 sensor sets',
     'Combinations of cameras need one input vector per sample.',
     'Disease-specific feature sets of the cameras.',
     'Fused feature set of each sensor set, fold and task → all models.',
     ['Single camera (S1–S4): its disease-specific feature set is the input.', 'Combination (S5–S15): concatenate the feature sets of its cameras and apply the variance inflation factor rule (below 10) again across cameras.', 'Standardise with training statistics (Step E5).'],
     'Feature-level fusion of spectral, thermal and texture features: Feng et al. (2022), Liu et al. (2024); fusion levels: Ghamisi et al. (2019); input- and intermediate-level fusion: Maimaitijiang et al. (2020).')
FIG('combinations', 'g10_combinations.png', 'The 15 sensor sets: 4 single cameras, 6 pairs, 4 triples and all four.', 520)
TAB('sets', [['Set', 'Cameras', 'Question it answers'], ['S1', 'hyperspectral', 'reference: what the most detailed camera achieves'], ['S2', 'multispectral', 'what a low-cost, satellite-like camera achieves'], ['S3', 'red–green–blue', 'what a consumer camera achieves'], ['S4', 'thermal', 'what canopy temperature alone achieves'],
    ['S5', 'hyperspectral + multispectral', 'whether the multispectral camera adds anything'], ['S6', 'hyperspectral + red–green–blue', 'whether fine colour texture adds to spectra'], ['S7', 'hyperspectral + thermal', 'whether temperature adds to spectra'], ['S8', 'multispectral + red–green–blue', 'low-cost optical pair'],
    ['S9', 'multispectral + thermal', 'low-cost spectral + thermal pair'], ['S10', 'red–green–blue + thermal', 'cheapest pair'], ['S11', 'hyperspectral + multispectral + red–green–blue', 'all optical cameras (is thermal needed?)'], ['S12', 'hyperspectral + multispectral + thermal', 'is red–green–blue needed?'],
    ['S13', 'hyperspectral + red–green–blue + thermal', 'is multispectral needed when hyperspectral is present?'], ['S14', 'multispectral + red–green–blue + thermal', 'all low-cost cameras'], ['S15', 'all four', 'full system; basis of the drop-one-camera ablation']],
    'The 15 sensor sets.', [900, 3600, 4806])
STEP('2.1.4', 'Final compact set by sequential floating forward selection (SFFS) for the machine-learning models',
     'Different models use features differently, and a small final set improves generalisation and interpretation.',
     'Fused feature set (training part).',
     'Optimum feature combination of each machine-learning model (at most 15 features) → Activity 2.2.',
     ['Run sequential floating forward selection (SFFS) wrapped around each machine-learning model, with macro-F1 (classes) or root-mean-square error (score) in the inner folds as criterion.',
      'Limit the set to 15 features and keep the smallest subset within 1% of the best score.',
      'The neural networks use the whole fused set, because they learn their own feature weights.'],
     'Floating search: Pudil et al. (1994); wrapper selection for disease models: Tian et al. (2021), Mustafa et al. (2023); backward wrapper selection for Fusarium head blight: Liu et al. (2020).')
TAB('sffsex', [['Iteration (dummy)', 'Action', 'Subset', 'Inner macro-F1'], ['1', 'add best single feature', 'WRI', '0.52'], ['2', 'add', 'WRI, OW 718 nm', '0.60'], ['3', 'add', 'WRI, OW 718 nm, ΔT', '0.65'],
    ['4', 'add', 'WRI, OW 718 nm, ΔT, TTFI', '0.68'], ['5', 'conditional removal: dropping OW 718 nm improves', 'WRI, ΔT, TTFI', '0.69'], ['…', 'continue until 15 features or no gain', '…', '…']],
    'Worked example (dummy data): sequential floating forward selection adds features and removes a feature when it becomes redundant.', [1600, 3600, 2500, 1606])
CARD('sffs', 'Sequential floating forward selection (SFFS)', 'Adds the feature that most improves the model; after every addition it tries to remove previously added features and removes one if the model improves ("floating").',
     'Finds a small feature set suited to each model and corrects early choices that later become redundant.', 'Wrapped around each machine-learning model; criterion macro-F1 or root-mean-square error in the inner folds; at most 15 features; smallest subset within 1% of the best.',
     'Maximum subset size (15) and tolerance (1%); fixed to keep at least about 60 training samples per feature.', 'Moderate candidate sets (20–40 features) after the earlier stages; not for hundreds of features.',
     'Gives the model-specific final set recommended in the staged approach while keeping the number of candidates small.', 'Pudil et al. (1994); Tian et al. (2021)')
STEP('2.1.5', 'Hyperspectral feature-group configurations for the network comparison',
     'The DT-EDNet study compared networks on separate feature groups and on their combinations; the same design shows which hyperspectral feature types help each network.',
     'Fold-wise optimal wavelengths, selected indices, selected texture features and best TTFI of the hyperspectral camera.',
     'Six input configurations → pseudo-image networks (Activity 2.3) and the best machine-learning model as reference.',
     ['OW: optimal wavelengths only.', 'VI: selected vegetation indices only.', 'TF: selected texture features only.', 'OW + VI.', 'OW + TTFI.', 'OW + VI + TTFI (the best combination in Ma et al., 2026).'],
     'Feature-group configurations: Ma et al. (2026); vegetation index and texture fusion for yellow rust: Guo et al. (2021).')

# ---------------------------------------------------------------- 2.2
H2('Activity 2.2 – Machine-learning models')
P('Five machine-learning model families are used for classification and their regression versions for the severity score. They cover kernel, tree-ensemble, boosting, instance-based and latent-variable approaches, so that conclusions do not depend on one type of model.')
STEP('2.2.1', 'Support vector machine (SVM) and support vector regression (SVR)',
     'A robust classifier and regressor for a few hundred to a few thousand samples with correlated features.',
     'Optimum feature combination (standardised).', 'Predictions on the test replication → Activity 2.4.',
     ['Radial basis function kernel; class weights for classes; one-vs-one for several classes.', 'Tune C, γ (and ε for regression) by grid search in the inner folds (Table [[T:mlgrid]]).'],
     'Cortes and Vapnik (1995); Mountrakis et al. (2011); disease applications: Tian et al. (2021), Mustafa et al. (2023), Yuan et al. (2025).')
CARD('svm', 'Support vector machine (SVM) and support vector regression (SVR)', 'Finds the boundary with the largest margin between classes (or a tube of width ε around the regression line); the kernel maps the data so that curved boundaries become possible.',
     'Non-linear classification and regression with limited samples.', 'Radial basis function kernel; class weights; standardised inputs.',
     'C ∈ {0.1, 1, 10, 100}; γ ∈ {0.001, 0.01, 0.1, scale}; ε ∈ {0.1, 0.5} for regression; grid search in the inner folds.', 'Small to medium samples (hundreds to thousands), moderate numbers of standardised features.',
     'Among the most accurate classifiers in remote sensing for limited training data.', 'Cortes and Vapnik (1995); Mountrakis et al. (2011)')
STEP('2.2.2', 'Random forest (RF)',
     'A robust, little-tuned model that handles non-linear effects and gives feature importance.',
     'Optimum feature combination.', 'Predictions → Activity 2.4.',
     ['500 trees; class weights; tune the number of features per split and the minimum leaf size.'],
     'Breiman (2001); Belgiu and Drăguţ (2016); disease applications: Abdulridha et al. (2023), Liu et al. (2024), Yu et al. (2021), Yuan et al. (2025).')
CARD('rf', 'Random forest (RF)', 'Averages many decision trees, each grown on a bootstrap sample and choosing among a random subset of features at every split.',
     'Non-linear classification and regression that resists overfitting and noise.', '500 trees; class weights; out-of-bag error monitored.',
     'Features per split ∈ {√p, 0.3p}; minimum leaf size ∈ {1, 3, 5}; grid search in the inner folds.', 'Tabular data with mixed, noisy features; small and large samples.',
     'Little tuning, stable, widely used in UAV disease studies.', 'Breiman (2001); Belgiu and Drăguţ (2016)')
STEP('2.2.3', 'Extreme gradient boosting (XGBoost)',
     'Often the most accurate tree model on tabular features.',
     'Optimum feature combination.', 'Predictions → Activity 2.4.',
     ['Tune the number of trees, depth and learning rate; subsample 0.8; sample weights from the class weights.'],
     'Chen and Guestrin (2016).')
CARD('xgb', 'Extreme gradient boosting (XGBoost)', 'Adds small trees one after another; each new tree corrects the errors of the previous ones, with regularisation of tree complexity.',
     'High-accuracy non-linear modelling of tabular features.', 'Subsample 0.8; column subsample 0.8; early stopping on the inner validation plots.',
     'Trees ∈ {200, 500}; depth ∈ {3, 5}; learning rate ∈ {0.05, 0.1}; grid search in the inner folds.', 'Tabular data with non-linear interactions; medium samples.',
     'Strong benchmark model; complements random forest (boosting vs averaging).', 'Chen and Guestrin (2016)')
STEP('2.2.4', 'k-nearest neighbours (k-NN)',
     'A simple reference model that predicts from the most similar training samples.',
     'Optimum feature combination (standardised).', 'Predictions → Activity 2.4.',
     ['Tune k and the weighting (uniform or by distance).'], 'Cover and Hart (1967); Yuan et al. (2025).')
CARD('knn', 'k-nearest neighbours (k-NN)', 'Predicts the class (majority vote) or score (mean) of the k most similar training samples in feature space.',
     'Simple non-parametric reference model.', 'Euclidean distance on standardised features.',
     'k ∈ {3, 5, 7, 9, 11}; uniform or distance weights; grid search in the inner folds.', 'Compact, standardised feature sets; low-dimensional data.',
     'Transparent baseline; shows whether more complex models are needed.', 'Cover and Hart (1967)')
STEP('2.2.5', 'Partial least squares discriminant analysis (PLS-DA) and regression (PLSR)',
     'The standard chemometric model for correlated spectral features.',
     'Optimum feature combination (standardised).', 'Predictions → Activity 2.4.',
     ['Tune the number of latent variables (1–15) in the inner folds.'], 'Wold et al. (2001); Barker and Rayens (2003); Guo et al. (2021).')
CARD('pls', 'Partial least squares discriminant analysis (PLS-DA) and regression (PLSR)', 'Projects correlated features onto a few latent variables that have maximum covariance with the target, then fits a linear model on them.',
     'Linear modelling of many correlated predictors without collinearity problems.', 'Standardised inputs; classes coded as dummy variables for discriminant analysis.',
     'Number of latent variables 1–15, chosen in the inner folds.', 'Spectral data with strong collinearity; linear or near-linear relations.',
     'Linear reference used in most hyperspectral disease studies (for example yellow rust monitoring by Guo et al., 2021).', 'Wold et al. (2001); Barker and Rayens (2003)')
STEP('2.2.6', 'Tuning grids of the machine-learning models',
     'All models must be tuned in the same honest way.', 'Inner folds (Step F2).', 'Tuned hyper-parameters of every model, fold and sensor set → final training.',
     ['Use the grids in Table [[T:mlgrid]]; choose the combination with the best mean inner score.'], 'Kuhn and Johnson (2013); Cawley and Talbot (2010).')
TAB('mlgrid', [['Model', 'Tasks', 'Hyper-parameters tuned (inner cross-validation)'], ['Support vector machine / regression', 'A, B / C', 'C ∈ {0.1, 1, 10, 100}; γ ∈ {0.001, 0.01, 0.1, scale}; ε ∈ {0.1, 0.5} (regression)'],
    ['Random forest', 'A, B, C', '500 trees; features per split ∈ {√p, 0.3p}; minimum leaf size ∈ {1, 3, 5}'], ['Extreme gradient boosting', 'A, B, C', 'trees ∈ {200, 500}; depth ∈ {3, 5}; learning rate ∈ {0.05, 0.1}; subsample 0.8'],
    ['k-nearest neighbours', 'A, B, C', 'k ∈ {3, 5, 7, 9, 11}; uniform or distance weights'], ['Partial least squares (discriminant analysis / regression)', 'A, B / C', 'number of latent variables 1–15']],
    'Machine-learning models and tuning grids.', [3100, 1100, 5106])

# ---------------------------------------------------------------- 2.3
H2('Activity 2.3 – Deep-learning models')
P('Two kinds of networks are used. Feature-fusion networks (DNN-F1, DNN-F2) take the fused feature vector directly. Pseudo-image networks (DT-EDNet and the three comparison networks) first reshape the feature vector into a small two-dimensional "image", as in Ma et al. (2026). All networks are trained on exactly the same folds as the machine-learning models.')
STEP('2.3.1', 'Deep neural network with input-level feature fusion (DNN-F1)',
     'Learns non-linear interactions between the features of different cameras from one concatenated vector.',
     'Fused feature set (standardised).', 'Predictions → Activity 2.4.',
     ['Concatenate the features of all cameras of the set.', 'Two dense layers (64 and 32 units) with batch normalisation, ReLU activation and dropout, then the output layer (softmax for classes, linear for the score).', 'Adam optimiser, learning rate 0.001, weight decay 10^{−4}, batch size 32, up to 500 epochs with early stopping (patience 30) on the inner validation plots; five random seeds averaged.'],
     'Maimaitijiang et al. (2020); Kingma and Ba (2015); Srivastava et al. (2014); Ioffe and Szegedy (2015).')
STEP('2.3.2', 'Deep neural network with intermediate-level feature fusion (DNN-F2)',
     'Lets each camera be processed separately before fusion and learns how much each camera contributes.',
     'Selected features of each camera in the set (standardised).', 'Predictions and camera attention weights → Activities 2.4 and 2.5.',
     ['One small sub-network per camera (one or two dense layers of 16–32 units).', 'A squeeze-and-excitation (SE) attention block gives each camera branch a learned weight.', 'Concatenate the weighted branches → dense layer of 32 units → output; same training as DNN-F1; used only for sets with two or more cameras.'],
     'Maimaitijiang et al. (2020); squeeze-and-excitation: Hu et al. (2018).')
FIG('dnn', 'g21_dnn.png', 'Feature-fusion networks: DNN-F1 (input-level fusion) and DNN-F2 (intermediate fusion with camera attention).', 540)
CARD('dnnf', 'Feature-fusion deep neural networks (DNN-F1 and DNN-F2)', 'Fully connected layers learn weighted, non-linear combinations of the input features; DNN-F2 first learns a representation for each camera and weights the cameras with attention.',
     'Non-linear fusion of features from several cameras; DNN-F2 also shows which camera the model relies on.', 'DNN-F1: 64–32 units; DNN-F2: 16–32 units per camera branch, attention block, 32 units; batch normalisation; dropout; class-weighted cross-entropy or mean squared error.',
     'Units ∈ {32, 64} (first layer) and dropout ∈ {0.2, 0.3, 0.4}, tuned in the inner folds; epochs by early stopping.', 'About a thousand samples with tens of features; multi-sensor feature vectors.',
     'Compact enough for the sample size; intermediate fusion was better than input fusion in multi-sensor UAV data (Maimaitijiang et al., 2020).', 'Maimaitijiang et al. (2020); Hu et al. (2018)')
STEP('2.3.3', 'Pseudo-image construction',
     'Convolutional and transformer networks need a two-dimensional input, but each sample is a feature vector.',
     'Fused feature set or hyperspectral configuration (standardised).',
     'One-channel pseudo-image of k × k pixels per sample → Steps 2.3.4–2.3.7.',
     ['Order the features by group and, within the spectral group, by wavelength (optimal wavelengths, indices, texture, TTFI, then other cameras), so that neighbouring pixels hold related features.',
      'Choose k = the smallest integer with k² ≥ number of features (minimum 3); fill the k × k grid row by row.',
      'Fill the remaining pixels with zeros (zero is the training mean after standardisation, so padding adds no information).',
      'Example: 22 features → 5 × 5 image with 3 padded pixels (Figure [[F:pseudo]]).'],
     'Pseudo-two-dimensional input of spectral features: Ma et al. (2026); arranging non-image features as images for convolutional networks: Sharma et al. (2019).')
FIG('pseudo', 'g18_pseudoimage.png', 'Construction of a pseudo-image from a standardised feature vector (dummy values).', 540)
CARD('pseudo', 'Pseudo-image (feature-to-image) representation', 'Places the features of one sample on a small grid so that convolution and attention can relate neighbouring and distant features.',
     'Allows image networks to be applied to tabular features.', 'Group-and-wavelength ordering; k = ⌈√p⌉ (minimum 3); zero padding after standardisation; one channel.',
     'No tuning (fixed ordering, so results are reproducible).', 'Ordered features such as spectra, where neighbours are related.',
     'Needed to reproduce the DT-EDNet design; the fixed ordering keeps related features together.', 'Ma et al. (2026); Sharma et al. (2019)')
STEP('2.3.4', 'DT-EDNet (Dual Transformer Early Detection Network)',
     'Captures local relations between neighbouring features (convolution and attention) and long-range relations between distant features (self-attention) in one network.',
     'Pseudo-images.', 'Predictions → Activity 2.4; module ablation → Step 2.5.3.',
     ['Embedding: 3 × 3 convolution (stride 1) to 128 channels.',
      'Squeeze-and-excitation block: global average pooling of each channel → two small dense layers → sigmoid weight per channel → channels re-weighted.',
      'Tokens: flatten the k × k map into k² tokens of length 128 and add a learnable class token (and position embedding).',
      'Dual Transformer Group: one Kernel Transformer Block (convolution with the convolutional block attention module, CBAM: channel attention then spatial attention) followed by four Token Transformer Blocks (layer normalisation → multi-head self-attention with 4 heads → layer normalisation → feed-forward network, each with a residual connection); dropout 0.03.',
      'Head: layer normalisation of the class token → linear layer (softmax for classes, one linear output for the score).'],
     'DT-EDNet: Ma et al. (2026); squeeze-and-excitation: Hu et al. (2018); CBAM: Woo et al. (2018); self-attention and transformers: Vaswani et al. (2017); class token: Dosovitskiy et al. (2021).')
FIG('dtednet', 'g19_dtednet.png', 'Architecture of DT-EDNet (after Ma et al., 2026) and the role of its three attention mechanisms.', 560)
EQ('Attention(Q, K, V) = softmax( Q K^{T} / √d ) V')
P('In self-attention every token forms a query Q, a key K and a value V; the softmax of the scaled products Q K^{T} decides how much each token takes from every other token, d being the token length per head (128 / 4 = 32). This is how a red-edge wavelength can be related directly to a texture feature placed far away on the pseudo-image.')
CARD('dtednet', 'DT-EDNet (Dual Transformer Early Detection Network)', 'A hybrid network: convolution embeds the pseudo-image, squeeze-and-excitation re-weights channels, the Kernel Transformer Block (convolution + CBAM) learns local spatial–channel patterns and the Token Transformer Blocks (multi-head self-attention) learn global relations; the class token summarises the sample.',
     'Models both local and long-range interactions among selected spectral, index and texture features.', 'Embedding 128; SE block; 1 Kernel Transformer Block + 4 Token Transformer Blocks; 4 heads; dropout 0.03; trained from scratch.',
     'Fixed architecture as published; learning rate and dropout tuned in the inner folds (Step 2.3.8).', 'Sets of a few to a few tens of ordered features with complex interactions; best with thousands of samples.',
     'Highest accuracy on rice blast (overall accuracy 95.25% with optimal wavelengths + indices + TTFI) against EfficientNet, ResNet18 and ConvNeXt V2 (Ma et al., 2026); tested here under plot-grouped validation.', 'Ma et al. (2026); Hu et al. (2018); Woo et al. (2018); Vaswani et al. (2017)')
STEP('2.3.5', 'EfficientNet (comparison network)',
     'A modern, efficient convolutional network used as a comparison in the DT-EDNet study.',
     'Pseudo-images.', 'Predictions → Activity 2.4.',
     ['EfficientNet-B0: mobile inverted bottleneck blocks with depthwise convolution and squeeze-and-excitation.', 'Stem changed to a 3 × 3 convolution with stride 1 and one input channel (the input is only a few pixels wide).', 'Global average pooling → linear head; trained from scratch.'],
     'Tan and Le (2019); Ma et al. (2026).')
STEP('2.3.6', 'ResNet18 (comparison network)',
     'A classic residual convolutional network used as a comparison.',
     'Pseudo-images.', 'Predictions → Activity 2.4.',
     ['Four stages of two basic residual blocks (two 3 × 3 convolutions with an identity shortcut).', 'Stem changed to a 3 × 3 convolution with stride 1 and no max-pooling.', 'Global average pooling → linear head; trained from scratch.'],
     'He et al. (2016); Ma et al. (2026).')
STEP('2.3.7', 'ConvNeXt V2 (comparison network)',
     'A recent convolutional network that borrows design ideas from transformers, used as a comparison.',
     'Pseudo-images.', 'Predictions → Activity 2.4.',
     ['ConvNeXt V2-Atto (smallest version, about 3.7 million parameters): blocks with 7 × 7 depthwise convolution, layer normalisation and a feed-forward network with global response normalisation.', 'Stem changed to stride 1; global average pooling → linear head; trained from scratch.'],
     'Woo et al. (2023); Ma et al. (2026).')
FIG('cnns', 'g20_cnns.png', 'The three comparison networks with the changes made for small pseudo-images.', 540)
CARD('cnn', 'Comparison networks: EfficientNet-B0, ResNet18 and ConvNeXt V2-Atto', 'Convolutional networks: EfficientNet scales depth, width and resolution together and uses squeeze-and-excitation; ResNet adds identity shortcuts so deep networks train well; ConvNeXt V2 uses large depthwise kernels and global response normalisation.',
     'Benchmarks that show whether the transformer parts of DT-EDNet add accuracy over strong convolutional designs.', 'One input channel; stride-1 stems; global average pooling; linear head; trained from scratch with the same settings as DT-EDNet.',
     'Same tuning budget as DT-EDNet (learning rate and dropout in the inner folds).', 'Image-like inputs; large datasets (risk of overfitting with about a thousand samples, controlled by early stopping and regularisation).',
     'Exactly the comparison set used by Ma et al. (2026); covers classic, efficient and modern convolutional designs.', 'He et al. (2016); Tan and Le (2019); Woo et al. (2023); Kattenborn et al. (2021)')
STEP('2.3.8', 'Common training protocol and tuning of the pseudo-image networks',
     'A fair comparison requires identical training settings for all four networks.',
     'Pseudo-images of the training part; inner validation plots.',
     'Trained networks (five seeds each) → Activity 2.4.',
     ['Optimiser: AdamW, initial learning rate 6 × 10^{−4}, weight decay 1 × 10^{−5}; cosine annealing of the learning rate to 1 × 10^{−6} over 300 epochs; batch size 32.',
      'Loss: cross-entropy with label smoothing 0.01 and class weights (classes); mean squared error (score).',
      'Gradient clipping at a maximum norm of 1.2; early stopping with patience 60 epochs and minimum improvement 5 × 10^{−5}.',
      'Model selection on the inner validation plots (macro-F1 for classes because the classes are unequal; root-mean-square error for the score), not on a random 10% of samples.',
      'Tuning: learning rate ∈ {3 × 10^{−4}, 6 × 10^{−4}, 1 × 10^{−3}} and dropout ∈ {0.03, 0.1, 0.3}, same grid for all four networks.',
      'Five random seeds (42 and four others); report mean ± standard deviation.'],
     'Training settings: Ma et al. (2026); AdamW: Loshchilov and Hutter (2019); cosine annealing: Loshchilov and Hutter (2017); label smoothing: Szegedy et al. (2016), Müller et al. (2019); gradient clipping: Pascanu et al. (2013).')
CARD('train', 'Training techniques (AdamW, cosine annealing, label smoothing, gradient clipping, early stopping)', 'AdamW adapts the step size of every weight and applies weight decay separately; cosine annealing lowers the learning rate smoothly; label smoothing replaces hard 0/1 targets with slightly softened ones; gradient clipping limits very large updates; early stopping ends training when the validation score stops improving.',
     'Stable training and less overfitting on a small dataset.', 'Values of Step 2.3.8 (from Ma et al., 2026).',
     'Learning rate and dropout tuned; other values fixed as published.', 'Neural networks trained from scratch on small to medium datasets.',
     'Reproduces the published protocol, so differences come from the data and validation design, not from different training.', 'Loshchilov and Hutter (2017, 2019); Müller et al. (2019); Pascanu et al. (2013)')

# ---------------------------------------------------------------- 2.4
H2('Activity 2.4 – Evaluation')
STEP('2.4.1', 'Classification metrics',
     'Accuracy must reflect unequal classes and ordered grades.',
     'Predictions on the three test replications.', 'Metric tables → Activity 2.5.',
     ['Task A: overall accuracy, sensitivity, specificity, F1 and area under the receiver operating characteristic curve (AUC).',
      'Task B: overall accuracy, Cohen\'s kappa, quadratic-weighted kappa (ordered grades), macro-averaged recall and F1, per-class precision, recall and F1, confusion matrix and the share of predictions within one grade of the true grade.'],
     'Cohen (1960, 1968); Sokolova and Lapalme (2009); Fawcett (2006); the metrics of Ma et al. (2026) (overall accuracy, kappa, macro recall, macro-F1, per-class scores) are all included.')
EQ('OA = correct / N;    precision = TP / (TP + FP);    recall = TP / (TP + FN);    F1 = 2 × precision × recall / (precision + recall)')
EQ('κ = (p_{o} − p_{e}) / (1 − p_{e});    κ_{w} = 1 − Σ w_{ij} O_{ij} / Σ w_{ij} E_{ij},   w_{ij} = (i − j)^{2} / (k − 1)^{2}')
STEP('2.4.2', 'Regression metrics',
     'The severity-score models need error measures in score units.',
     'Predicted and observed scores of the test replications.', 'Metric tables → Activity 2.5.',
     ['Coefficient of determination (R²), root-mean-square error (RMSE) and ratio of performance to deviation (RPD = standard deviation of observed scores / RMSE).'],
     'Chang et al. (2001); Guo et al. (2021); Feng et al. (2022).')
EQ('R^{2} = 1 − Σ (y − ŷ)^{2} / Σ (y − ȳ)^{2};    RMSE = √[ (1/n) Σ (y − ŷ)^{2} ];    RPD = SD_{y} / RMSE')
STEP('2.4.3', 'Worked example of the metrics',
     'Shows how the numbers in the result tables are obtained.', 'Dummy confusion matrix and dummy predictions.', 'Example values (below).',
     ['Classification: from the confusion matrix in Figure [[F:dummycm]] (532 test samples), 396 are on the diagonal, so overall accuracy = 396 / 532 = 0.744; chance agreement p_{e} = 0.182, so κ = (0.744 − 0.182) / (1 − 0.182) = 0.687; quadratic-weighted kappa = 0.937 (most errors are between neighbouring grades); macro-F1 = 0.733; 97.4% of predictions are within one grade.',
      'Regression: for eight dummy subplots with observed scores 0, 1, 3, 5, 7, 9, 3, 5 and predictions 0.4, 1.6, 2.5, 5.8, 6.1, 8.2, 3.9, 4.4: R² = 0.94, RMSE = 0.71 and RPD = 3.00 / 0.71 = 4.2.'],
     'Cohen (1960); Sokolova and Lapalme (2009); Chang et al. (2001).')
FIG('dummycm', 'g22_dummy_cm.png', 'Dummy confusion matrix of one test replication (six grades).', 360)
CARD('metrics', 'Evaluation metrics', 'Overall accuracy counts correct predictions; kappa corrects it for chance; weighted kappa gives partial credit to near misses between ordered grades; F1 combines precision and recall per class; R², RMSE and RPD describe regression error.',
     'Measures performance fairly when classes are unequal and ordered.', 'Computed on the pooled predictions of the three test replications and per fold; mean ± standard deviation over folds and seeds.',
     'None.', 'Classification with unequal, ordered classes; continuous scores.',
     'Covers the metrics of the DT-EDNet study and the extra ones needed for ordered grades and regression.', 'Cohen (1960, 1968); Sokolova and Lapalme (2009); Chang et al. (2001)')

# ---------------------------------------------------------------- 2.5
H2('Activity 2.5 – Comparison, ablation and interpretation')
STEP('2.5.1', 'Ranking of sensor sets and models',
     'Identifies the best sensor set and model for each task.',
     'Metric tables of 15 sets × models × tasks.', 'Best sensor set and model per task → conclusions and maps.',
     ['Rank the 15 sets by macro-F1 (Task B), AUC (Task A) and RMSE (Task C) for each model.', 'Compare the best machine-learning, best feature-fusion network and best pseudo-image network.', 'Call a difference real only if it is larger than the fold-to-fold standard deviation and appears in all three folds.'],
     'Feng et al. (2022); Maimaitijiang et al. (2020); Ma et al. (2026).')
STEP('2.5.2', 'Fusion gain and drop-one-camera ablation',
     'Answers directly whether a camera is worth flying.',
     'Metrics of single cameras and combinations.', 'Fusion gains and the contribution of each camera → conclusions.',
     ['Fusion gain = metric of a combination minus the metric of its best single camera.', 'Remove one camera at a time from S15 and record the drop in macro-F1 and R².', 'Report the camera attention weights of DNN-F2.'],
     'Ablation of feature groups: Ma et al. (2026); fusion gain: Feng et al. (2022), Maimaitijiang et al. (2020).')
STEP('2.5.3', 'Network comparison on the hyperspectral configurations and DT-EDNet module ablation',
     'Shows whether DT-EDNet is better than the comparison networks under plot-grouped validation and which of its modules matter.',
     'Results of the four pseudo-image networks on the six configurations (Step 2.1.5); the best machine-learning model on the same inputs.',
     'Network comparison table; ablation table → conclusions.',
     ['Compare DT-EDNet, EfficientNet, ResNet18, ConvNeXt V2 and the best machine-learning model on the six configurations (overall accuracy, kappa, macro recall, macro-F1, per-class F1, RMSE).',
      'Ablation on the best configuration: DT-EDNet without the squeeze-and-excitation block, without the Dual Transformer Group, and without both.',
      'Report mean ± standard deviation over three folds × five seeds.'],
     'Network comparison and module ablation: Ma et al. (2026).')
TAB('ablationt', [['Model (template)', 'Overall accuracy', 'Kappa', 'Macro recall', 'Macro-F1'], ['DT-EDNet (full)', '…', '…', '…', '…'], ['without squeeze-and-excitation block', '…', '…', '…', '…'], ['without Dual Transformer Group', '…', '…', '…', '…'], ['without both', '…', '…', '…', '…']],
    'Template for the DT-EDNet module ablation (same folds and seeds for all rows).', [3400, 1500, 1300, 1500, 1606])
STEP('2.5.4', 'Shapley additive explanations (SHAP) and selection stability',
     'Shows which features drive the best models and how stable the selected features are.',
     'Best models; selected features of every fold.', 'Feature-importance figures; stability table → Objective 1 discussion.',
     ['Compute SHAP values of the best machine-learning model of each task; summarise the mean |SHAP| per feature and per camera.', 'Count how often every feature is selected over the three folds; final feature lists contain features selected in at least two of three folds.'],
     'Lundberg and Lee (2017); Lundberg et al. (2020); Nogueira et al. (2018).')
CARD('ablation', 'Ablation and Shapley interpretation', 'Ablation removes one part (a camera, a feature group or a network module) and measures the loss; SHAP divides each prediction among the features.',
     'Shows what each camera, feature type and network module contributes.', 'Drop-one-camera from S15; DT-EDNet without SE, without Dual Transformer Group, without both; SHAP on the best machine-learning models.',
     'None.', 'Any trained model on the same folds.',
     'Direct, easy-to-explain evidence of contribution; both used in the DT-EDNet study.', 'Ma et al. (2026); Lundberg and Lee (2017)')

# ---------------------------------------------------------------- 2.6
H2('Activity 2.6 – Robustness and maps')
STEP('2.6.1', 'Performance by treatment',
     'A model may work for one variety or crop age and fail for another.',
     'Test predictions with treatment codes.', 'Treatment-wise metric tables.',
     ['Report the metrics for each variety, inoculation timing and date.'], 'Liu et al. (2024); Blasch et al. (2023); Feng et al. (2022).')
STEP('2.6.2', 'Leave-one-variety-out and leave-one-timing-out tests',
     'Tests whether models transfer to a variety or crop age not seen in training.',
     'Best machine-learning and best deep-learning model of the three best sensor sets.', 'Transfer results → conclusions on robustness.',
     ['Train on two varieties and test on the third (mainly V1 ↔ V2, because the resistant variety has few diseased samples).', 'Train on three inoculation timings and test on the fourth.'],
     'Blocked validation for extrapolation: Roberts et al. (2017); independent-year test: Ma et al. (2026).')
STEP('2.6.3', 'Severity maps',
     'Field users need maps rather than tables.',
     'Best model of each task; subplot features of every date.', 'Subplot maps of detection, severity class and score.',
     ['Apply the best model of each task to all subplots of every date.', 'Map the predicted class and score together with the absolute error where scores exist.'],
     'Abdulridha et al. (2023); Liu et al. (2024); Deng et al. (2024); Liu et al. (2026).')

# =====================================================================================
H1('5. Objective 3 – Prediction of white rust at the pre-symptomatic stage')
P('Objective 3 uses the 576 pre-symptomatic samples of each camera. The question is whether subplots that will develop white rust can be separated from healthy subplots before pustules are visible, and whether their later severity can be predicted. Machine-learning models and the feature-fusion networks (DNN-F1, DNN-F2) are used; the pseudo-image networks are not used here because about 384 training samples per fold are too few for them.')
FIG('obj3', 'g07_obj3.png', 'Flow chart of Objective 3 (Activities 3.1–3.5).', 540)
FIG('obj3time', 'g27_obj3.png', 'Pre-symptomatic and post-symptomatic periods and how pre-symptomatic samples are labelled from the later status of the same subplot.', 520)
H2('Activity 3.1 – Pre-symptomatic samples and labels')
STEP('3.1.1', 'Labels from the later status of each subplot',
     'Before symptoms the visual score is zero everywhere; labels must come from what happens later.',
     'Pre-symptomatic subplot tables; scores of the first post-symptomatic date.', 'Labelled pre-symptomatic dataset → Activity 3.2.',
     ['Classification: healthy = subplots of the 12 healthy plots; infected = inoculated subplots that show pustules later; inoculated subplots that never show symptoms are excluded from the infected class.', 'Regression: target = severity score of the same subplot on the first post-symptomatic date.', 'Record days after inoculation for every sample.'],
     'Zhu et al. (2017); Tian et al. (2021); Mahlein et al. (2019); Yu et al. (2021) for the early stage of pine wilt disease.')
H2('Activity 3.2 – Normalisation to healthy plots')
STEP('3.2.1', 'Healthy-plot normalisation of all features',
     'Early disease changes are small compared with date, weather, variety and crop-age differences.',
     'Pre-symptomatic features; healthy-plot features of the same date and variety (training replications).', 'Healthy-normalised features → Activity 3.3.',
     ['Apply Step E3 to every feature: z_{h} = (x − mean_{healthy}) / SD_{healthy}, with the healthy plots of the same date and variety in the training replications.', 'Apply the same reference to the test samples.'],
     'Oerke et al. (2006); Zarco-Tejada et al. (2018); Calderón et al. (2014); Poblete et al. (2023).')
H2('Activity 3.3 – Pre-symptomatic feature selection')
STEP('3.3.1', 'Selection with the pre-symptomatic labels',
     'Features that respond after symptoms are not necessarily the earliest responders.',
     'Healthy-normalised feature groups (training part).', 'Pre-symptomatic feature sets of each camera and sensor set → Activity 3.4.',
     ['Repeat the one-method-per-type selection with the pre-symptomatic labels: SHAP-CARS for bands, ReliefF for indices (two classes) or RReliefF (later score), mRMR for texture, the TTFI search, the redundancy filter and the variance inflation factor.', 'Fuse the camera sets for the 15 sensor sets and run sequential floating forward selection for the machine-learning models, limited to 10 features because the training part is smaller.'],
     'Tian et al. (2021); Ma et al. (2026); early spectral changes in rusts and mildews: Terentev et al. (2023), Zhu et al. (2017).')
H2('Activity 3.4 – Pre-symptomatic models')
STEP('3.4.1', 'Models for the 15 sensor sets',
     'Detection must be tested for each camera and combination.',
     'Pre-symptomatic feature sets.', 'Trained models and test predictions → Activity 3.5.',
     ['Machine learning: support vector machine, random forest, extreme gradient boosting, k-nearest neighbours and partial least squares, with the grids of Table [[T:mlgrid]].', 'Feature-fusion networks: DNN-F1 and DNN-F2 with smaller layers (32 and 16 units) and stronger dropout (0.4).', 'Same folds as Objective 2.'],
     'Zhu et al. (2017); Tian et al. (2021); Yu et al. (2025); Srivastava et al. (2014).')
H2('Activity 3.5 – Evaluation, earliest detection day and risk maps')
STEP('3.5.1', 'Pre-symptomatic metrics, area under the curve (AUC) and earliest detection day',
     'Shows how early, with which sensor set and with what reliability white rust can be predicted.',
     'Test predictions with days after inoculation.', 'Accuracy tables; earliest detection day of every sensor set.',
     ['Classification: sensitivity, specificity, balanced accuracy and AUC; regression: R² and RMSE of the later score.', 'Compute balanced accuracy separately for each pre-symptomatic date; the earliest detection day is the first date on which it reaches 0.70 (Figure [[F:earliest]]).', 'Report the earliest detection day separately for each variety and inoculation timing.'],
     'Fawcett (2006); Mahlein et al. (2019); Zarco-Tejada et al. (2018).')
FIG('earliest', 'g23_dummy_earliest.png', 'Dummy example of balanced accuracy by days after inoculation and the earliest detection day of each sensor set.', 460)
TAB('earlyex', [['Days after inoculation (dummy)', '3', '6', '9', '12', '15'], ['Hyperspectral + thermal: balanced accuracy', '0.55', '0.62', '0.71', '0.78', '0.81'], ['Red–green–blue: balanced accuracy', '0.45', '0.47', '0.55', '0.65', '0.69']],
    'Worked example (dummy data): the hyperspectral + thermal set reaches 0.70 at 9 days after inoculation (earliest detection day = 9), while the red–green–blue set does not reach it before symptoms.', [3400, 1180, 1180, 1180, 1180, 1186])
CARD('roc', 'Receiver operating characteristic analysis and earliest detection day', 'The receiver operating characteristic curve plots sensitivity against 1 − specificity for all thresholds; its area (AUC) is the probability that an infected sample scores higher than a healthy one. The earliest detection day is the first date on which balanced accuracy reaches a set level.',
     'Measures early-warning ability independently of the class balance and threshold; gives a simple "how early" answer.', 'AUC and balanced accuracy per date; level 0.70.',
     'Level 0.70 (fixed in advance; 0.65 and 0.75 reported as checks).', 'Binary early-warning problems with unequal classes.',
     'Standard for early detection and comparable with published earliest-detection studies.', 'Fawcett (2006); Mahlein et al. (2019)')
STEP('3.5.2', 'Risk maps',
     'Early warnings are useful only if they show where to act.',
     'Best pre-symptomatic model; subplot features of each pre-symptomatic date.', 'Maps of the predicted infection probability of every subplot.',
     ['Map the predicted probability of later infection for every subplot and pre-symptomatic date.', 'Compare the maps with the later observed severity.'],
     'Zarco-Tejada et al. (2018); Yu et al. (2025).')
