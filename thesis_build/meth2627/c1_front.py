from c_lib import *


def add():
    B.append(dict(t='title', title='AI-based multimodal UAV sensing of white rust in Indian mustard: complete research methodology, season 2026-27',
                  subtitle='Step-by-step protocol for the UAV cameras and the ASD leaf spectra, with the disease papers behind every step. Grouped 7:3 split by whole plots. No results – demo data only.',
                  lines=['Animesh Panda · Ph.D. (Agricultural Physics) · ICAR-Indian Agricultural Research Institute, New Delhi',
                         'For the Advisory Committee, 2026-27. Leaf scoring on 5 plants per subplot; ASD leaf spectra on the centre plant of each subplot.',
                         'Every step: what is done, why at this position, disease papers – what they did, how my step follows them, with my data (exact settings), checks, output → next step.']))
    B.append(dict(t='toc'))

    h1('How to use this document')
    nl('**Follow the parts in order:** A (field and data) → B (UAV image processing) → C (features) → D (split and normalisation) → Objectives 1, 2 and 3 (UAV) → Part L (ASD leaf spectra). The master checklist (Chapter 1) lists every step.',
       '**Each step has one card** with the same rows: what is done; why at this position; disease papers – what they did; how my step follows them; with my data (exact settings, numbered actions); checks to tick; output → next step; alternatives and notes; likely question → answer.',
       '**Tick every box** under "Check before the next step" before moving on.',
       '**Nothing is decided after seeing the test plots.** The 15 test plots are fixed before the first flight and used once, at the end of each objective.',
       '**Demo tables and figures** show the layout of every output with invented numbers; they are not results.')
    rows = [['Abbreviation', 'Meaning', 'Abbreviation', 'Meaning'],
            ['ASD', 'ASD FieldSpec field spectroradiometer', 'OW', 'optimal wavelengths (SHAP-CARS)'], ['BBCH', 'growth-stage scale', 'PCA', 'principal component analysis'],
            ['CARS', 'competitive adaptive reweighted sampling', 'PLS-DA / PLSR', 'partial least squares discriminant analysis / regression'], ['DAI', 'days after inoculation', 'ReliefF', 'Relief-F feature weighting'],
            ['DI', 'disease index (%)', 'RSI', 'ratio spectral index'], ['DSF', 'disease-specific feature set', 'ROI', 'region of interest'],
            ['FD', 'first derivative', 'SFFS', 'sequential floating forward selection'], ['GLCM', 'grey-level co-occurrence matrix', 'SHAP', 'Shapley additive explanations'],
            ['HS, MS, RGB, TIR', 'hyperspectral, multispectral, red–green–blue, thermal cameras', 'SVM / SVR', 'support vector machine / regression'],
            ['k-NN', 'k-nearest neighbours', 'TTFI', 'Tri-band Texture Fusion Index'], ['mRMR', 'minimum redundancy maximum relevance', 'VI', 'selected vegetation indices'],
            ['NDSI', 'normalised difference spectral index', 'VIF', 'variance inflation factor'], ['NDVI', 'normalised difference vegetation index', 'WRI', 'White Rust Index']]
    tab('abbr', rows=rows, caption='Abbreviations.', widths=[1500, 3300, 1500, 3300], size=16)

    h1('1. Objectives, design and data')
    h2('1.1 Background and objectives')
    p('White rust, caused by the oomycete ~~Albugo candida~~, produces white pustules on leaves and stagheads on inflorescences of Indian mustard (~~Brassica juncea~~) and causes large yield losses in India (Saharan et al., 2014). '
      'Infected leaves lose pigments and water and change their biochemistry (Mishra et al., 2009), and the disease develops under cool, humid weather (Chattopadhyay et al., 2011). '
      'These changes alter canopy reflectance, temperature and texture, which UAV cameras can record (Mahlein, 2016). '
      'The methodology follows the disease studies that used the same cameras or the same analysis steps, above all the DT-EDNet study of rice blast (Ma et al., 2026).')
    rows = [['Objective', 'Question', 'Data', 'Main outputs'],
            ['1. Characterise white rust through multimodal UAV sensing', 'How does each camera (and the leaf spectrum) see white rust, and which features carry the disease signal?', 'post-symptomatic (1920 subplot-dates per camera) and pre-symptomatic (576) samples; 7488 ASD leaf spectra; physiology', 'response curves, optimal wavelengths, White Rust Index, selected indices and texture, disease-specific feature set (DSF), physiological basis'],
            ['2. Detect and discriminate severity through AI-based multimodal data fusion', 'Which camera or camera combination detects white rust and grades its severity best?', 'post-symptomatic samples, 15 sensor sets', 'accuracy on the 15 test plots of every sensor set and model; gain over a covariate-only model; maps; Bharatpur test'],
            ['3. Predict white rust at the pre-symptomatic stage', 'Can subplots that will develop white rust be separated from healthy subplots before pustules appear?', '576 pre-symptomatic samples (2, 5, 8 DAI)', 'pre-symptomatic models, earliest detection day, risk maps']]
    tab('objectives', rows=rows, caption='Objectives, questions, data and outputs.', widths=[2300, 2600, 2300, 2400], size=16)
    h2('1.2 Overall workflow')
    myfig('workflow', 'g01_workflow.png', 'Overall workflow: Parts A–D are done once; Objectives 1–3 use the UAV data; Part L analyses the ASD leaf spectra of the centre plant of every subplot.')
    h2('1.3 Data of the 2026-27 season')
    rows = [['Data', 'Unit of one sample', 'Dates', 'Samples', 'Training plots (33)', 'Test plots (15)'],
            ['UAV images, 4 cameras (HS, MS, RGB, TIR)', 'one subplot on one date', '10 post-symptomatic dates', '48 plots × 4 subplots × 10 = 1920 per camera', '1320', '600'],
            ['', '', '3 pre-symptomatic dates', '48 × 4 × 3 = 576 per camera', '396', '180'],
            ['ASD leaf spectrum + leaf grade', 'one leaf on one date', '13 dates', '48 × 4 subplots × 1 centre plant × 3 leaves = 576 per date; 7488 in all', '5148', '2340'],
            ['Disease index (DI)', 'one subplot on one date', '13 dates', 'from the 15 graded leaves of 5 plants per subplot (2880 grades per date)', '–', '–'],
            ['Biochemical and biophysical parameters', 'one designated subplot per plot', '4 dates', '48 per parameter and date', '–', '–'],
            ['Covariates (DAI, variety, timing, stage, weather)', 'one subplot on one date', '13 dates', 'one row per sample', '–', '–'],
            ['Bharatpur independent test', 'one quadrat on one date', '2–3 dates', '≥ 300 quadrat-dates', 'not used for training', 'all']]
    tab('datasets', rows=rows, caption='Data collected in 2026-27 and their division between the 33 training plots and the 15 test plots.', widths=[2200, 1500, 1500, 2300, 1100, 1000], size=15)
    h2('1.4 Data sets needed for the whole analysis')
    p('The analysis needs the following data sets. Each must carry the plot, subplot and date codes so that every table can be joined.')
    rows = [['No.', 'Data set', 'Content and format', 'When', 'Amount', 'Used in'],
            ['1', 'Field plan', 'plot number, block, replication, sowing date, variety, plot and subplot corners (GPS); Excel + shapefile', 'before sowing', '48 plots, 192 subplots', 'A1, B6, D1'],
            ['2', 'Inoculation record', 'date, suspension concentration, method, weather of the day', '30 Dec 2026', '1 sheet', 'A1, A6'],
            ['3', 'UAV hyperspectral images', 'raw VNIR and SWIR cubes, GNSS/IMU files, dark and white calibration files', '13 dates', 'whole field per date', 'B1–B6, C1–C3'],
            ['4', 'UAV multispectral images', '5-band frames and downwelling-light-sensor files', '13 dates', 'whole field per date', 'B1–B6, C4'],
            ['5', 'UAV RGB images', 'RAW/JPG frames', '13 dates', 'whole field per date', 'B2–B6, C4'],
            ['6', 'UAV thermal images', 'radiometric frames', '13 dates', 'whole field per date', 'B1–B6, C5'],
            ['7', 'Calibration and flight data', 'panel certificates; panel images before and after each flight; GCP coordinates (RTK); flight log (time, sky, wind, air temperature, RH, height)', 'every flight', '13 sets', 'B1, B2, B4, D3'],
            ['8', 'Leaf scoring sheets', 'date, plot, subplot, plant (centre or corner 1–4), leaf position (L3, L5, LL), grade 0–9; staghead racemes', '13 dates', '2880 grades per date (37 440)', 'A3, A5, Part L'],
            ['9', 'ASD leaf spectra', '.asd files of the centre plant (2 readings per leaf) and ASCII export; white-reference log', '13 dates', '1152 readings per date (14 976)', 'A4, Part L'],
            ['10', 'Growth stage', 'BBCH stage of every plot', '13 dates', '624 records', 'A6, 1.1.3, 2.10'],
            ['11', 'Weather', 'daily Tmax, Tmin, RH I, RH II, rainfall from the IARI observatory, 1 Dec 2026 – 31 Mar 2027', 'daily', '≈ 120 days', 'A6, 2.9, 3.5, L8'],
            ['12', 'Biochemical and biophysical parameters', '10 parameters of the designated subplot; LI-6400 files', '4 dates', '48 per parameter and date', 'A7, 1.7'],
            ['13', 'Bharatpur test data', 'images of the 4 cameras, quadrat positions (RTK), scoring sheets (5 plants per quadrat), covariates, local weather', '2–3 dates', '≥ 300 quadrat-dates', 'A8, 2.11'],
            ['14', 'Glasshouse data', 'pot plan, inoculation record, 0–6 severity, ASD spectra', '2, 5, 8, 11 DAI, then weekly', '48 pots', 'A9'],
            ['15', 'Tables made during the analysis', 'subplot ROI means of each camera; feature tables; leaf table; split file (test plots); inner folds and validation plots', 'after Parts B–D', '–', 'all later steps']]
    tab('datasets_needed', rows=rows, caption='Data sets needed for the whole analysis.', widths=[500, 1800, 3500, 1300, 1400, 1100], size=15)
    h2('1.5 Rules that hold in every step')
    nl('One sample is one subplot on one date (UAV) or one leaf on one date (ASD). All samples of a plot stay together in the training part or in the test part.',
       'The 15 test plots are fixed before the first flight (Step D1) and are used once, at the end.',
       'Every step that learns from the labels (feature selection for the models, tuning, early stopping, scaling constants) uses the 33 training plots only: GroupKFold(3) by plot for machine learning, 11 of the 33 training plots for the early stopping of the networks.',
       'In Objective 1 (and Part L), descriptive steps use all samples, while every feature-selection step uses the training plots only; the selected features are used unchanged by the models (Ma et al., 2026).',
       'All cameras are measured on the same subplot ROIs; each sample is the field-level average of its ROI (Step B6).',
       'Every sensor model is compared with a covariate-only model, because severity also follows time and weather (Step 2.9).')
    h2('1.6 Main disease papers used')
    rows = [['Paper', 'Disease, crop, data', 'Steps of this document that follow it'],
            ['Ma et al. (2026)', 'rice blast; UAV hyperspectral; DT-EDNet', 'D1, 1.2, 1.3, 1.4, 1.5, 2.6–2.8, 2.11, L5, L6'],
            ['Guo et al. (2021)', 'wheat yellow rust; UAV hyperspectral', 'A3, B1, B2, B5, B6, C3, 1.1, 1.5'],
            ['Feng et al. (2022)', 'wheat powdery mildew; hyperspectral + thermal + RGB fusion', 'A2, B4, C5, C6, 2.2, 2.8'],
            ['Liu et al. (2024); Liu et al. (2026)', 'wheat powdery mildew; UAV multispectral + thermal; ground-to-UAV index', 'A3, C4, C5, 1.3, 2.10, L9'],
            ['Calderón et al. (2014)', 'opium poppy downy mildew; UAV thermal + multispectral', 'A4, C5, D2'],
            ['Tian et al. (2021)', 'rice leaf blast, asymptomatic to mild; leaf spectra', 'A5, D1, 1.6, 2.3, 3.1, L10'],
            ['Lv et al. (2023)', 'southern corn leaf blight; leaf-clip spectra', 'D1, 1.4, 1.6, 2.3, L3, L5'],
            ['Mandal et al. (2023)', 'rice blast (0–9 scale); handheld spectroradiometer', 'A4, L3–L7'],
            ['Mahlein et al. (2013)', 'sugar-beet diseases; disease-specific indices, ReliefF', '1.3, 1.4, L5'],
            ['Zhang et al. (2014a)', 'wheat powdery mildew; weather with and without remote sensing', 'A6, 2.9, 3.5, L8'],
            ['Zarco-Tejada et al. (2018); Zhu et al. (2017)', 'Xylella in olive; tobacco virus; pre-symptomatic detection', 'A7, 1.8, 3.1–3.6'],
            ['Chattopadhyay et al. (2011)', 'white rust of Indian mustard; weather', 'A6, A8'],
            ['Mishra et al. (2009)', 'white rust of Indian mustard; pathological and biochemical changes', 'A1, A7, A9, 1.7']]
    tab('papers_main', rows=rows, caption='Main disease papers and the steps that follow them.', widths=[2500, 3700, 3400], size=16)
    h2('1.7 Recent disease studies (2021–2026) behind the methodology')
    p('Most steps follow studies published in the last five years. The table lists them with what each contributes; older papers are used mainly for the original definitions of methods and indices.')
    rows = [['Study', 'Disease, crop and data', 'What it contributes', 'Steps'],
            ['Ma et al. (2026)', 'rice blast; UAV hyperspectral; DT-EDNet', '7:3 split; effective ranges; SHAP-CARS; Relief indices; mRMR texture; TTFI; network comparison and ablation', 'D1, 1.2–1.5, 2.6, 2.8'],
            ['Liu et al. (2026)', 'wheat powdery mildew; leaf and canopy spectrometers, UAV', 'disease-specific index carried from ground to UAV', '1.3.2, L9'],
            ['Selvaprakash et al. (2026)', 'rice blast (IARI); leaf spectra 350–2500 nm', 'smoothing, exhaustive index search, PCA', 'L3, L5'],
            ['Yuan et al. (2025)', 'rice bacterial blight; UAV + satellite', 'mRMR; RF, SVM, k-NN; UAV-to-satellite transfer', '1.5.1, 2.4, 2.11'],
            ['Yu et al. (2025)', 'rice sheath blight; spectral + physiological signatures', 'physiology analysed with spectra; multimodal network', 'A7, 2.5'],
            ['Bijlwan et al. (2025)', 'crop disease severity; weather variables', 'weather-only machine-learning baseline', '2.9, L8'],
            ['Deng et al. (2024)', 'wheat stripe rust; multimodal deep learning', 'deep network for the disease index; maps', '2.5, 2.10'],
            ['Liu et al. (2024)', 'wheat powdery mildew; UAV multispectral + thermal', 'multi-features, thermal features, results by stage', 'A2, C4, C5, 2.10'],
            ['Zhang et al. (2024)', 'tomato bacterial leaf spot; hyperspectral imaging', 'water and red-edge bands before symptoms', '1.8.1, 3.5, L10'],
            ['Cross et al. (2024)', 'wheat stripe rust; hyperspectral reflectance', 'disease progression; hold-out testing', 'D1, L5.1'],
            ['Abdulridha et al. (2023)', 'wheat stem rust; drone hyperspectral', 'random forest; severity levels; maps', '2.1, 2.4, 2.10'],
            ['Blasch et al. (2023)', 'wheat yellow and stem rust; UAV + satellite', 'varieties of different resistance; growth stages; calibration', 'A1, B1, 1.1.3, 2.10'],
            ['Nguyen et al. (2023)', 'wheat yellow rust; multispectral UAV', 'red-edge and NIR bands; MS indices and texture; early detection by date', 'A2, C4, 3.4'],
            ['Mandal et al. (2023)', 'rice blast (IARI); handheld spectroradiometer', 'leaf spectra, indices, JM distance, RPD', 'A4, L3–L7'],
            ['Lv et al. (2023)', 'southern corn leaf blight; leaf-clip spectra', 'ReliefF, VIF, SFFS; inner cross-validation', 'D2, 1.4, 1.6, 2.3'],
            ['Terentev et al. (2023)', 'wheat leaf rust; hyperspectral', 'detection from the fourth day after inoculation', '1.8, L10'],
            ['Mustafa et al. (2023)', 'wheat Fusarium head blight; multimodal', 'smoothing; VIF', 'B3, 1.6.2'],
            ['Poblete et al. (2023)', 'vascular pathogens of tree crops; satellite vs airborne', 'transfer of detection to other sensors', '2.11, L9'],
            ['Chen et al. (2023)', 'tobacco viruses; ASD FieldSpec 4 leaves', 'grades 0, 1, 3, 5, 7, 9; smoothing', 'A3, A4, L1, L3'],
            ['Zhang et al. (2022)', 'rice leaf blast; hyperspectral imaging of leaves', 'leaf grades at several growth stages; SVM', 'A3, 1.1.3, L6'],
            ['Mandal et al. (2022)', 'rice blast (IARI); 0–9 scale', 'sensitive regions; red-edge amplitude', 'A4, C1'],
            ['Chatterjee et al. (2022)', 'white rust of Indian mustard', 'biochemical changes in infected plants', 'A7'],
            ['Feng et al. (2022); Ruan et al. (2022)', 'wheat powdery mildew; wheat stripe rust', 'fusion of hyperspectral, thermal and RGB; remote sensing + weather', 'A2, 2.2, 2.8, 2.9'],
            ['Tian et al. (2021); Guo et al. (2021); Yu et al. (2021); Bohnenkamp et al. (2021); Kundu et al. (2021)', 'rice leaf blast; wheat yellow rust; pine wilt; wheat foliar diseases; potato late blight', 'SFFS and early stages; PCA texture and NDVI mask; red-edge parameters; spectral library; DWSI', 'many steps']]
    tab('recent', rows=rows, caption='Recent disease studies (2021–2026) and the steps that follow them.', widths=[2300, 2700, 3400, 1200], size=15)
    h2('1.8 Master checklist')
    p('Tick each step when every box of its "Check before the next step" row is ticked.')
    B.append(dict(t='placeholder', name='master'))
    h2('1.9 Expected outcomes')
    rows = [['Objective', 'Expected outcome'],
            ['1', 'Sensitive spectral ranges, signatures and indices for the characterisation of white rust of mustard under glasshouse and field conditions, across crop stages and severity levels, for large-scale application.'],
            ['2', 'The best suitable sensor or fusion of sensors for detection and monitoring of white rust throughout the crop growth stages.'],
            ['3', 'Early, pre-symptomatic detection so that appropriate preventive measures can be taken in time.']]
    tab('outcomes', rows=rows, caption='Expected outcomes.', widths=[1200, 8400], size=17)
