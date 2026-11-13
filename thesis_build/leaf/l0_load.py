"""Parse the four ASD leaf files into one tidy table (leaf spectra + metadata)."""
import openpyxl, numpy as np, pandas as pd, os, glob
U = '/root/.claude/uploads/c5704ca0-f1ca-5695-b9e0-a810fbe166a9/'
FILES = {'2026-02-11': '135483cc-asd__data_complete_labelled_110226_scored.xlsx', '2026-02-24': '6543042b-asd__data_complete_labelled_240226_scored.xlsx',
         '2026-03-03': 'b7cbf7a5-asd__data_complete_labelled_030326_scored.xlsx', '2026-03-13': '7dd7a392-asd__data_complete_labelled_130326_scored.xlsx'}
D = os.path.dirname(os.path.abspath(__file__)) + '/data/'
trt = pd.read_excel(U + '82ac1646-treatment_detail.xlsx'); trt.columns = ['plot', 'inoc', 'variety_t', 'rep']
trt['rep'] = trt['rep'].replace({'Control/healthy': 'C'})
meta, spec = [], []
for date, f in FILES.items():
    ws = openpyxl.load_workbook(U + f, read_only=True).worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[:7]; wl = np.array([r[0] for r in rows[7:]], float); S = rows[7:]
    for j in range(1, len(hdr[0])):
        name = hdr[0][j]
        if not (isinstance(name, str) and name.lower().endswith('.sco')): continue   # skip plot-average columns
        meta.append(dict(date=date, file_col=name, plot=int(hdr[1][j]), variety=hdr[2][j], stage=hdr[3][j], status=hdr[4][j], leaf=hdr[5][j], score=hdr[6][j]))
        spec.append([r[j] for r in S])
M = pd.DataFrame(meta); X = np.array(spec, float)
M = M.merge(trt[['plot', 'inoc', 'rep']], on='plot', how='left')
print(M.shape, X.shape, wl[0], wl[-1], np.isnan(X).sum())
np.save(D + 'wl.npy', wl); np.save(D + 'X_leaf.npy', X); M.to_csv(D + 'meta_leaf.csv', index=False)
print(M.groupby('date').size()); print(pd.crosstab(M.date, M.score)); print(pd.crosstab(M.rep, M.status)); print(M.leaf.value_counts()); print(M.stage.value_counts())
print((M.variety != M.merge(trt, on='plot').variety_t.values).sum(), 'variety mismatches')
