from m_lib import *


def add():
    B.append(dict(t='title', title='Leaf-level hyperspectral detection and severity estimation of white rust in Indian mustard',
                  subtitle='Detailed methodology for the 2025-26 ASD contact-probe leaf spectra – grouped, stratified 70:30 hold-out design – with the disease-research papers behind every step',
                  lines=['Animesh Panda · Ph.D. (Agricultural Physics) · ICAR-Indian Agricultural Research Institute, New Delhi',
                         'Objective 1: spectral response and disease-specific features · Objective 2: machine-learning and deep-learning models',
                         'Methodology only: this document contains no results',
                         'Core reference: Ma et al. (2026), DT-EDNet for rice blast (IAENG International Journal of Applied Mathematics 56(11), 5380–5398), checked against the paper']))
    B.append(dict(t='toc'))

    h1('How to read this document')
    p('This document describes, step by step, how the 2025-26 leaf spectra of white rust are analysed. It contains no results. Each step has a **method card** with the same rows, '
      'so that every step can be defended in the same way:')
    bl('**What is done** – the operation in one or two sentences.',
       '**Why at this position** – why the step comes here in the sequence and what it needs from earlier steps.',
       '**Disease papers: what they did** – published plant-disease studies that used the same operation, and what exactly they did.',
       '**How my step follows them** – which part is taken from the paper, and where and why this study differs.',
       '**With my data (exact settings)** – the leaves used, the parameter values and the software.',
       '**Output → next step** – what the step produces and which later step uses it.',
       '**Alternatives and notes** – other options and the reason they were not chosen.',
       '**Likely question → answer** – a short answer for the committee.')
    p('References are taken from plant-disease studies wherever such a study exists. Where an operation has no disease paper (for example the correction of '
      'detector steps), the original methods paper is cited and this is said openly. Chapter 9 collects all reference papers in one matrix, lists every departure '
      'from them with the reason, and gives the settings of every step in one table.')

    h1('1. The methodology at a glance')
    h2('1.1 Objectives and prediction tasks')
    rows = [['Objective', 'Question', 'Main steps'],
            ['1. Spectral response and disease-specific features', 'Where and how does white rust change the leaf spectrum, and which compact set of features describes it?', 'D1–D12: mean and correlation spectra, NDSI/RSI maps, SHAP-CARS, indices, ReliefF, wavelet features, VIF, JM, PCA'],
            ['2. Detection and severity models', 'How accurately can machine-learning and deep-learning models detect white rust, place a leaf in a grade and estimate its severity on plots they have never seen?', 'E1–E7 (models), F1–F7 (evaluation), G (covariate baseline), H (check of the design)']]
    tab('objectives', rows=rows, caption='Objectives addressed with the 2025-26 leaf spectra.', widths=[2500, 3900, 3200], size=17)
    rows = [['Task', 'Target', 'Classes / range', 'Main metrics', 'Disease papers with the same task'],
            ['A – detection', 'healthy vs diseased leaf', 'grade 0 vs grade > 0', 'OA, kappa, macro-F1, sensitivity, specificity, AUC', 'Chen et al. (2023): healthy vs infected tobacco leaves; Lv et al. (2023): healthy vs infected corn leaves'],
            ['B – six grades', 'visual grade', '0, 1, 3, 5, 7, 9', 'macro-F1, QWK, within one class, per-grade F1', 'Chen et al. (2023): the same six grades 0, 1, 3, 5, 7, 9; Ma et al. (2026): five severity levels'],
            ['C – severity score', 'grade as a number', '0–9 (regression)', 'R², RMSE, RPD, bias', 'Mandal et al. (2023): rice blast 0–9 scale; Wang et al. (2016): rust severity regression']]
    tab('tasks', rows=rows, caption='The three prediction tasks.', widths=[1300, 1500, 1400, 2300, 3100], size=16)
    h2('1.2 Workflow')
    myfig('workflow', 'm01_workflow.png', 'Workflow of the methodology: experiment and quality control (A), the grouped 70:30 split (B), pre-processing and features (C), Objective 1 (D), Objective 2 (E), evaluation (F), covariate baseline (G), check of the validation design (H) and reproducibility (I).')
    p('The order matters. Quality control comes before everything. The 70:30 split is fixed before any feature is chosen or any model is fitted. Pre-processing works leaf by leaf, '
      'so it can be applied to all leaves. Objective 1 describes the disease on all leaves; when features are chosen for the models, the same chain is repeated on the training plots only '
      '(Step E2). The test plots are opened once, in Step F.')
    myfig('dataflow', 'm02_dataflow.png', 'Data flow after quality control: which leaves are used for which part of the analysis.')

    h2('1.3 Key design decisions and the papers behind them')
    rows = [['Decision', 'Choice in this study', 'Disease papers that support it'],
            ['Instrument and sample', 'ASD contact probe on single leaves, 350–2500 nm', 'Chen et al. (2023) ASD FieldSpec 4 on tobacco leaves; Meng et al. (2020) leaf clip on corn rust; Martínez-Martínez et al. (2018) contact spectra of bean leaves'],
            ['Validation', 'grouped, stratified 70:30 hold-out of whole plots', 'Ma et al. (2026) stratified 7:3 train:test; Mandal et al. (2023) stratified two-thirds : one-third; grouping by plot after Roberts et al. (2017) and Kattenborn et al. (2022)'],
            ['Smoothing', 'Savitzky–Golay, 11 nm, order 2', 'Ma et al. (2026); Selvaprakash et al. (2026); Mandal et al. (2023); Chen et al. (2023)'],
            ['Spectral range', '400–2400 nm, water bands kept', 'Meng et al. (2020) trimmed noisy ends (400–2450 nm); Chen et al. (2023) and Selvaprakash et al. (2026) used the full 350–2500 nm leaf spectrum'],
            ['Derivative', 'first derivative, no second derivative', 'Zhang et al. (2012); Lv et al. (2023); Anuar et al. (2017); Martínez-Martínez et al. (2018)'],
            ['Band grid for searches', '5-nm bands (mean of 1-nm values)', 'Ma et al. (2026) reduced sampling for the NDSI/RSI maps; Mandal et al. (2023) 10-nm band averaging; Mahlein et al. (2013) about 6 nm'],
            ['Feature families', 'bands and derivatives, indices and continuum removal, wavelet features', 'Ma et al. (2026); Zhang et al. (2012); Lv et al. (2023); Tian et al. (2021)'],
            ['Feature selection', 'effective ranges → SHAP-CARS; |r| filter → ReliefF; wavelet regions → ReliefF; VIF < 10; SFFS', 'Ma et al. (2026); Mahlein et al. (2013); Lv et al. (2023); Tian et al. (2021)'],
            ['Models', 'SVM, RF, XGBoost, k-NN, PLS-DA/PLSR; DNN-F1, DT-EDNet, EfficientNet-B0, ResNet18, ConvNeXt V2', 'Ma et al. (2026); Tian et al. (2021); Lv et al. (2023); Chen et al. (2023); Mandal et al. (2023); Gold et al. (2020)'],
            ['Metrics', 'OA, kappa, macro-F1, AUC, QWK, R², RMSE, RPD', 'Ma et al. (2026); Lv et al. (2023); Selvaprakash et al. (2026); Mandal et al. (2023); Wang et al. (2016)'],
            ['Sensor-free baseline', 'covariates only vs spectra vs both', 'Bhattacharya and Chattopadhyay (2013) mustard rot with meteorology and remote sensing; Zhang et al. (2014a); Ruan et al. (2022)']]
    tab('decisions', rows=rows, caption='Key methodological decisions with the plant-disease studies that support them (details in the method cards).', widths=[1900, 3200, 4500], size=15)
    box('Data quality control decided in this methodology.', [
        'Two problems in the raw files are handled in Step A5 before any analysis: (1) **75 duplicated leaf spectra** – on 13 March 2026, in plots 13, 34, 38, 41 and 42, fifteen leaf columns '
        'were exact copies of other columns of the same plot; one copy of each is kept; (2) **a residual step at the 1000-nm detector join** of the ASD (between the VNIR and SWIR-1 detectors), '
        'which is removed by an additive correction (Hueni and Bialek, 2017) before smoothing and differentiation.',
        'After quality control the data set has %d leaf spectra: %d in the 33 training plots and %d in the 15 test plots (%.1f%%).' % (CNT['all'], CNT['train'], CNT['test'], 100 * CNT['test_share'])], kind='caution')
