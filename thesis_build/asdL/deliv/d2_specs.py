"""One specification per chart: the same table feeds the native Excel chart, the native PowerPoint chart and the 300-dpi Word figure.
spec = dict(id, sheet, title, kind (line | col | bar | scatter), data (DataFrame; first column = category / x), series (columns), xlab, ylab, colors, note)."""
import json, numpy as np, pandas as pd
GR = [0, 1, 3, 5, 7, 9]
GC = {0: '1A9850', 1: '66BD63', 3: 'D9A400', 5: 'F46D43', 7: 'D73027', 9: '7F0000'}
MODELS = ['SVM', 'RF', 'k-NN', 'PLS', 'DNN-F1', 'DT-EDNet', 'EfficientNet-B0', 'ResNet18', 'ConvNeXt V2-Atto']
MC = dict(zip(MODELS, ['1F77B4', '2CA02C', 'FF7F0E', '9467BD', '8C564B', 'D62728', 'E377C2', '7F7F7F', '17BECF']))
TASK = {'A': 'Task A – healthy vs diseased leaf', 'B': 'Task B – six leaf grades', 'C': 'Task C – leaf grade (0–9) regression'}
MAIN = {'A': 'macro-F1', 'B': 'macro-F1', 'C': 'R²'}; MKEY = {'A': 'macro_F1', 'B': 'macro_F1', 'C': 'R2'}
DCOL = ['1F77B4', 'FF7F0E', '2CA02C', 'D62728']; SCOL = {'Vegetative': '66BD63', 'Flowering': 'D9A400', 'Pod formation': 'B2182B'}
def S(id, sheet, title, kind, data, series, xlab, ylab, colors, note='', **kw): return dict(id=id, sheet=sheet, title=title, kind=kind, data=data.reset_index(drop=True), series=list(series), xlab=xlab, ylab=ylab, colors=list(colors), note=note, **kw)
def specs(T, F):
    L = []; ad = lambda *a, **k: L.append(S(*a, **k))
    f = T['l1_flow']; ad('c01', 'L1', 'Leaf spectra at each stage of the leaf-table check', 'bar', f, ['Spectra'], '', 'Number of spectra', ['2F5D8A'], 'Step L1 flow: read → removed → final table.', labels=True)
    g = T['l1_grade_date']; ad('c02', 'L1', 'Leaves of each grade on each date', 'col', g, g.columns[1:], 'Leaf grade (0–9 scale)', 'Number of leaves', DCOL, 'Natural infection; leaves L3, L5 and LL.')
    g = T['l1_grade_leaf']; ad('c03', 'L1', 'Leaves of each grade by leaf position', 'col', g, g.columns[1:], 'Leaf grade', 'Number of leaves', ['2166AC', '762A83', 'E08214'])
    g = T['l1_grade_stage']; ad('c04', 'L1', 'Leaves of each grade by growth stage', 'col', g, g.columns[1:], 'Leaf grade', 'Number of leaves', list(SCOL.values()))
    g = T['l1_grade_variety']; ad('c05', 'L1', 'Leaves of each grade by variety', 'col', g, g.columns[1:], 'Leaf grade', 'Number of leaves', ['2166AC', '762A83', 'E08214'])
    c = T['l2_counts'].copy(); c = c[c.part != 'All']; d = c.set_index('part')[['grade %d' % g for g in GR]].T.reset_index().rename(columns={'index': 'Grade'}); d['Grade'] = d.Grade.str.replace('grade', 'Grade')
    keep = [x for x in d.columns[1:] if any(k in x for k in ('TRAIN', 'TEST'))]; ad('c06', 'L2', 'Grade distribution of the training and test leaves', 'col', d[['Grade'] + keep], keep, 'Leaf grade', 'Number of leaves', ['2F5D8A', 'C0392B'])
    d2 = d[['Grade'] + [x for x in d.columns[1:] if 'network' in x] + [x for x in keep if 'TEST' in x]].copy(); d2.columns = ['Grade', 'Network fitting (22 plots)', 'Network validation (11 plots)', 'Test (15 plots)']
    ad('c07', 'L2', 'Network fitting, validation and test leaves by grade', 'col', d2, d2.columns[1:], 'Leaf grade', 'Number of leaves', ['2F5D8A', '7FB3D5', 'C0392B'])
    d3 = d[['Grade'] + [x for x in d.columns[1:] if 'fold' in x]].copy(); d3.columns = ['Grade', 'Fold 1', 'Fold 2', 'Fold 3']
    ad('c07b', 'L2', 'GroupKFold(3) folds of the training plots by grade', 'col', d3, d3.columns[1:], 'Leaf grade', 'Number of leaves', ['1B9E77', '7570B3', 'D95F02'])
    s = T['l3_splice']; ad('c08', 'L3', 'Raw reflectance around the 1000-nm detector join (mean of each grade)', 'line', s, s.columns[1:], 'Wavelength (nm)', 'Reflectance', [GC[g] for g in GR], 'Residual step of −0.002 at 1000/1001 nm; first-derivative bands 995–1005 nm left out of band selection (DEV-1).')
    e = T['l3_example']; ad('c09', 'L3', 'Raw and Savitzky–Golay smoothed spectrum of one grade-0 and one grade-9 leaf', 'line', e, e.columns[1:5], 'Wavelength (nm)', 'Reflectance', ['8FD19E', '1A9850', 'F1948A', '7F0000'], 'SG window 11, order 2; 400–2400 nm kept (water bands kept).')
    ad('c10', 'L3', 'First derivative (SG 11, 2) of the same two leaves', 'line', e, e.columns[5:7], 'Wavelength (nm)', 'dR/dλ (nm⁻¹)', ['1A9850', '7F0000'])
    sp = T['l51_spectra']; w = sp[['wavelength']].rename(columns={'wavelength': 'Wavelength (nm)'})
    d = pd.concat([w, pd.DataFrame({'Grade %d' % g: sp['R_mean_g%d' % g] for g in GR})], axis=1); ad('c11', 'L5.1', 'Mean reflectance of each leaf grade (all 2255 leaves)', 'line', d, d.columns[1:], 'Wavelength (nm)', 'Reflectance', [GC[g] for g in GR])
    d = pd.concat([w, pd.DataFrame({'Grade %d' % g: sp['FD_mean_g%d' % g] for g in GR})], axis=1); ad('c12', 'L5.1', 'Mean first derivative of each leaf grade', 'line', d, d.columns[1:], 'Wavelength (nm)', 'dR/dλ (nm⁻¹)', [GC[g] for g in GR])
    d = pd.concat([w, pd.DataFrame({'Grade %d' % g: sp['diff_pct_g%d' % g] for g in GR[1:]})], axis=1); ad('c13', 'L5.1', 'Difference of each grade from grade 0 (%)', 'line', d, d.columns[1:], 'Wavelength (nm)', 'Difference from grade 0 (%)', [GC[g] for g in GR[1:]])
    d = pd.concat([w, sp[['r_R', 'r_FD']].rename(columns={'r_R': 'Reflectance', 'r_FD': 'First derivative'})], axis=1); ad('c14', 'L5.1', 'Pearson r of each 5-nm band with the leaf grade', 'line', d, d.columns[1:], 'Wavelength (nm)', 'Pearson r', ['2F5D8A', 'C0392B'])
    ir = T['l51_index_r'].head(15).iloc[::-1]; ad('c15', 'L5.1', 'The 15 indices most correlated with the leaf grade (|r|)', 'bar', ir[['Index', '|r|']], ['|r|'], '', '|r| with grade', ['2F5D8A'], labels=True)
    st = T['l51_strata']; st = st.assign(Level=st.stratum.str.replace('Leaf position', 'Leaf').str.replace('Growth stage', 'Stage') + ': ' + st.level.astype(str))
    ad('c16', 'L5.1', 'Highest |r| with the grade within each stratum', 'col', st[['Level', 'max |r| R', 'max |r| FD']], ['max |r| R', 'max |r| FD'], '', 'max |r|', ['2F5D8A', 'C0392B'])
    rs = T['l51_r_strata']; d = pd.concat([rs[['wavelength']].rename(columns={'wavelength': 'Wavelength (nm)'}), pd.DataFrame({k: rs['r_FD|leaf=%s' % k] for k in ('L3', 'L5', 'LL')})], axis=1)
    ad('c17', 'L5.1', 'r of the first derivative with the grade by leaf position', 'line', d, d.columns[1:], 'Wavelength (nm)', 'Pearson r', ['2166AC', '762A83', 'E08214'])
    v = T['l57_var'].head(6); ad('c18', 'L5.7', 'PCA: variance explained by each component', 'col', v, ['explained_pct', 'cumulative_pct'], 'Component', 'Variance (%)', ['2F5D8A', 'C0392B'], line_series=['cumulative_pct'], labels=True)
    l = T['l57_load'].rename(columns={'wavelength': 'Wavelength (nm)'}); ad('c19', 'L5.7', 'PCA loadings of PC1–PC3', 'line', l, ['PC1', 'PC2', 'PC3'], 'Wavelength (nm)', 'Loading', ['2F5D8A', 'C0392B', '2CA02C'])
    sc = T['l57_scores']; el = T['l57_ell']; el = el[el.pair == 'PC1-PC2']; rng = np.random.default_rng(1); rows = []
    for g in GR:
        k = sc[sc.grade == g]; k = k.iloc[rng.choice(len(k), min(120, len(k)), replace=False)]
        rows += [dict(x=x, **{'Grade %d' % g: y}) for x, y in zip(k.PC1, k.PC2)]
    for g in GR:
        k = el[el.grade == g]; rows += [dict(x=x, **{'Grade %d ellipse' % g: y}) for x, y in zip(k.x, k.y)]
    d = pd.DataFrame(rows); cols = ['Grade %d' % g for g in GR] + ['Grade %d ellipse' % g for g in GR]; d = d[['x'] + cols].rename(columns={'x': 'PC1 score'})
    ad('c20', 'L5.7', 'PCA scores (PC1–PC2) of the leaves with 95% ellipses of each grade', 'scatter', d, cols, 'PC1 score', 'PC2 score', [GC[g] for g in GR] * 2, '120 random leaves per grade shown (all leaves in sheet L5.7 data); lines = 95% ellipses.', line_series=cols[6:])
    sh = T['l52_shap'].head(25).iloc[::-1]; ad('c21', 'L5.2', 'SHAP importance (mean |SHAP|) of the 25 most important candidate bands', 'bar', sh[['feature', 'mean_abs_SHAP']], ['mean_abs_SHAP'], '', 'mean |SHAP| (grade units)', ['2F5D8A'])
    m = T['l52_mccv']; ad('c22', 'L5.2', 'MCCV (50 plot divisions): RMSE of PLS models by number of components', 'line', m, ['MCCV_RMSE'], 'PLS components', 'RMSE (grade units)', ['2F5D8A'], markers=True)
    ca = T['l52_cars'][['iteration', 'n_bands', 'GKF_RMSE']]; ad('c23', 'L5.2', 'CARS: bands kept at each iteration', 'line', ca, ['n_bands'], 'CARS iteration', 'Bands kept', ['2F5D8A'], markers=True)
    ad('c24', 'L5.2', 'CARS: GroupKFold(3) RMSE of each subset (minimum = optimal wavelengths)', 'line', ca, ['GKF_RMSE'], 'CARS iteration', 'RMSE (grade units)', ['C0392B'], markers=True)
    ow = set(T['l52_ow'].Wavelength[T['l52_ow'].Type == 'First derivative']); d = pd.DataFrame({'Wavelength (nm)': sp.wavelength, 'Mean first derivative, grade 0': sp.FD_mean_g0, 'Mean first derivative, grade 9': sp.FD_mean_g9})
    d['Optimal wavelength (FD)'] = np.where(d['Wavelength (nm)'].isin(ow), sp.FD_mean_g9, np.nan)
    ad('c25', 'L5.2', 'The 32 optimal wavelengths (31 FD, 1 reflectance) on the mean first-derivative spectra', 'scatter', d, d.columns[1:], 'Wavelength (nm)', 'dR/dλ (nm⁻¹)', ['1A9850', '7F0000', '000000'], 'Markers = first-derivative optimal wavelengths (R535 not shown).', line_series=list(d.columns[1:3]))
    bg = T['l53_by_grade']; ad('c26', 'L5.3', 'White Rust Index (WRI) of the training leaves by grade', 'col', bg[['Grade', 'WRI mean']].assign(Grade=bg.Grade.map(lambda g: 'Grade %d' % g)), ['WRI mean'], 'Leaf grade', 'Mean WRI', ['2F5D8A'], labels=True)
    ww = T['l53_wri_w'].copy(); ww['Weight w'] = ww.w.map(lambda x: 'w = %g' % x); ww = ww.sort_values('w')
    ad('c27', 'L5.3', 'Best WRI for each weight w (|r| with the grade)', 'col', ww[['Weight w', 'abs_r']], ['abs_r'], 'Weight of the third band', '|r| with grade', ['2F5D8A'], labels=True)
    rw = T['l54_relief']
    for t, col in (('A', '2F5D8A'), ('B', 'C0392B'), ('C', '2CA02C')):
        k = rw.sort_values('weight_' + t, ascending=False).head(10).iloc[::-1]; ad('c28' + t.lower(), 'L5.4', 'ReliefF weights, task %s (top 10 of %d indices)' % (t, len(rw)) if t != 'C' else 'RReliefF weights, task C (top 10 of %d indices)' % len(rw), 'bar', k[['feature', 'weight_' + t]], ['weight_' + t], '', 'Weight', [col])
    fv = T['l55_final']; k = fv[fv.task == 'B'].sort_values('VIF'); ad('c29', 'L5.5', 'VIF of the 14 features of the task-B DSF (all < 10)', 'bar', k[['feature', 'VIF']], ['VIF'], '', 'VIF', ['2F5D8A'], labels=True)
    jm = T['l56_jm'].copy(); jm['Pair'] = jm.grade_a.astype(str) + ' vs ' + jm.grade_b.astype(str); ad('c30', 'L5.6', 'Jeffries–Matusita distance between grade pairs (max 2)', 'col', jm[['Pair', 'JM']], ['JM'], 'Grade pair', 'JM distance', ['2F5D8A'], labels=True)
    if len(T.get('l6_paths', [])):
        P = T['l6_paths']
        for t in 'ABC':
            q = P[P.task == t].pivot(index='n_features', columns='model', values='cv_score').reset_index(); cols = [m for m in MODELS if m in q.columns]
            if t == 'C': q[cols] = -q[cols]
            ad('c31' + t.lower(), 'L6', 'SFFS path, %s: inner GroupKFold(3) score by number of features' % TASK[t].split(' – ')[0], 'line', q[['n_features'] + cols], cols, 'Number of features', 'RMSE' if t == 'C' else 'macro-F1', [MC[m] for m in cols], markers=True)
    if len(T.get('l6_hist', [])):
        H = T['l6_hist']
        for t in 'ABC':
            q = H[H.task == t].pivot(index='epoch', columns='model', values='val_score').reset_index(); cols = [m for m in MODELS if m in q.columns]
            if t == 'C': q[cols] = -q[cols]
            ad('c32' + t.lower(), 'L6', 'Network validation %s by epoch, %s' % ('RMSE' if t == 'C' else 'OA', TASK[t].split(' – ')[0]), 'line', q[['epoch'] + cols], cols, 'Epoch', 'Validation RMSE' if t == 'C' else 'Validation OA', [MC[m] for m in cols])
    if len(T.get('l7_metrics', [])):
        R = T['l7_metrics'].copy(); R = R.set_index('model').loc[[m for m in MODELS if m in set(R.model)]].reset_index() if False else R
        for t in 'ABC':
            q = R[R.task == t].copy(); q['order'] = q.model.map({m: i for i, m in enumerate(MODELS)}); q = q.sort_values('order')
            ad('c33' + t.lower(), 'L7', 'Test %s of every model, %s' % (MAIN[t], TASK[t].split(' – ')[0]), 'col', q[['model', MKEY[t]]], [MKEY[t]], '', MAIN[t] + ' (684 test leaves)', ['2F5D8A'], labels=True, point_colors=[MC[m] for m in q.model])
        q = R[R.task == 'A'].copy(); q['order'] = q.model.map({m: i for i, m in enumerate(MODELS)}); q = q.sort_values('order')
        ad('c34', 'L7', 'Task A: OA, sensitivity, specificity and AUC on the test leaves', 'col', q[['model', 'OA', 'sensitivity', 'specificity', 'AUC']], ['OA', 'sensitivity', 'specificity', 'AUC'], '', 'Value', ['2F5D8A', 'C0392B', '2CA02C', '9467BD'])
        b = F['best']['B']; r = R[(R.task == 'B') & (R.model == b)].iloc[0]; d = pd.DataFrame({'Grade': ['Grade %d' % g for g in GR], 'F1': [r['F1_g%d' % g] for g in GR], 'Recall': [r['recall_g%d' % g] for g in GR], 'Precision': [r['precision_g%d' % g] for g in GR]})
        ad('c35', 'L7', 'Task B: precision, recall and F1 of each grade (%s)' % b, 'col', d, ['Precision', 'Recall', 'F1'], 'Leaf grade', 'Value', ['7FB3D5', '2F5D8A', 'C0392B'])
        if 'l7_roc' in T:
            auc = float(R[(R.task == 'A') & (R.model == F['best']['A'])].AUC.iloc[0]); nm = '%s (AUC %.3f)' % (F['best']['A'], auc)
            ad('c36', 'L7', 'ROC curve of the best task-A model (%s)' % F['best']['A'], 'scatter', T['l7_roc'].rename(columns={'True positive rate': nm}).assign(Chance=lambda z: z['False positive rate']), [nm, 'Chance'], 'False positive rate', 'True positive rate', ['C0392B', '999999'], line_series=[nm, 'Chance'])
        P7 = T['l7_pred']; c = F['best']['C']; d = pd.DataFrame({'Observed grade': P7.grade, 'Predicted grade': P7['C|%s' % c]}).sort_values('Observed grade')
        mean = d.groupby('Observed grade')['Predicted grade'].mean(); d2 = pd.DataFrame({'Observed grade': list(d['Observed grade']) + GR, 'Leaves': list(d['Predicted grade']) + [np.nan] * 6, 'Mean of grade': [np.nan] * len(d) + [mean.get(g, np.nan) for g in GR], '1:1 line': [np.nan] * len(d) + GR})
        ad('c37', 'L7', 'Task C: predicted vs observed grade of the test leaves (%s)' % c, 'scatter', d2, ['Leaves', 'Mean of grade', '1:1 line'], 'Observed grade', 'Predicted grade', ['7FB3D5', 'C0392B', '555555'], line_series=['1:1 line'])
        stt = T['l7_strata']
        for t in 'ABC':
            q = stt[(stt.task == t) & (stt.model == F['best'][t])].copy(); q['Level'] = q.stratum.map({'leaf_pos': 'Leaf', 'stage': 'Stage', 'date': 'Date', 'variety': 'Variety'}) + ': ' + q.level.astype(str)
            ad('c38' + t.lower(), 'L7', '%s of the best model (%s) within each stratum, %s' % (MAIN[t], F['best'][t], TASK[t].split(' – ')[0]), 'col', q[['Level', 'value']], ['value'], '', MAIN[t], ['2F5D8A'], labels=True)
        lw = T['l7_low']; q = lw[lw.task == 'A'].copy(); q['order'] = q.model.map({m: i for i, m in enumerate(MODELS)}); q = q.sort_values('order')
        ad('c39', 'L7', 'Low-severity check: share of grade-1 test leaves detected as diseased (task A)', 'col', q[['model', 'value']], ['value'], '', 'Recall of grade-1 leaves', ['2F5D8A'], labels=True)
    if len(T.get('l6_stab_freq', [])):
        fq = T['l6_stab_freq']
        for t in 'ABC':
            q = fq[fq.task == t].sort_values('frequency'); ad('c40' + t.lower(), 'L6', 'SFFS stability, %s (%s): selection frequency over repeated GroupKFold(3) divisions' % (TASK[t].split(' – ')[0], q.model.iloc[0]), 'bar', q[['feature', 'frequency']], ['frequency'], '', 'Selection frequency', ['2F5D8A'], labels=True)
    if len(T.get('l8_models', [])):
        m = T['l8_models']; d = pd.DataFrame({'Task': ['Task A (macro-F1)', 'Task B (macro-F1)', 'Task C (R²)'], 'M0 covariates': m.M0.values, 'M1 leaf spectrum': m.M1.values, 'M2 spectrum + covariates': m.M2.values})
        ad('c41', 'L8', 'Covariate baseline: M0 covariates only, M1 best leaf-spectrum model, M2 spectrum + covariates', 'col', d, d.columns[1:], '', 'Main metric (test leaves)', ['999999', '2F5D8A', 'C0392B'], labels=True)
        gn = T['l8_gains']; q = gn[(gn.task == 'A') & gn.scope.str.startswith('date') & (gn.gain == 'dS')].copy(); q['Date'] = q.scope.str.replace('date ', '')
        ad('c42', 'L8', 'Task A per date: macro-F1 of M0, M1 and M2', 'col', q[['Date', 'M0', 'M1', 'M2']], ['M0', 'M1', 'M2'], 'Sampling date', 'macro-F1', ['999999', '2F5D8A', 'C0392B'], labels=True)
        if 'l8_imp' in T:
            q = T['l8_imp']; q = q[q.task == 'B'].head(12).iloc[::-1]; ad('c43', 'L8', 'Importance of the covariates in M0 (task B random forest)', 'bar', q[['covariate', 'importance']], ['importance'], '', 'Impurity importance', ['999999'])
    if len(T.get('l9_band', [])):
        bd = T['l9_band']; d = bd[['wavelength', 'leaf_mean_healthy', 'leaf_mean_diseased', 'UAV_mean_healthy', 'UAV_mean_diseased']].rename(columns={'wavelength': 'Wavelength (nm)', 'leaf_mean_healthy': 'Leaf (ASD), healthy plots', 'leaf_mean_diseased': 'Leaf (ASD), diseased plots', 'UAV_mean_healthy': 'UAV, healthy plots', 'UAV_mean_diseased': 'UAV, diseased plots'})
        ad('c44', 'L9', 'Mean leaf (ASD, resampled) and UAV canopy spectra of the 48 plots, 24 Feb 2026', 'scatter', d, d.columns[1:], 'Wavelength (nm)', 'Reflectance', ['1A9850', '7F0000', '66BD63', 'F46D43'], 'UAV band gaps 900–915, 1330–1460, 1780–1970 nm.', line_series=list(d.columns[1:]))
        d = bd[['wavelength', 'r_leaf_vs_UAV', 'r_leaf_vs_DI', 'r_UAV_vs_DI']].rename(columns={'wavelength': 'Wavelength (nm)', 'r_leaf_vs_UAV': 'r leaf vs UAV reflectance', 'r_leaf_vs_DI': 'r leaf reflectance vs plot DI', 'r_UAV_vs_DI': 'r UAV reflectance vs plot DI'})
        ad('c45', 'L9', 'Band-wise Pearson r over the 48 plots (24 Feb 2026)', 'scatter', d, d.columns[1:], 'Wavelength (nm)', 'Pearson r', ['555555', '2F5D8A', 'C0392B'], line_series=list(d.columns[1:]))
        p9 = T['l9_plots']; d = pd.DataFrame({'Plot DI (%)': p9.DI}); d['Healthy plots'] = np.where(p9.block == 'C', p9.UAV_WRI, np.nan); d['Diseased, training plots'] = np.where((p9.block != 'C') & (p9.split == 'TRAIN'), p9.UAV_WRI, np.nan); d['Diseased, test plots'] = np.where((p9.block != 'C') & (p9.split == 'TEST'), p9.UAV_WRI, np.nan)
        ad('c46', 'L9', 'Leaf WRI computed from the UAV plot spectra vs plot disease index', 'scatter', d, d.columns[1:], 'Plot DI (%) on 24 Feb 2026', 'WRI from UAV spectrum', ['1A9850', 'F46D43', '7F0000'])
        tf = T['l9_transfer']; ad('c47', 'L9', 'Detection of diseased test plots with leaf indices computed from UAV spectra (balanced accuracy)', 'col', tf[['feature', 'test_balanced_acc']], ['test_balanced_acc'], '', 'Balanced accuracy (15 test plots)', ['2F5D8A'], labels=True)
    return L
