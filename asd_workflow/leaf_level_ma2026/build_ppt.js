// Seminar deck (native editable charts and tables) - leaf-level analysis following Ma et al. (2026)
const pptxgen = require('pptxgenjs');
const J = require(process.argv[2]); const FIG = process.argv[3];
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.title = 'Leaf-level white rust detection from ASD spectra';
const TEAL = '1F6F78', DARK = '1B2A34', GREY = '5F6B73', AMBER = 'B7791F';
const C5 = ['2E7D32', '9E9E9E', 'E0B000', '1F5FD1', 'D62728'], MC = ['1F6F78', 'B7791F', '6B4C8A', 'B24A3F'];
const F = 'Calibri'; let n = 0; const LN = J.level_names;
const fmt = (v, d = 1) => (v === null || v === undefined) ? '–' : Number(v).toFixed(d);
const sum = a => a.reduce((x, y) => x + y, 0);
function slide(title, sub) {
  const s = pres.addSlide(); n++; s.background = { color: 'FFFFFF' };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 13.33, h: 0.08, fill: { color: TEAL }, line: { color: TEAL } });
  s.addText(title, { x: 0.5, y: 0.22, w: 12.3, h: 0.6, fontFace: F, fontSize: 24, bold: true, color: DARK, margin: 0, isTextBox: true });
  if (sub) s.addText(sub, { x: 0.5, y: 0.8, w: 12.3, h: 0.4, fontFace: F, fontSize: 13, color: GREY, italic: true, margin: 0, isTextBox: true });
  s.addText(String(n), { x: 12.6, y: 7.05, w: 0.5, h: 0.3, fontFace: F, fontSize: 10, color: GREY, align: 'right', isTextBox: true });
  return s;
}
function bullets(s, items, x, y, w, h, fs = 15) {
  s.addText(items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1, paraSpaceAfter: 6 } })), { x, y, w, h, fontFace: F, fontSize: fs, color: DARK, valign: 'top', isTextBox: true });
}
function table(s, rows, x, y, w, colW, fs = 11, o = {}) {
  s.addTable(rows.map((r, i) => r.map((c, j) => ({ text: (c === null || c === undefined) ? '' : String(c), options: {
    bold: i === 0, color: i === 0 ? 'FFFFFF' : DARK, fill: { color: i === 0 ? TEAL : ((o.fill && o.fill(i, j, c)) || (i % 2 ? 'FFFFFF' : 'F4F8F8')) },
    align: (j > 0 && o.center !== false) ? 'center' : 'left', valign: 'middle', fontSize: fs, fontFace: F } }))),
    { x, y, w, colW, border: { type: 'solid', pt: 0.5, color: 'B7C4C8' }, rowH: o.rowH || 0.3, autoPage: false });
}
function note(s, t, x, y, w, h) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: 'FFF4E0' }, line: { color: AMBER, width: 0.75 } });
  s.addText(t, { x: x + 0.12, y: y + 0.05, w: w - 0.24, h: h - 0.1, fontFace: F, fontSize: 12, color: DARK, valign: 'middle', isTextBox: true });
}
const ax = o => Object.assign({ catAxisLabelFontFace: F, valAxisLabelFontFace: F, catAxisLabelFontSize: 10, valAxisLabelFontSize: 10, catAxisLabelColor: GREY, valAxisLabelColor: GREY,
  valGridLine: { color: 'E5E5E5', size: 0.5 }, catGridLine: { style: 'none' }, legendFontFace: F, legendFontSize: 10, titleFontFace: F, titleFontSize: 13, titleColor: DARK, showTitle: true }, o);
function line(s, wl, ser, names, colors, x, y, w, h, title, yt, freq, extra = {}) {
  s.addChart(pres.charts.LINE, names.map((nm, i) => ({ name: nm, labels: wl.map(String), values: ser[i] })), ax({ x, y, w, h, title, chartColors: colors, lineSize: 2, lineDataSymbol: 'none',
    showLegend: true, legendPos: 'b', catAxisLabelFrequency: freq, catAxisTitle: 'Wavelength (nm)', showCatAxisTitle: true, valAxisTitle: yt, showValAxisTitle: true,
    catAxisTitleFontSize: 11, valAxisTitleFontSize: 11, catAxisTitleColor: GREY, valAxisTitleColor: GREY, ...extra }));
}
const bi = J.internal.best, be = J.external.best, es = J.ext_same_model;

// 1 title
{ const s = pres.addSlide(); n++; s.background = { color: TEAL };
  s.addText('Leaf-level detection of white rust in mustard from ASD contact-probe spectra', { x: 0.8, y: 1.6, w: 11.7, h: 1.6, fontFace: F, fontSize: 36, bold: true, color: 'FFFFFF', isTextBox: true });
  s.addText('Applying the multi-feature workflow of Ma et al. (2026), IAENG Int. J. Applied Mathematics 56(11): 5380–5398', { x: 0.8, y: 3.3, w: 11.7, h: 0.7, fontFace: F, fontSize: 18, color: 'D8ECEC', italic: true, isTextBox: true });
  s.addText('Animesh Panda  |  ICAR-IARI, New Delhi  |  MuDAS-AI  |  Rabi 2025–26', { x: 0.8, y: 5.6, w: 11.7, h: 0.5, fontFace: F, fontSize: 16, color: 'FFFFFF', isTextBox: true });
  s.addText(`${sum(J.counts.levels.map(sum)).toLocaleString()} leaves  •  4 dates  •  48 plots  •  350–2500 nm`, { x: 0.8, y: 6.1, w: 11.7, h: 0.5, fontFace: F, fontSize: 14, color: 'D8ECEC', isTextBox: true }); }

// 2 paper vs this work
{ const s = slide('The reference paper and how it is applied here', 'Ma et al. (2026): early detection of rice blast with UAV hyperspectral imaging and DT-EDNet');
  table(s, [['Paper step', 'Ma et al. (2026) – rice blast', 'This work – white rust, leaf level'],
    ['Data', 'UAV hyperspectral canopy, 400–1000 nm', 'ASD contact probe on single leaves, 350–2500 nm'],
    ['Labels (Tables II–IV)', 'Canopy DI → Levels 0–4', 'Leaf score 0/1/3/5/7/9 → Levels L0–L4'],
    ['Pre-processing', 'Savitzky–Golay; 450–1000 nm', 'Splice correction + Savitzky–Golay; whole 350–2500 nm (water bands kept)'],
    ['Spectral curves (Fig. 6)', 'Mean spectra per level', 'Same'],
    ['NDSI / RSI (Fig. 7)', 'R² maps → effective ranges (R² > 0.5)', 'Same; effective ranges at R² ≥ ' + J.r2_threshold],
    ['Band selection (Table VII)', 'RFE-SHAP, SAND, SHAP-CARS', 'RFE-RF, SAND, CARS-PLS (no SHAP)'],
    ['Vegetation indices', '16 VIs → Relief top 5', '16 VIs + PSRI → Relief top 5'],
    ['Texture + TTFI', 'GLCM texture, mRMR, TTFI', 'Not used – contact probe gives no image'],
    ['Models', 'DT-EDNet vs EfficientNet, ResNet18, ConvNeXt V2', 'RF, SVM, PLS-DA, MLP'],
    ['Validation', '7:3 split; independent 2024 site', 'CV grouped by plot (3 dates); independent date (13 Mar)']], 0.4, 1.3, 12.5, [2.5, 4.6, 5.4], 12, { center: false, rowH: 0.43 }); }

// 3 workflow
{ const s = slide('Workflow'); s.addImage({ path: FIG + '/fig_workflow.png', x: 3.6, y: 0.95, w: 6.1, h: 6.1 * 2250 / 1850 });
  bullets(s, ['One leaf = one sample; label = its own score', 'All selection steps fitted on training leaves only', 'Leaves of a plot never split between training and test'], 0.4, 1.4, 3.1, 4, 13);
  bullets(s, ['Each step has its own sheet in the Excel workbook (S01–S12)'], 9.95, 1.4, 3.0, 2, 13); }

// 4 data
{ const s = slide('Step 1 – Data', 'ASD FieldSpec contact probe; 75 duplicated spectra removed on 13 Mar');
  table(s, [['Date', 'Leaves', 'Plots', 'Growth stage(s)', 'Role'], ...J.inventory], 0.5, 1.4, 6.6, [1.0, 0.9, 0.8, 2.2, 1.7], 12, { rowH: 0.42 });
  bullets(s, ['48 plots: 36 inoculated, 12 healthy; varieties V1–V3', '5 plants × 3 leaf positions (L3, L5, LL) per plot on most dates', 'One spectrum per leaf', `No reflectance outside 0–1; ${J.qc.low_nir} leaves with NIR < 0.3 kept (severe disease)`], 0.5, 3.8, 6.6, 3, 14);
  s.addChart(pres.charts.BAR, LN.map((nm, i) => ({ name: nm, labels: J.counts.dates, values: J.counts.levels[i] })), ax({ x: 7.4, y: 1.3, w: 5.5, h: 5.6, barDir: 'col', barGrouping: 'stacked',
    chartColors: C5, title: 'Leaves per date and severity level', showLegend: true, legendPos: 'b', showValue: true, dataLabelPosition: 'ctr', dataLabelFontSize: 9, dataLabelColor: 'FFFFFF' })); }

// 5 labels
{ const s = slide('Step 2 – Leaf severity levels (paper Tables II–IV)');
  table(s, [['Leaf score', 'Level', 'Severity'], ['0', 'L0', 'Healthy'], ['1', 'L1', 'Mild'], ['3', 'L2', 'Moderate'], ['5', 'L3', 'Severe'], ['7 and 9', 'L4', 'Very severe (merged; 9 rare)']], 0.5, 1.3, 5.6, [1.4, 1.0, 3.2], 13, { rowH: 0.42 });
  const tr = [0, 1, 2, 3, 4].map(l => sum(J.counts.levels[l].slice(0, 3))), te = J.counts.levels.map(v => v[3]);
  table(s, [['Level', 'Training (3 dates)', 'Independent test (13 Mar)', 'Total'], ...LN.map((nm, l) => [nm, tr[l], te[l], tr[l] + te[l]]), ['Total', sum(tr), sum(te), sum(tr) + sum(te)]], 6.5, 1.3, 6.3, [2.3, 1.4, 1.6, 1.0], 12, { rowH: 0.4 });
  note(s, 'Label = the leaf’s own visible disease. Inoculated leaves without pustules are L0.', 0.5, 4.4, 5.6, 0.8);
  note(s, 'Class balance differs by date (few L4 on 11 Feb, few L1 on 13 Mar) → class-balanced models; macro F1 and kappa reported.', 6.5, 4.4, 6.3, 0.8); }

// 6 preprocessing
{ const s = slide('Step 3 – Pre-processing');
  table(s, [['Step', 'Setting', 'Reason'], ['Duplicate check', '75 identical spectra removed (13 Mar)', 'Columns repeated after a 2nd header'], ['Quality checks', 'Reflectance 0–1; NIR and red/green flags', 'Detect faulty readings'],
    ['Splice correction', 'VNIR and SWIR2 matched to SWIR1 at 1000/1800 nm', 'Remove detector steps'], ['Smoothing', 'Savitzky–Golay, window 11, order 2', 'Same filter as the paper'],
    ['Spectral range', 'Whole 350–2500 nm, water bands kept', 'Contact probe has its own light; 1450/1940 nm = leaf water'], ['Bands', '10-nm means → ' + J.n_bins + ' bands', 'Input to NDSI/RSI, selection and models']], 0.5, 1.3, 12.3, [2.4, 5.0, 4.9], 13, { center: false, rowH: 0.52 }); }

// 7 spectral curves
{ const s = slide('Step 4 – Spectral curves by severity level (paper Fig. 6)');
  line(s, J.mean_spectra.wl, LN.map(k => J.mean_spectra.series[k]), LN, C5, 0.3, 1.0, 7.9, 6.1, 'Mean reflectance, 350–2500 nm', 'Reflectance', 20);
  line(s, J.mean_zoom.wl, LN.map(k => J.mean_zoom.series[k]), LN, C5, 8.3, 1.0, 4.8, 4.2, 'Zoom 450–1000 nm', 'Reflectance', 20, { catAxisLabelFontSize: 8 });
  note(s, 'Visible reflectance rises and NIR falls with severity; SWIR rises as leaves dry. L0 and L1 overlap almost completely.', 8.3, 5.4, 4.8, 1.4); }

// 8 NDSI/RSI
{ const s = slide('Step 5 – NDSI and RSI (paper Fig. 7)', 'R² of all band pairs with leaf score; training dates; white contour = effective-range threshold');
  s.addImage({ path: FIG + '/fig_ndsi_rsi.png', x: 0.4, y: 1.3, w: 8.6, h: 3.7 });
  table(s, [['Index', 'Band i (nm)', 'Band j (nm)', 'R²'], ['NDSI', J.ndsi_best[0], J.ndsi_best[1], J.ndsi_best[2]], ['RSI', J.rsi_best[0], J.rsi_best[1], J.rsi_best[2]]], 9.3, 1.4, 3.6, [0.9, 0.9, 0.9, 0.9], 12);
  note(s, `Paper: R² > 0.5. Here the maximum R² is ${Math.max(J.ndsi_best[2], J.rsi_best[2])}, so effective ranges use R² ≥ ${J.r2_threshold} (|r| ≥ 0.5).`, 9.3, 2.85, 3.6, 1.2);
  table(s, [['Effective range(s)', 'Bands'], [J.effective.ranges.join(', ') + ' nm', J.effective.n]], 9.3, 4.3, 3.6, [2.5, 1.1], 12);
  note(s, 'Leaf spectra correlate only moderately with the visual leaf score: the probe reads one spot, while the score describes the whole leaf.', 0.5, 5.4, 8.4, 1.0); }

// 9 band selection
{ const s = slide('Step 6 – Optimal wavelengths (paper Table VII, Fig. 8)', 'Selection on the effective-range bands (all three training dates)');
  const j = a => a.join(', ');
  table(s, [['Method (paper)', 'n', 'Wavelengths (nm)'], ['RFE-RF (RFE-SHAP)', J.bands.rfe.length, j(J.bands.rfe)], ['SAND (SAND, threshold 0.524)', J.bands.sand.length, j(J.bands.sand)], ['CARS-PLS (SHAP-CARS) = OWs', J.bands.cars.length, j(J.bands.cars)]],
    0.4, 1.3, 12.5, [3.0, 0.6, 8.9], 11, { center: false, rowH: 0.55 });
  s.addChart(pres.charts.BAR, [{ name: 'SAND weight', labels: J.sand_w.wl.map(String), values: J.sand_w.w }], ax({ x: 0.4, y: 3.85, w: 6.3, h: 3.3, barDir: 'col', chartColors: [AMBER], title: 'SAND weights (keep > 0.524)', showLegend: false, catAxisLabelFrequency: 10, catAxisLabelFontSize: 8, valAxisMaxVal: 1 }));
  s.addChart(pres.charts.LINE, [{ name: 'RMSECV', labels: J.cars_curve.run.map(String), values: J.cars_curve.rmsecv }], ax({ x: 6.9, y: 3.85, w: 6.0, h: 3.3, title: 'CARS-PLS: RMSECV (best run ' + J.cars_curve.best + ')', chartColors: [TEAL], lineSize: 2, lineDataSymbol: 'none', showLegend: false, catAxisLabelFrequency: 5 })); }

// 10 stability
{ const s = slide('Step 6b – Stability of band selection', 'Number of the 5 internal folds in which each band was selected');
  const st = J.stability;
  s.addChart(pres.charts.BAR, [['RFE-RF', 1], ['SAND', 2], ['CARS-PLS', 3]].map(([nm, k]) => ({ name: nm, labels: st.map(r => String(r[0])), values: st.map(r => r[k]) })),
    ax({ x: 0.4, y: 1.25, w: 12.5, h: 4.9, barDir: 'col', barGrouping: 'clustered', chartColors: MC.slice(0, 3), title: 'Selection frequency (folds of 5)', showLegend: true, legendPos: 'b', valAxisMaxVal: 5, catAxisLabelRotate: -45, catAxisLabelFontSize: 8 }));
  note(s, 'Red edge (685–705 nm) and the short-wave edge (355–375 nm) are chosen repeatedly. The 350–400 nm detector edge is noisy, so these bands need confirmation.', 0.6, 6.3, 12.1, 0.75); }

// 11 VIs
{ const s = slide('Step 7 – Vegetation indices and Relief (paper Tables V, VIII; Fig. 10a)');
  const vi = J.vi.slice().sort((a, b) => b[3] - a[3]);
  table(s, [['Index', 'Formula', 'r', 'Relief', 'Top 5'], ...vi.map(r => [r[0], r[1], fmt(r[2], 3), fmt(r[3], 4), r[4]])], 0.3, 1.0, 7.0, [1.1, 3.3, 0.8, 1.0, 0.8], 9.5, { rowH: 0.3, fill: (i, j, c) => (j === 4 && c === 'Yes') ? 'FFE9B3' : null });
  s.addChart(pres.charts.BAR, [{ name: 'r', labels: J.vi.map(r => r[0]), values: J.vi.map(r => r[2]) }], ax({ x: 7.5, y: 1.0, w: 5.5, h: 6.1, barDir: 'bar', chartColors: [TEAL], title: 'Correlation with leaf score (training dates)', showLegend: false, valAxisMinVal: -1, valAxisMaxVal: 1, catAxisLabelFontSize: 9, catAxisLabelPos: 'low' })); }

// 12 VI correlation matrix
{ const s = slide('Step 7b – Correlation among vegetation indices (paper Fig. 9)');
  const nm = J.vi_corr.names, m = J.vi_corr.m;
  const col = v => { const a = Math.abs(v), t = Math.round(255 - a * 170).toString(16).padStart(2, '0'); return v >= 0 ? 'FF' + t + t : t + t + 'FF'; };
  table(s, [['', ...nm], ...nm.map((r, i) => [r, ...m[i].map(v => fmt(v, 2))])], 0.3, 1.0, 12.7, [1.1, ...nm.map(() => 11.6 / nm.length)], 7.5, { rowH: 0.33, fill: (i, j, c) => (i > 0 && j > 0) ? col(parseFloat(c)) : (j === 0 ? 'F4F8F8' : null) }); }

// 13 internal
function results(key, title, sub) {
  const s = slide(title, sub); const R = J[key];
  s.addChart(pres.charts.BAR, J.models.map(m => ({ name: m, labels: J.sets, values: R.OA[m] })), ax({ x: 0.3, y: 1.25, w: 8.7, h: 5.9, barDir: 'col', barGrouping: 'clustered', chartColors: MC,
    title: 'Overall accuracy (%) – chance level = 20 %', showLegend: true, legendPos: 'b', catAxisLabelFontSize: 10, valAxisMinVal: 0, valAxisMaxVal: 100 }));
  const b = R.best;
  table(s, [['Best combination', ''], ['Input', b.input], ['Model', b.model], ['OA', fmt(b.OA, 2) + ' %'], ['Cohen’s kappa', fmt(b.Kappa, 2) + ' %'], ['Quadratic-weighted kappa', fmt(b.QWK, 2) + ' %'], ['Macro F1', fmt(b.F1, 2) + ' %'],
    ['F1 L0 / L1 / L2', [b.F1_L0, b.F1_L1, b.F1_L2].map(v => fmt(v, 0)).join(' / ')], ['F1 L3 / L4', [b.F1_L3, b.F1_L4].map(v => fmt(v, 0)).join(' / ')]], 9.2, 1.3, 3.85, [1.85, 2.0], 11, { center: false, rowH: 0.38 });
  return s;
}
{ const s = results('internal', 'Steps 8–9 – Internal validation (paper Tables X–XII)', '5-fold CV grouped by plot; 11 Feb, 24 Feb, 3 Mar (1,616 leaves); all selection inside folds');
  const sd = J.internal.fold_sd[bi.input + '|' + bi.model]; note(s, `Fold-to-fold OA of the best model: ${fmt(sd[0])} ± ${fmt(sd[1])} %. As in the paper, the fused input (OWs + VIs) gives the best result.`, 9.2, 5.0, 3.85, 1.3); }

// 14 table of all results
{ const s = slide('Internal validation – full results (%)', 'Per-level F1, OA, kappa and macro F1 for every input and model');
  const rows = [['Input', 'Model', 'F1 L0', 'F1 L1', 'F1 L2', 'F1 L3', 'F1 L4', 'OA', 'Kappa', 'QWK', 'Macro F1']];
  J.sets.forEach(st => J.models.forEach(m => { const r = J.internal.table.find(x => x[0] === st && x[1] === m); rows.push([st, m, ...r.slice(2).map(v => v.toFixed(1))]); }));
  table(s, rows, 0.4, 1.25, 12.5, [3.2, 0.9, 0.82, 0.82, 0.82, 0.82, 0.82, 0.82, 0.82, 0.82, 0.82], 9, { rowH: 0.225, fill: (i, j, c) => (rows[i][0] === bi.input && rows[i][1] === bi.model) ? 'FFF2CC' : null }); }

// 15 external
{ const s = results('external', 'Step 10 – Independent validation (paper Table XIII)', 'Trained on 11 Feb, 24 Feb, 3 Mar; applied unchanged to 648 leaves of 13 Mar (mostly pod formation)');
  note(s, `Best internal model (${J.cm_key.join(' + ')}) on 13 Mar: OA ${fmt(es.OA)} %, kappa ${fmt(es.Kappa)} %. The models do not transfer to the later growth stage.`, 9.2, 5.0, 3.85, 1.3); }

// 16 confusion
{ const s = slide('Where do the errors occur?', 'Confusion matrices of the best internal model: ' + J.cm_key.join(' + '));
  const mk = cm => [['Observed \\ Predicted', 'L0', 'L1', 'L2', 'L3', 'L4'], ...cm.map((r, i) => ['L' + i, ...r.map(String)])];
  const sh = cm => (i, j) => { if (i === 0 || j === 0) return null; const t = sum(cm[i - 1]) || 1, f = 0.65 * cm[i - 1][j - 1] / t; const h = v => Math.round(255 - f * (255 - v)).toString(16).padStart(2, '0'); return h(0x1F) + h(0x9F) + h(0xA8); };
  s.addText('Internal CV (pooled)', { x: 0.5, y: 1.3, w: 6, h: 0.4, fontFace: F, fontSize: 15, bold: true, color: TEAL, isTextBox: true });
  table(s, mk(J.cm_internal), 0.5, 1.75, 5.9, [2.0, 0.78, 0.78, 0.78, 0.78, 0.78], 13, { rowH: 0.48, fill: sh(J.cm_internal) });
  s.addText('Independent test (13 Mar)', { x: 6.9, y: 1.3, w: 6, h: 0.4, fontFace: F, fontSize: 15, bold: true, color: TEAL, isTextBox: true });
  table(s, mk(J.cm_external), 6.9, 1.75, 5.9, [2.0, 0.78, 0.78, 0.78, 0.78, 0.78], 13, { rowH: 0.48, fill: sh(J.cm_external) });
  note(s, 'Internal errors fall mostly between neighbouring levels. On 13 Mar most leaves are predicted as one level: the later growth stage shifts the spectra.', 0.5, 5.0, 12.3, 0.9); }

// 17 comparison with paper
{ const s = slide('Comparison with Ma et al. (2026)');
  table(s, [['Aspect', 'Ma et al. (2026)', 'This work'], ['Best accuracy', 'OA 95.25 % (OWs + VIs + TTFI3, DT-EDNet)', `OA ${fmt(bi.OA)} % (${bi.input}, ${bi.model})`],
    ['Fusion better than single inputs?', 'Yes', 'Yes (internal)'], ['Hardest class', 'Level 2 (moderate)', 'L1–L3 (intermediate levels)'], ['Independent test', 'OA 95.50 % (2024 site)', `OA ${fmt(be.OA)} % (13 Mar)`],
    ['Validation split', 'Random pixel ROIs (7:3)', 'Grouped by plot; selection inside folds'], ['Label', 'Canopy DI level', 'Visual score of one leaf'], ['Texture', 'Used (GLCM, TTFI)', 'Not available (non-imaging)']], 0.6, 1.3, 12.1, [3.2, 4.3, 4.6], 13, { center: false, rowH: 0.5 });
  note(s, 'The large gap is expected: leaf scores overlap between adjacent levels, the probe reads one spot, plot-grouped nested validation is stricter, and the test date is a later growth stage.', 0.6, 5.6, 12.1, 0.9); }

// 18 conclusions
{ const s = slide('Conclusions and next steps');
  bullets(s, ['Leaf spectra change with white rust in the visible, red-edge, NIR and SWIR regions, but correlations with the leaf score are moderate (max R² ≈ ' + Math.max(J.ndsi_best[2], J.rsi_best[2]) + ').',
    `Following the paper, fused optimal wavelengths + vegetation indices gave the best internal result (OA ${fmt(bi.OA)} %, quadratic-weighted kappa ${fmt(bi.QWK)} %).`,
    'Five-level grading from single-leaf spectra is weak, and models trained on earlier dates did not transfer to the pod-formation date.',
    'Next: add 13 Mar (or a later date) to training; growth-stage-specific models; coarser classes or regression of the score; measure the pustule-bearing area directly; simulate UAV/MicaSense bands from the ASD spectra.'], 0.6, 1.3, 12.1, 5.6, 16); }

// 19 references
{ const s = slide('References');
  bullets(s, ['Ma, J., Wu, P., Guo, S., Lin, Y., Yu, F., Liu, T. (2026). Early detection of rice blast disease using a dual transformer network (DT-EDNet) based on hyperspectral imaging and multi-feature fusion. IAENG Int. J. Applied Mathematics 56(11), 5380–5398.',
    'Savitzky, A., Golay, M.J.E. (1964). Smoothing and differentiation of data by simplified least squares procedures. Analytical Chemistry 36(8), 1627–1639.',
    'Guyon, I., Weston, J., Barnhill, S., Vapnik, V. (2002). Gene selection for cancer classification using support vector machines. Machine Learning 46, 389–422.',
    'Li, H., Liang, Y., Xu, Q., Cao, D. (2009). Key wavelengths screening using competitive adaptive reweighted sampling method for multivariate calibration. Analytica Chimica Acta 648(1), 77–84.',
    'Robnik-Šikonja, M., Kononenko, I. (2003). Theoretical and empirical analysis of ReliefF and RReliefF. Machine Learning 53, 23–69.',
    'Breiman, L. (2001). Random forests. Machine Learning 45(1), 5–32.',
    'Roberts, D.R. et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. Ecography 40(8), 913–929.'], 0.6, 1.3, 12.1, 5.7, 12); }

pres.writeFile({ fileName: process.argv[4] }).then(f => console.log('saved', f));
