# Content of the interview guide v2 (no results). Executed inside i2_build.py, which provides Q, P, BL, TAB, FIG, NOTE, TIP, H1.

# ================= A =================
H1('A. Introducing the research')
Q('Please introduce your research in one minute.',
  'My research develops an objective, early and spatial method to detect and quantify white rust of Indian mustard using drone-borne hyperspectral, multispectral, RGB and thermal sensors combined with machine learning, and to make the findings usable for satellite-based monitoring.')
P('White rust, caused by the oomycete *Albugo candida*, is one of the most damaging foliar and inflorescence diseases of rapeseed–mustard in India (Saharan et al., 2014). Today it is assessed only by visual scoring of sample plants, which is slow, subjective and possible only after pustules appear (Bock et al., 2010). My thesis asks three questions: which spectral, thermal and textural signals are specific to white rust; how accurately can severity be classified and quantified when the sensors are used alone and together; and can infection be recognised before symptoms are visible. The physical idea is simple: the pathogen changes chlorophyll, leaf structure, leaf water and transpiration, and each of these leaves a measurable signature in a different part of the electromagnetic spectrum (Mahlein, 2016).')
TIP('Order: crop and disease → why visual scoring is not enough → what the sensors measure → what the thesis delivers. Keep jargon for the follow-up questions.')
Q('Give a three-minute overview of your thesis.',
  'Problem, gap, objectives, design, analysis chain, and the link to satellite monitoring, as described below.')
P('**Problem.** Rapeseed–mustard is India\'s main rabi oilseed, grown on roughly 9 million ha, mostly in Rajasthan, Haryana, Madhya Pradesh and Uttar Pradesh. White rust develops in cool, humid winter weather; systemic infection of the inflorescence (staghead) destroys seed set (Saharan et al., 2014). Fungicides are applied by calendar rather than by need because no objective spatial monitoring exists.')
P('**Gap.** Indian sensor work on mustard has addressed aphids with ground spectroscopy (Shukla et al., 2024) and Sclerotinia rot with satellite hyperspectral data (Bhattacharya and Chattopadhyay, 2013), but not white rust. There is no white-rust-specific index, no comparison of sensors on the same plots, no test of pre-symptomatic detection and no defined route to satellite monitoring.')
P('**Objectives.** (1) Characterise white rust with each UAV sensor; (2) classify six severity grades and estimate the percent disease index (PDI) with single and fused sensors; (3) predict infection before visible symptoms.')
P('**Design and analysis.** A replicated field experiment (48 plots: 12 healthy controls and 36 inoculated plots from three varieties × four inoculation dates × three replications) is flown on eight dates with four sensors, and leaf spectra are measured with an ASD spectroradiometer. A tiered analysis extracts features, selects disease-sensitive bands, builds a White Rust Index, tests responses statistically, measures class separability and selects disease-specific features; these feed machine-learning and deep-learning fusion models validated by leaving one replication out.')
P('**Link to ISRO.** The thesis identifies which wavelengths, spatial resolution and timing carry the white-rust signal, provides UAV-derived maps that can train and validate satellite models, and fits the multi-stage satellite approach developed at SAC (Bhattacharya and Chattopadhyay, 2013).')
FIG('master', 'i_master.png', 'Overall workflow of the thesis.', 460)
Q('What problem are you solving, and why does it matter?',
  'I am replacing subjective, point-based and late visual disease assessment with objective, spatially complete and potentially pre-symptomatic sensor-based assessment, so that fungicide use can be targeted and losses reduced.')
FIG('problem', 'i_problem.png', 'Problem, research gaps, solution and expected outcome.', 540)
BL(['**Agronomic importance:** mustard supplies a large share of India\'s edible oil; white rust epidemics coincide with the cool, humid weeks of December–February and, through staghead, reduce seed set directly (Saharan et al., 2014).',
    '**Limits of visual scoring:** scores depend on the observer, are recorded on a few plants, and are possible only after pustules appear; observer bias and sampling error are well documented (Bock et al., 2010).',
    '**What sensors add:** objective physical measurements, whole-field coverage, repeatability, and the possibility of detecting physiological changes (transpiration, photosynthesis) before tissue damage is visible (Mahlein, 2016; Mahlein et al., 2019).',
    '**Policy relevance:** need-based spraying lowers cost and pesticide load; spatial disease information supports advisories and crop-insurance assessment.'])
Q('What are the research gaps?',
  'Six gaps: no sensor-based white-rust study; no disease-specific index; sensors not compared on the same plots; severity treated only as a few classes; no pre-symptomatic test; no bridge from field to satellite for mustard diseases.')
TAB('gaps', [['Gap', 'Evidence from literature', 'How the thesis addresses it'],
             ['1. No sensor study of white rust', 'Indian mustard remote sensing covers aphid (Shukla et al., 2024) and rot (Bhattacharya and Chattopadhyay, 2013)', 'Leaf spectroscopy and four UAV sensors on white rust'],
             ['2. No disease-specific index', 'General vegetation indices respond to many stresses (Mahlein et al., 2013)', 'Systematic White Rust Index search'],
             ['3. Sensors not compared on the same plots', 'Most studies use one sensor (Zhang et al., 2012a; Liu et al., 2024)', 'HS, MS, RGB and thermal flown together'],
             ['4. Severity reduced to few classes', 'Adjacent severity levels overlap (Meng et al., 2020; Mandal et al., 2023)', 'Six grades plus PDI regression; adjacent-grade accuracy'],
             ['5. No pre-symptomatic test in mustard', 'Pre-symptomatic studies in rice and wheat (Tian et al., 2021; Mustafa et al., 2023)', 'Objective 3 with retrospective labels'],
             ['6. No field-to-satellite bridge', 'Features may not transfer between scales (Bohnenkamp et al., 2019)', 'Bands mapped to satellite sensors; UAV maps as training data']],
    [2700, 3500, 3106], 'Research gaps and how they are addressed.')
Q('What are your hypotheses?',
  'H1: white rust produces a spectral signature in the visible, red-edge and SWIR regions that differs from healthy canopy and can be captured in a disease-specific index. H2: thermal and textural information add to spectral information, so fused sensors estimate severity better than any single sensor. H3: changes in transpiration and photosynthesis are detectable before visible pustules.')
P('Each hypothesis follows from plant physiology: chlorophyll loss and tissue disruption alter visible, red-edge and NIR reflectance; loss of leaf water raises SWIR reflectance; stomatal regulation changes canopy temperature; pustules and staghead change texture and structure (Mahlein, 2016; Carter and Knapp, 2001).')
Q('What is the novelty of your study?',
  'To my knowledge it is the first multi-sensor (hyperspectral, multispectral, RGB, thermal) UAV study of white rust in Indian mustard, with a disease-specific index, severity modelling as both grades and PDI under leakage-free validation, a pre-symptomatic test, and an explicit pathway to ISRO satellite sensors.')
BL(['**Scientific:** disease-specific wavelengths and index; physiological interpretation of the signal.', '**Methodological:** a tiered, reproducible pipeline in which every selection and tuning step is repeated inside the training data (Varma and Simon, 2006).',
    '**Multi-sensor:** a fair comparison of four sensors on the same plots and dates.', '**Application:** wavelengths translated to satellite bands; UAV maps as calibration and validation data for satellite models.'])
Q('What will be the deliverables of the thesis?',
  'A set of white-rust-sensitive wavelengths and a White Rust Index; validated models for six grades and PDI; a comparison of sensors and fusion strategies; a pre-symptomatic risk model; and a documented method for transfer to satellites.')

# ================= B =================
H1('B. Disease biology and the physiological basis of detection')
Q('Describe the pathogen and the disease cycle.',
  'Albugo candida is an obligate biotrophic oomycete. Oospores in soil and crop debris give primary infection; zoospores released in free water infect leaves; white sori (pustules) form on the lower leaf surface; sporangia dispersed by wind and rain cause secondary cycles; systemic infection of the inflorescence produces staghead, often together with downy mildew (Saharan et al., 2014).')
FIG('cycle', 'i_cycle.png', 'Disease cycle of white rust and its weather drivers.', 460)
Q('How does infection change the leaf, and why can sensors see it?',
  'Infection alters stomatal behaviour, photosynthesis, pigments, cell structure, water status and organ morphology. Each change affects a different part of the spectrum or a different sensor.')
FIG('physio', 'i2_physio.png', 'From infection to remote-sensing signal.', 540)
BL(['**Stomata and transpiration:** infected tissue regulates stomata abnormally; reduced transpiration lowers evaporative cooling, so canopy temperature rises (thermal sensor; Mahlein et al., 2019).',
    '**Photosynthesis:** reduced photochemical efficiency changes xanthophyll-cycle activity and fluorescence, detectable with the photochemical reflectance index and fluorescence measurements (Gamon et al., 1992; Mohammed et al., 2019).',
    '**Pigments:** chlorophyll degradation around pustules raises visible reflectance and moves the red-edge inflection to shorter wavelengths (Horler et al., 1983; Filella and Peñuelas, 1994).',
    '**Structure:** sori rupture the epidermis and disturb the mesophyll, reducing NIR multiple scattering and adding white, high-contrast texture visible in RGB images.',
    '**Water:** damaged tissue loses water, increasing SWIR reflectance in the 1450–2400 nm water-absorption region (Carter and Knapp, 2001; Apan et al., 2004).',
    '**Morphology:** systemic infection causes hypertrophy and hyperplasia of the inflorescence (staghead), which changes canopy height and texture.'])
Q('Why is a biotroph like white rust spectrally different from a necrotroph like Alternaria?',
  'A biotroph keeps host cells alive while feeding, so early changes are physiological (stomata, photosynthesis, chlorosis) and pustules are raised and white; a necrotroph kills tissue, producing dark necrotic lesions with strong brown-pigment absorption and early collapse of NIR reflectance.')
P('This difference is the basis for discrimination: white rust is expected to show chlorosis, a red-edge shift, white textural spots and a gradual SWIR increase, whereas Alternaria blight is expected to show darker visible reflectance in lesions, concentric lesion texture and faster NIR decline. Mahlein et al. (2013) exploited such differences to separate three sugar-beet diseases with disease-specific indices.')
Q('What happens before symptoms appear, and can it be detected?',
  'In the latent period the pathogen grows inside the leaf; host defence (reactive oxygen species, callose, pathogenesis-related proteins) and altered stomatal regulation change transpiration and photosynthesis before tissue is visibly damaged. Thermal imaging, PRI and fluorescence are the most promising pre-symptomatic signals (Chaerle and Van der Straeten, 2000; Zarco-Tejada et al., 2018).')
P('Evidence from other pathosystems supports this: pigment and thermal changes separated infected wheat spikelets within days of inoculation (Mahlein et al., 2019), and pre-visual spectral trait changes revealed *Xylella* infection before symptoms (Zarco-Tejada et al., 2018). Objective 3 tests whether the same is true for white rust using plots that later became symptomatic.')
Q('Why does staghead matter for remote sensing?',
  'Staghead affects the inflorescence, the organ that determines yield, and changes canopy structure; it is therefore detectable through structure (height, texture) and through the spectral mixture of deformed inflorescences with leaves, and it is the most yield-relevant symptom to map.')

# ================= C: BIOTIC STRESS DETECTION =================
H1('C. Biotic stress detection with sensors')
Q('What are the principles of sensor-based biotic stress detection?',
  'Three tasks of increasing difficulty: detection (is the plant diseased?), identification (which disease?) and quantification (how severe?). Each relies on the disease altering an optical, thermal or structural property in a measurable and, ideally, specific way (Mahlein, 2016).')
BL(['**Detection** needs any reliable deviation from healthy plants; general indices and thermal anomalies can suffice.',
    '**Identification** needs specificity: a combination of spectral, temporal, textural and contextual features that differs between diseases and from abiotic stresses (Mahlein et al., 2013).',
    '**Quantification** needs a monotonic relation between the signal and severity; continuous targets (PDI) are better suited than classes (Liu et al., 2024).',
    'Sensors differ in what they see: hyperspectral (biochemistry), multispectral (operational indices), RGB (morphology and texture), thermal (transpiration), fluorescence (photosynthesis) (Mahlein et al., 2018; Thomas et al., 2018).'])
Q('Which spectral regions respond to fungal and oomycete diseases, and why?',
  'Visible (pigments), red edge (chlorophyll and structure), NIR (mesophyll scattering) and SWIR (water and dry matter). The direction and magnitude depend on the pathogen\'s mode of nutrition and the symptom type.')
TAB('regions', [['Region', 'Controlling property', 'Typical response to foliar disease', 'Example'],
                ['400–500 nm (blue)', 'Chlorophyll and carotenoid absorption', 'Small increase; carotenoid ratio changes', 'NPCI, SIPI (Peñuelas et al., 1995)'],
                ['500–680 nm (green–red)', 'Chlorophyll absorption, anthocyanin', 'Increase with chlorosis; anthocyanin may raise 550 nm absorption', 'ARI (Gitelson et al., 2001), PSRI'],
                ['680–760 nm (red edge)', 'Chlorophyll content, leaf structure', 'Inflection moves to shorter wavelengths; slope decreases', 'REP (Horler et al., 1983), NDRE'],
                ['760–1300 nm (NIR)', 'Mesophyll scattering, canopy structure', 'Decrease with tissue disruption and defoliation', 'NDVI, NIR plateau'],
                ['1300–2500 nm (SWIR)', 'Leaf water, cellulose, lignin, protein', 'Increase with water loss and necrosis', 'DWSI (Apan et al., 2004), NDWI (Gao, 1996)'],
                ['8–14 µm (thermal)', 'Emitted radiance ~ canopy temperature', 'Increase with stomatal closure', 'CTD, CWSI (Jackson et al., 1981)']], [1900, 2400, 2800, 2206], 'Spectral regions and their response to foliar disease.', 14)
FIG('bands', 'i_bands.png', 'Schematic healthy and infected canopy spectra with disease-sensitive regions and satellite band positions.', 540)
Q('Why use hyperspectral data rather than only multispectral data?',
  'Disease changes are often narrow (red-edge position, pigment ratios, specific water features). Hyperspectral sensors resolve them and allow derivatives, narrow-band indices and band selection; multispectral sensors average them over broad bands. Hyperspectral data identify the wavelengths; multispectral sensors then make monitoring affordable (Thenkabail et al., 2004; Mahlein et al., 2018).')
Q('What is the role of thermal imaging in biotic stress detection?',
  'Thermal imaging measures canopy temperature, a direct indicator of transpiration. Many pathogens disturb stomatal regulation early, so canopies warm before symptoms. Thermal data are sensitive but not specific: drought produces the same signal, so thermal is interpreted together with water status (Chaerle and Van der Straeten, 2000; Calderón et al., 2013).')
Q('What can chlorophyll fluorescence and SIF add?',
  'Fluorescence reports the efficiency of photosystem II and responds within hours to days of infection. Active fluorescence imaging works at leaf or plot level; sun-induced fluorescence (SIF) can be retrieved from very high spectral resolution radiance and is being developed for satellites such as FLEX (Mohammed et al., 2019). It is a promising pre-symptomatic signal but needs specialised sensors.')
Q('Why is disease detection harder at canopy level than at leaf level?',
  'At canopy level the leaf signal is mixed with soil, shadow, flowers, stems and other leaves, and it is modulated by canopy structure, leaf angle, illumination geometry (BRDF) and atmosphere. Symptoms on lower leaves may be hidden by upper leaves. Leaf studies show the potential signal; canopy studies show what remains of it (Mahlein, 2016; Bohnenkamp et al., 2019).')
P('This is why the thesis measures leaf spectra and UAV canopy data on the same plots: the leaf data define the expected signal, and the UAV data test how much survives mixing, structure and illumination.')
Q('How do you build a disease-specific spectral index?',
  'By searching systematically over band combinations for the one that best separates diseased from healthy (or other diseases) on training data, then validating it on independent data (Mahlein et al., 2013).')
BL(['Candidate forms: normalised differences ND(λ1, λ2) and ND plus a weighted third band, ND(λ1, λ2) + w·R(λ3).', 'Pre-selection of informative bands with ReliefF reduces the search; bands at least 50 nm apart avoid redundant pairs.',
    'For every candidate a threshold is chosen on training folds and balanced accuracy is computed on test folds.', 'The SWIR version is searched separately because water-related changes may be more specific than pigment changes.', 'The final index is checked against severity (correlation with PDI) and against other stresses (specificity).'])
Q('How is machine learning used for biotic stress detection?',
  'Machine learning combines many weak, partly redundant signals into a decision. Typical choices are SVM, random forest and k-NN on selected features, and deep networks when many labelled images exist (Rumpf et al., 2010; Behmann et al., 2015).')
P('The main risks are overfitting with few samples and many features, and leakage when neighbouring pixels or leaves of the same plot appear in training and test data. The thesis controls both by feature selection (Boruta, VIF, ML-SFFS) and by leaving whole replications out, with all selection repeated inside the training data (Varma and Simon, 2006; Roberts et al., 2017).')
Q('How should ground truth for biotic stress be collected?',
  'With a standard severity key, on the same day as the sensor acquisition, at georeferenced sampling points representative of the pixel or plot, by trained observers, and with records of other stresses. For white rust the 0–9 key for crucifer foliar diseases (Conn et al., 1990) and the PDI formula (Wheeler, 1969) are used.')
Q('How is insect-pest detection different from pathogen detection?',
  'Pests act through feeding damage, honeydew, sooty mould and defoliation, often on specific organs (aphids on inflorescences); pathogens act through tissue colonisation and physiological disruption. Pest damage is often patchier and faster, and pests are mobile, so timing and spatial pattern differ. Aphid severity in mustard has been related to visible and red-edge regions (Shukla et al., 2024), while weather-driven aphid population models support forecasting (Dutta et al., 2008).')
Q('How do you deal with mixed infections, such as white rust with downy mildew?',
  'Mixed infections are common on mustard inflorescences. The ground-truth record notes both diseases; models are first developed for white rust where it dominates; and features specific to each (white pustules versus angular chlorotic lesions with grey growth) are examined. Where separation is not possible, the product reports "foliar disease complex" rather than a false single-disease label.')
Q('How do you validate a biotic-stress model so that it generalises?',
  'Spatially and temporally independent validation: leave whole plots or replications out, then test on a different site, season or variety. Report class-wise metrics and transferability loss, not only overall accuracy (Roberts et al., 2017; Bohnenkamp et al., 2019).')
Q('What are the main sources of error in biotic stress detection?',
  'Label noise in visual scores, confounding stresses, phenology (flowering, senescence), illumination and BRDF, mixed pixels, sensor calibration, and small sample size relative to the number of features. Each has a specific control in the thesis: one trained scorer and explicit grade limits; controls and water checks; flower removal; panels and fixed flight times; crop mask and endmembers; calibration; feature selection.')
Q('How early can disease realistically be detected?',
  'It depends on the signal: physiological signals (temperature, fluorescence, PRI) can change during the latent period, pigment and structural signals only when tissue is affected, and satellite signals only when a substantial part of the pixel is affected. The thesis tests the earliest stage at which UAV sensors distinguish later-infected plots from controls.')
FIG('timeline', 'i_timeline.png', 'Expected detection windows of sensors along the development of white rust (hypothesis).', 540)

# ================= D =================
H1('D. Methodology')
Q('Give a complete overview of your methodology.',
  'Tier 0 common inputs; Objective 1 sensor tiers (features, band selection, White Rust Index, univariate tests, discriminant analysis, Boruta); Objective 2 models and fusion; Objective 3 pre-symptomatic prediction; leave-one-replication-out validation throughout.')
FIG('tiers', 'i_tiers.png', 'Tier structure of Objective 1 for the four sensors.', 470)
TAB('meth', [['Step', 'What is done', 'Why (reference)'],
             ['Ground truth', '0–9 leaf key; plot grade; PDI = Σ score/(9n) × 100', 'Conn et al. (1990); Wheeler (1969)'],
             ['Pre-processing', 'Panel and irradiance calibration; orthomosaics; crop mask NDVI > 0.6 and SAM < 0.3; endmember plot spectrum; flowers removed', 'Kruse et al. (1993); Sulik and Long (2016)'],
             ['Tier 1', 'Bands, derivatives, red edge, 48 indices; MS indices and texture; RGB texture and colour; thermal CT, CTD, NRCT', 'Guo et al. (2021); Feng et al. (2022)'],
             ['Tier 2', 'Correlation scalogram (PDI) and ReliefF (grades); one band per correlated region', 'Shukla et al. (2024); Robnik-Šikonja and Kononenko (2003)'],
             ['Tier 3', 'White Rust Index search with cross-validation', 'Mahlein et al. (2013)'],
             ['Tiers 4–6', 'ANOVA and Tukey; VIF and stepwise canonical discriminant analysis; Boruta', 'Bhattacharya and Chattopadhyay (2013); Kursa and Rudnicki (2010)'],
             ['Objective 2', 'VIF → ML-SFFS; SVM, RF, k-NN, PLSR, DNN; eight sensor sets', 'Tian et al. (2021); Maimaitijiang et al. (2020)'],
             ['Objective 3', 'Retrospective labels; t-test and Boruta; SVM, RF, k-NN; risk maps', 'Tian et al. (2021); Mustafa et al. (2023)'],
             ['Validation', 'Leave one replication out; nested selection; independent site', 'Roberts et al. (2017); Varma and Simon (2006)']], [1800, 4300, 3206], 'Methodology at a glance.', 14)
Q('Describe the experiment and ground truth.',
  'Forty-eight plots: 12 healthy controls and 36 inoculated plots (three varieties × four inoculation dates × three replications), scored on the 0–9 key on each flight date; plot PDI from leaf scores.')
BL(['Staggered inoculation creates a range of onset times and severities, needed for regression and for pre-symptomatic labels.', 'Controls give healthy references on every date and anchor the thermal baseline.', 'Same-day ground truth and one trained scorer reduce temporal and observer error (Bock et al., 2010).'])
Q('Which sensors do you use and why four?',
  'Hyperspectral VNIR + SWIR (biochemistry), multispectral red-edge camera (operational indices), RGB (texture and structure), thermal (transpiration). Each captures a different physiological consequence of infection, so together they test complementarity.')
TAB('sensors', [['Sensor', 'Measures', 'White-rust-related signal', 'Satellite analogue'],
                ['Hyperspectral VNIR + SWIR', 'Narrow-band reflectance 400–2500 nm', 'Red edge, pigments, leaf water, disease index', 'HySIS, EnMAP, PRISMA'],
                ['Multispectral (5 bands)', 'Blue, green, red, red edge, NIR', 'Red-edge indices', 'Sentinel-2 MSI'],
                ['RGB', 'Colour and texture', 'White pustules, chlorosis, staghead', 'Very-high-resolution optical'],
                ['Thermal 7.5–13.5 µm', 'Canopy temperature', 'Transpiration loss', 'Landsat TIRS, ECOSTRESS, TRISHNA (planned)']], [2200, 2400, 2500, 2206], 'Sensors, signals and satellite analogues.')
Q('How do you validate models and avoid optimistic accuracy?',
  'Leave one replication out: train on two replications and test on the third; all selection and tuning repeated inside training data; leaves of one plot never split; final test on an independent site (Varma and Simon, 2006; Roberts et al., 2017).')
Q('Why model PDI in addition to six grades?',
  'Grades are ordinal cuts of a continuous severity and neighbouring grades overlap; PDI keeps the full information, avoids errors at class boundaries and supports severity maps. Reporting adjacent-grade (±1) accuracy alongside exact accuracy reflects the ordinal nature of grades.')
Q('Why start from leaf-level ASD spectra?',
  'Leaf spectra contain the pure disease signal without soil, shadow, flowers or illumination effects; they define which wavelengths should be sought in canopy and satellite data (Mahlein et al., 2012).')

# ================= E: MASKING =================
H1('E. Mustard crop masking from satellite data')
Q('Why is a mustard crop mask the first step of satellite disease monitoring?',
  'Disease indices and anomalies are meaningful only on mustard pixels; wheat, chickpea, potato or fallow pixels would create false alarms. The mask also gives the area exposed to disease, needed for risk statistics.')
Q('What is the crop calendar, and why is it central to masking?',
  'In north-west India mustard is sown in October–November, is vegetative in November–December, flowers from late December to January, forms pods in February and is harvested in February–March. Wheat is sown later (November–December), peaks in February and is harvested in March–April. These timing differences, plus the unique yellow flowering, are the main discriminating information.')
FIG('profiles', 'i2_profiles.png', 'Schematic temporal profiles of NDVI, yellow-flower index and SAR VH backscatter for mustard and competing rabi crops.', 520)
Q('Which satellite data are used for masking?',
  'Optical time series (Sentinel-2 at 10–20 m; Resourcesat LISS-IV, LISS-III and AWiFS) and SAR time series (Sentinel-1, EOS-04/RISAT-1A), with ground-truth fields for training and validation.')
BL(['**Sentinel-2:** red-edge and SWIR bands and five-day revisit; blue and green bands capture flowering.', '**Resourcesat:** Indian operational sensors used in national crop forecasting (Parihar and Oza, 2006); LISS-IV for small fields.',
    '**SAR:** all-weather observations during foggy December–January; backscatter responds to canopy structure and biomass (Veloso et al., 2017).', '**Ground truth:** geotagged fields of each crop at vegetative and flowering stages, spread across the region.'])
Q('How do you map mustard in the vegetative stage, before flowering?',
  'By exploiting differences in timing, canopy architecture and leaf properties: earlier green-up and faster growth of mustard than wheat, the broad-leaved branched canopy of mustard (higher SAR cross-polarised backscatter and different VH/VV), and red-edge and SWIR differences, combined in a time-series classifier trained on previous-season or current ground truth.')
FIG('maskflow', 'i2_maskflow.png', 'Mustard masking workflow from vegetative stage to flowering.', 470)
P('**1. Temporal offset.** Mustard is sown and emerges several weeks before most wheat, so in November and early December mustard fields already show rising NDVI while wheat fields are bare or just emerging. Green-up date, NDVI slope and cumulative NDVI by mid-December are therefore strong vegetative-stage features. Potato also greens up early but is harvested in January; chickpea has a lower, more open canopy.')
P('**2. Canopy architecture (SAR).** Mustard is a broad-leaved, branched dicot that develops a dense, voluminous canopy early; cross-polarised (VH) backscatter, which comes mainly from volume scattering, rises earlier and higher than in wheat, whose vertical stems give a different VV and VH/VV pattern. Joint SAR–optical time series improve early crop identification (Inglada et al., 2016; Veloso et al., 2017).')
P('**3. Leaf and canopy optics.** Broad, flat mustard leaves with high chlorophyll give strong red-edge contrast; SWIR ratios reflect canopy water and leaf structure. Red-edge indices (NDRE, Sentinel-2 bands 5–7) and SWIR indices (NDWI, MSI) add separability at equal NDVI.')
P('**4. Classification.** Features from all available dates are stacked and classified with random forest or SVM, or time series are matched to reference crop profiles with time-weighted dynamic time warping, which tolerates shifts in sowing date (Belgiu and Csillik, 2018). For true early-season maps, models are trained on previous seasons\' labelled data and applied to the current season.')
P('**5. Honest limitation.** Vegetative-stage separation is weaker than flowering-stage separation; a study in Bihar found that early-season images added little to classification of mustard and other winter crops (Rao et al., 2021). Early maps should therefore be issued as provisional and refined once flowering is observed.')
Q('How do you map mustard at flowering?',
  'With yellow-flower indices. Yellow petals sharply increase green and red reflectance relative to blue, a signal no other major rabi crop shows. NDYI = (G − B)/(G + B) and similar indices peak at flowering, and the flowering date itself is a feature (Sulik and Long, 2016; d\'Andrimont et al., 2020).')
P('Automatic, training-free canola mapping has been achieved by detecting the flowering signal in Sentinel-2 time series with NDVI, red and green thresholds (Ashourloo et al., 2019). Because flowering lasts several weeks and is staggered, the maximum yellow-index value over late December–January is more robust than a single date. SAR helps when fog hides the flowering window.')
Q('Which classifier and post-processing do you use for the mask?',
  'Random forest as the main classifier (robust, little tuning, feature importance; Belgiu and Drăguţ, 2016), optionally time-weighted DTW; object-based majority within parcels to remove salt-and-pepper noise (Blaschke, 2010); training and validation split by field or village to avoid spatial leakage.')
Q('How do you handle small fields, mixed cropping and border rows?',
  'Use 10 m Sentinel-2 or 5.8 m LISS-IV, parcel boundaries where available (parcel-level crop maps are part of Krishi-DSS), erosion of field edges before training, and, for coarser sensors, sub-pixel crop fractions rather than hard classes. Mustard grown as border rows or intercrop is recorded separately in ground truth and usually falls below the mappable unit.')
Q('How do you estimate mustard acreage correctly?',
  'Not by counting classified pixels, which is biased, but by a stratified random reference sample from the map and an error-adjusted area estimator with confidence intervals (Olofsson et al., 2014).')
P('The map strata (mustard, other crops, non-crop) are sampled; each sample point is labelled from ground truth or very-high-resolution imagery; the estimated mustard area is A × Σₕ Wₕ (nₕ,mustard / nₕ), where Wₕ is the mapped proportion of stratum h. User\'s and producer\'s accuracies are reported with the area estimate (Congalton, 1991).')
Q('What are the typical confusions, and how are they resolved?',
  'Mustard–wheat (resolved by timing and flowering), mustard–potato (potato harvested early), mustard–chickpea (lower chickpea NDVI and no yellow signal), mustard–fallow or late-sown crops (green-up timing), and confusion during fog (SAR).')
TAB('confuse', [['Confusion', 'Discriminating evidence', 'Best period'],
                ['Mustard vs wheat', 'Earlier green-up and senescence of mustard; yellow-flower peak; earlier VH rise', 'Nov–Dec and late Dec–Jan; early March (wheat still green)'],
                ['Mustard vs potato', 'Potato harvested in January; no flowering signal', 'January'],
                ['Mustard vs chickpea', 'Lower NDVI and LAI of chickpea; no yellow signal', 'December–January'],
                ['Mustard vs late-sown crops', 'Green-up timing; phenology metrics', 'November–December'],
                ['Any crop under fog', 'SAR backscatter time series', 'December–January']], [2400, 4400, 2506], 'Common confusions in mustard mapping.', 14)

# ================= F: SATELLITE PATHWAY =================
H1('F. Using the research at satellite scale')
Q('What is the overall framework for scaling your results to satellites?',
  'Leaf data define the disease signal; UAV data test it at canopy level and produce plot-level severity maps; satellite models use the transferable part of the signal, trained and validated with UAV maps and ground surveys.')
FIG('scaling', 'i_scaling.png', 'Scaling framework: leaf → UAV → satellite.', 520)
Q('Give the detailed step-by-step satellite methodology.',
  'Seven steps: spectral transfer → crop mask → weather risk (when) → normal-profile anomaly (where) → stress attribution (what) → severity model (how much) → validation and delivery.')
FIG('satflow2', 'i2_satflow.png', 'Detailed pipeline for satellite-scale white-rust monitoring.', 470)
P('**Step 1 – Spectral transfer.** The narrow-band features selected at leaf and UAV level are simulated for each satellite sensor by convolving the hyperspectral reflectance with the sensor\'s spectral response function: R_band = ∫ R(λ) S(λ) dλ / ∫ S(λ) dλ. Features that remain discriminating after this broadening (typically red-edge, SWIR-1 and thermal features) are kept; the White Rust Index is re-derived on the simulated bands.')
P('**Step 2 – Crop mask.** Mustard pixels are identified with the vegetative-plus-flowering workflow of Part E.')
P('**Step 3 – Weather risk (when).** Gridded weather (IMD, MOSDAC) is converted into a daily risk score from cool temperatures, high humidity, dew and fog and sowing date, following weather-based white-rust models (Chattopadhyay et al., 2011). Only mustard pixels in high-risk periods are examined in detail, which reduces false alarms.')
P('**Step 4 – Normal-profile anomaly (where).** For each growth stage a "normal" value of red-edge, SWIR and land-surface temperature is derived from healthy fields or previous seasons; standardised deviations (z-scores) flag stressed pixels, as SAC did for wheat yellow rust with NDVI deviations from a normal growth profile (Dutta et al., 2014).')
P('**Step 5 – Stress attribution (what).** Stressed pixels are attributed using multiple evidence: drought (high temperature, low water index, low soil moisture from SAR or apparent thermal inertia), nutrient deficiency (uniform chlorosis without temperature rise), frost (sudden event after a cold night), flowering (yellow signal) and disease (temperature rise with normal water status, disease-index anomaly, patchy spreading pattern in a risk period). This mirrors the TVDI–NDWI logic of Bhattacharya and Chattopadhyay (2013).')
P('**Step 6 – Severity model (how much).** At UAV sentinel sites, plot-level PDI maps are aggregated to the satellite grid to give the fraction-weighted severity of each satellite pixel; a random-forest or SVM regressor is trained on satellite features against these sub-pixel labels and applied across the mask.')
P('**Step 7 – Validation and delivery.** Independent ground surveys and UAV transects validate the maps; outputs are district-level severity statistics and advisories delivered through existing platforms.')
Q('How do you transfer an index from hyperspectral bands to a satellite sensor?',
  'Simulate the satellite bands from hyperspectral spectra with the spectral response functions, recompute the index with the simulated bands, check how much separability is lost, and recalibrate thresholds or coefficients on satellite data with field validation.')
P('Narrow features such as the exact red-edge inflection are partly lost in broad bands; Sentinel-2 bands 5, 6 and 7 still sample the red edge, so red-edge slope indices remain usable. SWIR water features are broad and transfer well to Sentinel-2 band 11 and LISS-III/AWiFS SWIR.')
Q('How do you train a satellite model with UAV data?',
  'UAV severity maps are co-registered with satellite pixels and aggregated: for each satellite pixel the label is the area-weighted mean PDI (or the diseased fraction) of all UAV pixels inside it. This handles mixed pixels physically and gives many more training samples than ground plots alone.')
Q('What scale effects must be considered?',
  'Aggregation changes statistics (modifiable areal unit problem); relations found at one scale may weaken or change at another; within-pixel heterogeneity, soil fraction and canopy structure differ; and the effective point-spread function of the sensor blurs pixel boundaries. Scale transfer must be tested, not assumed (Bohnenkamp et al., 2019).')
Q('How would you separate disease from drought at satellite scale?',
  'By combining canopy temperature (thermal) with independent water information: water indices (NDWI, MSI from SWIR), soil moisture from SAR or apparent thermal inertia, rainfall and irrigation records. A warm canopy with normal water status in a disease-risk period indicates biotic stress; a warm canopy with low water status indicates drought.')
Q('Which Indian and international missions would be used, and for what?',
  'Resourcesat-2/2A (LISS-IV, LISS-III, AWiFS) for masks and SWIR; Sentinel-2 for red edge; EOS-04 and NISAR SAR for all-weather masks and structure; HySIS-class hyperspectral for disease indices; TRISHNA (planned) and Landsat/ECOSTRESS for thermal; INSAT-3D/3DR via MOSDAC for weather and land-surface temperature.')
TAB('missions', [['Mission / sensor', 'Key characteristics', 'Role'],
                 ['Resourcesat-2/2A LISS-IV', '5.8 m; green, red, NIR', 'Field-level mask, broad-band stress'],
                 ['LISS-III / AWiFS', '23.5 m / 56 m; includes SWIR', 'Regional stress and water status'],
                 ['Sentinel-2 MSI (ESA)', '10–20 m; three red-edge bands; SWIR; five-day revisit', 'Red-edge disease screening, flowering detection'],
                 ['HySIS', '≈ 30 m; VNIR and SWIR hyperspectral', 'Narrow-band disease indices'],
                 ['EOS-04 (RISAT-1A), NISAR', 'C-band; L- and S-band SAR', 'All-weather crop mask, canopy structure'],
                 ['TRISHNA (ISRO–CNES, planned)', 'High-resolution thermal infrared', 'Canopy temperature stress'],
                 ['INSAT-3D/3DR (MOSDAC)', 'Geostationary LST and humidity', 'Weather-risk inputs, thermal inertia']], [2600, 3200, 3506], 'Missions relevant to the satellite pathway.', 14)
NOTE('Check the latest status and specifications of planned missions before the interview.')
FIG('bandmap', 'i_satflow.png', 'Three-stage logic (weather → stress → discrimination) adapted from SAC to white rust.', 460)
Q('How can ISRO use your study for large-scale monitoring?',
  'As the disease module of an operational system: data layer (Resourcesat, Sentinel-2, SAR, hyperspectral, thermal, weather) → model layer (mask, risk, anomaly, attribution, severity trained at UAV sentinel sites) → delivery through Krishi-DSS, Bhuvan and state departments.')
FIG('ops', 'i_ops.png', 'Proposed architecture for a national white-rust monitoring service.', 470)
BL(['FASAL already integrates remote sensing, agrometeorology and land observations for crop forecasts (Parihar and Oza, 2006); a disease layer would use its crop masks and weather inputs.', 'Krishi-DSS (launched in 2024 with the Department of Space, using RISAT-1A and SAC\'s VEDAS) hosts parcel-level crop maps and stress layers.',
    'A network of UAV sentinel sites at ICAR stations and KVKs would supply training and validation data each season.', 'Uses: targeted-spraying advisories, pesticide planning, crop-insurance assessment, resistance breeding.'])
Q('If SAC designs a crop-health sensor, what would your thesis contribute?',
  'The disease-relevant wavelengths and bandwidths, the spatial resolution at which plots remain spectrally pure, the timing window, and evidence on whether thermal or texture adds value; together these define a minimum specification for disease monitoring (Mahlein et al., 2013; Thenkabail et al., 2004).')

# ================= G =================
H1('G. Practical problems with drones and satellites')
Q('What are the actual issues with drones for disease detection?',
  'Radiometric (illumination, calibration, BRDF), geometric (co-registration), thermal drift, limited area and endurance, regulation, data volume, and confounders such as flowers and shadows.')
TAB('drone', [['Issue', 'Effect', 'Mitigation'],
              ['Changing illumination', 'Reflectance drifts within a flight', 'Calibration panels and downwelling irradiance sensor; flights near solar noon under clear sky'],
              ['BRDF / view angle', 'Brightness gradients across images', 'Nadir flights, high overlap, plot-centre extraction'],
              ['Mixed pixels', 'Diluted disease signal', 'NDVI + SAM crop mask; endmember plot spectrum; flowers removed'],
              ['Thermal drift', 'Biased temperatures', 'Warm-up, reference targets, CTD and NRCT'],
              ['Co-registration', 'Feature mismatch between sensors', 'Ground control points; plot-level features; edge erosion'],
              ['Area and endurance', 'Few hectares per flight', 'UAV for calibration sites, satellites for coverage'],
              ['Regulation', 'Permissions required', 'Drone Rules 2021 and Digital Sky registration'],
              ['Data volume', 'Large processing load', 'Standardised pipeline, plot-level extraction']], [2500, 2700, 4106], 'Drone issues and mitigation.', 14)
Q('What are the actual issues with satellites for disease detection?',
  'Coarse pixels relative to fields, revisit and cloud or fog gaps, atmospheric effects, few narrow bands at high resolution, coarse thermal data, low specificity, and scarce georeferenced ground truth.')
TAB('sat', [['Issue', 'Why it matters', 'Possible solution'],
            ['Spatial resolution', 'Pustules are millimetres; fields 0.2–2 ha', 'Severity per pixel; 10 m data; sub-pixel training from UAV'],
            ['Revisit, cloud, fog', 'Epidemics develop within one to two weeks', 'Multi-sensor constellations; SAR for masks'],
            ['Atmospheric correction', 'Disease anomalies are small', 'Surface-reflectance products; exclude absorption bands'],
            ['Spectral resolution', 'Narrow disease features', 'Hyperspectral missions; red-edge approximations'],
            ['Thermal resolution', 'Coarse pixels mix fields', 'High-resolution thermal missions; disaggregation'],
            ['Specificity', 'Many stresses look similar', 'Weather risk, attribution logic, disease index'],
            ['Ground truth', 'Few georeferenced records', 'UAV sentinel sites; surveys with GPS']], [2400, 2900, 4006], 'Satellite issues and possible solutions.', 14)
Q('Why is disease detection harder than crop mapping or drought monitoring?',
  'Crop mapping relies on large phenological differences between crops; drought acts over large areas fairly uniformly. Disease starts in small foci, changes within days, produces spectral effects that overlap with other stresses, and requires specific features and precise timing.')

# ================= H =================
H1('H. Existing work by ISRO, NRSC and SAC')
Q('What has ISRO (NRSC, SAC) done on crop disease and pest remote sensing?',
  'Key studies: mustard rot tracking with weather, thermal–water indices and Hyperion (Bhattacharya and Chattopadhyay, 2013); mustard aphid modelling from satellite weather data (Dutta et al., 2008); wheat yellow-rust forewarning from NDVI deviations (Dutta et al., 2014); rice bacterial leaf blight with ground hyperspectral and LISS-IV data (Das et al., 2015); AVIRIS-NG crop health (Nigam et al., 2019); mustard aphid ground spectroscopy (Shukla et al., 2024).')
TAB('isro', [['Study (centre)', 'Crop / stress', 'Data', 'Technical core', 'Lesson for this thesis'],
             ['Bhattacharya and Chattopadhyay (2013) (SAC + DRMR)', 'Mustard Sclerotinia rot', 'Surface weather, thermal and water indices, EO-1 Hyperion, LISS-IV', 'Stage I weather anomaly; Stage II TVDI–NDWI; Stage III two-step stepwise canonical discriminant analysis; new indices (DRI, ROTI)', 'Multi-stage design; discriminant analysis; disease vs drought logic'],
             ['Dutta et al. (2008) (SAC team)', 'Mustard aphid', 'Satellite air temperature and humidity, sowing dates', 'Growth model driven by temperature weighted by humidity', 'Template for a weather-risk layer'],
             ['Dutta et al. (2014) (SAC)', 'Wheat yellow rust', 'Multi-date NDVI', 'Normal growth profile and inter-annual deviation', 'Anomaly screening at satellite scale'],
             ['Das et al. (2015) (NRSC)', 'Rice bacterial leaf blight', 'Ground spectroradiometer and LISS-IV', 'Stepwise discriminant analysis selecting a few bands; indices mapped on LISS-IV', 'Ground-to-satellite upscaling with selected bands'],
             ['Nigam et al. (2019) (SAC)', 'Wheat biotic stress', 'AVIRIS-NG airborne hyperspectral', 'Absorption band depth in red and SWIR regions', 'Band-depth features; airborne bridge to hyperspectral satellites'],
             ['Shukla et al. (2024) (NCIPM + SAC)', 'Mustard aphid', 'Ground ASD 400–2500 nm', 'Correlation of reflectance and derivatives with grade; PCA and PLSR loadings', 'Correlation scalogram as first step of band selection']],
    [1900, 1400, 1900, 2500, 1606], 'ISRO and partner studies on crop disease and pest remote sensing.', 13)
Q('Explain the SAC multi-stage method for mustard rot in technical detail.',
  'Stage I identifies weather anomalies favourable for the disease; Stage II separates canopy stress without soil-water stress in the TVDI–NDWI space; Stage III discriminates diseased from healthy crop with two-step stepwise canonical discriminant analysis on Hyperion bands and indices, mapped inside a LISS-IV crop mask.')
BL(['**Stage II:** TVDI scales surface temperature between dry and wet edges of the temperature–vegetation-index space (Sandholt et al., 2002); high TVDI with normal NDWI indicates stress not caused by drought.',
    '**Stage III:** stepwise discriminant analysis with Wilks\' lambda first selected informative Hyperion bands and then ranked published and new indices; ROTI = R1175/(R1982 + R691) was recommended.',
    '**Adopted in my thesis:** two-step discriminant design (Tier 5), DWSI and ROTI among the indices, the disease-versus-drought logic (thermal–water check), multi-stage scaling.',
    '**Improved in my thesis:** plot-level graded ground truth and PDI, leakage-free validation, four sensors, UAV resolution.'])
Q('Explain Shukla et al. (2024) and its relevance.',
  'NCIPM and SAC measured mustard canopies with an ASD spectroradiometer at Bharatpur, graded aphid infestation, correlated reflectance and its derivatives with grade and used PCA and PLSR loadings to select bands. I adopt the correlation scalogram and add ReliefF, one band per correlated region and cross-validated models.')
Q('What other ISRO programmes and platforms are relevant?',
  'FASAL (in-season crop forecasts integrating remote sensing, agrometeorology and land observations; Parihar and Oza, 2006), NADAMS (agricultural drought assessment), CHAMAN (horticulture assessment), Krishi-DSS (parcel-level crop maps and stress layers, 2024), VEDAS and Bhuvan (visualisation and dissemination), MOSDAC (meteorological satellite data).')
Q('How will you use these studies to strengthen your work?',
  'By adopting their tested components and filling their gaps.')
TAB('use', [['Study', 'What I borrow', 'How it strengthens the thesis'],
            ['Bhattacharya and Chattopadhyay (2013)', 'Two-step CDA; DWSI, ROTI; TVDI–NDWI logic; multi-stage scaling', 'Grade discrimination; disease-vs-drought check; satellite pathway'],
            ['Shukla et al. (2024)', 'Correlation scalogram of reflectance and derivatives', 'Objective band selection for mustard'],
            ['Dutta et al. (2008)', 'Weather-driven pest model', 'Weather-risk layer'],
            ['Dutta et al. (2014)', 'Normal profile and deviation', 'Anomaly screening'],
            ['Das et al. (2015)', 'Ground hyperspectral → LISS-IV transfer', 'Template for Resourcesat transfer'],
            ['Nigam et al. (2019)', 'Absorption band depth', 'Additional SWIR feature']], [2600, 3300, 3406], 'Using ISRO and partner studies.', 14)

# ================= I: WEATHER =================
H1('I. Weather and micro-weather of white rust')
Q('Which meteorological parameters influence white rust?',
  'Moderate temperatures, high relative humidity, dew, fog and leaf wetness, rainfall and cloudy spells during December–February, together with sowing date. Indian field studies report severity favoured by high morning humidity, moderately humid afternoons and cool to mild maximum temperatures (Chattopadhyay et al., 2011; Saharan et al., 2014).')
TAB('met', [['Parameter', 'Role in the disease', 'Large-scale data source'],
            ['Air temperature (Tmax, Tmin)', 'Moderate temperatures favour zoospore release and infection', 'IMD gridded data and AWS; MOSDAC; reanalysis'],
            ['Relative humidity', 'High humidity sustains sporulation and infection', 'IMD AWS; INSAT humidity products'],
            ['Rainfall, drizzle', 'Free water for zoospores; splash dispersal', 'IMD rain gauges; GPM'],
            ['Dew and fog', 'Long leaf-wetness periods at night', 'Derived from Tmin and humidity; fog from INSAT imagery'],
            ['Cloudiness, sunshine', 'Slower leaf drying', 'INSAT insolation products'],
            ['Wind', 'Dispersal of sporangia', 'AWS; reanalysis'],
            ['Sowing date and crop stage', 'Synchrony of susceptible stage with favourable weather', 'Satellite-derived crop calendar']], [2500, 3600, 3206], 'Meteorological parameters influencing white rust.', 14)
NOTE('Reported thresholds vary between locations and years; present them as reported ranges and explain that the risk model is calibrated locally.')
Q('Which micro-meteorological parameters matter, and how would you measure them?',
  'Leaf wetness duration, canopy-air humidity and temperature, dew deposition, radiation inside the canopy and air movement; measured with leaf-wetness sensors, canopy temperature and humidity loggers, infrared thermometers and the UAV thermal camera.')
BL(['Dense canopies, high nitrogen and frequent irrigation increase canopy humidity and leaf-wetness duration, favouring infection.', 'Canopy temperature integrates transpiration; logging air temperature and humidity at each flight allows CTD and CWSI (Idso et al., 1981; Jackson et al., 1981).'])
Q('How would you build a forecasting model and combine it with remote sensing?',
  'A weather-based model estimates infection risk (when and where); remote-sensing anomalies confirm whether disease developed; UAV sites calibrate both. Model forms include logistic regression of epidemic occurrence on humid-cool spell indices and infection-hour models (Chattopadhyay et al., 2011; Dutta et al., 2008).')

# ================= J: DISCRIMINATION =================
H1('J. Differentiating white rust from other diseases and stresses')
Q('What is the general strategy for differentiating white rust from other stresses?',
  'No single signal is specific, so differentiation relies on converging evidence from five independent lines: spectral signature, thermal–water relation, texture and morphology, temporal trajectory and spatial pattern, all interpreted in the context of weather and crop stage and confirmed by ground truth.')
FIG('tree', 'i_tree.png', 'Decision framework to separate white rust from other biotic and abiotic stresses.', 540)
BL(['**Spectral signature:** a disease index developed specifically against healthy and other-stress spectra, plus the pattern across visible, red-edge, NIR and SWIR rather than a single index (Mahlein et al., 2013).',
    '**Thermal–water relation:** a warm canopy with normal water status points to biotic stress; warm and dry points to drought (Bhattacharya and Chattopadhyay, 2013).',
    '**Texture and morphology:** white raised pustules (RGB texture) and staghead (canopy structure) are characteristic of white rust.',
    '**Temporal trajectory:** white rust appears and spreads after cool, humid spells, starting on lower leaves and progressing; abiotic stresses follow irrigation, soil or weather events.',
    '**Spatial pattern:** disease starts in foci and spreads between dates; abiotic stresses follow soil, topography or management boundaries.'])
Q('How is white rust different from other biotic stresses of mustard?',
  'By symptom morphology, organ affected, timing and the expected spectral, thermal and textural signature.')
TAB('biotic', [['Stress', 'Symptoms', 'Expected spectral / thermal signal', 'Discriminating evidence'],
               ['White rust (Albugo candida)', 'White raised pustules on lower leaf surface; staghead', 'Chlorosis (visible ↑), red-edge shift, NIR ↓, SWIR ↑ with water loss; canopy warming', 'White texture; cool humid weather; lower leaves first'],
               ['Downy mildew (Hyaloperonospora)', 'Angular yellow lesions, grey downy growth underneath; often on staghead', 'Chlorosis, red-edge shift', 'Lesion shape, no white pustules; frequently mixed with white rust'],
               ['Alternaria blight', 'Dark brown concentric necrotic spots; later season', 'Visible darkening in lesions (brown pigments), rapid NIR ↓', 'Dark lesion texture; warmer, later period'],
               ['Sclerotinia stem rot', 'Water-soaked stem lesions, wilting, lodging', 'Strong water stress, canopy temperature ↑, structural collapse', 'Patches with lodging at flowering–pod stage'],
               ['Powdery mildew', 'White powdery coating on upper surface, late season', 'Visible and NIR ↑ from the white coating', 'Upper-surface coating; dry late season'],
               ['Aphids', 'Colonies on inflorescence tips, honeydew, curling', 'Changes in visible and red-edge regions (Shukla et al., 2024)', 'Inflorescence-focused; January–February; warm, dry spells']], [1700, 2400, 2800, 2406], 'White rust versus other biotic stresses (symptoms after Saharan et al., 2014).', 13)
Q('How is white rust different from abiotic stresses?',
  'Abiotic stresses usually act uniformly or follow soil and management patterns, appear after identifiable events, and lack the white pustule texture and focal spread of white rust.')
TAB('abiotic', [['Abiotic stress', 'Pattern', 'Spectral and thermal signal', 'How to separate it'],
                ['Drought / water stress', 'Field-wide, follows irrigation and soil', 'Canopy temperature ↑, water index ↓, SWIR ↑', 'Water status, rainfall and irrigation records, thermal–water check'],
                ['Nitrogen deficiency', 'Uniform, older leaves first', 'Chlorophyll indices ↓ without temperature rise', 'No pustules; fertiliser and soil records'],
                ['Sulphur deficiency (important in mustard)', 'Young leaves pale, uniform', 'Chlorosis of young leaves, red-edge shift', 'Pattern on upper leaves; soil sulphur status'],
                ['Frost / cold injury', 'Sudden, after a cold night', 'Abrupt NIR drop, necrosis', 'Date of event; minimum temperature'],
                ['Salinity, waterlogging', 'Low-lying or saline patches', 'Chlorosis, stunting', 'Soil maps, elevation'],
                ['Herbicide injury', 'Along spray paths or field edges', 'Chlorosis, deformation', 'Geometric pattern; spray records'],
                ['Flowering', 'All plots at the same stage', 'Yellow: green and red ↑ relative to blue', 'Flower pixels removed; flower fraction as covariate (Sulik and Long, 2016)'],
                ['Senescence', 'Late season, all plots', 'Red-edge shift, PSRI ↑', 'Comparison with controls of the same date']], [2100, 2300, 2600, 2306], 'White rust versus abiotic stresses.', 13)
Q('How do you separate white rust from flowering and senescence effects?',
  'Flowering adds yellow petal reflectance (green and red increase relative to blue) and senescence lowers chlorophyll in all plots; both are phenological and affect controls equally. In UAV data flower pixels are removed from the leaf spectrum and the flower fraction is used as a covariate; every date is compared with healthy controls of the same date (Sulik and Long, 2016; Fang et al., 2016).')
Q('How can machine learning help discriminate between several stresses?',
  'A multi-class model trained on ground-truthed examples of each stress learns combinations of features that separate them; training data must include the confounding stresses, and validation must test each class separately. Interpretable features (indices, temperature, texture) and importance analysis show whether the model relies on physiologically meaningful signals (Behmann et al., 2015; Rumpf et al., 2010).')
Q('How do you confirm the attribution in the field?',
  'By targeted ground verification: inspection of flagged plots or pixels for pustules, lesions, pests and water status; laboratory confirmation where symptoms are ambiguous; records kept as validation data for the next season.')

# ================= K: OTHER APPROACHES =================
H1('K. Other remote-sensing approaches for disease detection and forecasting')
Q('What other methods are used, and what are their drawbacks?',
  'Vegetation-index anomalies, disease indices, band depth, machine learning, deep learning, fluorescence, thermal indices, radiative-transfer inversion, time-series anomalies, SAR, weather-based forecasting and hybrid systems.')
TAB('other', [['Approach', 'Examples (references)', 'Strengths', 'Drawbacks'],
              ['VI thresholds / NDVI anomaly', 'Yellow-rust forewarning (Dutta et al., 2014)', 'Simple, satellite-ready', 'Not specific; late'],
              ['Spectral disease indices', 'Mahlein et al. (2013); Ashourloo et al. (2014); Zheng et al. (2018)', 'Specific, transferable', 'Crop- and disease-specific; recalibration needed'],
              ['Band depth / continuum removal', 'Nigam et al. (2019); Kokaly and Clark (1999)', 'Physically based', 'Needs narrow bands; noise-sensitive'],
              ['Machine learning on spectra', 'Rumpf et al. (2010); Mustafa et al. (2023)', 'Uses many features', 'Overfitting; ground truth; transferability'],
              ['Deep learning on images', 'Mohanty et al. (2016); Maimaitijiang et al. (2020)', 'Automatic features', 'Large labelled data; black box'],
              ['Fluorescence / SIF', 'Mohammed et al. (2019); Zarco-Tejada et al. (2018)', 'Early physiological signal', 'Weak signal; special sensors'],
              ['Thermal indices', 'Calderón et al. (2013); Mahlein et al. (2019)', 'Early transpiration change', 'Not specific; weather-dependent'],
              ['Radiative-transfer inversion', 'PROSAIL (Jacquemoud et al., 2009)', 'Retrieves traits', 'Ill-posed; calibration effort'],
              ['Time-series anomalies', 'Normal-profile deviation', 'Operational', 'Confounded by sowing date'],
              ['SAR', 'EOS-04, NISAR', 'All-weather', 'Weak sensitivity to leaf disease'],
              ['Weather-based forecasting', 'Chattopadhyay et al. (2011); Dutta et al. (2008)', 'Predicts before infection', 'No information on actual disease'],
              ['Hybrid weather + remote sensing', 'Bhattacharya and Chattopadhyay (2013)', 'Combines when, where and whether', 'Needs good weather and ground data']], [2100, 2800, 2100, 2306], 'Remote-sensing approaches for disease detection and forecasting.', 13)
Q('Why did you choose a tiered feature approach over a deep CNN or a single index?',
  'A single index is simple but not specific; a CNN needs thousands of labelled images and is hard to interpret. The tiered approach first identifies interpretable, physiologically meaningful features, then uses compact models, and tests small deep networks against them, which suits a field experiment with a limited number of plot-dates.')
