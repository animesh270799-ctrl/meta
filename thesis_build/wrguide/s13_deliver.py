"""STEP 13 (I1): collect the delivered models (= the tested models, trained on TRAIN only) with the selection and the code needed by predict_new.py."""
import os, shutil, glob, json
import config as C
D = os.path.join(C.BASE, 'deliver'); os.makedirs(os.path.join(D, 'ml'), exist_ok=True); os.makedirs(os.path.join(D, 'dl'), exist_ok=True)
for f in glob.glob(os.path.join(C.OUT, '07_ml_models', '*.joblib')): shutil.copy(f, os.path.join(D, 'ml'))
for f in glob.glob(os.path.join(C.OUT, '08_dl_models', '*.pt')): shutil.copy(f, os.path.join(D, 'dl'))
shutil.copy(os.path.join(C.OUT, '06_selection_train.json'), os.path.join(D, 'selection_train.json'))
print('CHECK: %d ML and %d DL models in %s; use: python predict_new.py <new_spectra.xlsx>' % (len(glob.glob(os.path.join(D, 'ml', '*'))), len(glob.glob(os.path.join(D, 'dl', '*'))), D))
