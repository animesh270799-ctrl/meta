from c_lib import *


def add():
    h1('7. Objective 2 – Detection and severity discrimination through artificial intelligence-based multimodal data fusion')
    p('Objective 2 builds and compares predictive models on the post-symptomatic subplot-dates: 1320 from the 33 training plots for selection and training, 600 from the 15 test plots for the single final test. '
      'Every single camera and every combination of cameras (15 sensor sets) is modelled for the three tasks with the same plots, so that cameras, combinations and models can be compared directly.')
    myfig('models', 'g11_models.png', 'Model families, inner validation and test of Objective 2 (left); demo of a pseudo-image for the networks (right).')
    P = 'Objective 2'

    h2('Activity 2.1 – Tasks and sensor sets')
    step('2.1', 'Three tasks and 15 sensor sets', part=P,
         what='Task A: healthy vs diseased; Task B: DI class; Task C: DI (%). Sensor sets: four single cameras, six pairs, four triplets and all four cameras.',
         why='The objective asks which camera or combination works best; all combinations are tested on the same plots so that differences are due to the cameras.',
         do=['S1 HS, S2 MS, S3 RGB, S4 TIR; S5 HS+MS, S6 HS+RGB, S7 HS+TIR, S8 MS+RGB, S9 MS+TIR, S10 RGB+TIR; S11 HS+MS+RGB, S12 HS+MS+TIR, S13 HS+RGB+TIR, S14 MS+RGB+TIR; S15 all four.',
             'Tabulate class counts of Tasks A and B on the training and test plots.'],
         check=['Class counts table; classes with < 5% merged (Step A5).'],
         out='Task × sensor-set matrix → 2.2.',
         papers=[('Tian et al. (2021)', 'Rice leaf blast; detection at early stages and discrimination of severity with several models.', 'Detection and severity tasks.'),
                 ('Feng et al. (2022)', 'Wheat powdery mildew; models from each single data source (indices, temperature, texture) compared with fused sources.', 'Single cameras and their combinations compared.'),
                 ('Abdulridha et al. (2023)', 'Wheat stem rust; drone hyperspectral data for detection and severity levels.', 'Detection plus severity levels.')])

    h2('Activity 2.2 – Feature selection on the training plots and fusion')
    step('2.2', 'Selection repeated on the training plots; feature-level fusion', part=P,
         what='The selection chain of Objective 1 (1.2–1.6) is run again on the 1320 training samples only; the DSFs of the cameras of a sensor set are concatenated and VIF < 10 is applied again.',
         why='Features chosen with the test plots would make the test accuracy optimistic.',
         do=['Run 1.2.1–1.6.2 on the training plots for each camera and task.', 'For a sensor set, join the camera DSFs; remove features until all VIF < 10.', 'Compute the index values of the test samples with the wavelengths chosen on the training plots.'],
         check=['A DSF for each of the 15 sensor sets × 3 tasks, chosen on training plots only.'],
         out='Inputs of every model → 2.3–2.6.',
         papers=[('Ma et al. (2026)', 'Rice blast; feature selection on the training data (2023) only; testing on independent 2024 data.', 'Selection on the training plots only.'),
                 ('Feng et al. (2022)', 'Wheat powdery mildew; vegetation indices, thermal temperature parameters and texture features fused at feature level; PLSR, random forest and SVR compared.', 'Feature-level fusion by concatenation.'),
                 ('Liu et al. (2024)', 'Wheat powdery mildew; spectral, texture and canopy-temperature features fused after Pearson correlation and recursive feature elimination.', 'Same fusion level after selection.'),
                 ('Huang et al. (2020)', 'Wheat Fusarium head blight; spectral, colour and texture features of hyperspectral images of ears fused for severity diagnosis.', 'Feature-level fusion of spectral, colour and texture features.')])

    h2('Activity 2.3 – Machine-learning models')
    step('2.3', 'Sequential floating forward selection', part=P,
         what='For each ML model, SFFS adds the feature that most improves the GroupKFold(3) score and after each addition tries to remove one; the subset with the best score (at most 15 features) is kept.',
         why='Each model may need a different, smaller subset of the DSF.',
         do=['Criterion: macro-F1 (Tasks A, B) or negative RMSE (Task C); folds of Step D2.', 'Record the best subset of each size up to 15; keep the best one.'],
         check=['Subset and inner score of every model × sensor set × task.'],
         out='Feature subsets → 2.4.',
         papers=[('Tian et al. (2021)', 'Rice leaf blast; SFFS wrapped around LDA, k-NN and SVM found optimal combinations of 2–4 features; SVM-SFFS was best.', 'SFFS wrapped around each model.'),
                 ('Lv et al. (2023)', 'Southern corn leaf blight; SFFS with the SVM macro-F1 as criterion after RELIEF-F and VIF.', 'Macro-F1 criterion after ReliefF and VIF.')])
    step('2.4', 'Models, tuning grids and final fit', part=P,
         what='SVM/SVR, random forest, k-NN and PLS-DA/PLSR are tuned by grid search with the same inner folds, refitted on all 33 training plots and used once on the test plots.',
         why='Classical models are the reference for the networks and are used in most disease studies.',
         do=['Grid search on the SFFS subset (GroupKFold(3)).', 'Refit the best setting on all training samples.', 'Predict the 600 test samples once and save model, subset and predictions.'],
         check=['Model files and test predictions for 4 models × 15 sets × 3 tasks.'],
         out='ML predictions → 2.7.',
         papers=[('Tian et al. (2021)', 'Rice leaf blast; SVM C and γ by grid search; k-NN and LDA compared.', 'SVM and k-NN tuned by grid search.'),
                 ('Lv et al. (2023)', 'Southern corn leaf blight; SVM C and γ by grid search with cross-validation.', 'Grid search inside the training data.'),
                 ('Abdulridha et al. (2023); Yuan et al. (2025)', 'Wheat stem rust; rice bacterial blight: random forest (and SVM, k-NN) on UAV features.', 'Random forest, SVM and k-NN on UAV data.'),
                 ('Zhang et al. (2012); Mandal et al. (2023)', 'Wheat powdery mildew; rice blast: PLSR (and PLS-DA / Fisher discriminant) for severity.', 'PLS models for severity.')])
    rows = [['Model', 'Grid (GroupKFold(3))', 'Disease papers'],
            ['SVM / SVR (RBF)', 'C ∈ {0.1, 1, 10, 100}; γ ∈ {0.001, 0.01, 0.1, scale}; ε ∈ {0.1, 0.5}', 'Tian et al. (2021); Lv et al. (2023); Yuan et al. (2025)'],
            ['Random forest', '500 trees; max_features ∈ {sqrt, 0.3}; min_samples_leaf ∈ {1, 3, 5}', 'Abdulridha et al. (2023); Liu et al. (2024); Yuan et al. (2025)'],
            ['k-NN', 'k ∈ {3, 5, 7, 9, 11}; uniform or distance weights', 'Tian et al. (2021); Yuan et al. (2025)'],
            ['PLS-DA / PLSR', '1–15 components', 'Zhang et al. (2012); Mandal et al. (2023)']]
    tab('mlgrid', rows=rows, caption='Machine-learning models and tuning grids.', widths=[1800, 4600, 3200], size=16)

    h2('Activity 2.4 – Deep-learning models')
    step('2.5', 'Deep neural network with input-level feature fusion', part=P,
         what='A small fully connected network takes the fused feature vector (input-level fusion) for Tasks A, B and C.',
         why='Tests whether a neural network gains over the ML models on the same fused features, including the regression of DI.',
         do=['Two hidden layers (64 and 32 units), batch normalisation, ReLU, dropout 0.3; softmax (A, B) or linear output (C).', 'AdamW and the schedule of Step 2.6; fit on 22 training plots, early stopping on the 11 validation plots.'],
         check=['Learning curves saved; best epoch recorded.'],
         out='DNN-F1 predictions → 2.7.',
         papers=[('Deng et al. (2024)', 'Wheat stripe rust; RustQNet, a multimodal deep network that estimated the disease index from UAV data.', 'A neural network on multimodal UAV features, including regression of the DI.'),
                 ('Liu et al. (2020)', 'Wheat Fusarium head blight; a neural network classifier on UAV hyperspectral bands, indices and texture.', 'Neural network on selected UAV features.'),
                 ('Martínez-Martínez et al. (2018)', 'Bean angular leaf spot; neural networks estimated severity from reflectance.', 'Network regression of severity.'),
                 ('Yu et al. (2025)', 'Rice sheath blight; dual-branch multimodal network fusing spectral and physiological signatures.', 'A neural network on fused multimodal features.')])
    step('2.6', 'Pseudo-image networks: Dual Transformer Early Detection Network and its comparison networks', part=P,
         what='The selected features are arranged as a k × k pseudo-image and classified (Tasks A and B) by DT-EDNet, EfficientNet-B0, ResNet18 and ConvNeXt V2-Atto with identical settings.',
         why='DT-EDNet is the network of the core reference paper; the three others are its comparison networks.',
         do=['Pseudo-image side k = ⌈√p⌉ (at least 3) for p features; features in group order (OW, VI, texture, then the other cameras); empty cells 0.',
             'DT-EDNet: 3 × 3 convolutional embedding (128 channels) → squeeze-and-excitation → one kernel transformer block with CBAM and four token transformer blocks (4 heads) → class token, LayerNorm, linear head.',
             'Training: AdamW (6 × 10^{−4}, weight decay 10^{−5}), cosine schedule to 10^{−6}, 300 epochs, batch 32, label smoothing 0.01, gradient clipping 1.2, seed 42; early stopping with patience 60 and minimum improvement 5 × 10^{−5}; keep the model with the highest validation OA.',
             'Configurations on HS (Ma et al. design): OW, VI, TF, OW + VI, OW + TTFI, OW + VI + TTFI; and the DSFs of the 15 sensor sets.',
             'Module ablation of DT-EDNet: without SE, without the dual transformer group, without both.'],
         check=['All networks trained with identical settings; validation curves saved.'],
         out='Network predictions → 2.7, 2.8.',
         papers=[('Ma et al. (2026)', 'Rice blast; DT-EDNet compared with EfficientNet, ResNet18 and ConvNeXt V2 under identical settings (AdamW 6 × 10^{−4}, weight decay 10^{−5}, cosine to 10^{−6} over 300 epochs, batch 32, label smoothing 0.01, clipping 1.2, patience 60, minimum improvement 5 × 10^{−5}); the input feature vector was reshaped into a pseudo-2D representation; the model with the highest validation OA was kept; feature configurations and module ablation compared.', 'Same networks, settings, model selection, configurations and ablation; validation on whole plots (Step D2).')])
    rows = [['Setting', 'Ma et al. (2026)', 'This study'],
            ['Input', 'feature vector reshaped into a pseudo-2D representation', 'k × k pseudo-image of the selected features'], ['Optimiser, schedule', 'AdamW 6 × 10^{−4}, wd 10^{−5}; cosine to 10^{−6}', 'same'],
            ['Epochs, patience', '300; 60 (min. improvement 5 × 10^{−5})', 'same'], ['Batch, smoothing, clipping', '32; 0.01; 1.2', 'same'], ['Validation set', '10% of the training set', '11 of the 33 training plots (whole plots)'],
            ['Model selection', 'highest validation OA', 'same'], ['Tasks', 'severity classes', 'Tasks A and B']]
    tab('dlset', rows=rows, caption='Network settings of Ma et al. (2026) and of this study.', widths=[2200, 3900, 3500], size=16)

    h2('Activity 2.5 – Evaluation on the test plots')
    step('2.7', 'Test metrics', part=P,
         what='Every model is applied once to the 600 test samples; classification and regression metrics are computed.',
         why='The test plots were never used for selection, tuning or early stopping, so their metrics estimate performance on new plots.',
         do=['Tasks A and B: confusion matrix, overall accuracy (OA), Cohen\'s kappa, precision, recall and F1 of each class, macro-averaged recall and F1; Task A also sensitivity, specificity and the area under the ROC curve (AUC).',
             'Task C: R², RMSE and the ratio of performance to deviation RPD = SD/RMSE.',
             'Main metrics: macro-F1 (A, B) and R² (C).'],
         check=['One metric row per model × sensor set × task.'],
         out='Metric table → 2.8–2.10.',
         papers=[('Ma et al. (2026)', 'Rice blast; OA, specificity, precision, recall, F1, kappa, macro-average recall and F1, and per-class precision, recall and F1 on the test set.', 'Same classification metrics.'),
                 ('Liu et al. (2020)', 'Wheat Fusarium head blight; the area under the ROC curve to judge disease detection.', 'AUC for Task A.'),
                 ('Guo et al. (2021); Feng et al. (2022)', 'Wheat yellow rust; wheat powdery mildew: R² and RMSE of disease-index estimation (Feng et al.: R² 0.87 calibration, 0.86 validation for the fused random forest).', 'R² and RMSE for Task C.'),
                 ('Mandal et al. (2023)', 'Rice blast; R², RMSE and RPD of severity models.', 'RPD for Task C.')])
    myfig('evaldemo', 'g12_eval_demo.png', 'Demo of Steps 2.7–2.8 (simulated): (a) confusion matrix of DI classes on the test plots; (b) macro-F1 of sensor sets.')
    demo('metrics_ex', [['', 'Predicted healthy', 'Predicted diseased', 'Metric', 'Value'], ['Observed healthy', '150 (TN)', '30 (FP)', 'OA = (150 + 380)/600', '0.883'], ['Observed diseased', '40 (FN)', '380 (TP)', 'sensitivity = 380/420; specificity = 150/180', '0.905; 0.833'],
                         ['', '', '', 'kappa', '0.73'], ['', '', '', 'macro-F1', '0.86']], 'Worked example of the Task A metrics on 600 test samples', widths=[1800, 1700, 1800, 2700, 1600])

    h2('Activity 2.6 – Comparison, interpretation and covariate baseline')
    step('2.8', 'Comparison of sensor sets and models, ablation and Shapley additive explanations', part=P,
         what='Sensor sets and models are ranked by the main metric; the fusion gain is the difference between a fused set and its best single camera; networks are compared on the HS configurations; DT-EDNet modules are ablated; SHAP shows the features used by the best models.',
         why='Answers which camera or combination is best and why.',
         do=['Rank all model × sensor-set results per task.', 'Fusion gain = metric(fused set) − metric(best single camera in it).', 'Network comparison and DT-EDNet ablation (Step 2.6).', 'SHAP of the best ML model of each task.'],
         check=['Ranking table, fusion-gain table, ablation table, SHAP plots.'],
         out='Best camera / combination → conclusions.',
         papers=[('Feng et al. (2022)', 'Wheat powdery mildew; accuracy of the fused model compared with each single data source; random forest regression was stable in multi-source fusion.', 'Fusion gain over single cameras.'),
                 ('Ma et al. (2026)', 'Rice blast; network comparison on feature configurations, DT-EDNet module ablation and SHAP analysis of features.', 'Same comparison, ablation and SHAP.')])
    step('2.9', 'Covariate baseline: what the cameras add to time, crop and weather', part=P,
         what='Three models are compared on the same 33 training and 15 test plots: M0 uses only the covariates of Step A6 (DAI, variety, sowing date, growth stage, 7-day weather, favourable days); M1 uses only camera features (the best sensor set and model of the task, Step 2.8); M2 uses camera features + covariates with the same model type as M1.',
         why='White rust severity rises with time and depends on weather, variety and stage, so a camera model can look accurate by learning the calendar. As in disease-forecasting studies, the sensors are credited only with what they add to a weather-only model.',
         do=['Build the covariate table for every sample (Step A6); weather windows end the day before each flight (no look-ahead).',
             'M0: random forest on the covariates only, tuned with GroupKFold(3) by plot on the training plots (same grid as Step 2.4).',
             'M1: the best sensor model of the task (Step 2.8), unchanged.',
             'M2: the M1 model type on sensor features + covariates; the covariates are added to the DSF and SFFS and grid search are repeated.',
             'Predict the 15 test plots with M0, M1 and M2; compute all metrics of Step 2.7 (main: macro-F1 for Tasks A, B; R² for Task C).',
             'Gains: ΔS = M1 − M0 (what the cameras add to the covariates) and ΔC = M2 − M1 (what the covariates add to the cameras), per task and, for Task A, per date.',
             'Conclude: the cameras are useful if ΔS > 0; if ΔC > 0, practical models should combine cameras with weather and crop information.'],
         check=['M0, M1, M2 trained on the same plots and folds; no weather from after a flight date.'],
         out='Table of M0, M1, M2 and gains → conclusions; best practical model.',
         alt='In one season, weather has one value per date for all plots, so M0 mostly learns date and crop differences; it is reported as a within-season baseline.',
         q='Why compare with weather? → For wheat powdery mildew, adding remotely sensed data to meteorological data raised forecast accuracy (overall accuracy from about 69% to 78%; Zhang et al., 2014a); the same comparison shows what the UAV cameras add for white rust.',
         papers=[('Zhang et al. (2014a)', 'Wheat powdery mildew at regional scale: a logistic regression forecast from meteorological factors (precipitation, temperature, sun radiation, humidity) compared with one that added two remotely sensed features; overall accuracy rose from 69% to 78%.', 'M0 (covariates only) vs M2 (sensors + covariates), on the same samples.'),
                 ('Bijlwan et al. (2025)', 'Wheat yellow rust and powdery mildew; randomised block design with four sowing dates over two seasons; weekly severity predicted from meteorological variables with ANN and random forest (validation R² 0.93 and 0.90) and regularised regression.', 'A weather-only random forest as M0, in a design with four sowing dates like this one.'),
                 ('Ruan et al. (2022)', 'Wheat stripe rust; random forest on phenology-based Sentinel-2 vegetation indices plus meteorological features (overall accuracy 88.7%, kappa 0.772).', 'Sensor + weather model M2 with a random forest.'),
                 ('Chattopadhyay et al. (2011)', 'White rust of Indian mustard; stepwise regression models on weather forecast crop age at first appearance, peak leaf severity and staghead numbers.', 'Weather is a proven predictor of white rust; M0 uses the same kind of variables.'),
                 ('Bhattacharya and Chattopadhyay (2013)', 'Mustard rot tracked by combining surface meteorology with satellite remote sensing.', 'Weather combined with sensor data for a mustard disease.')])
    demo('covtab', [['Task', 'Main metric', 'M0 covariates', 'M1 sensors', 'M2 sensors + covariates', 'ΔS = M1 − M0', 'ΔC = M2 − M1'],
                    ['A detection', 'macro-F1', '0.71', '0.84', '0.86', '+0.13', '+0.02'], ['B DI class', 'macro-F1', '0.38', '0.52', '0.55', '+0.14', '+0.03'], ['C DI (%)', 'R²', '0.41', '0.63', '0.66', '+0.22', '+0.03']],
         'Output of Step 2.9 on the test plots', widths=[1300, 1200, 1300, 1200, 1800, 1400, 1400])
    myfig('covdemo', 'g13_covariate_demo.png', 'Demo of Step 2.9 (simulated): covariate-only model M0, sensor model M1 and sensor + covariate model M2.')

    h2('Activity 2.7 – Results by stratum, maps and independent testing')
    step('2.10', 'Results by stratum and severity maps', part=P,
         what='Test metrics of the best models are reported by variety, sowing date, growth stage and date; class and DI maps are drawn for every date.',
         why='Shows where the models work and where they fail, and gives the field maps.',
         do=['Macro-F1 and R² by variety, sowing date, stage and date (test plots).', 'Maps of predicted DI class and DI per subplot on the field layout; error maps on test plots.'],
         check=['Strata table; maps for all 10 post-symptomatic dates.'],
         out='Robustness tables and maps → conclusions.',
         papers=[('Liu et al. (2024)', 'Wheat powdery mildew; severity results by growth stage and severity maps from UAV.', 'Results by stage and maps.'),
                 ('Blasch et al. (2023)', 'Wheat rusts; detection by growth stage and variety.', 'Results by stratum.'),
                 ('Abdulridha et al. (2023); Deng et al. (2024)', 'Wheat stem rust; wheat stripe rust: maps of predicted severity from UAV models.', 'Severity maps.')])
    step('2.11', 'Independent testing at Bharatpur', part=P,
         what='The tested IARI models (trained on the 33 training plots) are frozen and applied once to the Bharatpur quadrats processed with the same steps.',
         why='Shows whether the models work at another site under natural infection.',
         do=['Process Bharatpur images with Parts B–C (one ROI per quadrat; IARI scaling constants).', 'Compute the selected features with the IARI wavelengths and formulas.', 'Apply the frozen models; same metrics as Step 2.7, by site type and variety; draw farm maps.'],
         check=['No refitting or tuning on Bharatpur data.'],
         out='Independent test results and farm maps → conclusions.',
         papers=[('Ma et al. (2026)', 'Rice blast; trained models evaluated on an independent 2024 data set from natural infection.', 'Frozen models tested once on independent data.'),
                 ('Yuan et al. (2025)', 'Rice bacterial blight; UAV disease models applied at another scale and area.', 'Transfer of UAV models.'),
                 ('Liu et al. (2026)', 'Wheat powdery mildew; an index developed on the ground applied to UAV images of other fields.', 'Application to new fields.'),
                 ('Poblete et al. (2023)', 'Vascular pathogens (Xylella, Verticillium) in olive and almond; detection with WorldView-2 and -3 satellite imagery compared with airborne hyperspectral and thermal results.', 'Testing whether UAV-level detection holds on other data.')])
