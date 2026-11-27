// Flow-chart deck of the UAV data-processing steps already completed (from the lab notebook, 2026).
const pptxgen = require('pptxgenjs');
const path = require('path');
const { applyTheme } = require('/root/.claude/skills/synced/9bf50f97-a337-4b6b-8c8b-ebd229b7e0d3_d565bc3b-4006-4195-b033-a8c25dfdc114/pptx/scripts/apply_theme.js');
const OUT = path.join(__dirname, '../outputs/Resampling_to_HS_grid_vegetation_mask.pptx');
const THEME = { name: 'Processing done', headFontFace: 'Cambria', bodyFontFace: 'Calibri',
  colors: { dk1: '1F2A2A', lt1: 'FFFFFF', dk2: '1F3864', lt2: 'F2F5FA', accent1: '2E7D32', accent2: '2E75B6', accent3: 'C55A11', accent4: '7030A0', accent5: 'C00000', accent6: 'BF9000', hlink: '2E75B6', folHlink: '7030A0' } };
const X = { navy: '1F3864', done: '2E7D32', ldone: 'E8F5E9', prog: 'BF9000', lprog: 'FFF4D6', next: '7F7F7F', lnext: 'F2F2F2', envi: '2E75B6', lenvi: 'DEEBF7', arc: 'C55A11', larc: 'FCE9DC', red: 'C00000', lred: 'F9E0DE', text: '1F2A2A', grey: '595959' };
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.theme = { headFontFace: 'Cambria', bodyFontFace: 'Calibri' };
pres.title = 'Resampling all sensors to the hyperspectral grid and vegetation masking';
const C = pres.SchemeColor;
pres.defineSlideMaster({ title: 'TITLE', background: { color: X.navy }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.8, y: 2.0, w: 11.7, h: 1.7, fontSize: 38, bold: true, color: C.background1, fontFace: 'Cambria', valign: 'bottom' }, text: '' } },
  { placeholder: { options: { name: 'body', type: 'body', x: 0.8, y: 3.9, w: 11.7, h: 1.8, fontSize: 18, color: 'D6E0F0', valign: 'top' }, text: '' } }] });
pres.defineSlideMaster({ title: 'CONTENT', background: { color: 'FFFFFF' }, margin: [0.5, 0.5, 0.6, 0.5],
  slideNumber: { x: 12.4, y: 7.08, w: 0.6, h: 0.3, fontSize: 10, color: X.grey },
  objects: [{ rect: { x: 0, y: 0, w: 13.333, h: 0.08, fill: { color: X.navy } } },
            { placeholder: { options: { name: 'title', type: 'title', x: 0.45, y: 0.22, w: 12.4, h: 0.75, fontSize: 28, bold: true, color: C.text2, fontFace: 'Cambria', valign: 'middle' }, text: '' } },
            { line: { x: 0.45, y: 1.0, w: 12.43, h: 0, line: { color: X.done, width: 1.5 } } },
            { text: { text: 'Co-registration, resampling and vegetation mask  |  Animesh Panda (13098)  |  Agricultural Physics, ICAR-IARI', options: { x: 0.45, y: 7.08, w: 9.5, h: 0.3, fontSize: 10, color: X.grey } } }] });
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



const refl = (s, t, y = 6.62) => txt(s, 'References: ' + t, { x: 0.45, y, w: 12.43, h: 0.38, fontSize: 10.5, italic: true, color: X.grey, margin: 0 });
const tbl = (s, rows, o) => s.addTable([rows[0].map(t => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: o.head || X.navy } } }))].concat(rows.slice(1)), Object.assign({ fontSize: 12, border: { type: 'solid', pt: 0.5, color: 'C9CED6' }, valign: 'middle', margin: 0.05 }, o));

// ============ 1 TITLE ============
let s = pres.addSlide({ masterName: 'TITLE' });
s.addText('Resampling all images to the hyperspectral grid and masking soil, grass and shadow', { placeholder: 'title' });
s.addText('RGB, multispectral and thermal images co-registered and resampled to the 2.2 cm hyperspectral grid; one vegetation mask from the hyperspectral image applied to every sensor so that only vegetation pixels remain\n\nAnimesh Panda (13098), Ph.D. Agricultural Physics, ICAR-IARI', { placeholder: 'body' });

// ============ 2 WHY ============
s = slide('Purpose and principle');
box(s, 0.45, 1.35, 6.1, 2.2, [{ text: 'Purpose', options: { bold: true, fontSize: 15, color: X.done, breakLine: true } }, { text: 'All four sensors must describe exactly the same vegetation pixels of every subplot, so that their features can be compared and fused at pixel and subplot level.', options: { fontSize: 13.5 } }], { fill: X.ldone, line: X.done, align: 'left', margin: 10 });
box(s, 6.78, 1.35, 6.1, 2.2, [{ text: 'Principle', options: { bold: true, fontSize: 15, color: X.envi, breakLine: true } }, { text: 'One common grid (the hyperspectral image) + one common mask (made from the hyperspectral image, which separates soil, grass, shadow and mustard best) = identical pixels in every sensor.', options: { fontSize: 13.5 } }], { fill: X.lenvi, line: X.envi, align: 'left', margin: 10 });
bul(s, ['Small misregistration between images causes large errors when images are compared pixel by pixel (Dai and Khorram, 1998)', 'Multi-sensor fusion studies align all sensor layers before extracting features (Maimaitijiang et al., 2020; Feng et al., 2022)', 'Soil, weeds and shadow in a plot change reflectance and canopy temperature and must be removed before disease features are extracted (Jones et al., 2009; Guo et al., 2021)'], { x: 0.45, y: 3.85, w: 12.43, h: 2.3, fontSize: 14 });
refl(s, 'Dai and Khorram, 1998; Maimaitijiang et al., 2020; Feng et al., 2022; Jones et al., 2009; Guo et al., 2021.');

// ============ 3 INPUTS ============
s = slide('Input images and the reference grid');
tbl(s, [['Sensor (per date)', 'Layers', 'Nominal pixel at 30 m', 'To the 2.2 cm HS grid'], ['Hyperspectral (Headwall Co-Aligned)', '483 bands, 399–2398 nm', '2.2 cm (image header)', 'reference grid (no resampling)'],
  ['RGB (DJI Phantom)', 'R, G, B', '≈ 0.8 cm', 'finer → aggregate (mean)'], ['Multispectral (MicaSense RedEdge-MX)', '475, 560, 668, 717, 840 nm', '≈ 2 cm', 'similar → bilinear (or nearest)'],
  ['Thermal (FLIR Vue Pro R, 13 mm)', 'canopy temperature', '≈ 3.9 cm', 'coarser → nearest neighbour'], ['Headwall Nano (if used)', 'VNIR bands', 'lens-dependent', 'by its pixel size, as above']], { x: 0.45, y: 1.35, w: 12.43, colW: [3.6, 2.9, 2.6, 3.33], rowH: 0.55 });
note(s, 'Check the actual pixel size of each orthomosaic in its metadata before resampling; the nominal values follow from sensor pixel pitch × flight height ÷ focal length.', 4.95, 0.6, X.prog, X.lprog);
note(s, '7 dates × 4 sensors = 28 images; every date is processed separately on that date\'s hyperspectral grid.', 5.75, 0.5, X.envi, X.lenvi);

// ============ 4 OVERVIEW ============
s = slide('Workflow overview');
const wf = [['Projection and units', 'all images to WGS 84 / UTM 43N; reflectance, °C (Smith and Milton, 1999)', X.arc, X.larc], ['Reference grid', 'HS cube defines pixel size, origin and extent (Richards, 2013)', X.envi, X.lenvi], ['Co-registration', 'GCPs + tie points; polynomial warp; RMSE < 1 pixel (Zitová and Flusser, 2003)', X.arc, X.larc], ['Resampling', 'RGB aggregate; MS bilinear; thermal nearest neighbour (Richards, 2013)', X.envi, X.lenvi],
  ['Layer stack', 'HS + MS + RGB + thermal on one grid (Feng et al., 2022)', X.navy, X.lnext], ['Vegetation mask (HS)', 'hourglass + SAM; keep canopy and flowers; remove soil, grass, shadow (Kruse et al., 1993)', X.done, X.ldone], ['Apply mask', 'same mask to every layer → only vegetation pixels (Jones et al., 2009)', X.done, X.ldone], ['Checks and output', 'registration RMSE, mask accuracy; subplot tables (Congalton, 1991)', X.prog, X.lprog]];
wf.forEach((w, i) => { const row = Math.floor(i / 4), c = i % 4, col = row === 0 ? c : 3 - c; const x = 0.55 + col * 3.15, y = 1.45 + row * 2.45;
  box(s, x, y, 2.75, 1.85, [{ text: (i + 1) + '. ' + w[0], options: { bold: true, fontSize: 14, breakLine: true } }, { text: w[1], options: { fontSize: 11.5 } }], { fill: w[3], line: w[2], lw: 1.75 });
  if (i < 7) { if (i === 3) arrow(s, x + 1.37, y + 1.85, x + 1.37, y + 2.45, X.grey); else if (row === 0) arrow(s, x + 2.75, y + 0.92, x + 3.15, y + 0.92, X.grey); else arrow(s, x, y + 0.92, x - 0.4, y + 0.92, X.grey); } });

// ============ 5 STEP 1 ============
s = slide('Step 1: projection and radiometric units');
chain(s, ['Read each orthomosaic and its metadata (pixel size, coordinate system)', 'Project to WGS 84 / UTM zone 43N (EPSG:32643), distances in metres (Richards, 2013)', 'HS: reflectance (check scale 0–1 or 0–10 000)', 'MS: reflectance from the calibration panel and sunlight sensor (Smith and Milton, 1999)', 'RGB: digital numbers; thermal: °C after emissivity correction (Jones et al., 2009)'], X.arc, X.larc, { y: 1.4, h: 0.72, gap: 0.2, w: 7.2 });
box(s, 8.0, 1.4, 4.88, 2.55, [{ text: 'Why first', options: { bold: true, fontSize: 14, breakLine: true } }, { text: 'The HS cube is in geographic degrees (pixel 2.3 × 10⁻⁷°). Erosion, subplot splitting and pixel size must be in metres, so every image is put in the same metric projection before alignment.', options: { fontSize: 12.5 } }], { fill: X.lnext, line: X.next, align: 'left', margin: 8 });
box(s, 8.0, 4.15, 4.88, 1.7, [{ text: 'Thermal', options: { bold: true, fontSize: 14, breakLine: true } }, { text: 'Emissivity 0.98 and air temperature/humidity of the flight are used to convert to canopy temperature (Jones et al., 2009).', options: { fontSize: 12.5 } }], { fill: X.lred, line: X.red, align: 'left', margin: 8 });
refl(s, 'Smith and Milton, 1999; Jones et al., 2009; Richards, 2013.');

// ============ 6 STEP 2 ============
s = slide('Step 2: the hyperspectral image as the reference (master) grid');
{ const gx = 0.7, gy = 1.6, n = 6, c = 0.55;
  for (let i = 0; i <= n; i++) { s.addShape(pres.shapes.LINE, { x: gx + i * c, y: gy, w: 0.001, h: n * c, line: { color: X.envi, width: 1 } }); s.addShape(pres.shapes.LINE, { x: gx, y: gy + i * c, w: n * c, h: 0.001, line: { color: X.envi, width: 1 } }); }
  s.addShape(pres.shapes.OVAL, { x: gx - 0.08, y: gy - 0.08, w: 0.16, h: 0.16, fill: { color: X.red }, line: { color: X.red } });
  txt(s, 'origin (upper-left corner)', { x: gx + 0.1, y: gy - 0.4, w: 2.5, h: 0.3, fontSize: 11, color: X.red, margin: 0 });
  txt(s, '2.2 cm', { x: gx, y: gy + n * c + 0.05, w: c, h: 0.25, fontSize: 10, align: 'center', margin: 0 });
  txt(s, 'HS grid: every other image is placed exactly on these cells', { x: gx - 0.2, y: gy + n * c + 0.35, w: 3.8, h: 0.5, fontSize: 11, italic: true, color: X.grey, align: 'center' }); }
tbl(s, [['Grid property', 'Taken from the HS cube'], ['Pixel size', '≈ 0.022 m (after projection to UTM 43N)'], ['Origin', 'upper-left corner of the HS cube'], ['Extent', '2355 × 2142 pixels (field + margin)'], ['Coordinate system', 'WGS 84 / UTM zone 43N']], { x: 5.0, y: 1.5, w: 7.88, colW: [2.6, 5.28], rowH: 0.5, head: X.envi });
bul(s, ['Called a "snap raster" (ArcGIS) or target-aligned pixels (GDAL); ENVI layer stacking can inherit this grid (Richards, 2013)', 'Same grid for all sensors of one date → pixel (row, column) is the same ground point in every layer'], { x: 5.0, y: 4.25, w: 7.88, h: 1.6, fontSize: 13.5 });
refl(s, 'Richards, 2013.');

// ============ 7 STEP 3 ============
s = slide('Step 3: co-registration to the hyperspectral image');
chain(s, ['Ground control points (RTK GNSS) used in all orthomosaics (Guo et al., 2021)', 'Tie points between each image and the HS image: plot corners, markers (Zitová and Flusser, 2003)', 'Fit a first-order (affine) or second-order polynomial transformation (Richards, 2013)', 'Root-mean-square error of independent check points (Zitová and Flusser, 2003)', 'Accept if RMSE < 1 HS pixel (< 2.2 cm); else add points and refit (Dai and Khorram, 1998)'], X.arc, X.larc, { y: 1.4, h: 0.72, gap: 0.2, w: 6.6 });
box(s, 7.4, 1.4, 5.48, 1.55, [{ text: 'Matching bands', options: { bold: true, fontSize: 13.5, breakLine: true } }, { text: 'RGB and MS green/red/NIR bands are matched with the HS bands nearest 560, 668 and 840 nm, which look most alike', options: { fontSize: 12 } }], { fill: X.lenvi, line: X.envi, align: 'left', margin: 8 });
box(s, 7.4, 3.15, 5.48, 1.55, [{ text: 'Thermal', options: { bold: true, fontSize: 13.5, breakLine: true } }, { text: 'Few common details with reflectance images → use targets visible in both (e.g. aluminium or heated markers) and plot edges', options: { fontSize: 12 } }], { fill: X.lred, line: X.red, align: 'left', margin: 8 });
box(s, 7.4, 4.9, 5.48, 1.0, [{ text: 'Why < 1 pixel', options: { bold: true, fontSize: 13.5, breakLine: true } }, { text: 'misregistration mixes canopy and soil values at the edges (Dai and Khorram, 1998)', options: { fontSize: 12 } }], { fill: X.lnext, line: X.next, align: 'left', margin: 8 });
refl(s, 'Zitová and Flusser, 2003; Dai and Khorram, 1998; Richards, 2013.');

// ============ 8 STEP 4 ============
s = slide('Step 4: resampling each sensor to the 2.2 cm grid');
tbl(s, [['Sensor', 'Native vs HS pixel', 'Method', 'Reason'], ['RGB', '≈ 0.8 cm → 2.2 cm (coarser)', 'Pixel aggregate (area mean) (Richards, 2013)', 'each new pixel = mean of the ≈ 7 RGB pixels it covers; avoids aliasing'],
  ['Multispectral', '≈ 2 cm → 2.2 cm (similar)', 'Bilinear or nearest neighbour (Richards, 2013)', 'smooth, small change in pixel size'], ['Thermal', '≈ 3.9 cm → 2.2 cm (finer)', 'Nearest neighbour (Guo et al., 2021)', 'keeps the original temperatures; no new values are invented'],
  ['Vegetation mask (if moved)', 'class image', 'Nearest neighbour (Richards, 2013)', 'class values must stay 0 or 1']], { x: 0.45, y: 1.35, w: 12.43, colW: [2.2, 3.0, 3.1, 4.13], rowH: 0.6, head: X.envi });
const rs = [['Nearest neighbour', 'value of the closest original pixel (Richards, 2013)'], ['Bilinear', 'distance-weighted mean of the 4 nearest pixels (Richards, 2013)'], ['Cubic convolution', '16 nearest pixels; sharper but can overshoot (Richards, 2013)'], ['Aggregate (mean)', 'mean of all original pixels inside the new pixel (Richards, 2013)']];
rs.forEach((r, i) => box(s, 0.45 + i * 3.15, 4.55, 2.9, 1.25, step(r[0], r[1]), { fill: X.lnext, line: X.next }));
refl(s, 'Richards, 2013; Guo et al., 2021.', 6.0);

// ============ 9 STEP 5 ============
s = slide('Step 5: multi-sensor layer stack on the hyperspectral grid');
[['HS', '483 bands', X.envi], ['MS', '5 bands', X.done], ['RGB', '3 bands', X.prog], ['Thermal', '1 band (°C)', X.red]].forEach((l, i) => { box(s, 0.45, 1.45 + i * 1.05, 2.8, 0.85, step(l[0], l[1]), { fill: 'FFFFFF', line: l[2], lw: 2 }); arrow(s, 3.25, 1.87 + i * 1.05, 4.2, 3.0, l[2]); });
box(s, 4.2, 2.3, 4.0, 1.4, step('Layer stack (one date)', '492 layers on the same 2.2 cm grid (Maimaitijiang et al., 2020; Feng et al., 2022)'), { fill: X.navy, line: X.navy, color: 'FFFFFF' });
arrow(s, 8.2, 3.0, 8.75, 3.0, X.navy);
box(s, 8.75, 1.45, 4.13, 3.1, [{ text: 'Advantages', options: { bold: true, fontSize: 14, breakLine: true } }, { text: '• one file per date; pixel (row, column) identical in all layers\n• one mask and one set of subplot polygons for all sensors\n• pixel-level fusion becomes possible', options: { fontSize: 12.5 } }], { fill: X.lnext, line: X.next, align: 'left', margin: 8 });
note(s, 'Large file (HS ≈ 9.75 GB per date): the stack can also be kept as separate co-registered files that share the same grid.', 5.85, 0.6, X.prog, X.lprog);
refl(s, 'Maimaitijiang et al., 2020; Feng et al., 2022.');

// ============ 10 STEP 6 ============
s = slide('Step 6: vegetation mask from the hyperspectral image');
chain(s, ['Hourglass endmembers: MNF → PPI → n-D (Green et al., 1988; Boardman et al., 1995)', 'Training ROIs: mustard canopy, flower, soil, grass/weeds, shadow (Guo et al., 2021)', 'SAM classification of every pixel, angle calibrated (Kruse et al., 1993)', 'Mask = 1 for canopy, stressed canopy, flower; 0 for soil, grass, shadow (Sulik and Long, 2016)', 'NDVI > 0.6 OR flower class; flowers have low NDVI (Rouse et al., 1974)', '1-pixel morphological erosion removes mixed edge pixels (Soille, 2003)'], X.done, X.ldone, { y: 1.35, h: 0.66, gap: 0.16, w: 6.8 });
box(s, 7.55, 1.35, 5.33, 2.0, [{ text: 'Grass and weeds', options: { bold: true, fontSize: 13.5, breakLine: true } }, { text: 'Bunds and channels are removed by the plot and subplot polygons. Weeds inside a plot are separated by their own SAM endmember; check them visually in RGB, because green weeds are spectrally close to mustard.', options: { fontSize: 12 } }], { fill: X.lred, line: X.red, align: 'left', margin: 8 });
box(s, 7.55, 3.55, 5.33, 1.55, [{ text: 'Why from hyperspectral', options: { bold: true, fontSize: 13.5, breakLine: true } }, { text: '483 bands separate soil, shadow, grass, green leaf and yellow flower far better than 3 or 5 broad bands', options: { fontSize: 12 } }], { fill: X.lenvi, line: X.envi, align: 'left', margin: 8 });
refl(s, 'Green et al., 1988; Boardman et al., 1995; Kruse et al., 1993; Rouse et al., 1974; Sulik and Long, 2016; Soille, 2003.');

// ============ 11 STEP 7 ============
s = slide('Step 7: apply the mask to every sensor and extract subplot values');
box(s, 0.45, 1.45, 3.4, 1.4, step('Mask (HS grid)', '1 = vegetation, 0 = soil / grass / shadow'), { fill: X.ldone, line: X.done, lw: 2 });
box(s, 0.45, 3.2, 3.4, 1.4, step('Resampled layers', 'HS, MS, RGB, thermal on the same grid'), { fill: X.lenvi, line: X.envi });
box(s, 4.35, 2.3, 2.8, 1.4, step('Multiply', 'layer × mask; 0 → NoData'), { fill: X.navy, line: X.navy, color: 'FFFFFF' });
arrow(s, 3.85, 2.15, 4.35, 2.8, X.done); arrow(s, 3.85, 3.9, 4.35, 3.2, X.envi);
box(s, 7.65, 2.3, 2.5, 1.4, step('Subplot polygons', '4 per plot × 48 plots'), { fill: X.larc, line: X.arc });
box(s, 10.55, 2.3, 2.33, 1.4, step('Zonal mean', 'per subplot, band and sensor (Feng et al., 2022)'), { fill: X.lprog, line: X.prog });
arrow(s, 7.15, 3.0, 7.65, 3.0, X.navy); arrow(s, 10.15, 3.0, 10.55, 3.0, X.arc);
bul(s, ['All sensors use exactly the same vegetation pixels of each subplot', 'Thermal: coarser native pixels at canopy edges can still contain warm soil → use an extra 1-pixel erosion or the median temperature (Jones et al., 2009)', 'Also saved: number of vegetation pixels, flower %, canopy cover % per subplot'], { x: 0.45, y: 4.9, w: 12.43, h: 1.6, fontSize: 13.5 });
refl(s, 'Jones et al., 2009; Feng et al., 2022.');

// ============ 12 STEP 8 ============
s = slide('Step 8: quality checks');
const qc = [['Registration', 'RMSE of check points < 1 HS pixel; swipe or flicker the RGB and thermal layers over the HS image'], ['Mask accuracy', 'independent reference pixels (canopy, flower, soil, grass, shadow) from RGB → confusion matrix, overall accuracy, kappa (Congalton, 1991)'],
  ['Visual check', 'masked RGB of random subplots: no soil, weeds or shadow left; flowers retained'], ['Thermal check', 'canopy temperature of masked pixels lower than soil and stable when erosion is increased by 1 pixel'], ['Per-subplot counts', 'flag subplots with very few vegetation pixels']];
qc.forEach((q, i) => box(s, 0.45, 1.4 + i * 0.95, 12.43, 0.8, [{ text: q[0] + ': ', options: { bold: true, color: X.done } }, { text: q[1] }], { fill: X.ldone, line: X.done, align: 'left', fs: 13, margin: 8 }));
refl(s, 'Congalton, 1991; Dai and Khorram, 1998; Jones et al., 2009.', 6.3);

// ============ 13 SOFTWARE ============
s = slide('Implementation in software');
tbl(s, [['Step', 'ENVI', 'ArcGIS', 'Python (GDAL / rasterio)'], ['Projection', 'Reproject Raster', 'Project Raster', 'gdalwarp -t_srs EPSG:32643'], ['Co-registration', 'Image Registration (image to image)', 'Georeferencing toolbar', 'rasterio + control points (affine fit)'],
  ['Resampling to HS grid', 'Resize Data / Layer Stacking (inherit grid)', 'Resample with snap raster and cell size', 'gdalwarp -tr 0.022 0.022 -tap -r average | bilinear | near'], ['Layer stack', 'Layer Stacking', 'Composite Bands', 'rasterio stack'],
  ['Vegetation mask', 'SAM classification; Band Math; Morphology (erode)', 'Reclassify; Raster Calculator', 'numpy; scipy.ndimage.binary_erosion'], ['Subplot means', 'ROI statistics', 'Zonal Statistics as Table', 'rasterstats / numpy']], { x: 0.45, y: 1.35, w: 12.43, colW: [2.1, 3.4, 3.2, 3.73], fontSize: 11.5, rowH: 0.58 });
note(s, 'Use the same settings for all 7 dates and record them (pixel size, method, RMSE) in a processing log.', 5.6, 0.55, X.envi, X.lenvi);

// ============ 14 OUTPUT ============
s = slide('Outputs and points to note');
box(s, 0.45, 1.35, 6.1, 3.0, [{ text: 'Outputs (per date)', options: { bold: true, fontSize: 15, color: X.done, breakLine: true } }, { text: '• co-registered HS, MS, RGB and thermal layers on one 2.2 cm grid\n• vegetation mask (canopy + flower)\n• masked layers (soil, grass, shadow = NoData)\n• subplot table per sensor: 192 subplots per date, 1344 for 7 dates', options: { fontSize: 13 } }], { fill: X.ldone, line: X.done, align: 'left', valign: 'top', margin: 10 });
box(s, 6.78, 1.35, 6.1, 3.0, [{ text: 'Points to note', options: { bold: true, fontSize: 15, color: X.red, breakLine: true } }, { text: '• resampling RGB to 2.2 cm loses fine texture → compute RGB GLCM texture (Haralick et al., 1973) before resampling, inside the same mask\n• thermal is up-sampled: no new detail is created\n• alternative: move the mask to each sensor\'s native grid instead of moving the data', options: { fontSize: 13 } }], { fill: X.lred, line: X.red, align: 'left', valign: 'top', margin: 10 });
note(s, 'Result: every sensor is measured on the same mustard canopy (leaves and flowers) of every subplot, ready for feature extraction and fusion.', 4.65, 0.6, X.done, X.ldone);

// ============ 15 REFS ============
s = slide('References');
const R = ['Boardman, J.W., Kruse, F.A., Green, R.O. (1995). Mapping target signatures via partial unmixing of AVIRIS data. Summaries of the Fifth Annual JPL Airborne Earth Science Workshop, JPL Publication 95-1, Vol. 1, 23–26.',
  'Congalton, R.G. (1991). A review of assessing the accuracy of classifications of remotely sensed data. Remote Sensing of Environment 37(1), 35–46.',
  'Dai, X., Khorram, S. (1998). The effects of image misregistration on the accuracy of remotely sensed change detection. IEEE Transactions on Geoscience and Remote Sensing 36(5), 1566–1577.',
  'Feng, Z., Song, L., Duan, J., He, L., Zhang, Y., Wei, Y., Feng, W. (2022). Monitoring wheat powdery mildew based on hyperspectral, thermal infrared, and RGB image data fusion. Sensors 22(1), 31.',
  'Green, A.A., Berman, M., Switzer, P., Craig, M.D. (1988). A transformation for ordering multispectral data in terms of image quality with implications for noise removal. IEEE Transactions on Geoscience and Remote Sensing 26(1), 65–74.',
  'Guo, A., Huang, W., Dong, Y., Ye, H., Ma, H., Liu, B., Wu, W., Ren, Y., Ruan, C., Geng, Y. (2021). Wheat yellow rust detection using UAV-based hyperspectral technology. Remote Sensing 13(1), 123.',
  'Jones, H.G., Serraj, R., Loveys, B.R., Xiong, L., Wheaton, A., Price, A.H. (2009). Thermal infrared imaging of crop canopies for the remote diagnosis and quantification of plant responses to water stress in the field. Functional Plant Biology 36(11), 978–989.',
  'Kruse, F.A., Lefkoff, A.B., Boardman, J.W., Heidebrecht, K.B., Shapiro, A.T., Barloon, P.J., Goetz, A.F.H. (1993). The spectral image processing system (SIPS) – interactive visualization and analysis of imaging spectrometer data. Remote Sensing of Environment 44(2–3), 145–163.',
  'Maimaitijiang, M., Sagan, V., Sidike, P., Hartling, S., Esposito, F., Fritschi, F.B. (2020). Soybean yield prediction from UAV using multimodal data fusion and deep learning. Remote Sensing of Environment 237, 111599.',
  'Haralick, R.M., Shanmugam, K., Dinstein, I. (1973). Textural features for image classification. IEEE Transactions on Systems, Man, and Cybernetics SMC-3(6), 610–621.',
  'Richards, J.A. (2013). Remote Sensing Digital Image Analysis: An Introduction, 5th edn. Springer, Berlin.',
  'Rouse, J.W., Haas, R.H., Schell, J.A., Deering, D.W. (1974). Monitoring vegetation systems in the Great Plains with ERTS. Third ERTS Symposium, NASA SP-351, 309–317.',
  'Smith, G.M., Milton, E.J. (1999). The use of the empirical line method to calibrate remotely sensed data to reflectance. International Journal of Remote Sensing 20(13), 2653–2662.',
  'Soille, P. (2003). Morphological Image Analysis: Principles and Applications, 2nd edn. Springer, Berlin.',
  'Sulik, J.J., Long, D.S. (2016). Spectral considerations for modeling yield of canola. Remote Sensing of Environment 184, 161–174.',
  'Zitová, B., Flusser, J. (2003). Image registration methods: a survey. Image and Vision Computing 21(11), 977–1000.'];
R.sort((a, b) => a.localeCompare(b));
[R.slice(0, 8), R.slice(8)].forEach((col, c) => s.addText(col.map((r, k) => ({ text: r, options: { breakLine: k < col.length - 1 } })), { isTextBox: true, x: 0.45 + c * 6.25, y: 1.2, w: 6.1, h: 5.7, fontSize: 10.5, color: X.text, valign: 'top', paraSpaceAfter: 4 }));
pres.writeFile({ fileName: OUT }).then(async () => { await applyTheme(OUT, THEME); console.log('saved', OUT); });
