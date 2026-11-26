// Two slides (Step D4): the 48 published hyperspectral indices (39 base + 9 SWIR) and the 3 red-edge parameters, with formulas,
// original references and recent (2006-2026) disease-sensing studies that used these index groups. Full references in a strip at the bottom.
module.exports = function () {
const { pres, F, FS, C, S, T } = require('./adv_lib.js');
const SR = require('./idx_short_refs.json');
const sr = k => SR[k] || (() => { throw new Error('missing ref ' + k); })();
// [index, formula, reference] ; group rows: ['#Group title']
const P1L = [['#Greenness and canopy structure (17)'],
  ['NDVI780', '(R780 − R670)/(R780 + R670)', 'Raun et al. (2001)'], ['NDVI850', '(R850 − R650)/(R850 + R650)', 'Raun et al. (2001)'], ['NDVI761', '(R761 − R651)/(R761 + R651)', 'Raun et al. (2001)'],
  ['SR900', 'R900/R680', 'Jordan (1969)'], ['SR850', 'R850/R680', 'Jordan (1969)'], ['SR761', 'R761/R651', 'Jordan (1969)'],
  ['GNDVI', '(R850 − R550)/(R850 + R550)', 'Gitelson et al. (1996)'], ['RDVI', '(R800 − R670)/√(R800 + R670)', 'Roujean and Bréon (1995)'],
  ['MSR', '(R800/R670 − 1)/√(R800/R670 + 1)', 'Chen (1996)'], ['TVI', '0.5[120(R750 − R550) − 200(R670 − R550)]', 'Broge and Leblanc (2001)'],
  ['MTVI1', '1.2[1.2(R800 − R550) − 2.5(R670 − R550)]', 'Haboudane et al. (2004)'],
  ['MTVI2', '1.5[1.2(R800 − R550) − 2.5(R670 − R550)] / √[(2R800 + 1)² − (6R800 − 5√R670) − 0.5]', 'Haboudane et al. (2004)'],
  ['MCARI1', '1.2[2.5(R800 − R670) − 1.3(R800 − R550)]', 'Haboudane et al. (2004)']];
const P1R = [['TCARI', '3[(R700 − R670) − 0.2(R700 − R550)(R700/R670)]', 'Haboudane et al. (2002)'], ['VIgreen', '(R550 − R670)/(R550 + R670)', 'Gitelson et al. (2002)'],
  ['GI', 'R554/R677', 'Guo et al. (2021)'], ['RR', '1/R700', 'Mustafa et al. (2023)'],
  ['#Red-edge parameters, 680–760 nm (3)'],
  ['REP', 'wavelength of maximum first derivative (FD)', 'Horler et al. (1983); Cho and Skidmore (2006)'], ['Dr', 'maximum FD (red-edge amplitude)', 'Filella and Peñuelas (1994)'], ['SDr', 'sum of FD over 680–760 nm (area)', 'Filella and Peñuelas (1994)'],
  ['#Pigment ratios (12; continued)'],
  ['PSSRa', 'R800/R680', 'Blackburn (1998)'], ['PSSRb', 'R800/R635', 'Blackburn (1998)'], ['PSSRc', 'R800/R470', 'Blackburn (1998)'],
  ['RARSa', 'R675/R700', 'Chappelle et al. (1992)'], ['RARSb', 'R675/(R700 × R650)', 'Chappelle et al. (1992)'], ['RARSc', 'R760/R500', 'Chappelle et al. (1992)']];
const P2L = [['#Pigment ratios (continued)'],
  ['SIPI', '(R800 − R445)/(R800 − R680)', 'Peñuelas et al. (1995)'], ['NPCI', '(R680 − R430)/(R680 + R430)', 'Peñuelas et al. (1994)'], ['PSRI', '(R680 − R500)/R750', 'Merzlyak et al. (1999)'],
  ['ARI', '1/R550 − 1/R700', 'Gitelson et al. (2001)'], ['PPR', '(R550 − R450)/(R550 + R450)', 'Metternicht (2003)'], ['NRI', '(R570 − R670)/(R570 + R670)', 'Bausch and Duke (1996)'],
  ['#Photosynthesis and stress (4)'],
  ['PRI', '(R531 − R570)/(R531 + R570)', 'Gamon et al. (1992)'], ['NPQI', '(R415 − R435)/(R415 + R435)', 'Barnes et al. (1992)'], ['RVSI', '(R712 + R752)/2 − R732', 'Merton and Huntington (1999)'],
  ['HI', '(R534 − R698)/(R534 + R698) − 0.5 R704', 'Mahlein et al. (2013)'],
  ['#Water (3)'],
  ['WI', 'R900/R970', 'Peñuelas et al. (1997)'], ['WI/NDVI', '(R900/R970)/NDVI', 'Peñuelas et al. (1997)'], ['NWI-2', '(R970 − R850)/(R970 + R850)', 'Babar et al. (2006)']];
const P2R = [['#SWIR disease–water (3 base + 9 SWIR)'],
  ['DWSI-1', 'R800/R1660', 'Apan et al. (2004)'], ['DWSI-2*', 'R1660/R550', 'Apan et al. (2004)'], ['DWSI-3*', 'R1660/R680', 'Apan et al. (2004)'], ['DWSI-4', 'R550/R680', 'Apan et al. (2004)'],
  ['DWSI-5*', '(R800 + R550)/(R1660 + R680)', 'Apan et al. (2004)'], ['ROTI', 'R1175/(R1982 + R691)', 'Bhattacharya and Chattopadhyay (2013)'],
  ['NDWI*', '(R860 − R1240)/(R860 + R1240)', 'Gao (1996)'], ['MSI*', 'R1600/R820', 'Hunt and Rock (1989)'], ['NDII*', '(R819 − R1649)/(R819 + R1649)', 'Hardisky et al. (1983)'],
  ['RBI_M*', 'R1148/R1301', 'Mandal et al. (2023)'], ['NDBI*', '(R1148 − R1301)/(R1148 + R1301)', 'Mandal et al. (2023)'], ['RBI_R*', 'R1068/R1560', 'Ramalingam et al. (2026)']];
function itable(s, rows, x, y, w) {
  const cw = [0.95, w - 0.95 - 2.05, 2.05];
  const hdr = ['Index', 'Formula (R = reflectance at the wavelength in nm)', 'Original reference'].map(t => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: C.g }, align: 'center', valign: 'middle' } }));
  const body = []; let k = 0;
  rows.forEach(r => {
    if (r[0].startsWith('#')) { body.push([{ text: r[0].slice(1), options: { colspan: 3, bold: true, color: C.g, fill: { color: 'E4ECDD' } } }]); k = 0; return; }
    const fill = k++ % 2 ? 'FFFFFF' : 'F5F8F2';
    body.push([{ text: r[0], options: { bold: true, fill: { color: fill } } }, { text: r[1], options: { fill: { color: fill } } }, { text: r[2], options: { fill: { color: fill }, italic: true } }]);
  });
  s.addTable([hdr, ...body], { x, y, w, colW: cw, fontFace: F, fontSize: 12, color: C.dk, border: { type: 'solid', pt: 0.5, color: 'B9C6B2' }, margin: [0.02, 0.05, 0.02, 0.05], autoPage: false, valign: 'middle' });
}
function strip(s, recent, keys, y, hr = 0.32) {
  T(s, [{ text: 'Recent disease-sensing studies using these index groups (2006–2026): ', options: { bold: true, color: C.g } }, { text: recent, options: { italic: true } }], 0.45, y, 12.43, hr, { fontSize: 12 });
  const txt = keys.map(sr).join('; ') + '.';
  T(s, [{ text: 'References: ', options: { bold: true, color: C.g } }, { text: txt }], 0.45, y + hr, 12.43, 7.02 - y - hr, { fontSize: 9, color: '3A3A3A' });
}
let s = S('Step C2: Published vegetation indices and red-edge parameters (1/2)', 'Data processing',
  '48 published hyperspectral indices (39 base indices of the methodology + 9 SWIR disease indices) and 3 red-edge parameters are computed from every subplot spectrum. This slide: greenness and canopy structure, red-edge parameters and the first pigment ratios. Each index keeps its original reference; recent disease-sensing studies that used these index groups are listed below the tables.');
itable(s, P1L, 0.45, 1.15, 6.1); itable(s, P1R, 6.78, 1.15, 6.1);
strip(s, 'Zhang et al. (2012b); Mahlein et al. (2013); Ashourloo et al. (2014); Guo et al. (2021); Mustafa et al. (2023).',
  ['Raun|2001', 'Jordan|1969', 'Gitelson, A.A., Kaufman, Y.J., Merzlyak|1996', 'Roujean|1995', 'Chen, J.M.|1996', 'Broge|2001', 'Haboudane, D., Miller, J.R., Pattey|2004', 'Haboudane, D., Miller, J.R., Tremblay|2002',
   'Gitelson, A.A., Kaufman, Y.J., Stark|2002', 'Guo, A|2021', 'Mustafa|2023', 'Horler|1983', 'CHO', 'Filella|1994', 'Blackburn|1998', 'Chappelle|1992', 'Zhang, J., Pu, R., Huang|2012', 'Mahlein, A.-K., Rumpf|2013', 'Ashourloo, D., Mobasheri|2014'], 5.72);
s = S('Step C2: Published vegetation indices and red-edge parameters (2/2)', 'Data processing',
  'Remaining pigment ratios, photosynthesis/stress, water and SWIR disease–water indices. The nine SWIR disease indices added to the 39 base indices are marked with an asterisk. Indices that need bands removed in quality control (water-vapour regions) are computed only if the band passes the noise check.');
itable(s, P2L, 0.45, 1.15, 6.1); itable(s, P2R, 6.78, 1.15, 6.1);
T(s, '* the 9 SWIR disease indices added to the 39 base indices → 48 published indices; data-driven indices (NDSI, RSI, White Rust Index) are built in Activity 1.3.', 6.78, 4.75, 6.1, 0.55, { fontSize: 12, italic: true, color: C.g });
strip(s, 'Mahlein et al. (2013); Bhattacharya and Chattopadhyay (2013); Zarco-Tejada et al. (2018); Yu et al. (2018); Mandal et al. (2023); Ramalingam et al. (2026).',
  ['Peñuelas, J., Baret|1995', 'Peñuelas, J., Gamon|1994', 'Merzlyak|1999', 'Gitelson, A.A., Merzlyak, M.N., Chivkunova|2001', 'Metternicht|2003', 'Bausch|1996', 'Gamon|1992', 'Barnes, J.D.|1992', 'Merton|1999', 'Mahlein, A.-K., Rumpf|2013',
   'Peñuelas, J., Piñol|1997', 'Babar|2006', 'Apan|2004', 'Bhattacharya|2013', 'Gao|1996', 'Hunt|1989', 'Hardisky|1983', 'Mandal, N., Adak|2023', 'Ramalingam|2026', 'Zarco|2018', 'Yu, K|2018'], 5.4, 0.55);
};
