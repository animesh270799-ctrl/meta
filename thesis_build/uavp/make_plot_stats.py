"""Plot-level evaluation of pixel maps (any number of models) against the plot Disease Index (DI) of the 48 plots.
Builds (1) the Jupyter notebook Plot_level_evaluation_48_plots_24Feb2026.ipynb that reads the model maps written by the per-model
notebooks, counts the pixel classes inside each plot ROI, computes plot DI = sum(x*f)/(n*sum f)*100 from the pixel classes, and
evaluates every model (healthy/diseased, DI, severity class) with bootstrap CIs, McNemar and Wilcoxon tests, figures and an Excel
workbook with live formulas; (2) the blank Excel workbook (same layout) for models entered by hand.
Output: uavp/kit/per_model/Plot_level_evaluation_48_plots_24Feb2026.ipynb and uavp/kit/per_model/Plot_level_evaluation_TEMPLATE.xlsx"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'; PM = HERE + 'kit/per_model/'
GT = json.load(open(HERE + 'plotstats_gt.json'))
P = 'C:\\Users\\BDI LAB\\Desktop\\ASD_MODEL_ON_240226_UAV_IMAGE_PIXELWISE'

TITLE = """# Plot-level evaluation of the pixel maps – 48 plots, UAV image of 24 February 2026
For every model map, the pixel classes inside each of the 48 plot ROIs are counted and turned into plot values, which are compared with the plot Disease Index (DI) of the ground truth (leaf ratings, `26_02_26_Plot_DI.xlsx`).

| Model type | Pixel class | Plot value from the pixel classes | Compared with |
|---|---|---|---|
| detection (healthy / diseased) | healthy or diseased | share of diseased pixels (%); plot diseased if share > 50% | plot status (DI > 0) |
| grade (0, 1, 3, 5, 7, 9) | grade of the pixel | **DI = Σ(x·f) / (n·Σf) × 100**, x = pixel grade, f = number of pixels at grade x, n = 9; DI class (Healthy … Very high) | plot DI, plot DI class and status |
| score (0–9, continuous) | score put in the nearest grade (<0.5 → 0, 0.5–2 → 1, 2–4 → 3, 4–6 → 5, 6–8 → 7, ≥8 → 9) | as for grade | as for grade |

**Statistics.** Healthy/diseased (all models): confusion counts, overall accuracy, sensitivity, specificity, balanced accuracy, Cohen's kappa, AUC. DI (grade and score models): R², RMSE, MAE, bias, Pearson r, Spearman ρ, Lin's concordance (CCC), and r / ρ / RMSE on the 36 diseased plots only. DI class: exact agreement, within one class, quadratic weighted kappa. Uncertainty: 95% bootstrap intervals (plots resampled within healthy / diseased). Model comparison: McNemar exact test (plot status), Wilcoxon signed-rank test (absolute DI error).

**Other models.** Add one line per model map to `MODELS` in step 1 (any detection, grade or score map written by the per-model notebooks). Models you evaluate elsewhere can be typed or pasted into the blank sheets of the Excel file: the formulas compute everything.

**Outputs** (folder `PLOT_STATISTICS`): `Plot_level_evaluation_48_plots_24Feb2026.xlsx` (formulas; opens in Excel), figures (PNG) and CSV tables.

**Steps.** 0 install · 1 settings · 2 libraries, image geometry and plot masks · 3 ground truth · 4 pixel classes in each plot · 5 statistics · 6 uncertainty and model comparison · 7 figures · 8 Excel workbook · 9 outputs.
**Before running:** run the model notebooks (detection, grade, score) – ideally all with the same `SPATIAL_STEP` (1 = full resolution for the final numbers)."""

C0 = "%pip install -q numpy scipy pandas matplotlib openpyxl pillow"

C1 = f"""# ============================ SETTINGS ============================
HDR_FILE = r'D:\\Coalighned\\24_02_2026\\subset_200526.hdr'      # header of the 24 Feb image (only the header is read: plot positions)
ROI_FILE = r'D:\\Coalighned\\24_02_2026\\48_plot_roi_new.xml'    # 48 plot ROIs, ROI #n = plot n
IMG_DIR  = r'{P}\\IMAGE_VALIDATED'   # folder that holds the model maps
OUT_DIR  = IMG_DIR + r'\\PLOT_STATISTICS'                        # results of this notebook
GT_FILE  = r'{P}\\26_02_26_Plot_DI.xlsx'   # optional: your plot DI workbook (the same leaf counts are embedded in step 3)

# one line per model map; type = 'detection' (healthy / diseased), 'grade' (0, 1, 3, 5, 7, 9) or 'score' (continuous 0-9)
MODELS = [
    dict(name='RF detection',      type='detection', file=IMG_DIR + r'\\A_detection_RF\\A_detection_RF_class.dat'),
    dict(name='RF six grades',     type='grade',     file=IMG_DIR + r'\\GRADE_RF\\B_six_grades_RF_grade.dat'),
    dict(name='RF severity score', type='score',     file=IMG_DIR + r'\\SCORE_RF\\C_severity_score_RF_score.dat'),
    # add other models in the same way, for example:
    # dict(name='SVM detection',    type='detection', file=IMG_DIR + r'\\A_SVM\\A_SVM_class.dat'),
    # dict(name='ConvNeXt grades',  type='grade',     file=IMG_DIR + r'\\B_ConvNeXt_V2-Atto\\B_ConvNeXt_V2-Atto.dat'),
    # dict(name='XGBoost score',    type='score',     file=IMG_DIR + r'\\C_XGBoost\\C_XGBoost.dat'),
]
PLOT_DISEASED_SHARE = 0.5   # a plot is called diseased when more than this share of its crop pixels is diseased (pixel grade > 0)
DET_THRESHOLD = 0.5         # only for detection maps given as probabilities: a pixel is diseased if its probability > this
N_BOOT, SEED  = 2000, 2026  # bootstrap resamples of the 48 plots (95% intervals) and random seed
BLANK_SHEETS  = 2           # extra empty model sheets in the Excel file, for models you enter by hand
XLSX_NAME = 'Plot_level_evaluation_48_plots_24Feb2026.xlsx'"""

C2 = r"""import os, re, json, math, warnings
import xml.etree.ElementTree as ET
import numpy as np, pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.path import Path as MplPath
from matplotlib.colors import ListedColormap
from scipy import stats
warnings.filterwarnings('ignore', category=RuntimeWarning)
try:
    from IPython.display import Image as _Img, display as _display
    def show(path, width=900): _display(_Img(path, width=width))
except Exception:
    def show(path, width=900): print('saved', path)
os.makedirs(OUT_DIR, exist_ok=True)
GRADES = [0, 1, 3, 5, 7, 9]; EDGES = [0.5, 2, 4, 6, 8]          # continuous score -> nearest grade
ENVI_DTYPES = {1: np.uint8, 2: np.int16, 3: np.int32, 4: np.float32, 5: np.float64, 12: np.uint16, 13: np.uint32, 14: np.int64, 15: np.uint64}
def read_envi_header(path):
    txt = open(path, encoding='latin-1').read(); hdr = {}
    for m in re.finditer(r'^\s*([^=\n{}]+?)\s*=\s*(\{[^}]*\}|[^\n]*)', txt, re.M):
        v = m.group(2).strip(); hdr[m.group(1).strip().lower()] = v[1:-1].strip() if v.startswith('{') else v
    return hdr
def read_raster(dat):
    # one-band ENVI raster written by the model notebooks -> 2-D array
    hdr = read_envi_header(os.path.splitext(dat)[0] + '.hdr'); ns, nl = int(hdr['samples']), int(hdr['lines'])
    dt = np.dtype(ENVI_DTYPES[int(hdr['data type'])])
    if int(hdr.get('byte order', '0')) == 1: dt = dt.newbyteorder('>')
    with open(dat, 'rb') as fh:
        fh.seek(int(hdr.get('header offset', '0'))); a = np.fromfile(fh, dtype=dt, count=ns * nl)
    return a.reshape(nl, ns)
class Geo:
    def __init__(self, hdr):
        mi = [s.strip() for s in hdr['map info'].split(',')]; self.refx, self.refy, self.e0, self.n0, self.dx, self.dy = map(float, mi[1:7])
    def to_file(self, x, y):
        x, y = np.asarray(x, float), np.asarray(y, float); return (x - self.e0) / self.dx + (self.refx - 1), (self.n0 - y) / self.dy + (self.refy - 1)
def read_roi_xml(path):
    # ENVI ROI .xml -> {plot number: [polygons in full-resolution file coordinates]}
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
hdr0 = read_envi_header(HDR_FILE); geo = Geo(hdr0); NS0, NL0 = int(hdr0['samples']), int(hdr0['lines'])
PLOTS = read_roi_xml(ROI_FILE); assert sorted(PLOTS) == list(range(1, 49)), 'the ROI file must hold the 48 plots (ROI #n = plot n)'
def grid_step(ns, nl):
    # SPATIAL_STEP used for a map: its size is ceil(image size / step)
    for s in range(1, 129):
        if -(-NS0 // s) == ns and -(-NL0 // s) == nl: return s
    raise ValueError(f'map size {ns} x {nl} does not fit the image {NS0} x {NL0}')
_MASKS = {}
def plot_masks(ST, NL, NS):
    # pixels of every plot on a map grid made with SPATIAL_STEP = ST (pixel centres inside the plot polygon)
    if ST not in _MASKS:
        yy, xx = np.mgrid[0:NL, 0:NS]; cx, cy = xx * ST + 0.5, yy * ST + 0.5; M = {}
        for p, polys in PLOTS.items():
            mk = np.zeros((NL, NS), bool)
            for pg in polys:
                sel = (cx >= pg[:, 0].min()) & (cx <= pg[:, 0].max()) & (cy >= pg[:, 1].min()) & (cy <= pg[:, 1].max())
                if sel.any(): mk[sel] |= MplPath(pg).contains_points(np.column_stack([cx[sel], cy[sel]]))
            M[p] = np.flatnonzero(mk)                                    # pixel positions of the plot (saves memory)
        _MASKS[ST] = M
    return _MASKS[ST]
print(f'image {NS0} x {NL0} px; {len(PLOTS)} plot ROIs read; results to {OUT_DIR}')"""

C3 = ("# leaf counts f at rating x = 0, 1, 3, 5, 7, 9 for plots 1-48 (sheet Plot_DI of 26_02_26_Plot_DI.xlsx)\n"
      "F_LEAF = %s\n" % json.dumps(GT['counts']) +
      "INFO = dict(block=%s,\n            variety=%s,\n            sowing=%s)\n" % (json.dumps(GT['block']), json.dumps(GT['variety']), json.dumps(GT['sowing'])) +
      r"""N_MAX = 9                                   # n = highest rating
DI_LIMITS = [0, 5, 10, 25, 50]              # upper DI limit of Healthy, Very low, Low, Moderate, High (above 50 = Very high)
CLASS_NAMES = ['Healthy', 'Very low', 'Low', 'Moderate', 'High', 'Very high']
if GT_FILE and os.path.isfile(GT_FILE):     # optional: read the leaf counts from your workbook instead of the embedded ones
    try:
        raw = pd.read_excel(GT_FILE, sheet_name='Plot_DI', header=None)
        rows = raw[pd.to_numeric(raw[0], errors='coerce').between(1, 48)]
        if len(rows) >= 48: F_LEAF = rows.iloc[:48, 1:7].astype(float).astype(int).values.tolist(); print('leaf counts read from', GT_FILE)
    except Exception as e:
        print('GT_FILE could not be read (' + type(e).__name__ + '); the embedded leaf counts are used')
def di_from_counts(F):
    # DI = sum(x * f) / (n * sum f) * 100
    F = np.asarray(F, float); n = F.sum(1); return np.where(n > 0, (F * np.array(GRADES)).sum(1) / (N_MAX * np.where(n > 0, n, 1)) * 100, np.nan)
def di_class(di):
    # class index 0-5: DI = 0 Healthy; 0 < DI <= 5 Very low; <= 10 Low; <= 25 Moderate; <= 50 High; > 50 Very high
    di = np.asarray(di, float); return np.where(np.isnan(di), -1, np.where(di <= DI_LIMITS[0], 0, np.searchsorted(DI_LIMITS[1:], di, side='left') + 1)).astype(int)
GT = pd.DataFrame({'plot': range(1, 49), 'block': INFO['block'], 'variety': INFO['variety'], 'sowing': INFO['sowing']})
for k, g in enumerate(GRADES): GT[f'f{g}'] = np.array(F_LEAF)[:, k]
GT['leaves'] = np.array(F_LEAF).sum(1); GT['DI'] = di_from_counts(F_LEAF); GT['class_idx'] = di_class(GT.DI)
GT['class'] = [CLASS_NAMES[i] for i in GT.class_idx]; GT['status'] = (GT.DI > 0).astype(int); GT['mean_leaf_score'] = GT.DI * N_MAX / 100
print('ground truth: ' + ', '.join(f'{c} {n}' for c, n in GT['class'].value_counts().reindex(CLASS_NAMES).dropna().astype(int).items()))
print(GT[['plot', 'block', 'leaves', 'DI', 'class', 'status']].head(14).round(2).to_string(index=False))""")

C4 = r"""def find_file(f):
    if os.path.isfile(f): return f
    for root, _, files in os.walk(IMG_DIR):
        if os.path.basename(f) in files: return os.path.join(root, os.path.basename(f))
    return None
def pixel_classes(typ, a):
    # map values -> (crop pixel?, pixel class): detection 0 healthy / 1 diseased; grade and score -> grade 0, 1, 3, 5, 7, 9
    if typ == 'detection':
        if a.dtype == np.uint8: return a > 0, (a == 2).astype(int)                  # class map: 0 outside, 1 healthy, 2 diseased
        ok = np.isfinite(a); return ok, (np.where(ok, a, 0) > DET_THRESHOLD).astype(int)  # probability map
    if a.dtype == np.uint8:                                                          # class map: 1-6 = grade 0, 1, 3, 5, 7, 9
        ok = (a >= 1) & (a <= 6); return ok, np.array(GRADES)[np.clip(a.astype(int) - 1, 0, 5)]
    ok = np.isfinite(a); return ok, np.array(GRADES)[np.digitize(np.where(ok, a, 0), EDGES)]
MD = []
for m in MODELS:
    f = find_file(m['file'])
    if f is None:
        print(f"!! {m['name']}: map not found ({m['file']}) – skipped; run that model's notebook first"); continue
    a = read_raster(f); NL, NS = a.shape; ST = grid_step(NS, NL); masks = plot_masks(ST, NL, NS); ok, cls = pixel_classes(m['type'], a)
    val = None                                                                       # mean pixel value: probability (detection) or score / grade
    if m['type'] == 'detection':
        fs = f.replace('_class.dat', '_score.dat')
        if fs != f and os.path.isfile(fs): val = read_raster(fs).astype(float)
        elif a.dtype != np.uint8: val = a.astype(float)
    else:
        val = a.astype(float) if a.dtype != np.uint8 else cls.astype(float)
    levels = [0, 1] if m['type'] == 'detection' else GRADES
    C = np.zeros((48, len(levels)), int); MV = np.full(48, np.nan)
    for j in range(48):
        ix = masks[j + 1]; ix = ix[ok.ravel()[ix]]; cj = cls.ravel()[ix]; C[j] = [int((cj == g).sum()) for g in levels]
        if val is not None and len(ix): MV[j] = float(np.nanmean(val.ravel()[ix]))
    MD.append(dict(m, file=f, step=ST, counts=C, mean_value=MV))
    print(f"{m['name']:<22} {m['type']:<9} map {NS} x {NL} (SPATIAL_STEP {ST}); crop pixels in the 48 plots {C.sum():,}; plots without pixels: {int((C.sum(1) == 0).sum())}")
if len({d['step'] for d in MD}) > 1:
    print('NOTE: the maps were made with different SPATIAL_STEP values – run all model notebooks with the same step for a fair comparison.')
def plot_table(d):
    # per-plot table of one model: pixel counts, share of diseased pixels, DI from the pixel classes, class and status
    C = d['counts']; n = C.sum(1).astype(float); nz = np.where(n > 0, n, 1)
    T = GT[['plot', 'DI', 'class_idx', 'class', 'status']].rename(columns={'DI': 'obs_DI', 'class_idx': 'obs_class_idx', 'class': 'obs_class', 'status': 'obs_status'})
    if d['type'] == 'detection':
        T['px_healthy'], T['px_diseased'] = C[:, 0], C[:, 1]; share = np.where(n > 0, C[:, 1] / nz * 100, np.nan)
    else:
        for k, g in enumerate(GRADES): T[f'px_grade{g}'] = C[:, k]
        share = np.where(n > 0, (n - C[:, 0]) / nz * 100, np.nan)
    T['pixels'] = n.astype(int); T['share_diseased_pct'] = share
    if d['type'] != 'detection':
        T['pred_DI'] = di_from_counts(C); T['pred_class_idx'] = di_class(T.pred_DI); T['pred_class'] = [CLASS_NAMES[i] if i >= 0 else '' for i in T.pred_class_idx]
    T['pred_status'] = np.where(n > 0, (share / 100 > PLOT_DISEASED_SHARE).astype(int), -1)
    T['correct'] = np.where(n > 0, (T.pred_status == T.obs_status).astype(int), -1)
    T['plot_value'] = T['pred_DI'] if d['type'] != 'detection' else share          # used for AUC and correlations
    T['mean_pixel_value'] = d['mean_value']
    return T
TABLES = {d['name']: plot_table(d) for d in MD}
for d in MD: TABLES[d['name']].to_csv(os.path.join(OUT_DIR, 'per_plot_' + re.sub(r'\W+', '_', d['name']) + '.csv'), index=False)
for name, T in TABLES.items():
    print('\n' + name); print(T.drop(columns=[c for c in T if c.startswith('px_')]).head(14).round(2).to_string(index=False)); print('...')"""

C5 = r"""def avg_rank(x): return pd.Series(np.asarray(x, float)).rank(method='average').values
def pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3 or x.std() == 0 or y.std() == 0: return np.nan
    return float(np.corrcoef(x, y)[0, 1])
def qwk(a, b, K=6):
    # quadratic weighted kappa over the 6 DI classes (Cohen, 1968)
    O = np.zeros((K, K))
    for i, j in zip(a, b): O[i, j] += 1
    E = np.outer(O.sum(1), O.sum(0)) / O.sum(); W = np.subtract.outer(np.arange(K), np.arange(K)) ** 2 / (K - 1) ** 2
    den = (W * E).sum(); return float(1 - (W * O).sum() / den) if den > 0 else np.nan
def compute_metrics(T, typ):
    U = T[T.pixels > 0]; y = U.obs_status.values; q = U.pred_status.values; s = U.plot_value.values.astype(float); o = U.obs_DI.values.astype(float)
    n = len(U); n1 = int((y == 1).sum()); n0 = n - n1
    TP, FN, FP, TN = [int(((y == a) & (q == b)).sum()) for a, b in ((1, 1), (1, 0), (0, 1), (0, 0))]
    M = dict(plots=n, n_diseased=n1, n_healthy=n0, TP=TP, FN=FN, FP=FP, TN=TN)
    M['OA'] = (TP + TN) / n if n else np.nan
    M['sens'] = TP / (TP + FN) if TP + FN else np.nan; M['spec'] = TN / (TN + FP) if TN + FP else np.nan; M['BA'] = (M['sens'] + M['spec']) / 2
    pe = ((TP + FN) * (TP + FP) + (FP + TN) * (FN + TN)) / n ** 2 if n else np.nan; M['kappa'] = (M['OA'] - pe) / (1 - pe) if pe < 1 else np.nan
    rk = avg_rank(s); M['AUC'] = (rk[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0) if n1 and n0 else np.nan
    d_ = y == 1; M['r_d'] = pearson(o[d_], s[d_]); M['rho_d'] = pearson(avg_rank(o[d_]), avg_rank(s[d_]))
    if typ != 'detection':
        e = s - o; M['R2'] = 1 - (e ** 2).sum() / ((o - o.mean()) ** 2).sum(); M['RMSE'] = float(np.sqrt((e ** 2).mean())); M['MAE'] = float(np.abs(e).mean()); M['bias'] = float(e.mean())
        M['r'] = pearson(o, s); M['p_r'] = float(2 * stats.t.sf(abs(M['r']) * np.sqrt((n - 2) / (1 - M['r'] ** 2)), n - 2)) if np.isfinite(M['r']) and abs(M['r']) < 1 else np.nan
        M['rho'] = pearson(avg_rank(o), avg_rank(s))
        M['CCC'] = 2 * np.mean((o - o.mean()) * (s - s.mean())) / (o.var() + s.var() + (o.mean() - s.mean()) ** 2)
        M['RMSE_d'] = float(np.sqrt((e[d_] ** 2).mean())) if d_.any() else np.nan
        oc, pc = U.obs_class_idx.values.astype(int), U.pred_class_idx.values.astype(int)
        M['cls_OA'] = float(np.mean(oc == pc)); M['within1'] = float(np.mean(np.abs(oc - pc) <= 1)); M['QWK'] = qwk(oc, pc)
    return M
LABELS = dict(plots='Plots used', OA='Overall accuracy (healthy/diseased)', sens='Sensitivity', spec='Specificity', BA='Balanced accuracy', kappa="Cohen's kappa", AUC='AUC',
              R2='R² (DI)', RMSE='RMSE (DI, %)', MAE='MAE (DI, %)', bias='Bias (DI, %)', r='Pearson r (DI)', p_r='p (r)', rho='Spearman ρ (DI)', CCC="Lin's CCC (DI)",
              r_d='r, diseased plots', rho_d='Spearman ρ, diseased plots', RMSE_d='RMSE, diseased plots (DI, %)', cls_OA='DI-class accuracy (6 classes)', within1='Within one DI class', QWK='Quadratic weighted kappa (DI class)')
METRICS = pd.DataFrame({d['name']: compute_metrics(TABLES[d['name']], d['type']) for d in MD}).reindex(['TP', 'FN', 'FP', 'TN'] + list(LABELS))
METRICS.index = [LABELS.get(k, k) for k in METRICS.index]
METRICS.to_csv(os.path.join(OUT_DIR, 'metrics_all_models.csv'))
print(METRICS.round(3).to_string())"""

C6 = r"""SEVERITY = [d for d in MD if d['type'] != 'detection']
def boot_ci(T, typ, keys, B=N_BOOT, seed=SEED):
    # 95% percentile intervals; plots resampled with replacement within healthy and within diseased (Efron and Tibshirani, 1993)
    rs = np.random.RandomState(seed); used = T[T.pixels > 0].reset_index(drop=True); ih, idis = np.where(used.obs_status == 0)[0], np.where(used.obs_status == 1)[0]; V = {k: [] for k in keys}
    for _ in range(B):
        idx = np.r_[rs.choice(ih, len(ih)), rs.choice(idis, len(idis))]; Mb = compute_metrics(used.iloc[idx], typ)
        for k in keys: V[k].append(Mb.get(k, np.nan))
    return {k: (np.nanpercentile(v, 2.5), np.nanpercentile(v, 97.5)) for k, v in V.items()}
rows = []
for d in MD:
    keys = ['BA', 'kappa', 'AUC', 'rho_d'] + (['RMSE', 'CCC', 'rho', 'QWK'] if d['type'] != 'detection' else [])
    M = compute_metrics(TABLES[d['name']], d['type']); CI = boot_ci(TABLES[d['name']], d['type'], keys)
    for k in keys: rows.append(dict(model=d['name'], statistic=LABELS[k], value=M[k], ci_low=CI[k][0], ci_high=CI[k][1]))
BOOT = pd.DataFrame(rows); BOOT.to_csv(os.path.join(OUT_DIR, 'bootstrap_95CI.csv'), index=False)
print('95% bootstrap intervals'); print(BOOT.round(3).to_string(index=False))
# McNemar exact test on the plot status (correct / wrong) of every pair of models (McNemar, 1947; Foody, 2004)
rows = []
for i in range(len(MD)):
    for j in range(i + 1, len(MD)):
        a, b = TABLES[MD[i]['name']], TABLES[MD[j]['name']]; ok = (a.correct >= 0) & (b.correct >= 0)
        n10 = int(((a.correct == 1) & (b.correct == 0) & ok).sum()); n01 = int(((a.correct == 0) & (b.correct == 1) & ok).sum())
        p = 1.0 if n10 + n01 == 0 else min(1.0, 2 * stats.binom.cdf(min(n10, n01), n10 + n01, 0.5))
        rows.append(dict(model_A=MD[i]['name'], model_B=MD[j]['name'], A_right_B_wrong=n10, A_wrong_B_right=n01, p_exact=p, different_at_5pct='yes' if p < 0.05 else 'no'))
MCN = pd.DataFrame(rows, columns=['model_A', 'model_B', 'A_right_B_wrong', 'A_wrong_B_right', 'p_exact', 'different_at_5pct']); MCN.to_csv(os.path.join(OUT_DIR, 'mcnemar.csv'), index=False)
print('\nMcNemar exact test (plot status)'); print(MCN.round(4).to_string(index=False) if len(MCN) else 'only one model')
# Wilcoxon signed-rank test on the absolute DI error of every pair of DI models (Wilcoxon, 1945)
rows = []
for i in range(len(SEVERITY)):
    for j in range(i + 1, len(SEVERITY)):
        a, b = TABLES[SEVERITY[i]['name']], TABLES[SEVERITY[j]['name']]; ok = (a.pixels > 0) & (b.pixels > 0)
        ea, eb = (a.pred_DI - a.obs_DI).abs()[ok].values, (b.pred_DI - b.obs_DI).abs()[ok].values
        try: p = float(stats.wilcoxon(ea, eb).pvalue)
        except ValueError: p = np.nan
        rows.append(dict(model_A=SEVERITY[i]['name'], model_B=SEVERITY[j]['name'], median_abs_error_A=np.median(ea), median_abs_error_B=np.median(eb), p_wilcoxon=p, different_at_5pct='' if np.isnan(p) else ('yes' if p < 0.05 else 'no')))
WIL = pd.DataFrame(rows, columns=['model_A', 'model_B', 'median_abs_error_A', 'median_abs_error_B', 'p_wilcoxon', 'different_at_5pct']); WIL.to_csv(os.path.join(OUT_DIR, 'wilcoxon_DI_error.csv'), index=False)
print('\nWilcoxon signed-rank test (absolute DI error)'); print(WIL.round(4).to_string(index=False) if len(WIL) else 'fewer than two DI models')"""

C7 = r"""FIGS = []
CLS_COL = ['#1A9850', '#91CF60', '#FEE08B', '#FDAE61', '#F46D43', '#A50026']; ST_COL = {0: '#1A9850', 1: '#D73027'}
def save(fig, name):
    fp = os.path.join(OUT_DIR, name); fig.savefig(fp, dpi=200, bbox_inches='tight'); plt.close(fig); FIGS.append(fp); show(fp); return fp
# 1 share of diseased pixels in each plot
fig, axs = plt.subplots(len(MD), 1, figsize=(11, 2.4 * len(MD)), squeeze=False, sharex=True)
for ax, d in zip(axs[:, 0], MD):
    T = TABLES[d['name']]; ax.bar(T['plot'], T.share_diseased_pct, color=[ST_COL[s] for s in T.obs_status], edgecolor='k', lw=0.3)
    ax.axhline(100 * PLOT_DISEASED_SHARE, color='k', ls='--', lw=0.8); ax.set_ylim(0, 100); ax.set_ylabel('diseased pixels (%)')
    ax.set_title(f"{d['name']}: share of diseased pixels per plot (green = healthy plot, red = diseased plot in the ground truth; dashed = plot rule)", fontsize=9)
axs[-1, 0].set_xlabel('plot'); axs[-1, 0].set_xticks(range(1, 49)); axs[-1, 0].tick_params(axis='x', labelsize=7); fig.tight_layout(); save(fig, 'fig1_share_diseased_pixels.png')
# 2 observed DI vs mapped plot value
fig, axs = plt.subplots(1, len(MD), figsize=(4.3 * len(MD), 4.3), squeeze=False)
for ax, d in zip(axs[0], MD):
    T = TABLES[d['name']][lambda t: t.pixels > 0]; M = compute_metrics(TABLES[d['name']], d['type'])
    ax.scatter(T.obs_DI, T.plot_value, c=[ST_COL[s] for s in T.obs_status], s=22, edgecolor='k', lw=0.3); ax.set_xlim(-2, 100); ax.set_ylim(-2, 100); ax.set_xlabel('observed plot DI (%)')
    if d['type'] == 'detection':
        ax.set_ylabel('diseased pixels (%)'); ax.set_title(f"{d['name']}\nρ (diseased plots) {M['rho_d']:.2f}", fontsize=9)
    else:
        ax.plot([0, 100], [0, 100], 'k--', lw=0.8); ax.set_ylabel('mapped plot DI (%)'); ax.set_title(f"{d['name']}\nR² {M['R2']:.2f}, RMSE {M['RMSE']:.1f}, CCC {M['CCC']:.2f}", fontsize=9)
    ax.set_aspect('equal')
fig.tight_layout(); save(fig, 'fig2_observed_vs_mapped.png')
# 3 Bland-Altman plots of the DI models (Bland and Altman, 1986)
if SEVERITY:
    fig, axs = plt.subplots(1, len(SEVERITY), figsize=(4.6 * len(SEVERITY), 3.8), squeeze=False)
    for ax, d in zip(axs[0], SEVERITY):
        T = TABLES[d['name']][lambda t: t.pixels > 0]; mean_, diff = (T.pred_DI + T.obs_DI) / 2, T.pred_DI - T.obs_DI; b, sd = diff.mean(), diff.std(ddof=1)
        ax.scatter(mean_, diff, c=[ST_COL[s] for s in T.obs_status], s=22, edgecolor='k', lw=0.3)
        for v, ls in ((b, '-'), (b + 1.96 * sd, '--'), (b - 1.96 * sd, '--')): ax.axhline(v, color='k', ls=ls, lw=0.8)
        ax.set_xlabel('mean of mapped and observed DI (%)'); ax.set_ylabel('mapped − observed DI (%)'); ax.set_title(f"{d['name']}: bias {b:.1f}, limits {b - 1.96 * sd:.1f} to {b + 1.96 * sd:.1f}", fontsize=9)
    fig.tight_layout(); save(fig, 'fig3_bland_altman.png')
# 4 ROC curves (plot value against plot status)
fig, ax = plt.subplots(figsize=(4.8, 4.8))
for d in MD:
    T = TABLES[d['name']][lambda t: t.pixels > 0]; y, s = T.obs_status.values, T.plot_value.values.astype(float); th = np.r_[np.inf, np.sort(np.unique(s))[::-1]]
    tpr = [((s >= t) & (y == 1)).sum() / max(1, (y == 1).sum()) for t in th]; fpr = [((s >= t) & (y == 0)).sum() / max(1, (y == 0).sum()) for t in th]
    ax.plot(fpr, tpr, lw=1.4, label=f"{d['name']} (AUC {compute_metrics(TABLES[d['name']], d['type'])['AUC']:.2f})")
ax.plot([0, 1], [0, 1], 'k:', lw=0.8); ax.set_xlabel('1 − specificity'); ax.set_ylabel('sensitivity'); ax.legend(fontsize=7, loc='lower right'); ax.set_title('ROC – healthy vs diseased plots', fontsize=9)
fig.tight_layout(); save(fig, 'fig4_roc.png')
# 5 confusion matrices: plot status (all models) and DI class (DI models)
fig, axs = plt.subplots(len(MD), 2, figsize=(9, 3.6 * len(MD)), squeeze=False)
for k, d in enumerate(MD):
    T = TABLES[d['name']][lambda t: t.pixels > 0]; cm = pd.crosstab(pd.Categorical(T.obs_status, [0, 1]), pd.Categorical(T.pred_status, [0, 1]), dropna=False).values
    ax = axs[k, 0]; ax.imshow(cm, cmap='Blues'); ax.set_xticks([0, 1]); ax.set_yticks([0, 1]); ax.set_xticklabels(['healthy', 'diseased']); ax.set_yticklabels(['healthy', 'diseased'])
    for (i, j), v in np.ndenumerate(cm): ax.text(j, i, v, ha='center', va='center', color='w' if v > cm.max() / 2 else 'k')
    ax.set_xlabel('mapped'); ax.set_ylabel('observed'); ax.set_title(d['name'] + ': plot status', fontsize=9)
    ax = axs[k, 1]
    if d['type'] == 'detection': ax.axis('off'); continue
    cm = pd.crosstab(pd.Categorical(T.obs_class_idx, range(6)), pd.Categorical(T.pred_class_idx, range(6)), dropna=False).values
    ax.imshow(cm, cmap='Blues'); ax.set_xticks(range(6)); ax.set_yticks(range(6)); ax.set_xticklabels(CLASS_NAMES, rotation=45, ha='right', fontsize=7); ax.set_yticklabels(CLASS_NAMES, fontsize=7)
    for (i, j), v in np.ndenumerate(cm):
        if v: ax.text(j, i, v, ha='center', va='center', color='w' if v > cm.max() / 2 else 'k', fontsize=8)
    ax.set_xlabel('mapped DI class'); ax.set_ylabel('observed DI class'); ax.set_title(d['name'] + ': DI class', fontsize=9)
fig.tight_layout(); save(fig, 'fig5_confusion_matrices.png')
# 6 plot maps: observed DI class and each model's plot result
fig, axs = plt.subplots(1, len(MD) + 1, figsize=(4.6 * (len(MD) + 1), 4.2), squeeze=False)
def draw(ax, colours, title):
    for p, polys in PLOTS.items():
        for pg in polys: ax.fill(pg[:, 0], pg[:, 1], color=colours[p - 1], ec='k', lw=0.4)
        c = np.vstack(polys).mean(0); ax.text(c[0], c[1], str(p), fontsize=5, ha='center', va='center')
    ax.set_aspect('equal'); ax.invert_yaxis(); ax.set_xticks([]); ax.set_yticks([]); ax.set_title(title, fontsize=9)
draw(axs[0, 0], [CLS_COL[i] for i in GT.class_idx], 'observed DI class (ground truth)')
for ax, d in zip(axs[0, 1:], MD):
    T = TABLES[d['name']]
    if d['type'] == 'detection': draw(ax, [ST_COL.get(s, '#BBBBBB') for s in T.pred_status], d['name'] + ': mapped plot status')
    else: draw(ax, [CLS_COL[i] if i >= 0 else '#BBBBBB' for i in T.pred_class_idx], d['name'] + ': mapped DI class')
hs = [matplotlib.patches.Patch(color=c, label=n) for c, n in zip(CLS_COL, CLASS_NAMES)] + [matplotlib.patches.Patch(color=ST_COL[1], label='diseased (detection)')]
fig.legend(handles=hs, loc='lower center', ncol=7, fontsize=7); fig.tight_layout(rect=(0, 0.07, 1, 1)); save(fig, 'fig6_plot_maps.png')"""

C8 = r"""def build_workbook(path, sheets, py_tables=None, figures=None):
    # Excel workbook with live formulas: Ground_truth, one sheet per model (pixel counts -> DI, class, status, statistics), Comparison
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter as CL
    try:
        from openpyxl.workbook.properties import CalcProperties
    except ImportError:
        CalcProperties = None
    FN = 'Arial'; f_n, f_b, f_in, f_ln, f_h, f_g = Font(name=FN, size=10), Font(name=FN, size=10, bold=True), Font(name=FN, size=10, color='0000FF'), Font(name=FN, size=10, color='008000'), Font(name=FN, size=12, bold=True), Font(name=FN, size=9, color='808080')
    HEAD, INP, GREY, HELP = PatternFill('solid', fgColor='D9E1F2'), PatternFill('solid', fgColor='FFF2CC'), PatternFill('solid', fgColor='EDEDED'), PatternFill('solid', fgColor='F2F2F2')
    wrap = Alignment(wrap_text=True, vertical='top')
    def put(ws, ref, v, font=None, fill=None, fmt=None, al=None):
        c = ws[ref]; c.value = v; c.font = font or f_n
        if fill: c.fill = fill
        if fmt: c.number_format = fmt
        if al: c.alignment = al
        return c
    wb = Workbook(); wr = wb.active; wr.title = 'README'
    if CalcProperties is not None: wb.calculation = CalcProperties(fullCalcOnLoad=True)
    wc = wb.create_sheet('Comparison'); wg = wb.create_sheet('Ground_truth')
    # ---------- Ground_truth
    put(wg, 'A1', 'Ground truth: plot Disease Index (DI) of the 48 plots from the leaf ratings (26_02_26_Plot_DI.xlsx)', f_h)
    put(wg, 'A2', 'DI = Σ(x × f) / (n × Σf) × 100;  x = leaf rating (0, 1, 3, 5, 7, 9), f = number of leaves at rating x, n = highest rating (9)')
    put(wg, 'A3', 'n (highest rating)', f_b); put(wg, 'C3', N_MAX, f_in, INP)
    put(wg, 'D4', 'rating x →', f_b)
    for k, g in enumerate(GRADES): put(wg, CL(5 + k) + '4', g, f_b)
    for k, h in enumerate(['Plot', 'Block', 'Variety', 'Sowing'] + [f'f at x = {g}' for g in GRADES] + ['Σf (leaves)', 'Σ(x·f)', 'Plot DI (%)', 'Class index', 'DI class', 'Status (1 = diseased)', 'Mean leaf score']):
        put(wg, CL(1 + k) + '5', h, f_b, HEAD, al=wrap)
    put(wg, 'S4', 'DI class limits (blue cells can be edited)', f_b)
    for k, h in enumerate(['Index', 'Upper DI limit (%)', 'Class', 'DI range (%)']): put(wg, CL(19 + k) + '5', h, f_b, HEAD, al=wrap)
    rng = ['0', '1-5', '6-10', '11-25', '26-50', '>50']
    for i in range(6):
        r = 6 + i; put(wg, f'S{r}', i); put(wg, f'U{r}', CLASS_NAMES[i]); put(wg, f'V{r}', rng[i])
        if i < 5: put(wg, f'T{r}', DI_LIMITS[i], f_in, INP)
    put(wg, 'S13', 'DI = 0 Healthy; 0 < DI ≤ 5 Very low; ≤ 10 Low; ≤ 25 Moderate; ≤ 50 High; > 50 Very high', f_g)
    def CLS(x, pre='Ground_truth!'):
        return f'IF({x}<={pre}$T$6,0,IF({x}<={pre}$T$7,1,IF({x}<={pre}$T$8,2,IF({x}<={pre}$T$9,3,IF({x}<={pre}$T$10,4,5)))))'
    for j in range(48):
        r = 6 + j; put(wg, f'A{r}', j + 1); put(wg, f'B{r}', INFO['block'][j]); put(wg, f'C{r}', INFO['variety'][j]); put(wg, f'D{r}', INFO['sowing'][j])
        for k in range(6): put(wg, CL(5 + k) + str(r), int(F_LEAF[j][k]), f_in)
        put(wg, f'K{r}', f'=SUM(E{r}:J{r})'); put(wg, f'L{r}', f'=SUMPRODUCT($E$4:$J$4,E{r}:J{r})')
        put(wg, f'M{r}', f'=IF(K{r}=0,"",L{r}/($C$3*K{r})*100)', fmt='0.00'); put(wg, f'N{r}', f'=IF(M{r}="","",{CLS("M%d" % r, "")})')
        put(wg, f'O{r}', f'=IF(N{r}="","",INDEX($U$6:$U$11,N{r}+1))'); put(wg, f'P{r}', f'=IF(M{r}="","",IF(M{r}>0,1,0))'); put(wg, f'Q{r}', f'=IF(K{r}=0,"",L{r}/K{r})', fmt='0.00')
    for k, w in enumerate([6, 7, 8, 8] + [8] * 6 + [9, 9, 10, 8, 11, 10, 10, 3, 7, 10, 11, 10]): wg.column_dimensions[CL(1 + k)].width = w
    wg.freeze_panes = 'B6'
    # ---------- model sheets
    MET = [('plots', 'Plots used (plots with crop pixels)', '0', 'all'), ('n1', 'Diseased plots (ground truth)', '0', 'all'), ('n0', 'Healthy plots (ground truth)', '0', 'all'),
           ('TP', 'TP: diseased plot mapped diseased', '0', 'all'), ('FN', 'FN: diseased plot mapped healthy', '0', 'all'), ('FP', 'FP: healthy plot mapped diseased', '0', 'all'), ('TN', 'TN: healthy plot mapped healthy', '0', 'all'),
           ('OA', 'Overall accuracy (healthy/diseased)', '0.000', 'all'), ('sens', 'Sensitivity', '0.000', 'all'), ('spec', 'Specificity', '0.000', 'all'), ('BA', 'Balanced accuracy', '0.000', 'all'),
           ('pe', 'Chance agreement (for kappa)', '0.000', 'all'), ('kappa', "Cohen's kappa", '0.000', 'all'), ('AUC', 'AUC (plot value vs status)', '0.000', 'all'),
           ('mo', 'Mean observed DI (plots used)', '0.00', 'sev'), ('R2', 'R² (DI)', '0.000', 'sev'), ('RMSE', 'RMSE (DI, %)', '0.00', 'sev'), ('MAE', 'MAE (DI, %)', '0.00', 'sev'), ('bias', 'Bias (DI, %; mapped − observed)', '0.00', 'sev'),
           ('r', 'Pearson r (DI)', '0.000', 'sev'), ('p_r', 'p (r)', '0.0000', 'sev'), ('rho', 'Spearman ρ (DI)', '0.000', 'sev'), ('CCC', "Lin's CCC (DI)", '0.000', 'sev'),
           ('r_d', 'r, diseased plots (plot value vs DI)', '0.000', 'all'), ('rho_d', 'Spearman ρ, diseased plots', '0.000', 'all'), ('RMSE_d', 'RMSE, diseased plots (DI, %)', '0.00', 'sev'),
           ('cls_OA', 'DI-class accuracy (6 classes)', '0.000', 'sev'), ('within1', 'Within one DI class', '0.000', 'sev'), ('QWK', 'Quadratic weighted kappa (DI class)', '0.000', 'sev')]
    ROW = {k: 8 + i for i, (k, *_) in enumerate(MET)}
    R0, R1 = 8, 55; rg = lambda c: f'${c}${R0}:${c}${R1}'
    names = []
    for si, s in enumerate(sheets):
        typ = s['type']; det = typ == 'detection'
        sh = (f"M{si + 1}_" + re.sub(r'\W+', '_', s['name']).strip('_'))[:31]; names.append((sh, s['name'], typ)); ws = wb.create_sheet(sh)
        put(ws, 'A1', 'Model sheet – pixel classes inside each plot → plot values → statistics', f_h)
        put(ws, 'A2', 'Model name', f_b); put(ws, 'B2', s['name'], f_in, INP)
        put(ws, 'A3', 'Model type', f_b); put(ws, 'B3', {'detection': 'detection (healthy / diseased pixels)', 'grade': 'grade (pixel grade 0, 1, 3, 5, 7, 9)', 'score': 'score (pixel score put in the nearest grade)'}[typ])
        put(ws, 'A4', 'Plot diseased if share of diseased pixels >', f_b); put(ws, 'B4', PLOT_DISEASED_SHARE, f_in, INP, '0.00')
        put(ws, 'A5', 'Pixel counts from', f_b); put(ws, 'B5', s.get('source') or 'enter or paste the pixel counts of each plot in the yellow cells (columns F-K)')
        heads = ['Plot', 'Observed DI (%)', 'Observed class index', 'Observed DI class', 'Observed status (1 = diseased)']
        heads += ['Healthy pixels', 'Diseased pixels', '–', '–', '–', '–'] if det else [f'Pixels at grade {g}' for g in GRADES]
        heads += ['Crop pixels (Σf)', 'Diseased pixels (%)', 'Mapped DI (%)', 'Mapped class index', 'Mapped DI class', 'Mapped status (1 = diseased)', 'Status correct (1/0)', 'DI error (mapped − observed)', 'Class within one (1/0)',
                  'Plot value for AUC / correlation', 'helper: rank observed DI', 'helper: rank plot value', 'helper: rank observed DI (diseased)', 'helper: rank plot value (diseased)', 'helper: diseased plot with pixels', 'helper: plot value or 0', 'helper: DI error or 0', 'Mean pixel value']
        for k, h in enumerate(heads): put(ws, CL(1 + k) + '7', h, f_b, HELP if h.startswith('helper') else HEAD, al=wrap)
        if not det:
            put(ws, 'E6', 'pixel grade x →', f_b)
            for k, g in enumerate(GRADES): put(ws, CL(6 + k) + '6', g, f_b)
        C = s.get('counts'); MV = s.get('mean_value')
        for j in range(48):
            r = R0 + j; g = 6 + j
            for col, src in zip('ABCDE', 'AMNOP'): put(ws, f'{col}{r}', f'=Ground_truth!{src}{g}', f_ln, fmt='0.00' if col == 'B' else None)
            for k in range(2 if det else 6):
                put(ws, CL(6 + k) + str(r), None if C is None else int(C[j][k]), f_in, INP)
            if det:
                for k in range(2, 6): ws[CL(6 + k) + str(r)].fill = GREY
            put(ws, f'L{r}', f'=SUM(F{r}:K{r})')
            if det:
                put(ws, f'M{r}', f'=IF(L{r}=0,"",G{r}/L{r}*100)', fmt='0.00')
                for col in 'NOPST': ws[f'{col}{r}'].fill = GREY
                put(ws, f'U{r}', f'=M{r}', fmt='0.00'); put(ws, f'AB{r}', 0, f_g)
            else:
                put(ws, f'M{r}', f'=IF(L{r}=0,"",(L{r}-F{r})/L{r}*100)', fmt='0.00')
                put(ws, f'N{r}', f'=IF(L{r}=0,"",SUMPRODUCT($F$6:$K$6,F{r}:K{r})/(Ground_truth!$C$3*L{r})*100)', fmt='0.00')
                put(ws, f'O{r}', f'=IF(N{r}="","",{CLS("N%d" % r)})'); put(ws, f'P{r}', f'=IF(O{r}="","",INDEX(Ground_truth!$U$6:$U$11,O{r}+1))')
                put(ws, f'S{r}', f'=IF(N{r}="","",N{r}-B{r})', fmt='0.00'); put(ws, f'T{r}', f'=IF(O{r}="","",IF(ABS(O{r}-C{r})<=1,1,0))')
                put(ws, f'U{r}', f'=N{r}', fmt='0.00'); put(ws, f'AB{r}', f'=IF(S{r}="",0,S{r})', f_g, fmt='0.00')
            put(ws, f'Q{r}', f'=IF(M{r}="","",IF(M{r}/100>$B$4,1,0))'); put(ws, f'R{r}', f'=IF(Q{r}="","",IF(Q{r}=E{r},1,0))')
            put(ws, f'V{r}', f'=IF(U{r}="","",SUMPRODUCT(({rg("U")}<>"")*({rg("B")}<B{r}))+(SUMPRODUCT(({rg("U")}<>"")*({rg("B")}=B{r}))+1)/2)', f_g)
            put(ws, f'W{r}', f'=IF(U{r}="","",SUMPRODUCT(--({rg("U")}<U{r}))+(SUMPRODUCT(--({rg("U")}=U{r}))+1)/2)', f_g)
            put(ws, f'X{r}', f'=IF(OR(U{r}="",E{r}<>1),0,SUMPRODUCT(({rg("E")}=1)*({rg("U")}<>"")*({rg("B")}<B{r}))+(SUMPRODUCT(({rg("E")}=1)*({rg("U")}<>"")*({rg("B")}=B{r}))+1)/2)', f_g)
            put(ws, f'Y{r}', f'=IF(OR(U{r}="",E{r}<>1),0,SUMPRODUCT(({rg("E")}=1)*({rg("U")}<U{r}))+(SUMPRODUCT(({rg("E")}=1)*({rg("U")}=U{r}))+1)/2)', f_g)
            put(ws, f'Z{r}', f'=IF(AND(E{r}=1,L{r}>0),1,0)', f_g); put(ws, f'AA{r}', f'=IF(U{r}="",0,U{r})', f_g, fmt='0.00')
            put(ws, f'AC{r}', None if MV is None or not np.isfinite(MV[j]) else float(MV[j]), f_in, fmt='0.000')
        # statistics
        put(ws, 'AE6', 'Statistics (formulas)', f_h); put(ws, 'AE7', 'Statistic', f_b, HEAD); put(ws, 'AF7', 'Value', f_b, HEAD); put(ws, 'AG7', 'Definition', f_b, HEAD)
        A = lambda k: f'AF{ROW[k]}'; nU = 'SUM($Z$8:$Z$55)'
        def corr(x, y):
            Z = '$Z$8:$Z$55'
            return (f'=IF(AF9<3,"",IFERROR(({nU}*SUMPRODUCT({Z},{x},{y})-SUMPRODUCT({Z},{x})*SUMPRODUCT({Z},{y}))/SQRT(({nU}*SUMPRODUCT({Z},{x},{x})-SUMPRODUCT({Z},{x})^2)*'
                    f'({nU}*SUMPRODUCT({Z},{y},{y})-SUMPRODUCT({Z},{y})^2)),""))')
        F = dict(plots=f'=COUNTIF({rg("L")},">0")', n1=f'=COUNTIFS({rg("E")},1,{rg("L")},">0")', n0=f'=COUNTIFS({rg("E")},0,{rg("L")},">0")',
                 TP=f'=COUNTIFS({rg("E")},1,{rg("Q")},1)', FN=f'=COUNTIFS({rg("E")},1,{rg("Q")},0)', FP=f'=COUNTIFS({rg("E")},0,{rg("Q")},1)', TN=f'=COUNTIFS({rg("E")},0,{rg("Q")},0)',
                 OA=f'=IF(AF8=0,"",(AF11+AF14)/AF8)', sens='=IF(AF11+AF12=0,"",AF11/(AF11+AF12))', spec='=IF(AF13+AF14=0,"",AF14/(AF13+AF14))', BA='=IF(OR(AF16="",AF17=""),"",(AF16+AF17)/2)',
                 pe='=IF(AF8=0,"",((AF11+AF12)*(AF11+AF13)+(AF13+AF14)*(AF12+AF14))/AF8^2)', kappa='=IF(OR(AF8=0,AF19=""),"",IF(AF19=1,"",(AF15-AF19)/(1-AF19)))',
                 AUC=f'=IF(OR(AF9=0,AF10=0),"",(SUMIF({rg("E")},1,{rg("W")})-AF9*(AF9+1)/2)/(AF9*AF10))',
                 mo=f'=IF(AF8=0,"",SUMIF({rg("L")},">0",{rg("B")})/AF8)', R2=f'=IF(AF8=0,"",IFERROR(1-SUMSQ({rg("S")})/SUMPRODUCT(({rg("L")}>0)*({rg("B")}-AF22)^2),""))',
                 RMSE=f'=IF(AF8=0,"",SQRT(SUMSQ({rg("S")})/AF8))', MAE=f'=IF(AF8=0,"",(SUMIF({rg("S")},">0")-SUMIF({rg("S")},"<0"))/AF8)', bias=f'=IF(AF8=0,"",SUM({rg("S")})/AF8)',
                 r=f'=IF(AF8<3,"",IFERROR(CORREL({rg("B")},{rg("U")}),""))', p_r='=IF(AF27="","",IFERROR(TDIST(ABS(AF27)*SQRT((AF8-2)/(1-AF27^2)),AF8-2,2),""))',
                 rho=f'=IF(AF8<3,"",IFERROR(CORREL({rg("V")},{rg("W")}),""))',
                 CCC=f'=IF(AF8<3,"",IFERROR(2*COVAR({rg("B")},{rg("U")})/(VARP({rg("B")})+VARP({rg("U")})+(AVERAGE({rg("B")})-AVERAGE({rg("U")}))^2),""))',
                 r_d=corr('$B$8:$B$55', '$AA$8:$AA$55'), rho_d=corr('$X$8:$X$55', '$Y$8:$Y$55'), RMSE_d=f'=IF(AF9=0,"",SQRT(SUMPRODUCT($Z$8:$Z$55,$AB$8:$AB$55,$AB$8:$AB$55)/{nU}))',
                 cls_OA=f'=IF(AF8=0,"",SUMPRODUCT(({rg("L")}>0)*({rg("O")}={rg("C")}))/AF8)', within1=f'=IF(AF8=0,"",SUM({rg("T")})/AF8)',
                 QWK='=IF(AF8=0,"",IFERROR(1-SUMPRODUCT($AF$60:$AK$65,$AF$42:$AK$47)/SUMPRODUCT($AF$60:$AK$65,$AF$51:$AK$56),""))')
        DEF = dict(plots='plots with at least one crop pixel', n1='observed DI > 0', n0='observed DI = 0', OA='(TP + TN) / plots', sens='TP / (TP + FN)', spec='TN / (TN + FP)', BA='(sensitivity + specificity) / 2',
                   pe='chance agreement of the 2 × 2 table', kappa='(OA − pe) / (1 − pe) (Cohen, 1960)', AUC='Mann–Whitney form, ties = ½ (Hanley and McNeil, 1982)', mo='helper for R²',
                   R2='1 − Σ(error²) / Σ(observed − mean)²', RMSE='√(mean error²)', MAE='mean |error|', bias='mean error', r='Pearson correlation', p_r='two-sided t test of r', rho='Pearson r of the average ranks',
                   CCC='2·cov / (var_obs + var_map + (mean_obs − mean_map)²), population moments (Lin, 1989)', r_d='36 diseased plots: does the map rank severity?', rho_d='rank version of the line above',
                   RMSE_d='DI error on the diseased plots only', cls_OA='mapped DI class = observed DI class', within1='|class index difference| ≤ 1', QWK='weights (i − j)² / 25 (Cohen, 1968)')
        for k, lab, fmt, kind in MET:
            r = ROW[k]; put(ws, f'AE{r}', lab, f_b if k in ('OA', 'BA', 'kappa', 'AUC', 'R2', 'RMSE', 'CCC', 'QWK') else f_n)
            if kind == 'sev' and det: put(ws, f'AF{r}', 'n/a', f_g)
            else: put(ws, f'AF{r}', F[k], fmt=fmt)
            put(ws, f'AG{r}', DEF.get(k, ''), f_g)
        if not det:
            put(ws, 'AE40', 'DI-class confusion matrix (rows = observed class, columns = mapped class)', f_b)
            put(ws, 'AE41', 'observed \\ mapped', f_b, HEAD); put(ws, 'AL41', 'Total', f_b, HEAD)
            for i in range(6):
                put(ws, CL(32 + i) + '41', f'=Ground_truth!U{6 + i}', f_b, HEAD); put(ws, f'AE{42 + i}', f'=Ground_truth!U{6 + i}', f_b)
                put(ws, f'AE{51 + i}', f'=Ground_truth!U{6 + i}', f_b); put(ws, f'AE{60 + i}', f'=Ground_truth!U{6 + i}', f_b)
                for jj in range(6):
                    col = CL(32 + jj); put(ws, f'{col}{42 + i}', f'=COUNTIFS({rg("C")},{i},{rg("O")},{jj})')
                    put(ws, f'{col}{51 + i}', f'=IF($AL$48=0,0,$AL{42 + i}*{col}$48/$AL$48)', fmt='0.00'); put(ws, f'{col}{60 + i}', (i - jj) ** 2 / 25, f_g, fmt='0.00')
                put(ws, f'AL{42 + i}', f'=SUM(AF{42 + i}:AK{42 + i})')
            put(ws, 'AE48', 'Total', f_b)
            for jj in range(7): col = CL(32 + jj); put(ws, f'{col}48', f'=SUM({col}42:{col}47)')
            put(ws, 'AE50', 'Expected counts by chance (row total × column total / N)', f_b); put(ws, 'AE59', 'Quadratic weights (i − j)² / 25', f_b)
        for k, w in enumerate([6, 9, 8, 10, 9] + [9] * 6 + [9, 9, 9, 9, 10, 9, 8, 9, 8, 10] + [7] * 7 + [9, 2, 34, 9, 52]): ws.column_dimensions[CL(1 + k)].width = w
        ws.freeze_panes = 'B8'
    # ---------- Comparison
    put(wc, 'A1', 'Comparison of the models – plot-level statistics (formulas linked to the model sheets)', f_h)
    put(wc, 'A2', f'Plot status: a plot is mapped diseased when more than the share in cell B4 of each model sheet of its crop pixels is diseased (pixel grade > 0). DI from pixel classes: Σ(x·f)/(9·Σf)×100. n/a = not defined for detection maps.', f_g)
    cols = [('plots', '0'), ('OA', '0.000'), ('sens', '0.000'), ('spec', '0.000'), ('BA', '0.000'), ('kappa', '0.000'), ('AUC', '0.000'), ('R2', '0.000'), ('RMSE', '0.00'), ('MAE', '0.00'), ('bias', '0.00'),
            ('r', '0.000'), ('p_r', '0.0000'), ('rho', '0.000'), ('CCC', '0.000'), ('r_d', '0.000'), ('rho_d', '0.000'), ('RMSE_d', '0.00'), ('cls_OA', '0.000'), ('within1', '0.000'), ('QWK', '0.000')]
    lab = {k: l for k, l, *_ in MET}
    put(wc, 'A4', 'Model', f_b, HEAD); put(wc, 'B4', 'Type', f_b, HEAD)
    for k, (key, fmt) in enumerate(cols): put(wc, CL(3 + k) + '4', lab[key], f_b, HEAD, al=wrap)
    for i, (sh, nm, typ) in enumerate(names):
        r = 5 + i; put(wc, f'A{r}', f"='{sh}'!B2", f_ln); put(wc, f'B{r}', typ)
        for k, (key, fmt) in enumerate(cols): put(wc, CL(3 + k) + str(r), f"='{sh}'!AF{ROW[key]}", f_ln, fmt=fmt)
    r = 5 + len(names) + 2; put(wc, f'A{r}', 'McNemar exact test – plot status correct / wrong, every pair of models (McNemar, 1947; Foody, 2004)', f_b); r += 1
    for k, h in enumerate(['Model A', 'Model B', 'A right, B wrong', 'A wrong, B right', 'p (exact, two-sided)', 'Different at 5%?']): put(wc, CL(1 + k) + str(r), h, f_b, HEAD, al=wrap)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            r += 1; a, b = names[i][0], names[j][0]
            put(wc, f'A{r}', f"='{a}'!B2", f_ln); put(wc, f'B{r}', f"='{b}'!B2", f_ln)
            put(wc, f'C{r}', f"=IF(OR('{a}'!AF8=0,'{b}'!AF8=0),\"\",SUMPRODUCT(('{a}'!$R$8:$R$55=1)*('{b}'!$R$8:$R$55=0)))")
            put(wc, f'D{r}', f"=IF(OR('{a}'!AF8=0,'{b}'!AF8=0),\"\",SUMPRODUCT(('{a}'!$R$8:$R$55=0)*('{b}'!$R$8:$R$55=1)))")
            put(wc, f'E{r}', f'=IF(C{r}="","",IF(C{r}+D{r}=0,1,MIN(1,2*BINOMDIST(MIN(C{r},D{r}),C{r}+D{r},0.5,TRUE))))', fmt='0.0000')
            put(wc, f'F{r}', f'=IF(E{r}="","",IF(E{r}<0.05,"yes","no"))')
    for k, w in enumerate([22, 10] + [10] * len(cols)): wc.column_dimensions[CL(1 + k)].width = w
    wc.freeze_panes = 'C5'
    # ---------- README
    txt = ['Plot-level evaluation of pixel maps – 48 plots, UAV hyperspectral image of 24 February 2026', '',
           'Sheets', 'Comparison – key statistics of every model side by side and McNemar tests between models (all formulas).',
           'Ground_truth – leaf counts per rating and the plot DI, DI class and status of the 48 plots (26_02_26_Plot_DI.xlsx).',
           'M1, M2, … – one sheet per model: pixel counts inside each plot (yellow), plot values and statistics (formulas). Blank sheets are for models you enter by hand.',
           'Python_stats – values computed by the notebook: bootstrap 95% intervals, McNemar and Wilcoxon tests, and the same statistics as a cross-check (present when the notebook made the file).',
           'Figures – the notebook figures (present when the notebook made the file).', '',
           'How the plot values are made',
           'Detection map: pixel healthy or diseased → share of diseased pixels (%) in the plot; plot mapped diseased if share > 0.5 (cell B4).',
           'Grade map: pixel grade x = 0, 1, 3, 5, 7, 9 → DI = Σ(x·f) / (n·Σf) × 100 with f = number of pixels at grade x and n = 9 (same formula as the leaf DI) → DI class with the limits on Ground_truth.',
           'Score map: pixel score put in the nearest grade (< 0.5 → 0, 0.5–2 → 1, 2–4 → 3, 4–6 → 5, 6–8 → 7, ≥ 8 → 9), then as for a grade map.',
           'Status for grade and score maps: pixel diseased if grade > 0; plot mapped diseased if share of diseased pixels > 0.5 – the same rule as for detection maps, so all models are compared alike.', '',
           'Entering another model by hand', 'Use a blank model sheet (or copy one with Move or Copy… → Create a copy). Type the model name in B2 and paste the pixel counts of plots 1–48 in the yellow cells:',
           'detection sheet: F = healthy pixels, G = diseased pixels; grade sheet: F–K = pixels at grade 0, 1, 3, 5, 7, 9 (e.g. from ENVI ROI statistics of a class map).',
           'All 48 plots should have pixels; the statistics use the plots with pixels. Blue = inputs, black = formulas, green = links to other sheets.', '',
           'References', 'Bland, J.M., Altman, D.G. (1986). Statistical methods for assessing agreement between two methods of clinical measurement. Lancet 327, 307–310.',
           'Cohen, J. (1960). A coefficient of agreement for nominal scales. Educational and Psychological Measurement 20, 37–46.',
           'Cohen, J. (1968). Weighted kappa: nominal scale agreement with provision for scaled disagreement or partial credit. Psychological Bulletin 70, 213–220.',
           'Congalton, R.G. (1991). A review of assessing the accuracy of classifications of remotely sensed data. Remote Sensing of Environment 37, 35–46.',
           'Efron, B., Tibshirani, R.J. (1993). An Introduction to the Bootstrap. Chapman and Hall, New York.',
           'Foody, G.M. (2004). Thematic map comparison: evaluating the statistical significance of differences in classification accuracy. Photogrammetric Engineering and Remote Sensing 70, 627–633.',
           'Hanley, J.A., McNeil, B.J. (1982). The meaning and use of the area under a receiver operating characteristic (ROC) curve. Radiology 143, 29–36.',
           'Lin, L.I. (1989). A concordance correlation coefficient to evaluate reproducibility. Biometrics 45, 255–268.',
           'McKinney, H.H. (1923). Influence of soil temperature and moisture on infection of wheat seedlings by Helminthosporium sativum. Journal of Agricultural Research 26, 195–218. (disease index)',
           'McNemar, Q. (1947). Note on the sampling error of the difference between correlated proportions or percentages. Psychometrika 12, 153–157.',
           'Wilcoxon, F. (1945). Individual comparisons by ranking methods. Biometrics Bulletin 1, 80–83.']
    for i, t in enumerate(txt): put(wr, f'A{1 + i}', t, f_h if i == 0 else (f_b if t in ('Sheets', 'How the plot values are made', 'Entering another model by hand', 'References') else f_n))
    wr.column_dimensions['A'].width = 160
    # ---------- Python tables and figures
    if py_tables:
        wp = wb.create_sheet('Python_stats'); r = 1
        for title, df in py_tables:
            if not isinstance(df.index, pd.RangeIndex): df = df.reset_index().rename(columns={'index': 'statistic'})
            put(wp, f'A{r}', title, f_b); r += 1
            for k, h in enumerate(df.columns): put(wp, CL(1 + k) + str(r), str(h), f_b, HEAD, al=wrap)
            for _, row in df.iterrows():
                r += 1
                for k, v in enumerate(row.values):
                    v = v.item() if hasattr(v, 'item') else v
                    if isinstance(v, float) and not np.isfinite(v): v = None
                    put(wp, CL(1 + k) + str(r), v, fmt='0.0000' if isinstance(v, float) else None)
            r += 3
        wp.column_dimensions['A'].width = 34
        for k in range(2, 12): wp.column_dimensions[CL(k)].width = 16
    if figures:
        try:
            from openpyxl.drawing.image import Image as XLImage
            wf = wb.create_sheet('Figures'); r = 1
            for fp in figures:
                put(wf, f'A{r}', os.path.basename(fp), f_b); im = XLImage(fp); sc = min(1.0, 900 / im.width); im.width, im.height = im.width * sc, im.height * sc
                wf.add_image(im, f'A{r + 1}'); r += int(im.height / 20) + 4
        except Exception as e:
            print('figures not placed in Excel (' + type(e).__name__ + '); they are saved as PNG files')
    wb.save(path)
    return names
SHEETS = [dict(name=d['name'], type=d['type'], source=d['file'] + f" (SPATIAL_STEP {d['step']})", counts=d['counts'], mean_value=d['mean_value']) for d in MD]
for b in range(BLANK_SHEETS): SHEETS.append(dict(name=f'Blank {("detection", "grade")[b % 2]} model {b + 1}', type=('detection', 'grade')[b % 2]))
PYT = [('Statistics of every model (computed in Python; same definitions as the formulas)', METRICS), ('95% bootstrap intervals', BOOT), ('McNemar exact test (plot status)', MCN),
       ('Wilcoxon signed-rank test (absolute DI error)', WIL)]
XLSX = os.path.join(OUT_DIR, XLSX_NAME); names = build_workbook(XLSX, SHEETS, PYT, FIGS)
print('Excel workbook:', XLSX); print('sheets:', ', '.join(['README', 'Comparison', 'Ground_truth'] + [n[0] for n in names] + ['Python_stats', 'Figures']))"""

C9 = r"""info = dict(models=[dict(name=d['name'], type=d['type'], file=d['file'], spatial_step=d['step'], crop_pixels_in_plots=int(d['counts'].sum())) for d in MD],
            plot_diseased_share=PLOT_DISEASED_SHARE, n_boot=N_BOOT, seed=SEED, di_limits=DI_LIMITS)
json.dump(info, open(os.path.join(OUT_DIR, 'run_info.json'), 'w'), indent=1)
print('results in', OUT_DIR); print('\n'.join(sorted(os.listdir(OUT_DIR))))"""

MD_ = ['## 0 Install the packages (run once)\nIf something new is installed, restart the kernel (*Kernel → Restart*) and continue with step 1.',
       "## 1 Settings\nPaths and the list of model maps. `MODELS`: one line per map (name, type, file). The three RF maps are filled in; uncomment or add lines for other models – any detection (`*_class.dat`), grade (`*_grade.dat` or grade `.dat`) or score (`*_score.dat` or score `.dat`) map written by the per-model notebooks.",
       '## 2 Libraries, image geometry and plot masks\nThe plot polygons of the ROI file are converted to image pixels with the map information of the image header; on each model map a pixel belongs to a plot when its centre lies inside the polygon (plots 1 and 48 extend slightly beyond the image: only their pixels inside the image are used).',
       '## 3 Ground truth – plot Disease Index\nLeaf counts f at each rating x (0, 1, 3, 5, 7, 9) per plot from `26_02_26_Plot_DI.xlsx` (embedded; read from `GT_FILE` if that file exists). DI = Σ(x·f)/(n·Σf)×100 with n = 9 (McKinney, 1923); class: DI = 0 Healthy, ≤ 5 Very low, ≤ 10 Low, ≤ 25 Moderate, ≤ 50 High, > 50 Very high; status diseased if DI > 0.',
       '## 4 Pixel classes inside each plot\nFor every model map: crop pixels inside each plot and their class (detection: healthy/diseased; grade: 0, 1, 3, 5, 7, 9; score: nearest grade). Per plot: counts f, share of diseased pixels, DI from the pixel classes (same formula as the leaf DI, f = number of pixels at grade x), DI class and status (diseased if more than `PLOT_DISEASED_SHARE` of the pixels are diseased).',
       '## 5 Statistics\nHealthy/diseased plots (all models; Congalton, 1991): TP, FN, FP, TN, overall accuracy, sensitivity, specificity, balanced accuracy, Cohen\'s kappa (Cohen, 1960), AUC of the plot value (Hanley and McNeil, 1982). DI (grade and score models): R², RMSE, MAE, bias, Pearson r with p, Spearman ρ, Lin\'s CCC (Lin, 1989); r, ρ and RMSE on the 36 diseased plots (does the map rank severity where disease is present?). DI class: exact, within one class, quadratic weighted kappa (Cohen, 1968).',
       '## 6 Uncertainty and model comparison\n95% bootstrap intervals (2000 resamples of the plots within healthy and within diseased; Efron and Tibshirani, 1993). McNemar exact test on plot status between every pair of models (McNemar, 1947; Foody, 2004); Wilcoxon signed-rank test on the absolute DI error between DI models (Wilcoxon, 1945).',
       '## 7 Figures\n1 share of diseased pixels per plot · 2 observed DI vs mapped value · 3 Bland–Altman (Bland and Altman, 1986) · 4 ROC · 5 confusion matrices · 6 plot maps (observed DI class and each model).',
       '## 8 Excel workbook (live formulas)\nThe pixel counts go into one sheet per model; DI, class, status and all statistics are Excel formulas, so the numbers recompute if a count or a class limit is changed. `Comparison` puts the models side by side with McNemar tests; `Python_stats` holds the bootstrap intervals and tests; `Figures` the PNGs. Blank sheets are added for models entered by hand.',
       '## 9 Outputs']
def cell(kind, t):
    c = dict(cell_type=kind, metadata={}, source=[l + '\n' for l in t.split('\n')]); c['source'][-1] = c['source'][-1].rstrip('\n')
    if kind == 'code': c.update(execution_count=None, outputs=[])
    return c
CODE = [C0, C1, C2, C3, C4, C5, C6, C7, C8, C9]
cells = [cell('markdown', TITLE)]
for m, c in zip(MD_, CODE): cells += [cell('markdown', m), cell('code', c)]
for i, c in enumerate(cells): c['id'] = 'c%02d' % i
meta = dict(kernelspec=dict(display_name='Python 3', language='python', name='python3'), language_info=dict(name='python'))
NB = PM + 'Plot_level_evaluation_48_plots_24Feb2026.ipynb'
json.dump(dict(nbformat=4, nbformat_minor=5, metadata=meta, cells=cells), open(NB, 'w'), indent=1); print('written', NB)
if __name__ == '__main__':
    # blank workbook with the same layout (3 RF model sheets + 2 blank sheets), for models entered by hand
    G = {'__name__': 'tpl', 'GT_FILE': None, 'PLOT_DISEASED_SHARE': 0.5}
    exec('import os, re, json, numpy as np, pandas as pd\nGRADES = [0, 1, 3, 5, 7, 9]', G); exec(C3.split("if GT_FILE")[0], G)
    exec(C8.split('SHEETS = [')[0], G)
    tpl = [dict(name='RF detection', type='detection'), dict(name='RF six grades', type='grade'), dict(name='RF severity score', type='score'),
           dict(name='Blank detection model 1', type='detection'), dict(name='Blank grade model 2', type='grade')]
    G['build_workbook'](PM + 'Plot_level_evaluation_TEMPLATE.xlsx', tpl); print('written', PM + 'Plot_level_evaluation_TEMPLATE.xlsx')
