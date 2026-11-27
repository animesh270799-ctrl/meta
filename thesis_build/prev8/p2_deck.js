// 8 slides (no introduction): work done with the 2025-26 data – data collected, UAV processing up to plot-average spectra, ASD leaf analysis
// up to the point of the user's ASD deck. Times New Roman, 14 pt body text; native charts and flow charts (editable).
const fs = require('fs');
const { pres, F, FS, C, THEME, S, sec, T, BL, box, arr, line, tb, refline } = require('../meth2627/deck/adv_lib.js');
const D = JSON.parse(fs.readFileSync(__dirname + '/prev8.json', 'utf8'));
const GC = ['1A9850', '66BD63', 'D9A400', 'F46D43', 'D73027', '7F0000'];
const AX = { catAxisLabelFontFace: F, valAxisLabelFontFace: F, legendFontFace: F, titleFontFace: F, dataLabelFontFace: F, catAxisTitleFontFace: F, valAxisTitleFontFace: F,
  catAxisLabelFontSize: FS, valAxisLabelFontSize: FS, legendFontSize: FS, titleFontSize: FS, dataLabelFontSize: 12, catAxisTitleFontSize: FS, valAxisTitleFontSize: FS,
  catAxisLabelColor: '333333', valAxisLabelColor: '333333', titleColor: C.dk, valGridLine: { color: 'E3E3E3', size: 0.5 }, catGridLine: { style: 'none' }, showTitle: true, legendPos: 'b' };
const ax = (o) => Object.assign({}, AX, o);
function tag(s, t, col) { s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 11.35, y: 0.38, w: 1.5, h: 0.42, fill: { color: col }, line: { color: col }, rectRadius: 0.08 }); s.addText(t, { x: 11.35, y: 0.38, w: 1.5, h: 0.42, fontFace: F, fontSize: FS, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', isTextBox: true, margin: 0 }); }
function stat(s, x, y, w, big, small, col, fill) { s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.95, fill: { color: fill }, line: { color: col, width: 1 }, rectRadius: 0.06 });
  s.addText([{ text: big, options: { bold: true, color: col, fontSize: 20, breakLine: true } }, { text: small, options: { fontSize: FS, color: C.dk } }], { x, y, w, h: 0.95, fontFace: F, align: 'center', valign: 'middle', isTextBox: true, margin: 0.03 }); }
const nd = (s, x, y, w, h, t, sub, col, fill) => box(s, x, y, w, h, t, sub, col, fill, { fs: FS });
const A = (s, x1, y1, x2, y2) => arr(s, x1, y1, x2, y2, '595959', 1.5);
const chart = (name) => D.asd_charts.find(c => c.title.startsWith(name));
let s;
sec('Data collected');
// ================================================================ 1 Data collected
s = S('Data collected in the 2025-26 season', 'Data', 'All data collected in 2025-26. UAV: RGB, multispectral and both hyperspectral cameras on four dates; thermal only on 24 February 2026. ASD leaf spectra with leaf scores on four dates. Daily weather from the IARI observatory.');
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.45, y: 1.15, w: 12.43, h: 0.5, fill: { color: C.lgold }, line: { color: C.gold, width: 1 }, rectRadius: 0.06 });
s.addText([{ text: 'Four data-collection dates: ', options: { bold: true, color: C.gold } }, { text: '11 February, 24 February, 3 March and 13 March 2026', options: { bold: true } }, { text: ' – UAV (RGB, multispectral, both hyperspectral cameras) and ASD leaf spectra with leaf scores on every date; thermal on 24 February 2026 only.' }],
  { x: 0.6, y: 1.15, w: 12.15, h: 0.5, fontFace: F, fontSize: FS, color: C.dk, valign: 'middle', isTextBox: true, margin: 0 });
tb(s, [['Data', 'Instrument', 'Dates (2026)', 'Details'],
  ['UAV RGB', 'DJI Phantom', '11 Feb, 24 Feb, 3 Mar, 13 Mar (4)', 'true-colour images of the field'],
  ['UAV multispectral', 'MicaSense RedEdge-MX', '11 Feb, 24 Feb, 3 Mar, 13 Mar (4)', '5 bands (blue, green, red, red edge, NIR)'],
  ['UAV hyperspectral VNIR–SWIR', 'Headwall Co-Aligned HP', '11 Feb, 24 Feb, 3 Mar, 13 Mar (4)', '613 bands, 400–2500 nm'],
  ['UAV hyperspectral VNIR', 'Headwall Nano', '11 Feb, 24 Feb, 3 Mar, 13 Mar (4)', 'VNIR bands'],
  ['UAV thermal', 'FLIR Vue Pro R', '24 Feb only (1)', 'canopy temperature'],
  ['Leaf spectra', 'ASD FieldSpec', '11 Feb, 24 Feb, 3 Mar, 13 Mar (4)', '2339 spectra, 350–2500 nm; leaves L3, L5, LL'],
  ['Leaf disease score', '0–9 white rust scale', 'same 4 dates', 'every scanned leaf (grades 0, 1, 3, 5, 7, 9)'],
  ['Weather', 'IARI observatory', 'whole season (daily)', 'Tmax, Tmin, RH (morning, afternoon), rain']], 0.45, 1.8, 8.3, [2.35, 1.95, 2.25, 1.75], { firstCol: true, rowH: 0.43 });
box(s, 9.0, 1.8, 3.88, 2.2, 'Field experiment (ICAR-IARI)', ['48 plots: 12 healthy (fungicide, plots 1–12) + 36 unsprayed (R1–R3)', '3 varieties × 4 sowing dates (9, 18, 27 Dec 2025; 9 Jan 2026)', 'Natural white rust infection'], C.g, C.lt, { fs: FS, align: 'left', valign: 'top' });
// date timeline
const dts = ['11 Feb', '24 Feb', '3 Mar', '13 Mar']; const tx = [9.25, 10.15, 11.05, 11.95];
s.addText('UAV flights and ASD sampling (2026)', { x: 9.0, y: 4.15, w: 3.88, h: 0.35, fontFace: F, fontSize: FS, bold: true, color: C.g, isTextBox: true, margin: 0 });
line(s, 9.15, 4.95, 12.75, 4.95, '595959', 1.5);
dts.forEach((d, i) => { s.addShape(pres.shapes.OVAL, { x: tx[i] + 0.2, y: 4.82, w: 0.26, h: 0.26, fill: { color: i === 1 ? C.red : C.g }, line: { color: 'FFFFFF', width: 1 } });
  s.addText(d, { x: tx[i] - 0.15, y: 4.5, w: 0.95, h: 0.3, fontFace: F, fontSize: FS, align: 'center', isTextBox: true, margin: 0 });
  s.addText(i === 1 ? 'RGB, MS, HS ×2, TIR, ASD' : 'RGB, MS, HS ×2, ASD', { x: tx[i] - 0.12, y: 5.15, w: 0.9, h: 0.95, fontFace: F, fontSize: 12, align: 'center', valign: 'top', isTextBox: true, margin: 0, color: i === 1 ? C.red : C.dk }); });
s.addText('Thermal (TIR) on 24 Feb 2026 only.', { x: 9.0, y: 6.2, w: 3.88, h: 0.35, fontFace: F, fontSize: FS, italic: true, color: C.red, isTextBox: true, margin: 0 });
// ================================================================ 2 UAV processing chain
sec('UAV data');
s = S('UAV data: processing chain and status', 'UAV', 'Twelve steps from the raw UAV images to plot spectra. Steps 1–9 are done for the hyperspectral data; endmember extraction is in progress; plot-average spectra are ready for the 24 February image; features are next.');
const ST = [['1. UAV flights', '11 Feb, 24 Feb, 3 Mar, 13 Mar 2026', 'd'], ['2. Band selection', '613 → 483 bands', 'd'], ['3. SG smoothing', 'width 5, order 2', 'd'], ['4. Projection + clip', 'WGS 84 / UTM 43N', 'd'],
            ['8. SAM + NDVI', 'R898, R684; 0.1–0.3 rad', 'd'], ['7. Training ROIs', 'soil, shadow, grass, mustard', 'd'], ['6. Plot clipping', '11 Feb, 24 Feb, 13 Mar done', 'd'], ['5. Plot boundaries', '48 plots, numbered', 'd'],
            ['9. Crop mask', 'NDVI > 0.6 × SAM 0.3; erode', 'd'], ['10. Crop polygons', 'raster → vector → clip', 'd'], ['11. Endmembers', 'SMACC per plot', 'p'], ['12. Plot-average spectra', '24 Feb done → features next', 'h']];
const COL = { d: [C.g, C.lt], p: [C.gold, C.lgold], h: [C.blue, C.lblue] };
const BX = [0.55, 3.75, 6.95, 10.15], BY = [1.35, 2.95, 4.55], BW = 2.65, BH = 1.05;
ST.forEach(([h, b, st], k) => { const r = Math.floor(k / 4), c = k % 4; nd(s, BX[c], BY[r], BW, BH, h, b, COL[st][0], COL[st][1]); });
for (let c = 0; c < 3; c++) { A(s, BX[c] + BW + 0.03, BY[0] + BH / 2, BX[c + 1] - 0.03, BY[0] + BH / 2); A(s, BX[c + 1] - 0.03, BY[1] + BH / 2, BX[c] + BW + 0.03, BY[1] + BH / 2); A(s, BX[c] + BW + 0.03, BY[2] + BH / 2, BX[c + 1] - 0.03, BY[2] + BH / 2); }
A(s, BX[3] + BW / 2, BY[0] + BH + 0.03, BX[3] + BW / 2, BY[1] - 0.03); A(s, BX[0] + BW / 2, BY[1] + BH + 0.03, BX[0] + BW / 2, BY[2] - 0.03);
[['Done', C.g, C.lt], ['In progress', C.gold, C.lgold], ['Ready for 24 Feb', C.blue, C.lblue]].forEach(([t, col, f], i) => { s.addShape(pres.shapes.RECTANGLE, { x: 0.55 + i * 2.6, y: 5.9, w: 0.35, h: 0.3, fill: { color: f }, line: { color: col, width: 1.25 } }); T(s, t, 0.98 + i * 2.6, 5.86, 2.1, 0.38); });
refline(s, 'Savitzky and Golay (1964); Thenkabail et al. (2004); Kruse et al. (1993); Rouse et al. (1974); Gruninger et al. (2004).', 6.45, 0.5);
// ================================================================ 3 Hyperspectral pre-processing
s = S('Hyperspectral pre-processing: bands, smoothing, projection', 'UAV', 'ENVI: 613 bands reduced to 483 by removing the noisy detector ends and the two atmospheric water-vapour regions; Savitzky–Golay smoothing; ArcMap projection to UTM 43N and clipping to the field.');
tb(s, [['Removed region (nm)', 'Reason'], ['900–915', 'noisy end of the VNIR detector (VNIR/SWIR join at 919.7 / 921.4 nm)'], ['1335–1460', 'atmospheric water vapour (≈ 1400 nm)'], ['1785–1965', 'atmospheric water vapour (≈ 1900 nm)'], ['2400–2500', 'low signal, noisy SWIR end']],
   0.45, 1.25, 6.4, [1.9, 4.5], { firstCol: true, rowH: 0.42 });
// kept / removed band bar (400–2500 nm)
const bx0 = 0.45, bw0 = 6.4, wl = (w) => bx0 + (w - 400) / 2100 * bw0;
s.addText('Bands kept (green) and removed (red), 400–2500 nm', { x: 0.45, y: 3.55, w: 6.4, h: 0.35, fontFace: F, fontSize: FS, bold: true, color: C.g, isTextBox: true, margin: 0 });
s.addShape(pres.shapes.RECTANGLE, { x: bx0, y: 3.95, w: bw0, h: 0.4, fill: { color: '8BC48A' }, line: { color: '595959', width: 0.75 } });
[[900, 915], [1335, 1460], [1785, 1965], [2400, 2500]].forEach(([a, b]) => s.addShape(pres.shapes.RECTANGLE, { x: wl(a), y: 3.95, w: Math.max(wl(b) - wl(a), 0.04), h: 0.4, fill: { color: 'E06666' }, line: { color: 'E06666', width: 0 } }));
[400, 800, 1200, 1600, 2000, 2400].forEach(w => s.addText(String(w), { x: wl(w) - 0.35, y: 4.37, w: 0.7, h: 0.3, fontFace: F, fontSize: 12, align: 'center', isTextBox: true, margin: 0 }));
stat(s, 0.45, 4.85, 3.1, '613 → 483', 'bands in every cube', C.g, C.lt); stat(s, 3.75, 4.85, 3.1, 'UTM 43N', 'same grid for all sensors', C.blue, C.lblue);
const steps3 = [['Savitzky–Golay smoothing (ENVI)', 'filter width 5, polynomial order 2: removes random noise, keeps absorption features; needed before derivatives'],
                ['Projection (ArcMap)', 'Project → WGS 1984 / UTM zone 43N for every date and sensor'], ['Field boundary and clipping', 'polygon shapefile → Extract by Mask → field-clipped reflectance image'], ['Plot polygons', '48 plots digitised, plot number added, dissolved; one subset per plot and date']];
steps3.forEach(([h, b], i) => { nd(s, 7.15, 1.25 + i * 1.2, 5.7, 1.0, h, b, C.blue, C.lblue); if (i < 3) A(s, 10.0, 2.25 + i * 1.2 + 0.01, 10.0, 2.45 + i * 1.2 - 0.01); });
refline(s, 'Thenkabail et al. (2004); Savitzky and Golay (1964).', 6.25, 0.4);
// ================================================================ 4 crop pixels
s = S('Crop pixels: SAM × NDVI mask, polygons, endmembers', 'UAV', 'Mustard pixels are separated from soil, shadow and weeds with a crop mask = NDVI mask × SAM mask, eroded at the edges; crop polygons are made per plot; SMACC endmember extraction per plot is in progress.');
const C4 = [['Training ROIs', 'soil, shadow, grass/weeds, mustard (+ flower); 3 × 2 sites per plot'], ['SAM classification', 'max. spectral angle 0.1, 0.2, 0.3 rad tested'], ['NDVI', '(R898 − R684)/(R898 + R684)']];
nd(s, 0.45, 1.3, 2.9, 1.15, C4[0][0], C4[0][1], C.g, C.lt); nd(s, 3.75, 1.3, 2.9, 1.15, C4[1][0], C4[1][1], C.g, C.lt); nd(s, 3.75, 2.75, 2.9, 1.0, C4[2][0], C4[2][1], C.g, C.lt);
A(s, 3.38, 1.88, 3.72, 1.88);
nd(s, 7.05, 1.75, 2.75, 1.55, 'Crop mask', 'NDVI > 0.6 (=1) × SAM mustard at 0.3 rad (=1); erode edge pixels', C.g, 'D9EAD3');
A(s, 6.68, 1.88, 7.02, 2.3); A(s, 6.68, 3.25, 7.02, 2.85);
nd(s, 10.2, 1.75, 2.68, 1.55, 'Crop polygons', 'reclassify → raster to polygon → select mustard → clip to plots', C.g, C.lt); A(s, 9.83, 2.52, 10.17, 2.52);
nd(s, 10.2, 3.75, 2.68, 1.3, 'Endmembers (SMACC)', 'per plot: crop, chlorotic/pustule, soil, shadow, flower', C.gold, C.lgold); A(s, 11.54, 3.33, 11.54, 3.72);
nd(s, 7.05, 3.75, 2.75, 1.3, 'Plot-average spectrum', 'mean of the plot ROI, 483 bands (24 Feb 2026)', C.blue, C.lblue); A(s, 10.17, 4.4, 9.83, 4.4);
BL(s, ['A pixel is kept only if it is green (NDVI) **and** spectrally similar to mustard (SAM): soil, shadow and weeds are removed.', 'Crop stage differed among plots on one date: 16 vegetative, 22 flowering, 10 pod-formation plots (sowing-date effect).',
       'Open questions: keep or remove flower pixels (yellow petals dominate 500–650 nm); multispectral values (DN, radiance or reflectance?); thermal emissivity correction.'], 0.45, 4.05, 6.35, 2.2);
refline(s, 'Kruse et al. (1993); Rouse et al. (1974); Gruninger et al. (2004); Sulik and Long (2016).', 6.35, 0.45);
// ================================================================ 5 UAV plot-average spectra
const U = D.uav;
s = S('UAV hyperspectral plot-average spectra, 24 Feb 2026', 'UAV', 'Plot-average spectra of the 48 plots from the 24 February image (ENVI ROI means, 483 bands). Diseased plots are compared with the healthy plots; diseased plots are also split at the median plot disease index.');
const xs = U.wl, nan = (a) => a.map((v, i) => v);
s.addChart(pres.charts.SCATTER, [{ name: 'X', values: xs }, { name: 'Healthy plots (12)', values: U.healthy }, { name: 'Diseased, PDI below median (18)', values: U.dis_low }, { name: 'Diseased, PDI above median (18)', values: U.dis_high }],
  ax({ x: 0.45, y: 1.2, w: 8.2, h: 5.0, title: 'Mean plot reflectance, 24 Feb 2026 (UAV Headwall, 483 bands)', chartColors: ['1A9850', 'F46D43', '7F0000'], lineSize: 2, lineDataSymbol: 'none', showLegend: true,
       catAxisMinVal: 400, catAxisMaxVal: 2400, catAxisMajorUnit: 400, showCatAxisTitle: true, catAxisTitle: 'Wavelength (nm)', showValAxisTitle: true, valAxisTitle: 'Reflectance', valAxisLabelFormatCode: 'General', catAxisLabelFormatCode: 'General' }));
const P = D.uav_points;
stat(s, 8.9, 1.25, 3.98, '48 plots × 483 bands', String(Math.round(U.wl_min)) + '–' + String(Math.round(U.wl_max)) + ' nm; ROI mean of each plot', C.blue, C.lblue);
stat(s, 8.9, 2.35, 3.98, P['800'][0].toFixed(3) + ' → ' + P['800'][1].toFixed(3), 'NIR (800 nm): healthy → diseased plots', C.red, C.lred);
stat(s, 8.9, 3.45, 3.98, Math.round(U.pdi_min) + '–' + Math.round(U.pdi_max) + '%', 'plot disease index of the 36 diseased plots (ASD leaf scores, 24 Feb)', C.gold, C.lgold);
BL(s, ['Band gaps = removed water-vapour and detector regions.', 'Next: plot features (bands, derivatives, indices) and the other dates and sensors.'], 8.9, 4.6, 3.98, 1.6);
refline(s, 'Plot disease index = Σ leaf grade / (9 × leaves) × 100 from the ASD leaf scores of the same plots.', 6.35, 0.45);
// ================================================================ 6 ASD data set and pre-processing
sec('ASD leaf data');
s = S('ASD leaf spectra: data set and pre-processing', 'ASD', 'ASD leaf spectra of 11 Feb, 24 Feb, 3 Mar and 13 Mar 2026 with the 0–9 leaf score of each leaf. 2339 spectra were read; the 9 L4 leaves were left out, giving 2330 leaves. Pre-processing as listed.');
const dlab = ['11 Feb 2026', '24 Feb 2026', '3 Mar 2026', '13 Mar 2026'];
s.addChart(pres.charts.BAR, [0, 1, 3, 5, 7, 9].map((g, i) => ({ name: 'Grade ' + g, labels: dlab, values: D.grade_date[String(g)] })),
  ax({ x: 0.45, y: 1.2, w: 5.6, h: 4.0, barDir: 'col', barGrouping: 'stacked', chartColors: GC, title: 'Leaves of each grade per date (n = ' + D.n_leaves + ')', showLegend: true, showValAxisTitle: true, valAxisTitle: 'Leaves' }));
tb(s, [['Leaf position', 'Leaves', 'Growth stage', 'Leaves', 'Variety', 'Leaves'], ['L3', D.by_leaf.L3, 'Vegetative', D.by_stage.Vegetative, 'V1', D.by_variety.V1], ['L5', D.by_leaf.L5, 'Flowering', D.by_stage.Flowering, 'V2', D.by_variety.V2], ['LL', D.by_leaf.LL, 'Pod formation', D.by_stage['Pod formation'], 'V3', D.by_variety.V3]],
   0.45, 5.3, 5.6, [1.05, 0.75, 1.3, 0.75, 0.85, 0.9], { rowH: 0.3, fs: FS });
BL(s, ['**Dates:** 11 Feb, 24 Feb, 3 Mar and 13 Mar 2026 (419, 540, 648, 723 leaves).', '**Read:** 2339 spectra (350–2500 nm, 1 nm) with plot, variety, stage, leaf position and score; 9 L4 leaves left out → **2330 leaves**.',
       '**Smoothing:** Savitzky–Golay, window 11 nm, order 2, on the full spectrum.', '**First derivative** from the same filter.', '**Range:** trimmed to 400–2400 nm (Matzrafi et al., 2017); water bands kept (contact probe).',
       '**5-nm values:** value at every 5th nm → 401 reflectance + 401 derivative bands.', '**Indices**, REP, Dr and REarea from the 1-nm smoothed spectrum.', '**Mean ± SD** spectra of each grade (all leaves, description).'], 6.35, 1.25, 6.5, 4.9);
T(s, [{ text: 'References: ', options: { bold: true, italic: true, color: C.g } }, { text: 'Savitzky and Golay (1964); Matzrafi et al. (2017).', options: { italic: true } }], 6.35, 6.2, 6.5, 0.4);
// ================================================================ 7 mean spectra + red edge
s = S('ASD results: mean spectra by grade and red-edge shift', 'ASD', 'With increasing grade, visible and SWIR reflectance rise and NIR reflectance falls; the red-edge position moves from 709 to 701 nm.');
const cm = chart('Mean reflectance'); const xw = cm.cats.map(Number);
s.addChart(pres.charts.SCATTER, [{ name: 'X', values: xw }].concat(cm.series.map(r => ({ name: r.name.replace('grade', 'Grade'), values: r.values }))),
  ax({ x: 0.45, y: 1.2, w: 7.3, h: 5.0, title: 'Mean leaf reflectance, 400–2400 nm', chartColors: GC, lineSize: 1.75, lineDataSymbol: 'none', showLegend: true, catAxisMinVal: 400, catAxisMaxVal: 2400, catAxisMajorUnit: 400,
       showCatAxisTitle: true, catAxisTitle: 'Wavelength (nm)', showValAxisTitle: true, valAxisTitle: 'Reflectance', valAxisLabelFormatCode: 'General', catAxisLabelFormatCode: 'General' }));
const rep = chart('Red-edge position');
s.addChart(pres.charts.BAR, [{ name: 'REP (nm)', labels: ['G0', 'G1', 'G3', 'G5', 'G7', 'G9'], values: rep.series[0].values }],
  ax({ x: 7.95, y: 1.2, w: 4.93, h: 2.7, barDir: 'col', chartColors: GC, title: 'Red-edge position (nm)', showLegend: false, valAxisMinVal: 698, valAxisMaxVal: 711, showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0.0' }));
const mr = (w, g) => cm.series[g].values[cm.cats.indexOf(String(w))];
stat(s, 7.95, 4.05, 2.4, mr(800, 0).toFixed(3) + ' → ' + mr(800, 5).toFixed(3), 'NIR 800 nm (G0 → G9)', C.g, C.lt); stat(s, 10.48, 4.05, 2.4, mr(680, 0).toFixed(3) + ' → ' + mr(680, 5).toFixed(3), 'red 680 nm', C.red, C.lred);
stat(s, 7.95, 5.15, 2.4, mr(1450, 0).toFixed(3) + ' → ' + mr(1450, 5).toFixed(3), 'water band 1450 nm', C.blue, C.lblue); stat(s, 10.48, 5.15, 2.4, rep.series[0].values[0].toFixed(1) + ' → ' + rep.series[0].values[5].toFixed(1), 'REP (nm): blue shift', C.gold, C.lgold);
refline(s, 'Chlorosis lowers chlorophyll absorption (red ↑) and damages leaf structure (NIR ↓); the red-edge peak falls and shifts to shorter wavelengths.', 6.35, 0.45);
// ================================================================ 8 correlation + stage
s = S('ASD results: correlation with the grade and growth stage', 'ASD', 'The first derivative correlates more strongly with the leaf grade than reflectance (r = 0.62 at 800 nm vs 0.46 at 695 nm). Mean grade rises from vegetative to pod formation; stage and date are linked in this design.');
const cr = chart('Pearson r'); const xr = cr.cats.map(Number);
s.addChart(pres.charts.SCATTER, [{ name: 'X', values: xr }, { name: 'Reflectance', values: cr.series[0].values }, { name: 'First derivative', values: cr.series[1].values }],
  ax({ x: 0.45, y: 1.2, w: 7.3, h: 5.0, title: 'Pearson r with the leaf grade (n = ' + D.n_leaves + ')', chartColors: ['1F4E79', 'C0392B'], lineSize: 1.75, lineDataSymbol: 'none', showLegend: true, catAxisMinVal: 400, catAxisMaxVal: 2400, catAxisMajorUnit: 400,
       showCatAxisTitle: true, catAxisTitle: 'Wavelength (nm)', showValAxisTitle: true, valAxisTitle: 'Pearson r', valAxisLabelFormatCode: 'General', catAxisLabelFormatCode: 'General' }));
const fdmax = Math.max(...cr.series[1].values.map(Math.abs)), rmax = Math.max(...cr.series[0].values.map(Math.abs));
stat(s, 7.95, 1.25, 2.4, 'r = 0.62', 'first derivative, 800 nm', C.red, C.lred);
stat(s, 10.48, 1.25, 2.4, 'r = 0.46', 'reflectance, 695 nm', C.blue, C.lblue);
const mg = D.mean_grade_stage;
s.addChart(pres.charts.BAR, [{ name: 'Mean grade', labels: ['Vegetative', 'Flowering', 'Pod formation'], values: [mg.Vegetative, mg.Flowering, mg['Pod formation']] }],
  ax({ x: 7.95, y: 2.35, w: 4.93, h: 2.75, barDir: 'col', chartColors: ['66BD63', 'D9A400', 'B2182B'], title: 'Mean leaf grade by growth stage', showLegend: false, showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0.00', valAxisMinVal: 0, valAxisMaxVal: 5 }));
BL(s, ['The grade effect appears at every stage; the spectral level changes with stage.', 'Stage and date are linked (later sowings were younger on each date).'], 7.95, 5.2, 4.93, 1.1);
refline(s, 'Derivative removes leaf-to-leaf brightness differences and sharpens the red-edge shift.', 6.35, 0.45);
const { applyTheme } = require(process.env.SKILL_DIR + '/scripts/apply_theme.js');
const OUT = process.env.OUT;
pres.writeFile({ fileName: OUT }).then(async () => { await applyTheme(OUT, THEME); console.log('saved', OUT); });
