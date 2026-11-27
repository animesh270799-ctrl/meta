from k0_lib import *


def add():
    h1('7. Step 11: testing once on the 15 test plots')
    p('Only now are the test plots opened. The 30 models of Steps 9 and 10 (15 machine-learning models and 15 networks) predict the 699 test leaves, and the predictions are compared '
      'with the visual grades. Nothing is changed after this step: no feature, setting or model is altered because of a test result.')
    card('card11', '11', 'Test evaluation and plot bootstrap (Activity 2.4)',
         'Measure how accurate each model is on plots it has never seen, and how uncertain that number is.',
         'TEST: 699 leaves of the 15 test plots (126 leaves of 4 healthy plots, 573 of 11 unsprayed plots). Evaluation only.',
         'Test predictions of the 30 models; observed grades of the test leaves.',
         steps('Detection (A): confusion matrix → OA, kappa, macro-F1, sensitivity, specificity, balanced accuracy; AUC from the probability or decision value.',
               'Six grades (B): OA, kappa, macro-F1, quadratic weighted kappa (QWK), share within one grade, F1 of each grade, confusion matrix.',
               'Score (C): R², RMSE, MAE, RPD, bias, r.',
               'Plot bootstrap: draw the 4 healthy and the 11 unsprayed test plots WITH replacement (separately), take all leaves of the drawn plots, recompute the metric; repeat 1000 times.',
               'Standard error = SD of the 1000 bootstrap values; 95% interval = 2.5th–97.5th percentile.',
               'Rank the models by the main metric (macro-F1 for A and B, R² for C).'),
         'Bootstrap: 1000 resamples, seed 42, healthy and unsprayed plots resampled separately (the strata of the split).',
         'metrics_all.csv, confusion matrices → report Tables 29–31, Figures 21–26 → Step 15 (comparison with LORO).',
         'a5_metrics.py (cls_metrics, reg_metrics, plot_boot) called by a5_extra.py.',
         'Cohen (1960, 1968); Fawcett (2006); Sokolova and Lapalme (2009); Williams (2001); Efron and Tibshirani (1993); Field and Welsh (2007).',
         '18, 38–43; appendix 97, 106–108, 138',
         'Run unchanged. With very few test plots (< 8) the bootstrap interval becomes unreliable; then prefer repeated splits or LORO.')
    tab('metrics', 20, widths=[2400, 5700, 1500], size=17)
    read(shows='Every metric used, its formula and the task it serves.',
         how='Macro-F1 = mean of the F1 of each class, so the rare grade 9 counts as much as grade 0. QWK gives partial credit to near misses: confusing grade 3 with 5 costs less than 0 with 9. RPD = SD of the observed grades / RMSE.',
         means='No single number describes a model. Detection needs both sensitivity and specificity; grades need an exact metric (macro-F1) and an ordinal one (QWK); the score needs error in grade units (RMSE).',
         say='"Macro-F1 is the main metric for classes, R² and RMSE for the score; QWK tells how far off the wrong grades are."')
    box('Why a bootstrap of whole plots?', 'With one test set there are no folds to give a spread. The test leaves of one plot are related, so resampling single leaves would make the interval '
        'too narrow. Resampling whole plots keeps each plot\'s leaves together, as the split did (Field and Welsh, 2007). Resampling healthy and unsprayed plots separately keeps the '
        'test set\'s mix of 4 healthy and 11 unsprayed plots in every resample.', kind='method')
    tab('mA', 29, widths=[2000, 900, 900, 1000, 1700, 1100, 1100, 900], size=17)
    read(shows='Detection results of all ten model types on the 699 test leaves, best first.',
         how='"± bootstrap SE" is the plot-bootstrap standard error. Sensitivity = share of diseased leaves found; specificity = share of healthy leaves called healthy.',
         found=['SVM was best: macro-F1 0.826 ± 0.017, AUC 0.930, sensitivity 0.843, specificity 0.900 (153 of 170 healthy and 446 of 529 diseased test leaves correct).',
                'DNN-F1 (0.824), ResNet18 (0.822), ConvNeXt V2-Atto (0.818), XGBoost (0.813), RF (0.811) and DT-EDNet (0.808) were within one standard error of SVM.',
                'Several networks reached high sensitivity (0.89–0.92) but low specificity (0.70–0.77): they called too many healthy leaves diseased. PLS-DA was weakest (0.719).'],
         means='Detection is reliable and does not need a deep network. The differences among the top seven models are smaller than the uncertainty of the test set.',
         say='"On plots it never saw, SVM detects a diseased leaf with macro-F1 0.83 and AUC 0.93; the next six models are statistically as good."')
    tab('mB', 30, widths=[1700, 600, 600, 700, 800, 600, 700, 600, 600, 600, 600, 600, 600], size=15)
    read(shows='Six-grade results with the F1 of each grade.',
         how='OA and macro-F1 count exact hits; QWK and "±1 grade" give credit for near misses.',
         found=['RF was best by macro-F1 (0.374; QWK 0.657; 77.3% within one grade); SVM had the highest OA (0.418) and QWK (0.658).',
                'Grade 0 was recognised best (F1 0.54–0.76); grades 3 (0.00–0.30) and 9 (0.00–0.31) worst. PLS-DA never predicted grades 3, 7 or 9 correctly (F1 0.00).'],
         means='The exact grade is right for only about 40% of leaves, but three in four leaves are within one grade. The spectral signal ranks severity but cannot separate neighbouring grades sharply.',
         say='"Exact six-grade accuracy is about 40%, but three quarters of leaves are within one grade."')
    tab('mC', 31, widths=[1900, 900, 900, 1700, 900, 900, 900, 900], size=17)
    read(shows='Severity-score results of all models.',
         found='RF (R² 0.517, RMSE 1.919 ± 0.115) and XGBoost (0.512) were best; DNN-F1 was the best network (0.481). RPD of the best models 1.43–1.44 ("fair"); bias −0.1 to −0.2 grades. EfficientNet-B0 was weakest (R² 0.287, bias −0.61).',
         means='The score explains about half of the variation in grade with a typical error of about two grades. It is useful for ranking leaves and plots, not for exact grading.',
         say='"The best score model explains 52% of the variation with an error of 1.9 grades."')
    fig('comp', 'f16_model_comparison.png', 'Model comparison on the 70:30 test plots: macro-F1 for detection and six grades (± plot-bootstrap SE) and R² for the severity score (blue: machine learning; purple: deep learning).', rep=21)
    read(shows='The main metric of all models for the three tasks.',
         how='Bars sorted from best to worst; blue = machine learning, purple = deep learning; whiskers = plot-bootstrap SE.',
         found='In every task the whiskers of the top models overlap. Tree ensembles and SVM lead; DT-EDNet is in the middle (score) or lower half (detection, six grades).',
         means='The choice between ML and DL matters less than the choice of features and the difficulty of the task.',
         say='"Machine learning and deep learning overlap; no model is clearly best."')
    fig('heat', 'f31_metric_heatmap.png', 'All metrics of all models (darker = better within each column).', rep=22)
    read(shows='Every metric of every model as a colour table.',
         how='Darker green = better within the column (lower is better for RMSE and MAE). Read along a row for a model\'s profile.',
         found='Rows of SVM, RF and XGBoost are dark across tasks; EfficientNet-B0 and PLS are light in most columns.',
         means='Good models are good across metrics, so the ranking does not depend on the choice of metric.',
         say='"The same few models are good on every metric."')
    fig('cm', 'f17_confusion.png', 'Confusion matrices (counts and row percentages) of the best machine-learning and deep-learning models for six grades.', rep=23)
    read(shows='For the best ML model (RF) and the best network (ConvNeXt V2-Atto), how the test leaves of each true grade were classified.',
         how='Rows = true grade, columns = predicted grade; each cell gives count and row percentage; the diagonal is correct.',
         found='RF classified 75% of grade-0 leaves correctly, 41% of grade 1, 19% of grade 3, 33% of grade 5, 28% of grade 7 and 33% of grade 9; most errors fall in the cells next to the diagonal.',
         means='Errors are mostly one grade away, which is why QWK (0.66) is much higher than macro-F1 (0.37).',
         say='"The models confuse neighbouring grades, not distant ones."')
    fig('roc', 'f18_roc.png', 'ROC curves for detection (solid: machine learning; dashed: deep learning).', rep=24)
    read(shows='Sensitivity against false-positive rate for all detection models as the threshold changes.',
         how='Curves closer to the upper-left corner are better; the area under each curve is the AUC.',
         found='Most curves lie close together with AUC 0.87–0.93; PLS-DA (0.825) lies lowest.',
         means='A threshold can be chosen to favour sensitivity (early warning) or specificity (fewer false alarms) without retraining.',
         say='"All good models separate healthy and diseased leaves with AUC around 0.9."')
    fig('radar', 'f19_radar.png', 'Six-grade performance profile (F1 of each grade, OA, kappa and macro-F1).', rep=25)
    read(shows='The six-grade profile of each model as a polygon.',
         how='Each axis is a metric (centre = 0). A larger polygon is better; dents show weak grades.',
         found='All polygons are large at grade 0 and dented at grade 3; most are also dented at grade 9 (F1 0.12–0.21), except RF (0.31).',
         means='The same grades are difficult for every model: the limitation lies in the data (overlapping grades, few grade-9 leaves), not in a particular method.',
         say='"Every model finds grade 0 easy and grades 3 and 9 hard."')
    fig('predobs', 'f20_pred_obs.png', 'Predicted vs observed severity score of the best machine-learning and deep-learning models (black: mean ± SD per grade).', rep=26)
    read(shows='Predicted score against observed grade for RF and DNN-F1.',
         how='Dots = leaves; black squares = mean prediction per grade ± SD; dashed = 1:1 line.',
         found='Mean predictions of RF rise steadily (1.20, 2.14, 3.28, 4.15, 4.88, 5.28 for grades 0, 1, 3, 5, 7, 9) but grade 0 is over-predicted and grades 7 and 9 under-predicted.',
         means='The order is right but extremes are pulled towards the middle (shrinkage), typical of regression on noisy labels. Leaves of grades 7 and 9 are under-estimated by about 2–4 grades.',
         say='"The score follows the right order but compresses the extremes."')

    # ---------------------------------------------------------------- Step 12
    h1('8. Steps 12–13: network checks, interpretation and robustness')
    h2('8.1 Step 12 – Feature configurations and DT-EDNet ablation')
    card('card12', '12', 'Network comparison on three feature configurations and DT-EDNet ablation (Step 2.5.3)',
         'Check whether the networks prefer another input, and which DT-EDNet modules help.',
         'Same as Step 10: DL-FIT (22 plots) to fit, DL-VAL (11 plots) to stop, TEST to evaluate. Six-grade task only.',
         'OW (15), VI (5) and DSF (11) of the six-grade task from Step 8.',
         steps('Train DT-EDNet, EfficientNet-B0, ResNet18 and ConvNeXt V2-Atto on OW, on VI and on DSF (12 runs).',
               'Train DT-EDNet without the dual transformer group (DT-EDNet-DTG), without squeeze-and-excitation (DT-EDNet-SE) and without both (DT-EDNet-SE-DTG) on DSF.',
               'Evaluate every run once on the 699 test leaves (macro-F1, OA, kappa, macro-recall, QWK).'),
         'Settings as Step 10 (learning rate 6 × 10^{−4}, ≤ 100 epochs, patience 20, seed 42).',
         'Report Tables 32–33, Figures 27–28 → discussion of DT-EDNet.',
         'a4_dl.py (stages config and ablation) → dl_config.json, dl_ablation.json.',
         'Ma et al. (2026); Hu et al. (2018); Woo et al. (2018).',
         '45–46; appendix 109–110, 139–140',
         'Run unchanged; on UAV images use real image patches instead of pseudo-images.')
    tab('cfg', 32, widths=[3000, 2200, 2200, 2200])
    read(shows='Six-grade macro-F1 of each network on each feature configuration.',
         found='ResNet18 with OW was best (0.347); DT-EDNet reached 0.342 (OW), 0.328 (VI), 0.313 (DSF). Differences between configurations were 0.01–0.07.',
         means='No configuration is clearly better; the networks gain nothing from the larger OW set compared with the compact DSF.',
         say='"The input configuration changed the networks by a few hundredths only."')
    fig('cfg', 'f22_config.png', 'Networks on the three feature configurations (six grades).', rep=27)
    read(shows='The same comparison as bars.', how='Light blue = OW, green = VI, purple = DSF.',
         found='Bars of the three configurations are of similar height for every network; VI is lowest for EfficientNet-B0 (0.261).',
         say='"All configurations perform alike."')
    tab('abl', 33, widths=[3000, 1300, 1300, 1600, 1300, 1100])
    read(shows='DT-EDNet with and without its two special modules.',
         found='Full DT-EDNet 0.313; without the dual transformer group 0.356; without SE 0.332; without both 0.352 (macro-F1).',
         means='On 4 × 4 pseudo-images the attention modules did not help; the simpler variants were slightly better. With 11 features there is no spatial structure for attention to use (Sharma et al., 2019). The modules are expected to matter on real UAV images.',
         caution='The differences (0.02–0.04) are within about one plot-bootstrap SE of the six-grade test set.',
         say='"At leaf level the DT-EDNet modules did not add accuracy; their place is on images."')
    fig('abl', 'f23_ablation.png', 'DT-EDNet module ablation (six grades).', rep=28)
    read(shows='The ablation results as grouped bars.', how='For each variant: OA, kappa, macro-recall and macro-F1.',
         found='The full network has the lowest macro-F1 and QWK of the four variants.', say='"Removing modules did not hurt at leaf level."')

    # ---------------------------------------------------------------- Step 13
    h2('8.2 Step 13 – Interpretation and robustness')
    card('card13', '13', 'SHAP, results by stratum, transfer tests and selection stability (Steps 2.5.4, 2.6.1–2.6.2)',
         'Explain what the models use, and check that accuracy does not depend on one stage, variety, leaf position, date or timing.',
         '13a strata: TEST predictions of the best ML (RF) and DL (ConvNeXt V2-Atto) six-grade models. 13b SHAP: ALL leaves (descriptive). 13c transfer: ALL leaves, each variety or timing held out once. 13d stability: the 70:30 training set and the three LORO training parts.',
         'Test predictions; Objective 1 DSF (for SHAP); bands and indices (for transfer).',
         steps('Strata: split the 699 test predictions by growth stage, variety, leaf position, date and timing; compute macro-F1 (B) and RMSE (C) in each group.',
               'SHAP: fit XGBoost (300 trees, depth 4, rate 0.05) on the Objective 1 DSF of all leaves for the score and the grades; compute TreeSHAP values.',
               'Transfer: for each variety (V1–V3) and timing (D1–D4) train on all other leaves, repeat the selection inside that training set (SHAP-CARS 10 runs, ReliefF, VIF), fit RF (500 trees) and test on the held-out group.',
               'Stability: count in how many of the four training sets each optimal wavelength was chosen.'),
         'Transfer and SHAP do not depend on the 70:30 split and are identical to the LORO report (the transfer file is copied from that run).',
         'Report Figures 29–31 and 19 → discussion and robustness statements.',
         'a5_extra.py (strata_metrics.csv, shap_*.npy, transfer_tests.csv, selection_stability.csv).',
         'Lundberg and Lee (2017); Lundberg et al. (2020); Roberts et al. (2017).',
         '47–49; appendix 141',
         'Run unchanged. On a new data set the transfer tests should be re-run (they use all leaves of that data set).')
    fig('shap', 'f24_shap.png', 'SHAP summary for the severity score and SHAP importance by grade for six grades (XGBoost on the disease-specific feature set).', rep=29)
    read(shows='Which features push the predicted severity up or down, and which matter for each grade.',
         how=['(a) Each dot is a leaf; x = SHAP value (right of zero raises the predicted score); colour = feature value (red high, blue low); features ordered by importance.',
              '(b) Mean |SHAP| of each feature for each grade.'],
         found='For the score the most important features were FD870, REP, FD1060 and FD1245 (mean |SHAP| 0.89, 0.58, 0.50, 0.37). High FD870, low REP, low FD1060 and high FD1245 raise the predicted grade.',
         means='The model relies on the expected physiology: a lower red-edge position (chlorophyll loss), a changed NIR slope (structure) and the NIR–SWIR water edge (dehydration).',
         caution='SHAP was computed on all leaves with the Objective 1 feature set; it explains the signal, not the specific 70:30 model files.',
         say='"The models use the red edge, the NIR slope and the water edge – the physiology of white rust."')
    fig('strata', 'f25_strata.png', 'Six-grade macro-F1 by growth stage, variety, leaf position and date.', rep=30)
    read(shows='Six-grade macro-F1 of RF and ConvNeXt V2-Atto within groups of the test leaves.',
         how='Each pair of bars is one group of test leaves; n = number of test leaves in it.',
         found=['RF: stage flowering 0.36, pod formation 0.28, vegetative 0.30; variety V1 0.39, V2 0.37, V3 0.35; leaf L3 0.33, L5 0.37, LL 0.36.',
                'By date RF rose from 0.21 (11 Feb, 122 leaves) to 0.33 (3 and 13 Mar); timing D4 0.48 was highest.'],
         means='Accuracy is similar across varieties and leaf positions. It is lower on the first date, when most leaves were grade 0–1 and the grade range was narrow. Small groups (122–359 leaves) make these values uncertain.',
         say='"Accuracy is similar for all varieties and leaf positions; the first date is hardest because disease was just starting."')
    fig('transfer', 'f26_transfer.png', 'Leave-one-variety-out and leave-one-timing-out tests (random forest).', rep=31)
    read(shows='Accuracy when a whole variety or sowing timing is left out of training and used as the test.',
         how='(a) six-grade macro-F1 of the held-out group; (b) score RMSE of the held-out group.',
         found='Held-out variety: macro-F1 0.37 (V1), 0.39 (V2), 0.34 (V3); held-out timing: 0.37 (D1), 0.31 (D2), 0.34 (D3), 0.40 (D4). RMSE 1.91–2.23 grades.',
         means='These values are close to the 70:30 test values (macro-F1 0.33–0.37, RMSE 1.92–2.10), so the models do not depend on having seen the same variety or sowing date.',
         caution='These tests use all 2330 leaves (each group held out once) and are the same as in the LORO report; the report text "close to the cross-validated value" should read "close to the test value".',
         say='"A model trained without a variety or sowing date still works on it."')
