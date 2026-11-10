K.push(H1('7. NRSC / SAC (ISRO) interview: questions and answers'));
K.push(P(`Interview panels at the National Remote Sensing Centre (NRSC, Hyderabad) and the Space Applications Centre (SAC, Ahmedabad) usually test remote-sensing fundamentals, data-quality problems and how a thesis connects to satellite missions. Each answer below has three parts: the concept, **how this thesis solves the problem**, and **how other researchers dealt with it**, with references.`));
K.push(H2('7.1 Hyperspectral data problems'));
QA3('Neighbouring hyperspectral bands are highly correlated. How do you deal with it?',
 'Adjacent bands are controlled by the same absorbers and structure and the sensor\'s spectral response overlaps, so they are near-duplicates (multicollinearity). This inflates the effective dimensionality, destabilises linear models and makes covariance matrices singular.',
 'I quantified it on my mustard ASD spectra (bands 10 nm apart: median r = 0.9997; 349 bands form only 18 regions with r ≥ 0.95) and then: keep one band per correlated region in the band-level analysis; use derivatives and band contrasts; average to 6 nm and keep combined bands 50 nm apart in the WRI search; remove remaining collinearity with VIF < 10; let ML-SFFS keep only non-redundant features; use PLSR for collinear predictors (Step 1.3).',
 'Tian et al. (2021) kept one representative feature per common feature region and applied VIF < 10; Mustafa et al. (2023) applied VIF after Boruta; Mahlein et al. (2013) reduced spectral resolution to 6 nm and set a 50 nm minimum distance; Bhattacharya and Chattopadhyay (2013) used single bands out of clusters of close bands in a stepwise discriminant analysis; Zhu et al. (2017) and Huang et al. (2020) used SPA, which selects wavelengths with minimum collinearity (Araújo et al., 2001); Shukla et al. (2024) and Krishna et al. (2014) used PLS loading weights.');
QA3('What is the Hughes phenomenon and how do you avoid it?',
 'For a fixed number of training samples, classification accuracy first rises and then falls as more features are added, because the parameters cannot be estimated reliably (Hughes, 1968).',
 'I have 8 flight dates × 72 plots = 576 plot-dates (about 432 post-symptomatic) but more than 1400 hyperspectral band features, so I reduce features in stages (band-level selection, Boruta, VIF, ML-SFFS) to fewer than ten per model and validate on held-out replications.',
 'Tian et al. (2021) showed that 2–4 ML-SFFS features were enough and up to 10% more accurate than all features; Mustafa et al. (2023) used Boruta → VIF → ML-SFFS; Zhu et al. (2017) reduced 512 bands to a few effective wavelengths.');
QA3('How do you deal with noisy bands and low signal-to-noise ratio?',
 'Detector edges and atmospheric water-vapour bands have very little signal, so their reflectance is mostly noise.',
 'I remove 1350–1450 and 1800–1950 nm and noisy sensor edges, smooth with Savitzky–Golay, and compute ROTI only if its 1982 nm band passes the noise check.',
 'Mahlein et al. (2013) restricted analysis to 450–950 nm for adequate SNR; Shukla et al. (2024) removed 350–400, 1301–1500, 1780–2050 and 2351–2500 nm; Ramalingam et al. (2026) used SNV and MSC normalisation and an isolation-forest outlier filter.');
QA3('Why use derivative spectra?',
 'First derivatives remove additive offsets and show slopes such as the red edge; second derivatives remove linear trends and separate overlapping absorption features (Tsai and Philpot, 1998).',
 'I compute FD and SD from the Savitzky–Golay fit for all 481 bands and include red-edge parameters (REP, Dr, SDr); derivative bands are also much less correlated than reflectance.',
 'Shukla et al. (2024) found sensitive aphid regions with FD and SD; Baranowski et al. (2015) classified Alternaria infection of oilseed rape best with second derivatives; Lv et al. (2023) improved severity classification by adding first derivatives; Mandal et al. (2022) used the red-edge peak amplitude for rice blast.');
K.push(H2('7.2 Radiometry, geometry and data quality'));
QA3('How do you correct UAV images radiometrically and atmospherically?',
 'At 30 m altitude the atmospheric path is short, so a full atmospheric model is not needed; the main task is converting digital numbers to reflectance and correcting changes in sunlight.',
 'I use the empirical line method with calibration panels imaged on every flight, the MicaSense downwelling irradiance sensor for changing light, white-reference calibration for the hyperspectral camera, and radiometric conversion of thermal data with emissivity, air temperature, humidity and height, checked against ground targets.',
 'Smith and Milton (1999) established the empirical line method; Aasen et al. (2018) review UAV spectroscopy calibration workflows; Maimaitijiang et al. (2020) calibrated the same FLIR thermal camera with ground targets.');
QA3('How do view-angle and BRDF effects affect your UAV mosaics?',
 'Reflectance depends on sun and view geometry (bidirectional reflectance distribution function); in a UAV mosaic, pixels come from different view angles and can show hot-spot or brightness gradients (Schaepman-Strub et al., 2006).',
 'Flights are at near-solar-noon (11:00–14:00 h) under clear sky with 85%/80% overlap, so the mosaic uses near-nadir parts of images; plot means over many pixels average the remaining effects, and control plots on every flight provide a within-flight reference.',
 'Aasen et al. (2018) discuss BRDF correction and recommend high overlap and near-nadir pixels for UAV spectroscopy; Guo et al. (2021) and Liu et al. (2024) flew around midday for the same reason.');
QA3('How do you handle mixed pixels of canopy, soil and shadow?',
 'A pixel that contains canopy and soil gives a mixed spectrum and temperature, which weakens the disease signal.',
 'I build one canopy mask per flight on the hyperspectral image (NDVI > 0.6 and spectral angle < 0.3 rad to a reference canopy spectrum), transfer it to the co-registered RGB, MS and thermal images with a one-pixel edge erosion, compute the HS plot spectrum as the average of the leaf-canopy endmembers among 30 extracted per plot (flower, soil and shadow endmembers removed; flower fraction kept as a covariate), and use a 0.5 m inner plot buffer; thresholds are checked on every flight because yellow flowers lower NDVI; SWIR pixels (about 36 cm) are used only if enough pure pixels remain.',
 'Kruse et al. (1993) introduced the spectral angle mapper; Feng et al. (2022) segmented canopy with K-means; Guo et al. (2021) used an NDVI mask and showed that pixel size strongly affects texture accuracy; Bhattacharya and Chattopadhyay (2013) used a LISS-IV crop mask; at satellite scale spectral unmixing separates mixed signals (Keshava and Mustard, 2002).');
QA3('How do you co-register four sensors with different pixel sizes?',
 'Products must refer to the same ground position, but resampling all sensors to one grid would blur the finest data.',
 'All orthomosaics use the same GNSS-surveyed ground control points, and features are extracted per plot polygon in each sensor\'s native resolution, so fusion happens at plot-feature level without resampling.',
 'Feng et al. (2022) and Maimaitijiang et al. (2020) also fused plot-level features from RGB, multispectral and thermal sensors.');
QA3('How do you make thermal data comparable between flights?',
 'Canopy temperature depends on air temperature, radiation, wind and humidity, which change between flights; raw temperature differences between dates are therefore not disease effects.',
 'I warm up the camera for 15–20 min, convert radiance with emissivity and meteorological data, and use normalised indices (CTD, CTR in kelvin, NRCT scaled within each image, MTD within the plot).',
 'Feng et al. (2022) used CT, CTD, CTR and NRCT; Liu et al. (2024) showed that canopy temperature tracks powdery-mildew DI; Mahlein et al. (2019) used MTD.');
K.push(H2('7.3 Disease-specific problems'));
QA3('How do you separate disease from water or nutrient stress?',
 'Chlorophyll loss, NIR decline and canopy warming are also caused by drought or nutrient deficiency, so a general stress index cannot identify the cause.',
 'The experiment has uniform irrigation and fertiliser and un-inoculated controls on every date; I build a White Rust Index specific to the disease, add disease–water indices (DWSI, ROTI), and check that warmer diseased plots do not have lower water status (thermal vs water index).',
 'Zhang et al. (2012b) found that only PhRI responded to yellow rust but not to nutrient stress; Bhattacharya and Chattopadhyay (2013) used the TVDI–NDWI space (canopy stress without soil-moisture stress = rot); Mahlein et al. (2013) designed indices that separate three sugar-beet diseases.');
QA3('Your severity classes overlap. How do you discriminate them?',
 'Classes cut from a continuous DI overlap near their limits, so methods that require non-overlapping classes fail.',
 'I use a correlation scalogram against DI (no class limits) with ReliefF (designed for overlapping classes), a disease-specific White Rust Index, a two-step stepwise discriminant analysis following Stage III of Bhattacharya and Chattopadhyay (2013), DI regression in parallel, and macro-F1 to show per-class performance.',
 'Tian et al. (2021) used separability thresholds, which suit non-overlapping stages; Meng et al. (2020) reached only 70% for three severity levels with ReliefF indices; Lv et al. (2023) improved severity classification by about 7% by combining features with ReliefF + SFFS; Mandal et al. (2023) used JM and found two adjacent blast levels inseparable.');
QA3('How do you discriminate between disease classes statistically?',
 'Discriminant analysis finds linear combinations of features that maximise between-class relative to within-class variance (Fisher, 1936); stepwise selection by Wilks\' lambda keeps the features that add separation.',
 'Step 1.5 uses the two-step design: a stepwise canonical discriminant analysis first on the robust bands of Step 1.3 and then on the indices (including the WRI), reporting Wilks\' lambda, the canonical correlation, a score plot and cross-validated accuracy.',
 'Bhattacharya and Chattopadhyay (2013) used this design on Hyperion data for mustard rot; Zhang et al. (2012a) used Fisher LDA for three powdery-mildew levels; Shukla et al. (2024) discriminated aphid grades with PCA/PLSR loading weights; Das et al. (2020) used CART, JM and QDA.');
QA3('How do you label plots before symptoms appear?',
 'Before symptoms DI = 0 everywhere, so the true state of an inoculated plot is unknown at the time of the flight.',
 'An inoculated plot is labelled infected only if symptoms later appear on it; controls are healthy; inoculated resistant plots that never show symptoms are excluded and reported separately.',
 'Tian et al. (2021) used the same retrospective labelling for rice blast; Zhu et al. (2017) and Terentev et al. (2023) used days after inoculation under controlled conditions.');
QA3('How reliable is your ground truth?',
 'Visual scores are subjective and sampled, so label noise limits the achievable accuracy.',
 'Leaves are scored on a 0–6 area scale at five points per plot by the same trained scorer, and DI is computed with the standard formula (Liu et al., 2024); class limits are explicit, and errors near limits are reported.',
 'Shukla et al. (2024) used expert entomologist ratings of aphid grade; Mandal et al. (2023) used the IRRI 0–9 blast scale; Bhattacharya and Chattopadhyay (2013) used incidence counts in fields.');
K.push(H2('7.4 Models, fusion and validation'));
QA3('How do you prevent over-optimistic accuracy?',
 'If test data influence feature selection or tuning, or if dates of the same plot are in both training and test sets, accuracy is inflated (selection bias and spatial/temporal dependence).',
 'Leave-one-replication-out cross-validation keeps all dates of a plot together; every selection and tuning step is repeated inside the training replications (nested CV); final testing is at Bharatpur and in farmers\' fields.',
 'Ambroise and McLachlan (2002) and Varma and Simon (2006) showed selection bias; Roberts et al. (2017) recommend block cross-validation for dependent data; Feng et al. (2022) validated on a separate experiment; Bohnenkamp et al. (2019) showed that feature sets do not transfer between scales.');
QA3('Which fusion strategy do you use and why?',
 'Fusion can be at data, feature or decision level; feature-level fusion lets features of different sensors interact in one model.',
 'I compare ML-SFFS feature-level fusion (small, interpretable feature sets) with DNN-F1 and DNN-F2 (learned fusion), for the 4-class and DI tasks and four sensor combinations (Step 2.3).',
 'Maimaitijiang et al. (2020) found DNN-F2 best for soybean yield; Mustafa et al. (2023) fused sensors with ML-SFFS; Feng et al. (2022) fused spectra, thermal and texture with RFR; Deng et al. (2024) used an end-to-end network; Mahlein et al. (2019) found that a third sensor did not improve accuracy.');
QA3('How do you handle unequal class sizes?',
 'A model can achieve high overall accuracy by ignoring a rare class.',
 'Class weights inversely proportional to class size, stratified folds, equal priors in discriminant analysis, and macro-F1 and kappa as main metrics.',
 'Lv et al. (2023) reported macro-F1 for severity classes; Mahlein et al. (2013) optimised balanced accuracy for their indices.');
QA3('Why not use a deep CNN on the images?',
 'Image CNNs learn features directly but need large labelled datasets.',
 'With 72 plots I use engineered, physically interpretable features and small DNNs only for fusion; a CNN is future work when more seasons are available.',
 'Deng et al. (2024) needed more than 180 million annotated pixels; Nguyen et al. (2023) reached 60–79% with a 3D-CNN for early yellow rust detection.');
QA3('How do you interpret your models?',
 'Interpretation shows whether a model uses physically meaningful signals or artefacts.',
 'ML-SFFS gives small feature sets whose sensor origin and physiology are known; discriminant coefficients and structure correlations show which features separate classes; RF importance is read on the final set; features are correlated with pigments, RWC and stomatal conductance.',
 'Mustafa et al. (2023) interpreted the selected cross-sensor features; Mahlein et al. (2019) correlated sensor parameters with each other and with disease severity; Maimaitijiang et al. (2020) noted that DNNs are less interpretable.');
K.push(H2('7.5 Linking to ISRO missions and applications'));
QA3('How can your UAV results be scaled to satellites?',
 'Satellite pixels (5.8–30 m for optical Indian and international sensors) mix many plants and soil, so UAV relations must be translated to coarser pixels and broader bands.',
 'I identify a minimal set of bands and indices, check which are available on satellite sensors, and use the UAV maps as reference data for training and validating satellite models.',
 'Bhattacharya and Chattopadhyay (2013) mapped mustard rot with 30 m Hyperion data inside a 5.8 m LISS-IV crop mask; Shukla et al. (2024) proposed transferring their bands to aerial and satellite sensors; Bohnenkamp et al. (2019) warned that feature sets do not transfer automatically between scales.');
QA3('Which ISRO sensors could use your findings?',
 'Indian sensors differ in spectral coverage: Resourcesat LISS-IV (5.8 m; green, red, NIR), LISS-III (23.5 m, including SWIR) and AWiFS (56 m); HySIS is a VNIR + SWIR hyperspectral imager (about 30 m); TRISHNA is a planned ISRO–CNES thermal mission.',
 'Indices that need only green, red and NIR can be tested on LISS-IV; red-edge indices need Sentinel-2-type bands; the WRI and SWIR indices need HySIS-type data; thermal features need high-resolution thermal data such as TRISHNA.',
 'Bhattacharya and Chattopadhyay (2013) combined Hyperion and LISS-IV; Liu et al. (2024) used multispectral bands similar to satellite red-edge bands.');
QA3('If SAC designed a sensor for crop-disease monitoring, what would your thesis contribute?',
 'Sensor design needs to know which wavelengths, bandwidths and spatial resolution carry the disease signal.',
 'The ML-SFFS optimum combinations, the WRI and the discriminant bands give a minimal set of disease-relevant wavelengths; the comparison of the four sensors shows which spatial and spectral resolution carries the signal; the fusion results show whether thermal data add value.',
 'Mahlein et al. (2013) designed disease indices that can be transferred to multispectral cameras; Zhu et al. (2017) selected effective wavelengths for portable multispectral devices; Thenkabail et al. (2004) identified optimal hyperspectral bands for vegetation.');
QA3('How does early detection help a national monitoring system?',
 'Early, spatial information allows targeted sprays before an epidemic spreads, reducing yield loss and pesticide use.',
 'Objective 3 tests pre-symptomatic prediction and produces plot-wise risk maps; combined with weather-based risk, this could support advisories.',
 'Bhattacharya and Chattopadhyay (2013) combined weather anomalies (Stage I), soil–canopy water stress (Stage II) and hyperspectral discrimination (Stage III) into a multi-stage tracking scheme; Nguyen et al. (2023) estimated that early UAV detection could save 3–7% of yield.');
QA3('What is the main novelty of your work for ISRO?',
 'A novel contribution fills a gap that existing studies have not addressed.',
 'First sensor-based study of white rust in mustard; four UAV sensors on the same plots; a White Rust Index including SWIR; comparison of ML-SFFS and DNN fusion; pre-symptomatic prediction at plot scale; leakage-free validation; and bands that can be tested on ISRO sensors.',
 'The closest Indian work used ground spectroscopy for mustard aphid (Shukla et al., 2024) and Hyperion data for mustard rot (Bhattacharya and Chattopadhyay, 2013); ICAR-IARI studies used field spectroradiometers for wheat and rice diseases (Krishna et al., 2014; Mandal et al., 2023).');
