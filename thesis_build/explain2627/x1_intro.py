from dsl import *

TEST = [1, 4, 5, 8, 13, 14, 18, 25, 27, 31, 35, 37, 44, 46, 48]
VAL = [6, 7, 11, 19, 24, 26, 28, 30, 36, 39, 41]


def stage_head(comes_after, feeds, data):
    box('Position in the analysis', ['**Comes after:** ' + comes_after, '**Feeds into:** ' + feeds, '**Samples used:** ' + data], kind='method')


def add():
    B.append(dict(t='title', title='How the 2026-27 white rust data are analysed: a step-by-step explanation from raw data to final results',
                  subtitle='UAV hyperspectral, multispectral, RGB and thermal cameras (subplot level) and ASD leaf spectra (leaf level). Order of the steps, the data used in each step, the plot-wise 7:3 split, exact settings, worked examples and references – written so that every step can be explained and repeated on a new data set.',
                  lines=['Animesh Panda · Ph.D. (Agricultural Physics) · ICAR-Indian Agricultural Research Institute, New Delhi',
                         'Companion to the document "White rust complete methodology 2026-27 (UAV + ASD)". Step codes in brackets (B1, 1.6.5, L5.2 …) are the step numbers of that document.',
                         'No results – all numbers in examples and figures are demo values.']))
    B.append(dict(t='toc'))

    h1('How to read this document')
    p('The methodology document describes each step on its own card. This document tells the **story of the analysis from beginning to end**: what is done first, what is done next, why it must come at that point, which samples each step uses, how each calculation is made and which paper each step follows. '
      'It is written so that you can explain any step in front of the Advisory Committee and repeat the whole analysis on another data set.')
    nl('**Chapters 1–2** give the whole analysis in one view and describe the data that enter it.',
       '**Chapters 3–6** are the preparation done once for all objectives: image processing, features, the data split and normalisation.',
       '**Chapters 7–12** are the UAV analysis of Objectives 1 and 2 in the order in which it is run.',
       '**Chapter 13** is the pre-symptomatic analysis (Objective 3) and **Chapter 14** the ASD leaf analysis (Part L), each in its own order.',
       '**Chapter 15** explains how to repeat everything on a new data set, with a checklist and the files to keep; **Chapter 16** answers likely questions about the order and the data used.')
    p('Four kinds of boxes are used:')
    box('Position in the analysis', 'what the stage comes after, what it feeds into, and which samples it uses.', kind='method')
    box('In short', 'the main idea of a step in two or three lines.', kind='key')
    box('Worked example', 'a small calculation with demo numbers, to show exactly how a step is computed.', kind='note')
    box('On a new data set', 'what to change and what to keep when the step is repeated on other data.', kind='present')
    p('References are given in the text as author and year (for example Ma et al., 2026) and listed at the end. For each step both the **disease study** that used the step and, where useful, the **original method paper** are cited.')

    # ---------------------------------------------------------------- chapter 1
    h1('1. The whole analysis in one view')
    h2('1.1 What the analysis must answer')
    p('The season produces images of four UAV cameras and leaf spectra of an ASD spectroradiometer on the same subplots and dates, together with a visual disease score of every subplot. The analysis answers three questions, one per objective:')
    nl('**Objective 1 – characterisation:** how does each camera (and the leaf spectrum) see white rust, and which wavelengths, indices, texture and thermal features carry the disease signal?',
       '**Objective 2 – detection and severity:** which camera or camera combination, with which model, best detects white rust and grades its severity on plots that the models have never seen?',
       '**Objective 3 – pre-symptomatic prediction:** can subplots that will develop white rust be separated from healthy subplots 2–8 days after inoculation, before pustules appear?')
    p('Every model is built for three tasks, because each task answers a different practical question (Tian et al., 2021; Chen et al., 2023; Mandal et al., 2023):')
    rows = [['Task', 'Question', 'Target (label)', 'Type', 'Main metric'],
            ['A', 'Is the subplot (or leaf) diseased?', 'healthy (DI = 0) or diseased (DI > 0)', 'two classes', 'macro-F1'],
            ['B', 'How severe is it, in classes?', 'DI class 0, 1, 3, 5, 7, 9', 'six ordered classes', 'macro-F1'],
            ['C', 'How severe is it, as a number?', 'DI (%) (leaf: grade as a number)', 'regression', 'R²']]
    tab('tasks', rows=rows, caption='The three tasks of every model.', widths=[700, 2600, 2700, 1700, 1900], size=17)

    h2('1.2 The order of the whole analysis')
    p('The analysis runs in **14 stages** ({F:order}). Stages 1–5 are done once and serve all objectives. Objective 1 comes next because it chooses the features that Objectives 2 and 3 use. Objective 2 builds and tests the models. Objective 3 repeats the chain for the pre-symptomatic dates, and the ASD leaf analysis (Part L) follows the same chain for leaves. {T:order} lists every stage with its input, output and the samples it uses; the chapters that follow explain each stage in this order.')
    myfig('order', 'x01_stage_order.png', 'Order of the whole analysis. Each stage uses the output of the stage above it. Objective 3 runs after Stage 7 with the same rules; the leaf analysis runs after Stage 5 as a parallel chain.', width=560)
    rows = [['Stage', 'Methodology steps', 'What happens', 'Input', 'Output', 'Samples used'],
            ['1', 'B1–B6', 'images calibrated, mosaicked, cleaned, co-registered; mean of every band in every subplot ROI', 'raw images of 13 dates', 'subplot average spectra and temperatures', 'all 48 plots'],
            ['2', 'C1–C6', 'features of each camera computed', 'subplot averages and ROI pixels', 'one feature table per camera', 'all 48 plots'],
            ['3', 'A3, A5, A6', 'DI, DI class, healthy/diseased label and covariates joined to every row', 'scoring sheets, weather', 'labelled tables', 'all 48 plots'],
            ['4', 'D1, D2', 'plots divided into 33 training and 15 test plots; inner folds and validation plots fixed', 'plot list', 'split column, folds, validation plots', 'defines the sets'],
            ['5', 'D3–D5', 'thermal normalisation; scaling rules; leakage rules', 'feature tables', 'normalised thermal features; rules', 'training plots for all constants'],
            ['6', '1.1, 1.7', 'response curves, correlations, strata, physiology', 'labelled tables', 'description of the disease signal', 'all 48 plots'],
            ['7', '1.2–1.6', 'feature selection inside each camera; VIF → disease-specific feature set (DSF) of each camera and task', 'training rows of each camera table', 'DSF of the 4 cameras × 3 tasks', '33 training plots'],
            ['8', '2.1–2.2', 'DSFs joined for the 15 sensor sets; VIF again', 'DSFs', '45 input tables (15 sets × 3 tasks)', '33 training plots'],
            ['9', '2.3–2.4', 'SFFS, grid search and final fit of SVM/SVR, random forest, k-NN, PLS-DA/PLSR', 'input tables', '180 frozen ML models', 'inner folds of the 33 training plots'],
            ['10', '2.5–2.6', 'DNN-F1, DNN-F2 and the pseudo-image networks', 'input tables', 'frozen networks', '22 fitting + 11 validation plots'],
            ['11', '2.7', 'every frozen model predicts the test plots once; metrics', 'frozen models', 'metric table', '15 test plots'],
            ['12', '2.8–2.11', 'ranking, fusion gain, ablation, SHAP, covariate baseline, strata, maps, Bharatpur', 'metric table, predictions', 'answers of Objective 2', 'test plots (and Bharatpur)'],
            ['13', '1.8, 3.1–3.6', 'pre-symptomatic labels, normalisation, selection, models, test, earliest day, risk maps', 'pre-symptomatic rows', 'answers of Objective 3', 'same split'],
            ['14', 'L1–L10', 'leaf table, smoothing, indices, description, selection, models, test, leaf–canopy link', 'ASD files', 'leaf results', 'same split (by plot)']]
    tab('order', rows=rows, caption='The 14 stages of the analysis in the order in which they are run.', widths=[600, 1100, 3200, 1600, 1700, 1400], size=14, nokeep=True)

    h2('1.3 The unit of analysis')
    p('**UAV data are analysed at subplot level.** One sample is one subplot on one date: the average of all pixels of its region of interest (ROI) for every band of every camera, with the disease index (DI) of the same subplot and date as the label. Each of the 48 plots has 4 subplots, so the field gives 192 samples per date and camera. '
      '**ASD data are analysed at leaf level.** One sample is one leaf on one date, with that leaf\'s own grade as the label. {F:journey} follows one sample from the field to the test.')
    myfig('journey', 'x07_sample_journey.png', 'Journey of one UAV sample. Subplot 25-2 belongs to a test plot, so it is never used to learn anything; it is only predicted at the end.')

    h2('1.4 Four rules that hold in every stage')
    nl('**Whole plots stay together.** All subplots of a plot on all dates, and all its ASD leaves, are either training or test data. Subplots of one plot share soil, microclimate and inoculum, so mixing them would let a model recognise the plot instead of the disease (Roberts et al., 2017).',
       '**Everything that is learned comes from the training plots.** Selected features, scaling constants, healthy references, tuning settings and model weights are computed on the 33 training plots; feature selection done on all data would make the test accuracy optimistic (Ambroise and McLachlan, 2002; Ma et al., 2026).',
       '**The test plots are used once.** The 15 test plots are fixed before the first flight and predicted only after every model is frozen (Ma et al., 2026; Bijlwan et al., 2025).',
       '**The same rules for every camera.** Every camera, sensor set and model uses the same split, folds and validation plots, so differences between them are due to the data, not to the division.')

    # ---------------------------------------------------------------- chapter 2
    h1('2. The data that enter the analysis')
    h2('2.1 Field design')
    p('The experiment at IARI, New Delhi has 4 sowing dates (19 and 26 November, 3 and 10 December 2026) × 3 varieties (PM 26, Pusa Vijay, PM 37) = 12 treatments. Each treatment is inoculated in three replications (R1–R3; 36 plots) and has one uninoculated healthy plot in a separate block (12 plots): 48 plots of 5 m × 3 m, each divided into 4 subplots of 2.5 m × 1.5 m (A1). '
      'The 36 plots were inoculated on 30 December 2026 with ~~Albugo candida~~ (1.5 × 10^{5} zoosporangia mL^{−1}), so the crops were 41, 34, 27 and 20 days old at inoculation. Staggered sowing gives different crop ages under the same weather, as in the white rust forecasting work of Chattopadhyay et al. (2011); inoculated and healthy plots of the same treatment give the severity range seen by the UAV (Guo et al., 2021; Liu et al., 2024).')
    myfig('layout', 'g02_layout.png', 'Field layout: healthy block (plots 1–12) and the inoculated replications R3 (13–24), R2 (25–36) and R1 (37–48).')
    h2('2.2 Dates')
    p('Thirteen dates are flown. The first three are pre-symptomatic (no pustules yet) and the other ten post-symptomatic ({T:dates}, {F:timeline}).')
    rows = [['Date', '1 Jan', '4 Jan', '7 Jan', '11 Jan', '18 Jan', '25 Jan', '1 Feb', '8 Feb', '15 Feb', '22 Feb', '1 Mar', '8 Mar', '15 Mar'],
            ['DAI', '2', '5', '8', '12', '19', '26', '33', '40', '47', '54', '61', '68', '75'],
            ['Stage', 'pre', 'pre', 'pre', 'post', 'post', 'post', 'post', 'post', 'post', 'post', 'post', 'post', 'post'],
            ['Physiology', '', '', '✓', '', '✓', '', '', '✓', '', '', '✓', '', '']]
    tab('dates', rows=rows, caption='The 13 flight dates (2027), days after inoculation (DAI), stage and the four dates with plant physiology.', widths=[1100] + [656] * 13, size=14)
    myfig('timeline', 'g04_timeline.png', 'Season timeline: sowing, inoculation, pre-symptomatic and post-symptomatic flights and the physiology dates.')
    h2('2.3 What is measured on every date')
    rows = [['Measurement', 'Instrument and setting', 'Unit of the record', 'Methodology step'],
            ['Hyperspectral images', 'Headwall co-aligned VNIR–SWIR imager, 400–2500 nm (483 usable bands), about 2.2 cm pixel', 'whole field', 'A2'],
            ['Multispectral images', 'MicaSense RedEdge-MX, 475, 560, 668, 717, 840 nm, about 2 cm', 'whole field', 'A2'],
            ['RGB images', 'DJI camera, about 0.8 cm', 'whole field', 'A2'],
            ['Thermal images', 'FLIR Vue Pro R, 7.5–13.5 µm, about 3.9 cm; air temperature and humidity of the flight', 'whole field', 'A2'],
            ['Leaf grades', 'L3, L5 and the lowest green leaf (LL) of 5 tagged plants per subplot (centre + 4 corners), 0–9 scale', '15 leaves per subplot', 'A3'],
            ['ASD leaf spectra', 'leaf clip with its own lamp; L3, L5, LL of the centre plant, 2 readings per leaf, 350–2500 nm', '3 leaves per subplot', 'A4'],
            ['Plant physiology', 'pigments, anthocyanin, protein, relative water content, membrane stability, gas exchange (LI-6400)', 'one designated subplot per plot', 'A7 (4 dates)'],
            ['Weather', 'IARI observatory: Tmax, Tmin, RH I, RH II, rainfall', 'daily', 'A6']]
    tab('measured', rows=rows, caption='Measurements of each date.', widths=[1900, 4500, 1900, 1300], size=15)
    h2('2.4 From leaf grades to the disease index of a subplot')
    p('Each graded leaf gets a grade x by the percentage of its area with pustules, judged with the area diagrams of Conn et al. (1990) by the same trained person on all dates, because raters disagree most between neighbouring classes (Bock et al., 2010): 0 = none, 1 = 1–5%, 3 = 6–10%, 5 = 11–25%, 7 = 26–50%, 9 = more than 50%. '
      'The 15 grades of a subplot give its disease index with the formula used for white rust by Mishra et al. (2009) and for UAV targets by Liu et al. (2024):')
    eq('DI (%) = Σ(x × f) / (9 × Σf) × 100')
    p('where f is the number of leaves with grade x and 9 the highest grade. The DI is then put in classes for Task B ({T:diclass}).')
    box('Worked example', ['Subplot 25-2 on 18 January: 15 leaves with grades 0, 0, 1, 1, 1, 3, 3, 3, 3, 5, 5, 5, 7, 7, 9.',
                           'Σ(x × f) = 0 × 2 + 1 × 3 + 3 × 4 + 5 × 3 + 7 × 2 + 9 × 1 = 53; DI = 53 / (9 × 15) × 100 = 39.3% → class 7 (high); Task A = diseased.'], kind='note')
    rows = [['Leaf area with pustules', 'Leaf grade', 'Subplot DI (%)', 'DI class (Task B)', 'Name'],
            ['0', '0', '0', '0', 'healthy'], ['1–5%', '1', '> 0 to 5', '1', 'very low'], ['6–10%', '3', '> 5 to 10', '3', 'low'],
            ['11–25%', '5', '> 10 to 25', '5', 'moderate'], ['26–50%', '7', '> 25 to 50', '7', 'high'], ['> 50%', '9', '> 50', '9', 'very high']]
    tab('diclass', rows=rows, caption='Leaf grades and DI classes.', widths=[2200, 1400, 2000, 2000, 2000], size=16)
    h2('2.5 Labels of the samples')
    rows = [['Data', 'Task A', 'Task B', 'Task C'],
            ['UAV, post-symptomatic dates', 'DI = 0 → healthy; DI > 0 → diseased (from the survey, not from the treatment)', 'DI class', 'DI (%)'],
            ['UAV, pre-symptomatic dates (Objective 3)', 'healthy plot subplots → healthy; inoculated subplots whose DI becomes > 0 later → later-infected; inoculated subplots that never show pustules are left out', '–', '–'],
            ['ASD leaves', 'grade 0 or > 0', 'leaf grade 0, 1, 3, 5, 7, 9', 'leaf grade as a number']]
    tab('labels', rows=rows, caption='Labels of the three tasks (A5).', widths=[2400, 3900, 1800, 1500], size=15)
    p('A DI class with fewer than 5% of the samples is merged with its neighbour (for example 7 + 9) before modelling. The pre-symptomatic label is taken from the later status of the same subplot, as Zhu et al. (2017) and Tian et al. (2021) labelled leaves that showed lesions later as infected.')
    h2('2.6 Covariates')
    p('Severity follows time, crop and weather, so each sample also carries covariates (A6). They are **not** used in feature selection; they are used only in the covariate baseline (Stage 12) and to report results by stratum.')
    rows = [['Covariate', 'How it is computed'],
            ['Days after inoculation (DAI)', 'flight date − 30 December 2026'], ['Variety, sowing date', 'from the plot table'],
            ['Growth stage', 'BBCH, coded 1 = vegetative (10–49), 2 = flowering (60–69), 3 = pod formation (≥ 70)'],
            ['7-day weather', 'mean Tmax, Tmin, RH I, RH II and total rainfall of the 7 days ending the day before the flight'],
            ['Favourable days', 'days since inoculation meeting the white rust conditions of Chattopadhyay et al. (2011): leaf infection Tmax 16–24 °C, RH I > 97% and RH II > 40%; staghead Tmax 20–29 °C, Tmin > 12 °C and RH I > 97%']]
    tab('covs', rows=rows, caption='Covariates of every sample.', widths=[2600, 7000], size=16)
    h2('2.7 How many samples')
    rows = [['Data set', 'How it is counted', 'All', 'Training plots (33)', 'Test plots (15)'],
            ['UAV post-symptomatic (per camera)', '48 plots × 4 subplots × 10 dates', '1920', '1320', '600'],
            ['UAV pre-symptomatic (per camera)', '48 × 4 × 3 dates (minus never-infected inoculated subplots)', '576', '396', '180'],
            ['ASD leaves', '48 plots × 4 subplots × 1 centre plant × 3 leaves × 13 dates', '7488', '5148', '2340'],
            ['Leaf grades for the DI', '192 subplots × 15 leaves × 13 dates', '37 440', '–', '–'],
            ['Physiology', '48 designated subplots × 4 dates per parameter', '192', 'description only', '–']]
    tab('counts', rows=rows, caption='Number of samples of each data set and their division between training and test plots.', widths=[2600, 3400, 1000, 1500, 1100], size=15)
