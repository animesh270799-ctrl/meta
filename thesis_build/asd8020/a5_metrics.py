"""Evaluation metrics (Activity 2.4) for machine-learning and deep-learning predictions."""
import numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score, cohen_kappa_score, confusion_matrix, precision_recall_fscore_support, r2_score
GR = [0, 1, 3, 5, 7, 9]

def cls_metrics(y, yp, K, score=None):
    y = np.asarray(y).astype(int); yp = np.asarray(yp).astype(int)
    labs = list(range(K)); cm = confusion_matrix(y, yp, labels=labs)
    pr, rc, f1, _ = precision_recall_fscore_support(y, yp, labels=labs, zero_division=0)
    out = dict(n=len(y), OA=float((y == yp).mean()), kappa=float(cohen_kappa_score(y, yp)), macro_P=float(pr.mean()), macro_R=float(rc.mean()), macro_F1=float(f1.mean()))
    if K == 2:
        tn, fp, fn, tp = cm.ravel(); out.update(sensitivity=float(tp / (tp + fn)), specificity=float(tn / (tn + fp)), balanced_acc=float((tp / (tp + fn) + tn / (tn + fp)) / 2), F1=float(f1[1]))
        if score is not None and not pd.isna(score).any(): out['AUC'] = float(roc_auc_score(y, score))
    else:
        out['QWK'] = float(cohen_kappa_score(y, yp, weights='quadratic')); out['within1'] = float((np.abs(y - yp) <= 1).mean())
        for i, g in enumerate(GR): out['F1_g%d' % g] = float(f1[i]); out['R_g%d' % g] = float(rc[i]); out['P_g%d' % g] = float(pr[i])
    return out, cm

def reg_metrics(y, yp):
    y = np.asarray(y, float); yp = np.asarray(yp, float); rmse = float(np.sqrt(((y - yp) ** 2).mean()))
    return dict(n=len(y), R2=float(r2_score(y, yp)), RMSE=rmse, MAE=float(np.abs(y - yp).mean()), RPD=float(y.std(ddof=1) / rmse), bias=float((yp - y).mean()), r=float(np.corrcoef(y, yp)[0, 1]))

# ---- single hold-out split: uncertainty from a plot bootstrap of the test predictions (whole test plots resampled with
#      replacement, healthy and unsprayed plots separately; Efron and Tibshirani, 1993; Field and Welsh, 2007) ----
_PLOTS = None
def _plots():
    global _PLOTS
    if _PLOTS is None:
        import os; _PLOTS = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) + '/data/meta.csv')['plot'].values
    return _PLOTS
def fast_metric(k, y, p, K=None):
    if k == 'macro_F1':
        cm = np.bincount(y * K + p, minlength=K * K).reshape(K, K); tp = np.diag(cm); den = cm.sum(0) + cm.sum(1)
        return float(np.mean(np.where(tp > 0, 2 * tp / np.maximum(den, 1), 0.0)))
    if k == 'RMSE': return float(np.sqrt(np.mean((y - p) ** 2)))
    if k == 'R2': return float(1 - np.sum((y - p) ** 2) / np.sum((y - y.mean()) ** 2))
def plot_boot(d, k, K=None, nb=1000, seed=42):
    pl = _plots()[d['leaf'].values.astype(int)]; y = d.y.values; p = d.pred.values
    if K: y = y.astype(int); p = p.astype(int)
    else: y = y.astype(float); p = p.astype(float)
    groups = [np.unique(pl[pl <= 12]), np.unique(pl[pl > 12])]; idx = {q: np.where(pl == q)[0] for q in np.unique(pl)}; rng = np.random.default_rng(seed); out = []
    for _ in range(nb):
        ii = np.concatenate([idx[q] for g in groups if len(g) for q in rng.choice(g, len(g), replace=True)]); out.append(fast_metric(k, y[ii], p[ii], K))
    return np.array(out)

def summarise(df):
    """df: columns task, model, y, pred, score (optional), fold. Returns metric table and confusion matrices."""
    rows, cms = [], {}
    for (task, model), d in df.groupby(['task', 'model'], sort=False):
        if task in ('A', 'B', 'X'):
            K = 2 if task in ('A', 'X') else 6; sc = d['score'].values if 'score' in d and task in ('A', 'X') and d['score'].notna().all() else None
            m, cm = cls_metrics(d.y.values, d.pred.values, K, sc); cms[(task, model)] = cm
            if d.fold.nunique() > 1: fm = [cls_metrics(g.y.values, g.pred.values, K)[0]['macro_F1'] for _, g in d.groupby('fold')]; m['macro_F1_sd'] = float(np.std(fm))
            else: bs = plot_boot(d, 'macro_F1', K); m['macro_F1_sd'] = float(np.std(bs, ddof=1)); m['macro_F1_lo'], m['macro_F1_hi'] = [float(x) for x in np.percentile(bs, [2.5, 97.5])]
        else:
            m = reg_metrics(d.y.values, d.pred.values)
            if d.fold.nunique() > 1: fr = [reg_metrics(g.y.values, g.pred.values)['RMSE'] for _, g in d.groupby('fold')]; m['RMSE_sd'] = float(np.std(fr))
            else:
                bs = plot_boot(d, 'RMSE'); m['RMSE_sd'] = float(np.std(bs, ddof=1)); m['RMSE_lo'], m['RMSE_hi'] = [float(x) for x in np.percentile(bs, [2.5, 97.5])]
                b2 = plot_boot(d, 'R2'); m['R2_lo'], m['R2_hi'] = [float(x) for x in np.percentile(b2, [2.5, 97.5])]
        rows.append(dict(task=task, model=model, **m))
    return pd.DataFrame(rows), cms
