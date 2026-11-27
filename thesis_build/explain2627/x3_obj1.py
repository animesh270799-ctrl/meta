from dsl import *
from x1_intro import stage_head


def add():
    # ---------------------------------------------------------------- chapter 7
    h1('7. Stage 6 – Objective 1, part 1: describing how white rust changes the signal')
    stage_head('Stages 1–5 (labelled, normalised camera tables).', 'interpretation of every selected feature (Stage 7) and the discussion.', 'all 48 plots: 1920 post-symptomatic subplot-dates per camera. Nothing from this stage enters a model, so the test plots may be used here.')
    box('In short', 'Before any feature is selected, the data are described: mean spectra of each DI class, their difference from healthy, the correlation of every feature with the DI, the same by growth stage and variety, and the changes in plant physiology.', kind='key')
    h3('Step 6.1 – Mean spectra by DI class (1.1.1)')
    p('The subplot-dates are grouped by DI class (0, 1, 3, 5, 7, 9). For the hyperspectral camera the mean ± SD reflectance and first derivative of each class are plotted, together with the percentage difference of each class from class 0; for the other cameras the class means of every feature are tabulated ({F:spec}). A class is drawn only if it has at least 5% of the samples. '
      'Ma et al. (2026) plotted the mean canopy spectra of each rice blast severity level, and Mandal et al. (2023) the difference of each blast level from healthy plants.')
    eq('difference (%) = (mean R of class − mean R of class 0) / mean R of class 0 × 100')
    myfig('spec', 'g07_spectra_demo.png', 'Demo output of Step 6.1: (a) mean reflectance by DI class, (b) percentage difference from class 0, (c) first derivative at the red edge.')
    h3('Step 6.2 – Correlation of every feature with the DI (1.1.2)')
    p('The Pearson correlation r between the DI and every band, derivative band and feature of every camera is computed on all samples, and r is plotted against wavelength; the ten strongest features of each camera are listed. Zhang et al. (2012) ranked 32 spectral features of wheat powdery mildew by their correlation with the disease index in the same way.')
    eq('r = Σ(x_{i} − x̄)(y_{i} − ȳ) / √[Σ(x_{i} − x̄)^{2} Σ(y_{i} − ȳ)^{2}]')
    h3('Step 6.3 – Response by variety, sowing date, growth stage and weather (1.1.3)')
    p('The class curves are repeated within each growth stage (vegetative, flowering, pod formation), and the mean DI is tabulated by variety × sowing date × date and plotted against the number of favourable days. Flowering changes the canopy signal independently of disease, so the disease signal must be shown within each stage (Blasch et al., 2023; Liu et al., 2024; Zhang et al., 2022).')
    h3('Step 6.4 – Plant physiology (1.7.1, 1.7.2)')
    p('On the four physiology dates the ten parameters (chlorophyll a and b, carotenoids, anthocyanin, total protein, relative water content, membrane stability index, photosynthesis, transpiration and stomatal conductance) are analysed in this order:')
    nl('Values beyond the median ± 3 SD of each parameter and date are flagged and checked against the sample sheet, and removed only if faulty (Tian et al., 2021).',
       'The mean of the three replications of each treatment is compared with the healthy plot of the same treatment on each date by a paired t-test (Wilcoxon signed-rank test if the differences are not normal), as Tian et al. (2021) compared infected and healthy leaves day by day.',
       'Varieties and sowing dates are compared within the inoculated plots by a two-way ANOVA of the RBD (LSD at 5%).',
       'Each parameter is correlated (Pearson r) with the subplot DI and with the selected features of the same subplot and date, to link each feature to a physiological change (Calderón et al., 2013; Yu et al., 2025; Mishra et al., 2009).')
    box('On a new data set', 'Repeat the description on all samples of the new data; it is the first look at whether the disease changes the signal in the same way.', kind='present')

    # ---------------------------------------------------------------- chapter 8
    h1('8. Stage 7 – Objective 1, part 2: choosing the features of each camera')
    stage_head('Stage 6 (description) and Stage 4 (split).', 'Objective 2 (the disease-specific feature sets are the model inputs) and Objective 3.', '33 training plots only: 1320 post-symptomatic subplot-dates per camera. The result is fixed here and used unchanged by every model.')
    box('In short', 'Each camera is treated on its own. Inside a camera, each type of feature has its own selection method: bands by maps and SHAP-CARS, indices by a redundancy filter and ReliefF, texture by mRMR and the TTFI. The survivors of a camera are pooled and thinned by the variance inflation factor (VIF). The result is the disease-specific feature set (DSF) of that camera for each task.', kind='key')
    h2('8.1 Why selection is done this way')
    nl('**Inside each camera.** If all cameras were pooled, about 1000 hyperspectral features would compete with 18 thermal and 33 RGB features and the small cameras would lose for numerical, not biological, reasons. Mustafa et al. (2023) selected features within each data source, applied VIF and only then fused the sources.',
       '**One method per feature type.** Bands are many and strongly correlated, indices must separate overlapping classes, and texture features are correlated with each other; Ma et al. (2026) therefore selected bands with SHAP-CARS, indices with Relief and texture with mRMR.',
       '**On the training plots only.** The selected features are the inputs of the models; if the test plots helped to choose them, the test accuracy would be optimistic (Ambroise and McLachlan, 2002).',
       '**For each task.** Ranking steps use the label of the task: ReliefF for the classes of Tasks A and B, RReliefF for the DI of Task C. Band selection (SHAP-CARS) and mRMR use the DI, as Ma et al. (2026) used severity. The VIF step is done for each task, so each camera has three DSFs.')
    myfig('chain', 'g10_selection_chain.png', 'Feature selection of each camera separately.', width=600)
    rows = [['Camera', 'Group (candidates)', 'Selection inside the group, in order', 'Kept'],
            ['Hyperspectral', 'bands R + FD (966)', 'NDSI/RSI R² maps → effective ranges → SHAP top 40% → CARS', 'OW 10–15'],
            ['', 'indices: 48 + 3 red-edge + NDSI, RSI, WRI', '|r| ≥ 0.95 filter → ReliefF / RReliefF', '5'],
            ['', 'texture: PCA-GLCM (24)', '|r| ≥ 0.95 filter → mRMR → TTFI', '6 + TTFI'],
            ['Multispectral', '5 bands + 12 indices + best ND (18)', '|r| ≥ 0.95 filter → ReliefF / RReliefF', '5'],
            ['', 'texture: GLCM of 5 bands (40)', '|r| ≥ 0.95 filter → mRMR → TTFI-MS', '6 + TTFI'],
            ['RGB', 'colour: 6 indices + H, S, V (9)', '|r| ≥ 0.95 filter → ReliefF / RReliefF', '5'],
            ['', 'texture: GLCM of R, G, B (24)', '|r| ≥ 0.95 filter → mRMR → TTFI-RGB', '6 + TTFI'],
            ['Thermal', 'statistics, normalised, texture (18)', '|r| ≥ 0.95 filter → ReliefF / RReliefF; 4 normalised temperatures always kept', '5 + 4'],
            ['Each camera', 'pooled survivors', 'VIF: remove the largest until all < 10', 'DSF']]
    tab('camsel', rows=rows, caption='Selection of each camera (for each task, on the training plots).', widths=[1400, 2700, 4300, 1200], size=15)

    h2('8.2 Hyperspectral bands: from 966 bands to 10–15 optimal wavelengths')
    h3('Step 7.1 – Band-pair maps and effective ranges (1.2.1)')
    p('For every pair of bands i and j (every second band, about 29 000 pairs), two indices are computed for all training samples and their coefficient of determination R² with the DI is drawn as a map ({F:ndsi}):')
    eq('NDSI(i, j) = (R_{i} − R_{j}) / (R_{i} + R_{j})     RSI(i, j) = R_{i} / R_{j}')
    p('Bands that take part in pairs with **R² > 0.5 in both maps** form the effective wavelength ranges; if no pair reaches 0.5, the pairs in the top 5% of R² are used. Ma et al. (2026) found effective ranges of 455–503, 520–661 and 702–1000 nm for rice blast with the same 0.5 rule; Mandal et al. (2023) drew the same kind of maps on their calibration data only, and Tian et al. (2021) kept the top 5% of features. The best NDSI and RSI pairs are kept for Step 7.3.')
    myfig('ndsi', 'g08_ndsi_demo.png', 'Demo NDSI R² map; the white line marks R² = 0.5, the limit of the effective ranges.', width=360)
    h3('Step 7.2 – Optimal wavelengths by SHAP-CARS (1.2.2)')
    p('The candidates are the reflectance and first-derivative bands inside the effective ranges. Three steps follow ({F:shap}):')
    nl('**SHAP ranking.** A random forest (500 trees; Breiman, 2001) predicts the DI from the candidate bands. Shapley additive explanations (SHAP; Lundberg and Lee, 2017) give, for every sample, the contribution of every band to the prediction; the mean absolute SHAP value of a band is its importance. The top 40% of bands are kept.',
       '**Number of PLS components.** The kept bands are standardised (z-score; PLS is scale-sensitive and reflectance and first derivative differ by about 100 times). Monte Carlo cross-validation (50 random 80/20 divisions by plot) chooses the number of partial least squares (PLS) components (1–15) with the lowest error.',
       '**CARS.** Competitive adaptive reweighted sampling (Li et al., 2009) runs 50 iterations. In each iteration a PLS model is fitted on a random subset of samples, bands with small PLS coefficients are removed (the number kept falls exponentially), and the remaining bands are re-sampled with weights proportional to their coefficients. Each iteration leaves a smaller band subset; the subset with the lowest GroupKFold(3) RMSE is the set of **optimal wavelengths (OW)**, usually 10–15 bands labelled R_{λ} or FD_{λ}.')
    p('This is the SHAP-CARS procedure of Ma et al. (2026), who kept 12 key wavelengths for rice blast. SHAP removes uninformative bands first; CARS then removes bands that repeat each other.')
    myfig('shap', 'g09_shapcars_demo.png', 'Demo of SHAP-CARS: (a) mean |SHAP| of candidate bands, top 40% in blue; (b) GroupKFold(3) RMSE of the CARS subsets over 50 iterations; the lowest RMSE gives the optimal wavelengths.')

    h2('8.3 Hyperspectral indices: data-driven indices, then redundancy filter and ReliefF')
    h3('Step 7.3 – Best NDSI and RSI and the White Rust Index (1.3.1–1.3.2)')
    p('The highest-R² NDSI and RSI pairs of Step 7.1 (bands at least 10 nm apart) become two data-driven indices, as Mandal et al. (2023) made the rice blast indices RBI and NDBI from the best band pair. '
      'A three-band **White Rust Index** is then searched in the form of the spectral disease indices of Mahlein et al. (2013):')
    eq('WRI = (R_{λ1} − R_{λ2}) / (R_{λ1} + R_{λ2}) + w × R_{λ3}')
    p('Bands are taken at 6-nm steps inside the effective ranges, λ_{1} and λ_{2} are at least 50 nm apart and w ∈ {−1, −0.5, 0, 0.5, 1}, all as in Mahlein et al. (2013). Each candidate is scored by |r| with the DI and by the balanced accuracy of healthy vs diseased with one optimised threshold; the best formula is kept, and the search is repeated once with SWIR bands. The wavelengths are fixed on the training plots and the index is then computed for every sample.')
    rows = [['Rank', 'λ1 (nm)', 'λ2 (nm)', 'λ3 (nm)', 'w', '|r| with DI', 'Balanced accuracy'], ['1', '754', '700', '532', '−0.5', '0.71', '0.83'], ['2', '760', '694', '550', '−0.5', '0.70', '0.82'], ['3', '790', '718', '—', '0', '0.68', '0.80']]
    tab('wri', rows=rows, caption='Demo output of the WRI search.', widths=[900, 1300, 1300, 1300, 900, 1700, 2200], size=16)
    h3('Step 7.4 – Redundancy filter of the indices (1.4.1)')
    p('The 48 published indices, 3 red-edge parameters, NDSI_best, RSI_best and WRI are correlated with each other; indices with |r| ≥ 0.95 form clusters, and from each cluster only the index with the highest |r| with the DI is kept. Many published indices are near-copies (for example the NDVI family), and ReliefF ranks are unreliable among near-identical features (Ma et al., 2026; Lv et al., 2023).')
    h3('Step 7.5 – ReliefF ranking (1.4.2)')
    p('The remaining indices are scaled to 0–1 (min–max) and ranked by **ReliefF** (Tasks A and B) or **RReliefF** (Task C) with k = 10 neighbours (Kononenko, 1994; Robnik-Šikonja and Kononenko, 2003). For a sample, ReliefF finds its 10 nearest samples of the same class ("hits") and of each other class ("misses"). A feature gains weight when it differs between the sample and its misses and loses weight when it differs between the sample and its hits:')
    eq('W(f) ← W(f) − diff(f, x, hit) / (m × k) + diff(f, x, miss) / (m × k)')
    p('where diff is the scaled difference of feature f between two samples and m the number of samples visited. A good feature therefore separates classes among similar samples. The **top five** indices per task are the selected indices (VI), as Ma et al. (2026) kept the five Relief-ranked indices and Mahlein et al. (2013) used RELIEF-F for disease features.')
    box('Worked example', 'A diseased sample has NDRE 0.22 (scaled 0.20); its nearest healthy samples (misses) have scaled NDRE 0.65 and its nearest diseased samples (hits) 0.24. The large miss difference (0.45) and small hit difference (0.04) raise the weight of NDRE. An index that differs equally between hits and misses gains nothing.', kind='note')

    h2('8.4 Hyperspectral texture: mRMR and the Tri-band Texture Fusion Index')
    h3('Step 7.6 – mRMR selection of texture (1.5.1)')
    p('The 24 PCA texture features are first filtered at |r| ≥ 0.95. **Minimum redundancy maximum relevance** (mRMR; Peng et al., 2005) then adds, one at a time, the feature with the largest relevance to the DI minus its mean redundancy with the features already chosen, both measured by mutual information I:')
    eq('score(f) = I(f; DI) − (1/|S|) Σ_{s ∈ S} I(f; s)')
    p('The **top six** (TF1–TF6) are kept, the number and method of Ma et al. (2026); Yuan et al. (2025) also used mRMR for UAV disease features.')
    h3('Step 7.7 – Tri-band Texture Fusion Index (1.5.2)')
    p('All ordered triplets of TF1–TF6 (6 × 5 × 4 = 120) are combined with three formulas (360 candidates); the candidate with the highest |r| with the DI is the TTFI (Ma et al., 2026, where TTFI3 reached |r| = 0.756):')
    eq('TTFI1 = (TF1 + TF2) / TF3     TTFI2 = TF1 × TF2 / TF3     TTFI3 = TF1 × (TF1 + TF2) / (TF2 + TF3)')
    box('Worked example', 'TF1 = 0.8, TF2 = 1.2, TF3 = 0.5: TTFI1 = 2.0/0.5 = 4.00; TTFI2 = 0.96/0.5 = 1.92; TTFI3 = 0.8 × 2.0/1.7 = 0.94.', kind='note')

    h2('8.5 Multispectral, RGB and thermal cameras')
    h3('Step 7.8 – Multispectral camera (1.3.3, 1.6.2)')
    nl('The 10 two-band normalised differences of the five bands are correlated with the DI and the best one (MS_NDbest) is added (1.3.3).',
       '**Spectral group** (5 bands + 12 indices + MS_NDbest = 18): |r| ≥ 0.95 filter → min–max scaling → ReliefF / RReliefF (k = 10) → top five. Five bands are too few for SHAP-CARS, so they compete with the indices.',
       '**Texture group** (40): |r| ≥ 0.95 filter → mRMR → top six → TTFI-MS with the 120 triplets and three formulas of Step 7.7.',
       'Pool 5 + 6 + 1 = 12 candidates → Step 7.11.')
    p('Liu et al. (2024) used multispectral band reflectance, vegetation indices and three-band texture combination indices built from the 40 textures (5 bands × 8 GLCM measures) for wheat powdery mildew; Nguyen et al. (2023) found multispectral indices and GLCM contrast most related to yellow rust.')
    h3('Step 7.9 – RGB camera (1.6.3)')
    nl('**Colour group** (9): |r| ≥ 0.95 filter → ReliefF / RReliefF → top five.',
       '**Texture group** (24): |r| ≥ 0.95 filter → mRMR → top six → TTFI-RGB.',
       'Pool 12 candidates → Step 7.11.')
    p('Huang et al. (2020) screened colour features and texture features separately before fusing them with spectral bands for Fusarium head blight; Feng et al. (2022) used RGB texture as its own data source.')
    h3('Step 7.10 – Thermal camera (1.6.4)')
    nl('The 6 statistics and 8 texture features are filtered at |r| ≥ 0.95 and ranked by ReliefF / RReliefF; the top five are kept.',
       'The four normalised temperatures (CTD, CTR, NRCT, ΔT) are always passed on, because raw temperatures follow the weather of the flight (Oerke et al., 2006; Calderón et al., 2013).',
       'Pool at most 9 candidates → Step 7.11, where VIF removes the collinear ones (CTD and CTR, for example, are almost the same).')
    p('Feng et al. (2022) used canopy temperature parameters and thermal texture as one data source; Maimaitijiang et al. (2020) used NRCT as the thermal feature of their UAV thermal camera.')

    h2('8.6 The disease-specific feature set of each camera')
    h3('Step 7.11 – Variance inflation factor (1.6.5)')
    p('For each camera and task the candidates are pooled. For every feature j, a linear regression of j on the other candidates gives R_{j}^{2}, and')
    eq('VIF_{j} = 1 / (1 − R_{j}^{2})')
    p('The feature with the largest VIF is removed, VIF is recomputed, and this is repeated until all VIF < 10. The remaining features are the **DSF** of the camera and task. VIF < 10 is the rule of Lv et al. (2023), Tian et al. (2021) and Mustafa et al. (2023), who all applied it before SFFS.')
    rows = [['Round', 'Largest VIF', 'Feature removed', 'Features left'], ['1', '86.4', 'FD_722', '26'], ['2', '31.2', 'NDVI780', '25'], ['3', '14.8', 'PC2-Var', '24'], ['…', '…', '…', '…'], ['12', '8.9 (< 10)', '—', '15 = DSF of the HS camera']]
    tab('vif', rows=rows, caption='Demo of the VIF elimination for the hyperspectral camera (Task C).', widths=[1200, 2200, 3000, 3200], size=16)
    rows = [['Camera', 'Candidates', 'DSF (Task C, demo)', 'Size'],
            ['Hyperspectral', '27', 'R_{560}, FD_{716}, FD_{742}, R_{1450}, WRI, PSRI, CI_{rededge}, PC2-Mea, PC2-Con, TTFI …', '15'],
            ['Multispectral', '12', 'NDRE, PSRI, MTCI, RE band, NIR-Con, RE-Hom, TTFI-MS', '7'],
            ['RGB', '12', 'ExG − ExR, VARI, saturation, G-Ent, R-Con, TTFI-RGB', '6'],
            ['Thermal', '9', 'CTD, NRCT, ΔT, MTD', '4']]
    tab('dsf', rows=rows, caption='Demo DSF of each camera – the output of Objective 1 that Objective 2 uses.', widths=[1600, 1300, 5300, 1400], size=15)
    h3('Step 7.12 – Stability across growth stages and severity (1.6.6)')
    p('Every DSF feature is then **described** (all 48 plots) within the vegetative, flowering and pod-formation stages: t-test of plot means healthy vs diseased, Pearson r with the DI and box plots by DI class. A feature is stable if it is significant with the same sign in all three stages. Tian et al. (2021) kept only features that were sensitive on every day after inoculation, Liu et al. (2024) found that only NDRE, PSRI and MTCI followed powdery mildew consistently in the middle and late stages, and Zhang et al. (2024) showed that the important bands change between disease stages.')
    h3('Step 7.13 – Complementarity of the cameras (1.6.7)')
    p('The correlation between the DSFs of different cameras shows whether the cameras carry different information. Low correlation between cameras means fusion may help (Mahlein et al., 2019; Feng et al., 2022); this expectation is checked in Objective 2.')
    box('On a new data set', 'In a new season analysed on its own, repeat the whole selection on its training plots – the DSFs may differ. When frozen 2026-27 models are tested on new data, do not select again: compute exactly the 2026-27 DSF features (same wavelengths, formulas and triplets) for the new samples.', kind='present')
