from dsl import *


def add():
    B.append(dict(t='title', title='White rust of Indian mustard: leaf hyperspectral analysis 2025-26',
                  subtitle='A step-by-step explanation of the methods, every table and figure, and what the results mean',
                  lines=['Prepared for presentation to the Chairman, Advisory Committee',
                         'Animesh Panda · Ph.D. (Agricultural Physics) · ICAR-Indian Agricultural Research Institute, New Delhi',
                         'Companion to the report ~~Leaf-level hyperspectral detection and severity estimation of white rust in Indian mustard~~, its Excel workbook and seminar slides',
                         'Data: 2330 leaf spectra (ASD FieldSpec, contact probe), 48 plots, 4 dates (11 February – 13 March 2026), natural infection']))
    B.append(dict(t='toc'))

    h1('How to use this document')
    p('This document explains, in plain language and in detail, the analysis of the 2025-26 leaf spectra of white rust in Indian mustard. '
      'It follows the order in which the analysis was done: the experiment and data, the validation design, the pre-processing, Objective 1 '
      '(which parts of the spectrum respond to the disease), Objective 2 (how well models can detect and grade the disease), the covariate '
      'baseline, robustness checks, discussion and conclusions.',
      'Every table and every figure of the report is reproduced here. After each one there is an explanation panel with the same headings, so that '
      'each item can be presented in the same way:')
    bl('**What it shows** – the content of the table or figure in one or two sentences.',
       '**How to read it** – the axes, colours, symbols or columns, so that the item can be read without the report.',
       '**What we found** – the numbers that matter, taken from the analysis.',
       '**What it means** – the interpretation: what the result says about white rust, the spectra or the models, and why it matters.',
       '**Say to the chairman** – one or two sentences that summarise the item when presenting it.')
    p('Where a method is introduced, a short panel explains **why it was done** and **how it was done** with these data. Each table and figure caption '
      'gives its number in the original report (for example "report Figure 4"), so the two documents can be used side by side. The Excel workbook '
      'holds every table as an editable sheet, and the seminar slides follow the same order.')
    box('Three numbers to remember.', ['Detection of a diseased leaf: macro-F1 0.79 and AUC 0.90 (SVM) – reliable.',
                                        'Six visual grades: macro-F1 0.36, but 75% of leaves are placed within one grade and quadratic weighted kappa is 0.63 – neighbouring grades overlap.',
                                        'Severity score 0–9: R² 0.46 and RMSE 2.0 grades (XGBoost) – a useful but approximate estimate.'])
    box('A note on corrections.', 'While preparing this explanation three small slips in the report text were found and are corrected here: the crop age of the "All" row of report '
        'Table 4 is 33–94 days after sowing (not 6–36); in the ablation discussion, removing the squeeze-and-excitation block lowered DT-EDNet more than removing the '
        'dual transformer group (0.319 vs 0.326); and DT-EDNet did best on the disease-specific feature set (0.337), not on the optimal wavelengths (0.319). '
        'FD1805 was selected in one outer fold only and is not part of the final feature set. None of the results or conclusions change.', kind='note')

    # ------------------------------------------------------------------ executive summary
    h1('Executive summary')
    h3('What was done')
    p('In the 2025-26 season, white rust (~~Albugo candida~~) developed naturally on Indian mustard in 48 field plots at IARI, New Delhi. On four dates '
      '(11 and 24 February, 3 and 13 March 2026) individual leaves were measured with an ASD FieldSpec spectroradiometer fitted with a contact probe '
      '(350–2500 nm), and each measured leaf was scored visually on the 0–9 scale (grades 0, 1, 3, 5, 7, 9). After removing nine spectra from a leaf '
      'position that was not part of the design, 2330 leaf spectra remained. The plots formed one fungicide-sprayed healthy block (plots 1–12) and three '
      'unsprayed replications (R1–R3, plots 13–48); each block contained three varieties and four sowing dates (D1–D4).')
    p('The analysis answered two thesis objectives with these leaf data. **Objective 1** asked which wavelengths, derivatives and vegetation indices change '
      'with white rust, and which compact set of features describes the disease. **Objective 2** asked how well a leaf can be (A) detected as diseased, '
      '(B) placed in one of the six grades and (C) given a severity score, using six machine-learning methods and five deep-learning networks, including '
      'DT-EDNet, the network of the rice-blast study on which the methodology is based.')
    h3('How it was done')
    bl('All selection and model fitting were tested with **leave-one-replication-out validation**: models were trained on two replications and tested on the '
       'third, which they had never seen, so that leaves of one plot never appeared in both training and test.',
       'Spectra were smoothed (Savitzky–Golay), converted to first derivatives and reduced to 5-nm bands; 41 published indices and three red-edge parameters were computed.',
       'Objective 1 followed the DT-EDNet steps: two-band index maps (NDSI, RSI), SHAP-CARS band selection, a three-band White Rust Index, ReliefF index '
       'selection and a variance-inflation check, giving an 11-feature **disease-specific feature set**.',
       'Objective 2 compared SVM, random forest, XGBoost, k-nearest neighbours, PLS-DA/PLSR and a dense network (DNN-F1) with four image networks '
       '(DT-EDNet, EfficientNet-B0, ResNet18, ConvNeXt V2-Atto) fed with "pseudo-images" of the features.',
       'A **covariate baseline** model that used only crop age, sowing date, variety, growth stage and weather – no spectra – showed how much of the disease '
       'level could be predicted from the calendar alone, so that the spectra were credited only with what they add.')
    h3('What was found')
    nl('**The disease has a clear spectral signature.** Diseased leaves reflect less near-infrared light, more red and more shortwave-infrared light, and the '
       'red-edge position moves 7.7 nm towards shorter wavelengths between grade 0 (709.0 nm) and grade 9 (701.3 nm). This agrees with chlorophyll loss, '
       'damaged leaf structure and water loss in infected tissue.',
       '**First derivatives carry the strongest signal.** The derivative at 800 nm correlated with the grade at r = 0.62, against 0.46 for the best reflectance '
       'band; all 15 wavelengths chosen by SHAP-CARS were derivative bands. The best two-band index was NDSI(795, 805) (R² 0.36).',
       '**Detection is reliable**: the best model (SVM) reached macro-F1 0.792 and AUC 0.897; sensitivity and specificity were both about 0.83.',
       '**Six grades are difficult**: the best model (ConvNeXt V2-Atto) reached macro-F1 0.360 and overall accuracy 0.39, but most errors were one grade away '
       '(75% within one grade; quadratic weighted kappa 0.633). Neighbouring grades overlap spectrally and in visual scoring.',
       '**The severity score is predicted with R² 0.459** (XGBoost; RMSE 2.04 grades); predictions follow the right order but are pulled towards the middle of the scale.',
       '**Machine learning and deep learning performed alike**: differences between the best models were smaller than the fold-to-fold variation. '
       'DT-EDNet did not outperform the other networks at leaf level, because 10–16 features give no real image for its attention modules to use.',
       '**The calendar explains much of the epidemic**, but the spectra add real information about severity: beyond the covariate-only model, the spectra raised '
       'six-grade macro-F1 by 0.043 and the score R² by 0.083 (both confirmed with plot-level bootstrap intervals).',
       '**The models transfer across varieties and sowing dates** (held-out variety or sowing date performed close to the cross-validated value).')
    h3('What it means')
    p('Leaf spectra can tell a diseased leaf from a healthy one with good reliability and can rank leaves by severity, but they cannot separate all six '
      'visual grades. For the UAV phase (2026-27) this supports (i) sensors covering the red edge, the near-infrared shoulder and the shortwave infrared, '
      '(ii) keeping derivative features, (iii) reporting detection plus a severity score or a small number of classes, and (iv) always comparing against a '
      'covariate baseline. Objective 3 (pre-symptomatic detection) could not be addressed with the 2025-26 data, because no pre-symptomatic dates were sampled.')



def intro():
    h1('1. Background and objectives')
    h2('1.1 White rust and why it needs objective measurement')
    p('White rust, caused by the oomycete ~~Albugo candida~~, is one of the most important foliar diseases of Indian mustard (~~Brassica juncea~~). On the lower '
      'leaf surface it forms white, blister-like pustules; on the upper surface the infected area becomes chlorotic and later necrotic. Systemic infection '
      'deforms the inflorescence into "stag heads" and reduces yield (Saharan et al., 2014; Mishra et al., 2009). Epidemics are favoured by cool, humid '
      'weather, typically in December and January in north India (Chattopadhyay et al., 2011).')
    p('The disease is normally scored by eye on a 0–9 scale. Visual scoring is quick, but it is subjective, and raters disagree most between neighbouring '
      'grades (Bock et al., 2010). Hyperspectral reflectance responds to the changes a pathogen causes inside the leaf – loss of chlorophyll, damage to cell '
      'structure and loss of water – and can therefore give an objective, non-destructive measure (Mahlein, 2016; Thomas et al., 2018).')
    h2('1.2 Why start at leaf level')
    p('A contact probe touches the leaf and has its own halogen lamp, so the measured spectrum contains only the leaf: no soil, no shadow, no sky and no '
      'atmosphere. Leaf spectra therefore show the pure disease signal that a sensor on an unmanned aerial vehicle (UAV) will later have to detect inside '
      'a mixed canopy pixel (Mahlein et al., 2013; Meng et al., 2020). If the signal is weak at leaf level, it will be weaker from the air; if it is clear, '
      'the leaf analysis tells which wavelengths and features the UAV analysis should look for.')
    box('In simple words.', 'The leaf study is the "laboratory version" of the UAV study: it tells us whether white rust can be seen in the spectrum at all, '
        'where in the spectrum it is seen, and how finely the severity can be measured when nothing else disturbs the signal.')
    h2('1.3 Objectives addressed with the 2025-26 data')
    tab('obj', 1, widths=[2600, 3900, 3100])
    read(shows='The two thesis objectives that the 2025-26 leaf data can answer, the question asked for each, and the outputs produced.',
         how='Each row is one objective; the middle column states the question in plain words; the right column lists the results that answer it and that are explained later in this document.',
         means='Objective 1 is about understanding the signal (which wavelengths and indices); Objective 2 is about using it (how accurate the models are). '
               'Objective 3 (pre-symptomatic detection) is not addressed because the first sampling date already had visible disease on almost half of the leaves; '
               'it is planned for the pre-symptomatic UAV flights of 2026-27.',
         say='"With one season of leaf spectra I answer two questions: where in the spectrum white rust shows, and how accurately it can be detected and graded."')
    h2('1.4 The workflow at a glance')
    fig('workflow', 'f00_workflow.png', 'Workflow of the analysis from data collection to discussion.', rep=1)
    read(shows='The complete sequence of steps, from the field experiment to the discussion.',
         how='Follow the arrows: the 16 numbered boxes run left to right in the first row, right to left in the second, and so on. The outline colours group the steps: '
             'green = data collection and quality control (1–4), dark blue = pre-processing and features (5–6), light blue = Objective 1 (7–10), yellow = validation design (11), '
             'purple = Objective 2 (12–14), red = covariate baseline, interpretation and discussion (15–16).',
         found='Sixteen steps were carried out. The steps that need images (orthomosaics, crop mask, texture, thermal, fusion of 15 sensor sets) do not apply to non-imaging leaf spectra and were not done.',
         means='The workflow makes clear that feature selection and modelling are tested inside a leakage-free validation design, and that a model without spectra '
               '(the covariate baseline) is part of the evaluation. Both are needed for the results to be trusted.',
         say='"This is the road map of the analysis; every later table and figure belongs to one of these boxes."')
