from c_lib import *


def add():
    h1('6. Objective 1 – Characterisation of white rust through multimodal unmanned aerial vehicle sensing')
    p('Objective 1 describes how each camera sees white rust and selects the features that carry the disease signal. Post-symptomatic description uses all 1920 subplot-dates of each camera with the DI as target (Activities 1.1–1.7); '
      'the pre-symptomatic stage uses the 576 subplot-dates with later-infected vs healthy as target (Activity 1.8). Descriptive steps (response curves, correlations, physiology, stability) use all 48 plots; every feature-selection step (Activities 1.2–1.6 and Step 1.8.2) uses the 33 training plots only, and its feature sets are used unchanged by the models of Objectives 2 and 3 (as Ma et al. (2026) selected features on their training data only). The row "Samples used" of each step says which. '
      'Activities 1.2–1.5 explain each selection method with the hyperspectral camera; Activity 1.6 then applies them to each camera separately – hyperspectral, multispectral, RGB and thermal – so that every camera gets its own disease-specific feature set before any fusion (as Mustafa et al. (2023) selected features within each sensor before fusing them).')
    myfig('chain', 'g10_selection_chain.png', 'Feature selection of each camera separately (Activity 1.6), run once on the 33 training plots for each task: one method per feature type inside each camera, then the variance inflation factor gives the disease-specific feature set (DSF) of that camera, used unchanged as model input.')
    P = 'Objective 1'
    DESC = 'All 48 plots (1920 subplot-dates per camera): description only; nothing from this step enters a model.'
    SEL = '33 training plots only (1320 subplot-dates per camera); the result is fixed here and used unchanged as model input in Objectives 2 and 3.'
    DESCP = 'All 48 plots (576 pre-symptomatic subplot-dates per camera): description only.'
    SELP = '33 training plots only (396 pre-symptomatic subplot-dates per camera); used unchanged in Objective 3.'

    h2('Activity 1.1 – Response analysis')
    step('1.1.1', 'Mean spectra and curves by disease index class', part=P,
         data=DESC,
         what='Mean ± SD reflectance and first derivative of each DI class, and the % difference of each class from class 0, for the HS camera; class means of every MS, RGB and thermal feature.',
         why='The first, model-free evidence of where and in which direction white rust changes the signal; it guides the reading of every selected feature.',
         do=['Group the subplot-dates by DI class (0, 1, 3, 5, 7, 9).', 'Plot mean ± SD reflectance and first derivative; plot (class − class 0)/class 0 × 100.', 'Tabulate class means of the MS, RGB and thermal features.'],
         check=['Curves drawn for every class with at least 5% of the samples.'],
         out='Response curves → interpretation of 1.2–1.6.',
         papers=[('Ma et al. (2026)', 'Rice blast; mean canopy spectra of each severity level after smoothing; the red edge (680–800 nm) and near-infrared separated the levels best.', 'Mean spectra by severity class from UAV hyperspectral data.'),
                 ('Mahlein et al. (2013)', 'Sugar-beet diseases; spectral signatures of each disease and severity.', 'Class-wise spectral signatures.'),
                 ('Guo et al. (2021)', 'Wheat yellow rust; canopy spectra of plots with different disease index.', 'Canopy spectra by severity from a UAV.'),
                 ('Mandal et al. (2023)', 'Rice blast; canopy spectra of each 0–9 severity level and the difference of each level from healthy plants; the red (about 690 nm) and near-infrared (800–1100 nm) regions differed most.', 'Mean curves and difference from class 0.'),
                 ('Bohnenkamp et al. (2021)', 'Wheat foliar diseases; hyperspectral library from infection to symptoms with spectral turning points confirmed by histology.', 'Spectral signatures described stage by stage and class by class.')])
    myfig('specdemo', 'g07_spectra_demo.png', 'Demo of the outputs of Step 1.1.1 (simulated spectra): (a) mean reflectance by DI class, (b) % difference from class 0, (c) first derivative at the red edge.')
    step('1.1.2', 'Correlation of each feature with the disease index', part=P,
         data=DESC,
         what='Pearson r between the DI and every band, derivative band and feature of every camera.',
         why='Shows the strength and sign of the relation at every wavelength and for every feature.',
         do=['Compute r with the DI for all features of all cameras (all 1920 samples).', 'Plot r against wavelength for R and FD; list the 10 strongest features of each camera.'],
         check=['Correlation curves and top-10 tables for the four cameras.'],
         out='Correlation curves → interpretation.',
         papers=[('Zhang et al. (2012)', 'Wheat powdery mildew; correlation coefficient of each of 32 leaf spectral features with the disease index (higher |r| = more sensitive) and t-tests between damage levels.', 'Univariate correlation of every feature with the DI.'),
                 ('Ma et al. (2026)', 'Rice blast; correlation of vegetation indices and texture features with severity.', 'Correlation of indices and texture with severity.'),
                 ('Guo et al. (2021)', 'Wheat yellow rust; correlation of indices and texture with the disease index.', 'Same analysis on UAV features.')])
    step('1.1.3', 'Response by variety, sowing date, growth stage, days after inoculation and weather', part=P,
         data=DESC,
         what='Mean DI and the class curves of 1.1.1 are shown separately by variety, sowing date, growth stage and DAI; DI is plotted against the favourable-day counts.',
         why='Growth stage (especially flowering) and date change the canopy signal independently of disease; the disease signal must hold within each stratum.',
         do=['Table of mean DI by variety × sowing date × date.', 'Class curves within each growth stage (vegetative, flowering, pod formation).', 'DI against favourable days (Step A6).'],
         check=['Every stratum has a table row.'],
         out='Strata → 2.10.',
         papers=[('Blasch et al. (2023)', 'Wheat rusts; UAV detection depended on the crop growth stage.', 'Results by growth stage.'),
                 ('Liu et al. (2024)', 'Wheat powdery mildew; spectral, texture and canopy-temperature features compared between healthy and infected plots at early, middle and late infection stages (Zadoks stage recorded).', 'Responses reported by stage.'),
                 ('Chattopadhyay et al. (2011)', 'White rust of mustard; disease development related to weather in different sowings.', 'DI related to weather and sowing date.'),
                 ('Zhang et al. (2022)', 'Rice leaf blast severity classified separately at the jointing, booting and heading stages.', 'Results reported within each growth stage.')])

    h2('Activity 1.2 – Optimal wavelengths of the hyperspectral camera by Shapley additive explanations and competitive adaptive reweighted sampling')
    step('1.2.1', 'Effective wavelength ranges from normalised difference spectral index and ratio spectral index maps', part=P,
         data=SEL,
         what='For every pair of HS bands, NDSI = (R_{i} − R_{j})/(R_{i} + R_{j}) and RSI = R_{i}/R_{j} are computed and their R² with the DI drawn as maps; bands in pairs with R² > 0.5 for both indices are the effective ranges.',
         why='The maps show which band combinations follow the disease and restrict SHAP-CARS to informative regions.',
         do=['Use the 483 HS bands with reduced sampling (every 2nd band).', 'Compute R² of NDSI and RSI with the DI for every pair; draw the two maps.',
             'Effective ranges = bands taking part in pairs with R² > 0.5 in both maps; if no pair reaches 0.5, use the pairs in the top 5% of R².'],
         settings=['about 29 000 band pairs per index.'],
         check=['Both maps drawn; effective ranges written in nm.'],
         out='Effective ranges → 1.2.2; best NDSI and RSI pairs → 1.3.1.',
         papers=[('Ma et al. (2026)', 'Rice blast; R² contour maps of NDSI and RSI with severity (450–1000 nm, reduced sampling); effective ranges were the regions where R² of both indices exceeded 0.5 (455–503, 520–661 and 702–1000 nm).', 'Same maps, indices and 0.5 threshold.'),
                 ('Tian et al. (2021)', 'Rice leaf blast; kept the top 5% of features by separability when choosing disease-sensitive features.', 'Top-5% fall-back if no pair reaches 0.5.'),
                 ('Mandal et al. (2023)', 'Rice blast; R² contour maps of ratio and normalised-difference indices of all band pairs (350–2500 nm) against the blast score, first at 10-nm and then at 1-nm sampling, drawn on the two-thirds calibration data only.', 'Band-pair R² maps on the training data only, with reduced sampling.'),
                 ('Huang et al. (2014)', 'Winter wheat diseases; optimised two-band indices from exhaustive band combinations.', 'Exhaustive two-band search.')])
    myfig('ndsidemo', 'g08_ndsi_demo.png', 'Demo of Step 1.2.1 (simulated): NDSI R² map with the R² = 0.5 contour that marks the effective ranges.', width=360)
    step('1.2.2', 'Optimal wavelengths by Shapley additive explanations and competitive adaptive reweighted sampling', part=P,
         data=SEL,
         what='Candidates are the R and FD bands inside the effective ranges. (1) A random forest predicts the DI and the bands are ranked by mean |SHAP|; the top-ranked bands are kept. (2) Monte Carlo cross-validation chooses the number of PLS components. (3) CARS eliminates redundant bands; the subset with the best cross-validated performance gives the optimal wavelengths (OW).',
         why='Hundreds of correlated bands cannot be given directly to a model; SHAP removes uninformative bands, then CARS removes redundant ones.',
         do=['Standardise the candidate bands (z-score; PLS is scale-sensitive and reflectance and first-derivative values differ by about 100 times).', 'Random forest regression of the DI (500 trees); mean |SHAP| per band (TreeSHAP); keep the top 40%.', 'MCCV (50 random 80/20 divisions by plot) chooses the PLS components (1–15).',
             'CARS: 50 iterations of PLS-weighted, exponentially decreasing band subsets with adaptive reweighted sampling; keep the subset with the lowest GroupKFold(3) RMSE.', 'Label the bands R_{λ} or FD_{λ}.'],
         settings=['Random forest 500 trees, seed 42; CARS 50 iterations; MCCV 50 divisions.'],
         check=['OW list of about 10–15 bands with wavelength and type.'],
         out='OW → 1.6.1, 2.6 (configurations).',
         papers=[('Ma et al. (2026)', 'Rice blast; SHAP-CARS – an ensemble model ranked the bands by mean |SHAP|, MCCV chose the PLS components, CARS eliminated redundant variables over many iterations, and the subset was fixed by validation performance; 12 key wavelengths were kept.', 'The three stages in the same order.'),
                 ('Tian et al. (2021)', 'Rice leaf blast; reflectance bands, 97 indices and wavelet features screened by their single-threshold separability of infected and healthy leaves on each day; the top 5% kept and only one representative feature per common region retained before modelling.', 'Band selection before the models.'),
                 ('Bijlwan et al. (2025)', 'Crop disease severity models; inputs of scale-sensitive models centred and scaled, tree models used without scaling.', 'Bands z-scored before PLS/CARS; the random forest SHAP ranking uses unscaled bands.')])
    myfig('shapdemo', 'g09_shapcars_demo.png', 'Demo of Step 1.2.2 (simulated): (a) SHAP ranking and the top 40% kept; (b) bands kept by CARS.')

    h2('Activity 1.3 – Spectral index construction')
    step('1.3.1', 'Best normalised difference spectral index and ratio spectral index', part=P,
         data=SEL,
         what='The NDSI and RSI pairs with the highest R² in the maps (bands at least 10 nm apart) are added as indices.',
         why='The best two-band indices are simple, data-driven white rust indices.',
         do=['Pick the highest-R² NDSI and RSI pairs from Step 1.2.1.', 'Fix the two pairs on the training plots; compute the indices at full spectral resolution for all samples (training and test).'],
         check=['Two indices with their band positions.'],
         out='NDSI_best, RSI_best → 1.4.',
         papers=[('Ma et al. (2026)', 'Rice blast; best NDSI and RSI from the band-pair maps.', 'Same indices.'),
                 ('Mandal et al. (2023)', 'Rice blast; new ratio and normalised-difference blast indices RBI = R1148/R1301 and NDBI (R1148, R1301) from the highest-R² band pair (R² 0.85 and 0.86).', 'Best two-band combination as a new index.')])
    step('1.3.2', 'White Rust Index', part=P,
         data=SEL,
         what='A three-band index WRI = NDSI(λ_{1}, λ_{2}) + w × R_{λ3} is searched.',
         why='A third band can correct an effect that a two-band index cannot; the index is specific to white rust and can be carried to cheaper sensors.',
         do=['Bands at 6-nm steps inside the effective ranges; λ_{1} and λ_{2} at least 50 nm apart; w ∈ {−1, −0.5, 0, 0.5, 1}.', 'Score each candidate by |r| with the DI and by the balanced accuracy of healthy vs diseased (single threshold).', 'Keep the best formula; repeat once with SWIR bands and keep the better one.'],
         check=['WRI formula with λ_{1}, λ_{2}, λ_{3} and w.'],
         out='WRI → 1.4, Objectives 2–3, L9.',
         papers=[('Mahlein et al. (2013)', 'Sugar-beet diseases; each spectral disease index = a normalised difference of two wavelengths at least 50 nm apart plus a weighted single wavelength (weights −1, −0.5, 0, 0.5, 1); spectral resolution reduced to 6 nm; the best 25% of RELIEF-F-weighted wavelengths and differences searched exhaustively; balanced accuracy with an optimised threshold.', 'Same form, 6-nm steps, 50-nm rule, weights and balanced accuracy.'),
                 ('Zheng et al. (2018)', 'Wheat yellow rust; a new three-band index for Sentinel-2.', 'Three-band disease index.'),
                 ('Liu et al. (2026)', 'Wheat powdery mildew; a specific vegetation index developed on the ground and used from UAV.', 'A disease-specific index for field use.')])
    demo('wri', [['Rank', 'λ1 (nm)', 'λ2 (nm)', 'λ3 (nm)', 'w', '|r| with DI', 'Balanced accuracy'], ['1', '754', '700', '532', '−0.5', '0.71', '0.83'], ['2', '760', '694', '550', '−0.5', '0.70', '0.82'], ['3', '790', '718', '—', '0', '0.68', '0.80']],
         'WRI search output', widths=[900, 1300, 1300, 1300, 900, 1700, 2200])
    step('1.3.3', 'Two-band indices of the multispectral camera', part=P,
         data=SEL,
         what='The 10 normalised differences of the five MS bands are compared, and the best is added to the MS group.',
         why='Gives the cheaper camera its own data-driven index.',
         do=['Compute (B_{i} − B_{j})/(B_{i} + B_{j}) for all 10 pairs; r with the DI.', 'Add the best pair as MS_NDbest.'],
         check=['Ten r values tabulated.'],
         out='MS_NDbest → 1.6.2.',
         papers=[('Ma et al. (2026)', 'Rice blast; normalised difference indices from band pairs.', 'Same index form.'),
                 ('Liu et al. (2024)', 'Wheat powdery mildew; red-edge multispectral indices for severity.', 'MS two-band indices.')])

    h2('Activity 1.4 – Vegetation index selection')
    p('Shown for the hyperspectral indices; the same filter and ranking are used for the multispectral spectral group, the RGB colour group and the thermal group (Steps 1.6.2–1.6.4).')
    step('1.4.1', 'Redundancy filter of the indices', part=P,
         data=SEL,
         what='Among the 48 published indices, 3 red-edge parameters, NDSI_best, RSI_best and WRI, indices correlated at |r| ≥ 0.95 form clusters; from each cluster the index most correlated with the DI is kept.',
         why='Many indices are near-copies (NDVI family, simple ratios); ReliefF ranks are unreliable among near-identical features.',
         do=['Correlation matrix of all indices.', 'Cluster indices with |r| ≥ 0.95; keep the one with the highest |r| with the DI.'],
         check=['List of kept and removed indices.'],
         out='Non-redundant indices → 1.4.2.',
         papers=[('Ma et al. (2026)', 'Rice blast; correlation analysis among vegetation indices showed that PSSRb, SR, RNDVI and FRI3 were strongly correlated (redundant) while WBI and others carried different information.', 'Correlation among indices to remove redundancy.'),
                 ('Lv et al. (2023)', 'Southern corn leaf blight; features sensitive in two experiments were merged when they lay within 10 nm of each other, giving one pool before SFFS.', 'Near-duplicate features merged before selection.')])
    step('1.4.2', 'Relief-F ranking of the indices', part=P,
         data=SEL,
         what='The remaining indices are ranked with ReliefF (DI classes, Tasks A and B) and RReliefF (DI, Task C); the top five per task are the selected indices (VI).',
         why='ReliefF rewards features that separate classes among similar samples and can reward a feature that is useful together with others.',
         do=['Min–max scale the indices to 0–1 (the ReliefF difference between two samples is |x1 − x2| divided by the feature range, so every feature counts equally).', 'ReliefF / RReliefF with k = 10 nearest neighbours.', 'Keep the top five per task.'],
         check=['VI lists of Tasks A, B and C.'],
         out='VI → 1.6.1.',
         papers=[('Ma et al. (2026)', 'Rice blast; the Relief algorithm selected the five vegetation indices with the highest weights (RVI, PSSRb, CIre, CIgreen, SR).', 'Relief ranking, top five.'),
                 ('Mahlein et al. (2013)', 'Sugar-beet diseases; RELIEF-F weighted single wavelengths and normalised wavelength differences by how well they separated near samples of different classes; the best 25% were kept for the index search.', 'ReliefF for disease features.'),
                 ('Lv et al. (2023)', 'Southern corn leaf blight; RELIEF-F weights ranked bands, indices, first derivatives and wavelet features; the top 10% were kept before SFFS.', 'Relief-F ranking before the next selection step (here the top five).')])

    h2('Activity 1.5 – Texture selection and the Tri-band Texture Fusion Index')
    p('Shown for the hyperspectral texture; the same steps are used for the multispectral and RGB texture (Steps 1.6.2–1.6.3).')
    step('1.5.1', 'Minimum redundancy maximum relevance selection of texture features', part=P,
         data=SEL,
         what='The 24 PCA texture features are filtered at |r| ≥ 0.95 and ranked by minimum redundancy maximum relevance (mRMR); the top six are kept.',
         why='Texture features are many and correlated; mRMR keeps features relevant to the DI and different from each other.',
         do=['Redundancy filter |r| ≥ 0.95.', 'mRMR ranking with the DI (mutual information); keep the top six (TF1–TF6).'],
         check=['Six texture features listed.'],
         out='TF1–TF6 → 1.5.2, 1.6.1.',
         papers=[('Ma et al. (2026)', 'Rice blast; mRMR ranked the texture features; the six with the strongest relevance and smallest redundancy were PC2-Mea, PC3-Mea, PC2-Dis, PC2-Con, PC2-Var and PC2-Hom.', 'Same method and number (six).'),
                 ('Yuan et al. (2025)', 'Rice bacterial blight; mRMR selection of UAV and satellite features.', 'mRMR for disease features.')])
    step('1.5.2', 'Tri-band Texture Fusion Index', part=P,
         data=SEL,
         what='All ordered triplets of TF1–TF6 are combined with three formulas; the triplet with the highest |r| with the DI is the TTFI.',
         why='One combination of three texture features can describe roughness, heterogeneity and structure together.',
         do=['Form 6 × 5 × 4 = 120 ordered triplets.', 'Compute TTFI1 = (TF1 + TF2)/TF3, TTFI2 = TF1 × TF2/TF3, TTFI3 = TF1 × (TF1 + TF2)/(TF2 + TF3) – 360 candidates.', 'Keep the candidate with the highest |r| with the DI.'],
         check=['Best TTFI formula and triplet.'],
         out='TTFI → 1.6.1, 2.6.',
         papers=[('Ma et al. (2026)', 'Rice blast; ordered triplets of the six mRMR texture features combined into TTFIs; TTFI3 had the highest correlation with infection (|r| = 0.756) and was used for modelling.', 'Same construction and selection by |r|.')])
    demo('ttfi', [['Formula', 'TF1, TF2, TF3 (demo values 0.8, 1.2, 0.5)', 'Value'], ['TTFI1 = (TF1 + TF2)/TF3', '(0.8 + 1.2)/0.5', '4.00'], ['TTFI2 = TF1 × TF2/TF3', '0.8 × 1.2/0.5', '1.92'], ['TTFI3 = TF1 × (TF1 + TF2)/(TF2 + TF3)', '0.8 × 2.0/1.7', '0.94']],
         'Worked example of the three TTFI formulas', widths=[3800, 3800, 2000])

    h2('Activity 1.6 – Feature selection for each camera separately')
    p('The methods of Activities 1.2–1.5 are now applied to each camera on its own. Inside a camera, features compete only with features of the same type; the survivors of the camera are pooled and thinned by the variance inflation factor (VIF), which gives the disease-specific feature set (DSF) of that camera. Cameras are joined only in Objective 2 (Step 2.2). '
      'This keeps the contribution of every camera visible and stops the few thermal or RGB features from being swamped by about 1000 hyperspectral features. All steps of this activity use the 33 training plots and are repeated for each task (A, B, C); Step 1.6.6 only describes the result.')
    rows = [['Camera', 'Feature group (candidates)', 'Selection inside the group', 'Kept', 'Disease papers'],
            ['Hyperspectral', 'Bands: reflectance and first derivative (966)', 'NDSI/RSI R² maps → effective ranges → SHAP top 40% → CARS (Steps 1.2.1–1.2.2)', 'OW, 10–15', 'Ma et al. (2026)'],
            ['', 'Indices: 48 published + 3 red-edge + NDSI_best, RSI_best, WRI (54)', '|r| ≥ 0.95 filter → ReliefF / RReliefF (Steps 1.3–1.4)', 'VI, 5', 'Ma et al. (2026); Mahlein et al. (2013)'],
            ['', 'Texture: GLCM of 3 principal components (24)', '|r| ≥ 0.95 filter → mRMR → TTFI (Step 1.5)', '6 + TTFI', 'Ma et al. (2026); Guo et al. (2021)'],
            ['Multispectral', 'Spectral: 5 bands + 12 indices + best two-band normalised difference (18)', '|r| ≥ 0.95 filter → ReliefF / RReliefF', '5', 'Liu et al. (2024); Ma et al. (2026)'],
            ['', 'Texture: GLCM of the 5 bands (40)', '|r| ≥ 0.95 filter → mRMR → TTFI-MS', '6 + TTFI', 'Liu et al. (2024); Ma et al. (2026)'],
            ['RGB', 'Colour: 6 colour indices + mean hue, saturation, value (9)', '|r| ≥ 0.95 filter → ReliefF / RReliefF', '5', 'Huang et al. (2020)'],
            ['', 'Texture: GLCM of the R, G and B images (24)', '|r| ≥ 0.95 filter → mRMR → TTFI-RGB', '6 + TTFI', 'Huang et al. (2020); Feng et al. (2022)'],
            ['Thermal', 'Temperature statistics (6), normalised temperatures (4), texture (8) (18)', '|r| ≥ 0.95 filter → ReliefF / RReliefF; normalised temperatures always passed on', '5 + 4', 'Feng et al. (2022); Calderón et al. (2013)'],
            ['Each camera', 'Pooled survivors of its groups', 'VIF: remove the largest until all < 10 (Step 1.6.5)', 'DSF', 'Tian et al. (2021); Mustafa et al. (2023); Lv et al. (2023)']]
    tab('camsel', rows=rows, caption='Feature selection of each camera (33 training plots, for each task).', widths=[1150, 2550, 2750, 950, 2200], size=15)
    step('1.6.1', 'Feature selection for the hyperspectral camera', part=P,
         data=SEL,
         what='The hyperspectral chain of Activities 1.2–1.5: bands give the optimal wavelengths (OW), indices give the selected indices (VI), and texture gives six texture features (TF) and the TTFI; these are pooled for the VIF step.',
         why='Bands are many and collinear, indices must separate overlapping classes and texture features are correlated, so each type gets its own selector, as in the core reference.',
         do=['Bands: 966 reflectance and first-derivative bands → effective ranges of the NDSI/RSI maps (Step 1.2.1) → SHAP top 40% → CARS → OW, about 10–15 bands (Step 1.2.2).',
             'Indices: 48 published indices, 3 red-edge parameters, NDSI_best, RSI_best and WRI (Steps 1.3.1–1.3.2) → |r| ≥ 0.95 filter (Step 1.4.1) → ReliefF / RReliefF top five = VI (Step 1.4.2).',
             'Texture: 24 PCA texture features → |r| ≥ 0.95 filter → mRMR top six = TF1–TF6 → TTFI (Steps 1.5.1–1.5.2).',
             'Pool OW + VI + TF + TTFI (about 27 features) and pass them to Step 1.6.5.'],
         check=['Candidate list of the HS camera for each task, with the group of every feature.'],
         out='HS candidates → 1.6.5.',
         papers=[('Ma et al. (2026)', 'Rice blast; UAV hyperspectral bands selected by SHAP-CARS, vegetation indices by Relief (top five) and texture by mRMR (top six) with the TTFI; the selected groups were then combined as model input.', 'Same three groups, selectors and numbers.'),
                 ('Guo et al. (2021)', 'Wheat yellow rust; UAV hyperspectral vegetation indices and texture of principal-component images computed as separate groups and then combined in one model.', 'Indices and texture as separate HS groups.'),
                 ('Mustafa et al. (2023)', 'Wheat Fusarium head blight; disease-sensitive features selected by Boruta within each data source (hyperspectral reflectance, chlorophyll-fluorescence imaging, phenotyping images), then VIF < 10 and ML-SFFS for the optimal combination.', 'Selection inside each sensor before any fusion.')])
    step('1.6.2', 'Feature selection for the multispectral camera', part=P,
         data=SEL,
         what='The 67 multispectral features are split into a spectral group (5 bands, 12 indices and the best two-band normalised difference of Step 1.3.3) and a texture group (40 GLCM features); each group is thinned with the method used for the same type of hyperspectral feature.',
         why='Five bands are too few for SHAP-CARS, so the bands enter the spectral group with the indices; multispectral texture is as correlated as hyperspectral texture and is treated the same way.',
         do=['Spectral group (18): |r| ≥ 0.95 filter → min–max scaling → ReliefF (Tasks A, B) or RReliefF (Task C), k = 10 → top five.',
             'Texture group (40 = 8 GLCM measures × 5 bands): |r| ≥ 0.95 filter → mRMR with the DI → top six (MS-TF1 to MS-TF6) → TTFI-MS from the 120 ordered triplets and three formulas of Step 1.5.2, highest |r| with the DI.',
             'Pool the five spectral features, six textures and TTFI-MS (12 features) and pass them to Step 1.6.5.'],
         check=['Candidate list of the MS camera for each task.'],
         out='MS candidates → 1.6.5.',
         papers=[('Liu et al. (2024)', 'Wheat powdery mildew; from UAV multispectral images: band reflectance, nine vegetation indices (NDRE, PSRI and MTCI tracked the disease in the middle and late stages) and three-band texture combination indices built from the 40 textures (5 bands × 8 GLCM measures); features chosen by Pearson correlation and recursive feature elimination with 10-fold cross-validation repeated 500 times.', 'An MS spectral group and an MS texture group with a three-texture index (TTFI-MS).'),
                 ('Nguyen et al. (2023)', 'Spring wheat yellow rust; CRI2, SAVI2 and GLCM contrast of multispectral UAV images were the features most correlated with the disease.', 'MS indices and MS texture both considered.'),
                 ('Ma et al. (2026)', 'Rice blast; Relief top five for indices, mRMR top six and TTFI for texture.', 'Same selectors and numbers as for the HS camera.')])
    step('1.6.3', 'Feature selection for the red–green–blue camera', part=P,
         data=SEL,
         what='The 33 RGB features are split into a colour group (6 colour indices and mean hue, saturation and value) and a texture group (24 GLCM features of the R, G and B images), thinned like the hyperspectral indices and texture.',
         why='Colour indices record chlorosis and the white pustules; texture records the uneven canopy; both are cheap features whose value must be judged on their own.',
         do=['Colour group (9): |r| ≥ 0.95 filter → min–max scaling → ReliefF / RReliefF (k = 10) → top five.',
             'Texture group (24 = 8 GLCM measures × 3 colour channels): |r| ≥ 0.95 filter → mRMR → top six → TTFI-RGB (rules of Step 1.5.2).',
             'Pool the five colour features, six textures and TTFI-RGB (12 features) and pass them to Step 1.6.5.'],
         check=['Candidate list of the RGB camera for each task.'],
         out='RGB candidates → 1.6.5.',
         papers=[('Huang et al. (2020)', 'Wheat Fusarium head blight; nine colour features (mean, SD and skewness of R, G and B) and GLCM texture of sensitive-band images; colour and texture features were each screened by correlation analysis and then fused with the spectral bands chosen by the successive projections algorithm (spectral + colour best: 92% on the prediction set with PSO-SVM).', 'Colour and texture groups screened separately, then fused.'),
                 ('Feng et al. (2022)', 'Wheat powdery mildew; texture features of RGB (and thermal) images used as their own data source beside vegetation indices and temperature parameters.', 'RGB texture as a separate group.'),
                 ('Ma et al. (2026)', 'Rice blast; Relief for indices, mRMR and TTFI for texture.', 'Same selectors as for the HS camera.')])
    step('1.6.4', 'Feature selection for the thermal camera', part=P,
         data=SEL,
         what='The 18 thermal features (6 temperature statistics including MTD, 4 normalised temperatures and 8 texture features) form one group; it is filtered and ranked, and the four normalised temperatures are always passed on.',
         why='The thermal group is small, so one group is enough; raw temperatures follow the air temperature and humidity of the flight, so the weather-corrected forms of Step D3 are kept whatever their rank.',
         do=['|r| ≥ 0.95 filter among the 6 statistics and 8 texture features.', 'ReliefF / RReliefF (k = 10) after min–max scaling → top five.',
             'Add the four normalised temperatures (CTD, CTR, NRCT, difference from healthy) and pass the 9 features to Step 1.6.5, where VIF removes the collinear ones.'],
         check=['Candidate list of the thermal camera for each task.'],
         out='Thermal candidates → 1.6.5.',
         papers=[('Feng et al. (2022)', 'Wheat powdery mildew; canopy temperature parameters from thermal images, corrected for the daily change of air temperature (CTD, CTR, NRCT), used as one data source together with texture of the thermal images.', 'Normalised temperatures and thermal texture as the thermal group.'),
                 ('Calderón et al. (2013)', 'Verticillium wilt of olive; airborne canopy minus air temperature and the crop water stress index detected infected trees early and followed the fall of stomatal conductance.', 'A weather-corrected canopy temperature is always kept.'),
                 ('Maimaitijiang et al. (2020)', 'Soybean yield (method support); NRCT = (T_{i} − T_{min})/(T_{max} − T_{min}) with the lowest and highest temperature of the whole field used as the thermal feature of the UAV thermal camera.', 'NRCT computed over the field on each date.'),
                 ('Oerke et al. (2006)', 'Cucumber downy mildew; the maximum temperature difference within leaves rose with infection, but air temperature and humidity also changed leaf temperature.', 'MTD as a candidate; normalised forms always kept.')])
    step('1.6.5', 'Variance inflation factor and the disease-specific feature set of each camera', part=P,
         data=SEL,
         what='For each camera and task, the candidates of Steps 1.6.1–1.6.4 are pooled; the feature with the largest VIF is removed one at a time until all VIF < 10. The rest is the disease-specific feature set (DSF) of that camera.',
         why='Bands, indices and texture of one camera overlap; collinear inputs make models unstable and explanations unreliable.',
         do=['VIF_{j} = 1/(1 − R_{j}^{2}), R_{j}^{2} from regressing feature j on the other candidates of the same camera.', 'Remove the largest VIF and repeat until all VIF < 10.', 'Write the DSF of each camera and task (four cameras × three tasks) with the group of every feature.'],
         check=['DSF of each camera and task with all VIF < 10.'],
         out='DSF of each camera and task (training plots) → 1.6.6, 1.6.7 and, unchanged, Step 2.2 (fusion) and the models.',
         papers=[('Lv et al. (2023)', 'Southern corn leaf blight; features with a variance inflation factor above 10 were not used for model development.', 'Same VIF < 10 rule.'),
                 ('Tian et al. (2021)', 'Rice leaf blast; the collinearity of the disease-specific feature pool was reduced by VIF and only features with VIF < 10 entered ML-SFFS.', 'VIF before SFFS.'),
                 ('Mustafa et al. (2023)', 'Wheat Fusarium head blight; VIF analysis on the Boruta-selected features of the hyperspectral, fluorescence and phenotyping data; features with VIF < 10 kept as the selected disease-specific features.', 'VIF on the selected features of each sensor.')])
    demo('vif', [['Round', 'Largest VIF', 'Feature removed', 'Features left'], ['1', '86.4', 'FD_722', '26'], ['2', '31.2', 'NDVI780', '25'], ['3', '14.8', 'PC2-Var', '24'], ['…', '…', '…', '…'], ['12', '8.9 (< 10)', '—', '15 = DSF of the HS camera']], 'VIF elimination for the hyperspectral camera', widths=[1200, 2200, 3000, 3200])
    demo('dsfdemo', [['Camera', 'Candidates', 'DSF (Task C, demo)', 'Size'], ['Hyperspectral', '27', 'R_{560}, FD_{716}, FD_{742}, R_{1450}, WRI, PSRI, CI_{rededge}, PC2-Mea, PC2-Con, TTFI …', '15'],
                     ['Multispectral', '12', 'NDRE, PSRI, MTCI, RE band, NIR-Con, RE-Hom, TTFI-MS', '7'], ['RGB', '12', 'ExG − ExR, VARI, saturation, G-Ent, R-Con, TTFI-RGB', '6'], ['Thermal', '9', 'CTD, NRCT, ΔT, MTD', '4']],
         'Disease-specific feature set of each camera (Step 1.6.5 output)', widths=[1500, 1300, 5400, 1400])
    step('1.6.6', 'Stability of the selected features across growth stages and severity levels', part=P,
         data=DESC,
         what='Every DSF feature of every camera is compared between healthy and diseased subplots and correlated with the DI separately in the vegetative, flowering and pod-formation stages, and its mean is shown for each DI class within each stage.',
         why='Flowering and pod formation change the canopy signal; a feature chosen on pooled data should be shown to follow white rust within each stage before it is interpreted (disease characterisation at different severity levels and growth stages).',
         do=['Within each stage: t-test of plot means (healthy vs diseased) and Pearson r with the DI for every DSF feature.', 'Box plots of each DSF feature by DI class within each stage.',
             'Table feature × stage with the sign and significance; a feature is stable if it is significant with the same sign in all three stages.'],
         check=['Stability table and box plots for the four cameras.'],
         out='Stable and stage-dependent features → interpretation, 2.10.',
         papers=[('Tian et al. (2021)', 'Rice leaf blast; sensitive features found on each day after inoculation, and only the features common to the days were kept as disease-specific features.', 'Features judged by their consistency over time.'),
                 ('Liu et al. (2024)', 'Wheat powdery mildew; spectral, texture and temperature features compared between healthy and infected plots at early, middle and late stages; only NDRE, PSRI and MTCI captured the change consistently in the middle to late stages.', 'Stage-by-stage check of the features.'),
                 ('Mustafa et al. (2023)', 'Wheat Fusarium head blight; only seven spectral features (CAR, SRPI, RR, PSSRb, NDVI, PSNDa, RARSb) showed consistently stable responses to the disease.', 'Consistency reported for each selected feature.'),
                 ('Zhang et al. (2024)', 'Tomato bacterial leaf spot; the critical bands and indices changed between the four disease stages (water and 750 nm early, leaf structure later).', 'Stage-dependent features are expected and reported.')])
    step('1.6.7', 'Complementarity of the cameras', part=P,
         data=SEL,
         what='Correlation between the DSFs of different cameras and the DI response of each DSF by treatment.',
         why='Cameras that carry different information are the ones worth fusing (Objective 2).',
         do=['Cross-camera correlation matrix of the DSFs.', 'Mean DSF values by treatment and DI class.'],
         check=['Correlation heat map and treatment table.'],
         out='Expected fusion benefit → 2.8.',
         papers=[('Mahlein et al. (2019)', 'Fusarium head blight of wheat; thermal, fluorescence and hyperspectral parameters were correlated with each other and with severity (except MTD); an SVM on thermal + hyperspectral parameters was best (mean 90%), and adding the third sensor did not improve accuracy (87%).', 'Correlation between cameras judges what a fusion can add.'),
                 ('Feng et al. (2022)', 'Wheat powdery mildew; vegetation indices were the best single source, followed by temperature parameters and texture; fusing all three gave the best model.', 'Fusion of complementary cameras.')])

    h2('Activity 1.7 – Physiological basis of the camera responses')
    step('1.7.1', 'Effect of white rust on the plant parameters', part=P,
         data='All 48 plots (designated subplots): description only.',
         what='Each parameter of Step A7 is compared between inoculated plots and the healthy plot of the same treatment on each date (paired t-test), and between varieties and sowing dates within the inoculated plots (two-way ANOVA of the RBD).',
         why='Shows what white rust does to pigments, water, membranes and gas exchange in this experiment.',
         do=['Flag values beyond the median ± 3 SD of each parameter and date, check them against the sample sheet and remove them only if faulty.', 'Mean of the three replications per treatment and date.', 'Paired t-test inoculated vs healthy (12 pairs) per date (Wilcoxon signed-rank test if the differences are not normal).', 'Two-way ANOVA (variety × sowing date) within R1–R3, LSD at 5%.'],
         check=['Table of means, differences and p-values per parameter and date.'],
         out='Changed parameters → 1.7.2.',
         papers=[('Mishra et al. (2009)', 'White rust of Indian mustard; protein, phenols and sugars of inoculated leaves of six genotypes related to the disease index.', 'Infected vs healthy comparison of biochemical parameters.'),
                 ('Calderón et al. (2013)', 'Verticillium wilt of olive; physiological measurements compared between severity levels.', 'Physiology by disease level.'),
                 ('Tian et al. (2021)', 'Rice leaf blast; chlorophyll, carotenoid, anthocyanin and water content of infected and healthy leaves compared on each day by paired t-test (Wilcoxon test if not normal), after outliers beyond the median ± 3 SD were removed.', 'Infected vs healthy tests per date after outlier screening.')])
    step('1.7.2', 'Relation of the plant parameters with the disease index and the camera features', part=P,
         data='All 48 plots (designated subplots): description only.',
         what='Pearson r between each parameter and the subplot DI, and between each parameter and the DSF features of the same subplot and date.',
         why='Links each selected feature to a physiological change (for example red edge with chlorophyll, thermal with stomatal conductance).',
         do=['Join parameters to the designated subplot\'s DI and features.', 'r within each date; table of the strongest links.'],
         check=['Parameter × feature correlation table.'],
         out='Physiological explanation of the DSF → discussion, 2.8.',
         papers=[('Calderón et al. (2013)', 'Verticillium wilt of olive; airborne fluorescence, temperature and narrow-band indices related to leaf physiology and disease severity.', 'Camera features related to measured physiology.'),
                 ('Zarco-Tejada et al. (2018)', 'Xylella in olive; pigment, fluorescence and temperature traits from imagery explained the disease signal.', 'Traits explain the spectral signal.')])

    h2('Activity 1.8 – Characterisation of the pre-symptomatic stage')
    step('1.8.1', 'Pre-symptomatic response curves and tests', part=P,
         data=DESCP,
         what='On 1, 4 and 7 January (2, 5, 8 DAI), mean spectra and features of later-infected subplots are compared with healthy subplots; a t-test of plot means is done for every feature and date.',
         why='Shows whether and where a signal exists before pustules are visible.',
         do=['Labels of Step A5 (healthy vs later-infected).', 'Mean curves of the two groups per date and their difference.', 't-test of plot means (plot = unit) per feature and date.'],
         check=['Curves and test table for the three dates.'],
         out='Responding features → 1.8.2.',
         papers=[('Zhu et al. (2017)', 'Tobacco mosaic virus; hyperspectral images of inoculated and healthy leaves 2, 4 and 6 days after inoculation, before visible symptoms.', 'Pre-symptomatic comparison of the two groups.'),
                 ('Terentev et al. (2023)', 'Wheat leaf rust; hyperspectral images (snapshot camera) of inoculated and healthy plants compared day by day; changes found before visible symptoms.', 'Early spectral differences day by day.'),
                 ('Gold et al. (2020)', 'Potato late and early blight; contact leaf spectra separated infected from healthy plants with more than 80% accuracy two to four days before visible symptoms; shortwave-infrared bands were important.', 'Pre-symptomatic spectral difference, including SWIR.'),
                 ('Zhang et al. (2024)', 'Tomato bacterial leaf spot; pre-symptomatic detection relied on water-related (about 1400 nm) and red-edge (about 750 nm) bands rather than pigments.', 'Water and red-edge features examined before symptoms.')])
    step('1.8.2', 'Pre-symptomatic feature selection', part=P,
         data=SELP,
         what='The selection of each camera (Steps 1.6.1–1.6.5) is run again with the binary label (later-infected vs healthy) on the 396 pre-symptomatic samples of the training plots.',
         why='Features that respond before symptoms can differ from those that grade visible severity.',
         do=['HS: NDSI/RSI maps with R² of the binary label; SHAP-CARS with a classification model; filter + ReliefF for indices; mRMR + TTFI for texture.', 'MS and RGB: filter + ReliefF for the spectral or colour group; mRMR + TTFI for texture.', 'Thermal: filter + ReliefF; normalised temperatures kept.', 'VIF < 10 within each camera → pre-symptomatic DSF of each camera.'],
         check=['Pre-symptomatic DSF of each camera.'],
         out='Pre-symptomatic DSF → 3.3.',
         papers=[('Tian et al. (2021)', 'Rice leaf blast; asymptomatic leaves labelled by their later lesions; sensitive features chosen by their separability of infected and healthy leaves on each day (top 5%), and SFFS found the optimal combination for each infection stage.', 'Separate selection for the early stage with the later-status label.'),
                 ('Ma et al. (2026)', 'Rice blast; the same selection chain for early detection.', 'Same chain.'),
                 ('Terentev et al. (2023)', 'Wheat leaf rust detected with 97–100% accuracy from the fourth day after inoculation with an SVM; the most important wavebands (502, 466, 598, 718 nm …) were identified.', 'Selection of the bands that respond earliest.')])
    step('1.8.3', 'Earliest-responding features', part=P,
         data=DESCP,
         what='For every feature of the pre-symptomatic DSF, the first date with a significant difference (Step 1.8.1) is recorded.',
         why='Tells which camera and feature responds first.',
         do=['Earliest significant date per feature; summary per camera.'],
         check=['Table of earliest dates.'],
         out='Earliest features → 3.5.',
         papers=[('Mahlein et al. (2019)', 'Fusarium head blight; a water index from hyperspectral images responded from 3 days after inoculation, thermal and fluorescence parameters from 5 days.', 'Earliest responding feature per sensor.'),
                 ('Zarco-Tejada et al. (2018)', 'Xylella; traits that changed before visual symptoms.', 'Earliest responding traits.')])
    myfig('presdemo', 'g15_presym_demo.png', 'Demo of Steps 1.8.1–1.8.3 and 3.5 (simulated): (a) difference of one feature between later-infected and healthy subplots; (b) pre-symptomatic AUC by date.')
