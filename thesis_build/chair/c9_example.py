from dsl import *


def example():
    h2('8.8 One leaf through the whole pipeline')
    p('To make the steps concrete, this section follows one real leaf from the data set through the analysis. The leaf was measured on 24 February 2026 in plot 21 '
      '(replication R3, variety V3, sowing D3, 59 days after sowing, vegetative stage) at position L5, and was scored **grade 5** by eye. In the validation design it belongs to '
      'outer fold 3, so all predictions below come from models trained without replication R3.')
    h3('Step 1 – Its spectrum')
    tab('xleafR', rows=[['Wavelength', '550 nm', '680 nm', '800 nm', '1450 nm', '1940 nm'],
                        ['This leaf (grade 5)', '0.266', '0.093', '0.622', '0.071', '0.051'],
                        ['Mean of grade 0 leaves', '0.249', '0.096', '0.606', '0.109', '0.059'],
                        ['Mean of grade 9 leaves', '0.264', '0.139', '0.549', '0.162', '0.099']],
        caption='Worked example: reflectance of the example leaf at five key wavelengths, compared with the average healthy and grade-9 leaf.', widths=[2800, 1360, 1360, 1360, 1360, 1360], size=16)
    p('On reflectance alone, this leaf looks healthy: its red reflectance (0.093) and its NIR reflectance (0.622) are those of a grade-0 leaf, and its water bands are even lower than '
      'the healthy average. This is typical of vegetative-stage leaves, which have a high NIR plateau (Chapter 7.2) – and it shows why reflectance alone is a poor indicator.')
    h3('Step 2 – Its disease-specific features')
    tab('xleafF', rows=[['Feature', 'This leaf', 'Mean grade 0', 'Mean grade 5', 'Mean grade 9', 'Looks like'],
                        ['REP (nm)', '702.0', '709.0', '703.5', '701.3', 'severe (grade 7–9)'],
                        ['Dr (×10^{−3})', '13.97', '12.90', '11.50', '10.83', 'healthy'],
                        ['FD665', '−1.18', '−0.60', '−0.86', '−1.00', 'severe'],
                        ['FD870', '−0.04', '−0.04', '0.02', '0.09', 'healthy'],
                        ['FD550', '−0.16', '−0.26', '−0.06', '−0.01', 'between grades 0 and 3'],
                        ['FD595', '−0.81', '−0.76', '−0.62', '−0.59', 'healthy'],
                        ['FD1060', '0.09', '0.05', '0.03', '0.04', 'healthy'],
                        ['DWSI-2', '0.95', '1.36', '1.44', '1.42', 'healthy (lower than all grades)']],
        caption='Worked example: the example leaf\'s main features compared with the grade averages (derivatives in 10^{−3} nm^{−1}).', widths=[1700, 1300, 1500, 1500, 1500, 2100], size=16)
    p('The features disagree. The red-edge position (702.0 nm, close to the grade-7–9 average) and the slope at the red absorption (FD665) point to severe chlorophyll loss, '
      'while the height of the red-edge peak (Dr), the NIR slopes and DWSI-2 resemble a healthy leaf. This is exactly the overlap seen in the box plots ({F:dsfbox}): for a single leaf, '
      'no one feature is decisive.')
    h3('Step 3 – What the models predicted')
    tab('xleafP', rows=[['Task', 'Model', 'Prediction', 'Correct?'],
                        ['A – detection', 'SVM', 'diseased (decision value +1.64)', 'yes'],
                        ['A – detection', 'RF', 'diseased (probability 0.78)', 'yes'],
                        ['A – detection', 'ConvNeXt V2-Atto', 'diseased (probability 0.98)', 'yes'],
                        ['B – six grades', 'RF / XGBoost / ConvNeXt V2-Atto', 'grade 5', 'yes'],
                        ['B – six grades', 'SVM', 'grade 0', 'no – a large error'],
                        ['C – score', 'XGBoost / RF / ConvNeXt V2-Atto', '4.62 / 4.18 / 4.21', 'close to 5 (error 0.4–0.8)']],
        caption='Worked example: predictions of the models for the example leaf (pooled test predictions, fold 3).', widths=[1900, 3100, 2900, 1700], size=16)
    read(shows='How one leaf moves through the analysis: its raw reflectance, its selected features and the predictions of the models.',
         found=['The leaf looks healthy in reflectance, mixed in its features, and was nevertheless recognised as diseased by all detection models.',
                'Three of four models gave the correct grade 5; the SVM, relying on a different feature subset, called it healthy.',
                'The score models predicted 4.2–4.6 for a grade-5 leaf.'],
         means='The models do not read one feature; they combine several, and the combination can be right even when individual features look healthy. The same example also shows '
               'the limits: a model with a different feature subset (SVM) can make a large error on a leaf whose features conflict. This is why several models were compared and why '
               'the "within one grade" and score results are more stable than exact grades.',
         say='"This grade-5 leaf looks healthy in plain reflectance, but the red-edge position gives it away; three of four models placed it correctly in grade 5."')


def recommendations():
    h2('9.8 Recommendations for data collection in 2026-27')
    p('The leaf analysis also shows how the next season\'s measurements can be made more informative. The following points follow directly from the results:')
    nl('**Sample before symptoms appear.** On the first date 45% of leaves already showed symptoms; Objective 3 needs measurements on dates before visible disease. The three pre-symptomatic UAV flights should be matched by leaf spectra on the same days.',
       '**Keep healthy leaves in the infected plots on every date.** After 11 February almost no unsprayed leaf was grade 0, which made detection within the unsprayed plots depend on the date. Marking a few protected leaves or sub-plots inside each replication would give healthy references on every date.',
       '**Reduce label noise.** A second rater on a subset of leaves, or a photograph of each measured leaf for image-based pustule area, would show how much of the six-grade confusion comes from the visual scale itself (Bock et al., 2010).',
       '**Increase the severe grades.** Grade 9 had only 132 leaves; targeted sampling of severely diseased leaves on the later dates would give the models more examples of the rarest class.',
       '**Spread growth stages across dates.** Where possible, sample leaves of different stages on the same date, so that stage and date effects can be separated.',
       '**Record leaf-level covariates.** Leaf age or node number and the time of measurement help to explain variation that is not disease.',
       '**Keep the evaluation design.** Use leave-one-replication-out validation, nested selection and the covariate baseline for the UAV data as well, so that results remain comparable with this leaf analysis.')
    box('Why these recommendations matter.', 'Each point addresses a limitation identified in this analysis. Together they will make the 2026-27 results stronger and allow Objective 3 '
        'and the role of weather to be tested properly.', kind='present')
