"""Model definitions and tuning grids of a3_ml.py (shared with a9_final.py)."""
from sklearn.svm import SVC, SVR
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
import xgboost as xgb
from wr_features import PLSDA, PLSR

def models(task, p):
    if task in 'AB':
        return {'SVM': (SVC(C=10, gamma='scale', class_weight='balanced', probability=False), {'C': [0.1, 1, 10, 100], 'gamma': [0.001, 0.01, 0.1, 'scale']}),
                'RF': (RandomForestClassifier(100, class_weight='balanced', random_state=42, n_jobs=1), {'n_estimators': [500], 'max_features': ['sqrt', 0.3], 'min_samples_leaf': [1, 3, 5]}),
                'XGBoost': (xgb.XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1, subsample=0.8, n_jobs=1, random_state=42, verbosity=0), {'n_estimators': [200, 500], 'max_depth': [3, 5], 'learning_rate': [0.05, 0.1]}),
                'k-NN': (KNeighborsClassifier(7, weights='distance'), {'n_neighbors': [3, 5, 7, 9, 11], 'weights': ['uniform', 'distance']}),
                'PLS-DA': (PLSDA(min(5, p)), {'n_components': list(range(1, min(15, p) + 1))})}
    return {'SVM': (SVR(C=10, gamma='scale'), {'C': [0.1, 1, 10, 100], 'gamma': [0.001, 0.01, 0.1, 'scale'], 'epsilon': [0.1, 0.5]}),
            'RF': (RandomForestRegressor(100, random_state=42, n_jobs=1), {'n_estimators': [500], 'max_features': ['sqrt', 0.3], 'min_samples_leaf': [1, 3, 5]}),
            'XGBoost': (xgb.XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1, subsample=0.8, n_jobs=1, random_state=42, verbosity=0), {'n_estimators': [200, 500], 'max_depth': [3, 5], 'learning_rate': [0.05, 0.1]}),
            'k-NN': (KNeighborsRegressor(7, weights='distance'), {'n_neighbors': [3, 5, 7, 9, 11], 'weights': ['uniform', 'distance']}),
            'PLS': (PLSR(min(5, p)), {'n_components': list(range(1, min(15, p) + 1))})}

