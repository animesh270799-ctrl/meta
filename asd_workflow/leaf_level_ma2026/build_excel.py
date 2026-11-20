"""Step-by-step Excel workbook (native, editable charts) - paper-faithful leaf-level analysis."""
import pickle, sys
import numpy as np, pandas as pd
from openpyxl import Workbook
from openpyxl.chart import ScatterChart, BarChart, Reference, Series
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.utils import get_column_letter
from sklearn.metrics import confusion_matrix

O = pickle.load(open(sys.argv[1], "rb"))
meta = O["meta"]; LN = O["level_names"]; bins = O["bins"]; ff = O["final_feats"]
SETS = ["RFE-RF", "SAND", "CARS-PLS", "VIs (Relief top 5)", "Full wavelength (350-2500 nm)", "OWs+VIs"]
MODELS = ["RF", "SVM", "PLS-DA", "MLP"]
DN = {"110226": "11 Feb 2026", "240226": "24 Feb 2026", "030326": "03 Mar 2026", "130326": "13 Mar 2026"}
wb = Workbook()
HFILL = PatternFill("solid", fgColor="1F6F78"); HFONT = Font(bold=True, color="FFFFFF"); TFONT = Font(bold=True, size=14, color="1F6F78")
thin = Side(style="thin", color="B7C4C8"); BORDER = Border(top=thin, bottom=thin, left=thin, right=thin)
COLORS = ["2E7D32", "9E9E9E", "E0B000", "1F5FD1", "D62728", "6B4C8A"]
MCOL = ["1F6F78", "B7791F", "6B4C8A", "B24A3F"]

def sheet(name, title, purpose):
    ws = wb.create_sheet(name); ws["A1"] = title; ws["A1"].font = TFONT
    ws["A2"] = purpose; ws["A2"].alignment = Alignment(wrap_text=True, vertical="top"); ws.merge_cells("A2:L3"); ws.row_dimensions[2].height = 32
    return ws

def table(ws, df, r0, c0=1, index=True, fmt=None, title=None):
    if title: ws.cell(r0, c0, title).font = Font(bold=True, color="1F6F78"); r0 += 1
    cols = ([df.index.name or ""] if index else []) + [str(c) for c in df.columns]
    for j, c in enumerate(cols):
        cell = ws.cell(r0, c0 + j, c); cell.fill = HFILL; cell.font = HFONT; cell.border = BORDER
        cell.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
    for i, (ix, row) in enumerate(df.iterrows()):
        for j, v in enumerate(([ix] if index else []) + list(row.values)):
            if isinstance(v, (float, np.floating)) and np.isnan(v): v = None
            elif isinstance(v, np.generic): v = v.item()
            cell = ws.cell(r0 + 1 + i, c0 + j, v); cell.border = BORDER
            if fmt and isinstance(v, float): cell.number_format = fmt
    return r0, r0 + len(df)

def scatter(ws, title, xt, yt, xref, yrefs, names, anchor, w=24, h=12, xmin=None, xmax=None, ymin=None, colors=COLORS):
    ch = ScatterChart(); ch.title = title; ch.style = 13; ch.x_axis.title = xt; ch.y_axis.title = yt; ch.width, ch.height = w, h; ch.legend.position = "b"
    for k, (yr, nm) in enumerate(zip(yrefs, names)):
        s = Series(yr, xref, title=nm); s.marker.symbol = "none"; s.smooth = False
        s.graphicalProperties.line.solidFill = colors[k % len(colors)]; s.graphicalProperties.line.width = 20000; ch.series.append(s)
    if xmin is not None: ch.x_axis.scaling.min = xmin
    if xmax is not None: ch.x_axis.scaling.max = xmax
    if ymin is not None: ch.y_axis.scaling.min = ymin
    ch.x_axis.delete = False; ch.y_axis.delete = False; ws.add_chart(ch, anchor); return ch

def bar(ws, title, yt, data_ref, cats_ref, anchor, w=24, h=11, grouping="clustered", colors=None, horizontal=False):
    ch = BarChart(); ch.type = "bar" if horizontal else "col"; ch.grouping = grouping; ch.title = title; ch.style = 10
    if grouping == "stacked": ch.overlap = 100
    ch.y_axis.title = yt; ch.width, ch.height = w, h; ch.legend.position = "b"
    ch.add_data(data_ref, titles_from_data=True); ch.set_categories(cats_ref)
    for k, s in enumerate(ch.series): s.graphicalProperties.solidFill = (colors or COLORS)[k % len(colors or COLORS)]
    ch.x_axis.delete = False; ch.y_axis.delete = False; ws.add_chart(ch, anchor); return ch

def cscale(ws, rng, start="FFFFFF", mid=None, end="1F6F78"):
    rule = (ColorScaleRule(start_type="min", start_color=start, mid_type="percentile", mid_value=50, mid_color=mid, end_type="max", end_color=end) if mid
            else ColorScaleRule(start_type="min", start_color=start, end_type="max", end_color=end))
    ws.conditional_formatting.add(rng, rule)

def widths(ws, w=12, first=18):
    ws.column_dimensions["A"].width = first
    for j in range(2, 40): ws.column_dimensions[get_column_letter(j)].width = w

# README
ws = wb.active; ws.title = "README"
ws["A1"] = "Leaf-level white rust analysis of ASD contact-probe spectra, following Ma et al. (2026)"; ws["A1"].font = Font(bold=True, size=16, color="1F6F78")
ws["A2"] = "Ma, J., Wu, P., Guo, S., Lin, Y., Yu, F., Liu, T. (2026). Early detection of rice blast disease using a dual transformer network (DT-EDNet) based on hyperspectral imaging and multi-feature fusion. IAENG Int. J. Applied Mathematics 56(11), 5380-5398."
ws["A3"] = "Unit = one leaf; label = that leaf's white rust score. Whole range 350-2500 nm (water bands kept: contact probe). Texture features and TTFI are not used (non-imaging data). Charts are native Excel charts linked to the tables."
steps = pd.DataFrame([
    ["S01_Data", "1", "Dates, leaves, plots, varieties, growth stages, leaf positions", "Study area / Table I"],
    ["S02_Labels", "2", "Leaf score -> 5 severity levels; samples per level, date and split", "Tables II-IV"],
    ["S03_Preprocessing", "3", "Duplicates, quality checks, splice correction, Savitzky-Golay smoothing, 10-nm bands", "Section II-B"],
    ["S04_Spectral_curves", "4", "Mean reflectance per severity level and date (whole range + 450-1000 nm zoom)", "Fig. 6"],
    ["S05_NDSI_R2 / S05b_RSI_R2", "5", "R2 of all band-pair NDSI and RSI with leaf score; effective ranges", "Fig. 7"],
    ["S06_Band_selection", "6", "RFE-RF, SAND and CARS-PLS on effective-range bands; SAND weights; CARS curve; stability across folds", "Table VII, Fig. 8"],
    ["S07_Vegetation_indices", "7", "16 indices + PSRI: formula, r with leaf score, Relief weight, top 5", "Tables V, VIII; Fig. 10a"],
    ["S08_VI_correlation", "7b", "Correlation among indices", "Fig. 9"],
    ["S09_Internal_validation", "8-9", "4 classifiers x 6 inputs; 5-fold CV grouped by plot (11 Feb, 24 Feb, 3 Mar)", "Tables X-XII, Fig. 12-13"],
    ["S10_Independent_test", "10", "Trained on 3 dates, tested on 13 Mar", "Table XIII, Fig. 14"],
    ["S11_Confusion", "11", "Confusion matrices of the best model", "-"],
    ["S12_Leaf_dataset", "Data", "One row per leaf: metadata, label, 17 VIs, 10-nm reflectance 355-2495 nm", "-"]],
    columns=["Sheet", "Step", "Content", "Paper item"])
table(ws, steps, 5, index=False)
for c, w in zip("ABCD", (28, 7, 90, 26)): ws.column_dimensions[c].width = w

# S01
ws = sheet("S01_Data", "Step 1 - Data inventory", "ASD FieldSpec contact probe, 48 plots (36 inoculated, 12 healthy), 3 varieties; one spectrum per leaf, 5 plants x 3 leaf positions per plot on most dates. 75 duplicated spectra on 13 Mar removed (columns repeated after a second header).")
inv = meta.groupby("date").agg(Leaves=("score", "size"), Plots=("plot", "nunique")).reindex(list(DN)); inv.index = list(DN.values()); inv.index.name = "Date"
for col, vals in (("variety", ["V1", "V2", "V3"]), ("treatment", ["Healthy", "Diseased"]), ("leaf", ["L3", "L4", "L5", "LL"])):
    ct = pd.crosstab(meta.date, meta[col]).reindex(index=list(DN), columns=vals, fill_value=0)
    for v in vals: inv[f"{col}: {v}"] = ct[v].values
st = pd.crosstab(meta.date, meta.stage).reindex(list(DN)).fillna(0).astype(int)
for c in st.columns: inv[f"stage: {c}"] = st[c].values
inv["Role"] = ["Training", "Training", "Training", "Independent test"]
h, last = table(ws, inv, 5); widths(ws, 11, 14)
bar(ws, "Leaves per date and treatment", "Leaves", Reference(ws, min_col=7, max_col=8, min_row=h, max_row=last), Reference(ws, min_col=1, min_row=h + 1, max_row=last), "B12", w=16, h=9, grouping="stacked")

# S02
ws = sheet("S02_Labels", "Step 2 - Leaf severity levels (paper Tables II-IV)", "Each leaf scored 0, 1, 3, 5, 7 or 9; grouped into five levels like the paper's Levels 0-4 (7 and 9 merged because 9 is rare). The label is the leaf's own score; inoculated leaves without pustules are L0.")
mp = pd.DataFrame({"Level": ["L0", "L1", "L2", "L3", "L4", "L4"], "Severity": ["Healthy", "Mild", "Moderate", "Severe", "Very severe", "Very severe"]}, index=pd.Index([0, 1, 3, 5, 7, 9], name="Leaf score"))
h0, l0 = table(ws, mp, 5)
cnt = pd.crosstab(meta.date, meta.level).reindex(index=list(DN), columns=range(5), fill_value=0); cnt.index = list(DN.values()); cnt.index.name = "Date"; cnt.columns = LN
cnt["Total"] = cnt.sum(1); cnt.loc["Total"] = cnt.sum()
h1, l1 = table(ws, cnt, l0 + 3, title="Table 2.1 Leaves per level and date (paper Table IV analogue)")
tr = meta.date != "130326"
sp = pd.DataFrame({"Training (11 Feb, 24 Feb, 3 Mar)": meta[tr].level.value_counts().reindex(range(5), fill_value=0).values,
                   "Independent test (13 Mar)": meta[~tr].level.value_counts().reindex(range(5), fill_value=0).values}, index=pd.Index(LN, name="Level"))
sp.loc["Total"] = sp.sum(); h2, l2 = table(ws, sp, l1 + 3, title="Table 2.2 Training / test split")
lp = pd.crosstab(meta.leaf, meta.level); lp.columns = LN; lp.index.name = "Leaf position"
table(ws, lp, l2 + 3, title="Table 2.3 Leaves per leaf position and level")
widths(ws, 15, 22)
bar(ws, "Leaves per level and date", "Leaves", Reference(ws, min_col=2, max_col=6, min_row=h1, max_row=h1 + 4), Reference(ws, min_col=1, min_row=h1 + 1, max_row=h1 + 4), "J5", w=20, h=10, grouping="stacked")

# S03
ws = sheet("S03_Preprocessing", "Step 3 - Quality control and pre-processing", "Duplicates removed -> physical checks -> splice correction (1000/1800 nm) -> Savitzky-Golay smoothing (window 11, order 2; as in the paper) -> whole range 350-2500 nm kept -> 10-nm band means for selection and modelling.")
qc = O["qc"]; s1, s2 = O["splice"]["step1000"], O["splice"]["step1800"]
q = pd.DataFrame([["Spectra in files", 2339, ""], ["Duplicate spectra removed (13 Mar)", 75, "Same 5 plots repeated"], ["Leaves analysed", len(meta), "One spectrum = one leaf"],
                  ["Reflectance outside 0-1", int(qc.out_of_range.sum()), "All physically valid"], ["NIR (800-900 nm) < 0.30", int(qc.low_nir.sum()), "Flagged, kept (severely diseased leaves)"],
                  ["Red >= green", int(qc.red_ge_green.sum()), "Flagged, kept"], ["Mean |splice step| at 1000 nm", float(np.abs(s1).mean()), "Corrected"],
                  ["Mean |splice step| at 1800 nm", float(np.abs(s2).mean()), "Corrected"], ["Smoothing", "SG 11 / 2", "Savitzky-Golay window 11 nm, order 2"],
                  ["Spectral range", "350-2500 nm (whole)", "Water-absorption regions kept: contact probe has its own light source"],
                  ["Bands for modelling", len(bins), "10-nm means, centres 355-2495 nm"]], columns=["Item", "Value", "Note"]).set_index("Item")
table(ws, q, 5, fmt="0.0000")
for c, w in zip("ABC", (38, 24, 66)): ws.column_dimensions[c].width = w

# S04
ws = sheet("S04_Spectral_curves", "Step 4 - Mean spectra by severity level (paper Fig. 6)", "Savitzky-Golay smoothed reflectance every 5 nm, 350-2500 nm, all four dates.")
mb = O["mean_by_level"].copy(); mb.index.name = "Wavelength (nm)"; h, last = table(ws, mb, 5, fmt="0.0000")
sd = O["sd_by_level"].copy(); sd.columns = [f"SD {c}" for c in sd.columns]; sd.index.name = "Wavelength (nm)"; table(ws, sd, 5, c0=8, fmt="0.0000")
md = O["mean_by_date"].copy(); md.columns = [DN[c] for c in md.columns]; md.index.name = "Wavelength (nm)"; table(ws, md, 5, c0=15, fmt="0.0000")
widths(ws, 12, 14)
scatter(ws, "Mean reflectance by severity level (350-2500 nm)", "Wavelength (nm)", "Reflectance", Reference(ws, min_col=1, min_row=h + 1, max_row=last),
        [Reference(ws, min_col=c, min_row=h, max_row=last) for c in range(2, 7)], LN, "U5", xmin=350, xmax=2500, ymin=0)
scatter(ws, "Mean reflectance by date", "Wavelength (nm)", "Reflectance", Reference(ws, min_col=15, min_row=h + 1, max_row=last),
        [Reference(ws, min_col=c, min_row=h, max_row=last) for c in range(16, 20)], list(md.columns), "U30", xmin=350, xmax=2500, ymin=0)
zz = mb.loc[450:1000]; hz, lz = table(ws, zz, last + 3, title="Zoom 450-1000 nm", fmt="0.0000")
scatter(ws, "Zoom 450-1000 nm", "Wavelength (nm)", "Reflectance", Reference(ws, min_col=1, min_row=hz + 1, max_row=lz),
        [Reference(ws, min_col=c, min_row=hz, max_row=lz) for c in range(2, 7)], LN, "U55", xmin=450, xmax=1000, ymin=0)

# S05
for nm, key in (("S05_NDSI_R2", "NDSI_R2"), ("S05b_RSI_R2", "RSI_R2")):
    M = O[key].copy(); kind = key.split("_")[0]
    ws = sheet(nm, f"Step 5 - {kind} R² with leaf score (paper Fig. 7)", f"{kind} = {'(Ri - Rj)/(Ri + Rj)' if kind == 'NDSI' else 'Ri/Rj'} for all pairs on a 20-nm grid (355-2495 nm), training dates only. Effective ranges = bands in any NDSI or RSI pair with R² >= {O['r2_threshold']} (the paper used R² > 0.5; the maximum R² here is lower).")
    v = M.values.copy(); i, j = np.unravel_index(np.nanargmax(v), v.shape)
    ws["A4"] = f"Best pair: band i = {M.index[i]} nm, band j = {M.columns[j]} nm, R² = {v[i, j]:.3f}"; ws["A4"].font = Font(bold=True, color="B24A3F")
    Mi = M.copy(); Mi.index.name = "band i \\ band j (nm)"; h, last = table(ws, Mi, 6, fmt="0.00")
    cscale(ws, f"B{h + 1}:{get_column_letter(1 + M.shape[1])}{last}", start="2C3E8F", mid="F2E35C", end="C0392B")
    for c in range(2, 2 + M.shape[1]): ws.column_dimensions[get_column_letter(c)].width = 5.2
    ws.column_dimensions["A"].width = 18

# S06
ws = sheet("S06_Band_selection", "Step 6 - Optimal wavelengths (paper Table VII, Fig. 8)",
           "Candidate bands = effective ranges from Step 5. RFE-RF: recursive elimination with random forest, 10 bands (as RFE-SHAP). SAND: learnable sigmoid weight per band with sparsity penalty, bands with weight > 0.524 kept (as in the paper). CARS-PLS: 50 Monte Carlo runs, lowest plot-grouped RMSECV (as SHAP-CARS, without SHAP). Final lists = selection on all three training dates.")
def rng_text(idx):
    w = sorted(int(bins[i]) for i in idx); out = []; s = p = w[0]
    for x in w[1:]:
        if x - p > 10: out.append(f"{s - 5}-{p + 5}"); s = x
        p = x
    out.append(f"{s - 5}-{p + 5}"); return ", ".join(out)
ws["A4"] = f"Effective ranges (training dates): {rng_text(ff['effective'])} nm ({len(ff['effective'])} bands)"; ws["A4"].font = Font(bold=True, color="B7791F")
sel = pd.DataFrame([[m, len(ff[k]), ", ".join(str(int(bins[i])) for i in sorted(ff[k]))] for m, k in (("RFE-RF", "rfe"), ("SAND", "sand"), ("CARS-PLS (= OWs)", "cars"))],
                   columns=["Method", "Variables", "Wavelength (nm)"]).set_index("Method")
h, last = table(ws, sel, 6); ws.column_dimensions["A"].width = 22; ws.column_dimensions["B"].width = 10; ws.column_dimensions["C"].width = 110
for rr in range(h + 1, last + 1): ws.cell(rr, 3).alignment = Alignment(wrap_text=True)
swd = pd.DataFrame({"SAND weight": ff["sand_w"].values, "Selected (> 0.524)": ["Yes" if v > 0.524 else "" for v in ff["sand_w"].values]}, index=pd.Index([int(x) for x in ff["sand_w"].index], name="Band (nm)"))
h2, l2 = table(ws, swd, last + 3, title="SAND weights of the effective-range bands", fmt="0.000")
bar(ws, "SAND feature weights (threshold 0.524)", "Weight", Reference(ws, min_col=2, min_row=h2, max_row=l2), Reference(ws, min_col=1, min_row=h2 + 1, max_row=l2), "E10", w=26, h=10, colors=["B7791F"])
ci = ff["cars_info"]; cdf = pd.DataFrame({"Variables kept": ci["n_vars"], "RMSECV": ci["rmsecv"]}, index=pd.Index(range(1, len(ci["rmsecv"]) + 1), name="CARS run"))
h3, l3 = table(ws, cdf, l2 + 3, title=f"CARS-PLS runs (best run = {ci['best_run']})", fmt="0.0000")
scatter(ws, "CARS: RMSECV over runs", "Run", "RMSECV", Reference(ws, min_col=1, min_row=h3 + 1, max_row=l3), [Reference(ws, min_col=3, min_row=h3, max_row=l3)], ["RMSECV"], "E32", w=13, h=8, colors=["1F6F78"])
scatter(ws, "CARS: variables kept", "Run", "Variables", Reference(ws, min_col=1, min_row=h3 + 1, max_row=l3), [Reference(ws, min_col=2, min_row=h3, max_row=l3)], ["Variables"], "M32", w=13, h=8, colors=["B7791F"])
freq = pd.DataFrame(index=pd.Index([int(x) for x in bins], name="Band (nm)"))
for k, nmx in (("rfe", "RFE-RF"), ("sand", "SAND"), ("cars", "CARS-PLS")):
    c = np.zeros(len(bins))
    for f in O["fold_feats"]: c[f[k]] += 1
    freq[nmx + " (folds of 5)"] = c.astype(int)
freq = freq[freq.sum(1) > 0]
h4, l4 = table(ws, freq, l3 + 3, title="Selection frequency across the 5 internal folds")
bar(ws, "Band selection frequency across folds", "Folds", Reference(ws, min_col=2, max_col=4, min_row=h4, max_row=l4), Reference(ws, min_col=1, min_row=h4 + 1, max_row=l4), "E50", w=30, h=11, colors=MCOL)

# S07
ws = sheet("S07_Vegetation_indices", "Step 7 - Vegetation indices (paper Tables V, VIII; Fig. 10a)", "16 indices of the paper + PSRI (listed in the paper's Table VIII). RVSI and EVI use the original published forms (the paper's printed formulas differ); MCARI uses the paper's 705/750-nm form. r = Pearson correlation with leaf score (training dates); Relief (k = 10) on the training dates; top 5 used as the VI input.")
names = list(O["VI"].columns); W = ff["relief_w"]; vr = O["VI_r"]
vt = pd.DataFrame({"Formula": [O["VI_formulas"][n] for n in names], "r with leaf score": vr[names].values, "Relief weight": W,
                   "Relief rank": pd.Series(W).rank(ascending=False).astype(int).values, "Selected (top 5)": ["Yes" if i in ff["vi_top"] else "" for i in range(len(names))]},
                  index=pd.Index(names, name="Index")).sort_values("Relief weight", ascending=False)
h, last = table(ws, vt, 5, fmt="0.000"); ws.column_dimensions["A"].width = 12; ws.column_dimensions["B"].width = 40
for c in "CDEF": ws.column_dimensions[c].width = 14
bar(ws, "Relief weight of vegetation indices", "Relief weight", Reference(ws, min_col=4, min_row=h, max_row=last), Reference(ws, min_col=1, min_row=h + 1, max_row=last), "H5", w=20, h=10, colors=["B7791F"])
bar(ws, "Correlation of indices with leaf score", "Pearson r", Reference(ws, min_col=3, min_row=h, max_row=last), Reference(ws, min_col=1, min_row=h + 1, max_row=last), "H27", w=20, h=10, colors=["1F6F78"])

ws = sheet("S08_VI_correlation", "Step 7b - Correlation among vegetation indices (paper Fig. 9)", "Pearson r between indices (training dates). Dark red/blue = strong redundancy.")
cm = O["VI_corrmat"].copy(); cm.index.name = "Index"; h, last = table(ws, cm, 5, fmt="0.00")
cscale(ws, f"B{h + 1}:{get_column_letter(1 + cm.shape[1])}{last}", start="2166AC", mid="FFFFFF", end="B2182B")
for c in range(2, 2 + cm.shape[1]): ws.column_dimensions[get_column_letter(c)].width = 8.5

# S09/S10
def res_sheet(name, title, purpose, df, sd=None):
    ws = sheet(name, title, purpose)
    d = df.copy(); d["input"] = pd.Categorical(d["input"], SETS); d["model"] = pd.Categorical(d["model"], MODELS); d = d.sort_values(["input", "model"])
    d = d[["input", "model", "F1_L0", "F1_L1", "F1_L2", "F1_L3", "F1_L4", "OA", "Kappa", "QWK", "Recall", "F1"]]
    d.columns = ["Input feature", "Model", "F1 L0", "F1 L1", "F1 L2", "F1 L3", "F1 L4", "OA (%)", "Kappa (%)", "Quadratic-weighted kappa (%)", "Macro recall (%)", "Macro F1 (%)"]
    d["Input feature"] = d["Input feature"].astype(str); d["Model"] = d["Model"].astype(str)
    h, last = table(ws, d.reset_index(drop=True), 5, index=False, fmt="0.00"); best = d.loc[d["OA (%)"].idxmax()]
    ws.cell(4, 1, f"Best: {best['Input feature']} + {best['Model']} | OA {best['OA (%)']:.2f}% | kappa {best['Kappa (%)']:.2f}% | macro F1 {best['Macro F1 (%)']:.2f}%").font = Font(bold=True, color="B24A3F")
    cscale(ws, f"H{h + 1}:H{last}", end="63BE7B")
    piv = d.pivot(index="Input feature", columns="Model", values="OA (%)").reindex(SETS)[MODELS]; piv.index.name = "OA (%)"
    h2, l2 = table(ws, piv, last + 3, title="OA (%) by input and model (chart source)", fmt="0.00")
    bar(ws, "Overall accuracy by input and model", "OA (%)", Reference(ws, min_col=2, max_col=5, min_row=h2, max_row=l2), Reference(ws, min_col=1, min_row=h2 + 1, max_row=l2), "N5", w=28, h=12, colors=MCOL)
    pf = d.pivot(index="Input feature", columns="Model", values="Macro F1 (%)").reindex(SETS)[MODELS]; pf.index.name = "Macro F1 (%)"
    h3, l3 = table(ws, pf, l2 + 3, title="Macro F1 (%) by input and model", fmt="0.00")
    bar(ws, "Macro F1 by input and model", "Macro F1 (%)", Reference(ws, min_col=2, max_col=5, min_row=h3, max_row=l3), Reference(ws, min_col=1, min_row=h3 + 1, max_row=l3), "N30", w=28, h=12, colors=MCOL)
    ws.column_dimensions["A"].width = 28; ws.column_dimensions["B"].width = 9
    for c in range(3, 13): ws.column_dimensions[get_column_letter(c)].width = 11
    if sd is not None: table(ws, sd, l3 + 3, title="Fold-to-fold OA (mean and SD of the 5 folds)", fmt="0.00")
    return best
fs = O["internal_folds"].groupby(["input", "model"]).OA.agg(["mean", "std"]).reset_index()
fs["input"] = pd.Categorical(fs["input"], SETS); fs["model"] = pd.Categorical(fs["model"], MODELS); fs = fs.sort_values(["input", "model"])
fs = fs.rename(columns={"input": "Input", "model": "Model", "mean": "OA mean (%)", "std": "OA SD (%)"}); fs["Input"] = fs["Input"].astype(str); fs["Model"] = fs["Model"].astype(str); fs = fs.set_index("Input")
b_int = res_sheet("S09_Internal_validation", "Steps 8-9 - Internal validation (paper Tables X-XII)", "5-fold cross-validation grouped by plot on 11 Feb, 24 Feb and 3 Mar (1,616 leaves). NDSI/RSI effective ranges, band selection and Relief were redone inside every training fold. OWs = CARS-PLS bands. Full wavelength = all 215 bands (baseline, as the paper's full-wavelength dataset).", O["internal"], fs)
b_ext = res_sheet("S10_Independent_test", "Step 10 - Independent validation on 13 Mar 2026 (paper Table XIII)", "Effective ranges, bands, indices and models fitted on the three training dates and applied unchanged to 648 leaves of 13 Mar (mostly pod formation).", O["external"])

# S11
ws = sheet("S11_Confusion", "Step 11 - Confusion matrices of the best internal model", "Rows = observed level; columns = predicted level (counts).")
y = meta.level.values; r0 = 5; key = (b_int["Input feature"], b_int["Model"])
for tag, P, idx in (("Internal CV (pooled)", O["internal_preds"][key][O["tr_idx"]], O["tr_idx"]), ("Independent test 13 Mar", O["external_preds"][key], O["te_idx"])):
    cmx = pd.DataFrame(confusion_matrix(y[idx], P, labels=range(5)), index=[f"Obs {n}" for n in LN], columns=[f"Pred L{k}" for k in range(5)]); cmx.index.name = f"{tag}: {key[0]} + {key[1]}"
    h, last = table(ws, cmx, r0); cscale(ws, f"B{h + 1}:F{last}"); r0 = last + 3
ws.column_dimensions["A"].width = 50
for c in "BCDEF": ws.column_dimensions[c].width = 11

# S12
ws = sheet("S12_Leaf_dataset", "Leaf-level dataset", "One row per leaf: metadata, score, level, 17 vegetation indices and smoothed reflectance in 10-nm bands (355-2495 nm).")
ds = pd.concat([meta[["date", "file", "plot", "variety", "stage", "treatment", "leaf", "score", "level"]].reset_index(drop=True), O["VI"].round(5).reset_index(drop=True),
                pd.DataFrame(O["B"].round(5), columns=[f"R{int(x)}" for x in bins])], axis=1)
for j, c in enumerate(ds.columns): cell = ws.cell(5, j + 1, c); cell.fill = HFILL; cell.font = HFONT
for i, row in enumerate(ds.itertuples(index=False)):
    for j, v in enumerate(row): ws.cell(6 + i, j + 1, v.item() if isinstance(v, np.generic) else v)
ws.freeze_panes = "J6"
wb.save(sys.argv[2]); print("saved", sys.argv[2])
