"""ASD FieldSpec spectra -> white rust features and models.

Step-by-step functions that follow the protocol in MuDAS-AI_ASD_Spectral_Protocol.docx.
Methods combine Selvaprakash et al. (2026), Mandal et al. (2022) and Gogoi et al. (2018)
with plot/plant-grouped validation. Tested only on simulated spectra (demo_simulated.py).

Spectra are held as a 2-D array R (samples x bands) with a wavelength vector wl (nm),
plus a metadata DataFrame `meta` with one row per sample (same order).
"""
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from scipy.stats import spearmanr, kruskal, rankdata

# ----------------------------------------------------------------------------- Step 3: import
def load_viewspec_ascii(path, sep="\t"):
    """ViewSpec Pro 'ASCII export, output to single file': first column = wavelength,
    one column per .asd file. Returns wl (nm), R (samples x bands), sample names."""
    df = pd.read_csv(path, sep=sep)
    wl = df.iloc[:, 0].to_numpy(float)
    R = df.iloc[:, 1:].to_numpy(float).T
    names = [str(c).strip() for c in df.columns[1:]]
    return wl, R, names


# ----------------------------------------------------------------------------- Step 4: quality control
def splice_correct(R, wl, splices=(1000, 1800), n_fit=3):
    """Remove the step at the detector joins (VNIR|SWIR1 at 1000/1001 nm, SWIR1|SWIR2 at 1800/1801 nm).
    SWIR1 is the reference; VNIR and SWIR2 are shifted additively so that each join matches a
    linear extrapolation of the neighbouring SWIR1 bands."""
    R = R.copy()
    s1, s2 = splices
    i1 = np.searchsorted(wl, s1, side="right")          # first SWIR1 band index
    i2 = np.searchsorted(wl, s2, side="right")          # first SWIR2 band index
    # VNIR: extrapolate SWIR1 backwards one band and shift VNIR to meet it
    slope = (R[:, i1 + n_fit - 1] - R[:, i1]) / (n_fit - 1)
    expected = R[:, i1] - slope
    R[:, :i1] += (expected - R[:, i1 - 1])[:, None]
    # SWIR2: extrapolate SWIR1 forwards one band and shift SWIR2 to meet it
    slope = (R[:, i2 - 1] - R[:, i2 - n_fit]) / (n_fit - 1)
    expected = R[:, i2 - 1] + slope
    R[:, i2:] += (expected - R[:, i2])[:, None]
    return R


NOISY = [(350, 399), (1341, 1459), (1791, 1959), (2351, 2500)]   # low signal and atmospheric water


def band_mask(wl, drop=NOISY):
    keep = np.ones(wl.size, bool)
    for a, b in drop:
        keep &= ~((wl >= a) & (wl <= b))
    return keep


def average_replicates(R, meta, key="leaf_id"):
    """Average repeated readings (e.g. 3 per leaf) into one spectrum per leaf."""
    g = meta[key].to_numpy()
    ids = pd.unique(g)
    Ravg = np.vstack([R[g == i].mean(0) for i in ids])
    m = meta.groupby(key, sort=False).first().loc[ids].reset_index()
    return Ravg, m


def physical_checks(R, wl):
    """Flags: reflectance outside 0-1, NIR plateau too low (background/soil), red not below green."""
    nir = R[:, (wl >= 780) & (wl <= 900)].mean(1)
    red = R[:, (wl >= 660) & (wl <= 680)].mean(1)
    green = R[:, (wl >= 540) & (wl <= 560)].mean(1)
    return pd.DataFrame({"out_of_range": (R < 0).any(1) | (R > 1).any(1),
                         "low_nir": nir < 0.2, "no_green_peak": red >= green})


def sam(a, b):
    """Spectral angle (radians) between spectra a (n x p) and reference b (p,)."""
    cos = (a @ b) / (np.linalg.norm(a, axis=1) * np.linalg.norm(b))
    return np.arccos(np.clip(cos, -1, 1))


# ----------------------------------------------------------------------------- Step 5: pre-processing
def sg(R, window=11, order=2, deriv=0):
    """Savitzky-Golay smoothing (deriv=0) or derivative (deriv=1, 2) along wavelength (1 nm step)."""
    return savgol_filter(R, window, order, deriv=deriv, delta=1.0, axis=1)


def snv(R):
    """Standard normal variate: each spectrum centred and scaled by its own mean and SD."""
    return (R - R.mean(1, keepdims=True)) / R.std(1, keepdims=True)


def msc(R, ref=None):
    """Multiplicative scatter correction against a reference (default: mean of R).
    Return the reference too, so that test spectra can be corrected with the TRAINING mean."""
    ref = R.mean(0) if ref is None else ref
    out = np.empty_like(R)
    for i, x in enumerate(R):
        b, a = np.polyfit(ref, x, 1)
        out[i] = (x - a) / b
    return out, ref


def continuum_removed(R, wl, lo, hi):
    """Continuum removal over [lo, hi] nm: divide by the upper convex hull. Returns (wl_seg, CR)."""
    s = (wl >= lo) & (wl <= hi)
    w, out = wl[s], []
    for x in R[:, s]:
        hull = [0]
        for i in range(1, w.size):                      # monotone-chain upper hull
            while len(hull) >= 2:
                i0, i1 = hull[-2], hull[-1]
                if (x[i1] - x[i0]) * (w[i] - w[i0]) <= (x[i] - x[i0]) * (w[i1] - w[i0]):
                    hull.pop()
                else:
                    break
            hull.append(i)
        out.append(x / np.interp(w, w[hull], x[hull]))
    return w, np.array(out)


# ----------------------------------------------------------------------------- Step 6-7: exploration and sensitive regions
def correlation_spectrum(R, y):
    """Spearman rho between severity grade y and every band."""
    rho = np.array([spearmanr(R[:, j], y)[0] for j in range(R.shape[1])])
    return rho


def bh_fdr(p):
    """Benjamini-Hochberg adjusted p-values."""
    p = np.asarray(p)
    n = p.size
    order = np.argsort(p)
    adj = p[order] * n / (np.arange(n) + 1)
    adj = np.minimum.accumulate(adj[::-1])[::-1]
    out = np.empty(n)
    out[order] = np.minimum(adj, 1)
    return out


def kruskal_spectrum(R, y):
    """Kruskal-Wallis H test across severity classes for every band; returns H and FDR q-values."""
    classes = np.unique(y)
    H, p = zip(*[kruskal(*[R[y == c, j] for c in classes]) for j in range(R.shape[1])])
    return np.array(H), bh_fdr(p)


def lagged_correlation(R, max_lag=60):
    """Mean across bands of corr(R[:, j], R[:, j+k]) for k = 1..max_lag (Selvaprakash et al. 2026)."""
    Z = (R - R.mean(0)) / R.std(0)
    n = R.shape[0]
    return np.array([np.nanmean((Z[:, :-k] * Z[:, k:]).sum(0) / n) for k in range(1, max_lag + 1)])


def persistence(signal, threshold):
    """Length of the contiguous run of bands with |signal| >= threshold that each band belongs to."""
    on = np.abs(signal) >= threshold
    out = np.zeros(signal.size, int)
    i = 0
    while i < signal.size:
        if on[i]:
            j = i
            while j < signal.size and on[j]:
                j += 1
            out[i:j] = j - i
            i = j
        else:
            i += 1
    return out


# ----------------------------------------------------------------------------- Step 8: features
def b(R, wl, nm):
    """Reflectance at the band nearest to nm."""
    return R[:, np.argmin(np.abs(wl - nm))]


def red_edge(R, wl, lo=680, hi=760, sum_lo=670, sum_hi=780):
    """Red-edge parameters (Mandal et al. 2022): REP and REV from the first derivative
    (SG smoothed, sub-nm REP by a 2nd-order polynomial around the peak), sum of dR 670-780 nm,
    and the linear four-point REP of Guyot & Baret (1988)."""
    d1 = sg(R, 11, 2, deriv=1)
    s = (wl >= lo) & (wl <= hi)
    w, d = wl[s], d1[:, s]
    k = d.argmax(1)
    rep, rev = np.empty(len(R)), np.empty(len(R))
    for i, ki in enumerate(k):
        a, c = max(ki - 5, 0), min(ki + 6, w.size)
        p = np.polyfit(w[a:c], d[i, a:c], 2)
        rep[i] = -p[1] / (2 * p[0]) if p[0] < 0 else w[ki]
        rev[i] = np.polyval(p, rep[i]) if p[0] < 0 else d[i, ki]
    ss = (wl >= sum_lo) & (wl <= sum_hi)
    r_re = (b(R, wl, 670) + b(R, wl, 780)) / 2
    rep_lin = 700 + 40 * (r_re - b(R, wl, 700)) / (b(R, wl, 740) - b(R, wl, 700))
    return pd.DataFrame({"REP": rep, "REV": rev, "SDr670_780": d1[:, ss].sum(1), "REP_linear": rep_lin})


def indices(R, wl):
    """Published indices; SWIR ones are available only from ASD/field spectroscopy, not VNIR UAV cameras."""
    B = lambda nm: b(R, wl, nm)
    nd = lambda x, y: (B(x) - B(y)) / (B(x) + B(y))
    return pd.DataFrame({
        "NDVI": nd(800, 680), "PRI": nd(531, 570), "NDRE": nd(790, 720),
        "CIre": B(790) / B(720) - 1, "PSRI": (B(680) - B(500)) / B(750),
        "MCARI": ((B(700) - B(670)) - 0.2 * (B(700) - B(550))) * (B(700) / B(670)),
        "ARI": 1 / B(550) - 1 / B(700), "CRI1": 1 / B(510) - 1 / B(550),
        "PSSRa": B(800) / B(680), "PSSRb": B(800) / B(635),
        "mND705": (B(750) - B(705)) / (B(750) + B(705) - 2 * B(445)),
        "WBI": B(900) / B(970),
        "NDWI_1240": nd(860, 1240), "MSI": B(1600) / B(820), "DWSI1": B(800) / B(1660),
        "RBI": nd(1068, 1560),
    })


def ndsi_search(R, wl, y, step=10, lo=400, hi=2350, keep=None):
    """Exhaustive normalised-difference search (Ri - Rj)/(Ri + Rj) on bands every `step` nm.
    Score = |Spearman rho| with severity. RUN ON TRAINING SAMPLES ONLY.
    Returns a DataFrame of all pairs sorted by score."""
    sel = (wl >= lo) & (wl <= hi) & (np.ones(wl.size, bool) if keep is None else keep)
    sel &= (np.round(wl) % step == 0)
    w, X = wl[sel], R[:, sel]
    ry = rankdata(y)
    ry = (ry - ry.mean()) / ry.std()
    rows = []
    for i in range(w.size - 1):
        N = (X[:, i:i + 1] - X[:, i + 1:]) / (X[:, i:i + 1] + X[:, i + 1:])
        RN = np.apply_along_axis(rankdata, 0, N)
        RN = (RN - RN.mean(0)) / RN.std(0)
        rho = (RN * ry[:, None]).mean(0)
        rows.append(pd.DataFrame({"b1": w[i], "b2": w[i + 1:], "rho": rho}))
    out = pd.concat(rows, ignore_index=True)
    out["abs_rho"] = out.rho.abs()
    return out.sort_values("abs_rho", ascending=False, ignore_index=True)


def ndsi(R, wl, b1, b2):
    return (b(R, wl, b1) - b(R, wl, b2)) / (b(R, wl, b1) + b(R, wl, b2))


# ----------------------------------------------------------------------------- Step 11: link to UAV sensors
MICASENSE_MX = {"Blue": (475, 32), "Green": (560, 27), "Red": (668, 14), "RedEdge": (717, 12), "NIR": (842, 57)}


def simulate_bands(R, wl, bands):
    """Convolve ASD spectra with Gaussian spectral response functions {name: (centre nm, FWHM nm)}."""
    out = {}
    for name, (c, fwhm) in bands.items():
        w = np.exp(-4 * np.log(2) * (wl - c) ** 2 / fwhm ** 2)
        out[name] = (R * w).sum(1) / w.sum()
    return pd.DataFrame(out)
