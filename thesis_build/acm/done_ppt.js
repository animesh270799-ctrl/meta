// Flow-chart deck of the UAV data-processing steps already completed (from the lab notebook, 2026).
const pptxgen = require('pptxgenjs');
const path = require('path');
const { applyTheme } = require('/root/.claude/skills/synced/9bf50f97-a337-4b6b-8c8b-ebd229b7e0d3_d565bc3b-4006-4195-b033-a8c25dfdc114/pptx/scripts/apply_theme.js');
const OUT = path.join(__dirname, '../outputs/UAV_processing_steps_done_flowcharts.pptx');
const THEME = { name: 'Processing done', headFontFace: 'Cambria', bodyFontFace: 'Calibri',
  colors: { dk1: '1F2A2A', lt1: 'FFFFFF', dk2: '1F3864', lt2: 'F2F5FA', accent1: '2E7D32', accent2: '2E75B6', accent3: 'C55A11', accent4: '7030A0', accent5: 'C00000', accent6: 'BF9000', hlink: '2E75B6', folHlink: '7030A0' } };
const X = { navy: '1F3864', done: '2E7D32', ldone: 'E8F5E9', prog: 'BF9000', lprog: 'FFF4D6', next: '7F7F7F', lnext: 'F2F2F2', envi: '2E75B6', lenvi: 'DEEBF7', arc: 'C55A11', larc: 'FCE9DC', red: 'C00000', lred: 'F9E0DE', text: '1F2A2A', grey: '595959' };
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.theme = { headFontFace: 'Cambria', bodyFontFace: 'Calibri' };
pres.title = 'UAV data processing: steps completed (flow charts)';
const C = pres.SchemeColor;
pres.defineSlideMaster({ title: 'TITLE', background: { color: X.navy }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.8, y: 2.0, w: 11.7, h: 1.7, fontSize: 38, bold: true, color: C.background1, fontFace: 'Cambria', valign: 'bottom' }, text: '' } },
  { placeholder: { options: { name: 'body', type: 'body', x: 0.8, y: 3.9, w: 11.7, h: 1.8, fontSize: 18, color: 'D6E0F0', valign: 'top' }, text: '' } }] });
pres.defineSlideMaster({ title: 'CONTENT', background: { color: 'FFFFFF' }, margin: [0.5, 0.5, 0.6, 0.5],
  slideNumber: { x: 12.4, y: 7.08, w: 0.6, h: 0.3, fontSize: 10, color: X.grey },
  objects: [{ rect: { x: 0, y: 0, w: 13.333, h: 0.08, fill: { color: X.navy } } },
            { placeholder: { options: { name: 'title', type: 'title', x: 0.45, y: 0.22, w: 12.4, h: 0.75, fontSize: 28, bold: true, color: C.text2, fontFace: 'Cambria', valign: 'middle' }, text: '' } },
            { line: { x: 0.45, y: 1.0, w: 12.43, h: 0, line: { color: X.done, width: 1.5 } } },
            { text: { text: 'UAV data processing completed  |  Animesh Panda (13098)  |  Agricultural Physics, ICAR-IARI', options: { x: 0.45, y: 7.08, w: 9.5, h: 0.3, fontSize: 10, color: X.grey } } }] });
const slide = (t) => { const s = pres.addSlide({ masterName: 'CONTENT' }); s.addText(t, { placeholder: 'title' }); return s; };
const txt = (s, t, o) => s.addText(t, Object.assign({ isTextBox: true, fontSize: 13, color: X.text, valign: 'top', margin: 3 }, o));
const bul = (s, items, o) => s.addText(items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1 } })), Object.assign({ isTextBox: true, fontSize: 13, color: X.text, paraSpaceAfter: 4, valign: 'top' }, o));
const box = (s, x, y, w, h, t, o = {}) => {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: o.fill || X.ldone }, line: { color: o.line || o.fill || X.done, width: o.lw || 1.25 }, rectRadius: 0.07, objectName: o.name || 'step' });
  s.addText(t, { isTextBox: true, x, y, w, h, fontSize: o.fs || 11.5, color: o.color || X.text, bold: !!o.bold, align: o.align || 'center', valign: o.valign || 'middle', margin: o.margin == null ? 4 : o.margin, paraSpaceAfter: 2 });
};
const arrow = (s, x1, y1, x2, y2, col, o = {}) => s.addShape(pres.shapes.LINE, { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1) || 0.001, h: Math.abs(y2 - y1) || 0.001, flipH: x2 < x1, flipV: y2 < y1,
  line: { color: col || X.grey, width: o.w || 1.75, endArrowType: o.noHead ? undefined : 'triangle' } });
const poly = (s, pts, col) => { for (let i = 0; i < pts.length - 1; i++) arrow(s, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], col, { noHead: i < pts.length - 2 }); };
const step = (title, sub) => [{ text: title, options: { bold: true, fontSize: 13, breakLine: true } }, { text: sub, options: { fontSize: 11 } }];
const tag = (s, t, col) => { s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 10.88, y: 1.06, w: 2.0, h: 0.32, fill: { color: col }, line: { color: col }, rectRadius: 0.1 }); txt(s, t, { x: 10.88, y: 1.06, w: 2.0, h: 0.32, fontSize: 12, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', margin: 0 }); };
const sw = (s, t) => txt(s, t, { x: 0.45, y: 1.05, w: 9, h: 0.3, fontSize: 12, italic: true, color: X.grey, margin: 0 });
const note = (s, t, y = 6.25, h = 0.6, col = X.prog, light = X.lprog) => { s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.45, y, w: 12.43, h, fill: { color: light }, line: { color: col, width: 1 }, rectRadius: 0.06 }); txt(s, t, { x: 0.6, y, w: 12.15, h, fontSize: 12, valign: 'middle', margin: 2 }); };
// vertical chain of steps (left), with details (right)
const chain = (s, steps, col, light, o = {}) => { const x = o.x || 0.45, w = o.w || 4.2, h = o.h || 0.62, gap = o.gap || 0.16, y0 = o.y || 1.45;
  steps.forEach((t, i) => { const y = y0 + i * (h + gap); box(s, x, y, w, h, t, { fill: light, line: col, fs: o.fs || 12 }); if (i < steps.length - 1) arrow(s, x + w / 2, y + h, x + w / 2, y + h + gap, col); }); };

// ============ 1 TITLE ============
let s = pres.addSlide({ masterName: 'TITLE' });
s.addText('UAV data processing: steps completed', { placeholder: 'title' });
s.addText('Flow charts of the work done on the 2025-26 drone data (ENVI and ArcMap): hyperspectral band selection, smoothing, projection, plot clipping, crop mask (SAM × NDVI), crop polygons and endmember extraction (SMACC)\n\nAnimesh Panda (13098), Ph.D. Agricultural Physics, ICAR-IARI', { placeholder: 'body' });

// ============ 2 OVERVIEW ============
s = slide('Overview: complete processing chain');
[['Done', X.done], ['In progress', X.prog], ['Next', X.next]].forEach((l, i) => { s.addShape(pres.shapes.RECTANGLE, { x: 8.9 + i * 1.35, y: 1.12, w: 0.25, h: 0.2, fill: { color: l[1] }, line: { color: l[1] } }); txt(s, l[0], { x: 9.2 + i * 1.35, y: 1.05, w: 1.1, h: 0.32, fontSize: 11, margin: 0 }); });
const ov = [['1', 'UAV flights', '5 sensors, 2025-26', 'd'], ['2', 'Band selection', '613 → 483 bands (ENVI)', 'd'], ['3', 'SG smoothing', 'width 5, order 2', 'd'], ['4', 'Projection', 'WGS 84 / UTM 43N', 'd'],
  ['5', 'Plot boundaries', 'shapefile, plot no., dissolve', 'd'], ['6', 'Plot clipping', '3 dates complete', 'd'], ['7', 'Training ROIs', 'soil, shadow, grass, mustard', 'd'], ['8', 'SAM + NDVI', 'angle 0.1–0.3; R898, R684', 'd'],
  ['9', 'Crop mask', 'NDVI 0.6 × SAM 0.3; erode', 'd'], ['10', 'Crop polygons', 'reclass → vector → clip', 'd'], ['11', 'Endmembers', 'SMACC per plot', 'p'], ['12', 'Plot spectra → features', 'remove non-crop; flowers?', 'n']];
ov.forEach((o, i) => { const row = Math.floor(i / 4), c = i % 4, col = row % 2 === 0 ? c : 3 - c; const x = 0.55 + col * 3.15, y = 1.55 + row * 1.75;
  const st = o[3] === 'd' ? [X.done, X.ldone] : o[3] === 'p' ? [X.prog, X.lprog] : [X.next, X.lnext];
  box(s, x, y, 2.75, 1.25, [{ text: o[0] + '. ' + o[1], options: { bold: true, fontSize: 13.5, breakLine: true } }, { text: o[2], options: { fontSize: 11 } }], { fill: st[1], line: st[0], lw: 1.75 });
  if (i < ov.length - 1) { if ((i + 1) % 4 === 0) arrow(s, x + 1.37, y + 1.25, x + 1.37, y + 1.75, X.grey); else if (row % 2 === 0) arrow(s, x + 2.75, y + 0.62, x + 3.15, y + 0.62, X.grey); else arrow(s, x, y + 0.62, x - 0.4, y + 0.62, X.grey); } });

// ============ 3 DATA ============
s = slide('Step 1: UAV data available (2025-26)'); tag(s, 'DONE', X.done);
const sens = [['RGB', 'DJI Phantom'], ['Thermal', 'FLIR Vue Pro R'], ['Multispectral', 'MicaSense RedEdge-MX'], ['Hyperspectral', 'Headwall Co-Aligned HP (VNIR + SWIR, 613 bands)'], ['Hyperspectral', 'Headwall Nano (VNIR)']];
sens.forEach((t, i) => { box(s, 0.45 + i * 2.5, 1.45, 2.3, 1.1, step(t[0], t[1]), { fill: X.lenvi, line: X.envi }); arrow(s, 1.6 + i * 2.5, 2.55, 6.65, 3.05, X.envi); });
box(s, 4.15, 3.05, 5.0, 0.8, step('IARI field, 48 plots', '12 treatments (D1–D4 × V1–V3) × 3 replications + 12 healthy'), { fill: X.ldone, line: X.done });
arrow(s, 6.65, 3.85, 6.65, 4.25, X.done);
['11 Feb 2026', '24 Feb 2026', '13 Mar 2026'].forEach((d, i) => box(s, 2.9 + i * 2.6, 4.25, 2.35, 0.7, d, { fill: X.done, line: X.done, color: 'FFFFFF', bold: true, fs: 14 }));
txt(s, 'Hyperspectral dates processed so far (7 flight dates acquired per sensor)', { x: 2.9, y: 5.0, w: 7.6, h: 0.3, fontSize: 11, italic: true, color: X.grey, align: 'center' });
note(s, 'Checks noted: multispectral pixel values — DN, radiance or scaled reflectance? (read the metadata); thermal images — has emissivity correction been applied?', 5.55, 0.6, X.red, X.lred);

// ============ 4 BAND SELECTION ============
s = slide('Step 2: hyperspectral band selection (ENVI)'); tag(s, 'DONE', X.done); sw(s, 'Software: ENVI  |  noted 24 Feb 2026 and 6 Jul 2026');
chain(s, ['Open Headwall Co-Aligned cube (613 bands)', 'File → Save As → ENVI format', 'Spectral subset: VNIR up to 919.72 nm + SWIR from 921.37 nm', 'Remove water-sensitive and noisy bands', 'Save reduced cube: 483 bands'], X.envi, X.lenvi, { y: 1.5, h: 0.72, gap: 0.2 });
// wavelength bar
{ const x0 = 5.2, x1 = 12.75, y = 2.2, wl = (w) => x0 + (w - 400) / 2100 * (x1 - x0);
  txt(s, 'Bands kept (green) and removed (red), 400–2500 nm', { x: x0, y: 1.5, w: 7.5, h: 0.3, fontSize: 12, bold: true, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: x0, y, w: x1 - x0, h: 0.55, fill: { color: '81C784' }, line: { color: X.done } });
  [[900, 915], [1335, 1460], [1785, 1965], [2400, 2500]].forEach(r => s.addShape(pres.shapes.RECTANGLE, { x: wl(r[0]), y, w: wl(r[1]) - wl(r[0]), h: 0.55, fill: { color: 'E57373' }, line: { color: X.red } }));
  s.addShape(pres.shapes.LINE, { x: wl(920.5), y: y - 0.15, w: 0.001, h: 0.85, line: { color: X.navy, width: 2, dashType: 'dash' } });
  [400, 800, 1200, 1600, 2000, 2400].forEach(w => txt(s, w + '', { x: wl(w) - 0.3, y: y + 0.58, w: 0.6, h: 0.25, fontSize: 10, align: 'center', margin: 0, color: X.grey }));
  txt(s, 'nm', { x: x1 - 0.3, y: y + 0.8, w: 0.4, h: 0.25, fontSize: 10, margin: 0, color: X.grey });
  txt(s, 'VNIR | SWIR join (919.7 / 921.4 nm)', { x: wl(920) - 1.6, y: y - 0.45, w: 3.2, h: 0.28, fontSize: 10, align: 'center', color: X.navy, margin: 0 }); }
s.addTable([[{ text: 'Removed region (nm)', options: { bold: true, color: 'FFFFFF', fill: { color: X.envi } } }, { text: 'Reason', options: { bold: true, color: 'FFFFFF', fill: { color: X.envi } } }],
  ['900–915', 'Noisy end of the VNIR detector / detector overlap'], ['1335–1460', 'Atmospheric water-vapour absorption (≈ 1400 nm)'], ['1785–1965', 'Atmospheric water-vapour absorption (≈ 1900 nm); also 1964.4 nm'], ['2400–2500 (and > 2500)', 'Low signal, noisy SWIR end']],
  { x: 5.2, y: 3.4, w: 7.55, colW: [2.4, 5.15], fontSize: 12, border: { type: 'solid', pt: 0.5, color: 'C9CED6' }, rowH: 0.42 });
note(s, 'Result: 613 → 483 bands in every cube. These regions are removed for UAV data because sunlight passes through the atmosphere twice (Thenkabail et al., 2004).', 6.15, 0.6, X.done, X.ldone);

// ============ 5 SMOOTHING ============
s = slide('Step 3: Savitzky–Golay smoothing (ENVI)'); tag(s, 'DONE', X.done); sw(s, 'Software: ENVI toolbox');
chain(s, ['Open the 483-band cube', 'Toolbox → search "Spectral smoothing"', 'Savitzky–Golay filter: filter width 5, polynomial degree 2', 'OK → export smoothed cube'], X.envi, X.lenvi, { y: 1.5, h: 0.85, gap: 0.3, w: 5.2 });
s.addShape(pres.shapes.RECTANGLE, { x: 6.2, y: 1.5, w: 6.68, h: 4.3, fill: { color: X.lnext }, line: { color: 'C9CED6' } });
txt(s, 'What the filter does', { x: 6.35, y: 1.6, w: 6.4, h: 0.35, fontSize: 14, bold: true, color: X.navy });
bul(s, ['Fits a 2nd-order polynomial to each moving window of 5 bands and keeps the fitted centre value', 'Removes random sensor noise but keeps the shape of absorption features (red edge, water bands)', 'Needed before derivatives (FD, SD), which amplify noise', 'Small window (5) chosen so narrow features are not flattened'], { x: 6.35, y: 2.05, w: 6.4, h: 3.6, fontSize: 13.5 });
note(s, 'Reference: Savitzky and Golay, 1964. Output: smoothed 483-band reflectance cube for each date.', 6.15, 0.55, X.done, X.ldone);

// ============ 6 PROJECTION + CLIPPING ============
s = slide('Step 4: projection and clipping to the field (ArcMap)'); tag(s, 'DONE', X.done); sw(s, 'Software: ArcMap (ArcGIS)');
chain(s, ['Search → Project (Data Management)', 'Output coordinate system: WGS 1984 / UTM zone 43N', 'Take reflectance image from the reflectance folder'], X.arc, X.larc, { y: 1.5, h: 0.75, gap: 0.3, w: 4.0 });
chain(s, ['Catalog → folder → New → Shapefile (polygon, UTM 43N)', 'Editor → Start editing → Create features → draw polygon', 'Save edits → Stop editing'], X.arc, X.larc, { x: 4.65, y: 1.5, h: 0.75, gap: 0.3, w: 4.0 });
chain(s, ['Search → Extract by Mask (Spatial Analyst)', 'Input raster = image; mask = shapefile', 'Save clipped reflectance file (default location if error) → Data → Export'], X.arc, X.larc, { x: 8.85, y: 1.5, h: 0.75, gap: 0.3, w: 4.0 });
arrow(s, 4.45, 1.87, 4.65, 1.87, X.arc); arrow(s, 8.65, 1.87, 8.85, 1.87, X.arc);
['A. Re-project', 'B. Draw field boundary', 'C. Clip image'].forEach((t, i) => txt(s, t, { x: [0.45, 4.65, 8.85][i], y: 4.7, w: 4.0, h: 0.35, fontSize: 13, bold: true, color: X.arc, align: 'center' }));
note(s, 'Output: field-clipped, projected images for each date (same coordinate system for all sensors, so the masks and plot polygons can be shared).', 5.6, 0.6, X.done, X.ldone);

// ============ 7 PLOT BOUNDARIES ============
s = slide('Step 5: plot boundaries and plot numbers (ArcMap → ENVI)'); tag(s, 'DONE', X.done); sw(s, 'Noted 20–21 May 2026');
chain(s, ['Digitise the 48 plot polygons', 'Add field "plot no." → select each polygon → set its number', 'Save edits', 'Dissolve (Data Management) by plot → merged plot polygons', 'Final boundary layer saved as shapefile (.dat image for ENVI)'], X.arc, X.larc, { y: 1.45, h: 0.68, gap: 0.2, w: 5.6 });
chain(s, ['Open original image + boundary shapefile in ENVI', 'Subset data from ROI / shapefile ("keep" = yes)', 'Save as subset file (one per plot / date)', 'Image enhancement: linear stretch; chip view to file (JPEG figures)'], X.envi, X.lenvi, { x: 6.5, y: 1.45, h: 0.8, gap: 0.25, w: 6.38 });
arrow(s, 6.05, 1.8, 6.5, 1.85, X.grey);
note(s, 'Status: clipping complete for all three dates (11 Feb, 24 Feb and 13 Mar 2026).', 6.0, 0.55, X.done, X.ldone);

// ============ 8 ROIs ============
s = slide('Step 6: training regions of interest (ENVI)'); tag(s, 'DONE', X.done); sw(s, 'Noted 12 May 2026');
const cls = [['Soil', '8D6E63'], ['Shadow', '424242'], ['Grass / weeds', '9CCC65'], ['Mustard (+ flower)', '2E7D32']];
cls.forEach((c, i) => { box(s, 0.45 + i * 3.15, 1.5, 2.9, 0.9, c[0], { fill: c[1], line: c[1], color: 'FFFFFF', bold: true, fs: 16 }); arrow(s, 1.9 + i * 3.15, 2.4, 6.65, 2.85, X.grey); });
box(s, 3.65, 2.85, 6.0, 0.9, step('ROIs drawn in every plot', '3 × 2 training sites per plot; 48 plot ROIs'), { fill: X.lenvi, line: X.envi });
arrow(s, 6.65, 3.75, 6.65, 4.1, X.envi);
box(s, 3.65, 4.1, 6.0, 0.8, step('ROIs saved / exported as vector', 'used for SAM classification (Step 7)'), { fill: X.lenvi, line: X.envi });
txt(s, 'True-colour display bands: R 640–670 nm, G 540–570 nm, B 460–480 nm (≈ 644, 544, 466 nm)', { x: 0.45, y: 5.2, w: 12.43, h: 0.35, fontSize: 13, align: 'center', color: X.grey });
note(s, 'Crop stage differed among plots on one date: 16 vegetative, 22 flowering, 10 pod-formation plots (sowing-date effect).', 5.75, 0.55);

// ============ 9 SAM + NDVI ============
s = slide('Step 7: SAM classification and NDVI (ENVI)'); tag(s, 'DONE', X.done); sw(s, 'Noted 12 May 2026');
txt(s, 'A. Spectral Angle Mapper', { x: 0.45, y: 1.4, w: 6.0, h: 0.35, fontSize: 15, bold: true, color: X.envi });
chain(s, ['Classification → SAM classifier', 'Import ROIs from input → select all → OK', 'Select all plots', 'Maximum spectral angle: 0.1, 0.2, 0.3 rad tested', 'Save classified image'], X.envi, X.lenvi, { y: 1.85, h: 0.62, gap: 0.18, w: 6.0 });
txt(s, 'B. NDVI', { x: 6.88, y: 1.4, w: 6.0, h: 0.35, fontSize: 15, bold: true, color: X.done });
chain(s, ['Band Math: (b1 − b2) / (b1 + b2)', 'b1 = NIR band at 898 nm (≈ 900 nm)', 'b2 = red band at 684 nm (≈ 685 nm)', 'Save NDVI as GeoTIFF'], X.done, X.ldone, { x: 6.88, y: 1.85, h: 0.75, gap: 0.2, w: 6.0 });
note(s, 'SAM compares the angle between each pixel spectrum and the class spectra; a smaller angle = more similar, independent of brightness (Kruse et al., 1993). NDVI = (NIR − Red)/(NIR + Red) (Rouse et al., 1974).', 6.0, 0.7, X.envi, X.lenvi);

// ============ 10 MASK ============
s = slide('Step 8: crop mask = NDVI mask × SAM mask'); tag(s, 'DONE', X.done); sw(s, 'Noted in notebook p. 049 and p. 057');
box(s, 0.45, 1.6, 3.0, 1.1, step('NDVI mask', 'NDVI > 0.6 → 1, else 0'), { fill: X.ldone, line: X.done });
box(s, 0.45, 3.2, 3.0, 1.1, step('SAM mask', 'mustard class at 0.3 rad → 1, else 0'), { fill: X.lenvi, line: X.envi });
box(s, 4.15, 2.3, 2.6, 1.3, step('Multiply', 'NDVI mask × SAM mask'), { fill: X.navy, line: X.navy, color: 'FFFFFF' });
arrow(s, 3.45, 2.15, 4.15, 2.75, X.done); arrow(s, 3.45, 3.75, 4.15, 3.15, X.envi);
box(s, 7.35, 2.3, 2.5, 1.3, step('Morphology: erode', 'removes mixed pixels at plot and canopy edges'), { fill: X.lnext, line: X.next });
box(s, 10.4, 2.3, 2.48, 1.3, step('Crop mask (.tif)', '1 = mustard canopy, 0 = background'), { fill: X.ldone, line: X.done, lw: 2 });
arrow(s, 6.75, 2.95, 7.35, 2.95, X.navy); arrow(s, 9.85, 2.95, 10.4, 2.95, X.navy);
bul(s, ['A pixel is kept only if it is green (NDVI) AND spectrally similar to mustard (SAM): removes soil, shadow and weeds', 'Thresholds 0.6 (NDVI) and 0.3 rad (SAM) follow the agreed methodology'], { x: 0.45, y: 4.75, w: 12.43, h: 1.1, fontSize: 13.5 });
note(s, 'Output: binary crop mask per date, applied to all sensors after co-registration.', 6.0, 0.55, X.done, X.ldone);

// ============ 11 VECTOR ============
s = slide('Step 9: crop polygons from the classified raster (ArcMap)'); tag(s, 'DONE', X.done); sw(s, 'Noted 12 May 2026 (p. 047–048, 057)');
const vv = [['Reclassify', 'others = 1, mustard = 2'], ['Raster to Polygon', '"Simplify polygons" unchecked'], ['Select by Attribute', 'gridcode = mustard class'], ['Clip (Analysis)', 'crop polygons to plot boundaries'], ['Data → Export', 'shapefile in own folder']];
vv.forEach((v, i) => { const x = 0.45 + i * 2.53; box(s, x, 1.6, 2.28, 1.35, step(v[0], v[1]), { fill: X.larc, line: X.arc }); if (i < 4) arrow(s, x + 2.28, 2.27, x + 2.53, 2.27, X.arc); });
box(s, 0.45, 3.4, 6.0, 1.0, step('Editing (if needed)', 'Explode multipart feature; cut polygon tool; select by attribute → keep the required part'), { fill: X.lnext, line: X.next });
box(s, 6.88, 3.4, 6.0, 1.0, step('Also: features to raster', 'crop polygons converted back to a raster mask when needed'), { fill: X.lnext, line: X.next });
note(s, 'Output: mustard-only polygons for each plot and date — used to extract plot spectra and for endmember extraction.', 4.9, 0.6, X.done, X.ldone);

// ============ 12 SMACC ============
s = slide('Step 10: endmember extraction per plot (ENVI, SMACC)'); tag(s, 'IN PROGRESS', X.prog); sw(s, 'Noted 21 May 2026 and 8 Jul 2026 (24 Feb 2026 image)');
chain(s, ['Open subset cube (.hdr, 483 bands)', 'Import plot boundary file as ROIs → each plot a separate ROI (48)', 'Subset data from ROI → plot 1 (keep = yes)', 'Run SMACC on plot 1 → save outputs', 'Choose plot 2 → SMACC → … repeat for all plots'], X.prog, X.lprog, { y: 1.45, h: 0.68, gap: 0.2, w: 6.0 });
box(s, 6.88, 1.45, 6.0, 1.7, [{ text: 'SMACC outputs (per plot)', options: { bold: true, fontSize: 13.5, breakLine: true } }, { text: 'Spectral library of endmembers (in memory) • abundance maps • ROIs of endmember pixels • signatures exported to desktop', options: { fontSize: 12 } }], { fill: X.lprog, line: X.prog, align: 'left', margin: 8 });
box(s, 6.88, 3.4, 6.0, 1.5, [{ text: 'Why SMACC', options: { bold: true, fontSize: 13.5, breakLine: true } }, { text: 'Finds the purest spectra (endmembers) of a plot automatically — crop, chlorotic/pustule leaf, soil, shadow, flower — and their abundance in each pixel (Gruninger et al., 2004)', options: { fontSize: 12 } }], { fill: X.lenvi, line: X.envi, align: 'left', margin: 8 });
note(s, 'Issue noted: ROI drawn by hand around a plot was not proper → use the plot boundary shapefile to create plot ROIs.', 5.75, 0.55, X.red, X.lred);


// ============ 12b DATASET + CUBE CHECK ============
s = slide('Dataset structure: dates, sensors, plots and subplots');
{ const lv = [['7 flight dates', 'all four sensors on each date'], ['4 sensors', 'HS, MS, RGB, thermal → 28 images'], ['48 plots per image', '12 treatments × 3 replications + 12 healthy'], ['4 subplots per plot', 'quadrants inside the crop mask']];
  lv.forEach((l, i) => { const y = 1.45 + i * 1.1; box(s, 0.45 + i * 0.35, y, 4.3, 0.88, [{ text: l[0], options: { bold: true, fontSize: 14, breakLine: true } }, { text: l[1], options: { fontSize: 11 } }], { fill: X.done, line: X.done, color: 'FFFFFF' });
    if (i < 3) arrow(s, 2.6 + i * 0.35, y + 0.88, 2.95 + i * 0.35, y + 1.1, X.grey); }); }
s.addTable([[{ text: 'Level', options: { bold: true, color: 'FFFFFF', fill: { color: X.navy } } }, { text: 'Per sensor', options: { bold: true, color: 'FFFFFF', fill: { color: X.navy } } }, { text: 'All 4 sensors', options: { bold: true, color: 'FFFFFF', fill: { color: X.navy } } }],
  ['Images', '7', '28'], ['Plot-dates', '336', '1344'], ['Subplot-dates', '1344', '5376'], ['Subplot-dates per date', '192', '768']], { x: 5.9, y: 1.45, w: 6.98, colW: [2.98, 2.0, 2.0], fontSize: 13, border: { type: 'solid', pt: 0.5, color: 'C9CED6' }, rowH: 0.45, align: 'center' });
bul(s, ['Unit for models: subplot-date (mean of crop pixels in each subplot)', 'Label: canopy-level disease severity score of each subplot, recorded in the field (1344 labelled subplot-dates)', 'The four subplots of a plot stay in the same validation fold; statistics use plot means or a mixed model'], { x: 5.9, y: 3.95, w: 6.98, h: 1.8, fontSize: 13 });
note(s, 'Status: 7 images per sensor available; hyperspectral cubes processed so far are listed in Steps 2–10.', 6.15, 0.5);

s = slide('Hyperspectral cube check (24 Feb 2026 header)'); tag(s, 'CHECK', X.red); sw(s, 'File subset_200526.hdr: Applied Mask Result, 20 May 2026');
s.addTable([[{ text: 'Item', options: { bold: true, color: 'FFFFFF', fill: { color: X.envi } } }, { text: 'Value in the header', options: { bold: true, color: 'FFFFFF', fill: { color: X.envi } } }],
  ['Size', '2355 × 2142 pixels × 483 bands; float32; BIL; ≈ 9.75 GB per date'], ['VNIR', '399.4–919.7 nm, 288 bands at 1.76 nm (gap 898.6–916.2 nm)'], ['SWIR', '921.4–2397.6 nm, 195 bands at 6 nm (gaps 1329.4–1461.4 and 1779.5–1971.5 nm)'],
  ['Pixel', '≈ 2.2 cm × 2.2 cm (resampled grid; native ≈ 9.7 cm VNIR, 36 cm SWIR)'], ['Coordinates', 'Geographic Lat/Lon, WGS-84 (not UTM)']], { x: 0.45, y: 1.5, w: 6.3, colW: [1.35, 4.95], fontSize: 12, border: { type: 'solid', pt: 0.5, color: 'C9CED6' }, rowH: 0.5 });
const fixes = [['Smoothing across gaps', 'SG (width 5) was run on the reduced cube, so each window near 899–916, 919.7/921.4, 1329–1461 and 1779–1971 nm mixes distant wavelengths → smooth each segment separately, or drop 2 bands on each side of every gap'],
  ['Isolated bands', '916.2–919.7 nm (3 VNIR bands at the detector edge) → drop'], ['Projection', 'Re-project to WGS 84 / UTM 43N before erosion and subplot splitting in metres'],
  ['Resolution', 'Do not compute texture on HS (2.2 cm grid over 9.7–36 cm pixels); use subplot mean spectra'], ['Data volume', '≈ 68 GB for 7 dates → extract subplot means date by date with a script']];
fixes.forEach((f, i) => box(s, 7.0, 1.5 + i * 0.93, 5.88, 0.82, [{ text: f[0] + ': ', options: { bold: true, color: X.red } }, { text: f[1] }], { fill: X.lred, line: X.red, fs: 10.5, align: 'left', margin: 6 }));
note(s, 'Band selection and the 483-band count match the notebook; the points on the right should be fixed before features are extracted.', 6.35, 0.5, X.done, X.ldone);
// ============ 13 NEXT ============
s = slide('Next steps and open questions'); tag(s, 'NEXT', X.next);
const nx = [['Label endmembers', 'crop (green, chlorotic, pustule) vs non-crop (soil, shadow, grass) by NDVI and spectral angle'], ['Plot spectrum', 'remove non-crop endmembers; average crop endmembers'], ['All dates and sensors', 'repeat for 11 Feb, 24 Feb, 13 Mar; RGB, MS, TIR, Nano'], ['Features and tiers', 'Objective 1: bands, derivatives, indices, White Rust Index …'], ['Healthy vs diseased', 'compare endmember spectra of healthy (H) and diseased (D1, D2) plots']];
nx.forEach((n, i) => { const y = 1.35 + i * 0.85; box(s, 0.45, y, 6.6, 0.7, [{ text: n[0] + ': ', options: { bold: true } }, { text: n[1] }], { fill: X.lnext, line: X.next, align: 'left', fs: 12, margin: 6 }); if (i < 4) arrow(s, 3.75, y + 0.7, 3.75, y + 0.85, X.next); });
box(s, 7.4, 1.35, 5.48, 2.35, [{ text: 'Open question: keep or remove flowers?', options: { bold: true, fontSize: 13.5, breakLine: true } }, { text: 'Proposal: remove flower endmembers/pixels from the leaf spectrum (yellow petals dominate 500–650 nm and flowering differs with sowing date and variety); keep the flower fraction as a covariate; keep inflorescence pixels for staghead severity (Sulik and Long, 2016)', options: { fontSize: 12 } }], { fill: X.lred, line: X.red, align: 'left', margin: 8 });
box(s, 7.4, 3.9, 5.48, 1.6, [{ text: 'Data checks', options: { bold: true, fontSize: 13.5, breakLine: true } }, { text: 'Multispectral values: DN, radiance or reflectance? • Thermal emissivity correction? • Same 483 bands in every subset cube', options: { fontSize: 12 } }], { fill: X.lred, line: X.red, align: 'left', margin: 8 });

// ============ 14 TIMELINE ============
s = slide('Timeline of work done (from the notebook)');
const tl = [['24 Feb 2026', 'ENVI processing plan: band removal list, SG smoothing, save as ENVI'], ['12 May 2026', 'ROIs (soil, shadow, grass, mustard); SAM (0.1–0.3 rad) and NDVI (898, 684 nm); raster to vector'], ['20 May 2026', 'Clipping complete for all three dates; boundary layer saved as shapefile'], ['21 May 2026', 'Plot numbers, dissolve/merge, subsetting; SMACC started plot by plot'], ['6 Jul 2026', 'Hyperspectral processing of the 13 Mar 2026 image: 613 → 483 bands, SG filter'], ['8 Jul 2026', 'Endmember extraction (SMACC) for the 24 Feb 2026 image']];
s.addShape(pres.shapes.LINE, { x: 1.9, y: 1.4, w: 0.001, h: 5.2, line: { color: X.done, width: 3 } });
tl.forEach((t, i) => { const y = 1.45 + i * 0.86; s.addShape(pres.shapes.OVAL, { x: 1.77, y: y + 0.12, w: 0.26, h: 0.26, fill: { color: i < 5 ? X.done : X.prog }, line: { color: 'FFFFFF', width: 1.5 } });
  txt(s, t[0], { x: 0.25, y, w: 1.45, h: 0.5, fontSize: 12.5, bold: true, color: X.navy, align: 'right', valign: 'middle' });
  box(s, 2.3, y, 10.58, 0.55, t[1], { fill: i < 5 ? X.ldone : X.lprog, line: i < 5 ? X.done : X.prog, align: 'left', fs: 12.5, margin: 8 }); });

// ============ 15 REFS ============
s = slide('References');
bul(s, ['Gruninger, J., Ratkowski, A.J., Hoke, M.L. (2004). The sequential maximum angle convex cone (SMACC) endmember model. Proceedings of SPIE 5425, Algorithms and Technologies for Multispectral, Hyperspectral, and Ultraspectral Imagery X, 1–14.',
  'Kruse, F.A., Lefkoff, A.B., Boardman, J.W., Heidebrecht, K.B., Shapiro, A.T., Barloon, P.J., Goetz, A.F.H. (1993). The spectral image processing system (SIPS) – interactive visualization and analysis of imaging spectrometer data. Remote Sensing of Environment 44(2–3), 145–163.',
  'Rouse, J.W., Haas, R.H., Schell, J.A., Deering, D.W. (1974). Monitoring vegetation systems in the Great Plains with ERTS. Third ERTS Symposium, NASA SP-351, 309–317.',
  'Savitzky, A., Golay, M.J.E. (1964). Smoothing and differentiation of data by simplified least squares procedures. Analytical Chemistry 36(8), 1627–1639.',
  'Sulik, J.J., Long, D.S. (2016). Spectral considerations for modeling yield of canola. Remote Sensing of Environment 184, 161–174.',
  'Thenkabail, P.S., Enclona, E.A., Ashton, M.S., Van Der Meer, B. (2004). Accuracy assessments of hyperspectral waveband performance for vegetation analysis applications. Remote Sensing of Environment 91(3–4), 354–376.'], { x: 0.45, y: 1.3, w: 12.43, h: 5.5, fontSize: 13 });
pres.writeFile({ fileName: OUT }).then(async () => { await applyTheme(OUT, THEME); console.log('saved', OUT); });
