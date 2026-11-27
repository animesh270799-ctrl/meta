from dsl import *


def add():
    h1('8. Results of Objective 2: how well can white rust be detected and graded?')
    h2('8.1 What the machine-learning models selected')
    tab('sffs', 25, widths=[700, 1100, 1300, 1400, 1300, 3800], size=16)
    read(shows='For each task and machine-learning model: how many candidate features were available, how many SFFS kept, the inner cross-validation score and the settings chosen in fold 1.',
         how='Columns 3–5 are averages over the three folds. The inner score is macro-F1 for tasks A and B and minus RMSE for task C (so −2.01 is better than −2.10).',
         found=['From about 11 candidates the models kept 5–9 features; k-NN and PLS kept the fewest.',
                'Inner scores were close between SVM, RF and XGBoost (detection 0.80–0.82, six grades 0.37–0.38, score RMSE 2.01–2.03); PLS-DA/PLSR were clearly lower.',
                'Typical settings: SVM C = 10; RF with 500 trees and minimum leaf size 1–3; XGBoost with shallow trees (depth 3–5) and a low learning rate (0.05).'],
         means='Compact models with 6–9 features are enough; adding more features did not improve the inner score by more than 1%. The inner scores already predict the final ranking: '
               'the non-linear models (SVM, RF, XGBoost) beat the linear PLS models, meaning that the relationship between spectra and grade is not purely linear.',
         say='"Each model needed only 6–9 features; the non-linear models were clearly better than the linear PLS models."')
    h2('8.2 How the networks trained')
    tab('dlruns', 26, widths=[2400, 2000, 2600, 2600], size=17)
    read(shows='The size of each network, how long it trained before early stopping, and its best validation score.',
         how='"Parameters" = number of trainable weights; "Epochs" = median number of passes over the training data before early stopping (9 runs = 3 folds × tasks); validation score = macro-F1 on the validation plots.',
         found=['The networks range from 3 thousand weights (DNN-F1) to 11 million (ResNet18). DT-EDNet has 0.95 million.',
                'The image networks stopped after a median of 31–42 epochs; DNN-F1 trained longer (81).',
                'Best validation scores were all between 0.616 and 0.638 – essentially the same.'],
         means='Having 1000–4000 times more weights than DNN-F1 did not give the image networks a better validation score. With 1500 training leaves and 10–16 features there is far '
               'less information than these networks were designed for, so they reach their limit quickly.',
         say='"Networks with millions of weights reached the same validation score as a tiny dense network."')
    fig('lc', 'f21_learning_curves.png', 'Training and validation loss and validation macro-F1 of the four pseudo-image networks (fold 1, six grades).', rep=19)
    read(shows='How the four image networks learned during training in fold 1 for the six-grade task.',
         how='Blue = training loss (error on the training leaves), orange = validation loss (error on held-out validation plots), green = validation macro-F1 (right axis). The dotted line marks the best epoch kept by early stopping.',
         found=['Training loss falls steadily in all four networks.',
                'Validation loss stops improving after a few epochs and then rises (most clearly for DT-EDNet and ResNet18).',
                'Validation macro-F1 stays flat at about 0.30–0.40; the best epochs were 10 (DT-EDNet), 13 (EfficientNet-B0), 5 (ResNet18) and 28 (ConvNeXt V2-Atto).'],
         means='This is the classic picture of **over-fitting**: after the first few epochs the networks start memorising the training leaves instead of learning patterns that hold for '
               'new plots. Early stopping on the validation plots kept the best epoch, so the test results are not affected by the over-fitting, but it shows that the networks are too '
               'large for this amount of leaf data.',
         say='"The networks learn the useful pattern within a few epochs and then start memorising; early stopping protects the results."')

    h2('8.3 Test results of all models')
    p('The three tables below are the core results of Objective 2. All numbers are pooled test predictions: every one of the 2330 leaves was predicted once, by a model trained '
      'without its replication.')
    tab('mA', 27, widths=[2000, 900, 900, 1000, 1700, 1100, 1100, 900], size=17)
    read(shows='Detection (healthy vs diseased) results of the 10 models, best first.',
         how='Macro-F1 is the main metric; "± SD folds" is its spread over the three test folds. Sensitivity = share of diseased leaves found; specificity = share of healthy leaves correctly called healthy.',
         found=['Best: SVM (macro-F1 0.792 ± 0.007, AUC 0.897) and DNN-F1 (0.790 ± 0.009, AUC 0.896), followed by ResNet18 (0.785) and ConvNeXt V2-Atto (0.783).',
                'SVM is balanced: sensitivity 0.831 and specificity 0.833. EfficientNet-B0, RF, k-NN and PLS-DA find more diseased leaves (sensitivity 0.85–0.92) but at the cost of '
                'calling many healthy leaves diseased (specificity 0.48–0.71).',
                'DT-EDNet: macro-F1 0.759, AUC 0.852 – eighth of ten.'],
         means='A diseased leaf can be recognised from its spectrum with about 83% accuracy in both directions, under a strict test on unseen replications. The top four models are '
               'within about one fold-to-fold SD of each other, so they should be regarded as equally good; SVM is preferred because it is simple and balanced.',
         say='"Detection is reliable: the SVM finds 83% of diseased leaves and correctly clears 83% of healthy ones, AUC 0.90."')
    tab('mB', 28, widths=[1700, 600, 600, 700, 800, 600, 700, 600, 600, 600, 600, 600, 600], size=15)
    read(shows='Six-grade results of the 10 models, with the F1 of each grade.',
         how='Overall accuracy (OA) and macro-F1 count only exact hits; QWK and "±1 grade" give credit for near-misses. The F1 columns show how well each grade is recognised.',
         found=['Best macro-F1: ConvNeXt V2-Atto 0.360 (QWK 0.633, 75.5% within one grade), then RF 0.349, SVM 0.346, DNN-F1 0.344, XGBoost 0.342.',
                'Exact accuracy is only 0.35–0.40 for all models, but 70–76% of leaves are within one grade and QWK is 0.59–0.63 for the good models.',
                'Grade 0 is recognised best (F1 0.59–0.70), grade 1 next (about 0.40); grades 3, 5 and 9 are the weakest (F1 often 0.15–0.35).',
                'PLS-DA failed on the extreme grades (F1 0.00 for grade 9).'],
         means='Exact six-grade classification of single leaves is not achievable with leaf spectra alone: about two leaves in five are placed in the exact grade. But the errors are mostly '
               'small – three leaves in four land in the right grade or the next one – and QWK above 0.6 means substantial agreement on the ordered scale. The models capture the '
               'severity **order**, not the exact visual category.',
         say='"Exact grades are right for only 39% of leaves, but 75% are within one grade – the models get the order right, not the exact class."')
    tab('mC', 29, widths=[1900, 900, 900, 1700, 900, 900, 900, 900], size=17)
    read(shows='Severity-score (0–9) results of the 10 models.',
         how='R² = share of the variation in grade explained; RMSE and MAE in grade units; RPD = SD of observed grades / RMSE; bias = mean of predicted − observed; r = correlation.',
         found=['Best: XGBoost R² 0.459, RMSE 2.04, MAE 1.58, RPD 1.36, r 0.68; RF (0.449), DNN-F1 (0.448) and SVR (0.445) are very close.',
                'All models have a small negative bias (−0.01 to −0.32): they slightly under-predict on average.',
                'RPD is 1.27–1.36 for all models, below the 1.4 often used as the limit of "fair".'],
         means='The score is predicted with moderate accuracy: the typical error is about 1.6–2.0 grade units, i.e. about one step on the 0, 1, 3, 5, 7, 9 scale. The score is useful for '
               'ranking leaves and for following severity over time, but it is not precise enough to replace visual grading of individual leaves.',
         say='"The severity score explains 46% of the variation with a typical error of about 2 grade units – useful for ranking, not for exact grading."')
    fig('comp', 'f16_model_comparison.png', 'Model comparison: macro-F1 for detection and six grades (± SD over folds) and R² for the severity score (blue: machine learning; purple: deep learning).', rep=20)
    read(shows='The main metric of every model for the three tasks, side by side.',
         how='Bars are sorted from best to worst; blue = machine learning, purple = deep learning; the small whiskers show the SD over the three folds.',
         found=['Detection: SVM 0.792 and DNN-F1 0.790 lead; nine of ten models are between 0.72 and 0.79.',
                'Six grades: ConvNeXt V2-Atto 0.360 leads, but the next six models (RF, SVM, DNN-F1, XGBoost, ResNet18, DT-EDNet) are within 0.023 of it.',
                'Score: XGBoost 0.459 leads; RF, DNN-F1 and SVR follow within 0.015.'],
         means='Machine-learning and deep-learning models are interleaved in every ranking; neither family is consistently better. The whiskers of the leading models overlap, so the '
               'differences between them are within the normal variation between replications.',
         say='"Machine learning and deep learning are mixed in every ranking – the differences between the best models are within the noise."')
    fig('heat', 'f31_metric_heatmap.png', 'All metrics of all models (darker = better within each column).', rep=21)
    read(shows='Every metric of every model as a colour table, separately for the three tasks.',
         how='Each column is one metric; darker green = better within that column (for RMSE and MAE lower is better). Read across a row to see a model\'s profile.',
         found=['Detection: SVM and DNN-F1 are dark in almost every column; PLS-DA has the highest sensitivity (0.92) but the lowest specificity (0.48).',
                'Six grades: ConvNeXt V2-Atto is darkest for macro-F1, QWK and within-one; SVM has the highest exact accuracy (0.40).',
                'Score: XGBoost is darkest for R², RMSE, RPD and r; SVR has the lowest MAE (1.56).'],
         means='Different metrics can favour different models, which is why several metrics are reported. A model that maximises sensitivity (PLS-DA) is not the best overall; '
               'balanced models are preferred for disease surveillance, where false alarms also have a cost.',
         say='"The heat map shows that the top models are good across all metrics, not just the main one."')
    fig('cm', 'f17_confusion.png', 'Confusion matrices (counts and row percentages) of the best machine-learning (RF) and deep-learning (ConvNeXt V2-Atto) models for six grades.', rep=22)
    read(shows='Where the six-grade predictions go: for each observed grade (rows), how many leaves were predicted in each grade (columns).',
         how='Each cell shows the number of leaves and the percentage of its row; darker green = higher share; the outlined diagonal cells are correct predictions. Cells next to the diagonal are one-grade errors.',
         found=['Grade 0: 70% (RF) and 67% (ConvNeXt) correct; most errors go to grade 1.',
                'Grade 1: 38% and 43% correct; errors spread mainly to grades 0 and 3.',
                'Grade 3: only 13% (RF) and 28% (ConvNeXt) correct; many grade-3 leaves were predicted as grade 5 (27% in RF).',
                'Grade 5: 34% (RF) correct but only 19% for ConvNeXt, which put 30% of grade-5 leaves in grade 3 and 24% in grade 7.',
                'Grade 9: 29% and 33% correct; 26–28% were predicted as grade 7 and 30% (RF) as grade 5.'],
         means='The errors pile up next to the diagonal: the models confuse neighbouring grades far more than distant ones. This is exactly the pattern expected when neighbouring '
               'grades overlap spectrally and when the visual scale itself is uncertain between adjacent grades (Bock et al., 2010). Gross errors (for example grade 9 predicted as 0) are rare (2%).',
         say='"Most mistakes are one grade off; a severe leaf is almost never called healthy."')
    fig('roc', 'f18_roc.png', 'ROC curves for detection (solid: machine learning; dashed: deep learning).', rep=23)
    read(shows='The trade-off between finding diseased leaves and raising false alarms, for every detection model.',
         how='Each curve traces sensitivity (vertical) against the false-positive rate (horizontal) as the decision threshold changes. A curve close to the upper-left corner is better; '
             'the diagonal dotted line is chance. The area under the curve (AUC) is given in the legend.',
         found=['SVM (AUC 0.897) and DNN-F1 (0.896) have the highest curves; RF, ResNet18, XGBoost, ConvNeXt, EfficientNet and DT-EDNet follow (0.85–0.88); k-NN and PLS-DA are lowest (0.84).',
                'At a false-positive rate of 10%, SVM and DNN-F1 still find about 75% of diseased leaves; at 20% they find about 86%.'],
         means='All models are far above chance. The ROC curve shows that the decision threshold can be moved depending on the purpose: an early-warning system can accept more false '
               'alarms to catch more diseased leaves, while a fungicide decision might demand fewer false alarms.',
         say='"All models are well above chance; the best reach AUC 0.90, and the threshold can be tuned to the purpose."')
    fig('radar', 'f19_radar.png', 'Six-grade performance profile (F1 of each grade, OA, kappa and macro-F1).', rep=24)
    read(shows='A "spider" chart comparing the five networks and the best tree model (XGBoost) on the F1 of each grade and three summary metrics.',
         how='Each axis is one metric (0 at the centre, higher further out). A larger polygon is better; the shape shows which grades a model handles well.',
         found=['All polygons extend furthest towards "F1 grade 0" (0.59–0.67) and are small towards grades 3, 5 and 9.',
                'DT-EDNet has the best F1 for grade 5 (0.39); DNN-F1 is relatively strong for grade 9 (0.28); ConvNeXt is strongest for grades 0 and 3.'],
         means='The models share the same strengths and weaknesses: healthy leaves are recognised, the middle grades are not. Differences between models are local (one grade here or there) '
               'rather than a general advantage.',
         say='"All models recognise healthy leaves well and struggle with the middle grades."')
    fig('predobs', 'f20_pred_obs.png', 'Predicted vs observed severity score of the best machine-learning (XGBoost) and deep-learning (DNN-F1) models (black: mean ± SD per grade).', rep=25)
    read(shows='For every leaf, the predicted severity score against its visual grade.',
         how='Each coloured dot is a leaf (spread sideways within its grade); black squares are the mean prediction per grade with ± SD bars; the dashed line is the 1:1 line of perfect prediction.',
         found=['XGBoost mean predictions: grade 0 → 1.2, 1 → 2.3, 3 → 3.5, 5 → 4.1, 7 → 4.9, 9 → 5.3. DNN-F1 is similar (1.1 to 5.0).',
                'The SD within each grade is about 1.1–1.6 grade units.'],
         means='The predictions increase with the true grade, so the ranking is right, but the line is flatter than 1:1: low grades are over-predicted and high grades are under-predicted. '
               'This "shrinkage towards the mean" is typical when the inputs explain only part of the variation; the model hedges towards the middle of the scale. It means the score '
               'should be calibrated before being used as an absolute severity value, especially for severe leaves.',
         say='"Predictions follow the grade but are pulled towards the middle: a grade-9 leaf is predicted at about 5."')

    h2('8.4 Feature configurations and the DT-EDNet ablation')
    tab('cfg', 30, widths=[3000, 2200, 2200, 2200])
    read(shows='Six-grade macro-F1 of the four image networks when fed with three different feature sets.',
         how='OW = the 15 optimal wavelengths; VI = the five selected indices; DSF = the disease-specific feature set (11 features).',
         found=['ConvNeXt V2-Atto was best overall with OW (0.371).', 'DT-EDNet did best with DSF (0.337), followed by VI (0.334) and OW (0.319).',
                'Differences between configurations are 0.02–0.04 for each network.'],
         means='No feature set is best for every network, and the differences are about the size of the fold-to-fold variation. The compact DSF is a sound default; the 15 optimal '
               'wavelengths can help a network that can exploit many inputs.',
         caution='The original report text stated that DT-EDNet did best on the optimal wavelengths; the table shows it did best on the DSF (0.337 vs 0.319 for OW).',
         say='"The choice of feature set changes the networks by only 0.02–0.04 macro-F1."')
    fig('cfg', 'f22_config.png', 'Networks on the three feature configurations (six grades).', rep=26)
    read(shows='The same comparison as the table, as grouped bars.',
         how='Light blue = OW, green = VI, purple = DSF, for each network.',
         found='All bars lie between 0.32 and 0.37 macro-F1.',
         means='The networks are limited by the information in the leaf spectra, not by the particular way the features are chosen.',
         say='"Whatever features they get, the networks land between 0.32 and 0.37."')
    tab('abl', 31, widths=[3000, 1300, 1300, 1600, 1300, 1100])
    read(shows='What happens to DT-EDNet when its special modules are removed.',
         how='DT-EDNet-DTG = without the dual transformer group; DT-EDNet-SE = without the squeeze-and-excitation block; DT-EDNet-SE-DTG = without both. Macro-recall = average recall over grades.',
         found=['Full DT-EDNet: macro-F1 0.337, QWK 0.592.',
                'Without SE: 0.319 (−0.018); without DTG: 0.326 (−0.011); without both: 0.327 (−0.010).',
                'QWK fell more clearly without DTG (0.533) or without both (0.543) than without SE (0.579).'],
         means='Each module adds a little, but the changes (0.01–0.02 macro-F1) are smaller than the fold-to-fold variation and not additive (removing both is not worse than removing one). '
               'On 4 × 4 pseudo-images there is little spatial structure for attention modules to use, so their benefit cannot show; the paper designed them for real hyperspectral images of canopies.',
         caution='The original report discussion said the dual transformer group mattered more; the table shows removing SE lowered macro-F1 more (0.319) than removing DTG (0.326). Both effects are small. '
                 'In the figure title DTG is written as "dual-token gating"; it is the dual transformer group of DT-EDNet.',
         say='"Removing DT-EDNet\'s modules changes it by only 0.01–0.02 – at leaf level its special design has little to work with."')
    fig('abl', 'f23_ablation.png', 'DT-EDNet module ablation (six grades).', rep=27)
    read(shows='The ablation as grouped bars for four metrics.',
         how='For each variant: OA, kappa, macro-recall and macro-F1.',
         found='The full network has the highest OA (0.39) and kappa (0.24); the variants are 0.35–0.37 and 0.21–0.22. Macro-recall is about the same (0.33–0.35) for all.',
         means='The full DT-EDNet is slightly more accurate overall, but its ability to recognise the individual grades (macro-recall) is not improved by the modules at leaf level.',
         say='"The full DT-EDNet is marginally better, but within the noise."')

    h2('8.5 Which features drive the predictions? (SHAP)')
    fig('shap', 'f24_shap.png', 'SHAP summary for the severity score and SHAP importance by grade for six grades (XGBoost on the disease-specific feature set).', rep=28)
    read(shows='(a) How each feature pushes the predicted severity score up or down; (b) how important each feature is for recognising each grade.',
         how=['(a) Each dot is a leaf. Its horizontal position is the SHAP value: right of zero = the feature raised the predicted score for that leaf, left = lowered it. Colour = the feature value (red = high, blue = low). Features are ordered by importance.',
              '(b) Mean |SHAP| for each feature, split by grade (colours); longer bars = more important.'],
         found=['Most important for the score: FD870 (mean |SHAP| 0.89), REP (0.58), FD1060 (0.50), FD1245 (0.37), FD665 (0.34), then DWSI-2, FD595, FD1090, Dr, FD760 and FD550.',
                'Directions: high FD870, high FD1245, high DWSI-2 and high FD595 raise the score; high REP, high FD1060, high FD665 and high Dr lower it.',
                'For six grades, FD870 is again the most important, contributing most to recognising grade 0 and grade 9; FD550 is important mainly for grade 1.'],
         means='The model uses the features in physically sensible ways. A low red-edge position (shifted towards the blue) and a low red-edge peak (Dr) mean less chlorophyll and a higher '
               'score; a steeper slope at 870 nm reflects the shifted red edge; a higher DWSI-2 (R_{1660}/R_{550}) and a higher slope at 1245 nm reflect drier tissue. The model is '
               'therefore not relying on an artefact: it reads chlorophyll, structure and water.',
         say='"The models rely on the red-edge position and the near-infrared slope, in the direction expected from chlorophyll loss – they read real physiology."')

    h2('8.6 Is the performance consistent across groups?')
    fig('strata', 'f25_strata.png', 'Six-grade macro-F1 by growth stage, variety, leaf position and sampling date (RF and ConvNeXt V2-Atto).', rep=29)
    read(shows='The six-grade macro-F1 of the best machine-learning (RF, blue) and deep-learning (ConvNeXt, purple) model computed separately within each group.',
         how='Each pair of bars is one group; n = number of leaves.',
         found=['Growth stage: 0.28–0.33 (vegetative lowest). Variety: 0.33–0.38. Leaf position: 0.32–0.38 (LL highest).',
                'Date: 0.22 on 11 February, 0.28–0.32 on the later dates.',
                'Detection was similarly stable (SVM macro-F1 0.76–0.80 by stage, variety and leaf position) except on 11 February (0.67), and the score R² was 0.38–0.48 by variety, leaf position and timing.'],
         means='Performance does not depend strongly on variety or leaf position. It is lower on 11 February because almost all leaves were grade 0–1 on that date: with little range of '
               'disease, the grades are harder to tell apart and R² within that date is even negative for the score (RMSE 1.35, small, but the variance within the date is also small). '
               'The models work best when the full range of disease is present.',
         say='"Results are similar across varieties, stages and leaf positions; only the first date, with very little disease, is weaker."')
    fig('transfer', 'f26_transfer.png', 'Leave-one-variety-out and leave-one-timing-out tests (random forest).', rep=30)
    read(shows='What happens when a model is applied to a variety (or sowing date) that it never saw during training.',
         how='(a) Six-grade macro-F1 on the held-out group; (b) severity-score RMSE on the held-out group. Dark bars = varieties, light bars = sowing timings.',
         found=['Six grades: held-out varieties V1 0.37, V2 0.39, V3 0.34; held-out timings D1 0.37, D2 0.31, D3 0.34, D4 0.40.',
                'Score RMSE 1.91–2.23 (R² 0.37–0.53), close to the cross-validated 2.04–2.06.'],
         means='A model trained on two varieties works as well on the third, and a model trained on three sowing dates works on the fourth. The spectral signal of white rust is '
               'therefore not specific to one variety or crop age – an important condition for applying the models to other fields and seasons.',
         say='"The models work on a variety or sowing date they have never seen – the signal is general."')

    h2('8.7 The covariate baseline: do the spectra add information beyond the calendar?')
    tab('covres', 32, widths=[1700, 1500, 900, 900, 1000, 900, 900, 900, 900], size=16)
    read(shows='The performance of three model types on three kinds of input – covariates only, leaf spectra only, and both – for the 1952 unsprayed leaves.',
         how='Rows are grouped by input; within each, B1 = interpretable statistical model, random forest, and the best machine-learning model of the task (B2). Higher is better except RMSE.',
         found=['**Covariates only** (no spectra): detection macro-F1 0.76–0.78 and AUC 0.93–0.94; six grades 0.29–0.31; score R² 0.32–0.33.',
                '**Leaf spectra only:** detection 0.70–0.73 (lower than covariates); six grades up to 0.36; score R² up to 0.41.',
                '**Spectra + covariates:** the best of all for every task – detection macro-F1 0.82 and AUC 0.96 (RF), six grades 0.41, score R² 0.45.'],
         means='The calendar (crop age, sowing date, stage, variety) predicts a large part of the disease level on its own. For the **severity** tasks the spectra do better than the '
               'calendar, and the combination is best. For **detection within unsprayed plots** the calendar is better than the spectra – explained below.',
         say='"Knowing only crop age, sowing date and stage already predicts much of the disease; the spectra beat this baseline for severity, and the combination is best."')
    fig('covmod', 'f32_cov_models.png', 'Primary metric of the three models on covariates only, leaf spectra and spectra + covariates (unsprayed, naturally infected leaves; M0 = the stronger covariate-only model).', rep=31)
    read(shows='The same results as bars: for each task, the main metric of the three models on each input.',
         how='Grey = interpretable model (logistic, ordinal logistic, linear), green = random forest, purple = best ML model; M0 marks the covariate model used as the baseline.',
         found=['Detection: covariates 0.76–0.78 > spectra 0.70–0.73 < spectra + covariates 0.76–0.82.',
                'Six grades: covariates 0.29–0.31 < spectra 0.27–0.36 < spectra + covariates 0.36–0.41.',
                'Score: covariates R² 0.32–0.33 < spectra 0.37–0.41 < spectra + covariates 0.39–0.45.'],
         means='The bars rise from left to right for the two severity tasks: each source of information adds to the other. For detection, the dip in the middle shows that within the '
               'unsprayed plots the date tells more about healthy vs diseased than the leaf spectrum does.',
         say='"For severity, spectra beat the calendar and the combination is best; for detection inside infected plots, the date says more."')
    tab('covgain', 33, widths=[1300, 1700, 2200, 2200, 2200], size=16)
    read(shows='The three gains with their 95% bootstrap intervals, and whether each gain meets the strict "real gain" rule.',
         how='ΔS = what the spectra add over the covariate baseline; ΔC = what the covariates add to the spectra; ΔT = both together over the baseline. ✓ = real gain, ✗ = real loss; '
             'unmarked = not consistent enough to be called real. For RMSE a negative value is an improvement.',
         found=['**Six grades:** ΔS +0.043 macro-F1 (+0.013 to +0.079) ✓; ΔC +0.037 ✓; ΔT +0.080 ✓ (QWK ΔT +0.071 ✓).',
                '**Score:** ΔS +0.083 R² (+0.048 to +0.117) ✓ and RMSE −0.135 ✓; ΔT +0.124 R² ✓ and RMSE −0.207 ✓.',
                '**Detection:** ΔS −0.078 macro-F1 and −0.199 balanced accuracy (a real loss ✗); ΔC +0.099; ΔT +0.021 (−0.031 to +0.070), not a real gain.'],
         means='Under a strict test, the leaf spectra add real information about **severity** that the calendar cannot provide: leaves of the same date, sowing and stage differ in their '
               'actual infection, and the spectra see that difference. For **detection inside the unsprayed plots** the spectra lose to the calendar – see the explanation box below.',
         say='"The spectra give a real, statistically confirmed gain for grades (+0.043) and score (+0.083 R²) beyond what the calendar predicts."')
    box('Why the calendar beats the spectra for detection inside unsprayed plots.', ['On 11 February 46% of the unsprayed leaves were still grade 0; on the later dates only 0–3% were. '
        'So within the unsprayed plots "healthy" almost means "first date", and the date alone separates most healthy from diseased leaves.',
        'This does not make the spectra useless for detection. A sensor surveying an unknown field does not know the sampling calendar of this experiment; and when the sprayed healthy '
        'plots are included (Chapter 8.3), the spectra detect disease with macro-F1 0.79 and AUC 0.90. The baseline shows that, in this experiment, time is a strong predictor that '
        'any honest evaluation has to account for.'], kind='present')
    fig('covgain', 'f33_cov_gains.png', 'Gains of the spectra (ΔS), of the covariates added to the spectra (ΔC) and of both (ΔT) with 95% plot-block bootstrap intervals (filled = real difference).', rep=32)
    read(shows='The gains of the previous table as points with interval bars.',
         how='Blue = ΔS, orange = ΔC, purple = ΔT. The vertical line is zero; right of zero = better (except RMSE, where left = better). Filled circles meet all three conditions of a real difference; open circles do not.',
         found=['Six grades: all three macro-F1 gains are filled and right of zero.', 'Score: ΔS and ΔT are filled for both R² and RMSE.',
                'Detection: ΔS is left of zero (filled for balanced accuracy = a real loss); ΔC is right of zero; ΔT straddles zero.'],
         means='The picture confirms the table at a glance: real gains for severity, no gain from spectra for detection within the infected plots.',
         say='"Filled points right of zero are the confirmed gains – they are all in the severity tasks."')
    p('DeLong tests of the detection AUC agree: the spectra model was below the covariate model (0.834 vs 0.926; z = −5.43, p < 0.001); spectra + covariates was slightly above the '
      'covariate model (0.942 vs 0.926; z = 2.10, p = 0.036) and well above the spectra alone (0.942 vs 0.834; z = 6.23, p < 0.001).')
    fig('covb1', 'f34_cov_b1.png', 'Standardised effects of the covariates in the interpretable models: logistic (detection), ordinal logistic (six grades) and linear (score) (95% CI).', rep=33)
    read(shows='The direction and size of each covariate\'s effect on disease in the three interpretable models, fitted on all unsprayed leaves.',
         how='Each point is the effect of a one-SD change in the covariate (or of a level compared with its reference, e.g. D4 vs D1), with its 95% interval. Red = raises disease, blue = lowers it, grey = not significant. Units: log-odds (detection, grades) or grade units (score).',
         found=['**Crop age (DAS)** has by far the largest effect: +5.0 log-odds per SD for detection, +2.77 for grades and +2.77 grade units for the score; its square is negative for grades (−0.38) and score (−0.21), i.e. the rise slows down.',
                '**Later sowing raises disease at the same crop age:** D2, D3, D4 vs D1 = +0.89, +1.74, +3.05 log-odds (detection), +0.49, +0.83, +1.73 (grades) and +0.54, +0.87, +1.72 grade units (score).',
                '**Growth stage** has a negative effect once crop age is accounted for (−0.66 grades, −0.60 score).',
                '**Variety V3** has less disease than V1 (−0.28 grades, −0.33 score); V2 slightly less (−0.11, −0.12).'],
         means='Disease increases strongly with crop age, as expected for a natural epidemic. At the same crop age, a later-sown crop is observed later in the season – for example '
               'D4 at 63 days on 13 March against D1 at 64 days on 11 February – when the epidemic and its inoculum had built up much further; the timing effect therefore largely carries calendar '
               'time. Variety V3 is somewhat more tolerant. These effects are why a model without spectra already '
               'predicts so much – and why the spectra must be judged by what they add beyond them.',
         say='"Crop age dominates; at the same age, later sowings had more disease, and V3 had the least."')
