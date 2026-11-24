"""Builds the Jupyter notebook that applies the top ASD white rust models to every crop pixel of the UAV hyperspectral image of 24 Feb 2026
(pixel-level disease maps). Models come from uavp/kit/models (export_models.py). Output: uavp/kit/White_rust_pixel_map_24Feb2026.ipynb"""
import json, os, sys, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'; TB = HERE + '../'
SC = pd.read_csv(TB + 'uavt/out/spectra_compare.csv'); GT = pd.read_csv(TB + 'uavt/out/ground_truth.csv'); MX = pd.read_csv(TB + 'uavt/out/maxstat.csv').set_index('task')
MT = json.load(open(HERE + 'kit/models/model_table.json'))
fmt = lambda a, d=10: '[' + ', '.join(('%.' + str(d) + 'g') % x for x in a) + ']'
MD, CODE = 'markdown', 'code'; cells = []
def add(kind, text): cells.append((kind, text.strip('\n')))
mt_rows = '\n'.join('| %s | %s | %s | %s | %s %.3f%s |' % ({'A': 'Detection', 'B': 'Six grades', 'C': 'Severity score'}[m['task']], m['model'], m['why'], m['variant'], 'macro-F1' if m['task'] != 'C' else 'R²', m['uav_value'],
                    (', AUC %.2f' % m['uav_auc']) if m.get('uav_auc') else '') for m in MT)

add(MD, r"""# White rust pixel-level disease maps – UAV hyperspectral image of 24 February 2026
This notebook applies the **top ASD white rust models** of the 2025-26 analysis to **every crop pixel** of the Headwall hyperspectral image of 24 Feb 2026 and writes, for each model, a pixel-level map (GeoTIFF/ENVI raster + PNG) and a per-plot accuracy check against the ASD leaf scores of the same day.

**Top models** (best on the leaves by leave-one-replication-out, plus the best transfer to the UAV plots) and their accuracy on the 48 UAV plot spectra (transfer report):

| Task | Model | Why it is a top model | Input used | Accuracy on the UAV plots |
|---|---|---|---|---|
MTROWS

**Which map to use.** Only the **ConvNeXt V2-Atto detection map** transferred beyond chance (maximum-statistic permutation p = MXP; Westfall and Young, 1993). The other maps are produced because they are the top leaf models, but their UAV accuracy is at chance (detection SVM, DNN-F1) or below chance (grades, score): **do not interpret the grade and score maps as severity** – they show what the leaf models predict, not validated severity.

**Steps.** 1 settings · 2 libraries and image helpers · 3 networks · 4 reference spectra, ground truth, model table · 5 features (identical to the ASD pipeline) · 6 load the models · 7 self-check on the 48 plot means · 8 open the image · 9 pixel loop (all models in one pass) · 10 maps · 11 per-plot accuracy · 12 summary.

**Requirements.** Python 3.9+, `numpy`, `scipy`, `pandas`, `matplotlib`, `torch` (CPU: `pip install torch --index-url https://download.pytorch.org/whl/cpu`); optional `rasterio` for GeoTIFF. The ML models (SVM, RF, XGBoost) are stored as plain arrays and predicted with NumPy, so scikit-learn/xgboost versions do not matter.

**Time.** First run with `SPATIAL_STEP = 4` (preview); then `SPATIAL_STEP = 1` for the final maps (≈ 5 million pixels; the two ConvNeXt networks take most of the time).""".replace('MTROWS', mt_rows).replace('MXP', '%.3f' % MX.loc['A', 'p_value']))

add(MD, "## 1 Settings\nChange the paths. `MODELS_TO_RUN` selects the maps; the first entry is the recommended detection model.")
add(CODE, r"""# ============================ SETTINGS ============================
HDR_FILE  = r'D:\Coalighned\24_02_2026\subset_200526.hdr'          # ENVI header of the 24 Feb image
DATA_NAME = 'subset_200526'                                         # image data file next to the .hdr
ROI_FILE  = r'D:\Coalighned\24_02_2026\48_plot_roi_new.xml'        # 48 plot ROIs (None = skip the per-plot accuracy)
KIT_DIR   = r'D:\Coalighned\white_rust_pixel_kit'                  # unzipped kit (contains the folder 'models')
PLOT_AVG_FILE = r'D:\Coalighned\24_02_2026\envi_plot_avg.txt'      # ENVI plot-average file for the self-check (None = skip)
OUT_NAME  = 'white_rust_pixel_maps_24Feb2026'                       # results folder, created next to the image

MODELS_TO_RUN = ['A_ConvNeXt_V2-Atto',      # detection, best transfer to the UAV  <- recommended map
                 'A_SVM', 'A_DNN-F1',       # detection, best leaf models (ML, DL)
                 'B_ConvNeXt_V2-Atto', 'B_RF',   # six grades, best leaf models (DL, ML)
                 'C_XGBoost', 'C_DNN-F1']   # severity score, best leaf models (ML, DL)
SPATIAL_STEP = 4        # 4 = quick preview; 1 = final full-resolution maps
BLOCK_ROWS   = 16       # image rows processed at a time (reduce if memory is short)
NDVI_MIN     = 0.6      # crop mask NDVI(898, 684) > 0.6 as in the methodology; 0 = use only the existing mask
THRESHOLD    = 0.5      # detection: probability above which a pixel is 'diseased' (SVM: decision value > 0)
PLOT_DISEASED_SHARE = 0.5   # a plot is called diseased if more than this share of its pixels is diseased
REFLECTANCE_SCALE = 'auto'  # 'auto' (divides by 10000 if the data look like 0-10000) or a number
BATCH  = 32768          # pixels per network batch
DEVICE = 'cpu'""")

add(MD, "## 2 Libraries and image helpers\nThe ENVI reader, georeferencing and ROI parser are those of the hourglass notebook (`HSI_hourglass_workflow_CODE.ipynb`), which already works with this image. The image is memory-mapped: only the rows being processed are read.")
add(CODE, r"""import os, re, json, time, math, warnings
import xml.etree.ElementTree as ET
import numpy as np, pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.path import Path as MplPath
from matplotlib.colors import ListedColormap, BoundaryNorm
from scipy.signal import savgol_coeffs
import torch, torch.nn as nn, torch.nn.functional as Fn
warnings.filterwarnings('ignore', category=RuntimeWarning)
try:
    from IPython.display import Image as _Img, display as _display
    def show(path, width=900): _display(_Img(path, width=width))
except Exception:
    def show(path, width=900): print('saved', path)

assert os.path.exists(HDR_FILE), f'Header not found: {HDR_FILE}'
SRC = os.path.dirname(HDR_FILE); _base = os.path.splitext(HDR_FILE)[0]
DATA_FILE = next((c for c in [os.path.join(SRC, DATA_NAME), _base, _base + '.dat', _base + '.img', _base + '.bil', _base + '.raw']
                  if os.path.isfile(c) and not c.lower().endswith('.hdr')), None)
if DATA_FILE is None:
    raise FileNotFoundError(f'Image data file not found next to {HDR_FILE}. Files there: {os.listdir(SRC)}')
OUT = os.path.join(SRC, OUT_NAME); os.makedirs(OUT, exist_ok=True); MODEL_DIR = os.path.join(KIT_DIR, 'models')

ENVI_DTYPES = {1: np.uint8, 2: np.int16, 3: np.int32, 4: np.float32, 5: np.float64, 12: np.uint16, 13: np.uint32, 14: np.int64, 15: np.uint64}
def read_envi_header(path):
    txt = open(path, encoding='latin-1').read(); hdr = {}
    for m in re.finditer(r'^\s*([^=\n{}]+?)\s*=\s*(\{[^}]*\}|[^\n]*)', txt, re.M):
        v = m.group(2).strip(); hdr[m.group(1).strip().lower()] = v[1:-1].strip() if v.startswith('{') else v
    return hdr
class EnviCube:
    # memory-mapped input image; reads only what is needed
    def __init__(self, path, hdr):
        self.ns, self.nl, self.nb = int(hdr['samples']), int(hdr['lines']), int(hdr['bands'])
        dt = np.dtype(ENVI_DTYPES[int(hdr['data type'])])
        if int(hdr.get('byte order', '0')) == 1: dt = dt.newbyteorder('>')
        self.il = hdr.get('interleave', 'bsq').strip().lower()
        shape = {'bil': (self.nl, self.nb, self.ns), 'bsq': (self.nb, self.nl, self.ns), 'bip': (self.nl, self.ns, self.nb)}[self.il]
        off = int(hdr.get('header offset', '0'))
        if os.path.getsize(path) < off + int(np.prod(shape)) * dt.itemsize: raise ValueError('data file is smaller than the header says')
        self.mm = np.memmap(path, dtype=dt, mode='r', offset=off, shape=shape)
    def rows(self, r0, r1, step):
        # rows r0..r1 (full-res, every step-th row and column) -> (rows, cols, bands) float32
        ys, xs = slice(r0, r1, step), slice(0, self.ns, step)
        if self.il == 'bil': a = np.asarray(self.mm[ys, :, xs]).transpose(0, 2, 1)
        elif self.il == 'bsq': a = np.asarray(self.mm[:, ys, xs]).transpose(1, 2, 0)
        else: a = np.asarray(self.mm[ys, xs])
        return a.astype(np.float32)
class Geo:
    def __init__(self, hdr):
        mi = [s.strip() for s in hdr['map info'].split(',')]; self.items, self.proj = mi, mi[0]
        self.refx, self.refy, self.e0, self.n0, self.dx, self.dy = map(float, mi[1:7]); self.csys = hdr.get('coordinate system string', '').strip()
        g = self.proj.lower().startswith('geographic')
        self.px_w = self.dx * (111320.0 * np.cos(np.radians(self.n0)) if g else 1.0); self.px_h = self.dy * (110574.0 if g else 1.0)
    def to_file(self, x, y):
        x, y = np.asarray(x, float), np.asarray(y, float); return (x - self.e0) / self.dx + (self.refx - 1), (self.n0 - y) / self.dy + (self.refy - 1)
    def to_map(self, fx, fy):
        fx, fy = np.asarray(fx, float), np.asarray(fy, float); return self.e0 + (fx - (self.refx - 1)) * self.dx, self.n0 - (fy - (self.refy - 1)) * self.dy
    def map_info(self, step=1):
        e, n = self.to_map(0.5 - 0.5 * step, 0.5 - 0.5 * step)          # output pixel centres = sampled input pixel centres
        return '{' + ', '.join([self.proj, '1.0000', '1.0000', f'{float(e):.10f}', f'{float(n):.10f}', repr(self.dx * step), repr(self.dy * step)] + self.items[7:]) + '}'
def write_envi(path, arr2d, band_name, dtype_code, extra=None):
    arr2d[:, None, :].astype({4: '<f4', 1: 'u1'}[dtype_code]).tofile(path)
    L = ['ENVI', f'description = {{{os.path.basename(path)}}}', f'samples = {arr2d.shape[1]}', f'lines   = {arr2d.shape[0]}', 'bands   = 1', 'header offset = 0',
         'file type = ENVI Standard', f'data type = {dtype_code}', 'interleave = bil', 'byte order = 0', f'map info = {geo.map_info(SPATIAL_STEP)}', 'band names = {' + band_name + '}']
    if geo.csys: L.append('coordinate system string = {' + geo.csys + '}')
    for k, v in (extra or {}).items(): L.append(f'{k} = {v}')
    open(os.path.splitext(path)[0] + '.hdr', 'w').write('\n'.join(L) + '\n')
def write_tif(path, arr2d, nodata):
    try:
        import rasterio
        from rasterio.transform import from_origin
    except ImportError:
        return False
    e0, n0 = geo.to_map(0.5 - 0.5 * SPATIAL_STEP, 0.5 - 0.5 * SPATIAL_STEP)
    with rasterio.open(path, 'w', driver='GTiff', height=arr2d.shape[0], width=arr2d.shape[1], count=1, dtype=str(arr2d.dtype), crs='EPSG:4326',
                       transform=from_origin(float(e0), float(n0), geo.dx * SPATIAL_STEP, geo.dy * SPATIAL_STEP), nodata=nodata) as dst:
        dst.write(arr2d, 1)
    return True
def read_roi_xml(path):
    # ENVI ROI .xml -> {plot number: [polygons in full-res file coordinates]}
    plots = {}
    for i, reg in enumerate(ET.parse(path).getroot().iter('Region')):
        m = re.search(r'(\d+)\D*$', reg.get('name', '')); pno = int(m.group(1)) if m else i + 1; polys = []
        for gd in reg.iter('GeometryDef'):
            cs = (gd.findtext('CoordSysStr') or 'none').strip()
            for poly in gd.iter('Polygon'):
                c = poly.find('.//Exterior//Coordinates')
                if c is None or not (c.text or '').strip(): continue
                v = np.array(c.text.split(), float).reshape(-1, 2)
                fx, fy = (v[:, 0], v[:, 1]) if cs.lower() == 'none' else geo.to_file(v[:, 0], v[:, 1])
                polys.append(np.column_stack([fx, fy]))
        if polys: plots[pno] = polys
    return dict(sorted(plots.items()))
hdr = read_envi_header(HDR_FILE); cube = EnviCube(DATA_FILE, hdr); geo = Geo(hdr)
WL = np.array([float(t) for t in hdr['wavelength'].split(',')])
print(f'image {cube.ns} x {cube.nl} px, {cube.nb} bands ({cube.il}), pixel {geo.px_w * 100:.2f} x {geo.px_h * 100:.2f} cm, {WL[0]:.1f}-{WL[-1]:.1f} nm')""")

add(MD, "## 3 Networks\nConvNeXt V2-Atto (Woo et al., 2023) with stride-1 stems for the 4 × 4 pseudo-image (features written into a k × k grid, zero-padded; Sharma et al., 2019) and DNN-F1 (fully connected network on the feature vector) – the same architectures as in the ASD analysis.")
add(CODE, r"""class LN2d(nn.Module):
    def __init__(s, c): super().__init__(); s.ln = nn.LayerNorm(c)
    def forward(s, x): return s.ln(x.permute(0, 2, 3, 1)).permute(0, 3, 1, 2)
class GRN(nn.Module):
    def __init__(s, c): super().__init__(); s.g = nn.Parameter(torch.zeros(1, 1, 1, c)); s.b = nn.Parameter(torch.zeros(1, 1, 1, c))
    def forward(s, x):
        gx = torch.norm(x, p=2, dim=(1, 2), keepdim=True); nx = gx / (gx.mean(-1, keepdim=True) + 1e-6); return s.g * (x * nx) + s.b + x
class CNBlock(nn.Module):
    def __init__(s, c):
        super().__init__(); s.dw = nn.Conv2d(c, c, 7, padding=3, groups=c); s.ln = nn.LayerNorm(c); s.p1 = nn.Linear(c, 4 * c); s.grn = GRN(4 * c); s.p2 = nn.Linear(4 * c, c)
    def forward(s, x):
        h = s.dw(x).permute(0, 2, 3, 1); h = s.p2(s.grn(Fn.gelu(s.p1(s.ln(h))))); return x + h.permute(0, 3, 1, 2)
class Down(nn.Module):
    def __init__(s, i, o): super().__init__(); s.ln = LN2d(i); s.c = nn.Conv2d(i, o, 2, 2)
    def forward(s, x):
        x = s.ln(x)
        if x.shape[-1] < 2: x = Fn.pad(x, (0, 1, 0, 1))
        return s.c(x)
class ConvNeXtV2Atto(nn.Module):
    def __init__(s, nout, dims=(40, 80, 160, 320), depths=(2, 2, 6, 2), drop=0.03):
        super().__init__(); s.stem = nn.Sequential(nn.Conv2d(1, dims[0], 2, 1), LN2d(dims[0])); S = []
        for i, (d, n) in enumerate(zip(dims, depths)):
            if i > 0: S.append(Down(dims[i - 1], d))
            S += [CNBlock(d) for _ in range(n)]
        s.stages = nn.Sequential(*S); s.norm = nn.LayerNorm(dims[-1]); s.drop = nn.Dropout(drop); s.fc = nn.Linear(dims[-1], nout)
    def forward(s, x): return s.fc(s.drop(s.norm(s.stages(s.stem(x)).mean((2, 3)))))
class DNNF1(nn.Module):
    def __init__(s, p, nout, drop=0.3):
        super().__init__(); s.f = nn.Sequential(nn.Linear(p, 64), nn.BatchNorm1d(64), nn.ReLU(), nn.Dropout(drop), nn.Linear(64, 32), nn.BatchNorm1d(32), nn.ReLU(), nn.Dropout(drop), nn.Linear(32, nout))
    def forward(s, x): return s.f(x.flatten(1))
def pseudo(X):
    p = X.shape[1]; k = max(3, math.ceil(math.sqrt(p))); Z = np.zeros((len(X), k * k), np.float32); Z[:, :p] = X; return Z.reshape(-1, 1, k, k)""")

add(MD, "## 4 Reference spectra, ground truth and model table (embedded)\n`ASD_HEALTHY` = mean of the healthy ASD leaves scored on 24 Feb 2026 at the image wavelengths; `UAV_HEALTHY` = mean of the 12 fungicide-sprayed plots of this image. Their ratio is the wavelength-wise **healthy-reference gain** (empirical-line idea with reference targets; Smith and Milton, 1999); brightness normalisation scales each spectrum to the mean reflectance of the healthy leaves (Barnes et al., 1989). `TRUTH` = ASD leaf scores of 24 Feb per plot. `MODEL_TABLE` = the top models, the input each one uses and its accuracy on the 48 UAV plots. `EXPECTED` = each model's prediction for the 48 plot means (self-check, step 7).")
ref = ("REF_WL = np.array(%s)\nASD_HEALTHY = np.array(%s)\nUAV_HEALTHY = np.array(%s)\n" % (fmt(SC.wavelength, 9), fmt(SC['ASD healthy (24 Feb)']), fmt(SC['UAV healthy']))
       + "TRUTH = pd.DataFrame({'plot': %s, 'block': %s, 'status': %s, 'variety': %s, 'sowing': %s, 'mean_score': %s, 'grade': %s, 'PDI': %s})\n" % (
           list(GT['plot']), list(GT.block), list(GT.status), list(GT.variety), list(GT.sowing), fmt(GT.score.round(4)), list(GT.grade.astype(int)), fmt(GT.PDI.round(3)))
       + "MODEL_TABLE = %s\n" % json.dumps([{k: m[k] for k in ('task', 'model', 'why', 'variant', 'uav_metric', 'uav_value', 'uav_auc', 'file', 'kind')} for m in MT]).replace('null', 'None')
       + "EXPECTED = __EXPECTED__\n")
add(CODE, ref + r"""GRADES = [0, 1, 3, 5, 7, 9]
assert len(REF_WL) == len(WL) and np.abs(REF_WL - WL).max() < 0.01, 'the image wavelengths differ from the 24 Feb image used to build the model inputs'
GAIN = ASD_HEALTHY / UAV_HEALTHY; TARGET_MEAN = ASD_HEALTHY.mean()
MT = {('%s_%s' % (m['task'], m['model'].replace(' ', '_'))): m for m in MODEL_TABLE}
print(pd.DataFrame(MODEL_TABLE)[['task', 'model', 'why', 'variant', 'uav_metric', 'uav_value']].round(3).to_string(index=False))""")

add(MD, "## 5 Features – identical to the ASD pipeline\nFor every pixel: (1) the input variant of the model – *direct*, *corrected* (× healthy-reference gain) or *normalised* (corrected and scaled to the healthy-leaf mean reflectance); (2) resampling to 1 nm, 350–2500 nm (gaps bridged linearly); (3) Savitzky–Golay smoothing and first derivative (window 11, order 2; Savitzky and Golay, 1964); (4) the model inputs: first derivatives FD at given wavelengths, red-edge position REP and amplitude Dr (680–760 nm; Horler et al., 1983; Filella and Peñuelas, 1994), DWSI-2 = R1660/R550 (Apan et al., 2004) and MCARI (Daughtry et al., 2000). Steps 2–3 are linear, so they are combined into one matrix evaluated only at the needed wavelengths: identical values to the ASD code (`wr_features.py`), fast and light on memory.")
add(CODE, r"""FULL = np.arange(350, 2501).astype(float)
_I = np.eye(len(WL)); MI = np.stack([np.interp(FULL, WL, _I[j]) for j in range(len(WL))], 1)   # (2151, bands): identical to np.interp per pixel
C0, C1 = savgol_coeffs(11, 2, deriv=0, use='dot'), savgol_coeffs(11, 2, deriv=1, use='dot')
def _op(w, c):
    v = np.zeros(len(FULL)); i = int(round(w - 350)); v[i - 5:i + 6] = c; return v
def build_operator(names):
    cols, keys = [], []
    def need(key, w, c):
        if key not in keys: cols.append(_op(w, c)); keys.append(key)
    for n in names:
        if n.startswith('FD') and n[2:].isdigit(): need(n, int(n[2:]), C1)
        elif n.startswith('R') and n[1:].isdigit(): need(n, int(n[1:]), C0)
        elif n in ('REP', 'Dr'):
            for w in range(680, 761): need('FD%d' % w, w, C1)
        elif n == 'DWSI-2': need('R1660', 1660, C0); need('R550', 550, C0)
        elif n == 'MCARI': need('R700', 700, C0); need('R670', 670, C0); need('R550', 550, C0)
        else: raise ValueError('feature not implemented: ' + n)
    return MI.T @ np.column_stack(cols), keys
def make_variant(S, v):
    if v == 'direct': return S
    C = S * GAIN
    return C if v == 'corrected' else C * (TARGET_MEAN / C.mean(1, keepdims=True))
def features(S, names, OP):
    M, keys = OP; Y = S.astype(np.float64) @ M; c = {k: j for j, k in enumerate(keys)}; g = lambda k: Y[:, c[k]]; out = []
    for n in names:
        if n in ('REP', 'Dr'):
            red = Y[:, [c['FD%d' % w] for w in range(680, 761)]]
            out.append(680 + red.argmax(1).astype(float) if n == 'REP' else red.max(1) * 1000)
        elif n == 'DWSI-2': out.append(g('R1660') / g('R550'))
        elif n == 'MCARI': out.append(((g('R700') - g('R670')) - 0.2 * (g('R700') - g('R550'))) * (g('R700') / g('R670')))
        else: out.append(g(n))
    return np.column_stack(out)""")

add(MD, "## 6 Load the models\nNetworks: weights loaded safely (`weights_only=True`). ML models: arrays from the `.npz` files, predicted with NumPy exactly as scikit-learn/xgboost do (SVM: radial-basis decision function; RF: average of the tree class proportions; XGBoost: base score + sum of the tree leaves). Inputs are always standardised with the training mean and SD stored with each model.")
add(CODE, r"""class Model:
    def __init__(self, key):
        m = MT[key]; self.key, self.task, self.name, self.variant, self.kind = key, m['task'], m['model'], m['variant'], m['kind']; p = os.path.join(MODEL_DIR, m['file'])
        if self.kind in ('convnext', 'dnn'):
            W = torch.load(p, map_location='cpu', weights_only=True); self.features = W['features']; self.mu, self.sd = np.array(W['scaler_mean']), np.array(W['scaler_sd'])
            self.net = (ConvNeXtV2Atto(W['n_out']) if self.kind == 'convnext' else DNNF1(len(self.features), W['n_out'])); self.net.load_state_dict(W['state_dict']); self.net.eval().to(DEVICE)
        else:
            z = np.load(p, allow_pickle=False); self.z = {k: z[k] for k in z.files}; self.features = [str(f) for f in self.z['features']]; self.mu, self.sd = self.z['mu'], self.z['sd']
        self.op = build_operator(self.features)
    def _trees(self, Z, left, right, feat, thr, off, le=True):
        # route every sample through every tree; returns the leaf index (global) per tree
        Z = Z.astype(np.float32); n = len(Z); rows = np.arange(n); out = []
        ends = list(off[1:]) + [len(feat)]
        for o, e in zip(off, ends):
            node = np.zeros(n, int)
            while True:
                g = o + node; lf = left[g] < 0 if le else self.z['isleaf'][g]
                if lf.all(): break
                go = Z[rows, np.maximum(feat[g], 0)] <= thr[g] if le else Z[rows, feat[g]] < thr[g]
                node = np.where(lf, node, np.where(go, left[g], right[g]))
            out.append(o + node)
        return out
    def predict(self, S):
        # spectra (pixels x bands, reflectance 0-1) -> dict(value=..., label=...)
        F = features(make_variant(S, self.variant), self.features, self.op); Z = (F - self.mu) / self.sd
        if self.kind in ('convnext', 'dnn'):
            Z = Z.astype(np.float32); outs = []
            with torch.no_grad():
                for i in range(0, len(Z), BATCH):
                    zb = Z[i:i + BATCH]; x = torch.from_numpy(pseudo(zb) if self.kind == 'convnext' else zb.reshape(-1, 1, 1, zb.shape[1])).to(DEVICE)
                    outs.append(self.net(x).cpu().numpy())
            o = np.concatenate(outs)
            if self.task == 'A': p = np.exp(o - o.max(1, keepdims=True)); p /= p.sum(1, keepdims=True); return dict(value=p[:, 1], label=(p[:, 1] >= THRESHOLD).astype(int))
            if self.task == 'B': g = np.array(GRADES)[o.argmax(1)]; return dict(value=g.astype(float), label=g)
            v = np.clip(o.ravel(), 0, 9); return dict(value=v, label=v)
        z = self.z
        if self.kind == 'svm':
            out = np.empty(len(Z))
            for i in range(0, len(Z), 4096):
                d2 = ((Z[i:i + 4096, None, :] - z['sv'][None]) ** 2).sum(2); out[i:i + 4096] = np.exp(-z['gamma'][0] * d2) @ z['dual'] + z['b0'][0]
            lab = np.where(out > 0, z['classes'][1], z['classes'][0]); return dict(value=out, label=lab.astype(int))
        if self.kind == 'rf':
            leaves = self._trees(Z, z['left'], z['right'], z['feat'], z['thr'], z['offset'])
            P = sum(z['value'][l] for l in leaves) / len(leaves); g = np.array(GRADES)[z['classes'][P.argmax(1)].astype(int)]; return dict(value=g.astype(float), label=g)
        leaves = self._trees(Z, z['yes'], z['no'], z['feat'], z['thr'], z['offset'], le=False)
        v = np.clip(z['base'][0] + sum(z['leaf'][l] for l in leaves), 0, 9); return dict(value=v, label=v)
torch.set_num_threads(max(1, os.cpu_count() or 1))
MODELS = [Model(k) for k in MODELS_TO_RUN]
for m in MODELS: print(f'{m.key:22s} task {m.task}  input {m.variant:10s}  features: {", ".join(m.features)}')""")

add(MD, "## 7 Self-check on the 48 plot-mean spectra\nWith the ENVI plot-average file, every model predicts the 48 plot means; the result is compared with the values computed when this notebook was built (`EXPECTED`). Differences below 0.001 mean your libraries reproduce the analysis exactly.")
add(CODE, r"""if PLOT_AVG_FILE and os.path.exists(PLOT_AVG_FILE):
    L = open(PLOT_AVG_FILE).read().splitlines(); nh = sum(l.startswith('Column') for l in L)
    A = np.array([[float(x) for x in l.split()] for l in L[nh + 1:] if l.strip()])
    assert np.abs(A[:, 0] - WL).max() < 0.01, 'plot-average wavelengths differ from the image'
    for m in MODELS:
        d = np.abs(m.predict(A[:, 1:].T.astype(np.float32))['value'] - np.array(EXPECTED[m.key])).max()
        print(f'{m.key:22s} max difference {d:.2e}', '-> OK' if d < 1e-3 else '-> CHECK library versions')
else:
    print('self-check skipped (no plot-average file)')""")

add(MD, "## 8 Open the image and build the crop mask\nPixels outside the field are 0 in the masked image. A pixel is used when its reflectance is valid and NDVI = (R898 − R684)/(R898 + R684) > `NDVI_MIN`. Reflectance is rescaled automatically if stored as 0–10000.")
add(CODE, r"""ST = SPATIAL_STEP; NS, NL = len(range(0, cube.ns, ST)), len(range(0, cube.nl, ST))
bi = lambda w: int(np.argmin(np.abs(WL - w)))
sample = cube.rows(0, cube.nl, max(ST, cube.nl // 200))[:, ::max(1, cube.ns // 400), bi(800)]
v = sample[np.isfinite(sample) & (sample > 0)]
SCALE = (1e4 if np.percentile(v, 95) > 2 else 1.0) if REFLECTANCE_SCALE == 'auto' else float(REFLECTANCE_SCALE)
print(f'processing grid {NS} x {NL} (SPATIAL_STEP={ST}); reflectance divided by {SCALE:g}')""")

add(MD, "## 9 Pixel loop – all selected models in one pass\nEach block of `BLOCK_ROWS` rows is read once; every model computes its own input variant, features and prediction. Rasters: detection = probability (SVM: decision value) and class; grades = grade 0–9; score = score 0–9 (NaN outside the crop).")
add(CODE, r"""VAL = {m.key: np.full((NL, NS), np.nan, np.float32) for m in MODELS}; LAB = {m.key: np.full((NL, NS), np.nan, np.float32) for m in MODELS}
CROP = np.zeros((NL, NS), bool); t0 = time.time(); n_crop = 0
for r0 in range(0, cube.nl, BLOCK_ROWS * ST):
    r1 = min(cube.nl, r0 + BLOCK_ROWS * ST); blk = cube.rows(r0, r1, ST) / SCALE
    nd = (blk[..., bi(898)] - blk[..., bi(684)]) / (blk[..., bi(898)] + blk[..., bi(684)] + 1e-12)
    valid = np.isfinite(blk).all(2) & (blk[..., bi(800)] > 0) & (blk.mean(2) > 0) & (nd > NDVI_MIN)
    i0 = r0 // ST; nr = blk.shape[0]
    if valid.any():
        S = blk[valid]; CROP[i0:i0 + nr][valid] = True; n_crop += len(S)
        for m in MODELS:
            out = m.predict(S); VAL[m.key][i0:i0 + nr][valid] = out['value']; LAB[m.key][i0:i0 + nr][valid] = out['label']
    if (r0 // (BLOCK_ROWS * ST)) % 20 == 0 or r1 == cube.nl:
        el = time.time() - t0; print(f'rows {r1}/{cube.nl}  crop pixels {n_crop:,}  {el / 60:.1f} min  ETA {el / r1 * (cube.nl - r1) / 60:.1f} min')
for m in MODELS:
    base = os.path.join(OUT, m.key)
    if m.task == 'A':
        cls = np.zeros((NL, NS), np.uint8); cls[CROP] = 1; cls[(LAB[m.key] == 1) & CROP] = 2
        write_envi(base + '_score.dat', VAL[m.key], 'probability of white rust' if m.kind != 'svm' else 'SVM decision value', 4, {'data ignore value': 'NaN'})
        write_envi(base + '_class.dat', cls, 'class (0 outside, 1 healthy, 2 diseased)', 1, {'file type': 'ENVI Classification', 'classes': 3, 'class names': '{outside, healthy, diseased}', 'class lookup': '{0 0 0, 26 152 80, 215 48 39}'})
        write_tif(base + '_class.tif', cls, 0); write_tif(base + '_score.tif', VAL[m.key], np.nan)
    else:
        write_envi(base + '.dat', VAL[m.key], 'grade (0-9)' if m.task == 'B' else 'severity score (0-9)', 4, {'data ignore value': 'NaN'}); write_tif(base + '.tif', VAL[m.key], np.nan)
print(f'done: {n_crop:,} crop pixels, {len(MODELS)} maps, {(time.time() - t0) / 60:.1f} min')""")

add(MD, "## 10 Maps\nOne figure per model, plus an overview of all selected models. Plot outlines and numbers are drawn when the ROI file is given. Titles carry the model's accuracy on the 48 UAV plots so that unreliable maps are recognised at once.")
add(CODE, r"""PLOTS = read_roi_xml(ROI_FILE) if ROI_FILE and os.path.exists(ROI_FILE) else {}
def outline(ax, numbers=True):
    for p, polys in PLOTS.items():
        for pg in polys: ax.plot((pg[:, 0] - 0.5) / ST, (pg[:, 1] - 0.5) / ST, color='k', lw=0.4)
        if numbers: c = (np.vstack(polys).mean(0) - 0.5) / ST; ax.text(c[0], c[1], str(p), fontsize=5, ha='center', va='center')
GCM = ListedColormap(['#1A9850', '#FEE08B', '#FDAE61', '#F46D43', '#D73027', '#7F0000']); GNORM = BoundaryNorm([-0.5, 0.5, 2, 4, 6, 8, 9.5], 6)
def draw_map(ax, m, numbers=True):
    acc = MT[m.key]; tag = f"UAV {acc['uav_metric'].replace('macro_F1', 'macro-F1').replace('R2', 'R²')} {acc['uav_value']:.2f}"
    if m.task == 'A':
        if m.kind == 'svm': im = ax.imshow(VAL[m.key], cmap='RdYlGn_r', vmin=-2, vmax=2, interpolation='nearest'); lab = 'SVM decision value'
        else: im = ax.imshow(VAL[m.key], cmap='RdYlGn_r', vmin=0, vmax=1, interpolation='nearest'); lab = 'probability of white rust'
        ttl = f'{m.name} detection ({m.variant} input; {tag})'
    elif m.task == 'B': im = ax.imshow(VAL[m.key], cmap=GCM, norm=GNORM, interpolation='nearest'); lab = 'grade'; ttl = f'{m.name} six grades ({m.variant}; {tag}; NOT validated)'
    else: im = ax.imshow(VAL[m.key], cmap='YlOrRd', vmin=0, vmax=9, interpolation='nearest'); lab = 'score (0-9)'; ttl = f'{m.name} severity score ({m.variant}; {tag}; NOT validated)'
    outline(ax, numbers); ax.set_xticks([]); ax.set_yticks([]); ax.set_title(ttl, fontsize=9); plt.colorbar(im, ax=ax, fraction=0.03, label=lab)
for m in MODELS:
    fig, axs = plt.subplots(1, 2 if m.task == 'A' else 1, figsize=(16 if m.task == 'A' else 9, 8 * NL / NS + 1), squeeze=False); axs = axs.ravel()
    draw_map(axs[0], m)
    if m.task == 'A':
        cls = np.where(CROP, 1 + (LAB[m.key] == 1), np.nan)
        axs[1].imshow(cls, cmap=ListedColormap(['#1A9850', '#D73027']), vmin=1, vmax=2, interpolation='nearest'); outline(axs[1]); axs[1].set_xticks([]); axs[1].set_yticks([])
        axs[1].set_title('class map (red = diseased)', fontsize=9)
        axs[1].legend(handles=[matplotlib.patches.Patch(color='#1A9850', label='healthy'), matplotlib.patches.Patch(color='#D73027', label='diseased')], loc='lower right', fontsize=8)
    fig.tight_layout(); fp = os.path.join(OUT, m.key + '_map.png'); fig.savefig(fp, dpi=300); plt.close(fig); show(fp)
n = len(MODELS); cols = 2; rows = math.ceil(n / cols)
fig, axs = plt.subplots(rows, cols, figsize=(16, rows * (8 * NL / NS + 0.8)), squeeze=False)
for ax, m in zip(axs.ravel(), MODELS): draw_map(ax, m, numbers=False)
for ax in axs.ravel()[n:]: ax.axis('off')
fig.tight_layout(); fp = os.path.join(OUT, 'all_models_overview.png'); fig.savefig(fp, dpi=200); plt.close(fig); show(fp)""")

add(MD, "## 11 Per-plot accuracy of every map\nFor each plot ROI: number of crop pixels and the plot value of the map (detection: share of diseased pixels; grades: median predicted grade; score: mean predicted score), compared with the ASD leaf scores of 24 Feb: detection – plot diseased if more than `PLOT_DISEASED_SHARE` of its pixels are diseased (confusion counts, sensitivity, specificity; Congalton, 1991); grades – share of plots within one grade; score – R², RMSE and Pearson r with the plot mean leaf score.")
add(CODE, r"""SUMMARY = []
if PLOTS:
    yy, xx = np.mgrid[0:NL, 0:NS]; cx, cy = xx * ST + 0.5, yy * ST + 0.5
    MASK = {}
    for p, polys in PLOTS.items():
        mk = np.zeros((NL, NS), bool)
        for pg in polys:
            sel = (cx >= pg[:, 0].min()) & (cx <= pg[:, 0].max()) & (cy >= pg[:, 1].min()) & (cy <= pg[:, 1].max())
            if sel.any(): mk[sel] |= MplPath(pg).contains_points(np.column_stack([cx[sel], cy[sel]]))
        MASK[p] = mk & CROP
    for m in MODELS:
        rows = []
        for p, mk in MASK.items():
            v, l = VAL[m.key][mk], LAB[m.key][mk]
            r = dict(plot=p, crop_pixels=int(mk.sum()))
            if m.task == 'A': r.update(share_diseased=float((l == 1).mean()) if len(l) else np.nan, mean_value=float(np.nanmean(v)) if len(v) else np.nan)
            elif m.task == 'B': r.update(median_grade=float(np.median(v)) if len(v) else np.nan, mean_grade=float(np.nanmean(v)) if len(v) else np.nan)
            else: r.update(mean_score_pred=float(np.nanmean(v)) if len(v) else np.nan)
            rows.append(r)
        PS = pd.DataFrame(rows).merge(TRUTH, on='plot', how='left'); s = dict(model=m.key, task=m.task, input=m.variant, plots=len(PS))
        if m.task == 'A':
            PS['mapped_diseased'] = (PS.share_diseased > PLOT_DISEASED_SHARE).astype(int); t = (PS.status == 'Diseased').astype(int)
            tp, tn, fp, fn = int(((t == 1) & (PS.mapped_diseased == 1)).sum()), int(((t == 0) & (PS.mapped_diseased == 0)).sum()), int(((t == 0) & (PS.mapped_diseased == 1)).sum()), int(((t == 1) & (PS.mapped_diseased == 0)).sum())
            sens, spec = tp / max(1, tp + fn), tn / max(1, tn + fp)
            s.update(TP=tp, TN=tn, FP=fp, FN=fn, overall_accuracy=(tp + tn) / len(PS), sensitivity=sens, specificity=spec, balanced_accuracy=(sens + spec) / 2,
                     r_with_score=PS[['share_diseased', 'mean_score']].corr().iloc[0, 1])
        elif m.task == 'B':
            gp = [GRADES.index(min(GRADES, key=lambda g: abs(g - x))) for x in PS.median_grade]; gt = [GRADES.index(int(x)) for x in PS.grade]
            s.update(exact=float(np.mean(np.array(gp) == np.array(gt))), within_one=float(np.mean(np.abs(np.array(gp) - np.array(gt)) <= 1)), r_with_score=PS[['mean_grade', 'mean_score']].corr().iloc[0, 1])
        else:
            e = PS.mean_score_pred - PS.mean_score
            s.update(R2=1 - (e ** 2).sum() / ((PS.mean_score - PS.mean_score.mean()) ** 2).sum(), RMSE=float(np.sqrt((e ** 2).mean())), r_with_score=PS[['mean_score_pred', 'mean_score']].corr().iloc[0, 1])
        PS.to_csv(os.path.join(OUT, m.key + '_per_plot.csv'), index=False); SUMMARY.append(s)
    SUMMARY = pd.DataFrame(SUMMARY); SUMMARY.to_csv(os.path.join(OUT, 'per_plot_accuracy_all_models.csv'), index=False)
    print(SUMMARY.round(3).to_string(index=False))
else:
    print('per-plot accuracy skipped (no ROI file)')""")

add(MD, "## 12 Summary and outputs\nIn the results folder, for each model `<task>_<model>`: rasters (`_score`/`_class` for detection, one raster for grades and score; ENVI `.dat/.hdr`, GeoTIFF if `rasterio` is installed), a PNG map, a per-plot CSV; plus `all_models_overview.png`, `per_plot_accuracy_all_models.csv` and `run_info.json`.\n\n**Reading the maps.** The recommended map is the ConvNeXt V2-Atto detection map (red = diseased). The other detection maps show what the best leaf models predict (at chance on the plots); the grade and score maps are **not validated** and must not be used as severity. Flowers, stems and leaf edges can be misclassified because all models were trained on single leaves. Confirm the map on the next flight and train UAV models on UAV data (transfer report).\n\n**References.** Apan et al. (2004); Barnes et al. (1989); Congalton (1991); Daughtry et al. (2000); Filella and Peñuelas (1994); Horler et al. (1983); Savitzky and Golay (1964); Sharma et al. (2019); Smith and Milton (1999); Westfall and Young (1993); Woo et al. (2023) – full entries in the transfer report.")
add(CODE, r"""info = dict(image=DATA_FILE, spatial_step=ST, grid=[NS, NL], crop_pixels=int(n_crop), models=[dict(key=m.key, task=m.task, input=m.variant, features=m.features) for m in MODELS],
            threshold=THRESHOLD, ndvi_min=NDVI_MIN, reflectance_scale=SCALE, minutes=round((time.time() - t0) / 60, 1))
json.dump(info, open(os.path.join(OUT, 'run_info.json'), 'w'), indent=1)
print('results in', OUT); print('\n'.join(sorted(os.listdir(OUT))))""")

def build(expected):
    nb = dict(nbformat=4, nbformat_minor=5, metadata=dict(kernelspec=dict(display_name='Python 3', language='python', name='python3'), language_info=dict(name='python')), cells=[])
    for i, (k, t) in enumerate(cells):
        t = t.replace('__EXPECTED__', expected)
        c = dict(cell_type=k, id='c%02d' % i, metadata={}, source=[l + '\n' for l in t.split('\n')]); c['source'][-1] = c['source'][-1].rstrip('\n')
        if k == CODE: c.update(execution_count=None, outputs=[])
        nb['cells'].append(c)
    return nb
if __name__ == '__main__':
    exp = open(sys.argv[1]).read() if len(sys.argv) > 1 else '{}'
    json.dump(build(exp), open(HERE + 'kit/White_rust_pixel_map_24Feb2026.ipynb', 'w'), indent=1); print('notebook written', len(cells), 'cells')
