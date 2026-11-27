// One slide: Fusion strategies (Objective 2), aligned with the 2026-27 methodology (Steps 2.2–2.6, 2.8). Native shapes, editable.
const pptxgen = require('pptxgenjs');
const OUT = process.argv[2] || 'Fusion_strategies_slide.pptx';
const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.title = 'Fusion strategies';
const NAVY = '1F3864', PUR = '7030A0', LAV = 'F1E6F8', LAV2 = 'EADCF4', SEN = 'EEF1F7', YEL = 'FFF4D6', GOLD = 'C9A227', GREY = '595959', ARROW = '595959';
const s = pres.addSlide();
s.background = { color: 'FFFFFF' };
s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 13.333, h: 0.09, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
s.addText('Fusion strategies (Activities 2.2–2.6)', { x: 0.45, y: 0.22, w: 12.43, h: 0.75, fontFace: 'Cambria', fontSize: 32, bold: true, color: NAVY, align: 'center', valign: 'middle', isTextBox: true });
s.addShape(pres.shapes.LINE, { x: 0.45, y: 1.0, w: 12.43, h: 0, line: { color: '2F5D8A', width: 1.25 } });
// ---------- four cards
const cards = [
  ['Feature-level fusion + ML (2.2–2.4)', ['Camera DSFs from Objective 1 (33 training plots) joined for each sensor set → VIF < 10 again', 'SVM/SVR, RF, k-NN, PLS-DA/PLSR: SFFS (≤ 15 features) → grid search, GroupKFold(3) by plot', 'Selected features show which camera contributes'], 'Feng et al., 2022; Huang et al., 2020'],
  ['DNN-F1: input-level fusion (2.5)', ['Joined DSF vector of the set is the input of one dense network', '64 → 32 units, batch normalisation, ReLU, dropout 0.3; softmax (A, B) or linear output (C)', 'All 15 sensor sets; early stopping on the 11 validation plots'], 'Maimaitijiang et al., 2020'],
  ['DNN-F2: intermediate fusion (2.5)', ['One branch per camera (dense 32, BN, ReLU, dropout 0.3)', 'Squeeze-and-excitation layer learns one weight per camera; weighted branches joined → dense 32 → output', '11 multi-camera sets; camera weights recorded'], 'Maimaitijiang et al., 2020; Deng et al., 2024; Hu et al., 2018'],
  ['Pseudo-image networks (2.6)', ['Fused DSF arranged as a k × k pseudo-image (k = ⌈√p⌉)', 'DT-EDNet vs EfficientNet-B0, ResNet18, ConvNeXt V2-Atto with identical settings (AdamW, 300 epochs, patience 60)', 'Tasks A, B; all 15 sets; DT-EDNet module ablation'], 'Ma et al., 2026']];
const CW = 2.95, CX = [0.45, 3.61, 6.77, 9.93], CY = 1.2, CH = 2.6, HH = 0.42;
cards.forEach(([head, items, ref], i) => {
  const x = CX[i];
  s.addShape(pres.shapes.RECTANGLE, { x, y: CY, w: CW, h: CH, fill: { color: LAV }, line: { color: PUR, width: 1.25 }, objectName: 'card ' + head });
  s.addShape(pres.shapes.RECTANGLE, { x, y: CY, w: CW, h: HH, fill: { color: PUR }, line: { color: PUR, width: 1.25 } });
  s.addText(head, { x, y: CY, w: CW, h: HH, fontFace: 'Calibri', fontSize: 13.5, bold: true, color: 'FFFFFF', align: 'center', valign: 'middle', isTextBox: true, margin: 0.03 });
  s.addText(items.map((t, k) => ({ text: t, options: { bullet: { indent: 11 }, breakLine: true, paraSpaceAfter: 3 } })).concat([{ text: ref, options: { italic: true, color: GREY, fontSize: 10.5 } }]),
    { x: x + 0.06, y: CY + HH + 0.04, w: CW - 0.12, h: CH - HH - 0.08, fontFace: 'Calibri', fontSize: 12, color: '1A1A1A', valign: 'top', isTextBox: true, margin: 0.04 });
});
// ---------- diagrams
const box = (x, y, w, h, t, fill, line, o = {}) => { s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: line, width: 1 }, rectRadius: 0.06, objectName: 'box ' + t });
  s.addText(t, { x, y, w, h, fontFace: 'Calibri', fontSize: o.fs || 12, bold: !!o.bold, color: o.color || '1A1A1A', align: 'center', valign: 'middle', isTextBox: true, margin: 0.02 }); };
const arr = (x1, y1, x2, y2) => s.addShape(pres.shapes.LINE, { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.max(Math.abs(x2 - x1), 0.001), h: Math.max(Math.abs(y2 - y1), 0.001), flipV: (y2 < y1) !== (x2 < x1) && x1 !== x2 && y1 !== y2 ? true : false, line: { color: ARROW, width: 1.25, endArrowType: 'triangle' } });
const SY = [4.3, 4.82, 5.34, 5.86], SH = 0.4, CAMS = ['RGB', 'MS', 'HS', 'TIR'];
s.addText('Feature-level and input-level fusion (ML models, DNN-F1, pseudo-image networks)', { x: 0.45, y: 3.9, w: 6.0, h: 0.32, fontFace: 'Calibri', fontSize: 12, bold: true, color: PUR, isTextBox: true, margin: 0 });
s.addText('Intermediate fusion with camera attention (DNN-F2)', { x: 6.85, y: 3.9, w: 6.0, h: 0.32, fontFace: 'Calibri', fontSize: 12, bold: true, color: PUR, isTextBox: true, margin: 0 });
// left
CAMS.forEach((c, i) => box(0.45, SY[i], 0.9, SH, c, SEN, NAVY, { bold: true }));
const JX = 1.62, JY = 4.86, JW = 1.25, JH = 0.75; box(JX, JY, JW, JH, 'DSF join +\nVIF < 10', LAV, PUR);
CAMS.forEach((c, i) => arr(1.35, SY[i] + SH / 2, JX, JY + JH / 2));
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 3.15, y: 4.2, w: 3.35, h: 1.5, fill: { color: 'FBF7FD' }, line: { color: PUR, width: 0.75, dashType: 'dash' }, rectRadius: 0.06, objectName: 'model group' });
const MX = 3.23, MW = 3.19, MB = [[4.27, 0.38, 'ML: SVM/SVR · RF · k-NN · PLS-DA/PLSR', 10.5], [4.71, 0.38, 'DNN-F1 (input-level dense network)', 10.5], [5.15, 0.48, 'Pseudo-image nets: DT-EDNet, EfficientNet-B0,\nResNet18, ConvNeXt V2-Atto', 10]];
MB.forEach(([y, h, t, fs]) => { box(MX, y, MW, h, t, PUR, PUR, { color: 'FFFFFF', bold: true, fs }); arr(JX + JW, JY + JH / 2, MX, y + h / 2); });
box(3.95, 5.86, 1.9, SH, 'Tasks A, B, C (DI)', YEL, GOLD, { bold: true }); arr(4.9, 5.7, 4.9, 5.86);
// right
CAMS.forEach((c, i) => { box(6.85, SY[i], 0.85, SH, c, SEN, NAVY, { bold: true }); box(7.95, SY[i], 1.2, SH, 'branch (32)', LAV, PUR, { fs: 11 }); arr(7.7, SY[i] + SH / 2, 7.95, SY[i] + SH / 2); });
const EX = 9.45, EW = 1.3; box(EX, SY[0], EW, SY[3] + SH - SY[0], 'SE camera\nattention\n(one weight\nper camera)', LAV2, PUR, { fs: 11 });
CAMS.forEach((c, i) => arr(9.15, SY[i] + SH / 2, EX, SY[i] + SH / 2));
const KX = 11.05, KW = 1.85; box(KX, JY - 0.08, KW, JH + 0.16, 'DNN-F2\njoint layers\n(dense 32)', PUR, PUR, { color: 'FFFFFF', bold: true });
arr(EX + EW, JY + JH / 2, KX, JY + JH / 2);
box(KX + 0.05, 5.86, KW - 0.1, SH, 'Tasks A, B, C (DI)', YEL, GOLD, { bold: true }); arr(KX + KW / 2, JY + JH + 0.08, KX + KW / 2, 5.86);
// ---------- banner + footer
s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.45, y: 6.4, w: 12.43, h: 0.5, fill: { color: LAV }, line: { color: PUR, width: 1 }, rectRadius: 0.08 });
s.addText('All 15 sensor sets (4 single cameras + 11 combinations) are modelled on the 33 training plots and tested once on the 15 test plots; fusion gain = fused set − its best single camera; drop-one-camera ablation of S15 is compared with the DNN-F2 camera weights (Step 2.8).',
  { x: 0.6, y: 6.4, w: 12.15, h: 0.5, fontFace: 'Calibri', fontSize: 12, color: '1A1A1A', valign: 'middle', isTextBox: true, margin: 0 });
s.addText('Outline of research work  |  Animesh Panda (13098)  |  Agricultural Physics, ICAR-IARI', { x: 0.55, y: 7.05, w: 8.5, h: 0.3, fontFace: 'Calibri', fontSize: 10.5, color: GREY, isTextBox: true, margin: 0 });
s.slideNumber = { x: 12.3, y: 7.02, w: 0.6, h: 0.3, fontFace: 'Calibri', fontSize: 10.5, color: GREY };
s.addNotes('Four fusion routes of Objective 2. (1) Feature-level fusion: the disease-specific feature sets selected for each camera in Objective 1 are joined for each sensor set, VIF < 10 is applied again, and SVM, RF, k-NN and PLS are trained with SFFS and grid search (GroupKFold(3) by plot). (2) DNN-F1 joins all features at the input of one dense network (Maimaitijiang et al., 2020). (3) DNN-F2 gives each camera its own branch and learns one weight per camera with a squeeze-and-excitation layer before joining (intermediate fusion; Maimaitijiang et al., 2020; Deng et al., 2024). (4) The fused features are arranged as a pseudo-image for DT-EDNet and its comparison networks (Ma et al., 2026). All 15 sensor sets are compared on the same split; the fusion gain is the improvement over the best single camera.');
pres.writeFile({ fileName: OUT }).then(() => console.log('written', OUT));
