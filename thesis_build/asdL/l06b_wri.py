"""STEP L5.3 detail: the White Rust Index search of l06_select.py repeated to keep the full record (best combination for every weight w).
Same data (training leaves, 5-nm reflectance), same 200 best NDSI pairs (bands >= 50 nm apart), lambda3 every 10 nm, |r| with the grade."""
import os, json, numpy as np, pandas as pd
import configL as C
M = pd.read_csv(os.path.join(C.OUT, 'L2_meta.csv')); S = np.load(os.path.join(C.OUT, 'L3_spectra.npz')); w5, R5 = S['w5'], S['R5']; tr = (M.split == 'TRAIN').values
Rt, yt = R5[tr], M.grade.values[tr].astype(float); n = len(yt); yc = (yt - yt.mean()) / yt.std(); N = np.load(os.path.join(C.OUT, 'L5_2_NDSI_R2.npy'))
A = N.copy(); i, j = np.indices(A.shape); A[np.abs(w5[i] - w5[j]) < C.WRI_SEP] = np.nan
flat = np.argsort(np.nan_to_num(A, nan=-1).ravel())[::-1][:C.WRI_PAIRS]; l3 = np.arange(0, len(w5), C.WRI_STEP // C.STEP); rows = []
for rank, f in enumerate(flat):
    a, b = np.unravel_index(f, A.shape); ndv = (Rt[:, a] - Rt[:, b]) / (Rt[:, a] + Rt[:, b])
    for wt in C.WRI_W:
        if wt == 0:
            r0 = float(np.corrcoef(ndv, yt)[0, 1]); rows.append(dict(pair_rank=rank + 1, l1=int(w5[a]), l2=int(w5[b]), NDSI_R2=float(N[a, b]), w=0.0, l3=None, r=r0, abs_r=abs(r0))); continue
        V = ndv[:, None] + wt * Rt[:, l3]; Vc = (V - V.mean(0)) / V.std(0); rr = yc @ Vc / n; k = int(np.argmax(np.abs(rr)))
        rows.append(dict(pair_rank=rank + 1, l1=int(w5[a]), l2=int(w5[b]), NDSI_R2=float(N[a, b]), w=wt, l3=int(w5[l3[k]]), r=float(rr[k]), abs_r=float(abs(rr[k]))))
D = pd.DataFrame(rows).sort_values('abs_r', ascending=False); D.to_csv(os.path.join(C.OUT, 'L5_3_wri_search_all.csv'), index=False)
best = D.loc[D.groupby('w').abs_r.idxmax()].sort_values('abs_r', ascending=False); best.to_csv(os.path.join(C.OUT, 'L5_3_wri_best_by_w.csv'), index=False)
sel = json.load(open(os.path.join(C.OUT, 'L5_selection.json'))); top = D.iloc[0]
assert int(top.l1) == sel['wri']['l1'] and int(top.l2) == sel['wri']['l2'] and float(top.w) == sel['wri']['w'], (top, sel['wri'])
print(best.round(4).to_string(index=False)); print('combinations searched', len(D))
