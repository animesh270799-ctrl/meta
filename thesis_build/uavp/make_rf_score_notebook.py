"""Pixel-map notebook for the LORO random-forest SEVERITY-SCORE regressor (RF/C_severity_score_RF.joblib, refitted on all ASD leaves of 2025-26).
Direct UAV reflectance (its best input on the 48 UAV plots: R2 -0.066, RMSE 2.01, MAE 1.58, r 0.067). Uses C_severity_score_RF.npz (same model as
plain arrays, identical predictions, any scikit-learn version) when present, otherwise loads the .joblib with scikit-learn.
Built from the tested C_XGBoost standalone notebook (reader, features, score map, per-plot accuracy); step 5 loads the npz/joblib like the other RF notebooks.
Output: uavp/kit/per_model/C_severity_score_RF_pixel_map_24Feb2026.ipynb"""
import json, os, copy
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'; PM = HERE + 'kit/per_model/'
XG = json.load(open(PM + 'C_XGBoost_pixel_map_24Feb2026_STANDALONE.ipynb'))
R = json.load(open(HERE + 'kit/models/B_RF_reference.json')); T = R['TRUTH']
EXP = [round(float(v), 6) for v in json.load(open(HERE + 'kit/models/C_severity_score_RF_expected.json'))]
src = lambda c: ''.join(c['source'])
def cell(kind, t):
    c = dict(cell_type=kind, metadata={}, source=[l + '\n' for l in t.split('\n')]); c['source'][-1] = c['source'][-1].rstrip('\n')
    if kind == 'code': c.update(execution_count=None, outputs=[])
    return c
def pick(nb, head):          # (markdown cell starting with head, the code cell after it)
    for i, c in enumerate(nb['cells']):
        if c['cell_type'] == 'markdown' and src(c).startswith(head): return copy.deepcopy(c), copy.deepcopy(nb['cells'][i + 1])
    raise KeyError(head)
def setsrc(c, t): c['source'] = cell(c['cell_type'], t)['source']
P = 'C:\\Users\\BDI LAB\\Desktop\\ASD_MODEL_ON_240226_UAV_IMAGE_PIXELWISE'
title = cell('markdown', """# White rust pixel map – Random forest, task C: severity score (0–9)
UAV hyperspectral image of 24 February 2026 · model `C_severity_score_RF.joblib` (random-forest regression, 500 trees, refitted on all ASD leaf spectra of 2025-26 after leave-one-replication-out evaluation)

| Item | This notebook |
|---|---|
| Model | **Random forest regression** (machine learning), `RF\\C_severity_score_RF.joblib`; the same model as plain arrays in `RF\\C_severity_score_RF.npz` |
| Input given to the model | direct UAV reflectance (its best input on the 48 UAV plots) |
| Features (computed from each pixel spectrum) | FD1090, FD1060, FD550, FD870, FD665, FD595, Dr |
| Accuracy on the 48 UAV plot spectra | R² −0.066, RMSE 2.01, MAE 1.58, bias +0.47, r 0.067 (predictions only 2.98–4.26) |
| Output (folder `SCORE_RF`) | `C_severity_score_RF_score` (predicted severity score 0–9) – ENVI `.dat/.hdr`, GeoTIFF (if `rasterio` is installed), a PNG map, a plot scatter and per-plot tables |

On the 48 UAV plots this model did not predict the field score (R² below 0: worse than using the mean score for every plot), so the map is **not validated** severity – it shows what the leaf model predicts.

**Model file.** The `.joblib` loads only with the scikit-learn version it was saved with (1.9.1). If `C_severity_score_RF.npz` is in the same folder, the notebook uses it instead: identical predictions with plain NumPy, any scikit-learn version.

**Steps.** 0 install packages · 1 settings · 2 libraries and image helpers · 3 reference data · 4 features · 5 load the model · 6 self-check · 7 open the image · 8 pixel loop · 9 map · 10 per-plot accuracy · 11 outputs.
**Time.** Run first with `SPATIAL_STEP = 4` (preview), then `SPATIAL_STEP = 1` for the final map.""")
md0, c0 = pick(XG, '## 0 Install'); md2, c2 = pick(XG, '## 2 Libraries'); md4, c4 = pick(XG, '## 4 Features')
md6, c6 = pick(XG, '## 6 Self-check'); md7, c7 = pick(XG, '## 7 Open the image'); md8, c8 = pick(XG, '## 8 Pixel loop')
md9, c9 = pick(XG, '## 9 Map'); md10, c10 = pick(XG, '## 10 Per-plot accuracy'); md11, c11 = pick(XG, '## 11 Outputs')
# ---- step 1
md1 = cell('markdown', '## 1 Settings\nYour paths are filled in. `MODEL_FILE` is your RF severity-score model; `NPZ_FILE` is the same model as plain arrays – put it in the same `RF` folder and it is used automatically, so the Python / scikit-learn version does not matter. Results go to `IMAGE_VALIDATED\\SCORE_RF`.')
c1 = cell('code', f"""# ============================ SETTINGS ============================
HDR_FILE  = r'D:\\Coalighned\\24_02_2026\\subset_200526.hdr'          # ENVI header of the 24 Feb image (the data file 'subset_200526', ~9 GB, must be next to it)
DATA_NAME = 'subset_200526'                                         # name of the image data file
ROI_FILE  = r'D:\\Coalighned\\24_02_2026\\48_plot_roi_new.xml'        # 48 plot ROIs, ROI #n = plot n (None = skip the per-plot accuracy)
OUT_DIR   = r'{P}\\IMAGE_VALIDATED'   # your output folder
OUT_NAME  = 'SCORE_RF'                                               # results go to OUT_DIR\\SCORE_RF
MODEL_FILE = r'{P}\\RF\\C_severity_score_RF.joblib'   # RF severity-score model (scikit-learn joblib)
NPZ_FILE   = r'{P}\\RF\\C_severity_score_RF.npz'      # same model as plain arrays: used if present (works with any Python / scikit-learn version)
PLOT_AVG_FILE = r'D:\\Coalighned\\24_02_2026\\envi_plot_avg.txt'      # ENVI plot-average file for the self-check (skipped if the file is not there)

SPATIAL_STEP = 4        # 4 = quick preview; 1 = final full-resolution map
BLOCK_ROWS   = 16       # image rows processed at a time (reduce if memory is short)
NDVI_MIN     = 0.6      # crop mask: NDVI(898, 684) > 0.6 as in the methodology
REFLECTANCE_SCALE = 'auto'  # 'auto' (divides by 10000 if the data look like 0-10000) or a number""")
# ---- step 2: model-file check for npz / joblib, versions
s2 = src(c2); a = s2.index("_mf = os.path.basename("); old = "print('model file  :', MODEL_FILE); print('results to  :', OUT)"; b = s2.index(old)
s2 = s2[:a] + "if not (os.path.isfile(NPZ_FILE) or os.path.isfile(MODEL_FILE)):\n    raise FileNotFoundError('Neither the model file nor the .npz was found:\\n  ' + MODEL_FILE + '\\n  ' + NPZ_FILE + '\\nCheck MODEL_FILE / NPZ_FILE in step 1.')\nprint('model file  :', NPZ_FILE if os.path.isfile(NPZ_FILE) else MODEL_FILE); print('results to  :', OUT)\nimport sys, scipy; print('python', sys.version.split()[0], '| numpy', np.__version__, '| scipy', scipy.__version__, '| pandas', pd.__version__)" + s2[b + len(old):]
setsrc(c2, s2)
# ---- step 3
md3 = cell('markdown', "## 3 Reference data (embedded)\n`TRUTH` = ASD leaf scores of 24 Feb 2026 for the 48 plots (mean score, plot grade, PDI); `EXPECTED` = this model's score for the 48 plot-mean spectra (self-check). The model uses the UAV reflectance **directly**, so no reference spectra are needed.")
c3 = cell('code', "# ASD leaf scores of 24 Feb 2026 for the 48 plots (plot = ROI number)\n"
          "TRUTH = pd.DataFrame({'plot': %s,\n" % T['plot'] + "    'block': %s,\n" % json.dumps(T['block']) + "    'status': %s,\n" % json.dumps(T['status']) +
          "    'variety': %s,\n" % json.dumps(T['variety']) + "    'sowing': %s,\n" % json.dumps(T['sowing']) + "    'mean_score': %s,\n" % json.dumps(T['mean_score']) +
          "    'grade': %s,\n" % json.dumps(T['grade']) + "    'PDI': %s})\n" % json.dumps(T['PDI']) +
          "# this model's severity score for the 48 plot-mean spectra (used by the self-check)\nEXPECTED = %s\n" % json.dumps(EXP) +
          "MODEL = dict(task='C', model='Random forest', variant='direct', uav_metric='R2', uav_value=-0.0664)\n"
          "GRADES = [0, 1, 3, 5, 7, 9]; KEY, TASK, VARIANT = 'C_severity_score_RF', MODEL['task'], MODEL['variant']\n"
          "assert len(WL) == 483 and abs(WL[0] - 399.38) < 0.5 and abs(WL[-1] - 2397.55) < 0.5, 'the image bands differ from the 24 Feb image the model inputs were built for'\n"
          "print(f\"{MODEL['model']} severity score – input '{VARIANT}' (reflectance used as it is), accuracy on the 48 UAV plots: R² -0.066, RMSE 2.01, MAE 1.58, r 0.067\")")
# ---- step 5
md5 = cell('markdown', '## 5 Load the model\nWith `C_severity_score_RF.npz`: the 500 regression trees as plain arrays, predicted with NumPy exactly as scikit-learn does (each tree gives the mean leaf score of the training leaves in the leaf it reaches; the forest averages the 500 trees; Breiman, 2001). Without it: the `.joblib` is loaded with scikit-learn. Inputs are standardised with the training mean and SD stored with the model; the model uses 7 of its 10 candidate features, so only these 7 are computed for each pixel. The score is kept within 0–9.')
c5 = cell('code', r"""if os.path.isfile(NPZ_FILE):
    z = np.load(NPZ_FILE, allow_pickle=False); IDX = z['idx']
    FEATURES = [str(z['features'][i]) for i in IDX]; MU, SD = z['mu'][IDX], z['sd'][IDX]                     # the 7 features the model uses
    LEFT, RIGHT, FEAT, THR, VALUE, OFFSET = z['left'], z['right'], z['feat'], z['thr'], z['value'][:, 0], z['offset']
    def forest_score(Zs):
        # every pixel is routed through every tree; the leaf values (mean leaf score of the training leaves) are averaged (scikit-learn RandomForestRegressor)
        Zs = Zs.astype(np.float32); n = len(Zs); rows = np.arange(n); v = np.zeros(n)
        for o in OFFSET:
            node = np.zeros(n, int)
            while True:
                g = o + node; leaf = LEFT[g] < 0
                if leaf.all(): break
                go = Zs[rows, np.maximum(FEAT[g], 0)] <= THR[g]; node = np.where(leaf, node, np.where(go, LEFT[g], RIGHT[g]))
            v += VALUE[o + node]
        return v / len(OFFSET)
    print(f'random forest regression (NumPy arrays): {len(OFFSET)} trees')
else:
    try:
        import joblib, sklearn
        B = joblib.load(MODEL_FILE)
    except Exception as e:
        raise RuntimeError('The .joblib cannot be read by this Python/scikit-learn (' + type(e).__name__ + '). Put C_severity_score_RF.npz next to it (NPZ_FILE in step 1) - then the joblib is not needed.') from None
    RFM = B['model']; IDX = np.array(B['idx']); FEATURES = [B['candidate_features'][i] for i in IDX]
    MU, SD = np.asarray(B['scaler_mean'])[IDX], np.asarray(B['scaler_sd'])[IDX]
    def forest_score(Zs): return RFM.predict(Zs)
    print(f"random forest regression (joblib, scikit-learn {sklearn.__version__}; saved with {B['versions']['sklearn']}): {RFM.n_estimators} trees")
def predict(S):
    # spectra -> severity score 0-9
    Z = (features(make_variant(S, VARIANT), FEATURES, OP) - MU) / SD
    v = np.clip(forest_score(Z), 0, 9); return v, v
print('features used:', ', '.join(FEATURES))
OP = build_operator(FEATURES)""")
# ---- step 8: score raster with clear names + pixel summary
s8 = src(c8); old8 = "write_envi(base + '.dat', VAL, 'severity score (0-9)', 4, {'data ignore value': 'NaN'}); tif = write_tif(base + '.tif', VAL, np.nan)"
assert old8 in s8
s8 = s8.replace(old8, "write_envi(base + '_score.dat', VAL, 'white rust severity score (0-9)', 4, {'data ignore value': 'NaN'}); tif = write_tif(base + '_score.tif', VAL, np.nan)\n"
                "q = np.nanpercentile(VAL[CROP], [2, 25, 50, 75, 98]); print(f'pixel scores: mean {np.nanmean(VAL[CROP]):.2f}; 2/25/50/75/98 % percentiles ' + ' / '.join(f'{x:.2f}' for x in q))")
setsrc(c8, s8)
md8 = cell('markdown', '## 8 Pixel loop\nThe image is read `BLOCK_ROWS` rows at a time; for the crop pixels of each block the model computes its features and score. Values are NaN outside the crop. The score raster is written as float (`C_severity_score_RF_score`), and the spread of the pixel scores is printed.')
# ---- step 9: map on the fixed 0-9 scale + histogram of pixel scores
s9 = src(c9)
s9 = s9.replace("fig, axs = plt.subplots(1, 1, figsize=(8 * 1 + 1, 8 * NL / NS + 1), squeeze=False); axs = axs.ravel(); ax = axs[0]",
                "fig, axs = plt.subplots(1, 2, figsize=(8 + 5, 8 * NL / NS + 1), squeeze=False, gridspec_kw=dict(width_ratios=[3, 1])); axs = axs.ravel(); ax = axs[0]")
s9 = s9.replace("fig.tight_layout(); fp =", "axs[1].hist(VAL[CROP], bins=np.arange(0, 9.01, 0.25), color='#F46D43', edgecolor='k', lw=0.3); axs[1].set_xlim(0, 9)\n"
                "axs[1].set_xlabel('predicted score (0-9)'); axs[1].set_ylabel('crop pixels'); axs[1].set_title('distribution of pixel scores', fontsize=9)\n"
                "fig.tight_layout(); fp =")
assert 'width_ratios' in s9 and 'distribution of pixel scores' in s9 and "vmin=0, vmax=9" in s9; setsrc(c9, s9)
md9 = cell('markdown', "## 9 Map\nLeft: score map on the fixed 0–9 scale (so maps of different models and dates are comparable), with plot outlines and numbers from the ROI file; the title carries the model's accuracy on the 48 UAV plots so that an unreliable map is recognised at once. Right: distribution of the pixel scores.")
# ---- step 10: add MAE, bias, r for diseased plots and a scatter of plot means
s10 = src(c10)
old_s = "    S_ = dict(R2=1 - (e ** 2).sum() / ((PS.mean_score - PS.mean_score.mean()) ** 2).sum(), RMSE=float(np.sqrt((e ** 2).mean())), r_with_score=PS[['mean_score_pred', 'mean_score']].corr().iloc[0, 1])"
assert old_s in s10
s10 = s10.replace(old_s, "    S_ = dict(R2=1 - (e ** 2).sum() / ((PS.mean_score - PS.mean_score.mean()) ** 2).sum(), RMSE=float(np.sqrt((e ** 2).mean())), MAE=float(e.abs().mean()), bias=float(e.mean()),\n"
                  "              r_with_score=PS[['mean_score_pred', 'mean_score']].corr().iloc[0, 1], r_diseased_plots=PS[PS.status == 'Diseased'][['mean_score_pred', 'mean_score']].corr().iloc[0, 1])")
old_p = "    print(PS.head(12).round(3).to_string(index=False)); print('...'); print(pd.Series(S_).round(3).to_string())"
assert old_p in s10
s10 = s10.replace(old_p, old_p + "\n"
                  "    fig, ax = plt.subplots(figsize=(4.8, 4.8))\n"
                  "    for st_, col in (('Healthy', '#1A9850'), ('Diseased', '#D73027')):\n"
                  "        q_ = PS[PS.status == st_]; ax.scatter(q_.mean_score, q_.mean_score_pred, c=col, s=20, edgecolor='k', lw=0.3, label=st_.lower() + ' plots')\n"
                  "    ax.plot([0, 9], [0, 9], 'k--', lw=0.8, label='1:1 line'); ax.set_xlim(0, 9); ax.set_ylim(0, 9); ax.set_aspect('equal')\n"
                  "    ax.set_xlabel('field mean leaf score (ASD, 24 Feb)'); ax.set_ylabel('mapped mean score of the plot'); ax.legend(fontsize=8, loc='upper left')\n"
                  "    ax.set_title(f\"48 plots: R² {S_['R2']:.2f}, RMSE {S_['RMSE']:.2f}, r {S_['r_with_score']:.2f}\", fontsize=9)\n"
                  "    fig.tight_layout(); fp2 = os.path.join(OUT, KEY + '_plot_scatter.png'); fig.savefig(fp2, dpi=300); plt.close(fig); show(fp2, 450)")
setsrc(c10, s10)
md10 = cell('markdown', '## 10 Per-plot accuracy\nFor each plot ROI: crop pixels inside the image and the mean predicted score of the plot, compared with the mean ASD leaf score of 24 Feb: R², RMSE, MAE, bias (mapped − field), Pearson r for all plots and for the 36 diseased plots, and a scatter of the plot means against the 1:1 line (Bellon-Maurel et al., 2010 for RMSE/RPD reporting). Plots 1 and 48 extend slightly beyond the image (95% and 89% of the plot inside); only their pixels inside the image are used.')
md11 = cell('markdown', "## 11 Outputs\nIn `IMAGE_VALIDATED\\SCORE_RF`: `C_severity_score_RF_score` (ENVI `.dat/.hdr` and GeoTIFF), `C_severity_score_RF_map.png`, `C_severity_score_RF_plot_scatter.png`, `C_severity_score_RF_per_plot.csv`, `C_severity_score_RF_accuracy.csv` and `run_info.json`. Open the `.dat/.hdr` or `.tif` in ENVI/QGIS – they carry the georeference of the image.\n\n**References.** Bellon-Maurel et al. (2010); Breiman (2001); Daughtry et al. (2000); Filella and Peñuelas (1994); Horler et al. (1983); Savitzky and Golay (1964) – full entries in the transfer report.")
cells = [title, md0, c0, md1, c1, md2, c2, md3, c3, md4, c4, md5, c5, md6, c6, md7, c7, md8, c8, md9, c9, md10, c10, md11, c11]
for i, c in enumerate(cells): c['id'] = 'c%02d' % i
nb = dict(nbformat=4, nbformat_minor=5, metadata=XG['metadata'], cells=cells)
code = ''.join(src(c) for c in cells if c['cell_type'] == 'code'); assert 'torch' not in code and 'REF_FILE' not in code and 'GAIN' not in code and 'XGBoost' not in code
json.dump(nb, open(PM + 'C_severity_score_RF_pixel_map_24Feb2026.ipynb', 'w'), indent=1); print('written C_severity_score_RF_pixel_map_24Feb2026.ipynb', len(cells), 'cells')
