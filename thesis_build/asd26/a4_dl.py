"""Objective 2, Activity 2.3: deep-learning models on the fold-wise selected leaf features.
DNN-F1 (feature vector) and pseudo-image networks DT-EDNet, EfficientNet-B0, ResNet18, ConvNeXt V2-Atto (Ma et al., 2026 settings,
adapted for CPU: maximum 100 epochs, early-stopping patience 20, seed 42, paper learning rate 6e-4 for all networks)."""
import numpy as np, pandas as pd, os, json, time, sys, math, argparse
import torch, torch.nn as nn, torch.nn.functional as Fn
D = os.path.dirname(os.path.abspath(__file__)) + '/data/'
torch.set_num_threads(int(os.environ.get('TT', '4')))
P = np.load(D + 'prep.npz'); w5, R5, FD5 = P['w5'], P['R5'], P['FD5']
M = pd.read_csv(D + 'meta.csv'); SEL = json.load(open(D + 'fold_selection.json'))
BANDS = pd.DataFrame(np.hstack([R5, FD5]), columns=['R%d' % w for w in w5] + ['FD%d' % w for w in w5])
GR = [0, 1, 3, 5, 7, 9]; enc = {g: i for i, g in enumerate(GR)}

# ------------------------------------------------------------------ building blocks
class SE(nn.Module):
    def __init__(s, c, r=16): super().__init__(); s.f = nn.Sequential(nn.Linear(c, max(4, c // r)), nn.ReLU(), nn.Linear(max(4, c // r), c), nn.Sigmoid())
    def forward(s, x): return x * s.f(x.mean((2, 3)))[:, :, None, None]
class CBAM(nn.Module):
    def __init__(s, c, r=16, k=7):
        super().__init__(); s.mlp = nn.Sequential(nn.Linear(c, max(4, c // r)), nn.ReLU(), nn.Linear(max(4, c // r), c)); s.sp = nn.Conv2d(2, 1, k, padding=k // 2)
    def forward(s, x):
        a = torch.sigmoid(s.mlp(x.mean((2, 3))) + s.mlp(x.amax((2, 3))))[:, :, None, None]; x = x * a
        m = torch.cat([x.mean(1, keepdim=True), x.amax(1, keepdim=True)], 1); return x * torch.sigmoid(s.sp(m))
class TTB(nn.Module):
    def __init__(s, d=128, h=4, drop=0.03):
        super().__init__(); s.n1 = nn.LayerNorm(d); s.att = nn.MultiheadAttention(d, h, dropout=drop, batch_first=True); s.n2 = nn.LayerNorm(d)
        s.ff = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Dropout(drop), nn.Linear(4 * d, d), nn.Dropout(drop))
    def forward(s, x):
        h = s.n1(x); x = x + s.att(h, h, h, need_weights=False)[0]; return x + s.ff(s.n2(x))
class DTEDNet(nn.Module):
    """Embedding 3x3 conv (128) -> SE -> class token -> Dual Transformer Group (1 Kernel Transformer Block with CBAM + 4 Token Transformer Blocks) -> LN(class token) -> linear."""
    def __init__(s, k, nout, d=128, use_se=True, use_dtg=True, drop=0.03):
        super().__init__(); s.k, s.use_se, s.use_dtg = k, use_se, use_dtg
        s.emb = nn.Sequential(nn.Conv2d(1, d, 3, padding=1), nn.BatchNorm2d(d), nn.GELU()); s.se = SE(d) if use_se else nn.Identity()
        s.cls = nn.Parameter(torch.zeros(1, 1, d)); s.pos = nn.Parameter(torch.zeros(1, k * k + 1, d)); nn.init.trunc_normal_(s.pos, std=0.02)
        s.ktb = nn.Sequential(nn.Conv2d(d, d, 3, padding=1), nn.BatchNorm2d(d), nn.GELU()); s.cbam = CBAM(d)
        s.ttb = nn.Sequential(*[TTB(d, 4, drop) for _ in range(4)]); s.norm = nn.LayerNorm(d); s.head = nn.Linear(d, nout)
    def forward(s, x):
        z = s.se(s.emb(x))
        if not s.use_dtg: return s.head(s.norm(z.mean((2, 3))))
        z = z + s.cbam(s.ktb(z))                                     # Kernel Transformer Block (local spatial-channel attention)
        t = z.flatten(2).transpose(1, 2); t = torch.cat([s.cls.expand(len(t), -1, -1), t], 1) + s.pos
        t = s.ttb(t); return s.head(s.norm(t[:, 0]))
class Basic(nn.Module):
    def __init__(s, i, o, st):
        super().__init__(); s.c1 = nn.Conv2d(i, o, 3, st, 1, bias=False); s.b1 = nn.BatchNorm2d(o); s.c2 = nn.Conv2d(o, o, 3, 1, 1, bias=False); s.b2 = nn.BatchNorm2d(o)
        s.sc = nn.Sequential() if (st == 1 and i == o) else nn.Sequential(nn.Conv2d(i, o, 1, st, bias=False), nn.BatchNorm2d(o))
    def forward(s, x): return Fn.relu(s.b2(s.c2(Fn.relu(s.b1(s.c1(x))))) + s.sc(x))
class ResNet18(nn.Module):
    def __init__(s, nout, drop=0.03):
        super().__init__(); s.stem = nn.Sequential(nn.Conv2d(1, 64, 3, 1, 1, bias=False), nn.BatchNorm2d(64), nn.ReLU())
        L = []; i = 64
        for o, st in ((64, 1), (128, 2), (256, 2), (512, 2)): L += [Basic(i, o, st), Basic(o, o, 1)]; i = o
        s.layers = nn.Sequential(*L); s.drop = nn.Dropout(drop); s.fc = nn.Linear(512, nout)
    def forward(s, x): return s.fc(s.drop(s.layers(s.stem(x)).mean((2, 3))))
class MBConv(nn.Module):
    def __init__(s, i, o, e, k, st):
        super().__init__(); m = i * e; s.res = (st == 1 and i == o)
        L = ([nn.Conv2d(i, m, 1, bias=False), nn.BatchNorm2d(m), nn.SiLU()] if e != 1 else []) + [nn.Conv2d(m, m, k, st, k // 2, groups=m, bias=False), nn.BatchNorm2d(m), nn.SiLU()]
        s.pre = nn.Sequential(*L); s.se = nn.Sequential(nn.AdaptiveAvgPool2d(1), nn.Conv2d(m, max(1, i // 4), 1), nn.SiLU(), nn.Conv2d(max(1, i // 4), m, 1), nn.Sigmoid())
        s.post = nn.Sequential(nn.Conv2d(m, o, 1, bias=False), nn.BatchNorm2d(o))
    def forward(s, x):
        h = s.pre(x); h = h * s.se(h); h = s.post(h); return x + h if s.res else h
class EfficientNetB0(nn.Module):
    CFG = [(1, 16, 1, 1, 3), (6, 24, 2, 2, 3), (6, 40, 2, 2, 5), (6, 80, 3, 2, 3), (6, 112, 3, 1, 5), (6, 192, 4, 2, 5), (6, 320, 1, 1, 3)]
    def __init__(s, nout, drop=0.03):
        super().__init__(); s.stem = nn.Sequential(nn.Conv2d(1, 32, 3, 1, 1, bias=False), nn.BatchNorm2d(32), nn.SiLU()); L = []; i = 32
        for e, o, n, st, k in s.CFG:
            for j in range(n): L.append(MBConv(i, o, e, k, st if j == 0 else 1)); i = o
        s.blocks = nn.Sequential(*L); s.head = nn.Sequential(nn.Conv2d(i, 1280, 1, bias=False), nn.BatchNorm2d(1280), nn.SiLU()); s.drop = nn.Dropout(max(drop, 0.2)); s.fc = nn.Linear(1280, nout)
    def forward(s, x): return s.fc(s.drop(s.head(s.blocks(s.stem(x))).mean((2, 3))))
class LN2d(nn.Module):
    def __init__(s, c): super().__init__(); s.ln = nn.LayerNorm(c)
    def forward(s, x): return s.ln(x.permute(0, 2, 3, 1)).permute(0, 3, 1, 2)
class GRN(nn.Module):
    def __init__(s, c): super().__init__(); s.g = nn.Parameter(torch.zeros(1, 1, 1, c)); s.b = nn.Parameter(torch.zeros(1, 1, 1, c))
    def forward(s, x):
        gx = torch.norm(x, p=2, dim=(1, 2), keepdim=True); nx = gx / (gx.mean(-1, keepdim=True) + 1e-6); return s.g * (x * nx) + s.b + x
class CNBlock(nn.Module):
    def __init__(s, c):
        super().__init__(); s.dw = nn.Conv2d(c, c, 7, padding=3, groups=c); s.ln = nn.LayerNorm(c); s.p1 = nn.Linear(c, 4 * c); s.grn = GRN(4 * c); s.p2 = nn.Linear(4 * c, c)
    def forward(s, x):
        h = s.dw(x).permute(0, 2, 3, 1); h = s.p2(s.grn(Fn.gelu(s.p1(s.ln(h))))); return x + h.permute(0, 3, 1, 2)
class Down(nn.Module):
    def __init__(s, i, o): super().__init__(); s.ln = LN2d(i); s.c = nn.Conv2d(i, o, 2, 2)
    def forward(s, x):
        x = s.ln(x)
        if x.shape[-1] < 2: x = Fn.pad(x, (0, 1, 0, 1))
        return s.c(x)
class ConvNeXtV2Atto(nn.Module):
    def __init__(s, nout, dims=(40, 80, 160, 320), depths=(2, 2, 6, 2), drop=0.03):
        super().__init__(); s.stem = nn.Sequential(nn.Conv2d(1, dims[0], 2, 1), LN2d(dims[0])); S = []
        for i, (d, n) in enumerate(zip(dims, depths)):
            if i > 0: S.append(Down(dims[i - 1], d))
            S += [CNBlock(d) for _ in range(n)]
        s.stages = nn.Sequential(*S); s.norm = nn.LayerNorm(dims[-1]); s.drop = nn.Dropout(drop); s.fc = nn.Linear(dims[-1], nout)
    def forward(s, x): return s.fc(s.drop(s.norm(s.stages(s.stem(x)).mean((2, 3)))))
class DNNF1(nn.Module):
    def __init__(s, p, nout, drop=0.3):
        super().__init__(); s.f = nn.Sequential(nn.Linear(p, 64), nn.BatchNorm1d(64), nn.ReLU(), nn.Dropout(drop), nn.Linear(64, 32), nn.BatchNorm1d(32), nn.ReLU(), nn.Dropout(drop), nn.Linear(32, nout))
    def forward(s, x): return s.f(x.flatten(1))

def build(name, k, p, nout, drop):
    return {'DT-EDNet': lambda: DTEDNet(k, nout, drop=drop), 'DT-EDNet-SE': lambda: DTEDNet(k, nout, use_se=False, drop=drop), 'DT-EDNet-DTG': lambda: DTEDNet(k, nout, use_dtg=False, drop=drop),
            'DT-EDNet-SE-DTG': lambda: DTEDNet(k, nout, use_se=False, use_dtg=False, drop=drop), 'ResNet18': lambda: ResNet18(nout, drop), 'EfficientNet-B0': lambda: EfficientNetB0(nout, drop),
            'ConvNeXt V2-Atto': lambda: ConvNeXtV2Atto(nout, drop=drop), 'DNN-F1': lambda: DNNF1(p, nout)}[name]()

def pseudo(X):
    p = X.shape[1]; k = max(3, math.ceil(math.sqrt(p))); Z = np.zeros((len(X), k * k), np.float32); Z[:, :p] = X; return Z.reshape(-1, 1, k, k), k

def macro_f1(y, yp, K):
    f = []
    for c in range(K):
        tp = ((yp == c) & (y == c)).sum(); fp = ((yp == c) & (y != c)).sum(); fn = ((yp != c) & (y == c)).sum()
        f.append(0 if tp == 0 else 2 * tp / (2 * tp + fp + fn))
    return float(np.mean(f))

def run(net, task, f, cols, lr=6e-4, drop=0.03, epochs=100, patience=20, seed=42, tag=''):
    torch.manual_seed(seed); np.random.seed(seed)
    s = SEL[str(f)]; Ff = pd.read_csv(D + 'fold%d_indices.csv' % f); ALL = pd.concat([BANDS, Ff], axis=1)
    tr = (M.fold != f).values; te = ~tr
    plots_tr = np.unique(M['plot'].values[tr]); rng = np.random.default_rng(seed); val_plots = set(rng.choice(plots_tr, len(plots_tr) // 3, replace=False))
    va = tr & M['plot'].isin(val_plots).values; fit = tr & ~va
    X = ALL[cols].values.astype(np.float32); mu, sd = X[fit].mean(0), X[fit].std(0) + 1e-6; X = (X - mu) / sd
    if task == 'A': y = M.diseased.values; K = 2
    elif task == 'B': y = M.grade.map(enc).values; K = 6
    else: y = M.grade.values.astype(np.float32); K = 1
    Xi, k = (X.reshape(-1, 1, 1, X.shape[1]), 1) if net == 'DNN-F1' else pseudo(X); model = build(net, k, X.shape[1], K, drop)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-5); sch = torch.optim.lr_scheduler.CosineAnnealingLR(opt, epochs, eta_min=1e-6)
    if K > 1:
        cw = torch.tensor(len(y[fit]) / (K * np.bincount(y[fit], minlength=K).clip(1)), dtype=torch.float32); lossf = nn.CrossEntropyLoss(weight=cw, label_smoothing=0.01)
    else: lossf = nn.MSELoss()
    Xt = torch.tensor(Xi); yt = torch.tensor(y, dtype=torch.long if K > 1 else torch.float32)
    idx_fit = np.where(fit)[0]; best, bstate, bad, hist = -1e9, None, 0, []
    for ep in range(epochs):
        model.train(); perm = rng.permutation(idx_fit); tl = 0
        for b in range(0, len(perm), 32):
            ii = perm[b:b + 32]
            if len(ii) < 2: continue
            opt.zero_grad(); out = model(Xt[ii]); loss = lossf(out, yt[ii]) if K > 1 else lossf(out.ravel(), yt[ii]); loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.2); opt.step(); tl += loss.item() * len(ii)
        sch.step(); model.eval()
        with torch.no_grad():
            ov = model(Xt[va]); vl = (lossf(ov, yt[va]) if K > 1 else lossf(ov.ravel(), yt[va])).item()
            if K > 1: vs = macro_f1(y[va], ov.argmax(1).numpy(), K)
            else: vs = -float(np.sqrt(((ov.ravel().numpy() - y[va]) ** 2).mean()))
        hist.append((ep + 1, tl / len(idx_fit), vl, vs))
        if vs > best + 5e-5: best, bstate, bad = vs, {kk: v.clone() for kk, v in model.state_dict().items()}, 0
        else:
            bad += 1
            if bad >= patience: break
    model.load_state_dict(bstate); model.eval()
    with torch.no_grad():
        ot = model(Xt[te])
        if K > 1: pr = torch.softmax(ot, 1).numpy(); yp = pr.argmax(1); sc = pr[:, 1] if K == 2 else None
        else: yp = ot.ravel().numpy(); sc = None
    nparam = sum(p.numel() for p in model.parameters())
    return dict(net=net, task=task, fold=f, tag=tag, lr=lr, k=k, p=X.shape[1], epochs=len(hist), best_val=best, nparam=nparam,
                leaf=np.where(te)[0].tolist(), y=y[te].tolist(), pred=np.asarray(yp).tolist(), score=(None if sc is None else sc.tolist()), hist=hist)

def cols_for(f, cfg, task):
    s = SEL[str(f)]
    if cfg == 'DSF': return s['DSF'][task]
    if cfg == 'OW': return s['OW']
    if cfg == 'VI': return s['VI'][task]
    if cfg == 'OW+VI': return s['OW'] + [c for c in s['VI'][task] if c not in s['OW']]

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--stage', default='time'); a = ap.parse_args()
    NETS = ['DT-EDNet', 'EfficientNet-B0', 'ResNet18', 'ConvNeXt V2-Atto']
    if a.stage == 'time':
        for net in NETS + ['DNN-F1']:
            t0 = time.time(); r = run(net, 'B', 0, cols_for(0, 'DSF', 'B'), epochs=3, patience=99); print(net, 'k', r['k'], 'params', r['nparam'], '%.1fs per epoch' % ((time.time() - t0) / 3), flush=True)
        sys.exit()
    out = []
    def save(name): json.dump(out, open(D + 'dl_%s.json' % name, 'w'))
    if a.stage == 'tune':
        for net in NETS:
            for lr in (3e-4, 6e-4, 1e-3):
                r = run(net, 'B', 0, cols_for(0, 'DSF', 'B'), lr=lr, tag='tune'); out.append({kk: r[kk] for kk in ('net', 'lr', 'best_val', 'epochs')}); print(net, lr, '%.3f' % r['best_val'], r['epochs'], flush=True); save('tune')
    if a.stage == 'main':
        LR = {n: 6e-4 for n in NETS}; LR['DNN-F1'] = 1e-3          # paper settings, identical for all networks (Ma et al., 2026)
        for task in 'ABC':
            for net in ['DNN-F1'] + NETS:
                for f in range(3):
                    t0 = time.time(); r = run(net, task, f, cols_for(f, 'DSF', task), lr=LR[net], tag='DSF'); out.append(r); save('main')
                    print(task, net, f, 'val %.3f ep %d %.0fs' % (r['best_val'], r['epochs'], time.time() - t0), flush=True)
    if a.stage == 'config':
        LR = {n: 6e-4 for n in NETS}
        for cfg in ('OW', 'VI'):
            for net in NETS:
                for f in range(3):
                    r = run(net, 'B', f, cols_for(f, cfg, 'B'), lr=LR[net], tag=cfg); out.append(r); save('config'); print(cfg, net, f, 'val %.3f' % r['best_val'], flush=True)
    if a.stage == 'ablation':
        lr = 6e-4
        for net in ('DT-EDNet-SE', 'DT-EDNet-DTG', 'DT-EDNet-SE-DTG'):
            for f in range(3):
                r = run(net, 'B', f, cols_for(f, 'DSF', 'B'), lr=lr, tag='ablation'); out.append(r); save('ablation'); print(net, f, 'val %.3f' % r['best_val'], flush=True)
