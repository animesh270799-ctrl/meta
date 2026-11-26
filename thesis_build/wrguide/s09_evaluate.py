"""STEP 9 (F1-F4): test metrics of every model with plot-bootstrap standard errors and 95 % intervals; confusion matrices; figures."""
import os, numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve
import config as C
from lib_metrics import cls_metrics, reg_metrics, boot_ci
O = C.OUT; M = pd.read_csv(os.path.join(O, '03_meta_split.csv')); plots_all = M['plot'].values
P = pd.concat([pd.read_csv(os.path.join(O, '07_ml_predictions.csv')), pd.read_csv(os.path.join(O, '08_dl_predictions_main.csv')).drop(columns='config')])
rows, cms = [], []
for (task, model), d in P.groupby(['task', 'model'], sort=False):
    y, p, pl = d.y.values, d.pred.values, plots_all[d.leaf.values]; s = d.score.values if task == 'A' and d.score.notna().all() else None
    if task == 'C': m = reg_metrics(y, p); key = 'R2'
    else:
        m, cm = cls_metrics(y, p, 2 if task == 'A' else 6, s); key = 'macro_F1'
        cms.append(pd.DataFrame(cm).assign(task=task, model=model))
    se, lo, hi = boot_ci(task, key, y.astype(float) if task == 'C' else y.astype(int), p.astype(float) if task == 'C' else p.astype(int), pl, s)
    rows.append(dict(task=task, model=model, family=d.family.iloc[0], **m, main_metric=key, boot_SE=se, CI_low=lo, CI_high=hi))
R = pd.DataFrame(rows); R.to_csv(os.path.join(O, '09_test_metrics.csv'), index=False); pd.concat(cms).to_csv(os.path.join(O, '09_confusion_matrices.csv'))
fig, ax = plt.subplots(1, 3, figsize=(15, 4.5))
for a, t in zip(ax, 'ABC'):
    d = R[R.task == t].sort_values('macro_F1' if t != 'C' else 'R2'); v = d['macro_F1' if t != 'C' else 'R2']
    a.barh(d.model, v, xerr=d.boot_SE, color=['#2E75B6' if f == 'ML' else '#7030A0' for f in d.family]); a.set_title({'A': 'A detection (macro-F1)', 'B': 'B six grades (macro-F1)', 'C': 'C score (R²)'}[t])
fig.tight_layout(); fig.savefig(os.path.join(O, '09_model_comparison.png'), dpi=150); plt.close(fig)
fig, ax = plt.subplots(figsize=(6, 6))
for (model), d in P[(P.task == 'A') & P.score.notna()].groupby('model'):
    f, t, _ = roc_curve(d.y, d.score); ax.plot(f, t, label=model)
ax.plot([0, 1], [0, 1], 'k:'); ax.set_xlabel('false-positive rate'); ax.set_ylabel('sensitivity'); ax.legend(fontsize=8); fig.savefig(os.path.join(O, '09_roc.png'), dpi=150); plt.close(fig)
print('CHECK: metrics of %d models written to 09_test_metrics.csv (main metric, bootstrap SE and 95 %% interval for each)' % len(R))
