from m_lib import *


def add():
    h1('5. Part D – Objective 1: spectral response and the disease-specific feature set')
    p('Part D describes how white rust changes the leaf spectrum and which compact set of features describes it. It follows the feature-selection chain of the DT-EDNet study '
      '(Ma et al., 2026) – effective wavelength ranges from band-pair maps, optimal wavelengths by SHAP-CARS, vegetation indices – and adds the steps of the leaf-level disease studies '
      'that worked best on these data in my earlier analyses: ReliefF ranking (Mahlein et al., 2013; Lv et al., 2023), wavelet features with region representatives (Tian et al., 2021; '
      'Lv et al., 2023) and the variance inflation factor (Lv et al., 2023). Run on all leaves, Part D is a description; for the models the same chain is repeated on the training plots only (Step E2).')
    myfig('chain', 'm04_feature_chain.png', 'Feature-selection chain of Objective 1 and Step E2: three feature families, their selection steps, the VIF step and the use of the disease-specific feature set by the models.')
    card('D1', 'Mean spectra by grade and difference from healthy leaves',
         what='Mean ± SD reflectance and first derivative of each grade over 400–2400 nm; difference spectrum of each grade from grade 0.',
         why='The first, model-free evidence of where and in which direction the spectrum changes; it guides the interpretation of every selected feature.',
         papers=L('Mandal et al. (2023): mean and SD spectra of each rice blast severity level and difference from healthy plants.',
                  'Mahlein et al. (2010): spectral difference and reflectance sensitivity of sugar-beet leaves with three diseases at each wavelength.',
                  'Zhang et al. (2012): mean reflectance of normal, slight and heavy powdery mildew leaves.',
                  'Shukla et al. (2024): reflectance of aphid-infested and healthy mustard measured with ground spectroscopy.'),
         match='Mean, SD and difference-from-healthy spectra as in Mandal et al. (2023); for mustard, Shukla et al. (2024) is the closest crop study.',
         mine='All %d leaves; 5-nm bands; healthy reference = grade 0.' % CNT['all'],
         out='Spectral regions of change → interpretation of D4–D12.')
    card('D2', 'Correlation spectra',
         what='Pearson r between the grade and each 5-nm reflectance and derivative band.',
         why='Shows the strength and sign of the relationship at every wavelength; used to read the band-pair maps and the selected bands.',
         papers=L('Zhang et al. (2012): correlation of each spectral feature with the powdery mildew disease index, ranked by R².',
                  'Mandal et al. (2023): correlation of indices and bands with rice blast severity.'),
         match='Same univariate correlation analysis.',
         mine='All leaves; reflectance and derivative separately.',
         out='Correlation curves → interpretation.')
    card('D3', 'Spectra by growth stage and by factor',
         what='Mean spectra of each grade within each growth stage; mean grade by stage, variety, leaf position and sowing date.',
         why='Growth stage and date change the leaf spectrum independently of disease; the check shows whether the disease signal holds within each stage.',
         papers=L('Lv et al. (2023): spectra of healthy and infected corn leaves compared stage by stage (asymptomatic, symptomatic).',
                  'Tian et al. (2021): rice leaf blast spectra analysed separately for the asymptomatic, early and mild stages.'),
         match='Stage-wise comparison as in Lv et al. (2023) and Tian et al. (2021).',
         mine='Stages vegetative, flowering, pod formation; four sowing dates; three leaf positions; three varieties.',
         out='Strata used again in F6.')
    card('D4', 'NDSI and RSI R² maps and effective wavelength ranges',
         what='For every pair of 5-nm reflectance bands (i < j), NDSI = (R_{i} − R_{j})/(R_{i} + R_{j}) and RSI = R_{i}/R_{j} are computed and their R² with the grade drawn as maps. Bands taking part in pairs with R² ≥ 0.5 form the effective ranges; if no pair reaches 0.5, the pairs in the top 5% of R² are used.',
         why='The maps show which band combinations follow the disease and restrict the candidate bands of SHAP-CARS to the informative regions.',
         papers=L('Ma et al. (2026): R² contour maps of NDSI and RSI against rice blast severity (450–1000 nm, reduced sampling); the effective ranges were the regions where R² of both indices exceeded 0.5 (455–503, 520–661 and 702–1000 nm).',
                  'Tian et al. (2021): kept the top 5% of features by separability when choosing disease-sensitive features of rice leaf blast.',
                  'Mandal et al. (2023): searched all two-band ratio and normalised-difference combinations against rice blast severity.'),
         match='Maps, indices and the 0.5 threshold exactly as Ma et al. (2026); the top-5% fall-back follows Tian et al. (2021) and is needed because single-leaf spectra correlate more weakly than canopy spectra.',
         mine='About 80 000 band pairs of 5-nm reflectance over 400–2400 nm (join zones excluded); R² from the squared Pearson r with the grade.',
         out='Effective ranges → D5 candidates; best NDSI and RSI pair → D6.',
         q='Why a fall-back to the top 5%? → R² ≥ 0.5 was set for canopy images; for single leaves no pair may reach it, and the top-5% rule of Tian et al. (2021) keeps the most informative pairs.')
    card('D5', 'Optimal wavelengths by SHAP-CARS',
         what='Candidates: reflectance and derivative bands inside the effective ranges, plus red-edge derivatives 680–760 nm. (1) An XGBoost model predicts the grade; bands are ranked by mean |SHAP|, and the top 40% are kept. (2) Monte Carlo cross-validation chooses the number of PLS components. (3) CARS is run 20 times; bands chosen in at least half of the runs (at most 15) are the optimal wavelengths (OW).',
         why='Hundreds of correlated bands cannot be given directly to a model; SHAP removes uninformative bands first, so that CARS works on a smaller, relevant set (Ma et al., 2026).',
         papers=L('Ma et al. (2026): SHAP-CARS – SHAP values of an ensemble model ranked the bands, Monte Carlo cross-validation chose the number of PLS components, and CARS eliminated redundant variables over many iterations; 12 key wavelengths were kept for rice blast.',
                  'CARS for disease bands: pine wilt disease and cotton Verticillium wilt studies used CARS to select characteristic bands from ASD spectra.',
                  'Li et al. (2009): introduced CARS (PLS coefficients as weights, exponentially decreasing number of bands, adaptive reweighted sampling).'),
         match='The three stages of Ma et al. (2026) in the same order. Two additions: CARS is repeated 20 times with a 50% stability rule, and the Monte Carlo splits are made by plot.',
         mine='XGBoost 300 trees, depth 4, learning rate 0.05, subsample 0.8; MCCV 50 random 80/20 divisions by plot, 1–15 PLS components; CARS 50 iterations per run; seeds 42 + run.',
         out='Optimal wavelengths (Family 1 result) → D10.',
         alt='RFE-SHAP and SAND were the two other selectors of Ma et al. (2026); SHAP-CARS was kept because it gave the most compact subset in that study and combines a non-linear ranking with a PLS-based elimination.',
         q='Why repeat CARS 20 times? → CARS depends on random sampling; keeping bands chosen in at least half of the runs makes the selection reproducible.')
    card('D6', 'Data-driven indices: best NDSI, best RSI and the White Rust Index',
         what='The best NDSI and RSI pairs of D4 (bands at least 10 nm apart) are added as indices. The White Rust Index WRI = NDSI(λ1, λ2) + w·R_{λ3} is searched over the 200 best NDSI pairs (bands at least 50 nm apart), every λ3 at 10-nm steps and w ∈ {−1, −0.5, 0, 0.5, 1}, scored by |r| with the grade.',
         why='A data-driven index captures the white rust signal of these leaves; the third band can correct an effect that a two-band index cannot (Mahlein et al., 2013).',
         papers=L('Mahlein et al. (2013): spectral disease indices for sugar-beet diseases built as a normalised difference of two wavelengths plus or minus a third wavelength; selected wavelengths at least 50 nm apart.',
                  'Mandal et al. (2023): new rice blast indices from the best two-band combination (RBI = R1148/R1301; NDBI from the same bands).',
                  'Selvaprakash et al. (2026): searched more than one million normalised-difference pairs for rice blast and proposed RBI = (R1068 − R1560)/(R1068 + R1560).',
                  'Ma et al. (2026): best NDSI and RSI from the band-pair maps.'),
         match='The WRI form and the 50-nm rule are those of Mahlein et al. (2013); the exhaustive pair search follows Mandal et al. (2023) and Selvaprakash et al. (2026).',
         mine='Searches on 5-nm reflectance; WRI values computed from 1-nm reflectance at the chosen wavelengths.',
         out='NDSI_best, RSI_best and WRI added to Family 2 → D7.')
    card('D7', 'Redundancy filter of the indices',
         what='Among Family 2 (published indices, red-edge parameters, continuum-removal features, data-driven indices), features correlated at |r| ≥ 0.95 form clusters; from each cluster the feature most correlated with the grade is kept.',
         why='Many indices are near-copies (NDVI family, simple ratios); ReliefF ranks are unreliable among near-identical features.',
         papers=L('Ma et al. (2026): correlation analysis among the vegetation indices to judge which indices were redundant and which carried independent information.',
                  'Tian et al. (2021) and Lv et al. (2023): kept one representative of features that described the same region or property.'),
         match='Correlation-based redundancy screening as in Ma et al. (2026), with an explicit |r| ≥ 0.95 cut-off.',
         mine='Pearson r among all Family 2 features; threshold 0.95.',
         out='Non-redundant indices → D8.')
    card('D8', 'ReliefF / RReliefF ranking of the indices',
         what='The remaining indices are ranked with ReliefF for detection and six grades and with RReliefF for the score; the top five per task are the selected indices (VI).',
         why='ReliefF rewards features that separate classes among similar leaves and can reward a feature that is useful together with others (Robnik-Šikonja and Kononenko, 2003).',
         papers=L('Mahlein et al. (2013): RELIEF-F selected the most relevant wavelengths and wavelength differences for the sugar-beet disease indices.',
                  'Lv et al. (2023): RELIEF-F with 10 nearest hits and misses ranked bands, indices, derivatives and wavelet features of southern corn leaf blight before SFFS.'),
         match='ReliefF with k = 10 neighbours as in Lv et al. (2023). Added: neighbours from the same plot are excluded, so plot similarity cannot raise the weights.',
         mine='Features min–max scaled; k = 10; ReliefF (classes) or RReliefF (score); top 5 per task.',
         out='VI of each task → D10.')
    card('D9', 'Wavelet-feature screening by separability and regions',
         what='For each wavelet coefficient, separability is measured (detection: best balanced accuracy of a single threshold between healthy and diseased leaves; grades and score: |r| with the grade). The top 5% are kept; coefficients of the same scale less than 10 nm apart are merged into a region, and the region representative is the coefficient with the highest separability. The representatives are ranked with ReliefF/RReliefF and the top five per task form WF.',
         why='There are about 12 000 wavelet coefficients; screening, merging and ranking reduce them to a few non-redundant features.',
         papers=L('Tian et al. (2021): separability of bands, wavelet coefficients and indices by thresholding; top 5% kept; features common to all dates merged into regions with one representative; then SFFS.',
                  'Lv et al. (2023): RELIEF-F ranking of wavelet features; features within 10 nm of a better one at the same scale dropped.'),
         match='Thresholding separability, top 5% and region representatives as in Tian et al. (2021); the 10-nm merging and ReliefF ranking as in Lv et al. (2023).',
         mine='Mexican-hat coefficients of C10; join zones excluded; top 5 representatives per task.',
         out='WF of each task → D10.')
    card('D10', 'Variance inflation factor and the disease-specific feature set',
         what='For each task, OW + VI + WF are pooled; the feature with the largest variance inflation factor is removed one at a time until all VIF < 10. The remaining features are the disease-specific feature set (DSF) of that task.',
         why='Optimal wavelengths, indices and wavelet features overlap; strongly collinear inputs make models unstable and explanations unreliable.',
         papers=L('Lv et al. (2023): VIF < 10 within each feature type before SFFS for southern corn leaf blight.',
                  'O\'Brien (2007) and Dormann et al. (2013): VIF of 10 as the usual limit and methods for collinear predictors.'),
         match='The VIF < 10 rule of Lv et al. (2023), applied to the pooled families.',
         mine='VIF_{j} = 1/(1 − R_{j}^{2}), with R_{j}^{2} from regressing feature j on all others; iterative removal.',
         out='DSF of Tasks A, B and C → D11, E2, E4, E6.')
    eq('VIF_{j} = 1 / (1 − R_{j}^{2})')
    card('D11', 'Separability of the grades (Jeffries–Matusita distance)',
         what='The Jeffries–Matusita (JM) distance between every pair of grades is computed on the DSF of Task B.',
         why='It shows, before any classifier, which grades the selected features can separate and which overlap.',
         papers=L('Mandal et al. (2023): JM distance between rice blast severity levels; almost all levels were separable (JM > 1.92) except levels 4 and 5.',
                  'Das et al. (2020): JM distance as one tier of a four-tier hierarchy (statistical test, feature selection, separability, classification) for rice genotypes with field spectroradiometry.'),
         match='JM distance on the selected features as in Mandal et al. (2023) and Das et al. (2020).',
         mine='JM = 2(1 − e^{−B}) with the Bhattacharyya distance B under Gaussian class distributions (Richards, 2013); all 15 grade pairs.',
         out='Separability table → interpretation of Task B (F2).')
    card('D12', 'Principal component analysis',
         what='Principal component analysis of the 5-nm reflectance; scores of the first components plotted with 95% ellipses of each grade.',
         why='Shows the main structure of the data and whether grades form separate or overlapping groups.',
         papers=L('Selvaprakash et al. (2026): PCA of rice blast leaf spectra; most of the variance in five components.',
                  'Martínez-Martínez et al. (2018): PCA of bean leaf spectra before neural-network severity estimation.',
                  'Shukla et al. (2024): PCA loadings to identify key bands of aphid-infested mustard.'),
         match='Exploratory PCA as in Selvaprakash et al. (2026) and Shukla et al. (2024).',
         mine='All leaves; standardised 5-nm reflectance.',
         out='Visual check of grade overlap → discussion.')
