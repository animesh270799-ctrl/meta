from c_lib import *


def add():
    h1('8. Objective 3 – Prediction of white rust at the pre-symptomatic stage')
    p('Objective 3 uses the 576 pre-symptomatic subplot-dates (1, 4 and 7 January 2027; 2, 5 and 8 DAI): 396 from the training plots and 180 from the test plots. '
      'The question is whether subplots that will develop white rust can be separated from healthy subplots before pustules are visible. ML models and DNN-F1 are used; the pseudo-image networks are not, because about 400 training samples are too few for them.')
    P = 'Objective 3'
    step('3.1', 'Pre-symptomatic samples and labels', part=P,
         what='Healthy = subplots of the healthy plots; later-infected = inoculated subplots whose DI becomes > 0 on a later date; inoculated subplots that never show pustules are left out.',
         why='Before symptoms the label cannot be seen; it comes from the later status of the same subplot.',
         do=['Read the DI of every inoculated subplot on all later dates.', 'Label each pre-symptomatic sample; count healthy and later-infected samples in training and test plots.'],
         check=['Label table per date.'],
         out='Pre-symptomatic labels → 3.2.',
         papers=[('Zhu et al. (2017)', 'Tobacco disease; pre-symptomatic hyperspectral samples labelled by the later infection status.', 'Labels from the later status.'),
                 ('Tian et al. (2021)', 'Rice leaf blast; asymptomatic infected leaves labelled by the inoculation and later symptoms.', 'Asymptomatic infected class.'),
                 ('Yu et al. (2021)', 'Pine wilt disease; early-stage trees identified by their later development.', 'Early stage defined by later status.')])
    step('3.2', 'Healthy-plot normalisation', part=P,
         what='Each feature is expressed relative to the healthy training plots of the same date and variety: z = (x − healthy mean)/healthy SD.',
         why='Before symptoms, disease effects are small compared with differences between dates and varieties; the healthy reference removes those differences.',
         do=['For each date and variety, compute the mean and SD of each feature over the healthy training plots.', 'Normalise training and test samples with these constants.'],
         check=['Constants from training plots only.'],
         out='Normalised features → 3.3.',
         papers=[('Oerke et al. (2006)', 'Cucumber downy mildew; infected leaves compared with healthy reference leaves under the same conditions.', 'Healthy reference of the same date.'),
                 ('Zarco-Tejada et al. (2018)', 'Xylella in olive; trait alterations of infected trees judged against non-infected trees.', 'Changes relative to healthy plants.')])
    step('3.3', 'Pre-symptomatic feature selection on the training plots', part=P,
         what='The chain of Step 1.8.2 is run on the 396 training samples; sensor sets are fused as in Step 2.2.',
         why='Selection must not see the test plots.',
         do=['Run 1.8.2 on training plots only.', 'Join camera DSFs for the 15 sensor sets; VIF < 10; SFFS (at most 10 features).'],
         check=['Pre-symptomatic DSF per sensor set.'],
         out='Inputs → 3.4.',
         papers=[('Tian et al. (2021)', 'Rice leaf blast; features selected for the asymptomatic stage, then SFFS.', 'Stage-specific selection and SFFS.'),
                 ('Ma et al. (2026)', 'Rice blast; selection on training data only.', 'Training plots only.')])
    step('3.4', 'Pre-symptomatic models', part=P,
         what='SVM, random forest, k-NN, PLS-DA and DNN-F1 for the 15 sensor sets (binary task), tuned as in Steps 2.4–2.5.',
         why='Same models and folds as Objective 2, so the stages can be compared.',
         do=['GroupKFold(3) tuning for ML; 11 validation plots for DNN-F1.', 'Predict the 180 test samples once.'],
         check=['Predictions for every model × sensor set.'],
         out='Predictions → 3.5.',
         papers=[('Zhu et al. (2017)', 'Tobacco disease; machine-learning classifiers on selected bands detected infection before symptoms.', 'ML classifiers for pre-symptomatic detection.'),
                 ('Tian et al. (2021)', 'Rice leaf blast; LDA, k-NN and SVM with SFFS for asymptomatic detection.', 'Same model types.'),
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
