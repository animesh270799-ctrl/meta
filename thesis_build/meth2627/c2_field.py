from c_lib import *
PART = 'A Field and data'


def add():
    h1('2. Part A – Field experiment and data collection')
    p('Part A creates every observation used later: the plots and treatments, the UAV images, the leaf scores and ASD leaf spectra at three survey points per subplot, the disease index, the covariates, the plant parameters and the independent test data.')
    myfig('layout', 'g02_layout.png', 'Field layout 2026-27 (same plot plan as 2025-26): healthy block (plots 1–12), 10 m buffer and inoculated block (R3, R2, R1). Each box shows the treatment (sowing date D, variety V) and plot number; colours show the fixed 7:3 split (Step D1).')

    step('A1', 'Experimental design and treatments', part=PART,
         what='Factorial field experiment at IARI, New Delhi: 4 sowing dates × 3 varieties = 12 treatments, inoculated in three replications (36 plots), plus one uninoculated healthy plot of every treatment in a separate block (12 plots) – 48 plots of 5 m × 3 m.',
         why='The design creates a range of severity (different crop ages at inoculation and different varieties) and gives healthy plots of the same age and variety; it also defines the plots that are kept together in the split.',
         do=['Sow D1 = 19 November, D2 = 26 November, D3 = 3 December and D4 = 10 December 2026 (7-day intervals).',
             'Varieties V1 = PM 26, V2 = Pusa Vijay, V3 = PM 37; plot plan as in the layout figure (healthy 1–12, R3 13–24, R2 25–36, R1 37–48).',
             'Inoculate all 36 plots of R1–R3 on 30 December 2026 with a zoosporangial suspension of ~~Albugo candida~~ (1.5 × 10^{5} zoosporangia mL^{−1}); crop age at inoculation 41, 34, 27 and 20 days for D1–D4.',
             'Keep the healthy block (plots 1–12) uninoculated, 10 m away from the inoculated block.',
             'Mark each plot with its code (plot number, treatment, replication) and divide it into four quadrant subplots (2.5 m × 1.5 m).'],
         check=['48 plots sown on the four dates; labels in place.', 'Inoculation date, suspension concentration and weather of the inoculation day recorded.', 'Subplot corners pegged (needed for Steps A3 and B6).'],
         out='Plot table (plot, block, replication, sowing date, variety) → A3, A5, D1.',
         q='Why a separate healthy block? → Healthy plots inside the inoculated block would be infected by spores from neighbouring plots; healthy controls of each treatment are needed for comparison and normalisation (Step D3).',
         papers=[('Mishra et al. (2009)', 'Inoculated ~~Brassica juncea~~ with ~~Albugo candida~~ and compared the pathological and biochemical changes of infected and healthy plants.', 'Same pathogen and crop; artificial inoculation with a zoosporangial suspension and healthy controls.'),
                 ('Guo et al. (2021)', 'Wheat yellow rust; inoculated and healthy plots to create a range of disease for UAV hyperspectral detection.', 'Inoculated replications plus healthy plots create the severity range seen by the UAV.'),
                 ('Liu et al. (2024)', 'Wheat powdery mildew; field plots with different infection levels and healthy controls for UAV multispectral and thermal images.', 'Same purpose: a field gradient of severity for UAV models.'),
                 ('Blasch et al. (2023)', 'Wheat yellow and stem rust; randomised field trial with varieties of different resistance, monitored by UAV and satellite.', 'Three varieties are included so that the models are tested across varieties.'),
                 ('Chattopadhyay et al. (2011)', 'Weather-based forecasting of white rust of Indian mustard over several sowing dates and seasons.', 'Four sowing dates give crops of different ages under the same weather.')])
    rows = [['Code', 'Sowing date', 'Crop age at inoculation (30 Dec 2026)', 'V1 PM 26', 'V2 Pusa Vijay', 'V3 PM 37'],
            ['D1', '19 Nov 2026', '41 days', 'D1V1', 'D1V2', 'D1V3'], ['D2', '26 Nov 2026', '34 days', 'D2V1', 'D2V2', 'D2V3'],
            ['D3', '3 Dec 2026', '27 days', 'D3V1', 'D3V2', 'D3V3'], ['D4', '10 Dec 2026', '20 days', 'D4V1', 'D4V2', 'D4V3']]
    tab('treat', rows=rows, caption='The 12 treatments (sowing date × variety); each is inoculated in R1–R3 and has one healthy plot.', widths=[900, 1600, 2600, 1500, 1500, 1500], size=17)

    step('A2', 'Unmanned aerial vehicle (UAV) flights and the four cameras', part=PART,
         what='On 13 dates the hyperspectral, multispectral, RGB and thermal cameras are flown over the whole field.',
         why='Each camera records a different effect of infection: pigments and structure (HS, MS), colour and texture of pustules (RGB), and transpiration (thermal).',
         do=['Fly between 11:00 and 14:00 h under clear sky and low wind, 30 m above ground, about 85% forward and 80% side overlap.',
             'Place the reflectance panels and the ground control points (GCPs) before every flight; image the panels before and after the flight.',
             'Record air temperature and relative humidity during the flight (needed for thermal conversion, Step B1).',
             'Pre-symptomatic dates: 1, 4 and 7 January 2027 (2, 5 and 8 DAI). Post-symptomatic dates: 11, 18 and 25 January, 1, 8, 15 and 22 February, 1, 8 and 15 March 2027 (12–75 DAI).',
             'On every flight day carry out the leaf scoring and ASD measurements (Steps A3 and A4).'],
         settings=['Hyperspectral: Headwall co-aligned VNIR–SWIR imager, 400–2500 nm (483 usable bands, 399–2398 nm); ground pixel about 2.2 cm.',
                   'Multispectral: MicaSense RedEdge-MX, 475, 560, 668, 717, 840 nm; about 2 cm.',
                   'RGB: DJI camera, about 0.8 cm. Thermal: FLIR Vue Pro R, 7.5–13.5 µm, 640 × 480 pixels, about 3.9 cm.'],
         check=['All four cameras flown on the date; panel images before and after.', 'GCPs visible in every mosaic.', 'Flight log (time, sky, wind, air temperature, RH) filled in.'],
         out='Raw images of the four cameras → Part B.',
         papers=[('Feng et al. (2022)', 'Wheat powdery mildew; hyperspectral, thermal infrared and RGB images acquired together and fused.', 'Same combination of cameras (plus multispectral) on the same dates.'),
                 ('Liu et al. (2024)', 'Wheat powdery mildew; UAV optical (multispectral) and thermal infrared images to estimate severity.', 'Multispectral and thermal cameras flown together.'),
                 ('Calderón et al. (2014)', 'Downy mildew of opium poppy; UAV multispectral and thermal imagery at high resolution.', 'UAV thermal + multispectral for a foliar disease.'),
                 ('Guo et al. (2021)', 'Wheat yellow rust; UAV hyperspectral imaging with reflectance panels.', 'UAV hyperspectral flights with panels.'),
                 ('Ma et al. (2026)', 'Rice blast; UAV hyperspectral images (400–1000 nm, 1.26 cm ground pixel).', 'UAV hyperspectral camera at centimetre resolution.'),
                 ('Nguyen et al. (2023)', 'Spring wheat yellow rust; multispectral UAV imagery: red-edge (690–740 nm) and near-infrared bands separated healthy and severely infected plots.', 'A multispectral camera with red-edge and near-infrared bands.')])
    myfig('timeline', 'g04_timeline.png', 'Data collection timeline, 2026-27: sowings, inoculation, 13 flight dates (pre- and post-symptomatic) with leaf scoring and ASD, and the 4 physiology dates.')
    rows = [['No.', 'Date', 'DAI', 'Stage of the data', 'Cameras', 'Leaf scoring + ASD', 'Physiology'],
            ['1', '1 Jan 2027', '2', 'pre-symptomatic', 'HS, MS, RGB, TIR', '✓', ''], ['2', '4 Jan', '5', 'pre-symptomatic', 'all four', '✓', ''], ['3', '7 Jan', '8', 'pre-symptomatic', 'all four', '✓', '✓'],
            ['4', '11 Jan', '12', 'post-symptomatic', 'all four', '✓', ''], ['5', '18 Jan', '19', 'post-symptomatic', 'all four', '✓', '✓'], ['6', '25 Jan', '26', 'post-symptomatic', 'all four', '✓', ''],
            ['7', '1 Feb', '33', 'post-symptomatic', 'all four', '✓', ''], ['8', '8 Feb', '40', 'post-symptomatic', 'all four', '✓', '✓'], ['9', '15 Feb', '47', 'post-symptomatic', 'all four', '✓', ''],
            ['10', '22 Feb', '54', 'post-symptomatic', 'all four', '✓', ''], ['11', '1 Mar', '61', 'post-symptomatic', 'all four', '✓', '✓'], ['12', '8 Mar', '68', 'post-symptomatic', 'all four', '✓', ''],
            ['13', '15 Mar', '75', 'post-symptomatic', 'all four', '✓', '']]
    tab('flights', rows=rows, caption='The 13 data-collection dates.', widths=[600, 1300, 700, 1900, 1700, 1800, 1300], size=16)

    step('A3', 'Survey points, leaf scoring and disease index', part=PART,
         what='In every subplot, three survey points are marked; at each point one plant is tagged and its leaves L3, L5 and LL are graded on the 0–9 scale on every flight day. The 9 grades of a subplot give its disease index (DI).',
         why='The DI is the reference (label) of every UAV model; grading the same tagged leaves that are measured with the ASD (Step A4) links leaf and canopy data one to one.',
         do=['Before inoculation, mark 3 survey points in each subplot on the diagonal, at 1/4, 1/2 and 3/4 of its length, inside an inner buffer that excludes border rows; tag the nearest plant at each point (3 × 4 = 12 tagged plants per plot, 576 in the field).',
             'On each flight day (same day or ± 1 day) grade the 3rd (L3) and 5th (L5) fully expanded leaves from the top and the lowest green leaf (LL) of each tagged plant; count the positions again on every date.',
             'Grade key (0–9 key of Conn et al., 1990): 0 = no pustules; 1 = 1–5%; 3 = 6–10%; 5 = 11–25%; 7 = 26–50%; 9 = more than 50% of the leaf area with pustules. Keep the written limits on the record sheet; the same trained person grades all dates.',
             'Subplot DI = Σ(x × f) / (9 × Σf) × 100, where x is the grade and f the number of leaves with grade x (9 leaves per subplot).',
             'From flowering, record staghead severity (%) per subplot = staghead racemes / total racemes × 100.',
             'If a tagged plant dies, tag the nearest healthy-looking neighbour and note the change.'],
         settings=['DI classes (Task B): 0 (DI = 0), 1 (0 < DI ≤ 5), 3 (5 < DI ≤ 10), 5 (10 < DI ≤ 25), 7 (25 < DI ≤ 50), 9 (DI > 50).'],
         check=['9 grades per subplot on every date (missing leaves written as missing).', 'DI computed for 192 subplots per date.', 'Scorer, date and time on every sheet.'],
         out='Leaf grades (→ A4, Part L) and subplot DI and DI class (→ A5, all UAV models).',
         alt='Image-based pustule area would avoid rater error but is not available for all leaves in the field; visual grades are the field standard (Bock et al., 2010).',
         q='Why three points on the diagonal? → They spread the tagged plants over the subplot so that the DI represents the whole subplot seen by the UAV, and the same points carry the ASD readings.',
         papers=[('Liu et al. (2024)', 'Wheat powdery mildew; severity of each plot expressed as a disease index from graded leaves and used as the target of UAV models.', 'Subplot DI from graded leaves is the target of the UAV models.'),
                 ('Ma et al. (2026)', 'Rice blast; disease index from lesion area and severity weights (healthy, mild, moderate, severe) as the label of UAV hyperspectral samples.', 'A disease index from weighted severity grades as the label.'),
                 ('Chen et al. (2023)', 'Tobacco viruses; severity scored in grades 0, 1, 3, 5, 7, 9.', 'The same six grade values.'),
                 ('Mandal et al. (2023)', 'Rice blast scored on the 0–9 scale and related to leaf spectra.', 'Same 0–9 scale for leaf grades.'),
                 ('Conn et al. (1990)', 'Alternaria blackspot of rapeseed and mustard; a disease assessment key that grades leaves 0–9 by the percentage of leaf area affected.', 'The same 0–9 leaf-area key, applied to white rust pustules.'),
                 ('Bock et al. (2010)', 'Reviewed visual severity assessment: raters disagree most between neighbouring classes; clear class limits and trained raters reduce error.', 'Written grade limits and one trained scorer for all dates.'),
                 ('Zhang et al. (2022)', 'Rice leaf blast; the disease grade of each leaf classified from hyperspectral images at the jointing, booting and heading stages.', 'Leaf grades recorded on every date across growth stages.')])
    myfig('survey', 'g03_survey.png', 'Subplots, inner buffer and the 3 survey points of each subplot (left); leaves graded and measured on each tagged plant (right).')
    demo('di_ex', [['Point', 'Leaf', 'Grade x', 'x × f contribution'],
                   ['1', 'L3 / L5 / LL', '0 / 1 / 3', '0 + 1 + 3'], ['2', 'L3 / L5 / LL', '1 / 3 / 5', '1 + 3 + 5'], ['3', 'L3 / L5 / LL', '0 / 3 / 7', '0 + 3 + 7'],
                   ['Subplot', '9 leaves', 'Σ(x × f) = 23', 'DI = 23 / (9 × 9) × 100 = 28.4% → DI class 7']],
         'Worked example of the disease index of one subplot', widths=[1500, 2500, 2500, 3100])

    step('A4', 'Leaf spectra with the ASD FieldSpec spectroradiometer at the same survey points', part=PART,
         what='Right after grading, the same 9 leaves of each subplot are measured with the ASD FieldSpec spectroradiometer (contact probe and leaf clip with its own lamp) on all 13 dates.',
         why='The leaf spectrum of a graded leaf is the cleanest record of the disease signal (no sun, sky, soil or atmosphere); it supports Part L and the link between leaf and canopy.',
         do=['Warm up the instrument; optimise and take a white reference at the start, then every 10–15 minutes or at the start of every plot.',
             'Take 2 readings per leaf on the lamina, avoiding the midrib (each reading = the instrument average of its scans), 350–2500 nm.',
             'Name every file with date, plot, subplot, point, leaf position and reading number; write the leaf grade of Step A3 on the same row of the sheet.',
             'Measure on the flight day (or ± 1 day); the clip has its own lamp, so the time of day does not matter.'],
         settings=['1728 leaves per date (48 plots × 4 subplots × 3 points × 3 leaves) × 2 readings = 3456 readings per date.'],
         check=['Every leaf graded in A3 has 2 readings.', 'White reference times recorded.', 'File names match the record sheet.'],
         out='Leaf spectra with leaf grade and identifiers → Part L.',
         papers=[('Mandal et al. (2023)', 'Rice blast; leaf spectra with a handheld spectroradiometer (350–2500 nm) of leaves scored on the 0–9 scale.', 'Leaf spectra of graded leaves, full range.'),
                 ('Chen et al. (2023)', 'Tobacco TMV and PVY; leaves measured with an ASD FieldSpec 4 (350–2500 nm) and graded 0, 1, 3, 5, 7, 9.', 'Same instrument class and grade scale.'),
                 ('Lv et al. (2023)', 'Southern corn leaf blight; leaf-clip spectra (350–2500 nm) for asymptomatic detection and severity classes.', 'Leaf clip with its own lamp.'),
                 ('Martínez-Martínez et al. (2018)', 'Bean angular leaf spot; spectra in contact with the leaf estimated severity better than spectra taken above the crop.', 'Contact measurement of single leaves.'),
                 ('Yu et al. (2021)', 'Pine wilt disease; field portable spectrometer measurements collected with UAV hyperspectral images.', 'Leaf spectra collected on the same dates as the UAV flights.'),
                 ('Mandal et al. (2022)', 'Rice blast (IARI); reflectance of ten genotypes scored 0–9; correlation above 0.6 with severity in 550–760 and 1140–1300 nm.', 'Leaf reflectance of plants scored on the 0–9 scale.')])
    demo('rec', [['Date', 'Plot', 'Subplot', 'Point', 'Leaf', 'Grade', 'ASD files', 'White ref.'],
                 ['18 Jan 2027', '25', '2', '1', 'L3', '1', '25_2_1_L3_01, _02', '10:42'], ['18 Jan 2027', '25', '2', '1', 'L5', '3', '25_2_1_L5_01, _02', '10:42'], ['18 Jan 2027', '25', '2', '1', 'LL', '5', '25_2_1_LL_01, _02', '10:42']],
         'Record sheet for leaf grades and ASD readings', widths=[1300, 700, 900, 800, 800, 800, 2700, 1100])

    step('A5', 'Labels and the datasets', part=PART,
         what='Labels of the three tasks are set for every UAV sample (subplot-date) and every leaf; the pre-symptomatic labels are set from the later status.',
         why='Each task answers a different question (is it diseased? how severe? what score?) and needs its own models and metrics.',
         do=['UAV, post-symptomatic dates: Task A = healthy (DI = 0) or diseased (DI > 0), from the survey, not from the treatment; Task B = DI class (0, 1, 3, 5, 7, 9); Task C = DI (%).',
             'If a DI class has fewer than 5% of the samples, merge it with its neighbour (for example 7 + 9) and note it.',
             'Leaves (Part L): Task A = grade 0 or > 0; Task B = leaf grade; Task C = leaf grade as a number.',
             'Pre-symptomatic dates (2, 5, 8 DAI): healthy = subplots of the healthy plots; later-infected = inoculated subplots whose DI becomes > 0 on a later date; inoculated subplots that never show pustules are left out.'],
         check=['Every sample has its three labels.', 'Class counts tabulated before any analysis.'],
         out='Labelled tables: UAV post-symptomatic (1920 per camera), UAV pre-symptomatic (576 per camera), leaves (22 464) → Parts B–D, L.',
         papers=[('Lv et al. (2023)', 'Southern corn leaf blight; asymptomatic and symptomatic detection plus severity classes.', 'Detection task plus severity classes.'),
                 ('Chen et al. (2023)', 'Tobacco viruses; binary (healthy/infected) and six-grade models.', 'Task A and six-class Task B.'),
                 ('Feng et al. (2022)', 'Wheat powdery mildew; classification and regression of severity from fused UAV data.', 'Classification and regression on the same samples.'),
                 ('Zhu et al. (2017)', 'Tobacco disease; pre-symptomatic samples labelled from the later development of the infection.', 'Pre-symptomatic labels from the later status.'),
                 ('Tian et al. (2021)', 'Rice leaf blast from asymptomatic to mild stages; infected and healthy classes at each stage.', 'Separate early-stage labels.')])

    step('A6', 'Covariates and weather', part=PART,
         what='For every sample: DAI, variety, crop age at inoculation, growth stage, 7-day weather and the number of favourable days for white rust.',
         why='Severity also follows time, crop stage and weather; these covariates describe the epidemic and form the sensor-free baseline of Steps 2.9, 3.5 and L8.',
         do=['DAI = flight date − 30 December 2026.',
             'Growth stage on each date with the BBCH scale, coded 1 = vegetative (BBCH 10–49), 2 = flowering (60–69), 3 = pod formation (70 and later).',
             'Daily weather from the IARI observatory: Tmax, Tmin, morning and afternoon relative humidity (RH I, RH II), rainfall; mean (rainfall: total) of the 7 days ending the day before each flight.',
             'Favourable days since inoculation, counted with the white rust weather conditions used in forecasting (Chattopadhyay et al., 2011): leaf infection Tmax 16–24 °C, RH I > 97%, RH II > 40%; staghead Tmax 20–29 °C, Tmin > 12 °C, RH I > 97% (confirm these limits against the original paper before the analysis).',
             'Do not use covariates in feature selection; use them only in the covariate models and to report results by stratum.'],
         check=['One covariate row per sample; no weather from after the flight date.'],
         out='Covariate table → 1.1, 2.9, 3.5, L8.',
         papers=[('Chattopadhyay et al. (2011)', 'Weather-based forecasting of white rust of Indian mustard: disease related to temperature and relative humidity over several sowings and seasons in India.', 'Temperature and humidity summaries and favourable-day counts as covariates of white rust (limits to be confirmed against the paper).'),
                 ('Zhang et al. (2014a)', 'Wheat powdery mildew; forecast from meteorological data alone and with remote sensing; adding remote sensing improved the forecast.', 'Weather covariates form the baseline against which the cameras are judged.'),
                 ('Bhattacharya and Chattopadhyay (2013)', 'Mustard rot; surface meteorology combined with satellite remote sensing.', 'Weather combined with sensor data for a mustard disease.'),
                 ('Blasch et al. (2023)', 'Wheat rusts; detection by UAV changed with the crop growth stage.', 'Growth stage recorded so that results can be reported by stage.')])

    step('A7', 'Biochemical and biophysical parameters', part=PART,
         what='Pigments, anthocyanin, protein, relative water content, membrane stability, gas exchange and leaf area index are measured on four dates.',
         why='They show what white rust does to the plant and explain the camera responses (Activity 1.7); they are not model inputs.',
         do=['Dates: 7 January (pre-symptomatic), 18 January, 8 February and 1 March 2027, on flight days.',
             'One designated subplot per plot, rotated so that each subplot position is sampled in 12 plots (position = plot number modulo 4, plus 1).',
             'Gas exchange on leaf L3 of one tagged plant of that subplot, 09:30–11:30 h, before the flight.',
             'Laboratory samples: L3 leaves of 3 untagged plants of the same subplot, kept cool and processed the same day.',
             'Leaf area index in all four subplots under diffuse light.'],
         check=['48 samples per parameter and date; LAI 192 per date.', 'Sample codes join to plot, subplot and date.'],
         out='Parameter table → 1.7, 3.1.',
         papers=[('Mishra et al. (2009)', 'White rust of Indian mustard; pathological and biochemical changes in infected compared with healthy plants.', 'Same pathogen and crop; biochemical parameters of infected vs healthy plants.'),
                 ('Calderón et al. (2013)', 'Verticillium wilt of olive; airborne fluorescence, temperature and narrow-band indices related to disease severity and to field physiological measurements.', 'Plant physiology measured to explain thermal and spectral signals.'),
                 ('Zarco-Tejada et al. (2018)', 'Xylella in olive; plant traits (pigments, fluorescence, temperature) retrieved from imagery changed before visible symptoms.', 'Pigments and gas exchange explain pre-symptomatic signals (7 January).'),
                 ('Baranowski et al. (2015)', 'Oilseed rape (~~Brassica napus~~) leaves infected by ~~Alternaria~~; hyperspectral and thermal responses.', 'Brassica leaf responses to a fungal disease.'),
                 ('Chatterjee et al. (2022)', 'White rust of Indian mustard; biochemical changes in infected plants in relation to the pathogenic variability of the pathogen.', 'Recent biochemical study of the same host and disease.'),
                 ('Yu et al. (2025)', 'Rice sheath blight; a dual-branch model that fused spectral and physiological signatures for early detection.', 'Physiological measurements analysed together with spectra.')])
    rows = [['Parameter (unit)', 'Method', 'Method reference'],
            ['Chlorophyll a, b (mg g^{−1} FW)', 'DMSO extraction; absorbance 645, 663 nm', 'Hiscox and Israelstam (1979); Wellburn (1994)'], ['Carotenoids (mg g^{−1} FW)', 'same extract; 470 nm', 'Lichtenthaler and Wellburn (1983); Wellburn (1994)'],
            ['Anthocyanin (mg L^{−1})', 'pH differential, 520 and 700 nm', 'Lee et al. (2005)'], ['Total protein (µg mg^{−1} FW)', 'Bradford dye binding, 595 nm', 'Bradford (1976)'],
            ['Relative water content (%)', '(FW − DW)/(TW − DW) × 100', 'Barrs and Weatherley (1962)'], ['Membrane stability index (%)', 'conductivity at 40 and 100 °C', 'Premachandra et al. (1990); Sairam et al. (1994)'],
            ['Photosynthesis, transpiration, stomatal conductance', 'LI-6400 portable photosynthesis system', 'Long and Bernacchi (2003)'], ['Leaf area index (m^{2} m^{−2})', 'plant canopy analyser, 1 reading above and 4 below', 'Bréda (2003); Goyal et al. (2021)']]
    tab('physio', rows=rows, caption='Parameters, methods and method references.', widths=[2800, 3600, 3200], size=16)

    step('A8', 'Independent test data at Bharatpur', part=PART,
         what='Research-farm plots and farmers\' fields with natural white rust at Bharatpur are flown with the same cameras and surveyed in the same way, to test the frozen IARI models.',
         why='A test on another site under natural infection shows whether the models transfer; these data are never used for training or tuning.',
         do=['Choose 8–10 fields covering healthy to severely diseased crops and the common varieties.',
             'Mark quadrats of subplot size (2.5 m × 1.5 m) with pegs and image-visible markers, record them with RTK GNSS; 15–20 quadrats per field.',
             'Fly the four cameras on 2–3 post-symptomatic dates (February–March) with the IARI flight settings.',
             'Survey 3 points per quadrat (Step A3) on the flight day and record covariates (variety, sowing date, stage, sprays, nearest weather station).'],
         check=['At least 300 quadrat-dates with all DI classes, including healthy.'],
         out='Independent test table → 2.11.',
         papers=[('Ma et al. (2026)', 'Rice blast; models built on 2023 data and tested on an independent 2024 data set from natural infection.', 'Independent test data never used for training.'),
                 ('Yuan et al. (2025)', 'Rice bacterial blight; UAV models carried to other areas and scales (UAV to satellite).', 'Transfer of UAV disease models to new fields.'),
                 ('Liu et al. (2026)', 'Wheat powdery mildew; a disease index developed on the ground and applied to UAV images of other fields and dates.', 'A model built in one setting applied to new fields.'),
                 ('Chattopadhyay et al. (2011)', 'White rust of mustard at several Indian locations including Bharatpur, related to weather.', 'Bharatpur is a known white rust site.')])

    step('A9', 'Glasshouse (pot) experiment', part=PART,
         what='A pot experiment with the same treatments gives leaf responses under controlled inoculation.',
         why='Controlled conditions separate the disease response from field variation and support the field results.',
         do=['Sow 23 November, 30 November, 7 December and 14 December 2026 × 3 varieties; 36 inoculated pots (R1–R3) and 12 healthy pots in a separate compartment.',
             'Inoculate on 4 January 2027 with 10 µL droplets of the suspension on the upper leaf surface; cover with polythene for 3 days (RH 80–90%, about 19 °C).',
             'At 2, 5, 8 and 11 DAI and then weekly: visual severity (0–6 scale) and ASD leaf spectra of the same leaves (Step A4 protocol).'],
         check=['Same identifiers and labels as in the field.'],
         out='Pot leaf data → comparison with field leaf responses (L5).',
         papers=[('Mishra et al. (2009)', 'Controlled inoculation of ~~Brassica juncea~~ with ~~Albugo candida~~; changes in infected leaves.', 'Same inoculation of the same host–pathogen system.'),
                 ('Mahlein et al. (2013)', 'Sugar-beet leaf diseases inoculated under controlled conditions; disease-specific indices from leaf spectra.', 'Leaf spectra under controlled inoculation.'),
                 ('Baranowski et al. (2015)', 'Oilseed rape leaves inoculated with ~~Alternaria~~ species under controlled conditions; hyperspectral and thermal imaging.', 'Brassica leaves under controlled infection.')])
