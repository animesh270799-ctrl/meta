"""Evaluation metrics (methodology Part F) and the plot bootstrap."""
import numpy as np, pandas as pd
from scipy import stats
from sklearn.metrics import roc_auc_score, cohen_kappa_score, confusion_matrix, precision_recall_fscore_support, r2_score
import config as C


def cls_metrics(y, yp, K, score=None):
    y = np.asarray(y).astype(int); yp = np.asarray(yp).astype(int); labs = list(range(K)); cm = confusion_matrix(y, yp, labels=labs)
    pr, rc, f1, _ = precision_recall_fscore_support(y, yp, labels=labs, zero_division=0)
    out = dict(n=len(y), OA=float((y == yp).mean()), kappa=float(cohen_kappa_score(y, yp)), macro_P=float(pr.mean()), macro_R=float(rc.mean()), macro_F1=float(f1.mean()))
    if K == 2:
        tn, fp, fn, tp = cm.ravel(); out.update(sensitivity=float(tp / (tp + fn)), specificity=float(tn / (tn + fp)), balanced_acc=float((tp / (tp + fn) + tn / (tn + fp)) / 2))
        if score is not None and not pd.isna(score).any(): out['AUC'] = float(roc_auc_score(y, score))
    else:
        out['QWK'] = float(cohen_kappa_score(y, yp, weights='quadratic')); out['within1'] = float((np.abs(y - yp) <= 1).mean())
        for i, g in enumerate(C.GRADES): out['F1_g%d' % g] = float(f1[i])
    return out, cm


def reg_metrics(y, yp):
    y = np.asarray(y, float); yp = np.asarray(yp, float); rmse = float(np.sqrt(((y - yp) ** 2).mean()))
    return dict(n=len(y), R2=float(r2_score(y, yp)), RMSE=rmse, MAE=float(np.abs(y - yp).mean()), RPD=float(y.std(ddof=1) / rmse), bias=float((yp - y).mean()), r=float(np.corrcoef(y, yp)[0, 1]))


def metric_value(task, name, y, p, s=None):
    if task == 'C':
        return reg_metrics(y, p)[name]
    return cls_metrics(y, p, 2 if task == 'A' else 6, s)[0][name]


def plot_boot_idx(plots, nb, seed):
    """Step F4: resample whole plots with replacement, healthy (1-12) and unsprayed plots separately."""
    rng = np.random.default_rng(seed); groups = [np.unique(plots[plots <= 12]), np.unique(plots[plots > 12])]; idx = {q: np.where(plots == q)[0] for q in np.unique(plots)}
    for _ in range(nb):
        yield np.concatenate([idx[q] for g in groups if len(g) for q in rng.choice(g, len(g), replace=True)])


def boot_ci(task, name, y, p, plots, s=None, nb=C.N_BOOT, seed=C.SEED):
    vals = []
    for ii in plot_boot_idx(plots, nb, seed):
        try: vals.append(metric_value(task, name, y[ii], p[ii], None if s is None else s[ii]))
        except ValueError: pass
    vals = np.array(vals); return float(vals.std(ddof=1)), float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def delong(y, s1, s2):
    """DeLong test for two correlated AUCs (DeLong et al., 1988; fast algorithm of Sun and Xu, 2014)."""
    pos, neg = s1[y == 1], s1[y == 0]; pos2, neg2 = s2[y == 1], s2[y == 0]; m, n = len(pos), len(neg)
    def comp(p, q):
        r = stats.rankdata(np.concatenate([p, q])); rp = stats.rankdata(p); rq = stats.rankdata(q)
        return (r[:m].sum() - m * (m + 1) / 2) / (m * n), (r[:m] - rp) / n, 1 - (r[m:] - rq) / m
    a1, v10a, v01a = comp(pos, neg); a2, v10b, v01b = comp(pos2, neg2)
    S = np.cov(np.vstack([v10a, v10b])) / m + np.cov(np.vstack([v01a, v01b])) / n
    z = (a1 - a2) / np.sqrt(S[0, 0] + S[1, 1] - 2 * S[0, 1]); return a1, a2, z, 2 * stats.norm.sf(abs(z))
