// Steps D5–D6: multispectral vegetation indices (12) and GLCM texture features (8 measures) – one slide
module.exports = function () {
const { F, C, S, T } = require('./adv_lib.js');
const SR = require('./idx_short_refs.json');
const MS = [['CIrededge', 'NIR/RE − 1', 'Gitelson et al. (2003)'], ['CIgreen', 'NIR/G − 1', 'Gitelson et al. (2003)'], ['TCARI', '3[(RE − R) − 0.2(RE − G)(RE/R)]', 'Haboudane et al. (2002)'],
  ['NDRE', '(NIR − RE)/(NIR + RE)', 'Gitelson and Merzlyak (1994)'], ['PSRI', '(R − G)/NIR', 'Merzlyak et al. (1999); Liu et al. (2024)'], ['NDVI', '(NIR − R)/(NIR + R)', 'Rouse et al. (1974)'],
  ['SAVI', '1.5(NIR − R)/(NIR + R + 0.5)', 'Huete (1988)'], ['MCARI', '[(RE − R) − 0.2(RE − G)](RE/R)', 'Daughtry et al. (2000)'], ['MTCI', '(NIR − RE)/(RE − R)', 'Dash and Curran (2004)'],
  ['GNDVI', '(NIR − G)/(NIR + G)', 'Gitelson et al. (1996)'], ['OSAVI', '1.16(NIR − R)/(NIR + R + 0.16)', 'Rondeaux et al. (1996)'], ['MSR', '(NIR/R − 1)/√(NIR/R + 1)', 'Chen (1996)']];
const GL = [['Mean (MEA)', 'ΣΣ i P(i,j)', 'average grey level'], ['Variance (VAR)', 'ΣΣ (i − μ)² P(i,j)', 'spread of grey levels'], ['Homogeneity (HOM)', 'ΣΣ P(i,j) / [1 + (i − j)²]', 'smoothness of the texture'],
  ['Contrast (CON)', 'ΣΣ (i − j)² P(i,j)', 'local grey-level variation'], ['Dissimilarity (DIS)', 'ΣΣ |i − j| P(i,j)', 'as contrast, linear weight'], ['Entropy (ENT)', '−ΣΣ P(i,j) log P(i,j)', 'disorder of the pattern'],
  ['Second moment (SEM)', 'ΣΣ P(i,j)²', 'uniformity (energy)'], ['Correlation (COR)', 'ΣΣ (i − μi)(j − μj) P(i,j) / (σi σj)', 'linear dependence of neighbours']];
function table(s, head, rows, x, y, w, cw, hc) {
  const hdr = head.map(t => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: hc }, align: 'center', valign: 'middle' } }));
  const body = rows.map((r, i) => r.map((c, j) => ({ text: c, options: { fill: { color: i % 2 ? 'FFFFFF' : 'F5F8F2' }, bold: j === 0, italic: j === 2 && hc === C.g } })));
  s.addTable([hdr, ...body], { x, y, w, colW: cw, fontFace: F, fontSize: 12, color: C.dk, border: { type: 'solid', pt: 0.5, color: 'B9C6B2' }, margin: [0.02, 0.05, 0.02, 0.05], autoPage: false, valign: 'middle' });
}
const s = S('Steps D5–D6: Multispectral indices and GLCM texture', 'Data processing',
  'Twelve published multispectral indices are computed from the five MicaSense bands of every subplot; texture is computed from the grey-level co-occurrence matrix (GLCM) of the RGB (and multispectral, hyperspectral principal-component and thermal) images with eight Haralick measures.');
T(s, '**Multispectral indices (B, G, R, RE, NIR = 475, 560, 668, 717, 840 nm)**', 0.45, 1.12, 6.4, 0.32, { fontSize: 13, color: C.g });
table(s, ['Index', 'Formula', 'Original reference'], MS, 0.45, 1.45, 6.4, [1.15, 2.85, 2.4], C.g);
T(s, '**GLCM texture features (RGB image; Haralick et al., 1973)**', 7.05, 1.12, 5.83, 0.32, { fontSize: 13, color: C.blue });
table(s, ['Texture', 'Equation', 'Meaning'], GL, 7.05, 1.45, 5.83, [1.75, 2.3, 1.78], C.blue);
T(s, [{ text: 'Note: ', options: { bold: true, color: C.blue } }, { text: 'i, j = grey levels (row and column of the GLCM); P(i,j) = normalised frequency of two neighbouring pixels with grey levels i and j; μ, σ = mean and SD of the GLCM margins; 32 grey levels, 3 × 3 window, distance 1, four directions averaged (Hall-Beyer, 2017).' }],
  7.05, 4.55, 5.83, 0.95, { fontSize: 12 });
T(s, [{ text: 'Use in UAV disease studies: ', options: { bold: true, color: C.g } }, { text: 'multispectral indices and GLCM texture for wheat powdery mildew (Feng et al., 2022) and wheat Fusarium head blight (Liu et al., 2024).', options: { italic: true } }], 0.45, 5.62, 12.43, 0.32, { fontSize: 12 });
const keys = ['Gitelson, A.A., Gritz|2003', 'Haboudane, D., Miller, J.R., Tremblay|2002', 'Gitelson, A., Merzlyak|1994', 'Merzlyak|1999', 'Liu, Y., Liu, G|2024', 'Rouse|1974', 'Huete|1988', 'Daughtry|2000', 'Dash|2004',
  'Gitelson, A.A., Kaufman, Y.J., Merzlyak|1996', 'Rondeaux|1996', 'Chen, J.M.|1996', 'Haralick|1973', 'Hall-Beyer|2017', 'Feng, Z., Song|2022'];
T(s, [{ text: 'References: ', options: { bold: true, color: C.g } }, { text: keys.map(k => SR[k]).join('; ') + '.' }], 0.45, 5.95, 12.43, 1.07, { fontSize: 9, color: '3A3A3A' });
};
