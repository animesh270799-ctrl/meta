from dsl import *
from x1_intro import stage_head


def add():
    # ---------------------------------------------------------------- chapter 9
    h1('9. Stage 8 – Objective 2: building the 15 sensor sets')
    stage_head('Stage 7 (DSF of each camera and task).', 'the models (Stages 9–10).', '33 training plots only (1320 subplot-dates).')
    box('In short', 'Each of the 15 camera combinations gets one input table: the DSFs of its cameras are joined side by side (feature-level fusion) and VIF < 10 is applied again. No new feature selection is done, because the DSFs were already chosen on the training plots.', kind='key')
    p('The four cameras and all their combinations are modelled, so the best camera and the best combination can be found on the same plots ({T:sets}). Maimaitijiang et al. (2020) also modelled every single UAV sensor and every combination, and Mahlein et al. (2019) compared each sensor and every combination of thermal, fluorescence and hyperspectral data.')
    rows = [['Type', 'Sensor sets', 'Number'],
            ['Single cameras', 'S1 HS, S2 MS, S3 RGB, S4 TIR', '4'],
            ['Pairs', 'S5 HS+MS, S6 HS+RGB, S7 HS+TIR, S8 MS+RGB, S9 MS+TIR, S10 RGB+TIR', '6'],
            ['Triplets', 'S11 HS+MS+RGB, S12 HS+MS+TIR, S13 HS+RGB+TIR, S14 MS+RGB+TIR', '4'],
            ['All four', 'S15 HS+MS+RGB+TIR', '1']]
    tab('sets', rows=rows, caption='The 15 sensor sets.', widths=[1700, 6800, 1100], size=16)
    p('For each sensor set and task, in this order (2.2):')
    nl('Take the DSF of each camera of the set for the task (Step 7.11).',
       'Join them by subplot code and date (feature-level fusion by concatenation; Feng et al., 2022; Liu et al., 2024).',
       'Joining cameras creates new collinearity (for example NDRE of the MS camera and a red-edge band of the HS camera), so the largest-VIF feature is removed until all VIF < 10, on the training plots (Mustafa et al., 2023).',
       'Compute the same features for the test samples with the wavelengths and formulas fixed on the training plots.')
    p('This gives 15 sets × 3 tasks = **45 input tables**. Single-camera sets are simply the DSF of that camera.')

    # ---------------------------------------------------------------- chapter 10
    h1('10. Stage 9 – Machine-learning models: SFFS, grid search and the final fit')
    stage_head('Stage 8 (45 input tables).', 'the test (Stage 11).', 'the 33 training plots, divided into the three GroupKFold(3) rounds; the final fit uses all 33 training plots.')
    box('In short', 'For every model, sensor set and task: (1) SFFS chooses the best feature subset (at most 15) by the GroupKFold(3) score; (2) a grid search tunes the model settings on that subset with the same folds; (3) the best model is refitted on all 33 training plots and frozen.', kind='key')
    h2('10.1 The four models')
    rows = [['Model', 'Idea', 'Tasks A, B', 'Task C', 'References'],
            ['SVM / SVR (RBF kernel)', 'finds the boundary (or tube) with the largest margin between classes in a transformed space', 'SVM', 'SVR', 'Cortes and Vapnik (1995); Tian et al. (2021); Lv et al. (2023)'],
            ['Random forest', 'many decision trees on bootstrap samples; majority vote or mean', 'classifier', 'regressor', 'Breiman (2001); Abdulridha et al. (2023)'],
            ['k-nearest neighbours', 'label of the k most similar training samples', 'classifier', 'regressor', 'Tian et al. (2021); Mustafa et al. (2023)'],
            ['PLS-DA / PLSR', 'few latent components that explain both features and target', 'PLS-DA', 'PLSR', 'Wold et al. (2001); Zhang et al. (2012); Krishna et al. (2014)']]
    tab('models', rows=rows, caption='The four machine-learning models.', widths=[1800, 3200, 1100, 1100, 2400], size=15)
    h2('10.2 The order inside one model')
    h3('Step 9.1 – Sequential floating forward selection (2.3)')
    p('SFFS (Pudil et al., 1994) builds the feature subset step by step ({F:sffs}):')
    nl('Start with no feature. Add the feature that gives the best GroupKFold(3) score.',
       'After each addition, try removing each feature already chosen; if a removal improves the score, remove it ("floating").',
       'Continue until 15 features; record the best subset of each size and keep the subset with the best score.')
    p('The score is macro-F1 for Tasks A and B and the negative RMSE for Task C, always as the mean of the three GroupKFold rounds. During SFFS each model uses its default settings (scikit-learn: SVM C = 1, γ = scale; random forest 500 trees; k-NN k = 5; PLS 2 components; Pedregosa et al., 2011), and the scaler sits inside the pipeline, so it is refitted in every round. The implementation is SequentialFeatureSelector of mlxtend with floating = True (Raschka, 2018), the tool used by Mustafa et al. (2023). '
      'Tian et al. (2021) wrapped SFFS around LDA, k-NN and SVM and found that 2–4 features were enough; Lv et al. (2023) used Relief-F followed by SFFS; Shafiee et al. (2021) wrapped sequential forward selection around SVR.')
    myfig('sffs', 'x06_sffs.png', 'Demo of SFFS: (a) score at each step – features are added, and one is removed when that improves the score; (b) selection frequency of each feature over 100 repeated runs (stability check of the best model).')
    p('**Stability check.** For the best model of each task (chosen in Stage 12), SFFS is repeated over 100 random GroupKFold(3) divisions of the training plots, and the percentage of runs that select each feature is reported, as Tian et al. (2021) repeated their cross-validation 100 times and kept the most frequent combination.')
    h3('Step 9.2 – Grid search (2.4)')
    p('With the SFFS subset fixed, every combination of the settings in {T:grid} is scored with the same GroupKFold(3) rounds, and the best combination is kept. Tian et al. (2021) tuned C and γ of the SVM by grid search; Chen et al. (2023) and Bijlwan et al. (2025) tuned their models by grid search inside the training set only.')
    rows = [['Model', 'Settings searched', 'Combinations'],
            ['SVM / SVR', 'C ∈ {0.1, 1, 10, 100}; γ ∈ {0.001, 0.01, 0.1, scale}; ε ∈ {0.1, 0.5} (SVR only); class_weight = balanced', '16 (SVR 32)'],
            ['Random forest', '500 trees; max_features ∈ {sqrt, 0.3}; min_samples_leaf ∈ {1, 3, 5}; class_weight = balanced', '6'],
            ['k-NN', 'k ∈ {3, 5, 7, 9, 11}; uniform or distance weights', '10'],
            ['PLS-DA / PLSR', '1–15 components (at most the number of features)', '≤ 15']]
    tab('grid', rows=rows, caption='Tuning grids of the machine-learning models.', widths=[1700, 6400, 1500], size=15)
    h3('Step 9.3 – Final fit and freezing')
    p('The pipeline (scaler + model) with the SFFS subset and the best settings is refitted on **all 33 training plots** and saved with its subset, settings and scaling constants. Nothing is changed after this point. With 4 models × 15 sensor sets × 3 tasks, **180 machine-learning models** are frozen.')
    box('Worked example', 'Random forest, sensor set S7 (HS + TIR), Task B: the joined DSF has 18 features; SFFS keeps 7 (WRI, FD_{716}, PC2-Con, TTFI, PSRI, NRCT, ΔT) with an inner macro-F1 of 0.61; the grid chooses max_features = sqrt and min_samples_leaf = 3 (inner macro-F1 0.63); the model is refitted on the 1320 training samples and frozen.', kind='note')

    # ---------------------------------------------------------------- chapter 11
    h1('11. Stage 10 – Neural networks')
    stage_head('Stage 8 (input tables).', 'the test (Stage 11).', 'weights fitted on the 22 fitting plots (880 subplot-dates); early stopping and model choice on the 11 validation plots (440); test plots not used.')
    box('In short', 'Two feature-fusion networks (DNN-F1, DNN-F2) use the same inputs as the machine-learning models; four pseudo-image networks (DT-EDNet and its three comparison networks) classify the features arranged as a small image. All are trained with the same settings and stopped on the 11 validation plots.', kind='key')
    h2('11.1 DNN-F1 and DNN-F2 (2.5)')
    nl('**DNN-F1 (input-level fusion):** the joined feature vector of a sensor set enters one network – two hidden layers of 64 and 32 units with batch normalisation, ReLU and dropout 0.3, then a softmax (Tasks A, B) or linear (Task C) output. Used for all 15 sensor sets.',
       '**DNN-F2 (intermediate-level fusion):** each camera has its own branch (dense layer of 32 units, batch normalisation, ReLU, dropout 0.3) on that camera\'s features; a squeeze-and-excitation layer learns one weight per camera (Hu et al., 2018); the weighted branch outputs are joined and passed to a dense layer of 32 units and the output layer. Used for the 11 sensor sets with two or more cameras.',
       'Inputs are z-scored with the 22 fitting plots; training with AdamW and the schedule of {T:dlset}; the epoch with the best validation score is kept; the learned camera weights of DNN-F2 are recorded.')
    p('The two fusion levels are those of Maimaitijiang et al. (2020), who found that DNN-F2 consistently beat DNN-F1 and used it only for sensor combinations. For disease, Deng et al. (2024) gave each UAV modality its own encoder joined by cross-attention to estimate the wheat stripe rust DI, and Yu et al. (2025) joined two branches with attention for rice sheath blight; the squeeze-and-excitation block is the one inside DT-EDNet (Ma et al., 2026).')
    h2('11.2 Pseudo-image networks (2.6)')
    p('For Tasks A and B the selected features are arranged as a k × k pseudo-image, with k = ⌈√p⌉ (at least 3) for p features, features in group order (OW, VI, texture, then the other cameras) and empty cells set to 0 – for example 22 features give a 5 × 5 image. Four networks classify it with identical settings ({T:dlset}): **DT-EDNet** (3 × 3 convolutional embedding with 128 channels → squeeze-and-excitation → one kernel transformer block with CBAM and four token transformer blocks with 4 heads → class token, LayerNorm, linear head; Ma et al., 2026), **EfficientNet-B0** (Tan and Le, 2019), **ResNet18** (He et al., 2016) and **ConvNeXt V2-Atto** (Woo et al., 2023).')
    rows = [['Setting', 'Ma et al. (2026)', 'This study'],
            ['Input', 'feature vector reshaped into a pseudo-2D representation', 'k × k pseudo-image of the selected features'],
            ['Optimiser, schedule', 'AdamW 6 × 10^{−4}, weight decay 10^{−5}; cosine to 10^{−6} (Loshchilov and Hutter, 2017, 2019)', 'same'],
            ['Epochs, patience', '300; 60 (minimum improvement 5 × 10^{−5})', 'same'],
            ['Batch, label smoothing, gradient clipping', '32; 0.01; 1.2', 'same; seed 42'],
            ['Validation data', '10% of the training samples', '11 of the 33 training plots (whole plots)'],
            ['Model kept', 'highest validation overall accuracy', 'same'],
            ['Comparisons', 'feature configurations; module ablation', 'HS configurations OW, VI, TF, OW + VI, OW + TTFI, OW + VI + TTFI; DT-EDNet without SE, without the transformer group, without both; all 15 sensor sets']]
    tab('dlset', rows=rows, caption='Training settings of the networks.', widths=[2300, 3900, 3400], size=15)
    p('Machine-learning models use GroupKFold(3), but networks need one fixed validation set to decide when to stop, so the 11 validation plots are used for them; both stay inside the training plots.')

    # ---------------------------------------------------------------- chapter 12
    h1('12. Stages 11–12 – Testing once, then comparing and interpreting')
    stage_head('Stages 9–10 (all models frozen).', 'the answers of Objective 2.', '15 test plots: 600 subplot-dates per camera, predicted once.')
    box('In short', 'Every frozen model predicts the 600 test samples once. Metrics are computed, sensor sets and models are ranked, the gain of fusion and of each camera is measured, the cameras are compared with a covariate-only model, and maps are drawn.', kind='key')
    h2('12.1 Test metrics (2.7)')
    p('From the confusion matrix of the test samples (TP, TN, FP, FN for Task A) the following metrics are computed (Ma et al., 2026; Sokolova and Lapalme, 2009):')
    rows = [['Metric', 'Formula or meaning', 'Task'],
            ['Overall accuracy (OA)', '(TP + TN) / all samples; for classes: correct / all', 'A, B'],
            ["Cohen's kappa", '(OA − chance agreement) / (1 − chance agreement) (Cohen, 1960)', 'A, B'],
            ['Precision, recall, F1 of each class', 'precision = TP/(TP + FP); recall = TP/(TP + FN); F1 = 2PR/(P + R)', 'A, B'],
            ['Macro-F1 (main metric)', 'mean F1 of the classes, each class counted equally', 'A, B'],
            ['Accuracy within one class', 'share of predictions at most one DI class from the observed class (Cross et al., 2024)', 'B'],
            ['Quadratic weighted kappa', 'kappa with larger penalties for predictions further from the true class (Cohen, 1968)', 'B'],
            ['Sensitivity, specificity, AUC', 'recall of diseased, recall of healthy; area under the ROC curve (Fawcett, 2006)', 'A'],
            ['R² (main metric), RMSE', '1 − Σ(y − ŷ)^{2}/Σ(y − ȳ)^{2}; √[Σ(y − ŷ)^{2}/n]', 'C'],
            ['RPD', 'SD of the observed DI / RMSE (Mandal et al., 2023)', 'C'],
            ['Low-severity check', 'Task A recall for DI ≤ 5; Task C RMSE for DI ≤ 10 (Abdulridha et al., 2023; Deng et al., 2024)', 'A, C']]
    tab('metrics', rows=rows, caption='Test metrics.', widths=[2600, 5700, 1300], size=15)
    box('Worked example', ['Task A on 600 test samples: 150 healthy predicted healthy (TN), 30 healthy predicted diseased (FP), 40 diseased predicted healthy (FN), 380 diseased predicted diseased (TP).',
                           'OA = (150 + 380)/600 = 0.883; sensitivity = 380/420 = 0.905; specificity = 150/180 = 0.833; kappa = 0.73; macro-F1 = 0.86.'], kind='note')
    myfig('eval', 'g12_eval_demo.png', 'Demo of the test output: (a) confusion matrix of DI classes, (b) macro-F1 of sensor sets.')
    h2('12.2 Comparison, ablation and SHAP (2.8)')
    nl('**Ranking:** all model × sensor-set results are ranked per task by the main metric.',
       '**Fusion gain** = metric of a fused set − metric of the best single camera in it (Feng et al., 2022; Deng et al., 2024, whose three-modality model beat single and two-modality models).',
       '**Drop-one-camera ablation:** for the four-camera set S15, each camera is removed in turn and the loss of accuracy recorded; it is compared with the DNN-F2 camera weights. Mahlein et al. (2019) found that two sensors could beat three, so more cameras are not assumed to be better.',
       '**Network comparison and DT-EDNet ablation** on the HS configurations (Ma et al., 2026).',
       '**SHAP** of the best machine-learning model of each task shows which features it uses (Lundberg and Lee, 2017; Ma et al., 2026).')
    h2('12.3 Covariate baseline (2.9)')
    p('Severity rises with time and depends on weather, variety and stage, so a camera model could look accurate by learning the calendar. Three models are compared on the same training and test plots:')
    rows = [['Model', 'Inputs', 'How it is built'],
            ['M0 – covariates only', 'DAI, variety, sowing date, growth stage, 7-day weather, favourable days', 'random forest; numeric covariates z-scored, variety and sowing date one-hot; tuned by GroupKFold(3) with the grid of {T:grid}'],
            ['M1 – sensors only', 'features of the best sensor set', 'the best model of the task from Step 12.2, unchanged'],
            ['M2 – sensors + covariates', 'DSF + covariates', 'same model type as M1; SFFS and grid search repeated']]
    tab('cov', rows=rows, caption='Models of the covariate baseline.', widths=[2200, 3200, 4200], size=15)
    eq('ΔS = metric(M1) − metric(M0)  (what the cameras add)     ΔC = metric(M2) − metric(M1)  (what the covariates add)')
    p('Weather windows end the day before each flight, so no future weather is used. For wheat powdery mildew, adding remotely sensed features to a weather model raised forecast accuracy from 69% to 78% (Zhang et al., 2014a); weather-only machine-learning models predicted wheat disease severity well (Bijlwan et al., 2025); a random forest on satellite indices plus weather mapped wheat stripe rust (Ruan et al., 2022); and weather predicts white rust (Chattopadhyay et al., 2011). In one season weather has one value per date for all plots, so M0 is a within-season baseline.')
    myfig('covdemo', 'g13_covariate_demo.png', 'Demo of the covariate baseline: M0, M1 and M2 on the test plots.')
    h2('12.4 Results by stratum, maps and the Bharatpur test (2.10–2.11)')
    nl('Test metrics of the best models are reported by variety, sowing date, growth stage and date (Blasch et al., 2023; Liu et al., 2024).',
       'Predicted DI class and DI are drawn for every subplot on the field layout for every date; error maps are drawn for the test plots (Deng et al., 2024, estimated the DI of every UAV pixel).',
       'The frozen models are applied once to the Bharatpur quadrats processed with Stages 1–2 and the IARI scaling constants; no refitting or tuning is done there (Ma et al., 2026, tested on an independent year).')
    box('On a new data set', 'For testing frozen models, Stage 11 is the only modelling step: compute the frozen features, apply the frozen pipelines, and compute the same metrics. For a new season analysed on its own, Stages 8–12 are repeated with its own training and test plots.', kind='present')
