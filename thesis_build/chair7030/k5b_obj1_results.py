from k0_lib import *

MEANING = {'FD870': 'NIR plateau slope beyond the red edge (mesophyll scattering)', 'FD665': 'slope at the red chlorophyll absorption',
           'FD595': 'slope from the green peak towards the red (pigments)', 'REP': 'red-edge position (chlorophyll content)', 'FD1090': 'near-infrared slope (leaf structure)'}


def fix_t23(r):
    for row in r[1:]:
        if row[0] in MEANING and (not row[4].strip() or row[0] == 'FD1090'): row[4] = MEANING[row[0]]
    return r




def results():
    h2('4.4 Step 7 results: how the spectrum changes with disease')
    fig('spectra', 'f02_mean_spectra.png', '(a) Mean leaf reflectance (± SD) of each severity grade over 400–2400 nm (water bands shaded and kept); (b) first derivative at the red edge.', rep=5)
    read(shows='(a) The average reflectance spectrum of each grade with its spread; (b) a close-up of the first derivative between 500 and 800 nm.',
         how=['Each line is the mean of all leaves of one grade (dark green = grade 0, purple = grade 9); the shaded band around each line is ± 1 SD. Blue shading marks the water-absorption regions.',
              'Labels at the top mark the regions: VIS (visible), RE (red edge), NIR, SWIR-1 and SWIR-2.',
              'In (b) the tall peak near 700–720 nm is the red edge: its height is Dr and its wavelength is REP.'],
         found=['NIR plateau (750–1300 nm): grades 0 and 1 are highest (about 0.61 at 800 nm); the higher grades are lower (0.55–0.58).',
                'Red (around 680 nm): reflectance rises with grade, so the red trough becomes shallower.',
                'SWIR and water bands: reflectance rises with grade, most clearly in the water bands near 1450 and 1940 nm.',
                '(b) The red-edge peak becomes lower and moves to shorter wavelengths as grade increases.',
                'The SD bands overlap widely: individual leaves of different grades can have very similar spectra.'],
         means='All three expected effects of white rust are visible: chlorophyll loss (red and red edge), structural damage (NIR) and water loss (SWIR). The large overlap of the SD '
               'bands is the first warning that individual leaves of neighbouring grades will be hard to separate.',
         say='"Diseased leaves reflect less near-infrared, more red and more shortwave-infrared light, and the red edge shifts towards shorter wavelengths."')
    tab('bands', 23, widths=[1300, 1100, 1100, 1100, 1100, 1100, 1100, 1700], size=17, subs=True)
    read(shows='The mean reflectance of each grade at nine key wavelengths and the two red-edge parameters, with the change from grade 0 to grade 9.',
         how='The last column gives the percentage change between grade 0 and grade 9 (for REP, the change in nm).',
         found=['Largest relative increases: 1940 nm water band (+66%), 1450 nm water band (+49%), 680 nm red (+45%) and 2200 nm (+34%).',
                'Decreases: 760 nm (−11%) and 800 nm (−9.5%) on the NIR plateau; Dr −16%.',
                'REP falls from 709.0 nm (grade 0) to 701.3 nm (grade 9): a blue shift of 7.7 nm, almost step by step (708.5, 705.2, 703.5, 701.8 nm for grades 1–7).',
                'The green band (550 nm) hardly changes (+6%).'],
         means='The red-edge position is the most regular indicator: it moves monotonically with grade. The water bands show the largest relative change, which supports keeping them '
               'in the analysis of contact-probe data. A blue shift of this size (about 8 nm) is typical of chlorophyll loss in diseased leaves (Mahlein et al., 2013; Meng et al., 2020).',
         say='"The red-edge position moves 7.7 nm from 709 to 701 nm between healthy and grade-9 leaves, and the water bands change by 50–66%."')
    fig('fdfull', 'f03_fd_full.png', 'First derivative of the mean spectra of each grade over 400–2400 nm.', rep=6)
    read(shows='The slope of the mean spectrum of each grade across the full range.',
         how='Positive values mean reflectance is rising with wavelength, negative values that it is falling. Peaks mark the steepest parts of the spectrum.',
         found=['The red-edge peak near 720 nm is by far the largest and is lower for higher grades.',
                'Smaller differences appear at the green peak (around 520–570 nm), at the edges of the water bands (near 1380, 1450, 1870 nm) and in the SWIR-2.'],
         means='The derivative turns small changes of shape into visible peaks. It shows that the disease signal is not only in the red edge: the flanks of the water bands also respond, '
               'which is why derivative bands from the NIR and SWIR are selected later.',
         say='"The derivative makes the red edge and the water-band edges stand out; both respond to the disease."')
    fig('stage', 'f13_spectra_by_stage.png', 'Mean reflectance by grade within each growth stage.', rep=7)
    read(shows='The mean spectra of each grade drawn separately for the vegetative, flowering and pod-formation stages.',
         how='Compare the lines within one panel (the grade effect at a given stage) and between panels (the stage effect).',
         found=['Vegetative (n = 555): the grade lines almost coincide; these leaves are mostly grade 0–1, so there is little disease to see.',
                'Flowering (n = 1160): a clear grade effect – NIR falls and SWIR rises with grade.',
                'Pod formation (n = 615): SWIR and the water bands rise strongly with grade; on the NIR plateau the higher grades are slightly **higher**, the opposite of flowering.'],
         means='The SWIR/water-band increase is consistent wherever there is disease, but the direction of the NIR change depends on the stage. This is an important caution: NIR '
               'reflectance on its own is not a stable disease indicator, because leaf ageing and canopy development also change it. Indicators based on the red edge and the water bands are more robust.',
         caution='Growth stage and date are linked in this design (vegetative leaves only on the first two dates, pod formation only on the last two), so stage effects cannot be separated from date effects.',
         say='"The water-band signal is present at every stage with disease; the near-infrared change depends on the stage, so it is not a reliable indicator on its own."')
    fig('factor', 'f14_grade_by_factor.png', 'Mean leaf grade (± 95% confidence interval) by growth stage, variety, leaf position and sowing timing.', rep=8)
    read(shows='The average grade in each level of four factors, with 95% confidence intervals.',
         how='Bar height = mean grade; the error bar = 95% confidence interval; n = number of leaves. Non-overlapping error bars indicate a clear difference.',
         found=['Growth stage: vegetative 1.44, flowering 3.48, pod formation 4.47.',
                'Variety: V1 3.45, V2 3.37, V3 2.96 – V3 had somewhat less disease.',
                'Leaf position: L3 2.59, L5 3.35, LL 4.07 – disease increases down the plant.',
                'Sowing timing: D1 3.63, D2 3.39, D3 2.81, D4 3.04.'],
         means='The large stage differences mostly reflect the date (later dates = later stages = more disease). Leaf position is a genuine within-date effect: the lower leaves carry '
               'more disease. The variety and timing differences are smaller; the covariate model (Step 14) shows that, at the same crop age, the late sowing D4 actually had more disease.',
         say='"Disease increased with stage and down the plant; V3 had the least disease."')
    fig('corr', 'f04_corr_curves.png', 'Pearson correlation of reflectance and first derivative with the leaf grade (dotted lines: |r| = 0.3).', rep=9)
    read(shows='For every wavelength, how strongly reflectance (blue) and its first derivative (red) follow the grade across all 2330 leaves.',
         how='The curve gives r at each wavelength; above zero means the value rises with grade, below zero that it falls. Dotted lines at ±0.3 mark a moderate correlation. The two circles mark the strongest values.',
         found=['Reflectance peaks at 695 nm (r = +0.46): red reflectance rises with disease. It is negative across the NIR (about −0.3 to −0.4) and positive in the SWIR (up to about +0.38).',
                'The derivative reaches r = +0.62 at 800 nm (just beyond the red edge) and −0.56 at 720 nm (on the red-edge peak).',
                'The derivative curve changes sign many times; reflectance changes smoothly.'],
         means='The first derivative carries a stronger disease signal than reflectance (0.62 vs 0.46). The opposite signs at 720 and 800 nm describe the same event: the red-edge peak '
               'becomes lower and shifts to shorter wavelengths, so the slope falls at 720 nm and rises at 800 nm. This explains why derivative bands dominate the selected features.',
         say='"The derivative at 800 nm is the single best indicator (r = 0.62); the derivative is consistently stronger than plain reflectance."')

    h2('4.5 Step 7 results: effective ranges and optimal wavelengths')
    fig('maps', 'f05_ndsi_rsi_maps.png', 'R² of (a) NDSI and (b) RSI with the leaf grade for all band pairs (white contour: effective-range threshold; star: best pair).', rep=10)
    read(shows='For every combination of two wavelengths, how well the normalised difference (a) or ratio (b) of those two bands predicts the grade.',
         how='Each point of the map is one band pair (λ_{1} on the horizontal axis, λ_{2} on the vertical). Colour = R² with the grade (dark blue 0, dark red 0.36). The maps are symmetric '
             'about the diagonal. The white contour encloses the top 5% of pairs (R² ≥ 0.23); the star marks the best pair.',
         found=['No pair reached the planned threshold of R² = 0.5; the best was **(795, 805) nm with R² = 0.36** for both NDSI and RSI.',
                'The highest values form a narrow corner where one band lies in the visible/red edge and the other on the NIR shoulder (around 750–850 nm), and a second area within the SWIR (1400–1900 nm).',
                'The effective ranges defined by the contour were 515–1365, 1380–1395, 1405–1895 and 2020–2105 nm (292 bands at 5-nm spacing).'],
         means='Two-band indices capture at most about a third of the variation in leaf grade. The best pair is two very close bands on the NIR shoulder – in effect a measure of the slope '
               'there, which links it directly to the derivative at 800 nm. Because no pair reached R² 0.5, the fall-back rule (top 5%) was used, as planned in the methodology.',
         say='"The best two-band index is NDSI(795, 805) with R² 0.36; the useful band pairs lie at the red edge–NIR shoulder and in the shortwave infrared."')
    fig('shapcars', 'f06_shapcars.png', 'SHAP-CARS: (a) SHAP importance of all candidate bands, (b) choice of PLS components, (c) one CARS run, (d) selection frequency over 20 runs.', rep=11)
    read(shows='The four stages of the band selection.',
         how=['(a) Mean |SHAP| of each candidate band (red = derivative, blue = reflectance); the dashed line marks the top-40% cut.',
              '(b) Cross-validated error (RMSE) of PLS against the number of components; the red line marks the number chosen.',
              '(c) One CARS run: black = number of bands still kept, red = cross-validated error; the dotted line marks the iteration with the lowest error.',
              '(d) How often each band was selected in 20 CARS runs; the dashed line marks 50%.'],
         found=['(a) The largest SHAP values are derivative bands near 680–870 nm and near 1800 nm; reflectance bands contribute little.',
                '(b) The error fell steadily up to 15 components, so 15 were used.',
                '(c) CARS reduced about 110 bands to a few dozen within the first iterations; the error was lowest early (around iteration 5) and rose when too many bands were removed.',
                '(d) Twenty-three bands were selected in at least 70% of runs; the 15 most frequent (FD1090 and FD565 in every run) were kept, all of them derivatives.'],
         means='The model-based selection agrees with the correlation curves: the derivative carries the information. Repeating CARS 20 times and keeping only frequently chosen bands '
               'protects against the randomness of a single run.',
         say='"SHAP removed the uninformative bands, CARS chose the best combination, and over 20 runs 15 derivative bands were chosen consistently."')
    tab('ow', 24, widths=[2000, 2000, 1900, 2000, 1700], size=17)
    read(shows='The 15 optimal wavelengths with their type, spectral region, CARS selection frequency and SHAP importance.',
         how='"CARS frequency" = share of the 20 runs in which the band was selected; "mean |SHAP|" = its average contribution to the XGBoost predictions.',
         found=['All 15 are first-derivative bands: 4 in the visible (FD550, FD565, FD595, FD665), 10 in the NIR (760–1245 nm) and 1 in the SWIR (FD1660).',
                'The bands with the largest SHAP values are FD860 (0.110), FD810 (0.106) and FD1060 (0.089); FD1090 and FD565 were chosen in every run.'],
         means='The selected bands cover the green peak and red absorption (pigments), the NIR shoulder and plateau (structure) and one SWIR band (water/dry matter). A high CARS frequency '
               'and a high SHAP value are different things: a band can be chosen often because it adds unique information even if its average contribution is small.',
         say='"Fifteen derivative bands were chosen – mostly on the NIR shoulder, plus green, red and one shortwave-infrared band."')
    fig('ow', 'f07_optimal_wavelengths.png', 'Optimal wavelengths marked on the mean reflectance (a) and first-derivative (b) spectra.', rep=12)
    read(shows='Where the 15 selected bands lie on the average spectrum.',
         how='Red vertical lines mark the selected wavelengths; panel (a) has none because no reflectance band was selected.',
         found='The lines cluster around the green peak (550–595 nm), the red absorption (665 nm), the red-edge shoulder and NIR (760–1090 nm), with single bands at 1245 and 1660 nm.',
         means='The selection is physically sensible: it picks the slopes on both sides of the green peak, the red edge and the NIR plateau, and the flank of the 1450-nm water band. '
               'These are the regions a UAV hyperspectral camera must cover.',
         say='"The chosen bands sit exactly on the parts of the spectrum that respond to chlorophyll, leaf structure and water."')

    h2('4.6 Step 7 results: indices and the disease-specific feature set')
    fig('wri', 'f08_wri.png', 'White Rust Index (WRI) by grade: (a) distributions, (b) all leaves with mean ± SD.', rep=13)
    read(shows='The best three-band index found by the search, and how its value changes with grade.',
         how='(a) Violin and box plots of the index for each grade; (b) every leaf as a dot (slightly spread sideways), with the mean ± SD per grade in black.',
         found=['The search returned WRI = NDSI(780, 830) with a third-band weight w = 0, i.e. the third band (400 nm) adds nothing. Correlation with grade r = −0.59.',
                'The mean WRI falls steadily from about +0.003 (grade 0) to about −0.007 (grade 9), but the spread within each grade is large and the distributions overlap.',
                'The next best candidates were almost identical (|r| 0.592–0.595).'],
         means='For leaf spectra, a third band did not improve the best two-band contrast: the NIR-shoulder slope already carries the signal. The index orders the grades correctly on '
               'average, but a single leaf cannot be graded from it reliably because of the overlap.',
         say='"A three-band White Rust Index did not beat the two-band NIR-shoulder index; it ranks grades on average, but leaves overlap."')
    fig('icorr', 'f09_index_corr.png', 'Correlation among the indices kept after the |r| ≥ 0.95 filter.', rep=14)
    read(shows='How the 23 remaining indices correlate with each other.',
         how='Each cell is the correlation between two indices: dark red = +1, dark blue = −1, white = 0.',
         found=['The redundancy filter reduced 47 index features (41 published, 3 red-edge parameters, 3 data-driven) to 23.',
                'A large block of greenness and red-edge indices (RSI_best, HI, PSSR, REP, NDVI850, RDVI, PRI, MTVI2) still correlate at 0.7–0.9 with each other.',
                'DWSI-2, MCARI, PSSRc and TCARI are only weakly related to the others.'],
         means='Even after removing near-duplicates, many indices measure almost the same thing (greenness and the red edge). The few independent indices (DWSI-2, MCARI) are valuable '
               'because they add different information, which is exactly what ReliefF and the VIF check reward.',
         say='"Most indices tell the same greenness story; only a few, like DWSI-2, add something different."')
    fig('relief', 'f10_relief.png', 'ReliefF weights of the indices for detection and six grades, and RReliefF weights for the score (dark blue: top five, selected).', rep=15)
    read(shows='The ranking of the indices by ReliefF for each task.',
         how='Longer bar = more useful for separating neighbouring leaves of different classes (or different scores). Dark blue bars are the five selected.',
         found=['Detection: RSI_best, HI, REP, RVSI, DWSI-2.', 'Six grades: REP, RSI_best, HI, DWSI-2, RVSI.', 'Score: RSI_best, HI, MCARI, PRI, Dr.'],
         means='The same core – the best data-driven ratio (RSI_best), the Healthy Index (HI) and the red-edge position (REP) – is chosen for all tasks, supported by the disease–water '
               'stress index DWSI-2 and the red-edge stress index RVSI. For the score, pigment indices (MCARI, PRI) and the red-edge height (Dr) enter.',
         say='"ReliefF picked the same core indices for all three tasks: the NIR-shoulder ratio, the Healthy Index and the red-edge position."')
    fig('vif', 'f11_vif.png', 'Variance inflation factors of the disease-specific feature set.', rep=16)
    read(shows='The 11 features left after the variance-inflation check and their VIF.',
         how='Red = derivative band, green = vegetation index; the dashed line is the limit of 10.',
         found=['Twelve features were removed in turn because they overlapped with others, the largest first: FD855 (VIF 119), PRI (93), FD565 (91), FD810 (75), then FD860, RVSI, FD830, RSI_best, FD1660, HI, FD915, MCARI.',
                'The final 11 all have VIF below 10; the highest are FD595 (9.6), DWSI-2 (7.7) and REP (6.8).'],
         means='Several strong features (RSI_best, HI, FD810) were removed not because they are poor, but because their information is already contained in the remaining features. '
               'The final set is compact and each feature contributes something of its own.',
         say='"After removing overlap, 11 features remain – eight derivative bands and three indices – each carrying its own information."')
    tab('dsf', 25, widths=[1300, 1600, 900, 1400, 4400], size=17, fix=fix_t23, subs=True)
    read(shows='The disease-specific feature set: each feature, whether it is a derivative band or an index, its VIF, its correlation with grade and its physical meaning.',
         found=['Eight derivative bands (FD1090, FD1060, FD550, FD1245, FD870, FD760, FD665, FD595) and three indices (DWSI-2, Dr, REP).',
                'Strongest single correlations with grade: REP (−0.50), FD870 (+0.49), Dr (−0.38).'],
         means='The set covers pigments (FD550, FD595, FD665, Dr, REP), leaf structure (FD760, FD870, FD1060, FD1090) and water (FD1245, DWSI-2). It is the main input of all models in Objective 2.',
         say='"This is the disease-specific feature set: 11 features covering chlorophyll, leaf structure and water."')
    fig('dsfbox', 'f30_dsf_by_grade.png', 'Distribution of each disease-specific feature by grade.', rep=17)
    read(shows='Box plots of each of the 11 features for the six grades, with their correlation r.',
         how='Each box spans the middle 50% of leaves of a grade, the line inside is the median and the whiskers show the range.',
         found=['REP falls clearly with grade (medians from about 710 to 700 nm); FD870 rises; Dr falls.',
                'For most features the boxes of neighbouring grades overlap heavily – for example grades 3, 5 and 7 have very similar FD1245, FD760 and DWSI-2.'],
         means='Each feature shifts with grade on average, but no single feature separates neighbouring grades. This is why combinations of features are modelled, and why even the '
               'best models confuse neighbouring grades (Step 11).',
         say='"Every feature moves with the grade, but neighbouring grades overlap – combining features is necessary."')
    fig('pca', 'f12_pca.png', 'Principal component scores of leaf reflectance with 95% ellipses of each grade.', rep=18)
    read(shows='A two-dimensional summary of the full reflectance spectra: each dot is a leaf placed by its first two principal components.',
         how='PC1 (55.6% of the variation) and PC2 (32.4%) are the two directions in which the spectra vary most. Large dots are the grade centroids; ellipses contain 95% of the leaves of each grade.',
         found=['The grade centroids move in order from upper left (grades 0–1) towards lower right (grade 9).',
                'The ellipses overlap almost completely; the leaves form two clouds, which reflect differences between dates and stages rather than grades.'],
         means='The largest sources of variation in the spectra are not the disease: they are leaf and crop differences (stage, date, leaf position). The disease is a smaller, consistent '
               'shift within this variation. This is why supervised selection (SHAP-CARS, ReliefF) is needed rather than relying on the main directions of variation.',
         say='"Disease shifts the spectra in a consistent direction, but this shift is smaller than the natural differences between leaves and dates."')

