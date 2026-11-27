from dsl import *
import re

S = '/tmp/claude-0/-home-user-meta/c5704ca0-f1ca-5695-b9e0-a810fbe166a9/scratchpad/chair/report.md'


def references():
    L = open(S).read().splitlines(); i = max(j for j, l in enumerate(L) if l.strip() == 'References')
    refs = [l.strip() for l in L[i + 1:] if l.strip()]
    refs.append('Jacquemoud, S., Ustin, S. (2019). Leaf Optical Properties. Cambridge University Press, Cambridge. https://doi.org/10.1017/9781108686457')
    clean = []
    for r in refs:
        r = r.replace("\\'", "'").replace('--', '–').replace('\\', '')
        clean.append(r)
    return sorted(set(clean), key=lambda s: s.lower())


def add():
    h1('9. Discussion: what the results mean')
    h2('9.1 The physical basis of the white rust signal')
    p('The spectral changes agree with the biology of white rust. The pathogen destroys chlorophyll around the pustules, which raises red reflectance, lowers the red-edge peak '
      'and shifts the red-edge position towards shorter wavelengths (Horler et al., 1983; Filella and Peñuelas, 1994). The 7.7-nm blue shift between grades 0 and 9 is of the size '
      'reported for chlorophyll loss in diseased leaves (Mahlein et al., 2013; Meng et al., 2020). The white pustules and the collapse of mesophyll cells change internal '
      'scattering, which lowers the near-infrared plateau, and tissue dehydration raises reflectance in the shortwave-infrared water bands (Mishra et al., 2009; Peñuelas et al., 1997).')
    p('Two observations add nuance. First, the near-infrared change was not in the same direction at every growth stage (Chapter 7.2), so NIR reflectance alone is not a robust '
      'indicator: leaf ageing and pod formation change it as well. Second, the water-band edges (FD1245, and FD1805/FD1810 in one fold) and DWSI-2 entered the selected features, '
      'which justifies keeping the water bands in contact-probe data.')
    box('One sentence for the chairman.', '"White rust removes chlorophyll, damages the leaf structure and dries the tissue; the spectra show all three, and the red-edge position '
        'is the clearest single indicator."', kind='present')
    h2('9.2 Why derivatives work best')
    p('All 15 optimal wavelengths were first-derivative bands, and the derivative correlated more strongly with the grade than reflectance (0.62 vs 0.46). The derivative '
      'removes additive differences between leaves – thickness, surface wax, small differences in probe contact – and highlights the shape of the spectrum, especially the red '
      'edge (Tsai and Philpot, 1998). This agrees with the DT-EDNet study, where the optimal wavelengths were concentrated in the red edge and near infrared (Ma et al., 2026), and '
      'with wheat and rice disease studies that used derivative or red-edge features (Huang et al., 2020; Mandal et al., 2023). The best two-band index, NDSI(795, 805), is in '
      'effect a slope on the NIR shoulder, and the White Rust Index search did not find a useful third band: for leaf spectra, a narrow red-edge-to-NIR contrast carries most of the signal.')
    h2('9.3 Why detection is good but six grades are difficult')
    p('Detection reached macro-F1 0.79, but six-grade macro-F1 stayed near 0.36. This gap is common in leaf-level severity work and has three causes:')
    nl('**The grades are steps on a continuum.** A grade-3 leaf and a grade-5 leaf differ only in the area covered by pustules; their spectra differ by small amounts (Chapter 7.4).',
       '**The labels themselves are uncertain.** Visual raters disagree most for intermediate grades (Bock et al., 2010); some of the "errors" of the models are disagreements with an imperfect label.',
       '**The spectral distributions overlap.** The box plots and the PCA show that neighbouring grades overlap for every feature, so no model can separate them sharply.')
    p('The ordinal metrics confirm that the errors were small in grade terms (QWK 0.63; 75% within one grade). Similar patterns were reported for wheat yellow rust and Fusarium head '
      'blight, where severity classes in the middle of the scale had the lowest accuracy (Huang et al., 2020; Lv et al., 2023), and for rice blast in India (Mandal et al., 2023). '
      'The usual remedies – merging grades into three or four classes, or treating severity as a continuous score – are both part of the thesis methodology (four severity classes '
      'plus disease-index regression).')
    h2('9.4 Machine learning versus deep learning')
    p('All models performed within a narrow range. For detection, the best network (DNN-F1, 0.790) and the best machine-learning model (SVM, 0.792) differed by 0.002 – less than the '
      'fold-to-fold SD (about 0.01). For six grades, ConvNeXt V2-Atto (0.360) and RF (0.349) were within one SD; for the score, XGBoost (R² 0.459) stayed ahead of the best network '
      '(DNN-F1, 0.448). DT-EDNet reached 0.759 (detection), 0.337 (six grades) and R² 0.419 (score) and did not exceed the comparison networks at leaf level.')
    p('The reason is the input. With 10–16 selected features, the 4 × 4 pseudo-images are an arrangement of numbers rather than a picture (Sharma et al., 2019): neighbouring cells '
      'are not neighbouring places on a leaf, so the convolution and attention modules that make these networks powerful on real images have little to use. The ablation agrees – '
      'removing DT-EDNet\'s modules changed macro-F1 by only 0.01–0.02 – and the learning curves show early over-fitting. Tree ensembles and support vector machines are known to be '
      'strong on small tabular data. The real test of DT-EDNet will come in the UAV phase, where it receives genuine spatial and spectral patterns, as in the original rice-blast study.')
    box('What to say if asked "So is deep learning useless?"', '"No. At leaf level the input is a short list of numbers, which is where classical machine learning is strongest. '
        'DT-EDNet was designed for hyperspectral images; it will be tested on the UAV images of 2026-27, where it has spatial patterns to learn from."', kind='present')
    h2('9.5 The role of the calendar and the weather')
    p('Growth stage, sowing date, crop age and sampling date follow the epidemic, so a model without any sensor data already explained much of the disease level (detection macro-F1 '
      '0.78 and AUC 0.93 within unsprayed plots; six-grade macro-F1 0.31; score R² 0.33), as expected from weather- and calendar-based disease models (De Wolf and Isard, 2007; Bijlwan et al., 2025).')
    p('For severity the spectra added information that the calendar cannot give: six-grade macro-F1 rose by 0.043 and score R² by 0.083 (both real gains), because leaves of the same '
      'date, sowing and stage differ in their actual infection. Spectra and covariates together gave the best results (ΔT +0.080 for grades, +0.124 R² for the score), in line with the '
      'benefit of combining sensor and weather data reported for wheat diseases (Zhang et al., 2014; Ruan et al., 2022).')
    p('Infection was natural, so the weather before sampling matters more than the weather during it. The 17 favourable leaf-infection days occurred between 18 December 2025 and '
      '4 February 2026; none fell in the sampling period. The crops sown on 9 and 18 December were exposed to all 17, the crop sown on 9 January to 7. With four sampling dates the '
      '7-day weather is the same for every leaf of a date, so it describes the epidemic but cannot be tested as an independent predictor; the 13 UAV flights of 2026-27 and the '
      'Bharatpur data will allow that.')
    h2('9.6 Limitations')
    bl('**One season, one location.** External validation (Bharatpur, next season) is needed before the models can be used elsewhere.',
       '**Subjective labels.** Visual leaf grades contain rater error; image-based pustule area or a second rater would reduce label noise (Bock et al., 2010).',
       '**Class imbalance.** Grade 9 had only 132 leaves; class weights reduce but do not remove its disadvantage.',
       '**Confounding of stage and date.** Vegetative leaves occur only on the first two dates and pod-formation leaves only on the last two, so stage and date effects cannot be separated.',
       '**Few healthy leaves in infected plots after the first date.** This is why detection within unsprayed plots depends so much on the date.',
       '**Networks not tuned.** The networks used the paper settings on CPU; tuning could change their ranking slightly.',
       '**No pre-symptomatic data.** Objective 3 could not be addressed; it needs the pre-symptomatic flights of 2026-27.')
    h2('9.7 Implications for the UAV phase (2026-27)')
    nl('**Wavelengths:** the red edge (690–760 nm), the NIR shoulder (780–870 nm) and the SWIR water-band edges carry the disease signal; the hyperspectral camera must cover them.',
       '**Features:** keep first-derivative features and the red-edge position; do not rely on NIR reflectance alone.',
       '**Outputs:** detection is realistic at canopy level; severity should be reported as a score or a small number of classes rather than six grades.',
       '**Evaluation:** keep the leave-one-replication-out design and the covariate baseline, so that the sensor is credited only with what it adds beyond the calendar.',
       '**Models:** the saved leaf models can be used to check the UAV predictions on the leaves sampled during the flights; DT-EDNet should be tested on real image patches.')



def add_rest():
    h1('10. Conclusions')
    nl('White rust lowers near-infrared reflectance, raises red and shortwave-infrared reflectance and shifts the red-edge position by 7.7 nm towards shorter wavelengths between grade 0 and grade 9.',
       'The first derivative carries the strongest signal. SHAP-CARS selected 15 derivative bands; the best two-band index is NDSI(795, 805) (R² 0.36); the disease-specific feature set has 11 '
       'features (FD1090, FD1060, FD550, FD1245, FD870, FD760, FD665, FD595, DWSI-2, Dr, REP), with FD760, FD1060, FD1090 and FD1245 selected in every fold.',
       'Detection of diseased leaves is reliable (SVM macro-F1 0.792, AUC 0.897, sensitivity and specificity 0.83).',
       'Six-grade classification is limited by the overlap of neighbouring grades (best macro-F1 0.360) but captures the order of severity (QWK 0.633; 75% within one grade).',
       'The severity score is predicted with R² 0.459 and RMSE 2.04 grades (XGBoost); predictions are compressed towards the middle of the scale.',
       'Machine-learning and deep-learning models performed alike; DT-EDNet did not gain from its attention modules on leaf-level pseudo-images.',
       'A covariate-only model explained much of the epidemic; the spectra added a real gain for six grades (+0.043 macro-F1) and score (+0.083 R²) beyond it, and the models '
       'transferred across varieties and sowing dates.',
       'Final models trained on all 2330 leaves are saved, with a prediction script, for the UAV phase and the Bharatpur validation.')
    box('The take-home message.', 'Leaf spectra detect white rust reliably and rank its severity; they show where in the spectrum to look from the UAV; and the evaluation design '
        'makes sure the sensor is credited only for what it truly adds.', kind='key')

    # ------------------------------------------------------------------ appendices
    h1('Appendix A. Cross-check against the thesis methodology')
    p('Every step of the revised methodology that applies to leaf spectra was performed. Steps that need images (radiometric calibration, orthomosaics, crop mask, texture, thermal, '
      'fusion of 15 sensor sets) do not apply to non-imaging contact-probe data.')
    tab('check', 34, widths=[3200, 5000, 1400], size=15)
    read(shows='Each step of the thesis methodology, whether it was done with the 2025-26 leaf data, and where the result is reported.',
         found='All applicable steps were done; image-based steps, multispectral indices, texture, sensor fusion, severity maps and biochemical parameters were not applicable or not '
               'measured; Bharatpur validation and Objective 3 belong to the next season.',
         say='"Every methodology step that applies to leaf spectra has been carried out; the rest needs the UAV images of 2026-27."')

    h1('Appendix B. The Excel workbook')
    tab('sheets', 35, widths=[2600, 7000], size=16)
    read(shows='The sheets of the Excel workbook that accompanies the report.',
         means='Every table of the report is in the workbook; most sheets use live formulas (for example AVERAGEIFS mean spectra, CORREL correlations, formula-based confusion-matrix '
               'metrics), so that the method can be checked and applied to other data sets.',
         say='"All numbers can be traced in the Excel workbook, most of them as live formulas."')

    h1('Appendix C. The saved model files')
    p('After evaluation, every model was refitted on all 2330 leaves. Each machine-learning model chose its own feature subset (SFFS) from the task-specific disease-specific set '
      'computed on all leaves; this is why FD1660 (detection and grades) and MCARI (score) appear in some model files although they are not in the 11-feature set of {T:dsf}.')
    tab('mfml', 36, widths=[3600, 700, 1200, 4100], size=15)
    tab('mfdl', 37, widths=[3600, 700, 1500, 3800], size=15)
    read(shows='The machine-learning (joblib) and deep-learning (PyTorch) model files and the features each one needs.',
         how='Load any model with predict_white_rust.py; it computes the listed features from a new leaf spectrum and returns the prediction.',
         say='"The final models are saved and ready to be applied to new spectra and to the UAV data."')

    h1('Appendix D. Questions the chairman may ask – with answers')
    qa('Why did you work at leaf level and not with plot means?', 'The grade is scored on each leaf, so leaf spectra and leaf grades match one to one. Plot means would mix grades and '
       'reduce 2330 samples to 192 plot-date means. The plot structure is respected in the validation: whole replications are held out and inner folds are grouped by plot.')
    qa('Why leave-one-replication-out and not random cross-validation?', 'Leaves of one plot share soil, micro-climate, variety and timing. Random splits would place leaves of the same plot '
       'in training and test and overestimate accuracy (Roberts et al., 2017). Holding out a whole replication tests the model as it would be used on a new replication.')
    qa('The healthy plots were sprayed – is that a problem?', 'They provide true disease-free leaves of the same varieties and ages, which detection needs. They were rotated so that every '
       'test fold had four of them. For the covariate baseline they were excluded, because spraying, not the covariates, kept them healthy.')
    qa('Why were the water bands kept?', 'The contact probe has its own lamp and touches the leaf, so there is no atmospheric water absorption, and the files were splice-corrected. These '
       'regions measure leaf water, which falls in diseased tissue; FD1245 and DWSI-2 come from them.')
    qa('Why only first-derivative bands among the optimal wavelengths?', 'The derivative removes offsets between leaves and emphasises the red-edge shape, which changes with chlorophyll '
       'loss. SHAP and CARS both preferred derivatives, and the derivative correlates more strongly with grade (0.62) than reflectance (0.46).')
    qa('Why did no band pair reach R² = 0.5?', 'Single leaves vary a lot within each grade (stage, date, leaf position), so two bands can explain at most about a third of the variation. '
       'The methodology foresaw this: the top 5% of pairs was used instead.')
    qa('What is the White Rust Index and why is its third-band weight zero?', 'It adds a weighted third band to the best two-band index. For leaf spectra the best weight was zero: the '
       'third band did not improve the NIR-shoulder contrast. It may still help at canopy level, where background effects need correcting.')
    qa('Why is six-grade accuracy so low?', 'Neighbouring grades overlap spectrally and visual grades are uncertain between neighbours. Most errors are one grade apart (75% within one '
       'grade, QWK 0.63). Detection and the severity score are the reliable outputs; for the UAV phase severity will be reported as a score or a few classes.')
    qa('Is 83% detection accuracy good enough?', 'It was obtained on replications the model never saw, with balanced sensitivity and specificity and AUC 0.90. It is comparable to leaf-level '
       'results for other diseases and adequate for an early-warning layer; the decision threshold can be adjusted to the purpose (ROC curve).')
    qa('Did DT-EDNet beat the other models?', 'No. At leaf level it reached 0.337 for six grades against 0.360 for ConvNeXt V2-Atto and 0.349 for RF, all within about one fold-to-fold SD. '
       'With 10–16 features the pseudo-images have no spatial structure; its strength is expected on the UAV hyperspectral images.')
    qa('Why do the networks over-fit?', 'They have 0.95–11 million weights but only about 1000 training leaves after the validation split, and 10–16 inputs. They learn the useful pattern in '
       'a few epochs and then start memorising; early stopping on validation plots kept the best epoch.')
    qa('How do you know there is no leakage?', 'All selection (band-pair maps, SHAP-CARS, ReliefF, VIF, SFFS) and all tuning were repeated inside each training part; the test replication '
       'was used once, only for the final metrics. Standardisation used training statistics only.')
    qa('What does the covariate baseline show?', 'A model without sensor data (crop age, sowing date, variety, stage, weather) already explains much of the disease level. The spectra are '
       'credited only with the gain over it: +0.043 macro-F1 for six grades and +0.083 R² for the score, both confirmed with a plot-level bootstrap.')
    qa('Then why are spectra worse than the covariates for detection?', 'Within the unsprayed plots almost all healthy leaves are from the first date, so the date alone separates them. A '
       'sensor survey does not know the sampling calendar, and with the sprayed healthy plots included the spectra detect disease with macro-F1 0.79 and AUC 0.90.')
    qa('What do D1–D4 mean, and why did D4 have more disease at the same crop age?', 'Four sowing dates (9, 18, 27 December 2025 and 9 January 2026), i.e. crops of 50, 40, 30 and 20 days at the end of '
       'January. At equal crop age a later-sown crop is observed later in the season, when the epidemic had built up further, so the timing effect largely carries calendar time.')
    qa('Why is the predicted score compressed towards the middle?', 'When the inputs explain only part of the variation (R² 0.46), a regression model hedges towards the mean: low grades are '
       'over-predicted and high grades under-predicted. The score ranks leaves correctly and can be calibrated before use as an absolute value.')
    qa('Are the models specific to one variety or sowing date?', 'No. Trained on two varieties, a model performed as well on the third (macro-F1 0.34–0.39); trained on three sowing dates, it '
       'performed on the fourth (0.31–0.40), with RMSE close to the cross-validated value.')
    qa('Why was the first date weaker in the strata?', 'On 11 February almost all leaves were grade 0–1, so there was little range of disease; grades are hard to separate and R² within that date is low.')
    qa('Why was Objective 3 not addressed?', 'No pre-symptomatic dates were sampled in 2025-26: on the first date 45% of leaves already showed symptoms. The 2026-27 programme includes three '
       'pre-symptomatic UAV flights for this objective.')
    qa('What will change in 2026-27?', 'UAV images with 13 flights (3 pre-symptomatic), plot and subplot features, multi-sensor fusion, the four severity classes plus disease-index regression, '
       'Objective 3, and external validation at Bharatpur.')
    qa('Can these leaf models be applied directly to UAV images?', 'Not reliably: canopy pixels mix leaves, flowers, soil and shadow, and the illumination differs from the probe. The leaf '
       'results tell which wavelengths and features to use; the UAV models must be trained or calibrated on canopy data, with the leaf models used as a check.')
    qa('How many models were compared, and which would you recommend?', 'Six machine-learning methods (SVM, RF, XGBoost, k-NN, PLS-DA/PLSR) and five networks. For detection SVM, for the score '
       'XGBoost or RF; for six grades the differences are within the noise, so a simple RF or SVM is preferred over a large network.')
    qa('What is the single most important spectral indicator?', 'The red-edge position: it falls almost step by step from 709.0 nm (grade 0) to 701.3 nm (grade 9), was selected by ReliefF '
       'for every task and is among the most important SHAP features.')

    h1('Appendix E. Glossary')
    for term, d in [
        ('AUC', 'Area under the ROC curve: probability that a diseased leaf gets a higher disease score than a healthy one (0.5 = chance, 1 = perfect).'),
        ('Balanced accuracy', 'Average of sensitivity and specificity; not inflated by unequal class sizes.'),
        ('Bootstrap (plot-block)', 'Repeated resampling of whole plots with replacement to estimate the uncertainty of a metric or a gain.'),
        ('CARS', 'Competitive adaptive reweighted sampling: repeatedly removes bands with small PLS coefficients and keeps the subset with the lowest error.'),
        ('Covariate baseline', 'A model using only crop age, sowing date, variety, stage and weather – no spectra – against which the spectra are judged.'),
        ('DAS', 'Days after sowing: crop age at sampling.'),
        ('DSF', 'Disease-specific feature set: the 11 non-redundant bands and indices selected in Objective 1.'),
        ('DT-EDNet', 'Dual transformer early-detection network of Ma et al. (2026), proposed for rice blast.'),
        ('Early stopping', 'Stopping network training when the validation score stops improving, to avoid over-fitting.'),
        ('First derivative (FD)', 'The slope of the reflectance spectrum at each wavelength.'),
        ('Kappa', 'Agreement beyond chance (0 = chance, 1 = perfect). Quadratic weighted kappa gives partial credit for near-misses on an ordered scale.'),
        ('Leakage', 'Information from the test data entering model building, which inflates accuracy.'),
        ('LORO', 'Leave-one-replication-out validation: train on two replications, test on the third.'),
        ('Macro-F1', 'Average over classes of F1 (the harmonic mean of precision and recall); gives every class equal weight.'),
        ('NDSI / RSI', 'Normalised difference and ratio of two bands.'),
        ('Over-fitting', 'A model learning the training data too closely, including noise, so that it performs worse on new data.'),
        ('PCA', 'Principal component analysis: summarises many correlated variables in a few uncorrelated components.'),
        ('Pseudo-image', 'A vector of features arranged in a small square grid so that image networks can process it.'),
        ('Red edge, REP, Dr', 'The steep rise of reflectance between about 680 and 760 nm; REP is the wavelength of its steepest point, Dr the height of the derivative there.'),
        ('ReliefF', 'Feature ranking that rewards features separating nearby leaves of different classes.'),
        ('RMSE, MAE, R², RPD', 'Root mean square error, mean absolute error, explained variance and ratio of the observed SD to RMSE.'),
        ('Savitzky–Golay', 'A smoothing filter that fits a local polynomial in a moving window; it can also give derivatives.'),
        ('SFFS', 'Sequential floating forward selection: adds features one by one, re-checking whether an earlier one can be removed.'),
        ('SHAP', 'Shapley additive explanations: the contribution of each feature to each prediction.'),
        ('VIF', 'Variance inflation factor: how much a feature is explained by the others (above 10 = strongly redundant).')]:
        p(f'**{term}.** {d}')



def add_refs():
    h1('References')
    for r in references(): B.append(dict(t='p', text=r))
