import json
IDX = json.load(open(B + 'idx_tables.json'))
def INDEX_TABLES():
    hs = [r for r in IDX['hs']]
    hs[-1] = ['Disease-specific', 'WRI', 'ND(λ_{1}, λ_{2}) + w R_{λ3}, searched in step O1-4', 'Mahlein et al. 2013 (method)']
    swir = [['SWIR disease–water', 'DWSI-2; DWSI-3', 'R_{1660}/R_{550};  R_{1660}/R_{680}', 'Apan et al. 2004'], ['', 'DWSI-5', '(R_{800} + R_{550})/(R_{1660} + R_{680})', 'Apan et al. 2004'],
            ['', 'NDWI', '(R_{860} − R_{1240})/(R_{860} + R_{1240})', 'Gao 1996'], ['', 'MSI', 'R_{1600}/R_{820}', 'Hunt and Rock 1989'], ['', 'NDII', '(R_{819} − R_{1649})/(R_{819} + R_{1649})', 'Hardisky et al. 1983'],
            ['', 'RBI; NDBI', 'R_{1148}/R_{1301};  (R_{1148} − R_{1301})/(R_{1148} + R_{1301})', 'Mandal et al. 2023'], ['', 'RBI_{R}', '(R_{1068} − R_{1560})/(R_{1068} + R_{1560})', 'Ramalingam et al. 2026']]
    rows = [['Group', 'Index', 'Formula', 'Reference']] + hs[:-1] + swir + [hs[-1]]
    H2('Index and feature definitions')
    P('The tables below define every index and feature used. Formulas were checked against the original papers; R_{λ} is the reflectance at λ nm (the nearest available band is used).')
    TAB('hsidx', rows, 'Hyperspectral indices (39 base indices, 9 SWIR disease and water indices and the White Rust Index).', [1600, 1700, 4206, 1800], 15)
    ms = [['Feature', 'Formula (B, G, R, RE, NIR = 475, 560, 668, 717, 840 nm)', 'Reference'], ['Band reflectance (5)', 'subplot mean reflectance of B, G, R, RE, NIR', 'Liu et al. 2024'],
          ['NDVI', '(NIR − R)/(NIR + R)', 'Rouse et al. 1974'], ['GNDVI', '(NIR − G)/(NIR + G)', 'Gitelson et al. 1996'], ['NDRE', '(NIR − RE)/(NIR + RE)', 'Gitelson and Merzlyak 1994'], ['CI_{green}', 'NIR/G − 1', 'Gitelson et al. 2003'], ['CI_{rededge}', 'NIR/RE − 1', 'Gitelson et al. 2003'],
          ['MTCI', '(NIR − RE)/(RE − R)', 'Dash and Curran 2004'], ['OSAVI', '1.16(NIR − R)/(NIR + R + 0.16)', 'Rondeaux et al. 1996'], ['SAVI', '1.5(NIR − R)/(NIR + R + 0.5)', 'Huete 1988'], ['TCARI', '3[(RE − R) − 0.2(RE − G)(RE/R)]', 'Haboudane et al. 2002'],
          ['MCARI', '[(RE − R) − 0.2(RE − G)](RE/R)', 'Daughtry et al. 2000'], ['MSR', '(NIR/R − 1)/√(NIR/R + 1)', 'Chen 1996'], ['PSRI_{MS}', '(R − G)/NIR', 'Merzlyak et al. 1999'], ['NDSI (10)', '(B_{i} − B_{j})/(B_{i} + B_{j}) for all band pairs', 'Ma et al. 2026 (search)'],
          ['Texture (40)', '8 GLCM measures (Table [[T:rgbfeat]]) of each of the 5 bands', 'Haralick et al. 1973; Liu et al. 2024']]
    TAB('msidx', ms, 'Multispectral features.', [2000, 4900, 2406], 15)
    rgb = [['Feature', 'Equation', 'Reference'], ['Chromatic coordinates', 'r = R/(R+G+B), g = G/(R+G+B), b = B/(R+G+B)', 'Woebbecke et al. 1995'], ['ExG', '2g − r − b', 'Woebbecke et al. 1995'], ['ExR', '1.4r − g', 'Meyer and Neto 2008'], ['ExG − ExR', 'ExG − ExR', 'Meyer and Neto 2008'],
           ['VARI', '(G − R)/(G + R − B)', 'Gitelson et al. 2002'], ['GLI', '(2G − R − B)/(2G + R + B)', 'Louhaichi et al. 2001'], ['NGRDI', '(G − R)/(G + R)', 'Tucker 1979'], ['HSV (3)', 'mean hue, saturation and value of vegetation pixels', '—'],
           ['Mean, MEA', 'Σ_{i} Σ_{j} i P(i, j)', 'Haralick et al. 1973'], ['Variance, VAR', 'Σ_{i} Σ_{j} (i − μ)^{2} P(i, j)', 'Haralick et al. 1973'], ['Homogeneity, HOM', 'Σ_{i} Σ_{j} P(i, j) / [1 + (i − j)^{2}]', 'Haralick et al. 1973'], ['Contrast, CON', 'Σ_{i} Σ_{j} (i − j)^{2} P(i, j)', 'Haralick et al. 1973'],
           ['Dissimilarity, DIS', 'Σ_{i} Σ_{j} |i − j| P(i, j)', 'Haralick et al. 1973'], ['Entropy, ENT', '− Σ_{i} Σ_{j} P(i, j) ln P(i, j)', 'Haralick et al. 1973'], ['Second moment, SEC', 'Σ_{i} Σ_{j} P(i, j)^{2}', 'Haralick et al. 1973'], ['Correlation, COR', 'Σ_{i} Σ_{j} (i − μ_{i})(j − μ_{j}) P(i, j) / (σ_{i} σ_{j})', 'Haralick et al. 1973']]
    TAB('rgbfeat', rgb, 'RGB colour indices and GLCM texture measures (texture of R, G and B at native resolution: 24 features). P(i, j) is the normalised frequency of grey levels i and j in neighbouring pixels (distance 1, four directions averaged).', [2100, 4800, 2406], 15)
    tir = [['Feature', 'Definition', 'Reference'], ['CT statistics (5)', 'mean, median, SD, 10th and 90th percentile of vegetation-pixel temperature', 'Liu et al. 2024'], ['CTD', 'CT − T_{air}', 'Feng et al. 2022'], ['CTR', '(CT + 273.15)/(T_{air} + 273.15)', 'Feng et al. 2022'],
           ['NRCT', '(CT − CT_{min})/(CT_{max} − CT_{min}) over the field on that date', 'Elsayed et al. 2017'], ['ΔT', 'CT − mean CT of healthy plots of the same date and variety', 'Oerke et al. 2006'], ['CWSI', '(CT − T_{wet})/(T_{dry} − T_{wet}) with wet and dry references', 'Idso et al. 1981; Jones et al. 2009'],
           ['Thermal texture (8)', 'GLCM measures of the temperature image quantised over one common range', 'Haralick et al. 1973']]
    TAB('tirfeat', tir, 'Thermal features.', [2000, 4900, 2406], 15)
EQS_PRE = r"""
P('**Spectral angle used by SAM** (Kruse et al., 1993), between a pixel spectrum t and an endmember spectrum r over n bands; smaller angles mean more similar spectra:')
EQ('α = cos^{−1} [ Σ_{i} t_{i} r_{i} / ( √(Σ_{i} t_{i}^{2}) √(Σ_{i} r_{i}^{2}) ) ]')
"""
EQS_IDX = r"""
P('**Index forms searched** (Mahlein et al., 2013; Ma et al., 2026):')
EQ('NDSI(λ_{1}, λ_{2}) = (R_{λ1} − R_{λ2}) / (R_{λ1} + R_{λ2});    WRI = NDSI(λ_{1}, λ_{2}) + w R_{λ3},  w ∈ {−1, −0.5, 0, 0.5, 1}')
"""
EQS_VIF = r"""
P('**Variance inflation factor** of feature j, where R_{j}^{2} is the coefficient of determination of feature j regressed on all other features (Dormann et al., 2013):')
EQ('VIF_{j} = 1 / (1 − R_{j}^{2})')
"""
EQS_MET = r"""
H2('Equations of the evaluation metrics')
P('For classification, TP, TN, FP and FN are counted per class; p_{o} is the observed and p_{e} the chance agreement; O_{ij} and E_{ij} are the observed and chance-expected counts of true class i predicted as j among k ordered classes (Cohen, 1960, 1968; Sokolova and Lapalme, 2009). For regression, y is the observed and ŷ the predicted score (Chang et al., 2001).')
EQ('OA = (TP + TN)/N;    precision P = TP/(TP + FP);    recall R = TP/(TP + FN);    F1 = 2PR/(P + R);    macro-F1 = (1/k) Σ_{c} F1_{c}')
EQ('κ = (p_{o} − p_{e}) / (1 − p_{e});    κ_{w} = 1 − Σ w_{ij} O_{ij} / Σ w_{ij} E_{ij},  w_{ij} = (i − j)^{2}/(k − 1)^{2}')
EQ('R^{2} = 1 − Σ (y − ŷ)^{2} / Σ (y − ȳ)^{2};    RMSE = √[ (1/n) Σ (y − ŷ)^{2} ];    RPD = SD_{y} / RMSE')
"""
MODELS = r"""
TAB('models', [['Model', 'How it works', 'Why it suits this dataset'],
 ['SVM / SVR', 'finds the boundary (or regression tube) with the largest margin; the RBF kernel allows curved boundaries', 'works well with a few hundred to a few thousand samples and correlated features (Cortes and Vapnik, 1995)'],
 ['RF / RFR', 'averages many decision trees grown on bootstrap samples and random feature subsets', 'robust to noise and non-linear effects; little tuning (Breiman, 2001)'],
 ['XGBoost', 'adds trees one after another, each correcting the errors of the previous ones, with regularisation', 'often the most accurate tree model on tabular features (Chen and Guestrin, 2016)'],
 ['k-NN', 'predicts from the k most similar training samples', 'simple reference model; good with compact standardised feature sets (Cover and Hart, 1967)'],
 ['PLS-DA / PLSR', 'projects correlated features onto a few latent variables that best predict the target', 'standard chemometric model for correlated spectral features (Wold et al., 2001; Barker and Rayens, 2003)'],
 ['DNN-F1', 'dense neural network on the concatenated features of all sensors', 'learns non-linear interactions between sensors (Maimaitijiang et al., 2020)'],
 ['DNN-F2', 'one sub-network per sensor, sensor attention, then joint layers', 'processes each sensor separately and learns sensor weights (Maimaitijiang et al., 2020; Hu et al., 2018)']],
 'How each model works and why it was chosen.', [1600, 3900, 3806], 15)
"""
