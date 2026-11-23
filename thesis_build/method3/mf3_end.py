# Cross-check, definitions, plan, software, questions (executed inside mf3_body.py)
# =====================================================================================
H1('6. Cross-check of the methodology')
P('This chapter checks that no step is missing, that every output is used by a later step, and that the methodology agrees with the feature-selection approach note for multi-sensor UAV data and with the DT-EDNet study (Ma et al., 2026). Where the methodology deliberately differs, the reason is given.')
H2('6.1 Input–output chain of all steps')
TAB('chain', [['Step(s)', 'Input', 'Output', 'Used by'],
 ['A1–A3, A5', 'field design, scores', 'labelled subplot list; post- and pre-symptomatic datasets', 'D8, F1, all objectives'],
 ['A4', 'tagged plants, ASD spectroradiometer', 'leaf spectra with leaf grades and metadata', 'separate leaf-level analysis (not part of this document)'], ['A9', 'glasshouse pots, inoculum', 'pot-level severity (0–6) and leaf spectra under controlled conditions', 'characterisation under controlled conditions (Objective 1)'],
 ['A8', 'designated subplots, laboratory and field instruments', 'biochemical and biophysical parameters (48 plots × 4 dates)', '1.7, 1.8, 3.1.2'],
 ['A7', 'Bharatpur research farms and farmers\' fields', 'independent test dataset (images, disease index, covariates)', '2.7, 3.5.4'],
 ['A6', 'field book, weather records', 'covariate table (days after inoculation, variety, timing, growth stage, weather)', 'D2, 1.1.3, 2.5.5, 3.5.3'],
 ['B1–B2', 'raw images, panels, control points', 'calibrated, georeferenced mosaics', 'B3, B4'],
 ['B3', 'hyperspectral cube', 'clean, smoothed 483-band cube', 'B4, C1, D3'],
 ['B4–B5', 'mosaics of all cameras', 'aligned layers on the hyperspectral grid', 'C6–C8, D2'],
 ['C1–C5', 'pixel samples of all dates', 'labelled endmember library', 'C6'],
 ['C6–C8', 'library, cubes, NDVI', 'accepted vegetation mask applied to all cameras', 'D2, D5'],
 ['D1–D2', 'masked layers, polygons', 'subplot mean spectra and band values joined with covariates', 'D3–D7'],
 ['D3–D7', 'subplot values', 'spectral, index, texture, colour and thermal groups', 'D8, E1'],
 ['D8', 'all features', 'feature table of each camera', 'E, F, Objective 1'],
 ['E1', 'temperatures', 'normalised thermal features', 'D7, Objective 1'],
 ['E2', 'features, healthy plots (rotated across folds)', 'healthy-normalised features', 'Objective 3; thermal difference features'],
 ['E3–E4', 'feature tables', 'standardised features; class weights', 'all models'],
 ['F1–F3', 'labelled tables', 'outer and inner folds with rotated healthy plots; tuning plan; leakage checklist', 'E2, Objectives 2–3'],
 ['1.1.1–1.1.3', 'post-symptomatic features', 'response figures', 'interpretation, 1.6.3'],
 ['1.2.1–1.2.4', 'reflectance and first derivative', 'effective ranges; optimal wavelengths', '1.3, 1.6.2, 2.1.5'],
 ['1.3.1–1.3.3', 'NDSI/RSI maps, bands', 'best NDSI, RSI, White Rust Index; multispectral indices', '1.4.1, 1.6.1'],
 ['1.4.1–1.4.3', 'index group', 'selected indices', '1.6.2, 2.1.5'],
 ['1.5.1–1.5.4', 'principal-component texture', 'selected texture features; best TTFI', '1.6.2, 2.1.5'],
 ['1.6.1–1.6.4', 'survivors of all groups', 'disease-specific feature set of each camera', '2.1.2, 3.3.1'],
 ['1.7.1–1.7.6', 'biochemical and biophysical parameters; camera features', 'disease effect by date and stage; parameter–feature links', 'interpretation of Objectives 1–3; 2.5.4'], ['1.8.1–1.8.5', '576 pre-symptomatic samples; later status; physiology of 7 January', 'pre-symptomatic response; earliest-responding features; pre-symptomatic feature set', '3.3.1, 3.1.2'],
 ['2.1.1–2.1.5', 'feature sets, folds', 'task labels; fused sets of 15 sensor sets; six hyperspectral configurations', '2.2, 2.3'],
 ['2.2.1–2.2.6', 'optimum feature combinations', 'tuned machine-learning predictions', '2.4'],
 ['2.3.1–2.3.8', 'fused sets; pseudo-images', 'neural-network predictions', '2.4'],
 ['2.4.1–2.4.3', 'predictions', 'metric tables', '2.5'],
 ['2.5.1–2.5.5', 'metric tables, models, covariates', 'best sensor set and model; contributions; ablation; explanation; gain over the covariate baseline', '2.6, conclusions'],
 ['2.6.1–2.6.3', 'best models', 'robustness results; maps', 'conclusions'],
 ['2.7.1–2.7.4', 'all IARI data; Bharatpur data', 'frozen final models; independent test accuracy; farm maps', 'conclusions'],
 ['3.1.1–3.5.2', 'pre-symptomatic features, later labels', 'pre-symptomatic models; earliest detection day; risk maps', 'conclusions']],
 'Input and output of every step and the step that uses each output.', [1300, 2700, 3400, 1906], 15)
P('**Result of the check.** Every output is used by at least one later step, every input is produced by an earlier step, and every label-based step runs inside the training folds ([[T:leak]]). No step is missing between the raw images and the three objectives.')
H2('6.2 Agreement with the feature-selection approach note')
TAB('fscheck', [['Recommendation of the note', 'In this methodology', 'Status'],
 ['Do not select from one big pool; select in stages, group by group', 'four stages; one method per feature type ([[T:stages]])', 'included'],
 ['Stage 0: build groups with physical meaning; red-edge parameters instead of all derivative bands', 'Activity D; red-edge parameters added; second derivative removed', 'included (second derivative removed on request)'],
 ['Stage 1: remove near-constant features; keep one per cluster with |r| > 0.95', 'Steps 1.4.2, 1.5.2, 1.6.1; spectral bands go directly to SHAP-CARS, which handles collinearity', 'included (adapted for bands)'],
 ['Stage 2: SPA or CARS for spectra; Boruta or RReliefF for indices; mRMR for texture; two-band search on training plots', 'SHAP-CARS for spectra; ReliefF/RReliefF for indices; mRMR for texture; NDSI/RSI and White Rust Index search in the inner folds', 'included (one method per type, as in Ma et al., 2026)'],
 ['Stage 3: variance inflation factor below 5 or 10', 'below 10 (5 as a check)', 'included'],
 ['Stage 4: final selection by floating forward selection or elastic net', 'sequential floating forward selection for machine learning, at most 15 features (10 for Objective 3)', 'included'],
 ['Every label-based step inside the training folds; folds grouped by plot', 'nested, leave-one-replication-out folds grouped by plot', 'included'],
 ['Limit the final number of features (about n/10 to n/20)', '15 features for about 1280 training samples (10 for about 384)', 'included'],
 ['Check stability of selection', 'CARS repeated 20 times; selection frequency over folds (Step 2.5.4)', 'included'],
 ['Ablation by group and by camera', 'drop-one-camera, six hyperspectral configurations, DT-EDNet module ablation', 'included'],
 ['Normalise thermal values against healthy plots or air temperature on each date', 'Steps E1 and E2', 'included'],
 ['Outer loop of 5 folds repeated 10 times', 'three leave-one-replication-out folds (replication is the natural block of the design); five seeds for networks', 'adapted'],
 ['Compare with decision-level fusion (stacking)', 'not done: the study is limited to feature-level fusion by design', 'not used (scope)']],
 'Cross-check against the feature-selection approach note for multi-sensor UAV data.', [3500, 4200, 1606], 15)
H2('6.3 Agreement with the DT-EDNet study (Ma et al., 2026)')
TAB('dtcheck', [['Step of Ma et al. (2026)', 'In this methodology', 'Difference and reason'],
 ['Spectral response by severity level', 'Step 1.1.1', 'same'],
 ['NDSI and RSI R² contour maps; effective ranges with R² > 0.5', 'Step 1.2.1', 'whole usable range 400–2400 nm instead of 450–1000 nm (both cameras of the Headwall imager are available)'],
 ['Band selection by RFE-SHAP, SAND and SHAP-CARS; SHAP-CARS chosen', 'Steps 1.2.2–1.2.4 (SHAP-CARS only)', 'one method per type, as requested; SHAP-CARS was the best in the study; stability rule added'],
 ['Vegetation index selection with Relief (top five)', 'Steps 1.4.2–1.4.3 (ReliefF / RReliefF)', 'ReliefF handles several classes; RReliefF for the score'],
 ['Principal components (> 95%) → GLCM texture (8 measures × 3 components) → mRMR (top six)', 'Steps 1.5.1–1.5.3', 'same, plus a label-free redundancy filter'],
 ['TTFI from ordered triplets, three formulas; best by correlation', 'Step 1.5.4', 'same'],
 ['DT-EDNet: pseudo-2D input, 3 × 3 embedding (128), SE, class token, 1 KTB with CBAM + 4 TTB, 4 heads, dropout 0.03', 'Steps 2.3.3–2.3.4', 'same; regression head added for the severity score'],
 ['EfficientNet, ResNet18, ConvNeXt V2 with identical settings', 'Steps 2.3.5–2.3.7', 'same; stems with stride 1 for small inputs'],
 ['AdamW 6 × 10⁻⁴, weight decay 10⁻⁵, cosine to 10⁻⁶, 300 epochs, batch 32, label smoothing 0.01, clipping 1.2, early stopping 60, seed 42', 'Step 2.3.8', 'same; five seeds and a small tuning grid; selection on validation plots'],
 ['Random 7:3 split with 10% validation; independent-year test', 'leave-one-replication-out folds grouped by plot (Step F1)', 'random splits put subplots of one plot on both sides and inflate accuracy'],
 ['Single and combined feature inputs (OW, VI, TF, TTFI; OW + VI, OW + TTFI, OW + VI + TTFI)', 'Step 2.1.5 (six configurations)', 'TTFI alone (one feature) is not given to the networks; it is assessed in Objective 1'],
 ['Ablation without SE, without DTG, without both', 'Step 2.5.3', 'same'],
 ['Metrics: overall accuracy, kappa, macro recall, macro-F1, per-class scores', 'Step 2.4.1', 'same, plus weighted kappa, AUC and regression metrics']],
 'Cross-check against the DT-EDNet study.', [3300, 2500, 3506], 15)
H2('6.4 Changes from the previous version of the methodology')
TAB('changes', [['Item', 'Previous version', 'This version', 'Reason'],
 ['Second derivative', 'used', 'removed', 'noise amplification; user request'],
 ['Band selection', 'correlation scalogram + ReliefF', 'NDSI/RSI effective ranges → SHAP-CARS', 'one method per type; best method in Ma et al. (2026)'],
 ['Vegetation index selection', 'Boruta', 'ReliefF / RReliefF', 'one method per type; Relief used for indices by Ma et al. (2026)'],
 ['Hyperspectral texture', 'not specified for the cube', 'principal-component texture → mRMR → TTFI', 'Guo et al. (2021); Ma et al. (2026)'],
 ['Response tests', 'analysis of variance and Tukey test', 'correlation and response curves', 'fewer statistics; simpler presentation'],
 ['Deep learning (post-symptomatic)', 'DNN-F1, DNN-F2', 'DNN-F1, DNN-F2 + DT-EDNet, EfficientNet, ResNet18, ConvNeXt V2', 'user request; comparison of Ma et al. (2026)'],
 ['Normalisation', 'inside other steps', 'separate Activity E (six steps)', 'clarity; user request'],
 ['Endmember extraction', 'one step', 'Activity C with eight steps', 'clarity; user request'],
 ['Biochemical and biophysical parameters', 'not included', 'Step A8 and Activity 1.7: 11 parameters on 4 dates with paired comparisons, analysis of variance, growth-stage comparison and parameter–feature correlations', 'user request; physiological basis'],
 ['Validation and testing', 'IARI field only', 'internal validation on the IARI field (nested leave-one-replication-out) and independent testing on Bharatpur research farms and farmers\' fields with frozen models', 'user request; transferability'],
 ['Field calendar (revision 5)', 'sowing at 8-day intervals; inoculation 10 January 2027; flights 12 January – 25 March', 'sowing 19 Nov, 26 Nov, 3 Dec, 10 Dec 2026 (7-day interval); inoculation 30 December 2026 (crop age 41, 34, 27, 20 days); flights 1 January – 15 March 2027; physiology 7 Jan, 18 Jan, 8 Feb, 1 Mar', 'field schedule of the researcher'],
 ['Severity label (revision 5)', 'canopy grade of the subplot (0–9)', 'disease index of the subplot from leaves graded at the centre and four corners (Liu et al., 2024); DI classes 0, 1, 3, 5, 7, 9; Task C = DI (%); staghead severity recorded', 'researcher\'s scoring protocol'],
 ['Pre-symptomatic characterisation (revision 5)', 'only in Objective 3 (prediction)', 'Activity 1.8: characterisation of the 576 pre-symptomatic samples per camera in Objective 1', 'user request'],
 ['Published indices (revision 5)', 'about 48, partly listed', '48 indices (39 base + 9 SWIR) and 3 red-edge parameters with formulas, original references and recent disease-sensing studies', 'user request'],
 ['Covariate baseline (revision 5)', 'best machine-learning model on covariates', 'interpretable model B1 and machine-learning model B2; M0/M1/M2; gains ΔS, ΔC, ΔT with plot-block bootstrap and DeLong test; real-gain rule; inoculated plots only; no look-ahead', 'leakage-free evaluation of what the cameras add'],
 ['Glasshouse experiment (revision 5)', 'not included', 'Step A9: 48-pot experiment with the same varieties and four sowing dates', 'user request; lab and field characterisation'],
 ['Leaf spectra', 'not collected', 'ASD leaf spectra of L3, L5 and LL from 3 plants per subplot on every flight date (acquisition only)', 'user request; leaf–canopy link'],
 ['Covariates', 'flower %, canopy cover %, vegetation pixel count', 'days after inoculation, variety, inoculation timing, growth stage, weather', 'user request; covariate baseline'],
 ['Radiometric consistency between dates; sample quality screening', 'Steps E1 and E4', 'not performed', 'user request; panels on every flight (Step B1)'],
 ['Varieties', 'V1 susceptible, V2 moderately susceptible, V3 resistant (assumed)', 'V1 PM 26, V2 Pusa Vijay, V3 PM 37 (no susceptibility assumed)', 'field record'],
 ['Technique descriptions', 'short', 'method card for every technique', 'user request']],
 'Main changes in this revision.', [2000, 2300, 2900, 2106], 15)

# =====================================================================================
H2('6.5 Drawbacks found and corrected in this version')
TAB('drawbacks', [['Drawback in the previous version', 'Correction', 'Supporting studies'],
 ['Healthy plots were assigned to folds by variety (V1 → fold 1, …), so the training part of each fold had no healthy plots of the test variety. Healthy-plot normalisation with the same variety was then impossible, and healthy samples of the test variety were never seen in training.', 'Healthy plots rotated across folds: every fold has each inoculation timing once and every variety at least once ([[T:healthyrot]]).', 'Roberts et al. (2017); Oerke et al. (2006); Zarco-Tejada et al. (2018)'],
 ['Severity rises with time and stage, so a model could appear accurate by learning days after inoculation or growth stage instead of disease.', 'Covariate-only baseline and sensor + covariate models (Steps 2.5.5 and 3.5.3); results by growth stage.', 'Zhang et al. (2014); Blasch et al. (2023); Kuhn and Johnson (2013)'],
 ['Flowering effects were checked with flower %, which mixes flowers with disease-related colour changes.', 'Growth stage recorded with the BBCH scale; responses and results reported for each stage.', 'Lancashire et al. (1991); Meier (2018); Sulik and Long (2016)'],
 ['Pooled reflectance and first-derivative bands in CARS without standardisation would favour one form for numerical reasons; the effective ranges could miss the red edge.', 'Bands standardised before PLS; red-edge first derivative always kept; bands labelled R_{λ} or FD_{λ}.', 'Li et al. (2009); Mehmood et al. (2012); Filella and Peñuelas (1994); Yu et al. (2021)'],
 ['Multi-camera pseudo-images could split a small camera group (thermal) across rows.', 'Each camera starts on a new row of the pseudo-image.', 'Sharma et al. (2019); Ma et al. (2026)'],
 ['Tuning every network for every case needed about 34 000 runs.', 'Tune once (fold 1, S15, Task B, one seed) and reuse the settings: about 3800 runs.', 'Ma et al. (2026); Cawley and Talbot (2010)'],
 ['Weather has one value per date and cannot be separated from the date in one season.', 'Weather used for interpretation and in covariate models labelled "within-season".', 'Zhang et al. (2014); Chattopadhyay et al. (2011)'],
 ['A variety was assumed to be resistant without field evidence.', 'Variety names from the field record; transfer test run for each variety in turn.', 'Blasch et al. (2023)'],
 ['The healthy plots lie in a separate block, so healthy vs inoculated differences can include a small block (location) effect.', 'Detection labels come from the observed score, so inoculated subplots with no pustules are also healthy samples; detection accuracy is reported separately for healthy-block samples and for symptom-free inoculated subplots; healthy-plot normalisation is done by date.', 'Roberts et al. (2017); Oerke et al. (2006)'],
 ['All results came from one site and one season.', 'Independent testing with frozen models on research-farm and farmers\' field data at Bharatpur (Activity 2.7); leave-one-variety-out and leave-one-timing-out tests kept as internal transfer tests; transfer to other seasons still to be tested.', 'Ma et al. (2026); Roberts et al. (2017); Ploton et al. (2020)']],
 'Drawbacks of the previous version and how they are corrected.', [3500, 3500, 2306], 15)

H1('7. Definitions of indices and features')
H = [['Group', 'Index', 'Formula', 'Original reference'],
 ['Greenness and canopy structure (17)', 'NDVI780', '(R_{780} − R_{670})/(R_{780} + R_{670})', 'Raun et al. 2001'], ['', 'NDVI850', '(R_{850} − R_{650})/(R_{850} + R_{650})', 'Raun et al. 2001'], ['', 'NDVI761', '(R_{761} − R_{651})/(R_{761} + R_{651})', 'Raun et al. 2001'],
 ['', 'SR900', 'R_{900}/R_{680}', 'Jordan 1969'], ['', 'SR850', 'R_{850}/R_{680}', 'Jordan 1969'], ['', 'SR761', 'R_{761}/R_{651}', 'Jordan 1969'], ['', 'GNDVI', '(R_{850} − R_{550})/(R_{850} + R_{550})', 'Gitelson et al. 1996'],
 ['', 'RDVI', '(R_{800} − R_{670})/√(R_{800} + R_{670})', 'Roujean and Bréon 1995'], ['', 'MSR', '(R_{800}/R_{670} − 1)/√(R_{800}/R_{670} + 1)', 'Chen 1996'], ['', 'TVI', '0.5[120(R_{750} − R_{550}) − 200(R_{670} − R_{550})]', 'Broge and Leblanc 2001'],
 ['', 'MTVI1', '1.2[1.2(R_{800} − R_{550}) − 2.5(R_{670} − R_{550})]', 'Haboudane et al. 2004'], ['', 'MTVI2', '1.5[1.2(R_{800} − R_{550}) − 2.5(R_{670} − R_{550})] / √[(2R_{800} + 1)^{2} − (6R_{800} − 5√R_{670}) − 0.5]', 'Haboudane et al. 2004'],
 ['', 'MCARI1', '1.2[2.5(R_{800} − R_{670}) − 1.3(R_{800} − R_{550})]', 'Haboudane et al. 2004'], ['', 'TCARI', '3[(R_{700} − R_{670}) − 0.2(R_{700} − R_{550})(R_{700}/R_{670})]', 'Haboudane et al. 2002'],
 ['', 'VIgreen', '(R_{550} − R_{670})/(R_{550} + R_{670})', 'Gitelson et al. 2002'], ['', 'GI', 'R_{554}/R_{677}', 'Guo et al. 2021'], ['', 'RR', '1/R_{700}', 'Mustafa et al. 2023'],
 ['Pigment ratios (12)', 'PSSRa; PSSRb; PSSRc', 'R_{800}/R_{680};  R_{800}/R_{635};  R_{800}/R_{470}', 'Blackburn 1998'], ['', 'RARSa; RARSb; RARSc', 'R_{675}/R_{700};  R_{675}/(R_{700} × R_{650});  R_{760}/R_{500}', 'Chappelle et al. 1992'],
 ['', 'SIPI', '(R_{800} − R_{445})/(R_{800} − R_{680})', 'Peñuelas et al. 1995'], ['', 'NPCI', '(R_{680} − R_{430})/(R_{680} + R_{430})', 'Peñuelas et al. 1994'], ['', 'PSRI', '(R_{680} − R_{500})/R_{750}', 'Merzlyak et al. 1999'],
 ['', 'ARI', '1/R_{550} − 1/R_{700}', 'Gitelson et al. 2001'], ['', 'PPR', '(R_{550} − R_{450})/(R_{550} + R_{450})', 'Metternicht 2003'], ['', 'NRI', '(R_{570} − R_{670})/(R_{570} + R_{670})', 'Bausch and Duke 1996'],
 ['Photosynthesis and stress (4)', 'PRI', '(R_{531} − R_{570})/(R_{531} + R_{570})', 'Gamon et al. 1992'], ['', 'NPQI', '(R_{415} − R_{435})/(R_{415} + R_{435})', 'Barnes et al. 1992'], ['', 'RVSI', '(R_{712} + R_{752})/2 − R_{732}', 'Merton and Huntington 1999'],
 ['', 'HI (healthy index)', '(R_{534} − R_{698})/(R_{534} + R_{698}) − 0.5 R_{704}', 'Mahlein et al. 2013'],
 ['Water (3)', 'WI', 'R_{900}/R_{970}', 'Peñuelas et al. 1997'], ['', 'WI/NDVI', '(R_{900}/R_{970})/NDVI', 'Peñuelas et al. 1997'], ['', 'NWI-2', '(R_{970} − R_{850})/(R_{970} + R_{850})', 'Babar et al. 2006'],
 ['SWIR disease–water (3 base)', 'DWSI-1', 'R_{800}/R_{1660}', 'Apan et al. 2004'], ['', 'DWSI-4', 'R_{550}/R_{680}', 'Apan et al. 2004'], ['', 'ROTI', 'R_{1175}/(R_{1982} + R_{691})', 'Bhattacharya and Chattopadhyay 2013']]
H2T = [['Group', 'Index', 'Formula', 'Original reference'],
 ['SWIR disease indices (9)', 'DWSI-2; DWSI-3', 'R_{1660}/R_{550};  R_{1660}/R_{680}', 'Apan et al. 2004'], ['', 'DWSI-5', '(R_{800} + R_{550})/(R_{1660} + R_{680})', 'Apan et al. 2004'],
 ['', 'NDWI', '(R_{860} − R_{1240})/(R_{860} + R_{1240})', 'Gao 1996'], ['', 'Moisture stress index (MSI)', 'R_{1600}/R_{820}', 'Hunt and Rock 1989'], ['', 'NDII', '(R_{819} − R_{1649})/(R_{819} + R_{1649})', 'Hardisky et al. 1983'],
 ['', 'RBI_{M}; NDBI', 'R_{1148}/R_{1301};  (R_{1148} − R_{1301})/(R_{1148} + R_{1301})', 'Mandal et al. 2023'], ['', 'RBI_{R}', 'R_{1068}/R_{1560}', 'Ramalingam et al. 2026'],
 ['Red-edge parameters (3; 680–760 nm)', 'REP', 'wavelength of the maximum first derivative', 'Horler et al. 1983; Cho and Skidmore 2006'], ['', 'D_{r}', 'maximum first derivative (red-edge amplitude)', 'Filella and Peñuelas 1994'], ['', 'SD_{r}', 'sum of the first derivative over 680–760 nm (area)', 'Filella and Peñuelas 1994'],
 ['Data-driven (Activity 1.3)', 'NDSI, RSI, WRI', 'best pair NDSI(λ_{1}, λ_{2}), RSI(λ_{1}, λ_{2}); WRI = NDSI(λ_{1}, λ_{2}) + w R_{λ3}', 'Ma et al. 2026; Mahlein et al. 2013 (method)']]
P('R_{λ} is the reflectance at λ nm (nearest available band). The 48 published hyperspectral indices are the 39 base indices of [[T:hsidx]] and the 9 SWIR disease indices of [[T:hsidx2]]; formulas were checked against the original papers, and the original reference of every index is kept. Indices that need a band removed in quality control (Step B3) are computed only if the band passes the noise check.')
TAB('hsidx', H, 'The 39 base hyperspectral indices with formulas and original references. Disease-sensing studies of the last 20 years (2006–2026) that used these index groups: Zhang et al. (2012b), Mahlein et al. (2013), Ashourloo et al. (2014), Guo et al. (2021), Mustafa et al. (2023).', [1900, 1700, 3906, 1800], 15)
TAB('hsidx2', H2T, 'The 9 SWIR disease indices (completing the 48 published indices), the 3 red-edge parameters and the data-driven indices. Disease-sensing studies of the last 20 years that used these index groups: Bhattacharya and Chattopadhyay (2013), Zarco-Tejada et al. (2018), Yu et al. (2018), Mandal et al. (2023), Ramalingam et al. (2026).', [1900, 1700, 3906, 1800], 15)
ms = [['Feature', 'Formula (B, G, R, RE, NIR = 475, 560, 668, 717, 840 nm)', 'Reference'], ['Band reflectance (5)', 'subplot mean reflectance of B, G, R, RE, NIR', 'Liu et al. 2024'],
      ['NDVI', '(NIR − R)/(NIR + R)', 'Rouse et al. 1974'], ['GNDVI', '(NIR − G)/(NIR + G)', 'Gitelson et al. 1996'], ['NDRE', '(NIR − RE)/(NIR + RE)', 'Gitelson and Merzlyak 1994'], ['CI_{green}', 'NIR/G − 1', 'Gitelson et al. 2003'], ['CI_{rededge}', 'NIR/RE − 1', 'Gitelson et al. 2003'],
      ['MTCI', '(NIR − RE)/(RE − R)', 'Dash and Curran 2004'], ['OSAVI', '1.16(NIR − R)/(NIR + R + 0.16)', 'Rondeaux et al. 1996'], ['SAVI', '1.5(NIR − R)/(NIR + R + 0.5)', 'Huete 1988'], ['TCARI', '3[(RE − R) − 0.2(RE − G)(RE/R)]', 'Haboudane et al. 2002'],
      ['MCARI', '[(RE − R) − 0.2(RE − G)](RE/R)', 'Daughtry et al. 2000'], ['MSR', '(NIR/R − 1)/√(NIR/R + 1)', 'Chen 1996'], ['PSRI', '(R − G)/NIR', 'Merzlyak et al. 1999'], ['Normalised differences (10)', '(B_{i} − B_{j})/(B_{i} + B_{j}) for all band pairs', 'Ma et al. 2026'],
      ['Texture (40)', '8 GLCM measures ([[T:rgbfeat]]) of each of the 5 bands', 'Haralick et al. 1973; Liu et al. 2024']]
TAB('msidx', ms, 'Multispectral features.', [2200, 4800, 2306], 15)
rgb = [['Feature', 'Equation', 'Reference'], ['Chromatic coordinates', 'r = R/(R+G+B), g = G/(R+G+B), b = B/(R+G+B)', 'Woebbecke et al. 1995'], ['Excess green (ExG)', '2g − r − b', 'Woebbecke et al. 1995'], ['Excess red (ExR)', '1.4r − g', 'Meyer and Neto 2008'], ['ExG − ExR', 'ExG − ExR', 'Meyer and Neto 2008'],
       ['VARI', '(G − R)/(G + R − B)', 'Gitelson et al. 2002'], ['GLI', '(2G − R − B)/(2G + R + B)', 'Louhaichi et al. 2001'], ['NGRDI', '(G − R)/(G + R)', 'Tucker 1979'], ['Hue, saturation, value (3)', 'mean of vegetation pixels', '—'],
       ['Mean (MEA)', 'Σ_{i} Σ_{j} i P(i, j)', 'Haralick et al. 1973'], ['Variance (VAR)', 'Σ_{i} Σ_{j} (i − μ)^{2} P(i, j)', 'Haralick et al. 1973'], ['Homogeneity (HOM)', 'Σ_{i} Σ_{j} P(i, j) / [1 + (i − j)^{2}]', 'Haralick et al. 1973'], ['Contrast (CON)', 'Σ_{i} Σ_{j} (i − j)^{2} P(i, j)', 'Haralick et al. 1973'],
       ['Dissimilarity (DIS)', 'Σ_{i} Σ_{j} |i − j| P(i, j)', 'Haralick et al. 1973'], ['Entropy (ENT)', '− Σ_{i} Σ_{j} P(i, j) ln P(i, j)', 'Haralick et al. 1973'], ['Second moment (SEC)', 'Σ_{i} Σ_{j} P(i, j)^{2}', 'Haralick et al. 1973'], ['Correlation (COR)', 'Σ_{i} Σ_{j} (i − μ_{i})(j − μ_{j}) P(i, j) / (σ_{i} σ_{j})', 'Haralick et al. 1973']]
TAB('rgbfeat', rgb, 'Colour indices and grey-level co-occurrence matrix (GLCM) texture measures. P(i, j) is the normalised frequency of grey levels i and j in neighbouring pixels.', [2300, 4700, 2306], 15)
tir = [['Feature', 'Definition', 'Reference'], ['Canopy temperature statistics (5)', 'mean, median, standard deviation, 10th and 90th percentile of vegetation-pixel temperature', 'Liu et al. 2024'], ['Canopy minus air temperature (CTD)', 'T_{c} − T_{air}', 'Calderón et al. 2014'],
       ['Normalised relative canopy temperature (NRCT)', '(T_{c} − T_{min})/(T_{max} − T_{min}) over the field on that date', 'Elsayed et al. 2017'], ['Difference from healthy plots (ΔT)', 'T_{c} − mean T_{c} of the healthy plots of the same date and variety', 'Oerke et al. 2006'],
       ['Crop water stress index (CWSI)', '(T_{c} − T_{wet})/(T_{dry} − T_{wet})', 'Idso et al. 1981; Jones et al. 2009'], ['Thermal texture (8)', 'GLCM measures of the temperature image quantised over one common range', 'Haralick et al. 1973']]
TAB('tirfeat', tir, 'Thermal features.', [2800, 4300, 2206], 15)

# =====================================================================================
H1('8. Six-month work plan')
FIG('gantt', 'g24_gantt.png', 'Six-month work plan for the analysis.', 540)
TAB('plan', [['Month', 'Work', 'Deliverable'], ['1', 'Common Activities A–C for all dates and cameras; mask accuracy', 'calibrated, masked images; endmember library'],
    ['2', 'Activities D–F: features, covariates, normalisation, folds; Activity 1.1', 'feature and covariate tables; response curves'], ['3', 'Activities 1.2–1.8; selection code tested inside folds; pre-symptomatic characterisation; analysis of the biochemical and biophysical parameters', 'optimal wavelengths, White Rust Index, selected indices, TTFI; pre-symptomatic feature set; Objective 1 draft'],
    ['4', 'Objective 2: machine learning and feature-fusion networks for 15 sensor sets', 'results of 15 sensor sets'], ['5', 'Objective 2: DT-EDNet and comparison networks; ablation; Shapley explanation; maps', 'network comparison; ablation; maps'],
    ['6', 'Objective 3; independent testing at Bharatpur (Activity 2.7); glasshouse data; synthesis and writing', 'earliest detection day; risk maps; independent test results; thesis chapters']], 'Month-wise plan.', [1000, 5000, 3306])
NOTE('Computing load: 15 sensor sets × 3 tasks × 3 folds × 5 machine-learning models with floating forward selection; two feature-fusion networks and four pseudo-image networks × 5 seeds. Run the selection of each camera once per fold and reuse it for all combinations, and train the networks on a graphics processing unit.')

# =====================================================================================
H1('9. Software and reproducibility')
TAB('software', [['Task', 'Software'], ['Image processing, registration, resampling, masks', 'ENVI or Python (GDAL, rasterio); hourglass notebook (minimum noise fraction, pixel purity index, n-dimensional visualisation, spectral angle mapper)'],
    ['Features, selection, machine learning', 'Python: numpy, pandas, scikit-learn (Pedregosa et al., 2011), xgboost (Chen and Guestrin, 2016), shap (Lundberg and Lee, 2017), ReliefF, mRMR, mlxtend floating selection (Raschka, 2018)'],
    ['Deep learning', 'PyTorch (Paszke et al., 2019)']], 'Software used.', [3300, 6006])
BL(['Fix random seeds; store the outer and inner folds as files and reuse them for all sensor sets and models.', 'Log every setting (bands removed, mask threshold, selected features per fold, hyper-parameters, seeds).', 'Keep raw, intermediate and final tables separate and versioned.'])

# =====================================================================================
H1('10. Questions expected in the interview')
for q, a in [('Why one feature-selection method for each type of feature?', 'Each type has a different nature: spectral bands are many and collinear (SHAP-CARS is designed for this), indices are fewer but must separate overlapping classes (ReliefF), and texture features are correlated with each other (mRMR balances relevance and redundancy). One method per type keeps the procedure simple and follows Ma et al. (2026).'),
    ('Why is the second derivative not used?', 'Derivatives amplify noise; at UAV signal-to-noise levels the second derivative adds hundreds of unstable variables (Rinnan et al., 2009). The red-edge parameters from the first derivative keep the useful information (Yu et al., 2021).'),
    ('Why are texture features computed on principal components?', 'Texture of 483 bands would be highly redundant; the first three components keep more than 95% of the variance, as in Guo et al. (2021) and Ma et al. (2026).'),
    ('What is the Tri-band Texture Fusion Index?', 'A combination of three selected texture features in sums, products and ratios; in rice blast it was more strongly related to disease than any single texture feature (Ma et al., 2026).'),
    ('Why compare DT-EDNet with EfficientNet, ResNet18 and ConvNeXt V2?', 'These were the comparison networks of the DT-EDNet study; repeating the comparison under plot-grouped validation shows whether its advantage holds for white rust when accuracy is not inflated by random splits.'),
    ('Is the dataset large enough for a transformer?', 'About 1280 training samples per fold is small for a transformer, which is why identical folds, early stopping, a small tuning grid, five seeds and strong machine-learning baselines are used; the pseudo-image networks are not used for the smaller pre-symptomatic dataset.'),
    ('Why are the folds grouped by replication?', 'Subplots of a plot and plots of a replication are similar; random splits put near-identical samples in training and test data and inflate accuracy (Roberts et al., 2017; Ploton et al., 2020).'),
    ('Why are flowers kept in the subplot spectrum?', 'The disease survey includes the inflorescence and staghead; the growth stage (vegetative, flowering, pod formation) is recorded with the BBCH scale and results are reported for each stage, so that selected features are not only flowering effects (Sulik and Long, 2016; Meier, 2018).'),
    ('How are weather and other covariates used?', 'Days after inoculation, variety, inoculation timing, growth stage and weather form a covariate-only baseline; a camera is useful only if it beats this baseline. Weather has one value per date, so models that contain it are labelled within-season (Zhang et al., 2014; Chattopadhyay et al., 2011).'),
    ('How is pre-symptomatic infection known if no symptoms are visible?', 'From the later status of the same subplot; inoculated subplots that never develop symptoms are excluded (Zhu et al., 2017; Tian et al., 2021). The same labels are used to characterise the pre-symptomatic response in Activity 1.8 and to build the prediction models of Objective 3.'),
    ('How is severity measured?', 'Leaves at the centre and four corners of each subplot are graded 0–9 and combined into the disease index DI = Σ(x × f) / (9 × Σf) × 100 (Liu et al., 2024); DI = 0 gives the healthy label, the DI range gives the class (0, 1, 3, 5, 7, 9) and the DI itself is the regression target.'),
    ('What do the covariate models show?', 'An interpretable model (logistic, ordinal logistic or linear) and the best machine-learning model are fitted on covariates only; the cameras are credited only with their gain over the stronger of the two, tested with a plot-block bootstrap and the DeLong test (Efron and Tibshirani, 1993; DeLong et al., 1988).'),
    ('Why are the biochemical and biophysical parameters measured at plot level?', 'The plot is the experimental unit of the randomised block design (Hurlbert, 1984). One designated subplot per plot keeps the gas-exchange readings inside the mid-morning window and links each sample to the UAV features of that subplot; the parameters explain the camera responses and are not model inputs (Calderón et al., 2013).'),
    ('How do you know the models work outside the IARI field?', 'The models are validated by leave-one-replication-out inside the IARI field, where they are chosen and assessed; then the frozen final models are tested once on independent research-farm and farmers\' field data from Bharatpur with natural infection (independent testing, not validation), as the DT-EDNet study did with an independent naturally infected dataset (Ma et al., 2026; Ploton et al., 2020).'),
    ('How can these results be used with satellite data?', 'The selected wavelengths and indices can be simulated for Sentinel-2 or LISS-IV bands from the hyperspectral spectra, as done for yellow rust and rice bacterial leaf blight (Zheng et al., 2018; Das et al., 2015).')]:
    P('**Q. ' + q + '** ' + a)
