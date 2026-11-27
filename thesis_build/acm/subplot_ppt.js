// Flow-chart deck of the UAV data-processing steps already completed (from the lab notebook, 2026).
const pptxgen = require('pptxgenjs');
const path = require('path');
const { applyTheme } = require('/root/.claude/skills/synced/9bf50f97-a337-4b6b-8c8b-ebd229b7e0d3_d565bc3b-4006-4195-b033-a8c25dfdc114/pptx/scripts/apply_theme.js');
const OUT = path.join(__dirname, '../outputs/Subplot_spectra_hourglass_SAM_workflow.pptx');
const THEME = { name: 'Processing done', headFontFace: 'Cambria', bodyFontFace: 'Calibri',
  colors: { dk1: '1F2A2A', lt1: 'FFFFFF', dk2: '1F3864', lt2: 'F2F5FA', accent1: '2E7D32', accent2: '2E75B6', accent3: 'C55A11', accent4: '7030A0', accent5: 'C00000', accent6: 'BF9000', hlink: '2E75B6', folHlink: '7030A0' } };
const X = { navy: '1F3864', done: '2E7D32', ldone: 'E8F5E9', prog: 'BF9000', lprog: 'FFF4D6', next: '7F7F7F', lnext: 'F2F2F2', envi: '2E75B6', lenvi: 'DEEBF7', arc: 'C55A11', larc: 'FCE9DC', red: 'C00000', lred: 'F9E0DE', text: '1F2A2A', grey: '595959' };
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.theme = { headFontFace: 'Cambria', bodyFontFace: 'Calibri' };
pres.title = 'From hyperspectral cube to subplot spectra (hourglass + SAM)';
const C = pres.SchemeColor;
pres.defineSlideMaster({ title: 'TITLE', background: { color: X.navy }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.8, y: 2.0, w: 11.7, h: 1.7, fontSize: 38, bold: true, color: C.background1, fontFace: 'Cambria', valign: 'bottom' }, text: '' } },
  { placeholder: { options: { name: 'body', type: 'body', x: 0.8, y: 3.9, w: 11.7, h: 1.8, fontSize: 18, color: 'D6E0F0', valign: 'top' }, text: '' } }] });
pres.defineSlideMaster({ title: 'CONTENT', background: { color: 'FFFFFF' }, margin: [0.5, 0.5, 0.6, 0.5],
  slideNumber: { x: 12.4, y: 7.08, w: 0.6, h: 0.3, fontSize: 10, color: X.grey },
  objects: [{ rect: { x: 0, y: 0, w: 13.333, h: 0.08, fill: { color: X.navy } } },
            { placeholder: { options: { name: 'title', type: 'title', x: 0.45, y: 0.22, w: 12.4, h: 0.75, fontSize: 28, bold: true, color: C.text2, fontFace: 'Cambria', valign: 'middle' }, text: '' } },
            { line: { x: 0.45, y: 1.0, w: 12.43, h: 0, line: { color: X.done, width: 1.5 } } },
            { text: { text: 'Subplot spectra workflow  |  Animesh Panda (13098)  |  Agricultural Physics, ICAR-IARI', options: { x: 0.45, y: 7.08, w: 9.5, h: 0.3, fontSize: 10, color: X.grey } } }] });
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
s.addText('From hyperspectral cube to subplot spectra', { placeholder: 'title' });
s.addText('Hourglass endmembers (MNF → PPI → n-D) + SAM classification → one mean spectrum per subplot (leaf + flower pixels, no unmixing) → feature selection\n\nAnimesh Panda (13098), Ph.D. Agricultural Physics, ICAR-IARI', { placeholder: 'body' });

// ============ 2 GOAL ============
s = slide('Goal and data');
box(s, 0.45, 1.35, 6.0, 1.6, [{ text: 'Goal', options: { bold: true, fontSize: 16, color: X.done, breakLine: true } }, { text: 'One average spectrum for every subplot that represents the canopy disease severity scored for that subplot', options: { fontSize: 14 } }], { fill: X.ldone, line: X.done, align: 'left', margin: 10 });
[['7', 'flight dates'], ['48', 'plots per image'], ['4', 'subplots per plot'], ['1344', 'subplot spectra per sensor, each with a canopy severity score']].forEach((c, i) => { const x = 6.75 + (i % 2) * 3.1, y = 1.35 + Math.floor(i / 2) * 1.75;
  box(s, x, y, 2.9, 1.55, [{ text: c[0], options: { bold: true, fontSize: 30, color: X.navy, breakLine: true } }, { text: c[1], options: { fontSize: 12 } }], { fill: X.lnext, line: X.lnext }); });
s.addTable([[{ text: 'Hyperspectral cube (24 Feb 2026)', options: { bold: true, color: 'FFFFFF', fill: { color: X.envi } } }, { text: 'Value', options: { bold: true, color: 'FFFFFF', fill: { color: X.envi } } }],
  ['Bands', '483: VNIR 399–920 nm (1.76 nm), SWIR 921–2398 nm (6 nm)'], ['Pixel', '≈ 2.2 cm (2355 × 2142 pixels)'], ['Masked', 'crop mask applied (SAM × NDVI)']], { x: 0.45, y: 3.3, w: 6.0, colW: [2.6, 3.4], fontSize: 12, border: { type: 'solid', pt: 0.5, color: 'C9CED6' }, rowH: 0.45 });
note(s, 'Same subplot boundaries and pixel selection are then applied to the co-registered RGB, multispectral and thermal images.', 6.0, 0.55, X.done, X.ldone);

// ============ 3 OVERALL FLOW ============
s = slide('Workflow overview');
const wf = [['Cube checks', 'smooth each band segment separately; drop 916–920 nm; reproject to UTM 43N', X.red, X.lred], ['Hourglass', 'MNF → PPI → n-D → field-wide endmember library (all 7 dates)', X.envi, X.lenvi], ['SAM classification', 'every pixel → canopy, stressed canopy, flower, soil, shadow', X.envi, X.lenvi],
  ['Vegetation pixels', 'keep canopy + stressed + flower; remove soil and shadow', X.done, X.ldone], ['Subplots', '4 quadrants per plot; edge pixels removed (erosion)', X.arc, X.larc], ['Subplot spectrum', 'mean reflectance of vegetation pixels in each subplot', X.done, X.ldone],
  ['Feature table', '1344 rows: spectrum features + severity score + flower % + canopy cover %', X.prog, X.lprog], ['Feature selection', 'Objective 1 tiers → Objectives 2 and 3 models', X.navy, X.lnext]];
wf.forEach((w, i) => { const row = Math.floor(i / 4), c = i % 4, col = row === 0 ? c : 3 - c; const x = 0.55 + col * 3.15, y = 1.45 + row * 2.45;
  box(s, x, y, 2.75, 1.85, [{ text: (i + 1) + '. ' + w[0], options: { bold: true, fontSize: 14, breakLine: true } }, { text: w[1], options: { fontSize: 11.5 } }], { fill: w[3], line: w[2], lw: 1.75 });
  if (i < 7) { if (i === 3) arrow(s, x + 1.37, y + 1.85, x + 1.37, y + 2.45, X.grey); else if (row === 0) arrow(s, x + 2.75, y + 0.92, x + 3.15, y + 0.92, X.grey); else arrow(s, x, y + 0.92, x - 0.4, y + 0.92, X.grey); } });

// ============ 4 HOURGLASS ============
s = slide('Step 2: hourglass endmembers (MNF → PPI → n-D)');
const hgs = [['MNF', 'noise-whitened components ordered by signal-to-noise; eigenvalues ≈ 1 = noise (Green et al., 1988)'], ['PPI', '10 000 random projections in MNF space; pixels often at the extremes = pure pixels (Boardman et al., 1995)'], ['n-D visualization', 'clusters at the corners of the pixel cloud; each endmember = mean of its cluster'], ['Identify', 'name endmembers with field photos, RGB and ASD leaf spectra']];
hgs.forEach((h, i) => { const x = 0.45 + i * 3.15; box(s, x, 1.5, 2.9, 1.9, step(h[0], h[1]), { fill: X.lenvi, line: X.envi }); if (i < 3) arrow(s, x + 2.9, 2.45, x + 3.15, 2.45, X.envi); });
[['Green canopy', '2E7D32'], ['Stressed canopy', '9E9D24'], ['Yellow flower', 'F9A825'], ['Soil', '8D6E63'], ['Shadow', '424242']].forEach((e, i) => box(s, 0.45 + i * 2.5, 3.85, 2.3, 0.75, e[0], { fill: e[1], line: e[1], color: 'FFFFFF', bold: true, fs: 14 }));
txt(s, 'Expected endmember classes (the notebook extracts 8 endmembers; similar ones are merged after identification)', { x: 0.45, y: 4.65, w: 12.43, h: 0.3, fontSize: 11.5, italic: true, color: X.grey, align: 'center' });
note(s, 'Build the library once from pixels sampled on all 7 dates, so every date is classified with the same reference spectra.', 5.4, 0.55, X.envi, X.lenvi);
note(s, 'Why not per-plot SMACC: SMACC gives a different set of endmembers in every plot, so plots and dates could not be compared.', 6.1, 0.55, X.prog, X.lprog);

// ============ 5 SAM + PIXEL SELECTION ============
s = slide('Steps 3–4: SAM classification and vegetation pixels');
box(s, 0.45, 1.45, 4.0, 1.7, step('SAM classification', 'class of each pixel = endmember with the smallest spectral angle; angle threshold calibrated on labelled pixels (Kruse et al., 1993)'), { fill: X.lenvi, line: X.envi });
arrow(s, 4.45, 2.3, 4.85, 2.3, X.grey);
box(s, 4.85, 1.45, 3.9, 0.8, step('Kept', 'green canopy, stressed canopy, yellow flower'), { fill: X.ldone, line: X.done });
box(s, 4.85, 2.35, 3.9, 0.8, step('Removed', 'soil, shadow (and unclassified)'), { fill: X.lred, line: X.red });
arrow(s, 8.75, 1.85, 9.15, 2.3, X.done);
box(s, 9.15, 1.45, 3.73, 1.7, step('Vegetation mask', 'kept pixels × eroded crop mask; same mask transferred to RGB, MS, TIR'), { fill: X.ldone, line: X.done, lw: 2 });
bul(s, ['Rule change: the earlier NDVI > 0.6 test removes yellow flower pixels (petals have low NDVI) → use NDVI > 0.6 OR flower class', 'Stressed (chlorotic) canopy is kept because it carries the disease signal', 'Edge erosion removes mixed leaf–soil pixels at canopy and plot borders'], { x: 0.45, y: 3.5, w: 12.43, h: 1.8, fontSize: 14 });
note(s, 'No unmixing: each pixel is either kept or removed; the subplot spectrum is a simple average of kept pixels.', 5.75, 0.55, X.done, X.ldone);

// ============ 6 SUBPLOT SPECTRUM ============
s = slide('Steps 5–6: subplot spectrum');
{ const x0 = 0.6, y0 = 1.5, w = 4.2, h = 3.6;
  s.addShape(pres.shapes.RECTANGLE, { x: x0, y: y0, w, h, fill: { color: X.ldone }, line: { color: X.done, width: 2 } });
  s.addShape(pres.shapes.RECTANGLE, { x: x0 + 0.25, y: y0 + 0.25, w: w - 0.5, h: h - 0.5, fill: { type: 'none' }, line: { color: X.red, width: 1, dashType: 'dash' } });
  s.addShape(pres.shapes.LINE, { x: x0 + w / 2, y: y0 + 0.25, w: 0.001, h: h - 0.5, line: { color: X.navy, width: 1.5 } });
  s.addShape(pres.shapes.LINE, { x: x0 + 0.25, y: y0 + h / 2, w: w - 0.5, h: 0.001, line: { color: X.navy, width: 1.5 } });
  ['S1', 'S2', 'S3', 'S4'].forEach((t, i) => txt(s, t, { x: x0 + 0.25 + (i % 2) * (w - 0.5) / 2, y: y0 + 0.25 + Math.floor(i / 2) * (h - 0.5) / 2, w: (w - 0.5) / 2, h: (h - 0.5) / 2, fontSize: 22, bold: true, color: X.navy, align: 'center', valign: 'middle' }));
  txt(s, 'Plot: 4 subplots (quadrants); dashed line = eroded edge', { x: x0, y: y0 + h + 0.05, w, h: 0.3, fontSize: 11, italic: true, color: X.grey, align: 'center' }); }
box(s, 5.3, 1.5, 7.58, 1.25, [{ text: 'Subplot spectrum', options: { bold: true, fontSize: 14, breakLine: true } }, { text: 'R_subplot(λ) = (1/N) Σ R_i(λ),  i = vegetation pixels inside the subplot,  N = number of those pixels (for every band λ)', options: { fontSize: 13 } }], { fill: X.ldone, line: X.done, align: 'left', margin: 8 });
box(s, 5.3, 2.95, 7.58, 1.15, [{ text: 'Also saved per subplot', options: { bold: true, fontSize: 14, breakLine: true } }, { text: 'N pixels; standard deviation per band; flower % and canopy cover % (from SAM class counts)', options: { fontSize: 13 } }], { fill: X.lnext, line: X.next, align: 'left', margin: 8 });
box(s, 5.3, 4.3, 7.58, 0.95, [{ text: 'Label', options: { bold: true, fontSize: 14, breakLine: true } }, { text: 'canopy disease severity score recorded for the same subplot', options: { fontSize: 13 } }], { fill: X.lprog, line: X.prog, align: 'left', margin: 8 });
note(s, 'Plot spectrum (if needed) = mean of its 4 subplot spectra; the 4 subplots of a plot always stay in the same validation fold.', 5.75, 0.55, X.done, X.ldone);

// ============ 7 WHY KEEP FLOWERS ============
s = slide('Why flowers are kept in the subplot spectrum');
box(s, 0.45, 1.45, 6.1, 3.3, [{ text: 'Reasons', options: { bold: true, fontSize: 15, color: X.done, breakLine: true } }, { text: '• The severity score is given to the whole canopy, including the inflorescence', options: { breakLine: true } }, { text: '• Systemic white rust deforms inflorescences (staghead), so flowers carry disease information', options: { breakLine: true } }, { text: '• The spectrum then describes the same canopy that was scored', options: { breakLine: true } }, { text: '• No arbitrary pixel removal inside the canopy' }], { fill: X.ldone, line: X.done, align: 'left', valign: 'top', margin: 10, fs: 13.5 });
box(s, 6.78, 1.45, 6.1, 3.3, [{ text: 'Risk and how it is controlled', options: { bold: true, fontSize: 15, color: X.red, breakLine: true } }, { text: '• Yellow petals raise reflectance at 500–650 nm and flowering differs with sowing date and variety (Sulik and Long, 2016)', options: { breakLine: true } }, { text: '• Record flower % per subplot', options: { breakLine: true } }, { text: '• Check selected features against flower % (correlation, partial correlation with severity)', options: { breakLine: true } }, { text: '• Report results by crop stage (vegetative, flowering, pod)' }], { fill: X.lred, line: X.red, align: 'left', valign: 'top', margin: 10, fs: 13.5 });
note(s, 'Flowers are kept for the spectrum; flower % is used only as a check (covariate), not as a disease feature.', 5.05, 0.6, X.prog, X.lprog);

// ============ 8 HOURGLASS VS SMACC ============
s = slide('Hourglass versus SMACC');
s.addTable([['', 'SMACC (per plot)', 'Hourglass (field-wide)'].map(t => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: X.navy } } })),
  ['Endmember source', 'single most extreme pixels', 'mean of clusters of pure pixels'], ['Noise handling', 'none (sensitive to outliers)', 'MNF noise whitening first'], ['Same endmembers in all plots and dates', 'no', 'yes'],
  ['Quality check of bands', 'no', 'MNF eigenvalues and images'], ['Speed', 'fast', 'slower (PPI)'], ['Use here', 'replaced', 'endmember library → SAM classes']],
  { x: 0.45, y: 1.4, w: 12.43, colW: [3.6, 4.4, 4.43], fontSize: 14, border: { type: 'solid', pt: 0.5, color: 'C9CED6' }, rowH: 0.55 });
note(s, 'Optional check: run SMACC once on the whole field; small spectral angles between matching endmembers confirm the library (Gruninger et al., 2004).', 5.6, 0.6, X.envi, X.lenvi);

// ============ 9 OUTPUT ============
s = slide('Output: feature table for feature selection');
const cols = [['ID', 'date, plot, subplot, replication, variety, sowing date', X.next, X.lnext], ['Label', 'canopy severity score of the subplot', X.prog, X.lprog], ['Spectral features', 'R, first and second derivatives, red-edge parameters, 48 indices, White Rust Index (from the subplot spectrum)', X.done, X.ldone], ['Covariates (checks)', 'flower %, canopy cover %, N pixels', X.red, X.lred]];
cols.forEach((c, i) => { const x = 0.45 + i * 3.15; box(s, x, 1.5, 2.9, 2.1, [{ text: c[0], options: { bold: true, fontSize: 14, breakLine: true } }, { text: c[1], options: { fontSize: 12 } }], { fill: c[3], line: c[2] }); });
box(s, 0.45, 3.95, 12.43, 0.75, '1344 rows (7 dates × 48 plots × 4 subplots), one table per sensor; tables joined by ID for fusion', { fill: X.lenvi, line: X.envi, bold: true, fs: 14 });
arrow(s, 6.66, 4.7, 6.66, 5.05, X.navy);
box(s, 0.45, 5.05, 12.43, 0.85, 'Feature selection: Tier 2 scalogram + ReliefF → White Rust Index → ANOVA / Tukey → VIF + stepwise CDA → Boruta → Objective 2 and 3 models', { fill: X.navy, line: X.navy, color: 'FFFFFF', bold: true, fs: 13.5 });

// ============ 10 REFS ============
s = slide('References');
bul(s, ['Boardman, J.W., Kruse, F.A., Green, R.O. (1995). Mapping target signatures via partial unmixing of AVIRIS data. Summaries of the Fifth Annual JPL Airborne Earth Science Workshop, JPL Publication 95-1, Vol. 1, 23–26.',
  'Green, A.A., Berman, M., Switzer, P., Craig, M.D. (1988). A transformation for ordering multispectral data in terms of image quality with implications for noise removal. IEEE Transactions on Geoscience and Remote Sensing 26(1), 65–74.',
  'Gruninger, J., Ratkowski, A.J., Hoke, M.L. (2004). The sequential maximum angle convex cone (SMACC) endmember model. Proceedings of SPIE 5425, 1–14.',
  'Kruse, F.A., Lefkoff, A.B., Boardman, J.W., Heidebrecht, K.B., Shapiro, A.T., Barloon, P.J., Goetz, A.F.H. (1993). The spectral image processing system (SIPS) – interactive visualization and analysis of imaging spectrometer data. Remote Sensing of Environment 44(2–3), 145–163.',
  'Sulik, J.J., Long, D.S. (2016). Spectral considerations for modeling yield of canola. Remote Sensing of Environment 184, 161–174.'], { x: 0.45, y: 1.3, w: 12.43, h: 5.5, fontSize: 13 });
pres.writeFile({ fileName: OUT }).then(async () => { await applyTheme(OUT, THEME); console.log('saved', OUT); });
