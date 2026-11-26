from c_lib import *
import re

SRC = open('/home/user/meta/thesis_build/method3/mf3_end.py').read()
NS = {}


def grab(start, end):
    i = SRC.index(start); j = SRC.index(end, i)
    exec(SRC[i:j], NS)


grab("H = [['Group'", "\nP('R_{λ}")
grab("ms = [['Feature'", "\nTAB('msidx'")
grab("rgb = [['Feature'", "\nTAB('rgbfeat'")
grab("tir = ", "\nTAB('tirfeat'")


def add():
    h1('10. Work plan, software and record keeping')
    rows = [['Month', 'Work', 'Deliverable'],
            ['1', 'Parts A–B for all dates and cameras; subplot ROIs; leaf table and checks (L1)', 'calibrated, co-registered images; subplot average spectra; checked leaf table'],
            ['2', 'Parts C–D: features, covariates, split column, folds; Activity 1.1; L3–L5.1', 'feature and covariate tables; response curves (canopy and leaf)'],
            ['3', 'Activities 1.2–1.8 and L5.2–L5.7; physiology statistics', 'optimal wavelengths, WRI, VI, TTFI, DSF (canopy and leaf); Objective 1 draft'],
            ['4', 'Objective 2: selection on training plots, ML and DNN-F1 for 15 sensor sets; leaf models (L6)', 'test metrics of all sensor sets; leaf results'],
            ['5', 'Objective 2: DT-EDNet and comparison networks, ablation, SHAP, covariate baseline, maps; L7–L9', 'network comparison; maps; leaf–canopy link'],
            ['6', 'Objective 3 and L10; Bharatpur independent test; glasshouse data; writing', 'earliest detection day; risk maps; independent test; thesis chapters']]
    tab('plan', rows=rows, caption='Six-month analysis plan.', widths=[900, 5200, 3500], size=16)
    rows = [['Task', 'Software'], ['Image processing, registration, resampling, ROI averages', 'ENVI or Python (GDAL, rasterio); Agisoft Metashape for mosaics'],
            ['Features, selection, machine learning', 'Python: numpy, pandas, scikit-learn, shap, ReliefF, mRMR, mlxtend (SFFS)'], ['Deep learning', 'PyTorch'], ['ASD files', 'ASD ViewSpec export; Python for the leaf table']]
    tab('software', rows=rows, caption='Software.', widths=[3600, 6000], size=16)
    bl('Fix random seeds (42); store the split column, inner folds and validation plots as files and reuse them for every sensor set and model.',
       'Log every setting: bands removed, ROI files, selected features, hyper-parameters, epochs.',
       'Keep raw, intermediate and final tables separate and versioned; never overwrite the raw ASD or image files.')

    h1('11. Definitions of indices and features')
    p('R_{λ} is the reflectance at λ nm (nearest available band). The same 48 published indices and 3 red-edge parameters are used for the UAV HS data (Step C2) and the ASD leaf spectra (Step L4).')
    tab('hsidx', rows=NS['H'], caption='The 39 base hyperspectral indices with formulas and original references.', widths=[1900, 1700, 4100, 1900], size=15)
    tab('hsidx2', rows=NS['H2T'], caption='The 9 SWIR disease indices, the 3 red-edge parameters and the data-driven indices.', widths=[1900, 1700, 4100, 1900], size=15)
    NS['H2T'] = [[c.replace('Ramalingam et al. 2026', 'Selvaprakash et al. 2026') for c in r] for r in NS['H2T']]
    ms = [r for r in NS['ms']]; ms = [[c.replace('[[T:rgbfeat]]', 'Table below') for c in r] for r in ms]
    tab('msidx', rows=ms, caption='Multispectral features.', widths=[2200, 5000, 2400], size=15)
    tab('rgbidx', rows=NS['rgb'], caption='RGB colour indices and GLCM texture measures; P(i, j) is the normalised frequency of grey levels i and j in neighbouring pixels.', widths=[2300, 4900, 2400], size=15)
    tab('tiridx', rows=NS['tir'], caption='Thermal features.', widths=[2800, 4500, 2300], size=15)

    h1('12. Likely questions of the Advisory Committee')
    qa('Why a 7:3 split by whole plots?', 'The 7:3 proportion is that of the DT-EDNet study (Ma et al., 2026) and close to the one-third hold-out of Mandal et al. (2023). Whole plots are assigned so that subplots and leaves of one plot are never in both training and test data; the test then measures performance on new plots.')
    qa('How are the models tuned without the test plots?', 'Inside the 33 training plots: GroupKFold(3) by plot for the machine-learning models, as Tian et al. (2021) and Lv et al. (2023) used cross-validation for SFFS and the SVM, and one third of the training plots for the early stopping of the networks, as Ma et al. (2026) used a validation set.')
    qa('Why five scored plants but only one ASD plant per subplot?', 'Five plants (centre and corners) give a disease index that represents the subplot seen by the UAV, with the leaf-based formula of Mishra et al. (2009) and Liu et al. (2024). The ASD is slow, so only the centre plant is measured: 576 leaves per date, as many per date as the 2025-26 ASD data, and every ASD leaf still has its own grade (Mandal et al., 2023).')
    qa('Why one feature-selection method per type of feature?', 'Bands are many and collinear (SHAP-CARS), indices must separate overlapping classes (ReliefF) and texture features are correlated (mRMR); this is the design of Ma et al. (2026).')
    qa('What is new for white rust?', 'A White Rust Index in the form of Mahlein et al. (2013); the first comparison of four UAV cameras and their 15 combinations for white rust; leaf and canopy analysed on the same subplots and dates; and a pre-symptomatic test with labels from the later status (Zhu et al., 2017).')
    qa('Why are the features of Objective 1 selected on the training plots only?', 'The selected features are the inputs of the models; if the test plots had helped to choose them, the test accuracy would be optimistic. Ma et al. (2026) also selected features on their training data only. The descriptive analyses (curves, correlations, physiology) still use all plots because nothing from them enters a model.')
    qa('Why compare with a covariate-only model?', 'Severity follows time and weather (Chattopadhyay et al., 2011); Zhang et al. (2014a) showed that remote sensing must be judged against a weather-only model. The cameras are credited only with their gain over it.')
    qa('Is the dataset large enough for DT-EDNet?', 'About 880 fitting and 440 validation samples per task is small for a transformer; this is why identical settings, early stopping and strong ML baselines are used, and why the pseudo-image networks are not used for the pre-symptomatic data.')
    qa('Why are flowers kept in the subplot average spectrum?', 'Staghead and inflorescence infection belong to the disease; growth stage is recorded and results are reported by stage so that selected features are not flowering effects (Blasch et al., 2023; Liu et al., 2024).')
    qa('How will the results reach farmers\' fields and satellites?', 'The frozen models are tested once at Bharatpur (Ma et al., 2026); the WRI and selected bands can be simulated for satellite bands as done for yellow rust (Zheng et al., 2018) and rice bacterial leaf blight (Das et al., 2015).')
