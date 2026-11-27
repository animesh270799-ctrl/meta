from dsl import *
from x1_intro import stage_head, TEST, VAL


def add():
    # ---------------------------------------------------------------- chapter 3
    h1('3. Stage 1 – From raw images to one value per band and subplot')
    stage_head('data collection (Part A).', 'feature extraction (Stage 2).', 'all 48 plots, all 13 dates, all four cameras.')
    box('In short', 'Each camera image is turned into reflectance (or temperature), put on one common map grid, and averaged inside the region of interest (ROI) of every subplot. The result is one row per subplot and date with the mean value of every band.', kind='key')
    p('The six processing steps are done in this order because each needs the result of the one before ({F:proc}):')
    myfig('proc', 'g06_processing.png', 'Image processing chain of Stage 1 (Steps B1–B6).')
    h3('Step 1.1 – Radiometric calibration (B1)')
    p('Digital numbers of the HS and MS cameras are converted to reflectance with the **empirical line method**: the reflectance panels imaged before and after each flight give a straight line between digital number and known reflectance for every band, and the downwelling light sensor corrects changes in sunlight during the flight. '
      'RGB images use fixed exposure and white balance; only colour ratios are used later, so overall brightness cancels. Thermal radiance is converted to temperature with emissivity 0.98 and the air temperature, humidity and height of the flight. Calibrated reflectance on every date is what allows dates to be compared (Ma et al., 2026; Calderón et al., 2014).')
    h3('Step 1.2 – Mosaics and georeferencing (B2)')
    p('Frame images (MS, RGB, thermal) are joined into orthomosaics by structure-from-motion; the push-broom HS lines are georectified with the GNSS/IMU data of the UAV. The same ground control points are used on every date, so a subplot falls on the same map position on all 13 dates (Liu et al., 2024; Guo et al., 2021).')
    h3('Step 1.3 – Cleaning and smoothing the hyperspectral data (B3)')
    p('Bands in the water-vapour regions (1335–1460 nm and 1785–1965 nm) and the noisy ends are removed, leaving **483 bands from 399 to 2398 nm**; Mandal et al. (2023) removed the same regions for the same reason. '
      'Each continuous segment is then smoothed with a **Savitzky–Golay filter** (window 5 bands, second-order polynomial; Savitzky and Golay, 1964), never across a removed region. The filter fits a small polynomial around each band and replaces the band by the fitted value, which removes random noise but keeps the shape of absorption features; Chen et al. (2023) used the same window and order, and Ma et al. (2026) and Feng et al. (2022) smoothed before computing features. Smoothing must come before the first derivative (Stage 2), because derivatives amplify noise.')
    h3('Step 1.4 – Co-registration (B4) and Step 1.5 – One common grid (B5)')
    p('All images are projected to WGS 84 / UTM 43N, and the RGB, MS and thermal images are registered to the HS image with tie points (plot corners, markers); registration is accepted when the error of check points is below one HS pixel (2.2 cm). '
      'The layers are then resampled to the 2.2-cm HS grid: RGB by averaging the finer pixels, MS by bilinear interpolation, thermal by nearest neighbour (so that measured temperatures are kept). RGB texture is computed **before** resampling, at its native 0.8-cm resolution, because averaging would smooth the texture away.')
    h3('Step 1.6 – Subplot ROIs and their averages (B6)')
    p('Each of the 192 subplots gets one ROI inside an inner buffer that excludes border rows and bunds. The same ROIs are used on all dates and for all cameras. For every band the **mean of all ROI pixels** is exported (ENVI ROI statistics), and for thermal the mean temperature; the ROI pixel values are also kept for texture. '
      'This field-level average is the sample of all UAV analyses, as the ROI mean spectra were the samples of Ma et al. (2026) and the plot means of Liu et al. (2024). Flowers inside the ROI are kept, because inflorescence infection (staghead) belongs to the disease; results are later reported by growth stage (Stage 6).')
    box('Worked example', ['ROI of subplot 25-2 on 18 January: 6 090 pixels. Mean reflectance R_{550} = 0.084, R_{670} = 0.052, R_{800} = 0.371; mean canopy temperature 24.1 °C; DI of the same subplot and date = 28.4% (class 7).',
                           'Healthy subplot 7-1 on the same date: R_{670} = 0.041, R_{800} = 0.418, 22.8 °C, DI = 0. The diseased subplot reflects more red (less chlorophyll) and less near infrared (damaged leaves) and is warmer (less transpiration).'], kind='note')
    box('On a new data set', 'Process every date with the same steps and settings; draw new ROIs for the new field, but keep the same buffer rule and use the same ROIs for all cameras and dates.', kind='present')

    # ---------------------------------------------------------------- chapter 4
    h1('4. Stage 2 – Features of each camera')
    stage_head('Stage 1 (subplot ROI means and ROI pixels).', 'labels (Stage 3), split (Stage 4) and all objectives.', 'all 48 plots, all dates. Feature formulas use no labels, so they can be computed on all samples.')
    box('In short', 'Each camera gives several groups of features: bands, derivatives, indices and texture for the hyperspectral camera; bands, indices and texture for the multispectral camera; colour indices and texture for the RGB camera; temperature statistics, normalised temperatures and texture for the thermal camera. Each camera gets its own table.', kind='key')
    h2('4.1 Hyperspectral camera')
    nl('**Reflectance** R_{λ} of the 483 bands.',
       '**First derivative** of each band on the smoothed spectrum: FD(λ_{i}) = [R(λ_{i+1}) − R(λ_{i−1})] / (λ_{i+1} − λ_{i−1}); derivatives within 10 nm of a removed region are not used (C1).',
       '**Red-edge parameters:** red-edge position (wavelength of the largest FD in 680–760 nm), amplitude D_{r} (that largest FD) and area SD_{r} (sum of FD over 680–760 nm), the derivative features used for powdery mildew by Zhang et al. (2012).',
       '**48 published indices** (39 base indices and 9 SWIR disease indices) with the nearest band; an index is skipped if one of its bands was removed (C2). Their formulas are in Chapter 11 of the methodology document.',
       '**Texture:** principal component analysis (PCA) of the HS pixels of all ROIs; the first three component images (more than 95% of the variance) are described by grey-level co-occurrence matrix (GLCM) texture (C3).')
    p('**How GLCM texture is computed.** The image is reduced to 64 grey levels. For every pixel and its neighbour at distance 1 in the four directions 0°, 45°, 90° and 135°, the pair of grey levels (i, j) is counted; dividing the counts by their total gives P(i, j), the probability of finding levels i and j side by side (Haralick et al., 1973). Eight measures summarise P: mean, variance, homogeneity, contrast, dissimilarity, entropy, second moment and correlation. With a 3 × 3 window and 64 levels, as in Ma et al. (2026), this gives 3 components × 8 measures = **24 texture features**.')
    eq('contrast = Σ_{i} Σ_{j} (i − j)^{2} P(i, j)     homogeneity = Σ_{i} Σ_{j} P(i, j) / [1 + (i − j)^{2}]')
    box('Worked example', ['A 4 × 4 image with grey levels (rows) 0 0 1 1 / 0 0 1 1 / 0 2 2 2 / 2 2 3 3, horizontal neighbours counted in both directions, gives 24 pairs.',
                           'Contrast = 0.583, homogeneity = 0.808, dissimilarity = 0.417, entropy = 2.095. A canopy with white pustules and chlorotic patches has more unequal neighbours, so contrast rises and homogeneity falls.'], kind='note')
    h2('4.2 Multispectral, RGB and thermal cameras')
    rows = [['Camera', 'Feature group', 'Features', 'Number'],
            ['Multispectral', 'bands', 'mean reflectance of B, G, R, RE, NIR (475, 560, 668, 717, 840 nm)', '5'],
            ['', 'indices', 'NDVI, GNDVI, NDRE, CI_{green}, CI_{rededge}, MTCI, OSAVI, SAVI, TCARI, MCARI, MSR, PSRI', '12'],
            ['', 'two-band normalised differences', '(B_{i} − B_{j}) / (B_{i} + B_{j}) for all 10 band pairs', '10'],
            ['', 'texture', '8 GLCM measures of each of the 5 bands', '40'],
            ['RGB', 'colour', 'ExG, ExR, ExG − ExR, VARI, GLI, NGRDI; mean hue, saturation and value of vegetation pixels', '9'],
            ['', 'texture', '8 GLCM measures of the R, G and B images (native 0.8-cm resolution)', '24'],
            ['Thermal', 'temperature statistics', 'mean, median, SD, 10th and 90th percentiles, maximum temperature difference MTD = highest − lowest', '6'],
            ['', 'normalised temperatures', 'CTD, CTR, NRCT, difference from healthy plots (Chapter 6)', '4'],
            ['', 'texture', '8 GLCM measures of the temperature image (64 levels over one common range)', '8']]
    tab('camfeat', rows=rows, caption='Features of the multispectral, RGB and thermal cameras (C4–C5).', widths=[1400, 2000, 5200, 1000], size=15)
    p('The multispectral indices are those used for UAV disease monitoring by Liu et al. (2024) and Nguyen et al. (2023); RGB texture is a separate data source in Feng et al. (2022); thermal statistics, normalised temperatures and MTD follow Feng et al. (2022), Calderón et al. (2014) and Oerke et al. (2006). Maimaitijiang et al. (2020) also kept the spectral, thermal and texture features of each UAV sensor as separate groups.')
    h2('4.3 The four camera tables')
    p('Each camera gets one table with one row per subplot-date (C6). Rows are identical in the four tables, so any sensor set is a join of tables by subplot code and date.')
    rows = [['Column group', 'Columns'],
            ['Identifiers', 'date, DAI, plot, subplot, replication, treatment, variety, sowing date, split (TRAIN / TEST)'],
            ['Labels', 'DI, DI class, healthy/diseased (and later-infected for the pre-symptomatic dates)'],
            ['Covariates', 'growth stage, 7-day weather, favourable days'],
            ['Features', 'with a group prefix: R_ (reflectance), FD_ (first derivative), RE_ (red edge), VI_ (indices), TX_ (texture), TH_ (thermal)']]
    tab('tablelayout', rows=rows, caption='Columns of every camera table.', widths=[2000, 7600], size=16)
    rows = [['Camera', 'Groups before selection', 'Number of features'],
            ['Hyperspectral', 'reflectance 483, first derivative 483, red edge 3, published indices 48, PCA texture 24 (+ NDSI, RSI, WRI and TTFI made in Objective 1)', 'about 1040'],
            ['Multispectral', '5 bands, 12 indices, 10 normalised differences, 40 texture', '67'],
            ['RGB', '6 colour indices, 3 colour means, 24 texture', '33'],
            ['Thermal', '6 statistics, 4 normalised temperatures, 8 texture', '18']]
    tab('featcount', rows=rows, caption='Number of candidate features of each camera.', widths=[1700, 6100, 1800], size=16)

    # ---------------------------------------------------------------- chapter 5
    h1('5. Stages 3–4 – Labels and the division of the data')
    stage_head('Stages 1–2 (camera tables).', 'every later stage: all of them use the split column, the inner folds and the validation plots made here.', 'the plot list; the division is made once, before the first flight.')
    box('In short', 'The 48 plots are divided once into 33 training plots and 15 test plots. Inside the training plots, machine-learning models are tuned with GroupKFold(3) (three rounds of 22 fitting and 11 scoring plots) and networks are stopped early on 11 fixed validation plots. The test plots are used once, at the end.', kind='key')
    h2('5.1 Joining the labels (Stage 3)')
    p('The DI, DI class and healthy/diseased label of Chapter 2 and the covariates are joined to every row of the four camera tables by plot, subplot and date (A5–A6). After this step every row is complete: identifiers, labels, covariates and features.')
    h2('5.2 Why the data are divided by whole plots')
    p('A model is useful only if it works on plots it has never seen. If subplots of the same plot were in both training and test data, the model could learn the soil, row spacing or microclimate of that plot and the test accuracy would be too high. Data with spatial or hierarchical structure must therefore be divided by groups (Roberts et al., 2017). '
      'The proportion 7:3 is that of the DT-EDNet study (Ma et al., 2026) and of other disease and UAV studies (Bijlwan et al., 2025; Abdulridha et al., 2023; Maimaitijiang et al., 2020), and close to the one-third hold-out of Mandal et al. (2023).')
    h2('5.3 How the 15 test plots are chosen (D1)')
    p('Healthy and inoculated plots are divided separately so that both are in the test set in the same proportion: **4 of the 12 healthy plots** and **11 of the 36 inoculated plots** (30%). The test plots cover all four sowing dates and all three varieties, spread over R1–R3, and are the same plots as in the 2025-26 analysis (same plot plan):')
    rows = [['Block', 'Plots', 'Test plots', 'Training plots'],
            ['Healthy', '1–12', '1, 4, 5, 8', '2, 3, 6, 7, 9, 10, 11, 12'],
            ['R3 (inoculated)', '13–24', '13, 14, 18', '15, 16, 17, 19, 20, 21, 22, 23, 24'],
            ['R2 (inoculated)', '25–36', '25, 27, 31, 35', '26, 28, 29, 30, 32, 33, 34, 36'],
            ['R1 (inoculated)', '37–48', '37, 44, 46, 48', '38, 39, 40, 41, 42, 43, 45, 47'],
            ['Total', '48', '15', '33']]
    tab('testplots', rows=rows, caption='Test and training plots of every block.', widths=[2000, 1200, 2400, 4000], size=16)
    myfig('split', 'x02_plot_split.png', 'The division of the 48 plots. Orange plots are test plots; green and blue plots are training plots (blue = validation plots of the networks).')
    p('The split column (TRAIN / TEST) is written into every table **before any analysis**, and the ASD leaves get the split of their plot.')
    h2('5.4 Validation inside the training plots (D2)')
    p('Models have settings (for example the C of an SVM) and need a feature subset; networks need a stopping epoch. These choices are made inside the 33 training plots, never on the test plots ({F:folds}):')
    nl('**Machine learning: GroupKFold(3).** The 33 training plots are divided into three groups of 11 plots. In round 1 the model is fitted on 22 plots and scored on the other 11; in rounds 2 and 3 another group is scored. The mean score of the three rounds judges a setting or a feature subset. Plots, not samples, are divided, so every round tests on new plots. Tian et al. (2021) and Lv et al. (2023) used cross-validation inside the training data for SFFS and the SVM; here the folds are made of whole plots.',
       '**Networks: 11 fixed validation plots** (6, 7, 11, 19, 24, 26, 28, 30, 36, 39, 41; random, seed 42). Network weights are fitted on the other 22 training plots; the validation plots decide when to stop and which epoch to keep. Ma et al. (2026) kept 10% of the training samples for validation; 10% would be only about three plots, so one third of the training plots is used.',
       '**The same folds and validation plots** are used for every camera, sensor set and model.')
    myfig('folds', 'x05_groupkfold.png', 'Inner validation inside the 33 training plots: three GroupKFold rounds for machine learning and the fixed network validation plots.')
    h2('5.5 Number of samples in every part')
    myfig('flow', 'x03_sample_flow.png', 'How the samples of each data set are divided.')
    rows = [['Data set', 'Training plots', 'of which network fitting (22 plots)', 'of which network validation (11 plots)', 'Test plots'],
            ['UAV post-symptomatic (per camera)', '1320', '880', '440', '600'],
            ['UAV pre-symptomatic (per camera, at most)', '396', '264', '132', '180'],
            ['ASD leaves', '5148', '3432', '1716', '2340']]
    tab('subsets', rows=rows, caption='Samples in each part of the division. In each GroupKFold round about 880 UAV samples fit and 440 score.', widths=[2700, 1500, 2000, 2000, 1400], size=15)
    h2('5.6 Which samples each stage uses')
    p('{F:datause} is the key to the whole analysis. **Descriptive** stages (response curves, correlations, physiology, stability) may use all plots, because nothing from them enters a model. **Learning** stages (feature selection, scaling constants, healthy references, tuning, fitting) use only the training plots or their inner parts. The **test plots** are only predicted.')
    myfig('datause', 'x04_data_use.png', 'Which samples each stage uses.', width=600)
    h2('5.7 Leakage rules (D5)')
    nl('No plot is on both sides of any division (training/test, fitting/scoring, fitting/validation).',
       'Selected features, scaling constants, healthy references and model weights come from the training plots only; indices of test samples are computed with the wavelengths chosen on the training plots.',
       'Every model is frozen before the test plots are predicted, and the test plots are predicted once.')
    box('On a new data set', 'Make a new plot-wise split for the new field before any analysis (30% of the plots of each block type as test plots, covering every treatment), fix new inner folds and validation plots, and write the split column into every table. If frozen 2026-27 models are only to be tested on new data, no split is needed: all new data are test data (Chapter 15).', kind='present')

    # ---------------------------------------------------------------- chapter 6
    h1('6. Stage 5 – Normalisation: what is scaled, when, and with which numbers')
    stage_head('Stage 4 (split), because every normalisation constant must come from the training plots.', 'Objective 1 (thermal and healthy references) and the models (z-score).', 'constants from the training plots (or the fitting part of each fold); applied to all samples.')
    box('In short', 'There is no z-score or min–max scaling at the start. Spectra are physically normalised (reflectance, ROI means, indices, derivatives); thermal values are expressed relative to air temperature and healthy plots; z-score scaling is done inside each model pipeline with the constants of the fitting part; ReliefF scales features to 0–1 inside its own calculation; the pre-symptomatic data are aligned to a healthy baseline.', kind='key')
    rows = [['Where', 'What is normalised', 'How', 'Constants from', 'References'],
            ['Stage 1 (B1, B6)', 'all spectra', 'reflectance from calibration panels; mean of the ROI pixels', 'panels of each flight', 'Ma et al. (2026)'],
            ['Stage 2 (C1–C2)', 'spectral features', 'indices (band ratios and differences) and derivatives remove part of the brightness effect', 'formulas only', 'Zhang et al. (2012); Mahlein et al. (2013)'],
            ['Stage 5 (D3)', 'canopy temperature', 'CTD = Tc − Ta; CTR = Tc/Ta; NRCT = (Tc − Tmin)/(Tmax − Tmin) within each date; ΔT = Tc − mean healthy Tc of the same date and variety', 'air temperature; image of the date; healthy training plots', 'Feng et al. (2022); Calderón et al. (2014); Oerke et al. (2006); Maimaitijiang et al. (2020)'],
            ['Stage 7 (ReliefF)', 'indices and camera features', 'min–max 0–1 inside the ReliefF distance', 'training plots', 'Robnik-Šikonja and Kononenko (2003); Lv et al. (2023)'],
            ['Stage 7 (SHAP-CARS)', 'candidate bands for PLS/CARS', 'z-score (random forest SHAP uses unscaled bands)', 'training plots', 'Bijlwan et al. (2025)'],
            ['Stages 9–10 (D4)', 'model inputs of SVM/SVR, k-NN, PLS, networks', 'z = (x − mean)/SD in a pipeline; random forest unscaled', 'fitting part of each fold; then all 33 training plots', 'Bijlwan et al. (2025); Shafiee et al. (2021)'],
            ['Stage 13 (3.2)', 'pre-symptomatic spectra', 'spectrum × baseline(λ)/healthy mean of the date(λ), per variety', 'healthy training plots', 'Lv et al. (2023)']]
    tab('norm', rows=rows, caption='Normalisation at each stage.', widths=[1500, 1700, 3000, 1700, 1700], size=14)
    h2('6.1 Thermal normalisation (D3)')
    p('Leaf temperature changes with air temperature, humidity and time of day, so raw temperatures of different dates cannot be compared (Oerke et al., 2006). Canopy temperature is therefore expressed in four normalised forms: the difference and ratio to air temperature (CTD, CTR; Feng et al., 2022; Calderón et al., 2014), the normalised relative canopy temperature within the image of the date (NRCT; Feng et al., 2022; Maimaitijiang et al., 2020) and the difference from the healthy training plots of the same date and variety (ΔT).')
    eq('CTD = T_{c} − T_{a}     CTR = T_{c} / T_{a}     NRCT = (T_{c} − T_{min}) / (T_{max} − T_{min})     ΔT = T_{c} − mean T_{c, healthy}')
    box('Worked example', 'Subplot 25-2: Tc = 24.1 °C, Ta = 22.0 °C → CTD = +2.1 °C, CTR = 1.095. Mean of the healthy training plots of the same variety and date = 22.9 °C → ΔT = +1.2 °C. Healthy subplot 7-1: Tc = 22.8 °C → CTD = +0.8 °C, ΔT = −0.1 °C.', kind='note')
    h2('6.2 z-score inside the model pipelines (D4)')
    p('SVM/SVR, k-NN, PLS and networks compare distances or weights between features, so a feature with large values would dominate. Each input is therefore standardised, z = (x − mean)/SD, with the mean and SD of the **fitting part only**: in each GroupKFold round the scaler is fitted on the 22 fitting plots and applied to the 11 scoring plots; the final scaler is fitted on all 33 training plots and applied to the test plots. In scikit-learn this is Pipeline(StandardScaler, model) (Pedregosa et al., 2011). Random forest is not affected by scale and gets unscaled inputs (Bijlwan et al., 2025; Shafiee et al., 2021).')
    box('Worked example', 'NDRE on the 22 fitting plots of one round: mean 0.31, SD 0.05. A scoring sample with NDRE = 0.24 gets z = (0.24 − 0.31)/0.05 = −1.4. The scoring plots never change the mean and SD.', kind='note')
    h2('6.3 Class balance')
    p('DI classes are not equally frequent. SVM and random forest use balanced class weights; the networks use the cross-entropy loss with label smoothing 0.01 (Ma et al., 2026); k-NN and PLS-DA have no class weights.')
    box('On a new data set', 'Recompute every constant (healthy means, scaling means and SDs, baseline spectra) from the training plots of the new data, or – when frozen models are tested – reuse the 2026-27 constants stored with the models.', kind='present')
