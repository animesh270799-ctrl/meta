"""Detailed Word report of the UAV transfer test (methodology step by step with references, detailed interpretation of every result).
python3 u4_word.py && NODE_PATH=/opt/node22/lib/node_modules node u4_build.js && python3 ../satmet/to_pdf.py <docx> <pdf>"""
import json, re, os, sys, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'; S = HERE + '../'; O = HERE + 'out/'
sys.path.insert(0, S + 'asd26'); sys.path.insert(0, HERE); import a_refs
from u_content import load, facts, steps, METRICS, GLOSSARY, APPLY, VAR, VSH, KEY, KL, TN, f2, f3, cis
OUTF = S + 'outputs/UAV_24Feb2026_ASD_model_transfer_report.docx'
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
def FIG(k, file, cap, w=600):
    FIGS.append(dict(key=k, file=file, caption=cap)); K.append("K.push(...fig2('%s', '%s', %s, %d));" % (k, file, js(cap), w))
def TAB(k, rows, cap, widths=None, size=17):
    if widths is None:
        L = [min(max(max(len(str(r[j])) for r in rows), 5), 46) for j in range(len(rows[0]))]; s = sum(L); widths = [int(9306 * x / s) for x in L]
    TABLES.append(dict(key=k, caption=cap, rows=[[str(c) for c in r] for r in rows]))
    R = '[' + ',\n'.join('[' + ', '.join(js(str(c)) for c in r) + ']' for r in rows) + ']'
    K.append("K.push(...tab2('%s', %s, %s, %s, %d));" % (k, R, json.dumps(widths), js(cap), size))
def PB(): K.append("K.push(new Paragraph({ children: [new PageBreak()] }));")
def INT(key, parts):
    """Interpretation block: list of (lead, text); stored for the Excel workbook and the slides."""
    INTERP[key] = parts
    for lead, txt in parts: P('**%s** %s' % (lead, txt))

D = load(); F = facts(D); GT, MF, PF, MU, DF, SC = D['GT'], D['MF'], D['PF'], D['MU'], D['DF'], D['SC']
best, mu, bv, bo, m, asd = F['best'], F['mu'], F['bv'], F['bo'], F['m'], F['asd']
dis = F['dis']; gapf = ', '.join(F['gapf']) if F['gapf'] else 'none'
MX = F['maxs']; mxA = MX.get('A')
mxs = lambda t: ('%s (%s input): %s %.3f, 95 %% CI %.2f to %.2f, maximum-statistic p = %.3f' % (MX[t].model, VSH[MX[t].variant], KL[t], MX[t].observed, MX[t].ci_lo, MX[t].ci_hi, MX[t].p_value)) if t in MX else ''
perm = F['perm']; pstr = lambda t: ('permutation p = %.3f' % perm[t].p_value) if t in perm else 'permutation test not run'
STEPS = steps(D, F)

def findings_list():
    a_, b2, c2 = bo['A'], bo['B'], bo['C']
    return ['Domain shift: canopy NIR reflectance %.2f vs leaf %.2f (healthy plots/leaves); %d of %d model inputs outside the leaf range for > 50 %% of plots (direct input)%s.' % (F['nir_uav'], F['nir_asd'], F['out50']['direct'], F['nfeat'], '; %s lies inside a UAV band gap' % gapf if F['gapf'] else ''),
            'Detection: best ASD model %s macro-F1 %.3f on the leaves vs %.3f on the UAV plots (%s input%s; AUC %s).' % (best['A']['overall'], asd('A', 'overall'), a_.macro_F1, VSH[bv['A']], cis(F, 'A', 'overall', bv['A'], 'macro_F1'), f3(a_.AUC)),
            ('Best of all 30 frozen model–input combinations for detection: %s (AUC %.2f); partial transfer, to be confirmed on another date.' % (mxs('A'), mxA.AUC) if mxA is not None else 'Best of all models: not computed.'),
            'Grades: %s macro-F1 %.3f on the leaves vs %.3f on the UAV plots; predictions concentrated in a few grades (best of all combinations: %s).' % (best['B']['overall'], asd('B', 'overall'), b2.macro_F1, mxs('B')),
            'Score: %s R² %.3f on the leaves vs %.3f on the UAV plots (r %.2f).' % (best['C']['overall'], asd('C', 'overall'), c2.R2, c2.r),
            'Corrections (healthy reference, brightness normalisation) moved some inputs into the leaf range but did not restore accuracy.',
            'In-domain check: %s refitted on the UAV plots reached detection macro-F1 %.3f (AUC %s, %s); grades macro-F1 %.3f (%s), score R² %.3f (%s).' % (mu['A'].model, mu['A'].macro_F1, f3(mu['A'].AUC), pstr('A'), mu['B'].macro_F1, pstr('B'), mu['C'].R2, pstr('C')),
            'Conclusion: leaf models cannot be applied to the canopy as they are; UAV models must be trained on UAV data, and the ASD results should guide feature choice and interpretation.']

# ================================================================== title and summary
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 900, after: 200 }, children: [new TextRun({ text: 'Do the ASD leaf models work on the UAV hyperspectral image?', font: FONT, size: 42, bold: true, color: '1E3A1F' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [new TextRun({ text: 'The best 2025-26 ASD white rust models applied to the UAV hyperspectral plot spectra of 24 February 2026: methodology, accuracy, domain shift, in-domain check and interpretation', font: FONT, size: 27, color: '2C5F2D' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 500 }, children: [new TextRun({ text: 'Animesh Panda | Ph.D. Agricultural Physics | ICAR-Indian Agricultural Research Institute, New Delhi', font: FONT, size: 22, bold: true })] }));")
a, b_, c = bo['A'], bo['B'], bo['C']
summ = ('**Question.** Can the best leaf-level models of the 2025-26 ASD analysis (trained on %d leaf spectra) be applied directly to the canopy-level UAV hyperspectral image of 24 February 2026? '
        '**Data.** %d plot mean spectra (%d healthy, %d diseased; %d bands, 399–2398 nm) and the ASD leaf scores of the same day (diseased plots: mean score %.1f–%.1f, PDI %.0f–%.0f %%). '
        '**Result.** On the leaves the best models reached macro-F1 %.3f (detection, %s), %.3f (six grades, %s) and R² %.3f (score, %s). On the UAV plots the same frozen models reached at best macro-F1 %.3f%s for detection, %.3f for grades and R² %.3f for the score: '
        'chance level for detection and no useful severity information. ' + (('Across all 30 frozen model–input combinations only one transferred partly for detection, %s; its AUC interval (%.2f to %.2f) reaches chance, so it needs confirmation on another date. ' % (mxs('A'), mxA.AUC_lo, mxA.AUC_hi)).replace('%', '%%') if mxA is not None and mxA.p_value < 0.05 else '') + 'Grades and score did not transfer with any model. '
        '**Why.** Canopy reflectance is far lower than leaf reflectance (NIR %.2f vs %.2f) and %d of the %d model inputs fall outside the leaf training range for more than half of the plots (%s inside a band removed from the UAV image). '
        '**In-domain check.** The same model type refitted on the UAV plots reached macro-F1 %.3f and AUC %s for detection (%s), so the canopy spectra do carry a disease signal. '
        '**Meaning.** Leaf models cannot be transferred to the canopy as they are; UAV models must be trained on UAV data, and the ASD analysis is best used to guide which wavelengths and indices to test.') % (
        F['asd_n'], len(GT), F['nH'], F['nD'], F['n_bands'], dis.score.min(), dis.score.max(), dis.PDI.min(), dis.PDI.max(),
        asd('A', 'overall'), best['A']['overall'], asd('B', 'overall'), best['B']['overall'], asd('C', 'overall'), best['C']['overall'],
        a.macro_F1, cis(F, 'A', 'overall', bv['A'], 'macro_F1'), b_.macro_F1, c.R2, F['nir_uav'], F['nir_asd'], F['out50']['direct'], F['nfeat'], gapf, mu['A'].macro_F1, f3(mu['A'].AUC), pstr('A'))
BOX('Summary of results.', summ, 'E8F5E9', '2E7D32')
BOX('How to read this report and the companion files.', 'Chapter 2 explains every step of the method in the same order: position in the workflow, concept, why it is needed, what published studies did, how it is done (with equations), how it was applied to these data, output, alternatives and a likely question. '
    'Chapter 3 gives each result with what is shown, how to read it, the result, its interpretation and its link to the literature. Every table and figure of this report is also in the Excel workbook (UAV_24Feb2026_ASD_model_transfer.xlsx: sheets R_Tables and R_Figures, plus live-formula sheets, a step-by-step guide and a metrics calculator) '
    'and in the slides (UAV_24Feb2026_ASD_model_transfer.pptx). Appendix G explains how to repeat the whole procedure on another data set.')
PB()
K.append("K.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: 'Contents', font: FONT, size: 32, bold: true, color: '1E3A1F' })] }));")
K.append("K.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-2' }));")
PB()

# ================================================================== 1 introduction
H1('1. Introduction')
H2('1.1 Background: leaf spectra and canopy spectra')
P('White rust (Albugo candida) causes white pustules, chlorosis and, in severe cases, distorted inflorescences (staghead) in Indian mustard; it changes leaf pigments, structure and water content and therefore leaf reflectance (Carter and Knapp, 2001; Mahlein et al., 2013). '
  'The 2025-26 ASD analysis measured these changes on single leaves with a contact probe: each spectrum comes from one leaf, lit by the probe lamp, with no soil, shadow or atmosphere. The models built on these spectra detected diseased leaves well (macro-F1 %.3f) but graded severity only moderately.' % asd('A', 'overall'))
P('The thesis aims at UAV-based detection. A UAV pixel is very different from a leaf clip: it mixes upper leaves, flowers, stems, soil and shadow; it is lit by the sun and the sky; and it is viewed from above through the canopy. '
  'Canopy reflectance therefore depends on leaf area, leaf angle, background and viewing geometry as much as on leaf optics (Asner, 1998; Jacquemoud et al., 2009). Reviews of disease sensing stress that models developed at one scale do not automatically hold at another (Mahlein, 2016; Thomas et al., 2018; Zhang et al., 2019), '
  'and field studies compare ground and UAV scales separately (Bohnenkamp et al., 2019).')
H2('1.2 Aim and questions')
P('The aim of this report is to test, with the only UAV image processed so far (24 February 2026), whether the best ASD leaf models can be used on the UAV data as they are, to explain the result, and to show what the UAV data themselves support.')
TAB('qs', [['Question', 'How it is answered', 'Where'],
           ['How accurate are the best ASD models on the UAV plots?', 'Frozen models applied to the 48 plot spectra; compared with the leaf scores of the same day', 'Steps M1–M4, M8; Sections 3.3–3.5'],
           ['Does a simple correction of the UAV spectra help?', 'Healthy-reference correction and brightness normalisation', 'Step M5; Sections 3.3–3.6'],
           ['Why does the transfer work or fail?', 'Spectra, feature ranges, PCA and Mahalanobis distance of leaves vs plots', 'Step M6; Sections 3.1–3.2'],
           ['Is there a disease signal in the UAV spectra at all?', 'Best ML model type refitted on the UAV plots, with a permutation test', 'Step M7; Section 3.7']],
    'Questions answered in this report.', [3100, 4300, 1906])
H2('1.3 Overview of the workflow')
FIG('wf', 'u01_workflow.png', 'Workflow of the transfer test: the frozen ASD leaf models are applied to the UAV plot spectra after the same pre-processing; an in-domain model checks the signal in the UAV data.', 620)
P('[[F:wf]] shows the eight steps of Chapter 2. The UAV plot spectra (M1) and the same-day ground truth (M2) are the inputs. The best ASD models (M3) are applied after exactly the same pre-processing (M4) to three versions of the UAV spectra (M5). '
  'Before judging accuracy, the domain check (M6) tests whether the UAV inputs lie inside the leaf training range. The in-domain check (M7) refits the best model type on the UAV plots. All predictions are evaluated with the same measures (M8).')

# ================================================================== 2 methodology
H1('2. Methodology (step by step)')
P('Each step is described in the same order: position in the workflow, concept, why it is needed here, what the reference papers did, how it is done, how it was applied to these data, output, notes and alternatives, and a likely question.')
for st in STEPS:
    H2('%s %s' % (st['no'], st['title']))
    P('**Position in the workflow.** ' + st['position']); P('**Concept.** ' + st['concept']); P('**Why it is needed here.** ' + st['why']); P('**What the reference papers did.** ' + st['papers'])
    P('**How it is done.**'); NL(st['how'])
    for e, lab in st['eqs']: EQ(e, lab)
    P('**How it was applied to these data.** ' + st['mine']); P('**Output.** ' + st['output']); P('**Notes and alternatives.** ' + st['notes']); P('**Likely question.** ' + st['question'])
    if st['no'] == 'M2':
        TAB('gts', [['Item', 'Value']] + [['Leaves scored on 24 Feb', int(GT.n_leaves.sum())], ['Healthy plots (task A = 0)', F['nH']], ['Diseased plots (task A = 1)', F['nD']],
                    ['Mean score of diseased plots', '%.2f (range %.2f–%.2f)' % (dis.score.mean(), dis.score.min(), dis.score.max())], ['PDI of diseased plots', '%.1f %% (range %.1f–%.1f %%)' % (dis.PDI.mean(), dis.PDI.min(), dis.PDI.max())]] +
            [['Plots in grade %d (task B)' % g, n] for g, n in F['grades'].items()],
            'Summary of the ground truth of 24 Feb 2026 (full table per plot: Appendix A).', [5000, 4306])
    if st['no'] == 'M3':
        idx = pd.concat([pd.read_csv(S + 'outputs/ASD_2025-26_models/ml_models_index.csv'), pd.read_csv(S + 'outputs/ASD_2025-26_models/dl_models_index.csv')], ignore_index=True)
        rows = [['Task', 'Role', 'Model', 'Leaf score (LORO)', 'Input features']]
        for t in 'ABC':
            for role in ('overall', 'ML', 'DL'):
                mod = best[t][role]; fr = idx[(idx.task == t) & (idx.model == mod)]
                rows.append([TN[t] if role == 'overall' else '', role, mod, '%s %s' % (KL[t], f3(asd(t, role))), fr.features.iloc[0] if len(fr) else '–'])
        TAB('best', rows, 'Best ASD models used in the test (trained on all leaves) and their leave-one-replication-out score on the leaves.', [1700, 800, 1500, 1400, 3906], 15)
    if st['no'] == 'M8':
        TAB('acc', [['Measure', 'Task', 'Formula', 'Excel formula', 'How to read it', 'Reference']] + [list(x) for x in METRICS],
            'Accuracy measures: formula, Excel formula used in the workbook, interpretation and reference.', [1500, 600, 1900, 1900, 2206, 1200], 14)

# ================================================================== 3 results
H1('3. Results and interpretation')
P('Every result below is given as: what is shown, how to read it, the result, its interpretation and its link to the literature.')
H2('3.1 Leaf and canopy spectra')
FIG('spec', 'u02_spectra.png', 'Mean spectra of ASD leaves (dashed) and UAV plots (solid) on 24 Feb 2026, healthy (green) and diseased (red), for the three input variants. Grey bands = bands removed from the UAV image.', 640)
REG = [('Blue', 450, 510), ('Green peak', 530, 570), ('Red', 650, 690), ('Red edge', 700, 740), ('NIR plateau', 780, 880), ('SWIR-1', 1550, 1750), ('SWIR-2', 2050, 2300)]
SCOL = ['ASD healthy (24 Feb)', 'ASD diseased (24 Feb)', 'UAV healthy', 'UAV diseased', 'UAV healthy corrected', 'UAV diseased corrected', 'UAV healthy normalised', 'UAV diseased normalised']
rm = F['rm']
TAB('bands', [['Region (nm)'] + ['ASD H', 'ASD D', 'UAV H', 'UAV D', 'UAV H corr.', 'UAV D corr.', 'UAV H norm.', 'UAV D norm.']] +
    [['%s %d–%d' % (n_, lo, hi)] + ['%.3f' % rm(c_, lo, hi) for c_ in SCOL] for n_, lo, hi in REG],
    'Mean reflectance per band region: ASD leaves and UAV plots of 24 Feb 2026 (H = healthy, D = diseased; corr. = healthy-reference corrected; norm. = corrected + brightness-normalised).', [1700] + [950] * 8, 15)
lc = lambda col: (rm(col.replace('healthy', 'diseased'), 780, 880) / rm(col, 780, 880) - 1) * 100
INT('spectra', [('What is shown.', '[[F:spec]] compares the mean spectra of the healthy and diseased ASD leaves of 24 Feb with the mean spectra of the healthy and diseased UAV plots, for the direct, corrected and normalised inputs; [[T:bands]] gives the mean values per band region.'),
    ('How to read it.', 'Dashed lines are leaves, solid lines are plots; the gap between a green and a red line of the same kind is the disease effect, the gap between dashed and solid lines is the leaf–canopy difference. Grey bands are wavelengths missing from the UAV image.'),
    ('Result.', 'The healthy UAV plots reflected %.2f in the NIR plateau against %.2f for the healthy leaves (%.0f %% of the leaf value), and %.3f vs %.3f in the red. Diseased leaves reflected %.1f %% less than healthy leaves in the NIR, diseased plots %.1f %% less than healthy plots. '
     'After correction the healthy plots match the healthy leaves by construction; after normalisation the diseased plots also come close to the leaf curves.' % (F['nir_uav'], F['nir_asd'], 100 * F['nir_uav'] / F['nir_asd'], F['red_uav'], F['red_asd'], -lc('ASD healthy (24 Feb)'), -lc('UAV healthy'))),
    ('Interpretation.', 'The leaf–canopy difference is much larger than the disease difference. A canopy contains shadow and soil and its leaves are inclined, so its NIR reflectance is far below that of a single leaf held flat against a probe (Asner, 1998). '
     'The disease effect at the canopy is diluted by healthy upper leaves, flowers and background, and partly confounded with brightness differences between plots (UAV spectra workbook).'),
    ('Link to the literature.', 'Radiative-transfer models such as PROSPECT + SAIL show that canopy reflectance depends on leaf area, leaf angle and soil as well as on leaf optics (Jacquemoud et al., 2009); this is why leaf-scale relations need re-calibration at the canopy (Thomas et al., 2018).')])
H2('3.2 Domain check: are the UAV inputs inside the leaf training range?')
FIG('feat', 'u04_features.png', 'Share of UAV plots whose feature value is outside the ASD training range (1st–99th percentile of the leaves), for the three input variants; (gap) = feature inside a UAV band gap.', 520)
TAB('dom', [['Feature', 'In UAV gap', 'ASD mean', 'UAV direct mean', 'Shift direct (SD)', '% out direct', '% out corrected', '% out normalised']] +
    [[r.feature, 'yes' if r.in_uav_gap else 'no', '%.4g' % r.asd_mean, '%.4g' % r.uav_direct_mean, '%.2f' % r.uav_direct_z, '%.0f' % r.uav_direct_out_pct, '%.0f' % r.uav_corrected_out_pct, '%.0f' % r.uav_normalised_out_pct] for r in DF.itertuples()],
    'Input features of the best models: ASD leaves vs UAV plots (range check, Sahigara et al., 2012).', None, 15)
FIG('pca', 'u03_pca.png', 'PCA of the standardised model features fitted on the ASD leaves; UAV plots projected (squares = direct, triangles = normalised).', 470)
po = F['pca_out']
INT('domain', [('What is shown.', '[[F:feat]] and [[T:dom]] show, for every input of the best models, how many UAV plots fall outside the range of the 2330 leaves; [[F:pca]] places leaves and plots in the same principal-component space.'),
    ('How to read it.', 'A long bar means the model sees values it never met in training (extrapolation). In the PCA, points far from the cloud of leaves are outside the applicability domain.'),
    ('Result.', '%d of %d features were outside the leaf range for more than half of the plots with the direct input, %d with the corrected and %d with the normalised input. The largest shifts (in leaf SD units) were %s. '
     'PC1 and PC2 explained %.0f %% and %.0f %% of the leaf variance; %.0f %% of the plots (direct) and %.0f %% (normalised) lay beyond the 99th-percentile Mahalanobis distance of the leaves. %s' % (
         F['out50']['direct'], F['nfeat'], F['out50']['corrected'], F['out50']['normalised'], ', '.join('%s %+.1f' % (f_, z_) for f_, z_ in F['zmax']), 100 * F['pca_var'][0], 100 * F['pca_var'][1],
         po.get('UAV plot (direct)', np.nan), po.get('UAV plot (corrected + brightness-normalised)', np.nan), ('%s lies inside a UAV band gap, so its UAV value is an interpolation.' % gapf) if F['gapf'] else '')),
    ('Interpretation.', 'The selected inputs are mostly first derivatives, whose size scales with reflectance; canopy derivatives are smaller than leaf derivatives, and the red-edge parameters shift because the canopy red-edge shape differs. '
     'The correction and normalisation bring several features back into range, but others move further out because the gain also amplifies the plot-to-plot brightness spread. Predictions on such inputs are extrapolations and cannot be trusted.'),
    ('Link to the literature.', 'Checking the applicability domain before using a model on new data is standard practice in chemometrics and QSAR (Sahigara et al., 2012); PCA projection is the simplest distance check (Jolliffe and Cadima, 2016). Calibration-transfer studies report that models fail when the instrument or sample domain changes (Feudale et al., 2002).')])

def tvals(t, x):
    if t == 'A': return [f3(x.macro_F1), f3(x.balanced_acc), f3(x.sensitivity), f3(x.specificity), f3(x.AUC), '%d of 48' % x.pred_diseased]
    if t == 'B': return [f3(x.OA), f3(x.macro_F1), f3(x.QWK), f3(x.within1), x.pred_grades]
    return [f3(x.R2), f2(x.RMSE), f2(x.bias), f3(x.r), f3(x.r_diseased)]
HDR = {'A': ['Macro-F1', 'Bal. acc.', 'Sensitivity', 'Specificity', 'AUC', 'Pred. diseased'], 'B': ['OA', 'Macro-F1', 'QWK', 'Within 1', 'Predicted grades'], 'C': ['R²', 'RMSE', 'Bias', 'r', 'r diseased']}
def rtab(t, cap):
    rows = [['Model (role)', 'Input'] + HDR[t]]
    for role in ('overall', 'ML', 'DL'):
        for v in VAR: rows.append(['%s (%s)' % (best[t][role], role), VSH[v]] + tvals(t, m(t, best[t][role], v)))
    rows.append(['%s refitted on UAV (LORO)' % mu[t].model, 'UAV-trained'] + tvals(t, mu[t]))
    TAB('t' + t, rows, cap, None, 15)

H2('3.3 Detection (healthy vs diseased plots)')
rtab('A', 'Detection on the 48 UAV plots (12 healthy, 36 diseased): best ASD models with three inputs and the UAV-trained model.')
FIG('cmA', 'u06_confusion_A.png', 'Detection confusion matrices of the best overall ASD model (three inputs) and of the UAV-trained model.', 640)
tA = F['top']['A']; vv = {v: m('A', best['A']['overall'], v) for v in VAR}
INT('detection', [('What is shown.', '[[T:tA]] gives the detection measures of the best overall, best ML and best DL ASD models for the three inputs and of the UAV-trained model; [[F:cmA]] shows the confusion matrices of the best overall model and of the UAV-trained model.'),
    ('How to read it.', 'Balanced accuracy and macro-F1 of 0.5 or lower mean chance; sensitivity is the share of the 36 diseased plots found, specificity the share of the 12 healthy plots recognised. In a confusion matrix, correct predictions lie on the diagonal.'),
    ('Result.', 'On the leaves %s reached macro-F1 %.3f. On the UAV plots it reached macro-F1 %s (direct), %s (corrected) and %s (normalised); its best input (%s) gave sensitivity %.3f, specificity %.3f and AUC %s%s. '
     'It predicted %d, %d and %d of the 48 plots as diseased for the three inputs. The best macro-F1 of any of the 30 models and three inputs was %.3f (%s, %s input).' % (
         best['A']['overall'], asd('A', 'overall'), f3(vv['Direct'].macro_F1), f3(vv['Healthy-reference corrected'].macro_F1), f3(vv['Corrected + brightness-normalised'].macro_F1), VSH[bv['A']], a.sensitivity, a.specificity, f3(a.AUC), cis(F, 'A', 'overall', bv['A'], 'AUC'),
         int(vv['Direct'].pred_diseased), int(vv['Healthy-reference corrected'].pred_diseased), int(vv['Corrected + brightness-normalised'].pred_diseased), tA.macro_F1, tA.model, VSH[tA.variant])),
    ('Interpretation.', 'The frozen leaf model selected as best on the leaves does not separate healthy and diseased plots: depending on the input, its errors are spread over both classes or it labels almost every plot the same way. '
     'This follows from the domain check: the inputs lie outside the leaf range, so the decision boundary learned on leaves does not cut the canopy data in the right place. ' + (('One exception: %s. A maximum-statistic test over all 30 combinations (Westfall and Young, 1993) shows that this best result is unlikely to be chance, but its AUC interval (%.2f to %.2f) reaches 0.5 and it was found after testing many combinations, so it is a lead to confirm on the next flight, not a validated model.' % (mxs('A'), mxA.AUC_lo, mxA.AUC_hi)) if mxA is not None and mxA.p_value < 0.05 else '')),
    ('Link to the literature.', 'Detection models need same-scale training data; studies that detect disease from UAV hyperspectral images train on UAV features with field labels (Zarco-Tejada et al., 2018; Bohnenkamp et al., 2019), and reviews warn against transferring leaf-scale results without validation (Thomas et al., 2018).')])
H2('3.4 Six-grade severity')
rtab('B', 'Six-grade severity on the UAV plots (true grade = nearest grade of the plot mean leaf score).')
FIG('cmB', 'u07_confusion_B.png', 'Grade confusion matrices of the best overall ASD model (three inputs) and of the UAV-trained model.', 640)
tB_ = F['top']['B']
INT('grades', [('What is shown.', '[[T:tB]] and [[F:cmB]] compare the predicted grade of each plot with the nearest grade of its mean leaf score.'),
    ('How to read it.', 'QWK near 0 means agreement no better than chance; "within one grade" credits predictions one grade away; the predicted-grades column shows how often each grade was predicted.'),
    ('Result.', 'True grades on 24 Feb: %s. The best overall model reached overall accuracy %.3f, macro-F1 %.3f, QWK %s and %.0f %% within one grade with the %s input; its predictions were %s. The best macro-F1 of any model and input was %.3f (%s, %s input).' % (
        ', '.join('%d (%d plots)' % (g, n) for g, n in F['grades'].items()), b_.OA, b_.macro_F1, f3(b_.QWK), 100 * b_.within1, VSH[bv['B']], b_.pred_grades, tB_.macro_F1, tB_.model, VSH[tB_.variant])),
    ('Interpretation.', 'The leaf grading model collapses onto a few grades on the canopy data, so it cannot rank plots by severity. Grading was already the weakest leaf task (macro-F1 %.3f on the leaves) because neighbouring grades overlap spectrally; at the canopy this overlap is compounded by the domain shift and by the narrow range of plot severities on one date.' % asd('B', 'overall')),
    ('Link to the literature.', 'Weighted kappa is the appropriate agreement measure for ordered classes (Cohen, 1968); low agreement for fine severity classes is common even within one scale (Mahlein, 2016).')])
H2('3.5 Severity score')
rtab('C', 'Severity score on the UAV plots (true = plot mean leaf score, 0–9).')
FIG('scat', 'u08_score.png', 'Predicted vs true plot mean leaf score: best overall ASD model (three inputs) and UAV-trained model; dashed line = 1:1.', 640)
tC_ = F['top']['C']
INT('score', [('What is shown.', '[[T:tC]] gives R², RMSE, bias and correlation between the predicted and the true plot mean leaf score; [[F:scat]] plots them against each other.'),
    ('How to read it.', 'Points on the 1:1 line are perfect; R² ≤ 0 means the predictions are no better than predicting the mean score for every plot; r measures whether the plots are at least ranked correctly even if biased.'),
    ('Result.', 'The best overall model (%s) gave R² %.3f%s, RMSE %.2f, bias %+.2f and r %.3f with the %s input; within the diseased plots r = %s. The predictions ranged from %.2f to %.2f. The best R² of any model and input was %.3f (%s, %s input). '
     'Using the upper-leaf (L3) score as the target gave r = %s.' % (best['C']['overall'], c.R2, cis(F, 'C', 'overall', bv['C'], 'R2'), c.RMSE, c.bias, c.r, VSH[bv['C']], f3(c.r_diseased), c.pred_min, c.pred_max, tC_.R2, tC_.model, VSH[tC_.variant], f3(F['rL3']))),
    ('Interpretation.', 'The predicted scores do not follow the plot severity: the model compresses its output into a narrow band and does not rank the diseased plots. The choice of leaf level for the ground truth does not change this, so the failure lies in the spectra, not in the target.'),
    ('Link to the literature.', 'An RPD below 1.4 indicates an unusable calibration (Williams, 2001); canopy-scale severity models in the literature are calibrated with canopy spectra and canopy-scale scores (Zhang et al., 2019).')])
H2('3.6 All 30 models')
FIG('heat', 'u09_heatmap.png', 'All ASD models on the UAV plots: macro-F1 (A, B) and R² (C) for the three inputs, and the UAV-trained model.', 640)
MLD = F['MLD']
INT('allmodels', [('What is shown.', '[[F:heat]] shows the main measure of every one of the 30 ASD models with every input (full tables in Appendix E).'),
    ('Result.', 'Best macro-F1 per input for detection: %s; for grades: %s; best R² per input for the score: %s.' % (', '.join('%.2f (%s)' % (MLD.loc[('A', v), 'macro_F1'], VSH[v]) for v in VAR), ', '.join('%.2f (%s)' % (MLD.loc[('B', v), 'macro_F1'], VSH[v]) for v in VAR), ', '.join('%.2f (%s)' % (MLD.loc[('C', v), 'R2'], VSH[v]) for v in VAR))),
    ('Interpretation.', 'The ranking on the leaves did not predict the ranking on the canopy. For grades (%s) and score (%s) even the best of the 30 combinations was not better than chance. For detection the best combination (%s) passed the maximum-statistic test (Westfall and Young, 1993), so one network transferred partly once brightness was normalised; with an AUC interval reaching 0.5 this needs confirmation (Efron and Tibshirani, 1993).' % (mxs('B'), mxs('C'), mxs('A')))])
if MX:
    TAB('maxs', [['Task', 'Best model', 'Input', 'Measure', 'Value', '95 % CI', 'Combinations', 'Best under chance (mean / 95th pct)', 'p (max-statistic)']] +
        [[TN[t], r.model, VSH[r.variant], KL[t], f3(r.observed), '%.2f to %.2f' % (r.ci_lo, r.ci_hi), r.n_combinations, '%.3f / %.3f' % (r.null_mean_of_max, r.null_p95_of_max), '%.3f' % r.p_value] for t, r in MX.items()],
        'Best of all 30 frozen model–input combinations per task, tested against chance with a maximum-statistic permutation test (2000 label permutations; Westfall and Young, 1993) and a bootstrap 95 % CI.', [1500, 1300, 900, 800, 700, 1100, 900, 1300, 806], 14)
H2('3.7 In-domain check (UAV-trained models)')
TAB('uavt', [['Task', 'Model', 'Features used (gap features removed)', 'Macro-F1', 'Bal. acc.', 'AUC', 'OA', 'QWK', 'Within 1', 'R²', 'RMSE', 'r']] +
    [[TN[t], mu[t].model, '%s%s' % (mu[t].features, ' (removed: %s)' % mu[t].dropped_gap_features if isinstance(mu[t].dropped_gap_features, str) and mu[t].dropped_gap_features else ''), f3(mu[t].macro_F1), f3(mu[t].balanced_acc), f3(mu[t].AUC), f3(mu[t].OA), f3(mu[t].QWK), f3(mu[t].within1), f3(mu[t].R2), f2(mu[t].RMSE), f3(mu[t].r)] for t in 'ABC'],
    'Best ML model type refitted on the UAV plots (leave-one-replication-out, same folds and hyper-parameters as the ASD analysis).', [1300, 800, 2706, 600, 600, 600, 500, 500, 600, 500, 500, 500], 14)
if perm:
    TAB('perm', [['Task', 'Model', 'Measure', 'Observed', 'Mean under chance', '95th percentile under chance', 'Permutations', 'p-value']] +
        [[TN[t], r.model, r.metric, f3(r.observed), f3(r.null_mean), f3(r.null_p95), r.n_perm, '%.3f' % r.p_value] for t, r in perm.items()],
        'Permutation test of the UAV-trained models (labels shuffled within folds; Ojala and Garriga, 2010).', [1800, 900, 900, 1000, 1300, 1500, 1000, 906], 15)
INT('indomain', [('What is shown.', '[[T:uavt]] gives the scores of the best ML model types refitted on the UAV plots%s.' % (' and [[T:perm]] tests them against chance' if perm else '')),
    ('How to read it.', 'These models learn from canopy spectra, so they show what the UAV data can support. A permutation p-value below 0.05 means the score is unlikely to arise by chance.'),
    ('Result.', '%s reached detection macro-F1 %.3f, balanced accuracy %.3f and AUC %s (%s), against macro-F1 %.3f for the best frozen leaf model. For grades %s reached macro-F1 %.3f and %.0f %% within one grade (%s); for the score %s reached R² %.3f and r %.3f (%s).' % (
        mu['A'].model, mu['A'].macro_F1, mu['A'].balanced_acc, f3(mu['A'].AUC), pstr('A'), a.macro_F1, mu['B'].model, mu['B'].macro_F1, 100 * mu['B'].within1, pstr('B'), mu['C'].model, mu['C'].R2, mu['C'].r, pstr('C'))),
    ('Interpretation.', 'The UAV spectra carry a detection signal once a model is trained on them: the failure of the frozen models is a leaf–canopy mismatch, not an absence of information. Severity grading and score estimation remain weak with 48 plots of one date and a narrow severity range; '
     'they need the larger 2026-27 data set (1536 post-symptomatic subplot samples per camera) and several dates.'),
    ('Link to the literature.', 'UAV hyperspectral disease studies that reach good accuracy train on UAV features with field labels at the same scale (Zarco-Tejada et al., 2018; Bohnenkamp et al., 2019); significance by permutation guards against chance results with small samples (Ojala and Garriga, 2010).')])
H2('3.8 Summary: leaves vs UAV')
FIG('summ', 'u05_summary.png', 'Best ASD models (overall, best ML, best DL): score on the leaves (LORO) and on the UAV plots for the three inputs, and the UAV-trained ML model.', 640)
INT('summary', [('What is shown.', '[[F:summ]] puts the leaf score of each best model next to its UAV scores and the UAV-trained score.'),
    ('Interpretation.', 'For every task the drop from leaves to UAV is large; the corrections recover little; the UAV-trained model recovers detection but not severity. The leaf models are therefore not a substitute for UAV models, but the features they rely on (red edge, green peak, NIR plateau, water-band edges) remain physically meaningful candidates for UAV models (Mahlein et al., 2013).')])

# ================================================================== 4 discussion
H1('4. Discussion')
H2('4.1 Why the leaf models do not transfer')
BL(['**Different measurement.** The contact probe measures one leaf with its own lamp; the UAV pixel mixes leaves, flowers, stems, soil and shadow in sunlight. Canopy structure and background change reflectance as much as leaf chemistry (Asner, 1998; Jacquemoud et al., 2009).',
    '**Out-of-range inputs.** Most selected features are first derivatives whose size scales with reflectance; canopy derivatives are smaller than leaf derivatives, so the models see values never met in training ([[T:dom]]; Sahigara et al., 2012).',
    ('**Missing bands.** %s lies inside a water-vapour band removed from the UAV image, so its value is an interpolation, not a measurement.' % gapf) if F['gapf'] else '**Missing bands.** None of the inputs of the new best models lies inside a removed UAV band, so the band gaps do not explain the failure; the earlier model set used FD1805, which did.',
    '**Brightness and illumination.** Plot brightness varied strongly even between replications of one treatment (UAV spectra workbook); this is radiometric rather than disease-related (Aasen et al., 2018).',
    '**Different target.** A leaf model predicts the score of one leaf; a plot spectrum averages the visible canopy (upper leaves and flowers), while the plot score averages three tagged leaf positions.'])
H2('4.2 What the corrections can and cannot do')
P('The healthy-reference correction is an empirical-line calibration that uses the healthy plots as reference targets (Smith and Milton, 1999); brightness normalisation removes multiplicative effects as in standard spectral pre-processing (Barnes et al., 1989; Rinnan et al., 2009). '
  'Both align the mean level of the spectra, the first step of calibration transfer (Feudale et al., 2002), but they cannot recreate the leaf-level contrast between healthy and diseased tissue in a canopy where diseased leaves are mixed with healthy ones, flowers and background. '
  'Proper transfer methods (direct or piecewise direct standardisation, domain-adaptation networks) need paired spectra of the same plants in both domains (Feudale et al., 2002; Pan and Yang, 2010), which this season did not provide.')
H2('4.3 What the in-domain check shows')
P('Trained on the UAV plots themselves, the detection model reached macro-F1 %.3f and AUC %s (%s), against %.3f for the best frozen leaf model. The disease signal is therefore present at the canopy, but it must be learned from canopy data. '
  'Grade and score models trained on 48 plots were weak (macro-F1 %.3f, R² %.3f), as expected with one date, 36 diseased plots and a narrow severity range (mean score %.1f–%.1f).' % (mu['A'].macro_F1, f3(mu['A'].AUC), pstr('A'), a.macro_F1, mu['B'].macro_F1, mu['C'].R2, dis.score.min(), dis.score.max()))
H2('4.4 Limitations')
BL(['One UAV date and 48 plots: confidence intervals are wide and only large effects can be detected (Efron and Tibshirani, 1993).',
    'Ground truth from three tagged leaf positions, not from the whole visible canopy.',
    'No paired leaf–canopy spectra, so only simple corrections could be tested (Feudale et al., 2002).',
    'Radiometric quality of the image (illumination differences between plots) is not yet verified (Aasen et al., 2018).'])
H2('4.5 Use for the 2026-27 season')
BL(['Train the UAV models on UAV features with subplot-level scores (1536 post-symptomatic samples per camera), not on leaf spectra.',
    'Use the ASD results to guide feature choice (red edge, green peak, NIR plateau, water-band edges) and to interpret the UAV features physically (Mahlein et al., 2013).',
    'Measure leaf and canopy spectra of the same tagged plants on the same day; these pairs allow a real calibration transfer and a leaf-to-canopy model check (Jacquemoud et al., 2009).',
    'Check the radiometric calibration (reflectance panels, illumination, flight lines) before modelling (Aasen et al., 2018).'])

# ================================================================== 5, 6
H1('5. Conclusions')
BL(['The best ASD leaf models, applied unchanged to the UAV plot spectra of 24 Feb 2026, gave chance-level detection (best macro-F1 %.3f) and no useful grade or score information (best R² %.3f).' % (a.macro_F1, c.R2),
    ('One frozen network transferred partly for detection after brightness normalisation (%s); it is a lead to confirm on the next flight.' % mxs('A')) if mxA is not None and mxA.p_value < 0.05 else 'No frozen model transferred beyond chance.',
    'Healthy-reference correction and brightness normalisation did not fix the leaf–canopy mismatch.',
    'The canopy spectra carry a detection signal: the same model type trained on the UAV plots reached macro-F1 %.3f (AUC %s; %s).' % (mu['A'].macro_F1, f3(mu['A'].AUC), pstr('A')),
    'Leaf models should guide, not replace, UAV models: UAV models must be trained and validated on UAV data with same-scale ground truth.'])
H1('6. Likely questions')
TAB('qa', [['Question', 'Answer'],
           ['Why not fine-tune the leaf models on the UAV data?', 'With 48 plots there are too few canopy samples to retrain a network; fine-tuning becomes possible with the 1536 subplot samples per camera of 2026-27 (Pan and Yang, 2010).'],
           ['Is the healthy-reference correction fair for detection?', 'Yes: a healthy plot is never used to correct itself (leave-one-out), and the diseased plots are not used at all.'],
           ['Why is UAV-trained detection good but grading poor?', 'Healthy vs diseased is a large contrast; grades on one date span a narrow range (mean score %.1f–%.1f) with only 36 diseased plots.' % (dis.score.min(), dis.score.max())],
           ['Could the band gaps alone explain the failure?', 'No: the features outside the gaps are also outside the leaf range, and the gap-free UAV-trained model still works for detection.'],
           ['How do you know the UAV-trained result is not chance?', 'A permutation test with labels shuffled within folds gave %s (Ojala and Garriga, 2010).' % pstr('A')],
           ['What would make leaf models transferable?', 'Paired leaf and canopy spectra (calibration transfer), radiative-transfer upscaling (PROSAIL) or training with simulated canopy spectra (Jacquemoud et al., 2009; Feudale et al., 2002).']],
    'Likely questions and short answers.', [3200, 6106])

# ================================================================== appendices
H1('Appendix A. Ground truth of the 48 plots (24 Feb 2026)')
TAB('gtab', [['Plot', 'Block', 'Status', 'Variety', 'Sowing', 'Crop stage', 'Leaves', 'Mean score', 'Score L3', 'PDI (%)', 'Grade', 'DI class']] +
    [[int(r['plot']), r.block, r.status, r.variety, r.sowing, r.stage, int(r.n_leaves), '%.2f' % r.score, '–' if pd.isna(r.score_L3) else '%.2f' % r.score_L3, '%.1f' % r.PDI, int(r.grade), int(r.DI_class)] for _, r in GT.iterrows()],
    'Ground truth per plot from the ASD leaf scores of 24 Feb 2026 (mean score 0–9; grade = nearest grade; DI class from PDI).', [550, 650, 900, 750, 750, 1150, 700, 950, 850, 800, 650, 800], 14)
PU2 = D['PU']
for t, ttl in (('A', 'Appendix B. Detection predictions per plot'), ('B', 'Appendix C. Grade predictions per plot'), ('C', 'Appendix D. Score predictions per plot')):
    H1(ttl)
    cols_ = [(r_, v) for r_ in ('overall', 'ML', 'DL') for v in VAR]
    hdr = ['Plot', 'Status', 'True'] + ['%s %s' % ({'overall': 'Best', 'ML': 'ML', 'DL': 'DL'}[r_], {'Direct': 'D', 'Healthy-reference corrected': 'C', 'Corrected + brightness-normalised': 'N'}[v]) for r_, v in cols_] + ['UAV-trained']
    rows_ = [hdr]
    for p_ in range(1, len(GT) + 1):
        tr_ = PF[(PF.task == t) & (PF['plot'] == p_)]
        row_ = [p_, GT.status[p_ - 1], ('%.2f' % GT.score[p_ - 1]) if t == 'C' else int({'A': GT.A, 'B': GT.grade}[t][p_ - 1])]
        for r_, v in cols_:
            x_ = tr_[(tr_.model == best[t][r_]) & (tr_.variant == v)].pred.iloc[0]; row_.append('%.2f' % x_ if t == 'C' else int(x_))
        x_ = PU2[(PU2.task == t) & (PU2['plot'] == p_)].pred.iloc[0]; row_.append('%.2f' % x_ if t == 'C' else int(x_)); rows_.append(row_)
    TAB('pp' + t, rows_, '%s: true value and predictions of the best overall (%s), best ML (%s) and best DL (%s) ASD models with the direct (D), corrected (C) and normalised (N) inputs, and of the UAV-trained %s.' % (
        TN[t].capitalize(), best[t]['overall'], best[t]['ML'], best[t]['DL'], mu[t].model), [550, 900, 650] + [700] * 9 + [906], 13)
H1('Appendix E. All ASD models on the UAV plots')
LB = {'macro_F1': 'macro-F1', 'AUC': 'AUC', 'QWK': 'QWK', 'R2': 'R²', 'RMSE': 'RMSE'}
for t in 'ABC':
    k1, k2 = (('macro_F1', 'AUC') if t == 'A' else ('macro_F1', 'QWK') if t == 'B' else ('R2', 'RMSE'))
    rows_ = [['Model', 'Source'] + ['%s %s' % (LB[k_], {'Direct': 'D', 'Healthy-reference corrected': 'C', 'Corrected + brightness-normalised': 'N'}[v]) for k_ in (k1, k2) for v in VAR]]
    for (mod, src), g_ in MF[MF.task == t].groupby(['model', 'source']):
        rows_.append([mod, src] + [f3(g_[g_.variant == v][k_].iloc[0]) for k_ in (k1, k2) for v in VAR])
    TAB('all' + t, rows_, '%s: every ASD model on the UAV plots with the direct (D), corrected (C) and normalised (N) inputs.' % TN[t].capitalize(), [1900, 900] + [1084] * 6, 15)
if D['CI'] is not None:
    H1('Appendix F. Confidence intervals of the main measures')
    CI = D['CI']; rows_ = [['Task', 'Model (role)', 'Input', 'Measure 1 [95 % CI]', 'Measure 2 [95 % CI]']]
    KM = {'A': ('macro_F1', 'AUC'), 'B': ('macro_F1', 'QWK'), 'C': ('R2', 'RMSE')}
    for r_ in CI.itertuples():
        k1, k2 = KM[r_.task]
        rows_.append([r_.task, '%s (%s)' % (r_.model, r_.role), VSH.get(r_.variant, r_.variant), '%s %s [%s, %s]' % (LB[k1], f3(getattr(r_, k1)), f3(getattr(r_, k1 + '_lo')), f3(getattr(r_, k1 + '_hi'))),
                      '%s %s [%s, %s]' % (LB[k2], f3(getattr(r_, k2)), f3(getattr(r_, k2 + '_lo')), f3(getattr(r_, k2 + '_hi')))])
    TAB('ci', rows_, 'Main measures with 95 % bootstrap confidence intervals (2000 resamples of plots, stratified by status; Efron and Tibshirani, 1993).', [600, 2600, 1400, 2353, 2353], 14)
H1('Appendix G. How to apply the procedure to another data set')
TAB('apply', [['Step', 'What to do', 'Details', 'Tool / template', 'Method step']] + [list(x) for x in APPLY], 'Procedure to repeat the transfer test (or to evaluate any model) on a new data set.', [600, 1800, 3706, 1900, 1300], 15)
H1('Appendix H. Key findings and glossary')
TAB('find', [['No.', 'Finding']] + [[i + 1, f_] for i, f_ in enumerate(findings_list())], 'Key findings (the same list as on the first Excel sheet and the summary slide).', [700, 8606], 16)
TAB('gloss', [['Term', 'Meaning']] + [list(x) for x in GLOSSARY], 'Glossary of the terms used.', [2400, 6906], 16)
H1('References')

# ================================================================== save shared content
json.dump(findings_list(), open(O + 'findings.json', 'w'), indent=1)
json.dump(dict(best_variant=bv, out50=F['out50'], gapf=F['gapf'], rL3=None if not np.isfinite(F['rL3']) else float(F['rL3']), nir_uav=F['nir_uav'], nir_asd=F['nir_asd'], pca_out=F['pca_out']), open(O + 'report_numbers.json', 'w'), indent=1)
json.dump(STEPS, open(O + 'methods.json', 'w'), indent=1, ensure_ascii=False)
json.dump(INTERP, open(O + 'interpretations.json', 'w'), indent=1, ensure_ascii=False)

# ================================================================== assemble (template of the thesis documents)
body = '\n'.join(K)
T = open(S + 'thesis/t_docx.js').read()
head = T[:T.index('// ======================= TITLE')]
head = re.sub(r"const B = '.*?';", "const B = '%s';" % HERE, head); head = re.sub(r"const OUT = '.*?';", "const OUT = '%s';" % OUTF, head)
head = re.sub(r"const FORDER = \[.*?\];", "const FORDER = __FORDER__;", head); head = re.sub(r"const TORDER = \[.*?\];", "const TORDER = __TORDER__;", head)
head = head.replace('children: [new Paragraph({ children: runs(String(c)', 'children: [new Paragraph({ keepNext: true, children: runs(String(c)')
plain = re.sub(r'\$\{[FT]\(\'\w+\'\)\}', '', body)
POOL = [l.strip() for l in open(HERE + 'u_extra_refs.txt').read().split('\n') if l.strip()] + a_refs.pool()
c_ = a_refs.cites(plain); used, seen = [], set()
for r in POOL:
    k = a_refs.rk(r)
    if k in c_ and k not in seen: seen.add(k); used.append(r)
used.sort(key=lambda r: r.lower())
FP = {('Young', '1993'), ('Golay', '1964'), ('Vapnik', '1995'), ('Yang', '2010'), ('Knapp', '2001'), ('Milton', '1999'), ('Garriga', '2010'), ('Tibshirani', '1993'), ('Rayens', '2003'), ('Guestrin', '2016'), ('Hart', '1967'), ('Lapalme', '2009'), ('Philpot', '1998'), ('Simon', '2006'), ('Talbot', '2010'), ('Cadima', '2016'), ('Le', '2019')}
missing = sorted(x for x in c_ if x not in seen and x[0] not in a_refs.SKIP and 1900 < int(x[1]) < 2028 and x not in FP)
print('missing refs:', missing)
q = lambda s: "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"
body += "\nconst refPara = r => new Paragraph({ spacing: { after: 70, line: 255 }, indent: { left: 400, hanging: 400 }, children: [new TextRun({ text: r, font: FONT, size: 19 })] });\n[" + ',\n'.join(q(r) for r in used) + "].forEach(r => K.push(refPara(r)));"
json.dump(used, open(O + 'refs_used.json', 'w'), indent=0, ensure_ascii=False)
FO = [mm.group(1) for mm in re.finditer(r"\bfig2\('([A-Za-z0-9]+)'", body)]; TO = [mm.group(1) for mm in re.finditer(r"\btab2\('([A-Za-z0-9]+)'", body)]
assert len(FO) == len(set(FO)) and len(TO) == len(set(TO)), 'duplicate keys'
mf = set(re.findall(r"\bF\('([A-Za-z0-9]+)'\)", body)) - set(FO); mt = set(re.findall(r"\bT\('([A-Za-z0-9]+)'\)", body)) - set(TO)
assert not mf and not mt, (mf, mt)
head = head.replace('__FORDER__', repr(FO)).replace('__TORDER__', repr(TO))
tail = T[T.index('\nconst numcfg'):]
tail = tail.replace("title: 'AI-based multimodal UAV sensing of white rust in mustard: complete methodology'", "title: 'ASD leaf models applied to the UAV hyperspectral image of 24 Feb 2026'")
tail = re.sub(r"'eqs', \d+, 'refs', \d+", "'eqs', %d, 'refs', %d" % (len(re.findall(r'K.push\(EQ\(', body)), len(used)), tail)
open(HERE + 'u4_build.js', 'w').write(head + '\n' + body + '\n' + tail)
tn = {k: i + 1 for i, k in enumerate(TO)}; fn = {k: i + 1 for i, k in enumerate(FO)}
json.dump([dict(t, number=tn[t['key']]) for t in TABLES], open(O + 'tables.json', 'w'), indent=0, ensure_ascii=False)
json.dump([dict(f, number=fn[f['key']]) for f in FIGS], open(O + 'figures.json', 'w'), indent=0, ensure_ascii=False)
print('figs', len(FO), 'tabs', len(TO), 'refs', len(used))
