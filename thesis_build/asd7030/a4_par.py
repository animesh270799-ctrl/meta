"""Parallel runner for a4_dl.py: the same runs (main, configuration and ablation stages) split over N single-thread workers
(longest-job-first balancing), each saving after every run; `merge` writes dl_main.json, dl_config.json and dl_ablation.json."""
import os, sys, json, time
from split_cfg import FOLDS, TAG, LABEL
os.environ.setdefault('TT', '1')
from a4_dl import run, cols_for, D
NETS = ['DT-EDNet', 'EfficientNet-B0', 'ResNet18', 'ConvNeXt V2-Atto']
COST = {'EfficientNet-B0': 11.3, 'ResNet18': 4.2, 'ConvNeXt V2-Atto': 3.6, 'DT-EDNet': 2.7, 'DT-EDNet-SE': 2.6, 'DT-EDNet-DTG': 1.0, 'DT-EDNet-SE-DTG': 0.9, 'DNN-F1': 0.1}
def jobs():
    J = [('main', t, n, f, 'DSF') for t in 'ABC' for n in ['DNN-F1'] + NETS for f in FOLDS]
    J += [('config', 'B', n, f, c) for c in ('OW', 'VI') for n in NETS for f in FOLDS]
    J += [('ablation', 'B', n, f, 'DSF') for n in ('DT-EDNet-SE', 'DT-EDNet-DTG', 'DT-EDNet-SE-DTG') for f in FOLDS]
    return J
def shard(n):
    S, load = [[] for _ in range(n)], [0.0] * n
    for j in sorted(jobs(), key=lambda j: -COST[j[2]]):
        i = load.index(min(load)); S[i].append(j); load[i] += COST[j[2]]
    return S
if __name__ == '__main__':
    if sys.argv[1] == 'worker':
        i, n = int(sys.argv[2]), int(sys.argv[3]); fn = D + 'dl_part%d.json' % i
        out = json.load(open(fn)) if os.path.exists(fn) else []; done = {(r['stage'], r['task'], r['net'], r['fold'], r['cfg']) for r in out}
        for st, task, net, f, cfg in shard(n)[i]:
            if (st, task, net, f, cfg) in done: continue
            t0 = time.time(); r = run(net, task, f, cols_for(f, cfg, task), lr=1e-3 if net == 'DNN-F1' else 6e-4, tag='ablation' if st == 'ablation' else cfg)
            r['stage'], r['cfg'] = st, cfg; out.append(r); json.dump(out, open(fn, 'w'))
            print(st, task, net, f, cfg, 'val %.3f ep %d %.0fs' % (r['best_val'], r['epochs'], time.time() - t0), flush=True)
        print('WORKER DONE', flush=True)
    if sys.argv[1] == 'merge':
        n = int(sys.argv[2]); R = []
        for i in range(n):
            if os.path.exists(D + 'dl_part%d.json' % i): R += json.load(open(D + 'dl_part%d.json' % i))
        order = {j: k for k, j in enumerate(jobs())}; R.sort(key=lambda r: order[(r['stage'], r['task'], r['net'], r['fold'], r['cfg'])])
        for st in ('main', 'config', 'ablation'):
            json.dump([r for r in R if r['stage'] == st], open(D + 'dl_%s.json' % st, 'w'))
        print('merged', {st: sum(r['stage'] == st for r in R) for st in ('main', 'config', 'ablation')}, 'of', len(jobs()))
