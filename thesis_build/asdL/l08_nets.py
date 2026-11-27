"""STEP L6 (networks): DNN-F1 (Tasks A, B, C) and the four pseudo-image networks DT-EDNet, EfficientNet-B0, ResNet18, ConvNeXt V2-Atto (Tasks A, B)
on the leaf DSF. Fitted on the training leaves minus the 11 network validation plots; early stopping on the validation plots (best validation OA;
lowest validation RMSE for Task C); ONE prediction of the 684 test leaves. Settings of methodology Step 2.6."""
import os, sys, json, time, numpy as np, pandas as pd, torch, torch.nn as nn
sys.path.insert(0, '/home/user/meta/thesis_build/wrguide')
import configL as C
from lib_nets import build, pseudo
torch.set_num_threads(int(os.environ.get('NT', 2)))
O = C.OUT; M = pd.read_csv(os.path.join(O, 'L2_meta.csv')); ALL = pd.read_csv(os.path.join(O, 'L5_all_features.csv')); SEL = json.load(open(os.path.join(O, 'L5_selection.json')))
te = (M.nn_part == 'test').values; va = (M.nn_part == 'validation').values; fit = (M.nn_part == 'fit').values
Y = {'A': M.diseased.values, 'B': M.grade.map({g: i for i, g in enumerate(C.GRADES)}).values, 'C': M.grade.values.astype(np.float32)}
def run(net, task, Xin=None, cols=None, save=True):
    torch.manual_seed(C.SEED); rng = np.random.default_rng(C.SEED); P = C.DL; cols = cols or SEL['DSF'][task]
    X = (ALL[cols].values if Xin is None else Xin).astype(np.float32); mu, sd = X[fit].mean(0), X[fit].std(0) + 1e-6; X = (X - mu) / sd          # z-score from the fitting leaves only
    y = Y[task]; K = 2 if task == 'A' else (6 if task == 'B' else 1)
    Xi, k = (X.reshape(-1, 1, 1, X.shape[1]), 1) if net == 'DNN-F1' else pseudo(X); model = build(net, k, X.shape[1], K, P['drop'])
    opt = torch.optim.AdamW(model.parameters(), lr=P['lr'], weight_decay=P['wd']); sch = torch.optim.lr_scheduler.CosineAnnealingLR(opt, P['epochs'], eta_min=P['lr_min'])
    if K > 1: cw = torch.tensor(len(y[fit]) / (K * np.bincount(y[fit], minlength=K).clip(1)), dtype=torch.float32); lossf = nn.CrossEntropyLoss(weight=cw, label_smoothing=P['smooth'])
    else: lossf = nn.MSELoss()
    Xt = torch.tensor(Xi); yt = torch.tensor(y, dtype=torch.long if K > 1 else torch.float32); idx = np.where(fit)[0]; best, state, bad, hist = -1e9, None, 0, []
    for ep in range(P['epochs']):
        model.train(); perm = rng.permutation(idx); tl = []
        for b in range(0, len(perm), P['batch']):
            ii = perm[b:b + P['batch']]
            if len(ii) < 2: continue
            opt.zero_grad(); out = model(Xt[ii]); loss = lossf(out, yt[ii]) if K > 1 else lossf(out.ravel(), yt[ii]); loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), P['clip']); opt.step(); tl.append(loss.item())
        sch.step(); model.eval()
        with torch.no_grad():
            ov = model(Xt[va]); vl = float(lossf(ov, yt[va]) if K > 1 else lossf(ov.ravel(), yt[va]))
            vs = float((ov.argmax(1).numpy() == y[va]).mean()) if K > 1 else -float(np.sqrt(((ov.ravel().numpy() - y[va]) ** 2).mean()))
        hist.append(dict(epoch=ep + 1, train_loss=float(np.mean(tl)), val_loss=vl, val_score=vs))
        if vs > best + P['min_delta']: best, state, bad, bep = vs, {a: v.clone() for a, v in model.state_dict().items()}, 0, ep + 1
        else:
            bad += 1
            if bad >= P['patience']: break
    model.load_state_dict(state); model.eval()
    with torch.no_grad():                                                                     # the ONLY use of the test leaves
        ot = model(Xt[te]); yp = ot.argmax(1).numpy() if K > 1 else np.clip(ot.ravel().numpy(), 0, 9); s = torch.softmax(ot, 1)[:, 1].numpy() if K == 2 else None
    if save: torch.save(dict(state_dict=state, net=net, task=task, features=cols, scaler_mean=mu, scaler_sd=sd, k=k, n_out=K, best_epoch=bep), os.path.join(O, 'L6_models', '%s_%s.pt' % (task, net.replace(' ', '_'))))
    return yp, s, hist, best, bep
if __name__ != '__main__': NETS = []
else: NETS = ['DNN-F1', 'DT-EDNet', 'EfficientNet-B0', 'ResNet18', 'ConvNeXt V2-Atto']; jobs = [(n, t) for t in 'ABC' for n in NETS if t in 'AB' or n == 'DNN-F1']
if len(sys.argv) > 1 and NETS: jobs = [j for j in jobs if j[0] in sys.argv[1].split(',')]
os.makedirs(os.path.join(O, 'L6_models'), exist_ok=True); rows, H, S = [], [], []
for net, task in (jobs if NETS else []):
    t0 = time.time(); yp, s, hist, best, bep = run(net, task)
    for i, leaf in enumerate(np.where(te)[0]): rows.append(dict(task=task, model=net, family='DL', leaf=int(leaf), y=float(Y[task][leaf]), pred=float(yp[i]), score=(None if s is None else float(s[i]))))
    for h in hist: H.append(dict(task=task, model=net, **h))
    S.append(dict(task=task, model=net, epochs_run=len(hist), best_epoch=bep, best_val=best, seconds=round(time.time() - t0)))
    print('task %s %-16s epochs %3d best epoch %3d best validation %.3f  %.0fs' % (task, net, len(hist), bep, best, time.time() - t0), flush=True)
if NETS:
  tag = '' if len(sys.argv) == 1 else '_' + sys.argv[1].replace(',', '_').replace(' ', '').replace('-', '')
  pd.DataFrame(rows).to_csv(os.path.join(O, 'L6_dl_predictions%s.csv' % tag), index=False); pd.DataFrame(H).to_csv(os.path.join(O, 'L6_dl_history%s.csv' % tag), index=False)
  pd.DataFrame(S).to_csv(os.path.join(O, 'L6_dl_summary%s.csv' % tag), index=False); print('CHECK done: %d network runs' % len(jobs))
