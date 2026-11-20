"""Dummy multi-class ReliefF figure (real ReliefF computation on simulated 4-class canopy spectra)."""
import os, json
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

D = os.path.dirname(os.path.abspath(__file__)) + '/'
plt.rcParams['font.family'] = 'DejaVu Sans'
rng = np.random.default_rng(11)
import sys
SW = float(sys.argv[1]) if len(sys.argv) > 1 else 0.10
IL = float(sys.argv[2]) if len(sys.argv) > 2 else 0.03
GR = float(sys.argv[3]) if len(sys.argv) > 3 else 0.03
RE = float(sys.argv[4]) if len(sys.argv) > 4 else 0.05
GT = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
CL = ['Healthy', 'Low', 'Moderate', 'High']; CC = ['#2E7D32', '#F9A825', '#EF6C00', '#C62828']

# ---- simulated spectra ----
pts_h = [(400,.040),(450,.045),(500,.060),(550,.120),(600,.070),(650,.045),(680,.040),(700,.090),(720,.250),(750,.420),(800,.460),(900,.470),(970,.440),(1050,.460),(1200,.400),(1300,.420),(1450,.200),(1650,.300),(1800,.270),(1940,.080),(2100,.180),(2200,.200),(2300,.150),(2400,.110)]
pts_d = [(400,.060),(450,.070),(500,.090),(550,.150),(600,.110),(650,.090),(680,.085),(700,.130),(720,.240),(750,.350),(800,.380),(900,.390),(970,.370),(1050,.390),(1200,.360),(1300,.380),(1450,.240),(1650,.330),(1800,.300),(1940,.120),(2100,.220),(2200,.240),(2300,.190),(2400,.140)]
w = np.arange(400, 2401, 5)
keep = ~(((w >= 1350) & (w <= 1450)) | ((w >= 1800) & (w <= 1950)))
w = w[keep]
H = PchipInterpolator(*zip(*pts_h))(w); Dd = PchipInterpolator(*zip(*pts_d))(w)
ns = [120, 140, 90, 50]
cls = np.repeat(np.arange(4), ns)
lo = np.array([0, 0.02, 0.34, 0.67]); hi = np.array([0, 0.33, 0.66, 1.0])
a = rng.uniform(lo[cls], hi[cls])                                   # within-class severity (classes overlap at limits)
X = H + GT * a[:, None] * (Dd - H)
green = np.exp(-((w - 555) / 25) ** 2); X += GR * np.minimum(a, 0.35)[:, None] / 0.35 * green      # early pigment change (Low onwards)
redge = np.exp(-((w - 705) / 12) ** 2); X += RE * (a ** 0.5)[:, None] * redge                    # red-edge shift (non-linear)
swir = np.exp(-((w - 1620) / 140) ** 2); X += SW * (a ** 3)[:, None] * swir                     # broad SWIR rise (water loss), accelerating at high severity
X *= rng.uniform(1 - IL, 1 + IL, (len(a), 1))                                                          # illumination
from scipy.ndimage import gaussian_filter1d
X += gaussian_filter1d(rng.normal(0, 0.004, X.shape), 3, axis=1)                                   # smooth sensor noise (after Savitzky-Golay)

# ---- ReliefF (Robnik-Sikonja and Kononenko, 2003) ----
def relieff(X, y, k=10):
    rngX = X.max(0) - X.min(0); Z = (X - X.min(0)) / rngX
    Dm = np.abs(Z[:, None, :] - Z[None, :, :]).sum(2); np.fill_diagonal(Dm, np.inf)
    cls_ = np.unique(y); P = {c: np.mean(y == c) for c in cls_}; m = len(y); W = np.zeros(X.shape[1])
    for i in range(m):
        same = np.where(y == y[i])[0]; same = same[same != i]
        hits = same[np.argsort(Dm[i, same])[:k]]
        W -= np.abs(Z[i] - Z[hits]).sum(0) / (m * k)
        for c in cls_:
            if c == y[i]: continue
            oth = np.where(y == c)[0]; miss = oth[np.argsort(Dm[i, oth])[:k]]
            W += P[c] / (1 - P[y[i]]) * np.abs(Z[i] - Z[miss]).sum(0) / (m * k)
    return W
W = relieff(X, cls)

# ---- top 5% + one band per correlated region (r >= 0.95) ----
C = np.corrcoef(X.T); regions = []; i = 0
while i < len(w):
    j = i
    while j + 1 < len(w) and C[i, j + 1] >= 0.95 and w[j + 1] - w[j] == 5: j += 1
    regions.append((i, j)); i = j + 1
thr = np.percentile(W, 95); sel = []
for (i, j) in regions:
    idx = np.arange(i, j + 1); idx = idx[W[idx] >= thr]
    if len(idx): sel.append(idx[np.argmax(W[idx])])
sel = sorted(sel)

# ---- pairwise ReliefF at selected bands ----
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
PW = np.zeros((len(pairs), len(sel)))
for r, (p, q) in enumerate(pairs):
    m = (cls == p) | (cls == q); PW[r] = relieff(X[m][:, sel], cls[m])

# ---- figure ----
fig = plt.figure(figsize=(12, 10.2)); gs = fig.add_gridspec(3, 1, height_ratios=[1, 1, 1.05], hspace=0.42)
ax = fig.add_subplot(gs[0])
for k in range(4):
    s = X[cls == k].mean(0); full = np.full(len(w), np.nan); ax.plot(w, s, color=CC[k], lw=1.6, label=CL[k])
for b in sel: ax.axvline(w[b], color='#555', lw=0.7, ls=':')
ax.set_ylabel('Reflectance'); ax.legend(fontsize=8.5, ncol=4, loc='upper right'); ax.set_xlim(400, 2400)
ax.set_title('(a) Dummy class-mean spectra (dotted lines = bands kept by ReliefF)', fontsize=10)
ax = fig.add_subplot(gs[1])
wf = np.arange(400, 2401, 5); Wf = np.full(len(wf), np.nan); Wf[np.isin(wf, w)] = W
ax.fill_between(wf, 0, np.where(np.isnan(Wf), 0, Wf), color='#1565C0', alpha=0.45, step='mid')
ax.axhline(thr, color='#C62828', ls='--', lw=1); ax.text(2395, thr, ' top 5%', color='#C62828', fontsize=8, va='bottom', ha='right')
ax.plot(w[sel], W[sel], '*', color='#C62828', ms=12)
for b in sel: ax.text(w[b], W[b] * 1.04, '%d' % w[b], ha='center', va='bottom', fontsize=8)
for x0, x1 in ((1350, 1450), (1800, 1950)): ax.axvspan(x0, x1, color='#EEEEEE')
ax.set_xlim(400, 2400); ax.set_ylabel('ReliefF weight'); ax.set_xlabel('Wavelength (nm)')
ax.set_ylim(min(0, W.min() * 1.1), W.max() * 1.22)
ax.set_title('(b) Multi-class ReliefF weights (Healthy, Low, Moderate, High; k = 10); stars = one band kept per correlated region', fontsize=10)
ax = fig.add_subplot(gs[2])
im = ax.imshow(PW, cmap='YlGnBu', aspect='auto')
for r in range(PW.shape[0]):
    for c in range(PW.shape[1]): ax.text(c, r, '%.2f' % PW[r, c], ha='center', va='center', fontsize=8.5, color='white' if PW[r, c] > PW.max() * 0.6 else 'black')
ax.set_xticks(range(len(sel)), ['%d nm' % w[b] for b in sel], fontsize=8.5)
ax.set_yticks(range(len(pairs)), ['%s – %s' % (CL[p], CL[q]) for p, q in pairs], fontsize=8.5)
plt.colorbar(im, ax=ax, fraction=0.025, label='Pairwise ReliefF weight')
ax.set_title('(c) Which class pair each selected band separates (ReliefF run on each pair of classes)', fontsize=10)
fig.suptitle('Dummy data: ReliefF for the four white-rust severity classes', fontsize=11.5, fontweight='bold', y=0.935)
plt.savefig(D + 'fig/m19_relief.png', dpi=200, bbox_inches='tight'); plt.close()
json.dump({'sel': [int(w[b]) for b in sel], 'n_regions': len(regions)}, open(D + 'relief_dummy.json', 'w'))
print('selected bands', [int(w[b]) for b in sel], 'regions', len(regions))

