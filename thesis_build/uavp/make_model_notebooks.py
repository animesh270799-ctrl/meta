"""One standalone Jupyter notebook PER MODEL that applies that model to every crop pixel of the UAV hyperspectral image of 24 Feb 2026.
Each notebook contains only the code its model needs (no shared module), reads the ENVI image block by block, writes the pixel map
(ENVI + GeoTIFF + PNG), checks itself on the 48 plot-mean spectra and computes the per-plot accuracy against the ASD scores of the day.
The helper code (image reader, georeferencing, ROI parser, networks, features) is taken verbatim from make_notebook.py (tested).
Output: uavp/kit/per_model/<task>_<model>_pixel_map_24Feb2026.ipynb (7 notebooks) + README.txt"""
import json, os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.argv = sys.argv[:1]; import make_notebook as MNB          # builds the shared cell texts (no file written on import)
OUTD = HERE + 'kit/per_model/'; os.makedirs(OUTD, exist_ok=True)
C = {i: t for i, (k, t) in enumerate(MNB.cells)}
# reference predictions of every model on the 48 plot means, as embedded in the tested all-model notebook
NB0 = json.load(open(HERE + 'kit/White_rust_pixel_map_24Feb2026.ipynb'))
src0 = next(''.join(c['source']) for c in NB0['cells'] if 'EXPECTED = ' in ''.join(c['source']))
EXPECTED = json.loads(src0[src0.index('EXPECTED = ') + len('EXPECTED = '):].split('\n')[0])
TASKN = {'A': 'detection (healthy / diseased)', 'B': 'six severity grades (0, 1, 3, 5, 7, 9)', 'C': 'severity score (0–9)'}
VARN = {'direct': 'direct UAV reflectance', 'corrected': 'UAV reflectance × healthy-reference gain (ASD healthy / UAV healthy)', 'normalised': 'gain-corrected reflectance scaled to the mean reflectance of the healthy ASD leaves'}
LIBS = C[4]; NETS = C[6]; FEAT = C[10]; OPEN = C[16]
MODEL_FIND = '''OUT = os.path.join(OUT_DIR, OUT_NAME); os.makedirs(OUT, exist_ok=True)
_mf = os.path.basename(MODEL_FILE.replace('\\\\', '/'))
_cands = [MODEL_FILE, os.path.join(os.getcwd(), 'models', _mf), os.path.join(os.getcwd(), _mf), os.path.join(os.path.dirname(OUT_DIR), 'models', _mf)]
MODEL_FILE = next((c for c in _cands if os.path.isfile(c)), None)
if MODEL_FILE is None: raise FileNotFoundError('Model file ' + _mf + ' not found. Looked in:\\n  ' + '\\n  '.join(_cands) + '\\nCopy the kit folder "models" to one of these places or correct MODEL_FILE in step 1.')
print('model file  :', MODEL_FILE); print('results to  :', OUT)'''
DNN_TXT = NETS[NETS.index('class DNNF1'):NETS.index('def pseudo')].rstrip() + '\n'
CNX_TXT = NETS[:NETS.index('class DNNF1')] + NETS[NETS.index('def pseudo'):]
fmt = MNB.fmt

LOAD = {
'svm': r"""z = np.load(MODEL_FILE, allow_pickle=False); FEATURES = [str(f) for f in z['features']]; MU, SD = z['mu'], z['sd']
SV, DUAL, B0, GAMMA, CLASSES = z['sv'], z['dual'], float(z['b0'][0]), float(z['gamma'][0]), z['classes']
def predict(S):
    # spectra (pixels x bands, reflectance 0-1) -> SVM decision value (> 0 = diseased) and class
    Z = (features(make_variant(S, VARIANT), FEATURES, OP) - MU) / SD; out = np.empty(len(Z))
    for i in range(0, len(Z), 4096):                           # radial-basis decision function, as in scikit-learn SVC
        d2 = ((Z[i:i + 4096, None, :] - SV[None]) ** 2).sum(2); out[i:i + 4096] = np.exp(-GAMMA * d2) @ DUAL + B0
    return out, np.where(out > 0, CLASSES[1], CLASSES[0]).astype(int)
print(f'SVM: {len(SV)} support vectors, gamma {GAMMA:.4g}; features: {", ".join(FEATURES)}')""",
'rf': r"""z = np.load(MODEL_FILE, allow_pickle=False); FEATURES = [str(f) for f in z['features']]; MU, SD = z['mu'], z['sd']
LEFT, RIGHT, FEAT, THR, VALUE, OFFSET, CLASSES = z['left'], z['right'], z['feat'], z['thr'], z['value'], z['offset'], z['classes']
def predict(S):
    # spectra -> grade: every pixel is routed through every tree; class proportions of the reached leaves are averaged (scikit-learn RandomForest)
    Z = ((features(make_variant(S, VARIANT), FEATURES, OP) - MU) / SD).astype(np.float32); n = len(Z); rows = np.arange(n); P = np.zeros((n, VALUE.shape[1]))
    for o in OFFSET:
        node = np.zeros(n, int)
        while True:
            g = o + node; leaf = LEFT[g] < 0
            if leaf.all(): break
            go = Z[rows, np.maximum(FEAT[g], 0)] <= THR[g]; node = np.where(leaf, node, np.where(go, LEFT[g], RIGHT[g]))
        P += VALUE[o + node]
    g = np.array(GRADES)[CLASSES[P.argmax(1)].astype(int)]; return g.astype(float), g
print(f'random forest: {len(OFFSET)} trees; features: {", ".join(FEATURES)}')""",
'xgb': r"""z = np.load(MODEL_FILE, allow_pickle=False); FEATURES = [str(f) for f in z['features']]; MU, SD = z['mu'], z['sd']
FEAT, THR, YES, NO, LEAF, ISLEAF, OFFSET, BASE = z['feat'], z['thr'], z['yes'], z['no'], z['leaf'], z['isleaf'], z['offset'], float(z['base'][0])
def predict(S):
    # spectra -> severity score: base score + sum of the leaf values of all boosted trees (XGBoost), clipped to 0-9
    Z = ((features(make_variant(S, VARIANT), FEATURES, OP) - MU) / SD).astype(np.float32); n = len(Z); rows = np.arange(n); v = np.full(n, BASE)
    for o in OFFSET:
        node = np.zeros(n, int)
        while True:
            g = o + node; lf = ISLEAF[g]
            if lf.all(): break
            go = Z[rows, FEAT[g]] < THR[g]; node = np.where(lf, node, np.where(go, YES[g], NO[g]))
        v += LEAF[o + node]
    v = np.clip(v, 0, 9); return v, v
print(f'XGBoost: {len(OFFSET)} trees, base score {BASE:.4f}; features: {", ".join(FEATURES)}')""",
'convnext': r"""W = torch.load(MODEL_FILE, map_location='cpu', weights_only=True); FEATURES = W['features']; MU, SD = np.array(W['scaler_mean']), np.array(W['scaler_sd'])
NET = ConvNeXtV2Atto(W['n_out']); NET.load_state_dict(W['state_dict']); NET.eval().to(DEVICE); torch.set_num_threads(max(1, os.cpu_count() or 1))
def predict(S):
    # spectra -> features -> k x k pseudo-image -> ConvNeXt V2-Atto
    Z = ((features(make_variant(S, VARIANT), FEATURES, OP) - MU) / SD).astype(np.float32); outs = []
    with torch.no_grad():
        for i in range(0, len(Z), BATCH): outs.append(NET(torch.from_numpy(pseudo(Z[i:i + BATCH])).to(DEVICE)).cpu().numpy())
    return OUTPUT(np.concatenate(outs))
print(f'ConvNeXt V2-Atto: {sum(p.numel() for p in NET.parameters()):,} parameters; features: {", ".join(FEATURES)}')""",
'dnn': r"""W = torch.load(MODEL_FILE, map_location='cpu', weights_only=True); FEATURES = W['features']; MU, SD = np.array(W['scaler_mean']), np.array(W['scaler_sd'])
NET = DNNF1(len(FEATURES), W['n_out']); NET.load_state_dict(W['state_dict']); NET.eval().to(DEVICE); torch.set_num_threads(max(1, os.cpu_count() or 1))
def predict(S):
    # spectra -> features -> fully connected network DNN-F1
    Z = ((features(make_variant(S, VARIANT), FEATURES, OP) - MU) / SD).astype(np.float32); outs = []
    with torch.no_grad():
        for i in range(0, len(Z), BATCH): zb = Z[i:i + BATCH]; outs.append(NET(torch.from_numpy(zb.reshape(-1, 1, 1, zb.shape[1])).to(DEVICE)).cpu().numpy())
    return OUTPUT(np.concatenate(outs))
print(f'DNN-F1: {sum(p.numel() for p in NET.parameters()):,} parameters; features: {", ".join(FEATURES)}')"""}
OUTPUT = {'A': r"""def OUTPUT(o):   # detection: softmax probability of 'diseased' and class (probability >= THRESHOLD)
    p = np.exp(o - o.max(1, keepdims=True)); p /= p.sum(1, keepdims=True); return p[:, 1], (p[:, 1] >= THRESHOLD).astype(int)""",
          'B': r"""def OUTPUT(o):   # six grades: class with the largest output -> grade 0, 1, 3, 5, 7 or 9
    g = np.array(GRADES)[o.argmax(1)]; return g.astype(float), g""",
          'C': r"""def OUTPUT(o):   # severity score, clipped to 0-9
    v = np.clip(o.ravel(), 0, 9); return v, v"""}

def notebook(m):
    key = '%s_%s' % (m['task'], m['model'].replace(' ', '_')); kind, task = m['kind'], m['task']; dl = kind in ('convnext', 'dnn')
    cells = []; add = lambda k, t: cells.append((k, t.strip('\n')))
    acc = '%s %.3f%s' % ('macro-F1' if task != 'C' else 'R²', m['uav_value'], (', AUC %.2f' % m['uav_auc']) if m.get('uav_auc') else '')
    if key == 'A_ConvNeXt_V2-Atto': use = 'This is the **recommended map**: the only model that transferred beyond chance to the 48 UAV plots (maximum-statistic permutation p = %.3f; Westfall and Young, 1993).' % MNB.MX.loc['A', 'p_value']
    elif task == 'A': use = 'On the 48 UAV plots this model was at chance level, so read the map as what the best leaf model predicts, not as validated detection; the recommended detection map is ConvNeXt V2-Atto.'
    else: use = 'On the 48 UAV plots this model was below chance, so the map is **not validated** and must not be read as severity – it shows what the leaf model predicts.'
    out_txt = {'A': '`%s_score` (probability of white rust%s) and `%s_class` (1 healthy, 2 diseased)' % (key, '; SVM: decision value, > 0 = diseased' if kind == 'svm' else '', key),
               'B': '`%s` (predicted grade 0, 1, 3, 5, 7 or 9)' % key, 'C': '`%s` (predicted severity score 0–9)' % key}[task]
    add('markdown', f"""# White rust pixel map – {m['model']}, task {task}: {TASKN[task]}
UAV hyperspectral image of 24 February 2026 · model trained on the 2025-26 ASD leaf spectra (leave-one-replication-out evaluation)

| Item | This notebook |
|---|---|
| Model | **{m['model']}** ({'deep learning' if dl else 'machine learning'}), file `{m['file']}` |
| Why this model | {m['why']} |
| Input given to the model | {m['variant']}: {VARN[m['variant']]} |
| Features (computed from each pixel spectrum) | {', '.join(m['features'])} |
| Accuracy on the 48 UAV plot spectra | {acc} |
| Output rasters | {out_txt} – ENVI `.dat/.hdr`, GeoTIFF (if `rasterio` is installed) and a PNG map |

{use}

**Steps.** 0 install packages · 1 settings · 2 libraries and image helpers{' · 3 network' if dl else ''} · {'4' if dl else '3'} reference data · features · load the model · self-check on the 48 plot means · open the image and crop mask · pixel loop · map · per-plot accuracy · outputs.

**Requirements.** Python 3.9+, `numpy`, `scipy`, `pandas`, `matplotlib`{', `torch` (CPU: `pip install torch --index-url https://download.pytorch.org/whl/cpu`)' if dl else ''}; optional `rasterio` for GeoTIFF.{'' if dl else ' The model is stored as plain arrays and predicted with NumPy exactly as scikit-learn/xgboost do, so their versions do not matter.'}
**Time.** Run first with `SPATIAL_STEP = 4` (preview, about 1/16 of the pixels), then `SPATIAL_STEP = 1` for the final map.""")
    add('markdown', '## 0 Install the packages (run once)\nRun this cell once. If it installs something new, restart the kernel (menu *Kernel → Restart*) and continue with step 1. Later runs can skip it.')
    add('code', "%pip install -q numpy scipy pandas matplotlib rasterio" + ("\n%pip install -q torch --index-url https://download.pytorch.org/whl/cpu" if dl else ''))
    add('markdown', '## 1 Settings\nYour paths are already filled in. The results go to a sub-folder of `OUT_DIR` named after the model. If the model file is not found at `MODEL_FILE`, the notebook also looks in a `models` folder next to the notebook.')
    add('code', f"""# ============================ SETTINGS ============================
HDR_FILE  = r'D:\\Coalighned\\24_02_2026\\subset_200526.hdr'          # ENVI header of the 24 Feb image (the data file 'subset_200526', ~9 GB, must be next to it)
DATA_NAME = 'subset_200526'                                         # name of the image data file
ROI_FILE  = r'D:\\Coalighned\\24_02_2026\\48_plot_roi_new.xml'        # 48 plot ROIs, ROI #n = plot n (None = skip the per-plot accuracy)
OUT_DIR   = r'C:\\Users\\BDI LAB\\Desktop\\ASD_MODEL_ON_240226_UAV_IMAGE_PIXELWISE\\IMAGE_VALIDATED'   # your output folder
MODEL_FILE = r'C:\\Users\\BDI LAB\\Desktop\\ASD_MODEL_ON_240226_UAV_IMAGE_PIXELWISE\\models\\{m['file']}'   # this model (from the kit's 'models' folder)
PLOT_AVG_FILE = r'D:\\Coalighned\\24_02_2026\\envi_plot_avg.txt'      # ENVI plot-average file for the self-check (skipped if the file is not there)
OUT_NAME  = '{key}'                                                 # sub-folder of OUT_DIR for this model's results

SPATIAL_STEP = 4        # 4 = quick preview; 1 = final full-resolution map
BLOCK_ROWS   = 16       # image rows processed at a time (reduce if memory is short)
NDVI_MIN     = 0.6      # crop mask: NDVI(898, 684) > 0.6 as in the methodology
REFLECTANCE_SCALE = 'auto'  # 'auto' (divides by 10000 if the data look like 0-10000) or a number""" +
        ('\nTHRESHOLD    = 0.5      # probability above which a pixel is called diseased\nPLOT_DISEASED_SHARE = 0.5   # a plot is called diseased if more than this share of its crop pixels is diseased' if task == 'A' and kind != 'svm' else '') +
        ('\nPLOT_DISEASED_SHARE = 0.5   # a plot is called diseased if more than this share of its crop pixels is diseased (SVM: decision value > 0 = diseased)' if kind == 'svm' else '') +
        ('\nBATCH  = 32768          # pixels per network batch\nDEVICE = \'cpu\'' if dl else ''))
    add('markdown', '## 2 Libraries and image helpers\nThe image is memory-mapped: only the rows being processed are read, so a 9 GB image runs in a few GB of memory. The ROI parser converts the plot polygons from map coordinates to image pixels.')
    libs = LIBS.replace("    DATA_FILE", "    DATA_FILE")
    libs = libs.replace("OUT = os.path.join(SRC, OUT_NAME); os.makedirs(OUT, exist_ok=True); MODEL_DIR = os.path.join(KIT_DIR, 'models')", MODEL_FIND)
    if not dl: libs = libs.replace("import torch, torch.nn as nn, torch.nn.functional as Fn\n", "")
    assert 'MODEL_DIR' not in libs
    add('code', libs)
    if dl:
        add('markdown', '## 3 Network\n' + ('ConvNeXt V2-Atto (Woo et al., 2023) with stride-1 stems for the small pseudo-image: the standardised features are written into a k × k grid (zero-padded; Sharma et al., 2019) – the same architecture as in the ASD analysis.' if kind == 'convnext' else 'DNN-F1: fully connected network on the standardised feature vector (64 → 32 → output, batch normalisation, ReLU) – the same architecture as in the ASD analysis.'))
        add('code', CNX_TXT if kind == 'convnext' else DNN_TXT)
    n0 = 4 if dl else 3
    add('markdown', f"## {n0} Reference data (from `{key}_reference.json` next to the model file)\n`ASD_HEALTHY` = mean of the healthy ASD leaves of 24 Feb at the image wavelengths, `UAV_HEALTHY` = mean of the 12 sprayed plots of this image; their ratio is the healthy-reference gain used by the *corrected* and *normalised* inputs (empirical-line idea; Smith and Milton, 1999; brightness normalisation: Barnes et al., 1989). `TRUTH` = ASD leaf scores of 24 Feb per plot. `EXPECTED` = this model's prediction for the 48 plot-mean spectra (self-check).")
    REFD = dict(REF_WL=[float(x) for x in MNB.SC.wavelength], ASD_HEALTHY=[float(x) for x in MNB.SC['ASD healthy (24 Feb)']], UAV_HEALTHY=[float(x) for x in MNB.SC['UAV healthy']],
                TRUTH=dict(plot=[int(x) for x in MNB.GT['plot']], block=list(MNB.GT.block), status=list(MNB.GT.status), variety=list(MNB.GT.variety), sowing=list(MNB.GT.sowing),
                           mean_score=[round(float(x), 4) for x in MNB.GT.score], grade=[int(x) for x in MNB.GT.grade], PDI=[round(float(x), 3) for x in MNB.GT.PDI]),
                MODEL={k: m[k] for k in ('task', 'model', 'why', 'variant', 'uav_metric', 'uav_value', 'uav_auc', 'file', 'kind', 'features')}, EXPECTED=EXPECTED[key])
    json.dump(REFD, open(HERE + 'kit/models/%s_reference.json' % key, 'w'))
    add('code', """REF_FILE = os.path.splitext(MODEL_FILE)[0] + '_reference.json'     # reference data, stored next to the model file
assert os.path.isfile(REF_FILE), f'Reference file not found: {REF_FILE} (copy it from the kit folder models)'
R = json.load(open(REF_FILE))
REF_WL, ASD_HEALTHY, UAV_HEALTHY = np.array(R['REF_WL']), np.array(R['ASD_HEALTHY']), np.array(R['UAV_HEALTHY'])
TRUTH = pd.DataFrame(R['TRUTH']); MODEL = R['MODEL']; EXPECTED = R['EXPECTED']
GRADES = [0, 1, 3, 5, 7, 9]; KEY, TASK, VARIANT = '%s', MODEL['task'], MODEL['variant']
assert len(REF_WL) == len(WL) and np.abs(REF_WL - WL).max() < 0.01, 'the image wavelengths differ from the 24 Feb image used to build the model inputs'
GAIN = ASD_HEALTHY / UAV_HEALTHY; TARGET_MEAN = ASD_HEALTHY.mean()
print(f"{MODEL['model']} – task {TASK}, input '{VARIANT}', accuracy on the 48 UAV plots: {MODEL['uav_metric']} {MODEL['uav_value']:.3f}")""" % key)
    add('markdown', f"## {n0 + 1} Features – identical to the ASD pipeline\nFor every pixel: (1) the input variant; (2) resampling to 1 nm, 350–2500 nm (gaps bridged linearly); (3) Savitzky–Golay smoothing / first derivative (window 11, order 2; Savitzky and Golay, 1964); (4) the model's features: first derivatives FD at given wavelengths, red-edge position REP and amplitude Dr (680–760 nm; Horler et al., 1983; Filella and Peñuelas, 1994), DWSI-2 = R1660/R550 (Apan et al., 2004), MCARI (Daughtry et al., 2000). Steps 2–3 are linear and are combined into one matrix evaluated only at the needed wavelengths – the same values as the ASD code, fast and light on memory.")
    add('code', FEAT)
    add('markdown', f"## {n0 + 2} Load the model\n" + ('Weights are loaded safely (`weights_only=True`); inputs are standardised with the training mean and SD stored in the file.' if dl else 'Arrays from the `.npz` file; the prediction below reproduces scikit-learn/xgboost exactly. Inputs are standardised with the training mean and SD stored in the file.'))
    add('code', (OUTPUT[task] + '\n' if dl else '') + LOAD[kind] + '\nOP = build_operator(FEATURES)')
    add('markdown', f"## {n0 + 3} Self-check on the 48 plot-mean spectra\nThe model predicts the 48 plot means of the ENVI plot-average file; the result must agree with `EXPECTED` (computed when this notebook was built). A maximum difference below 0.001 means your computer reproduces the analysis exactly.")
    add('code', r"""if PLOT_AVG_FILE and os.path.exists(PLOT_AVG_FILE):
    L = open(PLOT_AVG_FILE).read().splitlines(); nh = sum(l.startswith('Column') for l in L)
    A = np.array([[float(x) for x in l.split()] for l in L[nh + 1:] if l.strip()])
    assert np.abs(A[:, 0] - WL).max() < 0.01, 'plot-average wavelengths differ from the image'
    d = np.abs(predict(A[:, 1:].T.astype(np.float32))[0] - np.array(EXPECTED)).max()
    print(f'self-check: max difference {d:.2e}', '-> OK' if d < 1e-3 else '-> CHECK library versions')
else:
    print('self-check skipped (no plot-average file)')""")
    add('markdown', f"## {n0 + 4} Open the image and build the crop mask\nPixels outside the field are 0 in the masked image. A pixel is used when its reflectance is valid and NDVI = (R898 − R684)/(R898 + R684) > `NDVI_MIN`. Reflectance is rescaled automatically if stored as 0–10000.")
    add('code', OPEN)
    add('markdown', f"## {n0 + 5} Pixel loop\nThe image is read `BLOCK_ROWS` rows at a time; for the crop pixels of each block the model computes its input, features and prediction. Values are NaN outside the crop.")
    write = {'A': """cls = np.zeros((NL, NS), np.uint8); cls[CROP] = 1; cls[(LAB == 1) & CROP] = 2
write_envi(base + '_score.dat', VAL, '%s', 4, {'data ignore value': 'NaN'})
write_envi(base + '_class.dat', cls, 'class (0 outside, 1 healthy, 2 diseased)', 1, {'file type': 'ENVI Classification', 'classes': 3, 'class names': '{outside, healthy, diseased}', 'class lookup': '{0 0 0, 26 152 80, 215 48 39}'})
tif = write_tif(base + '_class.tif', cls, 0) and write_tif(base + '_score.tif', VAL, np.nan)""" % ('SVM decision value' if kind == 'svm' else 'probability of white rust'),
             'B': "write_envi(base + '.dat', VAL, 'grade (0-9)', 4, {'data ignore value': 'NaN'}); tif = write_tif(base + '.tif', VAL, np.nan)",
             'C': "write_envi(base + '.dat', VAL, 'severity score (0-9)', 4, {'data ignore value': 'NaN'}); tif = write_tif(base + '.tif', VAL, np.nan)"}[task]
    add('code', r"""VAL = np.full((NL, NS), np.nan, np.float32); LAB = np.full((NL, NS), np.nan, np.float32); CROP = np.zeros((NL, NS), bool); t0 = time.time(); n_crop = 0
for r0 in range(0, cube.nl, BLOCK_ROWS * ST):
    r1 = min(cube.nl, r0 + BLOCK_ROWS * ST); blk = cube.rows(r0, r1, ST) / SCALE
    nd = (blk[..., bi(898)] - blk[..., bi(684)]) / (blk[..., bi(898)] + blk[..., bi(684)] + 1e-12)
    valid = np.isfinite(blk).all(2) & (blk[..., bi(800)] > 0) & (blk.mean(2) > 0) & (nd > NDVI_MIN)
    i0 = r0 // ST; nr = blk.shape[0]
    if valid.any():
        S = blk[valid]; CROP[i0:i0 + nr][valid] = True; n_crop += len(S)
        v, l = predict(S); VAL[i0:i0 + nr][valid] = v; LAB[i0:i0 + nr][valid] = l
    if (r0 // (BLOCK_ROWS * ST)) % 20 == 0 or r1 == cube.nl:
        el = time.time() - t0; print(f'rows {r1}/{cube.nl}  crop pixels {n_crop:,}  {el / 60:.1f} min  ETA {el / r1 * (cube.nl - r1) / 60:.1f} min')
base = os.path.join(OUT, KEY)
""" + write + r"""
print(f'done: {n_crop:,} crop pixels in {(time.time() - t0) / 60:.1f} min; GeoTIFF written: {bool(tif)}')""")
    add('markdown', f"## {n0 + 6} Map\nPlot outlines and numbers are drawn from the ROI file. The title carries the model's accuracy on the 48 UAV plots so that an unreliable map is recognised at once.")
    draw = {'A': (("im = ax.imshow(VAL, cmap='RdYlGn_r', vmin=-2, vmax=2, interpolation='nearest'); lab = 'SVM decision value (> 0 = diseased)'" if kind == 'svm' else
                   "im = ax.imshow(VAL, cmap='RdYlGn_r', vmin=0, vmax=1, interpolation='nearest'); lab = 'probability of white rust'") + "\nttl = f\"{MODEL['model']} detection ({VARIANT} input; {tag})\""),
            'B': "GCM = ListedColormap(['#1A9850', '#FEE08B', '#FDAE61', '#F46D43', '#D73027', '#7F0000']); GNORM = BoundaryNorm([-0.5, 0.5, 2, 4, 6, 8, 9.5], 6)\nim = ax.imshow(VAL, cmap=GCM, norm=GNORM, interpolation='nearest'); lab = 'grade'\nttl = f\"{MODEL['model']} six grades ({VARIANT} input; {tag}; NOT validated)\"",
            'C': "im = ax.imshow(VAL, cmap='YlOrRd', vmin=0, vmax=9, interpolation='nearest'); lab = 'score (0-9)'\nttl = f\"{MODEL['model']} severity score ({VARIANT} input; {tag}; NOT validated)\""}[task]
    cls_panel = r"""
cls = np.where(CROP, 1 + (LAB == 1), np.nan)
axs[1].imshow(cls, cmap=ListedColormap(['#1A9850', '#D73027']), vmin=1, vmax=2, interpolation='nearest'); outline(axs[1]); axs[1].set_xticks([]); axs[1].set_yticks([])
axs[1].set_xlim(-0.5, NS - 0.5); axs[1].set_ylim(NL - 0.5, -0.5)
axs[1].set_title('class map (red = diseased)', fontsize=9)
axs[1].legend(handles=[matplotlib.patches.Patch(color='#1A9850', label='healthy'), matplotlib.patches.Patch(color='#D73027', label='diseased')], loc='lower right', fontsize=8)""" if task == 'A' else ''
    add('code', r"""PLOTS = read_roi_xml(ROI_FILE) if ROI_FILE and os.path.exists(ROI_FILE) else {}
def outline(ax, numbers=True):
    for p, polys in PLOTS.items():
        for pg in polys: ax.plot((pg[:, 0] - 0.5) / ST, (pg[:, 1] - 0.5) / ST, color='k', lw=0.4)
        if numbers: c = (np.vstack(polys).mean(0) - 0.5) / ST; ax.text(c[0], c[1], str(p), fontsize=5, ha='center', va='center')
tag = f"UAV {MODEL['uav_metric'].replace('macro_F1', 'macro-F1').replace('R2', 'R²')} {MODEL['uav_value']:.2f}"
fig, axs = plt.subplots(1, NPANEL, figsize=(8 * NPANEL + 1, 8 * NL / NS + 1), squeeze=False); axs = axs.ravel(); ax = axs[0]
""".replace('NPANEL', '2' if task == 'A' else '1') + draw + r"""
ax.set_xlim(-0.5, NS - 0.5); ax.set_ylim(NL - 0.5, -0.5); outline(ax); ax.set_xticks([]); ax.set_yticks([]); ax.set_title(ttl, fontsize=9); plt.colorbar(im, ax=ax, fraction=0.03, label=lab)""" + cls_panel + r"""
fig.tight_layout(); fp = os.path.join(OUT, KEY + '_map.png'); fig.savefig(fp, dpi=300); plt.close(fig); show(fp)""")
    add('markdown', f"## {n0 + 7} Per-plot accuracy\nFor each plot ROI: crop pixels inside the image and the plot value of the map, compared with the ASD leaf scores of 24 Feb. " +
        {'A': 'Detection: plot diseased if more than `PLOT_DISEASED_SHARE` of its pixels are diseased; confusion counts, sensitivity, specificity, balanced accuracy (Congalton, 1991).',
         'B': 'Grades: median predicted grade vs the plot grade (exact and within one grade).',
         'C': 'Score: mean predicted score vs the plot mean leaf score (R², RMSE, Pearson r).'}[task] +
        ' Plots 1 and 48 extend slightly beyond the image (95% and 89% of the plot inside); only their pixels inside the image are used.')
    stat = {'A': "        r.update(share_diseased=float((l == 1).mean()) if len(l) else np.nan, mean_value=float(np.nanmean(v)) if len(v) else np.nan)",
            'B': "        r.update(median_grade=float(np.median(v)) if len(v) else np.nan, mean_grade=float(np.nanmean(v)) if len(v) else np.nan)",
            'C': "        r.update(mean_score_pred=float(np.nanmean(v)) if len(v) else np.nan)"}[task]
    summ = {'A': """    PS['mapped_diseased'] = (PS.share_diseased > PLOT_DISEASED_SHARE).astype(int); t = (PS.status == 'Diseased').astype(int)
    tp, tn = int(((t == 1) & (PS.mapped_diseased == 1)).sum()), int(((t == 0) & (PS.mapped_diseased == 0)).sum()); fp, fn = int(((t == 0) & (PS.mapped_diseased == 1)).sum()), int(((t == 1) & (PS.mapped_diseased == 0)).sum())
    sens, spec = tp / max(1, tp + fn), tn / max(1, tn + fp)
    S_ = dict(TP=tp, TN=tn, FP=fp, FN=fn, overall_accuracy=(tp + tn) / len(PS), sensitivity=sens, specificity=spec, balanced_accuracy=(sens + spec) / 2, r_with_score=PS[['share_diseased', 'mean_score']].corr().iloc[0, 1])""",
            'B': """    gp = np.array([GRADES.index(min(GRADES, key=lambda g: abs(g - x))) for x in PS.median_grade]); gt = np.array([GRADES.index(int(x)) for x in PS.grade])
    S_ = dict(exact=float(np.mean(gp == gt)), within_one=float(np.mean(np.abs(gp - gt) <= 1)), r_with_score=PS[['mean_grade', 'mean_score']].corr().iloc[0, 1])""",
            'C': """    e = PS.mean_score_pred - PS.mean_score
    S_ = dict(R2=1 - (e ** 2).sum() / ((PS.mean_score - PS.mean_score.mean()) ** 2).sum(), RMSE=float(np.sqrt((e ** 2).mean())), r_with_score=PS[['mean_score_pred', 'mean_score']].corr().iloc[0, 1])"""}[task]
    add('code', """if PLOTS:
    yy, xx = np.mgrid[0:NL, 0:NS]; cx, cy = xx * ST + 0.5, yy * ST + 0.5; rows = []
    for p, polys in PLOTS.items():
        mk = np.zeros((NL, NS), bool)
        for pg in polys:
            sel = (cx >= pg[:, 0].min()) & (cx <= pg[:, 0].max()) & (cy >= pg[:, 1].min()) & (cy <= pg[:, 1].max())
            if sel.any(): mk[sel] |= MplPath(pg).contains_points(np.column_stack([cx[sel], cy[sel]]))
        mk &= CROP; v, l = VAL[mk], LAB[mk]; r = dict(plot=p, crop_pixels=int(mk.sum()))
""" + stat + """
        rows.append(r)
    PS = pd.DataFrame(rows).merge(TRUTH, on='plot', how='left'); PS = PS[PS.crop_pixels > 0]
""" + summ + """
    PS.to_csv(os.path.join(OUT, KEY + '_per_plot.csv'), index=False); pd.DataFrame([dict(model=KEY, plots=len(PS), **S_)]).to_csv(os.path.join(OUT, KEY + '_accuracy.csv'), index=False)
    print(PS.head(12).round(3).to_string(index=False)); print('...'); print(pd.Series(S_).round(3).to_string())
else:
    print('per-plot accuracy skipped (no ROI file)')""")
    add('markdown', f"## {n0 + 8} Outputs\nIn the results folder: the rasters ({out_txt}), `{key}_map.png`, `{key}_per_plot.csv`, `{key}_accuracy.csv` and `run_info.json`. Open the `.dat/.hdr` or `.tif` in ENVI/QGIS – they carry the georeference of the image.\n\n**References.** Apan et al. (2004); Barnes et al. (1989); Congalton (1991); Daughtry et al. (2000); Filella and Peñuelas (1994); Horler et al. (1983); Savitzky and Golay (1964); Sharma et al. (2019); Smith and Milton (1999); Westfall and Young (1993); Woo et al. (2023) – full entries in the transfer report.")
    add('code', r"""info = dict(model=KEY, image=DATA_FILE, spatial_step=ST, grid=[NS, NL], crop_pixels=int(n_crop), input=VARIANT, features=FEATURES, ndvi_min=NDVI_MIN, reflectance_scale=SCALE, minutes=round((time.time() - t0) / 60, 1))
json.dump(info, open(os.path.join(OUT, 'run_info.json'), 'w'), indent=1)
print('results in', OUT); print('\n'.join(sorted(os.listdir(OUT))))""")
    nb = dict(nbformat=4, nbformat_minor=5, metadata=dict(kernelspec=dict(display_name='Python 3', language='python', name='python3'), language_info=dict(name='python')), cells=[])
    for i, (k, t) in enumerate(cells):
        c = dict(cell_type=k, id='c%02d' % i, metadata={}, source=[l + '\n' for l in t.split('\n')]); c['source'][-1] = c['source'][-1].rstrip('\n')
        if k == 'code': c.update(execution_count=None, outputs=[])
        nb['cells'].append(c)
    fn = OUTD + '%s_pixel_map_24Feb2026.ipynb' % key; json.dump(nb, open(fn, 'w'), indent=1); return fn, key
if __name__ == '__main__':
    files = [notebook(m) for m in MNB.MT]
    for f, k in files: print('written', os.path.basename(f))
