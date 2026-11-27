from m_lib import *


def add():
    h1('2. Part A – Experiment, data collection and quality control')
    card('A1', 'Field experiment and treatments',
         what='48 plots (5 m × 3.5 m) in a 48 m × 24 m field at IARI, New Delhi: one fungicide-sprayed healthy block (plots 1–12) and three unsprayed replications (R3 13–24, R2 25–36, R1 37–48). Each block holds the 12 combinations of three varieties (V1–V3) and four sowing dates (D1 9 Dec, D2 18 Dec, D3 27 Dec 2025, D4 9 Jan 2026). Infection is natural.',
         why='The design defines the units that later steps keep together (plots), the strata of the split (healthy vs unsprayed blocks) and the factors used to check robustness (variety, sowing date).',
         papers=L('Chattopadhyay et al. (2011): studied white rust of Indian mustard under natural infection over several seasons and sowing dates in India and related it to weather, to build forecasting models.',
                  'Ram and Awasthi (2018): compared white rust in improved varieties of Indian mustard in the field by visual assessment.',
                  'Mandal et al. (2023): field trial of rice genotypes under natural blast infection (upland and lowland) at Almora, scored on the 0–9 scale.'),
         match='Natural field infection with several varieties and sowing dates, as in Chattopadhyay et al. (2011) and Mandal et al. (2023). A fungicide-sprayed block gives healthy leaves of the same age and variety (Saharan et al., 2014).',
         mine='Plot plan in a1_prep.py (plot → block, timing, variety). Crop age at sampling (days after sowing, DAS) is the time variable because there is no inoculation date.',
         out='Plot table → A5 (labels), B1 (split by plots and blocks), F6 (strata), G (covariates).',
         alt='Artificial inoculation (Mahlein et al., 2013; Lv et al., 2023) gives a known infection date but not field conditions; natural infection was chosen to match the UAV phase.',
         q='Why natural infection? → Because the models are meant for field conditions; the four sowing dates create crops of different ages under the same epidemic.')
    card('A2', 'Leaf spectra with the ASD contact probe',
         what='On 11 and 24 February and 3 and 13 March 2026, leaves at three positions (L3 and L5: third and fifth fully expanded leaf from the top; LL: lowest green leaf) are measured in all 48 plots with an ASD FieldSpec spectroradiometer, contact probe and leaf clip (own halogen lamp), 350–2500 nm at 1 nm.',
         why='The leaf spectrum is the basic observation of every later step; the contact probe removes sun, sky, soil and atmosphere, so the spectrum contains only the leaf (Milton et al., 2009).',
         papers=L('Chen et al. (2023): measured tobacco leaves infected with TMV and PVY with an ASD FieldSpec 4 over 350–2500 nm.',
                  'Martínez-Martínez et al. (2018): bean angular leaf spot; spectra measured in contact with the leaves estimated severity much better than spectra taken from above the crop.',
                  'Meng et al. (2020): leaf reflectance of corn leaves with southern corn rust at several severity levels measured with a leaf clip, used to build disease indices.',
                  'Baranowski et al. (2015): hyperspectral and thermal imaging of oilseed rape (~~Brassica napus~~) leaves responding to ~~Alternaria~~.'),
         match='Same instrument class and the same single-leaf contact measurement as Chen et al. (2023) and Martínez-Martínez et al. (2018).',
         mine='One Excel file per date; each leaf column has seven header rows (wavelength, plot, variety, growth stage, healthy/diseased, leaf level, score). 2339 leaf spectra recorded.',
         out='Raw spectra (X_leaf.npy) and leaf metadata → A5.',
         q='Why single leaves and not plot means? → The grade is given to each leaf, so leaf spectra and leaf grades match one to one; plot structure is respected in the split (B1).')
    card('A3', 'Visual severity grade of the same leaf',
         what='Each measured leaf is scored on the 0–9 white rust scale (grades 0, 1, 3, 5, 7, 9) immediately after measurement.',
         why='The grade is the reference (label) for all three tasks; it must belong to the same leaf as the spectrum.',
         papers=L('Mandal et al. (2023): rice blast scored on the 0–9 scale and related to spectra.',
                  'Chen et al. (2023): tobacco virus severity in grades 0, 1, 3, 5, 7, 9 (GB/T 23222-2008) – the same six grades as here.',
                  'Bock et al. (2010): reviewed visual severity assessment; raters disagree most between neighbouring classes.'),
         match='Same 0–9 ordinal scale and the same six grade values as Chen et al. (2023); Bock et al. (2010) explains why ordinal metrics are used for Task B (F2).',
         mine='Grades 0, 1, 3, 5, 7, 9; diseased = grade > 0. After quality control: grade 0 %d, 1 %d, 3 %d, 5 %d, 7 %d, 9 %d leaves.' % tuple(CNT['grades'][str(g)] for g in (0, 1, 3, 5, 7, 9)),
         out='Labels of Tasks A, B, C → A5, E1.',
         alt='Image-based pustule area (Ashourloo et al., 2014; Lv et al., 2023) would reduce rater noise; not available for 2025-26.',
         q='Is a visual grade precise enough? → It is the field standard; its imprecision between neighbouring grades is expected (Bock et al., 2010) and is handled with ordinal metrics and a regression score.')
    card('A4', 'Weather and crop covariates',
         what='Daily weather (IARI observatory, 1 Dec 2025 – 20 Mar 2026). For each sampling date: means of the 7 days ending the day before sampling (T max, T min, RH I, RH II, wind, sunshine, evaporation; rain as total); favourable days for leaf infection and staghead counted from each sowing date; crop age (DAS); growth-stage code; variety and sowing date.',
         why='These covariates describe the epidemic and form the sensor-free baseline of Step G, against which the spectra are judged.',
         papers=L('Chattopadhyay et al. (2011): defined the weather favourable to white rust of mustard: leaf infection at T max 16–24 °C, morning RH > 97% and afternoon RH > 40%; staghead at T max 20–29 °C, T min > 12 °C, morning RH > 97%.',
                  'Bhattacharya and Chattopadhyay (2013): tracked mustard rot disease by combining surface meteorology with satellite remote sensing.',
                  'Zhang et al. (2014a): forecast wheat powdery mildew from meteorological data with and without remote sensing.'),
         match='The favourable-day counts use exactly the thresholds of Chattopadhyay et al. (2011); combining weather with sensor data follows Bhattacharya and Chattopadhyay (2013) and Zhang et al. (2014a).',
         mine='7-day windows end the day before each date (no look-ahead); stage coded 1 vegetative, 2 flowering, 3 pod formation after the BBCH ranges (Lancashire et al., 1991).',
         out='One covariate row per leaf → G.',
         q='Why windows ending the day before? → So that no weather from after the measurement enters any model.')
    card('A5', 'Data organisation and quality control',
         what='The four files are parsed into one leaf table and checked: (1) plots joined to the plan; (2) L4 spectra removed; (3) duplicated spectra removed; (4) residual detector step at 1000 nm corrected; (5) value checks.',
         why='Every later step assumes one correct spectrum per leaf. Duplicates would count the same leaf twice; a detector step creates a false feature in derivatives and wavelets.',
         papers=L('No disease paper describes these checks in detail; they follow the instrument literature.',
                  'Hueni and Bialek (2017): showed that the joins between the three ASD detectors (near 1000 and 1800 nm) produce radiometric steps that change with instrument temperature, and gave an additive correction.',
                  'Mandal et al. (2023) and Selvaprakash et al. (2026) report pre-processing of handheld spectroradiometer data before analysis.'),
         match='The additive splice correction of Hueni and Bialek (2017) is applied; the same correction was used in my earlier white rust analyses that replicated Tian et al. (2021) and Mandal et al. (2023).',
         mine=steps('Join each plot to block, timing and variety; check that the variety in the file equals the plot plan.',
                    'Remove the 9 spectra labelled L4 (not a sampled position).',
                    'Find identical spectra (all 2151 values equal) and keep one copy: 75 copies removed (13 March 2026; plots 13, 34, 38, 41, 42).',
                    'Splice correction at each detector join (1000/1001 and 1800/1801 nm): the jump between the two bands is compared with the local slope on both sides; where the median excess is larger than 0.0005 reflectance, the bands above the join are shifted leaf by leaf so that the jump equals the local slope (needed at 1000 nm; no step at 1800 nm).',
                    'Check grades (0, 1, 3, 5, 7, 9 only), 2151 bands, no missing values, reflectance range, all 48 plots on every date.') + '\nResult: %d leaf spectra.' % CNT['all'],
         out='meta.csv and corrected spectra → B1 (split), C (features).',
         alt='Leaving the detector step in place would let ReliefF and wavelet selection pick the artefact (as found in my earlier Lv et al. (2023) replication).',
         q='How were duplicates found? → By comparing all 2151 values of every pair of spectra; identical spectra cannot come from two different leaves.')
    card('A6', 'Labels for the three tasks',
         what='Task A: 0 = grade 0, 1 = grade > 0. Task B: six classes coded 0–5 for grades 0, 1, 3, 5, 7, 9. Task C: grade 0–9 as a number.',
         why='Each task answers a different practical question and needs its own metrics (F1–F3).',
         papers=L('Lv et al. (2023): asymptomatic and symptomatic detection plus severity classes for southern corn leaf blight.',
                  'Chen et al. (2023): binary (healthy/infected) and six-class (severity grade) models for tobacco viruses.',
                  'Zhang et al. (2012): normal / slight / heavy powdery mildew classes plus a PLSR estimate of the disease index.',
                  'Mandal et al. (2023): regression and classification of rice blast severity on the 0–9 scale.'),
         match='The combination of a detection task, a severity-class task and a severity regression follows Lv et al. (2023), Chen et al. (2023) and Zhang et al. (2012).',
         mine='Class weights balanced in all classifiers because grade 9 is the rarest class (E3).',
         out='Labels → E, F, G.')

    # ---------------------------------------------------------------- Part B
    h1('3. Part B – Validation design: the grouped, stratified 70:30 split')
    p('The split decides which leaves may teach the models and which leaves test them. It is fixed once, before any feature selection or model fitting, and is kept for every part of the analysis.')
    card('B1', 'Grouped, stratified 70:30 hold-out of whole plots',
         what='The 48 plots are divided once into 33 training plots (TRAIN) and 15 test plots (TEST). Whole plots go to one side only. Healthy and unsprayed plots are split separately.',
         why='It must come before Step C-E, because every choice that learns from the data (features, subsets, settings, epochs) may use only the training plots.',
         papers=L('Ma et al. (2026): rice blast (UAV hyperspectral, 2,690 canopy samples) divided by stratified sampling into training and test sets at 7:3, with 10% of the training set as validation; plus an independent cross-year test (2023 → 2024).',
                  'Mandal et al. (2023): rice blast data divided by stratified sampling into two-thirds calibration and one-third validation; all modelling on the calibration part.',
                  'Wang et al. (2016): wheat rust severity models checked with leave-one-out cross-validation and an external validation set.',
                  'Kattenborn et al. (2022): plant mapping from UAV images; random splits over-estimated accuracy by up to 28% compared with spatially blocked splits.',
                  'Roberts et al. (2017): showed that dependent samples must be held out in blocks.'),
         match='The 70:30 proportion and stratification are those of Ma et al. (2026) and close to Mandal et al. (2023). Unlike them, whole plots are assigned, because leaves of one plot share soil, microclimate and inoculum (Roberts et al., 2017; Kattenborn et al., 2022).',
         mine=steps('Plot table with block, timing, variety, number of leaves.',
                    'Test plots per block type = round(0.30 × plots): 4 healthy, 11 unsprayed.',
                    'Random candidates obeying the rules: the 11 unsprayed test plots are 11 different treatments, spread as evenly as possible over R1–R3, varieties and sowing dates; the 4 healthy test plots have different sowing dates.',
                    '5000 different candidates (seed 2026); each scored by |leaf share − 0.30| + 0.5 × (0.5 × Σ|grade-share difference| + 0.5 × Σ|date-share difference|).',
                    'The lowest score is kept: test plots 1, 4, 5, 8 (healthy) and 13, 14, 18, 25, 27, 31, 35, 37, 44, 46, 48 (unsprayed).') +
             '\nAfter quality control: TRAIN %d leaves, TEST %d leaves (%.1f%%). The split was drawn before quality control and is kept unchanged.' % (CNT['train'], CNT['test'], 100 * CNT['test_share']),
         out='Column fold (0 = TEST, 1 = TRAIN) → every later step. Scripts split_lib.py, split_cfg.py.',
         alt='Random leaf split (Ma et al., 2026; Mandal et al., 2023) is simpler but would put leaves of one plot on both sides; leave-one-replication-out tests every leaf once and is used as a check (H3).',
         q='Was the best of 5000 splits chosen because models did well on it? → No; the score uses only leaf, grade and date counts, never a spectrum or a model result. It is stratified sampling.')
    eq('score = | n_{test} / N − 0.30 | + 0.5 × [ 0.5 × Σ_{g} | p_{g}(test) − p_{g}(all) | + 0.5 × Σ_{d} | p_{d}(test) − p_{d}(all) | ]')
    p('n_{test} is the number of leaves in the candidate test plots, N the number of all leaves, p_{g} the share of grade g and p_{d} the share of sampling date d. '
      'The first term keeps the test set at 30% of the leaves; the bracket keeps its grade and date mix like that of all leaves (Kuhn and Johnson, 2013).')
    myfig('splitmap', 'm03_split_map.png', 'Field plan with the 15 test plots (dark), the 33 training plots (light) and the 11 training plots used for early stopping of the networks (purple).')
    card('B2', 'Validation inside the training plots',
         what='Settings, feature subsets and stopping epochs are chosen inside TRAIN with a second division by plot: inner GroupKFold(3) for machine learning (three rounds of 22 fitting and 11 scoring plots) and a fixed set of 11 validation plots for the networks.',
         why='A model must be tuned on data it is not tested on; tuning on TEST would make the test accuracy optimistic (Varma and Simon, 2006; Cawley and Talbot, 2010).',
         papers=L('Ma et al. (2026): 10% of the training set as validation; the model with the highest validation accuracy was kept and then tested once.',
                  'Tian et al. (2021): rice leaf blast; SFFS wrapped around LDA, k-NN and SVM with 4-fold cross-validation repeated 100 times.',
                  'Lv et al. (2023): southern corn leaf blight; RELIEF-F, SFFS and SVM with 4-fold stratified cross-validation repeated 100 times.'),
         match='The inner validation of Ma et al. (2026), Tian et al. (2021) and Lv et al. (2023), but always by whole plots: GroupKFold(3) for ML and one third of the training plots for the networks.',
         mine='ML: GroupKFold(3) over the 33 training plots. Networks: 11 training plots (6, 7, 11, 19, 24, 26, 28, 30, 36, 39, 41; random, seed 42) = %d leaves; 22 plots = %d leaves fit the weights.' % (CNT['dlval'], CNT['dlfit']),
         out='Inner folds → E2–E7.',
         alt='10% of the training leaves as in Ma et al. (2026) would be about three plots – too few to represent the blocks, and leaves of one plot would be in fitting and validation.',
         q='Why one third and not 10% for the networks? → With whole plots, a third (11 plots) covers all blocks; 10% would be about three plots.')
    card('B3', 'Leakage rules that hold in every step',
         what='(1) Leaves of one plot are never on both sides of any division. (2) Every statistic that is learned (means and SDs for scaling, selected features, model weights) is computed from the fitting part only. (3) TEST is used once.',
         why='These rules make the test accuracy an honest estimate for new plots.',
         papers=L('Ambroise and McLachlan (2002): selecting features on all samples before validation gave error rates near zero even without real signal.',
                  'Ma et al. (2026): feature selection and model training on the 2023 data, evaluation on the independent 2024 data.',
                  'Roberts et al. (2017); Kattenborn et al. (2022): blocked validation for dependent samples.'),
         match='Feature selection for the models is repeated on TRAIN (E2), as Ma et al. (2026) selected features on the training year only.',
         mine='Scaling is fitted inside each inner fold (pipeline); the Objective 1 description (D) on all leaves is never passed to the models.',
         out='Rules → C–H.')
