from c_lib import *


def add():
    h1('8. Objective 3 – Prediction of white rust at the pre-symptomatic stage')
    p('Objective 3 uses the 576 pre-symptomatic subplot-dates (1, 4 and 7 January 2027; 2, 5 and 8 DAI): 396 from the training plots and 180 from the test plots. '
      'The question is whether subplots that will develop white rust can be separated from healthy subplots before pustules are visible. ML models, DNN-F1 and DNN-F2 are used; the pseudo-image networks are not, because about 400 training samples are too few for them.')
    P = 'Objective 3'
    step('3.1', 'Pre-symptomatic samples and labels', part=P,
         what='Healthy = subplots of the healthy plots; later-infected = inoculated subplots whose DI becomes > 0 on a later date; inoculated subplots that never show pustules are left out.',
         why='Before symptoms the label cannot be seen; it comes from the later status of the same subplot.',
         do=['Read the DI of every inoculated subplot on all later dates.', 'Label each pre-symptomatic sample; count healthy and later-infected samples in training and test plots.'],
         check=['Label table per date.'],
         out='Pre-symptomatic labels → 3.2.',
         papers=[('Zhu et al. (2017)', 'Tobacco mosaic virus; inoculated and healthy leaves imaged 2, 4 and 6 days after inoculation, before visible symptoms.', 'Early-date samples of infected and healthy plants; here infection is confirmed by later symptoms.'),
                 ('Tian et al. (2021)', 'Rice leaf blast; asymptomatic infected leaves labelled by the inoculation and later symptoms.', 'Asymptomatic infected class.'),
                 ('Yu et al. (2021)', 'Pine wilt disease; early-stage trees identified by their later development.', 'Early stage defined by later status.')])
    step('3.2', 'Healthy-baseline normalisation of the pre-symptomatic data', part=P,
         data='Healthy training plots define the constants; applied to all pre-symptomatic samples (training and test).',
         what='Pre-symptomatic spectra are aligned to a healthy baseline: for each date and variety, every spectrum is multiplied by the ratio between the healthy baseline spectrum (healthy training plots on the first flight, 1 January 2027) and the mean healthy spectrum of that date. Thermal features are used in their normalised forms (Step D3).',
         why='Before symptoms the disease signal is small compared with differences between dates and varieties; once the healthy spectra of all dates coincide with the baseline, the remaining difference of the inoculated subplots is due to infection.',
         do=['Baseline: mean reflectance of the healthy training plots of each variety on 1 January 2027.',
             'For each later pre-symptomatic date and variety: ratio(λ) = baseline(λ) / mean healthy reflectance of that date (healthy training plots).',
             'Multiply every subplot spectrum of that date and variety (healthy and inoculated, training and test) by ratio(λ); compute indices and first derivatives from the normalised spectra.',
             'Thermal: CTD, CTR, NRCT and the difference from the healthy training plots of the same date and variety (Step D3).',
             'Leaves (L10): the same normalisation with the leaves of the centre plants of the healthy training plots.'],
         check=['Normalised healthy spectra of all dates overlap the baseline.', 'All constants from healthy training plots only.'],
         out='Normalised pre-symptomatic features → 3.3.',
         alt='Not used in Objectives 1–2: there, calibrated reflectance keeps the published indices standard and lets the frozen models run at Bharatpur, where no healthy plots exist.',
         papers=[('Lv et al. (2023)', 'Southern corn leaf blight; to remove differences between cultivars and measurement dates, the spectra of every date were rescaled with the ratio between the healthy mean spectrum of that date and the healthy baseline spectrum, before asymptomatic detection.', 'Same healthy-baseline spectral normalisation, here per date and variety.'),
                 ('Oerke et al. (2006)', 'Cucumber downy mildew; infected and healthy leaf areas separated in thermograms before visible symptoms, while air temperature and humidity changed leaf temperature.', 'Thermal features compared with healthy plants of the same date.'),
                 ('Calderón et al. (2014)', 'Downy mildew of opium poppy; canopy temperature normalised by air temperature and compared between asymptomatic and symptomatic plants at similar growth (NDVI) levels.', 'Comparison against healthy plants at the same date and growth stage.'),
                 ('Zarco-Tejada et al. (2018)', 'Xylella in olive; plant traits (fluorescence, crop water stress index, pigments) from airborne imagery separated infected trees before visible symptoms; trees flagged as affected developed symptoms at about twice the rate of the others.', 'Pre-visual differences judged against healthy plants; labels confirmed by later symptoms.')])
    step('3.3', 'Pre-symptomatic feature sets and fusion on the training plots', part=P,
         what='The pre-symptomatic DSFs of Step 1.8.2 (selected on the 396 training samples) are joined for the 15 sensor sets as in Step 2.2; VIF < 10 and SFFS (at most 10 features) on the training plots.',
         why='Selection must not see the test plots.',
         do=['Take the pre-symptomatic DSF of each camera from Step 1.8.2 (training plots).', 'Join camera DSFs for the 15 sensor sets; VIF < 10; SFFS (at most 10 features).'],
         check=['Pre-symptomatic DSF per sensor set.'],
         out='Inputs → 3.4.',
         papers=[('Tian et al. (2021)', 'Rice leaf blast; features sensitive on the asymptomatic days chosen by separability (top 5%), VIF < 10, then SFFS with LDA, k-NN and SVM; 2–4 features gave over 65% accuracy at the asymptomatic stage.', 'Stage-specific selection, VIF and SFFS.'),
                 ('Ma et al. (2026)', 'Rice blast; selection on training data only.', 'Training plots only.')])
    step('3.4', 'Pre-symptomatic models', part=P,
         what='SVM, random forest, k-NN and PLS-DA (each with SFFS), DNN-F1 for all 15 sensor sets and DNN-F2 for the 11 fused sets (binary task), tuned as in Steps 2.3–2.5.',
         why='Same models and folds as Objective 2, so the stages can be compared.',
         do=['GroupKFold(3) tuning for ML; 11 validation plots for DNN-F1 and DNN-F2.', 'Predict the 180 test samples once.'],
         check=['Predictions for every model × sensor set.'],
         out='Predictions → 3.5.',
         papers=[('Zhu et al. (2017)', 'Tobacco mosaic virus; BPNN, ELM and LS-SVM on SPA-selected wavelengths and GLCM texture detected infection 48 h after inoculation (up to 95% accuracy).', 'ML classifiers on selected spectral and texture features before symptoms.'),
                 ('Tian et al. (2021)', 'Rice leaf blast; LDA, k-NN and SVM with SFFS for asymptomatic detection (4-fold cross-validation repeated 100 times).', 'Same model types with SFFS.'),
                 ('Nguyen et al. (2023)', 'Spring wheat yellow rust; a 3D-CNN on multispectral UAV images reached 60% accuracy early in the season, rising to 79% later.', 'Detection accuracy reported date by date in the early stage.')])
    step('3.5', 'Evaluation, earliest detection day and covariate baseline', part=P,
         what='Sensitivity, specificity, OA, kappa, macro-F1 and AUC on the test plots for each date; the earliest detection day is the first DAI on which predicted scores of later-infected and healthy test subplots differ significantly (t-test, p < 0.05); the covariate-only model is the reference.',
         why='Tells how early and with which camera white rust can be predicted.',
         do=['Metrics per date (2, 5, 8 DAI) and pooled.', 't-test of predicted scores per date → earliest detection day per sensor set.', 'Covariate-only model (Step 2.9) for the same samples.'],
         check=['Metrics and earliest day per sensor set.'],
         out='Earliest detection day → conclusions, 3.6.',
         papers=[('Mahlein et al. (2019)', 'Fusarium head blight; the day after inoculation on which each sensor first detected infection was compared.', 'Earliest detection day per sensor.'),
                 ('Gold et al. (2020)', 'Potato late and early blight; pre-symptomatic detection accuracy by day after inoculation.', 'Accuracy by date before symptoms.'),
                 ('Zhang et al. (2014a)', 'Wheat powdery mildew; meteorological model as the reference for remote-sensing models.', 'Covariate reference.'),
                 ('Zhang et al. (2024)', 'Tomato bacterial leaf spot; hyperspectral detection compared at pre-symptomatic and symptomatic stages.', 'Accuracy compared between pre-symptomatic dates.')])
    step('3.6', 'Risk maps and independent testing', part=P,
         what='Probability of later infection is mapped per subplot for each pre-symptomatic date; if an early flight is made at Bharatpur, the frozen models are tested there.',
         why='Risk maps show where preventive sprays would be needed.',
         do=['Map predicted probability on the field layout.', 'Bharatpur: apply frozen models only if a pre-symptomatic flight and later surveys exist.'],
         check=['Risk maps for 1, 4 and 7 January.'],
         out='Risk maps → conclusions.',
         papers=[('Zarco-Tejada et al. (2018)', 'Xylella; maps of pre-visual infection over orchards from airborne imagery.', 'Maps of infection before symptoms.'),
                 ('Abdulridha et al. (2023)', 'Wheat stem rust; disease maps from drone hyperspectral models.', 'Maps from UAV models.')])
