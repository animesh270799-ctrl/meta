# Extra question blocks inserted before the closing part (executed inside i_build.py namespace)
H1('K. Remote-sensing fundamentals the panel may test')
Q('Explain the spectral signature of a healthy and a diseased mustard leaf.',
  'Healthy leaf: low visible reflectance (chlorophyll absorption at about 450 and 670 nm, green peak near 550 nm), a steep red edge (690–750 nm), a high NIR plateau from mesophyll scattering, and SWIR reflectance controlled by water (1450, 1940 nm absorptions). Diseased leaf: visible reflectance rises, the red edge becomes lower and shifts to shorter wavelengths, NIR falls and SWIR rises.')
BL(['**Visible (400–700 nm):** pigment absorption; chlorosis around pustules raises reflectance, especially at 550–700 nm (Carter and Knapp, 2001).',
    '**Red edge (680–760 nm):** position and slope track chlorophyll content (Horler et al., 1983; Filella and Peñuelas, 1994).',
    '**NIR (760–1300 nm):** internal leaf structure; pustules and cell collapse lower NIR.',
    '**SWIR (1300–2500 nm):** water, cellulose, lignin and protein absorption features (Curran, 1989); water loss raises reflectance.',
    'In my leaf data, grade 9 leaves had higher visible and SWIR reflectance and a lower first-derivative peak than grade 0 leaves (Figure in Part C).'])
Q('What are spatial, spectral, radiometric and temporal resolution, and which matters most for disease?',
  'Spatial = pixel size; spectral = number and width of bands; radiometric = sensitivity (bit depth, SNR); temporal = revisit. For disease, spectral resolution (narrow red-edge and SWIR bands) and temporal resolution (catching onset) matter most; spatial resolution must be fine enough to keep fields pure.')
Q('Why does NDVI fail for disease detection?',
  'NDVI saturates at high canopy cover and responds to any loss of green biomass (drought, nutrients, senescence), so it is not specific and detects disease late. Red-edge and disease-specific indices are more sensitive to early chlorophyll change (Mahlein et al., 2013; Zheng et al., 2018).')
Q('What is atmospheric correction and why is it important for your indices?',
  'It converts top-of-atmosphere radiance to surface reflectance by removing scattering and absorption by gases and aerosols. Disease anomalies are small (a few percent reflectance), so uncorrected haze or water vapour can exceed the disease signal; water-vapour bands (1350–1450, 1800–1950 nm) are excluded.')
Q('What is emissivity, and how does it affect canopy temperature?',
  'Emissivity is the efficiency of thermal emission relative to a blackbody; vegetation has about 0.97–0.99. An error of 0.01 in emissivity changes retrieved temperature by roughly half a degree, comparable to disease effects, so a fixed canopy emissivity and calibration targets are used.')
Q('What is the signal-to-noise ratio, and where is it low in hyperspectral data?',
  'SNR is the ratio of useful signal to sensor noise; it is low at the spectral edges (below 400 nm, above 2400 nm) and in atmospheric absorption bands. In my ASD data the 350–399 nm range was about 50 times noisier than 800 nm and was removed.')
Q('What is the difference between multispectral and hyperspectral sensing?',
  'Multispectral sensors measure a few broad, separated bands (for example five 10–40 nm bands); hyperspectral sensors measure hundreds of narrow contiguous bands, giving a continuous spectrum in which specific absorption features and derivatives can be analysed (Thenkabail et al., 2004).')
Q('What is a spectral response function, and why does it matter when you transfer bands to satellites?',
  'It describes how strongly a sensor band responds at each wavelength. To simulate a satellite band from hyperspectral data, the narrow-band spectrum is weighted by the band\'s response function and integrated; without this, indices from UAV and satellite are not comparable.')

H1('L. Tough and critical questions')
Q('Your six-grade leaf classification accuracy is only about 0.32 macro-F1. Is the work useful?',
  'Yes. Exact six-grade accuracy is limited because neighbouring grades overlap; but %s of leaves were within one grade, healthy vs diseased accuracy was %s, and plot PDI was predicted with R² = %s. This is why the methodology reports PDI regression and ±1-grade accuracy, as others found for adjacent severity levels (Mandal et al., 2023; Meng et al., 2020).' % (f2(C['adj']), f2(C['detection_acc']), f2(R['r2'])))
Q('Your results come from one season and one site. How can you generalise?',
  'I cannot yet; that is why validation on an independent site (Bharatpur) and farmers\' fields is planned, and why features are physically interpretable (red edge, water) rather than site-specific. Transfer across scales and sites must be tested (Bohnenkamp et al., 2019).')
Q('Why should ISRO be interested in a drone study?',
  'Because satellites need calibration and validation data where the disease signal is known. UAV studies tell which wavelengths, resolutions and timings work, which is input for satellite algorithms and future sensor design, as SAC combined ground and satellite data for mustard rot (Bhattacharya and Chattopadhyay, 2013).')
Q('What if the White Rust Index does not work on satellite data?',
  'Then the red-edge and SWIR features, which are available on Sentinel-2 and Resourcesat SWIR, are used directly in a classifier, and the WRI is re-derived on simulated satellite bands. A negative result is still informative for sensor design.')
Q('How is your work different from routine ICAR disease surveys?',
  'Surveys give accurate but sparse point observations; my work converts them into continuous, objective maps and tests early detection. Surveys remain essential as ground truth.')
Q('Is it realistic to detect a disease with millimetre pustules from space?',
  'Not individual pustules; but the canopy-level effects – chlorophyll loss, water loss and warming over many leaves – are detectable as severity, as shown for wheat yellow rust with Sentinel-2 (Zheng et al., 2018) and airborne hyperspectral data (Nigam et al., 2019).')
Q('Could your thermal results simply reflect irrigation differences?',
  'All plots are irrigated uniformly, controls are included on every flight, and the thermal–water check tests whether warm plots have lower water status; if they do not, the warming is attributed to disease.')
Q('How do you know the spectral changes are caused by white rust and not by inoculation stress or variety?',
  'Controls of the same varieties are measured on the same dates; variety is analysed as a factor; accuracy was similar across the three varieties in the leaf data, so the features are not variety-specific.')

H1('M. Experiment, data and analysis details')
Q('Why did you use the 0–9 disease key?',
  'It is the standard assessment key for foliar diseases of rapeseed–mustard in India (Conn et al., 1990), it has explicit leaf-area limits for each grade, and the same scores give the PDI used for regression.')
Q('How is PDI calculated?',
  'PDI = Σ (score × number of leaves with that score) / (total leaves × maximum score 9) × 100 (Wheeler, 1969). In my leaf data plot PDI ranged from 0 to 76%.')
Q('Why Savitzky–Golay smoothing, and why window 11 nm?',
  'It removes high-frequency noise while preserving peak shape and gives derivatives from the same local polynomial fit (Savitzky and Golay, 1964); 11 nm at 1 nm sampling removes noise without blurring the red edge.')
Q('What is the ASD splice correction?',
  'The ASD uses separate VNIR and SWIR detectors; small steps occur at their joins (about 1000 and 1800 nm). I removed the step at 1000 nm (mean −0.0021 reflectance) by matching the SWIR segment to the VNIR extrapolation (Hueni and Bialek, 2017).')
Q('How did you remove soil, shadow and flowers from UAV hyperspectral data?',
  'A crop mask (NDVI > 0.6 and spectral angle < 0.3 rad to a crop reference; Kruse et al., 1993), then 30 endmembers per plot from which soil, shadow and flower endmembers are discarded; the plot spectrum is the mean of crop endmembers (Nascimento and Bioucas-Dias, 2005).')
Q('What is the leave-one-replication-out design exactly?',
  'Three folds: each fold tests one replication (12 inoculated plots) plus four control plots and trains on the rest; all selection and tuning use only training plots; leaves of one plot are never split.')
Q('Which models did best in your leaf analysis?',
  'Random forest for six grades (macro-F1 %s) and k-NN for PDI (R² %s with four features); the compact models were as accurate as random forest on all 53 features and better than full-spectrum PLS.' % (f2(C['macro_f1']), f2(R['r2'])))
TAB('formulas', [['Quantity', 'Formula', 'Reference'],
                 ['PDI (%)', 'Σ (score × n) / (N × 9) × 100', 'Wheeler (1969)'],
                 ['NDVI', '(R_{NIR} − R_{red}) / (R_{NIR} + R_{red})', 'Rouse et al. (1974)'],
                 ['NDRE', '(R_{NIR} − R_{RE}) / (R_{NIR} + R_{RE})', 'Gitelson and Merzlyak (1994)'],
                 ['PSRI', '(R_{680} − R_{500}) / R_{750}', 'Merzlyak et al. (1999)'],
                 ['DWSI-1; DWSI-5', 'R_{800}/R_{1660}; (R_{800} + R_{550})/(R_{1660} + R_{680})', 'Apan et al. (2004)'],
                 ['ROTI', 'R_{1175} / (R_{1982} + R_{691})', 'Bhattacharya and Chattopadhyay (2013)'],
                 ['WRI (leaf data)', WRI, 'Mahlein et al. (2013) method'],
                 ['CTD; CWSI', 'T_{c} − T_{a}; (T_{c} − T_{wet})/(T_{dry} − T_{wet})', 'Jackson et al. (1981); Jones (1999)'],
                 ['TVDI', '(T_{s} − T_{s,min}) / (T_{s,max} − T_{s,min})', 'Sandholt et al. (2002)'],
                 ['VIF', '1 / (1 − R_{j}^{2})', 'Dormann et al. (2013)'],
                 ['Macro-F1; kappa', '(1/k) Σ F1_{i}; (p_{o} − p_{e})/(1 − p_{e})', 'Sokolova and Lapalme (2009); Cohen (1960)'],
                 ['RPD', 'SD_{obs} / RMSE', 'Chang et al. (2001)']], [2000, 4500, 2806], 'Formula sheet for quick revision.', 14)

H1('N. Policy, application and future')
Q('How can your work support integrated pest and disease management and crop insurance?',
  'Maps of risk and severity allow need-based, targeted fungicide sprays (less chemical, lower cost), help plan pesticide supply, and provide objective loss evidence for crop-insurance assessment.')
Q('How might climate change affect white rust, and how can remote sensing help?',
  'Changes in winter temperature, fog and humidity patterns alter infection windows; long satellite and weather records allow risk maps to be updated and shifts in hotspots to be tracked.')
Q('If SAC designs a crop-health sensor, what specifications would you suggest from your results?',
  'Narrow bands across the red edge (690–760 nm, about 10 nm wide), NIR at 750 and 950 nm (WRI), a SWIR band near 1600 nm (and ideally 1500 and 1970 nm), 5–10 m pixels for smallholder fields, 3–5 day revisit during December–February, and a co-registered thermal band.')
Q('How would you collaborate with NRSC/SAC and ICAR after the thesis?',
  'Joint sentinel sites with UAV flights at ICAR centres (for example DRMR Bharatpur), shared spectral libraries (Krishi-DSS hosts one), and testing of the white-rust algorithm on Resourcesat, Sentinel-2 and HySIS data.')
