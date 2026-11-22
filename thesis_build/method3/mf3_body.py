"""Revised field methodology (Objectives 1-3, with the DT-EDNet paper methods): body of the Word document (docx JS)."""
import json, re, os
B = os.path.dirname(os.path.abspath(__file__)) + '/'
K = []
def esc(t):
    t = t.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    return re.sub(r'\[\[(T|F):(\w+)\]\]', lambda m: '${%s(\'%s\')}' % (m.group(1), m.group(2)), t)
def js(s): return '`' + esc(s) + '`'
def H1(t): K.append("K.push(H1(%s));" % js(t))
def H2(t): K.append("K.push(H2(%s));" % js(t))
def H3(t): K.append("K.push(H3(%s));" % js(t))
def P(t): K.append("K.push(P(%s));" % js(t))
def BL(items): K.extend("K.push(BL(%s));" % js(i) for i in items)
def NL(items): K.extend("K.push(NL(%s));" % js(i) for i in items)
def BOX(l, t, fill='FFF6E0', line='C98A00'): K.append("K.push(BOX(%s, %s, '%s', '%s'));" % (js(l), js(t), fill, line))
def NOTE(t): K.append("K.push(NOTE(%s));" % js(t))
def EQ(t): K.append("K.push(EQ(%s));" % js(t))
def FIG(k, file, cap, w=560): K.append("K.push(...fig2('%s', '%s', %s, %d));" % (k, file, js(cap), w))
def TAB(k, rows, cap, widths=None, size=17):
    if widths is None:
        L = [min(max(max(len(str(r[j])) for r in rows), 5), 46) for j in range(len(rows[0]))]; s = sum(L); widths = [int(9306 * x / s) for x in L]
    R = '[' + ',\n'.join('[' + ', '.join(js(str(c)) for c in r) + ']' for r in rows) + ']'
    K.append("K.push(...tab2('%s', %s, %s, %s, %d));" % (k, R, json.dumps(widths), js(cap), size))
def PB(): K.append("K.push(new Paragraph({ children: [new PageBreak()] }));")

def STEP(code, title, purpose, inp, out, proc, refs, note=None):
    """One step: heading, purpose/input/output table, numbered procedure, supporting studies."""
    H3('Step %s – %s' % (code, title))
    TAB('s' + re.sub(r'\W', '', code).lower(), [['Item', 'Description'], ['Purpose (problem it solves)', purpose], ['Input', inp], ['Output → next step', out]],
        'Step %s at a glance.' % code, [2200, 7106], 17)
    P('**Procedure.**'); NL(proc)
    P('**Supporting studies.** ' + refs)
    if note: NOTE(note)

def CARD(key, name, principle, problem, spec, tuning, data, why, refs):
    """Method card: principle, problem, specification, hyper-parameters, suitable data, reason for selection, references."""
    TAB('c' + key, [['Aspect', name], ['Principle (how it works)', principle], ['Problem it solves', problem], ['Specification in this study', spec],
                    ['Hyper-parameters and how they are tuned', tuning], ['Data on which it works well', data], ['Why it was selected', why], ['Key references', refs]],
        'Method card – %s.' % name, [2300, 7006], 16)

# =====================================================================================
# TITLE
# =====================================================================================
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1100, after: 200 }, children: [new TextRun({ text: 'AI-based multimodal UAV sensing of white rust in mustard', font: FONT, size: 44, bold: true, color: '1E3A1F' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [new TextRun({ text: 'Research methodology for the field experiment (revised): objectives → activities → steps', font: FONT, size: 28, color: '2C5F2D' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: 'Hyperspectral, multispectral, red–green–blue and thermal unmanned aerial vehicle (UAV) data | 15 sensor sets | feature-level fusion | machine learning, feature-fusion neural networks, DT-EDNet, EfficientNet, ResNet18 and ConvNeXt V2', font: FONT, size: 21, italics: true })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 }, children: [new TextRun({ text: 'Animesh Panda (Roll No. 13098) | Ph.D. Agricultural Physics | ICAR-Indian Agricultural Research Institute, New Delhi', font: FONT, size: 20 })] }));")
BOX('How to read this document.', 'The work is organised in three levels. (1) Six common activities (A to F) prepare the data once for all objectives. (2) Each objective is divided into activities (for example Activity 1.2). (3) Each activity is divided into numbered steps (for example Step 1.2.3). Every step has a heading and the same layout: purpose, input, output, procedure and supporting studies. Every technique used in a step is described in a method card that gives its principle, the problem it solves, its specification, its hyper-parameters and how they are tuned, the data on which it works well, why it was selected and its references. Flow charts are given for every objective and for the main activities, and small dummy datasets are used to show how each calculation works. Full names are written with their abbreviation in brackets.', 'EEF3E8', '2C5F2D')
BOX('What is new in this revision.', '(1) The methods of the DT-EDNet study on rice blast (Ma et al., 2026) are included: effective wavelength ranges from normalised difference and ratio spectral index maps, optimal wavelengths by SHAP-CARS, vegetation index selection by ReliefF, texture from principal-component images selected by minimum redundancy maximum relevance (mRMR), the Tri-band Texture Fusion Index (TTFI) and the DT-EDNet network with EfficientNet, ResNet18 and ConvNeXt V2 as comparison networks for the post-symptomatic data. (2) One feature-selection method is used for each type of feature. (3) The second derivative is not used. (4) A separate activity on normalisation and data preparation is added. (5) The endmember extraction is described step by step. (6) Each technique has a method card. (7) Covariates are days after inoculation, variety, inoculation timing, growth stage and weather; they are used for a covariate-only baseline and for sensor + covariate models, not as disease features. (8) Healthy plots are rotated across the folds so that every fold contains healthy plots of all three varieties. (9) SHAP-CARS standardises the bands and always keeps the red-edge first derivative. (10) All models, including DT-EDNet and the comparison networks, are built for every single camera and every camera combination, for classification and regression.')
PB()
K.append("K.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: 'Contents', font: FONT, size: 32, bold: true, color: '1E3A1F' })] }));")
K.append("K.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-3' }));")
PB()

H1('Full names and abbreviations')
P('The text always gives the full name with the abbreviation in brackets. This list is only for quick reference.')
TAB('abbr', [['Abbreviation', 'Full name', 'Abbreviation', 'Full name'],
 ['AdamW', 'adaptive moment estimation with decoupled weight decay', 'MNF', 'minimum noise fraction'],
 ['ASD', 'Analytical Spectral Devices field spectroradiometer (leaf spectra)', 'L3, L5, LL', '3rd and 5th fully expanded leaf from the top; lowest green leaf'],
 ['AUC', 'area under the receiver operating characteristic curve', 'mRMR', 'minimum redundancy maximum relevance'],
 ['BBCH', 'decimal scale of plant growth stages (Biologische Bundesanstalt, Bundessortenamt und Chemische Industrie)', 'RH', 'relative humidity'],
 ['CARS', 'competitive adaptive reweighted sampling', 'MS', 'multispectral'],
 ['CBAM', 'convolutional block attention module', 'NDSI', 'normalised difference spectral index'],
 ['CWSI', 'crop water stress index', 'NDVI', 'normalised difference vegetation index'],
 ['DAI', 'days after inoculation', 'NRCT', 'normalised relative canopy temperature'],
 ['DNN-F1, DNN-F2', 'deep neural network with input-level (F1) or intermediate-level (F2) feature fusion', 'OW', 'optimal wavelengths'],
 ['DT-EDNet', 'Dual Transformer Early Detection Network', 'PCA', 'principal component analysis'],
 ['DTG', 'Dual Transformer Group', 'PLS, PLS-DA, PLSR', 'partial least squares; discriminant analysis; regression'],
 ['GLCM', 'grey-level co-occurrence matrix', 'PPI', 'pixel purity index'],
 ['HS', 'hyperspectral', 'RF', 'random forest'],
 ['k-NN', 'k-nearest neighbours', 'RGB', 'red–green–blue (camera)'],
 ['KTB', 'Kernel Transformer Block', 'RMSE', 'root-mean-square error'],
 ['LORO', 'leave-one-replication-out (cross-validation)', 'RPD', 'ratio of performance to deviation'],
 ['MCCV', 'Monte Carlo cross-validation', 'RSI', 'ratio spectral index'],
 ['MHSA', 'multi-head self-attention', 'SAM', 'spectral angle mapper'],
 ['SE', 'squeeze-and-excitation (attention block)', 'SFFS', 'sequential floating forward selection'],
 ['SHAP', 'Shapley additive explanations', 'SVM, SVR', 'support vector machine; support vector regression'],
 ['TF', 'texture feature', 'TIR', 'thermal infrared'],
 ['TTB', 'Token Transformer Block', 'TTFI', 'Tri-band Texture Fusion Index'],
 ['UAV', 'unmanned aerial vehicle', 'VI', 'vegetation index'],
 ['VIF', 'variance inflation factor', 'WRI', 'White Rust Index'],
 ['XGBoost', 'extreme gradient boosting', 'T_{max}, T_{min}', 'daily maximum and minimum air temperature']],
 'Full names of the abbreviations used.', [1500, 3150, 1500, 3156], 16)

# =====================================================================================
H1('1. Objectives, data and overall design')
H2('1.1 Background and objectives')
P('White rust, caused by the obligate oomycete Albugo candida, produces white pustules on the leaves, chlorosis and, after systemic infection, distorted inflorescences (staghead) in Indian mustard, and it can reduce yield by 20–60% (Kumar and Kalha, 2005; Saharan et al., 2014). The disease develops under cool and humid weather (Chattopadhyay et al., 2011). Visual scoring is slow and possible only after symptoms appear. Cameras on an unmanned aerial vehicle (UAV) record the changes in pigments, leaf structure, water and temperature that accompany infection, sometimes before symptoms are visible (Mahlein, 2016; Terentev et al., 2022), and combining several cameras usually improves accuracy (Maimaitijiang et al., 2020; Feng et al., 2022).')
TAB('objectives', [['Objective', 'Question answered', 'Data used', 'Main output'],
    ['1. To characterise white rust of mustard through multimodal sensing from a UAV platform', 'Which wavelengths, vegetation indices, texture features and thermal features of each camera respond to white rust severity, and does the response change with variety and inoculation timing?', '1920 post-symptomatic subplot samples per camera', 'Optimal wavelengths, White Rust Index, selected indices, Tri-band Texture Fusion Index and the disease-specific feature set of each camera'],
    ['2. To detect and discriminate disease severity of white rust in mustard through AI-based multimodal data fusion', 'How accurately can (a) healthy vs diseased subplots, (b) severity classes and (c) the severity score be predicted by each of the 15 sensor sets with machine learning and deep learning?', '1920 post-symptomatic subplot samples per camera', 'Best sensor set and model for each task; contribution of each camera; comparison of DT-EDNet with EfficientNet, ResNet18 and ConvNeXt V2; severity maps'],
    ['3. To predict white rust at the pre-symptomatic stage using machine learning', 'Can subplots that will develop white rust be separated from healthy subplots before symptoms, and can their later severity be predicted?', '576 pre-symptomatic subplot samples per camera', 'Pre-symptomatic models; earliest detection day; risk maps']],
    'Objectives, questions, data and outputs.', [2600, 3000, 1600, 2106], 16)
H2('1.2 Overall design')
P('All objectives use the same field data and the same preparation. The common activities A to F are carried out once ([[F:overall]]). Objective 1 then describes and selects the features of each camera, Objective 2 builds the detection and severity models on the post-symptomatic data and Objective 3 builds the early-warning models on the pre-symptomatic data.')
FIG('overall', 'g01_overall.png', 'Overall workflow. Common activities A–F prepare the data once; each objective is divided into activities and steps.', 560)
P('**Eight rules apply to every activity.** They come from the methodological literature and from the weaknesses reported in recent disease-sensing studies (Ambroise and McLachlan, 2002; Varma and Simon, 2006; Cawley and Talbot, 2010; Roberts et al., 2017; Ma et al., 2026).')
NL(['One sample is one subplot on one date. The four subplots of a plot always stay together in the training part or in the test part.',
    'All cameras are measured on the same vegetation pixels of each subplot (Common Activity C).',
    'Features are grouped by type, and one selection method is used for each type of feature (Objective 1).',
    'Every step that uses the severity labels (index search, feature selection, tuning, early stopping) runs inside the training part only.',
    'All normalisation constants (means, standard deviations, healthy-plot references) are computed on the training part and then applied to the test part.',
    'Severity increases with time, so every sensor model is compared with a covariate-only model (days after inoculation, variety, inoculation timing, growth stage, weather); a sensor model is useful only if it is better than this baseline.',
    'The same folds are used for all sensor sets and all models, so that their accuracies are directly comparable.',
    'Validation has two stages: first inside the IARI field (leave-one-replication-out, nested), then on independent data from research farms and farmers\' fields at Bharatpur with frozen models.'])
H2('1.3 Dataset')
TAB('dataset', [['Item', 'Value'], ['Plots × subplots', '48 × 4 = 192 subplots in each image'], ['Cameras', '4: hyperspectral, multispectral, red–green–blue and thermal'], ['Images', '13 flight dates × 4 cameras = 52 images (3 pre-symptomatic + 10 post-symptomatic dates)'], ['Inoculation and flight dates', 'inoculation 10 Jan 2027; flights 12, 15, 18 Jan (pre-symptomatic) and 21, 28 Jan, 4, 11, 18, 25 Feb, 4, 11, 18, 25 Mar 2027 (post-symptomatic)'],
    ['Post-symptomatic samples per camera', '1920 (10 dates × 192 subplots)'], ['Pre-symptomatic samples per camera', '576 (3 dates × 192 subplots)'], ['Label of every sample', 'canopy severity score of the subplot (0–9 grade key) recorded on the flight day'], ['Varieties', 'V1 = PM 26, V2 = Pusa Vijay, V3 = PM 37'], ['Sowing dates (2026)', 'D1 = 19 Nov, D2 = 27 Nov, D3 = 5 Dec, D4 = 13 Dec'], ['Field layout', '48 m × 24 m; healthy block (12 plots) + 10 m buffer + inoculated block (R1–R3, 36 plots); plots 5 m × 3 m'], ['Covariates', 'days after inoculation, variety, inoculation timing, growth stage, weather (T_{max}, T_{min}, RH, rainfall)'], ['ASD leaf spectra', '3 plants per subplot × leaves L3, L5, LL on every flight date (1728 leaf spectra per date)'], ['Validation', 'first stage: IARI field (leave-one-replication-out, nested); second stage: Bharatpur research farms and farmers\' fields (independent, natural infection, at least 300 quadrat-dates)'],
    ['Sensor sets analysed', '15 (4 single cameras, 6 pairs, 4 triples, all four)'], ['Tasks', 'detection (healthy vs diseased), severity classes, severity score'], ['Time for the analysis', '6 months']], 'Dataset used in this methodology (numbers as recorded by the researcher).', [3300, 6006])
FIG('dataset', 'g26_dataset.png', 'Structure of the dataset: flight dates → cameras → plots → scored subplots, and the two datasets used by the objectives.', 520)
H2('1.4 Main published studies used to build the methodology')
P('Each step was chosen because it was used and tested for crop-disease sensing or for the specific data problem it solves. [[T:literature]] lists the main disease studies; the methodological references are given in every step and method card.')
TAB('literature', [['Study', 'Crop and disease', 'Sensors', 'What it contributes to this methodology'],
 ['Ma et al. (2026)', 'rice; blast', 'UAV hyperspectral', 'effective ranges from NDSI and RSI maps; SHAP-CARS; ReliefF for indices; principal-component texture with mRMR; TTFI; DT-EDNet vs EfficientNet, ResNet18, ConvNeXt V2; module ablation'],
 ['Guo et al. (2021)', 'wheat; yellow rust', 'UAV hyperspectral', 'texture from principal-component images; vegetation index + texture fusion; NDVI soil mask; disease index'],
 ['Liu et al. (2020)', 'wheat; Fusarium head blight', 'UAV hyperspectral', 'bands, indices and texture as feature groups; univariate area under the curve screening; neural network'],
 ['Yu et al. (2021)', 'pine; pine wilt disease', 'UAV hyperspectral + spectrometer', 'red-edge parameters best for the early stage; random forest'],
 ['Feng et al. (2022)', 'wheat; powdery mildew', 'hyperspectral + thermal + RGB', 'feature-level fusion of indices, thermal and texture features'],
 ['Liu et al. (2024); Liu et al. (2026)', 'wheat; powdery mildew', 'UAV multispectral + thermal; ground to UAV', 'red-edge indices, thermal features and severity maps; a disease-specific index transferred from ground to UAV'],
 ['Calderón et al. (2014)', 'opium poppy; downy mildew', 'UAV thermal + multispectral', 'canopy minus air temperature as a normalised thermal feature'],
 ['Zheng et al. (2018); Das et al. (2015)', 'wheat yellow rust; rice bacterial leaf blight', 'hyperspectral simulated to Sentinel-2 and LISS-IV', 'disease-specific three-band index; band simulation for satellite up-scaling'],
 ['Yuan et al. (2025)', 'rice; bacterial blight', 'UAV + satellite', 'mRMR feature selection; random forest, support vector machine and k-nearest neighbours'],
 ['Maimaitijiang et al. (2020)', 'soybean yield', 'UAV RGB + multispectral + thermal', 'deep neural networks with input-level and intermediate-level fusion'],
 ['Mahlein et al. (2013); Huang et al. (2014)', 'sugar beet and wheat diseases', 'hyperspectral', 'ReliefF and disease-specific spectral indices'],
 ['Tian et al. (2021); Mustafa et al. (2023)', 'rice blast; wheat Fusarium head blight', 'hyperspectral (+ fluorescence)', 'variance inflation factor and floating forward selection; pre-symptomatic stage'],
 ['Zhu et al. (2017); Zarco-Tejada et al. (2018)', 'tobacco virus; olive Xylella', 'hyperspectral (+ thermal)', 'pre-symptomatic detection with labels from the later status'],
 ['Mahlein et al. (2019)', 'wheat; Fusarium head blight', 'hyperspectral + thermal + fluorescence', 'sensor comparison and earliest detection day']],
 'Main disease studies and what they contribute.', [2100, 1700, 1800, 3706], 15)

# =====================================================================================
H1('2. Common activities (carried out once for all objectives)')
P('The six common activities turn the raw images into clean, normalised feature tables with one row per subplot-date and prepare the validation folds. Each activity is described as a sequence of steps.')
TAB('commonact', [['Activity', 'Steps', 'Main output'], ['A. Field experiment, ground truth and datasets', 'A1–A7', 'labelled subplot list; ASD leaf spectra; covariates; post- and pre-symptomatic datasets; Bharatpur validation dataset'], ['B. Image pre-processing', 'B1–B5', 'calibrated, aligned images on the hyperspectral grid'],
    ['C. Endmember extraction and vegetation mask', 'C1–C8', 'endmember library; vegetation mask applied to all cameras'], ['D. Subplot spectra and feature extraction', 'D1–D8', 'feature table of each camera'],
    ['E. Normalisation and data preparation', 'E1–E4', 'normalised and standardised features; class weights'], ['F. Validation design and tuning', 'F1–F3', 'outer and inner folds; tuning plan; leakage checklist']], 'Common activities and their outputs.', [3500, 1300, 4506])

# ---------------------------------------------------------------- A
H2('Activity A – Field experiment, ground truth and datasets')
STEP('A1', 'Experimental design and treatments',
     'Defines the sources of variation (inoculation timing, variety, replication) so that disease effects can be separated from crop-age and variety effects.',
     'IARI research farm, New Delhi, rabi 2026-27; field 48 m × 24 m (9.4 m healthy block + 10 m buffer + 28.6 m inoculated block); plots 5 m × 3 m with 0.2 m bunds and 2 m channels.',
     '48 plots with known treatment, replication and plot number → subplots (Step A3) and validation folds (Activity F).',
     ['Four sowing dates at 8-day intervals: D1 = 19 November, D2 = 27 November, D3 = 5 December and D4 = 13 December 2026, with one inoculation on 10 January 2027, so the crop is inoculated at four different ages: 52, 44, 36 and 28 days after sowing.',
      'Three varieties: V1 = PM 26, V2 = Pusa Vijay, V3 = PM 37.',
      'The 12 treatments (4 × 3) are inoculated in three replications (R1: plots 37–48, R2: plots 25–36, R3: plots 13–24) with a zoosporangial suspension of 1.5 × 10^{5} zoosporangia mL^{−1} (Mishra et al., 2009).',
      'One uninoculated healthy plot of every treatment (plots 1–12) is sown in a separate healthy block, 10 m away from the inoculated block, so that inoculum does not spread to the controls: 36 inoculated + 12 healthy = 48 plots.',
      'Each plot carries a code (treatment, replication, plot number) that is stored with every sample.'],
     'Staggered sowing or inoculation and healthy controls were used to create severity gradients for wheat yellow rust (Guo et al., 2021), wheat powdery mildew (Feng et al., 2022; Liu et al., 2024) and rice blast (Tian et al., 2021; Ma et al., 2026); a randomised trial with varieties of different resistance was used for wheat rusts by Blasch et al. (2023).')
STEP('A2', 'UAV flights and cameras',
     'Provides images of four cameras on the same day, each recording a different plant response.',
     'Flight plan; calibration panels; ground control points.',
     'Raw images of the four cameras on every date → pre-processing (Activity B).',
     ['Fly between 11:00 and 14:00 h under clear sky and low wind, at 30 m above the ground, with about 85% forward and 80% side overlap.',
      'Hyperspectral camera: Headwall co-aligned visible–near-infrared and short-wave-infrared imager (483 usable bands from 399 to 2398 nm after quality control; ground pixel about 2.2 cm).',
      'Multispectral camera: MicaSense RedEdge-MX (475, 560, 668, 717 and 840 nm; about 2 cm).',
      'Red–green–blue camera: DJI camera (about 0.8 cm). Thermal camera: FLIR Vue Pro R, 7.5–13.5 µm (about 3.9 cm).',
      'Place reflectance panels and ground control points before every flight; record air temperature and relative humidity during the flight.',
      'Measure ASD leaf spectra on the same dates (Step A4).',
      'Fly on 13 dates: 12, 15 and 18 January 2027 (pre-symptomatic) and 21 and 28 January, 4, 11, 18 and 25 February, 4, 11, 18 and 25 March 2027 (post-symptomatic); all four cameras on every date.',
      'Score the subplots on the day of the flight (or within one day).'],
     'The same four camera types were combined for wheat powdery mildew (Feng et al., 2022) and soybean yield (Maimaitijiang et al., 2020); flight protocols with panels and solar-noon windows are reviewed by Aasen et al. (2018); thermal flight practice: Messina and Modica (2020).')
TAB('flights', [['Flight', 'Date', 'Days after inoculation', 'Period', 'Cameras and scoring'],
    ['1', '12 Jan 2027', '2', 'pre-symptomatic', 'RGB (DJI Phantom), multispectral (MicaSense RedEdge), thermal (FLIR), hyperspectral (Headwall co-aligned), ASD leaf spectra, visual severity'],
    ['2', '15 Jan 2027', '5', 'pre-symptomatic', 'all four cameras + ASD leaf spectra + visual severity'], ['3', '18 Jan 2027', '8', 'pre-symptomatic', 'all four cameras + ASD leaf spectra + visual severity'],
    ['4', '21 Jan 2027', '11', 'post-symptomatic', 'all four cameras + ASD leaf spectra + visual severity'], ['5', '28 Jan 2027', '18', 'post-symptomatic', 'all four cameras + ASD leaf spectra + visual severity'],
    ['6', '4 Feb 2027', '25', 'post-symptomatic', 'all four cameras + ASD leaf spectra + visual severity'], ['7', '11 Feb 2027', '32', 'post-symptomatic', 'all four cameras + ASD leaf spectra + visual severity'],
    ['8', '18 Feb 2027', '39', 'post-symptomatic', 'all four cameras + ASD leaf spectra + visual severity'], ['9', '25 Feb 2027', '46', 'post-symptomatic', 'all four cameras + ASD leaf spectra + visual severity'],
    ['10', '4 Mar 2027', '53', 'post-symptomatic', 'all four cameras + ASD leaf spectra + visual severity'], ['11', '11 Mar 2027', '60', 'post-symptomatic', 'all four cameras + ASD leaf spectra + visual severity'],
    ['12', '18 Mar 2027', '67', 'post-symptomatic', 'all four cameras + ASD leaf spectra + visual severity'], ['13', '25 Mar 2027', '74', 'post-symptomatic', 'all four cameras + ASD leaf spectra + visual severity']],
    'Timeline of data collection in the field (inoculation on 10 January 2027): 3 pre-symptomatic and 10 post-symptomatic dates.', [900, 1500, 1700, 1700, 3506], 16)
STEP('A3', 'Subplots and canopy severity score',
     'Gives every sampling unit its label.',
     'Plot boundaries; field scoring sheets.',
     'Labelled subplot list (date, plot, subplot, treatment, replication, score) → labels (Step A5) and subplot extraction (Activity D).',
     ['Divide each plot into four equal quadrant subplots; exclude border rows with an inner buffer.',
      'One trained scorer grades the canopy of each subplot with the 0–9 key of Conn et al. (1990): 0 = no symptoms, 1 = 1–5%, 3 = 6–10%, 5 = 11–25%, 7 = 26–50%, 9 = more than 50% of the canopy leaf area with pustules; staghead is noted after flowering. Grade limits are written on the sheet to keep scoring consistent (Bock et al., 2010).',
      'For plot summaries, compute the percent disease index of the plot: PDI = Σ(grade of each subplot) / (number of subplots × 9) × 100.'],
     'Grade keys of this kind were used for canopy severity in UAV studies of wheat stem rust (Abdulridha et al., 2023), powdery mildew (Liu et al., 2024) and rice blast (Ma et al., 2026); disease indices from graded leaves: Guo et al. (2021).')
EQ('PDI = Σ_{i} grade_{i} / (n × 9) × 100      (n = 4 subplots per plot)')
TAB('pdiex', [['Subplot', '1', '2', '3', '4', 'Plot PDI'], ['Grade (dummy)', '3', '5', '1', '3', '(3 + 5 + 1 + 3) / (4 × 9) × 100 = 33.3%']], 'Worked example (dummy data): percent disease index of one plot.', [1800, 900, 900, 900, 900, 3906])
STEP('A4', 'Leaf spectra with the ASD field spectroradiometer',
     'Gives leaf-level reflectance spectra and leaf severity grades from the same subplots on the same days as the UAV flights, for a separate leaf-level analysis and for linking leaf and canopy data.',
     'Three tagged plants in every subplot (12 per plot, 576 in total); ASD FieldSpec spectroradiometer with plant probe and leaf clip (contact probe with its own light source); white reference panel (Spectralon).',
     'Leaf spectrum table (one row per leaf and date) with leaf grade and metadata → leaf-level dataset (its analysis is not part of this methodology).',
     ['Dates: all 13 flight dates (12, 15, 18 January; 21, 28 January; 4, 11, 18, 25 February; 4, 11, 18, 25 March 2027), on the day of the flight or within one day. The leaf clip has its own lamp, so measurements do not depend on the time of day or the sky.',
      'Plants: before inoculation, tag 3 plants in every subplot (3 × 4 = 12 plants per plot), inside the inner buffer and spread along the subplot diagonal. Measure the same plants on every date; if a plant dies, replace it with its nearest neighbour and record the change.',
      'Leaves: measure the 3rd (L3) and 5th (L5) fully expanded leaves counted from the top and the lowest green leaf (LL) of every plant. Count the positions again on each date because they shift as the plant grows; record a missing leaf (for example a senesced LL) as missing.',
      'Instrument set-up: optimise the instrument and take a white reference at the start, then a new white reference every 10–15 minutes or at the start of every plot.',
      'Readings: take 3 readings per leaf (near the tip, the middle and the base of the lamina, avoiding the midrib), each averaging 10–25 scans, over 350–2500 nm.',
      'Leaf grade: score the measured leaf immediately with the 0–9 key (Conn et al., 1990), using the same written grade limits as the canopy scoring.',
      'Metadata for every reading: date, time, plot, subplot, plant ID, leaf position, reading number, leaf grade, time of the last white reference and operator; save the files with names that contain the plot, subplot, plant and leaf codes.'],
     'Field spectroscopy protocols (reference panels, metadata): Milton et al. (2009); leaf measurements collected together with UAV imagery: Calderón et al. (2014), Yu et al. (2021); disease indices developed from leaf measurements and carried to canopy and UAV scale: Huang et al. (2014), Liu et al. (2026); leaf severity grades: Conn et al. (1990), Bock et al. (2010).',
     note='Only the acquisition of the leaf data is described here. The leaf-level analysis and the linking with the UAV data are carried out separately.')
TAB('asdvol', [['Item', 'Per date', 'All 13 dates'], ['Tagged plants', '576 (48 plots × 12)', 'same 576 plants'], ['Leaves (L3, L5, LL)', '1728', '≈ 22 500'], ['Readings (3 per leaf)', '5184', '≈ 67 000'],
    ['Working time at about 1 minute per leaf', '≈ 29 operator-hours', '—'], ['Suggested teams', '3 teams, one replication each (healthy block shared)', '—']],
    'Volume and organisation of the ASD leaf measurements.', [3600, 3000, 2706])
STEP('A5', 'Labels and the two datasets',
     'Defines exactly what each model predicts and which samples belong to which objective.',
     'Subplot scores of all 13 flight dates.',
     'Post-symptomatic dataset (1920 samples per camera) and pre-symptomatic dataset (576 samples per camera) with their labels → all objectives.',
     ['Pre-symptomatic dates: the first three flights (12, 15 and 18 January 2027; 2, 5 and 8 days after inoculation). Post-symptomatic dates: the next ten flights (21 January to 25 March 2027; 11–74 days after inoculation).',
      'Detection label: healthy (grade 0) or diseased (grade above 0), taken from the observed score, not from the treatment.',
      'Severity classes: the six grades 0, 1, 3, 5, 7 and 9; a grade with fewer than 5% of the samples is merged with its neighbour (for example 7 + 9).',
      'Severity score: the grade treated as a continuous number for regression.',
      'Pre-symptomatic labels (Objective 3): healthy = subplots of the healthy plots; infected = inoculated subplots that show pustules on a later date; inoculated subplots that never show symptoms are kept out of the infected class.'],
     'Detection, severity classes and regression were analysed together for rice blast (Tian et al., 2021) and wheat powdery mildew (Feng et al., 2022); labels from the later status for pre-symptomatic samples: Zhu et al. (2017), Tian et al. (2021).')
TAB('classex', [['Grade', '0', '1', '3', '5', '7', '9'], ['Detection label', 'healthy', 'diseased', 'diseased', 'diseased', 'diseased', 'diseased'], ['Severity class', '0', '1', '3', '5', '7', '9'], ['Dummy count (1920 samples)', '512', '413', '362', '313', '200', '120']],
    'How one score gives the three labels (dummy class counts).', [2500, 1134, 1134, 1134, 1134, 1134, 1136])
STEP('A6', 'Covariates: days after inoculation, variety, inoculation timing, growth stage and weather',
     'Disease severity changes with time, crop stage, variety and weather. These known factors must be recorded so that their effect can be separated from what the cameras add.',
     'Field book (sowing, inoculation and flight dates; variety; growth stage on each flight date); daily weather from the IARI agrometeorological observatory.',
     'Covariate table with one row per subplot-date → response analysis (Step 1.1.3), covariate baseline and sensor + covariate models (Steps 2.5.5 and 3.5.3), results by stage and treatment.',
     ['Days after inoculation (DAI): flight date minus inoculation date (numeric).',
      'Variety: V1 = PM 26, V2 = Pusa Vijay, V3 = PM 37 (categorical, one-hot coded in models).',
      'Inoculation timing: D1–D4, also expressed as crop age at inoculation in days (numeric).',
      'Growth stage of each plot on each flight date, read with the BBCH scale and coded as 1 = vegetative (BBCH 10–59), 2 = flowering (BBCH 60–69), 3 = pod formation (BBCH 70–79 and later) (ordinal).',
      'Weather: daily maximum and minimum air temperature (T_{max}, T_{min}), morning and afternoon relative humidity (RH I, RH II) and rainfall, summarised as the mean (rainfall: total) of the 7 days before each flight, plus the number of favourable days since inoculation (T_{max} 16–24 °C, RH I > 97% and RH II > 40%, the conditions reported to favour white rust on leaves).',
      'Covariates are not features of any camera and are not used in feature selection; they enter only the covariate models and the stratified results.'],
     'Weather conditions that favour white rust of Indian mustard and weather-based forecasting: Chattopadhyay et al. (2011), Saharan et al. (2014); BBCH growth stages: Lancashire et al. (1991), Meier (2018); stage-dependent spectral disease signals: Blasch et al. (2023), Liu et al. (2024); combining weather with remote sensing improved disease forecasts over weather alone: Zhang et al. (2014); days after inoculation in early detection: Mahlein et al. (2019), Zhu et al. (2017).')
TAB('covtab', [['Covariate', 'Type and coding', 'Varies between subplots on one date?', 'Main use'],
    ['Days after inoculation', 'numeric (days)', 'no (same inoculation date)', 'time trend; baseline model'],
    ['Variety (V1 PM 26, V2 Pusa Vijay, V3 PM 37)', 'categorical, one-hot', 'yes', 'baseline; stratified results; transfer test'],
    ['Inoculation timing (D1–D4)', 'categorical, or crop age at inoculation (days)', 'yes', 'baseline; stratified results; transfer test'],
    ['Growth stage (1 vegetative, 2 flowering, 3 pod formation)', 'ordinal from BBCH', 'yes (staggered sowing)', 'baseline; results by stage; flowering check'],
    ['Weather (T_{max}, T_{min}, RH I, RH II, rainfall; favourable days)', 'numeric, 7-day summaries', 'no (one value per date)', 'interpretation; baseline (time effect only)']],
    'Covariates recorded for every subplot-date. Weather is the same for all subplots on a date, so it can explain differences between dates but not between subplots.', [2900, 2200, 1900, 2306])
NOTE('Weather has only one value per flight date (ten values in the post-symptomatic period), so in a single season it cannot be separated from the date itself. It is therefore used for interpretation and inside the covariate baseline, and results of models that contain weather are labelled "within-season"; their transfer to another season must be tested with data of that season (Zhang et al., 2014; Ma et al., 2026).')

STEP('A7', 'Second-stage validation data at Bharatpur (research farms and farmers\' fields)',
     'Models tested only inside the IARI field may not work on other soils, varieties, management and natural epidemics. Independent data from another site are needed for a second-stage validation.',
     'Research farm(s) and farmers\' fields at Bharatpur, Rajasthan, with natural white rust; the same four cameras, calibration panels and ground control points; the same severity key and scorer.',
     'Bharatpur validation dataset (quadrat-dates with images of all four cameras, severity grade and covariates) → second-stage validation (Activity 2.7).',
     ['Sites: research-farm plots and farmers\' fields with natural white rust in the same season (rabi 2026-27), chosen to cover healthy to severely diseased canopies and the common local varieties.',
      'Sampling units: in every field mark validation quadrats of the same size as an IARI subplot (2.5 m × 1.5 m) with corner pegs and image-visible markers, recorded with an RTK GNSS receiver, away from field borders and bunds.',
      'Size: aim for at least 300 quadrat-dates in total (for example 8–10 farmers\' fields and research-farm plots × 15–20 quadrats × 2–3 post-symptomatic flight dates in February–March), with every severity grade represented, including healthy quadrats.',
      'Flights: the same four cameras and flight settings as at IARI (30 m, 11:00–14:00 h, about 85% forward and 80% side overlap, reflectance panels and ground control points on every flight); if possible add one flight before symptoms with the same quadrats revisited later.',
      'Ground truth: score the canopy of every quadrat with the same 0–9 key (Conn et al., 1990), by the same scorer, on the day of the flight.',
      'Covariates (as in Step A6): variety, sowing date, growth stage (BBCH), days since the first symptoms were seen, fungicide sprays of the farmer, and daily weather from the nearest agrometeorological observatory or automatic weather station.',
      'Healthy reference: where possible, keep a fungicide-protected strip of the main variety at the research farm, so that features that need a healthy reference can also be tested.'],
     'Independent validation on naturally infected fields from another site and year: Ma et al. (2026); importance of testing on independent locations: Roberts et al. (2017), Ploton et al. (2020); Bharatpur as a white rust site for weather-based forecasting: Chattopadhyay et al. (2011); UAV disease monitoring of smallholder fields: Liu et al. (2026); transfer of UAV disease models to new areas: Yuan et al. (2025).',
     note='The Bharatpur data are never used for feature selection, tuning or training. They are used only once, for the second-stage validation of the final models.')

# ---------------------------------------------------------------- B
H2('Activity B – Image pre-processing')
P('Activity B turns raw images into calibrated, aligned images on one common grid ([[F:preproc]]).')
FIG('preproc', 'g02_preproc.png', 'Flow chart of Activity B (Steps B1–B5).', 540)
STEP('B1', 'Radiometric calibration',
     'Raw digital numbers depend on illumination and camera settings and cannot be compared between dates or cameras.',
     'Raw images; panel images; sunlight-sensor records; air temperature and humidity.',
     'Reflectance images (hyperspectral, multispectral), consistent RGB images and temperature images → Step B2.',
     ['Hyperspectral and multispectral: convert digital numbers to reflectance with the empirical line method using the panels imaged before and after each flight; correct illumination changes during the flight with the downwelling sunlight sensor.',
      'Red–green–blue: fixed exposure and white balance on all dates; colour values are used as relative values (colour indices are ratios, so they are not affected by overall brightness).',
      'Thermal: convert radiance to temperature with emissivity 0.98 and the air temperature, relative humidity and flight height of each flight.'],
     'Empirical line method: Smith and Milton (1999); UAV spectroscopy workflows: Aasen et al. (2018); panels before and after the flight: Yuan et al. (2025), Blasch et al. (2023), Guo et al. (2021); thermal conversion: Jones et al. (2009), Messina and Modica (2020).')
CARD('eline', 'Empirical line calibration', 'A linear relation between the digital number and reflectance is fitted for each band from targets of known reflectance (panels); the relation is applied to every pixel.',
     'Removes the effect of sun angle, atmosphere and camera gain, so reflectance is comparable between dates.', 'Two or more panels of known reflectance (for example 5%, 20%, 50%) imaged before and after each flight; one linear fit per band and flight.',
     'No hyper-parameters; the panel reflectances must be certified and the panels must fill many pixels.', 'Low-altitude UAV images under stable sky, where the atmosphere between camera and ground is thin.',
     'Simple, standard and accurate for UAV data; used in almost all UAV disease studies.', 'Smith and Milton (1999); Aasen et al. (2018)')
STEP('B2', 'Orthomosaics and georeferencing',
     'Single frames must be joined into one map per camera and date with correct ground coordinates.',
     'Calibrated frames; ground control points.',
     'Georeferenced orthomosaics and georectified hyperspectral cubes → Steps B3 and B4.',
     ['Build orthomosaics of the frame cameras (multispectral, red–green–blue, thermal) by structure-from-motion.',
      'Georectify the push-broom hyperspectral lines with the position and attitude data of the UAV.',
      'Use the same ground control points on every date so that all dates share one coordinate frame.'],
     'Georeferenced UAV hyperspectral mosaics: Guo et al. (2021), Ma et al. (2026); mosaicking of RGB, multispectral and thermal frames before feature extraction: Maimaitijiang et al. (2020), Feng et al. (2022).')
STEP('B3', 'Hyperspectral cube quality control and smoothing',
     'Water-vapour absorption, detector edges and random noise make some bands unusable and add noise to the others.',
     'Georectified 613-band cube of each date.',
     'Clean 483-band reflectance cube → Step B4.',
     ['Remove the water-vapour regions (1335–1460 nm and 1785–1965 nm) and the noisy ends, giving 483 bands from 399 to 2398 nm; drop the three isolated bands at 916–920 nm (detector edge).',
      'Smooth every spectrum with a Savitzky–Golay filter (window 5 bands, second-order polynomial) separately on each continuous band segment, never across a removed region.',
      'Check that reflectance is between 0 and 1.'],
     'Removal of water-vapour bands: Thenkabail et al. (2004); Savitzky–Golay smoothing: Savitzky and Golay (1964), Schafer (2011); used before derivatives by Tsai and Philpot (1998) and in disease studies by Tian et al. (2021) and Mustafa et al. (2023).')
CARD('sg', 'Savitzky–Golay smoothing filter', 'A low-order polynomial is fitted by least squares to a moving window of bands; the centre value of the fitted polynomial replaces the measured value.',
     'Reduces random noise while keeping the shape and position of absorption features; prepares spectra for the first derivative.', 'Window of 5 bands (about 15–20 nm), polynomial order 2, applied on each continuous segment.',
     'Window length and polynomial order; chosen by visual check of the red edge and by the noise of the first derivative on panel pixels (a longer window smooths more but flattens narrow features).', 'Densely sampled spectra with random noise, such as hyperspectral reflectance.',
     'Keeps peaks better than a moving average; standard before derivatives.', 'Savitzky and Golay (1964); Schafer (2011); Rinnan et al. (2009)')
STEP('B4', 'Projection and co-registration',
     'Images of different cameras do not overlap exactly; small shifts mix canopy and soil values at the edges of rows.',
     'Georeferenced images of all cameras for one date.',
     'All images in one projection and aligned to the hyperspectral image → Step B5.',
     ['Project every image to WGS 84 / UTM zone 43N so that distances are in metres.',
      'Register the red–green–blue, multispectral and thermal images to the hyperspectral image with tie points (plot corners, markers) and a first- or second-order polynomial transformation.',
      'Accept the registration when the root-mean-square error of independent check points is below one hyperspectral pixel (2.2 cm).'],
     'Image registration: Zitová and Flusser (2003); polynomial warping: Richards (2013); co-registered multi-camera UAV layers: Maimaitijiang et al. (2020), Feng et al. (2022).')
STEP('B5', 'Resampling to the hyperspectral grid',
     'The cameras have different pixel sizes (about 0.8, 2, 2.2 and 3.9 cm); one grid is needed so that one pixel is the same ground point in every layer.',
     'Co-registered images.',
     'All layers on the 2.2 cm hyperspectral grid → vegetation mask (Activity C) and subplot values (Activity D).',
     ['Red–green–blue (finer): pixel aggregate, so each new pixel is the mean of the pixels it covers.',
      'Multispectral (similar size): bilinear interpolation.',
      'Thermal (coarser): nearest neighbour, which keeps the measured temperatures.',
      'Compute red–green–blue texture before resampling, at native resolution, because resampling removes fine texture.'],
     'Resampling methods: Richards (2013); resampling of UAV hyperspectral images to other resolutions: Guo et al. (2021); pixel aggregation between UAV and satellite grids: Revill et al. (2020), Yuan et al. (2025); common-grid stacking of RGB, multispectral and thermal data: Maimaitijiang et al. (2020).')
CARD('resample', 'Resampling (pixel aggregate, bilinear, nearest neighbour)', 'Pixel aggregate averages all fine pixels inside a coarse pixel; bilinear interpolation weights the four nearest pixels by distance; nearest neighbour copies the value of the closest pixel.',
     'Places all cameras on one grid so that one mask and one set of subplot polygons can be used.', 'Target grid: 2.2 cm hyperspectral grid; method chosen by the direction of the change in pixel size (finer → aggregate; similar → bilinear; coarser → nearest neighbour).',
     'No tuning; the choice follows the rule above.', 'Aggregate: going to a coarser grid; nearest neighbour: preserving measured values such as temperature.',
     'Avoids aliasing when coarsening and avoids inventing new temperatures when refining.', 'Richards (2013); Guo et al. (2021)')

# ---------------------------------------------------------------- C
H2('Activity C – Endmember extraction and vegetation mask')
P('Soil, grass, weeds and shadow inside a subplot change reflectance, texture and temperature and must be removed before disease features are extracted. Activity C builds one field-wide library of pure spectra (endmembers) with the hourglass workflow, classifies every pixel with the spectral angle mapper and keeps the canopy pixels ([[F:endmember]]). Flowers are kept because the canopy score includes the inflorescence; no spectral unmixing is done.')
FIG('endmember', 'g03_endmember.png', 'Flow chart of Activity C: endmember extraction (Steps C1–C5) and vegetation mask (Steps C6–C8).', 540)
STEP('C1', 'Sampling of pixels from all dates',
     'Endmember extraction on every full image would be slow, and endmembers extracted separately for each date or plot would not be comparable.',
     'Clean hyperspectral cubes of all dates (Step B3).',
     'One pooled pixel sample (for example 20 000 pixels from each date) → Step C2.',
     ['Draw a random sample of pixels from inside the field on every date, so that early green canopy, diseased canopy, flowering canopy, soil, grass and shadow are all represented.',
      'Add pixels of the reference panels and known soil and grass patches to make sure these classes are present.'],
     'One library for the whole scene gives the same classes in every plot and on every date (Bioucas-Dias et al., 2012); pooled samples for the hourglass workflow: Boardman and Kruse (2011).')
STEP('C2', 'Minimum noise fraction (MNF) transformation',
     'Hyperspectral bands are noisy and highly correlated; the corners of the pixel cloud, where pure pixels lie, are hidden by noise.',
     'Pooled pixel sample (483 bands).',
     'Minimum noise fraction (MNF) components ordered by signal-to-noise ratio; components with eigenvalues clearly above 1 → Step C3.',
     ['Estimate the noise from the differences between neighbouring pixels (shift difference) in a homogeneous area.',
      'Whiten the noise (rescale so the noise has unit variance in every direction) and then apply principal component analysis.',
      'Plot the eigenvalues ([[F:dummyem]]a); keep the components whose eigenvalue is clearly above 1 (here about 8–10); components with eigenvalues near 1 contain only noise.'],
     'Green et al. (1988); Boardman and Kruse (2011); Bioucas-Dias et al. (2012).')
CARD('mnf', 'Minimum noise fraction (MNF) transformation', 'Two principal component analyses in sequence: the first whitens the noise, the second orders the components by signal-to-noise ratio. Eigenvalue 1 means a component is pure noise.',
     'Separates signal from noise and reduces 483 correlated bands to about 10 informative components.', 'Noise from shift differences in a homogeneous field area; components with eigenvalue above about 2 kept.',
     'Number of components kept: chosen from the eigenvalue plot (the "knee" where values approach 1).', 'Hyperspectral images with many correlated, noisy bands.',
     'Unlike plain principal component analysis, it ranks components by image quality, not by variance (which can be dominated by noise or illumination).', 'Green et al. (1988); Boardman and Kruse (2011)')
STEP('C3', 'Pixel purity index (PPI)',
     'Among thousands of pixels, the few spectrally pure pixels (one material only) must be found.',
     'Selected MNF components of the pixel sample.',
     'Pixel purity index (PPI) image: count of how often each pixel was an extreme → Step C4.',
     ['Project the MNF pixel cloud onto many random unit vectors ("skewers"), for example 10 000.',
      'On each skewer, record the pixels at the two extreme ends; add one to their count.',
      'Keep pixels with high counts (for example at least 10) as pure-pixel candidates.'],
     'Boardman et al. (1995); Boardman and Kruse (2011); Bioucas-Dias et al. (2012).')
CARD('ppi', 'Pixel purity index (PPI)', 'In a cloud of mixed pixels, pure pixels lie at the corners (vertices). A random projection puts corner pixels at its ends; pixels that are repeatedly at the ends are pure.',
     'Finds candidate endmember pixels without prior knowledge.', '10 000 skewers on the kept MNF components; threshold of 10 hits.',
     'Number of skewers (more = more stable; 5000–20 000 usual) and the threshold (2–3 times the noise level); fixed after checking that the candidate set no longer changes.', 'Scenes with some pure pixels of each material; high spatial resolution (2.2 cm) makes pure canopy and soil pixels common.',
     'Simple, transparent and part of the standard hourglass workflow; candidates are checked visually in the next step.', 'Boardman et al. (1995); Boardman and Kruse (2011)')
STEP('C4', 'n-dimensional visualisation and endmember selection',
     'PPI candidates form clusters; each cluster corner must be turned into one endmember spectrum.',
     'Pure-pixel candidates in MNF space.',
     'Endmember spectra (mean reflectance of each cluster) → Step C5.',
     ['Display the candidates in two- and three-dimensional scatter plots of MNF components and rotate them (n-dimensional visualiser).',
      'Mark the clusters at the corners of the cloud ([[F:dummyem]]b).',
      'Compute the endmember spectrum as the mean reflectance (original bands) of the pixels in each cluster.'],
     'Boardman and Kruse (2011); Bioucas-Dias et al. (2012).')
STEP('C5', 'Endmember identification and library',
     'Endmembers must be named before they can be used to build a mask.',
     'Endmember spectra; field photographs; red–green–blue images; leaf spectra of the study.',
     'Labelled endmember library (green canopy, stressed canopy, flower, soil, grass, shadow) → Step C6.',
     ['Locate the pixels of each endmember in the red–green–blue image and in field photographs.',
      'Compare their shapes with known spectra: green canopy (red edge, high near-infrared), stressed canopy (higher red, lower near-infrared), yellow flower (high green–red reflectance), soil (rising, featureless), shadow (low everywhere) ([[F:dummyem]]c).',
      'Merge duplicates and store the final library.'],
     'Identification by spectral shape and image context: Boardman and Kruse (2011); flowers in Brassica canopies: Sulik and Long (2016).')
FIG('dummyem', 'g12_dummy_endmember.png', 'Dummy example of endmember extraction: (a) MNF eigenvalues; (b) pure pixels at the corners of the MNF cloud; (c) endmember library.', 560)
STEP('C6', 'Spectral angle mapper (SAM) classification',
     'Every pixel of every date must be assigned to one class.',
     'Labelled endmember library; clean cubes of all dates.',
     'Class map of every date → Step C7.',
     ['Compute the spectral angle between each pixel spectrum and each endmember (equation below).',
      'Assign the pixel to the endmember with the smallest angle; leave it unclassified if the smallest angle is larger than the threshold.',
      'Calibrate the threshold (0.10, 0.20 or 0.30 radian tested) on labelled reference pixels.'],
     'Kruse et al. (1993); spectral angle mapper for crop masks in UAV hyperspectral studies: Guo et al. (2021).')
EQ('α = cos^{−1} [ Σ_{i} t_{i} r_{i} / ( √(Σ_{i} t_{i}^{2}) √(Σ_{i} r_{i}^{2}) ) ]')
P('Here t is the pixel spectrum, r the endmember spectrum and i the band. Because the angle does not depend on the length of the spectra, a shaded canopy pixel and a sunlit canopy pixel have almost the same angle to the canopy endmember.')
TAB('samex', [['Spectrum (4 bands, dummy)', 'Blue', 'Green', 'Red', 'Near-infrared', 'Angle to pixel (radian)'], ['Pixel t', '0.05', '0.08', '0.06', '0.45', '—'],
    ['Green canopy endmember', '0.04', '0.09', '0.05', '0.50', '0.044 (smallest → canopy)'], ['Yellow flower endmember', '0.06', '0.20', '0.22', '0.40', '0.424'], ['Soil endmember', '0.10', '0.14', '0.18', '0.25', '0.550']],
    'Worked example (dummy data): spectral angle mapper classification of one pixel.', [2600, 900, 900, 900, 1300, 2706])
FIG('dummysam', 'g13_dummy_sam.png', 'Dummy example: (a) the spectral angle α between a pixel and an endmember; (b) class map and the resulting vegetation mask.', 520)
CARD('sam', 'Spectral angle mapper (SAM)', 'Treats each spectrum as a vector and measures the angle between two vectors; small angle = similar shape.',
     'Classifies pixels by spectral shape, so it is insensitive to brightness differences caused by shading and slope.', 'Endmember library from Step C5; maximum angle 0.10–0.30 radian (calibrated); one classification per date.',
     'Maximum angle: the value with the highest overall accuracy on reference pixels.', 'Hyperspectral data with distinct class shapes (vegetation, soil, shadow, flowers).',
     'Needs only one spectrum per class, works with the endmember library directly and is robust to illumination.', 'Kruse et al. (1993); Bioucas-Dias et al. (2012)')
STEP('C7', 'Vegetation mask rule and edge erosion',
     'Some flower pixels have low NDVI, and pixels at the edge of leaves are mixtures of canopy and soil.',
     'Class map; normalised difference vegetation index (NDVI) image.',
     'Binary vegetation mask (1 = green canopy, stressed canopy, flower; 0 = soil, grass, shadow, unclassified) → Step C8 and Activity D.',
     ['Keep the classes green canopy, stressed canopy and flower; remove soil, grass, shadow and unclassified pixels.',
      'Apply the rule: vegetation = (NDVI > 0.6 OR flower class) AND a kept class; NDVI alone would remove yellow flowers.',
      'Apply a one-pixel morphological erosion to remove mixed edge pixels.'],
     'NDVI: Rouse et al. (1974); NDVI threshold masks in UAV disease studies: Guo et al. (2021) (NDVI > 0.42); morphological erosion: Soille (2003); flowers and canopy spectra: Sulik and Long (2016).')
STEP('C8', 'Mask accuracy and transfer to all cameras',
     'The mask must be shown to be accurate and must be applied identically to all cameras.',
     'Vegetation mask; independent reference pixels from the red–green–blue image.',
     'Accepted mask on the hyperspectral grid, applied to the multispectral, red–green–blue and thermal layers → Activity D.',
     ['Digitise independent reference pixels of each class on the red–green–blue image (for example 300 per class).',
      'Compute the confusion matrix, overall accuracy and kappa coefficient; accept the mask when overall accuracy is at least 90%.',
      'Multiply every resampled layer of every camera by the mask, so all cameras are measured on the same pixels.'],
     'Accuracy assessment: Congalton (1991); same pixels for all sensors after masking: Feng et al. (2022), Maimaitijiang et al. (2020).')
CARD('erosion', 'Morphological erosion and mask accuracy assessment', 'Erosion removes the outer pixel ring of each vegetation patch; the confusion matrix compares mask classes with reference classes.',
     'Removes mixed edge pixels and proves that the mask is reliable.', 'Erosion with a 3 × 3 structuring element (one pixel); reference pixels from the red–green–blue image; overall accuracy ≥ 90% required.',
     'Size of the structuring element (one pixel to avoid losing small plants).', 'High-resolution masks with many leaf edges.',
     'Simple and widely used; accuracy assessment is required to report a mask.', 'Soille (2003); Congalton (1991)')

# ---------------------------------------------------------------- D
H2('Activity D – Subplot spectra and feature extraction')
P('Features are calculated for every subplot-date and kept in groups by type ([[F:features]]). The grouping matters because one selection method is later used for each type of feature (Objective 1).')
FIG('features', 'g04_features.png', 'Flow chart of Activity D (Steps D1–D6; Steps D7–D8 complete the feature table).', 540)
STEP('D1', 'Plot and subplot polygons',
     'Each sample must cover exactly the scored subplot.',
     'Field layout; plot numbers; aligned images.',
     '192 subplot polygons with codes → Step D2.',
     ['Digitise the 48 plot polygons once and add the plot number.', 'Split each plot into four quadrant subplots that match the field scoring; apply an inner buffer to exclude border rows and bunds.', 'Use the same polygons on all dates and for all cameras.'],
     'Plot polygons after soil masking: Liu et al. (2024), Feng et al. (2022); fixed sampling regions: Ma et al. (2026).')
STEP('D2', 'Subplot mean spectra',
     'Models need one value per feature and subplot that represents the scored canopy.',
     'Masked layers of all cameras; subplot polygons.',
     'One mean spectrum (and mean band values) per subplot, date and camera → Steps D3–D7 and Activity E.',
     ['Average the masked vegetation pixels inside each subplot for every band of every camera.', 'Join the covariates of Step A6 by the subplot code and date.'],
     'Plot-mean spectra after masking: Guo et al. (2021), Mustafa et al. (2023), Ma et al. (2026).')
FIG('dummyspec', 'g11_dummy_spectra.png', 'Dummy example of subplot mean spectra by severity grade (a) and the first derivative in the red-edge region (b). The water-vapour regions are removed.', 560)
STEP('D3', 'Hyperspectral spectral features',
     'Reflectance alone does not show red-edge shifts clearly; derivatives and red-edge parameters make them visible.',
     'Subplot mean reflectance (483 bands).',
     'Spectral group: reflectance (483), first derivative (483) and red-edge parameters → Objective 1 (Activities 1.2 and 1.4).',
     ['Reflectance of the 483 bands.',
      'First derivative of each smoothed segment: FD(λ_{i}) = [R(λ_{i+1}) − R(λ_{i−1})] / (λ_{i+1} − λ_{i−1}); derivative bands within 10 nm of a removed region are not used.',
      'Red-edge parameters: red-edge position (wavelength of the maximum first derivative between 680 and 760 nm), red-edge amplitude (that maximum value) and red-edge area (sum of the first derivative from 680 to 760 nm).',
      'The second derivative is not used, because it amplifies noise at UAV signal-to-noise levels and adds hundreds of unstable variables.'],
     'Derivative analysis: Tsai and Philpot (1998); red edge: Horler et al. (1983), Filella and Peñuelas (1994); red-edge parameters best for the early stage of pine wilt disease from UAV hyperspectral data: Yu et al. (2021); noise amplification by derivatives: Rinnan et al. (2009).')
P('**Worked example (dummy data).** If R(700 nm) = 0.10 and R(704 nm) = 0.14, the first derivative at 702 nm is (0.14 − 0.10) / 4 = 0.010 nm^{−1}. If the largest first derivative between 680 and 760 nm is 0.012 nm^{−1} at 718 nm, the red-edge position is 718 nm and the amplitude is 0.012 nm^{−1}. In diseased canopies the red-edge position moves to shorter wavelengths ([[F:dummyspec]]b).')
CARD('fd', 'First derivative and red-edge parameters', 'The derivative measures the slope of the spectrum; it removes constant offsets (for example brightness differences) and turns the red edge into a peak whose position and height can be measured.',
     'Makes the chlorophyll-related red-edge shift measurable and reduces background effects.', 'Central difference on Savitzky–Golay smoothed segments; red-edge position, amplitude and area from 680–760 nm.',
     'No tuning; the smoothing window (Step B3) controls the noise of the derivative.', 'Smoothed hyperspectral spectra with dense band spacing.',
     'Red-edge parameters were the best features for separating early-stage diseased trees from healthy trees (Yu et al., 2021).', 'Tsai and Philpot (1998); Filella and Peñuelas (1994); Yu et al. (2021)')
STEP('D4', 'Vegetation indices',
     'General physiological changes (pigments, structure, water) are captured best by published indices that have known meaning.',
     'Subplot mean reflectance.',
     'Index group (published indices + red-edge parameters; the searched indices of Activity 1.3 are added later) → Activity 1.4.',
     ['Compute the published indices in five groups: pigment (for example PRI, ARI, CARI, MCARI, PSRI, PSSRb), structure (NDVI, OSAVI, SR, RVI, MSR), red edge (NDRE, MTCI, CIrededge, CIgreen, RVSI), water (NDWI, MSI, NDII, WBI) and disease (DWSI, RBI); the indices used by Ma et al. (2026) are all included.',
      'Check every formula against the original paper and use the nearest available band.',
      'Index definitions are given in Chapter 7 ([[T:hsidx]]).'],
     'Index groups for disease detection: Mahlein et al. (2013), Huang et al. (2014), Ma et al. (2026); pigment indices: Gamon et al. (1992), Gitelson et al. (2003), Merzlyak et al. (1999); water and disease indices: Gao (1996), Apan et al. (2004); PSRI and PSSRb for rice bacterial leaf blight: Das et al. (2015).')
CARD('vi', 'Vegetation indices', 'Arithmetic combinations (differences, ratios, normalised differences) of reflectance at wavelengths sensitive to a plant property, which cancel part of the illumination and background effect.',
     'Turns many bands into a few physiologically meaningful variables that can be compared with other studies and sensors.', 'About 48 published hyperspectral indices, 12 multispectral indices and 6 colour indices (Chapter 7).',
     'No hyper-parameters; formulas fixed by the original papers.', 'Canopy reflectance at UAV and satellite scales.',
     'Interpretable, transferable and easy to apply to cheaper sensors.', 'Mahlein et al. (2013); Huang et al. (2014); Ma et al. (2026)')
STEP('D5', 'Texture features from the grey-level co-occurrence matrix (GLCM)',
     'White pustules and chlorotic patches make the canopy surface heterogeneous; spectra do not record this spatial pattern.',
     'Masked hyperspectral cube; red–green–blue image at native resolution; multispectral and thermal layers.',
     'Texture groups of each camera → Activity 1.5 (hyperspectral) and Activity 1.6 (other cameras).',
     ['Hyperspectral: reduce the cube with principal component analysis and keep the first three components (cumulative variance above 95%); compute texture on these three component images (Activity 1.5).',
      'For every image used, quantise the grey levels to 32 levels and compute the grey-level co-occurrence matrix (GLCM) in a 3 × 3 moving window at distance 1, averaged over four directions (0°, 45°, 90°, 135°).',
      'Compute eight texture measures: mean, variance, homogeneity, contrast, dissimilarity, entropy, second moment and correlation; average them over the vegetation pixels of the subplot.',
      'Red–green–blue: texture of the R, G and B bands (24 features); multispectral: texture of the five bands (40); thermal: texture of the temperature image (8).'],
     'GLCM: Haralick et al. (1973), Hall-Beyer (2017); texture from principal-component images of UAV hyperspectral data: Guo et al. (2021), Ma et al. (2026); texture as a feature group for Fusarium head blight: Liu et al. (2020).')
TAB('glcmex', [['Image row', 'Grey levels of the 4 × 4 image', 'GLCM counts (grey levels 0–3)', 'Texture measure', 'Value'],
    ['1', '0 0 1 1', '4 2 1 0', 'contrast', '0.583'], ['2', '0 0 1 1', '2 4 0 0', 'homogeneity', '0.808'], ['3', '0 2 2 2', '1 0 6 1', 'dissimilarity', '0.417'],
    ['4', '2 2 3 3', '0 0 1 2', 'entropy', '2.095'], ['', '', '24 neighbour pairs in total', 'second moment', '0.146']],
    'Worked example (dummy data): grey-level co-occurrence matrix (horizontal neighbours, both directions) and texture of a small image. Each count is divided by 24 to give probabilities before the measures are computed.', [1300, 2300, 2500, 1900, 1306])
CARD('glcm', 'Grey-level co-occurrence matrix (GLCM) texture', 'Counts how often pairs of grey levels occur next to each other; statistics of this matrix describe smoothness (homogeneity), local variation (contrast, dissimilarity), disorder (entropy) and uniformity (second moment).',
     'Describes the spatial pattern of pustules, chlorotic patches and canopy gaps, which spectra cannot.', '32 grey levels, 3 × 3 window, distance 1, four directions averaged, eight measures, averaged over vegetation pixels.',
     'Window size, distance and number of grey levels; fixed at small values because pustules are only a few pixels wide at 2.2 cm; 5 × 5 window is tested as a check.', 'High-resolution images where the target produces a spatial pattern (2–5 cm pixels).',
     'The most widely used and best-understood texture method in remote sensing; used in the main white-rust-like disease studies.', 'Haralick et al. (1973); Hall-Beyer (2017); Guo et al. (2021)')
CARD('pca', 'Principal component analysis (PCA)', 'Rotates correlated variables into uncorrelated components ordered by the variance they explain.',
     'Reduces 483 correlated bands to three images that keep most of the information, so texture is computed on 3 images instead of 483.', 'Computed on the masked vegetation pixels of all dates (training data); first three components kept (cumulative variance above 95%).',
     'Number of components: the smallest number with at least 95% cumulative variance ([[F:dummyrelief]]b).', 'Many highly correlated variables, such as hyperspectral bands.',
     'Used in exactly this role by Guo et al. (2021) and Ma et al. (2026).', 'Jolliffe and Cadima (2016); Guo et al. (2021); Ma et al. (2026)')
STEP('D6', 'Multispectral and red–green–blue features',
     'The cheaper cameras need their own features so that their value can be compared with the hyperspectral camera.',
     'Masked subplot means of the multispectral and red–green–blue images.',
     'Multispectral group (5 bands, 12 indices, 10 two-band normalised differences, 40 texture features) and colour group (6 colour indices, hue–saturation–value means, 24 texture features) → Activity 1.6.',
     ['Multispectral: band reflectance, NDVI, GNDVI, NDRE, CIgreen, CIrededge, MTCI, OSAVI, SAVI, TCARI, MCARI, MSR, PSRI and the ten normalised differences of the five bands.',
      'Red–green–blue: excess green, excess red, excess green minus excess red, VARI, GLI, NGRDI and mean hue, saturation and value.',
      'Formulas are in Chapter 7.'],
     'Multispectral indices and texture for wheat powdery mildew: Liu et al. (2024); multispectral and very-high-resolution indices for wheat rusts: Blasch et al. (2023); colour indices: Woebbecke et al. (1995), Meyer and Neto (2008).')
STEP('D7', 'Thermal features',
     'Infection changes transpiration and canopy temperature, but temperature also changes with weather and time.',
     'Masked thermal subplot values; air temperature; healthy-plot temperatures of the same date.',
     'Thermal group → Activity E (normalisation) and Activity 1.6.',
     ['Canopy temperature: mean, median, standard deviation, 10th and 90th percentiles of the vegetation pixels.',
      'Normalised thermal features (Step E1): canopy minus air temperature, normalised relative canopy temperature, crop water stress index and difference from the healthy plots of the same date and variety.',
      'Thermal texture (Step D5).'],
     'Thermal features for powdery mildew: Feng et al. (2022), Liu et al. (2024); canopy minus air temperature for downy mildew from a UAV: Calderón et al. (2014); reviews: Pineda et al. (2021), Messina and Modica (2020).')
STEP('D8', 'Feature table',
     'All later steps need one table layout for every camera so that sensor sets are simple joins.',
     'Features of Steps D3–D7.',
     'One table per camera with identifiers, labels, covariates and features → Activities E and F.',
     ['Columns: identifiers (date, days after inoculation, plot, subplot, replication, treatment, variety, inoculation timing, fold), labels (score, class, detection label), covariates (days after inoculation, variety, inoculation timing, growth stage, weather summaries) and features with a group prefix (R_, FD_, RE_, VI_, TX_, TH_).',
      'Rows: one per subplot-date.'],
     'Structured multi-sensor feature tables: Maimaitijiang et al. (2020), Feng et al. (2022).')
TAB('featcount', [['Camera', 'Feature groups', 'Approximate number'], ['Hyperspectral', 'reflectance 483, first derivative 483, red-edge parameters 3, published indices about 48, principal-component texture 24 (+ searched indices and TTFI)', '≈ 1040'],
    ['Multispectral', '5 bands, 12 indices, 10 normalised differences, 40 texture', '67'], ['Red–green–blue', '6 colour indices, 3 colour means, 24 texture', '33'], ['Thermal', '5 temperature statistics, 4 normalised temperatures, 8 texture', '17'],
    ['Covariates', 'days after inoculation, variety, inoculation timing, growth stage, weather (T_{max}, T_{min}, RH, rainfall)', 'not used as disease features']], 'Feature groups before selection.', [1800, 5600, 1906])

# ---------------------------------------------------------------- E
H2('Activity E – Normalisation and data preparation')
P('Normalisation removes effects that are not caused by the disease (weather, date, variety, units) and prepares the features for the models ([[F:normal]]). Step E1 is done once on all data because it does not use the labels; Steps E2–E4 use statistics that are computed on the training part of each fold only. Date-to-date consistency of reflectance relies on the calibration panels flown on every date (Step B1).')
FIG('normal', 'g25_normalisation.png', 'Flow chart of Activity E (Steps E1–E4).', 540)
STEP('E1', 'Thermal normalisation',
     'Canopy temperature changes with air temperature, radiation and time of flight, which can hide the disease effect.',
     'Canopy temperature statistics; air temperature; wet and dry reference temperatures.',
     'Normalised thermal features → Activity 1.6 and Objectives 2–3.',
     ['Canopy minus air temperature: CTD = T_{c} − T_{air}.',
      'Normalised relative canopy temperature over the field on that date: NRCT = (T_{c} − T_{min}) / (T_{max} − T_{min}).',
      'Crop water stress index: CWSI = (T_{c} − T_{wet}) / (T_{dry} − T_{wet}) with wet and dry references in the field.',
      'Difference from healthy plots of the same date and variety (Step E2).'],
     'Normalisation of canopy temperature by air temperature: Idso et al. (1981), Pineda et al. (2021); canopy minus air temperature for downy mildew detection from a UAV: Calderón et al. (2014); thermal indices and environmental effects: Jones et al. (2009), Maes and Steppe (2012), Oerke et al. (2006).')
P('**Worked example (dummy data).** A subplot has T_{c} = 24.6 °C when T_{air} = 22.0 °C, so CTD = +2.6 °C. On that date the field minimum and maximum canopy temperatures are 21.8 and 26.2 °C, so NRCT = (24.6 − 21.8) / (26.2 − 21.8) = 0.64.')
STEP('E2', 'Healthy-plot normalisation',
     'Early disease effects are small compared with the differences caused by date, crop age and variety; a same-day, same-variety healthy reference removes most of them.',
     'Features of all subplots; features of the healthy plots of the same date and variety in the training part (two or three plots of different inoculation timings, Step F1).',
     'Healthy-normalised features → Objective 3 (all features) and thermal difference features (Objectives 1–2).',
     ['For every feature, date and variety, compute the mean and standard deviation of the healthy subplots of that variety in the training part (8–12 subplots).',
      'Normalised value: z_{h} = (x − mean_{healthy}) / SD_{healthy}.',
      'Apply the same healthy-plot reference to the test samples of that date and variety.'],
     'Healthy references for thermal disease detection: Oerke et al. (2006); healthy references in pre-visual detection: Zarco-Tejada et al. (2018), Poblete et al. (2023); pre-symptomatic hyperspectral detection: Zhu et al. (2017).')
P('**Worked example (dummy data).** On one date the healthy plots of variety V1 have mean canopy temperature 23.8 °C (standard deviation 0.4 °C). An inoculated V1 subplot at 24.6 °C gets z_{h} = (24.6 − 23.8) / 0.4 = +2.0, that is, two healthy standard deviations warmer.')
CARD('healthy', 'Healthy-plot (control) normalisation', 'Expresses each value as its distance from healthy plants measured on the same day, of the same variety and age, in units of their natural variation.',
     'Removes date, weather, crop-age and variety effects so that only the disease effect remains; essential when symptoms are not yet visible.', 'Reference: healthy plots of the same date and variety in the training part (rotated across folds, Step F1); mean and standard deviation per feature.',
     'No hyper-parameters.', 'Experiments with healthy controls on every date; thermal and early-stage spectral data.',
     'Simple and directly justified by the design (one healthy plot for every treatment).', 'Oerke et al. (2006); Zarco-Tejada et al. (2018)')
STEP('E3', 'Standardisation (z-score) with training statistics',
     'Features have different units and ranges (reflectance 0–1, temperature 15–30 °C, texture 0–1000); distance- and gradient-based models are dominated by large-range features.',
     'Selected features of the training part and test part of each fold.',
     'Standardised features (mean 0, standard deviation 1 in the training part) → all models.',
     ['Compute the mean and standard deviation of every feature on the training part of the fold.', 'Standardise: z = (x − mean_{train}) / SD_{train}, for training and test samples alike.', 'Repeat for every fold; the test part never contributes to the statistics.'],
     'Pre-processing inside resampling: Kuhn and Johnson (2013); feature scaling for support vector machines and neural networks: Mountrakis et al. (2011), Kattenborn et al. (2021).')
P('**Worked example (dummy data).** In one training part NDVI has mean 0.72 and standard deviation 0.08. A test subplot with NDVI = 0.60 is standardised to z = (0.60 − 0.72) / 0.08 = −1.5.')
CARD('zscore', 'z-score standardisation', 'Subtracts the mean and divides by the standard deviation, so every feature has mean 0 and unit variance.',
     'Puts features with different units on one scale so that no feature dominates distances, kernels or gradient steps.', 'Training statistics of each fold; applied to all models (tree models do not need it but receive the same input for simplicity).',
     'No hyper-parameters.', 'Mixed feature types (reflectance, indices, texture, temperature).',
     'Required by support vector machines, k-nearest neighbours, partial least squares and neural networks.', 'Kuhn and Johnson (2013)')
STEP('E4', 'Class weights',
     'The severity classes have unequal sizes (for example 512 healthy vs 120 grade-9 samples); models tend to ignore small classes.',
     'Class counts of the training part.',
     'Class weights for the loss functions of all classifiers → Objectives 2–3.',
     ['Weight of class c: w_{c} = N / (k × n_{c}), where N is the number of training samples, k the number of classes and n_{c} the size of class c.', 'Use the weights in the loss (support vector machine, random forest, extreme gradient boosting, neural networks).', 'Report macro-averaged metrics, which give each class equal importance.'],
     'Class imbalance in deep learning: Johnson and Khoshgoftaar (2019); macro-averaged metrics: Sokolova and Lapalme (2009).')
P('**Worked example (dummy data).** With N = 1280 training samples, k = 6 classes and 80 samples of grade 9, the weight of grade 9 is 1280 / (6 × 80) = 2.67, while the weight of a class with 341 samples is 1280 / (6 × 341) = 0.63.')

# ---------------------------------------------------------------- F
H2('Activity F – Validation design and tuning')
STEP('F1', 'Leave-one-replication-out (LORO) outer folds',
     'Subplots of one plot, and plots of one replication, are similar; random splits put near-identical samples in training and test data and inflate accuracy.',
     'Labelled feature tables.',
     'Three outer folds → all models of Objectives 2 and 3.',
     ['Fold 1 tests replication R1, fold 2 tests R2, fold 3 tests R3 (leave-one-replication-out, LORO).',
      'The 12 healthy plots are rotated so that every fold contains one healthy plot of each inoculation timing and at least one of each variety ([[T:healthyrot]]). Every training part then holds two or three healthy plots of every variety, which the healthy-plot normalisation (Step E2) needs, and every test fold contains healthy samples of all three varieties.',
      'All dates and all four subplots of a plot stay in the same fold; each test fold has about 640 post-symptomatic (or 192 pre-symptomatic) samples.',
      'The same three folds are used for every sensor set, task and model.'],
     'Grouped (blocked) cross-validation: Roberts et al. (2017); healthy references of the same variety needed for normalisation: Oerke et al. (2006), Zarco-Tejada et al. (2018); spatial validation shows that random splits overestimate accuracy: Ploton et al. (2020); the random 7:3 split of Ma et al. (2026) is the optimistic design this step avoids, while its cross-year test supports testing on independent units.')
TAB('healthyrot', [['Outer fold', 'Inoculated plots tested', 'Healthy plots tested (variety–timing, plot number)'], ['1', 'replication R1 (plots 37–48)', 'V1-D1 (7), V2-D2 (2), V3-D3 (10), V1-D4 (12)'], ['2', 'replication R2 (plots 25–36)', 'V2-D1 (5), V3-D2 (8), V1-D3 (4), V2-D4 (1)'], ['3', 'replication R3 (plots 13–24)', 'V3-D1 (3), V1-D2 (9), V2-D3 (11), V3-D4 (6)']],
    'Rotation of the 12 healthy plots across the outer folds: each fold has every inoculation timing once and every variety at least once.', [1500, 3300, 4506])
FIG('validation', 'g09_validation.png', 'Leave-one-replication-out outer folds with the rotated healthy plots, and the inner cross-validation used for selection and tuning.', 520)
STEP('F2', 'Nested inner cross-validation and hyper-parameter tuning',
     'Feature selection and tuning done on all data (or on the test fold) give over-optimistic accuracy.',
     'Training part of each outer fold.',
     'Selected features, tuned hyper-parameters and early-stopping epochs for each outer fold → final training and one test prediction.',
     ['Inside the training replications, make three inner folds grouped by plot.',
      'Run all label-based steps inside this inner loop: index search, SHAP-CARS, ReliefF, mRMR, TTFI search, sequential floating forward selection, grid search of hyper-parameters and early stopping of neural networks (validation on plots that are not used for training).',
      'Choose the hyper-parameters with the best mean inner score (macro-F1 for classes, root-mean-square error for the score).',
      'Retrain the model on the whole training part with these settings and predict the test replication once.'],
     'Nested cross-validation: Varma and Simon (2006), Cawley and Talbot (2010); selection bias when features are chosen outside the folds: Ambroise and McLachlan (2002).')
CARD('nested', 'Grouped nested cross-validation with grid search', 'An outer loop estimates accuracy on unseen replications; an inner loop inside the training part chooses features and hyper-parameters. Grid search tries every combination in a small grid.',
     'Gives an almost unbiased accuracy estimate and prevents information from the test replication entering the model.', 'Outer: 3 folds (leave-one-replication-out); inner: 3 folds grouped by plot; grids in [[T:mlgrid]] and Step 2.3.8.',
     'The grids themselves; kept small (2–5 values per parameter) to limit overfitting of the selection.', 'Small, grouped datasets such as plots × dates.',
     'Standard practice for honest accuracy; required because many label-based steps are used.', 'Varma and Simon (2006); Cawley and Talbot (2010); Roberts et al. (2017)')
STEP('F3', 'Leakage checklist',
     'A single step done on all data can leak test information into the model.',
     'All steps of the methodology.',
     'Checklist of where every step is run ([[T:leak]]) → applied in all objectives.',
     ['List every step that uses labels or data statistics.', 'Assign it to "once on all data" (no labels), "training part" (statistics) or "inner folds" (labels).', 'Check the code of every objective against the list before running the final models.'],
     'Ambroise and McLachlan (2002); Kuhn and Johnson (2013).')
TAB('leak', [['Step', 'Uses labels?', 'Where it is run'], ['Activities B–D (pre-processing, mask, features)', 'no', 'once, on all data'], ['E1 (thermal normalisation)', 'no', 'once, on all data'],
    ['E2 (healthy-plot normalisation)', 'no (uses healthy plots)', 'training healthy plots → applied to test data'], ['E3–E4 (standardisation, class weights)', 'no (statistics)', 'training part of each fold'], ['Covariate coding (Step A6)', 'no', 'once; standardised with training statistics'],
    ['Within-group redundancy (|r| ≥ 0.95), variance inflation factor', 'no', 'training part of each fold'], ['NDSI/RSI and White Rust Index search, SHAP-CARS, ReliefF, mRMR, TTFI search', 'yes', 'inner folds only'],
    ['Sequential floating forward selection, hyper-parameter tuning, early stopping', 'yes', 'inner folds only'], ['Final evaluation', 'yes', 'test replication, once'], ['Second-stage validation (Bharatpur)', 'yes', 'once, with frozen final models; never used for selection, tuning or training']],
    'Where each step is run so that no information from the test replication enters the model.', [4300, 1900, 3106])
TAB('foldsize', [['Dataset', 'Training part per outer fold', 'Test part per outer fold', 'Inner folds'], ['Post-symptomatic (1920 per camera)', '≈ 1280 samples', '≈ 640 samples', '3, grouped by plot'], ['Pre-symptomatic (576 per camera)', '≈ 384 samples', '≈ 192 samples', '3, grouped by plot']],
    'Approximate sizes of the training and test parts.', [2800, 2600, 1900, 2006])

exec(open(B + 'mf3_obj.py').read())
exec(open(B + 'mf3_end.py').read())
open(B + 'mf3_body.js', 'w').write('\n'.join(K)); print('body lines', len(K))
