"""Export the chart specifications, step texts, small tables and references to pptdata.json for the PowerPoint builder (d5_ppt.js)."""
import os, sys, json, pickle, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import d0_text, d2_specs, refs, configL as C
T = pickle.load(open(os.path.join(HERE, 'tables.pkl'), 'rb')); F = json.load(open(os.path.join(HERE, 'facts.json'))); STEPS = d0_text.steps(T, F); SP = d2_specs.specs(T, F)
def clean(v):
    if v is None: return None
    if isinstance(v, (float, np.floating)): return None if not np.isfinite(v) else float(round(float(v), 6))
    if isinstance(v, (np.integer,)): return int(v)
    return v
def lab(v):
    if isinstance(v, (float, np.floating)) and float(v).is_integer(): return str(int(v))
    return str(v)
charts = {}
for s in SP:
    d = s['data']; x = d.iloc[:, 0]
    charts[s['id']] = dict(id=s['id'], kind=s['kind'], title=s['title'], xlab=s['xlab'], ylab=s['ylab'], colors=s['colors'], note=s['note'], labels_on=bool(s.get('labels')), markers=bool(s.get('markers')),
                           line_series=s.get('line_series', []), point_colors=s.get('point_colors'), x=[clean(v) for v in x] if s['kind'] == 'scatter' else [lab(v) for v in x],
                           series=[dict(name=c, values=[clean(v) for v in d[c]]) for c in s['series']])
def rows(df, fmt=None, cols=None):
    df = df[cols] if cols else df; out = [list(map(str, df.columns))]
    for r in df.itertuples(index=False):
        out.append([('%.3f' % v if abs(v) < 100 else '%.1f' % v) if isinstance(v, (float, np.floating)) and np.isfinite(v) and not float(v).is_integer() else (str(int(v)) if isinstance(v, (float, np.floating, np.integer)) and np.isfinite(v) else ('—' if v is None or (isinstance(v, float) and not np.isfinite(v)) else str(v))) for v in r])
    return out
tabs = {}
tabs['checks'] = rows(T['l1_checks'][['Code', 'Check', 'Result', 'Status']])
tabs['ranges'] = rows(T['l52_ranges'])
tabs['vi'] = rows(T['l54_vi'])
tabs['dsf'] = [['Task', 'Features', 'DSF (after VIF < 10)']] + [[r.Task, str(r.DSF_size), r.DSF] for r in T['l55_dsf'].itertuples()]
tabs['jm'] = [[''] + ['G%d' % g for g in C.GRADES]] + [['G%d' % g] + ['%.2f' % T['l56_matrix'].loc[g, h] for h in C.GRADES] for g in C.GRADES]
tabs['wri_w'] = [['w', 'λ1', 'λ2', 'λ3', 'r']] + [['%g' % r.w, str(int(r.l1)), str(int(r.l2)), '—' if pd.isna(r.l3) else str(int(r.l3)), '%.3f' % r.r] for r in T['l53_wri_w'].sort_values('w').itertuples()]
tabs['clusters'] = [['Kept index', 'Removed (|r| ≥ 0.95 with the kept index)']] + [[r.Kept, r.Removed] for r in T['l54_clusters'].itertuples() if r.n_removed > 0]
tabs['split'] = rows(T['l2_counts'])
tabs['l4groups'] = [['Group', 'Indices', 'Strongest index (r with grade)']] + [[g, str(len(d)), '%s (%.2f)' % (d.loc[d['r with grade (all leaves)'].abs().idxmax(), 'Index'], d['r with grade (all leaves)'].abs().max())] for g, d in T['l4_defs'].groupby('Group', sort=False)]
if 'l6_ml' in T and len(T['l6_ml']):
    ml = T['l6_ml'].copy(); ml['grid'] = ml.grid_best.str.replace('"', '').str.replace(r'(svc__|svr__|kneighborsclassifier__|kneighborsregressor__)', '', regex=True).str.replace('n_neighbors', 'k').str.replace('n_components', 'comp').str.replace('min_samples_leaf', 'leaf').str.replace('max_features', 'mtry')
    ml['inner CV'] = [('%.3f' % v) if t != 'C' else 'RMSE %.3f' % -v for t, v in zip(ml.task, ml.grid_cv)]
    tabs['ml'] = [['Task', 'Model', 'SFFS features', 'Best grid setting', 'Inner CV']] + [[t, m, '%d of %d' % (a, b), g, c] for t, m, a, b, g, c in zip(ml.task, ml.model, ml.sffs_n, ml.dsf_size, ml.grid, ml['inner CV'])]
if 'l6_dl' in T and len(T['l6_dl']): tabs['dl'] = [['Task', 'Network', 'Epochs run', 'Best epoch', 'Best validation']] + [[r.task, r.model, str(r.epochs_run), str(r.best_epoch), ('OA %.3f' % r.best_val) if r.task != 'C' else 'RMSE %.3f' % -r.best_val] for r in T['l6_dl'].itertuples()]
if 'l7_metrics' in T:
    R = T['l7_metrics']; b = F['best']
    tabs['best'] = [['Task', 'Best model', 'Main metric (95% CI)', 'Other metrics']]
    for t in 'ABC':
        r = R[(R.task == t) & (R.model == b[t])].iloc[0]
        if t == 'A': tabs['best'].append([d2_specs.TASK[t], b[t], 'macro-F1 %.3f (%.3f–%.3f)' % (r.macro_F1, r.CI_low, r.CI_high), 'OA %.3f; kappa %.3f; sensitivity %.3f; specificity %.3f; AUC %.3f' % (r.OA, r.kappa, r.sensitivity, r.specificity, r.AUC)])
        if t == 'B': tabs['best'].append([d2_specs.TASK[t], b[t], 'macro-F1 %.3f (%.3f–%.3f)' % (r.macro_F1, r.CI_low, r.CI_high), 'OA %.3f; kappa %.3f; within one grade %.3f; QWK %.3f' % (r.OA, r.kappa, r.within1, r.QWK)])
        if t == 'C': tabs['best'].append([d2_specs.TASK[t], b[t], 'R² %.3f (%.3f–%.3f)' % (r.R2, r.CI_low, r.CI_high), 'RMSE %.2f; MAE %.2f; RPD %.2f; bias %+.2f' % (r.RMSE, r.MAE, r.RPD, r.bias)])
    for t, cols in (('A', ['model', 'OA', 'kappa', 'macro_F1', 'sensitivity', 'specificity', 'AUC']), ('B', ['model', 'OA', 'kappa', 'macro_F1', 'within1', 'QWK']), ('C', ['model', 'R2', 'RMSE', 'MAE', 'RPD'])):
        q = R[R.task == t].copy(); q['o'] = q.model.map({m: i for i, m in enumerate(d2_specs.MODELS)}); tabs['met' + t] = rows(q.sort_values('o'), cols=cols)
    cf = T['l7_conf']
    for t, labs in (('A', ['Healthy', 'Diseased']), ('B', ['G%d' % g for g in C.GRADES])):
        q = cf[(cf.task == t) & (cf.model == b[t])]; K = len(labs); A = np.zeros((K, K), int)
        for r in q.itertuples(): A[r.observed, r.predicted] = r.n
        tabs['conf' + t] = dict(labels=labs, m=A.tolist())
    low = T['l7_low']; tabs['low'] = [['Task', 'Model', 'Check', 'Leaves', 'Value']] + [[r.task, r.model, r.check, str(r.n), '%.3f' % r.value] for r in low.itertuples() if r.model == b[r.task]]
if 'l8_models' in T:
    tabs['l8'] = [['Task', 'M0 covariates', 'M1 (%s)' % '/'.join(sorted(set(T['l8_models'].M1_model))), 'M2 spectrum + cov.', 'ΔS = M1 − M0', 'ΔC = M2 − M1']] + [[d2_specs.TASK[r.task].split(' – ')[0] + ' (%s)' % r.metric.replace('macro_F1', 'macro-F1'), '%.3f' % r.M0, '%.3f' % r.M1, '%.3f' % r.M2, '%+.3f' % r.dS, '%+.3f' % r.dC] for r in T['l8_models'].itertuples()]
    g = T['l8_gains']; g = g[g.scope == 'all test leaves']; tabs['l8ci'] = [['Task', 'Gain', 'Value', '95% CI']] + [[r.task, r.gain, '%+.3f' % r.value, '%+.3f to %+.3f' % (r.CI_low, r.CI_high)] for r in g.itertuples()]
if 'l9_transfer' in T:
    tf = T['l9_transfer']; tabs['l9'] = [['Index', 'r UAV vs DI', 'r leaf vs UAV index', 'Test BA', 'Sens.', 'Spec.']] + [[r.feature, '%.2f' % r.r_UAV_vs_DI_all48, '%.2f' % r.r_leaf_vs_UAV_index, '%.2f' % r.test_balanced_acc, '%.2f' % r.test_sensitivity, '%.2f' % r.test_specificity] for r in tf.itertuples()]
dev = [['Code', 'Step', 'Situation in 2025-26', 'What was done']] + [['DEV-1', 'L1/L5.2', 'Residual splice step −0.002 at 1000 nm', 'Not corrected; FD 995–1005 nm excluded from band selection'], ['DEV-2', 'L1', 'One spectrum per leaf in the files', '"Average 2 readings" not applicable'],
       ['DEV-3', 'L2', '2255 leaves (not the 7488 of the 2026-27 plan)', 'Same plot split applied'], ['DEV-4', 'L5.3', 'WRI search chose w = 0', 'WRI = NDSI(780, 830)'], ['DEV-5', 'L7', 'Leaf data, not subplots', 'Low-severity check on grade-1 leaves (A) and grades 0–1 (C)'],
       ['DEV-6', 'L6', 'SFFS stability run time', '50 divisions (SVM, tasks A, B); 20 divisions with 100 trees (RF, task C)'], ['DEV-7', 'L9', 'One UAV date; no canopy selection', 'OW overlap not computed; plot-mean leaf spectra'], ['DEV-8', 'L10', 'No pre-symptomatic leaves', 'Not run'], ['DEV-9', 'L6–L8', 'Task C predictions outside 0–9', 'Clipped to 0–9']]
tabs['dev'] = dev
tabs['lit'] = d0_text.literature(T, F)
alltext = ' '.join(' '.join([p[0] for p in s['papers']] + s['mrefs']) for s in STEPS) + ' Conn et al. (1990) Selvaprakash et al. (2026) Cross et al. (2024)'
RL, MISS = refs.resolve(alltext)
steps = [dict(code=s['code'], title=s['title'], why=s['why'], what=s['what'], position=s['position'], samples=s['samples'], settings=s['settings'], mydata=s['mydata'], result=s['result'], output=s['output'], notes=s['notes'], q=s['q'],
              refs='; '.join(dict.fromkeys([p[0] for p in s['papers']] + s['mrefs']))) for s in STEPS]
json.dump(dict(charts=charts, tabs=tabs, steps=steps, refs=RL, facts=F), open(os.path.join(HERE, 'pptdata.json'), 'w'), ensure_ascii=False, default=float)
print('charts', len(charts), 'tables', len(tabs), 'refs', len(RL), 'missing', MISS)
