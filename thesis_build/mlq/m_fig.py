"""Figures for the ML question-answer guide: all simulated or schematic (no thesis results)."""
import os, sys, shutil
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from scipy.interpolate import PchipInterpolator
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.model_selection import cross_val_predict, learning_curve, StratifiedKFold
from sklearn.metrics import roc_curve, auc, precision_recall_curve, confusion_matrix
from sklearn.inspection import permutation_importance
B = os.path.dirname(os.path.abspath(__file__)) + '/'; FG = B + 'fig/'; os.makedirs(FG, exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})
rng = np.random.default_rng(7)
save = lambda n: (plt.tight_layout(), plt.savefig(FG + n, dpi=200), plt.close())
for f in ('d_mlflow.png', 'd_biasvar.png', 'd_cv.png', 'd_nn.png'): shutil.copy(B + '../dipml/fig/' + f, FG + f)

# ---------- simulated 2-feature healthy/diseased data ----------
n = 500; yb = (rng.random(n) < 0.45).astype(int)
X = np.column_stack([rng.normal(0, 1, n) + 1.6 * yb + 0.6 * np.sin(rng.normal(0, 1, n)), rng.normal(0, 1, n) - 1.2 * yb + 0.5 * (yb * rng.normal(0, 1, n)) ** 2])
xx, yy = np.meshgrid(np.linspace(-3.5, 5, 250), np.linspace(-5, 3.5, 250)); grid = np.c_[xx.ravel(), yy.ravel()]
models = [('Logistic regression', LogisticRegression()), ('LDA', LDA()), ('k-NN (k = 15)', KNeighborsClassifier(15)),
          ('Decision tree (depth 4)', DecisionTreeClassifier(max_depth=4, random_state=0)), ('Random forest', RandomForestClassifier(300, max_depth=6, random_state=0)), ('RBF SVM', SVC(C=3, gamma=0.5))]
fig, ax = plt.subplots(2, 3, figsize=(12, 7.4))
for a, (nm, m) in zip(ax.flat, models):
    m.fit(X, yb); a.contourf(xx, yy, m.predict(grid).reshape(xx.shape), alpha=0.22, cmap='RdYlGn_r')
    a.scatter(X[:, 0], X[:, 1], c=yb, cmap='RdYlGn_r', s=8, edgecolor='none'); a.set_title(nm, fontsize=9.5); a.set_xticks([]); a.set_yticks([])
    a.set_xlabel('feature 1 (e.g. disease index)'); a.set_ylabel('feature 2 (e.g. canopy temperature)')
plt.suptitle('Decision boundaries of six classifiers on simulated healthy (green) and diseased (red) samples', fontsize=10)
save('m_boundaries.png')

# ---------- SVM margin and kernel ----------
fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))
Xa = np.r_[rng.normal([0, 0], 0.6, (40, 2)), rng.normal([2.6, 2.4], 0.6, (40, 2))]; ya = np.r_[np.zeros(40), np.ones(40)]
s = SVC(kernel='linear', C=1).fit(Xa, ya); w = s.coef_[0]; b = s.intercept_[0]; xs = np.linspace(-2, 4.5, 50)
ax[0].scatter(Xa[:, 0], Xa[:, 1], c=ya, cmap='RdYlGn_r', s=18)
for off, ls in ((0, '-'), (1, '--'), (-1, '--')): ax[0].plot(xs, (-w[0] * xs - b + off) / w[1], 'k' + ls, lw=1)
ax[0].scatter(*s.support_vectors_.T, s=90, facecolors='none', edgecolors='k'); ax[0].set_title('(a) Linear SVM: maximum margin; circled = support vectors', fontsize=9.5)
ax[0].set_xlim(-2, 4.5); ax[0].set_ylim(-2, 4.5)
r = np.r_[rng.uniform(0, 1, 80), rng.uniform(1.6, 2.4, 80)]; th = rng.uniform(0, 2 * np.pi, 160); Xr = np.c_[r * np.cos(th), r * np.sin(th)]; yr = np.r_[np.zeros(80), np.ones(80)]
sr = SVC(kernel='rbf', gamma=1, C=5).fit(Xr, yr); g2 = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-3, 3, 200))
ax[1].contourf(g2[0], g2[1], sr.decision_function(np.c_[g2[0].ravel(), g2[1].ravel()]).reshape(g2[0].shape), levels=[-10, 0, 10], colors=['#C8E6C9', '#FFCDD2'], alpha=0.6)
ax[1].scatter(Xr[:, 0], Xr[:, 1], c=yr, cmap='RdYlGn_r', s=12); ax[1].set_title('(b) RBF kernel separates classes that no straight line can', fontsize=9.5)
save('m_svm.png')

# ---------- decision tree + bagging schematic ----------
dt = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X, yb)
fig, ax = plt.subplots(figsize=(12, 4.8)); plot_tree(dt, feature_names=['disease index', 'canopy temperature'], class_names=['healthy', 'diseased'], filled=True, fontsize=8, ax=ax, proportion=True)
ax.set_title('Decision tree on simulated data: each split chooses the feature and threshold that most reduce Gini impurity', fontsize=10); save('m_tree.png')
fig, ax = plt.subplots(figsize=(12, 3.6)); ax.axis('off'); ax.set_xlim(0, 12); ax.set_ylim(0, 3.6)
def bx(x, y, w, h, t, fc, ec, fs=8.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02', fc=fc, ec=ec)); ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', fontsize=fs)
bx(0.2, 1.4, 1.8, 0.8, 'training data', '#ECEFF1', '#455A64')
for i in range(4):
    bx(2.8, 0.2 + i * 0.85, 1.7, 0.6, 'bootstrap sample %d' % (i + 1), '#E3F2FD', '#1565C0', 8); bx(5.2, 0.2 + i * 0.85, 1.7, 0.6, 'tree %d (random\nfeatures per split)' % (i + 1), '#E8F5E9', '#2E7D32', 7.5)
    ax.annotate('', xy=(2.78, 0.5 + i * 0.85), xytext=(2.0, 1.8), arrowprops=dict(arrowstyle='-|>', color='#777')); ax.annotate('', xy=(5.18, 0.5 + i * 0.85), xytext=(4.5, 0.5 + i * 0.85), arrowprops=dict(arrowstyle='-|>', color='#777'))
    ax.annotate('', xy=(7.8, 1.8), xytext=(6.9, 0.5 + i * 0.85), arrowprops=dict(arrowstyle='-|>', color='#777'))
bx(7.8, 1.4, 1.8, 0.8, 'majority vote /\naverage', '#FFF8E1', '#C98A00'); bx(10.2, 1.4, 1.6, 0.8, 'prediction', '#FCE4EC', '#AD1457')
ax.annotate('', xy=(10.18, 1.8), xytext=(9.6, 1.8), arrowprops=dict(arrowstyle='-|>', color='#777'))
ax.text(6, 3.45, 'Random forest = bagging of decorrelated trees; out-of-bag samples give an internal error estimate (Breiman, 2001)', ha='center', fontsize=9)
save('m_rf.png')

# ---------- simulated spectra: PCA ----------
pts_h = [(400,.040),(450,.045),(500,.060),(550,.120),(600,.070),(650,.045),(680,.040),(700,.090),(720,.250),(750,.420),(800,.460),(900,.470),(970,.440),(1050,.460),(1200,.400),(1300,.420),(1450,.200),(1650,.300),(1800,.270),(1940,.080),(2100,.180),(2200,.200),(2300,.150),(2400,.110)]
pts_d = [(400,.060),(450,.070),(500,.090),(550,.150),(600,.110),(650,.090),(680,.085),(700,.130),(720,.240),(750,.350),(800,.380),(900,.390),(970,.370),(1050,.390),(1200,.360),(1300,.380),(1450,.240),(1650,.330),(1800,.300),(1940,.120),(2100,.220),(2200,.240),(2300,.190),(2400,.140)]
wl = np.array([w for w in range(400, 2401, 10) if not (1350 <= w <= 1450 or 1800 <= w <= 1950)])
H, Dd = PchipInterpolator(*zip(*pts_h))(wl), PchipInterpolator(*zip(*pts_d))(wl)
m = 400; sev = rng.uniform(0, 1, m); bright = rng.normal(1, 0.08, m)
S = np.array([(H + s_ * (Dd - H)) * b_ for s_, b_ in zip(sev, bright)]) + rng.normal(0, 0.004, (m, len(wl)))
p = PCA(4).fit(S); sc = p.transform(S)
fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
ax[0].bar(range(1, 5), 100 * p.explained_variance_ratio_, color='#00695C'); ax[0].set_xlabel('Component'); ax[0].set_ylabel('Variance explained (%)'); ax[0].set_title('(a) Scree plot (simulated spectra)', fontsize=9)
for k, c in zip(range(2), ['#1565C0', '#C62828']):
    seg = np.split(np.arange(len(wl)), np.where(np.diff(wl) > 10)[0] + 1)
    for s_ in seg: ax[1].plot(wl[s_], p.components_[k][s_], color=c, lw=1.2, label='PC%d' % (k + 1) if s_[0] == 0 else None)
ax[1].legend(frameon=False); ax[1].set_xlabel('Wavelength (nm)'); ax[1].set_title('(b) Loadings: PC1 = brightness, PC2 = disease', fontsize=9)
sp = ax[2].scatter(sc[:, 0], sc[:, 1], c=sev, cmap='RdYlGn_r', s=8); plt.colorbar(sp, ax=ax[2], label='simulated severity'); ax[2].set_xlabel('PC1'); ax[2].set_ylabel('PC2'); ax[2].set_title('(c) Scores coloured by severity', fontsize=9)
save('m_pca.png')

# ---------- SFFS-like curve, learning curve (simulated) ----------
Xs = np.c_[X, rng.normal(0, 1, (n, 10))]                                  # 2 informative + 10 noise features
order, scores, rest = [], [], list(range(Xs.shape[1]))
for k in range(8):
    best = max(rest, key=lambda j: (cross_val_predict(RandomForestClassifier(100, random_state=0), Xs[:, order + [j]], yb, cv=5) == yb).mean())
    order.append(best); rest.remove(best); scores.append((cross_val_predict(RandomForestClassifier(100, random_state=0), Xs[:, order], yb, cv=5) == yb).mean())
ts, tr, te = learning_curve(RandomForestClassifier(200, random_state=0), Xs, yb, cv=5, train_sizes=np.linspace(0.1, 1, 7))
fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
ax[0].plot(range(1, 9), scores, '-o', color='#AD1457'); ax[0].set_xlabel('Number of selected features'); ax[0].set_ylabel('CV accuracy'); ax[0].set_title('(a) Forward selection: accuracy saturates after the informative features', fontsize=9)
ax[1].plot(ts, tr.mean(1), '-o', ms=3, label='training'); ax[1].plot(ts, te.mean(1), '-o', ms=3, label='validation'); ax[1].legend(frameon=False); ax[1].set_xlabel('Training samples'); ax[1].set_ylabel('Accuracy'); ax[1].set_title('(b) Learning curve: gap = variance; plateau = data limit', fontsize=9)
save('m_sffs_lc.png')

# ---------- evaluation: confusion, ROC, PR, permutation importance ----------
rf = RandomForestClassifier(300, random_state=0); prob = cross_val_predict(rf, Xs, yb, cv=5, method='predict_proba')[:, 1]; pred = (prob > 0.5).astype(int)
cm = confusion_matrix(yb, pred); fpr, tpr, _ = roc_curve(yb, prob); pr, rc, _ = precision_recall_curve(yb, prob)
pi = permutation_importance(rf.fit(Xs, yb), Xs, yb, n_repeats=5, random_state=0).importances_mean
fig, ax = plt.subplots(1, 4, figsize=(15, 3.6))
ax[0].imshow(cm, cmap='Greens'); [ax[0].text(j, i, cm[i, j], ha='center', va='center', fontsize=12) for i in range(2) for j in range(2)]
ax[0].set_xticks([0, 1], ['healthy', 'diseased']); ax[0].set_yticks([0, 1], ['healthy', 'diseased']); ax[0].set_xlabel('Predicted'); ax[0].set_ylabel('Observed'); ax[0].set_title('(a) Confusion matrix', fontsize=9)
ax[1].plot(fpr, tpr, color='#AD1457', lw=2, label='AUC %.2f' % auc(fpr, tpr)); ax[1].plot([0, 1], [0, 1], 'k--', lw=0.8); ax[1].legend(frameon=False); ax[1].set_xlabel('1 − specificity'); ax[1].set_ylabel('Sensitivity'); ax[1].set_title('(b) ROC curve', fontsize=9)
ax[2].plot(rc, pr, color='#1565C0', lw=2); ax[2].set_xlabel('Recall'); ax[2].set_ylabel('Precision'); ax[2].set_title('(c) Precision–recall curve', fontsize=9)
nm = ['f1 (index)', 'f2 (temperature)'] + ['noise %d' % i for i in range(1, 11)]; o = np.argsort(pi)
ax[3].barh(np.array(nm)[o], pi[o], color='#00695C'); ax[3].set_title('(d) Permutation importance', fontsize=9); ax[3].tick_params(labelsize=7)
plt.suptitle('Evaluation tools illustrated on simulated data (not thesis results)', fontsize=10); save('m_eval.png')

# ---------- regression: observed vs predicted + residuals ----------
sevp = rng.uniform(0, 80, 200); Xreg = np.c_[sevp / 80 + rng.normal(0, 0.12, 200), -sevp / 80 + rng.normal(0, 0.2, 200), rng.normal(0, 1, (200, 3))]
pr_ = cross_val_predict(RandomForestRegressor(300, random_state=0), Xreg, sevp, cv=5)
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
ax[0].scatter(sevp, pr_, s=10, color='#6A1B9A'); ax[0].plot([0, 80], [0, 80], 'k--', lw=0.8); ax[0].set_xlabel('Observed severity (simulated PDI)'); ax[0].set_ylabel('Predicted'); ax[0].set_title('(a) Observed vs predicted: points below the line at high values = underestimation', fontsize=8.5)
ax[1].scatter(pr_, pr_ - sevp, s=10, color='#6A1B9A'); ax[1].axhline(0, color='k', lw=0.8); ax[1].set_xlabel('Predicted'); ax[1].set_ylabel('Residual'); ax[1].set_title('(b) Residuals: patterns reveal bias (e.g. saturation, regression to the mean)', fontsize=8.5)
save('m_reg.png')

# ---------- nested CV and fusion levels diagrams ----------
fig, ax = plt.subplots(figsize=(12, 4.2)); ax.axis('off'); ax.set_xlim(0, 12); ax.set_ylim(0, 4.2)
cols = ['#2E7D32', '#1565C0', '#C98A00']
for f in range(3):
    y0 = 3.1 - f * 1.2; ax.text(0.1, y0 + 0.25, 'Outer fold %d' % (f + 1), fontsize=9, va='center')
    for r in range(3):
        c = '#C62828' if r == f else '#B0BEC5'; ax.add_patch(FancyBboxPatch((1.6 + r * 1.3, y0), 1.2, 0.5, boxstyle='square,pad=0', fc=c, ec='white'))
        ax.text(2.2 + r * 1.3, y0 + 0.25, ('TEST R%d' if r == f else 'train R%d') % (r + 1), ha='center', va='center', fontsize=8, color='white')
    ax.annotate('', xy=(6.0, y0 + 0.25), xytext=(5.5, y0 + 0.25), arrowprops=dict(arrowstyle='-|>', color='#777'))
    ax.add_patch(FancyBboxPatch((6.1, y0 - 0.05), 3.6, 0.6, boxstyle='round,pad=0.02', fc='#FFF8E1', ec='#C98A00'))
    ax.text(7.9, y0 + 0.25, 'inner CV on training replications only:\nfeature selection + tuning', ha='center', va='center', fontsize=8)
    ax.annotate('', xy=(10.2, y0 + 0.25), xytext=(9.75, y0 + 0.25), arrowprops=dict(arrowstyle='-|>', color='#777')); ax.text(10.3, y0 + 0.25, 'test once\non red fold', fontsize=8, va='center')
ax.set_title('Nested leave-one-replication-out validation: the test replication never influences selection or tuning', fontsize=10); save('m_nested.png')
fig, ax = plt.subplots(figsize=(12, 4.4)); ax.axis('off'); ax.set_xlim(0, 12); ax.set_ylim(0, 4.4)
lev = [('Early (feature-level)\nfusion', ['HS features', 'MS features', 'TIR features'], 'concatenate → one model'), ('Intermediate fusion\n(DNN-F2)', ['HS sub-network', 'MS sub-network', 'TIR sub-network'], 'join hidden layers → output'), ('Late (decision-level)\nfusion', ['HS model', 'MS model', 'TIR model'], 'vote / average / stacking')]
for i, (t, items, how) in enumerate(lev):
    x = 0.3 + i * 4.0; ax.text(x + 1.6, 4.15, t, ha='center', fontsize=9.5, fontweight='bold')
    for k, it in enumerate(items):
        ax.add_patch(FancyBboxPatch((x, 2.6 - k * 0.75), 1.6, 0.55, boxstyle='round,pad=0.02', fc='#E3F2FD', ec='#1565C0')); ax.text(x + 0.8, 2.87 - k * 0.75, it, ha='center', va='center', fontsize=8)
        ax.annotate('', xy=(x + 2.1, 1.85), xytext=(x + 1.62, 2.87 - k * 0.75), arrowprops=dict(arrowstyle='-|>', color='#777'))
    ax.add_patch(FancyBboxPatch((x + 2.1, 1.45), 1.75, 0.8, boxstyle='round,pad=0.02', fc='#FFF8E1', ec='#C98A00')); ax.text(x + 2.975, 1.85, how.replace(' → ', '\n→ '), ha='center', va='center', fontsize=7.5)
ax.text(6, 0.25, 'My study: early fusion with feature selection (VIF → ML-SFFS) and intermediate fusion (DNN-F2) are compared (Maimaitijiang et al., 2020)', ha='center', fontsize=8.5, style='italic')
save('m_fusion.png')
print('ok')
