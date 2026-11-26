from c_lib import *


def add():
    # ------------------------------------------------------------------ Part B
    h1('3. Part B – Unmanned aerial vehicle image processing')
    p('Part B turns the raw images of each date into calibrated, co-registered images on one grid and gives one average value per subplot for every band of every camera (field-level average spectra).')
    myfig('proc', 'g06_processing.png', 'Processing chain of Part B (Steps B1–B6).')
    P = 'B UAV processing'
    step('B1', 'Radiometric calibration', part=P,
         what='Digital numbers are converted to reflectance (HS, MS) or temperature (thermal).',
         why='Only calibrated values can be compared between dates, plots and cameras.',
         do=['HS and MS: empirical line method with the reflectance panels imaged before and after the flight; correct changes in sunlight with the downwelling light sensor.',
             'RGB: fixed exposure and white balance on all dates; colour indices (ratios) are used, so overall brightness cancels.',
             'Thermal: radiance to temperature with emissivity 0.98 and the air temperature, humidity and height of each flight.'],
         check=['Panel reflectance in the image within ± 0.02 of the certified value.', 'Canopy temperatures within a physically possible range (air temperature ± 15 °C).'],
         out='Calibrated images → B2.',
         papers=[('Ma et al. (2026)', 'Rice blast; two-point (empirical line) reflectance calibration of the UAV hyperspectral images with calibration targets.', 'Same empirical line calibration with panels.'),
                 ('Guo et al. (2021)', 'Wheat yellow rust; radiometric calibration of the UAV hyperspectral camera before every flight.', 'Calibration on every flight date.'),
                 ('Yuan et al. (2025)', 'Rice bacterial blight; a calibrated white panel placed on the ground before and after the flight for radiometric calibration.', 'Panels before and after the flight.'),
                 ('Blasch et al. (2023)', 'Wheat yellow and stem rust; multispectral images calibrated with the manufacturer\'s reflectance panel and the sunshine sensor of each flight.', 'Panel plus downwelling light sensor for the multispectral camera.'),
                 ('Liu et al. (2024)', 'Wheat powdery mildew; UAV multispectral images converted to reflectance with an empirical method and three target cloths.', 'Empirical line calibration with reference targets.')])
    step('B2', 'Orthomosaics and georeferencing', part=P,
         what='Frame images (MS, RGB, thermal) are mosaicked; push-broom HS lines are georectified; all dates share one coordinate frame through the same GCPs.',
         why='Subplot ROIs (B6) must fall on the same ground on every date and in every camera.',
         do=['Build orthomosaics of the frame cameras by structure-from-motion.', 'Georectify the HS lines with the GNSS/IMU data of the UAV and correct lens distortion.', 'Use the same GCPs on every date.'],
         check=['GCP residuals below 2 pixels of the camera.'],
         out='Georeferenced mosaics → B3, B4.',
         papers=[('Ma et al. (2026)', 'Rice blast; lens distortion correction, reflectance calibration and mosaicking of the hyperspectral images before extracting samples.', 'Same correction and mosaicking chain.'),
                 ('Guo et al. (2021)', 'Wheat yellow rust; georeferenced UAV hyperspectral mosaics of the field.', 'Georeferenced hyperspectral mosaics.'),
                 ('Liu et al. (2024)', 'Wheat powdery mildew; multispectral and thermal images aligned and mosaicked in Photoscan (structure-from-motion) with ground control points (errors within 1 cm).', 'Structure-from-motion mosaics with the same ground control points.')])
    step('B3', 'Hyperspectral quality control and smoothing', part=P,
         what='Noisy and water-vapour bands are removed and every spectrum is smoothed with a Savitzky–Golay filter.',
         why='Water-vapour regions and the detector ends are noisy under sunlight; smoothing is needed before the first derivative (Step C1).',
         do=['Remove 1335–1460 nm and 1785–1965 nm (water vapour) and the noisy ends; keep 483 bands from 399 to 2398 nm.',
             'Smooth each continuous segment with a Savitzky–Golay filter (window 5 bands, second order), never across a removed region.',
             'Check that reflectance lies between 0 and 1.'],
         check=['483 bands remain; no negative reflectance after smoothing.'],
         out='Clean HS cube → B4.',
         papers=[('Ma et al. (2026)', 'Rice blast; Savitzky–Golay smoothing of the canopy spectra to reduce sensor noise; the noisy 400–450 nm region was not used for analysis.', 'Same filter; noisy regions removed.'),
                 ('Mandal et al. (2023)', 'Rice blast; 1351–1439, 1801–1949 and 2351–2500 nm removed because of noise from ambient water absorption; Savitzky–Golay filter to reduce random noise.', 'Same reason for removing 1335–1460 and 1785–1965 nm in sunlit UAV data; same filter.'),
                 ('Chen et al. (2023)', 'Tobacco viruses; Savitzky–Golay smoothing with a second-order polynomial and a 5-point window; smoothing with SVM gave the best severity models.', 'Same window (5) and order (2).'),
                 ('Feng et al. (2022)', 'Wheat powdery mildew; noisy spectral regions removed and the spectra smoothed with the Savitzky–Golay function before the indices were computed.', 'Noisy regions removed, then smoothing.')])
    step('B4', 'Projection and co-registration', part=P,
         what='All images are projected to WGS 84 / UTM 43N and the RGB, MS and thermal images are registered to the HS image.',
         why='Features of different cameras must come from the same ground area for feature-level fusion.',
         do=['Project every image to WGS 84 / UTM zone 43N.', 'Register RGB, MS and thermal images to the HS image with tie points (plot corners, markers) and a first- or second-order polynomial.', 'Accept when the root-mean-square error of check points is below one HS pixel (2.2 cm).'],
         check=['RMSE of check points < 2.2 cm for each camera and date.'],
         out='Co-registered images → B5.',
         papers=[
                 ('Calderón et al. (2014)', 'Downy mildew of opium poppy; thermal and multispectral images of the same plots analysed together.', 'Thermal and multispectral layers on the same plots.'),
                 ('Liu et al. (2024)', 'Wheat powdery mildew; multispectral and thermal images geographically corrected with the same ground control points.', 'All cameras on one coordinate frame through common ground control points.')])
    step('B5', 'Resampling to the hyperspectral grid', part=P,
         what='RGB, MS and thermal layers are resampled to the 2.2-cm HS grid.',
         why='One pixel grid lets one set of subplot ROIs (B6) serve all cameras.',
         do=['Compute RGB texture first, at native resolution (Step C4).', 'RGB (finer): pixel aggregate (mean of covered pixels). MS (similar size): bilinear. Thermal (coarser): nearest neighbour, so measured temperatures are kept.'],
         check=['All layers have the HS grid size and origin.'],
         out='Image stack on one grid → B6.',
         papers=[('Guo et al. (2021)', 'Wheat yellow rust; UAV hyperspectral images resampled to coarser resolutions to study the effect of pixel size on detection.', 'Resampling between UAV pixel sizes.'),
                 ('Yuan et al. (2025)', 'Rice bacterial blight; UAV and satellite images brought to common grids for multi-scale monitoring.', 'Common grid for data of different resolution.')])
    step('B6', 'Subplot regions of interest and their average spectra', part=P,
         what='One region of interest (ROI) is drawn inside each subplot, and the mean of all its pixels is taken for every band of every camera on every date: the field-level average spectrum (and temperature) of the subplot.',
         why='The subplot is the unit that carries the DI (Step A3); one average per band and subplot gives one sample per subplot-date, and averaging many pixels reduces noise.',
         do=['Digitise the 48 plot polygons once on a mosaic and split each into its four subplots; draw the ROI of each subplot inside an inner buffer that excludes border rows and bunds.',
             'Use the same ROIs on all dates and for all cameras (images are co-registered, Step B4).',
             'Export the ROI mean of every band (ENVI ROI statistics, "Mean") for HS, MS and RGB, and the ROI mean temperature for thermal; keep the ROI pixel values for texture (Steps C3–C5).',
             'Join DI, labels and covariates by subplot code and date.'],
         check=['192 subplot rows per date and camera.', 'ROI outlines checked on the RGB mosaic of every date (no bund or path inside).'],
         out='Subplot average spectra and temperatures → Part C.',
         alt='Soil pixels inside the ROI could be excluded with an NDVI threshold, as Guo et al. (2021) did; here the full ROI average is used, as in the ROI-mean samples of Ma et al. (2026).',
         q='Why the average of the whole ROI? → It is the field-level signal that the camera records for the subplot whose DI was surveyed; ROI-mean spectra were the samples of the DT-EDNet study (Ma et al., 2026).',
         papers=[('Ma et al. (2026)', 'Rice blast; regions of interest delineated in ENVI 5.6; the average reflectance of the rice pixels in each ROI was the sample spectrum.', 'ENVI ROI mean as the sample spectrum.'),
                 ('Guo et al. (2021)', 'Wheat yellow rust; mean canopy spectra of plots related to the disease index.', 'Plot (subplot) means as samples.'),
                 ('Liu et al. (2024)', 'Wheat powdery mildew; the mean of all pixels in each plot region of interest (and percentile values) used as plot features; the share of soil pixels in the ROI was small after canopy closure.', 'Mean of all ROI pixels as the field-level sample.'),
                 ('Mustafa et al. (2023)', 'Wheat Fusarium head blight; values of the fluorescence and multispectral phenotyping images extracted from a region of interest of each spike for analysis.', 'Region-of-interest values as the sample.')])
    demo('roimean', [['Date', 'Subplot', 'ROI pixels', 'R_{550}', 'R_{670}', 'R_{800}', 'Mean Tc (°C)', 'DI (%)'], ['18 Jan 2027', '25-1', '6 120', '0.081', '0.046', '0.392', '23.4', '12.3'], ['18 Jan 2027', '25-2', '6 090', '0.084', '0.052', '0.371', '24.1', '28.4'], ['18 Jan 2027', '7-1 (healthy)', '6 150', '0.079', '0.041', '0.418', '22.8', '0.0']],
         'Subplot ROI averages joined to the DI', widths=[1300, 1400, 1100, 1000, 1000, 1000, 1400, 1400])

    # ------------------------------------------------------------------ Part C
    h1('4. Part C – Features of the four cameras')
    P = 'C Features'
    step('C1', 'Hyperspectral bands, first derivative and red-edge parameters', part=P,
         what='Reflectance of the 483 bands, their first derivative and three red-edge parameters.',
         why='The derivative removes brightness offsets and sharpens the red edge; chlorophyll loss moves the red edge to shorter wavelengths.',
         do=['Reflectance R_{λ} of the 483 bands.', 'First derivative FD(λ_{i}) = [R(λ_{i+1}) − R(λ_{i−1})] / (λ_{i+1} − λ_{i−1}) on each smoothed segment; derivatives within 10 nm of a removed region are not used.',
             'Red-edge position (wavelength of the largest FD in 680–760 nm), red-edge amplitude D_{r} (that largest FD) and red-edge area SD_{r} (sum of FD over 680–760 nm).'],
         check=['REP between about 690 and 740 nm for all subplots.'],
         out='HS spectral group → 1.2.',
         papers=[('Yu et al. (2021)', 'Pine wilt disease; red-edge parameters were the best features for the early stage from UAV hyperspectral data.', 'Red-edge parameters as features.'),
                 ('Zhang et al. (2012)', 'Wheat powdery mildew; derivative features (amplitude, position and area of the red edge) among the spectral features.', 'Same three red-edge parameters.'),
                 ('Lv et al. (2023)', 'Southern corn leaf blight; first-order spectral derivatives at every band were one of four spectral enhancement features; combining them with bands and indices improved accuracy by about 1–2%.', 'First derivative at every band.'),
                 ('Ma et al. (2026)', 'Rice blast; reflectance bands as the first feature group.', 'Reflectance bands as a feature group.'),
                 ('Mandal et al. (2022)', 'Rice blast; the amplitude of the red-edge first-derivative peak fell as severity increased.', 'Red-edge amplitude as a feature.')])
    step('C2', 'Published vegetation and disease indices', part=P,
         what='48 published hyperspectral indices (39 base + 9 SWIR disease indices) are computed for every subplot (definitions in Chapter 11).',
         why='Indices summarise pigments, structure, water and disease effects and can be compared with other studies and sensors.',
         do=['Compute the 48 indices with the nearest available band; check each formula against its original paper.', 'Skip an index if a band it needs was removed in Step B3.'],
         check=['No missing index values.'],
         out='HS index group → 1.3, 1.4.',
         papers=[('Ma et al. (2026)', 'Rice blast; common vegetation indices (PSSRb, SR, GNDVI, RVI, RVSI, WBI and others) computed from UAV spectra.', 'All indices of Ma et al. are in the list.'),
                 ('Mandal et al. (2023)', 'Rice blast; 26 published indices evaluated and two new blast indices (RBI, NDBI).', 'RBI and NDBI included.'),
                 ('Mahlein et al. (2013)', 'Sugar-beet diseases; the Healthy Index and disease-specific indices.', 'HI included.'),
                 ('Apan et al. (2004)', 'Sugarcane orange rust; disease–water stress indices (DWSI) from Hyperion.', 'DWSI-1 to DWSI-5 included.'),
                 ('Das et al. (2015)', 'Rice bacterial leaf blight; PSRI and PSSRb from ground hyperspectral data.', 'PSRI and PSSR included.'),
                 ('Kundu et al. (2021)', 'Potato late blight; field hyperspectral observations; the disease–water stress index correlated with severity (r ≈ −0.84).', 'DWSI indices included for a foliar disease.')])
    step('C3', 'Hyperspectral texture', part=P,
         what='Grey-level co-occurrence matrix (GLCM) texture of the first three principal-component images of the HS cube.',
         why='Pustules and chlorotic patches make the canopy uneven; spectra do not record this spatial pattern.',
         do=['PCA of the HS pixels inside the subplot ROIs (all dates); keep the first three components (cumulative variance > 95%).', 'GLCM in a 3 × 3 window, distance 1, four directions (0°, 45°, 90°, 135°), 64 grey levels.',
             'Eight measures: mean, variance, homogeneity, contrast, dissimilarity, entropy, second moment, correlation; average over the ROI pixels of the subplot (3 × 8 = 24 features).'],
         check=['24 texture features per subplot-date.'],
         out='HS texture group → 1.5.',
         papers=[('Ma et al. (2026)', 'Rice blast; GLCM texture (3 × 3 window, distance 1, four directions, 64 grey levels, 8 measures) of principal-component images (PC2-Mea, PC3-Mea …).', 'Same window, directions, grey levels and measures.'),
                 ('Guo et al. (2021)', 'Wheat yellow rust; texture of principal-component images combined with vegetation indices.', 'Texture of PCA images.'),
                 ('Liu et al. (2020)', 'Wheat Fusarium head blight; bands, indices and texture as feature groups from UAV hyperspectral images.', 'Texture as a separate feature group.')])
    demo('glcm', [['Image row', 'Grey levels of a 4 × 4 image', 'GLCM counts (levels 0–3)', 'Measure', 'Value'], ['1', '0 0 1 1', '4 2 1 0', 'contrast', '0.583'], ['2', '0 0 1 1', '2 4 0 0', 'homogeneity', '0.808'],
                  ['3', '0 2 2 2', '1 0 6 1', 'dissimilarity', '0.417'], ['4', '2 2 3 3', '0 0 1 2', 'entropy', '2.095']], 'Worked example of GLCM texture (horizontal neighbours, both directions; counts divided by 24)', widths=[1300, 2700, 2500, 1700, 1400])
    step('C4', 'Multispectral and red–green–blue camera features', part=P,
         what='Band reflectance, indices and texture of the multispectral camera; colour indices, hue–saturation–value and texture of the RGB camera.',
         why='The cheaper cameras need their own features so that their value can be compared with the HS camera.',
         do=['MS: 5 band means, 12 indices (NDVI, GNDVI, NDRE, CI_{green}, CI_{rededge}, MTCI, OSAVI, SAVI, TCARI, MCARI, MSR, PSRI), 10 two-band normalised differences, GLCM of the 5 bands (40).',
             'RGB: ExG, ExR, ExG − ExR, VARI, GLI, NGRDI, mean hue, saturation and value; GLCM of R, G and B (24), computed at native resolution.',
             'GLCM for MS and RGB: 64 grey levels, distance 1 pixel, mean of the four directions 0°, 45°, 90° and 135°; eight measures (mean, variance, homogeneity, contrast, dissimilarity, entropy, second moment, correlation) over the subplot ROI.'],
         check=['MS 67 and RGB 33 features per subplot-date.'],
         out='MS and RGB groups → 1.6.2, 1.6.3.',
         papers=[('Liu et al. (2024)', 'Wheat powdery mildew; band reflectance, nine vegetation indices (NDRE, PSRI, NDVI, SAVI, MCARI, MTCI, GNDVI, OSAVI, MSR) and eight GLCM textures of each of the five multispectral bands, combined into three-band texture combination indices.', 'Same MS indices and GLCM measures.'),
                 ('Maimaitijiang et al. (2020)', 'Soybean yield (method support); UAV RGB, multispectral and thermal images gave spectral, structure, thermal and GLCM texture (8 measures) features, kept by modality.', 'Features of each camera kept as their own groups.'),
                 ('Blasch et al. (2023)', 'Wheat yellow and stem rust; multispectral and very-high-resolution indices from UAV and satellite.', 'MS indices for rust detection.'),
                 ('Feng et al. (2022)', 'Wheat powdery mildew; texture features of RGB and thermal infrared images fused with hyperspectral vegetation indices.', 'RGB texture features.'),
                 ('Nguyen et al. (2023)', 'Spring wheat yellow rust; CRI2, SAVI2 and GLCM contrast from multispectral UAV images were the features most correlated with the disease.', 'Multispectral indices plus texture.')])
    step('C5', 'Thermal features', part=P,
         what='Canopy temperature statistics, normalised temperatures (Step D3) and thermal texture.',
         why='Infection changes transpiration and leaf temperature.',
         do=['Mean, median, SD, 10th and 90th percentiles and maximum temperature difference (MTD = highest − lowest temperature) of the ROI pixels.', 'Normalised temperatures from Step D3.', 'GLCM texture of the temperature image (8; temperatures quantised to 64 levels over one common range for all dates; distance 1, four directions).'],
         check=['18 thermal features per subplot-date (6 statistics, 4 normalised temperatures, 8 texture).'],
         out='Thermal group → D3, 1.6.4.',
         papers=[('Calderón et al. (2014)', 'Downy mildew of opium poppy; canopy temperature and canopy minus air temperature from UAV thermal images detected infected plants.', 'Canopy temperature and its normalised form.'),
                 ('Feng et al. (2022)', 'Wheat powdery mildew; thermal infrared temperature parameters as a separate data source in fusion with spectral indices and texture.', 'Thermal features as a fusion group.'),
                 ('Liu et al. (2024)', 'Wheat powdery mildew; canopy temperature from UAV thermal images analysed with spectral and texture features to estimate the disease index.', 'Canopy temperature added to optical features.'),
                 ('Oerke et al. (2006)', 'Cucumber downy mildew; the maximum temperature difference within a leaf increased during pathogenesis and was related to severity, but air temperature and humidity also changed leaf temperature.', 'MTD as a thermal feature; temperatures normalised for weather (Step D3).')])
    step('C6', 'Feature table of each camera', part=P,
         what='One table per camera, one row per subplot-date, with identifiers, labels, covariates and features with a group prefix.',
         why='Sensor sets are then simple joins of camera tables by subplot and date.',
         do=['Columns: identifiers (date, DAI, plot, subplot, replication, treatment, variety, timing, split), labels (DI, DI class, detection), covariates, features (prefixes R_, FD_, RE_, VI_, TX_, TH_).'],
         check=['Same rows (subplot-dates) in the four camera tables.'],
         out='Four camera tables → Part D.',
         papers=[('Feng et al. (2022)', 'Wheat powdery mildew; vegetation indices, temperature parameters and texture features of each sample combined for modelling.', 'One feature table per camera for fusion.'),
                 ('Liu et al. (2024)', 'Wheat powdery mildew; multi-feature table (spectral, texture, thermal) per plot.', 'Same organisation of feature groups.')])
    rows = [['Camera', 'Feature groups', 'Number'], ['Hyperspectral', 'reflectance 483, first derivative 483, red-edge parameters 3, published indices 48, PCA texture 24 (+ NDSI, RSI, WRI and TTFI of Objective 1)', '≈ 1040'],
            ['Multispectral', '5 bands, 12 indices, 10 normalised differences, 40 texture', '67'], ['RGB', '6 colour indices, 3 colour means, 24 texture', '33'], ['Thermal', '6 temperature statistics (incl. MTD), 4 normalised temperatures (CTD, CTR, NRCT, difference from healthy), 8 texture', '18'],
            ['Covariates', 'DAI, variety, timing, growth stage, weather', 'not features']]
    tab('featgroups', rows=rows, caption='Feature groups before selection.', widths=[1700, 6400, 1500], size=16)

    # ------------------------------------------------------------------ Part D
    h1('5. Part D – Data split and data preparation')
    P = 'D Split'
    step('D1', 'The 7:3 split by whole plots', part=P,
         what='The 48 plots are divided once into 33 training plots and 15 test plots. All samples of a plot – its 4 subplots on all dates and its 12 ASD leaves per date – go to the same side. Healthy and inoculated plots are split separately.',
         why='The test plots must be fixed before any step learns from the data; whole plots are kept together because subplots and leaves of one plot share soil, microclimate and inoculum, and a test on new plots is what the model will face.',
         do=['Test plots per block type = 30% of the plots: 4 of the 12 healthy plots and 11 of the 36 inoculated plots.',
             'Test plots: 1, 4, 5, 8 (healthy; four different sowing dates, all varieties) and 13, 14, 18, 25, 27, 31, 35, 37, 44, 46, 48 (inoculated; 11 different treatments spread over R1–R3, varieties and sowing dates) – the same plots as in the 2025-26 analysis (same plot plan).',
             'All other 33 plots are training plots.',
             'Write the split column (TEST / TRAIN) into every table before any analysis.'],
         settings=['UAV post-symptomatic: TRAIN 1320, TEST 600 subplot-dates; pre-symptomatic: TRAIN 396, TEST 180; ASD leaves: TRAIN 5148, TEST 2340.'],
         check=['No plot on both sides.', 'TEST contains all four sowing dates, all three varieties and all three replications.'],
         out='Split column → every later step.',
         alt='A random split of samples (Ma et al., 2026) is simpler but would put subplots and leaves of one plot on both sides.',
         q='Were the test plots chosen after seeing results? → No; they are fixed by the design before the first flight, using only plot, block, variety and sowing date.',
         papers=[('Ma et al. (2026)', 'Rice blast; samples divided by stratified sampling into training and test sets at 7:3, with 10% of the training set as validation; features selected and models trained on the 2023 data and tested on an independent 2024 data set.', 'Same 7:3 proportion and stratification; whole plots are assigned instead of single samples, as the cross-year test of Ma et al. kept test data independent.'),
                 ('Mandal et al. (2023)', 'Rice blast; data divided by stratified sampling into two-thirds calibration and one-third validation; all modelling on the calibration part.', 'A stratified hold-out of about one third, with all modelling on the training part.'),
                 ('Cross et al. (2024)', 'Wheat stripe rust progression from hyperspectral reflectance; models checked with 80:20 hold-out splits repeated 100 times.', 'A hold-out test set kept apart from training, as in recent disease spectroscopy.'),
                 ('Bijlwan et al. (2025)', 'Wheat yellow rust and powdery mildew; data split into 70% training and 30% testing sets.', 'Same 70:30 proportion.')])
    myfig('split', 'g05_split.png', 'Division of the three datasets: 33 training plots (22 fit + 11 validation plots for the networks) and 15 test plots.')
    step('D2', 'Validation inside the training plots', part=P,
         what='Settings, feature subsets and stopping epochs are chosen inside the 33 training plots: GroupKFold(3) by plot for machine learning (three rounds of 22 fitting and 11 scoring plots) and a fixed set of 11 validation plots (one third) for the networks.',
         why='A model must be tuned on data it is not tested on; tuning on the test plots would make the test accuracy optimistic.',
         do=['Machine learning: GroupKFold(3) over the 33 training plots (plots, not samples, are divided).',
             'Networks: validation plots 6, 7, 11, 19, 24, 26, 28, 30, 36, 39, 41 (random, seed 42); the other 22 training plots fit the weights.',
             'Use the same folds and validation plots for every camera, sensor set and model.'],
         settings=['Networks, UAV post-symptomatic: fit 880, validation 440 subplot-dates; ASD leaves: fit 3432, validation 1716.'],
         check=['No plot in both the fitting and the scoring part of any fold.'],
         out='Inner folds and validation plots → 2.2–2.6, 3.3–3.4, L6.',
         alt='10% of the training samples as in Ma et al. (2026) would be about three plots – too few to represent the blocks, and samples of one plot would be in fitting and validation.',
         papers=[('Ma et al. (2026)', 'Rice blast; 10% of the training set as validation; the model with the highest validation accuracy was kept and then tested once.', 'Validation inside the training part, test used once – but by whole plots.'),
                 ('Tian et al. (2021)', 'Rice leaf blast; SFFS wrapped around LDA, k-NN and SVM with 4-fold cross-validation repeated 100 times.', 'k-fold cross-validation inside the training data for the ML models.'),
                 ('Lv et al. (2023)', 'Southern corn leaf blight; RELIEF-F, SFFS and an SVM evaluated with 4-fold cross-validation repeated 100 times.', 'Cross-validated SFFS and tuning; here GroupKFold(3) by plot.'),
                 ('Bijlwan et al. (2025)', 'Wheat yellow rust and powdery mildew; 3-fold cross-validation inside the 70% training set for hyper-parameter tuning.', 'Three inner folds for tuning, here grouped by plot.')])
    demo('folds', [['Inner fold', 'Fitting plots', 'Scoring plots', 'Used for'], ['1', '22 training plots', '11 training plots', 'SFFS score, grid search'], ['2', '22 (different)', '11 (different)', 'SFFS score, grid search'], ['3', '22 (different)', '11 (different)', 'SFFS score, grid search'],
                   ['Networks', '22 training plots', '11 validation plots', 'early stopping, epoch choice']], 'Inner validation of the training plots', widths=[1500, 2500, 2500, 3100])
    step('D3', 'Thermal normalisation', part=P,
         what='Canopy temperature is expressed relative to air temperature and to the healthy plots of the same date.',
         why='Leaf temperature changes with air temperature, humidity and time of day, so raw temperatures of different dates cannot be compared.',
         do=['Canopy temperature difference CTD = Tc − Ta and canopy temperature ratio CTR = Tc / Ta (Ta = air temperature of the flight).', 'Normalised relative canopy temperature NRCT = (Tc − Tmin) / (Tmax − Tmin), with Tmin and Tmax the lowest and highest canopy temperatures in the image of that date (a min–max scaling within each date; no labels used).',
             'Difference from the mean temperature of the healthy training plots of the same date and variety.'],
         check=['Four normalised thermal features per subplot-date.'],
         out='Normalised thermal features → C5, 1.6.4.',
         papers=[('Calderón et al. (2014)', 'Downy mildew of opium poppy; UAV canopy temperature normalised by air temperature (Tc − Ta) separated infected plants; comparisons made at similar NDVI (growth) levels.', 'CTD used as a normalised thermal feature.'),
                 ('Oerke et al. (2006)', 'Cucumber downy mildew; air temperature and humidity at the time of measurement changed leaf temperature, so temperature alone was not suitable to quantify severity in the field.', 'Temperatures normalised by air temperature and by healthy plots of the same date.'),
                 ('Feng et al. (2022)', 'Wheat powdery mildew; canopy temperature difference CTD = CT − AT, canopy temperature ratio CTR = CT/AT and normalised relative canopy temperature NRCT = (CT − CTmin)/(CTmax − CTmin) computed to remove the effect of air temperature on canopy temperature.', 'Same three formulas (CTD, CTR, NRCT) for the same reason.'),
                 ('Maimaitijiang et al. (2020)', 'Soybean yield (method support); NRCT from the UAV thermal camera with the lowest and highest temperature of the whole field trial on the flight date.', 'NRCT scaled within the image of each date.')])
    demo('thermal', [['Subplot', 'Tc (°C)', 'Ta (°C)', 'CTD = Tc − Ta', 'Healthy mean Tc (same date, variety)', 'Difference'], ['25-2', '24.1', '22.0', '+2.1', '22.9', '+1.2'], ['7-1 (healthy)', '22.8', '22.0', '+0.8', '22.9', '−0.1']],
         'Thermal normalisation of two subplots', widths=[1500, 1100, 1100, 1700, 2600, 1600])
    step('D4', 'Standardisation and class balance', part=P,
         what='Features are standardised (z-score: z = (x − mean)/SD) with the mean and SD of the fitting part, inside every fold, for the scale-sensitive models (SVM/SVR, k-NN, PLS, networks); tree models (random forest) do not need scaling and receive the same inputs. Classifiers use balanced class weights; the networks use the cross-entropy loss with label smoothing 0.01.',
         why='SVM, k-NN, PLS and networks need features on comparable scales; balanced weights stop the models from ignoring rare classes.',
         do=['Fit the scaler inside every inner fold and then on all 33 training plots (scikit-learn Pipeline(StandardScaler, model)).', 'class_weight = balanced for SVM and random forest (k-NN and PLS-DA have no class weights).', 'Networks: label smoothing 0.01 in the cross-entropy loss.'],
         check=['No scaler fitted on test samples.'],
         out='Prepared inputs → 2.3–2.6, 3.4, L6.',
         papers=[
                 ('Ma et al. (2026)', 'Rice blast; cross-entropy loss with label smoothing 0.01 for DT-EDNet and the comparison networks.', 'Same loss settings for the networks.'),
                 ('Bijlwan et al. (2025)', 'Wheat yellow rust and powdery mildew; inputs of the artificial neural network centred and scaled within the 70% training part (3-fold cross-validation for tuning); random forest used without feature scaling because trees are not affected by scale.', 'z-score inside the training part for scale-sensitive models; no scaling needed for random forest.'),
                 ('Zhang et al. (2014a)', 'Wheat powdery mildew; the meteorological and remote-sensing variables of the logistic regression models were standardised, and their standardised coefficients compared.', 'Covariates and sensor features standardised before a regression-type model (Step 2.9).'),
                 ('Shafiee et al. (2021)', 'Wheat yield from UAV multispectral bands and indices (method support); z-score (mean 0, variance 1) applied before SVR with sequential forward selection, tuned by grid search and 10-fold cross-validation on the 70% training set.', 'z-score before SVM/SVR inside the training data.')])
    step('D5', 'Leakage rules', part=P,
         what='(1) Samples of one plot are never on both sides of any division. (2) Everything learned (selected features, scaling constants, model weights, healthy references) comes from the training plots only. (3) The test plots are used once.',
         why='These rules make the test accuracy an honest estimate for new plots.',
         do=['Run every feature-selection step of Objective 1 (and L5) on the training plots only; descriptive steps may use all plots but never decide model inputs.', 'Compute indices of test samples with the wavelengths chosen on the training plots.', 'Freeze all models before the test plots are predicted.'],
         check=['A log file records, for every step, which plots were used.'],
         out='Rules → all later steps.',
         papers=[('Ma et al. (2026)', 'Rice blast; feature selection and model training on the 2023 data; evaluation on the independent 2024 data.', 'Features selected on the training plots only and used unchanged by the models.'),
                 ('Mandal et al. (2023)', 'Rice blast; all selection and calibration on the calibration set; validation set kept apart.', 'Test plots kept apart from all selection.')])

    h2('D6 – Normalisation at each stage (summary)')
    p('No z-score or min–max scaling is applied to the spectra or images at the beginning. Normalisation before feature selection is physical (calibration, ratios and differences); statistical scaling is used only inside the steps whose method needs it, with constants from the training plots, and the fused feature table is standardised inside each model.')
    rows = [['Stage', 'What is normalised', 'Method', 'Constants from', 'Disease papers'],
            ['B1 calibration; A4 ASD', 'digital numbers, leaf readings', 'reflectance with panels / white reference; temperature from radiance', 'panels and white reference of each flight or plot', 'Ma et al. (2026); Liu et al. (2024); Zhang et al. (2022)'],
            ['B6 subplot sample', 'pixels of the region of interest', 'mean of all ROI pixels', 'the ROI itself', 'Ma et al. (2026); Liu et al. (2024); Guo et al. (2021)'],
            ['C1–C4 features', 'brightness and offsets', 'normalised-difference and ratio indices; first derivative', 'none (formulas)', 'Ma et al. (2026); Lv et al. (2023); Mandal et al. (2023)'],
            ['D3 thermal', 'canopy temperature', 'CTD = Tc − Ta; CTR = Tc/Ta; NRCT (min–max within each date); difference from healthy training plots', 'air temperature; image of the date; healthy training plots', 'Feng et al. (2022); Calderón et al. (2014); Oerke et al. (2006)'],
            ['1.2.2 PLS and CARS', 'candidate R and FD bands', 'z-score', '33 training plots', 'Bijlwan et al. (2025) (scale-sensitive models scaled)'],
            ['1.4.2, 1.6.2–1.6.4, L5.4 ReliefF', 'index and camera features', 'min–max (0–1), built into the ReliefF difference function', '33 training plots (training leaves in L5.4)', 'Lv et al. (2023); Mahlein et al. (2013); Ma et al. (2026) (Relief)'],
            ['Filters, mRMR, TTFI, VIF, NDSI/RSI maps, JM', '–', 'none (correlation, mutual information, ratios and R² do not depend on scale)', '–', 'Ma et al. (2026); Lv et al. (2023)'],
            ['2.2 fusion', 'joined camera features', 'none at the join (original units); VIF < 10 again', '–', 'Feng et al. (2022); Liu et al. (2024)'],
            ['D4 models', 'fused feature table', 'z-score (Pipeline) for SVM/SVR, k-NN, PLS, networks; trees unaffected', 'fitting part of each fold; 33 training plots; 22 fitting plots (networks)', 'Bijlwan et al. (2025)'],
            ['2.9 covariate models', 'numeric covariates', 'z-score; categorical one-hot', 'training plots', 'Zhang et al. (2014a); Bijlwan et al. (2025)'],
            ['3.2 pre-symptomatic', 'spectra; thermal features', 'spectra × [healthy baseline / healthy mean of the date] per variety; thermal as in D3', 'healthy training plots (first flight and each date)', 'Lv et al. (2023); Oerke et al. (2006); Calderón et al. (2014)'],
            ['L5.7 leaf PCA', '5-nm reflectance', 'z-score before PCA', 'all leaves (description)', 'Bijlwan et al. (2025)'],
            ['2.11 Bharatpur', 'all features', 'same formulas; frozen IARI constants (no re-fitting)', 'IARI training plots', 'Ma et al. (2026)']]
    tab('normsum', rows=rows, caption='Normalisation at each stage of the methodology.', widths=[1700, 1700, 2600, 1800, 1800], size=15)
