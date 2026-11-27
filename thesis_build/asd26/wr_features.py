"""White rust leaf models (ASD contact probe, 2025-26): pre-processing and feature computation for NEW spectra,
identical to the training pipeline (a1_prep.py), plus the two PLS wrapper classes needed to load the saved models.

Input : raw reflectance, 350-2500 nm at 1 nm (ASD export, splice-corrected), one row per leaf.
Steps : Savitzky-Golay (window 11, order 2) on 350-2500 nm -> keep 400-2400 nm (water bands kept) -> first derivative
        -> 5-nm bands R<wl>, FD<wl> -> 44 vegetation indices + REP, Dr, REarea -> NDSI_best, RSI_best, WRI (from the training selection)."""
import numpy as np, pandas as pd
from scipy.signal import savgol_filter
from sklearn.cross_decomposition import PLSRegression
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin

GRADES = [0, 1, 3, 5, 7, 9]

class PLSDA(BaseEstimator, ClassifierMixin):
    """PLS discriminant analysis: PLS regression on one-hot classes, class = largest predicted response."""
    def __init__(self, n_components=2): self.n_components = n_components
    def fit(self, X, y):
        self.classes_ = np.unique(y); Y = (y[:, None] == self.classes_[None, :]).astype(float)
        self.m_ = PLSRegression(min(self.n_components, X.shape[1]), scale=False).fit(X, Y); return self
    def decision_function(self, X): return self.m_.predict(X)
    def predict(self, X): return self.classes_[np.argmax(self.decision_function(X), 1)]
    def predict_proba(self, X):
        s = self.decision_function(X); e = np.exp(s - s.max(1, keepdims=True)); return e / e.sum(1, keepdims=True)

class PLSR(BaseEstimator, RegressorMixin):
    def __init__(self, n_components=2): self.n_components = n_components
    def fit(self, X, y): self.m_ = PLSRegression(min(self.n_components, X.shape[1]), scale=False).fit(X, y); return self
    def predict(self, X): return self.m_.predict(X).ravel()

def preprocess(X_raw, wl_raw):
    """Return wl (400-2400, 1 nm), R1, FD1 (1 nm) and w5, R5, FD5 (5 nm)."""
    X_raw = np.asarray(X_raw, float); wl_raw = np.asarray(wl_raw, float)
    if X_raw.ndim == 1: X_raw = X_raw[None, :]
    full = np.arange(350, 2501)
    if len(wl_raw) != len(full) or np.abs(wl_raw - full).max() > 0.01:     # resample to 1 nm if the grid differs
        X_raw = np.vstack([np.interp(full, wl_raw, x) for x in X_raw]); wl_raw = full.astype(float)
    keep = (wl_raw >= 400) & (wl_raw <= 2400); wl = wl_raw[keep]
    R1 = savgol_filter(X_raw, 11, 2, axis=1)[:, keep]; FD1 = savgol_filter(X_raw, 11, 2, deriv=1, axis=1)[:, keep]
    w5 = np.arange(400, 2401, 5); i5 = np.searchsorted(wl, w5)
    return wl, R1, FD1, w5, R1[:, i5], FD1[:, i5]

def indices(R1, FD1):
    ix = lambda w: int(round(w - 400)); r = lambda w: R1[:, ix(w)]; nd = lambda a, b: (r(a) - r(b)) / (r(a) + r(b))
    I = {}
    I['NDVI'] = nd(800, 670); I['NDVI850'] = nd(850, 650); I['SR'] = r(800) / r(680); I['RVI'] = r(800) / r(670); I['GNDVI'] = nd(850, 550)
    I['RDVI'] = (r(800) - r(670)) / np.sqrt(r(800) + r(670)); I['MSR'] = (r(800) / r(670) - 1) / np.sqrt(r(800) / r(670) + 1)
    I['OSAVI'] = 1.16 * (r(800) - r(670)) / (r(800) + r(670) + 0.16)
    I['TVI'] = 0.5 * (120 * (r(750) - r(550)) - 200 * (r(670) - r(550))); I['MTVI2'] = 1.5 * (1.2 * (r(800) - r(550)) - 2.5 * (r(670) - r(550))) / np.sqrt((2 * r(800) + 1) ** 2 - (6 * r(800) - 5 * np.sqrt(r(670))) - 0.5)
    I['MCARI'] = ((r(700) - r(670)) - 0.2 * (r(700) - r(550))) * (r(700) / r(670)); I['TCARI'] = 3 * ((r(700) - r(670)) - 0.2 * (r(700) - r(550)) * (r(700) / r(670)))
    I['VIgreen'] = nd(550, 670); I['GI'] = r(554) / r(677)
    I['CIrededge'] = r(790) / r(720) - 1; I['CIgreen'] = r(790) / r(550) - 1; I['NDRE'] = nd(790, 720); I['MTCI'] = (r(754) - r(709)) / (r(709) - r(681))
    I['PSSRa'] = r(800) / r(680); I['PSSRb'] = r(800) / r(635); I['PSSRc'] = r(800) / r(470)
    I['SIPI'] = (r(800) - r(445)) / (r(800) - r(680)); I['NPCI'] = nd(680, 430); I['PSRI'] = (r(680) - r(500)) / r(750)
    I['ARI'] = 1 / r(550) - 1 / r(700); I['PRI'] = nd(531, 570); I['NPQI'] = nd(415, 435); I['RVSI'] = (r(712) + r(752)) / 2 - r(732)
    I['HI'] = nd(534, 698) - 0.5 * r(704)
    I['WI'] = r(900) / r(970); I['WBI'] = r(970) / r(900); I['NDWI'] = nd(860, 1240); I['MoistSI'] = r(1600) / r(820); I['NDII'] = nd(819, 1649)
    I['DWSI-1'] = r(800) / r(1660); I['DWSI-2'] = r(1660) / r(550); I['DWSI-3'] = r(1660) / r(680); I['DWSI-4'] = r(550) / r(680); I['DWSI-5'] = (r(800) + r(550)) / (r(1660) + r(680))
    I['RBI'] = r(1148) / r(1301); I['NDBI'] = nd(1148, 1301)
    F = pd.DataFrame(I); fdre = FD1[:, ix(680):ix(760) + 1]
    F['REP'] = 680 + fdre.argmax(1).astype(float); F['Dr'] = fdre.max(1) * 1000; F['REarea'] = fdre.sum(1)
    return F

def all_features(X_raw, wl_raw, sel):
    """Full candidate table (5-nm bands + indices + NDSI_best, RSI_best, WRI); `sel` = selection dict saved with the models."""
    wl, R1, FD1, w5, R5, FD5 = preprocess(X_raw, wl_raw); g = lambda lam: R1[:, int(round(lam - 400))]
    T = pd.DataFrame(np.hstack([R5, FD5]), columns=['R%d' % w for w in w5] + ['FD%d' % w for w in w5])
    F = indices(R1, FD1); a, b = sel['ndsi']; c, d = sel['rsi']; W = sel['wri']
    F['NDSI_best'] = (g(a) - g(b)) / (g(a) + g(b)); F['RSI_best'] = g(c) / g(d); F['WRI'] = (g(W['l1']) - g(W['l2'])) / (g(W['l1']) + g(W['l2'])) + W['w'] * g(W['l3'])
    return pd.concat([T, F], axis=1)
