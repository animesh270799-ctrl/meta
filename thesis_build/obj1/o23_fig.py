"""Dummy figures and numbers for Objectives 2 and 3 (six grades 0, 1, 3, 5, 7, 9 and PDI), from the Objective 1 simulation."""
import os, json, shutil
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, confusion_matrix, cohen_kappa_score, r2_score, mean_squared_error, precision_recall_fscore_support

D = os.path.dirname(os.path.abspath(__file__)) + '/'; F = D + 'fig/'
plt.rcParams['font.family'] = 'DejaVu Sans'
rng = np.random.default_rng(5)
Z = np.load(D + 'o1_sim.npz'); cls = Z['cls']; n = len(cls)
# observed PDI includes visual-scoring noise of diseased plots (sd 7 PDI units)
PDI = np.clip(Z['DI'] + np.where(cls > 0, np.random.default_rng(9).normal(0, 7, n), 0), 0, 100)
GL = ['0', '1', '3', '5', '7', '9']; GC = ['#2E7D32', '#9CCC65', '#FDD835', '#FB8C00', '#E53935', '#7B1FA2']
feat = lambda s, f: Z['%s|%s' % (s, f)]
# three replications (LORO folds), stratified by grade
rep = np.empty(n, int)
for k in range(6):
    idx = np.where(cls == k)[0]; rng.shuffle(idx); rep[idx] = np.arange(len(idx)) % 3
OUT = {}

def loro(model_fn, X, y):
    pred = np.empty(len(y), dtype=float)
    for r in range(3):
        tr, te = rep != r, rep == r
        m = model_fn().fit(X[tr], y[tr]); pred[te] = m.predict(X[te])
    return pred

# ---------------- DSF pools ----------------
DSF = {'HS': ['PSSRa', 'REP (nm)', 'WRI', 'DWSI-1', 'DWSI-5', 'NDWI'], 'MS': ['NDRE', 'PSRI_MS', 'MTCI', 'CON_NIR'],
       'RGB': ['Contrast_G', 'Hue', 'VF', 'Entropy_G'], 'TIR': ['CTD (°C)', 'NRCT', 'MTD (°C)', 'CON_T']}

# ---------------- VIF on a dummy HS pool ----------------
pool = {f: feat('HS', f) for f in ['PSSRa', 'REP (nm)', 'WRI', 'DWSI-1', 'DWSI-5', 'NDWI', 'NDVI780', 'PSRI', 'PRI']}
pool['SR850'] = (1 + pool['NDVI780']) / (1 - pool['NDVI780'] + 1e-3) + rng.normal(0, 0.15, n)
pool['NDVI850'] = pool['NDVI780'] + rng.normal(0, 0.006, n)
def vifs(P):
    names = list(P); X = np.column_stack([P[k] for k in names]); out = {}
    for j, k in enumerate(names):
        o = np.delete(X, j, 1); r2 = LinearRegression().fit(o, X[:, j]).score(o, X[:, j]); out[k] = 1 / max(1 - r2, 1e-6)
    return out
vrows = []; P = dict(pool)
while True:
    v = vifs(P); top = sorted(v.items(), key=lambda x: -x[1])
    txt = '; '.join('%s %.1f' % (k, x) for k, x in top[:4]) + ('; others < %.1f' % top[4][1] if len(top) > 4 else '')
    if top[0][1] < 10: vrows.append([txt, 'All VIF < 10: stop (%d features kept)' % len(P)]); break
    vrows.append([txt, 'Remove %s' % top[0][0]]); del P[top[0][0]]
OUT['vif'] = vrows

# ---------------- ML-SFFS on the fused pool (six grades, macro-F1) ----------------
names = [(s, f) for s in DSF for f in DSF[s]]
Xall = np.column_stack([feat(s, f) for s, f in names]); lab = ['%s (%s)' % (f, s) for s, f in names]
models = {'SVM': lambda: make_pipeline(StandardScaler(), SVC(C=10, gamma='scale', class_weight='balanced')),
          'k-NN': lambda: make_pipeline(StandardScaler(), KNeighborsClassifier(7)),
          'RF': lambda: RandomForestClassifier(150, min_samples_leaf=2, class_weight='balanced', random_state=0, n_jobs=-1)}
def score(fn, cols): return f1_score(cls, loro(fn, Xall[:, cols], cls).astype(int), average='macro')
def sffs(fn, kmax=8):
    sel, best = [], {}
    while len(sel) < kmax:
        cand = [(score(fn, sel + [j]), j) for j in range(Xall.shape[1]) if j not in sel]
        s, j = max(cand); sel = sel + [j]
        while len(sel) > 2:                       # floating (conditional exclusion)
            rem = [(score(fn, [q for q in sel if q != r]), r) for r in sel[:-1]]
            s2, r = max(rem)
            if s2 > best.get(len(sel) - 1, (0,))[0] + 1e-9: sel = [q for q in sel if q != r]; s = s2; best[len(sel)] = (s, list(sel))
            else: break
        if s > best.get(len(sel), (0,))[0]: best[len(sel)] = (s, list(sel))
    ks = sorted(best); sc = [best[k][0] for k in ks]; top = max(sc)
    kopt = min(k for k in ks if best[k][0] >= top - 0.01)
    return ks, sc, kopt, best[kopt]
fig, ax = plt.subplots(figsize=(7.6, 4.2)); OUT['sffs'] = {}
for (m, fn), c in zip(models.items(), ['#1565C0', '#C98A00', '#2E7D32']):
    ks, sc, kopt, (sopt, sel) = sffs(fn)
    ax.plot(ks, sc, '-o', color=c, ms=4, label=m); ax.plot(kopt, sopt, '*', color=c, ms=16, mec='k')
    OUT['sffs'][m] = [', '.join(lab[q] for q in sel), round(float(sopt), 2), kopt]
ax.set_xlabel('Number of selected features'); ax.set_ylabel('Macro-F1 (six grades, LORO)'); ax.legend(frameon=False)
ax.set_title('Dummy ML-SFFS on the fused DSF pool (star = optimum feature combination)', fontsize=9.5)
plt.tight_layout(); plt.savefig(F + 'o2_sffs.png', dpi=200); plt.close()

# ---------------- single sensors vs combinations ----------------
sets = {'S1 RGB': ['RGB'], 'S2 MS': ['MS'], 'S3 HS': ['HS'], 'S4 TIR': ['TIR'], 'S5 RGB+TIR': ['RGB', 'TIR'], 'S6 MS+TIR': ['MS', 'TIR'], 'S7 HS+TIR': ['HS', 'TIR'], 'S8 all four': ['HS', 'MS', 'RGB', 'TIR']}
res = {}
for k, ss in sets.items():
    X = np.column_stack([feat(s, f) for s in ss for f in DSF[s]])
    pc = loro(models['SVM'], X, cls).astype(int)
    pr = loro(lambda: RandomForestRegressor(300, min_samples_leaf=2, random_state=0, n_jobs=-1), X, PDI)
    res[k] = (f1_score(cls, pc, average='macro'), r2_score(PDI, pr), pc, pr)
fig, axs = plt.subplots(1, 2, figsize=(12, 4.2))
for a, j, yl in ((axs[0], 0, 'Macro-F1 (six grades)'), (axs[1], 1, 'R² (PDI)')):
    v = [res[k][j] for k in sets]; cc = ['#9E9E9E'] * 4 + ['#1565C0'] * 4
    a.bar(range(8), v, color=cc); a.set_xticks(range(8), list(sets), rotation=30, ha='right', fontsize=8); a.set_ylabel(yl)
    for i, x in enumerate(v): a.text(i, x + 0.01, '%.2f' % x, ha='center', fontsize=8)
    a.set_ylim(0, 1.05 if j else max(v) + 0.15)
axs[0].set_title('(a) Classification: SVM on DSFs (LORO)', fontsize=10); axs[1].set_title('(b) PDI regression: RFR on DSFs (LORO)', fontsize=10)
plt.tight_layout(); plt.savefig(F + 'o2_fusion.png', dpi=200); plt.close()
OUT['fusion'] = {k: [round(float(res[k][0]), 2), round(float(res[k][1]), 2)] for k in sets}

# ---------------- evaluation of the best set ----------------
best = max(sets, key=lambda k: res[k][0]); bestR = max(sets, key=lambda k: res[k][1])
pc = res[best][2]; pr = res[bestR][3]
cm = confusion_matrix(cls, pc, labels=range(6)); P_, R_, F_, _ = precision_recall_fscore_support(cls, pc, labels=range(6), zero_division=0)
adj = float(np.mean(np.abs(pc - cls) <= 1)); rmse = float(np.sqrt(mean_squared_error(PDI, pr)))
OUT['cm'] = {'set': best, 'setR': bestR, 'P': ['%.2f' % x for x in P_], 'R': ['%.2f' % x for x in R_], 'F1': ['%.2f' % x for x in F_],
             'oa': '%.2f' % np.mean(pc == cls), 'kap': '%.2f' % cohen_kappa_score(cls, pc), 'mf1': '%.2f' % f1_score(cls, pc, average='macro'),
             'adj': '%.2f' % adj, 'r2': '%.2f' % r2_score(PDI, pr), 'rmse': '%.1f' % rmse, 'nrmse': '%.2f' % (rmse / PDI.mean())}
fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.6))
im = axs[0].imshow(cm, cmap='Blues')
for i in range(6):
    for j in range(6): axs[0].text(j, i, cm[i, j], ha='center', va='center', fontsize=9, color='white' if cm[i, j] > cm.max() / 2 else 'k')
axs[0].set_xticks(range(6), GL); axs[0].set_yticks(range(6), GL); axs[0].set_xlabel('Predicted grade'); axs[0].set_ylabel('Observed grade')
axs[0].set_title('(a) Confusion matrix, %s (OA %s, macro-F1 %s,\n±1-grade accuracy %s)' % (best, OUT['cm']['oa'], OUT['cm']['mf1'], OUT['cm']['adj']), fontsize=9.5)
axs[1].scatter(PDI, pr, c=[GC[k] for k in cls], s=12, alpha=0.7); axs[1].plot([0, 100], [0, 100], 'k--', lw=1)
axs[1].set_xlim(0, 100); axs[1].set_ylim(0, 100); axs[1].set_xlabel('Observed PDI (%)'); axs[1].set_ylabel('Predicted PDI (%)')
axs[1].set_title('(b) Observed vs predicted PDI, %s (R² %s, RMSE %s)' % (bestR, OUT['cm']['r2'], OUT['cm']['rmse']), fontsize=9.5)
plt.tight_layout(); plt.savefig(F + 'o2_eval.png', dpi=200); plt.close()

# ---------------- maps (one flight, 72 plots) ----------------
pick = np.concatenate([rng.choice(np.where(cls == k)[0], m, replace=False) for k, m in enumerate([24, 10, 8, 12, 10, 8])]); rng.shuffle(pick)
from matplotlib.colors import ListedColormap
fig, axs = plt.subplots(1, 3, figsize=(13, 3.6))
for a, v, t, cm_ in ((axs[0], cls[pick], 'Observed grade', ListedColormap(GC)), (axs[1], pc[pick], 'Predicted grade (%s)' % best, ListedColormap(GC)), (axs[2], np.abs(pr[pick] - PDI[pick]), '|PDI error| (%)', 'Reds')):
    g = v.reshape(3, 24); kw = dict(vmin=-0.5, vmax=5.5) if t != '|PDI error| (%)' else dict(vmin=0, vmax=25)
    im = a.imshow(g, cmap=cm_, aspect='auto', **kw); a.set_yticks(range(3), ['R1', 'R2', 'R3']); a.set_xticks([]); a.set_title(t, fontsize=10)
    for x in np.arange(-0.5, 24, 1): a.axvline(x, color='w', lw=0.6)
    for y in (0.5, 1.5): a.axhline(y, color='w', lw=1.5)
    cb = plt.colorbar(im, ax=a, orientation='horizontal', pad=0.05, fraction=0.08)
    if t != '|PDI error| (%)': cb.set_ticks(range(6)); cb.set_ticklabels(GL)
plt.suptitle('Dummy plot maps for one flight (72 plots in three replications)', fontsize=10.5); plt.tight_layout(); plt.savefig(F + 'o2_maps.png', dpi=200); plt.close()

# ---------------- copied binary-task figures (no change with grades) ----------------
for a, b in (('m16_presym.png', 'o3_presym.png'), ('m17_risk.png', 'o3_risk.png'), ('f2_dnn_fusion.png', 'o2_dnn.png')):
    shutil.copy(D + '../final/fig/' + a, F + b)

json.dump(OUT, open(D + 'o23_dummy.json', 'w'), indent=1)
print(json.dumps(OUT, indent=0)[:1800])
