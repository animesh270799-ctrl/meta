// Slide: Activity F validation design – nested leave-one-replication-out split (used in the full deck and as a one-slide file)
module.exports = function () {
const { pres, F, FS, C, S, T, BL, box, arr, refline } = require('./adv_lib.js');
let s;
s = S('Activity F: Validation design (LORO and nested tuning)', 'Data processing',
  'How the data are split. The unit that moves between training and test is the plot with its four subplots and all dates. Outer loop: each fold tests one replication (12 inoculated plots) plus four rotated healthy plots and trains on the other 32 plots. Inner loop: inside the 32 training plots, three folds grouped by plot run every label-based step and choose features and hyper-parameters; the model is retrained on all 32 plots and predicts the test replication once. After three folds every sample is predicted once.');
// ---- outer loop grid
T(s, '**1. Outer loop – leave one replication out (3 folds)**', 0.45, 1.1, 7.5, 0.35, { color: C.blue });
const cx = [0.45, 1.45, 2.75, 4.05, 5.35], cw = [0.95, 1.25, 1.25, 1.25, 2.6];
const hd = ['Fold', 'R1 (plots 37–48)', 'R2 (plots 25–36)', 'R3 (plots 13–24)', 'Healthy block (plots 1–12)'];
hd.forEach((h, j) => box(s, cx[j], 1.5, cw[j], 0.62, null, h, C.grey, C.lgrey));
const hrot = ['7, 2, 10, 12', '5, 8, 4, 1', '3, 9, 11, 6'];
for (let i = 0; i < 3; i++) {
  const y = 2.2 + i * 0.62;
  box(s, cx[0], y, cw[0], 0.54, null, '**Fold ' + (i + 1) + '**', C.grey, 'FFFFFF');
  for (let j = 0; j < 3; j++) { const test = i === j; box(s, cx[j + 1], y, cw[j + 1], 0.54, null, test ? '**TEST**' : 'train', test ? C.red : C.g, test ? C.lred : C.lt); }
  box(s, cx[4], y, cw[4], 0.54, null, '**test ' + hrot[i] + '**; train other 8', C.gold, C.lgold);
}
T(s, 'Per fold (post-symptomatic): test 16 plots × 4 subplots × 10 dates = **640**; train 32 plots = **1280** samples (pre-symptomatic: 192 / 384).', 0.45, 4.1, 7.5, 0.6);
// ---- arrow to inner loop
arr(s, 2.1, 4.68, 2.1, 5.02, C.blue, 1.75);
T(s, '**2. Inner loop – inside the 32 training plots (3 folds grouped by plot)**', 2.25, 4.68, 5.7, 0.35, { color: C.blue });
const ix = [0.45, 1.2, 1.95, 2.7], iw = [0.7, 0.7, 0.7, 0.7];
['', 'A', 'B', 'C'].forEach((h, j) => { if (j) box(s, ix[j], 5.08, iw[j], 0.34, null, h, C.grey, C.lgrey); });
for (let i = 0; i < 3; i++) { const y = 5.46 + i * 0.4; T(s, 'In ' + (i + 1), ix[0], y, iw[0], 0.36, { valign: 'middle' });
  for (let j = 0; j < 3; j++) { const v = i === j; box(s, ix[j + 1], y, iw[j + 1], 0.36, null, v ? 'val' : 'train', v ? C.purple : C.g, v ? C.lpurple : C.lt); } }
arr(s, 3.45, 5.95, 3.7, 5.95);
box(s, 3.72, 5.08, 2.3, 1.68, 'Label-based steps here', 'index search, SHAP-CARS, ReliefF, mRMR, TTFI, SFFS, grid search, early stopping', C.purple, C.lpurple);
arr(s, 6.04, 5.95, 6.24, 5.95);
box(s, 6.26, 5.08, 1.69, 1.68, 'Then', 'best mean inner score → retrain on all 32 plots → predict test fold once', C.red, C.lred);
// ---- rules panel
box(s, 8.15, 1.1, 4.73, 5.66, null, null, C.g, 'FBFCF9');
T(s, '**Rules of the split**', 8.3, 1.18, 4.45, 0.35, { color: C.g });
BL(s, ['**Unit = plot:** its 4 subplots and all dates stay in the same fold (no plot is seen in both training and test).',
  '**Healthy plots rotated:** each test fold has every sowing timing once and every variety; each training part keeps 2–3 healthy plots per variety (E2).',
  '**Inner folds:** the 32 training plots form 3 groups (A, B, C ≈ 10–11 plots); each group is the validation part once.',
  '**Same 3 folds** for all 15 sensor sets, models and tasks; every sample is predicted once → pooled metrics, mean ± SD over folds.',
  '**Leakage checklist:** features once on all data (no labels); means, SDs, healthy references and class weights from the training part; label-based steps in inner folds; Bharatpur only with frozen models.',
  '**Why not a random split:** subplots and dates of one plot are correlated; random splits inflate accuracy.'], 8.25, 1.55, 4.55, 5.15, { ps: 5 });
refline(s, 'Roberts et al. (2017); Varma and Simon (2006); Cawley and Talbot (2010); Ambroise and McLachlan (2002); Oerke et al. (2006).', 6.82, 0.3);
};
