"""Excel workbook of the validation-design comparison (LORO vs grouped 70:30 vs grouped 80:20): guide, designs, side-by-side metrics with
formula differences, best models, paired comparison with formula verdicts, repeated splits with formula summaries, leakage check, feature overlap,
covariate gains, split types, every report table and figure, references."""
import os, json, numpy as np, pandas as pd
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as CL
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule
from openpyxl.chart import BarChart, Reference, Series
from openpyxl.drawing.image import Image as XLImage
from PIL import Image as PILImage
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'; O = HERE + 'out/'; S = HERE + '../'; L = S + 'asd26/data/'
OUT = S + 'outputs/ASD_2025-26_validation_comparison_LORO_70-30_80-20.xlsx'
DES = [(lab, d) for lab, d in (('70:30', S + 'asd7030/'), ('80:20', S + 'asd8020/')) if os.path.exists(d + 'data/metrics_all.csv')]; LABS = ['LORO'] + [l for l, _ in DES]
S3 = pd.read_csv(O + 'cmp3_side.csv'); CP = pd.read_csv(O + 'cmp3_paired.csv') if os.path.exists(O + 'cmp3_paired.csv') else None
SUMM = json.load(open(O + 'cmp3_summary.json')); TABS = json.load(open(O + 'tables.json')); FIGJ = json.load(open(O + 'figures.json')); REFS = json.load(open(O + 'refs_used.json'))
AR = 'Arial'; TF = Font(name=AR, bold=True, size=14, color='1F3864'); SF = Font(name=AR, bold=True, size=11, color='1F3864'); HF = Font(name=AR, bold=True, color='FFFFFF', size=10)
HFILL = PatternFill('solid', fgColor='1F3864'); NF = Font(name=AR, size=10); BLUEF = Font(name=AR, size=10, color='0000FF'); NOTEF = Font(name=AR, size=9, italic=True, color='555555')
BLUE = PatternFill('solid', fgColor='EAF1FB'); thin = Side(style='thin', color='BFBFBF'); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
def cell(ws, r, c, v=None, font=NF, fill=None, fmt=None, wrap=False, text=False):
    if isinstance(v, (np.floating,)): v = float(v)
    if isinstance(v, (np.integer,)): v = int(v)
    if isinstance(v, float) and not np.isfinite(v): v = None
    x = ws.cell(r, c, v); x.font = font
    if text and isinstance(v, str) and v.startswith('='): x.data_type = 's'
    if fill: x.fill = fill
    if fmt: x.number_format = fmt
    if wrap: x.alignment = Alignment(wrap_text=True, vertical='top')
    return x
def header(ws, r, c, labels):
    for j, t in enumerate(labels):
        x = cell(ws, r, c + j, t, HF, HFILL); x.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True); x.border = BOX
def title(ws, t, sub=None, how=None):
    cell(ws, 1, 1, t, TF)
    if sub: cell(ws, 2, 1, sub, NOTEF)
    if how: x = cell(ws, 3, 1, 'HOW TO READ: ' + how, Font(name=AR, size=10, color='1F3864'), BLUE, wrap=True); ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=12); ws.row_dimensions[3].height = 48
def widths(ws, w, first=None, n=20):
    for j in range(1, n + 1): ws.column_dimensions[CL(j)].width = w
    if first: ws.column_dimensions['A'].width = first
def chartfix(ch, t, yt=None, w=22, h=10):
    ch.title = t; ch.roundedCorners = False; ch.width = w; ch.height = h; ch.legend.position = 'b'; ch.legend.overlay = False; ch.x_axis.delete = False; ch.y_axis.delete = False
    if yt: ch.y_axis.title = yt
    return ch
MK = {'macro_F1': 'macro-F1', 'R2': 'R²'}; MAINK = {'A': 'macro_F1', 'B': 'macro_F1', 'C': 'R2'}
wb = Workbook(); ws = wb.active; ws.title = '0_Contents'
# ---------------- 0 contents
title(ws, 'Validation design comparison – LORO vs grouped 70:30 vs grouped 80:20 (ASD leaf spectra, IARI 2025-26)', 'Blue values = data copied from the analyses; black = formulas. Report: ASD_2025-26_validation_comparison_LORO_70-30_80-20_report.docx')
SH = [('0a_Guide', 'how to repeat the comparison on another data set, step by step'), ('1_Designs', 'the three designs, test plots, grade balance, train : validation : test of the networks'), ('2_Side_by_side', 'every metric of every model under each design; differences by formula'),
      ('3_Best_models', 'best overall, ML and DL model of each design'), ('4_Paired', 'same test leaves: LORO vs split with 95% plot-bootstrap intervals; verdict by formula; counts'), ('5_Repeated', '20 other grouped splits per ratio, LORO and leaf-level splits (light pipeline); summary by formulas'),
      ('6_Leakage', 'grouped vs random leaf-level splits (formulas linked to 5_Repeated)'), ('7_Overlap', 'Jaccard similarity of the selected features'), ('8_Cov_gains', 'gain of the spectra over the covariates under each design'),
      ('9_Split_types', 'split types in plant-disease studies; train : validation : test; which models need which'), ('10_R_Tables', 'every table of the Word report'), ('11_R_Figures', 'every figure of the Word report'), ('12_References', 'references')]
header(ws, 5, 1, ['Sheet', 'Content'])
for i, (a, b) in enumerate(SH): cell(ws, 6 + i, 1, a, SF); cell(ws, 6 + i, 2, b)
r = 8 + len(SH); cell(ws, r, 1, 'Key findings', SF)
for i, lab in enumerate(SUMM): cell(ws, r + 1 + i, 1, lab, Font(name=AR, bold=True, size=10)); cell(ws, r + 1 + i, 2, SUMM[lab]['answer'], wrap=True); ws.row_dimensions[r + 1 + i].height = 150
widths(ws, 16, 18); ws.column_dimensions['B'].width = 150
# ---------------- 0a guide
ws = wb.create_sheet('0a_Guide'); title(ws, 'How to repeat this comparison on another data set', 'Each step names the script and the sheet where its result is.')
G = [('1', 'Keep groups together', 'Decide the unit that makes samples dependent (here the plot). Every split must put whole units on one side (Roberts et al., 2017).', 'split_lib.py'),
     ('2', 'Main design: grouped cross-validation', 'Use the blocks of the experiment as folds (here the replications, healthy plots rotated) → every sample tested once (LORO).', 'asd26 pipeline'),
     ('3', 'Hold-out split', 'Split units stratified by block type, treatment, replication; choose the candidate closest to the target share and the class/date balance; fix the seed.', 'split_lib.best_split; 1_Designs'),
     ('4', 'Nested selection and tuning', 'Repeat feature selection, SFFS and grid search on the training part only (inner GroupKFold); networks stop early on part of the training units.', 'a3_select, a3_ml, a4_dl'),
     ('5', 'Side by side', 'Compute every metric under each design.', '2_Side_by_side'),
     ('6', 'Same test samples', 'Score the cross-validation predictions of exactly the hold-out test samples and compare with the hold-out predictions; bootstrap whole units for a 95% interval.', 'c2_compare.py; 4_Paired'),
     ('7', 'Repeated splits', 'Run one identical light pipeline on many other valid hold-out splits and on the cross-validation; compare the spread with the difference.', 'c1_repeat.py; 5_Repeated'),
     ('8', 'Leakage check', 'Run the same light pipeline on random splits of samples that ignore the units; the gain is the leakage.', '6_Leakage'),
     ('9', 'Decide', 'A design "improves" accuracy only if it is higher on the same samples AND across other splits; otherwise report the cross-validation.', '0_Contents (key findings)')]
header(ws, 5, 1, ['Step', 'What', 'How', 'Where'])
for i, g in enumerate(G):
    for j, v in enumerate(g): cell(ws, 6 + i, 1 + j, v, wrap=True)
    ws.row_dimensions[6 + i].height = 45
ws.column_dimensions['A'].width = 6; ws.column_dimensions['B'].width = 30; ws.column_dimensions['C'].width = 110; ws.column_dimensions['D'].width = 30
# ---------------- report tables helper
def put_table(ws, r, key):
    t = next((t for t in TABS if t['key'] == key), None)
    if t is None: return r
    cell(ws, r, 1, 'Table %d. %s' % (t['number'], t['caption']), SF); header(ws, r + 1, 1, t['rows'][0])
    for i, row in enumerate(t['rows'][1:]):
        for j, v in enumerate(row): cell(ws, r + 2 + i, 1 + j, v, wrap=True, text=True)
    return r + 3 + len(t['rows'])
ws = wb.create_sheet('1_Designs'); title(ws, 'The three validation designs', how='Test plots of each design, grade balance of training and test sets, and the effective train : validation : test parts of the networks.')
r = 5
for k in ('designs', 'balance', 'dlparts'): r = put_table(ws, r, k) + 1
widths(ws, 16, 14, 12)
# ---------------- 2 side by side
ws = wb.create_sheet('2_Side_by_side'); title(ws, 'Every metric of every model under each design', how='Blue = metric from each analysis; Δ columns and "better" are formulas (lower is better for RMSE and MAE). Different designs test different leaves, so see 4_Paired for the fair comparison.')
cols = ['task', 'model', 'type', 'metric'] + LABS; header(ws, 5, 1, cols + ['Δ %s − LORO' % l for l in LABS[1:]] + ['%s better?' % l for l in LABS[1:]])
for i, (_, rw) in enumerate(S3.iterrows()):
    rr = 6 + i
    for j, c in enumerate(cols): cell(ws, rr, 1 + j, rw[c], BLUEF if j >= 4 else NF, fmt='0.000' if j >= 4 else None)
    for k, l in enumerate(LABS[1:]):
        dc = 1 + len(cols) + k; cell(ws, rr, dc, '=%s%d-E%d' % (CL(6 + k), rr, rr), fmt='+0.000;-0.000;0.000')
        cell(ws, rr, dc + len(LABS) - 1, '=IF(OR(D{0}="RMSE",D{0}="MAE"),IF({1}{0}<0,"yes","no"),IF({1}{0}>0,"yes","no"))'.format(rr, CL(dc)))
e = 5 + len(S3); r = e + 2; cell(ws, r, 1, 'Summary on the main metric (formulas)', SF); header(ws, r + 1, 1, ['task', 'metric'] + ['%s: models better (n)' % l for l in LABS[1:]] + ['%s: mean Δ' % l for l in LABS[1:]] + ['models (n)'])
for i, t in enumerate('ABC'):
    rr = r + 2 + i; cell(ws, rr, 1, t); cell(ws, rr, 2, MAINK[t])
    for k, l in enumerate(LABS[1:]):
        bc = CL(1 + len(cols) + k + len(LABS) - 1); dc = CL(1 + len(cols) + k)
        cell(ws, rr, 3 + k, '=COUNTIFS($A$6:$A$%d,A%d,$D$6:$D$%d,B%d,$%s$6:$%s$%d,"yes")' % (e, rr, e, rr, bc, bc, e))
        cell(ws, rr, 3 + len(LABS) - 1 + k, '=AVERAGEIFS($%s$6:$%s$%d,$A$6:$A$%d,A%d,$D$6:$D$%d,B%d)' % (dc, dc, e, e, rr, e, rr), fmt='+0.000;-0.000')
    cell(ws, rr, 3 + 2 * (len(LABS) - 1), '=COUNTIFS($A$6:$A$%d,A%d,$D$6:$D$%d,B%d)' % (e, rr, e, rr))
widths(ws, 12, 7); ws.column_dimensions['B'].width = 18
# chart of main metric (task B) from a helper block
hb = r + 7; cell(ws, hb - 1, 1, 'Chart data: main metric per model (linked)', SF); header(ws, hb, 1, ['task / model'] + LABS)
mr = [(i, rw) for i, (_, rw) in enumerate(S3.iterrows()) if rw.metric == MAINK[rw.task]]
for k, (i, rw) in enumerate(mr):
    cell(ws, hb + 1 + k, 1, '%s %s' % (rw.task, rw.model))
    for j in range(len(LABS)): cell(ws, hb + 1 + k, 2 + j, '=%s%d' % (CL(5 + j), 6 + i), fmt='0.000')
ch = BarChart(); ch.type = 'bar'
for j, l in enumerate(LABS): ch.series.append(Series(Reference(ws, min_col=2 + j, min_row=hb + 1, max_row=hb + len(mr)), title=l))
ch.set_categories(Reference(ws, min_col=1, min_row=hb + 1, max_row=hb + len(mr))); ws.add_chart(chartfix(ch, 'Main metric of every model and task', None, 22, 18), 'P5')
# ---------------- 3 best models
ws = wb.create_sheet('3_Best_models'); title(ws, 'Best models of each design'); put_table(ws, 5, 'best'); widths(ws, 26, 8, 6)
# ---------------- 4 paired
ws = wb.create_sheet('4_Paired'); title(ws, 'Same test leaves: LORO predictions of the hold-out test leaves vs the hold-out predictions', how='Δ = split − LORO (formula). Verdict (formula): "no real difference" when the 95% plot-bootstrap interval includes 0; otherwise higher/lower with the split (for RMSE lower Δ is better).')
if CP is not None:
    cols = ['design', 'task', 'model', 'type', 'metric', 'n_leaves', 'n_plots', 'LORO_same', 'split']; header(ws, 5, 1, cols + ['Δ (formula)', 'CI low', 'CI high', 'p (bootstrap)', 'verdict (formula)'])
    for i, (_, rw) in enumerate(CP.iterrows()):
        rr = 6 + i
        for j, c in enumerate(cols): cell(ws, rr, 1 + j, rw[c], BLUEF if j >= 7 else NF, fmt='0.000' if j >= 7 else None)
        cell(ws, rr, 10, '=I%d-H%d' % (rr, rr), fmt='+0.000;-0.000;0.000'); cell(ws, rr, 11, rw.ci_low, BLUEF, fmt='0.000'); cell(ws, rr, 12, rw.ci_high, BLUEF, fmt='0.000'); cell(ws, rr, 13, rw.p_boot, BLUEF, fmt='0.000')
        cell(ws, rr, 14, '=IF(AND(K{0}<=0,L{0}>=0),"no real difference",IF((K{0}>0)=(E{0}<>"RMSE"),"higher","lower"))'.format(rr))
    e = 5 + len(CP); r = e + 2; cell(ws, r, 1, 'Counts on the main metrics (COUNTIFS formulas)', SF); header(ws, r + 1, 1, ['design', 'verdict', 'A macro_F1', 'B macro_F1', 'C R2', 'total'])
    k = 0
    for l in LABS[1:]:
        for vd in ('higher', 'lower', 'no real difference'):
            rr = r + 2 + k; cell(ws, rr, 1, l); cell(ws, rr, 2, vd)
            for j, (t, m_) in enumerate((('A', 'macro_F1'), ('B', 'macro_F1'), ('C', 'R2'))): cell(ws, rr, 3 + j, '=COUNTIFS($A$6:$A$%d,A%d,$B$6:$B$%d,"%s",$E$6:$E$%d,"%s",$N$6:$N$%d,B%d)' % (e, rr, e, t, e, m_, e, rr))
            cell(ws, rr, 6, '=SUM(C%d:E%d)' % (rr, rr)); k += 1
    ws.conditional_formatting.add('N6:N%d' % e, CellIsRule(operator='equal', formula=['"higher"'], fill=PatternFill('solid', fgColor='E2F0D9')))
    ws.conditional_formatting.add('N6:N%d' % e, CellIsRule(operator='equal', formula=['"lower"'], fill=PatternFill('solid', fgColor='FBE5D6')))
widths(ws, 11, 9); ws.column_dimensions['C'].width = 18; ws.column_dimensions['N'].width = 20
# ---------------- 5 repeated + 6 leakage
ws = wb.create_sheet('5_Repeated'); title(ws, 'Repeated grouped splits, LORO and random leaf-level splits (identical light pipeline)', how='Left: every run (blue). Right: summary by AVERAGEIFS, MINIFS, MAXIFS and COUNTIFS formulas. "Above LORO" counts the grouped splits better than LORO.')
runs = []
for lab, d in DES:
    f = d + 'data/cmp_repeat_runs.csv'
    if os.path.exists(f): runs.append(pd.read_csv(f).assign(design=lab))
SUMROWS = {}
if runs:
    RR = pd.concat(runs, ignore_index=True); RR = RR[~((RR.scheme == 'LORO') & (RR.design != LABS[1]))]   # LORO once (identical in both)
    cols = ['design', 'scheme', 'run', 'task', 'n_test', 'macro_F1', 'OA', 'AUC', 'QWK', 'R2', 'RMSE']; RR = RR.reindex(columns=cols); header(ws, 5, 1, cols)
    for i, (_, rw) in enumerate(RR.iterrows()):
        for j, c in enumerate(cols): cell(ws, 6 + i, 1 + j, rw[c], BLUEF if j >= 5 else NF, fmt='0.000' if j >= 5 else None)
    e = 5 + len(RR); sr = lambda c: '$%s$6:$%s$%d' % (c, c, e)
    header(ws, 5, 13, ['design', 'task', 'metric', 'LORO', 'main split', 'grouped mean', 'grouped SD', 'grouped min', 'grouped max', 'above LORO', 'leaf-level mean', 'inflation'])
    k = 0; COLM = {'macro_F1': 'F', 'AUC': 'H', 'QWK': 'I', 'R2': 'J', 'RMSE': 'K'}
    for lab in LABS[1:]:
        for t, m_ in (('A', 'macro_F1'), ('A', 'AUC'), ('B', 'macro_F1'), ('B', 'QWK'), ('C', 'R2'), ('C', 'RMSE')):
            rr = 6 + k; c = COLM[m_]; g = '"grouped %s"' % lab
            cell(ws, rr, 13, lab); cell(ws, rr, 14, t); cell(ws, rr, 15, m_)
            cell(ws, rr, 16, '=AVERAGEIFS(%s,%s,"LORO",%s,"%s")' % (sr(c), sr('B'), sr('D'), t), fmt='0.000')
            cell(ws, rr, 17, '=AVERAGEIFS(%s,%s,"main %s",%s,"%s")' % (sr(c), sr('B'), lab, sr('D'), t), fmt='0.000')
            cell(ws, rr, 18, '=AVERAGEIFS(%s,%s,%s,%s,"%s")' % (sr(c), sr('B'), g, sr('D'), t), fmt='0.000')
            cell(ws, rr, 19, '=SQRT(SUMPRODUCT((%s=%s)*(%s="%s")*(%s-R%d)^2)/(COUNTIFS(%s,%s,%s,"%s")-1))' % (sr('B'), g, sr('D'), t, sr(c), rr, sr('B'), g, sr('D'), t), fmt='0.000')
            cell(ws, rr, 20, '=_xlfn.MINIFS(%s,%s,%s,%s,"%s")' % (sr(c), sr('B'), g, sr('D'), t), fmt='0.000'); cell(ws, rr, 21, '=_xlfn.MAXIFS(%s,%s,%s,%s,"%s")' % (sr(c), sr('B'), g, sr('D'), t), fmt='0.000')
            cell(ws, rr, 22, '=COUNTIFS(%s,%s,%s,"%s",%s,"%s"&P%d)' % (sr('B'), g, sr('D'), t, sr(c), '<' if m_ == 'RMSE' else '>', rr))
            cell(ws, rr, 23, '=AVERAGEIFS(%s,%s,"leaf %s",%s,"%s")' % (sr(c), sr('B'), lab, sr('D'), t), fmt='0.000')
            cell(ws, rr, 24, '=%s' % ('R%d-W%d' % (rr, rr) if m_ == 'RMSE' else 'W%d-R%d' % (rr, rr)), fmt='+0.000;-0.000')
            SUMROWS[(lab, t, m_)] = rr; k += 1
    widths(ws, 11, 9); ws.column_dimensions['B'].width = 15
ws6 = wb.create_sheet('6_Leakage'); title(ws6, 'Leakage check: grouped vs random leaf-level splits', how='Linked to the formula summary of 5_Repeated. Inflation = how much better the leaf-level split looks only because leaves of the same plot are in training and test.')
if SUMROWS:
    header(ws6, 5, 1, ['design', 'task', 'metric', 'grouped (mean of 20)', 'leaf-level (mean of 5)', 'inflation'])
    k = 0
    for lab in LABS[1:]:
        for t, m_ in (('A', 'macro_F1'), ('B', 'macro_F1'), ('C', 'R2')):
            rr = 6 + k; sr_ = SUMROWS[(lab, t, m_)]; cell(ws6, rr, 1, lab); cell(ws6, rr, 2, t); cell(ws6, rr, 3, m_)
            cell(ws6, rr, 4, "='5_Repeated'!R%d" % sr_, fmt='0.000'); cell(ws6, rr, 5, "='5_Repeated'!W%d" % sr_, fmt='0.000'); cell(ws6, rr, 6, '=E%d-D%d' % (rr, rr), fmt='+0.000;-0.000'); k += 1
    ch = BarChart(); ch.type = 'col'
    for j, nm in ((4, 'grouped'), (5, 'random leaf-level')): ch.series.append(Series(Reference(ws6, min_col=j, min_row=6, max_row=5 + k), title=nm))
    ch.set_categories(Reference(ws6, min_col=1, max_col=3, min_row=6, max_row=5 + k)); ws6.add_chart(chartfix(ch, 'Grouped vs random leaf-level splits', 'metric', 20, 9), 'H5')
widths(ws6, 16, 10)
# ---------------- 7 overlap, 8 gains, 9 split types
ws = wb.create_sheet('7_Overlap'); title(ws, 'Do the designs choose the same features? (Jaccard similarity)', how='1 = identical sets, 0 = no common feature. Colour scale: darker = more similar.')
r = 5
txt = open(O + 'cmp3_overlap.csv').read().split('\n\n')
for blk in txt:
    lines = [l for l in blk.strip().split('\n') if l]
    if not lines: continue
    cell(ws, r, 1, lines[0], SF); hdr = lines[1].split(','); header(ws, r + 1, 1, ['set'] + hdr[1:])
    for i, l in enumerate(lines[2:]):
        v = l.split(','); cell(ws, r + 2 + i, 1, v[0])
        for j, x in enumerate(v[1:]): cell(ws, r + 2 + i, 2 + j, float(x), BLUEF, fmt='0.00')
    ws.conditional_formatting.add('B%d:%s%d' % (r + 2, CL(len(hdr)), r + 1 + len(lines) - 2), ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', end_type='num', end_value=1, end_color='2E7D32'))
    r += len(lines) + 2
put_table(ws, r + 1, 'sets'); widths(ws, 18, 26, 10)
ws = wb.create_sheet('8_Cov_gains'); title(ws, 'Gain of the leaf spectra over the covariates under each design'); put_table(ws, 5, 'gains'); widths(ws, 30, 8, 6)
ws = wb.create_sheet('9_Split_types'); title(ws, 'Split types in plant-disease studies; train : validation : test; which models need which')
r = put_table(ws, 5, 'splittypes'); r = put_table(ws, r + 1, 'valroles'); put_table(ws, r + 1, 'dlparts'); ws.column_dimensions['A'].width = 34; ws.column_dimensions['B'].width = 40; ws.column_dimensions['C'].width = 60; ws.column_dimensions['D'].width = 30
# ---------------- 10-12 report tables, figures, references
ws = wb.create_sheet('10_R_Tables'); title(ws, 'Every table of the Word report (same numbering)'); r = 4
for t in TABS: r = put_table(ws, r, t['key']) + 1
widths(ws, 22, 22, 12)
ws = wb.create_sheet('11_R_Figures'); title(ws, 'Every figure of the Word report (same numbering)'); r = 4
for f in FIGJ:
    p = HERE + 'fig/' + f['file']
    if not os.path.exists(p): continue
    cell(ws, r, 1, 'Figure %d. %s' % (f['number'], f['caption']), SF); im = XLImage(p); w0, h0 = PILImage.open(p).size; sc = 900 / w0; im.width, im.height = int(w0 * sc), int(h0 * sc); ws.add_image(im, 'A%d' % (r + 1)); r += int(im.height / 20) + 4
ws = wb.create_sheet('12_References'); title(ws, 'References')
for i, rf in enumerate(REFS): cell(ws, 3 + i, 1, rf)
ws.column_dimensions['A'].width = 180
for w_ in wb.worksheets: w_.sheet_view.zoomScale = 90
wb.calculation.fullCalcOnLoad = True; wb.save(OUT); print('saved', OUT)
