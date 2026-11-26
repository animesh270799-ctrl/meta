from m_lib import *
import json, re
T13 = json.load(open('/home/user/meta/thesis_build/chair7030/report_tables.json'))[12]


def add():
    h1('4. Part C – Pre-processing and spectral features')
    p('Part C turns every corrected spectrum into the same set of numbers. Each operation works on one leaf at a time and learns nothing from other leaves, so it is applied to all leaves. '
      'Three families of features are produced: spectral bands and derivatives (C5–C6), indices including red-edge and continuum-removal features (C7–C9), and wavelet features (C10).')
    card('C1', 'Handling of the ASD detector joins',
         what='After the splice correction of Step A5, the two detector-join zones (990–1010 nm and 1790–1835 nm) are excluded from the candidate bands of Objective 1 and 2 feature selection; wavelet coefficients are excluded when their window (± 2 × scale) reaches a join zone; continuum-removal features whose window crosses a join are not used. Indices whose bands lie outside these zones are unaffected.',
         why='Even a small residual step at a join creates a sharp derivative and wavelet response that a selection method can mistake for a disease feature. Screening the zones before any selection removes that risk.',
         papers=L('No disease paper reports this check; it follows Hueni and Bialek (2017), who showed that ASD inter-detector steps vary with instrument temperature.',
                  'In my replication of Lv et al. (2023) on these leaves, RELIEF-F ranked the 1800-nm step first in every task until the join zones were excluded; in my replication of Tian et al. (2021), two selected features lay on the joins (1005 and 1808 nm).'),
         match='Correction (A5) plus exclusion of the join zones from selection, as in my earlier replications of Lv et al. (2023) and Tian et al. (2021).',
         mine='Zones 990–1010 nm and 1790–1835 nm removed from Family 1 and Family 3 candidates; the spectra themselves are kept for the indices.',
         out='Screened candidate lists → D4–D9, E2.',
         q='Do you lose information at 1000 and 1800 nm? → Only 66 nm of 2001 nm are excluded, and they carry instrument artefacts rather than leaf signal.')
    card('C2', 'Savitzky–Golay smoothing',
         what='Each 1-nm spectrum (350–2500 nm) is smoothed with a Savitzky–Golay filter: second-order polynomial fitted in an 11-nm moving window.',
         why='Smoothing must come before the derivative (C5) and the wavelet transform (C10), which amplify random noise (Tsai and Philpot, 1998; Rinnan et al., 2009).',
         papers=L('Ma et al. (2026): all rice blast spectra were processed with Savitzky–Golay smoothing to reduce sensor noise before band selection.',
                  'Selvaprakash et al. (2026): rice blast leaf spectra (350–2500 nm) pre-processed with Savitzky–Golay smoothing, followed by SNV and MSC, before the band-pair index search.',
                  'Chen et al. (2023): Savitzky–Golay smoothing of ASD tobacco leaf spectra (350–2500 nm) gave the best SVM model of TMV and PVY severity among the pre-processing options tested.',
                  'Mandal et al. (2023): Savitzky–Golay smoothing of rice blast spectra before index and band analysis.'),
         match='Same filter as all four disease studies; window 11 nm and order 2 (Savitzky and Golay, 1964).',
         mine='scipy.signal.savgol_filter(window 11, polyorder 2) on 350–2500 nm before trimming (C3), so the filter has full support at 400 and 2400 nm.',
         out='Smoothed 1-nm spectra → C3–C10.',
         alt='SNV and MSC (Selvaprakash et al., 2026; Chen et al., 2023) remove scatter differences but change the absolute reflectance needed by published indices; the contact probe already standardises illumination, so they are not used.',
         q='Why 11 nm? → It suppresses detector noise while keeping the red-edge shape; a window of 11 points with order 2 is a common choice in leaf-spectra studies (Selvaprakash et al., 2026).')
    card('C3', 'Spectral range 400–2400 nm',
         what='After smoothing, the spectrum is trimmed to 400–2400 nm; 350–399 nm and 2401–2500 nm are discarded.',
         why='The detector ends have low signal and high noise; trimming after smoothing avoids edge effects of the filter.',
         papers=L('Meng et al. (2020): southern corn rust leaf spectra trimmed at the noisy ends to 400–2450 nm before building disease indices.',
                  'Matzrafi et al. (2017): leaf spectra measured with an ASD FieldSpec 4 and contact probe; the noisy edges were removed and the range set to 400–2400 nm.',
                  'Chen et al. (2025): ASD FieldSpec 4 leaf spectra trimmed to 400–2400 nm because of noise at the extreme wavelengths.'),
         match='Same range as Matzrafi et al. (2017) and Chen et al. (2025) with the same instrument and the same reason; Meng et al. (2020) is the disease study with the same practice.',
         mine='2001 bands at 1 nm remain (400–2400 nm).',
         out='Trimmed spectra → C4–C10.')
    card('C4', 'Water-absorption bands kept',
         what='The water-absorption regions (about 1350–1460 nm and 1790–1960 nm) are kept, except the join zone 1790–1835 nm screened in C1.',
         why='With a contact probe and its own lamp the light path is a few millimetres of leaf, so these regions measure leaf water, which white rust reduces in infected tissue (Mishra et al., 2009).',
         papers=L('Chen et al. (2023) and Selvaprakash et al. (2026): full 350–2500 nm leaf spectra including the water regions.',
                  'Apan et al. (2004): sugarcane orange rust detected with disease–water stress indices (DWSI) that use SWIR water-sensitive bands.',
                  'Mandal et al. (2023): removed the water bands because their spectra were affected by atmospheric water vapour – not the case for a contact probe.'),
         match='Leaf-level studies with their own light keep the full range; the reason Mandal et al. (2023) removed the bands (atmosphere) does not apply.',
         mine='Water regions enter Families 1–3 and the water and DWSI indices (C7).',
         out='→ C5–C10.',
         q='Why not remove the water bands as many papers do? → Those papers measured through air under sunlight; the contact probe has no atmospheric path.')
    card('C5', 'First derivative (no second derivative)',
         what='The first derivative of each smoothed spectrum is computed with the same Savitzky–Golay filter (window 11, order 2, derivative 1), in units of reflectance per nm.',
         why='The derivative removes additive offsets between leaves (thickness, surface, probe contact) and turns the red edge into a peak whose height and position can be measured.',
         papers=L('Zhang et al. (2012): wheat powdery mildew; derivative spectral features (amplitude, position and area of the blue, yellow and red edges) among 32 spectral features for PLSR and Fisher discriminant analysis.',
                  'Lv et al. (2023): first-order spectral derivatives at every band were one of four spectral enhancements; adding them improved severity classification of southern corn leaf blight most.',
                  'Anuar et al. (2017): Ganoderma in oil palm seedlings; first-derivative analysis for de-noising before index development.',
                  'Martínez-Martínez et al. (2018): bean angular leaf spot; raw and first-derivative reflectance compared for severity estimation.'),
         match='First derivatives at every band, as in Lv et al. (2023), and derivative red-edge features (C8), as in Zhang et al. (2012). The second derivative is not used because it amplifies noise (Tsai and Philpot, 1998).',
         mine='scipy.signal.savgol_filter(window 11, polyorder 2, deriv 1) on 350–2500 nm, then trimmed to 400–2400 nm.',
         out='Derivative spectra at 1 nm → C6 (5-nm bands), C8 (red-edge parameters).',
         alt='Simple differences between neighbouring bands are avoided because they lower the signal-to-noise ratio (Rinnan et al., 2009).',
         q='Why the derivative at all? → It is the standard way to remove baseline differences and sharpen the red edge (Demetriades-Shah et al., 1990; Tsai and Philpot, 1998).')
    card('C6', 'Band features on a 5-nm grid',
         what='For the band-based searches (NDSI/RSI maps, effective ranges, SHAP-CARS candidates), reflectance and first-derivative spectra are reduced to 5-nm bands: each band is the mean of the five 1-nm values centred on it (λ − 2 … λ + 2 nm), for λ = 400, 405 … 2400 nm.',
         why='Neighbouring 1-nm values are almost identical (the ASD records at 1.4–2 nm steps with about 3–10 nm resolution and interpolates to 1 nm), so the exhaustive searches of Step D run on 5-nm bands without losing spectral shape. Indices and red-edge parameters still use the 1-nm spectra.',
         papers=L('Ma et al. (2026): used a reduced sampling of the spectrum to compute the R² contour maps of NDSI and RSI against rice blast severity, from which the effective wavelength ranges were taken.',
                  'Mandal et al. (2023): resampled the 1-nm rice blast spectra to 10-nm bands by averaging before band selection and the two-band index search.',
                  'Mahlein et al. (2013): worked at about 6-nm spectral resolution and kept selected wavelengths at least 50 nm apart because neighbouring wavelengths are highly correlated.'),
         match='Band averaging as in Mandal et al. (2023), at a finer 5-nm interval; reduced sampling for the band-pair maps as in Ma et al. (2026).',
         mine='401 reflectance bands (R400 … R2400) and 401 derivative bands (FD400 … FD2400), minus the join zones of C1.',
         out='5-nm bands → D1, D2, D4, D5.',
         alt='Using every 1-nm band (Lv et al., 2023; Tian et al., 2021) gives 2001 nearly identical bands per type; those studies then merged features less than 10 nm apart, which has a similar effect.',
         q='Why 5 nm and not 1 nm? → 1-nm values are interpolated and redundant; 5-nm averaging follows the band averaging of Mandal et al. (2023) and the reduced sampling of Ma et al. (2026), while indices and the red-edge position keep 1-nm precision.')
    card('C7', 'Published vegetation and disease indices',
         what='41 published indices are computed for every leaf from the smoothed 1-nm reflectance: greenness and structure, pigment, red-edge, water and disease indices (Appendix A).',
         why='Indices summarise physiology in a form that can be compared with other studies and transferred to other sensors; they are Family 2 of the feature selection.',
         papers=L('Mandal et al. (2023): 26 published indices evaluated against rice blast severity, plus two new blast indices (RBI and NDBI from R1148 and R1301).',
                  'Ma et al. (2026): a set of common vegetation indices (including PSSRb, SR, GNDVI, RVI, RVSI, WBI) computed for rice blast.',
                  'Zhang et al. (2012): 11 hyperspectral vegetation indices among the spectral features of wheat powdery mildew.',
                  'Mahlein et al. (2013): the Healthy Index (HI) for sugar-beet diseases; Apan et al. (2004): disease–water stress indices (DWSI) for sugarcane orange rust.'),
         match='The index set contains the indices used in these disease studies (HI, DWSI-1 to 5, RVSI, PRI, ARI, PSRI, NDVI family, water indices) plus the rice blast indices RBI and NDBI of Mandal et al. (2023).',
         mine='Formulas and original references in Appendix A; all computed at 1 nm.',
         out='Index table (41 columns) → C8 (adds REP, Dr, REarea), D6 (adds data-driven indices), D7.')
    card('C8', 'Red-edge parameters',
         what='From the 1-nm first derivative between 680 and 760 nm: red-edge position REP (wavelength of the largest derivative), Dr (that largest derivative) and REarea (sum of the derivative over 680–760 nm).',
         why='Chlorophyll loss moves the red edge to shorter wavelengths and lowers its slope (Horler et al., 1983; Filella and Peñuelas, 1994).',
         papers=L('Zhang et al. (2012): red-edge amplitude (Dr), red-edge position (λr) and red-edge area (SDr) of wheat leaves with powdery mildew.',
                  'Mandal et al. (2023): REP, red-edge amplitude and area from the first derivative of rice blast spectra.'),
         match='Same three parameters (Dr, REP, area) as Zhang et al. (2012) and Mandal et al. (2023), computed at 1 nm.',
         mine='REP = 680 + index of the maximum derivative in 680–760 nm; Dr in 10^{−3} nm^{−1}; REarea in reflectance units.',
         out='Three parameters added to the index table → D6, D7.')
    card('C9', 'Continuum-removal absorption features',
         what='The continuum (convex hull) is removed over the chlorophyll absorption feature (530–760 nm) and the leaf-water features near 1200, 1450 and 1940 nm; for each feature the depth, width (at half depth), area and position are computed. The 970-nm water feature is not used because its window crosses the 1000-nm detector join.',
         why='Continuum removal isolates the shape of an absorption feature from the overall brightness of the leaf (Clark and Roush, 1984; Kokaly and Clark, 1999).',
         papers=L('Zhang et al. (2012): depth, width and area of the 550–750 nm continuum-removed absorption feature among the spectral features of wheat powdery mildew.',
                  'In my earlier combined-feature analysis of these leaves (Mandal et al. (2023) workflow), continuum-removal features were among the features chosen by GA-PLS.'),
         match='The 550–750 nm depth, width and area exactly as in Zhang et al. (2012); the water features follow the band-depth analysis of Kokaly and Clark (1999).',
         mine='Continuum = upper convex hull of the 1-nm reflectance between the feature shoulders; features overlapping a join zone (C1) are not used.',
         out='Continuum-removal features added to Family 2 → D7.')
    card('C10', 'Continuous wavelet features',
         what='The continuous wavelet transform (Mexican-hat mother wavelet) is applied to each smoothed 1-nm spectrum at dyadic scales 2^{1} to 2^{6}; every coefficient WF(λ, scale) is a candidate feature (Family 3).',
         why='Low scales capture narrow absorption features and high scales the broad shape, so wavelet features describe changes that bands and indices miss (Cheng et al., 2010).',
         papers=L('Tian et al. (2021): rice leaf blast from asymptomatic to mild stages; wavelet features outperformed reflectance bands and spectral indices.',
                  'Lv et al. (2023): wavelet features were one of four spectral enhancements for southern corn leaf blight and the best single feature type.',
                  'Zhang et al. (2014b): wheat yellow rust at leaf level; wavelet features estimated severity better than conventional features, including derivative features.'),
         match='Mexican-hat continuous wavelet analysis as in Tian et al. (2021), Lv et al. (2023) and Zhang et al. (2014b). In my replications of Tian et al. (2021) and Lv et al. (2023) on these leaves, wavelet features were the best single feature type.',
         mine='pywt.cwt(mexh) on 400–2400 nm after splice correction; scales 2, 4, 8, 16, 32, 64; join zones excluded (C1).',
         out='Wavelet coefficients → D9.',
         q='Why add wavelet features if DT-EDNet did not use them? → Ma et al. (2026) used image texture as a third feature family; texture does not exist for single-leaf spectra, and wavelet features play that role for spectra (Tian et al., 2021; Lv et al., 2023).')

    h2('4.1 Index table (Appendix A)')
    rows = [[c for c in r[:3]] for r in T13['rows']]
    rows[0] = ['Index', 'Formula', 'Original reference']
    rows = [[re.sub(r'(?<![A-Za-z])R(\d{3,4})', r'R_{\1}', c) for c in r] for r in rows]
    tab('indextab', rows=rows, caption='Published indices and red-edge parameters computed for every leaf (1-nm smoothed reflectance; R_{λ} = reflectance at λ nm).', widths=[1400, 5200, 3000], size=15)
