// Advisory committee presentation: outline of research work with the updated methodology (drone-based field + glasshouse data).
const pptxgen = require('pptxgenjs');
const path = require('path');
const fs = require('fs');
const { applyTheme } = require('/root/.claude/skills/synced/9bf50f97-a337-4b6b-8c8b-ebd229b7e0d3_d565bc3b-4006-4195-b033-a8c25dfdc114/pptx/scripts/apply_theme.js');
const IMG = path.join(__dirname, 'img');
const LAY = require('./layout.json');
const REFS = fs.existsSync(path.join(__dirname, 'acm_refs.json')) ? require('./acm_refs.json') : [];
const OUT = path.join(__dirname, '../outputs/Advisory_committee_ORW_updated_methodology.pptx');
const THEME = { name: 'ORW advisory', headFontFace: 'Cambria', bodyFontFace: 'Calibri',
  colors: { dk1: '1F2A2A', lt1: 'FFFFFF', dk2: '1F3864', lt2: 'F2F5FA', accent1: '2E75B6', accent2: '2E7D32', accent3: 'C55A11', accent4: '7030A0', accent5: 'C00000', accent6: 'BF9000', hlink: '2E75B6', folHlink: '7030A0' } };
const X = { navy: '1F3864', blue: '2E75B6', field: '2E7D32', glass: 'C55A11', o1: '2E75B6', o2: '7030A0', o3: 'C00000', grey: '595959', lgrey: 'E7E6E6', text: '1F2A2A', gold: 'BF9000',
  lfield: 'E8F5E9', lglass: 'FCE9DC', lo1: 'DEEBF7', lo2: 'EDE2F6', lo3: 'F9E0DE', lcom: 'EEF1F6', out: 'FFF4D6' };
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.theme = { headFontFace: 'Cambria', bodyFontFace: 'Calibri' };
pres.title = 'Outline of research work: AI based multimodal UAV sensing of white rust in mustard (updated methodology)';
const C = pres.SchemeColor;
pres.defineSlideMaster({ title: 'SECTION', background: { color: X.navy }, objects: [
  { placeholder: { options: { name: 'title', type: 'title', x: 0.8, y: 2.3, w: 11.7, h: 1.4, fontSize: 40, bold: true, color: C.background1, fontFace: 'Cambria' }, text: '' } },
  { placeholder: { options: { name: 'body', type: 'body', x: 0.8, y: 3.8, w: 11.7, h: 1.6, fontSize: 20, color: 'D6E0F0' }, text: '' } }] });
pres.defineSlideMaster({ title: 'CONTENT', background: { color: 'FFFFFF' }, margin: [0.5, 0.5, 0.6, 0.5],
  slideNumber: { x: 12.4, y: 7.08, w: 0.6, h: 0.3, fontSize: 10, color: X.grey },
  objects: [{ rect: { x: 0, y: 0, w: 13.333, h: 0.08, fill: { color: X.navy } } },
            { placeholder: { options: { name: 'title', type: 'title', x: 0.45, y: 0.22, w: 12.4, h: 0.75, fontSize: 28, bold: true, color: C.text2, fontFace: 'Cambria', valign: 'middle' }, text: '' } },
            { line: { x: 0.45, y: 1.0, w: 12.43, h: 0, line: { color: X.blue, width: 1.5 } } },
            { text: { text: 'Outline of research work  |  Animesh Panda (13098)  |  Agricultural Physics, ICAR-IARI', options: { x: 0.45, y: 7.08, w: 9, h: 0.3, fontSize: 10, color: X.grey } } }] });
let sec = '';
const slide = (t) => { const s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: sec }); s.addText(t, { placeholder: 'title' }); return s; };
const section = (t, sub) => { sec = t; pres.addSection({ title: t }); const s = pres.addSlide({ masterName: 'SECTION', sectionTitle: t }); s.addText(t, { placeholder: 'title' }); if (sub) s.addText(sub, { placeholder: 'body' }); return s; };
const txt = (s, t, o) => s.addText(t, Object.assign({ isTextBox: true, fontSize: 14, color: X.text, valign: 'top', margin: 3 }, o));
const bul = (s, items, o) => s.addText(items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1 } })), Object.assign({ isTextBox: true, fontSize: 14, color: X.text, paraSpaceAfter: 4, valign: 'top' }, o));
const refl = (s, t, o) => txt(s, 'References: ' + t, Object.assign({ x: 0.45, y: 6.62, w: 12.4, h: 0.42, fontSize: 10, italic: true, color: X.grey }, o));
const H = (t, fill) => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: fill || X.navy } } });
const table = (s, rows, o) => s.addTable([rows[0].map(c => H(c, o.head))].concat(rows.slice(1)), Object.assign({ fontSize: 11, fontFace: 'Calibri', color: X.text, border: { type: 'solid', pt: 0.5, color: 'C9CED6' }, valign: 'middle', autoPage: false, margin: 0.04 }, o));
// flow-chart primitives
const box = (s, x, y, w, h, t, o = {}) => {
  s.addShape(o.shape || pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: o.fill || X.lcom }, line: { color: o.line || o.fill || X.lcom, width: o.lw || 1 }, rectRadius: 0.06, objectName: o.name || 'box' });
  s.addText(t, { isTextBox: true, x, y, w, h, fontSize: o.fs || 11, color: o.color || X.text, bold: !!o.bold, align: o.align || 'center', valign: o.valign || 'middle', margin: o.margin == null ? 3 : o.margin, fontFace: o.font || 'Calibri', paraSpaceAfter: 2 });
};
const hbox = (s, x, y, w, h, title, body, col, light, o = {}) => {  // header + body box
  const th = o.th || 0.36;
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: light }, line: { color: col, width: 1.25 }, objectName: 'hbox ' + title.slice(0, 20) });
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h: th, fill: { color: col }, line: { color: col, width: 1.25 } });
  s.addText(title, { isTextBox: true, x, y, w, h: th, fontSize: o.tfs || 12, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', margin: 2 });
  const b = Array.isArray(body) ? (typeof body[0] === 'object' ? body : body.map((t, i) => ({ text: t, options: { bullet: o.nobullet ? false : { indent: 10 }, breakLine: i < body.length - 1 } }))) : body;
  s.addText(b, { isTextBox: true, x: x + 0.04, y: y + th + 0.03, w: w - 0.08, h: h - th - 0.06, fontSize: o.fs || 10.5, color: X.text, valign: 'top', margin: 2, paraSpaceAfter: 2, align: o.align || 'left' });
};
const arrow = (s, x1, y1, x2, y2, col, o = {}) => s.addShape(pres.shapes.LINE, { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1) || 0.001, h: Math.abs(y2 - y1) || 0.001, flipH: x2 < x1, flipV: y2 < y1,
  line: { color: col || X.grey, width: o.w || 1.5, endArrowType: o.noHead ? undefined : 'triangle', dashType: o.dash || 'solid' } });
const poly = (s, pts, col, o = {}) => { for (let i = 0; i < pts.length - 1; i++) arrow(s, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], col, Object.assign({}, o, { noHead: i < pts.length - 2 })); };
const img = (s, f, x, y, w, h, o = {}) => s.addImage(Object.assign({ path: path.join(IMG, f), x, y, w, h, altText: o.alt || f }, o.sizing ? { sizing: o.sizing } : {}));
const figpath = (p) => path.join(__dirname, '..', p);
const banner = (s, t, col, light, y = 6.12, h = 0.45) => {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.45, y, w: 12.43, h, fill: { color: light || X.out }, line: { color: col || X.gold, width: 1 }, rectRadius: 0.06, objectName: 'banner' });
  s.addText(t, { isTextBox: true, x: 0.6, y, w: 12.15, h, fontSize: 12.5, color: X.text, valign: 'middle', margin: 2 });
};
const legend = (s, x, y) => { [['Drone / field', X.field], ['Glasshouse', X.glass], ['Common', X.navy]].forEach((l, i) => { s.addShape(pres.shapes.RECTANGLE, { x: x + i * 1.75, y: y + 0.05, w: 0.22, h: 0.18, fill: { color: l[1] }, line: { color: l[1] } }); txt(s, l[0], { x: x + i * 1.75 + 0.26, y, w: 1.45, h: 0.28, fontSize: 10.5, margin: 0 }); }); };

// =========================== 1 TITLE ===========================
sec = 'Introduction'; pres.addSection({ title: sec });
let s = pres.addSlide({ masterName: 'CONTENT', sectionTitle: sec });
s.background = { color: 'FFFFFF' };
img(s, 'logo_l.png', 0.35, 0.3, 1.05, 1.3); img(s, 'logo_r.png', 11.75, 0.35, 1.25, 1.25);
txt(s, 'OUTLINE OF RESEARCH WORK', { x: 1.6, y: 0.45, w: 10.1, h: 0.7, fontSize: 32, bold: true, color: X.field, align: 'center', fontFace: 'Cambria' });
txt(s, 'Updated methodology: drone-based field and glasshouse experiments', { x: 1.6, y: 1.15, w: 10.1, h: 0.45, fontSize: 18, color: X.glass, align: 'center', italic: true });
s.addShape(pres.shapes.RECTANGLE, { x: 1.6, y: 1.95, w: 10.1, h: 1.15, fill: { color: X.lcom }, line: { color: X.blue, width: 1 } });
txt(s, 'AI based multimodal UAV sensing of white rust in mustard', { x: 1.6, y: 1.95, w: 10.1, h: 1.15, fontSize: 28, bold: true, color: X.navy, align: 'center', valign: 'middle', fontFace: 'Cambria' });
txt(s, [{ text: 'Animesh Panda', options: { bold: true, fontSize: 22, color: X.navy, breakLine: true } }, { text: 'Ph.D. (Agricultural Physics)  |  Roll No. 13098', options: { fontSize: 16, color: X.o3, breakLine: true } },
  { text: 'Major field: Agricultural Physics  |  Minor field: Environmental Science', options: { fontSize: 14, color: X.grey, breakLine: true } }, { text: 'Date of joining: 19 February 2025', options: { fontSize: 14, color: X.grey } }], { x: 1.6, y: 3.4, w: 10.1, h: 1.6, align: 'center' });
txt(s, 'Division of Agricultural Physics, ICAR-Indian Agricultural Research Institute, New Delhi 110012', { x: 1.0, y: 5.6, w: 11.3, h: 0.5, fontSize: 18, bold: true, color: X.field, align: 'center' });
txt(s, 'Advisory committee meeting  |  rabi 2026-27', { x: 1.0, y: 6.15, w: 11.3, h: 0.4, fontSize: 14, color: X.grey, align: 'center' });

// =========================== 2 ADVISORY COMMITTEE ===========================
s = slide('Advisory committee');
table(s, [['Role', 'Name and designation', 'Division'], ['Chairperson', 'Dr. Rabi Narayan Sahoo (Principal Scientist)', 'Agricultural Physics'], ['Co-Chairperson', 'Dr. Rajeev Ranjan (Senior Scientist)', 'Agricultural Physics'],
  ['Member', 'Dr. Bidisha Chakrabarti (Principal Scientist)', 'Environmental Science'], ['Member', 'Dr. Amrender Kumar (Principal Scientist)', 'Agricultural Statistics'], ['Member', 'Dr. Chandan Kumar Deb (Scientist)', 'Computer Application'],
  ['Member', 'Dr. Lakshman Prasad (Principal Scientist)', 'Plant Pathology']], { x: 1.6, y: 1.4, w: 10.1, colW: [2.4, 4.9, 2.8], fontSize: 16, rowH: 0.62 });

// =========================== 3 OUTLINE ===========================
s = slide('Outline of the presentation');
const parts = [['1', 'Background, previous work and research gaps', X.navy], ['2', 'Objectives and what has been updated since the ORW', X.navy], ['3', 'Work done in 2025-26 (progress)', X.navy], ['4', 'Experimental set-up 2026-27: drone field, glasshouse, validation', X.field],
  ['5', 'Data collection: sensors, schedule, ground truth', X.field], ['6', 'Objective 1: characterisation (activities and flow charts)', X.o1], ['7', 'Objective 2: detection and severity discrimination by fusion', X.o2], ['8', 'Objective 3: pre-symptomatic prediction', X.o3], ['9', 'Programme of work, expected outcomes, facilities', X.navy]];
parts.forEach((p, i) => { const x = 0.6 + (i % 3) * 4.15, y = 1.35 + Math.floor(i / 3) * 1.75;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 3.95, h: 1.55, fill: { color: X.lcom }, line: { color: p[2], width: 1 }, rectRadius: 0.08 });
  s.addShape(pres.shapes.OVAL, { x: x + 0.2, y: y + 0.45, w: 0.65, h: 0.65, fill: { color: p[2] }, line: { color: p[2] } });
  txt(s, p[0], { x: x + 0.2, y: y + 0.45, w: 0.65, h: 0.65, fontSize: 20, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', margin: 0 });
  txt(s, p[1], { x: x + 1.0, y: y + 0.15, w: 2.85, h: 1.25, fontSize: 15, bold: true, color: X.navy, valign: 'middle' }); });

// =========================== 4 BACKGROUND ===========================
s = slide('Background and rationale');
hbox(s, 0.45, 1.2, 6.1, 5.3, 'Mustard and white rust', ['Indian mustard (Brassica juncea) covers > 90% of rapeseed-mustard area in India and gives 27% of national vegetable-oil output; it is a priority crop of NMEO-Oilseeds',
  'White rust (Albugo candida), an obligate biotrophic oomycete, causes 20–60% yield loss (Kumar and Kalha, 2005)', 'Favoured by mean temperature 11.4–17.7 °C and RH > 70% (Bal and Kumar, 2014); Tmax 16–24 °C, Tmin > 12 °C, morning RH > 97% (Chattopadhyay et al., 2011)',
  'Local pustules on leaves and stems; systemic infection gives staghead (distorted, sterile inflorescence) (Saharan et al., 2014)', 'Visual scoring is slow, subjective and possible only after symptoms appear'], X.field, X.lfield, { fs: 14.5 });
hbox(s, 6.75, 1.2, 6.13, 5.3, 'Why multimodal UAV sensing', ['Pigment and water changes precede visible pustules and can be sensed early (Terentev et al., 2022; Abdulridha et al., 2023)',
  'Each sensor sees a different plant response: RGB (colour, texture), multispectral (pigments), thermal (stomatal closure, transpiration), hyperspectral (fine biochemical change)',
  'Fusion of spectral, structural and thermal information gives higher accuracy than single sensors (Maimaitijiang et al., 2020; Feng et al., 2022)', 'Three fusion levels: data (raw inputs), feature (combined features), model/decision (combined outputs) (Li and Tang, 2024)',
  'A glasshouse study under controlled infection gives the physiological basis and dense early-time data; the drone field study tests it under real canopy conditions'], X.blue, X.lo1, { fs: 14.5 });

s = slide('White rust of mustard: symptoms and favourable weather');
img(s, 'wr_lower.png', 0.45, 1.25, 3.0, 2.55); img(s, 'wr_upper.png', 3.6, 1.25, 3.0, 2.55); img(s, 'staghead.png', 0.45, 4.05, 2.5, 2.4);
txt(s, 'White pustules (lower and upper leaf surface)', { x: 0.45, y: 3.8, w: 6.15, h: 0.25, fontSize: 11, italic: true, align: 'center', color: X.grey, margin: 0 });
txt(s, 'Staghead (systemic infection of the inflorescence)', { x: 3.05, y: 5.0, w: 3.55, h: 0.6, fontSize: 11, italic: true, color: X.grey });
table(s, [['Weather variable', 'Favourable range'], ['Maximum temperature', '16–24 °C'], ['Minimum temperature', '> 12 °C'], ['Afternoon RH', '> 40%'], ['Morning RH', '> 97%'], ['Mean temperature', '11.4–17.7 °C (RH > 70%)']], { x: 7.0, y: 1.3, w: 5.8, colW: [3.0, 2.8], fontSize: 14, rowH: 0.45 });
bul(s, ['Incubation period 4–9 days; latent period 9–12 days', 'Spectral expectation: chlorophyll loss (visible, red edge), mesophyll damage (NIR), leaf-water loss (SWIR, canopy temperature)'], { x: 7.0, y: 4.35, w: 5.8, h: 1.6, fontSize: 14 });
refl(s, 'Bal and Kumar, 2014; Chattopadhyay et al., 2011; Saharan et al., 2014.');

// =========================== 6 PREVIOUS WORK ===========================
s = slide('Previous work: sensing and AI for crop diseases');
table(s, [['Study', 'Crop / disease', 'Data', 'Method', 'Key result'], ['Zhu et al., 2017', 'Tobacco / TMV', 'HSI 380–1023 nm', 'SPA + GLCM; BPNN, ELM, LS-SVM', '95% accuracy 2 days after infection'],
  ['Mahlein et al., 2019', 'Wheat / Fusarium head blight', 'HSI, thermography, fluorescence', 'SVM', 'HSI earliest (3 DAI); HSI + IRT 90%'], ['Abdulridha et al., 2019', 'Citrus / canker', 'HSI lab + UAV', 'RBF network', '96% lab, 100% UAV'],
  ['Tian et al., 2021', 'Rice / leaf blast', 'Spectra 350–2500 nm', 'DSSFs; VIF → SFFS; SVM', '> 65% asymptomatic, 95% mild'], ['Feng et al., 2022', 'Wheat / powdery mildew', 'HS + thermal + RGB', 'PLSR, SVR, RFR', 'Fusion R² 0.86–0.87'],
  ['Mustafa et al., 2023', 'Wheat / Fusarium head blight', 'Fluorescence + HS', 'Boruta; KNN, SVM-SFFS', 'R² up to 0.92'], ['Abdulridha et al., 2023', 'Wheat / stem rust', 'UAV HSI, 960 plots', 'RF', '85% four classes, 88% binary'],
  ['Liu et al., 2024', 'Wheat / powdery mildew', 'UAV MS + thermal', 'TTCI, RF', 'R² 0.90, earlier detection'], ['Deng et al., 2024', 'Wheat / stripe rust', 'UAV RGB, MS, TIR', 'RustQNet (deep fusion)', 'Pixel-level DI maps'],
  ['Bhattacharya and Chattopadhyay, 2013', 'Mustard / rot', 'Hyperion + weather', 'Stepwise CDA, indices', 'Multi-stage disease tracking'], ['Shukla et al., 2024', 'Mustard / aphid', 'Ground hyperspectral', 'Correlation scalogram, PLSR', 'Sensitive 690–723 nm']],
  { x: 0.45, y: 1.2, w: 12.43, colW: [2.6, 2.3, 2.3, 2.6, 2.63], fontSize: 11, rowH: 0.42 });

s = slide('Research gaps and how this study addresses them');
const gaps = [['Most UAV disease models work after symptoms appear', 'Dense early sampling (1, 5, 9, 13 DAI) in glasshouse and field; Objective 3 trains models on pre-symptomatic samples labelled retrospectively'],
  ['No integrated multimodal UAV sensing for mustard diseases', 'Same plots imaged by RGB, multispectral, thermal and hyperspectral sensors; sensor-wise characterisation (Objective 1)'],
  ['Limited understanding of multimodal fusion for severity discrimination', 'Systematic comparison of single sensors and eight sensor combinations, feature- and deep-fusion (Objective 2)'],
  ['No white-rust-specific spectral index or physiological link', 'White Rust Index search; features related to RWC, pigments and gas exchange measured on the same leaves'],
  ['Leaf/controlled results rarely transferred to canopy and new sites', 'Glasshouse → field comparison of disease-specific features; independent validation at Bharatpur and farmers\' fields']];
gaps.forEach((g, i) => { const y = 1.25 + i * 1.0;
  box(s, 0.45, y, 5.6, 0.85, g[0], { fill: X.lo3, line: X.o3, fs: 13, bold: true, align: 'left', margin: 6 });
  arrow(s, 6.1, y + 0.42, 6.75, y + 0.42, X.grey);
  box(s, 6.8, y, 6.08, 0.85, g[1], { fill: X.lfield, line: X.field, fs: 12.5, align: 'left', margin: 6 }); });
txt(s, 'Gap', { x: 0.45, y: 0.98, w: 5.6, h: 0.3, fontSize: 12, bold: true, color: X.o3, margin: 0 }); txt(s, 'How it is addressed', { x: 6.8, y: 0.98, w: 6.0, h: 0.3, fontSize: 12, bold: true, color: X.field, margin: 0 });

// =========================== OBJECTIVES ===========================
s = slide('Objectives');
const objs = [['1', 'To characterise white rust of mustard through multimodal sensing from UAV platform', 'Which bands, indices, textures and thermal features respond to white rust, and how they relate to plant physiology (field and glasshouse)', X.o1, X.lo1],
  ['2', 'To detect and discriminate disease severity of white rust in mustard through AI based multimodal data fusion', 'Six-grade classification, healthy vs diseased detection and PDI regression with single sensors and sensor fusion; severity maps; independent validation', X.o2, X.lo2],
  ['3', 'To predict white rust at pre-symptomatic stage using machine learning technique(s)', 'Healthy vs infected-but-not-yet-symptomatic classification; earliest detection day (DAI); risk maps', X.o3, X.lo3]];
objs.forEach((o, i) => { const y = 1.3 + i * 1.75;
  s.addShape(pres.shapes.RECTANGLE, { x: 0.45, y, w: 1.3, h: 1.55, fill: { color: o[3] }, line: { color: o[3] } });
  txt(s, 'Objective\n' + o[0], { x: 0.45, y, w: 1.3, h: 1.55, fontSize: 16, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle' });
  s.addShape(pres.shapes.RECTANGLE, { x: 1.75, y, w: 11.13, h: 1.55, fill: { color: o[4] }, line: { color: o[3] } });
  txt(s, [{ text: o[1], options: { bold: true, fontSize: 17, color: X.navy, breakLine: true } }, { text: o[2], options: { fontSize: 13, color: X.text } }], { x: 1.9, y: y + 0.08, w: 10.9, h: 1.4, valign: 'middle' }); });

s = slide('What is updated since the ORW (2025)');
table(s, [['Component', 'ORW (2025)', 'Updated methodology (2026-27)'], ['Experiments', 'Field (IARI) + controlled condition; 72 plots of 3 m × 3 m', 'Drone field: 48 plots of 5 m × 3 m (4 dates × 3 varieties × 3 rep. + 12 healthy); glasshouse: 48 pots; validation at Bharatpur'],
  ['Sensors', 'RGB, MS, TIR, Headwall Co-Aligned HP, ASD', '+ Headwall Nano (VNIR); glasshouse RGB, MS, TIR, hyperspectral imaging, ASD; IRGA and canopy analyzer'],
  ['Ground truth', '0–6 scale; DI; five DI classes', 'Leaf grade 0–9 key → six grades (0, 1, 3, 5, 7, 9) and plot PDI (Conn et al., 1990; Wheeler, 1969); staghead %'],
  ['Pre-processing', 'NDVI threshold mask; plot mean', 'NDVI > 0.6 AND SAM < 0.3 rad crop mask on HS, transferred to all sensors; flower pixels removed; SMACC endmember-based plot spectrum'],
  ['Feature selection', 'Many alternative methods (t-test, JM, SPA, RFE, ReliefF, Boruta)', 'Fixed tier chain: correlation scalogram + ReliefF (one band per correlated region) → White Rust Index → ANOVA/Tukey → VIF + stepwise CDA → Boruta'],
  ['Models', 'SVM, BPNN, ELM, LS-SVM, PLS-DA, RF, QDA, RustQNet', 'SVM/SVR, RF/RFR, k-NN, PLS-DA/PLSR, DNN-F1 (input fusion), DNN-F2 (intermediate fusion); encoder-decoder for pixel maps'],
  ['Validation', 'Cross-validation', 'Nested leave-one-replication-out (all selection inside training replications) + Bharatpur + farmers\' fields'],
  ['Metrics', 'Acc, P, R, F1, kappa; R², RMSE, RE', '+ macro-F1, ±1-grade accuracy, RPD; sensitivity, specificity, AUC and earliest detection day for Objective 3']],
  { x: 0.45, y: 1.2, w: 12.43, colW: [1.9, 3.9, 6.63], fontSize: 11.5, rowH: 0.6 });

// =========================== PROGRESS 2025-26 ===========================
section('Work done in 2025-26', 'Field experiment, data collection and leaf-level analysis');
s = slide('Progress in 2025-26');
hbox(s, 0.45, 1.2, 4.0, 4.8, 'Completed', ['IARI field experiment (rabi 2025-26): staggered sowing, inoculation 10 January 2026', 'UAV flights: RGB, multispectral, thermal and hyperspectral sensors', 'Ground data: ASD spectra, visual grades, biophysical and biochemical parameters',
  'Leaf-level ASD analysis: 2339 leaf spectra, 4 dates, 48 plots, full tier methodology applied', 'Detailed methodology document (Objectives 1–3)'], X.field, X.lfield, { fs: 13.5 });
hbox(s, 4.6, 1.2, 4.0, 4.8, 'Key leaf-level findings', ['Red-edge first derivatives (790–830 nm) most robust (r with PDI up to 0.78)', 'White Rust Index ND(750, 948) − 0.5 R696: balanced accuracy 0.77; a whole-range search (400–2400 nm) chose the same region',
  'SWIR water indices respond (|r| up to 0.63)', 'Six-grade macro-F1 0.32, ±1-grade 0.73, healthy vs diseased 0.78; plot PDI R² 0.74 (nested validation)'], X.o1, X.lo1, { fs: 12.5 });
hbox(s, 8.75, 1.2, 4.13, 4.8, 'Lessons used in the update', ['Neighbouring grades overlap → report ±1-grade accuracy and PDI regression', 'Nested selection needed for honest accuracy', 'Healthy plots need isolation → 10 m buffer / isolation compartment', 'Denser early sampling needed for pre-symptomatic analysis → glasshouse study'], X.glass, X.lglass, { fs: 12.5 });
banner(s, 'The leaf-level analysis validated the tier chain on real data; the same chain is now applied to drone and glasshouse imagery.', X.gold, X.out, 6.15, 0.45);

s = slide('Leaf-level proof of concept (ASD, 2025-26)');
s.addImage({ path: figpath('leaf/fig/l_spectra.png'), x: 0.45, y: 1.2, w: 6.2, h: 6.2 * 0.42, altText: 'leaf spectra' });
s.addImage({ path: figpath('leaf/fig/l_wri_full.png'), x: 6.8, y: 1.2, w: 6.08, h: 6.08 * 0.5077, altText: 'WRI' });
bul(s, ['Visible and SWIR reflectance rise, NIR falls and the red-edge peak drops and shifts with grade', 'Whole-range White Rust Index search confirms the VNIR index (red edge, NIR, 970 nm water shoulder)'], { x: 0.45, y: 4.5, w: 12.4, h: 1.0, fontSize: 13 });
refl(s, 'Mahlein et al., 2013; Shukla et al., 2024; Robnik-Šikonja and Kononenko, 2003.');

// ---------- UAV image processing done (from lab notebook) ----------
s = slide('UAV processing done (2025-26): hyperspectral cubes');
const hp = [['Raw cube', 'Headwall Co-Aligned HP (VNIR + SWIR): 613 bands; imported in ENVI, saved in ENVI format'], ['Spectral subset', 'VNIR up to 919.7 nm + SWIR from 921.4 nm; water and noisy bands removed: 900–915, 1335–1460, 1785–1965, 2400–2500 nm (and 1964.4 nm) → 483 bands'],
  ['Smoothing', 'Savitzky–Golay filter in ENVI: filter width 5, polynomial order 2; exported'], ['Projection', 'ArcMap: WGS 1984 / UTM zone 43N (Project, data management)'],
  ['Plot boundaries', 'Plot polygons digitised; field "plot no." added; polygons dissolved/merged; final boundary saved as shapefile'], ['Plot clipping', 'Extract by mask (Spatial Analyst) / subset by ROI in ENVI → one clipped cube per plot']];
hp.forEach((p, i) => { const col = i % 3, row = Math.floor(i / 3), x = 0.45 + col * 4.15, y = 1.25 + row * 2.05;
  box(s, x, y, 0.42, 1.75, String(i + 1), { fill: X.field, line: X.field, color: 'FFFFFF', bold: true, fs: 15 });
  box(s, x + 0.47, y, 3.45, 1.75, [{ text: p[0], options: { bold: true, color: X.field, fontSize: 13, breakLine: true } }, { text: p[1] }], { fill: X.lfield, line: X.field, fs: 11.5, align: 'left', valign: 'top', margin: 6 });
  if (col < 2) arrow(s, x + 3.92, y + 0.87, x + 4.15, y + 0.87, X.field); });
arrow(s, 12.6, 3.0, 12.6, 3.15, X.field, { noHead: true }); poly(s, [[12.75, 3.0], [12.75, 3.17], [0.66, 3.17], [0.66, 3.3]], X.field);
hbox(s, 0.45, 5.45, 8.0, 1.15, 'Status', 'Clipping completed for three flight dates (11 Feb, 24 Feb and 13 Mar 2026); 13 Mar cube processing in progress. RGB, multispectral (MicaSense RedEdge-MX), thermal and Headwall Nano data follow the same projection and plot boundaries.', X.navy, X.lcom, { nobullet: true, fs: 11.5 });
hbox(s, 8.6, 5.45, 4.28, 1.15, 'Open checks', ['MS data units: DN, radiance or scaled reflectance (metadata)', 'Thermal: emissivity correction applied?'], X.o3, X.lo3, { fs: 11 });
refl(s, 'Savitzky and Golay, 1964; Thenkabail et al., 2004.', { y: 6.72, h: 0.3 });

s = slide('UAV processing done (2025-26): crop mask (SAM × NDVI)');
box(s, 0.45, 1.25, 2.7, 1.5, [{ text: 'Training ROIs', options: { bold: true, fontSize: 13, breakLine: true } }, { text: 'Soil, shadow, grass, mustard (+ flower); 3 × 2 training sites per plot; 48 plot ROIs' }], { fill: X.lfield, line: X.field, fs: 11 });
box(s, 3.55, 1.25, 2.9, 0.68, [{ text: 'SAM classification', options: { bold: true, breakLine: true } }, { text: 'angle 0.1, 0.2, 0.3 rad tested' }], { fill: X.field, line: X.field, color: 'FFFFFF', fs: 11 });
box(s, 3.55, 2.07, 2.9, 0.68, [{ text: 'NDVI (band math)', options: { bold: true, breakLine: true } }, { text: '(R898 − R684)/(R898 + R684)' }], { fill: X.field, line: X.field, color: 'FFFFFF', fs: 11 });
arrow(s, 3.15, 2.0, 3.55, 1.6, X.field); arrow(s, 3.15, 2.0, 3.55, 2.4, X.field);
box(s, 6.85, 1.25, 2.6, 1.5, [{ text: 'Binary masks multiplied', options: { bold: true, breakLine: true } }, { text: 'NDVI > 0.6 × SAM mustard class (0.3 rad) = crop pixels' }], { fill: X.lcom, line: X.navy, fs: 11 });
arrow(s, 6.45, 1.6, 6.85, 1.9, X.field); arrow(s, 6.45, 2.4, 6.85, 2.1, X.field);
box(s, 9.85, 1.25, 3.03, 1.5, [{ text: 'Morphological erosion', options: { bold: true, breakLine: true } }, { text: 'removes mixed edge pixels; saved as GeoTIFF' }], { fill: X.lcom, line: X.navy, fs: 11 });
arrow(s, 9.45, 2.0, 9.85, 2.0, X.navy);
const vs = [['Reclassify', 'mustard = 2, others = 1'], ['Raster → polygon', '"simplify polygons" unchecked'], ['Select by attribute', 'grid code of mustard class'], ['Clip and export', 'crop polygons / masked cube per plot']];
vs.forEach((v, i) => { const x = 0.45 + i * 3.15; box(s, x, 3.3, 2.9, 0.95, [{ text: v[0], options: { bold: true, breakLine: true } }, { text: v[1] }], { fill: X.lo1, line: X.o1, fs: 11.5 }); if (i < 3) arrow(s, x + 2.9, 3.77, x + 3.15, 3.77, X.o1); });
poly(s, [[11.36, 2.75], [11.36, 3.02], [1.9, 3.02], [1.9, 3.3]], X.navy);
bul(s, ['Same crop polygons are applied to RGB, multispectral and thermal images after co-registration', 'True-colour display: R 640–670, G 540–570, B 460–480 nm (bands near 644, 544, 466 nm)', 'Crop stage differed among plots on one date (16 vegetative, 22 flowering, 10 pod-formation plots) → flower pixels must be handled before leaf-based analysis'], { x: 0.45, y: 4.5, w: 12.43, h: 1.6, fontSize: 13 });
banner(s, 'Matches the agreed methodology: crop mask = NDVI > 0.6 AND SAM < 0.3 rad, with 1-pixel edge erosion.', X.gold, X.out, 6.12, 0.45);
refl(s, 'Kruse et al., 1993; Rouse et al., 1974.', { y: 6.72, h: 0.3 });

s = slide('UAV processing done (2025-26): endmember extraction (SMACC)');
const em = [['Subset cube', '483-band subset (.hdr) of one date opened in ENVI'], ['Plot ROI', 'Plot boundary shapefile → ROI per plot (48 ROIs); subset data from ROI'], ['SMACC', 'Sequential maximum angle convex cone endmember extraction run plot by plot'], ['Outputs', 'Spectral library (endmembers), abundance maps, endmember ROIs; signatures exported']];
em.forEach((e, i) => { const x = 0.45 + i * 3.15; box(s, x, 1.3, 2.9, 1.55, [{ text: e[0], options: { bold: true, fontSize: 13.5, breakLine: true } }, { text: e[1] }], { fill: X.field, line: X.field, color: 'FFFFFF', fs: 11.5 }); if (i < 3) arrow(s, x + 2.9, 2.07, x + 3.15, 2.07, X.field); });
hbox(s, 0.45, 3.15, 6.1, 2.85, 'Next steps (agreed methodology)', ['Label endmembers: crop (green, chlorotic, pustule) vs non-crop (soil, shadow, grass) by NDVI and spectral angle', 'Remove non-crop endmembers; average crop endmembers → plot spectrum', 'Chlorotic and pustule endmembers are kept (disease signal)', 'Repeat for every date; then features and tiers (Objective 1)'], X.o1, X.lo1, { fs: 12.5 });
hbox(s, 6.75, 3.15, 6.13, 2.85, 'Open question: keep or remove flowers?', ['Proposal: remove flower pixels/endmembers from the leaf spectrum, because yellow petals dominate 500–650 nm and flowering differs with sowing date and variety (Sulik and Long, 2016)', 'Keep the flower fraction as a covariate', 'Keep inflorescence pixels for staghead severity after flowering', 'For advisory committee decision'], X.glass, X.lglass, { fs: 12 });
refl(s, 'Gruninger et al., 2004; Sulik and Long, 2016; Winter, 1999.', { y: 6.15, h: 0.3 });

// ---------- dataset structure (2025-26) ----------
s = slide('2025-26 drone dataset: structure and sample size');
{ const lv = [['7 flight dates', 'each with all four sensors'], ['4 sensors per date', 'Hyperspectral, multispectral, RGB, thermal (28 images)'], ['48 plots per image', '12 treatments × 3 replications + 12 healthy'], ['4 subplots per plot', 'quadrants inside the eroded crop mask']];
  lv.forEach((l, i) => { const y = 1.25 + i * 1.12; box(s, 0.45 + i * 0.3, y, 4.1, 0.9, [{ text: l[0], options: { bold: true, fontSize: 14, breakLine: true } }, { text: l[1], options: { fontSize: 11 } }], { fill: [X.navy, X.blue, X.field, X.glass][i], line: [X.navy, X.blue, X.field, X.glass][i], color: 'FFFFFF' });
    if (i < 3) arrow(s, 2.5 + i * 0.3, y + 0.9, 2.8 + i * 0.3, y + 1.12, X.grey); }); }
[['336', 'plot-dates (7 × 48)'], ['1344', 'labelled subplot-dates per sensor (7 × 48 × 4)'], ['5376', 'sensor × subplot-date records (4 × 1344)']].forEach((c, i) => { const x = 5.75 + i * 2.4;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.25, w: 2.25, h: 1.25, fill: { color: X.lcom }, line: { color: X.lcom }, rectRadius: 0.08 });
  txt(s, c[0], { x, y: 1.3, w: 2.25, h: 0.6, fontSize: 28, bold: true, color: X.navy, align: 'center', fontFace: 'Cambria', margin: 0 }); txt(s, c[1], { x: x + 0.1, y: 1.9, w: 2.05, h: 0.55, fontSize: 11, align: 'center', margin: 0 }); });
hbox(s, 5.75, 2.75, 7.13, 3.3, 'How the subplots are used', ['Modelling unit = subplot-date: features = mean of crop pixels in each subplot (after the SAM × NDVI mask)',
  'Label = canopy-level disease severity score recorded in the field for every subplot → 1344 labelled subplot-dates (the same labels serve all four sensors)',
  'Validation: the four subplots of a plot always stay in the same fold (leave-one-replication-out), so they never leak between training and test',
  'Statistics (ANOVA, Tukey): on plot means, or a mixed model with plot as a random effect, because subplots are not independent replicates',
  'Plot prediction = mean of its four subplot predictions; their spread gives within-plot variability'], X.field, X.lfield, { fs: 11.5 });
banner(s, 'Pre- and post-symptomatic sets are split by flight date (dates before the first visible pustule → Objective 3).', X.gold, X.out, 6.2, 0.4);

// =========================== FRAMEWORK ===========================
section('Overall research framework', 'Two experimental platforms, one methodology');
s = slide('Overall research framework');
legend(s, 7.6, 1.05);
hbox(s, 0.45, 1.4, 4.0, 1.25, 'Drone-based field experiment', 'IARI, rabi 2025-26 and 2026-27; 48 plots; UAV RGB, MS, TIR, HS (Headwall Co-Aligned HP, Nano) + ASD, LAI, IRGA', X.field, X.lfield, { nobullet: true, fs: 10.5 });
hbox(s, 4.67, 1.4, 4.0, 1.25, 'Glasshouse pot experiment', 'Division of Plant Pathology, 2026-27; 48 pots; RGB, MS, TIR, hyperspectral imaging, ASD, IRGA', X.glass, X.lglass, { nobullet: true, fs: 10.5 });
hbox(s, 8.88, 1.4, 4.0, 1.25, 'Ground truth (both)', 'Leaf grade 0–9 → six grades, PDI, staghead %; RWC, MSI, chlorophyll a, b, carotenoid, anthocyanin, protein, Pn, gs, E', X.navy, X.lcom, { nobullet: true, fs: 10.5 });
box(s, 0.45, 2.95, 12.43, 0.62, 'Pre-processing: radiometric calibration → orthomosaic / image cubes → co-registration → crop mask (NDVI > 0.6 AND SAM < 0.3 rad) → flower removal → plot / pot spectra and features', { fill: X.lcom, line: X.navy, fs: 12.5, bold: true });
[2.45, 6.67, 10.88].forEach(x => arrow(s, x, 2.65, x, 2.95, X.navy));
const ob = [[0.45, 'Objective 1: Characterisation', ['Sensor-wise features', 'Tiers: scalogram + ReliefF, White Rust Index, ANOVA, VIF + CDA, Boruta', 'Physiology links; glasshouse vs field'], X.o1, X.lo1],
  [4.67, 'Objective 2: Detection and severity', ['VIF → ML-SFFS optimum features', 'Six models; 8 sensor sets; feature and deep fusion', 'Six grades, healthy vs diseased, PDI; maps'], X.o2, X.lo2],
  [8.88, 'Objective 3: Pre-symptomatic prediction', ['Retrospective labels (1–13 DAI)', 't-test, Boruta → VIF → ML-SFFS', 'SVM, RF, k-NN; earliest DAI; risk maps'], X.o3, X.lo3]];
ob.forEach(o => { hbox(s, o[0], 3.95, 4.0, 1.65, o[1], o[2], o[3], o[4], { fs: 11 }); arrow(s, o[0] + 2.0, 3.57, o[0] + 2.0, 3.95, X.navy); });
arrow(s, 4.45, 4.78, 4.67, 4.78, X.o1); arrow(s, 8.67, 4.78, 8.88, 4.78, X.o2);
box(s, 0.45, 5.9, 12.43, 0.62, 'Validation: nested leave-one-replication-out  →  IIRMR Bharatpur experiment  →  farmers\' fields (2026-27)  →  disease-specific features, best sensor/fusion model, early-warning maps', { fill: X.out, line: X.gold, fs: 12.5, bold: true });
[2.45, 6.67, 10.88].forEach(x => arrow(s, x, 5.6, x, 5.9, X.gold));

// =========================== EXPERIMENTS ===========================
section('Experimental set-up 2026-27', 'Drone-based field experiment, glasshouse pot study and validation sites');
s = slide('Drone-based field experiment (IARI, rabi 2026-27)');
hbox(s, 0.45, 1.2, 3.55, 5.35, 'Design', ['Crop: Indian mustard; factorial RBD', 'Factor 1, date of sowing: D1 20 Nov, D2 30 Nov, D3 10 Dec, D4 20 Dec 2026; one inoculation date → crop age 20–50 DAS', 'Factor 2, variety: V1 PM 26, V2 Pusa Vijay, V3 PM 37',
  '36 inoculated plots (12 treatments × R1–R3) + 12 healthy plots (one per treatment) = 48 plots', 'Plot 5 m × 3 m; 0.2 m bunds; 2 m channels', 'Healthy block separated by a 10 m buffer (no crucifers) to avoid cross-infection; field 48 m × 24 m', 'Inoculum 1.5 × 10⁵ zoosporangia mL⁻¹ (Mishra et al., 2009)'], X.field, X.lfield, { fs: 11.5 });
// field layout with buffer, scaled from layout.json
{ const L = LAY.buffer10; const ox = 4.15, oy = 1.25, sc = 8.7 / 11.2, x0 = 1.85, y0 = 1.1;
  const T = (o) => ({ x: ox + (o.x - x0) * sc, y: oy + (o.y - y0) * sc, w: Math.max(o.w * sc, 0.01), h: Math.max(o.h * sc, 0.01) });
  L.forEach(o => { if (o.x < x0 - 0.05 || o.t.startsWith('Field layout') || o.t.startsWith('Plot 5') || o.y > 6.5) return; const r = T(o);
    if (o.geom === 'line') { s.addShape(pres.shapes.LINE, { x: r.x, y: r.y, w: o.w ? r.w : 0.001, h: o.h ? r.h : 0.001, line: { color: '555555', width: 1 } }); return; }
    if (o.geom === 'upArrow') { s.addShape(pres.shapes.UP_ARROW, { x: r.x, y: r.y, w: r.w, h: r.h, fill: { color: o.fill }, line: { color: o.fill } }); return; }
    if (o.fill || o.line) s.addShape(o.geom === 'roundRect' ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, { x: r.x, y: r.y, w: r.w, h: r.h, fill: o.fill ? { color: o.fill } : { type: 'none' }, line: o.line ? { color: o.line, width: 0.75, dashType: o.t ? 'solid' : 'dash' } : { type: 'none' }, rectRadius: 0.04 });
    if (o.t) s.addText(o.t.replace(/\n/g, '\n'), { isTextBox: true, x: r.x, y: r.y, w: r.w, h: r.h, fontSize: Math.max(6, (o.sz || 11) * sc * 0.82), bold: !!o.b, color: o.col || '1F1F1F', align: 'center', valign: 'middle', margin: 0 }); });
  s.addImage({ path: path.join(IMG, 'compass.png'), x: 12.0, y: 1.15, w: 0.8, h: 0.8, rotate: 180 }); }
txt(s, 'Layout of the 2026-27 field (plot code: D = sowing date, V = variety; number = plot ID)', { x: 4.15, y: 6.25, w: 8.7, h: 0.3, fontSize: 10.5, italic: true, color: X.grey, align: 'center' });

s = slide('Glasshouse pot experiment (Division of Plant Pathology, 2026-27)');
hbox(s, 0.45, 1.2, 3.55, 5.35, 'Design', ['Treatments: 4 sowing dates (D1–D4, 10-day intervals; inoculation at 20, 30, 40, 50 DAS) × 3 varieties (V1 PM 26, V2 Pusa Vijay, V3 PM 37) = 12', '48 pots: 36 inoculated (12 × 3 replications) + 12 healthy (one per treatment, isolation compartment)',
  'Inoculum 1.5 × 10⁵ zoosporangia mL⁻¹; 10 µL droplets on the adaxial leaf surface', 'Polythene cover for 3 days after inoculation; RH 80–90%, 19 °C', 'Healthy pots kept under the same conditions in a separate compartment (Mishra et al., 2009)', 'Data: 1, 5, 9, 13 DAI, then every 10 days'], X.glass, X.lglass, { fs: 11.5 });
{ const L = LAY.glass; const ox = 4.15, oy = 1.25, sc = 8.7 / 12.6, x0 = 0.4, y0 = 3.4;
  const T = (o) => ({ x: ox + (o.x - x0) * sc, y: oy + (o.y - y0) * sc * 1.25, w: o.w * sc, h: o.h * sc * (o.geom === 'ellipse' ? 1 : 1.25) });
  L.forEach(o => { if (o.y < 3.4) return; const r = T(o); if (o.geom === 'ellipse') { r.w = o.w * sc * 1.25; r.h = r.w; }
    if (o.fill || o.line) s.addShape(o.geom === 'ellipse' ? pres.shapes.OVAL : pres.shapes.RECTANGLE, { x: r.x, y: r.y, w: r.w, h: r.h, fill: o.fill ? { color: o.fill } : { type: 'none' }, line: o.line ? { color: o.line, width: 0.75, dashType: o.geom === 'rect' && !o.t ? 'dash' : 'solid' } : { type: 'none' } });
    if (o.t) s.addText(o.t, { isTextBox: true, x: r.x, y: r.y, w: r.w, h: r.h, fontSize: Math.max(6.5, (o.sz || 11) * sc * (o.geom === 'ellipse' ? 1.0 : 0.95)), bold: !!o.b, color: o.col || '000000', align: o.x > 10 ? 'left' : 'center', valign: o.x > 10 ? 'top' : 'middle', margin: o.x > 10 ? 3 : 0 }); }); }
txt(s, 'Pot arrangement (D = sowing date, V = variety; number = pot ID)', { x: 4.15, y: 6.25, w: 8.7, h: 0.3, fontSize: 10.5, italic: true, color: X.grey, align: 'center' });

s = slide('Roles of the two experiments and the validation sites');
hbox(s, 0.45, 1.2, 4.0, 4.7, 'Glasshouse (controlled)', ['Known inoculation time and uniform infection', 'Dense early data: 1, 5, 9, 13 DAI → pre-symptomatic window', 'Leaf and pot imaging without soil, wind or illumination change', 'Physiology on the same leaves: RWC, MSI, pigments, protein, gas exchange', 'Answers: what changes, when, and why'], X.glass, X.lglass, { fs: 14 });
hbox(s, 4.67, 1.2, 4.0, 4.7, 'Drone field (IARI)', ['Natural canopy with soil, shadow, flowers, weather', 'Same treatments and schedule as glasshouse', 'Canopy-scale UAV RGB, MS, TIR, HS', 'Training and nested validation of models (LORO)', 'Answers: does it work at canopy scale from a drone'], X.field, X.lfield, { fs: 14 });
hbox(s, 8.88, 1.2, 4.0, 4.7, 'Validation (Bharatpur, farmers\' fields)', ['Stage 1: IIRMR research farm, local varieties, monitored ground truth', 'Stage 2: adjoining farmers\' fields, heterogeneous conditions', 'Best models applied without retraining', 'Answers: does it transfer to new sites and varieties'], X.navy, X.lcom, { fs: 14 });
arrow(s, 4.45, 3.55, 4.67, 3.55, X.grey); arrow(s, 8.67, 3.55, 8.88, 3.55, X.grey);
banner(s, 'Glasshouse explains the mechanism and the earliest change; the drone field tests it at canopy scale; Bharatpur and farmers\' fields test transfer.', X.gold, X.out, 6.1, 0.45);

// =========================== DATA COLLECTION ===========================
section('Data collection', 'Sensors, schedule, ground truth and biophysico-chemical parameters');
s = slide('Drone and ground sensors (field)');
img(s, 'dji.png', 0.5, 1.2, 1.55, 1.05); img(s, 'micasense.png', 2.2, 1.15, 1.15, 1.15); img(s, 'flir.png', 3.5, 1.15, 1.25, 1.12); img(s, 'headwall.png', 4.9, 1.12, 1.25, 1.19); img(s, 'asd.png', 6.3, 1.2, 1.6, 1.05);
['RGB', 'MS', 'TIR', 'HS', 'ASD'].forEach((t, i) => txt(s, t, { x: [0.5, 2.2, 3.5, 4.9, 6.3][i], y: 2.3, w: [1.55, 1.15, 1.25, 1.25, 1.6][i], h: 0.25, fontSize: 10, align: 'center', color: X.grey, margin: 0 }));
table(s, [['Sensor', 'Bands / range', 'Resolution', 'GSD at 30 m', 'Information'], ['RGB: DJI Phantom', 'R, G, B', '5472 × 3648', '0.8 cm', 'Colour, texture, pustules'], ['MS: MicaSense RedEdge-MX', '475, 560, 668, 717, 840 nm', '1280 × 960', '2 cm', 'Pigments, red edge'],
  ['TIR: FLIR Vue Pro R (13 mm)', '7.5–13.5 µm', '640 × 480', '3.9 cm', 'Canopy temperature'], ['HS: Headwall Co-Aligned HP', 'VNIR 400–1000 + SWIR 1000–2500 nm', 'VNIR 640, SWIR 320 px', '2.2 cm (processed cube)', 'Biochemistry, water'], ['HS: Headwall Nano', 'VNIR 400–1000 nm', '640 px', 'lens-dependent', 'Fine VNIR, red edge'],
  ['ASD FieldSpec 4', '350–2500 nm (2151 bands)', 'point', '—', 'Reference spectra'], ['Canopy analyzer', 'LAI', '—', '—', 'Canopy structure'], ['IRGA (LI-6400)', 'Pn, gs, E', '—', '—', 'Gas exchange']],
  { x: 0.45, y: 2.65, w: 12.43, colW: [2.6, 3.1, 2.2, 1.5, 3.03], fontSize: 11.5, rowH: 0.36 });
txt(s, 'Flights 11:00–14:00 h under clear sky and low wind; 30 m altitude; 85% front and 80% side overlap; calibration panels and ground control points every flight', { x: 8.05, y: 1.15, w: 4.83, h: 1.35, fontSize: 12, color: X.field, bold: true });

s = slide('Glasshouse sensors and biophysico-chemical parameters');
table(s, [['Glasshouse sensor', 'Measurement'], ['RGB digital camera', 'Leaf/pot images: colour, texture, pustule area'], ['Multispectral camera', 'Band reflectance, indices'], ['Thermal camera', 'Leaf/canopy temperature, CTD'], ['Hyperspectral imaging', 'Image cubes (VNIR) of leaves and pots'], ['ASD (contact probe / leaf clip)', 'Leaf spectra 350–2500 nm'], ['IRGA', 'Pn, gs, E'], ['Visual scoring', 'Leaf grade 0–9, PDI']], { x: 0.45, y: 1.2, w: 5.0, colW: [2.3, 2.7], fontSize: 12, rowH: 0.48, head: X.glass });
table(s, [['Parameter', 'Method', 'Reference'], ['Relative water content (%)', 'Dehydration and imbibition', 'Barrs and Weatherley, 1962'], ['Membrane stability index', 'Electrolyte leakage', 'Dwivedi et al., 2018'], ['Pn, gs, E', 'LI-6400 gas exchange', 'Riches et al., 2020'],
  ['Leaf area index (field)', 'Canopy analyzer', 'Behera et al., 2010'], ['Chlorophyll a, b', 'DMSO, spectrophotometry', 'Wellburn, 1994'], ['Carotenoids', 'Spectrophotometry', 'Lichtenthaler and Wellburn, 1983'], ['Anthocyanin', 'pH differential method', 'Lee et al., 2005'], ['Total protein', 'Bradford method', 'Bradford, 1976']],
  { x: 5.7, y: 1.2, w: 7.18, colW: [2.4, 2.3, 2.48], fontSize: 12, rowH: 0.48 });
banner(s, 'Biophysico-chemical parameters are measured on the same leaves after imaging, in both experiments, so that spectral and thermal features can be explained physiologically.', X.gold, X.out, 5.75, 0.6);

s = slide('Data collection schedule (field and glasshouse)');
{ const days = [-1, 1, 5, 9, 13, 23, 33, 43, 53]; const x0 = 1.9, x1 = 12.6, sx = (x1 - x0) / 56; const xp = d => x0 + 0.3 + days.indexOf(d) * (x1 - x0 - 0.6) / (days.length - 1);
  [['Glasshouse', 1.7, X.glass], ['Drone field', 2.75, X.field]].forEach(r => { txt(s, r[0], { x: 0.45, y: r[1] - 0.18, w: 1.4, h: 0.36, fontSize: 13, bold: true, color: r[2], margin: 0 });
    arrow(s, x0, r[1], x1, r[1], r[2], { noHead: false, w: 2 });
    days.forEach(d => { s.addShape(pres.shapes.OVAL, { x: xp(d) - 0.11, y: r[1] - 0.11, w: 0.22, h: 0.22, fill: { color: d < 0 ? X.grey : (d <= 13 ? 'FFFFFF' : r[2]) }, line: { color: d < 0 ? X.grey : r[2], width: 1.5 } }); }); });
  days.forEach(d => txt(s, d < 0 ? 'Before\ninoc.' : d + ' DAI', { x: xp(d) - 0.45, y: 3.05, w: 0.9, h: 0.45, fontSize: 10, align: 'center', margin: 0, color: X.text }));
  s.addShape(pres.shapes.RECTANGLE, { x: xp(1) - 0.3, y: 1.35, w: xp(13) - xp(1) + 0.6, h: 1.62, fill: { type: 'none' }, line: { color: X.o3, width: 1, dashType: 'dash' } });
  txt(s, 'Pre-symptomatic window (Objective 3)', { x: xp(1) - 0.2, y: 1.05, w: 3.2, h: 0.3, fontSize: 11, color: X.o3, bold: true, margin: 0 });
  txt(s, '… every 10 days until maturity (Objectives 1–2)', { x: xp(23) - 0.2, y: 1.05, w: 5, h: 0.3, fontSize: 11, color: X.navy, bold: true, margin: 0 }); }
table(s, [['Measured on each date', 'Drone field', 'Glasshouse'], ['RGB', 'UAV (DJI Phantom) + digital camera', 'Digital camera'], ['Multispectral', 'UAV (MicaSense RedEdge-MX)', 'Multispectral camera'], ['Thermal', 'UAV (FLIR Vue Pro R)', 'Thermal camera'],
  ['Hyperspectral', 'UAV (Headwall Co-Aligned HP; Nano)', 'Hyperspectral imaging'], ['Point spectra', 'ASD (canopy and leaf)', 'ASD (leaf contact probe)'], ['Physiology', 'IRGA, canopy analyzer, RWC, MSI, pigments, protein', 'IRGA, RWC, MSI, pigments, protein'], ['Disease', 'Leaf grade 0–9 (5 points/plot), PDI, staghead', 'Leaf grade 0–9 (all leaves), PDI']],
  { x: 0.45, y: 3.65, w: 12.43, colW: [2.4, 5.2, 4.83], fontSize: 11.5, rowH: 0.34 });

s = slide('Ground truth: disease grade, PDI and staghead severity');
table(s, [['Grade', 'Leaf area with pustules', 'Class'], ['0', 'No symptoms', 'Healthy'], ['1', '1–5%', 'Very low'], ['3', '6–10%', 'Low'], ['5', '11–25%', 'Moderate'], ['7', '26–50%', 'High'], ['9', '> 50%', 'Very high']], { x: 0.45, y: 1.2, w: 5.2, colW: [1.0, 2.5, 1.7], fontSize: 13, rowH: 0.45 });
hbox(s, 5.9, 1.2, 6.98, 3.15, 'Severity indices', [{ text: 'Percent disease index (plot or pot):', options: { bold: true, breakLine: true } }, { text: 'PDI = Σ (grade × number of leaves) / (total leaves × 9) × 100', options: { breakLine: true } },
  { text: 'Staghead severity (after flowering):', options: { bold: true, breakLine: true } }, { text: 'Staghead % = infected racemes / total racemes × 100 (Ram and Awasthi, 2018)', options: { breakLine: true } },
  { text: 'Labels:', options: { bold: true, breakLine: true } }, { text: 'Six grades (classification), healthy vs diseased (detection), PDI (regression); pre-symptomatic = inoculated plants before the first visible pustule' }], X.navy, X.lcom, { fs: 12.5, nobullet: true });
bul(s, ['Field: centre and four corners of each plot, all fully expanded leaves of uniform plants', 'Glasshouse: all leaves of each pot; tagged leaves for repeated measurements', 'One trained scorer, written grade limits (Bock et al., 2010)'], { x: 5.9, y: 4.5, w: 6.98, h: 1.5, fontSize: 13 });
refl(s, 'Conn et al., 1990; Wheeler, 1969; Ram and Awasthi, 2018; Bock et al., 2010.');

// =========================== OBJECTIVE 1 ===========================
section('Objective 1', 'To characterise white rust of mustard through multimodal sensing from UAV platform');
s = slide('Objective 1: activities (drone field and glasshouse)');
table(s, [['Activity', 'Drone-based field', 'Glasshouse', 'Output'], ['1.1 Sensor measurements', 'UAV RGB, MS, TIR, HS (Co-Aligned HP, Nano) + ASD, LAI, IRGA', 'RGB, MS, TIR, hyperspectral imaging, ASD, IRGA', 'Image and spectral data per date'],
  ['1.2 Biophysico-chemical parameters', 'RWC, MSI, pigments, anthocyanin, protein, gas exchange, LAI', 'Same, on imaged leaves', 'Physiological response table'], ['1.3 Disease assessment', 'Grades 0–9 at 5 points/plot; PDI; staghead', 'Grades of all leaves; PDI', 'Labels: six grades, PDI'],
  ['1.4 Pre-processing', 'Calibration, orthomosaic, co-registration, crop mask, flower removal, endmember plot spectrum', 'White/dark reference, leaf/pot segmentation, pustule/chlorosis masks', 'Plot / pot / leaf spectra and images'],
  ['1.5 Feature extraction', 'HS, MS, RGB, TIR features per plot', 'Same features per pot / leaf', 'Feature tables'], ['1.6 Disease-specific features (tiers)', 'Tiers per sensor → DSF pools', 'Tiers per sensor → DSF pools', 'Bands, White Rust Index, DSF pools'],
  ['1.7 Physiology and scale links', 'Feature–physiology correlation', 'Feature–physiology correlation; time trajectories', 'Common glasshouse–field features']],
  { x: 0.45, y: 1.2, w: 12.43, colW: [2.6, 4.0, 3.4, 2.43], fontSize: 11.5, rowH: 0.62 });

s = slide('Objective 1: flow chart');
legend(s, 7.6, 1.05);
const c1 = [[0.45, X.field, X.lfield, 'Drone field data', ['UAV RGB, MS, TIR, HS', 'ASD canopy, LAI, IRGA']], [3.6, X.glass, X.lglass, 'Glasshouse data', ['RGB, MS, TIR, HSI', 'ASD leaf, IRGA']], [6.75, X.navy, X.lcom, 'Ground truth', ['Grades, PDI, staghead', 'RWC, MSI, pigments, protein']]];
c1.forEach(c => hbox(s, c[0], 1.4, 2.95, 1.1, c[3], c[4], c[1], c[2], { fs: 10.5 }));
box(s, 0.45, 2.8, 9.25, 0.5, 'Pre-processing (A1.4): calibration → masks (NDVI > 0.6 AND SAM < 0.3) → flower removal → plot / pot / leaf spectra', { fill: X.lcom, line: X.navy, fs: 11.5, bold: true });
[1.9, 5.05, 8.2].forEach(x => arrow(s, x, 2.5, x, 2.8, X.navy));
const sens = [['HS', 'R, FD, SD; REP, Dr, SDr; 48 indices (39 + 9 SWIR)'], ['MS', '5 bands; 12 indices; 40 GLCM'], ['RGB', '24 GLCM; HSV; vegetation fraction; colour'], ['TIR', 'CT, CTD, CTR, NRCT, MTD; 8 GLCM']];
sens.forEach((t, i) => { const x = 0.45 + i * 2.35; box(s, x, 3.6, 2.2, 0.75, [{ text: t[0] + ' features', options: { bold: true, breakLine: true } }, { text: t[1], options: { fontSize: 9.5 } }], { fill: X.lo1, line: X.o1, fs: 11 }); arrow(s, x + 1.1, 3.3, x + 1.1, 3.6, X.o1); });
const tiers = [['HS Tier 2', 'Scalogram + ReliefF'], ['HS Tier 3', 'White Rust Index'], ['Tier M1', 'ANOVA, Tukey, r'], ['Tier M2 + M3', 'VIF + stepwise CDA'], ['Tier M4', 'Boruta']];
tiers.forEach((t, i) => { const x = 0.45 + i * 1.88; box(s, x, 4.7, 1.75, 0.72, [{ text: t[0], options: { bold: true, breakLine: true } }, { text: t[1] }], { fill: X.o1, line: X.o1, color: 'FFFFFF', fs: 10.5 }); if (i < 4) arrow(s, x + 1.75, 5.06, x + 1.88, 5.06, X.o1); });
arrow(s, 4.95, 4.35, 4.95, 4.7, X.o1);
box(s, 0.45, 5.75, 9.25, 0.55, 'Outputs: disease-sensitive bands, White Rust Index, responding features, grade separability, DSF pools (classification and regression) per sensor', { fill: X.out, line: X.gold, fs: 11.5, bold: true });
arrow(s, 5.1, 5.42, 5.1, 5.75, X.gold);
hbox(s, 9.95, 1.4, 2.93, 4.9, 'Glasshouse–field link (A1.7)', ['Correlate features with RWC, chlorophyll, carotenoid, anthocyanin, protein, Pn, gs', 'Feature trajectories over DAI (treatment × DAI ANOVA)', 'Compare DSF lists: leaf (ASD) → pot (imaging) → canopy (UAV)', 'Resample HS to MS bands (spectral response functions) to test transfer'], X.glass, X.lglass, { fs: 11 });
arrow(s, 9.7, 3.0, 9.95, 3.0, X.glass);

s = slide('A1.4 Pre-processing of drone data');
const pp = [['Radiometric calibration', 'Reflectance panels / empirical line; DLS for MS; ASD panel check', 'Smith and Milton, 1999'], ['Orthomosaic and geometry', 'Structure-from-motion mosaics; HS cubes georectified with IMU/GNSS', 'Guo et al., 2021'],
  ['Co-registration', 'Same ground control points; nearest-neighbour resampling to a common grid', 'Guo et al., 2021'], ['Thermal correction', 'Emissivity 0.98, air temperature and RH; CTD = CT − Tair', 'Jones, 2014'],
  ['Crop mask', 'NDVI (R898, R684) > 0.6 × SAM mustard class (0.3 rad) on HS; erosion; transferred to all sensors', 'Kruse et al., 1993'], ['Flower removal', 'Yellow-flower pixels removed from the leaf spectrum; flower fraction kept as covariate', 'Sulik and Long, 2016'],
  ['HS plot spectrum', 'Endmember extraction per plot (SMACC in ENVI); non-crop endmembers removed; crop endmembers averaged', 'Gruninger et al., 2004'], ['Spectral smoothing', '613 → 483 bands (water/noisy bands removed); Savitzky–Golay (width 5, order 2); derivatives', 'Savitzky and Golay, 1964']];
pp.forEach((p, i) => { const col = i % 2, row = Math.floor(i / 2), x = 0.45 + col * 6.3, y = 1.2 + row * 1.2;
  box(s, x, y, 0.45, 1.0, String(i + 1), { fill: X.field, line: X.field, color: 'FFFFFF', bold: true, fs: 16 });
  box(s, x + 0.5, y, 5.6, 1.0, [{ text: p[0], options: { bold: true, color: X.field, breakLine: true } }, { text: p[1], options: { breakLine: true } }, { text: p[2], options: { italic: true, color: X.grey, fontSize: 10 } }], { fill: X.lfield, line: X.field, fs: 11.5, align: 'left', margin: 5 });
  if (i < 7 && col === 0) arrow(s, x + 6.1, y + 0.5, x + 6.3, y + 0.5, X.field); });
txt(s, 'Steps run in numbered order (left to right, top to bottom); every sensor is brought to the same grid and mask before features are extracted.', { x: 0.45, y: 6.1, w: 12.43, h: 0.4, fontSize: 12, italic: true, color: X.grey });

s = slide('A1.4 Pre-processing of glasshouse data');
const gp = [['Imaging set-up', 'Fixed camera height and geometry; same time of day; halogen / uniform illumination for HSI; white and dark reference every session'], ['Reflectance and temperature', 'Reflectance = (raw − dark)/(white − dark); thermal with reference surface, air temperature and RH logged'],
  ['Segmentation', 'Plant vs background by NDVI / excess-green and Otsu threshold; leaf masks for tagged leaves'], ['Symptom masks', 'Pustule (white) and chlorotic pixels classified within leaves → symptom fraction (image-based severity)'],
  ['ASD leaf spectra', 'Contact probe with own light source; splice correction; Savitzky–Golay smoothing; water bands kept (no atmospheric path)'], ['Pot / leaf features', 'Same feature definitions as the drone data → directly comparable feature tables']];
gp.forEach((p, i) => { const y = 1.2 + i * 0.82; box(s, 0.45, y, 0.45, 0.68, String(i + 1), { fill: X.glass, line: X.glass, color: 'FFFFFF', bold: true, fs: 15 });
  box(s, 0.95, y, 7.4, 0.68, [{ text: p[0] + ': ', options: { bold: true, color: X.glass } }, { text: p[1] }], { fill: X.lglass, line: X.glass, fs: 11.5, align: 'left', margin: 5 }); if (i < 5) arrow(s, 0.67, y + 0.68, 0.67, y + 0.82, X.glass); });
hbox(s, 8.6, 1.2, 4.28, 4.85, 'Why the glasshouse data matter', ['Infection time known exactly → true pre-symptomatic samples', 'No soil, shadow, wind; one leaf can be followed over time', 'Physiology and spectra from the same leaf', 'Image-based symptom fraction gives an objective severity reference for visual grades'], X.glass, X.lglass, { fs: 12.5 });
refl(s, 'Woebbecke et al., 1995; Otsu, 1979; Hueni and Bialek, 2017; Savitzky and Golay, 1964.');

s = slide('A1.5 Feature extraction per sensor');
table(s, [['Sensor', 'Features', 'Number', 'Reference'], ['Hyperspectral', 'Reflectance (R), first and second derivatives (FD, SD); REP, Dr, SDr; 39 indices (pigment, structure, water, disease) + 9 SWIR disease/water indices (DWSI, NDWI, MSI, NDII, RBI)', '≈ 1500', 'Horler et al., 1983; Apan et al., 2004; Gao, 1996'],
  ['Multispectral', '5 band reflectances; 12 indices (NDVI, GNDVI, NDRE, CIgreen, CIrededge, MTCI, TCARI/OSAVI, PSRI, …); GLCM texture of each band', '57', 'Rouse et al., 1974; Gitelson et al., 2003'],
  ['RGB', 'GLCM texture (mean, variance, homogeneity, contrast, dissimilarity, entropy, second moment, correlation; 4 directions averaged); HSV; vegetation fraction; colour indices', '29', 'Haralick et al., 1973; Woebbecke et al., 1995'],
  ['Thermal', 'Canopy temperature (CT), CTD = CT − Tair, CTR = CT/Tair, NRCT = (CT − CTmin)/(CTmax − CTmin), MTD; GLCM texture', '13', 'Elsayed et al., 2017; Idso et al., 1981'],
  ['ASD (point)', 'Same hyperspectral features on leaf (glasshouse, field) and canopy spectra; reference for UAV HS', '≈ 1500', 'Hueni and Bialek, 2017']],
  { x: 0.45, y: 1.2, w: 12.43, colW: [1.6, 6.6, 1.0, 3.23], fontSize: 12, rowH: 0.82 });
banner(s, 'Features are computed on plot spectra (field), pot and leaf spectra (glasshouse) with identical definitions, so glasshouse and drone results can be compared directly.', X.gold, X.out, 6.0, 0.55);

s = slide('A1.6 Hyperspectral tiers: from bands to disease-specific features');
const ht = [['Tier 1', 'Features', 'R, FD, SD at all bands; red-edge parameters; 48 indices', 'Horler et al., 1983'], ['Tier 2', 'Correlation scalogram + ReliefF', 'r with PDI (p < 0.01, top 5%) and ReliefF on six grades (k = 10); one band per correlated region (r ≥ 0.95); robust / regression / classification lists', 'Shukla et al., 2024; Robnik-Šikonja and Kononenko, 2003'],
  ['Tier 3', 'White Rust Index', 'ND(λ1, λ2) + w·R(λ3); 6 nm bands ≥ 50 nm apart; VNIR, SWIR and whole range; balanced accuracy', 'Mahlein et al., 2013'], ['Tier 4 (M1)', 'Univariate response', 'One-way ANOVA + Tukey HSD across grades; Pearson r with PDI', 'Tukey, 1949'],
  ['Tier 5 (M2 + M3)', 'VIF + stepwise CDA', 'VIF < 10; two-step stepwise canonical discriminant analysis (bands, then indices + WRI); canonical r, score plot, LORO accuracy', 'Dormann et al., 2013; Bhattacharya and Chattopadhyay, 2013'],
  ['Tier 6 (M4)', 'Boruta', 'All-relevant selection vs shadow features → DSF pools for classification and regression', 'Kursa and Rudnicki, 2010']];
ht.forEach((t, i) => { const y = 1.2 + i * 0.85; box(s, 0.45, y, 1.55, 0.72, t[0], { fill: X.o1, line: X.o1, color: 'FFFFFF', bold: true, fs: 12 });
  box(s, 2.05, y, 2.4, 0.72, t[1], { fill: X.lo1, line: X.o1, bold: true, fs: 12, color: X.navy });
  box(s, 4.5, y, 5.6, 0.72, t[2], { fill: 'FFFFFF', line: X.o1, fs: 10.5, align: 'left', margin: 5 }); box(s, 10.15, y, 2.73, 0.72, t[3], { fill: 'FFFFFF', line: 'C9CED6', fs: 10, align: 'left', color: X.grey, margin: 5 });
  if (i < 5) arrow(s, 1.22, y + 0.72, 1.22, y + 0.85, X.o1); });
banner(s, 'Applied to UAV HS plot spectra and to glasshouse HSI / ASD spectra; outputs compared between platforms.', X.gold, X.out, 6.35, 0.38);

s = slide('A1.6 Multispectral, RGB and thermal tiers; cross-sensor tier');
['MS', 'RGB', 'TIR'].forEach((t, j) => { const x = 0.45 + j * 3.05;
  box(s, x, 1.2, 2.85, 0.45, t + ' tiers', { fill: [X.field, X.glass, X.o3][j], line: [X.field, X.glass, X.o3][j], color: 'FFFFFF', bold: true, fs: 13 });
  [['Tier 1', 'Features (bands, indices, GLCM, thermal)'], ['Tier 2 (M1)', 'ANOVA + Tukey; r with PDI'], ['Tier 3 (M2 + M3)', 'VIF + one-step stepwise CDA'], ['Tier 4 (M4)', 'Boruta → DSF pool']].forEach((q, i) => { const y = 1.85 + i * 0.95;
    box(s, x, y, 2.85, 0.75, [{ text: q[0], options: { bold: true, breakLine: true } }, { text: q[1], options: { fontSize: 10.5 } }], { fill: X.lcom, line: X.navy, fs: 11.5 }); if (i < 3) arrow(s, x + 1.42, y + 0.75, x + 1.42, y + 0.95, X.navy); }); });
hbox(s, 9.6, 1.2, 3.28, 4.3, 'Cross-sensor tier', ['Correlation of DSFs across sensors (e.g. CTD vs water indices, RWC)', 'Optional combined CDA on CDA-selected features of all sensors', 'Identifies complementary vs redundant sensors before fusion'], X.navy, X.lcom, { fs: 12 });
banner(s, 'Output of Objective 1: per-sensor DSF pools (classification, regression), White Rust Index and the physiological meaning of each feature — inputs to Objectives 2 and 3.', X.gold, X.out, 5.75, 0.6);
refl(s, 'Tukey, 1949; Dormann et al., 2013; Kursa and Rudnicki, 2010; Feng et al., 2022; Liu et al., 2024.');

// =========================== OBJECTIVE 2 ===========================
section('Objective 2', 'To detect and discriminate disease severity of white rust in mustard through AI based multimodal data fusion');
s = slide('Objective 2: activities (drone field and glasshouse)');
table(s, [['Activity', 'Drone-based field', 'Glasshouse', 'Output'], ['2.1 Single-sensor models', 'S1 RGB, S2 MS, S3 HS, S4 TIR (plot level)', 'Same sensors at pot / leaf level', 'Accuracy per sensor'],
  ['2.2 Multi-sensor fusion', 'S5 RGB+TIR, S6 MS+TIR, S7 HS+TIR, S8 all; ML-SFFS feature fusion; DNN-F1, DNN-F2', 'Same combinations (controlled reference)', 'Best fusion set and model'],
  ['2.3 Severity mapping', 'Class, PDI and uncertainty maps; pixel-level encoder–decoder fusion', 'Pot-level severity images', 'Disease maps'], ['2.4 Transfer test', 'Field ↔ glasshouse feature/model transfer', 'Glasshouse models tested on field data', 'Robust features across scales'],
  ['2.5 Two-stage validation', 'IIRMR Bharatpur → farmers\' fields (2026-27)', '—', 'Independent accuracy']],
  { x: 0.45, y: 1.2, w: 12.43, colW: [2.4, 4.6, 3.0, 2.43], fontSize: 12, rowH: 0.75 });
banner(s, 'Tasks: six-grade classification (0, 1, 3, 5, 7, 9), healthy vs diseased detection and PDI regression; post-symptomatic samples.', X.o2, X.lo2, 5.95, 0.5);

s = slide('Objective 2: nested modelling flow chart');
box(s, 0.45, 1.2, 3.2, 0.75, 'DSF pools from Objective 1 (per sensor; classification and regression)', { fill: X.lo1, line: X.o1, fs: 11.5, bold: true });
box(s, 4.0, 1.2, 4.6, 0.75, 'Outer loop: leave-one-replication-out (test R1, R2 or R3 with their controls)', { fill: X.out, line: X.gold, fs: 11.5, bold: true });
arrow(s, 3.65, 1.57, 4.0, 1.57, X.grey);
s.addShape(pres.shapes.RECTANGLE, { x: 0.45, y: 2.2, w: 9.2, h: 3.35, fill: { type: 'none' }, line: { color: X.o2, width: 1.25, dashType: 'dash' } });
txt(s, 'Inside the two training replications only', { x: 0.55, y: 2.22, w: 5, h: 0.3, fontSize: 11, italic: true, color: X.o2, margin: 0 });
const o2s = [['VIF < 10', 'Remove collinear features', 'Dormann et al., 2013'], ['ML-SFFS', 'Optimum feature combination per model (≤ 10 features; inner grouped CV)', 'Pudil et al., 1994; Tian et al., 2021'], ['Tuning', 'Grid search of hyperparameters (inner CV)', 'Varma and Simon, 2006'], ['Train', 'Six models on the optimum features', 'Breiman, 2001; Cortes and Vapnik, 1995']];
o2s.forEach((o, i) => { const x = 0.65 + i * 2.25; box(s, x, 2.65, 2.05, 1.5, [{ text: o[0], options: { bold: true, fontSize: 13, breakLine: true } }, { text: o[1], options: { breakLine: true } }, { text: o[2], options: { italic: true, fontSize: 9, color: 'EDE2F6' } }], { fill: X.o2, line: X.o2, color: 'FFFFFF', fs: 10.5 }); if (i < 3) arrow(s, x + 2.05, 3.4, x + 2.25, 3.4, X.o2); });
box(s, 0.65, 4.4, 8.8, 0.95, [{ text: 'Sensor sets: ', options: { bold: true } }, { text: 'S1 RGB, S2 MS, S3 HS, S4 TIR, S5 RGB+TIR, S6 MS+TIR, S7 HS+TIR, S8 all four   ' }, { text: 'Models: ', options: { bold: true } }, { text: 'SVM/SVR, RF/RFR, k-NN, PLS-DA/PLSR, DNN-F1, DNN-F2' }], { fill: X.lo2, line: X.o2, fs: 11.5, align: 'left', margin: 6 });
arrow(s, 6.3, 1.95, 6.3, 2.2, X.gold);
box(s, 0.45, 5.8, 4.4, 0.7, 'Predict the held-out replication once → OA, kappa, macro-F1, ±1 grade; R², RMSE, RPD', { fill: X.out, line: X.gold, fs: 11, bold: true });
box(s, 5.05, 5.8, 4.6, 0.7, 'Best sensor set and model → maps → Bharatpur and farmers\' field validation', { fill: X.out, line: X.gold, fs: 11, bold: true });
arrow(s, 2.65, 5.55, 2.65, 5.8, X.gold); arrow(s, 4.85, 6.15, 5.05, 6.15, X.gold);
hbox(s, 9.95, 1.2, 2.93, 5.3, 'Why nested LORO', ['Plots of one replication share a block; testing on a whole replication mimics new plots (Roberts et al., 2017)', 'Feature selection and tuning on all data would inflate accuracy (Varma and Simon, 2006)', 'Leaves/pixels of one plot never split between training and test'], X.o2, X.lo2, { fs: 11.5 });

s = slide('Fusion strategies (Activity 2.2)');
const fz = [['Feature-level fusion (ML)', 'DSFs of the sensors joined → VIF → ML-SFFS → model; selected features show which sensor contributes', X.o2], ['DNN-F1: input fusion', 'All selected features joined at the input of one dense network', X.o2],
  ['DNN-F2: intermediate fusion', 'One sub-network per sensor; joined at an intermediate layer (Maimaitijiang et al., 2020)', X.o2], ['Pixel-level deep fusion', 'Sensor-specific encoders, multi-scale feature fusion, decoder → pixel-level severity map (Deng et al., 2024; Sun et al., 2019)', X.o2]];
fz.forEach((f, i) => { const x = 0.45 + i * 3.13; hbox(s, x, 1.2, 2.95, 2.4, f[0], f[1], f[2], X.lo2, { nobullet: true, fs: 12 }); });
{ const y0 = 4.0; ['RGB', 'MS', 'HS', 'TIR'].forEach((t, i) => { box(s, 0.6, y0 + i * 0.5, 1.1, 0.4, t, { fill: X.lcom, line: X.navy, fs: 11, bold: true }); arrow(s, 1.7, y0 + 0.2 + i * 0.5, 2.3, y0 + 0.95, X.grey); });
  box(s, 2.3, y0 + 0.6, 1.6, 0.7, 'Feature concat. + selection', { fill: X.lo2, line: X.o2, fs: 10.5 }); arrow(s, 3.9, y0 + 0.95, 4.3, y0 + 0.95, X.grey); box(s, 4.3, y0 + 0.6, 1.4, 0.7, 'ML / DNN-F1', { fill: X.o2, line: X.o2, color: 'FFFFFF', fs: 11, bold: true });
  ['RGB', 'MS', 'HS', 'TIR'].forEach((t, i) => { box(s, 6.6, y0 + i * 0.5, 0.9, 0.4, t, { fill: X.lcom, line: X.navy, fs: 11, bold: true }); box(s, 7.65, y0 + i * 0.5, 1.2, 0.4, 'sub-network', { fill: X.lo2, line: X.o2, fs: 10 }); arrow(s, 7.5, y0 + 0.2 + i * 0.5, 7.65, y0 + 0.2 + i * 0.5, X.grey); arrow(s, 8.85, y0 + 0.2 + i * 0.5, 9.4, y0 + 0.95, X.grey); });
  box(s, 9.4, y0 + 0.6, 1.4, 0.7, 'Joint layers (DNN-F2)', { fill: X.o2, line: X.o2, color: 'FFFFFF', fs: 10.5, bold: true }); arrow(s, 10.8, y0 + 0.95, 11.2, y0 + 0.95, X.grey); box(s, 11.2, y0 + 0.6, 1.65, 0.7, 'Grade / PDI', { fill: X.out, line: X.gold, fs: 11, bold: true });
  arrow(s, 5.0, y0 + 1.3, 5.0, y0 + 1.55, X.grey); box(s, 4.3, y0 + 1.55, 1.4, 0.4, 'Grade / PDI', { fill: X.out, line: X.gold, fs: 10.5, bold: true }); }
banner(s, 'Sensors are compared alone and in combination (S1–S8); the gain of fusion over the best single sensor is reported with the same nested validation.', X.o2, X.lo2, 6.2, 0.4);

s = slide('Models, tuning and evaluation (Activities 2.1–2.3)');
table(s, [['Model', 'Type', 'Tasks', 'Main hyperparameters', 'Reference'], ['SVM / SVR', 'Kernel', 'C, R', 'C, γ (RBF)', 'Cortes and Vapnik, 1995'], ['RF / RFR', 'Ensemble of trees', 'C, R', 'trees, mtry, min leaf', 'Breiman, 2001'], ['k-NN', 'Instance-based', 'C, R', 'k, distance weighting', 'Cover and Hart, 1967'],
  ['PLS-DA / PLSR', 'Latent variables', 'C, R', 'number of components', 'Wold et al., 2001'], ['DNN-F1', 'Deep, input fusion', 'C, R', 'layers, units, dropout', 'Maimaitijiang et al., 2020'], ['DNN-F2', 'Deep, intermediate fusion', 'C, R', 'sub-networks, dropout', 'Maimaitijiang et al., 2020']],
  { x: 0.45, y: 1.2, w: 7.6, colW: [1.45, 1.75, 0.7, 1.85, 1.85], fontSize: 11.5, rowH: 0.5, head: X.o2 });
hbox(s, 8.3, 1.2, 4.58, 3.6, 'Evaluation', [{ text: 'Classification: ', options: { bold: true } }, { text: 'overall accuracy, Cohen\'s kappa, per-grade precision, recall, F1, macro-F1, confusion matrix, ±1-grade accuracy, healthy vs diseased accuracy', options: { breakLine: true } },
  { text: 'Regression: ', options: { bold: true } }, { text: 'R², RMSE, NRMSE, RPD; observed vs predicted PDI', options: { breakLine: true } }, { text: 'Also: ', options: { bold: true } }, { text: 'accuracy per variety and date; grades from predicted PDI vs direct classification' }], X.o2, X.lo2, { fs: 12, nobullet: true });
hbox(s, 0.45, 4.95, 12.43, 1.2, 'Severity maps (Activity 2.3)', 'Best model applied to the masked orthomosaics → grade map, PDI map and uncertainty map per date; pixel-level encoder–decoder map compared with plot-level predictions', X.navy, X.lcom, { fs: 12, nobullet: true });
refl(s, 'Cohen, 1960; Sokolova and Lapalme, 2009; Liu et al., 2024; Deng et al., 2024.');

s = slide('Glasshouse–field transfer and two-stage validation (Activities 2.4–2.5)');
box(s, 0.45, 1.3, 3.0, 1.2, 'Glasshouse models and DSFs (pot / leaf scale)', { fill: X.lglass, line: X.glass, fs: 12.5, bold: true });
box(s, 0.45, 3.2, 3.0, 1.2, 'Drone field models (IARI, nested LORO)', { fill: X.lfield, line: X.field, fs: 12.5, bold: true });
box(s, 4.2, 2.25, 3.2, 1.2, 'Transfer test: common features; glasshouse model on field data and vice versa; spectral resampling to sensor bands', { fill: X.lcom, line: X.navy, fs: 11.5 });
arrow(s, 3.45, 1.9, 4.2, 2.6, X.glass); arrow(s, 3.45, 3.8, 4.2, 3.1, X.field);
box(s, 8.1, 1.3, 4.78, 1.2, 'Stage 1: IIRMR research farm, Bharatpur (local varieties, monitored ground truth)', { fill: X.out, line: X.gold, fs: 12, bold: true });
box(s, 8.1, 3.2, 4.78, 1.2, 'Stage 2: adjoining farmers\' fields (heterogeneous management and varieties)', { fill: X.out, line: X.gold, fs: 12, bold: true });
arrow(s, 7.4, 2.85, 8.1, 1.9, X.gold); arrow(s, 10.5, 2.5, 10.5, 3.2, X.gold);
bul(s, ['Best models applied without retraining; same flight protocol and ground scoring', 'Accuracy reported separately for each stage; drop in accuracy shows the transfer gap', 'Output: validated sensor/model combination and its expected accuracy in farmers\' fields'], { x: 0.45, y: 4.8, w: 12.43, h: 1.4, fontSize: 13.5 });

// =========================== OBJECTIVE 3 ===========================
section('Objective 3', 'To predict white rust at pre-symptomatic stage using machine learning technique(s)');
s = slide('Objective 3: activities and labels');
table(s, [['Activity', 'Drone-based field', 'Glasshouse'], ['3.1 Pre-symptomatic samples', 'Flights before first visible pustule; inoculated vs healthy plots of the same date', '1, 5, 9, 13 DAI images of inoculated and healthy pots (primary data)'],
  ['3.2 Labels', 'Retrospective: inoculated plots/leaves that later show symptoms = infected; healthy controls = healthy', 'Tagged leaves followed until symptoms appear → exact latent period'],
  ['3.3 Screening', 't-test and % difference from healthy; Boruta', 'Same + physiology (RWC, Pn, gs, pigments) changes before symptoms'], ['3.4 Models', 'VIF → ML-SFFS → SVM, RF, k-NN; S1–S8', 'Same; sensor ranking for earliest detection'],
  ['3.5 Earliest detection and risk maps', 'Accuracy vs DAI; pre-symptomatic risk maps', 'Earliest DAI with sensitivity > threshold']],
  { x: 0.45, y: 1.2, w: 12.43, colW: [2.6, 5.0, 4.83], fontSize: 12, rowH: 0.78, head: X.o3 });
banner(s, 'Inoculated plants that never develop symptoms (e.g. resistant variety) are excluded from the "infected" class to avoid wrong labels (Tian et al., 2021).', X.o3, X.lo3, 6.0, 0.5);

s = slide('Objective 3: flow chart');
legend(s, 7.6, 1.05);
hbox(s, 0.45, 1.4, 3.0, 1.2, 'Glasshouse 1–13 DAI', ['Inoculated + healthy pots', 'Tagged leaves'], X.glass, X.lglass, { fs: 11 });
hbox(s, 0.45, 2.9, 3.0, 1.2, 'Drone field before symptoms', ['Inoculated + healthy plots', 'Same dates'], X.field, X.lfield, { fs: 11 });
box(s, 3.8, 2.1, 2.6, 1.3, 'Retrospective labels: healthy vs infected (pre-symptomatic)', { fill: X.lo3, line: X.o3, fs: 12, bold: true });
arrow(s, 3.45, 2.0, 3.8, 2.5, X.glass); arrow(s, 3.45, 3.5, 3.8, 3.0, X.field);
const o3s = [['Screening', 't-test, % difference, Boruta'], ['VIF + ML-SFFS', 'Optimum features per sensor set'], ['Models', 'SVM, RF, k-NN (S1–S8)']];
o3s.forEach((o, i) => { const x = 6.75 + i * 2.1; box(s, x, 2.1, 1.9, 1.3, [{ text: o[0], options: { bold: true, breakLine: true, fontSize: 13 } }, { text: o[1] }], { fill: X.o3, line: X.o3, color: 'FFFFFF', fs: 11 }); arrow(s, x - 0.35 + (i === 0 ? 0 : 0.15), 2.75, x, 2.75, X.o3); });
box(s, 0.45, 4.5, 4.0, 1.3, 'Evaluation: sensitivity, specificity, balanced accuracy, AUC (nested LORO)', { fill: X.out, line: X.gold, fs: 12, bold: true });
box(s, 4.67, 4.5, 4.0, 1.3, 'Earliest detection day: accuracy vs DAI per sensor set; link with physiology changes', { fill: X.out, line: X.gold, fs: 12, bold: true });
box(s, 8.88, 4.5, 4.0, 1.3, 'Pre-symptomatic risk maps; validation in Bharatpur / farmers\' fields; early warning', { fill: X.out, line: X.gold, fs: 12, bold: true });
poly(s, [[11.8, 3.4], [11.8, 3.95], [2.45, 3.95], [2.45, 4.5]], X.gold); arrow(s, 6.67, 3.95, 6.67, 4.5, X.gold); arrow(s, 10.88, 3.95, 10.88, 4.5, X.gold);
refl(s, 'Tian et al., 2021; Zhu et al., 2017; Mahlein et al., 2019; Yu et al., 2025.');

// =========================== PROGRAMME ===========================
section('Programme of work', 'Timeline, expected outcomes and facilities');
s = slide('Programme of work (objective and activity wise)');
{ const months = ['Nov 25', 'Feb 26', 'May 26', 'Aug 26', 'Nov 26', 'Feb 27', 'May 27', 'Aug 27', 'Nov 27', 'Feb 28', 'May 28'];
  const x0 = 4.75, x1 = 11.9, mw = (x1 - x0) / 33; const mx = (y, m) => x0 + ((y - 2025) * 12 + (m - 11)) * mw;  // from Nov 2025
  months.forEach((m, i) => { txt(s, m, { x: x0 + i * 3 * mw - 0.3, y: 1.12, w: 0.65, h: 0.25, fontSize: 9, align: 'center', color: X.grey, margin: 0 }); s.addShape(pres.shapes.LINE, { x: x0 + i * 3 * mw, y: 1.38, w: 0.001, h: 5.15, line: { color: 'E3E7EE', width: 0.5 } }); });
  const rows = [['Obj 1', '1.1–1.3 Field (IARI) data 2025-26: sensors, physiology, scoring', [[2026, 1, 2026, 3]], X.o1, '18'], ['', '1.1–1.3 Field (IARI) + glasshouse data 2026-27', [[2026, 11, 2027, 3]], X.o1, ''], ['', '1.4–1.6 Pre-processing, features, tiers (DSF pools)', [[2026, 4, 2026, 9], [2027, 3, 2027, 6]], X.o1, '10'], ['', '1.7 Physiology and glasshouse–field links', [[2027, 3, 2027, 7]], X.o1, ''],
    ['Obj 2', '2.1 Single-sensor detection and severity', [[2026, 4, 2026, 9], [2027, 4, 2027, 7]], X.o2, '7'], ['', '2.2–2.3 Fusion models and severity maps', [[2026, 7, 2026, 12], [2027, 4, 2027, 8]], X.o2, '8'], ['', '2.4–2.5 Transfer test; Bharatpur and farmers\' field validation', [[2026, 10, 2027, 5]], X.o2, '15'],
    ['Obj 3', '3.1–3.5 Pre-symptomatic detection, earliest DAI, risk maps', [[2027, 4, 2027, 9]], X.o3, '6'], ['Output', 'Research papers 1 and 2', [[2027, 10, 2027, 12]], X.gold, '6'], ['', 'Thesis writing and submission', [[2028, 1, 2028, 6]], X.navy, '']];
  txt(s, 'Credits', { x: 12.1, y: 1.12, w: 0.8, h: 0.25, fontSize: 9, bold: true, align: 'center', margin: 0 });
  rows.forEach((r, i) => { const y = 1.45 + i * 0.505; txt(s, r[0], { x: 0.45, y, w: 0.75, h: 0.42, fontSize: 11, bold: true, color: r[3], valign: 'middle', margin: 0 });
    txt(s, r[1], { x: 1.2, y, w: 3.5, h: 0.42, fontSize: 10.5, valign: 'middle', margin: 0 });
    r[2].forEach(b => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: mx(b[0], b[1]), y: y + 0.08, w: mx(b[2], b[3]) - mx(b[0], b[1]) + mw, h: 0.28, fill: { color: r[3] }, line: { color: r[3] }, rectRadius: 0.05 }));
    txt(s, r[4], { x: 12.1, y, w: 0.8, h: 0.42, fontSize: 11, align: 'center', valign: 'middle', margin: 0 }); });
  const now = mx(2026, 11) + mw * 0.6; s.addShape(pres.shapes.LINE, { x: now, y: 1.38, w: 0.001, h: 5.15, line: { color: X.o3, width: 1.5, dashType: 'dash' } }); txt(s, 'now', { x: now - 0.3, y: 6.5, w: 0.6, h: 0.25, fontSize: 10, color: X.o3, bold: true, align: 'center', margin: 0 }); }
txt(s, 'Admission to Ph.D.: 19 February 2025. Credits as in the approved ORW (total 70).', { x: 0.45, y: 6.72, w: 9, h: 0.3, fontSize: 10.5, italic: true, color: X.grey, margin: 0 });

s = slide('Expected outcomes');
const eo = [['Disease signature', 'Sensitive bands, White Rust Index, texture and thermal features of white rust at leaf, pot and canopy scale, with their physiological meaning', X.o1, X.lo1], ['Best sensor and fusion model', 'The most suitable single sensor or sensor combination and AI model for detecting white rust and grading its severity, validated in new fields', X.o2, X.lo2],
  ['Early detection', 'Earliest day after infection at which white rust can be detected, and pre-symptomatic risk maps for timely management', X.o3, X.lo3], ['Transferable workflow', 'A documented, nested workflow from UAV images to severity maps that can be extended to satellite bands and other mustard diseases', X.field, X.lfield]];
eo.forEach((e, i) => { const x = 0.45 + (i % 2) * 6.3, y = 1.25 + Math.floor(i / 2) * 2.5; hbox(s, x, y, 6.13, 2.3, e[0], e[1], e[2], e[3], { nobullet: true, fs: 17, tfs: 15, th: 0.45 }); });
txt(s, 'Planned papers: (1) leaf-to-canopy characterisation of white rust and the White Rust Index; (2) multimodal UAV fusion for severity and pre-symptomatic detection.', { x: 0.45, y: 6.3, w: 12.43, h: 0.5, fontSize: 13, italic: true, color: X.navy });

s = slide('Facilities required and SDG relevance');
table(s, [['Facility', 'Division / institute'], ['ASD FieldSpec 4 spectroradiometer', 'Agricultural Physics, IARI'], ['UAV with RGB, multispectral, thermal and hyperspectral (Headwall) sensors', 'Agricultural Physics, IARI'], ['Computer with image and spectral analysis software', 'Agricultural Physics, IARI'],
  ['Canopy analyzer', 'Agricultural Physics, IARI'], ['LI-6400 portable gas exchange system', 'Plant Physiology, IARI'], ['Glasshouse and controlled-condition facility; inoculum', 'Plant Pathology, IARI'], ['Validation site', 'IIRMR, Bharatpur']], { x: 0.45, y: 1.2, w: 8.0, colW: [5.2, 2.8], fontSize: 12.5, rowH: 0.52 });
hbox(s, 8.7, 1.2, 4.18, 4.2, 'SDG theme areas', ['SDG 2: Zero hunger', 'SDG 9: Industry, innovation and infrastructure', 'Radioactivity involved: No'], X.field, X.lfield, { fs: 15 });

// =========================== REFERENCES ===========================
const R = REFS; const per = 16; for (let i = 0, j = 1; i < R.length; i += per, j++) {
  const s2 = slide('References (' + j + '/' + Math.ceil(R.length / per) + ')'); const part = R.slice(i, i + per); const h = Math.ceil(part.length / 2);
  [part.slice(0, h), part.slice(h)].forEach((col, c) => s2.addText(col.map((r, k) => ({ text: r, options: { breakLine: k < col.length - 1 } })), { isTextBox: true, x: 0.45 + c * 6.25, y: 1.15, w: 6.1, h: 5.85, fontSize: 10.5, color: X.text, valign: 'top', paraSpaceAfter: 3 })); }
s = pres.addSlide({ masterName: 'SECTION', sectionTitle: sec }); s.addText('Thank you', { placeholder: 'title' }); s.addText('Suggestions of the advisory committee are welcome', { placeholder: 'body' });
pres.writeFile({ fileName: OUT }).then(async () => { await applyTheme(OUT, THEME); console.log('saved', OUT); });
