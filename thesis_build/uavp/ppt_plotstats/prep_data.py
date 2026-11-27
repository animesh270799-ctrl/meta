"""Collect the plot-level evaluation results (outputs/Plot_level_evaluation_RF_24Feb2026_step4) into deck_data.json for the slide deck."""
import json, os, numpy as np, pandas as pd
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../outputs/Plot_level_evaluation_RF_24Feb2026_step4/')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'deck_data.json')
M = pd.read_csv(D + 'metrics_all_models.csv', index_col=0); B = pd.read_csv(D + 'bootstrap_95CI.csv'); MC = pd.read_csv(D + 'mcnemar.csv'); W = pd.read_csv(D + 'wilcoxon_DI_error.csv')
names = {'RF detection': 'det', 'RF six grades': 'grd', 'RF severity score': 'scr'}
files = {'det': 'per_plot_RF_detection.csv', 'grd': 'per_plot_RF_six_grades.csv', 'scr': 'per_plot_RF_severity_score.csv'}
def f(x): return None if pd.isna(x) else float(x)
out = dict(metrics={names[c]: {k: f(v) for k, v in M[c].items()} for c in M.columns}, boot={}, plots={}, mcnemar=MC.to_dict('records'), wilcoxon=W.to_dict('records'))
for _, r in B.iterrows(): out['boot'].setdefault(names[r.model], {})[r.statistic] = [float(r.value), float(r.ci_low), float(r.ci_high)]
CN = ['Healthy', 'Very low', 'Low', 'Moderate', 'High', 'Very high']
for k, fn in files.items():
    T = pd.read_csv(D + fn); P = dict(plot=T['plot'].tolist(), obs_DI=T.obs_DI.round(2).tolist(), status=T.obs_status.tolist(), share=T.share_diseased_pct.round(1).tolist(), pixels=T.pixels.tolist())
    if 'pred_DI' in T: P['pred_DI'] = T.pred_DI.round(2).tolist(); P['cm'] = pd.crosstab(pd.Categorical(T.obs_class_idx, range(6)), pd.Categorical(T.pred_class_idx, range(6)), dropna=False).values.tolist()
    P['mean_value'] = T.mean_pixel_value.round(3).tolist()
    h, d = T[T.obs_status == 0], T[T.obs_status == 1]
    P['summary'] = dict(share_h=[float(h.share_diseased_pct.min()), float(h.share_diseased_pct.max())], share_d=[float(d.share_diseased_pct.min()), float(d.share_diseased_pct.max())],
                        mv_h=float(h.mean_pixel_value.mean()), mv_d=float(d.mean_pixel_value.mean()))
    if 'pred_DI' in T: P['summary'].update(di_h=[float(h.pred_DI.min()), float(h.pred_DI.max())], di_d=[float(d.pred_DI.min()), float(d.pred_DI.max())], classes=T.pred_class.value_counts().to_dict())
    out['plots'][k] = P
info = json.load(open(D + 'run_info.json')); out['info'] = dict(crop_pixels=int(sum(m['crop_pixels_in_plots'] for m in info['models']) / len(info['models'])), step=info['models'][0]['spatial_step'],
    px_min=int(min(out['plots']['det']['pixels'])), px_max=int(max(out['plots']['det']['pixels'])))
json.dump(out, open(OUT, 'w'), indent=1); print('written', OUT); print(json.dumps(out['info'])); print(out['plots']['det']['summary']); print(out['plots']['grd']['summary']); print(out['plots']['scr']['summary'])
