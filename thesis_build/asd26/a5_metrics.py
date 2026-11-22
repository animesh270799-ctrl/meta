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

def summarise(df):
    """df: columns task, model, y, pred, score (optional), fold. Returns metric table and confusion matrices."""
    rows, cms = [], {}
    for (task, model), d in df.groupby(['task', 'model'], sort=False):
        if task in ('A', 'B', 'X'):
            K = 2 if task in ('A', 'X') else 6; sc = d['score'].values if 'score' in d and task in ('A', 'X') and d['score'].notna().all() else None
            m, cm = cls_metrics(d.y.values, d.pred.values, K, sc); cms[(task, model)] = cm
            fm = [cls_metrics(g.y.values, g.pred.values, K)[0]['macro_F1'] for _, g in d.groupby('fold')]; m['macro_F1_sd'] = float(np.std(fm))
        else:
            m = reg_metrics(d.y.values, d.pred.values); fr = [reg_metrics(g.y.values, g.pred.values)['RMSE'] for _, g in d.groupby('fold')]; m['RMSE_sd'] = float(np.std(fr))
        rows.append(dict(task=task, model=model, **m))
    return pd.DataFrame(rows), cms
