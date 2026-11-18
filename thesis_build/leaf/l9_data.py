"""Export every number, table and figure path needed by the full results deck (l9_ppt.js)."""
import numpy as np, pandas as pd, json, os
from PIL import Image
B = os.path.dirname(os.path.abspath(__file__)) + '/'; D = B + 'data/'; FG = B + 'fig/'
M = pd.read_csv(D + 'meta_leaf2.csv'); P = pd.read_csv(D + 'plot_table.csv'); Fp = pd.read_csv(D + 'feat_plot_wri.csv')
R1 = json.load(open(D + 'res1.json')); RS = R1['RES']; R2 = json.load(open(D + 'res2.json')); SW = json.load(open(D + 'swir_tier2.json')); PI = json.load(open(D + 'prep_info.json'))
A = pd.read_csv(D + 't_anova.csv'); y = M.grade.values; G6 = [0, 1, 3, 5, 7, 9]
f2 = lambda v: '%.2f' % v; f3 = lambda v: '%.3f' % v
t2, t3, t4, t5, t6 = RS['tier2'], RS['tier3'], RS['tier4'], RS['tier5'], RS['tier6']
rc, rr = R2['cls'], R2['reg']; bc, br = R2['best']['cls'], R2['best']['reg']; bu = [k for k in rr if k.startswith('Bottom-up')][0]
out = {}
# ---- key numbers ----
out['k'] = dict(n_leaves=len(M), n_pd=len(P), pdi_max='%.1f' % P.PDI.max(), splice='%.4f' % PI['splice_mean'], n_bands=PI['n_bands'],
    regions=t2['n_regions'], scal=[t2['n_scal_cand'], t2['n_scal_reg']], rel=[t2['n_rel_cand'], t2['n_rel_reg']], n_rob=len(t2['robust']), n_reg=len(t2['regonly']), n_cls=len(t2['clsonly']),
    maxr_fd=[f2(t2['max_r']['FD'][0]), t2['max_r']['FD'][1]], maxr_r=[f2(t2['max_r']['R'][0]), t2['max_r']['R'][1]], adj_r='%.4f' % t2['median_adjacent_r'],
    wri=t3['vnir']['formula'], wri_ba=f2(t3['vnir']['best']['ba_cv']), wri_r=f2(np.corrcoef(Fp.WRI_VNIR, P.PDI)[0, 1]), wri_ncand='{:,}'.format(t3['vnir']['n_cand']),
    wri_sw=t3['swir']['formula'], wri_sw_ba=f2(t3['swir']['best']['ba_cv']), wri_sw_ncand='{:,}'.format(t3['swir']['n_cand']),
    n_sig=t4['n_sig'], n_feat=t4['n_feat'], top_f=[t4['top'][0][0], '%.0f' % t4['top'][0][1], f2(t4['top'][0][2])],
    cda1=[len(t5['step1']['selected']), f2(t5['step1']['cancor'][0]), '%.0f' % (100 * t5['step1']['share'][0]), f3(t5['step1']['wilks']), f2(t5['step1']['acc']), f2(t5['step1']['adj'])],
    cda2=[len(t5['step2']['selected']), f2(t5['step2']['cancor'][0]), '%.0f' % (100 * t5['step2']['share'][0]), f3(t5['step2']['wilks']), f2(t5['step2']['acc']), f2(t5['step2']['adj'])],
    bor=[len(t6['cls']['confirmed']), t6['cls']['n_in'], len(t6['reg']['confirmed']), t6['reg']['n_in']],
    bc=bc, br=br, c_mf1=f2(rc[bc]['macro_f1']), c_oa=f2(rc[bc]['oa']), c_kap=f2(rc[bc]['kappa']), c_adj=f2(rc[bc]['adj']), c_det=f2(rc[bc]['detection_acc']),
    plsda=f2(rc['PLS-DA (full spectrum)']['macro_f1']), rfall=f2(rc['RF (all 53 features)']['macro_f1']),
    r_r2=f2(rr[br]['r2']), r_rmse='%.1f' % rr[br]['rmse'], r_rpd=f2(rr[br]['rpd']), bu_r2=f2(rr[bu]['r2']), plsr=f2(rr['PLSR (full spectrum)']['r2']), rfrall=f2(rr['RFR (all 53 features)']['r2']),
    swir_best=[A[A.Group == 'SWIR index'].iloc[0].Feature, f2(A[A.Group == 'SWIR index'].iloc[0].r_PDI_plot)],
    swir_maxr=f2(A[A.Group == 'SWIR index'].r_PDI_plot.abs().max()),
    ofc_sizes=[min(len(f['ofc'][bc]['features']) for f in R2['folds']), max(len(f['ofc'][bc]['features']) for f in R2['folds'])])
# ---- tables ----
ct = pd.crosstab(M.date, M.grade)
out['t_data'] = [['Date', 'Main stage', 'Leaves'] + ['G%d' % g for g in G6] + ['Mean PDI (%)']] + \
    [[d, M[M.date == d].stage.mode()[0], str(int((M.date == d).sum()))] + [str(int(ct.loc[d, g])) if g in ct.columns else '0' for g in G6] + ['%.1f' % P.PDI[P.date == d].mean()] for d in sorted(M.date.unique())] + \
    [['All', '—', str(len(M))] + [str(int((y == g).sum())) for g in G6] + ['%.1f' % P.PDI.mean()]]
out['counts'] = {d: [int(ct.loc[d, g]) if g in ct.columns else 0 for g in G6] for d in sorted(M.date.unique())}
L = max(len(t2['robust']), len(t2['regonly']), len(t2['clsonly']))
out['t_bands'] = [['Robust (both tasks)', 'Regression only', 'Classification only']] + [[(t2['robust'] + [''] * L)[i], (t2['regonly'] + [''] * L)[i], (t2['clsonly'] + [''] * L)[i]] for i in range(L)]
wv = pd.read_csv(D + 't_wri_vnir_top.csv').head(5); ws = pd.read_csv(D + 't_wri_swir_top.csv').head(3)
out['t_wri'] = [['Candidate index', 'BA (screening)', 'BA (8-fold CV)', 'CV SD']] + [[r[0], f3(r[1]), f3(r[2]), f3(r[3])] for r in wv.values] + [[r[0] + ' (SWIR)', f3(r[1]), f3(r[2]), f3(r[3])] for r in ws.values]
F_ = pd.read_csv(D + 'feat_leaf_wri.csv'); out['wri_means'] = [round(float(F_.WRI_VNIR[y == g].mean()), 4) for g in G6]
out['t_anova'] = [['Feature', 'Group', 'F', 'η²', 'r with PDI', 'ρ with grade']] + [[r.Feature, r.Group, '%.0f' % r.F, f2(r.eta2), f2(r.r_PDI_plot), f2(r.rho_score_leaf)] for r in A.head(12).itertuples()]
lt = t4['letters']; out['t_tukey'] = [['Feature'] + ['G%d' % g for g in G6]] + [[k] + [lt[k][str(g)] for g in G6] for k in list(lt)[:6]]
sw_ = A[A.Group == 'SWIR index']; out['t_swir'] = [['SWIR index', 'F', 'η²', 'r with PDI']] + [[r.Feature, '%.0f' % r.F, f2(r.eta2), f2(r.r_PDI_plot)] for r in sw_.itertuples()]
out['swir_bar'] = [[r.Feature, round(float(r.r_PDI_plot), 3)] for r in sw_.itertuples()]
c1, c2 = t5['step1'], t5['step2']
out['t_cda'] = [['Quantity', 'Step 1: bands', 'Step 2: indices + red edge + WRI'], ['Variables in → after VIF < 10', '%d → %d' % (c1['n_in'], c1['n_vif']), '%d → %d' % (c2['n_in'], c2['n_vif'])],
    ['Selected variables', ', '.join(c1['selected']), ', '.join(c2['selected'])], ['Canonical r (F1, F2, F3)', ', '.join(f2(v) for v in c1['cancor'][:3]), ', '.join(f2(v) for v in c2['cancor'][:3])],
    ['Share of function 1', '%.0f%%' % (100 * c1['share'][0]), '%.0f%%' % (100 * c2['share'][0])], ["Wilks' lambda", f3(c1['wilks']), f3(c2['wilks'])],
    ['LORO accuracy / macro-F1', '%s / %s' % (f2(c1['acc']), f2(c1['macro_f1'])), '%s / %s' % (f2(c2['acc']), f2(c2['macro_f1']))], ['±1-grade accuracy', f2(c1['adj']), f2(c2['adj'])]]
out['t_dsf'] = [['Pool', 'Confirmed features'], ['Classification (%d of %d)' % (len(t6['cls']['confirmed']), t6['cls']['n_in']), ', '.join(t6['cls']['confirmed'])], ['Regression (%d of %d)' % (len(t6['reg']['confirmed']), t6['reg']['n_in']), ', '.join(t6['reg']['confirmed'])]]
fl = lambda Lst: ['%s%d' % (t, w) for t, w in Lst]
out['t_swirreg'] = [['SWIR list', 'Bands (SWIR-only Tier 2)'], ['Robust (both tasks)', ', '.join(fl(SW['robust']))], ['Regression only', ', '.join(fl(SW['regonly']))], ['Classification only', ', '.join(fl(SW['clsonly']))]]
out['t_folds'] = [['Test rep.', 'Bands (C / R)', 'Boruta (C / R)', 'VIF (C / R)', '%s features (classification)' % bc, '%s features (regression)' % br]] + \
    [[f['test_rep'], '%d / %d' % (f['n_cls_bands'], f['n_reg_bands']), '%d / %d' % (f['boruta_cls'], f['boruta_reg']), '%d / %d' % (len(f['vif_cls']), len(f['vif_reg'])), ', '.join(f['ofc'][bc]['features']), ', '.join(f['ofc']['R_' + br]['features'])] for f in R2['folds']]
out['t_cls'] = [['Model', 'OA', 'Kappa', 'Macro-F1', '±1 grade', 'Healthy vs diseased']] + [[k, f2(v['oa']), f2(v['kappa']), f2(v['macro_f1']), f2(v['adj']), f2(v['detection_acc'])] for k, v in rc.items()]
out['cls_bar'] = {k: [round(v['macro_f1'], 3), round(v['adj'], 3)] for k, v in rc.items()}
v = rc[bc]; out['t_grade'] = [['Grade'] + [str(g) for g in G6], ['Precision'] + [f2(q) for q in v['P']], ['Recall'] + [f2(q) for q in v['R']], ['F1'] + [f2(q) for q in v['F1']]]
out['cm'] = v['cm']
out['t_reg'] = [['Model', 'R²', 'RMSE (PDI %)', 'NRMSE', 'RPD']] + [[k, f2(q['r2']), '%.1f' % q['rmse'], f2(q['nrmse']), f2(q['rpd'])] for k, q in rr.items()]
out['reg_bar'] = {k: round(max(q['r2'], 0), 3) for k, q in rr.items()}
out['t_date'] = [['Date', 'OA', 'Macro-F1', 'R² (PDI)', 'RMSE (PDI)']] + [[d, f2(q['oa']), f2(q['macro_f1']), (f2(q['r2']) if q['r2'] is not None else '—'), '%.1f' % q['rmse']] for d, q in R2['by_date'].items()]
out['t_var'] = [['Variety', 'Macro-F1', 'R² (PDI)']] + [[k, f2(q['macro_f1']), f2(q['r2'])] for k, q in R2['by_variety'].items()]
# ---- full-range WRI comparison (l10_wri_full.py) ----
if os.path.exists(D + 'wri_full.json'):
    WF = json.load(open(D + 'wri_full.json')); C = WF['comparison']; S = WF['searches']; N = pd.DataFrame(WF['nested'])
    nm = [c['Index'] for c in C]; IX = WF['indices']
    out['k'].update(wf=IX[nm[3]][0], wf_ba=f3(C[3]['BA_CV']), wf_auc=f3(C[3]['AUC']), wf_r=f2(C[3]['r_PDI']), wsw=IX[nm[2]][0], wsw_ba=f3(C[2]['BA_CV']),
                    wnd=IX[nm[4]][0], wnd_ba=f3(C[4]['BA_CV']), wv_ba2=f3(C[0]['BA_CV']), wv_auc=f3(C[0]['AUC']), ws_ba2=f3(C[1]['BA_CV']),
                    wf_ncand='{:,}'.format(S['FULL all']['n_cand']), wf_npairs='{:,}'.format(S['FULL all']['n_pairs']), wf_nb=S['FULL all']['n_bands'],
                    nest={r: f3(N[N.Range == r].ba_test.mean()) for r in ('VNIR', 'SWIR', 'SWIR-W', 'FULL')})
    rng = {'VNIR': '450–950 nm', 'SWIR': '1000–2400 nm, water bands removed', 'SWIR-W': '1000–2400 nm, water bands kept', 'FULL': '400–2400 nm, all bands'}
    out['t_wf_search'] = [['Search', 'Wavelengths', 'Bands', 'ND pairs', 'Candidates', 'Best index (all leaves)', 'BA (8-fold CV)']] + \
        [[r, rng[r], str(S[r + ' all']['n_bands']), '{:,}'.format(S[r + ' all']['n_pairs']), '{:,}'.format(S[r + ' all']['n_cand']),
          IX[nm[{'VNIR': 0, 'SWIR': 1, 'SWIR-W': 2, 'FULL': 3}[r]]][0] if r != 'SWIR' else IX[nm[1]][0], f3(S[r + ' all']['top'][0]['ba_cv'])] for r in rng]
    out['t_wf_cmp'] = [['Index', 'Formula', 'BA (CV)', 'AUC', 'AUC 0 vs 1', 'F', 'η²', 'ρ grade', 'r PDI']] + \
        [[c['Index'].split(' (')[0], c['Formula'], f3(c['BA_CV']), f3(c['AUC']), f3(c['AUC_0v1']), '%.0f' % c['F'], f2(c['eta2']), f2(c['rho_grade']), f2(c['r_PDI'])] for c in C]
    out['t_wf_nested'] = [['Search', 'Test R1: formula (BA)', 'Test R2: formula (BA)', 'Test R3: formula (BA)', 'Mean BA']] + \
        [[r] + ['%s (%s)' % (q.formula, f3(q.ba_test)) for q in N[N.Range == r].itertuples()] + [f3(N[N.Range == r].ba_test.mean())] for r in rng]
    out['wf_bar'] = {c['Index'].split(' (')[0]: [round(c['BA_CV'], 3), round(c['AUC'], 3), round(c['AUC_0v1'], 3)] for c in C}
    out['wf_means'] = {k_.split(' (')[0]: v_ for k_, v_ in WF['grade_means'].items()}
# ---- figure aspect ratios ----
out['img'] = {f[:-4]: round(Image.open(FG + f).size[1] / Image.open(FG + f).size[0], 4) for f in os.listdir(FG) if f.endswith('.png')}
out['refs'] = json.load(open(D + 'refs_used.json'))
json.dump(out, open(D + 'deck.json', 'w'), ensure_ascii=False)
print('deck.json ok', len(out['refs']), 'refs')
