"""Write README.md for the model folder, copy the support files, test the prediction script on raw leaf spectra and zip the folder."""
import os, json, shutil, subprocess, numpy as np, pandas as pd
B = os.path.dirname(os.path.abspath(__file__)) + '/'; D = B + 'data/'; OUT = B + '../outputs/ASD_2025-26_models/'
for f in ('wr_features.py', 'wr_networks.py', 'predict_white_rust.py'): shutil.copy(B + f, OUT + f)
MT = pd.read_csv(D + 'metrics_all.csv'); SEL = json.load(open(OUT + 'feature_selection.json'))
mli = pd.read_csv(OUT + 'ml_models_index.csv') if os.path.exists(OUT + 'ml_models_index.csv') else pd.DataFrame()
dli = pd.read_csv(OUT + 'dl_models_index.csv') if os.path.exists(OUT + 'dl_models_index.csv') else pd.DataFrame()
def perf(t, m):
    r = MT[(MT.task == t) & (MT.model == m)]
    if not len(r): return '–'
    r = r.iloc[0]; return 'macro-F1 %.3f' % r.macro_F1 + (', AUC %.3f' % r.AUC if t == 'A' else ', QWK %.3f' % r.QWK) if t in 'AB' else 'R² %.3f, RMSE %.2f' % (r.R2, r.RMSE)
L = ['# White rust leaf models – ASD contact-probe spectra, IARI 2025-26', '',
     'Models refitted on all 2339 leaf spectra (4 dates, 3 varieties, 4 sowing timings, leaf positions L3/L5/LL) after leave-one-replication-out evaluation.',
     'The performance column is the **leave-one-replication-out test performance** of the same procedure (pooled test folds), i.e. the expected accuracy on a new replication of the same experiment.', '',
     '## Tasks', '', '- **A** detection: 0 = healthy (grade 0), 1 = diseased (grade > 0)', '- **B** six grades: 0, 1, 3, 5, 7, 9', '- **C** severity score: 0–9 (regression)', '',
     '## Input and pre-processing (done by the script)', '',
     'Raw reflectance 350–2500 nm at 1 nm (ASD export, splice-corrected) → Savitzky–Golay (window 11, order 2) → 400–2400 nm (water bands kept) → first derivative → 5-nm bands, 44 indices, REP/Dr/REarea, '
     'NDSI(%d, %d), RSI(%d, %d) and WRI = NDSI(%d, %d) + %s × R%d → z-score with the training mean and SD stored in each model file.' % (*SEL['ndsi'], *SEL['rsi'], SEL['wri']['l1'], SEL['wri']['l2'], SEL['wri']['w'], SEL['wri']['l3']), '',
     '## Feature sets (disease-specific feature set after VIF < 10)', '']
for t, n in (('A', 'detection'), ('B', 'six grades'), ('C', 'score')): L.append('- %s (%s): %s' % (t, n, ', '.join(SEL['DSF'][t])))
L += ['', 'Each machine-learning model then uses its own SFFS subset (listed below).', '', '## Files', '', '| File | Task | Model | Features used | LORO test performance |', '|---|---|---|---|---|']
for r in mli.itertuples(): L.append('| %s | %s | %s | %s | %s |' % (r.file, r.task, {'SVM': 'SVR', 'PLS': 'PLSR'}.get(r.model, r.model) if r.task == 'C' else r.model, r.features, perf(r.task, r.model)))
for r in dli.itertuples(): L.append('| %s | %s | %s | %s (%s) | %s |' % (r.file, r.task, r.model, r.features, 'feature vector' if r.model == 'DNN-F1' else '%d×%d pseudo-image' % (r.pseudo_image_k, r.pseudo_image_k), perf(r.task, r.model)))
L += ['', '## Use', '', '```', 'pip install numpy pandas scipy scikit-learn xgboost joblib openpyxl torch', 'python predict_white_rust.py my_spectra.xlsx          # column 1 = wavelength, one column per leaf (ASD export)',
      'python predict_white_rust.py my_spectra.csv --rows   # one row per leaf, headers = wavelengths', 'python predict_white_rust.py my_spectra.xlsx --models ml', '```', '',
      'Load one model directly in Python:', '', '```python', 'import joblib, wr_features  # wr_features must be importable (PLS classes)', "b = joblib.load('ml/C_severity_score_RF.joblib')",
      "print(b['features'], b['params'])", '```', '',
      '## Limits', '', '- Trained on one season (2025-26) and one site (IARI, New Delhi) with the ASD contact probe; check on new data (e.g. Bharatpur) before use.',
      '- Six-grade predictions are uncertain between neighbouring grades; use detection and the severity score for decisions.',
      '- Software versions are stored in each model file (key `versions` / `torch`). Load with the same major versions of scikit-learn, XGBoost and PyTorch.', '- Files `wr_features.py` and `wr_networks.py` hold the pre-processing and network definitions; keep them with the models.']
open(OUT + 'README.md', 'w').write('\n'.join(L)); print('README written')
# test the prediction script on 20 raw spectra in ASD layout
X0 = np.load(D + 'X_leaf.npy')[:20]; wl = np.load(D + 'wl.npy'); M = pd.read_csv(D + 'meta.csv')[:20]
tdir = B + 'data/predict_test/'; os.makedirs(tdir, exist_ok=True)
pd.DataFrame(np.column_stack([wl, X0.T]), columns=['Wavelength'] + ['leaf%d' % i for i in range(20)]).to_csv(tdir + 'test_spectra.csv', index=False)
r = subprocess.run(['python3', OUT + 'predict_white_rust.py', tdir + 'test_spectra.csv'], capture_output=True, text=True); print(r.stdout[-300:], r.stderr[-800:])
P = pd.read_csv(tdir + 'test_spectra_predictions.csv'); P.insert(1, 'observed_grade', M.grade.values); print(P.iloc[:8, :10].to_string())
shutil.make_archive(B + '../outputs/ASD_2025-26_models', 'zip', OUT); print('zipped')
