// Research paper – pooled leaf-level analysis, DT-EDNet vs CNNs (Word)
const L = require('../ijam_doc/lib');
const { D, add, H1, H2, P, B, NL, EQ, T, BOX, FIG, Paragraph, TextRun, TEAL, DARK, GREY, body } = L;
const { AlignmentType, LevelFormat, Header, Footer, PageNumber } = D;
const J = require(process.argv[2]); const FG = process.argv[3];
const f = (v, d = 1) => (v === null || v === undefined) ? '–' : Number(v).toFixed(d), sum = a => a.reduce((x, y) => x + y, 0);
const LN = J.level_names, SETS = J.sets, DL = J.dl_models, CL = J.cl_models, sp = J.split, bd = J.dl.best, bc = J.classical.best;
const N = sum(sp.leaves);
const bestFor = (blk, models, m) => SETS.map((s, i) => [s, blk.OA[m][i], blk.F1[m][i]]).sort((a, b) => b[1] - a[1])[0];
const dtB = bestFor(J.dl, DL, 'DT-EDNet'), effB = bestFor(J.dl, DL, 'EfficientNet'), resB = bestFor(J.dl, DL, 'ResNet18'), cnxB = bestFor(J.dl, DL, 'ConvNeXt V2');
const viS = J.vi.slice().sort((a, b) => Math.abs(b[2]) - Math.abs(a[2])), viTop = J.vi.filter(r => r[4] === 'Yes').map(r => r[0]);
const z = J.mean_zoom, sv = (l, w) => z.series[LN[l]][z.wl.indexOf(w)], maxR2 = Math.max(J.ndsi_best[2], J.rsi_best[2]);
const abl = Object.fromEntries(J.ablation.map(r => [r[0], r]));
const pdOA = J.per_date.OA, pdates = J.per_date.dates;

add(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 200, after: 200 }, children: [new TextRun({ text: 'Leaf-level classification of white rust (Albugo candida) severity in Indian mustard from ASD contact-probe spectra: DT-EDNet versus EfficientNet, ResNet18 and ConvNeXt V2', bold: true, size: 32, color: DARK })] }));
add(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [new TextRun({ text: 'Animesh Panda', size: 22 })] }));
add(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: 'ICAR-Indian Agricultural Research Institute, New Delhi – MuDAS-AI project', size: 20, italics: true, color: GREY })] }));
add(...BOX('Abstract', [`Ma et al. (2026) introduced DT-EDNet, a dual-transformer network combined with multi-feature fusion, for early detection of rice blast from UAV hyperspectral images. This study applies their workflow and the same four networks – DT-EDNet, EfficientNet, ResNet18 and ConvNeXt V2 – to leaf-level ASD contact-probe spectra of Indian mustard affected by white rust. Spectra (350–2500 nm) of ${N.toLocaleString()} leaves from four dates (11 Feb – 13 Mar 2026) and 48 plots were pooled. Each leaf’s score (0, 1, 3, 5, 7, 9) was grouped into five levels (L0–L4). Following the paper, the data were split 7:3 into training and test sets with 10% of the training set for validation, but the split was made by plot so that no plot contributed to both. NDSI/RSI maps defined effective wavelength ranges (${J.effective.ranges.join(', ')} nm); RFE with random forest, SAND and CARS-PLS selected ${J.bands.rfe.length}, ${J.bands.sand.length} and ${J.bands.cars.length} optimal wavelengths; Relief selected five of 17 vegetation indices. Texture features were not used because probe spectra are non-imaging. Networks were trained from scratch with the paper’s settings on six inputs. On ${sp.leaves[2]} test leaves from ${sp.plots[2]} unseen plots the best result was ${bd.model} with ${bd.input} (OA ${f(bd.OA)}%, Cohen’s kappa ${f(bd.Kappa)}%, quadratic-weighted kappa ${f(bd.QWK)}%, macro F1 ${f(bd.F1)}%). DT-EDNet reached ${f(dtB[1])}% (${dtB[0]}); the best classical model reached ${f(bc.OA)}% (${bc.model}). Accuracies were far below the 95% reported for rice blast, reflecting overlapping leaf scores, single-spot probe readings, strict plot-grouped testing, the absence of texture and a training set close to the minimum for deep networks.`]));
add(P('**Keywords:** white rust; Albugo candida; Brassica juncea; ASD FieldSpec; leaf reflectance; DT-EDNet; transformer; EfficientNet; ResNet18; ConvNeXt V2; band selection'));

add(H1('1. Introduction', false));
add(P('White rust, caused by *Albugo candida*, produces white pustules mainly on the lower leaf surface of Indian mustard (*Brassica juncea*), with chlorosis on the upper surface. Spectral sensing could make severity assessment faster and less subjective than visual scoring.'));
add(P('Ma et al. (2026) proposed a workflow for early detection of rice blast with UAV hyperspectral imagery: severity grading into five levels, NDSI/RSI band-pair search, optimal-wavelength selection by three methods, vegetation indices ranked by Relief, texture features and a tri-band texture index, and a new network, DT-EDNet, which combines a squeeze-and-excitation (SE) block, convolutional block attention (CBAM) and transformer self-attention. DT-EDNet outperformed EfficientNet, ResNet18 and ConvNeXt V2, reaching 95.25% overall accuracy.'));
add(P('This study tests the same workflow and networks on leaf-level contact-probe spectra of mustard. All four measurement dates were pooled so that every growth stage is represented in training. The objectives were to (i) characterise the leaf spectral response to white rust over 350–2500 nm, (ii) select wavelengths and indices following the paper, and (iii) compare DT-EDNet with EfficientNet, ResNet18 and ConvNeXt V2 for five-level leaf severity classification.'));

add(H1('2. Materials and methods', false));
add(H2('2.1 Data'));
add(P('The field experiment had 48 plots of three varieties (36 inoculated with *A. candida*, 12 healthy). Leaf reflectance was measured with an ASD FieldSpec spectroradiometer and contact probe (350–2500 nm) on four dates, generally on five plants × three leaf positions per plot, and each leaf was scored on the 0–9 scale. Seventy-five duplicated spectra on 13 Mar were removed (Table 1).'));
add(...T('Table 1. Leaf spectra per date (pooled for analysis)', [['Date', 'Leaves', 'Plots', 'Growth stage(s)'], ...J.inventory.map(r => r.map(String)), ['Total', String(N), '48', '']], [1.2, 1, 1, 3], { center: true }));
add(H2('2.2 Severity levels and pooled split'));
add(P(`Each leaf was labelled by its own score: L0 = 0, L1 = 1, L2 = 3, L3 = 5 and L4 = 7–9. As in the paper, the data were split 7:3 into training and test sets and 10% of the training set was held out for validation (early stopping and model selection). Because leaves of the same plot are correlated, the split was made by plot (stratified by treatment): ${sp.plots[0]} plots for training, ${sp.plots[1]} for validation and ${sp.plots[2]} for testing, each containing all four dates (Table 2).`));
add(...T('Table 2. Leaves per level in the pooled split (paper Table IV analogue)', [['Level', 'Training', 'Validation', 'Test'], ...LN.map((n, l) => [n, ...sp.by_level[l].map(String)]), ['Total leaves', ...sp.leaves.map(String)], ['Plots (healthy)', ...sp.plots.map((p, i) => `${p} (${sp.healthy_plots[i]})`)]], [2.4, 1.2, 1.2, 1.2], { center: true }));
add(...FIG(FG + '/fig_counts.jpg', 'Figure 1. (a) Leaves per level and date; (b) leaves per level in the plot-grouped training, validation and test sets.', 6.2));
add(H2('2.3 Pre-processing'));
add(P(`Detector steps at 1000 and 1800 nm were corrected and spectra were smoothed with a Savitzky–Golay filter (window 11, order 2), as in the paper. The whole 350–2500 nm range was kept (the contact probe has its own light source, so the water bands carry leaf information). Reflectance was averaged into 215 bands of 10 nm for selection; for the full-wavelength deep-learning input, 108 bands of 20 nm were used to keep transformer training time manageable.`));
add(H2('2.4 Band-pair indices, optimal wavelengths and vegetation indices'));
add(P(`On the training leaves only, NDSI = (R₁ − R₂)/(R₁ + R₂) and RSI = R₁/R₂ were computed for all band pairs (20-nm grid) and their R² with leaf score mapped. Effective ranges were the bands in any pair with R² ≥ ${J.r2_threshold} (the paper used R² > 0.5, which no pair reached here). Within these ranges, three selectors were applied: RFE with random forest (10 bands, as RFE-SHAP), SAND (learnable sigmoid weights with a sparsity penalty, bands with weight > 0.524 kept, as described in the paper) and CARS-PLS (50 Monte Carlo runs, plot-grouped RMSECV; Li et al., 2009). CARS bands were used as the optimal wavelengths (OWs). The paper’s 16 vegetation indices plus PSRI were computed and ranked with Relief; the top five formed the VI input. Texture features and TTFI were not used because contact-probe spectra are non-imaging.`));
add(H2('2.5 Networks'));
add(P('**DT-EDNet** was re-implemented from the description in Ma et al. (2026): the input feature vector is zero-padded and reshaped into a pseudo-2-D map, projected by a 3 × 3 convolution to 128 channels, recalibrated by an SE block (Hu et al., 2018), given a learnable class token and processed by a Dual Transformer Group consisting of one Kernel Transformer Block (depth-wise convolution with CBAM; Woo et al., 2018) and four Token Transformer Blocks (four-head self-attention and feed-forward layers; Vaswani et al., 2017); the normalised class token feeds a linear classifier (dropout 0.03). Details not given in the paper (feed-forward width, positional embedding) were chosen as standard values. **EfficientNet-B0** (Tan and Le, 2019), **ResNet18** (He et al., 2016) and **ConvNeXt V2-Atto** (Woo et al., 2023) were taken from the timm library with one input channel and trained from scratch; their pseudo-2-D inputs were resized to 32 × 32.'));
add(P('All networks used the paper’s training settings: AdamW (learning rate 6 × 10⁻⁴, weight decay 1 × 10⁻⁵), cosine schedule to 1 × 10⁻⁶ over 300 epochs, batch size 32, cross-entropy with label smoothing 0.01, gradient clipping at norm 1.2, early stopping with patience 60 on validation OA, selection of the epoch with the highest validation OA, and seed 42. Six inputs were tested: RFE-RF, SAND, CARS-PLS, VIs, full wavelength and OWs + VIs. The ablation of the paper (removing SE, the Dual Transformer Group, or both) was repeated on the full-wavelength input. Random forest, SVM, PLS-DA and an MLP were fitted on the same split as a reference.'));
add(H2('2.6 Metrics'));
add(P('Overall accuracy (OA), Cohen’s kappa, macro recall and macro and per-level F1 were computed on the test plots, as in the paper; quadratic-weighted kappa (which credits near-misses between ordered levels), test accuracy per date and confusion matrices were added.'));

add(H1('3. Results', false));
add(H2('3.1 Spectral response'));
add(P(`Reflectance at 550 nm was ${f(sv(0, 550), 3)} for L0 and ${f(sv(4, 550), 3)} for L4; at 680 nm ${f(sv(0, 680), 3)} and ${f(sv(4, 680), 3)}; at 850 nm ${f(sv(0, 850), 3)} and ${f(sv(4, 850), 3)} (Figure 2). Visible and SWIR reflectance rose and NIR reflectance fell with severity, but L0 and L1 were almost identical and within-level variation was large.`));
add(...FIG(FG + '/fig_mean_spectra.jpg', 'Figure 2. Mean leaf reflectance by severity level: (a) 350–2500 nm; (b) 450–1000 nm with ± 1 SD (paper Fig. 6 analogue).', 6.3));
add(H2('3.2 Band-pair indices, wavelengths and vegetation indices'));
add(P(`The best NDSI used ${J.ndsi_best[0]}/${J.ndsi_best[1]} nm (R² = ${J.ndsi_best[2]}) and the best RSI ${J.rsi_best[0]}/${J.rsi_best[1]} nm (R² = ${J.rsi_best[2]}) (Figure 3). The effective range was ${J.effective.ranges.join(', ')} nm (${J.effective.n} bands). Table 3 lists the selected wavelengths (Figure 4). The indices most correlated with leaf score were ${viS.slice(0, 4).map(r => `${r[0]} (r = ${f(r[2], 2)})`).join(', ')}; Relief selected ${viTop.join(', ')} (Table 4, Figure 5).`));
add(...FIG(FG + '/fig_ndsi_rsi.jpg', `Figure 3. R² between leaf score and (a) NDSI, (b) RSI (training leaves); white contour R² = ${J.r2_threshold}.`, 6.3));
add(...T('Table 3. Optimal wavelengths (paper Table VII analogue)', [['Method', 'Variables', 'Wavelength (nm)'], ['RFE-RF', String(J.bands.rfe.length), J.bands.rfe.join(', ')], ['SAND', String(J.bands.sand.length), J.bands.sand.join(', ')], ['CARS-PLS (OWs)', String(J.bands.cars.length), J.bands.cars.join(', ')]], [1.4, 0.8, 5], { size: 17 }));
add(...FIG(FG + '/fig_band_selection.jpg', 'Figure 4. (a) Selected wavelengths (shaded: effective ranges); (b) SAND weights; (c) CARS RMSECV and variables (paper Fig. 8 analogue).', 6.3));
add(...T('Table 4. Vegetation indices: correlation with leaf score and Relief weight (training leaves)', [['Index', 'Formula', 'r', 'Relief', 'Top 5'], ...J.vi.slice().sort((a, b) => b[3] - a[3]).map(r => [r[0], r[1], f(r[2], 3), f(r[3], 4), r[4]])], [1, 2.8, 0.8, 0.9, 0.7], { size: 16 }));
add(...FIG(FG + '/fig_vegetation_indices.jpg', 'Figure 5. Vegetation indices: (a) correlation, (b) Relief weights, (c) correlation among indices.', 6.4));
add(H2('3.3 DT-EDNet versus CNNs'));
add(P(`Figure 6 and Table 5 give the test results. The best combination was ${bd.model} with ${bd.input}: OA ${f(bd.OA)}%, kappa ${f(bd.Kappa)}%, quadratic-weighted kappa ${f(bd.QWK)}%, macro F1 ${f(bd.F1)}%, per-level F1 ${[bd.F1_L0, bd.F1_L1, bd.F1_L2, bd.F1_L3, bd.F1_L4].map(v => f(v, 0)).join(', ')}% for L0–L4. The best input for each network was: DT-EDNet – ${dtB[0]} (${f(dtB[1])}%); EfficientNet – ${effB[0]} (${f(effB[1])}%); ResNet18 – ${resB[0]} (${f(resB[1])}%); ConvNeXt V2 – ${cnxB[0]} (${f(cnxB[1])}%).`));
add(...FIG(FG + '/fig_models_dl.jpg', 'Figure 6. Test overall accuracy of DT-EDNet, EfficientNet, ResNet18 and ConvNeXt V2 with six inputs (paper Fig. 12–13 analogue).', 6.3));
const tbl = blk => [['Input', 'Model', 'F1 L0', 'F1 L1', 'F1 L2', 'F1 L3', 'F1 L4', 'OA', 'Kappa', 'QWK', 'Macro F1'], ...SETS.flatMap(s => blk.table.filter(r => r[0] === s).map(r => r.map(v => typeof v === 'number' ? v.toFixed(1) : v)))];
add(...T('Table 5. Test results (%) of the four networks (paper Tables XI–XII analogue)', tbl(J.dl), [2.2, 1.0, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62, 0.62, 0.72], { center: true, size: 14, hl: (i, j, r) => r[0] === bd.input && r[1] === bd.model }));
add(H2('3.4 Ablation'));
add(P(`On the full-wavelength input, DT-EDNet reached OA ${f(abl['DT-EDNet'][2])}%; without SE ${f(abl['DT-EDNet-SE'][2])}%, without the Dual Transformer Group ${f(abl['DT-EDNet-DTG'][2])}%, and without both ${f(abl['DT-EDNet-SE-DTG'][2])}% (Table 6, Figure 7).`));
add(...T('Table 6. Ablation of DT-EDNet on the full-wavelength input (paper Table X analogue)', [['Model', 'F1-score (%)', 'OA (%)', 'Kappa (%)', 'Recall (%)'], ...J.ablation.map(r => [r[0], ...r.slice(1).map(v => f(v, 2))])], [2, 1, 1, 1, 1], { center: true }));
add(...FIG(FG + '/fig_ablation.jpg', 'Figure 7. Ablation of the SE block and the Dual Transformer Group.', 4.8));
add(H2('3.5 Accuracy by date, classical reference and errors'));
add(P(`With ${J.per_date.set}, test OA by date (DT-EDNet) was ${pdates.map((d, i) => `${d} ${f(pdOA['DT-EDNet'][i])}%`).join(', ')} (Figure 8). The best classical model on the same split was ${bc.model} with ${bc.input} (OA ${f(bc.OA)}%, macro F1 ${f(bc.F1)}%; Table 7). Most errors were between neighbouring levels (Figure 9).`));
add(...FIG(FG + '/fig_per_date.jpg', 'Figure 8. Test accuracy of each network by date (best input).', 5.0));
add(...T('Table 7. Classical models on the same split (%), best input per model', [['Model', 'Best input', 'OA', 'Kappa', 'Macro F1'], ...CL.map(m => { const b = bestFor(J.classical, CL, m); const r = J.classical.table.find(x => x[0] === b[0] && x[1] === m); return [m, b[0], r[7].toFixed(1), r[8].toFixed(1), r[10].toFixed(1)]; })], [1, 2.6, 0.8, 0.8, 0.9], { center: true }));
add(...FIG(FG + '/fig_confusion.jpg', `Figure 9. Confusion matrices on the test plots: best network (${J.cm_key.join(' + ')}) and DT-EDNet (${J.cm_dt_key[0]}).`, 6.0));

add(H1('4. Discussion', false));
add(H2('4.1 Why the accuracies are lower than in the rice blast study'));
add(P('Ma et al. (2026) reported 95.25% OA for DT-EDNet with fused spectral, index and texture features. Several differences explain the much lower values here. First, the visual score describes the whole leaf, while the probe reads a single spot that may miss the pustule-bearing tissue, which lies mainly on the lower surface; neighbouring scores therefore overlap strongly, as the near-identical L0 and L1 spectra show. Second, the split here was by plot, whereas the paper divided pixel regions at random; neighbouring pixels share almost identical spectra, which inflates accuracy. Third, the texture index that gave the paper’s best single feature cannot be computed from probe spectra. Fourth, the spectral–score relationship was weaker (maximum R² ' + maxR2 + ' versus > 0.5 in the paper).'));
add(H2('4.2 Deep versus classical models'));
add(P(`DT-EDNet has about 0.6 million parameters and the CNNs 3–11 million, yet only ${sp.leaves[0].toLocaleString()} training leaves from ${sp.plots[0]} plots were available. Under these conditions deep networks have little room to outperform classical models; here the best network reached ${f(bd.OA)}% and the best classical model ${f(bc.OA)}%. CNNs designed for natural images also have no built-in reason to work on a resized pseudo-image of a spectrum, and all four networks stayed within a narrow band of accuracy (OA ${f(Math.min(...DL.flatMap(m => J.dl.OA[m])))}–${f(Math.max(...DL.flatMap(m => J.dl.OA[m])))}%), close to the classical models.`));
add(H2('4.3 Effect of pooling'));
add(P('Pooling all dates placed every growth stage in the training set, so the models were tested on new plots rather than a new stage. This avoids the failure seen when models trained on earlier dates were applied to the pod-formation date, but it does not test transfer to a new season, which remains necessary.'));
add(H2('4.4 Limitations'));
add(B('Visual leaf scores are ordinal and subjective; one spectrum per leaf.'));
add(B('Single plot-grouped split (as in the paper); results from one seed may vary by a few percentage points.'));
add(B('DT-EDNet re-implemented from the paper’s description; some architectural details had to be assumed.'));
add(B('One season and one location; effective ranges defined at R² ≥ ' + J.r2_threshold + '.'));

add(H1('5. Conclusions', false));
add(...NL([
  `Mustard leaf reflectance changes with white rust across 350–2500 nm, but the best band-pair index explained only ${Math.round(maxR2 * 100)}% of leaf-score variation.`,
  `With all dates pooled and an unseen-plot test set, the best network was ${bd.model} (${bd.input}; OA ${f(bd.OA)}%, quadratic-weighted kappa ${f(bd.QWK)}%); DT-EDNet reached ${f(dtB[1])}%.`,
  'Five-level grading of single leaves from probe spectra remains difficult; most errors are between neighbouring levels.',
  'Deep networks need substantially more independent data (more plots, seasons and growth stages) before their advantage reported for rice blast can be expected here.',
]));

add(H1('References', false));
['He, K., Zhang, X., Ren, S., Sun, J. (2016). Deep residual learning for image recognition. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, 770–778.',
 'Hu, J., Shen, L., Sun, G. (2018). Squeeze-and-excitation networks. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*, 7132–7141.',
 'Li, H., Liang, Y., Xu, Q., Cao, D. (2009). Key wavelengths screening using competitive adaptive reweighted sampling method for multivariate calibration. *Analytica Chimica Acta* 648(1), 77–84.',
 'Ma, J., Wu, P., Guo, S., Lin, Y., Yu, F., Liu, T. (2026). Early detection of rice blast disease using a dual transformer network (DT-EDNet) based on hyperspectral imaging and multi-feature fusion. *IAENG International Journal of Applied Mathematics* 56(11), 5380–5398.',
 'Robnik-Šikonja, M., Kononenko, I. (2003). Theoretical and empirical analysis of ReliefF and RReliefF. *Machine Learning* 53, 23–69.',
 'Savitzky, A., Golay, M.J.E. (1964). Smoothing and differentiation of data by simplified least squares procedures. *Analytical Chemistry* 36(8), 1627–1639.',
 'Tan, M., Le, Q. (2019). EfficientNet: Rethinking model scaling for convolutional neural networks. *Proceedings of the 36th International Conference on Machine Learning*, PMLR 97, 6105–6114.',
 'Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kaiser, Ł., Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems* 30.',
 'Woo, S., Debnath, S., Hu, R., Chen, X., Liu, Z., Kweon, I.S., Xie, S. (2023). ConvNeXt V2: Co-designing and scaling ConvNets with masked autoencoders. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 16133–16142.',
 'Woo, S., Park, J., Lee, J.-Y., Kweon, I.S. (2018). CBAM: Convolutional block attention module. *Proceedings of the European Conference on Computer Vision (ECCV)*, 3–19.',
].forEach(r => add(new Paragraph({ spacing: { after: 80 }, indent: { left: 400, hanging: 400 }, children: L.runs(r, { size: 19 }) })));

const doc = new D.Document({ creator: 'MuDAS-AI', title: 'Leaf-level white rust – DT-EDNet vs CNNs',
  styles: { default: { document: { run: { font: 'Calibri', size: 21 } } }, paragraphStyles: [
    { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 28, bold: true, color: TEAL }, paragraph: { spacing: { before: 280, after: 120 }, outlineLevel: 0, keepNext: true } },
    { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { size: 23, bold: true, color: DARK }, paragraph: { spacing: { before: 180, after: 80 }, outlineLevel: 1, keepNext: true } }] },
  numbering: { config: [
    { reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 280 } } } }] },
    { reference: 'num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 320 } } } }] }] },
  sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: 'Leaf-level white rust – DT-EDNet vs CNNs', size: 16, color: GREY })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: ['Page ', PageNumber.CURRENT, ' of ', PageNumber.TOTAL_PAGES], size: 16, color: GREY })] })] }) },
    children: body }] });
D.Packer.toBuffer(doc).then(b => { require('fs').writeFileSync(process.argv[4], b); console.log('written', b.length); });
