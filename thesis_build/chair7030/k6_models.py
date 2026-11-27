from k0_lib import *


def add():
    h1('5. Step 8: feature selection on the training plots')
    p('Step 8 is where the analysis starts to learn for the models. It repeats the whole Objective 1 selection chain of Step 7, but only on the 1631 leaves of the 33 training plots. '
      'Its output – one feature set per task – is the only input the models of Steps 9 and 10 receive. Because the test plots were not used, the selection cannot have been '
      'influenced by them. Choosing features on all data and then testing on part of the same data is a well-known source of optimistic accuracy (Ambroise and McLachlan, 2002).')
    card('card8', '8', 'Feature selection repeated on the training plots (Step 2.1.2)',
         'Choose the model inputs (optimal wavelengths, indices and the disease-specific set per task) without looking at the test plots.',
         'TRAIN: 1631 leaves of 33 plots. TEST is not read. (The index VALUES of the test leaves are later computed with the wavelengths chosen here.)',
         '5-nm R and FD bands; 44 published index features; grade, diseased flag and plot of the training leaves.',
         steps('NDSI and RSI R² maps on the training leaves; effective ranges by the top-5% rule (threshold R² ≥ 0.223; 260 bands).',
               'Candidate bands: R and FD inside the effective ranges plus FD 680–760 nm.',
               'SHAP-CARS: XGBoost SHAP top 40% → standardise → MCCV (50 random 80/20 splits of the training leaves) for the PLS components → CARS 50 iterations × 20 runs (seed 42) → bands in ≥ 50% of runs, max 15 = OW.',
               'Best NDSI and RSI pair and the WRI search on the training leaves; add NDSI_best, RSI_best, WRI to the 44 index features (47).',
               'Redundancy filter |r| ≥ 0.95 on the training leaves → 23 index features kept.',
               'ReliefF (detection with 2 classes, six grades) and RReliefF (score), k = 10, neighbours from the same plot excluded → top 5 indices per task = VI.',
               'For each task pool OW (15) + VI (5) and remove the largest VIF until all VIF < 10 → DSF of that task.'),
         'Same settings as Step 7. MCCV and the CARS cross-validation divide the training leaves at random (by leaf); this influences only which bands are kept, never the test set.',
         'fold_selection.json (OW, VI, DSF per task, NDSI/RSI/WRI wavelengths) and fold0_indices.csv (index values of all leaves with the training wavelengths) → Steps 9, 10, 12, 14.',
         'a3_select.py; alib.py.',
         'Ambroise and McLachlan (2002); Varma and Simon (2006); Ma et al. (2026); Li et al. (2009); Robnik-Šikonja and Kononenko (2003).',
         '35; appendix 103',
         'Run unchanged after Step 5. Never feed the Step 7 (all-leaf) features to the models.')
    rows = [['Item', 'Result on the 70:30 training plots'],
            ['Effective ranges', 'no pair reached R² 0.5 → top 5% of pairs (R² ≥ 0.223); 260 bands'],
            ['Optimal wavelengths (15)', 'FD550, FD565, FD595, FD760, FD860, FD870, FD985, FD1060, FD1075, FD1090, FD1185, FD1245, FD1350, FD1660, FD1810 – all first-derivative bands'],
            ['Best NDSI / RSI', '(795, 805) nm for both'],
            ['White Rust Index', 'NDSI(780, 830) with third-band weight w = 0 (r = −0.59): the third band did not improve the two-band index'],
            ['Index features after |r| filter', '23 of 47'],
            ['VI detection (ReliefF)', 'HI, RSI_best, REP, RVSI, DWSI-2'],
            ['VI six grades (ReliefF)', 'REP, HI, RSI_best, RVSI, PSSRb'],
            ['VI score (RReliefF)', 'RSI_best, HI, MCARI, Dr, DWSI-2'],
            ['DSF detection (11)', 'FD550, FD595, FD1810, FD1245, FD760, FD1060, FD1075, FD860, FD985, REP, DWSI-2'],
            ['DSF six grades (11)', 'FD550, FD595, FD1810, FD1245, FD760, FD1060, FD1075, FD860, FD985, REP, PSSRb'],
            ['DSF score (12)', 'FD550, FD1810, FD1245, FD760, FD1060, FD1075, FD860, FD985, HI, MCARI, Dr, DWSI-2']]
    tab('step8res', rows=rows, caption='Results of Step 8 on the 1631 training leaves (from fold_selection.json). These are the inputs of all models.', widths=[2600, 7000], size=17, boldfirst=True)
    read(shows='Every intermediate result of the selection chain on the training plots.',
         how='Read from top to bottom: each row is the input of the next. The last three rows are the model inputs.',
         found='VIF removed FD565, FD870, FD1090, FD1185, FD1350, FD1660 and the redundant indices (HI, RSI_best, RVSI for six grades), leaving 11–12 features per task. Eight derivative bands are common to all three tasks.',
         means='The model inputs are compact (11–12 numbers per leaf) and cover the green peak (550–595 nm), the red edge and NIR shoulder (760–985 nm), the NIR (1060–1075 nm) and the water-band edges (1245, 1810 nm).',
         say='"Repeated on the training plots only, the selection gave 11–12 features per task, mainly derivative bands plus REP and one or two indices."')
    tab('foldsel', 26, widths=[1500, 2300, 1300, 1000, 1200, 1200, 1100], size=14)
    read(shows='The selection on the 70:30 training plots (first row) next to the selections in the three LORO training parts.',
         how='Each row is one training set; columns give the optimal wavelengths, the best two-band pair, the WRI and the three disease-specific sets.',
         found='All four training sets found the same best pair (795, 805) nm and almost the same WRI; the optimal wavelengths and DSF differ in individual bands but lie in the same regions.',
         means='The 70:30 split did not discover a different signal; it chose neighbouring bands of the same spectral features. This supports comparing the two designs (Step 15).',
         say='"Every training set picked the same regions of the spectrum; only neighbouring bands change."')
    fig('stab', 'f29_stability.png', 'Number of training sets (of four: the 70:30 training plots and the three LORO training parts) in which each optimal wavelength was selected.', rep=19)
    read(shows='How often each optimal wavelength was chosen across four training sets.',
         how='Bar height = number of training sets (of four) that selected the band; all bars are red because every chosen band is a first-derivative band; a black dot marks the 15 bands of the 70:30 training set.',
         found='33 different bands were chosen in total; FD760, FD1060, FD1090 and FD1245 in all four. 11 of the 15 bands of the 70:30 set were also chosen in at least one LORO part.',
         means='Neighbouring derivative bands are almost interchangeable, so the exact band varies with the training leaves while the region is stable. For sensor design the regions matter, not the single band.',
         say='"The exact bands vary a little with the training leaves, but the same four bands appear every time."')

    # ---------------------------------------------------------------- Step 9
    h1('6. Steps 9–10: training the models inside the training plots')
    h2('6.1 Step 9 – Machine-learning models')
    card('card9', '9', 'Machine-learning models: SFFS, grid search and refit (Activity 2.2)',
         'For each task and each of five methods, choose a feature subset and settings, fit the model and predict the test leaves once.',
         'TRAIN for everything that is chosen or fitted; inner GroupKFold(3) of the 33 training plots for the choices; TEST only for the final prediction.',
         'DSF of the task from Step 8 (11 or 12 features); labels A (0/1), B (0–5) or C (0–9).',
         steps('Standardise: mean and SD of each feature from the 1631 training leaves; apply the same numbers to training and test leaves.',
               'Inner folds: GroupKFold(3) by plot on the training leaves (11 plots scored each time; 546/542/543 leaves).',
               'SFFS (sequential floating forward selection): start empty, add the feature that most improves the mean inner score, after each addition try to remove one; record the best subset of every size up to 15.',
               'Take the SMALLEST subset whose inner score is within 1% of the best inner score.',
               'Grid search (GridSearchCV) on that subset with the same three inner folds.',
               'Refit the best setting on all 1631 training leaves (class weights balanced; XGBoost with balanced sample weights).',
               'Predict the 699 test leaves once (class or score; probability or decision value for AUC).',
               'Save model, feature list, scaler and settings (joblib).'),
         'Scoring: macro-F1 (A, B), negative RMSE (C). Starting settings during SFFS: SVM C 10, γ scale; RF 100 trees; XGBoost 100 trees, depth 4, rate 0.1; k-NN k 7, distance; PLS min(5, p) components. Grids: report Table 18.',
         '15 models (5 methods × 3 tasks) and their 699 test predictions → Step 11; the same model files → Step 16.',
         'a3_ml.py, a3_ml_models.py → ml_models/*.joblib, ml_predictions.csv, ml_selection.csv.',
         'Pudil et al. (1994); Raschka (2018); Pedregosa et al. (2011); Varma and Simon (2006); Cawley and Talbot (2010).',
         '16, 37; appendix 95, 104',
         'Run unchanged. With fewer than about 15 training plots use GroupKFold(2) or leave-one-plot-out inner folds.')
    tab('mlmodels', 18, widths=[1500, 3100, 3300, 1700], size=17)
    read(shows='The five machine-learning methods, their principle, the grid of settings searched and the original reference.',
         found='SVM/SVR (C, γ, ε), random forest (500 trees; max_features, min_samples_leaf), XGBoost (trees, depth, learning rate), k-NN (k, weights) and PLS-DA/PLSR (1–15 components).',
         means='The methods range from linear (PLS) to strongly non-linear (SVM, tree ensembles, k-NN), so the comparison shows whether the white rust signal needs non-linear models.',
         say='"Five classical methods, each tuned on the training plots with a small grid."')
    box('Why the smallest subset within 1%?', 'Inner scores of neighbouring subset sizes differ by less than their own noise. Taking the smallest subset that is practically as good as the best '
        'reduces over-fitting and keeps the model simple – the same idea as the "one-standard-error rule" (Hastie et al., 2009).', kind='method')
    tab('sffs', 27, widths=[700, 1100, 1300, 1400, 1300, 3800], size=16)
    read(shows='For each task and model: candidate features, features kept by SFFS, inner score and the settings chosen by the grid search.',
         how='Inner score = mean over the three inner folds of the training plots: macro-F1 for A and B, negative RMSE (in grades) for C, so −1.93 means RMSE 1.93.',
         found=['Models kept 4–9 of the 11–12 candidates. Inner macro-F1: detection 0.75–0.85, six grades 0.25–0.40; inner RMSE 1.93–2.11.',
                'Most often chosen across models: FD860, FD1060, FD1810, FD1245, FD1075.'],
         means='The inner scores are close to the later test scores (e.g. SVM detection 0.853 inner vs 0.826 test; RF score RMSE 1.93 vs 1.92), which shows that the inner folds gave a realistic picture and the test set was not unusually easy or hard.',
         say='"Each model chose its own small subset of 4–9 features inside the training plots."')
    box('A small detail an examiner may ask about.', 'The scaler (mean and SD) was computed once from all 1631 training leaves and then used inside the inner folds. Strictly, the inner '
        'validation plots therefore contributed to the scaling of their own inner round. This can make the inner scores very slightly optimistic, but it cannot affect the test result, '
        'because the test leaves were not part of the scaler. A pipeline object (scaler inside each inner fold) would remove even this small effect.', kind='note')

    # ---------------------------------------------------------------- Step 10
    h2('6.2 Step 10 – Deep-learning models')
    card('card10', '10', 'Deep-learning models with early stopping (Activity 2.3)',
         'Train one dense network and four image networks per task and predict the test leaves once.',
         'DL-FIT: 22 training plots (1090 leaves) to fit the weights; DL-VAL: 11 training plots (541 leaves; plots 6, 7, 11, 19, 24, 26, 28, 30, 36, 39, 41) to stop training; TEST for the final prediction.',
         'DSF of the task from Step 8.',
         steps('Choose the validation plots: a random third of the 33 training plots (seed 42).',
               'Standardise with the mean and SD of the 22 fitting plots only.',
               'Input: DNN-F1 uses the feature vector; DT-EDNet, EfficientNet-B0, ResNet18 and ConvNeXt V2-Atto use a 4 × 4 pseudo-image (k = max(3, ⌈√p⌉); unused cells = 0).',
               'Loss: class-weighted cross-entropy with label smoothing 0.01 (A, B); mean squared error (C).',
               'Train with AdamW (learning rate 6 × 10^{−4}, weight decay 10^{−5}), cosine decay to 10^{−6}, batch 32, gradient clipping 1.2, dropout 0.03, seed 42.',
               'After every epoch score the validation plots (macro-F1 for A and B, −RMSE for C); keep the weights of the best epoch.',
               'Stop when the validation score has not improved for 20 epochs (maximum 100).',
               'Restore the best-epoch weights; predict the 699 test leaves once; save the network (.pt).'),
         'Paper settings of Ma et al. (2026), adapted for CPU (≤ 100 epochs, patience 20). No further tuning. The best-epoch network itself is the delivered model (not refitted on all 33 plots).',
         '15 networks and their test predictions → Step 11; the same files → Step 16. Learning curves → report Figure 20.',
         'run_dl.sh → a4_dl.py (stage main) → dl_models/*.pt, dl_main.json.',
         'Ma et al. (2026); Prechelt (1998); Goodfellow et al. (2016); Sharma et al. (2019); He et al. (2016); Tan and Le (2019); Woo et al. (2023).',
         '16–17, 44; appendix 96, 105, 138',
         'Keep the validation plots inside TRAIN. With GPU, tuning of the learning rate on DL-VAL is possible.')
    tab('dlcard', 19, widths=[2200, 7400], size=17, boldfirst=True, subs=True)
    read(why='DT-EDNet is the network of the rice-blast study on which the methodology is based; the other three networks are the comparison networks of the same paper.',
         done=['DT-EDNet: 3 × 3 convolutional embedding (128 channels) → squeeze-and-excitation (SE; re-weights channels) → dual transformer group (a kernel transformer block with CBAM attention and four token transformer blocks) → class token → output layer.',
               'Because a leaf gives 11–12 numbers, not an image, the features are arranged in a 4 × 4 grid ("pseudo-image"), and the networks use stride-1 stems so that the small grid is not shrunk away.'],
         means='The networks are trained exactly as in the paper, so their performance can be compared fairly with the machine-learning models.',
         say='"The networks were trained with the paper settings; early stopping on a third of the training plots chose the epoch."')
    tab('dlruns', 28, widths=[2400, 2000, 2600, 2600], size=17)
    read(shows='Size of each network, training length and validation score.',
         found='Parameters range from 3 106 (DNN-F1) to 11.2 million (ResNet18). Training stopped after a median of 36 epochs (22–80). Mean validation macro-F1 0.59–0.65 (A and B).',
         means='The image networks have hundreds to thousands of times more parameters than the 1090 fitting leaves can support, so early stopping is essential.',
         say='"Training stopped early, after about 36 epochs on average, to prevent over-fitting."')
    fig('lc', 'f21_learning_curves.png', 'Training and validation loss and validation macro-F1 of the four pseudo-image networks (six grades; early stopping on one third of the training plots).', rep=20)
    read(shows='How loss and validation macro-F1 change during training of the six-grade networks.',
         how='Blue = training loss; orange = validation loss; green = validation macro-F1 (right axis); the dotted vertical line marks the best validation epoch, whose weights were kept (DT-EDNet 8, EfficientNet-B0 16, ResNet18 28, ConvNeXt V2-Atto 37).',
         found='Training loss keeps falling, while validation loss starts to rise after a few epochs – the classic sign of over-fitting on a small data set. Validation macro-F1 levels off at about 0.35–0.42; training stopped 20 epochs after its best value.',
         means='Without early stopping the networks would memorise the 22 fitting plots. The kept epoch is the one that generalised best to the 11 validation plots.',
         say='"The networks begin to over-fit after a few epochs; early stopping keeps the best epoch."')
