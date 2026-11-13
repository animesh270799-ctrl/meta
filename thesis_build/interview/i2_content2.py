# Part L-P of guide v2 (no results)
H1('L. Remote-sensing and analysis fundamentals')
RQ = [
 ('Explain the spectral signature of healthy and diseased mustard leaves.', 'Healthy leaves absorb strongly in blue and red (chlorophyll), reflect a green peak, show a steep red edge, a high NIR plateau from mesophyll scattering and SWIR reflectance controlled by water absorption. Diseased leaves show higher visible reflectance, a lower and earlier red edge, lower NIR and higher SWIR reflectance (Carter and Knapp, 2001; Curran, 1989).'),
 ('What causes the red-edge shift in diseased plants?', 'Less chlorophyll narrows the red absorption feature, so the steep rise from red to NIR occurs at shorter wavelengths and is less steep; tissue damage lowers the NIR shoulder (Horler et al., 1983; Filella and Peñuelas, 1994).'),
 ('Why do diseased leaves reflect more in the SWIR?', 'SWIR reflectance is governed by water absorption; loss of leaf water reduces absorption and raises reflectance (Apan et al., 2004).'),
 ('What are spatial, spectral, radiometric and temporal resolution?', 'Pixel size; number and width of bands; sensitivity and bit depth; revisit interval. Disease monitoring needs fine spectral resolution in the red edge and SWIR and frequent revisits during the epidemic window.'),
 ('Why does NDVI fail for disease detection?', 'NDVI saturates at high canopy cover and responds to any loss of green biomass, so it is neither sensitive early nor specific; red-edge and disease indices are better (Mahlein et al., 2013; Zheng et al., 2018).'),
 ('Why use derivative spectra?', 'Derivatives remove additive offsets from illumination and background and sharpen inflection points such as the red edge (Tsai and Philpot, 1998).'),
 ('How do you handle correlated hyperspectral bands and the Hughes phenomenon?', 'Neighbouring bands are nearly identical, and too many features for the number of samples reduce accuracy (Hughes, 1968). I keep one band per correlated region, remove collinearity with VIF < 10 and select compact subsets with ML-SFFS (Dormann et al., 2013; Pudil et al., 1994).'),
 ('What is atmospheric correction and why does it matter?', 'It converts top-of-atmosphere radiance to surface reflectance by removing scattering and absorption; disease anomalies are small, so uncorrected haze or water vapour can mask them (Vermote et al., 1997).'),
 ('What is emissivity, and why is it important for thermal data?', 'The efficiency of thermal emission relative to a blackbody; vegetation is about 0.97–0.99, and errors of 0.01 shift retrieved temperature by roughly half a degree, comparable to disease effects.'),
 ('What is a spectral response function?', 'The sensitivity of a sensor band across wavelengths; satellite bands are simulated from hyperspectral spectra by weighting with it, which is essential for transferring indices.'),
 ('What is ReliefF?', 'A filter feature-selection method that weights features by how well they separate nearest neighbours of different classes; it handles multi-class, noisy, overlapping data (Robnik-Šikonja and Kononenko, 2003).'),
 ('What does canonical discriminant analysis tell you?', 'It finds linear combinations of features that maximise between-class relative to within-class variance; canonical correlations and Wilks\' lambda quantify separability (Fisher, 1936).'),
 ('Why Boruta after ANOVA and discriminant analysis?', 'ANOVA is univariate and discriminant analysis keeps a minimal linear set; Boruta selects all relevant features with non-linear random-forest importance against shadow features (Kursa and Rudnicki, 2010).'),
 ('Why macro-F1 and kappa rather than overall accuracy?', 'Grades have unequal sizes; macro-F1 weights each class equally and kappa corrects for chance agreement (Cohen, 1960; Sokolova and Lapalme, 2009).'),
 ('What is RPD?', 'The ratio of the standard deviation of observations to RMSE; values near or above two indicate useful quantitative models (Chang et al., 2001).'),
 ('How do you handle flowers in mustard images?', 'Yellow petals dominate 500–650 nm and change with phenology; flower pixels are removed and the flower fraction is used as a covariate (Sulik and Long, 2016).'),
 ('How do you make thermal data comparable between flights?', 'Radiometric calibration with emissivity, air temperature, humidity and distance, and weather-normalised indices: CTD, NRCT and CWSI (Jackson et al., 1981; Feng et al., 2022).'),
 ('What is the difference between TVDI and CWSI?', 'TVDI scales surface temperature between dry and wet edges of a scene\'s temperature–vegetation-index space and reflects surface moisture (Sandholt et al., 2002); CWSI scales canopy temperature between weather-based or reference limits and reflects crop transpiration deficit (Idso et al., 1981; Jones, 1999).'),
 ('What is thermal inertia?', 'Resistance of a material to temperature change, √(kρc); wet soil has high thermal inertia and a small day–night temperature range; apparent thermal inertia from day and night images estimates soil moisture (Price, 1977).'),
 ('Can SAR detect white rust?', 'SAR responds to canopy structure and moisture, not to pigments; it maps mustard and severe structural damage but not early pustules, so it supports masking rather than detection.'),
]
for q, a in RQ: Qd(q, a)

H1('M. Tough and critical questions')
TQ = [
 ('Exact classification of six severity grades is difficult. Is the approach useful?', 'Yes. Grades are ordinal cuts of a continuous variable and neighbouring grades overlap, as reported for other diseases (Mandal et al., 2023; Meng et al., 2020). The thesis therefore models PDI as a continuous target and reports adjacent-grade accuracy and healthy-versus-diseased performance, which are the decisions that matter for management.'),
 ('Your experiment covers one site and season. How can you generalise?', 'Generalisation is tested, not assumed: physically interpretable features, leave-one-replication-out validation, and independent validation at another site and in farmers\' fields (Bohnenkamp et al., 2019).'),
 ('Why should ISRO be interested in a drone study?', 'Satellite algorithms need calibration and validation data in which the disease signal is known; UAV studies define the wavelengths, resolution and timing that work, as SAC combined ground and satellite data for mustard rot (Bhattacharya and Chattopadhyay, 2013).'),
 ('What if the White Rust Index does not transfer to satellites?', 'Then the transferable components (red-edge slope, SWIR water features, thermal) are used directly in a classifier, and the index is re-derived on simulated satellite bands; a negative result also informs sensor design.'),
 ('Is it realistic to detect millimetre pustules from space?', 'Not individual pustules, but canopy-level consequences (chlorophyll loss, water loss, warming) over many leaves are detectable as severity, as demonstrated for wheat yellow rust with Sentinel-2 (Zheng et al., 2018) and airborne hyperspectral data (Nigam et al., 2019).'),
 ('Could thermal differences simply reflect irrigation differences?', 'Irrigation is uniform, controls are present on every date, and a water-status check (relative water content or water index) tests whether warm plots are also drier.'),
 ('How do you know the signal is caused by white rust and not by variety or inoculation?', 'Healthy controls of the same varieties are measured on the same dates; variety is analysed as a factor; and other diseases and stresses are recorded during ground truth.'),
 ('Why not use a deep CNN on the images?', 'A CNN needs thousands of labelled images; a field experiment provides a limited number of plot-dates. Compact models on interpretable features are more reliable here, and small deep networks are tested against them.'),
 ('What are the limitations of your study?', 'Single season and site initially; canopy effects reduce the leaf-level signal; ordinal grades overlap; thermal data depend on weather; satellite transfer must still be demonstrated.'),
 ('How is your work different from routine ICAR disease surveys?', 'Surveys give accurate but sparse observations; the thesis converts them into objective, spatially continuous estimates and tests early detection, while surveys remain the ground truth.'),
]
for q, a in TQ: Qd(q, a)

H1('N. Formula sheet')
TAB('formulas', [['Quantity', 'Formula', 'Reference'],
                 ['PDI (%)', 'Σ (score × n) / (N × 9) × 100', 'Wheeler (1969)'],
                 ['NDVI; NDRE', '(R_{NIR} − R_{red})/(R_{NIR} + R_{red}); (R_{NIR} − R_{RE})/(R_{NIR} + R_{RE})', 'Rouse et al. (1974); Gitelson and Merzlyak (1994)'],
                 ['NDYI (flowering)', '(R_{green} − R_{blue}) / (R_{green} + R_{blue})', 'Sulik and Long (2016)'],
                 ['PSRI', '(R_{680} − R_{500}) / R_{750}', 'Merzlyak et al. (1999)'],
                 ['DWSI-1; DWSI-5', 'R_{800}/R_{1660}; (R_{800} + R_{550})/(R_{1660} + R_{680})', 'Apan et al. (2004)'],
                 ['ROTI', 'R_{1175} / (R_{1982} + R_{691})', 'Bhattacharya and Chattopadhyay (2013)'],
                 ['Disease index form', 'ND(λ_{1}, λ_{2}) + w R(λ_{3})', 'Mahlein et al. (2013)'],
                 ['CTD; CWSI', 'T_{c} − T_{a}; (T_{c} − T_{wet})/(T_{dry} − T_{wet})', 'Jackson et al. (1981); Jones (1999)'],
                 ['TVDI', '(T_{s} − T_{s,min}) / (T_{s,max} − T_{s,min})', 'Sandholt et al. (2002)'],
                 ['Band simulation', 'R_{band} = ∫ R(λ) S(λ) dλ / ∫ S(λ) dλ', 'Thenkabail et al. (2004)'],
                 ['VIF', '1 / (1 − R_{j}^{2})', 'Dormann et al. (2013)'],
                 ['Error-adjusted area', 'A × Σ_{h} W_{h} (n_{h,k} / n_{h})', 'Olofsson et al. (2014)'],
                 ['Macro-F1; kappa; RPD', '(1/k) Σ F1_{i}; (p_{o} − p_{e})/(1 − p_{e}); SD/RMSE', 'Sokolova and Lapalme (2009); Cohen (1960); Chang et al. (2001)']], [2000, 4500, 2806], 'Formula sheet for quick revision.', 14)

H1('O. Policy, application and future')
PQ = [
 ('How can your work support integrated disease management and crop insurance?', 'Risk and severity maps allow need-based spraying, reduce pesticide use and cost, help plan inputs, and provide objective evidence for loss assessment.'),
 ('How might climate change affect white rust, and how can remote sensing help?', 'Changing winter temperature, humidity and fog patterns shift infection windows and hotspots; long satellite and weather records allow risk maps to be recalibrated and shifts to be tracked.'),
 ('If you join ISRO, what would you do first with this work?', 'Test the transferable white-rust features on Sentinel-2 and hyperspectral data over the main mustard belt, using UAV sentinel sites for validation, and prototype a disease layer combining weather risk, anomalies and attribution.'),
 ('How would you collaborate with NRSC, SAC and ICAR?', 'Joint sentinel sites with UAV flights at ICAR stations (for example the mustard research directorate at Bharatpur), shared spectral libraries, and testing of the algorithm on Resourcesat, Sentinel-2 and hyperspectral data.'),
]
for q, a in PQ: Qd(q, a)
H1('P. Closing statement')
Q('Summarise the contribution of your thesis in one sentence.', 'The thesis establishes the physiological and spectral basis for detecting white rust of mustard with UAV sensors, develops disease-specific features and validated severity models, and defines how these can be transferred to satellite-based monitoring for large-scale use.')
