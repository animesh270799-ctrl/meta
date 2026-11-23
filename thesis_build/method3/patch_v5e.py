"""Revision 5 (part e): expected outcomes section, title-page revision box, output file name, new references."""
def patch(f, reps):
    s = open(f).read()
    for a, b in reps:
        n = s.count(a); assert n == 1, (f, n, a[:100]); s = s.replace(a, b)
    open(f, 'w').write(s)
patch('mf3_body.py', [
 ("'Research methodology for the field experiment (revised): objectives → activities → steps'", "'Research methodology for the field experiment, season 2026-27 (revision 5): objectives → activities → steps'"),
 ("PB()\nK.append(\"K.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: 'Contents',",
  "BOX('Updates in revision 5.', '(1) Field calendar: sowing on 19 and 26 November and 3 and 10 December 2026 (7-day interval), inoculation on 30 December 2026 (crop age 41, 34, 27 and 20 days), 13 flights from 1 January to 15 March 2027, biochemical and biophysical sampling on 7 and 18 January, 8 February and 1 March. (2) Severity: disease index survey at the centre and four corners of every subplot (DI classes 0, 1, 3, 5, 7, 9; Task C = DI) and staghead severity (Step A3). (3) Objective 1 also characterises the pre-symptomatic stage with 576 samples per camera (Activity 1.8). (4) Bharatpur data are used for independent testing of frozen models, not for validation (Step A7, Activity 2.7). (5) All 48 published hyperspectral indices (39 base + 9 SWIR) and 3 red-edge parameters with formulas and references (Chapter 7). (6) Detailed covariate baseline with interpretable and machine-learning models, plot-block bootstrap and DeLong test (Step 2.5.5). (7) Sensor specifications, two ASD readings per leaf, BBCH vegetative stage 10–49 and a glasshouse pot experiment (Step A9). (8) Expected outcomes (Section 1.5).', 'E8F4F8', '1F6FB2')\nPB()\nK.append(\"K.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: 'Contents',"),
 ("# =====================================================================================\nH1('2. Common activities (carried out once for all objectives)')",
  "H2('1.5 Expected outcomes')\nTAB('outcomes', [['Objective', 'Expected outcome', 'Main outputs that support it'],\n    ['1', 'Sensitive spectral ranges, signatures and indices for the characterisation of white rust of mustard under laboratory/glasshouse and field conditions, across crop stages and disease severity levels, for large-scale application.', 'optimal wavelengths; White Rust Index; selected indices and TTFI; disease-specific and pre-symptomatic feature sets; physiological basis; glasshouse responses'],\n    ['2', 'The best suitable sensor or fusion of sensors for detection and monitoring of white rust throughout the crop growth stages.', 'accuracy of 15 sensor sets for detection, DI classes and DI; DT-EDNet vs comparison networks; gain over the covariate baseline; maps; independent test at Bharatpur'],\n    ['3', 'Early, pre-symptomatic detection so that appropriate preventive measures can be taken in time.', 'pre-symptomatic models; earliest detection day; risk maps; physiological changes before symptoms']],\n    'Expected outcomes of the research.', [1100, 4300, 3906], 16)\n\n# =====================================================================================\nH1('2. Common activities (carried out once for all objectives)')"),
])
patch('mf3_assemble.py', [("OUTF = S + 'outputs/White_rust_field_methodology_revised_DT-EDNet.docx'", "OUTF = S + 'outputs/White_rust_field_methodology_revised_DT-EDNet_5_updated.docx'")])
# references used in revision 5 that are not yet in the methodology pool
new = ["Bijlwan, A., Ranjan, R., Singh, M., Purohit, R., Nath, A.J., Chakravarty, S. (2025). Predicting crop disease severity using real time weather variability through machine learning algorithms. Scientific Reports 15, 34767. https://doi.org/10.1038/s41598-025-18613-7",
       "Cho, M.A., Skidmore, A.K. (2006). A new technique for extracting the red edge position from hyperspectral data: the linear extrapolation method. Remote Sensing of Environment 101(2), 181–193.",
       "DeLong, E.R., DeLong, D.M., Clarke-Pearson, D.L. (1988). Comparing the areas under two or more correlated receiver operating characteristic curves: a nonparametric approach. Biometrics 44(3), 837–845.",
       "De Wolf, E.D., Isard, S.A. (2007). Disease cycle approach to plant disease prediction. Annual Review of Phytopathology 45, 203–220. https://doi.org/10.1146/annurev.phyto.44.070505.143329",
       "Efron, B., Tibshirani, R.J. (1993). An Introduction to the Bootstrap. Chapman & Hall, New York.",
       "Madden, L.V., Hughes, G., van den Bosch, F. (2007). The Study of Plant Disease Epidemics. APS Press, St. Paul.",
       "Ruan, C., et al. (2022). Integrating remote sensing and meteorological data to predict wheat stripe rust. Remote Sensing 14(5), 1221. https://doi.org/10.3390/rs14051221"]
ex = open('mf3_extra_refs.txt').read().rstrip('\n').split('\n')
for r in new:
    if r[:25] not in '\n'.join(ex): ex.append(r)
open('mf3_extra_refs.txt', 'w').write('\n'.join(ex) + '\n')
print('part e ok')
