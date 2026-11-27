"""Revision 5 (part d): figures – new dates, independent testing, Activity 1.8, disease index."""
def patch(f, reps):
    s = open(f).read()
    for a, b in reps:
        n = s.count(a); assert n == 1, (f, n, a[:100]); s = s.replace(a, b)
    open(f, 'w').write(s)
s = open('mf3_fig.py').read()
i = s.index("        ('Objective 1 – Characterisation (Activities 1.1–1.7)',"); j = s.index("\n", i)
line = s[i:j]
line2 = line.replace("('Objective 1 – Characterisation (Activities 1.1–1.7)',", "('Objective 1 – Characterisation, post- and pre-symptomatic (Activities 1.1–1.8)',")
s = s[:i] + line2 + s[j:]; open('mf3_fig.py', 'w').write(s)
patch('mf3_fig.py', [
 ("DT-EDNet, EfficientNet, ResNet18, ConvNeXt V2 | detection, severity classes, severity score | ablation, maps', 'o2'),", "DT-EDNet, EfficientNet, ResNet18, ConvNeXt V2 | detection, DI classes, disease index | ablation, maps | independent testing at Bharatpur', 'o2'),"),
 ("chain('g05_obj1.png', 'Objective 1 – Characterisation of white rust by each camera (Activities 1.1–1.7)', [", "chain('g05_obj1.png', 'Objective 1 – Characterisation of white rust by each camera (Activities 1.1–1.8)', ["),
 ("disease effect by date and growth stage; links with camera features', 'physiological explanation')], 'o1')", "disease effect by date and growth stage; links with camera features', 'physiological explanation'),\n    ('Activity 1.8  Pre-symptomatic stage', '576 pre-symptomatic samples per camera; later-infected vs healthy; response curves, effect sizes,\\nwavelengths, indices, texture and thermal features before symptoms', 'pre-symptomatic feature set;\\nearliest-responding features')], 'o1')"),
 ("('Activity 2.7  Second-stage validation at Bharatpur',", "('Activity 2.7  Independent testing at Bharatpur',"),
 ("('Objective 1: Activities 1.1–1.6', 1.6, 2.7, 'o1')", "('Objective 1: Activities 1.1–1.8', 1.6, 2.7, 'o1')"),
 ("('Second-stage validation (Bharatpur)',", "('Independent testing (Bharatpur)',"),
 ("ax.set_xticks(dai); ax.set_xticklabels(['12 Jan\\n(2 DAI)', '15 Jan\\n(5 DAI)', '18 Jan\\n(8 DAI)'])", "ax.set_xticks(dai); ax.set_xticklabels(['1 Jan\\n(2 DAI)', '4 Jan\\n(5 DAI)', '7 Jan\\n(8 DAI)'])"),
 ("box(ax, 0.3, 0.4, 5.1, 1.8, 'Post-symptomatic set (Objectives 1 and 2)', '1920 subplot samples per camera\\n(10 dates × 48 plots × 4 subplots; 21 Jan – 25 Mar 2027)\\nlabels: severity score, class, healthy / diseased', 'o2', fs=9)",
  "box(ax, 0.3, 0.4, 5.1, 1.8, 'Post-symptomatic set (Objectives 1 and 2)', '1920 subplot samples per camera\\n(10 dates × 48 plots × 4 subplots; 11 Jan – 15 Mar 2027)\\nlabels: disease index, DI class, healthy / diseased', 'o2', fs=9)"),
 ("box(ax, 5.7, 0.4, 5.0, 1.8, 'Pre-symptomatic set (Objective 3)', '576 subplot samples per camera\\n(3 dates × 48 plots × 4 subplots; 12, 15, 18 Jan 2027)\\nlabels: healthy / infected (later status), later severity', 'o3', fs=9)",
  "box(ax, 5.7, 0.4, 5.0, 1.8, 'Pre-symptomatic set (Objectives 1 and 3)', '576 subplot samples per camera\\n(3 dates × 48 plots × 4 subplots; 1, 4, 7 Jan 2027)\\nlabels: healthy / infected (later status), later disease index', 'o3', fs=9)"),
 ("dates = [('12 Jan', 2), ('15 Jan', 5), ('18 Jan', 8), ('21 Jan', 11), ('28 Jan', 18), ('4 Feb', 25), ('11 Feb', 32), ('18 Feb', 39), ('25 Feb', 46), ('4 Mar', 53), ('11 Mar', 60), ('18 Mar', 67), ('25 Mar', 74)]",
  "dates = [('1 Jan', 2), ('4 Jan', 5), ('7 Jan', 8), ('11 Jan', 12), ('18 Jan', 19), ('25 Jan', 26), ('1 Feb', 33), ('8 Feb', 40), ('15 Feb', 47), ('22 Feb', 54), ('1 Mar', 61), ('8 Mar', 68), ('15 Mar', 75)]"),
 ("ax.text(x0 - 0.12, 2.3, 'inoculation\\n10 Jan 2027', ha='right', va='center', fontsize=7.8)", "ax.text(x0 - 0.12, 2.3, 'inoculation\\n30 Dec 2026', ha='right', va='center', fontsize=7.8)"),
 ("ax.add_patch(FancyBboxPatch((x0 + 10 * sc, 2.75), 65 * sc, 0.55,", "ax.add_patch(FancyBboxPatch((x0 + 11 * sc, 2.75), 65 * sc, 0.55,"),
 ("ax.text(x0 + 42.5 * sc, 3.02, 'post-symptomatic: 10 dates, 1920 samples (label = severity score observed on the same date)',", "ax.text(x0 + 43.5 * sc, 3.02, 'post-symptomatic: 10 dates, 1920 samples (label = disease index surveyed on the same date)',"),
 ("ax.text(0.4, 0.2, 'all four cameras (red–green–blue, multispectral, thermal, hyperspectral), ASD leaf spectra and visual severity scoring on every date', ha='left', fontsize=8, style='italic')", "ax.text(0.4, 0.2, 'all four cameras (red–green–blue, multispectral, thermal, hyperspectral), ASD leaf spectra and the disease index survey on every date', ha='left', fontsize=8, style='italic')"),
 ("box(ax, 0.2, 1.85, 3.6, 1.35, 'Stage 1 – IARI field (internal)',", "box(ax, 0.2, 1.85, 3.6, 1.35, 'Validation – IARI field (internal)',"),
 ("box(ax, 8.2, 1.85, 3.6, 1.35, 'Stage 2 – Bharatpur (independent)',", "box(ax, 8.2, 1.85, 3.6, 1.35, 'Independent testing – Bharatpur',"),
 ("box(ax, 0.2, 0.25, 11.6, 1.25, 'Reported for the second stage', 'same metrics as stage 1 (overall accuracy, kappa, weighted kappa, macro-F1, AUC; R², RMSE, RPD) | loss of accuracy from stage 1 to stage 2\\n",
  "box(ax, 0.2, 0.25, 11.6, 1.25, 'Reported for the independent test (not a validation)', 'same metrics as the internal validation (overall accuracy, kappa, weighted kappa, macro-F1, AUC; R², RMSE, RPD) | loss of accuracy from validation to test\\n"),
 ("print('figures ok')", """chain('g31_presym.png', 'Activity 1.8 – Characterisation of the pre-symptomatic stage (576 samples per camera)', [
    ('1.8.1  Response curves', 'mean spectra, first derivative, indices, texture and temperature of later-infected vs healthy subplots\\non 1, 4 and 7 January; percentage difference from healthy', 'pre-symptomatic response'),
    ('1.8.2  Univariate tests', 'plot means (unit = plot); Welch t-test or Mann–Whitney U; Hedges g with 95% interval;\\nBenjamini–Hochberg false discovery rate 5%', 'effect size per feature and date'),
    ('1.8.3  Effective ranges and optimal wavelengths', 'NDSI/RSI maps and SHAP-CARS with the binary later-status label (inside training folds)', 'pre-symptomatic wavelengths'),
    ('1.8.4  Indices, texture and thermal features', 'healthy-plot normalisation; ReliefF (two classes); mRMR; canopy minus air temperature, NRCT, CWSI;\\nvariance inflation factor below 10', 'pre-symptomatic feature set'),
    ('1.8.5  Earliest-responding features', 'first date (2, 5 or 8 days after inoculation) with a significant, large effect; by variety and timing;\\nlinked with the physiology of 7 January', 'earliest features → Objective 3')], 'o1')
print('figures ok')"""),
])
print('part d ok')
