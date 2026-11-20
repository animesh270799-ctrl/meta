// ======================= FRONT =======================
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 900, after: 160 }, children: [new TextRun({ text: 'Objective 1: Characterise white rust of mustard through multimodal UAV sensing', font: FONT, size: 40, bold: true, color: '1E3A1F' })] }));
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: 'Tier-wise, sensor-wise methodology (hyperspectral, multispectral, RGB, thermal)', font: FONT, size: 28, color: '2C5F2D' })] }));
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 500 }, children: [new TextRun({ text: 'Ph.D. (Agricultural Physics), ICAR-IARI  |  AI-based multimodal UAV sensing of white rust in mustard', font: FONT, size: 20, italics: true, color: '555555' })] }));
K.push(NOTE(`**How this document is organised.** Methods used by several sensors (univariate statistics, VIF, canonical discriminant analysis, Boruta) are described **once** in Chapter 3 (Methods M1–M4). Each sensor chapter then gives its tiers in detail; where a tier uses a common method, only the sensor-specific input, expectations, dummy results and output are given. Every tier has the same parts: **Position**, **Problem solved by this tier**, **Concept**, **Why it is needed at this position**, **Why this method in my case**, **What the reference papers used**, **Alternatives** (table), **How it is done**, **How it is used with my data**, **dummy figure/table**, **Output**, **Interview questions** and **References**. All dummy data are simulated and only show what results will look like.`));
K.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-2' }));
K.push(new Paragraph({ children: [new PageBreak()] }));

// ======================= 1 OVERVIEW =======================
K.push(H1('1. Objective 1 at a glance'));
K.push(P(`**Objective 1 (ORW):** to characterise white rust of mustard through multimodal sensing from a UAV platform. It answers six questions for each sensor: (Q1) which features change with white rust and in which direction; (Q2) which hyperspectral wavelengths respond; (Q3) can a white-rust-specific index be built; (Q4) how well do the features together separate the six severity grades; (Q5) which features are relevant for grade classification and for PDI regression; (Q6) are the sensors complementary? The answers form the input of Objectives 2 and 3.`));
K.push(...fig2('tiers', 'o1_tiers.png', 'Tier structure of Objective 1. Sensor-specific tiers (Tier 1 for every sensor; Tiers 2–3 for HS only) are followed by tiers that apply the common methods M1–M4 to each sensor, and a final cross-sensor tier.', 520));
K.push(...tab2('tiermap', [
  ['Tier', 'Problem solved', 'Method', 'Output'],
  ['Tier 0 (all)', 'Need labelled, comparable plot-level data', 'Grade by 0–9 key; PDI; pooled table; training replications', 'Labelled plot-date table'],
  ['Tier 1 (each sensor)', 'Images are not features; models need physically meaningful numbers', 'Sensor-specific feature extraction', 'HS 1494, MS 57, RGB 29, TIR 13 features'],
  ['HS Tier 2', '1443 redundant band features, more than the plots', 'Correlation scalogram + ReliefF; one band per correlated region', 'Robust white-rust bands'],
  ['HS Tier 3', 'General indices also respond to other stresses', 'White Rust Index (Mahlein 2013)', 'WRI'],
  ['HS Tier 4; MS/RGB/TIR Tier 2', 'Which single features respond, how and why', 'M1: ANOVA + Tukey; Pearson r; physiology', 'Responding features with direction'],
  ['HS Tier 5; MS/RGB/TIR Tier 3', 'How well features together separate the six grades', 'M2 VIF + M3 stepwise CDA', 'Separability, severity axis, overlap'],
  ['HS Tier 6; MS/RGB/TIR Tier 4', 'Formal, task-specific feature pools for modelling', 'M4: Boruta', '2 DSF pools per sensor'],
  ['Cross-sensor tier', 'Do sensors carry different information?', 'DSF correlation matrix; optional combined CDA', 'Complementarity; 8 DSF pools to Obj. 2–3'],
], [1900, 2700, 2600, 2106], 'What each tier solves, how and with what output.', 15));

// ======================= 2 TIER 0 =======================
K.push(H1('2. Tier 0: common inputs (all sensors)'));
TIER({ title: 'Tier 0. Plot-level data, severity grades and validation rule',
 pos: `Before every tier of every sensor; all later tiers use these labels and rules.`,
 problem: `Features can only be linked to white rust if every plot-date has a reliable severity label and if the same data rules apply to every sensor.`,
 concept: `Each plot is graded from the **mean percentage of leaf area covered by pustules** with the 0–9 key (Conn et al., 1990): grade 0 = no pustules, 1 = 1–5%, 3 = 6–10%, 5 = 11–25%, 7 = 26–50%, 9 = > 50%. The six grades are the classes. The **percent disease index (PDI)** summarises the leaf grades of a plot for regression:`,
 eqs: [EQ('PDI (%) = [ Σ (grade × number of leaves with that grade) / (total leaves × 9) ] × 100', 'e:pdi')],
 need: `Every statistical test, discriminant analysis and feature selection in Objective 1 compares features against these grades or against PDI.`,
 why: `The 0–9 key with odd grades is the standard assessment key for rapeseed–mustard foliar diseases in India (Conn et al., 1990); grading from leaf-area percentage gives ordered classes that agree with the continuous PDI, so the same scoring serves classification and regression. Pooling all post-symptomatic dates gives all grades in one dataset (Liu et al., 2024).`,
 papers: [`Conn et al. (1990): 0–9 key for rapeseed–mustard leaf disease (0, 1, 3, 5, 7, 9 by % leaf area).`, `Liu et al. (2024): disease index from a multi-point survey and one model for five pooled dates.`, `Shukla et al. (2024): 1–5 grade for mustard aphid; Mandal et al. (2023): IRRI 0–9 scale for rice blast.`],
 alts: TAB('alt0', [['Alternative', 'How it works / used by', 'Why not used here'], ['0–6 leaf-area scale', 'Seven classes of leaf area (used in the earlier plan)', 'The experiment is scored with the 0–9 key; using it keeps field scoring and analysis identical'], ['Fixed DI bands (e.g. ≤ 25, 25–50, > 50%)', 'Few broad classes from DI', 'Coarser than the field key; the grades of the key are the agreed classes'], ['Image-based severity', 'Pixel classification of pustules on close-range images (Bock et al., 2010)', 'Needs extra imaging of every plot; visual key is the reference of the ORW']], [2200, 3800, 3306], 'Alternatives for the severity labels.', 16),
 how: [`Five sampling points per plot; fully expanded leaves graded 0, 1, 3, 5, 7, 9; plot grade from the plot mean % leaf area; PDI from all graded leaves.`, `Pooled table of post-symptomatic plot-dates (8 flights in total; dates before symptoms go to Objective 3).`, `Every data-driven choice in Objective 1 that later feeds models is made on the training replications (leave-one-replication-out).`],
 mine: `Dummy example: 432 post-symptomatic plot-dates with unequal grade sizes (130, 90, 60, 70, 50, 32 for grades 0–9), so tests and models use equal class weighting where needed.`,
 vis: [TAB('key', [['Grade', 'Leaf area with pustules', 'Description'], ['0', '0%', 'Healthy, no pustules'], ['1', '1–5%', 'Few small pustules'], ['3', '6–10%', 'Scattered pustules'], ['5', '11–25%', 'Many pustules, chlorosis'], ['7', '26–50%', 'Large pustule area, chlorosis/necrosis'], ['9', '> 50%', 'Severe; leaves heavily covered']], [1500, 3000, 4806], '0–9 severity key used for plot grades (Conn et al., 1990).', 17), FIG('classes', 'o1_classes.png', 'Dummy plot % leaf area with the key limits (a) and grade sizes (b).', 540)],
 out: `Labelled table: plot-date × features (from Tier 1) × grade (0, 1, 3, 5, 7, 9) × PDI × physiology × plot ID × replication.`,
 qs: [[`Why six grades?`, `They are the grades of the standard 0–9 key used to score the field; using them directly avoids re-binning and keeps the agronomic meaning.`], [`Why both grades and PDI?`, `Grades are the management classes; PDI keeps the continuous information and is used for correlation scalograms and regression.`]],
 refs: `Conn et al. (1990); Liu et al. (2024); Bock et al. (2010).` });

// ======================= 3 COMMON METHODS =======================
K.push(H1('3. Common methods used in several tiers (described once)'));
K.push(P(`The four methods below are applied to every sensor. They are explained here once; the sensor chapters only give the sensor-specific input, expected responses, dummy results and outputs.`));
TIER({ title: 'Method M1. Univariate response: ANOVA + Tukey HSD and Pearson r',
 pos: `Used in HS Tier 4 and in MS, RGB and TIR Tier 2, after feature extraction.`,
 problem: `Before combining features, one must know which single features change with white rust, in which direction, between which grades and why.`,
 concept: `**One-way ANOVA** tests whether the mean of a feature differs among the six grades; **Tukey's HSD** then shows which pairs of grades differ (letters a, b, c …: grades sharing a letter do not differ). **Pearson's r** measures how strongly the feature changes with PDI. Correlation with physiological measurements explains the change.`,
 need: `It gives the physiological characterisation required by Objective 1 and a transparent first ranking before multivariate methods.`,
 why: `ANOVA + Tukey is the standard, easily explained test for several treatment groups in agricultural research (Gomez and Gomez, 1984; Tukey, 1949), and Pearson r is the simplest measure of association; both are used in the reference papers.`,
 papers: [`Mahlein et al. (2019): Tukey HSD between groups and Pearson r with disease severity.`, `Liu et al. (2024): Dunnett test of features between disease levels.`, `Zhang et al. (2012a): t-test and correlation of 32 spectral features with severity.`, `Guo et al. (2021): features kept if significantly correlated with DI (p < 0.01).`],
 alts: TAB('altm1', [['Alternative', 'How it works / used by', 'Why not used here'], ['Kruskal–Wallis + Dunn', 'Rank-based ANOVA and pairwise test (Kruskal and Wallis, 1952; Dunn, 1964)', 'Kept only for strongly non-normal features; ANOVA is simpler to present'], ['Spearman ρ', 'Rank correlation (Spearman, 1904; Shukla et al., 2024)', 'Used only if the relation is clearly non-linear'], ['Linear mixed model', 'Plot as random effect for repeated dates (Zuur et al., 2009)', 'More complex; p-values here only rank features, models are validated on held-out plots'], ['t-test per pair', 'Two groups at a time (Zhang et al., 2012a)', 'Six grades need a multi-group test']], [2000, 3900, 3406], 'Alternatives to Method M1.', 16),
 how: [`One-way ANOVA of each feature across grades 0, 1, 3, 5, 7, 9; Tukey HSD for all pairs.`, `Pearson r with PDI; correlation with chlorophyll a, b, carotenoid, anthocyanin, relative water content, stomatal conductance and transpiration.`, `p-values are used only to rank and describe, because repeated plot-dates are not independent.`],
 mine: `One results table per sensor (feature, ANOVA F, p, r with PDI) and one boxplot figure with Tukey letters (sensor chapters).`,
 vis: [],
 out: `Per sensor: which features respond, direction, separated grade pairs, r with PDI and physiological meaning.`,
 qs: [[`Why ANOVA and not t-tests?`, `There are six grades; repeated t-tests inflate errors, ANOVA tests all grades at once and Tukey HSD controls the pairwise error.`], [`What do the Tukey letters mean?`, `Grades sharing a letter are not significantly different; different letters mean the feature separates them.`]],
 refs: `Gomez and Gomez (1984); Tukey (1949); Mahlein et al. (2019); Liu et al. (2024).` });

TIER({ title: 'Method M2. Variance inflation factor (VIF)',
 pos: `Used before canonical discriminant analysis (HS Tier 5; MS, RGB, TIR Tier 3).`,
 problem: `Near-duplicate features (e.g. several NDVI variants, neighbouring bands) make the discriminant calculation unstable or impossible.`,
 concept: `VIF measures how well a feature is predicted by the other features; features with the largest VIF are removed one at a time until all VIF < 10 (i.e. less than 90% of a feature is explained by the others).`,
 eqs: [EQ('VIF_{j} = 1 / (1 − R_{j}^{2})', 'e:vif')],
 need: `Canonical discriminant analysis needs an invertible within-class covariance matrix, which collinear features prevent.`,
 why: `VIF < 10 is the threshold used before feature selection in the reference papers (Tian et al., 2021; Mustafa et al., 2023) and is simple to explain.`,
 papers: [`Tian et al. (2021): VIF < 10 before ML-SFFS.`, `Mustafa et al. (2023): VIF < 10 after Boruta.`],
 alts: TAB('altm2', [['Alternative', 'How it works / used by', 'Why not used here'], ['Correlation threshold (|r| > 0.9)', 'Drop one of each highly correlated pair', 'Looks at pairs only, misses multi-feature collinearity'], ['PCA', 'Uncorrelated components (Jolliffe, 2002)', 'Loses the original, interpretable features'], ['Regularised discriminant analysis', 'Shrinks the covariance matrix (Friedman, 1989)', 'Less interpretable; VIF is simpler']], [2400, 3500, 3406], 'Alternatives to Method M2.', 16),
 how: [`Compute VIF for every input feature; remove the largest; recompute; stop when all VIF < 10.`],
 mine: `Applied separately to each CDA input set (HS bands; HS indices + WRI; MS, RGB, TIR features).`,
 vis: [],
 out: `A non-redundant input set for CDA.`,
 qs: [[`Why 10?`, `VIF 10 means 90% of a feature is explained by the others; it is the usual threshold and the one used by Tian et al. (2021) and Mustafa et al. (2023).`]],
 refs: `Tian et al. (2021); Mustafa et al. (2023).` });

TIER({ title: 'Method M3. Stepwise canonical discriminant analysis (CDA)',
 pos: `Used in HS Tier 5 (two steps) and in MS, RGB and TIR Tier 3 (one step), after M1 and M2.`,
 problem: `M1 looks at one feature at a time; Objective 1 also needs to know how well a sensor separates the six grades when its features act together, which combination forms the severity axis and where grades overlap.`,
 concept: `CDA builds canonical functions z = w_{1}x_{1} + … + w_{k}x_{k} so that grade means are as far apart as possible relative to the spread within grades (Fisher, 1936); with six grades there are up to five functions, and the first usually orders the grades along a severity axis. In the stepwise form features enter one at a time if they reduce **Wilks' lambda** (0 = grades separated, 1 = not separated) and leave if they no longer contribute. The **canonical correlation** (0–1) shows how strongly a function is linked to the grades. The same functions classify held-out plots (the LDA side), giving a linear baseline accuracy.`,
 need: `It adds what no other tier gives: one comparable separability value per sensor, an interpretable severity axis and a picture of grade overlap.`,
 why: `It is the method used for mustard disease classes by Bhattacharya and Chattopadhyay (2013, SAC-ISRO), with a first step on bands and a second on indices; it is interpretable and easy to present with a score plot.`,
 papers: [`Bhattacharya and Chattopadhyay (2013): two-step stepwise canonical discriminant analysis — 25 Hyperion bands, then indices (ROTI, DRI, DWSI) — for mustard rot classes.`, `Zhang et al. (2012a): Fisher discriminant analysis for three powdery-mildew severity levels.`, `Tian et al. (2021): linear discriminant classifier within ML-SFFS.`],
 alts: TAB('altm3', [['Alternative', 'How it works / used by', 'Why not used here'], ['PLS discriminant analysis', 'PLS with class dummies (Barker and Rayens, 2003)', 'Latent components less directly interpretable'], ['Quadratic / regularised DA', 'Unequal covariances or shrinkage (Das et al., 2020; Friedman, 1989)', 'More parameters for six grades; linear CDA is simpler'], ['JM distance', 'Pairwise class separability 0–2 (Das et al., 2020; Mandal et al., 2023)', 'Pairwise only; CDA gives one multivariate picture'], ['t-SNE / UMAP', 'Non-linear visualisation (Ramalingam et al., 2026)', 'No interpretable weights or test']], [2200, 3800, 3306], 'Alternatives to Method M3.', 16),
 how: [`Input after M2; equal prior weight for the six grades; entry p < 0.05, removal p > 0.10.`, `Report canonical correlation of function 1, Wilks' lambda, feature weights, score plot (function 1 vs 2), held-out accuracy.`],
 mine: `Results for each sensor are given in its Tier 3 (HS Tier 5) with a dummy score plot.`,
 vis: [],
 out: `Per sensor: discriminating features, canonical correlation, Wilks' lambda, weights, score plot and baseline accuracy.`,
 qs: [[`CDA or LDA?`, `The same Fisher method: CDA describes the separation, LDA classifies with the same functions; I use CDA and report its accuracy as a baseline.`], [`Why stepwise?`, `To keep only features that add separation, giving a short interpretable set; its p-values are optimistic, so accuracy is judged on held-out plots (Whittingham et al., 2006).`]],
 refs: `Fisher (1936); Bhattacharya and Chattopadhyay (2013); Zhang et al. (2012a); Whittingham et al. (2006).` });

TIER({ title: 'Method M4. Boruta (disease-specific feature pools)',
 pos: `Used in HS Tier 6 and in MS, RGB and TIR Tier 4; last tier of each sensor. Its pools go to the cross-sensor tier and to Objectives 2 and 3.`,
 problem: `Earlier tiers describe the signal but do not give a formal, task-specific set of features for modelling, with one rule for all sensors and including non-linear relevance.`,
 concept: `Boruta copies every feature and shuffles the copies ("shadow" features, which carry no information), fits a random forest repeatedly and keeps a feature only if it is significantly more important than the best shadow; features are confirmed, tentative or rejected (Kursa and Rudnicki, 2010).`,
 need: `It is the only step that produces the disease-specific feature (DSF) pools that Objectives 2 and 3 use.`,
 why: `Boruta is all-relevant (keeps every feature related to white rust, which suits characterisation), captures non-linear and interacting effects, gives a statistical cut-off instead of an arbitrary top-k, and is the first step of the Boruta → VIF → ML-SFFS chain of Mustafa et al. (2023).`,
 papers: [`Mustafa et al. (2023): Boruta to select disease-specific features from three sensors before VIF and ML-SFFS.`, `Liu et al. (2024): recursive feature elimination; Feng et al. (2022): SPA (alternatives).`],
 alts: TAB('altm4', [['Alternative', 'How it works / used by', 'Why not used here'], ['Recursive feature elimination', 'Repeatedly drop the least important feature (Guyon et al., 2002; Liu et al., 2024)', 'Needs a chosen subset size; minimal-optimal rather than all-relevant'], ['LASSO / elastic net', 'Penalised regression selects features (Tibshirani, 1996; Zou and Hastie, 2005)', 'Linear; unstable with correlated features'], ['mRMR', 'Mutual-information relevance minus redundancy (Peng et al., 2005)', 'Needs a chosen number of features'], ['SHAP ranking', 'Model-based contribution (Lundberg and Lee, 2017)', 'A ranking, not a selection rule']], [2300, 3800, 3206], 'Alternatives to Method M4.', 16),
 how: [`Random forest with 500 trees, up to 100 runs, p = 0.01; run twice per sensor: six-grade classification and PDI regression.`, `Confirmed features = DSF pool; tentative features are reported.`],
 mine: `Two DSF pools per sensor (eight in total); dummy results in each sensor chapter.`,
 vis: [],
 out: `DSF pools for classification and regression for each sensor.`,
 qs: [[`What are shadow features?`, `Shuffled copies of the real features; a real feature must beat the best of them to be confirmed.`], [`Why Boruta after ANOVA and CDA?`, `ANOVA is univariate and linear, CDA keeps a minimal linear set; Boruta gives all relevant features of every sensor with one rule and non-linear relevance, which the models need.`]],
 refs: `Kursa and Rudnicki (2010); Mustafa et al. (2023).` });

// ======================= 4 HS =======================
K.push(H1('4. Hyperspectral sensor (HS)'));
K.push(P(`The hyperspectral sensor covers 400–2500 nm (VNIR + SWIR) and is the only sensor with band-level tiers and a disease-specific index. ${F('flowHS')} shows its six tiers.`));
K.push(...fig2('flowHS', 'o1_flow_HS.png', 'Flow chart of Objective 1 for the hyperspectral sensor.', 520));
TIER({ title: 'HS Tier 1. Feature extraction',
 pos: `After Tier 0 and pre-processing; before HS Tiers 2–6.`,
 problem: `A hyperspectral cube must be turned into plot-level spectra and physically meaningful features.`,
 concept: `The plot spectrum is the mean of the crop endmembers of the plot; from it come band reflectances (R), first and second derivatives (FD, SD), red-edge parameters and narrow-band indices (pigment, structure, water).`,
 eqs: [EQ('REP = argmax_{680–750 nm} FD(λ);   Dr = max FD;   SDr = Σ_{680–750 nm} FD(λ) Δλ', 'e:rep')],
 need: `All later HS tiers work on this feature table.`,
 why: `Endmember averaging removes residual soil–canopy mixing (Keshava and Mustard, 2002); derivatives remove offsets and show red-edge shifts (Tsai and Philpot, 1998); the 39 base indices are those of the ORW plus disease-related indices from the papers, and 9 further SWIR indices come from disease studies (rust, blotch, late blight, rice blast), because white rust also changes leaf water and dry matter, which only the SWIR sees (Apan et al., 2004; Yu et al., 2018).`,
 papers: [`Guo et al. (2021): 15 narrow-band indices from UAV hyperspectral data.`, `Shukla et al. (2024): reflectance, first and second derivatives of mustard canopy spectra.`, `Bhattacharya and Chattopadhyay (2013): SWIR disease–water indices (DWSI, ROTI) for mustard.`, `Apan et al. (2004): disease–water stress indices DWSI-1 to DWSI-5 (1660 nm) for sugarcane orange rust from Hyperion; Kundu et al. (2021): DWSI correlated with potato late blight severity (r ≈ −0.84).`, `Yu et al. (2018): NDWI (860/1240 nm) was the best index for Septoria tritici blotch in 335 wheat varieties.`, `Mandal et al. (2023) and Ramalingam et al. (2026), ICAR-IARI: rice blast indices from SWIR bands (1148/1301 nm for severity on the 0–9 scale; 1068/1560 nm for early detection).`],
 alts: TAB('althst1', [['Alternative', 'How it works / used by', 'Why not used here'], ['Mean of all canopy pixels', 'Simple plot mean', 'Keeps mixing with soil; reported as a check'], ['Continuous wavelet features', 'Multi-scale spectral features (Tian et al., 2021; Lv et al., 2023)', 'Many extra features; derivatives are simpler'], ['PROSAIL inversion', 'Retrieve chlorophyll, water, LAI (Jacquemoud et al., 2009)', 'Needs model calibration; indices are direct'], ['Continuum removal', 'Absorption band depth (Kokaly and Clark, 1999)', 'Optional; red-edge parameters and indices cover the main features']], [2200, 3800, 3306], 'Alternatives for HS feature extraction.', 16),
 how: [`Plot spectrum: 30 endmembers per plot; soil, shadow and flower endmembers removed; crop endmembers averaged.`, `Remove 1350–1450 and 1800–1950 nm; Savitzky–Golay smoothing; FD and SD from the same fit.`, `Red-edge REP, Dr, SDr; 39 base indices (${T('hsidx')}) + 9 SWIR disease indices (${T('hsswir')}, ${F('swir')}); ROTI only if the 1982 nm band passes the noise check.`, `SWIR indices use only bands outside the removed water regions (1350–1450 and 1800–1950 nm); they are computed from the endmember plot spectrum, so the coarser SWIR pixels (≈ 36 cm) do not mix with soil.`],
 mine: `1443 band features + 3 red-edge parameters + 48 indices (39 + 9 SWIR); ${F('spec')} shows dummy grade-mean spectra.`,
 vis: [TAB('hsidx', __HSIDX__), TAB('hsswir', __HSSWIR__), FIG('swir', 'o1_swir.png', 'Dummy SWIR reflectance of grades 0 and 9 with the bands used by the SWIR disease indices; grey: removed water-vapour regions. Diseased canopy has higher SWIR reflectance (less leaf water), which the SWIR indices capture.', 560), FIG('spec', 'o1_spectra.png', 'Dummy grade-mean reflectance (a) and first derivative (b) for grades 0–9: visible reflectance rises, the red edge shifts and NIR falls with severity.', 560)],
 out: `HS feature table: 1443 band features, 3 red-edge parameters, 48 indices (39 base + 9 SWIR disease indices).`,
 qs: [[`Why endmembers for the plot spectrum?`, `They are the purest spectra; averaging only crop endmembers removes soil and shadow mixing, important for the coarse SWIR pixels.`], [`Why add SWIR indices when white rust is seen in the visible?`, `Pustules and chlorosis change pigments (visible), but infection also reduces leaf water and changes dry matter; these show at 1240, 1600–1660 nm and beyond. Apan et al. (2004) found that adding the 1660 nm band improved rust separation over VNIR-only indices.`], [`Why not NDNI, NDLI or CAI?`, `They target nitrogen, lignin and cellulose (Serrano et al., 2002; Nagler et al., 2000) and have no validation for foliar disease; their 1510–2200 nm bands have low signal-to-noise in UAV data. They can be added later as a check.`], [`Can drought give the same SWIR signal?`, `Yes; this is why the thermal–water check (TIR Tier 2) and RWC sampling are used, and why water indices such as MSI and NDII are read together with DWSI and ROTI.`], [`Why remove flower endmembers?`, `Grades are leaf-based and yellow petals dominate 500–650 nm; flowering differs with sowing date and variety, so it would mix phenology with disease (Sulik and Long, 2016).`]],
 refs: `Keshava and Mustard (2002); Tsai and Philpot (1998); Guo et al. (2021); Shukla et al. (2024); Apan et al. (2004); Gao (1996); Hunt and Rock (1989); Hardisky et al. (1983); Yu et al. (2018); Kundu et al. (2021); Mandal et al. (2023); Ramalingam et al. (2026).` });

TIER({ title: 'HS Tier 2. Band-level selection: correlation scalogram + ReliefF',
 pos: `After HS Tier 1 (band features only); before HS Tier 3 (ReliefF ranking reused), Tier 5 (band step of CDA) and Tier 6 (Boruta).`,
 problem: `1443 band features are redundant (neighbouring bands r ≈ 1) and more than the plots; they cannot enter CDA or models directly.`,
 concept: `A **correlation scalogram** plots Pearson's r between PDI and R, FD and SD at every wavelength (regression side). **ReliefF** weights each band by how well it separates near samples of different grades (classification side; Robnik-Šikonja and Kononenko, 2003). From each list only **one band per correlated region** (band-to-band r ≥ 0.95) is kept.`,
 need: `It reduces the bands to a short, interpretable list before CDA and Boruta, and shows which wavelengths respond to white rust.`,
 why: `The grades are cuts of a continuous severity and overlap: a PDI-based scalogram needs no class limits, and ReliefF is designed for noisy, overlapping, multi-class data. The scalogram is the first step of Shukla et al. (2024) on mustard; ReliefF was used for severity by Mahlein et al. (2013) and Meng et al. (2020).`,
 papers: [`Shukla et al. (2024): correlation of R, FD and SD with aphid grade in mustard (483–487, 509–515, 690–714, 719–723 nm).`, `Mahlein et al. (2013); Meng et al. (2020): ReliefF for disease indices and three-level severity; Lv et al. (2023): ReliefF + SFFS.`, `Tian et al. (2021): one representative feature per common region.`],
 alts: TAB('althst2', [['Alternative', 'How it works / used by', 'Why not used here'], ['Separability scalogram', 'Threshold accuracy per band, top 5% (Tian et al., 2021)', 'Built for two well-separated classes; one threshold cannot split six overlapping grades; no help for regression'], ['SPA', 'Low-collinearity wavelengths chosen by projections and MLR (Zhu et al., 2017; Huang et al., 2020)', 'Picks bands for non-redundancy, not disease response; depends on start band'], ['PCA loadings', 'Peaks of component loadings (Shukla et al., 2024)', 'Follows overall variance (structure, illumination, flowering), not disease'], ['PLSR loadings / VIP', 'Supervised loadings (Krishna et al., 2014; Wold et al., 2001)', 'Subjective peak picking; Shukla\'s bands not linked to known absorptions'], ['Intersection only', 'Keep only regions common to both lists', 'Too few bands and loses task-specific bands']], [2000, 3700, 3606], 'Alternatives for HS band-level selection and why they fit less well.', 15),
 how: [`Scalogram: r(λ) for R, FD, SD vs PDI; candidates p < 0.01 and top 5% of |r|.`, `ReliefF: six grades, k = 10 neighbours, same-plot neighbours excluded; candidates top 5% of weights.`, `Correlated regions from the band-to-band correlation matrix (r ≥ 0.95); keep the highest |r| / weight per region in each list.`, `Common region (or within ±10 nm) → robust band, both tasks; scalogram-only → regression list; ReliefF-only → classification list.`, `Vegetation indices are not screened here (only raw bands); they go to Tiers 4–6.`],
 mine: `In the mustard ASD data 349 bands form 18 correlated regions (${F('bandcorr')}); in the dummy ReliefF example (${F('relief')}) one band per region was kept at ${DUM.relief_sel.join(', ')} nm.`,
 vis: [FIG('scal', 'm7_scalogram.png', 'Dummy correlation scalograms (reflectance and first derivative vs PDI) and ReliefF weights; red marks the top 5%.', 560), FIG('relief', 'o1_relief.png', 'Dummy multi-class ReliefF for the six grades: (a) weight spectrum with top-5% threshold and one band per correlated region; (b) pairwise ReliefF at the kept bands — adjacent grades are hard to separate, grade 0 vs 9 is easy.', 560), FIG('bandcorr', 'n8_bandcorr.png', 'Real band redundancy in the mustard ASD leaf spectra.', 540), TAB('bandgroups', [['Group', 'Dummy example', 'Meaning', 'Use'], ['Common to both', '555, 705 nm', 'Changes steadily with PDI and separates grades', 'Robust bands; both pools'], ['Scalogram only', '760, 2200 nm', 'Steady trend, weak grade separation', 'Regression list'], ['ReliefF only', '530, 715 nm', 'Grade-specific or non-linear response', 'Classification list']], [1700, 2300, 2900, 2406], 'Dummy example of combining the two band lists.', 16)],
 out: `Robust white-rust bands, a regression band list and a classification band list (typically 10–20 bands, one per region).`,
 qs: [[`Why scalogram + ReliefF?`, `The scalogram finds bands that change steadily with severity; ReliefF finds bands that separate the grades, including non-linear responses; together they cover regression and classification.`], [`Why one band per region?`, `Neighbouring bands are near-duplicates; one per region gives a short, non-redundant list.`]],
 refs: `Shukla et al. (2024); Robnik-Šikonja and Kononenko (2003); Mahlein et al. (2013); Meng et al. (2020); Tian et al. (2021).` });

TIER({ title: 'HS Tier 3. White Rust Index (WRI)',
 pos: `After HS Tier 2 (ReliefF ranking reused); the WRI joins the HS indices in Tiers 4–6.`,
 problem: `General indices (NDVI, PSSR) also respond to nutrient or water stress; a feature specific to white rust is needed.`,
 concept: `A spectral disease index combines a normalised difference of two bands with a weighted third band, searched exhaustively to separate healthy and diseased plots best (Mahlein et al., 2013):`,
 eqs: [EQ('WRI = (R_{λ1} − R_{λ2}) / (R_{λ1} + R_{λ2}) + w R_{λ3},   w ∈ {−1, −0.5, 0, 0.5, 1}', 'e:wri')],
 need: `It gives Objective 1 a white-rust-specific feature and a compact, transferable index.`,
 why: `Mahlein et al. (2013) built indices for three sugar-beet diseases with 85–92% balanced accuracy; the same approach worked for corn rust and rice blast; SWIR bands were the most sensitive for mustard rot (Bhattacharya and Chattopadhyay, 2013), so a SWIR search is added.`,
 papers: [`Mahlein et al. (2013): ReliefF + exhaustive search; e.g. SBRI = (R570 − R513)/(R570 + R513) + 0.5 R704.`, `Meng et al. (2020): health and severity indices for corn rust (+8.3% over best published index for severity).`, `Mandal et al. (2023): blast indices from R1148 and R1301; Bhattacharya and Chattopadhyay (2013): three-band ROTI.`],
 alts: TAB('althst3', [['Alternative', 'How it works / used by', 'Why not used here'], ['Two-band RSI/DSI/NDSI search', 'All band pairs, correlation contour (Shukla et al., 2024)', 'Two bands only; Mahlein form adds a weighted band'], ['Separate severity index', 'Index for severity levels (Meng et al., 2020)', 'Severity is handled by PDI regression; optional'], ['Three-band ratio (ROTI type)', 'R_{a}/(R_{b} + R_{c}) (Bhattacharya and Chattopadhyay, 2013)', 'Included among the 48 indices instead']], [2300, 3700, 3306], 'Alternatives for the disease-specific index.', 16),
 how: [`Training plot spectra; healthy (grade 0) vs diseased (grades 1–9).`, `450–950 nm averaged to 6 nm (84 bands); single bands and all normalised differences with bands ≥ 50 nm apart (2850).`, `ReliefF keeps the best 25% (21 bands, ≈ 713 NDs); all combinations × 5 weights (≈ 75 000 candidates).`, `Each candidate as a one-feature classifier with optimised threshold; 8-fold stratified, plot-grouped CV; criterion balanced accuracy = (sensitivity + specificity)/2.`, `Best = WRI; repeat with SWIR; keep the better; report r with PDI and grade means; compare with NDVI, PSSRa, PRI.`],
 mine: `Dummy search: best pair ${DUM.wri_best[0]} and ${DUM.wri_best[1]} nm, balanced accuracy ${DUM.wri_best[2]} (${F('wri')}).`,
 vis: [FIG('wri', 'o1_wri.png', 'Dummy WRI search (a; star = best pair) and WRI values by grade (b).', 560)],
 out: `WRI formula, threshold, balanced accuracy and r with PDI.`,
 qs: [[`How is the WRI different from NDVI?`, `NDVI responds to any greenness loss; the WRI bands and weight are searched to separate white-rust plots from healthy plots.`], [`Why 6 nm and 50 nm?`, `Neighbouring bands are nearly identical, so finer resolution adds nothing and close pairs carry little contrast (Mahlein et al., 2013).`]],
 refs: `Mahlein et al. (2013); Meng et al. (2020); Mandal et al. (2023); Bhattacharya and Chattopadhyay (2013).` });

TIER({ title: 'HS Tier 4. Univariate response of HS features (Method M1)',
 pos: `After HS Tiers 1–3; in parallel with HS Tiers 5–6.`,
 problem: `Which HS indices, red-edge parameters and bands change with white rust, between which grades, and why?`,
 concept: `Method M1 (Chapter 3) applied to the HS features.`,
 need: `It gives the physiological interpretation of the HS signal.`,
 why: `See Method M1; for HS, pigment, red-edge and water features are expected to respond (Mahlein et al., 2019; Guo et al., 2021).`,
 papers: [`Mahlein et al. (2019): PSSRa/b separated infected spikelets 3 days after inoculation.`, `Guo et al. (2021): PSRI, PRI, ARI, SIPI tracked yellow-rust DI.`],
 alts: `Alternatives as for Method M1 (${T('altm1')}).`,
 how: [`Input: 48 indices, REP/Dr/SDr, WRI and the robust bands of HS Tier 2.`, `ANOVA + Tukey across six grades; Pearson r with PDI; correlation with chlorophyll, carotenoid, anthocyanin and RWC.`],
 mine: `${T('expHS')} lists the expected responses; ${T('anovaHS')} and ${F('profHS')}a show dummy results.`,
 vis: [TAB('expHS', [['Feature', 'Expected change with grade', 'Physical reason', 'Reference'], ['PSSRa, NDVI, MTVI', 'Decrease', 'Chlorophyll loss, less NIR scattering', 'Blackburn 1998; Mahlein 2019'], ['REP', 'Decrease (blue shift)', 'Narrower chlorophyll absorption', 'Horler et al. 1983'], ['PSRI, ARI', 'Increase', 'Carotenoid/chlorophyll ratio up; senescence', 'Merzlyak et al. 1999; Gitelson et al. 2001'], ['PRI', 'Decrease', 'Lower light-use efficiency', 'Gamon et al. 1992'], ['WI, DWSI-1', 'Decrease', 'Leaf water loss (SWIR reflectance up)', 'Peñuelas et al. 1997; Apan et al. 2004'], ['WRI', 'Increase', 'Built to rise with white rust', 'Mahlein et al. 2013 (method)']], [1700, 2100, 3100, 2406], 'Expected response of key HS features.', 16), TAB('anovaHS', __ANOVA_HS__), FIG('profHS', 'o1_prof_HS.png', 'Dummy HS results: (a) key features by grade with ANOVA F, Tukey letters and r with PDI; (b) CDA score plot; (c) Boruta importance.', 560)],
 out: `Responding HS features with direction, separated grade pairs and physiological meaning.`,
 qs: [[`Which HS feature do you expect to respond first?`, `Pigment and red-edge features (PSSRa, REP) and the WRI, because chlorosis around pustules starts early.`]],
 refs: `Mahlein et al. (2019); Guo et al. (2021); Horler et al. (1983).` });

TIER({ title: 'HS Tier 5. Two-step class discrimination of HS features (Methods M2 + M3)',
 pos: `After HS Tiers 2–4; in parallel with HS Tier 6.`,
 problem: `How well do HS bands and indices together separate the six grades, and are bands or indices more discriminating?`,
 concept: `Methods M2 (VIF) and M3 (stepwise CDA) applied in two steps, as in Stage III of Bhattacharya and Chattopadhyay (2013): step 1 on the robust bands, step 2 on indices, red-edge parameters and WRI.`,
 need: `It gives the HS separability, its severity axis and the grade-overlap picture.`,
 why: `See Method M3; the two-step band-then-index design is specific to hyperspectral data and follows the mustard study.`,
 papers: [`Bhattacharya and Chattopadhyay (2013): 25 bands (step 1), then indices (step 2) ranked by canonical correlation.`],
 alts: `Alternatives as for Method M3 (${T('altm3')}).`,
 how: [`Step 1: VIF on robust bands → stepwise CDA → discriminating bands.`, `Step 2: VIF on indices + red-edge + WRI → stepwise CDA → discriminating indices.`, `Report canonical correlation, Wilks' lambda, weights, score plot, held-out accuracy.`],
 mine: `Dummy step-2 result: canonical correlation ${DUM.sensors.HS.cda.can[0]}, Wilks' lambda ${DUM.sensors.HS.cda.wilks}, accuracy ${DUM.sensors.HS.cda.acc} (${T('cdaHS')}, ${F('profHS')}b); the axis rises with the WRI and falls with PSSRa and REP.`,
 vis: [TAB('cdaHS', __CDA_HS__)],
 out: `Discriminating HS bands and indices, HS separability and severity axis.`,
 qs: [[`Why two steps for HS?`, `To compare bands and indices on equal terms, as Bhattacharya and Chattopadhyay (2013) did: first which bands separate the grades, then which indices.`]],
 refs: `Bhattacharya and Chattopadhyay (2013); Fisher (1936).` });

TIER({ title: 'HS Tier 6. HS disease-specific feature pools (Method M4)',
 pos: `Last HS tier; output to the cross-sensor tier and Objectives 2–3.`,
 problem: `Which HS features are relevant for six-grade classification and for PDI regression?`,
 concept: `Method M4 (Boruta) applied to all HS features after Tiers 2–3.`,
 need: `It produces the HS DSF pools used by the models.`,
 why: `See Method M4.`,
 papers: [`Mustafa et al. (2023): Boruta on hyperspectral and other sensor features.`],
 alts: `Alternatives as for Method M4 (${T('altm4')}).`,
 how: [`Input: robust bands + red-edge parameters + 48 indices + WRI.`, `Boruta for six-grade classes and for PDI.`],
 mine: `${T('borHS')} and ${F('profHS')}c show dummy results: pigment, red-edge and water indices and the WRI confirmed; RVSI and NPQI rejected.`,
 vis: [TAB('borHS', __BOR_HS__)],
 out: `HS DSF pool (classification) and HS DSF pool (regression).`,
 qs: [[`What if Boruta rejects an index that ANOVA found significant?`, `ANOVA p-values are optimistic with repeated plot-dates and test one feature at a time; Boruta's shadow test is stricter and multivariate, so its decision defines the pool.`]],
 refs: `Kursa and Rudnicki (2010); Mustafa et al. (2023).` });

// ======================= 5 MS =======================
K.push(H1('5. Multispectral sensor (MS)'));
K.push(P(`The MicaSense RedEdge-MX has five broad bands (475, 560, 668, 717, 840 nm). It has no band-level tier or WRI search because five broad bands give neither redundancy to reduce nor narrow bands to combine. ${F('flowMS')} shows its four tiers.`));
K.push(...fig2('flowMS', 'o1_flow_MS.png', 'Flow chart of Objective 1 for the multispectral sensor.', 520));
TIER({ title: 'MS Tier 1. Feature extraction',
 pos: `After Tier 0 and pre-processing; before MS Tiers 2–4.`,
 problem: `Five-band reflectance maps must be turned into plot features describing pigment, red edge and canopy pattern.`,
 concept: `Plot means of the five bands, 12 vegetation indices of the ORW and GLCM texture of each band.`,
 need: `MS Tiers 2–4 work on this table.`,
 why: `Red-edge indices (NDRE, CIrededge, MTCI) and PSRI tracked powdery-mildew DI from UAV MS data (Liu et al., 2024); texture adds spatial information (Guo et al., 2021).`,
 papers: [`Liu et al. (2024): 12 MS indices, texture, percentile spectra; NDRE, PSRI, MTCI tracked disease.`, `Nguyen et al. (2023): red-edge and NIR bands and GLCM contrast for yellow rust.`],
 alts: TAB('altmst1', [['Alternative', 'How it works / used by', 'Why not used here'], ['Percentile spectra', '20th–50th percentile reflectance (Liu et al., 2024)', 'Optional; plot mean is standard'], ['Three-band texture indices (TTCI)', 'Ratios of textures (Liu et al., 2024)', 'Optional; raw textures are simpler'], ['Band-level search / WRI', 'As for HS', 'Five broad bands: no redundancy, no narrow features']], [2300, 3600, 3406], 'Alternatives for MS features.', 16),
 how: [`Reflectance by panels + irradiance sensor; HS canopy mask transferred with edge erosion.`, `5 band means; 12 indices (${T('msidx')}); 40 GLCM textures (32 levels, d = 1, four directions averaged).`],
 mine: `${F('msTir')}a shows dummy five-band grade means.`,
 vis: [TAB('msidx', __MSIDX__), FIG('msTir', 'o1_ms_tir.png', 'Dummy MS five-band grade-mean reflectance (a) and TIR canopy–air temperature difference by grade (b).', 540)],
 out: `57 MS features.`,
 qs: [[`Why no WRI for MS?`, `The WRI search needs many narrow bands; MS has five broad bands, so its indices are used directly.`]],
 refs: `Liu et al. (2024); Guo et al. (2021); Haralick et al. (1973).` });
TIER({ title: 'MS Tier 2. Univariate response of MS features (Method M1)',
 pos: `After MS Tier 1.`, problem: `Which MS features respond to white rust and why?`, concept: `Method M1 applied to the 57 MS features.`, need: `Physiological interpretation of the MS signal.`,
 why: `See Method M1.`, papers: [`Liu et al. (2024): Dunnett test of MS features between disease levels.`], alts: `Alternatives as for Method M1 (${T('altm1')}).`,
 how: [`ANOVA + Tukey; Pearson r with PDI; red-edge indices vs chlorophyll; textures vs pustule cover.`],
 mine: `Expected: R band and PSRI increase; RE, NIR, NDRE, CIrededge, MTCI decrease; texture contrast increases. Dummy results: ${T('anovaMS')}, ${F('profMS')}a.`,
 vis: [TAB('anovaMS', __ANOVA_MS__), FIG('profMS', 'o1_prof_MS.png', 'Dummy MS results: (a) key features by grade; (b) CDA score plot; (c) Boruta importance.', 560)],
 out: `Responding MS features with direction.`, qs: [[`Which MS feature is best?`, `Red-edge indices such as NDRE, because chlorophyll loss changes the red-edge contrast (Liu et al., 2024).`]], refs: `Liu et al. (2024).` });
TIER({ title: 'MS Tier 3. Class discrimination of MS features (Methods M2 + M3)',
 pos: `After MS Tier 2.`, problem: `How well do MS features together separate the six grades?`, concept: `VIF then one-step stepwise CDA (Methods M2, M3).`, need: `MS separability and severity axis.`,
 why: `See Method M3; one step is enough because MS has few features.`, papers: [`Bhattacharya and Chattopadhyay (2013): stepwise CDA design.`], alts: `Alternatives as for Method M3 (${T('altm3')}).`,
 how: [`VIF < 10 → stepwise CDA → canonical correlation, weights, score plot, held-out accuracy.`],
 mine: `Dummy: canonical correlation ${DUM.sensors.MS.cda.can[0]}, accuracy ${DUM.sensors.MS.cda.acc} (${T('cdaMS')}, ${F('profMS')}b).`, vis: [TAB('cdaMS', __CDA_MS__)],
 out: `MS separability of six grades.`, qs: [[`Why is MS accuracy lower than HS?`, `Broad bands miss narrow pigment and water features, so adjacent grades overlap more.`]], refs: `Bhattacharya and Chattopadhyay (2013).` });
TIER({ title: 'MS Tier 4. MS disease-specific feature pools (Method M4)',
 pos: `Last MS tier.`, problem: `Which MS features are relevant for classification and regression?`, concept: `Boruta (Method M4) on the 57 MS features.`, need: `MS DSF pools for Objectives 2–3.`,
 why: `See Method M4.`, papers: [`Mustafa et al. (2023).`], alts: `Alternatives as for Method M4 (${T('altm4')}).`,
 how: [`Boruta for six grades and for PDI.`], mine: `Dummy results: ${T('borMS')}, ${F('profMS')}c.`, vis: [TAB('borMS', __BOR_MS__)],
 out: `MS DSF pools (2).`, qs: [[`Why keep textures if indices are strong?`, `Boruta keeps them only if they beat the shadows; texture adds spatial information on pustules.`]], refs: `Kursa and Rudnicki (2010).` });

// ======================= 6 RGB =======================
K.push(H1('6. RGB sensor'));
K.push(P(`The RGB camera has the finest pixels and records colour, texture and canopy structure. ${F('flowRGB')} shows its four tiers.`));
K.push(...fig2('flowRGB', 'o1_flow_RGB.png', 'Flow chart of Objective 1 for the RGB sensor.', 520));
TIER({ title: 'RGB Tier 1. Feature extraction',
 pos: `After Tier 0 and pre-processing; before RGB Tiers 2–4.`,
 problem: `White pustules, chlorosis and stagheads change the colour and spatial pattern of the canopy; these must be quantified per plot.`,
 concept: `**GLCM texture** counts how often grey levels i and j occur next to each other and summarises the pattern (contrast, homogeneity, entropy …; Haralick et al., 1973); colour is described by hue, saturation and value; structure by vegetation fraction and canopy height.`,
 need: `RGB Tiers 2–4 use these features.`,
 why: `Texture was most informative at higher severity (Guo et al., 2021); entropy correlated with powdery-mildew DI (Feng et al., 2022); colour features helped Fusarium detection (Mustafa et al., 2023); structure from Maimaitijiang et al. (2020).`,
 papers: [`Feng et al. (2022): five GLCM textures; entropy most related to DI.`, `Guo et al. (2021): texture best at late stage; pixel size matters.`, `Maimaitijiang et al. (2020): canopy height and vegetation fraction from UAV RGB.`],
 alts: TAB('altrgbt1', [['Alternative', 'How it works / used by', 'Why not used here'], ['Local binary patterns', 'Texture from local pixel codes (Ojala et al., 2002)', 'GLCM is standard in the reference papers'], ['CNN image features', 'Learned features (Deng et al., 2024)', 'Needs large labelled image sets; 72 plots too few'], ['Colour indices (ExG etc.)', 'Index of R, G, B (Woebbecke et al., 1995)', 'Used for masking; HSV covers colour change']], [2300, 3600, 3406], 'Alternatives for RGB features.', 16),
 how: [`HS canopy mask transferred with edge erosion; GLCM on R, G, B (32 levels, d = 1, 4 directions averaged): 8 measures × 3 bands = 24.`, `Mean H, S, V; vegetation fraction; canopy height (DSM − DEM).`, `Flower fraction stored as a covariate, not a disease feature.`],
 mine: `${F('glcm')} shows a worked GLCM example; ${T('rgbfeat')} lists the features.`,
 vis: [TAB('rgbfeat', __RGBFEAT__), FIG('glcm', 'n7_glcm.png', 'Worked GLCM example: image, co-occurrence counts and texture measures.', 540)],
 out: `29 RGB features and the flower-fraction covariate.`,
 qs: [[`In the GLCM, what are i and j?`, `Grey levels (rows and columns of the matrix), not pixel positions.`], [`Why is flower fraction a covariate?`, `Yellow flowers change colour and texture but depend on sowing date and variety, not on disease; the covariate lets me check that features are not following flowering.`]],
 refs: `Haralick et al. (1973); Feng et al. (2022); Guo et al. (2021); Maimaitijiang et al. (2020).` });
TIER({ title: 'RGB Tier 2. Univariate response of RGB features (Method M1)',
 pos: `After RGB Tier 1.`, problem: `Which RGB features respond to white rust, and are they confounded with flowering?`, concept: `Method M1 applied to the 29 RGB features, plus a correlation check with flower fraction.`, need: `Physiological and visual interpretation.`,
 why: `See Method M1.`, papers: [`Feng et al. (2022): texture–DI correlation.`], alts: `Alternatives as for Method M1 (${T('altm1')}).`,
 how: [`ANOVA + Tukey; Pearson r with PDI; r of each feature with flower fraction (a feature mainly following flower fraction is flagged).`],
 mine: `Expected: contrast, dissimilarity, entropy increase; homogeneity decreases; hue decreases (yellowing); VF decreases. Dummy results: ${T('anovaRGB')}, ${F('profRGB')}a.`,
 vis: [TAB('anovaRGB', __ANOVA_RGB__), FIG('profRGB', 'o1_prof_RGB.png', 'Dummy RGB results: (a) key features by grade; (b) CDA score plot; (c) Boruta importance.', 560)],
 out: `Responding RGB features; flowering check.`, qs: [[`Why does contrast increase?`, `White pustules on green leaves create sharp grey-level differences between neighbouring pixels.`]], refs: `Feng et al. (2022); Haralick et al. (1973).` });
TIER({ title: 'RGB Tier 3. Class discrimination of RGB features (Methods M2 + M3)',
 pos: `After RGB Tier 2.`, problem: `How well do RGB features together separate the six grades?`, concept: `VIF then one-step stepwise CDA.`, need: `RGB separability.`,
 why: `See Method M3.`, papers: [`Bhattacharya and Chattopadhyay (2013).`], alts: `Alternatives as for Method M3 (${T('altm3')}).`,
 how: [`VIF < 10 → stepwise CDA → canonical correlation, weights, score plot, held-out accuracy.`],
 mine: `Dummy: canonical correlation ${DUM.sensors.RGB.cda.can[0]}, accuracy ${DUM.sensors.RGB.cda.acc} (${T('cdaRGB')}, ${F('profRGB')}b).`, vis: [TAB('cdaRGB', __CDA_RGB__)],
 out: `RGB separability of six grades.`, qs: [[`Why can RGB separate high grades well?`, `At high grades pustules and stagheads are large and visible, so texture and colour change strongly.`]], refs: `Bhattacharya and Chattopadhyay (2013).` });
TIER({ title: 'RGB Tier 4. RGB disease-specific feature pools (Method M4)',
 pos: `Last RGB tier.`, problem: `Which RGB features are relevant for classification and regression?`, concept: `Boruta on the 29 RGB features.`, need: `RGB DSF pools.`,
 why: `See Method M4.`, papers: [`Mustafa et al. (2023).`], alts: `Alternatives as for Method M4 (${T('altm4')}).`,
 how: [`Boruta for six grades and for PDI.`], mine: `Dummy results: ${T('borRGB')}, ${F('profRGB')}c.`, vis: [TAB('borRGB', __BOR_RGB__)],
 out: `RGB DSF pools (2).`, qs: [[`Is canopy height a disease feature?`, `Indirectly: stagheads and canopy thinning change height and cover; Boruta decides whether it is relevant.`]], refs: `Kursa and Rudnicki (2010).` });

// ======================= 7 TIR =======================
K.push(H1('7. Thermal sensor (TIR)'));
K.push(P(`The thermal camera measures canopy temperature, which rises when infection reduces transpiration. ${F('flowTIR')} shows its four tiers.`));
K.push(...fig2('flowTIR', 'o1_flow_TIR.png', 'Flow chart of Objective 1 for the thermal sensor.', 520));
TIER({ title: 'TIR Tier 1. Feature extraction',
 pos: `After Tier 0 and pre-processing; before TIR Tiers 2–4.`,
 problem: `Raw canopy temperature depends on the weather of each flight; comparable indices of transpiration change are needed.`,
 concept: `Canopy temperature (CT) and normalised indices: CTD = CT − AT, CTR = (CT + 273.15)/(AT + 273.15), NRCT = (CT − CT_{min})/(CT_{max} − CT_{min}) within the image, MTD = maximum − minimum canopy temperature in the plot, plus GLCM texture of the temperature image.`,
 need: `TIR Tiers 2–4 use these features; normalisation is needed because dates are pooled.`,
 why: `CT, CTD, CTR and NRCT were used for powdery mildew (Feng et al., 2022); MTD for Fusarium head blight (Mahlein et al., 2019); canopy temperature tracked DI (Liu et al., 2024).`,
 papers: [`Feng et al. (2022): CT, CTD, CTR, NRCT.`, `Mahlein et al. (2019): MTD and temperature differences of infected spikelets.`, `Maimaitijiang et al. (2020): thermal calibration and NRCT.`],
 alts: TAB('alttirt1', [['Alternative', 'How it works / used by', 'Why not used here'], ['CWSI', 'Crop water stress index from wet/dry references (Idso et al., 1981; Jackson et al., 1981)', 'Needs reference surfaces each flight; CTD and NRCT are simpler'], ['Temperature–emissivity separation', 'Retrieve emissivity per pixel (Gillespie et al., 1998)', 'Canopy emissivity ≈ constant; not needed'], ['Raw CT only', 'Mean canopy temperature', 'Varies with weather; normalised indices used']], [2300, 3700, 3306], 'Alternatives for TIR features.', 16),
 how: [`15–20 min warm-up; radiometric conversion with emissivity, air temperature, RH, height; check with ground targets.`, `HS canopy mask transferred with edge erosion (no warm soil); compute the five indices and 8 textures (${T('tirfeat')}).`],
 mine: `${F('msTir')}b shows dummy CTD by grade.`,
 vis: [TAB('tirfeat', __TIRFEAT__)],
 out: `13 TIR features.`,
 qs: [[`Why CTR in kelvin?`, `A ratio of Celsius values depends on the zero of the scale; in kelvin it is physically meaningful.`], [`Why NRCT?`, `It scales temperature 0–1 within each image, removing most of the weather difference between flights.`]],
 refs: `Feng et al. (2022); Mahlein et al. (2019); Maimaitijiang et al. (2020).` });
TIER({ title: 'TIR Tier 2. Univariate response of TIR features (Method M1) and thermal–water check',
 pos: `After TIR Tier 1.`, problem: `Which TIR features respond, and is warming caused by disease rather than drought?`,
 concept: `Method M1 applied to TIR features, plus correlation with stomatal conductance and transpiration and a check that warmer plots do not have lower water status.`,
 need: `Water deficit also warms canopies; the check separates disease from drought.`,
 why: `Bhattacharya and Chattopadhyay (2013) separated rot from water stress with canopy stress without soil-moisture stress; the experiment is uniformly irrigated, so warming without lower RWC indicates disease.`,
 papers: [`Bhattacharya and Chattopadhyay (2013): TVDI–NDWI space (canopy stress without soil-moisture stress = rot).`, `Liu et al. (2024): canopy temperature rose with DI.`],
 alts: TAB('alttirt2', [['Alternative', 'How it works / used by', 'Why not used here'], ['TVDI–NDWI trapezoid', 'Satellite surface temperature vs water index (Bhattacharya and Chattopadhyay, 2013)', 'Designed for satellite pixels; plot RWC and WI are direct'], ['Stomatal conductance only', 'Porometer readings', 'Used together with RWC']], [2300, 3700, 3306], 'Alternatives for the disease-vs-drought check.', 16),
 how: [`ANOVA + Tukey; Pearson r with PDI.`, `r of CTD/NRCT with stomatal conductance (expected negative) and with RWC and HS water indices (expected near zero).`],
 mine: `Expected: CT, CTD, NRCT, MTD increase with grade. Dummy check: r(CTD, RWC) = ${DUM.tir_check_r} (${F('tirCheck')}).`,
 vis: [TAB('anovaTIR', __ANOVA_TIR__), FIG('profTIR', 'o1_prof_TIR.png', 'Dummy TIR results: (a) key features by grade; (b) CDA score plot; (c) Boruta importance.', 560), FIG('tirCheck', 'o1_tir_check.png', 'Dummy thermal–water check: CTD increases with grade while relative water content stays uniform.', 380)],
 out: `Responding TIR features; evidence that warming is disease-related.`, qs: [[`How do you know the canopy is warm because of disease and not drought?`, `Irrigation is uniform, and warmer diseased plots do not show lower RWC or water index; stomatal conductance falls with grade.`]], refs: `Bhattacharya and Chattopadhyay (2013); Liu et al. (2024).` });
TIER({ title: 'TIR Tier 3. Class discrimination of TIR features (Methods M2 + M3)',
 pos: `After TIR Tier 2.`, problem: `How well do TIR features together separate the six grades?`, concept: `VIF then one-step stepwise CDA.`, need: `TIR separability.`,
 why: `See Method M3.`, papers: [`Bhattacharya and Chattopadhyay (2013).`], alts: `Alternatives as for Method M3 (${T('altm3')}).`,
 how: [`VIF < 10 → stepwise CDA → canonical correlation, weights, score plot, held-out accuracy.`],
 mine: `Dummy: canonical correlation ${DUM.sensors.TIR.cda.can[0]}, accuracy ${DUM.sensors.TIR.cda.acc} (${T('cdaTIR')}, ${F('profTIR')}b).`, vis: [TAB('cdaTIR', __CDA_TIR__)],
 out: `TIR separability of six grades.`, qs: [[`Why is TIR weaker alone?`, `Temperature responds to transpiration, which also varies with weather and canopy; it is expected to add most in fusion with HS (Mahlein et al., 2019).`]], refs: `Mahlein et al. (2019).` });
TIER({ title: 'TIR Tier 4. TIR disease-specific feature pools (Method M4)',
 pos: `Last TIR tier.`, problem: `Which TIR features are relevant for classification and regression?`, concept: `Boruta on the 13 TIR features.`, need: `TIR DSF pools.`,
 why: `See Method M4.`, papers: [`Mustafa et al. (2023).`], alts: `Alternatives as for Method M4 (${T('altm4')}).`,
 how: [`Boruta for six grades and for PDI.`], mine: `Dummy results: ${T('borTIR')}, ${F('profTIR')}c.`, vis: [TAB('borTIR', __BOR_TIR__)],
 out: `TIR DSF pools (2).`, qs: [[`Is raw CT kept?`, `Only if Boruta confirms it; normalised indices usually carry the disease signal better.`]], refs: `Kursa and Rudnicki (2010).` });

// ======================= 8 CROSS-SENSOR =======================
K.push(H1('8. Cross-sensor tier'));
TIER({ title: 'Cross-sensor tier. Complementarity of the four sensors',
 pos: `After the last tier of every sensor; final tier of Objective 1. Its outputs go to Objectives 2 and 3.`,
 problem: `Objective 2 fuses sensors; Objective 1 must show whether the sensors carry different information and which separates the grades best.`,
 concept: `A correlation matrix of the DSFs of all sensors shows shared and complementary information; an optional combined CDA on the features selected by the four single-sensor CDAs shows whether combining raises separability.`,
 need: `It justifies fusion and summarises Objective 1.`,
 why: `Mahlein et al. (2019) correlated thermal, fluorescence and spectral parameters with each other and with severity to judge complementarity; a combined CDA is a simple linear preview before the fusion models of Objective 2.`,
 papers: [`Mahlein et al. (2019): cross-sensor correlation; HS + thermal best pair.`, `Feng et al. (2022); Maimaitijiang et al. (2020): fusion improved over single sensors.`],
 alts: TAB('altx', [['Alternative', 'How it works / used by', 'Why not used here'], ['Canonical correlation analysis between sensors', 'Shared variance of two feature sets (Hotelling, 1936)', 'Pairwise and more complex; correlation matrix is simpler'], ['Fusion models now', 'Train fused classifiers', 'Belongs to Objective 2 with proper validation']], [2600, 3600, 3106], 'Alternatives for the cross-sensor analysis.', 16),
 how: [`Pearson correlation among DSFs of all sensors and with PDI.`, `Optional: pool the CDA-selected features of the four sensors → VIF → stepwise CDA; compare canonical correlation and accuracy with the best single sensor.`, `Summarise per sensor: number of DSFs, canonical correlation, CDA accuracy.`],
 mine: `Dummy comparison in ${T('sensorcmp')}; dummy correlations in ${F('xcorr')} (low correlation of TIR with HS pigment features suggests complementarity).`,
 vis: [FIG('xcorr', 'o1_xcorr.png', 'Dummy correlation between DSFs of the four sensors.', 460), TAB('sensorcmp', __SENSORCMP__)],
 out: `Complementarity evidence; sensor ranking; **eight DSF pools** (4 sensors × classification and regression), robust white-rust bands and the WRI for Objectives 2 and 3.`,
 qs: [[`What if two sensors are highly correlated?`, `Then one may be enough; Objective 2 tests this with the fusion models.`], [`Why is combined CDA only optional?`, `Combinations are tested properly in Objective 2; here it is only a quick linear preview.`]],
 refs: `Mahlein et al. (2019); Feng et al. (2022); Maimaitijiang et al. (2020).` });
K.push(BOX('How Objective 1 is satisfied:', `Tier 1 gives physically meaningful features for every sensor; HS Tiers 2–3 identify white-rust wavelengths and a disease-specific index; M1 tiers show which features respond and why; M3 tiers show how well each sensor separates the six grades; M4 tiers give the disease-specific feature pools; the cross-sensor tier shows complementarity. Together these answer Q1–Q6.`, 'E3F2FD', '1565C0'));

// ======================= 9 GENERAL Q&A =======================
K.push(H1('9. General interview questions on Objective 1'));
QA('What is the main output of Objective 1?', 'For every sensor, the features that respond to white rust and why, the robust hyperspectral bands and a White Rust Index, the separability of the six grades, and two disease-specific feature pools (classification and PDI regression) that feed Objectives 2 and 3.');
QA('Why are the tiers different for each sensor?', 'Each sensor measures a different property: only the hyperspectral sensor has many narrow, redundant bands that need band-level selection and allow a disease index; MS, RGB and TIR go directly from features to the common analysis tiers.');
QA('Why not go straight to machine learning?', 'Objective 1 must explain which features respond and why; the tiers also reduce hundreds of features to relevant pools, which prevents overfitting in Objective 2.');
QA('How do you prevent information leakage in Objective 1?', 'When features become model inputs, band selection, the WRI search, VIF, CDA and Boruta are repeated on the training replications only.');
