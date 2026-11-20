"""Step-by-step Excel (native charts) - pooled leaf-level analysis with DT-EDNet vs CNNs.
Usage: python build_excel_dl.py results_dl.pkl pooled_extra.pkl results_dl.json out.xlsx"""
import pickle, sys, json
import numpy as np, pandas as pd
from openpyxl import Workbook
from openpyxl.chart import ScatterChart, BarChart, Reference, Series
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.utils import get_column_letter

R = pickle.load(open(sys.argv[1], "rb")); E = pickle.load(open(sys.argv[2], "rb")); J = json.load(open(sys.argv[3]))
meta = R["meta"]; f = R["feats"]; bins = R["bins"]; LN = J["level_names"]; SETS = J["sets"]; DL = J["dl_models"]; CL = J["cl_models"]
tr, va, te = R["split"]["tr"], R["split"]["va"], R["split"]["te"]
DN = {"110226": "11 Feb 2026", "240226": "24 Feb 2026", "030326": "03 Mar 2026", "130326": "13 Mar 2026"}
wb = Workbook(); HF = PatternFill("solid", fgColor="1F6F78"); HFo = Font(bold=True, color="FFFFFF"); TF = Font(bold=True, size=14, color="1F6F78")
th = Side(style="thin", color="B7C4C8"); BD = Border(top=th, bottom=th, left=th, right=th)
C5 = ["2E7D32", "9E9E9E", "E0B000", "1F5FD1", "D62728"]; MC = ["1F6F78", "B7791F", "6B4C8A", "B24A3F"]

def sheet(n, t, p):
    ws = wb.create_sheet(n); ws["A1"] = t; ws["A1"].font = TF; ws["A2"] = p; ws["A2"].alignment = Alignment(wrap_text=True, vertical="top"); ws.merge_cells("A2:L3"); ws.row_dimensions[2].height = 34; return ws
def table(ws, df, r0, c0=1, index=True, fmt=None, title=None):
    if title: ws.cell(r0, c0, title).font = Font(bold=True, color="1F6F78"); r0 += 1
    cols = ([df.index.name or ""] if index else []) + [str(c) for c in df.columns]
    for j, c in enumerate(cols):
        cell = ws.cell(r0, c0 + j, c); cell.fill = HF; cell.font = HFo; cell.border = BD; cell.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
    for i, (ix, row) in enumerate(df.iterrows()):
        for j, v in enumerate(([ix] if index else []) + list(row.values)):
            if isinstance(v, (float, np.floating)) and np.isnan(v): v = None
            elif isinstance(v, np.generic): v = v.item()
            cell = ws.cell(r0 + 1 + i, c0 + j, v); cell.border = BD
            if fmt and isinstance(v, float): cell.number_format = fmt
    return r0, r0 + len(df)
def scatter(ws, title, xt, yt, xref, yrefs, names, anchor, w=24, h=12, xmin=None, xmax=None, ymin=None, colors=C5):
    ch = ScatterChart(); ch.title = title; ch.style = 13; ch.x_axis.title = xt; ch.y_axis.title = yt; ch.width, ch.height = w, h; ch.legend.position = "b"
    for k, (yr, nm) in enumerate(zip(yrefs, names)):
        s = Series(yr, xref, title=nm); s.marker.symbol = "none"; s.graphicalProperties.line.solidFill = colors[k % len(colors)]; s.graphicalProperties.line.width = 20000; ch.series.append(s)
    if xmin is not None: ch.x_axis.scaling.min = xmin
    if xmax is not None: ch.x_axis.scaling.max = xmax
    if ymin is not None: ch.y_axis.scaling.min = ymin
    ch.x_axis.delete = False; ch.y_axis.delete = False; ws.add_chart(ch, anchor)
def bar(ws, title, yt, dref, cref, anchor, w=24, h=11, grouping="clustered", colors=None, ymax=None):
    ch = BarChart(); ch.type = "col"; ch.grouping = grouping; ch.title = title; ch.style = 10
    if grouping == "stacked": ch.overlap = 100
    ch.y_axis.title = yt; ch.width, ch.height = w, h; ch.legend.position = "b"; ch.add_data(dref, titles_from_data=True); ch.set_categories(cref)
    for k, s in enumerate(ch.series): s.graphicalProperties.solidFill = (colors or C5)[k % len(colors or C5)]
    if ymax: ch.y_axis.scaling.max = ymax; ch.y_axis.scaling.min = 0
    ch.x_axis.delete = False; ch.y_axis.delete = False; ws.add_chart(ch, anchor)
def cscale(ws, rng, start="FFFFFF", mid=None, end="1F6F78"):
    ws.conditional_formatting.add(rng, ColorScaleRule(start_type="min", start_color=start, mid_type="percentile", mid_value=50, mid_color=mid, end_type="max", end_color=end) if mid
                                  else ColorScaleRule(start_type="min", start_color=start, end_type="max", end_color=end))
def widths(ws, w=12, first=18):
    ws.column_dimensions["A"].width = first
    for j in range(2, 40): ws.column_dimensions[get_column_letter(j)].width = w

ws = wb.active; ws.title = "README"
ws["A1"] = "Leaf-level white rust analysis of ASD contact-probe spectra – all dates pooled – DT-EDNet vs EfficientNet, ResNet18, ConvNeXt V2"; ws["A1"].font = Font(bold=True, size=15, color="1F6F78")
ws["A2"] = "Following Ma, J., Wu, P., Guo, S., Lin, Y., Yu, F., Liu, T. (2026). IAENG Int. J. Applied Mathematics 56(11), 5380-5398."
ws["A3"] = "Unit = one leaf (label = its own score). All 4 dates pooled; 7:3 train/test split by plot (no plot in both), 10% of training plots for validation. Whole range 350-2500 nm. No texture features (non-imaging data). Charts are native Excel charts."
steps = pd.DataFrame([["S01_Data", "1", "Dates, leaves, plots, stages", "Table I"], ["S02_Labels_Split", "2", "Severity levels; pooled plot-grouped train/validation/test split", "Tables II-IV"],
    ["S03_Preprocessing", "3", "QC, splice correction, Savitzky-Golay, 10-nm bands", "Section II-B"], ["S04_Spectral_curves", "4", "Mean spectra per level and date", "Fig. 6"],
    ["S05_NDSI_R2 / S05b_RSI_R2", "5", "Band-pair R2 maps (training leaves); effective ranges", "Fig. 7"], ["S06_Band_selection", "6", "RFE-RF, SAND, CARS-PLS", "Table VII, Fig. 8"],
    ["S07_Vegetation_indices", "7", "17 indices, correlation, Relief top 5", "Tables V, VIII; Fig. 10a"], ["S08_VI_correlation", "7b", "Correlation among indices", "Fig. 9"],
    ["S09_DTEDNet_vs_CNNs", "8", "DT-EDNet, EfficientNet, ResNet18, ConvNeXt V2 x 6 inputs on the test plots", "Tables XI-XII, Fig. 12-13"],
    ["S10_Ablation", "9", "DT-EDNet without SE / DTG / both (full wavelength)", "Table X"], ["S11_Per_date", "10", "Test accuracy of each model by date", "Fig. 14 / Table XIII analogue"],
    ["S12_Classical_reference", "11", "RF, SVM, PLS-DA, MLP on the same split", "Reference"], ["S13_Confusion", "12", "Confusion matrices", "-"],
    ["S14_Training_details", "13", "Parameters, epochs, best validation OA, run time; DT-EDNet validation curve", "Section II-G"], ["S15_Leaf_dataset", "Data", "Leaf table with split, VIs and 10-nm reflectance", "-"]],
    columns=["Sheet", "Step", "Content", "Paper item"]); table(ws, steps, 5, index=False)
for c, w in zip("ABCD", (28, 7, 80, 28)): ws.column_dimensions[c].width = w

ws = sheet("S01_Data", "Step 1 - Data (all four dates pooled)", "ASD contact probe; 48 plots (36 inoculated, 12 healthy), 3 varieties; one spectrum per leaf. 75 duplicated spectra (13 Mar) removed.")
inv = pd.DataFrame(J["inventory"], columns=["Date", "Leaves", "Plots", "Growth stage(s)"]).set_index("Date"); inv.loc["Total (pooled)"] = [int(inv.Leaves.sum()), 48, "All"]
h, last = table(ws, inv, 5); widths(ws, 14, 16); ws.column_dimensions["D"].width = 30

ws = sheet("S02_Labels_Split", "Step 2 - Severity levels and pooled split (paper Tables II-IV)", "Leaf score 0/1/3/5/7/9 -> L0-L4 (7 and 9 merged). Pooled leaves of all dates split 7:3 into training and test BY PLOT (stratified by treatment); 10% of the training plots form the validation set used for early stopping and model selection, as in the paper.")
mp = pd.DataFrame({"Level": ["L0", "L1", "L2", "L3", "L4", "L4"], "Severity": ["Healthy", "Mild", "Moderate", "Severe", "Very severe", "Very severe"]}, index=pd.Index([0, 1, 3, 5, 7, 9], name="Leaf score"))
h0, l0 = table(ws, mp, 5)
spl = pd.DataFrame(np.array(J["split"]["by_level"]), index=pd.Index(LN, name="Level"), columns=["Training", "Validation", "Test"]); spl.loc["Total leaves"] = spl.sum()
spl.loc["Plots"] = J["split"]["plots"]; spl.loc["Healthy plots"] = J["split"]["healthy_plots"]
h1, l1 = table(ws, spl, l0 + 3, title="Table 2.1 Pooled split (paper Table IV analogue)")
bar(ws, "Leaves per level in each split", "Leaves", Reference(ws, min_col=2, max_col=4, min_row=h1, max_row=h1 + 5), Reference(ws, min_col=1, min_row=h1 + 1, max_row=h1 + 5), "G5", w=18, h=9, colors=MC)
cnt = pd.crosstab(meta.date, meta.level).reindex(index=list(DN), columns=range(5), fill_value=0); cnt.index = list(DN.values()); cnt.index.name = "Date"; cnt.columns = LN
table(ws, cnt, l1 + 3, title="Table 2.2 Leaves per level and date"); widths(ws, 13, 22)

ws = sheet("S03_Preprocessing", "Step 3 - Pre-processing", "Duplicates removed -> quality checks -> splice correction (1000/1800 nm) -> Savitzky-Golay (11, 2) -> whole 350-2500 nm kept -> 10-nm bands (215); 20-nm bands (108) for the full-wavelength deep-learning input.")
qc = E["qc"]; q = pd.DataFrame([["Leaves analysed", len(meta), ""], ["Reflectance outside 0-1", int(qc.out_of_range.sum()), "All valid"], ["NIR < 0.30", int(qc.low_nir.sum()), "Flagged, kept"],
    ["Smoothing", "SG 11 / 2", "As in the paper"], ["Spectral range", "350-2500 nm", "Water bands kept (contact probe)"], ["Bands (selection, classical models)", 215, "10-nm means"],
    ["Full-wavelength deep input", 108, "20-nm means (to keep transformer training time manageable)"], ["Pseudo-2-D input", "zero-padded square", "DT-EDNet: native size; CNNs: resized to 32 x 32"]], columns=["Item", "Value", "Note"]).set_index("Item")
table(ws, q, 5)
for c, w in zip("ABC", (36, 22, 60)): ws.column_dimensions[c].width = w

ws = sheet("S04_Spectral_curves", "Step 4 - Mean spectra by severity level (paper Fig. 6)", "All pooled leaves, every 5 nm, 350-2500 nm.")
mb = E["mean_by_level"].copy(); mb.index.name = "Wavelength (nm)"; h, last = table(ws, mb, 5, fmt="0.0000")
md = E["mean_by_date"].copy(); md.columns = [DN[c] for c in md.columns]; md.index.name = "Wavelength (nm)"; table(ws, md, 5, c0=8, fmt="0.0000"); widths(ws, 12, 14)
scatter(ws, "Mean reflectance by level", "Wavelength (nm)", "Reflectance", Reference(ws, min_col=1, min_row=h + 1, max_row=last), [Reference(ws, min_col=c, min_row=h, max_row=last) for c in range(2, 7)], LN, "N5", xmin=350, xmax=2500, ymin=0)
scatter(ws, "Mean reflectance by date", "Wavelength (nm)", "Reflectance", Reference(ws, min_col=8, min_row=h + 1, max_row=last), [Reference(ws, min_col=c, min_row=h, max_row=last) for c in range(9, 13)], list(md.columns), "N30", xmin=350, xmax=2500, ymin=0)

for nm, key in (("S05_NDSI_R2", "NDSI_R2"), ("S05b_RSI_R2", "RSI_R2")):
    M = E[key].copy(); kind = key.split("_")[0]
    ws = sheet(nm, f"Step 5 - {kind} R² with leaf score (paper Fig. 7)", f"All band pairs on a 20-nm grid; training leaves only. Effective ranges = bands in pairs with R² >= {E['r2_threshold']}: {', '.join(J['effective']['ranges'])} nm.")
    v = M.values.copy(); i, j = np.unravel_index(np.nanargmax(v), v.shape); ws["A4"] = f"Best pair: {M.index[i]} / {M.columns[j]} nm, R² = {v[i, j]:.3f}"; ws["A4"].font = Font(bold=True, color="B24A3F")
    Mi = M.copy(); Mi.index.name = "band i \\ band j (nm)"; h, last = table(ws, Mi, 6, fmt="0.00"); cscale(ws, f"B{h + 1}:{get_column_letter(1 + M.shape[1])}{last}", start="2C3E8F", mid="F2E35C", end="C0392B")
    for c in range(2, 2 + M.shape[1]): ws.column_dimensions[get_column_letter(c)].width = 5.2
    ws.column_dimensions["A"].width = 18

ws = sheet("S06_Band_selection", "Step 6 - Optimal wavelengths (paper Table VII, Fig. 8)", "On the effective-range bands of the training leaves: RFE-RF (10 bands), SAND (sigmoid weights > 0.524), CARS-PLS (50 runs, plot-grouped RMSECV). CARS bands = OWs.")
sel = pd.DataFrame([[m, len(J["bands"][k]), ", ".join(map(str, J["bands"][k]))] for m, k in (("RFE-RF", "rfe"), ("SAND", "sand"), ("CARS-PLS (= OWs)", "cars"))], columns=["Method", "Variables", "Wavelength (nm)"]).set_index("Method")
h, last = table(ws, sel, 5); ws.column_dimensions["A"].width = 20; ws.column_dimensions["B"].width = 10; ws.column_dimensions["C"].width = 110
for rr in range(h + 1, last + 1): ws.cell(rr, 3).alignment = Alignment(wrap_text=True)
swd = pd.DataFrame({"SAND weight": J["sand_w"]["w"], "Selected": ["Yes" if v > 0.524 else "" for v in J["sand_w"]["w"]]}, index=pd.Index(J["sand_w"]["wl"], name="Band (nm)"))
h2, l2 = table(ws, swd, last + 3, title="SAND weights", fmt="0.000")
bar(ws, "SAND feature weights (threshold 0.524)", "Weight", Reference(ws, min_col=2, min_row=h2, max_row=l2), Reference(ws, min_col=1, min_row=h2 + 1, max_row=l2), "E10", w=26, h=10, colors=["B7791F"])
cdf = pd.DataFrame({"Variables kept": J["cars_curve"]["nvars"], "RMSECV": J["cars_curve"]["rmsecv"]}, index=pd.Index(J["cars_curve"]["run"], name="CARS run"))
h3, l3 = table(ws, cdf, l2 + 3, title=f"CARS runs (best run = {J['cars_curve']['best']})", fmt="0.0000")
scatter(ws, "CARS: RMSECV", "Run", "RMSECV", Reference(ws, min_col=1, min_row=h3 + 1, max_row=l3), [Reference(ws, min_col=3, min_row=h3, max_row=l3)], ["RMSECV"], "E32", w=13, h=8, colors=["1F6F78"])

ws = sheet("S07_Vegetation_indices", "Step 7 - Vegetation indices (paper Tables V, VIII; Fig. 10a)", "16 paper indices + PSRI; r with leaf score and Relief (k = 10) on training leaves; top 5 = VI input. RVSI and EVI in their original forms.")
vt = pd.DataFrame(J["vi"], columns=["Index", "Formula", "r with leaf score", "Relief weight", "Selected (top 5)"]).set_index("Index").sort_values("Relief weight", ascending=False)
h, last = table(ws, vt, 5, fmt="0.000"); ws.column_dimensions["A"].width = 12; ws.column_dimensions["B"].width = 40
for c in "CDE": ws.column_dimensions[c].width = 14
bar(ws, "Relief weight", "Relief", Reference(ws, min_col=4, min_row=h, max_row=last), Reference(ws, min_col=1, min_row=h + 1, max_row=last), "G5", w=20, h=10, colors=["B7791F"])
bar(ws, "Correlation with leaf score", "r", Reference(ws, min_col=3, min_row=h, max_row=last), Reference(ws, min_col=1, min_row=h + 1, max_row=last), "G27", w=20, h=10, colors=["1F6F78"])
ws = sheet("S08_VI_correlation", "Step 7b - Correlation among indices (paper Fig. 9)", "Pearson r (training leaves).")
cm = pd.DataFrame(J["vi_corr"]["m"], index=pd.Index(J["vi_corr"]["names"], name="Index"), columns=J["vi_corr"]["names"]); h, last = table(ws, cm, 5, fmt="0.00")
cscale(ws, f"B{h + 1}:{get_column_letter(1 + cm.shape[1])}{last}", start="2166AC", mid="FFFFFF", end="B2182B")
for c in range(2, 2 + cm.shape[1]): ws.column_dimensions[get_column_letter(c)].width = 8.5

def res_sheet(name, title, purpose, block, models):
    ws = sheet(name, title, purpose)
    d = pd.DataFrame(block["table"], columns=["Input feature", "Model", "F1 L0", "F1 L1", "F1 L2", "F1 L3", "F1 L4", "OA (%)", "Kappa (%)", "Quadratic-weighted kappa (%)", "Macro F1 (%)"])
    d["s"] = d["Input feature"].map(SETS.index); d["m"] = d["Model"].map(models.index); d = d.sort_values(["s", "m"]).drop(columns=["s", "m"]).reset_index(drop=True)
    h, last = table(ws, d, 5, index=False, fmt="0.0"); b = block["best"]
    ws.cell(4, 1, f"Best: {b['input']} + {b['model']} | OA {b['OA']:.2f}% | kappa {b['Kappa']:.2f}% | macro F1 {b['F1']:.2f}%").font = Font(bold=True, color="B24A3F"); cscale(ws, f"H{h + 1}:H{last}", end="63BE7B")
    piv = pd.DataFrame(block["OA"], index=pd.Index(SETS, name="OA (%)"))[models]; h2, l2 = table(ws, piv, last + 3, title="OA (%) by input and model (chart source)", fmt="0.00")
    bar(ws, title.split(" - ")[-1] + ": overall accuracy", "OA (%)", Reference(ws, min_col=2, max_col=5, min_row=h2, max_row=l2), Reference(ws, min_col=1, min_row=h2 + 1, max_row=l2), "N5", w=28, h=12, colors=MC, ymax=100)
    pf = pd.DataFrame(block["F1"], index=pd.Index(SETS, name="Macro F1 (%)"))[models]; h3, l3 = table(ws, pf, l2 + 3, title="Macro F1 (%) by input and model", fmt="0.00")
    bar(ws, "Macro F1", "Macro F1 (%)", Reference(ws, min_col=2, max_col=5, min_row=h3, max_row=l3), Reference(ws, min_col=1, min_row=h3 + 1, max_row=l3), "N30", w=28, h=12, colors=MC, ymax=100)
    ws.column_dimensions["A"].width = 28; ws.column_dimensions["B"].width = 13
    for c in range(3, 12): ws.column_dimensions[get_column_letter(c)].width = 11
res_sheet("S09_DTEDNet_vs_CNNs", "Step 8 - DT-EDNet vs EfficientNet, ResNet18, ConvNeXt V2 (paper Tables XI-XII)", f"Test set = {len(te)} leaves from {J['split']['plots'][2]} plots never used for training (all dates). Training as in the paper: AdamW lr 6e-4, wd 1e-5, cosine to 1e-6, max 300 epochs, batch 32, label smoothing 0.01, gradient clip 1.2, early stopping patience 60 on validation OA, seed 42. CNNs (timm efficientnet_b0, resnet18, convnextv2_atto; 1 input channel; trained from scratch) on the pseudo-2-D map resized to 32 x 32.", J["dl"], DL)

ws = sheet("S10_Ablation", "Step 9 - Ablation of DT-EDNet (paper Table X)", "Full-wavelength input (108 bands of 20 nm); same split and training settings. -SE: SE block removed; -DTG: Dual Transformer Group removed (embedding -> global pooling -> head).")
ab = pd.DataFrame(J["ablation"], columns=["Model", "F1-score (%)", "OA (%)", "Kappa (%)", "Recall (%)"]).set_index("Model"); h, last = table(ws, ab, 5, fmt="0.00")
bar(ws, "Ablation on full-wavelength input", "%", Reference(ws, min_col=2, max_col=5, min_row=h, max_row=last), Reference(ws, min_col=1, min_row=h + 1, max_row=last), "H5", w=20, h=10, colors=MC, ymax=100); widths(ws, 14, 20)

ws = sheet("S11_Per_date", "Step 10 - Test accuracy by date (paper Fig. 14 / Table XIII analogue)", f"Input: {J['per_date']['set']} (best input). Test leaves of each date from the unseen test plots.")
pdf = pd.DataFrame(J["per_date"]["OA"], index=pd.Index(J["per_date"]["dates"], name="Date")); pdf.insert(0, "Test leaves", J["per_date"]["n_test"])
h, last = table(ws, pdf, 5, fmt="0.0"); bar(ws, "Test OA by date", "OA (%)", Reference(ws, min_col=3, max_col=6, min_row=h, max_row=last), Reference(ws, min_col=1, min_row=h + 1, max_row=last), "H5", w=20, h=10, colors=MC, ymax=100); widths(ws, 14, 14)

res_sheet("S12_Classical_reference", "Step 11 - Classical models on the same split (reference)", "RF, SVM (RBF, tuned by plot-grouped inner CV), PLS-DA and MLP fitted on training + validation leaves, same test plots.", J["classical"], CL)

ws = sheet("S13_Confusion", "Step 12 - Confusion matrices", "Rows = observed level; columns = predicted (counts), test plots.")
r0 = 5
for tag, cmx in ((f"Best: {J['cm_key'][0]} + {J['cm_key'][1]}", J["cm"]), (f"DT-EDNet: {J['cm_dt_key'][0]}", J["cm_dt"])):
    c = pd.DataFrame(cmx, index=[f"Obs {n}" for n in LN], columns=[f"Pred L{k}" for k in range(5)]); c.index.name = tag
    h, last = table(ws, c, r0); cscale(ws, f"B{h + 1}:F{last}"); r0 = last + 3
ws.column_dimensions["A"].width = 48

ws = sheet("S14_Training_details", "Step 13 - Training details", "Trainable parameters, epochs run before early stopping, best validation OA and run time (CPU, 1 thread per model).")
ti = pd.DataFrame(J["train_info"], columns=["Input", "Model", "Parameters", "Epochs run", "Best validation OA (%)", "Run time (s)"]); h, last = table(ws, ti, 5, index=False)
vc = pd.DataFrame({"Validation OA (%)": J["dt_val_curve"]["val_oa"]}, index=pd.Index(J["dt_val_curve"]["epoch"], name="Epoch"))
h2, l2 = table(ws, vc, 5, c0=9, title=f"DT-EDNet validation curve ({J['cm_dt_key'][0]})")
scatter(ws, "DT-EDNet validation OA per epoch", "Epoch", "Validation OA (%)", Reference(ws, min_col=9, min_row=h2 + 1, max_row=l2), [Reference(ws, min_col=10, min_row=h2, max_row=l2)], ["Validation OA"], "L5", w=18, h=9, colors=["1F6F78"])
for c, w in zip("ABCDEF", (30, 18, 12, 11, 14, 12)): ws.column_dimensions[c].width = w

ws = sheet("S15_Leaf_dataset", "Leaf-level dataset", "One row per leaf: metadata, level, split, 17 vegetation indices and 10-nm reflectance.")
split = np.array(["Training"] * len(meta), object); split[va] = "Validation"; split[te] = "Test"
ds = pd.concat([meta[["date", "file", "plot", "variety", "stage", "treatment", "leaf", "score", "level"]].reset_index(drop=True), pd.Series(split, name="split"),
                E["VI"].round(5).reset_index(drop=True), pd.DataFrame(E["B"].round(5), columns=[f"R{int(x)}" for x in bins])], axis=1)
for j, c in enumerate(ds.columns): cell = ws.cell(5, j + 1, c); cell.fill = HF; cell.font = HFo
for i, row in enumerate(ds.itertuples(index=False)):
    for j, v in enumerate(row): ws.cell(6 + i, j + 1, v.item() if isinstance(v, np.generic) else v)
ws.freeze_panes = "K6"
wb.save(sys.argv[4]); print("saved", sys.argv[4])
