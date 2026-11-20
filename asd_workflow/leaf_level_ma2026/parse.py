import pandas as pd, numpy as np, pickle, sys
D = pickle.load(open(sys.argv[1], 'rb'))
DATES = {'110226': '2026-02-11', '240226': '2026-02-24', '030326': '2026-03-03', '130326': '2026-03-13'}
rows, specs, plotdi = [], [], []
wl = None
for date in ['110226', '240226', '030326', '130326']:
    df = D[date]
    w = df.iloc[7:, 0].astype(float).values
    wl = w if wl is None else wl
    assert np.allclose(w, wl)
    for j in range(1, df.shape[1]):
        h = str(df.iat[0, j]); meta = df.iloc[1:7, j].tolist()
        if 'asd' in h:
            x = pd.to_numeric(df.iloc[7:, j], errors='coerce').values.astype(float)
            rows.append(dict(date=date, date_iso=DATES[date], file=h.replace('.asd.sco', ''), plot=int(meta[0]), variety=str(meta[1]).strip(),
                             stage=str(meta[2]).strip(), treatment=str(meta[3]).strip(), leaf=str(meta[4]).strip(), score=int(float(meta[5]))))
            specs.append(x)
        elif str(meta[4]).startswith('Plot DI'):
            plotdi.append(dict(date=date, plot=int(meta[0]), DI_recorded=float(meta[5])))
        else:
            print('skip', date, j, h, meta)
meta = pd.DataFrame(rows); R = np.vstack(specs)
print(meta.shape, R.shape, 'nan', np.isnan(R).sum())
print(meta.groupby('date').size())
pickle.dump(dict(meta=meta, R=R, wl=wl, plotdi=pd.DataFrame(plotdi)), open('leaf.pkl', 'wb'))
