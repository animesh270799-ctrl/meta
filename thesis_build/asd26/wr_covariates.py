"""Covariates and prediction for the white rust covariate baseline models (Step 2.5.5), ASD leaf data IARI 2025-26.

Covariates are known WITHOUT any sensor: days after inoculation (DAI), inoculation timing (D1-D4), variety (V1-V3),
growth stage, 7-day weather ending the day before the sampling date (no look-ahead) and favourable days since
inoculation (Chattopadhyay et al., 2011). Models were trained on inoculated, unsprayed leaves only.

    import joblib, pandas as pd, wr_covariates as wc
    b = joblib.load('covariate/A_covariates_only_Logistic_regression.joblib')
    leaves = pd.DataFrame({'date': ['2026-02-24'], 'variety': ['V1'], 'timing': ['D2'], 'stage': ['Flowering']})
    weather = pd.read_csv('daily_weather.csv')      # columns: date, Tmax, Tmin, RH1, RH2, rain
    print(wc.predict(b, leaves, weather))            # spectra-based bundles also need the spectral feature table
"""
import numpy as np, pandas as pd
VARIETIES = ['V1', 'V2', 'V3']; TIMINGS = ['D1', 'D2', 'D3', 'D4']
STAGE_CODE = {'Vegetative': 1, 'Flowering': 2, 'Pod formation': 3}
WEATHER_COLS = ['Tmax7', 'Tmin7', 'RH1_7', 'RH2_7', 'rain7', 'fav_leaf', 'fav_staghead']
GRADES = [0, 1, 3, 5, 7, 9]


def weather_covariates(weather, dates, inoculation='2026-02-05'):
    """7-day means (rain: total) for the 7 days BEFORE each date, and favourable days from inoculation to the day before the date.
    Leaf infection: Tmax 16-24 C, RH I > 97 %, RH II > 40 %; staghead: Tmax 20-29 C, Tmin > 12 C, RH I > 97 % (Chattopadhyay et al., 2011)."""
    W = weather.copy(); W['date'] = pd.to_datetime(W['date']); inoc = pd.Timestamp(inoculation); rows = []
    for d in sorted(set(pd.to_datetime(pd.Series(dates)))):
        win = W[(W.date < d) & (W.date >= d - pd.Timedelta(days=7))]; since = W[(W.date >= inoc) & (W.date < d)]
        rows.append(dict(date=d, Tmax7=win.Tmax.mean(), Tmin7=win.Tmin.mean(), RH1_7=win.RH1.mean(), RH2_7=win.RH2.mean(), rain7=win.rain.sum(),
                         fav_leaf=int((since.Tmax.between(16, 24) & (since.RH1 > 97) & (since.RH2 > 40)).sum()),
                         fav_staghead=int((since.Tmax.between(20, 29) & (since.Tmin > 12) & (since.RH1 > 97)).sum())))
    return pd.DataFrame(rows)


def leaf_covariates(leaves, weather=None, inoculation='2026-02-05', dai_mean=0.0):
    """leaves: one row per leaf with date, variety (V1-V3), timing (D1-D4) and stage (Vegetative / Flowering / Pod formation) or stage_code (1-3).
    Returns COV2 (random forest / best ML: one-hot variety and timing, DAI, stage code, weather) and COV1 (B1 statistical: one-hot with V1 and D1
    as reference, stage code, centred DAI and DAI^2)."""
    L = leaves.copy(); L['date'] = pd.to_datetime(L['date'])
    dai = (L.date - pd.Timestamp(inoculation)).dt.days.astype(float)
    sc = L['stage_code'].astype(float) if 'stage_code' in L else L['stage'].map(STAGE_CODE).astype(float)
    if sc.isna().any(): raise ValueError('unknown growth stage; use Vegetative, Flowering or Pod formation')
    oh = {('variety_' + v): (L.variety.astype(str) == v).astype(float).values for v in VARIETIES}
    oh.update({('timing_' + t): (L.timing.astype(str) == t).astype(float).values for t in TIMINGS})
    cov2 = pd.DataFrame(oh, index=L.index); cov2['DAI'] = dai.values; cov2['stage_code'] = sc.values
    if weather is not None:
        wc = weather_covariates(weather, L.date, inoculation); wx = L[['date']].merge(wc, on='date', how='left')
        for c in WEATHER_COLS: cov2[c] = wx[c].values
    cov1 = cov2[['variety_V2', 'variety_V3', 'timing_D2', 'timing_D3', 'timing_D4', 'stage_code']].copy()
    cov1['DAI'] = dai.values - dai_mean; cov1['DAI2'] = cov1['DAI'] ** 2
    return cov2, cov1


def predict(bundle, leaves, weather=None, spectral_features=None):
    """Predict with a covariate-baseline bundle. spectral_features: DataFrame with the bundle's spectral feature columns
    (from wr_features.all_features) for 'spectra + covariates' bundles. Returns a DataFrame of predictions."""
    cov2, cov1 = leaf_covariates(leaves, weather if bundle['uses_weather'] else None, bundle['inoculation'], bundle['dai_mean'])
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
