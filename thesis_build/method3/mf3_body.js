K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1100, after: 200 }, children: [new TextRun({ text: 'AI-based multimodal UAV sensing of white rust in mustard', font: FONT, size: 44, bold: true, color: '1E3A1F' })] }));
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [new TextRun({ text: 'Research methodology for the field experiment, season 2026-27 (revision 5): objectives → activities → steps', font: FONT, size: 28, color: '2C5F2D' })] }));
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: 'Hyperspectral, multispectral, red–green–blue and thermal unmanned aerial vehicle (UAV) data | 15 sensor sets | feature-level fusion | machine learning, feature-fusion neural networks, DT-EDNet, EfficientNet, ResNet18 and ConvNeXt V2', font: FONT, size: 21, italics: true })] }));
K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 }, children: [new TextRun({ text: 'Animesh Panda (Roll No. 13098) | Ph.D. Agricultural Physics | ICAR-Indian Agricultural Research Institute, New Delhi', font: FONT, size: 20 })] }));
K.push(BOX(`How to read this document.`, `The work is organised in three levels. (1) Six common activities (A to F) prepare the data once for all objectives. (2) Each objective is divided into activities (for example Activity 1.2). (3) Each activity is divided into numbered steps (for example Step 1.2.3). Every step has a heading and the same layout: purpose, input, output, procedure and supporting studies. Every technique used in a step is described in a method card that gives its principle, the problem it solves, its specification, its hyper-parameters and how they are tuned, the data on which it works well, why it was selected and its references. Flow charts are given for every objective and for the main activities, and small dummy datasets are used to show how each calculation works. Full names are written with their abbreviation in brackets.`, 'EEF3E8', '2C5F2D'));
K.push(BOX(`What is new in this revision.`, `(1) The methods of the DT-EDNet study on rice blast (Ma et al., 2026) are included: effective wavelength ranges from normalised difference and ratio spectral index maps, optimal wavelengths by SHAP-CARS, vegetation index selection by ReliefF, texture from principal-component images selected by minimum redundancy maximum relevance (mRMR), the Tri-band Texture Fusion Index (TTFI) and the DT-EDNet network with EfficientNet, ResNet18 and ConvNeXt V2 as comparison networks for the post-symptomatic data. (2) One feature-selection method is used for each type of feature. (3) The second derivative is not used. (4) A separate activity on normalisation and data preparation is added. (5) The endmember extraction is described step by step. (6) Each technique has a method card. (7) Covariates are days after inoculation, variety, inoculation timing, growth stage and weather; they are used for a covariate-only baseline and for sensor + covariate models, not as disease features. (8) Healthy plots are rotated across the folds so that every fold contains healthy plots of all three varieties. (9) SHAP-CARS standardises the bands and always keeps the red-edge first derivative. (10) All models, including DT-EDNet and the comparison networks, are built for every single camera and every camera combination, for classification and regression.`, 'FFF6E0', 'C98A00'));
K.push(BOX(`Updates in revision 5.`, `(1) Field calendar: sowing on 19 and 26 November and 3 and 10 December 2026 (7-day interval), inoculation on 30 December 2026 (crop age 41, 34, 27 and 20 days), 13 flights from 1 January to 15 March 2027, biochemical and biophysical sampling on 7 and 18 January, 8 February and 1 March. (2) Severity: disease index survey at the centre and four corners of every subplot (DI classes 0, 1, 3, 5, 7, 9; Task C = DI) and staghead severity (Step A3). (3) Objective 1 also characterises the pre-symptomatic stage with 576 samples per camera (Activity 1.8). (4) Bharatpur data are used for independent testing of frozen models, not for validation (Step A7, Activity 2.7). (5) All 48 published hyperspectral indices (39 base + 9 SWIR) and 3 red-edge parameters with formulas and references (Chapter 7). (6) Detailed covariate baseline with interpretable and machine-learning models, plot-block bootstrap and DeLong test (Step 2.5.5). (7) Sensor specifications, two ASD readings per leaf, BBCH vegetative stage 10–49 and a glasshouse pot experiment (Step A9). (8) Expected outcomes (Section 1.5).`, 'E8F4F8', '1F6FB2'));
K.push(new Paragraph({ children: [new PageBreak()] }));
K.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: 'Contents', font: FONT, size: 32, bold: true, color: '1E3A1F' })] }));
K.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-3' }));
K.push(new Paragraph({ children: [new PageBreak()] }));
K.push(H1(`Full names and abbreviations`));
K.push(P(`The text always gives the full name with the abbreviation in brackets. This list is only for quick reference.`));
K.push(...tab2('abbr', [[`Abbreviation`, `Full name`, `Abbreviation`, `Full name`],
[`AdamW`, `adaptive moment estimation with decoupled weight decay`, `MNF`, `minimum noise fraction`],
[`ASD`, `Analytical Spectral Devices field spectroradiometer (leaf spectra)`, `L3, L5, LL`, `3rd and 5th fully expanded leaf from the top; lowest green leaf`],
[`DMSO`, `dimethyl sulfoxide (pigment extraction solvent)`, `IRGA`, `infrared gas analyser (LI-6400 portable gas exchange system)`],
[`LAI`, `leaf area index`, `RWC`, `relative water content`],
[`MSI`, `membrane stability index (the moisture stress index is written in full)`, `FW, TW, DW`, `fresh, turgid and dry weight`],
[`AUC`, `area under the receiver operating characteristic curve`, `mRMR`, `minimum redundancy maximum relevance`],
[`BBCH`, `decimal scale of plant growth stages (Biologische Bundesanstalt, Bundessortenamt und Chemische Industrie)`, `RH`, `relative humidity`],
[`CARS`, `competitive adaptive reweighted sampling`, `MS`, `multispectral`],
[`CBAM`, `convolutional block attention module`, `NDSI`, `normalised difference spectral index`],
[`CWSI`, `crop water stress index`, `NDVI`, `normalised difference vegetation index`],
[`DAI`, `days after inoculation`, `NRCT`, `normalised relative canopy temperature`],
[`DNN-F1, DNN-F2`, `deep neural network with input-level (F1) or intermediate-level (F2) feature fusion`, `OW`, `optimal wavelengths`],
[`DT-EDNet`, `Dual Transformer Early Detection Network`, `PCA`, `principal component analysis`],
[`DTG`, `Dual Transformer Group`, `PLS, PLS-DA, PLSR`, `partial least squares; discriminant analysis; regression`],
[`GLCM`, `grey-level co-occurrence matrix`, `PPI`, `pixel purity index`],
[`HS`, `hyperspectral`, `RF`, `random forest`],
[`k-NN`, `k-nearest neighbours`, `RGB`, `red–green–blue (camera)`],
[`KTB`, `Kernel Transformer Block`, `RMSE`, `root-mean-square error`],
[`LORO`, `leave-one-replication-out (cross-validation)`, `RPD`, `ratio of performance to deviation`],
[`MCCV`, `Monte Carlo cross-validation`, `RSI`, `ratio spectral index`],
[`MHSA`, `multi-head self-attention`, `SAM`, `spectral angle mapper`],
[`SE`, `squeeze-and-excitation (attention block)`, `SFFS`, `sequential floating forward selection`],
[`SHAP`, `Shapley additive explanations`, `SVM, SVR`, `support vector machine; support vector regression`],
[`TF`, `texture feature`, `TIR`, `thermal infrared`],
[`TTB`, `Token Transformer Block`, `TTFI`, `Tri-band Texture Fusion Index`],
[`UAV`, `unmanned aerial vehicle`, `VI`, `vegetation index`],
[`VIF`, `variance inflation factor`, `WRI`, `White Rust Index`],
[`XGBoost`, `extreme gradient boosting`, `T_{max}, T_{min}`, `daily maximum and minimum air temperature`]], [1500, 3150, 1500, 3156], `Full names of the abbreviations used.`, 16));
K.push(H1(`1. Objectives, data and overall design`));
K.push(H2(`1.1 Background and objectives`));
K.push(P(`White rust, caused by the obligate oomycete Albugo candida, produces white pustules on the leaves, chlorosis and, after systemic infection, distorted inflorescences (staghead) in Indian mustard, and it can reduce yield by 20–60% (Kumar and Kalha, 2005; Saharan et al., 2014). The disease develops under cool and humid weather (Chattopadhyay et al., 2011). Visual scoring is slow and possible only after symptoms appear. Cameras on an unmanned aerial vehicle (UAV) record the changes in pigments, leaf structure, water and temperature that accompany infection, sometimes before symptoms are visible (Mahlein, 2016; Terentev et al., 2022), and combining several cameras usually improves accuracy (Maimaitijiang et al., 2020; Feng et al., 2022).`));
K.push(...tab2('objectives', [[`Objective`, `Question answered`, `Data used`, `Main output`],
[`1. To characterise white rust of mustard through multimodal sensing from a UAV platform`, `Which wavelengths, vegetation indices, texture features and thermal features of each camera respond to white rust severity, does the response change with variety and inoculation timing, and which features already differ before symptoms appear?`, `1920 post-symptomatic and 576 pre-symptomatic subplot samples per camera`, `Optimal wavelengths, White Rust Index, selected indices, Tri-band Texture Fusion Index, the disease-specific feature set of each camera and the pre-symptomatic feature set`],
[`2. To detect and discriminate disease severity of white rust in mustard through AI-based multimodal data fusion`, `How accurately can (a) healthy vs diseased subplots, (b) severity classes and (c) the severity score be predicted by each of the 15 sensor sets with machine learning and deep learning?`, `1920 post-symptomatic subplot samples per camera`, `Best sensor set and model for each task; contribution of each camera; comparison of DT-EDNet with EfficientNet, ResNet18 and ConvNeXt V2; severity maps`],
[`3. To predict white rust at the pre-symptomatic stage using machine learning`, `Can subplots that will develop white rust be separated from healthy subplots before symptoms, and can their later severity be predicted?`, `576 pre-symptomatic subplot samples per camera`, `Pre-symptomatic models; earliest detection day; risk maps`]], [2600, 3000, 1600, 2106], `Objectives, questions, data and outputs.`, 16));
K.push(H2(`1.2 Overall design`));
K.push(P(`All objectives use the same field data and the same preparation. The common activities A to F are carried out once (${F('overall')}). Objective 1 then describes and selects the features of each camera at the post-symptomatic stage and at the pre-symptomatic stage, Objective 2 builds the detection and severity models on the post-symptomatic data and Objective 3 builds the early-warning models on the pre-symptomatic data. A glasshouse pot experiment (Step A9) gives the same responses under controlled conditions.`));
K.push(...fig2('overall', 'g01_overall.png', `Overall workflow. Common activities A–F prepare the data once; each objective is divided into activities and steps.`, 560));
K.push(P(`**Eight rules apply to every activity.** They come from the methodological literature and from the weaknesses reported in recent disease-sensing studies (Ambroise and McLachlan, 2002; Varma and Simon, 2006; Cawley and Talbot, 2010; Roberts et al., 2017; Ma et al., 2026).`));
K.push(NL(`One sample is one subplot on one date. The four subplots of a plot always stay together in the training part or in the test part.`));
K.push(NL(`All cameras are measured on the same vegetation pixels of each subplot (Common Activity C).`));
K.push(NL(`Features are grouped by type, and one selection method is used for each type of feature (Objective 1).`));
K.push(NL(`Every step that uses the severity labels (index search, feature selection, tuning, early stopping) runs inside the training part only.`));
K.push(NL(`All normalisation constants (means, standard deviations, healthy-plot references) are computed on the training part and then applied to the test part.`));
K.push(NL(`Severity increases with time, so every sensor model is compared with a covariate-only model (days after inoculation, variety, inoculation timing, growth stage, weather); a sensor model is useful only if it is better than this baseline.`));
K.push(NL(`The same folds are used for all sensor sets and all models, so that their accuracies are directly comparable.`));
K.push(NL(`Models are validated inside the IARI field (leave-one-replication-out, nested) and then tested once on independent data from research farms and farmers' fields at Bharatpur with frozen models (independent testing, not validation).`));
K.push(H2(`1.3 Dataset`));
K.push(...tab2('dataset', [[`Item`, `Value`],
[`Plots × subplots`, `48 × 4 = 192 subplots in each image`],
[`Cameras`, `4: hyperspectral, multispectral, red–green–blue and thermal`],
[`Images`, `13 flight dates × 4 cameras = 52 images (3 pre-symptomatic + 10 post-symptomatic dates)`],
[`Inoculation and flight dates`, `inoculation 30 Dec 2026; flights 1, 4, 7 Jan (pre-symptomatic; 2, 5, 8 days after inoculation) and 11, 18, 25 Jan, 1, 8, 15, 22 Feb, 1, 8, 15 Mar 2027 (post-symptomatic; 12–75 days after inoculation)`],
[`Post-symptomatic samples per camera`, `1920 (10 dates × 192 subplots; Objectives 1 and 2)`],
[`Pre-symptomatic samples per camera`, `576 (3 dates × 192 subplots; Objective 1 characterisation and Objective 3 prediction)`],
[`Label of every sample`, `disease index (DI, %) of the subplot from leaves graded 0–9 at the centre and four corners on the flight day; DI class 0, 1, 3, 5, 7, 9`],
[`Varieties`, `V1 = PM 26, V2 = Pusa Vijay, V3 = PM 37`],
[`Sowing dates (2026)`, `D1 = 19 Nov, D2 = 26 Nov, D3 = 3 Dec, D4 = 10 Dec (7-day interval; crop age at inoculation 41, 34, 27 and 20 days)`],
[`Glasshouse pot experiment`, `48 pots (36 inoculated + 12 healthy), same varieties, sowing 23 Nov–14 Dec 2026, inoculation 4 Jan 2027 (Step A9)`],
[`Field layout`, `48 m × 24 m; healthy block (12 plots) + 10 m buffer + inoculated block (R1–R3, 36 plots); plots 5 m × 3 m`],
[`Covariates`, `days after inoculation, variety, inoculation timing, growth stage, weather (T_{max}, T_{min}, RH, rainfall)`],
[`ASD leaf spectra`, `3 plants per subplot × leaves L3, L5, LL on every flight date (1728 leaf spectra per date)`],
[`Biochemical and biophysical parameters`, `chlorophyll a and b, carotenoids, anthocyanin, protein, relative water content, membrane stability index, photosynthesis, transpiration, stomatal conductance, leaf area index; 1 designated subplot per plot on 4 dates (1 pre-, 3 post-symptomatic)`],
[`Validation and independent testing`, `validation: IARI field (leave-one-replication-out, nested); independent testing: Bharatpur research farms and farmers' fields with frozen models (natural infection, at least 300 quadrat-dates)`],
[`Sensor sets analysed`, `15 (4 single cameras, 6 pairs, 4 triples, all four)`],
[`Tasks`, `detection (healthy vs diseased), severity classes, severity score`],
[`Time for the analysis`, `6 months`]], [3300, 6006], `Dataset used in this methodology (numbers as recorded by the researcher).`, 17));
K.push(...fig2('dataset', 'g26_dataset.png', `Structure of the dataset: flight dates → cameras → plots → scored subplots, and the two datasets used by the objectives.`, 520));
K.push(H2(`1.4 Main published studies used to build the methodology`));
K.push(P(`Each step was chosen because it was used and tested for crop-disease sensing or for the specific data problem it solves. ${T('literature')} lists the main disease studies; the methodological references are given in every step and method card.`));
K.push(...tab2('literature', [[`Study`, `Crop and disease`, `Sensors`, `What it contributes to this methodology`],
[`Ma et al. (2026)`, `rice; blast`, `UAV hyperspectral`, `effective ranges from NDSI and RSI maps; SHAP-CARS; ReliefF for indices; principal-component texture with mRMR; TTFI; DT-EDNet vs EfficientNet, ResNet18, ConvNeXt V2; module ablation`],
[`Guo et al. (2021)`, `wheat; yellow rust`, `UAV hyperspectral`, `texture from principal-component images; vegetation index + texture fusion; NDVI soil mask; disease index`],
[`Liu et al. (2020)`, `wheat; Fusarium head blight`, `UAV hyperspectral`, `bands, indices and texture as feature groups; univariate area under the curve screening; neural network`],
[`Yu et al. (2021)`, `pine; pine wilt disease`, `UAV hyperspectral + spectrometer`, `red-edge parameters best for the early stage; random forest`],
[`Feng et al. (2022)`, `wheat; powdery mildew`, `hyperspectral + thermal + RGB`, `feature-level fusion of indices, thermal and texture features`],
[`Liu et al. (2024); Liu et al. (2026)`, `wheat; powdery mildew`, `UAV multispectral + thermal; ground to UAV`, `red-edge indices, thermal features and severity maps; a disease-specific index transferred from ground to UAV`],
[`Calderón et al. (2014)`, `opium poppy; downy mildew`, `UAV thermal + multispectral`, `canopy minus air temperature as a normalised thermal feature`],
[`Zheng et al. (2018); Das et al. (2015)`, `wheat yellow rust; rice bacterial leaf blight`, `hyperspectral simulated to Sentinel-2 and LISS-IV`, `disease-specific three-band index; band simulation for satellite up-scaling`],
[`Yuan et al. (2025)`, `rice; bacterial blight`, `UAV + satellite`, `mRMR feature selection; random forest, support vector machine and k-nearest neighbours`],
[`Maimaitijiang et al. (2020)`, `soybean yield`, `UAV RGB + multispectral + thermal`, `deep neural networks with input-level and intermediate-level fusion`],
[`Mahlein et al. (2013); Huang et al. (2014)`, `sugar beet and wheat diseases`, `hyperspectral`, `ReliefF and disease-specific spectral indices`],
[`Tian et al. (2021); Mustafa et al. (2023)`, `rice blast; wheat Fusarium head blight`, `hyperspectral (+ fluorescence)`, `variance inflation factor and floating forward selection; pre-symptomatic stage`],
[`Zhu et al. (2017); Zarco-Tejada et al. (2018)`, `tobacco virus; olive Xylella`, `hyperspectral (+ thermal)`, `pre-symptomatic detection with labels from the later status`],
[`Mahlein et al. (2019)`, `wheat; Fusarium head blight`, `hyperspectral + thermal + fluorescence`, `sensor comparison and earliest detection day`]], [2100, 1700, 1800, 3706], `Main disease studies and what they contribute.`, 15));
K.push(H2(`1.5 Expected outcomes`));
K.push(...tab2('outcomes', [[`Objective`, `Expected outcome`, `Main outputs that support it`],
[`1`, `Sensitive spectral ranges, signatures and indices for the characterisation of white rust of mustard under laboratory/glasshouse and field conditions, across crop stages and disease severity levels, for large-scale application.`, `optimal wavelengths; White Rust Index; selected indices and TTFI; disease-specific and pre-symptomatic feature sets; physiological basis; glasshouse responses`],
[`2`, `The best suitable sensor or fusion of sensors for detection and monitoring of white rust throughout the crop growth stages.`, `accuracy of 15 sensor sets for detection, DI classes and DI; DT-EDNet vs comparison networks; gain over the covariate baseline; maps; independent test at Bharatpur`],
[`3`, `Early, pre-symptomatic detection so that appropriate preventive measures can be taken in time.`, `pre-symptomatic models; earliest detection day; risk maps; physiological changes before symptoms`]], [1100, 4300, 3906], `Expected outcomes of the research.`, 16));
K.push(H1(`2. Common activities (carried out once for all objectives)`));
K.push(P(`The six common activities turn the raw images into clean, normalised feature tables with one row per subplot-date and prepare the validation folds. Each activity is described as a sequence of steps.`));
K.push(...tab2('commonact', [[`Activity`, `Steps`, `Main output`],
[`A. Field experiment, ground truth and datasets`, `A1–A9`, `labelled subplot list (disease index); ASD leaf spectra; covariates; post- and pre-symptomatic datasets; Bharatpur independent test dataset; biochemical and biophysical parameters; glasshouse pot data`],
[`B. Image pre-processing`, `B1–B5`, `calibrated, aligned images on the hyperspectral grid`],
[`C. Endmember extraction and vegetation mask`, `C1–C8`, `endmember library; vegetation mask applied to all cameras`],
[`D. Subplot spectra and feature extraction`, `D1–D8`, `feature table of each camera`],
[`E. Normalisation and data preparation`, `E1–E4`, `normalised and standardised features; class weights`],
[`F. Validation design and tuning`, `F1–F3`, `outer and inner folds; tuning plan; leakage checklist`]], [3500, 1300, 4506], `Common activities and their outputs.`, 17));
K.push(H2(`Activity A – Field experiment, ground truth and datasets`));
K.push(H3(`Step A1 – Experimental design and treatments`));
K.push(...tab2('sa1', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Defines the sources of variation (inoculation timing, variety, replication) so that disease effects can be separated from crop-age and variety effects.`],
[`Input`, `IARI research farm, New Delhi, rabi 2026-27; field 48 m × 24 m (9.4 m healthy block + 10 m buffer + 28.6 m inoculated block); plots 5 m × 3 m with 0.2 m bunds and 2 m channels.`],
[`Output → next step`, `48 plots with known treatment, replication and plot number → subplots (Step A3) and validation folds (Activity F).`]], [2200, 7106], `Step A1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Four sowing dates at 7-day intervals: D1 = 19 November, D2 = 26 November, D3 = 3 December and D4 = 10 December 2026, with one inoculation on 30 December 2026, so the crop is inoculated at four different ages: 41, 34, 27 and 20 days after sowing.`));
K.push(NL(`Three varieties: V1 = PM 26, V2 = Pusa Vijay, V3 = PM 37.`));
K.push(NL(`The 12 treatments (4 × 3) are inoculated in three replications (R1: plots 37–48, R2: plots 25–36, R3: plots 13–24) with a zoosporangial suspension of 1.5 × 10^{5} zoosporangia mL^{−1} (Mishra et al., 2009).`));
K.push(NL(`One uninoculated healthy plot of every treatment (plots 1–12) is sown in a separate healthy block, 10 m away from the inoculated block, so that inoculum does not spread to the controls: 36 inoculated + 12 healthy = 48 plots.`));
K.push(NL(`Each plot carries a code (treatment, replication, plot number) that is stored with every sample.`));
K.push(P(`**Supporting studies.** Staggered sowing or inoculation and healthy controls were used to create severity gradients for wheat yellow rust (Guo et al., 2021), wheat powdery mildew (Feng et al., 2022; Liu et al., 2024) and rice blast (Tian et al., 2021; Ma et al., 2026); a randomised trial with varieties of different resistance was used for wheat rusts by Blasch et al. (2023).`));
K.push(H3(`Step A2 – UAV flights and cameras`));
K.push(...tab2('sa2', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Provides images of four cameras on the same day, each recording a different plant response.`],
[`Input`, `Flight plan; calibration panels; ground control points.`],
[`Output → next step`, `Raw images of the four cameras on every date → pre-processing (Activity B).`]], [2200, 7106], `Step A2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Fly between 11:00 and 14:00 h under clear sky and low wind, at 30 m above the ground, with about 85% forward and 80% side overlap.`));
K.push(NL(`Hyperspectral camera: Headwall co-aligned HP visible–near-infrared and short-wave-infrared imager (400–2500 nm; 483 usable bands from 399 to 2398 nm after quality control, Step B3; ground pixel about 2.2 cm).`));
K.push(NL(`Multispectral camera: MicaSense RedEdge-MX (475, 560, 668, 717 and 840 nm; about 2 cm).`));
K.push(NL(`Red–green–blue camera: DJI camera (about 0.8 cm). Thermal camera: FLIR Vue Pro R, 7.5–13.5 µm (about 3.9 cm).`));
K.push(NL(`Place reflectance panels and ground control points before every flight; record air temperature and relative humidity during the flight.`));
K.push(NL(`Measure ASD leaf spectra (ASD FieldSpec 4) on the same dates (Step A4). Camera specifications are given in ${T('sensors')}.`));
K.push(NL(`Fly on 13 dates: 1, 4 and 7 January 2027 (pre-symptomatic) and 11, 18 and 25 January, 1, 8, 15 and 22 February, 1, 8 and 15 March 2027 (post-symptomatic); all four cameras on every date.`));
K.push(NL(`Survey the disease index of every subplot on the day of the flight (or within one day; Step A3).`));
K.push(P(`**Supporting studies.** The same four camera types were combined for wheat powdery mildew (Feng et al., 2022) and soybean yield (Maimaitijiang et al., 2020); flight protocols with panels and solar-noon windows are reviewed by Aasen et al. (2018); thermal flight practice: Messina and Modica (2020).`));
K.push(...tab2('sensors', [[`Item`, `RGB camera`, `Multispectral camera`, `Thermal camera`, `Hyperspectral camera`, `Leaf spectroradiometer`],
[`Instrument`, `DJI Phantom`, `MicaSense RedEdge-MX`, `FLIR Vue Pro R`, `Headwall co-aligned HP`, `ASD FieldSpec 4`],
[`Spectral bands`, `3 (red, green, blue)`, `5 (blue, green, red, red edge, near infrared)`, `1`, `VNIR + SWIR; 483 usable bands after quality control (Step B3)`, `2151`],
[`Wavelength range`, `R 620–750, G 520–600, B 450–495 nm`, `475, 560, 668, 717, 840 nm`, `7.5–13.5 µm`, `VNIR 400–1000 nm, SWIR 1000–2500 nm`, `350–2500 nm`],
[`Image size (pixels)`, `5472 × 3648`, `1280 × 960`, `640 × 480`, `VNIR 640, SWIR 320 (across track)`, `—`],
[`Focal length`, `8.8 mm`, `5.4 mm`, `13 mm`, `17–25 mm`, `25° field of view (bare fibre); contact probe used`],
[`Radiometric resolution`, `14 bit`, `12 bit`, `14 bit`, `14 bit`, `16 bit`],
[`Ground pixel at 30 m (this study)`, `≈ 0.8 cm`, `≈ 2 cm`, `≈ 3.9 cm`, `≈ 2.2 cm after resampling`, `leaf level`]], [1700, 1400, 1550, 1300, 1900, 1456], `Sensors used on the UAV and on the ground (specifications from the instrument sheets used by the researcher).`, 15));
K.push(...tab2('flights', [[`Flight`, `Date`, `Days after inoculation`, `Period`, `Cameras and scoring`],
[`1`, `1 Jan 2027`, `2`, `pre-symptomatic`, `RGB (DJI Phantom), multispectral (MicaSense RedEdge-MX), thermal (FLIR Vue Pro R), hyperspectral (Headwall co-aligned), ASD leaf spectra, disease index survey`],
[`2`, `4 Jan 2027`, `5`, `pre-symptomatic`, `all four cameras + ASD leaf spectra + disease index survey`],
[`3`, `7 Jan 2027`, `8`, `pre-symptomatic`, `all four cameras + ASD leaf spectra + disease index survey`],
[`4`, `11 Jan 2027`, `12`, `post-symptomatic`, `all four cameras + ASD leaf spectra + disease index survey`],
[`5`, `18 Jan 2027`, `19`, `post-symptomatic`, `all four cameras + ASD leaf spectra + disease index survey`],
[`6`, `25 Jan 2027`, `26`, `post-symptomatic`, `all four cameras + ASD leaf spectra + disease index survey`],
[`7`, `1 Feb 2027`, `33`, `post-symptomatic`, `all four cameras + ASD leaf spectra + disease index survey`],
[`8`, `8 Feb 2027`, `40`, `post-symptomatic`, `all four cameras + ASD leaf spectra + disease index survey`],
[`9`, `15 Feb 2027`, `47`, `post-symptomatic`, `all four cameras + ASD leaf spectra + disease index survey`],
[`10`, `22 Feb 2027`, `54`, `post-symptomatic`, `all four cameras + ASD leaf spectra + disease index survey`],
[`11`, `1 Mar 2027`, `61`, `post-symptomatic`, `all four cameras + ASD leaf spectra + disease index survey`],
[`12`, `8 Mar 2027`, `68`, `post-symptomatic`, `all four cameras + ASD leaf spectra + disease index survey`],
[`13`, `15 Mar 2027`, `75`, `post-symptomatic`, `all four cameras + ASD leaf spectra + disease index survey`]], [900, 1500, 1700, 1700, 3506], `Timeline of data collection in the field (inoculation on 30 December 2026): 3 pre-symptomatic and 10 post-symptomatic dates. Biochemical and biophysical parameters are sampled on flights 3, 5, 8 and 11 (Step A8).`, 16));
K.push(H3(`Step A3 – Subplots and disease index survey`));
K.push(...tab2('sa3', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Gives every sampling unit its label.`],
[`Input`, `Plot boundaries; field scoring sheets.`],
[`Output → next step`, `Labelled subplot list (date, plot, subplot, treatment, replication, leaf grades, disease index, DI class) → labels (Step A5) and subplot extraction (Activity D).`]], [2200, 7106], `Step A3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Divide each plot into four equal quadrant subplots; exclude border rows with an inner buffer.`));
K.push(NL(`Survey points: on every flight day one trained scorer examines the leaves at the centre and the four corners of each subplot (five points per subplot).`));
K.push(NL(`Leaf grade: each examined leaf is graded with the 0–9 key of Conn et al. (1990): 0 = no symptoms, 1 = 1–5%, 3 = 6–10%, 5 = 11–25%, 7 = 26–50%, 9 = more than 50% of the leaf area with pustules. Grade limits are written on the sheet to keep scoring consistent (Bock et al., 2010).`));
K.push(NL(`Disease index of the subplot: DI = Σ(x × f) / (n × Σf) × 100, where x is the grade, f the number of leaves with grade x and n = 9 the highest grade (Liu et al., 2024). The subplot DI is converted to the DI class of ${T('diclass')}.`));
K.push(NL(`Staghead severity (%) = number of staghead (infected) racemes / total racemes × 100, recorded per subplot from flowering onward.`));
K.push(NL(`For plot summaries, the plot DI is the mean of its four subplot DIs.`));
K.push(P(`**Supporting studies.** Disease index from graded leaves for UAV disease studies: Liu et al. (2024), Guo et al. (2021); grade keys for canopy severity: Abdulridha et al. (2023), Ma et al. (2026); leaf grade key of white rust: Conn et al. (1990).`));
K.push(EQ(`DI = Σ (x × f) / (n × Σ f) × 100      (x = leaf grade 0–9; f = leaves with grade x; n = 9)`));
K.push(...tab2('diclass', [[`DI range (%)`, `0`, `1–5`, `6–10`, `11–25`, `26–50`, `> 50`],
[`Severity level (field and leaf)`, `healthy`, `very low`, `low`, `moderate`, `high`, `very high`],
[`DI class`, `0`, `1`, `3`, `5`, `7`, `9`]], [2600, 1100, 1100, 1100, 1100, 1100, 1206], `Disease index ranges and severity classes (Liu et al., 2024).`, 17));
K.push(...tab2('pdiex', [[`Grade x`, `0`, `1`, `3`, `5`, `7`, `9`, `Subplot DI`],
[`Leaves f (dummy, 5 survey points)`, `6`, `5`, `4`, `3`, `2`, `0`, `Σ(x × f) = 0 + 5 + 12 + 15 + 14 + 0 = 46; Σf = 20; DI = 46 / (9 × 20) × 100 = 25.6% → class 7`]], [2200, 600, 600, 600, 600, 600, 600, 3506], `Worked example (dummy data): disease index of one subplot.`, 17));
K.push(H3(`Step A4 – Leaf spectra with the ASD field spectroradiometer`));
K.push(...tab2('sa4', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Gives leaf-level reflectance spectra and leaf severity grades from the same subplots on the same days as the UAV flights, for a separate leaf-level analysis and for linking leaf and canopy data.`],
[`Input`, `Three tagged plants in every subplot (12 per plot, 576 in total); ASD FieldSpec spectroradiometer with plant probe and leaf clip (contact probe with its own light source); white reference panel (Spectralon).`],
[`Output → next step`, `Leaf spectrum table (one row per leaf and date) with leaf grade and metadata → leaf-level dataset (its analysis is not part of this methodology).`]], [2200, 7106], `Step A4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Dates: all 13 flight dates (1, 4, 7 January; 11, 18, 25 January; 1, 8, 15, 22 February; 1, 8, 15 March 2027), on the day of the flight or within one day. The leaf clip has its own lamp, so measurements do not depend on the time of day or the sky.`));
K.push(NL(`Plants: before inoculation, tag 3 plants in every subplot (3 × 4 = 12 plants per plot), inside the inner buffer and spread along the subplot diagonal. Measure the same plants on every date; if a plant dies, replace it with its nearest neighbour and record the change.`));
K.push(NL(`Leaves: measure the 3rd (L3) and 5th (L5) fully expanded leaves counted from the top and the lowest green leaf (LL) of every plant. Count the positions again on each date because they shift as the plant grows; record a missing leaf (for example a senesced LL) as missing.`));
K.push(NL(`Instrument set-up: optimise the instrument and take a white reference at the start, then a new white reference every 10–15 minutes or at the start of every plot.`));
K.push(NL(`Readings: take 2 readings per leaf with the contact probe (on the lamina, avoiding the midrib), over 350–2500 nm.`));
K.push(NL(`Leaf grade: score the measured leaf immediately with the 0–9 key (Conn et al., 1990), using the same written grade limits as the canopy scoring.`));
K.push(NL(`Metadata for every reading: date, time, plot, subplot, plant ID, leaf position, reading number, leaf grade, time of the last white reference and operator; save the files with names that contain the plot, subplot, plant and leaf codes.`));
K.push(P(`**Supporting studies.** Field spectroscopy protocols (reference panels, metadata): Milton et al. (2009); leaf measurements collected together with UAV imagery: Calderón et al. (2014), Yu et al. (2021); disease indices developed from leaf measurements and carried to canopy and UAV scale: Huang et al. (2014), Liu et al. (2026); leaf severity grades: Conn et al. (1990), Bock et al. (2010).`));
K.push(NOTE(`Only the acquisition of the leaf data is described here. The leaf-level analysis and the linking with the UAV data are carried out separately.`));
K.push(...tab2('asdvol', [[`Item`, `Per date`, `All 13 dates`],
[`Tagged plants`, `576 (48 plots × 12)`, `same 576 plants`],
[`Leaves (L3, L5, LL)`, `1728`, `≈ 22 500`],
[`Readings (2 per leaf)`, `3456`, `≈ 45 000`],
[`Working time at about 40 seconds per leaf`, `≈ 20 operator-hours`, `—`],
[`Suggested teams`, `3 teams, one replication each (healthy block shared)`, `—`]], [3600, 3000, 2706], `Volume and organisation of the ASD leaf measurements.`, 17));
K.push(H3(`Step A5 – Labels and the two datasets`));
K.push(...tab2('sa5', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Defines exactly what each model predicts and which samples belong to which objective.`],
[`Input`, `Subplot disease indices and DI classes of all 13 flight dates (Step A3).`],
[`Output → next step`, `Post-symptomatic dataset (1920 samples per camera) and pre-symptomatic dataset (576 samples per camera) with their labels → all objectives.`]], [2200, 7106], `Step A5 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Pre-symptomatic dates: the first three flights (1, 4 and 7 January 2027; 2, 5 and 8 days after inoculation). Post-symptomatic dates: the next ten flights (11 January to 15 March 2027; 12–75 days after inoculation).`));
K.push(NL(`Detection label (Task A): healthy (DI = 0) or diseased (DI above 0), taken from the survey, not from the treatment.`));
K.push(NL(`Severity classes (Task B): the six DI classes 0, 1, 3, 5, 7 and 9 (${T('diclass')}); a class with fewer than 5% of the samples is merged with its neighbour (for example 7 + 9).`));
K.push(NL(`Severity score (Task C): the disease index DI (%) as a continuous variable for regression.`));
K.push(NL(`Pre-symptomatic labels (Activity 1.8 and Objective 3): healthy = subplots of the healthy plots; infected = inoculated subplots that show pustules on a later date; inoculated subplots that never show symptoms are kept out of the infected class.`));
K.push(P(`**Supporting studies.** Detection, severity classes and regression were analysed together for rice blast (Tian et al., 2021) and wheat powdery mildew (Feng et al., 2022); labels from the later status for pre-symptomatic samples: Zhu et al. (2017), Tian et al. (2021).`));
K.push(...tab2('classex', [[`Disease index (%)`, `0`, `1–5`, `6–10`, `11–25`, `26–50`, `> 50`],
[`Detection label (Task A)`, `healthy`, `diseased`, `diseased`, `diseased`, `diseased`, `diseased`],
[`DI class (Task B)`, `0`, `1`, `3`, `5`, `7`, `9`],
[`Dummy count (1920 samples)`, `512`, `413`, `362`, `313`, `200`, `120`]], [2500, 1134, 1134, 1134, 1134, 1134, 1136], `How one disease index gives the three labels (Task C uses the DI itself; dummy class counts).`, 17));
K.push(H3(`Step A6 – Covariates: days after inoculation, variety, inoculation timing, growth stage and weather`));
K.push(...tab2('sa6', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Disease severity changes with time, crop stage, variety and weather. These known factors must be recorded so that their effect can be separated from what the cameras add.`],
[`Input`, `Field book (sowing, inoculation and flight dates; variety; growth stage on each flight date); daily weather from the IARI agrometeorological observatory.`],
[`Output → next step`, `Covariate table with one row per subplot-date → response analysis (Step 1.1.3), covariate baseline and sensor + covariate models (Steps 2.5.5 and 3.5.3), results by stage and treatment.`]], [2200, 7106], `Step A6 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Days after inoculation (DAI): flight date minus inoculation date, 30 December 2026 (numeric).`));
K.push(NL(`Variety: V1 = PM 26, V2 = Pusa Vijay, V3 = PM 37 (categorical, one-hot coded in models).`));
K.push(NL(`Inoculation timing: D1–D4, also expressed as crop age at inoculation: 41, 34, 27 and 20 days (numeric).`));
K.push(NL(`Growth stage of each plot on each flight date, read with the BBCH scale and coded as 1 = vegetative (BBCH 10–49), 2 = flowering (BBCH 60–69), 3 = pod formation (BBCH 70–79 and later) (ordinal).`));
K.push(NL(`Weather: daily maximum and minimum air temperature (T_{max}, T_{min}), morning and afternoon relative humidity (RH I, RH II) and rainfall, summarised as the mean (rainfall: total) of the 7 days ending the day before each flight (no look-ahead), plus the number of favourable days since inoculation for leaf infection (T_{max} 16–24 °C, RH I > 97% and RH II > 40%) and for staghead (T_{max} 20–29 °C, T_{min} > 12 °C and RH I > 97%) (Chattopadhyay et al., 2011).`));
K.push(NL(`Covariates are not features of any camera and are not used in feature selection; they enter only the covariate models and the stratified results.`));
K.push(P(`**Supporting studies.** Weather conditions that favour white rust of Indian mustard and weather-based forecasting: Chattopadhyay et al. (2011), Saharan et al. (2014); BBCH growth stages: Lancashire et al. (1991), Meier (2018); stage-dependent spectral disease signals: Blasch et al. (2023), Liu et al. (2024); combining weather with remote sensing improved disease forecasts over weather alone: Zhang et al. (2014); days after inoculation in early detection: Mahlein et al. (2019), Zhu et al. (2017).`));
K.push(...tab2('covtab', [[`Covariate`, `Type and coding`, `Varies between subplots on one date?`, `Main use`],
[`Days after inoculation`, `numeric (days)`, `no (same inoculation date)`, `time trend; baseline model`],
[`Variety (V1 PM 26, V2 Pusa Vijay, V3 PM 37)`, `categorical, one-hot`, `yes`, `baseline; stratified results; transfer test`],
[`Inoculation timing (D1–D4)`, `categorical, or crop age at inoculation (days)`, `yes`, `baseline; stratified results; transfer test`],
[`Growth stage (1 vegetative, 2 flowering, 3 pod formation)`, `ordinal from BBCH`, `yes (staggered sowing)`, `baseline; results by stage; flowering check`],
[`Weather (T_{max}, T_{min}, RH I, RH II, rainfall; favourable days)`, `numeric, 7-day summaries`, `no (one value per date)`, `interpretation; baseline (time effect only)`]], [2900, 2200, 1900, 2306], `Covariates recorded for every subplot-date. Weather is the same for all subplots on a date, so it can explain differences between dates but not between subplots.`, 17));
K.push(NOTE(`Weather has only one value per flight date (ten values in the post-symptomatic period), so in a single season it cannot be separated from the date itself. It is therefore used for interpretation and inside the covariate baseline, and results of models that contain weather are labelled "within-season"; their transfer to another season must be tested with data of that season (Zhang et al., 2014; Ma et al., 2026).`));
K.push(H3(`Step A7 – Independent testing data at Bharatpur (research farms and farmers' fields)`));
K.push(...tab2('sa7', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Models validated only inside the IARI field may not work on other soils, varieties, management and natural epidemics. Independent data from another site are needed to test the frozen models (independent testing, not validation).`],
[`Input`, `Research farm(s) and farmers' fields at Bharatpur, Rajasthan, with natural white rust; the same four cameras, calibration panels and ground control points; the same severity key and scorer.`],
[`Output → next step`, `Bharatpur independent test dataset (quadrat-dates with images of all four cameras, disease index and covariates) → independent testing (Activity 2.7).`]], [2200, 7106], `Step A7 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Sites: research-farm plots and farmers' fields with natural white rust in the same season (rabi 2026-27), chosen to cover healthy to severely diseased canopies and the common local varieties.`));
K.push(NL(`Sampling units: in every field mark validation quadrats of the same size as an IARI subplot (2.5 m × 1.5 m) with corner pegs and image-visible markers, recorded with an RTK GNSS receiver, away from field borders and bunds.`));
K.push(NL(`Size: aim for at least 300 quadrat-dates in total (for example 8–10 farmers' fields and research-farm plots × 15–20 quadrats × 2–3 post-symptomatic flight dates in February–March), with every DI class represented, including healthy quadrats.`));
K.push(NL(`Flights: the same four cameras and flight settings as at IARI (30 m, 11:00–14:00 h, about 85% forward and 80% side overlap, reflectance panels and ground control points on every flight); if possible add one flight before symptoms with the same quadrats revisited later.`));
K.push(NL(`Ground truth: survey the disease index of every quadrat (centre and four corners, 0–9 leaf grades; Step A3), by the same scorer, on the day of the flight.`));
K.push(NL(`Covariates (as in Step A6): variety, sowing date, growth stage (BBCH), days since the first symptoms were seen, fungicide sprays of the farmer, and daily weather from the nearest agrometeorological observatory or automatic weather station.`));
K.push(NL(`Healthy reference: where possible, keep a fungicide-protected strip of the main variety at the research farm, so that features that need a healthy reference can also be tested.`));
K.push(P(`**Supporting studies.** Independent testing on naturally infected fields from another site and year: Ma et al. (2026); importance of testing on independent locations: Roberts et al. (2017), Ploton et al. (2020); Bharatpur as a white rust site for weather-based forecasting: Chattopadhyay et al. (2011); UAV disease monitoring of smallholder fields: Liu et al. (2026); transfer of UAV disease models to new areas: Yuan et al. (2025).`));
K.push(NOTE(`The Bharatpur data are never used for feature selection, tuning or training. They are used only once, for independent testing of the frozen final models.`));
K.push(H3(`Step A8 – Biochemical and biophysical parameters`));
K.push(...tab2('sa8', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Spectral and thermal features are indirect. Measured pigments, water status, membrane damage, gas exchange and leaf area show what white rust does to the plant and give the camera responses a physiological explanation.`],
[`Input`, `One designated subplot per plot; untagged plants of that subplot for destructive samples; leaf L3 (third fully expanded leaf from the top); spectrophotometer, conductivity meter, LI-6400 portable gas exchange system, plant canopy analyser.`],
[`Output → next step`, `Table of 11 parameters for 48 plots × 4 dates (192 samples per parameter; leaf area index for all 4 subplots) → Activities 1.7 and 1.8 and Step 3.1.2.`]], [2200, 7106], `Step A8 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Dates (all on UAV flight days): 7 January 2027 (pre-symptomatic, 8 days after inoculation) and 18 January, 8 February and 1 March 2027 (post-symptomatic, 19, 40 and 61 days after inoculation), covering early, peak and late disease and the vegetative, flowering and pod-formation stages.`));
K.push(NL(`Designated subplot: one subplot per plot, rotated so that each of the four subplot positions is sampled in 12 plots (position = plot number modulo 4, plus 1); its code is stored with every sample, so the parameters can be joined to the UAV features and canopy score of that subplot.`));
K.push(NL(`Gas exchange: on leaf L3 of one tagged plant (non-destructive, Step A4), between 09:30 and 11:30 h, before the flight.`));
K.push(NL(`Leaf samples for the laboratory: after the gas-exchange readings, collect L3 leaves from 3 untagged plants of the designated subplot, keep them in a cool box and process them the same day; the tagged plants are not damaged.`));
K.push(NL(`Leaf area index: in all four subplots, under diffuse light (early morning, late afternoon or overcast sky).`));
K.push(NL(`Record the BBCH growth stage of each plot on every sampling date (Step A6).`));
K.push(NL(`Methods and units are given in ${T('physio')}; the formulas are given below.`));
K.push(P(`**Supporting studies.** Plant traits measured together with airborne and UAV imagery to explain disease-related spectral and thermal changes: Calderón et al. (2013), Zarco-Tejada et al. (2018), Poblete et al. (2023); leaf area index of mustard with a plant canopy analyser at IARI: Goyal et al. (2021).`));
K.push(...tab2('physio', [[`Parameter (unit)`, `Method`, `Sample`, `References`],
[`Chlorophyll a and b (mg g⁻¹ fresh weight)`, `extraction in dimethyl sulfoxide (DMSO) without grinding; absorbance at 665 and 649 nm; DMSO equations`, `100 mg leaf discs in 10 mL DMSO, 65 °C until colourless`, `Hiscox and Israelstam (1979); Wellburn (1994)`],
[`Total carotenoids (mg g⁻¹ fresh weight)`, `same DMSO extract; absorbance at 480 nm; DMSO equation`, `same extract`, `Lichtenthaler and Wellburn (1983); Wellburn (1994)`],
[`Anthocyanin (µg g⁻¹ fresh weight)`, `pH differential method: absorbance at about 520 and 700 nm in pH 1.0 (potassium chloride) and pH 4.5 (sodium acetate) buffers`, `acidified-methanol extract of 0.5 g leaf tissue`, `Lee et al. (2005)`],
[`Total soluble protein (mg g⁻¹ fresh weight)`, `Bradford dye-binding method; absorbance at 595 nm against a bovine serum albumin standard curve`, `buffer extract of 0.5 g leaf tissue`, `Bradford (1976)`],
[`Relative water content (%)`, `fresh weight, turgid weight after 4 h floating on distilled water, dry weight after 48 h at 70 °C`, `10 leaf discs`, `Barrs and Weatherley (1962)`],
[`Membrane stability index (%)`, `electrolyte leakage: conductivity after 30 min at 40 °C (C₁) and after 10 min at 100 °C (C₂)`, `two sets of 0.1 g leaf discs in 10 mL double-distilled water`, `Premachandra et al. (1990); Sairam (1994)`],
[`Net photosynthetic rate (µmol CO₂ m⁻² s⁻¹)`, `LI-6400 portable gas exchange system (infrared gas analyser): leaf chamber with LED light 1200 µmol m⁻² s⁻¹, reference CO₂ 400 µmol mol⁻¹, flow 500 µmol s⁻¹, leaf temperature near ambient; read after the values are stable`, `leaf L3 of a tagged plant`, `Long and Bernacchi (2003); Riches et al. (2020)`],
[`Transpiration rate (mmol H₂O m⁻² s⁻¹)`, `same reading`, `same leaf`, `Long and Bernacchi (2003)`],
[`Stomatal conductance (mol H₂O m⁻² s⁻¹)`, `same reading (intercellular CO₂ also recorded)`, `same leaf`, `Long and Bernacchi (2003)`],
[`Leaf area index (m² m⁻²)`, `plant canopy analyser: one reading above and four below the canopy across the rows, with a view cap that hides the operator`, `every subplot`, `Bréda (2003); Goyal et al. (2021)`]], [2400, 3200, 1800, 1906], `Biochemical and biophysical parameters, methods and units. Pigments, anthocyanin and protein are expressed per gram of fresh weight; µg mg⁻¹ equals mg g⁻¹.`, 15));
K.push(P(`**Formulas.** Pigments in µg mL⁻¹ of DMSO extract for a spectrophotometer of 1–4 nm resolution (Wellburn, 1994); they are converted to mg g⁻¹ fresh weight with the extract volume and sample weight. The anthocyanin content is expressed as cyanidin-3-glucoside equivalents (molecular weight 449.2 g mol⁻¹, molar absorptivity 26 900 L mol⁻¹ cm⁻¹; Lee et al., 2005).`));
K.push(EQ(`C_{a} = 12.47 A_{665} − 3.62 A_{649};    C_{b} = 25.06 A_{649} − 6.5 A_{665};    C_{x+c} = (1000 A_{480} − 1.29 C_{a} − 53.78 C_{b}) / 220`));
K.push(EQ(`A = (A_{520} − A_{700})_{pH 1.0} − (A_{520} − A_{700})_{pH 4.5};    anthocyanin (mg L^{−1}) = A × 449.2 × dilution × 1000 / (26 900 × path length)`));
K.push(EQ(`RWC (%) = (FW − DW) / (TW − DW) × 100;    membrane stability index (%) = [1 − (C_{1} / C_{2})] × 100`));
K.push(...tab2('physex', [[`Parameter (dummy data)`, `Readings`, `Result`],
[`Chlorophyll a, b and carotenoids`, `A₆₆₅ = 0.62, A₆₄₉ = 0.25, A₄₈₀ = 0.40; 0.1 g in 10 mL`, `C_a = 6.83, C_b = 2.24, C_x+c = 1.23 µg mL⁻¹ → 0.68, 0.22 and 0.12 mg g⁻¹ fresh weight`],
[`Anthocyanin`, `(A₅₂₀ − A₇₀₀) = 0.230 at pH 1.0 and 0.045 at pH 4.5; 0.5 g in 5 mL`, `A = 0.185 → 3.09 mg L⁻¹ → 30.9 µg g⁻¹ fresh weight`],
[`Relative water content`, `FW = 0.52 g, TW = 0.60 g, DW = 0.10 g`, `(0.52 − 0.10) / (0.60 − 0.10) × 100 = 84%`],
[`Membrane stability index`, `C₁ = 120 µS cm⁻¹, C₂ = 600 µS cm⁻¹`, `[1 − 120/600] × 100 = 80%`]], [2400, 3800, 3106], `Worked examples of the calculations (dummy data).`, 17));
K.push(...tab2('cirga', [[`Aspect`, `Leaf gas exchange with a portable infrared gas analyser (LI-6400)`],
[`Principle (how it works)`, `Air of known CO₂ and water-vapour concentration flows through a leaf chamber; infrared gas analysers measure the concentrations before and after the leaf, and the differences give net photosynthesis, transpiration and stomatal conductance.`],
[`Problem it solves`, `Measures the physiological activity of the leaf directly, which explains canopy temperature (transpiration) and photosynthesis-related spectral indices.`],
[`Specification in this study`, `Leaf L3 of a tagged plant; LED light 1200 µmol m⁻² s⁻¹; reference CO₂ 400 µmol mol⁻¹; flow 500 µmol s⁻¹; readings after stabilisation; 09:30–11:30 h.`],
[`Hyper-parameters and how they are tuned`, `Chamber settings fixed for all dates; readings accepted when CO₂ and water differences are stable; instrument zeroed and matched before each session.`],
[`Data on which it works well`, `Field leaves under stable mid-morning light; one leaf per plot because each reading takes several minutes.`],
[`Why it was selected`, `The standard method for leaf photosynthesis, transpiration and stomatal conductance; stomatal conductance explained canopy temperature in airborne disease detection (Calderón et al., 2013).`],
[`Key references`, `Long and Bernacchi (2003); Riches et al. (2020)`]], [2300, 7006], `Method card – Leaf gas exchange with a portable infrared gas analyser (LI-6400).`, 16));
K.push(...tab2('clai', [[`Aspect`, `Leaf area index with a plant canopy analyser`],
[`Principle (how it works)`, `A fish-eye optical sensor compares diffuse light above and below the canopy at several view angles; the gap fraction is inverted to leaf area per ground area.`],
[`Problem it solves`, `Gives canopy size, which changes with growth stage and with disease and affects every canopy spectral feature.`],
[`Specification in this study`, `One above and four below readings per subplot, view cap, diffuse light.`],
[`Hyper-parameters and how they are tuned`, `No tuning; readings only under diffuse light, the same sensor and view cap on all dates.`],
[`Data on which it works well`, `Row crops with closed or nearly closed canopies.`],
[`Why it was selected`, `Fast, non-destructive and used for mustard at IARI (Goyal et al., 2021); separates canopy-size effects from disease effects.`],
[`Key references`, `Bréda (2003); Goyal et al. (2021)`]], [2300, 7006], `Method card – Leaf area index with a plant canopy analyser.`, 16));
K.push(H3(`Step A9 – Glasshouse (pot) experiment`));
K.push(...tab2('sa9', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Field data contain weather, soil and canopy effects. A pot experiment under controlled conditions shows the response of the same varieties and crop ages to white rust in the laboratory/glasshouse situation and links leaf-level and field-level characterisation.`],
[`Input`, `Glasshouse of the Division of Plant Pathology, IARI; 48 pots; the three varieties of the field (V1 = PM 26, V2 = Pusa Vijay, V3 = PM 37); inoculum of 1.5 × 10^{5} zoosporangia mL^{−1}.`],
[`Output → next step`, `Pot-level and leaf-level dataset (visual severity and sensor measurements of each pot and date) → response analysis and characterisation under controlled conditions (Objective 1).`]], [2200, 7106], `Step A9 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Treatments: four sowing dates at 7-day intervals (D1 = 23 November, D2 = 30 November, D3 = 7 December, D4 = 14 December 2026) × three varieties = 12 treatments.`));
K.push(NL(`Pots: 36 inoculated pots (12 treatments × 3 replications, R1–R3) in the inoculated compartment and 12 healthy pots (one per treatment) in a separate isolation compartment; total 48 pots, each with a code (sowing date, variety, pot number).`));
K.push(NL(`Inoculation on 4 January 2027: 10 µL droplets of the zoosporangial suspension on the adaxial leaf surface; pots covered with polythene for 3 days; relative humidity 80–90% and about 19 °C.`));
K.push(NL(`Observations at 2, 5, 8 and 11 days after inoculation and then every 7 days: visual severity on the 0–6 scale and handheld sensor measurements of the same leaves (ASD leaf spectra with the contact probe, Step A4 protocol).`));
K.push(NL(`The same data organisation as in the field (identifiers, labels, covariates) is used, so that the pot and field responses can be compared.`));
K.push(P(`**Supporting studies.** Controlled-environment inoculation of Brassica juncea with Albugo candida: Mishra et al. (2009); white rust biology and assessment: Saharan et al. (2014); leaf-level disease spectra under controlled conditions linked to field and UAV scale: Mahlein et al. (2013), Huang et al. (2014), Liu et al. (2026).`));
K.push(NOTE(`The pot experiment uses its own severity scale (0–6) and is analysed separately from the field datasets; it is not used for training or testing the field models.`));
K.push(H2(`Activity B – Image pre-processing`));
K.push(P(`Activity B turns raw images into calibrated, aligned images on one common grid (${F('preproc')}).`));
K.push(...fig2('preproc', 'g02_preproc.png', `Flow chart of Activity B (Steps B1–B5).`, 540));
K.push(H3(`Step B1 – Radiometric calibration`));
K.push(...tab2('sb1', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Raw digital numbers depend on illumination and camera settings and cannot be compared between dates or cameras.`],
[`Input`, `Raw images; panel images; sunlight-sensor records; air temperature and humidity.`],
[`Output → next step`, `Reflectance images (hyperspectral, multispectral), consistent RGB images and temperature images → Step B2.`]], [2200, 7106], `Step B1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Hyperspectral and multispectral: convert digital numbers to reflectance with the empirical line method using the panels imaged before and after each flight; correct illumination changes during the flight with the downwelling sunlight sensor.`));
K.push(NL(`Red–green–blue: fixed exposure and white balance on all dates; colour values are used as relative values (colour indices are ratios, so they are not affected by overall brightness).`));
K.push(NL(`Thermal: convert radiance to temperature with emissivity 0.98 and the air temperature, relative humidity and flight height of each flight.`));
K.push(P(`**Supporting studies.** Empirical line method: Smith and Milton (1999); UAV spectroscopy workflows: Aasen et al. (2018); panels before and after the flight: Yuan et al. (2025), Blasch et al. (2023), Guo et al. (2021); thermal conversion: Jones et al. (2009), Messina and Modica (2020).`));
K.push(...tab2('celine', [[`Aspect`, `Empirical line calibration`],
[`Principle (how it works)`, `A linear relation between the digital number and reflectance is fitted for each band from targets of known reflectance (panels); the relation is applied to every pixel.`],
[`Problem it solves`, `Removes the effect of sun angle, atmosphere and camera gain, so reflectance is comparable between dates.`],
[`Specification in this study`, `Two or more panels of known reflectance (for example 5%, 20%, 50%) imaged before and after each flight; one linear fit per band and flight.`],
[`Hyper-parameters and how they are tuned`, `No hyper-parameters; the panel reflectances must be certified and the panels must fill many pixels.`],
[`Data on which it works well`, `Low-altitude UAV images under stable sky, where the atmosphere between camera and ground is thin.`],
[`Why it was selected`, `Simple, standard and accurate for UAV data; used in almost all UAV disease studies.`],
[`Key references`, `Smith and Milton (1999); Aasen et al. (2018)`]], [2300, 7006], `Method card – Empirical line calibration.`, 16));
K.push(H3(`Step B2 – Orthomosaics and georeferencing`));
K.push(...tab2('sb2', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Single frames must be joined into one map per camera and date with correct ground coordinates.`],
[`Input`, `Calibrated frames; ground control points.`],
[`Output → next step`, `Georeferenced orthomosaics and georectified hyperspectral cubes → Steps B3 and B4.`]], [2200, 7106], `Step B2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Build orthomosaics of the frame cameras (multispectral, red–green–blue, thermal) by structure-from-motion.`));
K.push(NL(`Georectify the push-broom hyperspectral lines with the position and attitude data of the UAV.`));
K.push(NL(`Use the same ground control points on every date so that all dates share one coordinate frame.`));
K.push(P(`**Supporting studies.** Georeferenced UAV hyperspectral mosaics: Guo et al. (2021), Ma et al. (2026); mosaicking of RGB, multispectral and thermal frames before feature extraction: Maimaitijiang et al. (2020), Feng et al. (2022).`));
K.push(H3(`Step B3 – Hyperspectral cube quality control and smoothing`));
K.push(...tab2('sb3', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Water-vapour absorption, detector edges and random noise make some bands unusable and add noise to the others.`],
[`Input`, `Georectified 613-band cube of each date.`],
[`Output → next step`, `Clean 483-band reflectance cube → Step B4.`]], [2200, 7106], `Step B3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Remove the water-vapour regions (1335–1460 nm and 1785–1965 nm) and the noisy ends, giving 483 bands from 399 to 2398 nm; drop the three isolated bands at 916–920 nm (detector edge).`));
K.push(NL(`Smooth every spectrum with a Savitzky–Golay filter (window 5 bands, second-order polynomial) separately on each continuous band segment, never across a removed region.`));
K.push(NL(`Check that reflectance is between 0 and 1.`));
K.push(P(`**Supporting studies.** Removal of water-vapour bands: Thenkabail et al. (2004); Savitzky–Golay smoothing: Savitzky and Golay (1964), Schafer (2011); used before derivatives by Tsai and Philpot (1998) and in disease studies by Tian et al. (2021) and Mustafa et al. (2023).`));
K.push(...tab2('csg', [[`Aspect`, `Savitzky–Golay smoothing filter`],
[`Principle (how it works)`, `A low-order polynomial is fitted by least squares to a moving window of bands; the centre value of the fitted polynomial replaces the measured value.`],
[`Problem it solves`, `Reduces random noise while keeping the shape and position of absorption features; prepares spectra for the first derivative.`],
[`Specification in this study`, `Window of 5 bands (about 15–20 nm), polynomial order 2, applied on each continuous segment.`],
[`Hyper-parameters and how they are tuned`, `Window length and polynomial order; chosen by visual check of the red edge and by the noise of the first derivative on panel pixels (a longer window smooths more but flattens narrow features).`],
[`Data on which it works well`, `Densely sampled spectra with random noise, such as hyperspectral reflectance.`],
[`Why it was selected`, `Keeps peaks better than a moving average; standard before derivatives.`],
[`Key references`, `Savitzky and Golay (1964); Schafer (2011); Rinnan et al. (2009)`]], [2300, 7006], `Method card – Savitzky–Golay smoothing filter.`, 16));
K.push(H3(`Step B4 – Projection and co-registration`));
K.push(...tab2('sb4', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Images of different cameras do not overlap exactly; small shifts mix canopy and soil values at the edges of rows.`],
[`Input`, `Georeferenced images of all cameras for one date.`],
[`Output → next step`, `All images in one projection and aligned to the hyperspectral image → Step B5.`]], [2200, 7106], `Step B4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Project every image to WGS 84 / UTM zone 43N so that distances are in metres.`));
K.push(NL(`Register the red–green–blue, multispectral and thermal images to the hyperspectral image with tie points (plot corners, markers) and a first- or second-order polynomial transformation.`));
K.push(NL(`Accept the registration when the root-mean-square error of independent check points is below one hyperspectral pixel (2.2 cm).`));
K.push(P(`**Supporting studies.** Image registration: Zitová and Flusser (2003); polynomial warping: Richards (2013); co-registered multi-camera UAV layers: Maimaitijiang et al. (2020), Feng et al. (2022).`));
K.push(H3(`Step B5 – Resampling to the hyperspectral grid`));
K.push(...tab2('sb5', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The cameras have different pixel sizes (about 0.8, 2, 2.2 and 3.9 cm); one grid is needed so that one pixel is the same ground point in every layer.`],
[`Input`, `Co-registered images.`],
[`Output → next step`, `All layers on the 2.2 cm hyperspectral grid → vegetation mask (Activity C) and subplot values (Activity D).`]], [2200, 7106], `Step B5 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Red–green–blue (finer): pixel aggregate, so each new pixel is the mean of the pixels it covers.`));
K.push(NL(`Multispectral (similar size): bilinear interpolation.`));
K.push(NL(`Thermal (coarser): nearest neighbour, which keeps the measured temperatures.`));
K.push(NL(`Compute red–green–blue texture before resampling, at native resolution, because resampling removes fine texture.`));
K.push(P(`**Supporting studies.** Resampling methods: Richards (2013); resampling of UAV hyperspectral images to other resolutions: Guo et al. (2021); pixel aggregation between UAV and satellite grids: Revill et al. (2020), Yuan et al. (2025); common-grid stacking of RGB, multispectral and thermal data: Maimaitijiang et al. (2020).`));
K.push(...tab2('cresample', [[`Aspect`, `Resampling (pixel aggregate, bilinear, nearest neighbour)`],
[`Principle (how it works)`, `Pixel aggregate averages all fine pixels inside a coarse pixel; bilinear interpolation weights the four nearest pixels by distance; nearest neighbour copies the value of the closest pixel.`],
[`Problem it solves`, `Places all cameras on one grid so that one mask and one set of subplot polygons can be used.`],
[`Specification in this study`, `Target grid: 2.2 cm hyperspectral grid; method chosen by the direction of the change in pixel size (finer → aggregate; similar → bilinear; coarser → nearest neighbour).`],
[`Hyper-parameters and how they are tuned`, `No tuning; the choice follows the rule above.`],
[`Data on which it works well`, `Aggregate: going to a coarser grid; nearest neighbour: preserving measured values such as temperature.`],
[`Why it was selected`, `Avoids aliasing when coarsening and avoids inventing new temperatures when refining.`],
[`Key references`, `Richards (2013); Guo et al. (2021)`]], [2300, 7006], `Method card – Resampling (pixel aggregate, bilinear, nearest neighbour).`, 16));
K.push(H2(`Activity C – Endmember extraction and vegetation mask`));
K.push(P(`Soil, grass, weeds and shadow inside a subplot change reflectance, texture and temperature and must be removed before disease features are extracted. Activity C builds one field-wide library of pure spectra (endmembers) with the hourglass workflow, classifies every pixel with the spectral angle mapper and keeps the canopy pixels (${F('endmember')}). Flowers are kept because the disease survey includes the inflorescence (staghead); no spectral unmixing is done.`));
K.push(...fig2('endmember', 'g03_endmember.png', `Flow chart of Activity C: endmember extraction (Steps C1–C5) and vegetation mask (Steps C6–C8).`, 540));
K.push(H3(`Step C1 – Sampling of pixels from all dates`));
K.push(...tab2('sc1', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Endmember extraction on every full image would be slow, and endmembers extracted separately for each date or plot would not be comparable.`],
[`Input`, `Clean hyperspectral cubes of all dates (Step B3).`],
[`Output → next step`, `One pooled pixel sample (for example 20 000 pixels from each date) → Step C2.`]], [2200, 7106], `Step C1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Draw a random sample of pixels from inside the field on every date, so that early green canopy, diseased canopy, flowering canopy, soil, grass and shadow are all represented.`));
K.push(NL(`Add pixels of the reference panels and known soil and grass patches to make sure these classes are present.`));
K.push(P(`**Supporting studies.** One library for the whole scene gives the same classes in every plot and on every date (Bioucas-Dias et al., 2012); pooled samples for the hourglass workflow: Boardman and Kruse (2011).`));
K.push(H3(`Step C2 – Minimum noise fraction (MNF) transformation`));
K.push(...tab2('sc2', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Hyperspectral bands are noisy and highly correlated; the corners of the pixel cloud, where pure pixels lie, are hidden by noise.`],
[`Input`, `Pooled pixel sample (483 bands).`],
[`Output → next step`, `Minimum noise fraction (MNF) components ordered by signal-to-noise ratio; components with eigenvalues clearly above 1 → Step C3.`]], [2200, 7106], `Step C2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Estimate the noise from the differences between neighbouring pixels (shift difference) in a homogeneous area.`));
K.push(NL(`Whiten the noise (rescale so the noise has unit variance in every direction) and then apply principal component analysis.`));
K.push(NL(`Plot the eigenvalues (${F('dummyem')}a); keep the components whose eigenvalue is clearly above 1 (here about 8–10); components with eigenvalues near 1 contain only noise.`));
K.push(P(`**Supporting studies.** Green et al. (1988); Boardman and Kruse (2011); Bioucas-Dias et al. (2012).`));
K.push(...tab2('cmnf', [[`Aspect`, `Minimum noise fraction (MNF) transformation`],
[`Principle (how it works)`, `Two principal component analyses in sequence: the first whitens the noise, the second orders the components by signal-to-noise ratio. Eigenvalue 1 means a component is pure noise.`],
[`Problem it solves`, `Separates signal from noise and reduces 483 correlated bands to about 10 informative components.`],
[`Specification in this study`, `Noise from shift differences in a homogeneous field area; components with eigenvalue above about 2 kept.`],
[`Hyper-parameters and how they are tuned`, `Number of components kept: chosen from the eigenvalue plot (the "knee" where values approach 1).`],
[`Data on which it works well`, `Hyperspectral images with many correlated, noisy bands.`],
[`Why it was selected`, `Unlike plain principal component analysis, it ranks components by image quality, not by variance (which can be dominated by noise or illumination).`],
[`Key references`, `Green et al. (1988); Boardman and Kruse (2011)`]], [2300, 7006], `Method card – Minimum noise fraction (MNF) transformation.`, 16));
K.push(H3(`Step C3 – Pixel purity index (PPI)`));
K.push(...tab2('sc3', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Among thousands of pixels, the few spectrally pure pixels (one material only) must be found.`],
[`Input`, `Selected MNF components of the pixel sample.`],
[`Output → next step`, `Pixel purity index (PPI) image: count of how often each pixel was an extreme → Step C4.`]], [2200, 7106], `Step C3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Project the MNF pixel cloud onto many random unit vectors ("skewers"), for example 10 000.`));
K.push(NL(`On each skewer, record the pixels at the two extreme ends; add one to their count.`));
K.push(NL(`Keep pixels with high counts (for example at least 10) as pure-pixel candidates.`));
K.push(P(`**Supporting studies.** Boardman et al. (1995); Boardman and Kruse (2011); Bioucas-Dias et al. (2012).`));
K.push(...tab2('cppi', [[`Aspect`, `Pixel purity index (PPI)`],
[`Principle (how it works)`, `In a cloud of mixed pixels, pure pixels lie at the corners (vertices). A random projection puts corner pixels at its ends; pixels that are repeatedly at the ends are pure.`],
[`Problem it solves`, `Finds candidate endmember pixels without prior knowledge.`],
[`Specification in this study`, `10 000 skewers on the kept MNF components; threshold of 10 hits.`],
[`Hyper-parameters and how they are tuned`, `Number of skewers (more = more stable; 5000–20 000 usual) and the threshold (2–3 times the noise level); fixed after checking that the candidate set no longer changes.`],
[`Data on which it works well`, `Scenes with some pure pixels of each material; high spatial resolution (2.2 cm) makes pure canopy and soil pixels common.`],
[`Why it was selected`, `Simple, transparent and part of the standard hourglass workflow; candidates are checked visually in the next step.`],
[`Key references`, `Boardman et al. (1995); Boardman and Kruse (2011)`]], [2300, 7006], `Method card – Pixel purity index (PPI).`, 16));
K.push(H3(`Step C4 – n-dimensional visualisation and endmember selection`));
K.push(...tab2('sc4', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `PPI candidates form clusters; each cluster corner must be turned into one endmember spectrum.`],
[`Input`, `Pure-pixel candidates in MNF space.`],
[`Output → next step`, `Endmember spectra (mean reflectance of each cluster) → Step C5.`]], [2200, 7106], `Step C4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Display the candidates in two- and three-dimensional scatter plots of MNF components and rotate them (n-dimensional visualiser).`));
K.push(NL(`Mark the clusters at the corners of the cloud (${F('dummyem')}b).`));
K.push(NL(`Compute the endmember spectrum as the mean reflectance (original bands) of the pixels in each cluster.`));
K.push(P(`**Supporting studies.** Boardman and Kruse (2011); Bioucas-Dias et al. (2012).`));
K.push(H3(`Step C5 – Endmember identification and library`));
K.push(...tab2('sc5', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Endmembers must be named before they can be used to build a mask.`],
[`Input`, `Endmember spectra; field photographs; red–green–blue images; leaf spectra of the study.`],
[`Output → next step`, `Labelled endmember library (green canopy, stressed canopy, flower, soil, grass, shadow) → Step C6.`]], [2200, 7106], `Step C5 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Locate the pixels of each endmember in the red–green–blue image and in field photographs.`));
K.push(NL(`Compare their shapes with known spectra: green canopy (red edge, high near-infrared), stressed canopy (higher red, lower near-infrared), yellow flower (high green–red reflectance), soil (rising, featureless), shadow (low everywhere) (${F('dummyem')}c).`));
K.push(NL(`Merge duplicates and store the final library.`));
K.push(P(`**Supporting studies.** Identification by spectral shape and image context: Boardman and Kruse (2011); flowers in Brassica canopies: Sulik and Long (2016).`));
K.push(...fig2('dummyem', 'g12_dummy_endmember.png', `Dummy example of endmember extraction: (a) MNF eigenvalues; (b) pure pixels at the corners of the MNF cloud; (c) endmember library.`, 560));
K.push(H3(`Step C6 – Spectral angle mapper (SAM) classification`));
K.push(...tab2('sc6', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Every pixel of every date must be assigned to one class.`],
[`Input`, `Labelled endmember library; clean cubes of all dates.`],
[`Output → next step`, `Class map of every date → Step C7.`]], [2200, 7106], `Step C6 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Compute the spectral angle between each pixel spectrum and each endmember (equation below).`));
K.push(NL(`Assign the pixel to the endmember with the smallest angle; leave it unclassified if the smallest angle is larger than the threshold.`));
K.push(NL(`Calibrate the threshold (0.10, 0.20 or 0.30 radian tested) on labelled reference pixels.`));
K.push(P(`**Supporting studies.** Kruse et al. (1993); spectral angle mapper for crop masks in UAV hyperspectral studies: Guo et al. (2021).`));
K.push(EQ(`α = cos^{−1} [ Σ_{i} t_{i} r_{i} / ( √(Σ_{i} t_{i}^{2}) √(Σ_{i} r_{i}^{2}) ) ]`));
K.push(P(`Here t is the pixel spectrum, r the endmember spectrum and i the band. Because the angle does not depend on the length of the spectra, a shaded canopy pixel and a sunlit canopy pixel have almost the same angle to the canopy endmember.`));
K.push(...tab2('samex', [[`Spectrum (4 bands, dummy)`, `Blue`, `Green`, `Red`, `Near-infrared`, `Angle to pixel (radian)`],
[`Pixel t`, `0.05`, `0.08`, `0.06`, `0.45`, `—`],
[`Green canopy endmember`, `0.04`, `0.09`, `0.05`, `0.50`, `0.044 (smallest → canopy)`],
[`Yellow flower endmember`, `0.06`, `0.20`, `0.22`, `0.40`, `0.424`],
[`Soil endmember`, `0.10`, `0.14`, `0.18`, `0.25`, `0.550`]], [2600, 900, 900, 900, 1300, 2706], `Worked example (dummy data): spectral angle mapper classification of one pixel.`, 17));
K.push(...fig2('dummysam', 'g13_dummy_sam.png', `Dummy example: (a) the spectral angle α between a pixel and an endmember; (b) class map and the resulting vegetation mask.`, 520));
K.push(...tab2('csam', [[`Aspect`, `Spectral angle mapper (SAM)`],
[`Principle (how it works)`, `Treats each spectrum as a vector and measures the angle between two vectors; small angle = similar shape.`],
[`Problem it solves`, `Classifies pixels by spectral shape, so it is insensitive to brightness differences caused by shading and slope.`],
[`Specification in this study`, `Endmember library from Step C5; maximum angle 0.10–0.30 radian (calibrated); one classification per date.`],
[`Hyper-parameters and how they are tuned`, `Maximum angle: the value with the highest overall accuracy on reference pixels.`],
[`Data on which it works well`, `Hyperspectral data with distinct class shapes (vegetation, soil, shadow, flowers).`],
[`Why it was selected`, `Needs only one spectrum per class, works with the endmember library directly and is robust to illumination.`],
[`Key references`, `Kruse et al. (1993); Bioucas-Dias et al. (2012)`]], [2300, 7006], `Method card – Spectral angle mapper (SAM).`, 16));
K.push(H3(`Step C7 – Vegetation mask rule and edge erosion`));
K.push(...tab2('sc7', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Some flower pixels have low NDVI, and pixels at the edge of leaves are mixtures of canopy and soil.`],
[`Input`, `Class map; normalised difference vegetation index (NDVI) image.`],
[`Output → next step`, `Binary vegetation mask (1 = green canopy, stressed canopy, flower; 0 = soil, grass, shadow, unclassified) → Step C8 and Activity D.`]], [2200, 7106], `Step C7 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Keep the classes green canopy, stressed canopy and flower; remove soil, grass, shadow and unclassified pixels.`));
K.push(NL(`Apply the rule: vegetation = (NDVI > 0.6 OR flower class) AND a kept class; NDVI alone would remove yellow flowers.`));
K.push(NL(`Apply a one-pixel morphological erosion to remove mixed edge pixels.`));
K.push(P(`**Supporting studies.** NDVI: Rouse et al. (1974); NDVI threshold masks in UAV disease studies: Guo et al. (2021) (NDVI > 0.42); morphological erosion: Soille (2003); flowers and canopy spectra: Sulik and Long (2016).`));
K.push(H3(`Step C8 – Mask accuracy and transfer to all cameras`));
K.push(...tab2('sc8', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The mask must be shown to be accurate and must be applied identically to all cameras.`],
[`Input`, `Vegetation mask; independent reference pixels from the red–green–blue image.`],
[`Output → next step`, `Accepted mask on the hyperspectral grid, applied to the multispectral, red–green–blue and thermal layers → Activity D.`]], [2200, 7106], `Step C8 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Digitise independent reference pixels of each class on the red–green–blue image (for example 300 per class).`));
K.push(NL(`Compute the confusion matrix, overall accuracy and kappa coefficient; accept the mask when overall accuracy is at least 90%.`));
K.push(NL(`Multiply every resampled layer of every camera by the mask, so all cameras are measured on the same pixels.`));
K.push(P(`**Supporting studies.** Accuracy assessment: Congalton (1991); same pixels for all sensors after masking: Feng et al. (2022), Maimaitijiang et al. (2020).`));
K.push(...tab2('cerosion', [[`Aspect`, `Morphological erosion and mask accuracy assessment`],
[`Principle (how it works)`, `Erosion removes the outer pixel ring of each vegetation patch; the confusion matrix compares mask classes with reference classes.`],
[`Problem it solves`, `Removes mixed edge pixels and proves that the mask is reliable.`],
[`Specification in this study`, `Erosion with a 3 × 3 structuring element (one pixel); reference pixels from the red–green–blue image; overall accuracy ≥ 90% required.`],
[`Hyper-parameters and how they are tuned`, `Size of the structuring element (one pixel to avoid losing small plants).`],
[`Data on which it works well`, `High-resolution masks with many leaf edges.`],
[`Why it was selected`, `Simple and widely used; accuracy assessment is required to report a mask.`],
[`Key references`, `Soille (2003); Congalton (1991)`]], [2300, 7006], `Method card – Morphological erosion and mask accuracy assessment.`, 16));
K.push(H2(`Activity D – Subplot spectra and feature extraction`));
K.push(P(`Features are calculated for every subplot-date and kept in groups by type (${F('features')}). The grouping matters because one selection method is later used for each type of feature (Objective 1).`));
K.push(...fig2('features', 'g04_features.png', `Flow chart of Activity D (Steps D1–D6; Steps D7–D8 complete the feature table).`, 540));
K.push(H3(`Step D1 – Plot and subplot polygons`));
K.push(...tab2('sd1', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Each sample must cover exactly the scored subplot.`],
[`Input`, `Field layout; plot numbers; aligned images.`],
[`Output → next step`, `192 subplot polygons with codes → Step D2.`]], [2200, 7106], `Step D1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Digitise the 48 plot polygons once and add the plot number.`));
K.push(NL(`Split each plot into four quadrant subplots that match the field scoring; apply an inner buffer to exclude border rows and bunds.`));
K.push(NL(`Use the same polygons on all dates and for all cameras.`));
K.push(P(`**Supporting studies.** Plot polygons after soil masking: Liu et al. (2024), Feng et al. (2022); fixed sampling regions: Ma et al. (2026).`));
K.push(H3(`Step D2 – Subplot mean spectra`));
K.push(...tab2('sd2', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Models need one value per feature and subplot that represents the scored canopy.`],
[`Input`, `Masked layers of all cameras; subplot polygons.`],
[`Output → next step`, `One mean spectrum (and mean band values) per subplot, date and camera → Steps D3–D7 and Activity E.`]], [2200, 7106], `Step D2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Average the masked vegetation pixels inside each subplot for every band of every camera.`));
K.push(NL(`Join the covariates of Step A6 by the subplot code and date.`));
K.push(P(`**Supporting studies.** Plot-mean spectra after masking: Guo et al. (2021), Mustafa et al. (2023), Ma et al. (2026).`));
K.push(...fig2('dummyspec', 'g11_dummy_spectra.png', `Dummy example of subplot mean spectra by DI class (a) and the first derivative in the red-edge region (b). The water-vapour regions are removed.`, 560));
K.push(H3(`Step D3 – Hyperspectral spectral features`));
K.push(...tab2('sd3', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Reflectance alone does not show red-edge shifts clearly; derivatives and red-edge parameters make them visible.`],
[`Input`, `Subplot mean reflectance (483 bands).`],
[`Output → next step`, `Spectral group: reflectance (483), first derivative (483) and red-edge parameters → Objective 1 (Activities 1.2 and 1.4).`]], [2200, 7106], `Step D3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Reflectance of the 483 bands.`));
K.push(NL(`First derivative of each smoothed segment: FD(λ_{i}) = [R(λ_{i+1}) − R(λ_{i−1})] / (λ_{i+1} − λ_{i−1}); derivative bands within 10 nm of a removed region are not used.`));
K.push(NL(`Red-edge parameters: red-edge position (wavelength of the maximum first derivative between 680 and 760 nm), red-edge amplitude (that maximum value) and red-edge area (sum of the first derivative from 680 to 760 nm).`));
K.push(NL(`The second derivative is not used, because it amplifies noise at UAV signal-to-noise levels and adds hundreds of unstable variables.`));
K.push(P(`**Supporting studies.** Derivative analysis: Tsai and Philpot (1998); red edge: Horler et al. (1983), Filella and Peñuelas (1994); red-edge parameters best for the early stage of pine wilt disease from UAV hyperspectral data: Yu et al. (2021); noise amplification by derivatives: Rinnan et al. (2009).`));
K.push(P(`**Worked example (dummy data).** If R(700 nm) = 0.10 and R(704 nm) = 0.14, the first derivative at 702 nm is (0.14 − 0.10) / 4 = 0.010 nm^{−1}. If the largest first derivative between 680 and 760 nm is 0.012 nm^{−1} at 718 nm, the red-edge position is 718 nm and the amplitude is 0.012 nm^{−1}. In diseased canopies the red-edge position moves to shorter wavelengths (${F('dummyspec')}b).`));
K.push(...tab2('cfd', [[`Aspect`, `First derivative and red-edge parameters`],
[`Principle (how it works)`, `The derivative measures the slope of the spectrum; it removes constant offsets (for example brightness differences) and turns the red edge into a peak whose position and height can be measured.`],
[`Problem it solves`, `Makes the chlorophyll-related red-edge shift measurable and reduces background effects.`],
[`Specification in this study`, `Central difference on Savitzky–Golay smoothed segments; red-edge position, amplitude and area from 680–760 nm.`],
[`Hyper-parameters and how they are tuned`, `No tuning; the smoothing window (Step B3) controls the noise of the derivative.`],
[`Data on which it works well`, `Smoothed hyperspectral spectra with dense band spacing.`],
[`Why it was selected`, `Red-edge parameters were the best features for separating early-stage diseased trees from healthy trees (Yu et al., 2021).`],
[`Key references`, `Tsai and Philpot (1998); Filella and Peñuelas (1994); Yu et al. (2021)`]], [2300, 7006], `Method card – First derivative and red-edge parameters.`, 16));
K.push(H3(`Step D4 – Vegetation indices`));
K.push(...tab2('sd4', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `General physiological changes (pigments, structure, water) are captured best by published indices that have known meaning.`],
[`Input`, `Subplot mean reflectance.`],
[`Output → next step`, `Index group (published indices + red-edge parameters; the searched indices of Activity 1.3 are added later) → Activity 1.4.`]], [2200, 7106], `Step D4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Compute 48 published hyperspectral indices: the 39 base indices in five groups – greenness and canopy structure (17), pigment ratios (12), photosynthesis and stress (4), water (3) and SWIR disease–water (3) – plus 9 SWIR disease indices (DWSI-2, DWSI-3, DWSI-5, NDWI, moisture stress index, NDII, RBI_{M}, NDBI and RBI_{R}); the indices used by Ma et al. (2026) are all included.`));
K.push(NL(`Check every formula against the original paper and use the nearest available band.`));
K.push(NL(`Index definitions, formulas and original references are given in Chapter 7 (${T('hsidx')} and ${T('hsidx2')}); recent disease-sensing studies that used each index group are listed with the tables.`));
K.push(P(`**Supporting studies.** Index groups for disease detection: Mahlein et al. (2013), Huang et al. (2014), Ma et al. (2026); pigment indices: Gamon et al. (1992), Gitelson et al. (2003), Merzlyak et al. (1999); water and disease indices: Gao (1996), Apan et al. (2004); PSRI and PSSRb for rice bacterial leaf blight: Das et al. (2015).`));
K.push(...tab2('cvi', [[`Aspect`, `Vegetation indices`],
[`Principle (how it works)`, `Arithmetic combinations (differences, ratios, normalised differences) of reflectance at wavelengths sensitive to a plant property, which cancel part of the illumination and background effect.`],
[`Problem it solves`, `Turns many bands into a few physiologically meaningful variables that can be compared with other studies and sensors.`],
[`Specification in this study`, `48 published hyperspectral indices (39 base + 9 SWIR disease indices) and 3 red-edge parameters, 12 multispectral indices and 6 colour indices (Chapter 7).`],
[`Hyper-parameters and how they are tuned`, `No hyper-parameters; formulas fixed by the original papers.`],
[`Data on which it works well`, `Canopy reflectance at UAV and satellite scales.`],
[`Why it was selected`, `Interpretable, transferable and easy to apply to cheaper sensors.`],
[`Key references`, `Mahlein et al. (2013); Huang et al. (2014); Ma et al. (2026)`]], [2300, 7006], `Method card – Vegetation indices.`, 16));
K.push(H3(`Step D5 – Texture features from the grey-level co-occurrence matrix (GLCM)`));
K.push(...tab2('sd5', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `White pustules and chlorotic patches make the canopy surface heterogeneous; spectra do not record this spatial pattern.`],
[`Input`, `Masked hyperspectral cube; red–green–blue image at native resolution; multispectral and thermal layers.`],
[`Output → next step`, `Texture groups of each camera → Activity 1.5 (hyperspectral) and Activity 1.6 (other cameras).`]], [2200, 7106], `Step D5 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Hyperspectral: reduce the cube with principal component analysis and keep the first three components (cumulative variance above 95%); compute texture on these three component images (Activity 1.5).`));
K.push(NL(`For every image used, quantise the grey levels to 32 levels and compute the grey-level co-occurrence matrix (GLCM) in a 3 × 3 moving window at distance 1, averaged over four directions (0°, 45°, 90°, 135°).`));
K.push(NL(`Compute eight texture measures: mean, variance, homogeneity, contrast, dissimilarity, entropy, second moment and correlation (${T('rgbfeat')}); average them over the vegetation pixels of the subplot.`));
K.push(NL(`Red–green–blue: texture of the R, G and B bands (24 features); multispectral: texture of the five bands (40); thermal: texture of the temperature image (8).`));
K.push(P(`**Supporting studies.** GLCM: Haralick et al. (1973), Hall-Beyer (2017); texture from principal-component images of UAV hyperspectral data: Guo et al. (2021), Ma et al. (2026); texture as a feature group for Fusarium head blight: Liu et al. (2020).`));
K.push(...tab2('glcmex', [[`Image row`, `Grey levels of the 4 × 4 image`, `GLCM counts (grey levels 0–3)`, `Texture measure`, `Value`],
[`1`, `0 0 1 1`, `4 2 1 0`, `contrast`, `0.583`],
[`2`, `0 0 1 1`, `2 4 0 0`, `homogeneity`, `0.808`],
[`3`, `0 2 2 2`, `1 0 6 1`, `dissimilarity`, `0.417`],
[`4`, `2 2 3 3`, `0 0 1 2`, `entropy`, `2.095`],
[``, ``, `24 neighbour pairs in total`, `second moment`, `0.146`]], [1300, 2300, 2500, 1900, 1306], `Worked example (dummy data): grey-level co-occurrence matrix (horizontal neighbours, both directions) and texture of a small image. Each count is divided by 24 to give probabilities before the measures are computed.`, 17));
K.push(...tab2('cglcm', [[`Aspect`, `Grey-level co-occurrence matrix (GLCM) texture`],
[`Principle (how it works)`, `Counts how often pairs of grey levels occur next to each other; statistics of this matrix describe smoothness (homogeneity), local variation (contrast, dissimilarity), disorder (entropy) and uniformity (second moment).`],
[`Problem it solves`, `Describes the spatial pattern of pustules, chlorotic patches and canopy gaps, which spectra cannot.`],
[`Specification in this study`, `32 grey levels, 3 × 3 window, distance 1, four directions averaged, eight measures, averaged over vegetation pixels.`],
[`Hyper-parameters and how they are tuned`, `Window size, distance and number of grey levels; fixed at small values because pustules are only a few pixels wide at 2.2 cm; 5 × 5 window is tested as a check.`],
[`Data on which it works well`, `High-resolution images where the target produces a spatial pattern (2–5 cm pixels).`],
[`Why it was selected`, `The most widely used and best-understood texture method in remote sensing; used in the main white-rust-like disease studies.`],
[`Key references`, `Haralick et al. (1973); Hall-Beyer (2017); Guo et al. (2021)`]], [2300, 7006], `Method card – Grey-level co-occurrence matrix (GLCM) texture.`, 16));
K.push(...tab2('cpca', [[`Aspect`, `Principal component analysis (PCA)`],
[`Principle (how it works)`, `Rotates correlated variables into uncorrelated components ordered by the variance they explain.`],
[`Problem it solves`, `Reduces 483 correlated bands to three images that keep most of the information, so texture is computed on 3 images instead of 483.`],
[`Specification in this study`, `Computed on the masked vegetation pixels of all dates (training data); first three components kept (cumulative variance above 95%).`],
[`Hyper-parameters and how they are tuned`, `Number of components: the smallest number with at least 95% cumulative variance (${F('dummyrelief')}b).`],
[`Data on which it works well`, `Many highly correlated variables, such as hyperspectral bands.`],
[`Why it was selected`, `Used in exactly this role by Guo et al. (2021) and Ma et al. (2026).`],
[`Key references`, `Jolliffe and Cadima (2016); Guo et al. (2021); Ma et al. (2026)`]], [2300, 7006], `Method card – Principal component analysis (PCA).`, 16));
K.push(H3(`Step D6 – Multispectral and red–green–blue features`));
K.push(...tab2('sd6', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The cheaper cameras need their own features so that their value can be compared with the hyperspectral camera.`],
[`Input`, `Masked subplot means of the multispectral and red–green–blue images.`],
[`Output → next step`, `Multispectral group (5 bands, 12 indices, 10 two-band normalised differences, 40 texture features) and colour group (6 colour indices, hue–saturation–value means, 24 texture features) → Activity 1.6.`]], [2200, 7106], `Step D6 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Multispectral: band reflectance, NDVI, GNDVI, NDRE, CIgreen, CIrededge, MTCI, OSAVI, SAVI, TCARI, MCARI, MSR, PSRI and the ten normalised differences of the five bands.`));
K.push(NL(`Red–green–blue: excess green, excess red, excess green minus excess red, VARI, GLI, NGRDI and mean hue, saturation and value.`));
K.push(NL(`Formulas are in Chapter 7.`));
K.push(P(`**Supporting studies.** Multispectral indices and texture for wheat powdery mildew: Liu et al. (2024); multispectral and very-high-resolution indices for wheat rusts: Blasch et al. (2023); colour indices: Woebbecke et al. (1995), Meyer and Neto (2008).`));
K.push(H3(`Step D7 – Thermal features`));
K.push(...tab2('sd7', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Infection changes transpiration and canopy temperature, but temperature also changes with weather and time.`],
[`Input`, `Masked thermal subplot values; air temperature; healthy-plot temperatures of the same date.`],
[`Output → next step`, `Thermal group → Activity E (normalisation) and Activity 1.6.`]], [2200, 7106], `Step D7 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Canopy temperature: mean, median, standard deviation, 10th and 90th percentiles of the vegetation pixels.`));
K.push(NL(`Normalised thermal features (Step E1): canopy minus air temperature, normalised relative canopy temperature, crop water stress index and difference from the healthy plots of the same date and variety.`));
K.push(NL(`Thermal texture (Step D5).`));
K.push(P(`**Supporting studies.** Thermal features for powdery mildew: Feng et al. (2022), Liu et al. (2024); canopy minus air temperature for downy mildew from a UAV: Calderón et al. (2014); reviews: Pineda et al. (2021), Messina and Modica (2020).`));
K.push(H3(`Step D8 – Feature table`));
K.push(...tab2('sd8', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `All later steps need one table layout for every camera so that sensor sets are simple joins.`],
[`Input`, `Features of Steps D3–D7.`],
[`Output → next step`, `One table per camera with identifiers, labels, covariates and features → Activities E and F.`]], [2200, 7106], `Step D8 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Columns: identifiers (date, days after inoculation, plot, subplot, replication, treatment, variety, inoculation timing, fold), labels (score, class, detection label), covariates (days after inoculation, variety, inoculation timing, growth stage, weather summaries) and features with a group prefix (R_, FD_, RE_, VI_, TX_, TH_).`));
K.push(NL(`Rows: one per subplot-date.`));
K.push(P(`**Supporting studies.** Structured multi-sensor feature tables: Maimaitijiang et al. (2020), Feng et al. (2022).`));
K.push(...tab2('featcount', [[`Camera`, `Feature groups`, `Approximate number`],
[`Hyperspectral`, `reflectance 483, first derivative 483, red-edge parameters 3, published indices 48 (39 base + 9 SWIR), principal-component texture 24 (+ searched indices and TTFI)`, `≈ 1040`],
[`Multispectral`, `5 bands, 12 indices, 10 normalised differences, 40 texture`, `67`],
[`Red–green–blue`, `6 colour indices, 3 colour means, 24 texture`, `33`],
[`Thermal`, `5 temperature statistics, 4 normalised temperatures, 8 texture`, `17`],
[`Covariates`, `days after inoculation, variety, inoculation timing, growth stage, weather (T_{max}, T_{min}, RH, rainfall)`, `not used as disease features`]], [1800, 5600, 1906], `Feature groups before selection.`, 17));
K.push(H2(`Activity E – Normalisation and data preparation`));
K.push(P(`Normalisation removes effects that are not caused by the disease (weather, date, variety, units) and prepares the features for the models (${F('normal')}). Step E1 is done once on all data because it does not use the labels; Steps E2–E4 use statistics that are computed on the training part of each fold only. Date-to-date consistency of reflectance relies on the calibration panels flown on every date (Step B1).`));
K.push(...fig2('normal', 'g25_normalisation.png', `Flow chart of Activity E (Steps E1–E4).`, 540));
K.push(H3(`Step E1 – Thermal normalisation`));
K.push(...tab2('se1', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Canopy temperature changes with air temperature, radiation and time of flight, which can hide the disease effect.`],
[`Input`, `Canopy temperature statistics; air temperature; wet and dry reference temperatures.`],
[`Output → next step`, `Normalised thermal features → Activity 1.6 and Objectives 2–3.`]], [2200, 7106], `Step E1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Canopy minus air temperature: CTD = T_{c} − T_{air}.`));
K.push(NL(`Normalised relative canopy temperature over the field on that date: NRCT = (T_{c} − T_{min}) / (T_{max} − T_{min}).`));
K.push(NL(`Crop water stress index: CWSI = (T_{c} − T_{wet}) / (T_{dry} − T_{wet}) with wet and dry references in the field.`));
K.push(NL(`Difference from healthy plots of the same date and variety (Step E2).`));
K.push(P(`**Supporting studies.** Normalisation of canopy temperature by air temperature: Idso et al. (1981), Pineda et al. (2021); canopy minus air temperature for downy mildew detection from a UAV: Calderón et al. (2014); thermal indices and environmental effects: Jones et al. (2009), Maes and Steppe (2012), Oerke et al. (2006).`));
K.push(P(`**Worked example (dummy data).** A subplot has T_{c} = 24.6 °C when T_{air} = 22.0 °C, so CTD = +2.6 °C. On that date the field minimum and maximum canopy temperatures are 21.8 and 26.2 °C, so NRCT = (24.6 − 21.8) / (26.2 − 21.8) = 0.64.`));
K.push(H3(`Step E2 – Healthy-plot normalisation`));
K.push(...tab2('se2', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Early disease effects are small compared with the differences caused by date, crop age and variety; a same-day, same-variety healthy reference removes most of them.`],
[`Input`, `Features of all subplots; features of the healthy plots of the same date and variety in the training part (two or three plots of different inoculation timings, Step F1).`],
[`Output → next step`, `Healthy-normalised features → Objective 3 (all features) and thermal difference features (Objectives 1–2).`]], [2200, 7106], `Step E2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`For every feature, date and variety, compute the mean and standard deviation of the healthy subplots of that variety in the training part (8–12 subplots).`));
K.push(NL(`Normalised value: z_{h} = (x − mean_{healthy}) / SD_{healthy}.`));
K.push(NL(`Apply the same healthy-plot reference to the test samples of that date and variety.`));
K.push(P(`**Supporting studies.** Healthy references for thermal disease detection: Oerke et al. (2006); healthy references in pre-visual detection: Zarco-Tejada et al. (2018), Poblete et al. (2023); pre-symptomatic hyperspectral detection: Zhu et al. (2017).`));
K.push(P(`**Worked example (dummy data).** On one date the healthy plots of variety V1 have mean canopy temperature 23.8 °C (standard deviation 0.4 °C). An inoculated V1 subplot at 24.6 °C gets z_{h} = (24.6 − 23.8) / 0.4 = +2.0, that is, two healthy standard deviations warmer.`));
K.push(...tab2('chealthy', [[`Aspect`, `Healthy-plot (control) normalisation`],
[`Principle (how it works)`, `Expresses each value as its distance from healthy plants measured on the same day, of the same variety and age, in units of their natural variation.`],
[`Problem it solves`, `Removes date, weather, crop-age and variety effects so that only the disease effect remains; essential when symptoms are not yet visible.`],
[`Specification in this study`, `Reference: healthy plots of the same date and variety in the training part (rotated across folds, Step F1); mean and standard deviation per feature.`],
[`Hyper-parameters and how they are tuned`, `No hyper-parameters.`],
[`Data on which it works well`, `Experiments with healthy controls on every date; thermal and early-stage spectral data.`],
[`Why it was selected`, `Simple and directly justified by the design (one healthy plot for every treatment).`],
[`Key references`, `Oerke et al. (2006); Zarco-Tejada et al. (2018)`]], [2300, 7006], `Method card – Healthy-plot (control) normalisation.`, 16));
K.push(H3(`Step E3 – Standardisation (z-score) with training statistics`));
K.push(...tab2('se3', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Features have different units and ranges (reflectance 0–1, temperature 15–30 °C, texture 0–1000); distance- and gradient-based models are dominated by large-range features.`],
[`Input`, `Selected features of the training part and test part of each fold.`],
[`Output → next step`, `Standardised features (mean 0, standard deviation 1 in the training part) → all models.`]], [2200, 7106], `Step E3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Compute the mean and standard deviation of every feature on the training part of the fold.`));
K.push(NL(`Standardise: z = (x − mean_{train}) / SD_{train}, for training and test samples alike.`));
K.push(NL(`Repeat for every fold; the test part never contributes to the statistics.`));
K.push(P(`**Supporting studies.** Pre-processing inside resampling: Kuhn and Johnson (2013); feature scaling for support vector machines and neural networks: Mountrakis et al. (2011), Kattenborn et al. (2021).`));
K.push(P(`**Worked example (dummy data).** In one training part NDVI has mean 0.72 and standard deviation 0.08. A test subplot with NDVI = 0.60 is standardised to z = (0.60 − 0.72) / 0.08 = −1.5.`));
K.push(...tab2('czscore', [[`Aspect`, `z-score standardisation`],
[`Principle (how it works)`, `Subtracts the mean and divides by the standard deviation, so every feature has mean 0 and unit variance.`],
[`Problem it solves`, `Puts features with different units on one scale so that no feature dominates distances, kernels or gradient steps.`],
[`Specification in this study`, `Training statistics of each fold; applied to all models (tree models do not need it but receive the same input for simplicity).`],
[`Hyper-parameters and how they are tuned`, `No hyper-parameters.`],
[`Data on which it works well`, `Mixed feature types (reflectance, indices, texture, temperature).`],
[`Why it was selected`, `Required by support vector machines, k-nearest neighbours, partial least squares and neural networks.`],
[`Key references`, `Kuhn and Johnson (2013)`]], [2300, 7006], `Method card – z-score standardisation.`, 16));
K.push(H3(`Step E4 – Class weights`));
K.push(...tab2('se4', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The severity classes have unequal sizes (for example 512 healthy vs 120 grade-9 samples); models tend to ignore small classes.`],
[`Input`, `Class counts of the training part.`],
[`Output → next step`, `Class weights for the loss functions of all classifiers → Objectives 2–3.`]], [2200, 7106], `Step E4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Weight of class c: w_{c} = N / (k × n_{c}), where N is the number of training samples, k the number of classes and n_{c} the size of class c.`));
K.push(NL(`Use the weights in the loss (support vector machine, random forest, extreme gradient boosting, neural networks).`));
K.push(NL(`Report macro-averaged metrics, which give each class equal importance.`));
K.push(P(`**Supporting studies.** Class imbalance in deep learning: Johnson and Khoshgoftaar (2019); macro-averaged metrics: Sokolova and Lapalme (2009).`));
K.push(P(`**Worked example (dummy data).** With N = 1280 training samples, k = 6 classes and 80 samples of grade 9, the weight of grade 9 is 1280 / (6 × 80) = 2.67, while the weight of a class with 341 samples is 1280 / (6 × 341) = 0.63.`));
K.push(H2(`Activity F – Validation design and tuning`));
K.push(H3(`Step F1 – Leave-one-replication-out (LORO) outer folds`));
K.push(...tab2('sf1', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Subplots of one plot, and plots of one replication, are similar; random splits put near-identical samples in training and test data and inflate accuracy.`],
[`Input`, `Labelled feature tables.`],
[`Output → next step`, `Three outer folds → all models of Objectives 2 and 3.`]], [2200, 7106], `Step F1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Fold 1 tests replication R1, fold 2 tests R2, fold 3 tests R3 (leave-one-replication-out, LORO).`));
K.push(NL(`The 12 healthy plots are rotated so that every fold contains one healthy plot of each inoculation timing and at least one of each variety (${T('healthyrot')}). Every training part then holds two or three healthy plots of every variety, which the healthy-plot normalisation (Step E2) needs, and every test fold contains healthy samples of all three varieties.`));
K.push(NL(`All dates and all four subplots of a plot stay in the same fold; each test fold has about 640 post-symptomatic (or 192 pre-symptomatic) samples.`));
K.push(NL(`The same three folds are used for every sensor set, task and model.`));
K.push(P(`**Supporting studies.** Grouped (blocked) cross-validation: Roberts et al. (2017); healthy references of the same variety needed for normalisation: Oerke et al. (2006), Zarco-Tejada et al. (2018); spatial validation shows that random splits overestimate accuracy: Ploton et al. (2020); the random 7:3 split of Ma et al. (2026) is the optimistic design this step avoids, while its cross-year test supports testing on independent units.`));
K.push(...tab2('healthyrot', [[`Outer fold`, `Inoculated plots tested`, `Healthy plots tested (variety–timing, plot number)`],
[`1`, `replication R1 (plots 37–48)`, `V1-D1 (7), V2-D2 (2), V3-D3 (10), V1-D4 (12)`],
[`2`, `replication R2 (plots 25–36)`, `V2-D1 (5), V3-D2 (8), V1-D3 (4), V2-D4 (1)`],
[`3`, `replication R3 (plots 13–24)`, `V3-D1 (3), V1-D2 (9), V2-D3 (11), V3-D4 (6)`]], [1500, 3300, 4506], `Rotation of the 12 healthy plots across the outer folds: each fold has every inoculation timing once and every variety at least once.`, 17));
K.push(...fig2('validation', 'g09_validation.png', `Leave-one-replication-out outer folds with the rotated healthy plots, and the inner cross-validation used for selection and tuning.`, 520));
K.push(H3(`Step F2 – Nested inner cross-validation and hyper-parameter tuning`));
K.push(...tab2('sf2', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Feature selection and tuning done on all data (or on the test fold) give over-optimistic accuracy.`],
[`Input`, `Training part of each outer fold.`],
[`Output → next step`, `Selected features, tuned hyper-parameters and early-stopping epochs for each outer fold → final training and one test prediction.`]], [2200, 7106], `Step F2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Inside the training replications, make three inner folds grouped by plot.`));
K.push(NL(`Run all label-based steps inside this inner loop: index search, SHAP-CARS, ReliefF, mRMR, TTFI search, sequential floating forward selection, grid search of hyper-parameters and early stopping of neural networks (validation on plots that are not used for training).`));
K.push(NL(`Choose the hyper-parameters with the best mean inner score (macro-F1 for classes, root-mean-square error for the score).`));
K.push(NL(`Retrain the model on the whole training part with these settings and predict the test replication once.`));
K.push(P(`**Supporting studies.** Nested cross-validation: Varma and Simon (2006), Cawley and Talbot (2010); selection bias when features are chosen outside the folds: Ambroise and McLachlan (2002).`));
K.push(...tab2('cnested', [[`Aspect`, `Grouped nested cross-validation with grid search`],
[`Principle (how it works)`, `An outer loop estimates accuracy on unseen replications; an inner loop inside the training part chooses features and hyper-parameters. Grid search tries every combination in a small grid.`],
[`Problem it solves`, `Gives an almost unbiased accuracy estimate and prevents information from the test replication entering the model.`],
[`Specification in this study`, `Outer: 3 folds (leave-one-replication-out); inner: 3 folds grouped by plot; grids in ${T('mlgrid')} and Step 2.3.8.`],
[`Hyper-parameters and how they are tuned`, `The grids themselves; kept small (2–5 values per parameter) to limit overfitting of the selection.`],
[`Data on which it works well`, `Small, grouped datasets such as plots × dates.`],
[`Why it was selected`, `Standard practice for honest accuracy; required because many label-based steps are used.`],
[`Key references`, `Varma and Simon (2006); Cawley and Talbot (2010); Roberts et al. (2017)`]], [2300, 7006], `Method card – Grouped nested cross-validation with grid search.`, 16));
K.push(H3(`Step F3 – Leakage checklist`));
K.push(...tab2('sf3', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A single step done on all data can leak test information into the model.`],
[`Input`, `All steps of the methodology.`],
[`Output → next step`, `Checklist of where every step is run (${T('leak')}) → applied in all objectives.`]], [2200, 7106], `Step F3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`List every step that uses labels or data statistics.`));
K.push(NL(`Assign it to "once on all data" (no labels), "training part" (statistics) or "inner folds" (labels).`));
K.push(NL(`Check the code of every objective against the list before running the final models.`));
K.push(P(`**Supporting studies.** Ambroise and McLachlan (2002); Kuhn and Johnson (2013).`));
K.push(...tab2('leak', [[`Step`, `Uses labels?`, `Where it is run`],
[`Activities B–D (pre-processing, mask, features)`, `no`, `once, on all data`],
[`E1 (thermal normalisation)`, `no`, `once, on all data`],
[`E2 (healthy-plot normalisation)`, `no (uses healthy plots)`, `training healthy plots → applied to test data`],
[`E3–E4 (standardisation, class weights)`, `no (statistics)`, `training part of each fold`],
[`Covariate coding (Step A6)`, `no`, `once; standardised with training statistics`],
[`Within-group redundancy (|r| ≥ 0.95), variance inflation factor`, `no`, `training part of each fold`],
[`NDSI/RSI and White Rust Index search, SHAP-CARS, ReliefF, mRMR, TTFI search`, `yes`, `inner folds only`],
[`Sequential floating forward selection, hyper-parameter tuning, early stopping`, `yes`, `inner folds only`],
[`Final evaluation`, `yes`, `test replication, once`],
[`Independent testing (Bharatpur)`, `yes`, `once, with frozen final models; never used for selection, tuning or training`]], [4300, 1900, 3106], `Where each step is run so that no information from the test replication enters the model.`, 17));
K.push(...tab2('foldsize', [[`Dataset`, `Training part per outer fold`, `Test part per outer fold`, `Inner folds`],
[`Post-symptomatic (1920 per camera)`, `≈ 1280 samples`, `≈ 640 samples`, `3, grouped by plot`],
[`Pre-symptomatic (576 per camera)`, `≈ 384 samples`, `≈ 192 samples`, `3, grouped by plot`]], [2800, 2600, 1900, 2006], `Approximate sizes of the training and test parts.`, 17));
K.push(H1(`3. Objective 1 – Characterisation of white rust through multimodal UAV sensing`));
K.push(P(`Objective 1 describes how each camera sees white rust and selects the features that carry disease information, at two stages. At the post-symptomatic stage it uses the 1920 post-symptomatic samples of each camera with the disease index as target (Activities 1.1–1.7). At the pre-symptomatic stage it uses the 576 pre-symptomatic samples of each camera with later-infected vs healthy as target (Activity 1.8). For description and interpretation the steps are run on all samples of a stage; for prediction (Objectives 2 and 3) exactly the same steps are repeated inside the training part of every fold (Step F2), so the test replication never influences the selection.`));
K.push(...fig2('obj1', 'g05_obj1.png', `Flow chart of Objective 1 (Activities 1.1–1.8).`, 540));
K.push(...tab2('o1act', [[`Activity`, `Steps`, `Technique (one per feature type)`, `Output`],
[`1.1 Response analysis`, `1.1.1–1.1.3`, `mean spectra, first derivative, Pearson correlation`, `response figures; responsive regions`],
[`1.2 Optimal wavelengths`, `1.2.1–1.2.4`, `NDSI/RSI maps → SHAP-CARS`, `10–15 optimal wavelengths (OW)`],
[`1.3 Spectral index construction`, `1.3.1–1.3.3`, `exhaustive two-band and three-band search`, `best NDSI, RSI and White Rust Index (WRI)`],
[`1.4 Vegetation index selection`, `1.4.1–1.4.3`, `redundancy filter → ReliefF / RReliefF`, `5–8 selected indices`],
[`1.5 Texture selection and TTFI`, `1.5.1–1.5.4`, `principal-component texture → mRMR → TTFI`, `6 texture features + best TTFI`],
[`1.6 Disease-specific feature sets`, `1.6.1–1.6.4`, `same rules for other cameras → variance inflation factor`, `feature set of each camera; treatment response`],
[`1.7 Biochemical and biophysical basis`, `1.7.1–1.7.6`, `paired comparisons, analysis of variance, within-date correlation`, `disease effect by date and growth stage; parameter–feature links`],
[`1.8 Pre-symptomatic characterisation`, `1.8.1–1.8.5`, `the same steps with the label later-infected vs healthy (576 samples per camera)`, `pre-symptomatic response; earliest-responding features; pre-symptomatic feature set`]], [2400, 1100, 3000, 2806], `Activities of Objective 1.`, 17));
K.push(H2(`The feature-selection rule: one method for each type of feature`));
K.push(P(`Pooling all features (about 1150 for the four cameras) and selecting from one big pool would be unstable, would keep many near-duplicates and would let the hundreds of spectral bands swamp the small thermal and texture groups (Hughes, 1968; Guyon and Elisseeff, 2003; Dormann et al., 2013; Ghamisi et al., 2019). Selection is therefore done in four stages, and in Stage 2 one method is used for each type of feature, the method that best suits the nature of that type and that was used for the same type in the DT-EDNet study (Ma et al., 2026) (${F('selection')}).`));
K.push(...tab2('stages', [[`Stage`, `What is done`, `Uses labels?`, `Where in this document`],
[`0. Build groups`, `calculate features with physical meaning (no second derivative)`, `no`, `Activity D`],
[`1. Redundancy within groups`, `remove near-constant features; keep one feature of every cluster with |r| ≥ 0.95 (indices, texture, thermal, multispectral and colour groups)`, `no`, `Steps 1.4.2, 1.5.3, 1.6.1`],
[`2. Selection within groups (one method per type)`, `spectral bands: SHAP-CARS; vegetation indices: ReliefF (RReliefF for the score); texture: mRMR; constructed indices: exhaustive search; thermal and multispectral bands: kept`, `yes`, `Activities 1.2–1.5`],
[`3. Redundancy across groups`, `pool the survivors; variance inflation factor below 10`, `no`, `Step 1.6.2`],
[`4. Final compact set (machine learning only)`, `sequential floating forward selection with each model, at most 15 features`, `yes`, `Step 2.1.4`]], [2200, 4400, 1100, 1606], `The four selection stages.`, 17));
K.push(...fig2('selection', 'g08_selection.png', `One feature-selection method for each feature type, run inside the training part of each fold.`, 540));
K.push(H2(`Activity 1.1 – Response analysis`));
K.push(H3(`Step 1.1.1 – Mean spectra and first-derivative curves by severity grade`));
K.push(...tab2('s111', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Shows how the spectrum changes with severity before any selection and gives the physiological basis for later results.`],
[`Input`, `Subplot mean reflectance and first derivative (post-symptomatic).`],
[`Output → next step`, `Response figures (${F('dummyspec')}) and a list of responsive regions → Activities 1.2–1.3 (interpretation).`]], [2200, 7106], `Step 1.1.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Average the subplot spectra of each grade (0, 1, 3, 5, 7, 9) and plot them with ± one standard deviation.`));
K.push(NL(`Plot the first derivative in the red edge (680–760 nm) for each grade.`));
K.push(NL(`Describe the changes: visible rise from chlorophyll loss, shift of the red edge to shorter wavelengths, near-infrared fall from leaf damage, short-wave-infrared rise from water loss.`));
K.push(P(`**Supporting studies.** Spectral response by severity level: Mahlein et al. (2013), Guo et al. (2021), Ma et al. (2026); red-edge shift under stress: Horler et al. (1983), Filella and Peñuelas (1994).`));
K.push(H3(`Step 1.1.2 – Correlation of each feature with the severity score`));
K.push(...tab2('s112', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Quantifies how strongly each feature follows severity and gives the direction of the response.`],
[`Input`, `All features of each camera.`],
[`Output → next step`, `Correlation table and correlation curves → interpretation; used again in Steps 1.3 and 1.5.`]], [2200, 7106], `Step 1.1.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Compute the Pearson correlation coefficient r between each feature and the severity score.`));
K.push(NL(`Plot r against wavelength for reflectance and first derivative (correlation curve).`));
K.push(NL(`Report r with its sign; p-values are not used for selection because subplots of one plot are related.`));
K.push(P(`**Supporting studies.** Correlation of indices and texture with severity: Ma et al. (2026), Guo et al. (2021); univariate feature screening: Liu et al. (2020).`));
K.push(H3(`Step 1.1.3 – Response by variety, inoculation timing, growth stage, days after inoculation and weather`));
K.push(...tab2('s113', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A feature may respond in one variety, crop age or growth stage and not in another; treatments, stage and weather must be considered.`],
[`Input`, `Responsive features; covariates (Step A6).`],
[`Output → next step`, `Treatment-wise response figures → Step 1.6.3 and Objective 2 robustness (Activity 2.6).`]], [2200, 7106], `Step 1.1.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Plot the main features against days after inoculation for each variety (V1 PM 26, V2 Pusa Vijay, V3 PM 37) and inoculation timing (D1–D4).`));
K.push(NL(`Draw the response curves separately for the three growth stages (vegetative, flowering, pod formation), because yellow flowers and pods change canopy reflectance.`));
K.push(NL(`Compare inoculated plots with healthy plots of the same variety on every date.`));
K.push(NL(`Plot the disease progress (mean severity per date) together with the 7-day weather summaries and the favourable days since inoculation.`));
K.push(P(`**Supporting studies.** Treatment-wise and stage-wise disease response: Liu et al. (2024), Blasch et al. (2023), Feng et al. (2022); flowering effects on Brassica canopy spectra: Sulik and Long (2016); weather and white rust development: Chattopadhyay et al. (2011).`));
K.push(H2(`Activity 1.2 – Optimal wavelengths with Shapley additive explanations and competitive adaptive reweighted sampling (SHAP-CARS)`));
K.push(P(`The hyperspectral camera gives 483 reflectance bands and 483 first-derivative bands. Activity 1.2 reduces them to 10–15 optimal wavelengths (OW) in two stages: first the effective ranges are found from two-band index maps, then Shapley additive explanations combined with competitive adaptive reweighted sampling (SHAP-CARS) select the optimal wavelengths inside these ranges (Ma et al., 2026).`));
K.push(H3(`Step 1.2.1 – Effective wavelength ranges from normalised difference spectral index (NDSI) and ratio spectral index (RSI) maps`));
K.push(...tab2('s121', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Many regions of the spectrum carry no disease information; searching all bands wastes time and adds noise.`],
[`Input`, `Subplot reflectance (training part).`],
[`Output → next step`, `Effective wavelength ranges (regions where index pairs relate strongly to severity) → Step 1.2.2; the best pairs → Step 1.3.1.`]], [2200, 7106], `Step 1.2.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`For every pair of bands (λ_{1}, λ_{2}) compute the normalised difference spectral index NDSI and the ratio spectral index RSI (equations below); with 483 bands there are 116 403 pairs for each index.`));
K.push(NL(`Compute the coefficient of determination R² between each index and the severity score and draw R² contour maps (${F('dummyndsi')}).`));
K.push(NL(`Effective ranges = the wavelength regions that take part in pairs with R² ≥ 0.5 (as in Ma et al., 2026); if no pair reaches 0.5, use the regions of the top 5% of pairs.`));
K.push(P(`**Supporting studies.** Two-band NDSI and RSI searches and R² contour maps: Ma et al. (2026); optimised two-band indices for wheat diseases: Huang et al. (2014).`));
K.push(EQ(`NDSI(λ_{1}, λ_{2}) = (R_{λ1} − R_{λ2}) / (R_{λ1} + R_{λ2});      RSI(λ_{1}, λ_{2}) = R_{λ1} / R_{λ2}`));
K.push(P(`**Worked example (dummy data).** With R_{760} = 0.45 and R_{550} = 0.09, NDSI(760, 550) = (0.45 − 0.09) / (0.45 + 0.09) = 0.667 and RSI(760, 550) = 5.0. In a diseased subplot with R_{760} = 0.38 and R_{550} = 0.11 the values fall to 0.551 and 3.45.`));
K.push(...fig2('dummyndsi', 'g14_dummy_ndsi.png', `Dummy example of an R² contour map of NDSI(λ₁, λ₂) against the severity score. The star marks the best pair; the bright regions define the effective ranges.`, 400));
K.push(...tab2('cndsi', [[`Aspect`, `Exhaustive two-band index search (NDSI and RSI maps)`],
[`Principle (how it works)`, `Every pair of bands is turned into a normalised difference and a ratio; the relation of each index with severity is mapped, which shows which band combinations carry disease information.`],
[`Problem it solves`, `Finds disease-sensitive band combinations without prior assumptions and narrows the search for later selection.`],
[`Specification in this study`, `All 116 403 pairs of the 483 bands; R² with the severity score on the training part; threshold R² ≥ 0.5.`],
[`Hyper-parameters and how they are tuned`, `Threshold for the effective ranges (0.5, from Ma et al., 2026); checked so that the ranges are not narrower than about 20 nm.`],
[`Data on which it works well`, `Hyperspectral data with a continuous target (severity score).`],
[`Why it was selected`, `Simple, visual and directly linked to index construction (Step 1.3.1).`],
[`Key references`, `Ma et al. (2026); Huang et al. (2014)`]], [2300, 7006], `Method card – Exhaustive two-band index search (NDSI and RSI maps).`, 16));
K.push(H3(`Step 1.2.2 – Shapley additive explanations (SHAP) pre-screening of the bands`));
K.push(...tab2('s122', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Inside the effective ranges there are still hundreds of correlated bands; a quick, model-based ranking removes clearly unimportant bands before the slower CARS step.`],
[`Input`, `Reflectance and first-derivative bands inside the effective ranges, plus the first-derivative bands of the red edge (680–760 nm), which are always kept as candidates (training part).`],
[`Output → next step`, `Top 40% of bands by mean absolute Shapley value → Step 1.2.3.`]], [2200, 7106], `Step 1.2.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Put the reflectance and first-derivative bands in one pool, because they are two forms of the same spectral information (one feature type); label each band as R_{λ} (reflectance) or FD_{λ} (first derivative).`));
K.push(NL(`Add the red-edge first-derivative bands (680–760 nm) even if the effective ranges miss part of the red edge, because the red-edge shift is a known disease indicator.`));
K.push(NL(`Train a tree ensemble (extreme gradient boosting, 300 trees, depth 4, learning rate 0.05) to predict the severity score from the bands; tree models do not need standardised inputs.`));
K.push(NL(`Compute the Shapley additive explanation (SHAP) value of every band for every training sample with the tree explainer.`));
K.push(NL(`Rank bands by the mean absolute SHAP value and keep the top 40% (${F('dummyshap')}a).`));
K.push(P(`**Supporting studies.** Shapley values: Lundberg and Lee (2017), Lundberg et al. (2020); SHAP-based band selection: Ma et al. (2026); red edge as a disease indicator: Filella and Peñuelas (1994), Yu et al. (2021).`));
K.push(...tab2('cshap', [[`Aspect`, `Shapley additive explanations (SHAP)`],
[`Principle (how it works)`, `From cooperative game theory: the contribution of a feature is its average effect on the prediction over all possible orders in which features are added to the model; for tree models it is computed exactly and quickly.`],
[`Problem it solves`, `Ranks bands by their real contribution to a non-linear model, including interactions, which simple correlation misses.`],
[`Specification in this study`, `Tree explainer on an extreme gradient boosting model trained on the training part; ranking by mean |SHAP|; top 40% kept.`],
[`Hyper-parameters and how they are tuned`, `Model settings (300 trees, depth 4, learning rate 0.05) fixed, because the model is only used for ranking; the kept share (30–50%) checked in the inner folds.`],
[`Data on which it works well`, `Tabular data with many correlated features and non-linear relations.`],
[`Why it was selected`, `Consistent and model-agnostic importance; used in this exact role by Ma et al. (2026).`],
[`Key references`, `Lundberg and Lee (2017); Lundberg et al. (2020); Ma et al. (2026)`]], [2300, 7006], `Method card – Shapley additive explanations (SHAP).`, 16));
K.push(H3(`Step 1.2.3 – Competitive adaptive reweighted sampling (CARS) with partial least squares (PLS)`));
K.push(...tab2('s123', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The pre-screened bands are still strongly collinear; a small set of complementary wavelengths is needed.`],
[`Input`, `Pre-screened bands (training part).`],
[`Output → next step`, `Optimal wavelength subset with the lowest cross-validated error → Step 1.2.4.`]], [2200, 7106], `Step 1.2.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Standardise every pre-screened band (mean 0 and standard deviation 1 on the training part). CARS ranks bands by the size of their PLS coefficients, which depend on units: reflectance is about 0–0.6, first-derivative values about 0.001–0.01 nm^{−1}; without standardising, one form would be favoured for numerical, not biological, reasons.`));
K.push(NL(`Choose the number of partial least squares (PLS) components (1–15) by Monte Carlo cross-validation (MCCV: 50 random 80/20 splits of the training plots).`));
K.push(NL(`Run competitive adaptive reweighted sampling (CARS) for 50 iterations: in each iteration, fit PLS on a random 80% of the samples, weight every band by the absolute value of its PLS regression coefficient, remove bands by an exponentially decreasing function and then by adaptive reweighted sampling.`));
K.push(NL(`After every iteration compute the root-mean-square error of cross-validation (RMSECV); the subset with the minimum RMSECV is the optimal subset (${F('dummyshap')}b, c).`));
K.push(P(`**Supporting studies.** CARS: Li et al. (2009); variable selection in PLS: Mehmood et al. (2012); SHAP-CARS with MCCV for the PLS components: Ma et al. (2026).`));
K.push(...fig2('dummyshap', 'g15_dummy_shapcars.png', `Dummy example of SHAP-CARS: (a) Shapley pre-screening; (b) number of wavelengths kept in each CARS iteration; (c) the iteration with the minimum cross-validated error defines the optimal wavelengths.`, 560));
K.push(...tab2('ccars', [[`Aspect`, `Competitive adaptive reweighted sampling (CARS) with partial least squares (PLS)`],
[`Principle (how it works)`, `Imitates "survival of the fittest": bands with large PLS regression coefficients survive, bands with small coefficients are removed step by step; the subset with the lowest cross-validated error is kept. PLS itself projects correlated bands onto a few latent components that best predict the target.`],
[`Problem it solves`, `Selects a small set of non-redundant, informative wavelengths from highly collinear spectra.`],
[`Specification in this study`, `Bands standardised before PLS; 50 iterations; 80% sampling per iteration; PLS components by MCCV (50 splits, maximum 15); CARS repeated 20 times with different random seeds.`],
[`Hyper-parameters and how they are tuned`, `Number of PLS components (by MCCV) and number of iterations (50); because results vary between runs, wavelengths selected in at least 50% of the 20 runs are kept (stability rule).`],
[`Data on which it works well`, `Spectra with many correlated bands and a continuous target.`],
[`Why it was selected`, `Designed for spectra, fast and the best of the three band-selection methods in the DT-EDNet study (Ma et al., 2026); the Shapley pre-screening adds a non-linear view.`],
[`Key references`, `Li et al. (2009); Mehmood et al. (2012); Ma et al. (2026)`]], [2300, 7006], `Method card – Competitive adaptive reweighted sampling (CARS) with partial least squares (PLS).`, 16));
K.push(H3(`Step 1.2.4 – Optimal wavelengths (OW) and their stability`));
K.push(...tab2('s124', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The final wavelength set must be stable and physiologically interpretable.`],
[`Input`, `Optimal subsets of the 20 CARS runs.`],
[`Output → next step`, `Optimal wavelengths (OW, 10–15 bands of reflectance and first derivative) → Activity 1.3, fused inputs of Objective 2 and the network configurations (Step 2.1.5).`]], [2200, 7106], `Step 1.2.4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Count how often each wavelength is selected over the 20 runs; keep those selected in at least 50%.`));
K.push(NL(`If more than 15 remain, keep the 15 most frequent.`));
K.push(NL(`Report every selected wavelength with its label (R_{λ} or FD_{λ}) and the number of each type, so that it is clear which form carries the white rust signal.`));
K.push(NL(`Link each wavelength to a known absorption feature (chlorophyll, red edge, water, structure) for interpretation.`));
K.push(P(`**Supporting studies.** Stability of selection: Meinshausen and Bühlmann (2010), Nogueira et al. (2018); optimal wavelengths for rice blast: Ma et al. (2026).`));
K.push(H2(`Activity 1.3 – Spectral index construction`));
K.push(H3(`Step 1.3.1 – Best normalised difference spectral index (NDSI) and ratio spectral index (RSI)`));
K.push(...tab2('s131', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A single disease-related index is simpler and more transferable than many bands.`],
[`Input`, `NDSI and RSI maps (Step 1.2.1).`],
[`Output → next step`, `Best NDSI and best RSI (highest R² with the severity score) → Activity 1.4 (index group).`]], [2200, 7106], `Step 1.3.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Take the pair with the highest R² from each map.`));
K.push(NL(`Avoid pairs closer than 10 nm (they measure noise rather than a spectral feature).`));
K.push(P(`**Supporting studies.** Ma et al. (2026); Huang et al. (2014).`));
K.push(H3(`Step 1.3.2 – White Rust Index (WRI), a three-band index`));
K.push(...tab2('s132', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Two bands may not capture both the pigment change and the structural change caused by white rust.`],
[`Input`, `Reflectance and the best normalised differences (training part).`],
[`Output → next step`, `White Rust Index (WRI) formula → Activity 1.4 and Objectives 2–3.`]], [2200, 7106], `Step 1.3.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Search WRI = NDSI(λ_{1}, λ_{2}) + w × R(λ_{3}) with w ∈ {−1, −0.5, 0, 0.5, 1}, using bands at 6 nm steps and λ_{1} and λ_{2} at least 50 nm apart.`));
K.push(NL(`Score each candidate by its correlation with the severity score and by the balanced accuracy of healthy vs diseased in grouped inner cross-validation.`));
K.push(NL(`Keep the best formula; repeat the search inside the training part of every fold for prediction.`));
K.push(P(`**Supporting studies.** Disease-specific indices from a normalised difference plus a single band: Mahlein et al. (2013); three-band disease index for yellow rust: Zheng et al. (2018); ground-to-UAV disease index for powdery mildew: Liu et al. (2026).`));
K.push(EQ(`WRI = NDSI(λ_{1}, λ_{2}) + w R_{λ3},      w ∈ {−1, −0.5, 0, 0.5, 1}`));
K.push(...tab2('cwri', [[`Aspect`, `Disease-specific index search (White Rust Index)`],
[`Principle (how it works)`, `Combines the most informative normalised difference with a third band that carries extra information; the weight w sets how much the third band contributes.`],
[`Problem it solves`, `Creates one interpretable index specific to white rust instead of a general vegetation index.`],
[`Specification in this study`, `Bands at 6 nm steps inside the effective ranges; five weights; correlation and balanced accuracy in grouped inner folds.`],
[`Hyper-parameters and how they are tuned`, `The weight w (five values) and the band positions; chosen in the inner folds only.`],
[`Data on which it works well`, `Hyperspectral data from which a cheaper sensor or a satellite band set may later be designed.`],
[`Why it was selected`, `The same form gave disease-specific indices for sugar beet diseases (Mahlein et al., 2013); the three-band idea was also used for yellow rust (Zheng et al., 2018).`],
[`Key references`, `Mahlein et al. (2013); Zheng et al. (2018)`]], [2300, 7006], `Method card – Disease-specific index search (White Rust Index).`, 16));
K.push(H3(`Step 1.3.3 – Two-band indices of the multispectral camera`));
K.push(...tab2('s133', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The multispectral camera has only five bands; its best band combination must be known.`],
[`Input`, `Five multispectral bands.`],
[`Output → next step`, `Ranked ten normalised differences → Step 1.6.1.`]], [2200, 7106], `Step 1.3.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Compute all ten normalised differences of the five bands.`));
K.push(NL(`Rank them by R² with the severity score and compare the best with the White Rust Index.`));
K.push(P(`**Supporting studies.** Ma et al. (2026); multispectral red-edge indices for powdery mildew: Liu et al. (2024).`));
K.push(H2(`Activity 1.4 – Vegetation index selection with ReliefF`));
K.push(H3(`Step 1.4.1 – Index group`));
K.push(...tab2('s141', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Collects all index-type features into one group.`],
[`Input`, `Published indices and red-edge parameters (Step D4); best NDSI, RSI and WRI (Activity 1.3).`],
[`Output → next step`, `Index group of about 55 features → Step 1.4.2.`]], [2200, 7106], `Step 1.4.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Join the published indices, the three red-edge parameters and the constructed indices.`));
K.push(P(`**Supporting studies.** Ma et al. (2026); Mahlein et al. (2013).`));
K.push(H3(`Step 1.4.2 – Within-group redundancy filter`));
K.push(...tab2('s142', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Many indices are nearly identical (for example several NDVI versions), which wastes the selection on duplicates.`],
[`Input`, `Index group (training part).`],
[`Output → next step`, `Thinned index group → Step 1.4.3.`]], [2200, 7106], `Step 1.4.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Remove near-constant indices (standard deviation close to zero).`));
K.push(NL(`Group indices with |r| ≥ 0.95 and keep one per group (the one with the strongest correlation with the severity score).`));
K.push(P(`**Supporting studies.** Correlation clustering before selection: Dormann et al. (2013); high correlation among vegetation indices: Ma et al. (2026).`));
K.push(...tab2('ccorr', [[`Aspect`, `Correlation-cluster redundancy filter`],
[`Principle (how it works)`, `Features whose pairwise |r| is at least 0.95 measure almost the same thing; one representative per cluster keeps the information.`],
[`Problem it solves`, `Removes duplicates before relevance selection, which makes ReliefF and mRMR more stable.`],
[`Specification in this study`, `Pearson |r| ≥ 0.95; representative = the member with the strongest correlation with the severity score.`],
[`Hyper-parameters and how they are tuned`, `Threshold 0.95 (fixed; 0.90 tested as a check).`],
[`Data on which it works well`, `Groups of derived features (indices, texture, thermal statistics).`],
[`Why it was selected`, `Label-free (no leakage), simple and transparent.`],
[`Key references`, `Dormann et al. (2013)`]], [2300, 7006], `Method card – Correlation-cluster redundancy filter.`, 16));
K.push(H3(`Step 1.4.3 – ReliefF ranking of the indices`));
K.push(...tab2('s143', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The indices that best separate overlapping severity classes must be chosen.`],
[`Input`, `Thinned index group, standardised (training part).`],
[`Output → next step`, `Top five to eight indices (number chosen in the inner folds) → Step 1.6.2 and the "VI" group of Step 2.1.5.`]], [2200, 7106], `Step 1.4.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Classes: run ReliefF with k = 10 nearest neighbours on standardised indices; neighbours from the same plot are excluded so that a subplot is not compared with its own plot.`));
K.push(NL(`Severity score: run RReliefF, the regression version, in the same way.`));
K.push(NL(`Rank the indices by their weight and keep the top five (as in Ma et al., 2026); check 3–8 in the inner folds (${F('dummyrelief')}a).`));
K.push(P(`**Supporting studies.** ReliefF and RReliefF: Robnik-Šikonja and Kononenko (2003), Urbanowicz et al. (2018); ReliefF for disease indices: Mahlein et al. (2013), Huang et al. (2014); Relief for vegetation indices in rice blast: Ma et al. (2026).`));
K.push(EQ(`W_{j} ← W_{j} − diff(j, x, H)/m + Σ_{c≠class(x)} [P(c)/(1 − P(class(x)))] diff(j, x, M_{c})/m`));
K.push(P(`For each sampled subplot x, H is its nearest neighbour of the same class (nearest hit) and M_{c} its nearest neighbour of another class c (nearest miss); diff is the absolute difference of feature j. A feature gains weight when it differs between classes and loses weight when it differs within a class. **Worked example (dummy data):** for one sample, index A differs by 0.05 from its hit and by 0.40 from its misses, so its weight rises by about (0.40 − 0.05)/m; index B differs by 0.30 from both and gains nothing.`));
K.push(...fig2('dummyrelief', 'g16_dummy_relief_mrmr.png', `Dummy example: (a) ReliefF weights of the indices (top six kept); (b) cumulative variance of the principal components of the cube (three kept); (c) mRMR ranking of the texture features (top six kept).`, 560));
K.push(...tab2('crelief', [[`Aspect`, `ReliefF (classes) and RReliefF (severity score)`],
[`Principle (how it works)`, `For each sample, compares its feature values with its nearest neighbours of the same class and of other classes; features that separate classes but are stable within classes gain weight. RReliefF does the same with the probability that predictions differ for a continuous target.`],
[`Problem it solves`, `Ranks features by their ability to separate overlapping, ordered severity classes, including effects that appear only together with other features.`],
[`Specification in this study`, `k = 10 neighbours; all training samples used; standardised features; neighbours from the same plot excluded; top five kept.`],
[`Hyper-parameters and how they are tuned`, `k (5, 10, 20) and the number kept (3–8) checked in the inner folds; k = 10 is the usual default.`],
[`Data on which it works well`, `Classification with several overlapping classes and moderate numbers of features (tens to hundreds).`],
[`Why it was selected`, `Handles several classes and interactions, is fast and was used for vegetation indices in the DT-EDNet study and for disease indices in hyperspectral studies.`],
[`Key references`, `Robnik-Šikonja and Kononenko (2003); Urbanowicz et al. (2018); Ma et al. (2026)`]], [2300, 7006], `Method card – ReliefF (classes) and RReliefF (severity score).`, 16));
K.push(H2(`Activity 1.5 – Texture selection and the Tri-band Texture Fusion Index (TTFI)`));
K.push(H3(`Step 1.5.1 – Principal component analysis (PCA) texture of the hyperspectral cube`));
K.push(...tab2('s151', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Texture of 483 bands would give almost 4000 redundant features.`],
[`Input`, `Masked hyperspectral cube (Step D5).`],
[`Output → next step`, `24 texture features (8 measures × 3 principal components, for example PC2-Dis = dissimilarity of component 2) → Step 1.5.2.`]], [2200, 7106], `Step 1.5.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Fit principal component analysis on vegetation pixels of the training data and keep the first three components (cumulative variance above 95%; ${F('dummyrelief')}b).`));
K.push(NL(`Compute the eight GLCM measures on each component image (Step D5) and average them over the vegetation pixels of each subplot.`));
K.push(P(`**Supporting studies.** Texture from principal-component images: Guo et al. (2021), Ma et al. (2026); GLCM: Haralick et al. (1973), Hall-Beyer (2017).`));
K.push(H3(`Step 1.5.2 – Within-group redundancy filter`));
K.push(...tab2('s152', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Some texture measures are almost identical (for example contrast and dissimilarity).`],
[`Input`, `24 texture features (training part).`],
[`Output → next step`, `Thinned texture group → Step 1.5.3.`]], [2200, 7106], `Step 1.5.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Apply the correlation-cluster filter (|r| ≥ 0.95), as in Step 1.4.2.`));
K.push(P(`**Supporting studies.** Dormann et al. (2013); Hall-Beyer (2017) on the strong correlation of contrast and dissimilarity.`));
K.push(H3(`Step 1.5.3 – Minimum redundancy maximum relevance (mRMR) selection of texture`));
K.push(...tab2('s153', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Texture features are correlated with each other; the selected set should be informative and non-redundant.`],
[`Input`, `Thinned texture group (training part).`],
[`Output → next step`, `Top six texture features (TF1–TF6) → Step 1.5.4 and the "TF" group of Step 2.1.5.`]], [2200, 7106], `Step 1.5.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Estimate the relevance of each texture feature as its mutual information with the severity class (or score).`));
K.push(NL(`Select features one at a time: the next feature is the one with the largest relevance minus its mean mutual information with the features already selected (${F('dummyrelief')}c).`));
K.push(NL(`Stop at six features (as in Ma et al., 2026); check 4–8 in the inner folds.`));
K.push(P(`**Supporting studies.** mRMR: Peng et al. (2005); mRMR for texture features of rice blast: Ma et al. (2026); mRMR for UAV and satellite disease features: Yuan et al. (2025).`));
K.push(EQ(`next feature = arg max_{j} [ I(f_{j}; y) − (1/|S|) Σ_{s∈S} I(f_{j}; f_{s}) ]`));
K.push(...tab2('mrmrex', [[`Texture feature (dummy)`, `Relevance I(f; y)`, `Mean redundancy with selected set`, `mRMR score`, `Decision`],
[`PC2-Dis`, `0.62`, `— (first pick)`, `0.62`, `selected 1st`],
[`PC2-Con`, `0.60`, `0.55 (with PC2-Dis)`, `0.05`, `not selected now`],
[`PC3-Mea`, `0.41`, `0.08`, `0.33`, `selected 2nd`],
[`PC2-Hom`, `0.52`, `0.30`, `0.22`, `selected 3rd`]], [2200, 1500, 2300, 1300, 2006], `Worked example (dummy data): the first picks of mRMR. A strongly relevant but redundant feature (PC2-Con) is delayed in favour of a less relevant but new one (PC3-Mea).`, 17));
K.push(...tab2('cmrmr', [[`Aspect`, `Minimum redundancy maximum relevance (mRMR)`],
[`Principle (how it works)`, `Greedy forward selection that balances two quantities measured with mutual information: relevance to the target and redundancy with the features already chosen.`],
[`Problem it solves`, `Selects a compact, complementary set from correlated texture features.`],
[`Specification in this study`, `Mutual information estimated with a k-nearest-neighbour estimator (k = 3) on standardised features; difference criterion (relevance minus redundancy); six features.`],
[`Hyper-parameters and how they are tuned`, `Number of features (4–8) checked in the inner folds; k of the estimator fixed at 3.`],
[`Data on which it works well`, `Groups of correlated features with non-linear relations to the target.`],
[`Why it was selected`, `Removes redundancy and selects relevance in one step; used for texture in the DT-EDNet study and for disease features by Yuan et al. (2025).`],
[`Key references`, `Peng et al. (2005); Ma et al. (2026); Yuan et al. (2025)`]], [2300, 7006], `Method card – Minimum redundancy maximum relevance (mRMR).`, 16));
K.push(H3(`Step 1.5.4 – Construction of the Tri-band Texture Fusion Index (TTFI)`));
K.push(...tab2('s154', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Single texture features describe only one aspect of the lesion pattern; a combination of three can describe roughness, heterogeneity and structure together.`],
[`Input`, `Selected texture features TF1–TF6 (training part).`],
[`Output → next step`, `Best TTFI (strongest correlation with severity) → Step 1.6.2 and the network configurations (Step 2.1.5).`]], [2200, 7106], `Step 1.5.4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Form all ordered triplets (TF1, TF2, TF3) of the six texture features: 6 × 5 × 4 = 120 triplets.`));
K.push(NL(`For every triplet compute the three Tri-band Texture Fusion Indices (equations below), giving 360 candidates.`));
K.push(NL(`Compute the correlation of every candidate with the severity score; keep the best candidate of each formula for description (${F('dummyttfi')}) and the overall best TTFI as the texture index used in modelling.`));
K.push(P(`**Supporting studies.** Tri-band Texture Fusion Index: Ma et al. (2026).`));
K.push(EQ(`TTFI1 = (TF1 + TF2) / TF3;      TTFI2 = TF1 × TF2 / TF3;      TTFI3 = TF1 × (TF1 + TF2) / (TF2 + TF3)`));
K.push(P(`**Worked example (dummy data).** With TF1 = 0.8, TF2 = 1.2 and TF3 = 0.5: TTFI1 = (0.8 + 1.2) / 0.5 = 4.00; TTFI2 = 0.8 × 1.2 / 0.5 = 1.92; TTFI3 = 0.8 × (0.8 + 1.2) / (1.2 + 0.5) = 0.94. Texture values are used on their original (positive) scale; a small constant is added to a denominator that can approach zero.`));
K.push(...fig2('dummyttfi', 'g17_dummy_ttfi.png', `Dummy example: correlation of the best triplet of each TTFI formula with severity, compared with the best single texture feature and the best index.`, 460));
K.push(...tab2('cttfi', [[`Aspect`, `Tri-band Texture Fusion Index (TTFI)`],
[`Principle (how it works)`, `Combines three texture features in sums, products and ratios so that their joint behaviour (for example rising dissimilarity with falling homogeneity) is captured in one number.`],
[`Problem it solves`, `Gives one strong, interpretable texture variable instead of several weak ones.`],
[`Specification in this study`, `Six mRMR-selected features; 120 ordered triplets × 3 formulas; best by |r| with the severity score on the training part.`],
[`Hyper-parameters and how they are tuned`, `No hyper-parameters; the triplet is chosen in the inner folds only.`],
[`Data on which it works well`, `High-resolution texture from canopies with spotty lesions.`],
[`Why it was selected`, `In rice blast, TTFI3 was more strongly related to disease (|r| = 0.75) than any single texture feature and improved all networks when fused with the optimal wavelengths (Ma et al., 2026).`],
[`Key references`, `Ma et al. (2026)`]], [2300, 7006], `Method card – Tri-band Texture Fusion Index (TTFI).`, 16));
K.push(H2(`Activity 1.6 – Disease-specific feature sets of each camera`));
K.push(H3(`Step 1.6.1 – Selection for the multispectral, red–green–blue and thermal cameras`));
K.push(...tab2('s161', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The other cameras must be treated with the same rule so that the cameras can be compared fairly.`],
[`Input`, `Feature groups of the three cameras (training part).`],
[`Output → next step`, `Selected features of each camera → Step 1.6.2.`]], [2200, 7106], `Step 1.6.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Multispectral: keep the five bands (small group); indices and normalised differences: redundancy filter → ReliefF (RReliefF for the score), top five; texture: redundancy filter → mRMR, top four.`));
K.push(NL(`Red–green–blue: colour indices and colour means: redundancy filter → ReliefF, top four; texture: redundancy filter → mRMR, top four.`));
K.push(NL(`Thermal: keep all thermal features after the redundancy filter (group of about 10).`));
K.push(P(`**Supporting studies.** One selection approach per group: Ma et al. (2026); thermal features kept as their own group: Feng et al. (2022), Liu et al. (2024).`));
K.push(H3(`Step 1.6.2 – Variance inflation factor (VIF) across groups`));
K.push(...tab2('s162', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Survivors of different groups can still be correlated (for example a red-edge wavelength and a red-edge index).`],
[`Input`, `Pooled survivors of all groups of one camera (training part).`],
[`Output → next step`, `Disease-specific feature set of the camera (about 10–25 features) → Objective 2 (Step 2.1.2) and discussion.`]], [2200, 7106], `Step 1.6.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Pool the selected features of all groups of the camera.`));
K.push(NL(`Compute the variance inflation factor (VIF) of every feature; remove the feature with the highest VIF and repeat until all VIF values are below 10.`));
K.push(P(`**Supporting studies.** Dormann et al. (2013); variance inflation factor before feature-combination search in disease studies: Tian et al. (2021), Mustafa et al. (2023).`));
K.push(EQ(`VIF_{j} = 1 / (1 − R_{j}^{2})`));
K.push(P(`Here R_{j}^{2} is the coefficient of determination of feature j regressed on all other features. **Worked example:** a feature explained 90% by the others (R_{j}^{2} = 0.90) has VIF = 1 / 0.10 = 10, which is the removal limit.`));
K.push(...tab2('cvif', [[`Aspect`, `Variance inflation factor (VIF)`],
[`Principle (how it works)`, `Measures how much of a feature can be predicted from the other features; a large value means the feature is redundant with the rest.`],
[`Problem it solves`, `Removes multicollinearity across feature groups, which makes models and importance values stable.`],
[`Specification in this study`, `Iterative removal of the feature with the largest VIF until all are below 10.`],
[`Hyper-parameters and how they are tuned`, `Threshold 10 (the usual limit; 5 tested as a check).`],
[`Data on which it works well`, `Pooled sets of correlated predictors.`],
[`Why it was selected`, `Label-free, simple and widely used in disease-feature selection.`],
[`Key references`, `Dormann et al. (2013); Tian et al. (2021)`]], [2300, 7006], `Method card – Variance inflation factor (VIF).`, 16));
K.push(H3(`Step 1.6.3 – Response by treatment and complementarity of cameras`));
K.push(...tab2('s163', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Shows whether the selected features behave the same in all varieties and inoculation timings and whether the cameras carry different information.`],
[`Input`, `Disease-specific feature sets; treatment codes.`],
[`Output → next step`, `Treatment-wise response figures; correlation matrix between the cameras → Objective 2 interpretation.`]], [2200, 7106], `Step 1.6.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Plot the selected features against days after inoculation for each variety and inoculation timing.`));
K.push(NL(`Compute the correlation matrix between the selected features of the four cameras (for example thermal difference vs short-wave-infrared water indices).`));
K.push(NL(`Check that the selected features respond within each growth stage (vegetative, flowering, pod formation), so that they are not only flowering or stage effects.`));
K.push(P(`**Supporting studies.** Sensor complementarity: Mahlein et al. (2019), Maimaitijiang et al. (2020); flowering effects in Brassica: Sulik and Long (2016).`));
K.push(H3(`Step 1.6.4 – Outputs of Objective 1`));
K.push(...tab2('s164', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Summarises what Objective 1 delivers to the other objectives.`],
[`Input`, `Results of Activities 1.1–1.6.`],
[`Output → next step`, `Feature lists and figures → Objectives 2 and 3; Objective 1 chapter of the thesis.`]], [2200, 7106], `Step 1.6.4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Response curves by grade, variety and inoculation timing.`));
K.push(NL(`Optimal wavelengths (OW) with their stability.`));
K.push(NL(`Best NDSI, RSI and the White Rust Index.`));
K.push(NL(`Selected vegetation indices, selected texture features and the best TTFI.`));
K.push(NL(`Disease-specific feature set of each camera and the correlation between cameras.`));
K.push(P(`**Supporting studies.** Ma et al. (2026); Mahlein et al. (2013).`));
K.push(H2(`Activity 1.7 – Biochemical and biophysical basis of the camera responses`));
K.push(P(`Activity 1.7 uses the parameters of Step A8 to show what white rust does to the plant and to explain the camera responses. The parameters are not inputs to any model; they are measured on one designated subplot per plot, which is the experimental unit of the field design (Hurlbert, 1984). Statistics are kept to what each question needs (${F('obj1phys')}).`));
K.push(...fig2('obj1phys', 'g29_physio.png', `Flow chart of Activity 1.7 (Steps 1.7.1–1.7.6).`, 540));
K.push(H3(`Step 1.7.1 – Data preparation`));
K.push(...tab2('s171', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Laboratory and field readings must be on one scale and joined to the image data before analysis.`],
[`Input`, `Parameter table (Step A8); severity grades; covariates; UAV features of the designated subplots.`],
[`Output → next step`, `One analysis table: plot-date rows with the 11 parameters, plot disease index of the plot and of the designated subplot and camera features, growth stage, variety and inoculation timing → Steps 1.7.2–1.7.6.`]], [2200, 7106], `Step 1.7.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Average technical replicates (duplicate absorbance or conductivity readings).`));
K.push(NL(`Express pigments, anthocyanin and protein per gram of fresh weight; keep the units of ${T('physio')}.`));
K.push(NL(`Join by date, plot and designated subplot.`));
K.push(P(`**Supporting studies.** Gomez and Gomez (1984).`));
K.push(H3(`Step 1.7.2 – Effect of white rust on the parameters`));
K.push(...tab2('s172', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Shows whether, and how much, infection changes each parameter on each date.`],
[`Input`, `Analysis table; the 12 treatments (variety × inoculation timing).`],
[`Output → next step`, `Mean difference (inoculated − healthy) with 95% confidence interval for each parameter and date → interpretation; 18 January → Step 3.1.2.`]], [2200, 7106], `Step 1.7.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`For each treatment and date, pair the mean of its three inoculated plots with its healthy plot (12 pairs per date).`));
K.push(NL(`Test the paired differences with a paired t-test, or the Wilcoxon signed-rank test when the differences are clearly not normal.`));
K.push(NL(`Report the mean difference, its 95% confidence interval and the effect size (mean difference divided by the standard deviation of the differences).`));
K.push(P(`**Supporting studies.** Paired designs and tests: Gomez and Gomez (1984), Wilcoxon (1945); effect sizes instead of p-values alone: Sullivan and Feinn (2012).`));
K.push(P(`Pairing compares plots of the same variety and sowing date on the same day, which removes crop-age, date and weather effects. The healthy plots lie in a separate, fungicide-protected block, so the differences can also contain small block and fungicide effects; this is stated with the results.`));
K.push(H3(`Step 1.7.3 – Effect of variety and inoculation timing`));
K.push(...tab2('s173', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Shows whether varieties or crop ages at inoculation differ in their physiological response, as expected from a factorial field experiment.`],
[`Input`, `Inoculated plots (36 per date).`],
[`Output → next step`, `Two-way analysis of variance tables and treatment means → interpretation of variety and timing effects.`]], [2200, 7106], `Step 1.7.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`For each parameter and date, fit a two-way analysis of variance for a randomised block design: replication + variety + inoculation timing + variety × inoculation timing.`));
K.push(NL(`Compare means with the least significant difference at 5% when the F-test is significant.`));
K.push(P(`**Supporting studies.** Analysis of factorial experiments in randomised block designs: Gomez and Gomez (1984).`));
K.push(H3(`Step 1.7.4 – Comparison of growth stages`));
K.push(...tab2('s174', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `White rust may affect the plant more at one growth stage than at another; stage also changes the parameters in healthy plants.`],
[`Input`, `Analysis table with the BBCH growth stage of every plot and date.`],
[`Output → next step`, `Parameter means by stage (healthy plots), disease effect by stage, and a test of whether the disease effect differs between stages → interpretation of stage-dependent camera responses.`]], [2200, 7106], `Step 1.7.4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Healthy reference: mean ± standard error of each parameter for the vegetative, flowering and pod-formation stages, healthy plots only.`));
K.push(NL(`Disease effect by stage: the paired differences of Step 1.7.2 grouped by stage, each with its mean and 95% confidence interval.`));
K.push(NL(`Difference between stages: one-way analysis of variance on the paired differences with stage as the factor (Kruskal–Wallis test if the differences are not normal), followed by Tukey comparisons; a linear mixed model with plot as a random effect is the stricter alternative for the repeated dates.`));
K.push(NL(`Report the number of plots in every stage × date cell.`));
K.push(P(`**Supporting studies.** Kruskal and Wallis (1952); Tukey (1949); mixed models for repeated measurements: Bates et al. (2015); growth-stage dependence of disease signals: Blasch et al. (2023); flowering and Brassica canopy spectra: Sulik and Long (2016).`));
K.push(...tab2('stageex', [[`Growth stage (dummy)`, `Healthy`, `Inoculated`, `Difference (95% confidence interval)`],
[`Vegetative`, `2.10`, `1.95`, `−0.15 (−0.30 to 0.00)`],
[`Flowering`, `1.85`, `1.45`, `−0.40 (−0.58 to −0.22)`],
[`Pod formation`, `1.30`, `1.05`, `−0.25 (−0.42 to −0.08)`]], [2200, 1800, 1800, 3506], `Worked example (dummy data): total chlorophyll (mg g⁻¹ fresh weight) by growth stage; the disease effect is largest at flowering.`, 17));
K.push(H3(`Step 1.7.5 – Relation of the parameters with disease severity`));
K.push(...tab2('s175', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Shows which parameters change in proportion to severity, not only between healthy and diseased plants.`],
[`Input`, `Inoculated plots; plot percent disease index; designated-subplot canopy score.`],
[`Output → next step`, `Correlation coefficients with 95% confidence intervals for each parameter and post-symptomatic date → interpretation.`]], [2200, 7106], `Step 1.7.5 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Compute the Pearson correlation of each parameter with the plot disease index and with the disease index of the designated subplot, separately for each post-symptomatic date (36 plots per date).`));
K.push(NL(`Do not pool dates directly: if a pooled value is wanted, remove the date means first (within-date correlation), because parameters and severity both change with time.`));
K.push(P(`**Supporting studies.** Correlation with repeated observations: Bland and Altman (1995), Bakdash and Marusich (2017).`));
K.push(H3(`Step 1.7.6 – Relation of the parameters with the camera features`));
K.push(...tab2('s176', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Links each camera feature to a plant process, which shows why the feature responds to white rust.`],
[`Input`, `Parameters and the camera features of the designated subplots (selected features of Activities 1.2–1.6 and the indices of ${T('traitlinks')}).`],
[`Output → next step`, `Parameter × feature correlation heat maps for each date and growth stage; check of the expected links → interpretation of Objectives 1 and 2.`]], [2200, 7106], `Step 1.7.6 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Compute Pearson correlations between each parameter and each selected camera feature within each date (48 designated subplots), and within each growth stage.`));
K.push(NL(`Control false discoveries over the many pairs with the Benjamini–Hochberg procedure (5%).`));
K.push(NL(`Compare the strongest links with the expected links of ${T('traitlinks')}.`));
K.push(P(`**Supporting studies.** Benjamini and Hochberg (1995); physiological traits explaining spectral and thermal disease signals: Calderón et al. (2013), Zarco-Tejada et al. (2018), Poblete et al. (2023).`));
K.push(...tab2('traitlinks', [[`Parameter`, `Expected camera features`, `Why`, `References`],
[`Chlorophyll a, b`, `red-edge position, CIrededge, MTCI, NDRE, PSSR, White Rust Index`, `chlorophyll absorbs red light and sets the position of the red edge`, `Gitelson et al. (2003); Filella and Peñuelas (1994)`],
[`Carotenoids`, `PRI, PSRI`, `carotenoid/chlorophyll ratio changes with stress and senescence`, `Gamon et al. (1992); Merzlyak et al. (1999)`],
[`Anthocyanin`, `anthocyanin reflectance index (ARI)`, `anthocyanin absorbs green light near 550 nm`, `Gitelson et al. (2001)`],
[`Relative water content`, `NDWI, NDII, water index, moisture stress index; canopy minus air temperature`, `water absorbs near 970, 1200, 1450 and 1650 nm; water loss warms the canopy`, `Gao (1996); Peñuelas et al. (1997); Jones et al. (2009)`],
[`Stomatal conductance, transpiration`, `canopy minus air temperature, normalised relative canopy temperature, crop water stress index`, `transpiration cools the leaves`, `Jones et al. (2009); Calderón et al. (2013)`],
[`Net photosynthesis`, `PRI, chlorophyll indices`, `PRI follows xanthophyll changes linked to light use`, `Gamon et al. (1992)`],
[`Membrane stability index`, `near-infrared plateau, texture features`, `tissue damage around pustules changes leaf structure and canopy pattern`, `Mahlein (2016)`],
[`Protein`, `red-edge features`, `leaf protein follows leaf nitrogen and chlorophyll`, `Filella and Peñuelas (1994)`],
[`Leaf area index`, `NDVI, OSAVI, MSR, texture features`, `canopy size controls near-infrared scattering and canopy cover`, `Haboudane et al. (2004)`]], [1900, 2900, 2700, 1806], `Expected links between the parameters and the camera features, checked in Step 1.7.6.`, 15));
K.push(...fig2('physdummy', 'g30_dummy_physio.png', `Dummy example: (a) chlorophyll of healthy and inoculated plots by growth stage; (b) correlation heat map between parameters and camera features on one date.`, 560));
K.push(...tab2('cphysstats', [[`Aspect`, `Statistical analysis of the biochemical and biophysical parameters`],
[`Principle (how it works)`, `Paired comparisons isolate the disease effect within the same variety, sowing date and day; analysis of variance tests treatment factors in the randomised block design; within-date correlations measure the strength of relations without the time trend.`],
[`Problem it solves`, `Answers whether white rust changes a parameter, at which growth stage most, and which camera features follow which parameter, without pseudo-replication.`],
[`Specification in this study`, `Paired t-test or Wilcoxon signed-rank test (12 pairs per date); two-way analysis of variance (36 inoculated plots per date); one-way analysis of variance or Kruskal–Wallis test on paired differences by stage; Pearson correlation within dates; Benjamini–Hochberg control of false discoveries.`],
[`Hyper-parameters and how they are tuned`, `Significance level 5%; false discovery rate 5%; effect sizes and 95% confidence intervals reported with every test.`],
[`Data on which it works well`, `Plot-level measurements from designed field experiments with few replications.`],
[`Why it was selected`, `Simple, standard in agricultural research and matched to the design; the plot is treated as the experimental unit.`],
[`Key references`, `Gomez and Gomez (1984); Hurlbert (1984); Benjamini and Hochberg (1995); Sullivan and Feinn (2012)`]], [2300, 7006], `Method card – Statistical analysis of the biochemical and biophysical parameters.`, 16));
K.push(H2(`Activity 1.8 – Characterisation of the pre-symptomatic stage`));
K.push(P(`Activities 1.1–1.7 describe white rust after symptoms appear. Activity 1.8 repeats the characterisation before symptoms, with the 576 pre-symptomatic subplot samples of each camera (3 flights × 192 subplots). No grade exists yet, so the target is later-infected vs healthy: the label of an inoculated subplot is taken from its later status (Step A5). The result is the pre-symptomatic feature set of each camera and a list of the earliest-responding wavelengths, indices, texture and thermal features, which feed the prediction models of Objective 3 (${F('presym')}).`));
K.push(...fig2('presym', 'g31_presym.png', `Activity 1.8 – characterisation of the pre-symptomatic stage (Steps 1.8.1–1.8.5).`, 540));
K.push(...tab2('presymn', [[`Flight`, `Days after inoculation`, `Healthy subplots`, `Inoculated subplots`, `Total`],
[`1 Jan 2027`, `2`, `48`, `144`, `192`],
[`4 Jan 2027`, `5`, `48`, `144`, `192`],
[`7 Jan 2027`, `8`, `48`, `144`, `192`],
[`All`, ``, `144`, `432 (later-infected subplots only are used)`, `576`]], [1800, 1800, 1600, 2600, 1506], `Pre-symptomatic samples per camera.`, 16));
K.push(H3(`Step 1.8.1 – Pre-symptomatic response curves`));
K.push(...tab2('s181', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Shows whether and where the spectrum, temperature and texture of later-infected subplots already differ from healthy subplots.`],
[`Input`, `Pre-symptomatic features of all cameras; later-status labels.`],
[`Output → next step`, `Mean curves and percentage differences by date → Steps 1.8.2–1.8.5.`]], [2200, 7106], `Step 1.8.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Mean reflectance, first derivative, indices, texture and thermal features of later-infected and healthy subplots on each pre-symptomatic date (± 1 standard deviation).`));
K.push(NL(`Percentage difference from healthy: Δ% = (x_{infected} − x_{healthy}) / x_{healthy} × 100, per feature and date.`));
K.push(NL(`Separate curves for each variety and inoculation timing.`));
K.push(P(`**Supporting studies.** Pre-symptomatic spectral and thermal changes: Zarco-Tejada et al. (2018), Calderón et al. (2013), Zhu et al. (2017); early changes in rusts and mildews: Terentev et al. (2023).`));
K.push(H3(`Step 1.8.2 – Univariate tests with plot means and effect sizes`));
K.push(...tab2('s182', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Gives a simple statistical answer to which features differ before symptoms, without pseudo-replication.`],
[`Input`, `Plot means of every feature (unit = plot) on each pre-symptomatic date.`],
[`Output → next step`, `Effect size and adjusted p-value of every feature and date → interpretation; Step 1.8.4.`]], [2200, 7106], `Step 1.8.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Average the subplots of each plot so that the plot is the experimental unit (Hurlbert, 1984).`));
K.push(NL(`Welch t-test (or Mann–Whitney U test for skewed features) between later-infected inoculated plots and healthy plots for every feature and date.`));
K.push(NL(`Report the effect size (Hedges g) with its 95% confidence interval and control false discoveries with the Benjamini–Hochberg procedure (5%).`));
K.push(P(`**Supporting studies.** Hurlbert (1984); Sullivan and Feinn (2012); Benjamini and Hochberg (1995).`));
K.push(H3(`Step 1.8.3 – Pre-symptomatic effective ranges and optimal wavelengths`));
K.push(...tab2('s183', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The wavelengths that respond earliest may differ from those that respond after symptoms.`],
[`Input`, `Reflectance and first derivative; binary later-status label (training part).`],
[`Output → next step`, `Pre-symptomatic effective ranges and optimal wavelengths → Step 1.8.4 and Objective 3.`]], [2200, 7106], `Step 1.8.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`NDSI and RSI maps with the binary label (area under the curve or point-biserial r^{2} of each band pair).`));
K.push(NL(`SHAP-CARS with partial least squares discriminant analysis on the binary label (Activity 1.2 settings).`));
K.push(NL(`Run inside the training part of every fold when used for prediction.`));
K.push(P(`**Supporting studies.** Ma et al. (2026); Li et al. (2009); Lundberg and Lee (2017); Zhu et al. (2017).`));
K.push(H3(`Step 1.8.4 – Indices, texture and thermal features before symptoms`));
K.push(...tab2('s184', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Small early changes are easier to see after removing date, weather and variety effects.`],
[`Input`, `48 published indices, red-edge parameters, texture and thermal features; healthy plots of the same date and variety.`],
[`Output → next step`, `Pre-symptomatic feature set of each camera (variance inflation factor below 10) → Objective 3 (Activity 3.3).`]], [2200, 7106], `Step 1.8.4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Healthy-plot normalisation (Step E2) of every feature.`));
K.push(NL(`Indices: ReliefF with the two classes; texture: mRMR; thermal: canopy minus air temperature, normalised relative canopy temperature, crop water stress index and difference from healthy plots.`));
K.push(NL(`Pool the survivors and keep features with a variance inflation factor below 10.`));
K.push(P(`**Supporting studies.** Oerke et al. (2006); Calderón et al. (2014); Robnik-Šikonja and Kononenko (2003); Peng et al. (2005); Dormann et al. (2013).`));
K.push(H3(`Step 1.8.5 – Earliest-responding features`));
K.push(...tab2('s185', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Shows how early and with which feature type white rust can be seen.`],
[`Input`, `Effect sizes and selected features of the three pre-symptomatic dates.`],
[`Output → next step`, `Earliest date on which each feature differs from healthy, by variety and timing; physiological explanation with Step 3.1.2.`]], [2200, 7106], `Step 1.8.5 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`For every selected feature, find the first date (2, 5 or 8 days after inoculation) on which the effect size is significant and larger than 0.8.`));
K.push(NL(`Compare the earliest features with the pre-symptomatic biochemical and biophysical parameters of 7 January (Step 3.1.2).`));
K.push(P(`**Supporting studies.** Mahlein et al. (2019); Zarco-Tejada et al. (2018); Sullivan and Feinn (2012).`));
K.push(BOX(`Link to satellite monitoring (optional extension, not part of the six-month plan).`, `The subplot hyperspectral spectra can be convolved with the relative spectral response functions of Sentinel-2 and Resourcesat LISS-IV to simulate satellite band reflectance, and the selected wavelengths and indices can then be tested with these simulated bands. This approach was used for yellow rust with Sentinel-2 (Zheng et al., 2018) and for rice bacterial leaf blight with LISS-IV (Das et al., 2015); UAV data have also been used to bridge field and satellite scales (Revill et al., 2020; Blasch et al., 2023; Poblete et al., 2023; Yuan et al., 2025).`, 'EEF3E8', '2C5F2D'));
K.push(H1(`4. Objective 2 – Detection and severity discrimination through AI-based multimodal data fusion`));
K.push(P(`Objective 2 builds and compares predictive models on the 1920 post-symptomatic samples of each camera. For every single camera and for every combination of cameras (15 sensor sets), classification models (Task A, healthy vs diseased; Task B, severity classes) and regression models (Task C, severity score) are developed with all model families, so that the performance of every camera and every combination can be compared on the same folds (${T('modelmatrix')}). In combinations, thermal, multispectral and red–green–blue features are added to the hyperspectral features by feature-level fusion for all models, including DT-EDNet and the comparison networks. A second comparison repeats the design of Ma et al. (2026) on the hyperspectral feature groups, with plot-grouped validation.`));
K.push(...fig2('obj2', 'g06_obj2.png', `Flow chart of Objective 2 (Activities 2.1–2.6).`, 540));
K.push(...tab2('o2act', [[`Activity`, `Steps`, `Main output`],
[`2.1 Tasks and inputs`, `2.1.1–2.1.5`, `task labels; fused feature sets of 15 sensor sets; hyperspectral feature-group configurations`],
[`2.2 Machine-learning models`, `2.2.1–2.2.6`, `tuned support vector machine, random forest, extreme gradient boosting, k-nearest neighbours and partial least squares models`],
[`2.3 Deep-learning models`, `2.3.1–2.3.8`, `feature-fusion networks and pseudo-image networks (DT-EDNet, EfficientNet, ResNet18, ConvNeXt V2)`],
[`2.4 Evaluation`, `2.4.1–2.4.3`, `metric tables`],
[`2.5 Comparison, ablation and interpretation`, `2.5.1–2.5.5`, `best sensor set and model; contribution of each camera; module ablation; Shapley explanation; gain over the covariate baseline`],
[`2.6 Robustness and maps`, `2.6.1–2.6.3`, `results by treatment; transfer tests; severity maps`],
[`2.7 Independent testing at Bharatpur`, `2.7.1–2.7.4`, `accuracy of frozen models on independent research-farm and farmers' field data; farm maps`]], [2900, 1300, 5106], `Activities of Objective 2.`, 17));
K.push(H2(`Activity 2.1 – Tasks and inputs`));
K.push(H3(`Step 2.1.1 – Three tasks and class balance`));
K.push(...tab2('s211', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Defines the three prediction problems and handles unequal class sizes.`],
[`Input`, `Post-symptomatic dataset with labels (Step A5).`],
[`Output → next step`, `Three labelled task datasets → all models.`]], [2200, 7106], `Step 2.1.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Task A, detection: healthy (DI = 0) vs diseased (DI above 0).`));
K.push(NL(`Task B, severity classes: DI classes 0, 1, 3, 5, 7, 9 (merged if a class has fewer than 5% of samples).`));
K.push(NL(`Task C, regression: disease index DI (%).`));
K.push(NL(`Class weights (Step E4) for all classifiers; macro-averaged metrics.`));
K.push(P(`**Supporting studies.** Detection, severity classes and regression together: Tian et al. (2021), Feng et al. (2022), Abdulridha et al. (2023); three-class healthy, mild and severe classification: Yuan et al. (2025).`));
K.push(H3(`Step 2.1.2 – Fold-wise feature selection for each camera`));
K.push(...tab2('s212', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Features must be selected without the test replication.`],
[`Input`, `Feature groups of each camera; outer and inner folds (Activity F).`],
[`Output → next step`, `Disease-specific feature set of each camera for every fold and task → Step 2.1.3.`]], [2200, 7106], `Step 2.1.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`For every outer fold and task, repeat Activities 1.2–1.6 on the training part (label-based steps inside the inner folds).`));
K.push(NL(`Store the selected features of every fold (they are used for the stability analysis in Step 2.5.4).`));
K.push(P(`**Supporting studies.** Nested selection: Ambroise and McLachlan (2002), Varma and Simon (2006).`));
K.push(H3(`Step 2.1.3 – Feature-level fusion for the 15 sensor sets`));
K.push(...tab2('s213', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Combinations of cameras need one input vector per sample.`],
[`Input`, `Disease-specific feature sets of the cameras.`],
[`Output → next step`, `Fused feature set of each sensor set, fold and task → all models.`]], [2200, 7106], `Step 2.1.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Single camera (S1–S4): its disease-specific feature set is the input.`));
K.push(NL(`Combination (S5–S15): concatenate the feature sets of its cameras (thermal, multispectral and red–green–blue features added to the hyperspectral features) and apply the variance inflation factor rule (below 10) again across cameras.`));
K.push(NL(`Standardise with training statistics (Step E3).`));
K.push(NL(`The same fused set is the input of every model: machine learning, DNN-F1, DNN-F2 and the pseudo-image networks.`));
K.push(P(`**Supporting studies.** Feature-level fusion of spectral, thermal and texture features: Feng et al. (2022), Liu et al. (2024); fusion levels: Ghamisi et al. (2019); input- and intermediate-level fusion: Maimaitijiang et al. (2020).`));
K.push(...fig2('combinations', 'g10_combinations.png', `The 15 sensor sets: 4 single cameras, 6 pairs, 4 triples and all four.`, 520));
K.push(...tab2('sets', [[`Set`, `Cameras`, `Question it answers`],
[`S1`, `hyperspectral`, `reference: what the most detailed camera achieves`],
[`S2`, `multispectral`, `what a low-cost, satellite-like camera achieves`],
[`S3`, `red–green–blue`, `what a consumer camera achieves`],
[`S4`, `thermal`, `what canopy temperature alone achieves`],
[`S5`, `hyperspectral + multispectral`, `whether the multispectral camera adds anything`],
[`S6`, `hyperspectral + red–green–blue`, `whether fine colour texture adds to spectra`],
[`S7`, `hyperspectral + thermal`, `whether temperature adds to spectra`],
[`S8`, `multispectral + red–green–blue`, `low-cost optical pair`],
[`S9`, `multispectral + thermal`, `low-cost spectral + thermal pair`],
[`S10`, `red–green–blue + thermal`, `cheapest pair`],
[`S11`, `hyperspectral + multispectral + red–green–blue`, `all optical cameras (is thermal needed?)`],
[`S12`, `hyperspectral + multispectral + thermal`, `is red–green–blue needed?`],
[`S13`, `hyperspectral + red–green–blue + thermal`, `is multispectral needed when hyperspectral is present?`],
[`S14`, `multispectral + red–green–blue + thermal`, `all low-cost cameras`],
[`S15`, `all four`, `full system; basis of the drop-one-camera ablation`]], [900, 3600, 4806], `The 15 sensor sets.`, 17));
K.push(...tab2('modelmatrix', [[`Model family`, `Models`, `Sensor sets`, `Classification (Tasks A, B)`, `Regression (Task C)`],
[`Machine learning`, `support vector machine / regression, random forest, extreme gradient boosting, k-nearest neighbours, partial least squares (discriminant analysis / regression)`, `all 15`, `yes`, `yes`],
[`Feature-fusion networks`, `DNN-F1`, `all 15`, `yes`, `yes`],
[``, `DNN-F2 (one branch per camera)`, `the 11 combinations (S5–S15)`, `yes`, `yes`],
[`Pseudo-image networks`, `DT-EDNet, EfficientNet-B0, ResNet18, ConvNeXt V2-Atto`, `all 15 (fused features of all cameras in the set)`, `yes`, `yes (linear output)`],
[`Covariate models (Step 2.5.5)`, `best machine-learning model`, `covariates only; best sensor sets + covariates`, `yes`, `yes`]], [1800, 3200, 1800, 1300, 1206], `Every model is built for every sensor set and task on the same folds, so that single cameras and combinations can be compared directly.`, 17));
K.push(H3(`Step 2.1.4 – Final compact set by sequential floating forward selection (SFFS) for the machine-learning models`));
K.push(...tab2('s214', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Different models use features differently, and a small final set improves generalisation and interpretation.`],
[`Input`, `Fused feature set (training part).`],
[`Output → next step`, `Optimum feature combination of each machine-learning model (at most 15 features) → Activity 2.2.`]], [2200, 7106], `Step 2.1.4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Run sequential floating forward selection (SFFS) wrapped around each machine-learning model, with macro-F1 (classes) or root-mean-square error (score) in the inner folds as criterion.`));
K.push(NL(`Limit the set to 15 features and keep the smallest subset within 1% of the best score.`));
K.push(NL(`The neural networks use the whole fused set, because they learn their own feature weights.`));
K.push(P(`**Supporting studies.** Floating search: Pudil et al. (1994); wrapper selection for disease models: Tian et al. (2021), Mustafa et al. (2023); backward wrapper selection for Fusarium head blight: Liu et al. (2020).`));
K.push(...tab2('sffsex', [[`Iteration (dummy)`, `Action`, `Subset`, `Inner macro-F1`],
[`1`, `add best single feature`, `WRI`, `0.52`],
[`2`, `add`, `WRI, OW 718 nm`, `0.60`],
[`3`, `add`, `WRI, OW 718 nm, ΔT`, `0.65`],
[`4`, `add`, `WRI, OW 718 nm, ΔT, TTFI`, `0.68`],
[`5`, `conditional removal: dropping OW 718 nm improves`, `WRI, ΔT, TTFI`, `0.69`],
[`…`, `continue until 15 features or no gain`, `…`, `…`]], [1600, 3600, 2500, 1606], `Worked example (dummy data): sequential floating forward selection adds features and removes a feature when it becomes redundant.`, 17));
K.push(...tab2('csffs', [[`Aspect`, `Sequential floating forward selection (SFFS)`],
[`Principle (how it works)`, `Adds the feature that most improves the model; after every addition it tries to remove previously added features and removes one if the model improves ("floating").`],
[`Problem it solves`, `Finds a small feature set suited to each model and corrects early choices that later become redundant.`],
[`Specification in this study`, `Wrapped around each machine-learning model; criterion macro-F1 or root-mean-square error in the inner folds; at most 15 features; smallest subset within 1% of the best.`],
[`Hyper-parameters and how they are tuned`, `Maximum subset size (15) and tolerance (1%); fixed to keep at least about 85 training samples per feature.`],
[`Data on which it works well`, `Moderate candidate sets (20–40 features) after the earlier stages; not for hundreds of features.`],
[`Why it was selected`, `Gives the model-specific final set recommended in the staged approach while keeping the number of candidates small.`],
[`Key references`, `Pudil et al. (1994); Tian et al. (2021)`]], [2300, 7006], `Method card – Sequential floating forward selection (SFFS).`, 16));
K.push(H3(`Step 2.1.5 – Hyperspectral feature-group configurations for the network comparison`));
K.push(...tab2('s215', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The DT-EDNet study compared networks on separate feature groups and on their combinations; the same design shows which hyperspectral feature types help each network.`],
[`Input`, `Fold-wise optimal wavelengths, selected indices, selected texture features and best TTFI of the hyperspectral camera.`],
[`Output → next step`, `Six input configurations → pseudo-image networks (Activity 2.3) and the best machine-learning model as reference.`]], [2200, 7106], `Step 2.1.5 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`OW: optimal wavelengths only.`));
K.push(NL(`VI: selected vegetation indices only.`));
K.push(NL(`TF: selected texture features only.`));
K.push(NL(`OW + VI.`));
K.push(NL(`OW + TTFI.`));
K.push(NL(`OW + VI + TTFI (the best combination in Ma et al., 2026).`));
K.push(P(`**Supporting studies.** Feature-group configurations: Ma et al. (2026); vegetation index and texture fusion for yellow rust: Guo et al. (2021).`));
K.push(H2(`Activity 2.2 – Machine-learning models`));
K.push(P(`Five machine-learning model families are used for classification and their regression versions for the severity score. They cover kernel, tree-ensemble, boosting, instance-based and latent-variable approaches, so that conclusions do not depend on one type of model.`));
K.push(H3(`Step 2.2.1 – Support vector machine (SVM) and support vector regression (SVR)`));
K.push(...tab2('s221', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A robust classifier and regressor for a few hundred to a few thousand samples with correlated features.`],
[`Input`, `Optimum feature combination (standardised).`],
[`Output → next step`, `Predictions on the test replication → Activity 2.4.`]], [2200, 7106], `Step 2.2.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Radial basis function kernel; class weights for classes; one-vs-one for several classes.`));
K.push(NL(`Tune C, γ (and ε for regression) by grid search in the inner folds (${T('mlgrid')}).`));
K.push(P(`**Supporting studies.** Cortes and Vapnik (1995); Mountrakis et al. (2011); disease applications: Tian et al. (2021), Mustafa et al. (2023), Yuan et al. (2025).`));
K.push(...tab2('csvm', [[`Aspect`, `Support vector machine (SVM) and support vector regression (SVR)`],
[`Principle (how it works)`, `Finds the boundary with the largest margin between classes (or a tube of width ε around the regression line); the kernel maps the data so that curved boundaries become possible.`],
[`Problem it solves`, `Non-linear classification and regression with limited samples.`],
[`Specification in this study`, `Radial basis function kernel; class weights; standardised inputs.`],
[`Hyper-parameters and how they are tuned`, `C ∈ {0.1, 1, 10, 100}; γ ∈ {0.001, 0.01, 0.1, scale}; ε ∈ {0.1, 0.5} for regression; grid search in the inner folds.`],
[`Data on which it works well`, `Small to medium samples (hundreds to thousands), moderate numbers of standardised features.`],
[`Why it was selected`, `Among the most accurate classifiers in remote sensing for limited training data.`],
[`Key references`, `Cortes and Vapnik (1995); Mountrakis et al. (2011)`]], [2300, 7006], `Method card – Support vector machine (SVM) and support vector regression (SVR).`, 16));
K.push(H3(`Step 2.2.2 – Random forest (RF)`));
K.push(...tab2('s222', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A robust, little-tuned model that handles non-linear effects and gives feature importance.`],
[`Input`, `Optimum feature combination.`],
[`Output → next step`, `Predictions → Activity 2.4.`]], [2200, 7106], `Step 2.2.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`500 trees; class weights; tune the number of features per split and the minimum leaf size.`));
K.push(P(`**Supporting studies.** Breiman (2001); Belgiu and Drăguţ (2016); disease applications: Abdulridha et al. (2023), Liu et al. (2024), Yu et al. (2021), Yuan et al. (2025).`));
K.push(...tab2('crf', [[`Aspect`, `Random forest (RF)`],
[`Principle (how it works)`, `Averages many decision trees, each grown on a bootstrap sample and choosing among a random subset of features at every split.`],
[`Problem it solves`, `Non-linear classification and regression that resists overfitting and noise.`],
[`Specification in this study`, `500 trees; class weights; out-of-bag error monitored.`],
[`Hyper-parameters and how they are tuned`, `Features per split ∈ {√p, 0.3p}; minimum leaf size ∈ {1, 3, 5}; grid search in the inner folds.`],
[`Data on which it works well`, `Tabular data with mixed, noisy features; small and large samples.`],
[`Why it was selected`, `Little tuning, stable, widely used in UAV disease studies.`],
[`Key references`, `Breiman (2001); Belgiu and Drăguţ (2016)`]], [2300, 7006], `Method card – Random forest (RF).`, 16));
K.push(H3(`Step 2.2.3 – Extreme gradient boosting (XGBoost)`));
K.push(...tab2('s223', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Often the most accurate tree model on tabular features.`],
[`Input`, `Optimum feature combination.`],
[`Output → next step`, `Predictions → Activity 2.4.`]], [2200, 7106], `Step 2.2.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Tune the number of trees, depth and learning rate; subsample 0.8; sample weights from the class weights.`));
K.push(P(`**Supporting studies.** Chen and Guestrin (2016).`));
K.push(...tab2('cxgb', [[`Aspect`, `Extreme gradient boosting (XGBoost)`],
[`Principle (how it works)`, `Adds small trees one after another; each new tree corrects the errors of the previous ones, with regularisation of tree complexity.`],
[`Problem it solves`, `High-accuracy non-linear modelling of tabular features.`],
[`Specification in this study`, `Subsample 0.8; column subsample 0.8; early stopping on the inner validation plots.`],
[`Hyper-parameters and how they are tuned`, `Trees ∈ {200, 500}; depth ∈ {3, 5}; learning rate ∈ {0.05, 0.1}; grid search in the inner folds.`],
[`Data on which it works well`, `Tabular data with non-linear interactions; medium samples.`],
[`Why it was selected`, `Strong benchmark model; complements random forest (boosting vs averaging).`],
[`Key references`, `Chen and Guestrin (2016)`]], [2300, 7006], `Method card – Extreme gradient boosting (XGBoost).`, 16));
K.push(H3(`Step 2.2.4 – k-nearest neighbours (k-NN)`));
K.push(...tab2('s224', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A simple reference model that predicts from the most similar training samples.`],
[`Input`, `Optimum feature combination (standardised).`],
[`Output → next step`, `Predictions → Activity 2.4.`]], [2200, 7106], `Step 2.2.4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Tune k and the weighting (uniform or by distance).`));
K.push(P(`**Supporting studies.** Cover and Hart (1967); Yuan et al. (2025).`));
K.push(...tab2('cknn', [[`Aspect`, `k-nearest neighbours (k-NN)`],
[`Principle (how it works)`, `Predicts the class (majority vote) or score (mean) of the k most similar training samples in feature space.`],
[`Problem it solves`, `Simple non-parametric reference model.`],
[`Specification in this study`, `Euclidean distance on standardised features.`],
[`Hyper-parameters and how they are tuned`, `k ∈ {3, 5, 7, 9, 11}; uniform or distance weights; grid search in the inner folds.`],
[`Data on which it works well`, `Compact, standardised feature sets; low-dimensional data.`],
[`Why it was selected`, `Transparent baseline; shows whether more complex models are needed.`],
[`Key references`, `Cover and Hart (1967)`]], [2300, 7006], `Method card – k-nearest neighbours (k-NN).`, 16));
K.push(H3(`Step 2.2.5 – Partial least squares discriminant analysis (PLS-DA) and regression (PLSR)`));
K.push(...tab2('s225', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The standard chemometric model for correlated spectral features.`],
[`Input`, `Optimum feature combination (standardised).`],
[`Output → next step`, `Predictions → Activity 2.4.`]], [2200, 7106], `Step 2.2.5 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Tune the number of latent variables (1–15) in the inner folds.`));
K.push(P(`**Supporting studies.** Wold et al. (2001); Barker and Rayens (2003); Guo et al. (2021).`));
K.push(...tab2('cpls', [[`Aspect`, `Partial least squares discriminant analysis (PLS-DA) and regression (PLSR)`],
[`Principle (how it works)`, `Projects correlated features onto a few latent variables that have maximum covariance with the target, then fits a linear model on them.`],
[`Problem it solves`, `Linear modelling of many correlated predictors without collinearity problems.`],
[`Specification in this study`, `Standardised inputs; classes coded as dummy variables for discriminant analysis.`],
[`Hyper-parameters and how they are tuned`, `Number of latent variables 1–15, chosen in the inner folds.`],
[`Data on which it works well`, `Spectral data with strong collinearity; linear or near-linear relations.`],
[`Why it was selected`, `Linear reference used in most hyperspectral disease studies (for example yellow rust monitoring by Guo et al., 2021).`],
[`Key references`, `Wold et al. (2001); Barker and Rayens (2003)`]], [2300, 7006], `Method card – Partial least squares discriminant analysis (PLS-DA) and regression (PLSR).`, 16));
K.push(H3(`Step 2.2.6 – Tuning grids of the machine-learning models`));
K.push(...tab2('s226', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `All models must be tuned in the same honest way.`],
[`Input`, `Inner folds (Step F2).`],
[`Output → next step`, `Tuned hyper-parameters of every model, fold and sensor set → final training.`]], [2200, 7106], `Step 2.2.6 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Use the grids in ${T('mlgrid')}; choose the combination with the best mean inner score.`));
K.push(P(`**Supporting studies.** Kuhn and Johnson (2013); Cawley and Talbot (2010).`));
K.push(...tab2('mlgrid', [[`Model`, `Tasks`, `Hyper-parameters tuned (inner cross-validation)`],
[`Support vector machine / regression`, `A, B / C`, `C ∈ {0.1, 1, 10, 100}; γ ∈ {0.001, 0.01, 0.1, scale}; ε ∈ {0.1, 0.5} (regression)`],
[`Random forest`, `A, B, C`, `500 trees; features per split ∈ {√p, 0.3p}; minimum leaf size ∈ {1, 3, 5}`],
[`Extreme gradient boosting`, `A, B, C`, `trees ∈ {200, 500}; depth ∈ {3, 5}; learning rate ∈ {0.05, 0.1}; subsample 0.8`],
[`k-nearest neighbours`, `A, B, C`, `k ∈ {3, 5, 7, 9, 11}; uniform or distance weights`],
[`Partial least squares (discriminant analysis / regression)`, `A, B / C`, `number of latent variables 1–15`]], [3100, 1100, 5106], `Machine-learning models and tuning grids.`, 17));
K.push(H2(`Activity 2.3 – Deep-learning models`));
K.push(P(`Two kinds of networks are used. Feature-fusion networks (DNN-F1, DNN-F2) take the fused feature vector directly. Pseudo-image networks (DT-EDNet and the three comparison networks) first reshape the feature vector into a small two-dimensional "image", as in Ma et al. (2026). All networks are trained on exactly the same folds as the machine-learning models.`));
K.push(H3(`Step 2.3.1 – Deep neural network with input-level feature fusion (DNN-F1)`));
K.push(...tab2('s231', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Learns non-linear interactions between the features of different cameras from one concatenated vector.`],
[`Input`, `Fused feature set (standardised).`],
[`Output → next step`, `Predictions → Activity 2.4.`]], [2200, 7106], `Step 2.3.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Concatenate the features of all cameras of the set.`));
K.push(NL(`Two dense layers (64 and 32 units) with batch normalisation, ReLU activation and dropout, then the output layer (softmax for classes, linear for the score).`));
K.push(NL(`Adam optimiser, learning rate 0.001, weight decay 10^{−4}, batch size 32, up to 500 epochs with early stopping (patience 30) on the inner validation plots; five random seeds averaged.`));
K.push(P(`**Supporting studies.** Maimaitijiang et al. (2020); Kingma and Ba (2015); Srivastava et al. (2014); Ioffe and Szegedy (2015).`));
K.push(H3(`Step 2.3.2 – Deep neural network with intermediate-level feature fusion (DNN-F2)`));
K.push(...tab2('s232', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Lets each camera be processed separately before fusion and learns how much each camera contributes.`],
[`Input`, `Selected features of each camera in the set (standardised).`],
[`Output → next step`, `Predictions and camera attention weights → Activities 2.4 and 2.5.`]], [2200, 7106], `Step 2.3.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`One small sub-network per camera (one or two dense layers of 16–32 units).`));
K.push(NL(`A squeeze-and-excitation (SE) attention block gives each camera branch a learned weight.`));
K.push(NL(`Concatenate the weighted branches → dense layer of 32 units → output; same training as DNN-F1; used only for sets with two or more cameras.`));
K.push(P(`**Supporting studies.** Maimaitijiang et al. (2020); squeeze-and-excitation: Hu et al. (2018).`));
K.push(...fig2('dnn', 'g21_dnn.png', `Feature-fusion networks: DNN-F1 (input-level fusion) and DNN-F2 (intermediate fusion with camera attention).`, 540));
K.push(...tab2('cdnnf', [[`Aspect`, `Feature-fusion deep neural networks (DNN-F1 and DNN-F2)`],
[`Principle (how it works)`, `Fully connected layers learn weighted, non-linear combinations of the input features; DNN-F2 first learns a representation for each camera and weights the cameras with attention.`],
[`Problem it solves`, `Non-linear fusion of features from several cameras; DNN-F2 also shows which camera the model relies on.`],
[`Specification in this study`, `DNN-F1: 64–32 units; DNN-F2: 16–32 units per camera branch, attention block, 32 units; batch normalisation; dropout; class-weighted cross-entropy or mean squared error.`],
[`Hyper-parameters and how they are tuned`, `Units ∈ {32, 64} (first layer) and dropout ∈ {0.2, 0.3, 0.4}, tuned in the inner folds; epochs by early stopping.`],
[`Data on which it works well`, `About a thousand samples with tens of features; multi-sensor feature vectors.`],
[`Why it was selected`, `Compact enough for the sample size; intermediate fusion was better than input fusion in multi-sensor UAV data (Maimaitijiang et al., 2020).`],
[`Key references`, `Maimaitijiang et al. (2020); Hu et al. (2018)`]], [2300, 7006], `Method card – Feature-fusion deep neural networks (DNN-F1 and DNN-F2).`, 16));
K.push(H3(`Step 2.3.3 – Pseudo-image construction`));
K.push(...tab2('s233', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Convolutional and transformer networks need a two-dimensional input, but each sample is a feature vector.`],
[`Input`, `Fused feature set or hyperspectral configuration (standardised).`],
[`Output → next step`, `One-channel pseudo-image of k × k pixels per sample → Steps 2.3.4–2.3.7.`]], [2200, 7106], `Step 2.3.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Order the features by camera (hyperspectral, multispectral, red–green–blue, thermal) and, within the hyperspectral camera, by group and wavelength (optimal wavelengths, indices, texture, TTFI), so that neighbouring pixels hold related features.`));
K.push(NL(`Choose k so that the k × k grid holds all features when every camera starts on a new row (minimum 3); fill the grid row by row. A small group such as the thermal features then stays together in one row and is not split.`));
K.push(NL(`Fill the remaining pixels with zeros (zero is the training mean after standardisation, so padding adds no information).`));
K.push(NL(`Example (hyperspectral only): 22 features → 5 × 5 image with 3 padded pixels (${F('pseudo')}). Example (S7, hyperspectral + thermal): 16 hyperspectral features fill three rows of six, the 6 thermal features fill the fourth row and two empty rows complete a 6 × 6 image.`));
K.push(P(`**Supporting studies.** Pseudo-two-dimensional input of spectral features: Ma et al. (2026); arranging non-image features as images for convolutional networks: Sharma et al. (2019); attention relates features regardless of their position: Vaswani et al. (2017).`));
K.push(NOTE(`Ma et al. (2026) used DT-EDNet with hyperspectral features only. Its use with thermal, multispectral and red–green–blue features is an extension made in this study; whether it helps is shown by comparing each fused set with the hyperspectral set (S1) and with DNN-F2, which processes each camera in its own branch.`));
K.push(...fig2('pseudo', 'g18_pseudoimage.png', `Construction of a pseudo-image from a standardised feature vector (dummy values).`, 540));
K.push(...tab2('cpseudo', [[`Aspect`, `Pseudo-image (feature-to-image) representation`],
[`Principle (how it works)`, `Places the features of one sample on a small grid so that convolution and attention can relate neighbouring and distant features.`],
[`Problem it solves`, `Allows image networks to be applied to tabular features.`],
[`Specification in this study`, `Group-and-wavelength ordering; k = ⌈√p⌉ (minimum 3); zero padding after standardisation; one channel.`],
[`Hyper-parameters and how they are tuned`, `No tuning (fixed ordering, so results are reproducible).`],
[`Data on which it works well`, `Ordered features such as spectra, where neighbours are related.`],
[`Why it was selected`, `Needed to reproduce the DT-EDNet design; the fixed ordering keeps related features together.`],
[`Key references`, `Ma et al. (2026); Sharma et al. (2019)`]], [2300, 7006], `Method card – Pseudo-image (feature-to-image) representation.`, 16));
K.push(H3(`Step 2.3.4 – DT-EDNet (Dual Transformer Early Detection Network)`));
K.push(...tab2('s234', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Captures local relations between neighbouring features (convolution and attention) and long-range relations between distant features (self-attention) in one network.`],
[`Input`, `Pseudo-images.`],
[`Output → next step`, `Predictions → Activity 2.4; module ablation → Step 2.5.3.`]], [2200, 7106], `Step 2.3.4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Embedding: 3 × 3 convolution (stride 1) to 128 channels.`));
K.push(NL(`Squeeze-and-excitation block: global average pooling of each channel → two small dense layers → sigmoid weight per channel → channels re-weighted.`));
K.push(NL(`Tokens: flatten the k × k map into k² tokens of length 128 and add a learnable class token (and position embedding).`));
K.push(NL(`Dual Transformer Group: one Kernel Transformer Block (convolution with the convolutional block attention module, CBAM: channel attention then spatial attention) followed by four Token Transformer Blocks (layer normalisation → multi-head self-attention with 4 heads → layer normalisation → feed-forward network, each with a residual connection); dropout 0.03.`));
K.push(NL(`Head: layer normalisation of the class token → linear layer (softmax for classes, one linear output for the score).`));
K.push(P(`**Supporting studies.** DT-EDNet: Ma et al. (2026); squeeze-and-excitation: Hu et al. (2018); CBAM: Woo et al. (2018); self-attention and transformers: Vaswani et al. (2017); class token: Dosovitskiy et al. (2021).`));
K.push(...fig2('dtednet', 'g19_dtednet.png', `Architecture of DT-EDNet (after Ma et al., 2026) and the role of its three attention mechanisms.`, 560));
K.push(EQ(`Attention(Q, K, V) = softmax( Q K^{T} / √d ) V`));
K.push(P(`In self-attention every token forms a query Q, a key K and a value V; the softmax of the scaled products Q K^{T} decides how much each token takes from every other token, d being the token length per head (128 / 4 = 32). This is how a red-edge wavelength can be related directly to a texture feature placed far away on the pseudo-image.`));
K.push(...tab2('cdtednet', [[`Aspect`, `DT-EDNet (Dual Transformer Early Detection Network)`],
[`Principle (how it works)`, `A hybrid network: convolution embeds the pseudo-image, squeeze-and-excitation re-weights channels, the Kernel Transformer Block (convolution + CBAM) learns local spatial–channel patterns and the Token Transformer Blocks (multi-head self-attention) learn global relations; the class token summarises the sample.`],
[`Problem it solves`, `Models both local and long-range interactions among selected spectral, index and texture features.`],
[`Specification in this study`, `Embedding 128; SE block; 1 Kernel Transformer Block + 4 Token Transformer Blocks; 4 heads; dropout 0.03; trained from scratch; input = fused features of all cameras in the sensor set (each camera on its own rows).`],
[`Hyper-parameters and how they are tuned`, `Fixed architecture as published; learning rate and dropout tuned in the inner folds (Step 2.3.8).`],
[`Data on which it works well`, `Sets of a few to a few tens of ordered features with complex interactions; best with thousands of samples.`],
[`Why it was selected`, `Highest accuracy on rice blast (overall accuracy 95.25% with optimal wavelengths + indices + TTFI) against EfficientNet, ResNet18 and ConvNeXt V2 (Ma et al., 2026); tested here under plot-grouped validation.`],
[`Key references`, `Ma et al. (2026); Hu et al. (2018); Woo et al. (2018); Vaswani et al. (2017)`]], [2300, 7006], `Method card – DT-EDNet (Dual Transformer Early Detection Network).`, 16));
K.push(H3(`Step 2.3.5 – EfficientNet (comparison network)`));
K.push(...tab2('s235', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A modern, efficient convolutional network used as a comparison in the DT-EDNet study.`],
[`Input`, `Pseudo-images.`],
[`Output → next step`, `Predictions → Activity 2.4.`]], [2200, 7106], `Step 2.3.5 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`EfficientNet-B0: mobile inverted bottleneck blocks with depthwise convolution and squeeze-and-excitation.`));
K.push(NL(`Stem changed to a 3 × 3 convolution with stride 1 and one input channel (the input is only a few pixels wide).`));
K.push(NL(`Global average pooling → linear head; trained from scratch.`));
K.push(P(`**Supporting studies.** Tan and Le (2019); Ma et al. (2026).`));
K.push(H3(`Step 2.3.6 – ResNet18 (comparison network)`));
K.push(...tab2('s236', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A classic residual convolutional network used as a comparison.`],
[`Input`, `Pseudo-images.`],
[`Output → next step`, `Predictions → Activity 2.4.`]], [2200, 7106], `Step 2.3.6 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Four stages of two basic residual blocks (two 3 × 3 convolutions with an identity shortcut).`));
K.push(NL(`Stem changed to a 3 × 3 convolution with stride 1 and no max-pooling.`));
K.push(NL(`Global average pooling → linear head; trained from scratch.`));
K.push(P(`**Supporting studies.** He et al. (2016); Ma et al. (2026).`));
K.push(H3(`Step 2.3.7 – ConvNeXt V2 (comparison network)`));
K.push(...tab2('s237', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A recent convolutional network that borrows design ideas from transformers, used as a comparison.`],
[`Input`, `Pseudo-images.`],
[`Output → next step`, `Predictions → Activity 2.4.`]], [2200, 7106], `Step 2.3.7 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`ConvNeXt V2-Atto (smallest version, about 3.7 million parameters): blocks with 7 × 7 depthwise convolution, layer normalisation and a feed-forward network with global response normalisation.`));
K.push(NL(`Stem changed to stride 1; global average pooling → linear head; trained from scratch.`));
K.push(P(`**Supporting studies.** Woo et al. (2023); Ma et al. (2026).`));
K.push(...fig2('cnns', 'g20_cnns.png', `The three comparison networks with the changes made for small pseudo-images.`, 540));
K.push(...tab2('ccnn', [[`Aspect`, `Comparison networks: EfficientNet-B0, ResNet18 and ConvNeXt V2-Atto`],
[`Principle (how it works)`, `Convolutional networks: EfficientNet scales depth, width and resolution together and uses squeeze-and-excitation; ResNet adds identity shortcuts so deep networks train well; ConvNeXt V2 uses large depthwise kernels and global response normalisation.`],
[`Problem it solves`, `Benchmarks that show whether the transformer parts of DT-EDNet add accuracy over strong convolutional designs.`],
[`Specification in this study`, `One input channel; stride-1 stems; global average pooling; linear head; trained from scratch with the same settings as DT-EDNet.`],
[`Hyper-parameters and how they are tuned`, `Same tuning budget as DT-EDNet (learning rate and dropout in the inner folds).`],
[`Data on which it works well`, `Image-like inputs; large datasets (risk of overfitting with about a thousand samples, controlled by early stopping and regularisation).`],
[`Why it was selected`, `Exactly the comparison set used by Ma et al. (2026); covers classic, efficient and modern convolutional designs.`],
[`Key references`, `He et al. (2016); Tan and Le (2019); Woo et al. (2023); Kattenborn et al. (2021)`]], [2300, 7006], `Method card – Comparison networks: EfficientNet-B0, ResNet18 and ConvNeXt V2-Atto.`, 16));
K.push(H3(`Step 2.3.8 – Common training protocol and tuning of the pseudo-image networks`));
K.push(...tab2('s238', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A fair comparison requires identical training settings for all four networks.`],
[`Input`, `Pseudo-images of the training part; inner validation plots.`],
[`Output → next step`, `Trained networks (five seeds each) → Activity 2.4.`]], [2200, 7106], `Step 2.3.8 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Optimiser: AdamW, initial learning rate 6 × 10^{−4}, weight decay 1 × 10^{−5}; cosine annealing of the learning rate to 1 × 10^{−6} over 300 epochs; batch size 32.`));
K.push(NL(`Loss: cross-entropy with label smoothing 0.01 and class weights (classes); mean squared error (score).`));
K.push(NL(`Gradient clipping at a maximum norm of 1.2; early stopping with patience 60 epochs and minimum improvement 5 × 10^{−5}.`));
K.push(NL(`Model selection on the inner validation plots (macro-F1 for classes because the classes are unequal; root-mean-square error for the score), not on a random 10% of samples.`));
K.push(NL(`Tuning: learning rate ∈ {3 × 10^{−4}, 6 × 10^{−4}, 1 × 10^{−3}} and dropout ∈ {0.03, 0.1, 0.3}, same grid for all four networks. To keep the computing load feasible (about 34 000 runs if every case were tuned), each network is tuned once, on outer fold 1, sensor set S15 and Task B with one seed, and the chosen values are then used for all sensor sets, tasks and folds (about 3800 runs).`));
K.push(NL(`Five random seeds (42 and four others); report mean ± standard deviation.`));
K.push(P(`**Supporting studies.** Training settings: Ma et al. (2026); AdamW: Loshchilov and Hutter (2019); cosine annealing: Loshchilov and Hutter (2017); label smoothing: Szegedy et al. (2016), Müller et al. (2019); gradient clipping: Pascanu et al. (2013).`));
K.push(...tab2('ctrain', [[`Aspect`, `Training techniques (AdamW, cosine annealing, label smoothing, gradient clipping, early stopping)`],
[`Principle (how it works)`, `AdamW adapts the step size of every weight and applies weight decay separately; cosine annealing lowers the learning rate smoothly; label smoothing replaces hard 0/1 targets with slightly softened ones; gradient clipping limits very large updates; early stopping ends training when the validation score stops improving.`],
[`Problem it solves`, `Stable training and less overfitting on a small dataset.`],
[`Specification in this study`, `Values of Step 2.3.8 (from Ma et al., 2026).`],
[`Hyper-parameters and how they are tuned`, `Learning rate and dropout tuned; other values fixed as published.`],
[`Data on which it works well`, `Neural networks trained from scratch on small to medium datasets.`],
[`Why it was selected`, `Reproduces the published protocol, so differences come from the data and validation design, not from different training.`],
[`Key references`, `Loshchilov and Hutter (2017, 2019); Müller et al. (2019); Pascanu et al. (2013)`]], [2300, 7006], `Method card – Training techniques (AdamW, cosine annealing, label smoothing, gradient clipping, early stopping).`, 16));
K.push(H2(`Activity 2.4 – Evaluation`));
K.push(H3(`Step 2.4.1 – Classification metrics`));
K.push(...tab2('s241', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Accuracy must reflect unequal classes and ordered grades.`],
[`Input`, `Predictions on the three test replications.`],
[`Output → next step`, `Metric tables → Activity 2.5.`]], [2200, 7106], `Step 2.4.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Task A: overall accuracy, sensitivity, specificity, F1 and area under the receiver operating characteristic curve (AUC).`));
K.push(NL(`Task B: overall accuracy, Cohen's kappa, quadratic-weighted kappa (ordered grades), macro-averaged recall and F1, per-class precision, recall and F1, confusion matrix and the share of predictions within one grade of the true grade.`));
K.push(P(`**Supporting studies.** Cohen (1960, 1968); Sokolova and Lapalme (2009); Fawcett (2006); the metrics of Ma et al. (2026) (overall accuracy, kappa, macro recall, macro-F1, per-class scores) are all included.`));
K.push(EQ(`OA = correct / N;    precision = TP / (TP + FP);    recall = TP / (TP + FN);    F1 = 2 × precision × recall / (precision + recall)`));
K.push(EQ(`κ = (p_{o} − p_{e}) / (1 − p_{e});    κ_{w} = 1 − Σ w_{ij} O_{ij} / Σ w_{ij} E_{ij},   w_{ij} = (i − j)^{2} / (k − 1)^{2}`));
K.push(H3(`Step 2.4.2 – Regression metrics`));
K.push(...tab2('s242', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The severity-score models need error measures in score units.`],
[`Input`, `Predicted and observed scores of the test replications.`],
[`Output → next step`, `Metric tables → Activity 2.5.`]], [2200, 7106], `Step 2.4.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Coefficient of determination (R²), root-mean-square error (RMSE) and ratio of performance to deviation (RPD = standard deviation of observed scores / RMSE).`));
K.push(P(`**Supporting studies.** Chang et al. (2001); Guo et al. (2021); Feng et al. (2022).`));
K.push(EQ(`R^{2} = 1 − Σ (y − ŷ)^{2} / Σ (y − ȳ)^{2};    RMSE = √[ (1/n) Σ (y − ŷ)^{2} ];    RPD = SD_{y} / RMSE`));
K.push(H3(`Step 2.4.3 – Worked example of the metrics`));
K.push(...tab2('s243', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Shows how the numbers in the result tables are obtained.`],
[`Input`, `Dummy confusion matrix and dummy predictions.`],
[`Output → next step`, `Example values (below).`]], [2200, 7106], `Step 2.4.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Classification: from the confusion matrix in ${F('dummycm')} (532 test samples), 396 are on the diagonal, so overall accuracy = 396 / 532 = 0.744; chance agreement p_{e} = 0.182, so κ = (0.744 − 0.182) / (1 − 0.182) = 0.687; quadratic-weighted kappa = 0.937 (most errors are between neighbouring grades); macro-F1 = 0.733; 97.4% of predictions are within one grade.`));
K.push(NL(`Regression: for eight dummy subplots with observed scores 0, 1, 3, 5, 7, 9, 3, 5 and predictions 0.4, 1.6, 2.5, 5.8, 6.1, 8.2, 3.9, 4.4: R² = 0.94, RMSE = 0.71 and RPD = 3.00 / 0.71 = 4.2.`));
K.push(P(`**Supporting studies.** Cohen (1960); Sokolova and Lapalme (2009); Chang et al. (2001).`));
K.push(...fig2('dummycm', 'g22_dummy_cm.png', `Dummy confusion matrix of one test replication (six grades).`, 360));
K.push(...tab2('cmetrics', [[`Aspect`, `Evaluation metrics`],
[`Principle (how it works)`, `Overall accuracy counts correct predictions; kappa corrects it for chance; weighted kappa gives partial credit to near misses between ordered grades; F1 combines precision and recall per class; R², RMSE and RPD describe regression error.`],
[`Problem it solves`, `Measures performance fairly when classes are unequal and ordered.`],
[`Specification in this study`, `Computed on the pooled predictions of the three test replications and per fold; mean ± standard deviation over folds and seeds.`],
[`Hyper-parameters and how they are tuned`, `None.`],
[`Data on which it works well`, `Classification with unequal, ordered classes; continuous scores.`],
[`Why it was selected`, `Covers the metrics of the DT-EDNet study and the extra ones needed for ordered grades and regression.`],
[`Key references`, `Cohen (1960, 1968); Sokolova and Lapalme (2009); Chang et al. (2001)`]], [2300, 7006], `Method card – Evaluation metrics.`, 16));
K.push(H2(`Activity 2.5 – Comparison, ablation and interpretation`));
K.push(H3(`Step 2.5.1 – Ranking of sensor sets and models`));
K.push(...tab2('s251', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Identifies the best sensor set and model for each task.`],
[`Input`, `Metric tables of 15 sets × models × tasks.`],
[`Output → next step`, `Best sensor set and model per task → conclusions and maps.`]], [2200, 7106], `Step 2.5.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Rank the 15 sets by macro-F1 (Task B), AUC (Task A) and RMSE (Task C) for each model.`));
K.push(NL(`Compare the best machine-learning, best feature-fusion network and best pseudo-image network.`));
K.push(NL(`Call a difference real only if it is larger than the fold-to-fold standard deviation and appears in all three folds.`));
K.push(P(`**Supporting studies.** Feng et al. (2022); Maimaitijiang et al. (2020); Ma et al. (2026).`));
K.push(H3(`Step 2.5.2 – Fusion gain and drop-one-camera ablation`));
K.push(...tab2('s252', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Answers directly whether a camera is worth flying.`],
[`Input`, `Metrics of single cameras and combinations.`],
[`Output → next step`, `Fusion gains and the contribution of each camera → conclusions.`]], [2200, 7106], `Step 2.5.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Fusion gain = metric of a combination minus the metric of its best single camera.`));
K.push(NL(`Remove one camera at a time from S15 and record the drop in macro-F1 and R².`));
K.push(NL(`Report the camera attention weights of DNN-F2.`));
K.push(P(`**Supporting studies.** Ablation of feature groups: Ma et al. (2026); fusion gain: Feng et al. (2022), Maimaitijiang et al. (2020).`));
K.push(H3(`Step 2.5.3 – Network comparison on the hyperspectral configurations and DT-EDNet module ablation`));
K.push(...tab2('s253', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Shows whether DT-EDNet is better than the comparison networks under plot-grouped validation and which of its modules matter.`],
[`Input`, `Results of the four pseudo-image networks on the six configurations (Step 2.1.5); the best machine-learning model on the same inputs.`],
[`Output → next step`, `Network comparison table; ablation table → conclusions.`]], [2200, 7106], `Step 2.5.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Compare DT-EDNet, EfficientNet, ResNet18, ConvNeXt V2 and the best machine-learning model on the six configurations (overall accuracy, kappa, macro recall, macro-F1, per-class F1, RMSE).`));
K.push(NL(`Ablation on the best configuration: DT-EDNet without the squeeze-and-excitation block, without the Dual Transformer Group, and without both.`));
K.push(NL(`Report mean ± standard deviation over three folds × five seeds.`));
K.push(P(`**Supporting studies.** Network comparison and module ablation: Ma et al. (2026).`));
K.push(...tab2('ablationt', [[`Model (template)`, `Overall accuracy`, `Kappa`, `Macro recall`, `Macro-F1`],
[`DT-EDNet (full)`, `…`, `…`, `…`, `…`],
[`without squeeze-and-excitation block`, `…`, `…`, `…`, `…`],
[`without Dual Transformer Group`, `…`, `…`, `…`, `…`],
[`without both`, `…`, `…`, `…`, `…`]], [3400, 1500, 1300, 1500, 1606], `Template for the DT-EDNet module ablation (same folds and seeds for all rows).`, 17));
K.push(H3(`Step 2.5.4 – Shapley additive explanations (SHAP) and selection stability`));
K.push(...tab2('s254', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Shows which features drive the best models and how stable the selected features are.`],
[`Input`, `Best models; selected features of every fold.`],
[`Output → next step`, `Feature-importance figures; stability table → Objective 1 discussion.`]], [2200, 7106], `Step 2.5.4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Compute SHAP values of the best machine-learning model of each task; summarise the mean |SHAP| per feature and per camera.`));
K.push(NL(`Compare the most important features with the biochemical and biophysical parameters that changed with disease (Activity 1.7), to give the model a physiological explanation.`));
K.push(NL(`Count how often every feature is selected over the three folds; final feature lists contain features selected in at least two of three folds.`));
K.push(P(`**Supporting studies.** Lundberg and Lee (2017); Lundberg et al. (2020); Nogueira et al. (2018).`));
K.push(...tab2('cablation', [[`Aspect`, `Ablation and Shapley interpretation`],
[`Principle (how it works)`, `Ablation removes one part (a camera, a feature group or a network module) and measures the loss; SHAP divides each prediction among the features.`],
[`Problem it solves`, `Shows what each camera, feature type and network module contributes.`],
[`Specification in this study`, `Drop-one-camera from S15; DT-EDNet without SE, without Dual Transformer Group, without both; SHAP on the best machine-learning models.`],
[`Hyper-parameters and how they are tuned`, `None.`],
[`Data on which it works well`, `Any trained model on the same folds.`],
[`Why it was selected`, `Direct, easy-to-explain evidence of contribution; both used in the DT-EDNet study.`],
[`Key references`, `Ma et al. (2026); Lundberg and Lee (2017)`]], [2300, 7006], `Method card – Ablation and Shapley interpretation.`, 16));
K.push(H3(`Step 2.5.5 – Covariate baseline and sensor + covariate models`));
K.push(...tab2('s255', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Severity rises with days after inoculation and differs with variety, inoculation timing, growth stage and weather; a sensor model could look accurate only because it learns time or stage. The cameras must add information beyond these known factors.`],
[`Input`, `Covariates (Step A6); fused feature sets of the sensor sets; same folds.`],
[`Output → next step`, `Accuracy of the covariate-only model, of the sensor models and of the sensor + covariate models → evidence of what the cameras add.`]], [2200, 7106], `Step 2.5.5 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Samples: inoculated, unsprayed subplots only; the healthy plots are fungicide-protected and share every covariate with their inoculated plots, so they would teach a false rule. Weather windows end the day before each flight (no look-ahead).`));
K.push(NL(`B1 – interpretable epidemiological model: logistic regression (Task A), proportional-odds ordinal logistic regression (Task B; McCullagh, 1980) and a linear model of the disease index with days after inoculation and its square (Task C; disease-progress shape, Madden et al., 2007), with variety, inoculation timing and growth stage.`));
K.push(NL(`B2 – machine-learning baseline: the best model of Activity 2.2 (for example random forest; Breiman, 2001) with all covariates, including the weather summaries and favourable days, tuned with the same inner grid search as the sensor models.`));
K.push(NL(`M0 = the stronger of B1 and B2 (covariates only); M1 = the sensor models of each sensor set (Activities 2.2–2.3); M2 = the best three sensor sets + covariates (one-hot variety and timing, ordinal growth stage, numeric days after inoculation and weather), labelled "within-season".`));
K.push(NL(`Gains: ΔS = metric(M1) − metric(M0) (what the cameras add); ΔC = metric(M2) − metric(M1) (what known context adds); ΔT = metric(M2) − metric(M0). Metrics: macro-F1 and AUC (Task A), macro-F1 and quadratic-weighted kappa (Task B), R² and RMSE (Task C).`));
K.push(NL(`Is a gain real? 95% confidence interval from 2000 bootstrap resamples of the pooled test predictions that resample whole plots (Efron and Tibshirani, 1993); AUCs of M1 and M0 compared with the DeLong test (DeLong et al., 1988). A gain is real only if the interval excludes zero, it is larger than the fold-to-fold standard deviation and it has the same sign in all three folds.`));
K.push(NL(`The coefficients of B1, fitted on all inoculated subplots with standardised covariates, show the direction and size of each known effect (for example later sowing or variety).`));
K.push(P(`**Supporting studies.** Calendar effect in disease prediction: De Wolf and Isard (2007); weather-only machine learning for disease severity: Bijlwan et al. (2025); combining weather with remote sensing compared with a weather-only model: Zhang et al. (2014), Ruan et al. (2022); weather-based white rust forecasting: Chattopadhyay et al. (2011); simple baseline models as a reference for predictive models: Kuhn and Johnson (2013); bootstrap and DeLong test: Efron and Tibshirani (1993), DeLong et al. (1988).`));
K.push(...tab2('covex', [[`Model set (dummy results, Task B)`, `Inputs`, `Macro-F1`, `Gain (95% bootstrap interval)`],
[`M0 – covariate baseline (stronger of B1, B2)`, `days after inoculation, variety, timing, stage, weather`, `0.41`, `—`],
[`M1 – hyperspectral (S1)`, `S1 fused features`, `0.66`, `ΔS = +0.25 (+0.18 to +0.31): real`],
[`M1 – hyperspectral + thermal (S7)`, `S7 fused features`, `0.69`, `ΔS = +0.28 (+0.21 to +0.34): real`],
[`M2 – hyperspectral + thermal + covariates`, `S7 features + covariates`, `0.71`, `ΔC = +0.02 (−0.02 to +0.06): not real; within-season`]], [2900, 2700, 1100, 2606], `Worked example (dummy data): how the covariate baseline and the bootstrap intervals show what the cameras add.`, 17));
K.push(H2(`Activity 2.6 – Robustness and maps`));
K.push(H3(`Step 2.6.1 – Performance by treatment`));
K.push(...tab2('s261', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `A model may work for one variety or crop age and fail for another.`],
[`Input`, `Test predictions with treatment codes.`],
[`Output → next step`, `Treatment-wise metric tables.`]], [2200, 7106], `Step 2.6.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Report the metrics for each variety, inoculation timing and date.`));
K.push(P(`**Supporting studies.** Liu et al. (2024); Blasch et al. (2023); Feng et al. (2022).`));
K.push(H3(`Step 2.6.2 – Leave-one-variety-out and leave-one-timing-out tests`));
K.push(...tab2('s262', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Tests whether models transfer to a variety or crop age not seen in training.`],
[`Input`, `Best machine-learning and best deep-learning model of the three best sensor sets.`],
[`Output → next step`, `Transfer results → conclusions on robustness.`]], [2200, 7106], `Step 2.6.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Train on two varieties and test on the third, for each variety in turn (V1 PM 26, V2 Pusa Vijay, V3 PM 37); a variety with very few diseased samples is used only for the detection task.`));
K.push(NL(`Train on three inoculation timings and test on the fourth.`));
K.push(NL(`All results come from one season; transfer to another season needs an independent test with data of that season, as done across years by Ma et al. (2026).`));
K.push(P(`**Supporting studies.** Blocked validation for extrapolation: Roberts et al. (2017); independent-year test: Ma et al. (2026).`));
K.push(H3(`Step 2.6.3 – Severity maps`));
K.push(...tab2('s263', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Field users need maps rather than tables.`],
[`Input`, `Best model of each task; subplot features of every date.`],
[`Output → next step`, `Subplot maps of detection, severity class and score.`]], [2200, 7106], `Step 2.6.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Apply the best model of each task to all subplots of every date.`));
K.push(NL(`Map the predicted class and score together with the absolute error where scores exist.`));
K.push(P(`**Supporting studies.** Abdulridha et al. (2023); Liu et al. (2024); Deng et al. (2024); Liu et al. (2026).`));
K.push(H2(`Activity 2.7 – Independent testing at Bharatpur`));
K.push(P(`The validation (Activity F, leave-one-replication-out inside the IARI field) chooses the models and estimates their accuracy on new plots of the same field. Independent testing then applies the frozen final models once to data from research farms and farmers' fields at Bharatpur (Step A7), with other soils, varieties, management and a natural epidemic (${F('twostage')}). This is a test, not a validation: nothing is selected, tuned or retrained on the Bharatpur data.`));
K.push(...fig2('twostage', 'g28_twostage.png', `Internal validation inside the IARI field and independent testing on Bharatpur data with frozen models.`, 560));
K.push(H3(`Step 2.7.1 – Final models trained on all IARI data and frozen`));
K.push(...tab2('s271', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Models for an independent test must be fixed before the test data are seen.`],
[`Input`, `All IARI post-symptomatic samples (1920 per camera); the selection and tuning procedure of Objectives 1 and 2.`],
[`Output → next step`, `Frozen final models with their selected features, hyper-parameters and standardisation constants → Steps 2.7.2–2.7.3.`]], [2200, 7106], `Step 2.7.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Repeat feature selection and tuning on all IARI data with grouped inner cross-validation (folds by plot), exactly as in the internal validation.`));
K.push(NL(`Train the final models on all IARI data: the best machine-learning model and the best deep-learning model of each task, for the three best sensor sets, the full set (S15) and the best low-cost set without the hyperspectral camera.`));
K.push(NL(`Store the selected features, hyper-parameters, standardisation means and standard deviations, and the trained weights; nothing is changed afterwards.`));
K.push(P(`**Supporting studies.** Final model refitted on all development data after nested validation: Cawley and Talbot (2010), Kuhn and Johnson (2013).`));
K.push(H3(`Step 2.7.2 – Processing of the Bharatpur data with the same steps`));
K.push(...tab2('s272', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `The test data must pass through exactly the same processing, otherwise differences in processing would look like model errors.`],
[`Input`, `Bharatpur images, quadrat polygons, severity grades and covariates (Step A7).`],
[`Output → next step`, `Bharatpur feature tables in the same layout as the IARI tables → Step 2.7.3.`]], [2200, 7106], `Step 2.7.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Apply Activities B–D unchanged: calibration, mosaics, quality control, co-registration, resampling, quadrat means and feature extraction.`));
K.push(NL(`Build the vegetation mask with the same procedure (Activity C) on the Bharatpur images, because soils and weeds differ; this uses no labels.`));
K.push(NL(`Compute only the features selected for the frozen models; standardise them with the IARI constants (frozen).`));
K.push(NL(`Features that need a healthy reference (difference from healthy plots, healthy-normalised features) are used only where a fungicide-protected strip exists; otherwise models without these features are used (canopy minus air temperature and the normalised relative canopy temperature need no healthy reference).`));
K.push(P(`**Supporting studies.** Processing fixed on the development data and applied to new data: Kuhn and Johnson (2013); same-sensor protocols across sites: Aasen et al. (2018).`));
K.push(H3(`Step 2.7.3 – Application and evaluation of the frozen models`));
K.push(...tab2('s273', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Shows how accurate the models are on new fields and how much accuracy is lost compared with the internal validation.`],
[`Input`, `Frozen models; Bharatpur feature tables and severity grades.`],
[`Output → next step`, `Independent test accuracy tables and the loss of accuracy from the internal validation to the independent test → conclusions on transferability.`]], [2200, 7106], `Step 2.7.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Predict every Bharatpur quadrat-date once with each frozen model; no retraining or re-tuning.`));
K.push(NL(`Compute the same metrics as in Activity 2.4 (overall accuracy, kappa, weighted kappa, macro-F1, AUC; R², RMSE, RPD).`));
K.push(NL(`Report the results for research farms and farmers' fields separately, by variety and by growth stage, and the difference from the accuracy of the internal validation.`));
K.push(NL(`As a second, clearly labelled result, re-standardise the features with the means and standard deviations of the Bharatpur data (no labels used) to show how much of any loss comes from a simple shift between sites.`));
K.push(NL(`Test the covariate models (Step 2.5.5) on Bharatpur weather as well; this is the first test of the weather effect outside the IARI season data.`));
K.push(P(`**Supporting studies.** Independent external test after internal validation: Ma et al. (2026); spatial transfer and loss of accuracy at new locations: Ploton et al. (2020), Roberts et al. (2017); cross-scale transfer of UAV disease models: Yuan et al. (2025).`));
K.push(...tab2('twostaget', [[`Item`, `Validation (internal, IARI field)`, `Independent testing (Bharatpur)`],
[`Data`, `IARI field, 48 plots, 13 dates`, `Bharatpur research farms and farmers' fields`],
[`Infection`, `artificial inoculation (30 December 2026)`, `natural epidemic`],
[`Design`, `leave-one-replication-out, nested`, `frozen final models applied once`],
[`Used for`, `feature selection, tuning, model choice, accuracy on new plots`, `accuracy on new fields, varieties and management`],
[`Varieties`, `PM 26, Pusa Vijay, PM 37`, `local varieties (recorded)`]], [2000, 3600, 3706], `Internal validation and independent testing.`, 17));
K.push(H3(`Step 2.7.4 – Severity maps of farmers' fields`));
K.push(...tab2('s274', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Farm-level maps show whether the models are useful where decisions are made.`],
[`Input`, `Frozen best models; Bharatpur images.`],
[`Output → next step`, `Severity maps of the farmers' fields with the scored quadrats overlaid → reporting.`]], [2200, 7106], `Step 2.7.4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Apply the best model of each task to the whole vegetated area of each field in quadrat-sized cells.`));
K.push(NL(`Overlay the scored quadrats and their grades to show agreement and errors.`));
K.push(P(`**Supporting studies.** UAV disease maps of smallholder fields: Liu et al. (2026); severity maps from UAV models: Abdulridha et al. (2023), Liu et al. (2024).`));
K.push(H1(`5. Objective 3 – Prediction of white rust at the pre-symptomatic stage`));
K.push(P(`Objective 3 uses the 576 pre-symptomatic samples of each camera. The question is whether subplots that will develop white rust can be separated from healthy subplots before pustules are visible, and whether their later severity can be predicted. Machine-learning models and the feature-fusion networks (DNN-F1, DNN-F2) are used; the pseudo-image networks are not used here because about 384 training samples per fold are too few for them.`));
K.push(...fig2('obj3', 'g07_obj3.png', `Flow chart of Objective 3 (Activities 3.1–3.5).`, 540));
K.push(...fig2('obj3time', 'g27_obj3.png', `Pre-symptomatic and post-symptomatic periods and how pre-symptomatic samples are labelled from the later status of the same subplot.`, 600));
K.push(H2(`Activity 3.1 – Pre-symptomatic samples and labels`));
K.push(H3(`Step 3.1.1 – Labels from the later status of each subplot`));
K.push(...tab2('s311', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Before symptoms the visual score is zero everywhere; labels must come from what happens later.`],
[`Input`, `Pre-symptomatic subplot tables; scores of the first post-symptomatic date.`],
[`Output → next step`, `Labelled pre-symptomatic dataset → Activity 3.2.`]], [2200, 7106], `Step 3.1.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Classification: healthy = subplots of the 12 healthy plots; infected = inoculated subplots that show pustules later; inoculated subplots that never show symptoms are excluded from the infected class (the same labels as Activity 1.8).`));
K.push(NL(`Regression: target = disease index of the same subplot on the first post-symptomatic date.`));
K.push(NL(`Record days after inoculation for every sample.`));
K.push(P(`**Supporting studies.** Zhu et al. (2017); Tian et al. (2021); Mahlein et al. (2019); Yu et al. (2021) for the early stage of pine wilt disease.`));
K.push(H3(`Step 3.1.2 – Physiological changes before symptoms (7 January 2027)`));
K.push(...tab2('s312', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `If pigments, water status or gas exchange already change before pustules appear, there is a physiological reason why pre-symptomatic detection can work.`],
[`Input`, `Biochemical and biophysical parameters of 7 January (Step A8); later severity of the same plots.`],
[`Output → next step`, `Inoculated − healthy differences on the pre-symptomatic date and their relation with later severity → interpretation of Objective 3.`]], [2200, 7106], `Step 3.1.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Compare inoculated and healthy plots for every parameter with the paired comparison of Step 1.7.2 (12 pairs).`));
K.push(NL(`Correlate the pre-symptomatic parameters of the inoculated plots with their disease index on 18 January (first post-symptomatic sampling date of Step A8).`));
K.push(NL(`Report effect sizes and 95% confidence intervals; note the block and fungicide caveat of Step 1.7.2.`));
K.push(P(`**Supporting studies.** Pre-visual physiological changes behind early detection: Zarco-Tejada et al. (2018), Calderón et al. (2013); pre-symptomatic hyperspectral detection: Zhu et al. (2017).`));
K.push(H2(`Activity 3.2 – Normalisation to healthy plots`));
K.push(H3(`Step 3.2.1 – Healthy-plot normalisation of all features`));
K.push(...tab2('s321', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Early disease changes are small compared with date, weather, variety and crop-age differences.`],
[`Input`, `Pre-symptomatic features; healthy-plot features of the same date and variety (training replications).`],
[`Output → next step`, `Healthy-normalised features → Activity 3.3.`]], [2200, 7106], `Step 3.2.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Apply Step E2 to every feature: z_{h} = (x − mean_{healthy}) / SD_{healthy}, with the healthy plots of the same date and variety in the training part (rotated healthy plots, ${T('healthyrot')}).`));
K.push(NL(`Apply the same reference to the test samples.`));
K.push(P(`**Supporting studies.** Oerke et al. (2006); Zarco-Tejada et al. (2018); Calderón et al. (2014); Poblete et al. (2023).`));
K.push(H2(`Activity 3.3 – Pre-symptomatic feature selection`));
K.push(H3(`Step 3.3.1 – Selection with the pre-symptomatic labels`));
K.push(...tab2('s331', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Features that respond after symptoms are not necessarily the earliest responders.`],
[`Input`, `Healthy-normalised feature groups (training part).`],
[`Output → next step`, `Pre-symptomatic feature sets of each camera and sensor set → Activity 3.4.`]], [2200, 7106], `Step 3.3.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Start from the pre-symptomatic feature sets of Activity 1.8 and repeat the one-method-per-type selection with the pre-symptomatic labels inside every training fold: SHAP-CARS for bands, ReliefF for indices (two classes) or RReliefF (later score), mRMR for texture, the TTFI search, the redundancy filter and the variance inflation factor.`));
K.push(NL(`Fuse the camera sets for the 15 sensor sets and run sequential floating forward selection for the machine-learning models, limited to 10 features because the training part is smaller.`));
K.push(P(`**Supporting studies.** Tian et al. (2021); Ma et al. (2026); early spectral changes in rusts and mildews: Terentev et al. (2023), Zhu et al. (2017).`));
K.push(H2(`Activity 3.4 – Pre-symptomatic models`));
K.push(H3(`Step 3.4.1 – Models for the 15 sensor sets`));
K.push(...tab2('s341', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Detection must be tested for each camera and combination.`],
[`Input`, `Pre-symptomatic feature sets.`],
[`Output → next step`, `Trained models and test predictions → Activity 3.5.`]], [2200, 7106], `Step 3.4.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Machine learning: support vector machine, random forest, extreme gradient boosting, k-nearest neighbours and partial least squares, with the grids of ${T('mlgrid')}.`));
K.push(NL(`Feature-fusion networks: DNN-F1 and DNN-F2 with smaller layers (32 and 16 units) and stronger dropout (0.4).`));
K.push(NL(`Same folds as Objective 2.`));
K.push(P(`**Supporting studies.** Zhu et al. (2017); Tian et al. (2021); Yu et al. (2025); Srivastava et al. (2014).`));
K.push(H2(`Activity 3.5 – Evaluation, earliest detection day and risk maps`));
K.push(H3(`Step 3.5.1 – Pre-symptomatic metrics, area under the curve (AUC) and earliest detection day`));
K.push(...tab2('s351', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Shows how early, with which sensor set and with what reliability white rust can be predicted.`],
[`Input`, `Test predictions with days after inoculation.`],
[`Output → next step`, `Accuracy tables; earliest detection day of every sensor set.`]], [2200, 7106], `Step 3.5.1 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Classification: sensitivity, specificity, balanced accuracy and AUC; regression: R² and RMSE of the later score.`));
K.push(NL(`Compute balanced accuracy separately for each pre-symptomatic date; the earliest detection day is the first date on which it reaches 0.70 (${F('earliest')}).`));
K.push(NL(`Report the earliest detection day separately for each variety and inoculation timing.`));
K.push(P(`**Supporting studies.** Fawcett (2006); Mahlein et al. (2019); Zarco-Tejada et al. (2018).`));
K.push(...fig2('earliest', 'g23_dummy_earliest.png', `Dummy example of balanced accuracy by days after inoculation and the earliest detection day of each sensor set.`, 460));
K.push(...tab2('earlyex', [[`Pre-symptomatic flight (days after inoculation)`, `1 Jan (2)`, `4 Jan (5)`, `7 Jan (8)`],
[`Hyperspectral + thermal: balanced accuracy (dummy)`, `0.58`, `0.66`, `0.74`],
[`Red–green–blue: balanced accuracy (dummy)`, `0.48`, `0.52`, `0.57`]], [3700, 1868, 1868, 1870], `Worked example (dummy data): the hyperspectral + thermal set reaches 0.70 on 7 January (earliest detection day = 8 days after inoculation), while the red–green–blue set does not reach it before symptoms.`, 17));
K.push(...tab2('croc', [[`Aspect`, `Receiver operating characteristic analysis and earliest detection day`],
[`Principle (how it works)`, `The receiver operating characteristic curve plots sensitivity against 1 − specificity for all thresholds; its area (AUC) is the probability that an infected sample scores higher than a healthy one. The earliest detection day is the first date on which balanced accuracy reaches a set level.`],
[`Problem it solves`, `Measures early-warning ability independently of the class balance and threshold; gives a simple "how early" answer.`],
[`Specification in this study`, `AUC and balanced accuracy per date; level 0.70.`],
[`Hyper-parameters and how they are tuned`, `Level 0.70 (fixed in advance; 0.65 and 0.75 reported as checks).`],
[`Data on which it works well`, `Binary early-warning problems with unequal classes.`],
[`Why it was selected`, `Standard for early detection and comparable with published earliest-detection studies.`],
[`Key references`, `Fawcett (2006); Mahlein et al. (2019)`]], [2300, 7006], `Method card – Receiver operating characteristic analysis and earliest detection day.`, 16));
K.push(H3(`Step 3.5.2 – Risk maps`));
K.push(...tab2('s352', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Early warnings are useful only if they show where to act.`],
[`Input`, `Best pre-symptomatic model; subplot features of each pre-symptomatic date.`],
[`Output → next step`, `Maps of the predicted infection probability of every subplot.`]], [2200, 7106], `Step 3.5.2 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Map the predicted probability of later infection for every subplot and pre-symptomatic date.`));
K.push(NL(`Compare the maps with the later observed severity.`));
K.push(P(`**Supporting studies.** Zarco-Tejada et al. (2018); Yu et al. (2025).`));
K.push(H3(`Step 3.5.3 – Covariate baseline for the pre-symptomatic stage`));
K.push(...tab2('s353', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Before symptoms, infection depends strongly on weather after inoculation and on variety; the cameras must be shown to detect more than these factors.`],
[`Input`, `Covariates (Step A6) of the pre-symptomatic dates; pre-symptomatic models.`],
[`Output → next step`, `Accuracy of the covariate-only model compared with the sensor models → evidence that the early signal comes from the plants.`]], [2200, 7106], `Step 3.5.3 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Fit the best machine-learning model with days after inoculation, variety, inoculation timing, growth stage and the weather summaries only.`));
K.push(NL(`Report the sensor models and the best sensor set + covariates next to it, with the same B1/B2 baselines, bootstrap intervals and real-gain rule as in Step 2.5.5.`));
K.push(P(`**Supporting studies.** Zhang et al. (2014); Chattopadhyay et al. (2011); Zhu et al. (2017).`));
K.push(H3(`Step 3.5.4 – Independent testing of the pre-symptomatic models`));
K.push(...tab2('s354', [[`Item`, `Description`],
[`Purpose (problem it solves)`, `Early-warning models also need an independent test, but pre-symptomatic labels require a flight before symptoms and a later visit of the same quadrats.`],
[`Input`, `Bharatpur quadrats flown before symptoms and scored later (Step A7); a fungicide-protected healthy strip for the healthy-plot normalisation.`],
[`Output → next step`, `Independent test accuracy of the pre-symptomatic models, where the data allow → conclusions on early warning.`]], [2200, 7106], `Step 3.5.4 at a glance.`, 17));
K.push(P(`**Procedure.**`));
K.push(NL(`Apply the frozen pre-symptomatic models (trained on all IARI pre-symptomatic data) to quadrats flown before symptoms and labelled from their later status.`));
K.push(NL(`Use the protected strip as the healthy reference; where no early flight or healthy reference exists, the pre-symptomatic models are evaluated with the internal validation only, and this is stated.`));
K.push(P(`**Supporting studies.** Ma et al. (2026); Zhu et al. (2017); Zarco-Tejada et al. (2018).`));
K.push(H1(`6. Cross-check of the methodology`));
K.push(P(`This chapter checks that no step is missing, that every output is used by a later step, and that the methodology agrees with the feature-selection approach note for multi-sensor UAV data and with the DT-EDNet study (Ma et al., 2026). Where the methodology deliberately differs, the reason is given.`));
K.push(H2(`6.1 Input–output chain of all steps`));
K.push(...tab2('chain', [[`Step(s)`, `Input`, `Output`, `Used by`],
[`A1–A3, A5`, `field design, scores`, `labelled subplot list; post- and pre-symptomatic datasets`, `D8, F1, all objectives`],
[`A4`, `tagged plants, ASD spectroradiometer`, `leaf spectra with leaf grades and metadata`, `separate leaf-level analysis (not part of this document)`],
[`A9`, `glasshouse pots, inoculum`, `pot-level severity (0–6) and leaf spectra under controlled conditions`, `characterisation under controlled conditions (Objective 1)`],
[`A8`, `designated subplots, laboratory and field instruments`, `biochemical and biophysical parameters (48 plots × 4 dates)`, `1.7, 1.8, 3.1.2`],
[`A7`, `Bharatpur research farms and farmers' fields`, `independent test dataset (images, disease index, covariates)`, `2.7, 3.5.4`],
[`A6`, `field book, weather records`, `covariate table (days after inoculation, variety, timing, growth stage, weather)`, `D2, 1.1.3, 2.5.5, 3.5.3`],
[`B1–B2`, `raw images, panels, control points`, `calibrated, georeferenced mosaics`, `B3, B4`],
[`B3`, `hyperspectral cube`, `clean, smoothed 483-band cube`, `B4, C1, D3`],
[`B4–B5`, `mosaics of all cameras`, `aligned layers on the hyperspectral grid`, `C6–C8, D2`],
[`C1–C5`, `pixel samples of all dates`, `labelled endmember library`, `C6`],
[`C6–C8`, `library, cubes, NDVI`, `accepted vegetation mask applied to all cameras`, `D2, D5`],
[`D1–D2`, `masked layers, polygons`, `subplot mean spectra and band values joined with covariates`, `D3–D7`],
[`D3–D7`, `subplot values`, `spectral, index, texture, colour and thermal groups`, `D8, E1`],
[`D8`, `all features`, `feature table of each camera`, `E, F, Objective 1`],
[`E1`, `temperatures`, `normalised thermal features`, `D7, Objective 1`],
[`E2`, `features, healthy plots (rotated across folds)`, `healthy-normalised features`, `Objective 3; thermal difference features`],
[`E3–E4`, `feature tables`, `standardised features; class weights`, `all models`],
[`F1–F3`, `labelled tables`, `outer and inner folds with rotated healthy plots; tuning plan; leakage checklist`, `E2, Objectives 2–3`],
[`1.1.1–1.1.3`, `post-symptomatic features`, `response figures`, `interpretation, 1.6.3`],
[`1.2.1–1.2.4`, `reflectance and first derivative`, `effective ranges; optimal wavelengths`, `1.3, 1.6.2, 2.1.5`],
[`1.3.1–1.3.3`, `NDSI/RSI maps, bands`, `best NDSI, RSI, White Rust Index; multispectral indices`, `1.4.1, 1.6.1`],
[`1.4.1–1.4.3`, `index group`, `selected indices`, `1.6.2, 2.1.5`],
[`1.5.1–1.5.4`, `principal-component texture`, `selected texture features; best TTFI`, `1.6.2, 2.1.5`],
[`1.6.1–1.6.4`, `survivors of all groups`, `disease-specific feature set of each camera`, `2.1.2, 3.3.1`],
[`1.7.1–1.7.6`, `biochemical and biophysical parameters; camera features`, `disease effect by date and stage; parameter–feature links`, `interpretation of Objectives 1–3; 2.5.4`],
[`1.8.1–1.8.5`, `576 pre-symptomatic samples; later status; physiology of 7 January`, `pre-symptomatic response; earliest-responding features; pre-symptomatic feature set`, `3.3.1, 3.1.2`],
[`2.1.1–2.1.5`, `feature sets, folds`, `task labels; fused sets of 15 sensor sets; six hyperspectral configurations`, `2.2, 2.3`],
[`2.2.1–2.2.6`, `optimum feature combinations`, `tuned machine-learning predictions`, `2.4`],
[`2.3.1–2.3.8`, `fused sets; pseudo-images`, `neural-network predictions`, `2.4`],
[`2.4.1–2.4.3`, `predictions`, `metric tables`, `2.5`],
[`2.5.1–2.5.5`, `metric tables, models, covariates`, `best sensor set and model; contributions; ablation; explanation; gain over the covariate baseline`, `2.6, conclusions`],
[`2.6.1–2.6.3`, `best models`, `robustness results; maps`, `conclusions`],
[`2.7.1–2.7.4`, `all IARI data; Bharatpur data`, `frozen final models; independent test accuracy; farm maps`, `conclusions`],
[`3.1.1–3.5.2`, `pre-symptomatic features, later labels`, `pre-symptomatic models; earliest detection day; risk maps`, `conclusions`]], [1300, 2700, 3400, 1906], `Input and output of every step and the step that uses each output.`, 15));
K.push(P(`**Result of the check.** Every output is used by at least one later step, every input is produced by an earlier step, and every label-based step runs inside the training folds (${T('leak')}). No step is missing between the raw images and the three objectives.`));
K.push(H2(`6.2 Agreement with the feature-selection approach note`));
K.push(...tab2('fscheck', [[`Recommendation of the note`, `In this methodology`, `Status`],
[`Do not select from one big pool; select in stages, group by group`, `four stages; one method per feature type (${T('stages')})`, `included`],
[`Stage 0: build groups with physical meaning; red-edge parameters instead of all derivative bands`, `Activity D; red-edge parameters added; second derivative removed`, `included (second derivative removed on request)`],
[`Stage 1: remove near-constant features; keep one per cluster with |r| > 0.95`, `Steps 1.4.2, 1.5.2, 1.6.1; spectral bands go directly to SHAP-CARS, which handles collinearity`, `included (adapted for bands)`],
[`Stage 2: SPA or CARS for spectra; Boruta or RReliefF for indices; mRMR for texture; two-band search on training plots`, `SHAP-CARS for spectra; ReliefF/RReliefF for indices; mRMR for texture; NDSI/RSI and White Rust Index search in the inner folds`, `included (one method per type, as in Ma et al., 2026)`],
[`Stage 3: variance inflation factor below 5 or 10`, `below 10 (5 as a check)`, `included`],
[`Stage 4: final selection by floating forward selection or elastic net`, `sequential floating forward selection for machine learning, at most 15 features (10 for Objective 3)`, `included`],
[`Every label-based step inside the training folds; folds grouped by plot`, `nested, leave-one-replication-out folds grouped by plot`, `included`],
[`Limit the final number of features (about n/10 to n/20)`, `15 features for about 1280 training samples (10 for about 384)`, `included`],
[`Check stability of selection`, `CARS repeated 20 times; selection frequency over folds (Step 2.5.4)`, `included`],
[`Ablation by group and by camera`, `drop-one-camera, six hyperspectral configurations, DT-EDNet module ablation`, `included`],
[`Normalise thermal values against healthy plots or air temperature on each date`, `Steps E1 and E2`, `included`],
[`Outer loop of 5 folds repeated 10 times`, `three leave-one-replication-out folds (replication is the natural block of the design); five seeds for networks`, `adapted`],
[`Compare with decision-level fusion (stacking)`, `not done: the study is limited to feature-level fusion by design`, `not used (scope)`]], [3500, 4200, 1606], `Cross-check against the feature-selection approach note for multi-sensor UAV data.`, 15));
K.push(H2(`6.3 Agreement with the DT-EDNet study (Ma et al., 2026)`));
K.push(...tab2('dtcheck', [[`Step of Ma et al. (2026)`, `In this methodology`, `Difference and reason`],
[`Spectral response by severity level`, `Step 1.1.1`, `same`],
[`NDSI and RSI R² contour maps; effective ranges with R² > 0.5`, `Step 1.2.1`, `whole usable range 400–2400 nm instead of 450–1000 nm (both cameras of the Headwall imager are available)`],
[`Band selection by RFE-SHAP, SAND and SHAP-CARS; SHAP-CARS chosen`, `Steps 1.2.2–1.2.4 (SHAP-CARS only)`, `one method per type, as requested; SHAP-CARS was the best in the study; stability rule added`],
[`Vegetation index selection with Relief (top five)`, `Steps 1.4.2–1.4.3 (ReliefF / RReliefF)`, `ReliefF handles several classes; RReliefF for the score`],
[`Principal components (> 95%) → GLCM texture (8 measures × 3 components) → mRMR (top six)`, `Steps 1.5.1–1.5.3`, `same, plus a label-free redundancy filter`],
[`TTFI from ordered triplets, three formulas; best by correlation`, `Step 1.5.4`, `same`],
[`DT-EDNet: pseudo-2D input, 3 × 3 embedding (128), SE, class token, 1 KTB with CBAM + 4 TTB, 4 heads, dropout 0.03`, `Steps 2.3.3–2.3.4`, `same; regression head added for the severity score`],
[`EfficientNet, ResNet18, ConvNeXt V2 with identical settings`, `Steps 2.3.5–2.3.7`, `same; stems with stride 1 for small inputs`],
[`AdamW 6 × 10⁻⁴, weight decay 10⁻⁵, cosine to 10⁻⁶, 300 epochs, batch 32, label smoothing 0.01, clipping 1.2, early stopping 60, seed 42`, `Step 2.3.8`, `same; five seeds and a small tuning grid; selection on validation plots`],
[`Random 7:3 split with 10% validation; independent-year test`, `leave-one-replication-out folds grouped by plot (Step F1)`, `random splits put subplots of one plot on both sides and inflate accuracy`],
[`Single and combined feature inputs (OW, VI, TF, TTFI; OW + VI, OW + TTFI, OW + VI + TTFI)`, `Step 2.1.5 (six configurations)`, `TTFI alone (one feature) is not given to the networks; it is assessed in Objective 1`],
[`Ablation without SE, without DTG, without both`, `Step 2.5.3`, `same`],
[`Metrics: overall accuracy, kappa, macro recall, macro-F1, per-class scores`, `Step 2.4.1`, `same, plus weighted kappa, AUC and regression metrics`]], [3300, 2500, 3506], `Cross-check against the DT-EDNet study.`, 15));
K.push(H2(`6.4 Changes from the previous version of the methodology`));
K.push(...tab2('changes', [[`Item`, `Previous version`, `This version`, `Reason`],
[`Second derivative`, `used`, `removed`, `noise amplification; user request`],
[`Band selection`, `correlation scalogram + ReliefF`, `NDSI/RSI effective ranges → SHAP-CARS`, `one method per type; best method in Ma et al. (2026)`],
[`Vegetation index selection`, `Boruta`, `ReliefF / RReliefF`, `one method per type; Relief used for indices by Ma et al. (2026)`],
[`Hyperspectral texture`, `not specified for the cube`, `principal-component texture → mRMR → TTFI`, `Guo et al. (2021); Ma et al. (2026)`],
[`Response tests`, `analysis of variance and Tukey test`, `correlation and response curves`, `fewer statistics; simpler presentation`],
[`Deep learning (post-symptomatic)`, `DNN-F1, DNN-F2`, `DNN-F1, DNN-F2 + DT-EDNet, EfficientNet, ResNet18, ConvNeXt V2`, `user request; comparison of Ma et al. (2026)`],
[`Normalisation`, `inside other steps`, `separate Activity E (six steps)`, `clarity; user request`],
[`Endmember extraction`, `one step`, `Activity C with eight steps`, `clarity; user request`],
[`Biochemical and biophysical parameters`, `not included`, `Step A8 and Activity 1.7: 11 parameters on 4 dates with paired comparisons, analysis of variance, growth-stage comparison and parameter–feature correlations`, `user request; physiological basis`],
[`Validation and testing`, `IARI field only`, `internal validation on the IARI field (nested leave-one-replication-out) and independent testing on Bharatpur research farms and farmers' fields with frozen models`, `user request; transferability`],
[`Field calendar (revision 5)`, `sowing at 8-day intervals; inoculation 10 January 2027; flights 12 January – 25 March`, `sowing 19 Nov, 26 Nov, 3 Dec, 10 Dec 2026 (7-day interval); inoculation 30 December 2026 (crop age 41, 34, 27, 20 days); flights 1 January – 15 March 2027; physiology 7 Jan, 18 Jan, 8 Feb, 1 Mar`, `field schedule of the researcher`],
[`Severity label (revision 5)`, `canopy grade of the subplot (0–9)`, `disease index of the subplot from leaves graded at the centre and four corners (Liu et al., 2024); DI classes 0, 1, 3, 5, 7, 9; Task C = DI (%); staghead severity recorded`, `researcher's scoring protocol`],
[`Pre-symptomatic characterisation (revision 5)`, `only in Objective 3 (prediction)`, `Activity 1.8: characterisation of the 576 pre-symptomatic samples per camera in Objective 1`, `user request`],
[`Published indices (revision 5)`, `about 48, partly listed`, `48 indices (39 base + 9 SWIR) and 3 red-edge parameters with formulas, original references and recent disease-sensing studies`, `user request`],
[`Covariate baseline (revision 5)`, `best machine-learning model on covariates`, `interpretable model B1 and machine-learning model B2; M0/M1/M2; gains ΔS, ΔC, ΔT with plot-block bootstrap and DeLong test; real-gain rule; inoculated plots only; no look-ahead`, `leakage-free evaluation of what the cameras add`],
[`Glasshouse experiment (revision 5)`, `not included`, `Step A9: 48-pot experiment with the same varieties and four sowing dates`, `user request; lab and field characterisation`],
[`Leaf spectra`, `not collected`, `ASD leaf spectra of L3, L5 and LL from 3 plants per subplot on every flight date (acquisition only)`, `user request; leaf–canopy link`],
[`Covariates`, `flower %, canopy cover %, vegetation pixel count`, `days after inoculation, variety, inoculation timing, growth stage, weather`, `user request; covariate baseline`],
[`Radiometric consistency between dates; sample quality screening`, `Steps E1 and E4`, `not performed`, `user request; panels on every flight (Step B1)`],
[`Varieties`, `V1 susceptible, V2 moderately susceptible, V3 resistant (assumed)`, `V1 PM 26, V2 Pusa Vijay, V3 PM 37 (no susceptibility assumed)`, `field record`],
[`Technique descriptions`, `short`, `method card for every technique`, `user request`]], [2000, 2300, 2900, 2106], `Main changes in this revision.`, 15));
K.push(H2(`6.5 Drawbacks found and corrected in this version`));
K.push(...tab2('drawbacks', [[`Drawback in the previous version`, `Correction`, `Supporting studies`],
[`Healthy plots were assigned to folds by variety (V1 → fold 1, …), so the training part of each fold had no healthy plots of the test variety. Healthy-plot normalisation with the same variety was then impossible, and healthy samples of the test variety were never seen in training.`, `Healthy plots rotated across folds: every fold has each inoculation timing once and every variety at least once (${T('healthyrot')}).`, `Roberts et al. (2017); Oerke et al. (2006); Zarco-Tejada et al. (2018)`],
[`Severity rises with time and stage, so a model could appear accurate by learning days after inoculation or growth stage instead of disease.`, `Covariate-only baseline and sensor + covariate models (Steps 2.5.5 and 3.5.3); results by growth stage.`, `Zhang et al. (2014); Blasch et al. (2023); Kuhn and Johnson (2013)`],
[`Flowering effects were checked with flower %, which mixes flowers with disease-related colour changes.`, `Growth stage recorded with the BBCH scale; responses and results reported for each stage.`, `Lancashire et al. (1991); Meier (2018); Sulik and Long (2016)`],
[`Pooled reflectance and first-derivative bands in CARS without standardisation would favour one form for numerical reasons; the effective ranges could miss the red edge.`, `Bands standardised before PLS; red-edge first derivative always kept; bands labelled R_{λ} or FD_{λ}.`, `Li et al. (2009); Mehmood et al. (2012); Filella and Peñuelas (1994); Yu et al. (2021)`],
[`Multi-camera pseudo-images could split a small camera group (thermal) across rows.`, `Each camera starts on a new row of the pseudo-image.`, `Sharma et al. (2019); Ma et al. (2026)`],
[`Tuning every network for every case needed about 34 000 runs.`, `Tune once (fold 1, S15, Task B, one seed) and reuse the settings: about 3800 runs.`, `Ma et al. (2026); Cawley and Talbot (2010)`],
[`Weather has one value per date and cannot be separated from the date in one season.`, `Weather used for interpretation and in covariate models labelled "within-season".`, `Zhang et al. (2014); Chattopadhyay et al. (2011)`],
[`A variety was assumed to be resistant without field evidence.`, `Variety names from the field record; transfer test run for each variety in turn.`, `Blasch et al. (2023)`],
[`The healthy plots lie in a separate block, so healthy vs inoculated differences can include a small block (location) effect.`, `Detection labels come from the observed score, so inoculated subplots with no pustules are also healthy samples; detection accuracy is reported separately for healthy-block samples and for symptom-free inoculated subplots; healthy-plot normalisation is done by date.`, `Roberts et al. (2017); Oerke et al. (2006)`],
[`All results came from one site and one season.`, `Independent testing with frozen models on research-farm and farmers' field data at Bharatpur (Activity 2.7); leave-one-variety-out and leave-one-timing-out tests kept as internal transfer tests; transfer to other seasons still to be tested.`, `Ma et al. (2026); Roberts et al. (2017); Ploton et al. (2020)`]], [3500, 3500, 2306], `Drawbacks of the previous version and how they are corrected.`, 15));
K.push(H1(`7. Definitions of indices and features`));
K.push(P(`R_{λ} is the reflectance at λ nm (nearest available band). The 48 published hyperspectral indices are the 39 base indices of ${T('hsidx')} and the 9 SWIR disease indices of ${T('hsidx2')}; formulas were checked against the original papers, and the original reference of every index is kept. Indices that need a band removed in quality control (Step B3) are computed only if the band passes the noise check.`));
K.push(...tab2('hsidx', [[`Group`, `Index`, `Formula`, `Original reference`],
[`Greenness and canopy structure (17)`, `NDVI780`, `(R_{780} − R_{670})/(R_{780} + R_{670})`, `Raun et al. 2001`],
[``, `NDVI850`, `(R_{850} − R_{650})/(R_{850} + R_{650})`, `Raun et al. 2001`],
[``, `NDVI761`, `(R_{761} − R_{651})/(R_{761} + R_{651})`, `Raun et al. 2001`],
[``, `SR900`, `R_{900}/R_{680}`, `Jordan 1969`],
[``, `SR850`, `R_{850}/R_{680}`, `Jordan 1969`],
[``, `SR761`, `R_{761}/R_{651}`, `Jordan 1969`],
[``, `GNDVI`, `(R_{850} − R_{550})/(R_{850} + R_{550})`, `Gitelson et al. 1996`],
[``, `RDVI`, `(R_{800} − R_{670})/√(R_{800} + R_{670})`, `Roujean and Bréon 1995`],
[``, `MSR`, `(R_{800}/R_{670} − 1)/√(R_{800}/R_{670} + 1)`, `Chen 1996`],
[``, `TVI`, `0.5[120(R_{750} − R_{550}) − 200(R_{670} − R_{550})]`, `Broge and Leblanc 2001`],
[``, `MTVI1`, `1.2[1.2(R_{800} − R_{550}) − 2.5(R_{670} − R_{550})]`, `Haboudane et al. 2004`],
[``, `MTVI2`, `1.5[1.2(R_{800} − R_{550}) − 2.5(R_{670} − R_{550})] / √[(2R_{800} + 1)^{2} − (6R_{800} − 5√R_{670}) − 0.5]`, `Haboudane et al. 2004`],
[``, `MCARI1`, `1.2[2.5(R_{800} − R_{670}) − 1.3(R_{800} − R_{550})]`, `Haboudane et al. 2004`],
[``, `TCARI`, `3[(R_{700} − R_{670}) − 0.2(R_{700} − R_{550})(R_{700}/R_{670})]`, `Haboudane et al. 2002`],
[``, `VIgreen`, `(R_{550} − R_{670})/(R_{550} + R_{670})`, `Gitelson et al. 2002`],
[``, `GI`, `R_{554}/R_{677}`, `Guo et al. 2021`],
[``, `RR`, `1/R_{700}`, `Mustafa et al. 2023`],
[`Pigment ratios (12)`, `PSSRa; PSSRb; PSSRc`, `R_{800}/R_{680};  R_{800}/R_{635};  R_{800}/R_{470}`, `Blackburn 1998`],
[``, `RARSa; RARSb; RARSc`, `R_{675}/R_{700};  R_{675}/(R_{700} × R_{650});  R_{760}/R_{500}`, `Chappelle et al. 1992`],
[``, `SIPI`, `(R_{800} − R_{445})/(R_{800} − R_{680})`, `Peñuelas et al. 1995`],
[``, `NPCI`, `(R_{680} − R_{430})/(R_{680} + R_{430})`, `Peñuelas et al. 1994`],
[``, `PSRI`, `(R_{680} − R_{500})/R_{750}`, `Merzlyak et al. 1999`],
[``, `ARI`, `1/R_{550} − 1/R_{700}`, `Gitelson et al. 2001`],
[``, `PPR`, `(R_{550} − R_{450})/(R_{550} + R_{450})`, `Metternicht 2003`],
[``, `NRI`, `(R_{570} − R_{670})/(R_{570} + R_{670})`, `Bausch and Duke 1996`],
[`Photosynthesis and stress (4)`, `PRI`, `(R_{531} − R_{570})/(R_{531} + R_{570})`, `Gamon et al. 1992`],
[``, `NPQI`, `(R_{415} − R_{435})/(R_{415} + R_{435})`, `Barnes et al. 1992`],
[``, `RVSI`, `(R_{712} + R_{752})/2 − R_{732}`, `Merton and Huntington 1999`],
[``, `HI (healthy index)`, `(R_{534} − R_{698})/(R_{534} + R_{698}) − 0.5 R_{704}`, `Mahlein et al. 2013`],
[`Water (3)`, `WI`, `R_{900}/R_{970}`, `Peñuelas et al. 1997`],
[``, `WI/NDVI`, `(R_{900}/R_{970})/NDVI`, `Peñuelas et al. 1997`],
[``, `NWI-2`, `(R_{970} − R_{850})/(R_{970} + R_{850})`, `Babar et al. 2006`],
[`SWIR disease–water (3 base)`, `DWSI-1`, `R_{800}/R_{1660}`, `Apan et al. 2004`],
[``, `DWSI-4`, `R_{550}/R_{680}`, `Apan et al. 2004`],
[``, `ROTI`, `R_{1175}/(R_{1982} + R_{691})`, `Bhattacharya and Chattopadhyay 2013`]], [1900, 1700, 3906, 1800], `The 39 base hyperspectral indices with formulas and original references. Disease-sensing studies of the last 20 years (2006–2026) that used these index groups: Zhang et al. (2012b), Mahlein et al. (2013), Ashourloo et al. (2014), Guo et al. (2021), Mustafa et al. (2023).`, 15));
K.push(...tab2('hsidx2', [[`Group`, `Index`, `Formula`, `Original reference`],
[`SWIR disease indices (9)`, `DWSI-2; DWSI-3`, `R_{1660}/R_{550};  R_{1660}/R_{680}`, `Apan et al. 2004`],
[``, `DWSI-5`, `(R_{800} + R_{550})/(R_{1660} + R_{680})`, `Apan et al. 2004`],
[``, `NDWI`, `(R_{860} − R_{1240})/(R_{860} + R_{1240})`, `Gao 1996`],
[``, `Moisture stress index (MSI)`, `R_{1600}/R_{820}`, `Hunt and Rock 1989`],
[``, `NDII`, `(R_{819} − R_{1649})/(R_{819} + R_{1649})`, `Hardisky et al. 1983`],
[``, `RBI_{M}; NDBI`, `R_{1148}/R_{1301};  (R_{1148} − R_{1301})/(R_{1148} + R_{1301})`, `Mandal et al. 2023`],
[``, `RBI_{R}`, `R_{1068}/R_{1560}`, `Ramalingam et al. 2026`],
[`Red-edge parameters (3; 680–760 nm)`, `REP`, `wavelength of the maximum first derivative`, `Horler et al. 1983; Cho and Skidmore 2006`],
[``, `D_{r}`, `maximum first derivative (red-edge amplitude)`, `Filella and Peñuelas 1994`],
[``, `SD_{r}`, `sum of the first derivative over 680–760 nm (area)`, `Filella and Peñuelas 1994`],
[`Data-driven (Activity 1.3)`, `NDSI, RSI, WRI`, `best pair NDSI(λ_{1}, λ_{2}), RSI(λ_{1}, λ_{2}); WRI = NDSI(λ_{1}, λ_{2}) + w R_{λ3}`, `Ma et al. 2026; Mahlein et al. 2013 (method)`]], [1900, 1700, 3906, 1800], `The 9 SWIR disease indices (completing the 48 published indices), the 3 red-edge parameters and the data-driven indices. Disease-sensing studies of the last 20 years that used these index groups: Bhattacharya and Chattopadhyay (2013), Zarco-Tejada et al. (2018), Yu et al. (2018), Mandal et al. (2023), Ramalingam et al. (2026).`, 15));
K.push(...tab2('msidx', [[`Feature`, `Formula (B, G, R, RE, NIR = 475, 560, 668, 717, 840 nm)`, `Reference`],
[`Band reflectance (5)`, `subplot mean reflectance of B, G, R, RE, NIR`, `Liu et al. 2024`],
[`NDVI`, `(NIR − R)/(NIR + R)`, `Rouse et al. 1974`],
[`GNDVI`, `(NIR − G)/(NIR + G)`, `Gitelson et al. 1996`],
[`NDRE`, `(NIR − RE)/(NIR + RE)`, `Gitelson and Merzlyak 1994`],
[`CI_{green}`, `NIR/G − 1`, `Gitelson et al. 2003`],
[`CI_{rededge}`, `NIR/RE − 1`, `Gitelson et al. 2003`],
[`MTCI`, `(NIR − RE)/(RE − R)`, `Dash and Curran 2004`],
[`OSAVI`, `1.16(NIR − R)/(NIR + R + 0.16)`, `Rondeaux et al. 1996`],
[`SAVI`, `1.5(NIR − R)/(NIR + R + 0.5)`, `Huete 1988`],
[`TCARI`, `3[(RE − R) − 0.2(RE − G)(RE/R)]`, `Haboudane et al. 2002`],
[`MCARI`, `[(RE − R) − 0.2(RE − G)](RE/R)`, `Daughtry et al. 2000`],
[`MSR`, `(NIR/R − 1)/√(NIR/R + 1)`, `Chen 1996`],
[`PSRI`, `(R − G)/NIR`, `Merzlyak et al. 1999`],
[`Normalised differences (10)`, `(B_{i} − B_{j})/(B_{i} + B_{j}) for all band pairs`, `Ma et al. 2026`],
[`Texture (40)`, `8 GLCM measures (${T('rgbfeat')}) of each of the 5 bands`, `Haralick et al. 1973; Liu et al. 2024`]], [2200, 4800, 2306], `Multispectral features.`, 15));
K.push(...tab2('rgbfeat', [[`Feature`, `Equation`, `Reference`],
[`Chromatic coordinates`, `r = R/(R+G+B), g = G/(R+G+B), b = B/(R+G+B)`, `Woebbecke et al. 1995`],
[`Excess green (ExG)`, `2g − r − b`, `Woebbecke et al. 1995`],
[`Excess red (ExR)`, `1.4r − g`, `Meyer and Neto 2008`],
[`ExG − ExR`, `ExG − ExR`, `Meyer and Neto 2008`],
[`VARI`, `(G − R)/(G + R − B)`, `Gitelson et al. 2002`],
[`GLI`, `(2G − R − B)/(2G + R + B)`, `Louhaichi et al. 2001`],
[`NGRDI`, `(G − R)/(G + R)`, `Tucker 1979`],
[`Hue, saturation, value (3)`, `mean of vegetation pixels`, `—`],
[`Mean (MEA)`, `Σ_{i} Σ_{j} i P(i, j)`, `Haralick et al. 1973`],
[`Variance (VAR)`, `Σ_{i} Σ_{j} (i − μ)^{2} P(i, j)`, `Haralick et al. 1973`],
[`Homogeneity (HOM)`, `Σ_{i} Σ_{j} P(i, j) / [1 + (i − j)^{2}]`, `Haralick et al. 1973`],
[`Contrast (CON)`, `Σ_{i} Σ_{j} (i − j)^{2} P(i, j)`, `Haralick et al. 1973`],
[`Dissimilarity (DIS)`, `Σ_{i} Σ_{j} |i − j| P(i, j)`, `Haralick et al. 1973`],
[`Entropy (ENT)`, `− Σ_{i} Σ_{j} P(i, j) ln P(i, j)`, `Haralick et al. 1973`],
[`Second moment (SEC)`, `Σ_{i} Σ_{j} P(i, j)^{2}`, `Haralick et al. 1973`],
[`Correlation (COR)`, `Σ_{i} Σ_{j} (i − μ_{i})(j − μ_{j}) P(i, j) / (σ_{i} σ_{j})`, `Haralick et al. 1973`]], [2300, 4700, 2306], `Colour indices and grey-level co-occurrence matrix (GLCM) texture measures. P(i, j) is the normalised frequency of grey levels i and j in neighbouring pixels.`, 15));
K.push(...tab2('tirfeat', [[`Feature`, `Definition`, `Reference`],
[`Canopy temperature statistics (5)`, `mean, median, standard deviation, 10th and 90th percentile of vegetation-pixel temperature`, `Liu et al. 2024`],
[`Canopy minus air temperature (CTD)`, `T_{c} − T_{air}`, `Calderón et al. 2014`],
[`Normalised relative canopy temperature (NRCT)`, `(T_{c} − T_{min})/(T_{max} − T_{min}) over the field on that date`, `Elsayed et al. 2017`],
[`Difference from healthy plots (ΔT)`, `T_{c} − mean T_{c} of the healthy plots of the same date and variety`, `Oerke et al. 2006`],
[`Crop water stress index (CWSI)`, `(T_{c} − T_{wet})/(T_{dry} − T_{wet})`, `Idso et al. 1981; Jones et al. 2009`],
[`Thermal texture (8)`, `GLCM measures of the temperature image quantised over one common range`, `Haralick et al. 1973`]], [2800, 4300, 2206], `Thermal features.`, 15));
K.push(H1(`8. Six-month work plan`));
K.push(...fig2('gantt', 'g24_gantt.png', `Six-month work plan for the analysis.`, 540));
K.push(...tab2('plan', [[`Month`, `Work`, `Deliverable`],
[`1`, `Common Activities A–C for all dates and cameras; mask accuracy`, `calibrated, masked images; endmember library`],
[`2`, `Activities D–F: features, covariates, normalisation, folds; Activity 1.1`, `feature and covariate tables; response curves`],
[`3`, `Activities 1.2–1.8; selection code tested inside folds; pre-symptomatic characterisation; analysis of the biochemical and biophysical parameters`, `optimal wavelengths, White Rust Index, selected indices, TTFI; pre-symptomatic feature set; Objective 1 draft`],
[`4`, `Objective 2: machine learning and feature-fusion networks for 15 sensor sets`, `results of 15 sensor sets`],
[`5`, `Objective 2: DT-EDNet and comparison networks; ablation; Shapley explanation; maps`, `network comparison; ablation; maps`],
[`6`, `Objective 3; independent testing at Bharatpur (Activity 2.7); glasshouse data; synthesis and writing`, `earliest detection day; risk maps; independent test results; thesis chapters`]], [1000, 5000, 3306], `Month-wise plan.`, 17));
K.push(NOTE(`Computing load: 15 sensor sets × 3 tasks × 3 folds × 5 machine-learning models with floating forward selection; two feature-fusion networks and four pseudo-image networks × 5 seeds. Run the selection of each camera once per fold and reuse it for all combinations, and train the networks on a graphics processing unit.`));
K.push(H1(`9. Software and reproducibility`));
K.push(...tab2('software', [[`Task`, `Software`],
[`Image processing, registration, resampling, masks`, `ENVI or Python (GDAL, rasterio); hourglass notebook (minimum noise fraction, pixel purity index, n-dimensional visualisation, spectral angle mapper)`],
[`Features, selection, machine learning`, `Python: numpy, pandas, scikit-learn (Pedregosa et al., 2011), xgboost (Chen and Guestrin, 2016), shap (Lundberg and Lee, 2017), ReliefF, mRMR, mlxtend floating selection (Raschka, 2018)`],
[`Deep learning`, `PyTorch (Paszke et al., 2019)`]], [3300, 6006], `Software used.`, 17));
K.push(BL(`Fix random seeds; store the outer and inner folds as files and reuse them for all sensor sets and models.`));
K.push(BL(`Log every setting (bands removed, mask threshold, selected features per fold, hyper-parameters, seeds).`));
K.push(BL(`Keep raw, intermediate and final tables separate and versioned.`));
K.push(H1(`10. Questions expected in the interview`));
K.push(P(`**Q. Why one feature-selection method for each type of feature?** Each type has a different nature: spectral bands are many and collinear (SHAP-CARS is designed for this), indices are fewer but must separate overlapping classes (ReliefF), and texture features are correlated with each other (mRMR balances relevance and redundancy). One method per type keeps the procedure simple and follows Ma et al. (2026).`));
K.push(P(`**Q. Why is the second derivative not used?** Derivatives amplify noise; at UAV signal-to-noise levels the second derivative adds hundreds of unstable variables (Rinnan et al., 2009). The red-edge parameters from the first derivative keep the useful information (Yu et al., 2021).`));
K.push(P(`**Q. Why are texture features computed on principal components?** Texture of 483 bands would be highly redundant; the first three components keep more than 95% of the variance, as in Guo et al. (2021) and Ma et al. (2026).`));
K.push(P(`**Q. What is the Tri-band Texture Fusion Index?** A combination of three selected texture features in sums, products and ratios; in rice blast it was more strongly related to disease than any single texture feature (Ma et al., 2026).`));
K.push(P(`**Q. Why compare DT-EDNet with EfficientNet, ResNet18 and ConvNeXt V2?** These were the comparison networks of the DT-EDNet study; repeating the comparison under plot-grouped validation shows whether its advantage holds for white rust when accuracy is not inflated by random splits.`));
K.push(P(`**Q. Is the dataset large enough for a transformer?** About 1280 training samples per fold is small for a transformer, which is why identical folds, early stopping, a small tuning grid, five seeds and strong machine-learning baselines are used; the pseudo-image networks are not used for the smaller pre-symptomatic dataset.`));
K.push(P(`**Q. Why are the folds grouped by replication?** Subplots of a plot and plots of a replication are similar; random splits put near-identical samples in training and test data and inflate accuracy (Roberts et al., 2017; Ploton et al., 2020).`));
K.push(P(`**Q. Why are flowers kept in the subplot spectrum?** The disease survey includes the inflorescence and staghead; the growth stage (vegetative, flowering, pod formation) is recorded with the BBCH scale and results are reported for each stage, so that selected features are not only flowering effects (Sulik and Long, 2016; Meier, 2018).`));
K.push(P(`**Q. How are weather and other covariates used?** Days after inoculation, variety, inoculation timing, growth stage and weather form a covariate-only baseline; a camera is useful only if it beats this baseline. Weather has one value per date, so models that contain it are labelled within-season (Zhang et al., 2014; Chattopadhyay et al., 2011).`));
K.push(P(`**Q. How is pre-symptomatic infection known if no symptoms are visible?** From the later status of the same subplot; inoculated subplots that never develop symptoms are excluded (Zhu et al., 2017; Tian et al., 2021). The same labels are used to characterise the pre-symptomatic response in Activity 1.8 and to build the prediction models of Objective 3.`));
K.push(P(`**Q. How is severity measured?** Leaves at the centre and four corners of each subplot are graded 0–9 and combined into the disease index DI = Σ(x × f) / (9 × Σf) × 100 (Liu et al., 2024); DI = 0 gives the healthy label, the DI range gives the class (0, 1, 3, 5, 7, 9) and the DI itself is the regression target.`));
K.push(P(`**Q. What do the covariate models show?** An interpretable model (logistic, ordinal logistic or linear) and the best machine-learning model are fitted on covariates only; the cameras are credited only with their gain over the stronger of the two, tested with a plot-block bootstrap and the DeLong test (Efron and Tibshirani, 1993; DeLong et al., 1988).`));
K.push(P(`**Q. Why are the biochemical and biophysical parameters measured at plot level?** The plot is the experimental unit of the randomised block design (Hurlbert, 1984). One designated subplot per plot keeps the gas-exchange readings inside the mid-morning window and links each sample to the UAV features of that subplot; the parameters explain the camera responses and are not model inputs (Calderón et al., 2013).`));
K.push(P(`**Q. How do you know the models work outside the IARI field?** The models are validated by leave-one-replication-out inside the IARI field, where they are chosen and assessed; then the frozen final models are tested once on independent research-farm and farmers' field data from Bharatpur with natural infection (independent testing, not validation), as the DT-EDNet study did with an independent naturally infected dataset (Ma et al., 2026; Ploton et al., 2020).`));
K.push(P(`**Q. How can these results be used with satellite data?** The selected wavelengths and indices can be simulated for Sentinel-2 or LISS-IV bands from the hyperspectral spectra, as done for yellow rust and rice bacterial leaf blight (Zheng et al., 2018; Das et al., 2015).`));