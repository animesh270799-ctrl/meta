from k0_lib import *


def fix_t4(r):
    for row in r:
        if row[0].strip().lower() == 'all': row[1] = '33–94'
    return r


def add():
    h1('2. Steps 1–4: the experiment and the data')
    p('The first four steps produce one checked table of 2330 leaves, each with its spectrum, its grade, its plot and treatment, and its covariates. Nothing is learned in these steps; '
      'they use ALL leaves.')
    tab('obj', 1, widths=[2600, 3900, 3100])
    read(shows='The two thesis objectives answered with the 2025-26 leaf data and the questions behind them.',
         how='One row per objective; the right column lists the outputs that answer it.',
         means='Objective 1 explains the signal (Step 7); Objective 2 measures how well models use it (Steps 8–15). Objective 3, pre-symptomatic detection, needs pre-symptomatic dates, which were not sampled in 2025-26.',
         say='"One season of leaf spectra answers two questions: where white rust shows in the spectrum, and how accurately it can be detected and graded."')
    fig('workflow', 'f00_workflow.png', 'Workflow of the analysis from data collection to discussion.', rep=1)
    read(shows='The 16 boxes of the analysis workflow as drawn in the report.',
         how='Follow the arrows; colours group the phases: green = data collection and checks, dark blue = pre-processing, light blue = Objective 1, yellow = validation design, purple = Objective 2, red = covariate baseline and discussion.',
         means='The boxes of this figure correspond to the steps of this protocol. The yellow validation box is Step 5; in the 70:30 analysis it comes before every learning step.',
         say='"This is the road map; the rest of the talk walks through it box by box."')

    # ---------------------------------------------------------------- Step 1
    h2('2.1 Step 1 – Field experiment and treatments')
    card('card1', '1', 'Field experiment and treatments',
         'Create plots with known treatments and disease contrast, so that leaf spectra can be linked to disease and to plot, variety and crop age.',
         'Not a data step; it defines the 48 plots used by every later step.',
         'Field 48 m × 24 m at IARI, New Delhi; 3 varieties (V1–V3); 4 sowing dates (D1–D4).',
         steps('Lay out 48 plots of 5 m × 3.5 m (0.5-m bunds, 2-m channels).',
               'Assign plots 1–12 to the fungicide-sprayed healthy block and 13–24 (R3), 25–36 (R2), 37–48 (R1) to the unsprayed replications.',
               'Place the 12 treatment combinations (3 varieties × 4 sowing dates) once in every block (plot plan in a1_prep.py).',
               'Sow D1 9 Dec, D2 18 Dec, D3 27 Dec 2025 and D4 9 Jan 2026 (50, 40, 30 and 20 days old at the end of January).',
               'Leave infection to the natural inoculum of the season; spray only the healthy block.'),
         'No inoculation; crop age at sampling (days after sowing, DAS) is the time variable.',
         'Plot plan (plot → block, timing, variety) → Step 4 (labels) and Step 5 (the split is made by plots and blocks).',
         'Plot plan dictionary LAY in a1_prep.py.',
         'Saharan et al. (2014); Chattopadhyay et al. (2011) for white rust epidemiology.',
         '8',
         'Write the new plot plan (plot number → block, treatment). If there is no healthy block, Step 5 splits only the unsprayed blocks.')
    tab('design', 2, widths=[1500, 1700, 2100, 2000, 2700])
    read(shows='The four sowing dates, the crop age that defines each treatment, and the crop age of each sowing on the four sampling dates.',
         how='Each row is one sowing timing; the last column gives the age on 11 Feb, 24 Feb, 3 Mar and 13 Mar 2026.',
         found='At sampling the crops were 33 DAS (D4, 11 February) to 94 DAS (D1, 13 March) old.',
         means='Because disease rises with time, a model could look accurate by learning crop age rather than the leaf signal. This is why Step 14 builds a model from crop age, timing, variety, stage and weather alone.',
         say='"Four sowing dates gave four crop ages under the same natural epidemic, 33 to 94 days at sampling."')

    # ---------------------------------------------------------------- Step 2
    h2('2.2 Step 2 – Leaf spectra and visual grades')
    card('card2', '2', 'Leaf spectra and visual grades',
         'Record, for single leaves, a reflectance spectrum and the visual white rust grade of the same leaf.',
         'ALL: every measured leaf of the 48 plots on the four dates.',
         'ASD FieldSpec with contact probe and leaf clip (own halogen lamp).',
         steps('On each date (11 Feb, 24 Feb, 3 Mar, 13 Mar 2026) visit all 48 plots.',
               'In each plot select leaves at three positions: L3 and L5 (third and fifth fully expanded leaf from the top) and LL (lowest green leaf).',
               'Clamp the leaf in the leaf clip and record reflectance 350–2500 nm at 1 nm (splice-corrected export).',
               'Score the same leaf on the 0–9 scale (grades 0, 1, 3, 5, 7, 9).',
               'Save one Excel file per date: one column per leaf, seven header rows (wavelength, plot, variety, growth stage, healthy/diseased, leaf level, score).'),
         'Contact probe: no sun, sky, soil or atmosphere in the signal (Milton et al., 2009). 3–30 leaves per plot and date (median 15).',
         '2339 leaf columns read by a0_load.py → Step 4 (nine L4 spectra removed → 2330).',
         'a0_load.py → meta_raw.csv, X_leaf.npy.',
         'Milton et al. (2009); Bock et al. (2010) on visual scoring.',
         '9, 12',
         'Keep the same header rows (or edit a0_load.py). For UAV data the "leaf" becomes a plot or sub-plot spectrum with its ground-truth score.')
    tab('leafpos', 3, widths=[1500, 900, 900, 900, 1200, 1100, 2700])
    read(shows='Leaf spectra per date and leaf position.',
         how='Rows are dates; "Leaves per plot" gives the median and range of leaves per plot on that date.',
         found='419 leaves on 11 February rising to 723 on 13 March; the lowest leaf (LL) was sampled less on the first two dates (54 and 108).',
         means='Later dates contribute more leaves. This matters for Step 5: the split is required to keep the date mix of the test set close to the mix of all leaves.',
         say='"2330 leaves over four dates and 48 plots, about 10–15 leaves per plot and date."')
    tab('dates', 4, widths=[1500, 1500, 2500, 1100, 1300, 1700], fix=fix_t4)
    read(shows='Crop age, growth stages, number of leaves, mean grade and share of diseased leaves on each date.',
         found='Mean grade 0.67 (11 Feb) → 3.39 → 3.51 → 4.43 (13 Mar); diseased leaves 44.6% → 83.3% → 81.2% → 85.1%.',
         means='The epidemic built up quickly between the first two dates. Growth stage and date are tied: vegetative leaves only on the first two dates, pod formation only on the last two.',
         caution='The "All" row of the report printed 6–36 days; the correct crop age is 33–94 days after sowing.',
         say='"Between 11 and 24 February most leaves became diseased; after that the grades kept rising."')
    tab('grades', 5, widths=[1500, 1000, 1000, 1000, 1000, 1000, 1000, 1500])
    read(shows='The number and percentage of leaves in each grade.',
         found='Grade 0: 552 (23.7%); grade 5: 533 (22.9%); grade 9 the rarest: 132 (5.7%).',
         means='Classes are unequal, so all classifiers use balanced class weights and the main metric is macro-F1, in which every grade counts equally. Step 5 also keeps the grade mix of the test set close to this table.',
         say='"Grade 9 is rare, so models were weighted and judged with a metric that treats all grades equally."')
    fig('dataset', 'f01_dataset.png', 'Leaves by (a) sampling date, (b) growth stage, (c) variety and (d) leaf position, coloured by severity grade.', rep=2)
    read(shows='The 2330 leaves split by date, stage, variety and leaf position, coloured by grade.',
         found=['(a) 11 February is mostly grade 0–1; from 24 February grades 5–9 dominate.',
                '(b) mean grade 1.44 vegetative, 3.48 flowering, 4.47 pod formation.',
                '(c) varieties similar (mean 3.45, 3.37, 2.96).', '(d) disease increases down the plant: 2.59 (L3), 3.35 (L5), 4.07 (LL).'],
         means='Disease depends strongly on time and leaf position, little on variety. These are the factors used later to check robustness (Step 13).',
         say='"Disease rose with date and was highest on the lowest leaves."')

    # ---------------------------------------------------------------- Step 3
    h2('2.3 Step 3 – Weather and covariates')
    card('card3', '3', 'Weather and covariates',
         'Describe the epidemic and prepare the sensor-free information (calendar, crop and weather) used by the covariate baseline.',
         'ALL leaves receive their covariates; only the unsprayed leaves are later modelled with them (Step 14).',
         'Daily IARI observatory data 1 Dec 2025 – 20 Mar 2026 (T max, T min, RH I, RH II, rain, wind, sunshine, evaporation).',
         steps('For every sampling date take the 7 days that END THE DAY BEFORE the date (no look-ahead) and compute mean T max, T min, RH I, RH II, wind, sunshine, evaporation and total rain.',
               'Count favourable leaf-infection days (T max 16–24 °C, RH I > 97%, RH II > 40%) and staghead days (T max 20–29 °C, T min > 12 °C, RH I > 97%) from each sowing date to the day before sampling.',
               'Compute crop age (DAS = sampling date − sowing date) and the growth-stage code (1 vegetative, 2 flowering, 3 pod formation).',
               'Attach variety and timing from the plot plan.'),
         'Criteria of Chattopadhyay et al. (2011); stage code after the BBCH ranges (Lancashire et al., 1991).',
         'One covariate row per leaf → Step 14; disease-progress table → discussion.',
         'a5_extra.py (weather_season.csv, disease_progress.csv); a11_covariate.py (cov2_covariates_by_date.csv).',
         'Chattopadhyay et al. (2011); Lancashire et al. (1991); De Wolf and Isard (2007).',
         '10, 24',
         'Use the weather of the new site and season; keep windows ending the day before each sampling date.')
    tab('covdate', 6, widths=[900, 1000, 1000, 1000, 1000, 1000, 1200, 1700, 1100], size=16)
    read(shows='Weather of the 7 days before each date and the favourable-day counts.',
         found=['7-day T max rose from 23.3 to 34.5 °C and afternoon humidity fell from 50% to 33–36%; almost no rain.',
                'Since sowing, D1 and D2 had 17 favourable leaf days, D3 13 and D4 7; no staghead day.'],
         means='Infection took place during the cool, humid spell of December–January (last favourable day 4 February). During sampling the weather was unfavourable.',
         say='"Infection happened in December and January; during sampling it was getting hot and dry."')
    fig('weather', 'f15_weather_progress.png', 'Weather of the season with sowing dates, favourable leaf-infection days and the four sampling dates (boxes: mean grade and % diseased leaves); natural infection.', rep=4)
    read(shows='The whole season: temperature (top), rain and humidity (bottom), sowing dates and sampling dates.',
         how='Green triangles = days meeting all leaf-infection criteria; dotted green lines = sowings; purple lines = sampling dates with mean grade and % diseased.',
         found='17 favourable days between 18 December and 4 February; T max above 25 °C from mid-February and about 35 °C by mid-March.',
         means='What was measured in February–March is the expression and spread of infections that started earlier.',
         say='"The favourable weather came before sampling; what I measured is that infection becoming visible."')
    tab('weather', 22, widths=[800, 1100, 900, 900, 900, 900, 900, 900, 900, 1100], size=16)
    read(shows='Disease progress and the 7-day weather before each date in one table.',
         found='Mean grade 0.67 → 4.43; diseased 45% → 85%; favourable days since the first sowing stay at 17 for every date.',
         means='With four dates the 7-day weather is the same for every leaf of a date, so in this season weather cannot be separated from the date. Step 14 therefore uses crop age (DAS, DAS²) as the time effect in the interpretable model.',
         say='"The weather describes the epidemic, but with four dates it cannot be tested separately from the date."')

    # ---------------------------------------------------------------- Step 4
    h2('2.4 Step 4 – Data organisation, labels and checks')
    card('card4', '4', 'Data organisation, labels and quality checks',
         'Turn the raw files into one checked leaf table with labels for the three tasks.',
         'ALL.',
         'meta_raw.csv and X_leaf.npy from Step 2; plot plan from Step 1.',
         steps('Join every leaf to its plot: block, timing, variety (check that the variety in the file equals the plot plan: 48/48 agreed).',
               'Remove the nine L4 spectra of 11 February (not a sampled position) → 2330 leaves.',
               'Labels: grade = score (0, 1, 3, 5, 7, 9); diseased = grade > 0 (task A); six grades (task B); score 0–9 (task C).',
               'Mark unsprayed plots (R1–R3) and the sprayed healthy block (all 378 of its leaves are grade 0).',
               'Checks: grades valid; 2151 bands 350–2500 nm; no missing values; reflectance 0.026–0.935; all 48 plots on every date.'),
         'Class labels encoded 0–5 for the six grades.',
         'meta.csv (one row per leaf) → Step 5 (split), Step 6 (features).',
         'a1_prep.py.',
         'Kuhn and Johnson (2013) on data preparation.',
         '11, 13',
         'Re-run the same checks; a failed check stops the pipeline (assert statements in a1_prep.py).')
    tab('tasks', 7, widths=[1700, 3600, 2200, 2100])
    read(shows='The three prediction tasks and how each is evaluated.',
         found='A: 552 healthy vs 1778 diseased leaves; B: six ordered classes; C: a number 0–9.',
         means='Each task needs its own metric (Step 11). Detection is the first need of an early-warning system; the score is the most natural sensor output because severity is continuous.',
         say='"I ask three questions: is the leaf diseased, which grade is it, and what is its severity score?"')
    box('Output of Steps 1–4.', 'One table of 2330 leaves × (spectrum 350–2500 nm, plot, block, variety, timing, date, leaf position, growth stage, DAS, grade, diseased flag) plus the weather covariates. '
        'All checks passed; the only change to the raw data was the removal of the nine L4 spectra.', kind='key')
