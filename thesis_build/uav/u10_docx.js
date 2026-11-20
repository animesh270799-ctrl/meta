const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType, ImageRun,
  TableOfContents, PageBreak, LevelFormat, Footer, PageNumber, BorderStyle } = require('docx');
const B = '/tmp/claude-0/-home-user-meta/c5704ca0-f1ca-5695-b9e0-a810fbe166a9/scratchpad/uav/';
const OUT = '/tmp/claude-0/-home-user-meta/c5704ca0-f1ca-5695-b9e0-a810fbe166a9/scratchpad/outputs/White_rust_UAV_multimodal_methodology_revised.docx';
const FONT = 'Calibri', EQF = 'Cambria Math';
// ---------- text helpers: _x / _{..} = subscript, ^x / ^{..} = superscript, **..** = bold ----------
function runs(text, base = {}) {
  const out = []; let i = 0, buf = '', bold = false;
  const flush = () => { if (buf) { out.push(new TextRun({ text: buf, font: base.font || FONT, size: base.size || 22, bold: bold || base.bold, italics: base.italics })); buf = ''; } };
  while (i < text.length) {
    const ch = text[i];
    if (text.startsWith('**', i)) { flush(); bold = !bold; i += 2; continue; }
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
const NL = (t, ref = 'num') => new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 60, line: 280 }, children: runs(t) });
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
const FORDER = ['matrix', 'workflow', 'design', 'chains', 'step12', 'funnel', 'fusion', 'dnn'];
const TORDER = ['papers', 'lessons', 'mustard', 'objmap', 'tasks', 'dataset', 'sensors', 'hsfeat', 'hsidx', 'msidx', 'rgbfeat', 'tirfeat', 'consensus', 'statsdesign', 'stats', 'objsens', 'inputsets', 'hyper', 'models', 'metrics', 'runs', 'satisfy', 'idxcorr', 'methcorr', 'corrections', 'simplify'];
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
// ======================= TITLE =======================
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 500, after: 120 }, children: [new TextRun({ text: 'AI-based multimodal UAV sensing of white rust in mustard', font: FONT, size: 38, bold: true, color: '1E3A1F' })] }));
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 }, children: [new TextRun({ text: 'Detailed objective-wise methodology for RGB, multispectral, hyperspectral and thermal UAV data', font: FONT, size: 27, color: '2C5F2D' })] }));
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 }, children: [new TextRun({ text: 'Ph.D. (Agricultural Physics), ICAR-IARI  |  Disease detection, severity discrimination and pre-symptomatic prediction  |  ML-SFFS and deep-learning feature-level fusion', font: FONT, size: 20, italics: true, color: '555555' })] }));
K.push(NOTE('**Scope of this document.** (1) The methodology follows the three objectives of the ORW and uses only the four UAV datasets (RGB, multispectral MS, hyperspectral HS, thermal TIR); disease scores and biochemical/biophysical measurements are ground truth. (2) Images of **all flight dates are pooled into one dataset**; the date is not used as a variable, factor or grouping in any analysis. (3) Two tasks are treated separately throughout: **disease detection** (healthy vs diseased) and **severity discrimination** into three plot-level classes (Low ≤ 25%, Moderate 25–50%, High > 50% disease index), together with **regression** of the disease index. (4) Every analysis is done **first for each sensor separately, then for sensor combinations**. (5) Fusion is at feature level, by two ML-SFFS strategies (Tian et al., 2021; Mustafa et al., 2023) and two deep-learning strategies (Maimaitijiang et al., 2020). (6) Index formulas supplied in the ORW slides were checked against the original papers; corrections are listed in Section 10.'));
K.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-2' }));
K.push(new Paragraph({ children: [new PageBreak()] }));

// ======================= 1 =======================
K.push(H1('1. Research problem and objectives'));
K.push(P('White rust of Indian mustard (Brassica juncea), caused by the obligate biotrophic oomycete Albugo candida, causes 20–60% yield loss in India (as cited in the ORW). Local infection produces white to creamy-yellow pustules on leaves, stems and floral parts; systemic infection deforms the inflorescence into a "staghead". These symptoms change pigment content and leaf colour (measured by MS and HS), leaf water status and transpiration (HS short-wave infrared, TIR) and canopy surface pattern (RGB and thermal texture). No single sensor measures all of these, which motivates multimodal sensing and data fusion (Maimaitijiang et al., 2020; Feng et al., 2022).'));
K.push(P('The three objectives of the thesis (ORW, item 12) and the tasks addressed in each are:'));
K.push(NL('**Objective 1. To characterise white rust of mustard through multimodal sensing from a UAV platform.** For each sensor: which features change with disease (detection) and with severity (severity discrimination), and which plant property explains the change.'));
K.push(NL('**Objective 2. To detect and discriminate disease severity of white rust through AI-based multimodal data fusion.** Post-symptomatic classification (healthy vs diseased; three severity classes) and regression of the disease index, for each sensor and for fused sensors.'));
K.push(NL('**Objective 3. To predict white rust at the pre-symptomatic stage using machine learning.** Classification of healthy vs later-infected plots before symptoms, for each sensor and for fused sensors.'));

// ======================= 2 =======================
K.push(H1('2. Analysis of the eight reference papers'));
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

K.push(H2('2.1 What the papers agree on'));
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
K.push(H2('2.2 ML-SFFS as a feature-level fusion technique'));
K.push(P('Sequential floating forward selection (SFFS; Pudil et al., 1994) with a machine-learning classifier as criterion is called ML-SFFS (Tian et al., 2021). Tian et al. (2021) used it within one sensor to combine reflectance bands, indices and wavelet features. Mustafa et al. (2023) extended it to multiple sensors: features of hyperspectral reflectance, chlorophyll-fluorescence imaging and a phenotyping camera were screened by Boruta and VIF, pooled, and ML-SFFS (k-NN, RF, SVM) selected the optimum cross-sensor combination ("partial fusion of selected disease-sensitive features through ML-SFFS"). The selected combinations mixed sensors (e.g. the fluorescence parameter Fv/Fm with NDVI and SRPI), had two to four features, and gave 87.04% accuracy at the asymptomatic stage, rising to 95% at 20% severity. No study was found that applies ML-SFFS fusion to UAV RGB, MS, HS and TIR data for a crop disease; this is a novel element of the thesis. In this experiment all four sensors observe the same plots on the same flights, so their features are exactly paired for fusion.'));
K.push(H2('2.3 Gaps filled by this thesis'));
K.push(BL('None of the eight papers studies white rust or mustard. The two mustard studies from Bharatpur (Section 2.4) used ground spectroscopy (aphid) or satellite data (Sclerotinia rot), not UAVs, and neither studied white rust.'));
K.push(BL('Only two papers use a UAV for disease (Guo 2021: HS only; Liu 2024: MS + TIR); none combines all four UAV sensors.'));
K.push(BL('ML-SFFS fusion (Mustafa 2023) and DNN fusion (Maimaitijiang 2020) have not been compared, nor applied to UAV data for disease severity.'));
K.push(BL('Pre-symptomatic detection was shown only at leaf or spike scale under controlled conditions (Tian 2021; Mustafa 2023; Mahlein 2019).'));
K.push(...fig2('matrix', 'f3_paper_method_matrix.png', 'Methods used in each reference paper. Dark green cells marked * are adopted in this methodology; grey cells are used in the papers but not adopted.', 430));
K.push(H2('2.4 Supporting mustard studies from Bharatpur'));
K.push(P('Two hyperspectral studies on Indian mustard at Bharatpur, the planned validation site of this thesis, support several steps of the methodology (' + T('mustard') + '). They are used as mustard-specific evidence; the eight papers above remain the methodological basis.'));
K.push(...tab2('mustard', [
  ['Paper', 'Crop, stress and data', 'Key methods', 'Main result', 'Taken for this thesis'],
  ['Shukla et al. (2024), Remote Sens.', 'Mustard aphid (Lipaphis erysimi), severity grade 1–5 (AISG); ASD FieldSpec 4 canopy spectra (350–2500 nm, analysed 400–1100 nm); 8 farmers\' fields, two seasons', 'Savitzky–Golay smoothing (9 nm); Spearman correlation of reflectance, FD and SD with AISG; common sensitive regions; PCA and PLSR loadings; RSI, DSI, NDSI; PLSR, PCR and other regression models; 80/20 split', 'Common sensitive regions 483–487, 509–515, 690–714, 719–723 nm; key bands 679, 746, 979 nm; PLSR best (RMSE 0.66, r^{2} 0.71)', 'Correlation scalograms of R, FD and SD (Step 1.2); common-region rule; PLSR for severity; a mustard baseline to compare white rust bands with'],
  ['Bhattacharya and Chattopadhyay (2013), Comput. Electron. Agric.', 'Mustard Sclerotinia rot, 5 km × 5 km; Tmin, MODIS LST and NDWI, EO-1 Hyperion (30 m), LISS-IV mask; 16 sites', 'Stage I weather anomaly; Stage II TVDI–NDWI space (canopy stress without soil-moisture stress = rot); Stage III two-step stepwise canonical discriminant analysis (25 bands), 224 new band combinations', 'SWIR bands most sensitive (R^{2} 0.74–0.95); new three-band ROTI = R_{1175}/(R_{1982} + R_{691}), R^{2} 0.94; DWSI-1 and DWSI-4 retained', 'ROTI, DWSI-1 and DWSI-4 added to the HS indices; SWIR in the WRI search; separating disease from water stress in the thermal analysis'],
], [1500, 1900, 2250, 1950, 1706], 'Mustard hyperspectral studies from Bharatpur used as supporting evidence.', 16));
K.push(BL('**Caution 1.** Shukla et al. (2024) list the sensitive regions differently in the abstract (493–497, 509–515, 690–714, 717–721 and 752–756 nm) and in the results (Table 4: 483–487, 509–515, 690–714, 719–723 nm); the results table is quoted here.'));
K.push(BL('**Caution 2.** In Bhattacharya and Chattopadhyay (2013), the R^{2} values are fitted to five group means of disease incidence (16 sites), so they are optimistic; the DWSI-1 and DWSI-4 values also differ between text and figure (0.87 and 0.93). The indices are therefore tested here, not assumed to work for white rust.'));

// ======================= 3 =======================
K.push(H1('3. Overall workflow'));
K.push(P(F('workflow') + ' shows the workflow and ' + T('objmap') + ' links each objective to its ORW activities, methods and outputs.'));
K.push(...fig2('workflow', 'f1_workflow.png', 'Objective-wise workflow of the thesis.', 520));
K.push(...tab2('objmap', [
  ['Objective (ORW activities)', 'Question', 'Main methods (source)', 'Output'],
  ['1. Characterise (Act. 1.1–1.4)', 'Which features of each sensor respond to white rust (detection) and to its severity, and why?', 'Sensor-specific features; correlation scalograms + ReliefF + JM (HS); WRI (Mahlein 2013); t-test / Mann–Whitney, ANOVA / Kruskal–Wallis; Boruta (Mustafa 2023); cross-sensor correlation (Mahlein 2019)', 'Disease-specific feature (DSF) pools per sensor and task'],
  ['2. Detect and discriminate severity (Act. 2.1–2.3)', 'Which sensor or combination, fusion strategy and model detect white rust and discriminate its severity best?', 'VIF → ML-SFFS; pooled and sensor-wise ML-SFFS fusion (Mustafa 2023); DNN-F1/F2 (Maimaitijiang 2020); SVM, RF, k-NN, PLSR', 'Best sensor set, fusion and model for detection, severity classes and DI; maps'],
  ['3. Pre-symptomatic prediction (Act. 3.1)', 'Can later-infected plots be separated from healthy plots before symptoms?', 'Boruta → VIF → ML-SFFS; single sensors and fusion; SVM, RF, k-NN (Tian 2021; Mustafa 2023)', 'Best early-warning sensor set; risk maps'],
], [2000, 2300, 3200, 1806], 'Objectives, questions, methods and outputs.', 16));

// ======================= 4 =======================
K.push(H1('4. Experiment, ground truth and dataset'));
K.push(H2('4.1 Field experiment'));
K.push(P('The IARI experiment (2025–26) is a factorial randomised block design (RBD) with three factors: inoculation timing G1–G4 (about 50, 40, 30 and 20 days after sowing, created by staggered sowing on 20 Nov, 30 Nov, 10 Dec and 20 Dec 2025 and one inoculation on 10 Jan 2026), variety (V1 Varuna, highly susceptible; V2 Pusa Vijay, moderately susceptible; V3 PM 38, resistant) and dose (D1 control; D2 inoculated with 1.5 × 10^5 zoosporangia mL^{−1}). This gives 24 treatments × 3 replications = **72 plots** of 3 m × 3 m (' + F('design') + ').'));
K.push(...fig2('design', 'f4_design_validation.png', 'Factorial RBD with 72 plots in three replications and the replication-wise validation scheme.', 560));
K.push(H2('4.2 Ground truth, severity classes and tasks'));
K.push(BL('**Disease index (DI).** At the centre and four corners of each plot, fully expanded leaves of sampled plants are scored on the 0–6 scale of leaf area covered by pustules (0 none; 1 0–5%; 2 5–10%; 3 10–20%; 4 20–35%; 5 35–50%; 6 > 50%). The plot DI follows Liu et al. (2024):'));
K.push(EQ('DI (%) = [ Σ (x × f) / ( n × Σ f ) ] × 100', '1'));
K.push(P('where x is the score, f the number of leaves with that score and n = 6 the highest score.'));
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
K.push(H2('4.3 Pooled dataset'));
K.push(P('After pre-processing, every plot on every flight is one sample (plot-date). All flights are pooled into one dataset, because only the pooled data contain the full range from healthy to high severity, and the date is not used in any analysis. Pooling across dates was also used by Liu et al. (2024), who built one disease-index model over five dates, and by Feng et al. (2022). Repeated observations of the same plot are not independent, so every training/test split keeps all observations of a plot in the same set (Section 9; Roberts et al., 2017). ' + T('dataset') + ' summarises the dataset.'));
K.push(...tab2('dataset', [
  ['Item', 'Description'],
  ['Sample unit', 'One plot on one flight (plot-date)'],
  ['Post-symptomatic samples (Objectives 1, 2)', '72 plots × post-symptomatic flights (1296 plot-dates planned in the ORW)'],
  ['Pre-symptomatic samples (Objective 3)', '72 plots × 6 flights (432 plot-dates; ORW)'],
  ['Predictors', 'Sensor-specific features (Section 6.1)'],
  ['Targets', 'Health status; severity class; DI (%); staghead (%); pre-symptomatic label'],
  ['Grouping for validation', 'Plot ID and replication (R1–R3)'],
], [3200, 6106], 'Structure of the pooled dataset.', 17));

// ======================= 5 =======================
K.push(H1('5. Sensor-specific pre-processing'));
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

// ======================= 6 OBJECTIVE 1 =======================
K.push(H1('6. Objective 1: Characterise white rust through multimodal UAV sensing'));
K.push(LBL('Aim'));
K.push(P('To identify, for each sensor, which features differ between healthy and diseased plots (detection) and which change across the three severity classes and with DI (severity discrimination), and to explain these changes physiologically. Objective 1 has a common core applied to all sensors (statistics, Boruta, cross-sensor comparison) and sensor-specific parts (hyperspectral band-level analysis and the White Rust Index).'));
K.push(H2('6.1 Step 1.1: Sensor-specific feature extraction'));
K.push(H3('6.1.1 Hyperspectral features'));
K.push(...tab2('hsfeat', [
  ['Feature family', 'Number', 'Description', 'Reference'],
  ['Reflectance', '481 bands', 'Smoothed plot-mean reflectance of all retained bands', 'Tian 2021; Guo 2021'],
  ['First derivative (FD)', '481', 'Slope of the spectrum (Eq. 2); reduces illumination and background effects', 'Tsai and Philpot 1998'],
  ['Second derivative (SD)', '481', 'Curvature (Eq. 2); separates overlapping absorption features', 'Tsai and Philpot 1998'],
  ['Red-edge parameters', '3', 'REP, Dr, SDr (Eq. 3)', 'Horler et al. 1983; Filella and Peñuelas 1994'],
  ['Narrow-band indices', '39', 'Chlorophyll, pigment ratio, photosynthesis, stress and water indices (' + T('hsidx') + ')', 'See ' + T('hsidx')],
  ['White Rust Index (WRI)', '1', 'Disease-specific index built in Step 1.3', 'Mahlein et al. 2013'],
], [2100, 1100, 3900, 2206], 'Hyperspectral feature families.', 17));
K.push(P('Derivatives are computed with the Savitzky–Golay derivative filter on the smoothed spectra; in finite-difference form (Tsai and Philpot, 1998):'));
K.push(EQ('FD(λ_{i}) = [R(λ_{i+1}) − R(λ_{i−1})] / (λ_{i+1} − λ_{i−1})'));
K.push(EQ('SD(λ_{i}) = [FD(λ_{i+1}) − FD(λ_{i−1})] / (λ_{i+1} − λ_{i−1})', '2'));
K.push(EQ('REP = argmax_{680–750 nm} FD(λ);   Dr = max_{680–750 nm} FD(λ);   SDr = Σ_{680–750 nm} FD(λ) Δλ', '3'));
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
K.push(H3('6.1.2 Multispectral features'));
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
K.push(H3('6.1.3 RGB features'));
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
K.push(H3('6.1.4 Thermal features'));
K.push(P('The canopy temperature CT is the mean temperature of canopy pixels after K-means segmentation (Feng et al., 2022); AT is the air temperature at the time of the flight.'));
K.push(EQ('CTD = CT − AT;    CTR = (CT + 273.15) / (AT + 273.15)'));
K.push(EQ('NRCT = (CT − CT_{min}) / (CT_{max} − CT_{min});    MTD = T_{max} − T_{min}', '4'));
K.push(...tab2('tirfeat', [
  ['Feature', 'Description', 'Reference'],
  ['CT', 'Mean canopy temperature (°C)', 'Liu 2024'],
  ['CTD', 'Canopy minus air temperature; reduces the effect of weather', 'Feng 2022'],
  ['CTR', 'Canopy-to-air temperature ratio, computed in kelvin (a ratio of °C values depends on the temperature scale)', 'Feng 2022 (kelvin: this study)'],
  ['NRCT', 'Normalised relative canopy temperature; CT_{min} and CT_{max} are the lowest and highest canopy temperatures in the same thermal image', 'Feng 2022; Maimaitijiang 2020'],
  ['MTD', 'Maximum minus minimum canopy temperature within the plot', 'Mahlein 2019'],
  ['Thermal texture (8)', 'GLCM measures of the temperature image after quantisation to a fixed number of grey levels over one common temperature range for all flights; d = 1 pixel, θ = 0°, 45°, 90°, 135°', 'Maimaitijiang 2020 (texture of the thermal layer); Haralick et al. 1973'],
], [1900, 5000, 2406], 'Thermal features (13).', 16));

// ---- Step 1.2 HS band level ----
K.push(H2('6.2 Step 1.2: Hyperspectral band-level analysis (HS only)'));
K.push(P('Hyperspectral data contain 1443 band-level features (481 reflectance + 481 FD + 481 SD), far more than the number of plots. Band-level analysis therefore identifies a few robust bands before modelling. It is needed only for HS: the MS has five bands, and RGB and TIR features are not spectral bands. Because severity classes overlap, two complementary methods are combined (' + F('step12') + '): a correlation scalogram against DI, which needs no class boundaries (Cheng et al., 2010), and ReliefF, which is designed for noisy, overlapping, multi-class data (Robnik-Šikonja and Kononenko, 2003; Mahlein et al., 2013). JM distance only reports class overlap.'));
K.push(...fig2('step12', 'f7_step12.png', 'Sub-steps of the hyperspectral band-level analysis. Schematic curves are illustrations; real curves come from the UAV hyperspectral data.', 540));
K.push(LBL('Sub-step A. Data'));
K.push(BL('Pooled post-symptomatic plot-dates, including healthy plots; reflectance, FD and SD of all retained bands; targets: DI for sub-step B, health status (detection) and the three severity classes (severity) for sub-steps C and E.'));
K.push(BL('For the description in Objective 1 all IARI data are used. When selected bands become model inputs (Objectives 2 and 3), sub-steps B–D are repeated inside the training data of each cross-validation fold so that test plots never influence band selection (Ambroise and McLachlan, 2002; Varma and Simon, 2006).'));
K.push(LBL('Sub-step B. Correlation scalograms against DI (reflectance, FD, SD)'));
K.push(BL('For each band λ, Spearman\'s rank correlation ρ(λ) between the feature (R, FD or SD) and DI is computed over all samples (Spearman, 1904). Because many healthy plots share DI = 0, ρ is computed as the Pearson correlation of the ranks (Eq. 5); Pearson\'s r is reported alongside (Guo et al., 2021; Feng et al., 2022; Liu et al., 2024).'));
K.push(EQ('ρ(λ) = Σ (u_{i} − ū)(v_{i} − v̄) / √[ Σ (u_{i} − ū)^{2} Σ (v_{i} − v̄)^{2} ],   u_{i} = rank of the feature,  v_{i} = rank of DI_{i}', '5'));
K.push(BL('ρ(λ) is plotted against wavelength for R, FD and SD (three scalograms; Cheng et al., 2010). Bands with p < 0.01 (Guo et al., 2021) and in the top 5% of |ρ| (Tian et al., 2021) are retained; one band with the highest |ρ| is kept per spectral region (Tian et al., 2021). Repeated plot-dates make p-values optimistic, so bands are ranked mainly by |ρ|.'));
K.push(BL('Stability: the scalograms are repeated for replications R1, R2 and R3 separately; regions found in all three are stable.'));
K.push(BL('Common regions: regions significant in all three scalograms (R, FD and SD) are reported as common sensitive regions, as in the mustard aphid study of Shukla et al. (2024: 483–487, 509–515, 690–714 and 719–723 nm). Comparing the white rust regions with these shows whether white rust has a spectral signature different from aphid damage in the same crop.'));
K.push(LBL('Sub-step C. ReliefF relevance spectra (detection and severity)'));
K.push(BL('ReliefF is run twice: with health status (detection) and with the three severity classes (severity discrimination). For each sample x, its k nearest neighbours of the same class (hits H) and of every other class C (misses M) are found; a band gains weight when it differs between x and its misses and loses weight when it differs between x and its hits (Eq. 6; Robnik-Šikonja and Kononenko, 2003).'));
K.push(EQ('W(λ) ← W(λ) − Σ_{j=1}^{k} diff(λ, x, H_{j}) / (m k)'));
K.push(EQ('+ Σ_{C ≠ c(x)} [ P(C) / (1 − P(c(x))) ] Σ_{j=1}^{k} diff(λ, x, M_{j}(C)) / (m k)', '6'));
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
K.push(EQ('JM_{ij} = 2 [1 − exp(−B_{ij})]', '7'));
K.push(P('JM ranges from 0 (complete overlap) to 2 (complete separation); ≥ 1.9 indicates good separability. JM shows which classes overlap and explains classification errors; it is not used to select bands because it assumes normally distributed classes.'));

// ---- Step 1.3 WRI ----
K.push(H2('6.3 Step 1.3: White Rust Index (HS only)'));
K.push(...STEP('White Rust Index (WRI)',
  'Build one index specific to white rust from the UAV hyperspectral data.',
  'General vegetation indices also respond to nutrient or water stress; a disease-specific index of three bands reduces this confusion (Mahlein et al., 2013).',
  ['Data: healthy vs diseased plot-dates of the training data, 450–950 nm (range of Mahlein et al., 2013), averaged to about 10 nm.',
   'ReliefF ranks all single bands and all two-band normalised differences ND(λ_{1}, λ_{2}) = (R_{λ1} − R_{λ2})/(R_{λ1} + R_{λ2}); the top 25% of each are retained.',
   'All combinations of Eq. 8, with a minimum distance between combined bands, are tested exhaustively with an optimised threshold; the combination with the highest balanced accuracy in 8-fold stratified cross-validation is the WRI (Mahlein et al., 2013).',
   'The search is repeated with SWIR bands added (retained bands up to 2500 nm), because SWIR bands were the most sensitive to Sclerotinia rot in mustard and the three-band ROTI (red, NIR and SWIR) beat two-band indices (Bhattacharya and Chattopadhyay, 2013). The VNIR and VNIR + SWIR indices are compared and the better one is kept as the WRI.'],
  'Mahlein et al. (2013). Example of this form: sugar beet rust index = (R570 − R513)/(R570 + R513) + 0.5 × R704.'));
K.push(EQ('WRI = (R_{λ1} − R_{λ2}) / (R_{λ1} + R_{λ2}) + w R_{λ3},    w ∈ {−1, −0.5, 0, 0.5, 1}', '8'));

// ---- Step 1.4 statistics ----
K.push(H2('6.4 Step 1.4: Statistical characterisation (all sensors)'));
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
  ['Variance inflation factor', 'Collinearity before ML-SFFS (Objectives 2 and 3)'],
], [3800, 5506], 'Summary of statistical techniques.', 17));

// ---- Step 1.5 ML relevance ----
K.push(H2('6.5 Step 1.5: Machine-learning relevance (all sensors)'));
K.push(...STEP('Boruta relevance per sensor and task',
  'Identify the disease-specific features (DSFs) of each sensor, separately for detection, severity discrimination and DI.',
  'Statistics test one feature at a time; Boruta, built on random forest, also captures non-linear and interacting relevance and keeps every relevant feature without an arbitrary cut-off (Kursa and Rudnicki, 2010). Mustafa et al. (2023) used Boruta to select disease-specific features before ML-SFFS.',
  ['Input: all features of one sensor (for HS: the robust bands of Step 1.2, red-edge parameters, indices and WRI).',
   'Each feature is copied and shuffled ("shadow" features). A random forest is fitted on real and shadow features; the importance (Z-score of mean decrease in accuracy) of each real feature is compared with the best shadow feature over repeated runs (e.g. 100); features significantly more important are "confirmed", significantly less important are "rejected", the rest "tentative" (Kursa and Rudnicki, 2010).',
   'Run three times per sensor: classification with health status (detection), classification with the three severity classes (diseased plot-dates), and regression with DI.',
   'Output: importance boxplots and a table of confirmed / tentative / rejected features per sensor and task; confirmed features form the DSF pool of that sensor and task.'],
  'Mustafa et al. (2023); Kursa and Rudnicki (2010).'));
K.push(...STEP('Univariate regression of each DSF against DI',
  'Measure how well each DSF alone tracks severity.',
  'A simple, interpretable ranking that complements Boruta (Mustafa et al., 2023; Feng et al., 2022).',
  'Linear regression DI = a + b x for each DSF x; R^2 and RMSE are reported (Eq. 9).',
  'Mustafa et al. (2023): best single feature 1/R700, R^2 = 0.81; Feng et al. (2022): single index R^2 < 0.56.'));
K.push(EQ('DI_{i} = a + b x_{i} + ε_{i};    R^{2} = 1 − Σ (DI_{i} − DÎ_{i})^{2} / Σ (DI_{i} − mean DI)^{2}', '9'));

// ---- Step 1.6 cross-sensor ----
K.push(H2('6.6 Step 1.6: Cross-sensor characterisation'));
K.push(BL('**Cross-sensor correlation matrix:** Pearson correlation among the DSFs of all four sensors and with DI. Low correlation between sensors means complementary information and justifies fusion (approach of Mahlein et al., 2019, who correlated thermal, fluorescence and spectral parameters with each other and with disease severity).'));
K.push(BL('**JM distance per sensor:** JM between healthy, Low, Moderate and High computed with the few top DSFs of each sensor (Eq. 7), giving one comparable measure of how well each sensor separates the severity groups (Richards, 2013).'));
// ---- Step 1.7 sensor-wise implementation for MS, TIR, RGB ----
K.push(H2('6.7 Sensor-wise implementation of Objective 1 for multispectral, thermal and RGB data'));
K.push(P('Sections 6.4–6.6 apply to every sensor. This section gives the complete step-by-step procedure for the three non-hyperspectral datasets, which do not use band-level scalograms or the WRI. For each sensor the analysis is done twice, for detection (healthy vs diseased) and for severity (healthy, Low, Moderate, High and DI), on the pooled post-symptomatic plot-dates. ' + T('objsens') + ' summarises the three procedures.'));
K.push(H3('6.7.1 Multispectral data (MicaSense RedEdge-MX)'));
K.push(NLm('**Feature table.** For every plot-date: plot-mean reflectance of the five bands (B 475, G 560, R 668, RE 717, NIR 840 nm), the 12 vegetation indices of ' + T('msidx') + ', the 40 GLCM textures of the five bands and, optionally, percentile reflectance (20th–50th percentile of canopy pixels) and TTCI (Liu et al., 2024).'));
K.push(NLm('**Spectral response by group.** Mean ± standard deviation of each band for healthy, Low, Moderate and High plots, and the ratio of diseased to healthy reflectance per band. Expected: visible and red-edge reflectance rise and NIR reflectance falls as chlorophyll and leaf structure are lost (Liu et al., 2024; Guo et al., 2021).'));
K.push(NLm('**Pixel histograms and extraction method.** Frequency histograms of canopy-pixel reflectance of each band per group show whether disease shifts the whole distribution (Liu et al., 2024). The plot mean (CS) and percentile reflectance (LS) are compared by their correlation with DI; Liu et al. (2024) found LS more sensitive than CS for powdery mildew.'));
K.push(NLm('**Statistical tests (Section 6.4).** Detection: t-test or Mann–Whitney U for each band, index and texture. Severity: one-way ANOVA + Tukey HSD or Kruskal–Wallis + Dunn across healthy, Low, Moderate and High; Spearman ρ and Pearson r with DI (Liu et al., 2024; Feng et al., 2022; Tian et al., 2021).'));
K.push(NLm('**Physiological interpretation.** Correlation of the significant indices with chlorophyll a and b, carotenoid and anthocyanin (ORW Activity 1.2). Chlorophyll and red-edge indices (NDRE, MTCI, CI_{rededge}, PSRI) are expected to respond most; NDRE, PSRI and MTCI were the indices that consistently tracked wheat powdery mildew (Liu et al., 2024).'));
K.push(NLm('**Machine-learning relevance (Section 6.5).** Boruta on all MS features, separately for detection, severity classes and DI, gives the MS DSF pools (Mustafa et al., 2023); univariate regression of each DSF against DI gives R^2 and RMSE (Mustafa et al., 2023; Feng et al., 2022).'));
K.push(NLm('**Separability (Section 6.6).** JM distance between the four groups using the top MS DSFs (Richards, 2013).'));
K.push(BOX('MS output:', 'MS DSF pools for detection, severity and DI; the most sensitive bands and indices; whether percentile extraction is better than the plot mean.', 'EEF3E8', '2C5F2D'));
K.push(H3('6.7.2 Thermal data (FLIR Vue Pro R)'));
K.push(NLt('**Feature table.** For every plot-date: CT, CTD, CTR (kelvin), NRCT and MTD (Eq. 4) and the 8 GLCM textures of the quantised temperature image (' + T('tirfeat') + '; Feng et al., 2022; Mahlein et al., 2019; Maimaitijiang et al., 2020).'));
K.push(NLt('**Thermal response by group.** Maps and frequency histograms of canopy temperature for healthy, Low, Moderate and High plots; mean ± standard deviation of each thermal parameter per group. Expected: diseased canopies are warmer because infection disturbs stomatal regulation and transpiration; in wheat powdery mildew, DI and canopy temperature increased together (r = 0.88; Liu et al., 2024), and thermography showed temperature differences in infected spikelets (Mahlein et al., 2019).'));
K.push(NLt('**Raw versus normalised temperature.** Because all flights are pooled, CT is compared with CTD, CTR and NRCT by their correlation with DI. The normalised parameters remove the influence of air temperature and are expected to be more consistent (Feng et al., 2022, retained CTD and NRCT).'));
K.push(NLt('**Statistical tests (Section 6.4).** Detection: t-test or Mann–Whitney U; severity: ANOVA + Tukey HSD or Kruskal–Wallis + Dunn; Spearman ρ and Pearson r with DI.'));
K.push(NLt('**Physiological interpretation.** Correlation of CT, CTD and NRCT with stomatal conductance, transpiration rate and relative water content (ORW Activity 1.2); negative correlation with stomatal conductance would confirm that the thermal signal reflects reduced transpiration.'));
K.push(NLt('**Disease versus water stress.** A warm canopy can also mean water deficit. Following the logic of the TVDI–NDWI space of Bhattacharya and Chattopadhyay (2013), where canopy stress without soil-moisture stress indicated mustard rot, CTD and NRCT are plotted against a hyperspectral water index (WI or DWSI-1) and checked against the uniform irrigation of the plots. Diseased plots that are warmer without lower water status confirm a disease signal rather than drought.'));
K.push(NLt('**Machine-learning relevance.** Boruta for detection, severity and DI gives the TIR DSF pools; univariate regression against DI (Mustafa et al., 2023). MTD is reported even if not selected, because Mahlein et al. (2019) found it was the only parameter not correlated with disease severity.'));
K.push(NLt('**Separability.** JM distance between the four groups with the top TIR DSFs (Richards, 2013).'));
K.push(BOX('TIR output:', 'TIR DSF pools; how much warmer diseased canopies are at each severity level; the best normalised thermal parameter; the physiological basis of the thermal signal.', 'EEF3E8', '2C5F2D'));
K.push(H3('6.7.3 RGB data (DJI Phantom)'));
K.push(NLg('**Feature table.** For every plot-date: 8 GLCM textures of each of the R, G and B bands (' + T('rgbfeat') + '), mean hue, saturation and value of canopy pixels, vegetation fraction VF and, if a bare-soil elevation model is available, canopy height CH (Haralick et al., 1973; Feng et al., 2022; Liu et al., 2024; Mustafa et al., 2023; Maimaitijiang et al., 2020).'));
K.push(NLg('**Visual reference.** Example image patches of healthy, Low, Moderate and High plots document how pustules, chlorosis and stagheads appear at UAV resolution (as in Liu et al., 2024, Fig. 3).'));
K.push(NLg('**Texture response.** Each texture is compared across groups and correlated with DI. Expected: contrast, dissimilarity and entropy increase and homogeneity and second moment decrease as pustules and lesions make the canopy less uniform. Entropy was the texture most correlated with powdery-mildew DI (r = 0.486; Feng et al., 2022), and texture features were most informative at higher severity (Guo et al., 2021).'));
K.push(NLg('**Colour and structure.** Hue and saturation are expected to shift with chlorosis and white pustules (colour features as in Mustafa et al., 2023); VF and CH describe canopy thinning and staghead deformation (Maimaitijiang et al., 2020).'));
K.push(NLg('**Statistical tests and physiology (Section 6.4).** Detection: t-test or Mann–Whitney U; severity: ANOVA + Tukey HSD or Kruskal–Wallis + Dunn; Spearman ρ and Pearson r with DI; correlation of colour features with chlorophyll content and of VF/CH with LAI.'));
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
  ['Separability', 'JM, four groups', 'JM, four groups', 'JM, four groups'],
  ['Key references', 'Liu 2024; Guo 2021; Feng 2022; Mustafa 2023', 'Feng 2022; Liu 2024; Mahlein 2019; Maimaitijiang 2020', 'Feng 2022; Guo 2021; Liu 2024; Mustafa 2023; Maimaitijiang 2020; Haralick 1973'],
], [1700, 2600, 2500, 2506], 'Objective 1 procedure for the multispectral, thermal and RGB datasets.', 15));
K.push(BOX('How Objective 1 is satisfied:', 'for each sensor, the tests, correlations and Boruta show which features respond to white rust (detection) and which change across severity classes and with DI (severity), and the physiological correlations explain why. For HS, the correlation scalograms, ReliefF and the WRI identify white-rust wavelengths. The cross-sensor correlation and JM show which sensor separates severity best and whether sensors are complementary. Output: DSF pools per sensor and task for Objectives 2 and 3.', 'E3F2FD', '1565C0'));

// ======================= 7 OBJECTIVE 2 =======================
K.push(H1('7. Objective 2: Detect and discriminate severity through multimodal data fusion'));
K.push(LBL('Aim'));
K.push(P('To develop classification models for disease detection (task D) and severity discrimination into three classes (task S), and regression models for DI (task R), first with each UAV sensor separately and then with sensor combinations, and to identify the best sensor set, fusion strategy and model.'));
K.push(H2('7.1 Step 2.1: Feature selection for modelling (VIF → ML-SFFS)'));
K.push(P('The task-specific DSF pool of Objective 1 is reduced to an optimum feature combination (OFC) for each model (' + F('funnel') + '). Features are standardised with the mean and standard deviation of the training data (Eq. 10).'));
K.push(...fig2('funnel', 'f5_feature_selection.png', 'Feature selection from Objective 1 (Boruta DSF pool) to the optimum feature combination used in Objectives 2 and 3.', 470));
K.push(EQ('z = (x − μ_{train}) / σ_{train}', '10'));
K.push(...STEP('Variance inflation factor (VIF < 10)',
  'Remove DSFs that repeat the information of others.',
  'Many indices share the same bands (e.g. several NDVI and simple-ratio variants); collinear features make models unstable.',
  'For feature j, R_{j}^{2} is obtained by regressing feature j on all other retained features (Eq. 11); the feature with the largest VIF is removed and VIF is recomputed until all VIF < 10 (Kutner et al., 2005; Tian et al., 2021; Mustafa et al., 2023).',
  'Tian et al. (2021); Mustafa et al. (2023).'));
K.push(EQ('VIF_{j} = 1 / (1 − R_{j}^{2})', '11'));
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
K.push(H2('7.2 Step 2.2: Single-sensor models (RGB, MS, HS, TIR)'));
K.push(P('For each sensor separately (input sets S1–S4) and for each task, the task-specific DSF pool of that sensor goes through VIF and ML-SFFS, and the models of ' + T('models') + ' are trained:'));
K.push(BL('**Detection (D):** SVM, RF and k-NN on their own OFC; DNN-F1 on the DSF pool after VIF.'));
K.push(BL('**Severity discrimination (S):** the same models, trained on diseased plot-dates with the three classes.'));
K.push(BL('**Regression (R):** SVR, RFR and k-NN on their own OFC; PLSR and DNN-F1 on the DSF pool after VIF.'));
K.push(P('This gives the stand-alone performance of each sensor for each task, the reference against which fusion is judged (Mahlein et al., 2019; Feng et al., 2022).'));
K.push(H2('7.3 Step 2.3: Sensor combinations and fusion strategies'));
K.push(...tab2('inputsets', [
  ['Input set', 'Sensors', 'Rationale'],
  ['S1–S4', 'RGB; MS; HS; TIR (each alone)', 'Stand-alone ability of each sensor'],
  ['S5', 'RGB + TIR', 'Visible symptoms + stomatal response'],
  ['S6', 'MS + TIR', 'Low-cost operational pair (Liu 2024)'],
  ['S7', 'HS + TIR', 'Best pair in Mahlein 2019 (spectral + thermal)'],
  ['S8', 'RGB + MS + HS + TIR', 'Full multimodal fusion (Maimaitijiang 2020)'],
], [1700, 3300, 4306], 'Input sets (single sensors and the combinations listed in the ORW).', 17));
K.push(P('Each combination is fused at feature level by four strategies (' + F('fusion') + '). Fusion is done separately for each task, because the DSF pools are task-specific.'));
K.push(...fig2('fusion', 'f6_fusion_strategies.png', 'Single-sensor modelling (a) and the four feature-level fusion strategies (b–d).', 560));
K.push(H3('Fusion pipeline for classification (tasks D and S)'));
K.push(P('Inside each training fold (Section 9):'));
K.push(NLc('Take the task-specific Boruta DSF pool of each sensor in the set (Boruta repeated on the training data).'));
K.push(NLc('**FA – Pooled ML-SFFS fusion (Mustafa et al., 2023):** concatenate the DSFs of all sensors in the set → standardise → VIF < 10 on the pooled set → ML-SFFS with SVM, RF or k-NN as judge (criterion: macro-F1 for S, accuracy or F1 for D) → one cross-sensor OFC per classifier. The sensor make-up of the OFC shows which sensors contribute.'));
K.push(NLc('**FB – Sensor-wise ML-SFFS fusion (ORW Activity 3.1):** VIF and ML-SFFS within each sensor → concatenate the sensor OFCs → VIF < 10 → a final ML-SFFS pass removes cross-sensor redundancy → classifier.'));
K.push(NLc('**FC / FD – DNN fusion (Maimaitijiang et al., 2020):** DSFs of each sensor after VIF are fed to DNN-F1 (all features concatenated at the input) or DNN-F2 (one sub-network per sensor, joined at an intermediate layer), with a softmax output layer and cross-entropy loss (Eq. 17) for classes. This adapts the regression networks of Maimaitijiang et al. (2020) to classification by changing only the output layer and loss.'));
K.push(NLc('Train the classifier with class weights inversely proportional to class size; predict the held-out replication; compute the metrics of Section 7.5.'));
K.push(H3('Fusion pipeline for regression (task R)'));
K.push(NLr('Take the DI-specific Boruta DSF pool of each sensor in the set (training data).'));
K.push(NLr('**FA:** concatenate → standardise → VIF < 10 → ML-SFFS with SVR, RFR or k-NN as judge (criterion: cross-validated RMSE) → OFC → model.'));
K.push(NLr('**FB:** VIF and ML-SFFS (RMSE) within each sensor → concatenate the sensor OFCs → VIF → final SFFS pass → model.'));
K.push(NLr('**Linear baseline:** PLSR on the concatenated DSF pool after VIF (Maimaitijiang et al., 2020).'));
K.push(NLr('**FC / FD:** DNN-F1 and DNN-F2 with a linear output and mean-squared-error loss (Maimaitijiang et al., 2020).'));
K.push(NLr('Predict DI of the held-out replication; compute R^2, RMSE and NRMSE; derive severity classes from predicted DI and compare with direct classification.'));

// ---- models ----
K.push(H2('7.4 Step 2.4: Models'));
K.push(BL('**Support vector machine (SVM / SVR)** with radial basis function kernel (Cortes and Vapnik, 1995); one-vs-one voting for three classes; SVR with ε-insensitive loss; C and γ tuned by grid search (Tian et al., 2021; Mahlein et al., 2019).'));
K.push(EQ('f(x) = sign[ Σ_{i} α_{i} y_{i} K(x_{i}, x) + b ],   K(x_{i}, x) = exp(−γ ‖x − x_{i}‖^{2})', '12'));
K.push(BL('**Random forest (RF / RFR)** (Breiman, 2001): B trees grown on bootstrap samples with m random features per split; majority vote (classes) or mean (DI).'));
K.push(EQ('ŷ(x) = mode{ T_{b}(x) }  (classification);    ŷ(x) = (1/B) Σ_{b=1}^{B} T_{b}(x)  (regression)', '13'));
K.push(BL('**k-nearest neighbours (k-NN)** (Cover and Hart, 1967): majority class or mean DI of the k nearest training samples in standardised feature space (Euclidean distance; Tian et al., 2021; Mustafa et al., 2023).'));
K.push(BL('**Partial least squares regression (PLSR)** (Wold et al., 2001): projection of predictors and DI onto latent components; number of components by minimum cross-validated RMSE (Guo et al., 2021; Feng et al., 2022). PLSR also gave the best prediction of aphid severity grade in mustard (Shukla et al., 2024).'));
K.push(EQ('X = T P^{T} + E,     y = T q + f', '14'));
K.push(BL('**DNN-F1 and DNN-F2** (Maimaitijiang et al., 2020): fully connected layers with ReLU activation, batch normalisation (Ioffe and Szegedy, 2015) and dropout (Srivastava et al., 2014), Adam optimiser (Kingma and Ba, 2015) and early stopping on a plot-grouped validation split (' + F('dnn') + ').'));
K.push(EQ('h^{(l)} = Dropout( ReLU( BN( W^{(l)} h^{(l−1)} + b^{(l)} ) ) )', '15'));
K.push(EQ('DNN-F2:  h_{s} = g_{s}(x_{s}),  s ∈ {RGB, MS, HS, TIR};    z = g_{joint}( [h_{RGB}; h_{MS}; h_{HS}; h_{TIR}] )', '16'));
K.push(EQ('Regression:  ŷ = w^{T} z + c,   loss = mean (y − ŷ)^{2}'));
K.push(EQ('Classification:  p_{k} = exp(z_{k}) / Σ_{j} exp(z_{j}),   loss = − Σ_{k} y_{k} ln p_{k}', '17'));
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
K.push(H2('7.5 Step 2.5: Evaluation metrics'));
K.push(P('Classification metrics are computed from the confusion matrix (n_{ij} = samples of true class i predicted as class j; N = total; K = number of classes):'));
K.push(EQ('OA = Σ_{k} n_{kk} / N;   P_{k} = n_{kk} / Σ_{i} n_{ik};   R_{k} = n_{kk} / Σ_{j} n_{kj}'));
K.push(EQ('F1_{k} = 2 P_{k} R_{k} / (P_{k} + R_{k})', '18'));
K.push(EQ('macro-F1 = (1/K) Σ_{k} F1_{k};   κ = (p_{o} − p_{e}) / (1 − p_{e}),   p_{e} = Σ_{k} n_{k+} n_{+k} / N^{2}', '19'));
K.push(P('with p_{o} = OA (Cohen, 1960; Sokolova and Lapalme, 2009). For detection, sensitivity = TP/(TP + FN) and specificity = TN/(TN + FP). Regression is evaluated with (Liu et al., 2024):'));
K.push(EQ('R^{2} = 1 − Σ (y_{i} − ŷ_{i})^{2} / Σ (y_{i} − ȳ)^{2}'));
K.push(EQ('RMSE = √[ Σ (y_{i} − ŷ_{i})^{2} / n ];    NRMSE = RMSE / ȳ × 100', '20'));
K.push(P('The relative error of Feng et al. (2022) divides by each measured value and is undefined for healthy plots (DI = 0), so NRMSE is used instead.'));
K.push(...tab2('metrics', [
  ['Metric', 'Task', 'Interpretation'],
  ['OA, kappa', 'D, S, P', 'Overall correctness; agreement beyond chance'],
  ['Sensitivity, specificity', 'D, P', 'Diseased and healthy plots correctly identified'],
  ['Precision, recall, F1, macro-F1', 'D, S, P', 'Per-class performance; macro-F1 weights Low, Moderate and High equally'],
  ['R^{2}, RMSE, NRMSE', 'R', 'Explained variance; error in DI units; error relative to mean DI'],
], [3000, 1300, 5006], 'Evaluation metrics.', 17));
K.push(H2('7.6 Step 2.6: Comparison, robustness and maps'));
K.push(BL('**Sensors and fusion:** for each task, S1–S4 are compared with S5–S8, and FA, FB, FC and FD are compared. A fusion is useful only if it beats the best single sensor on the test replications and at Bharatpur.'));
K.push(BL('**Robustness across varieties:** absolute errors of Varuna, Pusa Vijay and PM 38 are compared by one-way ANOVA + Tukey HSD (approach of Maimaitijiang et al., 2020).'));
K.push(BL('**Interpretation:** features of each OFC and their sensor origin; RF importance of the best model.'));
K.push(BL('**Maps:** detection followed by severity classification gives a map of healthy, Low, Moderate and High plots; the best regression model maps DI and its absolute error (Liu et al., 2024).'));
K.push(BOX('How Objective 2 is satisfied:', 'detection, three-class severity discrimination and DI estimation are each modelled with every sensor alone and with four combinations, using two ML-SFFS fusion strategies and two DNN fusion strategies. The comparison identifies the best sensor set, fusion strategy and model for each task.', 'FCE4EC', 'AD1457'));

// ======================= 8 OBJECTIVE 3 =======================
K.push(H1('8. Objective 3: Pre-symptomatic prediction'));
K.push(LBL('Aim'));
K.push(P('To separate inoculated plots that later develop white rust from healthy plots using UAV data collected before visible symptoms, with each sensor and with fused sensors.'));
K.push(...STEP('Step 3.1. Samples and labels',
  'Pool all pre-symptomatic flights (432 plot-dates; ORW) and label them.',
  'Wrong labels are the main risk in pre-symptomatic work.',
  ['Control plots = healthy; inoculated plots = infected only if symptoms later appear on them (Tian et al., 2021).',
   'Inoculated plots of the resistant variety (PM 38) that never show symptoms are excluded from the infected class and reported separately.',
   'Biochemical and biophysical parameters that differ between healthy and infected plots (t-test / Mann–Whitney U) are identified (ORW Activity 3.1).'],
  'Tian et al. (2021).'));
K.push(...STEP('Step 3.2. Pre-symptomatic features',
  'Find the features that differ before symptoms, for each sensor.',
  'Early changes are small and may involve other features than visible disease.',
  ['All features of Section 6.1 are tested between healthy and infected plots (t-test / Mann–Whitney U; Tian et al., 2021).',
   'HS: ReliefF (Step 1.2, sub-step C) is run with labels healthy vs infected to find pre-symptomatic bands (DI is 0 before symptoms, so the DI scalogram is not used).',
   'Boruta per sensor with the pre-symptomatic labels gives the pre-symptomatic DSF pools.'],
  'Tian et al. (2021); Mustafa et al. (2023).'));
K.push(...STEP('Step 3.3. Single-sensor and fused classification',
  'Classify healthy vs infected plots with each sensor and with fused sets.',
  'Identifies the sensor set that gives the most reliable early warning (Mahlein et al., 2019).',
  ['S1–S4: VIF → ML-SFFS → SVM, RF, k-NN. S5–S8: pooled (FA) and sensor-wise (FB) ML-SFFS fusion with the same classifiers.',
   'DNNs are not used, because 432 plot-dates from 72 plots are too few to train them reliably.',
   'Where physiological parameters change significantly before symptoms, PLSR and RFR estimate them from the selected features (ORW Activity 3.1).',
   'Metrics: OA, kappa, sensitivity, specificity, F1 (Section 7.5).'],
  'Tian et al. (2021); Mustafa et al. (2023); Mahlein et al. (2019).'));
K.push(...STEP('Step 3.4. Risk maps',
  'Map the probability of infection of each plot.',
  'Practical early-warning output.',
  'Class probabilities of the best model are mapped plot by plot (mapping approach of Liu et al., 2024).',
  'Liu et al. (2024).'));
K.push(BOX('How Objective 3 is satisfied:', 'the pooled pre-symptomatic models show whether white rust can be predicted before symptoms and which sensor or fusion gives the best early warning; risk maps show where infection is developing.', 'FCE4EC', 'AD1457'));

// ======================= 9 VALIDATION =======================
K.push(H1('9. Validation design'));
K.push(...STEP('Step V1. Leave-one-replication-out cross-validation (IARI 2025–26)',
  'Train on two replications and test on the third; repeat three times (' + F('design') + ').',
  'Each RBD replication contains every treatment once, so each test fold is a balanced copy of the experiment. All observations of a plot stay in the same fold, so no test plot is seen during training (Roberts et al., 2017).',
  ['Outer loop: R1, R2 and R3 held out in turn. Inner loop (two training replications): 4-fold cross-validation grouped by plot for Boruta, HS band selection, VIF, ML-SFFS and tuning.',
   'Reported performance: mean ± standard deviation over the three test replications. The final model is refitted on all IARI data.'],
  'Roberts et al. (2017); Ambroise and McLachlan (2002); Varma and Simon (2006).'));
K.push(...STEP('Step V2. Two-stage independent validation (2026–27)',
  'Test the final models on data never used for development.',
  'Validation on a separate experiment is the strongest test of transferability (Feng et al., 2022).',
  ['Stage 1: planned experiment at the IIRMR Research Farm, Bharatpur (local varieties).',
   'Stage 2: adjoining farmers\' fields with the same ground-truth survey.'],
  'Feng et al. (2022); ORW Activity 2.3.'));
K.push(...tab2('runs', [
  ['Input sets', 'Strategy', 'Detection (D) and severity (S)', 'Regression (R)'],
  ['S1–S4', 'a: DSF → VIF → ML-SFFS', 'SVM, RF, k-NN; DNN-F1 (DSF + VIF)', 'SVR, RFR, k-NN; PLSR, DNN-F1 (DSF + VIF)'],
  ['S5–S8', 'FA: pooled ML-SFFS', 'SVM, RF, k-NN', 'SVR, RFR, k-NN'],
  ['S5–S8', 'FB: sensor-wise ML-SFFS', 'SVM, RF, k-NN', 'SVR, RFR, k-NN'],
  ['S5–S8', 'Concatenation (DSF + VIF)', '–', 'PLSR'],
  ['S5–S8', 'FC / FD: DNN-F1 / DNN-F2', 'DNN-F1, DNN-F2 (softmax)', 'DNN-F1, DNN-F2 (linear output)'],
], [1500, 2500, 2600, 2706], 'Complete modelling plan of Objective 2 (Objective 3 uses the SVM, RF and k-NN rows of D).', 16));
K.push(H2('9.1 Software'));
K.push(P('Python with scikit-learn (Pedregosa et al., 2011) for SVM, RF, k-NN and PLSR; mlxtend (Raschka, 2018) for SFFS, as used by Mustafa et al. (2023); Boruta (Kursa and Rudnicki, 2010); statsmodels and SciPy for VIF and tests; TensorFlow/Keras for DNN-F1 and DNN-F2, as in Maimaitijiang et al. (2020). Equivalent R packages (Boruta, caret, e1071, kknn; Tian et al., 2021) may be used, as planned in the ORW.'));

// ======================= 10 SUMMARY & CORRECTIONS =======================
K.push(H1('10. Summary and corrections'));
K.push(...tab2('satisfy', [
  ['Objective', 'Per-sensor steps', 'Fusion', 'Models', 'Deliverable'],
  ['1. Characterise', 'Sensor-specific features; HS band-level analysis and WRI; statistics (detection, severity); Boruta; univariate regression', 'Cross-sensor correlation; JM per sensor', 'None (threshold classifier for WRI)', 'DSF pools per sensor and task; physiological explanation'],
  ['2. Detect and discriminate', 'VIF → ML-SFFS for D, S, R', 'FA, FB, DNN-F1, DNN-F2', 'SVM, RF, k-NN, PLSR, DNN-F1, DNN-F2', 'Best sensor set, fusion and model; maps'],
  ['3. Pre-symptomatic', 'Screening; ReliefF (HS); Boruta → VIF → ML-SFFS', 'FA, FB', 'SVM, RF, k-NN (PLSR, RFR for physiology)', 'Early-warning sensor set; risk maps'],
], [1500, 2800, 1700, 1700, 1606], 'Objective-wise summary.', 16));
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

// ======================= 11, 12 =======================
K.push(H1('11. Expected outcomes'));
K.push(BL('Disease-specific features of each UAV sensor for detection and for severity, their physiological meaning, robust white-rust wavelengths and a White Rust Index (Objective 1).'));
K.push(BL('The best sensor, combination, fusion strategy and model for detection, three-class severity discrimination and DI estimation; HS + TIR fusion and DNN-F2 are expected to perform well (Mahlein et al., 2019; Maimaitijiang et al., 2020), and ML-SFFS to give compact cross-sensor feature sets (Mustafa et al., 2023) (Objective 2).'));
K.push(BL('A pre-symptomatic detection model and early-warning maps (Objective 3).'));
K.push(H1('12. Likely interview questions and short answers'));
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

// ======================= REFERENCES =======================
K.push(H1('References'));
const refPara = r => new Paragraph({ spacing: { after: 70, line: 255 }, indent: { left: 400, hanging: 400 }, children: [new TextRun({ text: r, font: FONT, size: 18 })] });
K.push(H2('Reference papers (basis of the methodology)'));
[
  'Feng, Z., Song, L., Duan, J., He, L., Zhang, Y., Wei, Y., Feng, W. (2022). Monitoring wheat powdery mildew based on hyperspectral, thermal infrared, and RGB image data fusion. Sensors 22(1), 31. https://doi.org/10.3390/s22010031',
  'Guo, A., Huang, W., Dong, Y., Ye, H., Ma, H., Liu, B., Wu, W., Ren, Y., Ruan, C., Geng, Y. (2021). Wheat yellow rust detection using UAV-based hyperspectral technology. Remote Sensing 13(1), 123. https://doi.org/10.3390/rs13010123',
  'Liu, Y., Liu, G., Sun, H., An, L., Zhao, R., Liu, M., Tang, W., Li, M., Yan, X., Ma, Y., Zhao, F. (2024). Exploring multi-features in UAV based optical and thermal infrared images to estimate disease severity of wheat powdery mildew. Computers and Electronics in Agriculture 225, 109285. https://doi.org/10.1016/j.compag.2024.109285',
  'Mahlein, A.-K., Rumpf, T., Welke, P., Dehne, H.-W., Plümer, L., Steiner, U., Oerke, E.-C. (2013). Development of spectral indices for detecting and identifying plant diseases. Remote Sensing of Environment 128, 21–30. https://doi.org/10.1016/j.rse.2012.09.019',
  'Mahlein, A.-K., Alisaac, E., Al Masri, A., Behmann, J., Dehne, H.-W., Oerke, E.-C. (2019). Comparison and combination of thermal, fluorescence, and hyperspectral imaging for monitoring Fusarium head blight of wheat on spikelet scale. Sensors 19(10), 2281. https://doi.org/10.3390/s19102281',
  'Maimaitijiang, M., Sagan, V., Sidike, P., Hartling, S., Esposito, F., Fritschi, F.B. (2020). Soybean yield prediction from UAV using multimodal data fusion and deep learning. Remote Sensing of Environment 237, 111599. https://doi.org/10.1016/j.rse.2019.111599',
  'Mustafa, G., Zheng, H., Li, W., Yin, Y., Wang, Y., Zhou, M., Liu, P., Bilal, M., Jia, H., Li, G., Cheng, T., Tian, Y., Cao, W., Zhu, Y., Yao, X. (2023). Fusarium head blight monitoring in wheat ears using machine learning and multimodal data from asymptomatic to symptomatic periods. Frontiers in Plant Science 13, 1102341. https://doi.org/10.3389/fpls.2022.1102341',
  'Tian, L., Xue, B., Wang, Z., Li, D., Yao, X., Cao, Q., Zhu, Y., Cao, W., Cheng, T. (2021). Spectroscopic detection of rice leaf blast infection from asymptomatic to mild stages with integrated machine learning and feature selection. Remote Sensing of Environment 257, 112350. https://doi.org/10.1016/j.rse.2021.112350',
].forEach(r => K.push(refPara(r)));
K.push(H2('Supporting mustard studies'));
[
  'Bhattacharya, B.K., Chattopadhyay, C. (2013). A multi-stage tracking for mustard rot disease combining surface meteorology and satellite remote sensing. Computers and Electronics in Agriculture 90, 35–44. https://doi.org/10.1016/j.compag.2012.10.001',
  'Shukla, K.K., Nigam, R., Birah, A., Kanojia, A.K., Kumar, A., Bhattacharya, B.K., Chander, S. (2024). Detection of aphid-infested mustard crop using ground spectroscopy. Remote Sensing 16(1), 47. https://doi.org/10.3390/rs16010047',
].forEach(r => K.push(refPara(r)));
K.push(H2('Vegetation indices and spectral features'));
[
  'Apan, A., Held, A., Phinn, S., Markley, J. (2004). Detecting sugarcane \'orange rust\' disease using EO-1 Hyperion hyperspectral imagery. International Journal of Remote Sensing 25(2), 489–498.',
  'Babar, M.A., Reynolds, M.P., van Ginkel, M., Klatt, A.R., Raun, W.R., Stone, M.L. (2006). Spectral reflectance indices as a potential indirect selection criteria for wheat yield under irrigation. Crop Science 46(2), 578–588.',
  'Barnes, J.D., Balaguer, L., Manrique, E., Elvira, S., Davison, A.W. (1992). A reappraisal of the use of DMSO for the extraction and determination of chlorophylls a and b in lichens and higher plants. Environmental and Experimental Botany 32(2), 85–100.',
  'Bausch, W.C., Duke, H.R. (1996). Remote sensing of plant nitrogen status in corn. Transactions of the ASAE 39(5), 1869–1875.',
  'Blackburn, G.A. (1998). Quantifying chlorophylls and carotenoids at leaf and canopy scales: an evaluation of some hyperspectral approaches. Remote Sensing of Environment 66(3), 273–285.',
  'Broge, N.H., Leblanc, E. (2001). Comparing prediction power and stability of broadband and hyperspectral vegetation indices for estimation of green leaf area index and canopy chlorophyll density. Remote Sensing of Environment 76(2), 156–172.',
  'Chappelle, E.W., Kim, M.S., McMurtrey, J.E. (1992). Ratio analysis of reflectance spectra (RARS): an algorithm for the remote estimation of the concentrations of chlorophyll a, chlorophyll b, and carotenoids in soybean leaves. Remote Sensing of Environment 39(3), 239–247.',
  'Chen, J.M. (1996). Evaluation of vegetation indices and a modified simple ratio for boreal applications. Canadian Journal of Remote Sensing 22(3), 229–242.',
  'Dash, J., Curran, P.J. (2004). The MERIS terrestrial chlorophyll index. International Journal of Remote Sensing 25(23), 5403–5413.',
  'Daughtry, C.S.T., Walthall, C.L., Kim, M.S., de Colstoun, E.B., McMurtrey, J.E. (2000). Estimating corn leaf chlorophyll concentration from leaf and canopy reflectance. Remote Sensing of Environment 74(2), 229–239.',
  'Filella, I., Peñuelas, J. (1994). The red edge position and shape as indicators of plant chlorophyll content, biomass and hydric status. International Journal of Remote Sensing 15(7), 1459–1470.',
  'Gamon, J.A., Peñuelas, J., Field, C.B. (1992). A narrow-waveband spectral index that tracks diurnal changes in photosynthetic efficiency. Remote Sensing of Environment 41(1), 35–44.',
  'Gitelson, A., Merzlyak, M.N. (1994). Spectral reflectance changes associated with autumn senescence of Aesculus hippocastanum L. and Acer platanoides L. leaves. Journal of Plant Physiology 143(3), 286–292.',
  'Gitelson, A.A., Kaufman, Y.J., Merzlyak, M.N. (1996). Use of a green channel in remote sensing of global vegetation from EOS-MODIS. Remote Sensing of Environment 58(3), 289–298.',
  'Gitelson, A.A., Merzlyak, M.N., Chivkunova, O.B. (2001). Optical properties and nondestructive estimation of anthocyanin content in plant leaves. Photochemistry and Photobiology 74(1), 38–45.',
  'Gitelson, A.A., Kaufman, Y.J., Stark, R., Rundquist, D. (2002). Novel algorithms for remote estimation of vegetation fraction. Remote Sensing of Environment 80(1), 76–87.',
  'Gitelson, A.A., Gritz, Y., Merzlyak, M.N. (2003). Relationships between leaf chlorophyll content and spectral reflectance and algorithms for non-destructive chlorophyll assessment in higher plant leaves. Journal of Plant Physiology 160(3), 271–282.',
  'Haboudane, D., Miller, J.R., Tremblay, N., Zarco-Tejada, P.J., Dextraze, L. (2002). Integrated narrow-band vegetation indices for prediction of crop chlorophyll content for application to precision agriculture. Remote Sensing of Environment 81(2–3), 416–426.',
  'Haboudane, D., Miller, J.R., Pattey, E., Zarco-Tejada, P.J., Strachan, I.B. (2004). Hyperspectral vegetation indices and novel algorithms for predicting green LAI of crop canopies: modeling and validation in the context of precision agriculture. Remote Sensing of Environment 90(3), 337–352.',
  'Haralick, R.M., Shanmugam, K., Dinstein, I. (1973). Textural features for image classification. IEEE Transactions on Systems, Man, and Cybernetics SMC-3(6), 610–621.',
  'Horler, D.N.H., Dockray, M., Barber, J. (1983). The red edge of plant leaf reflectance. International Journal of Remote Sensing 4(2), 273–288.',
  'Huete, A.R. (1988). A soil-adjusted vegetation index (SAVI). Remote Sensing of Environment 25(3), 295–309.',
  'Jordan, C.F. (1969). Derivation of leaf-area index from quality of light on the forest floor. Ecology 50(4), 663–666.',
  'Merton, R., Huntington, J. (1999). Early simulation results of the ARIES-1 satellite sensor for multi-temporal vegetation research derived from AVIRIS. Proceedings of the 8th JPL Airborne Earth Science Workshop, Pasadena.',
  'Merzlyak, M.N., Gitelson, A.A., Chivkunova, O.B., Rakitin, V.Y. (1999). Non-destructive optical detection of pigment changes during leaf senescence and fruit ripening. Physiologia Plantarum 106(1), 135–141.',
  'Metternicht, G. (2003). Vegetation indices derived from high-resolution airborne videography for precision crop management. International Journal of Remote Sensing 24(14), 2855–2877.',
  'Peñuelas, J., Gamon, J.A., Fredeen, A.L., Merino, J., Field, C.B. (1994). Reflectance indices associated with physiological changes in nitrogen- and water-limited sunflower leaves. Remote Sensing of Environment 48(2), 135–146.',
  'Peñuelas, J., Baret, F., Filella, I. (1995). Semi-empirical indices to assess carotenoids/chlorophyll a ratio from leaf spectral reflectance. Photosynthetica 31(2), 221–230.',
  'Peñuelas, J., Piñol, J., Ogaya, R., Filella, I. (1997). Estimation of plant water concentration by the reflectance Water Index WI (R900/R970). International Journal of Remote Sensing 18(13), 2869–2875.',
  'Raun, W.R., Solie, J.B., Johnson, G.V., Stone, M.L., Lukina, E.V., Thomason, W.E., Schepers, J.S. (2001). In-season prediction of potential grain yield in winter wheat using canopy reflectance. Agronomy Journal 93(1), 131–138.',
  'Rondeaux, G., Steven, M., Baret, F. (1996). Optimization of soil-adjusted vegetation indices. Remote Sensing of Environment 55(2), 95–107.',
  'Roujean, J.-L., Bréon, F.-M. (1995). Estimating PAR absorbed by vegetation from bidirectional reflectance measurements. Remote Sensing of Environment 51(3), 375–384.',
  'Rouse, J.W., Haas, R.H., Schell, J.A., Deering, D.W. (1974). Monitoring vegetation systems in the Great Plains with ERTS. Third ERTS Symposium, NASA SP-351, Vol. 1, 309–317.',
  'Savitzky, A., Golay, M.J.E. (1964). Smoothing and differentiation of data by simplified least squares procedures. Analytical Chemistry 36(8), 1627–1639.',
  'Tsai, F., Philpot, W. (1998). Derivative analysis of hyperspectral data. Remote Sensing of Environment 66(1), 41–51.',
].forEach(r => K.push(refPara(r)));
K.push(H2('Statistical, feature-selection and machine-learning methods'));
[
  'Ambroise, C., McLachlan, G.J. (2002). Selection bias in gene extraction on the basis of microarray gene-expression data. Proceedings of the National Academy of Sciences 99(10), 6562–6566.',
  'Breiman, L. (2001). Random forests. Machine Learning 45(1), 5–32.',
  'Cheng, T., Rivard, B., Sánchez-Azofeifa, G.A., Feng, J., Calvo-Polanco, M. (2010). Continuous wavelet analysis for the detection of green attack damage due to mountain pine beetle infestation. Remote Sensing of Environment 114(4), 899–910.',
  'Cohen, J. (1960). A coefficient of agreement for nominal scales. Educational and Psychological Measurement 20(1), 37–46.',
  'Cortes, C., Vapnik, V. (1995). Support-vector networks. Machine Learning 20(3), 273–297.',
  'Cover, T., Hart, P. (1967). Nearest neighbor pattern classification. IEEE Transactions on Information Theory 13(1), 21–27.',
  'Dunn, O.J. (1964). Multiple comparisons using rank sums. Technometrics 6(3), 241–252.',
  'Ioffe, S., Szegedy, C. (2015). Batch normalization: accelerating deep network training by reducing internal covariate shift. Proceedings of the 32nd International Conference on Machine Learning, PMLR 37, 448–456.',
  'Kingma, D.P., Ba, J. (2015). Adam: a method for stochastic optimization. 3rd International Conference on Learning Representations (ICLR). arXiv:1412.6980.',
  'Kononenko, I. (1994). Estimating attributes: analysis and extensions of RELIEF. Proceedings of the European Conference on Machine Learning (ECML-94), LNCS 784, 171–182.',
  'Kruskal, W.H., Wallis, W.A. (1952). Use of ranks in one-criterion variance analysis. Journal of the American Statistical Association 47(260), 583–621.',
  'Kursa, M.B., Rudnicki, W.R. (2010). Feature selection with the Boruta package. Journal of Statistical Software 36(11), 1–13.',
  'Kutner, M.H., Nachtsheim, C.J., Neter, J., Li, W. (2005). Applied Linear Statistical Models, 5th ed. McGraw-Hill/Irwin, New York.',
  'Levene, H. (1960). Robust tests for equality of variances. In: Olkin, I. (Ed.), Contributions to Probability and Statistics. Stanford University Press, 278–292.',
  'Mann, H.B., Whitney, D.R. (1947). On a test of whether one of two random variables is stochastically larger than the other. Annals of Mathematical Statistics 18(1), 50–60.',
  'Pedregosa, F., et al. (2011). Scikit-learn: machine learning in Python. Journal of Machine Learning Research 12, 2825–2830.',
  'Pudil, P., Novovičová, J., Kittler, J. (1994). Floating search methods in feature selection. Pattern Recognition Letters 15(11), 1119–1125.',
  'Raschka, S. (2018). MLxtend: providing machine learning and data science utilities and extensions to Python\'s scientific computing stack. Journal of Open Source Software 3(24), 638.',
  'Richards, J.A. (2013). Remote Sensing Digital Image Analysis: An Introduction, 5th ed. Springer, Berlin.',
  'Roberts, D.R., et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. Ecography 40(8), 913–929.',
  'Robnik-Šikonja, M., Kononenko, I. (2003). Theoretical and empirical analysis of ReliefF and RReliefF. Machine Learning 53(1–2), 23–69.',
  'Schmidt, K.S., Skidmore, A.K. (2003). Spectral discrimination of vegetation types in a coastal wetland. Remote Sensing of Environment 85(1), 92–108.',
  'Shapiro, S.S., Wilk, M.B. (1965). An analysis of variance test for normality (complete samples). Biometrika 52(3–4), 591–611.',
  'Sokolova, M., Lapalme, G. (2009). A systematic analysis of performance measures for classification tasks. Information Processing and Management 45(4), 427–437.',
  'Spearman, C. (1904). The proof and measurement of association between two things. American Journal of Psychology 15(1), 72–101.',
  'Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., Salakhutdinov, R. (2014). Dropout: a simple way to prevent neural networks from overfitting. Journal of Machine Learning Research 15, 1929–1958.',
  'Tukey, J.W. (1949). Comparing individual means in the analysis of variance. Biometrics 5(2), 99–114.',
  'Varma, S., Simon, R. (2006). Bias in error estimation when using cross-validation for model selection. BMC Bioinformatics 7, 91.',
  'Wold, S., Sjöström, M., Eriksson, L. (2001). PLS-regression: a basic tool of chemometrics. Chemometrics and Intelligent Laboratory Systems 58(2), 109–130.',
].forEach(r => K.push(refPara(r)));

// order checks
const chk = (u, o, n) => { if (JSON.stringify(u) !== JSON.stringify(o)) { console.error(n + ' order mismatch', u, o); process.exit(1); } };
chk(usedF, FORDER, 'figure'); chk(usedT, TORDER, 'table');

const doc = new Document({
  features: { updateFields: true }, creator: 'Animesh Panda', title: 'AI-based multimodal UAV sensing of white rust in mustard: methodology',
  styles: { default: { document: { run: { font: FONT, size: 22 } }, heading1: hs(30, '1E3A1F', 320, 140, false, 0), heading2: hs(25, '2C5F2D', 220, 100, false, 1), heading3: hs(23, '2C5F2D', 180, 80, true, 2) } },
  numbering: { config: [
    { reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
                                 { level: 1, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1080, hanging: 360 } } } }] },
    { reference: 'num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: 'numc', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: 'numr', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: 'numm', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: 'numt', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    { reference: 'numg', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1300, bottom: 1300, left: 1300, right: 1300 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18 })] })] }) },
    children: K }] });
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('saved', OUT); });
