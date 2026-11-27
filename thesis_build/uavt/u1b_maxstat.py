"""Best of all frozen ASD models x inputs on the UAV plots, tested against chance with a maximum-statistic permutation test
(accounts for choosing the best of many model-input combinations; Westfall and Young, 1993; Ojala and Garriga, 2010)
and a bootstrap 95 % CI of that best combination (Efron and Tibshirani, 1993). Output: out/maxstat.csv"""
import os, numpy as np, pandas as pd
from sklearn.metrics import f1_score, roc_auc_score, r2_score
O = os.path.dirname(os.path.abspath(__file__)) + '/out/'
P = pd.read_csv(O + 'predictions_frozen.csv'); GT = pd.read_csv(O + 'ground_truth.csv')
rng = np.random.default_rng(7); NPERM, NB = 2000, 2000
SC = {'A': lambda y, p: f1_score(y, p, average='macro'), 'B': lambda y, p: f1_score(y, p, average='macro'), 'C': lambda y, p: r2_score(y, p)}
KEY = {'A': 'macro_F1', 'B': 'macro_F1', 'C': 'R2'}
rows = []
for t in 'ABC':
    d = P[P.task == t]; W = d.pivot_table(index='plot', columns=['model', 'variant'], values='pred').sort_index()
    y = d.drop_duplicates('plot').sort_values('plot').y.values; y = y.astype(float) if t == 'C' else y.astype(int)
    X = W.values if t == 'C' else W.values.astype(int)
    obs = np.array([SC[t](y, X[:, j]) for j in range(X.shape[1])]); j0 = int(np.argmax(obs))
    null = np.array([max(SC[t](yy, X[:, j]) for j in range(X.shape[1])) for yy in (rng.permutation(y) for _ in range(NPERM))])
    hi, di = np.where(GT.A.values == 0)[0], np.where(GT.A.values == 1)[0]
    bs = [np.r_[rng.choice(hi, len(hi)), rng.choice(di, len(di))] for _ in range(NB)]
    bv = [SC[t](y[b], X[b, j0]) for b in bs]
    r = dict(task=t, model=W.columns[j0][0], variant=W.columns[j0][1], metric=KEY[t], observed=obs[j0], ci_lo=np.percentile(bv, 2.5), ci_hi=np.percentile(bv, 97.5),
             n_combinations=X.shape[1], null_mean_of_max=null.mean(), null_p95_of_max=np.percentile(null, 95), p_value=(1 + np.sum(null >= obs[j0])) / (1 + NPERM))
    if t == 'A':
        s = d[(d.model == r['model']) & (d.variant == r['variant'])].sort_values('plot').score.values.astype(float)
        av = [roc_auc_score(y[b], s[b]) for b in bs]; r.update(AUC=roc_auc_score(y, s), AUC_lo=np.percentile(av, 2.5), AUC_hi=np.percentile(av, 97.5))
    rows.append(r)
M = pd.DataFrame(rows); M.to_csv(O + 'maxstat.csv', index=False); print(M.round(3).to_string(index=False))
