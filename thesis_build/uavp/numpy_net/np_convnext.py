"""ConvNeXt V2-Atto forward pass in NumPy (no PyTorch): same layers and order as the PyTorch model of the ASD analysis
(stride-1 stem for the k x k pseudo-image, LayerNorm, depthwise 7x7, GRN, GELU, downsampling with padding for 1x1 maps)."""
import numpy as np
from scipy.special import erf
def layernorm(x, w, b, eps=1e-5):                       # over the last axis
    m = x.mean(-1, keepdims=True); v = ((x - m) ** 2).mean(-1, keepdims=True); return (x - m) / np.sqrt(v + eps) * w + b
def ln2d(x, w, b):                                      # x (N, C, H, W): LayerNorm over C at every position
    return layernorm(x.transpose(0, 2, 3, 1), w, b).transpose(0, 3, 1, 2)
def conv2d(x, w, b, stride):                            # x (N, Ci, H, W), w (Co, Ci, kh, kw), no padding
    N, Ci, H, W = x.shape; Co, _, kh, kw = w.shape; Ho, Wo = (H - kh) // stride + 1, (W - kw) // stride + 1
    out = np.zeros((N, Ho, Wo, Co), np.float32)
    for dy in range(kh):
        for dx in range(kw):
            patch = x[:, :, dy:dy + stride * (Ho - 1) + 1:stride, dx:dx + stride * (Wo - 1) + 1:stride]   # (N, Ci, Ho, Wo)
            out += np.einsum('nihw,oi->nhwo', patch, w[:, :, dy, dx], optimize=True)
    return (out + b).transpose(0, 3, 1, 2)
def dwconv7(x, w, b):                                   # depthwise 7x7, padding 3; x (N, C, H, W), w (C, 1, 7, 7)
    N, C, H, W = x.shape; xp = np.zeros((N, C, H + 6, W + 6), np.float32); xp[:, :, 3:3 + H, 3:3 + W] = x; out = np.zeros_like(x)
    for dy in range(7):
        for dx in range(7):
            ys, xs = slice(dy, dy + H), slice(dx, dx + W)
            if not (dy + H > 3 and dy < 3 + H and dx + W > 3 and dx < 3 + W): continue     # window only sees padding
            out += xp[:, :, ys, xs] * w[:, 0, dy, dx][None, :, None, None]
    return out + b[None, :, None, None]
def gelu(x): return 0.5 * x * (1.0 + erf(x / np.sqrt(2.0)))
def cnblock(x, P, p):                                   # residual ConvNeXt V2 block
    h = dwconv7(x, P[p + 'dw.weight'], P[p + 'dw.bias']).transpose(0, 2, 3, 1)          # (N, H, W, C)
    h = layernorm(h, P[p + 'ln.weight'], P[p + 'ln.bias']); h = gelu(h @ P[p + 'p1.weight'].T + P[p + 'p1.bias'])
    gx = np.sqrt((h ** 2).sum(axis=(1, 2), keepdims=True)); nx = gx / (gx.mean(-1, keepdims=True) + 1e-6)
    h = P[p + 'grn.g'] * (h * nx) + P[p + 'grn.b'] + h
    h = h @ P[p + 'p2.weight'].T + P[p + 'p2.bias']; return x + h.transpose(0, 3, 1, 2)
def down(x, P, p):
    x = ln2d(x, P[p + 'ln.ln.weight'], P[p + 'ln.ln.bias'])
    if x.shape[-1] < 2: x = np.pad(x, ((0, 0), (0, 0), (0, 1), (0, 1)))
    return conv2d(x, P[p + 'c.weight'], P[p + 'c.bias'], 2)
def convnext_forward(X, P, depths=(2, 2, 6, 2)):
    """X: (N, 1, k, k) float32 pseudo-images; P: dict of the PyTorch state_dict arrays -> raw outputs (N, n_out)"""
    x = conv2d(X.astype(np.float32), P['stem.0.weight'], P['stem.0.bias'], 1); x = ln2d(x, P['stem.1.ln.weight'], P['stem.1.ln.bias'])
    i = 0
    for s, n in enumerate(depths):
        if s > 0: x = down(x, P, 'stages.%d.' % i); i += 1
        for _ in range(n): x = cnblock(x, P, 'stages.%d.' % i); i += 1
    x = layernorm(x.mean(axis=(2, 3)), P['norm.weight'], P['norm.bias'])
    return x @ P['fc.weight'].T + P['fc.bias']
