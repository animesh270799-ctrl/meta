from k0_lib import *
import k5b_obj1_results


def add():
    # ---------------------------------------------------------------- Step 6
    h1('4. Steps 6–7: pre-processing and the Objective 1 description')
    p('Step 6 turns every raw spectrum into the same set of numbers (bands, derivatives, indices). Step 7 uses these numbers to describe how white rust changes the spectrum. '
      'Both steps use ALL 2330 leaves. This is safe for two different reasons: Step 6 treats each leaf on its own, and Step 7 is a description whose selected features are '
      '**not** given to the models – the models get their features from Step 8, which repeats the selection on the training plots only.')
    h2('4.1 What a leaf spectrum contains')
    bl('**Visible, 400–700 nm:** absorbed by chlorophyll and carotenoids; a small green peak near 550 nm.',
       '**Red edge, 680–760 nm:** the steep rise from red absorption to the near-infrared plateau; its position and slope follow chlorophyll content.',
       '**Near infrared, 760–1300 nm:** high reflectance from scattering in the mesophyll; it falls when the leaf structure is damaged.',
       '**Shortwave infrared, 1300–2500 nm:** controlled mainly by leaf water (bands near 1450 and 1940 nm) and dry matter (Jacquemoud and Ustin, 2019; Mahlein, 2016).')
    h2('4.2 Step 6 – Pre-processing and index features')
    card('card6', '6', 'Pre-processing and index features',
         'Remove noise and offsets, and describe every leaf by the same bands, derivatives and indices.',
         'ALL 2330 leaves, each processed on its own (no mean, scale or parameter is estimated from other leaves).',
         '1-nm reflectance 350–2500 nm (X_leaf.npy).',
         steps('Savitzky–Golay smoothing, window 11 nm, polynomial order 2, on 350–2500 nm.',
               'First derivative with the same filter (units 10^{−3} per nm).',
               'Trim to 400–2400 nm (noisy detector ends removed); water bands 1350–1460 and 1790–1960 nm KEPT.',
               'Take every 5th nm: 401 reflectance bands (R400 … R2400) and 401 derivative bands (FD400 … FD2400).',
               'From the smoothed 1-nm spectrum compute 41 published indices and three red-edge parameters: REP (wavelength of the largest slope 680–760 nm), Dr (that slope) and REarea.'),
         'No second derivative (it amplifies noise). Indices, REP, Dr and REarea are computed from 1-nm data, not from the 5-nm bands.',
         '802 bands + 44 index features per leaf (prep.npz, indices.csv) → Step 7 (description) and Step 8 (selection for the models). Step 8 adds NDSI_best, RSI_best and WRI found on TRAIN → 47 index features.',
         'a1_prep.py; wr_features.py (the same functions are used by the prediction script for new spectra).',
         'Savitzky and Golay (1964); Tsai and Philpot (1998); index references in report Table 13.',
         '14; appendix 86–90',
         'Keep the same filter and grid, so that saved models can be applied. For UAV cameras with fewer bands, compute only the indices whose bands exist.')
    tab('prepcard', 12, widths=[2200, 7400], size=17, boldfirst=True, subs=True)
    read(why=['The detector ends are noisy; smoothing removes random fluctuations without changing the shape.',
              'The first derivative removes constant offsets (a brighter or thicker leaf) and turns the red edge into a peak whose height and position can be measured.'],
         done=['The water-absorption regions were kept: the probe has its own lamp and touches the leaf, so there is no atmospheric water in the light path, and these regions carry information on leaf water.'],
         means='After this step every leaf is described by 802 band values and 44 index features. Neighbouring bands are highly correlated, which is why selection is needed.',
         say='"I smoothed the spectra, kept 400–2400 nm including the water bands, and used reflectance and its first derivative at 5-nm steps."')
    box('Notation.', ['**R_{λ}** = reflectance at λ nm (e.g. R_{800}); **FDλ** = first derivative at λ nm (e.g. FD870).',
                      '**REP** = red-edge position; **Dr** = height of the red-edge slope; **REarea** = area under the red-edge derivative.',
                      '**OW** = optimal wavelengths (SHAP-CARS); **VI** = selected indices (ReliefF); **DSF** = disease-specific feature set (after VIF).'], kind='note')
    tab('indices', 13, widths=[1300, 4900, 2200, 1200], size=16, subs=True)
    read(shows='Every index, its formula, its source and its Pearson r with the grade over all 2330 leaves.',
         how='Negative r: the index falls as disease increases; |r| above about 0.5 is strong for single leaves.',
         found=['Strongest negative: HI (−0.54), PSSRb (−0.53), SR, RVI, MSR, PSSRa (−0.51), REP (−0.50).',
                'Strongest positive: RVSI (+0.56) and ARI (+0.53). Weak: MCARI, TCARI, PSSRc, GNDVI, CIgreen (|r| ≤ 0.16).'],
         means='The best single index explains about 30% of the variation of the grade (0.54² ≈ 0.29). No single index is enough, so a combination is selected.',
         caution='These r values are computed on all leaves and are descriptive. They are not used to choose the model inputs.',
         say='"The best published indices – HI, PSSRb, REP, RVSI – reach about |r| = 0.5; useful, but not enough alone."')

    # ---------------------------------------------------------------- Step 7
    h2('4.3 Step 7 – Objective 1 description on all leaves')
    card('card7', '7', 'Objective 1: spectral response and disease-specific features (description)',
         'Show where and how white rust changes the leaf spectrum, and which compact set of features describes it (thesis Objective 1).',
         'ALL 2330 leaves (descriptive). The resulting feature lists are reported, but the models do NOT use them; Step 8 repeats the selection on TRAIN.',
         '5-nm bands and derivatives, 44 index features (Step 6); grade of every leaf.',
         steps('Response (Activity 1.1): mean ± SD reflectance and derivative per grade; Pearson r of every band with the grade; spectra per growth stage; mean grade per factor.',
               'Effective ranges (1.2.1): R² of NDSI and RSI with the grade for all 80 200 band pairs; bands in pairs with R² ≥ 0.5, else in the top 5% of pairs.',
               'Optimal wavelengths (1.2.2–1.2.4): candidates = R and FD bands in the effective ranges + red-edge FD 680–760 nm; XGBoost SHAP keeps the top 40%; Monte Carlo CV chooses the PLS components; CARS 50 iterations × 20 runs; bands chosen in ≥ 50% of runs (max 15) = OW.',
               'Indices (1.3): best NDSI and RSI pair (≥ 10 nm apart); WRI = NDSI(λ1, λ2) + w·R(λ3) searched over the 200 best NDSI pairs (≥ 50 nm apart), λ3 every 10 nm, w ∈ {−1, −0.5, 0, 0.5, 1}.',
               'Index selection (1.4): of the 47 index features keep one per cluster with |r| ≥ 0.95 (the one closest to the grade); ReliefF (A, B) and RReliefF (C), k = 10 neighbours, neighbours of the same plot excluded; top 5 per task = VI.',
               'Collinearity (1.6): pool OW + VI; remove the feature with the largest VIF until all VIF < 10 = DSF.',
               'PCA of reflectance (scores by grade, 95% ellipses).'),
         'XGBoost 300 trees, depth 4, learning rate 0.05, subsample 0.8; MCCV 50 splits (80/20) for 1–15 PLS components; CARS seeds 42 + run.',
         'Figures 5–18 and Tables 23–25 of the report; o1_results.json. Used in the discussion (physical meaning) and to cross-check Step 8.',
         'a2_obj1.py; alib.py (r2_maps, effective_ranges, shap_cars, wri_search, corr_filter, relieff, vif_filter).',
         'Ma et al. (2026); Li et al. (2009); Lundberg and Lee (2017); Robnik-Šikonja and Kononenko (2003); Dormann et al. (2013).',
         '15, 22–35; appendix 91–94, 99–102, 132–137',
         'Run unchanged. If no band pair reaches R² 0.5 the top-5% rule is applied automatically (here R² ≥ 0.228).')
    tab('o11card', 14, widths=[2200, 7400], size=17, boldfirst=True)
    read(why='Model-free evidence first: does the spectrum change with disease, where, and in which direction?',
         means='These curves are the basis for the physical interpretation of every later result.',
         say='"First I simply looked at how the average spectrum of each grade differs."')
    tab('o12card', 15, widths=[2200, 7400], size=17, boldfirst=True)
    bl('**NDSI and RSI maps.** For every band pair, NDSI = (R_{λ1} − R_{λ2})/(R_{λ1} + R_{λ2}) and RSI = R_{λ1}/R_{λ2}; their R² with the grade is drawn as a map. Bright areas = band combinations that follow the disease.',
       '**SHAP.** An XGBoost model predicts the grade from all candidate bands; SHAP gives each band its average contribution (Lundberg and Lee, 2017). The top 40% are kept.',
       '**PLS.** Partial least squares compresses correlated bands into a few components; their number is chosen by Monte Carlo cross-validation.',
       '**CARS.** Competitive adaptive reweighted sampling repeatedly fits PLS, drops bands with small coefficients and keeps the subset with the lowest cross-validated error (Li et al., 2009). '
       'Twenty runs and a 50% stability rule make the result reproducible.')
    read(why='802 correlated bands cannot be given directly to a model; SHAP removes uninformative bands so that CARS works on a smaller, relevant set (Ma et al., 2026).',
         means='Output: the optimal wavelengths (OW).',
         say='"Band-pair maps showed where the signal is; SHAP and CARS picked the 15 most informative bands."')
    tab('o13card', 16, widths=[2200, 7400], size=17, boldfirst=True)
    read(why='Indices are easy to interpret and transfer to other sensors. ReliefF looks at each leaf and its nearest neighbours: a good index is similar for neighbours of the same grade and '
             'different for neighbours of another grade (Robnik-Šikonja and Kononenko, 2003). Excluding neighbours from the same plot stops plot similarity from inflating the weights.',
         means='Output: the selected indices (VI) for detection, six grades and score.',
         say='"I built a White Rust Index and let ReliefF pick the five most useful indices for each task."')
    tab('o16card', 17, widths=[2200, 7400], size=17, boldfirst=True)
    eq('VIF_{j} = 1 / (1 − R_{j}^{2})')
    p('R_{j}^{2} is the R² when feature j is predicted from all other features. VIF = 10 means 90% of its variation is already in the others. The feature with the largest VIF is removed '
      'one at a time until all are below 10 (Dormann et al., 2013).')
    read(why='Collinear inputs make models unstable and explanations unreliable.',
         means='Output: the disease-specific feature set (DSF), the compact input of Objective 2.',
         say='"I removed overlapping features until each carried its own information."')
    box('Two feature sets with the same name – which one do the models use?', [
        '**DSF of Step 7 (all leaves, report Table 25):** FD1090, FD1060, FD550, FD1245, FD870, FD760, FD665, FD595, DWSI-2, Dr, REP – one pooled set that describes the disease.',
        '**DSF of Step 8 (training plots, report Table 26):** one set per task, e.g. six grades: FD550, FD595, FD1810, FD1245, FD760, FD1060, FD1075, FD860, FD985, REP, PSSRb. '
        '**These are the model inputs.** The two lists share the same regions (green peak, red edge, NIR shoulder, NIR–SWIR water edges), but not every band, because the selection is '
        'run on different leaves and CARS chooses one of several nearly equivalent neighbouring bands.'], kind='caution')
    k5b_obj1_results.results()
