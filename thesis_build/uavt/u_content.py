"""Single source of the methodology steps, metric explanations, interpretations and glossary of the UAV transfer test.
Used by the Word report (u4_word.py), the Excel workbook (u3_excel.py) and the slides (u5_pptdata.py -> u5_ppt.js),
so the three files always carry the same content. All numbers come from uavt/out/."""
import json, os, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'; O = HERE + 'out/'; S = HERE + '../'
f2 = lambda x: '–' if x is None or (isinstance(x, float) and not np.isfinite(x)) else '%.2f' % x
f3 = lambda x: '–' if x is None or (isinstance(x, float) and not np.isfinite(x)) else '%.3f' % x

def load():
    D = dict(GT=pd.read_csv(O + 'ground_truth.csv'), MF=pd.read_csv(O + 'metrics_frozen.csv'), PF=pd.read_csv(O + 'predictions_frozen.csv'), MU=pd.read_csv(O + 'metrics_uav_trained.csv'),
             PU=pd.read_csv(O + 'predictions_uav_trained.csv'), BM=pd.read_csv(O + 'best_models.csv'), DF=pd.read_csv(O + 'domain_features.csv'), SC=pd.read_csv(O + 'spectra_compare.csv'),
             PC=pd.read_csv(O + 'pca_domain.csv'), SU=json.load(open(O + 'summary.json')),
             CI=pd.read_csv(O + 'ci.csv') if os.path.exists(O + 'ci.csv') else None, PM=pd.read_csv(O + 'permutation.csv') if os.path.exists(O + 'permutation.csv') else None,
             MX=pd.read_csv(O + 'maxstat.csv') if os.path.exists(O + 'maxstat.csv') else None)
    return D

VAR = ['Direct', 'Healthy-reference corrected', 'Corrected + brightness-normalised']
VSH = {'Direct': 'direct', 'Healthy-reference corrected': 'corrected', 'Corrected + brightness-normalised': 'normalised'}
KEY = {'A': 'macro_F1', 'B': 'macro_F1', 'C': 'R2'}; KL = {'A': 'macro-F1', 'B': 'macro-F1', 'C': 'R²'}
TN = {'A': 'detection (healthy vs diseased)', 'B': 'six-grade severity', 'C': 'severity score (0–9)'}

def facts(D):
    """Every number used in the texts."""
    GT, MF, MU, BM, DF, SC, PC, SU = D['GT'], D['MF'], D['MU'], D['BM'], D['DF'], D['SC'], D['PC'], D['SU']
    best = SU['best']; F = dict(best=best)
    m = lambda t, model, v: MF[(MF.task == t) & (MF.model == model) & (MF.variant == v)].iloc[0]
    F['m'] = m; F['asd'] = lambda t, role: float(BM[(BM.task == t) & (BM.role == role)].asd_value.iloc[0])
    F['mu'] = {t: MU[MU.task == t].iloc[0] for t in 'ABC'}
    F['bv'] = {t: max(VAR, key=lambda v: m(t, best[t]['overall'], v)[KEY[t]]) for t in 'ABC'}
    F['bo'] = {t: m(t, best[t]['overall'], F['bv'][t]) for t in 'ABC'}
    F['top'] = {t: MF[MF.task == t].sort_values(KEY[t], ascending=False).iloc[0] for t in 'ABC'}
    F['nH'], F['nD'] = int((GT.status == 'Healthy').sum()), int((GT.status == 'Diseased').sum())
    dis = GT[GT.status == 'Diseased']; F['dis'] = dis
    F['grades'] = GT.grade.value_counts().sort_index()
    rm = lambda col, lo, hi: SC.loc[(SC.wavelength >= lo) & (SC.wavelength <= hi), col].mean(); F['rm'] = rm
    F['nir_uav'], F['nir_asd'] = rm('UAV healthy', 780, 880), rm('ASD healthy (24 Feb)', 780, 880)
    F['red_uav'], F['red_asd'] = rm('UAV healthy', 650, 690), rm('ASD healthy (24 Feb)', 650, 690)
    F['nfeat'] = len(DF); F['out50'] = {t: int((DF['uav_%s_out_pct' % t] > 50).sum()) for t in ('direct', 'corrected', 'normalised')}
    F['gapf'] = DF[DF.in_uav_gap].feature.tolist()
    zz = DF.assign(az=DF.uav_direct_z.abs()).sort_values('az', ascending=False); F['zmax'] = zz.head(3)[['feature', 'uav_direct_z']].values.tolist()
    # PCA: share of UAV plots outside the 99th percentile Mahalanobis distance of the ASD leaves (PC1-PC2)
    a = PC[PC.source == 'ASD leaf'][['PC1', 'PC2']].values; mu_, cv = a.mean(0), np.cov(a.T); iv = np.linalg.inv(cv)
    md = lambda X: np.sqrt(np.einsum('ij,jk,ik->i', X - mu_, iv, X - mu_)); lim = np.percentile(md(a), 99)
    F['pca_out'] = {src: float(100 * np.mean(md(PC[PC.source == src][['PC1', 'PC2']].values) > lim)) for src in PC.source.unique() if src != 'ASD leaf'}
    F['pca_var'] = SU['pca_var']
    PFb = D['PF']; L3 = PFb[(PFb.task == 'C') & (PFb.model == best['C']['overall']) & (PFb.variant == F['bv']['C'])].sort_values('plot')
    ok = GT.score_L3.notna().values; F['rL3'] = np.corrcoef(L3.pred.values[ok], GT.score_L3.values[ok])[0, 1] if L3.pred.values[ok].std() > 0 else np.nan
    F['MLD'] = MF.groupby(['task', 'variant'])[['macro_F1', 'R2']].max()
    CI, PM = D['CI'], D['PM']
    def ci(t, role, v, k):
        if CI is None: return (np.nan, np.nan)
        r = CI[(CI.task == t) & (CI.role == role) & (CI.variant == v)]
        return (float(r[k + '_lo'].iloc[0]), float(r[k + '_hi'].iloc[0])) if len(r) and k + '_lo' in r else (np.nan, np.nan)
    F['ci'] = ci; F['perm'] = {r.task: r for r in PM.itertuples()} if PM is not None else {}
    F['maxs'] = {r.task: r for r in D['MX'].itertuples()} if D['MX'] is not None else {}
    F['n_bands'] = SU['n_bands']; F['asd_n'] = SU['asd_models_trained_on']; F['gaps'] = SU['gaps']
    return F

def cis(F, t, role, v, k):
    lo, hi = F['ci'](t, role, v, k); return '' if not np.isfinite(lo) else ' (95 %% CI %.2f to %.2f)' % (lo, hi)

# ---------------------------------------------------------------- methodology steps
def steps(D, F):
    best = F['best']; mu = F['mu']
    S_ = []
    def add(no, title, position, concept, why, papers, how, mine, output, notes, question, eqs=()):
        S_.append(dict(no=no, title=title, position=position, concept=concept, why=why, papers=papers, how=how, mine=mine, output=output, notes=notes, question=question, eqs=list(eqs)))
    gapf = ', '.join(F['gapf']) if F['gapf'] else 'none'
    add('M1', 'UAV image and plot mean spectra', 'First step: the input data of the test.',
        'A hyperspectral camera records reflectance in hundreds of narrow bands for every pixel. Averaging the crop pixels of one plot gives one plot mean spectrum that represents the canopy of that plot.',
        'The leaf models must be judged on the data the thesis will use operationally, the UAV image. Plot means match the plot-level ground truth and reduce pixel noise.',
        'UAV disease studies use plot or region-of-interest mean spectra as the modelling unit (Aasen et al., 2018; Zhang et al., 2019); hyperspectral pre-processing removes noisy and water-vapour bands and smooths the spectra (Savitzky and Golay, 1964; Rinnan et al., 2009).',
        ['Calibrate the image to reflectance and remove noisy bands (here done in ENVI: 613 → 483 bands; 900–915, 1335–1460, 1785–1965 and > 2400 nm removed; Savitzky–Golay filter 5/2).',
         'Clip the 48 plot polygons (ArcMap, WGS 84 / UTM 43N) and keep the crop pixels (NDVI > 0.6 and spectral angle < 0.3 rad).',
         'Export the mean spectrum of every plot ROI from ENVI as an ASCII plot file (column 1 wavelength, one column per ROI).',
         'Read the file and check: number of bands, wavelength range, gaps, negative values and brightness spread between plots.'],
        '%d plot mean spectra, %d bands from 399 to 2398 nm, three gaps (%s); ROI #n = plot n.' % (len(D['GT']), F['n_bands'], '; '.join('%.0f–%.0f nm' % (a, b) for a, b in F['gaps'])),
        '48 × %d reflectance matrix (sheet 9_Spectra; UAV_hyperspectral_plot_spectra_2025-26.xlsx).' % F['n_bands'],
        'Negative reflectance occurs only beyond ~2350 nm in a few plots (noise). Plot brightness differed strongly between plots; this is checked in step M5 and in the domain check.',
        'Why plot means and not pixels? The ground truth is a plot-level score; pixel-level labels do not exist.')
    add('M2', 'Ground truth of the same day', 'Second step: the true values against which predictions are judged.',
        'Each scored leaf has a 0–9 white rust score (Conn et al., 1990). The plot mean score summarises the plot; PDI expresses it in per cent (Wheeler, 1969).',
        'Accuracy can only be measured against independent observations taken at the same time as the image; the ASD scoring and the flight were on the same day.',
        'Plot severity from leaf scores: PDI = Σ score / (9 × n) × 100 (Wheeler, 1969); the 0–9 key of Conn et al. (1990) is the standard for rapeseed–mustard.',
        ['Take all leaf scores of 24 Feb 2026 (L3, L5 and LL leaves of the tagged plants).',
         'Task A: label = 1 (diseased) for unsprayed plots, 0 (healthy) for the fungicide-sprayed plots.',
         'Task C: plot mean score = mean of the leaf scores of the plot.',
         'Task B: grade = the grade of the 0, 1, 3, 5, 7, 9 key nearest to the plot mean score (ties to the lower grade).',
         'Also store PDI, the disease-index class from PDI and the mean score of the upper leaves (L3) for checks.'],
        '%d leaves; %d healthy and %d diseased plots; diseased mean score %.2f–%.2f (PDI %.0f–%.0f %%); grades %s.' % (int(D['GT'].n_leaves.sum()), F['nH'], F['nD'], F['dis'].score.min(), F['dis'].score.max(), F['dis'].PDI.min(), F['dis'].PDI.max(), ', '.join('%d: %d plots' % (g, n) for g, n in F['grades'].items())),
        'True labels of the three tasks (sheet 1_Ground_truth).',
        'The models output a leaf score, so the plot mean leaf score (not the PDI class) is the matching target. The disease-index class is listed for reference.',
        'Why the nearest grade and not the PDI class? The models were trained on leaf grades; the nearest grade keeps the same scale.',
        eqs=[('Mean score_{plot} = Σ score_{i} / n', 'M2.1'), ('PDI (%) = Σ score_{i} / (9 × n) × 100', 'M2.2')])
    rows = '; '.join('%s: %s (%s, %s %s)' % (TN[t], best[t]['overall'], 'ML ' + best[t]['ML'], 'DL ' + best[t]['DL'], '') for t in 'ABC')
    add('M3', 'Selection of the best ASD models', 'Third step: which trained models are tested.',
        'In the ASD analysis every model was tested with leave-one-replication-out (LORO) cross-validation: each replication is held out once while the model is trained on the others. The best model has the highest held-out score.',
        'Only models evaluated on unseen replications give a fair estimate; testing all 30 models on the UAV data as well shows whether the leaf ranking carries over.',
        'Grouped (blocked) cross-validation prevents optimistic accuracy when samples share a plot (Roberts et al., 2017); model selection must be separated from testing (Varma and Simon, 2006; Cawley and Talbot, 2010).',
        ['Read the LORO metrics of the ASD analysis (macro-F1 for detection and grades, R² for the score).',
         'For each task take the best model overall, the best machine-learning (ML) model and the best deep-learning (DL) model.',
         'Use the final versions of these models, refitted on all leaves (outputs/ASD_2025-26_models), without any change ("frozen").',
         'Apply all 30 saved models (5 ML + 5 DL per task) to the UAV data as well, for completeness.'],
        'Best models: %s. ML models: SVM (Cortes and Vapnik, 1995), random forest (Breiman, 2001), XGBoost (Chen and Guestrin, 2016), k-NN (Cover and Hart, 1967), PLS-DA/PLSR (Barker and Rayens, 2003); DL: DNN-F1, EfficientNet-B0 (Tan and Le, 2019), ResNet18 (He et al., 2016), ConvNeXt V2 (Woo et al., 2023) and DT-EDNet with squeeze-and-excitation (Hu et al., 2018) on pseudo-images (Sharma et al., 2019).' % rows,
        'List of frozen models and their inputs (sheet 2_Best_models; Table "Best ASD models").',
        'The best leaf model need not be the best canopy model; therefore all models are reported (sheet 7_All_models).',
        'Why freeze the models? The question is whether the leaf models can be used as they are; any refitting would answer a different question (that is step M6).')
    add('M4', 'Same pre-processing and features as for the leaves', 'Fourth step: turn every UAV spectrum into the model inputs.',
        'A trained model expects exactly the inputs it was trained on. The ASD pipeline smoothed the spectra, took the first derivative (FD) and computed band values, vegetation indices and red-edge parameters.',
        'Any difference in pre-processing would change the inputs and confound the test.',
        'Calibration transfer keeps the pre-processing identical and corrects the spectra instead (Feudale et al., 2002); derivatives sharpen absorption features and remove offsets (Tsai and Philpot, 1998); the red-edge position follows Horler et al. (1983).',
        ['Resample each UAV spectrum to 1 nm from 350 to 2500 nm by linear interpolation (gaps bridged by straight lines; values beyond the measured range held constant).',
         'Smooth with a Savitzky–Golay filter (window 11 nm, polynomial order 2) and compute the first derivative with the same filter.',
         'Keep 400–2400 nm; take the reflectance R and derivative FD at 5-nm steps.',
         'Compute the published indices (e.g. MCARI, DWSI-2), the red-edge parameters (REP = wavelength of maximum FD in 680–760 nm, Dr = maximum FD, red-edge area) and the data-driven NDSI, RSI and WRI of the leaf analysis.',
         'Pick, for each model, its own input features and standardise them with the training mean and SD saved in the model file.'],
        'Code wr_features.py (identical to the leaf pipeline). Features inside UAV gaps: %s (interpolated values, not measurements).' % gapf,
        'Feature table of the 48 plots for each input variant (out/uav_features_*.csv).',
        'Linear interpolation across the 1780–1970 nm gap replaces the water-absorption shape of the leaves with a straight line, so FD in that region has no physical meaning on the UAV data.',
        'Why standardise with the training statistics? Using the UAV mean and SD would leak information and change the model.',
        eqs=[('FD(λ) = dR/dλ ≈ Savitzky–Golay derivative (window 11, order 2)', 'M4.1'), ('z = (x − μ_{train}) / σ_{train}', 'M4.2'), ('REP = argmax_{680 ≤ λ ≤ 760} FD(λ)', 'M4.3')])
    add('M5', 'Three input variants (correction of the UAV spectra)', 'Fifth step: reduce the leaf–canopy difference before prediction.',
        'Variant 1 (direct) uses the UAV spectra as measured. Variant 2 (healthy-reference corrected) multiplies each wavelength by the ratio of the mean healthy ASD leaf to the mean healthy UAV plot of the same day. Variant 3 (brightness-normalised) scales variant 2 to the same mean reflectance as the healthy leaves, keeping only the spectral shape.',
        'Canopy reflectance is lower and differently shaped than leaf reflectance (Asner, 1998). A wavelength-wise gain built from reference targets removes the systematic part of the difference; normalisation removes the illumination-driven brightness differences between plots.',
        'Empirical-line calibration maps image values onto reference reflectance with targets of known reflectance (Smith and Milton, 1999); calibration transfer uses standards measured in both domains (Feudale et al., 2002); normalising each spectrum to remove multiplicative effects is standard spectral pre-processing (Barnes et al., 1989; Rinnan et al., 2009); in machine learning this is domain adaptation (Pan and Yang, 2010).',
        ['Compute the mean ASD spectrum of the healthy leaves of 24 Feb and interpolate it to the UAV wavelengths.',
         'For each plot p, compute the mean UAV spectrum of the healthy plots excluding p (leave-one-out, so a healthy plot never corrects itself).',
         'Gain(λ) = ASD healthy(λ) / UAV healthy without p(λ); corrected spectrum = UAV spectrum × gain.',
         'Normalised spectrum = corrected spectrum × (mean of the ASD healthy spectrum) / (mean of the corrected spectrum).',
         'Run step M4 on each variant.'],
        'Reference = the 12 fungicide-sprayed plots (known healthy by design). The diseased plots are never used to build the correction, so the test stays independent.',
        'Three feature tables → predictions of all 30 models (sheets 3–5, 7, 11).',
        'A full transfer (direct or piecewise direct standardisation) needs paired leaf and canopy spectra of the same plants (Feudale et al., 2002); these were not collected in 2025-26.',
        'Is the correction fair for detection? Yes: healthy plots are corrected with the other healthy plots only, and no diseased label is used.',
        eqs=[('R_{corr,p}(λ) = R_{UAV,p}(λ) × R̄_{ASD,healthy}(λ) / R̄_{UAV,healthy,−p}(λ)', 'M5.1'), ('R_{norm,p}(λ) = R_{corr,p}(λ) × mean(R̄_{ASD,healthy}) / mean(R_{corr,p})', 'M5.2')])
    add('M6', 'Domain check: are the UAV inputs inside the leaf training range?', 'Sixth step: explain the result before judging accuracy.',
        'A model is reliable only inside its applicability domain, the range of inputs seen in training. Values outside it are extrapolations.',
        'If most UAV inputs lie outside the leaf range, poor accuracy is expected and its cause is identified.',
        'Range-based and distance-based applicability domains are standard checks of model transfer (Sahigara et al., 2012); PCA projects new samples onto the training space (Jolliffe and Cadima, 2016).',
        ['For each input feature of the best models compute the 1st and 99th percentile over the 2330 leaves.',
         'Count the share of UAV plots outside this range for each input variant, and the shift of the UAV mean in leaf SD units (z).',
         'Fit a PCA on the standardised features of the leaves; project the UAV plots onto PC1–PC2.',
         'Compute the Mahalanobis distance of every point to the leaf centre in PC1–PC2; a UAV plot beyond the 99th percentile of the leaves is outside the domain.'],
        '%d features (union of the best models\' inputs).' % F['nfeat'], 'Sheets 8_Domain_features and 10_PCA; Figures of feature ranges and PCA.',
        'A range check is simple and transparent; a distance check (Mahalanobis) also catches unusual combinations of features.',
        'Why the 1st–99th percentile? It ignores a few extreme leaves while still describing the training range.',
        eqs=[('% out = 100 × #{UAV plots with x < P_{1} or x > P_{99}} / 48', 'M6.1'), ('shift (SD) = (mean_{UAV} − mean_{ASD}) / SD_{ASD}', 'M6.2'), ('D_{M} = √[(x − μ)^{T} Σ^{−1} (x − μ)]', 'M6.3')])
    add('M7', 'In-domain check: best ML model type refitted on the UAV plots', 'Seventh step: is there a disease signal in the UAV spectra at all?',
        'The same model type, hyper-parameters and input features as the best ASD ML model are trained on the UAV plots themselves and tested by LORO.',
        'A failed transfer has two possible causes: no disease signal in the canopy spectra, or a leaf–canopy mismatch. Training on the UAV data separates them.',
        'Grouped LORO testing (Roberts et al., 2017); standardisation inside the training folds only (Cawley and Talbot, 2010); significance of a classifier by label permutation (Ojala and Garriga, 2010).',
        ['Use the ASD folds: replications R1, R2, R3 held out in turn, with the healthy plots rotated among the folds (about 32 training and 16 test plots).',
         'Drop features that lie inside UAV band gaps; standardise with the training-fold mean and SD.',
         'Fit the model on the training fold, predict the test fold, repeat for the three folds and pool the 48 predictions.',
         'Permutation test: shuffle the labels within folds (999 times for A, 199 for B and C), repeat the whole LORO and compare the observed score with the null distribution.'],
        'Models: %s (A), %s (B), %s (C); features used: A %s; B %s; C %s.' % (mu['A'].model, mu['B'].model, mu['C'].model, mu['A'].features, mu['B'].features, mu['C'].features),
        'UAV-trained predictions and scores (sheet 6_UAV_trained) and permutation p-values.',
        'With 48 plots the deep networks were not refitted; this check is a lower bound of what UAV models can do with more samples.',
        'Why permute within folds? It keeps the fold structure and plot grouping, so only the label–spectrum link is broken.',
        eqs=[('p = (1 + #{null scores ≥ observed}) / (1 + number of permutations)', 'M7.1')])
    add('M8', 'Accuracy measures and uncertainty', 'Last step: express how good the predictions are.',
        'Different tasks need different measures: class agreement for detection and grades, error and correlation for the score. A bootstrap over plots gives confidence intervals.',
        'Macro-F1 and balanced accuracy are fair when classes are unequal (12 healthy vs 36 diseased); QWK credits near-misses for ordered grades; R² and RMSE describe the score error.',
        'Classification measures (Sokolova and Lapalme, 2009), ROC analysis (Fawcett, 2006), weighted kappa (Cohen, 1968), RPD (Williams, 2001), bootstrap confidence intervals (Efron and Tibshirani, 1993).',
        ['Compare predictions with the true values of step M2 for every model and variant.',
         'Compute the measures below (Excel recomputes the simple ones with live formulas in sheets 3–5).',
         'Bootstrap: resample the 12 healthy and 36 diseased plots with replacement 2000 times, recompute the measure, take the 2.5th and 97.5th percentiles as the 95 % confidence interval.',
         'Best of all models: because 30 model–input combinations are compared, the best one is tested with a maximum-statistic permutation test: the labels are shuffled 2000 times and the best score of all 30 combinations is recorded each time; p = share of shuffles whose best score reaches the observed best (Westfall and Young, 1993).'],
        'Measures computed in Python (scikit-learn; Pedregosa et al., 2011) and, where possible, again with Excel formulas.', 'Metric tables, confusion matrices, confidence intervals (sheets 2–7, 13).',
        'With 48 plots the confidence intervals are wide; differences smaller than the interval are not meaningful.',
        'Why macro-F1 rather than accuracy? Predicting "diseased" for every plot gives 75 % accuracy but macro-F1 0.43.')
    return S_

# ---------------------------------------------------------------- metric explanations (for Word table, Excel sheet and calculator)
METRICS = [
    ('Overall accuracy (OA)', 'A, B', '(number correct) / (number of plots)', '=SUMPRODUCT(--(pred=true))/COUNT(true)', 'Share of plots predicted correctly; misleading when classes are unequal.', 'Sokolova and Lapalme (2009)'),
    ('Sensitivity (recall of diseased)', 'A', 'TP / (TP + FN)', '=COUNTIFS(true,1,pred,1)/COUNTIF(true,1)', 'Share of diseased plots found; 1 = none missed.', 'Fawcett (2006)'),
    ('Specificity (recall of healthy)', 'A', 'TN / (TN + FP)', '=COUNTIFS(true,0,pred,0)/COUNTIF(true,0)', 'Share of healthy plots recognised; 1 = no false alarm.', 'Fawcett (2006)'),
    ('Balanced accuracy', 'A', '(sensitivity + specificity) / 2', '=(sens+spec)/2', '0.5 = chance, 1 = perfect; fair with unequal classes.', 'Sokolova and Lapalme (2009)'),
    ('F1 of a class', 'A, B', '2 × precision × recall / (precision + recall)', '=2*P*R/(P+R)', 'Balances false alarms and misses for one class.', 'Sokolova and Lapalme (2009)'),
    ('Macro-F1', 'A, B', 'mean of the class F1 values', '=AVERAGE(F1_class)', 'Treats small and large classes equally; main measure for A and B.', 'Sokolova and Lapalme (2009)'),
    ('AUC', 'A', 'area under the ROC curve of the disease score', 'Python (ranks of the scores)', '0.5 = chance, 0.7–0.8 acceptable, > 0.8 good.', 'Fawcett (2006)'),
    ('Quadratic weighted kappa (QWK)', 'B', '1 − Σ w_{ij} O_{ij} / Σ w_{ij} E_{ij}, w_{ij} = (i − j)² / (k − 1)²', 'Python', 'Agreement for ordered grades; near-misses cost less; 0 = chance, 1 = perfect.', 'Cohen (1968)'),
    ('Within one grade', 'B', 'share with |grade position(pred) − position(true)| ≤ 1', '=COUNTIF(steps,"<=1")/COUNT(steps)', 'How often the prediction is at most one grade away.', 'used in the ASD analysis'),
    ('R²', 'C', '1 − Σ (pred − true)² / Σ (true − mean)²', '=1-SUMXMY2(pred,true)/DEVSQ(true)', 'Share of the variance explained; ≤ 0 = no better than the mean.', 'Williams (2001)'),
    ('RMSE', 'C', '√[Σ (pred − true)² / n]', '=SQRT(SUMXMY2(pred,true)/COUNT(true))', 'Typical error in score units (0–9).', 'Williams (2001)'),
    ('MAE', 'C', 'Σ |pred − true| / n', '=SUMPRODUCT(ABS(pred-true))/COUNT(true)', 'Mean absolute error in score units.', 'Williams (2001)'),
    ('Bias', 'C', 'mean(pred) − mean(true)', '=AVERAGE(pred)-AVERAGE(true)', 'Systematic over- (+) or under-prediction (−).', 'Williams (2001)'),
    ('Pearson r', 'C', 'covariance / (SD_{pred} × SD_{true})', '=CORREL(pred,true)', 'Strength of the linear relation; ranks plots even when biased.', 'Williams (2001)'),
    ('RPD', 'C', 'SD(true) / RMSE', '=STDEV(true)/RMSE', '> 2 good, 1.4–2 fair, < 1.4 poor.', 'Williams (2001)'),
    ('95 % confidence interval', 'all', '2.5th–97.5th percentile of 2000 bootstrap resamples of plots', 'Python', 'Range of plausible values; overlapping intervals = no clear difference.', 'Efron and Tibshirani (1993)'),
    ('Permutation p-value', 'UAV-trained', '(1 + #null ≥ observed) / (1 + permutations)', 'Python', 'Probability of the observed score if the spectra carried no information; < 0.05 = significant.', 'Ojala and Garriga (2010)'),
    ('Maximum-statistic p-value', 'all models', 'share of label shuffles in which the best of the 30 combinations reaches the observed best', 'Python', 'Corrects for picking the best of many models; < 0.05 = the best result is unlikely to be chance.', 'Westfall and Young (1993)')]

GLOSSARY = [('ASD', 'Analytical Spectral Devices FieldSpec spectroradiometer; here used with a contact probe on single leaves.'),
            ('UAV', 'Unmanned aerial vehicle (drone) carrying the hyperspectral camera.'),
            ('Domain / domain shift', 'The kind of data a model was trained on (leaf spectra) vs the kind it is applied to (canopy spectra); the difference between them.'),
            ('Frozen model', 'A trained model used without any refitting or change.'),
            ('LORO', 'Leave-one-replication-out cross-validation: each replication is held out once as the test set.'),
            ('FD', 'First derivative of reflectance with respect to wavelength (per nm).'),
            ('REP, Dr', 'Red-edge position (wavelength of maximum FD, 680–760 nm) and its height (maximum FD).'),
            ('Healthy-reference correction', 'Wavelength-wise gain that maps the mean healthy UAV plot onto the mean healthy ASD leaf of the same day.'),
            ('Brightness normalisation', 'Scaling a spectrum to a fixed mean reflectance so only its shape remains.'),
            ('Applicability domain', 'Input range within which a model\'s predictions are reliable.'),
            ('PCA', 'Principal component analysis: new axes that summarise most of the variation of many features.'),
            ('Mahalanobis distance', 'Distance from the centre of a cloud of points that accounts for its spread and correlation.'),
            ('Macro-F1, QWK, AUC, R², RMSE, RPD', 'Accuracy measures; see sheet "Metrics explained".'),
            ('Bootstrap', 'Resampling the plots with replacement many times to estimate the uncertainty of a measure.'),
            ('Permutation test', 'Shuffling the labels many times to see how often a score as good as the observed one arises by chance.'),
            ('PDI', 'Per cent disease index = mean score / 9 × 100.')]

# ---------------------------------------------------------------- how to apply to another data set (Excel guide, Word appendix, slide)
APPLY = [('1', 'Prepare the spectra', 'One reflectance spectrum per sample (plot, subplot or leaf), wavelength in nm in the first column (or as headers). Remove noisy bands; keep reflectance on a 0–1 scale.', 'ENVI ASCII export or CSV/XLSX', 'u1_apply.py reads ENVI ASCII; predict_white_rust.py reads XLSX/CSV'),
         ('2', 'Prepare the ground truth', 'One row per sample with: id, status (healthy/diseased), mean leaf score (0–9) or grade, and the grouping used for validation (replication/fold).', 'Sheet 1_Ground_truth as a template', ''),
         ('3', 'Choose the models', 'Use the frozen ASD models (outputs/ASD_2025-26_models). For a new sensor, keep the same feature code (wr_features.py).', 'ml/*.joblib, dl/*.pt', ''),
         ('4', 'Pre-process identically', 'Run the same pre-processing (1-nm resampling, Savitzky–Golay 11/2, FD, indices). Never refit the scaler on the new data.', 'wr_features.all_features()', 'Step M4'),
         ('5', 'Correct the spectra (optional)', 'If healthy reference samples exist in the new data, build the healthy-reference gain (leave-one-out) and the brightness-normalised version.', 'u1_apply.py, section "spectra variants"', 'Step M5'),
         ('6', 'Check the domain', 'Before trusting predictions, check % of samples outside the training range and the PCA/Mahalanobis distance.', 'sheet 8_Domain_features, 10_PCA', 'Step M6'),
         ('7', 'Predict and evaluate', 'Predict with each model; paste true and predicted values into sheet 12_Metrics_calculator to get all measures and confusion matrices.', 'sheet 12_Metrics_calculator', 'Step M8'),
         ('8', 'In-domain check', 'If enough labelled samples exist (≥ 30 per class), refit the best model type on the new data with grouped cross-validation and a permutation test.', 'u1_apply.py, section "in-domain check"', 'Step M7'),
         ('9', 'Report', 'Rebuild the Excel, Word and slides with u2_figs.py, u4_word.py, u3_excel.py, u5_pptdata.py and u5_ppt.js.', 'commands in sheet 0a_Guide', '')]
