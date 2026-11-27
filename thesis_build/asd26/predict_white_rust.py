"""Predict white rust on NEW ASD leaf spectra with the saved 2025-26 models.

Usage
  python predict_white_rust.py spectra.xlsx                 # ASD export: column 1 = wavelength (350-2500 nm), one column per leaf
  python predict_white_rust.py spectra.csv --rows           # one row per leaf, column headers = wavelengths
  python predict_white_rust.py spectra.xlsx --models ml     # only machine-learning models (ml, dl or all; default all)
Output: <input>_predictions.csv with, for every leaf and model,
  A_<model>      detection (0 healthy, 1 diseased) and A_<model>_p (probability of disease, where available)
  B_<model>      predicted grade (0, 1, 3, 5, 7, 9)
  C_<model>      predicted severity score (0-9, clipped)
Keep this script, wr_features.py, wr_networks.py, feature_selection.json and the ml/ and dl/ folders together."""
import argparse, glob, json, os, sys, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from wr_features import all_features, GRADES

def read_spectra(path, rows):
    T = pd.read_excel(path) if path.lower().endswith(('.xlsx', '.xls')) else pd.read_csv(path)
    if rows:
        wcols = [c for c in T.columns if str(c).replace('.', '', 1).isdigit()]
        return T[wcols].values.astype(float), np.array([float(c) for c in wcols]), [str(i) for i in T.index]
    T = T.apply(pd.to_numeric, errors='coerce').dropna(how='all'); T = T[T.iloc[:, 0].between(300, 2600)]
    wl = T.iloc[:, 0].values.astype(float); X = T.iloc[:, 1:].values.T.astype(float)
    return X, wl, [str(c) for c in T.columns[1:]]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('file'); ap.add_argument('--rows', action='store_true'); ap.add_argument('--models', default='all', choices=['all', 'ml', 'dl']); a = ap.parse_args()
    X, wl, names = read_spectra(a.file, a.rows); sel = json.load(open(os.path.join(HERE, 'feature_selection.json')))
    ALL = all_features(X, wl, sel); out = pd.DataFrame({'leaf': names})
    if a.models in ('all', 'ml'):
        import joblib
        for f in sorted(glob.glob(os.path.join(HERE, 'ml', '*.joblib'))):
            b = joblib.load(f); Z = (ALL[b['candidate_features']].values - b['scaler_mean']) / b['scaler_sd']; Z = Z[:, b['idx']]
            col = b['task'] + '_' + b['model_name']; yp = b['model'].predict(Z)
            if b['task'] == 'A':
                out[col] = yp.astype(int)
                if hasattr(b['model'], 'predict_proba') and b['model_name'] != 'SVM': out[col + '_p'] = b['model'].predict_proba(Z)[:, 1].round(3)
            elif b['task'] == 'B': out[col] = [GRADES[int(i)] for i in yp]
            else: out[col] = np.clip(yp, 0, 9).round(2)
    if a.models in ('all', 'dl'):
        import torch, wr_networks as NW
        for f in sorted(glob.glob(os.path.join(HERE, 'dl', '*.pt'))):
            b = torch.load(f, map_location='cpu', weights_only=False); Z = ((ALL[b['features']].values - b['scaler_mean']) / b['scaler_sd']).astype(np.float32)
            Zi = Z.reshape(-1, 1, 1, Z.shape[1]) if b['net'] == 'DNN-F1' else NW.pseudo(Z)[0]
            m = NW.build(b['net'], b['k'], Z.shape[1], b['n_out'], 0.03); m.load_state_dict(b['state_dict']); m.eval()
            with torch.no_grad(): o = m(torch.tensor(Zi))
            col = b['task'] + '_' + b['net'].replace(' ', '_')
            if b['task'] == 'A': p = torch.softmax(o, 1).numpy(); out[col] = p.argmax(1); out[col + '_p'] = p[:, 1].round(3)
            elif b['task'] == 'B': out[col] = [GRADES[i] for i in o.argmax(1).numpy()]
            else: out[col] = np.clip(o.ravel().numpy(), 0, 9).round(2)
    fn = os.path.splitext(a.file)[0] + '_predictions.csv'; out.to_csv(fn, index=False); print('saved', fn, out.shape)

if __name__ == '__main__': main()
