"""Excel workbook of the UAV transfer test (formulas where Excel can compute the metric; native charts)."""
import os, json, numpy as np, pandas as pd
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as CL
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.chart import ScatterChart, BarChart, Reference, Series
from openpyxl.chart.series import SeriesLabel, StrRef
from openpyxl.chart.title import Title
from openpyxl.chart.text import Text, RichText
from openpyxl.chart.axis import ChartLines
from openpyxl.chart.marker import Marker
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.drawing.text import Paragraph, ParagraphProperties, CharacterProperties, RegularTextRun, Font as DFont
HERE = os.path.dirname(os.path.abspath(__file__)); O = HERE + '/out/'
OUT = os.path.join(HERE, '..', 'outputs', 'UAV_24Feb2026_ASD_model_transfer.xlsx')
GT = pd.read_csv(O + 'ground_truth.csv'); MF = pd.read_csv(O + 'metrics_frozen.csv'); PF = pd.read_csv(O + 'predictions_frozen.csv')
MU = pd.read_csv(O + 'metrics_uav_trained.csv'); PU = pd.read_csv(O + 'predictions_uav_trained.csv'); BM = pd.read_csv(O + 'best_models.csv')
SC = pd.read_csv(O + 'spectra_compare.csv'); DF = pd.read_csv(O + 'domain_features.csv'); PC = pd.read_csv(O + 'pca_domain.csv'); SU = json.load(open(O + 'summary.json'))
VAR = ['Direct', 'Healthy-reference corrected', 'Corrected + brightness-normalised']; VSH = {'Direct': 'Direct', 'Healthy-reference corrected': 'Corrected', 'Corrected + brightness-normalised': 'Normalised'}
best = SU['best']; GR = [0, 1, 3, 5, 7, 9]; NP = len(GT)
TN = {'A': 'Detection (healthy vs diseased)', 'B': 'Six-grade severity (0, 1, 3, 5, 7, 9)', 'C': 'Severity score (0-9)'}

AR = 'Arial'; TF = Font(name=AR, bold=True, size=14, color='1F3864'); SF = Font(name=AR, bold=True, size=11, color='1F3864')
HF = Font(name=AR, bold=True, color='FFFFFF', size=10); HFILL = PatternFill('solid', fgColor='1F3864'); NF = Font(name=AR, size=10); BF = Font(name=AR, size=10, bold=True)
INF = Font(name=AR, size=10, color='0000FF'); NOTEF = Font(name=AR, size=9, italic=True, color='555555'); GFILL = PatternFill('solid', fgColor='E2EFDA'); LFILL = PatternFill('solid', fgColor='F2F2F2'); YF = PatternFill('solid', fgColor='FFF2CC')
thin = Side(style='thin', color='BFBFBF'); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
def cell(ws, r, c, v=None, font=NF, fill=None, fmt=None, al=None, border=False, text=False):
    x = ws.cell(r, c, v); x.font = font
    if text and isinstance(v, str) and v.startswith('='): x.data_type = 's'      # show the formula as text, do not evaluate
    if fill: x.fill = fill
    if fmt: x.number_format = fmt
    if al: x.alignment = al
    if border: x.border = BOX
    return x
def header(ws, r, c, labels, widths=None, h=None):
    for j, t in enumerate(labels): cell(ws, r, c + j, t, HF, HFILL, al=Alignment(horizontal='center', vertical='center', wrap_text=True), border=True)
    if widths:
        for j, w in enumerate(widths): ws.column_dimensions[CL(c + j)].width = w
    if h: ws.row_dimensions[r].height = h
def title(ws, t, sub=None):
    cell(ws, 1, 1, t, TF)
    if sub: cell(ws, 2, 1, sub, NOTEF)
def _cp(size, bold=False, color='404040'): return CharacterProperties(sz=int(size * 100), b=bold, solidFill=color, latin=DFont(typeface=AR))
def rich(size): return RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=_cp(size)), endParaRPr=_cp(size))])
def mtitle(t, size=11, color='1F3864'):
    cp = _cp(size, True, color); return Title(tx=Text(rich=RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=cp), r=[RegularTextRun(rPr=cp, t=t)])])), overlay=False)
def axes(ch, xt, yt, xfmt='0', yfmt='0.00'):
    ch.x_axis.title = mtitle(xt, 9, '404040'); ch.y_axis.title = mtitle(yt, 9, '404040'); ch.x_axis.number_format = xfmt; ch.y_axis.number_format = yfmt
    ch.x_axis.delete = False; ch.y_axis.delete = False; ch.x_axis.tickLblPos = 'low'; ch.x_axis.txPr = rich(8); ch.y_axis.txPr = rich(8)
    ch.y_axis.majorGridlines = ChartLines(spPr=GraphicalProperties(ln=LineProperties(solidFill='E3E3E3', w=6350))); ch.roundedCorners = False
    ch.legend.position = 'b'; ch.legend.overlay = False; ch.legend.txPr = rich(8)
def xy(ch, ws, xc, yc, r1, r2, name, color, line=True, marker=None, w=1.75):
    s = Series(Reference(ws, min_col=yc, min_row=r1, max_row=r2), Reference(ws, min_col=xc, min_row=r1, max_row=r2)); s.tx = SeriesLabel(v=name)
    if line: s.marker = Marker(symbol='none'); s.spPr = GraphicalProperties(ln=LineProperties(solidFill=color, w=int(w * 12700)))
    else:
        s.marker = Marker(symbol=marker or 'circle', size=6); s.marker.graphicalProperties = GraphicalProperties(solidFill=color, ln=LineProperties(solidFill=color))
        s.spPr = GraphicalProperties(ln=LineProperties(noFill=True))
    s.smooth = False; ch.series.append(s)
q = lambda sh: "'%s'" % sh

wb = Workbook()
S0, S1, S2, S3, S4, S5, S6 = '0_Contents', '1_Ground_truth', '2_Best_models', '3_Detection', '4_Grade', '5_Score', '6_UAV_trained'
S7, S8, S9, S10, S11 = '7_All_models', '8_Domain_features', '9_Spectra', '10_PCA', '11_All_predictions'
SG, SM, SX, SI, SCALC, SRT, SRF, SGL, S12 = '0a_Guide', '0b_Methods', '0c_Metrics_explained', '0d_Interpretation', '12_Metrics_calculator', '13_R_Tables', '14_R_Figures', '15_Glossary', '16_References'
ws0 = wb.active; ws0.title = S0
for n in (SG, SM, SX, SI, S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11, SCALC, SRT, SRF, SGL, S12): wb.create_sheet(n)
import sys; sys.path.insert(0, HERE)
from u_content import METRICS, GLOSSARY, APPLY
STEPS = json.load(open(O + 'methods.json')); INTERP = json.load(open(O + 'interpretations.json')); TABS = json.load(open(O + 'tables.json')); FIGJ = json.load(open(O + 'figures.json'))
def howto(ws, text, ncol=12, h=60):
    cell(ws, 3, 1, text, Font(name=AR, size=10, color='1F3864'), PatternFill('solid', fgColor='EAF1FB'), al=Alignment(wrap_text=True, vertical='top'))
    ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=ncol); ws.row_dimensions[3].height = h
def itext(key): return ' '.join('%s %s' % (l, t) for l, t in INTERP.get(key, [])).replace('[[F:', 'Figure ').replace('[[T:', 'Table ').replace(']]', '')


# ---------------- 1 ground truth ----------------
ws = wb[S1]; title(ws, 'Ground truth of the 48 UAV plots on 24 Feb 2026 (ASD leaf scores of the same day)',
                  'Mean score = mean 0-9 leaf score of the plot (L3, L5, LL; Conn et al., 1990); PDI = mean score / 9 x 100 (Wheeler, 1969); grade = nearest grade of the mean score; DI class from PDI.')
cols = ['Plot', 'Block', 'Status', 'A (1 = diseased)', 'Variety', 'Sowing', 'Crop stage', 'Leaves scored', 'Mean score (0-9)', 'Mean score L3', 'PDI (%)', 'Grade (nearest)', 'DI class']
header(ws, 4, 1, cols, [6, 7, 10, 9, 8, 8, 12, 9, 10, 10, 9, 9, 9], 32)
for i, r in GT.iterrows():
    rr = 5 + i; fill = GFILL if r.status == 'Healthy' else None
    vals = [int(r['plot']), r.block, r.status, int(r.A), r.variety, r.sowing, r.stage, int(r.n_leaves), round(r.score, 4), None if pd.isna(r.score_L3) else round(r.score_L3, 4)]
    for j, v in enumerate(vals): cell(ws, rr, 1 + j, v, fill=fill, fmt='0.00' if j in (8, 9) else None, border=True)
    cell(ws, rr, 11, '=I%d/9*100' % rr, fill=fill, fmt='0.0', border=True)
    cell(ws, rr, 12, int(r.grade), fill=fill, border=True); cell(ws, rr, 13, '=IF(K%d=0,0,IF(K%d<=5,1,IF(K%d<=10,3,IF(K%d<=25,5,IF(K%d<=50,7,9)))))' % ((rr,) * 5), fill=fill, border=True)
r = 5 + NP + 1
cell(ws, r, 1, 'Counts', SF)
for j, (lab, f) in enumerate([('Healthy plots', '=COUNTIF(C5:C52,"Healthy")'), ('Diseased plots', '=COUNTIF(C5:C52,"Diseased")'), ('Mean score, diseased plots', '=AVERAGEIF(C5:C52,"Diseased",I5:I52)'),
                              ('Score range, diseased', '=TEXT(MIN(I17:I52),"0.0")&" - "&TEXT(MAX(I17:I52),"0.0")')] + [('Plots in grade %d' % g, '=COUNTIF(L5:L52,%d)' % g) for g in GR]):
    cell(ws, r + 1 + j, 1, lab, BF); cell(ws, r + 1 + j, 4, f, fmt='0.00' if 'Mean' in lab else '0')
ws.freeze_panes = 'B5'

# ---------------- prediction sheets with live metrics ----------------
GTC = {'A': 'D', 'B': 'L', 'C': 'I'}
def pred_sheet(sh, t):
    ws = wb[sh]; title(ws, '%s: predictions for the 48 UAV plots and the metrics (live formulas)' % TN[t],
                       'Columns = best ASD models (overall, best ML, best DL) x three input variants, and the best ML type refitted on the UAV plots (in-domain check, leave-one-replication-out).')
    cols = []
    for role in ('overall', 'ML', 'DL'):
        for v in VAR: cols.append(('%s %s | %s' % (role, best[t][role], VSH[v]), PF[(PF.task == t) & (PF.model == best[t][role]) & (PF.variant == v)].sort_values('plot')))
    cols.append(('UAV-trained %s (LORO)' % MU[MU.task == t].model.iloc[0], PU[PU.task == t].sort_values('plot')))
    header(ws, 4, 1, ['Plot', 'Status', 'True'] + [c[0] for c in cols], [6, 10, 8] + [13] * len(cols), 58)
    for i in range(NP):
        rr = 5 + i; fill = GFILL if GT.status[i] == 'Healthy' else None
        cell(ws, rr, 1, i + 1, fill=fill, border=True); cell(ws, rr, 2, GT.status[i], fill=fill, border=True)
        cell(ws, rr, 3, "=%s!%s%d" % (q(S1), GTC[t], rr), BF, fill=fill, fmt='0.00' if t == 'C' else '0', border=True)
        for j, (_, d) in enumerate(cols):
            v = d.pred.values[i]; cell(ws, rr, 4 + j, round(float(v), 3) if t == 'C' else int(v), fill=fill, fmt='0.00' if t == 'C' else '0', border=True)
    R1, R2 = 5, 4 + NP; m0 = R2 + 2
    cell(ws, m0, 1, 'Metrics', SF)
    if t == 'A':
        labs = ['Overall accuracy', 'Sensitivity (diseased found)', 'Specificity (healthy found)', 'Balanced accuracy', 'Plots predicted diseased', 'Macro-F1 (Python)', 'AUC (Python)']
        for k, lab in enumerate(labs): cell(ws, m0 + 1 + k, 1, lab, BF, LFILL, border=True); ws.merge_cells(start_row=m0 + 1 + k, start_column=1, end_row=m0 + 1 + k, end_column=3)
        for j, (name, d) in enumerate(cols):
            L = CL(4 + j); P_ = '%s%d:%s%d' % (L, R1, L, R2); T_ = '$C$%d:$C$%d' % (R1, R2)
            f = ['=SUMPRODUCT(--(%s=%s))/COUNT(%s)' % (P_, T_, T_), '=COUNTIFS(%s,1,%s,1)/COUNTIF(%s,1)' % (T_, P_, T_), '=COUNTIFS(%s,0,%s,0)/COUNTIF(%s,0)' % (T_, P_, T_),
                 '=(%s%d+%s%d)/2' % (L, m0 + 2, L, m0 + 3), '=SUM(%s)' % P_]
            for k, ff in enumerate(f): cell(ws, m0 + 1 + k, 4 + j, ff, BF if k == 3 else NF, fmt='0' if k == 4 else '0.000', border=True)
            mrow = MU[MU.task == t].iloc[0] if name.startswith('UAV') else MF[(MF.task == t) & (MF.model == best[t][name.split(' ')[0]]) & (MF.variant == [v for v in VAR if VSH[v] == name.split(' | ')[1]][0])].iloc[0]
            cell(ws, m0 + 6, 4 + j, round(float(mrow.macro_F1), 4), fmt='0.000', border=True); cell(ws, m0 + 7, 4 + j, None if pd.isna(mrow.AUC) else round(float(mrow.AUC), 4), fmt='0.000', border=True)
        # confusion matrices by COUNTIFS
        c0 = m0 + 10; cell(ws, c0, 1, 'Confusion matrices (rows = true, columns = predicted; COUNTIFS)', SF)
        for j, (name, d) in enumerate(cols):
            rb = c0 + 1 + (j // 5) * 5; cb = 1 + (j % 5) * 4; L = CL(4 + j); P_ = '$%s$%d:$%s$%d' % (L, R1, L, R2); T_ = '$C$%d:$C$%d' % (R1, R2)
            cell(ws, rb, cb, name, BF); cell(ws, rb + 1, cb + 1, 'Pred H', BF, LFILL, border=True); cell(ws, rb + 1, cb + 2, 'Pred D', BF, LFILL, border=True)
            for a_, lab in ((0, 'True H'), (1, 'True D')):
                cell(ws, rb + 2 + a_, cb, lab, BF, LFILL, border=True)
                for b_ in (0, 1): cell(ws, rb + 2 + a_, cb + 1 + b_, '=COUNTIFS(%s,%d,%s,%d)' % (T_, a_, P_, b_), fmt='0', border=True, fill=YF if a_ == b_ else None)
    elif t == 'B':
        labs = ['Overall accuracy', 'Within one grade', 'Mean grade steps away', 'Macro-F1 (Python)', 'QWK (Python)']
        for k, lab in enumerate(labs): cell(ws, m0 + 1 + k, 1, lab, BF, LFILL, border=True); ws.merge_cells(start_row=m0 + 1 + k, start_column=1, end_row=m0 + 1 + k, end_column=3)
        hc = 4 + len(cols) + 1; cell(ws, 3, hc, 'Grade steps away |position(pred) - position(true)| (helper for within-one)', NOTEF)
        for j, (name, d) in enumerate(cols):
            L = CL(4 + j); H = CL(hc + j); header(ws, 4, hc + j, ['steps: ' + name], [11])
            for i in range(NP):
                rr = 5 + i; cell(ws, rr, hc + j, '=ABS(MATCH(%s%d,{0,1,3,5,7,9},0)-MATCH($C%d,{0,1,3,5,7,9},0))' % (L, rr, rr), fmt='0', border=True)
            P_ = '%s%d:%s%d' % (L, R1, L, R2); T_ = '$C$%d:$C$%d' % (R1, R2); Hh = '%s%d:%s%d' % (H, R1, H, R2)
            for k, ff in enumerate(['=SUMPRODUCT(--(%s=%s))/COUNT(%s)' % (P_, T_, T_), '=COUNTIF(%s,"<=1")/COUNT(%s)' % (Hh, Hh), '=AVERAGE(%s)' % Hh]):
                cell(ws, m0 + 1 + k, 4 + j, ff, BF if k == 0 else NF, fmt='0.000' if k < 2 else '0.00', border=True)
            mrow = MU[MU.task == t].iloc[0] if name.startswith('UAV') else MF[(MF.task == t) & (MF.model == best[t][name.split(' ')[0]]) & (MF.variant == [v for v in VAR if VSH[v] == name.split(' | ')[1]][0])].iloc[0]
            cell(ws, m0 + 4, 4 + j, round(float(mrow.macro_F1), 4), fmt='0.000', border=True); cell(ws, m0 + 5, 4 + j, None if pd.isna(mrow.QWK) else round(float(mrow.QWK), 4), fmt='0.000', border=True)
        c0 = m0 + 8; cell(ws, c0, 1, 'Confusion matrices of the best overall model (rows = true grade, columns = predicted grade; COUNTIFS)', SF)
        for j in (0, 1, 2, len(cols) - 1):
            name = cols[j][0]; k_ = [0, 1, 2, len(cols) - 1].index(j); rb = c0 + 1 + (k_ // 2) * 10; cb = 1 + (k_ % 2) * 9
            L = CL(4 + j); P_ = '$%s$%d:$%s$%d' % (L, R1, L, R2); T_ = '$C$%d:$C$%d' % (R1, R2); cell(ws, rb, cb, name, BF)
            for g_i, g in enumerate(GR):
                cell(ws, rb + 1, cb + 1 + g_i, 'P%d' % g, BF, LFILL, border=True); cell(ws, rb + 2 + g_i, cb, 'T%d' % g, BF, LFILL, border=True)
                for h_i, h in enumerate(GR): cell(ws, rb + 2 + g_i, cb + 1 + h_i, '=COUNTIFS(%s,%d,%s,%d)' % (T_, g, P_, h), fmt='0', border=True, fill=YF if g == h else None)
    else:
        labs = ['R² = 1 - SSE/SST', 'RMSE', 'MAE', 'Bias (mean pred - mean true)', 'Pearson r (all plots)', 'Pearson r (36 diseased plots)', 'RPD = SD(true)/RMSE', 'Min prediction', 'Max prediction']
        for k, lab in enumerate(labs): cell(ws, m0 + 1 + k, 1, lab, BF, LFILL, border=True); ws.merge_cells(start_row=m0 + 1 + k, start_column=1, end_row=m0 + 1 + k, end_column=3)
        for j, (name, d) in enumerate(cols):
            L = CL(4 + j); P_ = '%s%d:%s%d' % (L, R1, L, R2); T_ = '$C$%d:$C$%d' % (R1, R2); Pd = '%s%d:%s%d' % (L, R1 + 12, L, R2); Td = '$C$%d:$C$%d' % (R1 + 12, R2)
            f = ['=1-SUMXMY2(%s,%s)/DEVSQ(%s)' % (P_, T_, T_), '=SQRT(SUMXMY2(%s,%s)/COUNT(%s))' % (P_, T_, T_), '=SUMPRODUCT(ABS(%s-%s))/COUNT(%s)' % (P_, T_, T_),
                 '=AVERAGE(%s)-AVERAGE(%s)' % (P_, T_), '=IF(STDEV(%s)=0,"-",CORREL(%s,%s))' % (P_, P_, T_), '=IF(STDEV(%s)=0,"-",CORREL(%s,%s))' % (Pd, Pd, Td),
                 '=STDEV(%s)/%s%d' % (T_, L, m0 + 2), '=MIN(%s)' % P_, '=MAX(%s)' % P_]
            for k, ff in enumerate(f): cell(ws, m0 + 1 + k, 4 + j, ff, BF if k in (0, 1) else NF, fmt='0.000' if k != 1 else '0.00', border=True)
        # scatter charts: true vs predicted, best overall model (three variants) + UAV-trained
        for k_, j in enumerate([0, 1, 2, len(cols) - 1]):
            ch = ScatterChart(); ch.title = mtitle(cols[j][0], 10); ch.style = 2; ch.width, ch.height = 12, 9
            xy(ch, ws, 3, 4 + j, R1, R1 + 11, 'healthy plots', '1A9850', line=False); xy(ch, ws, 3, 4 + j, R1 + 12, R2, 'diseased plots', 'D73027', line=False)
            axes(ch, 'True plot mean leaf score', 'Predicted score', '0', '0'); ch.x_axis.scaling.min, ch.x_axis.scaling.max = 0, 9; ch.y_axis.scaling.min, ch.y_axis.scaling.max = 0, 9
            ws.add_chart(ch, '%s%d' % (CL(4 + len(cols) + 1 + (k_ % 2) * 8), 5 + (k_ // 2) * 19))
    ws.freeze_panes = 'D5'
    return cols
for sh, t in ((S3, 'A'), (S4, 'B'), (S5, 'C')): pred_sheet(sh, t)

# ---------------- 2 best models ----------------
ws = wb[S2]; title(ws, 'Best ASD models and their accuracy: ASD leaves (LORO) vs UAV plots of 24 Feb 2026',
                  'Best = highest leave-one-replication-out score on the ASD leaves (macro-F1 for A and B, R² for C). UAV columns: the frozen model applied to the plot spectra; last column: same ML type refitted on the UAV plots.')
KEY = {'A': ('macro_F1', 'macro-F1'), 'B': ('macro_F1', 'macro-F1'), 'C': ('R2', 'R²')}
header(ws, 4, 1, ['Task', 'Role', 'Model', 'Metric', 'ASD leaves (LORO)'] + ['UAV %s' % VSH[v] for v in VAR] + ['UAV-trained (LORO, best ML type)', 'Drop from ASD to best UAV variant'],
       [30, 9, 18, 9, 12, 12, 12, 12, 16, 14], 45)
r = 5
for t in 'ABC':
    for role in ('overall', 'ML', 'DL'):
        b = BM[(BM.task == t) & (BM.role == role)].iloc[0]; key, lab = KEY[t]
        cell(ws, r, 1, TN[t], border=True); cell(ws, r, 2, role, border=True); cell(ws, r, 3, b.model, BF, border=True); cell(ws, r, 4, lab, border=True)
        cell(ws, r, 5, round(float(b.asd_value), 4), fmt='0.000', border=True, fill=LFILL)
        for k, v in enumerate(VAR):
            m = MF[(MF.task == t) & (MF.model == b.model) & (MF.variant == v)]; cell(ws, r, 6 + k, round(float(m[key].iloc[0]), 4), fmt='0.000', border=True)
        if role == 'ML': cell(ws, r, 9, round(float(MU[MU.task == t][key].iloc[0]), 4), fmt='0.000', border=True, fill=GFILL)
        cell(ws, r, 10, '=E%d-MAX(F%d:H%d)' % (r, r, r), fmt='0.000', border=True)
        r += 1
cell(ws, r + 1, 1, 'ASD values: leave-one-replication-out test on 2330 leaves (asd26/data/metrics_all.csv). UAV values: 48 plots, ground truth = ASD leaf scores of 24 Feb 2026 (1_Ground_truth).', NOTEF)
ch = BarChart(); ch.type = 'col'; ch.grouping = 'clustered'; ch.title = mtitle('Best overall model per task: ASD leaves vs UAV plots', 11); ch.width, ch.height = 24, 9
for k, (c, lab) in enumerate([(5, 'ASD leaves (LORO)')] + [(6 + i, 'UAV ' + VSH[v]) for i, v in enumerate(VAR)]):
    s = Series(Reference(ws, min_col=c, min_row=5, max_row=13), title=None); s.tx = SeriesLabel(v=lab); s.spPr = GraphicalProperties(solidFill=['999999', '4C72B0', 'DD8452', '8172B3'][k]); ch.series.append(s)
ch.set_categories(Reference(ws, min_col=3, min_row=5, max_row=13)); axes(ch, 'Model (rows of the table: A overall/ML/DL, B ..., C ...)', 'Score (macro-F1 or R²)', yfmt='0.0')
ch.y_axis.scaling.min = -1; ch.y_axis.scaling.max = 1
ws.add_chart(ch, 'A17')

# ---------------- 6 UAV-trained ----------------
ws = wb[S6]; title(ws, 'In-domain check: best ML model type refitted on the UAV plots (leave-one-replication-out)',
                  'Same folds as the ASD analysis (R1, R2, R3 with the healthy plots rotated); same hyper-parameters; features inside the UAV band gaps removed. Shows what the canopy spectra support when trained on UAV data.')
header(ws, 4, 1, ['Task', 'Model', 'Features used', 'Gap features removed', 'macro-F1', 'Balanced acc.', 'AUC', 'OA', 'QWK', 'Within one', 'R²', 'RMSE', 'r'], [26, 10, 50, 16, 9, 9, 9, 9, 9, 9, 9, 9, 9], 30)
for i, rr_ in enumerate(MU.itertuples()):
    r = 5 + i; vals = [TN[rr_.task], rr_.model, rr_.features, rr_.dropped_gap_features if isinstance(rr_.dropped_gap_features, str) else '-']
    for j, v in enumerate(vals): cell(ws, r, 1 + j, v, border=True, al=Alignment(wrap_text=True, vertical='top'))
    for j, k in enumerate(['macro_F1', 'balanced_acc', 'AUC', 'OA', 'QWK', 'within1', 'R2', 'RMSE', 'r']):
        v = getattr(rr_, k, np.nan); cell(ws, r, 5 + j, None if pd.isna(v) else round(float(v), 4), fmt='0.000', border=True)
    ws.row_dimensions[r].height = 30
header(ws, 10, 1, ['Plot', 'Fold', 'Status', 'A true', 'A pred', 'A score', 'B true', 'B pred', 'C true', 'C pred'], None, 28)
for i in range(NP):
    r = 11 + i; a = PU[(PU.task == 'A') & (PU['plot'] == i + 1)].iloc[0]; b = PU[(PU.task == 'B') & (PU['plot'] == i + 1)].iloc[0]; c = PU[(PU.task == 'C') & (PU['plot'] == i + 1)].iloc[0]
    for j, v in enumerate([i + 1, int(a.fold), GT.status[i], int(a.y), int(a.pred), round(float(a.score), 3), int(b.y), int(b.pred), round(float(c.y), 3), round(float(c.pred), 3)]):
        cell(ws, r, 1 + j, v, border=True, fill=GFILL if GT.status[i] == 'Healthy' else None)

# ---------------- 7 all models ----------------
ws = wb[S7]; title(ws, 'All 30 ASD models (15 ML + 15 DL) x three input variants on the UAV plots', 'Computed in Python (scikit-learn). Colour scale per metric column. pred_* = how often each class was predicted.')
cols = ['task', 'model', 'source', 'variant', 'macro_F1', 'balanced_acc', 'sensitivity', 'specificity', 'AUC', 'pred_diseased', 'OA', 'QWK', 'within1', 'pred_grades', 'R2', 'RMSE', 'MAE', 'bias', 'r', 'r_diseased', 'pred_min', 'pred_max']
header(ws, 4, 1, cols, [5, 16, 7, 26] + [10] * 9 + [26] + [9] * 8, 30)
D7 = MF.sort_values(['task', 'source', 'model', 'variant']).reset_index(drop=True)
for i, rr_ in D7.iterrows():
    for j, k in enumerate(cols):
        v = rr_.get(k, None); v = None if (isinstance(v, float) and np.isnan(v)) else v
        cell(ws, 5 + i, 1 + j, round(float(v), 4) if isinstance(v, (float, np.floating)) else v, fmt='0.000' if isinstance(v, (float, np.floating)) else None, border=True)
for k in ('macro_F1', 'balanced_acc', 'AUC', 'OA', 'QWK', 'within1', 'R2', 'r'):
    L = CL(1 + cols.index(k)); ws.conditional_formatting.add('%s5:%s%d' % (L, L, 4 + len(D7)), ColorScaleRule(start_type='min', start_color='F8696B', mid_type='percentile', mid_value=50, mid_color='FFEB84', end_type='max', end_color='63BE7B'))
ws.freeze_panes = 'E5'; ws.auto_filter.ref = 'A4:%s%d' % (CL(len(cols)), 4 + len(D7))

# ---------------- 8 domain features ----------------
ws = wb[S8]; title(ws, 'Domain check: input features of the best models on ASD leaves vs UAV plots',
                  'ASD range = 1st-99th percentile of the 2330 leaves. % out = share of the 48 UAV plots outside that range. Gap = the feature lies inside a band removed from the UAV image (value interpolated).')
cols = ['feature', 'in_uav_gap', 'asd_mean', 'asd_sd', 'asd_p1', 'asd_p99'] + ['uav_%s_%s' % (t_, m_) for t_ in ('direct', 'corrected', 'normalised') for m_ in ('mean', 'out_pct', 'z')]
labs = ['Feature', 'In UAV band gap', 'ASD mean', 'ASD SD', 'ASD 1st pct', 'ASD 99th pct'] + ['%s %s' % (t_, {'mean': 'mean', 'out_pct': '% out', 'z': 'shift (SD)'}[m_]) for t_ in ('Direct', 'Corrected', 'Normalised') for m_ in ('mean', 'out_pct', 'z')]
header(ws, 4, 1, labs, [10, 9] + [11] * 13, 32)
for i, rr_ in DF.iterrows():
    for j, k in enumerate(cols):
        v = rr_[k]; isf = isinstance(v, (float, np.floating)) and not isinstance(v, bool)
        fmt = '0.0' if 'out_pct' in k else '0.00' if k.endswith('_z') else ('0.000E+00' if (isf and abs(v) < 0.01 and v != 0) else '0.000')
        cell(ws, 5 + i, 1 + j, ('yes' if v else 'no') if k == 'in_uav_gap' else (float(v) if isf else v), fmt=fmt if isf else None, border=True, fill=YF if (k == 'in_uav_gap' and v) else None)
ch = BarChart(); ch.type = 'bar'; ch.grouping = 'clustered'; ch.title = mtitle('UAV plots outside the ASD training range (%)', 11); ch.width, ch.height = 18, 11
for k, (c, lab, col) in enumerate([(8, 'Direct', '4C72B0'), (11, 'Corrected', 'DD8452'), (14, 'Normalised', '8172B3')]):
    s = Series(Reference(ws, min_col=c, min_row=5, max_row=4 + len(DF)), title=None); s.tx = SeriesLabel(v=lab); s.spPr = GraphicalProperties(solidFill=col); ch.series.append(s)
ch.set_categories(Reference(ws, min_col=1, min_row=5, max_row=4 + len(DF))); axes(ch, 'Feature', '% of UAV plots', yfmt='0'); ch.y_axis.scaling.min, ch.y_axis.scaling.max = 0, 100
ch.x_axis.scaling.orientation = 'maxMin'
ws.add_chart(ch, 'B%d' % (7 + len(DF)))

# ---------------- 9 spectra ----------------
ws = wb[S9]; title(ws, 'Mean spectra: ASD leaves vs UAV plots of 24 Feb 2026 (three input variants)', 'ASD spectra interpolated to the UAV wavelengths; UAV band gaps (900-915, 1330-1460, 1780-1970 nm) are blank rows.')
cols = list(SC.columns); header(ws, 4, 1, cols, [12] + [14] * (len(cols) - 1), 45)
wl = SC.wavelength.values; gaps = set(np.where(np.diff(wl) > 8)[0] + 1); rows = []; r = 5
for i in range(len(SC)):
    if i in gaps: r += 1
    rows.append(r); r += 1
for i, rr_ in enumerate(rows):
    for j, c in enumerate(cols): cell(ws, rr_, 1 + j, round(float(SC[c].iloc[i]), 5), fmt='0.0' if j == 0 else '0.0000')
RL = rows[-1]
for k, (ttl, a, b_) in enumerate([('Direct: ASD leaves vs UAV plots', 'UAV healthy', 'UAV diseased'), ('Healthy-reference corrected', 'UAV healthy corrected', 'UAV diseased corrected'),
                                   ('Corrected + brightness-normalised', 'UAV healthy normalised', 'UAV diseased normalised')]):
    ch = ScatterChart(); ch.title = mtitle(ttl, 11); ch.style = 2; ch.width, ch.height = 16, 9; ch.display_blanks = 'gap'
    for nm, colr, w_ in (('ASD healthy (24 Feb)', '7FBF7B', 1.25), ('ASD diseased (24 Feb)', 'F4A582', 1.25), (a, '1A9850', 2.25), (b_, 'D73027', 2.25)):
        xy(ch, ws, 1, 1 + cols.index(nm), 5, RL, nm, colr, w=w_)
    axes(ch, 'Wavelength (nm)', 'Reflectance'); ch.x_axis.scaling.min, ch.x_axis.scaling.max, ch.x_axis.majorUnit = 400, 2400, 200
    ws.add_chart(ch, '%s%d' % (CL(len(cols) + 2), 4 + k * 19))
ws.freeze_panes = 'B5'

# ---------------- 10 PCA ----------------
ws = wb[S10]; title(ws, 'PCA of the model input features: ASD leaves and UAV plots (projected)', 'PCA fitted on the standardised features of the 2330 ASD leaves; UAV plots projected onto the same axes. PC1 %.0f %%, PC2 %.0f %% of the ASD variance.' % (100 * SU['pca_var'][0], 100 * SU['pca_var'][1]))
groups = [('ASD leaf', 'Healthy', 'ASD leaves healthy', '7FBF7B', 'circle'), ('ASD leaf', 'Diseased', 'ASD leaves diseased', 'F4A582', 'circle'),
          ('UAV plot (direct)', 'Healthy', 'UAV direct healthy', '1A9850', 'square'), ('UAV plot (direct)', 'Diseased', 'UAV direct diseased', 'D73027', 'square'),
          ('UAV plot (corrected + brightness-normalised)', 'Healthy', 'UAV normalised healthy', '1A9850', 'triangle'), ('UAV plot (corrected + brightness-normalised)', 'Diseased', 'UAV normalised diseased', 'D73027', 'triangle')]
ch = ScatterChart(); ch.title = mtitle('ASD leaves vs UAV plots (PC1-PC2)', 11); ch.style = 2; ch.width, ch.height = 18, 13
c = 1
for src, grp, lab, colr, mk in groups:
    d = PC[(PC.source == src) & (PC.group == grp)]
    header(ws, 4, c, [lab + ' PC1', 'PC2'], [11, 11], 32)
    for i, (x1, x2) in enumerate(zip(d.PC1, d.PC2)): cell(ws, 5 + i, c, round(float(x1), 4), fmt='0.00'); cell(ws, 5 + i, c + 1, round(float(x2), 4), fmt='0.00')
    xy(ch, ws, c, c + 1, 5, 4 + len(d), lab, colr, line=False, marker=mk)
    c += 2
axes(ch, 'PC1', 'PC2', '0', '0')
ws.add_chart(ch, '%s4' % CL(c + 1))

# ---------------- 11 all predictions (long) ----------------
ws = wb[S11]; title(ws, 'All predictions (30 models x 3 variants x 48 plots; long format)', 'Filter by task, model and variant. For task A, score = decision value (SVM) or probability of disease.')
cols = ['task', 'model', 'source', 'variant', 'plot', 'y', 'pred', 'score']; header(ws, 4, 1, ['Task', 'Model', 'Source', 'Variant', 'Plot', 'True', 'Predicted', 'Score/probability'], [6, 18, 7, 28, 6, 8, 10, 14])
for i, rr_ in enumerate(PF[cols].itertuples(index=False)):
    for j, v in enumerate(rr_):
        if isinstance(v, float) and np.isnan(v): v = None
        cell(ws, 5 + i, 1 + j, round(float(v), 4) if isinstance(v, (float, np.floating)) else v)
ws.auto_filter.ref = 'A4:H%d' % (4 + len(PF)); ws.freeze_panes = 'A5'

# ---------------- 12 references ----------------
ws = wb[S12]; title(ws, 'References')
REFS = json.load(open(O + 'refs_used.json')) if os.path.exists(O + 'refs_used.json') else []
for i, t_ in enumerate(REFS): cell(ws, 3 + i, 1, t_, al=Alignment(wrap_text=True, vertical='top')); ws.row_dimensions[3 + i].height = 30
ws.column_dimensions['A'].width = 150

# ---------------- how-to-read notes on every analysis sheet (row 3) ----------------
howto(wb[S1], 'HOW TO READ: one row per plot. Column D (A) is the detection label, I the plot mean leaf score (task C) and L its nearest grade (task B). PDI and DI class are computed by formulas (columns K, M). These are the "true" values against which all predictions are judged (method step M2).', 13, 45)
howto(wb[S2], 'HOW TO READ: each row is one best ASD model (overall, best ML, best DL per task). Column E = its score on the leaves (LORO); F-H = the same frozen model on the UAV plots with three inputs; I = the same model type trained on the UAV plots; J = drop from leaves to the best UAV input (formula). ' + itext('summary'), 10, 75)
howto(wb[S3], 'HOW TO READ: rows 5-52 = predicted class (0 healthy, 1 diseased) of each plot by each model/input; the metric rows below are live Excel formulas (accuracy, sensitivity, specificity, balanced accuracy) - change a prediction and they update. Confusion matrices below use COUNTIFS. ' + itext('detection'), 14, 105)
howto(wb[S4], 'HOW TO READ: predicted grade (0, 1, 3, 5, 7, 9) of each plot; helper columns on the right give the number of grade steps between prediction and truth (used for "within one grade"). ' + itext('grades'), 14, 105)
howto(wb[S5], 'HOW TO READ: predicted score (0-9) of each plot; metric rows (R², RMSE, MAE, bias, r, RPD) are live formulas; scatter charts on the right plot predicted vs true. ' + itext('score'), 14, 105)
howto(wb[S6], 'HOW TO READ: the best ML model type of each task retrained on the 48 UAV plots with leave-one-replication-out (same folds as the ASD analysis). It shows what the UAV spectra can support when a model learns from them (method step M7). ' + itext('indomain'), 13, 95)
howto(wb[S7], 'HOW TO READ: every one of the 30 ASD models with each input; colour scale green (better) to red (worse) per column; use the filter buttons in row 4 to select a task, model or input. ' + itext('allmodels'), 22, 75)
howto(wb[S8], 'HOW TO READ: for each input feature of the best models: the leaf range (1st-99th percentile of 2330 leaves) and the share of UAV plots outside it (% out) for each input; shift = difference of means in leaf SD units. Long bars in the chart = extrapolation (method step M6). ' + itext('domain'), 15, 105)
howto(wb[S9], 'HOW TO READ: mean spectra of ASD leaves and UAV plots of 24 Feb (healthy and diseased) for the three inputs; blank rows = UAV band gaps. ' + itext('spectra'), 11, 90)
howto(wb[S10], 'HOW TO READ: PCA fitted on the 2330 leaves (standardised model features); UAV plots projected on the same axes. Points far from the leaf cloud are outside the model domain (Mahalanobis distance; method step M6).', 12, 40)
howto(wb[S11], 'HOW TO READ: every prediction (30 models x 3 inputs x 48 plots). Use the filters in row 4. Task A score = SVM decision value or probability of disease.', 8, 35)

# ---------------- 0a guide ----------------
ws = wb[SG]; title(ws, 'Step-by-step guide: what was done, why, how, and how to repeat it on another data set', 'Read this sheet first. Each step names the sheet where its input or output is, the Excel formula or Python script used, and the supporting reference.')
header(ws, 4, 1, ['Step', 'What is done', 'Why', 'How (in short)', 'Input', 'Output / sheet', 'Excel formula or script', 'Reference'], [6, 26, 34, 50, 22, 24, 30, 30], 30)
GUIDE = [('M1', 'Read the UAV plot mean spectra', 'The test must use the UAV data', 'ENVI ASCII file -> 48 x 483 matrix; check gaps, negatives, brightness', 'envi_plot_avg.txt', '9_Spectra', 'u1_apply.py (section UAV plot spectra)', 'Aasen et al. (2018)'),
         ('M2', 'Build the ground truth of 24 Feb', 'Accuracy needs same-day observations', 'Mean leaf score per plot; nearest grade; status from the block', 'ASD leaf scores (24 Feb)', '1_Ground_truth', 'K: =I/9*100; M: IF ladder for DI class', 'Conn et al. (1990); Wheeler (1969)'),
         ('M3', 'Select the best ASD models', 'Only LORO-tested models are fair candidates', 'Highest LORO macro-F1 (A, B) or R² (C); overall, best ML, best DL', 'ASD metrics_all.csv', '2_Best_models', 'best_models.json', 'Roberts et al. (2017)'),
         ('M4', 'Same pre-processing', 'Inputs must match training', '1-nm resampling, Savitzky-Golay 11/2, first derivative, 5-nm bands, indices; scaler from the model file', 'UAV spectra', 'out/uav_features_*.csv', 'wr_features.all_features()', 'Savitzky and Golay (1964); Tsai and Philpot (1998)'),
         ('M5', 'Three inputs', 'Reduce the leaf-canopy difference', 'Direct; x gain(ASD healthy / UAV healthy, leave-one-out); + brightness normalisation', 'UAV + ASD healthy spectra', '9_Spectra', 'u1_apply.py (section spectra variants)', 'Smith and Milton (1999); Barnes et al. (1989)'),
         ('M6', 'Domain check', 'Explains failure before accuracy is judged', '% of plots outside the leaf 1st-99th percentile; PCA + Mahalanobis distance', 'Feature tables', '8_Domain_features, 10_PCA', 'u1_apply.py (domain check)', 'Sahigara et al. (2012); Jolliffe and Cadima (2016)'),
         ('M7', 'In-domain check', 'Is there a signal in the UAV data?', 'Best ML type refitted on UAV plots, LORO folds; permutation test', 'UAV features + truth', '6_UAV_trained', 'u1_apply.py (in-domain, permutation)', 'Ojala and Garriga (2010)'),
         ('M8', 'Accuracy and uncertainty', 'Quantify agreement and its uncertainty', 'Measures in 0c; bootstrap 95 % CI (2000 resamples of plots)', 'Predictions + truth', '2-7, 12, 13', 'formulas in 3_Detection, 4_Grade, 5_Score, 12_Metrics_calculator', 'Sokolova and Lapalme (2009); Efron and Tibshirani (1993)')]
for i, g in enumerate(GUIDE):
    for j, v in enumerate(g): cell(ws, 5 + i, 1 + j, v, BF if j == 0 else NF, border=True, al=Alignment(wrap_text=True, vertical='top'))
    ws.row_dimensions[5 + i].height = 45
r = 5 + len(GUIDE) + 1; cell(ws, r, 1, 'How to apply the procedure to another data set', SF)
header(ws, r + 1, 1, ['Step', 'What to do', 'Details', 'Tool / template', 'Method step'], None, 28)
for i, g in enumerate(APPLY):
    for j, v in enumerate(g): cell(ws, r + 2 + i, 1 + j, v, BF if j == 0 else NF, border=True, al=Alignment(wrap_text=True, vertical='top'))
    ws.row_dimensions[r + 2 + i].height = 45
r = r + 2 + len(APPLY) + 1; cell(ws, r, 1, 'Commands (run from thesis_build/uavt; ASD models in outputs/ASD_2025-26_models)', SF)
CMDS = ['python3 u1_apply.py            # predictions, metrics, domain check, in-domain check, confidence intervals, permutation tests -> out/',
        'python3 u2_figs.py             # figures -> fig/', 'python3 u4_word.py && node u4_build.js && python3 ../satmet/to_pdf.py <docx> <pdf>   # Word + PDF (also writes the shared tables/figures/methods)',
        'python3 u3_excel.py && python3 recalc.py <xlsx>   # this workbook (formulas recalculated)', 'python3 u5_pptdata.py && node u5_ppt.js   # slides',
        'To use another UAV image: replace uavhs/data/envi_plot_avg.txt and DATE in u1_apply.py; to use another model set: point MD in u1_apply.py to its folder.']
for i, c_ in enumerate(CMDS): cell(ws, r + 1 + i, 1, c_, Font(name='Courier New', size=9)); ws.merge_cells(start_row=r + 1 + i, start_column=1, end_row=r + 1 + i, end_column=8)
ws.freeze_panes = 'A5'

# ---------------- 0b methods ----------------
ws = wb[SM]; title(ws, 'Methodology in detail (the same text as Chapter 2 of the Word report)', 'One row per method step: position, concept, justification, what the reference papers did, how it is done (numbered), how it was applied here, equations, output, notes and a likely question.')
cols = ['Step', 'Title', 'Position in the workflow', 'Concept', 'Why it is needed here', 'What the reference papers did', 'How it is done', 'How it was applied to these data', 'Equations', 'Output', 'Notes and alternatives', 'Likely question']
header(ws, 4, 1, cols, [6, 22, 22, 40, 40, 44, 60, 44, 34, 30, 40, 34], 30)
for i, st in enumerate(STEPS):
    vals = [st['no'], st['title'], st['position'], st['concept'], st['why'], st['papers'], '\n'.join('%d. %s' % (k + 1, h) for k, h in enumerate(st['how'])), st['mine'],
            '\n'.join('(%s) %s' % (lab, e) for e, lab in st['eqs']) or '-', st['output'], st['notes'], st['question']]
    for j, v in enumerate(vals): cell(ws, 5 + i, 1 + j, v, BF if j < 2 else NF, border=True, al=Alignment(wrap_text=True, vertical='top'))
    ws.row_dimensions[5 + i].height = 230
ws.freeze_panes = 'C5'

# ---------------- 0c metrics explained ----------------
ws = wb[SX]; title(ws, 'Accuracy measures explained', 'Formula, the Excel formula used in this workbook, how to read the value and the reference. The same measures are computed live in 3_Detection, 4_Grade, 5_Score and 12_Metrics_calculator.')
header(ws, 4, 1, ['Measure', 'Task', 'Formula', 'Excel formula', 'How to read it', 'Reference'], [30, 10, 44, 40, 50, 26], 30)
for i, mm in enumerate(METRICS):
    for j, v in enumerate(mm): cell(ws, 5 + i, 1 + j, v, BF if j == 0 else (Font(name='Courier New', size=9) if j == 3 else NF), border=True, al=Alignment(wrap_text=True, vertical='top'), text=True)
    ws.row_dimensions[5 + i].height = 32
r = 5 + len(METRICS) + 1
cell(ws, r, 1, 'Terms: TP = diseased predicted diseased; TN = healthy predicted healthy; FP = healthy predicted diseased; FN = diseased predicted healthy; P = precision = TP/(TP+FP); R = recall.', NOTEF)

# ---------------- 0d interpretation ----------------
ws = wb[SI]; title(ws, 'Results and their interpretation (the same text as Chapter 3 of the Word report)', 'For each result: what is shown, how to read it, the result, the interpretation and the link to the literature; the last column names the sheet with the data.')
header(ws, 4, 1, ['Result', 'Part', 'Text', 'Data in sheet'], [22, 22, 130, 22], 28)
SHEET_OF = {'spectra': S9, 'domain': S8 + ', ' + S10, 'detection': S3, 'grades': S4, 'score': S5, 'allmodels': S7, 'indomain': S6, 'summary': S2}
NAME_OF = {'spectra': '3.1 Leaf and canopy spectra', 'domain': '3.2 Domain check', 'detection': '3.3 Detection', 'grades': '3.4 Six grades', 'score': '3.5 Severity score', 'allmodels': '3.6 All 30 models', 'indomain': '3.7 In-domain check', 'summary': '3.8 Summary'}
r = 5
for key, parts in INTERP.items():
    for lead, txt in parts:
        txt = txt.replace('[[F:', 'Figure ').replace('[[T:', 'Table ').replace(']]', '')
        for j, v in enumerate([NAME_OF.get(key, key), lead.rstrip('.'), txt, SHEET_OF.get(key, '')]): cell(ws, r, 1 + j, v, BF if j < 2 else NF, border=True, al=Alignment(wrap_text=True, vertical='top'))
        ws.row_dimensions[r].height = 15 * (1 + len(txt) // 120); r += 1
ws.freeze_panes = 'A5'

# ---------------- 12 metrics calculator ----------------
ws = wb[SCALC]; title(ws, 'Metrics calculator: paste true and predicted values of any data set (yellow cells) and read all measures', 'Example values = the UAV-trained models of this study (6_UAV_trained). Replace or extend the yellow columns (up to 500 rows); leave unused rows empty. Detection: 0 = healthy, 1 = diseased; grades: 0, 1, 3, 5, 7, 9; score: 0-9.')
NR = 500; R1c, R2c = 6, 5 + NR
header(ws, 5, 1, ['Sample id', 'True status (0/1)', 'Predicted status (0/1)', 'Disease score / probability', 'True grade', 'Predicted grade', 'True score', 'Predicted score', 'AUC helper', 'Grade steps (helper)'], [10, 11, 11, 13, 9, 10, 9, 10, 10, 10], 42)
pA, pB, pC = PU[PU.task == 'A'].sort_values('plot'), PU[PU.task == 'B'].sort_values('plot'), PU[PU.task == 'C'].sort_values('plot')
for i in range(NP):
    rr = R1c + i
    for j, v in enumerate(['P%d' % (i + 1), int(pA.y.values[i]), int(pA.pred.values[i]), round(float(pA.score.values[i]), 4), int(pB.y.values[i]), int(pB.pred.values[i]), round(float(pC.y.values[i]), 4), round(float(pC.pred.values[i]), 4)]):
        cell(ws, rr, 1 + j, v, INF if j else NF, YF, border=True)
for i in range(NP, NR):
    for j in range(8): cell(ws, R1c + i, 1 + j, None, fill=YF, border=True)
rg = lambda col: '$%s$%d:$%s$%d' % (col, R1c, col, R2c)
for i in range(NR):
    rr = R1c + i
    ws.cell(rr, 9, '=IF(AND(B%d=1,D%d<>""),COUNTIFS(%s,0,%s,"<"&D%d)+0.5*COUNTIFS(%s,0,%s,D%d),"")' % (rr, rr, rg('B'), rg('D'), rr, rg('B'), rg('D'), rr)).font = NOTEF
    ws.cell(rr, 10, '=IF(OR(E%d="",F%d=""),"",ABS(MATCH(F%d,{0,1,3,5,7,9},0)-MATCH(E%d,{0,1,3,5,7,9},0)))' % (rr, rr, rr, rr)).font = NOTEF
c0 = 12; cell(ws, 5, c0, 'Measure', HF, HFILL, border=True); cell(ws, 5, c0 + 1, 'Value', HF, HFILL, border=True); ws.column_dimensions[CL(c0)].width = 34; ws.column_dimensions[CL(c0 + 1)].width = 11
B_, C_, D_, E_, F_, G_, H_, I_, J_ = (rg(x) for x in 'BCDEFGHIJ')
calc = [('A  Detection', None, None),
        ('Samples (n)', '=COUNT(%s)' % B_, '0'), ('TP (diseased -> diseased)', '=COUNTIFS(%s,1,%s,1)' % (B_, C_), '0'), ('TN (healthy -> healthy)', '=COUNTIFS(%s,0,%s,0)' % (B_, C_), '0'),
        ('FP (healthy -> diseased)', '=COUNTIFS(%s,0,%s,1)' % (B_, C_), '0'), ('FN (diseased -> healthy)', '=COUNTIFS(%s,1,%s,0)' % (B_, C_), '0'),
        ('Overall accuracy', '=(M8+M9)/M7', '0.000'), ('Sensitivity', '=M8/(M8+M11)', '0.000'), ('Specificity', '=M9/(M9+M10)', '0.000'), ('Balanced accuracy', '=(M13+M14)/2', '0.000'),
        ('F1 diseased', '=2*M8/(2*M8+M10+M11)', '0.000'), ('F1 healthy', '=2*M9/(2*M9+M10+M11)', '0.000'), ('Macro-F1', '=(M16+M17)/2', '0.000'),
        ('AUC (rank formula; needs scores)', '=IF(COUNT(%s)=0,"-",SUM(%s)/(COUNTIF(%s,1)*COUNTIF(%s,0)))' % (D_, I_, B_, B_), '0.000'),
        ('B  Six grades', None, None),
        ('Samples (n)', '=COUNT(%s)' % F_, '0'), ('Overall accuracy', '=SUMPRODUCT((%s<>"")*(%s=%s))/M21' % (E_, E_, F_), '0.000'), ('Within one grade', '=COUNTIF(%s,"<=1")/COUNT(%s)' % (J_, J_), '0.000'),
        ('Macro-F1 (grades present)', '=AVERAGE(Q8:Q13)', '0.000'), ('Quadratic weighted kappa', '=1-SUMPRODUCT(W8:AB13,P17:U22)/SUMPRODUCT(W8:AB13,W17:AB22)', '0.000'),
        ('C  Score', None, None),
        ('Samples (n)', '=COUNT(%s)' % H_, '0'), ('R²', '=1-SUMXMY2(%s,%s)/DEVSQ(%s)' % (H_, G_, G_), '0.000'), ('RMSE', '=SQRT(SUMXMY2(%s,%s)/M27)' % (H_, G_), '0.000'),
        ('MAE', '=SUMPRODUCT((%s<>"")*ABS(%s-%s))/M27' % (G_, H_, G_), '0.000'), ('Bias', '=AVERAGE(%s)-AVERAGE(%s)' % (H_, G_), '0.000'), ('Pearson r', '=CORREL(%s,%s)' % (H_, G_), '0.000'),
        ('RPD', '=STDEV(%s)/M29' % G_, '0.00')]
for i, (lab, f, fmt) in enumerate(calc):
    rr = 6 + i
    if f is None: cell(ws, rr, c0, lab, SF); continue
    cell(ws, rr, c0, lab, BF, LFILL, border=True); cell(ws, rr, c0 + 1, f, BF, fmt=fmt, border=True)
# grade table for macro-F1 (columns O-R) and QWK matrices
cell(ws, 6, 15, 'Per grade (for macro-F1)', SF)
header(ws, 7, 15, ['Grade', 'F1', 'True n', 'Pred n'], [8, 9, 8, 8])
for i, g in enumerate(GR):
    rr = 8 + i; cell(ws, rr, 15, g, BF, border=True)
    cell(ws, rr, 17, '=IF(COUNTIF(%s,%d)+COUNTIF(%s,%d)=0,"",2*COUNTIFS(%s,%d,%s,%d)/(COUNTIF(%s,%d)+COUNTIF(%s,%d)))' % (E_, g, F_, g, E_, g, F_, g, E_, g, F_, g), fmt='0.000', border=True)
    cell(ws, rr, 18, '=COUNTIF(%s,%d)' % (E_, g), fmt='0', border=True); cell(ws, rr, 19, '=COUNTIF(%s,%d)' % (F_, g), fmt='0', border=True)
cell(ws, 6, 23, 'QWK weights w = (i - j)² / 25', SF); cell(ws, 15, 15, 'Observed counts O (rows = true, columns = predicted)', SF); cell(ws, 15, 23, 'Expected counts E = row total x column total / n', SF)
for i, g in enumerate(GR):
    cell(ws, 7, 23 + i, 'P%d' % g, BF, LFILL, border=True); cell(ws, 8 + i, 22, 'T%d' % g, BF, LFILL, border=True)
    cell(ws, 16, 16 + i, 'P%d' % g, BF, LFILL, border=True); cell(ws, 17 + i, 15, 'T%d' % g, BF, LFILL, border=True)
    cell(ws, 16, 23 + i, 'P%d' % g, BF, LFILL, border=True); cell(ws, 17 + i, 22, 'T%d' % g, BF, LFILL, border=True)
    for j, h in enumerate(GR):
        cell(ws, 8 + i, 23 + j, (i - j) ** 2 / 25, fmt='0.00', border=True)
        cell(ws, 17 + i, 16 + j, '=COUNTIFS(%s,%d,%s,%d)' % (E_, g, F_, h), fmt='0', border=True, fill=YF if i == j else None)
        cell(ws, 17 + i, 23 + j, '=SUM($P$%d:$U$%d)*SUM(%s$17:%s$22)/SUM($P$17:$U$22)' % (17 + i, 17 + i, CL(16 + j), CL(16 + j)), fmt='0.00', border=True)
for c_ in range(22, 29): ws.column_dimensions[CL(c_)].width = 7
for c_ in range(16, 22): ws.column_dimensions[CL(c_)].width = max(ws.column_dimensions[CL(c_)].width or 0, 7)
cell(ws, 25, 15, 'Check: with the example values the results equal the UAV-trained scores in 6_UAV_trained (QWK uses the six grade positions 0, 1, 3, 5, 7, 9 as in the Python code).', NOTEF)
ws.freeze_panes = 'A6'

# ---------------- 13 report tables and 14 report figures ----------------
ws = wb[SRT]; title(ws, 'All tables of the Word report (same numbering)', 'Every table of the report and slides, in the order of the report. The live-formula versions of the main tables are in sheets 1-12.')
r = 4
for T_ in TABS:
    cell(ws, r, 1, 'Table %d. %s' % (T_['number'], T_['caption']), SF, al=Alignment(wrap_text=False)); r += 1
    rows_ = T_['rows']
    for j, h in enumerate(rows_[0]): cell(ws, r, 1 + j, h, HF, HFILL, border=True, al=Alignment(wrap_text=True, vertical='center'))
    ws.row_dimensions[r].height = 30; r += 1
    for row_ in rows_[1:]:
        for j, v in enumerate(row_):
            try: vv = float(v) if (v.replace('.', '', 1).replace('-', '', 1).isdigit() and len(v) < 12) else v
            except Exception: vv = v
            cell(ws, r, 1 + j, vv, border=True, al=Alignment(wrap_text=True, vertical='top'), text=True)
        ws.row_dimensions[r].height = 15 * max(1, max(len(str(v)) // 45 + 1 for v in row_)); r += 1
    r += 2
for c_ in range(1, 15): ws.column_dimensions[CL(c_)].width = 18
ws.column_dimensions['A'].width = 26
from openpyxl.drawing.image import Image as XLImage
from PIL import Image as PILImage
ws = wb[SRF]; title(ws, 'All figures of the Word report (same numbering)', 'Static images at 300 dpi; native Excel charts of the same data are in sheets 2, 5, 8, 9 and 10.')
r = 4
for f_ in FIGJ:
    cell(ws, r, 1, 'Figure %d. %s' % (f_['number'], f_['caption']), SF); r += 1
    im = XLImage(HERE + '/fig/' + f_['file']); w0, h0 = PILImage.open(HERE + '/fig/' + f_['file']).size; scale = 900 / w0; im.width, im.height = int(w0 * scale), int(h0 * scale)
    ws.add_image(im, 'A%d' % r); r += int(im.height / 20) + 3

# ---------------- 15 glossary ----------------
ws = wb[SGL]; title(ws, 'Glossary')
header(ws, 4, 1, ['Term', 'Meaning'], [30, 120])
for i, (k_, v_) in enumerate(GLOSSARY): cell(ws, 5 + i, 1, k_, BF, border=True); cell(ws, 5 + i, 2, v_, border=True, al=Alignment(wrap_text=True))

# ---------------- 0 contents ----------------
ws = ws0
cell(ws, 1, 1, 'Applying the best ASD leaf models to the UAV hyperspectral image of 24 Feb 2026 (white rust, IARI 2025-26)', TF)
cell(ws, 2, 1, 'Frozen 2025-26 ASD models (leaf level) applied to the 48 UAV plot mean spectra; accuracy checked against the ASD leaf scores of the same day.', NOTEF)
info = [('UAV data', '48 plot mean spectra (ENVI ROI means), Headwall co-aligned VNIR-SWIR, %d bands 399-2398 nm, flight of 24 Feb 2026.' % SU['n_bands']),
        ('Ground truth', 'Same-day ASD leaf scores (L3, L5, LL; 0-9 key): healthy (12 sprayed) vs diseased (36 unsprayed) plots; plot mean score; nearest grade (1_Ground_truth).'),
        ('Models', 'Best model per task from the ASD leave-one-replication-out test (overall, best ML, best DL), trained on all %d leaves (outputs/ASD_2025-26_models).' % SU['asd_models_trained_on']),
        ('Pre-processing', 'Exactly as for the leaves: resampled to 1 nm (gaps bridged linearly), Savitzky-Golay 11/2, first derivative, 5-nm bands, indices, NDSI/RSI/WRI.'),
        ('Input variants', '1 Direct; 2 healthy-reference corrected (wavelength-wise gain mapping the healthy UAV plots onto the healthy ASD leaves of 24 Feb; a healthy plot never corrects itself); 3 = 2 + brightness normalisation (same mean reflectance, shape only).'),
        ('In-domain check', 'Best ML model type refitted on the UAV plots with the same LORO folds (6_UAV_trained), features inside UAV band gaps removed.')]
for i, (k, v) in enumerate(info):
    cell(ws, 4 + i, 1, k, BF, al=Alignment(vertical='top')); cell(ws, 4 + i, 2, v, al=Alignment(wrap_text=True, vertical='top')); ws.merge_cells(start_row=4 + i, start_column=2, end_row=4 + i, end_column=10); ws.row_dimensions[4 + i].height = 30
r = 11; cell(ws, r, 1, 'Key results (links to 2_Best_models)', SF)
header(ws, r + 1, 1, ['Task', 'Best overall model', 'Metric', 'ASD leaves', 'UAV direct', 'UAV corrected', 'UAV normalised', 'UAV-trained (best ML type)'], None, 32)
for k, t in enumerate('ABC'):
    rr_ = r + 2 + k; src = 5 + 3 * k
    cell(ws, rr_, 1, TN[t], BF, border=True); cell(ws, rr_, 2, "=%s!C%d" % (q(S2), src), border=True); cell(ws, rr_, 3, "=%s!D%d" % (q(S2), src), border=True)
    for j, col in enumerate('EFGH'): cell(ws, rr_, 4 + j, "=%s!%s%d" % (q(S2), col, src), fmt='0.000', border=True)
    cell(ws, rr_, 8, "=%s!I%d" % (q(S2), src + 1), fmt='0.000', border=True, fill=GFILL)
F = json.load(open(O + 'findings.json')) if os.path.exists(O + 'findings.json') else []
r = 17; cell(ws, r, 1, 'Main findings', SF)
for i, t_ in enumerate(F):
    cell(ws, r + 1 + i, 1, t_, al=Alignment(wrap_text=True, vertical='top')); ws.merge_cells(start_row=r + 1 + i, start_column=1, end_row=r + 1 + i, end_column=10); ws.row_dimensions[r + 1 + i].height = 15 * (1 + len(t_) // 150)
r = r + len(F) + 2; cell(ws, r, 1, 'Sheets', SF)
guide = [(SG, 'START HERE: step-by-step guide, how to repeat on another data set, commands'), (SM, 'methodology in detail (one row per step, with references)'), (SX, 'every accuracy measure explained (formula, Excel formula, reading, reference)'), (SI, 'every result with its interpretation'), (S1, 'plot status, mean leaf score, nearest grade, PDI of 24 Feb'), (S2, 'best models: ASD vs UAV accuracy (+ chart)'), (S3, 'detection predictions, live metrics, confusion matrices'),
         (S4, 'grade predictions, live metrics, confusion matrices'), (S5, 'score predictions, live R²/RMSE/bias/r, scatter charts'), (S6, 'best ML type refitted on the UAV plots (in-domain check)'),
         (S7, 'all 30 models x 3 variants'), (S8, 'feature values outside the ASD training range'), (S9, 'ASD vs UAV mean spectra (charts)'), (S10, 'PCA domain plot (chart)'),
         (S11, 'every prediction (long table)'), (SCALC, 'metrics calculator for any data set (paste true and predicted values)'), (SRT, 'all tables of the Word report'), (SRF, 'all figures of the Word report'), (SGL, 'glossary'), (S12, 'references')]
for i, (k, v) in enumerate(guide):
    x = cell(ws, r + 1 + i, 1, k, Font(name=AR, size=10, color='0563C1', underline='single')); x.hyperlink = "#'%s'!A1" % k; cell(ws, r + 1 + i, 2, v)
ws.column_dimensions['A'].width = 30
for c_ in 'BCDEFGHIJ': ws.column_dimensions[c_].width = 16
for w in wb.worksheets: w.sheet_view.zoomScale = 90
os.makedirs(os.path.dirname(OUT), exist_ok=True); wb.save(OUT); print('saved', OUT)
