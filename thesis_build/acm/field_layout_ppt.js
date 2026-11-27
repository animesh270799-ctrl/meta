// Field layout 2026-27 with a 10 m buffer and 5 m × 3 m plots; variety and sowing-date key.
// Rebuilt from the user's original layout (layout.json 'buffer'); writes the new geometry to layout.json 'buffer10'.
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');
const LJ = path.join(__dirname, 'layout.json'); const LAY = JSON.parse(fs.readFileSync(LJ));
const OUT = path.join(__dirname, '../outputs/Field_layout_2026-27_10m_buffer.pptx');
// ---- editable experiment facts ----
const VAR = { V1: 'PM 26', V2: 'Pusa Vijay', V3: 'PM 37' };
const DOS = { D1: '20 Nov 2026', D2: '30 Nov 2026', D3: '10 Dec 2026', D4: '20 Dec 2026' };
const PW = 3, PL = 5, BUF = 10, TOT = 48;              // plot width (along field length), plot length, buffer, field length (m)
const BUND = Math.round((TOT - BUF - 12 * PW) / 10 * 100) / 100;   // 10 bunds share the remaining length → 0.2 m
const HB = 3 * PW + 2 * BUND, IB = 9 * PW + 8 * BUND;   // 9.4 m and 28.6 m
const X0 = 2.1, X1 = 13.0, s = (X1 - X0) / TOT;       // inches per metre along the field
const G = '1E4D2B', BL = '2E6DA4', LBL = 'DCE9F5';
const fmt = (v) => (Math.round(v * 10) / 10).toString();

// ---- build the new shape list in the same schema as layout.json ----
const S = [];
const add = (o) => S.push(Object.assign({ t: '', fill: null, line: null, col: null, sz: null, b: null, geom: 'rect' }, o));
const old = LAY.buffer;
const plots = old.filter(o => /^D\dV\d/.test(o.t));
plots.forEach(o => {
  const healthy = o.x < 3.8; const k = Math.round((o.x - (healthy ? 2.1 : 7.97)) / 0.567);
  const x = healthy ? X0 + k * (PW + BUND) * s : X0 + (HB + BUF) * s + k * (PW + BUND) * s;
  add({ t: o.t, x, y: o.y, w: PW * s, h: o.h, fill: o.fill, line: o.line, col: o.col, sz: 11, b: true, healthy, k });
});
[2.76, 4.58].forEach(y => { add({ x: X0, y, w: HB * s, h: 0.26, fill: LBL }); add({ t: 'CHANNEL', x: X0, y, w: HB * s, h: 0.26, col: BL, sz: 10, b: true });
  add({ x: X0 + (HB + BUF) * s, y, w: IB * s, h: 0.26, fill: LBL }); add({ t: 'C H A N N E L', x: X0 + (HB + BUF) * s, y, w: IB * s, h: 0.26, col: BL, sz: 10.5, b: true }); });
add({ x: X0 + HB * s, y: 2.0, w: BUF * s, h: 3.6, fill: 'EEF3EA', line: '9E9E9E', dash: true });
add({ t: BUF + ' m BUFFER ZONE\nNo mustard or other crucifer.\nKeep fallow or sow a non-host crop; remove cruciferous weeds.', x: X0 + HB * s + 0.06, y: 2.75, w: BUF * s - 0.12, h: 2.0, col: '1F1F1F', sz: 11, buffer: true });
add({ t: 'HEALTHY', x: X0, y: 5.72, w: HB * s, h: 0.36, fill: BL, col: 'FFFFFF', sz: 14, b: true, geom: 'roundRect' });
['R3', 'R2', 'R1'].forEach((r, i) => add({ t: r, x: X0 + (HB + BUF) * s + i * 3 * (PW + BUND) * s, y: 5.72, w: (3 * PW + 2 * BUND) * s, h: 0.36, fill: BL, col: 'FFFFFF', sz: 14, b: true, geom: 'roundRect' }));
add({ t: 'Uninoculated control', x: X0, y: 6.12, w: HB * s, h: 0.3, col: '555555', sz: 12 });
add({ t: 'Inoculated (1.5 × 10⁵ zoosporangia mL⁻¹)', x: X0 + (HB + BUF) * s, y: 6.12, w: IB * s, h: 0.3, col: '555555', sz: 12 });
add({ x: X0 + (HB + BUF / 2) * s - 0.2, y: 5.72, w: 0.4, h: 0.42, fill: BL, geom: 'upArrow' });
add({ t: 'Facing field', x: X0 + (HB + BUF / 2) * s - 0.7, y: 6.14, w: 1.4, h: 0.28, col: '555555', sz: 12, italic: true });
[[0, HB, fmt(HB) + ' m'], [HB, HB + BUF, BUF + ' m buffer'], [HB + BUF, TOT, fmt(IB) + ' m']].forEach(d => {
  add({ x: X0 + d[0] * s + 0.02, y: 1.72, w: (d[1] - d[0]) * s - 0.04, h: 0, line: '555555', geom: 'line', arrows: true });
  add({ t: d[2], x: X0 + d[0] * s, y: 1.42, w: (d[1] - d[0]) * s, h: 0.26, col: G, sz: 13, b: true }); });
add({ t: 'Total ' + TOT + ' m × 24 m', x: X0, y: 1.12, w: X1 - X0, h: 0.28, col: '1F1F1F', sz: 14, b: true });
add({ x: 1.85, y: 2.0, w: 0, h: 3.6, line: '555555', geom: 'line', arrows: true });
add({ t: '24 m', x: 1.2, y: 2.3, w: 0.6, h: 0.3, col: G, sz: 13, b: true });
add({ t: 'Amrit\nSarovar', x: 0.35, y: 3.2, w: 1.05, h: 1.2, fill: BL, col: 'FFFFFF', sz: 14, b: true, geom: 'roundRect' });
LAY.buffer10 = S; fs.writeFileSync(LJ, JSON.stringify(LAY, null, 0));

// ---- render ----
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.title = 'Field layout 2026-27 (10 m buffer)';
const draw = (sl, o) => {
  if (o.geom === 'line') { sl.addShape(pres.shapes.LINE, { x: o.x, y: o.y, w: o.w || 0.001, h: o.h || 0.001, line: { color: o.line, width: 1.25, beginArrowType: o.arrows ? 'triangle' : undefined, endArrowType: o.arrows ? 'triangle' : undefined } }); return; }
  if (o.geom === 'upArrow') { sl.addShape(pres.shapes.UP_ARROW, { x: o.x, y: o.y, w: o.w, h: o.h, fill: { color: o.fill }, line: { color: o.fill } }); return; }
  if (o.fill || o.line) sl.addShape(o.geom === 'roundRect' ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, { x: o.x, y: o.y, w: o.w, h: o.h, rectRadius: 0.06,
    fill: o.fill ? { color: o.fill } : { type: 'none' }, line: o.line ? { color: o.line, width: 0.75, dashType: o.dash ? 'dash' : 'solid' } : { type: 'none' } });
  if (!o.t) return;
  if (o.buffer) { const [h1, ...rest] = o.t.split('\n'); sl.addText([{ text: h1, options: { bold: true, color: G, fontSize: 14, breakLine: true } }, { text: rest.join(' '), options: { fontSize: o.sz } }],
    { isTextBox: true, x: o.x, y: o.y, w: o.w, h: o.h, align: 'center', valign: 'middle', color: o.col, margin: 2, fontFace: 'Calibri' }); return; }
  sl.addText(o.t, { isTextBox: true, x: o.x, y: o.y, w: o.w, h: o.h, fontSize: o.sz || 12, bold: !!o.b, italic: !!o.italic, color: o.col || '1F1F1F', align: 'center', valign: 'middle', margin: 0, fontFace: 'Calibri' });
};
let sl = pres.addSlide(); sl.background = { color: 'FFFFFF' };
sl.addText('Field layout with ' + BUF + ' m buffer', { x: 0.6, y: 0.3, w: 9.5, h: 0.75, fontSize: 32, bold: true, color: G, fontFace: 'Cambria', margin: 0 });
sl.addImage({ path: path.join(__dirname, 'img', 'compass.png'), x: 11.75, y: 0.2, w: 1.15, h: 1.15, rotate: 180 });
S.forEach(o => draw(sl, o));
// variety and sowing-date key
const key = (x, w, title, items, col) => { sl.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 6.48, w, h: 0.42, fill: { color: 'F2F5FA' }, line: { color: col, width: 1 }, rectRadius: 0.06 });
  sl.addText([{ text: title + '  ', options: { bold: true, color: col } }].concat(items.map((t, i) => ({ text: (i ? '   |   ' : '') + t }))), { isTextBox: true, x: x + 0.1, y: 6.48, w: w - 0.2, h: 0.42, fontSize: 12.5, valign: 'middle', margin: 0, color: '1F1F1F', fontFace: 'Calibri' }); };
key(0.6, 5.4, 'Variety (V):', Object.entries(VAR).map(([k, v]) => k + ' = ' + v), BL);
key(6.15, 6.85, 'Date of sowing (D), 2026:', Object.entries(DOS).map(([k, v]) => k + ' = ' + v.replace(' 2026', '')), G);
sl.addText([{ text: 'Plot ' + PL + ' m × ' + PW + ' m, ' + BUND + ' m bunds between plots, 2 m channels. ', options: {} }, { text: 'Field ' + TOT + ' m × 24 m (' + fmt(HB) + ' m healthy block + ' + BUF + ' m buffer + ' + fmt(IB) + ' m inoculated block).', options: { bold: true } }],
  { isTextBox: true, x: 0.6, y: 6.97, w: 12.1, h: 0.3, fontSize: 12.5, color: '1F1F1F', margin: 0, fontFace: 'Calibri' });
sl.addText('Plot code: D = date of sowing, V = variety; number in brackets = plot ID.  White rust of mustard | ICAR-IARI New Delhi, rabi 2026-27', { isTextBox: true, x: 0.6, y: 7.22, w: 12.1, h: 0.22, fontSize: 9.5, color: '777777', margin: 0 });

// ---- slide 2: treatment key ----
sl = pres.addSlide(); sl.background = { color: 'FFFFFF' };
sl.addText('Treatments, varieties, sowing dates and plot numbers', { x: 0.6, y: 0.3, w: 12.1, h: 0.7, fontSize: 28, bold: true, color: G, fontFace: 'Cambria', margin: 0 });
const rep = (o) => o.healthy ? 'H' : ['R3', 'R2', 'R1'][Math.floor(o.k / 3)];
const rows = [];
['D1', 'D2', 'D3', 'D4'].forEach(d => ['V1', 'V2', 'V3'].forEach(v => {
  const ps = S.filter(o => o.t.startsWith(d + v)); const id = (r) => (ps.find(o => rep(o) === r) || { t: '\n(–)' }).t.split('\n')[1].replace(/[()]/g, '');
  rows.push([d + v, DOS[d], VAR[v], id('R1'), id('R2'), id('R3'), id('H')]); }));
const H = (t) => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: BL } } });
sl.addTable([['Code', 'Date of sowing', 'Variety', 'R1 plot', 'R2 plot', 'R3 plot', 'Healthy plot'].map(H)].concat(rows),
  { x: 0.6, y: 1.2, w: 8.0, colW: [0.9, 1.6, 1.5, 1.0, 1.0, 1.0, 1.0], fontSize: 12.5, fontFace: 'Calibri', border: { type: 'solid', pt: 0.5, color: 'C9CED6' }, rowH: 0.4, align: 'center', valign: 'middle' });
sl.addShape(pres.shapes.RECTANGLE, { x: 8.95, y: 1.2, w: 3.95, h: 5.2, fill: { color: 'F2F5FA' }, line: { color: BL, width: 1 } });
sl.addText([['Design', 'Factorial RBD: 4 sowing dates × 3 varieties = 12 treatments'], ['Plots', '36 inoculated (R1–R3) + 12 healthy (one per treatment) = 48'], ['Plot size', PL + ' m × ' + PW + ' m (' + PL * PW + ' m²); ' + BUND + ' m bunds; 2 m channels'],
  ['Buffer', BUF + ' m without crucifers between healthy and inoculated blocks'], ['Field', TOT + ' m × 24 m'], ['Inoculation', 'One inoculation date; crop age at inoculation differs with sowing date (10-day steps)']]
  .map((r, i, a) => [{ text: r[0], options: { bold: true, color: BL, breakLine: true } }, { text: r[1], options: { breakLine: i < a.length - 1 } }]).flat(),
  { isTextBox: true, x: 9.1, y: 1.3, w: 3.7, h: 5.0, fontSize: 13, color: '1F1F1F', valign: 'top', paraSpaceAfter: 6, margin: 3, fontFace: 'Calibri' });
pres.writeFile({ fileName: OUT }).then(() => console.log('saved', OUT, 'total', TOT, 'm; scale', s.toFixed(3)));
