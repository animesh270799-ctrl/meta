from m_lib import *


def add():
    h1('6. Part E – Objective 2: machine-learning and deep-learning models')
    card('E1', 'Model matrix',
         what='Ten model types are trained for each of the three tasks: SVM/SVR, random forest, XGBoost, k-nearest neighbours and PLS-DA/PLSR (machine learning), and DNN-F1, DT-EDNet, EfficientNet-B0, ResNet18 and ConvNeXt V2-Atto (deep learning).',
         why='Comparing classical and deep models on the same features and the same split shows whether the disease signal needs a deep network.',
         papers=L('Ma et al. (2026): DT-EDNet compared with EfficientNet, ResNet18 and ConvNeXt V2 under identical settings for rice blast.',
                  'Tian et al. (2021): LDA, k-NN and SVM wrapped in SFFS for rice leaf blast.',
                  'Mandal et al. (2023): PLS, random forest, MARS and SVM for rice blast severity.',
                  'Chen et al. (2023): SVM and random forest for tobacco virus severity; Gold et al. (2020): PLS-DA for potato late and early blight.'),
         match='The four networks of Ma et al. (2026) and the classical models used in the leaf-level disease studies.',
         mine='15 machine-learning and 15 deep-learning models (5 types × 3 tasks each).',
         out='→ E2–E7.')
    card('E2', 'Feature selection repeated on the training plots',
         what='The whole chain of Part D (D4–D10) is run again on the training plots only; its DSF of each task is the only input of the models.',
         why='Features chosen with the test plots would make the test accuracy optimistic (Ambroise and McLachlan, 2002).',
         papers=L('Ma et al. (2026): feature selection and model training on the 2023 data; testing on the independent 2024 data.',
                  'Mandal et al. (2023): all selection and calibration on the calibration set; validation set kept apart.'),
         match='Selection on the training part only, as in Ma et al. (2026) and Mandal et al. (2023).',
         mine='Same settings as D4–D10 on the %d training leaves; index values of the test leaves are computed with the wavelengths chosen on TRAIN.' % CNT['train'],
         out='DSF of Tasks A, B, C (training plots) → E3–E7.')
    card('E3', 'Scaling and class weights',
         what='Features are standardised with the mean and SD of the fitting part (inside each inner fold, then of all training plots for the final model). Classifiers use balanced class weights.',
         why='Scale-sensitive models (SVM, k-NN, PLS, networks) need comparable features; class weights stop the model from ignoring grade 9.',
         papers=L('Lv et al. (2023): standardised inputs and balanced classes for SVM.',
                  'Ma et al. (2026): cross-entropy loss with label smoothing 0.01 for the networks; the same smoothing is used here, with class weights added because the grades are unequal.'),
         match='Standardisation and balancing as in Lv et al. (2023).',
         mine='scikit-learn Pipeline(StandardScaler, model); class_weight = balanced (XGBoost: balanced sample weights); networks: inverse-frequency class weights in the cross-entropy loss.',
         out='→ E4, E5, E6.')
    card('E4', 'Sequential floating forward selection (SFFS)',
         what='For each machine-learning model, SFFS adds the feature that most improves the mean inner-fold score and after each addition tries to remove one; the best subset of every size up to 15 is recorded, and the smallest subset within 1% of the best inner score is kept.',
         why='Each model may need a different, smaller subset of the DSF; a wrapper choice gives the optimal feature combination for that model.',
         papers=L('Tian et al. (2021): SFFS wrapped around LDA, k-NN and SVM found optimal feature combinations of 2–4 features for rice leaf blast; SVM-SFFS was best.',
                  'Lv et al. (2023): SFFS with the SVM macro-F1 as criterion after RELIEF-F and VIF for southern corn leaf blight.'),
         match='SFFS as in Tian et al. (2021) with the macro-F1 criterion of Lv et al. (2023); the 1% rule follows the one-standard-error idea of Hastie et al. (2009).',
         mine='mlxtend SFFS; criterion macro-F1 (A, B) or negative RMSE (C); inner GroupKFold(3) by plot.',
         out='Feature subset of each model → E5.',
         q='Why the smallest subset within 1%? → Neighbouring subset sizes differ by less than their noise; the smaller subset generalises better.')
    rows = [['Model', 'Principle', 'Grid searched (inner GroupKFold(3))', 'Disease papers that used it'],
            ['SVM / SVR', 'maximum-margin boundary, RBF kernel', 'C ∈ {0.1, 1, 10, 100}; γ ∈ {0.001, 0.01, 0.1, scale}; ε ∈ {0.1, 0.5} (SVR)', 'Tian et al. (2021); Lv et al. (2023); Chen et al. (2023); Mandal et al. (2023)'],
            ['Random forest', 'ensemble of decorrelated trees', '500 trees; max_features ∈ {sqrt, 0.3}; min_samples_leaf ∈ {1, 3, 5}', 'Chen et al. (2023); Mandal et al. (2023); Selvaprakash et al. (2026)'],
            ['XGBoost', 'gradient-boosted trees', 'trees ∈ {200, 500}; depth ∈ {3, 5}; learning rate ∈ {0.05, 0.1}', 'Ma et al. (2026) (ensemble model inside SHAP-CARS)'],
            ['k-NN', 'label of the nearest training leaves', 'k ∈ {3, 5, 7, 9, 11}; uniform or distance weights', 'Tian et al. (2021)'],
            ['PLS-DA / PLSR', 'latent components maximising covariance', '1–15 components', 'Zhang et al. (2012); Gold et al. (2020); Wang et al. (2016); Mandal et al. (2023)']]
    tab('mlgrid', rows=rows, caption='Machine-learning models, tuning grids and the disease studies that used them.', widths=[1400, 2100, 3300, 2800], size=15)
    card('E5', 'Grid search and final fit of the machine-learning models',
         what='On the SFFS subset, the grid of each model is searched with the same inner folds; the best setting is refitted on all training plots and predicts the test leaves once.',
         why='Hyper-parameters are chosen without the test plots; the refitted model is the delivered model.',
         papers=L('Tian et al. (2021): SVM C and γ chosen by grid search for each comparison.',
                  'Lv et al. (2023): SVM C and γ by grid search with cross-validation.'),
         match='Grid search inside the training part as in Tian et al. (2021) and Lv et al. (2023), by plot.',
         mine='scikit-learn GridSearchCV; seeds 42.',
         out='15 machine-learning models and their test predictions → F.')
    card('E6', 'Deep-learning models',
         what='DNN-F1 (dense network on the feature vector) and four image networks fed with a k × k pseudo-image of the DSF: DT-EDNet, EfficientNet-B0, ResNet18, ConvNeXt V2-Atto.',
         why='DT-EDNet is the network of the core reference paper; the three others are its comparison networks.',
         papers=L('Ma et al. (2026): DT-EDNet – 3 × 3 convolutional embedding (128 channels) → squeeze-and-excitation → dual transformer group (one kernel transformer block with CBAM and four token transformer blocks, 4 attention heads) → class token, LayerNorm, linear head; the input spectral vector was reshaped into a pseudo-2D representation; AdamW (learning rate 6 × 10^{−4}, weight decay 10^{−5}), cosine schedule to 10^{−6} over 300 epochs, batch 32, label smoothing 0.01, gradient clipping 1.2, dropout 0.03, seed 42, early stopping with patience 60 and minimum improvement 5 × 10^{−5}; the model with the best validation accuracy was kept; all comparison networks used identical settings.',
                  'Sharma et al. (2019): DeepInsight – turning non-image data into images for convolutional networks.'),
         match='Architecture and optimiser settings exactly as Ma et al. (2026). Adapted: at most 100 epochs with patience 20 (the same patience-to-epochs ratio of 0.2 as 60/300), validation on 11 training plots, model selection by validation macro-F1 (A, B) or RMSE (C) because the classes are unequal; stride-1 stems so the small pseudo-image is not reduced away.',
         mine='Pseudo-image side k = max(3, ⌈√p⌉) for p features, unused cells zero; PyTorch; fit on %d leaves of 22 plots, early stopping on %d leaves of 11 plots; the best-epoch network is the delivered model.' % (CNT['dlfit'], CNT['dlval']),
         out='15 networks and their test predictions → F.',
         alt='300 epochs with patience 60 on CPU is not practical for 15 networks plus configurations and ablation; the shorter schedule keeps the same ratio.',
         q='Is a 4 × 4 pseudo-image meaningful? → It is an arrangement of features, not a picture (Sharma et al., 2019); this is tested directly by comparing with DNN-F1 and the machine-learning models.')
    rows = [['Setting', 'Ma et al. (2026)', 'This study', 'Reason'],
            ['Input', 'input feature vector reshaped into a pseudo-2D representation', 'k × k pseudo-image of the DSF', 'no texture for single leaves; wavelet features take that role'],
            ['Embedding, attention', '3 × 3 conv, 128 channels; SE; 1 KTB with CBAM + 4 TTB; 4 heads', 'same', '–'],
            ['Optimiser and schedule', 'AdamW 6 × 10^{−4}, weight decay 10^{−5}; cosine to 10^{−6}', 'same', '–'],
            ['Batch, smoothing, clipping, dropout', '32; 0.01; 1.2; 0.03', 'same', '–'],
            ['Epochs, patience', '300; 60 (min. improvement 5 × 10^{−5})', '100; 20 (same minimum improvement)', 'CPU training; same patience/epochs ratio'],
            ['Validation set', '10% of the training set', '11 of 33 training plots', 'whole plots (leakage rule B3)'],
            ['Model selection', 'highest validation OA', 'highest validation macro-F1 (A, B) / lowest RMSE (C)', 'unequal classes; regression task'],
            ['Seed', '42', '42', '–']]
    tab('dlsettings', rows=rows, caption='Deep-learning settings of Ma et al. (2026) and of this study.', widths=[1900, 3000, 2500, 2200], size=15)
    card('E7', 'Feature configurations and DT-EDNet ablation',
         what='On Task B, the four image networks are trained on four inputs (OW, VI, WF and DSF); DT-EDNet is also trained without the squeeze-and-excitation block, without the dual transformer group, and without both.',
         why='Shows which feature family the networks use best and whether each DT-EDNet module contributes.',
         papers=L('Ma et al. (2026): compared feature configurations (spectral bands, vegetation indices, texture indices and their fusion) and removed DT-EDNet modules one at a time.'),
         match='Same comparison and ablation as Ma et al. (2026), with wavelet features in place of texture.',
         mine='Settings of E6; evaluation on TEST.',
         out='Configuration and ablation tables → discussion.')
