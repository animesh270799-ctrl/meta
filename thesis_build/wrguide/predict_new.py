"""Apply the delivered models to NEW leaf spectra (same ASD export format: column 1 = wavelength 350-2500 nm, one column per leaf).
python predict_new.py new_spectra.xlsx   ->  new_spectra_predictions.csv  (A_<model> 0/1, B_<model> grade, C_<model> score)"""
import os, sys, glob, json, numpy as np, pandas as pd, joblib, torch
import config as C
from lib_spec import splice_correct, preprocess, indices, continuum_removed, cwt
from lib_select import feature_table
from lib_nets import build, pseudo
HERE = os.path.dirname(os.path.abspath(__file__)); DEL = os.path.join(HERE, 'deliver')
T0 = pd.read_excel(sys.argv[1]).apply(pd.to_numeric, errors='coerce').dropna(how='all'); T0 = T0[T0.iloc[:, 0].between(350, 2500)]
wl = T0.iloc[:, 0].values.astype(float); X = T0.iloc[:, 1:].values.T.astype(float); names = [str(c) for c in T0.columns[1:]]
X, _, _, _ = splice_correct(X, wl); w1, R1, FD1, w5, R5, FD5 = preprocess(X, wl); S = dict(w1=w1, R1=R1, FD1=FD1, w5=w5, R5=R5, FD5=FD5)
sel = json.load(open(os.path.join(DEL, 'selection_train.json'))); T = feature_table(sel, S, indices(R1, FD1), continuum_removed(R1, w1), cwt(R1)); out = pd.DataFrame({'leaf': names})
for f in sorted(glob.glob(os.path.join(DEL, 'ml', '*.joblib'))):
    d = joblib.load(f); p = d['model'].predict(T[d['features']].values)
    out['%s_%s' % (d['task'], d['name'])] = [C.GRADES[int(v)] for v in p] if d['task'] == 'B' else (np.clip(p, 0, 9) if d['task'] == 'C' else p)
for f in sorted(glob.glob(os.path.join(DEL, 'dl', '*.pt'))):
    d = torch.load(f, weights_only=False); Xs = ((T[d['features']].values - d['scaler_mean']) / d['scaler_sd']).astype(np.float32)
    Xi = Xs.reshape(-1, 1, 1, Xs.shape[1]) if d['net'] == 'DNN-F1' else pseudo(Xs)[0]; m = build(d['net'], d['k'], Xs.shape[1], d['n_out'], C.DL['drop']); m.load_state_dict(d['state_dict']); m.eval()
    with torch.no_grad(): o = m(torch.tensor(Xi))
    out['%s_%s' % (d['task'], d['net'])] = [C.GRADES[int(v)] for v in o.argmax(1)] if d['task'] == 'B' else (o.argmax(1).numpy() if d['task'] == 'A' else np.clip(o.ravel().numpy(), 0, 9))
out.to_csv(os.path.splitext(sys.argv[1])[0] + '_predictions.csv', index=False); print('predictions written for', len(out), 'leaves')
