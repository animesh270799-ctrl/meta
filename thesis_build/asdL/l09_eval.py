"""STEP L7: test metrics of every leaf model (ML + networks) on the 684 test leaves, computed once. Tasks A, B: confusion matrix, OA, kappa, per-class
precision/recall/F1, macro recall and F1; Task A also sensitivity, specificity, balanced accuracy, AUC; Task B also within-one-grade accuracy and
quadratic weighted kappa; Task C: R2, RMSE, MAE, RPD, bias. Low-severity check; results by leaf position, growth stage, date and variety;
plot-bootstrap 95% CI of the main metric (1000 resamples of whole test plots, healthy and unsprayed plots resampled separately)."""
import os, glob, json, numpy as np, pandas as pd
import configL as C
import lmods as LM
O = C.OUT; M = pd.read_csv(os.path.join(O, 'L2_meta.csv'))
P = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(os.path.join(O, 'L6_ml_predictions*.csv')) + glob.glob(os.path.join(O, 'L6_dl_predictions*.csv')))], ignore_index=True)
P = P.drop_duplicates(['task', 'model', 'leaf'], keep='last'); P = P.merge(M[['plot', 'leaf', 'stage', 'date', 'variety', 'grade', 'block']].rename(columns={'leaf': 'leaf_pos'}), left_on='leaf', right_index=True)
MAIN = LM.MAIN; ORDER = ['SVM', 'RF', 'k-NN', 'PLS', 'DNN-F1', 'DT-EDNet', 'EfficientNet-B0', 'ResNet18', 'ConvNeXt V2-Atto']
def metrics(task, d): return LM.metrics(task, d.y.values, d.pred.values, d.score.values)
def main_value(task, d): return LM.main_value(task, d.y.values, d.pred.values, d.score.values)
rng = np.random.default_rng(C.SEED); tplots = np.array(sorted(M.loc[M.split == 'TEST', 'plot'].unique())); hp, up = tplots[tplots <= 12], tplots[tplots > 12]
BOOT = [np.concatenate([rng.choice(hp, len(hp)), rng.choice(up, len(up))]) for _ in range(1000)]
rows, cms, strata, low = [], [], [], []
for (task, model), d in P.groupby(['task', 'model']):
    d = d.sort_values('leaf'); m, cm = metrics(task, d); byplot = {q: g for q, g in d.groupby('plot')}
    bv = [main_value(task, pd.concat([byplot[q] for q in b])) for b in BOOT]; m['CI_low'], m['CI_high'] = float(np.nanpercentile(bv, 2.5)), float(np.nanpercentile(bv, 97.5))
    rows.append(dict(task=task, model=model, family=d.family.iloc[0], **m))
    if cm is not None:
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]): cms.append(dict(task=task, model=model, observed=i, predicted=j, n=int(cm[i, j])))
    if task == 'A': g1 = d[d.grade == 1]; low.append(dict(task='A', model=model, check='recall of grade-1 leaves (detected as diseased)', n=len(g1), value=float((g1.pred == 1).mean())))
    if task == 'C': g1 = d[d.grade <= 1]; low.append(dict(task='C', model=model, check='RMSE of leaves with grade 0-1', n=len(g1), value=float(np.sqrt(((g1.pred - g1.y) ** 2).mean()))))
    for var in ('leaf_pos', 'stage', 'date', 'variety'):
        for lev, g in d.groupby(var): strata.append(dict(task=task, model=model, stratum=var, level=lev, n=len(g), metric=MAIN[task], value=main_value(task, g),
                                                          OA=(float((g.pred == g.y).mean()) if task != 'C' else np.nan), RMSE=(float(np.sqrt(((g.pred - g.y) ** 2).mean())) if task == 'C' else np.nan)))
R = pd.DataFrame(rows); R['order'] = R.model.map({m: i for i, m in enumerate(ORDER)}); R = R.sort_values(['task', 'order']).drop(columns='order')
best = {t: R[R.task == t].sort_values(MAIN[t]).model.iloc[-1] for t in 'ABC'}; bestml = {t: R[(R.task == t) & (R.family == 'ML')].sort_values(MAIN[t]).model.iloc[-1] for t in 'ABC'}
R.to_csv(os.path.join(O, 'L7_metrics.csv'), index=False); pd.DataFrame(cms).to_csv(os.path.join(O, 'L7_confusion.csv'), index=False)
pd.DataFrame(strata).to_csv(os.path.join(O, 'L7_strata.csv'), index=False); pd.DataFrame(low).to_csv(os.path.join(O, 'L7_low_severity.csv'), index=False)
json.dump(dict(best=best, best_ml=bestml, n_test=int((M.split == 'TEST').sum()), models=int(len(R))), open(os.path.join(O, 'L7_best.json'), 'w'), indent=1)
pd.set_option('display.width', 250); print(R[['task', 'model', 'OA', 'kappa', 'macro_F1', 'AUC', 'QWK', 'within1', 'R2', 'RMSE', 'RPD', 'CI_low', 'CI_high']].round(3).to_string(index=False)); print('best', best, 'best ML', bestml)
