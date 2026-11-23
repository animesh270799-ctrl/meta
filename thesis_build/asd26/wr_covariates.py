"""Covariates and prediction for the white rust covariate baseline models (Step 2.5.5), ASD leaf data IARI 2025-26 (natural infection).

Covariates are known WITHOUT any sensor: crop age (days after sowing, DAS), sowing timing (D1-D4 = 50, 40, 30, 20 DAS treatments),
variety (V1-V3), growth stage, 7-day weather ending the day before the sampling date (no look-ahead) and favourable days from
sowing to the day before the date (Chattopadhyay et al., 2011). Models were trained on unsprayed (naturally infected) leaves only.

    import joblib, pandas as pd, wr_covariates as wc
    b = joblib.load('covariate/A_covariates_only_Logistic_regression.joblib')
    leaves = pd.DataFrame({'date': ['2026-02-24'], 'variety': ['V1'], 'timing': ['D2'], 'stage': ['Flowering']})
    weather = pd.read_csv('covariate/IARI_daily_weather_2025-26.csv')   # columns: date, Tmax, Tmin, RH1, RH2, rain
    print(wc.predict(b, leaves, weather))            # spectra-based bundles also need the spectral feature table
For another season pass its own sowing dates: wc.predict(b, leaves, weather, sowing={'D1': '2026-11-19', ...}).
"""
import numpy as np, pandas as pd
VARIETIES = ['V1', 'V2', 'V3']; TIMINGS = ['D1', 'D2', 'D3', 'D4']
SOWING_2025_26 = {'D1': '2025-12-09', 'D2': '2025-12-18', 'D3': '2025-12-27', 'D4': '2026-01-09'}
STAGE_CODE = {'Vegetative': 1, 'Flowering': 2, 'Pod formation': 3}
WEATHER_COLS = ['Tmax7', 'Tmin7', 'RH1_7', 'RH2_7', 'rain7', 'fav_leaf', 'fav_staghead']
GRADES = [0, 1, 3, 5, 7, 9]


def fav_leaf(w):
    """leaf-infection days: Tmax 16-24 C, RH I > 97 %, RH II > 40 % (Chattopadhyay et al., 2011)"""
    return int(((w.Tmax.between(16, 24)) & (w.RH1 > 97) & (w.RH2 > 40)).sum())


def fav_staghead(w):
    """staghead days: Tmax 20-29 C, Tmin > 12 C, RH I > 97 % (Chattopadhyay et al., 2011)"""
    return int(((w.Tmax.between(20, 29)) & (w.Tmin > 12) & (w.RH1 > 97)).sum())


def window7(weather, dates):
    """7-day means (rain: total) for the 7 days BEFORE each date (no look-ahead)."""
    W = weather.copy(); W['date'] = pd.to_datetime(W['date']); rows = []
    for d in sorted(set(pd.to_datetime(pd.Series(dates)))):
        win = W[(W.date < d) & (W.date >= d - pd.Timedelta(days=7))]
        rows.append(dict(date=d, Tmax7=win.Tmax.mean(), Tmin7=win.Tmin.mean(), RH1_7=win.RH1.mean(), RH2_7=win.RH2.mean(), rain7=win.rain.sum()))
    return pd.DataFrame(rows)


def leaf_covariates(leaves, weather=None, sowing=None, das_mean=0.0):
    """leaves: one row per leaf with date, variety (V1-V3), timing (D1-D4) and stage (Vegetative / Flowering / Pod formation) or stage_code (1-3).
    Returns COV2 (random forest / best ML: one-hot variety and timing, DAS, stage code, 7-day weather, favourable days since sowing) and
    COV1 (B1 statistical: one-hot with V1 and D1 as reference, stage code, centred DAS and DAS^2)."""
    sowing = sowing or SOWING_2025_26
    L = leaves.copy(); L['date'] = pd.to_datetime(L['date']); sow = pd.to_datetime(L.timing.astype(str).map(sowing))
    if sow.isna().any(): raise ValueError('unknown sowing timing; give the sowing date of every timing')
    das = (L.date - sow).dt.days.astype(float)
    sc = L['stage_code'].astype(float) if 'stage_code' in L else L['stage'].map(STAGE_CODE).astype(float)
    if sc.isna().any(): raise ValueError('unknown growth stage; use Vegetative, Flowering or Pod formation')
    oh = {('variety_' + v): (L.variety.astype(str) == v).astype(float).values for v in VARIETIES}
    oh.update({('timing_' + t): (L.timing.astype(str) == t).astype(float).values for t in TIMINGS})
    cov2 = pd.DataFrame(oh, index=L.index); cov2['DAS'] = das.values; cov2['stage_code'] = sc.values
    if weather is not None:
        W = weather.copy(); W['date'] = pd.to_datetime(W['date'])
        wx = L[['date']].merge(window7(W, L.date), on='date', how='left')
        for c in ['Tmax7', 'Tmin7', 'RH1_7', 'RH2_7', 'rain7']: cov2[c] = wx[c].values
        cov2['fav_leaf'] = [fav_leaf(W[(W.date >= s) & (W.date < d)]) for s, d in zip(sow, L.date)]
        cov2['fav_staghead'] = [fav_staghead(W[(W.date >= s) & (W.date < d)]) for s, d in zip(sow, L.date)]
    cov1 = cov2[['variety_V2', 'variety_V3', 'timing_D2', 'timing_D3', 'timing_D4', 'stage_code']].copy()
    cov1['DAS'] = das.values - das_mean; cov1['DAS2'] = cov1['DAS'] ** 2
    return cov2, cov1


def predict(bundle, leaves, weather=None, spectral_features=None, sowing=None):
    """Predict with a covariate-baseline bundle. spectral_features: DataFrame with the bundle's spectral feature columns
    (from wr_features.all_features) for 'spectra + covariates' bundles. Returns a DataFrame of predictions."""
    cov2, cov1 = leaf_covariates(leaves, weather if bundle['uses_weather'] else None, sowing or bundle['sowing'], bundle['das_mean'])
    X = (cov1 if bundle['covariate_set'] == 'COV1' else cov2)[bundle['covariate_columns']]
    if bundle['spectral_columns']:
        if spectral_features is None: raise ValueError('this model also needs spectral features: ' + ', '.join(bundle['spectral_columns']))
        X = pd.concat([spectral_features[bundle['spectral_columns']].reset_index(drop=True), X.reset_index(drop=True)], axis=1)
    X = X.values.astype(float); t = bundle['task']; m = bundle['model']; out = pd.DataFrame(index=range(len(X)))
    if bundle['kind'] == 'ordinal':
        Xs = ((X - bundle['scaler_mean']) / bundle['scaler_sd'])[:, bundle['keep']]
        pr = np.asarray(m.model.predict(m.params, exog=Xs)); out['pred_grade'] = [GRADES[i] for i in pr.argmax(1)]
        for i, g in enumerate(GRADES): out['p_grade_%d' % g] = pr[:, i]
        return out
    p = m.predict(X)
    if t == 'A':
        out['pred_diseased'] = p.astype(int)
        if hasattr(m, 'predict_proba'): out['p_diseased'] = m.predict_proba(X)[:, 1]
    elif t == 'B': out['pred_grade'] = [GRADES[int(i)] for i in p]
    else: out['pred_score'] = np.clip(p, 0, 9)
    return out
