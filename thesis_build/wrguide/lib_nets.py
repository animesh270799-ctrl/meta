"""Network definitions used for the white rust leaf models (copied from a4_dl.py): DT-EDNet (Ma et al., 2026), EfficientNet-B0, ResNet18,
ConvNeXt V2-Atto (stride-1 stems for small pseudo-images) and DNN-F1. Needed to rebuild the saved PyTorch state dicts."""
import math, numpy as np, torch, torch.nn as nn, torch.nn.functional as Fn

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

