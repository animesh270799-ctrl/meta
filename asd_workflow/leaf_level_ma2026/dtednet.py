"""DT-EDNet (Ma et al., 2026, IJAM 56(11)) re-implemented from the paper's description, plus CNN baselines.
Input: a 1-D feature vector, zero-padded and reshaped into a pseudo-2-D map (as described in Section II-G).
DT-EDNet: 3x3 conv embedding (dim 128) -> SE block -> learnable class token -> Dual Transformer Group
(1 Kernel Transformer Block with CBAM + 4 Token Transformer Blocks with 4-head self-attention) -> LayerNorm -> linear head.
Training follows Section II-G: AdamW (lr 6e-4, wd 1e-5), cosine schedule to 1e-6 over 300 epochs, batch 32,
label smoothing 0.01, gradient clipping 1.2, early stopping (patience 60, min delta 5e-5) on validation OA, seed 42.
"""
import math, copy, time
import numpy as np, torch, torch.nn as nn, torch.nn.functional as Fn
import timm


def to_map(X, side=None):
    n, p = X.shape; s = side or math.ceil(math.sqrt(p))
    out = np.zeros((n, s * s), np.float32); out[:, :p] = X
    return out.reshape(n, 1, s, s), s


class SE(nn.Module):
    def __init__(self, c, r=8):
        super().__init__(); self.fc = nn.Sequential(nn.Linear(c, c // r), nn.ReLU(), nn.Linear(c // r, c), nn.Sigmoid())
    def forward(self, x): return x * self.fc(x.mean((2, 3)))[:, :, None, None]


class CBAM(nn.Module):
    def __init__(self, c, r=8):
        super().__init__(); self.mlp = nn.Sequential(nn.Linear(c, c // r), nn.ReLU(), nn.Linear(c // r, c)); self.sp = nn.Conv2d(2, 1, 7, padding=3)
    def forward(self, x):
        ca = torch.sigmoid(self.mlp(x.mean((2, 3))) + self.mlp(x.amax((2, 3))))[:, :, None, None]; x = x * ca
        sa = torch.sigmoid(self.sp(torch.cat([x.mean(1, keepdim=True), x.amax(1, keepdim=True)], 1))); return x * sa


class FFN(nn.Module):
    def __init__(self, d, mult=2, p=0.03):
        super().__init__(); self.net = nn.Sequential(nn.Linear(d, d * mult), nn.GELU(), nn.Dropout(p), nn.Linear(d * mult, d), nn.Dropout(p))
    def forward(self, x): return self.net(x)


class KTB(nn.Module):
    """Kernel Transformer Block: LayerNorm -> depthwise 3x3 conv + CBAM (local spatial-channel attention) -> LayerNorm -> FFN."""
    def __init__(self, d, p=0.03):
        super().__init__(); self.n1 = nn.LayerNorm(d); self.conv = nn.Conv2d(d, d, 3, padding=1, groups=d); self.cbam = CBAM(d); self.n2 = nn.LayerNorm(d); self.ffn = FFN(d, p=p)
    def forward(self, x):  # x: B,C,H,W
        y = self.n1(x.permute(0, 2, 3, 1)).permute(0, 3, 1, 2); x = x + self.cbam(self.conv(y))
        return x + self.ffn(self.n2(x.permute(0, 2, 3, 1))).permute(0, 3, 1, 2)


class TTB(nn.Module):
    """Token Transformer Block: pre-norm multi-head self-attention + FFN."""
    def __init__(self, d, heads=4, p=0.03):
        super().__init__(); self.n1 = nn.LayerNorm(d); self.att = nn.MultiheadAttention(d, heads, dropout=p, batch_first=True); self.n2 = nn.LayerNorm(d); self.ffn = FFN(d, p=p)
    def forward(self, t):
        y = self.n1(t); t = t + self.att(y, y, y, need_weights=False)[0]; return t + self.ffn(self.n2(t))


class DTEDNet(nn.Module):
    def __init__(self, side, n_classes=5, d=128, heads=4, n_ttb=4, p=0.03, use_se=True, use_dtg=True):
        super().__init__(); self.use_se, self.use_dtg = use_se, use_dtg
        self.embed = nn.Sequential(nn.Conv2d(1, d, 3, padding=1), nn.BatchNorm2d(d), nn.GELU())
        self.se = SE(d) if use_se else nn.Identity()
        if use_dtg:
            self.ktb = KTB(d, p); self.cls = nn.Parameter(torch.zeros(1, 1, d)); self.pos = nn.Parameter(torch.zeros(1, side * side + 1, d))
            nn.init.trunc_normal_(self.pos, std=0.02); nn.init.trunc_normal_(self.cls, std=0.02)
            self.ttb = nn.Sequential(*[TTB(d, heads, p) for _ in range(n_ttb)])
        self.norm = nn.LayerNorm(d); self.head = nn.Linear(d, n_classes)
    def forward(self, x):
        x = self.se(self.embed(x))
        if not self.use_dtg: return self.head(self.norm(x.mean((2, 3))))
        x = self.ktb(x); t = x.flatten(2).transpose(1, 2)
        t = torch.cat([self.cls.expand(len(t), -1, -1), t], 1) + self.pos
        t = self.ttb(t); return self.head(self.norm(t[:, 0]))


def make_model(name, side, n_classes=5):
    if name == "DT-EDNet": return DTEDNet(side, n_classes)
    if name == "DT-EDNet-SE": return DTEDNet(side, n_classes, use_se=False)
    if name == "DT-EDNet-DTG": return DTEDNet(side, n_classes, use_dtg=False)
    if name == "DT-EDNet-SE-DTG": return DTEDNet(side, n_classes, use_se=False, use_dtg=False)
    timm_name = {"EfficientNet": "efficientnet_b0", "ResNet18": "resnet18", "ConvNeXt V2": "convnextv2_atto"}[name]
    return timm.create_model(timm_name, pretrained=False, in_chans=1, num_classes=n_classes, drop_rate=0.03)

CNN_SIZE = 32  # CNN inputs: pseudo-2-D map resized to 32 x 32 (bilinear) so that 32x down-sampling leaves a 1x1 map


def prep(Xmap, name):
    x = torch.from_numpy(Xmap)
    if not name.startswith("DT-EDNet"): x = Fn.interpolate(x, size=(CNN_SIZE, CNN_SIZE), mode="bilinear", align_corners=False)
    return x


def train_eval(name, Xtr, ytr, Xva, yva, Xte, seed=42, epochs=300, batch=32, lr=6e-4, wd=1e-5, patience=60, min_delta=5e-5, log=None):
    torch.manual_seed(seed); np.random.seed(seed); torch.use_deterministic_algorithms(True, warn_only=True)
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-8
    Mtr, side = to_map((Xtr - mu) / sd); Mva, _ = to_map((Xva - mu) / sd, side); Mte, _ = to_map((Xte - mu) / sd, side)
    xtr, xva, xte = prep(Mtr, name), prep(Mva, name), prep(Mte, name)
    ytr_t = torch.from_numpy(ytr.astype(np.int64))
    model = make_model(name, side); opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=wd)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=epochs, eta_min=1e-6)
    lossf = nn.CrossEntropyLoss(label_smoothing=0.01)
    g = torch.Generator().manual_seed(seed); best, best_state, wait, hist = -1, None, 0, []
    for ep in range(epochs):
        model.train(); perm = torch.randperm(len(xtr), generator=g)
        for i in range(0, len(perm), batch):
            idx = perm[i:i + batch]
            if len(idx) < 2: continue
            opt.zero_grad(); loss = lossf(model(xtr[idx]), ytr_t[idx]); loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.2); opt.step()
        sched.step(); model.eval()
        with torch.no_grad(): va_oa = (model(xva).argmax(1).numpy() == yva).mean()
        hist.append(float(va_oa))
        if va_oa > best + min_delta: best, best_state, wait = va_oa, copy.deepcopy(model.state_dict()), 0
        else:
            wait += 1
            if wait >= patience: break
    model.load_state_dict(best_state); model.eval()
    with torch.no_grad(): pred = model(xte).argmax(1).numpy()
    n_par = sum(p.numel() for p in model.parameters())
    return pred, dict(epochs_run=ep + 1, best_val_oa=float(best), n_params=int(n_par), val_curve=hist)
