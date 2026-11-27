"""Reconstructed field methodology (Objectives 1-3): body of the Word document (docx JS)."""
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

def STEP(code, title, problem, inp, out, done, why, papers, sensors=None, settings=None, note=None):
    """One methodology step in a fixed template."""
    H3('%s  %s' % (code, title))
    TAB('t' + re.sub(r'\W', '', code).lower(), [['Item', 'Description'], ['Problem solved', problem], ['Input', inp], ['Output → next step', out]],
        'Step %s at a glance.' % code, [1900, 7406], 17)
    P('**What is done.**'); NL(done)
    P('**Why this method.** ' + why)
    P('**Studies that used the same step.** ' + papers)
    if sensors: P('**For each sensor.**'); BL(sensors)
    if settings: P('**Settings.** ' + settings)
    if note: NOTE(note)

exec(open(B + 'mf_more2.py').read())
# =====================================================================================
# TITLE
# =====================================================================================
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1200, after: 200 }, children: [new TextRun({ text: 'AI-based multimodal UAV sensing of white rust in mustard', font: FONT, size: 44, bold: true, color: '1E3A1F' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [new TextRun({ text: 'Reconstructed research methodology for the field experiment: Objectives 1, 2 and 3, step by step', font: FONT, size: 28, color: '2C5F2D' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: 'Hyperspectral, multispectral, RGB and thermal UAV data | 15 sensor sets | feature-level fusion with machine learning and deep learning', font: FONT, size: 22, italics: true })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 700 }, children: [new TextRun({ text: 'Animesh Panda (Roll No. 13098) | Ph.D. Agricultural Physics | ICAR-Indian Agricultural Research Institute, New Delhi', font: FONT, size: 20 })] }));")
BOX('How to read this document.', 'Each chapter is one block of the work and the blocks are used in the order of the chapters: field data (Chapter 2) → pre-processing (Chapter 3) → feature extraction (Chapter 4) → validation framework (Chapter 5) → Objective 1 (Chapter 6) → Objective 2 (Chapter 7) → Objective 3 (Chapter 8). Every step uses the same template: the problem it solves, its input, what is done, why this method was chosen, which published studies used the same step, details for each sensor, and the output that goes to the next step. Methods are kept as simple as the objectives allow, statistics are limited to what is needed, and every method carries its reference.', 'EEF3E8', '2C5F2D')
BOX('Design decisions fixed for the whole study.', '(1) Field experiment only (IARI, rabi 2025-26); the glasshouse study is not used here. (2) The modelling unit is the subplot-date; each subplot has its own canopy severity score. (3) All four sensors are brought to the hyperspectral grid and measured on the same vegetation pixels (soil, grass and shadow removed; leaves and flowers kept). (4) Fusion is feature-level only, with both machine learning and deep learning. (5) Both classification and regression are done. (6) Every step that uses the severity labels runs inside the training folds of a plot-grouped cross-validation.')

K.append("K.push(new Paragraph({ children: [new PageBreak()] }));")
K.append("K.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: 'Contents', font: FONT, size: 32, bold: true, color: '1E3A1F' })] }));")
K.append("K.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-3' }));")
K.append("K.push(new Paragraph({ children: [new PageBreak()] }));")


H1('Abbreviations')
TAB('abbr', [['Abbreviation', 'Meaning', 'Abbreviation', 'Meaning'],
 ['AUC', 'area under the ROC curve', 'MNF', 'minimum noise fraction'], ['CT, CTD', 'canopy temperature; CT minus air temperature', 'mRMR', 'minimum redundancy maximum relevance'], ['CWSI', 'crop water stress index', 'MS', 'multispectral'],
 ['DAI', 'days after inoculation', 'NDSI', 'normalised difference spectral index'], ['DL, ML', 'deep learning; machine learning', 'NRCT', 'normalised relative canopy temperature'], ['DNN-F1, DNN-F2', 'deep neural network with input- and intermediate-level feature fusion', 'OFC', 'optimum feature combination'],
 ['DSF', 'disease-specific feature', 'PLS-DA, PLSR', 'partial least squares discriminant analysis; regression'], ['FD, SD', 'first and second derivative of reflectance', 'PPI', 'pixel purity index'], ['GLCM', 'grey-level co-occurrence matrix (texture)', 'R', 'reflectance'],
 ['HS', 'hyperspectral', 'REP', 'red-edge position'], ['k-NN', 'k-nearest neighbours', 'RF, RFR', 'random forest classification; regression'], ['LORO', 'leave-one-replication-out', 'RGB', 'red–green–blue camera'],
 ['RMSE', 'root-mean-square error', 'RPD', 'ratio of performance to deviation'], ['SAM', 'spectral angle mapper', 'SE', 'squeeze-and-excitation attention'], ['SFFS', 'sequential floating forward selection', 'SHAP', 'Shapley additive explanations'],
 ['SVM, SVR', 'support vector machine; regression', 'TIR', 'thermal infrared'], ['VI', 'vegetation index', 'VIF', 'variance inflation factor'], ['WRI', 'White Rust Index', 'XGBoost', 'extreme gradient boosting']],
 'Abbreviations used in this document.', [1500, 3150, 1500, 3156], 16)
# =====================================================================================
H1('1. Objectives and overall design')
P('White rust, caused by the obligate oomycete Albugo candida, produces white pustules on leaves, chlorosis and, after systemic infection, distorted inflorescences (staghead) in Indian mustard, and can reduce yield by 20–60% (Kumar and Kalha, 2005; Saharan et al., 2014). The disease develops under cool, humid weather (Chattopadhyay et al., 2011). Visual scoring is slow and possible only after symptoms appear. Unmanned aerial vehicle (UAV) sensors record the pigment, structure, water and temperature changes that accompany infection, sometimes before symptoms are visible (Mahlein, 2016; Terentev et al., 2022), and combining sensors usually improves accuracy (Maimaitijiang et al., 2020; Feng et al., 2022).')
TAB('objectives', [['Objective (ORW wording)', 'Question answered in this methodology', 'Data used', 'Main output'],
    ['1. To characterise white rust of mustard through multimodal sensing from UAV platform', 'Which bands, indices, textures and thermal features of each sensor respond to white rust severity, and how does the response differ with variety and inoculation timing?', '1536 post-symptomatic subplot samples per sensor', 'Disease-specific feature (DSF) pools of each sensor; White Rust Index; response curves'],
    ['2. To detect and discriminate disease severity of white rust in mustard through AI based multimodal data fusion', 'How accurately can healthy vs diseased subplots, severity classes and the severity score be predicted by each of the 15 sensor sets with machine learning and deep learning?', '1536 post-symptomatic subplot samples per sensor', 'Best sensor set and model for each task; contribution of each sensor; severity maps'],
    ['3. To predict white rust at pre-symptomatic stage using machine learning technique(s)', 'Can subplots that will develop white rust be separated from healthy subplots before symptoms, and can their later severity be predicted?', '576 pre-symptomatic subplot samples per sensor', 'Pre-symptomatic models; earliest detection day; risk maps']],
    'Objectives, questions, data and outputs.', [2700, 3000, 1700, 1906], 16)
FIG('overall', 'f1_overall.png', 'Overall workflow of the field methodology. Each block is one chapter of this document; outputs of one block are the inputs of the next.', 560)
P('**Five rules apply to every chapter.** They come from the methodological literature on hyperspectral and multi-sensor modelling and from the weaknesses identified in recent disease-sensing studies (Ambroise and McLachlan, 2002; Varma and Simon, 2006; Roberts et al., 2017; Ma et al., 2026).')
NL(['One sample = one subplot on one date. The four subplots of a plot are never split between training and test data.', 'All sensors are measured on the same vegetation pixels of each subplot (Chapter 3).', 'Feature groups are built with physical meaning and thinned group by group before they are pooled (Chapter 4 and Stage 1–3 of the selection).', 'Every step that uses the severity labels (relevance screening, index search, final selection, tuning) runs inside the training folds only.', 'The same folds are used for all 15 sensor sets and all models, so their accuracies are directly comparable.'])


H2('Published studies on which the methodology is built')
P('Every step of this methodology was chosen because it has been used and tested for crop-disease sensing or for the specific data problem it solves. Table [[T:literature]] lists the main disease studies and the steps they support; the methodological references (validation, selection, models) are given in each step.')
TAB('literature', [['Study', 'Crop and disease', 'Sensors and data', 'What it showed', 'Steps supported'],
 ['Mahlein et al. (2013)', 'sugar beet; Cercospora, rust, powdery mildew', 'leaf hyperspectral', 'ReliefF bands combined into disease-specific indices', 'O1-3, O1-4'],
 ['Huang et al. (2014)', 'wheat; powdery mildew, yellow rust', 'leaf and canopy hyperspectral', 'ReliefF bands; new optimised indices transferred to canopy', 'O1-3, O1-4'],
 ['Shukla et al. (2024)', 'mustard; aphid stress', 'ground hyperspectral', 'correlation scalogram to find sensitive regions', 'O1-3, Stage 2'],
 ['Tian et al. (2021)', 'rice; leaf blast', 'spectra 350–2500 nm', 'disease-specific features, VIF → SFFS, asymptomatic stage', 'Stage 1, 3, 4; O3-1'],
 ['Mustafa et al. (2023)', 'wheat; Fusarium head blight', 'fluorescence + hyperspectral', 'Boruta and ML-SFFS; k-NN and SVM', 'O1-6, Stage 4'],
 ['Feng et al. (2022)', 'wheat; powdery mildew', 'hyperspectral + thermal + RGB', 'feature-level fusion of indices, thermal and texture; PLSR, SVR, RFR', 'F3, F4, fusion, O2-3'],
 ['Liu et al. (2024)', 'wheat; powdery mildew', 'UAV multispectral + thermal', 'red-edge indices and thermal features; RF; maps', 'F2, F4, O2-7'],
 ['Guo et al. (2021)', 'wheat; yellow rust', 'UAV hyperspectral', 'vegetation indices + texture; common resolution; masks', 'P5, P6, F3'],
 ['Maimaitijiang et al. (2020)', 'soybean yield', 'UAV RGB + multispectral + thermal', 'DNN with input- and intermediate-level fusion', 'O2-4'],
 ['Ma et al. (2026)', 'rice; blast', 'UAV hyperspectral', 'group-wise selection, texture index, SE attention, ablation', 'Stage 2, O2-4, O2-6'],
 ['Abdulridha et al. (2023)', 'wheat; stem rust', 'UAV hyperspectral, 960 plots', 'RF for severity classes and binary detection', 'O2-1, O2-3'],
 ['Mahlein et al. (2019)', 'wheat; Fusarium head blight', 'hyperspectral + thermal + fluorescence', 'sensor comparison and earliest detection day', 'O1-7, O3-5'],
 ['Zhu et al. (2017)', 'tobacco; mosaic virus', 'hyperspectral imaging', 'pre-symptomatic detection with retrospective labels', 'O3-1, O3-4'],
 ['Zarco-Tejada et al. (2018)', 'olive; Xylella fastidiosa', 'airborne hyperspectral + thermal', 'pre-visual detection and maps', 'O3-2, O3-5'],
 ['Yu et al. (2025)', 'rice; sheath blight', 'spectra + physiology', 'dual-branch fusion at the pre-symptomatic stage', 'O3-4'],
 ['Oerke et al. (2006)', 'cucumber; downy mildew', 'thermal imaging', 'temperature changes with disease and with environment', 'F4, O3-2'],
 ['Deng et al. (2024)', 'wheat; stripe rust', 'UAV multimodal', 'deep fusion for disease-index maps', 'O2-7']],
 'Main disease studies and the steps of this methodology they support.', [1750, 1700, 1750, 2500, 1606], 15)
# =====================================================================================
H1('2. Field experiment and dataset')
STEP('D1', 'Experimental design and treatments',
     'Defines the sources of variation (inoculation timing, variety, replication) so that disease effects can be separated from crop-stage and variety effects.',
     'IARI research farm, rabi 2025-26; factorial randomised block design.',
     '48 plots with known treatment, replication and plot number → subplots (D3) and validation folds (Chapter 5).',
     ['Four sowing dates at 10-day intervals (D1–D4: 20 Nov, 30 Nov, 10 Dec, 20 Dec 2025) with a single inoculation on 10 January 2026, so the crop was inoculated at about 50, 40, 30 and 20 days after sowing.',
      'Three varieties of different susceptibility (V1 Varuna, highly susceptible; V2 Pusa Vijay, moderately susceptible; V3 PM 38, resistant, as in the ORW).',
      'The 12 treatments (4 × 3) were inoculated in three replications (R1–R3) with a zoosporangial suspension of 1.5 × 10⁵ zoosporangia mL⁻¹ (Mishra et al., 2009), and one uninoculated healthy plot per treatment was kept: 36 inoculated + 12 healthy = 48 plots.',
      'Each plot carries a code (treatment, replication, plot number) that is stored with every sample.'],
     'A factorial design with staggered sowing produces a range of crop ages and severities on the same flight dates, which is necessary to learn severity rather than date. Healthy plots of every treatment give a same-stage, same-variety reference for each date, which is used for normalisation in Objective 3.',
     'Staggered sowing or inoculation timing to create severity gradients and healthy controls has been used for wheat yellow rust (Guo et al., 2021), wheat powdery mildew (Feng et al., 2022; Liu et al., 2024) and rice blast (Tian et al., 2021; Ma et al., 2026). The ORW design follows Mishra et al. (2009) for the inoculum.',
     note='Varieties and dates are taken from the ORW; correct them in Table D1 if the field sheets differ.')
STEP('D2', 'UAV flights and sensors',
     'Provides co-located, same-day images from four sensors that record different plant responses.',
     'Eight post-symptomatic flight dates and the pre-symptomatic flight dates; flights 11:00–14:00 h under clear sky and low wind, 30 m above ground, 85% front and 80% side overlap, calibration panels and RTK ground control points on every date.',
     'Raw images of four sensors for every date → pre-processing (Chapter 3).',
     ['Hyperspectral: Headwall Co-Aligned VNIR–SWIR imager (613 raw bands; 483 bands after quality control, 399–2398 nm; processed pixel ≈ 2.2 cm).', 'Multispectral: MicaSense RedEdge-MX (475, 560, 668, 717, 840 nm; ≈ 2 cm at 30 m).', 'RGB: DJI Phantom camera (≈ 0.8 cm at 30 m).', 'Thermal: FLIR Vue Pro R, 7.5–13.5 µm (≈ 3.9 cm at 30 m with the 13 mm lens).', 'Ground scoring is done on the same day as the flight, or within one day.'],
     'Each sensor measures a different response to infection: hyperspectral bands track pigment, structure and water in detail; multispectral bands track the red edge with a cheaper sensor; RGB records colour and canopy texture; thermal records stomatal and transpiration changes (Mahlein, 2016). A fixed solar window and panels make dates comparable.',
     'The same four sensor types were combined for wheat powdery mildew (Feng et al., 2022) and soybean yield (Maimaitijiang et al., 2020); UAV hyperspectral imaging was used for wheat stem rust (Abdulridha et al., 2023) and rice blast (Ma et al., 2026); the same-day pairing of scoring and flight follows Ma et al. (2026).')
STEP('D3', 'Subplots and the canopy severity score',
     'Turns each plot into four independently scored sampling units and gives each a label.',
     'Plot boundaries and the canopy severity score recorded for each of the four subplots on every date.',
     'Labelled subplot list (date, plot, subplot, treatment, replication, score) → labels (D4) and subplot extraction (P7–P8).',
     ['Each plot is divided into four quadrant subplots of equal size; border rows are excluded by an inner buffer.', 'One trained scorer records the canopy-level disease severity of each subplot with written grade limits (Bock et al., 2010), using the 0–9 grade key of Conn et al. (1990): 0 = no symptoms, 1 = 1–5%, 3 = 6–10%, 5 = 11–25%, 7 = 26–50%, 9 = > 50% of canopy leaf area with pustules; staghead is noted after flowering.', 'The score is entered with the subplot code so that it can be joined to the image features.'],
     'Scoring each subplot gives four labelled samples per plot instead of one and captures within-plot variability. The canopy score matches what the UAV sees (the canopy, including inflorescences), which is why flowers are kept in the subplot spectrum.',
     'Grade keys of this kind were used for canopy severity in UAV studies of wheat stem rust (Abdulridha et al., 2023), powdery mildew (Liu et al., 2024) and rice blast, where five canopy levels were defined from a disease index (Ma et al., 2026); the Conn et al. (1990) key is the standard key for Brassica foliar diseases.')
STEP('D4', 'Labels for the three tasks and the two datasets',
     'Defines exactly what each model predicts and which samples belong to which objective.',
     'Subplot scores of all dates; date of the first visible pustule in the field.',
     'Post-symptomatic dataset (1536 samples per sensor) and pre-symptomatic dataset (576 samples per sensor), each with its labels → all later chapters.',
     ['Post-symptomatic dates = dates on or after the first visible pustule; pre-symptomatic dates = earlier dates.', 'Binary label: healthy (score 0) vs diseased (score > 0), from the observed score (an inoculated subplot that shows no pustules is labelled healthy).', 'Severity classes: the six grades 0, 1, 3, 5, 7, 9; if a grade has fewer than 5% of samples, it is merged with its neighbour (for example 7 + 9).', 'Regression target: the canopy severity score of the subplot (treated as continuous).', 'Pre-symptomatic labels (Objective 3): healthy = subplots of healthy plots; infected = inoculated subplots that show pustules on a later date; inoculated subplots that never develop symptoms (mainly the resistant variety) are kept out of the infected class. Regression target = the severity score of the same subplot on the first post-symptomatic date.'],
     'Labels from the observed score (not from the treatment) avoid calling a symptomless inoculated subplot diseased. Retrospective labelling is the only way to know which pre-symptomatic samples were really infected. Regression is kept alongside classes because classes are cuts of a continuous severity and neighbouring classes overlap.',
     'Binary plus multi-class plus regression tasks were analysed together for rice blast (Tian et al., 2021) and wheat powdery mildew (Feng et al., 2022); retrospective pre-symptomatic labels were used by Zhu et al. (2017) and Tian et al. (2021); class overlap of neighbouring severity levels is reported by Ma et al. (2026), where the middle level was hardest for every model.')
TAB('dataset', [['Item', 'Value'], ['Plots × subplots', '48 × 4 = 192 subplots per image'], ['Sensors', '4 (hyperspectral, multispectral, RGB, thermal)'], ['Post-symptomatic samples per sensor', '1536 (8 dates × 192)'], ['Pre-symptomatic samples per sensor', '576'],
    ['Sensor sets analysed', '15 (4 single, 6 pairs, 4 triples, 1 all four)'], ['Tasks', 'binary detection, severity classes, severity regression (Objectives 2 and 3)']], 'Dataset used in this methodology (numbers as recorded by the researcher).', [3600, 5706])
FIG('dataset', 'f2_dataset.png', 'Structure of the dataset: flight dates → sensors → plots → scored subplots, and the two datasets used by the objectives.', 520)

# =====================================================================================
H1('3. Pre-processing (applied to every date and sensor)')
P('Pre-processing turns raw images into one table per date and sensor, with one row per subplot. It is identical for all objectives. Its central idea is that every sensor is aligned to the hyperspectral grid and measured on the same vegetation pixels.')
FIG('preproc', 'f3_preproc.png', 'Pre-processing steps P1–P8 with the output of each step.', 540)
STEP('P1', 'Radiometric calibration',
     'Raw digital numbers depend on illumination and sensor settings and cannot be compared between dates.',
     'Raw images, calibration-panel images, sunlight-sensor records, air temperature and humidity of each flight.',
     'Reflectance images (hyperspectral, multispectral), consistent RGB images and temperature images → P2.',
     ['Hyperspectral and multispectral: convert digital numbers to reflectance with the reflectance panels imaged before and after each flight (empirical line), using the sunlight sensor for illumination changes during the flight.', 'RGB: fixed exposure and white balance on all dates; values kept as digital numbers for colour indices and texture.', 'Thermal: radiometric conversion to temperature with emissivity 0.98 and the air temperature, humidity and flight height of each flight.'],
     'The empirical line method is the standard way to obtain surface reflectance from airborne images with ground panels, and emissivity and atmospheric corrections are needed for absolute canopy temperature.',
     'Empirical line: Smith and Milton (1999); panel calibration for UAV hyperspectral disease studies: Guo et al. (2021), Ma et al. (2026); thermal conversion for crop canopies: Jones et al. (2009), Liu et al. (2024).')
STEP('P2', 'Orthomosaics and georeferencing',
     'Individual frames must be joined into one map per sensor and date with correct ground coordinates.',
     'Calibrated frames and RTK ground control points.',
     'Georeferenced orthomosaics (RGB, multispectral, thermal) and georectified hyperspectral cubes → P3 and P4.',
     ['Build orthomosaics by structure-from-motion for the frame cameras; georectify the push-broom hyperspectral lines with the IMU/GNSS data.', 'Use the same RTK ground control points on every date so that all dates share one coordinate frame.'],
     'Accurate georeferencing is the precondition for co-registration and for extracting the same subplots on every date.',
     'Guo et al. (2021) and Ma et al. (2026) produced georeferenced UAV hyperspectral mosaics before sampling; Maimaitijiang et al. (2020) and Feng et al. (2022) mosaicked RGB, multispectral and thermal images before feature extraction.')
STEP('P3', 'Hyperspectral cube quality control',
     'Water-vapour absorption, detector edges and noise make some bands unusable, and smoothing across gaps creates artefacts.',
     'Georectified 613-band cube of each date.',
     'Clean 483-band reflectance cube on a 2.2 cm grid → P4.',
     ['Keep VNIR up to 919.7 nm and SWIR from 921.4 nm; remove the water-vapour regions 1335–1460 and 1785–1965 nm and the noisy ends (900–915 nm and > 2400 nm), giving 483 bands.', 'Drop the three isolated bands at 916–920 nm (detector edge).', 'Apply Savitzky–Golay smoothing (window 5, second-order polynomial) separately to each continuous band segment (399–899, 921–1329, 1461–1779, 1971–2398 nm), never across a gap.', 'Check that reflectance is on a 0–1 scale.'],
     'Atmospheric water vapour makes 1350–1450 and 1800–1950 nm unreliable for UAV data. Savitzky–Golay smoothing reduces noise while keeping absorption features and is required before derivatives, but a window that crosses a band gap mixes distant wavelengths.',
     'Removal of water-vapour bands: Thenkabail et al. (2004); Savitzky–Golay smoothing: Savitzky and Golay (1964), used before derivatives by Tsai and Philpot (1998) and in disease studies by Tian et al. (2021) and Mustafa et al. (2023); spectral pre-processing review: Rinnan et al. (2009).')
STEP('P4', 'Projection and co-registration to the hyperspectral image',
     'Images of different sensors do not overlap exactly; small shifts mix canopy and soil values at edges.',
     'Georeferenced images of all sensors for one date.',
     'All images in WGS 84 / UTM 43N and aligned to the hyperspectral image → P5.',
     ['Project every image to WGS 84 / UTM zone 43N so that distances are in metres.', 'Register RGB, multispectral and thermal images to the hyperspectral image with tie points (plot corners, markers) and a first- or second-order polynomial transformation.', 'Accept the registration when the root-mean-square error of independent check points is below one hyperspectral pixel (2.2 cm).'],
     'The hyperspectral image is the reference because the vegetation mask is made from it. Misregistration of even a fraction of a pixel causes large errors when images are compared pixel by pixel.',
     'Image registration methods: Zitová and Flusser (2003); effect of misregistration: Dai and Khorram (1998); polynomial warping: Richards (2013); co-registered multi-sensor UAV layers: Maimaitijiang et al. (2020), Feng et al. (2022).')
STEP('P5', 'Resampling to the hyperspectral grid',
     'Sensors have different pixel sizes (≈ 0.8, 2, 2.2 and 3.9 cm); one grid is needed so that pixel (row, column) is the same ground point in every layer.',
     'Co-registered images.',
     'All layers on the 2.2 cm hyperspectral grid → P6 and P8.',
     ['RGB (finer): pixel aggregate (area mean), so each new pixel is the mean of the RGB pixels it covers.', 'Multispectral (similar size): bilinear interpolation.', 'Thermal (coarser): nearest neighbour, which keeps the measured temperatures.', 'RGB texture features are computed before resampling, at native resolution and inside the same mask (P8), because resampling removes fine texture.'],
     'Area averaging avoids aliasing when moving to a coarser grid; nearest neighbour preserves original values when moving to a finer grid; snapping all layers to one grid allows one mask and one set of subplot polygons for all sensors.',
     'Resampling methods: Richards (2013); nearest-neighbour resampling of UAV layers to a common resolution: Guo et al. (2021); common-grid stacking of RGB, multispectral and thermal data: Maimaitijiang et al. (2020).')
STEP('P6', 'Vegetation mask from the hyperspectral image',
     'Soil, grass/weeds and shadow inside a plot change reflectance, texture and temperature and must be removed before disease features are extracted.',
     'Clean hyperspectral cube; training regions of soil, shadow, grass, mustard canopy and flowers.',
     'Binary mask (1 = mustard canopy, stressed canopy, flowers; 0 = soil, grass, shadow) on the hyperspectral grid → applied to all sensors in P8.',
     ['Build one endmember library for the whole field with the hourglass workflow: minimum noise fraction (MNF), pixel purity index (PPI) on the MNF bands and n-dimensional cluster selection; build it once from pixels sampled on all dates.', 'Classify every pixel with the spectral angle mapper (SAM); calibrate the angle threshold on labelled pixels.', 'Keep green canopy, stressed (chlorotic) canopy and flower classes; remove soil, grass and shadow. Because yellow petals have low NDVI, the vegetation rule is NDVI > 0.6 OR flower class.', 'Apply a one-pixel morphological erosion to remove mixed edge pixels.', 'Check the mask on independent reference pixels from RGB (overall accuracy and kappa).'],
     'The hyperspectral image separates soil, shadow, weeds, green leaves and yellow flowers far better than three or five broad bands. A field-wide endmember library gives the same classes in every plot and on every date (unlike per-plot endmember extraction). Flowers are kept because the canopy score includes the inflorescence (staghead).',
     'MNF: Green et al. (1988); PPI and n-D endmembers: Boardman et al. (1995); SAM: Kruse et al. (1993); NDVI: Rouse et al. (1974); flowers in Brassica canopies: Sulik and Long (2016); erosion: Soille (2003); accuracy assessment: Congalton (1991); soil and background removal before disease features: Guo et al. (2021), Feng et al. (2022).')
exec(EQS_PRE)
STEP('P7', 'Plot and subplot polygons',
     'Each sample must cover exactly the scored subplot and nothing else.',
     'Field layout, plot numbers, aligned images.',
     '192 subplot polygons with codes → P8.',
     ['Digitise the 48 plot polygons once on the reference date and add the plot number.', 'Split each plot into four quadrant subplots that match the field scoring; apply an inner buffer to exclude border rows and bunds.', 'Use the same polygons on all dates and all sensors.'],
     'Fixed polygons ensure that the same ground area is followed over time and across sensors, and the inner buffer removes edge effects and grass on bunds.',
     'Plot-level polygons after soil masking were used by Liu et al. (2024) and Feng et al. (2022); Ma et al. (2026) used fixed small regions at flagged spots, which is the same principle at a smaller scale.')
STEP('P8', 'Subplot values',
     'Models need one value per feature and subplot; thermal values change with weather from date to date.',
     'Masked, resampled layers of all sensors; subplot polygons; air temperature of each flight.',
     'One table per date and sensor (192 rows): mean reflectance per band, RGB texture, thermal statistics, pixel count, flower % and canopy cover % → feature extraction (Chapter 4).',
     ['Multiply each layer by the vegetation mask and compute the mean of the masked pixels in each subplot for every band; save the pixel count.', 'Compute RGB texture at native resolution within the mask, then aggregate per subplot.', 'Thermal: save the canopy temperature statistics and normalise them by air temperature and by the healthy plots of the same date and variety.', 'Save flower % and canopy cover % from the SAM classes as covariates.'],
     'The subplot mean of vegetation pixels is the spectrum that corresponds to the canopy score. Normalising thermal data removes the date and weather effect that would otherwise dominate canopy temperature.',
     'Plot-mean spectra after masking: Guo et al. (2021), Mustafa et al. (2023); thermal normalisation by air temperature and healthy references: Oerke et al. (2006), Jones et al. (2009), Elsayed et al. (2017).')


H2('Pre-processing of each sensor at a glance')
TAB('presensor', [['Step', 'Hyperspectral', 'Multispectral', 'RGB', 'Thermal'],
 ['P1 Calibration', 'panels → reflectance', 'panels + sunlight sensor → reflectance', 'fixed exposure; digital numbers', 'emissivity 0.98, air T, RH → °C'],
 ['P2 Mosaic', 'georectified push-broom cube', 'orthomosaic', 'orthomosaic', 'orthomosaic'],
 ['P3 Quality', '613 → 483 bands; segment-wise smoothing', 'band alignment check', '—', 'warm-up and drift check'],
 ['P4 Registration', 'reference image', 'to HS, RMSE < 1 pixel', 'to HS, RMSE < 1 pixel', 'to HS with markers'],
 ['P5 Resampling', 'reference grid (2.2 cm)', 'bilinear', 'pixel aggregate; texture before resampling', 'nearest neighbour'],
 ['P6 Mask', 'made here (hourglass + SAM)', 'HS mask applied', 'HS mask applied', 'HS mask + extra edge check'],
 ['P7 Polygons', '192 subplots', 'same', 'same', 'same'],
 ['P8 Values', 'mean per band', 'mean per band', 'colour means, texture', 'statistics, normalised temperatures']],
 'Pre-processing applied to each sensor.', [1700, 2000, 1900, 1900, 1806], 15)
# =====================================================================================
H1('4. Feature extraction (all sensors)')
P('Features are calculated for every subplot-date and grouped by type. Grouping matters: selection is later done group by group so that small groups (thermal, texture) are not swamped by hundreds of spectral bands (Ghamisi et al., 2019).')
FIG('features', 'f4_features.png', 'Feature groups of each sensor and the covariates that are recorded but not used as disease features.', 540)
STEP('F1', 'Hyperspectral features',
     'Raw reflectance alone does not show red-edge shifts and absorption features clearly.',
     'Subplot mean reflectance (483 bands) of each date.',
     'Hyperspectral feature groups → Objective 1 and the selection stages.',
     ['Reflectance (R) of the 483 bands.', 'First (FD) and second (SD) derivatives from the Savitzky–Golay fit of each segment; derivative bands within 10 nm of a gap are not used.', 'Red-edge parameters: red-edge position (REP), amplitude (Dr) and the second-derivative amplitude.', '48 vegetation indices in five groups: pigment (e.g. PRI, ARI, CARI, MCARI, TCARI/OSAVI, PSRI), structure (e.g. NDVI, OSAVI, MSR), red edge (NDRE, MTCI, CIrededge), water (NDWI, MSI, NDII) and disease indices (DWSI, RBI); each formula is checked against the original paper.', 'The White Rust Index and two-band normalised-difference indices are searched in Objective 1 and inside the training folds (Chapter 6, step O1-4).'],
     'Derivatives remove the additive background and sharpen absorption features; red-edge parameters summarise chlorophyll loss; published indices encode known physiology and are easier to transfer to other sensors.',
     'Derivative analysis: Tsai and Philpot (1998); red edge: Horler et al. (1983), Filella and Peñuelas (1994); pigment indices: Gamon et al. (1992), Gitelson et al. (2003), Merzlyak et al. (1999), Haboudane et al. (2002); water and disease indices: Gao (1996), Hunt and Rock (1989), Hardisky et al. (1983), Apan et al. (2004); index groups for disease detection: Mahlein et al. (2013), Huang et al. (2014), Ma et al. (2026).')
STEP('F2', 'Multispectral features',
     'Five broad bands carry less information than the hyperspectral cube but are cheaper and closer to satellite bands.',
     'Subplot means of the five MicaSense bands.',
     'Multispectral feature groups → selection.',
     ['Five band reflectances (475, 560, 668, 717, 840 nm).', 'Twelve vegetation indices: NDVI, GNDVI, NDRE, CIgreen, CIrededge, MTCI, OSAVI, TCARI/OSAVI, MSR, PSRI, SAVI and the red-edge ratio.', 'All ten two-band normalised differences of the five bands.', 'GLCM texture (eight statistics) of each band, computed within the mask.'],
     'Red-edge and chlorophyll indices from multispectral cameras track chlorophyll loss and were the most consistent powdery-mildew indicators; texture adds canopy heterogeneity caused by pustules and chlorotic patches.',
     'Gitelson et al. (1996, 2003); Dash and Curran (2004); Rondeaux et al. (1996); Haboudane et al. (2002); Merzlyak et al. (1999); multispectral indices and texture for wheat powdery mildew: Liu et al. (2024); texture: Haralick et al. (1973).')
STEP('F3', 'RGB features',
     'RGB images carry colour and fine texture but no near-infrared information.',
     'RGB orthomosaic at native resolution with the vegetation mask.',
     'RGB feature groups → selection.',
     ['Colour indices: excess green (ExG), excess red (ExR), ExG − ExR, VARI, GLI and NGRDI; mean hue, saturation and value.', 'GLCM texture of R, G and B (mean, variance, homogeneity, contrast, dissimilarity, entropy, second moment, correlation), four directions averaged, computed at native resolution.', 'Canopy cover (fraction of vegetation pixels) as a covariate.'],
     'White pustules and chlorosis change canopy colour and make the canopy surface rougher, which texture measures capture; texture features were as strongly related to severity as the best vegetation indices in rice blast and wheat powdery mildew.',
     'Woebbecke et al. (1995); Meyer and Neto (2008); Gitelson et al. (2002); Louhaichi et al. (2001); Tucker (1979); Haralick et al. (1973); RGB texture in disease fusion: Feng et al. (2022), Guo et al. (2021), Ma et al. (2026).')
STEP('F4', 'Thermal features',
     'Infection changes transpiration and canopy temperature, but temperature also changes with weather and time.',
     'Masked thermal subplot values, air temperature and the healthy-plot temperatures of the same date.',
     'Thermal feature group → selection.',
     ['Canopy temperature (CT): mean, median, standard deviation, 10th and 90th percentiles.', 'Canopy minus air temperature (CTD = CT − Tair) and the ratio CTR = CT / Tair (in kelvin).', 'Normalised relative canopy temperature NRCT = (CT − CTmin) / (CTmax − CTmin) over the field on that date.', 'Difference from healthy plots of the same date and variety (ΔT).', 'Crop water stress index (CWSI) with wet and dry references from the field, and GLCM texture of the temperature image.'],
     'Normalised temperatures remove most of the weather effect and are the thermal parameters most often linked to disease severity; ΔT to healthy plots of the same variety removes variety and stage effects.',
     'Idso et al. (1981); Jones et al. (2009); Elsayed et al. (2017); thermal parameters for wheat powdery mildew: Feng et al. (2022), Liu et al. (2024); leaf temperature and environmental effects in downy mildew: Oerke et al. (2006).')
TAB('featcount', [['Sensor', 'Feature groups', 'Approximate number'], ['Hyperspectral', 'R, FD, SD, red edge, 48 indices (+ searched indices)', '≈ 1500'], ['Multispectral', '5 bands, 12 indices, 10 NDSI, 40 texture', '≈ 67'], ['RGB', 'colour indices, HSV, 24 texture', '≈ 33'], ['Thermal', 'temperature statistics, normalised temperatures, CWSI, texture', '≈ 18'],
    ['Covariates', 'flower %, canopy cover %, days after inoculation, variety, inoculation timing', 'not disease features']], 'Feature groups and their approximate sizes before selection.', [2000, 5000, 2306])
NOTE('Why the groups are not simply pooled: about 1600 candidate features against about 1000 training samples per fold would make selection unstable (Hughes, 1968; Guyon and Elisseeff, 2003), many features would be near-duplicates (Dormann et al., 2013), and random-forest importance and ReliefF both favour large groups of correlated features (Strobl et al., 2007; Robnik-Šikonja and Kononenko, 2003). The staged selection in Chapter 5 (staged feature selection) avoids these problems.')


INDEX_TABLES()
H2('The feature table')
P('All later steps read the same table layout, one table per sensor, joined by the identifier columns for fusion. Keeping one row per subplot-date and the same identifiers for all sensors makes the 15 sensor sets simple joins of these tables.')
TAB('schema', [['Column block', 'Columns', 'Used for'], ['Identifiers', 'date, DAI, plot, subplot, replication, treatment, variety, inoculation timing, fold', 'joining sensors; validation folds; treatment-wise results'],
 ['Labels', 'severity score, severity class, healthy/diseased; for Objective 3: infected/healthy and later score', 'model targets'], ['Covariates', 'flower %, canopy cover %, vegetation pixel count', 'checks of confounding; quality flags'],
 ['Features', 'all features of the sensor, grouped (prefix R_, FD_, SD_, VI_, TX_, TH_)', 'selection and models']], 'Layout of the feature table of each sensor.', [1800, 4600, 2906])
# =====================================================================================
H1('5. Validation framework and feature-selection stages (common to Objectives 2 and 3)')
STEP('V1', 'Sampling unit and outer validation folds',
     'Subplots of one plot, and plots of one replication, are not independent; random splits would test the model on samples very similar to the training samples.',
     'Labelled subplot tables of all dates.',
     'Three outer folds → all models of Objectives 2 and 3.',
     ['Use leave-one-replication-out (LORO) folds: fold 1 tests replication R1, fold 2 tests R2, fold 3 tests R3.', 'The 12 healthy plots are divided by variety (V1 → fold 1, V2 → fold 2, V3 → fold 3) so that every test fold contains healthy samples.', 'All dates of a plot and all four subplots stay in the same fold; each test fold has about 512 post-symptomatic (or 192 pre-symptomatic) samples.', 'The same three folds are used for every sensor set, task and model.'],
     'Blocked (grouped) cross-validation gives realistic accuracy when data have spatial or hierarchical structure; testing on a whole replication is the closest available test to new plots.',
     'Roberts et al. (2017); plot-grouped validation in disease sensing: Tian et al. (2021), Mustafa et al. (2023); the random sample split of Ma et al. (2026) is an example of the optimistic design this step avoids.')
FIG('validation', 'f5_validation.png', 'Leave-one-replication-out outer folds and the inner cross-validation used for selection and tuning.', 520)
STEP('V2', 'Nested inner cross-validation',
     'Feature selection and tuning on all data, or on the test fold, give over-optimistic accuracy.',
     'Training part of each outer fold.',
     'Selected features, tuned hyper-parameters and early-stopping epochs for each outer fold → model training.',
     ['Inside the training replications, use a 3-fold cross-validation grouped by plot.', 'Run Stage 2–4 of the feature selection, the index search, hyper-parameter tuning and deep-learning early stopping inside this inner loop only.', 'Train the final model of the fold on the whole training part and predict the test replication once.'],
     'When selection is not nested, cross-validated error is optimistically biased; nested cross-validation gives an almost unbiased estimate.',
     'Ambroise and McLachlan (2002); Varma and Simon (2006); nested ML-SFFS for rice blast: Tian et al. (2021).')
H2('Staged feature selection')
P('Selection is done in stages and group by group, and the same procedure is used for every sensor (Figure [[F:selection]]). Stages 1 and 3 do not use labels; Stages 2 and 4 use labels and therefore run inside the training folds (Ambroise and McLachlan, 2002; Varma and Simon, 2006). This is the approach recommended for multi-sensor UAV disease data, and the same group-wise logic (bands, indices and texture selected separately, then fused) was used for rice blast by Ma et al. (2026).')
FIG('selection', 'f6_selection.png', 'Staged feature selection for one sensor inside each training fold, and the fusion step for sensor combinations.', 540)
STEP('S1', 'Stage 1: redundancy within each group (no labels)',
     'Neighbouring bands, derivatives and many indices are almost identical, which wastes the later selection on duplicates.',
     'Feature groups of one sensor (training part).',
     'Thinned groups → Stage 2.',
     ['Remove near-constant features.', 'Within each group, form clusters of features with |r| ≥ 0.95 and keep one representative per cluster; for bands, this is one band per correlated spectral region.'],
     'Neighbouring hyperspectral bands are almost perfectly correlated; one band per region keeps the information and makes the selection stable.',
     'Mahlein et al. (2013) used a minimum band distance because of this correlation; one feature per common region: Tian et al. (2021); correlation clustering before selection: Dormann et al. (2013).')
STEP('S2', 'Stage 2: relevance within each group (labels, training folds only)',
     'Most features carry little disease information; each group needs a method suited to its nature.',
     'Thinned groups and training labels.',
     '5–10 relevant features per group → Stage 3.',
     ['Hyperspectral bands and derivatives: correlation scalogram (Pearson r with the severity score) for regression and ReliefF (severity classes, k = 10, neighbours from the same plot excluded) for classification; keep the top 5% and one band per region.', 'Vegetation indices (all sensors): Boruta with random forest (classification and regression separately).', 'Texture (MS, RGB, thermal): minimum-redundancy-maximum-relevance (mRMR), top 5–10.', 'Two-band indices and the White Rust Index: searched on the training plots only (Chapter 6, step O1-4).', 'Thermal: all thinned thermal features are kept (the group is small).'],
     'Correlation suits a continuous target; ReliefF detects features that separate overlapping classes; Boruta tests each feature against shuffled copies; mRMR balances relevance and redundancy for correlated texture features.',
     'Correlation scalogram: Shukla et al. (2024), Cheng et al. (2010); ReliefF: Robnik-Šikonja and Kononenko (2003), used by Mahlein et al. (2013) and Huang et al. (2014); Boruta: Kursa and Rudnicki (2010), used by Mustafa et al. (2023); mRMR: Peng et al. (2005), used for texture by Ma et al. (2026).')
STEP('S3', 'Stage 3: redundancy across groups (no labels)',
     'Survivors of different groups can still be strongly correlated (for example a red-edge band and a red-edge index).',
     'Pooled Stage-2 survivors of one sensor.',
     'Sensor disease-specific feature set (DSF set, about 10–25 features) → fusion and Stage 4.',
     ['Pool the survivors of all groups of the sensor.', 'Remove features iteratively until every variance inflation factor (VIF) is below 10.'],
     'Collinearity makes model coefficients and importance unstable; VIF < 10 is the usual threshold.',
     'Dormann et al. (2013); VIF < 10 before feature-combination search: Tian et al. (2021), Mustafa et al. (2023).')
exec(EQS_VIF)
STEP('S4', 'Fusion of sensor sets (combinations only)',
     'Combinations of sensors need one input vector per sample.',
     'DSF sets of the sensors in the combination.',
     'Fused feature pool → Stage 4.',
     ['Concatenate the DSF sets of the sensors in the combination (feature-level fusion).', 'Apply VIF < 10 again across sensors.', 'Standardise every feature with the mean and standard deviation of the training part.'],
     'Feature-level fusion keeps each sensor\'s features identifiable, so the contribution of each sensor can be assessed, and avoids the dimensionality of fusing raw data.',
     'Feature-level fusion of spectral, thermal and texture features: Feng et al. (2022), Liu et al. (2024); fusion levels: Ghamisi et al. (2019); input- and intermediate-level fusion: Maimaitijiang et al. (2020).')
STEP('S5', 'Stage 4: model-specific final selection',
     'Different models use features differently; a small final set improves generalisation and interpretation.',
     'Fused pool (or the DSF set of a single sensor).',
     'Optimum feature combination (OFC) of each machine-learning model; the whole pool for deep-learning models → model training.',
     ['Machine learning: sequential floating forward selection (ML-SFFS) wrapped around each model, criterion macro-F1 (classification) or RMSE (regression) in the inner cross-validation; at most 15 features; keep the smallest subset within 1% of the best score.', 'Deep learning: the fused pool is used directly, because the network learns its own feature weights; the attention layer of DNN-F2 shows which sensors it relies on.', 'Record how often each feature is selected over the three folds (selection stability).'],
     'SFFS finds a small set that suits each model and can remove previously added features; limiting the number of features keeps the ratio of samples to features high.',
     'Pudil et al. (1994); ML-SFFS for rice blast and Fusarium head blight: Tian et al. (2021), Mustafa et al. (2023); stability of selection: Nogueira et al. (2018), Meinshausen and Bühlmann (2010).')


H2('Leakage checklist and fold sizes')
TAB('leak', [['Step', 'Uses labels?', 'Where it is run'], ['Pre-processing, mask, feature extraction', 'no', 'once, on all data'], ['Stage 1 (correlation clusters)', 'no', 'training part of each outer fold'], ['Thermal and control normalisation', 'no (uses healthy plots)', 'training healthy plots for training data; same reference applied to test data'],
 ['Stage 2 (scalogram, ReliefF, Boruta, mRMR), index search', 'yes', 'inner folds only'], ['Stage 3 (VIF) and fusion', 'no', 'training part'], ['Stage 4 (SFFS), hyper-parameter tuning, early stopping', 'yes', 'inner folds only'], ['Final evaluation', 'yes', 'test replication, once']],
 'Where each step is run so that no information from the test replication enters the model.', [3900, 1700, 3706])
TAB('foldsize', [['Dataset', 'Training part per outer fold', 'Test part per outer fold', 'Inner folds'], ['Post-symptomatic (1536 per sensor)', '≈ 1024 samples (two replications + their healthy plots)', '≈ 512 samples', '3, grouped by plot'], ['Pre-symptomatic (576 per sensor)', '≈ 384 samples', '≈ 192 samples', '3, grouped by plot']],
 'Approximate sizes of the training and test parts.', [2600, 2800, 1900, 2006])
P('With about 1024 training samples and at most 15 selected features, every model keeps more than 60 samples per feature, well above the ratio at which the Hughes effect becomes important (Hughes, 1968; Guyon and Elisseeff, 2003). The pre-symptomatic models (≈ 384 training samples) are limited to 10 features.')
# =====================================================================================
H1('6. Objective 1: characterisation of white rust by each sensor')
P('Objective 1 describes what each sensor sees. It uses the 1536 post-symptomatic samples of each sensor and produces the disease-specific feature pools that are the scientific basis of Objectives 2 and 3. The steps below are run on all post-symptomatic samples for description and interpretation; for prediction, the same selection steps are repeated inside the training folds (Chapter 5, staged feature selection).')
TAB('o1steps', [['Step', 'Hyperspectral', 'Multispectral', 'RGB', 'Thermal'], ['O1-1 Response curves', 'mean spectra by class', 'band means by class', 'colour and texture by class', 'temperature by class'], ['O1-2 Redundancy', 'one band per region', 'clusters', 'clusters', 'clusters'],
    ['O1-3 Band screening', 'scalogram + ReliefF', '—', '—', '—'], ['O1-4 Index search', 'White Rust Index', '10 NDSI', '—', '—'], ['O1-5 Response test', 'ANOVA, Tukey, r', 'ANOVA, Tukey, r', 'ANOVA, Tukey, r', 'ANOVA, Tukey, r'],
    ['O1-6 DSF pools', 'Boruta', 'Boruta', 'Boruta', 'Boruta'], ['O1-7 Treatments and sensors', 'variety, timing, cross-sensor correlation', 'same', 'same', 'same']], 'Objective 1 steps for each sensor.', [2200, 1900, 1750, 1750, 1706])
STEP('O1-1', 'Response curves by severity, date and treatment',
     'Shows how each sensor responds to white rust before any selection, and whether the response depends on variety or crop age.',
     'Subplot feature tables (post-symptomatic).',
     'Response figures and a list of responsive regions → O1-2 to O1-5 (interpretation).',
     ['Plot the mean spectrum (hyperspectral), mean band values (multispectral), colour and texture means (RGB) and temperature values (thermal) for each severity class.', 'Repeat by variety (V1–V3) and inoculation timing (D1–D4), and over days after inoculation for each treatment.'],
     'Response curves show the physiological basis (visible rise from chlorophyll loss, red-edge shift, NIR fall from structural damage, SWIR rise from water loss, warmer canopy) and make later results interpretable.',
     'Spectral response of severity levels: Mahlein et al. (2013), Ma et al. (2026); red-edge and pigment changes under stress: Carter and Knapp (2001), Horler et al. (1983); temperature response to disease: Oerke et al. (2006).')
STEP('O1-2', 'Redundancy reduction within groups',
     'As Stage 1 (Chapter 5, staged feature selection), applied to all post-symptomatic samples of each sensor.',
     'Feature groups of each sensor.', 'Thinned groups → O1-3 to O1-6.',
     ['Remove near-constant features; keep one feature per correlation cluster (|r| ≥ 0.95); one band per correlated spectral region for the hyperspectral bands.'],
     'See Stage 1.', 'Mahlein et al. (2013); Tian et al. (2021); Dormann et al. (2013).')
STEP('O1-3', 'Band-level screening of the hyperspectral bands',
     'Finds which wavelengths respond to severity (regression) and which separate the classes (classification).',
     'Thinned R, FD and SD bands.',
     'Robust bands (found by both methods), regression-only and classification-only bands → O1-5, O1-6.',
     ['Correlation scalogram: Pearson r of every band of R, FD and SD with the severity score; candidates with p < 0.01 and the top 5% |r|.', 'ReliefF on the severity classes (k = 10, neighbours from the same plot excluded); candidates = top 5% of weights.', 'Keep one band per correlated region in each list; bands found by both lists (same region or within 10 nm) are robust white-rust bands.'],
     'The scalogram is the first step used for mustard aphid stress with ground hyperspectral data; ReliefF handles overlapping classes and was used to build disease indices.',
     'Shukla et al. (2024); Cheng et al. (2010); Robnik-Šikonja and Kononenko (2003); Mahlein et al. (2013); Huang et al. (2014).')
STEP('O1-4', 'White Rust Index and two-band index search',
     'General vegetation indices are not specific to white rust.',
     'Hyperspectral reflectance (450–2400 nm at 6 nm steps); multispectral bands.',
     'White Rust Index (WRI) formula and the best multispectral NDSI → O1-5, O1-6 and the feature groups of Objectives 2–3.',
     ['Search WRI = ND(λ1, λ2) + w × R(λ3), with w ∈ {−1, −0.5, 0, 0.5, 1}, ND bands at least 50 nm apart, using the ReliefF top 25% of bands and NDs.', 'Score each candidate by balanced accuracy (healthy vs diseased) with a plot-grouped cross-validation; keep the best formula.', 'For multispectral data, evaluate all ten normalised differences of the five bands.', 'Inside the training folds of Objectives 2–3 the search is repeated, so the test data never choose the formula.'],
     'A disease-specific index combines the most informative band difference with a band that carries additional information; it is simple, interpretable and transferable.',
     'Mahlein et al. (2013); optimised disease indices: Huang et al. (2014); two-band NDSI and RSI searches: Ma et al. (2026); new texture-fusion index: Ma et al. (2026).')
exec(EQS_IDX)
STEP('O1-5', 'Response test of features',
     'Shows which features differ among severity classes and how strongly they relate to the score.',
     'Indices, red-edge parameters, WRI, robust bands, texture and thermal features of each sensor.',
     'Ranked list of responding features per sensor → O1-6 and interpretation.',
     ['One-way ANOVA across severity classes with effect size η² and Tukey HSD groups.', 'Pearson r with the severity score.', 'p-values are used only to rank features, because subplots of a plot are related.'],
     'ANOVA and Tukey are the simplest way to show where classes differ and which classes overlap; correlation shows the strength of the relation with severity.',
     'Tukey (1949); response tests in disease studies: Mahlein et al. (2019), Feng et al. (2022), Liu et al. (2024); correlation of indices and texture with severity: Ma et al. (2026).')
STEP('O1-6', 'Disease-specific feature (DSF) pools with Boruta',
     'Produces the final list of features of each sensor that carry white-rust information.',
     'Robust bands, WRI, indices, red-edge parameters, texture and thermal features of each sensor.',
     'Eight DSF pools (4 sensors × classification and regression) → Objectives 2 and 3 (as candidate groups) and discussion.',
     ['Run Boruta (random forest, 500 trees, up to 100 iterations, p = 0.01) on each sensor, once with the severity classes and once with the score.', 'Report confirmed, tentative and rejected features.'],
     'Boruta keeps all relevant features (not only the strongest), which suits a characterisation objective.',
     'Kursa and Rudnicki (2010); Mustafa et al. (2023).')
STEP('O1-7', 'Response by treatment and complementarity of sensors',
     'Shows whether features behave the same in all varieties and inoculation timings, and which sensors carry different information.',
     'DSF pools and the subplot tables with treatment codes.',
     'Treatment-wise response figures and a cross-sensor correlation matrix → choice of sensor combinations and interpretation of Objective 2.',
     ['Plot the main DSFs against days after inoculation for each variety and inoculation timing.', 'Compute the correlation matrix between the DSFs of the four sensors (for example thermal ΔT with SWIR water indices).', 'Check that DSFs are not simply following flower % or canopy cover (correlation with the covariates).'],
     'Features that respond in all varieties are robust; low correlation between sensors indicates complementary information that fusion can exploit.',
     'Sensor complementarity: Mahlein et al. (2019), Maimaitijiang et al. (2020); flowering effects in Brassica: Sulik and Long (2016).')


H2('What each sensor is expected to show and what to report')
P('The expected responses below are hypotheses derived from plant physiology and the published studies; Objective 1 tests them with the field data.')
H3('Hyperspectral')
BL(['Expected: higher visible reflectance and lower red-edge slope from chlorophyll loss and chlorosis; a shift of the red-edge position to shorter wavelengths; lower NIR reflectance from mesophyll damage around pustules; higher SWIR reflectance from leaf water loss at higher severity (Horler et al., 1983; Carter and Knapp, 2001; Apan et al., 2004). The leaf-level ASD analysis of this study already pointed to red-edge derivatives and a VNIR index combining the NIR plateau, the 970 nm water shoulder and red-edge reflectance.',
    'Report: mean spectra and first derivatives by class; scalogram and ReliefF curves; robust band list; WRI formula with its balanced accuracy; top indices with ANOVA groups; Boruta pools.'])
H3('Multispectral')
BL(['Expected: the 717 nm red-edge and 840 nm NIR bands and red-edge indices (NDRE, CIrededge, MTCI) respond most; red-edge indices were the most consistent multispectral indicators of powdery mildew (Liu et al., 2024).', 'Report: band means by class; ranking of the 12 indices and 10 NDSI; texture response; Boruta pools; comparison of each MS index with its hyperspectral equivalent.'])
H3('RGB')
BL(['Expected: lower greenness (ExG, NGRDI, GLI) with chlorosis; brighter, whiter patches with pustules; higher texture contrast and entropy and lower homogeneity as the canopy surface becomes heterogeneous (Meyer and Neto, 2008; Ma et al., 2026).', 'Report: colour-index and texture responses by class; whether RGB features follow flower % (they should be checked at flowering).'])
H3('Thermal')
BL(['Expected: changes in canopy temperature relative to healthy plots and higher within-subplot temperature variability as infection disturbs transpiration; the direction must be established from the data because environmental conditions also change canopy temperature (Oerke et al., 2006; Jones et al., 2009).', 'Report: ΔT, CTD, NRCT and temperature SD by class and date; correlation of thermal features with SWIR water indices.'])
# =====================================================================================
H1('7. Objective 2: detection and severity discrimination with single sensors and sensor fusion')
P('Objective 2 builds and compares predictive models on the 1536 post-symptomatic samples of each sensor. Three tasks are modelled: (i) healthy vs diseased, (ii) severity classes and (iii) severity score. Every task is run for the 15 sensor sets with machine-learning and deep-learning models, using feature-level fusion for the combinations.')
FIG('combinations', 'f7_combinations.png', 'The 15 sensor sets: 4 single sensors and 11 combinations (6 pairs, 4 triples and all four).', 520)
TAB('sets', [['Set', 'Sensors', 'Type', 'Question it answers'], ['S1', 'HS', 'single', 'what the hyperspectral sensor alone achieves'], ['S2', 'MS', 'single', 'what a low-cost multispectral sensor achieves'], ['S3', 'RGB', 'single', 'what a consumer camera achieves'], ['S4', 'TIR', 'single', 'what canopy temperature alone achieves'],
    ['S5', 'HS + MS', 'pair', 'whether MS adds to HS'], ['S6', 'HS + RGB', 'pair', 'whether texture adds to spectra'], ['S7', 'HS + TIR', 'pair', 'whether temperature adds to spectra'], ['S8', 'MS + RGB', 'pair', 'low-cost optical pair'], ['S9', 'MS + TIR', 'pair', 'low-cost spectral + thermal pair'], ['S10', 'RGB + TIR', 'pair', 'cheapest pair'],
    ['S11', 'HS + MS + RGB', 'triple', 'all optical sensors'], ['S12', 'HS + MS + TIR', 'triple', 'spectral + thermal'], ['S13', 'HS + RGB + TIR', 'triple', 'hyperspectral + texture + thermal'], ['S14', 'MS + RGB + TIR', 'triple', 'all low-cost sensors'], ['S15', 'HS + MS + RGB + TIR', 'all', 'full multimodal system']],
    'The 15 sensor sets analysed in Objectives 2 and 3.', [900, 2400, 1100, 4906])
STEP('O2-1', 'Tasks, labels and class balance',
     'Defines the three prediction problems and handles unequal class sizes.',
     'Post-symptomatic dataset with labels (D4).',
     'Three labelled task datasets → model training.',
     ['Task A, detection: healthy (score 0) vs diseased (score > 0).', 'Task B, severity classes: grades 0, 1, 3, 5, 7, 9 (merged if a class has < 5% of samples).', 'Task C, regression: canopy severity score.', 'Unequal classes are handled with class weights in the loss (machine and deep learning); macro-averaged metrics are reported.'],
     'Detection, class discrimination and quantitative severity answer different practical questions (where, how bad, how much). Class weights avoid models that ignore small classes.',
     'Detection, severity classes and disease index regression were analysed together by Feng et al. (2022), Tian et al. (2021) and Abdulridha et al. (2023); macro-averaged metrics: Sokolova and Lapalme (2009).')
STEP('O2-2', 'Fold-wise feature selection and fusion for each sensor set',
     'Prepares the input features of each sensor set without using the test replication.',
     'Feature groups of each sensor; outer and inner folds.',
     'Optimum feature combinations (ML) and fused pools (DL) for each sensor set, fold and task → O2-3 and O2-4.',
     ['For each outer fold and task: run Stages 1–3 on each sensor (training part) to get its DSF set.', 'For a single-sensor set, the DSF set is the input; for a combination, concatenate the DSF sets and apply VIF < 10 again (feature-level fusion).', 'Run Stage 4 (ML-SFFS) separately for every machine-learning model.'],
     'Selecting inside the folds keeps the test replication independent; feature-level fusion allows the contribution of each sensor to be measured.',
     'Nested selection: Ambroise and McLachlan (2002), Varma and Simon (2006); group-wise selection followed by fusion: Ma et al. (2026); fusion: Feng et al. (2022), Liu et al. (2024).')
STEP('O2-3', 'Machine-learning models',
     'Different learners capture different relations between features and severity; comparing them avoids a model-specific conclusion.',
     'Optimum feature combination of each model, standardised with training statistics.',
     'Trained models and predictions on each test replication → O2-5.',
     ['Classification: support vector machine with RBF kernel (SVM), random forest (RF), extreme gradient boosting (XGBoost), k-nearest neighbours (k-NN) and partial least squares discriminant analysis (PLS-DA).', 'Regression: support vector regression (SVR), random forest regression (RFR), XGBoost regression, k-NN regression and partial least squares regression (PLSR).', 'Hyper-parameters are tuned by grid search in the inner cross-validation (Table [[T:mlgrid]]).'],
     'These models cover kernel, tree-ensemble, boosting, instance-based and latent-variable approaches and are the models most often used for crop-disease detection with spectral, thermal and texture features.',
     'SVM: Cortes and Vapnik (1995); RF: Breiman (2001); XGBoost: Chen and Guestrin (2016); k-NN: Cover and Hart (1967); PLS-DA: Barker and Rayens (2003); PLSR: Wold et al. (2001); disease applications: Tian et al. (2021) and Mustafa et al. (2023) (SVM, k-NN with SFFS), Feng et al. (2022) (PLSR, SVR, RFR), Abdulridha et al. (2023) and Liu et al. (2024) (RF).')
TAB('mlgrid', [['Model', 'Tasks', 'Hyper-parameters tuned (inner CV)'], ['SVM / SVR', 'A, B / C', 'C ∈ {0.1, 1, 10, 100}; γ ∈ {0.001, 0.01, 0.1, scale}; ε ∈ {0.1, 0.5} for SVR'], ['RF / RFR', 'A, B / C', '500 trees; features per split ∈ {√p, 0.3p}; minimum leaf size ∈ {1, 3, 5}'],
    ['XGBoost', 'A, B, C', 'trees ∈ {200, 500}; depth ∈ {3, 5}; learning rate ∈ {0.05, 0.1}; subsample 0.8'], ['k-NN', 'A, B, C', 'k ∈ {3, 5, 7, 9, 11}; uniform or distance weights'], ['PLS-DA / PLSR', 'A, B / C', 'number of latent variables 1–15']],
    'Machine-learning models and tuning grids.', [1800, 1300, 6206])
exec(MODELS)
STEP('O2-4', 'Deep-learning models with feature-level fusion',
     'Neural networks can learn non-linear interactions between features of different sensors and can weight sensors adaptively.',
     'Fused feature pool (or single-sensor DSF set), standardised.',
     'Trained networks and predictions on each test replication → O2-5.',
     ['DNN-F1 (input-level feature fusion): the features of all sensors in the set are concatenated and passed through two dense layers (64 and 32 units) with batch normalisation, ReLU and dropout (0.3), then the output layer.', 'DNN-F2 (intermediate feature fusion): each sensor has its own sub-network (one or two dense layers of 16–32 units); a squeeze-and-excitation (SE) attention block gives each sensor branch a learned weight; the weighted branches are concatenated and passed to a dense layer of 32 units and the output layer. For single-sensor sets only DNN-F1 is used.', 'Outputs: sigmoid (Task A), softmax (Task B) or linear (Task C); losses: weighted cross-entropy or mean squared error.', 'Training: Adam optimiser (learning rate 0.001, weight decay 10⁻⁴), batch size 32, up to 500 epochs with early stopping (patience 30) on an inner validation split; five random seeds, predictions averaged.'],
     'With about 1000 training samples per fold, small fully connected networks are appropriate; very deep or transformer networks need much more data. DNN-F2 lets each sensor be processed separately before fusion and was better than input fusion in multi-sensor UAV data; the SE block learns how much each sensor contributes, an idea also used in DT-EDNet.',
     'DNN-F1 and DNN-F2 for RGB, multispectral and thermal fusion: Maimaitijiang et al. (2020); squeeze-and-excitation: Hu et al. (2018), used in DT-EDNet by Ma et al. (2026); deep learning: LeCun et al. (2015); Adam: Kingma and Ba (2015); dropout: Srivastava et al. (2014); batch normalisation: Ioffe and Szegedy (2015).',
     note='Ma et al. (2026) noted that about 2000 training samples is small for a transformer. This methodology therefore uses compact networks and compares them with machine-learning models on exactly the same folds.')
FIG('dl', 'f8_dl.png', 'Deep-learning models with feature-level fusion: DNN-F1 (input-level) and DNN-F2 (intermediate level with sensor attention).', 540)
STEP('O2-5', 'Evaluation metrics',
     'Accuracy must be measured in a way that reflects ordered classes, unequal class sizes and continuous severity.',
     'Predictions on the three test replications (pooled over folds).',
     'Metric tables for each sensor set, model and task → O2-6.',
     ['Task A: overall accuracy, sensitivity, specificity, F1, area under the ROC curve.', 'Task B: overall accuracy, Cohen\'s kappa and quadratic-weighted kappa (ordered classes), per-class F1, macro-F1, confusion matrix and the share of predictions within one class of the true class.', 'Task C: coefficient of determination (R²), root-mean-square error (RMSE), normalised RMSE and ratio of performance to deviation (RPD).', 'Report every metric also by variety, inoculation timing and date.'],
     'Macro-F1 gives equal weight to small classes; weighted kappa credits near-misses between ordered classes; RPD relates the error to the spread of the data.',
     'Cohen (1960, 1968); Sokolova and Lapalme (2009); Fawcett (2006); Chang et al. (2001); metrics in disease studies: Feng et al. (2022), Ma et al. (2026).')
exec(EQS_MET)
STEP('O2-6', 'Comparison of sensor sets and models, and contribution of each sensor',
     'Identifies the best sensor set and model and quantifies what each sensor adds.',
     'Metric tables of the 15 sets × models × tasks.',
     'Best sensor set and model for each task; contribution of each sensor → conclusions and O2-7.',
     ['Rank the 15 sets by macro-F1 (Task B), AUC (Task A) and RMSE (Task C) for each model; compare the best machine-learning and best deep-learning model.', 'Gain of fusion = metric of a combination minus the metric of its best single sensor.', 'Ablation: remove one sensor at a time from S15 and record the drop.', 'Report the selection frequency of every feature over the folds; final feature lists contain features selected in at least two of three folds.', 'Explain the best models with SHAP values (mean absolute SHAP per feature and per sensor).'],
     'Ablation and fusion gain answer directly whether a sensor is worth flying; SHAP gives consistent, model-agnostic feature importance.',
     'Ablation of feature groups and modules: Ma et al. (2026); SHAP: Lundberg and Lee (2017), used for band selection by Ma et al. (2026); fusion gain over single sensors: Feng et al. (2022), Maimaitijiang et al. (2020).')
STEP('O2-7', 'Severity maps',
     'Field managers need maps rather than tables.',
     'Best model of each task; subplot features of every date.',
     'Subplot-level maps of detection, severity class and severity score for each date → reporting.',
     ['Apply the best model of each task to all subplots of every date (models trained on all training folds).', 'Map the predicted class and score at subplot level, together with the absolute error where scores are available.'],
     'Maps show the spatial and temporal development of the disease and the agreement with field scores.',
     'Severity maps from UAV models: Abdulridha et al. (2023), Liu et al. (2024), Deng et al. (2024).')


STEP('O2-8', 'Treatment-wise performance and robustness',
     'A model may work for one variety or crop age and fail for another; treatments must be considered in the evaluation.',
     'Test predictions with variety, inoculation timing and date codes.',
     'Performance by treatment and transfer results → conclusions on robustness.',
     ['Report all metrics separately for each variety (V1–V3), each inoculation timing (D1–D4) and each date.', 'Leave-one-variety-out test: train on two varieties and test on the third (mainly V1 ↔ V2, because the resistant variety has few diseased samples).', 'Leave-one-inoculation-timing-out test: train on three timings and test on the fourth, to check transfer across crop ages.', 'Use these tests for the best ML and best DL model of the best three sensor sets only, to limit computation.'],
     'Blocked tests that leave out a whole group show whether a model extrapolates to new conditions; treatment-wise results show whether the selected features are variety-specific.',
     'Blocked cross-validation for extrapolation: Roberts et al. (2017); performance by variety and growth stage: Liu et al. (2024), Feng et al. (2022); independent-site testing: Ma et al. (2026).')

H2('Specification of the 15 sensor sets')
P('For every set the input is the union of the fold-wise DSF sets of its sensors (Stage 3), reduced again by VIF < 10; machine-learning models then select their own subset by ML-SFFS, and the deep-learning models use the fused pool. DNN-F2 is used whenever the set contains two or more sensors. The paragraphs below state what each set is expected to contribute and what comparison it answers.')
for s_, t_ in [('S1 – hyperspectral alone', 'Input: robust bands, derivatives, red-edge parameters, indices and the WRI. Expected to be the strongest single sensor because it covers pigment, structure and water features; it sets the reference against which all fusion gains are judged (Feng et al., 2022; Ma et al., 2026). Models: all ML models and DNN-F1.'),
 ('S2 – multispectral alone', 'Input: five bands, red-edge and chlorophyll indices, NDSI and texture. Answers whether a low-cost, satellite-like sensor captures most of the hyperspectral information; compare its best index with the WRI and with S1 (Liu et al., 2024).'),
 ('S3 – RGB alone', 'Input: colour indices and texture. Tests whether a consumer camera is sufficient for visible symptoms; expected to be weaker at low severity, where colour change is small (Guo et al., 2021; Ma et al., 2026).'),
 ('S4 – thermal alone', 'Input: normalised temperature features and thermal texture. Tests the physiological (transpiration) signal on its own; expected to be weaker for severity classes but potentially useful for early change (Mahlein et al., 2019; Liu et al., 2024).'),
 ('S5 – HS + MS', 'Tests whether multispectral texture and bands add anything to the hyperspectral spectrum; a small gain is expected because the spectral information overlaps, which shows whether the cheaper MS sensor can replace HS.'),
 ('S6 – HS + RGB', 'Combines detailed spectra with high-resolution canopy texture; tests the spectral + texture fusion found useful for powdery mildew and rice blast (Feng et al., 2022; Ma et al., 2026).'),
 ('S7 – HS + TIR', 'Combines spectral (pigment, structure, water) and thermal (transpiration) information; tests the hyperspectral + thermal fusion that improved Fusarium head blight detection (Mahlein et al., 2019).'),
 ('S8 – MS + RGB', 'An all-optical low-cost pair: red-edge spectra plus fine texture.'),
 ('S9 – MS + TIR', 'Low-cost spectral + thermal pair, the combination used for powdery mildew severity by Liu et al. (2024); a practical candidate for routine monitoring.'),
 ('S10 – RGB + TIR', 'The cheapest pair; shows how far colour, texture and temperature go without narrow bands.'),
 ('S11 – HS + MS + RGB', 'All optical sensors; tests whether thermal is needed at all.'),
 ('S12 – HS + MS + TIR', 'All spectral sensors with thermal; tests whether RGB texture is needed.'),
 ('S13 – HS + RGB + TIR', 'Hyperspectral, texture and thermal: the three types of information that Feng et al. (2022) fused; tests whether MS is redundant when HS is present.'),
 ('S14 – MS + RGB + TIR', 'All low-cost sensors; the main practical alternative to a hyperspectral system.'),
 ('S15 – all four sensors', 'The full multimodal system; used for the drop-one-sensor ablation that measures the contribution of each sensor.')]:
    P('**' + s_ + '.** ' + t_)

H2('Result tables to be produced')
TAB('templateA', [['Sensor set', 'Best ML model', 'Macro-F1', 'Weighted kappa', 'Best DL model', 'Macro-F1', 'Weighted kappa'], ['S1 HS', '…', '…', '…', '…', '…', '…'], ['S2 MS', '…', '…', '…', '…', '…', '…'], ['…', '…', '…', '…', '…', '…', '…'], ['S15 all', '…', '…', '…', '…', '…', '…']],
 'Template: severity-class results of the 15 sensor sets (one table each for Tasks A, B and C).', [1600, 1500, 1100, 1300, 1500, 1100, 1206])
TAB('templateB', [['Removed sensor (from S15)', 'Macro-F1 without it', 'Change', 'R² without it', 'Change'], ['HS', '…', '…', '…', '…'], ['MS', '…', '…', '…', '…'], ['RGB', '…', '…', '…', '…'], ['TIR', '…', '…', '…', '…']],
 'Template: drop-one-sensor ablation.', [2600, 1800, 1200, 1800, 1906])
# =====================================================================================
H1('8. Objective 3: prediction at the pre-symptomatic stage')
P('Objective 3 uses the 576 pre-symptomatic samples of each sensor. The question is whether subplots that will develop white rust can be separated from healthy subplots before pustules are visible, and whether their later severity can be predicted. The same 15 sensor sets and the same model families are used, with steps adapted to the weak early signal.')
FIG('obj3', 'f9_obj3.png', 'Pre-symptomatic and post-symptomatic periods and how pre-symptomatic samples are labelled from the later status of the same subplot.', 520)
STEP('O3-1', 'Pre-symptomatic samples and labels',
     'Before symptoms, the visual score is zero everywhere; labels must come from what happens later.',
     'Pre-symptomatic subplot tables; scores of the first post-symptomatic date.',
     'Labelled pre-symptomatic dataset → O3-2.',
     ['Classification: healthy = subplots of the 12 healthy plots; infected = inoculated subplots that show pustules later. Inoculated subplots that never develop symptoms are excluded from the infected class.', 'Regression: target = severity score of the same subplot on the first post-symptomatic date.', 'Record days after inoculation (DAI) for every sample.'],
     'Retrospective labelling separates truly infected from escaped plants; predicting the later score turns early detection into a forecast of severity.',
     'Retrospective labels for pre-symptomatic detection: Zhu et al. (2017), Tian et al. (2021); pre-symptomatic stages in fusion models: Yu et al. (2025); earliest detection days by sensor: Mahlein et al. (2019).')
STEP('O3-2', 'Normalisation to healthy plots of the same date and variety',
     'Early disease changes are small compared with differences caused by date, weather, variety and crop age.',
     'Pre-symptomatic features; healthy-plot features of the same date and variety.',
     'Control-normalised features → O3-3.',
     ['For every feature and date, subtract the mean of the healthy plots of the same variety (and divide by their standard deviation).', 'Healthy plots of the same treatment are used when available, so that crop age is matched.', 'Within each training fold, the normalisation uses only healthy plots of the training replications and of the same date.'],
     'Normalisation against healthy references removes most date and variety effects and was essential for thermal disease detection, where weather changes leaf temperature as much as infection does.',
     'Oerke et al. (2006); Jones et al. (2009); healthy references in early detection: Zhu et al. (2017), Zarco-Tejada et al. (2018).')
STEP('O3-3', 'Pre-symptomatic feature screening and selection',
     'Features that respond after symptoms are not necessarily the earliest responders.',
     'Control-normalised feature groups.',
     'Pre-symptomatic DSF sets of each sensor (fold-wise) → O3-4.',
     ['Screen each feature with the difference between infected and healthy samples (t-test and % difference) on each date, for description.', 'Inside the training folds, run the staged selection (Chapter 5, staged feature selection) with the pre-symptomatic labels: Stage 1, Stage 2 (Boruta for all groups because classes are binary; correlation with the later score for regression), Stage 3 VIF < 10, fusion for combinations, Stage 4 ML-SFFS.'],
     'The same staged procedure keeps the methods comparable with Objective 2, while the pre-symptomatic labels allow different, earlier features to be found.',
     'Pre-symptomatic disease-specific features with SFFS: Tian et al. (2021); Boruta: Kursa and Rudnicki (2010), Mustafa et al. (2023); early spectral changes in rust and mildew: Terentev et al. (2023), Zhu et al. (2017).')
STEP('O3-4', 'Pre-symptomatic models for the 15 sensor sets',
     'Detection must be tested for each sensor and combination.',
     'Pre-symptomatic optimum feature sets (ML) and fused pools (DL).',
     'Trained pre-symptomatic models and test predictions → O3-5.',
     ['Classification: SVM, RF, XGBoost, k-NN and PLS-DA; regression: SVR, RFR, XGBoost, k-NN and PLSR; same tuning grids as Objective 2.', 'Deep learning: DNN-F1 and DNN-F2 with smaller layers (32 and 16 units) and stronger dropout (0.4), because only about 384 samples are available for training in each fold.', 'Same LORO folds as Objective 2.'],
     'The same models allow a fair comparison between the pre- and post-symptomatic stages; smaller networks limit overfitting on the smaller dataset.',
     'Pre-symptomatic classification with SVM and related models: Zhu et al. (2017), Tian et al. (2021); dual-branch deep fusion for pre-symptomatic rice sheath blight: Yu et al. (2025); network regularisation: Srivastava et al. (2014).')
STEP('O3-5', 'Evaluation, earliest detection day and risk maps',
     'Shows how early, with which sensor set and with what reliability white rust can be predicted.',
     'Test predictions of all models and sensor sets with DAI.',
     'Pre-symptomatic accuracy tables, earliest detection day per sensor set, risk maps → conclusions.',
     ['Classification: sensitivity, specificity, balanced accuracy and AUC; regression: R² and RMSE of the later score.', 'Earliest detection day: compute balanced accuracy separately for each pre-symptomatic date (DAI) and take the first date on which it exceeds a chosen level (for example 0.70) for each sensor set.', 'Map the predicted infection probability of every subplot on each pre-symptomatic date (risk maps).'],
     'Sensitivity and specificity matter more than overall accuracy for an early warning; the accuracy-by-DAI curve shows when detection becomes reliable and which sensor responds first.',
     'Fawcett (2006); earliest detection days of hyperspectral, thermal and fluorescence sensors: Mahlein et al. (2019); pre-symptomatic maps for early warning: Zarco-Tejada et al. (2018), Yu et al. (2025).')


H2('Sensor-specific expectations at the pre-symptomatic stage')
BL(['Hyperspectral: small red-edge and pigment-index changes may appear before pustules, as reported for wheat leaf rust and tobacco mosaic virus (Terentev et al., 2023; Zhu et al., 2017).', 'Thermal: transpiration changes can precede visible symptoms; thermal imaging detected Fusarium head blight later than hyperspectral imaging in one study but added to fusion (Mahlein et al., 2019), so its value is tested here.', 'Multispectral: the red-edge band may carry part of the hyperspectral early signal.', 'RGB: colour and texture are expected to respond only after visible symptoms; RGB-only sets serve as a negative control for the pre-symptomatic stage.', 'Treatments: inoculation timing changes crop age at infection; earliest detection days are therefore reported separately for each inoculation timing and variety.'])
# =====================================================================================
H1('9. How the steps fulfil the three objectives')
TAB('fulfil', [['Objective', 'Steps', 'Evidence produced'], ['1. Characterisation', 'P1–P8, F1–F4, O1-1 to O1-7', 'response curves; robust bands; White Rust Index; DSF pools of each sensor; response by variety and inoculation timing; complementarity of sensors'],
    ['2. Detection and severity discrimination by fusion', 'V1–V2, S1–S5, O2-1 to O2-7', 'accuracy of 15 sensor sets × ML and DL models for detection, classes and regression; fusion gain; ablation; SHAP; maps'],
    ['3. Pre-symptomatic prediction', 'O3-1 to O3-5 (with V1–V2 and S1–S5)', 'pre-symptomatic accuracy of 15 sensor sets; earliest detection day; later-severity prediction; risk maps']], 'Link between steps and objectives.', [2600, 2700, 4006])
P('**What is new in this methodology.** (1) White rust of mustard is characterised with four UAV sensors measured on identical vegetation pixels; (2) a White Rust Index is derived and tested; (3) all 15 sensor sets are compared under one nested, plot-grouped design with both machine-learning and deep-learning feature-level fusion; (4) the contribution of each sensor is quantified by fusion gain, ablation and attention weights; (5) pre-symptomatic prediction is tested with retrospective labels, control normalisation and an earliest-detection analysis.')


H2('Input–output chain of all steps')
TAB('chain', [['Step', 'Input', 'Output (to next step)'], ['D1–D4', 'field design, scores', 'labelled subplot list; post- and pre-symptomatic datasets'], ['P1–P2', 'raw images, panels, GCPs', 'calibrated, georeferenced mosaics'], ['P3', 'HS cube', 'clean 483-band cube'], ['P4–P5', 'mosaics of all sensors', 'aligned layers on the HS grid'],
 ['P6', 'HS cube, training regions', 'vegetation mask'], ['P7–P8', 'masked layers, polygons', 'subplot tables per date and sensor'], ['F1–F4', 'subplot tables', 'feature groups per sensor'], ['V1–V2', 'labelled feature tables', 'outer and inner folds'],
 ['S1–S3', 'feature groups (training part)', 'sensor DSF sets'], ['S4', 'DSF sets of a combination', 'fused pool'], ['S5', 'fused pool', 'optimum feature combinations'], ['O1-1 to O1-7', 'post-symptomatic feature groups', 'DSF pools, WRI, response figures'],
 ['O2-1 to O2-8', 'fold-wise features, labels', 'models, metrics, best sensor set, contributions, maps'], ['O3-1 to O3-5', 'pre-symptomatic features, later labels', 'pre-symptomatic models, earliest detection day, risk maps']],
 'Input and output of every step.', [1700, 3700, 3906])
# =====================================================================================
H1('10. Six-month work plan')
FIG('gantt', 'f10_gantt.png', 'Six-month work plan for the analysis.', 540)
TAB('plan', [['Month', 'Work', 'Deliverable'], ['1', 'P1–P8 for all dates and sensors; mask accuracy; subplot tables', 'quality-checked subplot tables (4 sensors × all dates)'], ['2', 'F1–F4 feature extraction; O1-1 to O1-3', 'feature tables; response curves; band screening'],
    ['3', 'O1-4 to O1-7; validation folds; selection code tested', 'White Rust Index; DSF pools; Objective 1 chapter draft'], ['4', 'O2: single sensors S1–S4 (ML + DL, three tasks)', 'single-sensor results'], ['5', 'O2: 11 combinations, fusion gain, ablation, SHAP, maps; O3 started', 'fusion results; maps'],
    ['6', 'O3 models, earliest detection, risk maps; synthesis and writing', 'Objective 3 results; thesis chapters; two manuscripts']], 'Month-wise plan.', [1000, 5000, 3306])
NOTE('Computing load: 15 sensor sets × 3 tasks × 3 folds × 5 ML models with SFFS, plus two DL models × 5 seeds, for two datasets. Run the single-sensor selections once per fold and reuse them for all combinations; cache the subplot tables; run deep-learning training on a GPU.')

# =====================================================================================
H1('11. Software and reproducibility')
TAB('software', [['Task', 'Software'], ['Image processing, registration, resampling, masks', 'ENVI, ArcGIS or Python (GDAL, rasterio); hourglass notebook (MNF, PPI, n-D, SAM)'], ['Features, selection, ML models', 'Python: numpy, pandas, scikit-learn (Pedregosa et al., 2011), xgboost (Chen and Guestrin, 2016), BorutaPy, ReliefF, mlxtend SFFS (Raschka, 2018)'],
    ['Deep learning', 'PyTorch (Paszke et al., 2019)'], ['Interpretation', 'SHAP (Lundberg and Lee, 2017)']], 'Software used.', [3300, 6006])
BL(['Fix random seeds; store the outer and inner folds as files and reuse them for all sensor sets.', 'Log every setting (bands removed, mask threshold, selected features per fold, hyper-parameters).', 'Keep raw, intermediate and final tables separate and versioned.'])

# =====================================================================================
H1('12. Questions expected in the seminar')
for q, a in [('Why are the folds grouped by replication and not random?', 'Subplots of a plot and plots of a replication are similar; random splits put near-identical samples in training and test sets and inflate accuracy (Roberts et al., 2017). Testing on a whole replication is the closest test to new plots.'),
    ('Why select features in stages instead of using all features at once?', 'With about 1600 features and 1000 training samples, selection on one pool is unstable, keeps duplicates and lets large groups swamp small ones (Hughes, 1968; Guyon and Elisseeff, 2003; Dormann et al., 2013). Group-wise selection then pooling was also used by Ma et al. (2026).'),
    ('Why feature-level fusion only?', 'It keeps sensors identifiable, so each sensor\'s contribution can be measured, and it reduces dimensionality compared with fusing raw data (Ghamisi et al., 2019); both machine-learning and deep-learning versions are tested (Maimaitijiang et al., 2020).'),
    ('Why not a transformer such as DT-EDNet?', 'DT-EDNet was trained on about 2000 samples, which its own reviewers regard as small for a transformer (Ma et al., 2026). With about 1000 training samples per fold, compact DNNs are more appropriate; the SE attention idea is kept in DNN-F2.'),
    ('Why keep flowers in the subplot spectrum?', 'The canopy score includes the inflorescence and staghead; flower % is recorded and checked so that selected features are not only flowering effects (Sulik and Long, 2016).'),
    ('How is pre-symptomatic infection known if no symptoms are visible?', 'From the later status of the same subplot (retrospective labels); inoculated subplots that never develop symptoms are excluded (Zhu et al., 2017; Tian et al., 2021).'),
    ('How is the contribution of each sensor shown?', 'By fusion gain over the best single sensor, by removing one sensor at a time from the full set (ablation), by the attention weights of DNN-F2 and by SHAP values (Lundberg and Lee, 2017).')]:
    P('**Q. ' + q + '** ' + a)
open(B + 'mf_body.js', 'w').write('\n'.join(K)); print('body lines', len(K))
