// ======================= 9 OBJECTIVE 2 =======================
K.push(H1('9. Objective 2: Six-grade classification and PDI regression by multimodal fusion'));
K.push(P(`**Objective 2 (ORW):** to classify and estimate white-rust severity with machine-learning models on single sensors and sensor combinations. The two tasks run in parallel: **classification of the six grades (0, 1, 3, 5, 7, 9)** and **regression of PDI (%)**. Inputs are the DSF pools of Objective 1. ${F('o2flow')} shows the six tiers. Every selection and tuning step is repeated inside the training replications of the leave-one-replication-out (LORO) design of Tier 0, so the held-out replication never influences the model.`));
K.push(...fig2('o2flow', 'o2_flow.png', 'Flow chart of Objective 2.', 500));

TIER({ title: 'O2 Tier 1. Optimum feature combination: VIF → ML-SFFS',
 pos: `After the Boruta tiers of Objective 1 (DSF pools); before O2 Tier 2, whose models are trained on the selected features. Repeated inside every training replication.`,
 problem: `DSF pools still contain collinear features (several NDVI variants, neighbouring indices) and too many features for about 290 training plot-dates per fold; models overfit and become hard to explain.`,
 concept: `The **variance inflation factor** VIF_{j} = 1/(1 − R_{j}^{2}) measures how well feature j is predicted by the others; the feature with the largest VIF is removed until all VIF < 10. **ML-SFFS** (machine-learning sequential floating forward selection) then adds the feature that most improves the model's cross-validated score and, after each addition, removes earlier features that have become redundant (Pudil et al., 1994).`,
 eqs: [EQ('VIF_{j} = 1 / (1 − R_{j}^{2})', 'e:o2vif')],
 need: `It turns the broad, relevance-based DSF pools into a small, non-redundant, model-specific set before training.`,
 why: `Boruta (Objective 1) keeps **all** relevant features, including near-duplicates; models need a **minimal** set. VIF < 10 → ML-SFFS is exactly the chain of Tian et al. (2021) and Mustafa et al. (2023); 2–4 features were enough for rice blast and SVM-SFFS was up to 10% more accurate than SVM with all features (Tian et al., 2021). VIF is repeated here, although it was used before CDA, because the input sets are different (Boruta pools and fused pools of several sensors) and it must run inside the folds.`,
 papers: [`Tian et al. (2021): VIF < 10 then ML-SFFS with SVM, k-NN and LDA; 2–4 features enough.`, `Mustafa et al. (2023): Boruta → VIF < 10 → ML-SFFS across three sensors.`, `Zhu et al. (2017); Huang et al. (2020): SPA wavelength selection.`],
 alts: TAB('o2alt1', [['Alternative', 'How it works / used by', 'Why not used here'], ['SPA', 'Projections choose low-collinearity variables (Araújo et al., 2001; Huang et al., 2020)', 'Chooses for non-redundancy, not model performance; tied to MLR'], ['Recursive feature elimination', 'Drop the least important feature repeatedly (Guyon et al., 2002)', 'Needs a model importance measure; no floating correction'], ['mRMR', 'Maximum relevance, minimum redundancy by mutual information (Peng et al., 2005)', 'Filter method; the number of features must be fixed in advance'], ['LASSO', 'L1 penalty shrinks coefficients to zero (Tibshirani, 1996)', 'Linear; unstable with correlated features']], [2100, 3900, 3306], 'Alternatives for O2 Tier 1.', 16),
 how: [`VIF: compute for all features of the pool; remove the largest; repeat until all < 10.`, `ML-SFFS for each model: criterion macro-F1 (grades) or RMSE (PDI); at most 10 features; grouped 4-fold CV inside the training replications.`, `Optimum feature combination (OFC) = the subset with the best score; a smaller subset within 0.01 of it is preferred. Repeated 10 times with different inner splits; features selected in most repeats are kept.`],
 mine: `${T('o2vif')} shows VIF removing near-duplicate NDVI variants from a dummy HS pool. In the dummy ML-SFFS run on the fused pool (${F('o2sffs')}) SVM kept ${DUM2.sffs.SVM[2]} features (macro-F1 ${DUM2.sffs.SVM[1]}: ${DUM2.sffs.SVM[0]}), k-NN ${DUM2.sffs['k-NN'][2]} and RF ${DUM2.sffs.RF[2]}; the WRI and REP were chosen first by every model.`,
 vis: [TAB('o2vif', [['Iteration', 'Largest VIFs', 'Action']].concat(DUM2.vif.map((r, i) => [String(i + 1), r[0], r[1]])), [1100, 5600, 2606], 'Dummy VIF iterations on a hyperspectral pool with two added NDVI variants (computed on simulated data).', 16),
       FIG('o2sffs', 'o2_sffs.png', 'Dummy ML-SFFS curves on the fused DSF pool for SVM, k-NN and RF (six grades, LORO macro-F1); star = optimum feature combination.', 460)],
 out: `For each sensor set, task and model: the OFC (typically 3–8 features) and its cross-validated score.`,
 qs: [[`Why VIF before SFFS?`, `Removing near-duplicates first makes the search faster and more stable; SFFS then picks what helps the model.`], [`What is "floating" in SFFS?`, `After adding a feature, earlier features are dropped if that improves the score, so early wrong choices are corrected.`], [`You already did VIF before CDA. Why again?`, `Different input sets (Boruta pools, fused pools) and it must be inside each training fold to avoid leakage.`]],
 refs: `Pudil et al. (1994); Tian et al. (2021); Mustafa et al. (2023).` });

TIER({ title: 'O2 Tier 2. Six models and their tuning',
 pos: `After O2 Tier 1 (OFC per model); the trained models are compared in O2 Tiers 3 and 4.`,
 problem: `No single algorithm is best for every sensor and task; the choice must be shown by comparison, not assumed.`,
 concept: `Six models of different families: **SVM/SVR** (maximum-margin kernel method), **RF/RFR** (ensemble of decision trees), **k-NN** (majority or mean of the nearest neighbours), **PLSR** (linear latent components, regression only), **DNN-F1** (all features joined at the input) and **DNN-F2** (one sub-network per sensor, joined at an intermediate layer).`,
 need: `It shows whether linear, kernel, tree or deep models suit white-rust data and gives the models used for fusion in O2 Tier 3.`,
 why: `Each model was the best in one of the reference papers: SVM in Tian et al. (2021), RFR in Feng et al. (2022), k-NN in Mustafa et al. (2023), DNN-F2 in Maimaitijiang et al. (2020); PLSR is the standard linear baseline for spectra (Shukla et al., 2024; Guo et al., 2021). With six unequal grades (32 to 130 plot-dates), class weights are used in every classifier.`,
 papers: [`Feng et al. (2022): PLSR, SVR and RFR — RFR best.`, `Mustafa et al. (2023): k-NN, RF and SVM — k-NN best for regression.`, `Maimaitijiang et al. (2020): PLSR, SVR, RFR, DNN-F1, DNN-F2 — DNN-F2 best.`, `Tian et al. (2021): SVM, k-NN, LDA; Shukla et al. (2024) and Guo et al. (2021): PLSR.`],
 alts: TAB('o2alt2', [['Alternative', 'How it works / used by', 'Why not used here'], ['XGBoost', 'Gradient-boosted trees (Chen and Guestrin, 2016)', 'Similar to RF here; more hyperparameters for a small dataset'], ['Gaussian process regression', 'Kernel regression with uncertainty (Rasmussen and Williams, 2006)', 'Optional; uncertainty can come from RF quantiles'], ['BPNN, ELM, LS-SVM', 'Shallow networks and kernel variants (Zhu et al., 2017)', 'Covered by SVM and the small DNNs'], ['Ordinal classifier', 'Uses the order of grades (Frank and Hall, 2001)', 'Order is already used by PDI regression and ±1-grade accuracy']], [2200, 3800, 3306], 'Alternatives for O2 Tier 2.', 16),
 how: [`SVM/SVR: RBF kernel, C and γ (ε for SVR) by grid search; class weights inversely proportional to grade size.`, `RF/RFR: 500 trees, mtry and minimum leaf size tuned. k-NN: k = 3–11 on standardised features. PLSR: 1–10 components by minimum RMSE.`, `DNN-F1/F2: dense layers with ReLU, batch normalisation, dropout, Adam, early stopping; softmax output (six grades) or linear output (PDI). Kept very small (e.g. 8–4 units per sensor sub-network, about 1 000 weights), several random seeds, always compared with the classical models.`],
 mine: `Classification uses SVM, RF, k-NN, DNN-F1 and DNN-F2; regression uses SVR, RFR, k-NN, PLSR, DNN-F1 and DNN-F2 (${T('o2models')}, ${F('o2dnn')}).`,
 vis: [TAB('o2models', [['Model', 'Family', 'Task', 'Key hyperparameters', 'Basis'], ['SVM / SVR', 'Kernel', 'C, R', 'C, γ (ε for SVR)', 'Tian 2021; Mahlein 2019'], ['RF / RFR', 'Tree ensemble', 'C, R', 'trees, mtry, leaf size', 'Feng 2022'], ['k-NN', 'Instance-based', 'C, R', 'k', 'Mustafa 2023'], ['PLSR', 'Linear latent', 'R', 'components', 'Shukla 2024; Guo 2021'], ['DNN-F1', 'Deep, input fusion', 'C, R', 'layers, dropout', 'Maimaitijiang 2020'], ['DNN-F2', 'Deep, intermediate fusion', 'C, R', 'sub-networks, dropout', 'Maimaitijiang 2020']], [1500, 1900, 900, 2500, 2506], 'The six models (C = six-grade classification, R = PDI regression).', 16),
       FIG('o2dnn', 'o2_dnn.png', 'DNN-F1 (input-level fusion) and DNN-F2 (intermediate-level fusion), adapted from Maimaitijiang et al. (2020).', 500)],
 out: `Tuned models for each sensor set, task and fold.`,
 qs: [[`What do C and γ do in SVM?`, `C penalises training errors (large C fits closely); γ sets how local the RBF kernel is (large γ gives wiggly boundaries).`], [`Why are the DNNs so small?`, `About 290 training plot-dates per fold; a large network would memorise them.`], [`Why not an ordinal model for ordered grades?`, `The order is used through PDI regression and by reporting ±1-grade accuracy; an ordinal classifier is a possible extension.`]],
 refs: `Cortes and Vapnik (1995); Breiman (2001); Cover and Hart (1967); Wold et al. (2001); Maimaitijiang et al. (2020).` });

TIER({ title: 'O2 Tier 3. Single sensors versus sensor combinations (fusion)',
 pos: `After O2 Tiers 1 and 2; its predictions are evaluated in O2 Tier 4.`,
 problem: `Objective 2 asks whether combining sensors improves grade classification and PDI estimation over the best single sensor.`,
 concept: `**Feature-level fusion** combines features of several sensors in one model. Two ways are compared: **ML-SFFS fusion** (DSF pools concatenated → VIF → ML-SFFS → SVM, RF, k-NN, PLSR) and **DNN fusion** (DNN-F1, DNN-F2).`,
 need: `It answers the fusion question and tells which sensors are worth flying.`,
 why: `The cross-sensor tier of Objective 1 showed low correlation between thermal and spectral DSFs, i.e. complementary information. Fusion improved disease estimation in Feng et al. (2022), Liu et al. (2024) and Deng et al. (2024); ML-SFFS fusion was used by Mustafa et al. (2023), DNN fusion by Maimaitijiang et al. (2020). Mahlein et al. (2019) found that a third sensor did not always help, so each combination is tested.`,
 papers: [`Maimaitijiang et al. (2020): input- and intermediate-level DNN fusion of RGB, MS and thermal.`, `Mustafa et al. (2023): ML-SFFS fusion of features from three sensors.`, `Feng et al. (2022): fusion of spectra, thermal and texture (R² 0.86 in validation); Liu et al. (2024): MS + thermal.`, `Mahlein et al. (2019): HS + thermal best pair; a third sensor did not help.`],
 alts: TAB('o2alt3', [['Alternative', 'How it works / used by', 'Why not used here'], ['Decision-level fusion (stacking)', 'Combine predictions of single-sensor models (Wolpert, 1992)', 'Needs more data for the meta-model'], ['End-to-end image fusion network', 'CNN on co-registered image stacks (Deng et al., 2024)', 'Needs many labelled images; plot-level data are few'], ['Attention-based fusion', 'Learned sensor weights (Ramachandram and Taylor, 2017)', 'Too many parameters for this sample size']], [2400, 3700, 3206], 'Alternatives for O2 Tier 3.', 16),
 how: [`Input sets: S1 RGB, S2 MS, S3 HS, S4 TIR; S5 RGB + TIR, S6 MS + TIR, S7 HS + TIR, S8 all four (ORW).`, `For every set and task: ML-SFFS fusion with SVM, RF, k-NN (and PLSR for PDI), DNN-F1, and DNN-F2 for combinations.`, `Fusion is useful only if it beats the best single sensor on the held-out replications.`],
 mine: `80 configurations in total (single sensors: 16 for classification + 20 for regression; combinations: 20 + 24). In the dummy run (${F('o2fusion')}) HS was the best single sensor (macro-F1 ${DUM2.fusion['S3 HS'][0]}, R² ${DUM2.fusion['S3 HS'][1]}) and all four sensors gave the best result (macro-F1 ${DUM2.fusion['S8 all four'][0]}, R² ${DUM2.fusion['S8 all four'][1]}); the gain over HS was small, which is the kind of result that decides whether fusion is worth its cost.`,
 vis: [FIG('o2fusion', 'o2_fusion.png', 'Dummy comparison of single sensors (grey) and combinations (blue): macro-F1 for six grades (a) and R² for PDI (b), LORO.', 540)],
 out: `Performance of every sensor set and fusion approach for both tasks; the sensor make-up of the fused OFCs.`,
 qs: [[`What if fusion does not help?`, `Then the sensors are redundant for white rust and the cheaper sensor is enough; this is a valid result (Mahlein et al., 2019).`], [`Why test HS + TIR separately?`, `They measure different processes (pigment and water vs transpiration); it was the best pair in Mahlein et al. (2019).`]],
 refs: `Mustafa et al. (2023); Maimaitijiang et al. (2020); Feng et al. (2022); Mahlein et al. (2019).` });

TIER({ title: 'O2 Tier 4. Evaluation and comparison',
 pos: `After O2 Tier 3 (predictions on held-out replications); it selects the best configuration used in O2 Tiers 5 and 6.`,
 problem: `80 configurations must be compared fairly; with six unequal, ordered and overlapping grades, overall accuracy alone is misleading.`,
 concept: `Grades are evaluated from the confusion matrix: overall accuracy (OA), Cohen's kappa, per-grade precision, recall and F1, macro-F1, and **±1-grade accuracy** (share of plots predicted in the correct or an adjacent grade). PDI is evaluated with R^{2}, RMSE and NRMSE = RMSE/mean PDI.`,
 eqs: [EQ('F1_{k} = 2 P_{k} R_{k} / (P_{k} + R_{k});   macro-F1 = (1/6) Σ_{k} F1_{k};   RMSE = √[Σ (y − ŷ)^{2} / n]', 'e:o2met')],
 need: `Same metrics on the same held-out replications for every configuration.`,
 why: `Macro-F1 weights the six grades equally, necessary with 32–130 plot-dates per grade (Sokolova and Lapalme, 2009; Lv et al., 2023); kappa corrects for chance (Cohen, 1960); ±1-grade accuracy shows whether errors are only between neighbouring grades, which is expected because grades are cuts of a continuous severity; NRMSE is used because relative error is undefined for PDI = 0 (Liu et al., 2024).`,
 papers: [`Liu et al. (2024); Feng et al. (2022): R² and RMSE for disease index.`, `Tian et al. (2021): overall accuracy; Lv et al. (2023): macro-F1 for severity classes.`, `Mandal et al. (2023): adjacent blast grades on the 0–9 scale hard to separate; RPD for regression.`],
 alts: TAB('o2alt4', [['Alternative', 'How it works / used by', 'Why not used here'], ["McNemar's test", 'Compares two classifiers on the same samples (Dietterich, 1998)', 'Optional for the final pair of models'], ['Matthews correlation coefficient', 'Balanced single score (Chicco and Jurman, 2020)', 'Kappa and macro-F1 are more common in the papers'], ['RPD', 'SD / RMSE (Mandal et al., 2023)', 'Reported as an extra if asked'], ['Weighted kappa', 'Penalises distant grade errors more (Cohen, 1968)', '±1-grade accuracy is simpler to explain']], [2300, 3700, 3306], 'Alternatives for O2 Tier 4.', 16),
 how: [`Metrics per held-out replication; mean ± SD over the three folds.`, `Grades derived from predicted PDI (cut-points from the training data) are compared with direct grade classification.`, `Accuracy reported separately for each variety; share of errors in an adjacent grade reported.`],
 mine: `Dummy result for ${DUM2.cm.set}: OA ${DUM2.cm.oa}, kappa ${DUM2.cm.kap}, macro-F1 ${DUM2.cm.mf1}, ±1-grade accuracy ${DUM2.cm.adj}; grades 1 and 3 are hardest (F1 ${DUM2.cm.F1[1]} and ${DUM2.cm.F1[2]}) and almost all errors are between neighbouring grades; PDI R^{2} ${DUM2.cm.r2}, RMSE ${DUM2.cm.rmse} (${T('o2metrics')}, ${F('o2eval')}).`,
 vis: [TAB('o2metrics', [['Grade', 'Precision', 'Recall', 'F1']].concat(['0', '1', '3', '5', '7', '9'].map((g, i) => [g, DUM2.cm.P[i], DUM2.cm.R[i], DUM2.cm.F1[i]])).concat([['Overall', 'OA ' + DUM2.cm.oa + '; kappa ' + DUM2.cm.kap, 'macro-F1 ' + DUM2.cm.mf1, '±1 grade ' + DUM2.cm.adj]]), [2300, 2400, 2300, 2306], 'Dummy per-grade metrics of the best classification model (LORO, simulated data).', 16),
       FIG('o2eval', 'o2_eval.png', 'Dummy confusion matrix of the six grades (a) and observed vs predicted PDI (b).', 540)],
 out: `The best sensor set, fusion approach and model for grade classification and for PDI regression, with confusion matrices and error statistics.`,
 qs: [[`Why macro-F1 and not only accuracy?`, `With unequal grades a model can look accurate while missing grade 9; macro-F1 gives each grade equal weight.`], [`Why report ±1-grade accuracy?`, `Grades are ordered cuts of a continuous severity; confusing 3 with 5 is much less serious than 0 with 9.`], [`Why NRMSE?`, `Relative error divides by observed PDI, which is zero for healthy plots.`]],
 refs: `Cohen (1960); Sokolova and Lapalme (2009); Liu et al. (2024); Lv et al. (2023).` });

TIER({ title: 'O2 Tier 5. Disease maps',
 pos: `After O2 Tier 4 (best models); the practical output of Objective 2.`,
 problem: `Numbers per fold do not show where in the field the disease is or where the models fail.`,
 concept: `The best classification and regression models are applied to every plot of each flight to map the predicted grade, PDI and the absolute error.`,
 need: `Maps are the product a user needs and a check for spatial error patterns.`,
 why: `Plot-level disease-index and error maps were produced by Liu et al. (2024); class maps from hyperspectral indices by Bhattacharya and Chattopadhyay (2013).`,
 papers: [`Liu et al. (2024): plot-level DI and error maps.`, `Bhattacharya and Chattopadhyay (2013): healthy / rot maps from index thresholds.`],
 alts: TAB('o2alt5', [['Alternative', 'How it works / used by', 'Why not used here'], ['Uncertainty maps', 'Class probabilities or quantile regression forests (Meinshausen, 2006)', 'Added if time permits'], ['Kriging', 'Continuous field surface (Oliver and Webster, 1990)', 'Plots are the experimental units']], [2300, 3700, 3306], 'Alternatives for O2 Tier 5.', 16),
 how: [`Predict each plot of the held-out replication with the best model of each task; map grade, PDI and |error| for each flight.`],
 mine: `One set of maps per flight date for the 72 plots (${F('o2maps')}).`,
 vis: [FIG('o2maps', 'o2_maps.png', 'Dummy maps for one flight: observed grade, predicted grade and absolute PDI error.', 560)],
 out: `Grade, PDI and error maps for every flight.`,
 qs: [[`What do the error maps show?`, `Whether errors are random or concentrated, for example in one variety or near field edges.`]],
 refs: `Liu et al. (2024); Bhattacharya and Chattopadhyay (2013).` });

TIER({ title: 'O2 Tier 6. Independent validation',
 pos: `Last tier of Objective 2; uses the final models refitted on all IARI data.`,
 problem: `Cross-validation within one experiment cannot show whether the models transfer to another site, varieties and farmers' management.`,
 concept: `The final models are tested on data never used for development: the IIRMR Bharatpur experiment and adjoining farmers' fields, scored with the same protocol.`,
 need: `It measures transferability, the main question for any operational use.`,
 why: `Validation on a separate experiment is the strongest test (Feng et al., 2022); feature sets and models may not transfer between scales or sites (Bohnenkamp et al., 2019).`,
 papers: [`Feng et al. (2022): independent experiment as validation set.`, `Tian et al. (2021); Mustafa et al. (2023): two seasons.`, `Bohnenkamp et al. (2019): selected features did not transfer between scales.`],
 alts: TAB('o2alt6', [['Alternative', 'How it works / used by', 'Why not used here'], ['Domain adaptation', 'Adjust the model to a new site (Tuia et al., 2016)', 'Used only if the transfer loss is large'], ['Multi-season validation', 'Second season (Tian et al., 2021; Mustafa et al., 2023)', 'Depends on project time']], [2300, 3700, 3306], 'Alternatives for O2 Tier 6.', 16),
 how: [`Stage 1: Bharatpur experiment; stage 2: farmers' fields; same grading key and PDI.`, `Same metrics as O2 Tier 4 and the loss relative to LORO.`],
 mine: `${T('o2indep')} shows the reporting format with dummy values.`,
 vis: [TAB('o2indep', [['Dataset', 'macro-F1 (6 grades)', '±1-grade accuracy', 'R² (PDI)', 'RMSE (PDI %)'], ['IARI LORO (mean ± SD)', DUM2.cm.mf1 + ' ± 0.04', DUM2.cm.adj, DUM2.cm.r2 + ' ± 0.02', DUM2.cm.rmse + ' ± 0.6'], ['Bharatpur experiment', '0.64', '0.95', '0.84', '8.9'], ["Farmers' fields", '0.58', '0.92', '0.78', '10.6']], [2700, 1700, 1700, 1500, 1706], 'Dummy reporting format for independent validation.', 16)],
 out: `Accuracy at Bharatpur and in farmers' fields and the size of the transfer loss.`,
 qs: [[`What if accuracy drops at Bharatpur?`, `It is expected; I report the loss and, if needed, recalibrate with a few local plots.`]],
 refs: `Feng et al. (2022); Bohnenkamp et al. (2019).` });
K.push(BOX('How Objective 2 is satisfied:', `Six-grade classification and PDI regression are modelled with each sensor and four combinations, using ML-SFFS fusion and DNN fusion; O2 Tier 4 identifies the best sensor set, fusion and model, O2 Tier 5 maps the disease and O2 Tier 6 tests transferability.`, 'FCE4EC', 'AD1457'));

// ======================= 10 OBJECTIVE 3 =======================
K.push(H1('10. Objective 3: Pre-symptomatic prediction'));
K.push(P(`**Objective 3 (ORW):** to predict white rust before visible symptoms. The task is binary (healthy vs later-infected) because every plot is grade 0 before symptoms. ${F('o3flow')} shows the four tiers; they reuse the Tier 1 features and the selection and model chain of Objective 2.`));
K.push(...fig2('o3flow', 'o3_flow.png', 'Flow chart of Objective 3.', 480));

TIER({ title: 'O3 Tier 1. Pre-symptomatic samples and labels',
 pos: `Uses the flights before visible symptoms (Tier 0) and the later grades; before O3 Tier 2.`,
 problem: `Before symptoms every plot is grade 0 and PDI = 0, so the true state of an inoculated plot is unknown at the time of the flight; wrong labels are the main risk.`,
 concept: `The label comes from the future: control plots are healthy, and an inoculated plot is "infected" only if symptoms later appear on that plot (retrospective labelling).`,
 need: `Every later tier of Objective 3 depends on these labels.`,
 why: `Retrospective labelling was used for asymptomatic rice blast by Tian et al. (2021) and fits a field trial where infection cannot be confirmed at flight time.`,
 papers: [`Tian et al. (2021): inoculated sample labelled infected only if symptoms later appeared.`, `Zhu et al. (2017); Terentev et al. (2023): days after inoculation in controlled experiments.`],
 alts: TAB('o3alt1', [['Alternative', 'How it works / used by', 'Why not used here'], ['Days after inoculation', 'Time since inoculation as label (Zhu et al., 2017; Terentev et al., 2023)', 'Field infection is not synchronous'], ['Pathogen quantification', 'qPCR of leaf samples before symptoms (Zhang et al., 2024)', 'Destructive and costly for 72 plots × dates; optional subsample']], [2300, 3700, 3306], 'Alternatives for O3 Tier 1.', 16),
 how: [`Pool all pre-symptomatic dates of the 8 flights (72 plots × number of pre-symptomatic dates; e.g. 2 dates = 144 plot-dates).`, `Inoculated plots that never show symptoms (e.g. a resistant variety) are excluded from the infected class and reported separately.`],
 mine: `Per pre-symptomatic date: 36 healthy and up to 24 infected plots; with 2 such dates, 72 healthy and up to 48 infected plot-dates (${T('o3presym')}). The sample is small, so only simple models with few features are used.`,
 vis: [TAB('o3presym', [['Group', 'Plots', 'Plot-dates (2 pre-symptomatic dates)', 'Label'], ['Controls', '36', '72', 'Healthy'], ['Inoculated, symptoms later', 'up to 24', 'up to 48', 'Infected'], ['Inoculated, no symptoms', 'about 12', 'about 24', 'Excluded, reported separately']], [3300, 1400, 2400, 2206], 'Expected pre-symptomatic class sizes (the number of pre-symptomatic dates is fixed by when symptoms appeared).', 16)],
 out: `A labelled pre-symptomatic table with class counts.`,
 qs: [[`How can you label a plot that looks healthy?`, `By what happens later: it is infected only if symptoms appear on that plot (Tian et al., 2021).`]],
 refs: `Tian et al. (2021); Zhu et al. (2017).` });

TIER({ title: 'O3 Tier 2. Pre-symptomatic features',
 pos: `After O3 Tier 1 (labels), using the Tier 1 feature tables of all sensors; before O3 Tier 3.`,
 problem: `Early changes are small and may involve different features (temperature, PRI, water indices) than visible disease, so the DSF pools of Objective 1 cannot simply be reused.`,
 concept: `Features that already differ between healthy and later-infected plots are found with a **t-test** and the **percentage difference** of the means; **Boruta** then selects the pre-symptomatic DSF pool of each sensor.`,
 need: `It gives the inputs of the early-warning models.`,
 why: `A PDI scalogram is impossible (PDI = 0), so a two-group test is used, as for asymptomatic rice blast (Tian et al., 2021); Boruta was used for asymptomatic Fusarium head blight (Mustafa et al., 2023). Thermal and water-related features can change before symptoms (Mahlein et al., 2019; Zhang et al., 2024); the SWIR water indices of HS Tier 1 are therefore included.`,
 papers: [`Mustafa et al. (2023): Boruta for asymptomatic Fusarium head blight.`, `Mahlein et al. (2019): pigment indices (PSSRa/b) separated infected spikelets 3 days after inoculation.`, `Zhang et al. (2024): water (1400 nm) and 750 nm bands drove pre-symptomatic detection (1400 nm is removed in UAV data; 1240–1660 nm water indices are used instead).`],
 alts: TAB('o3alt2', [['Alternative', 'How it works / used by', 'Why not used here'], ['Chlorophyll-fluorescence parameters', 'Photosynthetic efficiency (Mahlein et al., 2019)', 'No fluorescence sensor on the UAV'], ['Change relative to control plots', 'Difference from controls on each flight (Nguyen et al., 2023)', 'Used as a check of the t-test result'], ['Mann–Whitney U test', 'Rank test for two groups (Mann and Whitney, 1947)', 'Used only for clearly non-normal features']], [2400, 3600, 3306], 'Alternatives for O3 Tier 2.', 16),
 how: [`t-test and % difference from healthy for every Tier 1 feature; Boruta per sensor → pre-symptomatic DSF pools.`],
 mine: `The dummy example (${F('o3presymf')}a) ranks thermal features highest, as expected if transpiration changes first.`,
 vis: [FIG('o3presymf', 'o3_presym.png', 'Dummy pre-symptomatic differences from healthy plots (a) and ROC curves of pre-symptomatic models (b).', 540)],
 out: `Pre-symptomatic DSF pools for each sensor.`,
 qs: [[`Which sensor do you expect to work earliest?`, `Thermal and hyperspectral, because transpiration, water and pigments can change before pustules appear.`]],
 refs: `Tian et al. (2021); Mustafa et al. (2023); Mahlein et al. (2019).` });

TIER({ title: 'O3 Tier 3. Pre-symptomatic classification',
 pos: `After O3 Tier 2; its best model produces the risk maps of O3 Tier 4.`,
 problem: `Objective 3 asks whether white rust can be predicted before symptoms and with which sensors.`,
 concept: `Healthy vs later-infected plots are classified with each sensor set (S1–S8) using the VIF → ML-SFFS chain of O2 Tier 1 and SVM, RF and k-NN.`,
 need: `It gives the early-warning model and its reliability.`,
 why: `ML-SFFS with SVM, RF and k-NN detected asymptomatic rice blast and wheat head blight (Tian et al., 2021; Mustafa et al., 2023). DNNs are not used because the pre-symptomatic set (about 144 plot-dates from 72 plots) is far too small.`,
 papers: [`Tian et al. (2021): SVM-SFFS > 65% for asymptomatic rice blast.`, `Mustafa et al. (2023): 87.04% for asymptomatic Fusarium head blight; Lv et al. (2023): SVM 87.1% asymptomatic.`, `Zhu et al. (2017): up to 95% at 48 h; Terentev et al. (2023): SVM 97–100% from 4 days (controlled conditions).`],
 alts: TAB('o3alt3', [['Alternative', 'How it works / used by', 'Why not used here'], ['Anomaly detection', 'Model trained on healthy plots only (Liu et al., 2008)', 'Optional if infected samples are very few'], ['LSTM on time series', 'Sequence model of feature trajectories (Hochreiter and Schmidhuber, 1997)', 'Only 1–3 pre-symptomatic dates']], [2300, 3700, 3306], 'Alternatives for O3 Tier 3.', 16),
 how: [`S1–S8; LORO validation; class weights; metrics: sensitivity, specificity, OA, kappa, F1 and ROC-AUC (Fawcett, 2006).`],
 mine: `In the dummy example (${F('o3presymf')}b) HS + TIR gives the highest AUC.`,
 vis: [],
 out: `The best early-warning sensor set and model with sensitivity and specificity.`,
 qs: [[`Why report sensitivity and specificity?`, `Sensitivity is how many infected plots are found; specificity is how many healthy plots are correctly left alone; both matter for spraying decisions.`]],
 refs: `Tian et al. (2021); Mustafa et al. (2023); Fawcett (2006).` });

TIER({ title: 'O3 Tier 4. Risk maps',
 pos: `After O3 Tier 3; final output of Objective 3.`,
 problem: `An early-warning result is useful only if it shows where to act.`,
 concept: `The predicted probability of infection of each plot is mapped for each pre-symptomatic flight.`,
 need: `It turns the model into a spatial early-warning product.`,
 why: `Plot-level mapping follows Liu et al. (2024); combining spectral data with weather-based risk follows the multi-stage scheme of Bhattacharya and Chattopadhyay (2013).`,
 papers: [`Liu et al. (2024): plot-level maps of model output.`, `Bhattacharya and Chattopadhyay (2013): weather-based outbreak conditions combined with spectral discrimination.`],
 alts: TAB('o3alt4', [['Alternative', 'How it works / used by', 'Why not used here'], ['Weather-based risk model', 'Outbreak conditions from weather (Bhattacharya and Chattopadhyay, 2013)', 'Complementary; can be combined later'], ['Kriging of probabilities', 'Continuous surface (Oliver and Webster, 1990)', 'Plots are the units']], [2300, 3700, 3306], 'Alternatives for O3 Tier 4.', 16),
 how: [`Class probabilities of the best model mapped plot by plot.`],
 mine: `One risk map per pre-symptomatic flight (${F('o3risk')}).`,
 vis: [FIG('o3risk', 'o3_risk.png', 'Dummy pre-symptomatic risk map.', 400)],
 out: `Plot-wise infection-probability maps.`,
 qs: [[`How would a farmer use the risk map?`, `To inspect and spray high-risk plots first, before the disease is visible.`]],
 refs: `Liu et al. (2024); Bhattacharya and Chattopadhyay (2013).` });
K.push(BOX('How Objective 3 is satisfied:', `The pre-symptomatic models show whether, and with which sensors, white rust can be predicted before symptoms; the risk maps show where infection is developing.`, 'F3E5F5', '6A1B9A'));

// ======================= 11 SUMMARY =======================
K.push(H1('11. Summary of the methodology'));
K.push(...tab2('summary', [
  ['Tier', 'Method', 'Output', 'Main references'],
  ['Tier 0', 'RBD experiment; grades 0, 1, 3, 5, 7, 9 (Conn key) and PDI; calibration; crop mask; endmember spectrum; LORO', 'Labelled plot-date table', 'Conn 1990; Gomez 1984'],
  ['Tier 1 (all sensors)', 'HS 481 bands, FD, SD, red-edge, 48 indices (incl. 9 SWIR disease indices); MS; RGB; TIR', 'Feature tables', 'Guo 2021; Apan 2004; Feng 2022'],
  ['HS Tier 2', 'Correlation scalogram + ReliefF; one band per region', 'Robust bands', 'Shukla 2024; Mahlein 2013'],
  ['HS Tier 3', 'White Rust Index', 'WRI', 'Mahlein 2013'],
  ['M1 tiers', 'One-way ANOVA + Tukey HSD; Pearson r; physiology', 'Responding features', 'Gomez 1984; Liu 2024'],
  ['M2 + M3 tiers', 'VIF; stepwise CDA per sensor (HS two steps)', 'Separability of six grades', 'Bhattacharya 2013'],
  ['M4 tiers; cross-sensor', 'Boruta; DSF correlation; optional combined CDA', '8 DSF pools', 'Mustafa 2023; Mahlein 2019'],
  ['O2 Tier 1', 'VIF < 10 → ML-SFFS', 'OFC per model', 'Tian 2021; Mustafa 2023'],
  ['O2 Tier 2', 'SVM/SVR, RF/RFR, k-NN, PLSR, DNN-F1, DNN-F2', 'Tuned models', 'Maimaitijiang 2020'],
  ['O2 Tier 3', 'S1–S8; ML-SFFS fusion and DNN fusion', 'Best sensor set', 'Mustafa 2023; Feng 2022'],
  ['O2 Tiers 4–6', 'OA, kappa, macro-F1, ±1 grade; R², RMSE; maps; Bharatpur validation', 'Best model, maps', 'Liu 2024; Feng 2022'],
  ['O3 Tiers 1–4', 'Retrospective labels; t-test + Boruta; VIF → ML-SFFS → SVM/RF/k-NN; risk maps', 'Early-warning model', 'Tian 2021; Mustafa 2023'],
], [1700, 3900, 1900, 1806], 'Summary of all tiers of the thesis.', 15));
