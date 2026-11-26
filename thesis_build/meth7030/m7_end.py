from m_lib import *
import re, os
HERE = os.path.dirname(os.path.abspath(__file__))

EXTRA = [
 'Anuar, M.I., Abu Seman, I., Mohd Noor, N., Abd Aziz, N., Mohd Shafri, H.Z., et al. (2017). The development of spectral indices for early detection of Ganoderma disease in oil palm seedlings. International Journal of Remote Sensing 38(23), 6505–6527. https://doi.org/10.1080/01431161.2017.1335908',
 'Ashourloo, D., Mobasheri, M.R., Huete, A. (2014). Developing two spectral disease indices for detection of wheat leaf rust (Puccinia triticina). Remote Sensing 6(6), 4723–4740. https://doi.org/10.3390/rs6064723',
 'Ben-David, A. (2008). Comparison of classification accuracy using Cohen\'s weighted kappa. Expert Systems with Applications 34(2), 825–832.',
 'Bellon-Maurel, V., Fernandez-Ahumada, E., Palagos, B., Roger, J.-M., McBratney, A. (2010). Critical review of chemometric indicators commonly used for assessing the quality of the prediction of soil attributes by NIR spectroscopy. TrAC Trends in Analytical Chemistry 29(9), 1073–1081. https://doi.org/10.1016/j.trac.2010.05.006',
 'Chen, H., Han, Y., Liu, Y., Liu, D., Jiang, L., Huang, K., Wang, H., Guo, L., Wang, X., Wang, J., Xue, W. (2023). Classification models for Tobacco Mosaic Virus and Potato Virus Y using hyperspectral and machine learning techniques. Frontiers in Plant Science 14, 1211617. https://doi.org/10.3389/fpls.2023.1211617',
 'Chen, Y., Monks, L., Rubio, V.E., Cox, A.J., Swenson, N.G. (2025). Linking leaf hyperspectral reflectance to gene expression. Communications Earth & Environment 6, 694. https://doi.org/10.1038/s43247-025-02696-1',
 'Demetriades-Shah, T.H., Steven, M.D., Clark, J.A. (1990). High resolution derivative spectra in remote sensing. Remote Sensing of Environment 33(1), 55–64. https://doi.org/10.1016/0034-4257(90)90055-Q',
 'Fawcett, T. (2006). An introduction to ROC analysis. Pattern Recognition Letters 27(8), 861–874. https://doi.org/10.1016/j.patrec.2005.10.010',
 'Gold, K.M., Townsend, P.A., et al. (2020). Hyperspectral measurements enable pre-symptomatic detection and differentiation of contrasting physiological effects of late blight and early blight in potato. Remote Sensing 12(2), 286. https://doi.org/10.3390/rs12020286',
 'Hanley, J.A., McNeil, B.J. (1982). The meaning and use of the area under a receiver operating characteristic (ROC) curve. Radiology 143(1), 29–36. https://doi.org/10.1148/radiology.143.1.7063747',
 'Mahlein, A.-K., Steiner, U., Dehne, H.-W., Oerke, E.-C. (2010). Spectral signatures of sugar beet leaves for the detection and differentiation of diseases. Precision Agriculture 11(4), 413–431. https://doi.org/10.1007/s11119-010-9180-7',
 'Martínez-Martínez, V., et al. (2018). Leaf and canopy reflectance spectrometry applied to the estimation of angular leaf spot disease severity of common bean crops. PLoS ONE 13(4), e0196072. https://doi.org/10.1371/journal.pone.0196072',
 'Matzrafi, M., Herrmann, I., Nansen, C., Kliper, T., Zait, Y., Ignat, T., Siso, D., Rubin, B., Karnieli, A., Eizenberg, H. (2017). Hyperspectral technologies for assessing seed germination and trifloxysulfuron-methyl response in Amaranthus palmeri (Palmer amaranth). Frontiers in Plant Science 8, 474. https://doi.org/10.3389/fpls.2017.00474',
 'Selvaprakash, R. [Ramalingam, S.], Sahoo, R.N., Kumar, A., Ranjan, R., Chinnasamy, V. (2026). Early detection of rice blast disease using hyperspectral remote sensing. Plant Science Today 13(1), 1–10. https://doi.org/10.14719/pst.11111',
 'Sokolova, M., Lapalme, G. (2009). A systematic analysis of performance measures for classification tasks. Information Processing & Management 45(4), 427–437. https://doi.org/10.1016/j.ipm.2009.03.002',
 'Wang, H., Qin, F., Ruan, L., et al. (2016). Identification and severity determination of wheat stripe rust and wheat leaf rust based on hyperspectral data acquired using a black-paper-based measuring method. PLoS ONE 11(4), e0154648. https://doi.org/10.1371/journal.pone.0154648',
 'Zhang, J., Pu, R., Yuan, L., Huang, W., Nie, C., Yang, G. (2014a). Integrating remotely sensed and meteorological observations to forecast wheat powdery mildew at a regional scale. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing 7(11), 4328–4339. https://doi.org/10.1109/JSTARS.2014.2315875',
 'Zhang, J., Yuan, L., Pu, R., Loraamm, R., et al. (2014b). Comparison between wavelet spectral features and conventional spectral features in detecting yellow rust for winter wheat. Computers and Electronics in Agriculture 100, 79–87. https://doi.org/10.1016/j.compag.2013.11.001',
 'Zhang, J.-C., Pu, R., Wang, J., Huang, W., Yuan, L., Luo, J. (2012). Detecting powdery mildew of winter wheat using leaf level hyperspectral measurements. Computers and Electronics in Agriculture 85, 13–23.',
 'Sun, X., Xu, W. (2014). Fast implementation of DeLong\'s algorithm for comparing the areas under correlated receiver operating characteristic curves. IEEE Signal Processing Letters 21(11), 1389–1393.',
 'Dietterich, T.G. (1998). Approximate statistical tests for comparing supervised classification learning algorithms. Neural Computation 10(7), 1895–1923.',
 'Rinnan, Å., van den Berg, F., Engelsen, S.B. (2009). Review of the most common pre-processing techniques for near-infrared spectra. TrAC Trends in Analytical Chemistry 28(10), 1201–1222. https://doi.org/10.1016/j.trac.2009.07.007',
 'Landis, J.R., Koch, G.G. (1977). The measurement of observer agreement for categorical data. Biometrics 33(1), 159–174. https://doi.org/10.2307/2529310',
 'Cheng, T., Rivard, B., Sánchez-Azofeifa, G.A., et al. (2010). Continuous wavelet analysis for the detection of green attack damage due to mountain pine beetle infestation. Remote Sensing of Environment 114(4), 899–910.',
 'Ma, J., Wu, P., Guo, S., Lin, Y., Yu, F., Liu, T. (2026). Early detection of rice blast disease using a dual transformer network (DT-EDNet) based on hyperspectral imaging and multi-feature fusion. IAENG International Journal of Applied Mathematics 56(11), 5380–5398.',
]


def add():
    h1('9. Reference papers, departures and settings')
    h2('9.1 Which paper supports which step')
    rows = [['Reference paper', 'Disease, crop and data', 'Steps of this methodology it supports'],
            ['Ma et al. (2026)', 'rice blast; UAV hyperspectral canopy, 400–1000 nm; 2,690 samples', 'B1 (7:3 stratified split), B2, C2, C6, D4, D5, D6, D7, E1, E2, E6, E7, F1, F2, F5, I1'],
            ['Mandal et al. (2023)', 'rice blast (India, 0–9 scale); handheld spectroradiometer 350–2500 nm', 'A1, A3, A6, B1, C2, C6, C7, C8, D1, D2, D4, D6, D11, E1, E2, F3'],
            ['Selvaprakash et al. (2026)', 'rice blast (IARI); 800 leaves; 350–2500 nm', 'C2, C4, D6, D12, F1'],
            ['Tian et al. (2021)', 'rice leaf blast, asymptomatic to mild; leaf spectra 350–2500 nm', 'B2, C6, C10, D3, D4, D7, D9, E1, E4, E5'],
            ['Lv et al. (2023)', 'southern corn leaf blight; leaf clip 350–2500 nm', 'A6, B2, C1, C5, C6, C10, D3, D7, D8, D9, D10, E3, E4, E5, F1'],
            ['Zhang et al. (2012)', 'wheat powdery mildew; leaf spectra (ASD, integrating sphere)', 'A6, C5, C7, C8, C9, D1, D2, E5, F2'],
            ['Mahlein et al. (2013)', 'three sugar-beet leaf diseases; hyperspectral', 'C6, C7, D6, D8, F1'],
            ['Chen et al. (2023)', 'tobacco TMV and PVY; ASD FieldSpec 4 leaves; grades 0, 1, 3, 5, 7, 9', 'A2, A3, A6, C2, C4, E1, E5, F2'],
            ['Meng et al. (2020)', 'southern corn rust; leaf clip', 'A2, C3'],
            ['Martínez-Martínez et al. (2018)', 'bean angular leaf spot; contact leaf spectra', 'A2, C5, D12'],
            ['Wang et al. (2016)', 'wheat stripe and leaf rust; in-field leaf spectra', 'B1, E5, F3'],
            ['Gold et al. (2020)', 'potato late and early blight; leaf spectra', 'E1, E5'],
            ['Zhang et al. (2014b)', 'wheat yellow rust; leaf spectra (wavelet features)', 'C10'],
            ['Anuar et al. (2017)', 'Ganoderma in oil palm seedlings', 'C5'],
            ['Apan et al. (2004)', 'sugarcane orange rust; Hyperion', 'C4, C7'],
            ['Das et al. (2020)', 'rice genotypes (IARI); field spectroradiometry', 'D11'],
            ['Shukla et al. (2024)', 'aphid-infested mustard; ground spectroscopy', 'D1, D12'],
            ['Bhattacharya and Chattopadhyay (2013)', 'mustard rot; meteorology + satellite remote sensing', 'A4, G1'],
            ['Chattopadhyay et al. (2011)', 'white rust of Indian mustard; weather and forecasting', 'A1, A4, G1'],
            ['Krishna et al. (2014)', 'wheat yellow rust (IARI); hyperspectral', 'F3']]
    tab('matrix', rows=rows, caption='Reference papers and the steps of this methodology that follow them.', widths=[2500, 3500, 3600], size=15)
    h2('9.2 Departures from the reference papers and why')
    rows = [['Step', 'Reference practice', 'This study', 'Reason'],
            ['B1 split', 'random stratified 7:3 (Ma et al., 2026) or two-thirds : one-third (Mandal et al., 2023)', 'grouped by whole plots, stratified by block type, grade and date', 'leaves of one plot are dependent (Roberts et al., 2017; Kattenborn et al., 2022)'],
            ['B2 network validation', '10% of the training set (Ma et al., 2026)', '11 of 33 training plots', 'whole plots; enough plots to cover all blocks'],
            ['C4 water bands', 'removed (Mandal et al., 2023, canopy)', 'kept', 'contact probe: no atmospheric path'],
            ['C6 band grid', '10-nm averaging (Mandal et al., 2023); reduced sampling (Ma et al., 2026)', '5-nm averaging for band searches; 1 nm for indices and red edge', 'finer grid keeps the red-edge shape'],
            ['C10 / D9 wavelets', 'texture indices of images (Ma et al., 2026)', 'wavelet features of the leaf spectrum', 'no image texture for single leaves; wavelets were best in Tian et al. (2021) and Lv et al. (2023)'],
            ['D4 threshold', 'R² ≥ 0.5 (Ma et al., 2026)', 'R² ≥ 0.5, else top 5% of pairs', 'single-leaf correlations are weaker than canopy correlations'],
            ['D5 SHAP-CARS', 'one CARS run, final subset by validation performance', '20 CARS runs, bands in ≥ 50% of runs; Monte Carlo splits by plot', 'reproducibility; leakage rule'],
            ['D8 ReliefF', 'neighbours from all samples (Lv et al., 2023)', 'neighbours of the same plot excluded', 'avoid plot similarity in the weights'],
            ['E4 SFFS', '4-fold random CV × 100 (Tian et al., 2021; Lv et al., 2023)', 'GroupKFold(3) by plot', 'leakage rule'],
            ['E6 epochs', '300 epochs, patience 60 (Ma et al., 2026)', '100 epochs, patience 20', 'CPU; same patience/epochs ratio'],
            ['E6 model selection', 'validation OA (Ma et al., 2026)', 'validation macro-F1 (A, B), RMSE (C)', 'unequal classes; regression task'],
            ['F4 uncertainty', 'single test values (Ma et al., 2026; Mandal et al., 2023)', 'plot bootstrap 95% intervals', 'one test set; related leaves']]
    tab('departures', rows=rows, caption='Departures from the reference papers, with the reason for each.', widths=[1500, 2900, 2700, 2500], size=15)

    h2('9.3 Settings of every step (Appendix B)')
    rows = [['Step', 'Setting', 'Value'],
            ['A5', 'quality control', 'L4 spectra removed; identical spectra removed (one copy kept); additive splice correction at 1000/1001 nm and check at 1800/1801 nm'],
            ['B1', 'split', 'test share 0.30; 4 healthy + 11 unsprayed test plots; 5000 candidates; seed 2026; test plots 1, 4, 5, 8, 13, 14, 18, 25, 27, 31, 35, 37, 44, 46, 48'],
            ['B2', 'inner validation', 'GroupKFold(3) by plot (ML); 11 training plots for early stopping (seed 42)'],
            ['C1', 'join zones excluded from selection', '990–1010 nm; 1790–1835 nm'],
            ['C2–C5', 'smoothing, range, derivative', 'Savitzky–Golay window 11, order 2; 400–2400 nm; water bands kept; first derivative from the same filter'],
            ['C6', 'band grid', '5-nm means of 1-nm values (λ − 2 … λ + 2 nm)'],
            ['C9', 'continuum removal', '550–750 nm; features near 970, 1200, 1450, 1940 nm; depth, width, area, position'],
            ['C10', 'wavelets', 'Mexican hat; scales 2, 4, 8, 16, 32, 64'],
            ['D4', 'effective ranges', 'R² ≥ 0.5, else top 5% of NDSI/RSI pairs'],
            ['D5', 'SHAP-CARS', 'XGBoost 300 trees, depth 4, learning rate 0.05; SHAP top 40%; MCCV 50 splits by plot, ≤ 15 PLS components; CARS 50 iterations × 20 runs; kept if ≥ 50% of runs; ≤ 15 bands'],
            ['D6', 'data-driven indices', 'pairs ≥ 10 nm apart; WRI: 200 best NDSI pairs ≥ 50 nm apart, λ3 every 10 nm, w ∈ {−1, −0.5, 0, 0.5, 1}'],
            ['D7–D9', 'redundancy and ranking', '|r| ≥ 0.95; ReliefF k = 10, same-plot neighbours excluded, top 5; wavelets: top 5%, regions < 10 nm at the same scale'],
            ['D10', 'collinearity', 'VIF < 10, iterative removal'],
            ['E3–E5', 'machine learning', 'pipeline scaling; balanced class weights; SFFS ≤ 15 features, smallest subset within 1%; grids of Table "mlgrid"'],
            ['E6', 'deep learning', 'AdamW 6 × 10^{−4}, weight decay 10^{−5}; cosine to 10^{−6}; batch 32; ≤ 100 epochs; patience 20 (minimum improvement 5 × 10^{−5}); dropout 0.03; clipping 1.2; label smoothing 0.01; seed 42; pseudo-image k = max(3, ⌈√p⌉)'],
            ['F4', 'bootstrap', '1000 resamples of whole test plots (healthy and unsprayed separately); seed 42'],
            ['G3', 'gains', '2000 paired plot-bootstrap resamples; DeLong test'],
            ['H1–H2', 'design check', '20 grouped splits (seed 7); 5 random leaf-level splits']]
    tab('settings', rows=rows, caption='Settings of every step.', widths=[900, 2400, 6300], size=15)

    h1('10. Likely questions and answers')
    qa('Why is the split 70:30?', 'It is the proportion used in the core reference paper (Ma et al., 2026: stratified 7:3) and close to the two-thirds : one-third of Mandal et al. (2023); a 20–30% test share is the usual rule (Gholamy et al., 2018). It leaves 15 test plots, enough for a plot bootstrap.')
    qa('Why split by plots and not by leaves as Ma et al. (2026) did?', 'Ma et al. split canopy samples at random; here many leaves come from each plot and share its conditions. Random leaf splits would put near-copies in training and test (Roberts et al., 2017; Kattenborn et al., 2022). Step H2 measures that inflation directly.')
    qa('Where is the reference for taking 5-nm bands?', 'Ma et al. (2026) used a reduced sampling of the spectrum for the NDSI/RSI maps; Mandal et al. (2023) averaged 1-nm spectra into 10-nm bands before band selection; Mahlein et al. (2013) worked at about 6 nm because neighbouring wavelengths are highly correlated. Here 5-nm averages are used for the searches, and indices and the red-edge position keep 1-nm precision.')
    qa('Why keep the water bands?', 'The contact probe has its own lamp and no atmospheric path, so the water regions measure leaf water, which white rust reduces. Papers that removed them measured through the atmosphere (Mandal et al., 2023).')
    qa('Why add wavelet and continuum-removal features to the DT-EDNet steps?', 'Ma et al. (2026) used image texture as a third feature family; single-leaf spectra have no texture. Wavelet features were the best single feature type for rice leaf blast (Tian et al., 2021) and southern corn leaf blight (Lv et al., 2023), and continuum-removal features were part of the powdery-mildew feature set of Zhang et al. (2012).')
    qa('How do you make sure that feature selection did not see the test plots?', 'The whole chain is repeated on the training plots (E2); inner validation is by plot (B2); scaling is fitted inside each fold (E3); the test plots are opened once (F).')
    qa('Why remove 75 spectra?', 'They were exact copies of other leaf columns of the same plot and date (13 March 2026); identical spectra cannot come from two leaves, so keeping them would count the same leaf twice.')
    qa('Why are the networks trained for 100 and not 300 epochs?', 'Training on CPU; the patience (20 of 100) keeps the same ratio as Ma et al. (2026) (60 of 300), and early stopping keeps the best epoch.')
    qa('Why judge the spectra against a model without sensors?', 'Severity follows crop age and date; weather-based models predict disease (Chattopadhyay et al., 2011; Bhattacharya and Chattopadhyay, 2013). The spectra are credited only with what they add (Zhang et al., 2014a).')
    qa('Which metric is the main one?', 'Macro-F1 for detection and grades (Ma et al., 2026; Lv et al., 2023), because the classes are unequal; QWK for the order of the grades; R², RMSE and RPD for the score (Mandal et al., 2023).')


def references(text):
    pool = []
    for fn in ('report_refs.txt', 'deck_refs.txt', 'pool_refs.txt'):
        pool += [l.strip().replace("\\'", "'").replace('--', '–').replace('\\', '') for l in open(os.path.join(HERE, fn)) if l.strip()]
    pool = EXTRA + pool
    cites = set()
    for m in re.finditer(r"([A-Z][A-Za-zÀ-ž'\-]+(?: [A-Z][a-zÀ-ž]+)?)(?: et al\.| and ([A-Z][A-Za-zÀ-ž'\-]+))?,? \(?((?:\d{4}[a-z]?, )*)(\d{4}[a-z]?)", text):
        sur, second, yrs = m.group(1), m.group(2), (m.group(3) or '').replace(',', ' ').split() + [m.group(4)]
        for y in yrs: cites.add((sur, second, y))
    chosen, missing = {}, []
    for sur, second, y in sorted(cites, key=lambda c: (c[0], c[2])):
        if sur in ('Step', 'Table', 'Figure', 'Steps', 'Appendix', 'Part', 'March', 'February', 'December', 'January', 'Dec', 'Jan', 'Feb', 'Mar', 'Python', 'R'): continue
        c = [r for r in pool if r.startswith(sur + ',') and ('(%s)' % y in r or '(%s' % y in r[:200])]
        if second: c = [r for r in c if second in r.split('(')[0]] or c
        ex = [r for r in c if r in EXTRA]
        full = ex or [r for r in c if 'et al.' not in r.split('(')[0] and '...' not in r] or c
        if not full: missing.append('%s %s' % (sur, y)); continue
        best = max(full, key=len) if len(set(full)) > 1 and all(r.split('(')[0] == full[0].split('(')[0] for r in full) else full[0]
        chosen[(sur, y, second)] = best
    return sorted(set(chosen.values()), key=str.lower), sorted(set(missing))


def add_refs(text):
    refs, missing = references(text)
    h1('References')
    for r in refs: B.append(dict(t='p', text=r))
    return len(refs), missing
