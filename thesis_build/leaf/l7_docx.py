"""Build the detailed Word report (JS for the docx library) from the analysis results; reuses the thesis helpers and reference pool."""
import numpy as np, pandas as pd, json, os, re
B = os.path.dirname(os.path.abspath(__file__)) + '/'; D = B + 'data/'; S = B + '../'
Z = np.load(D + 'prep.npz'); M = pd.read_csv(D + 'meta_leaf2.csv'); P = pd.read_csv(D + 'plot_table.csv')
F = pd.read_csv(D + 'feat_leaf_wri.csv'); Fp = pd.read_csv(D + 'feat_plot_wri.csv'); info = json.load(open(D + 'prep_info.json'))
R1 = json.load(open(D + 'res1.json')); RS = R1['RES']; R2 = json.load(open(D + 'res2.json'))
A = pd.read_csv(D + 't_anova.csv'); y = M.grade.values; G6 = [0, 1, 3, 5, 7, 9]
t2, t3, t4, t5, t6 = RS['tier2'], RS['tier3'], RS['tier4'], RS['tier5'], RS['tier6']
rc, rr = R2['cls'], R2['reg']; bc, br = R2['best']['cls'], R2['best']['reg']; bu = [k for k in rr if k.startswith('Bottom-up')][0]
f2 = lambda v: '%.2f' % v; f3 = lambda v: '%.3f' % v
K = []
def esc(t):
    t = t.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    return re.sub(r'\[\[(T|F):(\w+)\]\]', lambda m: '${%s(\'%s\')}' % (m.group(1), m.group(2)), t)
def js(s): return '`' + esc(s) + '`'
def H1(t): K.append("K.push(H1(%s));" % js(t))
def H2(t): K.append("K.push(H2(%s));" % js(t))
def H3(t): K.append("K.push(H3(%s));" % js(t))
def Pp(t): K.append("K.push(P(%s));" % js(t))
def BL(items): K.extend("K.push(BL(%s));" % js(i) for i in items)
def BOX(l, t, fill='FFF6E0', line='C98A00'): K.append("K.push(BOX(%s, %s, '%s', '%s'));" % (js(l), js(t), fill, line))
def NOTE(t): K.append("K.push(NOTE(%s));" % js(t))
def EQ(t): K.append("K.push(EQ(%s));" % js(t))
def FIG(k, file, cap, w=540): K.append("K.push(...fig2('%s', '%s', %s, %d));" % (k, file, js(cap), w))
def TAB(k, rows, widths, cap, size=16):
    R = '[' + ',\n'.join('[' + ', '.join(js(str(c)) for c in r) + ']' for r in rows) + ']'
    K.append("K.push(...tab2('%s', %s, %s, %s, %d));" % (k, R, json.dumps(widths), js(cap), size))
def QA(q, a): K.append("QA(%s, %s);" % (js(q), js(a)))
def STEP(aim, method, settings=None):
    K.append("K.push(BOX('Aim of the step:', %s, 'ECEFF1', '455A64'));" % js(aim))
    Pp('**Method.** ' + method)
    if settings: BL(settings)
def OUTB(t): BOX('Output of this step:', t)

counts = pd.crosstab(M.date, M.grade)
# ================= TITLE =================
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 900, after: 160 }, children: [new TextRun({ text: 'Leaf-level hyperspectral analysis of white rust in mustard', font: FONT, size: 40, bold: true, color: '1E3A1F' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: 'ASD leaf spectra of four sampling dates analysed with the proposed tier methodology: six-grade classification and plot-level PDI regression', font: FONT, size: 26, color: '2C5F2D' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 500 }, children: [new TextRun({ text: 'Ph.D. (Agricultural Physics), ICAR-IARI  |  AI-based multimodal UAV sensing of white rust in mustard', font: FONT, size: 20, italics: true, color: '555555' })] }));")
NOTE('**Summary.** %d leaf spectra (ASD, 350–2500 nm) from 48 plots and four dates (11 February to 13 March 2026) were analysed with the agreed methodology. Objective 1 tiers showed that red-edge first and second derivatives (690–860 nm) are the most robust white-rust features; a White Rust Index, %s, separated healthy and diseased leaves with a cross-validated balanced accuracy of %s and correlated with plot PDI (r = %s); SWIR water indices also responded (|r| up to %s). In Objective 2, with every selection step repeated inside the training replications, the best six-grade classifier (%s) reached macro-F1 %s (±1-grade accuracy %s, healthy vs diseased accuracy %s), and the best PDI model (%s) reached R² %s (RMSE %s PDI units). Every method is followed by its reference.'
     % (len(M), t3['vnir']['formula'], f2(t3['vnir']['best']['ba_cv']), f2(np.corrcoef(Fp.WRI_VNIR, P.PDI)[0, 1]), f2(max(abs(r[2]) for r in t4['swir'])), bc, f2(rc[bc]['macro_f1']), f2(rc[bc]['adj']), f2(rc[bc]['detection_acc']), br, f2(rr[br]['r2']), '%.1f' % rr[br]['rmse']))
K.append("K.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-2' }));")
K.append("K.push(new Paragraph({ children: [new PageBreak()] }));")

# ================= 1 INTRODUCTION =================
H1('1. Purpose of the leaf-level analysis')
Pp('White rust, caused by *Albugo candida*, produces white pustules, chlorosis and, in severe cases, staghead deformation of mustard (Saharan et al., 2014). Leaf-level spectra measured with a contact probe are free of soil, shadow, flowers and illumination effects, so they show the pure spectral response of the disease and give the reference against which UAV canopy data are interpreted (Mahlein et al., 2012; Mahlein, 2016). This report applies the proposed tier methodology, unchanged in logic, to the leaf ASD data: Objective 1 tiers describe which wavelengths and indices respond to white rust, and Objective 2 builds and validates models for the six severity grades (classification) and the plot-level percent disease index (PDI, regression).')
FIG('flow', 'l_flow.png', 'Workflow of the leaf-level analysis following the proposed methodology (references in the output boxes).', 500)
TAB('tiers', [['Step', 'Method (reference)', 'Output'],
              ['Tier 0', 'Leaf grade with the 0–9 key (Conn et al., 1990); PDI (Wheeler, 1969); leave-one-replication-out folds', 'Labelled leaf and plot tables'],
              ['Pre-processing', 'Splice correction (Hueni and Bialek, 2017); Savitzky–Golay (Savitzky and Golay, 1964); derivatives (Tsai and Philpot, 1998)', 'Clean spectra, 349 bands'],
              ['Tier 1', 'Band features, red-edge parameters (Horler et al., 1983), 48 indices (Apan et al., 2004 and others)', '1047 band + 51 features'],
              ['Tier 2', 'Correlation scalogram (Shukla et al., 2024) + ReliefF (Robnik-Šikonja and Kononenko, 2003)', 'Robust, regression and classification bands'],
              ['Tier 3', 'White Rust Index search (Mahlein et al., 2013)', 'WRI'],
              ['Tier 4', 'One-way ANOVA + Tukey HSD (Tukey, 1949); Pearson r with PDI', 'Responding features'],
              ['Tier 5', 'VIF < 10 + two-step stepwise CDA (Bhattacharya and Chattopadhyay, 2013)', 'Separability of six grades'],
              ['Tier 6', 'Boruta (Kursa and Rudnicki, 2010)', 'Two DSF pools'],
              ['Objective 2', 'Nested LORO: Tier 2 → Boruta → VIF → ML-SFFS (Pudil et al., 1994) → SVM, RF, k-NN, MLP, SVR, RFR, PLSR', 'Validated models']],
    [1500, 5300, 2506], 'Steps of the leaf-level analysis and the references they follow.', 15)

# ================= 2 DATA =================
H1('2. Data and experimental design (Tier 0)')
STEP('Assemble a labelled, comparable leaf and plot dataset and fix the validation rule before any analysis.',
     'The four ASD files (11 February, 24 February, 3 March and 13 March 2026) contain, for every leaf, the reflectance spectrum from 350 to 2500 nm at 1 nm, the plot number, variety (V1–V3), growth stage, health status, leaf position and the disease score on the 0–9 key (0 = no pustules; 1, 3, 5, 7, 9 increasing pustule cover; Conn et al., 1990). The treatment file gives the inoculation date (D1–D4) and replication of each plot: 12 control plots and 36 inoculated plots in three replications (R1–R3).',
     ['Classification target: the leaf grade (six classes 0, 1, 3, 5, 7, 9).', 'Regression target: plot PDI = Σ score / (9 × number of leaves) × 100 for each plot-date, the formula already used in the field sheets (Wheeler, 1969).',
      'Plot spectrum: mean of the leaf spectra of the plot-date (192 plot-dates).',
      'Validation: leave-one-replication-out (LORO). Test fold k = replication Rk plus four control plots (controls split by variety: V1 → R1, V2 → R2, V3 → R3). Leaves of one plot are never split between training and test (Roberts et al., 2017).'])
rows = [['Date', 'Stage (main)', 'Leaves'] + ['Grade %d' % g for g in G6] + ['Mean PDI (%)']]
for d in sorted(M.date.unique()):
    rows.append([d, M[M.date == d].stage.mode()[0], int((M.date == d).sum())] + [int(counts.loc[d, g]) if g in counts.columns else 0 for g in G6] + ['%.1f' % P.PDI[P.date == d].mean()])
rows.append(['All', '—', len(M)] + [int((y == g).sum()) for g in G6] + ['%.1f' % P.PDI.mean()])
TAB('data', rows, [1300, 1300, 800] + [750] * 6 + [1406], 'Leaves per date and grade and mean plot PDI.', 15)
Pp('All six grades are well represented (grade 9 is the smallest class with %d leaves). Severity rises from a mean PDI of %.1f%% on 11 February to %.1f%% on 13 March; control plots stay at grade 0 on every date. The folds are balanced: each holds 185–188 healthy leaves and a similar mix of grades.' % ((y == 9).sum(), P.PDI[P.date == '2026-02-11'].mean(), P.PDI[P.date == '2026-03-13'].mean()))
OUTB('2339 labelled leaf spectra, 192 plot-dates with PDI (0–76%), three LORO folds.')

# ================= 3 PREPROCESSING =================
H1('3. Pre-processing')
STEP('Remove instrument artefacts and noise so that features reflect leaf properties.',
     'Five operations were applied to every leaf spectrum.',
     ['**Splice correction.** The ASD has separate VNIR and SWIR detectors; a small step remained at 1000/1001 nm (mean %.4f ± %.4f reflectance). The offset between the measured value at 1001 nm and the linear extrapolation from 999–1000 nm was removed from 1001–1800 nm (Hueni and Bialek, 2017).' % (info['splice_mean'], info['splice_sd']),
      '**Spectral range.** 350–399 nm was dropped because it is noisy (standard deviation of first differences about 50 times higher than at 800 nm); 2401–2500 nm was dropped as in the methodology (Shukla et al., 2024).',
      '**Water-vapour bands.** 1350–1450 and 1800–1950 nm were removed; they are dominated by atmospheric water in field and UAV data (Thenkabail et al., 2004).',
      '**Smoothing and derivatives.** Savitzky–Golay filter, window 11 nm, second-order polynomial; first (FD) and second (SD) derivatives from the same fit (Savitzky and Golay, 1964; Tsai and Philpot, 1998).',
      '**Band sampling.** For band-level analysis the spectra were sampled every 5 nm, giving 349 bands and 1047 band features (R, FD, SD). Neighbouring 5 nm reflectance bands are almost identical (median r = %.4f), which is why one band per correlated region is kept later (Mahlein et al., 2013).' % t2['median_adjacent_r']])
FIG('spec', 'l_spectra.png', 'Mean leaf reflectance (a) and first derivative (b) of the six grades after pre-processing.', 560)
Pp('With increasing grade, reflectance rises in the visible (chlorophyll loss and chlorosis), falls on the NIR plateau (cell-structure damage around pustules) and rises in the SWIR (lower leaf water); the first-derivative peak at the red edge becomes lower and moves to shorter wavelengths. These are the classical spectral signs of foliar disease and chlorophyll loss (Carter and Knapp, 2001; Horler et al., 1983; Mahlein et al., 2012).')
OUTB('Smoothed, splice-corrected spectra; 349 bands × (R, FD, SD).')

# ================= 4 OBJECTIVE 1 =================
H1('4. Objective 1: characterisation of white rust (Tiers 1–6)')
H2('4.1 Tier 1: feature extraction')
STEP('Turn each spectrum into physically meaningful features.',
     'From every leaf spectrum and every plot-mean spectrum the following were computed: 1047 band features (R, FD, SD at 349 bands); the red-edge position REP (wavelength of maximum FD in 680–750 nm), its amplitude Dr and the area SDr (Horler et al., 1983; Filella and Peñuelas, 1994); and 48 vegetation indices: the 39 base indices of the methodology (pigment, structure, photosynthesis and water indices such as PSSRa, ARI, PRI, HI, WI; Blackburn, 1998; Gitelson et al., 2001; Gamon et al., 1992; Mahlein et al., 2013; Peñuelas et al., 1997) and 9 SWIR disease indices (DWSI-2, DWSI-3, DWSI-5, Apan et al., 2004; NDWI, Gao, 1996; MSI, Hunt and Rock, 1989; NDII, Hardisky et al., 1983; RBI_M and NDBI, Mandal et al., 2023; RBI_R, Ramalingam et al., 2026).',
     ['ROTI uses 1982 nm; the leaf spectra are clean there (noise similar to 800 nm), so ROTI was kept (Bhattacharya and Chattopadhyay, 2013).', 'All index formulas are given as live Excel formulas in the Index formulas sheet of the accompanying workbook.'])
OUTB('Leaf feature table (2339 × 1047 band features + 51 features) and plot feature table (192 × the same).')

H2('4.2 Tier 2: band-level selection (correlation scalogram + ReliefF)')
STEP('Reduce 1047 redundant band features to a short list of white-rust bands for each task.',
     'The **correlation scalogram** gives Pearson r between plot PDI and R, FD and SD at every band (192 plot-dates; Shukla et al., 2024; Cheng et al., 2010). **ReliefF** weights each band feature by how well it separates near leaves of different grades (2339 leaves, six grades, k = 10, Manhattan distance on range-scaled features, neighbours from the same plot excluded; Robnik-Šikonja and Kononenko, 2003). Correlated regions were formed from contiguous bands with r ≥ 0.95 to the first band of the region, and only the best band of each region was kept in each list (Tian et al., 2021).',
     ['Scalogram candidates: p < 0.01 and top 5% of |r| within each spectrum type; ReliefF candidates: top 5% of all 1047 weights.',
      'Derivative bands within 10 nm of the splice (1000 nm) or of a removed water band were not eligible, because derivatives are artefact-prone there (Tsai and Philpot, 1998).',
      'A band found in both lists (same region or within ±10 nm) is a **robust** band (both tasks); scalogram-only → regression list; ReliefF-only → classification list.'])
FIG('scal', 'l_scal_relief.png', 'Correlation scalograms of R, FD and SD with plot PDI and ReliefF weights for six leaf grades; red points = bands kept (one per correlated region).', 560)
FIG('reg', 'l_regions.png', 'Band-to-band correlation of leaf reflectance with the correlated regions used for "one band per region".', 380)
L = max(len(t2['robust']), len(t2['regonly']), len(t2['clsonly']))
TAB('bands', [['Robust (both tasks)', 'Regression only', 'Classification only']] + [[(t2['robust'] + [''] * L)[i], (t2['regonly'] + [''] * L)[i], (t2['clsonly'] + [''] * L)[i]] for i in range(L)], [3100, 3100, 3106], 'Band lists from Tier 2 (R = reflectance, FD = first derivative, SD = second derivative; number = wavelength in nm).', 16)
Pp('Reflectance formed %d correlated regions (FD %d, SD %d). The scalogram gave %d candidates (%d after one band per region) and ReliefF %d (%d). The strongest correlation with PDI was for FD at %d nm (r = %s) and for reflectance at %d nm (r = %s). %d robust bands were found, all in the red edge and NIR shoulder (630–860 nm), mostly first and second derivatives. This agrees with the red-edge bands found for mustard stress by Shukla et al. (2024) (690–723 nm) and for leaf diseases by Mahlein et al. (2013), and with the known sensitivity of the red-edge slope to chlorophyll loss (Filella and Peñuelas, 1994). The regression list adds visible reflectance (640–700 nm) and SWIR derivatives (1595, 2040 nm), which follow the water and dry-matter changes in severely infected leaves.'
   % (t2['n_regions']['R'], t2['n_regions']['FD'], t2['n_regions']['SD'], t2['n_scal_cand'], t2['n_scal_reg'], t2['n_rel_cand'], t2['n_rel_reg'], t2['max_r']['FD'][1], f2(t2['max_r']['FD'][0]), t2['max_r']['R'][1], f2(t2['max_r']['R'][0]), len(t2['robust'])))
OUTB('%d robust, %d regression-only and %d classification-only bands.' % (len(t2['robust']), len(t2['regonly']), len(t2['clsonly'])))

H2('4.3 Tier 3: White Rust Index (WRI)')
STEP('Build an index specific to white rust that is more selective than general vegetation indices.',
     'Following Mahlein et al. (2013), WRI = ND(λ1, λ2) + w × R(λ3), with ND the normalised difference of two bands at least 50 nm apart and w ∈ {−1, −0.5, 0, 0.5, 1}. Bands were taken every 6 nm (VNIR 450–950 nm: %d bands, %d ND pairs). ReliefF weights for healthy (grade 0) vs diseased leaves selected the top 25%% of bands and of NDs, giving %s candidates. Each candidate was screened by its best balanced accuracy over all thresholds; the 30 best were then evaluated with an 8-fold stratified, plot-grouped cross-validation in which the threshold was fitted on the training folds only. The search was repeated for the SWIR (1000–2400 nm without water bands: %d bands, %s candidates).' % (t3['vnir']['n_bands'], t3['vnir']['n_pairs'], '{:,}'.format(t3['vnir']['n_cand']), t3['swir']['n_bands'], '{:,}'.format(t3['swir']['n_cand'])))
FIG('wri', 'l_wri.png', 'ReliefF weights of 6 nm bands for healthy vs diseased leaves (a) and the best VNIR (b) and SWIR (c) indices by leaf grade.', 560)
wv = pd.read_csv(D + 't_wri_vnir_top.csv').head(5); ws_ = pd.read_csv(D + 't_wri_swir_top.csv').head(3)
TAB('wri', [['Candidate index', 'Balanced accuracy (screening)', 'Balanced accuracy (8-fold CV)', 'CV SD']] + [[r[0], f3(r[1]), f3(r[2]), f3(r[3])] for r in wv.values] + [[r[0] + ' (SWIR)', f3(r[1]), f3(r[2]), f3(r[3])] for r in ws_.values],
    [3400, 2000, 2000, 1906], 'Best White Rust Index candidates (healthy vs diseased leaves).', 16)
Pp('The best index was **WRI = %s**, with a cross-validated balanced accuracy of %s (± %s). It decreases steadily from grade 0 (%.3f) to grade 9 (%.3f) and correlates with plot PDI at r = %s. The index contrasts the NIR plateau at 750 nm with 948 nm, the shoulder of the 970 nm water absorption, and subtracts reflectance at 696 nm on the red edge, so it combines structure, water and chlorophyll information. The best SWIR index (%s) was less accurate (%s), so the VNIR index was kept, as planned. The accuracy is lower than the 85–92%% reported for sugar-beet diseases (Mahlein et al., 2013) because grade 1 leaves with 1–5%% pustule cover are spectrally close to healthy leaves; a similar limit for early severity levels was reported for wheat leaf rust (Ashourloo et al., 2014).'
   % (t3['vnir']['formula'], f3(t3['vnir']['best']['ba_cv']), f3(t3['vnir']['best']['ba_cv_sd']), t3['grade_means']['0'], t3['grade_means']['9'], f2(np.corrcoef(Fp.WRI_VNIR, P.PDI)[0, 1]), t3['swir']['formula'], f3(t3['swir']['best']['ba_cv'])))
NOTE('The formula search used all leaves (as in Mahlein et al., 2013), while its threshold and accuracy were cross-validated. In Objective 2 the WRI is used only as a feature, and the WRI formula is the one limitation of the otherwise fully nested design (Section 5.1).')
OUTB('WRI = %s; balanced accuracy %s; r with PDI %s.' % (t3['vnir']['formula'], f2(t3['vnir']['best']['ba_cv']), f2(np.corrcoef(Fp.WRI_VNIR, P.PDI)[0, 1])))

H2('4.4 Tier 4: univariate response of features (ANOVA, Tukey HSD, Pearson r)')
STEP('Find which single features respond to white rust, in which direction, and how strongly.',
     'For every index, red-edge parameter, WRI and robust band, a one-way ANOVA across the six grades (leaves) gave F, p and the effect size η² = SS_between/SS_total; Tukey HSD gave the pairwise grade differences (Tukey, 1949; Gomez and Gomez, 1984). Pearson r with PDI was computed at plot level and Spearman ρ with the leaf grade (Spearman, 1904; Mahlein et al., 2019).',
     ['Leaves within a plot are not independent, so p-values are used only to rank features; effect sizes and r are interpreted.'])
top = A.head(15)
TAB('anova', [['Feature', 'Group', 'F', 'η²', 'r with PDI (plots)', 'ρ with grade (leaves)']] + [[r.Feature, r.Group, '%.0f' % r.F, f2(r.eta2), f2(r.r_PDI_plot), f2(r.rho_score_leaf)] for r in top.itertuples()],
    [1700, 1500, 1200, 1100, 1900, 1906], 'Fifteen features with the largest ANOVA F across the six leaf grades (all p < 0.001).', 15)
FIG('anovaf', 'l_anova.png', 'Six strongest features by leaf grade with Tukey HSD letters (grades sharing a letter do not differ).', 560)
sw = A[A.Group == 'SWIR index']
TAB('swir', [['SWIR index', 'F', 'η²', 'r with PDI']] + [[r.Feature, '%.0f' % r.F, f2(r.eta2), f2(r.r_PDI_plot)] for r in sw.itertuples()], [2400, 2300, 2300, 2306], 'Response of the nine SWIR disease indices.', 16)
FIG('rpdi', 'l_r_pdi.png', 'Plot-level relation between PDI and the four indices most correlated with it (colour = date).', 560)
sep6 = [k for k, l in t4['letters'].items() if len(set(l.values())) == 6 and all(len(v) == 1 for v in l.values())]
same01 = [k for k, l in t4['letters'].items() if set(l['0']) & set(l['1'])]
tukey_txt = ('In Tukey tests all six grades differed for %s; grades 0 and 1 were not separated for %s, which is expected when the lowest diseased grade covers only 1–5%% of the leaf.' % (', '.join(sep6) if sep6 else 'none of the features', ', '.join(same01) if same01 else 'none')).replace('%', '%%')
Pp('%d of %d features differed among grades at p < 0.001. The strongest were red-edge first derivatives (FD790, FD825, FD830; η² ≈ 0.34–0.37), the WRI and the red-edge second derivatives, followed by the vegetation stress index RVSI and the pigment indices HI and ARI. %s Among the SWIR indices, DWSI-5 responded most (F = %.0f, r = %s), followed by MSI, NDII and NDWI (|r| ≈ 0.59–0.63): infected leaves lose water, as reported for sugarcane orange rust (Apan et al., 2004), potato late blight (Kundu et al., 2021) and wheat Septoria blotch (Yu et al., 2018). Pigment indices (ARI, HI) increased with grade in the expected direction for chlorophyll loss and anthocyanin accumulation (Gitelson et al., 2001; Mahlein et al., 2013).'
   % (t4['n_sig'], t4['n_feat'], tukey_txt, sw.F.max(), f2(sw.r_PDI_plot.iloc[0])))
NOTE('Physiological correlation (chlorophyll, carotenoids, anthocyanin, relative water content) is part of Tier 4 in the methodology; it can be added when the pigment and water measurements are entered.')
OUTB('Ranked responding features with direction and Tukey groups; SWIR indices confirmed as responsive.')

H2('4.5 Tier 5: VIF and two-step stepwise canonical discriminant analysis')
STEP('Measure how well features together separate the six grades and which combination does it.',
     'Collinear features were removed until all VIF < 10 (Dormann et al., 2013). Forward stepwise discriminant analysis with Wilks\' lambda then entered the variable with the largest partial F at each step, with removal of variables that lost significance (Klecka, 1980). Because with 2339 leaves almost any variable is significant, the entry criterion was p < 0.001 with at most 10 variables (Whittingham et al., 2006). As in Stage III of Bhattacharya and Chattopadhyay (2013), step 1 used bands (classification band list) and step 2 the indices, red-edge parameters and WRIs. Canonical correlations, Wilks\' lambda, standardised coefficients and structure correlations describe the functions (Fisher, 1936); the separability was checked with LDA (equal priors) on the held-out replications.')
c1, c2 = t5['step1'], t5['step2']
TAB('cda', [['Quantity', 'Step 1: bands', 'Step 2: indices + red edge + WRI'],
            ['Variables in → after VIF < 10', '%d → %d' % (c1['n_in'], c1['n_vif']), '%d → %d' % (c2['n_in'], c2['n_vif'])],
            ['Selected variables', ', '.join(c1['selected']), ', '.join(c2['selected'])],
            ['Canonical r (functions 1, 2, 3)', ', '.join(f2(v) for v in c1['cancor'][:3]), ', '.join(f2(v) for v in c2['cancor'][:3])],
            ['Share of function 1', '%.0f%%' % (100 * c1['share'][0]), '%.0f%%' % (100 * c2['share'][0])],
            ["Wilks' lambda", f3(c1['wilks']), f3(c2['wilks'])],
            ['LORO accuracy / macro-F1', '%s / %s' % (f2(c1['acc']), f2(c1['macro_f1'])), '%s / %s' % (f2(c2['acc']), f2(c2['macro_f1']))],
            ['±1-grade accuracy', f2(c1['adj']), f2(c2['adj'])]], [2600, 3350, 3356], 'Results of the two-step stepwise CDA (six leaf grades).', 15)
FIG('cdaf', 'l_cda.png', 'Canonical score plots of the two steps (X = grade centroids).', 560)
Pp('Both steps produced one dominant canonical function (%.0f%% and %.0f%% of the discriminating variance; r₁ = %s and %s) along which the grade centroids are ordered 0 → 9: white rust acts as one severity axis in leaf spectra. Six-grade LDA accuracy on held-out replications was %s and %s (chance ≈ 0.17–0.24), while %s and %s of leaves were classified within one grade, so most errors are between neighbouring grades. The two steps give similar separability, so bands and indices carry largely the same information; step 2 retained REP, DWSI-4, NPQI, water indices and NDBI, i.e. red-edge, pigment and water features together, as Bhattacharya and Chattopadhyay (2013) found for mustard rot (DWSI-1, DWSI-4, ROTI). Zhang et al. (2012a) likewise found that discriminant analysis separates disease presence well but severity levels less well.'
   % (100 * c1['share'][0], 100 * c2['share'][0], f2(c1['cancor'][0]), f2(c2['cancor'][0]), f2(c1['acc']), f2(c2['acc']), f2(c1['adj']), f2(c2['adj'])))
OUTB('One severity axis; linear six-grade separability ≈ %s; discriminating bands and indices.' % f2(max(c1['acc'], c2['acc'])))

H2('4.6 Tier 6: Boruta disease-specific feature pools')
STEP('Select all relevant features for each task with one formal, non-linear rule.',
     'Boruta compares the random-forest importance of each feature with that of shuffled "shadow" copies and confirms features that beat the best shadow significantly (alpha = 0.01, up to 100 iterations; Kursa and Rudnicki, 2010). It was run for classification on leaves (classification bands + 53 features) and for regression on plots (regression bands + 53 features), as in Mustafa et al. (2023).')
FIG('bor', 'l_boruta.png', 'Boruta decisions and random-forest importance for classification (left) and regression (right).', 560)
Pp('Boruta confirmed %d of %d features for classification and %d of %d for regression. The classification pool is led by FD825, HI, the WRI, FD830, FD790 and ARI, i.e. red-edge derivatives plus pigment indices; the regression pool is dominated by the WRI, followed by reflectance at 695 nm, FD860 and DWSI-5. The agreement with the ANOVA ranking and with the CDA variables shows that the same red-edge, pigment and water features are selected by linear and non-linear methods.' % (len(t6['cls']['confirmed']), t6['cls']['n_in'], len(t6['reg']['confirmed']), t6['reg']['n_in']))
TAB('dsf', [['Pool', 'Confirmed features'], ['Classification (%d)' % len(t6['cls']['confirmed']), ', '.join(t6['cls']['confirmed'])], ['Regression (%d)' % len(t6['reg']['confirmed']), ', '.join(t6['reg']['confirmed'])]], [2200, 7106], 'Leaf-level disease-specific feature (DSF) pools.', 15)
OUTB('Two DSF pools: classification and regression.')

# ================= 5 OBJECTIVE 2 =================
H1('5. Objective 2: six-grade classification and PDI regression')
H2('5.1 Nested validation design')
STEP('Estimate how well white-rust severity can be predicted for new plots, without optimistic bias.',
     'In each of the three LORO folds, all selection steps were repeated on the training replications only: Tier 2 band lists → Boruta → VIF < 10 → ML-SFFS for each model (Pudil et al., 1994) → hyperparameter tuning → prediction of the held-out replication. Selecting features on all data and testing afterwards would inflate accuracy (Ambroise and McLachlan, 2002; Varma and Simon, 2006).',
     ['ML-SFFS: forward selection with floating removal, criterion macro-F1 (classification) or RMSE (regression) in a 3-fold plot-grouped inner CV; up to 8 features; the smallest subset within 0.01 (2% for RMSE) of the best (Tian et al., 2021).',
      'Classifiers: SVM with RBF kernel (Cortes and Vapnik, 1995), random forest (Breiman, 2001), k-NN (Cover and Hart, 1967), all with class weights; a small MLP (16–8 units) on the VIF-filtered Boruta pool (Rumelhart et al., 1986).',
      'Regressors: SVR, RFR, k-NN, PLSR (Wold et al., 2001) and MLP.',
      'Baselines without the selection chain: PLS-DA/PLSR on the full 349-band reflectance spectrum (Shukla et al., 2024) and RF on all 53 features.',
      'Bottom-up PDI: the predicted grades of the leaves of a plot-date were turned into PDI with the same formula and compared with the observed PDI.'])
fr = [['Test replication', 'Bands (C / R)', 'Boruta (C / R)', 'After VIF (C / R)', 'SVM features', 'Best regressor (%s) features' % br]]
for f in R2['folds']:
    fr.append([f['test_rep'], '%d / %d' % (f['n_cls_bands'], f['n_reg_bands']), '%d / %d' % (f['boruta_cls'], f['boruta_reg']), '%d / %d' % (len(f['vif_cls']), len(f['vif_reg'])), ', '.join(f['ofc']['SVM']['features']), ', '.join(f['ofc'].get('R_' + br, f['ofc']['R_SVR'])['features'])])
TAB('folds', fr, [1100, 1100, 1100, 1100, 2450, 2456], 'Nested selection in each training fold (C = classification, R = regression).', 14)
FIG('sffs', 'l_sffs.png', 'ML-SFFS curves on the training data of fold 1 (inner-CV score against the number of features).', 520)

H2('5.2 Six-grade leaf classification')
cr = [['Model', 'OA', 'Kappa', 'Macro-F1', '±1 grade', 'Healthy vs diseased']] + [[k, f2(v['oa']), f2(v['kappa']), f2(v['macro_f1']), f2(v['adj']), f2(v['detection_acc'])] for k, v in rc.items()]
TAB('cls', cr, [3100, 1100, 1100, 1300, 1300, 1406], 'Classification of six leaf grades on held-out replications (2339 leaves).', 15)
FIG('models', 'l_models.png', 'Model comparison: six-grade classification (a) and PDI regression (b).', 560)
v = rc[bc]
TAB('pergrade', [['Grade'] + [str(g) for g in G6], ['Precision'] + [f2(q) for q in v['P']], ['Recall'] + [f2(q) for q in v['R']], ['F1'] + [f2(q) for q in v['F1']]], [1606] + [1283] * 6, 'Per-grade precision, recall and F1 of the best classifier (%s).' % bc, 16)
Pp('The best classifier, %s, reached overall accuracy %s, kappa %s and macro-F1 %s; %s of leaves were placed in the correct or an adjacent grade, and healthy vs diseased leaves were separated with %s accuracy. Grade 0 was recognised best (F1 %s) and grade 3 worst (F1 %s); diseased leaves of grades 1–5 were often predicted as a neighbouring grade, and grade 9 leaves were partly predicted as 5 or 7. The selection chain was better than the full-spectrum PLS-DA (macro-F1 %s) and as accurate as RF on all 53 features (macro-F1 %s) while using only %d–%d features, which makes the model interpretable and transferable to sensors with fewer bands. Similar or lower exact accuracies have been reported for multi-level severity: 70%% for three yellow-rust levels (Meng et al., 2020), 81.8%% for severity vs 93.1%% for detection (Lv et al., 2023), and poor separation of adjacent blast grades on the 0–9 scale (Mandal et al., 2023).'
   % (bc, f2(v['oa']), f2(v['kappa']), f2(v['macro_f1']), f2(v['adj']), f2(v['detection_acc']), f2(v['F1'][0]), f2(v['F1'][2]), f2(rc['PLS-DA (full spectrum)']['macro_f1']), f2(rc['RF (all 53 features)']['macro_f1']), min(len(f['ofc'][bc]['features']) for f in R2['folds']), max(len(f['ofc'][bc]['features']) for f in R2['folds'])))
FIG('eval', 'l_eval.png', 'Confusion matrix of the best classifier (a) and observed vs predicted plot PDI (b) on held-out replications.', 560)

H2('5.3 Plot-level PDI regression')
rg = [['Model', 'R²', 'RMSE (PDI %)', 'NRMSE', 'RPD']] + [[k, f2(q['r2']), '%.1f' % q['rmse'], f2(q['nrmse']), f2(q['rpd'])] for k, q in rr.items()]
TAB('reg', rg, [3800, 1300, 1500, 1300, 1406], 'PDI regression on held-out replications (192 plot-dates).', 15)
Pp('The best regressor, %s, predicted plot PDI with R² = %s, RMSE = %.1f PDI units and RPD = %s, close to the value of 2 above which spectral models are usually considered accurate for quantitative prediction (Chang et al., 2001). The PDI estimated bottom-up from the predicted leaf grades reached R² = %s, showing that the leaf classifier is consistent with plot severity even though its exact grade accuracy is modest. Plot-level regression is more accurate than leaf grading because averaging leaves removes much of the within-plot noise; this supports the methodology\'s choice of PDI regression as a parallel task to classification (Liu et al., 2024; Feng et al., 2022).'
   % (br, f2(rr[br]['r2']), rr[br]['rmse'], f2(rr[br]['rpd']), f2(rr[bu]['r2'])))

H2('5.4 Performance by date and variety')
bd = [['Date', 'OA (grades)', 'Macro-F1 (grades)', 'R² (PDI)', 'RMSE (PDI)']] + [[d, f2(q['oa']), f2(q['macro_f1']), (f2(q['r2']) if q['r2'] is not None else '—'), '%.1f' % q['rmse']] for d, q in R2['by_date'].items()]
TAB('bydate', bd, [1900, 1800, 1900, 1800, 1906], 'Best models per sampling date.', 16)
TAB('byvar', [['Variety', 'Macro-F1 (grades)', 'R² (PDI)']] + [[k, f2(q['macro_f1']), f2(q['r2'])] for k, q in R2['by_variety'].items()], [3100, 3100, 3106], 'Best models per variety.', 16)
Pp('Per-date R² depends on the spread of PDI on that date: on 11 February most leaves were grade 0–1 and PDI varied little (0–24%), so R² is not meaningful (negative) although the RMSE is the smallest (about 7 PDI units). Performance was similar for the three varieties, so the features are not variety-specific.')

# ================= 6 DISCUSSION =================
H1('6. Discussion: how the results support the methodology')
BL(['**Red edge as the core white-rust signal.** Tiers 2, 4, 5 and 6 independently selected red-edge first and second derivatives (680–860 nm). Pustules and chlorosis reduce chlorophyll and disturb mesophyll structure, which lowers and shifts the red-edge slope (Horler et al., 1983; Filella and Peñuelas, 1994); Shukla et al. (2024) found 690–723 nm for mustard aphid stress and Mahlein et al. (2013) red-edge bands for sugar-beet diseases.',
    '**Disease-specific index.** The WRI combines NIR structure, water (948 nm) and red-edge reflectance and was the single best regression feature, in line with disease-specific indices outperforming general indices (Mahlein et al., 2013; Ashourloo et al., 2014; Meng et al., 2020).',
    '**SWIR adds water information.** DWSI-5, MSI, NDII and NDWI responded with |r| ≈ 0.6 to PDI, as reported for rust and blotch diseases (Apan et al., 2004; Yu et al., 2018), and DWSI-5 entered the regression DSF pool; the SWIR WRI was weaker than the VNIR WRI, so SWIR is complementary rather than primary.',
    '**Class overlap.** Exact six-grade accuracy is limited (macro-F1 about 0.3), but ±1-grade accuracy (about 0.73) and PDI regression (R² about 0.74) are much better. This justifies reporting ±1-grade accuracy and keeping PDI regression in the methodology (Mandal et al., 2023; Lv et al., 2023).',
    '**Nested selection.** Repeating Tier 2, Boruta, VIF and ML-SFFS inside each training replication gave compact, interpretable models whose accuracy is an honest estimate for new plots (Varma and Simon, 2006); the features recurring across folds (red-edge derivatives, WRI, pigment and water indices) are the stable white-rust features.'])

H1('7. Conclusions and implications for the UAV analysis')
BL(['The red edge (680–860 nm), and its derivatives in particular, should be the priority region in the UAV hyperspectral band selection; the MS red-edge band (717 nm) is expected to be the most useful multispectral band.',
    'The leaf WRI (%s) should be tested on UAV canopy spectra; it may need recalibration because canopy spectra add soil, shadow and flowers.' % t3['vnir']['formula'],
    'PDI regression is the more reliable severity output; six-grade classification should be reported with ±1-grade accuracy.',
    'SWIR water indices (DWSI-5, MSI, NDII, NDWI) are worth computing from the UAV SWIR sensor as complementary features.',
    'The same nested selection chain (Tier 2 → Boruta → VIF → ML-SFFS) can be used unchanged for the UAV data.'])
H2('7.1 Limitations')
BL(['Leaf spectra are an upper bound for canopy performance (no soil, shadow or illumination effects; Mahlein, 2016).', 'The WRI formula was searched on all leaves; only its threshold was cross-validated.', 'p-values of leaf-level ANOVA are optimistic because leaves within plots are not independent; they were used only to rank features.', 'One season and one site; independent validation (Bharatpur) is still required.'])

H1('8. Interview questions on the leaf analysis')
QA('Why analyse leaf spectra when the thesis is about UAVs?', 'Leaf spectra show the pure disease signal without soil, shadow, flowers or illumination; they tell which wavelengths and indices to look for in the UAV data (Mahlein et al., 2012).')
QA('Why is exact six-grade accuracy only moderate?', 'Grades are cuts of a continuous severity; grades 0 and 1 differ by 1–5%% leaf area and neighbouring grades overlap spectrally. ±1-grade accuracy was %s and PDI regression R² %s (Mandal et al., 2023).' % (f2(rc[bc]['adj']), f2(rr[br]['r2'])))
QA('How did you avoid over-optimistic accuracy?', 'Every selection step was repeated inside the training replications and the test replication was used only once (Varma and Simon, 2006).')
QA('Which features matter most and why?', 'Red-edge derivatives (chlorophyll loss and structure), the WRI, pigment indices (HI, ARI) and SWIR water indices (DWSI-5), consistent with Horler et al. (1983) and Apan et al. (2004).')
QA('Why remove derivative bands near 1000 nm and the water bands?', 'The ASD detector splice and the edges of removed bands create artificial derivative peaks (Tsai and Philpot, 1998; Hueni and Bialek, 2017).')

open(D + 'docx_body.js', 'w').write('\n'.join(K))
print('body lines', len(K))
