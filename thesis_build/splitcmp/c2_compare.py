"""Comparison of the three validation designs on the 2025-26 ASD leaf data:
LORO (earlier analysis, asd26) vs grouped 70:30 hold-out (asd7030) vs grouped 80:20 hold-out (asd8020).
Writes, for each split S, data/cmp_*.csv + data/cmp_summary.json + fig/f35-f39 into that pipeline (used by its Word/Excel/PPT),
and the three-way tables and figures into splitcmp/out and splitcmp/fig (used by the comparison report).
  (1) side by side   all metrics of every model under each design
  (2) paired         same test leaves: LORO predictions of exactly the split's test leaves vs the split's predictions,
                     difference with a 95% plot-bootstrap interval (2000 resamples of the test plots, healthy / unsprayed separately;
                     Efron and Tibshirani, 1993; Field and Welsh, 2007)
  (3) repeated       light pipeline over 20 other grouped splits vs LORO (from c1_repeat.py)
  (4) leakage        grouped vs random leaf-level splits (from c1_repeat.py)
  (5) overlap        Jaccard similarity of the selected optimal wavelengths and feature sets"""
import numpy as np, pandas as pd, json, os, warnings
warnings.filterwarnings('ignore')
from scipy.stats import rankdata
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle
from matplotlib.lines import Line2D
T = '/home/user/meta/thesis_build/'; L = T + 'asd26/data/'; OUT = T + 'splitcmp/out/'; FGC = T + 'splitcmp/fig/'
os.makedirs(OUT, exist_ok=True); os.makedirs(FGC, exist_ok=True)
SPLITS = [(tag, lab, T + 'asd%s/' % tag.replace('-', '')) for tag, lab in (('70-30', '70:30'), ('80-20', '80:20'))]
SPLITS = [s for s in SPLITS if os.path.exists(s[2] + 'data/all_predictions.csv')]
COL = {'LORO': '#7F7F7F', '70:30': '#2E75B6', '80:20': '#C55A11', 'leaf': '#C62828'}
plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 12, 'axes.titlesize': 13, 'axes.titleweight': 'bold', 'axes.titlelocation': 'left', 'axes.titlepad': 9,
                     'axes.labelsize': 12, 'xtick.labelsize': 11, 'ytick.labelsize': 11, 'legend.fontsize': 10, 'legend.frameon': False, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.edgecolor': '#4D4D4D', 'axes.linewidth': 0.9, 'axes.grid': True, 'grid.color': '#E6E6E6', 'grid.linewidth': 0.7, 'axes.axisbelow': True,
                     'figure.facecolor': 'white', 'savefig.facecolor': 'white', 'axes.titlecolor': '#1B2A1E'})
def save(fig, path): fig.savefig(path, dpi=300, bbox_inches='tight', pad_inches=0.08); plt.close(fig); print('  ', os.path.basename(path))
M = pd.read_csv(L + 'meta.csv'); PLOT = M['plot'].values; N = len(M)
MLM = ['SVM', 'RF', 'XGBoost', 'k-NN', 'PLS-DA', 'PLS']; DLM = ['DNN-F1', 'DT-EDNet', 'EfficientNet-B0', 'ResNet18', 'ConvNeXt V2-Atto']
MAINK = {'A': 'macro_F1', 'B': 'macro_F1', 'C': 'R2'}; PM = {'A': ['macro_F1', 'AUC', 'OA'], 'B': ['macro_F1', 'QWK', 'OA'], 'C': ['R2', 'RMSE']}
SIDEK = {'A': ['OA', 'kappa', 'macro_F1', 'sensitivity', 'specificity', 'AUC'], 'B': ['OA', 'kappa', 'macro_F1', 'QWK', 'within1'], 'C': ['R2', 'RMSE', 'MAE', 'RPD']}
LOWER = {'RMSE', 'MAE'}
mname = lambda m, t: {'SVM': 'SVR', 'PLS': 'PLSR'}.get(m, m) if t == 'C' else m
MK = {'macro_F1': 'macro-F1', 'R2': 'R²', 'QWK': 'QWK', 'AUC': 'AUC', 'OA': 'OA', 'RMSE': 'RMSE'}

# ---------------- fast metrics ----------------
def met(k, y, p, s=None, K=None):
    if k == 'macro_F1':
        cm = np.bincount(y * K + p, minlength=K * K).reshape(K, K); tp = np.diag(cm); den = cm.sum(0) + cm.sum(1); return float(np.mean(np.where(tp > 0, 2 * tp / np.maximum(den, 1), 0.0)))
    if k == 'OA': return float(np.mean(y == p))
    if k == 'AUC':
        r = rankdata(s); n1 = int((y == 1).sum()); n0 = len(y) - n1; return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)) if n1 and n0 else np.nan
    if k == 'QWK':
        O = np.bincount(y * K + p, minlength=K * K).reshape(K, K).astype(float); i = np.arange(K); W = (i[:, None] - i[None, :]) ** 2 / (K - 1) ** 2
        E = np.outer(O.sum(1), O.sum(0)) / O.sum(); return float(1 - (W * O).sum() / (W * E).sum())
    if k == 'R2': return float(1 - np.sum((y - p) ** 2) / np.sum((y - y.mean()) ** 2))
    if k == 'RMSE': return float(np.sqrt(np.mean((y - p) ** 2)))

def boot_idx(leaves, nb=2000, seed=11):
    pl = PLOT[leaves]; groups = [np.unique(pl[pl <= 12]), np.unique(pl[pl > 12])]; idx = {q: np.where(pl == q)[0] for q in np.unique(pl)}; rng = np.random.default_rng(seed)
    for _ in range(nb): yield np.concatenate([idx[q] for g in groups if len(g) for q in rng.choice(g, len(g), replace=True)])

LP = pd.read_csv(L + 'all_predictions.csv'); LMT = pd.read_csv(L + 'metrics_all.csv')
SMT = {lab: pd.read_csv(d + 'data/metrics_all.csv') for tag, lab, d in SPLITS}
SPP = {lab: pd.read_csv(d + 'data/all_predictions.csv') for tag, lab, d in SPLITS}
SPJ = {lab: json.load(open(d + 'data/split.json')) for tag, lab, d in SPLITS}

# ---------------- (1) side by side ----------------
rows3 = []
for t in 'ABC':
    for m in [x for x in LMT[LMT.task == t].model]:
        for k in SIDEK[t]:
            r = dict(task=t, model=m, type='ML' if m in MLM else 'DL', metric=k, LORO=float(LMT[(LMT.task == t) & (LMT.model == m)][k].iloc[0]))
            for lab in SMT:
                d = SMT[lab][(SMT[lab].task == t) & (SMT[lab].model == m)]; r[lab] = float(d[k].iloc[0]) if len(d) else np.nan; r['d_' + lab] = r[lab] - r['LORO']
            rows3.append(r)
S3 = pd.DataFrame(rows3); S3.to_csv(OUT + 'cmp3_side.csv', index=False)
for tag, lab, d in SPLITS:   # per-split copy for that pipeline's report
    S3[['task', 'model', 'type', 'metric', 'LORO']].assign(split=S3[lab], delta=S3['d_' + lab]).to_csv(d + 'data/cmp_side.csv', index=False)

# ---------------- (2) paired on the same test leaves ----------------
PAIR = {}
for tag, lab, d in SPLITS:
    rows = []
    for t in 'ABC':
        K = {'A': 2, 'B': 6, 'C': None}[t]
        for m in SPP[lab][SPP[lab].task == t].model.unique():
            a = SPP[lab][(SPP[lab].task == t) & (SPP[lab].model == m)].sort_values('leaf'); b = LP[(LP.task == t) & (LP.model == m)].set_index('leaf').loc[a.leaf.values]
            lv = a.leaf.values.astype(int); y = a.y.values; pa = a.pred.values; pb = b.pred.values; sa = a.score.values.astype(float) if t == 'A' else None; sb = b.score.values.astype(float) if t == 'A' else None
            if t in 'AB': y, pa, pb = y.astype(int), pa.astype(int), pb.astype(int)
            assert np.allclose(b.y.values, a.y.values)
            for k in PM[t]:
                if k == 'AUC' and (np.isnan(sa).any() or np.isnan(sb).any()): continue
                va, vb = met(k, y, pa, sa, K), met(k, y, pb, sb, K); bd = []
                for ii in boot_idx(lv): bd.append(met(k, y[ii], pa[ii], None if sa is None else sa[ii], K) - met(k, y[ii], pb[ii], None if sb is None else sb[ii], K))
                bd = np.array(bd); lo, hi = np.percentile(bd, [2.5, 97.5]); dl = va - vb; better = (dl < 0) if k in LOWER else (dl > 0)
                verdict = 'no real difference' if lo <= 0 <= hi else ('higher' if (lo > 0) != (k in LOWER) else 'lower')   # higher = better with the split
                rows.append(dict(task=t, model=m, type='ML' if m in MLM else 'DL', metric=k, n_leaves=len(lv), n_plots=len(np.unique(PLOT[lv])), LORO_same=vb, split=va, delta=dl, ci_low=lo, ci_high=hi,
                                 p_boot=float(min(1, 2 * min((bd <= 0).mean(), (bd >= 0).mean()))), verdict=verdict))
        print(lab, t, 'paired done', flush=True)
    P = pd.DataFrame(rows); PAIR[lab] = P; P.to_csv(d + 'data/cmp_paired_all.csv', index=False)
    P[P.metric == P.task.map(MAINK)].to_csv(d + 'data/cmp_paired.csv', index=False)
pd.concat([p.assign(split=l_) if False else p.assign(design=l_) for l_, p in PAIR.items()]).to_csv(OUT + 'cmp3_paired.csv', index=False)

# ---------------- (2b) diagnostics of the paired result: healthy vs unsprayed test leaves, LORO folds of the test plots, test-set difficulty
DIAG = {}
for tag, lab, d in SPLITS:
    rows = []
    for (t, m), a_ in SPP[lab].groupby(['task', 'model']):
        b_ = LP[(LP.task == t) & (LP.model == m)].set_index('leaf').loc[a_.leaf.values]; h = PLOT[a_.leaf.values.astype(int)] <= 12
        for nm, msk in (('healthy plots', h), ('unsprayed plots', ~h)):
            y = a_.y.values[msk]; pa = a_.pred.values[msk]; pb = b_.pred.values[msk]
            if t in 'AB': rows.append(dict(task=t, model=m, plots=nm, metric='OA', n=int(msk.sum()), LORO_same=float(np.mean(pb == y)), split=float(np.mean(pa == y))))
            else: rows.append(dict(task=t, model=m, plots=nm, metric='RMSE', n=int(msk.sum()), LORO_same=float(np.sqrt(np.mean((pb - y) ** 2))), split=float(np.sqrt(np.mean((pa - y) ** 2)))))
    BT = pd.DataFrame(rows); BT['delta'] = BT.split - BT.LORO_same; BT.to_csv(d + 'data/cmp_blocktype.csv', index=False)
    BS = BT.groupby(['task', 'plots', 'metric'], sort=False).agg(n=('n', 'first'), LORO_same=('LORO_same', 'mean'), split=('split', 'mean'), delta=('delta', 'mean')).reset_index(); BS.to_csv(d + 'data/cmp_blocktype_summary.csv', index=False)
    te_pl = SPJ[lab]['test_plots']; lf = M.groupby('plot').fold.first(); hp = [p_ for p_ in te_pl if p_ <= 12]
    fold_of = {p_: int(lf[p_]) for p_ in te_pl}; hf = sorted(set(fold_of[p_] for p_ in hp))
    same_h = len(hf) == 1 and set(M[(M.fold == hf[0]) & (M['plot'] <= 12)]['plot'].unique()) == set(hp)
    Pm = PAIR[lab][PAIR[lab].metric == PAIR[lab].task.map(MAINK)]
    lp_all = {t: float(np.mean([LMT[(LMT.task == t) & (LMT.model == m)][MAINK[t]].iloc[0] for m in Pm[Pm.task == t].model])) for t in 'ABC'}
    lp_same = {t: float(Pm[Pm.task == t].LORO_same.mean()) for t in 'ABC'}; sp_same = {t: float(Pm[Pm.task == t].split.mean()) for t in 'ABC'}
    ntr_loro = {f: int((M.fold != f).sum()) for f in range(3)}
    DIAG[lab] = dict(test_plot_loro_fold={str(k): v + 1 for k, v in fold_of.items()}, healthy_test_plots=hp, healthy_same_as_loro_fold=(hf[0] + 1) if same_h else None,
                     loro_pooled_mean=lp_all, loro_same_mean=lp_same, split_same_mean=sp_same, n_train_split=int(SPJ[lab]['n_train_leaves']), n_train_loro=ntr_loro,
                     blocktype=json.loads(BS.round(4).to_json(orient='records')))

# ---------------- (3)-(4) repeated splits and leakage ----------------
REP, REPS, LEAK = {}, {}, {}
for tag, lab, d in SPLITS:
    f = d + 'data/cmp_repeat_runs.csv'
    if not os.path.exists(f): continue
    R = pd.read_csv(f); REP[lab] = R; rs, lk = [], []
    for t in 'ABC':
        for k in PM[t]:
            if k not in R.columns or k == 'OA' and t == 'B': continue
            lo_ = R[(R.scheme == 'LORO') & (R.task == t)][k]; mn_ = R[(R.scheme == 'main ' + lab) & (R.task == t)][k]; g = R[(R.scheme == 'grouped ' + lab) & (R.task == t)][k]; lf = R[(R.scheme == 'leaf ' + lab) & (R.task == t)][k]
            if not len(g): continue
            lv = float(lo_.iloc[0]) if len(lo_) else np.nan; above = int((g < lv).sum()) if k in LOWER else int((g > lv).sum())
            rs.append(dict(task=t, metric=k, LORO_light=lv, main_light=float(mn_.iloc[0]) if len(mn_) else np.nan, rep_mean=g.mean(), rep_sd=g.std(ddof=1), rep_min=g.min(), rep_max=g.max(), rep_above=above, rep_n=len(g),
                           z=(g.mean() - lv) / g.std(ddof=1) * (-1 if k in LOWER else 1)))
            if len(lf): lk.append(dict(task=t, metric=k, grouped=g.mean(), grouped_sd=g.std(ddof=1), leaf=lf.mean(), leaf_sd=lf.std(ddof=1), inflation=(g.mean() - lf.mean()) if k in LOWER else (lf.mean() - g.mean())))
    REPS[lab] = pd.DataFrame(rs); LEAK[lab] = pd.DataFrame(lk)
    REPS[lab].to_csv(d + 'data/cmp_repeat_summary.csv', index=False); LEAK[lab].to_csv(d + 'data/cmp_leak.csv', index=False)
if REPS: pd.concat([v.assign(design=k) for k, v in REPS.items()]).to_csv(OUT + 'cmp3_repeat.csv', index=False)
if LEAK: pd.concat([v.assign(design=k) for k, v in LEAK.items()]).to_csv(OUT + 'cmp3_leak.csv', index=False)

# ---------------- (5) selection overlap ----------------
LS = json.load(open(L + 'fold_selection.json')); O1 = json.load(open(L + 'o1_results.json'))
SETS = {'All leaves (Obj. 1)': dict(OW=O1['OW'], DSF_B=O1['DSF']), **{'LORO fold %d' % (int(f) + 1): dict(OW=LS[f]['OW'], DSF_B=LS[f]['DSF']['B']) for f in sorted(LS)}}
for tag, lab, d in SPLITS:
    s0 = json.load(open(d + 'data/fold_selection.json'))['0']; SETS['%s training' % lab] = dict(OW=s0['OW'], DSF_B=s0['DSF']['B'])
names = list(SETS); jac = lambda a, b: len(set(a) & set(b)) / len(set(a) | set(b))
OV = {key: pd.DataFrame([[jac(SETS[a][key], SETS[b][key]) for b in names] for a in names], index=names, columns=names) for key in ('OW', 'DSF_B')}
with open(OUT + 'cmp3_overlap.csv', 'w') as fh:
    for key, df in OV.items(): fh.write('Jaccard similarity of %s\n' % key); df.round(3).to_csv(fh); fh.write('\n')
pd.DataFrame([dict(set=n, OW=', '.join(SETS[n]['OW']), DSF_B=', '.join(SETS[n]['DSF_B'])) for n in names]).to_csv(OUT + 'cmp3_sets.csv', index=False)

# ---------------- figures ----------------
LAY = {}
exec(open(T + 'asd7030/a1_prep.py').read().split('blk = lambda')[0].split('# ---- treatments')[1].split('\n', 1)[1])   # LAY dict of the field layout
BLOCKS = [('Healthy (sprayed) 1–12', range(1, 13)), ('R3 13–24', range(13, 25)), ('R2 25–36', range(25, 37)), ('R1 37–48', range(37, 49))]
def plotmap(ax, colour_of, title):
    for bi, (bn, rg) in enumerate(BLOCKS):
        for j, p in enumerate(rg):
            c = colour_of(p); ax.add_patch(Rectangle((j, -bi), 0.92, 0.82, facecolor=c, edgecolor='#555', lw=0.6))
            dark = c not in ('#FFFFFF', '#EEEEEE', '#F2F2F2', '#DDEBF7', '#FBE5D6')
            ax.text(j + 0.46, -bi + 0.53, str(p), ha='center', va='center', fontsize=8.5, color='white' if dark else '#222', fontweight='bold')
            ax.text(j + 0.46, -bi + 0.2, LAY[p], ha='center', va='center', fontsize=6.5, color='white' if dark else '#444')
        ax.text(-0.25, -bi + 0.41, bn, ha='right', va='center', fontsize=9.5)
    ax.set_xlim(-0.1, 12); ax.set_ylim(-3.3, 1.0); ax.axis('off'); ax.set_title(title, fontsize=12)
for tag, lab, d in SPLITS:
    FG = d + 'fig/'; os.makedirs(FG, exist_ok=True); TE = set(SPJ[lab]['test_plots']); C = COL[lab]; light = {'70:30': '#DDEBF7', '80:20': '#FBE5D6'}[lab]
    fig, ax = plt.subplots(figsize=(11, 3.6)); plotmap(ax, lambda p: C if p in TE else light, 'Grouped, stratified %s split: %d test plots (dark), %d training plots (light)' % (lab, len(TE), 48 - len(TE)))
    ax.legend([Patch(color=C), Patch(facecolor=light, edgecolor='#555')], ['test plot (%d leaves)' % SPJ[lab]['n_test_leaves'], 'training plot (%d leaves)' % SPJ[lab]['n_train_leaves']], loc='lower center', bbox_to_anchor=(0.5, -0.16), ncol=2)
    save(fig, FG + 'f35_split_map.png')
    # f36 side by side
    fig, axs = plt.subplots(1, 3, figsize=(15, 5.2))
    for ax, t in zip(axs, 'ABC'):
        k = MAINK[t]; dd = S3[(S3.task == t) & (S3.metric == k)].sort_values(lab); y_ = np.arange(len(dd))
        ax.barh(y_ - 0.2, dd.LORO, 0.38, color=COL['LORO'], label='LORO'); ax.barh(y_ + 0.2, dd[lab], 0.38, color=C, label=lab)
        ax.set_yticks(y_); ax.set_yticklabels([mname(m, t) for m in dd.model], fontsize=10); ax.set_xlabel(MK[k]); ax.grid(axis='y', visible=False)
        ax.set_xlim(max(0, min(dd.LORO.min(), dd[lab].min()) - 0.08), max(dd.LORO.max(), dd[lab].max()) + 0.04)
        ax.set_title({'A': 'A – detection', 'B': 'B – six grades', 'C': 'C – severity score'}[t])
    axs[0].legend(loc='lower right'); plt.tight_layout(); save(fig, FG + 'f36_cmp_side.png')
    # f37 paired forest
    P = PAIR[lab]; P_ = P[P.metric == P.task.map(MAINK)].copy(); P_['lab'] = [('%s  %s' % (t, mname(m, t))) for t, m in zip(P_.task, P_.model)]
    fig, ax = plt.subplots(figsize=(8.5, 0.32 * len(P_) + 1.4)); y_ = np.arange(len(P_))[::-1]
    for yy, r in zip(y_, P_.itertuples()):
        cc = '#2E7D32' if r.verdict == 'higher' else ('#C62828' if r.verdict == 'lower' else '#757575')
        ax.plot([r.ci_low, r.ci_high], [yy, yy], color=cc, lw=2); ax.plot(r.delta, yy, 'o', color=cc, ms=6)
    ax.axvline(0, color='#333', lw=1); ax.set_yticks(y_); ax.set_yticklabels(P_.lab, fontsize=9.5); ax.grid(axis='y', visible=False)
    ax.set_xlabel('%s − LORO on the same %d test leaves (macro-F1 for A and B, R² for C)' % (lab, P_.n_leaves.iloc[0]), fontsize=10.5)
    ax.legend([Line2D([], [], color='#2E7D32', marker='o'), Line2D([], [], color='#C62828', marker='o'), Line2D([], [], color='#757575', marker='o')], ['really higher with ' + lab, 'really lower with ' + lab, 'no real difference'], loc='lower right', fontsize=9)
    ax.set_title('Paired comparison on the same test leaves (95% plot-bootstrap intervals)', fontsize=12); save(fig, FG + 'f37_cmp_paired.png')
    if lab in REP:
        R = REP[lab]; fig, axs = plt.subplots(1, 3, figsize=(14, 4.6))
        for ax, t in zip(axs, 'ABC'):
            k = MAINK[t]; g = R[(R.scheme == 'grouped ' + lab) & (R.task == t)][k].values; lo_ = R[(R.scheme == 'LORO') & (R.task == t)][k].values; mn_ = R[(R.scheme == 'main ' + lab) & (R.task == t)][k].values
            ax.boxplot([g], positions=[0], widths=0.45, showfliers=False, medianprops=dict(color=C, lw=2), boxprops=dict(color='#555'), whiskerprops=dict(color='#555'), capprops=dict(color='#555'))
            ax.scatter(np.random.default_rng(1).normal(0, 0.06, len(g)), g, s=26, color=C, alpha=0.75, zorder=3, label='20 other %s splits' % lab)
            if len(lo_): ax.axhline(lo_[0], color=COL['LORO'], ls='--', lw=1.6, label='LORO')
            if len(mn_): ax.scatter([0.38], mn_, marker='D', s=60, color='#1B2A1E', zorder=4, label='main %s split' % lab)
            ax.set_xticks([]); ax.set_xlim(-0.6, 0.7); ax.set_ylabel(MK[k]); ax.set_title({'A': 'A – detection (SVM)', 'B': 'B – six grades (RF)', 'C': 'C – score (XGBoost)'}[t]); ax.grid(axis='x', visible=False)
        axs[0].legend(loc='lower left', fontsize=9); plt.tight_layout(); save(fig, FG + 'f38_cmp_repeat.png')
        Lk = LEAK[lab]; Lk_ = Lk[Lk.metric == Lk.task.map(MAINK)]
        fig, ax = plt.subplots(figsize=(7.5, 4.4)); x_ = np.arange(len(Lk_))
        ax.bar(x_ - 0.2, Lk_.grouped, 0.38, yerr=Lk_.grouped_sd, color=C, capsize=4, label='grouped %s (whole plots)' % lab)
        ax.bar(x_ + 0.2, Lk_.leaf, 0.38, yerr=Lk_.leaf_sd, color=COL['leaf'], capsize=4, label='random leaf-level %s' % lab)
        for xx, r in zip(x_, Lk_.itertuples()): ax.text(xx + 0.2, r.leaf + r.leaf_sd + 0.015, '%+.3f' % r.inflation, ha='center', fontsize=10, color=COL['leaf'])
        ax.set_xticks(x_); ax.set_xticklabels(['A detection\nmacro-F1', 'B six grades\nmacro-F1', 'C score\nR²']); ax.set_ylim(0, 1.05); ax.legend(loc='upper right', fontsize=9.5); ax.grid(axis='x', visible=False)
        ax.set_title('Leakage check: random leaf splits look better than they are', fontsize=12); save(fig, FG + 'f39_cmp_leak.png')

# three-way figures for the comparison report
fig, axs = plt.subplots(3, 1, figsize=(11, 10.5))
FCOL = {0: '#4472C4', 1: '#ED7D31', 2: '#70AD47'}
plotmap(axs[0], lambda p: FCOL[int(M[M['plot'] == p].fold.iloc[0])], 'LORO: three folds (colour = fold in which the plot is tested); every plot is tested once')
axs[0].legend([Patch(color=FCOL[i]) for i in range(3)], ['fold 1 (R1 + 4 healthy)', 'fold 2 (R2 + 4 healthy)', 'fold 3 (R3 + 4 healthy)'], loc='lower center', bbox_to_anchor=(0.5, -0.14), ncol=3, fontsize=9.5)
for ax, (tag, lab, d) in zip(axs[1:], SPLITS):
    TE = set(SPJ[lab]['test_plots']); light = {'70:30': '#DDEBF7', '80:20': '#FBE5D6'}[lab]
    plotmap(ax, lambda p: COL[lab] if p in TE else light, '%s: %d test plots (%d leaves, dark) tested once; %d training plots' % (lab, len(TE), SPJ[lab]['n_test_leaves'], 48 - len(TE)))
plt.tight_layout(); save(fig, FGC + 'c01_designs.png')
labs = ['LORO'] + [l for _, l, _ in SPLITS]
fig, axs = plt.subplots(1, 3, figsize=(16, 5.6))
for ax, t in zip(axs, 'ABC'):
    k = MAINK[t]; dd = S3[(S3.task == t) & (S3.metric == k)].sort_values('LORO'); y_ = np.arange(len(dd)); w = 0.8 / len(labs)
    for i, l_ in enumerate(labs): ax.barh(y_ + (i - (len(labs) - 1) / 2) * w, dd[l_], w, color=COL[l_], label=l_)
    ax.set_yticks(y_); ax.set_yticklabels([mname(m, t) for m in dd.model], fontsize=10); ax.set_xlabel(MK[k]); ax.grid(axis='y', visible=False)
    ax.set_xlim(max(0, dd[labs].min().min() - 0.08), dd[labs].max().max() + 0.04); ax.set_title({'A': 'A – detection', 'B': 'B – six grades', 'C': 'C – severity score'}[t])
axs[0].legend(loc='lower right'); plt.tight_layout(); save(fig, FGC + 'c02_side.png')
if PAIR:
    fig, axs = plt.subplots(1, len(PAIR), figsize=(7.2 * len(PAIR), 9), sharey=True); axs = np.atleast_1d(axs)
    for ax, (lab, P) in zip(axs, PAIR.items()):
        P_ = P[P.metric == P.task.map(MAINK)]; y_ = np.arange(len(P_))[::-1]
        for yy, r in zip(y_, P_.itertuples()):
            cc = '#2E7D32' if r.verdict == 'higher' else ('#C62828' if r.verdict == 'lower' else '#757575'); ax.plot([r.ci_low, r.ci_high], [yy, yy], color=cc, lw=2); ax.plot(r.delta, yy, 'o', color=cc, ms=6)
        ax.axvline(0, color='#333', lw=1); ax.set_yticks(y_); ax.set_yticklabels(['%s  %s' % (t, mname(m, t)) for t, m in zip(P_.task, P_.model)], fontsize=9.5); ax.grid(axis='y', visible=False)
        ax.set_xlabel('%s − LORO, same %d test leaves' % (lab, P_.n_leaves.iloc[0])); ax.set_title('%s vs LORO' % lab, color=COL[lab])
    plt.tight_layout(); save(fig, FGC + 'c03_paired.png')
if REP:
    fig, axs = plt.subplots(1, 3, figsize=(14, 4.8))
    for ax, t in zip(axs, 'ABC'):
        k = MAINK[t]; lo_ = None
        for i, (lab, R) in enumerate(REP.items()):
            g = R[(R.scheme == 'grouped ' + lab) & (R.task == t)][k].values; mn_ = R[(R.scheme == 'main ' + lab) & (R.task == t)][k].values; lo_ = R[(R.scheme == 'LORO') & (R.task == t)][k].values
            ax.boxplot([g], positions=[i], widths=0.45, showfliers=False, medianprops=dict(color=COL[lab], lw=2)); ax.scatter(i + np.random.default_rng(i).normal(0, 0.06, len(g)), g, s=22, color=COL[lab], alpha=0.75, zorder=3)
            if len(mn_): ax.scatter([i + 0.35], mn_, marker='D', s=50, color='#1B2A1E', zorder=4)
        if lo_ is not None and len(lo_): ax.axhline(lo_[0], color=COL['LORO'], ls='--', lw=1.6)
        ax.set_xticks(range(len(REP))); ax.set_xticklabels(['%s\n(20 splits)' % l_ for l_ in REP]); ax.set_ylabel(MK[k]); ax.grid(axis='x', visible=False)
        ax.set_title({'A': 'A – detection (SVM)', 'B': 'B – six grades (RF)', 'C': 'C – score (XGBoost)'}[t])
    axs[0].legend([Line2D([], [], color=COL['LORO'], ls='--'), Line2D([], [], marker='D', ls='', color='#1B2A1E')], ['LORO (same light pipeline)', 'main split of the full analysis'], loc='lower left', fontsize=9)
    plt.tight_layout(); save(fig, FGC + 'c04_repeat.png')
if LEAK:
    fig, ax = plt.subplots(figsize=(9, 4.6)); x_ = np.arange(3); w = 0.8 / (2 * len(LEAK)); i = 0
    for lab, Lk in LEAK.items():
        Lk_ = Lk[Lk.metric == Lk.task.map(MAINK)]
        ax.bar(x_ + (i - len(LEAK) + 0.5) * w, Lk_.grouped, w, yerr=Lk_.grouped_sd, color=COL[lab], capsize=3, label='grouped %s' % lab); i += 1
        ax.bar(x_ + (i - len(LEAK) + 0.5) * w, Lk_.leaf, w, yerr=Lk_.leaf_sd, color=COL[lab], alpha=0.45, hatch='//', capsize=3, label='random leaf-level %s' % lab); i += 1
    ax.set_xticks(x_); ax.set_xticklabels(['A detection macro-F1', 'B six grades macro-F1', 'C score R²']); ax.set_ylim(0, 1.05); ax.legend(fontsize=9, ncol=2); ax.grid(axis='x', visible=False)
    ax.set_title('Grouped vs random leaf-level splits', fontsize=12); save(fig, FGC + 'c05_leak.png')
fig, axs = plt.subplots(1, 2, figsize=(14, 5.6))
for ax, (key, ttl) in zip(axs, (('OW', 'Optimal wavelengths (SHAP-CARS)'), ('DSF_B', 'Disease-specific feature set, six grades'))):
    im = ax.imshow(OV[key].values, cmap='Greens', vmin=0, vmax=1); ax.set_xticks(range(len(names))); ax.set_xticklabels(names, rotation=40, ha='right', fontsize=9.5); ax.set_yticks(range(len(names))); ax.set_yticklabels(names, fontsize=9.5)
    for a_ in range(len(names)):
        for b_ in range(len(names)): ax.text(b_, a_, '%.2f' % OV[key].values[a_, b_], ha='center', va='center', fontsize=8.5, color='white' if OV[key].values[a_, b_] > 0.6 else '#222')
    ax.set_title(ttl + ' – Jaccard similarity', fontsize=11.5); ax.grid(False)
plt.tight_layout(); save(fig, FGC + 'c06_overlap.png')

# ---------------- summary sentences ----------------
SUMM3 = {}
for tag, lab, d in SPLITS:
    P = PAIR[lab]; Pm = P[P.metric == P.task.map(MAINK)]; nh, nl = int((Pm.verdict == 'higher').sum()), int((Pm.verdict == 'lower').sum()); n0 = len(Pm) - nh - nl
    side = S3[S3.metric == S3.task.map(MAINK)]; mdA, mdB, mdC = [side[side.task == t]['d_' + lab].mean() for t in 'ABC']
    J = dict(label=lab, n_test=int(SPJ[lab]['n_test_leaves']), n_test_plots=int(SPJ[lab]['n_test_plots']), n_train=int(SPJ[lab]['n_train_leaves']), paired_higher=nh, paired_lower=nl, paired_none=n0, paired_n=len(Pm),
             mean_delta_side=dict(A=mdA, B=mdB, C=mdC))
    s1 = 'On the same %d test leaves, the %s models were really better than LORO in %d of %d model–task comparisons, really worse in %d and not different in %d (95%% plot-bootstrap intervals).' % (J['n_test'], lab, nh, len(Pm), nl, n0)
    rep_txt, leak_txt, zs = '', '', {}
    if lab in REPS:
        Rs = REPS[lab]; Rm = Rs[Rs.metric == Rs.task.map(MAINK)].set_index('task'); zs = {t: float(Rm.loc[t, 'z']) for t in 'ABC'}
        rep_txt = ('With the same light pipeline, LORO gave macro-F1 %.3f (detection), %.3f (six grades) and R² %.3f (score). Over 20 other grouped %s splits the hold-out accuracy moved from %.3f to %.3f, %.3f to %.3f and %.3f to %.3f '
                   '(mean %.3f, %.3f and %.3f; SD %.3f, %.3f and %.3f); %d, %d and %d of the 20 splits were above LORO. The main %s split gave %.3f, %.3f and %.3f, so it sits %s the range of other possible splits.') % (
            Rm.loc['A', 'LORO_light'], Rm.loc['B', 'LORO_light'], Rm.loc['C', 'LORO_light'], lab, Rm.loc['A', 'rep_min'], Rm.loc['A', 'rep_max'], Rm.loc['B', 'rep_min'], Rm.loc['B', 'rep_max'], Rm.loc['C', 'rep_min'], Rm.loc['C', 'rep_max'],
            Rm.loc['A', 'rep_mean'], Rm.loc['B', 'rep_mean'], Rm.loc['C', 'rep_mean'], Rm.loc['A', 'rep_sd'], Rm.loc['B', 'rep_sd'], Rm.loc['C', 'rep_sd'], Rm.loc['A', 'rep_above'], Rm.loc['B', 'rep_above'], Rm.loc['C', 'rep_above'], lab,
            Rm.loc['A', 'main_light'], Rm.loc['B', 'main_light'], Rm.loc['C', 'main_light'],
            'inside' if all(Rm.loc[t, 'rep_min'] <= Rm.loc[t, 'main_light'] <= Rm.loc[t, 'rep_max'] for t in 'ABC') else 'partly outside')
        Lk = LEAK[lab]; Lm = Lk[Lk.metric == Lk.task.map(MAINK)].set_index('task')
        leak_txt = ('Random leaf-level %s splits, which put leaves of the same plot in training and test, gave macro-F1 %.3f and %.3f and R² %.3f, against %.3f, %.3f and %.3f for grouped splits: an apparent gain of %+.3f, %+.3f and %+.3f that is due only to leakage '
                    '(Roberts et al., 2017; Kattenborn et al., 2022).') % (lab, Lm.loc['A', 'leaf'], Lm.loc['B', 'leaf'], Lm.loc['C', 'leaf'], Lm.loc['A', 'grouped'], Lm.loc['B', 'grouped'], Lm.loc['C', 'grouped'], Lm.loc['A', 'inflation'], Lm.loc['B', 'inflation'], Lm.loc['C', 'inflation'])
    share = {}
    if lab in REPS:
        Rs = REPS[lab]; Rm = Rs[Rs.metric == Rs.task.map(MAINK)].set_index('task'); share = {t: float(Rm.loc[t, 'rep_above'] / Rm.loc[t, 'rep_n']) for t in 'ABC'}
    fh = nh / len(Pm); msh = float(np.mean(list(share.values()))) if share else None
    dg = DIAG[lab]; tr_gain = 100 * (dg['n_train_split'] / np.mean(list(dg['n_train_loro'].values())) - 1)
    why = (' In LORO a whole replication is left out of training, so every test leaf comes from a field block the model has never seen; in the %s split the training plots include every replication (and the training set is %.0f%% larger than a LORO training part), so the test is closer to prediction within known field blocks than to prediction in a new block (Roberts et al., 2017).' % (lab, tr_gain))
    if nh == 0 and nl == 0: verdict = 'No: on the same test leaves the %s models are as accurate as the LORO models; the differences in the raw numbers come from which leaves are tested.' % lab
    elif nl > nh: verdict = 'No: on the same test leaves the %s models are less accurate than the LORO models more often than they are more accurate.' % lab
    elif msh is None: verdict = 'On the same test leaves the %s models are higher than LORO in %d of %d comparisons and lower in %d; whether this holds for other %s splits is tested with the repeated splits.' % (lab, nh, len(Pm), nl, lab)
    elif fh >= 0.4 and nl == 0 and msh >= 0.75: verdict = ('Yes, the numbers are higher, but for a reason that does not make the models better: the %s split gives higher accuracy than LORO on the same test leaves and in most other %s splits (%.0f%% of them above LORO).' % (lab, lab, 100 * msh)) + why
    elif fh >= 0.4 and nl == 0: verdict = 'Only partly: the %s models are higher than LORO on these test leaves, but other %s splits are not consistently higher (%.0f%% of them above LORO), so the gain depends on which plots are drawn.' % (lab, lab, 100 * msh)
    else: verdict = 'Mixed: some %s models are higher and some are not different from LORO on the same leaves; %.0f%% of other %s splits are above LORO.' % (lab, 100 * msh, lab)
    hs = [b for b in dg['blocktype'] if b['task'] == 'A']
    diag_txt = ('The %d test leaves were harder than average for LORO: on them the LORO models reached mean macro-F1 %.3f (detection) and R² %.3f (score), against %.3f and %.3f over all %d leaves. ' % (J['n_test'], dg['loro_same_mean']['A'], dg['loro_same_mean']['C'], dg['loro_pooled_mean']['A'], dg['loro_pooled_mean']['C'], N)
                + ('The gain was not limited to the unsprayed plots: detection accuracy rose from %.3f to %.3f on the leaves of the healthy test plots and from %.3f to %.3f on the unsprayed test plots (mean of the ten models). ' % (hs[0]['LORO_same'], hs[0]['split'], hs[1]['LORO_same'], hs[1]['split']) if len(hs) == 2 else '')
                + ('The healthy test plots (%s) are exactly the healthy plots that LORO fold %d tested, so the healthy training plots were the same in both designs; the difference lies in the unsprayed training plots, which in the %s split come from all three replications.' % (', '.join(map(str, dg['healthy_test_plots'])), dg['healthy_same_as_loro_fold'], lab) if dg['healthy_same_as_loro_fold'] else ''))
    J['diag_sentence'] = diag_txt; J['share_above'] = share
    J['verdict'] = verdict; J['z'] = zs
    J['summary_sentence'] = s1 + ' ' + verdict
    J['repeat_sentence'] = rep_txt; J['leak_sentence'] = leak_txt
    J['qa_better'] = verdict + ' ' + s1 + (' ' + rep_txt.split('. The main')[0] + '.' if rep_txt else '')
    J['diag'] = DIAG[lab]
    J['answer'] = verdict + ' ' + s1 + ' ' + diag_txt + (' ' + rep_txt if rep_txt else '') + (' ' + leak_txt if leak_txt else '') + ' For new fields and seasons the relevant question is prediction in an unseen block, which LORO measures; LORO therefore remains the main accuracy estimate (it also tests every leaf once), and the %s models are kept as deployable models with their test-plot accuracy (Kohavi, 1995; Roberts et al., 2017; Vabalas et al., 2019).' % lab
    json.dump(J, open(d + 'data/cmp_summary.json', 'w'), indent=1, default=float); SUMM3[lab] = J; print(lab, J['summary_sentence'])
json.dump(SUMM3, open(OUT + 'cmp3_summary.json', 'w'), indent=1, default=float)
print('comparison done')
