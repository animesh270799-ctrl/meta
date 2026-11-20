const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType, ImageRun,
  TableOfContents, PageBreak, LevelFormat, Footer, PageNumber, BorderStyle } = require('docx');
const B = '/home/user/meta/thesis_build/method2/';
const OUT = '/home/user/meta/thesis_build/method2/../outputs/White_rust_field_methodology_reconstructed.docx';
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
    children: [new Paragraph({ keepNext: true, children: runs(String(c), { size, bold: head }).map(x => { if (head) x.root && 0; return x; }) })] })) });
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
const FORDER = ['overall', 'dataset', 'preproc', 'features', 'validation', 'selection', 'combinations', 'dl', 'obj3', 'gantt'];
const TORDER = ['abbr', 'objectives', 'literature', 'td1', 'td2', 'td3', 'td4', 'dataset', 'tp1', 'tp2', 'tp3', 'tp4', 'tp5', 'tp6', 'tp7', 'tp8', 'presensor', 'tf1', 'tf2', 'tf3', 'tf4', 'featcount', 'hsidx', 'msidx', 'rgbfeat', 'tirfeat', 'schema', 'tv1', 'tv2', 'ts1', 'ts2', 'ts3', 'ts4', 'ts5', 'leak', 'foldsize', 'o1steps', 'to11', 'to12', 'to13', 'to14', 'to15', 'to16', 'to17', 'sets', 'to21', 'to22', 'to23', 'mlgrid', 'models', 'to24', 'to25', 'to26', 'to27', 'to28', 'templateA', 'templateB', 'to31', 'to32', 'to33', 'to34', 'to35', 'fulfil', 'chain', 'plan', 'software'];
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


K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1200, after: 200 }, children: [new TextRun({ text: 'AI-based multimodal UAV sensing of white rust in mustard', font: FONT, size: 44, bold: true, color: '1E3A1F' })] }));
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [new TextRun({ text: 'Reconstructed research methodology for the field experiment: Objectives 1, 2 and 3, step by step', font: FONT, size: 28, color: '2C5F2D' })] }));
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: 'Hyperspectral, multispectral, RGB and thermal UAV data | 15 sensor sets | feature-level fusion with machine learning and deep learning', font: FONT, size: 22, italics: true })] }));
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 700 }, children: [new TextRun({ text: 'Animesh Panda (Roll No. 13098) | Ph.D. Agricultural Physics | ICAR-Indian Agricultural Research Institute, New Delhi', font: FONT, size: 20 })] }));
K.push(BOX(`How to read this document.`, `Each chapter is one block of the work and the blocks are used in the order of the chapters: field data (Chapter 2) → pre-processing (Chapter 3) → feature extraction (Chapter 4) → validation framework (Chapter 5) → Objective 1 (Chapter 6) → Objective 2 (Chapter 7) → Objective 3 (Chapter 8). Every step uses the same template: the problem it solves, its input, what is done, why this method was chosen, which published studies used the same step, details for each sensor, and the output that goes to the next step. Methods are kept as simple as the objectives allow, statistics are limited to what is needed, and every method carries its reference.`, 'EEF3E8', '2C5F2D'));
K.push(BOX(`Design decisions fixed for the whole study.`, `(1) Field experiment only (IARI, rabi 2025-26); the glasshouse study is not used here. (2) The modelling unit is the subplot-date; each subplot has its own canopy severity score. (3) All four sensors are brought to the hyperspectral grid and measured on the same vegetation pixels (soil, grass and shadow removed; leaves and flowers kept). (4) Fusion is feature-level only, with both machine learning and deep learning. (5) Both classification and regression are done. (6) Every step that uses the severity labels runs inside the training folds of a plot-grouped cross-validation.`, 'FFF6E0', 'C98A00'));
K.push(new Paragraph({ children: [new PageBreak()] }));
K.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: 'Contents', font: FONT, size: 32, bold: true, color: '1E3A1F' })] }));
K.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-3' }));
K.push(new Paragraph({ children: [new PageBreak()] }));
K.push(H1(`Abbreviations`));
K.push(...tab2('abbr', [[`Abbreviation`, `Meaning`, `Abbreviation`, `Meaning`],
[`AUC`, `area under the ROC curve`, `MNF`, `minimum noise fraction`],
[`CT, CTD`, `canopy temperature; CT minus air temperature`, `mRMR`, `minimum redundancy maximum relevance`],
[`CWSI`, `crop water stress index`, `MS`, `multispectral`],
[`DAI`, `days after inoculation`, `NDSI`, `normalised difference spectral index`],
[`DL, ML`, `deep learning; machine learning`, `NRCT`, `normalised relative canopy temperature`],
[`DNN-F1, DNN-F2`, `deep neural network with input- and intermediate-level feature fusion`, `OFC`, `optimum feature combination`],
[`DSF`, `disease-specific feature`, `PLS-DA, PLSR`, `partial least squares discriminant analysis; regression`],
[`FD, SD`, `first and second derivative of reflectance`, `PPI`, `pixel purity index`],
[`GLCM`, `grey-level co-occurrence matrix (texture)`, `R`, `reflectance`],
[`HS`, `hyperspectral`, `REP`, `red-edge position`],
[`k-NN`, `k-nearest neighbours`, `RF, RFR`, `random forest classification; regression`],
[`LORO`, `leave-one-replication-out`, `RGB`, `red–green–blue camera`],
[`RMSE`, `root-mean-square error`, `RPD`, `ratio of performance to deviation`],
[`SAM`, `spectral angle mapper`, `SE`, `squeeze-and-excitation attention`],
[`SFFS`, `sequential floating forward selection`, `SHAP`, `Shapley additive explanations`],
[`SVM, SVR`, `support vector machine; regression`, `TIR`, `thermal infrared`],
[`VI`, `vegetation index`, `VIF`, `variance inflation factor`],
[`WRI`, `White Rust Index`, `XGBoost`, `extreme gradient boosting`]], [1500, 3150, 1500, 3156], `Abbreviations used in this document.`, 16));
K.push(H1(`1. Objectives and overall design`));
K.push(P(`White rust, caused by the obligate oomycete Albugo candida, produces white pustules on leaves, chlorosis and, after systemic infection, distorted inflorescences (staghead) in Indian mustard, and can reduce yield by 20–60% (Kumar and Kalha, 2005; Saharan et al., 2014). The disease develops under cool, humid weather (Chattopadhyay et al., 2011). Visual scoring is slow and possible only after symptoms appear. Unmanned aerial vehicle (UAV) sensors record the pigment, structure, water and temperature changes that accompany infection, sometimes before symptoms are visible (Mahlein, 2016; Terentev et al., 2022), and combining sensors usually improves accuracy (Maimaitijiang et al., 2020; Feng et al., 2022).`));
K.push(...tab2('objectives', [[`Objective (ORW wording)`, `Question answered in this methodology`, `Data used`, `Main output`],
[`1. To characterise white rust of mustard through multimodal sensing from UAV platform`, `Which bands, indices, textures and thermal features of each sensor respond to white rust severity, and how does the response differ with variety and inoculation timing?`, `1536 post-symptomatic subplot samples per sensor`, `Disease-specific feature (DSF) pools of each sensor; White Rust Index; response curves`],
[`2. To detect and discriminate disease severity of white rust in mustard through AI based multimodal data fusion`, `How accurately can healthy vs diseased subplots, severity classes and the severity score be predicted by each of the 15 sensor sets with machine learning and deep learning?`, `1536 post-symptomatic subplot samples per sensor`, `Best sensor set and model for each task; contribution of each sensor; severity maps`],
[`3. To predict white rust at pre-symptomatic stage using machine learning technique(s)`, `Can subplots that will develop white rust be separated from healthy subplots before symptoms, and can their later severity be predicted?`, `576 pre-symptomatic subplot samples per sensor`, `Pre-symptomatic models; earliest detection day; risk maps`]], [2700, 3000, 1700, 1906], `Objectives, questions, data and outputs.`, 16));
K.push(...fig2('overall', 'f1_overall.png', `Overall workflow of the field methodology. Each block is one chapter of this document; outputs of one block are the inputs of the next.`, 560));
K.push(P(`**Five rules apply to every chapter.** They come from the methodological literature on hyperspectral and multi-sensor modelling and from the weaknesses identified in recent disease-sensing studies (Ambroise and McLachlan, 2002; Varma and Simon, 2006; Roberts et al., 2017; Ma et al., 2026).`));
K.push(NL(`One sample = one subplot on one date. The four subplots of a plot are never split between training and test data.`));
K.push(NL(`All sensors are measured on the same vegetation pixels of each subplot (Chapter 3).`));
K.push(NL(`Feature groups are built with physical meaning and thinned group by group before they are pooled (Chapter 4 and Stage 1–3 of the selection).`));
K.push(NL(`Every step that uses the severity labels (relevance screening, index search, final selection, tuning) runs inside the training folds only.`));
K.push(NL(`The same folds are used for all 15 sensor sets and all models, so their accuracies are directly comparable.`));
K.push(H2(`Published studies on which the methodology is built`));
K.push(P(`Every step of this methodology was chosen because it has been used and tested for crop-disease sensing or for the specific data problem it solves. Table ${T('literature')} lists the main disease studies and the steps they support; the methodological references (validation, selection, models) are given in each step.`));
K.push(...tab2('literature', [[`Study`, `Crop and disease`, `Sensors and data`, `What it showed`, `Steps supported`],
[`Mahlein et al. (2013)`, `sugar beet; Cercospora, rust, powdery mildew`, `leaf hyperspectral`, `ReliefF bands combined into disease-specific indices`, `O1-3, O1-4`],
[`Huang et al. (2014)`, `wheat; powdery mildew, yellow rust`, `leaf and canopy hyperspectral`, `ReliefF bands; new optimised indices transferred to canopy`, `O1-3, O1-4`],
[`Shukla et al. (2024)`, `mustard; aphid stress`, `ground hyperspectral`, `correlation scalogram to find sensitive regions`, `O1-3, Stage 2`],
[`Tian et al. (2021)`, `rice; leaf blast`, `spectra 350–2500 nm`, `disease-specific features, VIF → SFFS, asymptomatic stage`, `Stage 1, 3, 4; O3-1`],
[`Mustafa et al. (2023)`, `wheat; Fusarium head blight`, `fluorescence + hyperspectral`, `Boruta and ML-SFFS; k-NN and SVM`, `O1-6, Stage 4`],
[`Feng et al. (2022)`, `wheat; powdery mildew`, `hyperspectral + thermal + RGB`, `feature-level fusion of indices, thermal and texture; PLSR, SVR, RFR`, `F3, F4, fusion, O2-3`],
[`Liu et al. (2024)`, `wheat; powdery mildew`, `UAV multispectral + thermal`, `red-edge indices and thermal features; RF; maps`, `F2, F4, O2-7`],
[`Guo et al. (2021)`, `wheat; yellow rust`, `UAV hyperspectral`, `vegetation indices + texture; common resolution; masks`, `P5, P6, F3`],
[`Maimaitijiang et al. (2020)`, `soybean yield`, `UAV RGB + multispectral + thermal`, `DNN with input- and intermediate-level fusion`, `O2-4`],
[`Ma et al. (2026)`, `rice; blast`, `UAV hyperspectral`, `group-wise selection, texture index, SE attention, ablation`, `Stage 2, O2-4, O2-6`],
[`Abdulridha et al. (2023)`, `wheat; stem rust`, `UAV hyperspectral, 960 plots`, `RF for severity classes and binary detection`, `O2-1, O2-3`],
[`Mahlein et al. (2019)`, `wheat; Fusarium head blight`, `hyperspectral + thermal + fluorescence`, `sensor comparison and earliest detection day`, `O1-7, O3-5`],
[`Zhu et al. (2017)`, `tobacco; mosaic virus`, `hyperspectral imaging`, `pre-symptomatic detection with retrospective labels`, `O3-1, O3-4`],
[`Zarco-Tejada et al. (2018)`, `olive; Xylella fastidiosa`, `airborne hyperspectral + thermal`, `pre-visual detection and maps`, `O3-2, O3-5`],
[`Yu et al. (2025)`, `rice; sheath blight`, `spectra + physiology`, `dual-branch fusion at the pre-symptomatic stage`, `O3-4`],
[`Oerke et al. (2006)`, `cucumber; downy mildew`, `thermal imaging`, `temperature changes with disease and with environment`, `F4, O3-2`],
[`Deng et al. (2024)`, `wheat; stripe rust`, `UAV multimodal`, `deep fusion for disease-index maps`, `O2-7`]], [1750, 1700, 1750, 2500, 1606], `Main disease studies and the steps of this methodology they support.`, 15));
K.push(H1(`2. Field experiment and dataset`));
K.push(H3(`D1  Experimental design and treatments`));
K.push(...tab2('td1', [[`Item`, `Description`],
[`Problem solved`, `Defines the sources of variation (inoculation timing, variety, replication) so that disease effects can be separated from crop-stage and variety effects.`],
[`Input`, `IARI research farm, rabi 2025-26; factorial randomised block design.`],
[`Output → next step`, `48 plots with known treatment, replication and plot number → subplots (D3) and validation folds (Chapter 5).`]], [1900, 7406], `Step D1 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Four sowing dates at 10-day intervals (D1–D4: 20 Nov, 30 Nov, 10 Dec, 20 Dec 2025) with a single inoculation on 10 January 2026, so the crop was inoculated at about 50, 40, 30 and 20 days after sowing.`));
K.push(NL(`Three varieties of different susceptibility (V1 Varuna, highly susceptible; V2 Pusa Vijay, moderately susceptible; V3 PM 38, resistant, as in the ORW).`));
K.push(NL(`The 12 treatments (4 × 3) were inoculated in three replications (R1–R3) with a zoosporangial suspension of 1.5 × 10⁵ zoosporangia mL⁻¹ (Mishra et al., 2009), and one uninoculated healthy plot per treatment was kept: 36 inoculated + 12 healthy = 48 plots.`));
K.push(NL(`Each plot carries a code (treatment, replication, plot number) that is stored with every sample.`));
K.push(P(`**Why this method.** A factorial design with staggered sowing produces a range of crop ages and severities on the same flight dates, which is necessary to learn severity rather than date. Healthy plots of every treatment give a same-stage, same-variety reference for each date, which is used for normalisation in Objective 3.`));
K.push(P(`**Studies that used the same step.** Staggered sowing or inoculation timing to create severity gradients and healthy controls has been used for wheat yellow rust (Guo et al., 2021), wheat powdery mildew (Feng et al., 2022; Liu et al., 2024) and rice blast (Tian et al., 2021; Ma et al., 2026). The ORW design follows Mishra et al. (2009) for the inoculum.`));
K.push(NOTE(`Varieties and dates are taken from the ORW; correct them in Table D1 if the field sheets differ.`));
K.push(H3(`D2  UAV flights and sensors`));
K.push(...tab2('td2', [[`Item`, `Description`],
[`Problem solved`, `Provides co-located, same-day images from four sensors that record different plant responses.`],
[`Input`, `Eight post-symptomatic flight dates and the pre-symptomatic flight dates; flights 11:00–14:00 h under clear sky and low wind, 30 m above ground, 85% front and 80% side overlap, calibration panels and RTK ground control points on every date.`],
[`Output → next step`, `Raw images of four sensors for every date → pre-processing (Chapter 3).`]], [1900, 7406], `Step D2 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Hyperspectral: Headwall Co-Aligned VNIR–SWIR imager (613 raw bands; 483 bands after quality control, 399–2398 nm; processed pixel ≈ 2.2 cm).`));
K.push(NL(`Multispectral: MicaSense RedEdge-MX (475, 560, 668, 717, 840 nm; ≈ 2 cm at 30 m).`));
K.push(NL(`RGB: DJI Phantom camera (≈ 0.8 cm at 30 m).`));
K.push(NL(`Thermal: FLIR Vue Pro R, 7.5–13.5 µm (≈ 3.9 cm at 30 m with the 13 mm lens).`));
K.push(NL(`Ground scoring is done on the same day as the flight, or within one day.`));
K.push(P(`**Why this method.** Each sensor measures a different response to infection: hyperspectral bands track pigment, structure and water in detail; multispectral bands track the red edge with a cheaper sensor; RGB records colour and canopy texture; thermal records stomatal and transpiration changes (Mahlein, 2016). A fixed solar window and panels make dates comparable.`));
K.push(P(`**Studies that used the same step.** The same four sensor types were combined for wheat powdery mildew (Feng et al., 2022) and soybean yield (Maimaitijiang et al., 2020); UAV hyperspectral imaging was used for wheat stem rust (Abdulridha et al., 2023) and rice blast (Ma et al., 2026); the same-day pairing of scoring and flight follows Ma et al. (2026).`));
K.push(H3(`D3  Subplots and the canopy severity score`));
K.push(...tab2('td3', [[`Item`, `Description`],
[`Problem solved`, `Turns each plot into four independently scored sampling units and gives each a label.`],
[`Input`, `Plot boundaries and the canopy severity score recorded for each of the four subplots on every date.`],
[`Output → next step`, `Labelled subplot list (date, plot, subplot, treatment, replication, score) → labels (D4) and subplot extraction (P7–P8).`]], [1900, 7406], `Step D3 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Each plot is divided into four quadrant subplots of equal size; border rows are excluded by an inner buffer.`));
K.push(NL(`One trained scorer records the canopy-level disease severity of each subplot with written grade limits (Bock et al., 2010), using the 0–9 grade key of Conn et al. (1990): 0 = no symptoms, 1 = 1–5%, 3 = 6–10%, 5 = 11–25%, 7 = 26–50%, 9 = > 50% of canopy leaf area with pustules; staghead is noted after flowering.`));
K.push(NL(`The score is entered with the subplot code so that it can be joined to the image features.`));
K.push(P(`**Why this method.** Scoring each subplot gives four labelled samples per plot instead of one and captures within-plot variability. The canopy score matches what the UAV sees (the canopy, including inflorescences), which is why flowers are kept in the subplot spectrum.`));
K.push(P(`**Studies that used the same step.** Grade keys of this kind were used for canopy severity in UAV studies of wheat stem rust (Abdulridha et al., 2023), powdery mildew (Liu et al., 2024) and rice blast, where five canopy levels were defined from a disease index (Ma et al., 2026); the Conn et al. (1990) key is the standard key for Brassica foliar diseases.`));
K.push(H3(`D4  Labels for the three tasks and the two datasets`));
K.push(...tab2('td4', [[`Item`, `Description`],
[`Problem solved`, `Defines exactly what each model predicts and which samples belong to which objective.`],
[`Input`, `Subplot scores of all dates; date of the first visible pustule in the field.`],
[`Output → next step`, `Post-symptomatic dataset (1536 samples per sensor) and pre-symptomatic dataset (576 samples per sensor), each with its labels → all later chapters.`]], [1900, 7406], `Step D4 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Post-symptomatic dates = dates on or after the first visible pustule; pre-symptomatic dates = earlier dates.`));
K.push(NL(`Binary label: healthy (score 0) vs diseased (score > 0), from the observed score (an inoculated subplot that shows no pustules is labelled healthy).`));
K.push(NL(`Severity classes: the six grades 0, 1, 3, 5, 7, 9; if a grade has fewer than 5% of samples, it is merged with its neighbour (for example 7 + 9).`));
K.push(NL(`Regression target: the canopy severity score of the subplot (treated as continuous).`));
K.push(NL(`Pre-symptomatic labels (Objective 3): healthy = subplots of healthy plots; infected = inoculated subplots that show pustules on a later date; inoculated subplots that never develop symptoms (mainly the resistant variety) are kept out of the infected class. Regression target = the severity score of the same subplot on the first post-symptomatic date.`));
K.push(P(`**Why this method.** Labels from the observed score (not from the treatment) avoid calling a symptomless inoculated subplot diseased. Retrospective labelling is the only way to know which pre-symptomatic samples were really infected. Regression is kept alongside classes because classes are cuts of a continuous severity and neighbouring classes overlap.`));
K.push(P(`**Studies that used the same step.** Binary plus multi-class plus regression tasks were analysed together for rice blast (Tian et al., 2021) and wheat powdery mildew (Feng et al., 2022); retrospective pre-symptomatic labels were used by Zhu et al. (2017) and Tian et al. (2021); class overlap of neighbouring severity levels is reported by Ma et al. (2026), where the middle level was hardest for every model.`));
K.push(...tab2('dataset', [[`Item`, `Value`],
[`Plots × subplots`, `48 × 4 = 192 subplots per image`],
[`Sensors`, `4 (hyperspectral, multispectral, RGB, thermal)`],
[`Post-symptomatic samples per sensor`, `1536 (8 dates × 192)`],
[`Pre-symptomatic samples per sensor`, `576`],
[`Sensor sets analysed`, `15 (4 single, 6 pairs, 4 triples, 1 all four)`],
[`Tasks`, `binary detection, severity classes, severity regression (Objectives 2 and 3)`]], [3600, 5706], `Dataset used in this methodology (numbers as recorded by the researcher).`, 17));
K.push(...fig2('dataset', 'f2_dataset.png', `Structure of the dataset: flight dates → sensors → plots → scored subplots, and the two datasets used by the objectives.`, 520));
K.push(H1(`3. Pre-processing (applied to every date and sensor)`));
K.push(P(`Pre-processing turns raw images into one table per date and sensor, with one row per subplot. It is identical for all objectives. Its central idea is that every sensor is aligned to the hyperspectral grid and measured on the same vegetation pixels.`));
K.push(...fig2('preproc', 'f3_preproc.png', `Pre-processing steps P1–P8 with the output of each step.`, 540));
K.push(H3(`P1  Radiometric calibration`));
K.push(...tab2('tp1', [[`Item`, `Description`],
[`Problem solved`, `Raw digital numbers depend on illumination and sensor settings and cannot be compared between dates.`],
[`Input`, `Raw images, calibration-panel images, sunlight-sensor records, air temperature and humidity of each flight.`],
[`Output → next step`, `Reflectance images (hyperspectral, multispectral), consistent RGB images and temperature images → P2.`]], [1900, 7406], `Step P1 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Hyperspectral and multispectral: convert digital numbers to reflectance with the reflectance panels imaged before and after each flight (empirical line), using the sunlight sensor for illumination changes during the flight.`));
K.push(NL(`RGB: fixed exposure and white balance on all dates; values kept as digital numbers for colour indices and texture.`));
K.push(NL(`Thermal: radiometric conversion to temperature with emissivity 0.98 and the air temperature, humidity and flight height of each flight.`));
K.push(P(`**Why this method.** The empirical line method is the standard way to obtain surface reflectance from airborne images with ground panels, and emissivity and atmospheric corrections are needed for absolute canopy temperature.`));
K.push(P(`**Studies that used the same step.** Empirical line: Smith and Milton (1999); panel calibration for UAV hyperspectral disease studies: Guo et al. (2021), Ma et al. (2026); thermal conversion for crop canopies: Jones et al. (2009), Liu et al. (2024).`));
K.push(H3(`P2  Orthomosaics and georeferencing`));
K.push(...tab2('tp2', [[`Item`, `Description`],
[`Problem solved`, `Individual frames must be joined into one map per sensor and date with correct ground coordinates.`],
[`Input`, `Calibrated frames and RTK ground control points.`],
[`Output → next step`, `Georeferenced orthomosaics (RGB, multispectral, thermal) and georectified hyperspectral cubes → P3 and P4.`]], [1900, 7406], `Step P2 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Build orthomosaics by structure-from-motion for the frame cameras; georectify the push-broom hyperspectral lines with the IMU/GNSS data.`));
K.push(NL(`Use the same RTK ground control points on every date so that all dates share one coordinate frame.`));
K.push(P(`**Why this method.** Accurate georeferencing is the precondition for co-registration and for extracting the same subplots on every date.`));
K.push(P(`**Studies that used the same step.** Guo et al. (2021) and Ma et al. (2026) produced georeferenced UAV hyperspectral mosaics before sampling; Maimaitijiang et al. (2020) and Feng et al. (2022) mosaicked RGB, multispectral and thermal images before feature extraction.`));
K.push(H3(`P3  Hyperspectral cube quality control`));
K.push(...tab2('tp3', [[`Item`, `Description`],
[`Problem solved`, `Water-vapour absorption, detector edges and noise make some bands unusable, and smoothing across gaps creates artefacts.`],
[`Input`, `Georectified 613-band cube of each date.`],
[`Output → next step`, `Clean 483-band reflectance cube on a 2.2 cm grid → P4.`]], [1900, 7406], `Step P3 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Keep VNIR up to 919.7 nm and SWIR from 921.4 nm; remove the water-vapour regions 1335–1460 and 1785–1965 nm and the noisy ends (900–915 nm and > 2400 nm), giving 483 bands.`));
K.push(NL(`Drop the three isolated bands at 916–920 nm (detector edge).`));
K.push(NL(`Apply Savitzky–Golay smoothing (window 5, second-order polynomial) separately to each continuous band segment (399–899, 921–1329, 1461–1779, 1971–2398 nm), never across a gap.`));
K.push(NL(`Check that reflectance is on a 0–1 scale.`));
K.push(P(`**Why this method.** Atmospheric water vapour makes 1350–1450 and 1800–1950 nm unreliable for UAV data. Savitzky–Golay smoothing reduces noise while keeping absorption features and is required before derivatives, but a window that crosses a band gap mixes distant wavelengths.`));
K.push(P(`**Studies that used the same step.** Removal of water-vapour bands: Thenkabail et al. (2004); Savitzky–Golay smoothing: Savitzky and Golay (1964), used before derivatives by Tsai and Philpot (1998) and in disease studies by Tian et al. (2021) and Mustafa et al. (2023); spectral pre-processing review: Rinnan et al. (2009).`));
K.push(H3(`P4  Projection and co-registration to the hyperspectral image`));
K.push(...tab2('tp4', [[`Item`, `Description`],
[`Problem solved`, `Images of different sensors do not overlap exactly; small shifts mix canopy and soil values at edges.`],
[`Input`, `Georeferenced images of all sensors for one date.`],
[`Output → next step`, `All images in WGS 84 / UTM 43N and aligned to the hyperspectral image → P5.`]], [1900, 7406], `Step P4 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Project every image to WGS 84 / UTM zone 43N so that distances are in metres.`));
K.push(NL(`Register RGB, multispectral and thermal images to the hyperspectral image with tie points (plot corners, markers) and a first- or second-order polynomial transformation.`));
K.push(NL(`Accept the registration when the root-mean-square error of independent check points is below one hyperspectral pixel (2.2 cm).`));
K.push(P(`**Why this method.** The hyperspectral image is the reference because the vegetation mask is made from it. Misregistration of even a fraction of a pixel causes large errors when images are compared pixel by pixel.`));
K.push(P(`**Studies that used the same step.** Image registration methods: Zitová and Flusser (2003); effect of misregistration: Dai and Khorram (1998); polynomial warping: Richards (2013); co-registered multi-sensor UAV layers: Maimaitijiang et al. (2020), Feng et al. (2022).`));
K.push(H3(`P5  Resampling to the hyperspectral grid`));
K.push(...tab2('tp5', [[`Item`, `Description`],
[`Problem solved`, `Sensors have different pixel sizes (≈ 0.8, 2, 2.2 and 3.9 cm); one grid is needed so that pixel (row, column) is the same ground point in every layer.`],
[`Input`, `Co-registered images.`],
[`Output → next step`, `All layers on the 2.2 cm hyperspectral grid → P6 and P8.`]], [1900, 7406], `Step P5 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`RGB (finer): pixel aggregate (area mean), so each new pixel is the mean of the RGB pixels it covers.`));
K.push(NL(`Multispectral (similar size): bilinear interpolation.`));
K.push(NL(`Thermal (coarser): nearest neighbour, which keeps the measured temperatures.`));
K.push(NL(`RGB texture features are computed before resampling, at native resolution and inside the same mask (P8), because resampling removes fine texture.`));
K.push(P(`**Why this method.** Area averaging avoids aliasing when moving to a coarser grid; nearest neighbour preserves original values when moving to a finer grid; snapping all layers to one grid allows one mask and one set of subplot polygons for all sensors.`));
K.push(P(`**Studies that used the same step.** Resampling methods: Richards (2013); nearest-neighbour resampling of UAV layers to a common resolution: Guo et al. (2021); common-grid stacking of RGB, multispectral and thermal data: Maimaitijiang et al. (2020).`));
K.push(H3(`P6  Vegetation mask from the hyperspectral image`));
K.push(...tab2('tp6', [[`Item`, `Description`],
[`Problem solved`, `Soil, grass/weeds and shadow inside a plot change reflectance, texture and temperature and must be removed before disease features are extracted.`],
[`Input`, `Clean hyperspectral cube; training regions of soil, shadow, grass, mustard canopy and flowers.`],
[`Output → next step`, `Binary mask (1 = mustard canopy, stressed canopy, flowers; 0 = soil, grass, shadow) on the hyperspectral grid → applied to all sensors in P8.`]], [1900, 7406], `Step P6 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Build one endmember library for the whole field with the hourglass workflow: minimum noise fraction (MNF), pixel purity index (PPI) on the MNF bands and n-dimensional cluster selection; build it once from pixels sampled on all dates.`));
K.push(NL(`Classify every pixel with the spectral angle mapper (SAM); calibrate the angle threshold on labelled pixels.`));
K.push(NL(`Keep green canopy, stressed (chlorotic) canopy and flower classes; remove soil, grass and shadow. Because yellow petals have low NDVI, the vegetation rule is NDVI > 0.6 OR flower class.`));
K.push(NL(`Apply a one-pixel morphological erosion to remove mixed edge pixels.`));
K.push(NL(`Check the mask on independent reference pixels from RGB (overall accuracy and kappa).`));
K.push(P(`**Why this method.** The hyperspectral image separates soil, shadow, weeds, green leaves and yellow flowers far better than three or five broad bands. A field-wide endmember library gives the same classes in every plot and on every date (unlike per-plot endmember extraction). Flowers are kept because the canopy score includes the inflorescence (staghead).`));
K.push(P(`**Studies that used the same step.** MNF: Green et al. (1988); PPI and n-D endmembers: Boardman et al. (1995); SAM: Kruse et al. (1993); NDVI: Rouse et al. (1974); flowers in Brassica canopies: Sulik and Long (2016); erosion: Soille (2003); accuracy assessment: Congalton (1991); soil and background removal before disease features: Guo et al. (2021), Feng et al. (2022).`));
K.push(P(`**Spectral angle used by SAM** (Kruse et al., 1993), between a pixel spectrum t and an endmember spectrum r over n bands; smaller angles mean more similar spectra:`));
K.push(EQ(`α = cos^{−1} [ Σ_{i} t_{i} r_{i} / ( √(Σ_{i} t_{i}^{2}) √(Σ_{i} r_{i}^{2}) ) ]`));
K.push(H3(`P7  Plot and subplot polygons`));
K.push(...tab2('tp7', [[`Item`, `Description`],
[`Problem solved`, `Each sample must cover exactly the scored subplot and nothing else.`],
[`Input`, `Field layout, plot numbers, aligned images.`],
[`Output → next step`, `192 subplot polygons with codes → P8.`]], [1900, 7406], `Step P7 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Digitise the 48 plot polygons once on the reference date and add the plot number.`));
K.push(NL(`Split each plot into four quadrant subplots that match the field scoring; apply an inner buffer to exclude border rows and bunds.`));
K.push(NL(`Use the same polygons on all dates and all sensors.`));
K.push(P(`**Why this method.** Fixed polygons ensure that the same ground area is followed over time and across sensors, and the inner buffer removes edge effects and grass on bunds.`));
K.push(P(`**Studies that used the same step.** Plot-level polygons after soil masking were used by Liu et al. (2024) and Feng et al. (2022); Ma et al. (2026) used fixed small regions at flagged spots, which is the same principle at a smaller scale.`));
K.push(H3(`P8  Subplot values`));
K.push(...tab2('tp8', [[`Item`, `Description`],
[`Problem solved`, `Models need one value per feature and subplot; thermal values change with weather from date to date.`],
[`Input`, `Masked, resampled layers of all sensors; subplot polygons; air temperature of each flight.`],
[`Output → next step`, `One table per date and sensor (192 rows): mean reflectance per band, RGB texture, thermal statistics, pixel count, flower % and canopy cover % → feature extraction (Chapter 4).`]], [1900, 7406], `Step P8 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Multiply each layer by the vegetation mask and compute the mean of the masked pixels in each subplot for every band; save the pixel count.`));
K.push(NL(`Compute RGB texture at native resolution within the mask, then aggregate per subplot.`));
K.push(NL(`Thermal: save the canopy temperature statistics and normalise them by air temperature and by the healthy plots of the same date and variety.`));
K.push(NL(`Save flower % and canopy cover % from the SAM classes as covariates.`));
K.push(P(`**Why this method.** The subplot mean of vegetation pixels is the spectrum that corresponds to the canopy score. Normalising thermal data removes the date and weather effect that would otherwise dominate canopy temperature.`));
K.push(P(`**Studies that used the same step.** Plot-mean spectra after masking: Guo et al. (2021), Mustafa et al. (2023); thermal normalisation by air temperature and healthy references: Oerke et al. (2006), Jones et al. (2009), Elsayed et al. (2017).`));
K.push(H2(`Pre-processing of each sensor at a glance`));
K.push(...tab2('presensor', [[`Step`, `Hyperspectral`, `Multispectral`, `RGB`, `Thermal`],
[`P1 Calibration`, `panels → reflectance`, `panels + sunlight sensor → reflectance`, `fixed exposure; digital numbers`, `emissivity 0.98, air T, RH → °C`],
[`P2 Mosaic`, `georectified push-broom cube`, `orthomosaic`, `orthomosaic`, `orthomosaic`],
[`P3 Quality`, `613 → 483 bands; segment-wise smoothing`, `band alignment check`, `—`, `warm-up and drift check`],
[`P4 Registration`, `reference image`, `to HS, RMSE < 1 pixel`, `to HS, RMSE < 1 pixel`, `to HS with markers`],
[`P5 Resampling`, `reference grid (2.2 cm)`, `bilinear`, `pixel aggregate; texture before resampling`, `nearest neighbour`],
[`P6 Mask`, `made here (hourglass + SAM)`, `HS mask applied`, `HS mask applied`, `HS mask + extra edge check`],
[`P7 Polygons`, `192 subplots`, `same`, `same`, `same`],
[`P8 Values`, `mean per band`, `mean per band`, `colour means, texture`, `statistics, normalised temperatures`]], [1700, 2000, 1900, 1900, 1806], `Pre-processing applied to each sensor.`, 15));
K.push(H1(`4. Feature extraction (all sensors)`));
K.push(P(`Features are calculated for every subplot-date and grouped by type. Grouping matters: selection is later done group by group so that small groups (thermal, texture) are not swamped by hundreds of spectral bands (Ghamisi et al., 2019).`));
K.push(...fig2('features', 'f4_features.png', `Feature groups of each sensor and the covariates that are recorded but not used as disease features.`, 540));
K.push(H3(`F1  Hyperspectral features`));
K.push(...tab2('tf1', [[`Item`, `Description`],
[`Problem solved`, `Raw reflectance alone does not show red-edge shifts and absorption features clearly.`],
[`Input`, `Subplot mean reflectance (483 bands) of each date.`],
[`Output → next step`, `Hyperspectral feature groups → Objective 1 and the selection stages.`]], [1900, 7406], `Step F1 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Reflectance (R) of the 483 bands.`));
K.push(NL(`First (FD) and second (SD) derivatives from the Savitzky–Golay fit of each segment; derivative bands within 10 nm of a gap are not used.`));
K.push(NL(`Red-edge parameters: red-edge position (REP), amplitude (Dr) and the second-derivative amplitude.`));
K.push(NL(`48 vegetation indices in five groups: pigment (e.g. PRI, ARI, CARI, MCARI, TCARI/OSAVI, PSRI), structure (e.g. NDVI, OSAVI, MSR), red edge (NDRE, MTCI, CIrededge), water (NDWI, MSI, NDII) and disease indices (DWSI, RBI); each formula is checked against the original paper.`));
K.push(NL(`The White Rust Index and two-band normalised-difference indices are searched in Objective 1 and inside the training folds (Chapter 6, step O1-4).`));
K.push(P(`**Why this method.** Derivatives remove the additive background and sharpen absorption features; red-edge parameters summarise chlorophyll loss; published indices encode known physiology and are easier to transfer to other sensors.`));
K.push(P(`**Studies that used the same step.** Derivative analysis: Tsai and Philpot (1998); red edge: Horler et al. (1983), Filella and Peñuelas (1994); pigment indices: Gamon et al. (1992), Gitelson et al. (2003), Merzlyak et al. (1999), Haboudane et al. (2002); water and disease indices: Gao (1996), Hunt and Rock (1989), Hardisky et al. (1983), Apan et al. (2004); index groups for disease detection: Mahlein et al. (2013), Huang et al. (2014), Ma et al. (2026).`));
K.push(H3(`F2  Multispectral features`));
K.push(...tab2('tf2', [[`Item`, `Description`],
[`Problem solved`, `Five broad bands carry less information than the hyperspectral cube but are cheaper and closer to satellite bands.`],
[`Input`, `Subplot means of the five MicaSense bands.`],
[`Output → next step`, `Multispectral feature groups → selection.`]], [1900, 7406], `Step F2 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Five band reflectances (475, 560, 668, 717, 840 nm).`));
K.push(NL(`Twelve vegetation indices: NDVI, GNDVI, NDRE, CIgreen, CIrededge, MTCI, OSAVI, TCARI/OSAVI, MSR, PSRI, SAVI and the red-edge ratio.`));
K.push(NL(`All ten two-band normalised differences of the five bands.`));
K.push(NL(`GLCM texture (eight statistics) of each band, computed within the mask.`));
K.push(P(`**Why this method.** Red-edge and chlorophyll indices from multispectral cameras track chlorophyll loss and were the most consistent powdery-mildew indicators; texture adds canopy heterogeneity caused by pustules and chlorotic patches.`));
K.push(P(`**Studies that used the same step.** Gitelson et al. (1996, 2003); Dash and Curran (2004); Rondeaux et al. (1996); Haboudane et al. (2002); Merzlyak et al. (1999); multispectral indices and texture for wheat powdery mildew: Liu et al. (2024); texture: Haralick et al. (1973).`));
K.push(H3(`F3  RGB features`));
K.push(...tab2('tf3', [[`Item`, `Description`],
[`Problem solved`, `RGB images carry colour and fine texture but no near-infrared information.`],
[`Input`, `RGB orthomosaic at native resolution with the vegetation mask.`],
[`Output → next step`, `RGB feature groups → selection.`]], [1900, 7406], `Step F3 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Colour indices: excess green (ExG), excess red (ExR), ExG − ExR, VARI, GLI and NGRDI; mean hue, saturation and value.`));
K.push(NL(`GLCM texture of R, G and B (mean, variance, homogeneity, contrast, dissimilarity, entropy, second moment, correlation), four directions averaged, computed at native resolution.`));
K.push(NL(`Canopy cover (fraction of vegetation pixels) as a covariate.`));
K.push(P(`**Why this method.** White pustules and chlorosis change canopy colour and make the canopy surface rougher, which texture measures capture; texture features were as strongly related to severity as the best vegetation indices in rice blast and wheat powdery mildew.`));
K.push(P(`**Studies that used the same step.** Woebbecke et al. (1995); Meyer and Neto (2008); Gitelson et al. (2002); Louhaichi et al. (2001); Tucker (1979); Haralick et al. (1973); RGB texture in disease fusion: Feng et al. (2022), Guo et al. (2021), Ma et al. (2026).`));
K.push(H3(`F4  Thermal features`));
K.push(...tab2('tf4', [[`Item`, `Description`],
[`Problem solved`, `Infection changes transpiration and canopy temperature, but temperature also changes with weather and time.`],
[`Input`, `Masked thermal subplot values, air temperature and the healthy-plot temperatures of the same date.`],
[`Output → next step`, `Thermal feature group → selection.`]], [1900, 7406], `Step F4 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Canopy temperature (CT): mean, median, standard deviation, 10th and 90th percentiles.`));
K.push(NL(`Canopy minus air temperature (CTD = CT − Tair) and the ratio CTR = CT / Tair (in kelvin).`));
K.push(NL(`Normalised relative canopy temperature NRCT = (CT − CTmin) / (CTmax − CTmin) over the field on that date.`));
K.push(NL(`Difference from healthy plots of the same date and variety (ΔT).`));
K.push(NL(`Crop water stress index (CWSI) with wet and dry references from the field, and GLCM texture of the temperature image.`));
K.push(P(`**Why this method.** Normalised temperatures remove most of the weather effect and are the thermal parameters most often linked to disease severity; ΔT to healthy plots of the same variety removes variety and stage effects.`));
K.push(P(`**Studies that used the same step.** Idso et al. (1981); Jones et al. (2009); Elsayed et al. (2017); thermal parameters for wheat powdery mildew: Feng et al. (2022), Liu et al. (2024); leaf temperature and environmental effects in downy mildew: Oerke et al. (2006).`));
K.push(...tab2('featcount', [[`Sensor`, `Feature groups`, `Approximate number`],
[`Hyperspectral`, `R, FD, SD, red edge, 48 indices (+ searched indices)`, `≈ 1500`],
[`Multispectral`, `5 bands, 12 indices, 10 NDSI, 40 texture`, `≈ 67`],
[`RGB`, `colour indices, HSV, 24 texture`, `≈ 33`],
[`Thermal`, `temperature statistics, normalised temperatures, CWSI, texture`, `≈ 18`],
[`Covariates`, `flower %, canopy cover %, days after inoculation, variety, inoculation timing`, `not disease features`]], [2000, 5000, 2306], `Feature groups and their approximate sizes before selection.`, 17));
K.push(NOTE(`Why the groups are not simply pooled: about 1600 candidate features against about 1000 training samples per fold would make selection unstable (Hughes, 1968; Guyon and Elisseeff, 2003), many features would be near-duplicates (Dormann et al., 2013), and random-forest importance and ReliefF both favour large groups of correlated features (Strobl et al., 2007; Robnik-Šikonja and Kononenko, 2003). The staged selection in Chapter 5 (staged feature selection) avoids these problems.`));
K.push(H2(`Index and feature definitions`));
K.push(P(`The tables below define every index and feature used. Formulas were checked against the original papers; R_{λ} is the reflectance at λ nm (the nearest available band is used).`));
K.push(...tab2('hsidx', [[`Group`, `Index`, `Formula`, `Reference`],
[`Group`, `Index`, `Formula`, `Reference`],
[`Chlorophyll / greenness`, `NDVI780`, `(R_{780} − R_{670})/(R_{780} + R_{670})`, `Raun et al. 2001`],
[``, `NDVI850`, `(R_{850} − R_{650})/(R_{850} + R_{650})`, `Raun et al. 2001`],
[``, `NDVI761`, `(R_{761} − R_{651})/(R_{761} + R_{651})`, `Raun et al. 2001`],
[``, `SR900; SR850; SR761`, `R_{900}/R_{680};  R_{850}/R_{680};  R_{761}/R_{651}`, `Jordan 1969`],
[``, `GNDVI`, `(R_{850} − R_{550})/(R_{850} + R_{550})`, `Gitelson et al. 1996`],
[``, `RDVI`, `(R_{800} − R_{670})/√(R_{800} + R_{670})`, `Roujean and Bréon 1995`],
[``, `MSR`, `(R_{800}/R_{670} − 1)/√(R_{800}/R_{670} + 1)`, `Chen 1996; Guo 2021`],
[``, `TVI`, `0.5[120(R_{750} − R_{550}) − 200(R_{670} − R_{550})]`, `Broge and Leblanc 2001`],
[``, `MTVI1`, `1.2[1.2(R_{800} − R_{550}) − 2.5(R_{670} − R_{550})]`, `Haboudane et al. 2004`],
[``, `MTVI2`, `1.5[1.2(R_{800} − R_{550}) − 2.5(R_{670} − R_{550})] / √[(2R_{800} + 1)^{2} − (6R_{800} − 5√R_{670}) − 0.5]`, `Haboudane et al. 2004`],
[``, `MCARI1`, `1.2[2.5(R_{800} − R_{670}) − 1.3(R_{800} − R_{550})]`, `Haboudane et al. 2004`],
[``, `TCARI`, `3[(R_{700} − R_{670}) − 0.2(R_{700} − R_{550})(R_{700}/R_{670})]`, `Haboudane et al. 2002`],
[``, `VIgreen`, `(R_{550} − R_{670})/(R_{550} + R_{670})`, `Gitelson et al. 2002`],
[``, `GI`, `R_{554}/R_{677}`, `Guo et al. 2021`],
[``, `RR`, `1/R_{700}`, `Mustafa et al. 2023`],
[`Pigment ratios`, `PSSRa; PSSRb; PSSRc`, `R_{800}/R_{680};  R_{800}/R_{635};  R_{800}/R_{470}`, `Blackburn 1998; Mahlein 2019`],
[``, `RARSa; RARSb; RARSc`, `R_{675}/R_{700};  R_{675}/(R_{700} × R_{650});  R_{760}/R_{500}`, `Chappelle et al. 1992`],
[``, `SIPI`, `(R_{800} − R_{445})/(R_{800} − R_{680})`, `Peñuelas et al. 1995`],
[``, `NPCI`, `(R_{680} − R_{430})/(R_{680} + R_{430})`, `Peñuelas et al. 1994`],
[``, `PSRI`, `(R_{680} − R_{500})/R_{750}`, `Merzlyak et al. 1999`],
[``, `ARI`, `1/R_{550} − 1/R_{700}`, `Gitelson et al. 2001`],
[``, `PPR`, `(R_{550} − R_{450})/(R_{550} + R_{450})`, `Metternicht 2003`],
[``, `NRI`, `(R_{570} − R_{670})/(R_{570} + R_{670})`, `Bausch and Duke 1996`],
[`Photosynthesis / stress`, `PRI`, `(R_{531} − R_{570})/(R_{531} + R_{570})`, `Gamon et al. 1992`],
[``, `NPQI`, `(R_{415} − R_{435})/(R_{415} + R_{435})`, `Barnes et al. 1992`],
[``, `RVSI`, `(R_{712} + R_{752})/2 − R_{732}`, `Merton and Huntington 1999`],
[``, `HI (healthy index)`, `(R_{534} − R_{698})/(R_{534} + R_{698}) − 0.5 R_{704}`, `Mahlein et al. 2013`],
[`Water`, `WI`, `R_{900}/R_{970}`, `Peñuelas et al. 1997`],
[``, `WI/NDVI`, `(R_{900}/R_{970}) / NDVI`, `Peñuelas et al. 1997`],
[``, `NWI-2`, `(R_{970} − R_{850})/(R_{970} + R_{850})`, `Babar et al. 2006`],
[`SWIR disease–water (mustard)`, `DWSI-1`, `R_{800}/R_{1660}`, `Apan et al. 2004; Bhattacharya and Chattopadhyay 2013`],
[``, `DWSI-4`, `R_{550}/R_{680}`, `Apan et al. 2004; Bhattacharya and Chattopadhyay 2013`],
[``, `ROTI`, `R_{1175}/(R_{1982} + R_{691})`, `Bhattacharya and Chattopadhyay 2013`],
[`SWIR disease–water`, `DWSI-2; DWSI-3`, `R_{1660}/R_{550};  R_{1660}/R_{680}`, `Apan et al. 2004`],
[``, `DWSI-5`, `(R_{800} + R_{550})/(R_{1660} + R_{680})`, `Apan et al. 2004`],
[``, `NDWI`, `(R_{860} − R_{1240})/(R_{860} + R_{1240})`, `Gao 1996`],
[``, `MSI`, `R_{1600}/R_{820}`, `Hunt and Rock 1989`],
[``, `NDII`, `(R_{819} − R_{1649})/(R_{819} + R_{1649})`, `Hardisky et al. 1983`],
[``, `RBI; NDBI`, `R_{1148}/R_{1301};  (R_{1148} − R_{1301})/(R_{1148} + R_{1301})`, `Mandal et al. 2023`],
[``, `RBI_{R}`, `(R_{1068} − R_{1560})/(R_{1068} + R_{1560})`, `Ramalingam et al. 2026`],
[`Disease-specific`, `WRI`, `ND(λ_{1}, λ_{2}) + w R_{λ3}, searched in step O1-4`, `Mahlein et al. 2013 (method)`]], [1600, 1700, 4206, 1800], `Hyperspectral indices (39 base indices, 9 SWIR disease and water indices and the White Rust Index).`, 15));
K.push(...tab2('msidx', [[`Feature`, `Formula (B, G, R, RE, NIR = 475, 560, 668, 717, 840 nm)`, `Reference`],
[`Band reflectance (5)`, `subplot mean reflectance of B, G, R, RE, NIR`, `Liu et al. 2024`],
[`NDVI`, `(NIR − R)/(NIR + R)`, `Rouse et al. 1974`],
[`GNDVI`, `(NIR − G)/(NIR + G)`, `Gitelson et al. 1996`],
[`NDRE`, `(NIR − RE)/(NIR + RE)`, `Gitelson and Merzlyak 1994`],
[`CI_{green}`, `NIR/G − 1`, `Gitelson et al. 2003`],
[`CI_{rededge}`, `NIR/RE − 1`, `Gitelson et al. 2003`],
[`MTCI`, `(NIR − RE)/(RE − R)`, `Dash and Curran 2004`],
[`OSAVI`, `1.16(NIR − R)/(NIR + R + 0.16)`, `Rondeaux et al. 1996`],
[`SAVI`, `1.5(NIR − R)/(NIR + R + 0.5)`, `Huete 1988`],
[`TCARI`, `3[(RE − R) − 0.2(RE − G)(RE/R)]`, `Haboudane et al. 2002`],
[`MCARI`, `[(RE − R) − 0.2(RE − G)](RE/R)`, `Daughtry et al. 2000`],
[`MSR`, `(NIR/R − 1)/√(NIR/R + 1)`, `Chen 1996`],
[`PSRI_{MS}`, `(R − G)/NIR`, `Merzlyak et al. 1999`],
[`NDSI (10)`, `(B_{i} − B_{j})/(B_{i} + B_{j}) for all band pairs`, `Ma et al. 2026 (search)`],
[`Texture (40)`, `8 GLCM measures (Table ${T('rgbfeat')}) of each of the 5 bands`, `Haralick et al. 1973; Liu et al. 2024`]], [2000, 4900, 2406], `Multispectral features.`, 15));
K.push(...tab2('rgbfeat', [[`Feature`, `Equation`, `Reference`],
[`Chromatic coordinates`, `r = R/(R+G+B), g = G/(R+G+B), b = B/(R+G+B)`, `Woebbecke et al. 1995`],
[`ExG`, `2g − r − b`, `Woebbecke et al. 1995`],
[`ExR`, `1.4r − g`, `Meyer and Neto 2008`],
[`ExG − ExR`, `ExG − ExR`, `Meyer and Neto 2008`],
[`VARI`, `(G − R)/(G + R − B)`, `Gitelson et al. 2002`],
[`GLI`, `(2G − R − B)/(2G + R + B)`, `Louhaichi et al. 2001`],
[`NGRDI`, `(G − R)/(G + R)`, `Tucker 1979`],
[`HSV (3)`, `mean hue, saturation and value of vegetation pixels`, `—`],
[`Mean, MEA`, `Σ_{i} Σ_{j} i P(i, j)`, `Haralick et al. 1973`],
[`Variance, VAR`, `Σ_{i} Σ_{j} (i − μ)^{2} P(i, j)`, `Haralick et al. 1973`],
[`Homogeneity, HOM`, `Σ_{i} Σ_{j} P(i, j) / [1 + (i − j)^{2}]`, `Haralick et al. 1973`],
[`Contrast, CON`, `Σ_{i} Σ_{j} (i − j)^{2} P(i, j)`, `Haralick et al. 1973`],
[`Dissimilarity, DIS`, `Σ_{i} Σ_{j} |i − j| P(i, j)`, `Haralick et al. 1973`],
[`Entropy, ENT`, `− Σ_{i} Σ_{j} P(i, j) ln P(i, j)`, `Haralick et al. 1973`],
[`Second moment, SEC`, `Σ_{i} Σ_{j} P(i, j)^{2}`, `Haralick et al. 1973`],
[`Correlation, COR`, `Σ_{i} Σ_{j} (i − μ_{i})(j − μ_{j}) P(i, j) / (σ_{i} σ_{j})`, `Haralick et al. 1973`]], [2100, 4800, 2406], `RGB colour indices and GLCM texture measures (texture of R, G and B at native resolution: 24 features). P(i, j) is the normalised frequency of grey levels i and j in neighbouring pixels (distance 1, four directions averaged).`, 15));
K.push(...tab2('tirfeat', [[`Feature`, `Definition`, `Reference`],
[`CT statistics (5)`, `mean, median, SD, 10th and 90th percentile of vegetation-pixel temperature`, `Liu et al. 2024`],
[`CTD`, `CT − T_{air}`, `Feng et al. 2022`],
[`CTR`, `(CT + 273.15)/(T_{air} + 273.15)`, `Feng et al. 2022`],
[`NRCT`, `(CT − CT_{min})/(CT_{max} − CT_{min}) over the field on that date`, `Elsayed et al. 2017`],
[`ΔT`, `CT − mean CT of healthy plots of the same date and variety`, `Oerke et al. 2006`],
[`CWSI`, `(CT − T_{wet})/(T_{dry} − T_{wet}) with wet and dry references`, `Idso et al. 1981; Jones et al. 2009`],
[`Thermal texture (8)`, `GLCM measures of the temperature image quantised over one common range`, `Haralick et al. 1973`]], [2000, 4900, 2406], `Thermal features.`, 15));
K.push(H2(`The feature table`));
K.push(P(`All later steps read the same table layout, one table per sensor, joined by the identifier columns for fusion. Keeping one row per subplot-date and the same identifiers for all sensors makes the 15 sensor sets simple joins of these tables.`));
K.push(...tab2('schema', [[`Column block`, `Columns`, `Used for`],
[`Identifiers`, `date, DAI, plot, subplot, replication, treatment, variety, inoculation timing, fold`, `joining sensors; validation folds; treatment-wise results`],
[`Labels`, `severity score, severity class, healthy/diseased; for Objective 3: infected/healthy and later score`, `model targets`],
[`Covariates`, `flower %, canopy cover %, vegetation pixel count`, `checks of confounding; quality flags`],
[`Features`, `all features of the sensor, grouped (prefix R_, FD_, SD_, VI_, TX_, TH_)`, `selection and models`]], [1800, 4600, 2906], `Layout of the feature table of each sensor.`, 17));
K.push(H1(`5. Validation framework and feature-selection stages (common to Objectives 2 and 3)`));
K.push(H3(`V1  Sampling unit and outer validation folds`));
K.push(...tab2('tv1', [[`Item`, `Description`],
[`Problem solved`, `Subplots of one plot, and plots of one replication, are not independent; random splits would test the model on samples very similar to the training samples.`],
[`Input`, `Labelled subplot tables of all dates.`],
[`Output → next step`, `Three outer folds → all models of Objectives 2 and 3.`]], [1900, 7406], `Step V1 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Use leave-one-replication-out (LORO) folds: fold 1 tests replication R1, fold 2 tests R2, fold 3 tests R3.`));
K.push(NL(`The 12 healthy plots are divided by variety (V1 → fold 1, V2 → fold 2, V3 → fold 3) so that every test fold contains healthy samples.`));
K.push(NL(`All dates of a plot and all four subplots stay in the same fold; each test fold has about 512 post-symptomatic (or 192 pre-symptomatic) samples.`));
K.push(NL(`The same three folds are used for every sensor set, task and model.`));
K.push(P(`**Why this method.** Blocked (grouped) cross-validation gives realistic accuracy when data have spatial or hierarchical structure; testing on a whole replication is the closest available test to new plots.`));
K.push(P(`**Studies that used the same step.** Roberts et al. (2017); plot-grouped validation in disease sensing: Tian et al. (2021), Mustafa et al. (2023); the random sample split of Ma et al. (2026) is an example of the optimistic design this step avoids.`));
K.push(...fig2('validation', 'f5_validation.png', `Leave-one-replication-out outer folds and the inner cross-validation used for selection and tuning.`, 520));
K.push(H3(`V2  Nested inner cross-validation`));
K.push(...tab2('tv2', [[`Item`, `Description`],
[`Problem solved`, `Feature selection and tuning on all data, or on the test fold, give over-optimistic accuracy.`],
[`Input`, `Training part of each outer fold.`],
[`Output → next step`, `Selected features, tuned hyper-parameters and early-stopping epochs for each outer fold → model training.`]], [1900, 7406], `Step V2 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Inside the training replications, use a 3-fold cross-validation grouped by plot.`));
K.push(NL(`Run Stage 2–4 of the feature selection, the index search, hyper-parameter tuning and deep-learning early stopping inside this inner loop only.`));
K.push(NL(`Train the final model of the fold on the whole training part and predict the test replication once.`));
K.push(P(`**Why this method.** When selection is not nested, cross-validated error is optimistically biased; nested cross-validation gives an almost unbiased estimate.`));
K.push(P(`**Studies that used the same step.** Ambroise and McLachlan (2002); Varma and Simon (2006); nested ML-SFFS for rice blast: Tian et al. (2021).`));
K.push(H2(`Staged feature selection`));
K.push(P(`Selection is done in stages and group by group, and the same procedure is used for every sensor (Figure ${F('selection')}). Stages 1 and 3 do not use labels; Stages 2 and 4 use labels and therefore run inside the training folds (Ambroise and McLachlan, 2002; Varma and Simon, 2006). This is the approach recommended for multi-sensor UAV disease data, and the same group-wise logic (bands, indices and texture selected separately, then fused) was used for rice blast by Ma et al. (2026).`));
K.push(...fig2('selection', 'f6_selection.png', `Staged feature selection for one sensor inside each training fold, and the fusion step for sensor combinations.`, 540));
K.push(H3(`S1  Stage 1: redundancy within each group (no labels)`));
K.push(...tab2('ts1', [[`Item`, `Description`],
[`Problem solved`, `Neighbouring bands, derivatives and many indices are almost identical, which wastes the later selection on duplicates.`],
[`Input`, `Feature groups of one sensor (training part).`],
[`Output → next step`, `Thinned groups → Stage 2.`]], [1900, 7406], `Step S1 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Remove near-constant features.`));
K.push(NL(`Within each group, form clusters of features with |r| ≥ 0.95 and keep one representative per cluster; for bands, this is one band per correlated spectral region.`));
K.push(P(`**Why this method.** Neighbouring hyperspectral bands are almost perfectly correlated; one band per region keeps the information and makes the selection stable.`));
K.push(P(`**Studies that used the same step.** Mahlein et al. (2013) used a minimum band distance because of this correlation; one feature per common region: Tian et al. (2021); correlation clustering before selection: Dormann et al. (2013).`));
K.push(H3(`S2  Stage 2: relevance within each group (labels, training folds only)`));
K.push(...tab2('ts2', [[`Item`, `Description`],
[`Problem solved`, `Most features carry little disease information; each group needs a method suited to its nature.`],
[`Input`, `Thinned groups and training labels.`],
[`Output → next step`, `5–10 relevant features per group → Stage 3.`]], [1900, 7406], `Step S2 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Hyperspectral bands and derivatives: correlation scalogram (Pearson r with the severity score) for regression and ReliefF (severity classes, k = 10, neighbours from the same plot excluded) for classification; keep the top 5% and one band per region.`));
K.push(NL(`Vegetation indices (all sensors): Boruta with random forest (classification and regression separately).`));
K.push(NL(`Texture (MS, RGB, thermal): minimum-redundancy-maximum-relevance (mRMR), top 5–10.`));
K.push(NL(`Two-band indices and the White Rust Index: searched on the training plots only (Chapter 6, step O1-4).`));
K.push(NL(`Thermal: all thinned thermal features are kept (the group is small).`));
K.push(P(`**Why this method.** Correlation suits a continuous target; ReliefF detects features that separate overlapping classes; Boruta tests each feature against shuffled copies; mRMR balances relevance and redundancy for correlated texture features.`));
K.push(P(`**Studies that used the same step.** Correlation scalogram: Shukla et al. (2024), Cheng et al. (2010); ReliefF: Robnik-Šikonja and Kononenko (2003), used by Mahlein et al. (2013) and Huang et al. (2014); Boruta: Kursa and Rudnicki (2010), used by Mustafa et al. (2023); mRMR: Peng et al. (2005), used for texture by Ma et al. (2026).`));
K.push(H3(`S3  Stage 3: redundancy across groups (no labels)`));
K.push(...tab2('ts3', [[`Item`, `Description`],
[`Problem solved`, `Survivors of different groups can still be strongly correlated (for example a red-edge band and a red-edge index).`],
[`Input`, `Pooled Stage-2 survivors of one sensor.`],
[`Output → next step`, `Sensor disease-specific feature set (DSF set, about 10–25 features) → fusion and Stage 4.`]], [1900, 7406], `Step S3 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Pool the survivors of all groups of the sensor.`));
K.push(NL(`Remove features iteratively until every variance inflation factor (VIF) is below 10.`));
K.push(P(`**Why this method.** Collinearity makes model coefficients and importance unstable; VIF < 10 is the usual threshold.`));
K.push(P(`**Studies that used the same step.** Dormann et al. (2013); VIF < 10 before feature-combination search: Tian et al. (2021), Mustafa et al. (2023).`));
K.push(P(`**Variance inflation factor** of feature j, where R_{j}^{2} is the coefficient of determination of feature j regressed on all other features (Dormann et al., 2013):`));
K.push(EQ(`VIF_{j} = 1 / (1 − R_{j}^{2})`));
K.push(H3(`S4  Fusion of sensor sets (combinations only)`));
K.push(...tab2('ts4', [[`Item`, `Description`],
[`Problem solved`, `Combinations of sensors need one input vector per sample.`],
[`Input`, `DSF sets of the sensors in the combination.`],
[`Output → next step`, `Fused feature pool → Stage 4.`]], [1900, 7406], `Step S4 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Concatenate the DSF sets of the sensors in the combination (feature-level fusion).`));
K.push(NL(`Apply VIF < 10 again across sensors.`));
K.push(NL(`Standardise every feature with the mean and standard deviation of the training part.`));
K.push(P(`**Why this method.** Feature-level fusion keeps each sensor's features identifiable, so the contribution of each sensor can be assessed, and avoids the dimensionality of fusing raw data.`));
K.push(P(`**Studies that used the same step.** Feature-level fusion of spectral, thermal and texture features: Feng et al. (2022), Liu et al. (2024); fusion levels: Ghamisi et al. (2019); input- and intermediate-level fusion: Maimaitijiang et al. (2020).`));
K.push(H3(`S5  Stage 4: model-specific final selection`));
K.push(...tab2('ts5', [[`Item`, `Description`],
[`Problem solved`, `Different models use features differently; a small final set improves generalisation and interpretation.`],
[`Input`, `Fused pool (or the DSF set of a single sensor).`],
[`Output → next step`, `Optimum feature combination (OFC) of each machine-learning model; the whole pool for deep-learning models → model training.`]], [1900, 7406], `Step S5 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Machine learning: sequential floating forward selection (ML-SFFS) wrapped around each model, criterion macro-F1 (classification) or RMSE (regression) in the inner cross-validation; at most 15 features; keep the smallest subset within 1% of the best score.`));
K.push(NL(`Deep learning: the fused pool is used directly, because the network learns its own feature weights; the attention layer of DNN-F2 shows which sensors it relies on.`));
K.push(NL(`Record how often each feature is selected over the three folds (selection stability).`));
K.push(P(`**Why this method.** SFFS finds a small set that suits each model and can remove previously added features; limiting the number of features keeps the ratio of samples to features high.`));
K.push(P(`**Studies that used the same step.** Pudil et al. (1994); ML-SFFS for rice blast and Fusarium head blight: Tian et al. (2021), Mustafa et al. (2023); stability of selection: Nogueira et al. (2018), Meinshausen and Bühlmann (2010).`));
K.push(H2(`Leakage checklist and fold sizes`));
K.push(...tab2('leak', [[`Step`, `Uses labels?`, `Where it is run`],
[`Pre-processing, mask, feature extraction`, `no`, `once, on all data`],
[`Stage 1 (correlation clusters)`, `no`, `training part of each outer fold`],
[`Thermal and control normalisation`, `no (uses healthy plots)`, `training healthy plots for training data; same reference applied to test data`],
[`Stage 2 (scalogram, ReliefF, Boruta, mRMR), index search`, `yes`, `inner folds only`],
[`Stage 3 (VIF) and fusion`, `no`, `training part`],
[`Stage 4 (SFFS), hyper-parameter tuning, early stopping`, `yes`, `inner folds only`],
[`Final evaluation`, `yes`, `test replication, once`]], [3900, 1700, 3706], `Where each step is run so that no information from the test replication enters the model.`, 17));
K.push(...tab2('foldsize', [[`Dataset`, `Training part per outer fold`, `Test part per outer fold`, `Inner folds`],
[`Post-symptomatic (1536 per sensor)`, `≈ 1024 samples (two replications + their healthy plots)`, `≈ 512 samples`, `3, grouped by plot`],
[`Pre-symptomatic (576 per sensor)`, `≈ 384 samples`, `≈ 192 samples`, `3, grouped by plot`]], [2600, 2800, 1900, 2006], `Approximate sizes of the training and test parts.`, 17));
K.push(P(`With about 1024 training samples and at most 15 selected features, every model keeps more than 60 samples per feature, well above the ratio at which the Hughes effect becomes important (Hughes, 1968; Guyon and Elisseeff, 2003). The pre-symptomatic models (≈ 384 training samples) are limited to 10 features.`));
K.push(H1(`6. Objective 1: characterisation of white rust by each sensor`));
K.push(P(`Objective 1 describes what each sensor sees. It uses the 1536 post-symptomatic samples of each sensor and produces the disease-specific feature pools that are the scientific basis of Objectives 2 and 3. The steps below are run on all post-symptomatic samples for description and interpretation; for prediction, the same selection steps are repeated inside the training folds (Chapter 5, staged feature selection).`));
K.push(...tab2('o1steps', [[`Step`, `Hyperspectral`, `Multispectral`, `RGB`, `Thermal`],
[`O1-1 Response curves`, `mean spectra by class`, `band means by class`, `colour and texture by class`, `temperature by class`],
[`O1-2 Redundancy`, `one band per region`, `clusters`, `clusters`, `clusters`],
[`O1-3 Band screening`, `scalogram + ReliefF`, `—`, `—`, `—`],
[`O1-4 Index search`, `White Rust Index`, `10 NDSI`, `—`, `—`],
[`O1-5 Response test`, `ANOVA, Tukey, r`, `ANOVA, Tukey, r`, `ANOVA, Tukey, r`, `ANOVA, Tukey, r`],
[`O1-6 DSF pools`, `Boruta`, `Boruta`, `Boruta`, `Boruta`],
[`O1-7 Treatments and sensors`, `variety, timing, cross-sensor correlation`, `same`, `same`, `same`]], [2200, 1900, 1750, 1750, 1706], `Objective 1 steps for each sensor.`, 17));
K.push(H3(`O1-1  Response curves by severity, date and treatment`));
K.push(...tab2('to11', [[`Item`, `Description`],
[`Problem solved`, `Shows how each sensor responds to white rust before any selection, and whether the response depends on variety or crop age.`],
[`Input`, `Subplot feature tables (post-symptomatic).`],
[`Output → next step`, `Response figures and a list of responsive regions → O1-2 to O1-5 (interpretation).`]], [1900, 7406], `Step O1-1 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Plot the mean spectrum (hyperspectral), mean band values (multispectral), colour and texture means (RGB) and temperature values (thermal) for each severity class.`));
K.push(NL(`Repeat by variety (V1–V3) and inoculation timing (D1–D4), and over days after inoculation for each treatment.`));
K.push(P(`**Why this method.** Response curves show the physiological basis (visible rise from chlorophyll loss, red-edge shift, NIR fall from structural damage, SWIR rise from water loss, warmer canopy) and make later results interpretable.`));
K.push(P(`**Studies that used the same step.** Spectral response of severity levels: Mahlein et al. (2013), Ma et al. (2026); red-edge and pigment changes under stress: Carter and Knapp (2001), Horler et al. (1983); temperature response to disease: Oerke et al. (2006).`));
K.push(H3(`O1-2  Redundancy reduction within groups`));
K.push(...tab2('to12', [[`Item`, `Description`],
[`Problem solved`, `As Stage 1 (Chapter 5, staged feature selection), applied to all post-symptomatic samples of each sensor.`],
[`Input`, `Feature groups of each sensor.`],
[`Output → next step`, `Thinned groups → O1-3 to O1-6.`]], [1900, 7406], `Step O1-2 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Remove near-constant features; keep one feature per correlation cluster (|r| ≥ 0.95); one band per correlated spectral region for the hyperspectral bands.`));
K.push(P(`**Why this method.** See Stage 1.`));
K.push(P(`**Studies that used the same step.** Mahlein et al. (2013); Tian et al. (2021); Dormann et al. (2013).`));
K.push(H3(`O1-3  Band-level screening of the hyperspectral bands`));
K.push(...tab2('to13', [[`Item`, `Description`],
[`Problem solved`, `Finds which wavelengths respond to severity (regression) and which separate the classes (classification).`],
[`Input`, `Thinned R, FD and SD bands.`],
[`Output → next step`, `Robust bands (found by both methods), regression-only and classification-only bands → O1-5, O1-6.`]], [1900, 7406], `Step O1-3 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Correlation scalogram: Pearson r of every band of R, FD and SD with the severity score; candidates with p < 0.01 and the top 5% |r|.`));
K.push(NL(`ReliefF on the severity classes (k = 10, neighbours from the same plot excluded); candidates = top 5% of weights.`));
K.push(NL(`Keep one band per correlated region in each list; bands found by both lists (same region or within 10 nm) are robust white-rust bands.`));
K.push(P(`**Why this method.** The scalogram is the first step used for mustard aphid stress with ground hyperspectral data; ReliefF handles overlapping classes and was used to build disease indices.`));
K.push(P(`**Studies that used the same step.** Shukla et al. (2024); Cheng et al. (2010); Robnik-Šikonja and Kononenko (2003); Mahlein et al. (2013); Huang et al. (2014).`));
K.push(H3(`O1-4  White Rust Index and two-band index search`));
K.push(...tab2('to14', [[`Item`, `Description`],
[`Problem solved`, `General vegetation indices are not specific to white rust.`],
[`Input`, `Hyperspectral reflectance (450–2400 nm at 6 nm steps); multispectral bands.`],
[`Output → next step`, `White Rust Index (WRI) formula and the best multispectral NDSI → O1-5, O1-6 and the feature groups of Objectives 2–3.`]], [1900, 7406], `Step O1-4 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Search WRI = ND(λ1, λ2) + w × R(λ3), with w ∈ {−1, −0.5, 0, 0.5, 1}, ND bands at least 50 nm apart, using the ReliefF top 25% of bands and NDs.`));
K.push(NL(`Score each candidate by balanced accuracy (healthy vs diseased) with a plot-grouped cross-validation; keep the best formula.`));
K.push(NL(`For multispectral data, evaluate all ten normalised differences of the five bands.`));
K.push(NL(`Inside the training folds of Objectives 2–3 the search is repeated, so the test data never choose the formula.`));
K.push(P(`**Why this method.** A disease-specific index combines the most informative band difference with a band that carries additional information; it is simple, interpretable and transferable.`));
K.push(P(`**Studies that used the same step.** Mahlein et al. (2013); optimised disease indices: Huang et al. (2014); two-band NDSI and RSI searches: Ma et al. (2026); new texture-fusion index: Ma et al. (2026).`));
K.push(P(`**Index forms searched** (Mahlein et al., 2013; Ma et al., 2026):`));
K.push(EQ(`NDSI(λ_{1}, λ_{2}) = (R_{λ1} − R_{λ2}) / (R_{λ1} + R_{λ2});    WRI = NDSI(λ_{1}, λ_{2}) + w R_{λ3},  w ∈ {−1, −0.5, 0, 0.5, 1}`));
K.push(H3(`O1-5  Response test of features`));
K.push(...tab2('to15', [[`Item`, `Description`],
[`Problem solved`, `Shows which features differ among severity classes and how strongly they relate to the score.`],
[`Input`, `Indices, red-edge parameters, WRI, robust bands, texture and thermal features of each sensor.`],
[`Output → next step`, `Ranked list of responding features per sensor → O1-6 and interpretation.`]], [1900, 7406], `Step O1-5 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`One-way ANOVA across severity classes with effect size η² and Tukey HSD groups.`));
K.push(NL(`Pearson r with the severity score.`));
K.push(NL(`p-values are used only to rank features, because subplots of a plot are related.`));
K.push(P(`**Why this method.** ANOVA and Tukey are the simplest way to show where classes differ and which classes overlap; correlation shows the strength of the relation with severity.`));
K.push(P(`**Studies that used the same step.** Tukey (1949); response tests in disease studies: Mahlein et al. (2019), Feng et al. (2022), Liu et al. (2024); correlation of indices and texture with severity: Ma et al. (2026).`));
K.push(H3(`O1-6  Disease-specific feature (DSF) pools with Boruta`));
K.push(...tab2('to16', [[`Item`, `Description`],
[`Problem solved`, `Produces the final list of features of each sensor that carry white-rust information.`],
[`Input`, `Robust bands, WRI, indices, red-edge parameters, texture and thermal features of each sensor.`],
[`Output → next step`, `Eight DSF pools (4 sensors × classification and regression) → Objectives 2 and 3 (as candidate groups) and discussion.`]], [1900, 7406], `Step O1-6 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Run Boruta (random forest, 500 trees, up to 100 iterations, p = 0.01) on each sensor, once with the severity classes and once with the score.`));
K.push(NL(`Report confirmed, tentative and rejected features.`));
K.push(P(`**Why this method.** Boruta keeps all relevant features (not only the strongest), which suits a characterisation objective.`));
K.push(P(`**Studies that used the same step.** Kursa and Rudnicki (2010); Mustafa et al. (2023).`));
K.push(H3(`O1-7  Response by treatment and complementarity of sensors`));
K.push(...tab2('to17', [[`Item`, `Description`],
[`Problem solved`, `Shows whether features behave the same in all varieties and inoculation timings, and which sensors carry different information.`],
[`Input`, `DSF pools and the subplot tables with treatment codes.`],
[`Output → next step`, `Treatment-wise response figures and a cross-sensor correlation matrix → choice of sensor combinations and interpretation of Objective 2.`]], [1900, 7406], `Step O1-7 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Plot the main DSFs against days after inoculation for each variety and inoculation timing.`));
K.push(NL(`Compute the correlation matrix between the DSFs of the four sensors (for example thermal ΔT with SWIR water indices).`));
K.push(NL(`Check that DSFs are not simply following flower % or canopy cover (correlation with the covariates).`));
K.push(P(`**Why this method.** Features that respond in all varieties are robust; low correlation between sensors indicates complementary information that fusion can exploit.`));
K.push(P(`**Studies that used the same step.** Sensor complementarity: Mahlein et al. (2019), Maimaitijiang et al. (2020); flowering effects in Brassica: Sulik and Long (2016).`));
K.push(H2(`What each sensor is expected to show and what to report`));
K.push(P(`The expected responses below are hypotheses derived from plant physiology and the published studies; Objective 1 tests them with the field data.`));
K.push(H3(`Hyperspectral`));
K.push(BL(`Expected: higher visible reflectance and lower red-edge slope from chlorophyll loss and chlorosis; a shift of the red-edge position to shorter wavelengths; lower NIR reflectance from mesophyll damage around pustules; higher SWIR reflectance from leaf water loss at higher severity (Horler et al., 1983; Carter and Knapp, 2001; Apan et al., 2004). The leaf-level ASD analysis of this study already pointed to red-edge derivatives and a VNIR index combining the NIR plateau, the 970 nm water shoulder and red-edge reflectance.`));
K.push(BL(`Report: mean spectra and first derivatives by class; scalogram and ReliefF curves; robust band list; WRI formula with its balanced accuracy; top indices with ANOVA groups; Boruta pools.`));
K.push(H3(`Multispectral`));
K.push(BL(`Expected: the 717 nm red-edge and 840 nm NIR bands and red-edge indices (NDRE, CIrededge, MTCI) respond most; red-edge indices were the most consistent multispectral indicators of powdery mildew (Liu et al., 2024).`));
K.push(BL(`Report: band means by class; ranking of the 12 indices and 10 NDSI; texture response; Boruta pools; comparison of each MS index with its hyperspectral equivalent.`));
K.push(H3(`RGB`));
K.push(BL(`Expected: lower greenness (ExG, NGRDI, GLI) with chlorosis; brighter, whiter patches with pustules; higher texture contrast and entropy and lower homogeneity as the canopy surface becomes heterogeneous (Meyer and Neto, 2008; Ma et al., 2026).`));
K.push(BL(`Report: colour-index and texture responses by class; whether RGB features follow flower % (they should be checked at flowering).`));
K.push(H3(`Thermal`));
K.push(BL(`Expected: changes in canopy temperature relative to healthy plots and higher within-subplot temperature variability as infection disturbs transpiration; the direction must be established from the data because environmental conditions also change canopy temperature (Oerke et al., 2006; Jones et al., 2009).`));
K.push(BL(`Report: ΔT, CTD, NRCT and temperature SD by class and date; correlation of thermal features with SWIR water indices.`));
K.push(H1(`7. Objective 2: detection and severity discrimination with single sensors and sensor fusion`));
K.push(P(`Objective 2 builds and compares predictive models on the 1536 post-symptomatic samples of each sensor. Three tasks are modelled: (i) healthy vs diseased, (ii) severity classes and (iii) severity score. Every task is run for the 15 sensor sets with machine-learning and deep-learning models, using feature-level fusion for the combinations.`));
K.push(...fig2('combinations', 'f7_combinations.png', `The 15 sensor sets: 4 single sensors and 11 combinations (6 pairs, 4 triples and all four).`, 520));
K.push(...tab2('sets', [[`Set`, `Sensors`, `Type`, `Question it answers`],
[`S1`, `HS`, `single`, `what the hyperspectral sensor alone achieves`],
[`S2`, `MS`, `single`, `what a low-cost multispectral sensor achieves`],
[`S3`, `RGB`, `single`, `what a consumer camera achieves`],
[`S4`, `TIR`, `single`, `what canopy temperature alone achieves`],
[`S5`, `HS + MS`, `pair`, `whether MS adds to HS`],
[`S6`, `HS + RGB`, `pair`, `whether texture adds to spectra`],
[`S7`, `HS + TIR`, `pair`, `whether temperature adds to spectra`],
[`S8`, `MS + RGB`, `pair`, `low-cost optical pair`],
[`S9`, `MS + TIR`, `pair`, `low-cost spectral + thermal pair`],
[`S10`, `RGB + TIR`, `pair`, `cheapest pair`],
[`S11`, `HS + MS + RGB`, `triple`, `all optical sensors`],
[`S12`, `HS + MS + TIR`, `triple`, `spectral + thermal`],
[`S13`, `HS + RGB + TIR`, `triple`, `hyperspectral + texture + thermal`],
[`S14`, `MS + RGB + TIR`, `triple`, `all low-cost sensors`],
[`S15`, `HS + MS + RGB + TIR`, `all`, `full multimodal system`]], [900, 2400, 1100, 4906], `The 15 sensor sets analysed in Objectives 2 and 3.`, 17));
K.push(H3(`O2-1  Tasks, labels and class balance`));
K.push(...tab2('to21', [[`Item`, `Description`],
[`Problem solved`, `Defines the three prediction problems and handles unequal class sizes.`],
[`Input`, `Post-symptomatic dataset with labels (D4).`],
[`Output → next step`, `Three labelled task datasets → model training.`]], [1900, 7406], `Step O2-1 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Task A, detection: healthy (score 0) vs diseased (score > 0).`));
K.push(NL(`Task B, severity classes: grades 0, 1, 3, 5, 7, 9 (merged if a class has < 5% of samples).`));
K.push(NL(`Task C, regression: canopy severity score.`));
K.push(NL(`Unequal classes are handled with class weights in the loss (machine and deep learning); macro-averaged metrics are reported.`));
K.push(P(`**Why this method.** Detection, class discrimination and quantitative severity answer different practical questions (where, how bad, how much). Class weights avoid models that ignore small classes.`));
K.push(P(`**Studies that used the same step.** Detection, severity classes and disease index regression were analysed together by Feng et al. (2022), Tian et al. (2021) and Abdulridha et al. (2023); macro-averaged metrics: Sokolova and Lapalme (2009).`));
K.push(H3(`O2-2  Fold-wise feature selection and fusion for each sensor set`));
K.push(...tab2('to22', [[`Item`, `Description`],
[`Problem solved`, `Prepares the input features of each sensor set without using the test replication.`],
[`Input`, `Feature groups of each sensor; outer and inner folds.`],
[`Output → next step`, `Optimum feature combinations (ML) and fused pools (DL) for each sensor set, fold and task → O2-3 and O2-4.`]], [1900, 7406], `Step O2-2 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`For each outer fold and task: run Stages 1–3 on each sensor (training part) to get its DSF set.`));
K.push(NL(`For a single-sensor set, the DSF set is the input; for a combination, concatenate the DSF sets and apply VIF < 10 again (feature-level fusion).`));
K.push(NL(`Run Stage 4 (ML-SFFS) separately for every machine-learning model.`));
K.push(P(`**Why this method.** Selecting inside the folds keeps the test replication independent; feature-level fusion allows the contribution of each sensor to be measured.`));
K.push(P(`**Studies that used the same step.** Nested selection: Ambroise and McLachlan (2002), Varma and Simon (2006); group-wise selection followed by fusion: Ma et al. (2026); fusion: Feng et al. (2022), Liu et al. (2024).`));
K.push(H3(`O2-3  Machine-learning models`));
K.push(...tab2('to23', [[`Item`, `Description`],
[`Problem solved`, `Different learners capture different relations between features and severity; comparing them avoids a model-specific conclusion.`],
[`Input`, `Optimum feature combination of each model, standardised with training statistics.`],
[`Output → next step`, `Trained models and predictions on each test replication → O2-5.`]], [1900, 7406], `Step O2-3 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Classification: support vector machine with RBF kernel (SVM), random forest (RF), extreme gradient boosting (XGBoost), k-nearest neighbours (k-NN) and partial least squares discriminant analysis (PLS-DA).`));
K.push(NL(`Regression: support vector regression (SVR), random forest regression (RFR), XGBoost regression, k-NN regression and partial least squares regression (PLSR).`));
K.push(NL(`Hyper-parameters are tuned by grid search in the inner cross-validation (Table ${T('mlgrid')}).`));
K.push(P(`**Why this method.** These models cover kernel, tree-ensemble, boosting, instance-based and latent-variable approaches and are the models most often used for crop-disease detection with spectral, thermal and texture features.`));
K.push(P(`**Studies that used the same step.** SVM: Cortes and Vapnik (1995); RF: Breiman (2001); XGBoost: Chen and Guestrin (2016); k-NN: Cover and Hart (1967); PLS-DA: Barker and Rayens (2003); PLSR: Wold et al. (2001); disease applications: Tian et al. (2021) and Mustafa et al. (2023) (SVM, k-NN with SFFS), Feng et al. (2022) (PLSR, SVR, RFR), Abdulridha et al. (2023) and Liu et al. (2024) (RF).`));
K.push(...tab2('mlgrid', [[`Model`, `Tasks`, `Hyper-parameters tuned (inner CV)`],
[`SVM / SVR`, `A, B / C`, `C ∈ {0.1, 1, 10, 100}; γ ∈ {0.001, 0.01, 0.1, scale}; ε ∈ {0.1, 0.5} for SVR`],
[`RF / RFR`, `A, B / C`, `500 trees; features per split ∈ {√p, 0.3p}; minimum leaf size ∈ {1, 3, 5}`],
[`XGBoost`, `A, B, C`, `trees ∈ {200, 500}; depth ∈ {3, 5}; learning rate ∈ {0.05, 0.1}; subsample 0.8`],
[`k-NN`, `A, B, C`, `k ∈ {3, 5, 7, 9, 11}; uniform or distance weights`],
[`PLS-DA / PLSR`, `A, B / C`, `number of latent variables 1–15`]], [1800, 1300, 6206], `Machine-learning models and tuning grids.`, 17));
K.push(...tab2('models', [[`Model`, `How it works`, `Why it suits this dataset`],
[`SVM / SVR`, `finds the boundary (or regression tube) with the largest margin; the RBF kernel allows curved boundaries`, `works well with a few hundred to a few thousand samples and correlated features (Cortes and Vapnik, 1995)`],
[`RF / RFR`, `averages many decision trees grown on bootstrap samples and random feature subsets`, `robust to noise and non-linear effects; little tuning (Breiman, 2001)`],
[`XGBoost`, `adds trees one after another, each correcting the errors of the previous ones, with regularisation`, `often the most accurate tree model on tabular features (Chen and Guestrin, 2016)`],
[`k-NN`, `predicts from the k most similar training samples`, `simple reference model; good with compact standardised feature sets (Cover and Hart, 1967)`],
[`PLS-DA / PLSR`, `projects correlated features onto a few latent variables that best predict the target`, `standard chemometric model for correlated spectral features (Wold et al., 2001; Barker and Rayens, 2003)`],
[`DNN-F1`, `dense neural network on the concatenated features of all sensors`, `learns non-linear interactions between sensors (Maimaitijiang et al., 2020)`],
[`DNN-F2`, `one sub-network per sensor, sensor attention, then joint layers`, `processes each sensor separately and learns sensor weights (Maimaitijiang et al., 2020; Hu et al., 2018)`]], [1600, 3900, 3806], `How each model works and why it was chosen.`, 15));
K.push(H3(`O2-4  Deep-learning models with feature-level fusion`));
K.push(...tab2('to24', [[`Item`, `Description`],
[`Problem solved`, `Neural networks can learn non-linear interactions between features of different sensors and can weight sensors adaptively.`],
[`Input`, `Fused feature pool (or single-sensor DSF set), standardised.`],
[`Output → next step`, `Trained networks and predictions on each test replication → O2-5.`]], [1900, 7406], `Step O2-4 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`DNN-F1 (input-level feature fusion): the features of all sensors in the set are concatenated and passed through two dense layers (64 and 32 units) with batch normalisation, ReLU and dropout (0.3), then the output layer.`));
K.push(NL(`DNN-F2 (intermediate feature fusion): each sensor has its own sub-network (one or two dense layers of 16–32 units); a squeeze-and-excitation (SE) attention block gives each sensor branch a learned weight; the weighted branches are concatenated and passed to a dense layer of 32 units and the output layer. For single-sensor sets only DNN-F1 is used.`));
K.push(NL(`Outputs: sigmoid (Task A), softmax (Task B) or linear (Task C); losses: weighted cross-entropy or mean squared error.`));
K.push(NL(`Training: Adam optimiser (learning rate 0.001, weight decay 10⁻⁴), batch size 32, up to 500 epochs with early stopping (patience 30) on an inner validation split; five random seeds, predictions averaged.`));
K.push(P(`**Why this method.** With about 1000 training samples per fold, small fully connected networks are appropriate; very deep or transformer networks need much more data. DNN-F2 lets each sensor be processed separately before fusion and was better than input fusion in multi-sensor UAV data; the SE block learns how much each sensor contributes, an idea also used in DT-EDNet.`));
K.push(P(`**Studies that used the same step.** DNN-F1 and DNN-F2 for RGB, multispectral and thermal fusion: Maimaitijiang et al. (2020); squeeze-and-excitation: Hu et al. (2018), used in DT-EDNet by Ma et al. (2026); deep learning: LeCun et al. (2015); Adam: Kingma and Ba (2015); dropout: Srivastava et al. (2014); batch normalisation: Ioffe and Szegedy (2015).`));
K.push(NOTE(`Ma et al. (2026) noted that about 2000 training samples is small for a transformer. This methodology therefore uses compact networks and compares them with machine-learning models on exactly the same folds.`));
K.push(...fig2('dl', 'f8_dl.png', `Deep-learning models with feature-level fusion: DNN-F1 (input-level) and DNN-F2 (intermediate level with sensor attention).`, 540));
K.push(H3(`O2-5  Evaluation metrics`));
K.push(...tab2('to25', [[`Item`, `Description`],
[`Problem solved`, `Accuracy must be measured in a way that reflects ordered classes, unequal class sizes and continuous severity.`],
[`Input`, `Predictions on the three test replications (pooled over folds).`],
[`Output → next step`, `Metric tables for each sensor set, model and task → O2-6.`]], [1900, 7406], `Step O2-5 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Task A: overall accuracy, sensitivity, specificity, F1, area under the ROC curve.`));
K.push(NL(`Task B: overall accuracy, Cohen's kappa and quadratic-weighted kappa (ordered classes), per-class F1, macro-F1, confusion matrix and the share of predictions within one class of the true class.`));
K.push(NL(`Task C: coefficient of determination (R²), root-mean-square error (RMSE), normalised RMSE and ratio of performance to deviation (RPD).`));
K.push(NL(`Report every metric also by variety, inoculation timing and date.`));
K.push(P(`**Why this method.** Macro-F1 gives equal weight to small classes; weighted kappa credits near-misses between ordered classes; RPD relates the error to the spread of the data.`));
K.push(P(`**Studies that used the same step.** Cohen (1960, 1968); Sokolova and Lapalme (2009); Fawcett (2006); Chang et al. (2001); metrics in disease studies: Feng et al. (2022), Ma et al. (2026).`));
K.push(H2(`Equations of the evaluation metrics`));
K.push(P(`For classification, TP, TN, FP and FN are counted per class; p_{o} is the observed and p_{e} the chance agreement; O_{ij} and E_{ij} are the observed and chance-expected counts of true class i predicted as j among k ordered classes (Cohen, 1960, 1968; Sokolova and Lapalme, 2009). For regression, y is the observed and ŷ the predicted score (Chang et al., 2001).`));
K.push(EQ(`OA = (TP + TN)/N;    precision P = TP/(TP + FP);    recall R = TP/(TP + FN);    F1 = 2PR/(P + R);    macro-F1 = (1/k) Σ_{c} F1_{c}`));
K.push(EQ(`κ = (p_{o} − p_{e}) / (1 − p_{e});    κ_{w} = 1 − Σ w_{ij} O_{ij} / Σ w_{ij} E_{ij},  w_{ij} = (i − j)^{2}/(k − 1)^{2}`));
K.push(EQ(`R^{2} = 1 − Σ (y − ŷ)^{2} / Σ (y − ȳ)^{2};    RMSE = √[ (1/n) Σ (y − ŷ)^{2} ];    RPD = SD_{y} / RMSE`));
K.push(H3(`O2-6  Comparison of sensor sets and models, and contribution of each sensor`));
K.push(...tab2('to26', [[`Item`, `Description`],
[`Problem solved`, `Identifies the best sensor set and model and quantifies what each sensor adds.`],
[`Input`, `Metric tables of the 15 sets × models × tasks.`],
[`Output → next step`, `Best sensor set and model for each task; contribution of each sensor → conclusions and O2-7.`]], [1900, 7406], `Step O2-6 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Rank the 15 sets by macro-F1 (Task B), AUC (Task A) and RMSE (Task C) for each model; compare the best machine-learning and best deep-learning model.`));
K.push(NL(`Gain of fusion = metric of a combination minus the metric of its best single sensor.`));
K.push(NL(`Ablation: remove one sensor at a time from S15 and record the drop.`));
K.push(NL(`Report the selection frequency of every feature over the folds; final feature lists contain features selected in at least two of three folds.`));
K.push(NL(`Explain the best models with SHAP values (mean absolute SHAP per feature and per sensor).`));
K.push(P(`**Why this method.** Ablation and fusion gain answer directly whether a sensor is worth flying; SHAP gives consistent, model-agnostic feature importance.`));
K.push(P(`**Studies that used the same step.** Ablation of feature groups and modules: Ma et al. (2026); SHAP: Lundberg and Lee (2017), used for band selection by Ma et al. (2026); fusion gain over single sensors: Feng et al. (2022), Maimaitijiang et al. (2020).`));
K.push(H3(`O2-7  Severity maps`));
K.push(...tab2('to27', [[`Item`, `Description`],
[`Problem solved`, `Field managers need maps rather than tables.`],
[`Input`, `Best model of each task; subplot features of every date.`],
[`Output → next step`, `Subplot-level maps of detection, severity class and severity score for each date → reporting.`]], [1900, 7406], `Step O2-7 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Apply the best model of each task to all subplots of every date (models trained on all training folds).`));
K.push(NL(`Map the predicted class and score at subplot level, together with the absolute error where scores are available.`));
K.push(P(`**Why this method.** Maps show the spatial and temporal development of the disease and the agreement with field scores.`));
K.push(P(`**Studies that used the same step.** Severity maps from UAV models: Abdulridha et al. (2023), Liu et al. (2024), Deng et al. (2024).`));
K.push(H3(`O2-8  Treatment-wise performance and robustness`));
K.push(...tab2('to28', [[`Item`, `Description`],
[`Problem solved`, `A model may work for one variety or crop age and fail for another; treatments must be considered in the evaluation.`],
[`Input`, `Test predictions with variety, inoculation timing and date codes.`],
[`Output → next step`, `Performance by treatment and transfer results → conclusions on robustness.`]], [1900, 7406], `Step O2-8 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Report all metrics separately for each variety (V1–V3), each inoculation timing (D1–D4) and each date.`));
K.push(NL(`Leave-one-variety-out test: train on two varieties and test on the third (mainly V1 ↔ V2, because the resistant variety has few diseased samples).`));
K.push(NL(`Leave-one-inoculation-timing-out test: train on three timings and test on the fourth, to check transfer across crop ages.`));
K.push(NL(`Use these tests for the best ML and best DL model of the best three sensor sets only, to limit computation.`));
K.push(P(`**Why this method.** Blocked tests that leave out a whole group show whether a model extrapolates to new conditions; treatment-wise results show whether the selected features are variety-specific.`));
K.push(P(`**Studies that used the same step.** Blocked cross-validation for extrapolation: Roberts et al. (2017); performance by variety and growth stage: Liu et al. (2024), Feng et al. (2022); independent-site testing: Ma et al. (2026).`));
K.push(H2(`Specification of the 15 sensor sets`));
K.push(P(`For every set the input is the union of the fold-wise DSF sets of its sensors (Stage 3), reduced again by VIF < 10; machine-learning models then select their own subset by ML-SFFS, and the deep-learning models use the fused pool. DNN-F2 is used whenever the set contains two or more sensors. The paragraphs below state what each set is expected to contribute and what comparison it answers.`));
K.push(P(`**S1 – hyperspectral alone.** Input: robust bands, derivatives, red-edge parameters, indices and the WRI. Expected to be the strongest single sensor because it covers pigment, structure and water features; it sets the reference against which all fusion gains are judged (Feng et al., 2022; Ma et al., 2026). Models: all ML models and DNN-F1.`));
K.push(P(`**S2 – multispectral alone.** Input: five bands, red-edge and chlorophyll indices, NDSI and texture. Answers whether a low-cost, satellite-like sensor captures most of the hyperspectral information; compare its best index with the WRI and with S1 (Liu et al., 2024).`));
K.push(P(`**S3 – RGB alone.** Input: colour indices and texture. Tests whether a consumer camera is sufficient for visible symptoms; expected to be weaker at low severity, where colour change is small (Guo et al., 2021; Ma et al., 2026).`));
K.push(P(`**S4 – thermal alone.** Input: normalised temperature features and thermal texture. Tests the physiological (transpiration) signal on its own; expected to be weaker for severity classes but potentially useful for early change (Mahlein et al., 2019; Liu et al., 2024).`));
K.push(P(`**S5 – HS + MS.** Tests whether multispectral texture and bands add anything to the hyperspectral spectrum; a small gain is expected because the spectral information overlaps, which shows whether the cheaper MS sensor can replace HS.`));
K.push(P(`**S6 – HS + RGB.** Combines detailed spectra with high-resolution canopy texture; tests the spectral + texture fusion found useful for powdery mildew and rice blast (Feng et al., 2022; Ma et al., 2026).`));
K.push(P(`**S7 – HS + TIR.** Combines spectral (pigment, structure, water) and thermal (transpiration) information; tests the hyperspectral + thermal fusion that improved Fusarium head blight detection (Mahlein et al., 2019).`));
K.push(P(`**S8 – MS + RGB.** An all-optical low-cost pair: red-edge spectra plus fine texture.`));
K.push(P(`**S9 – MS + TIR.** Low-cost spectral + thermal pair, the combination used for powdery mildew severity by Liu et al. (2024); a practical candidate for routine monitoring.`));
K.push(P(`**S10 – RGB + TIR.** The cheapest pair; shows how far colour, texture and temperature go without narrow bands.`));
K.push(P(`**S11 – HS + MS + RGB.** All optical sensors; tests whether thermal is needed at all.`));
K.push(P(`**S12 – HS + MS + TIR.** All spectral sensors with thermal; tests whether RGB texture is needed.`));
K.push(P(`**S13 – HS + RGB + TIR.** Hyperspectral, texture and thermal: the three types of information that Feng et al. (2022) fused; tests whether MS is redundant when HS is present.`));
K.push(P(`**S14 – MS + RGB + TIR.** All low-cost sensors; the main practical alternative to a hyperspectral system.`));
K.push(P(`**S15 – all four sensors.** The full multimodal system; used for the drop-one-sensor ablation that measures the contribution of each sensor.`));
K.push(H2(`Result tables to be produced`));
K.push(...tab2('templateA', [[`Sensor set`, `Best ML model`, `Macro-F1`, `Weighted kappa`, `Best DL model`, `Macro-F1`, `Weighted kappa`],
[`S1 HS`, `…`, `…`, `…`, `…`, `…`, `…`],
[`S2 MS`, `…`, `…`, `…`, `…`, `…`, `…`],
[`…`, `…`, `…`, `…`, `…`, `…`, `…`],
[`S15 all`, `…`, `…`, `…`, `…`, `…`, `…`]], [1600, 1500, 1100, 1300, 1500, 1100, 1206], `Template: severity-class results of the 15 sensor sets (one table each for Tasks A, B and C).`, 17));
K.push(...tab2('templateB', [[`Removed sensor (from S15)`, `Macro-F1 without it`, `Change`, `R² without it`, `Change`],
[`HS`, `…`, `…`, `…`, `…`],
[`MS`, `…`, `…`, `…`, `…`],
[`RGB`, `…`, `…`, `…`, `…`],
[`TIR`, `…`, `…`, `…`, `…`]], [2600, 1800, 1200, 1800, 1906], `Template: drop-one-sensor ablation.`, 17));
K.push(H1(`8. Objective 3: prediction at the pre-symptomatic stage`));
K.push(P(`Objective 3 uses the 576 pre-symptomatic samples of each sensor. The question is whether subplots that will develop white rust can be separated from healthy subplots before pustules are visible, and whether their later severity can be predicted. The same 15 sensor sets and the same model families are used, with steps adapted to the weak early signal.`));
K.push(...fig2('obj3', 'f9_obj3.png', `Pre-symptomatic and post-symptomatic periods and how pre-symptomatic samples are labelled from the later status of the same subplot.`, 520));
K.push(H3(`O3-1  Pre-symptomatic samples and labels`));
K.push(...tab2('to31', [[`Item`, `Description`],
[`Problem solved`, `Before symptoms, the visual score is zero everywhere; labels must come from what happens later.`],
[`Input`, `Pre-symptomatic subplot tables; scores of the first post-symptomatic date.`],
[`Output → next step`, `Labelled pre-symptomatic dataset → O3-2.`]], [1900, 7406], `Step O3-1 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Classification: healthy = subplots of the 12 healthy plots; infected = inoculated subplots that show pustules later. Inoculated subplots that never develop symptoms are excluded from the infected class.`));
K.push(NL(`Regression: target = severity score of the same subplot on the first post-symptomatic date.`));
K.push(NL(`Record days after inoculation (DAI) for every sample.`));
K.push(P(`**Why this method.** Retrospective labelling separates truly infected from escaped plants; predicting the later score turns early detection into a forecast of severity.`));
K.push(P(`**Studies that used the same step.** Retrospective labels for pre-symptomatic detection: Zhu et al. (2017), Tian et al. (2021); pre-symptomatic stages in fusion models: Yu et al. (2025); earliest detection days by sensor: Mahlein et al. (2019).`));
K.push(H3(`O3-2  Normalisation to healthy plots of the same date and variety`));
K.push(...tab2('to32', [[`Item`, `Description`],
[`Problem solved`, `Early disease changes are small compared with differences caused by date, weather, variety and crop age.`],
[`Input`, `Pre-symptomatic features; healthy-plot features of the same date and variety.`],
[`Output → next step`, `Control-normalised features → O3-3.`]], [1900, 7406], `Step O3-2 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`For every feature and date, subtract the mean of the healthy plots of the same variety (and divide by their standard deviation).`));
K.push(NL(`Healthy plots of the same treatment are used when available, so that crop age is matched.`));
K.push(NL(`Within each training fold, the normalisation uses only healthy plots of the training replications and of the same date.`));
K.push(P(`**Why this method.** Normalisation against healthy references removes most date and variety effects and was essential for thermal disease detection, where weather changes leaf temperature as much as infection does.`));
K.push(P(`**Studies that used the same step.** Oerke et al. (2006); Jones et al. (2009); healthy references in early detection: Zhu et al. (2017), Zarco-Tejada et al. (2018).`));
K.push(H3(`O3-3  Pre-symptomatic feature screening and selection`));
K.push(...tab2('to33', [[`Item`, `Description`],
[`Problem solved`, `Features that respond after symptoms are not necessarily the earliest responders.`],
[`Input`, `Control-normalised feature groups.`],
[`Output → next step`, `Pre-symptomatic DSF sets of each sensor (fold-wise) → O3-4.`]], [1900, 7406], `Step O3-3 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Screen each feature with the difference between infected and healthy samples (t-test and % difference) on each date, for description.`));
K.push(NL(`Inside the training folds, run the staged selection (Chapter 5, staged feature selection) with the pre-symptomatic labels: Stage 1, Stage 2 (Boruta for all groups because classes are binary; correlation with the later score for regression), Stage 3 VIF < 10, fusion for combinations, Stage 4 ML-SFFS.`));
K.push(P(`**Why this method.** The same staged procedure keeps the methods comparable with Objective 2, while the pre-symptomatic labels allow different, earlier features to be found.`));
K.push(P(`**Studies that used the same step.** Pre-symptomatic disease-specific features with SFFS: Tian et al. (2021); Boruta: Kursa and Rudnicki (2010), Mustafa et al. (2023); early spectral changes in rust and mildew: Terentev et al. (2023), Zhu et al. (2017).`));
K.push(H3(`O3-4  Pre-symptomatic models for the 15 sensor sets`));
K.push(...tab2('to34', [[`Item`, `Description`],
[`Problem solved`, `Detection must be tested for each sensor and combination.`],
[`Input`, `Pre-symptomatic optimum feature sets (ML) and fused pools (DL).`],
[`Output → next step`, `Trained pre-symptomatic models and test predictions → O3-5.`]], [1900, 7406], `Step O3-4 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Classification: SVM, RF, XGBoost, k-NN and PLS-DA; regression: SVR, RFR, XGBoost, k-NN and PLSR; same tuning grids as Objective 2.`));
K.push(NL(`Deep learning: DNN-F1 and DNN-F2 with smaller layers (32 and 16 units) and stronger dropout (0.4), because only about 384 samples are available for training in each fold.`));
K.push(NL(`Same LORO folds as Objective 2.`));
K.push(P(`**Why this method.** The same models allow a fair comparison between the pre- and post-symptomatic stages; smaller networks limit overfitting on the smaller dataset.`));
K.push(P(`**Studies that used the same step.** Pre-symptomatic classification with SVM and related models: Zhu et al. (2017), Tian et al. (2021); dual-branch deep fusion for pre-symptomatic rice sheath blight: Yu et al. (2025); network regularisation: Srivastava et al. (2014).`));
K.push(H3(`O3-5  Evaluation, earliest detection day and risk maps`));
K.push(...tab2('to35', [[`Item`, `Description`],
[`Problem solved`, `Shows how early, with which sensor set and with what reliability white rust can be predicted.`],
[`Input`, `Test predictions of all models and sensor sets with DAI.`],
[`Output → next step`, `Pre-symptomatic accuracy tables, earliest detection day per sensor set, risk maps → conclusions.`]], [1900, 7406], `Step O3-5 at a glance.`, 17));
K.push(P(`**What is done.**`));
K.push(NL(`Classification: sensitivity, specificity, balanced accuracy and AUC; regression: R² and RMSE of the later score.`));
K.push(NL(`Earliest detection day: compute balanced accuracy separately for each pre-symptomatic date (DAI) and take the first date on which it exceeds a chosen level (for example 0.70) for each sensor set.`));
K.push(NL(`Map the predicted infection probability of every subplot on each pre-symptomatic date (risk maps).`));
K.push(P(`**Why this method.** Sensitivity and specificity matter more than overall accuracy for an early warning; the accuracy-by-DAI curve shows when detection becomes reliable and which sensor responds first.`));
K.push(P(`**Studies that used the same step.** Fawcett (2006); earliest detection days of hyperspectral, thermal and fluorescence sensors: Mahlein et al. (2019); pre-symptomatic maps for early warning: Zarco-Tejada et al. (2018), Yu et al. (2025).`));
K.push(H2(`Sensor-specific expectations at the pre-symptomatic stage`));
K.push(BL(`Hyperspectral: small red-edge and pigment-index changes may appear before pustules, as reported for wheat leaf rust and tobacco mosaic virus (Terentev et al., 2023; Zhu et al., 2017).`));
K.push(BL(`Thermal: transpiration changes can precede visible symptoms; thermal imaging detected Fusarium head blight later than hyperspectral imaging in one study but added to fusion (Mahlein et al., 2019), so its value is tested here.`));
K.push(BL(`Multispectral: the red-edge band may carry part of the hyperspectral early signal.`));
K.push(BL(`RGB: colour and texture are expected to respond only after visible symptoms; RGB-only sets serve as a negative control for the pre-symptomatic stage.`));
K.push(BL(`Treatments: inoculation timing changes crop age at infection; earliest detection days are therefore reported separately for each inoculation timing and variety.`));
K.push(H1(`9. How the steps fulfil the three objectives`));
K.push(...tab2('fulfil', [[`Objective`, `Steps`, `Evidence produced`],
[`1. Characterisation`, `P1–P8, F1–F4, O1-1 to O1-7`, `response curves; robust bands; White Rust Index; DSF pools of each sensor; response by variety and inoculation timing; complementarity of sensors`],
[`2. Detection and severity discrimination by fusion`, `V1–V2, S1–S5, O2-1 to O2-7`, `accuracy of 15 sensor sets × ML and DL models for detection, classes and regression; fusion gain; ablation; SHAP; maps`],
[`3. Pre-symptomatic prediction`, `O3-1 to O3-5 (with V1–V2 and S1–S5)`, `pre-symptomatic accuracy of 15 sensor sets; earliest detection day; later-severity prediction; risk maps`]], [2600, 2700, 4006], `Link between steps and objectives.`, 17));
K.push(P(`**What is new in this methodology.** (1) White rust of mustard is characterised with four UAV sensors measured on identical vegetation pixels; (2) a White Rust Index is derived and tested; (3) all 15 sensor sets are compared under one nested, plot-grouped design with both machine-learning and deep-learning feature-level fusion; (4) the contribution of each sensor is quantified by fusion gain, ablation and attention weights; (5) pre-symptomatic prediction is tested with retrospective labels, control normalisation and an earliest-detection analysis.`));
K.push(H2(`Input–output chain of all steps`));
K.push(...tab2('chain', [[`Step`, `Input`, `Output (to next step)`],
[`D1–D4`, `field design, scores`, `labelled subplot list; post- and pre-symptomatic datasets`],
[`P1–P2`, `raw images, panels, GCPs`, `calibrated, georeferenced mosaics`],
[`P3`, `HS cube`, `clean 483-band cube`],
[`P4–P5`, `mosaics of all sensors`, `aligned layers on the HS grid`],
[`P6`, `HS cube, training regions`, `vegetation mask`],
[`P7–P8`, `masked layers, polygons`, `subplot tables per date and sensor`],
[`F1–F4`, `subplot tables`, `feature groups per sensor`],
[`V1–V2`, `labelled feature tables`, `outer and inner folds`],
[`S1–S3`, `feature groups (training part)`, `sensor DSF sets`],
[`S4`, `DSF sets of a combination`, `fused pool`],
[`S5`, `fused pool`, `optimum feature combinations`],
[`O1-1 to O1-7`, `post-symptomatic feature groups`, `DSF pools, WRI, response figures`],
[`O2-1 to O2-8`, `fold-wise features, labels`, `models, metrics, best sensor set, contributions, maps`],
[`O3-1 to O3-5`, `pre-symptomatic features, later labels`, `pre-symptomatic models, earliest detection day, risk maps`]], [1700, 3700, 3906], `Input and output of every step.`, 17));
K.push(H1(`10. Six-month work plan`));
K.push(...fig2('gantt', 'f10_gantt.png', `Six-month work plan for the analysis.`, 540));
K.push(...tab2('plan', [[`Month`, `Work`, `Deliverable`],
[`1`, `P1–P8 for all dates and sensors; mask accuracy; subplot tables`, `quality-checked subplot tables (4 sensors × all dates)`],
[`2`, `F1–F4 feature extraction; O1-1 to O1-3`, `feature tables; response curves; band screening`],
[`3`, `O1-4 to O1-7; validation folds; selection code tested`, `White Rust Index; DSF pools; Objective 1 chapter draft`],
[`4`, `O2: single sensors S1–S4 (ML + DL, three tasks)`, `single-sensor results`],
[`5`, `O2: 11 combinations, fusion gain, ablation, SHAP, maps; O3 started`, `fusion results; maps`],
[`6`, `O3 models, earliest detection, risk maps; synthesis and writing`, `Objective 3 results; thesis chapters; two manuscripts`]], [1000, 5000, 3306], `Month-wise plan.`, 17));
K.push(NOTE(`Computing load: 15 sensor sets × 3 tasks × 3 folds × 5 ML models with SFFS, plus two DL models × 5 seeds, for two datasets. Run the single-sensor selections once per fold and reuse them for all combinations; cache the subplot tables; run deep-learning training on a GPU.`));
K.push(H1(`11. Software and reproducibility`));
K.push(...tab2('software', [[`Task`, `Software`],
[`Image processing, registration, resampling, masks`, `ENVI, ArcGIS or Python (GDAL, rasterio); hourglass notebook (MNF, PPI, n-D, SAM)`],
[`Features, selection, ML models`, `Python: numpy, pandas, scikit-learn (Pedregosa et al., 2011), xgboost (Chen and Guestrin, 2016), BorutaPy, ReliefF, mlxtend SFFS (Raschka, 2018)`],
[`Deep learning`, `PyTorch (Paszke et al., 2019)`],
[`Interpretation`, `SHAP (Lundberg and Lee, 2017)`]], [3300, 6006], `Software used.`, 17));
K.push(BL(`Fix random seeds; store the outer and inner folds as files and reuse them for all sensor sets.`));
K.push(BL(`Log every setting (bands removed, mask threshold, selected features per fold, hyper-parameters).`));
K.push(BL(`Keep raw, intermediate and final tables separate and versioned.`));
K.push(H1(`12. Questions expected in the seminar`));
K.push(P(`**Q. Why are the folds grouped by replication and not random?** Subplots of a plot and plots of a replication are similar; random splits put near-identical samples in training and test sets and inflate accuracy (Roberts et al., 2017). Testing on a whole replication is the closest test to new plots.`));
K.push(P(`**Q. Why select features in stages instead of using all features at once?** With about 1600 features and 1000 training samples, selection on one pool is unstable, keeps duplicates and lets large groups swamp small ones (Hughes, 1968; Guyon and Elisseeff, 2003; Dormann et al., 2013). Group-wise selection then pooling was also used by Ma et al. (2026).`));
K.push(P(`**Q. Why feature-level fusion only?** It keeps sensors identifiable, so each sensor's contribution can be measured, and it reduces dimensionality compared with fusing raw data (Ghamisi et al., 2019); both machine-learning and deep-learning versions are tested (Maimaitijiang et al., 2020).`));
K.push(P(`**Q. Why not a transformer such as DT-EDNet?** DT-EDNet was trained on about 2000 samples, which its own reviewers regard as small for a transformer (Ma et al., 2026). With about 1000 training samples per fold, compact DNNs are more appropriate; the SE attention idea is kept in DNN-F2.`));
K.push(P(`**Q. Why keep flowers in the subplot spectrum?** The canopy score includes the inflorescence and staghead; flower % is recorded and checked so that selected features are not only flowering effects (Sulik and Long, 2016).`));
K.push(P(`**Q. How is pre-symptomatic infection known if no symptoms are visible?** From the later status of the same subplot (retrospective labels); inoculated subplots that never develop symptoms are excluded (Zhu et al., 2017; Tian et al., 2021).`));
K.push(P(`**Q. How is the contribution of each sensor shown?** By fusion gain over the best single sensor, by removing one sensor at a time from the full set (ablation), by the attention weights of DNN-F2 and by SHAP values (Lundberg and Lee, 2017).`));
K.push(H1('References'));
const refPara = r => new Paragraph({ spacing: { after: 70, line: 255 }, indent: { left: 400, hanging: 400 }, children: [new TextRun({ text: r, font: FONT, size: 19 })] });
['Abdulridha, J., Min, A., Rouse, M. N., Kianian, S., Isler, V., & Yang, C. (2023). Evaluation of stem rust disease in wheat fields by drone hyperspectral imaging. Sensors, 23(8), 4154.',
'Ambroise, C., McLachlan, G.J. (2002). Selection bias in gene extraction on the basis of microarray gene-expression data. Proceedings of the National Academy of Sciences 99(10), 6562–6566. https://doi.org/10.1073/pnas.102102699',
'Apan, A., Held, A., Phinn, S., Markley, J. (2004). Detecting sugarcane \'orange rust\' disease using EO-1 Hyperion hyperspectral imagery. International Journal of Remote Sensing 25(2), 489–498.',
'Babar, M.A., Reynolds, M.P., van Ginkel, M., Klatt, A.R., Raun, W.R., Stone, M.L. (2006). Spectral reflectance indices as a potential indirect selection criteria for wheat yield under irrigation. Crop Science 46(2), 578–588.',
'Barker, M., Rayens, W. (2003). Partial least squares for discrimination. Journal of Chemometrics 17(3), 166–173.',
'Barnes, J.D., Balaguer, L., Manrique, E., Elvira, S., Davison, A.W. (1992). A reappraisal of the use of DMSO for the extraction and determination of chlorophylls a and b in lichens and higher plants. Environmental and Experimental Botany 32(2), 85–100.',
'Bausch, W.C., Duke, H.R. (1996). Remote sensing of plant nitrogen status in corn. Transactions of the ASAE 39(5), 1869–1875.',
'Bhattacharya, B.K., Chattopadhyay, C. (2013). A multi-stage tracking for mustard rot disease combining surface meteorology and satellite remote sensing. Computers and Electronics in Agriculture 90, 35–44. https://doi.org/10.1016/j.compag.2012.10.001',
'Blackburn, G.A. (1998). Quantifying chlorophylls and carotenoids at leaf and canopy scales: an evaluation of some hyperspectral approaches. Remote Sensing of Environment 66(3), 273–285.',
'Boardman, J.W., Kruse, F.A., Green, R.O. (1995). Mapping target signatures via partial unmixing of AVIRIS data. Summaries of the Fifth Annual JPL Airborne Earth Science Workshop, JPL Publication 95-1, Vol. 1, 23–26.',
'Bock, C.H., Poole, G.H., Parker, P.E., Gottwald, T.R. (2010). Plant disease severity estimated visually, by digital photography and image analysis, and by hyperspectral imaging. Critical Reviews in Plant Sciences 29(2), 59–107.',
'Breiman, L. (2001). Random forests. Machine Learning 45(1), 5–32.',
'Broge, N.H., Leblanc, E. (2001). Comparing prediction power and stability of broadband and hyperspectral vegetation indices for estimation of green leaf area index and canopy chlorophyll density. Remote Sensing of Environment 76(2), 156–172.',
'Carter, G.A., Knapp, A.K. (2001). Leaf optical properties in higher plants: linking spectral characteristics to stress and chlorophyll concentration. American Journal of Botany 88(4), 677–684.',
'Chang, C.-W., Laird, D.A., Mausbach, M.J., Hurburgh, C.R. (2001). Near-infrared reflectance spectroscopy–principal components regression analyses of soil properties. Soil Science Society of America Journal 65(2), 480–490.',
'Chappelle, E.W., Kim, M.S., McMurtrey, J.E. (1992). Ratio analysis of reflectance spectra (RARS): an algorithm for the remote estimation of the concentrations of chlorophyll a, chlorophyll b, and carotenoids in soybean leaves. Remote Sensing of Environment 39(3), 239–247.',
'Chattopadhyay, C., et al. (2011). Epidemiology and development of forecasting models for white rust of Brassica juncea in India. Archives of Phytopathology and Plant Protection 44(8), 751–763.',
'Chen, J.M. (1996). Evaluation of vegetation indices and a modified simple ratio for boreal applications. Canadian Journal of Remote Sensing 22(3), 229–242.',
'Chen, T., Guestrin, C. (2016). XGBoost: a scalable tree boosting system. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 785–794.',
'Cheng, T., Rivard, B., Sánchez-Azofeifa, G.A., Feng, J., Calvo-Polanco, M. (2010). Continuous wavelet analysis for the detection of green attack damage due to mountain pine beetle infestation. Remote Sensing of Environment 114(4), 899–910.',
'Cohen, J. (1960). A coefficient of agreement for nominal scales. Educational and Psychological Measurement 20(1), 37–46.',
'Cohen, J. (1968). Weighted kappa: nominal scale agreement with provision for scaled disagreement or partial credit. Psychological Bulletin 70(4), 213–220.',
'Congalton, R.G. (1991). A review of assessing the accuracy of classifications of remotely sensed data. Remote Sensing of Environment 37(1), 35–46. https://doi.org/10.1016/0034-4257(91)90048-B',
'Conn, K.L., Tewari, J.P., Awasthi, R.P. (1990). A disease assessment key for Alternaria blackspot in rapeseed and mustard. Canadian Plant Disease Survey 70(1), 19–22.',
'Cortes, C., Vapnik, V. (1995). Support-vector networks. Machine Learning 20(3), 273–297.',
'Cover, T., Hart, P. (1967). Nearest neighbor pattern classification. IEEE Transactions on Information Theory 13(1), 21–27.',
'Dai, X., Khorram, S. (1998). The effects of image misregistration on the accuracy of remotely sensed change detection. IEEE Transactions on Geoscience and Remote Sensing 36(5), 1566–1577. https://doi.org/10.1109/36.718860',
'Dash, J., Curran, P.J. (2004). The MERIS terrestrial chlorophyll index. International Journal of Remote Sensing 25(23), 5403–5413.',
'Daughtry, C.S.T., Walthall, C.L., Kim, M.S., de Colstoun, E.B., McMurtrey, J.E. (2000). Estimating corn leaf chlorophyll concentration from leaf and canopy reflectance. Remote Sensing of Environment 74(2), 229–239.',
'Deng, J., Hong, D., Li, C., Yao, J., Yang, Z., Zhang, Z., Chanussot, J. (2024). RustQNet: multimodal deep learning for quantitative inversion of wheat stripe rust disease index. Computers and Electronics in Agriculture 225, 109245.',
'Dormann, C.F., Elith, J., Bacher, S., et al. (2013). Collinearity: a review of methods to deal with it and a simulation study evaluating their performance. Ecography 36(1), 27–46. https://doi.org/10.1111/j.1600-0587.2012.07348.x',
'Elsayed, S., Elhoweity, M., Ibrahim, H.H., Dewir, Y.H., Migdadi, H.M., Schmidhalter, U. (2017). Thermal imaging and passive reflectance sensing to estimate the water status and grain yield of wheat under different irrigation regimes. Agricultural Water Management 189, 98–110.',
'Fawcett, T. (2006). An introduction to ROC analysis. Pattern Recognition Letters 27(8), 861–874.',
'Feng, Z., Song, L., Duan, J., He, L., Zhang, Y., Wei, Y., Feng, W. (2022). Monitoring wheat powdery mildew based on hyperspectral, thermal infrared, and RGB image data fusion. Sensors 22(1), 31. https://doi.org/10.3390/s22010031',
'Filella, I., Peñuelas, J. (1994). The red edge position and shape as indicators of plant chlorophyll content, biomass and hydric status. International Journal of Remote Sensing 15(7), 1459–1470.',
'Gamon, J.A., Peñuelas, J., Field, C.B. (1992). A narrow-waveband spectral index that tracks diurnal changes in photosynthetic efficiency. Remote Sensing of Environment 41(1), 35–44.',
'Gao, B.-C. (1996). NDWI – a normalized difference water index for remote sensing of vegetation liquid water from space. Remote Sensing of Environment 58(3), 257–266.',
'Ghamisi, P., Rasti, B., Yokoya, N., et al. (2019). Multisource and multitemporal data fusion in remote sensing: A comprehensive review of the state of the art. IEEE Geoscience and Remote Sensing Magazine 7(1), 6–39. https://doi.org/10.1109/MGRS.2018.2890023',
'Gitelson, A., Merzlyak, M.N. (1994). Spectral reflectance changes associated with autumn senescence of Aesculus hippocastanum L. and Acer platanoides L. leaves. Journal of Plant Physiology 143(3), 286–292.',
'Gitelson, A.A., Gritz, Y., Merzlyak, M.N. (2003). Relationships between leaf chlorophyll content and spectral reflectance and algorithms for non-destructive chlorophyll assessment in higher plant leaves. Journal of Plant Physiology 160(3), 271–282.',
'Gitelson, A.A., Kaufman, Y.J., Merzlyak, M.N. (1996). Use of a green channel in remote sensing of global vegetation from EOS-MODIS. Remote Sensing of Environment 58(3), 289–298.',
'Gitelson, A.A., Kaufman, Y.J., Stark, R., Rundquist, D. (2002). Novel algorithms for remote estimation of vegetation fraction. Remote Sensing of Environment 80(1), 76–87.',
'Gitelson, A.A., Merzlyak, M.N., Chivkunova, O.B. (2001). Optical properties and nondestructive estimation of anthocyanin content in plant leaves. Photochemistry and Photobiology 74(1), 38–45.',
'Green, A.A., Berman, M., Switzer, P., Craig, M.D. (1988). A transformation for ordering multispectral data in terms of image quality with implications for noise removal. IEEE Transactions on Geoscience and Remote Sensing 26(1), 65–74.',
'Guo, A., Huang, W., Dong, Y., Ye, H., Ma, H., Liu, B., Wu, W., Ren, Y., Ruan, C., Geng, Y. (2021). Wheat yellow rust detection using UAV-based hyperspectral technology. Remote Sensing 13(1), 123. https://doi.org/10.3390/rs13010123',
'Guyon, I., Elisseeff, A. (2003). An introduction to variable and feature selection. Journal of Machine Learning Research 3, 1157–1182.',
'Haboudane, D., Miller, J.R., Pattey, E., Zarco-Tejada, P.J., Strachan, I.B. (2004). Hyperspectral vegetation indices and novel algorithms for predicting green LAI of crop canopies: modeling and validation in the context of precision agriculture. Remote Sensing of Environment 90(3), 337–352.',
'Haboudane, D., Miller, J.R., Tremblay, N., Zarco-Tejada, P.J., Dextraze, L. (2002). Integrated narrow-band vegetation indices for prediction of crop chlorophyll content for application to precision agriculture. Remote Sensing of Environment 81(2–3), 416–426.',
'Haralick, R.M., Shanmugam, K., Dinstein, I. (1973). Textural features for image classification. IEEE Transactions on Systems, Man, and Cybernetics SMC-3(6), 610–621.',
'Hardisky, M.A., Klemas, V., Smart, R.M. (1983). The influence of soil salinity, growth form, and leaf moisture on the spectral radiance of Spartina alterniflora canopies. Photogrammetric Engineering and Remote Sensing 49(1), 77–83.',
'Horler, D.N.H., Dockray, M., Barber, J. (1983). The red edge of plant leaf reflectance. International Journal of Remote Sensing 4(2), 273–288.',
'Hu, J., Shen, L., Sun, G. (2018). Squeeze-and-excitation networks. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 7132–7141. https://doi.org/10.1109/CVPR.2018.00745',
'Huang, W., Guan, Q., Luo, J., Zhang, J., Zhao, J., Liang, D., Huang, L., Zhang, D. (2014). New optimized spectral indices for identifying and monitoring winter wheat diseases. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing 7(6), 2516–2524. https://doi.org/10.1109/JSTARS.2013.2294961',
'Huete, A.R. (1988). A soil-adjusted vegetation index (SAVI). Remote Sensing of Environment 25(3), 295–309.',
'Hughes, G. (1968). On the mean accuracy of statistical pattern recognizers. IEEE Transactions on Information Theory 14(1), 55–63. https://doi.org/10.1109/TIT.1968.1054102',
'Hunt, E.R., Rock, B.N. (1989). Detection of changes in leaf water content using near- and middle-infrared reflectances. Remote Sensing of Environment 30(1), 43–54.',
'Idso, S.B., Jackson, R.D., Pinter, P.J., Reginato, R.J., Hatfield, J.L. (1981). Normalizing the stress-degree-day parameter for environmental variability. Agricultural Meteorology 24, 45–55.',
'Ioffe, S., Szegedy, C. (2015). Batch normalization: accelerating deep network training by reducing internal covariate shift. Proceedings of the 32nd International Conference on Machine Learning (ICML), PMLR 37, 448–456.',
'Jones, H.G., Serraj, R., Loveys, B.R., Xiong, L., Wheaton, A., Price, A.H. (2009). Thermal infrared imaging of crop canopies for the remote diagnosis and quantification of plant responses to water stress in the field. Functional Plant Biology 36(11), 978–989. https://doi.org/10.1071/FP09123',
'Jordan, C.F. (1969). Derivation of leaf-area index from quality of light on the forest floor. Ecology 50(4), 663–666.',
'Kingma, D.P., Ba, J. (2015). Adam: a method for stochastic optimization. 3rd International Conference on Learning Representations (ICLR). arXiv:1412.6980.',
'Kruse, F.A., Lefkoff, A.B., Boardman, J.W., Heidebrecht, K.B., Shapiro, A.T., Barloon, P.J., Goetz, A.F.H. (1993). The spectral image processing system (SIPS) – interactive visualization and analysis of imaging spectrometer data. Remote Sensing of Environment 44(2–3), 145–163.',
'Kumar, S., Kalha, C.S. (2005). Evaluation of rapeseed-mustard germplasm against white rust and alternaria blight. Annals of Biology (India) 21(1).',
'Kursa, M.B., Rudnicki, W.R. (2010). Feature selection with the Boruta package. Journal of Statistical Software 36(11), 1–13.',
'LeCun, Y., Bengio, Y., Hinton, G. (2015). Deep learning. Nature 521, 436–444. https://doi.org/10.1038/nature14539',
'Liu, Y., Liu, G., Sun, H., An, L., Zhao, R., Liu, M., Tang, W., Li, M., Yan, X., Ma, Y., Zhao, F. (2024). Exploring multi-features in UAV based optical and thermal infrared images to estimate disease severity of wheat powdery mildew. Computers and Electronics in Agriculture 225, 109285. https://doi.org/10.1016/j.compag.2024.109285',
'Louhaichi, M., Borman, M.M., Johnson, D.E. (2001). Spatially located platform and aerial photography for documentation of grazing impacts on wheat. Geocarto International 16(1), 65–70. https://doi.org/10.1080/10106040108542184',
'Lundberg, S.M., Lee, S.-I. (2017). A unified approach to interpreting model predictions. Advances in Neural Information Processing Systems 30, 4765–4774.',
'Ma, J., Wu, P., Guo, S., Lin, Y., Yu, F., Liu, T. (2026). Early detection of rice blast disease using a dual transformer network (DT-EDNet) based on hyperspectral imaging and multi-feature fusion. IAENG International Journal of Applied Mathematics 56(11), 5380–5398.',
'Mahlein, A.-K. (2016). Plant disease detection by imaging sensors – parallels and specific demands for precision agriculture and plant phenotyping. Plant Disease 100(2), 241–251.',
'Mahlein, A.-K., Alisaac, E., Al Masri, A., Behmann, J., Dehne, H.-W., Oerke, E.-C. (2019). Comparison and combination of thermal, fluorescence, and hyperspectral imaging for monitoring Fusarium head blight of wheat on spikelet scale. Sensors 19(10), 2281. https://doi.org/10.3390/s19102281',
'Mahlein, A.-K., Rumpf, T., Welke, P., Dehne, H.-W., Plümer, L., Steiner, U., Oerke, E.-C. (2013). Development of spectral indices for detecting and identifying plant diseases. Remote Sensing of Environment 128, 21–30. https://doi.org/10.1016/j.rse.2012.09.019',
'Maimaitijiang, M., Sagan, V., Sidike, P., Hartling, S., Esposito, F., Fritschi, F.B. (2020). Soybean yield prediction from UAV using multimodal data fusion and deep learning. Remote Sensing of Environment 237, 111599. https://doi.org/10.1016/j.rse.2019.111599',
'Mandal, N., Adak, S., Das, D.K., Sahoo, R.N., Mukherjee, J., Kumar, A., Chinnusamy, V., Das, B., Mukhopadhyay, A., Rajashekara, H., Gakhar, S. (2023). Spectral characterization and severity assessment of rice blast disease using univariate and multivariate models. Frontiers in Plant Science 14, 1067189. https://doi.org/10.3389/fpls.2023.1067189',
'Meinshausen, N., Bühlmann, P. (2010). Stability selection. Journal of the Royal Statistical Society: Series B (Statistical Methodology) 72(4), 417–473. https://doi.org/10.1111/j.1467-9868.2010.00740.x',
'Merton, R., Huntington, J. (1999). Early simulation results of the ARIES-1 satellite sensor for multi-temporal vegetation research derived from AVIRIS. Proceedings of the 8th JPL Airborne Earth Science Workshop, Pasadena.',
'Merzlyak, M.N., Gitelson, A.A., Chivkunova, O.B., Rakitin, V.Y. (1999). Non-destructive optical detection of pigment changes during leaf senescence and fruit ripening. Physiologia Plantarum 106(1), 135–141.',
'Metternicht, G. (2003). Vegetation indices derived from high-resolution airborne videography for precision crop management. International Journal of Remote Sensing 24(14), 2855–2877.',
'Meyer, G.E., Neto, J.C. (2008). Verification of color vegetation indices for automated crop imaging applications. Computers and Electronics in Agriculture 63(2), 282–293. https://doi.org/10.1016/j.compag.2008.03.009',
'Mishra, K.K., Kolte, S.J., Nashaat, N.I., Awasthi, R.P. (2009). Pathological and biochemical changes in Brassica juncea (mustard) infected with Albugo candida (white rust). Plant Pathology 58(1), 80–86. https://doi.org/10.1111/j.1365-3059.2008.01939.x',
'Mustafa, G., Zheng, H., Li, W., Yin, Y., Wang, Y., Zhou, M., Liu, P., Bilal, M., Jia, H., Li, G., Cheng, T., Tian, Y., Cao, W., Zhu, Y., Yao, X. (2023). Fusarium head blight monitoring in wheat ears using machine learning and multimodal data from asymptomatic to symptomatic periods. Frontiers in Plant Science 13, 1102341. https://doi.org/10.3389/fpls.2022.1102341',
'Nogueira, S., Sechidis, K., Brown, G. (2018). On the stability of feature selection algorithms. Journal of Machine Learning Research 18(174), 1–54.',
'Oerke, E.-C., Steiner, U., Dehne, H.-W., Lindenthal, M. (2006). Thermal imaging of cucumber leaves affected by downy mildew and environmental conditions. Journal of Experimental Botany 57(9), 2121–2132. https://doi.org/10.1093/jxb/erj170',
'Paszke, A., Gross, S., Massa, F., et al. (2019). PyTorch: an imperative style, high-performance deep learning library. Advances in Neural Information Processing Systems 32, 8024–8035.',
'Pedregosa, F., et al. (2011). Scikit-learn: machine learning in Python. Journal of Machine Learning Research 12, 2825–2830.',
'Peng, H., Long, F., Ding, C. (2005). Feature selection based on mutual information: criteria of max-dependency, max-relevance, and min-redundancy. IEEE Transactions on Pattern Analysis and Machine Intelligence 27(8), 1226–1238. https://doi.org/10.1109/TPAMI.2005.159',
'Peñuelas, J., Baret, F., Filella, I. (1995). Semi-empirical indices to assess carotenoids/chlorophyll a ratio from leaf spectral reflectance. Photosynthetica 31(2), 221–230.',
'Peñuelas, J., Gamon, J.A., Fredeen, A.L., Merino, J., Field, C.B. (1994). Reflectance indices associated with physiological changes in nitrogen- and water-limited sunflower leaves. Remote Sensing of Environment 48(2), 135–146.',
'Peñuelas, J., Piñol, J., Ogaya, R., Filella, I. (1997). Estimation of plant water concentration by the reflectance Water Index WI (R900/R970). International Journal of Remote Sensing 18(13), 2869–2875.',
'Pudil, P., Novovičová, J., Kittler, J. (1994). Floating search methods in feature selection. Pattern Recognition Letters 15(11), 1119–1125.',
'Ramalingam, S., Sahoo, R.N., Kumar, A., Ranjan, R., Chinnasamy, V. (2026). Early detection of rice blast disease using hyperspectral remote sensing. Plant Science Today 13(1), 1–10. https://doi.org/10.14719/pst.11111',
'Raschka, S. (2018). MLxtend: providing machine learning and data science utilities and extensions to Python\'s scientific computing stack. Journal of Open Source Software 3(24), 638.',
'Raun, W.R., Solie, J.B., Johnson, G.V., Stone, M.L., Lukina, E.V., Thomason, W.E., Schepers, J.S. (2001). In-season prediction of potential grain yield in winter wheat using canopy reflectance. Agronomy Journal 93(1), 131–138.',
'Richards, J.A. (2013). Remote Sensing Digital Image Analysis: An Introduction, 5th edn. Springer, Berlin. https://doi.org/10.1007/978-3-642-30062-2',
'Rinnan, Å., van den Berg, F., Engelsen, S.B. (2009). Review of the most common pre-processing techniques for near-infrared spectra. TrAC Trends in Analytical Chemistry 28(10), 1201–1222. https://doi.org/10.1016/j.trac.2009.07.007',
'Roberts, D.R., Bahn, V., Ciuti, S., et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. Ecography 40(8), 913–929. https://doi.org/10.1111/ecog.02881',
'Robnik-Šikonja, M., Kononenko, I. (2003). Theoretical and empirical analysis of ReliefF and RReliefF. Machine Learning 53, 23–69. https://doi.org/10.1023/A:1025667309714',
'Rondeaux, G., Steven, M., Baret, F. (1996). Optimization of soil-adjusted vegetation indices. Remote Sensing of Environment 55(2), 95–107.',
'Roujean, J.-L., Bréon, F.-M. (1995). Estimating PAR absorbed by vegetation from bidirectional reflectance measurements. Remote Sensing of Environment 51(3), 375–384.',
'Rouse, J.W., Haas, R.H., Schell, J.A., Deering, D.W. (1974). Monitoring vegetation systems in the Great Plains with ERTS. Third ERTS Symposium, NASA SP-351, Vol. 1, 309–317.',
'Saharan, G.S., Verma, P.R., Meena, P.D., Kumar, A. (2014). White Rust of Crucifers: Biology, Ecology and Management. Springer India, New Delhi.',
'Savitzky, A., Golay, M.J.E. (1964). Smoothing and differentiation of data by simplified least squares procedures. Analytical Chemistry 36(8), 1627–1639.',
'Shukla, K.K., Nigam, R., Birah, A., Kanojia, A.K., Kumar, A., Bhattacharya, B.K., Chander, S. (2024). Detection of aphid-infested mustard crop using ground spectroscopy. Remote Sensing 16(1), 47. https://doi.org/10.3390/rs16010047',
'Smith, G.M., Milton, E.J. (1999). The use of the empirical line method to calibrate remotely sensed data to reflectance. International Journal of Remote Sensing 20(13), 2653–2662.',
'Soille, P. (2003). Morphological Image Analysis: Principles and Applications, 2nd edn. Springer, Berlin. https://doi.org/10.1007/978-3-662-05088-0',
'Sokolova, M., Lapalme, G. (2009). A systematic analysis of performance measures for classification tasks. Information Processing and Management 45(4), 427–437.',
'Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., Salakhutdinov, R. (2014). Dropout: a simple way to prevent neural networks from overfitting. Journal of Machine Learning Research 15, 1929–1958.',
'Strobl, C., Boulesteix, A.-L., Zeileis, A., Hothorn, T. (2007). Bias in random forest variable importance measures: Illustrations, sources and a solution. BMC Bioinformatics 8, 25. https://doi.org/10.1186/1471-2105-8-25',
'Sulik, J.J., Long, D.S. (2016). Spectral considerations for modeling yield of canola. Remote Sensing of Environment 184, 161–174.',
'Terentev, A., Badenko, V., Shaydayuk, E., Emelyanov, D., Eremenko, D., Klabukov, D., Fedotov, A., Dolzhenko, V. (2023). Hyperspectral remote sensing for early detection of wheat leaf rust caused by Puccinia triticina. Agriculture 13(6), 1186. https://doi.org/10.3390/agriculture13061186',
'Terentev, A., Dolzhenko, V., Fedotov, A., Eremenko, D. (2022). Current state of hyperspectral remote sensing for early plant disease detection: a review. Sensors 22(3), 757. https://doi.org/10.3390/s22030757',
'Thenkabail, P.S., Enclona, E.A., Ashton, M.S., Van Der Meer, B. (2004). Accuracy assessments of hyperspectral waveband performance for vegetation analysis applications. Remote Sensing of Environment 91(3–4), 354–376.',
'Tian, L., Xue, B., Wang, Z., Li, D., Yao, X., Cao, Q., Zhu, Y., Cao, W., Cheng, T. (2021). Spectroscopic detection of rice leaf blast infection from asymptomatic to mild stages with integrated machine learning and feature selection. Remote Sensing of Environment 257, 112350. https://doi.org/10.1016/j.rse.2021.112350',
'Tsai, F., Philpot, W. (1998). Derivative analysis of hyperspectral data. Remote Sensing of Environment 66(1), 41–51.',
'Tucker, C.J. (1979). Red and photographic infrared linear combinations for monitoring vegetation. Remote Sensing of Environment 8(2), 127–150. https://doi.org/10.1016/0034-4257(79)90013-0',
'Tukey, J.W. (1949). Comparing individual means in the analysis of variance. Biometrics 5(2), 99–114.',
'Varma, S., Simon, R. (2006). Bias in error estimation when using cross-validation for model selection. BMC Bioinformatics 7, 91. https://doi.org/10.1186/1471-2105-7-91',
'Woebbecke, D.M., Meyer, G.E., Von Bargen, K., Mortensen, D.A. (1995). Color indices for weed identification under various soil, residue, and lighting conditions. Transactions of the ASAE 38(1), 259–269.',
'Wold, S., Sjöström, M., Eriksson, L. (2001). PLS-regression: a basic tool of chemometrics. Chemometrics and Intelligent Laboratory Systems 58(2), 109–130.',
'Yu, H., Li, X., Yu, Y., Sui, Y., Zhang, J., Zhang, L., ... & Jiang, R. (2025). A dual-branch multimodal model for early detection of rice sheath blight: Fusing spectral and physiological signatures. Computers and Electronics in Agriculture, 231, 110031.',
'Zarco-Tejada, P.J., Camino, C., Beck, P.S.A., et al. (2018). Previsual symptoms of Xylella fastidiosa infection revealed in spectral plant-trait alterations. Nature Plants 4, 432–439.',
'Zhu, H., Chu, B., Zhang, C., Liu, F., Jiang, L., He, Y. (2017). Hyperspectral imaging for presymptomatic detection of tobacco disease with successive projections algorithm and machine-learning classifiers. Scientific Reports 7, 4125. https://doi.org/10.1038/s41598-017-04501-2',
'Zitová, B., Flusser, J. (2003). Image registration methods: a survey. Image and Vision Computing 21(11), 977–1000. https://doi.org/10.1016/S0262-8856(03)00137-9'].forEach(r => K.push(refPara(r)));


const numcfg = r => ({ reference: r, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] });
const doc = new Document({
  features: { updateFields: true }, creator: 'Animesh Panda', title: 'White rust UAV methodology (field, Objectives 1–3)',
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
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('saved', OUT, 'figs', FORDER.length, 'tabs', TORDER.length, 'eqs', 0, 'refs', 123); });
