"""Flow charts for Objectives 2 and 3 and the overall workflow."""
import os
from o1_flow import chart, COL, FILL

# ---------------- flow charts ----------------
COL.update({'O2': '#AD1457', 'O3': '#6A1B9A', 'M': '#1E3A1F'}); FILL.update({'O2': '#FCE4EC', 'O3': '#F3E5F5', 'M': '#EEF3E8'})
chart('O2', 'Objective 2: six-grade classification and PDI regression by multimodal fusion', [
 ('O2 Tier 1  Optimum feature combination', ['Input: DSF pools of Objective 1 (per sensor, classification and regression)', 'VIF < 10, then ML-SFFS for each model (criterion macro-F1 or RMSE)', 'Inside each training replication only; repeated 10 times, frequent features kept'], 'Tian 2021; Mustafa 2023', ['Optimum feature combination', '(OFC) per sensor set, task, model']),
 ('O2 Tier 2  Six models and tuning', ['SVM/SVR, RF/RFR, k-NN, PLSR (regression only), DNN-F1, DNN-F2', 'Grid search in grouped inner CV; class weights for unequal grades', 'DNNs kept very small (about 1 000 weights); several random seeds'], 'Maimaitijiang 2020', ['Tuned models']),
 ('O2 Tier 3  Single sensors vs fusion', ['S1 RGB, S2 MS, S3 HS, S4 TIR; S5 RGB+TIR, S6 MS+TIR, S7 HS+TIR, S8 all', 'ML-SFFS fusion (concatenated DSFs) and DNN fusion (F1 input, F2 intermediate)', '80 configurations, each tested on the three held-out replications'], 'Mustafa 2023; Feng 2022', ['Performance of every', 'sensor set and fusion']),
 ('O2 Tier 4  Evaluation', ['Grades: OA, kappa, per-grade F1, macro-F1, ±1-grade accuracy, confusion matrix', 'PDI: R², RMSE, NRMSE; grades from predicted PDI vs direct grades', 'Per variety; share of errors in the adjacent grade'], 'Sokolova 2009; Liu 2024', ['Best sensor set, fusion', 'and model per task']),
 ('O2 Tier 5  Disease maps', ['Best models applied to every plot of each flight', 'Maps of predicted grade, PDI and absolute error'], 'Liu 2024', ['Grade, PDI and error maps']),
 ('O2 Tier 6  Independent validation', ['Final models refitted on all IARI data', 'Stage 1 IIRMR Bharatpur experiment; stage 2 farmers\' fields', 'Same metrics; transfer loss relative to LORO'], 'Feng 2022', ['Transferability']),
], 'o2_flow.png', foot='Best early-season sensors and features are passed to Objective 3 (pre-symptomatic prediction)')
chart('O3', 'Objective 3: pre-symptomatic prediction of white rust', [
 ('O3 Tier 1  Samples and labels', ['Flights before visible symptoms (grade 0 everywhere)', 'Label from the future: infected only if symptoms later appear on that plot', 'Inoculated plots that never show symptoms excluded, reported separately'], 'Tian 2021', ['Labelled healthy vs', 'later-infected table']),
 ('O3 Tier 2  Pre-symptomatic features', ['t-test and % difference from healthy plots for every Tier 1 feature', 'Boruta per sensor (healthy vs later-infected)'], 'Mustafa 2023; Mahlein 2019', ['Pre-symptomatic DSF pools']),
 ('O3 Tier 3  Pre-symptomatic classification', ['S1–S8; VIF -> ML-SFFS -> SVM, RF, k-NN (no DNN: sample too small)', 'LORO; class weights; sensitivity, specificity, kappa, ROC-AUC'], 'Tian 2021; Mustafa 2023', ['Best early-warning', 'sensor set and model']),
 ('O3 Tier 4  Risk maps', ['Probability of infection of each plot mapped for each pre-symptomatic flight'], 'Liu 2024', ['Plot-wise risk maps']),
], 'o3_flow.png', foot='Early-warning product: where to scout and spray before white rust is visible')
chart('M', 'Overall workflow of the thesis', [
 ('Tier 0  Common inputs', ['RBD field experiment (72 plots, 3 replications); 8 flights with HS, MS, RGB, TIR', 'Calibration; HS crop mask (NDVI > 0.6 and SAM < 0.3) transferred to all sensors', 'Endmember plot spectrum; grades 0, 1, 3, 5, 7, 9 (Conn key) and PDI; LORO'], 'Conn 1990', ['Labelled plot-date table', 'with features of 4 sensors']),
 ('Objective 1  Characterisation (sensor tiers)', ['HS Tiers 1–6: features, scalogram + ReliefF, WRI, ANOVA, CDA, Boruta', 'MS, RGB, TIR Tiers 1–4: features, ANOVA, CDA, Boruta; cross-sensor tier'], 'Bhattacharya 2013', ['Responding features, WRI,', '8 DSF pools']),
 ('Objective 2  Classification and regression by fusion', ['O2 Tiers 1–6: VIF -> ML-SFFS, six models, S1–S8 fusion,', 'evaluation, maps, independent validation'], 'Maimaitijiang 2020', ['Best sensor set and model', 'for grades and PDI']),
 ('Objective 3  Pre-symptomatic prediction', ['O3 Tiers 1–4: retrospective labels, early features, classification, risk maps'], 'Tian 2021', ['Early-warning model', 'and risk maps']),
], 'o_master.png', foot='Outputs: white-rust features and index, severity maps, early-warning maps; link to satellite missions')

print('ok')
