from dsl import *


def add():
    h1('4. Pre-processing and spectral features')
    h2('4.1 What a leaf spectrum contains')
    p('A reflectance spectrum gives, for every wavelength, the fraction of light that the leaf reflects. Different parts of the spectrum respond to different leaf properties '
      '(Jacquemoud and Ustin, 2019; Mahlein, 2016):')
    bl('**Visible, 400–700 nm:** absorbed by chlorophyll and carotenoids; reflectance is low except for a small green peak near 550 nm.',
       '**Red edge, 680–760 nm:** the steep rise from the red absorption to the near-infrared plateau. Its position and slope depend on chlorophyll content and are among the '
       'most sensitive indicators of plant stress.',
       '**Near infrared (NIR), 760–1300 nm:** high reflectance caused by scattering at cell walls and air spaces in the mesophyll; it falls when the leaf structure is damaged.',
       '**Shortwave infrared (SWIR), 1300–2500 nm:** controlled mainly by leaf water (absorption bands near 1450 and 1940 nm) and by dry matter; reflectance rises when the leaf loses water.')
    box('In simple words.', 'White rust removes chlorophyll (visible and red edge change), damages the cells around the pustules (NIR changes) and dries the tissue (SWIR changes). '
        'A leaf spectrum can therefore "see" the disease in three different ways.', kind='key')
    h2('4.2 Smoothing, trimming and the first derivative')
    tab('prepcard', 10, widths=[2200, 7400], size=17, boldfirst=True, subs=True)
    read(why=['The two ends of the detector range (350–399 nm and 2401–2500 nm) are noisy and were trimmed.',
              'Smoothing removes small random fluctuations without changing the shape of the spectrum.',
              'The first derivative (the slope of the spectrum) removes constant offsets – for example a slightly brighter or thicker leaf – and turns the red edge into a sharp peak '
              'whose height and position can be measured.'],
         done=['Savitzky–Golay filter with an 11-nm window and a second-order polynomial (Savitzky and Golay, 1964), applied to 350–2500 nm and then trimmed to 400–2400 nm.',
               'First derivative from the same filter, in units of 10^{−3} per nm.',
               'Bands taken every 5 nm: 401 reflectance values (R_{400} … R_{2400}) and 401 derivative values (FD400 … FD2400) per leaf.',
               'The water-absorption regions (1350–1460 and 1790–1960 nm) were **kept**: the probe uses its own lamp and touches the leaf, so there is no atmospheric water in the light path, '
               'and these regions carry information on leaf water.'],
         means='After this step every leaf is described by 802 numbers. They are highly correlated with their neighbours, which is why the selection steps of Objective 1 are needed.',
         say='"I smoothed the spectra, kept 400–2400 nm including the water bands, and used both reflectance and its first derivative at 5-nm steps."')
    box('Notation used in the rest of the document.', ['**R_{λ}** = reflectance at wavelength λ nm (for example R_{800}).',
                                                       '**FDλ** = first derivative at λ nm (for example FD870 is the slope of the spectrum at 870 nm).',
                                                       '**REP** = red-edge position (wavelength of the largest slope between 680 and 760 nm); **Dr** = height of that slope; **REarea** = area under the red-edge derivative.'], kind='note')
    h2('4.3 Vegetation indices')
    p('A vegetation index combines two or three bands in a formula designed to respond to one leaf property. Forty-one published indices and three red-edge parameters '
      '(44 features) were computed for every leaf from the smoothed 1-nm reflectance. They fall into five groups: greenness/structure indices (NDVI, SR, OSAVI, MTVI2 …), '
      'pigment indices (PSSR, SIPI, NPCI, PSRI, ARI, PRI), red-edge indices (CIrededge, NDRE, MTCI, REP, Dr, REarea), water indices (WI, WBI, NDWI, MoistSI, NDII) and '
      'disease indices (DWSI-1 to 5, HI, RVSI, RBI, NDBI).')
    tab('indices', 11, widths=[1300, 4900, 2200, 1200], size=16, subs=True)
    read(shows='Every index computed, its formula, the paper that proposed it, and its Pearson correlation r with the leaf grade across all 2330 leaves.',
         how='r ranges from −1 to +1. A negative r means the index falls as disease increases; a positive r means it rises. |r| above about 0.5 is a strong relationship for '
             'single leaves; |r| below 0.2 means the index hardly follows the grade.',
         found=['Strongest negative: the Healthy Index HI (−0.54), PSSRb (−0.53), SR, RVI, MSR and PSSRa (−0.51), REP (−0.50) and the NDVI family (−0.48 to −0.49).',
                'Strongest positive: RVSI (+0.56, red-edge vegetation stress index) and ARI (+0.53, anthocyanin reflectance index).',
                'Water indices were moderate (|r| 0.37–0.40); MCARI, TCARI, PSSRc, GNDVI and CIgreen were weak (|r| ≤ 0.16).'],
         means='The best single published index explains only about 30% of the variation in grade (r² = 0.54² ≈ 0.29). Indices that contrast red or red-edge with NIR work best, '
               'confirming that chlorophyll loss and structural change are the main signals. Green-based indices (GNDVI, CIgreen) respond weakly because the green peak changed '
               'little (Table of mean reflectance, Chapter 7.2). No single index is enough, which is why the analysis goes on to select a combination of features.',
         say='"The best published indices – HI, PSSRb, REP and RVSI – correlate at about |r| = 0.5 with the grade; useful, but no single index is enough."')

    h1('5. Objective 1 methods: finding the disease-specific features')
    p('Objective 1 follows the steps of the DT-EDNet rice-blast study (Ma et al., 2026). The idea is to go from 802 bands and 44 indices to a small set of features that '
      'carry the disease signal and are not redundant. Four activities do this, each summarised in a "step card" from the report.')
    h2('5.1 Activity 1.1 – Response analysis')
    tab('o11card', 12, widths=[2200, 7400], size=17, boldfirst=True)
    read(why='Before any model, the raw evidence: does the spectrum change with disease, where, and in which direction? This is model-free and easy to check.',
         done='Mean reflectance and mean derivative of each grade (± SD) over 400–2400 nm; Pearson r of every 5-nm band with the grade; mean spectra within each growth stage; '
              'mean grade by stage, variety, leaf position and sowing timing.',
         means='These curves are the basis for all later selection steps and for the physical interpretation in the discussion.',
         say='"First I simply looked at how the average spectrum of each grade differs."')
    h2('5.2 Activity 1.2 – Effective ranges and optimal wavelengths (SHAP-CARS)')
    tab('o12card', 13, widths=[2200, 7400], size=17, boldfirst=True)
    p('This activity uses four techniques. Each is explained here in plain terms:')
    bl('**NDSI and RSI maps.** For every pair of bands (λ_{1}, λ_{2}) the normalised difference NDSI = (R_{λ1} − R_{λ2})/(R_{λ1} + R_{λ2}) and the ratio RSI = R_{λ1}/R_{λ2} are '
       'computed, and their R² with the grade is drawn as a coloured map. Bright areas show which band combinations follow the disease. The area above a threshold defines the '
       '"effective ranges" of wavelengths.',
       '**SHAP (Shapley additive explanations).** A gradient-boosting model (XGBoost) is trained to predict the grade from all candidate bands. SHAP measures how much each band '
       'contributes to the predictions, averaged over all leaves (Lundberg and Lee, 2017). Bands in the top 40% of mean |SHAP| are kept; the rest are discarded.',
       '**PLS (partial least squares).** A regression method that compresses many correlated bands into a few "latent components" that best predict the grade. Its number of '
       'components was chosen by Monte Carlo cross-validation (50 random splits).',
       '**CARS (competitive adaptive reweighted sampling).** Starting from the SHAP-screened bands, CARS repeatedly fits PLS, removes bands with small PLS coefficients and keeps the '
       'subset with the lowest cross-validated error (Li et al., 2009). Running CARS 20 times and keeping bands selected in at least half of the runs (maximum 15) makes the '
       'selection stable.')
    read(why='802 correlated bands cannot be given directly to a model: many are redundant and some are noise. SHAP removes uninformative bands first, so that CARS works on a '
             'smaller, relevant set and gives a more stable answer (Ma et al., 2026).',
         done=['Threshold for effective ranges: R² ≥ 0.5, or – if no pair reaches it – the top 5% of all pairs (used here: R² ≥ 0.228).',
               'Red-edge derivatives (680–760 nm) were always candidates, because of their known link to chlorophyll.',
               'XGBoost with 300 trees, depth 4, learning rate 0.05; bands standardised; CARS 50 iterations × 20 runs.'],
         means='The output is a list of **optimal wavelengths (OW)** – the individual bands that best describe the disease.',
         say='"Band-pair maps showed where the signal is; SHAP and CARS then picked the 15 most informative bands."')
    h2('5.3 Activities 1.3–1.4 – Index construction and ReliefF selection')
    tab('o13card', 14, widths=[2200, 7400], size=17, boldfirst=True)
    p('Three data-driven indices were added to the 44 published features: the best NDSI and RSI from the maps (NDSI_best, RSI_best) and a **White Rust Index (WRI)** that adds '
      'a weighted third band to the best two-band index: WRI = NDSI(λ_{1}, λ_{2}) + w·R_{λ3}. A third band can correct an effect that a two-band index cannot, for example leaf '
      'thickness. The search tried the 200 best NDSI pairs, every third band at 10-nm steps and five weights (w = −1, −0.5, 0, 0.5, 1).')
    p('Indices that were nearly identical (|r| ≥ 0.95 with each other) were reduced to the one most correlated with the grade. The remaining indices were ranked with '
      '**ReliefF** (for the classes) and **RReliefF** (for the score). ReliefF looks at each leaf and its nearest neighbours: a good index has similar values for neighbours of '
      'the same grade and different values for neighbours of a different grade (Kira and Rendell, 1992; Robnik-Šikonja and Kononenko, 2003). Unlike correlation, it can '
      'reward an index that is useful only together with others. Neighbours from the same plot were excluded so that plot similarity could not inflate the weights. The top '
      'five indices were kept for each task.')
    read(why='Indices summarise physiology in a form that is easy to interpret and to transfer to other sensors; ReliefF chooses the indices that separate grades among similar leaves.',
         means='The output is the **selected indices (VI)** for detection, six grades and score.',
         say='"I built a White Rust Index and let ReliefF pick the five most useful indices for each task."')
    h2('5.4 Activity 1.6 – Variance inflation factor and the disease-specific feature set')
    tab('o16card', 15, widths=[2200, 7400], size=17, boldfirst=True)
    eq('VIF_{j} = 1 / (1 − R_{j}^{2})')
    p('Here R_{j}^{2} is the R² obtained when feature j is predicted from all the other features. A VIF of 1 means the feature is independent of the others; a VIF of 10 means '
      '90% of its variation is already contained in the others. The feature with the largest VIF was removed one at a time until all VIFs were below 10 (Dormann et al., 2013).')
    read(why='Optimal wavelengths and indices overlap (several derivative bands near 800–870 nm carry almost the same information). Strongly collinear inputs make models unstable and '
             'make explanations (such as SHAP) unreliable.',
         means='The output is the **disease-specific feature set (DSF)**: a compact, non-redundant set of bands and indices that is the main input of Objective 2.',
         say='"Finally I removed overlapping features until each one carried its own information; the result is an 11-feature disease-specific set."')
    box('Important: selection was repeated inside each fold.', 'For the final description of the signal (Chapter 7) the selection was run once on all leaves. For the models '
        '(Chapter 8) the whole selection – maps, SHAP-CARS, ReliefF and VIF – was repeated inside the training part of each outer fold, so the test replication never influenced '
        'which features were used.', kind='method')
