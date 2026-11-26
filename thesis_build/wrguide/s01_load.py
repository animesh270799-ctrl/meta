"""STEP 1 (A2): read the four ASD Excel exports into one leaf table and one spectra matrix.
Each file: column 1 = wavelength (350-2500 nm); every leaf column has 7 header rows
(name ending .sco, plot, variety, growth stage, healthy/diseased, leaf level, score). Plot-average columns are skipped."""
import os, openpyxl, numpy as np, pandas as pd
import config as C
meta, spec, wl = [], [], None
for date, fn in C.RAW_FILES.items():
    rows = list(openpyxl.load_workbook(os.path.join(C.RAW_DIR, fn), read_only=True).worksheets[0].iter_rows(values_only=True))
    hdr = rows[:7]; body = rows[7:]; w = np.array([r[0] for r in body], float); wl = w if wl is None else wl
    assert np.array_equal(w, wl), 'wavelength grid differs between files'
    n0 = len(meta)
    for j in range(1, len(hdr[0])):
        name = hdr[0][j]
        if not (isinstance(name, str) and name.lower().endswith('.sco')): continue
        meta.append(dict(date=date, file_col=name, plot=int(hdr[1][j]), variety=str(hdr[2][j]).strip(), stage=str(hdr[3][j]).strip(),
                         status=str(hdr[4][j]).strip(), leaf=str(hdr[5][j]).strip(), score=hdr[6][j]))
        spec.append([r[j] for r in body])
    print(date, fn, 'leaf columns:', len(meta) - n0)
M = pd.DataFrame(meta); X = np.array(spec, float)
np.save(os.path.join(C.OUT, '01_wl.npy'), wl); np.save(os.path.join(C.OUT, '01_X_raw.npy'), X); M.to_csv(os.path.join(C.OUT, '01_meta_raw.csv'), index=False)
print('CHECK: total leaf spectra', len(M), '| bands', X.shape[1], '| range', wl[0], '-', wl[-1], 'nm | missing values', int(np.isnan(X).sum()))
print(M.groupby(['date', 'leaf']).size().unstack(fill_value=0))
