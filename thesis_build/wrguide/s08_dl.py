"""STEP 8 (E6-E7): deep-learning models. Fit on 22 training plots, early stopping on the 11 validation plots, ONE prediction of TEST.
python s08_dl.py main | config | ablation   (main = 5 networks x 3 tasks; config = 4 image networks x OW, VI, WF, DSF on task B; ablation = DT-EDNet variants on task B)"""
import os, sys, json, time, numpy as np, pandas as pd, torch, torch.nn as nn
import config as C
from lib_nets import build, pseudo
torch.set_num_threads(4)
O = C.OUT; M = pd.read_csv(os.path.join(O, '03_meta_split.csv')); T = pd.read_csv(os.path.join(O, '06_model_features.csv')); SEL = json.load(open(os.path.join(O, '06_selection_train.json')))
SPL = json.load(open(os.path.join(O, '03_split.json'))); tr = (M.fold == 1).values; te = ~tr; va = tr & M['plot'].isin(SPL['dl_val_plots']).values; fit = tr & ~va
Y = {'A': M.diseased.values, 'B': M.grade.map({g: i for i, g in enumerate(C.GRADES)}).values, 'C': M.grade.values.astype(np.float32)}

def macro_f1(y, p, K): return float(np.mean([0 if ((p == c) & (y == c)).sum() == 0 else 2 * ((p == c) & (y == c)).sum() / ((p == c).sum() + (y == c).sum()) for c in range(K)]))

def run(net, task, cols, save=None):
    torch.manual_seed(C.SEED); rng = np.random.default_rng(C.SEED); P = C.DL
    X = T[cols].values.astype(np.float32); mu, sd = X[fit].mean(0), X[fit].std(0) + 1e-6; X = (X - mu) / sd          # scaling from the fitting plots only
    y = Y[task]; K = 2 if task == 'A' else (6 if task == 'B' else 1)
    Xi, k = (X.reshape(-1, 1, 1, X.shape[1]), 1) if net == 'DNN-F1' else pseudo(X); model = build(net, k, X.shape[1], K, P['drop'])
    opt = torch.optim.AdamW(model.parameters(), lr=P['lr'], weight_decay=P['weight_decay']); sch = torch.optim.lr_scheduler.CosineAnnealingLR(opt, P['epochs'], eta_min=P['lr_min'])
    if K > 1: cw = torch.tensor(len(y[fit]) / (K * np.bincount(y[fit], minlength=K).clip(1)), dtype=torch.float32); lossf = nn.CrossEntropyLoss(weight=cw, label_smoothing=P['label_smoothing'])
    else: lossf = nn.MSELoss()
    Xt = torch.tensor(Xi); yt = torch.tensor(y, dtype=torch.long if K > 1 else torch.float32); idx = np.where(fit)[0]; best, state, bad, hist = -1e9, None, 0, []
    for ep in range(P['epochs']):
        model.train(); perm = rng.permutation(idx)
        for b in range(0, len(perm), P['batch']):
            ii = perm[b:b + P['batch']]
            if len(ii) < 2: continue
            opt.zero_grad(); out = model(Xt[ii]); loss = lossf(out, yt[ii]) if K > 1 else lossf(out.ravel(), yt[ii]); loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), P['clip']); opt.step()
        sch.step(); model.eval()
        with torch.no_grad():
            ov = model(Xt[va]); vs = macro_f1(y[va], ov.argmax(1).numpy(), K) if K > 1 else -float(np.sqrt(((ov.ravel().numpy() - y[va]) ** 2).mean()))
        hist.append(vs)
        if vs > best + P['min_delta']: best, state, bad = vs, {a: v.clone() for a, v in model.state_dict().items()}, 0
        else:
            bad += 1
            if bad >= P['patience']: break
    model.load_state_dict(state); model.eval()
    with torch.no_grad():                                                                                             # the ONLY use of the test leaves
        ot = model(Xt[te]); yp = ot.argmax(1).numpy() if K > 1 else ot.ravel().numpy(); s = torch.softmax(ot, 1)[:, 1].numpy() if K == 2 else None
    if save: torch.save(dict(state_dict=state, net=net, task=task, features=cols, scaler_mean=mu, scaler_sd=sd, k=k, n_out=K, best_epoch=int(np.argmax(hist)) + 1, val_plots=SPL['dl_val_plots']), save)
    return yp, s, len(hist), best

stage = sys.argv[1] if len(sys.argv) > 1 else 'main'; os.makedirs(os.path.join(O, '08_dl_models'), exist_ok=True); rows = []
jobs = [(n, t, 'DSF') for t in 'ABC' for n in C.NETS] if stage == 'main' else \
       [(n, 'B', cfg) for cfg in ('OW', 'VI', 'WF', 'DSF') for n in C.NETS[1:]] if stage == 'config' else \
       [(n, 'B', 'DSF') for n in ('DT-EDNet', 'DT-EDNet-SE', 'DT-EDNet-DTG', 'DT-EDNet-SE-DTG')]
for net, task, cfg in jobs:
    cols = SEL['DSF'][task] if cfg == 'DSF' else (SEL['OW'] if cfg == 'OW' else SEL[cfg][task]); t0 = time.time()
    save = os.path.join(O, '08_dl_models', '%s_%s.pt' % (task, net.replace(' ', '_'))) if stage == 'main' else None
    yp, s, ep, best = run(net, task, cols, save)
    for i, leaf in enumerate(np.where(te)[0]): rows.append(dict(task=task, model=net, family='DL', config=cfg, leaf=int(leaf), y=float(Y[task][leaf]), pred=float(yp[i]), score=(None if s is None else float(s[i]))))
    print('%s task %s %-16s %-4s epochs %d  best validation %.3f  %.0fs' % (stage, task, net, cfg, ep, best, time.time() - t0), flush=True)
pd.DataFrame(rows).to_csv(os.path.join(O, '08_dl_predictions_%s.csv' % stage), index=False); print('CHECK: %d runs written to 08_dl_predictions_%s.csv' % (len(jobs), stage))
