const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType, ImageRun,
  TableOfContents, PageBreak, LevelFormat, Footer, PageNumber, BorderStyle } = require('docx');
const B = '/home/user/meta/thesis_build/method3/';
const OUT = '/home/user/meta/thesis_build/method3/../outputs/White_rust_field_methodology_revised_DT-EDNet.docx';
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
const FORDER = ['overall', 'dataset', 'preproc', 'endmember', 'dummyem', 'dummysam', 'features', 'dummyspec', 'normal', 'validation', 'obj1', 'selection', 'dummyndsi', 'dummyshap', 'dummyrelief', 'dummyttfi', 'obj2', 'combinations', 'dnn', 'pseudo', 'dtednet', 'cnns', 'dummycm', 'obj3', 'obj3time', 'earliest', 'gantt'];
const TORDER = ['abbr', 'objectives', 'dataset', 'literature', 'commonact', 'sa1', 'sa2', 'sa3', 'pdiex', 'sa4', 'classex', 'sb1', 'celine', 'sb2', 'sb3', 'csg', 'sb4', 'sb5', 'cresample', 'sc1', 'sc2', 'cmnf', 'sc3', 'cppi', 'sc4', 'sc5', 'sc6', 'samex', 'csam', 'sc7', 'sc8', 'cerosion', 'sd1', 'sd2', 'sd3', 'cfd', 'sd4', 'cvi', 'sd5', 'glcmex', 'cglcm', 'cpca', 'sd6', 'sd7', 'sd8', 'featcount', 'se1', 'se2', 'se3', 'chealthy', 'se4', 'se5', 'czscore', 'se6', 'sf1', 'sf2', 'cnested', 'sf3', 'leak', 'foldsize', 'o1act', 'stages', 's111', 's112', 's113', 's121', 'cndsi', 's122', 'cshap', 's123', 'ccars', 's124', 's131', 's132', 'cwri', 's133', 's141', 's142', 'ccorr', 's143', 'crelief', 's151', 's152', 's153', 'mrmrex', 'cmrmr', 's154', 'cttfi', 's161', 's162', 'cvif', 's163', 's164', 'o2act', 's211', 's212', 's213', 'sets', 's214', 'sffsex', 'csffs', 's215', 's221', 'csvm', 's222', 'crf', 's223', 'cxgb', 's224', 'cknn', 's225', 'cpls', 's226', 'mlgrid', 's231', 's232', 'cdnnf', 's233', 'cpseudo', 's234', 'cdtednet', 's235', 's236', 's237', 'ccnn', 's238', 'ctrain', 's241', 's242', 's243', 'cmetrics', 's251', 's252', 's253', 'ablationt', 's254', 'cablation', 's261', 's262', 's263', 's311', 's321', 's331', 's341', 's351', 'earlyex', 'croc', 's352', 'chain', 'fscheck', 'dtcheck', 'changes', 'hsidx', 'msidx', 'rgbfeat', 'tirfeat', 'plan', 'software'];
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


K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1100, after: 200 }, children: [new TextRun({ text: 'AI-based multimodal UAV sensing of white rust in mustard', font: FONT, size: 44, bold: true, color: '1E3A1F' })] }));
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [new TextRun({ text: 'Research methodology for the field experiment (revised): objectives → activities → steps', font: FONT, size: 28, color: '2C5F2D' })] }));
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: 'Hyperspectral, multispectral, red–green–blue and thermal unmanned aerial vehicle (UAV) data | 15 sensor sets | feature-level fusion | machine learning, feature-fusion neural networks, DT-EDNet, EfficientNet, ResNet18 and ConvNeXt V2', font: FONT, size: 21, italics: true })] }));
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 }, children: [new TextRun({ text: 'Animesh Panda (Roll No. 13098) | Ph.D. Agricultural Physics | ICAR-Indian Agricultural Research Institute, New Delhi', font: FONT, size: 20 })] }));
K.push(BOX(`How to read this document.`, `The work is organised in three levels. (1) Six common activities (A to F) prepare the data once for all objectives. (2) Each objective is divided into activities (for example Activity 1.2). (3) Each activity is divided into numbered steps (for example Step 1.2.3). Every step has a heading and the same layout: purpose, input, output, procedure and supporting studies. Every technique used in a step is described in a method card that gives its principle, the problem it solves, its specification, its hyper-parameters and how they are tuned, the data on which it works well, why it was selected and its references. Flow charts are given for every objective and for the main activities, and small dummy datasets are used to show how each calculation works. Full names are written with their abbreviation in brackets.`, 'EEF3E8', '2C5F2D'));
K.push(BOX(`What is new in this revision.`, `(1) The methods of the DT-EDNet study on rice blast (Ma et al., 2026) are included: effective wavelength ranges from normalised difference and ratio spectral index maps, optimal wavelengths by SHAP-CARS, vegetation index selection by ReliefF, texture from principal-component images selected by minimum redundancy maximum relevance (mRMR), the Tri-band Texture Fusion Index (TTFI) and the DT-EDNet network with EfficientNet, ResNet18 and ConvNeXt V2 as comparison networks for the post-symptomatic data. (2) One feature-selection method is used for each type of feature. (3) The second derivative is not used. (4) A separate activity on normalisation and data preparation is added. (5) The endmember extraction is described step by step. (6) Each technique has a method card.`, 'FFF6E0', 'C98A00'));
K.push(new Paragraph({ children: [new PageBreak()] }));
K.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: 'Contents', font: FONT, size: 32, bold: true, color: '1E3A1F' })] }));
K.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-3' }));
K.push(new Paragraph({ children: [new PageBreak()] }));
K.push(H1(`Full names and abbreviations`));
K.push(P(`The text always gives the full name with the abbreviation in brackets. This list is only for quick reference.`));
K.push(...tab2('abbr', [[`Abbreviation`, `Full name`, `Abbreviation`, `Full name`],
[`AdamW`, `adaptive moment estimation with decoupled weight decay`, `MNF`, `minimum noise fraction`],
[`AUC`, `area under the receiver operating characteristic curve`, `mRMR`, `minimum redundancy maximum relevance`],
[`CARS`, `competitive adaptive reweighted sampling`, `MS`, `multispectral`],
[`CBAM`, `convolutional block attention module`, `NDSI`, `normalised difference spectral index`],
[`CWSI`, `crop water stress index`, `NDVI`, `normalised difference vegetation index`],
[`DAI`, `days after inoculation`, `NRCT`, `normalised relative canopy temperature`],
[`DNN-F1, DNN-F2`, `deep neural network with input-level (F1) or intermediate-level (F2) feature fusion`, `OW`, `optimal wavelengths`],
[`DT-EDNet`, `Dual Transformer Early Detection Network`, `PCA`, `principal component analysis`],
[`DTG`, `Dual Transformer Group`, `PLS, PLS-DA, PLSR`, `partial least squares; discriminant analysis; regression`],
[`GLCM`, `grey-level co-occurrence matrix`, `PPI`, `pixel purity index`],
[`HS`, `hyperspectral`, `RF`, `random forest`],
[`k-NN`, `k-nearest neighbours`, `RGB`, `red–green–blue (camera)`],
[`KTB`, `Kernel Transformer Block`, `RMSE`, `root-mean-square error`],
[`LORO`, `leave-one-replication-out (cross-validation)`, `RPD`, `ratio of performance to deviation`],
[`MCCV`, `Monte Carlo cross-validation`, `RSI`, `ratio spectral index`],
[`MHSA`, `multi-head self-attention`, `SAM`, `spectral angle mapper`],
[`SE`, `squeeze-and-excitation (attention block)`, `SFFS`, `sequential floating forward selection`],
[`SHAP`, `Shapley additive explanations`, `SVM, SVR`, `support vector machine; support vector regression`],
[`TF`, `texture feature`, `TIR`, `thermal infrared`],
[`TTB`, `Token Transformer Block`, `TTFI`, `Tri-band Texture Fusion Index`],
[`UAV`, `unmanned aerial vehicle`, `VI`, `vegetation index`],
[`VIF`, `variance inflation factor`, `WRI`, `White Rust Index`],
[`XGBoost`, `extreme gradient boosting`, ``, ``]], [1500, 3150, 1500, 3156], `Full names of the abbreviations used.`, 16));
K.push(H1(`1. Objectives, data and overall design`));
K.push(H2(`1.1 Background and objectives`));
K.push(P(`White rust, caused by the obligate oomycete Albugo candida, produces white pustules on the leaves, chlorosis and, after systemic infection, distorted inflorescences (staghead) in Indian mustard, and it can reduce yield by 20–60% (Kumar and Kalha, 2005; Saharan et al., 2014). The disease develops under cool and humid weather (Chattopadhyay et al., 2011). Visual scoring is slow and possible only after symptoms appear. Cameras on an unmanned aerial vehicle (UAV) record the changes in pigments, leaf structure, water and temperature that accompany infection, sometimes before symptoms are visible (Mahlein, 2016; Terentev et al., 2022), and combining several cameras usually improves accuracy (Maimaitijiang et al., 2020; Feng et al., 2022).`));
K.push(...tab2('objectives', [[`Objective`, `Question answered`, `Data used`, `Main output`],
[`1. To characterise white rust of mustard through multimodal sensing from a UAV platform`, `Which wavelengths, vegetation indices, texture features and thermal features of each camera respond to white rust severity, and does the response change with variety and inoculation timing?`, `1536 post-symptomatic subplot samples per camera`, `Optimal wavelengths, White Rust Index, selected indices, Tri-band Texture Fusion Index and the disease-specific feature set of each camera`],
[`2. To detect and discriminate disease severity of white rust in mustard through AI-based multimodal data fusion`, `How accurately can (a) healthy vs diseased subplots, (b) severity classes and (c) the severity score be predicted by each of the 15 sensor sets with machine learning and deep learning?`, `1536 post-symptomatic subplot samples per camera`, `Best sensor set and model for each task; contribution of each camera; comparison of DT-EDNet with EfficientNet, ResNet18 and ConvNeXt V2; severity maps`],
[`3. To predict white rust at the pre-symptomatic stage using machine learning`, `Can subplots that will develop white rust be separated from healthy subplots before symptoms, and can their later severity be predicted?`, `576 pre-symptomatic subplot samples per camera`, `Pre-symptomatic models; earliest detection day; risk maps`]], [2600, 3000, 1600, 2106], `Objectives, questions, data and outputs.`, 16));
K.push(H2(`1.2 Overall design`));
K.push(P(`All objectives use the same field data and the same preparation. The common activities A to F are carried out once (Figure ${F('overall')}). Objective 1 then describes and selects the features of each camera, Objective 2 builds the detection and severity models on the post-symptomatic data and Objective 3 builds the early-warning models on the pre-symptomatic data.`));
K.push(...fig2('overall', 'g01_overall.png', `Overall workflow. Common activities A–F prepare the data once; each objective is divided into activities and steps.`, 560));
K.push(P(`**Six rules apply to every activity.** They come from the methodological literature and from the weaknesses reported in recent disease-sensing studies (Ambroise and McLachlan, 2002; Varma and Simon, 2006; Cawley and Talbot, 2010; Roberts et al., 2017; Ma et al., 2026).`));
K.push(NL(`One sample is one subplot on one date. The four subplots of a plot always stay together in the training part or in the test part.`));
K.push(NL(`All cameras are measured on the same vegetation pixels of each subplot (Common Activity C).`));
K.push(NL(`Features are grouped by type, and one selection method is used for each type of feature (Objective 1).`));
K.push(NL(`Every step that uses the severity labels (index search, feature selection, tuning, early stopping) runs inside the training part only.`));
K.push(NL(`All normalisation constants (means, standard deviations, healthy-plot references) are computed on the training part and then applied to the test part.`));
K.push(NL(`The same folds are used for all sensor sets and all models, so that their accuracies are directly comparable.`));
K.push(H2(`1.3 Dataset`));
K.push(...tab2('dataset', [[`Item`, `Value`],
[`Plots × subplots`, `48 × 4 = 192 subplots in each image`],
[`Cameras`, `4: hyperspectral, multispectral, red–green–blue and thermal`],
[`Images`, `8 flight dates × 4 cameras for the post-symptomatic period; pre-symptomatic flight dates in addition`],
[`Post-symptomatic samples per camera`, `1536 (8 dates × 192 subplots)`],
[`Pre-symptomatic samples per camera`, `576 (3 dates × 192 subplots)`],
[`Label of every sample`, `canopy severity score of the subplot (0–9 grade key) recorded on the flight day`],
[`Sensor sets analysed`, `15 (4 single cameras, 6 pairs, 4 triples, all four)`],
[`Tasks`, `detection (healthy vs diseased), severity classes, severity score`],
[`Time for the analysis`, `6 months`]], [3300, 6006], `Dataset used in this methodology (numbers as recorded by the researcher).`, 17));
K.push(...fig2('dataset', 'g26_dataset.png', `Structure of the dataset: flight dates → cameras → plots → scored subplots, and the two datasets used by the objectives.`, 520));
K.push(H2(`1.4 Main published studies used to build the methodology`));
K.push(P(`Each step was chosen because it was used and tested for crop-disease sensing or for the specific data problem it solves. Table ${T('literature')} lists the main disease studies; the methodological references are given in every step and method card.`));
K.push(...tab2('literature', [[`Study`, `Crop and disease`, `Sensors`, `What it contributes to this methodology`],
[`Ma et al. (2026)`, `rice; blast`, `UAV hyperspectral`, `effective ranges from NDSI and RSI maps; SHAP-CARS; ReliefF for indices; principal-component texture with mRMR; TTFI; DT-EDNet vs EfficientNet, ResNet18, ConvNeXt V2; module ablation`],
[`Guo et al. (2021)`, `wheat; yellow rust`, `UAV hyperspectral`, `texture from principal-component images; vegetation index + texture fusion; NDVI soil mask; disease index`],
[`Liu et al. (2020)`, `wheat; Fusarium head blight`, `UAV hyperspectral`, `bands, indices and texture as feature groups; univariate area under the curve screening; neural network`],
[`Yu et al. (2021)`, `pine; pine wilt disease`, `UAV hyperspectral + spectrometer`, `red-edge parameters best for the early stage; random forest`],
[`Feng et al. (2022)`, `wheat; powdery mildew`, `hyperspectral + thermal + RGB`, `feature-level fusion of indices, thermal and texture features`],
[`Liu et al. (2024); Liu et al. (2026)`, `wheat; powdery mildew`, `UAV multispectral + thermal; ground to UAV`, `red-edge indices, thermal features and severity maps; a disease-specific index transferred from ground to UAV`],
[`Calderón et al. (2014)`, `opium poppy; downy mildew`, `UAV thermal + multispectral`, `canopy minus air temperature as a normalised thermal feature`],
[`Zheng et al. (2018); Das et al. (2015)`, `wheat yellow rust; rice bacterial leaf blight`, `hyperspectral simulated to Sentinel-2 and LISS-IV`, `disease-specific three-band index; band simulation for satellite up-scaling`],
[`Yuan et al. (2025)`, `rice; bacterial blight`, `UAV + satellite`, `mRMR feature selection; random forest, support vector machine and k-nearest neighbours`],
[`Maimaitijiang et al. (2020)`, `soybean yield`, `UAV RGB + multispectral + thermal`, `deep neural networks with input-level and intermediate-level fusion`],
[`Mahlein et al. (2013); Huang et al. (2014)`, `sugar beet and wheat diseases`, `hyperspectral`, `ReliefF and disease-specific spectral indices`],
[`Tian et al. (2021); Mustafa et al. (2023)`, `rice blast; wheat Fusarium head blight`, `hyperspectral (+ fluorescence)`, `variance inflation factor and floating forward selection; pre-symptomatic stage`],
[`Zhu et al. (2017); Zarco-Tejada et al. (2018)`, `tobacco virus; olive Xylella`, `hyperspectral (+ thermal)`, `pre-symptomatic detection with labels from the later status`],
[`Mahlein et al. (2019)`, `wheat; Fusarium head blight`, `hyperspectral + thermal + fluorescence`, `sensor comparison and earliest detection day`]], [2100, 1700, 1800, 3706], `Main disease studies and what they contribute.`, 15));
K.push(H1(`2. Common activities (carried out once for all objectives)`));
K.push(P(`The six common activities turn the raw images into clean, normalised feature tables with one row per subplot-date and prepare the validation folds. Each activity is described as a sequence of steps.`));
K.push(...tab2('commonact', [[`Activity`, `Steps`, `Main output`],
[`A. Field experiment, ground truth and datasets`, `A1–A4`, `labelled subplot list; post- and pre-symptomatic datasets`],
[`B. Image pre-processing`, `B1–B5`, `calibrated, aligned images on the hyperspectral grid`],
[`C. Endmember extraction and vegetation mask`, `C1–C8`, `endmember library; vegetation mask applied to all cameras`],
[`D. Subplot spectra and feature extraction`, `D1–D8`, `feature table of each camera`],
[`E. Normalisation and data preparation`, `E1–E6`, `normalised, screened and standardised features`],
[`F. Validation design and tuning`, `F1–F3`, `outer and inner folds; tuning plan; leakage checklist`]], [3500, 1300, 4506], `Common activities and their outputs.`, 17));
K.push(H2(`Activity A – Field experiment, ground truth and datasets`));
K.push(H3(`Step A1 – Experimental design and treatments`));
K.push(...tab2('sa1', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Defines the sources of variation (inoculation timing, variety, replication) so that disease effects can be separated from crop-age and variety effects.`],
[`Input`, `IARI research farm, rabi season; factorial randomised block design.`],
[`Output → next step`, `48 plots with known treatment, replication and plot number → subplots (Step A3) and validation folds (Activity F).`]], [2200, 7106], `Step A1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Four sowing dates at 10-day intervals (D1–D4) with one inoculation date, so the crop is inoculated at four different ages.`));
K.push(NL(`Three varieties of different susceptibility (V1 highly susceptible, V2 moderately susceptible, V3 resistant; names as recorded in the field book).`));
K.push(NL(`The 12 treatments (4 × 3) are inoculated in three replications (R1–R3) with a zoosporangial suspension (Mishra et al., 2009), and one healthy (uninoculated) plot is kept for every treatment: 36 inoculated + 12 healthy = 48 plots.`));
K.push(NL(`Each plot carries a code (treatment, replication, plot number) that is stored with every sample.`));
K.push(P(`**Supporting studies.** Staggered sowing or inoculation and healthy controls were used to create severity gradients for wheat yellow rust (Guo et al., 2021), wheat powdery mildew (Feng et al., 2022; Liu et al., 2024) and rice blast (Tian et al., 2021; Ma et al., 2026); a randomised trial with varieties of different resistance was used for wheat rusts by Blasch et al. (2023).`));
K.push(H3(`Step A2 – UAV flights and cameras`));
K.push(...tab2('sa2', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Provides images of four cameras on the same day, each recording a different plant response.`],
[`Input`, `Flight plan; calibration panels; ground control points.`],
[`Output → next step`, `Raw images of the four cameras on every date → pre-processing (Activity B).`]], [2200, 7106], `Step A2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Fly between 11:00 and 14:00 h under clear sky and low wind, at 30 m above the ground, with about 85% forward and 80% side overlap.`));
K.push(NL(`Hyperspectral camera: Headwall co-aligned visible–near-infrared and short-wave-infrared imager (483 usable bands from 399 to 2398 nm after quality control; ground pixel about 2.2 cm).`));
K.push(NL(`Multispectral camera: MicaSense RedEdge-MX (475, 560, 668, 717 and 840 nm; about 2 cm).`));
K.push(NL(`Red–green–blue camera: DJI camera (about 0.8 cm). Thermal camera: FLIR Vue Pro R, 7.5–13.5 µm (about 3.9 cm).`));
K.push(NL(`Place reflectance panels and ground control points before every flight; record air temperature and relative humidity during the flight.`));
K.push(NL(`Score the subplots on the day of the flight (or within one day).`));
K.push(P(`**Supporting studies.** The same four camera types were combined for wheat powdery mildew (Feng et al., 2022) and soybean yield (Maimaitijiang et al., 2020); flight protocols with panels and solar-noon windows are reviewed by Aasen et al. (2018); thermal flight practice: Messina and Modica (2020).`));
K.push(H3(`Step A3 – Subplots and canopy severity score`));
K.push(...tab2('sa3', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Gives every sampling unit its label.`],
[`Input`, `Plot boundaries; field scoring sheets.`],
[`Output → next step`, `Labelled subplot list (date, plot, subplot, treatment, replication, score) → labels (Step A4) and subplot extraction (Activity D).`]], [2200, 7106], `Step A3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Divide each plot into four equal quadrant subplots; exclude border rows with an inner buffer.`));
K.push(NL(`One trained scorer grades the canopy of each subplot with the 0–9 key of Conn et al. (1990): 0 = no symptoms, 1 = 1–5%, 3 = 6–10%, 5 = 11–25%, 7 = 26–50%, 9 = more than 50% of the canopy leaf area with pustules; staghead is noted after flowering. Grade limits are written on the sheet to keep scoring consistent (Bock et al., 2010).`));
K.push(NL(`For plot summaries, compute the percent disease index of the plot: PDI = Σ(grade of each subplot) / (number of subplots × 9) × 100.`));
K.push(P(`**Supporting studies.** Grade keys of this kind were used for canopy severity in UAV studies of wheat stem rust (Abdulridha et al., 2023), powdery mildew (Liu et al., 2024) and rice blast (Ma et al., 2026); disease indices from graded leaves: Guo et al. (2021).`));
K.push(EQ(`PDI = Σ_{i} grade_{i} / (n × 9) × 100      (n = 4 subplots per plot)`));
K.push(...tab2('pdiex', [[`Subplot`, `1`, `2`, `3`, `4`, `Plot PDI`],
[`Grade (dummy)`, `3`, `5`, `1`, `3`, `(3 + 5 + 1 + 3) / (4 × 9) × 100 = 33.3%`]], [1800, 900, 900, 900, 900, 3906], `Worked example (dummy data): percent disease index of one plot.`, 17));
K.push(H3(`Step A4 – Labels and the two datasets`));
K.push(...tab2('sa4', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Defines exactly what each model predicts and which samples belong to which objective.`],
[`Input`, `Subplot scores of all dates; date of the first visible pustule.`],
[`Output → next step`, `Post-symptomatic dataset (1536 samples per camera) and pre-symptomatic dataset (576 samples per camera) with their labels → all objectives.`]], [2200, 7106], `Step A4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Post-symptomatic dates: on or after the first visible pustule; pre-symptomatic dates: before it.`));
K.push(NL(`Detection label: healthy (grade 0) or diseased (grade above 0), taken from the observed score, not from the treatment.`));
K.push(NL(`Severity classes: the six grades 0, 1, 3, 5, 7 and 9; a grade with fewer than 5% of the samples is merged with its neighbour (for example 7 + 9).`));
K.push(NL(`Severity score: the grade treated as a continuous number for regression.`));
K.push(NL(`Pre-symptomatic labels (Objective 3): healthy = subplots of the healthy plots; infected = inoculated subplots that show pustules on a later date; inoculated subplots that never show symptoms are kept out of the infected class.`));
K.push(P(`**Supporting studies.** Detection, severity classes and regression were analysed together for rice blast (Tian et al., 2021) and wheat powdery mildew (Feng et al., 2022); labels from the later status for pre-symptomatic samples: Zhu et al. (2017), Tian et al. (2021).`));
K.push(...tab2('classex', [[`Grade`, `0`, `1`, `3`, `5`, `7`, `9`],
[`Detection label`, `healthy`, `diseased`, `diseased`, `diseased`, `diseased`, `diseased`],
[`Severity class`, `0`, `1`, `3`, `5`, `7`, `9`],
[`Dummy count (1536 samples)`, `410`, `330`, `290`, `250`, `160`, `96`]], [2500, 1134, 1134, 1134, 1134, 1134, 1136], `How one score gives the three labels (dummy class counts).`, 17));
K.push(H2(`Activity B – Image pre-processing`));
K.push(P(`Activity B turns raw images into calibrated, aligned images on one common grid (Figure ${F('preproc')}).`));
K.push(...fig2('preproc', 'g02_preproc.png', `Flow chart of Activity B (Steps B1–B5).`, 540));
K.push(H3(`Step B1 – Radiometric calibration`));
K.push(...tab2('sb1', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Raw digital numbers depend on illumination and camera settings and cannot be compared between dates or cameras.`],
[`Input`, `Raw images; panel images; sunlight-sensor records; air temperature and humidity.`],
[`Output → next step`, `Reflectance images (hyperspectral, multispectral), consistent RGB images and temperature images → Step B2.`]], [2200, 7106], `Step B1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Hyperspectral and multispectral: convert digital numbers to reflectance with the empirical line method using the panels imaged before and after each flight; correct illumination changes during the flight with the downwelling sunlight sensor.`));
K.push(NL(`Red–green–blue: fixed exposure and white balance on all dates; colour values are used as relative values (colour indices are ratios, so they are not affected by overall brightness).`));
K.push(NL(`Thermal: convert radiance to temperature with emissivity 0.98 and the air temperature, relative humidity and flight height of each flight.`));
K.push(P(`**Supporting studies.** Empirical line method: Smith and Milton (1999); UAV spectroscopy workflows: Aasen et al. (2018); panels before and after the flight: Yuan et al. (2025), Blasch et al. (2023), Guo et al. (2021); thermal conversion: Jones et al. (2009), Messina and Modica (2020).`));
K.push(...tab2('celine', [[`Aspect`, `Empirical line calibration`],
[`Principle (how it works)`, `A linear relation between the digital number and reflectance is fitted for each band from targets of known reflectance (panels); the relation is applied to every pixel.`],
[`Problem it solves`, `Removes the effect of sun angle, atmosphere and camera gain, so reflectance is comparable between dates.`],
[`Specification in this study`, `Two or more panels of known reflectance (for example 5%, 20%, 50%) imaged before and after each flight; one linear fit per band and flight.`],
[`Hyper-parameters and how they are tuned`, `No hyper-parameters; the panel reflectances must be certified and the panels must fill many pixels.`],
[`Data on which it works well`, `Low-altitude UAV images under stable sky, where the atmosphere between camera and ground is thin.`],
[`Why it was selected`, `Simple, standard and accurate for UAV data; used in almost all UAV disease studies.`],
[`Key references`, `Smith and Milton (1999); Aasen et al. (2018)`]], [2300, 7006], `Method card – Empirical line calibration.`, 16));
K.push(H3(`Step B2 – Orthomosaics and georeferencing`));
K.push(...tab2('sb2', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Single frames must be joined into one map per camera and date with correct ground coordinates.`],
[`Input`, `Calibrated frames; ground control points.`],
[`Output → next step`, `Georeferenced orthomosaics and georectified hyperspectral cubes → Steps B3 and B4.`]], [2200, 7106], `Step B2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Build orthomosaics of the frame cameras (multispectral, red–green–blue, thermal) by structure-from-motion.`));
K.push(NL(`Georectify the push-broom hyperspectral lines with the position and attitude data of the UAV.`));
K.push(NL(`Use the same ground control points on every date so that all dates share one coordinate frame.`));
K.push(P(`**Supporting studies.** Georeferenced UAV hyperspectral mosaics: Guo et al. (2021), Ma et al. (2026); mosaicking of RGB, multispectral and thermal frames before feature extraction: Maimaitijiang et al. (2020), Feng et al. (2022).`));
K.push(H3(`Step B3 – Hyperspectral cube quality control and smoothing`));
K.push(...tab2('sb3', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Water-vapour absorption, detector edges and random noise make some bands unusable and add noise to the others.`],
[`Input`, `Georectified 613-band cube of each date.`],
[`Output → next step`, `Clean 483-band reflectance cube → Step B4.`]], [2200, 7106], `Step B3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Remove the water-vapour regions (1335–1460 nm and 1785–1965 nm) and the noisy ends, giving 483 bands from 399 to 2398 nm; drop the three isolated bands at 916–920 nm (detector edge).`));
K.push(NL(`Smooth every spectrum with a Savitzky–Golay filter (window 5 bands, second-order polynomial) separately on each continuous band segment, never across a removed region.`));
K.push(NL(`Check that reflectance is between 0 and 1.`));
K.push(P(`**Supporting studies.** Removal of water-vapour bands: Thenkabail et al. (2004); Savitzky–Golay smoothing: Savitzky and Golay (1964), Schafer (2011); used before derivatives by Tsai and Philpot (1998) and in disease studies by Tian et al. (2021) and Mustafa et al. (2023).`));
K.push(...tab2('csg', [[`Aspect`, `Savitzky–Golay smoothing filter`],
[`Principle (how it works)`, `A low-order polynomial is fitted by least squares to a moving window of bands; the centre value of the fitted polynomial replaces the measured value.`],
[`Problem it solves`, `Reduces random noise while keeping the shape and position of absorption features; prepares spectra for the first derivative.`],
[`Specification in this study`, `Window of 5 bands (about 15–20 nm), polynomial order 2, applied on each continuous segment.`],
[`Hyper-parameters and how they are tuned`, `Window length and polynomial order; chosen by visual check of the red edge and by the noise of the first derivative on panel pixels (a longer window smooths more but flattens narrow features).`],
[`Data on which it works well`, `Densely sampled spectra with random noise, such as hyperspectral reflectance.`],
[`Why it was selected`, `Keeps peaks better than a moving average; standard before derivatives.`],
[`Key references`, `Savitzky and Golay (1964); Schafer (2011); Rinnan et al. (2009)`]], [2300, 7006], `Method card – Savitzky–Golay smoothing filter.`, 16));
K.push(H3(`Step B4 – Projection and co-registration`));
K.push(...tab2('sb4', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Images of different cameras do not overlap exactly; small shifts mix canopy and soil values at the edges of rows.`],
[`Input`, `Georeferenced images of all cameras for one date.`],
[`Output → next step`, `All images in one projection and aligned to the hyperspectral image → Step B5.`]], [2200, 7106], `Step B4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Project every image to WGS 84 / UTM zone 43N so that distances are in metres.`));
K.push(NL(`Register the red–green–blue, multispectral and thermal images to the hyperspectral image with tie points (plot corners, markers) and a first- or second-order polynomial transformation.`));
K.push(NL(`Accept the registration when the root-mean-square error of independent check points is below one hyperspectral pixel (2.2 cm).`));
K.push(P(`**Supporting studies.** Image registration: Zitová and Flusser (2003); polynomial warping: Richards (2013); co-registered multi-camera UAV layers: Maimaitijiang et al. (2020), Feng et al. (2022).`));
K.push(H3(`Step B5 – Resampling to the hyperspectral grid`));
K.push(...tab2('sb5', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The cameras have different pixel sizes (about 0.8, 2, 2.2 and 3.9 cm); one grid is needed so that one pixel is the same ground point in every layer.`],
[`Input`, `Co-registered images.`],
[`Output → next step`, `All layers on the 2.2 cm hyperspectral grid → vegetation mask (Activity C) and subplot values (Activity D).`]], [2200, 7106], `Step B5 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Red–green–blue (finer): pixel aggregate, so each new pixel is the mean of the pixels it covers.`));
K.push(NL(`Multispectral (similar size): bilinear interpolation.`));
K.push(NL(`Thermal (coarser): nearest neighbour, which keeps the measured temperatures.`));
K.push(NL(`Compute red–green–blue texture before resampling, at native resolution, because resampling removes fine texture.`));
K.push(P(`**Supporting studies.** Resampling methods: Richards (2013); resampling of UAV hyperspectral images to other resolutions: Guo et al. (2021); pixel aggregation between UAV and satellite grids: Revill et al. (2020), Yuan et al. (2025); common-grid stacking of RGB, multispectral and thermal data: Maimaitijiang et al. (2020).`));
K.push(...tab2('cresample', [[`Aspect`, `Resampling (pixel aggregate, bilinear, nearest neighbour)`],
[`Principle (how it works)`, `Pixel aggregate averages all fine pixels inside a coarse pixel; bilinear interpolation weights the four nearest pixels by distance; nearest neighbour copies the value of the closest pixel.`],
[`Problem it solves`, `Places all cameras on one grid so that one mask and one set of subplot polygons can be used.`],
[`Specification in this study`, `Target grid: 2.2 cm hyperspectral grid; method chosen by the direction of the change in pixel size (finer → aggregate; similar → bilinear; coarser → nearest neighbour).`],
[`Hyper-parameters and how they are tuned`, `No tuning; the choice follows the rule above.`],
[`Data on which it works well`, `Aggregate: going to a coarser grid; nearest neighbour: preserving measured values such as temperature.`],
[`Why it was selected`, `Avoids aliasing when coarsening and avoids inventing new temperatures when refining.`],
[`Key references`, `Richards (2013); Guo et al. (2021)`]], [2300, 7006], `Method card – Resampling (pixel aggregate, bilinear, nearest neighbour).`, 16));
K.push(H2(`Activity C – Endmember extraction and vegetation mask`));
K.push(P(`Soil, grass, weeds and shadow inside a subplot change reflectance, texture and temperature and must be removed before disease features are extracted. Activity C builds one field-wide library of pure spectra (endmembers) with the hourglass workflow, classifies every pixel with the spectral angle mapper and keeps the canopy pixels (Figure ${F('endmember')}). Flowers are kept because the canopy score includes the inflorescence; no spectral unmixing is done.`));
K.push(...fig2('endmember', 'g03_endmember.png', `Flow chart of Activity C: endmember extraction (Steps C1–C5) and vegetation mask (Steps C6–C8).`, 540));
K.push(H3(`Step C1 – Sampling of pixels from all dates`));
K.push(...tab2('sc1', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Endmember extraction on every full image would be slow, and endmembers extracted separately for each date or plot would not be comparable.`],
[`Input`, `Clean hyperspectral cubes of all dates (Step B3).`],
[`Output → next step`, `One pooled pixel sample (for example 20 000 pixels from each date) → Step C2.`]], [2200, 7106], `Step C1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Draw a random sample of pixels from inside the field on every date, so that early green canopy, diseased canopy, flowering canopy, soil, grass and shadow are all represented.`));
K.push(NL(`Add pixels of the reference panels and known soil and grass patches to make sure these classes are present.`));
K.push(P(`**Supporting studies.** One library for the whole scene gives the same classes in every plot and on every date (Bioucas-Dias et al., 2012); pooled samples for the hourglass workflow: Boardman and Kruse (2011).`));
K.push(H3(`Step C2 – Minimum noise fraction (MNF) transformation`));
K.push(...tab2('sc2', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Hyperspectral bands are noisy and highly correlated; the corners of the pixel cloud, where pure pixels lie, are hidden by noise.`],
[`Input`, `Pooled pixel sample (483 bands).`],
[`Output → next step`, `Minimum noise fraction (MNF) components ordered by signal-to-noise ratio; components with eigenvalues clearly above 1 → Step C3.`]], [2200, 7106], `Step C2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Estimate the noise from the differences between neighbouring pixels (shift difference) in a homogeneous area.`));
K.push(NL(`Whiten the noise (rescale so the noise has unit variance in every direction) and then apply principal component analysis.`));
K.push(NL(`Plot the eigenvalues (Figure ${F('dummyem')}a); keep the components whose eigenvalue is clearly above 1 (here about 8–10); components with eigenvalues near 1 contain only noise.`));
K.push(P(`**Supporting studies.** Green et al. (1988); Boardman and Kruse (2011); Bioucas-Dias et al. (2012).`));
K.push(...tab2('cmnf', [[`Aspect`, `Minimum noise fraction (MNF) transformation`],
[`Principle (how it works)`, `Two principal component analyses in sequence: the first whitens the noise, the second orders the components by signal-to-noise ratio. Eigenvalue 1 means a component is pure noise.`],
[`Problem it solves`, `Separates signal from noise and reduces 483 correlated bands to about 10 informative components.`],
[`Specification in this study`, `Noise from shift differences in a homogeneous field area; components with eigenvalue above about 2 kept.`],
[`Hyper-parameters and how they are tuned`, `Number of components kept: chosen from the eigenvalue plot (the "knee" where values approach 1).`],
[`Data on which it works well`, `Hyperspectral images with many correlated, noisy bands.`],
[`Why it was selected`, `Unlike plain principal component analysis, it ranks components by image quality, not by variance (which can be dominated by noise or illumination).`],
[`Key references`, `Green et al. (1988); Boardman and Kruse (2011)`]], [2300, 7006], `Method card – Minimum noise fraction (MNF) transformation.`, 16));
K.push(H3(`Step C3 – Pixel purity index (PPI)`));
K.push(...tab2('sc3', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Among thousands of pixels, the few spectrally pure pixels (one material only) must be found.`],
[`Input`, `Selected MNF components of the pixel sample.`],
[`Output → next step`, `Pixel purity index (PPI) image: count of how often each pixel was an extreme → Step C4.`]], [2200, 7106], `Step C3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Project the MNF pixel cloud onto many random unit vectors ("skewers"), for example 10 000.`));
K.push(NL(`On each skewer, record the pixels at the two extreme ends; add one to their count.`));
K.push(NL(`Keep pixels with high counts (for example at least 10) as pure-pixel candidates.`));
K.push(P(`**Supporting studies.** Boardman et al. (1995); Boardman and Kruse (2011); Bioucas-Dias et al. (2012).`));
K.push(...tab2('cppi', [[`Aspect`, `Pixel purity index (PPI)`],
[`Principle (how it works)`, `In a cloud of mixed pixels, pure pixels lie at the corners (vertices). A random projection puts corner pixels at its ends; pixels that are repeatedly at the ends are pure.`],
[`Problem it solves`, `Finds candidate endmember pixels without prior knowledge.`],
[`Specification in this study`, `10 000 skewers on the kept MNF components; threshold of 10 hits.`],
[`Hyper-parameters and how they are tuned`, `Number of skewers (more = more stable; 5000–20 000 usual) and the threshold (2–3 times the noise level); fixed after checking that the candidate set no longer changes.`],
[`Data on which it works well`, `Scenes with some pure pixels of each material; high spatial resolution (2.2 cm) makes pure canopy and soil pixels common.`],
[`Why it was selected`, `Simple, transparent and part of the standard hourglass workflow; candidates are checked visually in the next step.`],
[`Key references`, `Boardman et al. (1995); Boardman and Kruse (2011)`]], [2300, 7006], `Method card – Pixel purity index (PPI).`, 16));
K.push(H3(`Step C4 – n-dimensional visualisation and endmember selection`));
K.push(...tab2('sc4', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `PPI candidates form clusters; each cluster corner must be turned into one endmember spectrum.`],
[`Input`, `Pure-pixel candidates in MNF space.`],
[`Output → next step`, `Endmember spectra (mean reflectance of each cluster) → Step C5.`]], [2200, 7106], `Step C4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Display the candidates in two- and three-dimensional scatter plots of MNF components and rotate them (n-dimensional visualiser).`));
K.push(NL(`Mark the clusters at the corners of the cloud (Figure ${F('dummyem')}b).`));
K.push(NL(`Compute the endmember spectrum as the mean reflectance (original bands) of the pixels in each cluster.`));
K.push(P(`**Supporting studies.** Boardman and Kruse (2011); Bioucas-Dias et al. (2012).`));
K.push(H3(`Step C5 – Endmember identification and library`));
K.push(...tab2('sc5', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Endmembers must be named before they can be used to build a mask.`],
[`Input`, `Endmember spectra; field photographs; red–green–blue images; leaf spectra of the study.`],
[`Output → next step`, `Labelled endmember library (green canopy, stressed canopy, flower, soil, grass, shadow) → Step C6.`]], [2200, 7106], `Step C5 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Locate the pixels of each endmember in the red–green–blue image and in field photographs.`));
K.push(NL(`Compare their shapes with known spectra: green canopy (red edge, high near-infrared), stressed canopy (higher red, lower near-infrared), yellow flower (high green–red reflectance), soil (rising, featureless), shadow (low everywhere) (Figure ${F('dummyem')}c).`));
K.push(NL(`Merge duplicates and store the final library.`));
K.push(P(`**Supporting studies.** Identification by spectral shape and image context: Boardman and Kruse (2011); flowers in Brassica canopies: Sulik and Long (2016).`));
K.push(...fig2('dummyem', 'g12_dummy_endmember.png', `Dummy example of endmember extraction: (a) MNF eigenvalues; (b) pure pixels at the corners of the MNF cloud; (c) endmember library.`, 560));
K.push(H3(`Step C6 – Spectral angle mapper (SAM) classification`));
K.push(...tab2('sc6', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Every pixel of every date must be assigned to one class.`],
[`Input`, `Labelled endmember library; clean cubes of all dates.`],
[`Output → next step`, `Class map of every date → Step C7.`]], [2200, 7106], `Step C6 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Compute the spectral angle between each pixel spectrum and each endmember (equation below).`));
K.push(NL(`Assign the pixel to the endmember with the smallest angle; leave it unclassified if the smallest angle is larger than the threshold.`));
K.push(NL(`Calibrate the threshold (0.10, 0.20 or 0.30 radian tested) on labelled reference pixels.`));
K.push(P(`**Supporting studies.** Kruse et al. (1993); spectral angle mapper for crop masks in UAV hyperspectral studies: Guo et al. (2021).`));
K.push(EQ(`α = cos^{−1} [ Σ_{i} t_{i} r_{i} / ( √(Σ_{i} t_{i}^{2}) √(Σ_{i} r_{i}^{2}) ) ]`));
K.push(P(`Here t is the pixel spectrum, r the endmember spectrum and i the band. Because the angle does not depend on the length of the spectra, a shaded canopy pixel and a sunlit canopy pixel have almost the same angle to the canopy endmember.`));
K.push(...tab2('samex', [[`Spectrum (4 bands, dummy)`, `Blue`, `Green`, `Red`, `Near-infrared`, `Angle to pixel (radian)`],
[`Pixel t`, `0.05`, `0.08`, `0.06`, `0.45`, `—`],
[`Green canopy endmember`, `0.04`, `0.09`, `0.05`, `0.50`, `0.044 (smallest → canopy)`],
[`Yellow flower endmember`, `0.06`, `0.20`, `0.22`, `0.40`, `0.424`],
[`Soil endmember`, `0.10`, `0.14`, `0.18`, `0.25`, `0.550`]], [2600, 900, 900, 900, 1300, 2706], `Worked example (dummy data): spectral angle mapper classification of one pixel.`, 17));
K.push(...fig2('dummysam', 'g13_dummy_sam.png', `Dummy example: (a) the spectral angle α between a pixel and an endmember; (b) class map and the resulting vegetation mask.`, 520));
K.push(...tab2('csam', [[`Aspect`, `Spectral angle mapper (SAM)`],
[`Principle (how it works)`, `Treats each spectrum as a vector and measures the angle between two vectors; small angle = similar shape.`],
[`Problem it solves`, `Classifies pixels by spectral shape, so it is insensitive to brightness differences caused by shading and slope.`],
[`Specification in this study`, `Endmember library from Step C5; maximum angle 0.10–0.30 radian (calibrated); one classification per date.`],
[`Hyper-parameters and how they are tuned`, `Maximum angle: the value with the highest overall accuracy on reference pixels.`],
[`Data on which it works well`, `Hyperspectral data with distinct class shapes (vegetation, soil, shadow, flowers).`],
[`Why it was selected`, `Needs only one spectrum per class, works with the endmember library directly and is robust to illumination.`],
[`Key references`, `Kruse et al. (1993); Bioucas-Dias et al. (2012)`]], [2300, 7006], `Method card – Spectral angle mapper (SAM).`, 16));
K.push(H3(`Step C7 – Vegetation mask rule and edge erosion`));
K.push(...tab2('sc7', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Some flower pixels have low NDVI, and pixels at the edge of leaves are mixtures of canopy and soil.`],
[`Input`, `Class map; normalised difference vegetation index (NDVI) image.`],
[`Output → next step`, `Binary vegetation mask (1 = green canopy, stressed canopy, flower; 0 = soil, grass, shadow, unclassified) → Step C8 and Activity D.`]], [2200, 7106], `Step C7 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Keep the classes green canopy, stressed canopy and flower; remove soil, grass, shadow and unclassified pixels.`));
K.push(NL(`Apply the rule: vegetation = (NDVI > 0.6 OR flower class) AND a kept class; NDVI alone would remove yellow flowers.`));
K.push(NL(`Apply a one-pixel morphological erosion to remove mixed edge pixels.`));
K.push(P(`**Supporting studies.** NDVI: Rouse et al. (1974); NDVI threshold masks in UAV disease studies: Guo et al. (2021) (NDVI > 0.42); morphological erosion: Soille (2003); flowers and canopy spectra: Sulik and Long (2016).`));
K.push(H3(`Step C8 – Mask accuracy and transfer to all cameras`));
K.push(...tab2('sc8', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The mask must be shown to be accurate and must be applied identically to all cameras.`],
[`Input`, `Vegetation mask; independent reference pixels from the red–green–blue image.`],
[`Output → next step`, `Accepted mask on the hyperspectral grid, applied to the multispectral, red–green–blue and thermal layers → Activity D.`]], [2200, 7106], `Step C8 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Digitise independent reference pixels of each class on the red–green–blue image (for example 300 per class).`));
K.push(NL(`Compute the confusion matrix, overall accuracy and kappa coefficient; accept the mask when overall accuracy is at least 90%.`));
K.push(NL(`Multiply every resampled layer of every camera by the mask, so all cameras are measured on the same pixels.`));
K.push(P(`**Supporting studies.** Accuracy assessment: Congalton (1991); same pixels for all sensors after masking: Feng et al. (2022), Maimaitijiang et al. (2020).`));
K.push(...tab2('cerosion', [[`Aspect`, `Morphological erosion and mask accuracy assessment`],
[`Principle (how it works)`, `Erosion removes the outer pixel ring of each vegetation patch; the confusion matrix compares mask classes with reference classes.`],
[`Problem it solves`, `Removes mixed edge pixels and proves that the mask is reliable.`],
[`Specification in this study`, `Erosion with a 3 × 3 structuring element (one pixel); reference pixels from the red–green–blue image; overall accuracy ≥ 90% required.`],
[`Hyper-parameters and how they are tuned`, `Size of the structuring element (one pixel to avoid losing small plants).`],
[`Data on which it works well`, `High-resolution masks with many leaf edges.`],
[`Why it was selected`, `Simple and widely used; accuracy assessment is required to report a mask.`],
[`Key references`, `Soille (2003); Congalton (1991)`]], [2300, 7006], `Method card – Morphological erosion and mask accuracy assessment.`, 16));
K.push(H2(`Activity D – Subplot spectra and feature extraction`));
K.push(P(`Features are calculated for every subplot-date and kept in groups by type (Figure ${F('features')}). The grouping matters because one selection method is later used for each type of feature (Objective 1).`));
K.push(...fig2('features', 'g04_features.png', `Flow chart of Activity D (Steps D1–D6; Steps D7–D8 complete the feature table).`, 540));
K.push(H3(`Step D1 – Plot and subplot polygons`));
K.push(...tab2('sd1', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Each sample must cover exactly the scored subplot.`],
[`Input`, `Field layout; plot numbers; aligned images.`],
[`Output → next step`, `192 subplot polygons with codes → Step D2.`]], [2200, 7106], `Step D1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Digitise the 48 plot polygons once and add the plot number.`));
K.push(NL(`Split each plot into four quadrant subplots that match the field scoring; apply an inner buffer to exclude border rows and bunds.`));
K.push(NL(`Use the same polygons on all dates and for all cameras.`));
K.push(P(`**Supporting studies.** Plot polygons after soil masking: Liu et al. (2024), Feng et al. (2022); fixed sampling regions: Ma et al. (2026).`));
K.push(H3(`Step D2 – Subplot mean spectra`));
K.push(...tab2('sd2', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Models need one value per feature and subplot that represents the scored canopy.`],
[`Input`, `Masked layers of all cameras; subplot polygons.`],
[`Output → next step`, `One mean spectrum (and mean band values) per subplot, date and camera; vegetation pixel count, flower % and canopy cover % → Steps D3–D7 and Activity E.`]], [2200, 7106], `Step D2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Average the masked vegetation pixels inside each subplot for every band of every camera.`));
K.push(NL(`Save the number of vegetation pixels, the flower % and the canopy cover % (from the class map) as quality and confounding checks.`));
K.push(P(`**Supporting studies.** Plot-mean spectra after masking: Guo et al. (2021), Mustafa et al. (2023), Ma et al. (2026).`));
K.push(...fig2('dummyspec', 'g11_dummy_spectra.png', `Dummy example of subplot mean spectra by severity grade (a) and the first derivative in the red-edge region (b). The water-vapour regions are removed.`, 560));
K.push(H3(`Step D3 – Hyperspectral spectral features`));
K.push(...tab2('sd3', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Reflectance alone does not show red-edge shifts clearly; derivatives and red-edge parameters make them visible.`],
[`Input`, `Subplot mean reflectance (483 bands).`],
[`Output → next step`, `Spectral group: reflectance (483), first derivative (483) and red-edge parameters → Objective 1 (Activities 1.2 and 1.4).`]], [2200, 7106], `Step D3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Reflectance of the 483 bands.`));
K.push(NL(`First derivative of each smoothed segment: FD(λ_{i}) = [R(λ_{i+1}) − R(λ_{i−1})] / (λ_{i+1} − λ_{i−1}); derivative bands within 10 nm of a removed region are not used.`));
K.push(NL(`Red-edge parameters: red-edge position (wavelength of the maximum first derivative between 680 and 760 nm), red-edge amplitude (that maximum value) and red-edge area (sum of the first derivative from 680 to 760 nm).`));
K.push(NL(`The second derivative is not used, because it amplifies noise at UAV signal-to-noise levels and adds hundreds of unstable variables.`));
K.push(P(`**Supporting studies.** Derivative analysis: Tsai and Philpot (1998); red edge: Horler et al. (1983), Filella and Peñuelas (1994); red-edge parameters best for the early stage of pine wilt disease from UAV hyperspectral data: Yu et al. (2021); noise amplification by derivatives: Rinnan et al. (2009).`));
K.push(P(`**Worked example (dummy data).** If R(700 nm) = 0.10 and R(704 nm) = 0.14, the first derivative at 702 nm is (0.14 − 0.10) / 4 = 0.010 nm^{−1}. If the largest first derivative between 680 and 760 nm is 0.012 nm^{−1} at 718 nm, the red-edge position is 718 nm and the amplitude is 0.012 nm^{−1}. In diseased canopies the red-edge position moves to shorter wavelengths (Figure ${F('dummyspec')}b).`));
K.push(...tab2('cfd', [[`Aspect`, `First derivative and red-edge parameters`],
[`Principle (how it works)`, `The derivative measures the slope of the spectrum; it removes constant offsets (for example brightness differences) and turns the red edge into a peak whose position and height can be measured.`],
[`Problem it solves`, `Makes the chlorophyll-related red-edge shift measurable and reduces background effects.`],
[`Specification in this study`, `Central difference on Savitzky–Golay smoothed segments; red-edge position, amplitude and area from 680–760 nm.`],
[`Hyper-parameters and how they are tuned`, `No tuning; the smoothing window (Step B3) controls the noise of the derivative.`],
[`Data on which it works well`, `Smoothed hyperspectral spectra with dense band spacing.`],
[`Why it was selected`, `Red-edge parameters were the best features for separating early-stage diseased trees from healthy trees (Yu et al., 2021).`],
[`Key references`, `Tsai and Philpot (1998); Filella and Peñuelas (1994); Yu et al. (2021)`]], [2300, 7006], `Method card – First derivative and red-edge parameters.`, 16));
K.push(H3(`Step D4 – Vegetation indices`));
K.push(...tab2('sd4', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `General physiological changes (pigments, structure, water) are captured best by published indices that have known meaning.`],
[`Input`, `Subplot mean reflectance.`],
[`Output → next step`, `Index group (published indices + red-edge parameters; the searched indices of Activity 1.3 are added later) → Activity 1.4.`]], [2200, 7106], `Step D4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Compute the published indices in five groups: pigment (for example PRI, ARI, CARI, MCARI, PSRI, PSSRb), structure (NDVI, OSAVI, SR, RVI, MSR), red edge (NDRE, MTCI, CIrededge, CIgreen, RVSI), water (NDWI, MSI, NDII, WBI) and disease (DWSI, RBI); the indices used by Ma et al. (2026) are all included.`));
K.push(NL(`Check every formula against the original paper and use the nearest available band.`));
K.push(NL(`Index definitions are given in Chapter 7 (Table ${T('hsidx')}).`));
K.push(P(`**Supporting studies.** Index groups for disease detection: Mahlein et al. (2013), Huang et al. (2014), Ma et al. (2026); pigment indices: Gamon et al. (1992), Gitelson et al. (2003), Merzlyak et al. (1999); water and disease indices: Gao (1996), Apan et al. (2004); PSRI and PSSRb for rice bacterial leaf blight: Das et al. (2015).`));
K.push(...tab2('cvi', [[`Aspect`, `Vegetation indices`],
[`Principle (how it works)`, `Arithmetic combinations (differences, ratios, normalised differences) of reflectance at wavelengths sensitive to a plant property, which cancel part of the illumination and background effect.`],
[`Problem it solves`, `Turns many bands into a few physiologically meaningful variables that can be compared with other studies and sensors.`],
[`Specification in this study`, `About 48 published hyperspectral indices, 12 multispectral indices and 6 colour indices (Chapter 7).`],
[`Hyper-parameters and how they are tuned`, `No hyper-parameters; formulas fixed by the original papers.`],
[`Data on which it works well`, `Canopy reflectance at UAV and satellite scales.`],
[`Why it was selected`, `Interpretable, transferable and easy to apply to cheaper sensors.`],
[`Key references`, `Mahlein et al. (2013); Huang et al. (2014); Ma et al. (2026)`]], [2300, 7006], `Method card – Vegetation indices.`, 16));
K.push(H3(`Step D5 – Texture features from the grey-level co-occurrence matrix (GLCM)`));
K.push(...tab2('sd5', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `White pustules and chlorotic patches make the canopy surface heterogeneous; spectra do not record this spatial pattern.`],
[`Input`, `Masked hyperspectral cube; red–green–blue image at native resolution; multispectral and thermal layers.`],
[`Output → next step`, `Texture groups of each camera → Activity 1.5 (hyperspectral) and Activity 1.6 (other cameras).`]], [2200, 7106], `Step D5 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Hyperspectral: reduce the cube with principal component analysis and keep the first three components (cumulative variance above 95%); compute texture on these three component images (Activity 1.5).`));
K.push(NL(`For every image used, quantise the grey levels to 32 levels and compute the grey-level co-occurrence matrix (GLCM) in a 3 × 3 moving window at distance 1, averaged over four directions (0°, 45°, 90°, 135°).`));
K.push(NL(`Compute eight texture measures: mean, variance, homogeneity, contrast, dissimilarity, entropy, second moment and correlation; average them over the vegetation pixels of the subplot.`));
K.push(NL(`Red–green–blue: texture of the R, G and B bands (24 features); multispectral: texture of the five bands (40); thermal: texture of the temperature image (8).`));
K.push(P(`**Supporting studies.** GLCM: Haralick et al. (1973), Hall-Beyer (2017); texture from principal-component images of UAV hyperspectral data: Guo et al. (2021), Ma et al. (2026); texture as a feature group for Fusarium head blight: Liu et al. (2020).`));
K.push(...tab2('glcmex', [[`Image row`, `Grey levels of the 4 × 4 image`, `GLCM counts (grey levels 0–3)`, `Texture measure`, `Value`],
[`1`, `0 0 1 1`, `4 2 1 0`, `contrast`, `0.583`],
[`2`, `0 0 1 1`, `2 4 0 0`, `homogeneity`, `0.808`],
[`3`, `0 2 2 2`, `1 0 6 1`, `dissimilarity`, `0.417`],
[`4`, `2 2 3 3`, `0 0 1 2`, `entropy`, `2.095`],
[``, ``, `24 neighbour pairs in total`, `second moment`, `0.146`]], [1300, 2300, 2500, 1900, 1306], `Worked example (dummy data): grey-level co-occurrence matrix (horizontal neighbours, both directions) and texture of a small image. Each count is divided by 24 to give probabilities before the measures are computed.`, 17));
K.push(...tab2('cglcm', [[`Aspect`, `Grey-level co-occurrence matrix (GLCM) texture`],
[`Principle (how it works)`, `Counts how often pairs of grey levels occur next to each other; statistics of this matrix describe smoothness (homogeneity), local variation (contrast, dissimilarity), disorder (entropy) and uniformity (second moment).`],
[`Problem it solves`, `Describes the spatial pattern of pustules, chlorotic patches and canopy gaps, which spectra cannot.`],
[`Specification in this study`, `32 grey levels, 3 × 3 window, distance 1, four directions averaged, eight measures, averaged over vegetation pixels.`],
[`Hyper-parameters and how they are tuned`, `Window size, distance and number of grey levels; fixed at small values because pustules are only a few pixels wide at 2.2 cm; 5 × 5 window is tested as a check.`],
[`Data on which it works well`, `High-resolution images where the target produces a spatial pattern (2–5 cm pixels).`],
[`Why it was selected`, `The most widely used and best-understood texture method in remote sensing; used in the main white-rust-like disease studies.`],
[`Key references`, `Haralick et al. (1973); Hall-Beyer (2017); Guo et al. (2021)`]], [2300, 7006], `Method card – Grey-level co-occurrence matrix (GLCM) texture.`, 16));
K.push(...tab2('cpca', [[`Aspect`, `Principal component analysis (PCA)`],
[`Principle (how it works)`, `Rotates correlated variables into uncorrelated components ordered by the variance they explain.`],
[`Problem it solves`, `Reduces 483 correlated bands to three images that keep most of the information, so texture is computed on 3 images instead of 483.`],
[`Specification in this study`, `Computed on the masked vegetation pixels of all dates (training data); first three components kept (cumulative variance above 95%).`],
[`Hyper-parameters and how they are tuned`, `Number of components: the smallest number with at least 95% cumulative variance (Figure ${F('dummyrelief')}b).`],
[`Data on which it works well`, `Many highly correlated variables, such as hyperspectral bands.`],
[`Why it was selected`, `Used in exactly this role by Guo et al. (2021) and Ma et al. (2026).`],
[`Key references`, `Jolliffe and Cadima (2016); Guo et al. (2021); Ma et al. (2026)`]], [2300, 7006], `Method card – Principal component analysis (PCA).`, 16));
K.push(H3(`Step D6 – Multispectral and red–green–blue features`));
K.push(...tab2('sd6', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The cheaper cameras need their own features so that their value can be compared with the hyperspectral camera.`],
[`Input`, `Masked subplot means of the multispectral and red–green–blue images.`],
[`Output → next step`, `Multispectral group (5 bands, 12 indices, 10 two-band normalised differences, 40 texture features) and colour group (6 colour indices, hue–saturation–value means, 24 texture features) → Activity 1.6.`]], [2200, 7106], `Step D6 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Multispectral: band reflectance, NDVI, GNDVI, NDRE, CIgreen, CIrededge, MTCI, OSAVI, SAVI, TCARI, MCARI, MSR, PSRI and the ten normalised differences of the five bands.`));
K.push(NL(`Red–green–blue: excess green, excess red, excess green minus excess red, VARI, GLI, NGRDI and mean hue, saturation and value.`));
K.push(NL(`Formulas are in Chapter 7.`));
K.push(P(`**Supporting studies.** Multispectral indices and texture for wheat powdery mildew: Liu et al. (2024); multispectral and very-high-resolution indices for wheat rusts: Blasch et al. (2023); colour indices: Woebbecke et al. (1995), Meyer and Neto (2008).`));
K.push(H3(`Step D7 – Thermal features`));
K.push(...tab2('sd7', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Infection changes transpiration and canopy temperature, but temperature also changes with weather and time.`],
[`Input`, `Masked thermal subplot values; air temperature; healthy-plot temperatures of the same date.`],
[`Output → next step`, `Thermal group → Activity E (normalisation) and Activity 1.6.`]], [2200, 7106], `Step D7 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Canopy temperature: mean, median, standard deviation, 10th and 90th percentiles of the vegetation pixels.`));
K.push(NL(`Normalised thermal features (Step E2): canopy minus air temperature, normalised relative canopy temperature, crop water stress index and difference from the healthy plots of the same date and variety.`));
K.push(NL(`Thermal texture (Step D5).`));
K.push(P(`**Supporting studies.** Thermal features for powdery mildew: Feng et al. (2022), Liu et al. (2024); canopy minus air temperature for downy mildew from a UAV: Calderón et al. (2014); reviews: Pineda et al. (2021), Messina and Modica (2020).`));
K.push(H3(`Step D8 – Feature table`));
K.push(...tab2('sd8', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `All later steps need one table layout for every camera so that sensor sets are simple joins.`],
[`Input`, `Features of Steps D3–D7.`],
[`Output → next step`, `One table per camera with identifiers, labels, covariates and features → Activities E and F.`]], [2200, 7106], `Step D8 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Columns: identifiers (date, days after inoculation, plot, subplot, replication, treatment, variety, inoculation timing, fold), labels (score, class, detection label), covariates (vegetation pixel count, flower %, canopy cover %) and features with a group prefix (R_, FD_, RE_, VI_, TX_, TH_).`));
K.push(NL(`Rows: one per subplot-date.`));
K.push(P(`**Supporting studies.** Structured multi-sensor feature tables: Maimaitijiang et al. (2020), Feng et al. (2022).`));
K.push(...tab2('featcount', [[`Camera`, `Feature groups`, `Approximate number`],
[`Hyperspectral`, `reflectance 483, first derivative 483, red-edge parameters 3, published indices about 48, principal-component texture 24 (+ searched indices and TTFI)`, `≈ 1040`],
[`Multispectral`, `5 bands, 12 indices, 10 normalised differences, 40 texture`, `67`],
[`Red–green–blue`, `6 colour indices, 3 colour means, 24 texture`, `33`],
[`Thermal`, `5 temperature statistics, 4 normalised temperatures, 8 texture`, `17`],
[`Covariates`, `flower %, canopy cover %, vegetation pixel count, days after inoculation, variety, inoculation timing`, `not used as disease features`]], [1800, 5600, 1906], `Feature groups before selection.`, 17));
K.push(H2(`Activity E – Normalisation and data preparation`));
K.push(P(`Normalisation removes effects that are not caused by the disease (illumination, weather, date, variety, units) and prepares the features for the models (Figure ${F('normal')}). Steps E1–E2 and E4 are done once on all data because they do not use the labels; Steps E3, E5 and E6 use statistics that are computed on the training part of each fold only.`));
K.push(...fig2('normal', 'g25_normalisation.png', `Flow chart of Activity E (Steps E1–E6).`, 540));
K.push(H3(`Step E1 – Radiometric consistency between dates`));
K.push(...tab2('se1', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Even after calibration, small differences between flights (panel shading, haze, sensor drift) can look like a disease effect when dates are pooled.`],
[`Input`, `Reflectance images of all dates; invariant targets.`],
[`Output → next step`, `Checked reflectance on all dates (re-calibrated where needed) → Activity D.`]], [2200, 7106], `Step E1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Place the calibration panels on every flight and record their reflectance in every image.`));
K.push(NL(`Compare the reflectance of invariant targets (panels, concrete, bare road) between dates; differences above 5% in any band flag the date.`));
K.push(NL(`Re-calibrate a flagged date with its own panels or, if they failed, with a linear fit to the invariant targets of a reference date.`));
K.push(P(`**Supporting studies.** Panels on every flight for relative radiometric calibration: Yuan et al. (2025), Blasch et al. (2023); scaling and consistency between UAV and satellite reflectance: Revill et al. (2020); UAV spectroscopy correction workflow: Aasen et al. (2018).`));
K.push(H3(`Step E2 – Thermal normalisation`));
K.push(...tab2('se2', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Canopy temperature changes with air temperature, radiation and time of flight, which can hide the disease effect.`],
[`Input`, `Canopy temperature statistics; air temperature; wet and dry reference temperatures.`],
[`Output → next step`, `Normalised thermal features → Activity 1.6 and Objectives 2–3.`]], [2200, 7106], `Step E2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Canopy minus air temperature: CTD = T_{c} − T_{air}.`));
K.push(NL(`Normalised relative canopy temperature over the field on that date: NRCT = (T_{c} − T_{min}) / (T_{max} − T_{min}).`));
K.push(NL(`Crop water stress index: CWSI = (T_{c} − T_{wet}) / (T_{dry} − T_{wet}) with wet and dry references in the field.`));
K.push(NL(`Difference from healthy plots of the same date and variety (Step E3).`));
K.push(P(`**Supporting studies.** Normalisation of canopy temperature by air temperature: Idso et al. (1981), Pineda et al. (2021); canopy minus air temperature for downy mildew detection from a UAV: Calderón et al. (2014); thermal indices and environmental effects: Jones et al. (2009), Maes and Steppe (2012), Oerke et al. (2006).`));
K.push(P(`**Worked example (dummy data).** A subplot has T_{c} = 24.6 °C when T_{air} = 22.0 °C, so CTD = +2.6 °C. On that date the field minimum and maximum canopy temperatures are 21.8 and 26.2 °C, so NRCT = (24.6 − 21.8) / (26.2 − 21.8) = 0.64.`));
K.push(H3(`Step E3 – Healthy-plot normalisation`));
K.push(...tab2('se3', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Early disease effects are small compared with the differences caused by date, crop age and variety; a same-day, same-variety healthy reference removes most of them.`],
[`Input`, `Features of all subplots; features of the healthy plots of the same date and variety (training replications only).`],
[`Output → next step`, `Healthy-normalised features → Objective 3 (all features) and thermal difference features (Objectives 1–2).`]], [2200, 7106], `Step E3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`For every feature, date and variety, compute the mean and standard deviation of the healthy plots of the training replications.`));
K.push(NL(`Normalised value: z_{h} = (x − mean_{healthy}) / SD_{healthy}.`));
K.push(NL(`Apply the same healthy-plot reference to the test samples of that date and variety.`));
K.push(P(`**Supporting studies.** Healthy references for thermal disease detection: Oerke et al. (2006); healthy references in pre-visual detection: Zarco-Tejada et al. (2018), Poblete et al. (2023); pre-symptomatic hyperspectral detection: Zhu et al. (2017).`));
K.push(P(`**Worked example (dummy data).** On one date the healthy plots of variety V1 have mean canopy temperature 23.8 °C (standard deviation 0.4 °C). An inoculated V1 subplot at 24.6 °C gets z_{h} = (24.6 − 23.8) / 0.4 = +2.0, that is, two healthy standard deviations warmer.`));
K.push(...tab2('chealthy', [[`Aspect`, `Healthy-plot (control) normalisation`],
[`Principle (how it works)`, `Expresses each value as its distance from healthy plants measured on the same day, of the same variety and age, in units of their natural variation.`],
[`Problem it solves`, `Removes date, weather, crop-age and variety effects so that only the disease effect remains; essential when symptoms are not yet visible.`],
[`Specification in this study`, `Reference: healthy plots of the same date and variety in the training replications; mean and standard deviation per feature.`],
[`Hyper-parameters and how they are tuned`, `No hyper-parameters.`],
[`Data on which it works well`, `Experiments with healthy controls on every date; thermal and early-stage spectral data.`],
[`Why it was selected`, `Simple and directly justified by the design (one healthy plot for every treatment).`],
[`Key references`, `Oerke et al. (2006); Zarco-Tejada et al. (2018)`]], [2300, 7006], `Method card – Healthy-plot (control) normalisation.`, 16));
K.push(H3(`Step E4 – Sample quality screening`));
K.push(...tab2('se4', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Subplots with very few vegetation pixels, cloud shadow or missing data give unreliable mean spectra.`],
[`Input`, `Subplot tables with vegetation pixel count and covariates.`],
[`Output → next step`, `Clean sample list (flagged samples documented) → Activity F.`]], [2200, 7106], `Step E4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Flag subplots with fewer than 30% vegetation pixels, with cloud shadow or with missing data in any camera.`));
K.push(NL(`Check visually the spectra that lie more than three standard deviations from the mean of their date and grade.`));
K.push(NL(`Remove a sample only for a documented technical reason, never because of its label; report the number removed.`));
K.push(P(`**Supporting studies.** Quality checks of UAV spectral data: Aasen et al. (2018); data screening before modelling: Kuhn and Johnson (2013).`));
K.push(H3(`Step E5 – Standardisation (z-score) with training statistics`));
K.push(...tab2('se5', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Features have different units and ranges (reflectance 0–1, temperature 15–30 °C, texture 0–1000); distance- and gradient-based models are dominated by large-range features.`],
[`Input`, `Selected features of the training part and test part of each fold.`],
[`Output → next step`, `Standardised features (mean 0, standard deviation 1 in the training part) → all models.`]], [2200, 7106], `Step E5 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Compute the mean and standard deviation of every feature on the training part of the fold.`));
K.push(NL(`Standardise: z = (x − mean_{train}) / SD_{train}, for training and test samples alike.`));
K.push(NL(`Repeat for every fold; the test part never contributes to the statistics.`));
K.push(P(`**Supporting studies.** Pre-processing inside resampling: Kuhn and Johnson (2013); feature scaling for support vector machines and neural networks: Mountrakis et al. (2011), Kattenborn et al. (2021).`));
K.push(P(`**Worked example (dummy data).** In one training part NDVI has mean 0.72 and standard deviation 0.08. A test subplot with NDVI = 0.60 is standardised to z = (0.60 − 0.72) / 0.08 = −1.5.`));
K.push(...tab2('czscore', [[`Aspect`, `z-score standardisation`],
[`Principle (how it works)`, `Subtracts the mean and divides by the standard deviation, so every feature has mean 0 and unit variance.`],
[`Problem it solves`, `Puts features with different units on one scale so that no feature dominates distances, kernels or gradient steps.`],
[`Specification in this study`, `Training statistics of each fold; applied to all models (tree models do not need it but receive the same input for simplicity).`],
[`Hyper-parameters and how they are tuned`, `No hyper-parameters.`],
[`Data on which it works well`, `Mixed feature types (reflectance, indices, texture, temperature).`],
[`Why it was selected`, `Required by support vector machines, k-nearest neighbours, partial least squares and neural networks.`],
[`Key references`, `Kuhn and Johnson (2013)`]], [2300, 7006], `Method card – z-score standardisation.`, 16));
K.push(H3(`Step E6 – Class weights`));
K.push(...tab2('se6', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The severity classes have unequal sizes (for example 410 healthy vs 96 grade-9 samples); models tend to ignore small classes.`],
[`Input`, `Class counts of the training part.`],
[`Output → next step`, `Class weights for the loss functions of all classifiers → Objectives 2–3.`]], [2200, 7106], `Step E6 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Weight of class c: w_{c} = N / (k × n_{c}), where N is the number of training samples, k the number of classes and n_{c} the size of class c.`));
K.push(NL(`Use the weights in the loss (support vector machine, random forest, extreme gradient boosting, neural networks).`));
K.push(NL(`Report macro-averaged metrics, which give each class equal importance.`));
K.push(P(`**Supporting studies.** Class imbalance in deep learning: Johnson and Khoshgoftaar (2019); macro-averaged metrics: Sokolova and Lapalme (2009).`));
K.push(P(`**Worked example (dummy data).** With N = 1024 training samples, k = 6 classes and 64 samples of grade 9, the weight of grade 9 is 1024 / (6 × 64) = 2.67, while the weight of a class with 273 samples is 1024 / (6 × 273) = 0.63.`));
K.push(H2(`Activity F – Validation design and tuning`));
K.push(H3(`Step F1 – Leave-one-replication-out (LORO) outer folds`));
K.push(...tab2('sf1', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Subplots of one plot, and plots of one replication, are similar; random splits put near-identical samples in training and test data and inflate accuracy.`],
[`Input`, `Clean, labelled feature tables.`],
[`Output → next step`, `Three outer folds → all models of Objectives 2 and 3.`]], [2200, 7106], `Step F1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Fold 1 tests replication R1, fold 2 tests R2, fold 3 tests R3 (leave-one-replication-out, LORO).`));
K.push(NL(`The 12 healthy plots are divided by variety (V1 → fold 1, V2 → fold 2, V3 → fold 3) so that every test fold contains healthy samples.`));
K.push(NL(`All dates and all four subplots of a plot stay in the same fold; each test fold has about 512 post-symptomatic (or 192 pre-symptomatic) samples.`));
K.push(NL(`The same three folds are used for every sensor set, task and model.`));
K.push(P(`**Supporting studies.** Grouped (blocked) cross-validation: Roberts et al. (2017); spatial validation shows that random splits overestimate accuracy: Ploton et al. (2020); the random 7:3 split of Ma et al. (2026) is the optimistic design this step avoids, while its cross-year test supports testing on independent units.`));
K.push(...fig2('validation', 'g09_validation.png', `Leave-one-replication-out outer folds and the inner cross-validation used for selection and tuning.`, 520));
K.push(H3(`Step F2 – Nested inner cross-validation and hyper-parameter tuning`));
K.push(...tab2('sf2', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Feature selection and tuning done on all data (or on the test fold) give over-optimistic accuracy.`],
[`Input`, `Training part of each outer fold.`],
[`Output → next step`, `Selected features, tuned hyper-parameters and early-stopping epochs for each outer fold → final training and one test prediction.`]], [2200, 7106], `Step F2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Inside the training replications, make three inner folds grouped by plot.`));
K.push(NL(`Run all label-based steps inside this inner loop: index search, SHAP-CARS, ReliefF, mRMR, TTFI search, sequential floating forward selection, grid search of hyper-parameters and early stopping of neural networks (validation on plots that are not used for training).`));
K.push(NL(`Choose the hyper-parameters with the best mean inner score (macro-F1 for classes, root-mean-square error for the score).`));
K.push(NL(`Retrain the model on the whole training part with these settings and predict the test replication once.`));
K.push(P(`**Supporting studies.** Nested cross-validation: Varma and Simon (2006), Cawley and Talbot (2010); selection bias when features are chosen outside the folds: Ambroise and McLachlan (2002).`));
K.push(...tab2('cnested', [[`Aspect`, `Grouped nested cross-validation with grid search`],
[`Principle (how it works)`, `An outer loop estimates accuracy on unseen replications; an inner loop inside the training part chooses features and hyper-parameters. Grid search tries every combination in a small grid.`],
[`Problem it solves`, `Gives an almost unbiased accuracy estimate and prevents information from the test replication entering the model.`],
[`Specification in this study`, `Outer: 3 folds (leave-one-replication-out); inner: 3 folds grouped by plot; grids in Table ${T('mlgrid')} and Step 2.3.8.`],
[`Hyper-parameters and how they are tuned`, `The grids themselves; kept small (2–5 values per parameter) to limit overfitting of the selection.`],
[`Data on which it works well`, `Small, grouped datasets such as plots × dates.`],
[`Why it was selected`, `Standard practice for honest accuracy; required because many label-based steps are used.`],
[`Key references`, `Varma and Simon (2006); Cawley and Talbot (2010); Roberts et al. (2017)`]], [2300, 7006], `Method card – Grouped nested cross-validation with grid search.`, 16));
K.push(H3(`Step F3 – Leakage checklist`));
K.push(...tab2('sf3', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A single step done on all data can leak test information into the model.`],
[`Input`, `All steps of the methodology.`],
[`Output → next step`, `Checklist of where every step is run (Table ${T('leak')}) → applied in all objectives.`]], [2200, 7106], `Step F3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`List every step that uses labels or data statistics.`));
K.push(NL(`Assign it to "once on all data" (no labels), "training part" (statistics) or "inner folds" (labels).`));
K.push(NL(`Check the code of every objective against the list before running the final models.`));
K.push(P(`**Supporting studies.** Ambroise and McLachlan (2002); Kuhn and Johnson (2013).`));
K.push(...tab2('leak', [[`Step`, `Uses labels?`, `Where it is run`],
[`Activities B–D (pre-processing, mask, features)`, `no`, `once, on all data`],
[`E1–E2 (date consistency, thermal normalisation)`, `no`, `once, on all data`],
[`E3 (healthy-plot normalisation)`, `no (uses healthy plots)`, `training healthy plots → applied to test data`],
[`E5–E6 (standardisation, class weights)`, `no (statistics)`, `training part of each fold`],
[`Within-group redundancy (|r| ≥ 0.95), variance inflation factor`, `no`, `training part of each fold`],
[`NDSI/RSI and White Rust Index search, SHAP-CARS, ReliefF, mRMR, TTFI search`, `yes`, `inner folds only`],
[`Sequential floating forward selection, hyper-parameter tuning, early stopping`, `yes`, `inner folds only`],
[`Final evaluation`, `yes`, `test replication, once`]], [4300, 1900, 3106], `Where each step is run so that no information from the test replication enters the model.`, 17));
K.push(...tab2('foldsize', [[`Dataset`, `Training part per outer fold`, `Test part per outer fold`, `Inner folds`],
[`Post-symptomatic (1536 per camera)`, `≈ 1024 samples`, `≈ 512 samples`, `3, grouped by plot`],
[`Pre-symptomatic (576 per camera)`, `≈ 384 samples`, `≈ 192 samples`, `3, grouped by plot`]], [2800, 2600, 1900, 2006], `Approximate sizes of the training and test parts.`, 17));
K.push(H1(`3. Objective 1 – Characterisation of white rust through multimodal UAV sensing`));
K.push(P(`Objective 1 describes how each camera sees white rust and selects the features that carry disease information. It uses the 1536 post-symptomatic samples of each camera. For description and interpretation the steps are run on all post-symptomatic samples; for prediction (Objectives 2 and 3) exactly the same steps are repeated inside the training part of every fold (Step F2), so the test replication never chooses a feature.`));
K.push(...fig2('obj1', 'g05_obj1.png', `Flow chart of Objective 1 (Activities 1.1–1.6).`, 540));
K.push(...tab2('o1act', [[`Activity`, `Steps`, `Technique (one per feature type)`, `Output`],
[`1.1 Response analysis`, `1.1.1–1.1.3`, `mean spectra, first derivative, Pearson correlation`, `response figures; responsive regions`],
[`1.2 Optimal wavelengths`, `1.2.1–1.2.4`, `NDSI/RSI maps → SHAP-CARS`, `10–15 optimal wavelengths (OW)`],
[`1.3 Spectral index construction`, `1.3.1–1.3.3`, `exhaustive two-band and three-band search`, `best NDSI, RSI and White Rust Index (WRI)`],
[`1.4 Vegetation index selection`, `1.4.1–1.4.3`, `redundancy filter → ReliefF / RReliefF`, `5–8 selected indices`],
[`1.5 Texture selection and TTFI`, `1.5.1–1.5.4`, `principal-component texture → mRMR → TTFI`, `6 texture features + best TTFI`],
[`1.6 Disease-specific feature sets`, `1.6.1–1.6.4`, `same rules for other cameras → variance inflation factor`, `feature set of each camera; treatment response`]], [2400, 1100, 3000, 2806], `Activities of Objective 1.`, 17));
K.push(H2(`The feature-selection rule: one method for each type of feature`));
K.push(P(`Pooling all features (about 1150 for the four cameras) and selecting from one big pool would be unstable, would keep many near-duplicates and would let the hundreds of spectral bands swamp the small thermal and texture groups (Hughes, 1968; Guyon and Elisseeff, 2003; Dormann et al., 2013; Ghamisi et al., 2019). Selection is therefore done in four stages, and in Stage 2 one method is used for each type of feature, the method that best suits the nature of that type and that was used for the same type in the DT-EDNet study (Ma et al., 2026) (Figure ${F('selection')}).`));
K.push(...tab2('stages', [[`Stage`, `What is done`, `Uses labels?`, `Where in this document`],
[`0. Build groups`, `calculate features with physical meaning (no second derivative)`, `no`, `Activity D`],
[`1. Redundancy within groups`, `remove near-constant features; keep one feature of every cluster with |r| ≥ 0.95 (indices, texture, thermal, multispectral and colour groups)`, `no`, `Steps 1.4.2, 1.5.3, 1.6.1`],
[`2. Selection within groups (one method per type)`, `spectral bands: SHAP-CARS; vegetation indices: ReliefF (RReliefF for the score); texture: mRMR; constructed indices: exhaustive search; thermal and multispectral bands: kept`, `yes`, `Activities 1.2–1.5`],
[`3. Redundancy across groups`, `pool the survivors; variance inflation factor below 10`, `no`, `Step 1.6.2`],
[`4. Final compact set (machine learning only)`, `sequential floating forward selection with each model, at most 15 features`, `yes`, `Step 2.1.4`]], [2200, 4400, 1100, 1606], `The four selection stages.`, 17));
K.push(...fig2('selection', 'g08_selection.png', `One feature-selection method for each feature type, run inside the training part of each fold.`, 540));
K.push(H2(`Activity 1.1 – Response analysis`));
K.push(H3(`Step 1.1.1 – Mean spectra and first-derivative curves by severity grade`));
K.push(...tab2('s111', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Shows how the spectrum changes with severity before any selection and gives the physiological basis for later results.`],
[`Input`, `Subplot mean reflectance and first derivative (post-symptomatic).`],
[`Output → next step`, `Response figures (Figure ${F('dummyspec')}) and a list of responsive regions → Activities 1.2–1.3 (interpretation).`]], [2200, 7106], `Step 1.1.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Average the subplot spectra of each grade (0, 1, 3, 5, 7, 9) and plot them with ± one standard deviation.`));
K.push(NL(`Plot the first derivative in the red edge (680–760 nm) for each grade.`));
K.push(NL(`Describe the changes: visible rise from chlorophyll loss, shift of the red edge to shorter wavelengths, near-infrared fall from leaf damage, short-wave-infrared rise from water loss.`));
K.push(P(`**Supporting studies.** Spectral response by severity level: Mahlein et al. (2013), Guo et al. (2021), Ma et al. (2026); red-edge shift under stress: Horler et al. (1983), Filella and Peñuelas (1994).`));
K.push(H3(`Step 1.1.2 – Correlation of each feature with the severity score`));
K.push(...tab2('s112', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Quantifies how strongly each feature follows severity and gives the direction of the response.`],
[`Input`, `All features of each camera.`],
[`Output → next step`, `Correlation table and correlation curves → interpretation; used again in Steps 1.3 and 1.5.`]], [2200, 7106], `Step 1.1.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Compute the Pearson correlation coefficient r between each feature and the severity score.`));
K.push(NL(`Plot r against wavelength for reflectance and first derivative (correlation curve).`));
K.push(NL(`Report r with its sign; p-values are not used for selection because subplots of one plot are related.`));
K.push(P(`**Supporting studies.** Correlation of indices and texture with severity: Ma et al. (2026), Guo et al. (2021); univariate feature screening: Liu et al. (2020).`));
K.push(H3(`Step 1.1.3 – Response by variety, inoculation timing and days after inoculation`));
K.push(...tab2('s113', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A feature may respond in one variety or crop age and not in another; treatments must be considered.`],
[`Input`, `Responsive features; treatment codes.`],
[`Output → next step`, `Treatment-wise response figures → Step 1.6.3 and Objective 2 robustness (Activity 2.6).`]], [2200, 7106], `Step 1.1.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Plot the main features against days after inoculation for each variety (V1–V3) and inoculation timing (D1–D4).`));
K.push(NL(`Compare inoculated plots with their healthy plot of the same treatment on every date.`));
K.push(P(`**Supporting studies.** Treatment-wise disease response: Liu et al. (2024), Blasch et al. (2023), Feng et al. (2022).`));
K.push(H2(`Activity 1.2 – Optimal wavelengths with Shapley additive explanations and competitive adaptive reweighted sampling (SHAP-CARS)`));
K.push(P(`The hyperspectral camera gives 483 reflectance bands and 483 first-derivative bands. Activity 1.2 reduces them to 10–15 optimal wavelengths (OW) in two stages: first the effective ranges are found from two-band index maps, then Shapley additive explanations combined with competitive adaptive reweighted sampling (SHAP-CARS) select the optimal wavelengths inside these ranges (Ma et al., 2026).`));
K.push(H3(`Step 1.2.1 – Effective wavelength ranges from normalised difference spectral index (NDSI) and ratio spectral index (RSI) maps`));
K.push(...tab2('s121', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Many regions of the spectrum carry no disease information; searching all bands wastes time and adds noise.`],
[`Input`, `Subplot reflectance (training part).`],
[`Output → next step`, `Effective wavelength ranges (regions where index pairs relate strongly to severity) → Step 1.2.2; the best pairs → Step 1.3.1.`]], [2200, 7106], `Step 1.2.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`For every pair of bands (λ_{1}, λ_{2}) compute the normalised difference spectral index NDSI and the ratio spectral index RSI (equations below); with 483 bands there are 116 403 pairs for each index.`));
K.push(NL(`Compute the coefficient of determination R² between each index and the severity score and draw R² contour maps (Figure ${F('dummyndsi')}).`));
K.push(NL(`Effective ranges = the wavelength regions that take part in pairs with R² ≥ 0.5 (as in Ma et al., 2026); if no pair reaches 0.5, use the regions of the top 5% of pairs.`));
K.push(P(`**Supporting studies.** Two-band NDSI and RSI searches and R² contour maps: Ma et al. (2026); optimised two-band indices for wheat diseases: Huang et al. (2014).`));
K.push(EQ(`NDSI(λ_{1}, λ_{2}) = (R_{λ1} − R_{λ2}) / (R_{λ1} + R_{λ2});      RSI(λ_{1}, λ_{2}) = R_{λ1} / R_{λ2}`));
K.push(P(`**Worked example (dummy data).** With R_{760} = 0.45 and R_{550} = 0.09, NDSI(760, 550) = (0.45 − 0.09) / (0.45 + 0.09) = 0.667 and RSI(760, 550) = 5.0. In a diseased subplot with R_{760} = 0.38 and R_{550} = 0.11 the values fall to 0.551 and 3.45.`));
K.push(...fig2('dummyndsi', 'g14_dummy_ndsi.png', `Dummy example of an R² contour map of NDSI(λ₁, λ₂) against the severity score. The star marks the best pair; the bright regions define the effective ranges.`, 400));
K.push(...tab2('cndsi', [[`Aspect`, `Exhaustive two-band index search (NDSI and RSI maps)`],
[`Principle (how it works)`, `Every pair of bands is turned into a normalised difference and a ratio; the relation of each index with severity is mapped, which shows which band combinations carry disease information.`],
[`Problem it solves`, `Finds disease-sensitive band combinations without prior assumptions and narrows the search for later selection.`],
[`Specification in this study`, `All 116 403 pairs of the 483 bands; R² with the severity score on the training part; threshold R² ≥ 0.5.`],
[`Hyper-parameters and how they are tuned`, `Threshold for the effective ranges (0.5, from Ma et al., 2026); checked so that the ranges are not narrower than about 20 nm.`],
[`Data on which it works well`, `Hyperspectral data with a continuous target (severity score).`],
[`Why it was selected`, `Simple, visual and directly linked to index construction (Step 1.3.1).`],
[`Key references`, `Ma et al. (2026); Huang et al. (2014)`]], [2300, 7006], `Method card – Exhaustive two-band index search (NDSI and RSI maps).`, 16));
K.push(H3(`Step 1.2.2 – Shapley additive explanations (SHAP) pre-screening of the bands`));
K.push(...tab2('s122', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Inside the effective ranges there are still hundreds of correlated bands; a quick, model-based ranking removes clearly unimportant bands before the slower CARS step.`],
[`Input`, `Reflectance and first-derivative bands inside the effective ranges (training part).`],
[`Output → next step`, `Top 40% of bands by mean absolute Shapley value → Step 1.2.3.`]], [2200, 7106], `Step 1.2.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Train a tree ensemble (extreme gradient boosting, 300 trees, depth 4, learning rate 0.05) to predict the severity score from the bands.`));
K.push(NL(`Compute the Shapley additive explanation (SHAP) value of every band for every training sample with the tree explainer.`));
K.push(NL(`Rank bands by the mean absolute SHAP value and keep the top 40% (Figure ${F('dummyshap')}a).`));
K.push(P(`**Supporting studies.** Shapley values: Lundberg and Lee (2017), Lundberg et al. (2020); SHAP-based band selection: Ma et al. (2026).`));
K.push(...tab2('cshap', [[`Aspect`, `Shapley additive explanations (SHAP)`],
[`Principle (how it works)`, `From cooperative game theory: the contribution of a feature is its average effect on the prediction over all possible orders in which features are added to the model; for tree models it is computed exactly and quickly.`],
[`Problem it solves`, `Ranks bands by their real contribution to a non-linear model, including interactions, which simple correlation misses.`],
[`Specification in this study`, `Tree explainer on an extreme gradient boosting model trained on the training part; ranking by mean |SHAP|; top 40% kept.`],
[`Hyper-parameters and how they are tuned`, `Model settings (300 trees, depth 4, learning rate 0.05) fixed, because the model is only used for ranking; the kept share (30–50%) checked in the inner folds.`],
[`Data on which it works well`, `Tabular data with many correlated features and non-linear relations.`],
[`Why it was selected`, `Consistent and model-agnostic importance; used in this exact role by Ma et al. (2026).`],
[`Key references`, `Lundberg and Lee (2017); Lundberg et al. (2020); Ma et al. (2026)`]], [2300, 7006], `Method card – Shapley additive explanations (SHAP).`, 16));
K.push(H3(`Step 1.2.3 – Competitive adaptive reweighted sampling (CARS) with partial least squares (PLS)`));
K.push(...tab2('s123', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The pre-screened bands are still strongly collinear; a small set of complementary wavelengths is needed.`],
[`Input`, `Pre-screened bands (training part).`],
[`Output → next step`, `Optimal wavelength subset with the lowest cross-validated error → Step 1.2.4.`]], [2200, 7106], `Step 1.2.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Choose the number of partial least squares (PLS) components (1–15) by Monte Carlo cross-validation (MCCV: 50 random 80/20 splits of the training plots).`));
K.push(NL(`Run competitive adaptive reweighted sampling (CARS) for 50 iterations: in each iteration, fit PLS on a random 80% of the samples, weight every band by the absolute value of its PLS regression coefficient, remove bands by an exponentially decreasing function and then by adaptive reweighted sampling.`));
K.push(NL(`After every iteration compute the root-mean-square error of cross-validation (RMSECV); the subset with the minimum RMSECV is the optimal subset (Figure ${F('dummyshap')}b, c).`));
K.push(P(`**Supporting studies.** CARS: Li et al. (2009); variable selection in PLS: Mehmood et al. (2012); SHAP-CARS with MCCV for the PLS components: Ma et al. (2026).`));
K.push(...fig2('dummyshap', 'g15_dummy_shapcars.png', `Dummy example of SHAP-CARS: (a) Shapley pre-screening; (b) number of wavelengths kept in each CARS iteration; (c) the iteration with the minimum cross-validated error defines the optimal wavelengths.`, 560));
K.push(...tab2('ccars', [[`Aspect`, `Competitive adaptive reweighted sampling (CARS) with partial least squares (PLS)`],
[`Principle (how it works)`, `Imitates "survival of the fittest": bands with large PLS regression coefficients survive, bands with small coefficients are removed step by step; the subset with the lowest cross-validated error is kept. PLS itself projects correlated bands onto a few latent components that best predict the target.`],
[`Problem it solves`, `Selects a small set of non-redundant, informative wavelengths from highly collinear spectra.`],
[`Specification in this study`, `50 iterations; 80% sampling per iteration; PLS components by MCCV (50 splits, maximum 15); CARS repeated 20 times with different random seeds.`],
[`Hyper-parameters and how they are tuned`, `Number of PLS components (by MCCV) and number of iterations (50); because results vary between runs, wavelengths selected in at least 50% of the 20 runs are kept (stability rule).`],
[`Data on which it works well`, `Spectra with many correlated bands and a continuous target.`],
[`Why it was selected`, `Designed for spectra, fast and the best of the three band-selection methods in the DT-EDNet study (Ma et al., 2026); the Shapley pre-screening adds a non-linear view.`],
[`Key references`, `Li et al. (2009); Mehmood et al. (2012); Ma et al. (2026)`]], [2300, 7006], `Method card – Competitive adaptive reweighted sampling (CARS) with partial least squares (PLS).`, 16));
K.push(H3(`Step 1.2.4 – Optimal wavelengths (OW) and their stability`));
K.push(...tab2('s124', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The final wavelength set must be stable and physiologically interpretable.`],
[`Input`, `Optimal subsets of the 20 CARS runs.`],
[`Output → next step`, `Optimal wavelengths (OW, 10–15 bands of reflectance and first derivative) → Activity 1.3, fused inputs of Objective 2 and the network configurations (Step 2.1.5).`]], [2200, 7106], `Step 1.2.4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Count how often each wavelength is selected over the 20 runs; keep those selected in at least 50%.`));
K.push(NL(`If more than 15 remain, keep the 15 most frequent.`));
K.push(NL(`Link each wavelength to a known absorption feature (chlorophyll, red edge, water, structure) for interpretation.`));
K.push(P(`**Supporting studies.** Stability of selection: Meinshausen and Bühlmann (2010), Nogueira et al. (2018); optimal wavelengths for rice blast: Ma et al. (2026).`));
K.push(H2(`Activity 1.3 – Spectral index construction`));
K.push(H3(`Step 1.3.1 – Best normalised difference spectral index (NDSI) and ratio spectral index (RSI)`));
K.push(...tab2('s131', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A single disease-related index is simpler and more transferable than many bands.`],
[`Input`, `NDSI and RSI maps (Step 1.2.1).`],
[`Output → next step`, `Best NDSI and best RSI (highest R² with the severity score) → Activity 1.4 (index group).`]], [2200, 7106], `Step 1.3.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Take the pair with the highest R² from each map.`));
K.push(NL(`Avoid pairs closer than 10 nm (they measure noise rather than a spectral feature).`));
K.push(P(`**Supporting studies.** Ma et al. (2026); Huang et al. (2014).`));
K.push(H3(`Step 1.3.2 – White Rust Index (WRI), a three-band index`));
K.push(...tab2('s132', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Two bands may not capture both the pigment change and the structural change caused by white rust.`],
[`Input`, `Reflectance and the best normalised differences (training part).`],
[`Output → next step`, `White Rust Index (WRI) formula → Activity 1.4 and Objectives 2–3.`]], [2200, 7106], `Step 1.3.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Search WRI = NDSI(λ_{1}, λ_{2}) + w × R(λ_{3}) with w ∈ {−1, −0.5, 0, 0.5, 1}, using bands at 6 nm steps and λ_{1} and λ_{2} at least 50 nm apart.`));
K.push(NL(`Score each candidate by its correlation with the severity score and by the balanced accuracy of healthy vs diseased in grouped inner cross-validation.`));
K.push(NL(`Keep the best formula; repeat the search inside the training part of every fold for prediction.`));
K.push(P(`**Supporting studies.** Disease-specific indices from a normalised difference plus a single band: Mahlein et al. (2013); three-band disease index for yellow rust: Zheng et al. (2018); ground-to-UAV disease index for powdery mildew: Liu et al. (2026).`));
K.push(EQ(`WRI = NDSI(λ_{1}, λ_{2}) + w R_{λ3},      w ∈ {−1, −0.5, 0, 0.5, 1}`));
K.push(...tab2('cwri', [[`Aspect`, `Disease-specific index search (White Rust Index)`],
[`Principle (how it works)`, `Combines the most informative normalised difference with a third band that carries extra information; the weight w sets how much the third band contributes.`],
[`Problem it solves`, `Creates one interpretable index specific to white rust instead of a general vegetation index.`],
[`Specification in this study`, `Bands at 6 nm steps inside the effective ranges; five weights; correlation and balanced accuracy in grouped inner folds.`],
[`Hyper-parameters and how they are tuned`, `The weight w (five values) and the band positions; chosen in the inner folds only.`],
[`Data on which it works well`, `Hyperspectral data from which a cheaper sensor or a satellite band set may later be designed.`],
[`Why it was selected`, `The same form gave disease-specific indices for sugar beet diseases (Mahlein et al., 2013); the three-band idea was also used for yellow rust (Zheng et al., 2018).`],
[`Key references`, `Mahlein et al. (2013); Zheng et al. (2018)`]], [2300, 7006], `Method card – Disease-specific index search (White Rust Index).`, 16));
K.push(H3(`Step 1.3.3 – Two-band indices of the multispectral camera`));
K.push(...tab2('s133', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The multispectral camera has only five bands; its best band combination must be known.`],
[`Input`, `Five multispectral bands.`],
[`Output → next step`, `Ranked ten normalised differences → Step 1.6.1.`]], [2200, 7106], `Step 1.3.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Compute all ten normalised differences of the five bands.`));
K.push(NL(`Rank them by R² with the severity score and compare the best with the White Rust Index.`));
K.push(P(`**Supporting studies.** Ma et al. (2026); multispectral red-edge indices for powdery mildew: Liu et al. (2024).`));
K.push(H2(`Activity 1.4 – Vegetation index selection with ReliefF`));
K.push(H3(`Step 1.4.1 – Index group`));
K.push(...tab2('s141', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Collects all index-type features into one group.`],
[`Input`, `Published indices and red-edge parameters (Step D4); best NDSI, RSI and WRI (Activity 1.3).`],
[`Output → next step`, `Index group of about 55 features → Step 1.4.2.`]], [2200, 7106], `Step 1.4.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Join the published indices, the three red-edge parameters and the constructed indices.`));
K.push(P(`**Supporting studies.** Ma et al. (2026); Mahlein et al. (2013).`));
K.push(H3(`Step 1.4.2 – Within-group redundancy filter`));
K.push(...tab2('s142', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Many indices are nearly identical (for example several NDVI versions), which wastes the selection on duplicates.`],
[`Input`, `Index group (training part).`],
[`Output → next step`, `Thinned index group → Step 1.4.3.`]], [2200, 7106], `Step 1.4.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Remove near-constant indices (standard deviation close to zero).`));
K.push(NL(`Group indices with |r| ≥ 0.95 and keep one per group (the one with the strongest correlation with the severity score).`));
K.push(P(`**Supporting studies.** Correlation clustering before selection: Dormann et al. (2013); high correlation among vegetation indices: Ma et al. (2026).`));
K.push(...tab2('ccorr', [[`Aspect`, `Correlation-cluster redundancy filter`],
[`Principle (how it works)`, `Features whose pairwise |r| is at least 0.95 measure almost the same thing; one representative per cluster keeps the information.`],
[`Problem it solves`, `Removes duplicates before relevance selection, which makes ReliefF and mRMR more stable.`],
[`Specification in this study`, `Pearson |r| ≥ 0.95; representative = the member with the strongest correlation with the severity score.`],
[`Hyper-parameters and how they are tuned`, `Threshold 0.95 (fixed; 0.90 tested as a check).`],
[`Data on which it works well`, `Groups of derived features (indices, texture, thermal statistics).`],
[`Why it was selected`, `Label-free (no leakage), simple and transparent.`],
[`Key references`, `Dormann et al. (2013)`]], [2300, 7006], `Method card – Correlation-cluster redundancy filter.`, 16));
K.push(H3(`Step 1.4.3 – ReliefF ranking of the indices`));
K.push(...tab2('s143', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The indices that best separate overlapping severity classes must be chosen.`],
[`Input`, `Thinned index group, standardised (training part).`],
[`Output → next step`, `Top five to eight indices (number chosen in the inner folds) → Step 1.6.2 and the "VI" group of Step 2.1.5.`]], [2200, 7106], `Step 1.4.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Classes: run ReliefF with k = 10 nearest neighbours on standardised indices; neighbours from the same plot are excluded so that a subplot is not compared with its own plot.`));
K.push(NL(`Severity score: run RReliefF, the regression version, in the same way.`));
K.push(NL(`Rank the indices by their weight and keep the top five (as in Ma et al., 2026); check 3–8 in the inner folds (Figure ${F('dummyrelief')}a).`));
K.push(P(`**Supporting studies.** ReliefF and RReliefF: Robnik-Šikonja and Kononenko (2003), Urbanowicz et al. (2018); ReliefF for disease indices: Mahlein et al. (2013), Huang et al. (2014); Relief for vegetation indices in rice blast: Ma et al. (2026).`));
K.push(EQ(`W_{j} ← W_{j} − diff(j, x, H)/m + Σ_{c≠class(x)} [P(c)/(1 − P(class(x)))] diff(j, x, M_{c})/m`));
K.push(P(`For each sampled subplot x, H is its nearest neighbour of the same class (nearest hit) and M_{c} its nearest neighbour of another class c (nearest miss); diff is the absolute difference of feature j. A feature gains weight when it differs between classes and loses weight when it differs within a class. **Worked example (dummy data):** for one sample, index A differs by 0.05 from its hit and by 0.40 from its misses, so its weight rises by about (0.40 − 0.05)/m; index B differs by 0.30 from both and gains nothing.`));
K.push(...fig2('dummyrelief', 'g16_dummy_relief_mrmr.png', `Dummy example: (a) ReliefF weights of the indices (top six kept); (b) cumulative variance of the principal components of the cube (three kept); (c) mRMR ranking of the texture features (top six kept).`, 560));
K.push(...tab2('crelief', [[`Aspect`, `ReliefF (classes) and RReliefF (severity score)`],
[`Principle (how it works)`, `For each sample, compares its feature values with its nearest neighbours of the same class and of other classes; features that separate classes but are stable within classes gain weight. RReliefF does the same with the probability that predictions differ for a continuous target.`],
[`Problem it solves`, `Ranks features by their ability to separate overlapping, ordered severity classes, including effects that appear only together with other features.`],
[`Specification in this study`, `k = 10 neighbours; all training samples used; standardised features; neighbours from the same plot excluded; top five kept.`],
[`Hyper-parameters and how they are tuned`, `k (5, 10, 20) and the number kept (3–8) checked in the inner folds; k = 10 is the usual default.`],
[`Data on which it works well`, `Classification with several overlapping classes and moderate numbers of features (tens to hundreds).`],
[`Why it was selected`, `Handles several classes and interactions, is fast and was used for vegetation indices in the DT-EDNet study and for disease indices in hyperspectral studies.`],
[`Key references`, `Robnik-Šikonja and Kononenko (2003); Urbanowicz et al. (2018); Ma et al. (2026)`]], [2300, 7006], `Method card – ReliefF (classes) and RReliefF (severity score).`, 16));
K.push(H2(`Activity 1.5 – Texture selection and the Tri-band Texture Fusion Index (TTFI)`));
K.push(H3(`Step 1.5.1 – Principal component analysis (PCA) texture of the hyperspectral cube`));
K.push(...tab2('s151', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Texture of 483 bands would give almost 4000 redundant features.`],
[`Input`, `Masked hyperspectral cube (Step D5).`],
[`Output → next step`, `24 texture features (8 measures × 3 principal components, for example PC2-Dis = dissimilarity of component 2) → Step 1.5.2.`]], [2200, 7106], `Step 1.5.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Fit principal component analysis on vegetation pixels of the training data and keep the first three components (cumulative variance above 95%; Figure ${F('dummyrelief')}b).`));
K.push(NL(`Compute the eight GLCM measures on each component image (Step D5) and average them over the vegetation pixels of each subplot.`));
K.push(P(`**Supporting studies.** Texture from principal-component images: Guo et al. (2021), Ma et al. (2026); GLCM: Haralick et al. (1973), Hall-Beyer (2017).`));
K.push(H3(`Step 1.5.2 – Within-group redundancy filter`));
K.push(...tab2('s152', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Some texture measures are almost identical (for example contrast and dissimilarity).`],
[`Input`, `24 texture features (training part).`],
[`Output → next step`, `Thinned texture group → Step 1.5.3.`]], [2200, 7106], `Step 1.5.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Apply the correlation-cluster filter (|r| ≥ 0.95), as in Step 1.4.2.`));
K.push(P(`**Supporting studies.** Dormann et al. (2013); Hall-Beyer (2017) on the strong correlation of contrast and dissimilarity.`));
K.push(H3(`Step 1.5.3 – Minimum redundancy maximum relevance (mRMR) selection of texture`));
K.push(...tab2('s153', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Texture features are correlated with each other; the selected set should be informative and non-redundant.`],
[`Input`, `Thinned texture group (training part).`],
[`Output → next step`, `Top six texture features (TF1–TF6) → Step 1.5.4 and the "TF" group of Step 2.1.5.`]], [2200, 7106], `Step 1.5.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Estimate the relevance of each texture feature as its mutual information with the severity class (or score).`));
K.push(NL(`Select features one at a time: the next feature is the one with the largest relevance minus its mean mutual information with the features already selected (Figure ${F('dummyrelief')}c).`));
K.push(NL(`Stop at six features (as in Ma et al., 2026); check 4–8 in the inner folds.`));
K.push(P(`**Supporting studies.** mRMR: Peng et al. (2005); mRMR for texture features of rice blast: Ma et al. (2026); mRMR for UAV and satellite disease features: Yuan et al. (2025).`));
K.push(EQ(`next feature = arg max_{j} [ I(f_{j}; y) − (1/|S|) Σ_{s∈S} I(f_{j}; f_{s}) ]`));
K.push(...tab2('mrmrex', [[`Texture feature (dummy)`, `Relevance I(f; y)`, `Mean redundancy with selected set`, `mRMR score`, `Decision`],
[`PC2-Dis`, `0.62`, `— (first pick)`, `0.62`, `selected 1st`],
[`PC2-Con`, `0.60`, `0.55 (with PC2-Dis)`, `0.05`, `not selected now`],
[`PC3-Mea`, `0.41`, `0.08`, `0.33`, `selected 2nd`],
[`PC2-Hom`, `0.52`, `0.30`, `0.22`, `selected 3rd`]], [2200, 1500, 2300, 1300, 2006], `Worked example (dummy data): the first picks of mRMR. A strongly relevant but redundant feature (PC2-Con) is delayed in favour of a less relevant but new one (PC3-Mea).`, 17));
K.push(...tab2('cmrmr', [[`Aspect`, `Minimum redundancy maximum relevance (mRMR)`],
[`Principle (how it works)`, `Greedy forward selection that balances two quantities measured with mutual information: relevance to the target and redundancy with the features already chosen.`],
[`Problem it solves`, `Selects a compact, complementary set from correlated texture features.`],
[`Specification in this study`, `Mutual information estimated with a k-nearest-neighbour estimator (k = 3) on standardised features; difference criterion (relevance minus redundancy); six features.`],
[`Hyper-parameters and how they are tuned`, `Number of features (4–8) checked in the inner folds; k of the estimator fixed at 3.`],
[`Data on which it works well`, `Groups of correlated features with non-linear relations to the target.`],
[`Why it was selected`, `Removes redundancy and selects relevance in one step; used for texture in the DT-EDNet study and for disease features by Yuan et al. (2025).`],
[`Key references`, `Peng et al. (2005); Ma et al. (2026); Yuan et al. (2025)`]], [2300, 7006], `Method card – Minimum redundancy maximum relevance (mRMR).`, 16));
K.push(H3(`Step 1.5.4 – Construction of the Tri-band Texture Fusion Index (TTFI)`));
K.push(...tab2('s154', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Single texture features describe only one aspect of the lesion pattern; a combination of three can describe roughness, heterogeneity and structure together.`],
[`Input`, `Selected texture features TF1–TF6 (training part).`],
[`Output → next step`, `Best TTFI (strongest correlation with severity) → Step 1.6.2 and the network configurations (Step 2.1.5).`]], [2200, 7106], `Step 1.5.4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Form all ordered triplets (TF1, TF2, TF3) of the six texture features: 6 × 5 × 4 = 120 triplets.`));
K.push(NL(`For every triplet compute the three Tri-band Texture Fusion Indices (equations below), giving 360 candidates.`));
K.push(NL(`Compute the correlation of every candidate with the severity score; keep the best candidate of each formula for description (Figure ${F('dummyttfi')}) and the overall best TTFI as the texture index used in modelling.`));
K.push(P(`**Supporting studies.** Tri-band Texture Fusion Index: Ma et al. (2026).`));
K.push(EQ(`TTFI1 = (TF1 + TF2) / TF3;      TTFI2 = TF1 × TF2 / TF3;      TTFI3 = TF1 × (TF1 + TF2) / (TF2 + TF3)`));
K.push(P(`**Worked example (dummy data).** With TF1 = 0.8, TF2 = 1.2 and TF3 = 0.5: TTFI1 = (0.8 + 1.2) / 0.5 = 4.00; TTFI2 = 0.8 × 1.2 / 0.5 = 1.92; TTFI3 = 0.8 × (0.8 + 1.2) / (1.2 + 0.5) = 0.94. Texture values are used on their original (positive) scale; a small constant is added to a denominator that can approach zero.`));
K.push(...fig2('dummyttfi', 'g17_dummy_ttfi.png', `Dummy example: correlation of the best triplet of each TTFI formula with severity, compared with the best single texture feature and the best index.`, 460));
K.push(...tab2('cttfi', [[`Aspect`, `Tri-band Texture Fusion Index (TTFI)`],
[`Principle (how it works)`, `Combines three texture features in sums, products and ratios so that their joint behaviour (for example rising dissimilarity with falling homogeneity) is captured in one number.`],
[`Problem it solves`, `Gives one strong, interpretable texture variable instead of several weak ones.`],
[`Specification in this study`, `Six mRMR-selected features; 120 ordered triplets × 3 formulas; best by |r| with the severity score on the training part.`],
[`Hyper-parameters and how they are tuned`, `No hyper-parameters; the triplet is chosen in the inner folds only.`],
[`Data on which it works well`, `High-resolution texture from canopies with spotty lesions.`],
[`Why it was selected`, `In rice blast, TTFI3 was more strongly related to disease (|r| = 0.75) than any single texture feature and improved all networks when fused with the optimal wavelengths (Ma et al., 2026).`],
[`Key references`, `Ma et al. (2026)`]], [2300, 7006], `Method card – Tri-band Texture Fusion Index (TTFI).`, 16));
K.push(H2(`Activity 1.6 – Disease-specific feature sets of each camera`));
K.push(H3(`Step 1.6.1 – Selection for the multispectral, red–green–blue and thermal cameras`));
K.push(...tab2('s161', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The other cameras must be treated with the same rule so that the cameras can be compared fairly.`],
[`Input`, `Feature groups of the three cameras (training part).`],
[`Output → next step`, `Selected features of each camera → Step 1.6.2.`]], [2200, 7106], `Step 1.6.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Multispectral: keep the five bands (small group); indices and normalised differences: redundancy filter → ReliefF (RReliefF for the score), top five; texture: redundancy filter → mRMR, top four.`));
K.push(NL(`Red–green–blue: colour indices and colour means: redundancy filter → ReliefF, top four; texture: redundancy filter → mRMR, top four.`));
K.push(NL(`Thermal: keep all thermal features after the redundancy filter (group of about 10).`));
K.push(P(`**Supporting studies.** One selection approach per group: Ma et al. (2026); thermal features kept as their own group: Feng et al. (2022), Liu et al. (2024).`));
K.push(H3(`Step 1.6.2 – Variance inflation factor (VIF) across groups`));
K.push(...tab2('s162', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Survivors of different groups can still be correlated (for example a red-edge wavelength and a red-edge index).`],
[`Input`, `Pooled survivors of all groups of one camera (training part).`],
[`Output → next step`, `Disease-specific feature set of the camera (about 10–25 features) → Objective 2 (Step 2.1.2) and discussion.`]], [2200, 7106], `Step 1.6.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Pool the selected features of all groups of the camera.`));
K.push(NL(`Compute the variance inflation factor (VIF) of every feature; remove the feature with the highest VIF and repeat until all VIF values are below 10.`));
K.push(P(`**Supporting studies.** Dormann et al. (2013); variance inflation factor before feature-combination search in disease studies: Tian et al. (2021), Mustafa et al. (2023).`));
K.push(EQ(`VIF_{j} = 1 / (1 − R_{j}^{2})`));
K.push(P(`Here R_{j}^{2} is the coefficient of determination of feature j regressed on all other features. **Worked example:** a feature explained 90% by the others (R_{j}^{2} = 0.90) has VIF = 1 / 0.10 = 10, which is the removal limit.`));
K.push(...tab2('cvif', [[`Aspect`, `Variance inflation factor (VIF)`],
[`Principle (how it works)`, `Measures how much of a feature can be predicted from the other features; a large value means the feature is redundant with the rest.`],
[`Problem it solves`, `Removes multicollinearity across feature groups, which makes models and importance values stable.`],
[`Specification in this study`, `Iterative removal of the feature with the largest VIF until all are below 10.`],
[`Hyper-parameters and how they are tuned`, `Threshold 10 (the usual limit; 5 tested as a check).`],
[`Data on which it works well`, `Pooled sets of correlated predictors.`],
[`Why it was selected`, `Label-free, simple and widely used in disease-feature selection.`],
[`Key references`, `Dormann et al. (2013); Tian et al. (2021)`]], [2300, 7006], `Method card – Variance inflation factor (VIF).`, 16));
K.push(H3(`Step 1.6.3 – Response by treatment and complementarity of cameras`));
K.push(...tab2('s163', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Shows whether the selected features behave the same in all varieties and inoculation timings and whether the cameras carry different information.`],
[`Input`, `Disease-specific feature sets; treatment codes.`],
[`Output → next step`, `Treatment-wise response figures; correlation matrix between the cameras → Objective 2 interpretation.`]], [2200, 7106], `Step 1.6.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Plot the selected features against days after inoculation for each variety and inoculation timing.`));
K.push(NL(`Compute the correlation matrix between the selected features of the four cameras (for example thermal difference vs short-wave-infrared water indices).`));
K.push(NL(`Check that selected features do not simply follow flower % or canopy cover (correlation with the covariates).`));
K.push(P(`**Supporting studies.** Sensor complementarity: Mahlein et al. (2019), Maimaitijiang et al. (2020); flowering effects in Brassica: Sulik and Long (2016).`));
K.push(H3(`Step 1.6.4 – Outputs of Objective 1`));
K.push(...tab2('s164', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Summarises what Objective 1 delivers to the other objectives.`],
[`Input`, `Results of Activities 1.1–1.6.`],
[`Output → next step`, `Feature lists and figures → Objectives 2 and 3; Objective 1 chapter of the thesis.`]], [2200, 7106], `Step 1.6.4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Response curves by grade, variety and inoculation timing.`));
K.push(NL(`Optimal wavelengths (OW) with their stability.`));
K.push(NL(`Best NDSI, RSI and the White Rust Index.`));
K.push(NL(`Selected vegetation indices, selected texture features and the best TTFI.`));
K.push(NL(`Disease-specific feature set of each camera and the correlation between cameras.`));
K.push(P(`**Supporting studies.** Ma et al. (2026); Mahlein et al. (2013).`));
K.push(BOX(`Link to satellite monitoring (optional extension, not part of the six-month plan).`, `The subplot hyperspectral spectra can be convolved with the relative spectral response functions of Sentinel-2 and Resourcesat LISS-IV to simulate satellite band reflectance, and the selected wavelengths and indices can then be tested with these simulated bands. This approach was used for yellow rust with Sentinel-2 (Zheng et al., 2018) and for rice bacterial leaf blight with LISS-IV (Das et al., 2015); UAV data have also been used to bridge field and satellite scales (Revill et al., 2020; Blasch et al., 2023; Poblete et al., 2023; Yuan et al., 2025).`, 'EEF3E8', '2C5F2D'));
K.push(H1(`4. Objective 2 – Detection and severity discrimination through AI-based multimodal data fusion`));
K.push(P(`Objective 2 builds and compares predictive models on the 1536 post-symptomatic samples of each camera. Three tasks are modelled: (A) healthy vs diseased, (B) severity classes and (C) severity score. Two comparisons are made: (1) all 15 sensor sets with machine learning, feature-fusion neural networks and the pseudo-image networks; (2) on the hyperspectral feature groups, DT-EDNet against EfficientNet, ResNet18 and ConvNeXt V2, repeating the design of Ma et al. (2026) with plot-grouped validation.`));
K.push(...fig2('obj2', 'g06_obj2.png', `Flow chart of Objective 2 (Activities 2.1–2.6).`, 540));
K.push(...tab2('o2act', [[`Activity`, `Steps`, `Main output`],
[`2.1 Tasks and inputs`, `2.1.1–2.1.5`, `task labels; fused feature sets of 15 sensor sets; hyperspectral feature-group configurations`],
[`2.2 Machine-learning models`, `2.2.1–2.2.6`, `tuned support vector machine, random forest, extreme gradient boosting, k-nearest neighbours and partial least squares models`],
[`2.3 Deep-learning models`, `2.3.1–2.3.8`, `feature-fusion networks and pseudo-image networks (DT-EDNet, EfficientNet, ResNet18, ConvNeXt V2)`],
[`2.4 Evaluation`, `2.4.1–2.4.3`, `metric tables`],
[`2.5 Comparison, ablation and interpretation`, `2.5.1–2.5.4`, `best sensor set and model; contribution of each camera; module ablation; Shapley explanation`],
[`2.6 Robustness and maps`, `2.6.1–2.6.3`, `results by treatment; transfer tests; severity maps`]], [2900, 1300, 5106], `Activities of Objective 2.`, 17));
K.push(H2(`Activity 2.1 – Tasks and inputs`));
K.push(H3(`Step 2.1.1 – Three tasks and class balance`));
K.push(...tab2('s211', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Defines the three prediction problems and handles unequal class sizes.`],
[`Input`, `Post-symptomatic dataset with labels (Step A4).`],
[`Output → next step`, `Three labelled task datasets → all models.`]], [2200, 7106], `Step 2.1.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Task A, detection: healthy (grade 0) vs diseased (grade above 0).`));
K.push(NL(`Task B, severity classes: grades 0, 1, 3, 5, 7, 9 (merged if a class has fewer than 5% of samples).`));
K.push(NL(`Task C, regression: severity score.`));
K.push(NL(`Class weights (Step E6) for all classifiers; macro-averaged metrics.`));
K.push(P(`**Supporting studies.** Detection, severity classes and regression together: Tian et al. (2021), Feng et al. (2022), Abdulridha et al. (2023); three-class healthy, mild and severe classification: Yuan et al. (2025).`));
K.push(H3(`Step 2.1.2 – Fold-wise feature selection for each camera`));
K.push(...tab2('s212', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Features must be selected without the test replication.`],
[`Input`, `Feature groups of each camera; outer and inner folds (Activity F).`],
[`Output → next step`, `Disease-specific feature set of each camera for every fold and task → Step 2.1.3.`]], [2200, 7106], `Step 2.1.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`For every outer fold and task, repeat Activities 1.2–1.6 on the training part (label-based steps inside the inner folds).`));
K.push(NL(`Store the selected features of every fold (they are used for the stability analysis in Step 2.5.4).`));
K.push(P(`**Supporting studies.** Nested selection: Ambroise and McLachlan (2002), Varma and Simon (2006).`));
K.push(H3(`Step 2.1.3 – Feature-level fusion for the 15 sensor sets`));
K.push(...tab2('s213', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Combinations of cameras need one input vector per sample.`],
[`Input`, `Disease-specific feature sets of the cameras.`],
[`Output → next step`, `Fused feature set of each sensor set, fold and task → all models.`]], [2200, 7106], `Step 2.1.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Single camera (S1–S4): its disease-specific feature set is the input.`));
K.push(NL(`Combination (S5–S15): concatenate the feature sets of its cameras and apply the variance inflation factor rule (below 10) again across cameras.`));
K.push(NL(`Standardise with training statistics (Step E5).`));
K.push(P(`**Supporting studies.** Feature-level fusion of spectral, thermal and texture features: Feng et al. (2022), Liu et al. (2024); fusion levels: Ghamisi et al. (2019); input- and intermediate-level fusion: Maimaitijiang et al. (2020).`));
K.push(...fig2('combinations', 'g10_combinations.png', `The 15 sensor sets: 4 single cameras, 6 pairs, 4 triples and all four.`, 520));
K.push(...tab2('sets', [[`Set`, `Cameras`, `Question it answers`],
[`S1`, `hyperspectral`, `reference: what the most detailed camera achieves`],
[`S2`, `multispectral`, `what a low-cost, satellite-like camera achieves`],
[`S3`, `red–green–blue`, `what a consumer camera achieves`],
[`S4`, `thermal`, `what canopy temperature alone achieves`],
[`S5`, `hyperspectral + multispectral`, `whether the multispectral camera adds anything`],
[`S6`, `hyperspectral + red–green–blue`, `whether fine colour texture adds to spectra`],
[`S7`, `hyperspectral + thermal`, `whether temperature adds to spectra`],
[`S8`, `multispectral + red–green–blue`, `low-cost optical pair`],
[`S9`, `multispectral + thermal`, `low-cost spectral + thermal pair`],
[`S10`, `red–green–blue + thermal`, `cheapest pair`],
[`S11`, `hyperspectral + multispectral + red–green–blue`, `all optical cameras (is thermal needed?)`],
[`S12`, `hyperspectral + multispectral + thermal`, `is red–green–blue needed?`],
[`S13`, `hyperspectral + red–green–blue + thermal`, `is multispectral needed when hyperspectral is present?`],
[`S14`, `multispectral + red–green–blue + thermal`, `all low-cost cameras`],
[`S15`, `all four`, `full system; basis of the drop-one-camera ablation`]], [900, 3600, 4806], `The 15 sensor sets.`, 17));
K.push(H3(`Step 2.1.4 – Final compact set by sequential floating forward selection (SFFS) for the machine-learning models`));
K.push(...tab2('s214', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Different models use features differently, and a small final set improves generalisation and interpretation.`],
[`Input`, `Fused feature set (training part).`],
[`Output → next step`, `Optimum feature combination of each machine-learning model (at most 15 features) → Activity 2.2.`]], [2200, 7106], `Step 2.1.4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Run sequential floating forward selection (SFFS) wrapped around each machine-learning model, with macro-F1 (classes) or root-mean-square error (score) in the inner folds as criterion.`));
K.push(NL(`Limit the set to 15 features and keep the smallest subset within 1% of the best score.`));
K.push(NL(`The neural networks use the whole fused set, because they learn their own feature weights.`));
K.push(P(`**Supporting studies.** Floating search: Pudil et al. (1994); wrapper selection for disease models: Tian et al. (2021), Mustafa et al. (2023); backward wrapper selection for Fusarium head blight: Liu et al. (2020).`));
K.push(...tab2('sffsex', [[`Iteration (dummy)`, `Action`, `Subset`, `Inner macro-F1`],
[`1`, `add best single feature`, `WRI`, `0.52`],
[`2`, `add`, `WRI, OW 718 nm`, `0.60`],
[`3`, `add`, `WRI, OW 718 nm, ΔT`, `0.65`],
[`4`, `add`, `WRI, OW 718 nm, ΔT, TTFI`, `0.68`],
[`5`, `conditional removal: dropping OW 718 nm improves`, `WRI, ΔT, TTFI`, `0.69`],
[`…`, `continue until 15 features or no gain`, `…`, `…`]], [1600, 3600, 2500, 1606], `Worked example (dummy data): sequential floating forward selection adds features and removes a feature when it becomes redundant.`, 17));
K.push(...tab2('csffs', [[`Aspect`, `Sequential floating forward selection (SFFS)`],
[`Principle (how it works)`, `Adds the feature that most improves the model; after every addition it tries to remove previously added features and removes one if the model improves ("floating").`],
[`Problem it solves`, `Finds a small feature set suited to each model and corrects early choices that later become redundant.`],
[`Specification in this study`, `Wrapped around each machine-learning model; criterion macro-F1 or root-mean-square error in the inner folds; at most 15 features; smallest subset within 1% of the best.`],
[`Hyper-parameters and how they are tuned`, `Maximum subset size (15) and tolerance (1%); fixed to keep at least about 60 training samples per feature.`],
[`Data on which it works well`, `Moderate candidate sets (20–40 features) after the earlier stages; not for hundreds of features.`],
[`Why it was selected`, `Gives the model-specific final set recommended in the staged approach while keeping the number of candidates small.`],
[`Key references`, `Pudil et al. (1994); Tian et al. (2021)`]], [2300, 7006], `Method card – Sequential floating forward selection (SFFS).`, 16));
K.push(H3(`Step 2.1.5 – Hyperspectral feature-group configurations for the network comparison`));
K.push(...tab2('s215', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The DT-EDNet study compared networks on separate feature groups and on their combinations; the same design shows which hyperspectral feature types help each network.`],
[`Input`, `Fold-wise optimal wavelengths, selected indices, selected texture features and best TTFI of the hyperspectral camera.`],
[`Output → next step`, `Six input configurations → pseudo-image networks (Activity 2.3) and the best machine-learning model as reference.`]], [2200, 7106], `Step 2.1.5 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`OW: optimal wavelengths only.`));
K.push(NL(`VI: selected vegetation indices only.`));
K.push(NL(`TF: selected texture features only.`));
K.push(NL(`OW + VI.`));
K.push(NL(`OW + TTFI.`));
K.push(NL(`OW + VI + TTFI (the best combination in Ma et al., 2026).`));
K.push(P(`**Supporting studies.** Feature-group configurations: Ma et al. (2026); vegetation index and texture fusion for yellow rust: Guo et al. (2021).`));
K.push(H2(`Activity 2.2 – Machine-learning models`));
K.push(P(`Five machine-learning model families are used for classification and their regression versions for the severity score. They cover kernel, tree-ensemble, boosting, instance-based and latent-variable approaches, so that conclusions do not depend on one type of model.`));
K.push(H3(`Step 2.2.1 – Support vector machine (SVM) and support vector regression (SVR)`));
K.push(...tab2('s221', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A robust classifier and regressor for a few hundred to a few thousand samples with correlated features.`],
[`Input`, `Optimum feature combination (standardised).`],
[`Output → next step`, `Predictions on the test replication → Activity 2.4.`]], [2200, 7106], `Step 2.2.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Radial basis function kernel; class weights for classes; one-vs-one for several classes.`));
K.push(NL(`Tune C, γ (and ε for regression) by grid search in the inner folds (Table ${T('mlgrid')}).`));
K.push(P(`**Supporting studies.** Cortes and Vapnik (1995); Mountrakis et al. (2011); disease applications: Tian et al. (2021), Mustafa et al. (2023), Yuan et al. (2025).`));
K.push(...tab2('csvm', [[`Aspect`, `Support vector machine (SVM) and support vector regression (SVR)`],
[`Principle (how it works)`, `Finds the boundary with the largest margin between classes (or a tube of width ε around the regression line); the kernel maps the data so that curved boundaries become possible.`],
[`Problem it solves`, `Non-linear classification and regression with limited samples.`],
[`Specification in this study`, `Radial basis function kernel; class weights; standardised inputs.`],
[`Hyper-parameters and how they are tuned`, `C ∈ {0.1, 1, 10, 100}; γ ∈ {0.001, 0.01, 0.1, scale}; ε ∈ {0.1, 0.5} for regression; grid search in the inner folds.`],
[`Data on which it works well`, `Small to medium samples (hundreds to thousands), moderate numbers of standardised features.`],
[`Why it was selected`, `Among the most accurate classifiers in remote sensing for limited training data.`],
[`Key references`, `Cortes and Vapnik (1995); Mountrakis et al. (2011)`]], [2300, 7006], `Method card – Support vector machine (SVM) and support vector regression (SVR).`, 16));
K.push(H3(`Step 2.2.2 – Random forest (RF)`));
K.push(...tab2('s222', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A robust, little-tuned model that handles non-linear effects and gives feature importance.`],
[`Input`, `Optimum feature combination.`],
[`Output → next step`, `Predictions → Activity 2.4.`]], [2200, 7106], `Step 2.2.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`500 trees; class weights; tune the number of features per split and the minimum leaf size.`));
K.push(P(`**Supporting studies.** Breiman (2001); Belgiu and Drăguţ (2016); disease applications: Abdulridha et al. (2023), Liu et al. (2024), Yu et al. (2021), Yuan et al. (2025).`));
K.push(...tab2('crf', [[`Aspect`, `Random forest (RF)`],
[`Principle (how it works)`, `Averages many decision trees, each grown on a bootstrap sample and choosing among a random subset of features at every split.`],
[`Problem it solves`, `Non-linear classification and regression that resists overfitting and noise.`],
[`Specification in this study`, `500 trees; class weights; out-of-bag error monitored.`],
[`Hyper-parameters and how they are tuned`, `Features per split ∈ {√p, 0.3p}; minimum leaf size ∈ {1, 3, 5}; grid search in the inner folds.`],
[`Data on which it works well`, `Tabular data with mixed, noisy features; small and large samples.`],
[`Why it was selected`, `Little tuning, stable, widely used in UAV disease studies.`],
[`Key references`, `Breiman (2001); Belgiu and Drăguţ (2016)`]], [2300, 7006], `Method card – Random forest (RF).`, 16));
K.push(H3(`Step 2.2.3 – Extreme gradient boosting (XGBoost)`));
K.push(...tab2('s223', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Often the most accurate tree model on tabular features.`],
[`Input`, `Optimum feature combination.`],
[`Output → next step`, `Predictions → Activity 2.4.`]], [2200, 7106], `Step 2.2.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Tune the number of trees, depth and learning rate; subsample 0.8; sample weights from the class weights.`));
K.push(P(`**Supporting studies.** Chen and Guestrin (2016).`));
K.push(...tab2('cxgb', [[`Aspect`, `Extreme gradient boosting (XGBoost)`],
[`Principle (how it works)`, `Adds small trees one after another; each new tree corrects the errors of the previous ones, with regularisation of tree complexity.`],
[`Problem it solves`, `High-accuracy non-linear modelling of tabular features.`],
[`Specification in this study`, `Subsample 0.8; column subsample 0.8; early stopping on the inner validation plots.`],
[`Hyper-parameters and how they are tuned`, `Trees ∈ {200, 500}; depth ∈ {3, 5}; learning rate ∈ {0.05, 0.1}; grid search in the inner folds.`],
[`Data on which it works well`, `Tabular data with non-linear interactions; medium samples.`],
[`Why it was selected`, `Strong benchmark model; complements random forest (boosting vs averaging).`],
[`Key references`, `Chen and Guestrin (2016)`]], [2300, 7006], `Method card – Extreme gradient boosting (XGBoost).`, 16));
K.push(H3(`Step 2.2.4 – k-nearest neighbours (k-NN)`));
K.push(...tab2('s224', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A simple reference model that predicts from the most similar training samples.`],
[`Input`, `Optimum feature combination (standardised).`],
[`Output → next step`, `Predictions → Activity 2.4.`]], [2200, 7106], `Step 2.2.4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Tune k and the weighting (uniform or by distance).`));
K.push(P(`**Supporting studies.** Cover and Hart (1967); Yuan et al. (2025).`));
K.push(...tab2('cknn', [[`Aspect`, `k-nearest neighbours (k-NN)`],
[`Principle (how it works)`, `Predicts the class (majority vote) or score (mean) of the k most similar training samples in feature space.`],
[`Problem it solves`, `Simple non-parametric reference model.`],
[`Specification in this study`, `Euclidean distance on standardised features.`],
[`Hyper-parameters and how they are tuned`, `k ∈ {3, 5, 7, 9, 11}; uniform or distance weights; grid search in the inner folds.`],
[`Data on which it works well`, `Compact, standardised feature sets; low-dimensional data.`],
[`Why it was selected`, `Transparent baseline; shows whether more complex models are needed.`],
[`Key references`, `Cover and Hart (1967)`]], [2300, 7006], `Method card – k-nearest neighbours (k-NN).`, 16));
K.push(H3(`Step 2.2.5 – Partial least squares discriminant analysis (PLS-DA) and regression (PLSR)`));
K.push(...tab2('s225', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The standard chemometric model for correlated spectral features.`],
[`Input`, `Optimum feature combination (standardised).`],
[`Output → next step`, `Predictions → Activity 2.4.`]], [2200, 7106], `Step 2.2.5 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Tune the number of latent variables (1–15) in the inner folds.`));
K.push(P(`**Supporting studies.** Wold et al. (2001); Barker and Rayens (2003); Guo et al. (2021).`));
K.push(...tab2('cpls', [[`Aspect`, `Partial least squares discriminant analysis (PLS-DA) and regression (PLSR)`],
[`Principle (how it works)`, `Projects correlated features onto a few latent variables that have maximum covariance with the target, then fits a linear model on them.`],
[`Problem it solves`, `Linear modelling of many correlated predictors without collinearity problems.`],
[`Specification in this study`, `Standardised inputs; classes coded as dummy variables for discriminant analysis.`],
[`Hyper-parameters and how they are tuned`, `Number of latent variables 1–15, chosen in the inner folds.`],
[`Data on which it works well`, `Spectral data with strong collinearity; linear or near-linear relations.`],
[`Why it was selected`, `Linear reference used in most hyperspectral disease studies (for example yellow rust monitoring by Guo et al., 2021).`],
[`Key references`, `Wold et al. (2001); Barker and Rayens (2003)`]], [2300, 7006], `Method card – Partial least squares discriminant analysis (PLS-DA) and regression (PLSR).`, 16));
K.push(H3(`Step 2.2.6 – Tuning grids of the machine-learning models`));
K.push(...tab2('s226', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `All models must be tuned in the same honest way.`],
[`Input`, `Inner folds (Step F2).`],
[`Output → next step`, `Tuned hyper-parameters of every model, fold and sensor set → final training.`]], [2200, 7106], `Step 2.2.6 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Use the grids in Table ${T('mlgrid')}; choose the combination with the best mean inner score.`));
K.push(P(`**Supporting studies.** Kuhn and Johnson (2013); Cawley and Talbot (2010).`));
K.push(...tab2('mlgrid', [[`Model`, `Tasks`, `Hyper-parameters tuned (inner cross-validation)`],
[`Support vector machine / regression`, `A, B / C`, `C ∈ {0.1, 1, 10, 100}; γ ∈ {0.001, 0.01, 0.1, scale}; ε ∈ {0.1, 0.5} (regression)`],
[`Random forest`, `A, B, C`, `500 trees; features per split ∈ {√p, 0.3p}; minimum leaf size ∈ {1, 3, 5}`],
[`Extreme gradient boosting`, `A, B, C`, `trees ∈ {200, 500}; depth ∈ {3, 5}; learning rate ∈ {0.05, 0.1}; subsample 0.8`],
[`k-nearest neighbours`, `A, B, C`, `k ∈ {3, 5, 7, 9, 11}; uniform or distance weights`],
[`Partial least squares (discriminant analysis / regression)`, `A, B / C`, `number of latent variables 1–15`]], [3100, 1100, 5106], `Machine-learning models and tuning grids.`, 17));
K.push(H2(`Activity 2.3 – Deep-learning models`));
K.push(P(`Two kinds of networks are used. Feature-fusion networks (DNN-F1, DNN-F2) take the fused feature vector directly. Pseudo-image networks (DT-EDNet and the three comparison networks) first reshape the feature vector into a small two-dimensional "image", as in Ma et al. (2026). All networks are trained on exactly the same folds as the machine-learning models.`));
K.push(H3(`Step 2.3.1 – Deep neural network with input-level feature fusion (DNN-F1)`));
K.push(...tab2('s231', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Learns non-linear interactions between the features of different cameras from one concatenated vector.`],
[`Input`, `Fused feature set (standardised).`],
[`Output → next step`, `Predictions → Activity 2.4.`]], [2200, 7106], `Step 2.3.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Concatenate the features of all cameras of the set.`));
K.push(NL(`Two dense layers (64 and 32 units) with batch normalisation, ReLU activation and dropout, then the output layer (softmax for classes, linear for the score).`));
K.push(NL(`Adam optimiser, learning rate 0.001, weight decay 10^{−4}, batch size 32, up to 500 epochs with early stopping (patience 30) on the inner validation plots; five random seeds averaged.`));
K.push(P(`**Supporting studies.** Maimaitijiang et al. (2020); Kingma and Ba (2015); Srivastava et al. (2014); Ioffe and Szegedy (2015).`));
K.push(H3(`Step 2.3.2 – Deep neural network with intermediate-level feature fusion (DNN-F2)`));
K.push(...tab2('s232', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Lets each camera be processed separately before fusion and learns how much each camera contributes.`],
[`Input`, `Selected features of each camera in the set (standardised).`],
[`Output → next step`, `Predictions and camera attention weights → Activities 2.4 and 2.5.`]], [2200, 7106], `Step 2.3.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`One small sub-network per camera (one or two dense layers of 16–32 units).`));
K.push(NL(`A squeeze-and-excitation (SE) attention block gives each camera branch a learned weight.`));
K.push(NL(`Concatenate the weighted branches → dense layer of 32 units → output; same training as DNN-F1; used only for sets with two or more cameras.`));
K.push(P(`**Supporting studies.** Maimaitijiang et al. (2020); squeeze-and-excitation: Hu et al. (2018).`));
K.push(...fig2('dnn', 'g21_dnn.png', `Feature-fusion networks: DNN-F1 (input-level fusion) and DNN-F2 (intermediate fusion with camera attention).`, 540));
K.push(...tab2('cdnnf', [[`Aspect`, `Feature-fusion deep neural networks (DNN-F1 and DNN-F2)`],
[`Principle (how it works)`, `Fully connected layers learn weighted, non-linear combinations of the input features; DNN-F2 first learns a representation for each camera and weights the cameras with attention.`],
[`Problem it solves`, `Non-linear fusion of features from several cameras; DNN-F2 also shows which camera the model relies on.`],
[`Specification in this study`, `DNN-F1: 64–32 units; DNN-F2: 16–32 units per camera branch, attention block, 32 units; batch normalisation; dropout; class-weighted cross-entropy or mean squared error.`],
[`Hyper-parameters and how they are tuned`, `Units ∈ {32, 64} (first layer) and dropout ∈ {0.2, 0.3, 0.4}, tuned in the inner folds; epochs by early stopping.`],
[`Data on which it works well`, `About a thousand samples with tens of features; multi-sensor feature vectors.`],
[`Why it was selected`, `Compact enough for the sample size; intermediate fusion was better than input fusion in multi-sensor UAV data (Maimaitijiang et al., 2020).`],
[`Key references`, `Maimaitijiang et al. (2020); Hu et al. (2018)`]], [2300, 7006], `Method card – Feature-fusion deep neural networks (DNN-F1 and DNN-F2).`, 16));
K.push(H3(`Step 2.3.3 – Pseudo-image construction`));
K.push(...tab2('s233', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Convolutional and transformer networks need a two-dimensional input, but each sample is a feature vector.`],
[`Input`, `Fused feature set or hyperspectral configuration (standardised).`],
[`Output → next step`, `One-channel pseudo-image of k × k pixels per sample → Steps 2.3.4–2.3.7.`]], [2200, 7106], `Step 2.3.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Order the features by group and, within the spectral group, by wavelength (optimal wavelengths, indices, texture, TTFI, then other cameras), so that neighbouring pixels hold related features.`));
K.push(NL(`Choose k = the smallest integer with k² ≥ number of features (minimum 3); fill the k × k grid row by row.`));
K.push(NL(`Fill the remaining pixels with zeros (zero is the training mean after standardisation, so padding adds no information).`));
K.push(NL(`Example: 22 features → 5 × 5 image with 3 padded pixels (Figure ${F('pseudo')}).`));
K.push(P(`**Supporting studies.** Pseudo-two-dimensional input of spectral features: Ma et al. (2026); arranging non-image features as images for convolutional networks: Sharma et al. (2019).`));
K.push(...fig2('pseudo', 'g18_pseudoimage.png', `Construction of a pseudo-image from a standardised feature vector (dummy values).`, 540));
K.push(...tab2('cpseudo', [[`Aspect`, `Pseudo-image (feature-to-image) representation`],
[`Principle (how it works)`, `Places the features of one sample on a small grid so that convolution and attention can relate neighbouring and distant features.`],
[`Problem it solves`, `Allows image networks to be applied to tabular features.`],
[`Specification in this study`, `Group-and-wavelength ordering; k = ⌈√p⌉ (minimum 3); zero padding after standardisation; one channel.`],
[`Hyper-parameters and how they are tuned`, `No tuning (fixed ordering, so results are reproducible).`],
[`Data on which it works well`, `Ordered features such as spectra, where neighbours are related.`],
[`Why it was selected`, `Needed to reproduce the DT-EDNet design; the fixed ordering keeps related features together.`],
[`Key references`, `Ma et al. (2026); Sharma et al. (2019)`]], [2300, 7006], `Method card – Pseudo-image (feature-to-image) representation.`, 16));
K.push(H3(`Step 2.3.4 – DT-EDNet (Dual Transformer Early Detection Network)`));
K.push(...tab2('s234', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Captures local relations between neighbouring features (convolution and attention) and long-range relations between distant features (self-attention) in one network.`],
[`Input`, `Pseudo-images.`],
[`Output → next step`, `Predictions → Activity 2.4; module ablation → Step 2.5.3.`]], [2200, 7106], `Step 2.3.4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Embedding: 3 × 3 convolution (stride 1) to 128 channels.`));
K.push(NL(`Squeeze-and-excitation block: global average pooling of each channel → two small dense layers → sigmoid weight per channel → channels re-weighted.`));
K.push(NL(`Tokens: flatten the k × k map into k² tokens of length 128 and add a learnable class token (and position embedding).`));
K.push(NL(`Dual Transformer Group: one Kernel Transformer Block (convolution with the convolutional block attention module, CBAM: channel attention then spatial attention) followed by four Token Transformer Blocks (layer normalisation → multi-head self-attention with 4 heads → layer normalisation → feed-forward network, each with a residual connection); dropout 0.03.`));
K.push(NL(`Head: layer normalisation of the class token → linear layer (softmax for classes, one linear output for the score).`));
K.push(P(`**Supporting studies.** DT-EDNet: Ma et al. (2026); squeeze-and-excitation: Hu et al. (2018); CBAM: Woo et al. (2018); self-attention and transformers: Vaswani et al. (2017); class token: Dosovitskiy et al. (2021).`));
K.push(...fig2('dtednet', 'g19_dtednet.png', `Architecture of DT-EDNet (after Ma et al., 2026) and the role of its three attention mechanisms.`, 560));
K.push(EQ(`Attention(Q, K, V) = softmax( Q K^{T} / √d ) V`));
K.push(P(`In self-attention every token forms a query Q, a key K and a value V; the softmax of the scaled products Q K^{T} decides how much each token takes from every other token, d being the token length per head (128 / 4 = 32). This is how a red-edge wavelength can be related directly to a texture feature placed far away on the pseudo-image.`));
K.push(...tab2('cdtednet', [[`Aspect`, `DT-EDNet (Dual Transformer Early Detection Network)`],
[`Principle (how it works)`, `A hybrid network: convolution embeds the pseudo-image, squeeze-and-excitation re-weights channels, the Kernel Transformer Block (convolution + CBAM) learns local spatial–channel patterns and the Token Transformer Blocks (multi-head self-attention) learn global relations; the class token summarises the sample.`],
[`Problem it solves`, `Models both local and long-range interactions among selected spectral, index and texture features.`],
[`Specification in this study`, `Embedding 128; SE block; 1 Kernel Transformer Block + 4 Token Transformer Blocks; 4 heads; dropout 0.03; trained from scratch.`],
[`Hyper-parameters and how they are tuned`, `Fixed architecture as published; learning rate and dropout tuned in the inner folds (Step 2.3.8).`],
[`Data on which it works well`, `Sets of a few to a few tens of ordered features with complex interactions; best with thousands of samples.`],
[`Why it was selected`, `Highest accuracy on rice blast (overall accuracy 95.25% with optimal wavelengths + indices + TTFI) against EfficientNet, ResNet18 and ConvNeXt V2 (Ma et al., 2026); tested here under plot-grouped validation.`],
[`Key references`, `Ma et al. (2026); Hu et al. (2018); Woo et al. (2018); Vaswani et al. (2017)`]], [2300, 7006], `Method card – DT-EDNet (Dual Transformer Early Detection Network).`, 16));
K.push(H3(`Step 2.3.5 – EfficientNet (comparison network)`));
K.push(...tab2('s235', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A modern, efficient convolutional network used as a comparison in the DT-EDNet study.`],
[`Input`, `Pseudo-images.`],
[`Output → next step`, `Predictions → Activity 2.4.`]], [2200, 7106], `Step 2.3.5 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`EfficientNet-B0: mobile inverted bottleneck blocks with depthwise convolution and squeeze-and-excitation.`));
K.push(NL(`Stem changed to a 3 × 3 convolution with stride 1 and one input channel (the input is only a few pixels wide).`));
K.push(NL(`Global average pooling → linear head; trained from scratch.`));
K.push(P(`**Supporting studies.** Tan and Le (2019); Ma et al. (2026).`));
K.push(H3(`Step 2.3.6 – ResNet18 (comparison network)`));
K.push(...tab2('s236', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A classic residual convolutional network used as a comparison.`],
[`Input`, `Pseudo-images.`],
[`Output → next step`, `Predictions → Activity 2.4.`]], [2200, 7106], `Step 2.3.6 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Four stages of two basic residual blocks (two 3 × 3 convolutions with an identity shortcut).`));
K.push(NL(`Stem changed to a 3 × 3 convolution with stride 1 and no max-pooling.`));
K.push(NL(`Global average pooling → linear head; trained from scratch.`));
K.push(P(`**Supporting studies.** He et al. (2016); Ma et al. (2026).`));
K.push(H3(`Step 2.3.7 – ConvNeXt V2 (comparison network)`));
K.push(...tab2('s237', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A recent convolutional network that borrows design ideas from transformers, used as a comparison.`],
[`Input`, `Pseudo-images.`],
[`Output → next step`, `Predictions → Activity 2.4.`]], [2200, 7106], `Step 2.3.7 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`ConvNeXt V2-Atto (smallest version, about 3.7 million parameters): blocks with 7 × 7 depthwise convolution, layer normalisation and a feed-forward network with global response normalisation.`));
K.push(NL(`Stem changed to stride 1; global average pooling → linear head; trained from scratch.`));
K.push(P(`**Supporting studies.** Woo et al. (2023); Ma et al. (2026).`));
K.push(...fig2('cnns', 'g20_cnns.png', `The three comparison networks with the changes made for small pseudo-images.`, 540));
K.push(...tab2('ccnn', [[`Aspect`, `Comparison networks: EfficientNet-B0, ResNet18 and ConvNeXt V2-Atto`],
[`Principle (how it works)`, `Convolutional networks: EfficientNet scales depth, width and resolution together and uses squeeze-and-excitation; ResNet adds identity shortcuts so deep networks train well; ConvNeXt V2 uses large depthwise kernels and global response normalisation.`],
[`Problem it solves`, `Benchmarks that show whether the transformer parts of DT-EDNet add accuracy over strong convolutional designs.`],
[`Specification in this study`, `One input channel; stride-1 stems; global average pooling; linear head; trained from scratch with the same settings as DT-EDNet.`],
[`Hyper-parameters and how they are tuned`, `Same tuning budget as DT-EDNet (learning rate and dropout in the inner folds).`],
[`Data on which it works well`, `Image-like inputs; large datasets (risk of overfitting with about a thousand samples, controlled by early stopping and regularisation).`],
[`Why it was selected`, `Exactly the comparison set used by Ma et al. (2026); covers classic, efficient and modern convolutional designs.`],
[`Key references`, `He et al. (2016); Tan and Le (2019); Woo et al. (2023); Kattenborn et al. (2021)`]], [2300, 7006], `Method card – Comparison networks: EfficientNet-B0, ResNet18 and ConvNeXt V2-Atto.`, 16));
K.push(H3(`Step 2.3.8 – Common training protocol and tuning of the pseudo-image networks`));
K.push(...tab2('s238', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A fair comparison requires identical training settings for all four networks.`],
[`Input`, `Pseudo-images of the training part; inner validation plots.`],
[`Output → next step`, `Trained networks (five seeds each) → Activity 2.4.`]], [2200, 7106], `Step 2.3.8 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Optimiser: AdamW, initial learning rate 6 × 10^{−4}, weight decay 1 × 10^{−5}; cosine annealing of the learning rate to 1 × 10^{−6} over 300 epochs; batch size 32.`));
K.push(NL(`Loss: cross-entropy with label smoothing 0.01 and class weights (classes); mean squared error (score).`));
K.push(NL(`Gradient clipping at a maximum norm of 1.2; early stopping with patience 60 epochs and minimum improvement 5 × 10^{−5}.`));
K.push(NL(`Model selection on the inner validation plots (macro-F1 for classes because the classes are unequal; root-mean-square error for the score), not on a random 10% of samples.`));
K.push(NL(`Tuning: learning rate ∈ {3 × 10^{−4}, 6 × 10^{−4}, 1 × 10^{−3}} and dropout ∈ {0.03, 0.1, 0.3}, same grid for all four networks.`));
K.push(NL(`Five random seeds (42 and four others); report mean ± standard deviation.`));
K.push(P(`**Supporting studies.** Training settings: Ma et al. (2026); AdamW: Loshchilov and Hutter (2019); cosine annealing: Loshchilov and Hutter (2017); label smoothing: Szegedy et al. (2016), Müller et al. (2019); gradient clipping: Pascanu et al. (2013).`));
K.push(...tab2('ctrain', [[`Aspect`, `Training techniques (AdamW, cosine annealing, label smoothing, gradient clipping, early stopping)`],
[`Principle (how it works)`, `AdamW adapts the step size of every weight and applies weight decay separately; cosine annealing lowers the learning rate smoothly; label smoothing replaces hard 0/1 targets with slightly softened ones; gradient clipping limits very large updates; early stopping ends training when the validation score stops improving.`],
[`Problem it solves`, `Stable training and less overfitting on a small dataset.`],
[`Specification in this study`, `Values of Step 2.3.8 (from Ma et al., 2026).`],
[`Hyper-parameters and how they are tuned`, `Learning rate and dropout tuned; other values fixed as published.`],
[`Data on which it works well`, `Neural networks trained from scratch on small to medium datasets.`],
[`Why it was selected`, `Reproduces the published protocol, so differences come from the data and validation design, not from different training.`],
[`Key references`, `Loshchilov and Hutter (2017, 2019); Müller et al. (2019); Pascanu et al. (2013)`]], [2300, 7006], `Method card – Training techniques (AdamW, cosine annealing, label smoothing, gradient clipping, early stopping).`, 16));
K.push(H2(`Activity 2.4 – Evaluation`));
K.push(H3(`Step 2.4.1 – Classification metrics`));
K.push(...tab2('s241', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Accuracy must reflect unequal classes and ordered grades.`],
[`Input`, `Predictions on the three test replications.`],
[`Output → next step`, `Metric tables → Activity 2.5.`]], [2200, 7106], `Step 2.4.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Task A: overall accuracy, sensitivity, specificity, F1 and area under the receiver operating characteristic curve (AUC).`));
K.push(NL(`Task B: overall accuracy, Cohen's kappa, quadratic-weighted kappa (ordered grades), macro-averaged recall and F1, per-class precision, recall and F1, confusion matrix and the share of predictions within one grade of the true grade.`));
K.push(P(`**Supporting studies.** Cohen (1960, 1968); Sokolova and Lapalme (2009); Fawcett (2006); the metrics of Ma et al. (2026) (overall accuracy, kappa, macro recall, macro-F1, per-class scores) are all included.`));
K.push(EQ(`OA = correct / N;    precision = TP / (TP + FP);    recall = TP / (TP + FN);    F1 = 2 × precision × recall / (precision + recall)`));
K.push(EQ(`κ = (p_{o} − p_{e}) / (1 − p_{e});    κ_{w} = 1 − Σ w_{ij} O_{ij} / Σ w_{ij} E_{ij},   w_{ij} = (i − j)^{2} / (k − 1)^{2}`));
K.push(H3(`Step 2.4.2 – Regression metrics`));
K.push(...tab2('s242', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The severity-score models need error measures in score units.`],
[`Input`, `Predicted and observed scores of the test replications.`],
[`Output → next step`, `Metric tables → Activity 2.5.`]], [2200, 7106], `Step 2.4.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Coefficient of determination (R²), root-mean-square error (RMSE) and ratio of performance to deviation (RPD = standard deviation of observed scores / RMSE).`));
K.push(P(`**Supporting studies.** Chang et al. (2001); Guo et al. (2021); Feng et al. (2022).`));
K.push(EQ(`R^{2} = 1 − Σ (y − ŷ)^{2} / Σ (y − ȳ)^{2};    RMSE = √[ (1/n) Σ (y − ŷ)^{2} ];    RPD = SD_{y} / RMSE`));
K.push(H3(`Step 2.4.3 – Worked example of the metrics`));
K.push(...tab2('s243', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Shows how the numbers in the result tables are obtained.`],
[`Input`, `Dummy confusion matrix and dummy predictions.`],
[`Output → next step`, `Example values (below).`]], [2200, 7106], `Step 2.4.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Classification: from the confusion matrix in Figure ${F('dummycm')} (532 test samples), 396 are on the diagonal, so overall accuracy = 396 / 532 = 0.744; chance agreement p_{e} = 0.182, so κ = (0.744 − 0.182) / (1 − 0.182) = 0.687; quadratic-weighted kappa = 0.937 (most errors are between neighbouring grades); macro-F1 = 0.733; 97.4% of predictions are within one grade.`));
K.push(NL(`Regression: for eight dummy subplots with observed scores 0, 1, 3, 5, 7, 9, 3, 5 and predictions 0.4, 1.6, 2.5, 5.8, 6.1, 8.2, 3.9, 4.4: R² = 0.94, RMSE = 0.71 and RPD = 3.00 / 0.71 = 4.2.`));
K.push(P(`**Supporting studies.** Cohen (1960); Sokolova and Lapalme (2009); Chang et al. (2001).`));
K.push(...fig2('dummycm', 'g22_dummy_cm.png', `Dummy confusion matrix of one test replication (six grades).`, 360));
K.push(...tab2('cmetrics', [[`Aspect`, `Evaluation metrics`],
[`Principle (how it works)`, `Overall accuracy counts correct predictions; kappa corrects it for chance; weighted kappa gives partial credit to near misses between ordered grades; F1 combines precision and recall per class; R², RMSE and RPD describe regression error.`],
[`Problem it solves`, `Measures performance fairly when classes are unequal and ordered.`],
[`Specification in this study`, `Computed on the pooled predictions of the three test replications and per fold; mean ± standard deviation over folds and seeds.`],
[`Hyper-parameters and how they are tuned`, `None.`],
[`Data on which it works well`, `Classification with unequal, ordered classes; continuous scores.`],
[`Why it was selected`, `Covers the metrics of the DT-EDNet study and the extra ones needed for ordered grades and regression.`],
[`Key references`, `Cohen (1960, 1968); Sokolova and Lapalme (2009); Chang et al. (2001)`]], [2300, 7006], `Method card – Evaluation metrics.`, 16));
K.push(H2(`Activity 2.5 – Comparison, ablation and interpretation`));
K.push(H3(`Step 2.5.1 – Ranking of sensor sets and models`));
K.push(...tab2('s251', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Identifies the best sensor set and model for each task.`],
[`Input`, `Metric tables of 15 sets × models × tasks.`],
[`Output → next step`, `Best sensor set and model per task → conclusions and maps.`]], [2200, 7106], `Step 2.5.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Rank the 15 sets by macro-F1 (Task B), AUC (Task A) and RMSE (Task C) for each model.`));
K.push(NL(`Compare the best machine-learning, best feature-fusion network and best pseudo-image network.`));
K.push(NL(`Call a difference real only if it is larger than the fold-to-fold standard deviation and appears in all three folds.`));
K.push(P(`**Supporting studies.** Feng et al. (2022); Maimaitijiang et al. (2020); Ma et al. (2026).`));
K.push(H3(`Step 2.5.2 – Fusion gain and drop-one-camera ablation`));
K.push(...tab2('s252', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Answers directly whether a camera is worth flying.`],
[`Input`, `Metrics of single cameras and combinations.`],
[`Output → next step`, `Fusion gains and the contribution of each camera → conclusions.`]], [2200, 7106], `Step 2.5.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Fusion gain = metric of a combination minus the metric of its best single camera.`));
K.push(NL(`Remove one camera at a time from S15 and record the drop in macro-F1 and R².`));
K.push(NL(`Report the camera attention weights of DNN-F2.`));
K.push(P(`**Supporting studies.** Ablation of feature groups: Ma et al. (2026); fusion gain: Feng et al. (2022), Maimaitijiang et al. (2020).`));
K.push(H3(`Step 2.5.3 – Network comparison on the hyperspectral configurations and DT-EDNet module ablation`));
K.push(...tab2('s253', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Shows whether DT-EDNet is better than the comparison networks under plot-grouped validation and which of its modules matter.`],
[`Input`, `Results of the four pseudo-image networks on the six configurations (Step 2.1.5); the best machine-learning model on the same inputs.`],
[`Output → next step`, `Network comparison table; ablation table → conclusions.`]], [2200, 7106], `Step 2.5.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Compare DT-EDNet, EfficientNet, ResNet18, ConvNeXt V2 and the best machine-learning model on the six configurations (overall accuracy, kappa, macro recall, macro-F1, per-class F1, RMSE).`));
K.push(NL(`Ablation on the best configuration: DT-EDNet without the squeeze-and-excitation block, without the Dual Transformer Group, and without both.`));
K.push(NL(`Report mean ± standard deviation over three folds × five seeds.`));
K.push(P(`**Supporting studies.** Network comparison and module ablation: Ma et al. (2026).`));
K.push(...tab2('ablationt', [[`Model (template)`, `Overall accuracy`, `Kappa`, `Macro recall`, `Macro-F1`],
[`DT-EDNet (full)`, `…`, `…`, `…`, `…`],
[`without squeeze-and-excitation block`, `…`, `…`, `…`, `…`],
[`without Dual Transformer Group`, `…`, `…`, `…`, `…`],
[`without both`, `…`, `…`, `…`, `…`]], [3400, 1500, 1300, 1500, 1606], `Template for the DT-EDNet module ablation (same folds and seeds for all rows).`, 17));
K.push(H3(`Step 2.5.4 – Shapley additive explanations (SHAP) and selection stability`));
K.push(...tab2('s254', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Shows which features drive the best models and how stable the selected features are.`],
[`Input`, `Best models; selected features of every fold.`],
[`Output → next step`, `Feature-importance figures; stability table → Objective 1 discussion.`]], [2200, 7106], `Step 2.5.4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Compute SHAP values of the best machine-learning model of each task; summarise the mean |SHAP| per feature and per camera.`));
K.push(NL(`Count how often every feature is selected over the three folds; final feature lists contain features selected in at least two of three folds.`));
K.push(P(`**Supporting studies.** Lundberg and Lee (2017); Lundberg et al. (2020); Nogueira et al. (2018).`));
K.push(...tab2('cablation', [[`Aspect`, `Ablation and Shapley interpretation`],
[`Principle (how it works)`, `Ablation removes one part (a camera, a feature group or a network module) and measures the loss; SHAP divides each prediction among the features.`],
[`Problem it solves`, `Shows what each camera, feature type and network module contributes.`],
[`Specification in this study`, `Drop-one-camera from S15; DT-EDNet without SE, without Dual Transformer Group, without both; SHAP on the best machine-learning models.`],
[`Hyper-parameters and how they are tuned`, `None.`],
[`Data on which it works well`, `Any trained model on the same folds.`],
[`Why it was selected`, `Direct, easy-to-explain evidence of contribution; both used in the DT-EDNet study.`],
[`Key references`, `Ma et al. (2026); Lundberg and Lee (2017)`]], [2300, 7006], `Method card – Ablation and Shapley interpretation.`, 16));
K.push(H2(`Activity 2.6 – Robustness and maps`));
K.push(H3(`Step 2.6.1 – Performance by treatment`));
K.push(...tab2('s261', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A model may work for one variety or crop age and fail for another.`],
[`Input`, `Test predictions with treatment codes.`],
[`Output → next step`, `Treatment-wise metric tables.`]], [2200, 7106], `Step 2.6.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Report the metrics for each variety, inoculation timing and date.`));
K.push(P(`**Supporting studies.** Liu et al. (2024); Blasch et al. (2023); Feng et al. (2022).`));
K.push(H3(`Step 2.6.2 – Leave-one-variety-out and leave-one-timing-out tests`));
K.push(...tab2('s262', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Tests whether models transfer to a variety or crop age not seen in training.`],
[`Input`, `Best machine-learning and best deep-learning model of the three best sensor sets.`],
[`Output → next step`, `Transfer results → conclusions on robustness.`]], [2200, 7106], `Step 2.6.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Train on two varieties and test on the third (mainly V1 ↔ V2, because the resistant variety has few diseased samples).`));
K.push(NL(`Train on three inoculation timings and test on the fourth.`));
K.push(P(`**Supporting studies.** Blocked validation for extrapolation: Roberts et al. (2017); independent-year test: Ma et al. (2026).`));
K.push(H3(`Step 2.6.3 – Severity maps`));
K.push(...tab2('s263', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Field users need maps rather than tables.`],
[`Input`, `Best model of each task; subplot features of every date.`],
[`Output → next step`, `Subplot maps of detection, severity class and score.`]], [2200, 7106], `Step 2.6.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Apply the best model of each task to all subplots of every date.`));
K.push(NL(`Map the predicted class and score together with the absolute error where scores exist.`));
K.push(P(`**Supporting studies.** Abdulridha et al. (2023); Liu et al. (2024); Deng et al. (2024); Liu et al. (2026).`));
K.push(H1(`5. Objective 3 – Prediction of white rust at the pre-symptomatic stage`));
K.push(P(`Objective 3 uses the 576 pre-symptomatic samples of each camera. The question is whether subplots that will develop white rust can be separated from healthy subplots before pustules are visible, and whether their later severity can be predicted. Machine-learning models and the feature-fusion networks (DNN-F1, DNN-F2) are used; the pseudo-image networks are not used here because about 384 training samples per fold are too few for them.`));
K.push(...fig2('obj3', 'g07_obj3.png', `Flow chart of Objective 3 (Activities 3.1–3.5).`, 540));
K.push(...fig2('obj3time', 'g27_obj3.png', `Pre-symptomatic and post-symptomatic periods and how pre-symptomatic samples are labelled from the later status of the same subplot.`, 520));
K.push(H2(`Activity 3.1 – Pre-symptomatic samples and labels`));
K.push(H3(`Step 3.1.1 – Labels from the later status of each subplot`));
K.push(...tab2('s311', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Before symptoms the visual score is zero everywhere; labels must come from what happens later.`],
[`Input`, `Pre-symptomatic subplot tables; scores of the first post-symptomatic date.`],
[`Output → next step`, `Labelled pre-symptomatic dataset → Activity 3.2.`]], [2200, 7106], `Step 3.1.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Classification: healthy = subplots of the 12 healthy plots; infected = inoculated subplots that show pustules later; inoculated subplots that never show symptoms are excluded from the infected class.`));
K.push(NL(`Regression: target = severity score of the same subplot on the first post-symptomatic date.`));
K.push(NL(`Record days after inoculation for every sample.`));
K.push(P(`**Supporting studies.** Zhu et al. (2017); Tian et al. (2021); Mahlein et al. (2019); Yu et al. (2021) for the early stage of pine wilt disease.`));
K.push(H2(`Activity 3.2 – Normalisation to healthy plots`));
K.push(H3(`Step 3.2.1 – Healthy-plot normalisation of all features`));
K.push(...tab2('s321', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Early disease changes are small compared with date, weather, variety and crop-age differences.`],
[`Input`, `Pre-symptomatic features; healthy-plot features of the same date and variety (training replications).`],
[`Output → next step`, `Healthy-normalised features → Activity 3.3.`]], [2200, 7106], `Step 3.2.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Apply Step E3 to every feature: z_{h} = (x − mean_{healthy}) / SD_{healthy}, with the healthy plots of the same date and variety in the training replications.`));
K.push(NL(`Apply the same reference to the test samples.`));
K.push(P(`**Supporting studies.** Oerke et al. (2006); Zarco-Tejada et al. (2018); Calderón et al. (2014); Poblete et al. (2023).`));
K.push(H2(`Activity 3.3 – Pre-symptomatic feature selection`));
K.push(H3(`Step 3.3.1 – Selection with the pre-symptomatic labels`));
K.push(...tab2('s331', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Features that respond after symptoms are not necessarily the earliest responders.`],
[`Input`, `Healthy-normalised feature groups (training part).`],
[`Output → next step`, `Pre-symptomatic feature sets of each camera and sensor set → Activity 3.4.`]], [2200, 7106], `Step 3.3.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Repeat the one-method-per-type selection with the pre-symptomatic labels: SHAP-CARS for bands, ReliefF for indices (two classes) or RReliefF (later score), mRMR for texture, the TTFI search, the redundancy filter and the variance inflation factor.`));
K.push(NL(`Fuse the camera sets for the 15 sensor sets and run sequential floating forward selection for the machine-learning models, limited to 10 features because the training part is smaller.`));
K.push(P(`**Supporting studies.** Tian et al. (2021); Ma et al. (2026); early spectral changes in rusts and mildews: Terentev et al. (2023), Zhu et al. (2017).`));
K.push(H2(`Activity 3.4 – Pre-symptomatic models`));
K.push(H3(`Step 3.4.1 – Models for the 15 sensor sets`));
K.push(...tab2('s341', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Detection must be tested for each camera and combination.`],
[`Input`, `Pre-symptomatic feature sets.`],
[`Output → next step`, `Trained models and test predictions → Activity 3.5.`]], [2200, 7106], `Step 3.4.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Machine learning: support vector machine, random forest, extreme gradient boosting, k-nearest neighbours and partial least squares, with the grids of Table ${T('mlgrid')}.`));
K.push(NL(`Feature-fusion networks: DNN-F1 and DNN-F2 with smaller layers (32 and 16 units) and stronger dropout (0.4).`));
K.push(NL(`Same folds as Objective 2.`));
K.push(P(`**Supporting studies.** Zhu et al. (2017); Tian et al. (2021); Yu et al. (2025); Srivastava et al. (2014).`));
K.push(H2(`Activity 3.5 – Evaluation, earliest detection day and risk maps`));
K.push(H3(`Step 3.5.1 – Pre-symptomatic metrics, area under the curve (AUC) and earliest detection day`));
K.push(...tab2('s351', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Shows how early, with which sensor set and with what reliability white rust can be predicted.`],
[`Input`, `Test predictions with days after inoculation.`],
[`Output → next step`, `Accuracy tables; earliest detection day of every sensor set.`]], [2200, 7106], `Step 3.5.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Classification: sensitivity, specificity, balanced accuracy and AUC; regression: R² and RMSE of the later score.`));
K.push(NL(`Compute balanced accuracy separately for each pre-symptomatic date; the earliest detection day is the first date on which it reaches 0.70 (Figure ${F('earliest')}).`));
K.push(NL(`Report the earliest detection day separately for each variety and inoculation timing.`));
K.push(P(`**Supporting studies.** Fawcett (2006); Mahlein et al. (2019); Zarco-Tejada et al. (2018).`));
K.push(...fig2('earliest', 'g23_dummy_earliest.png', `Dummy example of balanced accuracy by days after inoculation and the earliest detection day of each sensor set.`, 460));
K.push(...tab2('earlyex', [[`Days after inoculation (dummy)`, `3`, `6`, `9`, `12`, `15`],
[`Hyperspectral + thermal: balanced accuracy`, `0.55`, `0.62`, `0.71`, `0.78`, `0.81`],
[`Red–green–blue: balanced accuracy`, `0.45`, `0.47`, `0.55`, `0.65`, `0.69`]], [3400, 1180, 1180, 1180, 1180, 1186], `Worked example (dummy data): the hyperspectral + thermal set reaches 0.70 at 9 days after inoculation (earliest detection day = 9), while the red–green–blue set does not reach it before symptoms.`, 17));
K.push(...tab2('croc', [[`Aspect`, `Receiver operating characteristic analysis and earliest detection day`],
[`Principle (how it works)`, `The receiver operating characteristic curve plots sensitivity against 1 − specificity for all thresholds; its area (AUC) is the probability that an infected sample scores higher than a healthy one. The earliest detection day is the first date on which balanced accuracy reaches a set level.`],
[`Problem it solves`, `Measures early-warning ability independently of the class balance and threshold; gives a simple "how early" answer.`],
[`Specification in this study`, `AUC and balanced accuracy per date; level 0.70.`],
[`Hyper-parameters and how they are tuned`, `Level 0.70 (fixed in advance; 0.65 and 0.75 reported as checks).`],
[`Data on which it works well`, `Binary early-warning problems with unequal classes.`],
[`Why it was selected`, `Standard for early detection and comparable with published earliest-detection studies.`],
[`Key references`, `Fawcett (2006); Mahlein et al. (2019)`]], [2300, 7006], `Method card – Receiver operating characteristic analysis and earliest detection day.`, 16));
K.push(H3(`Step 3.5.2 – Risk maps`));
K.push(...tab2('s352', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Early warnings are useful only if they show where to act.`],
[`Input`, `Best pre-symptomatic model; subplot features of each pre-symptomatic date.`],
[`Output → next step`, `Maps of the predicted infection probability of every subplot.`]], [2200, 7106], `Step 3.5.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Map the predicted probability of later infection for every subplot and pre-symptomatic date.`));
K.push(NL(`Compare the maps with the later observed severity.`));
K.push(P(`**Supporting studies.** Zarco-Tejada et al. (2018); Yu et al. (2025).`));
K.push(H1(`6. Cross-check of the methodology`));
K.push(P(`This chapter checks that no step is missing, that every output is used by a later step, and that the methodology agrees with the feature-selection approach note for multi-sensor UAV data and with the DT-EDNet study (Ma et al., 2026). Where the methodology deliberately differs, the reason is given.`));
K.push(H2(`6.1 Input–output chain of all steps`));
K.push(...tab2('chain', [[`Step(s)`, `Input`, `Output`, `Used by`],
[`A1–A4`, `field design, scores`, `labelled subplot list; post- and pre-symptomatic datasets`, `D8, F1, all objectives`],
[`B1–B2`, `raw images, panels, control points`, `calibrated, georeferenced mosaics`, `B3, B4`],
[`B3`, `hyperspectral cube`, `clean, smoothed 483-band cube`, `B4, C1, D3`],
[`B4–B5`, `mosaics of all cameras`, `aligned layers on the hyperspectral grid`, `C6–C8, D2`],
[`C1–C5`, `pixel samples of all dates`, `labelled endmember library`, `C6`],
[`C6–C8`, `library, cubes, NDVI`, `accepted vegetation mask applied to all cameras`, `D2, D5`],
[`D1–D2`, `masked layers, polygons`, `subplot mean spectra and band values; pixel counts`, `D3–D7, E4`],
[`D3–D7`, `subplot values`, `spectral, index, texture, colour and thermal groups`, `D8, E2`],
[`D8`, `all features`, `feature table of each camera`, `E, F, Objective 1`],
[`E1–E2`, `reflectance and temperatures`, `date-consistent reflectance; normalised thermal features`, `D, Objective 1`],
[`E3`, `features, healthy plots`, `healthy-normalised features`, `Objective 3; thermal difference features`],
[`E4–E6`, `feature tables`, `clean samples; standardised features; class weights`, `all models`],
[`F1–F3`, `clean labelled tables`, `outer and inner folds; tuning plan; leakage checklist`, `Objectives 2–3`],
[`1.1.1–1.1.3`, `post-symptomatic features`, `response figures`, `interpretation, 1.6.3`],
[`1.2.1–1.2.4`, `reflectance and first derivative`, `effective ranges; optimal wavelengths`, `1.3, 1.6.2, 2.1.5`],
[`1.3.1–1.3.3`, `NDSI/RSI maps, bands`, `best NDSI, RSI, White Rust Index; multispectral indices`, `1.4.1, 1.6.1`],
[`1.4.1–1.4.3`, `index group`, `selected indices`, `1.6.2, 2.1.5`],
[`1.5.1–1.5.4`, `principal-component texture`, `selected texture features; best TTFI`, `1.6.2, 2.1.5`],
[`1.6.1–1.6.4`, `survivors of all groups`, `disease-specific feature set of each camera`, `2.1.2, 3.3.1`],
[`2.1.1–2.1.5`, `feature sets, folds`, `task labels; fused sets of 15 sensor sets; six hyperspectral configurations`, `2.2, 2.3`],
[`2.2.1–2.2.6`, `optimum feature combinations`, `tuned machine-learning predictions`, `2.4`],
[`2.3.1–2.3.8`, `fused sets; pseudo-images`, `neural-network predictions`, `2.4`],
[`2.4.1–2.4.3`, `predictions`, `metric tables`, `2.5`],
[`2.5.1–2.5.4`, `metric tables, models`, `best sensor set and model; contributions; ablation; explanation`, `2.6, conclusions`],
[`2.6.1–2.6.3`, `best models`, `robustness results; maps`, `conclusions`],
[`3.1.1–3.5.2`, `pre-symptomatic features, later labels`, `pre-symptomatic models; earliest detection day; risk maps`, `conclusions`]], [1300, 2700, 3400, 1906], `Input and output of every step and the step that uses each output.`, 15));
K.push(P(`**Result of the check.** Every output is used by at least one later step, every input is produced by an earlier step, and every label-based step runs inside the training folds (Table ${T('leak')}). No step is missing between the raw images and the three objectives.`));
K.push(H2(`6.2 Agreement with the feature-selection approach note`));
K.push(...tab2('fscheck', [[`Recommendation of the note`, `In this methodology`, `Status`],
[`Do not select from one big pool; select in stages, group by group`, `four stages; one method per feature type (Table ${T('stages')})`, `included`],
[`Stage 0: build groups with physical meaning; red-edge parameters instead of all derivative bands`, `Activity D; red-edge parameters added; second derivative removed`, `included (second derivative removed on request)`],
[`Stage 1: remove near-constant features; keep one per cluster with |r| > 0.95`, `Steps 1.4.2, 1.5.2, 1.6.1; spectral bands go directly to SHAP-CARS, which handles collinearity`, `included (adapted for bands)`],
[`Stage 2: SPA or CARS for spectra; Boruta or RReliefF for indices; mRMR for texture; two-band search on training plots`, `SHAP-CARS for spectra; ReliefF/RReliefF for indices; mRMR for texture; NDSI/RSI and White Rust Index search in the inner folds`, `included (one method per type, as in Ma et al., 2026)`],
[`Stage 3: variance inflation factor below 5 or 10`, `below 10 (5 as a check)`, `included`],
[`Stage 4: final selection by floating forward selection or elastic net`, `sequential floating forward selection for machine learning, at most 15 features (10 for Objective 3)`, `included`],
[`Every label-based step inside the training folds; folds grouped by plot`, `nested, leave-one-replication-out folds grouped by plot`, `included`],
[`Limit the final number of features (about n/10 to n/20)`, `15 features for about 1024 training samples (10 for about 384)`, `included`],
[`Check stability of selection`, `CARS repeated 20 times; selection frequency over folds (Step 2.5.4)`, `included`],
[`Ablation by group and by camera`, `drop-one-camera, six hyperspectral configurations, DT-EDNet module ablation`, `included`],
[`Normalise thermal values against healthy plots or air temperature on each date`, `Steps E2 and E3`, `included`],
[`Outer loop of 5 folds repeated 10 times`, `three leave-one-replication-out folds (replication is the natural block of the design); five seeds for networks`, `adapted`],
[`Compare with decision-level fusion (stacking)`, `not done: the study is limited to feature-level fusion by design`, `not used (scope)`]], [3500, 4200, 1606], `Cross-check against the feature-selection approach note for multi-sensor UAV data.`, 15));
K.push(H2(`6.3 Agreement with the DT-EDNet study (Ma et al., 2026)`));
K.push(...tab2('dtcheck', [[`Step of Ma et al. (2026)`, `In this methodology`, `Difference and reason`],
[`Spectral response by severity level`, `Step 1.1.1`, `same`],
[`NDSI and RSI R² contour maps; effective ranges with R² > 0.5`, `Step 1.2.1`, `whole usable range 400–2400 nm instead of 450–1000 nm (both cameras of the Headwall imager are available)`],
[`Band selection by RFE-SHAP, SAND and SHAP-CARS; SHAP-CARS chosen`, `Steps 1.2.2–1.2.4 (SHAP-CARS only)`, `one method per type, as requested; SHAP-CARS was the best in the study; stability rule added`],
[`Vegetation index selection with Relief (top five)`, `Steps 1.4.2–1.4.3 (ReliefF / RReliefF)`, `ReliefF handles several classes; RReliefF for the score`],
[`Principal components (> 95%) → GLCM texture (8 measures × 3 components) → mRMR (top six)`, `Steps 1.5.1–1.5.3`, `same, plus a label-free redundancy filter`],
[`TTFI from ordered triplets, three formulas; best by correlation`, `Step 1.5.4`, `same`],
[`DT-EDNet: pseudo-2D input, 3 × 3 embedding (128), SE, class token, 1 KTB with CBAM + 4 TTB, 4 heads, dropout 0.03`, `Steps 2.3.3–2.3.4`, `same; regression head added for the severity score`],
[`EfficientNet, ResNet18, ConvNeXt V2 with identical settings`, `Steps 2.3.5–2.3.7`, `same; stems with stride 1 for small inputs`],
[`AdamW 6 × 10⁻⁴, weight decay 10⁻⁵, cosine to 10⁻⁶, 300 epochs, batch 32, label smoothing 0.01, clipping 1.2, early stopping 60, seed 42`, `Step 2.3.8`, `same; five seeds and a small tuning grid; selection on validation plots`],
[`Random 7:3 split with 10% validation; independent-year test`, `leave-one-replication-out folds grouped by plot (Step F1)`, `random splits put subplots of one plot on both sides and inflate accuracy`],
[`Single and combined feature inputs (OW, VI, TF, TTFI; OW + VI, OW + TTFI, OW + VI + TTFI)`, `Step 2.1.5 (six configurations)`, `TTFI alone (one feature) is not given to the networks; it is assessed in Objective 1`],
[`Ablation without SE, without DTG, without both`, `Step 2.5.3`, `same`],
[`Metrics: overall accuracy, kappa, macro recall, macro-F1, per-class scores`, `Step 2.4.1`, `same, plus weighted kappa, AUC and regression metrics`]], [3300, 2500, 3506], `Cross-check against the DT-EDNet study.`, 15));
K.push(H2(`6.4 Changes from the previous version of the methodology`));
K.push(...tab2('changes', [[`Item`, `Previous version`, `This version`, `Reason`],
[`Second derivative`, `used`, `removed`, `noise amplification; user request`],
[`Band selection`, `correlation scalogram + ReliefF`, `NDSI/RSI effective ranges → SHAP-CARS`, `one method per type; best method in Ma et al. (2026)`],
[`Vegetation index selection`, `Boruta`, `ReliefF / RReliefF`, `one method per type; Relief used for indices by Ma et al. (2026)`],
[`Hyperspectral texture`, `not specified for the cube`, `principal-component texture → mRMR → TTFI`, `Guo et al. (2021); Ma et al. (2026)`],
[`Response tests`, `analysis of variance and Tukey test`, `correlation and response curves`, `fewer statistics; simpler presentation`],
[`Deep learning (post-symptomatic)`, `DNN-F1, DNN-F2`, `DNN-F1, DNN-F2 + DT-EDNet, EfficientNet, ResNet18, ConvNeXt V2`, `user request; comparison of Ma et al. (2026)`],
[`Normalisation`, `inside other steps`, `separate Activity E (six steps)`, `clarity; user request`],
[`Endmember extraction`, `one step`, `Activity C with eight steps`, `clarity; user request`],
[`Technique descriptions`, `short`, `method card for every technique`, `user request`]], [2000, 2300, 2900, 2106], `Main changes in this revision.`, 15));
K.push(H1(`7. Definitions of indices and features`));
K.push(P(`R_{λ} is the reflectance at λ nm (nearest available band). Formulas were checked against the original papers.`));
K.push(...tab2('hsidx', [[`Group`, `Index`, `Formula`, `Reference`],
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
[`Red edge`, `CI_{rededge}`, `R_{790}/R_{720} − 1`, `Gitelson et al. 2003`],
[``, `CI_{green}`, `R_{790}/R_{550} − 1`, `Gitelson et al. 2003`],
[``, `NDRE`, `(R_{790} − R_{720})/(R_{790} + R_{720})`, `Gitelson and Merzlyak 1994`],
[``, `MTCI`, `(R_{754} − R_{709})/(R_{709} − R_{681})`, `Dash and Curran 2004`],
[``, `OSAVI`, `1.16(R_{800} − R_{670})/(R_{800} + R_{670} + 0.16)`, `Rondeaux et al. 1996`],
[``, `MCARI`, `[(R_{700} − R_{670}) − 0.2(R_{700} − R_{550})](R_{700}/R_{670})`, `Daughtry et al. 2000`],
[`Red-edge parameters`, `REP; D_{r}; area`, `wavelength of the maximum first derivative (680–760 nm); its value; sum of the first derivative over 680–760 nm`, `Filella and Peñuelas 1994; Yu et al. 2021`],
[`SWIR disease–water`, `DWSI-2; DWSI-3`, `R_{1660}/R_{550};  R_{1660}/R_{680}`, `Apan et al. 2004`],
[``, `DWSI-5`, `(R_{800} + R_{550})/(R_{1660} + R_{680})`, `Apan et al. 2004`],
[``, `NDWI`, `(R_{860} − R_{1240})/(R_{860} + R_{1240})`, `Gao 1996`],
[``, `MSI`, `R_{1600}/R_{820}`, `Hunt and Rock 1989`],
[``, `NDII`, `(R_{819} − R_{1649})/(R_{819} + R_{1649})`, `Hardisky et al. 1983`],
[`Disease-specific`, `WRI`, `NDSI(λ_{1}, λ_{2}) + w R_{λ3} (Step 1.3.2)`, `Mahlein et al. 2013 (method)`]], [1700, 1700, 4106, 1800], `Hyperspectral indices and red-edge parameters.`, 15));
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
[`PSRI`, `(R − G)/NIR`, `Merzlyak et al. 1999`],
[`Normalised differences (10)`, `(B_{i} − B_{j})/(B_{i} + B_{j}) for all band pairs`, `Ma et al. 2026`],
[`Texture (40)`, `8 GLCM measures (Table ${T('rgbfeat')}) of each of the 5 bands`, `Haralick et al. 1973; Liu et al. 2024`]], [2200, 4800, 2306], `Multispectral features.`, 15));
K.push(...tab2('rgbfeat', [[`Feature`, `Equation`, `Reference`],
[`Chromatic coordinates`, `r = R/(R+G+B), g = G/(R+G+B), b = B/(R+G+B)`, `Woebbecke et al. 1995`],
[`Excess green (ExG)`, `2g − r − b`, `Woebbecke et al. 1995`],
[`Excess red (ExR)`, `1.4r − g`, `Meyer and Neto 2008`],
[`ExG − ExR`, `ExG − ExR`, `Meyer and Neto 2008`],
[`VARI`, `(G − R)/(G + R − B)`, `Gitelson et al. 2002`],
[`GLI`, `(2G − R − B)/(2G + R + B)`, `Louhaichi et al. 2001`],
[`NGRDI`, `(G − R)/(G + R)`, `Tucker 1979`],
[`Hue, saturation, value (3)`, `mean of vegetation pixels`, `—`],
[`Mean (MEA)`, `Σ_{i} Σ_{j} i P(i, j)`, `Haralick et al. 1973`],
[`Variance (VAR)`, `Σ_{i} Σ_{j} (i − μ)^{2} P(i, j)`, `Haralick et al. 1973`],
[`Homogeneity (HOM)`, `Σ_{i} Σ_{j} P(i, j) / [1 + (i − j)^{2}]`, `Haralick et al. 1973`],
[`Contrast (CON)`, `Σ_{i} Σ_{j} (i − j)^{2} P(i, j)`, `Haralick et al. 1973`],
[`Dissimilarity (DIS)`, `Σ_{i} Σ_{j} |i − j| P(i, j)`, `Haralick et al. 1973`],
[`Entropy (ENT)`, `− Σ_{i} Σ_{j} P(i, j) ln P(i, j)`, `Haralick et al. 1973`],
[`Second moment (SEC)`, `Σ_{i} Σ_{j} P(i, j)^{2}`, `Haralick et al. 1973`],
[`Correlation (COR)`, `Σ_{i} Σ_{j} (i − μ_{i})(j − μ_{j}) P(i, j) / (σ_{i} σ_{j})`, `Haralick et al. 1973`]], [2300, 4700, 2306], `Colour indices and grey-level co-occurrence matrix (GLCM) texture measures. P(i, j) is the normalised frequency of grey levels i and j in neighbouring pixels.`, 15));
K.push(...tab2('tirfeat', [[`Feature`, `Definition`, `Reference`],
[`Canopy temperature statistics (5)`, `mean, median, standard deviation, 10th and 90th percentile of vegetation-pixel temperature`, `Liu et al. 2024`],
[`Canopy minus air temperature (CTD)`, `T_{c} − T_{air}`, `Calderón et al. 2014`],
[`Normalised relative canopy temperature (NRCT)`, `(T_{c} − T_{min})/(T_{max} − T_{min}) over the field on that date`, `Elsayed et al. 2017`],
[`Difference from healthy plots (ΔT)`, `T_{c} − mean T_{c} of the healthy plots of the same date and variety`, `Oerke et al. 2006`],
[`Crop water stress index (CWSI)`, `(T_{c} − T_{wet})/(T_{dry} − T_{wet})`, `Idso et al. 1981; Jones et al. 2009`],
[`Thermal texture (8)`, `GLCM measures of the temperature image quantised over one common range`, `Haralick et al. 1973`]], [2800, 4300, 2206], `Thermal features.`, 15));
K.push(H1(`8. Six-month work plan`));
K.push(...fig2('gantt', 'g24_gantt.png', `Six-month work plan for the analysis.`, 540));
K.push(...tab2('plan', [[`Month`, `Work`, `Deliverable`],
[`1`, `Common Activities A–C for all dates and cameras; mask accuracy`, `calibrated, masked images; endmember library`],
[`2`, `Activities D–F: features, normalisation, folds; Activity 1.1`, `feature tables; response curves`],
[`3`, `Activities 1.2–1.6; selection code tested inside folds`, `optimal wavelengths, White Rust Index, selected indices, TTFI; Objective 1 draft`],
[`4`, `Objective 2: machine learning and feature-fusion networks for 15 sensor sets`, `results of 15 sensor sets`],
[`5`, `Objective 2: DT-EDNet and comparison networks; ablation; Shapley explanation; maps`, `network comparison; ablation; maps`],
[`6`, `Objective 3; synthesis and writing`, `earliest detection day; risk maps; thesis chapters`]], [1000, 5000, 3306], `Month-wise plan.`, 17));
K.push(NOTE(`Computing load: 15 sensor sets × 3 tasks × 3 folds × 5 machine-learning models with floating forward selection; two feature-fusion networks and four pseudo-image networks × 5 seeds. Run the selection of each camera once per fold and reuse it for all combinations, and train the networks on a graphics processing unit.`));
K.push(H1(`9. Software and reproducibility`));
K.push(...tab2('software', [[`Task`, `Software`],
[`Image processing, registration, resampling, masks`, `ENVI or Python (GDAL, rasterio); hourglass notebook (minimum noise fraction, pixel purity index, n-dimensional visualisation, spectral angle mapper)`],
[`Features, selection, machine learning`, `Python: numpy, pandas, scikit-learn (Pedregosa et al., 2011), xgboost (Chen and Guestrin, 2016), shap (Lundberg and Lee, 2017), ReliefF, mRMR, mlxtend floating selection (Raschka, 2018)`],
[`Deep learning`, `PyTorch (Paszke et al., 2019)`]], [3300, 6006], `Software used.`, 17));
K.push(BL(`Fix random seeds; store the outer and inner folds as files and reuse them for all sensor sets and models.`));
K.push(BL(`Log every setting (bands removed, mask threshold, selected features per fold, hyper-parameters, seeds).`));
K.push(BL(`Keep raw, intermediate and final tables separate and versioned.`));
K.push(H1(`10. Questions expected in the interview`));
K.push(P(`**Q. Why one feature-selection method for each type of feature?** Each type has a different nature: spectral bands are many and collinear (SHAP-CARS is designed for this), indices are fewer but must separate overlapping classes (ReliefF), and texture features are correlated with each other (mRMR balances relevance and redundancy). One method per type keeps the procedure simple and follows Ma et al. (2026).`));
K.push(P(`**Q. Why is the second derivative not used?** Derivatives amplify noise; at UAV signal-to-noise levels the second derivative adds hundreds of unstable variables (Rinnan et al., 2009). The red-edge parameters from the first derivative keep the useful information (Yu et al., 2021).`));
K.push(P(`**Q. Why are texture features computed on principal components?** Texture of 483 bands would be highly redundant; the first three components keep more than 95% of the variance, as in Guo et al. (2021) and Ma et al. (2026).`));
K.push(P(`**Q. What is the Tri-band Texture Fusion Index?** A combination of three selected texture features in sums, products and ratios; in rice blast it was more strongly related to disease than any single texture feature (Ma et al., 2026).`));
K.push(P(`**Q. Why compare DT-EDNet with EfficientNet, ResNet18 and ConvNeXt V2?** These were the comparison networks of the DT-EDNet study; repeating the comparison under plot-grouped validation shows whether its advantage holds for white rust when accuracy is not inflated by random splits.`));
K.push(P(`**Q. Is the dataset large enough for a transformer?** About 1024 training samples per fold is small for a transformer, which is why identical folds, early stopping, a small tuning grid, five seeds and strong machine-learning baselines are used; the pseudo-image networks are not used for the smaller pre-symptomatic dataset.`));
K.push(P(`**Q. Why are the folds grouped by replication?** Subplots of a plot and plots of a replication are similar; random splits put near-identical samples in training and test data and inflate accuracy (Roberts et al., 2017; Ploton et al., 2020).`));
K.push(P(`**Q. Why are flowers kept in the subplot spectrum?** The canopy score includes the inflorescence and staghead; flower % is recorded and checked so that selected features are not only flowering effects (Sulik and Long, 2016).`));
K.push(P(`**Q. How is pre-symptomatic infection known if no symptoms are visible?** From the later status of the same subplot; inoculated subplots that never develop symptoms are excluded (Zhu et al., 2017; Tian et al., 2021).`));
K.push(P(`**Q. How can these results be used with satellite data?** The selected wavelengths and indices can be simulated for Sentinel-2 or LISS-IV bands from the hyperspectral spectra, as done for yellow rust and rice bacterial leaf blight (Zheng et al., 2018; Das et al., 2015).`));
K.push(H1('References'));
const refPara = r => new Paragraph({ spacing: { after: 70, line: 255 }, indent: { left: 400, hanging: 400 }, children: [new TextRun({ text: r, font: FONT, size: 19 })] });
['Aasen, H., Honkavaara, E., Lucieer, A., Zarco-Tejada, P.J. (2018). Quantitative remote sensing at ultra-high resolution with UAV spectroscopy: a review of sensor technology, measurement procedures, and data correction workflows. Remote Sensing 10(7), 1091. https://doi.org/10.3390/rs10071091',
'Abdulridha, J., Min, A., Rouse, M. N., Kianian, S., Isler, V., & Yang, C. (2023). Evaluation of stem rust disease in wheat fields by drone hyperspectral imaging. Sensors, 23(8), 4154.',
'Ambroise, C., McLachlan, G.J. (2002). Selection bias in gene extraction on the basis of microarray gene-expression data. Proceedings of the National Academy of Sciences 99(10), 6562–6566. https://doi.org/10.1073/pnas.102102699',
'Apan, A., Held, A., Phinn, S., Markley, J. (2004). Detecting sugarcane \'orange rust\' disease using EO-1 Hyperion hyperspectral imagery. International Journal of Remote Sensing 25(2), 489–498.',
'Babar, M.A., Reynolds, M.P., van Ginkel, M., Klatt, A.R., Raun, W.R., Stone, M.L. (2006). Spectral reflectance indices as a potential indirect selection criteria for wheat yield under irrigation. Crop Science 46(2), 578–588.',
'Barker, M., Rayens, W. (2003). Partial least squares for discrimination. Journal of Chemometrics 17(3), 166–173.',
'Barnes, J.D., Balaguer, L., Manrique, E., Elvira, S., Davison, A.W. (1992). A reappraisal of the use of DMSO for the extraction and determination of chlorophylls a and b in lichens and higher plants. Environmental and Experimental Botany 32(2), 85–100.',
'Bausch, W.C., Duke, H.R. (1996). Remote sensing of plant nitrogen status in corn. Transactions of the ASAE 39(5), 1869–1875.',
'Bhattacharya, B.K., Chattopadhyay, C. (2013). A multi-stage tracking for mustard rot disease combining surface meteorology and satellite remote sensing. Computers and Electronics in Agriculture 90, 35–44. https://doi.org/10.1016/j.compag.2012.10.001',
'Bioucas-Dias, J.M., Plaza, A., Dobigeon, N., Parente, M., Du, Q., Gader, P., Chanussot, J. (2012). Hyperspectral unmixing overview: geometrical, statistical, and sparse regression-based approaches. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing 5(2), 354–379. https://doi.org/10.1109/JSTARS.2012.2194696',
'Blackburn, G.A. (1998). Quantifying chlorophylls and carotenoids at leaf and canopy scales: an evaluation of some hyperspectral approaches. Remote Sensing of Environment 66(3), 273–285.',
'Blasch, G., Anberbir, T., Negash, T., Tilahun, L., Belayineh, F.Y., Alemayehu, Y., Mamo, G., Hodson, D.P., Rodrigues, F.A. Jr. (2023). The potential of UAV and very high-resolution satellite imagery for yellow and stem rust detection and phenotyping in Ethiopia. Scientific Reports 13, 16768. https://doi.org/10.1038/s41598-023-43770-y',
'Boardman, J.W., Kruse, F.A. (2011). Analysis of imaging spectrometer data using N-dimensional geometry and a mixture-tuned matched filtering approach. IEEE Transactions on Geoscience and Remote Sensing 49(11), 4138–4152. https://doi.org/10.1109/TGRS.2011.2161585',
'Boardman, J.W., Kruse, F.A., Green, R.O. (1995). Mapping target signatures via partial unmixing of AVIRIS data. Summaries of the Fifth Annual JPL Airborne Earth Science Workshop, JPL Publication 95-1, Vol. 1, 23–26.',
'Bock, C.H., Poole, G.H., Parker, P.E., Gottwald, T.R. (2010). Plant disease severity estimated visually, by digital photography and image analysis, and by hyperspectral imaging. Critical Reviews in Plant Sciences 29(2), 59–107.',
'Breiman, L. (2001). Random forests. Machine Learning 45(1), 5–32.',
'Broge, N.H., Leblanc, E. (2001). Comparing prediction power and stability of broadband and hyperspectral vegetation indices for estimation of green leaf area index and canopy chlorophyll density. Remote Sensing of Environment 76(2), 156–172.',
'Calderón, R., Montes-Borrego, M., Landa, B.B., Navas-Cortés, J.A., Zarco-Tejada, P.J. (2014). Detection of downy mildew of opium poppy using high-resolution multi-spectral and thermal imagery acquired with an unmanned aerial vehicle. Precision Agriculture 15(6), 639–661. https://doi.org/10.1007/s11119-014-9360-y',
'Cawley, G.C., Talbot, N.L.C. (2010). On over-fitting in model selection and subsequent selection bias in performance evaluation. Journal of Machine Learning Research 11, 2079–2107.',
'Chang, C.-W., Laird, D.A., Mausbach, M.J., Hurburgh, C.R. (2001). Near-infrared reflectance spectroscopy–principal components regression analyses of soil properties. Soil Science Society of America Journal 65(2), 480–490.',
'Chappelle, E.W., Kim, M.S., McMurtrey, J.E. (1992). Ratio analysis of reflectance spectra (RARS): an algorithm for the remote estimation of the concentrations of chlorophyll a, chlorophyll b, and carotenoids in soybean leaves. Remote Sensing of Environment 39(3), 239–247.',
'Chattopadhyay, C., et al. (2011). Epidemiology and development of forecasting models for white rust of Brassica juncea in India. Archives of Phytopathology and Plant Protection 44(8), 751–763.',
'Chen, J.M. (1996). Evaluation of vegetation indices and a modified simple ratio for boreal applications. Canadian Journal of Remote Sensing 22(3), 229–242.',
'Chen, T., Guestrin, C. (2016). XGBoost: a scalable tree boosting system. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 785–794.',
'Cohen, J. (1960). A coefficient of agreement for nominal scales. Educational and Psychological Measurement 20(1), 37–46.',
'Cohen, J. (1968). Weighted kappa: nominal scale agreement with provision for scaled disagreement or partial credit. Psychological Bulletin 70(4), 213–220.',
'Congalton, R.G. (1991). A review of assessing the accuracy of classifications of remotely sensed data. Remote Sensing of Environment 37(1), 35–46. https://doi.org/10.1016/0034-4257(91)90048-B',
'Conn, K.L., Tewari, J.P., Awasthi, R.P. (1990). A disease assessment key for Alternaria blackspot in rapeseed and mustard. Canadian Plant Disease Survey 70(1), 19–22.',
'Cortes, C., Vapnik, V. (1995). Support-vector networks. Machine Learning 20(3), 273–297.',
'Cover, T., Hart, P. (1967). Nearest neighbor pattern classification. IEEE Transactions on Information Theory 13(1), 21–27.',
'Das, P.K., Laxman, B., Kameswara Rao, S.V.C., Seshasai, M.V.R., Dadhwal, V.K. (2015). Monitoring of bacterial leaf blight in rice using ground-based hyperspectral and LISS IV satellite data in Kurnool, Andhra Pradesh, India. International Journal of Pest Management 61(4), 359–368.',
'Dash, J., Curran, P.J. (2004). The MERIS terrestrial chlorophyll index. International Journal of Remote Sensing 25(23), 5403–5413.',
'Daughtry, C.S.T., Walthall, C.L., Kim, M.S., de Colstoun, E.B., McMurtrey, J.E. (2000). Estimating corn leaf chlorophyll concentration from leaf and canopy reflectance. Remote Sensing of Environment 74(2), 229–239.',
'Deng, J., Hong, D., Li, C., Yao, J., Yang, Z., Zhang, Z., Chanussot, J. (2024). RustQNet: multimodal deep learning for quantitative inversion of wheat stripe rust disease index. Computers and Electronics in Agriculture 225, 109245.',
'Dormann, C.F., Elith, J., Bacher, S., et al. (2013). Collinearity: a review of methods to deal with it and a simulation study evaluating their performance. Ecography 36(1), 27–46. https://doi.org/10.1111/j.1600-0587.2012.07348.x',
'Dosovitskiy, A., Beyer, L., Kolesnikov, A., Weissenborn, D., Zhai, X., Unterthiner, T., Dehghani, M., Minderer, M., Heigold, G., Gelly, S., Uszkoreit, J., Houlsby, N. (2021). An image is worth 16x16 words: transformers for image recognition at scale. International Conference on Learning Representations (ICLR 2021).',
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
'Hall-Beyer, M. (2017). Practical guidelines for choosing GLCM textures to use in landscape classification tasks over a range of moderate spatial scales. International Journal of Remote Sensing 38(5), 1312–1338. https://doi.org/10.1080/01431161.2016.1278314',
'Haralick, R.M., Shanmugam, K., Dinstein, I. (1973). Textural features for image classification. IEEE Transactions on Systems, Man, and Cybernetics SMC-3(6), 610–621.',
'Hardisky, M.A., Klemas, V., Smart, R.M. (1983). The influence of soil salinity, growth form, and leaf moisture on the spectral radiance of Spartina alterniflora canopies. Photogrammetric Engineering and Remote Sensing 49(1), 77–83.',
'He, K., Zhang, X., Ren, S., Sun, J. (2016). Deep residual learning for image recognition. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 770–778. https://doi.org/10.1109/CVPR.2016.90',
'Horler, D.N.H., Dockray, M., Barber, J. (1983). The red edge of plant leaf reflectance. International Journal of Remote Sensing 4(2), 273–288.',
'Hu, J., Shen, L., Sun, G. (2018). Squeeze-and-excitation networks. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 7132–7141. https://doi.org/10.1109/CVPR.2018.00745',
'Huang, W., Guan, Q., Luo, J., Zhang, J., Zhao, J., Liang, D., Huang, L., Zhang, D. (2014). New optimized spectral indices for identifying and monitoring winter wheat diseases. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing 7(6), 2516–2524. https://doi.org/10.1109/JSTARS.2013.2294961',
'Huete, A.R. (1988). A soil-adjusted vegetation index (SAVI). Remote Sensing of Environment 25(3), 295–309.',
'Hughes, G. (1968). On the mean accuracy of statistical pattern recognizers. IEEE Transactions on Information Theory 14(1), 55–63. https://doi.org/10.1109/TIT.1968.1054102',
'Hunt, E.R., Rock, B.N. (1989). Detection of changes in leaf water content using near- and middle-infrared reflectances. Remote Sensing of Environment 30(1), 43–54.',
'Idso, S.B., Jackson, R.D., Pinter, P.J., Reginato, R.J., Hatfield, J.L. (1981). Normalizing the stress-degree-day parameter for environmental variability. Agricultural Meteorology 24, 45–55.',
'Ioffe, S., Szegedy, C. (2015). Batch normalization: accelerating deep network training by reducing internal covariate shift. Proceedings of the 32nd International Conference on Machine Learning (ICML), PMLR 37, 448–456.',
'Johnson, J.M., Khoshgoftaar, T.M. (2019). Survey on deep learning with class imbalance. Journal of Big Data 6, 27. https://doi.org/10.1186/s40537-019-0192-5',
'Jolliffe, I.T., Cadima, J. (2016). Principal component analysis: a review and recent developments. Philosophical Transactions of the Royal Society A 374, 20150202. https://doi.org/10.1098/rsta.2015.0202',
'Jones, H.G., Serraj, R., Loveys, B.R., Xiong, L., Wheaton, A., Price, A.H. (2009). Thermal infrared imaging of crop canopies for the remote diagnosis and quantification of plant responses to water stress in the field. Functional Plant Biology 36(11), 978–989. https://doi.org/10.1071/FP09123',
'Jordan, C.F. (1969). Derivation of leaf-area index from quality of light on the forest floor. Ecology 50(4), 663–666.',
'Kattenborn, T., Leitloff, J., Schiefer, F., Hinz, S. (2021). Review on convolutional neural networks (CNN) in vegetation remote sensing. ISPRS Journal of Photogrammetry and Remote Sensing 173, 24–49. https://doi.org/10.1016/j.isprsjprs.2020.12.010',
'Kingma, D.P., Ba, J. (2015). Adam: a method for stochastic optimization. 3rd International Conference on Learning Representations (ICLR). arXiv:1412.6980.',
'Kruse, F.A., Lefkoff, A.B., Boardman, J.W., Heidebrecht, K.B., Shapiro, A.T., Barloon, P.J., Goetz, A.F.H. (1993). The spectral image processing system (SIPS) – interactive visualization and analysis of imaging spectrometer data. Remote Sensing of Environment 44(2–3), 145–163.',
'Kuhn, M., Johnson, K. (2013). Applied Predictive Modeling. Springer, New York. https://doi.org/10.1007/978-1-4614-6849-3',
'Kumar, S., Kalha, C.S. (2005). Evaluation of rapeseed-mustard germplasm against white rust and alternaria blight. Annals of Biology (India) 21(1).',
'Li, H., Liang, Y., Xu, Q., Cao, D. (2009). Key wavelengths screening using competitive adaptive reweighted sampling method for multivariate calibration. Analytica Chimica Acta 648(1), 77–84.',
'Liu, L., Dong, Y., Huang, W., Du, X., Ma, H. (2020). Monitoring wheat Fusarium head blight using unmanned aerial vehicle hyperspectral imagery. Remote Sensing 12(22), 3811. https://doi.org/10.3390/rs12223811',
'Liu, Y., An, L., Ma, X., Feng, H., Sun, H., Liu, G., Liu, M., Zhao, F., Yan, X., Ma, Y., Li, M. (2026). A specific vegetation index for monitoring and tracking the spatiotemporal dynamics of wheat powdery mildew from ground to unmanned aerial vehicle scales. Journal of Remote Sensing 6, 0955. https://doi.org/10.34133/remotesensing.0955',
'Liu, Y., Liu, G., Sun, H., An, L., Zhao, R., Liu, M., Tang, W., Li, M., Yan, X., Ma, Y., Zhao, F. (2024). Exploring multi-features in UAV based optical and thermal infrared images to estimate disease severity of wheat powdery mildew. Computers and Electronics in Agriculture 225, 109285. https://doi.org/10.1016/j.compag.2024.109285',
'Loshchilov, I., Hutter, F. (2017). SGDR: stochastic gradient descent with warm restarts. International Conference on Learning Representations (ICLR 2017).',
'Loshchilov, I., Hutter, F. (2019). Decoupled weight decay regularization. International Conference on Learning Representations (ICLR 2019).',
'Louhaichi, M., Borman, M.M., Johnson, D.E. (2001). Spatially located platform and aerial photography for documentation of grazing impacts on wheat. Geocarto International 16(1), 65–70. https://doi.org/10.1080/10106040108542184',
'Lundberg, S.M., Erion, G., Chen, H., DeGrave, A., Prutkin, J.M., Nair, B., Katz, R., Himmelfarb, J., Bansal, N., Lee, S.-I. (2020). From local explanations to global understanding with explainable AI for trees. Nature Machine Intelligence 2(1), 56–67. https://doi.org/10.1038/s42256-019-0138-9',
'Lundberg, S.M., Lee, S.-I. (2017). A unified approach to interpreting model predictions. Advances in Neural Information Processing Systems 30, 4765–4774.',
'Ma, J., Wu, P., Guo, S., Lin, Y., Yu, F., Liu, T. (2026). Early detection of rice blast disease using a dual transformer network (DT-EDNet) based on hyperspectral imaging and multi-feature fusion. IAENG International Journal of Applied Mathematics 56(11), 5380–5398.',
'Maes, W.H., Steppe, K. (2012). Estimating evapotranspiration and drought stress with ground-based thermal remote sensing in agriculture: a review. Journal of Experimental Botany 63(13), 4671–4712. https://doi.org/10.1093/jxb/ers165',
'Mahlein, A.-K. (2016). Plant disease detection by imaging sensors – parallels and specific demands for precision agriculture and plant phenotyping. Plant Disease 100(2), 241–251.',
'Mahlein, A.-K., Alisaac, E., Al Masri, A., Behmann, J., Dehne, H.-W., Oerke, E.-C. (2019). Comparison and combination of thermal, fluorescence, and hyperspectral imaging for monitoring Fusarium head blight of wheat on spikelet scale. Sensors 19(10), 2281. https://doi.org/10.3390/s19102281',
'Mahlein, A.-K., Rumpf, T., Welke, P., Dehne, H.-W., Plümer, L., Steiner, U., Oerke, E.-C. (2013). Development of spectral indices for detecting and identifying plant diseases. Remote Sensing of Environment 128, 21–30. https://doi.org/10.1016/j.rse.2012.09.019',
'Maimaitijiang, M., Sagan, V., Sidike, P., Hartling, S., Esposito, F., Fritschi, F.B. (2020). Soybean yield prediction from UAV using multimodal data fusion and deep learning. Remote Sensing of Environment 237, 111599. https://doi.org/10.1016/j.rse.2019.111599',
'Mehmood, T., Liland, K.H., Snipen, L., Sæbø, S. (2012). A review of variable selection methods in partial least squares regression. Chemometrics and Intelligent Laboratory Systems 118, 62–69. https://doi.org/10.1016/j.chemolab.2012.07.010',
'Meinshausen, N., Bühlmann, P. (2010). Stability selection. Journal of the Royal Statistical Society: Series B (Statistical Methodology) 72(4), 417–473. https://doi.org/10.1111/j.1467-9868.2010.00740.x',
'Merton, R., Huntington, J. (1999). Early simulation results of the ARIES-1 satellite sensor for multi-temporal vegetation research derived from AVIRIS. Proceedings of the 8th JPL Airborne Earth Science Workshop, Pasadena.',
'Merzlyak, M.N., Gitelson, A.A., Chivkunova, O.B., Rakitin, V.Y. (1999). Non-destructive optical detection of pigment changes during leaf senescence and fruit ripening. Physiologia Plantarum 106(1), 135–141.',
'Messina, G., Modica, G. (2020). Applications of UAV thermal imagery in precision agriculture: state of the art and future research outlook. Remote Sensing 12(9), 1491. https://doi.org/10.3390/rs12091491',
'Metternicht, G. (2003). Vegetation indices derived from high-resolution airborne videography for precision crop management. International Journal of Remote Sensing 24(14), 2855–2877.',
'Meyer, G.E., Neto, J.C. (2008). Verification of color vegetation indices for automated crop imaging applications. Computers and Electronics in Agriculture 63(2), 282–293. https://doi.org/10.1016/j.compag.2008.03.009',
'Mishra, K.K., Kolte, S.J., Nashaat, N.I., Awasthi, R.P. (2009). Pathological and biochemical changes in Brassica juncea (mustard) infected with Albugo candida (white rust). Plant Pathology 58(1), 80–86. https://doi.org/10.1111/j.1365-3059.2008.01939.x',
'Mountrakis, G., Im, J., Ogole, C. (2011). Support vector machines in remote sensing: a review. ISPRS Journal of Photogrammetry and Remote Sensing 66(3), 247–259. https://doi.org/10.1016/j.isprsjprs.2010.11.001',
'Mustafa, G., Zheng, H., Li, W., Yin, Y., Wang, Y., Zhou, M., Liu, P., Bilal, M., Jia, H., Li, G., Cheng, T., Tian, Y., Cao, W., Zhu, Y., Yao, X. (2023). Fusarium head blight monitoring in wheat ears using machine learning and multimodal data from asymptomatic to symptomatic periods. Frontiers in Plant Science 13, 1102341. https://doi.org/10.3389/fpls.2022.1102341',
'Müller, R., Kornblith, S., Hinton, G.E. (2019). When does label smoothing help? Advances in Neural Information Processing Systems 32.',
'Nogueira, S., Sechidis, K., Brown, G. (2018). On the stability of feature selection algorithms. Journal of Machine Learning Research 18(174), 1–54.',
'Oerke, E.-C., Steiner, U., Dehne, H.-W., Lindenthal, M. (2006). Thermal imaging of cucumber leaves affected by downy mildew and environmental conditions. Journal of Experimental Botany 57(9), 2121–2132. https://doi.org/10.1093/jxb/erj170',
'Pascanu, R., Mikolov, T., Bengio, Y. (2013). On the difficulty of training recurrent neural networks. Proceedings of the 30th International Conference on Machine Learning, PMLR 28(3), 1310–1318.',
'Paszke, A., Gross, S., Massa, F., et al. (2019). PyTorch: an imperative style, high-performance deep learning library. Advances in Neural Information Processing Systems 32, 8024–8035.',
'Pedregosa, F., et al. (2011). Scikit-learn: machine learning in Python. Journal of Machine Learning Research 12, 2825–2830.',
'Peng, H., Long, F., Ding, C. (2005). Feature selection based on mutual information: criteria of max-dependency, max-relevance, and min-redundancy. IEEE Transactions on Pattern Analysis and Machine Intelligence 27(8), 1226–1238. https://doi.org/10.1109/TPAMI.2005.159',
'Peñuelas, J., Baret, F., Filella, I. (1995). Semi-empirical indices to assess carotenoids/chlorophyll a ratio from leaf spectral reflectance. Photosynthetica 31(2), 221–230.',
'Peñuelas, J., Gamon, J.A., Fredeen, A.L., Merino, J., Field, C.B. (1994). Reflectance indices associated with physiological changes in nitrogen- and water-limited sunflower leaves. Remote Sensing of Environment 48(2), 135–146.',
'Peñuelas, J., Piñol, J., Ogaya, R., Filella, I. (1997). Estimation of plant water concentration by the reflectance Water Index WI (R900/R970). International Journal of Remote Sensing 18(13), 2869–2875.',
'Pineda, M., Barón, M., Pérez-Bueno, M.-L. (2021). Thermal imaging for plant stress detection and phenotyping. Remote Sensing 13(1), 68. https://doi.org/10.3390/rs13010068',
'Ploton, P., Mortier, F., Réjou-Méchain, M., Barbier, N., Picard, N., Rossi, V., Dormann, C., Cornu, G., Viennois, G., Bayol, N., Lyapustin, A., Gourlet-Fleury, S., Pélissier, R. (2020). Spatial validation reveals poor predictive performance of large-scale ecological mapping models. Nature Communications 11, 4540. https://doi.org/10.1038/s41467-020-18321-y',
'Poblete, T., Navas-Cortes, J.A., Hornero, A., Camino, C., Calderon, R., Hernandez-Clemente, R., Landa, B.B., Zarco-Tejada, P.J. (2023). Detection of symptoms induced by vascular plant pathogens in tree crops using high-resolution satellite data: modelling and assessment with airborne hyperspectral imagery. Remote Sensing of Environment 295, 113698. https://doi.org/10.1016/j.rse.2023.113698',
'Pudil, P., Novovičová, J., Kittler, J. (1994). Floating search methods in feature selection. Pattern Recognition Letters 15(11), 1119–1125.',
'Raschka, S. (2018). MLxtend: providing machine learning and data science utilities and extensions to Python\'s scientific computing stack. Journal of Open Source Software 3(24), 638.',
'Raun, W.R., Solie, J.B., Johnson, G.V., Stone, M.L., Lukina, E.V., Thomason, W.E., Schepers, J.S. (2001). In-season prediction of potential grain yield in winter wheat using canopy reflectance. Agronomy Journal 93(1), 131–138.',
'Revill, A., Florence, A., MacArthur, A., Hoad, S., Rees, R., Williams, M. (2020). Quantifying uncertainty and bridging the scaling gap in the retrieval of leaf area index by coupling Sentinel-2 and UAV observations. Remote Sensing 12(11), 1843. https://doi.org/10.3390/rs12111843',
'Richards, J.A. (2013). Remote Sensing Digital Image Analysis: An Introduction, 5th edn. Springer, Berlin. https://doi.org/10.1007/978-3-642-30062-2',
'Rinnan, Å., van den Berg, F., Engelsen, S.B. (2009). Review of the most common pre-processing techniques for near-infrared spectra. TrAC Trends in Analytical Chemistry 28(10), 1201–1222. https://doi.org/10.1016/j.trac.2009.07.007',
'Roberts, D.R., Bahn, V., Ciuti, S., et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. Ecography 40(8), 913–929. https://doi.org/10.1111/ecog.02881',
'Robnik-Šikonja, M., Kononenko, I. (2003). Theoretical and empirical analysis of ReliefF and RReliefF. Machine Learning 53, 23–69. https://doi.org/10.1023/A:1025667309714',
'Rondeaux, G., Steven, M., Baret, F. (1996). Optimization of soil-adjusted vegetation indices. Remote Sensing of Environment 55(2), 95–107.',
'Roujean, J.-L., Bréon, F.-M. (1995). Estimating PAR absorbed by vegetation from bidirectional reflectance measurements. Remote Sensing of Environment 51(3), 375–384.',
'Rouse, J.W., Haas, R.H., Schell, J.A., Deering, D.W. (1974). Monitoring vegetation systems in the Great Plains with ERTS. Third ERTS Symposium, NASA SP-351, Vol. 1, 309–317.',
'Saharan, G.S., Verma, P.R., Meena, P.D., Kumar, A. (2014). White Rust of Crucifers: Biology, Ecology and Management. Springer India, New Delhi.',
'Savitzky, A., Golay, M.J.E. (1964). Smoothing and differentiation of data by simplified least squares procedures. Analytical Chemistry 36(8), 1627–1639.',
'Schafer, R.W. (2011). What is a Savitzky–Golay filter? IEEE Signal Processing Magazine 28(4), 111–117. https://doi.org/10.1109/MSP.2011.941097',
'Sharma, A., Vans, E., Shigemizu, D., Boroevich, K.A., Tsunoda, T. (2019). DeepInsight: a methodology to transform a non-image data to an image for convolution neural network architecture. Scientific Reports 9, 11399. https://doi.org/10.1038/s41598-019-47765-6',
'Smith, G.M., Milton, E.J. (1999). The use of the empirical line method to calibrate remotely sensed data to reflectance. International Journal of Remote Sensing 20(13), 2653–2662.',
'Soille, P. (2003). Morphological Image Analysis: Principles and Applications, 2nd edn. Springer, Berlin. https://doi.org/10.1007/978-3-662-05088-0',
'Sokolova, M., Lapalme, G. (2009). A systematic analysis of performance measures for classification tasks. Information Processing and Management 45(4), 427–437.',
'Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., Salakhutdinov, R. (2014). Dropout: a simple way to prevent neural networks from overfitting. Journal of Machine Learning Research 15, 1929–1958.',
'Sulik, J.J., Long, D.S. (2016). Spectral considerations for modeling yield of canola. Remote Sensing of Environment 184, 161–174.',
'Szegedy, C., Vanhoucke, V., Ioffe, S., Shlens, J., Wojna, Z. (2016). Rethinking the Inception architecture for computer vision. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2818–2826. https://doi.org/10.1109/CVPR.2016.308',
'Tan, M., Le, Q.V. (2019). EfficientNet: rethinking model scaling for convolutional neural networks. Proceedings of the 36th International Conference on Machine Learning, PMLR 97, 6105–6114.',
'Terentev, A., Badenko, V., Shaydayuk, E., Emelyanov, D., Eremenko, D., Klabukov, D., Fedotov, A., Dolzhenko, V. (2023). Hyperspectral remote sensing for early detection of wheat leaf rust caused by Puccinia triticina. Agriculture 13(6), 1186. https://doi.org/10.3390/agriculture13061186',
'Terentev, A., Dolzhenko, V., Fedotov, A., Eremenko, D. (2022). Current state of hyperspectral remote sensing for early plant disease detection: a review. Sensors 22(3), 757. https://doi.org/10.3390/s22030757',
'Thenkabail, P.S., Enclona, E.A., Ashton, M.S., Van Der Meer, B. (2004). Accuracy assessments of hyperspectral waveband performance for vegetation analysis applications. Remote Sensing of Environment 91(3–4), 354–376.',
'Tian, L., Xue, B., Wang, Z., Li, D., Yao, X., Cao, Q., Zhu, Y., Cao, W., Cheng, T. (2021). Spectroscopic detection of rice leaf blast infection from asymptomatic to mild stages with integrated machine learning and feature selection. Remote Sensing of Environment 257, 112350. https://doi.org/10.1016/j.rse.2021.112350',
'Tsai, F., Philpot, W. (1998). Derivative analysis of hyperspectral data. Remote Sensing of Environment 66(1), 41–51.',
'Tucker, C.J. (1979). Red and photographic infrared linear combinations for monitoring vegetation. Remote Sensing of Environment 8(2), 127–150. https://doi.org/10.1016/0034-4257(79)90013-0',
'Urbanowicz, R.J., Meeker, M., La Cava, W., Olson, R.S., Moore, J.H. (2018). Relief-based feature selection: introduction and review. Journal of Biomedical Informatics 85, 189–203. https://doi.org/10.1016/j.jbi.2018.07.014',
'Varma, S., Simon, R. (2006). Bias in error estimation when using cross-validation for model selection. BMC Bioinformatics 7, 91. https://doi.org/10.1186/1471-2105-7-91',
'Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kaiser, Ł., Polosukhin, I. (2017). Attention is all you need. Advances in Neural Information Processing Systems 30, 5998–6008.',
'Woebbecke, D.M., Meyer, G.E., Von Bargen, K., Mortensen, D.A. (1995). Color indices for weed identification under various soil, residue, and lighting conditions. Transactions of the ASAE 38(1), 259–269.',
'Wold, S., Sjöström, M., Eriksson, L. (2001). PLS-regression: a basic tool of chemometrics. Chemometrics and Intelligent Laboratory Systems 58(2), 109–130.',
'Woo, S., Debnath, S., Hu, R., Chen, X., Liu, Z., Kweon, I.S., Xie, S. (2023). ConvNeXt V2: co-designing and scaling ConvNets with masked autoencoders. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 16133–16142. https://doi.org/10.1109/CVPR52729.2023.01548',
'Woo, S., Park, J., Lee, J.-Y., Kweon, I.S. (2018). CBAM: convolutional block attention module. Proceedings of the European Conference on Computer Vision (ECCV), Lecture Notes in Computer Science 11211, 3–19. https://doi.org/10.1007/978-3-030-01234-2_1',
'Yu, H., Li, X., Yu, Y., Sui, Y., Zhang, J., Zhang, L., ... & Jiang, R. (2025). A dual-branch multimodal model for early detection of rice sheath blight: Fusing spectral and physiological signatures. Computers and Electronics in Agriculture, 231, 110031.',
'Yu, R., Ren, L., Luo, Y. (2021). Early detection of pine wilt disease in Pinus tabuliformis in North China using a field portable spectrometer and UAV-based hyperspectral imagery. Forest Ecosystems 8, 44. https://doi.org/10.1186/s40663-021-00328-6',
'Yuan, L., Yu, Q., Xiang, L., Zeng, F., Dong, J., Xu, O., Zhang, J. (2025). Integrating UAV and high-resolution satellite remote sensing for multi-scale rice disease monitoring. Computers and Electronics in Agriculture 234, 110287. https://doi.org/10.1016/j.compag.2025.110287',
'Zarco-Tejada, P.J., Camino, C., Beck, P.S.A., et al. (2018). Previsual symptoms of Xylella fastidiosa infection revealed in spectral plant-trait alterations. Nature Plants 4, 432–439.',
'Zheng, Q., Huang, W., Cui, X., Shi, Y., Liu, L. (2018). New spectral index for detecting wheat yellow rust using Sentinel-2 multispectral imagery. Sensors 18(3), 868.',
'Zhu, H., Chu, B., Zhang, C., Liu, F., Jiang, L., He, Y. (2017). Hyperspectral imaging for presymptomatic detection of tobacco disease with successive projections algorithm and machine-learning classifiers. Scientific Reports 7, 4125. https://doi.org/10.1038/s41598-017-04501-2',
'Zitová, B., Flusser, J. (2003). Image registration methods: a survey. Image and Vision Computing 21(11), 977–1000. https://doi.org/10.1016/S0262-8856(03)00137-9'].forEach(r => K.push(refPara(r)));


const numcfg = r => ({ reference: r, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] });
const doc = new Document({
  features: { updateFields: true }, creator: 'Animesh Panda', title: 'White rust UAV methodology – revised (Objectives 1–3)',
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
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('saved', OUT, 'figs', FORDER.length, 'tabs', TORDER.length, 'eqs', 0, 'refs', 154); });
