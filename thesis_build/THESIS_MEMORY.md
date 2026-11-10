# Thesis methodology memory (white rust, UAV multimodal) — decisions so far

Last updated: 10 Nov 2026. Status: methodology agreed step by step; **final PDF not yet produced — make it only when the user asks**.

## 1. User and how to work
- Ph.D. (Agricultural Physics), ICAR-IARI. Thesis: *AI-based multimodal UAV sensing of white rust in mustard*. Preparing for NRSC/SAC (ISRO) interview.
- Wants: scientifically correct, no mistakes, proper references in every step, Word + PDF, figures/flow charts, **simple and easy to present** (no unnecessary statistics), interview-ready answers.
- Every step in the final document uses one template: Position in workflow → Concept → Why needed at this position → Importance and justification → What the reference papers used for this problem → How it is done → How it is used with my data → dummy-data figure/table → Output → Notes (other methods with references) → Interview questions → References.
- End of document: NRSC/SAC Q&A, each answer = concept + "How I solved it" + "How other researchers dealt with it" (with references).

## 2. Data and experiment (facts from the user)
- IARI 2025–26 factorial RBD: inoculation timing G1–G4 (sowings 20 Nov, 30 Nov, 10 Dec, 20 Dec 2025; one inoculation 10 Jan 2026), varieties V1 Varuna (HS), V2 Pusa Vijay (MS), V3 PM 38 (resistant), dose D1 control / D2 1.5 × 10^5 zoosporangia mL^-1; 24 treatments × 3 replications = 72 plots of 3 m × 3 m.
- Sensors: RGB (DJI Phantom), MS (MicaSense RedEdge-MX 475/560/668/717/840 nm), HS (VNIR 400–1000 + SWIR 1000–2500 nm; 481 bands used; SWIR pixel ≈ 36 cm), TIR (FLIR Vue Pro R, 7.5–13.5 µm).
- **8 flight dates, all four sensors each date → 72 × 8 = 576 plot-dates.** Dates before first visible symptoms = pre-symptomatic set (Obj. 3); rest = post-symptomatic (Obj. 1–2). Example used in document: 2 + 6 dates = 144 + 432 plot-dates (real split depends on symptom appearance).
- Independent validation: IIRMR Bharatpur experiment, then farmers' fields (2026–27).
- **Crop mask:** built on the HS image with NDVI > 0.6 AND SAM < 0.3 rad (spectral angle to a reference canopy spectrum; Kruse et al. 1993); the same mask is transferred to RGB, MS and TIR (co-registered with the same GCPs, nearest-neighbour resampling, 1-pixel edge erosion). Written as "both conditions (AND)" — confirm with user if they combine differently.
- **HS plot spectrum:** endmember extraction per plot, 30 endmembers, non-crop endmembers removed, remaining crop endmembers averaged. Non-crop decided only by low NDVI / large spectral angle (soil, shadow, background); chlorotic/pustule endmembers are KEPT (disease signal). Algorithm not yet named by user — document says "e.g. N-FINDR or VCA" (Winter 1999; Nascimento and Bioucas-Dias 2005). **Ask user which algorithm.**
- **Flower pixels: REMOVED from the leaf spectrum**, flower fraction stored as a covariate (DI is leaf-based; yellow petals dominate 500–650 nm; flowering differs with sowing date/variety → confounding; Sulik and Long 2016; Fang et al. 2016). For staghead severity, inflorescence pixels are kept.
- User's ASD mustard leaf spectra (file asd__data_complete_labelled_030326_scored.xlsx; assumed date 3 Mar 2026 — confirm): 648 spectra (108 healthy, 540 diseased). Band redundancy: bands 10 nm apart median r = 0.9997; 50 nm apart 0.993; 349 bands (5 nm) → 18 correlated regions (r ≥ 0.95); first derivatives → 161 regions.

## 3. Tasks and classes
- Objective 1: characterise white rust through multimodal UAV sensing.
- Objective 2 (ORW wording kept; user did not give new wording): detect and discriminate disease severity through AI-based multimodal data fusion.
- Objective 3: predict white rust at the pre-symptomatic stage.
- **Classification: 4 classes — Healthy (DI = 0), Low (0 < DI ≤ 25), Moderate (25 < DI ≤ 50), High (DI > 50).** Healthy is a class, so detection is part of the 4-class task.
- **Regression: DI (%)** in parallel. Pre-symptomatic task: healthy vs later-infected.
- DI = Σ(x·f)/(n·Σf) × 100, 0–6 leaf scale (Liu et al. 2024).
- All dates pooled (no date effect modelled).

## 4. Final step list (agreed)
Common: A1 experiment; A2 DI and classes; A3 acquisition + pre-processing (calibration, HS mask NDVI>0.6 & SAM<0.3, mask transfer, endmember plot spectrum, flowers removed); A4 pooled table + leave-one-replication-out (LORO) validation, selection/tuning inside training replications (nested).

Objective 1:
- 1.1 Features: HS 481 bands + FD + SD + REP/Dr/SDr + **39 indices** (all ORW slide indices with corrected formulas + MSR, GI, RR, PSSRb/c, HI, DWSI-1, DWSI-4, ROTI); MS 5 bands + 12 indices + 40 GLCM; RGB 24 GLCM + HSV + VF + CH (29); TIR CT, CTD, CTR (kelvin), NRCT, MTD + 8 GLCM (13).
- 1.2 Univariate: **one-way ANOVA + Tukey HSD** across 4 classes; **Pearson r** with DI; physiology correlation; thermal-vs-water check (CTD vs WI/DWSI-1, RWC). (Kruskal–Wallis/Spearman only as notes.)
- 1.3 HS band level: **correlation scalogram (R, FD, SD vs DI) + ReliefF (4 classes)**.
  - Candidates: scalogram p < 0.01 & top 5% |r|; ReliefF top 5% weights (k = 10, same-plot neighbours excluded).
  - **One band per correlated region applies to BOTH lists**: regions from band-to-band correlation matrix (run of neighbouring bands with r ≥ 0.95 to region's first band); keep highest |r| / highest weight per region.
  - **Combining**: common region (same region or ±10 nm) = robust white-rust band → both tasks; scalogram-only → DI regression pool; ReliefF-only → classification pool. Do NOT keep intersection only (would lose task-specific bands); Boruta/VIF/ML-SFFS remove the rest.
  - **Vegetation indices are NOT screened in Step 1.3** (it is only for raw bands R/FD/SD). The 39 indices, red-edge parameters and WRI go directly to Step 1.2 (ANOVA, r), Step 1.5 (second discriminant step) and Step 1.6 (Boruta, with the robust bands).
  - Why not alternatives: separability scalogram (Tian 2021) needs two well-separated classes; SPA (Zhu 2017) picks low-collinearity bands, not disease response, depends on start band, tied to MLR; PCA loadings follow overall variance (structure, illumination, flowering); PLSR loadings subjective peak picking, Shukla's bands not linked to known absorption features. Scalogram = Shukla 2024's own first step (same crop); ReliefF used by Mahlein 2013, Meng 2020 (3-level severity), Lv 2023.
- 1.4 White Rust Index: ND(λ1,λ2) + w·R(λ3), w ∈ {−1,−0.5,0,0.5,1}; 450–950 nm at 6 nm, ReliefF top 25% of bands and NDs, ≥ 50 nm apart (Mahlein 2013); balanced accuracy healthy vs diseased; repeat with SWIR; keep better.
- 1.5 Class discrimination: **two-step stepwise LDA (Stage III, Bhattacharya and Chattopadhyay 2013)** — step 1 robust bands, step 2 indices + WRI (after VIF); output canonical correlation, Wilks' lambda (one sentence), score plot, LORO accuracy. JM only in notes.
- 1.6 DSF pools: **Boruta** per sensor for classification and regression → 8 pools; cross-sensor correlation matrix.

Objective 2:
- 2.1 VIF < 10 → ML-SFFS (criterion macro-F1 / RMSE; ≤ 10 features; grouped 4-fold inner CV); OFC = best score, or a smaller subset within 0.01; repeated 10×, keep features chosen in most runs.
- 2.2 Six models: SVM/SVR, RF/RFR, k-NN, PLSR (regression only), DNN-F1, DNN-F2; class weights; DNNs kept very small (≈290 training plot-dates per fold).
- 2.3 S1 RGB, S2 MS, S3 HS, S4 TIR, S5 RGB+TIR, S6 MS+TIR, S7 HS+TIR, S8 all; fusion = ML-SFFS feature-level fusion (pooled) + DNN-F1 + DNN-F2 (sensor-wise ML-SFFS dropped for simplicity). 80 model configurations.
- 2.4 Metrics: OA, kappa, per-class F1, macro-F1, confusion matrix; R², RMSE, NRMSE; classes from predicted DI vs direct; accuracy per variety; share of errors in adjacent class (± 1).
- 2.5 Maps (class, DI, error). 2.6 Independent validation (Bharatpur, farmers' fields).

Objective 3: 3.1 labels (control = healthy; inoculated = infected only if symptoms appear later; non-symptomatic inoculated e.g. PM 38 excluded; Tian 2021); 3.2 t-test + % difference from healthy, Boruta; 3.3 VIF → ML-SFFS → SVM, RF, k-NN for S1–S8 (no DNN), sensitivity/specificity/AUC; 3.4 risk maps.

## 5. Class-overlap handling (Section 1.2 of final document)
Classes are cuts of continuous DI → neighbours overlap (literature: Meng 2020 70% severity vs 87% detection; Lv 2023 81.8% vs 93.1%; Mandal 2023 adjacent blast levels inseparable). Measures: careful scoring (5 points, same scorer, explicit limits; Bock 2010); DI-based screening (scalogram); ReliefF for overlapping classes; disease-specific WRI (Mahlein 2013; Meng 2020); multivariate LDA (Bhattacharya 2013; Zhang 2012a); sensor/feature fusion (Lv 2023; Feng 2022; Mahlein 2019); soft-margin SVM, RF, k-NN with class weights; DI regression alongside; per-class F1 and adjacent-class error reporting.

## 6. Paper facts to remember (checked against the PDFs)
- Shukla 2024: abstract regions (493–497, 509–515, 690–714, 717–721, 752–756 nm) differ from results Table 4 (483–487, 509–515, 690–714, 719–723 nm) — quote Table 4. Key bands PCA 500/679/746/979, PLSR 491/679/746/979; PLSR val r² 0.71, RMSE 0.66. No formal discriminant analysis (discrimination = correlation + PCA/PLSR loadings).
- Bhattacharya and Chattopadhyay 2013 (SAC-ISRO + DRMR): Stage III two-step stepwise canonical discriminant analysis; 25 Hyperion bands (canonical corr > 0.5); 224 new + 30 published indices; ROTI = R1175/(R1982+R691) recommended; DWSI-1/DWSI-4 R² inconsistent between text and figure (0.87/0.93); R² from 5 group means (optimistic); thresholds 1.25 < DRI ≤ 3.5, 0 < ROTI ≤ 1.5; indirect validation (fractional cover 2005 vs 2007). Also "single bands out of closely located bands".
- Mahlein 2013: 6 nm resolution and 50 nm minimal distance because neighbouring wavelengths are highly correlated.
- Tian 2021: top 5% + one representative feature per common region; VIF < 10 → ML-SFFS.

## 7. Files and how to rebuild
- Build sources: `thesis_build/` in this repo (`final/f_body.js` content, `final/f_isro.js` ISRO Q&A, `final/f_fig.py` dummy figures, `final/f_assemble.py` assembler; uses `thesis/t_docx.js` for helpers and reference pool and `uav/u10_docx.js` for index tables).
- Rebuild: `cd thesis_build/final && python3 f_fig.py && python3 f_assemble.py && NODE_PATH=/opt/node22/lib/node_modules node f_docx.js` → `thesis_build/outputs/White_rust_final_methodology.docx`; then `python3 ../satmet/to_pdf.py <docx> <pdf>` (LibreOffice) for the PDF with updated TOC.
- Earlier, larger documents (thesis edition, ML guide, SIF/FLEX, chlorophyll fluorescence) were made in the earlier session scratchpad and are superseded by the final methodology.

## 8. Pending / to confirm
- Produce the final PDF + Word only when the user says so.
- Confirm endmember algorithm, NDVI/SAM combination (AND), ASD file date, and whether Objective 2 wording changes.
