// Seminar deck – pooled leaf-level analysis, DT-EDNet vs CNNs (native charts and tables)
const pptxgen = require('pptxgenjs');
const J = require(process.argv[2]); const FIG = process.argv[3];
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.title = 'Leaf-level white rust detection – DT-EDNet';
const TEAL = '1F6F78', DARK = '1B2A34', GREY = '5F6B73', AMBER = 'B7791F';
const C5 = ['2E7D32', '9E9E9E', 'E0B000', '1F5FD1', 'D62728'], MC = ['1F6F78', 'B7791F', '6B4C8A', 'B24A3F'];
const F = 'Calibri'; let n = 0; const LN = J.level_names, SETS = J.sets, DL = J.dl_models, CL = J.cl_models;
const fmt = (v, d = 1) => (v === null || v === undefined) ? '–' : Number(v).toFixed(d), sum = a => a.reduce((x, y) => x + y, 0);
function slide(title, sub) {
  const s = pres.addSlide(); n++; s.background = { color: 'FFFFFF' };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 13.33, h: 0.08, fill: { color: TEAL }, line: { color: TEAL } });
  s.addText(title, { x: 0.5, y: 0.22, w: 12.3, h: 0.6, fontFace: F, fontSize: 24, bold: true, color: DARK, margin: 0, isTextBox: true });
  if (sub) s.addText(sub, { x: 0.5, y: 0.8, w: 12.3, h: 0.4, fontFace: F, fontSize: 13, color: GREY, italic: true, margin: 0, isTextBox: true });
  s.addText(String(n), { x: 12.6, y: 7.05, w: 0.5, h: 0.3, fontFace: F, fontSize: 10, color: GREY, align: 'right', isTextBox: true }); return s;
}
function bullets(s, items, x, y, w, h, fs = 15) { s.addText(items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1, paraSpaceAfter: 6 } })), { x, y, w, h, fontFace: F, fontSize: fs, color: DARK, valign: 'top', isTextBox: true }); }
function table(s, rows, x, y, w, colW, fs = 11, o = {}) {
  s.addTable(rows.map((r, i) => r.map((c, j) => ({ text: (c === null || c === undefined) ? '' : String(c), options: { bold: i === 0, color: i === 0 ? 'FFFFFF' : DARK,
    fill: { color: i === 0 ? TEAL : ((o.fill && o.fill(i, j, c)) || (i % 2 ? 'FFFFFF' : 'F4F8F8')) }, align: (j > 0 && o.center !== false) ? 'center' : 'left', valign: 'middle', fontSize: fs, fontFace: F } }))),
    { x, y, w, colW, border: { type: 'solid', pt: 0.5, color: 'B7C4C8' }, rowH: o.rowH || 0.3, autoPage: false });
}
function note(s, t, x, y, w, h) { s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: 'FFF4E0' }, line: { color: AMBER, width: 0.75 } }); s.addText(t, { x: x + 0.12, y: y + 0.05, w: w - 0.24, h: h - 0.1, fontFace: F, fontSize: 12, color: DARK, valign: 'middle', isTextBox: true }); }
const ax = o => Object.assign({ catAxisLabelFontFace: F, valAxisLabelFontFace: F, catAxisLabelFontSize: 10, valAxisLabelFontSize: 10, catAxisLabelColor: GREY, valAxisLabelColor: GREY,
  valGridLine: { color: 'E5E5E5', size: 0.5 }, catGridLine: { style: 'none' }, legendFontFace: F, legendFontSize: 10, titleFontFace: F, titleFontSize: 13, titleColor: DARK, showTitle: true }, o);
function line(s, wl, ser, names, colors, x, y, w, h, title, yt, freq, extra = {}) {
  s.addChart(pres.charts.LINE, names.map((nm, i) => ({ name: nm, labels: wl.map(String), values: ser[i] })), ax({ x, y, w, h, title, chartColors: colors, lineSize: 2, lineDataSymbol: 'none', showLegend: true, legendPos: 'b',
    catAxisLabelFrequency: freq, catAxisTitle: 'Wavelength (nm)', showCatAxisTitle: true, valAxisTitle: yt, showValAxisTitle: true, catAxisTitleFontSize: 11, valAxisTitleFontSize: 11, catAxisTitleColor: GREY, valAxisTitleColor: GREY, ...extra }));
}
const bd = J.dl.best, bc = J.classical.best, sp = J.split;
const dtBest = DL.slice(0, 1).map(m => SETS.map((s, i) => [s, J.dl.OA[m][i]]).sort((a, b) => b[1] - a[1])[0])[0];

{ const s = pres.addSlide(); n++; s.background = { color: TEAL };
  s.addText('Leaf-level white rust severity in mustard from ASD contact-probe spectra: DT-EDNet vs CNNs', { x: 0.8, y: 1.5, w: 11.7, h: 1.7, fontFace: F, fontSize: 34, bold: true, color: 'FFFFFF', isTextBox: true });
  s.addText('All four dates pooled • workflow and models of Ma et al. (2026), IAENG Int. J. Applied Mathematics 56(11): 5380–5398', { x: 0.8, y: 3.3, w: 11.7, h: 0.7, fontFace: F, fontSize: 18, color: 'D8ECEC', italic: true, isTextBox: true });
  s.addText('Animesh Panda  |  ICAR-IARI, New Delhi  |  MuDAS-AI  |  Rabi 2025–26', { x: 0.8, y: 5.6, w: 11.7, h: 0.5, fontFace: F, fontSize: 16, color: 'FFFFFF', isTextBox: true });
  s.addText(`${sum(sp.leaves).toLocaleString()} leaves  •  4 dates pooled  •  48 plots  •  350–2500 nm`, { x: 0.8, y: 6.1, w: 11.7, h: 0.5, fontFace: F, fontSize: 14, color: 'D8ECEC', isTextBox: true }); }

{ const s = slide('The reference paper and this study', 'Ma et al. (2026): rice blast, UAV hyperspectral imaging, DT-EDNet');
  table(s, [['Item', 'Ma et al. (2026)', 'This study'], ['Data', 'UAV hyperspectral canopy, 400–1000 nm', 'ASD contact probe, single leaves, 350–2500 nm'], ['Labels', 'Canopy DI → Levels 0–4', 'Leaf score 0/1/3/5/7/9 → L0–L4'],
    ['Data used', '2023 training; 2024 independent site', 'All 4 dates (11 Feb – 13 Mar 2026) pooled'], ['Split', 'Random 7:3; 10% of training = validation', 'Same 7:3 and 10%, but by PLOT (no plot in train and test)'],
    ['Features', 'OWs (RFE-SHAP, SAND, SHAP-CARS), VIs, texture, TTFI', 'OWs (RFE-RF, SAND, CARS-PLS), VIs; texture/TTFI not possible (no image)'],
    ['Models', 'DT-EDNet, EfficientNet, ResNet18, ConvNeXt V2', 'Same four (re-implemented; trained from scratch)'], ['Training', 'AdamW 6e-4, cosine, 300 epochs, batch 32, label smoothing 0.01, clip 1.2, patience 60', 'Same settings'],
    ['Ablation', 'DT-EDNet −SE, −DTG, −both (Table X)', 'Same, full-wavelength input']], 0.4, 1.3, 12.5, [1.8, 5.0, 5.7], 12, { center: false, rowH: 0.5 }); }

{ const s = slide('Data and pooled split', 'One leaf = one sample; split 7:3 by plot, stratified by treatment; 10% of training plots for validation');
  table(s, [['Date', 'Leaves', 'Plots', 'Growth stage(s)'], ...J.inventory], 0.4, 1.35, 6.2, [1.1, 1.0, 0.9, 3.2], 12, { rowH: 0.42 });
  table(s, [['Level', 'Training', 'Validation', 'Test'], ...LN.map((nm, l) => [nm, ...sp.by_level[l]]), ['Leaves', ...sp.leaves], ['Plots (healthy)', ...sp.plots.map((p, i) => `${p} (${sp.healthy_plots[i]})`)]], 0.4, 3.75, 6.2, [2.6, 1.2, 1.2, 1.2], 12, { rowH: 0.36 });
  s.addChart(pres.charts.BAR, LN.map((nm, l) => ({ name: nm, labels: sp.names, values: sp.by_level[l] })), ax({ x: 6.9, y: 1.3, w: 6.1, h: 5.8, barDir: 'col', barGrouping: 'stacked', chartColors: C5, title: 'Leaves per split and level', showLegend: true, legendPos: 'b', showValue: true, dataLabelPosition: 'ctr', dataLabelFontSize: 9, dataLabelColor: 'FFFFFF' })); }

{ const s = slide('Workflow (Ma et al., 2026, without texture)');
  table(s, [['Step', 'What was done'], ['1–2', 'Pool 4 dates; leaf score → L0–L4; plot-grouped 7:3 split, 10% validation'], ['3', 'Splice correction; Savitzky–Golay (11, 2); whole 350–2500 nm; 10-nm bands (215)'],
    ['4', 'Mean spectra by level (Fig. 6)'], ['5', 'NDSI / RSI R² maps on training leaves → effective ranges (Fig. 7)'], ['6', 'RFE-RF (10), SAND (w > 0.524), CARS-PLS → OWs (Table VII)'],
    ['7', '17 vegetation indices; correlation; Relief top 5 (Tables V, VIII; Fig. 9–10)'], ['8', 'DT-EDNet vs EfficientNet, ResNet18, ConvNeXt V2 on 6 inputs (Tables XI–XII)'],
    ['9', 'Ablation of DT-EDNet (Table X)'], ['10', 'Test accuracy by date; classical models as reference; confusion matrices']], 0.6, 1.2, 12.1, [1.0, 11.1], 14, { center: false, rowH: 0.52 }); }

{ const s = slide('Step 4 – Spectral curves by severity level (paper Fig. 6)');
  line(s, J.mean_spectra.wl, LN.map(k => J.mean_spectra.series[k]), LN, C5, 0.3, 1.0, 7.9, 6.1, 'Mean reflectance, 350–2500 nm (all leaves)', 'Reflectance', 20);
  line(s, J.mean_zoom.wl, LN.map(k => J.mean_zoom.series[k]), LN, C5, 8.3, 1.0, 4.8, 4.2, 'Zoom 450–1000 nm', 'Reflectance', 20, { catAxisLabelFontSize: 8 });
  note(s, 'Visible and SWIR reflectance rise and NIR falls with severity; L0 and L1 overlap almost completely.', 8.3, 5.4, 4.8, 1.2); }

{ const s = slide('Step 5 – NDSI and RSI (paper Fig. 7)', 'Training leaves only; white contour = effective-range threshold');
  s.addImage({ path: FIG + '/fig_ndsi_rsi.jpg', x: 0.4, y: 1.3, w: 8.6, h: 3.7 });
  table(s, [['Index', 'Band i', 'Band j', 'R²'], ['NDSI', J.ndsi_best[0], J.ndsi_best[1], J.ndsi_best[2]], ['RSI', J.rsi_best[0], J.rsi_best[1], J.rsi_best[2]]], 9.3, 1.4, 3.6, [0.9, 0.9, 0.9, 0.9], 12);
  table(s, [['Effective range(s)', 'Bands'], [J.effective.ranges.join(', ') + ' nm', J.effective.n]], 9.3, 2.85, 3.6, [2.5, 1.1], 12);
  note(s, `Paper threshold R² > 0.5; maximum here ${Math.max(J.ndsi_best[2], J.rsi_best[2])}, so R² ≥ ${J.r2_threshold} was used.`, 9.3, 3.9, 3.6, 1.0); }

{ const s = slide('Step 6 – Optimal wavelengths (paper Table VII, Fig. 8)');
  table(s, [['Method (paper)', 'n', 'Wavelengths (nm)'], ['RFE-RF (RFE-SHAP)', J.bands.rfe.length, J.bands.rfe.join(', ')], ['SAND (threshold 0.524)', J.bands.sand.length, J.bands.sand.join(', ')], ['CARS-PLS (SHAP-CARS) = OWs', J.bands.cars.length, J.bands.cars.join(', ')]],
    0.4, 1.1, 12.5, [3.0, 0.6, 8.9], 11, { center: false, rowH: 0.55 });
  s.addChart(pres.charts.BAR, [{ name: 'SAND weight', labels: J.sand_w.wl.map(String), values: J.sand_w.w }], ax({ x: 0.4, y: 3.7, w: 6.3, h: 3.4, barDir: 'col', chartColors: [AMBER], title: 'SAND weights (keep > 0.524)', showLegend: false, catAxisLabelFrequency: 10, catAxisLabelFontSize: 8, valAxisMaxVal: 1 }));
  s.addChart(pres.charts.LINE, [{ name: 'RMSECV', labels: J.cars_curve.run.map(String), values: J.cars_curve.rmsecv }], ax({ x: 6.9, y: 3.7, w: 6.0, h: 3.4, title: 'CARS-PLS RMSECV (best run ' + J.cars_curve.best + ')', chartColors: [TEAL], lineSize: 2, lineDataSymbol: 'none', showLegend: false, catAxisLabelFrequency: 5 })); }

{ const s = slide('Step 7 – Vegetation indices and Relief (paper Tables V, VIII; Fig. 10a)');
  const vi = J.vi.slice().sort((a, b) => b[3] - a[3]);
  table(s, [['Index', 'Formula', 'r', 'Relief', 'Top 5'], ...vi.map(r => [r[0], r[1], fmt(r[2], 3), fmt(r[3], 4), r[4]])], 0.3, 1.0, 7.0, [1.1, 3.3, 0.8, 1.0, 0.8], 9.5, { rowH: 0.3, fill: (i, j, c) => (j === 4 && c === 'Yes') ? 'FFE9B3' : null });
  s.addChart(pres.charts.BAR, [{ name: 'r', labels: J.vi.map(r => r[0]), values: J.vi.map(r => r[2]) }], ax({ x: 7.5, y: 1.0, w: 5.5, h: 6.1, barDir: 'bar', chartColors: [TEAL], title: 'Correlation with leaf score', showLegend: false, valAxisMinVal: -1, valAxisMaxVal: 1, catAxisLabelFontSize: 9, catAxisLabelPos: 'low' })); }

{ const s = slide('Step 8 – DT-EDNet vs EfficientNet, ResNet18, ConvNeXt V2 (paper Tables XI–XII)', `Test set: ${sp.leaves[2]} leaves from ${sp.plots[2]} unseen plots, all dates; chance = 20 %`);
  s.addChart(pres.charts.BAR, DL.map(m => ({ name: m, labels: SETS, values: J.dl.OA[m] })), ax({ x: 0.3, y: 1.25, w: 8.7, h: 5.9, barDir: 'col', barGrouping: 'clustered', chartColors: MC, title: 'Overall accuracy (%)', showLegend: true, legendPos: 'b', catAxisLabelFontSize: 10, valAxisMinVal: 0, valAxisMaxVal: 100 }));
  table(s, [['Best combination', ''], ['Input', bd.input], ['Model', bd.model], ['OA', fmt(bd.OA, 2) + ' %'], ['Cohen’s kappa', fmt(bd.Kappa, 2) + ' %'], ['Quadratic-weighted kappa', fmt(bd.QWK, 2) + ' %'], ['Macro F1', fmt(bd.F1, 2) + ' %'],
    ['F1 L0 / L1 / L2', [bd.F1_L0, bd.F1_L1, bd.F1_L2].map(v => fmt(v, 0)).join(' / ')], ['F1 L3 / L4', [bd.F1_L3, bd.F1_L4].map(v => fmt(v, 0)).join(' / ')]], 9.2, 1.3, 3.85, [1.85, 2.0], 11, { center: false, rowH: 0.38 });
  note(s, `DT-EDNet best: ${dtBest[0]}, OA ${fmt(dtBest[1])} %.`, 9.2, 5.0, 3.85, 0.8); }

{ const s = slide('Step 8 – Full results (%) on the test plots', 'Per-level F1, OA, kappa and macro F1 for every input and network');
  const rows = [['Input', 'Model', 'F1 L0', 'F1 L1', 'F1 L2', 'F1 L3', 'F1 L4', 'OA', 'Kappa', 'QWK', 'Macro F1']];
  SETS.forEach(st => DL.forEach(m => { const r = J.dl.table.find(x => x[0] === st && x[1] === m); rows.push([st, m, ...r.slice(2).map(v => v.toFixed(1))]); }));
  table(s, rows, 0.4, 1.25, 12.5, [3.2, 1.3, 0.78, 0.78, 0.78, 0.78, 0.78, 0.78, 0.78, 0.78, 0.78], 9, { rowH: 0.225, fill: (i) => (rows[i][0] === bd.input && rows[i][1] === bd.model) ? 'FFF2CC' : null }); }

{ const s = slide('Step 9 – Ablation of DT-EDNet (paper Table X)', 'Full-wavelength input (108 bands of 20 nm), same split and training');
  table(s, [['Model', 'F1-score (%)', 'OA (%)', 'Kappa (%)', 'Recall (%)'], ...J.ablation.map(r => [r[0], ...r.slice(1).map(v => fmt(v, 2))])], 0.5, 1.4, 6.5, [2.3, 1.05, 1.05, 1.05, 1.05], 13, { rowH: 0.48 });
  s.addChart(pres.charts.BAR, ['F1', 'OA', 'Kappa', 'Recall'].map((k, i) => ({ name: k, labels: J.ablation.map(r => r[0]), values: J.ablation.map(r => r[i + 1]) })), ax({ x: 7.3, y: 1.3, w: 5.7, h: 4.5, barDir: 'col', barGrouping: 'clustered', chartColors: MC, title: 'Ablation', showLegend: true, legendPos: 'b', valAxisMinVal: 0, valAxisMaxVal: 100, catAxisLabelFontSize: 9 }));
  note(s, 'Paper: removing SE or DTG lowered OA by about 1 point (91.4 → 90.4 %). Compare the direction of change here.', 0.5, 4.3, 6.5, 0.9); }

{ const s = slide('Step 10 – Test accuracy by date', `Input: ${J.per_date.set}; test leaves from unseen plots on each date`);
  s.addChart(pres.charts.BAR, DL.map(m => ({ name: m, labels: J.per_date.dates.map((d, i) => `${d} (n = ${J.per_date.n_test[i]})`), values: J.per_date.OA[m] })), ax({ x: 0.4, y: 1.3, w: 8.4, h: 5.8, barDir: 'col', barGrouping: 'clustered', chartColors: MC, title: 'Test OA (%) by date', showLegend: true, legendPos: 'b', valAxisMinVal: 0, valAxisMaxVal: 100 }));
  table(s, [['Date', ...DL], ...J.per_date.dates.map((d, i) => [d, ...DL.map(m => fmt(J.per_date.OA[m][i]))])], 9.0, 1.4, 4.0, [0.9, 0.85, 0.75, 0.75, 0.75], 10, { rowH: 0.36 });
  note(s, 'Pooling puts every growth stage into training, so the models now see 13 Mar-type leaves (the earlier date-transfer failure is avoided).', 9.0, 3.6, 4.0, 1.3); }

{ const s = slide('Reference: classical models on the same split');
  s.addChart(pres.charts.BAR, CL.map(m => ({ name: m, labels: SETS, values: J.classical.OA[m] })), ax({ x: 0.3, y: 1.1, w: 8.7, h: 6.0, barDir: 'col', barGrouping: 'clustered', chartColors: MC, title: 'Overall accuracy (%) – RF, SVM, PLS-DA, MLP', showLegend: true, legendPos: 'b', valAxisMinVal: 0, valAxisMaxVal: 100 }));
  table(s, [['', 'Deep (best)', 'Classical (best)'], ['Input', bd.input, bc.input], ['Model', bd.model, bc.model], ['OA', fmt(bd.OA) + ' %', fmt(bc.OA) + ' %'], ['Kappa', fmt(bd.Kappa) + ' %', fmt(bc.Kappa) + ' %'], ['Macro F1', fmt(bd.F1) + ' %', fmt(bc.F1) + ' %']],
    9.2, 1.3, 3.85, [0.9, 1.5, 1.45], 10, { center: false, rowH: 0.45 }); }

{ const s = slide('Where do the errors occur?', 'Confusion matrices on the test plots');
  const mk = cm => [['Obs \\ Pred', 'L0', 'L1', 'L2', 'L3', 'L4'], ...cm.map((r, i) => ['L' + i, ...r.map(String)])];
  const sh = cm => (i, j) => { if (i === 0 || j === 0) return null; const t = sum(cm[i - 1]) || 1, fr = 0.65 * cm[i - 1][j - 1] / t; const h = v => Math.round(255 - fr * (255 - v)).toString(16).padStart(2, '0'); return h(0x1F) + h(0x9F) + h(0xA8); };
  s.addText(`Best: ${J.cm_key.join(' + ')}`, { x: 0.5, y: 1.3, w: 6, h: 0.4, fontFace: F, fontSize: 14, bold: true, color: TEAL, isTextBox: true });
  table(s, mk(J.cm), 0.5, 1.75, 5.9, [1.6, 0.86, 0.86, 0.86, 0.86, 0.86], 13, { rowH: 0.48, fill: sh(J.cm) });
  s.addText(`DT-EDNet: ${J.cm_dt_key[0]}`, { x: 6.9, y: 1.3, w: 6, h: 0.4, fontFace: F, fontSize: 14, bold: true, color: TEAL, isTextBox: true });
  table(s, mk(J.cm_dt), 6.9, 1.75, 5.9, [1.6, 0.86, 0.86, 0.86, 0.86, 0.86], 13, { rowH: 0.48, fill: sh(J.cm_dt) });
  note(s, 'Most errors are between neighbouring levels (L0↔L1, L2↔L3); quadratic-weighted kappa is therefore higher than Cohen’s kappa.', 0.5, 5.0, 12.3, 0.8); }

{ const s = slide('Training details', 'Parameters, epochs before early stopping, best validation OA');
  const ti = J.train_info.filter(r => DL.includes(r[1]));
  table(s, [['Input', 'Model', 'Parameters', 'Epochs', 'Best val. OA (%)'], ...ti.map(r => [r[0], r[1], r[2].toLocaleString(), r[3], fmt(r[4])])], 0.4, 1.2, 7.4, [2.8, 1.4, 1.2, 0.8, 1.2], 9, { rowH: 0.23 });
  s.addChart(pres.charts.LINE, [{ name: 'Validation OA', labels: J.dt_val_curve.epoch.map(String), values: J.dt_val_curve.val_oa }], ax({ x: 8.0, y: 1.2, w: 5.0, h: 3.6, title: 'DT-EDNet validation OA per epoch', chartColors: [TEAL], lineSize: 1.5, lineDataSymbol: 'none', showLegend: false, catAxisLabelFrequency: 20 }));
  note(s, 'DT-EDNet has ~0.6 M parameters; the CNNs have 3–11 M. All were trained from scratch on ~1,400 leaves, which is small for these networks.', 8.0, 5.0, 5.0, 1.3); }

{ const s = slide('Comparison with Ma et al. (2026)');
  table(s, [['Aspect', 'Ma et al. (2026)', 'This study'], ['Best result', 'OA 95.25 % (OWs + VIs + TTFI3, DT-EDNet)', `OA ${fmt(bd.OA)} % (${bd.input}, ${bd.model})`], ['DT-EDNet best', '95.25 %', `${fmt(dtBest[1])} % (${dtBest[0]})`],
    ['Split', 'Random pixel ROIs 7:3', '7:3 by plot (stricter)'], ['Label', 'Canopy DI level', 'Visual score of one leaf'], ['Texture / TTFI', 'Used; TTFI3 best single feature', 'Not available (non-imaging)'], ['Training samples', '1,201', `${sp.leaves[0].toLocaleString()} (+ ${sp.leaves[1]} validation)`]],
    0.6, 1.3, 12.1, [2.6, 4.6, 4.9], 13, { center: false, rowH: 0.5 });
  note(s, 'Lower accuracy is expected: overlapping leaf scores, one probe spot per leaf, plot-grouped testing, no texture information, and a weaker spectral–score relation (max R² ≈ 0.36).', 0.6, 5.2, 12.1, 0.9); }

{ const s = slide('Conclusions');
  bullets(s, [`With all dates pooled and a plot-grouped 7:3 split, the best network was ${bd.model} with ${bd.input} (OA ${fmt(bd.OA)} %, quadratic-weighted kappa ${fmt(bd.QWK)} %).`,
    `DT-EDNet reached ${fmt(dtBest[1])} % (${dtBest[0]}); the best classical model reached ${fmt(bc.OA)} % (${bc.model}, ${bc.input}).`,
    'Five-level grading of single leaves remains difficult; errors are mostly between neighbouring levels.',
    'The data are near the minimum for deep networks (~1,400 training leaves, 31 training plots). More plots, seasons and growth stages are needed before DT-EDNet can show an advantage.'], 0.6, 1.3, 12.1, 5.6, 16); }

{ const s = slide('References');
  bullets(s, ['Ma, J., Wu, P., Guo, S., Lin, Y., Yu, F., Liu, T. (2026). Early detection of rice blast disease using a dual transformer network (DT-EDNet) based on hyperspectral imaging and multi-feature fusion. IAENG Int. J. Applied Mathematics 56(11), 5380–5398.',
    'He, K., Zhang, X., Ren, S., Sun, J. (2016). Deep residual learning for image recognition. Proc. IEEE CVPR, 770–778.',
    'Tan, M., Le, Q. (2019). EfficientNet: Rethinking model scaling for convolutional neural networks. Proc. ICML, PMLR 97, 6105–6114.',
    'Woo, S., Debnath, S., Hu, R., Chen, X., Liu, Z., Kweon, I.S., Xie, S. (2023). ConvNeXt V2: Co-designing and scaling ConvNets with masked autoencoders. Proc. IEEE/CVF CVPR, 16133–16142.',
    'Hu, J., Shen, L., Sun, G. (2018). Squeeze-and-excitation networks. Proc. IEEE CVPR, 7132–7141.',
    'Woo, S., Park, J., Lee, J.-Y., Kweon, I.S. (2018). CBAM: Convolutional block attention module. Proc. ECCV, 3–19.',
    'Vaswani, A. et al. (2017). Attention is all you need. Advances in Neural Information Processing Systems 30.',
    'Li, H., Liang, Y., Xu, Q., Cao, D. (2009). Key wavelengths screening using competitive adaptive reweighted sampling method for multivariate calibration. Analytica Chimica Acta 648(1), 77–84.'], 0.6, 1.2, 12.1, 5.9, 11.5); }

pres.writeFile({ fileName: process.argv[4] }).then(f => console.log('saved', f));
