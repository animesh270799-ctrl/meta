"""Pixel-map notebook for the LORO random-forest SIX-GRADE model (RF/B_six_grades_RF.joblib, refitted on all ASD leaves of 2025-26).
Direct UAV reflectance (its best input on the 48 UAV plots: OA 0.417, macro-F1 0.262, QWK 0.199, within one grade 0.729). Uses B_six_grades_RF.npz
(same model as plain arrays, identical predictions, any scikit-learn version) when present, otherwise loads the .joblib with scikit-learn.
Built from the tested B_RF standalone notebook (reader, features, grade map, per-plot accuracy); step 5 loads the npz/joblib like the detection notebook.
Output: uavp/kit/per_model/B_six_grades_RF_pixel_map_24Feb2026.ipynb"""
import json, os, copy
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'; PM = HERE + 'kit/per_model/'
RF = json.load(open(PM + 'B_RF_pixel_map_24Feb2026_STANDALONE.ipynb'))
R = json.load(open(HERE + 'kit/models/B_RF_reference.json')); T = R['TRUTH']; EXP = [round(float(v), 6) for v in R['EXPECTED']]
assert R['MODEL']['variant'] == 'direct'
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
title = cell('markdown', """# White rust pixel map – Random forest, task B: six severity grades (0, 1, 3, 5, 7, 9)
UAV hyperspectral image of 24 February 2026 · model `B_six_grades_RF.joblib` (random forest, 500 trees, refitted on all ASD leaf spectra of 2025-26 after leave-one-replication-out evaluation)

| Item | This notebook |
|---|---|
| Model | **Random forest** (machine learning), `RF\\B_six_grades_RF.joblib`; the same model as plain arrays in `RF\\B_six_grades_RF.npz` |
| Input given to the model | direct UAV reflectance (its best input on the 48 UAV plots) |
| Features (computed from each pixel spectrum) | FD1090, FD1060, FD550, FD1660, FD1245, FD870, FD760, FD595, DWSI-2 |
| Accuracy on the 48 UAV plot spectra | overall accuracy 0.417, macro-F1 0.262, quadratic weighted kappa 0.199, within one grade 0.729 |
| Output (folder `GRADE_RF`) | `B_six_grades_RF_grade` (grade 0, 1, 3, 5, 7 or 9) and `B_six_grades_RF_class` (ENVI classification, 1–6 = grades 0–9) – ENVI `.dat/.hdr`, GeoTIFF (if `rasterio` is installed), a PNG map and per-plot tables |

On the 48 UAV plots this model was weak (macro-F1 0.262; QWK 0.199), so the map is **not validated** severity – it shows what the leaf model predicts.

**Model file.** The `.joblib` loads only with the scikit-learn version it was saved with (1.9.1). If `B_six_grades_RF.npz` is in the same folder, the notebook uses it instead: identical predictions with plain NumPy, any scikit-learn version.

**Steps.** 0 install packages · 1 settings · 2 libraries and image helpers · 3 reference data · 4 features · 5 load the model · 6 self-check · 7 open the image · 8 pixel loop · 9 map · 10 per-plot accuracy · 11 outputs.
**Time.** Run first with `SPATIAL_STEP = 4` (preview), then `SPATIAL_STEP = 1` for the final map.""")
md0, c0 = pick(RF, '## 0 Install'); md2, c2 = pick(RF, '## 2 Libraries'); md4, c4 = pick(RF, '## 4 Features')
md6, c6 = pick(RF, '## 6 Self-check'); md7, c7 = pick(RF, '## 7 Open the image'); md8, c8 = pick(RF, '## 8 Pixel loop')
md9, c9 = pick(RF, '## 9 Map'); md10, c10 = pick(RF, '## 10 Per-plot accuracy'); md11, c11 = pick(RF, '## 11 Outputs')
# ---- step 1
md1 = cell('markdown', '## 1 Settings\nYour paths are filled in. `MODEL_FILE` is your RF six-grade model; `NPZ_FILE` is the same model as plain arrays – put it in the same `RF` folder and it is used automatically, so the Python / scikit-learn version does not matter. Results go to `IMAGE_VALIDATED\\GRADE_RF`.')
c1 = cell('code', f"""# ============================ SETTINGS ============================
HDR_FILE  = r'D:\\Coalighned\\24_02_2026\\subset_200526.hdr'          # ENVI header of the 24 Feb image (the data file 'subset_200526', ~9 GB, must be next to it)
DATA_NAME = 'subset_200526'                                         # name of the image data file
ROI_FILE  = r'D:\\Coalighned\\24_02_2026\\48_plot_roi_new.xml'        # 48 plot ROIs, ROI #n = plot n (None = skip the per-plot accuracy)
OUT_DIR   = r'{P}\\IMAGE_VALIDATED'   # your output folder
OUT_NAME  = 'GRADE_RF'                                               # results go to OUT_DIR\\GRADE_RF
MODEL_FILE = r'{P}\\RF\\B_six_grades_RF.joblib'   # RF six-grade model (scikit-learn joblib)
NPZ_FILE   = r'{P}\\RF\\B_six_grades_RF.npz'      # same model as plain arrays: used if present (works with any Python / scikit-learn version)
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
md3 = cell('markdown', "## 3 Reference data (embedded)\n`TRUTH` = ASD leaf scores of 24 Feb 2026 for the 48 plots (mean score, plot grade, PDI); `EXPECTED` = this model's grade for the 48 plot-mean spectra (self-check). The model uses the UAV reflectance **directly**, so no reference spectra are needed.")
c3 = cell('code', "# ASD leaf scores of 24 Feb 2026 for the 48 plots (plot = ROI number)\n"
          "TRUTH = pd.DataFrame({'plot': %s,\n" % T['plot'] + "    'block': %s,\n" % json.dumps(T['block']) + "    'status': %s,\n" % json.dumps(T['status']) +
          "    'variety': %s,\n" % json.dumps(T['variety']) + "    'sowing': %s,\n" % json.dumps(T['sowing']) + "    'mean_score': %s,\n" % json.dumps(T['mean_score']) +
          "    'grade': %s,\n" % json.dumps(T['grade']) + "    'PDI': %s})\n" % json.dumps(T['PDI']) +
          "# this model's grade for the 48 plot-mean spectra (used by the self-check)\nEXPECTED = %s\n" % json.dumps(EXP) +
          "MODEL = dict(task='B', model='Random forest', variant='direct', uav_metric='macro_F1', uav_value=%.4f)\n" % R['MODEL']['uav_value'] +
          "GRADES = [0, 1, 3, 5, 7, 9]; KEY, TASK, VARIANT = 'B_six_grades_RF', MODEL['task'], MODEL['variant']\n"
          "assert len(WL) == 483 and abs(WL[0] - 399.38) < 0.5 and abs(WL[-1] - 2397.55) < 0.5, 'the image bands differ from the 24 Feb image the model inputs were built for'\n"
          "print(f\"{MODEL['model']} six grades – input '{VARIANT}' (reflectance used as it is), accuracy on the 48 UAV plots: overall 0.417, macro-F1 0.262, QWK 0.199, within one grade 0.729\")")
# ---- step 5
md5 = cell('markdown', '## 5 Load the model\nWith `B_six_grades_RF.npz`: the 500 trees as plain arrays, predicted with NumPy exactly as scikit-learn does (the class proportions of the reached leaves are averaged; the class with the largest average is the grade). Without it: the `.joblib` is loaded with scikit-learn. Inputs are standardised with the training mean and SD stored with the model; the model uses 9 of its 11 candidate features, so only these 9 are computed for each pixel.')
c5 = cell('code', r"""if os.path.isfile(NPZ_FILE):
    z = np.load(NPZ_FILE, allow_pickle=False); IDX = z['idx']
    FEATURES = [str(z['features'][i]) for i in IDX]; MU, SD = z['mu'][IDX], z['sd'][IDX]                     # the 9 features the model uses
    LEFT, RIGHT, FEAT, THR, VALUE, OFFSET, CLASSES = z['left'], z['right'], z['feat'], z['thr'], z['value'], z['offset'], z['classes']
    def class_proportions(Zs):
        # every pixel is routed through every tree; the class proportions of the reached leaves are averaged (scikit-learn RandomForest)
        Zs = Zs.astype(np.float32); n = len(Zs); rows = np.arange(n); P = np.zeros((n, VALUE.shape[1]))
        for o in OFFSET:
            node = np.zeros(n, int)
            while True:
                g = o + node; leaf = LEFT[g] < 0
                if leaf.all(): break
                go = Zs[rows, np.maximum(FEAT[g], 0)] <= THR[g]; node = np.where(leaf, node, np.where(go, LEFT[g], RIGHT[g]))
            P += VALUE[o + node]
        return P / len(OFFSET)
    print(f'random forest (NumPy arrays): {len(OFFSET)} trees, {len(CLASSES)} classes')
else:
    try:
        import joblib, sklearn
        B = joblib.load(MODEL_FILE)
    except Exception as e:
        raise RuntimeError('The .joblib cannot be read by this Python/scikit-learn (' + type(e).__name__ + '). Put B_six_grades_RF.npz next to it (NPZ_FILE in step 1) - then the joblib is not needed.') from None
    RFM = B['model']; IDX = np.array(B['idx']); FEATURES = [B['candidate_features'][i] for i in IDX]
    MU, SD = np.asarray(B['scaler_mean'])[IDX], np.asarray(B['scaler_sd'])[IDX]; CLASSES = np.asarray(RFM.classes_)
    def class_proportions(Zs): return RFM.predict_proba(Zs)
    print(f"random forest (joblib, scikit-learn {sklearn.__version__}; saved with {B['versions']['sklearn']}): {RFM.n_estimators} trees")
def predict(S):
    # spectra -> grade 0, 1, 3, 5, 7 or 9 (class with the largest average proportion)
    Z = (features(make_variant(S, VARIANT), FEATURES, OP) - MU) / SD
    g = np.array(GRADES)[CLASSES[class_proportions(Z).argmax(1)].astype(int)]; return g.astype(float), g
print('features used:', ', '.join(FEATURES))
OP = build_operator(FEATURES)""")
# ---- step 8: grade raster + ENVI classification raster
s8 = src(c8); old8 = "write_envi(base + '.dat', VAL, 'grade (0-9)', 4, {'data ignore value': 'NaN'}); tif = write_tif(base + '.tif', VAL, np.nan)"
assert old8 in s8
s8 = s8.replace(old8, "cls = np.zeros((NL, NS), np.uint8)\nfor k, g in enumerate(GRADES): cls[CROP & (VAL == g)] = k + 1            # class 1-6 = grade 0, 1, 3, 5, 7, 9; 0 = outside the crop\n"
                "write_envi(base + '_grade.dat', VAL, 'white rust grade (0, 1, 3, 5, 7, 9)', 4, {'data ignore value': 'NaN'})\n"
                "write_envi(base + '_class.dat', cls, 'grade class (0 outside, 1-6 = grade 0, 1, 3, 5, 7, 9)', 1, {'file type': 'ENVI Classification', 'classes': 7,\n"
                "           'class names': '{outside, grade 0, grade 1, grade 3, grade 5, grade 7, grade 9}', 'class lookup': '{0 0 0, 26 152 80, 254 224 139, 253 174 97, 244 109 67, 215 48 39, 127 0 0}'})\n"
                "tif = write_tif(base + '_grade.tif', VAL, np.nan) and write_tif(base + '_class.tif', cls, 0)\n"
                "share = pd.Series({f'grade {g}': float((LAB[CROP] == g).mean()) for g in GRADES}); print('share of crop pixels per grade:'); print(share.round(3).to_string())")
setsrc(c8, s8)
md8 = cell('markdown', '## 8 Pixel loop\nThe image is read `BLOCK_ROWS` rows at a time; for the crop pixels of each block the model computes its features and grade. Values are NaN outside the crop. Two rasters are written: the grade itself (float, NaN outside) and an ENVI classification (1–6 = grades 0, 1, 3, 5, 7, 9; 0 = outside) that opens in ENVI with the grade colours.')
# ---- step 9: grade map with grade ticks + bar chart of pixel shares
s9 = src(c9)
s9 = s9.replace("fig, axs = plt.subplots(1, 1, figsize=(8 * 1 + 1, 8 * NL / NS + 1), squeeze=False); axs = axs.ravel(); ax = axs[0]",
                "fig, axs = plt.subplots(1, 2, figsize=(8 + 5, 8 * NL / NS + 1), squeeze=False, gridspec_kw=dict(width_ratios=[3, 1])); axs = axs.ravel(); ax = axs[0]")
s9 = s9.replace("plt.colorbar(im, ax=ax, fraction=0.03, label=lab)", "plt.colorbar(im, ax=ax, fraction=0.03, label=lab, ticks=GRADES)")
s9 = s9.replace("fig.tight_layout(); fp =", "axs[1].bar([str(g) for g in GRADES], [100 * share[f'grade {g}'] for g in GRADES], color=GCM.colors, edgecolor='k', lw=0.4)\n"
                "axs[1].set_xlabel('grade'); axs[1].set_ylabel('% of crop pixels'); axs[1].set_title('pixels per grade', fontsize=9)\n"
                "fig.tight_layout(); fp =")
assert 'ticks=GRADES' in s9 and 'width_ratios' in s9 and 'pixels per grade' in s9; setsrc(c9, s9)
md9 = cell('markdown', '## 9 Map\nLeft: grade map with plot outlines and numbers from the ROI file; the title carries the model\'s accuracy on the 48 UAV plots so that an unreliable map is recognised at once. Right: share of crop pixels in each grade.')
# ---- step 10: add the plot-level confusion table (field grade x mapped grade)
s10 = src(c10); old10 = "    PS.to_csv(os.path.join(OUT, KEY + '_per_plot.csv'), index=False)"
assert old10 in s10
s10 = s10.replace(old10, "    PS['mapped_grade'] = [GRADES[i] for i in gp]\n"
                  "    CT = pd.crosstab(pd.Categorical(PS.grade, GRADES), pd.Categorical(PS.mapped_grade, GRADES), rownames=['field grade'], colnames=['mapped grade'], dropna=False)\n"
                  "    CT.to_csv(os.path.join(OUT, KEY + '_plot_confusion.csv'))\n" + old10)
s10 = s10.replace("print(pd.Series(S_).round(3).to_string())", "print(pd.Series(S_).round(3).to_string()); print('\\nplots: field grade (rows) x mapped grade (columns)'); print(CT.to_string())")
assert 'CT.to_string()' in s10; setsrc(c10, s10)
md10 = cell('markdown', '## 10 Per-plot accuracy\nFor each plot ROI: crop pixels inside the image, the median and mean predicted grade, compared with the ASD leaf scores of 24 Feb. Mapped plot grade = the grade nearest to the median pixel grade; reported: exact agreement, agreement within one grade step and the correlation of the mean pixel grade with the mean leaf score (Congalton, 1991; Cohen, 1968 for weighted agreement), plus the plot confusion table. Plots 1 and 48 extend slightly beyond the image (95% and 89% of the plot inside); only their pixels inside the image are used.')
md11 = cell('markdown', "## 11 Outputs\nIn `IMAGE_VALIDATED\\GRADE_RF`: `B_six_grades_RF_grade` and `B_six_grades_RF_class` (ENVI `.dat/.hdr` and GeoTIFF), `B_six_grades_RF_map.png`, `B_six_grades_RF_per_plot.csv`, `B_six_grades_RF_plot_confusion.csv`, `B_six_grades_RF_accuracy.csv` and `run_info.json`. Open the `.dat/.hdr` or `.tif` in ENVI/QGIS – they carry the georeference of the image.\n\n**References.** Apan et al. (2004); Breiman (2001); Cohen (1968); Congalton (1991); Savitzky and Golay (1964) – full entries in the transfer report.")
cells = [title, md0, c0, md1, c1, md2, c2, md3, c3, md4, c4, md5, c5, md6, c6, md7, c7, md8, c8, md9, c9, md10, c10, md11, c11]
for i, c in enumerate(cells): c['id'] = 'c%02d' % i
nb = dict(nbformat=4, nbformat_minor=5, metadata=RF['metadata'], cells=cells)
code = ''.join(src(c) for c in cells if c['cell_type'] == 'code'); assert 'torch' not in code and 'REF_FILE' not in code and 'GAIN' not in code
json.dump(nb, open(PM + 'B_six_grades_RF_pixel_map_24Feb2026.ipynb', 'w'), indent=1); print('written B_six_grades_RF_pixel_map_24Feb2026.ipynb', len(cells), 'cells')
