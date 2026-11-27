const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType, ImageRun,
  TableOfContents, PageBreak, LevelFormat, Footer, PageNumber, BorderStyle } = require('docx');
const B = '/tmp/claude-0/-home-user-meta/c5704ca0-f1ca-5695-b9e0-a810fbe166a9/scratchpad/thesis/';
const OUT = '/tmp/claude-0/-home-user-meta/c5704ca0-f1ca-5695-b9e0-a810fbe166a9/scratchpad/outputs/White_rust_thesis_methodology_complete.docx';
const FONT = 'Calibri', EQF = 'Cambria Math';
// ---------- text helpers: _x / _{..} = subscript, ^x / ^{..} = superscript, **..** = bold ----------
function runs(text, base = {}) {
  const out = []; let i = 0, buf = '', bold = false;
  const flush = () => { if (buf) { out.push(new TextRun({ text: buf, font: base.font || FONT, size: base.size || 22, bold: bold || base.bold, italics: base.italics })); buf = ''; } };
  while (i < text.length) {
    const ch = text[i];
    if (text.startsWith('**', i)) { flush(); bold = !bold; i += 2; continue; }
    if (text.startsWith('\\_', i)) { buf += '_'; i += 2; continue; }
    if ((ch === '_' || ch === '^') && i + 1 < text.length && text[i + 1] !== ' ') {
      flush(); let s;
      if (text[i + 1] === '{') { const j = text.indexOf('}', i); s = text.slice(i + 2, j); i = j + 1; } else { s = text[i + 1]; i += 2; }
      out.push(new TextRun({ text: s, font: base.font || FONT, size: base.size || 22, bold: bold || base.bold, italics: base.italics, subScript: ch === '_', superScript: ch === '^' })); continue;
    }
    buf += ch; i++;
  }
  flush(); return out;
}
const P = (t, o = {}) => new Paragraph({ spacing: { after: 120, line: 290 }, alignment: AlignmentType.JUSTIFIED, ...o, children: runs(t) });
const EQ = (t, label) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 80, after: 120 }, children: [...runs(t, { font: EQF, size: 23 }), ...(label ? [new TextRun({ text: `        (${label})`, font: FONT, size: 20 })] : [])] });
const H1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: t, font: FONT })] });
const H2 = t => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: t, font: FONT })] });
const H3 = t => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun({ text: t, font: FONT })] });
const BL = (t, lvl = 0) => new Paragraph({ numbering: { reference: 'bul', level: lvl }, spacing: { after: 60, line: 280 }, children: runs(t) });
let LISTI = 0, lastNL = false;
const NL = (t, ref = 'num') => { if (!lastNL) LISTI++; lastNL = true; const p = new Paragraph({ numbering: { reference: 'num', level: 0, instance: LISTI }, spacing: { after: 60, line: 280 }, children: runs(t) }); p.__nl = true; return p; };
const NOTE = t => new Paragraph({ spacing: { before: 80, after: 140 }, shading: { type: ShadingType.CLEAR, color: 'auto', fill: 'EEF3E8' }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: '2C5F2D', space: 6 } },
  indent: { left: 200, right: 200 }, children: runs(t, { size: 21 }) });
let figN = 0, tabN = 0;
function fig(file, caption, w = 560) {
  const buf = fs.readFileSync(B + 'fig/' + file);
  const dim = require('child_process').execSync(`python3 -c "from PIL import Image;im=Image.open('${B}fig/${file}');print(im.size[0],im.size[1])"`).toString().trim().split(' ').map(Number);
  figN += 1;
  return [new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 120 }, children: [new ImageRun({ type: 'png', data: buf, transformation: { width: w, height: Math.round(w * dim[1] / dim[0]) }, altText: { title: caption, description: caption, name: file } })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [new TextRun({ text: `Figure ${figN}. `, bold: true, font: FONT, size: 19 }), ...runs(caption, { size: 19, italics: true })] })];
}
function table(rows, widths, caption, size = 19) {
  tabN += 1; const total = widths.reduce((a, b) => a + b, 0); const bd = { style: BorderStyle.SINGLE, size: 4, color: 'BBBBBB' };
  const mk = (r, head) => new TableRow({ tableHeader: head, cantSplit: true, children: r.map((c, j) => new TableCell({ width: { size: widths[j], type: WidthType.DXA }, borders: { top: bd, bottom: bd, left: bd, right: bd },
    shading: head ? { type: ShadingType.CLEAR, color: 'auto', fill: '2C5F2D' } : undefined, margins: { top: 50, bottom: 50, left: 90, right: 90 },
    children: [new Paragraph({ children: runs(String(c), { size, bold: head }).map(x => { if (head) x.root && 0; return x; }) })] })) });
  const headRow = new TableRow({ tableHeader: true, cantSplit: true, children: rows[0].map((c, j) => new TableCell({ width: { size: widths[j], type: WidthType.DXA }, borders: { top: bd, bottom: bd, left: bd, right: bd },
    shading: { type: ShadingType.CLEAR, color: 'auto', fill: '2C5F2D' }, margins: { top: 50, bottom: 50, left: 90, right: 90 },
    children: [new Paragraph({ children: [new TextRun({ text: String(c), font: FONT, size, bold: true, color: 'FFFFFF' })] })] })) });
  return [new Paragraph({ spacing: { before: 160, after: 80 }, keepNext: true, children: [new TextRun({ text: `Table ${tabN}. `, bold: true, font: FONT, size: 19 }), ...runs(caption, { size: 19, italics: true })] }),
    new Table({ width: { size: total, type: WidthType.DXA }, columnWidths: widths, rows: [headRow, ...rows.slice(1).map(r => mk(r, false))] }), new Paragraph({ spacing: { after: 120 }, children: [] })];
}
// White rust UAV multimodal methodology (body). Build: cat u4_head.js u4_body.js > u4_docx.js && node u4_docx.js
const hs = (size, color, before, after, italics = false, lvl = 0) => ({ run: { font: FONT, size, bold: true, color, italics }, paragraph: { spacing: { before, after }, keepNext: true, keepLines: true, outlineLevel: lvl } });
const K = [];
const _push = K.push.bind(K);
K.push = (...items) => { for (const it of items) { if (!(it && it.__nl)) lastNL = false; } return _push(...items); };
const FORDER = ['physics', 'symsensor', 'matrix', 'workflow', 'design', 'chains', 'obj1flow', 'step12', 'bandcorr', 'statstree', 'obj2flow', 'funnel', 'fusion', 'dnn', 'obj3flow', 'mloverview', 'mloverfit', 'glcm', 'mlborsffs', 'mlsvm', 'mlrf', 'mlknn', 'mldnn', 'mlfusion', 'mlnested', 'mlconfusion'];
const TORDER = ['abbrev', 'sensorroles', 'rqh', 'mustard', 'papers', 'lessons', 'extralit', 'objmap', 'tasks', 'dataset', 'sensors', 'hsfeat', 'hsidx', 'msidx', 'rgbfeat', 'tirfeat', 'consensus', 'mcol', 'statsdesign', 'stats', 'stage3', 'objsens', 'inputsets', 'hyper', 'models', 'metrics', 'runs', 'mlcomponents', 'mlscaling', 'mlsffsex', 'mlfscompare', 'mlsvmparams', 'mlrfparams', 'mlknnparams', 'mlplsparams', 'mldnnparams', 'mldnncount', 'mlfusioncmp', 'mlgrids', 'mlmetricex', 'mlkappascale', 'mlsoftware', 'mlmodelcmp', 'satisfy', 'limits', 'idxcorr', 'methcorr', 'corrections', 'simplify'];
const usedF = [], usedT = [];
const F = k => 'Figure ' + (FORDER.indexOf(k) + 1);
const T = k => 'Table ' + (TORDER.indexOf(k) + 1);
function fig2(k, file, cap, w) { usedF.push(k); return fig(file, cap, w); }
function tab2(k, rows, widths, cap, size) { usedT.push(k); return table(rows, widths, cap, size); }
const LBL = t => new Paragraph({ spacing: { before: 140, after: 60 }, keepNext: true, children: [new TextRun({ text: t, bold: true, font: FONT, size: 22, color: '2C5F2D' })] });
const BOX = (label, t, fill = 'FFF6E0', line = 'C98A00') => new Paragraph({ spacing: { before: 100, after: 160 }, shading: { type: ShadingType.CLEAR, color: 'auto', fill },
  border: { left: { style: BorderStyle.SINGLE, size: 18, color: line, space: 6 } }, indent: { left: 200, right: 200 },
  children: [new TextRun({ text: label + ' ', bold: true, font: FONT, size: 21 }), ...runs(t, { size: 21 })] });
// step block: title + What / Why / How
function STEP(title, what, why, how, ref) {
  const out = [new Paragraph({ spacing: { before: 160, after: 60 }, keepNext: true, children: [new TextRun({ text: title, bold: true, font: FONT, size: 22, color: '1E3A1F' })] })];
  out.push(new Paragraph({ spacing: { after: 60, line: 280 }, indent: { left: 300 }, children: [new TextRun({ text: 'What: ', bold: true, font: FONT, size: 21, color: '1565C0' }), ...runs(what, { size: 21 })] }));
  out.push(new Paragraph({ spacing: { after: 60, line: 280 }, indent: { left: 300 }, children: [new TextRun({ text: 'Why: ', bold: true, font: FONT, size: 21, color: 'AD1457' }), ...runs(why, { size: 21 })] }));
  if (Array.isArray(how)) {
    out.push(new Paragraph({ spacing: { after: 40, line: 280 }, indent: { left: 300 }, keepNext: true, children: [new TextRun({ text: 'How:', bold: true, font: FONT, size: 21, color: '2E7D32' })] }));
    how.forEach(h => out.push(BL(h, 1)));
  } else {
    out.push(new Paragraph({ spacing: { after: 60, line: 280 }, indent: { left: 300 }, children: [new TextRun({ text: 'How: ', bold: true, font: FONT, size: 21, color: '2E7D32' }), ...runs(how, { size: 21 })] }));
  }
  if (ref) out.push(new Paragraph({ spacing: { after: 120, line: 260 }, indent: { left: 300 }, children: [new TextRun({ text: 'Reference basis: ', bold: true, italics: true, font: FONT, size: 19, color: '555555' }), new TextRun({ text: ref, italics: true, font: FONT, size: 19, color: '555555' })] }));
  return out;
}

const NLc = t => NL(t, 'numc');
const NLr = t => NL(t, 'numr');
const NLm = t => NL(t, 'numm');
const NLt = t => NL(t, 'numt');
const NLg = t => NL(t, 'numg');
const KEY = (label, t) => BOX(label, t);
const INCASE = t => BOX('In my case:', t, 'E8F5E9', '2E7D32');
const SIMPLE = t => BOX('In simple words:', t, 'E3F2FD', '1565C0');
const STAGE = (title, concept, req, imp, mine, qs, outp, notes) => {
  const lab = (l, c, t) => new Paragraph({ spacing: { after: 60, line: 280 }, indent: { left: 300 }, children: [new TextRun({ text: l + ' ', bold: true, font: FONT, size: 21, color: c }), ...runs(t, { size: 21 })] });
  const out = [new Paragraph({ spacing: { before: 180, after: 60 }, keepNext: true, children: [new TextRun({ text: title, bold: true, font: FONT, size: 22, color: '1E3A1F' })] }),
    lab('Concept:', '1565C0', concept), lab('Why it is needed at this position:', 'AD1457', req), lab('Importance:', '6A1B9A', imp), lab('How it is used with my data:', '2E7D32', mine),
    ...STEPEND(outp, notes),
    new Paragraph({ spacing: { after: 40 }, indent: { left: 300 }, keepNext: true, children: [new TextRun({ text: 'Interview questions:', bold: true, font: FONT, size: 21, color: 'C98A00' })] })];
  qs.forEach(([q, a]) => { out.push(new Paragraph({ spacing: { after: 20, line: 270 }, indent: { left: 600 }, keepNext: true, children: [new TextRun({ text: 'Q. ' + q, bold: true, font: FONT, size: 20 })] }));
    out.push(new Paragraph({ spacing: { after: 70, line: 270 }, indent: { left: 600 }, children: runs('A. ' + a, { size: 20 }) })); });
  return out; };
function STEPEND(outp, notes) {
  const out = [BOX('Output of this step:', outp, 'F3E5F5', '6A1B9A')];
  out.push(new Paragraph({ spacing: { before: 60, after: 40 }, keepNext: true, shading: { type: ShadingType.CLEAR, color: 'auto', fill: 'FFF8E1' }, indent: { left: 200, right: 200 }, border: { left: { style: BorderStyle.SINGLE, size: 18, color: 'C98A00', space: 6 } }, children: [new TextRun({ text: 'Notes – other methods and approaches:', bold: true, font: FONT, size: 21 })] }));
  notes.forEach(n => out.push(new Paragraph({ numbering: { reference: 'bul', level: 0 }, spacing: { after: 40, line: 270 }, shading: { type: ShadingType.CLEAR, color: 'auto', fill: 'FFF8E1' }, children: runs(n, { size: 20 }) })));
  out.push(new Paragraph({ spacing: { after: 100 }, children: [] }));
  return out; }
const QA3 = (q, ans, mine, others) => { K.push(new Paragraph({ spacing: { before: 140, after: 50 }, keepNext: true, children: [new TextRun({ text: 'Q. ' + q, bold: true, font: FONT, size: 21, color: '1E3A1F' })] }));
  const lab = (l, c, t, kn) => new Paragraph({ spacing: { after: 60, line: 280 }, indent: { left: 300 }, keepNext: kn, alignment: AlignmentType.JUSTIFIED, children: [new TextRun({ text: l + ' ', bold: true, font: FONT, size: 21, color: c }), ...runs(t, { size: 21 })] });
  K.push(lab('Answer:', '1565C0', ans, true)); K.push(lab('How I solved it:', '2E7D32', mine, false)); K.push(lab('How other researchers dealt with it:', 'AD1457', others, false)); };
const QA = (q, a) => { K.push(new Paragraph({ spacing: { before: 110, after: 40 }, keepNext: true, children: [new TextRun({ text: 'Q. ' + q, bold: true, font: FONT, size: 21, color: '1E3A1F' })] })); K.push(P('A. ' + a)); };

// ======================= TITLE =======================
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 900, after: 160 }, children: [new TextRun({ text: 'AI-based multimodal UAV sensing of white rust in mustard', font: FONT, size: 44, bold: true, color: '1E3A1F' })] }));
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: 'Complete research methodology, algorithms and interview preparation (thesis edition)', font: FONT, size: 28, color: '2C5F2D' })] }));
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: [new TextRun({ text: 'Ph.D. (Agricultural Physics), ICAR-Indian Agricultural Research Institute, New Delhi', font: FONT, size: 22, italics: true, color: '555555' })] }));
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 500 }, children: [new TextRun({ text: 'UAV RGB, multispectral, hyperspectral and thermal sensing  |  detection, severity discrimination and pre-symptomatic prediction  |  ML-SFFS and deep-learning feature-level fusion', font: FONT, size: 20, italics: true, color: '555555' })] }));
K.push(NOTE(`**How to read this document.** Chapters 1 and 2 give the background and the literature on which every decision rests. Chapter 3 describes the experiment, ground truth and sensor pre-processing. Chapters 4, 5 and 6 give the step-by-step methodology of Objectives 1, 2 and 3; every step has a flow chart, a **What / Why / How** block, a reference basis and an **In my case** box that explains exactly what happens with the white rust data. Chapter 7 gives the validation design. Chapter 8 explains every algorithm (statistics, feature selection, machine learning, deep learning, fusion, validation, metrics) from first principles, with equations, hyperparameters and a worked example for this thesis. Chapter 9 summarises outputs, novelty, limitations and relevance to ISRO; Chapter 10 lists corrections to the ORW; Chapter 11 collects about 100 interview questions with short answers, and Chapter 12 gives NRSC/SAC (ISRO) interview questions, each answered with the concept, how this thesis solves the problem and how other researchers dealt with it.`));
K.push(KEY('Key messages in one paragraph.', `White rust (Albugo candida) changes leaf pigments, structure, water status, transpiration and canopy pattern. Each UAV sensor sees part of this: RGB sees colour and texture, multispectral (MS) sees broad-band pigment and red-edge change, hyperspectral (HS) sees narrow pigment and water features (400–2500 nm), and thermal (TIR) sees warming caused by disturbed transpiration. **Objective 1** finds, for each sensor, the disease-specific features (DSFs) for detection, severity discrimination (Low ≤ 25%, Moderate 25–50%, High > 50% disease index) and disease-index (DI) regression, using statistics, correlation scalograms, ReliefF, a White Rust Index and Boruta. **Objective 2** reduces each DSF pool with VIF and ML-SFFS and compares six models (SVM/SVR, RF/RFR, k-NN, PLSR, DNN-F1, DNN-F2) on each sensor and on four sensor combinations with four fusion strategies. **Objective 3** tests whether inoculated plots can be separated from healthy plots before symptoms appear. All dates are pooled, every split keeps a plot's observations together (leave-one-replication-out cross-validation), and the final models are tested at Bharatpur and in farmers' fields.`));
K.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-2' }));
K.push(new Paragraph({ children: [new PageBreak()] }));
K.push(H1('Abbreviations'));
K.push(...tab2('abbrev', [
  ['Abbreviation', 'Meaning', 'Abbreviation', 'Meaning'],
  ['ANOVA', 'Analysis of variance', 'MS', 'Multispectral (MicaSense RedEdge-MX)'],
  ['CT, CTD', 'Canopy temperature; canopy–air temperature difference', 'MTD', 'Maximum temperature difference within the canopy'],
  ['CV', 'Cross-validation', 'NIR', 'Near infrared (750–1000 nm)'],
  ['DI', 'Disease index (%)', 'NRCT', 'Normalised relative canopy temperature'],
  ['DNN-F1, DNN-F2', 'Deep neural network with input-level / intermediate-level fusion', 'OA', 'Overall accuracy'],
  ['DSF', 'Disease-specific feature', 'OFC', 'Optimum feature combination (output of ML-SFFS)'],
  ['FD, SD', 'First and second derivative of reflectance', 'PLSR', 'Partial least squares regression'],
  ['GLCM', 'Grey-level co-occurrence matrix (texture)', 'RBD', 'Randomised block design'],
  ['HS', 'Hyperspectral (VNIR 400–1000 nm + SWIR 1000–2500 nm)', 'RF, RFR', 'Random forest classification, regression'],
  ['JM', 'Jeffries–Matusita distance', 'RGB', 'Red–green–blue camera'],
  ['k-NN', 'k-nearest neighbours', 'SFFS', 'Sequential floating forward selection'],
  ['LORO', 'Leave-one-replication-out (cross-validation)', 'SVM, SVR', 'Support vector machine, regression'],
  ['ML-SFFS', 'SFFS with a machine-learning model as the criterion', 'SWIR', 'Short-wave infrared (1000–2500 nm)'],
  ['macro-F1', 'Mean of per-class F1 scores', 'TIR', 'Thermal infrared camera (7.5–13.5 µm)'],
  ['REP', 'Red-edge position', 'VIF', 'Variance inflation factor'],
  ['RMSE, NRMSE', 'Root mean square error; normalised RMSE', 'WRI', 'White Rust Index'],
], [1500, 3150, 1500, 3156], 'Abbreviations used in this document.', 16));
K.push(new Paragraph({ children: [new PageBreak()] }));

// ======================= CHAPTER 1 INTRODUCTION =======================
K.push(H1('1. Introduction'));
K.push(H2('1.1 Indian mustard and white rust'));
K.push(P(`Indian mustard (Brassica juncea) is the main rabi oilseed crop of India and is grown mostly in Rajasthan, Uttar Pradesh, Haryana, Madhya Pradesh and West Bengal. Among its diseases, **white rust**, caused by the obligate biotrophic oomycete **Albugo candida**, is one of the most damaging; the ORW cites yield losses of 20–60% in India. The pathogen survives between seasons as thick-walled **oospores** in soil, crop debris and seed. Under cool (roughly 10–20 °C), humid weather with free moisture on the leaves, oospores and zoosporangia release motile **zoospores** that enter the leaf through stomata. Mycelium grows between the cells and forms chains of **zoosporangia** under the epidermis, which ruptures to expose white to creamy-yellow **pustules**; wind and rain spread the zoosporangia and start secondary cycles (Saharan et al., 2014).`));
K.push(P(`Two kinds of infection matter for sensing. **Local infection** produces pustules on leaves and stems, with chlorosis around them. **Systemic infection** of the inflorescence causes hypertrophy and hyperplasia of the floral parts, which become swollen and distorted ("**staghead**"), and often carries oospores to the next season. The disease therefore changes the canopy in several physically different ways — colour, pigment content, tissue structure, water status, transpiration and canopy architecture — and these changes develop over weeks, from invisible early infection to severe pustule cover and stagheads.`));
K.push(H2('1.2 Why sensor-based assessment'));
K.push(P(`Disease is normally assessed by visual scoring of leaves on a 0–6 or 0–9 scale. Visual scoring is slow, needs trained staff, varies between observers and can only be done on a few plants per plot. It also sees the disease only after symptoms appear, when the pathogen is already established. Optical and thermal sensors measure the canopy objectively, cover every plant of a plot, can be repeated at short intervals and can detect physiological changes that precede visible symptoms (West et al., 2003; Mahlein, 2016). Combined with machine learning, sensor data can be turned into maps of disease presence, severity and risk that support site-specific protection and can later be scaled up to satellite data.`));
K.push(H2('1.3 Physical basis of sensing white rust'));
K.push(H3('1.3.1 Reflectance (RGB, multispectral and hyperspectral sensors)'));
K.push(P(`Reflectance is the fraction of incoming solar radiation that the canopy reflects at each wavelength. A healthy green canopy has a characteristic signature (${F('physics')}): low reflectance in the blue (around 450 nm) and red (around 670 nm) because chlorophyll absorbs there; a small green peak near 550 nm; a steep rise between about 680 and 750 nm, the **red edge**; a high **near-infrared (NIR) plateau** (750–1300 nm) caused by multiple scattering at the air–cell interfaces of the leaf mesophyll; and in the **short-wave infrared (SWIR)** a series of water absorption features near 970, 1200, 1450 and 1940 nm, separated by reflectance peaks near 1650 and 2200 nm (Curran, 1989; Carter and Knapp, 2001).`));
K.push(P(`White rust changes every part of this signature. Chlorophyll loss around pustules weakens the red absorption and raises visible reflectance, and the white pustules themselves are bright at all visible wavelengths. As chlorophyll declines, the red edge moves to shorter wavelengths (a "blue shift"; Horler et al., 1983) and its slope decreases. Damage to mesophyll cells reduces NIR scattering. Water loss in infected tissue weakens SWIR water absorption, raising SWIR reflectance (Bhattacharya and Chattopadhyay, 2013). Changes in carotenoids and anthocyanins alter the 500–550 nm region used by PRI, PSRI and ARI. Because pustules occur as small bright spots on a green background, the disease also changes the **spatial pattern** of the canopy, which texture measures capture (Guo et al., 2021).`));
K.push(...fig2('physics', 'n1_physics.png', 'Schematic canopy reflectance of healthy and white-rust infected mustard, with the spectral regions covered by each sensor. Grey bands (1350–1450 and 1800–1950 nm) are strongly absorbed by atmospheric water vapour and are removed from UAV hyperspectral data.', 560));
K.push(H3('1.3.2 Thermal emission (thermal camera)'));
K.push(P(`Every surface emits thermal radiation according to its temperature and emissivity. The thermal camera measures emitted radiance in the 7.5–13.5 µm window and converts it to temperature using the Stefan–Boltzmann law, corrected for emissivity (about 0.98 for leaves), reflected sky radiation, air temperature, humidity and distance:`));
K.push(EQ('M = ε σ T^{4},     σ = 5.67 × 10^{−8} W m^{−2} K^{−4}', '1.1'));
K.push(P(`Canopy temperature is controlled by the surface energy balance. Net radiation R_{n}, minus soil heat flux G, is shared between sensible heat H (warming the air) and latent heat λE (evaporating water through stomata):`));
K.push(EQ('R_{n} − G = H + λE', '1.2'));
K.push(P(`When stomata are open, transpiration (λE) consumes energy and cools the leaves. Infection disturbs stomatal regulation and damages tissue, so transpiration falls and more energy goes into H: the canopy becomes warmer than a healthy canopy under the same weather (Jones, 2014; Mahlein et al., 2019). Because air temperature differs between flights, normalised indices such as the canopy–air temperature difference (CTD) and the normalised relative canopy temperature (NRCT) are used rather than raw canopy temperature (Feng et al., 2022). Water deficit also warms the canopy, so thermal signals are interpreted together with a water index and the uniform irrigation of the experiment (Bhattacharya and Chattopadhyay, 2013).`));
K.push(H3('1.3.3 Colour, texture and structure (RGB camera)'));
K.push(P(`The RGB camera has the finest pixel size. It records colour (pustules are white, chlorotic tissue yellow) and the spatial arrangement of pixels. Grey-level co-occurrence matrix (GLCM) texture measures quantify how uniform or patchy the canopy is (Haralick et al., 1973): pustules and lesions increase contrast, dissimilarity and entropy and decrease homogeneity. Photogrammetric surface models give canopy height and vegetation fraction, which change when stagheads deform the inflorescence or the canopy thins (Maimaitijiang et al., 2020). ${F('symsensor')} links each symptom to the plant change it causes and to the sensor feature that records it.`));
K.push(...fig2('symsensor', 'n2_symptom_sensor.png', 'From white rust symptom to plant change to sensor feature. No single sensor records every change, which is the physical reason for multimodal fusion.', 560));
K.push(H2('1.4 Why a UAV and why four sensors'));
K.push(P(`Satellites cover large areas but their pixels (10–30 m for most optical sensors) are larger than an experimental plot (3 m × 3 m) and their revisit is limited by orbit and clouds. Ground spectroradiometers are precise but measure only a small spot. A UAV fills the gap: centimetre-to-decimetre pixels, flights on demand between 11:00 and 14:00 h, and the same plots measured by several sensors on the same day. The four sensors are complementary (${T('sensorroles')}): each measures a different physical quantity, and the thesis asks which of them, alone or combined, detects white rust and discriminates its severity best.`));
K.push(...tab2('sensorroles', [
  ['Sensor', 'Physical quantity', 'Strength for white rust', 'Limitation'],
  ['RGB (DJI Phantom, 5472 × 3648 pixels)', 'Visible radiance in three broad bands', 'Finest pixels: pustule texture, colour, canopy cover and height', 'No NIR or SWIR; colour depends on illumination'],
  ['Multispectral (MicaSense RedEdge-MX: 475, 560, 668, 717, 840 nm)', 'Calibrated reflectance in five bands', 'Red-edge and NIR indices; low cost; operational', 'Broad bands miss narrow features'],
  ['Hyperspectral (VNIR 400–1000 nm, SWIR 1000–2500 nm; 481 bands used)', 'Narrow-band reflectance spectrum', 'Pigment, structure and water features; disease-specific index', 'Large data volume; coarse SWIR pixels (about 36 cm)'],
  ['Thermal (FLIR Vue Pro R, 7.5–13.5 µm)', 'Canopy temperature', 'Detects disturbed transpiration, possibly before visible symptoms', 'Affected by weather; needs normalisation'],
], [2300, 2000, 2700, 2306], 'Roles of the four UAV sensors.', 16));
K.push(H2('1.5 Research questions and hypotheses'));
K.push(P('The thesis is built around four research questions (RQ) and the hypotheses (H) that the methodology tests:'));
K.push(...tab2('rqh', [
  ['Research question', 'Hypothesis', 'Tested in'],
  ['RQ1. Which features of each UAV sensor respond to white rust, and to its severity, and why?', 'H1. White rust causes sensor-specific changes — pigment and red-edge (MS, HS), NIR structure and SWIR water (HS), warming (TIR) and texture (RGB) — that differ between Low, Moderate and High severity and correlate with physiological measurements.', 'Objective 1 (Chapter 4)'],
  ['RQ2. Which sensor, sensor combination, fusion strategy and model detect white rust and discriminate its severity best?', 'H2. Because the sensors measure different properties, feature-level fusion improves detection, three-class severity discrimination and DI estimation over the best single sensor; HS + TIR is expected to be the strongest pair (Mahlein et al., 2019).', 'Objective 2 (Chapter 5)'],
  ['RQ3. Can white rust be predicted before visible symptoms?', 'H3. Infection changes transpiration and pigments before pustules appear, so thermal and hyperspectral features separate later-infected from healthy plots before symptoms (Tian et al., 2021; Mustafa et al., 2023).', 'Objective 3 (Chapter 6)'],
  ['RQ4. Do the models work for other varieties, sites and farmers\' fields?', 'H4. Models built on features selected inside training folds and validated on unseen replications transfer to an independent site, although some loss of accuracy is expected (Bohnenkamp et al., 2019; Feng et al., 2022).', 'Validation (Chapter 7)'],
], [2900, 4500, 1906], 'Research questions and hypotheses.', 16));
K.push(H2('1.6 Objectives'));

K.push(P('The three objectives of the thesis (ORW, item 12) and the tasks addressed in each are:'));
K.push(NL('**Objective 1. To characterise white rust of mustard through multimodal sensing from a UAV platform.** For each sensor: which features change with disease (detection) and with severity (severity discrimination), and which plant property explains the change.'));
K.push(NL('**Objective 2. To detect and discriminate disease severity of white rust through AI-based multimodal data fusion.** Post-symptomatic classification (healthy vs diseased; three severity classes) and regression of the disease index, for each sensor and for fused sensors.'));
K.push(NL('**Objective 3. To predict white rust at the pre-symptomatic stage using machine learning.** Classification of healthy vs later-infected plots before symptoms, for each sensor and for fused sensors.'));
K.push(H2('1.7 Scope'));
K.push(P(`The methodology uses only the four UAV datasets (RGB, MS, HS, TIR) for modelling; disease scores and physiological measurements are ground truth and explanatory variables. All flight dates are pooled (no date effect is modelled), detection and severity are treated as separate tasks, and every method is taken from, or justified by, the cited literature.`));
// ======================= CHAPTER 2 REVIEW OF LITERATURE =======================
K.push(H1('2. Review of literature'));
K.push(P(`This chapter reviews the studies on which the methodology is built. Sections 2.1–2.9 are organised by theme; Section 2.10 analyses the eight core reference papers in detail; Section 2.11 summarises the additional studies in one table; and Section 2.12 lists the gaps that this thesis fills.`));
K.push(H2('2.1 Spectral signatures of plant diseases'));
K.push(P(`Plant pathogens change the optical properties of leaves in a way that depends on the host–pathogen interaction: biotrophs such as rusts and white rust first cause chlorosis and then sporulating pustules, whereas necrotrophs kill tissue (Mahlein, 2016). Leaf-scale studies established the typical response. Zhang et al. (2012a) measured leaves of winter wheat with powdery mildew in the laboratory and found that most of 32 spectral features responded to the disease; PLSR estimated disease severity better than multiple linear regression (R^{2} = 0.80, relative RMSE 0.23 with seven components) and Fisher linear discriminant analysis separated heavily damaged leaves with producer's and user's accuracies above 90%. At the canopy scale, Krishna et al. (2014, ICAR-IARI) used a field spectroradiometer (350–2500 nm) for wheat yellow rust; a full-spectrum PLS model gave R^{2} = 0.96 in calibration and r^{2} = 0.93 in validation, and PLS loading weights identified 428, 672 and 1399 nm, which in a three-band MLR gave r^{2} = 0.89–0.90.`));
K.push(P(`Spectral change develops in stages. Bohnenkamp et al. (2021) built a hyperspectral library of wheat foliar diseases from infection to symptom appearance, defined spectral "turning points" with histology and classified biotrophic and necrotrophic fungi with high accuracy. Terentev et al. (2023) detected wheat leaf rust from the fourth day after inoculation with 97–100% accuracy using SVM, and linked the most important wavebands (502, 466, 598, 718, 534, 766, 694, 650, 866, 602 and 858 nm) to leaf pigments. Zhang et al. (2024) showed for tomato bacterial leaf spot that pre-symptomatic detection relied more on water content (around 1400 nm) and defence-related responses (around 750 nm) than on pigments or structure, which became important only at symptomatic stages; vegetation indices as features improved classification by 26–37% over raw spectra.`));
K.push(P(`A practical problem is that disease and abiotic stress can produce similar spectral change. Zhang et al. (2012b) compared yellow rust with nitrogen and water stress in canopy spectra over five growth stages: 28 of 38 spectral features responded to yellow rust, but most also responded to nutrient or water stress; only the physiological reflectance index (PhRI) responded to yellow rust alone at all stages. This is why the thesis uses an RBD with uniform irrigation and fertiliser, tests disease-specific features and interprets thermal signals together with a water index.`));
K.push(H2('2.2 Disease-specific spectral indices'));
K.push(P(`General vegetation indices respond to any loss of greenness. Mahlein et al. (2013) introduced **spectral disease indices**: ReliefF ranks single bands and normalised band differences, and an exhaustive search finds the combination ND(λ_{1}, λ_{2}) + w R_{λ3} that best separates healthy and diseased leaves; indices for Cercospora leaf spot, sugar beet rust and powdery mildew reached 85–92% balanced accuracy. The approach has been repeated for other diseases. Meng et al. (2020) used RELIEF-F on leaf spectra (350–2500 nm) of southern corn rust to build a health index (572, 766 and 1445 nm) and a severity index (575, 640 and 1670 nm); with SVM they reached 87% accuracy for detection and 70% for three-level severity classification, 1.1% and 8.3% better than the best of 38 published indices. Mandal et al. (2023, ICAR-IARI) developed a ratio and a normalised-difference blast index from R1148 and R1301 (R^{2} = 0.85 and 0.86 with blast severity). Ramalingam et al. (2026, ICAR-IARI) used random-forest impurity to select ten informative wavelengths, searched over one million band combinations and proposed the Rice Blast Index (R1068 − R1560)/(R1068 + R1560), with an F1-score of 0.95 across independent seasons. Bhattacharya and Chattopadhyay (2013) formulated 224 new band combinations from Hyperion data for mustard Sclerotinia rot and recommended the three-band ROTI = R1175/(R1982 + R691). These studies show that (i) a disease-specific index is worth building, (ii) SWIR bands often enter the best index, and (iii) severity is harder to classify than presence. The thesis therefore builds a White Rust Index (Step 1.3) and searches both VNIR and SWIR bands.`));
K.push(H2('2.3 UAV-based disease sensing'));
K.push(P(`UAVs move disease sensing from the leaf to the plot. Guo et al. (2021) flew a hyperspectral camera (450–950 nm) over wheat yellow rust six times; indices gave R^{2} = 0.75 at mid stage, texture was more useful at late stage, combining indices and texture was best, and a 10 cm pixel size was optimal. Bohnenkamp et al. (2019) compared ground-vehicle and UAV hyperspectral imaging of yellow rust and found that feature selection improved prediction only when performed on the data set being analysed: feature sets transferred between scales or sensors performed worse than an uninformed, regularly sampled band set. This finding is the reason why, in this thesis, every feature-selection step is repeated on UAV data inside the training folds. Abdulridha et al. (2019) detected citrus canker with a UAV hyperspectral camera (400–1000 nm) and reached 100% accuracy at tree level, with the water index (WI) and chlorophyll indices among the best of 31 indices. Nguyen et al. (2023) used a multispectral UAV over spring wheat yellow rust: red-edge (690–740 nm) and NIR bands separated healthy and severely infected plots, CRI2, SAVI2 and GLCM contrast were the most correlated features, and a 3D-CNN reached 60% accuracy at 40 days after sowing, rising to 79% with spectral–spatial–temporal data. Liu et al. (2024) combined UAV multispectral and thermal images of wheat powdery mildew and estimated disease index with R^{2} = 0.90. Deng et al. (2024) proposed RustQNet, a deep network fusing UAV RGB, multispectral and vegetation-index images for the wheat stripe rust disease index (R^{2} = 0.80; three modalities improved R^{2} by 17.65–35.59% over single modalities and by 1.27–6.67% over two modalities).`));
K.push(H2('2.4 Thermal sensing of disease'));
K.push(P(`Thermal imaging detects the effect of infection on transpiration. Mahlein et al. (2019) compared thermal, chlorophyll-fluorescence and hyperspectral imaging of wheat spikelets with Fusarium head blight: hyperspectral imaging was the best single sensor (up to 89% accuracy), thermal + hyperspectral the best pair (mean 90%), and adding the third sensor did not improve further (87%). Feng et al. (2022) fused canopy spectra, thermal and RGB texture for wheat powdery mildew: vegetation indices were the best single source, then thermal parameters (CT, CTD, CTR, NRCT) and texture, and random forest regression with all three gave R^{2} = 0.872 in calibration and 0.862 in validation. Baranowski et al. (2015) used thermal (8–13 µm) and VNIR + SWIR hyperspectral imaging of oilseed rape (Brassica napus) leaves inoculated with Alternaria species: leaf-temperature distributions and spectra, especially in the SWIR (1000–2500 nm), differed significantly between treatments, and second-derivative spectra with back-propagation neural networks classified days after inoculation with 90.5% accuracy. This is the closest Brassica precedent for combining thermal and SWIR hyperspectral data.`));
K.push(H2('2.5 Feature selection for disease detection'));
K.push(P(`Hyperspectral and multi-sensor data contain far more features than samples, so feature selection is central. Tian et al. (2021) combined threshold-based separability scalograms, VIF < 10 and ML-SFFS with LDA, k-NN and SVM for rice leaf blast and needed only 2–4 features. Mustafa et al. (2023) chained Boruta → VIF < 10 → ML-SFFS for Fusarium head blight across three sensors. Meng et al. (2020) and Mahlein et al. (2013) used ReliefF; Lv et al. (2023) combined RELIEF-F with SFFS to merge spectral bands, indices, wavelet features and first-derivative features for southern corn leaf blight, improving severity classification by about 7% (OA 81.8%, macro-F1 0.82) and asymptomatic detection by 1–2% (OA 87.1%). Zhu et al. (2017) and Huang et al. (2020) used the successive projections algorithm (SPA) to select effective wavelengths. Das et al. (2020, ICAR-IARI) selected 17 wavelengths with ANOVA and classification and regression trees (CART) and quantified separability of rice genotypes with the Jeffries–Matusita (JM) distance; Mandal et al. (2023) used JM to show that blast severity levels were separable (JM > 1.92) except two adjacent levels. Together these studies support the combination used here: a relevance step (statistics, ReliefF, Boruta), a redundancy step (VIF) and a wrapper step (ML-SFFS), with JM used to describe separability.`));
K.push(H2('2.6 Multimodal data fusion'));
K.push(P(`Fusion combines information from several sources at the pixel (data) level, the feature level or the decision level. Most disease studies fuse at the **feature level**: features extracted from each sensor are concatenated or merged in a model. Maimaitijiang et al. (2020) compared input-level (DNN-F1) and intermediate-level (DNN-F2) fusion of UAV RGB, multispectral and thermal features for soybean yield; fusion beat every single sensor, DNN-F2 was best (R^{2} = 0.720, RMSE 15.9%) and was more robust across genotypes. Mustafa et al. (2023) pooled disease-sensitive features from hyperspectral reflectance, fluorescence imaging and a phenotyping camera and let ML-SFFS choose the cross-sensor combination. Feng et al. (2022) and Liu et al. (2024) showed that adding thermal features raises accuracy. Zhu et al. (2017) fused effective wavelengths with GLCM texture and reached accuracies up to 95%, and Huang et al. (2020) fused spectral, colour and texture features of hyperspectral images of wheat ears with a PSO-optimised SVM (95% training and 92% prediction accuracy). Deng et al. (2024) fused image modalities in an end-to-end network with a mutual-information minimisation module. Mahlein et al. (2019) also showed the limit: a third sensor did not help. The thesis therefore tests each sensor alone and four combinations, and compares interpretable ML-SFFS fusion with DNN fusion.`));
K.push(H2('2.7 Pre-symptomatic detection'));
K.push(P(`Detection before symptoms is the most valuable and the most difficult task. Under controlled conditions, Zhu et al. (2017) detected tobacco mosaic virus 48 h after inoculation with hyperspectral imaging (380–1023 nm), SPA wavelengths and texture, whereas visible symptoms appeared after 5 days. Tian et al. (2021) detected asymptomatic rice blast with overall accuracies above 65%, rising above 80% at the early stage; they labelled a sample as infected only if symptoms later appeared, the labelling rule adopted here. Mustafa et al. (2023) reached 87.04% for asymptomatic Fusarium head blight; Lv et al. (2023) reached 87.1% for asymptomatic southern corn leaf blight; Terentev et al. (2023) reached 97–100% from four days after inoculation; Zhang et al. (2024) found that water- and defence-related bands drive pre-symptomatic detection. All of these were at leaf, spike or plant scale; Nguyen et al. (2023) is one of few field UAV studies of early detection (60% at tillering). Objective 3 tests whether pre-symptomatic detection of white rust is possible at UAV plot scale.`));

K.push(H2('2.8 Brassica and mustard studies'));
K.push(P(`No sensor study of white rust in mustard was found. The closest work is on other stresses of Brassica crops. Baranowski et al. (2015) (Section 2.4) showed that thermal and SWIR hyperspectral imaging detect Alternaria infection in oilseed rape. Two studies on Indian mustard were carried out at Bharatpur (Rajasthan), the planned validation site of this thesis, and both involved the Space Applications Centre (ISRO): Shukla et al. (2024) on mustard aphid and Bhattacharya and Chattopadhyay (2013) on Sclerotinia rot.`));

K.push(P('Two hyperspectral studies on Indian mustard at Bharatpur, the planned validation site of this thesis, support several steps of the methodology (' + T('mustard') + '). They are used as mustard-specific evidence; the eight papers above remain the methodological basis.'));
K.push(...tab2('mustard', [
  ['Paper', 'Crop, stress and data', 'Key methods', 'Main result', 'Taken for this thesis'],
  ['Shukla et al. (2024), Remote Sens.', 'Mustard aphid (Lipaphis erysimi), severity grade 1–5 (AISG); ASD FieldSpec 4 canopy spectra (350–2500 nm, analysed 400–1100 nm); 8 farmers\' fields, two seasons', 'Savitzky–Golay smoothing (9 nm); Spearman correlation of reflectance, FD and SD with AISG; common sensitive regions; PCA and PLSR loadings; RSI, DSI, NDSI; PLSR, PCR and other regression models; 80/20 split', 'Common sensitive regions 483–487, 509–515, 690–714, 719–723 nm; key bands 679, 746, 979 nm; PLSR best (RMSE 0.66, r^{2} 0.71)', 'Correlation scalograms of R, FD and SD (Step 1.2); common-region rule; PCA/PLSR loading-based discrimination of severity classes (Step 1.2, Sub-step F); PLSR for severity; a mustard baseline to compare white rust bands with'],
  ['Bhattacharya and Chattopadhyay (2013), Comput. Electron. Agric.', 'Mustard Sclerotinia rot, 5 km × 5 km; Tmin, MODIS LST and NDWI, EO-1 Hyperion (30 m), LISS-IV mask; 16 sites', 'Stage I weather anomaly; Stage II TVDI–NDWI space (canopy stress without soil-moisture stress = rot); Stage III two-step stepwise canonical discriminant analysis (25 bands), 224 new band combinations', 'SWIR bands most sensitive (R^{2} 0.74–0.95); new three-band ROTI = R_{1175}/(R_{1982} + R_{691}), R^{2} 0.94; DWSI-1 and DWSI-4 retained', 'ROTI, DWSI-1 and DWSI-4 added to the HS indices; SWIR in the WRI search; separating disease from water stress in the thermal analysis'],
], [1500, 1900, 2250, 1950, 1706], 'Mustard hyperspectral studies from Bharatpur used as supporting evidence.', 16));
K.push(BL('**Caution 1.** Shukla et al. (2024) list the sensitive regions differently in the abstract (493–497, 509–515, 690–714, 717–721 and 752–756 nm) and in the results (Table 4: 483–487, 509–515, 690–714, 719–723 nm); the results table is quoted here.'));
K.push(BL('**Caution 2.** In Bhattacharya and Chattopadhyay (2013), the R^{2} values are fitted to five group means of disease incidence (16 sites), so they are optimistic; the DWSI-1 and DWSI-4 values also differ between text and figure (0.87 and 0.93). The indices are therefore tested here, not assumed to work for white rust.'));
K.push(H3('2.8.1 How the two mustard studies discriminated disease classes'));
K.push(P(`**Shukla et al. (2024)** rated aphid damage on a five-grade scale (AISG 1 = no infestation to 5 = highly severe) and discriminated the grades in four steps. (i) **Grade-wise spectra:** the mean reflectance of each grade was compared; healthy plants reflected more in the blue (431–498 nm) and NIR (750–1100 nm), and reflectance was correlated with AISG mainly within 490–720 nm. (ii) **Derivative analysis:** first-derivative spectra showed peaks at 502 and 699 nm and lower lobes at 572, 612 and 662 nm, and the first derivative decreased as AISG increased; second-derivative values increased with AISG in 477–489 and 690–715 nm. (iii) **Correlation:** Spearman correlation of reflectance, first and second derivatives with AISG (99% significance) gave the common sensitive regions 483–487, 509–515, 690–714 and 719–723 nm. (iv) **PCA and PLSR loading weights:** PCA (600 samples, full cross-validation) and PLSR were applied to 400–1100 nm; bands at the local maxima and minima of the loading weights of the first three PCs or factors were taken as the dominant bands "for discrimination of different AISGs" — 500, 679, 746 and 979 nm (PCA) and 491, 679, 746 and 979 nm (PLSR). The grades were then predicted with regression models, PLSR being best (validation r^{2} 0.71, RMSE 0.66). Shukla et al. did not use a formal linear or canonical discriminant analysis; their "discrimination" is the correlation- and loading-based band selection described above. This thesis adopts it as Sub-step F of Step 1.2.`));
K.push(P(`**Bhattacharya and Chattopadhyay (2013)** used a formal **two-step stepwise canonical discriminant analysis**. Rot incidence at 16 sites was grouped into five levels (5, 15, 30, 35 and 45%), which served as the grouping variable. The first analysis, with Hyperion band reflectances (mean of 3 × 3 pixels) as predictors and Wilks' lambda as the stepwise criterion, retained 25 bands in the green, red, NIR and SWIR with canonical correlation above 0.5; the second analysis ranked 30 published indices and 224 new band combinations by canonical correlation and retained DWSI-1 and DWSI-4 among the published indices (correlation with incidence above 0.8) and DRI and ROTI among the new ones (canonical correlation above 0.8). This thesis adopts the method as a canonical discriminant analysis between healthy, Low, Moderate and High plots for every sensor (Step 1.6).`));

K.push(H2('2.9 Hyperspectral disease work at ICAR-IARI'));
K.push(P(`The Division of Agricultural Physics, ICAR-IARI, has a line of field-spectroradiometer studies that this thesis extends to UAV multimodal sensing. Krishna et al. (2014) assessed wheat yellow rust with PLS and MLR (Section 2.1). Mandal et al. (2022) characterised rice blast reflectance for ten genotypes scored 0–9: severely infected plants had higher visible and lower NIR reflectance, the 550–760 nm region and 1140–1300 nm had correlations above 0.6 with severity, and the amplitude of the red-edge first-derivative peak fell with severity. Mandal et al. (2023) extended this to 20 genotypes under upland and lowland conditions, used JM distance to test separability of severity levels, evaluated 26 published indices, proposed new blast indices and found SVM regression the best multivariate model (validation R^{2} = 0.94, RMSE 0.7). Das et al. (2020) combined ANOVA, CART and JM distance to discriminate 14 rice genotypes from canopy spectra. Ramalingam et al. (2026) used Savitzky–Golay smoothing, SNV and MSC normalisation, derivatives, PCA, t-SNE and UMAP, random-forest band selection and an isolation-forest outlier filter to build a rice blast index. The thesis reuses several of these tools — Savitzky–Golay smoothing, derivative spectra, red-edge parameters, JM distance, correlation with severity, PLSR, SVM and random forest — and adds what the earlier studies did not have: UAV imaging, four sensors, fusion and pre-symptomatic prediction.`));
K.push(H2('2.10 The eight core reference papers'));

K.push(P(T('papers') + ' summarises the eight reference papers. All values were checked against the original papers.'));
K.push(...tab2('papers', [
  ['Paper', 'Crop, disease and data', 'Key methods', 'Main result', 'Taken for this thesis'],
  ['Tian et al. (2021), RSE', 'Rice leaf blast; leaf spectra (ASD, 350–2500 nm); greenhouse, two years', 'Reflectance, 97 indices, wavelet features; threshold-based separability scalogram; VIF < 10; ML-SFFS with LDA, k-NN, SVM; 4-fold CV × 100', '2–4 features enough; OA > 65% (asymptomatic), > 80% (early), up to 95% (mild); SVM-SFFS up to 10% better than SVM with all features', 'VIF; ML-SFFS; top-5% and one-band-per-region selection rules; rule for labelling pre-symptomatic samples'],
  ['Mustafa et al. (2023), Front. Plant Sci.', 'Wheat Fusarium head blight; spike spectra, fluorescence and phenotyping images; two seasons', 'Boruta → VIF < 10 → ML-SFFS (k-NN, RF, SVM); univariate and multivariate regression', 'Asymptomatic detection 87.04% rising to 95%; best single feature 1/R_{700} (R^2 0.81); k-NN regression R^2 0.92', 'ML-SFFS multi-sensor fusion; Boruta → VIF → SFFS chain; k-NN and RF; 1/R_{700} feature'],
  ['Mahlein et al. (2013), RSE', 'Sugar beet: Cercospora leaf spot, rust, powdery mildew; leaf spectra (analysed 450–950 nm)', 'ReliefF ranking of single bands and normalised differences; exhaustive search for index = ND + w·R; 8-fold stratified CV; balanced accuracy', 'Disease-specific indices classified healthy and diseased leaves with 85–92% balanced accuracy; transferable to imaging data', 'Method to build a White Rust Index (WRI) from UAV HS data'],
  ['Mahlein et al. (2019), Sensors', 'Wheat Fusarium head blight on spikelets; thermal, fluorescence and hyperspectral imaging', 'Thermal (MTD, ΔT), fluorescence (Fm, Fv/Fm, Y(II)) and indices (NDVI, PRI, PSSRa/b/c, WI); Tukey HSD; Pearson r; SVM on single sensors and combinations', 'PSSRa/b separated infected spikelets 3 dai; HSI best single sensor (max 89%); thermal + HSI best pair (mean 90%); all three sensors did not improve further (87%)', 'Testing single sensors versus combinations; PSSRa, PSSRb, WI; Tukey HSD'],
  ['Feng et al. (2022), Sensors', 'Wheat powdery mildew; ground canopy spectra (325–1075 nm) and thermal/RGB images at 1 m', 'Indices, GLCM texture, thermal parameters (CT, CTD, CTR, NRCT); SPA; PLSR, SVR, RFR; independent experiment for validation', 'Indices best single source, then thermal, then texture; RFR with all three: R^2 0.872 (calibration), 0.862 (validation)', 'CTD and NRCT; five texture measures; RFR; independent-site validation'],
  ['Guo et al. (2021), Remote Sens.', 'Wheat yellow rust; UAV hyperspectral (450–950 nm, 1.2 cm); 6 flights', '15 indices; GLCM on PCA images; feature kept if significantly correlated with DI (p < 0.01) in all stages; PLSR; leave-one-out CV', 'Index model R^2 0.75 (mid stage); texture R^2 0.65 (mid) and 0.82 (late); index + texture best; 10 cm best pixel size', 'UAV narrow-band indices (SIPI, PSRI, PRI, ARI, NPCI); correlation rule; PLSR'],
  ['Liu et al. (2024), Comput. Electron. Agric.', 'Wheat powdery mildew; UAV multispectral (475–840 nm) + thermal; 60 plots, 5 dates', 'Mean and percentile reflectance; 12 indices; three-band texture combination indices (TTCI); canopy temperature; Dunnett test; RFE; multiple linear regression', 'NDRE, PSRI and MTCI consistently tracked disease; spectra + TTCI2 + CT: R^2 0.90, RMSE 8.28%', 'MS indices; disease-index formula and 5-point survey; disease maps'],
  ['Maimaitijiang et al. (2020), RSE', 'Soybean yield; UAV RGB + multispectral + thermal (FLIR Vue Pro R 640)', 'Spectral, structure (height, vegetation fraction), thermal (NRCT) and texture features; PLSR, SVR, RFR; DNN-F1 (input-level) and DNN-F2 (intermediate-level) fusion', 'Fusion beat single sensors; DNN-F2 best (R^2 0.720, RMSE 15.9%); more robust across genotypes', 'Feature-level fusion design; DNN-F1 and DNN-F2; thermal calibration; vegetation fraction'],
], [1500, 1750, 2300, 2050, 1706], 'Summary of the eight reference papers.', 16));

K.push(H3('2.10.1 What the papers agree on'));
K.push(...tab2('lessons', [
  ['Lesson from the papers', 'Evidence', 'How it is used here'],
  ['Pigment (chlorophyll) indices respond first', 'PSSRa/b at 3 dai (Mahlein 2019); chlorophyll indices dominate selected features (Tian 2021); 1/R_{700} best single feature (Mustafa 2023)', 'Many chlorophyll indices in the HS and MS feature sets'],
  ['Fusion helps, but not with every sensor', 'Fusion improved accuracy (Feng 2022; Liu 2024; Maimaitijiang 2020); adding a third sensor gave no gain (Mahlein 2019)', 'Each sensor alone and each combination is tested'],
  ['A few well-chosen features beat many', 'Optimum combinations of 2–4 features (Tian 2021; Mustafa 2023)', 'Boruta → VIF → ML-SFFS'],
  ['ML-SFFS can fuse sensors at feature level', 'Mustafa 2023 pooled features of three sensors and let ML-SFFS choose a cross-sensor combination', 'Pooled and sensor-wise ML-SFFS fusion'],
  ['Intermediate fusion DNN is the strongest fusion model', 'DNN-F2 > DNN-F1 > RFR, SVR, PLSR (Maimaitijiang 2020)', 'DNN-F1 and DNN-F2 compared with ML-SFFS fusion'],
  ['Thermal and texture add information that spectra miss', 'Thermal raised R^2 (Feng 2022; Liu 2024); texture helped at high severity (Guo 2021)', 'Thermal parameters and RGB/MS/thermal texture are separate feature families'],
  ['Multi-date data can be pooled', 'One disease-index model over five dates (Liu 2024); two growth stages pooled (Feng 2022)', 'All dates pooled'],
  ['Independent validation is essential', 'Second experiment as validation set (Feng 2022); two years (Tian 2021; Mustafa 2023)', 'Replication-wise cross-validation, then Bharatpur and farmers\' fields'],
], [2500, 3700, 3106], 'Common findings of the reference papers and their use in this methodology.', 17));
K.push(H3('2.10.2 ML-SFFS as a feature-level fusion technique'));
K.push(P('Sequential floating forward selection (SFFS; Pudil et al., 1994) with a machine-learning classifier as criterion is called ML-SFFS (Tian et al., 2021). Tian et al. (2021) used it within one sensor to combine reflectance bands, indices and wavelet features. Mustafa et al. (2023) extended it to multiple sensors: features of hyperspectral reflectance, chlorophyll-fluorescence imaging and a phenotyping camera were screened by Boruta and VIF, pooled, and ML-SFFS (k-NN, RF, SVM) selected the optimum cross-sensor combination ("partial fusion of selected disease-sensitive features through ML-SFFS"). The selected combinations mixed sensors (e.g. the fluorescence parameter Fv/Fm with NDVI and SRPI), had two to four features, and gave 87.04% accuracy at the asymptomatic stage, rising to 95% at 20% severity. No study was found that applies ML-SFFS fusion to UAV RGB, MS, HS and TIR data for a crop disease; this is a novel element of the thesis. In this experiment all four sensors observe the same plots on the same flights, so their features are exactly paired for fusion.'));
K.push(H2('2.11 Summary of the additional studies'));
K.push(P(`${T('extralit')} summarises the additional studies reviewed in Sections 2.1–2.9 and what each contributes to the methodology.`));
K.push(...tab2('extralit', [
  ['Study', 'Crop, disease, data', 'Methods and main result', 'Used in this thesis'],
  ['Zhang et al. (2012a)', 'Wheat powdery mildew; leaf spectra (lab)', '32 spectral features; t-test and correlation; PLSR R^{2} 0.80; FLDA > 90% for heavy damage', 'Statistics per feature; PLSR for severity'],
  ['Zhang et al. (2012b)', 'Wheat yellow rust vs N and water stress; canopy spectra', 'Independent t-test of 38 features at 5 stages; only PhRI specific to yellow rust', 'Disease vs abiotic stress; disease-specific index'],
  ['Krishna et al. (2014)', 'Wheat yellow rust; canopy spectra 350–2500 nm (IARI)', 'PLS R^{2} 0.96 (val. 0.93); bands 428, 672, 1399 nm by PLS loadings', 'PLSR; loadings as band evidence'],
  ['Mahlein (2016)', 'Review: imaging sensors for disease detection', 'Principles of RGB, multispectral, hyperspectral, thermal and fluorescence sensing', 'Physical basis (Chapter 1)'],
  ['Bohnenkamp et al. (2019)', 'Wheat yellow rust; ground and UAV hyperspectral imaging', 'Feature selection helps only on the analysed data set; transfer of feature sets fails', 'Selection repeated inside UAV training folds'],
  ['Abdulridha et al. (2019)', 'Citrus canker; lab and UAV hyperspectral (400–1000 nm)', 'RBF network and k-NN; WI, ARI, TCARI best indices; 100% at tree level', 'k-NN; WI and ARI features'],
  ['Meng et al. (2020)', 'Southern corn rust; leaf spectra 350–2500 nm', 'RELIEF-F disease indices; SVM 87% detection, 70% severity', 'ReliefF; separate detection and severity indices'],
  ['Huang et al. (2020)', 'Wheat FHB; hyperspectral images of ears', 'SPA bands, GLCM and colour features; PSO-SVM; fusion best (92% prediction)', 'Spectral + texture + colour fusion'],
  ['Das et al. (2020)', 'Rice genotypes; canopy spectra (IARI)', 'ANOVA + CART selected 17 bands; JM separability; QDA 98%', 'JM distance'],
  ['Bohnenkamp et al. (2021)', 'Wheat foliar diseases; hyperspectral library', 'Spectral turning points from infection to symptoms; ML classifiers', 'Stage-dependent spectral change'],
  ['Mandal et al. (2022)', 'Rice blast, 10 genotypes (IARI)', 'Reflectance and first-derivative correlation; red-edge amplitude falls with severity', 'Red-edge parameters; FD scalograms'],
  ['Mandal et al. (2023)', 'Rice blast, 20 genotypes (IARI)', 'JM > 1.92 for most levels; new blast indices; SVM regression best', 'JM; index search; SVR'],
  ['Lv et al. (2023)', 'Southern corn leaf blight; leaf spectra', 'Bands + indices + wavelets + FD; RELIEF-F + SFFS; SVM; severity OA 81.8%', 'Combining R, FD and indices; ReliefF + SFFS'],
  ['Nguyen et al. (2023)', 'Wheat yellow rust; UAV multispectral', 'Indices + GLCM; SVM, RF, MLP, 3D-CNN; 60–79% early detection', 'MS indices and texture; RF, SVM'],
  ['Terentev et al. (2023)', 'Wheat leaf rust; hyperspectral, lab', 'SVM 97–100% from 4 dai; pigment-linked bands', 'Pre-symptomatic evidence'],
  ['Deng et al. (2024)', 'Wheat stripe rust; UAV RGB + MS + VI', 'RustQNet deep fusion; R^{2} 0.80; three modalities > two > one', 'Deep fusion; DI regression'],
  ['Zhang et al. (2024)', 'Tomato bacterial leaf spot; hyperspectral images', 'Pre-symptomatic detection driven by water (1400 nm) and 750 nm; VIs improve ML by 26–37%', 'Pre-symptomatic features; indices as inputs'],
  ['Zhu et al. (2017)', 'Tobacco mosaic virus; hyperspectral imaging', 'SPA bands + GLCM; BPNN, ELM, LS-SVM up to 95%; detection at 48 h', 'Pre-symptomatic fusion of spectra and texture'],
  ['Baranowski et al. (2015)', 'Oilseed rape, Alternaria; thermal + VNIR/SWIR imaging', 'Temperature and SWIR differ; second derivative + BPNN 90.5%', 'Brassica precedent for TIR + SWIR'],
  ['Ramalingam et al. (2026)', 'Rice blast; leaf and canopy spectra (IARI)', 'SG, SNV, MSC, derivatives; RF band selection; Rice Blast Index, F1 0.95', 'Pre-processing; index search'],
], [1800, 2300, 3100, 2106], 'Additional studies reviewed and their contribution to the methodology.', 15));
K.push(H2('2.12 Research gaps filled by this thesis'));

K.push(BL('None of the eight papers studies white rust or mustard. The two mustard studies from Bharatpur (Section 2.8) used ground spectroscopy (aphid) or satellite data (Sclerotinia rot), not UAVs, and neither studied white rust.'));
K.push(BL('Only two papers use a UAV for disease (Guo 2021: HS only; Liu 2024: MS + TIR); none combines all four UAV sensors.'));
K.push(BL('ML-SFFS fusion (Mustafa 2023) and DNN fusion (Maimaitijiang 2020) have not been compared, nor applied to UAV data for disease severity.'));
K.push(BL('Pre-symptomatic detection was shown only at leaf or spike scale under controlled conditions (Tian 2021; Mustafa 2023; Mahlein 2019).'));
K.push(...fig2('matrix', 'f3_paper_method_matrix.png', 'Methods used in each reference paper. Dark green cells marked * are adopted in this methodology; grey cells are used in the papers but not adopted.', 430));
K.push(BL('No sensor-based study of white rust in mustard exists at leaf, canopy, UAV or satellite scale; ICAR-IARI work on other diseases used field spectroradiometers, not imaging sensors.'));
K.push(BL('Feature sets do not transfer between scales or sensors (Bohnenkamp et al., 2019), so white-rust features must be selected from UAV data themselves.'));
K.push(H1('3. Materials and methods'));
K.push(H2('3.1 Overall workflow'));
K.push(P(F('workflow') + ' shows the workflow and ' + T('objmap') + ' links each objective to its ORW activities, methods and outputs.'));
K.push(...fig2('workflow', 'f1_workflow.png', 'Objective-wise workflow of the thesis.', 520));
K.push(...tab2('objmap', [
  ['Objective (ORW activities)', 'Question', 'Main methods (source)', 'Output'],
  ['1. Characterise (Act. 1.1–1.4)', 'Which features of each sensor respond to white rust (detection) and to its severity, and why?', 'Sensor-specific features; correlation scalograms + ReliefF + JM (HS); WRI (Mahlein 2013); t-test / Mann–Whitney, ANOVA / Kruskal–Wallis; Boruta (Mustafa 2023); cross-sensor correlation (Mahlein 2019)', 'Disease-specific feature (DSF) pools per sensor and task'],
  ['2. Detect and discriminate severity (Act. 2.1–2.3)', 'Which sensor or combination, fusion strategy and model detect white rust and discriminate its severity best?', 'VIF → ML-SFFS; pooled and sensor-wise ML-SFFS fusion (Mustafa 2023); DNN-F1/F2 (Maimaitijiang 2020); SVM, RF, k-NN, PLSR', 'Best sensor set, fusion and model for detection, severity classes and DI; maps'],
  ['3. Pre-symptomatic prediction (Act. 3.1)', 'Can later-infected plots be separated from healthy plots before symptoms?', 'Boruta → VIF → ML-SFFS; single sensors and fusion; SVM, RF, k-NN (Tian 2021; Mustafa 2023)', 'Best early-warning sensor set; risk maps'],
], [2000, 2300, 3200, 1806], 'Objectives, questions, methods and outputs.', 16));
K.push(SIMPLE(`The work moves from **understanding** to **modelling** to **early warning**. Objective 1 asks which measurements of each sensor change when mustard gets white rust and why; its output is a short list of disease-specific features (DSFs) per sensor. Objective 2 uses those lists to build classifiers and regressors, first with one sensor at a time and then with sensors combined (fusion). Objective 3 repeats the modelling with data from before symptoms appear. The same validation rules apply everywhere, so results are comparable.`));

// ======================= 4 =======================
K.push(H2('3.2 Field experiment'));
K.push(P('The IARI experiment (2025–26) is a factorial randomised block design (RBD) with three factors: inoculation timing G1–G4 (about 50, 40, 30 and 20 days after sowing, created by staggered sowing on 20 Nov, 30 Nov, 10 Dec and 20 Dec 2025 and one inoculation on 10 Jan 2026), variety (V1 Varuna, highly susceptible; V2 Pusa Vijay, moderately susceptible; V3 PM 38, resistant) and dose (D1 control; D2 inoculated with 1.5 × 10^5 zoosporangia mL^{−1}). This gives 24 treatments × 3 replications = **72 plots** of 3 m × 3 m (' + F('design') + ').'));
K.push(...fig2('design', 'f4_design_validation.png', 'Factorial RBD with 72 plots in three replications and the replication-wise validation scheme.', 560));
K.push(INCASE(`**Why this design?** (i) Four inoculation timings (G1–G4) on staggered sowings mean that on any flight date the plots are at different stages of infection, so one flight already contains a range of severities. (ii) Three varieties of different susceptibility (Varuna highly susceptible, Pusa Vijay moderately susceptible, PM 38 resistant) widen the severity range and allow a test of robustness across genotypes. (iii) Un-inoculated controls (D1) provide the healthy class at every date. (iv) Three replications in randomised blocks remove field gradients and give three balanced, independent test folds for leave-one-replication-out validation (Chapter 7). With 24 treatments × 3 replications there are 72 plots of 3 m × 3 m.`));
K.push(...STEPEND(`72 plots (24 treatments × 3 replications) with a range of white-rust severities on every flight date, healthy controls at every date, three genotypes of different susceptibility, and three balanced replications that become the validation folds.`, [
  `**Split-plot or strip-plot designs** when one factor (e.g. sowing date) is hard to randomise in small plots (Gomez and Gomez, 1984).`,
  `**Natural infection at hot-spot locations or spreader-row screening** instead of artificial inoculation; more realistic, but severity is less controlled (Saharan et al., 2014).`,
  `**Multi-season, multi-site experiments** to capture year and site effects, as in the two-year designs of Tian et al. (2021) and Mustafa et al. (2023).`
]));
K.push(H2('3.3 Ground truth, severity classes and tasks'));
K.push(BL('**Disease index (DI).** At the centre and four corners of each plot, fully expanded leaves of sampled plants are scored on the 0–6 scale of leaf area covered by pustules (0 none; 1 0–5%; 2 5–10%; 3 10–20%; 4 20–35%; 5 35–50%; 6 > 50%). The plot DI follows Liu et al. (2024):'));
K.push(EQ('DI (%) = [ Σ (x × f) / ( n × Σ f ) ] × 100', '3.1'));
K.push(P('where x is the score, f the number of leaves with that score and n = 6 the highest score.'));
K.push(INCASE(`**Worked example of the disease index.** Suppose 10 leaves are scored in a plot: 2 leaves score 0, 3 score 1, 3 score 3 and 2 score 5. Then Σ(x × f) = 0×2 + 1×3 + 3×3 + 5×2 = 22 and n × Σf = 6 × 10 = 60, so DI = 22/60 × 100 = 36.7%. The plot is diseased (DI > 0) and falls in the **Moderate** class (25% < DI ≤ 50%). If all 10 leaves scored 6, DI would be 100%; if all scored 0, DI = 0 (healthy).`));
K.push(BL('**Health status.** Healthy: DI = 0; diseased: DI > 0. For pre-symptomatic flights (DI = 0 everywhere), a control plot is healthy and an inoculated plot is infected only if symptoms later appear on it (Tian et al., 2021).'));
K.push(BL('**Three plot-level severity classes** for diseased plots: Low, 0 < DI ≤ 25%; Moderate, 25% < DI ≤ 50%; High, DI > 50%. Because DI is continuous, class limits are written with "≤" and "<" so that every value falls into exactly one class.'));
K.push(BL('**Staghead severity (%)** = infected racemes / total racemes × 100, after inflorescence initiation (ORW).'));
K.push(BL('**Biochemical and biophysical parameters** (chlorophyll a and b, carotenoid, anthocyanin, relative water content, stomatal conductance, transpiration, photosynthesis, LAI; ORW Activity 1.2), used to interpret sensor features.'));
K.push(...tab2('tasks', [
  ['Task', 'Samples', 'Target', 'Objective'],
  ['D. Disease detection', 'All post-symptomatic plot-dates', 'Healthy (DI = 0) vs diseased (DI > 0)', '1 (characterise), 2 (model)'],
  ['S. Severity discrimination', 'Diseased plot-dates (DI > 0)', 'Low / Moderate / High', '1, 2'],
  ['R. Severity estimation', 'All post-symptomatic plot-dates', 'DI (%), continuous; also staghead (%)', '1, 2'],
  ['P. Pre-symptomatic detection', 'Pre-symptomatic plot-dates', 'Healthy vs later-infected', '3'],
], [2300, 2600, 2700, 1706], 'Tasks addressed in the thesis.', 17));
K.push(P('In practice the detection and severity models are applied in sequence: a plot-date classified as diseased by the detection model is then assigned a severity class by the severity model, giving one map with healthy, Low, Moderate and High plots.'));
K.push(...STEPEND(`For every plot-date: DI (%), health status (healthy/diseased), severity class (Low/Moderate/High), staghead severity after flowering, the pre-symptomatic label, and the physiological measurements used to interpret sensor features.`, [
  `**Image-based severity** from close-range RGB or hyperspectral images of leaves (pixel classification of pustules), which is more objective than visual scoring (Bock et al., 2010).`,
  `**Area under the disease progress curve (AUDPC)** as a season-level severity measure when one value per plot is needed (Shaner and Finney, 1977).`,
  `**Pathogen quantification** (e.g. qPCR or in planta pathogen populations) as ground truth for pre-symptomatic stages (Zhang et al., 2024).`,
  `**Ordinal treatment of the 0–6 scale** with ordinal regression instead of a continuous DI (McCullagh, 1980).`
]));
K.push(H2('3.4 Pooled dataset'));
K.push(P('After pre-processing, every plot on every flight is one sample (plot-date). All flights are pooled into one dataset, because only the pooled data contain the full range from healthy to high severity, and the date is not used in any analysis. Pooling across dates was also used by Liu et al. (2024), who built one disease-index model over five dates, and by Feng et al. (2022). Repeated observations of the same plot are not independent, so every training/test split keeps all observations of a plot in the same set (Chapter 7; Roberts et al., 2017). ' + T('dataset') + ' summarises the dataset.'));
K.push(...tab2('dataset', [
  ['Item', 'Description'],
  ['Sample unit', 'One plot on one flight (plot-date)'],
  ['Post-symptomatic samples (Objectives 1, 2)', '72 plots × post-symptomatic flights (1296 plot-dates planned in the ORW)'],
  ['Pre-symptomatic samples (Objective 3)', '72 plots × 6 flights (432 plot-dates; ORW)'],
  ['Predictors', 'Sensor-specific features (Section 4.1)'],
  ['Targets', 'Health status; severity class; DI (%); staghead (%); pre-symptomatic label'],
  ['Grouping for validation', 'Plot ID and replication (R1–R3)'],
], [3200, 6106], 'Structure of the pooled dataset.', 17));
K.push(INCASE(`One **sample** is one plot on one flight, described by one feature vector per sensor (for example 57 multispectral features) and labelled with health status, severity class and DI. If a plot is flown 18 times after symptoms appear, it contributes 18 samples, but these are not independent: the plot's soil, variety and position stay the same. If one date of plot 17 were in training and another date of plot 17 in testing, a model could recognise the plot rather than the disease and the accuracy would be inflated. Keeping all dates of a plot in the same fold prevents this **leakage**.`));

// ======================= 5 =======================
K.push(...STEPEND(`One pooled table with one row per plot-date (about 1296 post-symptomatic and 432 pre-symptomatic rows planned), the targets, and plot ID and replication for grouped validation.`, [
  `**Date-wise (stage-wise) models**, one per flight or growth stage, as in Guo et al. (2021); simpler interpretation but fewer samples per model.`,
  `**Mixed-effects models** with plot as a random effect to account for repeated measures explicitly (Zuur et al., 2009).`,
  `**Spectral–temporal features** (change between flights) instead of pooling single dates (Nguyen et al., 2023).`
]));
K.push(H2('3.5 Sensor-specific pre-processing'));
K.push(P('The four sensors record different physical quantities and need different pre-processing (' + F('chains') + ', ' + T('sensors') + '). Common to all: flights at 30 m with 85% forward and 80% side overlap between 11:00 and 14:00 h (ORW; similar to Liu et al., 2024 and Guo et al., 2021), GNSS-surveyed ground control points (GCPs), structure-from-motion orthomosaics, and co-registration of all products with the same GCPs. Features are extracted per plot inside an inner buffer of the plot polygon, so each sensor keeps its native pixel size; no pixel resampling between sensors is needed.'));
K.push(...fig2('chains', 'f8_sensor_chains.png', 'Pre-processing and feature-extraction chain of each UAV sensor.', 560));
K.push(...tab2('sensors', [
  ['Sensor (ORW)', 'Measures', 'Relevance to white rust', 'Pre-processing'],
  ['RGB (DJI Phantom, 5472 × 3648)', 'Visible colour, fine spatial pattern', 'White pustules, chlorosis and stagheads change texture, colour and cover', 'Orthomosaic; K-means canopy mask (Feng 2022); grey level and R, G, B bands'],
  ['MS (MicaSense RedEdge-MX: 475, 560, 668, 717, 840 nm)', 'Broad-band reflectance incl. red edge', 'Chlorophyll loss lowers NIR/red-edge contrast', 'Reflectance from irradiance sensor + ground panels (empirical line); NDVI canopy mask (Guo 2021)'],
  ['HS (VNIR 400–1000 nm; SWIR 1000–2500 nm; 481 bands used)', 'Narrow-band reflectance', 'Pigment, structure and water changes; disease-specific index', 'White-reference calibration; removal of noisy and water-absorption bands; Savitzky–Golay smoothing (Savitzky and Golay, 1964; Shukla et al., 2024; Mahlein et al., 2019)'],
  ['TIR (FLIR Vue Pro R, 7.5–13.5 µm)', 'Canopy temperature', 'Infection disturbs stomata and transpiration', 'Warm-up 15–20 min; radiometric conversion with air temperature, humidity, emissivity, height; check with blackbody/ground targets (Maimaitijiang 2020); K-means canopy segmentation (Feng 2022)'],
], [2100, 1700, 2500, 3006], 'Sensor-specific pre-processing.', 16));
K.push(BL('**Canopy masks.** The NDVI threshold of the MS mask is checked on each flight, because yellow mustard flowers lower NDVI and must not be removed as soil.'));
K.push(BL('**Hyperspectral pixel size.** The SWIR pixels are coarse (about 36 cm at 30 m, ORW), so a 3 m × 3 m plot with a 0.5 m inner buffer contains only about 5 × 5 SWIR pixels; plot means must be computed from pure canopy pixels only.'));
K.push(BL('**Water-absorption regions.** Bands in the strong atmospheric water-absorption regions (about 1350–1450 nm and 1800–1950 nm) and noisy sensor edges are removed if their signal is noisy; the remaining bands of the 481 are analysed.'));
K.push(LBL('Radiometric calibration in equations'));
K.push(P(`Multispectral and hyperspectral digital numbers (DN) are converted to reflectance ρ with the **empirical line method**: calibration panels of known reflectance are imaged on every flight and a linear relation is fitted for each band λ (Smith and Milton, 1999):`));
K.push(EQ('ρ_{λ} = a_{λ} DN_{λ} + b_{λ}', '3.2'));
K.push(P(`where a_{λ} (gain) and b_{λ} (offset) are obtained by least squares from the panels. For the MicaSense camera the downwelling irradiance sensor additionally corrects changes in sunlight during the flight. Thermal radiance is converted to temperature with the camera's radiometric model using emissivity, air temperature, relative humidity and flight height, and checked against ground targets of known temperature (Maimaitijiang et al., 2020).`));
K.push(INCASE(`For each flight the processing chain gives four co-registered products: an RGB orthomosaic and surface model, a five-band reflectance map, a hyperspectral reflectance cube and a canopy-temperature map. Plot polygons with a 0.5 m inner buffer are overlaid, soil and shadow pixels are removed with the canopy mask, and the mean (and, where needed, texture) of canopy pixels gives one value per feature, plot and flight.`));

K.push(...STEPEND(`Four co-registered, calibrated products per flight (RGB orthomosaic and surface model, five-band reflectance, hyperspectral reflectance cube, canopy-temperature map), canopy masks, and one feature value per plot-date for every feature.`, [
  `**Physics-based atmospheric correction** (6S or MODTRAN-type radiative transfer) instead of the empirical line, needed at higher altitudes and for satellites (Vermote et al., 1997).`,
  `**Scatter correction** of spectra with SNV or MSC (Barnes et al., 1989), as used by Ramalingam et al. (2026).`,
  `**Canopy masking** by Otsu thresholding of an index (Otsu, 1979), the excess-green index for RGB (Woebbecke et al., 1995) or supervised pixel classification, instead of NDVI thresholds or K-means.`,
  `**Temperature–emissivity separation** when emissivity varies within the scene (Gillespie et al., 1998); a constant canopy emissivity is used here.`,
  `**BRDF correction** of UAV mosaics from multi-angle observations (Aasen et al., 2018).`
]));
// ======================= 6 OBJECTIVE 1 =======================
K.push(H1('4. Objective 1: Characterise white rust through multimodal UAV sensing'));
K.push(LBL('Aim'));
K.push(P('To identify, for each sensor, which features differ between healthy and diseased plots (detection) and which change across the three severity classes and with DI (severity discrimination), and to explain these changes physiologically. Objective 1 has a common core applied to all sensors (statistics, Boruta, cross-sensor comparison) and sensor-specific parts (hyperspectral band-level analysis and the White Rust Index).'));
K.push(...fig2('obj1flow', 'n3_obj1_flow.png', 'Flow chart of Objective 1: sensor-specific feature extraction, hyperspectral band-level analysis and White Rust Index, statistical and machine-learning characterisation, and the disease-specific feature (DSF) pools passed to Objectives 2 and 3.', 520));
K.push(SIMPLE(`Objective 1 is the "diagnosis" stage. For every sensor it asks three questions: Does this feature differ between healthy and diseased plots (detection)? Does it change from Low to Moderate to High severity (severity discrimination and DI)? Which plant property explains the change? The answers come from statistical tests, correlation, ReliefF and Boruta, and are interpreted with the physiological measurements. Hyperspectral data get extra band-level steps (1.2, 1.3) because they have hundreds of contiguous bands.`));
K.push(H2('4.1 Step 1.1: Sensor-specific feature extraction'));
K.push(H3('4.1.1 Hyperspectral features'));
K.push(...tab2('hsfeat', [
  ['Feature family', 'Number', 'Description', 'Reference'],
  ['Reflectance', '481 bands', 'Smoothed plot-mean reflectance of all retained bands', 'Tian 2021; Guo 2021'],
  ['First derivative (FD)', '481', 'Slope of the spectrum (Eq. 4.1); reduces illumination and background effects', 'Tsai and Philpot 1998'],
  ['Second derivative (SD)', '481', 'Curvature (Eq. 4.1); separates overlapping absorption features', 'Tsai and Philpot 1998'],
  ['Red-edge parameters', '3', 'REP, Dr, SDr (Eq. 4.2)', 'Horler et al. 1983; Filella and Peñuelas 1994'],
  ['Narrow-band indices', '39', 'Chlorophyll, pigment ratio, photosynthesis, stress and water indices (' + T('hsidx') + ')', 'See ' + T('hsidx')],
  ['White Rust Index (WRI)', '1', 'Disease-specific index built in Step 1.3', 'Mahlein et al. 2013'],
], [2100, 1100, 3900, 2206], 'Hyperspectral feature families.', 17));
K.push(P('Derivatives are computed with the Savitzky–Golay derivative filter on the smoothed spectra; in finite-difference form (Tsai and Philpot, 1998):'));
K.push(EQ('FD(λ_{i}) = [R(λ_{i+1}) − R(λ_{i−1})] / (λ_{i+1} − λ_{i−1})'));
K.push(EQ('SD(λ_{i}) = [FD(λ_{i+1}) − FD(λ_{i−1})] / (λ_{i+1} − λ_{i−1})', '4.1'));
K.push(EQ('REP = argmax_{680–750 nm} FD(λ);   Dr = max_{680–750 nm} FD(λ);   SDr = Σ_{680–750 nm} FD(λ) Δλ', '4.2'));
K.push(P('REP is the red-edge position, Dr the amplitude of the red-edge peak and SDr the red-edge area (Filella and Peñuelas, 1994).'));
K.push(...tab2('hsidx', [
  ['Group', 'Index', 'Formula', 'Reference'],
  ['Chlorophyll / greenness', 'NDVI780', '(R_{780} − R_{670})/(R_{780} + R_{670})', 'Raun et al. 2001'],
  ['', 'NDVI850', '(R_{850} − R_{650})/(R_{850} + R_{650})', 'Raun et al. 2001'],
  ['', 'NDVI761', '(R_{761} − R_{651})/(R_{761} + R_{651})', 'Raun et al. 2001'],
  ['', 'SR900; SR850; SR761', 'R_{900}/R_{680};  R_{850}/R_{680};  R_{761}/R_{651}', 'Jordan 1969'],
  ['', 'GNDVI', '(R_{850} − R_{550})/(R_{850} + R_{550})', 'Gitelson et al. 1996'],
  ['', 'RDVI', '(R_{800} − R_{670})/√(R_{800} + R_{670})', 'Roujean and Bréon 1995'],
  ['', 'MSR', '(R_{800}/R_{670} − 1)/√(R_{800}/R_{670} + 1)', 'Chen 1996; Guo 2021'],
  ['', 'TVI', '0.5[120(R_{750} − R_{550}) − 200(R_{670} − R_{550})]', 'Broge and Leblanc 2001'],
  ['', 'MTVI1', '1.2[1.2(R_{800} − R_{550}) − 2.5(R_{670} − R_{550})]', 'Haboudane et al. 2004'],
  ['', 'MTVI2', '1.5[1.2(R_{800} − R_{550}) − 2.5(R_{670} − R_{550})] / √[(2R_{800} + 1)^{2} − (6R_{800} − 5√R_{670}) − 0.5]', 'Haboudane et al. 2004'],
  ['', 'MCARI1', '1.2[2.5(R_{800} − R_{670}) − 1.3(R_{800} − R_{550})]', 'Haboudane et al. 2004'],
  ['', 'TCARI', '3[(R_{700} − R_{670}) − 0.2(R_{700} − R_{550})(R_{700}/R_{670})]', 'Haboudane et al. 2002'],
  ['', 'VIgreen', '(R_{550} − R_{670})/(R_{550} + R_{670})', 'Gitelson et al. 2002'],
  ['', 'GI', 'R_{554}/R_{677}', 'Guo et al. 2021'],
  ['', 'RR', '1/R_{700}', 'Mustafa et al. 2023'],
  ['Pigment ratios', 'PSSRa; PSSRb; PSSRc', 'R_{800}/R_{680};  R_{800}/R_{635};  R_{800}/R_{470}', 'Blackburn 1998; Mahlein 2019'],
  ['', 'RARSa; RARSb; RARSc', 'R_{675}/R_{700};  R_{675}/(R_{700} × R_{650});  R_{760}/R_{500}', 'Chappelle et al. 1992'],
  ['', 'SIPI', '(R_{800} − R_{445})/(R_{800} − R_{680})', 'Peñuelas et al. 1995'],
  ['', 'NPCI', '(R_{680} − R_{430})/(R_{680} + R_{430})', 'Peñuelas et al. 1994'],
  ['', 'PSRI', '(R_{680} − R_{500})/R_{750}', 'Merzlyak et al. 1999'],
  ['', 'ARI', '1/R_{550} − 1/R_{700}', 'Gitelson et al. 2001'],
  ['', 'PPR', '(R_{550} − R_{450})/(R_{550} + R_{450})', 'Metternicht 2003'],
  ['', 'NRI', '(R_{570} − R_{670})/(R_{570} + R_{670})', 'Bausch and Duke 1996'],
  ['Photosynthesis / stress', 'PRI', '(R_{531} − R_{570})/(R_{531} + R_{570})', 'Gamon et al. 1992'],
  ['', 'NPQI', '(R_{415} − R_{435})/(R_{415} + R_{435})', 'Barnes et al. 1992'],
  ['', 'RVSI', '(R_{712} + R_{752})/2 − R_{732}', 'Merton and Huntington 1999'],
  ['', 'HI (healthy index)', '(R_{534} − R_{698})/(R_{534} + R_{698}) − 0.5 R_{704}', 'Mahlein et al. 2013'],
  ['Water', 'WI', 'R_{900}/R_{970}', 'Peñuelas et al. 1997'],
  ['', 'WI/NDVI', '(R_{900}/R_{970}) / NDVI', 'Peñuelas et al. 1997'],
  ['', 'NWI-2', '(R_{970} − R_{850})/(R_{970} + R_{850})', 'Babar et al. 2006'],
  ['SWIR disease–water (mustard)', 'DWSI-1', 'R_{800}/R_{1660}', 'Apan et al. 2004; Bhattacharya and Chattopadhyay 2013'],
  ['', 'DWSI-4', 'R_{550}/R_{680}', 'Apan et al. 2004; Bhattacharya and Chattopadhyay 2013'],
  ['', 'ROTI', 'R_{1175}/(R_{1982} + R_{691})', 'Bhattacharya and Chattopadhyay 2013'],
  ['Disease-specific', 'WRI', 'ND(λ_{1}, λ_{2}) + w R_{λ3} (Step 1.3)', 'Mahlein et al. 2013 (method)'],
], [1700, 1800, 4106, 1700], 'Hyperspectral narrow-band indices (39 indices; R_{λ} = reflectance at λ nm). The list contains the indices of the ORW slides (corrected where needed, Section 10.1) and further indices important in the reference papers (MSR, GI, RR, PSSRb/c, HI) and the mustard SWIR indices of Bhattacharya and Chattopadhyay (2013) (DWSI-1, DWSI-4, ROTI). R_{1982} lies just outside the removed 1800–1950 nm water band; ROTI is computed only if that band passes the noise check.', 15));
K.push(INCASE(`The hyperspectral sensor gives 1443 band-level features (481 reflectances, 481 first and 481 second derivatives), three red-edge parameters, 39 narrow-band indices and the White Rust Index. Band-level features are first reduced by Steps 1.2 and 1.3; indices and red-edge parameters go directly to Steps 1.4 and 1.5.`));
K.push(H3('4.1.2 Multispectral features'));
K.push(...tab2('msidx', [
  ['Feature', 'Formula (B, G, R, RE, NIR = 475, 560, 668, 717, 840 nm)', 'Reference'],
  ['Band reflectance (5)', 'Plot-mean reflectance of B, G, R, RE, NIR', 'Liu 2024; Maimaitijiang 2020'],
  ['CI_{rededge}', 'NIR/RE − 1', 'Gitelson et al. 2003'],
  ['CI_{green}', 'NIR/G − 1', 'Gitelson et al. 2003'],
  ['TCARI', '3[(RE − R) − 0.2(RE − G)(RE/R)]', 'Haboudane et al. 2002; Maimaitijiang 2020'],
  ['NDRE', '(NIR − RE)/(NIR + RE)', 'Gitelson and Merzlyak 1994; Liu 2024'],
  ['PSRI_{MS}', '(R − G)/NIR', 'Merzlyak et al. 1999, as adapted by Liu 2024'],
  ['NDVI', '(NIR − R)/(NIR + R)', 'Rouse et al. 1974'],
  ['SAVI', '1.5(NIR − R)/(NIR + R + 0.5)', 'Huete 1988'],
  ['MCARI', '[(RE − R) − 0.2(RE − G)](RE/R)', 'Daughtry et al. 2000'],
  ['MTCI', '(NIR − RE)/(RE − R)', 'Dash and Curran 2004'],
  ['GNDVI', '(NIR − G)/(NIR + G)', 'Gitelson et al. 1996'],
  ['OSAVI', '1.16(NIR − R)/(NIR + R + 0.16)', 'Rondeaux et al. 1996'],
  ['MSR', '(NIR/R − 1)/√(NIR/R + 1)', 'Chen 1996'],
  ['MS texture (40)', '8 GLCM measures (' + T('rgbfeat') + ') of each of the 5 bands', 'Liu 2024'],
  ['Percentile spectra (optional)', '20th–50th percentile reflectance of canopy pixels; Liu found them more sensitive than plot means', 'Liu 2024'],
  ['TTCI (optional)', 'Three-band texture combination indices, e.g. TTCI2 = TF_{1}/(TF_{2} × TF_{3}), optimised on training data', 'Liu 2024'],
], [2100, 4700, 2506], 'Multispectral features (12 indices of the ORW slides with corrected formulas, plus bands and texture).', 16));
K.push(H3('4.1.3 RGB features'));
K.push(...tab2('rgbfeat', [
  ['Feature', 'Equation', 'Meaning'],
  ['Mean, MEA', 'Σ_{i} Σ_{j} i P(i, j)', 'Average grey level'],
  ['Variance, VAR', 'Σ_{i} Σ_{j} (i − μ)^{2} P(i, j)', 'Spread of grey levels'],
  ['Homogeneity, HOM', 'Σ_{i} Σ_{j} P(i, j) / [1 + (i − j)^{2}]', 'Local uniformity (high for smooth canopy)'],
  ['Contrast, CON', 'Σ_{i} Σ_{j} (i − j)^{2} P(i, j)', 'Local variation (pustules, lesions)'],
  ['Dissimilarity, DIS', 'Σ_{i} Σ_{j} |i − j| P(i, j)', 'Linear version of contrast'],
  ['Entropy, ENT', '− Σ_{i} Σ_{j} P(i, j) ln P(i, j)', 'Disorder of the texture'],
  ['Second moment, SEC (energy)', 'Σ_{i} Σ_{j} P(i, j)^{2}', 'Orderliness of grey-level pairs'],
  ['Correlation, COR', 'Σ_{i} Σ_{j} (i − μ_{i})(j − μ_{j}) P(i, j) / (σ_{i} σ_{j})', 'Linear dependence of neighbouring grey levels'],
  ['Colour (3)', 'Mean hue, saturation and value of canopy pixels', 'Chlorosis and white pustules change colour (HSV features as in Mustafa 2023)'],
  ['Vegetation fraction, VF', 'canopy pixels / total plot pixels', 'Canopy cover (Maimaitijiang 2020)'],
  ['Canopy height, CH (if a bare-soil DEM exists)', 'DSM − DEM', 'Canopy structure, staghead effects (Maimaitijiang 2020)'],
], [2400, 3700, 3206], 'RGB features. GLCM measures are computed for the R, G and B bands (24 features) following Haralick et al. (1973), Feng et al. (2022) and Liu et al. (2024).', 16));
K.push(P('In the GLCM equations, i and j are **grey levels** (the row and column indices of the co-occurrence matrix, not image row and column numbers), P(i, j) is the normalised frequency with which grey levels i and j occur in two pixels separated by distance d in direction θ, and μ and σ are the GLCM mean and standard deviation (Haralick et al., 1973). Settings: d = 1 pixel, averaged over θ = 0°, 45°, 90° and 135° (Guo et al., 2021), 3 × 3 window (ORW), and the same number of grey levels for every flight.'));
K.push(H3('4.1.4 Thermal features'));
K.push(P('The canopy temperature CT is the mean temperature of canopy pixels after K-means segmentation (Feng et al., 2022); AT is the air temperature at the time of the flight.'));
K.push(EQ('CTD = CT − AT;    CTR = (CT + 273.15) / (AT + 273.15)'));
K.push(EQ('NRCT = (CT − CT_{min}) / (CT_{max} − CT_{min});    MTD = T_{max} − T_{min}', '4.3'));
K.push(...tab2('tirfeat', [
  ['Feature', 'Description', 'Reference'],
  ['CT', 'Mean canopy temperature (°C)', 'Liu 2024'],
  ['CTD', 'Canopy minus air temperature; reduces the effect of weather', 'Feng 2022'],
  ['CTR', 'Canopy-to-air temperature ratio, computed in kelvin (a ratio of °C values depends on the temperature scale)', 'Feng 2022 (kelvin: this study)'],
  ['NRCT', 'Normalised relative canopy temperature; CT_{min} and CT_{max} are the lowest and highest canopy temperatures in the same thermal image', 'Feng 2022; Maimaitijiang 2020'],
  ['MTD', 'Maximum minus minimum canopy temperature within the plot', 'Mahlein 2019'],
  ['Thermal texture (8)', 'GLCM measures of the temperature image after quantisation to a fixed number of grey levels over one common temperature range for all flights; d = 1 pixel, θ = 0°, 45°, 90°, 135°', 'Maimaitijiang 2020 (texture of the thermal layer); Haralick et al. 1973'],
], [1900, 5000, 2406], 'Thermal features (13).', 16));

K.push(...STEPEND(`A feature table per sensor and plot-date: HS 1443 band-level features + 3 red-edge parameters + 39 indices (+ WRI after Step 1.3); MS 57 features; RGB 29 features; TIR 13 features.`, [
  `**Continuous wavelet transform features** of the spectra (Tian et al., 2021; Lv et al., 2023).`,
  `**Continuum removal and band-depth features** of absorption regions (Kokaly and Clark, 1999).`,
  `**Radiative-transfer inversion** (PROSPECT + SAIL) to retrieve chlorophyll, water and LAI as features (Jacquemoud et al., 2009).`,
  `**Other texture descriptors** such as local binary patterns (Ojala et al., 2002) or three-band texture combination indices (Liu et al., 2024).`,
  `**Crop water stress index** from canopy temperature and reference surfaces (Idso et al., 1981; Jackson et al., 1981); **solar-induced fluorescence** from very-high-resolution spectrometers (Mohammed et al., 2019).`
]));
// ---- Step 1.2 HS band level ----
K.push(H2('4.2 Step 1.2: Hyperspectral band-level analysis (HS only)'));
K.push(P('Hyperspectral data contain 1443 band-level features (481 reflectance + 481 FD + 481 SD), far more than the number of plots. Band-level analysis therefore identifies a few robust bands before modelling. It is needed only for HS: the MS has five bands, and RGB and TIR features are not spectral bands. Because severity classes overlap, two complementary methods are combined (' + F('step12') + '): a correlation scalogram against DI, which needs no class boundaries (Cheng et al., 2010), and ReliefF, which is designed for noisy, overlapping, multi-class data (Robnik-Šikonja and Kononenko, 2003; Mahlein et al., 2013). JM distance only reports class overlap.'));
K.push(...fig2('step12', 'f7_step12.png', 'Sub-steps of the hyperspectral band-level analysis. Schematic curves are illustrations; real curves come from the UAV hyperspectral data.', 540));
K.push(LBL('Sub-step A. Data'));
K.push(BL('Pooled post-symptomatic plot-dates, including healthy plots; reflectance, FD and SD of all retained bands; targets: DI for sub-step B, health status (detection) and the three severity classes (severity) for sub-steps C and E.'));
K.push(BL('For the description in Objective 1 all IARI data are used. When selected bands become model inputs (Objectives 2 and 3), sub-steps B–D are repeated inside the training data of each cross-validation fold so that test plots never influence band selection (Ambroise and McLachlan, 2002; Varma and Simon, 2006).'));
K.push(LBL('Sub-step B. Correlation scalograms against DI (reflectance, FD, SD)'));
K.push(BL('For each band λ, Spearman\'s rank correlation ρ(λ) between the feature (R, FD or SD) and DI is computed over all samples (Spearman, 1904). Because many healthy plots share DI = 0, ρ is computed as the Pearson correlation of the ranks (Eq. 4.4); Pearson\'s r is reported alongside (Guo et al., 2021; Feng et al., 2022; Liu et al., 2024).'));
K.push(EQ('ρ(λ) = Σ (u_{i} − ū)(v_{i} − v̄) / √[ Σ (u_{i} − ū)^{2} Σ (v_{i} − v̄)^{2} ],   u_{i} = rank of the feature,  v_{i} = rank of DI_{i}', '4.4'));
K.push(BL('ρ(λ) is plotted against wavelength for R, FD and SD (three scalograms; Cheng et al., 2010). Bands with p < 0.01 (Guo et al., 2021) and in the top 5% of |ρ| (Tian et al., 2021) are retained; one band with the highest |ρ| is kept per spectral region (Tian et al., 2021), regions being defined from the band-to-band correlation matrix (Section 4.2.1). Repeated plot-dates make p-values optimistic, so bands are ranked mainly by |ρ|.'));
K.push(BL('Stability: the scalograms are repeated for replications R1, R2 and R3 separately; regions found in all three are stable.'));
K.push(INCASE(`For each of the 481 retained bands, ρ is computed three times (R, FD, SD), giving three curves of ρ against wavelength. A typical expectation is a negative ρ for reflectance in the NIR (DI up, NIR down), a positive ρ in the red and SWIR (DI up, reflectance up) and strong FD correlations along the red edge (690–740 nm), where the blue shift of the red edge changes the slope. The highest |ρ| band of each significant region is kept, giving perhaps 10–20 robust bands instead of 1443 band features.`));
K.push(BL('Common regions: regions significant in all three scalograms (R, FD and SD) are reported as common sensitive regions, as in the mustard aphid study of Shukla et al. (2024: 483–487, 509–515, 690–714 and 719–723 nm). Comparing the white rust regions with these shows whether white rust has a spectral signature different from aphid damage in the same crop.'));
K.push(LBL('Sub-step C. ReliefF relevance spectra (detection and severity)'));
K.push(BL('ReliefF is run twice: with health status (detection) and with the three severity classes (severity discrimination). For each sample x, its k nearest neighbours of the same class (hits H) and of every other class C (misses M) are found; a band gains weight when it differs between x and its misses and loses weight when it differs between x and its hits (Eq. 4.5; Robnik-Šikonja and Kononenko, 2003).'));
K.push(EQ('W(λ) ← W(λ) − Σ_{j=1}^{k} diff(λ, x, H_{j}) / (m k)'));
K.push(EQ('+ Σ_{C ≠ c(x)} [ P(C) / (1 − P(c(x))) ] Σ_{j=1}^{k} diff(λ, x, M_{j}(C)) / (m k)', '4.5'));
K.push(P('where diff(λ, x, y) = |value of x − value of y| / (range of band λ), m = number of samples, k = number of neighbours (10), c(x) = class of x and P(C) = prior probability of class C. Neighbours from the same plot (other flights) are excluded as near-duplicates. The top 5% of bands are retained with one per region.'));
K.push(LBL('Sub-step D. Robust white-rust bands'));
K.push(BL('Regions from B and C within about ±10 nm are treated as the same (' + T('consensus') + '). Robust bands are interpreted against known absorption features: chlorophyll near 550 and 670–700 nm (PSSRa/b, Mahlein 2019; 1/R_{700}, Mustafa 2023), red edge 700–740 nm, leaf structure in the NIR (750–900 nm) and water near 970, 1180, 1650 and 2200 nm.'));
K.push(...tab2('consensus', [
  ['Group', 'Meaning', 'Use'],
  ['Selected by both methods', 'Changes steadily with severity and separates classes locally', 'Robust bands for detection and severity; added to the HS DSF candidates'],
  ['Correlation only', 'Steady trend with DI but weak class separation', 'Mainly useful for DI regression'],
  ['ReliefF only', 'Non-linear or class-specific response', 'Mainly useful for classification'],
], [2600, 3600, 3106], 'Interpretation of bands selected by the correlation scalograms and ReliefF.', 17));
K.push(LBL('Sub-step E. Jeffries–Matusita distance (reporting only)'));
K.push(BL('With the few robust bands, the Bhattacharyya distance B and the JM distance are computed between every pair of the four groups healthy, Low, Moderate and High (6 pairs; Richards, 2013; Schmidt and Skidmore, 2003):'));
K.push(EQ('B_{ij} = (1/8)(μ_{i} − μ_{j})^{T} Σ^{−1} (μ_{i} − μ_{j}) + (1/2) ln[ |Σ| / √(|Σ_{i}| |Σ_{j}|) ],   Σ = (Σ_{i} + Σ_{j})/2'));
K.push(EQ('JM_{ij} = 2 [1 − exp(−B_{ij})]', '4.6'));
K.push(P('JM ranges from 0 (complete overlap) to 2 (complete separation); ≥ 1.9 indicates good separability. JM shows which classes overlap and explains classification errors; it is not used to select bands because it assumes normally distributed classes.'));
K.push(LBL('Sub-step F. PCA and PLSR loading weights for discriminating severity classes (Shukla et al., 2024)'));
K.push(BL(`**What:** identify the bands that carry most of the difference between healthy plots and the severity classes from the loading weights of principal component analysis (PCA) and partial least squares (PLS) models of the reflectance spectra, as Shukla et al. (2024) did to discriminate the five aphid infestation severity grades of mustard.`));
K.push(BL(`**How:** PCA is run on the smoothed plot-mean reflectance (all retained bands) of healthy and diseased plot-dates; a PLS model is fitted with DI (and, as PLS discriminant analysis, with dummy-coded health status and severity classes) as the response. The loading weights of the first three principal components and of the first three PLS factors are plotted against wavelength; bands at their local maxima and minima are the dominant bands for discriminating the classes (Shukla et al., 2024, found 500, 679, 746 and 979 nm by PCA and 491, 679, 746 and 979 nm by PLSR).`));
K.push(BL(`**Use:** a check on the robust bands of Sub-step D. Bands selected by the scalograms or ReliefF that also appear as loading extremes are the most reliable white-rust bands; comparing them with the aphid bands of Shukla et al. (2024) shows whether white rust and aphid damage of mustard have different spectral signatures. As in Sub-steps B–D, the loadings are recomputed inside the training data when bands become model inputs.`));

K.push(H3('4.2.1 How the correlation between neighbouring bands is handled'));
K.push(LBL('Concept'));
K.push(P(`Reflectance changes smoothly with wavelength because the same absorbers (chlorophyll, water, dry matter) and the same leaf and canopy structure control many neighbouring bands; in addition, the spectral response of each detector element is wider than the band spacing, and Savitzky–Golay smoothing averages neighbouring bands. Neighbouring hyperspectral bands are therefore almost duplicates of each other — **multicollinearity** or **spectral redundancy** (Thenkabail et al., 2004; Shukla et al., 2024). ${F('bandcorr')} quantifies it with the ground ASD spectra of mustard leaves measured in the IARI experiment on 3 March 2026 (648 spectra: 108 healthy, 540 diseased), smoothed and resampled to 5 nm after removing the water-absorption regions (349 bands). Bands 10 nm apart have a median correlation of r = 0.9997 (98% of pairs above 0.95), and even bands 50 nm apart have a median r = 0.993 (82% above 0.95); 24% of all band pairs have |r| > 0.9. First derivatives are far less redundant (median r = 0.95 at 10 nm and 0.49 at 50 nm).`));
K.push(...fig2('bandcorr', 'n8_bandcorr.png', 'Spectral redundancy in the mustard ASD leaf spectra of the IARI experiment (3 March 2026; 648 spectra, Savitzky–Golay smoothed, 5 nm, water bands removed): (a) band-to-band correlation of reflectance; (b) of first-derivative spectra; (c) correlation of each band with the band 5, 10, 20 and 50 nm further. Large dark-red blocks in (a) are groups of interchangeable bands.', 560));
K.push(LBL('Why it is a problem at this position'));
K.push(BL(`**Too many effective duplicates (Hughes phenomenon):** 1443 band features carry the information of only a few tens of independent variables, but a model sees them all and overfits (Section 8.2.1).`));
K.push(BL(`**Unstable linear models:** in multiple regression, LDA and canonical discriminant analysis the coefficients of collinear bands become large, opposite in sign and unstable, and the within-class covariance matrix becomes singular, so Wilks' lambda, JM and Mahalanobis distances cannot be computed (Dormann et al., 2013).`));
K.push(BL(`**Misleading rankings:** correlation scalograms and ReliefF give similar values to all bands of a block, so a "top 5%" list is filled with neighbours of one feature; random-forest importance is shared between correlated bands (Strobl et al., 2007).`));
K.push(LBL('Region rule used in this thesis'));
K.push(P(`To make "one band per spectral region" objective, regions are defined from the band-to-band correlation matrix of the training data: starting at the shortest wavelength, a region is extended band by band as long as each new band correlates with the first band of the region at r ≥ 0.95, and it always breaks at a removed water band. The rule is applied separately to reflectance, first and second derivatives. Applied to the ASD data of ${F('bandcorr')}, the 349 reflectance bands collapse into only **18 regions** (for example 400–430, 435–505, 645–695, 700–710, 735–845, 850–1090 and 1540–1795 nm), whereas the first derivatives form 161 regions. Narrow regions occur where reflectance changes fastest (the red edge, 700–730 nm), broad ones on the NIR plateau and in the SWIR. From each region only the band with the highest |ρ|, ReliefF weight or loading is kept.`));
K.push(...tab2('mcol', [
  ['Stage (section)', 'How redundancy is handled in this thesis', 'How other researchers handled it'],
  ['Pre-processing (3.5, 8.3.1)', 'Savitzky–Golay smoothing; noisy and water bands removed; region rule computed on smoothed spectra', 'Mahlein et al. (2013) reduced the spectral resolution to 6 nm "due to high correlation between neighboring wavelengths"; Shukla et al. (2024) removed noisy regions and used SG derivatives'],
  ['Band-level analysis (4.2)', 'One band per correlation region (r ≥ 0.95) from scalograms, ReliefF and PCA/PLSR loadings; regions within ±10 nm across methods merged', 'Tian et al. (2021) kept "only one representative feature with the highest separability within each common feature region"; Bhattacharya and Chattopadhyay (2013) used "single bands out of multiple closely located bands"'],
  ['Derivatives and indices (4.1)', 'FD, SD and band contrasts (ratios, normalised differences) used because they are much less correlated than raw reflectance (Fig. above, panel b)', 'Lv et al. (2023) combined first derivatives with bands, indices and wavelets; Ramalingam et al. (2026) quantified redundancy with lagged and spectral autocorrelation'],
  ['White Rust Index (4.3)', 'Spectra averaged to 6 nm; minimum distance of 50 nm between combined bands', 'Mahlein et al. (2013): 6 nm resolution and 50 nm minimal distance in normalised differences'],
  ['Relevance (4.5)', 'Boruta keeps correlated relevant features by design; redundancy is passed to the next step', 'Mustafa et al. (2023) followed Boruta by VIF'],
  ['Redundancy filter (5.1)', 'VIF < 10, iteratively removing the most collinear feature, before ML-SFFS, PLSR, DNNs and discriminant analysis', 'Tian et al. (2021) and Mustafa et al. (2023): VIF < 10 before ML-SFFS'],
  ['Subset search (5.1)', 'ML-SFFS drops a feature that adds nothing once a correlated partner is in the subset', 'Tian et al. (2021): 2–4 features enough; Zhu et al. (2017) and Huang et al. (2020) used SPA, which selects wavelengths with minimum collinearity (Araújo et al., 2001)'],
  ['Stepwise discriminant analysis (4.6.1)', 'Input restricted to region-representative bands; Wilks\' lambda entry and removal criteria', 'Bhattacharya and Chattopadhyay (2013): two-step stepwise canonical discriminant analysis'],
  ['Models (5.4, 8.6)', 'PLSR (latent components), SVM (regularisation C), RF (robust predictions; importance interpreted only on the final small set)', 'Shukla et al. (2024) and Krishna et al. (2014): PLS on full spectra with loading weights to pick a few bands; Zhang et al. (2012a): PLSR better than MLR'],
], [1900, 3500, 3906], 'How the correlation between neighbouring hyperspectral bands is handled in this thesis and in the reference studies.', 15));
K.push(INCASE(`For the UAV hyperspectral data the same analysis is run on the plot-mean spectra of the training replications: the band-to-band correlation matrix is computed, the regions are defined with r ≥ 0.95, and every band-level selection keeps one band per region. In the ASD example, 349 bands reduce to 18 regions, so at most 18 reflectance bands (plus derivative bands) can enter the next steps before VIF and ML-SFFS reduce them further. Canopy-level UAV spectra are expected to be at least as redundant as leaf spectra because of the wider spectral response of the imaging sensor and the mixing of leaves, shadow and soil.`));
K.push(...STEPEND(`The band-to-band correlation matrix and its heat map, the correlation regions (r ≥ 0.95) for reflectance, first and second derivatives, and the rule that only one band per region enters later steps.`, [
  `**Principal component analysis** or the **minimum noise fraction transform**, which turn correlated bands into uncorrelated components but lose band-level interpretation (Jolliffe, 2002; Green et al., 1988).`,
  `**Band binning** to a coarser spectral resolution (6 nm in Mahlein et al., 2013).`,
  `**Wavelength selection designed against collinearity**: SPA (Araújo et al., 2001) or CARS (Li et al., 2009).`,
  `**Shrinkage regression** — ridge, LASSO or elastic net — which keeps or selects correlated bands with penalised coefficients (Hoerl and Kennard, 1970; Tibshirani, 1996; Zou and Hastie, 2005).`,
  `**Redundancy diagnostics** such as lagged correlation and spectral autocorrelation (Ramalingam et al., 2026).`
]));
K.push(LBL('Interview questions on this step'));
QA('Why are neighbouring hyperspectral bands correlated?', 'Because the same pigments, water and structure control reflectance over broad wavelength ranges, the sensor\'s spectral response is wider than the band spacing, and smoothing averages neighbours. In my mustard ASD data, bands 10 nm apart have median r = 0.9997.');
QA('How did you define a spectral region for the one-band-per-region rule?', 'Objectively from the band-to-band correlation matrix of the training data: a region extends while each band correlates with its first band at r ≥ 0.95, separately for reflectance and derivatives. In my ASD data 349 reflectance bands form 18 regions.');
QA('Does random forest not handle collinearity anyway?', 'Its predictions are robust, but its importance is shared between correlated bands, so the ranking is misleading (Strobl et al., 2007). That is why VIF and ML-SFFS precede interpretation, and importance is read only for the final small feature set.');
K.push(...STEPEND(`Correlation scalograms of R, FD and SD vs DI; ReliefF relevance spectra for detection and severity; correlation regions (r ≥ 0.95); a short list of robust white-rust bands (one per region, typically 10–20); PCA/PLSR loading curves; JM distances between the four groups.`, [
  `**Separability scalograms** with class thresholds (Tian et al., 2021), suited to non-overlapping stages.`,
  `**Successive projections algorithm (SPA)** (Araújo et al., 2001; Zhu et al., 2017) or **competitive adaptive reweighted sampling (CARS)** (Li et al., 2009) for wavelength selection.`,
  `**Variable importance in projection (VIP)** from PLS (Wold et al., 2001; Chong and Jun, 2005).`,
  `**Random-forest impurity ranking** of bands (Ramalingam et al., 2026) or **CART** (Das et al., 2020).`,
  `**Minimum-redundancy maximum-relevance (mRMR)** selection based on mutual information (Peng et al., 2005).`
]));
// ---- Step 1.3 WRI ----
K.push(H2('4.3 Step 1.3: White Rust Index (HS only)'));
K.push(...STEP('White Rust Index (WRI)',
  'Build one index specific to white rust from the UAV hyperspectral data.',
  'General vegetation indices also respond to nutrient or water stress; a disease-specific index of three bands reduces this confusion (Mahlein et al., 2013).',
  ['Data: healthy vs diseased plot-dates of the training data, 450–950 nm (range of Mahlein et al., 2013), averaged to 6 nm because neighbouring wavelengths are highly correlated (Mahlein et al., 2013; Section 4.2.1); the search is repeated with SWIR bands added (below).',
   'ReliefF ranks all single bands and all two-band normalised differences ND(λ_{1}, λ_{2}) = (R_{λ1} − R_{λ2})/(R_{λ1} + R_{λ2}); the top 25% of each are retained.',
   'All combinations of Eq. 4.7, with a minimum distance of 50 nm between combined bands (Mahlein et al., 2013), are tested exhaustively with an optimised threshold; the combination with the highest balanced accuracy in 8-fold stratified cross-validation is the WRI (Mahlein et al., 2013).',
   'The search is repeated with SWIR bands added (retained bands up to 2500 nm), because SWIR bands were the most sensitive to Sclerotinia rot in mustard and the three-band ROTI (red, NIR and SWIR) beat two-band indices (Bhattacharya and Chattopadhyay, 2013). The VNIR and VNIR + SWIR indices are compared and the better one is kept as the WRI.'],
  'Mahlein et al. (2013). Example of this form: sugar beet rust index = (R570 − R513)/(R570 + R513) + 0.5 × R704.'));
K.push(EQ('WRI = (R_{λ1} − R_{λ2}) / (R_{λ1} + R_{λ2}) + w R_{λ3},    w ∈ {−1, −0.5, 0, 0.5, 1}', '4.7'));
K.push(P(`Each candidate index is used as a one-feature classifier with an optimised threshold t (a plot-date is called diseased if WRI > t, or < t for indices that decrease with disease). Because healthy and diseased plot-dates are not equally frequent, the criterion is **balanced accuracy**:`));
K.push(EQ('BA = (sensitivity + specificity) / 2 = [ TP/(TP + FN) + TN/(TN + FP) ] / 2', '4.8'));
K.push(INCASE(`Suppose ReliefF retains 60 single bands and 300 normalised differences. Every ND is combined with every single band and each of the five weights w, giving 60 × 300 × 5 = 90 000 candidate indices; each is evaluated by 8-fold stratified cross-validation, which takes minutes on a desktop computer. The winning combination, for example a normalised difference between a green and a red-edge band plus a weighted NIR band, is the WRI; it is then tested on the held-out replication like any other feature.`));

K.push(...STEPEND(`The White Rust Index formula (two bands of a normalised difference, a weighted third band, the weight w and the threshold), its balanced accuracy, and a VNIR-only and a VNIR + SWIR version.`, [
  `**Exhaustive two-band ratio, difference and normalised-difference searches** shown as correlation contour maps (Shukla et al., 2024, used RSI, DSI and NDSI).`,
  `**Separate detection and severity indices** (health index and severity index; Meng et al., 2020).`,
  `**Indices from random-forest-selected bands** with over a million combinations tested (Ramalingam et al., 2026).`,
  `**Three-band ratio indices** of the ROTI type, R_{a}/(R_{b} + R_{c}) (Bhattacharya and Chattopadhyay, 2013).`
]));
// ---- Step 1.4 statistics ----
K.push(H2('4.4 Step 1.4: Statistical characterisation (all sensors)'));
K.push(P('The same statistical tests are applied to every feature of every sensor, separately for detection and for severity (' + T('statsdesign') + '). Repeated plot-dates make p-values optimistic, so tests are used to describe and rank features; generalisation is judged only by the validation of Objectives 2 and 3.'));
K.push(...tab2('statsdesign', [
  ['Question', 'Detection (healthy vs diseased)', 'Severity (healthy, Low, Moderate, High)', 'Reference'],
  ['Does the feature differ between groups?', 'Independent t-test if normal with equal variances, else Mann–Whitney U test', 'One-way ANOVA + Tukey HSD if normal with equal variances, else Kruskal–Wallis + Dunn test', 'Tian 2021; Mahlein 2019; Mann and Whitney 1947; Kruskal and Wallis 1952; Tukey 1949; Dunn 1964'],
  ['Are assumptions met?', 'Shapiro–Wilk (normality), Levene (equal variances)', 'Same', 'Shapiro and Wilk 1965; Levene 1960'],
  ['How strongly is the feature related to severity?', 'Point-biserial correlation (Pearson r with 0/1 status)', 'Spearman ρ and Pearson r with DI', 'Guo 2021; Feng 2022; Liu 2024'],
  ['What physiology does it reflect?', 'Correlation with chlorophyll, carotenoid, anthocyanin, RWC, stomatal conductance, transpiration', 'Same; plus ANOVA/Tukey of physiological parameters across severity groups', 'Tian 2021; Mustafa 2023; ORW Act. 1.2'],
], [2100, 2500, 2700, 2006], 'Statistical characterisation of each feature for detection and for severity.', 15));
K.push(...tab2('stats', [
  ['Technique', 'Where used'],
  ['t-test / Mann–Whitney U', 'Detection (Objective 1); pre-symptomatic screening (Objective 3)'],
  ['ANOVA + Tukey HSD / Kruskal–Wallis + Dunn', 'Severity groups (Objective 1); model errors across varieties (Objective 2)'],
  ['Pearson / Spearman correlation', 'Features vs DI and physiology (Objective 1); correlation scalograms (HS)'],
  ['Canonical discriminant analysis (stepwise, Wilks\' lambda)', 'Multivariate separation of healthy, Low, Moderate and High per sensor (Objective 1)'],
  ['PCA and PLSR loading weights', 'Hyperspectral bands that discriminate severity classes (Objective 1, Step 1.2; Shukla et al., 2024)'],
  ['Variance inflation factor', 'Collinearity before ML-SFFS (Objectives 2 and 3)'],
], [3800, 5506], 'Summary of statistical techniques.', 17));
K.push(...fig2('statstree', 'n6_stats_tree.png', 'Choice of statistical test for one feature: two groups (detection) or three or more groups (severity), parametric or rank-based depending on normality and equal variances.', 500));
K.push(INCASE(`Take canopy–air temperature difference (CTD) as an example. For detection, Shapiro–Wilk may show that CTD is skewed in diseased plots, so the Mann–Whitney U test compares healthy and diseased plot-dates; a significant result with diseased plots warmer supports H1. For severity, Kruskal–Wallis tests whether CTD differs among healthy, Low, Moderate and High; Dunn's post-hoc test then shows which pairs differ (for example healthy ≠ Low, but Moderate ≈ High). Spearman ρ between CTD and DI measures the strength of the trend, and correlation with stomatal conductance explains it. The same procedure is applied to all features of all sensors and summarised in one table per sensor.`));

K.push(...STEPEND(`One table per sensor: mean ± SD of every feature for healthy, Low, Moderate and High; test statistics and adjusted p-values; significant pairs; Spearman ρ with DI; correlations with physiological parameters.`, [
  `**Linear mixed models** with plot as a random effect, which handle repeated plot-dates correctly (Zuur et al., 2009).`,
  `**False discovery rate** control instead of family-wise correction when many features are tested (Benjamini and Hochberg, 1995).`,
  `**Effect sizes** such as Cohen's d alongside p-values (Cohen, 1988).`,
  `**MANOVA** to test all features of a sensor jointly (Huberty and Olejnik, 2006).`
]));
// ---- Step 1.5 ML relevance ----
K.push(H2('4.5 Step 1.5: Machine-learning relevance (all sensors)'));
K.push(...STEP('Boruta relevance per sensor and task',
  'Identify the disease-specific features (DSFs) of each sensor, separately for detection, severity discrimination and DI.',
  'Statistics test one feature at a time; Boruta, built on random forest, also captures non-linear and interacting relevance and keeps every relevant feature without an arbitrary cut-off (Kursa and Rudnicki, 2010). Mustafa et al. (2023) used Boruta to select disease-specific features before ML-SFFS.',
  ['Input: all features of one sensor (for HS: the robust bands of Step 1.2, red-edge parameters, indices and WRI).',
   'Each feature is copied and shuffled ("shadow" features). A random forest is fitted on real and shadow features; the importance (Z-score of mean decrease in accuracy) of each real feature is compared with the best shadow feature over repeated runs (e.g. 100); features significantly more important are "confirmed", significantly less important are "rejected", the rest "tentative" (Kursa and Rudnicki, 2010).',
   'Run three times per sensor: classification with health status (detection), classification with the three severity classes (diseased plot-dates), and regression with DI.',
   'Output: importance boxplots and a table of confirmed / tentative / rejected features per sensor and task; confirmed features form the DSF pool of that sensor and task.'],
  'Mustafa et al. (2023); Kursa and Rudnicki (2010).'));
K.push(INCASE(`For the multispectral sensor, Boruta receives all 57 features (5 bands, 12 indices, 40 textures). For detection it may confirm, for example, the red-edge and NIR bands, NDRE, CIrededge, PSRI and a few red-edge textures, reject most blue-band textures and leave some tentative. The confirmed set is the MS detection DSF pool. The same is done for severity (diseased plot-dates, three classes) and for DI (regression), and for the other three sensors, giving 12 DSF pools.`));
K.push(...STEP('Univariate regression of each DSF against DI',
  'Measure how well each DSF alone tracks severity.',
  'A simple, interpretable ranking that complements Boruta (Mustafa et al., 2023; Feng et al., 2022).',
  'Linear regression DI = a + b x for each DSF x; R^2 and RMSE are reported (Eq. 4.9).',
  'Mustafa et al. (2023): best single feature 1/R700, R^2 = 0.81; Feng et al. (2022): single index R^2 < 0.56.'));
K.push(EQ('DI_{i} = a + b x_{i} + ε_{i};    R^{2} = 1 − Σ (DI_{i} − DÎ_{i})^{2} / Σ (DI_{i} − mean DI)^{2}', '4.9'));

K.push(...STEPEND(`Twelve DSF pools (4 sensors × detection, severity, DI) listing confirmed, tentative and rejected features with importance plots, and the univariate R^{2} and RMSE of each DSF against DI.`, [
  `**Recursive feature elimination** with SVM or RF (Guyon et al., 2002), as used by Liu et al. (2024).`,
  `**LASSO or elastic-net** regression, which select features while fitting (Tibshirani, 1996; Zou and Hastie, 2005).`,
  `**SHAP values** to rank features by their contribution to model predictions (Lundberg and Lee, 2017).`,
  `**Permutation importance** of a tuned model instead of the shadow-feature test (Breiman, 2001).`
]));
// ---- Step 1.6 cross-sensor ----
K.push(H2('4.6 Step 1.6: Cross-sensor characterisation'));
K.push(BL('**Cross-sensor correlation matrix:** Pearson correlation among the DSFs of all four sensors and with DI. Low correlation between sensors means complementary information and justifies fusion (approach of Mahlein et al., 2019, who correlated thermal, fluorescence and spectral parameters with each other and with disease severity).'));
K.push(BL('**JM distance per sensor:** JM between healthy, Low, Moderate and High computed with the few top DSFs of each sensor (Eq. 4.6), giving one comparable measure of how well each sensor separates the severity groups (Richards, 2013).'));
K.push(INCASE(`If, for example, the HS index PSSRa and the TIR feature CTD are both strongly related to DI but only weakly correlated with each other (|r| < 0.5), they carry different information — pigment loss and transpiration loss — and fusing them is expected to help (Hypothesis H2). If the DSFs of two sensors are highly correlated, one sensor may be enough. JM distance computed with the top three DSFs of each sensor then ranks the sensors by how well they separate healthy, Low, Moderate and High.`));
K.push(H3('4.6.1 Disease-class discrimination adapted from Stage III of Bhattacharya and Chattopadhyay (2013)'));
K.push(P(`Stage III of the multi-stage tracking of mustard Sclerotinia rot (Bhattacharya and Chattopadhyay, 2013) is the part of that study that discriminates disease classes from hyperspectral data: rot-incidence groups are related to Hyperion reflectance through a **two-step stepwise canonical discriminant analysis** — first to select bands, then to screen indices built from them — and the best index is thresholded to map diseased patches. The same logic is applied here, as a multivariate characterisation of how well each sensor separates healthy, Low, Moderate and High plots, with the changes needed for UAV plot data (${T('stage3')}). Each step below gives its concept, why it is needed at this position, its importance, how it is used with the white rust data, and likely interview questions. The equations are in Section 8.5.6.`));
K.push(...tab2('stage3', [
  ['Step', 'Bhattacharya and Chattopadhyay (2013), Stage III', 'This thesis (UAV, white rust)'],
  ['III.1 Disease groups', 'Rot incidence at 16 sites grouped into five levels (5, 15, 30, 35, 45%)', 'Healthy (DI = 0), Low (≤ 25%), Moderate (25–50%), High (> 50%); healthy vs diseased for detection'],
  ['III.2 Spectrum per observation', 'Mean of 3 × 3 Hyperion pixels (30 m) around each GPS point', 'Mean of pure canopy pixels inside the plot buffer, per plot-date'],
  ['III.3 First discriminant step', 'Stepwise canonical discriminant analysis on band reflectances; 25 bands with canonical correlation > 0.5', 'Same, on the region-representative robust bands of Step 1.2 (one per correlated region)'],
  ['III.4 Response curves', 'Group-mean reflectance of selected bands vs group-mean incidence; SWIR bands most sensitive (R^{2} 0.74–0.95)', 'Class means and plot-level Spearman ρ of each selected band with DI'],
  ['III.5 Candidate indices', '224 new band combinations + 30 published indices (Apan et al., 2004); one band from each cluster of close bands', 'Ratios, normalised differences and three-band forms of selected bands (≥ 50 nm apart) + 39 published indices + WRI'],
  ['III.6 Second discriminant step', 'Stepwise analysis on indices, ranked by canonical correlation; DWSI-1, DWSI-4, DRI, ROTI kept; ROTI recommended', 'Same, after VIF; top indices added to the HS DSF pool; single step for MS, RGB and TIR features'],
  ['III.7 Thresholds and maps', '1.25 < DRI ≤ 3.5 and 0 < ROTI ≤ 1.5 (observed incidence limits ± 10%); LISS-IV crop mask; maps of 7 Jan and 24 Feb 2005', 'Class thresholds or discriminant boundaries from training replications; plot-level class maps of the held-out replication'],
  ['III.8 Validation', 'Indirect: lower fractional canopy cover in the disease year (2005) than in a normal year (2007)', 'Direct: leave-one-replication-out against ground DI; Bharatpur and farmers\' fields'],
], [1700, 3700, 3906], 'Stage III of Bhattacharya and Chattopadhyay (2013) and its adaptation in this thesis.', 15));
K.push(...STAGE('Step III.1 Define the disease groups (grouping variable)',
  'Discriminant analysis needs a categorical grouping variable: every sample must belong to one known class, and the method finds the feature combinations that separate these classes.',
  'It is the first step because all later steps (band selection, index ranking, thresholds) are judged by how well they separate these groups; the groups must match the decisions the thesis wants to make (detection and three severity classes).',
  'Badly chosen groups make discrimination meaningless. Bhattacharya and Chattopadhyay (2013) grouped incidence into five levels and used group means, which "normalizes the under or over representation of disease incidence levels".',
  'Post-symptomatic plot-dates are labelled healthy, Low, Moderate or High from the plot DI (Section 3.3); a second analysis uses healthy vs diseased. Class sizes are unequal, so equal prior probabilities are used, and analyses are fitted inside the training replications only.',
  [['Why use classes when DI is continuous?', 'Management decisions are made by class (no action, monitor, spray), and discriminant analysis needs groups. DI regression is done in parallel, so no information is lost.'],
   ['Why equal priors?', 'With proportional priors the rare High class would be under-predicted; equal priors give every class the same chance, consistent with the use of macro-F1.']], `Each post-symptomatic plot-date labelled healthy, Low, Moderate or High (and healthy/diseased), with class counts and the chosen priors.`, [
    `**Ordinal regression** that keeps the order of the classes (McCullagh, 1980).`,
    `**Continuous DI regression** without classes (Section 5.3; Liu et al., 2024).`,
    `**Clustering-based groups** (e.g. K-means on DI) instead of fixed limits (MacQueen, 1967).`]));
K.push(...STAGE('Step III.2 Extract one spectrum per observation',
  'Each ground observation must be represented by one reliable spectrum: an average over several pixels reduces sensor noise and positional error.',
  'It comes before any analysis because noisy or mixed spectra would make the class separation look worse (or better) than it is.',
  'Bhattacharya and Chattopadhyay (2013) used the mean of 3 × 3 Hyperion pixels centred on each GPS location, which absorbs geolocation error at 30 m resolution.',
  'For each plot-date the mean of pure canopy pixels inside the 0.5 m inner buffer is used (after the canopy mask), which for the SWIR is about 5 × 5 pixels and for the VNIR many more (Section 3.5).',
  [['Why not use individual pixels as samples?', 'Pixels of one plot share the same DI label and are strongly correlated; treating them as independent samples would inflate the sample size and the significance. The plot is the experimental unit.']], `One spectrum (and one value per feature) per plot-date from pure canopy pixels.`, [
    `**Median or percentile spectra** of canopy pixels, which are less sensitive to outliers (Liu et al., 2024).`,
    `**Pixel-level classification** of diseased pixels and the diseased-pixel fraction per plot (Abdulridha et al., 2019).`,
    `**Outlier removal** of spectra with an isolation forest before averaging (Ramalingam et al., 2026; Liu et al., 2008).`]));
K.push(...STAGE('Step III.3 First discriminant step: select discriminating bands',
  'Stepwise canonical discriminant analysis with band reflectances as predictors: at each step the band that most reduces Wilks\' lambda (Eq. 8.13) is entered, and bands that no longer contribute are removed. Canonical correlation measures how strongly the discriminant function is related to the groups.',
  'It follows the band-level reduction of Step 1.2 because stepwise discriminant analysis cannot be run on hundreds of collinear bands: the within-class covariance matrix would be singular. Only one band per correlated region (Section 4.2.1) is offered.',
  'It identifies the few bands that jointly separate the classes, rather than bands that are only individually correlated with DI. Bhattacharya and Chattopadhyay (2013) retained 25 Hyperion bands in the green, red, NIR and SWIR with canonical correlation above 0.5.',
  'Input: the region-representative robust bands of Step 1.2 (reflectance and derivatives), standardised; groups of Step III.1; entry p < 0.05, removal p > 0.10; repeated in every training fold. Output: the selected bands, the canonical correlation and Wilks\' lambda of each function, and the standardised coefficients.',
  [['Why stepwise rather than all bands?', 'All bands would make the covariance matrix singular and overfit; stepwise entry by Wilks\' lambda keeps only bands that add separation given those already selected, which also removes redundant neighbours.'],
   ['What does a canonical correlation of 0.5 mean?', 'The discriminant function explains 0.5^{2} = 25% of the variance between groups; Bhattacharya and Chattopadhyay (2013) used it as the minimum for retaining bands.']], `A short list of jointly discriminating bands per task, with Wilks' lambda, canonical correlations and standardised coefficients.`, [
    `**Regularised discriminant analysis** for many or collinear bands (Friedman, 1989).`,
    `**PLS discriminant analysis** (Barker and Rayens, 2003).`,
    `**SPA** or **CARS** wavelength selection (Araújo et al., 2001; Li et al., 2009).`]));
K.push(...STAGE('Step III.4 Examine response curves of the selected bands',
  'Plot the reflectance of each selected band against the disease level to see the direction and shape of the response.',
  'It comes after band selection and before index building because the direction of response (increase or decrease with disease) determines how bands should be combined into indices.',
  'It gives the physical interpretation. In Bhattacharya and Chattopadhyay (2013), green and red reflectance rose with incidence (R^{2} 0.71–0.84), NIR fell (R^{2} 0.5–0.81) and SWIR rose most strongly (R^{2} 0.74–0.95), showing that water status was the strongest signal of rot.',
  'Class-mean reflectance of each selected band is plotted against class-mean DI, and Spearman ρ is computed with all plot-dates (not only class means, which inflate R^{2}). Expected for white rust: visible ↑ (chlorosis, white pustules), red edge shifted, NIR ↓, SWIR ↑.',
  [['Why are R² values from group means optimistic?', 'Averaging removes within-group scatter; with five points even a weak relation can give a high R^{2}. I therefore report plot-level correlations.']], `Response curves and Spearman ρ of each selected band with DI, showing which regions rise or fall with white rust.`, [
    `**Correlation scalograms** over the whole spectrum (Step 1.2; Shukla et al., 2024).`,
    `**Ratio of diseased to healthy reflectance** per band (Liu et al., 2024).`,
    `**Smoothed non-linear response curves** with generalised additive models (Zuur et al., 2009).`]));
K.push(...STAGE('Step III.5 Build candidate indices from the selected bands',
  'Combine selected bands into ratios, normalised differences and three-band indices so that bands responding in opposite directions reinforce each other and illumination effects cancel.',
  'Indices are built only after the response curves are known and only from bands that survived Step III.3, which keeps the number of candidates manageable and physically meaningful.',
  'Bhattacharya and Chattopadhyay (2013) built 224 new indices; the best, ROTI = R1175/(R1982 + R691), combines NIR (structure), SWIR (water) and red (pigment). They used single bands out of clusters of closely located bands, avoiding indices made of near-duplicate bands.',
  'Candidates are ratios R_{a}/R_{b}, normalised differences (R_{a} − R_{b})/(R_{a} + R_{b}) and ROTI-type R_{a}/(R_{b} + R_{c}) of selected bands at least 50 nm apart (Mahlein et al., 2013), preferring bands with opposite responses (e.g. SWIR ↑ with NIR ↓). They are pooled with the 39 published indices (including DWSI-1, DWSI-4 and ROTI) and the WRI of Step 1.3.',
  [['Why combine bands with opposite responses?', 'If one band rises and the other falls with disease, their ratio or difference changes more than either band, while multiplicative illumination effects cancel.']], `A pool of candidate indices: new two- and three-band combinations of the selected bands, the 39 published indices and the WRI.`, [
    `**Exhaustive two-band RSI, DSI and NDSI searches** over all band pairs (Shukla et al., 2024).`,
    `**Spectral disease index search** with ReliefF and an optimised weight (Mahlein et al., 2013).`,
    `**Random-forest-guided combination search** (Ramalingam et al., 2026).`]));
K.push(...STAGE('Step III.6 Second discriminant step: screen the indices',
  'A second stepwise canonical discriminant analysis with indices as predictors; indices are ranked by canonical correlation and by their contribution to Wilks\' lambda.',
  'It comes last in the selection chain because it compares new and published indices on equal terms, using the same groups as Step III.3.',
  'It gives a small, interpretable set of disease-discriminating indices. Bhattacharya and Chattopadhyay (2013) kept DWSI-1 and DWSI-4 among published indices and DRI and ROTI among new ones (canonical correlation above 0.8), and recommended ROTI because its three bands capture pigment, structure and water.',
  'Indices, red-edge parameters and the WRI are passed through VIF < 10, then the stepwise analysis; indices with canonical correlation > 0.8 (or the top-ranked ones) are added to the HS DSF pool together with the Boruta-confirmed features. For MS, RGB and TIR, which have few features, a single stepwise analysis on their features after VIF is enough. The cross-validated classification accuracy of the discriminant functions is reported as a linear benchmark for Objective 2.',
  [['How is this different from Boruta?', 'Boruta tests each feature\'s relevance with a non-linear random forest and keeps all relevant features; stepwise discriminant analysis keeps a minimal linear combination that separates the classes. Agreement between them strengthens the conclusion.'],
   ['Why did ROTI beat DRI in their study?', 'DRI uses two bands (SWIR and green) and reflects only pigment and water; ROTI uses red, NIR and SWIR and captures pigment, structure and water. On the maps DRI also flagged pixels on 7 January 2005, when the ground showed only low blight and a normal crop, whereas ROTI clearly separated rot-affected from rot-free patches.']], `A ranked set of discriminating indices with canonical correlations; the top ones added to the HS DSF pool; a cross-validated linear benchmark accuracy for each sensor.`, [
    `**Ranking by balanced accuracy** of one-feature threshold classifiers (Mahlein et al., 2013).`,
    `**Boruta** relevance of the indices (Kursa and Rudnicki, 2010).`,
    `**Univariate R^{2} of each index with DI** (Mustafa et al., 2023).`]));
K.push(...STAGE('Step III.7 Set class thresholds and map',
  'Convert the best index (or the discriminant functions) into a classification by thresholds or decision boundaries and apply it to every plot.',
  'It turns the characterisation into a map, the practical output, and tests whether the separation found in Steps III.3–III.6 holds on data not used to find it.',
  'Bhattacharya and Chattopadhyay (2013) set 1.25 < DRI ≤ 3.5 and 0 < ROTI ≤ 1.5 from the observed incidence limits with ±10% margins and overlaid them on a LISS-IV mustard mask; ROTI separated rot-affected from rot-free patches.',
  'Thresholds of the best index (optimised on training replications) or LDA boundaries are applied to the held-out replication to give a healthy / Low / Moderate / High map per flight; accuracy is reported with OA, kappa and macro-F1 (Section 5.5).',
  [['Why not set thresholds on all the data?', 'Thresholds fitted on the test data would make the map accuracy optimistic; they are fitted on training replications only.']], `Class thresholds or discriminant boundaries and plot-level healthy / Low / Moderate / High maps of the held-out replication with their accuracy.`, [
    `**ROC-optimal thresholds** maximising Youden's index (Youden, 1950; Fawcett, 2006).`,
    `**Probabilistic classification maps** from the posterior probabilities of LDA or SVM.`,
    `**Otsu thresholding** of the index histogram when no labels are available (Otsu, 1979).`]));
K.push(...STAGE('Step III.8 Validate',
  'Check the discrimination against independent truth.',
  'Validation closes the chain; without it, the selected bands and thresholds may only describe the training data.',
  'Bhattacharya and Chattopadhyay (2013) had no later Hyperion data, so they validated indirectly through the lower fractional canopy cover of diseased patches in 2005 compared with the normal year 2007.',
  'Validation is direct: plot DI scored on the ground, leave-one-replication-out cross-validation, and the Bharatpur and farmers\' field datasets (Chapter 7).',
  [['What would you do differently from Bhattacharya and Chattopadhyay (2013)?', 'Use plot-level rather than group-mean correlations, select bands inside cross-validation folds, and validate directly against ground-scored DI on independent plots; their study was limited by Hyperion availability, not by the method.']], `Independent accuracy of the discriminant indices and maps on held-out replications and at Bharatpur and farmers' fields.`, [
    `**Indirect impact validation** through canopy cover or LAI differences between disease and normal years (Bhattacharya and Chattopadhyay, 2013).`,
    `**Relating maps to yield loss** (Nguyen et al., 2023).`,
    `**Multi-season validation** (Tian et al., 2021; Mustafa et al., 2023).`]));
K.push(INCASE(`For the hyperspectral severity task, Step III.3 might keep five bands (for example in the green, red edge, NIR and two SWIR regions) with a first canonical correlation of 0.8. The response curves could show SWIR reflectance rising and NIR falling with DI, so Step III.5 would build ROTI-type indices combining them. Step III.6 might rank the WRI, PSSRa and a new SWIR/NIR index highest; these enter the HS DSF pool. The canonical score plot then shows healthy and High clearly apart and Low and Moderate partly overlapping, consistent with the JM distances. For MS, RGB and TIR the single-step analysis gives each sensor's canonical correlation, a simple measure for comparing sensors before Objective 2.`));
K.push(...STEPEND(`A cross-sensor correlation matrix of DSFs; JM distances per sensor; for each sensor the discriminating bands and indices, canonical correlations, Wilks' lambda, canonical score plots and the cross-validated accuracy of the discriminant functions; discriminant indices added to the HS DSF pool.`, [
  `**Canonical correlation analysis** between the feature sets of two sensors to measure shared information (Hotelling, 1936).`,
  `**PLS discriminant analysis** (Barker and Rayens, 2003) or **regularised discriminant analysis** when features are many or collinear (Friedman, 1989).`,
  `**Quadratic discriminant analysis** when class covariances differ (Das et al., 2020).`,
  `**Non-linear visualisation** of class separation with t-SNE or UMAP (Ramalingam et al., 2026).`
]));
// ---- Step 1.7 sensor-wise implementation for MS, TIR, RGB ----
K.push(H2('4.7 Sensor-wise implementation of Objective 1 for multispectral, thermal and RGB data'));
K.push(P('Sections 4.4–4.6 apply to every sensor. This section gives the complete step-by-step procedure for the three non-hyperspectral datasets, which do not use band-level scalograms or the WRI. For each sensor the analysis is done twice, for detection (healthy vs diseased) and for severity (healthy, Low, Moderate, High and DI), on the pooled post-symptomatic plot-dates. ' + T('objsens') + ' summarises the three procedures.'));
K.push(H3('4.7.1 Multispectral data (MicaSense RedEdge-MX)'));
K.push(NLm('**Feature table.** For every plot-date: plot-mean reflectance of the five bands (B 475, G 560, R 668, RE 717, NIR 840 nm), the 12 vegetation indices of ' + T('msidx') + ', the 40 GLCM textures of the five bands and, optionally, percentile reflectance (20th–50th percentile of canopy pixels) and TTCI (Liu et al., 2024).'));
K.push(NLm('**Spectral response by group.** Mean ± standard deviation of each band for healthy, Low, Moderate and High plots, and the ratio of diseased to healthy reflectance per band. Expected: visible and red-edge reflectance rise and NIR reflectance falls as chlorophyll and leaf structure are lost (Liu et al., 2024; Guo et al., 2021).'));
K.push(NLm('**Pixel histograms and extraction method.** Frequency histograms of canopy-pixel reflectance of each band per group show whether disease shifts the whole distribution (Liu et al., 2024). The plot mean (CS) and percentile reflectance (LS) are compared by their correlation with DI; Liu et al. (2024) found LS more sensitive than CS for powdery mildew.'));
K.push(NLm('**Statistical tests (Section 4.4).** Detection: t-test or Mann–Whitney U for each band, index and texture. Severity: one-way ANOVA + Tukey HSD or Kruskal–Wallis + Dunn across healthy, Low, Moderate and High; Spearman ρ and Pearson r with DI (Liu et al., 2024; Feng et al., 2022; Tian et al., 2021).'));
K.push(NLm('**Physiological interpretation.** Correlation of the significant indices with chlorophyll a and b, carotenoid and anthocyanin (ORW Activity 1.2). Chlorophyll and red-edge indices (NDRE, MTCI, CI_{rededge}, PSRI) are expected to respond most; NDRE, PSRI and MTCI were the indices that consistently tracked wheat powdery mildew (Liu et al., 2024).'));
K.push(NLm('**Machine-learning relevance (Section 4.5).** Boruta on all MS features, separately for detection, severity classes and DI, gives the MS DSF pools (Mustafa et al., 2023); univariate regression of each DSF against DI gives R^2 and RMSE (Mustafa et al., 2023; Feng et al., 2022).'));
K.push(NLm('**Separability (Section 4.6).** JM distance between the four groups using the top MS DSFs (Richards, 2013).'));
K.push(BOX('MS output:', 'MS DSF pools for detection, severity and DI; the most sensitive bands and indices; whether percentile extraction is better than the plot mean.', 'EEF3E8', '2C5F2D'));
K.push(H3('4.7.2 Thermal data (FLIR Vue Pro R)'));
K.push(NLt('**Feature table.** For every plot-date: CT, CTD, CTR (kelvin), NRCT and MTD (Eq. 4.3) and the 8 GLCM textures of the quantised temperature image (' + T('tirfeat') + '; Feng et al., 2022; Mahlein et al., 2019; Maimaitijiang et al., 2020).'));
K.push(NLt('**Thermal response by group.** Maps and frequency histograms of canopy temperature for healthy, Low, Moderate and High plots; mean ± standard deviation of each thermal parameter per group. Expected: diseased canopies are warmer because infection disturbs stomatal regulation and transpiration; in wheat powdery mildew, DI and canopy temperature increased together (r = 0.88; Liu et al., 2024), and thermography showed temperature differences in infected spikelets (Mahlein et al., 2019).'));
K.push(NLt('**Raw versus normalised temperature.** Because all flights are pooled, CT is compared with CTD, CTR and NRCT by their correlation with DI. The normalised parameters remove the influence of air temperature and are expected to be more consistent (Feng et al., 2022, retained CTD and NRCT).'));
K.push(NLt('**Statistical tests (Section 4.4).** Detection: t-test or Mann–Whitney U; severity: ANOVA + Tukey HSD or Kruskal–Wallis + Dunn; Spearman ρ and Pearson r with DI.'));
K.push(NLt('**Physiological interpretation.** Correlation of CT, CTD and NRCT with stomatal conductance, transpiration rate and relative water content (ORW Activity 1.2); negative correlation with stomatal conductance would confirm that the thermal signal reflects reduced transpiration.'));
K.push(NLt('**Disease versus water stress.** A warm canopy can also mean water deficit. Following the logic of the TVDI–NDWI space of Bhattacharya and Chattopadhyay (2013), where canopy stress without soil-moisture stress indicated mustard rot, CTD and NRCT are plotted against a hyperspectral water index (WI or DWSI-1) and checked against the uniform irrigation of the plots. Diseased plots that are warmer without lower water status confirm a disease signal rather than drought.'));
K.push(NLt('**Machine-learning relevance.** Boruta for detection, severity and DI gives the TIR DSF pools; univariate regression against DI (Mustafa et al., 2023). MTD is reported even if not selected, because Mahlein et al. (2019) found it was the only parameter not correlated with disease severity.'));
K.push(NLt('**Separability.** JM distance between the four groups with the top TIR DSFs (Richards, 2013).'));
K.push(BOX('TIR output:', 'TIR DSF pools; how much warmer diseased canopies are at each severity level; the best normalised thermal parameter; the physiological basis of the thermal signal.', 'EEF3E8', '2C5F2D'));
K.push(H3('4.7.3 RGB data (DJI Phantom)'));
K.push(NLg('**Feature table.** For every plot-date: 8 GLCM textures of each of the R, G and B bands (' + T('rgbfeat') + '), mean hue, saturation and value of canopy pixels, vegetation fraction VF and, if a bare-soil elevation model is available, canopy height CH (Haralick et al., 1973; Feng et al., 2022; Liu et al., 2024; Mustafa et al., 2023; Maimaitijiang et al., 2020).'));
K.push(NLg('**Visual reference.** Example image patches of healthy, Low, Moderate and High plots document how pustules, chlorosis and stagheads appear at UAV resolution (as in Liu et al., 2024, Fig. 3).'));
K.push(NLg('**Texture response.** Each texture is compared across groups and correlated with DI. Expected: contrast, dissimilarity and entropy increase and homogeneity and second moment decrease as pustules and lesions make the canopy less uniform. Entropy was the texture most correlated with powdery-mildew DI (r = 0.486; Feng et al., 2022), and texture features were most informative at higher severity (Guo et al., 2021).'));
K.push(NLg('**Colour and structure.** Hue and saturation are expected to shift with chlorosis and white pustules (colour features as in Mustafa et al., 2023); VF and CH describe canopy thinning and staghead deformation (Maimaitijiang et al., 2020).'));
K.push(NLg('**Statistical tests and physiology (Section 4.4).** Detection: t-test or Mann–Whitney U; severity: ANOVA + Tukey HSD or Kruskal–Wallis + Dunn; Spearman ρ and Pearson r with DI; correlation of colour features with chlorophyll content and of VF/CH with LAI.'));
K.push(NLg('**Optional pixel-size test.** Texture depends on pixel size: Guo et al. (2021) found that spatial resolution strongly affected texture-based accuracy (best combined model at 10 cm). The RGB orthomosaic can be resampled (e.g. to 2, 5 and 10 cm, nearest-neighbour as in Guo et al., 2021) and the texture–DI correlations compared to choose the pixel size for texture extraction.'));
K.push(NLg('**Machine-learning relevance and separability.** Boruta for detection, severity and DI gives the RGB DSF pools; univariate regression against DI; JM distance between the four groups (Mustafa et al., 2023; Richards, 2013).'));
K.push(BOX('RGB output:', 'RGB DSF pools; which texture, colour and structure features respond to white rust; the best pixel size for texture.', 'EEF3E8', '2C5F2D'));
K.push(...tab2('objsens', [
  ['Step', 'Multispectral (RedEdge-MX)', 'Thermal (FLIR)', 'RGB'],
  ['Features', '5 bands, 12 indices, 40 textures; optional percentile spectra, TTCI', 'CT, CTD, CTR, NRCT, MTD, 8 textures', '24 textures, H/S/V colour, VF, CH'],
  ['Descriptive analysis', 'Band profiles, diseased/healthy ratio, pixel histograms, mean vs percentile', 'Temperature maps and histograms; raw vs normalised temperature', 'Image patches; texture, colour and cover by group; optional pixel-size test'],
  ['Statistics (detection; severity)', 't-test/Mann–Whitney; ANOVA–Tukey or Kruskal–Wallis–Dunn; Spearman/Pearson with DI', 'Same', 'Same'],
  ['Physiology', 'Chlorophyll, carotenoid, anthocyanin', 'Stomatal conductance, transpiration, RWC', 'Chlorophyll (colour), LAI (VF, CH)'],
  ['ML relevance', 'Boruta (D, S, DI); univariate regression', 'Same', 'Same'],
  ['Separability', 'JM + canonical discriminant analysis, four groups', 'JM + canonical discriminant analysis, four groups', 'JM + canonical discriminant analysis, four groups'],
  ['Key references', 'Liu 2024; Guo 2021; Feng 2022; Mustafa 2023', 'Feng 2022; Liu 2024; Mahlein 2019; Maimaitijiang 2020', 'Feng 2022; Guo 2021; Liu 2024; Mustafa 2023; Maimaitijiang 2020; Haralick 1973'],
], [1700, 2600, 2500, 2506], 'Objective 1 procedure for the multispectral, thermal and RGB datasets.', 15));
K.push(BOX('How Objective 1 is satisfied:', 'for each sensor, the tests, correlations and Boruta show which features respond to white rust (detection) and which change across severity classes and with DI (severity), and the physiological correlations explain why. For HS, the correlation scalograms, ReliefF and the WRI identify white-rust wavelengths. The cross-sensor correlation and JM show which sensor separates severity best and whether sensors are complementary. Output: DSF pools per sensor and task for Objectives 2 and 3.', 'E3F2FD', '1565C0'));

// ======================= 7 OBJECTIVE 2 =======================
K.push(H1('5. Objective 2: Detect and discriminate severity through multimodal data fusion'));
K.push(LBL('Aim'));
K.push(P('To develop classification models for disease detection (task D) and severity discrimination into three classes (task S), and regression models for DI (task R), first with each UAV sensor separately and then with sensor combinations, and to identify the best sensor set, fusion strategy and model.'));
K.push(...fig2('obj2flow', 'n4_obj2_flow.png', 'Flow chart of Objective 2: inside each leave-one-replication-out training set, features are standardised and reduced (VIF, ML-SFFS), single-sensor and fused models are trained and tuned, and the held-out replication is predicted; the final model is validated at Bharatpur and in farmers\' fields and used for maps.', 520));
K.push(SIMPLE(`Objective 2 turns the DSF pools into working models. For each task — detection (D), three-class severity (S) and DI regression (R) — it first finds the best features and model for each sensor alone, then for sensor combinations. Two families of fusion are compared: ML-SFFS fusion picks a small, interpretable cross-sensor feature set; DNN fusion lets a neural network learn how to combine sensors. Every comparison uses the same leave-one-replication-out validation.`));
K.push(H2('5.1 Step 2.1: Feature selection for modelling (VIF → ML-SFFS)'));
K.push(P('The task-specific DSF pool of Objective 1 is reduced to an optimum feature combination (OFC) for each model (' + F('funnel') + '). Features are standardised with the mean and standard deviation of the training data (Eq. 5.1).'));
K.push(...fig2('funnel', 'f5_feature_selection.png', 'Feature selection from Objective 1 (Boruta DSF pool) to the optimum feature combination used in Objectives 2 and 3.', 470));
K.push(EQ('z = (x − μ_{train}) / σ_{train}', '5.1'));
K.push(...STEP('Variance inflation factor (VIF < 10)',
  'Remove DSFs that repeat the information of others.',
  'Many indices share the same bands (e.g. several NDVI and simple-ratio variants); collinear features make models unstable.',
  'For feature j, R_{j}^{2} is obtained by regressing feature j on all other retained features (Eq. 5.2); the feature with the largest VIF is removed and VIF is recomputed until all VIF < 10 (Kutner et al., 2005; Tian et al., 2021; Mustafa et al., 2023).',
  'Tian et al. (2021); Mustafa et al. (2023).'));
K.push(EQ('VIF_{j} = 1 / (1 − R_{j}^{2})', '5.2'));
K.push(INCASE(`Suppose the HS detection pool contains NDVI780, NDVI850 and SR850. These indices use almost the same bands, so regressing NDVI780 on the other features may give R^{2} = 0.98 and VIF = 50. It is removed first; VIF is recomputed and the next most collinear feature removed, until all VIF < 10. A pool of 25 confirmed features typically shrinks to 8–15.`));
K.push(...STEP('Machine-learning sequential floating forward selection (ML-SFFS)',
  'Select the smallest feature combination that gives the best performance for each model.',
  'Floating search can remove earlier choices that become redundant, so it finds compact combinations that simple ranking misses (Pudil et al., 1994). With the classifier as judge, Tian et al. (2021) obtained 2–4 features and up to 10% higher accuracy than with all features.',
  ['**Start:** empty subset; criterion J = cross-validated performance of the model (macro-F1 or accuracy for classification, negative RMSE for regression).',
   '**Step 1 – Inclusion:** each feature not yet selected is added in turn; the feature giving the highest J is added (the most significant feature).',
   '**Step 2 – Conditional exclusion:** the least significant feature of the new subset (the one whose removal lowers J least) is identified; it is removed only if it is not the feature just added and if the smaller subset has a higher J than the best subset of that size found before.',
   '**Step 3 – Continued exclusion:** after a removal, Step 2 is repeated on the smaller subset while J keeps improving; then the search returns to Step 1.',
   '**Stop:** at 10 features (or all features). The OFC is the subset with the highest J; between equal values, the smaller subset (Pudil et al., 1994; Tian et al., 2021).',
   '**Robustness:** J is computed by 4-fold cross-validation grouped by plot, repeated 10 times; the most frequently selected subset is the OFC (Tian et al., 2021, used 100 repetitions).'],
  'Pudil et al. (1994); Tian et al. (2021); Mustafa et al. (2023). Using a regression criterion (RMSE) follows the wrapper principle of the RMSE-based feature elimination of Liu et al. (2024).'));
K.push(...STEPEND(`For every sensor or sensor set, task and model: the optimum feature combination (OFC), its selection frequency over repeated searches and its cross-validated score; features removed by VIF are listed.`, [
  `**Genetic-algorithm or particle-swarm wrappers** for subset search (Huang et al., 2020, used PSO to tune SVM).`,
  `**Recursive feature elimination** (Guyon et al., 2002; Liu et al., 2024).`,
  `**mRMR** filter selection (Peng et al., 2005) or **SPA** (Araújo et al., 2001).`,
  `**Embedded selection** with LASSO or elastic net (Tibshirani, 1996; Zou and Hastie, 2005).`
]));
K.push(H2('5.2 Step 2.2: Single-sensor models (RGB, MS, HS, TIR)'));
K.push(P('For each sensor separately (input sets S1–S4) and for each task, the task-specific DSF pool of that sensor goes through VIF and ML-SFFS, and the models of ' + T('models') + ' are trained:'));
K.push(BL('**Detection (D):** SVM, RF and k-NN on their own OFC; DNN-F1 on the DSF pool after VIF.'));
K.push(BL('**Severity discrimination (S):** the same models, trained on diseased plot-dates with the three classes.'));
K.push(BL('**Regression (R):** SVR, RFR and k-NN on their own OFC; PLSR and DNN-F1 on the DSF pool after VIF.'));
K.push(P('This gives the stand-alone performance of each sensor for each task, the reference against which fusion is judged (Mahlein et al., 2019; Feng et al., 2022).'));
K.push(...STEPEND(`Stand-alone performance of RGB, MS, HS and TIR for detection (OA, kappa, F1), severity (macro-F1) and DI (R^{2}, RMSE, NRMSE), with confusion matrices: the baseline that fusion must beat.`, [
  `**Gradient boosting** such as XGBoost (Chen and Guestrin, 2016).`,
  `**Gaussian process regression**, which also gives prediction uncertainty (Rasmussen and Williams, 2006).`,
  `**Back-propagation neural networks, extreme learning machines and LS-SVM** (Zhu et al., 2017; Baranowski et al., 2015).`,
  `**Fisher LDA** for severity levels (Zhang et al., 2012a) and **MARS** for severity regression (Mandal et al., 2023).`
]));
K.push(H2('5.3 Step 2.3: Sensor combinations and fusion strategies'));
K.push(...tab2('inputsets', [
  ['Input set', 'Sensors', 'Rationale'],
  ['S1–S4', 'RGB; MS; HS; TIR (each alone)', 'Stand-alone ability of each sensor'],
  ['S5', 'RGB + TIR', 'Visible symptoms + stomatal response'],
  ['S6', 'MS + TIR', 'Low-cost operational pair (Liu 2024)'],
  ['S7', 'HS + TIR', 'Best pair in Mahlein 2019 (spectral + thermal)'],
  ['S8', 'RGB + MS + HS + TIR', 'Full multimodal fusion (Maimaitijiang 2020)'],
], [1700, 3300, 4306], 'Input sets (single sensors and the combinations listed in the ORW).', 17));
K.push(INCASE(`**How many models are trained?** Single sensors S1–S4: for D and S, SVM, RF, k-NN and DNN-F1 (4 models × 4 sensors × 2 tasks = 32); for R, SVR, RFR, k-NN, PLSR and DNN-F1 (5 × 4 = 20). Combinations S5–S8: for D and S, FA (3 classifiers) + FB (3) + DNN-F1 + DNN-F2 (8 × 4 × 2 = 64); for R, FA (3) + FB (3) + PLSR + DNN-F1 + DNN-F2 (9 × 4 = 36). In total **152 model configurations**, each trained and tested three times (one per held-out replication). Six algorithms are used; the large number comes only from systematic combination of sensors, tasks and fusion strategies.`));
K.push(P('Each combination is fused at feature level by four strategies (' + F('fusion') + '). Fusion is done separately for each task, because the DSF pools are task-specific.'));
K.push(...fig2('fusion', 'f6_fusion_strategies.png', 'Single-sensor modelling (a) and the four feature-level fusion strategies (b–d).', 560));
K.push(H3('Fusion pipeline for classification (tasks D and S)'));
K.push(P('Inside each training fold (Chapter 7):'));
K.push(NLc('Take the task-specific Boruta DSF pool of each sensor in the set (Boruta repeated on the training data).'));
K.push(NLc('**FA – Pooled ML-SFFS fusion (Mustafa et al., 2023):** concatenate the DSFs of all sensors in the set → standardise → VIF < 10 on the pooled set → ML-SFFS with SVM, RF or k-NN as judge (criterion: macro-F1 for S, accuracy or F1 for D) → one cross-sensor OFC per classifier. The sensor make-up of the OFC shows which sensors contribute.'));
K.push(NLc('**FB – Sensor-wise ML-SFFS fusion (ORW Activity 3.1):** VIF and ML-SFFS within each sensor → concatenate the sensor OFCs → VIF < 10 → a final ML-SFFS pass removes cross-sensor redundancy → classifier.'));
K.push(NLc('**FC / FD – DNN fusion (Maimaitijiang et al., 2020):** DSFs of each sensor after VIF are fed to DNN-F1 (all features concatenated at the input) or DNN-F2 (one sub-network per sensor, joined at an intermediate layer), with a softmax output layer and cross-entropy loss (Eq. 5.8) for classes. This adapts the regression networks of Maimaitijiang et al. (2020) to classification by changing only the output layer and loss.'));
K.push(NLc('Train the classifier with class weights inversely proportional to class size; predict the held-out replication; compute the metrics of Section 5.5.'));
K.push(H3('Fusion pipeline for regression (task R)'));
K.push(NLr('Take the DI-specific Boruta DSF pool of each sensor in the set (training data).'));
K.push(NLr('**FA:** concatenate → standardise → VIF < 10 → ML-SFFS with SVR, RFR or k-NN as judge (criterion: cross-validated RMSE) → OFC → model.'));
K.push(NLr('**FB:** VIF and ML-SFFS (RMSE) within each sensor → concatenate the sensor OFCs → VIF → final SFFS pass → model.'));
K.push(NLr('**Linear baseline:** PLSR on the concatenated DSF pool after VIF (Maimaitijiang et al., 2020).'));
K.push(NLr('**FC / FD:** DNN-F1 and DNN-F2 with a linear output and mean-squared-error loss (Maimaitijiang et al., 2020).'));
K.push(NLr('Predict DI of the held-out replication; compute R^2, RMSE and NRMSE; derive severity classes from predicted DI and compare with direct classification.'));
K.push(INCASE(`**Pooled versus sensor-wise ML-SFFS fusion, with S7 (HS + TIR) for severity.** In FA the HS severity pool (say 12 features after VIF) and the TIR pool (say 5) are concatenated into 17 features; VIF is re-run on the 17, and ML-SFFS with SVM as judge may choose {PSSRa, WRI, CTD, NRCT}. In FB, ML-SFFS first picks the best HS subset (say {PSSRa, WRI, REP}) and the best TIR subset (say {CTD, MTD}); these five are concatenated and a final SFFS pass removes redundancy, giving for example {PSSRa, WRI, CTD}. FA can find cross-sensor interactions directly; FB guarantees that each sensor is represented by its best features. Comparing them shows which is more accurate and more stable.`));

K.push(...STEPEND(`For S5–S8 and each task: the cross-sensor OFCs of FA and FB with their sensor make-up, and the performance of FA, FB, DNN-F1, DNN-F2 and PLSR compared with the best single sensor.`, [
  `**Decision-level fusion** by voting or stacking of single-sensor models (Wolpert, 1992).`,
  `**End-to-end multimodal deep networks** on images, e.g. RustQNet with mutual-information minimisation (Deng et al., 2024).`,
  `**Attention-based or late-fusion deep architectures** reviewed by Ramachandram and Taylor (2017).`
]));
// ---- models ----
K.push(H2('5.4 Step 2.4: Models'));
K.push(BL('**Support vector machine (SVM / SVR)** with radial basis function kernel (Cortes and Vapnik, 1995); one-vs-one voting for three classes; SVR with ε-insensitive loss; C and γ tuned by grid search (Tian et al., 2021; Mahlein et al., 2019).'));
K.push(EQ('f(x) = sign[ Σ_{i} α_{i} y_{i} K(x_{i}, x) + b ],   K(x_{i}, x) = exp(−γ ‖x − x_{i}‖^{2})', '5.3'));
K.push(BL('**Random forest (RF / RFR)** (Breiman, 2001): B trees grown on bootstrap samples with m random features per split; majority vote (classes) or mean (DI).'));
K.push(EQ('ŷ(x) = mode{ T_{b}(x) }  (classification);    ŷ(x) = (1/B) Σ_{b=1}^{B} T_{b}(x)  (regression)', '5.4'));
K.push(BL('**k-nearest neighbours (k-NN)** (Cover and Hart, 1967): majority class or mean DI of the k nearest training samples in standardised feature space (Euclidean distance; Tian et al., 2021; Mustafa et al., 2023).'));
K.push(BL('**Partial least squares regression (PLSR)** (Wold et al., 2001): projection of predictors and DI onto latent components; number of components by minimum cross-validated RMSE (Guo et al., 2021; Feng et al., 2022). PLSR also gave the best prediction of aphid severity grade in mustard (Shukla et al., 2024).'));
K.push(EQ('X = T P^{T} + E,     y = T q + f', '5.5'));
K.push(BL('**DNN-F1 and DNN-F2** (Maimaitijiang et al., 2020): fully connected layers with ReLU activation, batch normalisation (Ioffe and Szegedy, 2015) and dropout (Srivastava et al., 2014), Adam optimiser (Kingma and Ba, 2015) and early stopping on a plot-grouped validation split (' + F('dnn') + ').'));
K.push(EQ('h^{(l)} = Dropout( ReLU( BN( W^{(l)} h^{(l−1)} + b^{(l)} ) ) )', '5.6'));
K.push(EQ('DNN-F2:  h_{s} = g_{s}(x_{s}),  s ∈ {RGB, MS, HS, TIR};    z = g_{joint}( [h_{RGB}; h_{MS}; h_{HS}; h_{TIR}] )', '5.7'));
K.push(EQ('Regression:  ŷ = w^{T} z + c,   loss = mean (y − ŷ)^{2}'));
K.push(EQ('Classification:  p_{k} = exp(z_{k}) / Σ_{j} exp(z_{j}),   loss = − Σ_{k} y_{k} ln p_{k}', '5.8'));
K.push(...fig2('dnn', 'f2_dnn_fusion.png', 'Deep-learning fusion networks adapted from Maimaitijiang et al. (2020): (a) DNN-F1, input-level fusion; (b) DNN-F2, intermediate-level fusion with one sub-network per sensor.', 560));
K.push(...tab2('hyper', [
  ['Model', 'Hyper-parameters (tuned in inner cross-validation)'],
  ['SVM / SVR', 'C ∈ {2^{−2}, …, 2^{8}}; γ ∈ {2^{−8}, …, 2^{2}}; SVR ε ∈ {0.1, 0.5, 1}; class weights balanced'],
  ['RF / RFR', '500 trees; m ∈ {√p, p/3, p/2}; minimum leaf size ∈ {1, 3, 5}; class weights balanced'],
  ['k-NN', 'k ∈ {3, 5, 7, 9, 11}; Euclidean distance on standardised features'],
  ['PLSR', 'Latent components 1 to min(10, p), by minimum cross-validated RMSE'],
  ['DNN-F1', 'Three dense layers (e.g. 64–32–16 units); dropout ∈ {0.2, 0.3, 0.5}; Adam, learning rate 10^{−3}; batch 32; up to 500 epochs; early stopping (patience 30)'],
  ['DNN-F2', 'Two-layer sub-network per sensor (e.g. 16–8 units); joint layer of 16 units; other settings as DNN-F1'],
], [1800, 7506], 'Hyper-parameter ranges (p = number of input features; "e.g." values are starting configurations).', 17));
K.push(...tab2('models', [
  ['Model', 'Type', 'Tasks', 'Strategies', 'Why chosen (source)'],
  ['SVM / SVR (RBF)', 'Kernel machine learning', 'D, S, R, P', 'a, FA, FB', 'Best SFFS criterion in Tian 2021; used in Mahlein 2019, Mustafa 2023; SVR in Feng 2022'],
  ['RF / RFR', 'Ensemble of trees', 'D, S, R, P', 'a, FA, FB', 'Best regressor in Feng 2022; basis of Boruta'],
  ['k-NN', 'Instance-based', 'D, S, R, P', 'a, FA, FB', 'Best multivariate regression in Mustafa 2023; SFFS criterion in Tian 2021'],
  ['PLSR', 'Linear latent-variable', 'R', 'a, concatenation', 'Linear baseline (Guo 2021; Feng 2022; Maimaitijiang 2020)'],
  ['DNN-F1', 'Deep learning, input-level fusion', 'D, S, R', 'a, FC', 'Maimaitijiang 2020'],
  ['DNN-F2', 'Deep learning, intermediate fusion', 'D, S, R', 'FD', 'Best model in Maimaitijiang 2020'],
], [1600, 1900, 1100, 1500, 3206], 'The six models (P = pre-symptomatic task of Objective 3).', 16));
K.push(...STEPEND(`Tuned hyperparameters for each model (C, γ, ε; number of trees and mtry; k; number of PLS components; DNN architecture, dropout and epochs) and the trained models for each fold.`, [
  `**Random search** instead of grid search (Bergstra and Bengio, 2012).`,
  `**Bayesian optimisation** of hyperparameters (Snoek et al., 2012).`,
  `**Particle-swarm optimisation** of SVM parameters (Huang et al., 2020).`
]));
K.push(H2('5.5 Step 2.5: Evaluation metrics'));
K.push(P('Classification metrics are computed from the confusion matrix (n_{ij} = samples of true class i predicted as class j; N = total; K = number of classes):'));
K.push(EQ('OA = Σ_{k} n_{kk} / N;   P_{k} = n_{kk} / Σ_{i} n_{ik};   R_{k} = n_{kk} / Σ_{j} n_{kj}'));
K.push(EQ('F1_{k} = 2 P_{k} R_{k} / (P_{k} + R_{k})', '5.9'));
K.push(EQ('macro-F1 = (1/K) Σ_{k} F1_{k};   κ = (p_{o} − p_{e}) / (1 − p_{e}),   p_{e} = Σ_{k} n_{k+} n_{+k} / N^{2}', '5.10'));
K.push(P('with p_{o} = OA (Cohen, 1960; Sokolova and Lapalme, 2009). For detection, sensitivity = TP/(TP + FN) and specificity = TN/(TN + FP). Regression is evaluated with (Liu et al., 2024):'));
K.push(EQ('R^{2} = 1 − Σ (y_{i} − ŷ_{i})^{2} / Σ (y_{i} − ȳ)^{2}'));
K.push(EQ('RMSE = √[ Σ (y_{i} − ŷ_{i})^{2} / n ];    NRMSE = RMSE / ȳ × 100', '5.11'));
K.push(P('The relative error of Feng et al. (2022) divides by each measured value and is undefined for healthy plots (DI = 0), so NRMSE is used instead.'));
K.push(...tab2('metrics', [
  ['Metric', 'Task', 'Interpretation'],
  ['OA, kappa', 'D, S, P', 'Overall correctness; agreement beyond chance'],
  ['Sensitivity, specificity', 'D, P', 'Diseased and healthy plots correctly identified'],
  ['Precision, recall, F1, macro-F1', 'D, S, P', 'Per-class performance; macro-F1 weights Low, Moderate and High equally'],
  ['R^{2}, RMSE, NRMSE', 'R', 'Explained variance; error in DI units; error relative to mean DI'],
], [3000, 1300, 5006], 'Evaluation metrics.', 17));
K.push(...STEPEND(`For every configuration and test replication: confusion matrix, OA, kappa, precision, recall, F1, macro-F1, sensitivity and specificity (D, S) or R^{2}, RMSE and NRMSE (R), summarised as mean ± SD over three folds.`, [
  `**Balanced accuracy** (Mahlein et al., 2013) and **ROC curves and AUC** for detection (Fawcett, 2006).`,
  `**Matthews correlation coefficient**, robust to class imbalance (Chicco and Jurman, 2020).`,
  `**Ratio of performance to deviation (RPD)** for regression (Mandal et al., 2023) and **Lin's concordance correlation coefficient** (Lin, 1989).`
]));
K.push(H2('5.6 Step 2.6: Comparison, robustness and maps'));
K.push(BL('**Sensors and fusion:** for each task, S1–S4 are compared with S5–S8, and FA, FB, FC and FD are compared. A fusion is useful only if it beats the best single sensor on the test replications and at Bharatpur.'));
K.push(BL('**Robustness across varieties:** absolute errors of Varuna, Pusa Vijay and PM 38 are compared by one-way ANOVA + Tukey HSD (approach of Maimaitijiang et al., 2020).'));
K.push(BL('**Interpretation:** features of each OFC and their sensor origin; RF importance of the best model.'));
K.push(BL('**Maps:** detection followed by severity classification gives a map of healthy, Low, Moderate and High plots; the best regression model maps DI and its absolute error (Liu et al., 2024).'));
K.push(...STEPEND(`The best sensor or sensor set, fusion strategy and model for detection, severity and DI; robustness across varieties; the features driving the best models; maps of severity class, DI and absolute error.`, [
  `**McNemar's test** to compare two classifiers on the same test data, or the **corrected resampled t-test** for cross-validated scores (Dietterich, 1998; Nadeau and Bengio, 2003).`,
  `**Uncertainty maps** from class probabilities or quantile regression forests (Meinshausen, 2006).`,
  `**Spatial interpolation** of plot predictions by kriging for field-scale maps (Oliver and Webster, 1990).`
]));
K.push(BOX('How Objective 2 is satisfied:', 'detection, three-class severity discrimination and DI estimation are each modelled with every sensor alone and with four combinations, using two ML-SFFS fusion strategies and two DNN fusion strategies. The comparison identifies the best sensor set, fusion strategy and model for each task.', 'FCE4EC', 'AD1457'));

// ======================= 8 OBJECTIVE 3 =======================
K.push(H1('6. Objective 3: Pre-symptomatic prediction'));
K.push(LBL('Aim'));
K.push(P('To separate inoculated plots that later develop white rust from healthy plots using UAV data collected before visible symptoms, with each sensor and with fused sensors.'));
K.push(...fig2('obj3flow', 'n5_obj3_flow.png', 'Flow chart of Objective 3: pre-symptomatic samples, labelling rule, screening and feature selection, single-sensor and fused classification, and risk maps.', 500));
K.push(SIMPLE(`Before pustules appear, every plot has DI = 0, so the label must come from the future: an inoculated plot is called "infected" only if symptoms later appear on it. The question is whether thermal, spectral or texture features already differ between these plots and the healthy controls. Because these early differences are small, only the strongest, simplest models (SVM, RF, k-NN) are used, and sensitivity (how many infected plots are found) and specificity (how many healthy plots are correctly left alone) are reported.`));
K.push(...STEP('Step 3.1. Samples and labels',
  'Pool all pre-symptomatic flights (432 plot-dates; ORW) and label them.',
  'Wrong labels are the main risk in pre-symptomatic work.',
  ['Control plots = healthy; inoculated plots = infected only if symptoms later appear on them (Tian et al., 2021).',
   'Inoculated plots of the resistant variety (PM 38) that never show symptoms are excluded from the infected class and reported separately.',
   'Biochemical and biophysical parameters that differ between healthy and infected plots (t-test / Mann–Whitney U) are identified (ORW Activity 3.1).'],
  'Tian et al. (2021).'));
K.push(INCASE(`**Expected class sizes.** Of the 72 plots, 36 are controls (healthy) and 36 are inoculated. If the 12 inoculated PM 38 plots (4 timings × 3 replications) never show symptoms, they are excluded, leaving up to 24 infected plots. With 6 pre-symptomatic flights this gives about 216 healthy and 144 infected plot-dates — an imbalance of 1.5 : 1 that is handled with class weights and with sensitivity, specificity and F1 rather than accuracy alone.`));
K.push(...STEPEND(`A labelled pre-symptomatic table: healthy control plot-dates, later-infected plot-dates and excluded resistant plots, with class counts and the physiological parameters that differ before symptoms.`, [
  `**Days-after-inoculation labels** under controlled conditions (Zhu et al., 2017; Terentev et al., 2023).`,
  `**Pathogen quantification** in tissue to confirm infection before symptoms (Zhang et al., 2024).`,
  `**Semi-supervised or one-class labelling** that uses only confidently healthy samples (Liu et al., 2008).`
]));
K.push(...STEP('Step 3.2. Pre-symptomatic features',
  'Find the features that differ before symptoms, for each sensor.',
  'Early changes are small and may involve other features than visible disease.',
  ['All features of Section 4.1 are tested between healthy and infected plots (t-test / Mann–Whitney U; Tian et al., 2021).',
   'HS: ReliefF (Step 1.2, sub-step C) is run with labels healthy vs infected to find pre-symptomatic bands (DI is 0 before symptoms, so the DI scalogram is not used).',
   'Boruta per sensor with the pre-symptomatic labels gives the pre-symptomatic DSF pools.'],
  'Tian et al. (2021); Mustafa et al. (2023).'));
K.push(...STEPEND(`Pre-symptomatic DSF pools per sensor (features that differ before symptoms) and HS bands ranked by ReliefF for healthy vs later-infected.`, [
  `**Chlorophyll-fluorescence imaging** parameters (Fv/Fm, Y(II)) as early indicators (Mahlein et al., 2019).`,
  `**Change features relative to control plots** on each flight, or temporal trajectories (Nguyen et al., 2023).`,
  `**Water- and defence-related bands** found to drive pre-symptomatic detection (around 1400 and 750 nm; Zhang et al., 2024).`
]));
K.push(...STEP('Step 3.3. Single-sensor and fused classification',
  'Classify healthy vs infected plots with each sensor and with fused sets.',
  'Identifies the sensor set that gives the most reliable early warning (Mahlein et al., 2019).',
  ['S1–S4: VIF → ML-SFFS → SVM, RF, k-NN. S5–S8: pooled (FA) and sensor-wise (FB) ML-SFFS fusion with the same classifiers.',
   'DNNs are not used, because 432 plot-dates from 72 plots are too few to train them reliably.',
   'Where physiological parameters change significantly before symptoms, PLSR and RFR estimate them from the selected features (ORW Activity 3.1).',
   'Metrics: OA, kappa, sensitivity, specificity, F1 (Section 5.5).'],
  'Tian et al. (2021); Mustafa et al. (2023); Mahlein et al. (2019).'));
K.push(...STEPEND(`Pre-symptomatic models for S1–S8 with sensitivity, specificity, OA, kappa and F1; the best early-warning sensor set; PLSR/RFR estimates of early physiological change.`, [
  `**Anomaly detection** (isolation forest) trained on healthy plots only (Liu et al., 2008).`,
  `**Recurrent networks (LSTM)** on time series of features when many flights are available (Hochreiter and Schmidhuber, 1997).`,
  `**Fusion of spectra with texture** for early detection (Zhu et al., 2017).`
]));
K.push(...STEP('Step 3.4. Risk maps',
  'Map the probability of infection of each plot.',
  'Practical early-warning output.',
  'Class probabilities of the best model are mapped plot by plot (mapping approach of Liu et al., 2024).',
  'Liu et al. (2024).'));
K.push(...STEPEND(`Plot-wise infection-probability (risk) maps for each pre-symptomatic flight.`, [
  `**Weather-based risk models** combined with spectral data, as in the multi-stage scheme of Bhattacharya and Chattopadhyay (2013).`,
  `**Kriging** of plot probabilities into continuous risk surfaces (Oliver and Webster, 1990).`
]));
K.push(BOX('How Objective 3 is satisfied:', 'the pooled pre-symptomatic models show whether white rust can be predicted before symptoms and which sensor or fusion gives the best early warning; risk maps show where infection is developing.', 'FCE4EC', 'AD1457'));

// ======================= 9 VALIDATION =======================
K.push(H1('7. Validation design'));
K.push(...STEP('Step V1. Leave-one-replication-out cross-validation (IARI 2025–26)',
  'Train on two replications and test on the third; repeat three times (' + F('design') + ').',
  'Each RBD replication contains every treatment once, so each test fold is a balanced copy of the experiment. All observations of a plot stay in the same fold, so no test plot is seen during training (Roberts et al., 2017).',
  ['Outer loop: R1, R2 and R3 held out in turn. Inner loop (two training replications): 4-fold cross-validation grouped by plot for Boruta, HS band selection, VIF, ML-SFFS and tuning.',
   'Reported performance: mean ± standard deviation over the three test replications. The final model is refitted on all IARI data.'],
  'Roberts et al. (2017); Ambroise and McLachlan (2002); Varma and Simon (2006).'));
K.push(INCASE(`In each outer fold, the 48 plots of two replications (all their dates) form the training set and the 24 plots of the third replication form the test set. Inside the training set, 4-fold cross-validation grouped by plot (12 plots per inner fold) is used for every data-driven choice: Boruta, ReliefF, VIF, ML-SFFS and hyperparameter tuning. The test replication is touched only once, to compute the reported metrics. Because each replication contains every treatment exactly once, every test fold has the same mix of varieties, inoculation timings and controls.`));
K.push(...STEPEND(`Mean ± SD of every metric over the three held-out replications for every configuration, and final models refitted on all IARI data.`, [
  `**Spatial block cross-validation** with blocks defined by distance (Roberts et al., 2017).`,
  `**Repeated grouped k-fold** or **leave-one-plot-out** cross-validation.`,
  `**.632+ bootstrap** error estimation (Efron and Tibshirani, 1997).`
]));
K.push(...STEP('Step V2. Two-stage independent validation (2026–27)',
  'Test the final models on data never used for development.',
  'Validation on a separate experiment is the strongest test of transferability (Feng et al., 2022).',
  ['Stage 1: planned experiment at the IIRMR Research Farm, Bharatpur (local varieties).',
   'Stage 2: adjoining farmers\' fields with the same ground-truth survey.'],
  'Feng et al. (2022); ORW Activity 2.3.'));
K.push(...STEPEND(`Accuracy of the final models at Bharatpur and in farmers' fields, showing how well they transfer to new sites, varieties and management.`, [
  `**Domain adaptation or transfer learning** to adjust models to a new site (Tuia et al., 2016).`,
  `**Multi-season validation** in a second year (Tian et al., 2021; Mustafa et al., 2023).`,
  `**Indirect validation** through the impact of disease on canopy cover or yield (Bhattacharya and Chattopadhyay, 2013; Nguyen et al., 2023).`
]));
K.push(...tab2('runs', [
  ['Input sets', 'Strategy', 'Detection (D) and severity (S)', 'Regression (R)'],
  ['S1–S4', 'a: DSF → VIF → ML-SFFS', 'SVM, RF, k-NN; DNN-F1 (DSF + VIF)', 'SVR, RFR, k-NN; PLSR, DNN-F1 (DSF + VIF)'],
  ['S5–S8', 'FA: pooled ML-SFFS', 'SVM, RF, k-NN', 'SVR, RFR, k-NN'],
  ['S5–S8', 'FB: sensor-wise ML-SFFS', 'SVM, RF, k-NN', 'SVR, RFR, k-NN'],
  ['S5–S8', 'Concatenation (DSF + VIF)', '–', 'PLSR'],
  ['S5–S8', 'FC / FD: DNN-F1 / DNN-F2', 'DNN-F1, DNN-F2 (softmax)', 'DNN-F1, DNN-F2 (linear output)'],
], [1500, 2500, 2600, 2706], 'Complete modelling plan of Objective 2 (Objective 3 uses the SVM, RF and k-NN rows of D).', 16));
K.push(H2('7.1 Software'));
K.push(P('Python with scikit-learn (Pedregosa et al., 2011) for SVM, RF, k-NN and PLSR; mlxtend (Raschka, 2018) for SFFS, as used by Mustafa et al. (2023); Boruta (Kursa and Rudnicki, 2010); statsmodels and SciPy for VIF and tests; TensorFlow/Keras for DNN-F1 and DNN-F2, as in Maimaitijiang et al. (2020). Equivalent R packages (Boruta, caret, e1071, kknn; Tian et al., 2021) may be used, as planned in the ORW.'));
K.push(H1('8. Algorithms and machine-learning techniques in detail'));
K.push(P(`This chapter explains every algorithm used in Chapters 3–7: what it is, how it works (with equations), its hyperparameters and the values planned in the thesis, why it is used for white rust, its strengths and limitations, and an **In my case** example showing how it works with the white rust data. Worked numbers are illustrative.`));
K.push(H2('8.1 Overview: where each technique is used'));
K.push(P('The thesis develops supervised machine-learning models from UAV RGB, multispectral (MS), hyperspectral (HS) and thermal (TIR) features. **Supervised learning** means that every training sample (a plot on a flight date) has a known label: healthy or diseased, a severity class (Low ≤ 25%, Moderate 25–50%, High > 50% disease index) or the disease index (DI) itself. **Classification** predicts a class; **regression** predicts a number. ' + F('mloverview') + ' and ' + T('mlcomponents') + ' show the components and where they are used.'));
K.push(...fig2('mloverview', 'g1_overview.png', 'Machine-learning components of the thesis, from data to evaluation.', 560));
K.push(...tab2('mlcomponents', [
  ['Component', 'Technique', 'Type', 'Used in'],
  ['Feature relevance', 'ReliefF / RReliefF', 'Filter (instance-based weighting)', 'Objective 1 (HS bands, WRI; all sensors as a check)'],
  ['Feature relevance', 'Boruta', 'Wrapper (all-relevant, random forest)', 'Objective 1: disease-specific feature (DSF) pools'],
  ['Redundancy removal', 'Variance inflation factor (VIF)', 'Statistical filter', 'Objectives 2, 3'],
  ['Optimum combination', 'ML-SFFS', 'Wrapper (floating search with a model)', 'Objectives 2, 3; ML-SFFS fusion'],
  ['Classification / regression', 'SVM / SVR', 'Kernel method', 'Objectives 2, 3'],
  ['Classification / regression', 'Random forest / RFR', 'Ensemble of decision trees', 'Objectives 2, 3; basis of Boruta'],
  ['Classification / regression', 'k-nearest neighbours', 'Instance-based (lazy) learner', 'Objectives 2, 3'],
  ['Regression', 'PLSR', 'Linear latent-variable model', 'Objective 2 (DI)'],
  ['Classification / regression', 'DNN-F1, DNN-F2', 'Deep neural networks (feature-level fusion)', 'Objective 2'],
  ['Validation', 'Nested, grouped cross-validation; external test', 'Model assessment', 'Objectives 2, 3'],
], [2200, 2400, 2500, 2206], 'Machine-learning components and their use.', 16));

// ===== 2 BASICS =====
K.push(H2('8.2 Foundations of machine learning'));
K.push(H3('8.2.1 Overfitting, bias–variance and the Hughes phenomenon'));
K.push(P('A model that is too simple misses real patterns (**underfitting**, high bias); a model that is too flexible learns noise in the training data (**overfitting**, high variance) and performs poorly on new plots (' + F('mloverfit') + 'a). With hyperspectral data the risk is large: for a fixed number of samples, classification accuracy first rises and then falls as more features are added — the **Hughes phenomenon** (Hughes, 1968; ' + F('mloverfit') + 'b). This is why the thesis uses feature selection (Boruta, VIF, ML-SFFS) and regularised models, and why performance is always measured on plots not used for training.'));
K.push(...fig2('mloverfit', 'g2_overfit.png', '(a) Training and test error against model complexity; (b) test accuracy against number of features for a fixed sample size (illustrations).', 540));
K.push(INCASE(`The post-symptomatic dataset is planned as about 1296 plot-dates, but they come from only 72 plots, so the effective number of independent samples is much smaller. The hyperspectral sensor alone gives 1443 band-level features plus indices. Without reduction, a flexible model could separate the training plots perfectly and fail on the test replication. This is why every model in the thesis sees only a few features: band-level reduction (Steps 1.2–1.3), Boruta, VIF and ML-SFFS reduce hundreds of candidates to an optimum combination of typically fewer than ten.`));
K.push(H3('8.2.2 Feature scaling'));
K.push(P('Features have different units (reflectance 0–1, temperature in °C, texture values of different ranges). Distance- and gradient-based methods would be dominated by large-valued features, so each feature is standardised with the mean μ and standard deviation σ of the **training** data only:'));
K.push(EQ('z = (x − μ_{train}) / σ_{train}', '8.1'));
K.push(...tab2('mlscaling', [
  ['Method', 'Scaling needed?', 'Reason'],
  ['SVM / SVR (RBF)', 'Yes', 'Kernel uses Euclidean distance'],
  ['k-NN', 'Yes', 'Prediction is based on distances'],
  ['ReliefF', 'Yes (or range-normalised diff)', 'Uses nearest neighbours'],
  ['PLSR', 'Yes (mean-centred, usually autoscaled)', 'Variance of features affects latent components'],
  ['DNN', 'Yes', 'Gradient descent converges poorly with unequal scales'],
  ['Random forest, Boruta', 'No', 'Tree splits depend only on the order of values'],
  ['VIF', 'Not required', 'R^{2} is scale-invariant'],
], [2600, 2800, 3906], 'Which methods need feature scaling.', 17));
K.push(INCASE(`Features in this thesis have very different ranges: reflectance 0–0.5, CTD about −5 to +3 °C, GLCM contrast 0–50 or more, REP 700–730 nm. Without standardisation the RBF kernel of SVM and the distance of k-NN would be dominated by contrast and REP. The mean and standard deviation are computed on the two training replications of each outer fold and then applied unchanged to the test replication.`));
K.push(H3('8.2.3 Class imbalance'));
K.push(P('Severity classes are unlikely to be equally frequent. Three measures are used: (i) stratified folds, so each fold keeps the class proportions; (ii) class weights inversely proportional to class size in SVM and RF (the "balanced" option of scikit-learn); (iii) macro-averaged F1 and kappa as main metrics, because overall accuracy can look high when a model ignores a rare class.'));
K.push(EQ('w_{k} = N / (K × n_{k})', '8.2'));
K.push(P('where N is the number of training samples, K the number of classes and n_{k} the number of samples in class k. Errors on a rare class therefore cost more during training.'));
K.push(INCASE(`If, in the training set of one fold, there are 600 Low, 300 Moderate and 150 High plot-dates (N = 1050, K = 3), Eq. 8.2 gives weights w_{Low} = 1050/(3 × 600) = 0.58, w_{Moderate} = 1.17 and w_{High} = 2.33. Misclassifying a High plot then costs four times as much as misclassifying a Low plot, so the model cannot ignore the rare class. Macro-F1 weights the three classes equally when results are reported.`));
K.push(H3('8.2.4 Data leakage and grouped data'));
K.push(P('If any step that looks at the labels (feature selection, tuning) uses test samples, the reported accuracy is optimistic — **selection bias** (Ambroise and McLachlan, 2002; Varma and Simon, 2006). Also, the same plot observed on several dates is not independent; if one date is in training and another in testing, the model may recognise the plot rather than the disease. Therefore every split keeps all observations of a plot together (grouped cross-validation; Roberts et al., 2017), and all selection and tuning are done inside the training folds (Section 8.8; Chapter 7).'));

// ===== 3 FEATURE SELECTION =====
// ===== 8.3 Feature-extraction algorithms (new) =====
K.push(H2('8.3 Feature-extraction algorithms'));
K.push(H3('8.3.1 Savitzky–Golay smoothing and derivative spectra'));
K.push(P(`Hyperspectral spectra contain random noise that is amplified by differentiation. The Savitzky–Golay (SG) filter fits a low-order polynomial by least squares to the 2m + 1 points of a moving window and replaces the centre point by the value (or the derivative) of that polynomial (Savitzky and Golay, 1964). For a quadratic or cubic polynomial this is equivalent to a weighted moving average with fixed convolution coefficients c_{j}:`));
K.push(EQ('R̃(λ_{i}) = Σ_{j=−m}^{m} c_{j} R(λ_{i+j})', '8.3'));
K.push(P(`Unlike a simple moving average, SG preserves the height and position of absorption features. The same polynomial gives the first and second derivatives analytically. First derivatives (FD) remove additive offsets such as background or illumination differences and highlight slopes, especially the red edge; second derivatives (SD) remove linear trends and separate overlapping absorption features (Tsai and Philpot, 1998). The window must be wide enough to suppress noise but narrower than the features of interest; a window of about 9–11 bands with a second-order polynomial is typical (Shukla et al., 2024, used 9 nm).`));
K.push(INCASE(`Each plot-mean hyperspectral spectrum (481 retained bands) is smoothed with SG, and FD and SD are computed from the same fit. The red-edge position REP is the wavelength of maximum FD between 680 and 750 nm; as white rust reduces chlorophyll, REP is expected to move to shorter wavelengths and the FD peak amplitude Dr to fall, as observed for rice blast by Mandal et al. (2022).`));
K.push(H3('8.3.2 Vegetation indices'));
K.push(P(`A vegetation index combines two or three bands so that the response to one property (for example chlorophyll) is enhanced and the response to others (illumination, soil, leaf angle) is reduced. **Ratio** indices (SR = R_{NIR}/R_{red}) and **normalised differences** (ND = (R_{a} − R_{b})/(R_{a} + R_{b}), bounded between −1 and +1) cancel multiplicative illumination effects; **soil-adjusted** and **triangular** indices (MCARI, TCARI, MTVI) reduce soil and LAI effects; **narrow-band physiological** indices (PRI, PSRI, ARI, NPCI) target specific pigments. Chapter 4 lists the 39 hyperspectral and 12 multispectral indices with their original formulas.`));
K.push(H3('8.3.3 Grey-level co-occurrence matrix (GLCM) texture'));
K.push(P(`Texture describes the spatial arrangement of grey levels. The image (one band) is quantised into N_{g} grey levels; for a given distance d and direction θ, the GLCM counts how often a pixel with level i has a neighbour with level j. The counts are made symmetric and normalised to probabilities P(i, j) (Haralick et al., 1973). Texture measures are then computed from P (${F('glcm')}):`));
K.push(EQ('Contrast = Σ_{i,j} P(i,j) (i − j)^{2};    Homogeneity = Σ_{i,j} P(i,j) / [1 + (i − j)^{2}]'));
K.push(EQ('Entropy = − Σ_{i,j} P(i,j) ln P(i,j);    Second moment = Σ_{i,j} P(i,j)^{2}', '8.4'));
K.push(P(`Here i and j are grey levels, not pixel coordinates. Mean, variance, dissimilarity and correlation are defined similarly. Entropy is sometimes computed with log_{2}; the base changes only the scale.`));
K.push(...fig2('glcm', 'n7_glcm.png', 'Worked GLCM example: (a) a 4 × 4 image with four grey levels; (b) symmetric co-occurrence counts for horizontal neighbours (distance 1, angle 0°); (c) texture measures computed from P = counts/24.', 560));
K.push(INCASE(`For each plot, the RGB bands, the five MS bands and the thermal image are quantised (for example to 32 levels) and the GLCM is computed for distance 1 and averaged over the four directions (0°, 45°, 90°, 135°) to make the measures independent of row direction. Eight measures per band give 24 RGB, 40 MS and 8 thermal textures. On a uniform healthy canopy, neighbouring pixels have similar levels, P is concentrated on the diagonal, homogeneity is high and contrast low; white pustules and chlorotic patches spread P away from the diagonal, increasing contrast, dissimilarity and entropy.`));
K.push(H3('8.3.4 Canopy segmentation by K-means'));
K.push(P(`Plot means must use canopy pixels only. K-means clustering divides pixels into K groups (for example canopy, soil, shadow) by minimising the within-cluster sum of squared distances between each pixel vector x_{i} and the centre μ_{k} of its cluster k (MacQueen, 1967):`));
K.push(EQ('J = Σ_{k=1}^{K} Σ_{i ∈ k} ‖x_{i} − μ_{k}‖^{2}', '8.5'));
K.push(P(`The algorithm alternates two steps until assignments stop changing: assign each pixel to the nearest centre, then recompute each centre as the mean of its pixels. The cluster with the highest NDVI (MS, HS) or the coolest temperature during the day (TIR) is the canopy (Feng et al., 2022). Because yellow mustard flowers lower NDVI, the threshold or cluster assignment is checked on every flight.`));
K.push(H3('8.3.5 Thermal indices'));
K.push(P(`Raw canopy temperature (CT, the mean of canopy pixels) depends on the weather of each flight, so normalised indices are computed for each plot (Section 4.1.4; Feng et al., 2022; Maimaitijiang et al., 2020): CTD = CT − AT, where AT is air temperature (negative when transpiration cools the canopy); CTR = (CT + 273.15)/(AT + 273.15), a ratio computed in kelvin; NRCT = (CT − CT_{min})/(CT_{max} − CT_{min}), where CT_{min} and CT_{max} are the lowest and highest canopy temperatures in the same thermal image; and MTD, the maximum minus minimum canopy temperature within the plot (Mahlein et al., 2019). NRCT is scaled 0–1 within each image, which removes most of the between-flight weather effect when dates are pooled.`));
// ===== 8.4 Statistical tests (new) =====
K.push(H2('8.4 Statistical tests'));
K.push(P(`Statistical tests answer whether a feature differs between groups more than expected by chance. In this thesis they **describe and rank** features in Objective 1; generalisation is judged only by cross-validated models. Repeated plot-dates are not independent, so p-values are optimistic, and many features are tested, so p-values are adjusted for multiple comparisons (Holm, 1979) or interpreted together with effect sizes.`));
K.push(H3('8.4.1 Checking assumptions: Shapiro–Wilk and Levene'));
K.push(P(`Parametric tests assume normally distributed values with equal variances. The **Shapiro–Wilk** test compares the ordered sample with the values expected under normality; W close to 1 indicates normality (Shapiro and Wilk, 1965). **Levene's** test applies ANOVA to the absolute deviations of each value from its group mean (or median, in the robust Brown–Forsythe form); a significant result means unequal variances (Levene, 1960). With large samples, small departures become significant, so histograms and Q–Q plots are inspected as well.`));
K.push(H3('8.4.2 Two groups: t-test and Mann–Whitney U'));
K.push(P(`For detection (healthy vs diseased) the **t-test** compares means. With unequal variances the Welch form is used (Welch, 1947):`));
K.push(EQ('t = (x̄_{1} − x̄_{2}) / √( s_{1}^{2}/n_{1} + s_{2}^{2}/n_{2} )', '8.6'));
K.push(P(`If the data are not normal, the **Mann–Whitney U test** ranks all values together and compares the rank sums: U_{1} = R_{1} − n_{1}(n_{1} + 1)/2, where R_{1} is the sum of ranks of group 1 (Mann and Whitney, 1947). U/(n_{1}n_{2}) is the probability that a random diseased plot has a higher value than a random healthy plot, a useful effect size. The **point-biserial correlation** (Pearson r between the feature and 0/1 health status) measures the strength of the difference.`));
K.push(H3('8.4.3 Three or more groups: ANOVA, Tukey HSD, Kruskal–Wallis and Dunn'));
K.push(P(`For severity (healthy, Low, Moderate, High) one-way **ANOVA** compares the variance between group means with the variance within groups:`));
K.push(EQ('F = [ Σ_{g} n_{g} (x̄_{g} − x̄)^{2} / (G − 1) ] / [ Σ_{g} Σ_{i} (x_{gi} − x̄_{g})^{2} / (N − G) ]', '8.7'));
K.push(P(`A significant F says that at least one group differs; **Tukey's HSD** test then compares every pair of groups while keeping the family-wise error rate at α (Tukey, 1949). The rank-based alternative is the **Kruskal–Wallis H test** (Kruskal and Wallis, 1952), followed by **Dunn's test** for pairs with Holm or Bonferroni adjustment (Dunn, 1964). The pattern of significant pairs is important for white rust: a feature that separates healthy from Low is useful for detection; one that separates Low, Moderate and High is useful for severity discrimination.`));
K.push(H3('8.4.4 Correlation: Pearson and Spearman'));
K.push(P(`Pearson's r measures linear association; Spearman's ρ is Pearson's r computed on ranks and measures any monotonic association, so it is robust to non-linearity and outliers (Spearman, 1904). Because DI has many zeros (healthy plots), ties are given their average rank. ρ is used for the correlation scalograms (Step 1.2) and for every feature–DI relation; Pearson r is reported alongside for comparison with the literature.`));
K.push(INCASE(`For each feature of each sensor the output is one row: mean ± SD per group (healthy, Low, Moderate, High), the detection test and its p-value, the severity test, the significant pairs (e.g. "H–L, H–M, H–Hi, L–Hi"), Spearman ρ with DI and the correlation with the most related physiological parameter. Sorting these rows by |ρ| and by the number of separated pairs gives a transparent first ranking that is later confirmed (or not) by Boruta.`));

K.push(H2('8.5 Feature-selection techniques'));
K.push(P('Feature-selection methods are grouped into **filters** (rank features by a statistic, independent of the final model), **wrappers** (evaluate feature subsets with a learning model) and **embedded** methods (selection happens during model training, e.g. LASSO) (Guyon and Elisseeff, 2003). The thesis uses a filter (ReliefF), two wrappers (Boruta, SFFS) and a statistical redundancy filter (VIF).'));
K.push(H3('8.5.1 ReliefF'));
K.push(LBL('What it is'));
K.push(P('A filter that weights each feature by how well it separates samples that are close to each other but belong to different classes (Kononenko, 1994; Robnik-Šikonja and Kononenko, 2003). It extends the original two-class Relief to several classes and noisy data.'));
K.push(LBL('How it works'));
K.push(NL('Set all weights W(A) = 0.'));
K.push(NL('Repeat m times: pick a sample x; find its k nearest neighbours of the same class (nearest hits H_{j}) and k nearest neighbours of each other class C (nearest misses M_{j}(C)).'));
K.push(NL('Update each feature weight with Eq. 8.8: a feature loses weight if it differs between x and its hits (bad: it separates similar samples of the same class) and gains weight if it differs between x and its misses (good: it separates classes).'));
K.push(EQ('W(A) ← W(A) − Σ_{j=1}^{k} diff(A, x, H_{j}) / (m k)'));
K.push(EQ('+ Σ_{C ≠ c(x)} [ P(C) / (1 − P(c(x))) ] Σ_{j=1}^{k} diff(A, x, M_{j}(C)) / (m k)', '8.8'));
K.push(P('diff(A, x, y) = |A(x) − A(y)| / (max(A) − min(A)) for numeric features; P(C) is the prior probability of class C, which weights misses from each class. **RReliefF** replaces classes by a continuous target (DI) for regression.'));
K.push(LBL('Specification in the thesis'));
K.push(BL('k = 10 neighbours (the usual default); m = all training samples; features standardised; neighbours from the same plot (other dates) excluded; run separately for detection (2 classes), severity (3 classes) and, as RReliefF, for DI.'));
K.push(BL('Relevant features: positive weight and in the top part of the ranking (e.g. top 5% of hyperspectral bands; top 25% for the WRI search of Mahlein et al., 2013).'));
K.push(LBL('Strengths and limitations'));
K.push(BL('Strengths: fast (cost about m × N × d operations); detects features that are useful only together (interactions); robust to noise; handles several classes; suits overlapping classes because it uses local neighbourhoods.'));
K.push(BL('Limitations: gives a ranking but no automatic cut-off; does not remove redundancy (two correlated features get similar weights); affected by many irrelevant features in the distance computation.'));
K.push(INCASE(`ReliefF is used on the hyperspectral band-level features (R, FD and SD of 481 bands = 1443 features) twice: with health status (detection) and with the three severity classes. Each plot-date looks for its 10 nearest hits and misses among plot-dates of **other** plots (same-plot dates are excluded, because they would be near-duplicates). The top 5% of features (about 72) are kept, and only the highest-weighted band in each spectral region survives, so a handful of robust bands remain. In Step 1.3 ReliefF also ranks bands and normalised differences for the White Rust Index search.`));
K.push(H3('8.5.2 Boruta'));
K.push(LBL('What it is'));
K.push(P('An **all-relevant** wrapper built around random forest (Kursa and Rudnicki, 2010). Instead of finding the smallest good subset, it finds every feature that carries more information than random noise — ideal for characterising which features respond to disease (Mustafa et al., 2023).'));
K.push(LBL('How it works (' + F('mlborsffs') + 'a)'));
K.push(NL('For every feature, create a **shadow feature** by randomly shuffling its values; shadows have no relation with the target.', 'num2'));
K.push(NL('Train a random forest on real + shadow features and compute the importance of each (by default the permutation importance as a Z-score: mean decrease in accuracy divided by its standard deviation).', 'num2'));
K.push(NL('Record a **hit** for each real feature whose importance exceeds the maximum importance among shadow features (MZSA).', 'num2'));
K.push(NL('Repeat with new shuffles. After each run, a two-sided binomial test (hits vs. the 50% expected by chance, Bonferroni-corrected) labels features **confirmed** (significantly more hits) or **rejected** (significantly fewer); rejected features are removed.', 'num2'));
K.push(NL('Stop when all features are decided or the maximum number of runs is reached; undecided features are **tentative**.', 'num2'));
K.push(EQ('Z_{A} = mean(I_{A}) / sd(I_{A});    hit if Z_{A} > max_{shadow} Z', '8.9'));
K.push(LBL('Specification in the thesis'));
K.push(BL('maxRuns = 100, p-value 0.01, multiple-comparison correction on (R package defaults); random forest with 500 trees; run per sensor for detection, severity and DI; confirmed features = DSF pool.'));
K.push(BL('Note: the R package uses permutation importance by default; the Python BorutaPy uses the impurity (Gini) importance of the forest — report which was used.'));
K.push(LBL('Strengths and limitations'));
K.push(BL('Strengths: statistically grounded cut-off; captures non-linear and interacting effects; no scaling needed.'));
K.push(BL('Limitations: keeps correlated relevant features (redundancy must be removed by VIF); slower than filters; importance can be biased towards features with many distinct values (Strobl et al., 2007).'));
K.push(INCASE(`For the multispectral detection task, Boruta adds 57 shadow features (shuffled copies) to the 57 real features, so the random forest sees 114 columns. In each of up to 100 runs, a real feature scores a hit if its importance beats the best shadow. After enough runs, a feature like NDRE that beats the shadows in nearly every run is confirmed; a blue-band texture that rarely beats them is rejected. Confirmed features become the MS detection DSF pool; the same is repeated for severity and DI and for every sensor.`));
K.push(H3('8.5.3 Variance inflation factor (VIF)'));
K.push(P('VIF measures multicollinearity: how well a feature can be predicted from the other features (Kutner et al., 2005).'));
K.push(EQ('VIF_{j} = 1 / (1 − R_{j}^{2})', '8.10'));
K.push(P('R_{j}^{2} is the coefficient of determination when feature j is regressed on all other features. VIF = 1 means no collinearity; **VIF = 10 corresponds to R_{j}^{2} = 0.90**, i.e. 90% of the feature is explained by the others; VIF = 20 corresponds to R_{j}^{2} = 0.95. The thesis removes the feature with the largest VIF, recomputes, and stops when all VIF < 10 (Tian et al., 2021; Mustafa et al., 2023). Tolerance = 1/VIF is sometimes reported instead.'));
K.push(H3('8.5.4 Sequential floating forward selection (ML-SFFS)'));
K.push(LBL('What it is'));
K.push(P('A wrapper search proposed by Pudil et al. (1994). Plain **sequential forward selection (SFS)** adds the best feature at each step but can never remove one ("nesting problem"); **sequential backward selection (SBS)** removes but never re-adds. **SFFS** adds a feature and then conditionally removes features as long as this improves the criterion, so it corrects early wrong choices. When a machine-learning model provides the criterion, it is called ML-SFFS (Tian et al., 2021).'));
K.push(LBL('How it works (' + F('mlborsffs') + 'b)'));
K.push(NL('**Start** with an empty subset; the criterion J(X) is the cross-validated performance of the model trained on subset X (macro-F1 or accuracy for classification, negative RMSE for regression).', 'num3'));
K.push(NL('**Step 1 – Inclusion:** add the feature that gives the highest J.', 'num3'));
K.push(NL('**Step 2 – Conditional exclusion:** find the least significant feature in the subset (whose removal lowers J least); remove it only if it is not the feature just added and the reduced subset has a higher J than the best subset of that size found before.', 'num3'));
K.push(NL('**Step 3 – Continued exclusion:** repeat Step 2 while J improves, then go back to Step 1.', 'num3'));
K.push(NL('**Stop** at the maximum subset size; the optimum feature combination (OFC) is the subset with the highest J (the smaller one if tied).', 'num3'));
K.push(...fig2('mlborsffs', 'g7_boruta_sffs.png', '(a) Boruta importance boxplots with shadow features (illustration); (b) the SFFS search loop.', 540));
K.push(...tab2('mlsffsex', [
  ['Round', 'Step 1 (add)', 'Subset, J', 'Steps 2–3 (check)', 'Best J by size'],
  ['1', 'WRI best alone', '{WRI} 0.72', 'Only feature: skip', '1: 0.72'],
  ['2', '+CTD best', '{WRI, CTD} 0.80', 'Removing WRI gives 0.62 < 0.72: keep', '2: 0.80'],
  ['3', '+ENT best', '{WRI, CTD, ENT} 0.84', 'Removing WRI gives 0.82 > 0.80: remove WRI', '3: 0.84; 2: 0.82'],
  ['4', '+PSSRa best', '{CTD, ENT, PSSRa} 0.86', 'No removal improves J', '3: 0.86'],
  ['5', '+NDRE', '4 features, 0.86', 'No removal improves J', '4: 0.86'],
], [900, 1600, 2300, 2800, 1706], 'Worked SFFS example (illustrative J values). OFC = {CTD, ENT, PSSRa}: the first-chosen feature (WRI) was later dropped, which plain SFS cannot do.', 16));
K.push(LBL('Specification in the thesis'));
K.push(BL('Maximum subset size 10; J from 4-fold cross-validation grouped by plot, repeated 10 times (Tian et al., 2021, used 100); the most frequently selected subset is the OFC; run separately for SVM, RF and k-NN (and SVR, RFR, k-NN for regression).'));
K.push(BL('Implementation: mlxtend SequentialFeatureSelector(estimator, k\\_features=(1, 10), forward=True, floating=True, scoring=..., cv=GroupKFold) (Raschka, 2018), as used by Mustafa et al. (2023).'));
K.push(BL('Cost: many model fits (roughly d to d^{2} subsets per size, each cross-validated), so it is applied after Boruta and VIF have reduced the feature set.'));
K.push(...tab2('mlfscompare', [
  ['Method', 'Type', 'Output', 'Removes redundancy?', 'Role in thesis'],
  ['ReliefF', 'Filter', 'Weight per feature', 'No', 'HS band ranking; WRI; check on Boruta'],
  ['Boruta', 'Wrapper (all-relevant)', 'Confirmed / tentative / rejected', 'No', 'DSF pool (Objective 1)'],
  ['VIF', 'Statistical filter', 'VIF per feature', 'Yes', 'Before ML-SFFS'],
  ['ML-SFFS', 'Wrapper (minimal-optimal)', 'Optimum subset for a model', 'Yes (implicitly)', 'OFC; ML-SFFS fusion'],
], [1500, 1900, 2200, 1500, 2206], 'Comparison of the feature-selection techniques.', 16));

// ===== 4 MODELS =====
K.push(INCASE(`After VIF a task-specific pool typically has 8–15 features. ML-SFFS then searches subsets of up to 10 features. Each candidate subset is scored by grouped 4-fold cross-validation inside the training replications, repeated 10 times with different fold assignments, for each of SVM, RF and k-NN separately. The subset chosen most often is the optimum feature combination (OFC) of that model. An OFC such as {PSSRa, WRI, CTD} is easy to interpret: one pigment index, one disease-specific index and one thermal feature.`));
K.push(H3('8.5.5 Jeffries–Matusita (JM) distance'));
K.push(P(`JM measures how separable two classes are in a feature space, assuming each class is normally distributed (Richards, 2013). It is computed from the Bhattacharyya distance B (Eq. 4.6) and ranges from 0 (identical distributions) to 2 (no overlap); values above about 1.9 indicate good separability. For a single feature with equal variance σ^{2} in both classes, B reduces to:`));
K.push(EQ('B = (1/8) (μ_{1} − μ_{2})^{2} / σ^{2},     JM = 2 [1 − exp(−B)]', '8.11'));
K.push(INCASE(`Suppose PSSRa has a mean of 0.30 in Low and 0.36 in Moderate plots with a standard deviation of 0.03 in both. Then B = (1/8)(0.06)^{2}/0.0009 = 0.5 and JM = 2(1 − e^{−0.5}) = 0.79: the classes overlap strongly. Between healthy (mean 0.30) and High (mean 0.42), B = (1/8)(0.12)^{2}/0.0009 = 2 and JM = 2(1 − e^{−2}) = 1.73: much better, but not complete separation. This is how JM explains confusion between adjacent severity classes (as for rice blast levels 4 and 5 in Mandal et al., 2023). Because JM assumes normality and saturates at 2, it is used only to report separability, not to select features.`));
K.push(H3('8.5.6 Linear and canonical discriminant analysis'));
K.push(P(`Discriminant analysis looks for linear combinations of the features, z = w^{T}x, that separate predefined groups as well as possible (Fisher, 1936). With S_{W} the pooled within-group scatter matrix and S_{B} the between-group scatter matrix, Fisher's criterion is maximised:`));
K.push(EQ('J(w) = (w^{T} S_{B} w) / (w^{T} S_{W} w)   →   S_{W}^{−1} S_{B} w = λ w', '8.12'));
K.push(P(`The eigenvectors w_{1}, w_{2}, … are the **canonical discriminant functions** and the eigenvalues λ_{i} measure how strongly each separates the groups; with G groups and p features there are at most min(G − 1, p) functions (3 for healthy, Low, Moderate and High). The overall significance is tested with **Wilks' lambda**, the ratio of within-group to total scatter, and the strength of each function with its **canonical correlation** r_{i}:`));
K.push(EQ('Λ = |S_{W}| / |S_{W} + S_{B}| = Π_{i} 1/(1 + λ_{i});     r_{i} = √[ λ_{i} / (1 + λ_{i}) ]', '8.13'));
K.push(P(`Λ near 0 means well-separated groups and Λ = 1 means no separation; Bartlett's approximation χ^{2} = −[N − 1 − (p + G)/2] ln Λ with p(G − 1) degrees of freedom gives a significance test (Huberty and Olejnik, 2006). **Stepwise discriminant analysis** enters at each step the feature that most reduces Λ and removes features that no longer contribute, as used by Bhattacharya and Chattopadhyay (2013) for mustard rot. As a **classifier (LDA)**, a sample is assigned to the group with the nearest centroid in the discriminant space (equivalently, the highest posterior probability under normal distributions with a common covariance matrix). LDA assumes multivariate normality and equal group covariance matrices (checked with Box's M test; Box, 1949); quadratic discriminant analysis (QDA) relaxes the equal-covariance assumption (Das et al., 2020).`));
K.push(INCASE(`Canonical discriminant analysis is used in Objective 1 (Step 1.6) as a multivariate description: for each sensor it shows whether healthy, Low, Moderate and High differ significantly (Wilks' Λ), how many independent directions of separation exist, which DSFs define them (standardised coefficients and structure correlations) and where the classes overlap (canonical score plot). Its cross-validated accuracy is a simple linear benchmark against which SVM, RF and k-NN in Objective 2 can be compared.`));
K.push(H3('8.5.7 PCA and PLSR loading weights for band selection'));
K.push(P(`**Principal component analysis** decomposes the centred spectral matrix X (samples × bands) into scores T and loadings P, X = T P^{T} + E, where each principal component is a weighted sum of all bands and the loading p_{kj} is the weight of band j in component k (Jolliffe, 2002). PCA is unsupervised: components maximise spectral variance. **PLSR** (Section 8.6.4) instead chooses latent factors that maximise covariance with the response (DI, or dummy-coded classes in PLS discriminant analysis; Barker and Rayens, 2003). In both, bands with the largest positive or negative loading weights — the local maxima and minima of the loading curves — contribute most to the components that separate the classes. Shukla et al. (2024) used the loading weights of the first three PCs and PLS factors of mustard canopy spectra to select 500, 679, 746 and 979 nm (PCA) and 491, 679, 746 and 979 nm (PLSR) as the dominant bands for discriminating aphid severity grades.`));
K.push(INCASE(`In Step 1.2 (Sub-step F), PCA and PLS(-DA) are fitted on the plot-mean hyperspectral reflectance of healthy and diseased plot-dates. If, for example, the PLS loading curves peak near the red edge and in the SWIR and these bands were also selected by the correlation scalograms and ReliefF, they are confirmed as robust white-rust bands. Bands that appear only in PCA loadings may reflect canopy or illumination variation unrelated to disease, which is why the supervised PLS loadings carry more weight.`));
K.push(H2('8.6 Models'));
K.push(H3('8.6.1 Support vector machine (SVM) and support vector regression (SVR)'));
K.push(LBL('Idea'));
K.push(P('SVM finds the hyperplane that separates two classes with the **largest margin** — the largest distance to the nearest training samples, called **support vectors** (Cortes and Vapnik, 1995; ' + F('mlsvm') + 'a). A large margin generalises well to new data.'));
K.push(LBL('Soft-margin formulation'));
K.push(P('Real classes overlap, so slack variables ξ_{i} allow some samples inside the margin or on the wrong side, at a cost C:'));
K.push(EQ('minimise  (1/2) ‖w‖^{2} + C Σ_{i} ξ_{i}'));
K.push(EQ('subject to  y_{i} (w · φ(x_{i}) + b) ≥ 1 − ξ_{i},   ξ_{i} ≥ 0,   y_{i} ∈ {−1, +1}', '8.14'));
K.push(P('The problem is solved in its dual form, in which data appear only through inner products, replaced by a kernel K:'));
K.push(EQ('maximise  Σ_{i} α_{i} − (1/2) Σ_{i} Σ_{j} α_{i} α_{j} y_{i} y_{j} K(x_{i}, x_{j}),   0 ≤ α_{i} ≤ C,   Σ_{i} α_{i} y_{i} = 0', '8.15'));
K.push(EQ('f(x) = sign[ Σ_{i} α_{i} y_{i} K(x_{i}, x) + b ]', '8.16'));
K.push(P('Only samples with α_{i} > 0 (the support vectors) define the decision function.'));
K.push(LBL('Kernel trick and the RBF kernel'));
K.push(P('A kernel computes inner products in a high-dimensional feature space without computing φ(x) explicitly, allowing non-linear boundaries (' + F('mlsvm') + 'b). The thesis uses the radial basis function (RBF, Gaussian) kernel:'));
K.push(EQ('K(x_{i}, x) = exp( −γ ‖x − x_{i}‖^{2} )', '8.17'));
K.push(...tab2('mlsvmparams', [
  ['Hyperparameter', 'Meaning', 'Small value', 'Large value', 'Search range (thesis)'],
  ['C', 'Penalty for margin violations', 'Wide margin, smoother boundary, risk of underfitting', 'Narrow margin, fits training data closely, risk of overfitting', '2^{−2} … 2^{8}'],
  ['γ (RBF)', 'Inverse width of the kernel', 'Each sample influences far: smooth boundary', 'Influence is local: wiggly boundary, overfitting', '2^{−8} … 2^{2}'],
  ['ε (SVR only)', 'Half-width of the error-free tube', 'Many support vectors, closer fit', 'Fewer support vectors, flatter fit', '0.1, 0.5, 1 (on DI scale after scaling)'],
  ['class\\_weight', 'Cost per class', '–', '–', '"balanced" (Eq. 8.2)'],
], [1500, 2000, 2200, 2200, 1406], 'SVM/SVR hyperparameters and their effect (grid search following Hsu et al., 2003; Tian et al., 2021).', 15));
K.push(LBL('Multi-class SVM'));
K.push(P('SVM is binary. For the three severity classes, LIBSVM (used by scikit-learn) trains **one-vs-one** classifiers, one for each pair of classes — K(K − 1)/2 = 3 classifiers for K = 3 — and predicts by majority vote (Chang and Lin, 2011). Class probabilities, if needed, come from Platt scaling (Platt, 1999).'));
K.push(LBL('Support vector regression (SVR)'));
K.push(P('SVR fits a function that deviates from the measured DI by at most ε for as many samples as possible; errors inside the ε-tube cost nothing (' + F('mlsvm') + 'c; Smola and Schölkopf, 2004):'));
K.push(EQ('minimise  (1/2) ‖w‖^{2} + C Σ_{i} (ξ_{i} + ξ_{i}^{*})   subject to  |y_{i} − f(x_{i})| ≤ ε + ξ_{i}^{(*)}', '8.18'));
K.push(...fig2('mlsvm', 'g3_svm.png', '(a) Maximum-margin hyperplane and support vectors; (b) non-linear RBF-kernel boundary; (c) SVR ε-insensitive tube (synthetic data).', 560));
K.push(LBL('Strengths and limitations'));
K.push(BL('Strengths: effective with few samples and many features; global optimum (convex problem); flexible non-linear boundaries via kernels; the most accurate criterion classifier in ML-SFFS for rice blast (Tian et al., 2021).'));
K.push(BL('Limitations: needs feature scaling and careful tuning of C and γ; training cost grows roughly between n^{2} and n^{3} with the number of samples; less interpretable than trees.'));
K.push(INCASE(`Severity discrimination has three classes, so the SVM trains three binary machines (Low–Moderate, Low–High, Moderate–High) and each plot-date is assigned the class with most votes (one-vs-one). C and γ are tuned on an 11 × 11 grid (121 combinations), each scored by grouped 4-fold cross-validation inside the training replications. For DI, SVR fits a tube of half-width ε around the regression function; plot-dates inside the tube cost nothing, which makes SVR robust to small scoring errors in visual DI.`));
K.push(H3('8.6.2 Random forest (RF) and random forest regression (RFR)'));
K.push(LBL('Decision trees'));
K.push(P('A classification and regression tree (CART; Breiman et al., 1984) splits the data repeatedly on one feature at a time. At each node it chooses the split that most reduces impurity. For classification the impurity is the Gini index; for regression it is the mean squared error.'));
K.push(EQ('Gini(t) = 1 − Σ_{k} p_{k}^{2};    ΔG = Gini(parent) − (n_{L}/n) Gini(L) − (n_{R}/n) Gini(R)', '8.19'));
K.push(KEY('Worked example:', 'a node with 30 healthy and 10 diseased plot-dates has Gini = 1 − (0.75^{2} + 0.25^{2}) = 0.375. A split into left (28 healthy, 2 diseased; Gini = 0.124) and right (2 healthy, 8 diseased; Gini = 0.320) has weighted Gini = 0.75 × 0.124 + 0.25 × 0.320 = 0.173, so the impurity decrease is 0.375 − 0.173 = 0.202. The split with the largest decrease is chosen.'));
K.push(LBL('Random forest'));
K.push(P('A single deep tree overfits. Random forest (Breiman, 2001) grows B trees, each on a **bootstrap sample** (n samples drawn with replacement; about 63.2% unique samples) and considers only **m randomly chosen features at each split**. Averaging many decorrelated trees reduces variance (' + F('mlrf') + ').'));
K.push(EQ('ŷ(x) = mode{ T_{b}(x) }  (classification);    ŷ(x) = (1/B) Σ_{b=1}^{B} T_{b}(x)  (regression)', '8.20'));
K.push(BL('**Out-of-bag (OOB) error:** each tree is tested on the ~36.8% of samples not in its bootstrap sample, giving an internal error estimate. With repeated plot-dates, OOB samples can include other dates of training plots, so OOB is optimistic here; the grouped validation of Section 8.8 is used for reporting.'));
K.push(BL('**Feature importance:** mean decrease in impurity (MDI, fast but biased towards features with many split points; Strobl et al., 2007) or permutation importance (drop in accuracy when a feature is shuffled; preferred).'));
K.push(...fig2('mlrf', 'g4_rf.png', 'Random forest: bootstrap samples, randomised trees and aggregation of their predictions.', 520));
K.push(...tab2('mlrfparams', [
  ['Hyperparameter', 'Meaning', 'Thesis setting'],
  ['n\\_estimators (B)', 'Number of trees; more trees never overfit but cost time', '500'],
  ['max\\_features (m)', 'Features tried per split; controls tree correlation', '√p, p/3, p/2 (√p is the usual default for classification, p/3 for regression)'],
  ['min\\_samples\\_leaf', 'Minimum samples in a leaf; larger values smooth predictions', '1, 3, 5'],
  ['max\\_depth', 'Maximum tree depth', 'Unlimited (controlled by leaf size)'],
  ['class\\_weight', 'Cost per class', '"balanced"'],
], [2200, 4300, 2806], 'Random-forest hyperparameters (Breiman, 2001; Probst et al., 2019).', 16));
K.push(LBL('Strengths and limitations'));
K.push(BL('Strengths: handles non-linearity and interactions; no scaling; robust to noise and outliers; little tuning; importance measures; best regressor in Feng et al. (2022).'));
K.push(BL('Limitations: cannot extrapolate beyond the range of training DI; correlated features share importance; large models are less interpretable than a single tree.'));
K.push(INCASE(`With 500 trees and an OFC of, say, 8 features, each split considers m = √8 ≈ 3 randomly chosen features (classification) or about 8/3 ≈ 3 (regression). Each tree sees a bootstrap sample of plot-dates; because dates of the same plot are correlated, the out-of-bag error is optimistic, so the reported performance always comes from the held-out replication. Mean decrease in accuracy shows which OFC features drive the predictions, for example whether CTD or PSSRa matters more for High severity.`));
K.push(H3('8.6.3 k-nearest neighbours (k-NN)'));
K.push(P('k-NN stores the training samples and classifies a new sample by the **majority class of its k nearest neighbours** (regression: mean DI of the neighbours) (Cover and Hart, 1967; ' + F('mlknn') + '). It has no training phase ("lazy learner"). Distance is the Minkowski distance over the p features; q = 2 gives the Euclidean distance used in the thesis:'));
K.push(EQ('d(x, z) = ( Σ_{j=1}^{p} |x_{j} − z_{j}|^{q} )^{1/q},   q = 2 (Euclidean)', '8.21'));
K.push(...fig2('mlknn', 'g5_knn.png', 'k-NN with k = 5: the new plot (star) has 3 healthy and 2 diseased neighbours, so it is classified healthy (synthetic data).', 330));
K.push(...tab2('mlknnparams', [
  ['Hyperparameter', 'Effect', 'Thesis setting'],
  ['k', 'Small k: flexible, sensitive to noise; large k: smoother, may blur class borders', '3, 5, 7, 9, 11 (odd values avoid ties in binary tasks)'],
  ['Distance', 'How similarity is measured', 'Euclidean on standardised features'],
  ['Weights', 'Uniform vote or closer neighbours count more', 'Uniform (distance weighting optional)'],
], [2000, 4500, 2806], 'k-NN hyperparameters.', 16));
K.push(BL('Strengths: simple, non-parametric, naturally multi-class; gave the best multivariate regression (R^{2} = 0.92) in Mustafa et al. (2023); a fast criterion in ML-SFFS (Tian et al., 2021).'));
K.push(BL('Limitations: needs scaling; suffers in high dimensions (distances become similar), hence used after feature selection; prediction cost grows with the training set; sensitive to class imbalance.'));
K.push(INCASE(`A new plot-date is placed in the standardised OFC space; its k (for example 7) nearest training plot-dates are found by Euclidean distance. For detection it is called diseased if most neighbours are diseased; for DI, its predicted DI is the mean DI of the neighbours. k-NN needs no training phase, but it is sensitive to irrelevant features, which is why it is always used after ML-SFFS.`));
K.push(H3('8.6.4 Partial least squares regression (PLSR)'));
K.push(P('PLSR handles many collinear predictors by projecting X onto a few **latent components** (scores) T that have **maximum covariance with y**, then regressing y on T (Wold et al., 2001; Geladi and Kowalski, 1986). Unlike principal component regression, the components are chosen with the response in mind.'));
K.push(EQ('X = T P^{T} + E,     y = T q + f', '8.22'));
K.push(P('NIPALS algorithm for one response (PLS1), repeated for each component a: (1) weight w = X^{T}y / ‖X^{T}y‖; (2) score t = Xw; (3) X-loading p = X^{T}t / (t^{T}t); (4) y-loading q = y^{T}t / (t^{T}t); (5) deflate X ← X − t p^{T} and y ← y − t q. The number of components is chosen by the minimum cross-validated RMSE. Variable importance in projection (VIP) summarises each feature\'s contribution (Chong and Jun, 2005):'));
K.push(EQ('VIP_{j} = √[ p Σ_{a} SS_{a} (w_{ja} / ‖w_{a}‖)^{2} / Σ_{a} SS_{a} ],   SS_{a} = q_{a}^{2} t_{a}^{T} t_{a}', '8.23'));
K.push(...tab2('mlplsparams', [
  ['Item', 'Specification'],
  ['Preprocessing', 'Mean-centring and scaling of each feature (autoscaling)'],
  ['Components', '1 to min(10, p), chosen by minimum RMSE in grouped inner cross-validation'],
  ['Inputs', 'DSF pool after VIF (single sensor or concatenated sensors)'],
  ['Role', 'Linear baseline for DI regression (Guo 2021; Feng 2022; Maimaitijiang 2020)'],
], [2400, 6906], 'PLSR specification.', 17));
K.push(BL('Strengths: works when features outnumber samples or are highly collinear; fast; interpretable (loadings, VIP). Limitations: linear; may underfit non-linear severity responses (the reason non-linear models are compared).'));
K.push(INCASE(`PLSR is the linear baseline for DI. It receives the concatenated DSFs after VIF (for S8 perhaps 30–40 features from four sensors) and compresses them into a few latent components that are maximally correlated with DI. The number of components (1–10) is chosen by the lowest inner cross-validated RMSE. The loading weights and the variable importance in projection (VIP; Wold et al., 2001) show which features contribute, which is useful for physical interpretation.`));
K.push(H3('8.6.5 Deep neural networks: DNN-F1 and DNN-F2'));
K.push(LBL('Building blocks'));
K.push(P('A neuron computes a weighted sum of its inputs plus a bias and passes it through a non-linear activation; layers of neurons form a fully connected feed-forward network (multilayer perceptron). The thesis uses the rectified linear unit (ReLU):'));
K.push(EQ('z = w^{T} x + b,     a = ReLU(z) = max(0, z)', '8.24'));
K.push(BL('**Training:** weights are learned by minimising a loss with gradient descent; gradients are computed by back-propagation, the chain rule applied layer by layer (Rumelhart et al., 1986). Weights are initialised with He initialisation (variance 2/n_{in}), suited to ReLU (He et al., 2015).'));
K.push(BL('**Loss functions:** mean squared error for DI; softmax output with cross-entropy for classes (Eq. 8.25).'));
K.push(EQ('p_{k} = exp(z_{k}) / Σ_{j} exp(z_{j}),    L_{CE} = − Σ_{k} y_{k} ln p_{k};    L_{MSE} = (1/n) Σ_{i} (y_{i} − ŷ_{i})^{2}', '8.25'));
K.push(BL('**Adam optimiser** (Kingma and Ba, 2015) adapts the step size of each weight using running averages of the gradient g_{t} and of its square:'));
K.push(EQ('m_{t} = β_{1} m_{t−1} + (1 − β_{1}) g_{t};    v_{t} = β_{2} v_{t−1} + (1 − β_{2}) g_{t}^{2}'));
K.push(EQ('θ_{t} = θ_{t−1} − α m̂_{t} / (√v̂_{t} + ε),   m̂_{t} = m_{t}/(1 − β_{1}^{t}),  v̂_{t} = v_{t}/(1 − β_{2}^{t})', '8.26'));
K.push(P('Defaults: α = 0.001, β_{1} = 0.9, β_{2} = 0.999, ε = 10^{−8}.'));
K.push(BL('**Batch normalisation** (Ioffe and Szegedy, 2015) standardises the inputs of a layer over each mini-batch and then rescales them with learned parameters γ and β, which speeds and stabilises training:'));
K.push(EQ('x̂ = (x − μ_{B}) / √(σ_{B}^{2} + ε),     y = γ x̂ + β', '8.27'));
K.push(BL('**Dropout** (Srivastava et al., 2014) randomly switches off a fraction p of neurons in each training step, so the network cannot rely on single neurons; this reduces overfitting. At prediction time all neurons are used.'));
K.push(BL('**Early stopping** (Prechelt, 1998) stops training when the validation loss has not improved for a set number of epochs (patience) and keeps the best weights.'));
K.push(LBL('DNN-F1 and DNN-F2 (feature-level fusion; Maimaitijiang et al., 2020)'));
K.push(BL('**DNN-F1 (input-level fusion):** the selected features of all sensors are concatenated into one vector and passed through shared dense layers.'));
K.push(BL('**DNN-F2 (intermediate-level fusion):** each sensor has its own small sub-network that learns a sensor-specific representation; these representations are concatenated and passed to joint layers. This lets each sensor\'s features be transformed on their own scale before interaction, which gave the best accuracy and robustness in Maimaitijiang et al. (2020) (see also Ramachandram and Taylor, 2017).'));
K.push(...fig2('mldnn', 'g9_dnn.png', 'DNN-F1 (input-level fusion) and DNN-F2 (intermediate-level fusion) adapted from Maimaitijiang et al. (2020).', 560));
K.push(...tab2('mldnnparams', [
  ['Hyperparameter', 'DNN-F1', 'DNN-F2'],
  ['Architecture', '3 dense layers, e.g. 64–32–16 units', 'Per sensor: 2 layers, e.g. 16–8 units; joint layer 16 units'],
  ['Activation / normalisation', 'ReLU; batch normalisation', 'Same'],
  ['Dropout rate', '0.2, 0.3 or 0.5 (tuned)', 'Same'],
  ['Output', 'Linear (DI) or softmax (classes)', 'Same'],
  ['Optimiser', 'Adam, learning rate 10^{−3}', 'Same'],
  ['Batch size / epochs', '32 / up to 500 with early stopping (patience 30)', 'Same'],
  ['Validation for early stopping', 'Plot-grouped split of the training data', 'Same'],
], [2600, 3300, 3406], 'DNN specifications (starting configurations to be tuned).', 16));
K.push(...tab2('mldnncount', [
  ['Network (example inputs)', 'Layer-by-layer parameters (weights + biases)', 'Total'],
  ['DNN-F1, 24 inputs, 64–32–16–1', '24×64+64 = 1600; 64×32+32 = 2080; 32×16+16 = 528; 16×1+1 = 17', '4225'],
  ['DNN-F2, inputs RGB 6, MS 6, HS 8, TIR 4; sub-networks 16–8; joint 16; output 1', 'RGB 248; MS 248; HS 280; TIR 216; joint 32×16+16 = 528; output 17', '1537'],
], [3000, 4700, 1606], 'Number of trainable parameters (batch-normalisation parameters excluded). With about 1300 plot-dates, small networks with dropout and early stopping are needed.', 16));
K.push(BL('Strengths: learn non-linear interactions between sensors; DNN-F2 respects the different nature of each sensor; less prone to saturation than linear models (Maimaitijiang et al., 2020).'));
K.push(BL('Limitations: need more data than classical models (hence not used for the 432 pre-symptomatic plot-dates); many hyperparameters; results vary with random initialisation (repeat training with several seeds and report the mean); less interpretable.'));

// ===== 5 FUSION =====
K.push(INCASE(`For severity with S8, DNN-F2 has four sub-networks. Suppose the inputs after VIF are 10 RGB, 12 MS, 15 HS and 6 TIR features. Each sub-network has two dense layers (16 and 8 units; for HS 15 × 16 + 16 = 256 and 16 × 8 + 8 = 136 parameters); the four 8-unit outputs are concatenated (32 values) and passed through a joint layer of 16 units (528 parameters) to a 3-unit softmax output (51 parameters). In total the network has about 1 900 trainable parameters (batch-normalisation parameters excluded), while one training fold has about 860 post-symptomatic plot-dates; dropout, batch normalisation, early stopping on a plot-grouped validation split and repeated training with several random seeds keep it from overfitting. DNN-F1 instead concatenates all 43 inputs at the start and passes them through one stack of dense layers (e.g. 64–32–16).`));
K.push(H2('8.7 Multimodal data fusion'));
K.push(P('Fusion can be done at three levels (Maimaitijiang et al., 2020; Ramachandram and Taylor, 2017): **data level** (raw data stacked before modelling), **feature level** (features of each sensor combined before or inside a model) and **decision level** (separate models per sensor whose outputs are combined). The thesis uses feature-level fusion, because the four sensors have different resolutions and units but give comparable plot-level features (' + F('mlfusion') + ').'));
K.push(...fig2('mlfusion', 'g10_fusion.png', 'Single-sensor modelling and the four feature-level fusion strategies of the thesis.', 560));
K.push(...tab2('mlfusioncmp', [
  ['Strategy', 'How sensors are combined', 'Models', 'Advantage', 'Source'],
  ['FA: pooled ML-SFFS', 'DSFs of all sensors pooled; VIF; SFFS chooses one cross-sensor subset', 'SVM, RF, k-NN (and SVR, RFR, k-NN)', 'Finds complementary features; shows which sensors contribute', 'Mustafa et al. 2023'],
  ['FB: sensor-wise ML-SFFS', 'SFFS within each sensor; sensor OFCs concatenated; final SFFS pass', 'Same', 'Every sensor represented; smaller searches', 'Tian et al. 2021; ORW'],
  ['FC: DNN-F1', 'All features concatenated at the input', 'DNN', 'Simple deep fusion', 'Maimaitijiang et al. 2020'],
  ['FD: DNN-F2', 'Sensor sub-networks joined at an intermediate layer', 'DNN', 'Sensor-specific representations; best in source study', 'Maimaitijiang et al. 2020'],
], [1500, 2600, 1600, 2000, 1606], 'Feature-level fusion strategies.', 15));

// ===== 6 VALIDATION =====
K.push(H2('8.8 Validation and hyperparameter tuning'));
K.push(H3('8.8.1 Cross-validation'));
K.push(P('In k-fold cross-validation the data are split into k folds; each fold is used once for testing and the other k − 1 for training, and the k results are averaged (Kohavi, 1995). **Stratified** folds keep class proportions; **grouped** folds keep all samples of a group (here a plot) in the same fold (Roberts et al., 2017).'));
K.push(H3('8.8.2 Nested cross-validation in the thesis'));
K.push(P('Two loops are used (' + F('mlnested') + '; Cawley and Talbot, 2010):'));
K.push(BL('**Outer loop – leave-one-replication-out:** train on two RBD replications, test on the third, three times. Each replication contains all 24 treatments, so every test fold is a complete copy of the experiment. The outer loop estimates performance.'));
K.push(BL('**Inner loop – grouped 4-fold cross-validation inside the two training replications:** used for Boruta/ReliefF, hyperspectral band selection, VIF, ML-SFFS and grid search of hyperparameters. The test replication is never seen.'));
K.push(BL('After cross-validation, the final model is refitted on all IARI data and tested on independent data: the IIRMR Bharatpur experiment and farmers\' fields (Feng et al., 2022, also validated on a separate experiment).'));
K.push(...fig2('mlnested', 'g6_nestedcv.png', 'Nested validation: outer leave-one-replication-out loop and inner plot-grouped 4-fold loop.', 560));
K.push(H3('8.8.3 Grid search'));
K.push(P('Every combination of candidate hyperparameter values is evaluated in the inner loop and the best combination (highest macro-F1 or lowest RMSE) is used to refit the model on the outer training data (Hsu et al., 2003).'));
K.push(...tab2('mlgrids', [
  ['Model', 'Grid', 'Combinations', 'Fits with inner 4-fold CV'],
  ['SVM (C, γ)', '11 values of C × 11 values of γ', '121', '484'],
  ['SVR (C, γ, ε)', '11 × 11 × 3', '363', '1452'],
  ['RF (m, leaf)', '3 × 3', '9', '36'],
  ['k-NN (k)', '5', '5', '20'],
  ['PLSR (components)', '1–10', '10', '40'],
], [2000, 3000, 2000, 2306], 'Size of the hyperparameter grids (per outer fold and feature subset).', 17));

// ===== 7 METRICS =====
K.push(H2('8.9 Evaluation metrics'));
K.push(H3('8.9.1 Classification'));
K.push(P('All classification metrics come from the **confusion matrix** n_{ij} (true class i, predicted class j). For K classes and N samples:'));
K.push(EQ('OA = Σ_{k} n_{kk} / N;    Precision_{k} = n_{kk} / Σ_{i} n_{ik};    Recall_{k} = n_{kk} / Σ_{j} n_{kj}'));
K.push(EQ('F1_{k} = 2 Precision_{k} Recall_{k} / (Precision_{k} + Recall_{k});    macro-F1 = (1/K) Σ_{k} F1_{k}', '8.28'));
K.push(EQ('κ = (p_{o} − p_{e}) / (1 − p_{e}),    p_{o} = OA,    p_{e} = Σ_{k} n_{k+} n_{+k} / N^{2}', '8.29'));
K.push(P('Precision answers "of the plots predicted as class k, how many really are k?"; recall (sensitivity for the diseased class) answers "of the real class-k plots, how many were found?"; specificity = TN/(TN + FP) is the recall of the healthy class. Cohen\'s kappa corrects agreement for chance (Cohen, 1960); macro-F1 weights every class equally (Sokolova and Lapalme, 2009).'));
K.push(...fig2('mlconfusion', 'g8_confusion.png', 'Example confusion matrix for the three severity classes (illustrative numbers).', 300));
K.push(...tab2('mlmetricex', [
  ['Class', 'Precision', 'Recall', 'F1'],
  ['Low', '40/52 = 0.769', '40/50 = 0.800', '0.784'],
  ['Moderate', '25/39 = 0.641', '25/40 = 0.625', '0.633'],
  ['High', '22/29 = 0.759', '22/30 = 0.733', '0.746'],
  ['Overall', 'OA = 87/120 = 0.725', 'macro-F1 = 0.721', 'κ = 0.577'],
], [2000, 2500, 2500, 2306], 'Metrics of the example confusion matrix: p_{e} = (50×52 + 40×39 + 30×29)/120^{2} = 0.349, so κ = (0.725 − 0.349)/(1 − 0.349) = 0.577.', 17));
K.push(...tab2('mlkappascale', [
  ['Kappa', '< 0', '0.00–0.20', '0.21–0.40', '0.41–0.60', '0.61–0.80', '0.81–1.00'],
  ['Agreement', 'Poor', 'Slight', 'Fair', 'Moderate', 'Substantial', 'Almost perfect'],
], [1300, 1300, 1300, 1300, 1300, 1300, 1506], 'Common interpretation of kappa (Landis and Koch, 1977).', 16));
K.push(H3('8.9.2 Regression'));
K.push(EQ('R^{2} = 1 − Σ (y_{i} − ŷ_{i})^{2} / Σ (y_{i} − ȳ)^{2};    RMSE = √[ (1/n) Σ (y_{i} − ŷ_{i})^{2} ];    NRMSE = RMSE / ȳ × 100', '8.30'));
K.push(KEY('Worked example:', 'measured DI = 10, 30, 55% and predicted DI = 14, 26, 50%. Squared errors 16 + 16 + 25 = 57; RMSE = √(57/3) = 4.36% DI; mean DI = 31.7%, so NRMSE = 13.8%; Σ (y − ȳ)^{2} = 1016.7, so R^{2} = 1 − 57/1016.7 = 0.944. R^{2} computed this way can be negative on test data if the model is worse than predicting the mean. The relative error of Feng et al. (2022) divides by each measured DI and is undefined for healthy plots (DI = 0), so NRMSE is used.'));

// ===== 8 SOFTWARE =====
K.push(INCASE(`If the best regression model has RMSE = 8.5 DI percentage points on the test replication and the mean measured DI is 34%, NRMSE = 8.5/34 × 100 = 25%. If R^{2} = 0.82, the model explains 82% of the variance of DI among test plot-dates. For the severity classes, a macro-F1 of 0.75 with per-class F1 of 0.85 (Low), 0.62 (Moderate) and 0.78 (High) would show that the middle class is hardest, as expected when classes are defined by thresholds on a continuous index.`));
K.push(H2('8.10 Software implementation'));
K.push(...tab2('mlsoftware', [
  ['Step', 'Python implementation (key settings)', 'R alternative'],
  ['Scaling', 'sklearn.preprocessing.StandardScaler (fit on training data only, inside a Pipeline)', 'caret::preProcess'],
  ['ReliefF', 'skrebate.ReliefF(n\\_neighbors=10)', 'CORElearn::attrEval("ReliefFequalK")'],
  ['Boruta', 'boruta.BorutaPy(RandomForestClassifier(n\\_estimators=500), max\\_iter=100, alpha=0.01)', 'Boruta::Boruta(maxRuns=100, pValue=0.01)'],
  ['VIF', 'statsmodels variance\\_inflation\\_factor (iterative removal)', 'car::vif'],
  ['SFFS', 'mlxtend SequentialFeatureSelector(k\\_features=(1,10), forward=True, floating=True, cv=GroupKFold(4))', '–'],
  ['SVM / SVR', 'sklearn.svm.SVC(kernel="rbf", class\\_weight="balanced"); SVR(kernel="rbf")', 'e1071::svm'],
  ['RF / RFR', 'sklearn.ensemble.RandomForestClassifier / Regressor(n\\_estimators=500)', 'randomForest / ranger'],
  ['k-NN', 'sklearn.neighbors.KNeighborsClassifier / Regressor', 'kknn'],
  ['PLSR', 'sklearn.cross\\_decomposition.PLSRegression', 'pls::plsr'],
  ['DNN-F1/F2', 'TensorFlow/Keras functional API (Dense, BatchNormalization, Dropout, Concatenate)', 'keras'],
  ['Validation', 'GroupKFold / LeaveOneGroupOut (groups = replication, plot); GridSearchCV inside the outer loop', 'caret (groupKFold)'],
  ['Metrics', 'sklearn.metrics (accuracy, precision\\_recall\\_fscore\\_support, f1\\_score(average="macro"), cohen\\_kappa\\_score, r2\\_score, mean\\_squared\\_error)', 'caret::confusionMatrix'],
], [1500, 5300, 2506], 'Software for each step (scikit-learn: Pedregosa et al., 2011; mlxtend: Raschka, 2018; Boruta: Kursa and Rudnicki, 2010).', 15));
K.push(P('All preprocessing and selection steps that use labels are placed inside a scikit-learn Pipeline or inside the outer-loop function, so that they are re-fitted on every training fold and never see test data.'));

// ===== 9 SUMMARY =====
K.push(H2('8.11 Summary of model specifications'));
K.push(...tab2('mlmodelcmp', [
  ['Property', 'SVM / SVR', 'RF / RFR', 'k-NN', 'PLSR', 'DNN-F1 / F2'],
  ['Model type', 'Kernel, maximum margin', 'Ensemble of trees', 'Instance-based', 'Linear latent variables', 'Neural network'],
  ['Non-linear', 'Yes (RBF)', 'Yes', 'Yes', 'No', 'Yes'],
  ['Scaling needed', 'Yes', 'No', 'Yes', 'Yes', 'Yes'],
  ['Main hyperparameters', 'C, γ, (ε)', 'Trees, m, leaf size', 'k', 'Components', 'Layers, units, dropout, learning rate'],
  ['Handles collinearity', 'Partly', 'Yes', 'Poorly', 'Yes (designed for it)', 'Partly'],
  ['Data needed', 'Small–medium', 'Small–large', 'Small–medium', 'Small', 'Medium–large'],
  ['Interpretability', 'Low–medium', 'Medium (importance)', 'Medium', 'High (loadings, VIP)', 'Low'],
  ['Role in thesis', 'Classifier and regressor; SFFS judge', 'Classifier and regressor; SFFS judge; Boruta', 'Classifier and regressor; SFFS judge', 'Linear DI baseline', 'Deep feature-level fusion'],
], [1600, 1550, 1550, 1500, 1500, 1606], 'Comparison of the six models.', 15));

// ===== 10 Q&A =====
K.push(H1('9. Expected outcomes, novelty, limitations and relevance'));
K.push(H2('9.1 How each objective is satisfied'));
K.push(...tab2('satisfy', [
  ['Objective', 'Per-sensor steps', 'Fusion', 'Models', 'Deliverable'],
  ['1. Characterise', 'Sensor-specific features; HS band-level analysis and WRI; statistics (detection, severity); Boruta; univariate regression', 'Cross-sensor correlation; JM and canonical discriminant analysis per sensor', 'None (threshold classifier for WRI)', 'DSF pools per sensor and task; physiological explanation'],
  ['2. Detect and discriminate', 'VIF → ML-SFFS for D, S, R', 'FA, FB, DNN-F1, DNN-F2', 'SVM, RF, k-NN, PLSR, DNN-F1, DNN-F2', 'Best sensor set, fusion and model; maps'],
  ['3. Pre-symptomatic', 'Screening; ReliefF (HS); Boruta → VIF → ML-SFFS', 'FA, FB', 'SVM, RF, k-NN (PLSR, RFR for physiology)', 'Early-warning sensor set; risk maps'],
], [1500, 2800, 1700, 1700, 1606], 'Objective-wise summary.', 16));
K.push(H2('9.2 Expected outcomes'));
K.push(BL('Disease-specific features of each UAV sensor for detection and for severity, their physiological meaning, robust white-rust wavelengths and a White Rust Index (Objective 1).'));
K.push(BL('The best sensor, combination, fusion strategy and model for detection, three-class severity discrimination and DI estimation; HS + TIR fusion and DNN-F2 are expected to perform well (Mahlein et al., 2019; Maimaitijiang et al., 2020), and ML-SFFS to give compact cross-sensor feature sets (Mustafa et al., 2023) (Objective 2).'));
K.push(BL('A pre-symptomatic detection model and early-warning maps (Objective 3).'));
K.push(H2('9.3 Novelty of the thesis'));
K.push(BL('**First sensor-based study of white rust in mustard**, at any scale; the closest mustard studies concern aphid (Shukla et al., 2024) and Sclerotinia rot (Bhattacharya and Chattopadhyay, 2013).'));
K.push(BL('**Four UAV sensors on the same plots and flights** (RGB, multispectral, VNIR + SWIR hyperspectral, thermal); the reference studies used at most three, and only two of them used a UAV for disease.'));
K.push(BL('**A White Rust Index** built from UAV hyperspectral data with the ReliefF + exhaustive-search method of Mahlein et al. (2013), extended to SWIR bands.'));
K.push(BL('**Direct comparison of interpretable ML-SFFS fusion (pooled and sensor-wise) with deep-learning fusion (DNN-F1, DNN-F2)** for disease detection, three-class severity and DI regression.'));
K.push(BL('**Pre-symptomatic prediction at UAV plot scale under field conditions**, whereas earlier pre-symptomatic studies were at leaf or spike scale under controlled conditions.'));
K.push(BL('**Leakage-free validation** (all selection inside training folds; plot-grouped leave-one-replication-out) and independent validation at Bharatpur and in farmers\' fields.'));
K.push(H2('9.4 Limitations and how they are handled'));
K.push(...tab2('limits', [
  ['Limitation', 'Consequence', 'How it is handled'],
  ['Repeated observations of the same 72 plots', 'Samples not independent; p-values and random-split accuracies optimistic', 'Plot-grouped LORO cross-validation; tests used only to rank features; independent validation site'],
  ['One season and one site for model development', 'Models may not transfer to other years, varieties or soils', 'Validation at Bharatpur and in farmers\' fields (2026–27); report loss of accuracy honestly'],
  ['Visual DI scoring is subjective and sampled', 'Label noise, especially near class limits (25%, 50%)', 'Five sampling points per plot; same trained scorer; SVR ε-tube and macro-F1; report class confusion'],
  ['Overlapping severity classes', 'Adjacent classes (Low–Moderate, Moderate–High) confused', 'DI regression alongside classification; JM to report overlap; correlation scalogram and ReliefF instead of separability thresholds'],
  ['Coarse SWIR pixels (about 36 cm)', 'Few pure canopy pixels per plot; mixing with soil', 'Inner buffer; canopy mask; SWIR features used only if enough pure pixels'],
  ['Thermal signal depends on weather', 'Raw CT varies between flights', 'Flights at 11:00–14:00 h; CTD, CTR, NRCT normalisation; air temperature and humidity recorded'],
  ['Other stresses (water, nutrients, other diseases such as Alternaria blight)', 'Non-specific spectral or thermal change', 'Uniform irrigation and fertiliser; control plots; disease-specific WRI; water index check of thermal signal; scoring of other diseases recorded'],
  ['Small sample for deep learning', 'DNN overfitting', 'Small networks, dropout, batch normalisation, early stopping; DNNs not used for Objective 3'],
  ['Flowering of mustard', 'Yellow flowers change reflectance and NDVI masks', 'Mask threshold checked per flight; flowering stage recorded'],
], [2500, 2900, 3906], 'Limitations of the study and how they are handled.', 16));
K.push(H2('9.5 Relevance to ISRO and scaling to satellites'));
K.push(P(`UAV results are the link between field measurements and satellite monitoring. Spectral regions and indices found at UAV scale can be tested on satellite sensors with similar bands: the multispectral red-edge and NIR indices on Sentinel-2 (ESA) and on Indian sensors such as LISS-IV and AWiFS of Resourcesat; the hyperspectral bands and the White Rust Index on spaceborne imaging spectrometers such as ISRO's HySIS, PRISMA (ASI) and EnMAP (DLR), all with about 30 m pixels; and the thermal features on future high-resolution thermal missions such as TRISHNA, a joint ISRO–CNES mission. The mustard studies of Bhattacharya and Chattopadhyay (2013) and Shukla et al. (2024), both involving the Space Applications Centre, show the route: ground or UAV measurements identify sensitive bands, which are then used with weather and satellite data over larger areas. Because a 30 m satellite pixel mixes many plants and soil, the UAV maps of this thesis can also serve as reference data to train and validate satellite-scale disease models.`));
K.push(KEY('Take-home for the interview:', `the thesis delivers (i) the physical and physiological signature of white rust in each UAV sensor, (ii) the best sensor and fusion strategy for detection, severity and DI, with an honest, leakage-free accuracy estimate, (iii) an early-warning model, and (iv) a set of bands, indices and features that can be transferred to satellite sensors.`));

K.push(H1('10. Corrections and simplifications relative to the ORW'));
K.push(P(`The ORW was checked against the original papers. The tables below list the corrections made in this methodology; they are useful if an examiner compares the ORW with the thesis.`));
K.push(H2('10.1 Corrections to the index tables of the ORW slides'));
K.push(...tab2('idxcorr', [
  ['Item in slides', 'Correction (used in this document)'],
  ['mCARI1 = 1.2[(2.5R671 − R651) − 1.3(R761 − R581)]', 'MCARI1 = 1.2[2.5(R800 − R670) − 1.3(R800 − R550)] (Haboudane et al., 2004)'],
  ['MTVI1, MTVI2, TVI, RDVI, SR761, NDVI761 with 761, 651, 581 nm', 'These are band centres of a specific sensor; the original indices use 800 (750 for TVI), 670 and 550 nm. Use the original wavelengths (nearest band of the HS sensor)'],
  ['RARSc = R750/R700', 'RARSc = R760/R500 (Chappelle et al., 1992)'],
  ['NCPI = (R670 − R450)/(R670 + R450), "Peñuelas et al. [42]"', 'NPCI = (R680 − R430)/(R680 + R430) (Peñuelas et al., 1994)'],
  ['SIPI "Peñuelas et al. [41]"', 'Peñuelas et al. (1995)'],
  ['PSRI reference Peñuelas et al. (1995)', 'Merzlyak et al. (1999)'],
  ['WI/ND = R900/R970, Hunt et al. (1989)', 'This formula is WI itself. WI/NDVI = (R900/R970)/NDVI (Peñuelas et al., 1997)'],
  ['VIgreen = (R760 − R550)/(R760 + R550)', 'That formula is a green NDVI. VIgreen = (R550 − R670)/(R550 + R670) (Gitelson et al., 2002)'],
  ['RVS1 = (R651 + Red Edge 750); RVS2 = (R651 + Red Edge 750)/(R651 − Red Edge 750)', 'Formulas incomplete. RVSI = (R712 + R752)/2 − R732 (Merton and Huntington, 1999), as used by Guo et al. (2021)'],
  ['PPR = R550/R450', 'PPR = (R550 − R450)/(R550 + R450) (Metternicht, 2003)'],
  ['GNDVI = (R850 − R580)/(R850 + R580)', 'Green band of 540–570 nm: (R850 − R550)/(R850 + R550) (Gitelson et al., 1996)'],
  ['MS table: "NIR − 1R", "10.2", "R − 1G"', 'Copy artefacts of minus signs and of 0.2 from the source table: (NIR − R), 0.2, (R − G)'],
  ['MS PSRI = (R − G)/REG/R', 'PSRI_MS = (R − G)/NIR (Liu et al., 2024; adapted from Merzlyak et al., 1999)'],
  ['MS TCARI with NIR', 'TCARI was designed with 700 nm; with MS bands use RE: 3[(RE − R) − 0.2(RE − G)(RE/R)] (Haboudane et al., 2002; Maimaitijiang et al., 2020)'],
  ['MS references: NDVI (Rocha and Shaver 2009); GNDVI (Dash and Curran 2004); PSRI (Foster 2012); CIgreen (Vincini and Frazzi 2011); MSR, TCARI (Haboudane 2004)', 'Original sources: NDVI Rouse et al. (1974); GNDVI Gitelson et al. (1996); PSRI Merzlyak et al. (1999); CIgreen and CIrededge Gitelson et al. (2003); MSR Chen (1996); TCARI Haboudane et al. (2002)'],
  ['GLCM note: "i and j are row and column number of the images"', 'i and j are grey levels (row and column indices of the co-occurrence matrix); P(i, j) is the normalised co-occurrence frequency'],
], [4000, 5306], 'Corrections to the index and texture tables of the ORW slides.', 15));
K.push(H2('10.2 Corrections to the methodology'));
K.push(...tab2('methcorr', [
  ['Issue', 'Correction'],
  ['Severity classes 0–25%, 26–50%, > 50% (DI is continuous)', 'Low 0 < DI ≤ 25%; Moderate 25% < DI ≤ 50%; High DI > 50%; healthy (DI = 0) handled by the detection model'],
  ['CTR = CT/AT with °C', 'A ratio of °C values depends on the temperature scale; compute CTR in kelvin'],
  ['NRCT minimum and maximum', 'Take CT_{min} and CT_{max} from the same thermal image, so NRCT is comparable after pooling'],
  ['Thermal and RGB texture after pooling', 'Quantise images to the same number of grey levels over one common range for all flights; otherwise textures are not comparable'],
  ['Thermal texture "Energy"', 'Energy is the angular second moment (SEC); do not count it twice'],
  ['Hyperspectral bands: 491 in the ORW table, 481 used here', 'Confirm the band count after removing noisy bands and report it consistently'],
  ['Many near-identical indices (three NDVI and three simple-ratio variants)', 'Kept as supplied; VIF < 10 removes redundant ones before modelling'],
  ['Feature selection on all data before validation', 'Boruta, HS band selection, VIF and SFFS are repeated inside the training folds (Ambroise and McLachlan, 2002)'],
  ['Relative error (RE) for DI', 'Undefined for DI = 0; NRMSE is used'],
  ['JM > 1.94 for band selection (ORW)', 'Classes overlap; bands are selected by correlation scalograms + ReliefF, and JM only reports overlap'],
], [3800, 5506], 'Corrections to the methodology.', 15));
K.push(H2('10.3 Corrections to the ORW text'));
K.push(P('The following items were found while checking the ORW text against the reference papers and sensor specifications.'));
K.push(...tab2('corrections', [
  ['ORW text', 'Correction'],
  ['Liu et al. (2024): "Thermal-Terrestrial Chlorophyll Index (TTCI)"', 'TTCI means three-band texture combination indices (texture features, not a thermal or chlorophyll index). The best model combined percentile spectra, TTCI2 and canopy temperature (R^2 0.90, RMSE 8.28%).'],
  ['Mahlein et al. (2019): IRT and CFI needed 5 and 7 days', 'The abstract reports changes from 5 dai for both thermography and fluorescence (Fm); PSSRa/b separated infected spikelets at 3 dai.'],
  ['Mustafa et al. (2022): "KNN and SVM-SFFS models reached R^2 up to 0.92"', 'R^2 0.92 was the multivariate k-NN regression for severity. ML-SFFS was used for classification (87.04% asymptomatic, up to 95%). The paper is Front. Plant Sci. 13:1102341, published January 2023.'],
  ['Activity 2.1: "Tian et al., 2024"', 'Should be Tian et al. (2021), Remote Sensing of Environment 257, 112350.'],
  ['Feng et al. 2021 / 2022', 'Use one year consistently: Sensors 22(1), 31 (2022).'],
  ['D2: "1.5 × 10^5 mg/ml"', '1.5 × 10^5 zoosporangia mL^{−1}.'],
  ['Specificity = 1 − FP/(TP + FP); Sensitivity = 1 − FN/(TN + FN)', 'Specificity = TN/(TN + FP); sensitivity = TP/(TP + FN). (The kappa formula given is correct.)'],
  ['GSD at 30 m: RGB 8.2 cm, thermal 2 cm', 'Please verify: a 5472-pixel, 8.8 mm, 1-inch sensor gives about 0.8 cm at 30 m; FLIR Vue Pro R 640 with 13 mm lens (17 µm pixels) gives about 3.9 cm at 30 m.'],
  ['Reference "Jw, R. (1973)"', 'Rouse, J.W., Haas, R.H., Schell, J.A., Deering, D.W. (1974). Monitoring vegetation systems in the Great Plains with ERTS. Third ERTS Symposium, NASA SP-351, Vol. 1, 309–317.'],
  ['G1–G4 = 50, 40, 30, 20 DAS', 'With sowing on 20 Nov–20 Dec and inoculation on 10 Jan, the exact values are 51, 41, 31 and 21 DAS; "about 50, 40, 30, 20 DAS" is acceptable.'],
], [3300, 6006], 'Corrections to the ORW text.', 16));


K.push(H2('10.4 Simplifications relative to the ORW'));
K.push(...tab2('simplify', [
  ['Item in ORW', 'In this methodology', 'Reason'],
  ['Many selectors (t-test, chi-square, ANOVA-F, RFE, ReliefF, SPA, scalogram, Boruta, JM, MIM)', 'Statistics + Boruta (Objective 1); VIF → ML-SFFS (Objectives 2, 3); correlation scalograms + ReliefF for HS bands', 'One clear chain from the reference papers'],
  ['Many models (SVM, BPNN, ELM, LS-SVM, PLS-DA, RF, QDA, RustQNet, ICA/FVBA)', 'SVM, RF, k-NN, PLSR, DNN-F1, DNN-F2', 'All used in the reference papers'],
  ['Data-, feature- and model-level fusion', 'Feature-level fusion: ML-SFFS (FA, FB) and DNN (FC, FD)', 'Approaches of Mustafa 2023 and Maimaitijiang 2020'],
  ['Stage- or date-wise analysis', 'All dates pooled', 'One model covering the full severity range'],
  ['Pixel-level severity mapping', 'Plot-level maps', 'Ground truth is per plot'],
], [3200, 3200, 2906], 'Simplifications relative to the ORW.', 16));

K.push(H1('11. Interview questions and answers'));
K.push(P(`The questions are grouped by topic. Answers are short enough to say in one breath; the chapter and section numbers point to the detailed explanation.`));
K.push(H2('11.1 Disease and experiment'));
QA('What is white rust and what causes it?', 'A disease of crucifers caused by the obligate biotrophic oomycete Albugo candida. It produces white to creamy pustules of zoosporangia on leaves and stems (local infection) and swollen, distorted inflorescences called stagheads (systemic infection) (Section 1.1).');
QA('Is Albugo candida a fungus?', 'No. It is an oomycete (water mould), more closely related to brown algae than to true fungi. It has cellulose cell walls and motile zoospores, which is why free water on the leaf is needed for infection.');
QA('Which weather favours white rust?', 'Cool (roughly 10–20 °C), humid weather with dew or rain that keeps leaves wet, because zoospores need free water to swim and enter through stomata. Infection in north India is therefore common in December–February (Saharan et al., 2014).');
QA('Why did you use four inoculation timings and three varieties?', 'To create a wide range of severities on every flight date and to test whether the models work across genotypes of different susceptibility. Staggered sowing with one inoculation date gives plants of different ages at infection (Section 3.2).');
QA('Why is the resistant variety PM 38 included?', 'It provides inoculated plots with little or no disease, which tests whether models confuse inoculation with disease, and it widens the range of host response. In Objective 3, inoculated PM 38 plots that never show symptoms are not labelled infected.');
QA('How is the disease index calculated?', 'Leaves are scored 0–6 by the percentage of leaf area with pustules; DI = Σ(score × number of leaves)/(6 × total leaves) × 100. For example, 2 leaves at 0, 3 at 1, 3 at 3 and 2 at 5 give DI = 22/60 × 100 = 36.7%, the Moderate class (Section 3.3).');
QA('Why three severity classes with limits at 25% and 50%?', 'They split the DI range into management-relevant levels (low, moderate, high) as defined in the ORW; each value falls in exactly one class because the limits are written as ≤ 25%, 25–50% and > 50%. DI regression is done as well, so no information is lost by classing.');
QA('What is staghead severity and how is it measured?', 'After inflorescence initiation, staghead severity (%) = infected racemes / total racemes × 100 per plot (ORW). It is a second severity target that RGB structure and texture features (canopy height, vegetation fraction) are expected to track.');
QA('Why 3 m × 3 m plots?', 'They are large enough for every sensor to give pure canopy pixels after a 0.5 m inner buffer — even the coarse SWIR pixels (about 36 cm) give about 5 × 5 pixels — while allowing 72 plots in a replicated factorial design.');
K.push(H2('11.2 Sensors and physics'));
QA('Why does a diseased canopy reflect more red light?', 'Chlorophyll absorbs red light (around 670 nm). White rust destroys chlorophyll around pustules and the white pustules themselves reflect strongly, so red reflectance rises (Section 1.3.1).');
QA('What is the red edge and why does it shift?', 'The steep rise of reflectance between about 680 and 750 nm, between chlorophyll absorption and NIR scattering. When chlorophyll falls, the absorption feature narrows and the inflection point (REP) moves to shorter wavelengths — the blue shift (Horler et al., 1983).');
QA('Why is NIR reflectance high in healthy leaves?', 'NIR light is not absorbed by pigments and is scattered many times at the air–cell-wall interfaces of the spongy mesophyll. Tissue damage reduces this internal scattering and lowers NIR reflectance.');
QA('What does the SWIR region tell you?', 'SWIR reflectance is controlled mainly by leaf water (absorption near 1450 and 1940 nm, weaker near 970 and 1200 nm) and by dry matter. Water loss in infected tissue raises SWIR reflectance; Bhattacharya and Chattopadhyay (2013) found SWIR bands most sensitive to mustard rot.');
QA('Why do you remove 1350–1450 and 1800–1950 nm?', 'Atmospheric water vapour absorbs almost all solar radiation there, so the signal reaching the sensor is very small and noisy, even from a UAV at 30 m.');
QA('Why does a diseased canopy become warmer?', 'Infection disturbs stomata and damages tissue, so transpiration falls. Less energy is used for evaporation (latent heat), so more goes into sensible heat and the leaf temperature rises (energy balance, Section 1.3.2).');
QA('Why use CTD or NRCT instead of canopy temperature?', 'Canopy temperature follows air temperature and radiation, which change between flights. CTD subtracts air temperature; NRCT scales temperatures within each image from 0 to 1. Both reduce weather effects when all dates are pooled.');
QA('What emissivity do you use and why does it matter?', 'About 0.98 for a green canopy. The camera measures radiance; converting radiance to temperature requires emissivity. An error of 0.01 in emissivity gives a temperature error of roughly 0.5–0.8 K, so the same value and atmospheric settings are used for all flights.');
QA('What is the spatial resolution of your sensors and why does it matter?', 'RGB has the finest pixels (sub-centimetre to about a centimetre at 30 m), the multispectral and thermal cameras a few centimetres, and the SWIR hyperspectral sensor about 36 cm. Fine pixels resolve pustule texture; coarse pixels mix canopy and soil, so plot means use only pure canopy pixels.');
QA('Why not use only the hyperspectral sensor, since it covers the most wavelengths?', 'It does not measure temperature and has coarser pixels than the RGB camera, so it misses transpiration change and fine texture. Mahlein et al. (2019) found that adding thermal to hyperspectral improved accuracy. The thesis tests this rather than assuming it.');
QA('How do you calibrate the multispectral and hyperspectral data?', 'With the empirical line method: calibration panels of known reflectance are imaged every flight, and a linear gain and offset per band convert digital numbers to reflectance (Smith and Milton, 1999); the MicaSense irradiance sensor also corrects changing sunlight.');
QA('How do you handle mustard flowering?', 'Yellow flowers increase visible reflectance and lower NDVI, which can confuse canopy masks and indices. The mask threshold is checked on every flight, flowering stage is recorded, and because dates are pooled, the models learn disease effects across flowering and non-flowering canopies.');
QA('What is the difference between multispectral and hyperspectral sensing?', 'A multispectral camera records a few broad, separated bands (here five, from blue to NIR); a hyperspectral sensor records hundreds of narrow, contiguous bands (here 481 retained bands, 400–2500 nm), giving a continuous spectrum in which narrow pigment and water features can be resolved.');
QA('What is ground sampling distance and how does flight height affect it?', 'GSD is the ground size of one pixel: GSD = detector pixel size × flight height / focal length. Doubling the height doubles the GSD and halves the detail; all flights are at 30 m so that the GSD is constant.');
QA('Why do you fly between 11:00 and 14:00 h?', 'The sun is high and changes little, so illumination is strong and stable and shadows are minimal; transpiration is near its daily maximum, which gives the largest thermal contrast between healthy and stressed canopies.');
QA('Why 85% forward and 80% side overlap?', 'Structure-from-motion needs every ground point in several images to match features and compute camera positions; homogeneous crop canopies have few distinctive features, so high overlap is needed for a reliable orthomosaic and surface model.');
QA('What is structure-from-motion?', 'A photogrammetric method that finds matching features in overlapping images, solves the camera positions and orientations (bundle adjustment) and reconstructs a dense 3-D point cloud, from which a digital surface model and an orthomosaic are produced.');
QA('Why do you need ground control points?', 'GNSS-surveyed GCPs georeference the orthomosaics accurately and make the products of all four sensors overlap pixel-to-plot, so that the same plot polygon extracts the same canopy from every sensor.');
K.push(H2('11.3 Pre-processing and features'));
QA('Why do you smooth spectra before taking derivatives?', 'Differentiation amplifies random noise. The Savitzky–Golay filter fits a local polynomial, removing noise but preserving the shape and position of absorption features, and gives the derivatives from the same fit (Section 8.3.1).');
QA('What do first and second derivatives add?', 'The first derivative removes constant offsets and shows slopes (e.g. the red edge); the second derivative removes linear trends and separates overlapping absorption features. Shukla et al. (2024) and Baranowski et al. (2015) found derivative spectra useful for Brassica stresses.');
QA('What is GLCM texture?', 'A grey-level co-occurrence matrix counts how often pairs of grey levels occur next to each other; measures such as contrast, homogeneity and entropy describe how patchy an image is. Pustules make the canopy patchier, raising contrast and entropy (Section 8.3.3).');
QA('In the GLCM formulas, what are i and j?', 'Grey levels (rows and columns of the co-occurrence matrix), not pixel coordinates.');
QA('Why did you add DWSI and ROTI to the hyperspectral indices?', 'They are SWIR-based disease–water indices that worked for mustard Sclerotinia rot in Bharatpur (Bhattacharya and Chattopadhyay, 2013). The sensor covers the SWIR, so they are tested for white rust; ROTI uses 1982 nm, close to the removed water band, so it is computed only if that band passes the noise check.');
QA('Why not use all published indices?', 'Many indices repeat the same bands and add collinearity. The list keeps the ORW indices (with corrected formulas) and indices proven in disease studies; Boruta and VIF then remove irrelevant and redundant ones.');
QA('What is a spectral disease index and how is your WRI different from NDVI?', 'NDVI responds to any loss of green biomass. A spectral disease index is searched specifically to separate healthy from diseased canopy: the WRI is the normalised difference of two bands plus a weighted third band, chosen by ReliefF and exhaustive search for the best balanced accuracy (Mahlein et al., 2013).');
QA('How is the red-edge position computed?', 'As the wavelength of the maximum of the first-derivative spectrum between 680 and 750 nm (REP); the height of that maximum is Dr and the area under the first derivative in that range is SDr (Filella and Peñuelas, 1994).');
QA('What do PSSRa, PSRI and PRI measure?', 'PSSRa = R800/R680 tracks chlorophyll a; PSRI = (R680 − R500)/R750 tracks the carotenoid-to-chlorophyll ratio, which rises with senescence; PRI = (R531 − R570)/(R531 + R570) tracks xanthophyll-cycle changes related to photosynthetic light-use efficiency.');
QA('Mahlein et al. (2013) searched 450–950 nm. Why do you also use SWIR for the WRI?', 'Their analysis covered that range. My hyperspectral sensor also covers the SWIR, and SWIR bands were the most sensitive to mustard Sclerotinia rot and entered the best three-band index (Bhattacharya and Chattopadhyay, 2013); so the search is run with and without SWIR and the better index is kept.');

K.push(H2('11.4 Methodology design and validation'));
[
  ['Why are all dates pooled?', 'Severity develops over time, so only the pooled data contain all severity levels; one model then works for any flight. Liu et al. (2024) also built one disease-index model over five dates.'],
  ['Why are detection and severity treated separately?', 'They are different decisions with different features: detection separates healthy from diseased canopy, severity separates degrees of damage. Separate DSF pools and models give better and more interpretable results; applied in sequence they give one map.'],
  ['Why are some methods only for hyperspectral data?', 'Band-level methods (correlation scalograms, ReliefF on bands, WRI) need many contiguous bands. MS has five bands, and RGB and thermal features are not spectral bands; for those, statistics and Boruta on their features are used.'],
  ['What is ML-SFFS fusion?', 'Features from several sensors are pooled and SFFS, with a classifier or regressor as judge, picks the smallest cross-sensor combination with the best performance (Mustafa et al., 2023).'],
  ['Why compare ML-SFFS fusion with DNN fusion?', 'ML-SFFS gives a small, interpretable feature set; DNN-F2 learns sensor-specific representations and was the best fusion model of Maimaitijiang et al. (2020).'],
  ['How do you avoid over-optimistic accuracy?', 'All selection and tuning are repeated inside training replications; a test replication is never seen, with all observations of a plot kept together; final testing is at Bharatpur and in farmers\' fields.'],
  ['Why did you correct some index formulas?', 'Several formulas in the slides differed from the original papers (e.g. RARSc, NPCI, VIgreen, PPR, WI/NDVI); the original definitions are used so that results are comparable with the literature.'],
  ['Is there earlier hyperspectral disease or pest work on mustard in India?', 'Yes, both from Bharatpur. Shukla et al. (2024) found aphid-sensitive regions at 483–487, 509–515, 690–714 and 719–723 nm with ground spectroscopy and predicted severity grade with PLSR (r^{2} 0.71). Bhattacharya and Chattopadhyay (2013, SAC-ISRO and DRMR) tracked Sclerotinia rot with weather, MODIS and Hyperion data and proposed the SWIR-based ROTI. Neither used a UAV or studied white rust; this thesis tests their bands and indices for white rust.'],
  ['Why compute CTR in kelvin?', 'A ratio of Celsius temperatures changes with the zero point of the scale; in kelvin the ratio is physically meaningful.'],
].forEach(([q, a]) => { K.push(new Paragraph({ spacing: { before: 100, after: 40 }, keepNext: true, children: [new TextRun({ text: 'Q. ' + q, bold: true, font: FONT, size: 21 })] })); K.push(P('A. ' + a)); });
QA('What is the difference between classification and regression in your work?', 'Classification predicts a category (healthy vs diseased; Low, Moderate or High severity); regression predicts the disease index as a continuous percentage. Both are supervised: they learn from plots with known ground truth.');
QA('Why do you need feature selection when you have powerful models?', 'With about 1300 plot-dates and up to 1500 hyperspectral features, models overfit (Hughes phenomenon). Selection removes irrelevant and redundant features, improves generalisation and makes results interpretable. Tian et al. (2021) obtained up to 10% higher accuracy with ML-SFFS than with all features.');
QA('What is overfitting and how do you prevent it?', 'Learning noise in the training data so that performance on new plots drops. Prevention: feature selection, regularisation (C in SVM, leaf size in RF, dropout and early stopping in DNNs), nested cross-validation, and testing on independent sites.');
QA('What is data leakage?', 'When information from test data influences training, e.g. selecting features on all data before cross-validation. It gives optimistic accuracy. I repeat all selection and tuning inside the training folds and keep all dates of a plot in the same fold.');
QA('Why leave-one-replication-out rather than random k-fold?', 'Plot-dates of one plot are correlated; random splits would put the same plot in training and test. Each RBD replication contains every treatment, so holding out one replication gives a balanced, independent test set.');
QA('What is nested cross-validation?', 'An outer loop estimates performance; an inner loop, inside each outer training set, selects features and tunes hyperparameters. This prevents tuning on the test data (Cawley and Talbot, 2010).');
QA('How do you handle class imbalance?', 'Stratified folds, class weights inversely proportional to class size (Eq. 8.2), and macro-F1 and kappa instead of overall accuracy alone.');
K.push(H2('11.5 Statistics'));
QA('When do you use a t-test and when Mann–Whitney U?', 'Both compare two groups (healthy vs diseased). The t-test compares means and assumes normal data (Welch form for unequal variances); Mann–Whitney U compares ranks and needs no normality. Shapiro–Wilk and Levene tests, plus Q–Q plots, decide (Section 8.4).');
QA('Why do you need a post-hoc test after ANOVA?', 'A significant ANOVA only says that at least one group differs. Tukey HSD (or Dunn after Kruskal–Wallis) shows which pairs differ — e.g. healthy vs Low for detection, Low vs Moderate vs High for severity — while controlling the error rate over all pairs.');
QA('Why Spearman rather than Pearson correlation?', 'Spearman uses ranks, so it captures any monotonic relation and is robust to outliers and to the many zero DI values of healthy plots. Pearson is reported alongside for comparison with the literature.');
QA('Your plot-dates are repeated measures. Are your p-values valid?', 'They are optimistic, because observations of the same plot are correlated. That is why tests are used only to describe and rank features; the decisive evidence is the accuracy on held-out replications and at the independent site. A mixed model with plot as a random effect could be used as a check.');
QA('How do you deal with testing hundreds of features?', 'p-values are adjusted for multiple comparisons (Holm, 1979) and interpreted with effect sizes (|ρ|, point-biserial r) and with Boruta, which uses its own corrected test.');
QA('What is the Jeffries–Matusita distance?', 'A measure of separability between two class distributions, from 0 (identical) to 2 (no overlap), computed from the Bhattacharyya distance under a normal assumption. It shows which severity classes overlap; it is used for reporting, not for selecting features (Section 8.5.5).');
QA('Why did you not use the separability-scalogram threshold of Tian et al. (2021)?', 'It looks for bands where classes do not overlap. White rust severity classes are cuts on a continuous DI and overlap by nature, so very few bands would pass. A correlation scalogram against DI needs no class boundaries, and ReliefF is designed for overlapping, noisy, multi-class data.');
QA('What is discriminant analysis and how do you use it?', 'It finds linear combinations of features (discriminant functions) that maximise the ratio of between-class to within-class variance (Fisher, 1936). I use stepwise canonical discriminant analysis per sensor to test whether healthy, Low, Moderate and High differ in the multivariate DSF space (Wilks\' lambda), to see which features drive the separation and to plot the classes in canonical space (Step 1.6), following Bhattacharya and Chattopadhyay (2013).');
QA('How did Shukla et al. (2024) discriminate the aphid severity grades?', 'Not with a formal discriminant analysis, but by comparing grade-wise spectra and derivatives, Spearman correlation of reflectance, first and second derivatives with the grade, and the loading weights of PCA and PLSR: bands at the loading maxima and minima (500, 679, 746, 979 nm by PCA; 491, 679, 746, 979 nm by PLSR) were taken as the bands that discriminate the grades. I use this as Sub-step F of Step 1.2.');
QA('What is the difference between LDA and PCA?', 'Both give linear combinations of features. PCA is unsupervised and maximises total variance; LDA is supervised and maximises separation between known classes relative to the spread within classes. For disease classes LDA is the relevant one; PCA loadings need supervised confirmation (e.g. PLS loadings or correlation).');
QA('What does Wilks\' lambda tell you?', 'The proportion of total variance not explained by group differences: near 0 means the classes are well separated, 1 means no separation. In stepwise discriminant analysis the feature that most reduces lambda is entered first.');

K.push(H2('11.6 Feature selection'));
QA('How does ReliefF work?', 'For each sample it finds the nearest neighbours of the same class and of other classes; a feature gains weight if it differs between neighbours of different classes and loses weight if it differs between neighbours of the same class. It detects interactions and suits overlapping classes.');
QA('What are shadow features in Boruta?', 'Shuffled copies of the real features, which carry no information. A real feature is relevant only if its random-forest importance is consistently higher than the best shadow feature, tested with a binomial test over repeated runs.');
QA('Difference between Boruta and SFFS?', 'Boruta is all-relevant: it keeps every feature related to the target, which suits characterisation. SFFS is minimal-optimal: it finds the smallest subset that maximises a model\'s performance, which suits prediction.');
QA('Why VIF < 10?', 'VIF = 10 means 90% of a feature\'s variance is explained by the others (R^{2} = 0.9). It is a widely used threshold (Kutner et al., 2005) and was used by Tian et al. (2021) and Mustafa et al. (2023).');
QA('What is the "floating" in SFFS?', 'After each forward step, SFFS conditionally removes features while this improves the criterion, so it can undo earlier choices; plain forward selection cannot (nesting problem; Pudil et al., 1994).');
QA('How is SFFS used for fusion?', 'Features of several sensors are pooled and SFFS, with a classifier as judge, picks the best cross-sensor combination (Mustafa et al., 2023). The sensor make-up of the selected subset shows which sensors contribute.');
K.push(H2('11.7 Models'));
QA('Explain the SVM in one minute.', 'SVM finds the separating boundary with the largest margin to the nearest samples (support vectors). Slack variables with penalty C allow overlap. The RBF kernel maps data implicitly to a higher-dimensional space, giving non-linear boundaries. Prediction depends only on the support vectors.');
QA('What do C and γ control?', 'C trades margin width against training errors (large C fits training data closely, risk of overfitting). γ sets the kernel width (large γ gives very local, wiggly boundaries). Both are tuned by grid search on a log2 scale.');
QA('How does SVM handle three classes?', 'One-vs-one: one binary SVM per pair of classes (3 for 3 classes) and majority voting (LIBSVM; Chang and Lin, 2011).');
QA('What is the ε in SVR?', 'The half-width of a tube around the regression function within which errors are ignored; only samples outside the tube become support vectors.');
QA('Why does random forest generalise better than one tree?', 'Each tree is trained on a bootstrap sample with random feature subsets, so trees make different errors; averaging many decorrelated trees reduces variance without increasing bias much (Breiman, 2001).');
QA('What is the Gini index?', '1 − Σ p_{k}^{2}, the probability of misclassifying a randomly chosen sample if labelled according to the class proportions in the node; 0 for a pure node. Splits maximise the decrease in Gini.');
QA('What is out-of-bag error and why do you not report it?', 'Error on samples not in a tree\'s bootstrap sample (~36.8%). With repeated plot-dates, OOB samples include other dates of training plots, so it is optimistic; I report grouped cross-validation instead.');
QA('How do you choose k in k-NN?', 'By inner cross-validation over odd values 3–11. Small k is sensitive to noise, large k smooths class borders. Features must be standardised because k-NN uses distances.');
QA('Why PLSR as a baseline?', 'It is the standard linear method for many collinear spectral predictors: it projects features onto a few components with maximum covariance with DI. If non-linear models do not beat PLSR, the extra complexity is not justified.');
QA('What is the difference between PLSR and PCA regression?', 'PCA components maximise the variance of X only; PLS components maximise covariance between X and y, so they are more relevant for prediction with fewer components.');
K.push(H2('11.8 Deep learning and fusion'));
QA('What is the difference between DNN-F1 and DNN-F2?', 'DNN-F1 concatenates all features at the input. DNN-F2 gives each sensor its own sub-network, then concatenates the learned representations in an intermediate layer. DNN-F2 was more accurate and robust in Maimaitijiang et al. (2020).');
QA('Why ReLU?', 'max(0, z) is cheap, does not saturate for positive inputs (less vanishing gradient than sigmoid) and works well with He initialisation.');
QA('What do batch normalisation and dropout do?', 'Batch normalisation standardises layer inputs per mini-batch, speeding and stabilising training. Dropout randomly disables neurons during training, preventing co-adaptation and overfitting.');
QA('How does Adam work?', 'It keeps running averages of gradients and squared gradients, corrects their bias, and updates each weight with its own adaptive step size (Kingma and Ba, 2015). Default learning rate 0.001.');
QA('How many parameters does your network have, and is your dataset enough?', 'About 1500–4200 trainable parameters for the planned sizes (Table ' + (TORDER.indexOf('mldnncount') + 1) + '). With about 1300 post-symptomatic plot-dates this is feasible only with small layers, dropout, early stopping and repeated runs; for the 432 pre-symptomatic plot-dates I do not use DNNs.');
QA('What are the levels of data fusion and which do you use?', 'Data level (raw data), feature level (features combined) and decision level (model outputs combined). I use feature level: ML-SFFS fusion and DNN fusion, because the sensors differ in resolution and units but give comparable plot-level features.');
K.push(H2('11.9 Evaluation'));
QA('Why macro-F1 and kappa instead of only overall accuracy?', 'Overall accuracy can be high if the model predicts the majority class well and ignores rare classes. Macro-F1 averages F1 over classes equally, and kappa corrects for chance agreement.');
QA('Compute kappa for your example confusion matrix.', 'OA = 87/120 = 0.725; p_{e} = (50×52 + 40×39 + 30×29)/120^{2} = 0.349; κ = (0.725 − 0.349)/(1 − 0.349) = 0.577, moderate agreement (Landis and Koch, 1977).');
QA('Difference between precision and recall?', 'Precision: of plots predicted diseased, the fraction truly diseased. Recall (sensitivity): of truly diseased plots, the fraction detected. In disease scouting, high recall avoids missing infected fields.');
QA('Why NRMSE rather than relative error?', 'Relative error divides by each measured DI and is undefined for healthy plots (DI = 0); NRMSE divides RMSE by the mean DI.');
QA('Can R² be negative?', 'Yes, on test data, when the model predicts worse than simply using the mean of the observed DI; it indicates a poor model.');

// ===== REFERENCES =====
K.push(H2('11.10 Design choices and alternatives'));
QA('If all dates are pooled, could growth stage be confused with disease?', 'Growth stage changes the canopy, but un-inoculated control plots are flown on every date, so healthy references exist at every stage, and staggered sowing puts different stages on the same date. Normalised indices and thermal normalisation further reduce stage and weather effects.');
QA('Many healthy plots have DI = 0. Does this bias the DI regression?', 'It can pull predictions towards zero. Applying the models in sequence (detection, then severity) handles it in practice, and errors are also reported for diseased plot-dates only, so the regression is judged where severity matters.');
QA('What happens to plots near the class limits of 25% and 50%?', 'They are the hardest to classify because small scoring differences move them across a limit. Their errors appear as confusion between adjacent classes, which macro-F1 and the confusion matrix make visible, and DI regression gives a continuous estimate that avoids the limits.');
QA('Why not train a convolutional neural network on the images directly?', 'With 72 plots there is too little labelled data for an image CNN; Deng et al. (2024) needed a dataset of more than 180 million annotated pixels. Feature-based models are also easier to interpret physically. A CNN is a possible extension once more seasons are available.');
QA('Why not reduce the hyperspectral data with PCA?', 'PCA is unsupervised: components maximise variance, not disease information, and each component mixes all bands, so physical interpretation is lost. Supervised selection keeps original, interpretable bands and indices.');
QA('What are filter, wrapper and embedded feature-selection methods?', 'Filters rank features by a statistic independent of the model (ReliefF, correlation, VIF); wrappers evaluate subsets with a model (Boruta, SFFS); embedded methods select during training (LASSO, tree importance) (Guyon and Elisseeff, 2003).');
QA('Why only six models?', 'They cover the main model families — kernel (SVM/SVR), tree ensemble (RF/RFR), instance-based (k-NN), linear latent-variable (PLSR) and deep learning with two fusion levels (DNN-F1, DNN-F2) — all used in the core papers. More models would add comparisons without adding understanding.');
QA('How do you express uncertainty in your accuracy?', 'As mean ± standard deviation over the three held-out replications, with confusion matrices for each fold; ML-SFFS is repeated with different fold assignments and DNNs are trained with several random seeds, and the spread of results is reported.');
QA('Why not decision-level fusion?', 'Decision-level fusion combines the outputs of separate single-sensor models (voting or averaging). It is simple but cannot use interactions between features of different sensors; feature-level fusion can, and it is the level compared by Mustafa et al. (2023) and Maimaitijiang et al. (2020).');
K.push(H2('11.11 Results, limitations and relevance'));
QA('What results do you expect?', 'Pigment and red-edge features (MS, HS) and thermal features to respond most to white rust; texture to add information at high severity; HS + TIR to be the best pair and full fusion to improve DI estimation; DNN-F2 and ML-SFFS fusion to be close, with ML-SFFS more interpretable; pre-symptomatic detection to be possible but less accurate than post-symptomatic detection.');
QA('What if fusion does not improve over the best single sensor?', 'That is a valid result: it would mean the sensors are redundant for white rust and the cheaper sensor is enough. Mahlein et al. (2019) found that a third sensor did not help. The thesis reports it with the cross-sensor correlation that explains why.');
QA('What if pre-symptomatic detection fails?', 'The thesis then reports how early detection becomes reliable after symptoms appear and which physiological parameters changed first, which is still useful for timing surveys and sprays.');
QA('How would you separate white rust from Alternaria blight or downy mildew?', 'In this experiment other diseases are recorded and kept low; a disease-specific index and multi-class models would be needed in farmers\' fields where they co-occur. The SWIR and thermal signatures and the pustule texture differ between diseases, which can be tested in the validation stage.');
QA('How can your results be used by ISRO?', 'Sensitive bands and indices can be transferred to Sentinel-2 or Resourcesat multispectral data, the White Rust Index to spaceborne hyperspectral sensors such as HySIS, PRISMA or EnMAP, and thermal features to future thermal missions such as TRISHNA. UAV maps can serve as reference data for satellite models (Section 9.5).');
QA('Can a satellite with 30 m pixels detect white rust?', 'Only when the disease covers a large part of the pixel, because a 30 m pixel mixes many plants and soil. Bhattacharya and Chattopadhyay (2013) detected Sclerotinia rot with 30 m Hyperion data at patch scale. UAV results identify which bands to use and give training data for such models.');
QA('What is the main limitation of your study?', 'Model development uses one season and one site with repeated observations of 72 plots. This is handled by plot-grouped LORO validation and by independent validation at Bharatpur and in farmers\' fields (Section 9.4).');
K.push(H2('11.12 Literature'));
QA('Which paper is your methodology mainly based on?', 'Eight core papers: Tian et al. (2021) and Mustafa et al. (2023) for feature selection and ML-SFFS, Mahlein et al. (2013) for the disease index, Mahlein et al. (2019) for sensor combinations, Maimaitijiang et al. (2020) for DNN fusion, and Guo et al. (2021), Feng et al. (2022) and Liu et al. (2024) for UAV indices, texture and thermal features.');
QA('Which study is closest to yours in sensors?', 'Liu et al. (2024) used UAV multispectral + thermal for wheat powdery mildew; Feng et al. (2022) fused hyperspectral, thermal and RGB at 1 m; Maimaitijiang et al. (2020) fused UAV RGB, multispectral and thermal with DNNs. No study used all four UAV sensors for a disease.');
QA('What did Bohnenkamp et al. (2019) teach you?', 'That feature sets selected at one scale or with one sensor did not transfer to another; selection must be done on the data being analysed. Therefore all selection is repeated on UAV data inside training folds.');
QA('Which work from your own institute is related?', 'ICAR-IARI studies used field spectroradiometers for wheat yellow rust (Krishna et al., 2014), rice blast (Mandal et al., 2022, 2023; Ramalingam et al., 2026) and rice genotypes (Das et al., 2020), with PLSR, SVM, JM distance and new indices. This thesis extends that work to UAV imaging, four sensors, fusion and pre-symptomatic prediction.');

K.push(H1('12. NRSC / SAC (ISRO) interview: questions and answers'));
K.push(P(`Interview panels at the National Remote Sensing Centre (NRSC, Hyderabad) and the Space Applications Centre (SAC, Ahmedabad) usually test remote-sensing fundamentals, data-quality problems and how a thesis connects to satellite missions. Each answer below has three parts: the concept, **how this thesis solves the problem**, and **how other researchers dealt with it**, with references.`));
K.push(H2('12.1 Hyperspectral data problems'));
QA3('Neighbouring hyperspectral bands are highly correlated. How do you deal with it?',
 'Adjacent bands are controlled by the same absorbers and structure and the sensor\'s spectral response overlaps, so they are near-duplicates (multicollinearity). This inflates the effective dimensionality, destabilises linear models and makes covariance matrices singular.',
 'I quantified it on my mustard ASD spectra (bands 10 nm apart: median r = 0.9997; 349 bands form only 18 regions with r ≥ 0.95) and then: keep one band per correlated region in the band-level analysis; use derivatives and band contrasts; average to 6 nm and keep combined bands 50 nm apart in the WRI search; remove remaining collinearity with VIF < 10; let ML-SFFS keep only non-redundant features; use PLSR for collinear predictors (Section 4.2.1).',
 'Tian et al. (2021) kept one representative feature per common feature region and applied VIF < 10; Mustafa et al. (2023) applied VIF after Boruta; Mahlein et al. (2013) reduced spectral resolution to 6 nm and set a 50 nm minimum distance; Bhattacharya and Chattopadhyay (2013) used single bands out of clusters of close bands in a stepwise discriminant analysis; Zhu et al. (2017) and Huang et al. (2020) used SPA, which selects wavelengths with minimum collinearity (Araújo et al., 2001); Shukla et al. (2024) and Krishna et al. (2014) used PLS loading weights.');
QA3('What is the Hughes phenomenon and how do you avoid it?',
 'For a fixed number of training samples, classification accuracy first rises and then falls as more features are added, because the parameters cannot be estimated reliably (Hughes, 1968).',
 'I have about 1300 plot-dates from 72 plots but more than 1500 hyperspectral features, so I reduce features in stages (band-level selection, Boruta, VIF, ML-SFFS) to fewer than ten per model and validate on held-out replications.',
 'Tian et al. (2021) showed that 2–4 ML-SFFS features were enough and up to 10% more accurate than all features; Mustafa et al. (2023) used Boruta → VIF → ML-SFFS; Zhu et al. (2017) reduced 512 bands to a few effective wavelengths.');
QA3('How do you deal with noisy bands and low signal-to-noise ratio?',
 'Detector edges and atmospheric water-vapour bands have very little signal, so their reflectance is mostly noise.',
 'I remove 1350–1450 and 1800–1950 nm and noisy sensor edges, smooth with Savitzky–Golay, and compute ROTI only if its 1982 nm band passes the noise check.',
 'Mahlein et al. (2013) restricted analysis to 450–950 nm for adequate SNR; Shukla et al. (2024) removed 350–400, 1301–1500, 1780–2050 and 2351–2500 nm; Ramalingam et al. (2026) used SNV and MSC normalisation and an isolation-forest outlier filter.');
QA3('Why use derivative spectra?',
 'First derivatives remove additive offsets and show slopes such as the red edge; second derivatives remove linear trends and separate overlapping absorption features (Tsai and Philpot, 1998).',
 'I compute FD and SD from the Savitzky–Golay fit for all 481 bands and include red-edge parameters (REP, Dr, SDr); derivative bands are also much less correlated than reflectance.',
 'Shukla et al. (2024) found sensitive aphid regions with FD and SD; Baranowski et al. (2015) classified Alternaria infection of oilseed rape best with second derivatives; Lv et al. (2023) improved severity classification by adding first derivatives; Mandal et al. (2022) used the red-edge peak amplitude for rice blast.');
K.push(H2('12.2 Radiometry, geometry and data quality'));
QA3('How do you correct UAV images radiometrically and atmospherically?',
 'At 30 m altitude the atmospheric path is short, so a full atmospheric model is not needed; the main task is converting digital numbers to reflectance and correcting changes in sunlight.',
 'I use the empirical line method with calibration panels imaged on every flight, the MicaSense downwelling irradiance sensor for changing light, white-reference calibration for the hyperspectral camera, and radiometric conversion of thermal data with emissivity, air temperature, humidity and height, checked against ground targets.',
 'Smith and Milton (1999) established the empirical line method; Aasen et al. (2018) review UAV spectroscopy calibration workflows; Maimaitijiang et al. (2020) calibrated the same FLIR thermal camera with ground targets.');
QA3('How do view-angle and BRDF effects affect your UAV mosaics?',
 'Reflectance depends on sun and view geometry (bidirectional reflectance distribution function); in a UAV mosaic, pixels come from different view angles and can show hot-spot or brightness gradients (Schaepman-Strub et al., 2006).',
 'Flights are at near-solar-noon (11:00–14:00 h) under clear sky with 85%/80% overlap, so the mosaic uses near-nadir parts of images; plot means over many pixels average the remaining effects, and control plots on every flight provide a within-flight reference.',
 'Aasen et al. (2018) discuss BRDF correction and recommend high overlap and near-nadir pixels for UAV spectroscopy; Guo et al. (2021) and Liu et al. (2024) flew around midday for the same reason.');
QA3('How do you handle mixed pixels of canopy, soil and shadow?',
 'A pixel that contains canopy and soil gives a mixed spectrum and temperature, which weakens the disease signal.',
 'I use a 0.5 m inner plot buffer and canopy masks (NDVI threshold for MS/HS, K-means for RGB and thermal), checked on every flight because yellow flowers lower NDVI; SWIR pixels (about 36 cm) are used only if enough pure pixels remain.',
 'Feng et al. (2022) segmented canopy with K-means; Guo et al. (2021) used an NDVI mask and showed that pixel size strongly affects texture accuracy; Bhattacharya and Chattopadhyay (2013) used a LISS-IV crop mask; at satellite scale spectral unmixing separates mixed signals (Keshava and Mustard, 2002).');
QA3('How do you co-register four sensors with different pixel sizes?',
 'Products must refer to the same ground position, but resampling all sensors to one grid would blur the finest data.',
 'All orthomosaics use the same GNSS-surveyed ground control points, and features are extracted per plot polygon in each sensor\'s native resolution, so fusion happens at plot-feature level without resampling.',
 'Feng et al. (2022) and Maimaitijiang et al. (2020) also fused plot-level features from RGB, multispectral and thermal sensors.');
QA3('How do you make thermal data comparable between flights?',
 'Canopy temperature depends on air temperature, radiation, wind and humidity, which change between flights; raw temperature differences between dates are therefore not disease effects.',
 'I warm up the camera for 15–20 min, convert radiance with emissivity and meteorological data, and use normalised indices (CTD, CTR in kelvin, NRCT scaled within each image, MTD within the plot).',
 'Feng et al. (2022) used CT, CTD, CTR and NRCT; Liu et al. (2024) showed that canopy temperature tracks powdery-mildew DI; Mahlein et al. (2019) used MTD.');
K.push(H2('12.3 Disease-specific problems'));
QA3('How do you separate disease from water or nutrient stress?',
 'Chlorophyll loss, NIR decline and canopy warming are also caused by drought or nutrient deficiency, so a general stress index cannot identify the cause.',
 'The experiment has uniform irrigation and fertiliser and un-inoculated controls on every date; I build a White Rust Index specific to the disease, add disease–water indices (DWSI, ROTI), and check that warmer diseased plots do not have lower water status (thermal vs water index).',
 'Zhang et al. (2012b) found that only PhRI responded to yellow rust but not to nutrient stress; Bhattacharya and Chattopadhyay (2013) used the TVDI–NDWI space (canopy stress without soil-moisture stress = rot); Mahlein et al. (2013) designed indices that separate three sugar-beet diseases.');
QA3('Your severity classes overlap. How do you discriminate them?',
 'Classes cut from a continuous DI overlap near their limits, so methods that require non-overlapping classes fail.',
 'I use a correlation scalogram against DI (no class limits), ReliefF (designed for overlapping, noisy classes), a two-step stepwise canonical discriminant analysis following Stage III of Bhattacharya and Chattopadhyay (2013), JM distance only to report overlap, DI regression in parallel, and macro-F1 to show per-class performance.',
 'Tian et al. (2021) used separability thresholds, which suit non-overlapping stages; Meng et al. (2020) reached only 70% for three severity levels with ReliefF indices; Lv et al. (2023) improved severity classification by about 7% by combining features with ReliefF + SFFS; Mandal et al. (2023) used JM and found two adjacent blast levels inseparable.');
QA3('How do you discriminate between disease classes statistically?',
 'Discriminant analysis finds linear combinations of features that maximise between-class relative to within-class variance (Fisher, 1936); stepwise selection by Wilks\' lambda keeps the features that add separation.',
 'Section 4.6.1 adapts the two-step design: stepwise canonical discriminant analysis on region-representative bands, response curves, candidate indices, a second stepwise analysis on indices, thresholds and validation on held-out replications.',
 'Bhattacharya and Chattopadhyay (2013) used this design on Hyperion data for mustard rot; Zhang et al. (2012a) used Fisher LDA for three powdery-mildew levels; Shukla et al. (2024) discriminated aphid grades with PCA/PLSR loading weights; Das et al. (2020) used CART, JM and QDA.');
QA3('How do you label plots before symptoms appear?',
 'Before symptoms DI = 0 everywhere, so the true state of an inoculated plot is unknown at the time of the flight.',
 'An inoculated plot is labelled infected only if symptoms later appear on it; controls are healthy; inoculated resistant plots that never show symptoms are excluded and reported separately.',
 'Tian et al. (2021) used the same retrospective labelling for rice blast; Zhu et al. (2017) and Terentev et al. (2023) used days after inoculation under controlled conditions.');
QA3('How reliable is your ground truth?',
 'Visual scores are subjective and sampled, so label noise limits the achievable accuracy.',
 'Leaves are scored on a 0–6 area scale at five points per plot by the same trained scorer, and DI is computed with the standard formula (Liu et al., 2024); class limits are explicit, and errors near limits are reported.',
 'Shukla et al. (2024) used expert entomologist ratings of aphid grade; Mandal et al. (2023) used the IRRI 0–9 blast scale; Bhattacharya and Chattopadhyay (2013) used incidence counts in fields.');
K.push(H2('12.4 Models, fusion and validation'));
QA3('How do you prevent over-optimistic accuracy?',
 'If test data influence feature selection or tuning, or if dates of the same plot are in both training and test sets, accuracy is inflated (selection bias and spatial/temporal dependence).',
 'Leave-one-replication-out cross-validation keeps all dates of a plot together; every selection and tuning step is repeated inside the training replications (nested CV); final testing is at Bharatpur and in farmers\' fields.',
 'Ambroise and McLachlan (2002) and Varma and Simon (2006) showed selection bias; Roberts et al. (2017) recommend block cross-validation for dependent data; Feng et al. (2022) validated on a separate experiment; Bohnenkamp et al. (2019) showed that feature sets do not transfer between scales.');
QA3('Which fusion strategy do you use and why?',
 'Fusion can be at data, feature or decision level; feature-level fusion lets features of different sensors interact in one model.',
 'I compare pooled and sensor-wise ML-SFFS fusion (small, interpretable feature sets) with DNN-F1 and DNN-F2 (learned fusion), for each task and four sensor combinations.',
 'Maimaitijiang et al. (2020) found DNN-F2 best for soybean yield; Mustafa et al. (2023) fused sensors with ML-SFFS; Feng et al. (2022) fused spectra, thermal and texture with RFR; Deng et al. (2024) used an end-to-end network; Mahlein et al. (2019) found that a third sensor did not improve accuracy.');
QA3('How do you handle unequal class sizes?',
 'A model can achieve high overall accuracy by ignoring a rare class.',
 'Class weights inversely proportional to class size, stratified folds, equal priors in discriminant analysis, and macro-F1 and kappa as main metrics.',
 'Lv et al. (2023) reported macro-F1 for severity classes; Mahlein et al. (2013) optimised balanced accuracy for their indices.');
QA3('Why not use a deep CNN on the images?',
 'Image CNNs learn features directly but need large labelled datasets.',
 'With 72 plots I use engineered, physically interpretable features and small DNNs only for fusion; a CNN is future work when more seasons are available.',
 'Deng et al. (2024) needed more than 180 million annotated pixels; Nguyen et al. (2023) reached 60–79% with a 3D-CNN for early yellow rust detection.');
QA3('How do you interpret your models?',
 'Interpretation shows whether a model uses physically meaningful signals or artefacts.',
 'ML-SFFS gives small feature sets whose sensor origin and physiology are known; discriminant coefficients and structure correlations show which features separate classes; RF importance is read on the final set; features are correlated with pigments, RWC and stomatal conductance.',
 'Mustafa et al. (2023) interpreted the selected cross-sensor features; Mahlein et al. (2019) correlated sensor parameters with each other and with disease severity; Maimaitijiang et al. (2020) noted that DNNs are less interpretable.');
K.push(H2('12.5 Linking to ISRO missions and applications'));
QA3('How can your UAV results be scaled to satellites?',
 'Satellite pixels (5.8–30 m for optical Indian and international sensors) mix many plants and soil, so UAV relations must be translated to coarser pixels and broader bands.',
 'I identify a minimal set of bands and indices, check which are available on satellite sensors, and use the UAV maps as reference data for training and validating satellite models.',
 'Bhattacharya and Chattopadhyay (2013) mapped mustard rot with 30 m Hyperion data inside a 5.8 m LISS-IV crop mask; Shukla et al. (2024) proposed transferring their bands to aerial and satellite sensors; Bohnenkamp et al. (2019) warned that feature sets do not transfer automatically between scales.');
QA3('Which ISRO sensors could use your findings?',
 'Indian sensors differ in spectral coverage: Resourcesat LISS-IV (5.8 m; green, red, NIR), LISS-III (23.5 m, including SWIR) and AWiFS (56 m); HySIS is a VNIR + SWIR hyperspectral imager (about 30 m); TRISHNA is a planned ISRO–CNES thermal mission.',
 'Indices that need only green, red and NIR can be tested on LISS-IV; red-edge indices need Sentinel-2-type bands; the WRI and SWIR indices need HySIS-type data; thermal features need high-resolution thermal data such as TRISHNA.',
 'Bhattacharya and Chattopadhyay (2013) combined Hyperion and LISS-IV; Liu et al. (2024) used multispectral bands similar to satellite red-edge bands.');
QA3('If SAC designed a sensor for crop-disease monitoring, what would your thesis contribute?',
 'Sensor design needs to know which wavelengths, bandwidths and spatial resolution carry the disease signal.',
 'The ML-SFFS optimum combinations, the WRI and the discriminant bands give a minimal set of disease-relevant wavelengths; the pixel-size test of RGB texture shows the spatial resolution needed; the fusion results show whether thermal data add value.',
 'Mahlein et al. (2013) designed disease indices that can be transferred to multispectral cameras; Zhu et al. (2017) selected effective wavelengths for portable multispectral devices; Thenkabail et al. (2004) identified optimal hyperspectral bands for vegetation.');
QA3('How does early detection help a national monitoring system?',
 'Early, spatial information allows targeted sprays before an epidemic spreads, reducing yield loss and pesticide use.',
 'Objective 3 tests pre-symptomatic prediction and produces plot-wise risk maps; combined with weather-based risk, this could support advisories.',
 'Bhattacharya and Chattopadhyay (2013) combined weather anomalies (Stage I), soil–canopy water stress (Stage II) and hyperspectral discrimination (Stage III) into a multi-stage tracking scheme; Nguyen et al. (2023) estimated that early UAV detection could save 3–7% of yield.');
QA3('What is the main novelty of your work for ISRO?',
 'A novel contribution fills a gap that existing studies have not addressed.',
 'First sensor-based study of white rust in mustard; four UAV sensors on the same plots; a White Rust Index including SWIR; comparison of ML-SFFS and DNN fusion; pre-symptomatic prediction at plot scale; leakage-free validation; and bands that can be tested on ISRO sensors.',
 'The closest Indian work used ground spectroscopy for mustard aphid (Shukla et al., 2024) and Hyperion data for mustard rot (Bhattacharya and Chattopadhyay, 2013); ICAR-IARI studies used field spectroradiometers for wheat and rice diseases (Krishna et al., 2014; Mandal et al., 2023).');

K.push(H1('References'));
const refPara = r => new Paragraph({ spacing: { after: 70, line: 255 }, indent: { left: 400, hanging: 400 }, children: [new TextRun({ text: r, font: FONT, size: 18 })] });
[
  'Aasen, H., Honkavaara, E., Lucieer, A., Zarco-Tejada, P.J. (2018). Quantitative remote sensing at ultra-high resolution with UAV spectroscopy: a review of sensor technology, measurement procedures, and data correction workflows. Remote Sensing 10(7), 1091. https://doi.org/10.3390/rs10071091',
  'Abdulridha, J., Batuman, O., Ampatzidis, Y. (2019). UAV-based remote sensing technique to detect citrus canker disease utilizing hyperspectral imaging and machine learning. Remote Sensing 11(11), 1373. https://doi.org/10.3390/rs11111373',
  'Ambroise, C., McLachlan, G.J. (2002). Selection bias in gene extraction on the basis of microarray gene-expression data. Proceedings of the National Academy of Sciences 99(10), 6562–6566.',
  'Apan, A., Held, A., Phinn, S., Markley, J. (2004). Detecting sugarcane \'orange rust\' disease using EO-1 Hyperion hyperspectral imagery. International Journal of Remote Sensing 25(2), 489–498.',
  'Araújo, M.C.U., Saldanha, T.C.B., Galvão, R.K.H., Yoneyama, T., Chame, H.C., Visani, V. (2001). The successive projections algorithm for variable selection in spectroscopic multicomponent analysis. Chemometrics and Intelligent Laboratory Systems 57(2), 65–73.',
  'Babar, M.A., Reynolds, M.P., van Ginkel, M., Klatt, A.R., Raun, W.R., Stone, M.L. (2006). Spectral reflectance indices as a potential indirect selection criteria for wheat yield under irrigation. Crop Science 46(2), 578–588.',
  'Baranowski, P., Jedryczka, M., Mazurek, W., Babula-Skowronska, D., Siedliska, A., Kaczmarek, J. (2015). Hyperspectral and thermal imaging of oilseed rape (Brassica napus) response to fungal species of the genus Alternaria. PLoS ONE 10(3), e0122913. https://doi.org/10.1371/journal.pone.0122913',
  'Barker, M., Rayens, W. (2003). Partial least squares for discrimination. Journal of Chemometrics 17(3), 166–173.',
  'Barnes, J.D., Balaguer, L., Manrique, E., Elvira, S., Davison, A.W. (1992). A reappraisal of the use of DMSO for the extraction and determination of chlorophylls a and b in lichens and higher plants. Environmental and Experimental Botany 32(2), 85–100.',
  'Barnes, R.J., Dhanoa, M.S., Lister, S.J. (1989). Standard normal variate transformation and de-trending of near-infrared diffuse reflectance spectra. Applied Spectroscopy 43(5), 772–777.',
  'Bausch, W.C., Duke, H.R. (1996). Remote sensing of plant nitrogen status in corn. Transactions of the ASAE 39(5), 1869–1875.',
  'Benjamini, Y., Hochberg, Y. (1995). Controlling the false discovery rate: a practical and powerful approach to multiple testing. Journal of the Royal Statistical Society B 57(1), 289–300.',
  'Bergstra, J., Bengio, Y. (2012). Random search for hyper-parameter optimization. Journal of Machine Learning Research 13, 281–305.',
  'Bhattacharya, B.K., Chattopadhyay, C. (2013). A multi-stage tracking for mustard rot disease combining surface meteorology and satellite remote sensing. Computers and Electronics in Agriculture 90, 35–44. https://doi.org/10.1016/j.compag.2012.10.001',
  'Blackburn, G.A. (1998). Quantifying chlorophylls and carotenoids at leaf and canopy scales: an evaluation of some hyperspectral approaches. Remote Sensing of Environment 66(3), 273–285.',
  'Bock, C.H., Poole, G.H., Parker, P.E., Gottwald, T.R. (2010). Plant disease severity estimated visually, by digital photography and image analysis, and by hyperspectral imaging. Critical Reviews in Plant Sciences 29(2), 59–107.',
  'Bohnenkamp, D., Behmann, J., Mahlein, A.-K. (2019). In-field detection of yellow rust in wheat on the ground canopy and UAV scale. Remote Sensing 11(21), 2495. https://doi.org/10.3390/rs11212495',
  'Bohnenkamp, D., Behmann, J., Paulus, S., Steiner, U., Mahlein, A.-K. (2021). A hyperspectral library of foliar diseases of wheat. Phytopathology 111, 1583–1593. https://doi.org/10.1094/PHYTO-09-19-0335-R',
  'Box, G.E.P. (1949). A general distribution theory for a class of likelihood criteria. Biometrika 36(3–4), 317–346.',
  'Breiman, L. (2001). Random forests. Machine Learning 45(1), 5–32.',
  'Breiman, L., Friedman, J.H., Olshen, R.A., Stone, C.J. (1984). Classification and Regression Trees. Wadsworth, Belmont, CA.',
  'Broge, N.H., Leblanc, E. (2001). Comparing prediction power and stability of broadband and hyperspectral vegetation indices for estimation of green leaf area index and canopy chlorophyll density. Remote Sensing of Environment 76(2), 156–172.',
  'Carter, G.A., Knapp, A.K. (2001). Leaf optical properties in higher plants: linking spectral characteristics to stress and chlorophyll concentration. American Journal of Botany 88(4), 677–684.',
  'Cawley, G.C., Talbot, N.L.C. (2010). On over-fitting in model selection and subsequent selection bias in performance evaluation. Journal of Machine Learning Research 11, 2079–2107.',
  'Chang, C.-C., Lin, C.-J. (2011). LIBSVM: a library for support vector machines. ACM Transactions on Intelligent Systems and Technology 2(3), 27.',
  'Chappelle, E.W., Kim, M.S., McMurtrey, J.E. (1992). Ratio analysis of reflectance spectra (RARS): an algorithm for the remote estimation of the concentrations of chlorophyll a, chlorophyll b, and carotenoids in soybean leaves. Remote Sensing of Environment 39(3), 239–247.',
  'Chen, J.M. (1996). Evaluation of vegetation indices and a modified simple ratio for boreal applications. Canadian Journal of Remote Sensing 22(3), 229–242.',
  'Chen, T., Guestrin, C. (2016). XGBoost: a scalable tree boosting system. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 785–794.',
  'Cheng, T., Rivard, B., Sánchez-Azofeifa, G.A., Feng, J., Calvo-Polanco, M. (2010). Continuous wavelet analysis for the detection of green attack damage due to mountain pine beetle infestation. Remote Sensing of Environment 114(4), 899–910.',
  'Chicco, D., Jurman, G. (2020). The advantages of the Matthews correlation coefficient (MCC) over F1 score and accuracy in binary classification evaluation. BMC Genomics 21, 6.',
  'Chong, I.-G., Jun, C.-H. (2005). Performance of some variable selection methods when multicollinearity is present. Chemometrics and Intelligent Laboratory Systems 78(1–2), 103–112.',
  'Cohen, J. (1960). A coefficient of agreement for nominal scales. Educational and Psychological Measurement 20(1), 37–46.',
  'Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences, 2nd edn. Lawrence Erlbaum, Hillsdale, NJ.',
  'Cortes, C., Vapnik, V. (1995). Support-vector networks. Machine Learning 20(3), 273–297.',
  'Cover, T., Hart, P. (1967). Nearest neighbor pattern classification. IEEE Transactions on Information Theory 13(1), 21–27.',
  'Curran, P.J. (1989). Remote sensing of foliar chemistry. Remote Sensing of Environment 30(3), 271–278.',
  'Das, B., Sahoo, R.N., Biswas, A., Pargal, S., Krishna, G., Verma, R., Chinnusamy, V., Sehgal, V.K., Gupta, V.K. (2020). Discrimination of rice genotypes using field spectroradiometry. Geocarto International 35(1), 64–77.',
  'Dash, J., Curran, P.J. (2004). The MERIS terrestrial chlorophyll index. International Journal of Remote Sensing 25(23), 5403–5413.',
  'Daughtry, C.S.T., Walthall, C.L., Kim, M.S., de Colstoun, E.B., McMurtrey, J.E. (2000). Estimating corn leaf chlorophyll concentration from leaf and canopy reflectance. Remote Sensing of Environment 74(2), 229–239.',
  'Deng, J., Hong, D., Li, C., Yao, J., Yang, Z., Zhang, Z., Chanussot, J. (2024). RustQNet: multimodal deep learning for quantitative inversion of wheat stripe rust disease index. Computers and Electronics in Agriculture 225, 109245.',
  'Dietterich, T.G. (1998). Approximate statistical tests for comparing supervised classification learning algorithms. Neural Computation 10(7), 1895–1923.',
  'Dormann, C.F., Elith, J., Bacher, S., Buchmann, C., Carl, G., Carré, G., Marquéz, J.R.G., Gruber, B., Lafourcade, B., Leitão, P.J., Münkemüller, T., McClean, C., Osborne, P.E., Reineking, B., Schröder, B., Skidmore, A.K., Zurell, D., Lautenbach, S. (2013). Collinearity: a review of methods to deal with it and a simulation study evaluating their performance. Ecography 36(1), 27–46.',
  'Dunn, O.J. (1964). Multiple comparisons using rank sums. Technometrics 6(3), 241–252.',
  'Efron, B., Tibshirani, R. (1997). Improvements on cross-validation: the .632+ bootstrap method. Journal of the American Statistical Association 92(438), 548–560.',
  'Fawcett, T. (2006). An introduction to ROC analysis. Pattern Recognition Letters 27(8), 861–874.',
  'Feng, Z., Song, L., Duan, J., He, L., Zhang, Y., Wei, Y., Feng, W. (2022). Monitoring wheat powdery mildew based on hyperspectral, thermal infrared, and RGB image data fusion. Sensors 22(1), 31. https://doi.org/10.3390/s22010031',
  'Filella, I., Peñuelas, J. (1994). The red edge position and shape as indicators of plant chlorophyll content, biomass and hydric status. International Journal of Remote Sensing 15(7), 1459–1470.',
  'Fisher, R.A. (1936). The use of multiple measurements in taxonomic problems. Annals of Eugenics 7(2), 179–188.',
  'Friedman, J.H. (1989). Regularized discriminant analysis. Journal of the American Statistical Association 84(405), 165–175.',
  'Gamon, J.A., Peñuelas, J., Field, C.B. (1992). A narrow-waveband spectral index that tracks diurnal changes in photosynthetic efficiency. Remote Sensing of Environment 41(1), 35–44.',
  'Geladi, P., Kowalski, B.R. (1986). Partial least-squares regression: a tutorial. Analytica Chimica Acta 185, 1–17.',
  'Gillespie, A., Rokugawa, S., Matsunaga, T., Cothern, J.S., Hook, S., Kahle, A.B. (1998). A temperature and emissivity separation algorithm for Advanced Spaceborne Thermal Emission and Reflection Radiometer (ASTER) images. IEEE Transactions on Geoscience and Remote Sensing 36(4), 1113–1126.',
  'Gitelson, A., Merzlyak, M.N. (1994). Spectral reflectance changes associated with autumn senescence of Aesculus hippocastanum L. and Acer platanoides L. leaves. Journal of Plant Physiology 143(3), 286–292.',
  'Gitelson, A.A., Gritz, Y., Merzlyak, M.N. (2003). Relationships between leaf chlorophyll content and spectral reflectance and algorithms for non-destructive chlorophyll assessment in higher plant leaves. Journal of Plant Physiology 160(3), 271–282.',
  'Gitelson, A.A., Kaufman, Y.J., Merzlyak, M.N. (1996). Use of a green channel in remote sensing of global vegetation from EOS-MODIS. Remote Sensing of Environment 58(3), 289–298.',
  'Gitelson, A.A., Kaufman, Y.J., Stark, R., Rundquist, D. (2002). Novel algorithms for remote estimation of vegetation fraction. Remote Sensing of Environment 80(1), 76–87.',
  'Gitelson, A.A., Merzlyak, M.N., Chivkunova, O.B. (2001). Optical properties and nondestructive estimation of anthocyanin content in plant leaves. Photochemistry and Photobiology 74(1), 38–45.',
  'Gomez, K.A., Gomez, A.A. (1984). Statistical Procedures for Agricultural Research, 2nd edn. John Wiley & Sons, New York.',
  'Green, A.A., Berman, M., Switzer, P., Craig, M.D. (1988). A transformation for ordering multispectral data in terms of image quality with implications for noise removal. IEEE Transactions on Geoscience and Remote Sensing 26(1), 65–74.',
  'Guo, A., Huang, W., Dong, Y., Ye, H., Ma, H., Liu, B., Wu, W., Ren, Y., Ruan, C., Geng, Y. (2021). Wheat yellow rust detection using UAV-based hyperspectral technology. Remote Sensing 13(1), 123. https://doi.org/10.3390/rs13010123',
  'Guyon, I., Elisseeff, A. (2003). An introduction to variable and feature selection. Journal of Machine Learning Research 3, 1157–1182.',
  'Guyon, I., Weston, J., Barnhill, S., Vapnik, V. (2002). Gene selection for cancer classification using support vector machines. Machine Learning 46, 389–422.',
  'Haboudane, D., Miller, J.R., Pattey, E., Zarco-Tejada, P.J., Strachan, I.B. (2004). Hyperspectral vegetation indices and novel algorithms for predicting green LAI of crop canopies: modeling and validation in the context of precision agriculture. Remote Sensing of Environment 90(3), 337–352.',
  'Haboudane, D., Miller, J.R., Tremblay, N., Zarco-Tejada, P.J., Dextraze, L. (2002). Integrated narrow-band vegetation indices for prediction of crop chlorophyll content for application to precision agriculture. Remote Sensing of Environment 81(2–3), 416–426.',
  'Haralick, R.M., Shanmugam, K., Dinstein, I. (1973). Textural features for image classification. IEEE Transactions on Systems, Man, and Cybernetics SMC-3(6), 610–621.',
  'He, K., Zhang, X., Ren, S., Sun, J. (2015). Delving deep into rectifiers: surpassing human-level performance on ImageNet classification. Proceedings of the IEEE International Conference on Computer Vision, 1026–1034.',
  'Hochreiter, S., Schmidhuber, J. (1997). Long short-term memory. Neural Computation 9(8), 1735–1780.',
  'Hoerl, A.E., Kennard, R.W. (1970). Ridge regression: biased estimation for nonorthogonal problems. Technometrics 12(1), 55–67.',
  'Holm, S. (1979). A simple sequentially rejective multiple test procedure. Scandinavian Journal of Statistics 6(2), 65–70.',
  'Horler, D.N.H., Dockray, M., Barber, J. (1983). The red edge of plant leaf reflectance. International Journal of Remote Sensing 4(2), 273–288.',
  'Hotelling, H. (1936). Relations between two sets of variates. Biometrika 28(3–4), 321–377.',
  'Hsu, C.-W., Chang, C.-C., Lin, C.-J. (2003). A practical guide to support vector classification. Technical report, Department of Computer Science, National Taiwan University.',
  'Huang, L., Li, T., Ding, C., Zhao, J., Zhang, D., Yang, G. (2020). Diagnosis of the severity of Fusarium head blight of wheat ears on the basis of image and spectral feature fusion. Sensors 20(10), 2887. https://doi.org/10.3390/s20102887',
  'Huberty, C.J., Olejnik, S. (2006). Applied MANOVA and Discriminant Analysis, 2nd edn. Wiley, Hoboken, NJ.',
  'Huete, A.R. (1988). A soil-adjusted vegetation index (SAVI). Remote Sensing of Environment 25(3), 295–309.',
  'Hughes, G.F. (1968). On the mean accuracy of statistical pattern recognizers. IEEE Transactions on Information Theory 14(1), 55–63.',
  'Idso, S.B., Jackson, R.D., Pinter, P.J., Reginato, R.J., Hatfield, J.L. (1981). Normalizing the stress-degree-day parameter for environmental variability. Agricultural Meteorology 24, 45–55.',
  'Ioffe, S., Szegedy, C. (2015). Batch normalization: accelerating deep network training by reducing internal covariate shift. Proceedings of the 32nd International Conference on Machine Learning, PMLR 37, 448–456.',
  'Jackson, R.D., Idso, S.B., Reginato, R.J., Pinter, P.J. (1981). Canopy temperature as a crop water stress indicator. Water Resources Research 17(4), 1133–1138.',
  'Jacquemoud, S., Verhoef, W., Baret, F., Bacour, C., Zarco-Tejada, P.J., Asner, G.P., François, C., Ustin, S.L. (2009). PROSPECT + SAIL models: a review of use for vegetation characterization. Remote Sensing of Environment 113, S56–S66.',
  'Jolliffe, I.T. (2002). Principal Component Analysis, 2nd edn. Springer, New York.',
  'Jones, H.G. (2014). Plants and Microclimate: A Quantitative Approach to Environmental Plant Physiology, 3rd edn. Cambridge University Press, Cambridge.',
  'Jordan, C.F. (1969). Derivation of leaf-area index from quality of light on the forest floor. Ecology 50(4), 663–666.',
  'Keshava, N., Mustard, J.F. (2002). Spectral unmixing. IEEE Signal Processing Magazine 19(1), 44–57.',
  'Kingma, D.P., Ba, J. (2015). Adam: a method for stochastic optimization. 3rd International Conference on Learning Representations (ICLR). arXiv:1412.6980.',
  'Kohavi, R. (1995). A study of cross-validation and bootstrap for accuracy estimation and model selection. Proceedings of the 14th International Joint Conference on Artificial Intelligence, 1137–1145.',
  'Kokaly, R.F., Clark, R.N. (1999). Spectroscopic determination of leaf biochemistry using band-depth analysis of absorption features and stepwise multiple linear regression. Remote Sensing of Environment 67(3), 267–287.',
  'Kononenko, I. (1994). Estimating attributes: analysis and extensions of RELIEF. Proceedings of the European Conference on Machine Learning (ECML-94), LNCS 784, 171–182.',
  'Krishna, G., Sahoo, R.N., Pargal, S., Gupta, V.K., Sinha, P., Bhagat, S., Saharan, M.S., Singh, R., Chattopadhyay, C. (2014). Assessing wheat yellow rust disease through hyperspectral remote sensing. International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences XL-8, 1413–1416. https://doi.org/10.5194/isprsarchives-XL-8-1413-2014',
  'Kruskal, W.H., Wallis, W.A. (1952). Use of ranks in one-criterion variance analysis. Journal of the American Statistical Association 47(260), 583–621.',
  'Kursa, M.B., Rudnicki, W.R. (2010). Feature selection with the Boruta package. Journal of Statistical Software 36(11), 1–13.',
  'Kutner, M.H., Nachtsheim, C.J., Neter, J., Li, W. (2005). Applied Linear Statistical Models, 5th ed. McGraw-Hill/Irwin, New York.',
  'Landis, J.R., Koch, G.G. (1977). The measurement of observer agreement for categorical data. Biometrics 33(1), 159–174.',
  'Levene, H. (1960). Robust tests for equality of variances. In: Olkin, I. (Ed.), Contributions to Probability and Statistics. Stanford University Press, 278–292.',
  'Li, H., Liang, Y., Xu, Q., Cao, D. (2009). Key wavelengths screening using competitive adaptive reweighted sampling method for multivariate calibration. Analytica Chimica Acta 648(1), 77–84.',
  'Lin, L.I.-K. (1989). A concordance correlation coefficient to evaluate reproducibility. Biometrics 45(1), 255–268.',
  'Liu, F.T., Ting, K.M., Zhou, Z.-H. (2008). Isolation forest. Proceedings of the 8th IEEE International Conference on Data Mining, 413–422.',
  'Liu, Y., Liu, G., Sun, H., An, L., Zhao, R., Liu, M., Tang, W., Li, M., Yan, X., Ma, Y., Zhao, F. (2024). Exploring multi-features in UAV based optical and thermal infrared images to estimate disease severity of wheat powdery mildew. Computers and Electronics in Agriculture 225, 109285. https://doi.org/10.1016/j.compag.2024.109285',
  'Lundberg, S.M., Lee, S.-I. (2017). A unified approach to interpreting model predictions. Advances in Neural Information Processing Systems 30, 4765–4774.',
  'Lv, Z., Meng, R., Chen, G., Zhao, F., Xu, B., Zhao, Y., Huang, Z., Zhou, L., Zeng, L., Yan, J. (2023). Combining multiple spectral enhancement features for improving spectroscopic asymptomatic detection and symptomatic severity classification of southern corn leaf blight. Precision Agriculture 24, 1593–1618. https://doi.org/10.1007/s11119-023-10010-2',
  'MacQueen, J. (1967). Some methods for classification and analysis of multivariate observations. Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability 1, 281–297.',
  'Mahlein, A.-K. (2016). Plant disease detection by imaging sensors – parallels and specific demands for precision agriculture and plant phenotyping. Plant Disease 100(2), 241–251.',
  'Mahlein, A.-K., Alisaac, E., Al Masri, A., Behmann, J., Dehne, H.-W., Oerke, E.-C. (2019). Comparison and combination of thermal, fluorescence, and hyperspectral imaging for monitoring Fusarium head blight of wheat on spikelet scale. Sensors 19(10), 2281. https://doi.org/10.3390/s19102281',
  'Mahlein, A.-K., Rumpf, T., Welke, P., Dehne, H.-W., Plümer, L., Steiner, U., Oerke, E.-C. (2013). Development of spectral indices for detecting and identifying plant diseases. Remote Sensing of Environment 128, 21–30. https://doi.org/10.1016/j.rse.2012.09.019',
  'Maimaitijiang, M., Sagan, V., Sidike, P., Hartling, S., Esposito, F., Fritschi, F.B. (2020). Soybean yield prediction from UAV using multimodal data fusion and deep learning. Remote Sensing of Environment 237, 111599. https://doi.org/10.1016/j.rse.2019.111599',
  'Mandal, N., Adak, S., Das, D.K., Sahoo, R.N., Mukherjee, J., Kumar, A., Chinnusamy, V., Das, B., Mukhopadhyay, A., Rajashekara, H., Gakhar, S. (2023). Spectral characterization and severity assessment of rice blast disease using univariate and multivariate models. Frontiers in Plant Science 14, 1067189. https://doi.org/10.3389/fpls.2023.1067189',
  'Mandal, N., Das, D.K., Sahoo, R.N., Adak, S., Kumar, A., Viswanathan, C., Mukherjee, J., Rajashekara, H., Ranjan, R., Das, B. (2022). Assessing rice blast disease severity through hyperspectral remote sensing. Journal of Agrometeorology 24(3), 241–248.',
  'Mann, H.B., Whitney, D.R. (1947). On a test of whether one of two random variables is stochastically larger than the other. Annals of Mathematical Statistics 18(1), 50–60.',
  'McCullagh, P. (1980). Regression models for ordinal data. Journal of the Royal Statistical Society B 42(2), 109–142.',
  'Meinshausen, N. (2006). Quantile regression forests. Journal of Machine Learning Research 7, 983–999.',
  'Meng, R., Lv, Z., Yan, J., Chen, G., Zhao, F., Zeng, L., Xu, B. (2020). Development of spectral disease indices for southern corn rust detection and severity classification. Remote Sensing 12(19), 3233. https://doi.org/10.3390/rs12193233',
  'Merton, R., Huntington, J. (1999). Early simulation results of the ARIES-1 satellite sensor for multi-temporal vegetation research derived from AVIRIS. Proceedings of the 8th JPL Airborne Earth Science Workshop, Pasadena.',
  'Merzlyak, M.N., Gitelson, A.A., Chivkunova, O.B., Rakitin, V.Y. (1999). Non-destructive optical detection of pigment changes during leaf senescence and fruit ripening. Physiologia Plantarum 106(1), 135–141.',
  'Metternicht, G. (2003). Vegetation indices derived from high-resolution airborne videography for precision crop management. International Journal of Remote Sensing 24(14), 2855–2877.',
  'Mohammed, G.H., Colombo, R., Middleton, E.M., Rascher, U., van der Tol, C., Nedbal, L., Goulas, Y., Pérez-Priego, O., Damm, A., Meroni, M., et al. (2019). Remote sensing of solar-induced chlorophyll fluorescence (SIF) in vegetation: 50 years of progress. Remote Sensing of Environment 231, 111177.',
  'Mustafa, G., Zheng, H., Li, W., Yin, Y., Wang, Y., Zhou, M., Liu, P., Bilal, M., Jia, H., Li, G., Cheng, T., Tian, Y., Cao, W., Zhu, Y., Yao, X. (2023). Fusarium head blight monitoring in wheat ears using machine learning and multimodal data from asymptomatic to symptomatic periods. Frontiers in Plant Science 13, 1102341. https://doi.org/10.3389/fpls.2022.1102341',
  'Nadeau, C., Bengio, Y. (2003). Inference for the generalization error. Machine Learning 52, 239–281.',
  'Nguyen, C., Sagan, V., Skobalski, J., Severo, J.I. (2023). Early detection of wheat yellow rust disease and its impact on terminal yield with multi-spectral UAV-imagery. Remote Sensing 15(13), 3301. https://doi.org/10.3390/rs15133301',
  'Ojala, T., Pietikäinen, M., Mäenpää, T. (2002). Multiresolution gray-scale and rotation invariant texture classification with local binary patterns. IEEE Transactions on Pattern Analysis and Machine Intelligence 24(7), 971–987.',
  'Oliver, M.A., Webster, R. (1990). Kriging: a method of interpolation for geographical information systems. International Journal of Geographical Information Systems 4(3), 313–332.',
  'Otsu, N. (1979). A threshold selection method from gray-level histograms. IEEE Transactions on Systems, Man, and Cybernetics 9(1), 62–66.',
  'Pedregosa, F., et al. (2011). Scikit-learn: machine learning in Python. Journal of Machine Learning Research 12, 2825–2830.',
  'Peng, H., Long, F., Ding, C. (2005). Feature selection based on mutual information: criteria of max-dependency, max-relevance, and min-redundancy. IEEE Transactions on Pattern Analysis and Machine Intelligence 27(8), 1226–1238.',
  'Peñuelas, J., Baret, F., Filella, I. (1995). Semi-empirical indices to assess carotenoids/chlorophyll a ratio from leaf spectral reflectance. Photosynthetica 31(2), 221–230.',
  'Peñuelas, J., Gamon, J.A., Fredeen, A.L., Merino, J., Field, C.B. (1994). Reflectance indices associated with physiological changes in nitrogen- and water-limited sunflower leaves. Remote Sensing of Environment 48(2), 135–146.',
  'Peñuelas, J., Piñol, J., Ogaya, R., Filella, I. (1997). Estimation of plant water concentration by the reflectance Water Index WI (R900/R970). International Journal of Remote Sensing 18(13), 2869–2875.',
  'Platt, J.C. (1999). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. In: Smola, A.J., et al. (Eds.), Advances in Large Margin Classifiers. MIT Press, 61–74.',
  'Prechelt, L. (1998). Early stopping — but when? In: Orr, G.B., Müller, K.-R. (Eds.), Neural Networks: Tricks of the Trade. LNCS 1524, Springer, 55–69.',
  'Probst, P., Wright, M.N., Boulesteix, A.-L. (2019). Hyperparameters and tuning strategies for random forest. WIREs Data Mining and Knowledge Discovery 9(3), e1301.',
  'Pudil, P., Novovičová, J., Kittler, J. (1994). Floating search methods in feature selection. Pattern Recognition Letters 15(11), 1119–1125.',
  'Ramachandram, D., Taylor, G.W. (2017). Deep multimodal learning: a survey on recent advances and trends. IEEE Signal Processing Magazine 34(6), 96–108.',
  'Ramalingam, S., Sahoo, R.N., Kumar, A., Ranjan, R., Chinnasamy, V. (2026). Early detection of rice blast disease using hyperspectral remote sensing. Plant Science Today 13(1), 1–10. https://doi.org/10.14719/pst.11111',
  'Raschka, S. (2018). MLxtend: providing machine learning and data science utilities and extensions to Python\'s scientific computing stack. Journal of Open Source Software 3(24), 638.',
  'Rasmussen, C.E., Williams, C.K.I. (2006). Gaussian Processes for Machine Learning. MIT Press, Cambridge, MA.',
  'Raun, W.R., Solie, J.B., Johnson, G.V., Stone, M.L., Lukina, E.V., Thomason, W.E., Schepers, J.S. (2001). In-season prediction of potential grain yield in winter wheat using canopy reflectance. Agronomy Journal 93(1), 131–138.',
  'Richards, J.A. (2013). Remote Sensing Digital Image Analysis: An Introduction, 5th ed. Springer, Berlin.',
  'Roberts, D.R., et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. Ecography 40(8), 913–929.',
  'Robnik-Šikonja, M., Kononenko, I. (2003). Theoretical and empirical analysis of ReliefF and RReliefF. Machine Learning 53(1–2), 23–69.',
  'Rondeaux, G., Steven, M., Baret, F. (1996). Optimization of soil-adjusted vegetation indices. Remote Sensing of Environment 55(2), 95–107.',
  'Roujean, J.-L., Bréon, F.-M. (1995). Estimating PAR absorbed by vegetation from bidirectional reflectance measurements. Remote Sensing of Environment 51(3), 375–384.',
  'Rouse, J.W., Haas, R.H., Schell, J.A., Deering, D.W. (1974). Monitoring vegetation systems in the Great Plains with ERTS. Third ERTS Symposium, NASA SP-351, Vol. 1, 309–317.',
  'Rumelhart, D.E., Hinton, G.E., Williams, R.J. (1986). Learning representations by back-propagating errors. Nature 323, 533–536.',
  'Saharan, G.S., Verma, P.R., Meena, P.D., Kumar, A. (2014). White Rust of Crucifers: Biology, Ecology and Management. Springer India, New Delhi.',
  'Savitzky, A., Golay, M.J.E. (1964). Smoothing and differentiation of data by simplified least squares procedures. Analytical Chemistry 36(8), 1627–1639.',
  'Schaepman-Strub, G., Schaepman, M.E., Painter, T.H., Dangel, S., Martonchik, J.V. (2006). Reflectance quantities in optical remote sensing – definitions and case studies. Remote Sensing of Environment 103(1), 27–42.',
  'Schmidt, K.S., Skidmore, A.K. (2003). Spectral discrimination of vegetation types in a coastal wetland. Remote Sensing of Environment 85(1), 92–108.',
  'Shaner, G., Finney, R.E. (1977). The effect of nitrogen fertilization on the expression of slow-mildewing resistance in Knox wheat. Phytopathology 67, 1051–1056.',
  'Shapiro, S.S., Wilk, M.B. (1965). An analysis of variance test for normality (complete samples). Biometrika 52(3–4), 591–611.',
  'Shukla, K.K., Nigam, R., Birah, A., Kanojia, A.K., Kumar, A., Bhattacharya, B.K., Chander, S. (2024). Detection of aphid-infested mustard crop using ground spectroscopy. Remote Sensing 16(1), 47. https://doi.org/10.3390/rs16010047',
  'Smith, G.M., Milton, E.J. (1999). The use of the empirical line method to calibrate remotely sensed data to reflectance. International Journal of Remote Sensing 20(13), 2653–2662.',
  'Smola, A.J., Schölkopf, B. (2004). A tutorial on support vector regression. Statistics and Computing 14(3), 199–222.',
  'Snoek, J., Larochelle, H., Adams, R.P. (2012). Practical Bayesian optimization of machine learning algorithms. Advances in Neural Information Processing Systems 25, 2951–2959.',
  'Sokolova, M., Lapalme, G. (2009). A systematic analysis of performance measures for classification tasks. Information Processing and Management 45(4), 427–437.',
  'Spearman, C. (1904). The proof and measurement of association between two things. American Journal of Psychology 15(1), 72–101.',
  'Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., Salakhutdinov, R. (2014). Dropout: a simple way to prevent neural networks from overfitting. Journal of Machine Learning Research 15, 1929–1958.',
  'Strobl, C., Boulesteix, A.-L., Zeileis, A., Hothorn, T. (2007). Bias in random forest variable importance measures: illustrations, sources and a solution. BMC Bioinformatics 8, 25.',
  'Terentev, A., Badenko, V., Shaydayuk, E., Emelyanov, D., Eremenko, D., Klabukov, D., Fedotov, A., Dolzhenko, V. (2023). Hyperspectral remote sensing for early detection of wheat leaf rust caused by Puccinia triticina. Agriculture 13(6), 1186. https://doi.org/10.3390/agriculture13061186',
  'Thenkabail, P.S., Enclona, E.A., Ashton, M.S., Van Der Meer, B. (2004). Accuracy assessments of hyperspectral waveband performance for vegetation analysis applications. Remote Sensing of Environment 91(3–4), 354–376.',
  'Tian, L., Xue, B., Wang, Z., Li, D., Yao, X., Cao, Q., Zhu, Y., Cao, W., Cheng, T. (2021). Spectroscopic detection of rice leaf blast infection from asymptomatic to mild stages with integrated machine learning and feature selection. Remote Sensing of Environment 257, 112350. https://doi.org/10.1016/j.rse.2021.112350',
  'Tibshirani, R. (1996). Regression shrinkage and selection via the lasso. Journal of the Royal Statistical Society B 58(1), 267–288.',
  'Tsai, F., Philpot, W. (1998). Derivative analysis of hyperspectral data. Remote Sensing of Environment 66(1), 41–51.',
  'Tuia, D., Persello, C., Bruzzone, L. (2016). Domain adaptation for the classification of remote sensing data: an overview of recent advances. IEEE Geoscience and Remote Sensing Magazine 4(2), 41–57.',
  'Tukey, J.W. (1949). Comparing individual means in the analysis of variance. Biometrics 5(2), 99–114.',
  'Varma, S., Simon, R. (2006). Bias in error estimation when using cross-validation for model selection. BMC Bioinformatics 7, 91.',
  'Vermote, E.F., Tanré, D., Deuzé, J.L., Herman, M., Morcrette, J.-J. (1997). Second Simulation of the Satellite Signal in the Solar Spectrum, 6S: an overview. IEEE Transactions on Geoscience and Remote Sensing 35(3), 675–686.',
  'Welch, B.L. (1947). The generalization of \'Student\'s\' problem when several different population variances are involved. Biometrika 34(1–2), 28–35.',
  'West, J.S., Bravo, C., Oberti, R., Lemaire, D., Moshou, D., McCartney, H.A. (2003). The potential of optical canopy measurement for targeted control of field crop diseases. Annual Review of Phytopathology 41, 593–614.',
  'Woebbecke, D.M., Meyer, G.E., Von Bargen, K., Mortensen, D.A. (1995). Color indices for weed identification under various soil, residue, and lighting conditions. Transactions of the ASAE 38(1), 259–269.',
  'Wold, S., Sjöström, M., Eriksson, L. (2001). PLS-regression: a basic tool of chemometrics. Chemometrics and Intelligent Laboratory Systems 58(2), 109–130.',
  'Wolpert, D.H. (1992). Stacked generalization. Neural Networks 5(2), 241–259.',
  'Youden, W.J. (1950). Index for rating diagnostic tests. Cancer 3(1), 32–35.',
  'Zhang, J., Pu, R., Huang, W., Yuan, L., Luo, J., Wang, J. (2012b). Using in-situ hyperspectral data for detecting and discriminating yellow rust disease from nutrient stresses. Field Crops Research 134, 165–174.',
  'Zhang, J.-C., Pu, R.-L., Wang, J.-H., Huang, W.-J., Yuan, L., Luo, J.-H. (2012a). Detecting powdery mildew of winter wheat using leaf level hyperspectral measurements. Computers and Electronics in Agriculture 85, 13–23.',
  'Zhang, X., Vinatzer, B.A., Li, S. (2024). Hyperspectral imaging analysis for early detection of tomato bacterial leaf spot disease. Scientific Reports 14, 27666. https://doi.org/10.1038/s41598-024-78650-6',
  'Zhu, H., Chu, B., Zhang, C., Liu, F., Jiang, L., He, Y. (2017). Hyperspectral imaging for presymptomatic detection of tobacco disease with successive projections algorithm and machine-learning classifiers. Scientific Reports 7, 4125. https://doi.org/10.1038/s41598-017-04501-2',
  'Zou, H., Hastie, T. (2005). Regularization and variable selection via the elastic net. Journal of the Royal Statistical Society B 67(2), 301–320.',
  'Zuur, A.F., Ieno, E.N., Walker, N.J., Saveliev, A.A., Smith, G.M. (2009). Mixed Effects Models and Extensions in Ecology with R. Springer, New York.',
].forEach(r => K.push(refPara(r)));


const numcfg = r => ({ reference: r, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] });
const doc = new Document({
  features: { updateFields: true }, creator: 'Animesh Panda', title: 'AI-based multimodal UAV sensing of white rust in mustard: complete methodology',
  styles: { default: { document: { run: { font: FONT, size: 22 } }, heading1: hs(30, '1E3A1F', 320, 140, false, 0), heading2: hs(25, '2C5F2D', 220, 100, false, 1), heading3: hs(23, '2C5F2D', 180, 80, true, 2) } },
  numbering: { config: [
    { reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
                                 { level: 1, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1080, hanging: 360 } } } }] },
    numcfg('num')] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1300, bottom: 1300, left: 1300, right: 1300 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18 })] })] }) },
    children: K }] });
const chk = (u, o, n) => { if (JSON.stringify(u) !== JSON.stringify(o)) { console.error(n + ' order mismatch', u, o); process.exit(1); } };
chk(usedF, FORDER, 'figure'); chk(usedT, TORDER, 'table');
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('saved', OUT, 'figs', FORDER.length, 'tabs', TORDER.length, 'eqs', 54, 'refs', 177); });
