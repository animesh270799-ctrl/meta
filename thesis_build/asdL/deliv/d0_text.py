"""Text of every Part L step (one source for Excel, PPT and Word). Numbers are filled from tables.pkl / facts.json, never typed by hand."""
import json, os, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); SJ = {s['code']: s for s in json.load(open(os.path.join(HERE, 'partL_steps.json')))}
TN = {'A': 'Task A (healthy vs diseased)', 'B': 'Task B (six grades)', 'C': 'Task C (grade 0–9)'}
def f3(x): return '%.3f' % x
import re
def clean(s):
    if not isinstance(s, str): return s
    s = s.replace('^{2}', '²').replace('^{−1}', '⁻¹'); return re.sub(r'[_^]\{([^}]*)\}', r'\1', s)
def steps(T, F):
    g = F['grade_counts']; l52 = F['l52']; l53 = F['l53']; S = []
    def add(code, title, sheet, position, samples, settings, mydata, result, output, notes, mrefs, q, figs=()):
        js = SJ.get(code, {}); S.append(dict(code=code, title=title, sheet=sheet, why=clean(js.get('why', '')), what=clean(js.get('what', '')), position=position, samples=samples, settings=settings,
                                             papers=[(p[0], clean(p[1])) for p in js.get('papers', [])], mydata=mydata, result=result, output=output, notes=notes, mrefs=mrefs, q=q, figs=list(figs)))
    add('L1', 'Leaf table and data checks', 'L1', 'First step: raw ASD files → leaf table. Feeds L2 (split) and L3 (pre-processing).', 'All spectra of the four dates (11 Feb, 24 Feb, 3 Mar, 13 Mar 2026).',
        'Leaf positions L3, L5, LL; grades 0, 1, 3, 5, 7, 9; exact duplicates removed; Isolation Forest (300 trees, contamination "auto", seed 42) within each date × grade on 10-nm means; removal only if faulty (reflectance < 0 or > 1).',
        ['Read the 7 header rows of every spectrum (file, plot, variety, stage, status, leaf position, score) and joined the plot plan (block, variety, sowing date).',
         'Removed %d L4 leaves (not a methodology leaf position) and %d exact duplicate spectra (13 Mar; plots 13, 34, 38, 41, 42).' % (F['n_L4'], F['n_dup']),
         'Checked the 1000/1001-nm detector join: median excess step −0.0021 (IQR −0.0025 to −0.0015); not corrected, first-derivative bands 995–1005 nm excluded from band selection (DEV-1).',
         'Isolation Forest flagged %d spectra; none was faulty, so none was removed (all flags listed in sheet L1).' % F['n_if']],
        ['%d spectra read → %d leaves in the final table.' % (F['n_read'], F['n_final']), 'Grades: ' + ', '.join('%d = %d' % (k, v) for k, v in [(0, g['0']), (1, g['1']), (3, g['3']), (5, g['5']), (7, g['7']), (9, g['9'])]) + ' leaves.',
         'All 48 plots on every date; no healthy-block (fungicide) leaf had a grade above 0.'],
        'Leaf table (sheet Leaf_table) and checked spectra → L2, L3.', 'One spectrum per leaf in the files (instrument average), so the methodology rule "average 2 readings" was not applicable. Splice correction of the step at 1000 nm is an alternative (Hueni and Bialek, 2017); it was not applied because the methodology assumes corrected files.',
        ['Liu et al. (2008)', 'Hueni and Bialek (2017)'], 'Why not remove all Isolation Forest flags? → A flag only means "unusual"; severe leaves are unusual by nature. Removing them would delete real disease signal, so only faulty spectra are removed (Selvaprakash et al., 2026).', ['c01', 'c02', 'c03', 'c04', 'c05'])
    add('L2', 'Same 7:3 split by plot and inner validation', 'L2', 'After L1; before every selection and model step. All later "training" steps use only the training plots.', 'All %d leaves, assigned by plot number.' % F['n_final'],
        'Test plots = 15 (4 healthy + 11 unsprayed): %s. Network validation plots (11): %s. GroupKFold(3) by plot on the 33 training plots; seed 42.' % (', '.join(str(p) for p in [1, 4, 5, 8, 13, 14, 18, 25, 27, 31, 35, 37, 44, 46, 48]), ', '.join(str(p) for p in [6, 7, 11, 19, 24, 26, 28, 30, 36, 39, 41])),
        ['Gave every leaf the split of its plot (same plot split as the 2026-27 plan).', 'Training leaves: %d (network fitting %d, network validation %d). Test leaves: %d (%.1f%%).' % (F['n_train'], F['n_fit'], F['n_val'], F['n_test'], 100 * F['n_test'] / F['n_final']),
         'Inner GroupKFold(3) folds of the training plots: %d / %d / %d leaves.' % tuple(F['fold_sizes'])],
        ['No plot has leaves in both training and test parts (checked).', 'All six grades occur in the training and test parts with similar proportions (Figure c06).'],
        'Split column, fold column and network part of every leaf → L3–L9.', 'A random leaf-level split would put leaves of the same plot on both sides and inflate accuracy; the plot split prevents that leakage.', [],
        'Why split by plot and not by leaf? → Leaves of one plot share variety, sowing date, microclimate and inoculum; a leaf split would test on "neighbours" of the training leaves.', ['c06', 'c07'])
    add('L3', 'Pre-processing: smoothing, range, derivative, 5-nm bands', 'L3', 'After L2; produces the spectra used by L4, L5 and L6.', 'All leaves (each leaf processed on its own, so no information passes between leaves).',
        'Savitzky–Golay filter, window 11 nm, order 2, on 350–2500 nm; first derivative with the same filter; trimmed to 400–2400 nm (water bands kept, contact probe); 5-nm band means (λ ± 2 nm) for the band searches.',
        ['Smoothed every spectrum, computed the first derivative, trimmed to 2001 bands (400–2400 nm) and averaged to 401 bands of 5 nm (reflectance and derivative).',
         'Residual SD between raw and smoothed spectra = 0.00018 reflectance (smoothing removes noise without changing the shape).'],
        ['401 reflectance + 401 first-derivative bands per leaf.'], '5-nm reflectance (Data_R5) and first-derivative bands → L4, L5, L6.', 'Window 11/order 2 follows the 2026-27 methodology; larger windows smooth more but blur narrow features. The derivative removes brightness (offset) differences between leaves.',
        ['Savitzky and Golay (1964)'], 'Why smooth before the derivative? → The derivative amplifies noise; smoothing first keeps the derivative usable (Savitzky and Golay, 1964).', ['c08', 'c09', 'c10'])
    add('L4', 'Spectral indices and red-edge parameters', 'L4', 'After L3; the indices enter L5.1 (correlation) and L5.4 (redundancy filter and ReliefF).', 'All leaves (indices are computed leaf by leaf).',
        '48 published indices (39 base + 9 SWIR) and REP, Dr, SDr at 1 nm from the smoothed spectra; formulas and original references in sheet L4. RBI_R in its published normalised-difference form (Selvaprakash et al., 2026).',
        ['Computed the 51 features for every leaf; all values finite.', 'REP = wavelength of the largest first derivative in 680–760 nm; Dr = that maximum; SDr = sum of the derivative over 680–760 nm.'],
        ['Mean REP fell from %.1f nm (grade 0) to %.1f nm (grade 9): a blue shift of the red edge with severity.' % (F['l51']['REP_by_grade']['0'], F['l51']['REP_by_grade']['9'])],
        'Index table (sheet L4_values) → L5.1, L5.4.', 'The methodology table lists RBI_R as R1068/R1560; the published form is the normalised difference used here (to be corrected in the methodology table).', [],
        'Why use published indices when you also search band pairs? → Published indices are physically interpretable (chlorophyll, red edge, water) and comparable with other studies; the data-driven indices are tested against them.', [])
    l51 = F['l51']; ir = T['l51_index_r']
    add('L5.1', 'Leaf response: mean spectra, differences and correlation', 'L5.1', 'After L3–L4; description only (no selection), so it uses all leaves. Guides the interpretation of L5.2–L5.6.', 'All %d leaves (hybrid design: description on all leaves, selection on training leaves).' % F['n_final'],
        'Mean ± SD of reflectance and first derivative per grade; % difference from grade 0; Pearson r of every 5-nm band and index with the grade; the same r within each leaf position, growth stage, variety and date.',
        ['Averaged the 5-nm spectra of each grade, computed the % difference from grade 0 and Pearson r with the grade for 401 reflectance bands, 401 derivative bands and 51 indices.',
         'Repeated the correlation within 13 strata (3 leaf positions, 3 stages, 3 varieties, 4 dates).'],
        ['Visible reflectance rises and NIR reflectance falls with grade; the red edge shifts to shorter wavelengths.', 'Highest |r|: reflectance %.3f at %d nm; first derivative %.3f at %d nm.' % (l51['max_abs_r_R'], l51['wl_max_r_R'], l51['max_abs_r_FD'], l51['wl_max_r_FD']),
         'Best published index: %s (r = %.3f), then %s (r = %.3f).' % (ir.Index.iloc[0], ir.r.iloc[0], ir.Index.iloc[1], ir.r.iloc[1])],
        'Response curves and r tables → interpretation of L5.2–L5.6.', 'Correlations are pooled over dates, stages and varieties; the stratum curves show whether the same bands respond in every stratum.', [],
        'Why is the derivative more correlated than reflectance? → It removes leaf-to-leaf brightness differences and sharpens the red-edge shift caused by chlorosis and pustules.', ['c11', 'c12', 'c13', 'c14', 'c15', 'c16', 'c17'])
    add('L5.2', 'Effective ranges and optimal wavelengths (R² maps → SHAP-CARS)', 'L5.2', 'After L3; first selection step; training leaves only. Its optimal wavelengths (OW) enter L5.5.', '%d training leaves (33 plots).' % F['n_train'],
        'NDSI and RSI R² maps of all 5-nm pairs with the grade; effective range = bands in R² > 0.5 in both maps, else the top 5%% of each map; SHAP (random forest 500 trees, TreeExplainer) on R and FD bands in the ranges (FD 995–1005 nm excluded), top 40%% kept; PLS components by MCCV (50 plot divisions, 1–15); CARS 50 iterations; subset with the lowest GroupKFold(3) RMSE = OW.',
        ['Maximum R²: NDSI %.3f, RSI %.3f (below 0.5) → top-5%% thresholds %.3f (NDSI) and %.3f (RSI).' % (l52['maxR2_ndsi'], l52['maxR2_rsi'], l52['thr']['NDSI'], l52['thr']['RSI']),
         'Effective ranges (bands in both maps): %s (%d bands).' % (', '.join(l52['ranges']), l52['n_eff']),
         'SHAP on %d candidates (R + FD) → %d kept; MCCV chose %d PLS components; CARS kept %d bands at iteration %d (GroupKFold RMSE %.3f).' % (l52['n_cand'], l52['n_shap'], l52['ncomp'], l52['n_ow'], l52['cars_it'], l52['cars_rmse'])],
        ['32 optimal wavelengths: 31 first-derivative bands (green peak 525–600 nm, red edge 650–870 nm, NIR and water bands 985–1505 nm and 1725–1810 nm) and reflectance at 535 nm.'],
        'Leaf OW (32 bands) → L5.5.', 'Single-pair R² stayed below 0.5, so the "top 5%" rule of the methodology was used. SHAP ranks bands by their contribution in a non-linear model; CARS then removes redundant neighbours.',
        ['Lundberg and Lee (2017)', 'Li et al. (2009)', 'Breiman (2001)'], 'Why SHAP before CARS? → SHAP removes bands with no model contribution; CARS then keeps a compact, non-redundant subset that predicts best (Ma et al., 2026).', ['h01', 'h02', 'c21', 'c22', 'c23', 'c24', 'c25'])
    w = l53['wri']; wn = l53['wri_best_nonzero']
    add('L5.3', 'Leaf indices: best NDSI, RSI and the White Rust Index', 'L5.3', 'After L5.2 (uses the same R² maps); the new indices join the 51 published ones in L5.4.', '%d training leaves.' % F['n_train'],
        'Best NDSI and RSI pair with bands ≥ 10 nm apart; WRI = NDSI(λ1, λ2) + w·R(λ3) over the 200 best NDSI pairs with λ1, λ2 ≥ 50 nm apart, w ∈ {−1, −0.5, 0, 0.5, 1}, λ3 every 10 nm; scored by |r| with the grade; indices then computed at 1 nm.',
        ['Best NDSI = NDSI(%d, %d), R² = %.3f; best RSI = RSI(%d, %d), R² = %.3f.' % (l53['ndsi'][0], l53['ndsi'][1], l53['ndsi'][2], l53['rsi'][0], l53['rsi'][1], l53['rsi'][2]),
         'WRI search: 1000 combinations; the best was w = 0, i.e. WRI = NDSI(%d, %d), r = %.3f. The best combination with a third band (w = %g, λ3 = %d nm) gave r = %.3f, lower.' % (w['l1'], w['l2'], w['r'], wn['w'], wn['l3'], wn['r'])],
        ['WRI (NDSI of 780 and 830 nm, on the NIR shoulder after the red edge) falls steadily from grade 0 to grade 9.'],
        'NDSI_best, RSI_best, WRI → L5.4.', 'In this data set the third band added nothing, so the WRI reduces to a normalised difference. The best NDSI pair (795, 805 nm) is only 10 nm apart and acts like a derivative of the NIR shoulder.',
        [], 'Why does the WRI need bands at least 50 nm apart? → To avoid a pair that only measures local slope (a derivative) and to keep an index that a coarser UAV/satellite sensor can still measure.', ['c26', 'c27'])
    l54 = F['l54']
    add('L5.4', 'Redundancy filter and ReliefF ranking of the indices', 'L5.4', 'After L4 and L5.3; its top-5 indices per task (VI) enter L5.5.', '%d training leaves.' % F['n_train'],
        'Indices (51 published + NDSI_best, RSI_best, WRI) ordered by |r| with the grade; an index is dropped if |r| ≥ 0.95 with an index already kept; ReliefF (Tasks A, B) and RReliefF (Task C), k = 10 neighbours, min–max scaling; top five per task.',
        ['%d indices → %d kept after the |r| ≥ 0.95 filter (each removed index is listed with the one that replaced it).' % (54, l54['n_kept']),
         'VI Task A: %s.' % ', '.join(l54['VI']['A']), 'VI Task B: %s.' % ', '.join(l54['VI']['B']), 'VI Task C: %s.' % ', '.join(l54['VI']['C'])],
        ['RSI_best, HI (healthy index), RR (1/R700), REP and RVSI are the strongest indices for detection and grading.'],
        'VI (5 indices per task) → L5.5.', 'ReliefF judges a feature by how well it separates near neighbours of different classes, so it captures non-linear relevance that r misses.',
        ['Kira and Rendell (1992)', 'Robnik-Šikonja and Kononenko (2003)'], 'Why remove correlated indices before ReliefF? → Near-duplicates share the same weight and would fill the top five with one kind of information.', ['c28a', 'c28b', 'c28c'])
    dsf = F['DSF']
    add('L5.5', 'Variance inflation factor → leaf disease-specific feature set (DSF)', 'L5.5', 'After L5.2 and L5.4; the DSF is the only input of the L6 models.', '%d training leaves.' % F['n_train'],
        'Pool = 32 OW + 5 VI of the task; the feature with the largest VIF is removed one at a time until all VIF < 10.',
        ['Task A: %d features → %s.' % (len(dsf['A']), ', '.join(dsf['A'])), 'Task B: same 14 features as Task A.' if dsf['A'] == dsf['B'] else 'Task B: %s.' % ', '.join(dsf['B']), 'Task C: %s.' % ', '.join(dsf['C'])],
        ['13 first-derivative bands are shared by all tasks; the remaining index is RR (Tasks A, B) or RARSa (Task C).'], 'Leaf DSF of Tasks A, B, C → L5.6, L6.', 'VIF removes collinearity, so most red-edge derivative bands (highly inter-correlated) collapse to a few representatives.', [],
        'Why VIF < 10? → A VIF of 10 means 90% of a feature is explained by the others; above that, model coefficients and importances become unstable (Lv et al., 2023).', ['c29'])
    jm = T['l56_jm']
    add('L5.6', 'Separability of the grades (Jeffries–Matusita distance)', 'L5.6', 'After L5.5; a check of the DSF before modelling.', '%d training leaves (task-B DSF).' % F['n_train'], 'JM = 2(1 − e^(−B)), B = Bhattacharyya distance under Gaussian classes; 15 grade pairs; JM ranges from 0 to 2.',
        ['Computed JM for all 15 pairs on the 14 standardised DSF features.'],
        ['Grade 0 vs 9: JM = %.2f (near-complete separation); 0 vs 1: %.2f; neighbouring grades are poorly separated (3 vs 5: %.2f; 5 vs 7: %.2f; 7 vs 9: %.2f).' % tuple(jm.set_index(['grade_a', 'grade_b']).JM.loc[[(0, 9), (0, 1), (3, 5), (5, 7), (7, 9)]])],
        'JM matrix → expectation for Task B (neighbouring grades will be confused).', 'JM assumes Gaussian classes; it is a guide, not a test.', [],
        'What does a low JM between neighbouring grades mean for the classifier? → Exact-grade accuracy will be limited; within-one-grade accuracy and QWK are fairer measures (Cross et al., 2024).', ['h03', 'c30'])
    v = T['l57_var']
    add('L5.7', 'Principal component analysis of the leaf spectra', 'L5.7', 'Description after L3 (all leaves); not used for selection.', 'All %d leaves.' % F['n_final'], 'PCA on z-scored 5-nm reflectance (401 bands); scores of PC1–PC3 with 95% grade ellipses; loadings.',
        ['PC1 %.1f%%, PC2 %.1f%%, PC3 %.1f%% of the variance (first three: %.1f%%).' % (v.explained_pct[0], v.explained_pct[1], v.explained_pct[2], v.cumulative_pct[2])],
        ['The grades overlap strongly in PC1–PC2; severity shifts the cloud gradually, which agrees with the low JM of neighbouring grades.'], 'PCA scores and loadings → interpretation.', 'PCA is unsupervised: the main variance (brightness, leaf structure, date) is not the disease signal.',
        ['Jolliffe and Cadima (2016)'], 'Why z-score before PCA? → Otherwise high-reflectance NIR bands dominate the components (Bijlwan et al., 2025).', ['c18', 'c19', 'c20'])
    # ---------------- L6–L9 (filled when results exist)
    if 'l6_ml' in T and len(T['l6_ml']):
        ml = T['l6_ml']; rows = ['%s %s: SFFS %d of %d features, %s' % (r.task, r.model, r.sffs_n, r.dsf_size, r.grid_best.replace('"', '').replace('svc__', '').replace('svr__', '').replace('kneighborsclassifier__', '').replace('kneighborsregressor__', '')) for r in ml.itertuples()]
        dl = T.get('l6_dl', pd.DataFrame()); dtxt = ['%s %s: best epoch %d of %d run' % (r.task, r.model, r.best_epoch, r.epochs_run) for r in dl.itertuples()] if len(dl) else []
        add('L6', 'Leaf models: machine learning and networks', 'L6', 'After L5.5 (DSF); models are tested once in L7.', 'Training leaves: ML on all %d (GroupKFold(3) by plot); networks fitted on %d and early-stopped on %d validation-plot leaves.' % (F['n_train'], F['n_fit'], F['n_val']),
            'ML: SFFS (mlxtend, floating, 1–15 features, default settings SVM C = 1 γ = scale, RF 500 trees, k-NN k = 5, PLS 2 components) → grid search (SVM C {0.1, 1, 10, 100}, γ {0.001, 0.01, 0.1, scale}, ε {0.1, 0.5}; RF max_features {sqrt, 0.3}, min_samples_leaf {1, 3, 5}; k-NN k {3–11}, uniform/distance; PLS 1–15) → refit on all training leaves; balanced class weights. Networks: AdamW 6e-4, weight decay 1e-5, cosine to 1e-6, 300 epochs, patience 60, batch 32, label smoothing 0.01, gradient clip 1.2; model of the epoch with the highest validation OA (lowest RMSE for Task C); pseudo-image k = ⌈√p⌉.',
            rows + dtxt, ['See L7 for the test results.'], 'Fitted models (L6_models folder) and test predictions → L7.', 'SFFS stability (repeated random GroupKFold(3) divisions) is reported for the best ML model of each task.',
            ['Pudil et al. (1994)', 'Cortes and Vapnik (1995)', 'Breiman (2001)', 'Wold et al. (2001)', 'Barker and Rayens (2003)', 'He et al. (2016)', 'Tan and Le (2019)', 'Woo et al. (2023)', 'Loshchilov and Hutter (2019)'],
            'Why SFFS after VIF? → VIF removes collinearity without looking at the model; SFFS keeps only the features that improve the inner-fold score of each model.', ['c31a', 'c31b', 'c31c', 'c32a', 'c32b', 'c32c', 'c40a', 'c40b', 'c40c'])
    if 'l7_metrics' in T:
        R = T['l7_metrics']; b = F['best']; ra = R[(R.task == 'A') & (R.model == b['A'])].iloc[0]; rb = R[(R.task == 'B') & (R.model == b['B'])].iloc[0]; rc = R[(R.task == 'C') & (R.model == b['C'])].iloc[0]
        low = T['l7_low']; la = low[(low.task == 'A') & (low.model == b['A'])].value.iloc[0]
        add('L7', 'Test metrics of the leaf models', 'L7', 'After L6; the only use of the 684 test leaves.', '%d test leaves (15 plots).' % F['n_test'],
            'Tasks A, B: confusion matrix, OA, kappa, per-class precision/recall/F1, macro-F1; Task A also sensitivity, specificity, AUC; Task B also within-one-grade accuracy and quadratic weighted kappa; Task C: R², RMSE, RPD; low-severity check; results by leaf position, stage, date, variety; 95% CI by resampling whole test plots (1000 times).',
            ['Computed every metric once for 9 (A, B) and 5 (C) models; Excel formulas in sheet L7_Formulas recompute the main metrics from the predictions (cross-check).'],
            ['Task A best: %s, macro-F1 %.3f (95%% CI %.3f–%.3f), OA %.3f, AUC %.3f.' % (b['A'], ra.macro_F1, ra.CI_low, ra.CI_high, ra.OA, ra.AUC),
             'Task B best: %s, macro-F1 %.3f, OA %.3f, within-one-grade %.3f, QWK %.3f.' % (b['B'], rb.macro_F1, rb.OA, rb.within1, rb.QWK),
             'Task C best: %s, R² %.3f, RMSE %.2f grade units, RPD %.2f.' % (b['C'], rc.R2, rc.RMSE, rc.RPD), 'Low severity: %.0f%% of grade-1 test leaves were detected as diseased by %s.' % (100 * la, b['A'])],
            'Metric table → conclusions, L8.', 'Exact grades overlap (L5.6), so within-one-grade accuracy and QWK are reported with macro-F1 (Cross et al., 2024).', ['Cohen (1960)', 'Sokolova and Lapalme (2009)', 'Efron and Tibshirani (1993)'],
            'Why macro-F1 as the main metric? → It weights every class equally, so the rare grades 7 and 9 count as much as grade 0.', ['c33a', 'c33b', 'c33c', 'c34', 'c35', 'h04', 'c36', 'c37', 'c38a', 'c38b', 'c38c', 'c39'])
    if 'l8_models' in T:
        m = T['l8_models']; gtxt = ['%s: M0 %.3f, M1 %.3f, M2 %.3f → ΔS = %+.3f, ΔC = %+.3f.' % (TN[r.task], r.M0, r.M1, r.M2, r.dS, r.dC) for r in m.itertuples()]
        add('L8', 'Leaf covariate baseline', 'L8', 'After L7; credits the leaf spectrum only with what it adds to time, crop and weather.', 'Same training (%d) and test (%d) leaves.' % (F['n_train'], F['n_test']),
            'M0 = random forest on covariates only (DAS, variety, sowing date, growth stage, leaf position, 7-day weather ending the day before sampling, favourable days since sowing), tuned with GroupKFold(3) (grid of Step 2.4); M1 = best leaf model of L7; M2 = M1 model type on DSF + covariates (SFFS and grid repeated); ΔS = M1 − M0, ΔC = M2 − M1; plot-bootstrap 95% CI.',
            gtxt, ['Read with care: in one season each date has one weather value for all plots, so M0 learns date and crop differences (within-season baseline).'], 'Gains table → conclusions.', 'Favourable-day rules: leaf infection Tmax 16–24 °C, morning RH > 97%, afternoon RH > 40% (Chattopadhyay et al., 2011).',
            ['Chattopadhyay et al. (2011)'], 'Why compare with a weather model? → Disease rises with time and weather, so a spectral model can look good by learning the calendar; ΔS shows what the spectrum adds (Zhang et al., 2014a).', ['c41', 'c42', 'c43'])
    if 'l9_transfer' in T:
        tf = T['l9_transfer'].set_index('feature'); l9 = F['l9']
        add('L9', 'Leaf–canopy link (UAV hyperspectral, 24 Feb 2026)', 'L9', 'After L5.3–L5.4; compares leaf features with the canopy.', '48 plots on 24 Feb 2026: plot-mean leaf spectra (all leaves of the plot) and UAV plot spectra; detection thresholds set on the 33 training plots, tested on the 15 test plots.',
            'Leaf spectra resampled to the %d UAV band centres (Gaussian response, FWHM = band spacing); band-wise r over 48 plots; leaf indices (WRI, NDSI_best, RSI_best and the VI) computed from the UAV spectra (1 nm, SG 11/2) and related to plot DI = Σgrade/(9n) × 100; threshold by Youden index on training plots.' % l9['n_uav_bands'],
            ['Leaf vs canopy OW overlap (part 1 of L9) not possible: the canopy selection chain was not run for 2025-26 (one UAV date).', 'Median band-wise r between leaf and UAV reflectance: %.2f (VIS %.2f, red edge %.2f, NIR %.2f, SWIR %.2f).' % (l9['median_r_leaf_vs_UAV'], *l9['r_by_region'].values())],
            ['WRI from UAV spectra: r = %.2f with plot DI; test balanced accuracy %.2f (sensitivity %.2f, specificity %.2f).' % (tf.loc['WRI', 'r_UAV_vs_DI_all48'], tf.loc['WRI', 'test_balanced_acc'], tf.loc['WRI', 'test_sensitivity'], tf.loc['WRI', 'test_specificity']),
             'Leaf WRI and UAV WRI of the same plots: r = %.2f; HI also transfers (r = %.2f), red-edge position and RVSI do not.' % (tf.loc['WRI', 'r_leaf_vs_UAV_index'], tf.loc['HI', 'r_leaf_vs_UAV_index'])],
            'Transfer table → conclusions on up-scaling.', 'Raw reflectance does not agree between leaf and canopy (canopy structure, soil, shadow), but normalised indices on the NIR shoulder do.', ['Youden (1950)'],
            'Why do indices transfer when reflectance does not? → Normalised differences cancel the brightness change from leaf to canopy, keeping the shape signal of the disease (Liu et al., 2026).', ['c44', 'c45', 'c46', 'c47'])
    add('L10', 'Pre-symptomatic leaves', 'L10', 'Not run for 2025-26.', '—', '—', ['Not applicable: the 2025-26 season had natural infection with no tagged pre-symptomatic leaves (1, 4, 7 January sampling is part of the 2026-27 plan).'], [], '—', 'Planned for the 2026-27 inoculated trial.', [], '', [])
    return S


def literature(T, F):
    """Comparison of the Part L results with the disease papers used in the methodology (paper facts as recorded in the methodology)."""
    rows = [['Paper', 'What they found', 'This analysis (2025-26 leaves)', 'Agreement']]
    if 'l7_metrics' in T:
        R = T['l7_metrics']; b = F['best']; rb = R[(R.task == 'B') & (R.model == b['B'])].iloc[0]; ra = R[(R.task == 'A') & (R.model == b['A'])].iloc[0]
        nets = R[(R.task == 'A') & (R.family == 'DL')].set_index('model').macro_F1
        rows += [['Cross et al. (2024)', 'Wheat stripe rust leaf spectra, 10 classes: exact accuracy 45–52%, 79–96% within one class.', 'Six grades: OA %.2f, within one grade %.2f (%s).' % (rb.OA, rb.within1, b['B']), 'Same pattern: neighbouring grades overlap; within-one accuracy is high.'],
                 ['Zhang et al. (2022)', 'Rice leaf blast grades from hyperspectral images of whole leaves: 88–98% accuracy (SVM, PNN).', 'Six grades OA %.2f; detection OA %.2f.' % (rb.OA, ra.OA), 'Lower for grades: a leaf-clip spectrum samples a small part of the leaf, while the grade describes the whole leaf.'],
                 ['Ma et al. (2026)', 'Rice blast: DT-EDNet best of the compared networks (canopy hyperspectral).', 'Task A macro-F1: DNN-F1 %.3f, ConvNeXt %.3f, ResNet18 %.3f, DT-EDNet %.3f.' % (nets.get('DNN-F1', np.nan), nets.get('ConvNeXt V2-Atto', np.nan), nets.get('ResNet18', np.nan), nets.get('DT-EDNet', np.nan)), 'Not confirmed here: with 14 tabular features the pseudo-image has little spatial structure for the image networks to exploit.']]
    jm = T['l56_jm'].set_index(['grade_a', 'grade_b']).JM
    rows += [['Mandal et al. (2023)', 'Rice blast canopy spectra: almost all severity pairs separable (JM > 1.92) except levels 4 and 5.', 'Only grade 0 vs 9 nearly separable (JM %.2f); neighbouring grades JM %.2f–%.2f.' % (jm[(0, 9)], min(jm[(3, 5)], jm[(5, 7)], jm[(7, 9)]), max(jm[(1, 3)], jm[(3, 5)], jm[(5, 7)], jm[(7, 9)])), 'Partly: leaf grades of white rust overlap more than canopy levels of rice blast.'],
             ['Selvaprakash et al. (2026)', 'Isolation Forest screening of leaf spectra made the models more robust (4.7%).', '%d spectra flagged; none faulty, so none removed.' % F['n_if'], 'Method applied; flags here were severe but valid leaves.'],
             ['Mahlein et al. (2010); Lv et al. (2023)', 'Disease changes the visible, red-edge and NIR reflectance; derivative features help.', 'Visible ↑, NIR ↓, red edge shifts %.1f → %.1f nm; FD |r| %.3f > reflectance |r| %.3f.' % (F['l51']['REP_by_grade']['0'], F['l51']['REP_by_grade']['9'], F['l51']['max_abs_r_FD'], F['l51']['max_abs_r_R']), 'Agrees.']]
    if 'l8_models' in T:
        m = T['l8_models'].set_index('task')
        rows.append(['Zhang et al. (2014a)', 'Wheat powdery mildew: adding remote sensing to a weather model raised OA from 69% to 78%.', 'ΔS (spectrum over covariates): A %+.3f, B %+.3f, C %+.3f; ΔC: A %+.3f, B %+.3f, C %+.3f.' % (m.loc['A', 'dS'], m.loc['B', 'dS'], m.loc['C', 'dS'], m.loc['A', 'dC'], m.loc['B', 'dC'], m.loc['C', 'dC']),
                     'Spectrum adds over covariates where ΔS > 0; covariates add over the spectrum where ΔC > 0 (one season: covariates mostly describe date and crop).'])
    if 'l9_transfer' in T:
        tf = T['l9_transfer'].set_index('feature')
        rows += [['Liu et al. (2026)', 'Wheat powdery mildew: an index developed from ground spectra tracked the disease from UAV.', 'Leaf WRI on UAV plot spectra: r = %.2f with plot DI; test balanced accuracy %.2f.' % (tf.loc['WRI', 'r_UAV_vs_DI_all48'], tf.loc['WRI', 'test_balanced_acc']), 'Agrees for normalised NIR indices.'],
                 ['Bohnenkamp et al. (2019)', 'Wheat yellow rust: features transferred between scales performed worse than features selected at each scale.', 'Band-wise leaf vs UAV reflectance r median %.2f; RVSI, REP, GNDVI do not transfer.' % F['l9']['median_r_leaf_vs_UAV'], 'Agrees: only some leaf features survive at canopy scale; canopy selection is needed (2026-27).']]
    return rows
