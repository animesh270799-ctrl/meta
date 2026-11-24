"""Excel workbook of the plot-level disease maps: field maps drawn with formulas and colour scales, accuracy and Moran's I with formulas,
guide, methods, interpretations, every report table and figure."""
import os, json, numpy as np, pandas as pd
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as CL
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, FormulaRule
from openpyxl.drawing.image import Image as XLImage
from PIL import Image as PILImage
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'; O = HERE + 'out/'; T = HERE + '../uavt/out/'
OUT = HERE + '../outputs/UAV_24Feb2026_disease_maps.xlsx'
TB = pd.read_csv(O + 'map_table.csv'); MO = pd.read_csv(O + 'moran.csv'); MS = json.load(open(O + 'map_summary.json')); NB = pd.read_csv(O + 'neighbours.csv', index_col=0)
TABS = json.load(open(O + 'tables.json')); FIGJ = json.load(open(O + 'figures.json')); STEPS = json.load(open(O + 'methods.json')); INTERP = json.load(open(O + 'interpretations.json')); FIND = json.load(open(O + 'findings.json'))
REFS = json.load(open(O + 'refs_used.json')); best, bv = MS['best'], MS['best_variant']
VSH = {'Direct': 'direct', 'Healthy-reference corrected': 'corrected', 'Corrected + brightness-normalised': 'normalised'}; tg = {t: VSH[bv[t]] for t in 'ABC'}; NP = len(TB)
AR = 'Arial'; TF = Font(name=AR, bold=True, size=14, color='1F3864'); SF = Font(name=AR, bold=True, size=11, color='1F3864'); HF = Font(name=AR, bold=True, color='FFFFFF', size=10)
HFILL = PatternFill('solid', fgColor='1F3864'); NF = Font(name=AR, size=10); BF = Font(name=AR, size=10, bold=True); NOTEF = Font(name=AR, size=9, italic=True, color='555555')
LFILL = PatternFill('solid', fgColor='F2F2F2'); BLUE = PatternFill('solid', fgColor='EAF1FB'); thin = Side(style='thin', color='BFBFBF'); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
def cell(ws, r, c, v=None, font=NF, fill=None, fmt=None, al=None, border=False, text=False):
    x = ws.cell(r, c, v); x.font = font
    if text and isinstance(v, str) and v.startswith('='): x.data_type = 's'
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
def title(ws, t, sub=None, how=None, ncol=14, h=60):
    cell(ws, 1, 1, t, TF)
    if sub: cell(ws, 2, 1, sub, NOTEF)
    if how: cell(ws, 3, 1, 'HOW TO READ: ' + how, Font(name=AR, size=10, color='1F3864'), BLUE, al=Alignment(wrap_text=True, vertical='top')); ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=ncol); ws.row_dimensions[3].height = h
itext = lambda key: ' '.join('%s %s' % (l, t) for l, t in INTERP.get(key, [])).replace('[[F:', 'Figure ').replace('[[T:', 'Table ').replace(']]', '')
q = lambda sh: "'%s'" % sh
wb = Workbook(); ws0 = wb.active; ws0.title = '0_Contents'
NAMES = ['0a_Guide', '0b_Methods', '0c_Interpretation', '1_Plot_table', '2_Field_maps', '3_Accuracy', '4_Neighbours_Moran', '5_Group_summary', '6_R_Tables', '7_R_Figures', '8_Glossary', '9_References']
for n in NAMES: wb.create_sheet(n)

# ---------------- 1 plot table (errors as formulas)
ws = wb['1_Plot_table']; S1 = '1_Plot_table'
title(ws, 'Plot table: ground truth, predictions and errors (24 Feb 2026)', 'Yellow columns = values from the analysis (truth from the ASD leaf scores; predictions from the transfer test); grey columns = live formulas.',
      'Each row is one plot. Outcome = TP/TN/FP/FN; grade steps = position(predicted grade) - position(true grade) on 0, 1, 3, 5, 7, 9; error = predicted - true score. Paste the predictions of another model into the yellow columns and every map, accuracy and Moran\'s I updates.', 20, 48)
cols = [('Plot', 'plot', None), ('Block', 'block', None), ('Status', 'status', None), ('Sowing', 'sowing', None), ('Variety', 'variety', None), ('True A (0/1)', 'A', '0'), ('True grade', 'grade', '0'), ('True score', 'score', '0.00'),
        ('ASD status (%s)' % tg['A'], 'A_%s' % tg['A'], '0'), ('ASD disease score', 'A_%s_score' % tg['A'], '0.000'), ('ASD grade (%s)' % tg['B'], 'B_%s' % tg['B'], '0'), ('ASD score (%s)' % tg['C'], 'C_%s' % tg['C'], '0.00'),
        ('UAV status', 'A_uav', '0'), ('UAV disease score', 'A_uav_score', '0.000'), ('UAV grade', 'B_uav', '0'), ('UAV score', 'C_uav', '0.00')]
FORM = [('ASD outcome', lambda r: '=IF(AND(F{0}=1,I{0}=1),"TP",IF(AND(F{0}=0,I{0}=0),"TN",IF(AND(F{0}=0,I{0}=1),"FP","FN")))'.format(r)),
        ('ASD grade steps', lambda r: '=MATCH(K{0},{{0,1,3,5,7,9}},0)-MATCH(G{0},{{0,1,3,5,7,9}},0)'.format(r)), ('ASD score error', lambda r: '=L{0}-H{0}'.format(r)),
        ('UAV outcome', lambda r: '=IF(AND(F{0}=1,M{0}=1),"TP",IF(AND(F{0}=0,M{0}=0),"TN",IF(AND(F{0}=0,M{0}=1),"FP","FN")))'.format(r)),
        ('UAV grade steps', lambda r: '=MATCH(O{0},{{0,1,3,5,7,9}},0)-MATCH(G{0},{{0,1,3,5,7,9}},0)'.format(r)), ('UAV score error', lambda r: '=P{0}-H{0}'.format(r))]
header(ws, 4, 1, [c[0] for c in cols] + [f[0] for f in FORM], [6, 8, 9, 7, 7, 8, 8, 8, 11, 11, 11, 11, 9, 11, 9, 9, 10, 10, 10, 10, 10, 10], 42)
YF = PatternFill('solid', fgColor='FFF2CC')
for i, r in TB.iterrows():
    rr = 5 + i
    for j, (_, k, fmt) in enumerate(cols):
        v = r[k]; v = (int(v) if fmt == '0' else round(float(v), 4)) if fmt else v
        cell(ws, rr, 1 + j, v, fill=YF if j >= 5 else None, fmt=fmt, border=True)
    for j, (_, f) in enumerate(FORM): cell(ws, rr, len(cols) + 1 + j, f(rr), fill=LFILL, fmt='0.00' if 'error' in FORM[j][0] else None, border=True)
R1, R2 = 5, 4 + NP
ws.freeze_panes = 'B5'
COL = {lab: CL(1 + j) for j, (lab, _, _) in enumerate(cols)}; COL.update({f[0]: CL(len(cols) + 1 + j) for j, f in enumerate(FORM)})
rng = lambda lab: "%s!$%s$%d:$%s$%d" % (q(S1), COL[lab], R1, COL[lab], R2)

# ---------------- 2 field maps (formulas + colour scales)
ws = wb['2_Field_maps']; S2 = '2_Field_maps'
title(ws, 'Field maps drawn in Excel (schematic plot arrangement, not to scale)', 'Every map cell looks up its plot in 1_Plot_table (INDEX/MATCH); colours come from conditional formatting with the same scales as the report figures.',
      'Top block = plot numbers. Each map has the four rows and the columns of the field: Healthy block | gap | R3 | R2 | R1. Score maps: yellow (0) to red (9); errors: blue (under) - white (0) - red (over); outcomes: TN green, TP red, FP orange, FN blue.', 18, 52)
ncol_h = 3; blocks = [('C', 'Healthy'), ('R3', 'R3'), ('R2', 'R2'), ('R1', 'R1')]
pos = {}
for p in range(1, NP + 1):
    r = TB[TB['plot'] == p].iloc[0]; bi = [b for b, _ in blocks].index(r.block)
    cols_in_block = sorted(TB[TB.block == r.block]['col'].unique()); ci = cols_in_block.index(r['col'])
    pos[p] = (int(r['row']), bi * (ncol_h + 1) + ci)
def mapblock(r0, ttl, lab, kind, fmt='0.0'):
    cell(ws, r0, 1, ttl, SF)
    for bi, (_, bname) in enumerate(blocks): cell(ws, r0 + 1, 2 + bi * (ncol_h + 1), bname, BF)
    cells = []
    for p, (rw, cc) in pos.items():
        rr, c_ = r0 + 2 + rw, 2 + cc
        if lab == 'plot': cell(ws, rr, c_, p, BF, border=True, al=Alignment(horizontal='center'))
        else:
            cell(ws, rr, c_, '=INDEX(%s,MATCH(%d,%s,0))' % (rng(lab), p, rng('Plot')), BF, fmt=None if kind == 'cat' else fmt, border=True, al=Alignment(horizontal='center'))
        cells.append('%s%d' % (CL(c_), rr))
    area = '%s%d:%s%d' % (CL(2), r0 + 2, CL(2 + 4 * (ncol_h + 1) - 2), r0 + 5)
    if kind == 'score': ws.conditional_formatting.add(area, ColorScaleRule(start_type='num', start_value=0, start_color='FFFFCC', mid_type='num', mid_value=4.5, mid_color='FD8D3C', end_type='num', end_value=9, end_color='800026'))
    elif kind == 'err': ws.conditional_formatting.add(area, ColorScaleRule(start_type='num', start_value=-4, start_color='2166AC', mid_type='num', mid_value=0, mid_color='FFFFFF', end_type='num', end_value=4, end_color='B2182B'))
    elif kind == 'grade': ws.conditional_formatting.add(area, ColorScaleRule(start_type='num', start_value=0, start_color='1A9850', mid_type='num', mid_value=4, mid_color='FDAE61', end_type='num', end_value=9, end_color='7F0000'))
    elif kind == 'prob': ws.conditional_formatting.add(area, ColorScaleRule(start_type='min', start_color='1A9850', mid_type='percentile', mid_value=50, mid_color='FFFFBF', end_type='max', end_color='D73027'))
    elif kind == 'status': ws.conditional_formatting.add(area, ColorScaleRule(start_type='num', start_value=0, start_color='1A9850', end_type='num', end_value=1, end_color='D73027'))
    elif kind == 'cat':
        for val, col in (('TN', '1A9850'), ('TP', 'D73027'), ('FP', 'FDAE61'), ('FN', '4575B4')):
            ws.conditional_formatting.add(area, CellIsRule(operator='equal', formula=['"%s"' % val], fill=PatternFill('solid', fgColor=col)))
    return r0 + 8
r = 5
for ttl, lab, kind, fmt in [('Plot numbers', 'plot', None, None), ('True status (0 healthy, 1 diseased)', 'True A (0/1)', 'status', '0'), ('True plot mean score (0-9)', 'True score', 'score', '0.0'), ('True grade', 'True grade', 'grade', '0'),
                            ('Best ASD model: predicted status (%s, %s input)' % (best['A']['overall'], tg['A']), 'ASD status (%s)' % tg['A'], 'status', '0'), ('Best ASD model: detection outcome', 'ASD outcome', 'cat', None),
                            ('Best ASD model: disease score', 'ASD disease score', 'prob', '0.00'), ('Best ASD model: predicted grade (%s, %s input)' % (best['B']['overall'], tg['B']), 'ASD grade (%s)' % tg['B'], 'grade', '0'),
                            ('Best ASD model: predicted score (%s, %s input)' % (best['C']['overall'], tg['C']), 'ASD score (%s)' % tg['C'], 'score', '0.0'), ('Best ASD model: score error (predicted - true)', 'ASD score error', 'err', '+0.0;-0.0;0.0'),
                            ('UAV-trained: predicted status', 'UAV status', 'status', '0'), ('UAV-trained: detection outcome', 'UAV outcome', 'cat', None), ('UAV-trained: disease score', 'UAV disease score', 'prob', '0.00'),
                            ('UAV-trained: predicted grade', 'UAV grade', 'grade', '0'), ('UAV-trained: predicted score', 'UAV score', 'score', '0.0'), ('UAV-trained: score error', 'UAV score error', 'err', '+0.0;-0.0;0.0')]:
    r = mapblock(r, ttl, lab, kind, fmt)
for c_ in range(2, 2 + 4 * (ncol_h + 1)): ws.column_dimensions[CL(c_)].width = 7
ws.column_dimensions['A'].width = 3

# ---------------- 3 accuracy (formulas)
ws = wb['3_Accuracy']
title(ws, 'Map accuracy (live formulas from 1_Plot_table)', 'Standard map accuracy assessment: confusion counts, overall accuracy, producer\'s accuracy (sensitivity) and specificity; grade agreement; score R² and RMSE (Congalton, 1991; Olofsson et al., 2014).',
      'Column C = best ASD maps, column D = UAV-trained maps. Producer\'s accuracy of the diseased class = share of truly diseased plots shown as diseased.', 8, 40)
header(ws, 4, 2, ['Measure', 'Best ASD maps', 'UAV-trained maps'], [34, 16, 16], 28)
def acc(lab_out, lab_steps, lab_pred, lab_err):
    o, st, pr, er, tr = rng(lab_out), rng(lab_steps), rng(lab_pred), rng(lab_err), rng('True score')
    return [('TP', '=COUNTIF(%s,"TP")' % o, '0'), ('TN', '=COUNTIF(%s,"TN")' % o, '0'), ('FP', '=COUNTIF(%s,"FP")' % o, '0'), ('FN', '=COUNTIF(%s,"FN")' % o, '0'),
            ('Overall accuracy', '=(COUNTIF(%s,"TP")+COUNTIF(%s,"TN"))/COUNTA(%s)' % (o, o, o), '0.000'), ('Producer\'s accuracy, diseased (sensitivity)', '=COUNTIF(%s,"TP")/(COUNTIF(%s,"TP")+COUNTIF(%s,"FN"))' % (o, o, o), '0.000'),
            ('Specificity (healthy recognised)', '=COUNTIF(%s,"TN")/(COUNTIF(%s,"TN")+COUNTIF(%s,"FP"))' % (o, o, o), '0.000'), ('User\'s accuracy, diseased (precision)', '=IF(COUNTIF(%s,"TP")+COUNTIF(%s,"FP")=0,"-",COUNTIF(%s,"TP")/(COUNTIF(%s,"TP")+COUNTIF(%s,"FP")))' % (o, o, o, o, o), '0.000'),
            ('Grade: exact', '=COUNTIF(%s,0)/COUNT(%s)' % (st, st), '0.000'), ('Grade: within one grade', '=(COUNTIF(%s,0)+COUNTIF(%s,1)+COUNTIF(%s,-1))/COUNT(%s)' % (st, st, st, st), '0.000'),
            ('Score: R²', '=1-SUMSQ(%s)/DEVSQ(%s)' % (er, tr), '0.000'), ('Score: RMSE', '=SQRT(SUMSQ(%s)/COUNT(%s))' % (er, er), '0.000'), ('Score: mean error (bias)', '=AVERAGE(%s)' % er, '0.000'),
            ('Score: min / max predicted', '=TEXT(MIN(%s),"0.0")&" / "&TEXT(MAX(%s),"0.0")' % (pr, pr), None)]
A1_ = acc('ASD outcome', 'ASD grade steps', 'ASD score (%s)' % tg['C'], 'ASD score error'); A2_ = acc('UAV outcome', 'UAV grade steps', 'UAV score', 'UAV score error')
for i, ((lab, f1, fmt), (_, f2_, _)) in enumerate(zip(A1_, A2_)):
    cell(ws, 5 + i, 2, lab, BF, LFILL, border=True); cell(ws, 5 + i, 3, f1, fmt=fmt, border=True); cell(ws, 5 + i, 4, f2_, fmt=fmt, border=True)

# ---------------- 4 neighbours and Moran's I (formulas)
ws = wb['4_Neighbours_Moran']
title(ws, 'Rook neighbour matrix and Moran\'s I computed with formulas', 'w(i,j) = 1 if plots i and j share a side within the same block; Moran\'s I = (n/S0) Σ w z_i z_j / Σ z² (Moran, 1950); the permutation p-values come from Python (999 permutations; Cliff and Ord, 1981).',
      'Left: Moran\'s I for three variables (true score, best ASD score error, UAV-trained score error) computed from the columns z (deviation from the mean) and lag (sum of neighbour z). Right: the 48 x 48 neighbour matrix.', 14, 48)
header(ws, 5, 1, ['Plot', 'True score', 'ASD error', 'UAV error', 'z true', 'z ASD', 'z UAV', 'lag true', 'lag ASD', 'lag UAV'], [6, 9, 9, 9, 9, 9, 9, 9, 9, 9], 30)
W0c = 13; cell(ws, 4, W0c, 'Neighbour matrix W (rows and columns = plots 1-48)', SF)
for j in range(NP): cell(ws, 5, W0c + 1 + j, j + 1, BF, LFILL, al=Alignment(horizontal='center')); ws.column_dimensions[CL(W0c + 1 + j)].width = 3.2
ZR = 56                                                     # z values laid out as rows (transposed) for the lag formulas
cell(ws, ZR - 1, W0c, 'z as rows (transposed; used by the lag formulas)', NOTEF)
for i in range(NP):
    rr = 6 + i; p = i + 1
    cell(ws, rr, 1, p, BF)
    for k, lab in enumerate(['True score', 'ASD score error', 'UAV score error']):
        cell(ws, rr, 2 + k, '=INDEX(%s,MATCH(%d,%s,0))' % (rng(lab), p, rng('Plot')), fmt='0.00')
        cell(ws, rr, 5 + k, '=%s%d-AVERAGE($%s$6:$%s$%d)' % (CL(2 + k), rr, CL(2 + k), CL(2 + k), 5 + NP), fmt='0.00')
        cell(ws, rr, 8 + k, '=SUMPRODUCT($%s%d:$%s%d,$%s$%d:$%s$%d)' % (CL(W0c + 1), rr, CL(W0c + NP), rr, CL(W0c + 1), ZR + k, CL(W0c + NP), ZR + k), fmt='0.00')
    cell(ws, rr, W0c, p, BF, LFILL)
    for j in range(NP): cell(ws, rr, W0c + 1 + j, int(NB.iloc[i, j]), fill=PatternFill('solid', fgColor='C6EFCE') if NB.iloc[i, j] else None)
for k in range(3):
    cell(ws, ZR + k, W0c, ['z true', 'z ASD', 'z UAV'][k], BF)
    for j in range(NP): cell(ws, ZR + k, W0c + 1 + j, '=INDEX($%s$6:$%s$%d,%d)' % (CL(5 + k), CL(5 + k), 5 + NP, j + 1), fmt='0.0')
r0 = 6 + NP + 1
header(ws, r0, 1, ['Variable', '', 'Moran\'s I (Excel)', 'E(I)', 'Moran\'s I (Python)', 'p (Python, 999 perm.)'], None, 30)
S0 = '(SUM($%s$6:$%s$%d))' % (CL(W0c + 1), CL(W0c + NP), 5 + NP)
for k, (lab, tag, var) in enumerate([('True plot mean score', 'truth', 'True plot mean score'), ('Best ASD score error', tg['C'], 'C residual'), ('UAV-trained score error', 'uav', 'C residual')]):
    rr = r0 + 1 + k; zc, lc = CL(5 + k), CL(8 + k)
    cell(ws, rr, 1, lab, BF); ws.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=2)
    cell(ws, rr, 3, '=%d/%s*SUMPRODUCT($%s$6:$%s$%d,$%s$6:$%s$%d)/SUMSQ($%s$6:$%s$%d)' % (NP, S0, zc, zc, 5 + NP, lc, lc, 5 + NP, zc, zc, 5 + NP), BF, fmt='0.000', border=True)
    cell(ws, rr, 4, '=-1/(%d-1)' % NP, fmt='0.000', border=True)
    mr = MO[(MO.tag == tag) & (MO.variable.str.startswith(var))].iloc[0]
    cell(ws, rr, 5, round(float(mr.moran_I), 4), fmt='0.000', border=True); cell(ws, rr, 6, round(float(mr.p_value), 4), fmt='0.000', border=True)

# ---------------- 5 group summary (formulas)
ws = wb['5_Group_summary']
title(ws, 'Map accuracy and errors by block, sowing date and variety (AVERAGEIFS / COUNTIFS formulas)', 'Groups of 9-12 plots: only large differences are meaningful (Olofsson et al., 2014).',
      'Mean error > 0 = the map over-predicts the group; < 0 = under-predicts. Detection accuracy = share of plots with outcome TP or TN.', 10, 36)
header(ws, 4, 1, ['Grouping', 'Group', 'Plots', 'Mean true score', 'ASD mean predicted score', 'ASD mean error', 'ASD detection accuracy', 'UAV mean predicted score', 'UAV mean error', 'UAV detection accuracy'], [11, 9, 7, 11, 12, 11, 12, 12, 11, 12], 42)
r = 5
for gname, lab, groups in (('Block', 'Block', ['C', 'R1', 'R2', 'R3']), ('Sowing date', 'Sowing', ['D1', 'D2', 'D3', 'D4']), ('Variety', 'Variety', ['V1', 'V2', 'V3'])):
    for g in groups:
        G = rng(lab); cell(ws, r, 1, gname, BF); cell(ws, r, 2, g, BF)
        f = ['=COUNTIF(%s,B%d)' % (G, r), '=AVERAGEIFS(%s,%s,B%d)' % (rng('True score'), G, r), '=AVERAGEIFS(%s,%s,B%d)' % (rng('ASD score (%s)' % tg['C']), G, r), '=AVERAGEIFS(%s,%s,B%d)' % (rng('ASD score error'), G, r),
             '=(COUNTIFS(%s,B%d,%s,"TP")+COUNTIFS(%s,B%d,%s,"TN"))/C%d' % (G, r, rng('ASD outcome'), G, r, rng('ASD outcome'), r),
             '=AVERAGEIFS(%s,%s,B%d)' % (rng('UAV score'), G, r), '=AVERAGEIFS(%s,%s,B%d)' % (rng('UAV score error'), G, r), '=(COUNTIFS(%s,B%d,%s,"TP")+COUNTIFS(%s,B%d,%s,"TN"))/C%d' % (G, r, rng('UAV outcome'), G, r, rng('UAV outcome'), r)]
        for j, ff in enumerate(f): cell(ws, r, 3 + j, ff, fmt='0' if j == 0 else ('+0.00;-0.00;0.00' if j in (3, 6) else '0.00'), border=True)
        r += 1
    r += 1

# ---------------- 0a guide, 0b methods, 0c interpretation
ws = wb['0a_Guide']
title(ws, 'Step-by-step guide: how the maps were made and how to make them for another image or model', 'Read this first. Steps D1-D7 are explained in detail in 0b_Methods and Chapter 2 of the Word report.')
header(ws, 4, 1, ['Step', 'What', 'How (in short)', 'Sheet / file', 'Reference'], [6, 32, 70, 28, 32], 28)
G = [('D1', 'Collect predictions and truth', 'Per-plot predictions of the best ASD models (transfer test) and of the UAV-trained models; truth = ASD leaf scores of the same day', '1_Plot_table', 'Congalton (1991)'),
     ('D2', 'Place the plots', 'Plot arrangement of the experiment; rook neighbours within blocks; for GIS: join the plot table to the plot polygons (field "plot no.")', '2_Field_maps, 4_Neighbours_Moran', 'Aasen et al. (2018)'),
     ('D3', 'Colour the maps', 'Fixed sequential scale for scores (0-9), class colours for status/grade/outcome, diverging scale for errors', '2_Field_maps', 'Harrower and Brewer (2003)'),
     ('D4', 'Assess accuracy', 'Confusion counts, overall/producer\'s/user\'s accuracy, specificity, grade agreement, score R² and RMSE', '3_Accuracy', 'Congalton (1991); Olofsson et al. (2014)'),
     ('D5', 'Test spatial pattern', 'Moran\'s I of the errors with the neighbour matrix; permutation test', '4_Neighbours_Moran', 'Moran (1950); Cliff and Ord (1981)'),
     ('D6', 'Summarise by group', 'Mean error and accuracy by block, sowing date, variety', '5_Group_summary', 'Olofsson et al. (2014)'),
     ('D7', 'Pixel maps (next)', 'Crop-masked pixels of the cube -> same features -> UAV-trained model -> raster -> summary per plot', 'needs ENVI .dat/.hdr', 'Zarco-Tejada et al. (2018)')]
for i, g in enumerate(G):
    for j, v in enumerate(g): cell(ws, 5 + i, 1 + j, v, BF if j == 0 else NF, border=True, al=Alignment(wrap_text=True, vertical='top'))
    ws.row_dimensions[5 + i].height = 32
r = 5 + len(G) + 1; cell(ws, r, 1, 'To map another model or image', SF)
for i, t in enumerate(['1. Put the plot predictions (status 0/1, disease score, grade, score) in the yellow columns of 1_Plot_table (same plot order).', '2. All maps (2_Field_maps), accuracy (3_Accuracy), Moran\'s I (4_Neighbours_Moran) and group summaries (5_Group_summary) update automatically.',
                       '3. For a different field layout, edit the plot positions (Python: m1_maps.py reads acm/layout.json) and rebuild with: python3 m1_maps.py && python3 m2_word.py && node m2_build.js && python3 m3_excel.py && python3 m4_pptdata.py && node m4_ppt.js.',
                       '4. For a georeferenced map, export 1_Plot_table as CSV and join it to the plot polygons in ArcMap/QGIS by plot number; use the same colour classes.']):
    cell(ws, r + 1 + i, 1, t); ws.merge_cells(start_row=r + 1 + i, start_column=1, end_row=r + 1 + i, end_column=5)
ws = wb['0b_Methods']
title(ws, 'Methodology in detail (same text as Chapter 2 of the Word report)')
mc = ['Step', 'Title', 'Position', 'Concept', 'Why', 'What the papers did', 'How it is done', 'Applied to these data', 'Equations', 'Output', 'Notes', 'Likely question']
header(ws, 4, 1, mc, [6, 22, 22, 40, 40, 40, 60, 40, 34, 28, 36, 34], 30)
for i, st in enumerate(STEPS):
    vals = [st['no'], st['title'], st['position'], st['concept'], st['why'], st['papers'], '\n'.join('%d. %s' % (k + 1, h) for k, h in enumerate(st['how'])), st['mine'], '\n'.join('(%s) %s' % (lab, e) for e, lab in st['eqs']) or '-', st['output'], st['notes'], st['question']]
    for j, v in enumerate(vals): cell(ws, 5 + i, 1 + j, v, BF if j < 2 else NF, border=True, al=Alignment(wrap_text=True, vertical='top'))
    ws.row_dimensions[5 + i].height = 200
ws = wb['0c_Interpretation']
title(ws, 'Maps and their interpretation (same text as Chapter 3 of the Word report)')
header(ws, 4, 1, ['Map', 'Part', 'Text'], [16, 18, 140], 28); r = 5
for key, parts in INTERP.items():
    for lead, txt in parts:
        txt = txt.replace('[[F:', 'Figure ').replace('[[T:', 'Table ').replace(']]', '')
        for j, v in enumerate([key, lead.rstrip('.'), txt]): cell(ws, r, 1 + j, v, BF if j < 2 else NF, border=True, al=Alignment(wrap_text=True, vertical='top'))
        ws.row_dimensions[r].height = 15 * (1 + len(txt) // 130); r += 1

# ---------------- 6 report tables, 7 report figures, 8 glossary, 9 references
ws = wb['6_R_Tables']; title(ws, 'Every table of the Word report (same numbering)'); r = 4
for T_ in TABS:
    cell(ws, r, 1, 'Table %d. %s' % (T_['number'], T_['caption']), SF); r += 1
    for j, h in enumerate(T_['rows'][0]): cell(ws, r, 1 + j, h, HF, HFILL, border=True, al=Alignment(wrap_text=True))
    ws.row_dimensions[r].height = 30; r += 1
    for row_ in T_['rows'][1:]:
        for j, v in enumerate(row_): cell(ws, r, 1 + j, v, border=True, al=Alignment(wrap_text=True, vertical='top'), text=True)
        ws.row_dimensions[r].height = 15 * max(1, max(len(str(v)) // 40 + 1 for v in row_)); r += 1
    r += 2
for c_ in range(1, 16): ws.column_dimensions[CL(c_)].width = 18
ws = wb['7_R_Figures']; title(ws, 'Every figure (map) of the Word report (same numbering)'); r = 4
for f_ in FIGJ:
    cell(ws, r, 1, 'Figure %d. %s' % (f_['number'], f_['caption']), SF); r += 1
    im = XLImage(HERE + 'fig/' + f_['file']); w0, h0 = PILImage.open(HERE + 'fig/' + f_['file']).size; s = 1000 / w0; im.width, im.height = int(w0 * s), int(h0 * s); ws.add_image(im, 'A%d' % r); r += int(im.height / 20) + 3
ws = wb['8_Glossary']; title(ws, 'Glossary')
GL = [('Disease map', 'Map of predicted disease status, grade or severity per mapping unit (here: plot).'), ('TP, TN, FP, FN', 'True positive (diseased mapped diseased), true negative, false positive (false alarm), false negative (missed disease).'),
      ('Producer\'s accuracy', 'Share of truly diseased plots shown as diseased (= sensitivity).'), ('User\'s accuracy', 'Share of plots mapped diseased that are truly diseased (= precision).'),
      ('Rook neighbours', 'Plots that share a side (left, right, above, below) within the same block.'), ('Moran\'s I', 'Index of spatial autocorrelation; > E(I) = neighbouring plots are similar (clustered), ≈ E(I) = random.'),
      ('Permutation p-value', 'Share of 999 random rearrangements of the values among plots with Moran\'s I at least as large as observed.'), ('Out-of-fold prediction', 'Prediction of a plot by a model trained without that plot (leave-one-replication-out).'),
      ('Schematic map', 'Plots drawn in their row/column positions, not to scale; adjacency is exact.')]
header(ws, 4, 1, ['Term', 'Meaning'], [26, 120])
for i, (k_, v_) in enumerate(GL): cell(ws, 5 + i, 1, k_, BF, border=True); cell(ws, 5 + i, 2, v_, border=True, al=Alignment(wrap_text=True))
ws = wb['9_References']; title(ws, 'References')
for i, t_ in enumerate(REFS): cell(ws, 3 + i, 1, t_, al=Alignment(wrap_text=True, vertical='top')); ws.row_dimensions[3 + i].height = 30
ws.column_dimensions['A'].width = 150

# ---------------- 0 contents
ws = ws0
cell(ws, 1, 1, 'White rust disease maps from the UAV hyperspectral image of 24 Feb 2026 (best ASD models and UAV-trained check)', TF)
cell(ws, 2, 1, 'Plot-level maps (48 plots; schematic field arrangement); predictions from the transfer test; truth = ASD leaf scores of the same day. Pixel maps need the image cube.', NOTEF)
cell(ws, 4, 1, 'Main findings', SF)
for i, f in enumerate(FIND): cell(ws, 5 + i, 1, '%d. %s' % (i + 1, f), al=Alignment(wrap_text=True, vertical='top')); ws.merge_cells(start_row=5 + i, start_column=1, end_row=5 + i, end_column=10); ws.row_dimensions[5 + i].height = 15 * (1 + len(f) // 140)
r = 6 + len(FIND); cell(ws, r, 1, 'Sheets', SF)
GUIDE = [('0a_Guide', 'START HERE: step-by-step guide and how to map another model or image'), ('0b_Methods', 'methodology in detail with references'), ('0c_Interpretation', 'every map with its interpretation'),
         ('1_Plot_table', 'truth, predictions and errors per plot (errors = formulas)'), ('2_Field_maps', 'all maps drawn in Excel (formulas + colour scales)'), ('3_Accuracy', 'map accuracy (formulas)'),
         ('4_Neighbours_Moran', 'neighbour matrix and Moran\'s I (formulas)'), ('5_Group_summary', 'errors by block, sowing date, variety (formulas)'), ('6_R_Tables', 'every table of the report'), ('7_R_Figures', 'every map/figure of the report'),
         ('8_Glossary', 'terms'), ('9_References', 'references')]
for i, (k_, v_) in enumerate(GUIDE):
    x = cell(ws, r + 1 + i, 1, k_, Font(name=AR, size=10, color='0563C1', underline='single')); x.hyperlink = "#'%s'!A1" % k_; cell(ws, r + 1 + i, 3, v_)
ws.column_dimensions['A'].width = 24; ws.column_dimensions['B'].width = 2
for c_ in 'CDEFGHIJ': ws.column_dimensions[c_].width = 16
for w in wb.worksheets: w.sheet_view.zoomScale = 90
os.makedirs(os.path.dirname(OUT), exist_ok=True); wb.save(OUT); print('saved', OUT)
