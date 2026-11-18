"""Slide-by-slide guide (Word + PDF) to the full leaf-analysis deck: slide image, what it shows, method with references,
full tables and figures, output of the step and how to present it. Body JS is assembled by l7_assemble.py --slides."""
import json, os, re
B = os.path.dirname(os.path.abspath(__file__)) + '/'; D = B + 'data/'
DK = json.load(open(D + 'deck.json')); k = DK['k']
K = []
def esc(t):
    t = t.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    return re.sub(r'\[\[(T|F):(\w+)\]\]', lambda m: '${%s(\'%s\')}' % (m.group(1), m.group(2)), t)
def js(s): return '`' + esc(s) + '`'
def H1(t): K.append("K.push(H1(%s));" % js(t))
def H2(t): K.append("K.push(H2(%s));" % js(t))
def Pp(t): K.append("K.push(P(%s));" % js(t))
def BL(items): K.extend("K.push(BL(%s));" % js(i) for i in items)
def BOX(l, t, fill='FFF6E0', line='C98A00'): K.append("K.push(BOX(%s, %s, '%s', '%s'));" % (js(l), js(t), fill, line))
def NOTE(t): K.append("K.push(NOTE(%s));" % js(t))
def FIG(key, file, cap, w=540): K.append("K.push(...fig2('%s', '%s', %s, %d));" % (key, file, js(cap), w))
def TAB(key, rows, cap, size=16, widths=None):
    if widths is None:
        L = [min(max(max(len(str(r[j])) for r in rows), 4), 42) for j in range(len(rows[0]))]; s = sum(L); widths = [int(9306 * x / s) for x in L]
    R = '[' + ',\n'.join('[' + ', '.join(js(str(c)) for c in r) + ']' for r in rows) + ']'
    K.append("K.push(...tab2('%s', %s, %s, %s, %d));" % (key, R, json.dumps(widths), js(cap), size))

def SL(n, title, shows, explain, result, talk, figs=(), tabs=(), refs=None):
    H2('Slide %d. %s' % (n, title))
    FIG('s%02d' % n, 'slides/s-%02d.png' % n, 'Slide %d as presented: %s.' % (n, title), 470)
    Pp('**What the slide shows.** ' + shows)
    if isinstance(explain, str): Pp('**Explanation.** ' + explain)
    else: Pp('**Explanation.**'); BL(explain)
    if refs: Pp('**References for this step:** ' + refs)
    for key, rows, cap in tabs: TAB(key, rows, cap)
    for key, file, cap in figs: FIG(key, file, cap, 560)
    BOX('Output / result:', result)
    NOTE('**How to present it.** ' + talk)

nest = k['nest']
# ================= TITLE =================
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 900, after: 160 }, children: [new TextRun({ text: 'Leaf-level hyperspectral analysis of white rust in mustard', font: FONT, size: 40, bold: true, color: '1E3A1F' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: 'Slide-by-slide explanation of the methodology and results presentation, with all tables and figures', font: FONT, size: 26, color: '2C5F2D' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 500 }, children: [new TextRun({ text: 'Ph.D. (Agricultural Physics), ICAR-IARI  |  AI-based multimodal UAV sensing of white rust in mustard', font: FONT, size: 20, italics: true })] }));")
NOTE('**How to use this document.** Each section follows one slide of the presentation (Leaf_ASD_analysis_presentation_full.pptx). It shows the slide, explains what it shows, describes the method with its references (et al., year), gives the full tables and figures at readable size, states the output of the step and suggests what to say when presenting. Section-divider and reference slides are summarised; the full reference list is at the end.')
Pp('**Study in one paragraph.** %s ASD contact-probe leaf spectra (350–2500 nm) from 48 plots (12 controls, 36 inoculated) on four dates (11 February to 13 March 2026) were analysed with the proposed tier methodology. Objective 1 (Tiers 0–6) identified the wavelengths and indices that respond to white rust (Albugo candida): red-edge derivatives, a White Rust Index and SWIR water features. Objective 2 built nested, leave-one-replication-out models for six-grade leaf classification and plot-level PDI regression. All accuracies come from held-out replications.' % k['n_leaves'])

# ================= INTRODUCTION =================
H1('Part 1. Introduction')
SL(1, 'Title slide', 'The title of the study, the data (ASD leaf spectra, four dates, February–March 2026) and the two tasks: Objective 1 tiers and Objective 2 models for six-grade classification and plot PDI regression.',
   'The leaf-level analysis is the first, controlled step of the thesis. It applies the agreed methodology to leaf spectra before it is used on UAV canopy data (Mahlein, 2016).',
   'The scope of the talk: one dataset, one methodology, two tasks.', 'Open with the problem (white rust reduces mustard yield) and say that leaf spectra show the pure disease signal that the UAV analysis will look for.')
SL(2, 'Outline', 'Six parts: study and data; methodology flow with results; pre-processing and features; Objective 1 tiers; Objective 2 models; results and discussion.',
   'The talk follows the order of the methodology, so every result is shown directly after the step that produced it.', 'Road map of the presentation.', 'Keep it short; tell the audience that each step slide ends with an "Output" box.')
SL(3, 'Background and objectives of the leaf-level analysis', 'Why leaf spectra are analysed and what the two objectives are; four cards summarise Objective 1, Objective 2, the six grades and PDI.',
   ['White rust, caused by Albugo candida, produces white pustules, chlorosis and staghead in mustard (Saharan et al., 2014).',
    'Leaf spectra contain the disease signal without soil, shadow, flowers or illumination effects (Mahlein et al., 2012; Mahlein, 2016).',
    'They define which wavelengths and indices should be looked for in UAV and satellite data.',
    'Objective 1 asks which wavelengths and indices respond to white rust; Objective 2 asks how well six leaf grades (0, 1, 3, 5, 7, 9) and plot PDI can be predicted.'],
   'A complete, referenced chain from raw ASD spectra to disease-sensitive features and validated severity models.', 'State both objectives in one sentence each; mention that the same chain will be used for the UAV data.')

# ================= FLOW =================
H1('Part 2. Methodology flow with results')
Pp('Slide 4 is the section divider "Methodology flow with results: every step, its reference and its result". Slides 5–7 give the complete flow before the step-by-step slides.')
SL(5, 'Objective 1 flow: methods, references and results', 'Eight connected boxes (Tier 0 → pre-processing → Tier 1 → Tier 2 → Tier 3 → Tier 4 → Tier 5 → Tier 6). Each box gives the method, its reference and the key result (red arrow).',
   ['**Tier 0** — data and labels: %s leaves, %s plot-dates, PDI 0–%s%% (Conn et al., 1990; Wheeler, 1969).' % (k['n_leaves'], k['n_pd'], k['pdi_max']),
    '**Pre-processing** — splice correction, 400–2400 nm, water bands removed for band selection, Savitzky–Golay smoothing, derivatives: %s bands × R, FD, SD = 1047 features (Hueni and Bialek, 2017; Savitzky and Golay, 1964).' % k['n_bands'],
    '**Tier 1** — red-edge parameters and 48 indices (Horler et al., 1983; Apan et al., 2004).',
    '**Tier 2** — correlation scalogram + ReliefF: %s robust, %s regression-only and %s classification-only bands (Shukla et al., 2024; Robnik-Šikonja and Kononenko, 2003).' % (k['n_rob'], k['n_reg'], k['n_cls']),
    '**Tier 3** — White Rust Index search in VNIR, SWIR and the whole range: WRI = %s, balanced accuracy %s, r with PDI %s; the whole-range search gives the same bands (BA %s) (Mahlein et al., 2013).' % (k['wri'], k['wri_ba'], k['wri_r'], k['wf_ba']),
    '**Tier 4** — ANOVA and Tukey HSD: %s of %s features differ at p < 0.001; strongest %s (F %s) (Tukey, 1949).' % (k['n_sig'], k['n_feat'], k['top_f'][0], k['top_f'][1]),
    '**Tier 5** — VIF and stepwise CDA: one severity axis (%s%% of separation), r₁ %s (Bhattacharya and Chattopadhyay, 2013).' % (k['cda1'][2], k['cda1'][1]),
    '**Tier 6** — Boruta: %s classification and %s regression disease-specific features (Kursa and Rudnicki, 2010).' % (k['bor'][0], k['bor'][2])],
   'Disease-sensitive bands, a White Rust Index, ranked responding features, separability of the six grades and two disease-specific feature pools.',
   'Walk along the arrows; read only the red result line of each box. This slide can be used alone as a one-slide summary of Objective 1.')
SL(6, 'Objective 2 flow: nested models and results', 'The six-step nested pipeline (Tier 2 bands → Boruta → VIF < 10 → ML-SFFS → tuning → test on the held-out replication) and the headline results for classification and regression.',
   ['Every selection step is repeated inside the training replications, so the test replication is used only once (Roberts et al., 2017; Varma and Simon, 2006).',
    'Selection: Boruta (Kursa and Rudnicki, 2010), VIF < 10 (Dormann et al., 2013), sequential floating forward selection (Pudil et al., 1994).',
    'Models: SVM (Cortes and Vapnik, 1995), random forest (Breiman, 2001), k-NN (Cover and Hart, 1967), MLP (Rumelhart et al., 1986), PLSR (Wold et al., 2001).',
    'Classification (%s leaves): best %s, macro-F1 %s, %s within ±1 grade, %s healthy vs diseased.' % (k['n_leaves'], k['bc'], k['c_mf1'], k['c_adj'], k['c_det']),
    'Regression (%s plot-dates): best %s, R² %s, RMSE %s PDI units, RPD %s.' % (k['n_pd'], k['br'], k['r_r2'], k['r_rmse'], k['r_rpd']),
    'Baselines: PLS-DA full spectrum macro-F1 %s; RF all 53 features %s; PLSR full spectrum R² %s; RFR all features %s; bottom-up PDI from leaf grades R² %s.' % (k['plsda'], k['rfall'], k['plsr'], k['rfrall'], k['bu_r2'])],
   'Validated models: compact feature sets (%s–%s features) match or exceed all-feature and full-spectrum baselines.' % (k['ofc_sizes'][0], k['ofc_sizes'][1]),
   'Stress that the numbers are from replications the model never saw during selection or tuning.')
SL(7, 'Workflow of the analysis (report Figure 1 and Table 1)', 'The workflow figure of the Word report and a table of each step, its method with reference and its output.',
   'The figure is the same flow drawn as a vertical chart with output boxes; the table is the compact version for the methods chapter.',
   'One-page overview of steps, references and outputs.', 'Use this slide if the audience wants the whole method on one page.',
   figs=[('lflow', 'l_flow.png', 'Workflow of the leaf-level analysis with references and outputs.')],
   tabs=[('steps', [['Step', 'Method (reference)', 'Output'], ['Tier 0', 'Grades (Conn et al., 1990); PDI (Wheeler, 1969); LORO folds', 'Labelled tables'], ['Pre-processing', 'Splice (Hueni and Bialek, 2017); SG (Savitzky and Golay, 1964)', 'Clean spectra'],
         ['Tier 1', 'Red edge (Horler et al., 1983); indices (Apan et al., 2004)', '1047 + 51 features'], ['Tier 2', 'Scalogram (Shukla et al., 2024); ReliefF (Robnik-Šikonja and Kononenko, 2003)', 'Band lists'], ['Tier 3', 'WRI search: VNIR, SWIR, full range (Mahlein et al., 2013)', 'WRI'],
         ['Tier 4', 'ANOVA + Tukey (Tukey, 1949)', 'Responding features'], ['Tier 5', 'VIF + stepwise CDA (Bhattacharya and Chattopadhyay, 2013)', 'Separability'], ['Tier 6', 'Boruta (Kursa and Rudnicki, 2010)', 'DSF pools'], ['Objective 2', 'Nested LORO; ML-SFFS (Pudil et al., 1994)', 'Validated models']],
         'Steps of the analysis, methods with references and outputs.')])

# ================= DATA =================
H1('Part 3. Study data and pre-processing')
Pp('Slide 8 is the section divider "Study data and pre-processing: Tier 0, pre-processing and Tier 1".')
SL(9, 'Tier 0: data, labels and validation design', 'The four ASD files, the 48-plot design, the grade key, the PDI formula and the validation folds, with a table of leaves per date and grade.',
   ['Four ASD contact-probe files: 11 February, 24 February, 3 March and 13 March 2026; 350–2500 nm at 1 nm.',
    '48 plots: 12 controls and 36 inoculated (3 varieties × 4 inoculation dates × 3 replications).',
    'Each leaf was scored with the 0–9 key (Conn et al., 1990), giving six classes (0, 1, 3, 5, 7, 9).',
    'Plot PDI = Σ score / (9 × n) × 100 (Wheeler, 1969) is the regression target; the plot spectrum is the mean of its leaves.',
    'Validation: leave-one-replication-out (R1, R2, R3); controls split by variety; leaves of one plot are never split between training and test (Roberts et al., 2017).'],
   '%s labelled leaf spectra and %s plot-dates (PDI 0–%s%%); three balanced LORO folds.' % (k['n_leaves'], k['n_pd'], k['pdi_max']),
   'Explain why replications are the folds: plots of one replication share a block, so testing on a whole replication mimics new plots.',
   tabs=[('data', DK['t_data'], 'Leaves per date and grade and mean plot PDI.')])
SL(10, 'Tier 0: grade distribution across dates', 'A stacked bar chart of leaves per grade on each date.',
   'Severity increases over time: on 11 February most leaves are grade 0–1 (onset); from 24 February all grades occur; on 13 March grades 5 and 7 dominate; controls stay grade 0. Grade 9 is the smallest class, so class weights and macro-F1 are used in modelling (Sokolova and Lapalme, 2009).',
   'All six grades are represented; severity increases with time; unequal class sizes are handled in modelling.', 'Point at 13 March to show the epidemic development; mention class imbalance.')
SL(11, 'Pre-processing of the ASD spectra', 'The pre-processing steps and the mean reflectance and first derivative of the six grades.',
   ['Splice correction at the VNIR/SWIR detector join (1000 nm; mean step %s) (Hueni and Bialek, 2017).' % k['splice'],
    '400–2400 nm kept; 350–399 nm is noisy.',
    '1350–1450 and 1800–1950 nm removed for band-level selection, so the band results transfer to field and UAV data (Thenkabail et al., 2004). Because the spectra were taken with the contact probe, these bands carry leaf-water information and were kept for the whole-range WRI (slides 18–21).',
    'Savitzky–Golay smoothing (11 nm, 2nd order) with first and second derivatives (Savitzky and Golay, 1964; Tsai and Philpot, 1998).',
    '5 nm bands → 349 bands × (R, FD, SD); plot spectrum = mean of the leaves of a plot-date.'],
   'Clean spectra: visible and SWIR reflectance rise, NIR falls and the red-edge peak drops and shifts to shorter wavelengths with increasing grade.',
   'Show the figure and describe the three changes (visible up, NIR down, red-edge peak lower) as the classical signs of foliar disease (Carter and Knapp, 2001).',
   figs=[('spec', 'l_spectra.png', 'Mean leaf reflectance (a) and first derivative (b) of the six grades.')])
SL(12, 'Tier 1: features extracted from each spectrum', 'Four cards (1047 band features, 39 base indices, 9 SWIR disease indices, 3 red-edge parameters) and the SWIR index table.',
   'Band features are reflectance and its derivatives at 349 bands. Indices cover pigments, structure and water (Filella and Peñuelas, 1994; Blackburn, 1998; Gitelson et al., 2001), plus SWIR disease and water indices: DWSI (Apan et al., 2004), NDWI (Gao, 1996), MSI (Hunt and Rock, 1989), NDII (Hardisky et al., 1983), RBI and NDBI (Mandal et al., 2023; Ramalingam et al., 2026). Red-edge position, amplitude and second-derivative amplitude follow Horler et al. (1983).',
   'Leaf feature table (2339 × 1098) and plot feature table (192 × 1098).', 'Say that features were computed separately on leaf spectra (classification) and on plot-mean spectra (regression).',
   tabs=[('swiridx', [['SWIR index', 'Formula', 'Reference'], ['DWSI-2', 'R1660/R550', 'Apan et al., 2004'], ['DWSI-3', 'R1660/R680', 'Apan et al., 2004'], ['DWSI-5', '(R800+R550)/(R1660+R680)', 'Apan et al., 2004'], ['NDWI', '(R860−R1240)/(R860+R1240)', 'Gao, 1996'],
         ['MSI', 'R1600/R820', 'Hunt and Rock, 1989'], ['NDII', '(R819−R1649)/(R819+R1649)', 'Hardisky et al., 1983'], ['RBI_M / NDBI', 'R1148, R1301', 'Mandal et al., 2023'], ['RBI_R', '(R1068−R1560)/(R1068+R1560)', 'Ramalingam et al., 2026']], 'SWIR disease and water indices.')])

# ================= OBJECTIVE 1 =================
H1('Part 4. Objective 1: characterisation (Tiers 2–6)')
Pp('Slide 13 is the section divider "Objective 1: characterisation (Tiers 2–6)".')
SL(14, 'Tier 2: correlation scalogram and ReliefF', 'The settings of the two band-selection methods and the scalogram (r of R, FD and SD with PDI) and ReliefF weights across the spectrum.',
   ['Correlation scalogram: Pearson r of every band of R, FD and SD with plot PDI (n = 192); candidates with p < 0.01 and the top 5% |r| (Shukla et al., 2024; Cheng et al., 2010).',
    'ReliefF on the six leaf grades (k = 10; neighbours from the same plot excluded); top 5% of weights (Robnik-Šikonja and Kononenko, 2003).',
    'One band per correlated region (r ≥ 0.95) avoids picking many copies of the same information (Tian et al., 2021).',
    'Derivative bands within 10 nm of the splice or of removed water-band edges are not eligible (artefact peaks).'],
   'Strongest correlation: FD at %s nm (r = %s); reflectance at %s nm (r = %s); ReliefF peaks in the red edge.' % (k['maxr_fd'][1], k['maxr_fd'][0], k['maxr_r'][1], k['maxr_r'][0]),
   'Explain that the scalogram serves regression (PDI) and ReliefF serves classification (grades); bands found by both are "robust".',
   figs=[('scal', 'l_scal_relief.png', 'Correlation scalograms of R, FD and SD with plot PDI and ReliefF weights for the six grades.')])
SL(15, 'Tier 2 results: correlated regions and band lists', 'The band-to-band correlation matrix with region borders, and the three band lists.',
   'Regions R / FD / SD: %s / %s / %s; scalogram candidates %s → %s regions; ReliefF candidates %s → %s regions. Neighbouring reflectance bands are almost identical (median adjacent r = %s). Bands found in both lists are robust; scalogram-only bands go to the regression list and ReliefF-only bands to the classification list (Tian et al., 2021).'
   % (k['regions']['R'], k['regions']['FD'], k['regions']['SD'], k['scal'][0], k['scal'][1], k['rel'][0], k['rel'][1], k['adj_r']),
   '%s robust bands (red to red edge, 630–860 nm, mostly derivatives), %s regression-only and %s classification-only bands.' % (k['n_rob'], k['n_reg'], k['n_cls']),
   'Point at the red block of high correlation to explain why one band per region is enough.',
   figs=[('regions', 'l_regions.png', 'Band-to-band correlation of leaf reflectance with correlated regions.')],
   tabs=[('bands', DK['t_bands'], 'Tier 2 band lists.')])
SL(16, 'Tier 3: White Rust Index search', 'The index form, the search settings and the ReliefF weights with the best VNIR and SWIR indices by grade.',
   ['WRI = ND(λ1, λ2) + w × R(λ3), w ∈ {−1, −0.5, 0, 0.5, 1} (Mahlein et al., 2013).',
    'Bands every 6 nm; ND bands at least 50 nm apart; ReliefF (healthy vs diseased) keeps the top 25% of bands and NDs (Robnik-Šikonja and Kononenko, 2003).',
    'VNIR (450–950 nm): %s candidates; SWIR (1000–2400 nm, water bands removed): %s candidates.' % (k['wri_ncand'], k['wri_sw_ncand']),
    'Each candidate is screened by its best balanced accuracy; the 30 best are checked by 8-fold plot-grouped cross-validation with the threshold fitted on training folds.'],
   'WRI = %s: balanced accuracy %s, r with PDI %s; SWIR index %s weaker (%s).' % (k['wri'], k['wri_ba'], k['wri_r'], k['wri_sw'], k['wri_sw_ba']),
   'Explain the three parts of the WRI: NIR structure (750 nm), water shoulder (948 nm) and red-edge chlorophyll (696 nm).',
   figs=[('wri', 'l_wri.png', 'ReliefF weights (a) and best VNIR (b) and SWIR (c) indices by grade.')])
SL(17, 'Tier 3 results: best candidates and WRI by grade', 'The table of the best candidates and a bar chart of the mean VNIR WRI by grade.',
   'The best candidates are all similar NIR–water-shoulder contrasts, which shows that the result is stable. The mean WRI by grade (%s) decreases steadily from grade 0 to 9.' % ', '.join('%.3f' % v for v in DK['wri_means']),
   'The WRI decreases steadily from grade 0 to 9 and combines structure, water and chlorophyll information.', 'Read the bar chart from left to right to show the monotonic decrease.',
   tabs=[('wricand', DK['t_wri'], 'Best White Rust Index candidates (healthy vs diseased leaves).')])
SL(18, 'Tier 3b: full-range WRI with contact-probe spectra', 'Why the water bands can be kept, the four index searches and their best formulas.',
   ['The ASD contact probe has its own light source and only a few millimetres of air between leaf and fibre, so atmospheric water vapour does not affect 1350–1450 and 1800–1950 nm.',
    'In these spectra the absorption near 1450 and 1940 nm is leaf liquid water, a disease-relevant signal (Gao, 1996; Hunt and Rock, 1989), so the bands were kept.',
    'Same rules as Tier 3 (Mahlein et al., 2013); splice correction applied to 1001–2500 nm (Hueni and Bialek, 2017).',
    'Four searches on the same corrected spectra: VNIR, SWIR without water bands, SWIR with water bands (SWIR-W) and the whole range 400–2400 nm (FULL).',
    'Nested check: formula chosen without the test replication (Varma and Simon, 2006).'],
   'Whole range: %s bands, %s pairs, %s candidates; best WRI-FULL = %s (BA %s), the same red-edge / NIR / 970 nm region as the VNIR WRI.' % (k['wf_nb'], k['wf_npairs'], k['wf_ncand'], k['wf'], k['wf_ba']),
   'Say clearly: the whole range was searched, with water bands, and it chose the VNIR again.',
   tabs=[('wfsearch', DK['t_wf_search'], 'White Rust Index searches (6 nm bands; ND bands ≥ 50 nm apart; ReliefF top 25%).')])
SL(19, 'Tier 3b results: ReliefF (400–2400 nm) and WRIs by grade', 'ReliefF weights over the whole range with the kept water bands shaded and the bands of WRI-FULL marked, and box plots of the four WRIs by grade with Tukey letters.',
   'ReliefF is highest in the red edge (about 700 nm) and the red; smaller peaks appear inside the kept water bands (about 1450 and 1880 nm), confirming that these bands carry some disease information in contact-probe spectra. All four WRIs decrease with grade; VNIR, SWIR-W and FULL separate all six grades (letters a–f), whereas the SWIR index without water bands does not separate grades 7 and 9.',
   'Red edge dominates; water bands add secondary information; all WRIs track severity.', 'Point at the shaded water bands and their small ReliefF peaks, then at the red-edge peak.',
   figs=[('wrifull', 'l_wri_full.png', 'ReliefF weights over 400–2400 nm (a) and the VNIR, SWIR, SWIR-W and FULL indices by grade (b–e).')])
SL(20, 'Tier 3b results: comparison of the White Rust Indices', 'All WRIs compared with NDVI and NDWI on the same leaves: balanced accuracy, AUC, early-detection AUC (grade 0 vs 1), ANOVA F, η², Spearman ρ with grade and r with plot PDI.',
   ['WRI-FULL ≈ WRI-VNIR (BA %s vs %s, within the CV SD of 0.02): the whole range adds no extra discrimination.' % (k['wf_ba'], k['wv_ba2']),
    'Keeping water bands improves the SWIR index (BA %s → %s; r with PDI −0.66 → −0.71), but SWIR stays below VNIR.' % (k['ws_ba2'], k['wsw_ba']),
    'All WRIs beat NDVI (Rouse et al., 1974) and NDWI (Gao, 1996); the simplest two-band %s gives the highest F and the best grade 0 vs 1 AUC.' % k['wnd'],
    'The SWIR index re-derived on the corrected spectra is ND(1564, 2116) + 0.5 R2314 (Tier 3: ND(1564, 2122)).'],
   'Best overall: WRI-FULL ≈ WRI-VNIR ≈ ND(790, 862) > SWIR-W > SWIR > NDVI > NDWI.', 'Use this table to answer "did you try the whole spectrum?" and "is your index better than NDVI?".',
   tabs=[('wfcmp', DK['t_wf_cmp'], 'Comparison of the White Rust Indices with NDVI and NDWI.')])
SL(21, 'Tier 3b results: nested leave-one-replication-out check', 'The formula chosen in each training fold with its held-out balanced accuracy, and a bar chart comparing cross-validated and nested accuracy.',
   ['VNIR and FULL searches choose the same region in every fold (748–808 nm against 862–994 nm, with or without R696–700): the index is stable.',
    'SWIR formulas change between folds: less stable, lower held-out accuracy.',
    'Held-out BA: %s (VNIR), %s (FULL), %s (SWIR), %s (SWIR-W); only slightly below the cross-validated 0.77, so the search on all leaves caused little optimism (Varma and Simon, 2006).' % (nest['VNIR'], nest['FULL'], nest['SWIR'], nest['SWIR-W'])],
   'Recommended: VNIR WRI (UAV-compatible); the whole-range search confirms it. The SWIR index with water bands is complementary severity information.',
   'Stress stability: the same wavelengths are chosen whichever replication is left out.',
   tabs=[('wfnest', DK['t_wf_nested'], 'Nested check: formula (balanced accuracy on the held-out replication).')])
SL(22, 'Tier 4: univariate response (ANOVA, Tukey HSD, r with PDI)', 'The statistical tests and the 12 strongest features ranked by ANOVA F.',
   'One-way ANOVA across the six grades gives F and η² = SS_between/SS_total; Tukey HSD gives grade groups (Tukey, 1949; Gomez and Gomez, 1984); Pearson r with PDI is computed on plot-mean features and Spearman ρ with the leaf grade (Spearman, 1904). Leaves within a plot are not independent, so p-values are used only to rank features (Mahlein et al., 2019).',
   '%s of %s features differ at p < 0.001; strongest: red-edge FD (%s, F %s, η² %s), WRI, red-edge SD, RVSI, HI, ARI.' % (k['n_sig'], k['n_feat'], k['top_f'][0], k['top_f'][1], k['top_f'][2]),
   'Say that η² ≈ 0.3–0.37 means that a third of the leaf-to-leaf variation is explained by the grade.',
   tabs=[('anova', DK['t_anova'], 'Twelve strongest features (one-way ANOVA across six grades; r with plot PDI; ρ with leaf grade).')])
SL(23, 'Tier 4 results: grade responses and Tukey groups', 'Box plots of the six strongest features by grade with Tukey letters and the letter table.',
   'Grades that share a letter do not differ (Tukey, 1949). First derivatives and the WRI separate all six grades; some second-derivative features and RVSI do not separate grades 0 and 1.',
   'Monotonic response with severity; grades 0 and 1 overlap for some features.', 'Point at grade 0 vs grade 1 to introduce the early-detection difficulty.',
   figs=[('anovafig', 'l_anova.png', 'Six strongest features by grade with Tukey letters.')], tabs=[('tukey', DK['t_tukey'], 'Tukey HSD letters (α = 0.05).')])
SL(24, 'Tier 4 results: SWIR indices and relation with PDI', 'The SWIR index ANOVA table and scatter plots of plot PDI against the four indices most correlated with it.',
   'SWIR water indices respond to white rust because infected leaves lose water (Apan et al., 2004; Yu et al., 2018; Kundu et al., 2021). DWSI-5, MSI, NDII and NDWI reach |r| about 0.6 with PDI (Gao, 1996; Hunt and Rock, 1989; Hardisky et al., 1983).',
   'SWIR water indices respond; strongest %s (r = %s); |r| up to %s.' % (k['swir_best'][0], k['swir_best'][1], k['swir_maxr']),
   'Mention that later dates (red points) give the strongest SWIR response.',
   figs=[('rpdi', 'l_r_pdi.png', 'Plot PDI against the four indices most correlated with it (colour = date).')], tabs=[('swirt', DK['t_swir'], 'SWIR indices: ANOVA F, η² and r with PDI.')])
SL(25, 'Tier 5: VIF and two-step stepwise CDA', 'The CDA settings and the results table for the two steps.',
   'Collinear features are removed until VIF < 10 (Dormann et al., 2013). Forward stepwise discriminant analysis enters the variable with the largest partial F (Wilks\' lambda; p < 0.001; at most 10 variables) (Klecka, 1980; Whittingham et al., 2006). Step 1 uses the classification bands, step 2 indices + red edge + WRI (Bhattacharya and Chattopadhyay, 2013). LDA accuracy (Fisher, 1936) is computed on held-out replications.',
   'One dominant severity axis (%s%% / %s%%); r₁ %s / %s; six-grade LDA accuracy %s / %s; ±1 grade %s / %s.' % (k['cda1'][2], k['cda2'][2], k['cda1'][1], k['cda2'][1], k['cda1'][4], k['cda2'][4], k['cda1'][5], k['cda2'][5]),
   'Explain that one canonical function explains about 90% of the separation: severity behaves as one continuous axis.',
   tabs=[('cda', DK['t_cda'], 'Two-step stepwise CDA.')])
SL(26, 'Tier 5 results: canonical score plots', 'Canonical scores of the two CDA steps; crosses mark the grade centroids, ordered 0 → 9 along function 1.',
   'The centroids line up along function 1 in grade order, and the clouds of neighbouring grades overlap. Exact six-grade separation is therefore limited, as reported for other leaf diseases (Zhang et al., 2012a).',
   'Grades lie on one severity axis; neighbouring grades overlap.', 'Use the figure to explain why exact grade accuracy is moderate but ±1-grade accuracy is high.',
   figs=[('cdafig', 'l_cda.png', 'Canonical scores of the two CDA steps.')])
SL(27, 'Tier 6: Boruta disease-specific feature pools', 'Boruta settings and the importance plots for classification and regression.',
   'Boruta compares each feature\'s random-forest importance with shuffled "shadow" copies (alpha = 0.01, up to 100 iterations) and confirms all relevant features (Kursa and Rudnicki, 2010; Mustafa et al., 2023). It was run on leaves for grades and on plots for PDI.',
   '%s of %s features confirmed for classification; %s of %s for regression, led by the WRI.' % (k['bor'][0], k['bor'][1], k['bor'][2], k['bor'][3]),
   'Green bars are confirmed, yellow tentative, red rejected.', figs=[('boruta', 'l_boruta.png', 'Boruta importance for classification (left) and regression (right).')])
SL(28, 'Tier 6 results: disease-specific feature (DSF) pools', 'The confirmed features of the two pools.',
   'The classification pool combines red-edge derivatives with pigment indices (HI, ARI, NPCI, PRI); the regression pool combines the WRI, red reflectance (695 nm), red-edge derivatives and DWSI-5. The pools agree with the ANOVA ranking and the CDA variables.',
   'Two DSF pools (classification and regression) that feed Objective 2.', 'Say that the pools are the starting point of the nested selection in Objective 2.',
   tabs=[('dsf', DK['t_dsf'], 'Disease-specific feature pools confirmed by Boruta.')])
SL(29, 'Additional analysis: robust SWIR regions', 'Tier 2 repeated on 1000–2400 nm only, with the resulting SWIR band lists.',
   'The SWIR-only band selection was tested in every training fold and by date. 1595–1615 nm lies in the SWIR-1 water and dry-matter region used by MSI, NDII and DWSI (Apan et al., 2004); 1495–1515 and 1965–1995 nm are shoulders of the leaf-water absorption bands. The SWIR signal is stronger at higher severity (later dates).',
   'Robust SWIR regions (1495–1515, 1595–1615, 1965–1995 nm) reflect leaf-water loss; 1595–1615 nm is the most usable for UAV and satellite sensors.', 'Link 1600 nm to the SWIR-1 bands of satellite sensors.',
   tabs=[('swirreg', DK['t_swirreg'], 'SWIR-only Tier 2 band lists.')])

# ================= OBJECTIVE 2 =================
H1('Part 5. Objective 2: classification and regression')
Pp('Slide 30 is the section divider "Objective 2: classification and regression — nested leave-one-replication-out models".')
SL(31, 'Nested selection in each training fold', 'For each held-out replication, the number of bands, Boruta features and VIF-free features and the final feature sets of the best models.',
   'All selection is repeated on the training replications only. ML-SFFS (floating forward selection; Pudil et al., 1994) uses an inner 3-fold plot-grouped CV and keeps the smallest subset within 0.01 macro-F1 (2% RMSE) of the best (Tian et al., 2021). Selecting features on all data would bias accuracy upwards (Ambroise and McLachlan, 2002; Varma and Simon, 2006).',
   'Compact, fold-specific optimum feature sets; red-edge derivatives and pigment/water indices recur across folds.', 'Show that different folds choose similar features: evidence of stable features.',
   tabs=[('folds', DK['t_folds'], 'Nested selection per test replication (C = classification, R = regression).')])
SL(32, 'ML-SFFS curves (fold 1 training data)', 'Inner-CV score against the number of selected features for classification and regression.',
   'Performance rises quickly with the first few features and then flattens, so small models are enough (Pudil et al., 1994).',
   'Performance saturates after a few features, supporting compact models and limiting overfitting.', 'Point at the plateau and say why the smallest subset near the best is chosen.',
   figs=[('sffs', 'l_sffs.png', 'ML-SFFS curves: classification (a) and regression (b).')])
SL(33, 'Six-grade leaf classification', 'Held-out performance of the classifiers and baselines (table and bar chart).',
   'Models: SVM (Cortes and Vapnik, 1995), RF (Breiman, 2001), k-NN (Cover and Hart, 1967) and MLP (Rumelhart et al., 1986), compared with PLS-DA on the full spectrum and RF on all 53 features. Metrics: overall accuracy, kappa (Cohen, 1960), macro-F1 (Sokolova and Lapalme, 2009), ±1-grade accuracy and healthy-vs-diseased accuracy.',
   'Best %s: macro-F1 %s, OA %s, kappa %s, ±1 grade %s, healthy vs diseased %s.' % (k['bc'], k['c_mf1'], k['c_oa'], k['c_kap'], k['c_adj'], k['c_det']),
   'Present macro-F1 and ±1-grade accuracy together; explain why macro-F1 is used (unequal classes).',
   tabs=[('cls', DK['t_cls'], 'Six-grade classification on held-out replications.')])
SL(34, 'Classification detail: confusion matrix and per-grade metrics', 'The confusion matrix of the best classifier, observed vs predicted PDI, and precision, recall and F1 per grade.',
   'Grade 0 is recognised best; grades 1–5 are confused mainly with their neighbours; grade 9 is partly predicted as 5 or 7. Errors between neighbouring grades are expected because grades are cuts of a continuous severity (Mandal et al., 2023; Meng et al., 2020).',
   'Errors are mainly between neighbouring grades.', 'Point at the diagonal band of the confusion matrix.',
   figs=[('evalfig', 'l_eval.png', 'Confusion matrix (a) and observed vs predicted plot PDI (b).')], tabs=[('grade', DK['t_grade'], 'Per-grade precision, recall and F1 of the best classifier.')])
SL(35, 'Plot-level PDI regression', 'Held-out performance of the regressors and baselines (table and bar chart).',
   'Models: SVR, RFR, k-NN, PLSR (Wold et al., 2001) and MLP; baselines PLSR on the full spectrum and RFR on all features; bottom-up PDI from predicted leaf grades. Metrics: R², RMSE, NRMSE and RPD = SD/RMSE (Chang et al., 2001; Liu et al., 2024).',
   'Best %s: R² %s, RMSE %s PDI units, RPD %s; bottom-up PDI from leaf grades R² %s.' % (k['br'], k['r_r2'], k['r_rmse'], k['r_rpd'], k['bu_r2']),
   'Mention that RPD 1.95 is just below 2, i.e. good for screening but not yet for precise quantification.',
   tabs=[('reg', DK['t_reg'], 'Plot PDI regression on held-out replications.')])
SL(36, 'Model comparison (report figure)', 'Bar charts of classification and regression performance for all models.',
   'Selected-feature models use 4–7 features and perform as well as or better than baselines that use all features or the full spectrum.',
   'Selected-feature models are as good as or better than all-feature and full-spectrum baselines with far fewer features.', 'Use this as the summary figure of Objective 2.',
   figs=[('models', 'l_models.png', 'Six-grade classification (a) and PDI regression (b) on held-out replications.')])
SL(37, 'Performance by date and variety', 'Accuracy of the best models per date and per variety.',
   'On 11 February the PDI range is very small, so R² is not meaningful although RMSE is smallest. Performance is similar across the three varieties, so the features are not variety-specific.',
   'Models are consistent across dates with sufficient severity range and across varieties.', 'Mention that early dates need detection rather than severity models.',
   tabs=[('date', DK['t_date'], 'Performance by date.'), ('var', DK['t_var'], 'Performance by variety.')])

# ================= RESULTS AND DISCUSSION =================
H1('Part 6. Results, findings and discussion')
Pp('Slide 38 is the section divider "Results, findings and discussion".')
SL(39, 'Outputs of each step', 'A table with the output and key result of every step.',
   'This table links each step to what it produced; it is the bridge between the methods and the discussion.', 'Every step produced a defined, quantified output.', 'Use it as a recap before the discussion.',
   tabs=[('outputs', [['Step', 'Output', 'Key result'], ['Tier 0', 'Labelled data, folds', '%s leaves; %s plot-dates' % (k['n_leaves'], k['n_pd'])], ['Pre-processing', 'Clean spectra', '349 bands × R, FD, SD'], ['Tier 1', 'Feature tables', '1047 band + 51 features'],
         ['Tier 2', 'Band lists', '%s robust bands (630–860 nm); max r %s (FD%s)' % (k['n_rob'], k['maxr_fd'][0], k['maxr_fd'][1])], ['Tier 3', 'White Rust Index', '%s; BA %s; r %s; full-range WRI %s (BA %s)' % (k['wri'], k['wri_ba'], k['wri_r'], k['wf'], k['wf_ba'])],
         ['Tier 4', 'Responding features', '%s/%s significant; SWIR |r| up to %s' % (k['n_sig'], k['n_feat'], k['swir_maxr'])], ['Tier 5', 'Separability', 'One severity axis; r₁ %s; ±1 grade %s' % (k['cda1'][1], k['cda1'][5])],
         ['Tier 6', 'DSF pools', '%s classification, %s regression features' % (k['bor'][0], k['bor'][2])], ['SWIR analysis', 'Robust SWIR regions', '1495–1515, 1595–1615, 1965–1995 nm'],
         ['Objective 2 (grades)', 'Classifier', '%s: macro-F1 %s; ±1 grade %s; healthy vs diseased %s' % (k['bc'], k['c_mf1'], k['c_adj'], k['c_det'])], ['Objective 2 (PDI)', 'Regressor', '%s: R² %s; RMSE %s; RPD %s' % (k['br'], k['r_r2'], k['r_rmse'], k['r_rpd'])]],
         'Output and key result of each step.')])
SL(40, 'Major results', 'Eight result cards.',
   ['Red-edge first derivative at %s nm has the highest correlation with PDI (r = %s).' % (k['maxr_fd'][1], k['maxr_fd'][0]),
    'The WRI separates healthy and diseased leaves with balanced accuracy %s; the whole-range search confirms it.' % k['wri_ba'],
    'SWIR water indices reach |r| = %s with PDI.' % k['swir_maxr'],
    '%s%% of the grade separation lies on one canonical severity axis.' % k['cda1'][2],
    'Six-grade macro-F1 %s, %s within ±1 grade, %s healthy vs diseased (%s).' % (k['c_mf1'], k['c_adj'], k['c_det'], k['bc']),
    'Plot PDI R² %s (%s, 4 features).' % (k['r_r2'], k['br'])],
   'Red edge and WRI carry the white-rust signal; SWIR adds water information; PDI is predicted better than exact grades.', 'Read the cards row by row; all values are held-out estimates.')
SL(41, 'Key findings and literature support', 'Seven findings, the evidence in this study and the supporting literature.',
   'Each finding is supported by independent tiers and by published work: red-edge derivatives (Horler et al., 1983; Filella and Peñuelas, 1994; Shukla et al., 2024); disease-specific indices (Mahlein et al., 2013; Ashourloo et al., 2014; Meng et al., 2020); SWIR water information (Apan et al., 2004; Yu et al., 2018; Kundu et al., 2021); grade overlap (Mandal et al., 2023; Lv et al., 2023); PDI regression (Liu et al., 2024; Feng et al., 2022); nested validation (Varma and Simon, 2006; Tian et al., 2021; Mustafa et al., 2023).',
   'The results agree with the literature and are consistent across tiers.', 'Pick two or three findings and name one supporting paper for each.',
   tabs=[('findings', [['Finding', 'Evidence in this study', 'Literature'], ['Red-edge derivatives are the most robust features', 'Tiers 2, 4, 5, 6 all select FD/SD at 680–860 nm', 'Horler et al., 1983; Filella and Peñuelas, 1994; Shukla et al., 2024'],
         ['A disease-specific index works better than general indices', 'WRI top univariate and regression feature', 'Mahlein et al., 2013; Ashourloo et al., 2014; Meng et al., 2020'], ['SWIR adds water-loss information', 'DWSI-5, MSI, NDII, NDWI respond; DWSI-5 in DSF pool', 'Apan et al., 2004; Yu et al., 2018; Kundu et al., 2021'],
         ['Neighbouring grades overlap', 'One canonical axis; errors mostly adjacent', 'Mandal et al., 2023; Meng et al., 2020; Lv et al., 2023'], ['PDI regression is more reliable than exact grades', 'Plot averaging reduces within-plot noise', 'Liu et al., 2024; Feng et al., 2022'],
         ['Compact nested models generalise', 'Selected features match all-feature baselines', 'Varma and Simon, 2006; Tian et al., 2021; Mustafa et al., 2023'], ['The VNIR carries the white-rust index signal', 'Whole-range search selects 748, 994, 700 nm; SWIR indices weaker', 'Mahlein et al., 2013; Apan et al., 2004']],
         'Key findings with evidence and literature.')])
SL(42, 'Discussion: physiological interpretation', 'Three panels: red edge, White Rust Index and SWIR.',
   ['**Red edge.** Pustules and chlorosis reduce chlorophyll and disturb the mesophyll, lowering and shifting the red-edge slope; first derivatives at 790–830 nm capture this best (Horler et al., 1983; Carter and Knapp, 2001).',
    '**White Rust Index.** It combines the NIR plateau (750 nm), the 970 nm water-band shoulder (948 nm) and red-edge chlorophyll (696 nm): structure, water and pigment in one index (Mahlein et al., 2013). The whole-range search with water bands kept chose the same bands (748, 994, 700 nm).',
    '**SWIR.** Infected leaves lose water, raising reflectance near 1500, 1600 and 1970 nm; the SWIR signal grows with severity, so it marks severity rather than early infection (Apan et al., 2004).'],
   'The selected features are physically meaningful, which supports their transfer to UAV and satellite sensors.', 'Connect each spectral region to a leaf process (pigment, structure, water).')
SL(43, 'Discussion: severity, validation and other studies', 'Why exact grade accuracy is limited, how it compares with other studies, and why nested validation matters.',
   ['Exact six-grade accuracy (macro-F1 %s) is limited because grades 0 and 1 differ by only 1–5%% leaf area and neighbouring grades overlap spectrally.' % k['c_mf1'],
    'Similar limits: 70% for three yellow-rust levels (Meng et al., 2020); severity 81.8% vs detection 93.1% (Lv et al., 2023); adjacent blast grades inseparable (Mandal et al., 2023).',
    'Within-one-grade (%s) and healthy-vs-diseased accuracy (%s) are the decision-relevant measures.' % (k['c_adj'], k['c_det']),
    'Plot PDI (R² %s) is predicted better than leaf grades because averaging leaves removes within-plot variation; bottom-up PDI from leaf grades (R² %s) confirms consistency.' % (k['r_r2'], k['bu_r2']),
    'Nested leave-one-replication-out validation gives honest accuracy; selecting on all data would inflate it (Varma and Simon, 2006).'],
   'Report PDI regression and ±1-grade accuracy alongside exact grade accuracy.', 'Answer the expected question "why is accuracy only 0.32?" with the overlap argument and the literature.')
SL(44, 'Implications for UAV and satellite analysis, and limitations', 'Four implications and five limitations.',
   ['**Implications.** Prioritise the red edge (690–860 nm) in UAV band selection; test the leaf WRI on UAV canopy spectra (recalibration likely); use SWIR water indices and 1595–1615 nm as complementary features; apply the same nested chain (Tier 2 → Boruta → VIF → ML-SFFS) to UAV data.',
    '**Limitations.** Leaf data are an upper bound for canopy performance (Mahlein, 2016); the WRI formula was searched on all leaves, but the nested check gives a held-out BA of about %s; leaf-level p-values are optimistic; one season and one site; physiological measurements (pigments, relative water content) are still to be added.' % nest['VNIR']],
   'Leaf results fix the wavelengths and the index to test at canopy and satellite scale.', 'Show that limitations are known and have a plan.')
SL(45, 'Conclusions', 'Five numbered conclusions and the next step.',
   ['Red-edge first and second derivatives (680–860 nm) are the most robust white-rust features.',
    'A VNIR White Rust Index (%s) separates healthy and diseased leaves and tracks PDI; a whole-range search confirms it.' % k['wri'],
    'SWIR water regions (1495–1515, 1595–1615, 1965–1995 nm) add severity information.',
    'Severity acts as one spectral axis; neighbouring grades overlap, so PDI and ±1-grade accuracy are essential.',
    'Compact nested models predict plot PDI well and give honest accuracy estimates.'],
   'Next: apply the same chain to UAV hyperspectral, multispectral, RGB and thermal data and test transfer to satellite bands.', 'End with the next step to link the leaf study to the UAV and satellite work.')
Pp('Slides 46–49 list the references cited in the presentation; the complete list follows.')
open(D + 'docx_body_slides.js', 'w').write('\n'.join(K)); print('slide guide body lines', len(K))
