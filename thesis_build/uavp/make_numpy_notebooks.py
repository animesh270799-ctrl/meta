"""PyTorch-free versions of the ConvNeXt V2-Atto pixel-map notebooks (for PCs where 'import torch' fails, e.g. WinError 1114 c10.dll).
The network runs in NumPy (numpy_net/np_convnext.py, verified against PyTorch: max probability difference ~1e-6, identical classes);
weights come from <key>_numpy.npz. Built from the PyTorch notebooks of make_model_notebooks.py by replacing the torch-specific cells.
Output: uavp/kit/per_model/<key>_pixel_map_24Feb2026_NO_TORCH.ipynb"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'; PM = HERE + 'kit/per_model/'
NPNET = open(HERE + 'numpy_net/np_convnext.py').read(); NPNET = NPNET[NPNET.index('import numpy as np'):]
NPNET = NPNET.replace('import numpy as np\nfrom scipy.special import erf\n', 'from scipy.special import erf\n')
PSEUDO = "def pseudo(X):\n    p = X.shape[1]; k = max(3, math.ceil(math.sqrt(p))); Z = np.zeros((len(X), k * k), np.float32); Z[:, :p] = X; return Z.reshape(-1, 1, k, k)"
LOAD = {'A': "def OUTPUT(o):   # detection: softmax probability of 'diseased' and class (probability >= THRESHOLD)\n    p = np.exp(o - o.max(1, keepdims=True)); p /= p.sum(1, keepdims=True); return p[:, 1], (p[:, 1] >= THRESHOLD).astype(int)",
        'B': "def OUTPUT(o):   # six grades: class with the largest output -> grade 0, 1, 3, 5, 7 or 9\n    g = np.array(GRADES)[o.argmax(1)]; return g.astype(float), g"}
def src(c): return ''.join(c['source'])
def put(c, t): c['source'] = [l + '\n' for l in t.split('\n')]; c['source'][-1] = c['source'][-1].rstrip('\n')
for key in ('A_ConvNeXt_V2-Atto', 'B_ConvNeXt_V2-Atto'):
    nb = json.load(open(PM + key + '_pixel_map_24Feb2026.ipynb')); C = nb['cells']; task = key[0]
    for c in C:
        s = src(c)
        if c['cell_type'] == 'markdown' and s.startswith('# White rust pixel map'):
            s = s.replace('# White rust pixel map – ConvNeXt V2-Atto', '# White rust pixel map – ConvNeXt V2-Atto (NumPy version, no PyTorch needed)', 1)
            s = re.sub(r"\*\*Requirements\.\*\*[^\n]*", "**Requirements.** Python 3.9+, `numpy`, `scipy`, `pandas`, `matplotlib`; optional `rasterio` for GeoTIFF. **No PyTorch**: the network runs in NumPy with the weights in `%s_numpy.npz` (identical results to the PyTorch model, maximum probability difference about 0.000002)." % key, s)
            s = s.replace('· 3 network ·', '· 3 network (NumPy) ·'); put(c, s)
        elif c['cell_type'] == 'code' and s.startswith('%pip'): put(c, '%pip install -q numpy scipy pandas matplotlib rasterio')
        elif c['cell_type'] == 'code' and s.startswith('# ============================ SETTINGS'):
            s = s.replace("models\\%s.pt'   # this model (from the kit's 'models' folder)" % key, "models\\%s_numpy.npz'   # this model, NumPy weights (from the kit's 'models' folder)" % key)
            s = s.replace("BATCH  = 32768          # pixels per network batch\nDEVICE = 'cpu'", "BATCH  = 8192           # pixels per network batch (reduce to 4096 if memory is short)")
            assert '_numpy.npz' in s and 'DEVICE' not in s; put(c, s)
        elif c['cell_type'] == 'code' and s.startswith('import torch'):
            put(c, s.split('\n', 1)[1])
        elif c['cell_type'] == 'markdown' and s.startswith('## 3 Network'):
            put(c, '## 3 Network (NumPy)\nConvNeXt V2-Atto (Woo et al., 2023) written in NumPy: the same layers and order as the PyTorch model of the ASD analysis – stride-1 stem for the k × k pseudo-image (features written into a k × k grid, zero-padded; Sharma et al., 2019), LayerNorm, depthwise 7 × 7 convolution, global response normalisation (GRN), GELU, and down-sampling with padding for 1 × 1 maps. Checked against PyTorch: identical classes, probabilities within 0.000002.')
        elif c['cell_type'] == 'code' and s.startswith('class LN2d'):
            put(c, NPNET.rstrip() + '\n' + PSEUDO)
        elif c['cell_type'] == 'code' and s.startswith('REF_FILE'):
            put(c, s.replace("REF_FILE = os.path.splitext(MODEL_FILE)[0] + '_reference.json'     # reference data, stored next to the model file",
                             "REF_FILE = os.path.join(os.path.dirname(MODEL_FILE), '%s_reference.json')     # reference data, stored next to the model file" % key))
        elif c['cell_type'] == 'markdown' and s.startswith('## 6 Load the model'):
            put(c, '## 6 Load the model\nThe network weights are read from the `.npz` file (plain NumPy arrays); inputs are standardised with the training mean and SD stored in the file.')
        elif c['cell_type'] == 'code' and s.startswith('def OUTPUT'):
            put(c, LOAD[task] + r"""
_z = np.load(MODEL_FILE, allow_pickle=False); P = {k[3:]: _z[k] for k in _z.files if k.startswith('w__')}
FEATURES = [str(f) for f in _z['features']]; MU, SD = _z['scaler_mean'], _z['scaler_sd']
def predict(S):
    # spectra -> features -> k x k pseudo-image -> ConvNeXt V2-Atto (NumPy)
    Z = ((features(make_variant(S, VARIANT), FEATURES, OP) - MU) / SD).astype(np.float32); outs = []
    for i in range(0, len(Z), BATCH): outs.append(convnext_forward(pseudo(Z[i:i + BATCH]), P))
    return OUTPUT(np.concatenate(outs))
print(f'ConvNeXt V2-Atto (NumPy): {sum(v.size for v in P.values()):,} parameters; features: {", ".join(FEATURES)}')
OP = build_operator(FEATURES)""")
    txt = json.dumps(nb)
    assert 'torch' not in ''.join(src(c) for c in C if c['cell_type'] == 'code'), key
    json.dump(nb, open(PM + key + '_pixel_map_24Feb2026_NO_TORCH.ipynb', 'w'), indent=1); print('written', key + '_pixel_map_24Feb2026_NO_TORCH.ipynb')
