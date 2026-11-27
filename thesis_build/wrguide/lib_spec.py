"""Spectral pre-processing and features (methodology Part C). Every function works leaf by leaf (one row = one leaf)."""
import numpy as np, pandas as pd
from scipy.signal import savgol_filter, fftconvolve
from sklearn.cross_decomposition import PLSRegression
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
import config as C


def splice_correct(X, wl):
    """Step A5: additive correction of the ASD detector steps (Hueni and Bialek, 2017). At each join J the jump X[J+1] - X[J] is compared with the
    local slope (mean of the differences just below and just above the join). If the median excess is larger than SPLICE_MIN_STEP, the bands above J
    are shifted so that the jump equals the local slope, leaf by leaf; otherwise the join is left unchanged."""
    X = X.copy(); before, after, applied = {}, {}, {}
    for J in C.SPLICE_JOINS:
        i = int(np.where(wl == J)[0][0]); step = X[:, i + 1] - X[:, i]; slope = 0.5 * ((X[:, i] - X[:, i - 1]) + (X[:, i + 2] - X[:, i + 1]))
        before[J] = float(np.median(step - slope)); applied[J] = abs(before[J]) > C.SPLICE_MIN_STEP
        if applied[J]: X[:, i + 1:] -= (step - slope)[:, None]
        after[J] = float(np.median((X[:, i + 1] - X[:, i]) - 0.5 * ((X[:, i] - X[:, i - 1]) + (X[:, i + 2] - X[:, i + 1]))))
    return X, before, after, applied


def preprocess(X, wl):
    """Steps C2-C6: Savitzky-Golay (11, 2) and first derivative on 350-2500 nm, trim to 400-2400 nm, 5-nm band means (lambda-2 ... lambda+2)."""
    R = savgol_filter(X, C.SG_WINDOW, C.SG_ORDER, axis=1); FD = savgol_filter(X, C.SG_WINDOW, C.SG_ORDER, deriv=1, axis=1)
    keep = (wl >= C.WL_MIN) & (wl <= C.WL_MAX); w1 = wl[keep]; R1, FD1 = R[:, keep], FD[:, keep]
    w5 = np.arange(C.WL_MIN, C.WL_MAX + 1, C.BAND_STEP)
    idx = [np.where((w1 >= w - 2) & (w1 <= w + 2))[0] for w in w5]
    R5 = np.stack([R1[:, i].mean(1) for i in idx], 1); FD5 = np.stack([FD1[:, i].mean(1) for i in idx], 1)
    return w1, R1, FD1, w5, R5, FD5


def join_mask(w):
    """True for wavelengths outside the detector-join zones (Step C1)."""
    m = np.ones(len(w), bool)
    for a, b in C.JOIN_ZONES: m &= ~((w >= a) & (w <= b))
    return m


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



def continuum_removed(R1, w1):
    """Step C9: depth, width (at half depth, nm), area and position of each absorption feature after continuum removal (upper convex hull)."""
    out = {}
    for name, (a, b) in C.CR_FEATURES.items():
        sel = (w1 >= a) & (w1 <= b); w = w1[sel]; D, Wd, Ar, Ps = [], [], [], []
        for r in R1[:, sel]:
            hull = [0]
            for k in range(1, len(w)):                                            # monotone chain, upper hull
                while len(hull) >= 2:
                    i, j = hull[-2], hull[-1]
                    if (r[j] - r[i]) * (w[k] - w[i]) <= (r[k] - r[i]) * (w[j] - w[i]): hull.pop()
                    else: break
                hull.append(k)
            cont = np.interp(w, w[hull], r[hull]); dep = 1 - r / cont; m = dep.max()
            D.append(m); Ps.append(w[dep.argmax()]); Ar.append(dep.sum()); Wd.append(float((dep >= m / 2).sum()) if m > 0 else 0.0)
        out[name + '_depth'], out[name + '_width'], out[name + '_area'], out[name + '_pos'] = D, Wd, Ar, Ps
    return pd.DataFrame(out)


def mexican_hat(scale):
    t = np.arange(-5 * scale, 5 * scale + 1, dtype=float) / scale
    return (2 / (np.sqrt(3) * np.pi ** 0.25)) * (1 - t ** 2) * np.exp(-t ** 2 / 2) / np.sqrt(scale)


def cwt(R1):
    """Step C10: continuous wavelet transform (Mexican hat) of every spectrum at the scales of config.CWT_SCALES; returns n x scales x bands."""
    out = np.zeros((R1.shape[0], len(C.CWT_SCALES), R1.shape[1]), np.float32)
    for s, a in enumerate(C.CWT_SCALES):
        k = mexican_hat(a); pad = len(k)
        Z = np.pad(R1, ((0, 0), (pad, pad)), mode='reflect')
        out[:, s, :] = fftconvolve(Z, k[None, :], mode='same', axes=1)[:, pad:-pad]
    return out


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

