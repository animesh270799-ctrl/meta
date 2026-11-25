"""Pixel-map notebook for the LORO random-forest DETECTION model (ALL_model/A_detection_RF.joblib, refitted on all 2330 leaves).
Direct UAV reflectance (its best input on the 48 UAV plots: macro-F1 0.621, AUC 0.613, OA 0.750). Uses A_detection_RF.npz (same model as plain
arrays, identical predictions, any scikit-learn version) when it is next to the .joblib, otherwise loads the .joblib with scikit-learn.
Composed from the tested per-model notebooks (B_RF standalone for the reader/features, A_ConvNeXt for the detection map and accuracy).
Output: uavp/kit/per_model/A_detection_RF_pixel_map_24Feb2026.ipynb"""
import json, os, copy
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'; PM = HERE + 'kit/per_model/'
RF = json.load(open(PM + 'B_RF_pixel_map_24Feb2026_STANDALONE.ipynb')); CX = json.load(open(PM + 'A_ConvNeXt_V2-Atto_pixel_map_24Feb2026.ipynb'))
EXP = json.load(open('/tmp/claude-0/-home-user-meta/c5704ca0-f1ca-5695-b9e0-a810fbe166a9/scratchpad/A_RF_expected.json'))
src = lambda c: ''.join(c['source'])
def cell(kind, t):
    c = dict(cell_type=kind, metadata={}, source=[l + '\n' for l in t.split('\n')]); c['source'][-1] = c['source'][-1].rstrip('\n')
    if kind == 'code': c.update(execution_count=None, outputs=[])
    return c
def pick(nb, head):          # (markdown cell starting with head, the code cell after it)
    for i, c in enumerate(nb['cells']):
        if c['cell_type'] == 'markdown' and src(c).startswith(head): return copy.deepcopy(c), copy.deepcopy(nb['cells'][i + 1])
    raise KeyError(head)
P = 'C:\\Users\\BDI LAB\\Desktop\\ASD_MODEL_ON_240226_UAV_IMAGE_PIXELWISE'
title = cell('markdown', """# White rust pixel map – Random forest, task A: detection (healthy / diseased)
UAV hyperspectral image of 24 February 2026 · model `A_detection_RF.joblib` (random forest, 500 trees, refitted on all 2330 ASD leaf spectra of 2025-26 after leave-one-replication-out evaluation)

| Item | This notebook |
|---|---|
| Model | **Random forest** (machine learning), `ALL_model\\A_detection_RF.joblib`; the same model as plain arrays in `A_detection_RF.npz` |
| Input given to the model | direct UAV reflectance (its best input on the 48 UAV plots) |
| Features (computed from each pixel spectrum) | FD1090, FD1060, FD550, FD1660, FD1245, FD870, FD760, FD595, REP (candidates also FD665, DWSI-2) |
| Accuracy on the 48 UAV plot spectra | macro-F1 0.621, AUC 0.613, overall accuracy 0.750 |
| Output rasters | `A_detection_RF_score` (probability of white rust) and `A_detection_RF_class` (1 healthy, 2 diseased) – ENVI `.dat/.hdr`, GeoTIFF (if `rasterio` is installed) and a PNG map |

On the 48 UAV plots this model was only slightly better than chance, so read the map as what the leaf model predicts, not as validated detection.

**Model file.** The `.joblib` loads only with the scikit-learn version it was saved with (1.9.1). If `A_detection_RF.npz` is in the same folder, the notebook uses it instead: identical predictions with plain NumPy, any scikit-learn version.

**Steps.** 0 install packages · 1 settings · 2 libraries and image helpers · 3 reference data · 4 features · 5 load the model · 6 self-check · 7 open the image · 8 pixel loop · 9 map · 10 per-plot accuracy · 11 outputs.
**Time.** Run first with `SPATIAL_STEP = 4` (preview), then `SPATIAL_STEP = 1` for the final map.""")
md0, c0 = pick(RF, '## 0 Install'); md1, c1 = pick(RF, '## 1 Settings'); md2, c2 = pick(RF, '## 2 Libraries'); md4, c4 = pick(RF, '## 4 Features')
md6, c6 = pick(RF, '## 6 Self-check'); md7, c7 = pick(RF, '## 7 Open the image'); md11, c11 = pick(RF, '## 11 Outputs')
md8, c8 = pick(CX, '## 9 Pixel loop'); md9, c9 = pick(CX, '## 10 Map'); md10, c10 = pick(CX, '## 11 Per-plot accuracy')
for m_, n_ in ((md8, '8'), (md9, '9'), (md10, '10')):
    s = src(m_); s = '## ' + n_ + s[s.index(' ', 3):]; m_['source'] = cell('markdown', s)['source']
md1 = cell('markdown', '## 1 Settings\nYour paths are filled in. `MODEL_FILE` is your RF detection model; `NPZ_FILE` is the same model as plain arrays – it is in the same `RF` folder and is used automatically, so the Python / scikit-learn version does not matter.')
c1 = cell('code', f"""# ============================ SETTINGS ============================
HDR_FILE  = r'D:\\Coalighned\\24_02_2026\\subset_200526.hdr'          # ENVI header of the 24 Feb image (the data file 'subset_200526', ~9 GB, must be next to it)
DATA_NAME = 'subset_200526'                                         # name of the image data file
ROI_FILE  = r'D:\\Coalighned\\24_02_2026\\48_plot_roi_new.xml'        # 48 plot ROIs, ROI #n = plot n (None = skip the per-plot accuracy)
OUT_DIR   = r'{P}\\IMAGE_VALIDATED'   # your output folder
MODEL_FILE = r'{P}\\RF\\A_detection_RF.joblib'   # RF detection model (scikit-learn joblib)
NPZ_FILE   = r'{P}\\RF\\A_detection_RF.npz'      # same model as plain arrays: used if present (works with any Python / scikit-learn version)
PLOT_AVG_FILE = r'D:\\Coalighned\\24_02_2026\\envi_plot_avg.txt'      # ENVI plot-average file for the self-check (skipped if the file is not there)
OUT_NAME  = 'A_detection_RF'                                         # sub-folder of OUT_DIR for this model's results

SPATIAL_STEP = 4        # 4 = quick preview; 1 = final full-resolution map
BLOCK_ROWS   = 16       # image rows processed at a time (reduce if memory is short)
NDVI_MIN     = 0.6      # crop mask: NDVI(898, 684) > 0.6 as in the methodology
REFLECTANCE_SCALE = 'auto'  # 'auto' (divides by 10000 if the data look like 0-10000) or a number
THRESHOLD    = 0.5      # probability above which a pixel is called diseased (0.5 = the random forest's own decision)
PLOT_DISEASED_SHARE = 0.5   # a plot is called diseased if more than this share of its crop pixels is diseased""")
s2 = src(c2); a = s2.index("_mf = os.path.basename("); b = s2.index("print('model file  :', MODEL_FILE); print('results to  :', OUT)")
s2 = s2[:a] + "if not (os.path.isfile(NPZ_FILE) or os.path.isfile(MODEL_FILE)):\n    raise FileNotFoundError('Neither the model file nor the .npz was found:\\n  ' + MODEL_FILE + '\\n  ' + NPZ_FILE + '\\nCheck MODEL_FILE / NPZ_FILE in step 1.')\nprint('model file  :', NPZ_FILE if os.path.isfile(NPZ_FILE) else MODEL_FILE); print('results to  :', OUT)\nimport sys, scipy; print('python', sys.version.split()[0], '| numpy', np.__version__, '| scipy', scipy.__version__, '| pandas', pd.__version__)" + s2[b + len("print('model file  :', MODEL_FILE); print('results to  :', OUT)"):]
c2['source'] = cell('code', s2)['source']
R = json.load(open(HERE + 'kit/models/B_RF_reference.json')); T = R['TRUTH']
md3 = cell('markdown', "## 3 Reference data (embedded)\n`TRUTH` = ASD leaf scores of 24 Feb 2026 for the 48 plots; `EXPECTED` = this model's probability of white rust for the 48 plot-mean spectra (self-check). The model uses the UAV reflectance **directly**, so no reference spectra are needed.")
c3 = cell('code', "# ASD leaf scores of 24 Feb 2026 for the 48 plots (plot = ROI number)\n"
          "TRUTH = pd.DataFrame({'plot': %s,\n" % T['plot'] + "    'block': %s,\n" % json.dumps(T['block']) + "    'status': %s,\n" % json.dumps(T['status']) +
          "    'variety': %s,\n" % json.dumps(T['variety']) + "    'sowing': %s,\n" % json.dumps(T['sowing']) + "    'mean_score': %s,\n" % json.dumps(T['mean_score']) +
          "    'grade': %s,\n" % json.dumps(T['grade']) + "    'PDI': %s})\n" % json.dumps(T['PDI']) +
          "# this model's probability of white rust for the 48 plot-mean spectra (used by the self-check)\nEXPECTED = %s\n" % json.dumps(EXP) +
          "MODEL = dict(task='A', model='Random forest', variant='direct', uav_metric='macro_F1', uav_value=0.6213)\n"
          "GRADES = [0, 1, 3, 5, 7, 9]; KEY, TASK, VARIANT = 'A_detection_RF', MODEL['task'], MODEL['variant']\n"
          "assert len(WL) == 483 and abs(WL[0] - 399.38) < 0.5 and abs(WL[-1] - 2397.55) < 0.5, 'the image bands differ from the 24 Feb image the model inputs were built for'\n"
          "print(f\"{MODEL['model']} detection – input '{VARIANT}' (reflectance used as it is), accuracy on the 48 UAV plots: macro-F1 0.621, AUC 0.613, overall accuracy 0.750\")")
md5 = cell('markdown', '## 5 Load the model\nWith `A_detection_RF.npz`: the 500 trees as plain arrays, predicted with NumPy exactly as scikit-learn does (average of the class proportions of the reached leaves). Without it: the `.joblib` is loaded with scikit-learn. Inputs are standardised with the training mean and SD stored with the model; the model uses 9 of its 11 candidate features.')
c5 = cell('code', r"""if os.path.isfile(NPZ_FILE):
    z = np.load(NPZ_FILE, allow_pickle=False); FEATURES = [str(f) for f in z['features']]; IDX = z['idx']; MU, SD = z['mu'], z['sd']
    LEFT, RIGHT, FEAT, THR, VALUE, OFFSET = z['left'], z['right'], z['feat'], z['thr'], z['value'], z['offset']
    def proba(Zs):
        # every pixel is routed through every tree; the class proportions of the reached leaves are averaged (scikit-learn RandomForest)
        Zs = Zs.astype(np.float32); n = len(Zs); rows = np.arange(n); P = np.zeros((n, VALUE.shape[1]))
        for o in OFFSET:
            node = np.zeros(n, int)
            while True:
                g = o + node; leaf = LEFT[g] < 0
                if leaf.all(): break
                go = Zs[rows, np.maximum(FEAT[g], 0)] <= THR[g]; node = np.where(leaf, node, np.where(go, LEFT[g], RIGHT[g]))
            P += VALUE[o + node]
        return P[:, 1] / len(OFFSET)
    print(f'random forest (NumPy arrays): {len(OFFSET)} trees')
else:
    try:
        import joblib, sklearn
        B = joblib.load(MODEL_FILE)
    except Exception as e:
        raise RuntimeError('The .joblib cannot be read by this Python/scikit-learn (' + type(e).__name__ + '). Put A_detection_RF.npz next to it (NPZ_FILE in step 1) - then the joblib is not needed.') from None
    RFM = B['model']; FEATURES = list(B['candidate_features']); IDX = np.array(B['idx']); MU, SD = np.asarray(B['scaler_mean']), np.asarray(B['scaler_sd'])
    def proba(Zs): return RFM.predict_proba(Zs)[:, 1]
    print(f"random forest (joblib, scikit-learn {sklearn.__version__}; saved with {B['versions']['sklearn']}): {RFM.n_estimators} trees")
def predict(S):
    # spectra -> probability of white rust and class (probability > THRESHOLD = diseased)
    Z = (features(make_variant(S, VARIANT), FEATURES, OP) - MU) / SD; p = proba(Z[:, IDX]); return p, (p > THRESHOLD).astype(int)
print('features used:', ', '.join(FEATURES[i] for i in IDX))
OP = build_operator(FEATURES)""")
md11s = src(md11).replace('## 11 Outputs', '## 11 Outputs');
cells = [title, md0, c0, md1, c1, md2, c2, md3, c3, md4, c4, md5, c5, md6, c6, md7, c7, md8, c8, md9, c9, md10, c10, md11, c11]
for i, c in enumerate(cells): c['id'] = 'c%02d' % i
nb = dict(nbformat=4, nbformat_minor=5, metadata=RF['metadata'], cells=cells)
code = ''.join(src(c) for c in cells if c['cell_type'] == 'code'); assert 'torch' not in code and 'REF_FILE' not in code
json.dump(nb, open(PM + 'A_detection_RF_pixel_map_24Feb2026.ipynb', 'w'), indent=1); print('written A_detection_RF_pixel_map_24Feb2026.ipynb', len(cells), 'cells')
