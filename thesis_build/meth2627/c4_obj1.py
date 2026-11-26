from c_lib import *


def add():
    h1('6. Objective 1 – Characterisation of white rust through multimodal unmanned aerial vehicle sensing')
    p('Objective 1 describes how each camera sees white rust and selects the features that carry the disease signal. Post-symptomatic description uses all 1920 subplot-dates of each camera with the DI as target (Activities 1.1–1.7); '
      'the pre-symptomatic stage uses the 576 subplot-dates with later-infected vs healthy as target (Activity 1.8). For the models (Objectives 2 and 3) the same selection steps are repeated on the 33 training plots only (Step 2.2).')
    myfig('chain', 'g10_selection_chain.png', 'Feature-selection chain of Objective 1: one selection method per feature type, then the variance inflation factor gives the disease-specific feature set (DSF) of each camera.')
    P = 'Objective 1'

    h2('Activity 1.1 – Response analysis')
    step('1.1.1', 'Mean spectra and curves by disease index class', part=P,
         what='Mean ± SD reflectance and first derivative of each DI class, and the % difference of each class from class 0, for the HS camera; class means of every MS, RGB and thermal feature.',
         why='The first, model-free evidence of where and in which direction white rust changes the signal; it guides the reading of every selected feature.',
         do=['Group the subplot-dates by DI class (0, 1, 3, 5, 7, 9).', 'Plot mean ± SD reflectance and first derivative; plot (class − class 0)/class 0 × 100.', 'Tabulate class means of the MS, RGB and thermal features.'],
         check=['Curves drawn for every class with at least 5% of the samples.'],
         out='Response curves → interpretation of 1.2–1.6.',
         papers=[('Ma et al. (2026)', 'Rice blast; mean canopy spectra of each severity level after smoothing; the red edge (680–800 nm) and near-infrared separated the levels best.', 'Mean spectra by severity class from UAV hyperspectral data.'),
                 ('Mahlein et al. (2013)', 'Sugar-beet diseases; spectral signatures of each disease and severity.', 'Class-wise spectral signatures.'),
                 ('Guo et al. (2021)', 'Wheat yellow rust; canopy spectra of plots with different disease index.', 'Canopy spectra by severity from a UAV.'),
                 ('Mandal et al. (2023)', 'Rice blast; mean and SD spectra of each severity level and difference from healthy plants.', 'Mean ± SD and difference from class 0.'),
                 ('Bohnenkamp et al. (2021)', 'Wheat foliar diseases; hyperspectral library from infection to symptoms with spectral turning points confirmed by histology.', 'Spectral signatures described stage by stage and class by class.')])
    myfig('specdemo', 'g07_spectra_demo.png', 'Demo of the outputs of Step 1.1.1 (simulated spectra): (a) mean reflectance by DI class, (b) % difference from class 0, (c) first derivative at the red edge.')
    step('1.1.2', 'Correlation of each feature with the disease index', part=P,
         what='Pearson r between the DI and every band, derivative band and feature of every camera.',
         why='Shows the strength and sign of the relation at every wavelength and for every feature.',
         do=['Compute r with the DI for all features of all cameras (all 1920 samples).', 'Plot r against wavelength for R and FD; list the 10 strongest features of each camera.'],
         check=['Correlation curves and top-10 tables for the four cameras.'],
         out='Correlation curves → interpretation.',
         papers=[('Zhang et al. (2012)', 'Wheat powdery mildew; correlation of each spectral feature with the disease index, ranked by R².', 'Univariate correlation of every feature with the DI.'),
                 ('Ma et al. (2026)', 'Rice blast; correlation of vegetation indices and texture features with severity.', 'Correlation of indices and texture with severity.'),
                 ('Guo et al. (2021)', 'Wheat yellow rust; correlation of indices and texture with the disease index.', 'Same analysis on UAV features.')])
    step('1.1.3', 'Response by variety, sowing date, growth stage, days after inoculation and weather', part=P,
         what='Mean DI and the class curves of 1.1.1 are shown separately by variety, sowing date, growth stage and DAI; DI is plotted against the favourable-day counts.',
         why='Growth stage (especially flowering) and date change the canopy signal independently of disease; the disease signal must hold within each stratum.',
         do=['Table of mean DI by variety × sowing date × date.', 'Class curves within each growth stage (vegetative, flowering, pod formation).', 'DI against favourable days (Step A6).'],
         check=['Every stratum has a table row.'],
         out='Strata → 2.10.',
         papers=[('Blasch et al. (2023)', 'Wheat rusts; UAV detection depended on the crop growth stage.', 'Results by growth stage.'),
                 ('Liu et al. (2024)', 'Wheat powdery mildew; spectral, texture and canopy-temperature features compared between healthy and infected plots at early, middle and late infection stages (Zadoks stage recorded).', 'Responses reported by stage.'),
                 ('Chattopadhyay et al. (2011)', 'White rust of mustard; disease development related to weather in different sowings.', 'DI related to weather and sowing date.'),
                 ('Zhang et al. (2022)', 'Rice leaf blast severity classified separately at the jointing, booting and heading stages.', 'Results reported within each growth stage.')])

    h2('Activity 1.2 – Optimal wavelengths by Shapley additive explanations and competitive adaptive reweighted sampling')
    step('1.2.1', 'Effective wavelength ranges from normalised difference spectral index and ratio spectral index maps', part=P,
         what='For every pair of HS bands, NDSI = (R_{i} − R_{j})/(R_{i} + R_{j}) and RSI = R_{i}/R_{j} are computed and their R² with the DI drawn as maps; bands in pairs with R² > 0.5 for both indices are the effective ranges.',
         why='The maps show which band combinations follow the disease and restrict SHAP-CARS to informative regions.',
         do=['Use the 483 HS bands with reduced sampling (every 2nd band).', 'Compute R² of NDSI and RSI with the DI for every pair; draw the two maps.',
             'Effective ranges = bands taking part in pairs with R² > 0.5 in both maps; if no pair reaches 0.5, use the pairs in the top 5% of R².'],
         settings=['about 29 000 band pairs per index.'],
         check=['Both maps drawn; effective ranges written in nm.'],
         out='Effective ranges → 1.2.2; best NDSI and RSI pairs → 1.3.1.',
         papers=[('Ma et al. (2026)', 'Rice blast; R² contour maps of NDSI and RSI with severity (450–1000 nm, reduced sampling); effective ranges were the regions where R² of both indices exceeded 0.5 (455–503, 520–661 and 702–1000 nm).', 'Same maps, indices and 0.5 threshold.'),
                 ('Tian et al. (2021)', 'Rice leaf blast; kept the top 5% of features by separability when choosing disease-sensitive features.', 'Top-5% fall-back if no pair reaches 0.5.'),
                 ('Huang et al. (2014)', 'Winter wheat diseases; optimised two-band indices from exhaustive band combinations.', 'Exhaustive two-band search.')])
    myfig('ndsidemo', 'g08_ndsi_demo.png', 'Demo of Step 1.2.1 (simulated): NDSI R² map with the R² = 0.5 contour that marks the effective ranges.', width=360)
    step('1.2.2', 'Optimal wavelengths by Shapley additive explanations and competitive adaptive reweighted sampling', part=P,
         what='Candidates are the R and FD bands inside the effective ranges. (1) A random forest predicts the DI and the bands are ranked by mean |SHAP|; the top-ranked bands are kept. (2) Monte Carlo cross-validation chooses the number of PLS components. (3) CARS eliminates redundant bands; the subset with the best cross-validated performance gives the optimal wavelengths (OW).',
         why='Hundreds of correlated bands cannot be given directly to a model; SHAP removes uninformative bands, then CARS removes redundant ones.',
         do=['Standardise the candidate bands.', 'Random forest regression of the DI (500 trees); mean |SHAP| per band (TreeSHAP); keep the top 40%.', 'MCCV (50 random 80/20 divisions by plot) chooses the PLS components (1–15).',
             'CARS: 50 iterations of PLS-weighted, exponentially decreasing band subsets with adaptive reweighted sampling; keep the subset with the lowest GroupKFold(3) RMSE.', 'Label the bands R_{λ} or FD_{λ}.'],
         settings=['Random forest 500 trees, seed 42; CARS 50 iterations; MCCV 50 divisions.'],
         check=['OW list of about 10–15 bands with wavelength and type.'],
         out='OW → 1.6.2, 2.6 (configurations).',
         papers=[('Ma et al. (2026)', 'Rice blast; SHAP-CARS – an ensemble model ranked the bands by mean |SHAP|, MCCV chose the PLS components, CARS eliminated redundant variables over many iterations, and the subset was fixed by validation performance; 12 key wavelengths were kept.', 'The three stages in the same order.'),
                 ('Tian et al. (2021)', 'Rice leaf blast; disease-sensitive bands selected from leaf spectra before model building.', 'Band selection before the models.')])
    myfig('shapdemo', 'g09_shapcars_demo.png', 'Demo of Step 1.2.2 (simulated): (a) SHAP ranking and the top 40% kept; (b) bands kept by CARS.')

    h2('Activity 1.3 – Spectral index construction')
    step('1.3.1', 'Best normalised difference spectral index and ratio spectral index', part=P,
         what='The NDSI and RSI pairs with the highest R² in the maps (bands at least 10 nm apart) are added as indices.',
         why='The best two-band indices are simple, data-driven white rust indices.',
         do=['Pick the highest-R² NDSI and RSI pairs from Step 1.2.1.', 'Compute them at full spectral resolution for all samples.'],
         check=['Two indices with their band positions.'],
         out='NDSI_best, RSI_best → 1.4.',
         papers=[('Ma et al. (2026)', 'Rice blast; best NDSI and RSI from the band-pair maps.', 'Same indices.'),
                 ('Mandal et al. (2023)', 'Rice blast; new indices RBI = R1148/R1301 and NDBI from the best two-band combination.', 'Best two-band combination as a new index.')])
    step('1.3.2', 'White Rust Index', part=P,
         what='A three-band index WRI = NDSI(λ_{1}, λ_{2}) + w × R_{λ3} is searched.',
         why='A third band can correct an effect that a two-band index cannot; the index is specific to white rust and can be carried to cheaper sensors.',
         do=['Bands at 6-nm steps inside the effective ranges; λ_{1} and λ_{2} at least 50 nm apart; w ∈ {−1, −0.5, 0, 0.5, 1}.', 'Score each candidate by |r| with the DI and by the balanced accuracy of healthy vs diseased (single threshold).', 'Keep the best formula; repeat once with SWIR bands and keep the better one.'],
         check=['WRI formula with λ_{1}, λ_{2}, λ_{3} and w.'],
         out='WRI → 1.4, Objectives 2–3, L9.',
         papers=[('Mahlein et al. (2013)', 'Sugar-beet diseases; spectral disease indices built as a normalised difference of two wavelengths plus or minus a third; selected wavelengths at least 50 nm apart.', 'Same form and 50-nm rule.'),
                 ('Zheng et al. (2018)', 'Wheat yellow rust; a new three-band index for Sentinel-2.', 'Three-band disease index.'),
                 ('Liu et al. (2026)', 'Wheat powdery mildew; a specific vegetation index developed on the ground and used from UAV.', 'A disease-specific index for field use.')])
    demo('wri', [['Rank', 'λ1 (nm)', 'λ2 (nm)', 'λ3 (nm)', 'w', '|r| with DI', 'Balanced accuracy'], ['1', '754', '700', '532', '−0.5', '0.71', '0.83'], ['2', '760', '694', '550', '−0.5', '0.70', '0.82'], ['3', '790', '718', '—', '0', '0.68', '0.80']],
         'WRI search output', widths=[900, 1300, 1300, 1300, 900, 1700, 2200])
    step('1.3.3', 'Two-band indices of the multispectral camera', part=P,
         what='The 10 normalised differences of the five MS bands are compared, and the best is added to the MS group.',
         why='Gives the cheaper camera its own data-driven index.',
         do=['Compute (B_{i} − B_{j})/(B_{i} + B_{j}) for all 10 pairs; r with the DI.', 'Add the best pair as MS_NDbest.'],
         check=['Ten r values tabulated.'],
         out='MS_NDbest → 1.6.1.',
         papers=[('Ma et al. (2026)', 'Rice blast; normalised difference indices from band pairs.', 'Same index form.'),
                 ('Liu et al. (2024)', 'Wheat powdery mildew; red-edge multispectral indices for severity.', 'MS two-band indices.')])

    h2('Activity 1.4 – Vegetation index selection')
    step('1.4.1', 'Redundancy filter of the indices', part=P,
         what='Among the 48 published indices, 3 red-edge parameters, NDSI_best, RSI_best and WRI, indices correlated at |r| ≥ 0.95 form clusters; from each cluster the index most correlated with the DI is kept.',
         why='Many indices are near-copies (NDVI family, simple ratios); ReliefF ranks are unreliable among near-identical features.',
         do=['Correlation matrix of all indices.', 'Cluster indices with |r| ≥ 0.95; keep the one with the highest |r| with the DI.'],
         check=['List of kept and removed indices.'],
         out='Non-redundant indices → 1.4.2.',
         papers=[('Ma et al. (2026)', 'Rice blast; correlation analysis among vegetation indices showed that PSSRb, SR, RNDVI and FRI3 were strongly correlated (redundant) while WBI and others carried different information.', 'Correlation among indices to remove redundancy.'),
                 ('Lv et al. (2023)', 'Southern corn leaf blight; features describing the same property reduced to one representative before selection.', 'One representative per cluster.')])
    step('1.4.2', 'Relief-F ranking of the indices', part=P,
         what='The remaining indices are ranked with ReliefF (DI classes, Tasks A and B) and RReliefF (DI, Task C); the top five per task are the selected indices (VI).',
         why='ReliefF rewards features that separate classes among similar samples and can reward a feature that is useful together with others.',
         do=['Min–max scale the indices.', 'ReliefF / RReliefF with k = 10 nearest neighbours.', 'Keep the top five per task.'],
         check=['VI lists of Tasks A, B and C.'],
         out='VI → 1.6.2.',
         papers=[('Ma et al. (2026)', 'Rice blast; the Relief algorithm selected the five vegetation indices with the highest weights (RVI, PSSRb, CIre, CIgreen, SR).', 'Relief ranking, top five.'),
                 ('Mahlein et al. (2013)', 'Sugar-beet diseases; RELIEF-F selected the most relevant wavelengths for the disease indices.', 'ReliefF for disease features.'),
                 ('Lv et al. (2023)', 'Southern corn leaf blight; RELIEF-F with 10 nearest hits and misses ranked bands, indices and derivatives before SFFS.', 'k = 10 neighbours.')])

    h2('Activity 1.5 – Texture selection and the Tri-band Texture Fusion Index')
    step('1.5.1', 'Minimum redundancy maximum relevance selection of texture features', part=P,
         what='The 24 PCA texture features are filtered at |r| ≥ 0.95 and ranked by minimum redundancy maximum relevance (mRMR); the top six are kept.',
         why='Texture features are many and correlated; mRMR keeps features relevant to the DI and different from each other.',
         do=['Redundancy filter |r| ≥ 0.95.', 'mRMR ranking with the DI (mutual information); keep the top six (TF1–TF6).'],
         check=['Six texture features listed.'],
         out='TF1–TF6 → 1.5.2, 1.6.2.',
         papers=[('Ma et al. (2026)', 'Rice blast; mRMR ranked the texture features; the six with the strongest relevance and smallest redundancy were PC2-Mea, PC3-Mea, PC2-Dis, PC2-Con, PC2-Var and PC2-Hom.', 'Same method and number (six).'),
                 ('Yuan et al. (2025)', 'Rice bacterial blight; mRMR selection of UAV and satellite features.', 'mRMR for disease features.')])
    step('1.5.2', 'Tri-band Texture Fusion Index', part=P,
         what='All ordered triplets of TF1–TF6 are combined with three formulas; the triplet with the highest |r| with the DI is the TTFI.',
         why='One combination of three texture features can describe roughness, heterogeneity and structure together.',
         do=['Form 6 × 5 × 4 = 120 ordered triplets.', 'Compute TTFI1 = (TF1 + TF2)/TF3, TTFI2 = TF1 × TF2/TF3, TTFI3 = TF1 × (TF1 + TF2)/(TF2 + TF3) – 360 candidates.', 'Keep the candidate with the highest |r| with the DI.'],
         check=['Best TTFI formula and triplet.'],
         out='TTFI → 1.6.2, 2.6.',
         papers=[('Ma et al. (2026)', 'Rice blast; ordered triplets of the six mRMR texture features combined into TTFIs; TTFI3 had the highest correlation with infection (|r| = 0.756) and was used for modelling.', 'Same construction and selection by |r|.')])
    demo('ttfi', [['Formula', 'TF1, TF2, TF3 (demo values 0.8, 1.2, 0.5)', 'Value'], ['TTFI1 = (TF1 + TF2)/TF3', '(0.8 + 1.2)/0.5', '4.00'], ['TTFI2 = TF1 × TF2/TF3', '0.8 × 1.2/0.5', '1.92'], ['TTFI3 = TF1 × (TF1 + TF2)/(TF2 + TF3)', '0.8 × 2.0/1.7', '0.94']],
         'Worked example of the three TTFI formulas', widths=[3800, 3800, 2000])

    h2('Activity 1.6 – Disease-specific feature set of each camera')
    step('1.6.1', 'Selection for the multispectral, red–green–blue and thermal cameras', part=P,
         what='For each of these cameras, features are filtered at |r| ≥ 0.95 and ranked with ReliefF/RReliefF; the top five per task are kept. All four normalised thermal features are kept.',
         why='One selection method per feature type keeps the procedure simple and comparable between cameras.',
         do=['Redundancy filter |r| ≥ 0.95 within each camera.', 'ReliefF / RReliefF (k = 10), top five per task (thermal: normalised temperatures always kept).'],
         check=['Selected features of MS, RGB and thermal for Tasks A–C.'],
         out='Camera feature lists → 1.6.2.',
         papers=[('Ma et al. (2026)', 'Rice blast; one selection method per feature group (SHAP-CARS for bands, Relief for indices, mRMR for texture).', 'One method per group.'),
                 ('Feng et al. (2022)', 'Wheat powdery mildew; thermal temperature parameters kept as their own data source in the fusion.', 'Thermal group kept.')])
    step('1.6.2', 'Variance inflation factor and the disease-specific feature set', part=P,
         what='For each camera and task, the selected features (HS: OW + VI + TF + TTFI) are pooled; the feature with the largest VIF is removed one at a time until all VIF < 10. The rest is the disease-specific feature set (DSF).',
         why='Bands, indices and texture overlap; collinear inputs make models unstable and explanations unreliable.',
         do=['VIF_{j} = 1/(1 − R_{j}^{2}), R_{j}^{2} from regressing feature j on the others.', 'Remove the largest VIF and repeat until all VIF < 10.'],
         check=['DSF of each camera and task with all VIF < 10.'],
         out='DSF → 1.6.3; the same chain on the training plots → 2.2.',
         papers=[('Lv et al. (2023)', 'Southern corn leaf blight; VIF < 10 within each feature type before SFFS.', 'Same VIF < 10 rule.'),
                 ('Tian et al. (2021)', 'Rice leaf blast; VIF screening before the feature-combination search.', 'VIF before SFFS.'),
                 ('Mustafa et al. (2023)', 'Wheat Fusarium head blight; VIF to remove collinear features before modelling.', 'Same purpose.')])
    demo('vif', [['Round', 'Largest VIF', 'Feature removed', 'Features left'], ['1', '86.4', 'FD_722', '17'], ['2', '31.2', 'NDVI780', '16'], ['3', '14.8', 'PC2-Var', '15'], ['4', '8.9 (< 10)', '—', '15 = DSF']], 'VIF elimination', widths=[1200, 2200, 3000, 3200])
    step('1.6.3', 'Complementarity of the cameras', part=P,
         what='Correlation between the DSFs of different cameras and the DI response of each DSF by treatment.',
         why='Cameras that carry different information are the ones worth fusing (Objective 2).',
         do=['Cross-camera correlation matrix of the DSFs.', 'Mean DSF values by treatment and DI class.'],
         check=['Correlation heat map and treatment table.'],
         out='Expected fusion benefit → 2.8.',
         papers=[('Mahlein et al. (2019)', 'Fusarium head blight of wheat; thermal, fluorescence and hyperspectral imaging compared and combined; the sensors carried complementary information.', 'Complementarity of sensors before fusion.'),
                 ('Feng et al. (2022)', 'Wheat powdery mildew; vegetation indices were the best single source, followed by temperature parameters and texture; fusing all three gave the best model.', 'Fusion of complementary cameras.')])

    h2('Activity 1.7 – Physiological basis of the camera responses')
    step('1.7.1', 'Effect of white rust on the plant parameters', part=P,
         what='Each parameter of Step A7 is compared between inoculated plots and the healthy plot of the same treatment on each date (paired t-test), and between varieties and sowing dates within the inoculated plots (two-way ANOVA of the RBD).',
         why='Shows what white rust does to pigments, water, membranes and gas exchange in this experiment.',
         do=['Mean of the three replications per treatment and date.', 'Paired t-test inoculated vs healthy (12 pairs) per date.', 'Two-way ANOVA (variety × sowing date) within R1–R3, LSD at 5%.'],
         check=['Table of means, differences and p-values per parameter and date.'],
         out='Changed parameters → 1.7.2.',
         papers=[('Mishra et al. (2009)', 'White rust of Indian mustard; protein, phenols and sugars of inoculated leaves of six genotypes related to the disease index.', 'Infected vs healthy comparison of biochemical parameters.'),
                 ('Calderón et al. (2013)', 'Verticillium wilt of olive; physiological measurements compared between severity levels.', 'Physiology by disease level.')])
    step('1.7.2', 'Relation of the plant parameters with the disease index and the camera features', part=P,
         what='Pearson r between each parameter and the subplot DI, and between each parameter and the DSF features of the same subplot and date.',
         why='Links each selected feature to a physiological change (for example red edge with chlorophyll, thermal with stomatal conductance).',
         do=['Join parameters to the designated subplot\'s DI and features.', 'r within each date; table of the strongest links.'],
         check=['Parameter × feature correlation table.'],
         out='Physiological explanation of the DSF → discussion, 2.8.',
         papers=[('Calderón et al. (2013)', 'Verticillium wilt of olive; airborne fluorescence, temperature and narrow-band indices related to leaf physiology and disease severity.', 'Camera features related to measured physiology.'),
                 ('Zarco-Tejada et al. (2018)', 'Xylella in olive; pigment, fluorescence and temperature traits from imagery explained the disease signal.', 'Traits explain the spectral signal.')])

    h2('Activity 1.8 – Characterisation of the pre-symptomatic stage')
    step('1.8.1', 'Pre-symptomatic response curves and tests', part=P,
         what='On 1, 4 and 7 January (2, 5, 8 DAI), mean spectra and features of later-infected subplots are compared with healthy subplots; a t-test of plot means is done for every feature and date.',
         why='Shows whether and where a signal exists before pustules are visible.',
         do=['Labels of Step A5 (healthy vs later-infected).', 'Mean curves of the two groups per date and their difference.', 't-test of plot means (plot = unit) per feature and date.'],
         check=['Curves and test table for the three dates.'],
         out='Responding features → 1.8.2.',
         papers=[('Zhu et al. (2017)', 'Tobacco mosaic virus; hyperspectral images of inoculated and healthy leaves 2, 4 and 6 days after inoculation, before visible symptoms.', 'Pre-symptomatic comparison of the two groups.'),
                 ('Terentev et al. (2023)', 'Wheat leaf rust; hyperspectral changes in inoculated plants before visible symptoms.', 'Early spectral differences day by day.'),
                 ('Gold et al. (2020)', 'Potato late and early blight; leaf spectra separated infected plants before symptoms.', 'Pre-symptomatic spectral difference.'),
                 ('Zhang et al. (2024)', 'Tomato bacterial leaf spot; pre-symptomatic detection relied on water-related (about 1400 nm) and red-edge (about 750 nm) bands rather than pigments.', 'Water and red-edge features examined before symptoms.')])
    step('1.8.2', 'Pre-symptomatic feature selection', part=P,
         what='The selection chain of Activities 1.2–1.6 is run with the binary label (later-infected vs healthy) on the 576 pre-symptomatic samples.',
         why='Features that respond before symptoms can differ from those that grade visible severity.',
         do=['NDSI/RSI maps with R² of the binary label; SHAP-CARS with a classification model.', 'Filter + ReliefF for indices and MS/RGB/thermal; mRMR + TTFI for texture.', 'VIF < 10 → pre-symptomatic DSF of each camera.'],
         check=['Pre-symptomatic DSF of each camera.'],
         out='Pre-symptomatic DSF → 3.3.',
         papers=[('Tian et al. (2021)', 'Rice leaf blast at the asymptomatic stage; features selected separately for that stage.', 'Separate selection for the early stage.'),
                 ('Ma et al. (2026)', 'Rice blast; the same selection chain for early detection.', 'Same chain.'),
                 ('Terentev et al. (2023)', 'Wheat leaf rust detected from the fourth day after inoculation with an SVM; the most important wavebands were identified.', 'Selection of the bands that respond earliest.')])
    step('1.8.3', 'Earliest-responding features', part=P,
         what='For every feature of the pre-symptomatic DSF, the first date with a significant difference (Step 1.8.1) is recorded.',
         why='Tells which camera and feature responds first.',
         do=['Earliest significant date per feature; summary per camera.'],
         check=['Table of earliest dates.'],
         out='Earliest features → 3.5.',
         papers=[('Mahlein et al. (2019)', 'Fusarium head blight; compared the day on which thermal, fluorescence and hyperspectral sensors first detected infection.', 'Earliest detection day per sensor.'),
                 ('Zarco-Tejada et al. (2018)', 'Xylella; traits that changed before visual symptoms.', 'Earliest responding traits.')])
    myfig('presdemo', 'g15_presym_demo.png', 'Demo of Steps 1.8.1–1.8.3 and 3.5 (simulated): (a) difference of one feature between later-infected and healthy subplots; (b) pre-symptomatic AUC by date.')
