"""Export the numbers the PPT needs (native charts) to data/ppt.json."""
import numpy as np, pandas as pd, json, os
B = os.path.dirname(os.path.abspath(__file__)) + '/'; D = B + 'data/'
Z = np.load(D + 'prep.npz'); M = pd.read_csv(D + 'meta_leaf2.csv'); P = pd.read_csv(D + 'plot_table.csv'); F = pd.read_csv(D + 'feat_leaf_wri.csv')
R1 = json.load(open(D + 'res1.json')); RS = R1['RES']; R2 = json.load(open(D + 'res2.json')); info = json.load(open(D + 'prep_info.json'))
wl = Z['b5']; y = M.grade.values; G6 = [0, 1, 3, 5, 7, 9]
r = lambda v, k=3: [round(float(x), k) for x in v]
sel10 = [i for i, w in enumerate(wl) if w % 10 == 0]
S = pd.read_csv(D + 't_scalogram.csv'); W = pd.read_csv(D + 't_relieff.csv'); A = pd.read_csv(D + 't_anova.csv')
out = dict(
    n_leaves=int(len(M)), n_plotdates=int(len(P)), dates=sorted(M.date.unique()),
    counts={d: [int(((M.date == d) & (y == g)).sum()) for g in G6] for d in sorted(M.date.unique())},
    pdi_date={d: round(float(P.PDI[P.date == d].mean()), 1) for d in sorted(P.date.unique())},
    wl10=[int(wl[i]) for i in sel10], spec={str(g): r(Z['R'][y == g].mean(0)[sel10], 4) for g in G6},
    wl5=[int(w) for w in wl], scal={t: r(S['r_' + t].values[sel10]) for t in ('R', 'FD', 'SD')}, relief={t: r(W['W_' + t].values[sel10], 4) for t in ('R', 'FD', 'SD')},
    t2=RS['tier2'], t3=RS['tier3'], t5=RS['tier5'], t6=RS['tier6'],
    wri_means=[round(float(F.WRI_VNIR[y == g].mean()), 4) for g in G6], wri_swir_means=[round(float(F.WRI_SWIR[y == g].mean()), 4) for g in G6],
    anova_top=A.head(12)[['Feature', 'F', 'eta2', 'r_PDI_plot']].round(3).values.tolist(), letters=RS['tier4']['letters'],
    swir=A[A.Group == 'SWIR index'][['Feature', 'F', 'r_PDI_plot']].round(3).values.tolist(),
    base_top_r=A[A.Group == 'Index'].assign(a=lambda d: d.r_PDI_plot.abs()).sort_values('a', ascending=False).head(6)[['Feature', 'r_PDI_plot']].round(3).values.tolist(),
    boruta_c=pd.read_csv(D + 't_boruta_cls.csv').head(12)[['Feature', 'Importance', 'Decision']].round(4).values.tolist(),
    boruta_r=pd.read_csv(D + 't_boruta_reg.csv').head(12)[['Feature', 'Importance', 'Decision']].round(4).values.tolist(),
    cls={k: {q: (round(v[q], 3) if isinstance(v[q], float) else v[q]) for q in ('oa', 'kappa', 'macro_f1', 'adj', 'detection_acc', 'F1', 'cm')} for k, v in R2['cls'].items()},
    reg={k: {q: round(v[q], 3) for q in ('r2', 'rmse', 'nrmse', 'rpd')} for k, v in R2['reg'].items()},
    best=R2['best'], by_date=R2['by_date'], by_variety=R2['by_variety'],
    folds=[dict(rep=f['test_rep'], boruta_cls=f['boruta_cls'], boruta_reg=f['boruta_reg'], vif_cls=len(f['vif_cls']), vif_reg=len(f['vif_reg']),
                ofc={k: f['ofc'][k]['features'] for k in f['ofc']}) for f in R2['folds']],
    splice=[round(info['splice_mean'], 4), round(info['splice_sd'], 4)])
pr = pd.read_csv(D + 'pred_reg.csv'); bu = [c for c in pr.columns if c.startswith('pred_Bottom')][0]
out['obs'] = r(pr.observed_PDI, 1); out['pred_best'] = r(pr['pred_' + R2['best']['reg']], 1); out['pred_bu'] = r(pr[bu], 1); out['bu_name'] = bu[5:]
json.dump(out, open(D + 'ppt.json', 'w'), default=lambda o: o.item() if hasattr(o, 'item') else str(o))
print('ppt.json ok')
