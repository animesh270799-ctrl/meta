from k0_lib import *
import pandas as pd, json
A = '/home/user/meta/thesis_build/asd7030/data/'
INFO = json.load(open(MYFIG + '/inner_info.json')); SS = json.load(open(MYFIG + '/split_search.json'))


def add():
    h1('3. Step 5: the grouped, stratified 70:30 split')
    p('Step 5 is the most important design decision of the analysis. It decides which leaves may be used to build the models and which leaves are kept back to test them. '
      'Everything that follows depends on it, so this chapter explains it in full: why a split is needed, why whole plots are split, how the 15 test plots were chosen, '
      'and how the training plots are divided again inside the model steps.')

    h2('3.1 Why the leaves must be split, and why by whole plots')
    p('A model is always more accurate on the leaves it was trained on than on new leaves. To know how it will work on new leaves, some leaves must be kept out of training and '
      'used only for testing. With a single division into a training set and a test set this is called a **hold-out** design; 70:30 means that about 70% of the data train and 30% test. '
      'A test share of 20–30% is the usual rule of thumb (Gholamy et al., 2018); Joseph (2022) showed that the best share depends on the number of model parameters.')
    p('The leaves of one plot are not independent. They share soil, micro-climate, variety, sowing date and the same local inoculum, and they were measured on the same days. If leaves were '
      'assigned to training and test at random, almost every test leaf would have "brothers" from the same plot in training. A model could then recognise the plot rather than the '
      'disease, and the test accuracy would be too high. This is called **leakage**. The remedy is to split by **groups**: all leaves of a plot go to the same side (Roberts et al., 2017). '
      'For remote-sensing data, Kattenborn et al. (2022) found random splits up to 28% more optimistic than spatially blocked ones, and Karasiak et al. (2022) showed that ignoring spatial '
      'dependence inflates the accuracy of classification maps.')
    p('Within the grouped design the split is also **stratified**: the healthy (sprayed) plots and the unsprayed plots are split separately, and the test plots are spread over the '
      'replications, varieties and sowing dates, so that the test set is a fair miniature of the whole experiment (Kuhn and Johnson, 2013).')
    rows = [['Design', 'What goes to the test set', 'Leaves of one plot in both sets?', 'Number of test sets', 'Used here'],
            ['Random leaf hold-out 70:30', '30% of the leaves, drawn at random', 'yes – leakage', '1', 'only as a leakage check (Step 15d)'],
            ['Grouped, stratified 70:30 hold-out (plot hold-out)', '15 whole plots (4 healthy + 11 unsprayed), spread over R1–R3, varieties, timings', 'no', '1', '**main design of this report**'],
            ['Leave-one-replication-out (LORO)', 'one whole replication + 4 rotated healthy plots, three times', 'no', '3 (every leaf tested once)', 'earlier analysis; compared in Step 15'],
            ['Random leaf-level cross-validation', 'k random parts of the leaves', 'yes – leakage', 'k', 'not used']]
    tab('designs', rows=rows, caption='Kinds of training/test division and how they treat the leaves of one plot.', widths=[2300, 3000, 1600, 1400, 1700], size=16)
    read(shows='Four ways of dividing the leaves and whether they let leaves of the same plot appear on both sides.',
         how='The third column is the critical one: "yes" means the test leaves are not truly new.',
         found='The 70:30 design of this report holds out whole plots, not whole replications. Every test plot has training plots of the same block around it, but none of its own leaves is in training.',
         means='A plot hold-out tests whether the model works on new plots of the same field and season; a replication hold-out (LORO) is stricter about the block. Both avoid leaf-level leakage.',
         say='"The 70:30 split is a plot hold-out: whole plots are either training or test, so no test leaf has a sister leaf in training."')

    h2('3.2 The step card')
    card('card5', '5', 'Grouped, stratified 70:30 split of whole plots',
         'Choose 15 test plots that are kept away from every learning step and that represent the experiment.',
         'ALL, summarised per plot (48 plots: block, timing, variety, number of leaves; grade and date counts per plot). No spectrum and no model result is used.',
         'meta.csv from Step 4.',
         steps('Make a plot table: one row per plot with block (C, R1, R2, R3), timing, variety and number of leaves.',
               'Number of test plots per block type = round(0.30 × plots): healthy round(3.6) = 4; unsprayed round(10.8) = 11.',
               'Draw random candidates that obey the rules: the 11 unsprayed test plots come from 11 different treatments (timing × variety); varieties as even as possible (4/4/3); timings as even as possible (3/3/3/2); replications 4/4/3; the 4 healthy test plots have different timings and as even varieties as possible.',
               'Collect 5000 different candidates (seed 2026).',
               'Score each candidate (formula below): distance from 30% of the leaves plus distance of its grade and date mix from the mix of all leaves.',
               'Keep the candidate with the lowest score; write fold = 0 for its plots (TEST) and fold = 1 for all other plots (TRAIN).'),
         'TEST_FRAC = 0.30; SEED = 2026; n_cand = 5000; weights 1 (leaf share) and 0.5 × (0.5 grades + 0.5 dates).',
         'Test plots 1, 4, 5, 8, 13, 14, 18, 25, 27, 31, 35, 37, 44, 46, 48; 699 TEST and 1631 TRAIN leaves; column fold in meta.csv and split.json → every later step.',
         'split_lib.py (candidates, score, best_split); split_cfg.py; a1_prep.py → split.json, split_plots.csv.',
         'Roberts et al. (2017); Kuhn and Johnson (2013); Kattenborn et al. (2022); Gholamy et al. (2018); Joseph (2022).',
         '13; appendix 81–85, 131',
         'Change TEST_FRAC or SEED in split_cfg.py only if the design changes; keep the rules (whole plots, block types split separately, different treatments). With other block structures edit candidates() in split_lib.py.')
    eq('score = | n_{test} / N − 0.30 | + 0.5 × [ 0.5 × Σ_{g} | p_{g}(test) − p_{g}(all) | + 0.5 × Σ_{d} | p_{d}(test) − p_{d}(all) | ]')
    p('Here n_{test} is the number of leaves in the candidate test plots and N = 2330; p_{g} is the share of leaves of grade g and p_{d} the share of leaves of date d. '
      'The first term keeps the test set close to 30% of the leaves; the bracket keeps its grades and dates like those of the whole data set. A score of 0 would be a perfect miniature.')
    box('Worked example: the score of the chosen split.', [
        'Leaf share: 699 / 2330 = 0.3000, so the first term is |0.3000 − 0.30| = 0.0000.',
        'Grades (test vs all, %): grade 0 24.32 vs 23.69; 1 16.60 vs 16.70; 3 19.03 vs 18.45; 5 22.60 vs 22.88; 7 11.87 vs 12.62; 9 5.58 vs 5.67. Sum of absolute differences = 0.0240.',
        'Dates (test vs all, %): 11 Feb 17.45 vs 17.98; 24 Feb 22.89 vs 23.18; 3 Mar 28.76 vs 27.81; 13 Mar 30.90 vs 31.03. Sum of absolute differences = 0.0189.',
        'Score = 0.0000 + 0.5 × (0.5 × 0.0240 + 0.5 × 0.0189) = 0.5 × 0.0215 = **0.0107**, the lowest of the %d candidates (median %.4f; 5%% of candidates below %.4f).' % (SS['n'], SS['median'], SS['p05'])], kind='method')
    myfig('search', 'p02_split_search.png', 'The split search: (a) distance scores of the 5000 rule-conforming candidates, with the chosen split; (b) test-leaf share and score of every candidate.')
    read(shows='All 5000 candidate test sets that obeyed the rules, and where the chosen one lies.',
         how='Left: a histogram of the scores (lower is better); the red line is the chosen split, the dashed line the median. Right: each dot is one candidate; x = share of leaves in its test plots.',
         found='Scores ran from %.4f to about 0.06; the chosen split (%.4f) was the best, against a median of %.4f. Candidate test sets held %.1f–%.1f%% of the leaves; the chosen one exactly 30.0%%.' % (SS['best'], SS['best'], SS['median'], 100 * SS['frac_min'], 100 * SS['frac_max']),
         means='Because whole plots have different numbers of leaves (27–75 per plot), a random choice of 15 plots rarely gives exactly 30% of the leaves and the same grade mix. The search removes this luck. '
               'It uses only the counts of grades and dates – never a spectrum or a model result – so it is stratification, not selection on the test results.',
         caution='Choosing the most balanced split does not remove the luck of WHICH plots are tested. Step 15 measures that luck with 20 other rule-conforming splits.',
         say='"Among 5000 splits that obeyed the design rules I took the one whose test set best matched 30% of the leaves and the overall grade and date mix."')

    h2('3.3 The result: training and test plots')
    tab('cvcard', 8, widths=[2200, 7400], size=17, boldfirst=True)
    read(shows='The step card of the report for the validation design.',
         found='Test plots: healthy 1, 4, 5, 8; unsprayed R1 37, 44, 46, 48; R2 25, 27, 31, 35; R3 13, 14, 18. 699 test leaves (30.0%) and 1631 training leaves.',
         means='Every learning step uses the training plots only; the uncertainty of the single test set comes from a plot bootstrap (Step 11).',
         say='"Whole plots, chosen by rule, 30% of the leaves; the test plots were opened once."')
    S = pd.read_csv(A + 'split_plots.csv'); T = S[S.set == 'test']
    rows = [['Test plot', 'Block', 'Sowing timing', 'Variety', 'Leaves']] + [[str(int(r.plot)), {'C': 'healthy (sprayed)'}.get(r.block, r.block), r.timing, r.variety, str(int(r.n))] for r in T.itertuples()]
    rows.append(['15 plots', '4 healthy + 11 unsprayed', 'D1 4, D2 5, D3 4, D4 2... see text', 'V1 4, V2 6, V3 5', str(int(T.n.sum()))])
    tv = T[T.block != 'C']
    rows[-1][2] = 'unsprayed: ' + ', '.join('%s %d' % (k, v) for k, v in tv.timing.value_counts().sort_index().items())
    rows[-1][3] = 'unsprayed: ' + ', '.join('%s %d' % (k, v) for k, v in tv.variety.value_counts().sort_index().items())
    tab('testplots', rows=rows, caption='The 15 test plots with their treatment and number of leaves.', widths=[1300, 2300, 2500, 2100, 1400], size=16)
    read(shows='Each test plot, its block, treatment and number of leaves.',
         how='D = sowing timing, V = variety. The last row counts the unsprayed test plots per timing and variety.',
         found='The 11 unsprayed test plots are 11 different treatments; only treatment D1V1 has no unsprayed test plot. Healthy test plots have four different timings (D4, D3, D1, D2). Test plots hold 27–75 leaves.',
         means='Every variety and every sowing date is tested in the unsprayed plots, and every sowing date in the healthy plots, so the test accuracy is not the accuracy of one variety or one date.',
         say='"The test set covers all varieties and sowing dates, with eleven different treatments among the unsprayed plots."')
    tab('sets', 9, widths=[1100, 900, 1300, 2000, 1000, 1300, 1100, 1200])
    read(shows='Size and disease level of the training and test sets.',
         found='Training: 33 plots, 1631 leaves (70.0%), mean grade 3.28, 76.6% diseased. Test: 15 plots, 699 leaves (30.0%), mean grade 3.20, 75.7% diseased.',
         means='The two sets have almost the same disease level, so a difference between training and test accuracy cannot be blamed on a harder or easier test set.',
         say='"The test set has the same disease level as the training set."')
    tab('balance', 10, widths=[1000] + [800] * 10, size=16)
    read(shows='Grade and date mix of the training and test leaves.',
         found='No grade differs by more than 1 percentage point (largest: grade 7, 12.9% vs 11.9%); no date by more than 1.4 points.',
         means='This is the result of the score in the formula above.',
         say='"Grades and dates are mixed in the same proportions in training and test."')
    fig('splitmap', 'f35_split_map.png', 'Field layout with the 15 test plots of the grouped 70:30 split (dark) and the 33 training plots (light).', rep=3)
    read(shows='The field plan with the test plots shaded.',
         how='Rows are the healthy block and R3, R2, R1; each square is one plot with its number and treatment code.',
         found='Each row has 3–4 test plots; they are scattered, not clustered.',
         means='The test plots come from all parts of the field, so field gradients (soil, shade, water) are present in both sets.',
         say='"The test plots are spread over the whole field."')

    h2('3.4 How the training plots are divided again inside the model steps')
    p('The models need more than training and testing: their settings (hyper-parameters), feature subsets and, for networks, the number of training epochs must be chosen from data too. '
      'If they were chosen on the test plots, the test accuracy would be optimistic (Varma and Simon, 2006; Cawley and Talbot, 2010). They are therefore chosen **inside TRAIN** with a '
      'second, inner division of the training plots, again by whole plots:')
    bl('**Machine-learning models (Step 9)**: inner GroupKFold(3) by plot. The 33 training plots are cut into three groups of 11 plots. Three times, 22 plots fit a candidate model and the '
       'other 11 plots score it; the average of the three scores decides. After the choice the model is refitted on all 33 plots.',
       '**Networks (Step 10)**: one fixed cut. 11 of the 33 training plots (chosen at random, seed 42) are the validation plots, checked after every epoch; the other 22 plots fit the weights. '
       'The network of the best epoch is kept. For the networks the design is therefore 47 : 23 : 30% of the leaves (fit : validation : test).')
    tab('valroles', 11, widths=[2600, 2200, 2700, 2100], size=16)
    read(shows='For each kind of model, what is chosen from the data and which part of the training plots is used to choose it.',
         found='ML models: hyper-parameters and the SFFS subset, chosen by inner GroupKFold(3). Networks: the stopping epoch, chosen on 11 validation plots (1090 : 541 : 699 leaves). '
               'Interpretable covariate models (ordinal logistic, linear) have nothing to tune.',
         means='Networks need a fixed validation set because they are trained epoch by epoch; ML models can afford three inner rounds, which use every training plot once for validation.',
         say='"Settings are chosen inside the training plots: by three inner folds for the ML models and on a third of the training plots for the networks."')
    myfig('inner', 'p03_inner_folds.png', 'Division of the 33 training plots inside the model steps: (a) the three inner GroupKFold folds of the machine-learning models; (b) the fitting and validation plots of the networks.')
    i1, i2, i3 = INFO['inner']['1'], INFO['inner']['2'], INFO['inner']['3']
    rows = [['Inner fold', 'Validation plots (scored)', 'Healthy / R1 / R2 / R3', 'Validation leaves', 'Fitting leaves (22 plots)']]
    for k, d in (('1', i1), ('2', i2), ('3', i3)):
        b = d['blocks']; rows.append([k, ', '.join(map(str, d['plots'])), '%d / %d / %d / %d' % (b.get('C', 0), b.get('R1', 0), b.get('R2', 0), b.get('R3', 0)), str(d['n_val']), str(d['n_fit'])])
    rows.append(['Networks', ', '.join(map(str, INFO['val_plots'])), '3 / 2 / 4 / 2', str(INFO['n_val']), str(INFO['n_fit'])])
    tab('innertab', rows=rows, caption='Plots and leaves of the inner folds (machine learning) and of the validation part (networks).', widths=[1200, 3800, 1800, 1400, 1400], size=16)
    read(shows='Exactly which training plots are scored in each inner fold, and which are the validation plots of the networks.',
         how='GroupKFold assigns whole plots to three folds so that the folds have about the same number of leaves; the network validation plots are a random third of the training plots.',
         found='The three inner folds hold 546, 542 and 543 leaves. They are balanced in size but not in blocks (fold 3 contains only one R2 plot), because GroupKFold balances leaves, not strata.',
         means='Every training plot is used once for inner validation. A stratified grouped fold (StratifiedGroupKFold) could also balance the blocks; with 11 plots per fold the difference is small.',
         say='"Inside the training plots, settings were tuned on 11 plots at a time that the candidate model had not seen."')
    box('Is choosing the best of 5000 splits a kind of leakage?', 'No. The search looked only at the number of leaves, grades and dates in each candidate, which are known before any model is built. '
        'It never used a spectrum, a feature or a model score. This is the same idea as stratified sampling in an ordinary hold-out (Kuhn and Johnson, 2013). Leakage would arise only if the split '
        'had been chosen because the models scored well on it.', kind='note')
