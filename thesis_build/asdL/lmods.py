"""Shared model definitions (Step L6) and metric functions (Step L7) used by l07_ml.py, l09_eval.py, l10_cov.py and l12_stability.py."""
import numpy as np, pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, SVR
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import roc_auc_score, cohen_kappa_score, confusion_matrix, precision_recall_fscore_support, r2_score
import configL as C

class PLSDA(BaseEstimator, ClassifierMixin):
    """PLS-DA: PLS regression on the one-hot class matrix; the class with the largest predicted value is assigned (Barker and Rayens, 2003)."""
    def __init__(self, n_components=2): self.n_components = n_components
    def fit(self, X, y):
        self.classes_ = np.unique(y); Yd = (np.asarray(y)[:, None] == self.classes_[None, :]).astype(float)
        self.pls_ = PLSRegression(min(self.n_components, X.shape[1]), scale=True).fit(X, Yd); return self
    def decision_function(self, X): return self.pls_.predict(X)
    def predict(self, X): return self.classes_[self.decision_function(X).argmax(1)]
class PLSR(BaseEstimator, RegressorMixin):
    """PLS regression (Wold et al., 2001); components capped at the number of features."""
    def __init__(self, n_components=2): self.n_components = n_components
    def fit(self, X, y): self.pls_ = PLSRegression(min(self.n_components, X.shape[1]), scale=True).fit(X, y); return self
    def predict(self, X): return self.pls_.predict(X).ravel()

def base(model, task):
    """Default settings used inside SFFS (scikit-learn defaults; RF 500 trees; k-NN k = 5; PLS 2 components); balanced class weights."""
    if task in 'AB':
        return {'SVM': make_pipeline(StandardScaler(), SVC(C=1, gamma='scale', class_weight='balanced')), 'RF': RandomForestClassifier(500, class_weight='balanced', random_state=C.SEED, n_jobs=4),
                'k-NN': make_pipeline(StandardScaler(), KNeighborsClassifier(5)), 'PLS': PLSDA(2)}[model]
    return {'SVM': make_pipeline(StandardScaler(), SVR(C=1, gamma='scale', epsilon=0.1)), 'RF': RandomForestRegressor(500, random_state=C.SEED, n_jobs=4),
            'k-NN': make_pipeline(StandardScaler(), KNeighborsRegressor(5)), 'PLS': PLSR(2)}[model]
def grid(model, task, p):
    if model == 'SVM':
        return {'svc__C': [0.1, 1, 10, 100], 'svc__gamma': [0.001, 0.01, 0.1, 'scale']} if task in 'AB' else {'svr__C': [0.1, 1, 10, 100], 'svr__gamma': [0.001, 0.01, 0.1, 'scale'], 'svr__epsilon': [0.1, 0.5]}
    if model == 'RF': return {'max_features': ['sqrt', 0.3], 'min_samples_leaf': [1, 3, 5]}
    if model == 'k-NN':
        s = 'kneighborsclassifier__' if task in 'AB' else 'kneighborsregressor__'; return {s + 'n_neighbors': [3, 5, 7, 9, 11], s + 'weights': ['uniform', 'distance']}
    return {'n_components': list(range(1, min(C.MAX_PLS, p) + 1))}
def score_of(est, X, task):
    """Continuous score of the diseased class for the AUC (Task A only)."""
    if task != 'A': return None
    if isinstance(est, PLSDA): d = est.decision_function(X); return d[:, 1] - d[:, 0]
    if hasattr(est, 'predict_proba'):
        try: return est.predict_proba(X)[:, 1]
        except AttributeError: pass
    return est.decision_function(X)

MAIN = {'A': 'macro_F1', 'B': 'macro_F1', 'C': 'R2'}
def cls(y, yp, K, s=None):
    y = np.asarray(y).astype(int); yp = np.asarray(yp).astype(int); labs = list(range(K)); cm = confusion_matrix(y, yp, labels=labs)
    pr, rc, f1, _ = precision_recall_fscore_support(y, yp, labels=labs, zero_division=0)
    o = dict(n=len(y), OA=(y == yp).mean(), kappa=cohen_kappa_score(y, yp), macro_P=pr.mean(), macro_R=rc.mean(), macro_F1=f1.mean())
    if K == 2:
        tn, fp, fn, tp = cm.ravel(); o.update(sensitivity=tp / max(tp + fn, 1), specificity=tn / max(tn + fp, 1), balanced_acc=(tp / max(tp + fn, 1) + tn / max(tn + fp, 1)) / 2, F1_healthy=f1[0], F1_diseased=f1[1])
        if s is not None and not pd.isna(s).any() and len(np.unique(y)) == 2: o['AUC'] = roc_auc_score(y, s)
    else:
        o['QWK'] = cohen_kappa_score(y, yp, weights='quadratic'); o['within1'] = (np.abs(y - yp) <= 1).mean()
        for i, g in enumerate(C.GRADES): o['F1_g%d' % g] = f1[i]; o['recall_g%d' % g] = rc[i]; o['precision_g%d' % g] = pr[i]
    return {k: float(v) for k, v in o.items()}, cm
def reg(y, yp):
    y = np.asarray(y, float); yp = np.asarray(yp, float); rmse = np.sqrt(((y - yp) ** 2).mean())
    return {k: float(v) for k, v in dict(n=len(y), R2=r2_score(y, yp), RMSE=rmse, MAE=np.abs(y - yp).mean(), RPD=y.std(ddof=1) / rmse, bias=(yp - y).mean(), r=np.corrcoef(y, yp)[0, 1]).items()}
def metrics(task, y, p, s=None):
    if task == 'C': return reg(y, p), None
    return cls(y, p, 2 if task == 'A' else 6, s if task == 'A' else None)
def main_value(task, y, p, s=None):
    try: return metrics(task, y, p, s)[0][MAIN[task]]
    except (ValueError, ZeroDivisionError): return np.nan
