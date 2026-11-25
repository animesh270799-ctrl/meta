from dsl import *


def add():
    h1('6. Objective 2 methods: models, metrics and the covariate baseline')
    h2('6.1 How each model was built inside a fold')
    p('Inside every outer training part, the model-building followed the same four steps:')
    nl('**Fold-wise Objective 1:** the effective ranges, SHAP-CARS, the indices, ReliefF and the VIF check were repeated on the training leaves only, giving a disease-specific feature set for that fold and task.',
       '**Sequential floating forward selection (SFFS):** each machine-learning model chose its own compact subset of these features. SFFS adds the feature that improves the inner '
       'score most, and after each addition tries removing a feature again ("floating"), which avoids getting stuck with an early poor choice (Pudil et al., 1994). Up to 15 features; '
       'the smallest subset within 1% of the best inner score was kept, to favour simple models.',
       '**Grid search:** the model settings (hyper-parameters) were chosen from a small grid by the inner GroupKFold(3) score.',
       '**Standardisation:** every feature was centred and scaled with the mean and SD of the training leaves only, and the same values were applied to the test leaves.')
    h2('6.2 The machine-learning models')
    tab('mlmodels', 16, widths=[1500, 3100, 3300, 1700], size=17)
    p('In plain terms:')
    bl('**Support vector machine (SVM / SVR):** finds the boundary between classes that leaves the widest possible margin; the radial-basis kernel lets the boundary curve. '
       'Strong on small, well-chosen feature sets (Cortes and Vapnik, 1995).',
       '**Random forest (RF):** grows 500 decision trees, each on a random sample of leaves and features, and lets them vote (classes) or averages them (score). Robust and hard '
       'to over-fit (Breiman, 2001).',
       '**XGBoost:** builds trees one after another, each correcting the errors of the previous ones, with regularisation to control over-fitting (Chen and Guestrin, 2016).',
       '**k-nearest neighbours (k-NN):** gives a leaf the grade most common among its k most similar training leaves. Simple and a useful reference (Cover and Hart, 1967).',
       '**PLS-DA / PLSR:** the classical chemometric method: compresses the features into a few latent components and classifies (DA) or regresses (R) on them (Wold et al., 2001).')
    read(shows='The five machine-learning methods, their principle, the settings searched, and the original reference.',
         how='"Grid searched" lists the values tried; the best combination was chosen inside each fold by the inner cross-validation score.',
         means='The set covers the main families: kernel (SVM), bagged trees (RF), boosted trees (XGBoost), instance-based (k-NN) and linear latent-variable models (PLS). '
               'Class weights were balanced in all of them, so the rare grade 9 was not ignored.',
         say='"Five standard machine-learning methods, each tuned and given its own feature subset inside every fold."')
    h2('6.3 The deep-learning models')
    tab('dlcard', 17, widths=[2200, 7400], size=17, boldfirst=True, subs=True)
    p('Five networks were compared:')
    bl('**DNN-F1:** a small fully connected network (about 3000 weights) that takes the feature vector directly – the deep-learning counterpart of the machine-learning models.',
       '**DT-EDNet** (Ma et al., 2026): the network proposed for early rice-blast detection. It embeds the input, re-weights its channels with a squeeze-and-excitation (SE) '
       'block, passes it through a dual transformer group (DTG: a kernel transformer block with CBAM attention and four token transformer blocks) and classifies from a class token.',
       '**EfficientNet-B0, ResNet18, ConvNeXt V2-Atto:** well-known image networks used as comparisons in the DT-EDNet paper (Tan and Le, 2019; He et al., 2016; Woo et al., 2023).')
    box('What is a "pseudo-image"?', ['Image networks need a grid of pixels. Leaf spectra after selection are a list of 10–16 numbers. The numbers were therefore placed in a '
                                      'k × k grid (k = ⌈√p⌉ = 4 here), with zeros filling the empty cells (Sharma et al., 2019).',
                                      'Such a 4 × 4 "image" is only an arrangement of features: neighbouring cells are not neighbouring places on a leaf. This is important for understanding '
                                      'why the image networks did not outperform simpler models (Chapter 8.4).'], kind='method')
    h3('How DT-EDNet processes an input, step by step')
    nl('**Embedding:** a 3 × 3 convolution turns the 4 × 4 input into 128 feature maps – 128 different "views" of the input.',
       '**Squeeze-and-excitation (SE):** the network summarises each of the 128 maps by its average, learns which maps matter, and scales them up or down (Hu et al., 2018).',
       '**Kernel transformer block with CBAM:** an attention block that learns where (spatial attention) and on which maps (channel attention) to concentrate (Woo et al., 2018).',
       '**Four token transformer blocks:** the maps are cut into small "tokens" and a transformer lets every token look at every other token through four attention heads (Vaswani et al., 2017), so relations between distant parts of the input can be learned.',
       '**Class token and output:** a special token collects the information from all others and is turned into the class probabilities (or the score).')
    p('Each of these components is designed to find structure in an image – which parts of it matter and how they relate. On a real hyperspectral image of a canopy, that structure '
      'exists (lesions, leaves, background); on a 4 × 4 arrangement of features it largely does not. Keeping this in mind explains the ablation results in Chapter 8.4.')
    read(why='DT-EDNet and its comparison networks are part of the thesis methodology; testing them on leaf data shows how they behave before the UAV images are available.',
         done=['Settings of the DT-EDNet paper: AdamW optimiser (learning rate 6 × 10^{−4}, weight decay 10^{−5}), cosine decay, batch 32, label smoothing 0.01, gradient clipping, class-weighted loss.',
               'Up to 100 epochs with early stopping (patience 20) on one third of the training plots used as validation; seed 42; CPU training; no extra tuning.',
               'Stems with stride 1, because a 4 × 4 input would vanish after the usual down-sampling.'],
         caution='The networks were not tuned separately, so their ranking could change slightly with tuning. DNN-F2 (fusion of several sensors) does not apply to one sensor.',
         say='"I trained the four image networks of the DT-EDNet paper and a plain dense network with the paper\'s settings, using the selected features arranged as small pseudo-images."')
    h2('6.4 How performance was measured')
    tab('metrics', 18, widths=[2400, 5700, 1500], size=17)
    p('The metrics are easiest to understand with a real example. For detection, the best model (SVM) produced the following pooled confusion matrix over the 2330 test leaves:')
    tab('cmsvm', rows=[['', 'Predicted healthy', 'Predicted diseased', 'Total'], ['Observed healthy (grade 0)', '460 (true negatives)', '92 (false positives)', '552'],
                       ['Observed diseased (grade > 0)', '301 (false negatives)', '1477 (true positives)', '1778'], ['Total', '761', '1569', '2330']],
        caption='Worked example: detection confusion matrix of the SVM (pooled leave-one-replication-out test predictions).', widths=[3000, 2400, 2400, 1800])
    bl('**Overall accuracy (OA)** = (460 + 1477) / 2330 = 0.831: 83% of leaves were classified correctly.',
       '**Sensitivity** = 1477 / 1778 = 0.831: 83% of diseased leaves were found. **Specificity** = 460 / 552 = 0.833: 83% of healthy leaves were correctly called healthy.',
       '**F1** of a class combines precision (how many of the leaves called "diseased" really are) and recall (how many diseased leaves were found): F1 = 2PR/(P + R). '
       '**Macro-F1** is the simple average of the F1 of all classes, so a small class counts as much as a large one (Sokolova and Lapalme, 2009). For this SVM macro-F1 = 0.792.',
       '**Cohen\'s kappa** compares the agreement with what chance alone would give: 0 = no better than chance, 1 = perfect (Cohen, 1960). Here 0.587.',
       '**AUC** (area under the ROC curve) is the probability that a randomly chosen diseased leaf receives a higher disease score than a randomly chosen healthy leaf: 0.5 = chance, 1 = perfect '
       '(Fawcett, 2006). Here 0.897.')
    p('For six grades two further measures matter, because the grades are ordered:')
    bl('**Quadratic weighted kappa (QWK)** gives partial credit: predicting grade 5 for a grade-7 leaf is a small error, predicting grade 0 is a large one; the penalty grows with the square of the distance (Cohen, 1968).',
       '**Within one grade** is the share of leaves predicted in the correct class or a neighbouring one.')
    p('For the severity score: **R²** (share of the variation in grade explained by the model), **RMSE** and **MAE** (typical error in grade units), **bias** (average over- or '
      'under-prediction) and **RPD** = SD of the observed grades / RMSE. RPD above 2 is usually called good, 1.4–2 fair and below 1.4 poor (Williams, 2001).')
    read(shows='The definition and purpose of each metric, and which task it is used for.',
         means='No single metric tells the whole story. Macro-F1 is the main metric for classes because the classes are unequal; QWK and "within one grade" are essential for the '
               'ordered six grades, because a near-miss is not the same as a gross error; R² and RMSE describe the score in grade units that a pathologist understands.',
         say='"I report macro-F1 because the classes are unequal, AUC for detection, weighted kappa for the ordered grades, and R² and RMSE in grade units for the score."')
    h2('6.5 The covariate baseline: what can be predicted without any spectra?')
    p('Severity rose with crop age and date and differed with variety, sowing date, growth stage and weather. A spectral model could therefore look accurate simply by '
      'learning the calendar – for example "late date = more disease" – without reading anything from the leaf (De Wolf and Isard, 2007). To guard against this, a model '
      'was built that uses **only** the covariates, and the spectra were credited only with what they add to it (Kuhn and Johnson, 2013). Weather-based models can predict '
      'disease well (Bijlwan et al., 2025), and adding sensor data to weather data has improved disease forecasts in wheat (Zhang et al., 2014; Ruan et al., 2022).')
    tab('covmodels', 19, widths=[2200, 1600, 2400, 2000, 1400], size=16)
    read(shows='The three types of covariate-only model fitted for each task and the covariates each one used.',
         how='B1 is an interpretable statistical model (logistic, ordinal logistic or linear regression); the random forest and "B2" (the best machine-learning model of each task) use all covariates.',
         means='Using an interpretable model alongside flexible ones shows both how well the calendar predicts disease and in which direction each covariate acts. With only four '
               'dates the 7-day weather is the same for all leaves of a date, so weather cannot be separated from date; crop age (DAS) and DAS² stand for time in B1.',
         say='"Before crediting the spectra, I asked how much a model knowing only crop age, sowing date, variety, stage and weather could predict."')
    bl('**Samples:** only the 1952 unsprayed, naturally infected leaves. The healthy block was sprayed and shares every covariate with the unsprayed plots, so including it would teach a false rule.',
       '**Three inputs:** covariates only, leaf spectra only (the fold-wise disease-specific features) and spectra + covariates; same outer folds and inner tuning as before.',
       '**Three gains:** ΔS = spectra model − best covariate model (what the spectra add); ΔC = spectra + covariates − spectra (what the covariates add to the spectra); ΔT = spectra + covariates − covariate model.',
       '**When is a gain real?** A 95% confidence interval was obtained from 2000 bootstrap resamples that resample whole plots (Efron and Tibshirani, 1993). A gain is called real only if the '
       'interval excludes zero, the gain is larger than the fold-to-fold SD and it has the same sign in all three folds. AUCs were also compared with the DeLong test (DeLong et al., 1988).')
    box('Why this is a strict test.', 'Requiring all three conditions means a gain is accepted only when it is statistically clear, larger than the normal variation between '
        'replications and consistent across all of them. Small or erratic gains are not counted, so the spectra are not over-credited.', kind='key')
    h2('6.6 Interpretation and robustness checks')
    bl('**SHAP** of an XGBoost model on the disease-specific features shows the direction and size of each feature\'s effect (Lundberg and Lee, 2017).',
       '**Strata:** the test metrics of the best models were computed separately for each growth stage, variety, leaf position, date and sowing timing.',
       '**Transfer tests:** a random forest was trained on two varieties and tested on the third (leave-one-variety-out), and trained on three sowing dates and tested on the fourth '
       '(leave-one-timing-out), with feature selection repeated inside each training set.',
       '**Selection stability:** how often each optimal wavelength and index was chosen across the three folds.')
    h2('6.7 Software and the final models')
    p('The analysis used Python 3 with NumPy, pandas, SciPy, scikit-learn (Pedregosa et al., 2011), mlxtend (Raschka, 2018), XGBoost, SHAP and PyTorch (Paszke et al., 2019). '
      'After evaluation, every model was refitted once on all 2330 leaves with the same procedure and saved, together with the feature definitions and a prediction script for new '
      'spectra (Appendix C). These final models are the ones applied to the UAV images.')
