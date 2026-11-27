"""Revision 4: biochemical and biophysical parameters (acquisition Step A8, Objective 1 Activity 1.7,
Objective 3 Step 3.1.2) with statistical analysis."""
def patch(f, reps):
    s = open(f).read()
    for a, b in reps:
        n = s.count(a)
        assert n == 1, (f, n, a[:90])
        s = s.replace(a, b)
    open(f, 'w').write(s)

# ------------------------------------------------------------------ body: abbreviations, dataset row, Step A8
A8 = r'''STEP('A8', 'Biochemical and biophysical parameters',
     'Spectral and thermal features are indirect. Measured pigments, water status, membrane damage, gas exchange and leaf area show what white rust does to the plant and give the camera responses a physiological explanation.',
     'One designated subplot per plot; untagged plants of that subplot for destructive samples; leaf L3 (third fully expanded leaf from the top); spectrophotometer, conductivity meter, LI-6400 portable gas exchange system, plant canopy analyser.',
     'Table of 11 parameters for 48 plots × 4 dates (192 samples per parameter; leaf area index for all 4 subplots) → Activity 1.7 and Step 3.1.2.',
     ['Dates (all on UAV flight days): 18 January 2027 (pre-symptomatic, 8 days after inoculation) and 28 January, 18 February and 11 March 2027 (post-symptomatic, 18, 39 and 60 days after inoculation), covering early, peak and late disease and the vegetative, flowering and pod-formation stages.',
      'Designated subplot: one subplot per plot, rotated so that each of the four subplot positions is sampled in 12 plots (position = plot number modulo 4, plus 1); its code is stored with every sample, so the parameters can be joined to the UAV features and canopy score of that subplot.',
      'Gas exchange: on leaf L3 of one tagged plant (non-destructive, Step A4), between 09:30 and 11:30 h, before the flight.',
      'Leaf samples for the laboratory: after the gas-exchange readings, collect L3 leaves from 3 untagged plants of the designated subplot, keep them in a cool box and process them the same day; the tagged plants are not damaged.',
      'Leaf area index: in all four subplots, under diffuse light (early morning, late afternoon or overcast sky).',
      'Record the BBCH growth stage of each plot on every sampling date (Step A6).',
      'Methods and units are given in Table [[T:physio]]; the formulas are given below.'],
     'Plant traits measured together with airborne and UAV imagery to explain disease-related spectral and thermal changes: Calderón et al. (2013), Zarco-Tejada et al. (2018), Poblete et al. (2023); leaf area index of mustard with a plant canopy analyser at IARI: Goyal et al. (2021).')
TAB('physio', [['Parameter (unit)', 'Method', 'Sample', 'References'],
    ['Chlorophyll a and b (mg g⁻¹ fresh weight)', 'extraction in dimethyl sulfoxide (DMSO) without grinding; absorbance at 665 and 649 nm; DMSO equations', '100 mg leaf discs in 10 mL DMSO, 65 °C until colourless', 'Hiscox and Israelstam (1979); Wellburn (1994)'],
    ['Total carotenoids (mg g⁻¹ fresh weight)', 'same DMSO extract; absorbance at 480 nm; DMSO equation', 'same extract', 'Lichtenthaler and Wellburn (1983); Wellburn (1994)'],
    ['Anthocyanin (µg g⁻¹ fresh weight)', 'pH differential method: absorbance at about 520 and 700 nm in pH 1.0 (potassium chloride) and pH 4.5 (sodium acetate) buffers', 'acidified-methanol extract of 0.5 g leaf tissue', 'Lee et al. (2005)'],
    ['Total soluble protein (mg g⁻¹ fresh weight)', 'Bradford dye-binding method; absorbance at 595 nm against a bovine serum albumin standard curve', 'buffer extract of 0.5 g leaf tissue', 'Bradford (1976)'],
    ['Relative water content (%)', 'fresh weight, turgid weight after 4 h floating on distilled water, dry weight after 48 h at 70 °C', '10 leaf discs', 'Barrs and Weatherley (1962)'],
    ['Membrane stability index (%)', 'electrolyte leakage: conductivity after 30 min at 40 °C (C₁) and after 10 min at 100 °C (C₂)', 'two sets of 0.1 g leaf discs in 10 mL double-distilled water', 'Premachandra et al. (1990); Sairam (1994)'],
    ['Net photosynthetic rate (µmol CO₂ m⁻² s⁻¹)', 'LI-6400 portable gas exchange system (infrared gas analyser): leaf chamber with LED light 1200 µmol m⁻² s⁻¹, reference CO₂ 400 µmol mol⁻¹, flow 500 µmol s⁻¹, leaf temperature near ambient; read after the values are stable', 'leaf L3 of a tagged plant', 'Long and Bernacchi (2003); Riches et al. (2020)'],
    ['Transpiration rate (mmol H₂O m⁻² s⁻¹)', 'same reading', 'same leaf', 'Long and Bernacchi (2003)'],
    ['Stomatal conductance (mol H₂O m⁻² s⁻¹)', 'same reading (intercellular CO₂ also recorded)', 'same leaf', 'Long and Bernacchi (2003)'],
    ['Leaf area index (m² m⁻²)', 'plant canopy analyser: one reading above and four below the canopy across the rows, with a view cap that hides the operator', 'every subplot', 'Bréda (2003); Goyal et al. (2021)']],
    'Biochemical and biophysical parameters, methods and units. Pigments, anthocyanin and protein are expressed per gram of fresh weight; µg mg⁻¹ equals mg g⁻¹.', [2400, 3200, 1800, 1906], 15)
P('**Formulas.** Pigments in µg mL⁻¹ of DMSO extract for a spectrophotometer of 1–4 nm resolution (Wellburn, 1994); they are converted to mg g⁻¹ fresh weight with the extract volume and sample weight. The anthocyanin content is expressed as cyanidin-3-glucoside equivalents (molecular weight 449.2 g mol⁻¹, molar absorptivity 26 900 L mol⁻¹ cm⁻¹; Lee et al., 2005).')
EQ('C_{a} = 12.47 A_{665} − 3.62 A_{649};    C_{b} = 25.06 A_{649} − 6.5 A_{665};    C_{x+c} = (1000 A_{480} − 1.29 C_{a} − 53.78 C_{b}) / 220')
EQ('A = (A_{520} − A_{700})_{pH 1.0} − (A_{520} − A_{700})_{pH 4.5};    anthocyanin (mg L^{−1}) = A × 449.2 × dilution × 1000 / (26 900 × path length)')
EQ('RWC (%) = (FW − DW) / (TW − DW) × 100;    membrane stability index (%) = [1 − (C_{1} / C_{2})] × 100')
TAB('physex', [['Parameter (dummy data)', 'Readings', 'Result'],
    ['Chlorophyll a, b and carotenoids', 'A₆₆₅ = 0.62, A₆₄₉ = 0.25, A₄₈₀ = 0.40; 0.1 g in 10 mL', 'C_a = 6.83, C_b = 2.24, C_x+c = 1.23 µg mL⁻¹ → 0.68, 0.22 and 0.12 mg g⁻¹ fresh weight'],
    ['Anthocyanin', '(A₅₂₀ − A₇₀₀) = 0.230 at pH 1.0 and 0.045 at pH 4.5; 0.5 g in 5 mL', 'A = 0.185 → 3.09 mg L⁻¹ → 30.9 µg g⁻¹ fresh weight'],
    ['Relative water content', 'FW = 0.52 g, TW = 0.60 g, DW = 0.10 g', '(0.52 − 0.10) / (0.60 − 0.10) × 100 = 84%'],
    ['Membrane stability index', 'C₁ = 120 µS cm⁻¹, C₂ = 600 µS cm⁻¹', '[1 − 120/600] × 100 = 80%']],
    'Worked examples of the calculations (dummy data).', [2400, 3800, 3106])
CARD('irga', 'Leaf gas exchange with a portable infrared gas analyser (LI-6400)', 'Air of known CO₂ and water-vapour concentration flows through a leaf chamber; infrared gas analysers measure the concentrations before and after the leaf, and the differences give net photosynthesis, transpiration and stomatal conductance.',
     'Measures the physiological activity of the leaf directly, which explains canopy temperature (transpiration) and photosynthesis-related spectral indices.', 'Leaf L3 of a tagged plant; LED light 1200 µmol m⁻² s⁻¹; reference CO₂ 400 µmol mol⁻¹; flow 500 µmol s⁻¹; readings after stabilisation; 09:30–11:30 h.',
     'Chamber settings fixed for all dates; readings accepted when CO₂ and water differences are stable; instrument zeroed and matched before each session.', 'Field leaves under stable mid-morning light; one leaf per plot because each reading takes several minutes.',
     'The standard method for leaf photosynthesis, transpiration and stomatal conductance; stomatal conductance explained canopy temperature in airborne disease detection (Calderón et al., 2013).', 'Long and Bernacchi (2003); Riches et al. (2020)')
CARD('lai', 'Leaf area index with a plant canopy analyser', 'A fish-eye optical sensor compares diffuse light above and below the canopy at several view angles; the gap fraction is inverted to leaf area per ground area.',
     'Gives canopy size, which changes with growth stage and with disease and affects every canopy spectral feature.', 'One above and four below readings per subplot, view cap, diffuse light.',
     'No tuning; readings only under diffuse light, the same sensor and view cap on all dates.', 'Row crops with closed or nearly closed canopies.',
     'Fast, non-destructive and used for mustard at IARI (Goyal et al., 2021); separates canopy-size effects from disease effects.', 'Bréda (2003); Goyal et al. (2021)')
'''
patch('mf3_body.py', [
 ("\n# ---------------------------------------------------------------- B\nH2('Activity B – Image pre-processing')", "\n" + A8 + "\n# ---------------------------------------------------------------- B\nH2('Activity B – Image pre-processing')"),
 ("['A. Field experiment, ground truth and datasets', 'A1–A7', 'labelled subplot list; ASD leaf spectra; covariates; post- and pre-symptomatic datasets; Bharatpur validation dataset']",
  "['A. Field experiment, ground truth and datasets', 'A1–A8', 'labelled subplot list; ASD leaf spectra; covariates; post- and pre-symptomatic datasets; Bharatpur validation dataset; biochemical and biophysical parameters']"),
 (" ['ASD', 'Analytical Spectral Devices field spectroradiometer (leaf spectra)', 'L3, L5, LL', '3rd and 5th fully expanded leaf from the top; lowest green leaf'],",
  " ['ASD', 'Analytical Spectral Devices field spectroradiometer (leaf spectra)', 'L3, L5, LL', '3rd and 5th fully expanded leaf from the top; lowest green leaf'],\n ['DMSO', 'dimethyl sulfoxide (pigment extraction solvent)', 'IRGA', 'infrared gas analyser (LI-6400 portable gas exchange system)'],\n ['LAI', 'leaf area index', 'RWC', 'relative water content'],\n ['MSI', 'membrane stability index (the moisture stress index is written in full)', 'FW, TW, DW', 'fresh, turgid and dry weight'],"),
 ("['Validation', 'first stage: IARI field",
  "['Biochemical and biophysical parameters', 'chlorophyll a and b, carotenoids, anthocyanin, protein, relative water content, membrane stability index, photosynthesis, transpiration, stomatal conductance, leaf area index; 1 designated subplot per plot on 4 dates (1 pre-, 3 post-symptomatic)'], ['Validation', 'first stage: IARI field"),
 ("water (NDWI, MSI, NDII, WBI)", "water (NDWI, moisture stress index, NDII, WBI)"),
])

# ------------------------------------------------------------------ objective 1: Activity 1.7, objective 3 step, objective 2 interpretation
ACT17 = r'''H2('Activity 1.7 – Biochemical and biophysical basis of the camera responses')
P('Activity 1.7 uses the parameters of Step A8 to show what white rust does to the plant and to explain the camera responses. The parameters are not inputs to any model; they are measured on one designated subplot per plot, which is the experimental unit of the field design (Hurlbert, 1984). Statistics are kept to what each question needs ([[F:obj1phys]]).')
FIG('obj1phys', 'g29_physio.png', 'Flow chart of Activity 1.7 (Steps 1.7.1–1.7.6).', 540)
STEP('1.7.1', 'Data preparation',
     'Laboratory and field readings must be on one scale and joined to the image data before analysis.',
     'Parameter table (Step A8); severity grades; covariates; UAV features of the designated subplots.',
     'One analysis table: plot-date rows with the 11 parameters, plot percent disease index, designated-subplot canopy score and camera features, growth stage, variety and inoculation timing → Steps 1.7.2–1.7.6.',
     ['Average technical replicates (duplicate absorbance or conductivity readings).', 'Express pigments, anthocyanin and protein per gram of fresh weight; keep the units of Table [[T:physio]].', 'Join by date, plot and designated subplot.'],
     'Gomez and Gomez (1984).')
STEP('1.7.2', 'Effect of white rust on the parameters',
     'Shows whether, and how much, infection changes each parameter on each date.',
     'Analysis table; the 12 treatments (variety × inoculation timing).',
     'Mean difference (inoculated − healthy) with 95% confidence interval for each parameter and date → interpretation; 18 January → Step 3.1.2.',
     ['For each treatment and date, pair the mean of its three inoculated plots with its healthy plot (12 pairs per date).', 'Test the paired differences with a paired t-test, or the Wilcoxon signed-rank test when the differences are clearly not normal.', 'Report the mean difference, its 95% confidence interval and the effect size (mean difference divided by the standard deviation of the differences).'],
     'Paired designs and tests: Gomez and Gomez (1984), Wilcoxon (1945); effect sizes instead of p-values alone: Sullivan and Feinn (2012).')
P('Pairing compares plots of the same variety and sowing date on the same day, which removes crop-age, date and weather effects. The healthy plots lie in a separate, fungicide-protected block, so the differences can also contain small block and fungicide effects; this is stated with the results.')
STEP('1.7.3', 'Effect of variety and inoculation timing',
     'Shows whether varieties or crop ages at inoculation differ in their physiological response, as expected from a factorial field experiment.',
     'Inoculated plots (36 per date).',
     'Two-way analysis of variance tables and treatment means → interpretation of variety and timing effects.',
     ['For each parameter and date, fit a two-way analysis of variance for a randomised block design: replication + variety + inoculation timing + variety × inoculation timing.', 'Compare means with the least significant difference at 5% when the F-test is significant.'],
     'Analysis of factorial experiments in randomised block designs: Gomez and Gomez (1984).')
STEP('1.7.4', 'Comparison of growth stages',
     'White rust may affect the plant more at one growth stage than at another; stage also changes the parameters in healthy plants.',
     'Analysis table with the BBCH growth stage of every plot and date.',
     'Parameter means by stage (healthy plots), disease effect by stage, and a test of whether the disease effect differs between stages → interpretation of stage-dependent camera responses.',
     ['Healthy reference: mean ± standard error of each parameter for the vegetative, flowering and pod-formation stages, healthy plots only.',
      'Disease effect by stage: the paired differences of Step 1.7.2 grouped by stage, each with its mean and 95% confidence interval.',
      'Difference between stages: one-way analysis of variance on the paired differences with stage as the factor (Kruskal–Wallis test if the differences are not normal), followed by Tukey comparisons; a linear mixed model with plot as a random effect is the stricter alternative for the repeated dates.',
      'Report the number of plots in every stage × date cell.'],
     'Kruskal and Wallis (1952); Tukey (1949); mixed models for repeated measurements: Bates et al. (2015); growth-stage dependence of disease signals: Blasch et al. (2023); flowering and Brassica canopy spectra: Sulik and Long (2016).')
TAB('stageex', [['Growth stage (dummy)', 'Healthy', 'Inoculated', 'Difference (95% confidence interval)'], ['Vegetative', '2.10', '1.95', '−0.15 (−0.30 to 0.00)'], ['Flowering', '1.85', '1.45', '−0.40 (−0.58 to −0.22)'], ['Pod formation', '1.30', '1.05', '−0.25 (−0.42 to −0.08)']],
    'Worked example (dummy data): total chlorophyll (mg g⁻¹ fresh weight) by growth stage; the disease effect is largest at flowering.', [2200, 1800, 1800, 3506])
STEP('1.7.5', 'Relation of the parameters with disease severity',
     'Shows which parameters change in proportion to severity, not only between healthy and diseased plants.',
     'Inoculated plots; plot percent disease index; designated-subplot canopy score.',
     'Correlation coefficients with 95% confidence intervals for each parameter and post-symptomatic date → interpretation.',
     ['Compute the Pearson correlation of each parameter with the plot percent disease index and with the canopy score of the designated subplot, separately for each post-symptomatic date (36 plots per date).', 'Do not pool dates directly: if a pooled value is wanted, remove the date means first (within-date correlation), because parameters and severity both change with time.'],
     'Correlation with repeated observations: Bland and Altman (1995), Bakdash and Marusich (2017).')
STEP('1.7.6', 'Relation of the parameters with the camera features',
     'Links each camera feature to a plant process, which shows why the feature responds to white rust.',
     'Parameters and the camera features of the designated subplots (selected features of Activities 1.2–1.6 and the indices of Table [[T:traitlinks]]).',
     'Parameter × feature correlation heat maps for each date and growth stage; check of the expected links → interpretation of Objectives 1 and 2.',
     ['Compute Pearson correlations between each parameter and each selected camera feature within each date (48 designated subplots), and within each growth stage.', 'Control false discoveries over the many pairs with the Benjamini–Hochberg procedure (5%).', 'Compare the strongest links with the expected links of Table [[T:traitlinks]].'],
     'Benjamini and Hochberg (1995); physiological traits explaining spectral and thermal disease signals: Calderón et al. (2013), Zarco-Tejada et al. (2018), Poblete et al. (2023).')
TAB('traitlinks', [['Parameter', 'Expected camera features', 'Why', 'References'],
    ['Chlorophyll a, b', 'red-edge position, CIrededge, MTCI, NDRE, PSSR, White Rust Index', 'chlorophyll absorbs red light and sets the position of the red edge', 'Gitelson et al. (2003); Filella and Peñuelas (1994)'],
    ['Carotenoids', 'PRI, PSRI', 'carotenoid/chlorophyll ratio changes with stress and senescence', 'Gamon et al. (1992); Merzlyak et al. (1999)'],
    ['Anthocyanin', 'anthocyanin reflectance index (ARI)', 'anthocyanin absorbs green light near 550 nm', 'Gitelson et al. (2001)'],
    ['Relative water content', 'NDWI, NDII, water index, moisture stress index; canopy minus air temperature', 'water absorbs near 970, 1200, 1450 and 1650 nm; water loss warms the canopy', 'Gao (1996); Peñuelas et al. (1997); Jones et al. (2009)'],
    ['Stomatal conductance, transpiration', 'canopy minus air temperature, normalised relative canopy temperature, crop water stress index', 'transpiration cools the leaves', 'Jones et al. (2009); Calderón et al. (2013)'],
    ['Net photosynthesis', 'PRI, chlorophyll indices', 'PRI follows xanthophyll changes linked to light use', 'Gamon et al. (1992)'],
    ['Membrane stability index', 'near-infrared plateau, texture features', 'tissue damage around pustules changes leaf structure and canopy pattern', 'Mahlein (2016)'],
    ['Protein', 'red-edge features', 'leaf protein follows leaf nitrogen and chlorophyll', 'Filella and Peñuelas (1994)'],
    ['Leaf area index', 'NDVI, OSAVI, MSR, texture features', 'canopy size controls near-infrared scattering and canopy cover', 'Haboudane et al. (2004)']],
    'Expected links between the parameters and the camera features, checked in Step 1.7.6.', [1900, 2900, 2700, 1806], 15)
FIG('physdummy', 'g30_dummy_physio.png', 'Dummy example: (a) chlorophyll of healthy and inoculated plots by growth stage; (b) correlation heat map between parameters and camera features on one date.', 560)
CARD('physstats', 'Statistical analysis of the biochemical and biophysical parameters', 'Paired comparisons isolate the disease effect within the same variety, sowing date and day; analysis of variance tests treatment factors in the randomised block design; within-date correlations measure the strength of relations without the time trend.',
     'Answers whether white rust changes a parameter, at which growth stage most, and which camera features follow which parameter, without pseudo-replication.', 'Paired t-test or Wilcoxon signed-rank test (12 pairs per date); two-way analysis of variance (36 inoculated plots per date); one-way analysis of variance or Kruskal–Wallis test on paired differences by stage; Pearson correlation within dates; Benjamini–Hochberg control of false discoveries.',
     'Significance level 5%; false discovery rate 5%; effect sizes and 95% confidence intervals reported with every test.', 'Plot-level measurements from designed field experiments with few replications.',
     'Simple, standard in agricultural research and matched to the design; the plot is treated as the experimental unit.', 'Gomez and Gomez (1984); Hurlbert (1984); Benjamini and Hochberg (1995); Sullivan and Feinn (2012)')

'''
patch('mf3_obj.py', [
 ("BOX('Link to satellite monitoring (optional extension, not part of the six-month plan).'", ACT17 + "BOX('Link to satellite monitoring (optional extension, not part of the six-month plan).'"),
 ("    ['1.6 Disease-specific feature sets', '1.6.1–1.6.4', 'same rules for other cameras → variance inflation factor', 'feature set of each camera; treatment response']],",
  "    ['1.6 Disease-specific feature sets', '1.6.1–1.6.4', 'same rules for other cameras → variance inflation factor', 'feature set of each camera; treatment response'],\n    ['1.7 Biochemical and biophysical basis', '1.7.1–1.7.6', 'paired comparisons, analysis of variance, within-date correlation', 'disease effect by date and growth stage; parameter–feature links']],"),
 ("     ['Compute SHAP values of the best machine-learning model of each task; summarise the mean |SHAP| per feature and per camera.',",
  "     ['Compute SHAP values of the best machine-learning model of each task; summarise the mean |SHAP| per feature and per camera.', 'Compare the most important features with the biochemical and biophysical parameters that changed with disease (Activity 1.7), to give the model a physiological explanation.',"),
 ("H2('Activity 3.2 – Normalisation to healthy plots')",
  """STEP('3.1.2', 'Physiological changes before symptoms (18 January 2027)',
     'If pigments, water status or gas exchange already change before pustules appear, there is a physiological reason why pre-symptomatic detection can work.',
     'Biochemical and biophysical parameters of 18 January (Step A8); later severity of the same plots.',
     'Inoculated − healthy differences on the pre-symptomatic date and their relation with later severity → interpretation of Objective 3.',
     ['Compare inoculated and healthy plots for every parameter with the paired comparison of Step 1.7.2 (12 pairs).', 'Correlate the pre-symptomatic parameters of the inoculated plots with their percent disease index on 28 January (first post-symptomatic sampling date).', 'Report effect sizes and 95% confidence intervals; note the block and fungicide caveat of Step 1.7.2.'],
     'Pre-visual physiological changes behind early detection: Zarco-Tejada et al. (2018), Calderón et al. (2013); pre-symptomatic hyperspectral detection: Zhu et al. (2017).')
H2('Activity 3.2 – Normalisation to healthy plots')"""),
])

# ------------------------------------------------------------------ end: chain, changes, index rename, plan, Q&A
patch('mf3_end.py', [
 (" ['A7', 'Bharatpur research farms and farmers\\' fields',", " ['A8', 'designated subplots, laboratory and field instruments', 'biochemical and biophysical parameters (48 plots × 4 dates)', '1.7, 3.1.2'],\n ['A7', 'Bharatpur research farms and farmers\\' fields',"),
 (" ['1.6.1–1.6.4', 'survivors of all groups', 'disease-specific feature set of each camera', '2.1.2, 3.3.1'],", " ['1.6.1–1.6.4', 'survivors of all groups', 'disease-specific feature set of each camera', '2.1.2, 3.3.1'],\n ['1.7.1–1.7.6', 'biochemical and biophysical parameters; camera features', 'disease effect by date and stage; parameter–feature links', 'interpretation of Objectives 1–3; 2.5.4'],"),
 (" ['Validation', 'IARI field only',", " ['Biochemical and biophysical parameters', 'not included', 'Step A8 and Activity 1.7: 11 parameters on 4 dates with paired comparisons, analysis of variance, growth-stage comparison and parameter–feature correlations', 'user request; physiological basis'],\n ['Validation', 'IARI field only',"),
 ("['', 'MSI', 'R_{1600}/R_{820}', 'Hunt and Rock 1989']", "['', 'Moisture stress index', 'R_{1600}/R_{820}', 'Hunt and Rock 1989']"),
 ("['3', 'Activities 1.2–1.6; selection code tested inside folds',", "['3', 'Activities 1.2–1.7; selection code tested inside folds; analysis of the biochemical and biophysical parameters',"),
 ("    ('How do you know the models work outside the IARI field?',",
  "    ('Why are the biochemical and biophysical parameters measured at plot level?', 'The plot is the experimental unit of the randomised block design (Hurlbert, 1984). One designated subplot per plot keeps the gas-exchange readings inside the mid-morning window and links each sample to the UAV features of that subplot; the parameters explain the camera responses and are not model inputs (Calderón et al., 2013).'),\n    ('How do you know the models work outside the IARI field?',"),
])
print('patched v4')
