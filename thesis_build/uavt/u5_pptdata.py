"""Collect the numbers for the slides into out/ppt_data.json."""
import json, os, numpy as np, pandas as pd
O = os.path.dirname(os.path.abspath(__file__)) + '/out/'
GT = pd.read_csv(O + 'ground_truth.csv'); MF = pd.read_csv(O + 'metrics_frozen.csv'); MU = pd.read_csv(O + 'metrics_uav_trained.csv')
BM = pd.read_csv(O + 'best_models.csv'); DF = pd.read_csv(O + 'domain_features.csv'); SU = json.load(open(O + 'summary.json')); RN = json.load(open(O + 'report_numbers.json'))
clean = lambda d: {k: (None if (isinstance(v, float) and not np.isfinite(v)) else (float(v) if isinstance(v, (np.floating, float)) else (int(v) if isinstance(v, (np.integer,)) else v))) for k, v in d.items()}
VAR = ['Direct', 'Healthy-reference corrected', 'Corrected + brightness-normalised']
best = SU['best']; rows = {}
for t in 'ABC':
    rows[t] = {role: {v: clean(MF[(MF.task == t) & (MF.model == best[t][role]) & (MF.variant == v)].iloc[0].to_dict()) for v in VAR} for role in ('overall', 'ML', 'DL')}
top = {t: clean(MF[MF.task == t].sort_values('R2' if t == 'C' else 'macro_F1', ascending=False).iloc[0].to_dict()) for t in 'ABC'}
heat = {t: MF[MF.task == t].pivot_table(index='model', columns='variant', values='R2' if t == 'C' else 'macro_F1')[VAR].round(3).reset_index().to_dict('records') for t in 'ABC'}
dis = GT[GT.status == 'Diseased']
D = dict(best=best, asd={t: {r: float(BM[(BM.task == t) & (BM.role == r)].asd_value.iloc[0]) for r in ('overall', 'ML', 'DL')} for t in 'ABC'},
         rows=rows, uav={t: clean(MU[MU.task == t].iloc[0].to_dict()) for t in 'ABC'}, top=top, heat=heat,
         gt=dict(n=len(GT), healthy=int((GT.status == 'Healthy').sum()), diseased=len(dis), score_min=float(dis.score.min()), score_max=float(dis.score.max()),
                 pdi_min=float(dis.PDI.min()), pdi_max=float(dis.PDI.max()), leaves=int(GT.n_leaves.sum()), grades={str(k): int(v) for k, v in GT.grade.value_counts().sort_index().items()}),
         dom=[clean(r) for r in DF.to_dict('records')], rn=RN, n_bands=SU['n_bands'], asd_n=SU['asd_models_trained_on'], gaps=SU['gaps'],
         findings=json.load(open(O + 'findings.json')), refs=json.load(open(O + 'refs_used.json')),
         features={t: {r: ', '.join(pd.concat([pd.read_csv(O + '../../outputs/ASD_2025-26_models/ml_models_index.csv'), pd.read_csv(O + '../../outputs/ASD_2025-26_models/dl_models_index.csv')]).query('task == @t and model == @m').features.iloc[0].split(', '))
                       for r, m in best[t].items()} for t in 'ABC'})
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from u_content import METRICS, GLOSSARY, APPLY
D.update(tables=json.load(open(O + 'tables.json')), figures=json.load(open(O + 'figures.json')), methods=json.load(open(O + 'methods.json')), interp=json.load(open(O + 'interpretations.json')),
         metrics_expl=[list(x) for x in METRICS], glossary=[list(x) for x in GLOSSARY], apply=[list(x) for x in APPLY])
json.dump(D, open(O + 'ppt_data.json', 'w'), indent=1, default=str); print('saved ppt_data.json')
