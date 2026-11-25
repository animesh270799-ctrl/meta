from dsl import *


def fix_t4(r):
    for row in r:
        if row[0].strip().lower() == 'all': row[1] = '33–94'
    return r


def add():
    h1('2. The experiment and the data')
    h2('2.1 Field layout and treatments')
    p('The 2025-26 experiment had 48 plots of 5 m × 3.5 m, separated by 0.5-m bunds and 2-m channels, in a field of 48 m × 24 m. Plots 1–12 formed the '
      '**healthy block**: they were sprayed with fungicide and stayed free of white rust. Plots 13–24, 25–36 and 37–48 were the three **unsprayed replications** '
      '(R3, R2 and R1), left to natural infection. No artificial inoculation was made; the disease came from the natural inoculum of the season.')
    p('Every block held the same 12 treatment combinations: three varieties (V1, V2, V3) × four sowing dates (D1–D4). The four sowing dates gave crops of '
      'four different ages when the epidemic developed at the end of January 2026 (Table below). This is useful: it shows how crop age during the epidemic '
      'affects the disease, and it makes the data more varied than a single sowing would.')
    tab('design', 2, widths=[1500, 1700, 2100, 2000, 2700])
    read(shows='The four sowing dates, the crop age they represent at the end of January 2026, and the crop age of each sowing at the four leaf-sampling dates.',
         how='Each row is one sowing timing. "Treatment crop age" is the age that defines the treatment (50, 40, 30, 20 days after sowing, DAS); the last column gives the '
             'age at 11 Feb, 24 Feb, 3 Mar and 13 Mar 2026.',
         found='At the time of sampling the crops ranged from 33 DAS (D4 on 11 February) to 94 DAS (D1 on 13 March). D1 was always the oldest crop and D4 the youngest.',
         means='Crop age at sampling is the natural time variable of this experiment. Because the disease increases with time, any model must be checked for whether it '
               'only learns crop age (or date) instead of the leaf signal – this is why the covariate baseline (Chapter 6.5) was built.',
         say='"Four sowing dates gave four crop ages under the same natural epidemic; crop age at sampling ran from 33 to 94 days."')
    box('Why natural infection matters for the analysis.', 'With natural infection there is no inoculation date, so time is measured from sowing (days after sowing). '
        'All unsprayed plots received the same inoculum and weather; differences between them come from crop age, variety and chance. The healthy block shows what a '
        'disease-free leaf of the same age looks like.', kind='method')

    h2('2.2 Measuring the leaf spectra and scoring the leaves')
    p('On each of the four sampling dates, leaves were measured in all 48 plots with the ASD FieldSpec spectroradiometer fitted with the contact probe and leaf clip. '
      'The probe has its own halogen lamp, so the readings do not depend on the sun, clouds or time of day (Milton et al., 2009). Reflectance was recorded from 350 to '
      '2500 nm at 1-nm steps; the files were already corrected for the small jumps at the joins of the three detectors ("splice correction").')
    p('Three leaf positions were sampled: the third (L3) and fifth (L5) fully expanded leaf from the top and the lowest green leaf (LL). Each measured leaf was '
      'scored on the 0–9 white rust scale (grades 0, 1, 3, 5, 7, 9). Nine spectra of 11 February were labelled L4, which is not a sampled position; they were removed, '
      'leaving **2330 leaf spectra**.')
    tab('leafpos', 3, widths=[1500, 900, 900, 900, 1200, 1100, 2700])
    read(shows='How many leaf spectra were recorded on each date and at each leaf position.',
         how='Rows are dates; L3, L5 and LL are the leaf positions; "Leaves per plot" gives the median and range of leaves measured in one plot on that date.',
         found='The number of leaves rose from 419 on 11 February to 723 on 13 March. The lowest green leaf (LL) was sampled less on the first two dates (54 and 108 leaves) '
               'and fully on the last two (216 and 241). Every date covered all 48 plots, with a median of 10–15 leaves per plot.',
         means='The data set is large (2330 leaves) but not perfectly balanced: later dates contribute more leaves, and lower leaves are under-represented on the early dates. '
               'This was kept in mind when reading results by date and leaf position (Chapter 8.6).',
         say='"2330 leaves over four dates and 48 plots, about 10–15 leaves per plot per date."')
    tab('dates', 4, widths=[1500, 1500, 2500, 1100, 1300, 1700], fix=fix_t4)
    read(shows='The crop age, growth stages, number of leaves, mean grade and percentage of diseased leaves on each date.',
         how='"Mean grade" is the average of the leaf grades (0–9); "Diseased leaves (%)" is the share of leaves with grade above 0. The last row pools all dates.',
         found='The disease rose quickly between the first two dates: the mean grade went from 0.67 (11 Feb) to 3.39 (24 Feb), then to 3.51 (3 Mar) and 4.43 (13 Mar). '
               'The share of diseased leaves jumped from 44.6% to 83.3% and then stayed at 81–85%. Over all dates, 76.3% of leaves were diseased and the mean grade was 3.26. '
               'Vegetative leaves occurred only on the first two dates and pod-formation leaves only on the last two.',
         means='Two points matter for the analysis. First, the epidemic was well developed: most leaves after mid-February were diseased, so the data are rich in disease '
               'but contain few healthy leaves from the unsprayed plots after the first date. Second, growth stage and date are tied together, so a difference between stages '
               'cannot be separated from a difference between dates.',
         caution='The "All" row of the original report showed the crop age as 6–36 (a left-over from an earlier draft); the correct range is 33–94 days after sowing, as shown here.',
         say='"The epidemic built up between 11 and 24 February; after that more than 80% of leaves were diseased and the mean grade kept rising to 4.4."')
    tab('grades', 5, widths=[1500, 1000, 1000, 1000, 1000, 1000, 1000, 1500])
    read(shows='How the 2330 leaves are distributed over the six grades.',
         how='The first row gives counts, the second the percentage of all leaves.',
         found='Grade 0 (552 leaves, 23.7%) and grade 5 (533, 22.9%) were the most common; grade 9 was the rarest (132 leaves, 5.7%).',
         means='The classes are unequal. A model that ignored this would favour the common grades and rarely predict grade 9. Therefore every model used **balanced class weights**, '
               'and the main metric is **macro-F1**, which gives every grade the same importance regardless of its size.',
         say='"Grade 9 is rare – only 6% of leaves – so all models were trained with class weights and judged with a metric that treats all grades equally."')
    fig('dataset', 'f01_dataset.png', 'Leaves by (a) sampling date, (b) growth stage, (c) variety and (d) leaf position, coloured by severity grade.', rep=2)
    read(shows='Four bar charts that split the 2330 leaves by date, growth stage, variety and leaf position; each bar is coloured by grade (dark green = grade 0 to purple = grade 9).',
         how='The height of a bar is the number of leaves; the coloured segments show how many of them fall in each grade; n above each bar is the total.',
         found=['(a) On 11 February the bar is almost all green (grades 0 and 1); from 24 February the orange, red and purple segments (grades 5–9) dominate.',
                '(b) Vegetative leaves are mostly grade 0–1 (mean grade 1.44); flowering (3.48) and pod-formation leaves (4.47) carry most of the severe disease.',
                '(c) The three varieties have similar grade mixtures (mean 3.45, 3.37 and 2.96 for V1, V2, V3).',
                '(d) Disease increases down the plant: mean grade 2.59 (L3), 3.35 (L5) and 4.07 (LL).'],
         means='The disease level depends strongly on time (date and stage) and on leaf position, and only a little on variety. The higher disease on lower leaves agrees with '
               'the biology of white rust: older, lower leaves stay longer in the humid micro-climate near the ground and were exposed to the inoculum for longer.',
         say='"Disease rose with date and was highest on the lowest leaves; the varieties differed only slightly."')

    h2('2.3 Weather and covariates')
    p('Daily weather from 1 December 2025 to 20 March 2026 came from the IARI agro-meteorological observatory: maximum and minimum temperature, rainfall, morning (RH I) and '
      'afternoon (RH II) relative humidity, wind, sunshine and evaporation. For each sampling date the seven days before the date were summarised; the window ends the day '
      'before sampling, so no weather from the future enters any model ("no look-ahead").')
    p('Because infection was natural, the number of **favourable days** was counted from each sowing date to the day before sampling, using the white rust criteria of '
      'Chattopadhyay et al. (2011): for leaf infection a maximum temperature of 16–24 °C with morning humidity above 97% and afternoon humidity above 40%; for the staghead '
      'phase a maximum temperature of 20–29 °C, minimum above 12 °C and morning humidity above 97%. Leaf-level covariates were crop age (DAS), sowing timing, variety and '
      'growth stage (vegetative, flowering, pod formation coded 1–3 following the BBCH ranges; Lancashire et al., 1991).')
    tab('covdate', 6, widths=[900, 1000, 1000, 1000, 1000, 1000, 1200, 1700, 1100], size=16)
    read(shows='The weather of the seven days before each sampling date and the number of favourable days.',
         how='T max and T min are the mean daily maximum and minimum temperatures; RH I and RH II are morning and afternoon humidity; "Favourable leaf days since sowing" '
             'gives one value for each sowing date (D1 / D2 / D3 / D4).',
         found=['The weather warmed and dried during sampling: 7-day T max rose from 23.3 to 34.5 °C and afternoon humidity fell from 50% to 33–36%. Almost no rain fell.',
                'Only one favourable leaf-infection day fell within the 7 days before 11 February and none before the other dates.',
                'Since sowing, D1 and D2 had 17 favourable days, D3 13 and D4 7; no staghead-favourable day occurred.'],
         means='The infection happened earlier, during the cool, humid spell of December–January (the last favourable day was 4 February). What was measured in February–March is '
               'the expression and spread of that infection as the crop aged, under weather that was becoming unfavourable. The earlier sowings were exposed to more favourable '
               'days, which helps explain why D1 and D2 had more disease.',
         say='"Infection happened in the cool, humid weeks of December and January; during sampling the weather became hot and dry."')

    h2('2.4 Data organisation and quality control')
    p('Before any analysis, the data were organised and checked in seven steps:')
    nl('**Parsing:** the four Excel files were read and the 2330 leaf columns kept; columns holding plot averages were skipped because the analysis is at leaf level.',
       '**Treatments:** each plot number was joined to the field layout (block, sowing date, variety); the variety written in the files agreed with the layout for all 48 plots.',
       '**Labels:** the grade was taken from the score; for detection a leaf is "diseased" when its grade is above 0. All 378 leaves of the sprayed healthy block were grade 0; '
       '1952 leaves came from the unsprayed plots.',
       '**Leaf positions:** only L3, L5 and LL were kept (the nine L4 spectra were removed).',
       '**Derived fields:** crop age at sampling (DAS) and the growth-stage code.',
       '**Checks:** grades only 0, 1, 3, 5, 7, 9; wavelengths 350–2500 nm at 1 nm; no missing values; reflectance between 0.026 and 0.935; all 48 plots on every date; 3–30 leaves '
       'per plot and date (median 15).',
       '**Folds:** every leaf was assigned to the validation fold of its plot (Chapter 3).')
    box('Why this matters.', 'Quality control is the reason the results can be trusted: a wrong variety, a mislabelled leaf position or a corrupted spectrum would silently '
        'distort every later step. All checks passed; the only change was the removal of the nine L4 spectra.', kind='key')

    h2('2.5 Three prediction tasks')
    tab('tasks', 7, widths=[1700, 3600, 2200, 2100])
    read(shows='The three questions the models answer and how each is evaluated.',
         how='Task A has two classes, task B six ordered classes, task C a number from 0 to 9.',
         found='Detection compares 552 healthy with 1778 diseased leaves; six grades uses all six classes; the score treats the grade as a continuous number.',
         means='The three tasks are three levels of detail. Detection is what a farmer or an early-warning system needs first; six grades follow the visual scale used by '
               'pathologists; the score is the most natural output for a sensor, because disease severity is continuous. Each task needs its own metric (Chapter 6.4).',
         say='"I ask three questions of each model: is the leaf diseased, which of the six grades is it, and what is its severity score?"')

    # ------------------------------------------------------------------ validation
    h1('3. Validation design: how the models were tested fairly')
    p('The single most important methodological decision is how the data are split into training and test parts. If leaves from the same plot appear in both parts, '
      'a model can recognise the plot (its soil, micro-climate, variety and timing) instead of the disease, and the test accuracy is inflated. This is called '
      '**leakage**. Spatially blocked cross-validation avoids it by keeping whole blocks out of training (Roberts et al., 2017).')
    tab('cvcard', 8, widths=[2200, 7400], size=17, boldfirst=True)
    read(why='Leaves of one plot are not independent; random leaf-level splits would place near-copies in training and test.',
         done=['Fold 1 tests replication R1 (plots 37–48) plus healthy plots 7, 2, 10, 12; fold 2 tests R2 plus 5, 8, 4, 1; fold 3 tests R3 plus 3, 9, 11, 6.',
               'The healthy block has no replications of its own, so its 12 plots were rotated: each test fold receives four healthy plots, and every healthy plot is tested once.',
               'Inside each training part, all feature selection, subset selection and tuning use an inner GroupKFold(3) split by plot – the test replication is never touched.'],
         means='Every leaf is predicted exactly once by a model that never saw its replication. The reported accuracy is therefore an honest estimate of how the method would '
               'work on a new replication of the same experiment.',
         say='"I train on two replications and test on the third, three times; the test plots are never used for choosing features or settings."')
    tab('folds', 9, widths=[1400, 2000, 2400, 1800, 2000])
    read(shows='The three outer folds: which replication and healthy plots are tested in each, and how many leaves are in the test and training parts.',
         how='Each row is one round of training and testing.',
         found='The test parts are of similar size (764–798 leaves), and each training part has about 1530–1570 leaves.',
         means='The three folds are balanced, so the results do not depend on one unusually small or large fold. The spread of a metric across the three folds (shown as "± SD") '
               'is used throughout as the yardstick for whether two models really differ.',
         say='"Three balanced folds of about 770 test leaves each; the fold-to-fold spread tells me which differences are real."')
    box('Nested validation in one picture.', ['**Outer loop (3 folds):** hold out one replication + four healthy plots → this is the final test.',
                                             '**Inner loop (inside the training part):** GroupKFold(3) by plot → used to choose wavelengths, indices, the feature subset and the model settings.',
                                             'Only after these choices are fixed is the model applied once to the held-out replication. This "nested" design prevents selection bias (Varma and Simon, 2006; Cawley and Talbot, 2010).'], kind='method')
