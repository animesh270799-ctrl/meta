// Research paper (Word) - leaf-level white rust analysis following Ma et al. (2026)
const L = require('../ijam_doc/lib');
const { D, add, H1, H2, P, B, NL, EQ, T, BOX, FIG, Paragraph, TextRun, TEAL, DARK, GREY, body } = L;
const { AlignmentType, LevelFormat, Header, Footer, PageNumber } = D;
const J = require(process.argv[2]); const FG = process.argv[3];
const f = (v, d = 1) => (v === null || v === undefined) ? '–' : Number(v).toFixed(d);
const sum = a => a.reduce((x, y) => x + y, 0);
const LN = J.level_names, bi = J.internal.best, be = J.external.best, es = J.ext_same_model;
const tot = [0, 1, 2, 3, 4].map(l => sum(J.counts.levels[l])), trn = [0, 1, 2, 3, 4].map(l => sum(J.counts.levels[l].slice(0, 3)));
const N = sum(tot);
const si = s => J.sets.indexOf(s);
const bestOf = (key, set) => J.models.map(m => [m, J[key].OA[m][si(set)], J[key].F1[m][si(set)]]).sort((a, b) => b[1] - a[1])[0];
const singles = ['RFE-RF', 'SAND', 'CARS-PLS', 'VIs (Relief top 5)'];
const bestSingle = singles.map(s => [s, ...bestOf('internal', s)]).sort((a, b) => b[2] - a[2])[0];
const fused = ['OWs+VIs', ...bestOf('internal', 'OWs+VIs')], full = ['Full wavelength (350-2500 nm)', ...bestOf('internal', 'Full wavelength (350-2500 nm)')];
const viS = J.vi.slice().sort((a, b) => Math.abs(b[2]) - Math.abs(a[2])), viTop = J.vi.filter(r => r[4] === 'Yes').map(r => r[0]);
const z = J.mean_zoom, iw = w => z.wl.indexOf(w), sv = (l, w) => z.series[LN[l]][iw(w)];
const maxR2 = Math.max(J.ndsi_best[2], J.rsi_best[2]);
const sd = J.internal.fold_sd[bi.input + '|' + bi.model];

add(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 200, after: 200 }, children: [new TextRun({ text: 'Leaf-level classification of white rust (Albugo candida) severity in Indian mustard from ASD contact-probe reflectance using the multi-feature workflow of Ma et al. (2026)', bold: true, size: 32, color: DARK })] }));
add(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [new TextRun({ text: 'Animesh Panda', size: 22 })] }));
add(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: 'ICAR-Indian Agricultural Research Institute, New Delhi – MuDAS-AI project', size: 20, italics: true, color: GREY })] }));
add(...BOX('Abstract', [
  `Ma et al. (2026) proposed a multi-feature workflow for early detection of rice blast from UAV hyperspectral images, combining two-band spectral indices, optimal wavelengths selected by three methods, vegetation indices, texture features and a dual-transformer classifier. This study applies the same workflow to leaf-level ASD contact-probe spectra of Indian mustard affected by white rust. Spectra (350–2500 nm, whole range including the water-absorption regions) of ${N.toLocaleString()} leaves were collected on four dates (11 Feb – 13 Mar 2026) from 48 plots (36 inoculated, 12 healthy; three varieties). Each leaf’s visual score (0, 1, 3, 5, 7, 9) was grouped into five levels (L0–L4). Texture features and the texture index (TTFI) of the paper were not used because contact-probe data are non-imaging. NDSI and RSI maps defined effective ranges (${J.effective.ranges.join(', ')} nm), from which RFE with random forest, SAND (sigmoid feature weights, threshold 0.524) and CARS-PLS selected ${J.bands.rfe.length}, ${J.bands.sand.length} and ${J.bands.cars.length} bands. Seventeen vegetation indices were ranked by Relief. Random forest, SVM, PLS-DA and a multilayer perceptron were compared on single inputs, a full-wavelength baseline and the fused OWs + VIs input, using five-fold cross-validation grouped by plot on three dates (all selection inside folds) and an independent later date. The best two-band index reached R² = ${maxR2}. In cross-validation the best result was ${bi.input} with ${bi.model} (OA ${f(bi.OA)}%, Cohen’s kappa ${f(bi.Kappa)}%, quadratic-weighted kappa ${f(bi.QWK)}%, macro F1 ${f(bi.F1)}%); as in the paper, fusion of wavelengths and indices was best. On the independent date (pod formation) the best OA was ${f(be.OA)}% with kappa near zero, showing that the models did not transfer to a later growth stage. Leaf spectra thus carry a moderate white rust signal, but five-level grading of single leaves remains difficult.`]));
add(P('**Keywords:** white rust; Albugo candida; Brassica juncea; ASD FieldSpec; contact probe; leaf reflectance; NDSI; band selection; CARS; SAND; Relief; vegetation indices'));

add(H1('1. Introduction', false));
add(P('White rust, caused by the oomycete *Albugo candida*, is a major disease of Indian mustard (*Brassica juncea*). White pustules develop mainly on the lower leaf surface, with chlorotic areas on the upper surface, and systemic infection can deform the inflorescence. Visual scoring is slow and subjective, so spectral methods are of interest for breeding and disease management.'));
add(P('Ma et al. (2026) developed a workflow for early detection of rice blast from UAV hyperspectral images. Canopy disease was graded into five levels; spectra were smoothed; normalised-difference (NDSI) and ratio (RSI) spectral indices were searched over all band pairs to define effective wavelength ranges; optimal wavelengths were selected by RFE-SHAP, SAND and SHAP-CARS; 16 vegetation indices were ranked by Relief; texture features from the grey-level co-occurrence matrix were ranked by mRMR and combined into a tri-band texture index (TTFI); and a dual-transformer network (DT-EDNet) was compared with three CNNs using single and fused inputs, with an independent test in a second year.'));
add(P('Leaf-level measurements remove the mixing of leaves with soil, shadow and flowers that complicates canopy images, so they are a useful first test of such a workflow for white rust. The objectives were: (i) to describe the leaf spectral response to white rust severity over 350–2500 nm; (ii) to identify sensitive band pairs, optimal wavelengths and vegetation indices following Ma et al. (2026); (iii) to compare four classifiers on single and fused inputs; and (iv) to test transfer of the models to an independent later date. Because a contact probe records a single spot without an image, the texture-based steps of the paper were omitted.'));

add(H1('2. Materials and methods', false));
add(H2('2.1 Experiment and measurements'));
add(P(`The experiment comprised 48 plots of three varieties (V1–V3); 36 plots were inoculated with *A. candida* and 12 were left healthy. Leaf reflectance was measured with an ASD FieldSpec spectroradiometer and contact probe (350–2500 nm, 1-nm output) on 11 Feb, 24 Feb, 3 Mar and 13 Mar 2026 (vegetative to pod-formation stages). On most dates, five plants per plot were sampled at three leaf positions (L3, L5 and the lowest leaf, LL); each leaf gave one spectrum and was scored on the 0–9 white rust scale (Table 1).`));
add(...T('Table 1. Leaf spectra per date (75 duplicated spectra on 13 Mar removed)', [['Date', 'Leaves', 'Plots', 'Growth stage(s)', 'Role'], ...J.inventory.map(r => r.map(String))], [1.1, 0.8, 0.7, 2.4, 1.6], { center: true }));
add(H2('2.2 Severity levels'));
add(P('The analysis unit was the individual leaf and the label was the leaf’s own score. Following the five levels of the paper (Tables II–III), scores were grouped as L0 = 0 (healthy), L1 = 1 (mild), L2 = 3 (moderate), L3 = 5 (severe) and L4 = 7 or 9 (very severe; merged because score 9 was rare). Leaves from inoculated plots without pustules were labelled L0. Table 2 gives the sample numbers (paper Table IV).'));
add(...T('Table 2. Leaves per severity level in the training and independent-test dates', [['Level', 'Training (11 Feb, 24 Feb, 3 Mar)', 'Independent test (13 Mar)', 'Total'],
  ...LN.map((n, l) => [n, String(trn[l]), String(J.counts.levels[l][3]), String(tot[l])]), ['Total', String(sum(trn)), String(sum(J.counts.levels.map(v => v[3]))), String(N)]], [2.4, 2, 1.8, 1], { center: true }));
add(...FIG(FG + '/fig_counts.jpg', 'Figure 1. Leaves per severity level and date.', 4.6));
add(H2('2.3 Pre-processing'));
add(P(`Exact duplicate spectra (75 on 13 Mar) were removed, leaving ${N.toLocaleString()} leaves. All reflectance values were between 0 and 1. Detector steps at 1000 and 1800 nm were corrected by matching the VNIR and SWIR2 segments to SWIR1, and spectra were smoothed with a Savitzky–Golay filter (window 11 nm, second order; Savitzky and Golay, 1964), as in the paper. The whole range of 350–2500 nm was retained: the contact probe has its own light source, so the 1450- and 1940-nm features represent leaf water absorption rather than atmospheric noise. For index search, selection and modelling, reflectance was averaged into ${J.n_bins} bands of 10 nm (centres 355–2495 nm).`));
add(H2('2.4 NDSI, RSI and effective ranges'));
add(P('As in the paper, all two-band combinations (20-nm grid) were tested:'));
add(EQ('NDSI = (R₁ − R₂) / (R₁ + R₂)        RSI = R₁ / R₂'));
add(P(`The coefficient of determination (R²) with leaf score was mapped for each pair (training dates only). The paper defined effective wavelength ranges as those with R² > 0.5. Because the maximum R² in the leaf data was ${maxR2}, the effective ranges were defined here as the bands appearing in any NDSI or RSI pair with R² ≥ ${J.r2_threshold} (|r| ≥ 0.5).`));
add(H2('2.5 Optimal wavelength selection'));
add(P('Three selectors were applied to the effective-range bands, mirroring the paper while avoiding SHAP: (i) **RFE-RF** – recursive feature elimination with a random forest (Guyon et al., 2002; Breiman, 2001), keeping 10 bands as RFE-SHAP did; (ii) **SAND** – exactly as described in the paper, a learnable logit per band is mapped to a weight in [0, 1] by a sigmoid, the weighted bands feed a softmax classifier, the loss is cross-entropy plus a sparsity penalty on the mean weight, and bands with weight > 0.524 are kept; (iii) **CARS-PLS** – competitive adaptive reweighted sampling (Li et al., 2009) with PLS regression on the severity level, 50 Monte Carlo runs and plot-grouped five-fold RMSECV, as in SHAP-CARS but without the SHAP pre-screen. As in the paper, the CARS bands were used as the optimal wavelengths (OWs) in the fused input.'));
add(H2('2.6 Vegetation indices'));
add(P('The 16 vegetation indices of the paper (Table V) and PSRI (listed in the paper’s Table VIII) were calculated. RVSI and EVI were computed in their original published forms because the formulas printed in the paper differ from the sources; MCARI was computed in the paper’s 705/750-nm form. Pearson correlations with leaf score were calculated (Table VIII analogue), and indices were ranked with Relief (k = 10; Robnik-Šikonja and Kononenko, 2003); the top five formed the VI input, as in the paper.'));
add(H2('2.7 Texture features'));
add(P('The paper’s GLCM texture features, mRMR texture selection and TTFI require an image. Contact-probe spectra are non-imaging, so these steps were not applied.'));
add(H2('2.8 Classifiers and inputs'));
add(P('The paper compared DT-EDNet with EfficientNet, ResNet18 and ConvNeXt V2. With 1,616 training leaves and short feature vectors, four standard classifiers were used instead: random forest (500 trees; Breiman, 2001), SVM with RBF kernel (Cortes and Vapnik, 1995; C and γ tuned by plot-grouped inner cross-validation), PLS-DA (Wold et al., 2001; latent variables tuned by inner cross-validation) and a multilayer perceptron (64 and 32 hidden units, early stopping). Class weights were balanced where supported. Inputs followed the paper: single inputs (RFE-RF, SAND, CARS-PLS, VIs), a full-wavelength baseline (all 215 bands; the paper’s full-wavelength dataset) and the fused input OWs + VIs. Analyses used scikit-learn (Pedregosa et al., 2011).'));
add(H2('2.9 Validation and metrics'));
add(P('**Internal validation:** the three training dates (1,616 leaves) were split into five folds grouped by plot and stratified by treatment, so that leaves of one plot were never in both training and test parts (Roberts et al., 2017). The NDSI/RSI maps, effective ranges, band selection, Relief and tuning were repeated inside every training fold (Varma and Simon, 2006). **Independent validation:** all steps were fitted on the three training dates and applied unchanged to the 648 leaves of 13 Mar, analogous to the paper’s independent 2024 dataset. Metrics followed the paper (Eq. 7–11): overall accuracy (OA), Cohen’s kappa (Cohen, 1960), macro recall and macro and per-level F1; quadratic-weighted kappa, which gives partial credit for near-misses between ordered levels, and confusion matrices were added.'));
add(...FIG(FG + '/fig_workflow.jpg', 'Figure 2. Workflow of this study, following Ma et al. (2026) without texture features.', 4.8, 5.9));

add(H1('3. Results', false));
add(H2('3.1 Spectral curves'));
add(P(`Mean spectra differed by severity (Figure 3). At 550 nm reflectance was ${f(sv(0, 550), 3)} for L0 and ${f(sv(4, 550), 3)} for L4; at 680 nm ${f(sv(0, 680), 3)} and ${f(sv(4, 680), 3)}; and at 850 nm ${f(sv(0, 850), 3)} and ${f(sv(4, 850), 3)}. Visible and SWIR reflectance increased and NIR reflectance decreased with severity. The curves of L0 and L1 were almost identical, and the standard deviations within each level were large compared with the differences between levels.`));
add(...FIG(FG + '/fig_mean_spectra.jpg', 'Figure 3. Mean leaf reflectance by severity level: (a) whole range 350–2500 nm; (b) 450–1000 nm with ± 1 SD (paper Fig. 6 analogue).', 6.3));
add(H2('3.2 NDSI, RSI and effective ranges'));
add(P(`The best NDSI combined ${J.ndsi_best[0]} and ${J.ndsi_best[1]} nm (R² = ${J.ndsi_best[2]}) and the best RSI combined ${J.rsi_best[0]} and ${J.rsi_best[1]} nm (R² = ${J.rsi_best[2]}) (Figure 4). Pairs with R² ≥ ${J.r2_threshold} defined an effective range of ${J.effective.ranges.join(', ')} nm (${J.effective.n} bands); the SWIR region beyond this range had lower R².`));
add(...FIG(FG + '/fig_ndsi_rsi.jpg', `Figure 4. R² between leaf score and (a) NDSI and (b) RSI for all band pairs (training dates). White contours: R² = ${J.r2_threshold}; stars: maxima (paper Fig. 7 analogue).`, 6.3));
add(H2('3.3 Optimal wavelengths'));
add(...T('Table 3. Optimal wavelengths selected on the three training dates (paper Table VII analogue)', [['Method', 'Variables', 'Wavelength (nm)'],
  ['RFE-RF', String(J.bands.rfe.length), J.bands.rfe.join(', ')], ['SAND', String(J.bands.sand.length), J.bands.sand.join(', ')], ['CARS-PLS (OWs)', String(J.bands.cars.length), J.bands.cars.join(', ')]], [1.4, 0.8, 5], { size: 17 }));
add(P(`All three methods selected red-edge bands (685–705 nm) and bands at the short-wave edge (355–375 nm). CARS reached its lowest RMSECV at run ${J.cars_curve.best} (Figure 5). Across the five internal folds the number of selected bands varied (RFE-RF ${J.fold_counts.map(r => r[1]).join('/')}, SAND ${J.fold_counts.map(r => r[2]).join('/')}, CARS-PLS ${J.fold_counts.map(r => r[3]).join('/')}).`));
add(...FIG(FG + '/fig_band_selection.jpg', 'Figure 5. (a) Selected wavelengths on the mean healthy spectrum (shaded: effective ranges); (b) SAND weights with the 0.524 threshold; (c) CARS RMSECV and number of variables (paper Fig. 8 analogue).', 6.3));
const stab = J.stability.map(r => [r[0], r[1], r[2], r[3], r[1] + r[2] + r[3]]).sort((a, b) => b[4] - a[4]).slice(0, 12);
add(...T('Table 4. Bands most often selected across the 5 internal folds', [['Band (nm)', 'RFE-RF', 'SAND', 'CARS-PLS', 'Total (max 15)'], ...stab.map(r => r.map(String))], [1, 1, 1, 1, 1.2], { center: true, size: 17 }));
add(H2('3.4 Vegetation indices'));
add(P(`The indices most correlated with leaf score were ${viS.slice(0, 4).map(r => `${r[0]} (r = ${f(r[2], 2)})`).join(', ')}. Relief selected ${viTop.join(', ')} (Table 5, Figure 6). As in the paper (Fig. 9), many indices were strongly inter-correlated.`));
add(...T('Table 5. Vegetation indices: formula, correlation with leaf score and Relief weight (paper Tables V and VIII analogue)', [['Index', 'Formula', 'r', 'Relief', 'Top 5'], ...J.vi.slice().sort((a, b) => b[3] - a[3]).map(r => [r[0], r[1], f(r[2], 3), f(r[3], 4), r[4]])], [1, 2.8, 0.8, 0.9, 0.7], { size: 16 }));
add(...FIG(FG + '/fig_vegetation_indices.jpg', 'Figure 6. Vegetation indices: (a) correlation with leaf score, (b) Relief weights (top five coloured), (c) correlation among indices.', 6.4));
add(H2('3.5 Internal validation'));
add(P(`Figure 7 and Table 6 summarise the internal results. The best single input was ${bestSingle[0]} (${bestSingle[1]}, OA ${f(bestSingle[2])}%), the full-wavelength baseline reached ${f(full[2])}% (${full[1]}) and the fused OWs + VIs input reached ${f(fused[2])}% (${fused[1]}). The overall best combination was ${bi.input} with ${bi.model}: OA ${f(bi.OA)}%, kappa ${f(bi.Kappa)}%, quadratic-weighted kappa ${f(bi.QWK)}%, macro F1 ${f(bi.F1)}%, and per-level F1 ${[bi.F1_L0, bi.F1_L1, bi.F1_L2, bi.F1_L3, bi.F1_L4].map(v => f(v, 0)).join(', ')}% for L0–L4. Fold-to-fold OA of this model was ${f(sd[0])} ± ${f(sd[1])}%.`));
add(...FIG(FG + '/fig_models_internal.jpg', 'Figure 7. Overall accuracy of four classifiers with six inputs, internal 5-fold cross-validation grouped by plot.', 6.3));
const tbl = key => [['Input', 'Model', 'F1 L0', 'F1 L1', 'F1 L2', 'F1 L3', 'F1 L4', 'OA', 'Kappa', 'QWK', 'Macro F1'],
  ...J.sets.flatMap(s => J.models.map(m => J[key].table.find(r => r[0] === s && r[1] === m)).map(r => r.map(v => typeof v === 'number' ? v.toFixed(1) : v)))];
add(...T('Table 6. Internal validation results (%) (paper Tables XI–XII analogue)', tbl('internal'), [2.2, 0.8, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.75], { center: true, size: 14, hl: (i, j, r) => r[0] === bi.input && r[1] === bi.model }));
add(H2('3.6 Independent validation'));
add(P(`On 13 Mar the best combination was ${be.input} with ${be.model} (OA ${f(be.OA)}%, kappa ${f(be.Kappa)}%, macro F1 ${f(be.F1)}%; Figure 8, Table 7). The best internal model (${J.cm_key.join(' + ')}) gave OA ${f(es.OA)}% and kappa ${f(es.Kappa)}% on this date. Kappa values near zero show that predictions on the later date were little better than chance; most leaves were assigned to a single level (Figure 9).`));
add(...FIG(FG + '/fig_models_external.jpg', 'Figure 8. Overall accuracy on the independent date (13 Mar 2026) for models trained on the three earlier dates.', 6.3));
add(...T('Table 7. Independent validation results (%) on 13 Mar 2026 (paper Table XIII analogue)', tbl('external'), [2.2, 0.8, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.75], { center: true, size: 14, hl: (i, j, r) => r[0] === be.input && r[1] === be.model }));
add(...FIG(FG + '/fig_confusion.jpg', `Figure 9. Confusion matrices of ${J.cm_key.join(' + ')}: internal cross-validation and independent date (counts and row %).`, 6.0));

add(H1('4. Discussion', false));
add(H2('4.1 Leaf spectral response'));
add(P('The direction of the spectral changes agrees with the physiology of foliar infection: chlorosis raises visible reflectance and alters the red edge, disruption of the mesophyll lowers NIR reflectance, and drying of infected tissue raises SWIR reflectance. As in the rice blast study, red-edge bands were selected repeatedly. The whole-range measurement also showed SWIR differences that UAV VNIR sensors cannot record. Bands at 355–375 nm were selected by all three methods; this short-wave edge of the ASD detector is noisy, so these bands should be confirmed before they are interpreted.'));
add(H2('4.2 Comparison with Ma et al. (2026)'));
add(P(`The paper reported OA of 95.25% with fused features and DT-EDNet, and 95.50% on its independent dataset. The leaf-level accuracies here are far lower (best internal OA ${f(bi.OA)}%), although the main pattern of the paper – fused wavelengths and indices performing best – was reproduced. Several factors explain the gap: (i) the visual score describes the whole leaf, while the probe reads one spot that may or may not include infected tissue; pustules are mainly on the lower surface; (ii) adjacent scores (0 vs 1, 3 vs 5) overlap strongly, as the near-identical L0 and L1 spectra show; (iii) validation here grouped leaves by plot and nested all selection steps, whereas the paper split pixel regions at random, which raises apparent accuracy; and (iv) texture information, which gave the paper’s best single feature (TTFI3), is not available from a probe.`));
add(H2('4.3 Transfer to a later date'));
add(P('The independent date was dominated by the pod-formation stage and had a higher mean score than the training dates. The spectral differences caused by leaf ageing and senescence were larger than those caused by disease, so models trained on earlier stages did not transfer. Including later stages in training, building stage-specific models, or normalising spectra within each date are needed before leaf-level models can be applied across the season.'));
add(H2('4.4 Limitations'));
add(B('Visual leaf scores are ordinal and subjective; one spectrum per leaf may not represent the scored leaf area.'));
add(B('Growth stage and disease are partly confounded across dates.'));
add(B('Classical models replaced DT-EDNet; with more data a deep network could be tested.'));
add(B('Effective ranges were defined at R² ≥ 0.25 instead of the paper’s 0.5 because correlations were weaker.'));
add(B('One season, one location.'));

add(H1('5. Conclusions', false));
add(...NL([
  `Leaf reflectance of mustard changes with white rust over 350–2500 nm, but the best two-band index explained only ${Math.round(maxR2 * 100)}% of the variation in leaf score.`,
  `Following Ma et al. (2026), RFE-RF, SAND and CARS-PLS selected compact band sets dominated by the red edge, and Relief selected ${viTop.join(', ')}.`,
  `The fused OWs + VIs input gave the best internal result (OA ${f(bi.OA)}%, quadratic-weighted kappa ${f(bi.QWK)}%), reproducing the paper’s finding that fusion helps, but five-level accuracy was modest.`,
  `Models did not transfer to the independent pod-formation date (best OA ${f(be.OA)}%, kappa ≈ 0).`,
  'Next steps: training across all growth stages, stage-specific or date-normalised models, measurement of the pustule-bearing surface, and testing the selected red-edge bands on simulated and real UAV data.',
]));

add(H1('References', false));
['Breiman, L. (2001). Random forests. *Machine Learning* 45(1), 5–32.',
 'Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement* 20(1), 37–46.',
 'Cortes, C., Vapnik, V. (1995). Support-vector networks. *Machine Learning* 20(3), 273–297.',
 'Guyon, I., Weston, J., Barnhill, S., Vapnik, V. (2002). Gene selection for cancer classification using support vector machines. *Machine Learning* 46, 389–422.',
 'Li, H., Liang, Y., Xu, Q., Cao, D. (2009). Key wavelengths screening using competitive adaptive reweighted sampling method for multivariate calibration. *Analytica Chimica Acta* 648(1), 77–84.',
 'Ma, J., Wu, P., Guo, S., Lin, Y., Yu, F., Liu, T. (2026). Early detection of rice blast disease using a dual transformer network (DT-EDNet) based on hyperspectral imaging and multi-feature fusion. *IAENG International Journal of Applied Mathematics* 56(11), 5380–5398.',
 'Pedregosa, F., Varoquaux, G., Gramfort, A., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research* 12, 2825–2830.',
 'Roberts, D.R., Bahn, V., Ciuti, S., et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography* 40(8), 913–929.',
 'Robnik-Šikonja, M., Kononenko, I. (2003). Theoretical and empirical analysis of ReliefF and RReliefF. *Machine Learning* 53, 23–69.',
 'Savitzky, A., Golay, M.J.E. (1964). Smoothing and differentiation of data by simplified least squares procedures. *Analytical Chemistry* 36(8), 1627–1639.',
 'Varma, S., Simon, R. (2006). Bias in error estimation when using cross-validation for model selection. *BMC Bioinformatics* 7, 91.',
 'Wold, S., Sjöström, M., Eriksson, L. (2001). PLS-regression: a basic tool of chemometrics. *Chemometrics and Intelligent Laboratory Systems* 58(2), 109–130.',
].forEach(r => add(new Paragraph({ spacing: { after: 80 }, indent: { left: 400, hanging: 400 }, children: L.runs(r, { size: 19 }) })));

const doc = new D.Document({ creator: 'MuDAS-AI', title: 'Leaf-level white rust detection from ASD spectra',
  styles: { default: { document: { run: { font: 'Calibri', size: 21 } } }, paragraphStyles: [
    { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 28, bold: true, color: TEAL }, paragraph: { spacing: { before: 280, after: 120 }, outlineLevel: 0, keepNext: true } },
    { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 23, bold: true, color: DARK }, paragraph: { spacing: { before: 180, after: 80 }, outlineLevel: 1, keepNext: true } }] },
  numbering: { config: [
    { reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 280 } } } }] },
    { reference: 'num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 320 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: 'Leaf-level white rust detection from ASD spectra', size: 16, color: GREY })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: ['Page ', PageNumber.CURRENT, ' of ', PageNumber.TOTAL_PAGES], size: 16, color: GREY })] })] }) },
    children: body }] });
D.Packer.toBuffer(doc).then(b => { require('fs').writeFileSync(process.argv[4], b); console.log('written', b.length); });
