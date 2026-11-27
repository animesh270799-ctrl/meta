"""Excel workbook of the Part L analysis: one sheet per step (step card + tables + native charts built from the cells of the sheet),
the leaf table, the 5-nm spectra, formula sheets that recompute key results (cross-check), a Checks sheet, deviations and references."""
import os, sys, json, pickle, numpy as np, pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as CL
from openpyxl.chart import ScatterChart, BarChart, LineChart, Reference, Series
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.marker import Marker, DataPoint
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.worksheet.hyperlink import Hyperlink
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..'))
import d0_text, d2_specs, refs, configL as C
T = pickle.load(open(os.path.join(HERE, 'tables.pkl'), 'rb')); F = json.load(open(os.path.join(HERE, 'facts.json')))
STEPS = d0_text.steps(T, F); SPECS = {s['id']: s for s in d2_specs.specs(T, F)}; OUTX = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'PartL_ASD_2025-26_leaf_analysis.xlsx')
AR = 'Arial'; FN = Font(name=AR, size=10); FB = Font(name=AR, size=10, bold=True); FT = Font(name=AR, size=14, bold=True, color='1F3864'); FS = Font(name=AR, size=11, bold=True, color='1F3864')
FH = Font(name=AR, size=10, bold=True, color='FFFFFF'); FNOTE = Font(name=AR, size=9, italic=True, color='555555'); FLINK = Font(name=AR, size=10, color='0563C1', underline='single')
HF = PatternFill('solid', fgColor='1F3864'); LF = PatternFill('solid', fgColor='DCE6F1'); GF = PatternFill('solid', fgColor='E2EFDA'); YF = PatternFill('solid', fgColor='FFF2CC'); RF = PatternFill('solid', fgColor='FCE4D6')
thin = Side(style='thin', color='BFBFBF'); BOX = Border(left=thin, right=thin, top=thin, bottom=thin); WR = Alignment(wrap_text=True, vertical='top'); CEN = Alignment(horizontal='center', vertical='center', wrap_text=True)
wb = Workbook(); wb.remove(wb.active); SHEETS = {}
def sheet(name, tab=None):
    ws = wb.create_sheet(name); ws.sheet_view.showGridLines = False; ws.sheet_properties.tabColor = tab; SHEETS[name] = ws; return ws
def put(ws, r, c, v, font=FN, fill=None, fmt=None, al=None, border=False):
    x = ws.cell(r, c, v); x.font = font
    if fill: x.fill = fill
    if fmt: x.number_format = fmt
    if al: x.alignment = al
    if border: x.border = BOX
    return x
def title(ws, t, sub=None):
    put(ws, 1, 1, t, FT); 
    if sub: put(ws, 2, 1, sub, FNOTE)
    return 4
def numfmt(v):
    if isinstance(v, (int, np.integer)): return '0'
    if isinstance(v, (float, np.floating)): return '0.000' if abs(v) < 100 else '0.0'
    return None
def table(ws, r, c, df, caption=None, widths=None, fmts=None, index=False, hdr_fill=HF, wrap=False):
    """Write a DataFrame with a caption row; returns (header row, first data row, last data row, {column name: column number})."""
    if index: df = df.reset_index()
    if caption: put(ws, r, c, caption, FS); r += 1
    cols = {}
    for j, h in enumerate(df.columns):
        put(ws, r, c + j, str(h), FH, hdr_fill, al=CEN, border=True); cols[h] = c + j
    for i, row in enumerate(df.itertuples(index=False)):
        for j, v in enumerate(row):
            if isinstance(v, (np.floating, float)) and not np.isfinite(v): v = None
            elif isinstance(v, np.integer): v = int(v)
            elif isinstance(v, np.floating): v = float(v)
            elif isinstance(v, (np.bool_, bool)): v = bool(v)
            fm = (fmts or {}).get(df.columns[j]) or numfmt(v)
            put(ws, r + 1 + i, c + j, v, fmt=fm, border=True, al=WR if wrap else None)
    if widths:
        for j, w in enumerate(widths): ws.column_dimensions[CL(c + j)].width = max(ws.column_dimensions[CL(c + j)].width or 0, w)
    return r, r + 1, r + len(df), cols
def card(ws, s, r=4):
    """Step card: the fixed rows every step sheet starts with."""
    put(ws, r, 1, 'Step %s – %s' % (s['code'], s['title']), Font(name=AR, size=12, bold=True, color='FFFFFF'), HF); ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=12); r += 1
    rows = [('Concept (what)', s['what']), ('Why (justification)', s['why']), ('Position in the analysis', s['position']), ('Samples used', s['samples']), ('Settings', s['settings']),
            ('What the papers did', '\n'.join('• %s: %s' % p for p in s['papers'])), ('How it was done with my data', '\n'.join('• ' + x for x in s['mydata'])), ('Result', '\n'.join('• ' + x for x in s['result'])),
            ('Output → next step', s['output']), ('Notes / alternatives', s['notes']), ('Interview question', s['q']),
            ('References', '; '.join([p[0] for p in s['papers']] + s['mrefs']) + ' (full list: sheet References)')]
    for lab, txt in rows:
        if not txt: continue
        put(ws, r, 1, lab, FB, LF, al=WR, border=True); put(ws, r, 2, txt, FN, al=WR, border=True); ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=12)
        n = sum(max(1, int(len(line) / 150) + 1) for line in str(txt).split('\n')); ws.row_dimensions[r].height = min(409, 14 * n + 2); r += 1
    ws.column_dimensions['A'].width = 24
    for j in range(2, 13): ws.column_dimensions[CL(j)].width = max(ws.column_dimensions[CL(j)].width or 0, 13)
    return r + 1
def chart(ws, sp, at, data_col, data_row=None, h=9.0, w=17.0):
    """Write the chart data at (data_row, data_col) of the same sheet and draw the native chart from those cells at cell `at`."""
    d = sp['data']; r0 = data_row
    put(ws, r0, data_col, 'Chart data – %s (%s). Edit these cells to change the chart.' % (sp['title'], sp['id']), FNOTE)
    hr, fr, lr, cols = table(ws, r0 + 1, data_col, d)
    xcol = data_col; kind = sp['kind']; ser = sp['series']; colors = dict(zip(ser, sp['colors']))
    if kind in ('line', 'scatter'):
        ch = ScatterChart(); ch.style = 2; xref = Reference(ws, min_col=xcol, min_row=fr, max_row=lr)
        for sname in ser:
            c = cols[sname]; s_ = Series(Reference(ws, min_col=c, min_row=hr, max_row=lr), xref, title_from_data=True); col = colors[sname]
            is_line = kind == 'line' or sname in sp.get('line_series', [])
            if is_line:
                s_.marker = Marker(symbol='circle' if sp.get('markers') else 'none', size=5); s_.smooth = False
                s_.graphicalProperties.line.solidFill = col; s_.graphicalProperties.line.width = 19050 if 'ellipse' not in sname else 12700
                if sname in ('Chance', '1:1 line'): s_.graphicalProperties.line.dashStyle = 'dash'
                if sp.get('markers'): s_.marker.graphicalProperties = None
            else:
                s_.marker = Marker(symbol='circle', size=4); s_.marker.graphicalProperties = None; s_.graphicalProperties.line.noFill = True
                from openpyxl.chart.shapes import GraphicalProperties
                gp = GraphicalProperties(solidFill=col); gp.line.solidFill = col; s_.marker.graphicalProperties = gp
            ch.series.append(s_)
        ch.display_blanks = 'gap'
    else:
        ch = BarChart(); ch.type = 'bar' if kind == 'bar' else 'col'; ch.grouping = 'clustered'; ch.overlap = -10 if len(ser) > 1 else 0; ch.gapWidth = 60
        cats = Reference(ws, min_col=xcol, min_row=fr, max_row=lr); bars = [x for x in ser if x not in sp.get('line_series', [])]
        for sname in bars:
            c = cols[sname]; s_ = Series(Reference(ws, min_col=c, min_row=hr, max_row=lr), title_from_data=True); s_.graphicalProperties.solidFill = colors[sname]; s_.graphicalProperties.line.solidFill = colors[sname]
            if sp.get('point_colors') and len(bars) == 1:
                for i, pc in enumerate(sp['point_colors']):
                    dp = DataPoint(idx=i); dp.graphicalProperties.solidFill = pc; dp.graphicalProperties.line.solidFill = pc; s_.dPt.append(dp)
            ch.series.append(s_)
        ch.set_categories(cats)
        if sp.get('labels'): ch.dataLabels = DataLabelList(); ch.dataLabels.showVal = True
        if sp.get('line_series'):
            lc = LineChart()
            for sname in sp['line_series']:
                c = cols[sname]; s_ = Series(Reference(ws, min_col=c, min_row=hr, max_row=lr), title_from_data=True); s_.graphicalProperties.line.solidFill = colors[sname]; s_.marker = Marker(symbol='circle', size=6); lc.series.append(s_)
            lc.set_categories(cats); ch += lc
    ch.title = sp['title']; ch.x_axis.title = sp['xlab'] if kind != 'bar' else None; ch.y_axis.title = sp['ylab']; ch.height = h; ch.width = w; ch.roundedCorners = False
    ch.x_axis.delete = False; ch.y_axis.delete = False; ch.legend.position = 'b'; ch.legend.overlay = False
    if len(ser) == 1 and not sp.get('line_series'): ch.legend = None
    if kind in ('line', 'scatter'):
        xs = pd.to_numeric(d.iloc[:, 0], errors='coerce'); ch.x_axis.scaling.min = float(np.floor(xs.min())) if xs.notna().any() else None; ch.x_axis.scaling.max = float(np.ceil(xs.max())) if xs.notna().any() else None
        ch.x_axis.majorGridlines = None
    ch.title.overlay = False if ch.title is not None and hasattr(ch.title, 'overlay') else None
    ws.add_chart(ch, at); return lr
def charts_block(ws, ids, r, data_col=15, h=9.0, w=17.0, gap=20):
    """Stack the charts of a sheet in columns A–M and their data side by side from column `data_col`."""
    dc = data_col
    for i, cid in enumerate(ids):
        if cid not in SPECS: continue
        sp = SPECS[cid]; put(ws, r, 1, 'Figure %s – %s' % (cid, sp['title']), FB)
        if sp['note']: put(ws, r + 1, 1, sp['note'], FNOTE)
        chart(ws, sp, 'A%d' % (r + 2), dc, data_row=r, h=h, w=w); dc += len(sp['data'].columns) + 1; r += gap
    return r
def link(ws, r, c, text, target):
    x = put(ws, r, c, text, FLINK); x.hyperlink = Hyperlink(ref=x.coordinate, location="'%s'!A1" % target); return x
# ======================================================================= sheets
ws = sheet('README', '1F3864'); r = title(ws, 'Part L analysis of the 2025-26 ASD leaf spectra – white rust of mustard (pooled over dates, stages, varieties and leaf positions)',
                                          'Methodology: White rust complete methodology 2026-27, Part L (Steps L1–L10). Data: 4 ASD FieldSpec files (11 Feb, 24 Feb, 3 Mar, 13 Mar 2026), natural infection, 48 plots.')
txt = ['How to use this workbook', 'Each step sheet (L1 … L9) starts with a step card: concept, justification, position in the analysis, samples used, settings, what the papers did, how it was done with my data, result, output, notes and references.',
       'Below the card are the result tables and the figures. Every figure is a native Excel chart drawn from the "Chart data" cells to the right of it (column O onwards): change a cell and the chart changes.',
       'Formula sheets (L5.1_Formulas, L7_Formulas) recompute key results from the raw cells with Excel formulas; the Checks sheet compares them with the Python results (PASS = agreement).',
       'Colours: dark-blue header = table header; light-blue cell = label; green = PASS; orange = check needed. Numbers in tables come from the Python scripts in thesis_build/asdL (l01_qc.py … l12_stability.py).',
       'Samples: training leaves (33 plots) are used for selection (L5.2–L5.6) and model fitting (L6); all leaves are used for description (L5.1, L5.7); the test leaves (15 plots) are predicted once (L7).']
for i, t in enumerate(txt): put(ws, r + i, 1, t, FS if i == 0 else FN)
r += len(txt) + 1; put(ws, r, 1, 'Contents', FS); r += 1
contents = [('Steps', 'Overview of all steps, samples, settings and outputs'), ('Leaf_table', 'One row per leaf: identifiers, grade, split, folds'), ('Data_R5', '5-nm smoothed reflectance of every leaf (401 bands)'),
            ('L1', 'Leaf table and checks'), ('L2', 'Split by plot and inner validation'), ('L3', 'Pre-processing'), ('L4', 'Index definitions'), ('L4_values', 'Index values of every leaf'), ('L5.1', 'Leaf response curves'),
            ('L5.1_Formulas', 'Mean spectra and r recomputed with formulas'), ('L5.2', 'R² maps, SHAP-CARS, optimal wavelengths'), ('L5.3', 'NDSI, RSI, WRI'), ('L5.4', 'Redundancy filter and ReliefF'), ('L5.5', 'VIF and DSF'),
            ('L5.6', 'Jeffries–Matusita distance'), ('L5.7', 'PCA'), ('L5_features', 'Selected features of every leaf'), ('L6', 'Models (SFFS, grid, networks, stability)'), ('L7', 'Test metrics'), ('L7_Predictions', 'Test predictions of every model'),
            ('L7_Formulas', 'Confusion matrices and metrics recomputed with formulas'), ('L8', 'Covariate baseline'), ('L9', 'Leaf–canopy link'), ('L10', 'Pre-symptomatic (not applicable)'), ('Checks', 'Cross-check of every step'), ('Findings', 'Main findings and comparison with the literature'),
            ('Deviations', 'Deviations from the methodology and why'), ('References', 'Full references')]
for i, (sh, d) in enumerate(contents): link(ws, r + i, 1, sh, sh); put(ws, r + i, 2, d)
ws.column_dimensions['A'].width = 22; ws.column_dimensions['B'].width = 110
# ---------------- Steps overview
ws = sheet('Steps', '1F3864'); r = title(ws, 'Overview of the Part L steps applied to the 2025-26 ASD leaf data', 'One row per step; click a step code to open its sheet.')
hdr = ['Step', 'Title', 'Position in the analysis', 'Samples used', 'Settings', 'Key result', 'Output → next step', 'References']
for j, h in enumerate(hdr): put(ws, r, j + 1, h, FH, HF, al=CEN, border=True)
for i, s in enumerate(STEPS):
    rr = r + 1 + i; x = link(ws, rr, 1, s['code'], s['sheet']) if s['sheet'] in [c[0] for c in contents] else put(ws, rr, 1, s['code']); x.border = BOX
    for j, v in enumerate([s['title'], s['position'], s['samples'], s['settings'], ' '.join(s['result']) or '—', s['output'], '; '.join([p[0] for p in s['papers']] + s['mrefs'])]): put(ws, rr, j + 2, v, al=WR, border=True)
    ws.row_dimensions[rr].height = 120
for j, wdt in enumerate([7, 26, 30, 26, 50, 45, 24, 34]): ws.column_dimensions[CL(j + 1)].width = wdt
ws.freeze_panes = 'C5'
# ---------------- Leaf table and spectra
lt = T['leaf_table'].copy(); ws = sheet('Leaf_table', '7F7F7F'); r = title(ws, 'Leaf table (Step L1–L2): one row per leaf', 'grade = leaf score on the 0–9 key; diseased = grade > 0; split = TRAIN/TEST by plot; nn_part = network fit/validation/test; inner_fold = GroupKFold(3) fold of training plots (0 = test).')
LT = table(ws, r, 1, lt, widths=[8, 11, 20, 6, 7, 8, 8, 11, 6, 13, 7, 7, 7, 9, 8, 7, 11, 10]); ws.freeze_panes = ws.cell(LT[1], 3)
LTC = {k: CL(v) for k, v in LT[3].items()}; LT1, LTN = LT[1], LT[2]; rngL = lambda col: "Leaf_table!$%s$%d:$%s$%d" % (LTC[col], LT1, LTC[col], LTN)
ws = sheet('Data_R5', '7F7F7F'); S3 = np.load(os.path.join(C.OUT, 'L3_spectra.npz')); w5 = S3['w5']; R5 = S3['R5']
put(ws, 1, 1, '5-nm smoothed reflectance (Savitzky–Golay 11/2, mean of λ ± 2 nm) of every leaf; row order = Leaf_table; first column = leaf_id, second = grade.', FNOTE)
put(ws, 2, 1, 'leaf_id', FH, HF); put(ws, 2, 2, 'grade', FH, HF)
for j, wv in enumerate(w5): put(ws, 2, 3 + j, int(wv), FH, HF)
for i in range(len(R5)):
    ws.cell(3 + i, 1, i); ws.cell(3 + i, 2, int(lt.grade.iloc[i]))
    for j in range(R5.shape[1]): ws.cell(3 + i, 3 + j, round(float(R5[i, j]), 6))
ws.freeze_panes = 'C3'; D1, DN = 3, 2 + len(R5)
# ---------------- L1
st = {s['code']: s for s in STEPS}
ws = sheet('L1', '2E75B6'); r = title(ws, 'Step L1 – Leaf table and data checks'); r = card(ws, st['L1'], r)
hr, fr, lr, _ = table(ws, r, 1, T['l1_flow'], 'Table L1.1 – Sample flow', widths=[48, 12]); r = lr + 2
hr, fr, lr, _ = table(ws, r, 1, T['l1_checks'], 'Table L1.2 – Data checks', widths=[24, 30, 30, 60, 10], wrap=True)
for k in range(fr, lr + 1): ws.cell(k, 5).fill = GF if ws.cell(k, 5).value == 'PASS' else RF
r = lr + 2; put(ws, r, 1, 'Table L1.3 – Leaves per grade and date (COUNTIFS formulas on Leaf_table)', FS); r += 1
dates = sorted(lt.date.unique()); put(ws, r, 1, 'Grade', FH, HF, border=True)
for j, d in enumerate(dates): put(ws, r, 2 + j, d, FH, HF, border=True)
put(ws, r, 2 + len(dates), 'Total', FH, HF, border=True)
for i, g in enumerate(C.GRADES):
    put(ws, r + 1 + i, 1, g, border=True)
    for j, d in enumerate(dates): put(ws, r + 1 + i, 2 + j, '=COUNTIFS(%s,$A%d,%s,%s$%d)' % (rngL('grade'), r + 1 + i, rngL('date'), CL(2 + j), r), border=True, fmt='0')
    put(ws, r + 1 + i, 2 + len(dates), '=SUM(%s%d:%s%d)' % (CL(2), r + 1 + i, CL(1 + len(dates)), r + 1 + i), FB, border=True, fmt='0')
put(ws, r + 7, 1, 'Total', FB, border=True)
for j in range(len(dates) + 1): put(ws, r + 7, 2 + j, '=SUM(%s%d:%s%d)' % (CL(2 + j), r + 1, CL(2 + j), r + 6), FB, border=True, fmt='0')
L1TOT = "'L1'!$%s$%d" % (CL(2 + len(dates)), r + 7); r += 9
for key, cap in (('l1_grade_leaf', 'Table L1.4 – Leaves per grade and leaf position'), ('l1_grade_stage', 'Table L1.5 – Leaves per grade and growth stage'), ('l1_grade_variety', 'Table L1.6 – Leaves per grade and variety'), ('l1_grade_sowing', 'Table L1.7 – Leaves per grade and sowing date')):
    hr, fr, lr, _ = table(ws, r, 1, T[key], cap); r = lr + 2
ifs = T['l1_if_summary'].pivot(index='grade', columns='date', values='flagged').fillna(0).astype(int).reset_index(); hr, fr, lr, _ = table(ws, r, 1, ifs, 'Table L1.8 – Isolation Forest flags per grade and date (checked, none faulty)'); r = lr + 2
r = charts_block(ws, ['c01', 'c02', 'c03', 'c04', 'c05'], r)
hr, fr, lr, _ = table(ws, r, 1, T['l1_dups'], 'Table L1.9 – Exact duplicate spectra removed'); r = lr + 2
hr, fr, lr, _ = table(ws, r, 1, T['l1_if'], 'Table L1.10 – All Isolation Forest flags (kept; reflectance within 0–1)'); r = lr + 2
# ---------------- L2
ws = sheet('L2', '2E75B6'); r = title(ws, 'Step L2 – Split by plot and inner validation'); r = card(ws, st['L2'], r)
put(ws, r, 1, 'Table L2.1 – Leaves in each part (COUNTIFS formulas on Leaf_table)', FS); r += 1
parts = [('TRAIN', 'split', 'TRAIN'), ('TEST', 'split', 'TEST'), ('Network fitting', 'nn_part', 'fit'), ('Network validation', 'nn_part', 'validation'), ('Fold 1', 'inner_fold', 1), ('Fold 2', 'inner_fold', 2), ('Fold 3', 'inner_fold', 3)]
for j, h in enumerate(['Part', 'Leaves'] + ['Grade %d' % g for g in C.GRADES] + ['% of all leaves']): put(ws, r, 1 + j, h, FH, HF, al=CEN, border=True)
for i, (lab, col, val) in enumerate(parts):
    rr = r + 1 + i; put(ws, rr, 1, lab, border=True); crit = '"%s"' % val if isinstance(val, str) else val
    put(ws, rr, 2, '=COUNTIFS(%s,%s)' % (rngL(col), crit), FB, border=True, fmt='0')
    for k, g in enumerate(C.GRADES): put(ws, rr, 3 + k, '=COUNTIFS(%s,%s,%s,%d)' % (rngL(col), crit, rngL('grade'), g), border=True, fmt='0')
    put(ws, rr, 9, '=B%d/%s' % (rr, L1TOT), border=True, fmt='0.0%')
L2R = r + 1; r += len(parts) + 2
hr, fr, lr, _ = table(ws, r, 1, T['l2_plots'], 'Table L2.2 – Plots: block, treatment, split, network part and inner fold', widths=[7, 7, 8, 8, 8, 13, 10, 8, 10, 13]); r = lr + 2
charts_block(ws, ['c06', 'c07', 'c07b'], r)
# ---------------- L3
ws = sheet('L3', '2E75B6'); r = title(ws, 'Step L3 – Pre-processing'); r = card(ws, st['L3'], r)
hr, fr, lr, _ = table(ws, r, 1, T['l3_summary'], 'Table L3.1 – Pre-processing summary', widths=[30, 50]); r = lr + 2
charts_block(ws, ['c08', 'c09', 'c10'], r)
# ---------------- L4
ws = sheet('L4', '2E75B6'); r = title(ws, 'Step L4 – Spectral indices and red-edge parameters'); r = card(ws, st['L4'], r)
hr, fr, lr, _ = table(ws, r, 1, T['l4_defs'], 'Table L4.1 – The 48 indices and 3 red-edge parameters (formula, original reference, r with grade on all leaves)', widths=[24, 12, 60, 34, 12], wrap=True)
ws2 = sheet('L4_values', '7F7F7F'); put(ws2, 1, 1, 'Index values of every leaf (Step L4, 1-nm smoothed spectra). Row order = Leaf_table.', FNOTE); IV = table(ws2, 2, 1, T['l4_values']); ws2.freeze_panes = 'G3'
IVC = {k: CL(v) for k, v in IV[3].items()}; IV1, IVN = IV[1], IV[2]
# ---------------- L5.1
ws = sheet('L5.1', '548235'); r = title(ws, 'Step L5.1 – Leaf response: mean spectra, differences and correlation'); r = card(ws, st['L5.1'], r)
it = T['l51_index_r'].copy(); hr, fr, lr, _ = table(ws, r, 1, it, 'Table L5.1.1 – Pearson r of the 51 indices with the leaf grade (all leaves), sorted by |r|', widths=[12, 9, 9, 24, 30]); r = lr + 2
hr, fr, lr, _ = table(ws, r, 1, T['l51_index_means'], 'Table L5.1.2 – Mean of every index for each grade'); r = lr + 2
hr, fr, lr, _ = table(ws, r, 1, T['l51_strata'], 'Table L5.1.3 – Strata: leaves, grade distribution, highest |r| and REP'); r = lr + 2
put(ws, r, 1, 'Full curves (mean ± SD per grade, % difference, r) are in the chart data of the figures below and in L5.1_Formulas.', FNOTE); r += 2
charts_block(ws, ['c11', 'c12', 'c13', 'c14', 'c15', 'c16', 'c17'], r)
# formulas: mean spectra and r recomputed from Data_R5
ws = sheet('L5.1_Formulas', '548235'); put(ws, 1, 1, 'Cross-check of Step L5.1: mean reflectance of each grade (AVERAGEIFS) and Pearson r with the grade (CORREL) computed by Excel from sheet Data_R5; Python values alongside.', FS)
hdr = ['Wavelength (nm)'] + ['Mean grade %d (Excel)' % g for g in C.GRADES] + ['r with grade (Excel)', 'Mean grade 0 (Python)', 'Mean grade 9 (Python)', 'r with grade (Python)', '|Excel − Python| max']
for j, h in enumerate(hdr): put(ws, 3, 1 + j, h, FH, HF, al=CEN, border=True)
sp = T['l51_spectra']; gcol = "Data_R5!$B$%d:$B$%d" % (D1, DN)
for i, wv in enumerate(w5):
    rr = 4 + i; col = CL(3 + i); rng = "Data_R5!$%s$%d:$%s$%d" % (col, D1, col, DN); put(ws, rr, 1, int(wv))
    for k, g in enumerate(C.GRADES): put(ws, rr, 2 + k, '=AVERAGEIFS(%s,%s,%d)' % (rng, gcol, g), fmt='0.00000')
    put(ws, rr, 8, '=CORREL(%s,%s)' % (rng, gcol), fmt='0.0000'); put(ws, rr, 9, float(sp.R_mean_g0[i]), fmt='0.00000'); put(ws, rr, 10, float(sp.R_mean_g9[i]), fmt='0.00000'); put(ws, rr, 11, float(sp.r_R[i]), fmt='0.0000')
    put(ws, rr, 12, '=MAX(ABS(B%d-I%d),ABS(G%d-J%d),ABS(H%d-K%d))' % (rr, rr, rr, rr, rr, rr), fmt='0.0E+00')
F51 = "'L5.1_Formulas'!$L$4:$L$%d" % (3 + len(w5))
for j in range(1, 13): ws.column_dimensions[CL(j)].width = 15
ws.freeze_panes = 'B4'
# ---------------- L5.2
ws = sheet('L5.2', '548235'); r = title(ws, 'Step L5.2 – Effective ranges and optimal wavelengths (R² maps → SHAP-CARS)'); r = card(ws, st['L5.2'], r)
hr, fr, lr, _ = table(ws, r, 1, T['l52_ranges'], 'Table L5.2.1 – Effective wavelength ranges (bands above the threshold in both R² maps)'); r = lr + 2
hr, fr, lr, owc = table(ws, r, 1, T['l52_ow'], 'Table L5.2.2 – The 32 optimal wavelengths (OW) with their SHAP importance'); OWR = (fr, lr, owc); r = lr + 2
hr, fr, lr, _ = table(ws, r, 1, T['l52_cars'][['iteration', 'n_bands', 'GKF_RMSE']], 'Table L5.2.3 – CARS iterations (bands kept, GroupKFold(3) RMSE); bands of each subset in L5.2 data below'); r = lr + 2
for nm, cap in (('l52_ndsi20', 'NDSI'), ('l52_rsi20', 'RSI')):
    A = T[nm]; put(ws, r, 1, 'Table – %s R² map with the grade on a 20-nm grid (row = λ1, column = λ2; colour scale = editable heat map; full 5-nm maps in the Word/PPT figures)' % cap, FS); r += 1
    put(ws, r, 1, 'λ1 \\ λ2', FH, HF)
    for j, wv in enumerate(A.columns): put(ws, r, 2 + j, int(wv), FH, HF)
    for i, wv in enumerate(A.index):
        put(ws, r + 1 + i, 1, int(wv), FB)
        for j in range(A.shape[1]):
            v = A.iat[i, j]; 
            if np.isfinite(v): ws.cell(r + 1 + i, 2 + j, round(float(v), 4)).number_format = '0.00'
    rng = '%s%d:%s%d' % (CL(2), r + 1, CL(1 + A.shape[1]), r + A.shape[0]); ws.conditional_formatting.add(rng, ColorScaleRule(start_type='num', start_value=0, start_color='440154', mid_type='percentile', mid_value=50, mid_color='21918C', end_type='max', end_color='FDE725'))
    for j in range(2, 2 + A.shape[1]): ws.column_dimensions[CL(j)].width = max(ws.column_dimensions[CL(j)].width or 0, 5)
    r += A.shape[0] + 3
charts_block(ws, ['c21', 'c22', 'c23', 'c24', 'c25'], r, data_col=110)
# ---------------- L5.3
ws = sheet('L5.3', '548235'); r = title(ws, 'Step L5.3 – Best NDSI, RSI and the White Rust Index'); r = card(ws, st['L5.3'], r)
hr, fr, lr, _ = table(ws, r, 1, T['l53_wri_w'], 'Table L5.3.1 – Best WRI combination for each weight w (λ3 blank when w = 0)'); r = lr + 2
hr, fr, lr, _ = table(ws, r, 1, T['l53_wri'], 'Table L5.3.2 – The 50 best WRI combinations of the search'); r = lr + 2
hr, fr, lr, _ = table(ws, r, 1, T['l53_by_grade'], 'Table L5.3.3 – Mean and SD of NDSI_best, RSI_best and WRI by grade (training leaves)'); r = lr + 2
charts_block(ws, ['c26', 'c27'], r)
# ---------------- L5.4
ws = sheet('L5.4', '548235'); r = title(ws, 'Step L5.4 – Redundancy filter and ReliefF ranking'); r = card(ws, st['L5.4'], r)
hr, fr, lr, _ = table(ws, r, 1, T['l54_clusters'], 'Table L5.4.1 – Indices kept after the |r| ≥ 0.95 filter and the indices each one replaced', widths=[14, 60, 10], wrap=True); r = lr + 2
hr, fr, lr, _ = table(ws, r, 1, T['l54_relief'], 'Table L5.4.2 – ReliefF (A, B) and RReliefF (C) weights of the kept indices'); r = lr + 2
hr, fr, lr, _ = table(ws, r, 1, T['l54_vi'], 'Table L5.4.3 – Leaf VI: top five indices per task'); r = lr + 2
charts_block(ws, ['c28a', 'c28b', 'c28c'], r)
# ---------------- L5.5
ws = sheet('L5.5', '548235'); r = title(ws, 'Step L5.5 – Variance inflation factor and the leaf DSF'); r = card(ws, st['L5.5'], r)
hr, fr, lr, _ = table(ws, r, 1, T['l55_dsf'], 'Table L5.5.1 – Leaf DSF of each task', widths=[8, 8, 8, 10, 90], wrap=True); r = lr + 2
hr, fr, lr, _ = table(ws, r, 1, T['l55_steps'], 'Table L5.5.2 – Removal order: the largest-VIF feature of every round (removed while ≥ 10)'); r = lr + 2
hr, fr, lr, _ = table(ws, r, 1, T['l55_final'], 'Table L5.5.3 – VIF of the final DSF features (all < 10)'); VIFR = (fr, lr, _['VIF']); r = lr + 2
charts_block(ws, ['c29'], r)
# ---------------- L5.6
ws = sheet('L5.6', '548235'); r = title(ws, 'Step L5.6 – Jeffries–Matusita distance between grades'); r = card(ws, st['L5.6'], r)
hr, fr, lr, _ = table(ws, r, 1, T['l56_matrix'].rename_axis('Grade').reset_index().rename(columns=lambda c: 'Grade %s' % c if c != 'Grade' else c), 'Table L5.6.1 – JM matrix (0 = identical, 2 = fully separable; colour scale)')
ws.conditional_formatting.add('B%d:G%d' % (fr, lr), ColorScaleRule(start_type='num', start_value=0, start_color='FFFFFF', end_type='num', end_value=2, end_color='C0392B')); JMR = "'L5.6'!$B$%d:$G$%d" % (fr, lr); r = lr + 2
hr, fr, lr, _ = table(ws, r, 1, T['l56_jm'], 'Table L5.6.2 – JM and Bhattacharyya distance of the 15 grade pairs'); r = lr + 2
charts_block(ws, ['c30'], r)
# ---------------- L5.7
ws = sheet('L5.7', '548235'); r = title(ws, 'Step L5.7 – Principal component analysis'); r = card(ws, st['L5.7'], r)
hr, fr, lr, _ = table(ws, r, 1, T['l57_var'], 'Table L5.7.1 – Variance explained'); PCV = "'L5.7'!$C$%d" % lr; r = lr + 2
hr, fr, lr, _ = table(ws, r, 1, T['l57_means'], 'Table L5.7.2 – Mean PC scores of each grade'); r = lr + 2
r = charts_block(ws, ['c18', 'c19', 'c20'], r)
put(ws, r, 1, 'PCA scores of all leaves', FS); table(ws, r + 1, 1, T['l57_scores'])
# ---------------- L5 features
ALLF = pd.read_csv(os.path.join(C.OUT, 'L5_all_features.csv')); cols = list(dict.fromkeys(F['OW'] + [c for t in 'ABC' for c in F['DSF'][t]] + ['NDSI_best', 'RSI_best', 'WRI'] + [v for t in 'ABC' for v in json.load(open(os.path.join(C.OUT, 'L5_selection.json')))['VI'][t]]))
ws = sheet('L5_features', '7F7F7F'); put(ws, 1, 1, 'Selected features of every leaf: 32 OW, the DSF of each task, NDSI_best, RSI_best, WRI and the VI (row order = Leaf_table).', FNOTE)
table(ws, 2, 1, pd.concat([lt[['leaf_id', 'plot', 'date', 'leaf', 'grade', 'split']], ALLF[cols].round(7)], axis=1)); ws.freeze_panes = 'G3'
# ---------------- L6
if 'L6' in st:
    ws = sheet('L6', 'C55A11'); r = title(ws, 'Step L6 – Leaf models: SFFS + grid search and networks'); r = card(ws, st['L6'], r)
    hr, fr, lr, _ = table(ws, r, 1, T['l6_ml'], 'Table L6.1 – ML models: SFFS features, inner-fold scores and best grid settings (score: macro-F1 for A, B; negative RMSE for C)', widths=[6, 9, 8, 7, 70, 9, 40, 9, 8], wrap=True); r = lr + 2
    if len(T.get('l6_dl', [])): hr, fr, lr, _ = table(ws, r, 1, T['l6_dl'], 'Table L6.2 – Networks: epochs run, best epoch and best validation score (OA; negative RMSE for task C)'); r = lr + 2
    if len(T.get('l6_stab_freq', [])): hr, fr, lr, _ = table(ws, r, 1, T['l6_stab_freq'], 'Table L6.3 – SFFS stability of the best ML model of each task: selection frequency of every DSF feature'); r = lr + 2
    r = charts_block(ws, ['c31a', 'c31b', 'c31c', 'c32a', 'c32b', 'c32c', 'c40a', 'c40b', 'c40c'], r)
    hr, fr, lr, _ = table(ws, r, 1, T['l6_paths'], 'Table L6.4 – SFFS path: best subset of each size (inner GroupKFold(3) score)', widths=[6, 9, 9, 9, 80]); r = lr + 2
# ---------------- L7
if 'L7' in st:
    R = T['l7_metrics']; ws = sheet('L7', 'C55A11'); r = title(ws, 'Step L7 – Test metrics (684 test leaves, computed once)'); r = card(ws, st['L7'], r)
    for t, cols_ in (('A', ['model', 'family', 'n', 'OA', 'kappa', 'macro_P', 'macro_R', 'macro_F1', 'sensitivity', 'specificity', 'balanced_acc', 'F1_healthy', 'F1_diseased', 'AUC', 'CI_low', 'CI_high']),
                     ('B', ['model', 'family', 'n', 'OA', 'kappa', 'macro_F1', 'within1', 'QWK'] + ['F1_g%d' % g for g in C.GRADES] + ['CI_low', 'CI_high']), ('C', ['model', 'family', 'n', 'R2', 'RMSE', 'MAE', 'RPD', 'bias', 'r', 'CI_low', 'CI_high'])):
        q = R[R.task == t][cols_]; hr, fr, lr, _ = table(ws, r, 1, q, 'Table L7.%s – %s (CI = 95%% interval of the main metric over 1000 resamples of whole test plots)' % ({'A': 1, 'B': 2, 'C': 3}[t], d2_specs.TASK[t])); r = lr + 2
    hr, fr, lr, _ = table(ws, r, 1, T['l7_low'], 'Table L7.4 – Low-severity check'); r = lr + 2
    q = T['l7_strata']; q = q[[m == F['best'][t] for t, m in zip(q.task, q.model)]]; hr, fr, lr, _ = table(ws, r, 1, q, 'Table L7.5 – Main metric of the best model of each task by leaf position, stage, date and variety'); r = lr + 2
    charts_block(ws, ['c33a', 'c33b', 'c33c', 'c34', 'c35', 'c36', 'c37', 'c38a', 'c38b', 'c38c', 'c39'], r)
    # predictions + formula sheet
    P7 = T['l7_pred']; ws = sheet('L7_Predictions', '7F7F7F'); put(ws, 1, 1, 'Test predictions of every model (one row per test leaf). Task A: 0 = healthy, 1 = diseased; Task B: class 0–5 = grade 0, 1, 3, 5, 7, 9; Task C: predicted grade (0–9).', FNOTE)
    PV = table(ws, 2, 1, P7); ws.freeze_panes = 'H3'; PVC = {k: CL(v) for k, v in PV[3].items()}; P1, PN = PV[1], PV[2]; rngP = lambda col: "L7_Predictions!$%s$%d:$%s$%d" % (PVC[col], P1, PVC[col], PN)
    ws = sheet('L7_Formulas', 'C55A11'); put(ws, 1, 1, 'Cross-check of Step L7: confusion matrices (COUNTIFS on L7_Predictions) and metrics recomputed with Excel formulas; the Python value and the difference are shown for every model.', FS)
    r = 3; XCHK = []
    for t in 'ABC':
        for m in [x for x in d2_specs.MODELS if '%s|%s' % (t, x) in P7.columns]:
            pc = '%s|%s' % (t, m); py = R[(R.task == t) & (R.model == m)].iloc[0]; put(ws, r, 1, '%s – %s' % (d2_specs.TASK[t], m), FS); r += 1
            if t in 'AB':
                K = 2 if t == 'A' else 6; oc = 'A observed' if t == 'A' else 'B observed class'; labs = ['Healthy', 'Diseased'] if t == 'A' else ['G%d' % g for g in C.GRADES]
                put(ws, r, 1, 'Observed \\ Predicted', FH, HF, border=True)
                for j in range(K): put(ws, r, 2 + j, labs[j], FH, HF, border=True)
                put(ws, r, 2 + K, 'Row total', FH, HF, border=True); top = r + 1
                for i in range(K):
                    put(ws, top + i, 1, labs[i], FB, LF, border=True)
                    for j in range(K): put(ws, top + i, 2 + j, '=COUNTIFS(%s,%d,%s,%d)' % (rngP(oc), i, rngP(pc), j), border=True, fmt='0')
                    put(ws, top + i, 2 + K, '=SUM(%s%d:%s%d)' % (CL(2), top + i, CL(1 + K), top + i), FB, border=True, fmt='0')
                bot = top + K; put(ws, bot, 1, 'Column total', FB, LF, border=True)
                for j in range(K + 1): put(ws, bot, 2 + j, '=SUM(%s%d:%s%d)' % (CL(2 + j), top, CL(2 + j), bot - 1), FB, border=True, fmt='0')
                Mr = '%s%d:%s%d' % (CL(2), top, CL(1 + K), bot - 1); N = '%s%d' % (CL(2 + K), bot); diag = '+'.join('%s%d' % (CL(2 + i), top + i) for i in range(K))
                mc = 4 + K; put(ws, top - 1, mc, 'Class', FH, HF, border=True); put(ws, top - 1, mc + 1, 'Precision', FH, HF, border=True); put(ws, top - 1, mc + 2, 'Recall', FH, HF, border=True); put(ws, top - 1, mc + 3, 'F1', FH, HF, border=True)
                for i in range(K):
                    rr = top + i; tp = '%s%d' % (CL(2 + i), top + i); put(ws, rr, mc, labs[i], border=True)
                    put(ws, rr, mc + 1, '=IFERROR(%s/%s%d,0)' % (tp, CL(2 + i), bot), border=True, fmt='0.000'); put(ws, rr, mc + 2, '=IFERROR(%s/%s%d,0)' % (tp, CL(2 + K), top + i), border=True, fmt='0.000')
                    put(ws, rr, mc + 3, '=IFERROR(2*%s%d*%s%d/(%s%d+%s%d),0)' % (CL(mc + 1), rr, CL(mc + 2), rr, CL(mc + 1), rr, CL(mc + 2), rr), border=True, fmt='0.000')
                rr = bot + 1; f1 = '%s%d:%s%d' % (CL(mc + 3), top, CL(mc + 3), bot - 1)
                pe = 'SUMPRODUCT(%s%d:%s%d,%s%d:%s%d)/%s^2' % (CL(2 + K), top, CL(2 + K), bot - 1, 'TRANSPOSE(' if False else '', 0, '', 0, N) if False else None
                rowt = ['%s%d' % (CL(2 + K), top + i) for i in range(K)]; colt = ['%s%d' % (CL(2 + i), bot) for i in range(K)]; pe = '(' + '+'.join('%s*%s' % (a, b) for a, b in zip(rowt, colt)) + ')/%s^2' % N
                items = [('OA', '=(%s)/%s' % (diag, N), py['OA']), ('kappa', '=((%s)/%s-%s)/(1-%s)' % (diag, N, pe, pe), py['kappa']), ('macro-F1', '=AVERAGE(%s)' % f1, py['macro_F1'])]
                if t == 'A':
                    items += [('sensitivity', '=C%d/D%d' % (top + 1, top + 1), py['sensitivity']), ('specificity', '=B%d/D%d' % (top, top), py['specificity'])]
                else:
                    near = '+'.join('%s%d' % (CL(2 + j), top + i) for i in range(K) for j in range(K) if abs(i - j) <= 1)
                    wO = '+'.join('%g*%s%d' % (((i - j) / (K - 1)) ** 2, CL(2 + j), top + i) for i in range(K) for j in range(K) if i != j)
                    wE = '+'.join('%g*%s*%s/%s' % (((i - j) / (K - 1)) ** 2, rowt[i], colt[j], N) for i in range(K) for j in range(K) if i != j)
                    items += [('within one grade', '=(%s)/%s' % (near, N), py['within1']), ('QWK', '=1-(%s)/(%s)' % (wO, wE), py['QWK'])]
            else:
                o, p = rngP('grade'), rngP(pc); top = r; bot = r; mc = 1
                items = [('R²', '=1-SUMXMY2(%s,%s)/DEVSQ(%s)' % (o, p, o), py['R2']), ('RMSE', '=SQRT(SUMXMY2(%s,%s)/COUNT(%s))' % (o, p, o), py['RMSE']), ('RPD', '=STDEV(%s)/SQRT(SUMXMY2(%s,%s)/COUNT(%s))' % (o, o, p, o), py['RPD']),
                         ('bias', '=AVERAGE(%s)-AVERAGE(%s)' % (p, o), py['bias'])]
            rr = bot + 2 if t in 'AB' else r; put(ws, rr, 1, 'Metric', FH, HF, border=True); put(ws, rr, 2, 'Excel formula', FH, HF, border=True); put(ws, rr, 3, 'Python', FH, HF, border=True); put(ws, rr, 4, '|difference|', FH, HF, border=True)
            for k, (nm, fml, pv) in enumerate(items):
                put(ws, rr + 1 + k, 1, nm, border=True); put(ws, rr + 1 + k, 2, fml, border=True, fmt='0.0000'); put(ws, rr + 1 + k, 3, float(pv), border=True, fmt='0.0000'); put(ws, rr + 1 + k, 4, '=ABS(B%d-C%d)' % (rr + 1 + k, rr + 1 + k), border=True, fmt='0.0E+00')
                XCHK.append("'L7_Formulas'!$D$%d" % (rr + 1 + k))
            r = rr + len(items) + 3
    for j in range(1, 16): ws.column_dimensions[CL(j)].width = 13
    ws.column_dimensions['A'].width = 22
# ---------------- L8
if 'L8' in st:
    ws = sheet('L8', 'C55A11'); r = title(ws, 'Step L8 – Leaf covariate baseline'); r = card(ws, st['L8'], r)
    m = T['l8_models']; put(ws, r, 1, 'Table L8.1 – M0, M1, M2 and gains (ΔS = M1 − M0 and ΔC = M2 − M1 are Excel formulas)', FS); r += 1
    for j, h in enumerate(['Task', 'Main metric', 'M0 covariates (RF)', 'M1 model', 'M1 leaf spectrum', 'M2 spectrum + covariates', 'ΔS = M1 − M0', 'ΔC = M2 − M1', 'M2 features (after SFFS)', 'Top covariates in M0']): put(ws, r, 1 + j, h, FH, HF, al=CEN, border=True)
    for i, x in enumerate(m.itertuples()):
        rr = r + 1 + i
        for j, v in enumerate([d2_specs.TASK[x.task], x.metric, float(x.M0), x.M1_model, float(x.M1), float(x.M2)]): put(ws, rr, 1 + j, v, border=True, fmt='0.000' if isinstance(v, float) else None)
        put(ws, rr, 7, '=E%d-C%d' % (rr, rr), FB, border=True, fmt='+0.000;-0.000'); put(ws, rr, 8, '=F%d-E%d' % (rr, rr), FB, border=True, fmt='+0.000;-0.000'); put(ws, rr, 9, x.M2_features, border=True, al=WR); put(ws, rr, 10, x.top_covariates, border=True, al=WR)
        ws.row_dimensions[rr].height = 45
    for j, wdt in enumerate([30, 10, 12, 12, 12, 14, 12, 12, 50, 50]): ws.column_dimensions[CL(1 + j)].width = wdt
    r += len(m) + 2
    hr, fr, lr, _ = table(ws, r, 1, T['l8_gains'], 'Table L8.2 – Gains with plot-bootstrap 95% CI (all test leaves) and per date for task A'); r = lr + 2
    hr, fr, lr, _ = table(ws, r, 1, T['l8_weather'], 'Table L8.3 – Weather covariates: 7-day window ending the day before sampling, favourable days since sowing (per date × sowing date)'); r = lr + 2
    if 'l8_imp' in T: hr, fr, lr, _ = table(ws, r, 1, T['l8_imp'], 'Table L8.4 – Covariate importance in M0'); r = lr + 2
    charts_block(ws, ['c41', 'c42', 'c43'], r)
# ---------------- L9
if 'L9' in st:
    ws = sheet('L9', 'C55A11'); r = title(ws, 'Step L9 – Leaf–canopy link (UAV hyperspectral plot spectra, 24 Feb 2026)'); r = card(ws, st['L9'], r)
    hr, fr, lr, _ = table(ws, r, 1, T['l9_transfer'], 'Table L9.1 – Leaf indices computed from the UAV spectra: r with plot DI and detection of the test plots'); r = lr + 2
    p9 = T['l9_plots']; hr, fr, lr, cols9 = table(ws, r, 1, p9, 'Table L9.2 – Plots: DI on 24 Feb (Σgrade/(9n) × 100), UAV and leaf index values'); P9 = (fr, lr, cols9); r = lr + 2
    put(ws, r, 1, 'Check: r(UAV WRI, DI) by Excel formula', FB); put(ws, r, 4, '=CORREL(%s%d:%s%d,%s%d:%s%d)' % (CL(cols9['UAV_WRI']), fr, CL(cols9['UAV_WRI']), lr, CL(cols9['DI']), fr, CL(cols9['DI']), lr), FB, fmt='0.000'); L9X = "'L9'!$D$%d" % r; r += 2
    charts_block(ws, ['c44', 'c45', 'c46', 'c47'], r)
ws = sheet('L10', 'C55A11'); r = title(ws, 'Step L10 – Pre-symptomatic leaves'); card(ws, st['L10'], r)
# ---------------- Checks
ws = sheet('Checks', '00B050'); r = title(ws, 'Cross-check of every step (formulas compare the workbook cells with the expected values; PASS when they agree)')
for j, h in enumerate(['Step', 'Check', 'Value (formula)', 'Expected', 'Status']): put(ws, r, 1 + j, h, FH, HF, border=True)
CK = [('L1', 'Leaves in the leaf table', '=COUNTA(%s)' % rngL('leaf_id'), F['n_final']), ('L1', 'Sum of the grade × date table (formulas)', '=%s' % L1TOT, F['n_final']),
      ('L1', 'Healthy-block leaves with grade > 0', '=COUNTIFS(%s,"C",%s,">0")' % (rngL('block'), rngL('grade')), 0), ('L1', 'Grades other than 0, 1, 3, 5, 7, 9', '=COUNTA(%s)-SUM(COUNTIFS(%s,{0,1,3,5,7,9}))' % (rngL('grade'), rngL('grade')), 0),
      ('L2', 'Training + test leaves = all leaves', "='L2'!B%d+'L2'!B%d" % (L2R, L2R + 1), F['n_final']), ('L2', 'Network fitting + validation = training leaves', "='L2'!B%d+'L2'!B%d" % (L2R + 2, L2R + 3), F['n_train']),
      ('L2', 'Leaves of test plots labelled TRAIN', '=SUMPRODUCT(COUNTIFS(%s,{%s},%s,"TRAIN"))' % (rngL('plot'), ','.join(str(p) for p in C.TEST_PLOTS), rngL('split')), 0),
      ('L2', 'Validation-plot leaves outside the training part', '=COUNTIFS(%s,"validation",%s,"TEST")' % (rngL('nn_part'), rngL('split')), 0), ('L2', 'Fold 1 + 2 + 3 = training leaves', "='L2'!B%d+'L2'!B%d+'L2'!B%d" % (L2R + 4, L2R + 5, L2R + 6), F['n_train']),
      ('L2', 'Test share of all leaves (%)', "=ROUND(100*'L2'!B%d/%s,1)" % (L2R + 1, L1TOT), round(100 * F['n_test'] / F['n_final'], 1)),
      ('L4', 'Index values: rows = leaves', '=COUNTA(L4_values!$A$%d:$A$%d)' % (IV1, IVN), F['n_final']),
      ('L5.1', 'Mean spectra and r: max |Excel − Python| < 1e-5', '=IF(MAX(%s)<0.00001,0,1)' % F51, 0),
      ('L5.2', 'Optimal wavelengths in Table L5.2.2', "=COUNTA('L5.2'!A%d:A%d)" % (OWR[0], OWR[1]), 32), ('L5.2', 'First-derivative OW inside the 995–1005 nm guard', "=COUNTIFS('L5.2'!%s%d:%s%d,\"First derivative\",'L5.2'!%s%d:%s%d,\">=995\",'L5.2'!%s%d:%s%d,\"<=1005\")" % (CL(OWR[2]['Type']), OWR[0], CL(OWR[2]['Type']), OWR[1], CL(OWR[2]['Wavelength']), OWR[0], CL(OWR[2]['Wavelength']), OWR[1], CL(OWR[2]['Wavelength']), OWR[0], CL(OWR[2]['Wavelength']), OWR[1]), 0),
      ('L5.5', 'Largest VIF of the final DSF features < 10', "=IF(MAX('L5.5'!%s%d:%s%d)<10,0,1)" % (CL(VIFR[2]), VIFR[0], CL(VIFR[2]), VIFR[1]), 0),
      ('L5.6', 'JM values within 0–2', '=IF(AND(MIN(%s)>=0,MAX(%s)<=2),0,1)' % (JMR, JMR), 0), ('L5.7', 'Cumulative variance of 10 PCs ≤ 100%', '=IF(%s<=100.0001,0,1)' % PCV, 0)]
if 'L7' in st:
    CK += [('L7', 'Test leaves in the prediction sheet', '=COUNTA(%s)' % rngP('leaf_id'), F['n_test']), ('L7', 'Metrics: max |Excel formula − Python| < 1e-6 (all models)', '=IF(MAX(%s)<0.000001,0,1)' % ','.join(XCHK), 0)]
    R = T['l7_metrics']; inside = int(((R.CI_low <= R[[{'A': 'macro_F1', 'B': 'macro_F1', 'C': 'R2'}[t] for t in R.task]].values.diagonal()) & (R[[{'A': 'macro_F1', 'B': 'macro_F1', 'C': 'R2'}[t] for t in R.task]].values.diagonal() <= R.CI_high)).sum())
    CK += [('L7', 'Point estimate inside its bootstrap CI (models)', '=%d' % inside, len(R))]
if 'L9' in st: CK += [('L9', 'r(UAV WRI, DI): Excel CORREL vs Python', '=ROUND(%s,6)' % L9X, round(float(T['l9_transfer'].set_index('feature').loc['WRI', 'r_UAV_vs_DI_all48']), 6))]
for i, (s_, c_, f_, e_) in enumerate(CK):
    rr = r + 1 + i; put(ws, rr, 1, s_, border=True); put(ws, rr, 2, c_, border=True); put(ws, rr, 3, f_, border=True); put(ws, rr, 4, e_, border=True); put(ws, rr, 5, '=IF(ABS(C%d-D%d)<0.0000011,"PASS","CHECK")' % (rr, rr), FB, border=True)
from openpyxl.formatting.rule import CellIsRule
ws.conditional_formatting.add('E%d:E%d' % (r + 1, r + len(CK)), CellIsRule(operator='equal', formula=['"PASS"'], fill=GF)); ws.conditional_formatting.add('E%d:E%d' % (r + 1, r + len(CK)), CellIsRule(operator='equal', formula=['"CHECK"'], fill=RF))
for j, wdt in enumerate([8, 60, 16, 12, 10]): ws.column_dimensions[CL(1 + j)].width = wdt
r += len(CK) + 2; put(ws, r, 1, 'Checks done in the Python scripts (see sheet L1 Table L1.2 and the run logs):', FS)
more = ['L1: one spectrum per leaf; 2151 bands 350–2500 nm; no missing values; variety agrees with the plot plan; all 48 plots on every date.', 'L3: smoothing residual SD 0.00018; all 51 index values finite.',
        'L5.2–L5.6: selection uses training leaves only (split == TRAIN); CARS subset chosen by GroupKFold(3) RMSE; WRI search repeated and the best combination confirmed (l06b_wri.py).',
        'L5.4: no two kept indices have |r| ≥ 0.95.', 'L6: SFFS features are a subset of the task DSF; scalers are fitted on training leaves only (inside pipelines); network scaling uses the fitting leaves only.',
        'L7: each test leaf predicted once per model; bootstrap resamples whole plots (healthy and unsprayed separately).', 'L8: weather window ends the day before sampling (no look-ahead).']
for i, t in enumerate(more): put(ws, r + 1 + i, 1, '• ' + t)
# ---------------- Findings and literature
ws = sheet('Findings', '00B050'); r = title(ws, 'Main findings and comparison with the disease papers of the methodology')
fnd = [x for c in ('L5.1', 'L5.2', 'L5.3', 'L5.4', 'L5.6', 'L7', 'L8', 'L9') if c in st for x in (st[c]['result'] if c not in ('L5.3', 'L8') else st[c]['mydata'][-1:] if c == 'L5.3' else st[c]['mydata'])]
put(ws, r, 1, 'Main findings', FS); r += 1
for i, t in enumerate(fnd): put(ws, r + i, 1, '• ' + t, al=WR); ws.merge_cells(start_row=r + i, start_column=1, end_row=r + i, end_column=4); ws.row_dimensions[r + i].height = 30
r += len(fnd) + 1; LIT = d0_text.literature(T, F); put(ws, r, 1, 'Comparison with the literature', FS); r += 1
for j, h in enumerate(LIT[0]): put(ws, r, 1 + j, h, FH, HF, border=True)
for i, row in enumerate(LIT[1:]):
    for j, v in enumerate(row): put(ws, r + 1 + i, 1 + j, v, al=WR, border=True)
    ws.row_dimensions[r + 1 + i].height = 48
for j, wdt in enumerate([26, 50, 50, 50]): ws.column_dimensions[CL(1 + j)].width = wdt
# ---------------- Deviations
ws = sheet('Deviations', 'FFC000'); r = title(ws, 'Deviations from the methodology and adaptations to the 2025-26 data')
dev = [('DEV-1', 'L1/L5.2', 'Splice correction assumed done by the instrument software', 'Residual step −0.0021 at 1000/1001 nm found', 'Not corrected (methodology); FD bands 995–1005 nm excluded from band selection', 'Prevents a detector artefact from being selected as a disease band'),
       ('DEV-2', 'L1', 'Average the 2 readings of each leaf', 'Files contain one spectrum per leaf (instrument average)', 'Not applicable', '—'),
       ('DEV-3', 'L2', 'Leaf counts of the 2026-27 plan (5148 / 2340)', '2025-26: 1571 training / 684 test leaves', 'Same plot split applied', 'Same plots as the 2026-27 plan'),
       ('DEV-4', 'L5.3', 'WRI = NDSI + w·R(λ3)', 'Best weight w = 0', 'WRI reported as NDSI(780, 830); λ3 not used', 'The search itself chose w = 0 (best |r|)'),
       ('DEV-5', 'L7', 'Low-severity check on DI ≤ 5 / ≤ 10 (canopy)', 'Leaf data', 'Grade-1 leaves (Task A recall) and grades 0–1 (Task C RMSE)', 'Leaf-level equivalent'),
       ('DEV-6', 'L6', 'SFFS stability over 100 divisions', 'Run time', '50 random GroupKFold(3) divisions for the SVM models (tasks A, B); 20 divisions with 100 trees for the RF model (task C)', 'Keeps the check feasible on 4 CPU cores'),
       ('DEV-7', 'L9', 'Leaf vs canopy OW overlap; centre-plant leaves', 'One UAV date, no canopy selection; leaves of the whole plot', 'Overlap not computed; plot-mean leaf spectra used', 'Only data available for 2025-26'),
       ('DEV-8', 'L10', 'Pre-symptomatic leaves', 'No tagged pre-symptomatic leaves in 2025-26', 'Not run', 'Planned for 2026-27'),
       ('DEV-9', 'L6–L8', 'Task C predictions', 'Predictions outside 0–9', 'Clipped to 0–9', 'Grade scale limits')]
for j, h in enumerate(['Code', 'Step', 'Methodology', 'Situation in 2025-26', 'What was done', 'Why']): put(ws, r, 1 + j, h, FH, HF, border=True)
for i, row in enumerate(dev):
    for j, v in enumerate(row): put(ws, r + 1 + i, 1 + j, v, al=WR, border=True)
    ws.row_dimensions[r + 1 + i].height = 45
for j, wdt in enumerate([8, 8, 36, 36, 40, 36]): ws.column_dimensions[CL(1 + j)].width = wdt
# ---------------- References
ws = sheet('References', '7030A0'); r = title(ws, 'References (disease-sensing papers of each step and method references)')
alltext = ' '.join(' '.join([p[0] for p in s['papers']] + s['mrefs']) for s in STEPS) + ' ' + ' '.join(T['l4_defs'].Reference.str.replace(r' (\d{4})', r' (\1)', regex=True))
RL, MISS = refs.resolve(alltext + ' Conn et al. (1990) Selvaprakash et al. (2026)')
for i, x in enumerate(RL): put(ws, r + i, 1, x, al=WR); ws.row_dimensions[r + i].height = 28
ws.column_dimensions['A'].width = 160
if MISS: put(ws, r + len(RL) + 1, 1, 'Original index references not in the reference pool (cited as in the methodology index table): ' + ', '.join(MISS), FNOTE)
order = ['README', 'Steps', 'L1', 'L2', 'L3', 'L4', 'L5.1', 'L5.2', 'L5.3', 'L5.4', 'L5.5', 'L5.6', 'L5.7', 'L6', 'L7', 'L8', 'L9', 'L10', 'Checks', 'Findings', 'Deviations', 'References', 'L5.1_Formulas', 'L7_Formulas', 'Leaf_table', 'Data_R5', 'L4_values', 'L5_features', 'L7_Predictions']
wb._sheets = [wb[s] for s in order if s in wb.sheetnames] + [s for s in wb._sheets if s.title not in order]
wb.save(OUTX); print('saved', OUTX, len(wb.sheetnames), 'sheets; references', len(RL), 'missing', MISS)
