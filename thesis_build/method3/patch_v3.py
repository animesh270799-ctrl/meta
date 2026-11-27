"""Revision 3: second-stage (independent) validation at Bharatpur research farms and farmers' fields."""
def patch(f, reps):
    s = open(f).read()
    for a, b in reps:
        n = s.count(a)
        assert n == 1, (f, n, a[:90])
        s = s.replace(a, b)
    open(f, 'w').write(s)

# ------------------------------------------------------------------ body
A7 = '''STEP('A7', 'Second-stage validation data at Bharatpur (research farms and farmers\\' fields)',
     'Models tested only inside the IARI field may not work on other soils, varieties, management and natural epidemics. Independent data from another site are needed for a second-stage validation.',
     'Research farm(s) and farmers\\' fields at Bharatpur, Rajasthan, with natural white rust; the same four cameras, calibration panels and ground control points; the same severity key and scorer.',
     'Bharatpur validation dataset (quadrat-dates with images of all four cameras, severity grade and covariates) → second-stage validation (Activity 2.7).',
     ['Sites: research-farm plots and farmers\\' fields with natural white rust in the same season (rabi 2026-27), chosen to cover healthy to severely diseased canopies and the common local varieties.',
      'Sampling units: in every field mark validation quadrats of the same size as an IARI subplot (2.5 m × 1.5 m) with corner pegs and image-visible markers, recorded with an RTK GNSS receiver, away from field borders and bunds.',
      'Size: aim for at least 300 quadrat-dates in total (for example 8–10 farmers\\' fields and research-farm plots × 15–20 quadrats × 2–3 post-symptomatic flight dates in February–March), with every severity grade represented, including healthy quadrats.',
      'Flights: the same four cameras and flight settings as at IARI (30 m, 11:00–14:00 h, about 85% forward and 80% side overlap, reflectance panels and ground control points on every flight); if possible add one flight before symptoms with the same quadrats revisited later.',
      'Ground truth: score the canopy of every quadrat with the same 0–9 key (Conn et al., 1990), by the same scorer, on the day of the flight.',
      'Covariates (as in Step A6): variety, sowing date, growth stage (BBCH), days since the first symptoms were seen, fungicide sprays of the farmer, and daily weather from the nearest agrometeorological observatory or automatic weather station.',
      'Healthy reference: where possible, keep a fungicide-protected strip of the main variety at the research farm, so that features that need a healthy reference can also be tested.'],
     'Independent validation on naturally infected fields from another site and year: Ma et al. (2026); importance of testing on independent locations: Roberts et al. (2017), Ploton et al. (2020); Bharatpur as a white rust site for weather-based forecasting: Chattopadhyay et al. (2011); UAV disease monitoring of smallholder fields: Liu et al. (2026); transfer of UAV disease models to new areas: Yuan et al. (2025).',
     note='The Bharatpur data are never used for feature selection, tuning or training. They are used only once, for the second-stage validation of the final models.')
'''
patch('mf3_body.py', [
 ("# ---------------------------------------------------------------- B\nH2('Activity B – Image pre-processing')",
  A7 + "\n# ---------------------------------------------------------------- B\nH2('Activity B – Image pre-processing')"),
 ("['A. Field experiment, ground truth and datasets', 'A1–A6', 'labelled subplot list; ASD leaf spectra; covariates; post- and pre-symptomatic datasets']",
  "['A. Field experiment, ground truth and datasets', 'A1–A7', 'labelled subplot list; ASD leaf spectra; covariates; post- and pre-symptomatic datasets; Bharatpur validation dataset']"),
 ("['ASD leaf spectra', '3 plants per subplot × leaves L3, L5, LL on every flight date (1728 leaf spectra per date)'],",
  "['ASD leaf spectra', '3 plants per subplot × leaves L3, L5, LL on every flight date (1728 leaf spectra per date)'], ['Validation', 'first stage: IARI field (leave-one-replication-out, nested); second stage: Bharatpur research farms and farmers\\' fields (independent, natural infection, at least 300 quadrat-dates)'],"),
 ("    ['Sequential floating forward selection, hyper-parameter tuning, early stopping', 'yes', 'inner folds only'], ['Final evaluation', 'yes', 'test replication, once']],",
  "    ['Sequential floating forward selection, hyper-parameter tuning, early stopping', 'yes', 'inner folds only'], ['Final evaluation', 'yes', 'test replication, once'], ['Second-stage validation (Bharatpur)', 'yes', 'once, with frozen final models; never used for selection, tuning or training']],"),
])
s = open('mf3_body.py').read()
s = s.replace("'Six rules apply to every activity.'", "'Six rules apply to every activity.'")
s = s.replace("    'The same folds are used for all sensor sets and all models, so that their accuracies are directly comparable.'])",
              "    'The same folds are used for all sensor sets and all models, so that their accuracies are directly comparable.',\n    'Validation has two stages: first inside the IARI field (leave-one-replication-out, nested), then on independent data from research farms and farmers\\' fields at Bharatpur with frozen models.'])", 1)
open('mf3_body.py', 'w').write(s)

# ------------------------------------------------------------------ objectives
ACT27 = '''H2('Activity 2.7 – Second-stage validation at Bharatpur')
P('The first-stage validation (Activity F, leave-one-replication-out inside the IARI field) chooses the models and estimates their accuracy on new plots of the same field. The second stage tests the final models on independent data from research farms and farmers\\' fields at Bharatpur (Step A7), with other soils, varieties, management and a natural epidemic ([[F:twostage]]).')
FIG('twostage', 'g28_twostage.png', 'Two-stage validation: first stage inside the IARI field, second stage on independent Bharatpur data with frozen models.', 560)
STEP('2.7.1', 'Final models trained on all IARI data and frozen',
     'Models for an independent test must be fixed before the test data are seen.',
     'All IARI post-symptomatic samples (1920 per camera); the selection and tuning procedure of Objectives 1 and 2.',
     'Frozen final models with their selected features, hyper-parameters and standardisation constants → Steps 2.7.2–2.7.3.',
     ['Repeat feature selection and tuning on all IARI data with grouped inner cross-validation (folds by plot), exactly as in the first stage.',
      'Train the final models on all IARI data: the best machine-learning model and the best deep-learning model of each task, for the three best sensor sets, the full set (S15) and the best low-cost set without the hyperspectral camera.',
      'Store the selected features, hyper-parameters, standardisation means and standard deviations, and the trained weights; nothing is changed afterwards.'],
     'Final model refitted on all development data after nested validation: Cawley and Talbot (2010), Kuhn and Johnson (2013).')
STEP('2.7.2', 'Processing of the Bharatpur data with the same steps',
     'The validation data must pass through exactly the same processing, otherwise differences in processing would look like model errors.',
     'Bharatpur images, quadrat polygons, severity grades and covariates (Step A7).',
     'Bharatpur feature tables in the same layout as the IARI tables → Step 2.7.3.',
     ['Apply Activities B–D unchanged: calibration, mosaics, quality control, co-registration, resampling, quadrat means and feature extraction.',
      'Build the vegetation mask with the same procedure (Activity C) on the Bharatpur images, because soils and weeds differ; this uses no labels.',
      'Compute only the features selected for the frozen models; standardise them with the IARI constants (frozen).',
      'Features that need a healthy reference (difference from healthy plots, healthy-normalised features) are used only where a fungicide-protected strip exists; otherwise models without these features are used (canopy minus air temperature and the normalised relative canopy temperature need no healthy reference).'],
     'Processing fixed on the development data and applied to new data: Kuhn and Johnson (2013); same-sensor protocols across sites: Aasen et al. (2018).')
STEP('2.7.3', 'Application and evaluation of the frozen models',
     'Shows how accurate the models are on new fields and how much accuracy is lost compared with the first stage.',
     'Frozen models; Bharatpur feature tables and severity grades.',
     'Second-stage accuracy tables and the loss of accuracy from stage 1 to stage 2 → conclusions on transferability.',
     ['Predict every Bharatpur quadrat-date once with each frozen model; no retraining or re-tuning.',
      'Compute the same metrics as in Activity 2.4 (overall accuracy, kappa, weighted kappa, macro-F1, AUC; R², RMSE, RPD).',
      'Report the results for research farms and farmers\\' fields separately, by variety and by growth stage, and the difference from the first-stage accuracy.',
      'As a second, clearly labelled result, re-standardise the features with the means and standard deviations of the Bharatpur data (no labels used) to show how much of any loss comes from a simple shift between sites.',
      'Test the covariate models (Step 2.5.5) on Bharatpur weather as well; this is the first test of the weather effect outside the IARI season data.'],
     'Independent external test after internal validation: Ma et al. (2026); spatial transfer and loss of accuracy at new locations: Ploton et al. (2020), Roberts et al. (2017); cross-scale transfer of UAV disease models: Yuan et al. (2025).')
TAB('twostaget', [['Item', 'First stage (internal)', 'Second stage (independent)'], ['Data', 'IARI field, 48 plots, 13 dates', 'Bharatpur research farms and farmers\\' fields'],
    ['Infection', 'artificial inoculation (10 January 2027)', 'natural epidemic'], ['Design', 'leave-one-replication-out, nested', 'frozen final models applied once'],
    ['Used for', 'feature selection, tuning, model choice, accuracy on new plots', 'accuracy on new fields, varieties and management'], ['Varieties', 'PM 26, Pusa Vijay, PM 37', 'local varieties (recorded)']],
    'The two validation stages.', [2000, 3600, 3706])
STEP('2.7.4', 'Severity maps of farmers\\' fields',
     'Farm-level maps show whether the models are useful where decisions are made.',
     'Frozen best models; Bharatpur images.', 'Severity maps of the farmers\\' fields with the scored quadrats overlaid → reporting.',
     ['Apply the best model of each task to the whole vegetated area of each field in quadrat-sized cells.', 'Overlay the scored quadrats and their grades to show agreement and errors.'],
     'UAV disease maps of smallholder fields: Liu et al. (2026); severity maps from UAV models: Abdulridha et al. (2023), Liu et al. (2024).')

'''
patch('mf3_obj.py', [
 ("H1('5. Objective 3 – Prediction of white rust at the pre-symptomatic stage')", ACT27 + "H1('5. Objective 3 – Prediction of white rust at the pre-symptomatic stage')"),
 ("    ['2.6 Robustness and maps', '2.6.1–2.6.3', 'results by treatment; transfer tests; severity maps']], 'Activities of Objective 2.',",
  "    ['2.6 Robustness and maps', '2.6.1–2.6.3', 'results by treatment; transfer tests; severity maps'], ['2.7 Second-stage validation at Bharatpur', '2.7.1–2.7.4', 'accuracy of frozen models on independent research-farm and farmers\\' field data; farm maps']], 'Activities of Objective 2.',"),
])
s = open('mf3_obj.py').read()
s = s.rstrip('\n') + '''
STEP('3.5.4', 'Second-stage validation of the pre-symptomatic models',
     'Early-warning models also need an independent test, but pre-symptomatic labels require a flight before symptoms and a later visit of the same quadrats.',
     'Bharatpur quadrats flown before symptoms and scored later (Step A7); a fungicide-protected healthy strip for the healthy-plot normalisation.',
     'Second-stage accuracy of the pre-symptomatic models, where the data allow → conclusions on early warning.',
     ['Apply the frozen pre-symptomatic models (trained on all IARI pre-symptomatic data) to quadrats flown before symptoms and labelled from their later status.', 'Use the protected strip as the healthy reference; where no early flight or healthy reference exists, the pre-symptomatic models are validated in the first stage only, and this is stated.'],
     'Ma et al. (2026); Zhu et al. (2017); Zarco-Tejada et al. (2018).')
'''
open('mf3_obj.py', 'w').write(s)

# ------------------------------------------------------------------ end
patch('mf3_end.py', [
 (" ['A6', 'field book, weather records',", " ['A7', 'Bharatpur research farms and farmers\\' fields', 'independent validation dataset (images, grades, covariates)', '2.7, 3.5.4'],\n ['A6', 'field book, weather records',"),
 (" ['2.6.1–2.6.3', 'best models', 'robustness results; maps', 'conclusions'],", " ['2.6.1–2.6.3', 'best models', 'robustness results; maps', 'conclusions'],\n ['2.7.1–2.7.4', 'all IARI data; Bharatpur data', 'frozen final models; second-stage accuracy; farm maps', 'conclusions'],"),
 (" ['All results come from one season.', 'Stated as a limitation; leave-one-variety-out and leave-one-timing-out tests used as internal transfer tests.', 'Ma et al. (2026); Roberts et al. (2017)']],",
  " ['All results came from one site and one season.', 'Second-stage validation with frozen models on independent research-farm and farmers\\' field data at Bharatpur (Activity 2.7); leave-one-variety-out and leave-one-timing-out tests kept as internal transfer tests; transfer to other seasons still to be tested.', 'Ma et al. (2026); Roberts et al. (2017); Ploton et al. (2020)']],"),
 (" ['Leaf spectra', 'not collected',", " ['Validation', 'IARI field only', 'two stages: IARI field (internal) and Bharatpur research farms and farmers\\' fields (independent)', 'user request; transferability'],\n ['Leaf spectra', 'not collected',"),
 ("    ['6', 'Objective 3; synthesis and writing', 'earliest detection day; risk maps; thesis chapters']], 'Month-wise plan.', [1000, 5000, 3306])",
  "    ['6', 'Objective 3; second-stage validation at Bharatpur (Activity 2.7); synthesis and writing', 'earliest detection day; risk maps; independent validation results; thesis chapters']], 'Month-wise plan.', [1000, 5000, 3306])"),
 ("    ('How can these results be used with satellite data?',",
  "    ('How do you know the models work outside the IARI field?', 'Validation has two stages: leave-one-replication-out inside the IARI field to choose and assess the models, then frozen final models tested once on independent research-farm and farmers\\' field data from Bharatpur with natural infection, as the DT-EDNet study did with an independent naturally infected dataset (Ma et al., 2026; Ploton et al., 2020).'),\n    ('How can these results be used with satellite data?',"),
])
print('patched v3')
