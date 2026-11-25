from dsl import *


def key_ideas():
    h1('Key ideas in plain language')
    p('Eight ideas from statistics and machine learning are used throughout the analysis. They are explained here once, without formulas, so that the later chapters can be read easily.')
    ideas = [
        ('Training and testing', 'A model learns from one part of the data (training) and is judged on another part it has never seen (testing). Only the test result says how well the '
         'model would work on new leaves; the training result is always too optimistic.'),
        ('Over-fitting', 'A flexible model can memorise the training data, including its noise, instead of learning the general pattern. It then looks excellent on training data and poor '
         'on new data. Simple models, feature selection, early stopping and honest testing protect against it.'),
        ('Cross-validation and blocking', 'Instead of one split, the data are split several times so that every leaf is tested once. When samples are grouped (leaves within plots), whole '
         'groups must stay together in training or test – otherwise the model recognises the group, not the disease. Here whole replications were held out.'),
        ('Nested selection', 'Any choice made with the data – which wavelengths, which features, which settings – is itself a kind of training. It must be made using only the training part, '
         'otherwise the test result is inflated ("selection bias"). Here every choice was repeated inside each training part.'),
        ('Class imbalance', 'When some classes are rare (grade 9 = 6% of leaves), a model can score well by ignoring them. Class weights make errors on rare classes count more, and macro-F1 '
         'gives every class equal weight in the evaluation.'),
        ('Correlation is not the whole story', 'A feature can correlate with the grade only because both follow time (date, crop age). This is called confounding. The covariate baseline '
         'measures how much the calendar alone predicts, so that the spectra are credited only with what they add.'),
        ('Uncertainty', 'Every result would change a little with another replication. The spread across the three folds (± SD) and bootstrap confidence intervals show how large that '
         'variation is; differences smaller than it should not be called real.'),
        ('Interpretability', 'A good model should use the inputs in a way that makes physical sense. SHAP values show which features drive each prediction and in which direction, so that '
         'the model can be checked against plant physiology.'),
    ]
    for t, d in ideas:
        h3(t); p(d)
    box('Why these ideas matter for this analysis.', 'Leaf-level disease data are small, grouped by plot, unbalanced across grades and strongly tied to the calendar. Each of these '
        'features can make a model look better than it is. The design of this analysis – blocked and nested validation, class weights, macro-F1, the covariate baseline and SHAP – '
        'addresses each of them, which is why the reported numbers can be presented with confidence.', kind='key')


def storyline():
    h1('Suggested presentation storyline (about 20 minutes)')
    p('The full document has more material than a single meeting can cover. The sequence below presents the analysis in about 20 minutes with 12 items; the remaining tables and '
      'figures are available for questions.')
    tab('story', rows=[['Step', 'Show', 'Key sentence', 'Minutes'],
                       ['1', 'Title and objectives ({T:obj})', 'One season of leaf spectra answers two questions: where the disease shows in the spectrum, and how well it can be detected and graded.', '1'],
                       ['2', 'Workflow ({F:workflow})', 'Sixteen steps, with selection and modelling inside a leakage-free validation design and a no-sensor baseline.', '1'],
                       ['3', 'Data ({T:dates}, {F:dataset})', '2330 leaves, 48 plots, four dates; the epidemic built up between 11 and 24 February.', '2'],
                       ['4', 'Weather ({F:weather})', 'Infection happened in the cool, humid weeks of December–January; sampling was in warm, dry weather.', '1.5'],
                       ['5', 'Validation ({T:folds})', 'Train on two replications, test on the third; every choice made inside the training part.', '1.5'],
                       ['6', 'Mean spectra ({F:spectra}, {T:bands})', 'Less NIR, more red and SWIR; the red edge moves 7.7 nm towards the blue.', '2'],
                       ['7', 'Correlation ({F:corr})', 'The derivative at 800 nm is the best single indicator (r = 0.62).', '1'],
                       ['8', 'Selected features ({F:ow}, {T:dsf})', '15 derivative bands and an 11-feature disease-specific set covering chlorophyll, structure and water.', '2'],
                       ['9', 'Model comparison ({F:comp})', 'Detection 0.79 macro-F1; six grades 0.36; score R² 0.46; ML and DL within the noise.', '2'],
                       ['10', 'Confusion matrix ({F:cm})', 'Most six-grade errors are one grade away; QWK 0.63, 75% within one grade.', '1.5'],
                       ['11', 'Covariate baseline ({F:covgain})', 'The calendar predicts much; spectra add a confirmed gain for severity.', '2'],
                       ['12', 'Conclusions and next steps', 'Reliable detection, ranked severity, wavelengths for the UAV camera, Objective 3 in 2026-27.', '1.5']],
        caption='A 20-minute storyline: what to show and what to say.', widths=[700, 2300, 5600, 1000], size=16)
    read(shows='A suggested order for presenting the analysis, with the item to show, the one sentence to say, and the time to spend.',
         how='The items refer to the tables and figures of this document; each has a "Say to the chairman" sentence in its explanation panel.',
         means='The storyline moves from the question and the data, through the evidence that the disease is visible in the spectrum, to how well models use it and how honestly this was tested.',
         say='"I will show twelve items in about twenty minutes and keep the rest for questions."')
    h2('The whole analysis in one table')
    tab('onetable', rows=[['Step', 'Method', 'Main result', 'Meaning'],
                          ['Data', '2330 leaf spectra, 48 plots, 4 dates, natural infection', 'Mean grade 0.67 → 4.43; 76% of leaves diseased', 'A well-developed epidemic with all grades represented'],
                          ['Validation', 'Leave-one-replication-out, nested selection', '3 balanced folds (764–798 test leaves)', 'Honest estimate for a new replication'],
                          ['Response', 'Mean and derivative spectra, correlation', 'REP 709.0 → 701.3 nm; FD800 r = 0.62', 'Chlorophyll loss, structural damage and water loss are visible'],
                          ['Band pairs', 'NDSI/RSI R² maps', 'Best NDSI(795, 805), R² 0.36', 'Two bands explain at most a third of the variation'],
                          ['Wavelengths', 'SHAP-CARS', '15 derivative bands', 'Derivatives carry the signal'],
                          ['Indices', 'WRI, ReliefF', 'WRI = NDSI(780, 830); RSI_best, HI, REP selected', 'A third band adds nothing at leaf level'],
                          ['Feature set', 'VIF < 10', '11 features (8 derivatives, DWSI-2, Dr, REP)', 'Compact and non-redundant'],
                          ['Detection', '10 models', 'SVM macro-F1 0.792, AUC 0.897', 'Reliable'],
                          ['Six grades', '10 models', 'ConvNeXt 0.360, QWK 0.633, 75% within one', 'Order captured, exact grade not'],
                          ['Score', '10 models', 'XGBoost R² 0.459, RMSE 2.04', 'Useful for ranking; compressed to the middle'],
                          ['DT-EDNet', 'Configurations and ablation', '0.337 (grades); modules ±0.02', 'No advantage on leaf pseudo-images'],
                          ['Robustness', 'Strata, LOVO, LOTO', 'Similar across varieties, positions, timings', 'The signal is general'],
                          ['Baseline', 'Covariate-only models, bootstrap', 'ΔS +0.043 (grades), +0.083 R² (score)', 'Spectra add real information on severity']],
        caption='The whole analysis in one table.', widths=[1300, 2500, 3000, 2800], size=16)
    read(shows='Every step of the analysis with its method, its main result and its meaning, in one place.',
         means='Read down the "Meaning" column for the argument of the whole study in thirteen lines.',
         say='"If you remember one table, it is this one."')


def extra():
    h1('Appendix F. Additional result tables')
    p('These tables give numbers that lie behind the figures but are not printed in the report. They are computed from the same pooled test predictions and data.')
    tab('xdate', rows=[['Date', 'Leaves', 'Sprayed healthy block', 'Unsprayed plots', 'Grade 0', 'Grade 1', 'Grade 3', 'Grade 5', 'Grade 7', 'Grade 9', 'Grade 0 among unsprayed (%)'],
                       ['11 Feb 2026', '419', '72', '347', '232', '147', '33', '7', '0', '0', '46.1'], ['24 Feb 2026', '540', '90', '450', '90', '97', '123', '146', '62', '22', '0.0'],
                       ['03 Mar 2026', '648', '108', '540', '122', '119', '132', '140', '77', '58', '2.6'], ['13 Mar 2026', '723', '108', '615', '108', '26', '142', '240', '155', '52', '0.0'],
                       ['All', '2330', '378', '1952', '552', '389', '430', '533', '294', '132', '8.9']],
        caption='Leaves by date: healthy block, unsprayed plots and grade counts.', widths=[1300, 700, 1000, 1000, 700, 700, 700, 700, 700, 700, 1400], size=15)
    read(shows='The grade distribution on each date, and the share of healthy leaves among the unsprayed plots.',
         found=['On 11 February, 46% of the unsprayed leaves were still healthy and none was grade 7 or 9.',
                'On the later dates almost no unsprayed leaf was healthy (0–2.6%); healthy leaves then came only from the sprayed block.',
                'Grade 9 leaves appeared from 24 February and were most frequent on 3 March (58).'],
         means='This table explains the result of the covariate baseline for detection: inside the unsprayed plots, "healthy" almost means "11 February", so the date alone separates '
               'most healthy from diseased leaves.',
         say='"After the first date there were practically no healthy leaves in the unsprayed plots."')
    tab('xdet', rows=[['Group', 'Level', 'Leaves', 'Macro-F1', 'OA'],
                      ['Growth stage', 'Vegetative / Flowering / Pod formation', '555 / 1160 / 615', '0.757 / 0.790 / 0.774', '0.757 / 0.847 / 0.870'],
                      ['Variety', 'V1 / V2 / V3', '773 / 793 / 764', '0.797 / 0.779 / 0.798', '0.838 / 0.824 / 0.833'],
                      ['Leaf position', 'L3 / L5 / LL', '869 / 842 / 619', '0.794 / 0.778 / 0.787', '0.809 / 0.830 / 0.864'],
                      ['Date', '11 Feb / 24 Feb / 3 Mar / 13 Mar', '419 / 540 / 648 / 723', '0.670 / 0.825 / 0.778 / 0.772', '0.690 / 0.885 / 0.838 / 0.867'],
                      ['Sowing timing', 'D1 / D2 / D3 / D4', '723 / 580 / 540 / 487', '0.802 / 0.810 / 0.776 / 0.772', '0.853 / 0.852 / 0.804 / 0.805']],
        caption='Detection (SVM) by group.', widths=[1500, 2900, 1900, 1900, 1400], size=15)
    tab('xdetdate', rows=[['Date', 'Leaves', 'Healthy leaves', 'Specificity', 'Sensitivity'],
                          ['11 Feb 2026', '419', '232', '0.845', '0.497'], ['24 Feb 2026', '540', '90', '0.900', '0.882'],
                          ['03 Mar 2026', '648', '122', '0.844', '0.837'], ['13 Mar 2026', '723', '108', '0.741', '0.889']],
        caption='Detection (SVM): sensitivity and specificity on each date.', widths=[2000, 1500, 2000, 2000, 2100], size=16)
    read(shows='How detection performed in each group and on each date.',
         found=['Detection is stable across varieties, leaf positions and sowing timings (macro-F1 0.77–0.81).',
                'On 11 February only half of the diseased leaves were found (sensitivity 0.50), while healthy leaves were recognised well (0.85).',
                'From 24 February sensitivity was 0.84–0.89; specificity was lowest on 13 March (0.74).'],
         means='Of the 94 diseased leaves missed on 11 February, 72 were grade 1 – very early symptoms with little spectral change. Detection becomes reliable once lesions are established. '
               'On 13 March, some healthy-block leaves were called diseased, possibly because ageing (senescence) produces spectral changes similar to disease.',
         say='"Very early, grade-1 leaves are hard to detect; once lesions develop, more than 85% of diseased leaves are found."')
    tab('xscore', rows=[['Group', 'Level', 'RMSE (grades)', 'R²'],
                        ['Growth stage', 'Vegetative / Flowering / Pod formation', '1.57 / 2.14 / 2.23', '0.33 / 0.40 / 0.28'],
                        ['Variety', 'V1 / V2 / V3', '2.08 / 2.08 / 1.96', '0.47 / 0.45 / 0.44'],
                        ['Leaf position', 'L3 / L5 / LL', '1.88 / 2.06 / 2.24', '0.48 / 0.43 / 0.38'],
                        ['Date', '11 Feb / 24 Feb / 3 Mar / 13 Mar', '1.35 / 2.05 / 2.25 / 2.17', '−0.77 / 0.35 / 0.38 / 0.31'],
                        ['Sowing timing', 'D1 / D2 / D3 / D4', '2.04 / 2.13 / 2.01 / 1.96', '0.47 / 0.44 / 0.44 / 0.45']],
        caption='Severity score (XGBoost) by group.', widths=[1700, 3400, 2500, 2000], size=15)
    read(shows='How the severity score performed in each group.',
         found=['R² is 0.43–0.48 for varieties and timings, but lower within a single stage or date (0.28–0.40), and negative on 11 February.',
                'The RMSE is smallest on 11 February (1.35) and in the vegetative stage (1.57), where the grades are low.'],
         means='R² within a group is always lower than overall, because each group covers a narrower range of grades. On 11 February the leaves were almost all grade 0–1, so even a small '
               'error is large compared with the tiny spread of grades and R² becomes negative – the RMSE shows that the absolute error was actually the smallest.',
         say='"The score error is smallest early in the season; R² is low within a date only because the grades vary little within it."')
    tab('xerr', rows=[['Model', 'Exact grade', 'Within one grade', 'Three or more grades off'],
                      ['ConvNeXt V2-Atto', '0.389', '0.755', '0.078'], ['SVM', '0.403', '0.743', '0.082'], ['XGBoost', '0.383', '0.751', '0.079'],
                      ['DT-EDNet', '0.392', '0.739', '0.091'], ['RF', '0.388', '0.734', '0.081'], ['DNN-F1', '0.382', '0.722', '0.097']],
        caption='Size of the six-grade errors (share of the 2330 leaves).', widths=[2600, 2300, 2300, 2400], size=16)
    read(shows='How far off the six-grade predictions were.',
         found='About 39% of leaves were placed in the exact grade, about 74% within one grade, and only 8–10% three or more grade steps away.',
         means='Large errors are rare. The difference between the models lies mostly in the near-misses; for practical use the "within one grade" rate is the relevant number.',
         say='"Only about one leaf in eleven is badly misgraded."')
    tab('xshrink', rows=[['Observed grade', '0', '1', '3', '5', '7', '9'],
                         ['Mean predicted score (XGBoost)', '1.21', '2.34', '3.49', '4.13', '4.86', '5.27'],
                         ['Mean error (predicted − observed)', '+1.21', '+1.34', '+0.49', '−0.87', '−2.14', '−3.73'],
                         ['RMSE within the grade', '1.63', '1.98', '1.65', '1.70', '2.54', '4.00'],
                         ['Leaves', '552', '389', '430', '533', '294', '132']],
        caption='Severity score (XGBoost): mean prediction and error for each observed grade.', widths=[3400, 1000, 1000, 1000, 1000, 1000, 1200], size=16)
    read(shows='The prediction and error of the score model for each true grade.',
         found='Low grades are over-predicted by about 1.2–1.3 grade units; grade 7 is under-predicted by 2.1 and grade 9 by 3.7. The error is largest for grade 9 (RMSE 4.0).',
         means='This is the shrinkage seen in the predicted-versus-observed figure, in numbers. A simple calibration (stretching predictions back to the 0–9 range) could reduce the '
               'systematic part of the error, but it cannot remove the overlap between leaves; severe leaves will remain the hardest to quantify.',
         say='"The score under-estimates severe leaves – a grade-9 leaf is predicted at about 5 on average."')
    tab('xtransfer', rows=[['Held-out group', 'Leaves', 'Six grades macro-F1', 'Six grades OA', 'Score RMSE', 'Score R²'],
                           ['Variety V1', '773', '0.373', '0.408', '2.11', '0.45'], ['Variety V2', '793', '0.392', '0.419', '1.93', '0.53'], ['Variety V3', '764', '0.341', '0.410', '1.93', '0.46'],
                           ['Timing D1', '723', '0.368', '0.386', '2.23', '0.37'], ['Timing D2', '580', '0.314', '0.364', '2.17', '0.42'], ['Timing D3', '540', '0.337', '0.417', '2.06', '0.41'],
                           ['Timing D4', '487', '0.396', '0.448', '1.91', '0.48']],
        caption='Transfer tests (random forest): results on the held-out variety or sowing timing.', widths=[2000, 1100, 1800, 1500, 1500, 1700], size=16)
    read(shows='The complete results of the leave-one-variety-out and leave-one-timing-out tests.',
         found='Held-out varieties: macro-F1 0.34–0.39 and R² 0.45–0.53. Held-out timings: macro-F1 0.31–0.40 and R² 0.37–0.48.',
         means='The results on unseen groups match the cross-validated results (macro-F1 0.35, R² 0.45–0.46). The models do not depend on one variety or sowing date.',
         say='"On a variety or sowing date never seen in training the models perform as in cross-validation."')


def chart_guide():
    h1('How to read the chart types used')
    p('Eight kinds of chart appear in this document. A one-paragraph guide to each saves explanation during the presentation.')
    for t, d in [
        ('Mean spectrum with SD band', 'A line for the average reflectance of a group at every wavelength, with a shaded band of ± 1 standard deviation. Where the bands of two groups overlap, '
         'individual leaves of the two groups can look the same even if their averages differ.'),
        ('Correlation curve', 'For each wavelength, the correlation r between a spectral value and the grade (−1 to +1). Peaks show where the spectrum follows the disease most closely; the sign shows the direction.'),
        ('Band-pair (R²) map', 'A square in which every point is a combination of two wavelengths, coloured by how well an index made from them predicts the grade. Bright areas are useful band combinations.'),
        ('Box plot and violin plot', 'The box covers the middle 50% of values, the line inside is the median, the whiskers show the spread; a violin adds the shape of the distribution. Boxes that overlap mean the groups are hard to separate.'),
        ('Confusion matrix', 'A table with the true class in rows and the predicted class in columns. The diagonal holds the correct predictions; cells next to the diagonal are near-misses; distant cells are gross errors.'),
        ('ROC curve', 'Sensitivity plotted against the false-alarm rate for every possible decision threshold. A curve hugging the upper-left corner is good; the diagonal is chance. The area under it (AUC) summarises it in one number.'),
        ('Radar (spider) chart', 'Several metrics on axes radiating from a centre; each model is a polygon. Bigger polygons are better, and the shape shows where a model is strong or weak.'),
        ('Forest (interval) plot', 'Points with horizontal bars for an estimate and its 95% confidence interval. If the bar does not cross zero, the effect or gain is statistically clear.')]:
        h3(t); p(d)


def index_groups():
    h1('Appendix G. What each group of vegetation indices measures')
    p('The 44 published features of {T:indices} fall into five groups. For each group, this appendix explains what it measures, how it responded to white rust in these data, and why.')
    groups = [
        ('Greenness and structure indices', 'NDVI, NDVI850, SR, RVI, GNDVI, RDVI, MSR, OSAVI, TVI, MTVI2',
         'They contrast near-infrared with red (or green) reflectance and respond to the amount of green tissue and leaf structure.',
         'Moderate negative correlations (r −0.43 to −0.51) for the red-based indices; GNDVI was weak (−0.15) because green reflectance changed little.',
         'Disease raises red and lowers NIR reflectance, so every NIR/red contrast falls. They are useful, but they also respond to leaf age and stage, so they are not specific to white rust.'),
        ('Pigment indices', 'PSSRa, PSSRb, PSSRc, SIPI, NPCI, PSRI, ARI, PRI, NPQI, MCARI, TCARI, VIgreen, GI',
         'They target chlorophyll, carotenoids or anthocyanins through bands where each pigment absorbs.',
         'PSSRb (−0.53) and ARI (+0.53) were among the strongest indices; PRI −0.46; MCARI, TCARI and PSSRc were weak (|r| ≤ 0.08).',
         'Chlorophyll loss around the pustules lowers the chlorophyll-sensitive ratios; the rise of ARI and PSRI reflects the relative increase of other pigments in damaged and senescing tissue.'),
        ('Red-edge indices and parameters', 'CIrededge, NDRE, MTCI, REP, Dr, REarea',
         'They describe the position, height and area of the red edge, which depend closely on chlorophyll content.',
         'REP (−0.50), MTCI (−0.49), CIrededge and NDRE (−0.48 to −0.49), REarea (−0.48), Dr (−0.38).',
         'The red edge shifts towards shorter wavelengths and flattens as chlorophyll is lost. REP was selected by ReliefF for every task and is the most regular single indicator.'),
        ('Water indices', 'WI, WBI, NDWI, MoistSI, NDII',
         'They use the water absorption features near 970, 1240 and 1600 nm.',
         'Moderate correlations (|r| 0.37–0.40): drier tissue in diseased leaves.',
         'Infection damages cells and the tissue loses water, which raises reflectance in the water-sensitive bands. Their contribution is real but smaller than that of the red edge.'),
        ('Disease and stress indices', 'DWSI-1 to DWSI-5, HI, RVSI, RBI, NDBI',
         'Indices proposed specifically for diseases (sugarcane rust, sugar-beet diseases, rice blast) that combine pigment, red-edge and water bands.',
         'HI (−0.54) and RVSI (+0.56) were the strongest published indices overall; DWSI-2 was weakly correlated (+0.14) but carried independent information and entered the final feature set.',
         'Indices designed for other leaf diseases transfer partly to white rust, because the underlying changes (chlorophyll loss, red-edge stress, water loss) are similar. DWSI-2 shows that a weak correlation alone does not make a feature useless.')]
    for name, members, what, found, why in groups:
        h2(name)
        read(shows=f'**Members:** {members}. {what}', found=found, means=why)
