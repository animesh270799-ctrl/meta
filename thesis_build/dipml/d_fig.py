"""Figures for the DIP + ML interview guide: a simulated 5-band field scene for image processing, real leaf ASD data for ML."""
import os, sys, shutil
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from scipy import ndimage as ndi
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_decomposition import PLSRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.model_selection import cross_val_predict, GroupKFold, learning_curve
from sklearn.metrics import roc_curve, auc, confusion_matrix
from sklearn.inspection import permutation_importance
from sklearn.preprocessing import StandardScaler
B = os.path.dirname(os.path.abspath(__file__)) + '/'; FG = B + 'fig/'; os.makedirs(FG, exist_ok=True)
sys.path.insert(0, B + '../obj1'); from o1_flow import chart, COL, FILL
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})
rng = np.random.default_rng(3)
save = lambda n: (plt.tight_layout(), plt.savefig(FG + n, dpi=200), plt.close())

# ===================== simulated 5-band field scene (B, G, R, RE, NIR) =====================
N = 200; scene = np.zeros((5, N, N)); cls = np.zeros((N, N), int)          # 0 soil, 1 healthy crop, 2 diseased crop
soil = np.array([0.10, 0.14, 0.18, 0.22, 0.26]); healthy = np.array([0.04, 0.10, 0.05, 0.25, 0.48]); dis = np.array([0.06, 0.13, 0.11, 0.24, 0.36])
for i in range(4):
    for j in range(4):
        y0, x0 = 12 + i * 47, 12 + j * 47; cls[y0:y0 + 38, x0:x0 + 38] = 1
yy, xx = np.mgrid[:N, :N]
for cy, cx, r in ((40, 60, 14), (120, 140, 18), (160, 40, 12), (70, 170, 10)):
    cls[((yy - cy) ** 2 + (xx - cx) ** 2 < r ** 2) & (cls == 1)] = 2
for b in range(5):
    base = np.choose(cls, [soil[b], healthy[b], dis[b]])
    scene[b] = ndi.gaussian_filter(base, 1.2) + rng.normal(0, 0.012, (N, N))
scene = np.clip(scene, 0, 1)
rgb = lambda s: np.clip(np.dstack([s[2], s[1], s[0]]) / np.percentile(s[:3], 99.5), 0, 1)
fcc = lambda s: np.clip(np.dstack([s[4], s[2], s[1]]) / np.percentile(s[[4, 2, 1]], 99.5), 0, 1)
ndvi = (scene[4] - scene[2]) / (scene[4] + scene[2])

# 1. composites + NDVI + histogram stretch
fig, ax = plt.subplots(1, 4, figsize=(13, 3.6))
raw = np.dstack([scene[2], scene[1], scene[0]]); ax[0].imshow(np.clip(raw, 0, 1)); ax[0].set_title('(a) True colour, no stretch')
ax[1].imshow(rgb(scene)); ax[1].set_title('(b) True colour, linear 2–98% stretch')
ax[2].imshow(fcc(scene)); ax[2].set_title('(c) False colour (NIR, R, G)')
im = ax[3].imshow(ndvi, cmap='RdYlGn', vmin=0, vmax=0.85); ax[3].set_title('(d) NDVI'); plt.colorbar(im, ax=ax[3], fraction=0.046)
for a in ax: a.axis('off')
save('d_composites.png')
# histogram equalisation demo
fig, ax = plt.subplots(1, 3, figsize=(12, 3.3))
band = scene[2]; ax[0].hist(band.ravel(), 100, color='#C62828'); ax[0].set_title('(a) Histogram of red band (narrow range)'); ax[0].set_xlabel('Reflectance')
lo, hi = np.percentile(band, (2, 98)); st = np.clip((band - lo) / (hi - lo), 0, 1); ax[1].hist(st.ravel(), 100, color='#1565C0'); ax[1].set_title('(b) After linear 2–98% stretch'); ax[1].set_xlabel('Display value (0–1)')
r_ = band.ravel().argsort().argsort() / band.size; ax[2].hist(r_, 100, color='#2E7D32'); ax[2].set_title('(c) After equalisation: flat histogram'); ax[2].set_xlabel('Display value (0–1)')
save('d_hist.png')

# 2. filters and edges
nir = scene[4]; noisy = nir + rng.normal(0, 0.05, nir.shape)
sob = np.hypot(ndi.sobel(nir, 0), ndi.sobel(nir, 1))
fig, ax = plt.subplots(1, 5, figsize=(14, 3.2))
for a, im_, t in zip(ax, [noisy, ndi.uniform_filter(noisy, 5), ndi.median_filter(noisy, 5), ndi.gaussian_filter(noisy, 1.5), sob],
                     ['(a) NIR with noise', '(b) Mean 5×5 (low-pass)', '(c) Median 5×5', '(d) Gaussian σ = 1.5', '(e) Sobel edges (high-pass)']):
    a.imshow(im_, cmap='gray'); a.set_title(t, fontsize=9); a.axis('off')
save('d_filters.png')

# 3. Otsu threshold + k-means + PCA
def otsu(x, nb=256):
    h, e = np.histogram(x.ravel(), nb); c = (e[:-1] + e[1:]) / 2; w = np.cumsum(h); m = np.cumsum(h * c); mt = m[-1]
    sb = (mt * w / w[-1] - m) ** 2 / (w * (w[-1] - w) + 1e-12) * w[-1]; return c[np.nanargmax(sb)]
t = otsu(ndvi); mask = ndvi > t
X = scene.reshape(5, -1).T
km = KMeans(3, n_init=5, random_state=0).fit(X); lab = km.labels_.reshape(N, N)
pc = PCA(3).fit(X); pcs = pc.transform(X).reshape(N, N, 3)
fig, ax = plt.subplots(1, 4, figsize=(13, 3.5))
ax[0].imshow(mask, cmap='Greens'); ax[0].set_title('(a) Otsu threshold on NDVI (t = %.2f)' % t, fontsize=9)
ax[1].imshow(lab, cmap='Set2'); ax[1].set_title('(b) k-means, 3 clusters (unsupervised)', fontsize=9)
for k in range(2): ax[2 + k].imshow(pcs[:, :, k], cmap='gray'); ax[2 + k].set_title('(%s) PC%d (%.1f%% variance)' % ('cd'[k], k + 1, 100 * pc.explained_variance_ratio_[k]), fontsize=9)
for a in ax: a.axis('off')
save('d_segment.png')

# 4. GLCM texture
def glcm_feat(img, levels=16, win=9):
    q = np.clip((img - img.min()) / (np.ptp(img) + 1e-9) * (levels - 1), 0, levels - 1).astype(int)
    out = np.zeros((2,) + img.shape); h = win // 2
    for i in range(h, img.shape[0] - h, 3):
        for j in range(h, img.shape[1] - h, 3):
            w = q[i - h:i + h + 1, j - h:j + h + 1]; P = np.zeros((levels, levels))
            np.add.at(P, (w[:, :-1].ravel(), w[:, 1:].ravel()), 1); P = P + P.T; P /= P.sum()
            I, J = np.indices(P.shape); out[0, i - 1:i + 2, j - 1:j + 2] = (P * (I - J) ** 2).sum(); out[1, i - 1:i + 2, j - 1:j + 2] = (P / (1 + (I - J) ** 2)).sum()
    return out
tex_img = scene[2] + np.where(cls == 2, rng.normal(0, 0.05, cls.shape), 0)          # diseased patches have speckled pustule texture
g = glcm_feat(tex_img)
fig, ax = plt.subplots(1, 3, figsize=(11, 3.6))
ax[0].imshow(tex_img, cmap='gray'); ax[0].set_title('(a) Red band (pustule texture in patches)', fontsize=9)
ax[1].imshow(g[0], cmap='magma'); ax[1].set_title('(b) GLCM contrast (9×9 window)', fontsize=9)
ax[2].imshow(g[1], cmap='viridis'); ax[2].set_title('(c) GLCM homogeneity', fontsize=9)
for a in ax: a.axis('off')
save('d_glcm.png')

# 5. resampling
small = scene[4][60:76, 60:76]; up = lambda o: ndi.zoom(small, 8, order=o)
fig, ax = plt.subplots(1, 4, figsize=(12, 3.2))
ax[0].imshow(small, cmap='gray', interpolation='nearest'); ax[0].set_title('(a) Original 16×16 pixels', fontsize=9)
for a, o, tt in zip(ax[1:], (0, 1, 3), ('(b) Nearest neighbour', '(c) Bilinear', '(d) Cubic convolution')): a.imshow(up(o), cmap='gray'); a.set_title(tt, fontsize=9)
for a in ax: a.axis('off')
save('d_resample.png')

# 6. pansharpening (Brovey) demo
pan = scene[[1, 2, 4]].mean(0); ms_low = np.stack([ndi.zoom(ndi.zoom(scene[b], 0.25, order=1), 4, order=1) for b in range(5)])
bro = ms_low[[2, 1, 0]] / (ms_low[[2, 1, 0]].sum(0) + 1e-9) * pan * 3
fig, ax = plt.subplots(1, 3, figsize=(11, 3.6))
ax[0].imshow(rgb(ms_low)); ax[0].set_title('(a) Low-resolution multispectral (4× coarser)', fontsize=9)
ax[1].imshow(pan, cmap='gray'); ax[1].set_title('(b) High-resolution panchromatic', fontsize=9)
ax[2].imshow(np.clip(np.dstack(bro) / np.percentile(bro, 99.5), 0, 1)); ax[2].set_title('(c) Brovey pansharpened', fontsize=9)
for a in ax: a.axis('off')
save('d_pansharp.png')

# ===================== flow charts =====================
COL.update({'D': '#00695C', 'M': '#AD1457', 'U': '#1565C0'}); FILL.update({'D': '#E0F2F1', 'M': '#FCE4EC', 'U': '#E3F2FD'})
chart('D', 'Image-processing chain from raw data to features', [
 ('1  Radiometric correction', ['DN → radiance (gain, offset); dark current; vignetting', 'Radiance → reflectance: panels (empirical line) or atmospheric model'], 'Smith 1999', ['Surface reflectance']),
 ('2  Geometric correction', ['GCPs, polynomial or orthorectification with DEM; resampling', 'Co-registration of all sensors (RMSE < 1 pixel)'], 'Toutin 2004', ['Georeferenced images']),
 ('3  Enhancement and noise', ['Stretching, filtering, bad-band removal, Savitzky–Golay smoothing'], 'Savitzky 1964', ['Clean images / spectra']),
 ('4  Masking and segmentation', ['NDVI + SAM crop mask; soil, shadow, flower removal; plot polygons'], 'Kruse 1993', ['Crop pixels per plot']),
 ('5  Feature extraction', ['Bands, derivatives, indices, PCA/MNF, texture (GLCM), temperature'], 'Haralick 1973', ['Feature table']),
 ('6  Analysis', ['Statistics, feature selection, classification and regression, maps'], 'Hastie 2009', ['Maps and accuracy']),
], 'd_chain.png', foot='Errors at an early step propagate: calibration and registration decide what the models can learn')
chart('U', 'UAV photogrammetry (structure from motion) workflow', [
 ('1  Flight planning', ['Altitude → ground sampling distance; 75–80% front, 70% side overlap; nadir view', 'Calibration panel before and after flight; GCPs measured by GNSS'], '', ['Image set']),
 ('2  Feature matching', ['Key points (SIFT-type) detected and matched between overlapping images'], 'Lowe 2004', ['Tie points']),
 ('3  Bundle adjustment', ['Camera positions, orientations and lens model solved together; GCPs fix scale and position'], 'Westoby 2012', ['Sparse point cloud']),
 ('4  Dense matching', ['Dense point cloud → digital surface model (DSM); DSM − DTM = canopy height'], 'Westoby 2012', ['DSM, canopy height']),
 ('5  Orthomosaic', ['Images projected on DSM; mosaicking and seamline blending; reflectance calibration'], '', ['Orthomosaic per sensor']),
], 'd_sfm.png', foot='Thermal and hyperspectral images are co-registered to the RGB/MS orthomosaic with GCPs')
chart('M', 'Machine-learning workflow without information leakage', [
 ('1  Data and labels', ['Plot-level features + ground truth (grades, PDI); groups = plots / replications'], '', ['Labelled table']),
 ('2  Outer split', ['Leave-one-replication-out (or spatial blocks): test data set aside'], 'Roberts 2017', ['Training / test folds']),
 ('3  Inside training only', ['Scaling, feature selection (Boruta, VIF, SFFS), hyperparameter tuning with inner CV'], 'Varma 2006', ['Final model per fold']),
 ('4  Test', ['Predict held-out data once; metrics: OA, kappa, F1, R², RMSE'], 'Sokolova 2009', ['Unbiased accuracy']),
 ('5  Interpret and deploy', ['Importance, SHAP / permutation; maps; independent validation'], 'Lundberg 2017', ['Explained model, maps']),
], 'd_mlflow.png', foot='Anything that sees the test data before testing (scaling, selection, tuning) inflates accuracy')
for f in ('d_chain.png', 'd_sfm.png', 'd_mlflow.png'): shutil.move(B + '../obj1/fig/' + f, FG + f)

# ===================== ML figures (real leaf data) =====================
LD = B + '../leaf/data/'
Z = np.load(LD + 'prep.npz'); M = pd.read_csv(LD + 'meta_leaf2.csv'); F = pd.read_csv(LD + 'feat_leaf_wri.csv'); P = pd.read_csv(LD + 'plot_table.csv')
y6 = M.grade.values; yb = (y6 > 0).astype(int); grp = M['plot'].values; fold = M.fold.values; wl = Z['b5']

# 7. bias-variance (polynomial fit)
x = np.sort(rng.uniform(0, 1, 30)); yt = np.sin(2 * np.pi * x); yn = yt + rng.normal(0, 0.25, x.size); xs = np.linspace(0, 1, 200)
fig, ax = plt.subplots(1, 4, figsize=(13, 3.3))
for a, d, t in zip(ax[:3], (1, 4, 15), ('(a) Underfit (degree 1): high bias', '(b) Good fit (degree 4)', '(c) Overfit (degree 15): high variance')):
    c = np.polyfit(x, yn, d); a.scatter(x, yn, s=12, color='k'); a.plot(xs, np.clip(np.polyval(c, xs), -2, 2), color='#AD1457'); a.plot(xs, np.sin(2 * np.pi * xs), '--', color='grey'); a.set_title(t, fontsize=9); a.set_ylim(-2, 2)
xtest = rng.uniform(0, 1, 200); ytest = np.sin(2 * np.pi * xtest) + rng.normal(0, 0.25, 200); tr, te = [], []
for d in range(1, 16):
    c = np.polyfit(x, yn, d); tr.append(np.sqrt(np.mean((np.polyval(c, x) - yn) ** 2))); te.append(np.sqrt(np.mean((np.polyval(c, xtest) - ytest) ** 2)))
ax[3].plot(range(1, 16), tr, '-o', ms=3, label='training error'); ax[3].plot(range(1, 16), np.clip(te, 0, 2), '-o', ms=3, label='test error'); ax[3].set_xlabel('Model complexity (degree)'); ax[3].set_ylabel('RMSE'); ax[3].legend(frameon=False); ax[3].set_title('(d) Training vs test error', fontsize=9)
save('d_biasvar.png')

# 8. cross-validation schemes diagram
fig, ax = plt.subplots(figsize=(12, 4.6)); ax.set_xlim(0, 12); ax.set_ylim(0, 4.6); ax.axis('off')
schemes = [('Random k-fold\n(samples)', [rng.permutation(np.repeat(range(3), 8))]), ('Grouped k-fold\n(plots kept together)', [np.repeat([0, 1, 2], 8)]), ('Leave-one-replication-\nout (my thesis)', [np.repeat([0, 1, 2], 8)])]
cl = ['#1565C0', '#C98A00', '#2E7D32']
for r, (name, arrs) in enumerate(schemes):
    yy0 = 3.6 - r * 1.35; ax.text(0.1, yy0 + 0.2, name, fontsize=9, va='center')
    a = arrs[0]
    for k in range(24):
        c = cl[a[k]]; ax.add_patch(FancyBboxPatch((2.4 + k * 0.38, yy0), 0.32, 0.4, boxstyle='square,pad=0', fc=c, ec='white'))
    if r == 0: ax.text(2.4, yy0 + 0.62, 'leakage risk: leaves of the same plot fall in training and test', fontsize=8, color='#C62828')
ax.text(6.9, 0.25, 'colours = test fold in each of three rounds; in grouped and LORO schemes all leaves/pixels of a plot (or replication) stay in one fold', ha='center', fontsize=8.5, style='italic')
save('d_cv.png')

# 9. SVM, k-NN, tree, LDA boundaries on two real features
Xf = StandardScaler().fit_transform(F[['WRI_VNIR', 'Dr']].values); sub = rng.choice(len(yb), 700, replace=False)
xx_, yy_ = np.meshgrid(np.linspace(-3, 3, 250), np.linspace(-3, 3, 250)); grid = np.c_[xx_.ravel(), yy_.ravel()]
models = [('Linear SVM (C = 1)', SVC(kernel='linear', C=1, class_weight='balanced')), ('RBF SVM (C = 10, γ = 1)', SVC(C=10, gamma=1, class_weight='balanced')), ('k-NN (k = 15)', KNeighborsClassifier(15)), ('Decision tree (depth 4)', DecisionTreeClassifier(max_depth=4, random_state=0, class_weight='balanced')), ('Random forest (300 trees)', RandomForestClassifier(300, max_depth=6, random_state=0, class_weight='balanced')), ('LDA (equal priors)', LDA(priors=[0.5, 0.5]))]
fig, ax = plt.subplots(2, 3, figsize=(12, 7.6))
for a, (nm, m) in zip(ax.flat, models):
    m.fit(Xf[sub], yb[sub]); zz = m.predict(grid).reshape(xx_.shape)
    a.contourf(xx_, yy_, zz, alpha=0.25, cmap='RdYlGn_r'); a.scatter(Xf[sub, 0], Xf[sub, 1], c=yb[sub], cmap='RdYlGn_r', s=6, edgecolor='none')
    if 'SVM' in nm: a.scatter(*m.support_vectors_[:60].T, s=14, facecolors='none', edgecolors='k', lw=0.5)
    pcv = cross_val_predict(m, Xf, yb, groups=grp, cv=GroupKFold(3)); bacc = 0.5 * (((pcv == 1) & (yb == 1)).sum() / (yb == 1).sum() + ((pcv == 0) & (yb == 0)).sum() / (yb == 0).sum())
    a.set_title('%s — balanced acc. %.2f' % (nm, bacc), fontsize=9); a.set_xlim(-3, 3); a.set_ylim(-3, 3)
    a.set_xlabel('WRI (standardised)'); a.set_ylabel('Dr (standardised)')
plt.suptitle('Decision boundaries of six classifiers: healthy (green) vs diseased (red) leaves, real ASD data, two features', fontsize=10)
save('d_boundaries.png')

# 10. decision tree plot
dt = DecisionTreeClassifier(max_depth=3, random_state=0, class_weight='balanced').fit(F[['WRI_VNIR', 'Dr', 'PSRI', 'DWSI-5']], yb)
fig, ax = plt.subplots(figsize=(13, 5.2)); plot_tree(dt, feature_names=['WRI', 'Dr', 'PSRI', 'DWSI-5'], class_names=['healthy', 'diseased'], filled=True, fontsize=8, ax=ax, impurity=True, proportion=True)
ax.set_title('Decision tree (depth 3) on real leaf features: each split minimises Gini impurity', fontsize=10); save('d_tree.png')

# 11. PCA of leaf spectra
Rs = Z['R']; p = PCA(5).fit(Rs); sc = p.transform(Rs)
fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
ax[0].bar(range(1, 6), 100 * p.explained_variance_ratio_, color='#00695C'); ax[0].set_xlabel('Principal component'); ax[0].set_ylabel('Variance explained (%)'); ax[0].set_title('(a) Scree plot (349 bands)', fontsize=9)
for k, c in zip(range(3), ['#1565C0', '#C62828', '#2E7D32']): ax[1].plot(wl, p.components_[k], color=c, lw=1, label='PC%d' % (k + 1))
ax[1].legend(frameon=False); ax[1].set_xlabel('Wavelength (nm)'); ax[1].set_title('(b) Loadings', fontsize=9)
GC = ['#2E7D32', '#9CCC65', '#FDD835', '#FB8C00', '#E53935', '#7B1FA2']
for g, c in zip([0, 1, 3, 5, 7, 9], GC): ax[2].scatter(sc[y6 == g, 0], sc[y6 == g, 1], s=3, color=c, label=str(g), alpha=0.5)
ax[2].legend(title='grade', fontsize=7, markerscale=3, frameon=False); ax[2].set_xlabel('PC1'); ax[2].set_ylabel('PC2'); ax[2].set_title('(c) Scores: PCA is unsupervised, grades overlap', fontsize=9)
save('d_pca.png')

# 12. PLSR on plot spectra (real)
Xp = Z['Rp']; yp = P.PDI.values; rm = []
for nc in range(1, 13):
    pr = np.zeros_like(yp)
    for f in range(3):
        tr_, te_ = P.fold.values != f, P.fold.values == f; pr[te_] = PLSRegression(nc).fit(Xp[tr_], yp[tr_]).predict(Xp[te_]).ravel()
    rm.append(np.sqrt(np.mean((pr - yp) ** 2)))
best = int(np.argmin(rm)) + 1; pr = np.zeros_like(yp)
for f in range(3):
    tr_, te_ = P.fold.values != f, P.fold.values == f; pr[te_] = PLSRegression(best).fit(Xp[tr_], yp[tr_]).predict(Xp[te_]).ravel()
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
ax[0].plot(range(1, 13), rm, '-o', ms=4, color='#6A1B9A'); ax[0].axvline(best, ls='--', color='grey'); ax[0].set_xlabel('Number of latent components'); ax[0].set_ylabel('LORO RMSE (PDI %)'); ax[0].set_title('(a) Choosing PLSR components', fontsize=9)
ax[1].scatter(yp, np.clip(pr, 0, 100), s=12, color='#6A1B9A'); ax[1].plot([0, 80], [0, 80], 'k--', lw=0.8); r2 = 1 - np.sum((pr - yp) ** 2) / np.sum((yp - yp.mean()) ** 2)
ax[1].set_xlabel('Observed PDI (%)'); ax[1].set_ylabel('Predicted PDI (%)'); ax[1].set_title('(b) PLSR, %d components, full spectrum: R² = %.2f' % (best, r2), fontsize=9)
save('d_plsr.png')

# 13. ROC + confusion matrix + permutation importance (RF healthy vs diseased)
feats = ['WRI_VNIR', 'Dr', 'REP', 'PSRI', 'ARI', 'HI', 'PRI', 'NDVI780', 'DWSI-5', 'MSI', 'NDWI', 'WI']
Xr = F[feats].values; prob = np.zeros(len(yb)); predc = np.zeros(len(yb), int); imps = []
for f in range(3):
    tr_, te_ = fold != f, fold == f; rf = RandomForestClassifier(300, random_state=0, n_jobs=-1, class_weight='balanced').fit(Xr[tr_], yb[tr_])
    prob[te_] = rf.predict_proba(Xr[te_])[:, 1]; predc[te_] = (prob[te_] > 0.5).astype(int)
    imps.append(permutation_importance(rf, Xr[te_], yb[te_], n_repeats=5, random_state=0, scoring='balanced_accuracy').importances_mean)
fpr, tpr, _ = roc_curve(yb, prob); cm = confusion_matrix(yb, predc)
fig, ax = plt.subplots(1, 3, figsize=(13, 3.9))
ax[0].plot(fpr, tpr, color='#AD1457', lw=2, label='RF, AUC = %.2f' % auc(fpr, tpr)); ax[0].plot([0, 1], [0, 1], 'k--', lw=0.8); ax[0].set_xlabel('False positive rate (1 − specificity)'); ax[0].set_ylabel('True positive rate (sensitivity)'); ax[0].legend(frameon=False); ax[0].set_title('(a) ROC curve (held-out replications)', fontsize=9)
ax[1].imshow(cm, cmap='Greens'); [ax[1].text(j, i, cm[i, j], ha='center', va='center', fontsize=12) for i in range(2) for j in range(2)]
ax[1].set_xticks([0, 1], ['healthy', 'diseased']); ax[1].set_yticks([0, 1], ['healthy', 'diseased']); ax[1].set_xlabel('Predicted'); ax[1].set_ylabel('Observed'); ax[1].set_title('(b) Confusion matrix', fontsize=9)
im_ = np.mean(imps, 0); o = np.argsort(im_); ax[2].barh(np.array(feats)[o], im_[o], color='#00695C'); ax[2].set_xlabel('Drop in balanced accuracy when shuffled'); ax[2].set_title('(c) Permutation importance', fontsize=9)
save('d_eval.png')

# 14. learning curve
ts, trs, tes = learning_curve(RandomForestClassifier(200, random_state=0, n_jobs=-1), Xr, yb, groups=grp, cv=GroupKFold(3), train_sizes=np.linspace(0.1, 1, 7), scoring='balanced_accuracy')
fig, ax = plt.subplots(figsize=(6, 3.6)); ax.plot(ts, trs.mean(1), '-o', ms=3, label='training'); ax.plot(ts, tes.mean(1), '-o', ms=3, label='validation (grouped CV)')
ax.set_xlabel('Number of training leaves'); ax.set_ylabel('Balanced accuracy'); ax.legend(frameon=False); ax.set_title('Learning curve: gap = variance; plateau = more data will not help much', fontsize=9)
save('d_learning.png')

# 15. neural network and CNN schematic
fig, ax = plt.subplots(1, 2, figsize=(13, 4.6))
a = ax[0]; a.axis('off'); a.set_xlim(0, 4); a.set_ylim(0, 6)
layers = [5, 8, 4, 6]; names = ['input\n(features)', 'hidden 1\n(ReLU)', 'hidden 2\n(ReLU)', 'output\n(softmax: 6 grades)']
pos = []
for li, n in enumerate(layers):
    ys = np.linspace(0.8, 5.2, n); pos.append([(li + 0.5, y_) for y_ in ys]); a.text(li + 0.5, 0.15, names[li], ha='center', fontsize=8)
for l in range(3):
    for p1 in pos[l]:
        for p2 in pos[l + 1]: a.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#BBBBBB', lw=0.4)
for l in range(4):
    for p1 in pos[l]: a.add_patch(plt.Circle(p1, 0.13, color=['#1565C0', '#00695C', '#00695C', '#AD1457'][l], zorder=3))
a.set_title('(a) Multilayer perceptron: weighted sums + non-linear activation;\ntrained by back-propagation of the loss gradient', fontsize=9)
a = ax[1]; a.axis('off'); a.set_xlim(0, 13); a.set_ylim(0, 6)
blocks = [(0.2, 1.5, 1.6, 3.0, '#90CAF9', 'image patch\n(bands)'), (2.4, 1.8, 1.4, 2.4, '#A5D6A7', 'conv 3×3\n+ ReLU'), (4.3, 2.1, 1.1, 1.8, '#C5E1A5', 'pooling'), (5.9, 2.3, 1.0, 1.4, '#A5D6A7', 'conv\n+ ReLU'), (7.4, 2.5, 0.8, 1.0, '#C5E1A5', 'pool'), (8.8, 1.2, 0.5, 3.6, '#FFE082', 'flatten /\ndense'), (10.3, 2.4, 1.0, 1.2, '#F48FB1', 'softmax')]
for x0, y0, w, h, c, t in blocks:
    a.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle='round,pad=0.02', fc=c, ec='#555')); a.text(x0 + w / 2, y0 - 0.35, t, ha='center', va='top', fontsize=8)
for i in range(len(blocks) - 1):
    x0, y0, w, h = blocks[i][:4]; a.annotate('', xy=(blocks[i + 1][0], 3.0), xytext=(x0 + w, 3.0), arrowprops=dict(arrowstyle='-|>', color='#555'))
a.text(12.2, 3.0, 'class\nprobabilities', fontsize=8, va='center')
a.set_title('(b) Convolutional neural network: filters learn spatial/spectral patterns;\npooling reduces size; dense layers classify', fontsize=9)
save('d_nn.png')

# 16. k-means on spectra + SAM illustration
fig, ax = plt.subplots(1, 2, figsize=(11, 3.8))
km = KMeans(4, n_init=5, random_state=0).fit(Rs)
for k, c in zip(range(4), ['#1565C0', '#C62828', '#2E7D32', '#C98A00']):
    seg = np.split(np.arange(len(wl)), np.where(np.diff(wl) > 5)[0] + 1)
    for s_ in seg: ax[0].plot(wl[s_], km.cluster_centers_[k][s_], color=c, lw=1.5, label='cluster %d' % (k + 1) if s_[0] == 0 else None)
ax[0].legend(frameon=False, fontsize=8); ax[0].set_xlabel('Wavelength (nm)'); ax[0].set_ylabel('Reflectance'); ax[0].set_title('(a) k-means cluster centres of 2339 leaf spectra', fontsize=9)
ax[1].set_xlim(0, 1); ax[1].set_ylim(0, 1); ax[1].set_aspect('equal')
for v, c, t in (((0.9, 0.35), '#2E7D32', 'reference (crop)'), ((0.6, 0.55), '#C62828', 'pixel'), ((0.45, 0.17), '#555', 'same angle, darker')):
    ax[1].annotate('', xy=v, xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', color=c, lw=2)); ax[1].text(v[0] + 0.02, v[1], t, color=c, fontsize=8)
ax[1].set_xlabel('Band 1 reflectance'); ax[1].set_ylabel('Band 2 reflectance'); ax[1].set_title('(b) Spectral angle mapper: angle between vectors\nis insensitive to brightness (illumination)', fontsize=9)
save('d_kmeans_sam.png')
print('figures ok')
