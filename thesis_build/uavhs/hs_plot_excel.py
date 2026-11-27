"""UAV hyperspectral plot spectra (ENVI ROI means, 48 plots, 483 bands) -> Excel workbook with formulas and native charts.
Plot spectra, healthy vs diseased, by variety, by growth stage (sowing date), by treatment (mean of R1-R3 vs the matching
healthy plot) and by disease severity (plot PDI from the ASD leaf scores of the selected image date).
usage: python3 hs_plot_excel.py [envi_txt] [out.xlsx]"""
import sys, os, numpy as np, pandas as pd
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as CL
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.chart import ScatterChart, BarChart, Reference, Series
from openpyxl.chart.series import SeriesLabel, StrRef
from openpyxl.chart.title import Title
from openpyxl.chart.text import Text, RichText
from openpyxl.chart.axis import ChartLines
from openpyxl.chart.marker import Marker
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.drawing.text import Paragraph, ParagraphProperties, CharacterProperties, RegularTextRun, Font as DFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'data', 'envi_plot_avg.txt')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '..', 'outputs', 'UAV_hyperspectral_plot_spectra_2025-26.xlsx')
META = os.path.join(HERE, '..', 'asd26', 'data', 'meta.csv')
DEFAULT_DATE = '2026-02-24'

# ---------------- data ----------------
L = open(SRC).read().splitlines()
ncol = sum(l.startswith('Column') for l in L)
A = np.array([[float(x) for x in l.split()] for l in L[ncol + 1:] if l.strip()])
WL, R = A[:, 0], A[:, 1:]
NP = R.shape[1]; assert NP == 48, NP
gaps = set(int(i) + 1 for i in np.where(np.diff(WL) > 8)[0])       # band index that starts a new segment
M = pd.read_csv(META, parse_dates=['date'])
P = M.groupby('plot')[['block', 'variety', 'timing', 'sowing']].first()
DATES = sorted(M.date.unique())
STAGE = M.groupby(['plot', 'date']).stage.agg(lambda s: s.mode().iloc[0]).unstack()
SOWD = {'D1': '9 Dec 2025', 'D2': '18 Dec 2025', 'D3': '27 Dec 2025', 'D4': '9 Jan 2026'}
SOWG = {'D1': '50 DAS', 'D2': '40 DAS', 'D3': '30 DAS', 'D4': '20 DAS'}
status = lambda p: 'Healthy' if P.loc[p, 'block'] == 'C' else 'Diseased'
D0 = pd.Timestamp(DEFAULT_DATE)
_d = M[M.date == D0]
PDI0 = _d.groupby('plot').score.apply(lambda x: x.sum() / (9 * len(x)) * 100).round(6)
STG0 = STAGE[D0]
SOWT = {k: pd.Timestamp(v) for k, v in {'D1': '2025-12-09', 'D2': '2025-12-18', 'D3': '2025-12-27', 'D4': '2026-01-09'}.items()}
DAS0 = {k: (D0 - v).days for k, v in SOWT.items()}
trt = lambda p: '%s-%s' % (P.loc[p, 'variety'], P.loc[p, 'timing'])

# ---------------- styles ----------------
AR = 'Arial'
TF = Font(name=AR, bold=True, size=14, color='1F3864'); SF = Font(name=AR, bold=True, size=11, color='1F3864')
HF = Font(name=AR, bold=True, color='FFFFFF', size=10); HFILL = PatternFill('solid', fgColor='1F3864')
NF = Font(name=AR, size=10); BF = Font(name=AR, size=10, bold=True); NOTEF = Font(name=AR, size=9, italic=True, color='555555')
INF = Font(name=AR, size=10, color='0000FF', bold=True); YEL = PatternFill('solid', fgColor='FFFF00')
GFILL = PatternFill('solid', fgColor='E2EFDA'); RFILL = PatternFill('solid', fgColor='FCE4D6'); LFILL = PatternFill('solid', fgColor='F2F2F2')
thin = Side(style='thin', color='BFBFBF'); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
CH, CD = '1A9850', 'D73027'
CV = {'V1': '2166AC', 'V2': '762A83', 'V3': 'E08214'}
CS = {'D1': '1B9E77', 'D2': '7570B3', 'D3': 'D95F02', 'D4': 'E6AB02'}
CQ = {'Healthy': CH, 'Q1': 'FEB24C', 'Q2': 'FD8D3C', 'Q3': 'E31A1C', 'Q4': '800026'}
CC = {0: CH, 1: 'FED976', 3: 'FEB24C', 5: 'FD8D3C', 7: 'E31A1C', 9: '800026'}

def grad(n, stops=('1A9850', 'A6D96A', 'FEE08B', 'F46D43', 'A50026', '67001F')):
    st = [np.array([int(s[i:i + 2], 16) for i in (0, 2, 4)]) for s in stops]; out = []
    for k in range(n):
        t = k / max(n - 1, 1) * (len(st) - 1); i = min(int(t), len(st) - 2); f = t - i
        c = st[i] * (1 - f) + st[i + 1] * f; out.append('%02X%02X%02X' % tuple(int(round(v)) for v in c))
    return out

def cell(ws, r, c, v=None, font=NF, fill=None, fmt=None, al=None, border=False):
    x = ws.cell(r, c, v); x.font = font
    if fill: x.fill = fill
    if fmt: x.number_format = fmt
    if al: x.alignment = al
    if border: x.border = BOX
    return x

def header(ws, r, c, labels, widths=None):
    for j, t in enumerate(labels):
        cell(ws, r, c + j, t, HF, HFILL, al=Alignment(horizontal='center', vertical='center', wrap_text=True), border=True)
    if widths:
        for j, w in enumerate(widths): ws.column_dimensions[CL(c + j)].width = w

def title(ws, t, sub=None):
    cell(ws, 1, 1, t, TF)
    if sub: cell(ws, 2, 1, sub, NOTEF)

# ---------------- chart helpers ----------------
def _cp(size, bold=False, color='404040'):
    return CharacterProperties(sz=int(size * 100), b=bold, solidFill=color, latin=DFont(typeface=AR))
def rich(size, bold=False, color='404040'):
    return RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=_cp(size, bold, color)), endParaRPr=_cp(size, bold, color))])
def mtitle(t, size=11, color='1F3864'):
    cp = _cp(size, True, color)
    return Title(tx=Text(rich=RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=cp), r=[RegularTextRun(rPr=cp, t=t)])])), overlay=False)

def scatter(t, w=16, h=8.5, ytitle='Reflectance', ymin=None, ymax=None, yfmt='0.00', legend='b', tsize=11, xmin=400, xmax=2400):
    ch = ScatterChart(); ch.title = mtitle(t, tsize); ch.style = 2; ch.roundedCorners = False
    ch.width, ch.height = w, h; ch.display_blanks = 'gap'
    ch.x_axis.title = mtitle('Wavelength (nm)', 9, '404040'); ch.y_axis.title = mtitle(ytitle, 9, '404040')
    ch.x_axis.scaling.min, ch.x_axis.scaling.max, ch.x_axis.majorUnit = xmin, xmax, 200
    ch.x_axis.number_format = '0'; ch.y_axis.number_format = yfmt
    ch.x_axis.delete = False; ch.y_axis.delete = False; ch.x_axis.tickLblPos = 'low'
    ch.x_axis.txPr = rich(8); ch.y_axis.txPr = rich(8)
    ch.x_axis.majorGridlines = None
    ch.y_axis.majorGridlines = ChartLines(spPr=GraphicalProperties(ln=LineProperties(solidFill='E3E3E3', w=6350)))
    if ymin is not None: ch.y_axis.scaling.min = ymin
    if ymax is not None: ch.y_axis.scaling.max = ymax
    if legend: ch.legend.position = legend; ch.legend.overlay = False; ch.legend.txPr = rich(8)
    else: ch.legend = None
    return ch

def line(ch, ws, col, r1, r2, xws, name=None, ref=None, color='000000', w=1.75, dash=None):
    s = Series(Reference(ws, min_col=col, min_row=r1, max_row=r2), Reference(xws, min_col=1, min_row=r1, max_row=r2))
    if ref: s.tx = SeriesLabel(strRef=StrRef(ref))
    elif name: s.tx = SeriesLabel(v=name)
    s.marker = Marker(symbol='none'); s.smooth = False
    s.spPr = GraphicalProperties(ln=LineProperties(solidFill=color, w=int(w * 12700), prstDash=dash))
    ch.series.append(s); return s

def zero_line(ch, ws, col, r1, r2, name='0 % (= healthy)'):     # horizontal reference at 0 (column of zeros)
    line(ch, ws, col, r1, r2, ws, name=name, color='7F7F7F', w=0.75, dash='dash')

def place(ws, ch, anchor): ws.add_chart(ch, anchor)

from openpyxl.drawing.spreadsheet_drawing import OneCellAnchor, AnchorMarker
from openpyxl.drawing.xdr import XDRPositiveSize2D
from openpyxl.utils.units import cm_to_EMU
def _wcm(ws, c):
    d = ws.column_dimensions.get(CL(c)); w = d.width if (d is not None and d.customWidth and d.width) else 8.43
    return int(w * 7 + 5) * 2.54 / 96
def colx(ws, col): return sum(_wcm(ws, c) for c in range(1, col))
def place_at(ws, ch, row, x_cm):
    """anchor a chart at an exact horizontal position (cm from the sheet's left edge), independent of column widths"""
    c, left = 1, 0.0
    while left + _wcm(ws, c) <= x_cm: left += _wcm(ws, c); c += 1
    ch.anchor = OneCellAnchor(_from=AnchorMarker(col=c - 1, colOff=cm_to_EMU(x_cm - left), row=row - 1, rowOff=0),
                              ext=XDRPositiveSize2D(cm_to_EMU(ch.width), cm_to_EMU(ch.height)))
    ws.add_chart(ch)


def q(sh): return "'%s'" % sh

wb = Workbook()
S_CON, S_INFO, S_SPEC, S_PCH = '0_Contents', '1_Plot_info', '2_Spectra', '3_Plot_charts'
S_HD, S_VAR, S_STG, S_CST, S_TRT, S_TSV = '4_Healthy_vs_Diseased', '5_By_variety', '6_By_growth_stage', '6b_By_crop_stage', '7_By_treatment', '8_Treatments_by_severity'
S_SEV, S_SRT, S_PSV, S_REG, S_LEAF, S_REF = '9_Severity_groups', '10_Sorted_spectra', '11_Plots_by_severity', '12_Region_means', '13_Leaf_scores', '14_References'
ws0 = wb.active; ws0.title = S_CON
for n in (S_INFO, S_SPEC, S_PCH, S_HD, S_VAR, S_STG, S_CST, S_TRT, S_TSV, S_SEV, S_SRT, S_PSV, S_REG, S_LEAF, S_REF): wb.create_sheet(n)
DATE_CELL = "%s!$C$6" % q(S_CON)

# ---------------- 13 Leaf scores ----------------
ws = wb[S_LEAF]; title(ws, 'ASD leaf scores used for plot severity (2025-26, natural infection)',
                     'One row per scored leaf (L3, L5, LL; the 9 L4 leaves of 11 Feb are excluded). Score = 0-9 white rust key (Conn et al., 1990). Source: ASD field records of the same plots.')
header(ws, 3, 1, ['Date', 'Plot', 'Leaf position', 'Score (0-9)', 'Growth stage', 'Status'], [13, 7, 12, 11, 15, 11])
Ms = M.sort_values(['date', 'plot', 'leaf']).reset_index(drop=True)
LR1, LR2 = 4, 3 + len(Ms)
for i, r in Ms.iterrows():
    k = LR1 + i
    cell(ws, k, 1, r.date.to_pydatetime(), fmt='dd-mmm-yyyy'); cell(ws, k, 2, int(r['plot'])); cell(ws, k, 3, r['leaf'])
    cell(ws, k, 4, int(r['score'])); cell(ws, k, 5, r['stage']); cell(ws, k, 6, status(int(r['plot'])))
ws.freeze_panes = 'A4'
LS = lambda col: "%s!$%s$%d:$%s$%d" % (q(S_LEAF), col, LR1, col, LR2)

# ---------------- 1 Plot info ----------------
ws = wb[S_INFO]; title(ws, 'Plot information, treatment and disease severity',
                     'Image date = 0_Contents!C6 (24 Feb 2026); columns S-X use it. PDI = sum of leaf scores / (9 x number of leaves) x 100 (Wheeler, 1969), from 13_Leaf_scores; the other ASD dates are kept for reference.')
cols = ['Plot', 'ENVI ROI', 'Block', 'Status', 'Variety', 'Sowing (growth stage)', 'Sowing date', 'Treatment', 'DAS on image date'] + \
       ['PDI (%%) %s' % pd.Timestamp(d).strftime('%d %b') for d in DATES] + ['Stage %s' % pd.Timestamp(d).strftime('%d %b') for d in DATES] + \
       ['Leaves scored on image date', 'PDI on image date (%)', 'Severity class (0-9)', 'Severity rank (1 = lowest)', 'Severity group', 'Growth stage on image date', 'Chart label']
header(ws, 4, 1, cols, [6, 8, 8, 10, 8, 12, 12, 10, 10] + [10] * 4 + [13] * 4 + [10, 11, 10, 11, 11, 15, 40])
ws.row_dimensions[4].height = 45
for j, d in enumerate(DATES):
    cell(ws, 3, 10 + j, pd.Timestamp(d).to_pydatetime(), BF, fmt='dd-mmm-yyyy'); cell(ws, 3, 14 + j, pd.Timestamp(d).to_pydatetime(), BF, fmt='dd-mmm-yyyy')
cell(ws, 3, 9, 'dates →', NOTEF)
for p in range(1, NP + 1):
    r = 4 + p; hfill = GFILL if status(p) == 'Healthy' else None
    vals = [p, 'ROI #%d' % p, P.loc[p, 'block'], status(p), P.loc[p, 'variety'], P.loc[p, 'timing'], pd.Timestamp(P.loc[p, 'sowing']).to_pydatetime(), trt(p)]
    for j, v in enumerate(vals): cell(ws, r, 1 + j, v, fill=hfill, fmt='dd-mmm-yyyy' if j == 6 else None, border=True)
    cell(ws, r, 9, '=%s-G%d' % (DATE_CELL, r), fmt='0', border=True)
    for j in range(4):
        c = CL(10 + j)
        cell(ws, r, 10 + j, '=IFERROR(AVERAGEIFS(%s,%s,$A%d,%s,%s$3)/9*100,NA())' % (LS('D'), LS('B'), r, LS('A'), c), fmt='0.0', border=True)
        cell(ws, r, 14 + j, STAGE.loc[p, DATES[j]], border=True)
    cell(ws, r, 18, '=COUNTIFS(%s,$A%d,%s,%s)' % (LS('B'), r, LS('A'), DATE_CELL), fmt='0', border=True)
    cell(ws, r, 19, '=ROUND(INDEX($J%d:$M%d,MATCH(%s,$J$3:$M$3,0)),6)' % (r, r, DATE_CELL), BF, fmt='0.0', border=True)
    cell(ws, r, 20, '=IF(S%d=0,0,IF(S%d<=5,1,IF(S%d<=10,3,IF(S%d<=25,5,IF(S%d<=50,7,9)))))' % ((r,) * 5), fmt='0', border=True)
    cell(ws, r, 21, '=RANK(S%d,$S$5:$S$52,1)+COUNTIF($S$4:S%d,S%d)' % (r, r - 1, r), fmt='0', border=True)
    cell(ws, r, 22, '=IF(D%d="Healthy","Healthy","Q"&ROUNDUP((COUNTIFS($D$5:$D$52,"Diseased",$U$5:$U$52,"<"&U%d)+1)/9,0))' % (r, r), border=True)
    cell(ws, r, 23, '=INDEX($N%d:$Q%d,MATCH(%s,$N$3:$Q$3,0))' % (r, r, DATE_CELL), border=True)
    cell(ws, r, 24, '="P"&A%d&" "&H%d&" "&C%d&" | PDI "&TEXT(S%d,"0.0")&"%% | class "&T%d' % (r, r, r, r, r), border=True)
ws.freeze_panes = 'B5'
cell(ws, 54, 1, 'Severity class from plot PDI: 0 = 0 %; 1 = >0-5 %; 3 = >5-10 %; 5 = >10-25 %; 7 = >25-50 %; 9 = >50 % (0-9 disease-index classes of the methodology).', NOTEF)
cell(ws, 55, 1, 'Severity group: diseased plots ranked by PDI on the image date and split into four equal groups of 9 plots (Q1 = least, Q4 = most severe). Ties are broken by plot number.', NOTEF)
cell(ws, 56, 1, 'Growth stage = sowing date treatment D1-D4 (sown 9 Dec, 18 Dec, 27 Dec 2025, 9 Jan 2026 = the 50, 40, 30, 20 DAS groups); recorded phenological stage on each date in columns N-Q.', NOTEF)

INFO = lambda col, p: "%s!$%s$%d" % (q(S_INFO), col, 4 + p)

# ---------------- 2 Spectra ----------------
ws = wb[S_SPEC]; title(ws, 'Plot mean reflectance spectra (UAV hyperspectral, ENVI ROI means)',
                     'Source: %s (ENVI ASCII plot file, flight of %s, 48 ROIs, %d bands, %.0f-%.0f nm). Rows 3-13 = plot attributes; row 14 = series name. Blank rows = bands removed in processing.' % (os.path.basename(SRC), D0.strftime('%d %b %Y'), len(WL), WL[0], WL[-1]))
lab = ['Plot', 'Status', 'Block', 'Variety', 'Sowing (growth stage)', 'Treatment', 'PDI on image date (%)', 'Severity class', 'Severity group', 'Severity rank', 'Crop stage on image date']
for i, t in enumerate(lab): cell(ws, 3 + i, 1, t, BF, LFILL, border=True)
SPR = {k: 3 + i for i, k in enumerate(['plot', 'status', 'block', 'var', 'sow', 'trt', 'pdi', 'cls', 'grp', 'rank', 'stage'])}; SPR['name'] = 14
for p in range(1, NP + 1):
    c = 1 + p; fill = GFILL if status(p) == 'Healthy' else RFILL
    for k, v in [('plot', p), ('status', status(p)), ('block', P.loc[p, 'block']), ('var', P.loc[p, 'variety']), ('sow', P.loc[p, 'timing']), ('trt', trt(p))]:
        cell(ws, SPR[k], c, v, BF if k == 'plot' else NF, fill, border=True, al=Alignment(horizontal='center'))
    for k, col, fmt in [('pdi', 'S', '0.0'), ('cls', 'T', '0'), ('grp', 'V', None), ('rank', 'U', '0')]:
        cell(ws, SPR[k], c, '=' + INFO(col, p), NF, fill, fmt=fmt, border=True, al=Alignment(horizontal='center'))
    cell(ws, SPR['stage'], c, '=' + INFO('W', p), NF, fill, border=True, al=Alignment(horizontal='center'))
    cell(ws, SPR['name'], c, 'P%d %s %s' % (p, trt(p), 'H' if status(p) == 'Healthy' else P.loc[p, 'block']), HF, HFILL, border=True, al=Alignment(horizontal='center'))
cell(ws, 14, 1, 'Wavelength (nm)', HF, HFILL, border=True)
R0 = 15; rows = []; r = R0
for i in range(len(WL)):
    if i in gaps: r += 1
    rows.append(r); r += 1
RL = rows[-1]                                   # last data row
for i, rr in enumerate(rows):
    cell(ws, rr, 1, round(float(WL[i]), 3), BF, fmt='0.0')
    for p in range(NP): cell(ws, rr, 2 + p, round(float(R[i, p]), 6), fmt='0.0000')
ws.conditional_formatting.add('B%d:AW%d' % (R0, RL), CellIsRule(operator='lessThan', formula=['0'], font=Font(name=AR, color='FF0000', bold=True)))
ws.column_dimensions['A'].width = 24
for p in range(NP): ws.column_dimensions[CL(2 + p)].width = 9.5
ws.freeze_panes = 'B15'
WSS = ws
SP = lambda col, rr: "%s!%s%d" % (q(S_SPEC), col, rr)
SPC = lambda p: CL(1 + p)                       # column letter of plot p in the Spectra sheet
HCOL = (2, 13); DCOL = (14, 49)

# mean-based normalisation helper: each derived sheet gets rows aligned with the Spectra sheet (same row numbers)
def wl_col(ws, off=0):
    cell(ws, 14 + off, 1, 'Wavelength (nm)', HF, HFILL, border=True)
    for i, rr in enumerate(rows): cell(ws, rr + off, 1, round(float(WL[i]), 3), BF, fmt='0.0')
    ws.column_dimensions['A'].width = 16

def pct(ws, rr, cd, ch):           # % difference formula, only where healthy reflectance > 0.005
    return '=IF(%s%d>0.005,(%s%d-%s%d)/%s%d*100,NA())' % (ch, rr, cd, rr, ch, rr, ch, rr)

# ---------------- 3 Plot charts ----------------
ws = wb[S_PCH]; title(ws, 'Reflectance spectrum of every plot (plot-number order)',
                     'Green = healthy (fungicide-sprayed) plots 1-12; red = diseased (unsprayed, natural infection) plots 13-48. Same y-axis (0-0.40) in every chart. For the severity order see 11_Plots_by_severity.')
ch = scatter('All 48 plots: healthy (green) vs diseased (red)', 33, 11, ymin=0, ymax=0.4, legend=None)
for p in range(1, NP + 1): line(ch, WSS, 1 + p, R0, RL, WSS, ref="%s!$%s$%d" % (q(S_SPEC), SPC(p), SPR['name']), color=CH if p <= 12 else CD, w=1.0)
place(ws, ch, 'A4')
for p in range(1, NP + 1):
    k = p - 1; rr = 27 + (k // 4) * 17
    st = status(p); blk = 'Healthy' if st == 'Healthy' else P.loc[p, 'block']
    ch = scatter('Plot %d: %s, %s-%s | PDI %.1f %% | %s' % (p, blk, P.loc[p, 'variety'], P.loc[p, 'timing'], PDI0[p], STG0[p].lower()), 15, 8.2, ymin=0, ymax=0.4, legend=None, tsize=10)
    line(ch, WSS, 1 + p, R0, RL, WSS, name='Plot %d' % p, color=CH if st == 'Healthy' else CD, w=1.75)
    place_at(ws, ch, rr, (k % 4) * 15.3)

# ---------------- 4 Healthy vs diseased ----------------
ws = wb[S_HD]; title(ws, 'Healthy vs diseased: mean spectra of all plots',
                    'Healthy = mean of the 12 sprayed plots; diseased = mean of the 36 unsprayed plots (3 replications x 12 treatments). % difference = (diseased - healthy) / healthy x 100.')
wl_col(ws)
header(ws, 14, 2, ['Healthy mean', 'Healthy SD', 'Diseased mean', 'Diseased SD', 'Difference (D - H)', '% difference', 'Healthy mean + SD', 'Healthy mean - SD', 'Diseased mean + SD',
                   'Diseased mean - SD', 'Healthy (shape)', 'Diseased (shape)', 'zero'], [11] * 13)
hb, he, db, de = SPC(1), SPC(12), SPC(13), SPC(48)
for rr in rows:
    S = lambda a, b: "%s!%s%d:%s%d" % (q(S_SPEC), a, rr, b, rr)
    cell(ws, rr, 2, '=AVERAGE(%s)' % S(hb, he), fmt='0.0000'); cell(ws, rr, 3, '=STDEV(%s)' % S(hb, he), fmt='0.0000')
    cell(ws, rr, 4, '=AVERAGE(%s)' % S(db, de), fmt='0.0000'); cell(ws, rr, 5, '=STDEV(%s)' % S(db, de), fmt='0.0000')
    cell(ws, rr, 6, '=D%d-B%d' % (rr, rr), fmt='0.0000'); cell(ws, rr, 7, pct(ws, rr, 'D', 'B'), fmt='0.0')
    cell(ws, rr, 8, '=B%d+C%d' % (rr, rr), fmt='0.0000'); cell(ws, rr, 9, '=B%d-C%d' % (rr, rr), fmt='0.0000')
    cell(ws, rr, 10, '=D%d+E%d' % (rr, rr), fmt='0.0000'); cell(ws, rr, 11, '=D%d-E%d' % (rr, rr), fmt='0.0000')
    cell(ws, rr, 12, '=B%d/AVERAGE($B$%d:$B$%d)' % (rr, R0, RL), fmt='0.000'); cell(ws, rr, 13, '=D%d/AVERAGE($D$%d:$D$%d)' % (rr, R0, RL), fmt='0.000')
    cell(ws, rr, 14, 0, fmt='0')
cell(ws, 4, 1, 'Image date', BF); cell(ws, 4, 2, '=' + DATE_CELL, INF, fmt='dd-mmm-yyyy')
cell(ws, 5, 1, 'Healthy plots (n)', BF); cell(ws, 5, 2, 12); cell(ws, 6, 1, 'Diseased plots (n)', BF); cell(ws, 6, 2, 36)
cell(ws, 7, 1, 'Mean PDI of diseased plots (%)', BF); cell(ws, 7, 2, "=AVERAGE(%s!N%d:AW%d)" % (q(S_SPEC), SPR['pdi'], SPR['pdi']), fmt='0.0')
cell(ws, 8, 1, 'Shape = mean spectrum divided by its own mean reflectance over all bands (removes overall brightness, keeps the spectral shape).', NOTEF)
cell(ws, 9, 1, 'Band-region statistics (means, % difference, Welch t-test, correlation with PDI): sheet 12_Region_means.', NOTEF)
ch = scatter('Mean reflectance: healthy vs diseased (dashed = mean ± SD)', 24, 11)
line(ch, ws, 2, R0, RL, ws, name='Healthy (12 plots)', color=CH, w=2.25); line(ch, ws, 4, R0, RL, ws, name='Diseased (36 plots)', color=CD, w=2.25)
for c, col in ((8, CH), (9, CH), (10, CD), (11, CD)): line(ch, ws, c, R0, RL, ws, name=['Healthy + SD', 'Healthy - SD', 'Diseased + SD', 'Diseased - SD'][c - 8], color=col, w=0.75, dash='dash')
place(ws, ch, 'P4')
ch = scatter('% difference of diseased from healthy', 24, 9, ytitle='% difference', yfmt='0')
line(ch, ws, 7, R0, RL, ws, name='(Diseased - Healthy) / Healthy x 100', color=CD, w=2); zero_line(ch, ws, 14, R0, RL)
place(ws, ch, 'P27')
ch = scatter('Spectral shape (brightness removed): healthy vs diseased', 24, 9, ytitle='Relative reflectance', yfmt='0.0')
line(ch, ws, 12, R0, RL, ws, name='Healthy (shape)', color=CH, w=2.25); line(ch, ws, 13, R0, RL, ws, name='Diseased (shape)', color=CD, w=2.25)
place(ws, ch, 'P46')
ws.freeze_panes = 'B15'

# ---------------- 5 By variety / 6 By growth stage (group means with criteria in rows 12-13) ----------------
def group_sheet(sh, ttl, sub, groups, crit_row, colors, glabel, extra):
    ws = wb[sh]; title(ws, ttl, sub); wl_col(ws)
    G = len(groups); c0 = 2
    for g, gv in enumerate(groups):
        for k, stt in enumerate(('Healthy', 'Diseased')):
            c = c0 + 2 * g + k; cell(ws, 12, c, stt, NOTEF); cell(ws, 13, c, gv, NOTEF)
            cell(ws, 14, c, '%s %s' % (gv, stt.lower()), HF, HFILL, border=True, al=Alignment(horizontal='center', wrap_text=True)); ws.column_dimensions[CL(c)].width = 11
    pc0 = c0 + 2 * G
    for g, gv in enumerate(groups):
        cell(ws, 14, pc0 + g, '%s %% difference' % gv, HF, HFILL, border=True, al=Alignment(horizontal='center', wrap_text=True)); ws.column_dimensions[CL(pc0 + g)].width = 11
    zc = pc0 + G; cell(ws, 14, zc, 'zero', HF, HFILL, border=True)
    cell(ws, 12, 1, 'criterion: status', NOTEF); cell(ws, 13, 1, 'criterion: ' + glabel, NOTEF)
    for rr in rows:
        rng = "%s!$B%d:$AW%d" % (q(S_SPEC), rr, rr)
        for g in range(G):
            for k in range(2):
                c = c0 + 2 * g + k; L_ = CL(c)
                cell(ws, rr, c, '=AVERAGEIFS(%s,%s!$B$%d:$AW$%d,%s$12,%s!$B$%d:$AW$%d,%s$13)' % (rng, q(S_SPEC), SPR['status'], SPR['status'], L_, q(S_SPEC), crit_row, crit_row, L_), fmt='0.0000')
            cell(ws, rr, pc0 + g, pct(ws, rr, CL(c0 + 2 * g + 1), CL(c0 + 2 * g)), fmt='0.0')
        cell(ws, rr, zc, 0, fmt='0')
    # summary table
    header(ws, 4, 1, [glabel.capitalize(), 'Healthy plots (n)', 'Diseased plots (n)', 'Mean PDI of diseased plots (%)'] + extra[0])
    for g, gv in enumerate(groups):
        r = 5 + g; cell(ws, r, 1, gv, BF, border=True)
        cell(ws, r, 2, '=COUNTIFS(%s!$B$%d:$AW$%d,"Healthy",%s!$B$%d:$AW$%d,$A%d)' % (q(S_SPEC), SPR['status'], SPR['status'], q(S_SPEC), crit_row, crit_row, r), fmt='0', border=True)
        cell(ws, r, 3, '=COUNTIFS(%s!$B$%d:$AW$%d,"Diseased",%s!$B$%d:$AW$%d,$A%d)' % (q(S_SPEC), SPR['status'], SPR['status'], q(S_SPEC), crit_row, crit_row, r), fmt='0', border=True)
        cell(ws, r, 4, '=AVERAGEIFS(%s!$B$%d:$AW$%d,%s!$B$%d:$AW$%d,"Diseased",%s!$B$%d:$AW$%d,$A%d)' % (q(S_SPEC), SPR['pdi'], SPR['pdi'], q(S_SPEC), SPR['status'], SPR['status'], q(S_SPEC), crit_row, crit_row, r), fmt='0.0', border=True)
        for j, f in enumerate(extra[1](gv, r)): cell(ws, r, 5 + j, f[0], fmt=f[1], border=True)
    # charts: one healthy-vs-diseased chart per group (2 per row) + one % difference chart
    acol = zc + 2
    for g, gv in enumerate(groups):
        ch = scatter(extra[2](gv), 15, 8.5)
        line(ch, ws, c0 + 2 * g, R0, RL, ws, name='Healthy (%s)' % gv, color=CH, w=2.25)
        line(ch, ws, c0 + 2 * g + 1, R0, RL, ws, name='Diseased (%s, mean of reps)' % gv, color=CD, w=2.25)
        place_at(ws, ch, 4 + (g // 2) * 17, colx(ws, acol) + (g % 2) * 15.3)
    ch = scatter('%% difference from healthy by %s' % glabel, 33, 9.5, ytitle='% difference', yfmt='0')
    for g, gv in enumerate(groups): line(ch, ws, pc0 + g, R0, RL, ws, name=gv, color=colors[gv], w=2)
    zero_line(ch, ws, zc, R0, RL)
    place(ws, ch, '%s%d' % (CL(acol), 4 + ((G + 1) // 2) * 17))
    ch = scatter('Diseased plots: mean spectrum by %s' % glabel, 15, 8.5)
    for g, gv in enumerate(groups): line(ch, ws, c0 + 2 * g + 1, R0, RL, ws, name='%s diseased' % gv, color=colors[gv], w=2)
    place(ws, ch, '%s%d' % (CL(acol), 4 + ((G + 1) // 2) * 17 + 20))
    ch = scatter('Healthy plots: mean spectrum by %s' % glabel, 15, 8.5)
    for g, gv in enumerate(groups): line(ch, ws, c0 + 2 * g, R0, RL, ws, name='%s healthy' % gv, color=colors[gv], w=2, dash='dash')
    place_at(ws, ch, 4 + ((G + 1) // 2) * 17 + 20, colx(ws, acol) + 15.3)
    ws.freeze_panes = 'B15'

group_sheet(S_VAR, 'Healthy vs diseased by variety', 'Each variety: healthy = mean of its 4 sprayed plots (D1-D4); diseased = mean of its 12 unsprayed plots (D1-D4 x R1-R3).',
            ['V1', 'V2', 'V3'], SPR['var'], CV, 'variety',
            ([], lambda gv, r: [], lambda gv: 'Variety %s: healthy vs diseased (mean PDI %.1f %%)' % (gv, np.mean([PDI0[p] for p in range(13, 49) if P.loc[p, 'variety'] == gv]))))
group_sheet(S_STG, 'Healthy vs diseased by growth stage (sowing date)',
            'Growth stage = sowing date D1-D4. Each stage: healthy = mean of its 3 sprayed plots (V1-V3); diseased = mean of its 9 unsprayed plots (V1-V3 x R1-R3).',
            ['D1', 'D2', 'D3', 'D4'], SPR['sow'], CS, 'growth stage',
            (['Sowing date', 'Group', 'DAS on image date'], lambda gv, r: [(SOWD[gv], None), (SOWG[gv], None), ('=%s-DATEVALUE(E%d)' % (DATE_CELL, r), '0')],
             lambda gv: '%s (sown %s, %d DAS): mean PDI %.1f %%' % (gv, SOWD[gv], DAS0[gv], np.mean([PDI0[p] for p in range(13, 49) if P.loc[p, 'timing'] == gv]))))
CSTG = sorted(set(STG0.values), key=['Vegetative', 'Flowering', 'Pod formation'].index)
group_sheet(S_CST, 'Healthy vs diseased by recorded crop stage on the image date',
            'Crop stage recorded in the field on %s (column W of 1_Plot_info). Healthy = sprayed plots in that stage; diseased = unsprayed plots in that stage. Flowering plots carry yellow petals (500-650 nm), so compare within a stage.' % D0.strftime('%d %b %Y'),
            CSTG, SPR['stage'], {'Vegetative': '1B9E77', 'Flowering': 'E6AB02', 'Pod formation': '7570B3'}, 'crop stage',
            ([], lambda gv, r: [], lambda gv: '%s plots: healthy vs diseased (mean PDI %.1f %%)' % (gv, np.mean([PDI0[p] for p in range(13, 49) if STG0[p] == gv]))))
# DATEVALUE on a text date is fragile across locales -> write real sowing dates instead
ws = wb[S_STG]
for g, gv in enumerate(['D1', 'D2', 'D3', 'D4']):
    cell(ws, 5 + g, 5, pd.Timestamp({'D1': '2025-12-09', 'D2': '2025-12-18', 'D3': '2025-12-27', 'D4': '2026-01-09'}[gv]).to_pydatetime(), fmt='dd-mmm-yyyy', border=True)
    cell(ws, 5 + g, 7, '=%s-E%d' % (DATE_CELL, 5 + g), fmt='0', border=True)
for c, w in ((5, 12), (6, 9), (7, 10)): ws.column_dimensions[CL(c)].width = max(ws.column_dimensions[CL(c)].width or 0, w)

# ---------------- 7 By treatment (V x D): healthy plot vs mean of R1-R3 ----------------
OT = 66                                          # data rows = Spectra rows + OT (charts above the data)
ws = wb[S_TRT]; title(ws, 'Treatment-wise comparison: mean of the 3 replications vs the matching healthy plot',
                     'Each treatment (variety x sowing date) has one sprayed healthy plot and three unsprayed replications (R1-R3). Charts: rows = growth stage D1-D4, columns = variety V1-V3; thin lines = individual replications. Data from row %d.' % (14 + OT))
wl_col(ws, OT)
TRTS = [(v, d) for d in ('D1', 'D2', 'D3', 'D4') for v in ('V1', 'V2', 'V3')]
TP = {}
for v, d in TRTS:
    ps = [p for p in range(1, NP + 1) if P.loc[p, 'variety'] == v and P.loc[p, 'timing'] == d]
    h = [p for p in ps if status(p) == 'Healthy'][0]; reps = {P.loc[p, 'block']: p for p in ps if status(p) == 'Diseased'}
    TP[(v, d)] = (h, [reps['R1'], reps['R2'], reps['R3']])
for t, (v, d) in enumerate(TRTS):
    c = 2 + 3 * t; h, reps = TP[(v, d)]
    cell(ws, 12 + OT, c, 'H: P%d | R1-R3: P%d, P%d, P%d' % ((h,) + tuple(reps)), NOTEF)
    cell(ws, 13 + OT, c, '%s-%s' % (v, d), BF)
    for k, lab_ in enumerate(['Healthy (P%d)' % h, 'Mean R1-R3', '% difference']):
        cell(ws, 14 + OT, c + k, lab_, HF, HFILL, border=True, al=Alignment(horizontal='center', wrap_text=True)); ws.column_dimensions[CL(c + k)].width = 10
    for rr in rows:
        cell(ws, rr + OT, c, '=' + SP(SPC(h), rr), fmt='0.0000')
        cell(ws, rr + OT, c + 1, '=AVERAGE(%s,%s,%s)' % tuple(SP(SPC(p), rr) for p in reps), fmt='0.0000')
        cell(ws, rr + OT, c + 2, pct(ws, rr + OT, CL(c + 1), CL(c)), fmt='0.0')
TZ = 2 + 3 * len(TRTS); cell(ws, 14 + OT, TZ, 'zero', HF, HFILL, border=True)
for rr in rows: cell(ws, rr + OT, TZ, 0, fmt='0')
ws.row_dimensions[14 + OT].height = 30
cell(ws, 3, 1, 'Chart rows: D1 (sown 9 Dec), D2 (18 Dec), D3 (27 Dec 2025), D4 (9 Jan 2026). Chart columns: V1, V2, V3. Mean PDI of each treatment and its severity rank: sheet 8_Treatments_by_severity.', NOTEF)
for t, (v, d) in enumerate(TRTS):
    c = 2 + 3 * t; h, reps = TP[(v, d)]
    ch = scatter('%s x %s (%d DAS) | mean PDI %.1f %%' % (v, d, DAS0[d], np.mean([PDI0[p] for p in reps])), 15, 8.5, ymin=0, ymax=0.4, tsize=10)
    line(ch, ws, c, R0 + OT, RL + OT, ws, name='Healthy P%d' % h, color=CH, w=2.25)
    for k, p in enumerate(reps): line(ch, WSS, 1 + p, R0, RL, WSS, name='R%d P%d' % (k + 1, p), color='F4A582', w=0.75)
    line(ch, ws, c + 1, R0 + OT, RL + OT, ws, name='Mean R1-R3', color=CD, w=2.25)
    place_at(ws, ch, 5 + (t // 3) * 17, (t % 3) * 15.3)
ws.freeze_panes = 'B5'

# ---------------- 8 Treatments ordered by severity ----------------
ws = wb[S_TSV]; title(ws, 'Treatments arranged by disease severity (mean PDI of R1-R3 on the image date)',
                     'Left table: the 12 treatments with their plots and mean PDI. Right table: the same treatments sorted from least to most severe. Charts follow the sorted order and update when the image date changes.')
header(ws, 4, 1, ['Treatment', 'Variety', 'Sowing', 'Healthy plot', 'R1 plot', 'R2 plot', 'R3 plot', 'Mean PDI R1-R3 (%)', 'Severity rank (1 = lowest)', 'Column position'], [10, 8, 8, 9, 8, 8, 8, 11, 11, 9])
for t, (v, d) in enumerate(TRTS):
    r = 5 + t; h, reps = TP[(v, d)]
    for j, val in enumerate(['%s-%s' % (v, d), v, d, h] + reps): cell(ws, r, 1 + j, val, border=True)
    cell(ws, r, 8, '=ROUND(AVERAGE(%s,%s,%s),6)' % tuple(INFO('S', p) for p in reps), BF, fmt='0.0', border=True)
    cell(ws, r, 9, '=RANK(H%d,$H$5:$H$16,1)+COUNTIF($H$4:H%d,H%d)' % (r, r - 1, r), fmt='0', border=True)
    cell(ws, r, 10, t + 1, border=True)
header(ws, 4, 12, ['Rank', 'Treatment', 'Mean PDI (%)', 'Position', 'Healthy label', 'Diseased label', 'Healthy P', 'R1-R3 plots'], [6, 10, 10, 8, 22, 30, 9, 14])
for k in range(1, 13):
    r = 4 + k; cell(ws, r, 12, k, BF, border=True)
    cell(ws, r, 13, '=INDEX($A$5:$A$16,MATCH(L%d,$I$5:$I$16,0))' % r, BF, border=True)
    cell(ws, r, 14, '=INDEX($H$5:$H$16,MATCH(L%d,$I$5:$I$16,0))' % r, fmt='0.0', border=True)
    cell(ws, r, 15, '=INDEX($J$5:$J$16,MATCH(L%d,$I$5:$I$16,0))' % r, fmt='0', border=True)
    cell(ws, r, 16, '=M%d&" healthy (P"&INDEX($D$5:$D$16,O%d)&")"' % (r, r), border=True)
    cell(ws, r, 17, '=M%d&" mean R1-R3 (PDI "&TEXT(N%d,"0.0")&"%%)"' % (r, r), border=True)
    cell(ws, r, 18, '=INDEX($D$5:$D$16,O%d)' % r, fmt='0', border=True)
    cell(ws, r, 19, '=INDEX($E$5:$E$16,O%d)&", "&INDEX($F$5:$F$16,O%d)&", "&INDEX($G$5:$G$16,O%d)' % (r, r, r), border=True)
# sorted data (rows = Spectra rows + OS); for rank k: healthy, mean R1-R3, % difference from 7_By_treatment
OS = 110
wl_col(ws, OS)
trng = lambda rr: "%s!$B%d:$%s%d" % (q(S_TRT), rr + OT, CL(1 + 3 * len(TRTS)), rr + OT)
for k in range(1, 13):
    c = 2 + 3 * (k - 1); pr = 4 + k
    for j, lab_ in enumerate(['Rank %d healthy' % k, 'Rank %d mean R1-R3' % k, 'Rank %d %% difference' % k]):
        cell(ws, 14 + OS, c + j, lab_, HF, HFILL, border=True, al=Alignment(horizontal='center', wrap_text=True))
    for rr in rows:
        for j in range(3): cell(ws, rr + OS, c + j, '=INDEX(%s,3*($O$%d-1)+%d)' % (trng(rr), pr, j + 1), fmt='0.0' if j == 2 else '0.0000')
TZ2 = 2 + 3 * 12; cell(ws, 14 + OS, TZ2, 'zero', HF, HFILL, border=True)
for rr in rows: cell(ws, rr + OS, TZ2, 0, fmt='0')
ws.row_dimensions[14 + OS].height = 30
cell(ws, 18, 1, 'Charts follow the sorted table (rank 1 = least severe). Data of the charts from row %d.' % (14 + OS), NOTEF)
ch = scatter('% difference from healthy: treatments from least (light) to most (dark) severe', 33, 11, ytitle='% difference', yfmt='0')
gc = grad(12, ('FEE08B', 'FDAE61', 'F46D43', 'D73027', 'A50026', '67001F'))
for k in range(1, 13): line(ch, ws, 2 + 3 * (k - 1) + 2, R0 + OS, RL + OS, ws, ref="%s!$Q$%d" % (q(S_TSV), 4 + k), color=gc[k - 1], w=1.75)
zero_line(ch, ws, TZ2, R0 + OS, RL + OS)
place(ws, ch, 'A19')
for k in range(1, 13):
    c = 2 + 3 * (k - 1)
    ch = scatter('Severity rank %d of 12%s' % (k, ' (least severe)' if k == 1 else ' (most severe)' if k == 12 else ''), 15, 8.5, ymin=0, ymax=0.4, tsize=10)
    line(ch, ws, c, R0 + OS, RL + OS, ws, ref="%s!$P$%d" % (q(S_TSV), 4 + k), color=CH, w=2.25)
    line(ch, ws, c + 1, R0 + OS, RL + OS, ws, ref="%s!$Q$%d" % (q(S_TSV), 4 + k), color=gc[k - 1] if k > 3 else 'F46D43', w=2.25)
    place_at(ws, ch, 42 + ((k - 1) // 3) * 17, ((k - 1) % 3) * 15.3)
ws.freeze_panes = 'A5'

# ---------------- 9 Severity groups and classes ----------------
ws = wb[S_SEV]; title(ws, 'Spectra by disease severity (plot PDI on the image date)',
                     'Severity groups: diseased plots ranked by PDI on the image date and split into four groups of 9 plots (Q1 least - Q4 most severe). The table on the right counts plots per 0-9 severity class (classes change with the date, so the group means are used for the curves).')
OV = 80                                          # data rows = Spectra rows + OV (charts above the data)
wl_col(ws, OV)
GR = ['Healthy', 'Q1', 'Q2', 'Q3', 'Q4']; CLS = [0, 1, 3, 5, 7, 9]
header(ws, 4, 1, ['Severity group', 'Plots (n)', 'Min PDI (%)', 'Max PDI (%)', 'Mean PDI (%)'], [16, 9, 10, 10, 10])
INFR = lambda col: "%s!$%s$5:$%s$52" % (q(S_INFO), col, col)
for g, gv in enumerate(GR):
    r = 5 + g; cell(ws, r, 1, gv, BF, border=True)
    cell(ws, r, 2, '=COUNTIF(%s,A%d)' % (INFR('V'), r), fmt='0', border=True)
    cell(ws, r, 3, '=_xlfn.MINIFS(%s,%s,A%d)' % (INFR('S'), INFR('V'), r), fmt='0.0', border=True)
    cell(ws, r, 4, '=_xlfn.MAXIFS(%s,%s,A%d)' % (INFR('S'), INFR('V'), r), fmt='0.0', border=True)
    cell(ws, r, 5, '=AVERAGEIFS(%s,%s,A%d)' % (INFR('S'), INFR('V'), r), fmt='0.0', border=True)
header(ws, 4, 7, ['Severity class', 'PDI range', 'Plots (n)', 'Mean PDI (%)'], [10, 11, 9, 10])
rng_txt = {0: '0 %', 1: '>0-5 %', 3: '>5-10 %', 5: '>10-25 %', 7: '>25-50 %', 9: '>50 %'}
for g, cv in enumerate(CLS):
    r = 5 + g; cell(ws, r, 7, cv, BF, border=True); cell(ws, r, 8, rng_txt[cv], border=True)
    cell(ws, r, 9, '=COUNTIF(%s,G%d)' % (INFR('T'), r), fmt='0', border=True)
    cell(ws, r, 10, '=IFERROR(AVERAGEIFS(%s,%s,G%d),"-")' % (INFR('S'), INFR('T'), r), fmt='0.0', border=True)
# columns
c = 2; GC = {}
for gv in GR: GC[gv] = c; cell(ws, 13 + OV, c, gv, NOTEF); cell(ws, 14 + OV, c, '%s mean' % gv, HF, HFILL, border=True); c += 1
PCC = {}
for gv in GR[1:]: PCC[gv] = c; cell(ws, 14 + OV, c, '%s %% difference' % gv, HF, HFILL, border=True); c += 1
RA, RD = c, c + 1; cell(ws, 14 + OV, RA, 'r with PDI (all 48 plots)', HF, HFILL, border=True); cell(ws, 14 + OV, RD, 'r with PDI (36 diseased plots)', HF, HFILL, border=True); c += 2
NC = {}
for gv in GR: NC[gv] = c; cell(ws, 14 + OV, c, '%s (shape)' % gv, HF, HFILL, border=True); c += 1
ZC = c; cell(ws, 14 + OV, ZC, 'zero', HF, HFILL, border=True)
for j in range(2, ZC + 1): ws.column_dimensions[CL(j)].width = 10.5
ws.row_dimensions[14 + OV].height = 42
for j in range(2, ZC + 1): ws.cell(14 + OV, j).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
for rr in rows:
    rng = "%s!$B%d:$AW%d" % (q(S_SPEC), rr, rr); o = rr + OV
    for gv in GR: cell(ws, o, GC[gv], '=AVERAGEIFS(%s,%s!$B$%d:$AW$%d,%s$%d)' % (rng, q(S_SPEC), SPR['grp'], SPR['grp'], CL(GC[gv]), 13 + OV), fmt='0.0000')
    for gv in GR[1:]: cell(ws, o, PCC[gv], pct(ws, o, CL(GC[gv]), CL(GC['Healthy'])), fmt='0.0')
    cell(ws, o, RA, '=CORREL(%s!$B%d:$AW%d,%s!$B$%d:$AW$%d)' % (q(S_SPEC), rr, rr, q(S_SPEC), SPR['pdi'], SPR['pdi']), fmt='0.00')
    cell(ws, o, RD, '=CORREL(%s!$N%d:$AW%d,%s!$N$%d:$AW$%d)' % (q(S_SPEC), rr, rr, q(S_SPEC), SPR['pdi'], SPR['pdi']), fmt='0.00')
    for gv in GR: cell(ws, o, NC[gv], '=%s%d/AVERAGE(%s$%d:%s$%d)' % (CL(GC[gv]), o, CL(GC[gv]), R0 + OV, CL(GC[gv]), RL + OV), fmt='0.000')
    cell(ws, o, ZC, 0, fmt='0')
cell(ws, 12, 1, 'Charts below; data of the charts from row %d. ' % (14 + OV) + 'r: Pearson correlation between plot reflectance and plot PDI at each wavelength. |r| > 0.33 is significant at p < 0.05 for 36 plots (> 0.28 for 48 plots).', NOTEF)
ch = scatter('Mean spectrum by severity group (healthy, Q1 least - Q4 most severe)', 23, 10.5)
for gv in GR: line(ch, ws, GC[gv], R0 + OV, RL + OV, ws, name=gv if gv == 'Healthy' else '%s diseased' % gv, color=CQ[gv], w=2.25)
place(ws, ch, 'A14')
ch = scatter('% difference from healthy by severity group', 23, 10.5, ytitle='% difference', yfmt='0')
for gv in GR[1:]: line(ch, ws, PCC[gv], R0 + OV, RL + OV, ws, name=gv, color=CQ[gv], w=2)
zero_line(ch, ws, ZC, R0 + OV, RL + OV); place_at(ws, ch, 14, 23.3)
ch = scatter('Correlation of reflectance with plot PDI', 23, 10.5, ytitle='Pearson r', yfmt='0.0', )
line(ch, ws, RA, R0 + OV, RL + OV, ws, name='All 48 plots (healthy + diseased)', color='4D4D4D', w=2)
line(ch, ws, RD, R0 + OV, RL + OV, ws, name='36 diseased plots only', color=CD, w=2); zero_line(ch, ws, ZC, R0 + OV, RL + OV, name='r = 0')
ch.y_axis.scaling.min, ch.y_axis.scaling.max = -1, 1
place(ws, ch, 'A36')
ch = scatter('Spectral shape (brightness removed) by severity group', 23, 10.5, ytitle='Relative reflectance', yfmt='0.0')
for gv in GR: line(ch, ws, NC[gv], R0 + OV, RL + OV, ws, name=gv, color=CQ[gv], w=2)
place_at(ws, ch, 36, 23.3)
ws.freeze_panes = 'A4'

# ---------------- 10 Sorted spectra (rank order) ----------------
ws = wb[S_SRT]; title(ws, 'Plot spectra sorted by disease severity (rank 1 = lowest PDI on the image date)',
                     'Rows 3-10: rank, column of the plot in 2_Spectra, plot, status, treatment, PDI, class and label (all formulas). Healthy plots (PDI 0) come first, ordered by plot number.')
labs = ['Severity rank', 'Column in 2_Spectra', 'Plot', 'Status', 'Treatment', 'PDI (%)', 'Severity class', 'Chart label']
for i, t in enumerate(labs): cell(ws, 3 + i, 1, t, BF, LFILL, border=True)
SR = lambda row: "%s!$B$%d:$AW$%d" % (q(S_SPEC), row, row)
for k in range(1, NP + 1):
    c = 1 + k; L_ = CL(c)
    cell(ws, 3, c, k, BF, border=True, al=Alignment(horizontal='center'))
    cell(ws, 4, c, '=MATCH(%s3,%s,0)' % (L_, SR(SPR['rank'])), fmt='0', border=True, al=Alignment(horizontal='center'))
    for i, key in enumerate(['plot', 'status', 'trt', 'pdi', 'cls']):
        cell(ws, 5 + i, c, '=INDEX(%s,%s$4)' % (SR(SPR[key]), L_), fmt='0.0' if key == 'pdi' else None, border=True, al=Alignment(horizontal='center'))
    cell(ws, 10, c, '="Rank "&%s3&": P"&%s5&" "&%s7&" ("&%s6&") PDI "&TEXT(%s8,"0.0")&"%%"' % (L_, L_, L_, L_, L_), border=True, al=Alignment(wrap_text=True))
    cell(ws, 14, c, 'Rank %d' % k, HF, HFILL, border=True, al=Alignment(horizontal='center'))
    ws.column_dimensions[L_].width = 10
ws.row_dimensions[10].height = 55
wl_col(ws)
for rr in rows:
    rng = "%s!$B%d:$AW%d" % (q(S_SPEC), rr, rr)
    for k in range(1, NP + 1): cell(ws, rr, 1 + k, '=INDEX(%s,%s$4)' % (rng, CL(1 + k)), fmt='0.0000')
ws.column_dimensions['A'].width = 20
ws.freeze_panes = 'B15'

# ---------------- 11 Plots by severity (charts) ----------------
ws = wb[S_PSV]; title(ws, 'Plot spectra arranged by disease severity (least to most severe)',
                     'Every chart shows the plot at that severity rank on the selected image date (legend = plot, treatment, status, PDI). Colour runs from green (rank 1) to dark red (rank 48). Same y-axis (0-0.40).')
gc48 = grad(NP)
ch = scatter('All plots coloured by severity rank (green = least, dark red = most severe)', 33, 12, ymin=0, ymax=0.4, legend=None)
for k in range(1, NP + 1): line(ch, wb[S_SRT], 1 + k, R0, RL, wb[S_SRT], ref="%s!$%s$10" % (q(S_SRT), CL(1 + k)), color=gc48[k - 1], w=1.0)
place(ws, ch, 'A4')
for k in range(1, NP + 1):
    j = k - 1; rr = 29 + (j // 4) * 17
    ch = scatter('Severity rank %d of 48' % k, 15, 8.2, ymin=0, ymax=0.4, legend='t', tsize=10)
    line(ch, wb[S_SRT], 1 + k, R0, RL, wb[S_SRT], ref="%s!$%s$10" % (q(S_SRT), CL(1 + k)), color=gc48[j], w=1.75)
    place_at(ws, ch, rr, (j % 4) * 15.3)

# ---------------- 12 Region means ----------------
ws = wb[S_REG]; title(ws, 'Band-region means per plot and the main statistics',
                     'Mean reflectance of each plot in seven regions (AVERAGEIFS over the bands inside each range). Statistics: healthy vs diseased means, % difference, Welch t-test (Welch, 1947) and correlation with PDI.')
REG = [('Blue', 450, 510, 'chlorophyll/carotenoid absorption'), ('Green peak', 530, 570, 'chlorophyll (green reflectance rises when chlorophyll falls)'),
       ('Red', 650, 690, 'chlorophyll absorption maximum'), ('Red edge', 700, 740, 'chlorophyll content; red-edge shift'),
       ('NIR plateau', 780, 880, 'leaf internal structure and canopy'), ('SWIR-1', 1550, 1750, 'leaf water and dry matter'), ('SWIR-2', 2050, 2300, 'water, cellulose, lignin')]
header(ws, 4, 1, ['Region', 'From (nm)', 'To (nm)', 'Bands (n)', 'What it mainly shows (Carter and Knapp, 2001; Mahlein et al., 2013)'], [14, 9, 9, 9, 9]); ws.merge_cells('E4:L4')
WLR = "%s!$A$%d:$A$%d" % (q(S_SPEC), R0, RL)
for i, (n, lo, hi, txt) in enumerate(REG):
    r = 5 + i; cell(ws, r, 1, n, BF, border=True); cell(ws, r, 2, lo, INF, border=True); cell(ws, r, 3, hi, INF, border=True)
    cell(ws, r, 4, '=COUNTIFS(%s,">="&B%d,%s,"<="&C%d)' % (WLR, r, WLR, r), fmt='0', border=True); cell(ws, r, 5, txt, border=True); ws.merge_cells(start_row=r, start_column=5, end_row=r, end_column=12)
cell(ws, 12, 1, 'Blue cells (region limits) can be changed; all values below update.', NOTEF)
PR0 = 15
header(ws, PR0 - 1, 1, ['Plot', 'Status', 'Variety', 'Sowing', 'PDI (%)'] + [n for n, *_ in REG])
for c in range(6, 6 + len(REG)): ws.column_dimensions[CL(c)].width = 11
for p in range(1, NP + 1):
    r = PR0 - 1 + p; fill = GFILL if status(p) == 'Healthy' else None
    for j, v in enumerate([p, status(p), P.loc[p, 'variety'], P.loc[p, 'timing']]): cell(ws, r, 1 + j, v, fill=fill, border=True)
    cell(ws, r, 5, '=' + INFO('S', p), fmt='0.0', fill=fill, border=True)
    col = "%s!$%s$%d:$%s$%d" % (q(S_SPEC), SPC(p), R0, SPC(p), RL)
    for i in range(len(REG)):
        cell(ws, r, 6 + i, '=AVERAGEIFS(%s,%s,">="&$B$%d,%s,"<="&$C$%d)' % (col, WLR, 5 + i, WLR, 5 + i), fmt='0.0000', fill=fill, border=True)
HR1, HR2, DR1, DR2 = PR0, PR0 + 11, PR0 + 12, PR0 + 47
SS = DR2 + 2
labels = ['Healthy mean (12 plots)', 'Diseased mean (36 plots)', '% difference (D - H) / H', 'Welch t-test p (healthy vs diseased)', 'r with PDI (36 diseased plots)', 'r with PDI (all 48 plots)']
for i, t in enumerate(labels): cell(ws, SS + i, 1, t, BF, LFILL, border=True); ws.merge_cells(start_row=SS + i, start_column=1, end_row=SS + i, end_column=5)
for i in range(len(REG)):
    L_ = CL(6 + i)
    f = ['=AVERAGE(%s%d:%s%d)' % (L_, HR1, L_, HR2), '=AVERAGE(%s%d:%s%d)' % (L_, DR1, L_, DR2), '=(%s%d-%s%d)/%s%d*100' % (L_, SS + 1, L_, SS, L_, SS),
         '=TTEST(%s%d:%s%d,%s%d:%s%d,2,3)' % (L_, HR1, L_, HR2, L_, DR1, L_, DR2), '=CORREL(%s%d:%s%d,$E$%d:$E$%d)' % (L_, DR1, L_, DR2, DR1, DR2),
         '=CORREL(%s%d:%s%d,$E$%d:$E$%d)' % (L_, HR1, L_, DR2, HR1, DR2)]
    for j, ff in enumerate(f): cell(ws, SS + j, 6 + i, ff, BF if j == 2 else NF, fmt=['0.0000', '0.0000', '0.0', '0.000', '0.00', '0.00'][j], border=True)
# % difference by variety and by growth stage (group mean of diseased vs healthy of the same group)
def pdiff_table(r0, name, crit_col, groups):
    cell(ws, r0, 1, '%% difference (diseased vs healthy of the same %s) per region' % name, SF)
    header(ws, r0 + 1, 1, [name.capitalize(), '', '', '', 'Mean PDI (%)'] + [n for n, *_ in REG])
    for g, gv in enumerate(groups):
        r = r0 + 2 + g; cell(ws, r, 1, gv, BF, border=True)
        cell(ws, r, 5, '=AVERAGEIFS($E$%d:$E$%d,$%s$%d:$%s$%d,$A%d)' % (DR1, DR2, crit_col, DR1, crit_col, DR2, r), fmt='0.0', border=True)
        for i in range(len(REG)):
            L_ = CL(6 + i)
            cell(ws, r, 6 + i, '=(AVERAGEIFS(%s$%d:%s$%d,$%s$%d:$%s$%d,$A%d)/AVERAGEIFS(%s$%d:%s$%d,$%s$%d:$%s$%d,$A%d)-1)*100' %
                 (L_, DR1, L_, DR2, crit_col, DR1, crit_col, DR2, r, L_, HR1, L_, HR2, crit_col, HR1, crit_col, HR2, r), fmt='0.0', border=True)
    return r0 + 2, r0 + 1 + len(groups)
VT = SS + 8; v1, v2 = pdiff_table(VT, 'variety', 'C', ['V1', 'V2', 'V3'])
ST = v2 + 3; s1, s2 = pdiff_table(ST, 'growth stage', 'D', ['D1', 'D2', 'D3', 'D4'])
def bar(ttl, r1, r2, colors, anchor, ytitle='% difference'):
    ch = BarChart(); ch.type = 'col'; ch.grouping = 'clustered'; ch.title = mtitle(ttl, 11); ch.roundedCorners = False; ch.width, ch.height = 22, 9
    for r in range(r1, r2 + 1):
        s = Series(Reference(ws, min_col=6, max_col=5 + len(REG), min_row=r), title=None); s.tx = SeriesLabel(strRef=StrRef("%s!$A$%d" % (q(S_REG), r)))
        s.spPr = GraphicalProperties(solidFill=colors[r - r1]); ch.series.append(s)
    ch.set_categories(Reference(ws, min_col=6, max_col=5 + len(REG), min_row=PR0 - 1))
    ch.y_axis.title = mtitle(ytitle, 9, '404040'); ch.x_axis.delete = False; ch.y_axis.delete = False; ch.x_axis.tickLblPos = 'low'
    ch.x_axis.txPr = rich(8); ch.y_axis.txPr = rich(8); ch.y_axis.number_format = '0'
    ch.y_axis.majorGridlines = ChartLines(spPr=GraphicalProperties(ln=LineProperties(solidFill='E3E3E3', w=6350)))
    ch.legend.position = 'b'; ch.legend.overlay = False; ch.legend.txPr = rich(8)
    ws.add_chart(ch, anchor)
bar('% difference of diseased from healthy per band region (all plots)', SS + 2, SS + 2, [CD], 'N4')
bar('% difference per band region by variety', v1, v2, [CV[g] for g in ('V1', 'V2', 'V3')], 'N24')
bar('% difference per band region by growth stage', s1, s2, [CS[g] for g in ('D1', 'D2', 'D3', 'D4')], 'N44')
# the all-plots bar uses the label in column A of the % difference row
ws.freeze_panes = 'A15'

# ---------------- 14 References ----------------
ws = wb[S_REF]; title(ws, 'References')
REFS = ['Aasen, H., Honkavaara, E., Lucieer, A., Zarco-Tejada, P.J. (2018). Quantitative remote sensing at ultra-high resolution with UAV spectroscopy: a review of sensor technology, measurement procedures, and data correction workflows. Remote Sensing 10(7), 1091.',
        'Carter, G.A., Knapp, A.K. (2001). Leaf optical properties in higher plants: linking spectral characteristics to stress and chlorophyll concentration. American Journal of Botany 88(4), 677-684.',
        'Conn, K.L., Tewari, J.P., Awasthi, R.P. (1990). A disease assessment key for Alternaria blackspot in rapeseed and mustard. Canadian Plant Disease Survey 70(1), 19-22.',
        'Gruninger, J., Ratkowski, A.J., Hoke, M.L. (2004). The sequential maximum angle convex cone (SMACC) endmember model. Proceedings of SPIE 5425, 1-14.',
        'Mahlein, A.-K., Rumpf, T., Welke, P., Dehne, H.-W., Plümer, L., Steiner, U., Oerke, E.-C. (2013). Development of spectral indices for detecting and identifying plant diseases. Remote Sensing of Environment 128, 21-30.',
        'Savitzky, A., Golay, M.J.E. (1964). Smoothing and differentiation of data by simplified least squares procedures. Analytical Chemistry 36(8), 1627-1639.',
        "Welch, B.L. (1947). The generalization of 'Student's' problem when several different population variances are involved. Biometrika 34(1-2), 28-35.",
        'Wheeler, B.E.J. (1969). An Introduction to Plant Diseases. John Wiley and Sons, London.']
for i, t in enumerate(REFS): cell(ws, 3 + i, 1, t, NF, al=Alignment(wrap_text=True, vertical='top')); ws.row_dimensions[3 + i].height = 30
ws.column_dimensions['A'].width = 150

# ---------------- 0 Contents ----------------
from scipy import stats
ws = ws0
pdi_v = np.array([PDI0[p] for p in range(1, NP + 1)]); dis = slice(12, NP)
def regm(lo, hi): return R[(WL >= lo) & (WL <= hi)].mean(0)
RS = []
for n_, lo, hi, _ in REG:
    m = regm(lo, hi); RS.append((n_, (m[dis].mean() / m[:12].mean() - 1) * 100, stats.ttest_ind(m[:12], m[dis], equal_var=False).pvalue, np.corrcoef(m[dis], pdi_v[dis])[0, 1]))
nir = regm(780, 880)
tdiff = [(np.mean(nir[[p - 1 for p in TP[t][1]]]) / nir[TP[t][0] - 1] - 1) * 100 for t in TRTS]
Hm, Dm = R[:, :12].mean(1), R[:, dis].mean(1); Hn, Dn = Hm / Hm.mean(), Dm / Dm.mean()
shp = lambda w: (Dn[np.argmin(abs(WL - w))] / Hn[np.argmin(abs(WL - w))] - 1) * 100
tp = {'%s-%s' % t: np.mean([PDI0[p] for p in TP[t][1]]) for t in TRTS}; tmin, tmax = min(tp, key=tp.get), max(tp, key=tp.get)
grp_mean = lambda key, val: np.mean([PDI0[p] for p in range(13, NP + 1) if key(p) == val])
cls = pd.Series(pdi_v[dis]).apply(lambda x: 0 if x == 0 else 1 if x <= 5 else 3 if x <= 10 else 5 if x <= 25 else 7 if x <= 50 else 9).value_counts()
pv = [x[2] for x in RS]; dv_ = [x[1] for x in RS]; rv = [x[3] for x in RS]
def stg_nir(st):
    h = [p - 1 for p in range(1, 13) if STG0[p] == st]; d_ = [p - 1 for p in range(13, NP + 1) if STG0[p] == st]
    return (nir[d_].mean() / nir[h].mean() - 1) * 100
cell(ws, 1, 1, 'UAV hyperspectral plot spectra, %s: healthy vs white-rust-diseased mustard (IARI 2025-26)' % D0.strftime('%d %b %Y'), TF)
cell(ws, 2, 1, 'Plot mean reflectance of 48 plots (ENVI ROI means, %d bands, %.0f-%.0f nm) compared by disease status, variety, growth stage, crop stage, treatment and severity.' % (len(WL), WL[0], WL[-1]), NOTEF)
cell(ws, 4, 1, 'Image', SF)
cell(ws, 6, 1, 'Image (flight) date', BF); cell(ws, 6, 3, D0.to_pydatetime(), Font(name=AR, size=11, bold=True, color='1F3864'), LFILL, fmt='dd-mmm-yyyy', border=True)
cell(ws, 6, 4, 'Headwall hyperspectral flight of %s (the only image processed so far). Plot severity = ASD leaf scores recorded on the same day. All formulas use this cell; images of later flights will be added as they are processed.' % D0.strftime('%d %b %Y'), NOTEF)
cell(ws, 8, 1, 'Experiment', SF)
exp = [('Design', '48 plots: 12 treatments (varieties V1-V3 x sowing dates D1-D4) x 3 unsprayed replications (R1-R3) + 12 fungicide-sprayed healthy plots (one per treatment).'),
       ('Healthy', 'Plots 1-12 (block C, fungicide-sprayed; PDI = 0).'),
       ('Diseased', 'Plots 13-48 (R3 = 13-24, R2 = 25-36, R1 = 37-48), unsprayed, natural white rust infection.'),
       ('Growth stage', 'Sowing date D1 = 9 Dec 2025 (50 DAS group), D2 = 18 Dec (40 DAS), D3 = 27 Dec 2025 (30 DAS), D4 = 9 Jan 2026 (20 DAS) = %d, %d, %d and %d days after sowing on %s; recorded crop stage on the day in 6b_By_crop_stage.' % (DAS0['D1'], DAS0['D2'], DAS0['D3'], DAS0['D4'], D0.strftime('%d %b'))),
       ('Severity', 'Plot PDI = sum of ASD leaf scores (0-9) / (9 x leaves) x 100 (Wheeler, 1969; Conn et al., 1990), from 13_Leaf_scores; classes 0/1/3/5/7/9 and four equal severity groups (Q1-Q4) of diseased plots.'),
       ('Spectra', 'ENVI ASCII plot file "Mean: ROI #n" columns; ROI #n = plot n (plot-number order). Bands removed in processing (900-915, 1335-1460, 1785-1965 nm) appear as gaps.')]
for i, (k, v) in enumerate(exp): cell(ws, 9 + i, 1, k, BF); cell(ws, 9 + i, 3, v)
F0 = 16; cell(ws, F0, 1, 'Key findings (%s)' % D0.strftime('%d %b %Y'), SF)
finds = [
 '1. Disease level: the 36 unsprayed plots had PDI %.1f-%.1f %% (mean %.1f %%; %d plots in class 7, %d in class 9); healthy plots 0 %%. Least severe treatment %s (%.1f %%), most severe %s (%.1f %%). Earlier sowing = more disease: D1 %.1f, D2 %.1f, D3 %.1f, D4 %.1f %%; by variety V1 %.1f, V2 %.1f, V3 %.1f %%; flowering plots %.1f %% vs vegetative plots %.1f %%.'
   % (pdi_v[dis].min(), pdi_v[dis].max(), pdi_v[dis].mean(), cls.get(7, 0), cls.get(9, 0), tmin, tp[tmin], tmax, tp[tmax],
      *[grp_mean(lambda p: P.loc[p, 'timing'], d) for d in ('D1', 'D2', 'D3', 'D4')], *[grp_mean(lambda p: P.loc[p, 'variety'], v) for v in ('V1', 'V2', 'V3')], grp_mean(lambda p: STG0[p], 'Flowering'), grp_mean(lambda p: STG0[p], 'Vegetative')),
 '2. Mean spectra: diseased plots reflect %.1f to %.1f %% less than healthy plots in all seven band regions (largest in SWIR-2 and the NIR plateau), but no region differs significantly (Welch p = %.2f-%.2f) because plot-to-plot variation is large (12_Region_means). Within the recorded crop stage, vegetative diseased plots are %.0f %% darker in the NIR than vegetative healthy plots (5 healthy plots only), while flowering plots hardly differ (%+.0f %%) (6b_By_crop_stage).'
   % (abs(max(dv_)), abs(min(dv_)), min(pv), max(pv), -stg_nir('Vegetative'), stg_nir('Flowering')),
 '3. Brightness: single-plot NIR reflectance ranges from %.2f to %.2f, also between replications of one treatment, and D3 plots are dark in healthy and diseased plots alike. Treatment by treatment, diseased NIR is %.0f %% to +%.0f %% of its healthy plot (%d of 12 lower). These are mainly illumination/radiometric differences (Aasen et al., 2018).'
   % (nir.min(), nir.max(), min(tdiff), max(tdiff), sum(x < 0 for x in tdiff)),
 '4. Spectral shape (each mean spectrum divided by its own mean): diseased plots are relatively higher in the red (680 nm %+.1f %%) and green (550 nm %+.1f %%) and lower in SWIR-2 (2200 nm %+.1f %%), the expected signs of chlorophyll loss and drier tissue (Carter and Knapp, 2001) (4_Healthy_vs_Diseased, 9_Severity_groups).'
   % (shp(680), shp(550), shp(2200)),
 '5. Severity: within the diseased plots, reflectance rises slightly with PDI (r = %+.2f to %+.2f) because the most severe plots are the early-sown D1 plots, which are also the brightest. Severity is mixed with sowing date and canopy brightness, so judge it within treatments (7_, 8_) and from the shape curves.'
   % (min(rv), max(rv)),
 '6. Before modelling: check the radiometric calibration (reflectance panels, illumination, flight lines, view angle) or use brightness-independent features (spectral shape, first derivative, normalised indices); then repeat this workbook for the other flight dates.']
for i, t in enumerate(finds):
    cell(ws, F0 + 1 + i, 1, t, NF, al=Alignment(wrap_text=True, vertical='top')); ws.merge_cells(start_row=F0 + 1 + i, start_column=1, end_row=F0 + 1 + i, end_column=14)
    ws.row_dimensions[F0 + 1 + i].height = 15 * (1 + len(t) // 170)
G0 = F0 + len(finds) + 2; cell(ws, G0, 1, 'Sheets', SF)
guide = [(S_INFO, 'plot, block, status, variety, sowing, treatment, PDI and severity class/rank/group, crop stage (PDI of other ASD dates for reference)'),
         (S_SPEC, 'the 48 plot spectra (one column per plot) with attribute rows used by all comparisons'),
         (S_PCH, 'spectrum of every plot (one chart per plot, PDI and crop stage in the title) + all plots overlaid'),
         (S_HD, 'mean healthy vs mean diseased spectra, ± SD, % difference and spectral shape'),
         (S_VAR, 'healthy vs diseased for each variety; % difference by variety'),
         (S_STG, 'healthy vs diseased for each growth stage (sowing date D1-D4); % difference by stage'),
         (S_CST, 'healthy vs diseased within the recorded crop stage of the day (vegetative, flowering)'),
         (S_TRT, 'each treatment: mean of the 3 replications vs its healthy plot (12 charts, D1-D4 x V1-V3)'),
         (S_TSV, 'the 12 treatment comparisons arranged from least to most severe + % difference by severity rank'),
         (S_SEV, 'mean spectra of healthy and severity groups Q1-Q4, % difference, correlation with PDI, spectral shape; plots per 0-9 class'),
         (S_SRT, 'plot spectra sorted by severity rank (formulas)'),
         (S_PSV, 'one chart per plot arranged by severity rank (least to most severe) + overlay coloured by rank'),
         (S_REG, 'band-region means per plot; healthy vs diseased means, % difference, Welch t-test p, r with PDI; by variety and stage'),
         (S_LEAF, 'ASD leaf scores used for plot PDI'), (S_REF, 'references')]
for i, (k, v) in enumerate(guide):
    x = cell(ws, G0 + 1 + i, 1, k, Font(name=AR, size=10, color='0563C1', underline='single')); x.hyperlink = "#'%s'!A1" % k; cell(ws, G0 + 1 + i, 3, v)
    ws.merge_cells(start_row=G0 + 1 + i, start_column=3, end_row=G0 + 1 + i, end_column=14)
r = G0 + len(guide) + 2
cell(ws, r, 1, 'Main results per band region (live formulas from 12_Region_means)', SF)
header(ws, r + 1, 1, ['Band region', '', 'Healthy mean', 'Diseased mean', '% difference', 'Welch p', 'r with PDI (diseased)'])
for i, (n, *_r) in enumerate(REG):
    rr = r + 2 + i; L_ = CL(6 + i); cell(ws, rr, 1, n, BF, border=True)
    for j, (off, fmt) in enumerate([(0, '0.0000'), (1, '0.0000'), (2, '0.0'), (3, '0.000'), (4, '0.00')]):
        cell(ws, rr, 3 + j, "=%s!%s%d" % (q(S_REG), L_, SS + off), fmt=fmt, border=True)
for rr_ in range(r + 1, r + 2 + len(REG)): ws.merge_cells(start_row=rr_, start_column=1, end_row=rr_, end_column=2)
r2 = r + 2 + len(REG) + 1
cell(ws, r2, 1, 'Data checks and notes', SF)
notes = ['1. Negative reflectance (red in 2_Spectra) occurs only at the SWIR end (from 1996 nm in plots 13-14, from 2360 nm in plots 16, 30, 31, 32, 41, 42) = sensor noise. Do not interpret > 2350 nm or the noisy band edges next to the removed water bands (about 1310-1330, 1461-1480 and 1971-2000 nm).',
         '2. Because overall brightness differs strongly between plots (finding 3), compare each treatment with its own healthy plot (7_, 8_) and look at the spectral shape curves rather than raw reflectance alone.',
         '3. % difference = (diseased - healthy) / healthy x 100, shown only where healthy reflectance > 0.005.',
         '4. Healthy plots have PDI = 0, so they take severity ranks 1-12; diseased plots are ranked 13-48 by PDI (ties broken by plot number).',
         '5. Colours: green = healthy, red = diseased; severity charts run from yellow/orange (low) to dark red (high). All values are formulas or recorded data.']
for i, t in enumerate(notes): cell(ws, r2 + 1 + i, 1, t, NF, al=Alignment(wrap_text=True, vertical='top')); ws.merge_cells(start_row=r2 + 1 + i, start_column=1, end_row=r2 + 1 + i, end_column=14); ws.row_dimensions[r2 + 1 + i].height = 15 * (1 + len(t) // 170)
ws.column_dimensions['A'].width = 26; ws.column_dimensions['B'].width = 2; ws.column_dimensions['C'].width = 16
for c in 'DEFGHIJKLMN': ws.column_dimensions[c].width = 15
for i in range(len(exp)):
    ws.merge_cells(start_row=9 + i, start_column=3, end_row=9 + i, end_column=14); ws.cell(9 + i, 3).alignment = Alignment(wrap_text=True, vertical='top')
    ws.row_dimensions[9 + i].height = 15 * (1 + len(exp[i][1]) // 170)
ws.merge_cells('D6:N6'); ws['D6'].alignment = Alignment(wrap_text=True, vertical='top'); ws.row_dimensions[6].height = 30
for rr_ in [6] + list(range(9, 9 + len(exp))): ws.cell(rr_, 1).alignment = Alignment(vertical='top')
ws['C6'].alignment = Alignment(horizontal='center', vertical='top')

for w in wb.worksheets: w.sheet_view.zoomScale = 90
PA = {S_CON: 'A1:N70', S_CST: 'J1:AA80', S_PCH: 'A1:AJ230', S_HD: 'P1:AF64', S_VAR: 'M1:AD80', S_STG: 'O1:AF100', S_TRT: 'A1:AA74', S_TSV: 'A1:AA112', S_SEV: 'A1:AC78', S_PSV: 'A1:AJ232', S_REG: 'A1:AB100'}
for sh, a in PA.items():
    w = wb[sh]; w.print_area = a; w.page_setup.orientation = 'landscape'; w.page_setup.fitToWidth = 1; w.page_setup.fitToHeight = 0
    w.sheet_properties.pageSetUpPr.fitToPage = True
if os.environ.get('QA'):                          # QA copy: only chart sheets are exported to PDF
    for w in wb.worksheets:
        if w.title not in PA: w.sheet_state = 'hidden'
os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT); print('saved', OUT, 'rows', R0, RL)
