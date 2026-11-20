"""Leaf-level white rust analysis of ASD contact-probe spectra following Ma et al. (2026, IJAM 56(11), 5380-5398).
Paper steps reproduced: severity levels (Tables II-IV) -> SG smoothing -> mean spectra (Fig. 6) -> NDSI/RSI R2 maps and
effective ranges (Fig. 7) -> band selection by three methods on the effective-range bands (Table VII, Fig. 8)
-> vegetation indices, correlation (Table VIII, Fig. 9) and Relief selection (Fig. 10a) -> classification with single and
fused inputs (Tables XI-XII) and a full-wavelength baseline (Table X) -> independent validation (Table XIII).
Texture features (GLCM) and the texture index (TTFI) are NOT used: contact-probe spectra are non-imaging.
Whole range 350-2500 nm kept (contact probe has its own light source; 1400/1900-nm water absorption is leaf signal).
Band selectors are SHAP-free: RFE with random forest (RFE-SHAP analogue), SAND (sigmoid feature weights with sparsity,
threshold 0.524, as described in the paper) and CARS-PLS (SHAP-CARS analogue).
"""
import pickle, sys, time, warnings
import numpy as np, pandas as pd
from scipy.signal import savgol_filter
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.cross_decomposition import PLSRegression
from sklearn.feature_selection import RFE
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedGroupKFold, GroupKFold, GridSearchCV
from sklearn.metrics import accuracy_score, cohen_kappa_score, f1_score, recall_score

warnings.filterwarnings("ignore")
t0 = time.time()
d = pickle.load(open(sys.argv[1], "rb"))
meta, R, wl = d["meta"].copy(), d["R"], d["wl"]
meta["level"] = meta["score"].map({0: 0, 1: 1, 3: 2, 5: 3, 7: 4, 9: 4})
LEVEL_NAMES = ["L0 healthy (0)", "L1 mild (1)", "L2 moderate (3)", "L3 severe (5)", "L4 very severe (7-9)"]
TRAIN_DATES, TEST_DATE = ["110226", "240226", "030326"], "130326"
R2_EFFECTIVE = 0.25   # paper used R2 > 0.5; max R2 here is lower, so |r| >= 0.5 (R2 >= 0.25) defines the effective ranges
OUT = {"meta": meta, "level_names": LEVEL_NAMES, "r2_threshold": R2_EFFECTIVE}

# ---------------------------------------------------------------- pre-processing
def splice_correct(R, wl, joins=(1000, 1800)):
    R = R.copy()
    i1 = np.searchsorted(wl, joins[0], side="right"); i2 = np.searchsorted(wl, joins[1], side="right")
    step1 = (R[:, i1] - (R[:, i1 + 2] - R[:, i1]) / 2) - R[:, i1 - 1]; R[:, :i1] += step1[:, None]
    step2 = (R[:, i2 - 1] + (R[:, i2 - 1] - R[:, i2 - 3]) / 2) - R[:, i2]; R[:, i2:] += step2[:, None]
    return R, step1, step2

Rc, st1, st2 = splice_correct(R, wl)
Rs = savgol_filter(Rc, 11, 2, axis=1)
centres = np.arange(355, 2500, 10)
B = np.column_stack([Rs[:, (wl >= c - 5) & (wl < c + 5)].mean(1) for c in centres]); bw = centres.copy()
nir = Rs[:, (wl >= 800) & (wl <= 900)].mean(1); red = Rs[:, (wl >= 660) & (wl <= 680)].mean(1); green = Rs[:, (wl >= 540) & (wl <= 560)].mean(1)
OUT.update(splice=dict(step1000=st1, step1800=st2), bins=bw, B=B,
           qc=pd.DataFrame(dict(out_of_range=((R < 0) | (R > 1)).any(1), low_nir=nir < 0.3, red_ge_green=red >= green)))

# ---------------------------------------------------------------- mean spectra (Fig. 6)
wl5 = np.arange(350, 2501, 5); i5 = np.searchsorted(wl, wl5)
OUT["mean_by_level"] = pd.DataFrame({LEVEL_NAMES[l]: Rs[meta.level == l][:, i5].mean(0) for l in range(5)}, index=wl5)
OUT["sd_by_level"] = pd.DataFrame({LEVEL_NAMES[l]: Rs[meta.level == l][:, i5].std(0) for l in range(5)}, index=wl5)
OUT["mean_by_date"] = pd.DataFrame({dt: Rs[meta.date == dt][:, i5].mean(0) for dt in TRAIN_DATES + [TEST_DATE]}, index=wl5)

# ---------------------------------------------------------------- vegetation indices (Table V + PSRI from Table VIII)
def b(nm): return Rs[:, np.argmin(np.abs(wl - nm))]
VI = pd.DataFrame({
    "PSSRb": b(800) / b(635), "GNDVI": (b(750) - b(540)) / (b(750) + b(540)), "PRI": (b(531) - b(570)) / (b(531) + b(570)),
    "SR": b(800) / b(650), "RNDVI": (b(750) - b(705)) / (b(750) + b(705)), "FRI3": b(740) / b(800), "WBI": b(900) / b(970),
    "WSCT": (b(970) + b(850)) / (b(970) + b(650)), "ARI": 1 / b(550) - 1 / b(700), "CIgreen": b(790) / b(550) - 1,
    "CIre": b(790) / b(720) - 1, "EVI2": 2.5 * (b(800) - b(670)) / (1 + b(800) + 2.4 * b(670)),
    "MCARI705": ((b(750) - b(705)) - 0.2 * (b(750) - b(550))) * (b(750) / b(705)), "PhRI": (b(550) - b(531)) / (b(550) + b(531)),
    "RVI": b(810) / b(650), "RVSI": (b(714) + b(752)) / 2 - b(733), "PSRI": (b(680) - b(500)) / b(750)})
OUT["VI"] = VI
OUT["VI_formulas"] = {"PSSRb": "R800/R635", "GNDVI": "(R750-R540)/(R750+R540)", "PRI": "(R531-R570)/(R531+R570)", "SR": "R800/R650",
                      "RNDVI": "(R750-R705)/(R750+R705)", "FRI3": "R740/R800", "WBI": "R900/R970", "WSCT": "(R970+R850)/(R970+R650)",
                      "ARI": "1/R550-1/R700", "CIgreen": "R790/R550-1", "CIre": "R790/R720-1", "EVI2": "2.5(R800-R670)/(1+R800+2.4R670)",
                      "MCARI705": "((R750-R705)-0.2(R750-R550))(R750/R705)", "PhRI": "(R550-R531)/(R550+R531)", "RVI": "R810/R650",
                      "RVSI": "(R714+R752)/2-R733", "PSRI": "(R680-R500)/R750"}

# ---------------------------------------------------------------- NDSI / RSI (Fig. 7) and effective ranges
grid = np.arange(355, 2500, 20); gi = np.searchsorted(bw, grid); gw = bw[gi]
def r2_maps(idx):
    X, y = B[idx][:, gi], meta.score.values[idx].astype(float)
    y = (y - y.mean()) / y.std(); n = X.shape[1]; MN = np.full((n, n), np.nan); MR = np.full((n, n), np.nan)
    for i in range(n):
        nd = (X[:, [i]] - X) / (X[:, [i]] + X); rs = X[:, [i]] / X
        for M, V in ((MN, nd), (MR, rs)):
            Vz = (V - V.mean(0)) / (V.std(0) + 1e-12); M[i] = ((Vz * y[:, None]).mean(0)) ** 2
        MN[i, i] = MR[i, i] = np.nan
    return MN, MR
def effective_bins(MN, MR):
    hit = np.zeros(len(gw), bool)
    for M in (MN, MR):
        m = np.nan_to_num(M) >= R2_EFFECTIVE; hit |= m.any(0) | m.any(1)
    eff = np.zeros(len(bw), bool)
    for g, h in zip(gw, hit):
        if h: eff |= np.abs(bw - g) <= 10
    return np.where(eff)[0]
tr_all = meta.date.isin(TRAIN_DATES).values
MN, MR = r2_maps(np.where(tr_all)[0])
OUT["NDSI_R2"] = pd.DataFrame(MN, index=gw, columns=gw); OUT["RSI_R2"] = pd.DataFrame(MR, index=gw, columns=gw)
print("maps done; effective bins (all training):", len(effective_bins(MN, MR)), flush=True)

# ---------------------------------------------------------------- band selectors
def sel_rfe(X, y, k=10):
    rf = RandomForestClassifier(n_estimators=300, max_features="sqrt", class_weight="balanced", random_state=42, n_jobs=-1)
    return np.where(RFE(rf, n_features_to_select=k, step=0.1).fit(X, y).support_)[0]

def sel_sand(X, y, lam=0.3, thr=0.524, epochs=400, lr=0.02, seed=42):
    """SAND as described by Ma et al.: learnable logits a -> sigmoid weights w in [0,1]; input x*w feeds a softmax layer;
    loss = cross-entropy + lam * mean(w); keep features with w > thr. Full-batch Adam, numpy."""
    rng = np.random.default_rng(seed)
    Xs = (X - X.mean(0)) / X.std(0); n, p = Xs.shape; K = 5; Y = np.eye(K)[y]
    cw = n / (K * np.bincount(y, minlength=K)); sw = cw[y][:, None]
    a = np.zeros(p); Wt = rng.normal(0, 0.01, (p, K)); bt = np.zeros(K)
    params = [a, Wt, bt]; m_ = [np.zeros_like(q) for q in params]; v_ = [np.zeros_like(q) for q in params]
    for t in range(1, epochs + 1):
        w = 1 / (1 + np.exp(-a)); Z = (Xs * w) @ Wt + bt; Z -= Z.max(1, keepdims=True)
        P = np.exp(Z); P /= P.sum(1, keepdims=True)
        G = sw * (P - Y) / sw.sum()
        gW = (Xs * w).T @ G + 1e-4 * Wt; gb = G.sum(0)
        gw_ = (Xs * (G @ Wt.T)).sum(0) + lam / p
        ga = gw_ * w * (1 - w)
        for q, g, mm, vv in zip(params, (ga, gW, gb), m_, v_):
            mm *= 0.9; mm += 0.1 * g; vv *= 0.999; vv += 0.001 * g * g
            q -= lr * (mm / (1 - 0.9 ** t)) / (np.sqrt(vv / (1 - 0.999 ** t)) + 1e-8)
    w = 1 / (1 + np.exp(-a))
    return np.where(w > thr)[0], w

def sel_cars(X, y, groups, n_runs=50, seed=42, max_lv=10):
    rng = np.random.default_rng(seed); n, p = X.shape
    a_ = (p / 2) ** (1 / (n_runs - 1)); kk = np.log(p / 2) / (n_runs - 1)
    keep_idx = np.arange(p); subsets, rmse = [], []
    for i in range(1, n_runs + 1):
        cal = rng.choice(n, int(0.8 * n), replace=False); lv = min(max_lv, len(keep_idx))
        pls = PLSRegression(lv, scale=True).fit(X[np.ix_(cal, keep_idx)], y[cal])
        w = np.abs(pls.coef_).ravel(); w = w / w.sum()
        nkeep = max(2, int(round(a_ * np.exp(-kk * i) * p)))
        o = np.argsort(-w)[:nkeep]; ww = w[o] / w[o].sum()
        keep_idx = np.unique(rng.choice(keep_idx[o], nkeep, replace=True, p=ww))
        lv = min(max_lv, len(keep_idx)); err = []
        for trn, tst in GroupKFold(5).split(X, y, groups):
            m2 = PLSRegression(lv, scale=True).fit(X[np.ix_(trn, keep_idx)], y[trn])
            err.append(np.mean((m2.predict(X[np.ix_(tst, keep_idx)]).ravel() - y[tst]) ** 2))
        subsets.append(keep_idx.copy()); rmse.append(np.sqrt(np.mean(err)))
    best = int(np.argmin(rmse))
    return subsets[best], dict(n_vars=[len(s) for s in subsets], rmsecv=rmse, best_run=best + 1)

def relief(X, y, k=10):
    Xn = (X - X.min(0)) / (X.max(0) - X.min(0) + 1e-12); n, p = Xn.shape
    cls, cnt = np.unique(y, return_counts=True); prior = dict(zip(cls, cnt / n))
    Dm = np.abs(Xn[:, None, :] - Xn[None, :, :]).sum(2); W = np.zeros(p)
    for i in range(n):
        di = Dm[i].copy(); di[i] = np.inf
        same = np.where(y == y[i])[0]; W -= np.abs(Xn[same[np.argsort(di[same])][:k]] - Xn[i]).mean(0) / n
        for c in cls:
            if c == y[i]: continue
            oth = np.where(y == c)[0]
            W += prior[c] / (1 - prior[y[i]]) * np.abs(Xn[oth[np.argsort(di[oth])][:k]] - Xn[i]).mean(0) / n
    return W

def build_features(tr, te):
    y, g = meta.level.values, meta["plot"].values
    mn, mr = r2_maps(tr); eff = effective_bins(mn, mr)
    Xe = B[tr][:, eff]
    f = {"effective": eff}
    f["rfe"] = eff[sel_rfe(Xe, y[tr])]
    sidx, sw = sel_sand(Xe, y[tr]); f["sand"] = eff[sidx]; f["sand_w"] = pd.Series(sw, index=bw[eff])
    cidx, cinfo = sel_cars(Xe, y[tr].astype(float), g[tr]); f["cars"] = eff[cidx]; f["cars_info"] = cinfo
    W = relief(VI.values[tr], y[tr]); f["relief_w"] = W; f["vi_top"] = list(np.argsort(-W)[:5])
    def mats(idx):
        return {"RFE-RF": B[idx][:, f["rfe"]], "SAND": B[idx][:, f["sand"]], "CARS-PLS": B[idx][:, f["cars"]],
                "VIs (Relief top 5)": VI.values[idx][:, f["vi_top"]], "Full wavelength (350-2500 nm)": B[idx],
                "OWs+VIs": np.hstack([B[idx][:, f["cars"]], VI.values[idx][:, f["vi_top"]]])}
    return f, mats(tr), mats(te)

def pls_da(Xtr, ytr, Xte, gtr):
    Y = np.eye(5)[ytr]; best, be = 2, np.inf
    for lv in (2, 4, 6, 8, 10, 12, 15):
        lv_ = min(lv, Xtr.shape[1]); err = []
        for a_, b_ in GroupKFold(3).split(Xtr, ytr, gtr):
            m_ = make_pipeline(StandardScaler(), PLSRegression(lv_, scale=False)).fit(Xtr[a_], Y[a_])
            err.append(np.mean(m_.predict(Xtr[b_]).argmax(1) != ytr[b_]))
        if np.mean(err) < be: be, best = np.mean(err), lv_
    return make_pipeline(StandardScaler(), PLSRegression(best, scale=False)).fit(Xtr, Y).predict(Xte).argmax(1)

def fit_predict(model, Xtr, ytr, Xte, gtr):
    if model == "PLS-DA": return pls_da(Xtr, ytr, Xte, gtr)
    if model == "SVM":
        m_ = GridSearchCV(make_pipeline(StandardScaler(), SVC(kernel="rbf", class_weight="balanced")),
                          {"svc__C": [1, 10, 100], "svc__gamma": ["scale", 0.01]}, cv=GroupKFold(3), scoring="f1_macro")
        return m_.fit(Xtr, ytr, groups=gtr).predict(Xte)
    if model == "RF":
        m_ = RandomForestClassifier(n_estimators=500, max_features="sqrt", class_weight="balanced", random_state=42, n_jobs=-1)
    else:
        m_ = make_pipeline(StandardScaler(), MLPClassifier((64, 32), alpha=1e-3, max_iter=600, early_stopping=True,
                                                            validation_fraction=0.1, n_iter_no_change=30, random_state=42))
    return m_.fit(Xtr, ytr).predict(Xte)

def metrics(y, p):
    f1 = f1_score(y, p, average=None, labels=range(5), zero_division=0)
    return dict(OA=accuracy_score(y, p) * 100, Kappa=cohen_kappa_score(y, p) * 100, QWK=cohen_kappa_score(y, p, weights="quadratic") * 100,
                Recall=recall_score(y, p, average="macro", labels=range(5), zero_division=0) * 100,
                F1=f1_score(y, p, average="macro", labels=range(5), zero_division=0) * 100, **{f"F1_L{l}": f1[l] * 100 for l in range(5)})

MODELS = ["RF", "SVM", "PLS-DA", "MLP"]
y_all, g_all = meta.level.values, meta["plot"].values
tr_idx = np.where(tr_all)[0]; te_idx = np.where(meta.date.values == TEST_DATE)[0]
folds = list(StratifiedGroupKFold(5, shuffle=True, random_state=42).split(tr_idx, meta.treatment.values[tr_idx], g_all[tr_idx]))
preds, fold_feats = {}, []
for k, (a_, b_) in enumerate(folds):
    tr, te = tr_idx[a_], tr_idx[b_]
    f, Mtr, Mte = build_features(tr, te); fold_feats.append(f)
    for s in Mtr:
        for m in MODELS: preds.setdefault((s, m), np.full(len(y_all), -1))[te] = fit_predict(m, Mtr[s], y_all[tr], Mte[s], g_all[tr])
    print("fold", k, "done", round(time.time() - t0), "s | eff", len(f["effective"]), "rfe", len(f["rfe"]), "sand", len(f["sand"]), "cars", len(f["cars"]), flush=True)
OUT["internal"] = pd.DataFrame([dict(input=s, model=m, **metrics(y_all[tr_idx], p[tr_idx])) for (s, m), p in preds.items()])
OUT["internal_folds"] = pd.DataFrame([dict(input=s, model=m, fold=k + 1, OA=accuracy_score(y_all[tr_idx[b_]], p[tr_idx[b_]]) * 100)
                                      for (s, m), p in preds.items() for k, (a_, b_) in enumerate(folds)])
OUT.update(internal_preds=preds, folds=folds, fold_feats=fold_feats, tr_idx=tr_idx, te_idx=te_idx)

f, Mtr, Mte = build_features(tr_idx, te_idx); OUT["final_feats"] = f
ext = {}; rows = []
for s in Mtr:
    for m in MODELS:
        p = fit_predict(m, Mtr[s], y_all[tr_idx], Mte[s], g_all[tr_idx]); ext[(s, m)] = p
        rows.append(dict(input=s, model=m, **metrics(y_all[te_idx], p)))
OUT["external"] = pd.DataFrame(rows); OUT["external_preds"] = ext
OUT["VI_r"] = pd.Series({c: np.corrcoef(VI[c].values[tr_all], meta.score.values[tr_all])[0, 1] for c in VI.columns})
OUT["VI_corrmat"] = VI[tr_all].corr()
with open(sys.argv[2], "wb") as fh: pickle.dump(OUT, fh)
print("final: eff", len(f["effective"]), "rfe", len(f["rfe"]), "sand", len(f["sand"]), "cars", len(f["cars"]))
print("ALL DONE", round(time.time() - t0), "s")
