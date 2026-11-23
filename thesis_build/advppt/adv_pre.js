// Activity 1.8: characterisation of the pre-symptomatic stage (576 pre-symptomatic subplot samples per camera)
module.exports = function () {
const { pres, C, S, T, BL, box, arr, chain, tb, refline } = require('./adv_lib.js');
const s = S('Activity 1.8: Characterisation of the pre-symptomatic stage', 'Objective 1',
  'The same characterisation is repeated before symptoms appear, with 576 pre-symptomatic subplot samples per camera (3 flights × 192 subplots). Because no grade exists yet, the target is later-infected vs healthy: the label of an inoculated subplot is taken back from its later status. The result is a pre-symptomatic feature set of each camera, which feeds the prediction models of Objective 3.');
box(s, 0.45, 1.2, 6.6, 2.05, 'Samples and labels (per camera)', ['**576 samples** = 3 flights (1, 4, 7 Jan 2027; 2, 5, 8 days after inoculation) × 192 subplots',
  '**Healthy:** 144 subplots of the 12 healthy plots (12 × 4 × 3)', '**Later-infected:** inoculated subplots (up to 432 = 36 × 4 × 3) that show pustules on a later flight; those that never show symptoms are excluded',
  '**Physiology:** 11 parameters on 7 Jan (Step A8)'], C.red, C.lred, { valign: 'top', align: 'left', fs: 13 });
tb(s, [['Flight', 'DAI', 'Healthy', 'Inoculated', 'Total'], ['1 Jan 2027', '2', '48', '144', '192'], ['4 Jan 2027', '5', '48', '144', '192'], ['7 Jan 2027', '8', '48', '144', '192'], ['Total', '', '144', '432', '576']],
  7.3, 1.2, 5.58, [1.5, 0.75, 1.05, 1.28, 1.0], { fs: 13, firstCol: true, head: C.red });
chain(s, [{ h: '1.8.1 Response', b: 'mean spectra, FD, thermal and texture of later-infected vs healthy per date; % difference from healthy' },
  { h: '1.8.2 Univariate tests', b: 'plot means (unit = plot); Welch t-test or Mann–Whitney; Hedges g; Benjamini–Hochberg FDR 5%' },
  { h: '1.8.3 Wavelengths', b: 'NDSI/RSI maps and SHAP-CARS with the binary label, inside training folds' },
  { h: '1.8.4 Indices, texture, thermal', b: 'healthy-plot normalisation (E2); ReliefF (binary); mRMR; CTD, NRCT, CWSI' },
  { h: '1.8.5 Earliest response', b: 'change of each feature over 2, 5, 8 DAI by variety and timing' }], 0.45, 3.45, 12.43, 1.85, 0.22, C.red, 'FFFFFF', { fs: 13 });
BL(s, ['**Same rules as the post-symptomatic stage:** one selection method per feature type; label-based steps only in the training part; 48 published indices + red-edge parameters, texture and thermal features of all four cameras.',
  '**Output:** pre-symptomatic feature set of each camera and the earliest-responding features (wavelength, index, texture, temperature) → Objective 3 (prediction) and Step 3.1.2 (physiology before symptoms).'], 0.45, 5.4, 12.43, 1.05, { lead: C.red, ps: 2 });
refline(s, 'Zarco-Tejada et al. (2018); Calderón et al. (2013); Mahlein et al. (2019); Terentev et al. (2023); Sullivan and Feinn (2012); Benjamini and Hochberg (1995).', 6.45, 0.6);
};
