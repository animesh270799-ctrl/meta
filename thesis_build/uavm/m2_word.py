"""Detailed Word report of the plot-level disease maps (UAV hyperspectral image of 24 Feb 2026, best ASD models).
Writes the shared content (tables, figures, methods, interpretations, findings) used by the Excel workbook and the slides.
python3 m2_word.py && NODE_PATH=/opt/node22/lib/node_modules node m2_build.js && python3 ../satmet/to_pdf.py <docx> <pdf>"""
import json, re, os, sys, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'; S = HERE + '../'; O = HERE + 'out/'; T = S + 'uavt/out/'
sys.path.insert(0, S + 'asd26'); import a_refs
OUTF = S + 'outputs/UAV_24Feb2026_disease_maps_report.docx'
K = []; TABLES = []; FIGS = []; INTERP = {}
def esc(t):
    t = t.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${'); t = re.sub(r'_(?!\{)', r'\\\\_', t)
    return re.sub(r'\[\[(T|F):(\w+)\]\]', lambda m: '${%s(\'%s\')}' % (m.group(1), m.group(2)), t)
def js(s): return '`' + esc(s) + '`'
def H1(t): K.append("K.push(H1(%s));" % js(t))
def H2(t): K.append("K.push(H2(%s));" % js(t))
def P(t): K.append("K.push(P(%s));" % js(t))
def BL(items): K.extend("K.push(BL(%s));" % js(i) for i in items)
def NL(items): K.extend("K.push(NL(%s));" % js(i) for i in items)
def BOX(l, t, fill='FFF6E0', line='C98A00'): K.append("K.push(BOX(%s, %s, '%s', '%s'));" % (js(l), js(t), fill, line))
def EQ(t, lab): K.append("K.push(EQ(%s, %s));" % (js(t), js(lab)))
def FIG(k, file, cap, w=620):
    FIGS.append(dict(key=k, file=file, caption=cap)); K.append("K.push(...fig2('%s', '%s', %s, %d));" % (k, file, js(cap), w))
def TAB(k, rows, cap, widths=None, size=16):
    if widths is None:
        L = [min(max(max(len(str(r[j])) for r in rows), 5), 46) for j in range(len(rows[0]))]; s = sum(L); widths = [int(9306 * x / s) for x in L]
    TABLES.append(dict(key=k, caption=cap, rows=[[str(c) for c in r] for r in rows]))
    R = '[' + ',\n'.join('[' + ', '.join(js(str(c)) for c in r) + ']' for r in rows) + ']'
    K.append("K.push(...tab2('%s', %s, %s, %s, %d));" % (k, R, json.dumps(widths), js(cap), size))
def PB(): K.append("K.push(new Paragraph({ children: [new PageBreak()] }));")
def INT(key, parts):
    INTERP[key] = parts
    for lead, txt in parts: P('**%s** %s' % (lead, txt))
f2 = lambda x: '–' if x is None or (isinstance(x, float) and not np.isfinite(x)) else '%.2f' % x
f3 = lambda x: '–' if x is None or (isinstance(x, float) and not np.isfinite(x)) else '%.3f' % x

# ---------------- data
TB = pd.read_csv(O + 'map_table.csv'); MO = pd.read_csv(O + 'moran.csv'); MS = json.load(open(O + 'map_summary.json'))
SB = {k: pd.read_csv(O + 'summary_by_%s.csv' % k) for k in ('block', 'sowing', 'variety')}
MF = pd.read_csv(T + 'metrics_frozen.csv'); MU = pd.read_csv(T + 'metrics_uav_trained.csv'); BM = pd.read_csv(T + 'best_models.csv')
best, bv = MS['best'], MS['best_variant']; VSH = {'Direct': 'direct', 'Healthy-reference corrected': 'corrected', 'Corrected + brightness-normalised': 'normalised'}
VAR = list(VSH)
m = lambda t: MF[(MF.task == t) & (MF.model == best[t]['overall']) & (MF.variant == bv[t])].iloc[0]
mu = {t: MU[MU.task == t].iloc[0] for t in 'ABC'}; asd = lambda t: float(BM[(BM.task == t) & (BM.role == 'overall')].asd_value.iloc[0])
tg = {t: VSH[bv[t]] for t in 'ABC'}
dis = TB[TB.status == 'Diseased']
nb = MS['n_neighbour_pairs']
def mo(tag, var): r = MO[(MO.tag == tag) & (MO.variable.str.startswith(var))]; return r.iloc[0] if len(r) else None
cnt = lambda col: TB[col].value_counts().to_dict()
nPredD = int((TB['A_%s' % tg['A']] == 1).sum()); nPredDu = int((TB.A_uav == 1).sum())

def findings_list():
    a, c = m('A'), m('C'); I_b, I_u = mo(tg['C'], 'C residual'), mo('uav', 'C residual'); I_t = mo('truth', 'True plot mean score')
    return ['Maps were made for all 48 plots of the 24 Feb 2026 image from the plot predictions of the best ASD models (%s for detection, %s for grades, %s for the score) and, for comparison, the models trained on the UAV plots.' % (best['A']['overall'], best['B']['overall'], best['C']['overall']),
            'True map: the 12 sprayed plots were healthy and the 36 unsprayed plots diseased (mean score %.1f–%.1f); true severity was spatially clustered (Moran\'s I %.2f, p = %.3f).' % (dis.score.min(), dis.score.max(), I_t.moran_I, I_t.p_value),
            'Best ASD detection map (%s input): %d of 48 plots mapped diseased (true 36); %d correct (sensitivity %.2f, specificity %.2f).' % (tg['A'], nPredD, int(TB['A_%s_cat' % tg['A']].isin(['TP', 'TN']).sum()), a.sensitivity, a.specificity),
            'Best ASD score map (%s input): R² %.2f, RMSE %.2f; predicted scores %.1f–%.1f vs true %.1f–%.1f; residuals %s (Moran\'s I %.2f, p = %.3f).' % (tg['C'], c.R2, c.RMSE, TB['C_%s' % tg['C']].min(), TB['C_%s' % tg['C']].max(), TB.score.min(), TB.score.max(), 'spatially clustered' if I_b.p_value < 0.05 else 'not spatially clustered', I_b.moran_I, I_b.p_value),
            'UAV-trained maps: detection %d of 48 correct (macro-F1 %.2f); score R² %.2f (residual Moran\'s I %.2f, p = %.3f).' % (int(TB.A_uav_cat.isin(['TP', 'TN']).sum()), mu['A'].macro_F1, mu['C'].R2, I_u.moran_I, I_u.p_value),
            'The frozen leaf models do not give usable disease maps of the canopy; the UAV-trained detection map is the most reliable map; severity maps need more UAV training data. A pixel-level map needs the image cube (ENVI .dat/.hdr).']

# ================================================================== title and summary
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 900, after: 200 }, children: [new TextRun({ text: 'Disease maps of white rust from the UAV hyperspectral image of 24 February 2026', font: FONT, size: 42, bold: true, color: '1E3A1F' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [new TextRun({ text: 'Plot-level maps from the best 2025-26 ASD models (and the UAV-trained check): method, accuracy, error maps, spatial pattern and interpretation', font: FONT, size: 27, color: '2C5F2D' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 500 }, children: [new TextRun({ text: 'Animesh Panda | Ph.D. Agricultural Physics | ICAR-Indian Agricultural Research Institute, New Delhi', font: FONT, size: 22, bold: true })] }));")
BOX('Summary of results.', ' '.join('**%d.** %s' % (i + 1, f) for i, f in enumerate(findings_list())), 'E8F5E9', '2E7D32')
BOX('How to read this report and the companion files.', 'Chapter 2 explains each mapping step (position, concept, justification, what published studies did, how it is done, how it was applied here, output, notes and a likely question). Chapter 3 shows each map with what is shown, how to read it, the result, its interpretation and its link to the literature. '
    'Every table and figure is also in the Excel workbook (UAV_24Feb2026_disease_maps.xlsx: field maps drawn with live formulas and colour scales, Moran\'s I computed with formulas, a step-by-step guide) and in the slides (UAV_24Feb2026_disease_maps.pptx). The predictions come from the transfer test (UAV_24Feb2026_ASD_model_transfer report).')
PB()
K.append("K.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: 'Contents', font: FONT, size: 32, bold: true, color: '1E3A1F' })] }));")
K.append("K.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-2' }));")
PB()

# ================================================================== 1 introduction
H1('1. Introduction')
P('A disease map shows where in the field disease occurs and how severe it is. It is the practical product of UAV disease sensing: it guides scouting, targeted spraying and the assessment of resistance trials (Mahlein, 2016; Zhang et al., 2019). '
  'Maps are made by applying a trained model to every mapping unit of an image (pixel, subplot or plot) and colouring the units by the predicted class or value; their accuracy is then checked against field observations (Congalton, 1991; Foody, 2002).')
P('This report applies the best models of the 2025-26 ASD leaf analysis to the 48 plots of the UAV hyperspectral image of 24 February 2026 and maps the predicted disease status, grade and severity score. Because the transfer test showed that the leaf models do not transfer well to the canopy, the maps of the models trained on the UAV plots are shown for comparison. '
  'The mapping unit is the plot, because only plot mean spectra are available; a pixel-level map needs the image cube.')
TAB('qs', [['Question', 'Answer in'], ['What do the true disease maps of 24 Feb look like?', 'Section 3.1'], ['What do the maps of the best ASD models show?', 'Sections 3.2–3.4'],
           ['Where are the errors, and are they spatially clustered?', 'Sections 3.3, 3.6'], ['How do the UAV-trained maps compare?', 'Section 3.5'], ['Do errors differ between blocks, sowing dates and varieties?', 'Section 3.7']],
    'Questions answered in this report.', [6000, 3306])

# ================================================================== 2 methodology
H1('2. Methodology (step by step)')
STEPS = [
 dict(no='D1', title='Inputs: plot predictions and ground truth', position='First step: the values to be mapped.',
      concept='Each plot has one predicted status (healthy/diseased), one predicted grade (0, 1, 3, 5, 7, 9) and one predicted score (0–9) from each model and input, and one true value of each from the ASD leaf scores of the same day.',
      why='A map is only as good as the predictions behind it; using the predictions and truth of the transfer test keeps the maps consistent with its accuracy figures.',
      papers='Map products are derived from per-unit model predictions and validated with independent ground truth (Congalton, 1991; Olofsson et al., 2014).',
      how=['Take the per-plot predictions of the best overall ASD model of each task for the three inputs (direct, healthy-reference corrected, brightness-normalised), and the out-of-fold predictions of the UAV-trained models.',
           'Take the ground truth: status (sprayed = healthy), plot mean leaf score, nearest grade and PDI.',
           'For each map, use the input that gave the best accuracy for that task (detection: %s; grades: %s; score: %s); maps of all inputs are in the Excel file.' % (tg['A'], tg['B'], tg['C'])],
      mine='Best models: %s (A), %s (B), %s (C); UAV-trained: %s (A), %s (B), %s (C).' % (best['A']['overall'], best['B']['overall'], best['C']['overall'], MS['uav_models']['A'], MS['uav_models']['B'], MS['uav_models']['C']),
      output='Plot table of truth, predictions and errors (Excel sheet 1_Plot_table).', notes='Out-of-fold predictions are used for the UAV-trained maps, so every plot is predicted by a model that did not see it.', question='Why use out-of-fold predictions? A map from a model fitted on the same plots would look better than it is.', eqs=[]),
 dict(no='D2', title='Field layout and plot polygons', position='Second step: where each value is drawn.',
      concept='Each plot is drawn as a rectangle in its position in the field; for a georeferenced map the same values are joined to the plot polygons of the image.',
      why='Maps reveal spatial patterns (blocks, sowing strips, field edges, flight lines) that tables hide.',
      papers='Plot polygons are digitised over the orthomosaic and joined to plot attributes in GIS (Aasen et al., 2018).',
      how=['Read the plot arrangement of the experiment (plot number, sowing date, variety, block) from the field layout; check that every plot carries the same treatment as in the 2025-26 records.',
           'Draw the 48 plots in their rows and columns (schematic, not to scale) with the block labels Healthy, R3, R2, R1.',
           'Define rook neighbours (plots sharing a side within the same block) for the spatial analysis (%d neighbour pairs).' % nb,
           'For a georeferenced map, join the plot table to the plot polygons (field "plot no.") in ArcMap/QGIS and colour them with the same classes.'],
      mine='The layout (acm/layout.json) matched the treatment of all 48 plots.', output='Plot positions and the neighbour matrix (Excel sheets 2_Field_maps and 4_Neighbours).',
      notes='Distances in the schematic are not to scale; the spatial analysis uses only adjacency, which is the same in the real field.', question='Why a schematic map? The image cube and polygons were not part of the uploaded data; the adjacency of the plots is exact.', eqs=[]),
 dict(no='D3', title='Map classes and colour scales', position='Third step: how values become colours.',
      concept='Categorical maps use one colour per class (status, grade, outcome); continuous maps use a sequential scale (score) or a diverging scale centred on zero (errors).',
      why='Consistent, perceptually ordered colours make maps comparable and readable, also for colour-blind readers.',
      papers='Sequential and diverging colour schemes for maps (Harrower and Brewer, 2003); disease grades follow the 0–9 key (Conn et al., 1990).',
      how=['Status: green = healthy, red = diseased.', 'Grade: green (0) → yellow (1) → orange (3, 5) → red (7) → dark red (9).', 'Score: yellow–orange–red scale from 0 to 9 (the same limits on every map).',
           'Detection outcome: TP red, TN green, FP orange (false alarm), FN blue (missed disease).', 'Errors: blue (under-prediction) – white (0) – red (over-prediction), symmetric limits.'],
      mine='Fixed colour limits (score 0–9; score error ±4; grade error ±5 steps) so maps of different models can be compared directly.', output='Maps m01–m06 (Figures 2–7).', notes='Excel uses the same scales with conditional formatting.', question='Why fixed colour limits? Rescaling each map to its own range would exaggerate small differences.', eqs=[]),
 dict(no='D4', title='Map accuracy', position='Fourth step: how good each map is.',
      concept='The map is compared plot by plot with the ground truth; agreement is summarised by the same measures as in the transfer test.',
      why='A map without an accuracy statement cannot be used for decisions.',
      papers='Error (confusion) matrices and overall, producer\'s and user\'s accuracy are the standard of map accuracy assessment (Congalton, 1991; Foody, 2002; Olofsson et al., 2014).',
      how=['Detection maps: confusion matrix, overall accuracy, sensitivity (producer\'s accuracy of the diseased class) and specificity.', 'Grade maps: share of plots within one grade.', 'Score maps: R², RMSE and the mean error.'],
      mine='Accuracy of the best ASD maps and of the UAV-trained maps (Table "Map accuracy").', output='Accuracy table and outcome maps.', notes='With 48 plots the accuracy has wide confidence intervals (transfer report, Appendix F).', question='What is producer\'s accuracy? The share of truly diseased plots that the map shows as diseased (= sensitivity).',
      eqs=[('Overall accuracy = (TP + TN) / N', 'D4.1'), ('RMSE = √[Σ (ŷ_{i} − y_{i})² / N]', 'D4.2')]),
 dict(no='D5', title='Error maps and spatial autocorrelation (Moran\'s I)', position='Fifth step: are the errors random in space?',
      concept='Moran\'s I measures whether neighbouring plots have similar values: I > E(I) means clustering, I ≈ E(I) = −1/(n − 1) means no spatial pattern.',
      why='Clustered errors point to a spatial cause (illumination, flight line, block or sowing-strip effect) rather than random model error, and indicate where a correction is needed.',
      papers='Moran\'s I (Moran, 1950) with a permutation test (Cliff and Ord, 1981) is the standard test of spatial autocorrelation; ignoring it biases inference (Legendre, 1993; Dormann et al., 2007).',
      how=['Compute the errors of each map (score residual = predicted − true; detection error 1/0; grade steps).', 'Compute Moran\'s I with the rook neighbour matrix W.', 'Permute the values among the plots 999 times and compute I each time; p = share of permuted I ≥ observed.', 'Do the same for the true score to describe the natural pattern of the disease.'],
      mine='%d rook neighbour pairs among the 48 plots; 999 permutations.' % nb, output='Moran\'s I table (Excel sheet 4_Neighbours computes I with formulas).', notes='Local indicators (LISA; Anselin, 1995) would locate the clusters; with 48 plots the global test is sufficient.', question='Why a permutation test? It needs no assumption about the distribution of the errors.',
      eqs=[('I = (n / S_{0}) × Σ_{i} Σ_{j} w_{ij} z_{i} z_{j} / Σ_{i} z_{i}²,  z_{i} = x_{i} − x̄,  S_{0} = Σ_{i} Σ_{j} w_{ij}', 'D5.1'), ('E(I) = −1 / (n − 1)', 'D5.2')]),
 dict(no='D6', title='Errors by block, sowing date and variety', position='Sixth step: which groups are mapped worse.',
      concept='Mean errors and accuracy are computed for each block (Healthy, R1, R2, R3), sowing date (D1–D4) and variety (V1–V3).',
      why='Systematic errors in one group (e.g. a darker sowing strip) show what drives the map errors.',
      papers='Stratified accuracy assessment reports accuracy per stratum (Olofsson et al., 2014).',
      how=['Group the plot table by block, sowing date and variety.', 'Compute detection accuracy, share within one grade, mean predicted score and mean score error per group.'],
      mine='Summaries for the best ASD maps and the UAV-trained maps.', output='Group tables and Figure "group errors".', notes='Groups have 9–12 plots, so only large differences are meaningful.', question='Why look at sowing dates? Plot brightness differed by sowing date (UAV spectra workbook), which can bias the maps.', eqs=[]),
 dict(no='D7', title='From plot maps to pixel maps (next step)', position='Last step: how the full-resolution map will be made.',
      concept='A pixel map applies the model to every crop pixel of the image and colours each pixel; plot or subplot maps aggregate the pixels.',
      why='Pixel maps show the disease pattern inside plots and in farmers\' fields without plot boundaries.',
      papers='UAV hyperspectral disease maps classify crop pixels after masking soil and shadow (Zarco-Tejada et al., 2018; Bohnenkamp et al., 2019).',
      how=['Read the reflectance cube (ENVI .dat/.hdr) of 24 Feb.', 'Apply the crop mask (NDVI > 0.6 and SAM < 0.3 rad).', 'Compute the same features for every crop pixel and apply a model trained on UAV data.', 'Write the class/score raster and summarise it per plot or subplot.'],
      mine='Not done: the cube was not part of the uploaded data. With the cube, the UAV-trained models (or the 2026-27 subplot models) can be applied per pixel.', output='Planned: pixel-level status and severity rasters.', notes='Leaf models should not be applied per pixel for the same reason they fail per plot (transfer report).', question='Why not apply the ASD model to every pixel now? Without the cube there are no pixel spectra; and the leaf model does not transfer to canopy spectra.', eqs=[])]
for st in STEPS:
    H2('%s %s' % (st['no'], st['title']))
    P('**Position in the workflow.** ' + st['position']); P('**Concept.** ' + st['concept']); P('**Why it is needed here.** ' + st['why']); P('**What the reference papers did.** ' + st['papers'])
    P('**How it is done.**'); NL(st['how'])
    for e, lab in st['eqs']: EQ(e, lab)
    P('**How it was applied to these data.** ' + st['mine']); P('**Output.** ' + st['output']); P('**Notes and alternatives.** ' + st['notes']); P('**Likely question.** ' + st['question'])

# ================================================================== 3 results
H1('3. Maps, results and interpretation')
H2('3.1 True disease map of 24 Feb 2026')
FIG('truth', 'm01_truth.png', 'True maps of 24 Feb 2026: (a) status, (b) plot mean leaf score, (c) nearest grade. Numbers = plot number and value; blocks Healthy, R3, R2, R1 (schematic, not to scale).')
It = mo('truth', 'True plot mean score')
INT('truth', [('What is shown.', '[[F:truth]] shows the true status, mean leaf score and grade of every plot on the flight day.'),
    ('How to read it.', 'Each rectangle is a plot; the colour is the value, the small numbers are plot number and value.'),
    ('Result.', 'All 12 sprayed plots were healthy (score 0). Diseased plots had mean scores %.1f–%.1f (grades: %s). Moran\'s I of the true score was %.2f (expected %.2f; p = %.3f).' % (dis.score.min(), dis.score.max(), ', '.join('%d: %d' % (k, v) for k, v in sorted(cnt('grade').items())), It.moran_I, It.expected_I, It.p_value)),
    ('Interpretation.', 'The strongest pattern is the sprayed (healthy) block against the unsprayed blocks. Within the unsprayed blocks severity varies with sowing date and variety, so neighbouring plots differ; the positive Moran\'s I mainly reflects the healthy block (Legendre, 1993).')])
H2('3.2 Maps of the best ASD models')
FIG('pred', 'm02_pred_best.png', 'Maps of the best ASD models (best input per task): (a) predicted status, (b) predicted grade, (c) predicted score.')
a, b_, c = m('A'), m('B'), m('C')
INT('pred', [('What is shown.', '[[F:pred]] maps the predictions of the best ASD model of each task with its best input (detection %s, grades %s, score %s).' % (tg['A'], tg['B'], tg['C'])),
    ('How to read it.', 'Compare each panel with the true map ([[F:truth]]): the same colours mean the same classes or scores.'),
    ('Result.', 'The detection map shows %d plots as diseased (true 36), the grade map %s, and the score map ranges from %.1f to %.1f (true %.1f–%.1f).' % (nPredD, ', '.join('%d: %d' % (int(k), v) for k, v in sorted(cnt('B_%s' % tg['B']).items())), TB['C_%s' % tg['C']].min(), TB['C_%s' % tg['C']].max(), TB.score.min(), TB.score.max())),
    ('Interpretation.', 'The maps do not reproduce the true pattern: the healthy block is not separated from the diseased blocks and the predicted severity is compressed into a narrow range. This is the spatial expression of the failed leaf-to-canopy transfer (transfer report: inputs outside the leaf range; Feudale et al., 2002).')])
H2('3.3 Error maps of the best ASD models')
FIG('err', 'm03_err_best.png', 'Error maps of the best ASD models: (a) detection outcome (TP, TN, FP, FN), (b) grade error in grade steps, (c) score error (predicted − true).')
Ib = mo(tg['C'], 'C residual'); Iab = mo(tg['A'], 'A error')
INT('err', [('What is shown.', '[[F:err]] shows where the maps are right or wrong.'),
    ('How to read it.', 'Detection: green and red = correct (TN, TP), orange = false alarm (FP), blue = missed disease (FN). Errors: red = over-prediction, blue = under-prediction.'),
    ('Result.', 'Detection outcomes: %s. Mean score error %+.2f; Moran\'s I of the score error %.2f (p = %.3f) and of the detection error %.2f (p = %.3f).' % (', '.join('%s %d' % (k, v) for k, v in sorted(cnt('A_%s_cat' % tg['A']).items())), TB['C_%s_res' % tg['C']].mean(), Ib.moran_I, Ib.p_value, Iab.moran_I, Iab.p_value)),
    ('Interpretation.', ('The score errors are spatially clustered: whole groups of neighbouring plots are over- or under-predicted, which points to a spatial cause such as plot brightness by sowing strip or illumination across the image (Aasen et al., 2018) rather than random model error (Dormann et al., 2007).' if Ib.p_value < 0.05 else
                         'The score errors are not significantly clustered: the model is wrong in a similar way across the field, consistent with a general leaf–canopy mismatch rather than a local spatial artefact (Legendre, 1993).'))])
H2('3.4 Score maps of the three inputs')
FIG('var', 'm04_score_variants.png', 'Predicted score maps of the best ASD score model with the three inputs and of the UAV-trained model.')
INT('var', [('What is shown.', '[[F:var]] compares the score maps of the three inputs with the UAV-trained map.'),
    ('Result.', 'Predicted score ranges: %s; UAV-trained %.1f–%.1f.' % ('; '.join('%s %.1f–%.1f' % (VSH[v], TB['C_%s' % VSH[v]].min(), TB['C_%s' % VSH[v]].max()) for v in VAR), TB.C_uav.min(), TB.C_uav.max())),
    ('Interpretation.', 'The corrections change the level of the map but not its pattern; none separates the healthy block clearly. Correcting the spectra cannot replace training on canopy data (Pan and Yang, 2010).')])
H2('3.5 Maps of the UAV-trained models')
FIG('uav', 'm05_uav_trained.png', 'Maps of the UAV-trained models (out-of-fold, leave-one-replication-out): predictions (a–c) and errors (d–f).')
Iu = mo('uav', 'C residual')
INT('uav', [('What is shown.', '[[F:uav]] shows the maps of the best ML model types trained on the UAV plots, each plot predicted by a model that did not see it.'),
    ('Result.', 'Detection: %d of 48 plots correct (%s); %d plots mapped diseased. Score map R² %.2f, RMSE %.2f; Moran\'s I of the score error %.2f (p = %.3f).' % (int(TB.A_uav_cat.isin(['TP', 'TN']).sum()), ', '.join('%s %d' % (k, v) for k, v in sorted(cnt('A_uav_cat').items())), nPredDu, mu['C'].R2, mu['C'].RMSE, Iu.moran_I, Iu.p_value)),
    ('Interpretation.', 'The UAV-trained detection map separates the healthy block from most diseased plots and is the most useful map of this date; the severity map still flattens the differences between diseased plots because 48 plots of one date are too few to learn severity (Zhang et al., 2019).')])
H2('3.6 Disease score maps (probability of disease)')
FIG('prob', 'm06_disease_score.png', 'Continuous disease score of the detection models: (a) best ASD model, (b) UAV-trained model (decision value or probability; red = more likely diseased).')
INT('prob', [('What is shown.', '[[F:prob]] maps the continuous output behind the detection maps, which can be thresholded to trade false alarms against missed disease (Fawcett, 2006).'),
    ('Interpretation.', 'A useful score map shows the healthy block in green and the diseased blocks in red; the best ASD model\'s score map does not, the UAV-trained map largely does (AUC %s vs %s).' % (f2(mu['A'].AUC), f2(a.AUC)))])
H2('3.7 Errors by block, sowing date and variety')
FIG('grp', 'm07_group_errors.png', 'Mean score error (predicted − true) by block, sowing date and variety for the best ASD map and the UAV-trained map.')
INT('group', [('What is shown.', '[[F:grp]] and the group tables show whether some blocks, sowing dates or varieties are mapped worse than others.'),
    ('Interpretation.', 'For the best ASD map the healthy block is over-predicted (positive error) and the severely diseased plots under-predicted (negative error): the map regresses towards a middle value. Differences between sowing dates follow the plot-brightness pattern of the image (Olofsson et al., 2014).')])
rows = [['Map', 'Detection accuracy', 'Sensitivity', 'Specificity', 'Within one grade', 'Score R²', 'Score RMSE', 'Moran\'s I score error (p)']]
for lab, tag, mA, mB, mC in [('Best ASD models (best input)', None, a, b_, c), ('UAV-trained models', 'uav', mu['A'], mu['B'], mu['C'])]:
    I_ = mo(tg['C'] if tag is None else 'uav', 'C residual')
    rows.append([lab, f3((mA.sensitivity * 36 + mA.specificity * 12) / 48), f3(mA.sensitivity), f3(mA.specificity), f3(mB.within1), f3(mC.R2), f2(mC.RMSE), '%.2f (%.3f)' % (I_.moran_I, I_.p_value)])
TAB('acc', rows, 'Map accuracy against the ASD ground truth of 24 Feb 2026 (48 plots).', [2400, 1000, 900, 900, 1000, 800, 900, 1406], 15)
TAB('moran', [['Map', 'Variable', 'Moran\'s I', 'E(I)', 'p (999 permutations)']] + [[r.model, r.variable, '%.3f' % r.moran_I, '%.3f' % r.expected_I, '%.3f' % r.p_value] for r in MO.itertuples()],
    'Spatial autocorrelation (Moran\'s I, rook neighbours) of the true values and of the map errors.', [3000, 2900, 1100, 1000, 1306], 15)
for k, ttl in (('block', 'block'), ('sowing', 'sowing date'), ('variety', 'variety')):
    d = SB[k]
    TAB('g' + k, [['Group', 'Map', 'Plots', 'Mean true score', 'Detection accuracy', 'Within one grade', 'Mean predicted score', 'Mean score error']] +
        [[r.group, r.model, r.n, f2(r.mean_true_score), f2(r.A_accuracy), f2(r.B_within1), f2(r.C_mean_pred), '%+.2f' % r.C_mean_residual] for r in d.itertuples()],
        'Map accuracy and errors by %s.' % ttl, [900, 2400, 600, 1100, 1100, 1100, 1100, 1006], 15)

# ================================================================== 4 discussion, 5 conclusions
H1('4. Discussion')
BL(['**What the maps show.** The best ASD maps do not reproduce the true pattern; the UAV-trained detection map does for most plots. This mirrors the accuracy of the transfer test and confirms that mapping must use models trained on canopy data (Mahlein, 2016; Bohnenkamp et al., 2019).',
    '**Spatial errors.** %s (Legendre, 1993; Dormann et al., 2007).' % ('Clustered errors indicate a spatial cause (brightness by strip or illumination) that radiometric correction should address before mapping (Aasen et al., 2018)' if Ib.p_value < 0.05 else 'Errors without spatial clustering indicate a general model mismatch rather than a local artefact'),
    '**Accuracy statements.** Each map is given with its confusion matrix and error measures, as required for map products (Congalton, 1991; Olofsson et al., 2014).',
    '**Next step.** With the image cube, pixel maps can be made with UAV-trained models; with the 2026-27 subplot data (1536 samples per camera), severity maps can be trained and validated.'])
H1('5. Conclusions')
BL(findings_list())
H1('6. Likely questions')
TAB('qa', [['Question', 'Answer'], ['Why are the maps plot-level?', 'Only plot mean spectra were uploaded; the plot is also the unit of the ground truth.'],
           ['Why show maps of models that do not work?', 'The user asked for maps of the best ASD models; showing their errors explains why UAV-trained models are needed.'],
           ['What does Moran\'s I add?', 'It tests whether errors cluster in space, which points to spatial causes such as illumination (Moran, 1950; Cliff and Ord, 1981).'],
           ['How will a pixel map be made?', 'Crop-masked pixels of the cube, same features, a UAV-trained model, then aggregation per plot (Zarco-Tejada et al., 2018).']],
    'Likely questions and short answers.', [3200, 6106])
H1('Appendix A. Plot table (truth, predictions and errors)')
cols = ['plot', 'block', 'status', 'score', 'grade', 'A_%s' % tg['A'], 'A_%s_cat' % tg['A'], 'B_%s' % tg['B'], 'C_%s' % tg['C'], 'C_%s_res' % tg['C'], 'A_uav', 'A_uav_cat', 'B_uav', 'C_uav', 'C_uav_res']
hdr = ['Plot', 'Block', 'Status', 'True score', 'True grade', 'ASD status', 'ASD outcome', 'ASD grade', 'ASD score', 'ASD error', 'UAV status', 'UAV outcome', 'UAV grade', 'UAV score', 'UAV error']
fmt = lambda v: ('%.2f' % v) if isinstance(v, float) else str(v)
TAB('ptab', [hdr] + [[fmt(r[c_]) for c_ in cols] for _, r in TB.iterrows()], 'Plot table: truth, predictions and errors of the best ASD maps (best input per task) and of the UAV-trained maps.', None, 12)
H1('Appendix B. Findings')
TAB('find', [['No.', 'Finding']] + [[i + 1, f] for i, f in enumerate(findings_list())], 'Key findings (the same list as in the Excel workbook and on the summary slide).', [700, 8606])
H1('References')

json.dump(findings_list(), open(O + 'findings.json', 'w'), indent=1)
json.dump(STEPS, open(O + 'methods.json', 'w'), indent=1, ensure_ascii=False)
json.dump(INTERP, open(O + 'interpretations.json', 'w'), indent=1, ensure_ascii=False)

# ================================================================== assemble
body = '\n'.join(K)
Tt = open(S + 'thesis/t_docx.js').read()
head = Tt[:Tt.index('// ======================= TITLE')]
head = re.sub(r"const B = '.*?';", "const B = '%s';" % HERE, head); head = re.sub(r"const OUT = '.*?';", "const OUT = '%s';" % OUTF, head)
head = re.sub(r"const FORDER = \[.*?\];", "const FORDER = __FORDER__;", head); head = re.sub(r"const TORDER = \[.*?\];", "const TORDER = __TORDER__;", head)
head = head.replace('children: [new Paragraph({ children: runs(String(c)', 'children: [new Paragraph({ keepNext: true, children: runs(String(c)')
plain = re.sub(r'\$\{[FT]\(\'\w+\'\)\}', '', body)
POOL = [l.strip() for l in open(HERE + 'm_extra_refs.txt').read().split('\n') if l.strip()] + [l.strip() for l in open(S + 'uavt/u_extra_refs.txt').read().split('\n') if l.strip()] + a_refs.pool()
c_ = a_refs.cites(plain); used, seen = [], set()
for r in POOL:
    k = a_refs.rk(r)
    if k in c_ and k not in seen: seen.add(k); used.append(r)
used.sort(key=lambda r: r.lower())
FP = {('Ord', '1981'), ('Brewer', '2003'), ('Yang', '2010')}
print('missing refs:', sorted(x for x in c_ if x not in seen and x[0] not in a_refs.SKIP and 1900 < int(x[1]) < 2028 and x not in FP))
q = lambda s: "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"
body += "\nconst refPara = r => new Paragraph({ spacing: { after: 70, line: 255 }, indent: { left: 400, hanging: 400 }, children: [new TextRun({ text: r, font: FONT, size: 19 })] });\n[" + ',\n'.join(q(r) for r in used) + "].forEach(r => K.push(refPara(r)));"
json.dump(used, open(O + 'refs_used.json', 'w'), indent=0, ensure_ascii=False)
FO = [mm.group(1) for mm in re.finditer(r"\bfig2\('([A-Za-z0-9]+)'", body)]; TO = [mm.group(1) for mm in re.finditer(r"\btab2\('([A-Za-z0-9]+)'", body)]
assert len(FO) == len(set(FO)) and len(TO) == len(set(TO))
mf = set(re.findall(r"\bF\('([A-Za-z0-9]+)'\)", body)) - set(FO); mt = set(re.findall(r"\bT\('([A-Za-z0-9]+)'\)", body)) - set(TO); assert not mf and not mt, (mf, mt)
head = head.replace('__FORDER__', repr(FO)).replace('__TORDER__', repr(TO))
tail = Tt[Tt.index('\nconst numcfg'):]
tail = tail.replace("title: 'AI-based multimodal UAV sensing of white rust in mustard: complete methodology'", "title: 'White rust disease maps, UAV hyperspectral image 24 Feb 2026'")
tail = re.sub(r"'eqs', \d+, 'refs', \d+", "'eqs', %d, 'refs', %d" % (len(re.findall(r'K.push\(EQ\(', body)), len(used)), tail)
open(HERE + 'm2_build.js', 'w').write(head + '\n' + body + '\n' + tail)
tn = {k: i + 1 for i, k in enumerate(TO)}; fn = {k: i + 1 for i, k in enumerate(FO)}
json.dump([dict(t, number=tn[t['key']]) for t in TABLES], open(O + 'tables.json', 'w'), indent=0, ensure_ascii=False)
json.dump([dict(f, number=fn[f['key']]) for f in FIGS], open(O + 'figures.json', 'w'), indent=0, ensure_ascii=False)
print('figs', len(FO), 'tabs', len(TO), 'refs', len(used))
