"""Data for the 8-slide summary of the 2025-26 work: chart data taken from the user's ASD deck (same numbers as that deck), leaf counts from the
2330-leaf table used there, UAV plot-mean spectra of 24 Feb 2026 (ENVI ROI means, ROI n = plot n) with plot DI from the ASD leaf scores of that date."""
import json, sys, numpy as np, pandas as pd
from pptx import Presentation
ASD = sys.argv[1]; UAVTXT = '/home/user/meta/thesis_build/uavhs/data/envi_plot_avg.txt'; META = '/home/user/meta/thesis_build/asd26/data/meta.csv'
D = {}
prs = Presentation(ASD)
for i, sl in enumerate(prs.slides, 1):
    for sh in sl.shapes:
        if sh.has_chart:
            ch = sh.chart; t = ch.chart_title.text_frame.text if ch.has_title else ''
            cats = [str(c) for c in ch.plots[0].categories]
            D.setdefault('asd_charts', []).append(dict(slide=i, title=t, cats=cats, series=[dict(name=s.name, values=[None if v is None else float(v) for v in s.values]) for s in ch.plots[0].series]))
M = pd.read_csv(META)
D['n_leaves'] = len(M); D['by_date'] = {d: int(n) for d, n in M.groupby('date').size().items()}
D['grade_date'] = {str(g): [int(((M.grade == g) & (M.date == d)).sum()) for d in sorted(M.date.unique())] for g in [0, 1, 3, 5, 7, 9]}
D['by_leaf'] = M.groupby('leaf').size().to_dict(); D['by_stage'] = M.groupby('stage').size().to_dict(); D['by_variety'] = M.groupby('variety').size().to_dict()
D['mean_grade_stage'] = M.groupby('stage').grade.mean().round(2).to_dict()
L = open(UAVTXT).read().splitlines(); nc = sum(l.startswith('Column') for l in L); A = np.array([[float(x) for x in l.split()] for l in L[nc + 1:] if l.strip()])
wl, R = A[:, 0], A[:, 1:]; assert R.shape[1] == 48
d24 = M[M.date == '2026-02-24']; pdi = d24.groupby('plot').score.apply(lambda x: x.sum() / (9 * len(x)) * 100).reindex(range(1, 49))
healthy = np.arange(1, 49) <= 12; dis = ~healthy; q = pdi[dis].rank(method='first'); hi = pdi[dis] >= pdi[dis].median()
keep = np.arange(0, len(wl), 2)                                                 # every 2nd band for the chart (about 8 nm)
D['uav'] = dict(n_bands=int(len(wl)), wl_min=float(wl[0]), wl_max=float(wl[-1]), wl=[round(float(w), 1) for w in wl[keep]],
                healthy=[round(float(v), 4) for v in R[:, healthy].mean(1)[keep]], diseased=[round(float(v), 4) for v in R[:, dis].mean(1)[keep]],
                dis_low=[round(float(v), 4) for v in R[:, np.where(dis)[0][~hi.values]].mean(1)[keep]], dis_high=[round(float(v), 4) for v in R[:, np.where(dis)[0][hi.values]].mean(1)[keep]],
                pdi_min=float(pdi[dis].min()), pdi_max=float(pdi[dis].max()), pdi_median=float(pdi[dis].median()),
                gaps=[[float(wl[i]), float(wl[i + 1])] for i in np.where(np.diff(wl) > 8)[0]])
def at(w): j = int(np.argmin(np.abs(wl - w))); return float(R[j, healthy].mean()), float(R[j, dis].mean())
D['uav_points'] = {str(w): [round(x, 3) for x in at(w)] for w in (550, 670, 800, 1650)}
json.dump(D, open('prev8.json', 'w'), indent=1); print(len(D['asd_charts']), 'charts;', D['n_leaves'], 'leaves;', D['by_date']); print(D['uav_points'], D['uav']['gaps'], D['uav']['pdi_min'], D['uav']['pdi_max'])
for c in D['asd_charts']: print(c['slide'], c['title'], len(c['cats']), [s['name'] for s in c['series']])
