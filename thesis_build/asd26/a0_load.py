"""Parse the four 2025-26 ASD leaf files (contact probe, splice corrected) into one leaf-level table."""
import openpyxl, numpy as np, pandas as pd, os
U = '/root/.claude/uploads/c5704ca0-f1ca-5695-b9e0-a810fbe166a9/'
FILES = {'2026-02-11': 'eeec9a7f-asd__data_complete_labelled_110226_scored.xlsx', '2026-02-24': 'c6bc9195-asd__data_complete_labelled_240226_scored.xlsx',
         '2026-03-03': '3ecb31e0-asd__data_complete_labelled_030326_scored.xlsx', '2026-03-13': '6584ad8d-asd__data_complete_labelled_130326_scored.xlsx'}
D = os.path.dirname(os.path.abspath(__file__)) + '/data/'
meta, spec = [], []
for date, f in FILES.items():
    ws = openpyxl.load_workbook(U + f, read_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[:7]; wl = np.array([r[0] for r in rows[7:]], float); S = rows[7:]
    for j in range(1, len(hdr[0])):
        name = hdr[0][j]
        if not (isinstance(name, str) and name.lower().endswith('.sco')): continue   # skip plot-average columns
        meta.append(dict(date=date, file_col=name, plot=int(hdr[1][j]), variety=str(hdr[2][j]).strip(), stage=str(hdr[3][j]).strip(), status=str(hdr[4][j]).strip(), leaf=str(hdr[5][j]).strip(), score=hdr[6][j]))
        spec.append([r[j] for r in S])
M = pd.DataFrame(meta); X = np.array(spec, float)
print(M.shape, X.shape, wl[0], wl[-1], 'NaN', np.isnan(X).sum())
np.save(D + 'wl.npy', wl); np.save(D + 'X_leaf.npy', X.astype(np.float32)); M.to_csv(D + 'meta_raw.csv', index=False)
print(M.groupby('date').size()); print(pd.crosstab(M.date, M.score)); print(M.leaf.value_counts()); print(M.stage.value_counts()); print(M.status.value_counts())
print(pd.crosstab(M.plot, M.status).head(14))
pv = M.groupby('plot').variety.agg(lambda s: '/'.join(sorted(set(s)))); print(pv.to_dict())
