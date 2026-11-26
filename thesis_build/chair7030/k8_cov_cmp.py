from k0_lib import *


def add():
    h1('9. Steps 14–15: the covariate baseline and the comparison with LORO')
    h2('9.1 Step 14 – Covariate baseline: what do the spectra add to the calendar?')
    p('Disease rose with crop age and date and differed with sowing time, variety and stage. A spectral model could therefore look accurate partly because it recognises the calendar '
      'rather than the disease (De Wolf and Isard, 2007). Step 14 builds models that know only the calendar, crop and weather – no spectrum – and credits the spectra only with what '
      'they add (Kuhn and Johnson, 2013; Zhang et al., 2014; Bijlwan et al., 2025).')
    card('card14', '14', 'Covariate baseline M0, spectral model M1, combined model M2 (Step 2.5.5)',
         'Measure how much of the disease the covariates explain without any sensor, and whether the leaf spectra add to it.',
         'UNS-TRAIN: 1379 unsprayed leaves of the 25 unsprayed training plots (fitting and inner tuning). UNS-TEST: 573 unsprayed leaves of the 11 unsprayed test plots (evaluation). '
         'The 378 leaves of the sprayed healthy block are left out: they share every covariate with the unsprayed plots but are healthy because of the fungicide, so they would teach a false rule.',
         'Covariates of Step 3 (DAS, DAS², timing, variety, stage code, 7-day weather, favourable days); DSF of Step 8 (spectra).',
         steps('Three inputs: covariates only; leaf spectra only (DSF of the task); spectra + covariates.',
               'Three models per input: B1 interpretable (logistic regression for A, proportional-odds ordinal logistic for B, linear regression with DAS and DAS² for C); random forest; B2 = the best ML model of Step 11 (SVM for A, XGBoost for B, RF for C).',
               'Standardise with the training statistics; tune RF, B2 and the logistic penalty in inner GroupKFold(3) by plot on UNS-TRAIN.',
               'Fit on UNS-TRAIN, predict UNS-TEST once.',
               'M0 = the stronger covariate-only model on the test leaves; M1 = B2 on spectra; M2 = B2 on spectra + covariates.',
               'Gains ΔS = M1 − M0, ΔC = M2 − M1, ΔT = M2 − M0 for macro-F1, AUC, balanced accuracy (A), macro-F1, QWK (B), R², RMSE (C).',
               'Paired plot bootstrap: resample the 11 unsprayed test plots 2000 times, recompute both models on the same resample, take the 2.5th–97.5th percentile of the difference. Real gain = interval excludes 0.',
               'DeLong test for the detection AUCs; B1 refitted on all unsprayed leaves with standardised covariates to show effect sizes (descriptive).'),
         'Seed 42; 2000 bootstrap resamples; weather windows end the day before sampling. With four dates, weather is collinear with date, so B1 uses DAS and DAS² as the time effect.',
         'Report Tables 34–35, Figures 32–34 → conclusion on the value of the spectra.',
         'a11_covariate.py, a12_figs_cov.py (cov2_metrics.csv, cov2_gains.csv, cov2_delong.csv, cov2_b1_coef.csv); a13_cov_models.py saves the 11 covariate models.',
         'De Wolf and Isard (2007); McCullagh (1980); Madden et al. (2007); Efron and Tibshirani (1993); DeLong et al. (1988); Sun and Xu (2014); Zhang et al. (2014); Ruan et al. (2022); Bijlwan et al. (2025).',
         '19–21, 50–52; appendix 98, 111–112',
         'Use the covariates of the new season; with more dates (e.g. 13 UAV flights) weather can enter as a separate predictor.')
    box('Two points to state openly.', [
        '**Choice of M0.** M0 is the better of the covariate-only models judged on the test leaves. This choice can only make the baseline stronger, so the reported gains of the spectra are conservative.',
        '**One test set, no folds.** The only rule for a real gain is that the 95% plot-bootstrap interval excludes zero. (Report section 3.12 and slide 21 mention LORO fold rules; they do not apply here.)'], kind='note')
    tab('covmodels', 21, widths=[2200, 1600, 2400, 2000, 1400], size=16)
    read(shows='The covariate-only models for each task and the covariates each uses.',
         found='B1 uses variety, timing, stage, DAS and DAS²; random forest and B2 also use the 7-day weather and favourable days.',
         means='B1 is the interpretable reference; RF and B2 are flexible enough to exploit any calendar pattern, so together they give a strong baseline.',
         say='"I built three models that know only the calendar, crop and weather."')
    tab('covres', 34, widths=[1700, 1500, 900, 900, 1000, 900, 900, 900, 900], size=16)
    read(shows='All nine input × model combinations on the 573 unsprayed test leaves.',
         how='Rows grouped by input; B1 = interpretable model; B2 = best ML model of the task. Higher is better except RMSE.',
         found=['Covariates only: detection macro-F1 0.735 (AUC 0.917), six grades 0.297 (QWK 0.497), score R² 0.340 (B1 best in all three = M0).',
                'Spectra only with B2 (M1): 0.731, 0.369, R² 0.442. Spectra + covariates with B2 (M2): 0.783, 0.400, R² 0.462.'],
         means='The calendar alone detects disease inside unsprayed plots as well as the spectra, because healthy leaves there occurred almost only on the first date. For grades and score the spectra are clearly better.',
         say='"Without a sensor, the calendar already detects disease; for severity the spectra are better."')
    fig('covmod', 'f32_cov_models.png', 'Primary metric of the three models on covariates only, leaf spectra and spectra + covariates (unsprayed, naturally infected leaves; M0 marked).', rep=32)
    read(shows='The same results as bars.', how='Grey = interpretable model, green = random forest, purple = best ML model; M0 marks the baseline.',
         found='Spectra (middle group) beat covariates (left group) for six grades and score; spectra + covariates (right group) are highest.',
         say='"Spectra beat the calendar for severity, and combining both is best."')
    tab('covgain', 35, widths=[1300, 1700, 2200, 2200, 2200], size=16)
    read(shows='Each gain with its 95% plot-bootstrap interval.',
         how='✓ = interval excludes zero (real gain); ✗ = real loss. For RMSE a negative value is a gain.',
         found=['ΔS (spectra over calendar): six grades macro-F1 +0.072 (+0.028 to +0.119) ✓, QWK +0.101 ✓; score R² +0.102 (+0.005 to +0.193) ✓; detection macro-F1 −0.003 (no difference), balanced accuracy −0.056 ✗.',
                'ΔC (calendar added to spectra): only the score gains (R² +0.020 ✓). ΔT (both over calendar): six grades +0.103 ✓, score R² +0.122 ✓.'],
         means='The spectra see severity that the calendar cannot: leaves of the same date, timing and stage differ in their real infection. For detection inside unsprayed plots the date already tells healthy from diseased.',
         caution='Inside unsprayed plots only 44 of the 573 test leaves are grade 0, so detection there is a small and date-driven problem; with the sprayed plots included the spectra detected disease with macro-F1 0.83 (Step 11).',
         say='"Beyond the calendar, the spectra add 0.07 macro-F1 for grades and 0.10 R² for the score – both real gains."')
    fig('covgain', 'f33_cov_gains.png', 'Gains of the spectra (ΔS), of the covariates added to the spectra (ΔC) and of both (ΔT) with 95% plot-block bootstrap intervals (filled = real difference; right of zero = better, except RMSE).', rep=33)
    read(shows='The gains as points with intervals.', how='Blue = ΔS, orange = ΔC, purple = ΔT; filled = interval excludes zero.',
         found='Filled points lie right of zero for six grades and the score; detection points straddle zero.',
         say='"For severity the intervals lie clearly above zero."')
    fig('covb1', 'f34_cov_b1.png', 'Standardised effects of the covariates in the interpretable models: logistic (detection), ordinal logistic (six grades) and linear (score) (95% CI).', rep=34)
    read(shows='The size and direction of each covariate effect in B1 (fitted on all unsprayed leaves, descriptive).',
         how='Each point = effect of a one-SD change (or of a level vs its reference) with 95% interval; red raises disease, blue lowers it.',
         found='Six grades: DAS +2.77 per SD (95% CI +2.45 to +3.08), DAS² −0.38, timing D4 +1.73 and D3 +0.83 vs D1, stage −0.66, variety V3 −0.28.',
         means='At the same crop age the late sowings had more disease: they were young when the favourable December–January weather came. Crop age is by far the strongest covariate.',
         say='"Crop age dominates; at the same age, the late sowings were more diseased."')

    # ---------------------------------------------------------------- Step 15
    h2('9.2 Step 15 – Comparison with LORO: does 70:30 improve the accuracy?')
    p('The earlier analysis used leave-one-replication-out (LORO) validation. The 70:30 numbers are mostly higher. Step 15 asks whether that is a real improvement or the luck of which '
      'plots were tested. It answers with four checks, each removing one possible explanation.')
    card('card15', '15', 'Comparison of the 70:30 hold-out with LORO',
         'Decide whether the higher 70:30 accuracy reflects the design or the particular test plots.',
         '(1) and (2): the 699 TEST leaves – 70:30 predictions and the LORO predictions of the same leaves (every leaf was tested once in LORO). (3): ALL leaves divided by LORO, the main split and 20 other grouped 70:30 splits. (4): ALL leaves divided by 5 random leaf-level 70:30 splits.',
         'Predictions of both designs; the split rules of Step 5.',
         steps('Side by side: every metric of every model under LORO (pooled over 2330 leaves) and 70:30 (699 leaves).',
               'Same test leaves (paired): for each model take the LORO predictions of exactly the 699 test leaves; difference 70:30 − LORO; 2000 resamples of whole test plots (healthy and unsprayed separately); "higher/lower" only when the 95% interval excludes zero.',
               'Repeated splits: draw 20 other rule-conforming grouped 70:30 splits (split_lib.random_splits, seed 7, candidates with score ≤ the median); run a light pipeline (selection on the training part with SHAP-CARS 10 runs, then SVM for A, RF for B, XGBoost for C with grid search in GroupKFold(3), no SFFS) under LORO, the main split and each of the 20 splits; compare each split with the LORO predictions of its own test leaves.',
               'Leakage check: 5 random leaf-level 70:30 splits stratified by grade (inner folds also by leaf); same light pipeline; compare with the grouped splits.'),
         'Bootstrap 2000 resamples (seed 11); light pipeline seeds 42 + run; leaf splits random_state 100–104.',
         'Report Tables 36–42, Figures 35–38 → answer "only partly".',
         'splitcmp/c2_compare.py (side by side, paired, figures); asd7030/c1_repeat.py (repeated and leaf-level splits) → cmp_*.csv.',
         'Kohavi (1995); Vabalas et al. (2019); Xu and Goodacre (2018); Dietterich (1998); Field and Welsh (2007); Roberts et al. (2017); Kattenborn et al. (2022).',
         '53–60; appendix 113–124',
         'Repeat the same four checks whenever a single hold-out is reported; they cost only the light pipeline runs.')
    tab('cmpcard', 36, widths=[2200, 7400], size=17, boldfirst=True)
    read(why='A hold-out estimate depends on which plots are in the test set; with 15 test plots its variance is large (Kohavi, 1995; Vabalas et al., 2019).',
         means='A higher 70:30 number counts as an improvement only if it holds on the same leaves and across other 70:30 splits.',
         say='"I compared the designs in four ways so that luck could not pass for improvement."')
    tab('splittypes', 37, widths=[2200, 3400, 4000], size=16)
    read(shows='How published plant-disease studies divide their data.',
         found='Most studies split images or leaves at random (80:20 or 70:30). Grouped or blocked splits are recommended for dependent samples; random hold-outs over-estimated accuracy by up to 28% against spatial blocks (Kattenborn et al., 2022). The PlantVillage model fell from 99.35% on a random hold-out to 31.4% on images taken under other conditions (Mohanty et al., 2016).',
         means='Our 70:30 split is the stricter, grouped kind, and LORO is grouped cross-validation. Both are more conservative than the random splits common in the literature.',
         say='"Most papers split leaves at random; I split whole plots, which is stricter."')
    tab('cmpside', 38, widths=[500, 1800, 700, 1100, 1800, 1900, 1800], size=15)
    read(shows='Main metric of every model under LORO (all 2330 leaves) and 70:30 (699 test leaves).',
         found='20 of 30 results were higher with 70:30; mean difference +0.030 (detection), −0.001 (six grades), +0.019 R² (score).',
         means='These raw numbers mix the effect of the design with the fact that different leaves are tested; they cannot answer the question alone.',
         say='"Side by side, 70:30 looks a little better, but the two numbers are measured on different leaves."')
    fig('cmpside', 'f36_cmp_side.png', 'Main metric of every model under LORO (grey) and the 70:30 split (colour).', rep=35)
    read(shows='The side-by-side numbers as paired bars.', how='Grey = LORO; colour = 70:30.',
         found='Detection and score bars are mostly higher with 70:30; six-grade bars are mixed.', say='"Higher for detection and score, mixed for grades."')
    tab('cmppair', 39, widths=[500, 1800, 1000, 1400, 1000, 1200, 1800, 900], size=15)
    read(shows='The fair comparison: both designs scored on exactly the same 699 test leaves.',
         how='"LORO on the same leaves" = the LORO predictions of the 70:30 test leaves; verdict "higher" only when the 95% plot-bootstrap interval excludes zero.',
         found=['17 of 30 comparisons really higher with 70:30, 0 really lower, 13 not different.',
                'Detection: 9 of 10 models higher (e.g. SVM 0.710 → 0.826); six grades: only k-NN higher; score: 7 of 10 higher.'],
         means='On these leaves the 70:30 models are genuinely better than the LORO models. Step (3) checks whether this holds for other test plots.',
         say='"On the same leaves 70:30 was better in 17 of 30 comparisons and never worse."')
    tab('blocktype', 40, widths=[700, 1700, 900, 900, 1800, 1200, 1300], size=16)
    read(shows='Where the paired gain comes from: healthy vs unsprayed test plots (mean of the ten models).',
         found='Detection OA rose 0.648 → 0.754 on the healthy test plots and 0.780 → 0.865 on the unsprayed ones; the score RMSE fell most on the healthy plots (2.06 → 1.73).',
         means='The healthy test plots (1, 4, 5, 8) are the same plots that LORO fold 2 tested, so the healthy training plots were identical in both designs. The difference lies in the unsprayed training plots: in the 70:30 split they come from all three replications, so every unsprayed test plot has training plots of its own replication; in LORO the whole replication of the test plot is missing from training.',
         say='"The 70:30 models have seen other plots of the same replication; LORO has not – that explains much of the gain."')
    box('What the paired gain means.', 'A plot hold-out asks: "does the model work on a new plot of a replication it has seen?" LORO asks: "does it work on a replication it has never seen?" '
        'Plots of one replication share conditions (position in the field, soil, management timing), so the plot hold-out is the easier question. Both are free of leaf-level leakage; LORO is the '
        'stricter test of generalisation to a new block, the 70:30 split the closer match to applying the models within the same field and season (Roberts et al., 2017).', kind='key')
    fig('cmppair', 'f37_cmp_paired.png', 'Difference 70:30 − LORO on the same test leaves with 95% plot-bootstrap intervals (right of zero = better with 70:30; for RMSE left of zero is better).', rep=36)
    read(shows='Each paired difference with its interval.', how='Green = really higher with 70:30; red = really lower; grey = interval includes zero.',
         found='Detection: green for all models except EfficientNet-B0. Six grades: grey except k-NN. Score: green except PLSR, EfficientNet-B0 and ConvNeXt V2-Atto. No red point.',
         say='"Green for detection and score, grey for six grades, never red."')
    tab('repeat', 41, widths=[500, 900, 1300, 1100, 2100, 1100, 1300, 1300], size=15)
    read(shows='The light pipeline under LORO, the main 70:30 split and 20 other 70:30 splits.',
         how='"Above LORO (all leaves)" compares each split\'s test value with the LORO value; "same leaves" compares each split with the LORO predictions of exactly its test leaves.',
         found=['Over 20 other splits macro-F1 ranged 0.770–0.863 (detection), 0.328–0.413 (six grades) and R² 0.392–0.547 (score); means 0.807, 0.370, 0.478, close to LORO (0.796, 0.358, 0.476).',
                'On the same leaves the 70:30 models beat LORO in 10, 12 and 4 of 20 splits (26 of 60 = 43%).',
                'The main split (0.848, 0.399, 0.510) lies near the top of the range for detection and six grades.'],
         means='The main 70:30 split was a favourable draw. Averaged over many splits, 70:30 and LORO give practically the same accuracy.',
         say='"Over 20 other splits, 70:30 and LORO are equal on average; my main split happened to be a favourable one."')
    fig('cmprep', 'f38_cmp_repeat.png', 'Test accuracy of the light pipeline over 20 grouped 70:30 splits (dots, box) compared with LORO (dashed line) and the main 70:30 split (diamond).', rep=37)
    read(shows='The spread of hold-out accuracy over 20 possible 70:30 splits.', how='Dots = the 20 splits; box = middle half; dashed line = LORO; diamond = main split.',
         found='The detection range spans about 0.09 macro-F1; the LORO line lies inside the box (detection, score) or at its lower edge (six grades); the diamond lies in the upper part.',
         means='One 70:30 split can land anywhere in this range just by which plots are tested. This is the strongest reason to report the range, not one number.',
         say='"The accuracy of a single split can move by almost 0.1 just by drawing other test plots."')
    tab('leak', 42, widths=[700, 1100, 2700, 2700, 2400], size=16)
    read(shows='Grouped (whole plots) vs random leaf-level 70:30 splits with the same light pipeline.',
         found='Leaf-level splits gave macro-F1 0.815 and 0.425 and R² 0.504, against 0.807, 0.370 and 0.478 for grouped splits: inflation +0.008, +0.055, +0.026.',
         means='Putting leaves of the same plot in training and test makes the models look better, most of all for six grades (+15% relative). This confirms that the grouped split was necessary (Roberts et al., 2017).',
         say='"A random leaf split would have inflated six-grade accuracy by 0.055 – that is leakage."')
    fig('cmpleak', 'f39_cmp_leak.png', 'Grouped vs random leaf-level 70:30 splits: leaf-level splits look better only because leaves of the same plot are in training and test.', rep=38)
    read(shows='The leakage check as bars.', found='Leaf-level bars are higher for every task.', say='"Leaf-level splitting flatters the models."')
    box('Answer of Step 15 – how to say it to the chairman.', [
        '"On the same 699 test leaves the 70:30 models were really better than LORO in 17 of 30 comparisons and never worse. Part of this comes from training plots of the same replication, '
        'and part from a favourable draw of test plots: over 20 other 70:30 splits the two designs are equal on average."',
        '"I therefore present the 70:30 models as the deployable models, with their test accuracy and the range from the repeated splits, and I keep LORO as the stricter estimate. '
        'The decisive test is the independent 2026-27 season and the Bharatpur site."'], kind='present')
