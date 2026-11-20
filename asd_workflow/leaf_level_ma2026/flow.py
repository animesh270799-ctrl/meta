import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

W, H = 7.4, 9.0
fig = plt.figure(figsize=(W, H)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
def box(x, y, w, h, t, fc, ec, fs=6.9, tc="#1B2A34"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.06", fc=fc, ec=ec, lw=1))
    L = t.split("\n"); lh = fs / 72 * 1.3; y0 = y + h / 2 + (len(L) - 1) * lh / 2
    for i, l in enumerate(L): ax.text(x + w / 2, y0 - i * lh, l, ha="center", va="center", fontsize=fs, fontweight="bold" if i == 0 else "normal", color=tc)
def ar(x1, y1, x2, y2): ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color="#4A5560", lw=0.9, mutation_scale=8))
A = ("#DCEBF7", "#2F6E9E"); P = ("#E4F1E4", "#3C7D3C"); F = ("#FFF1D6", "#B7791F"); M = ("#FDE3E1", "#B24A3F"); V = ("#E1F2F2", "#1F6F78"); I = ("#EFE6F6", "#6B4C8A")
ax.text(W / 2, H - 0.25, "Leaf-level workflow following Ma et al. (2026) – ASD contact-probe spectra (no texture: non-imaging data)", ha="center", fontsize=8.6, fontweight="bold")
box(0.3, 7.85, 3.3, 0.75, "Step 1  Data\n4 dates (11 Feb – 13 Mar 2026), 48 plots, V1–V3\nASD contact probe, 350–2500 nm\n2,264 leaves (75 duplicates removed)", *A)
box(3.8, 7.85, 3.3, 0.75, "Step 2  Leaf labels (paper Tables II–IV)\nLeaf score 0/1/3/5/7/9 → Levels L0–L4\nOne leaf = one sample", *A)
box(0.3, 6.85, 6.8, 0.7, "Step 3  Pre-processing\nSplice correction (1000, 1800 nm) → Savitzky–Golay (11, 2) → whole range 350–2500 nm kept\n(water-absorption bands retained: contact probe) → 215 bands of 10 nm", *P)
ar(1.95, 7.85, 1.95, 7.55); ar(5.45, 7.85, 5.45, 7.55)
box(0.3, 5.85, 3.3, 0.7, "Step 4  Spectral curves (Fig. 6)\nMean reflectance by severity level", *P)
box(3.8, 5.85, 3.3, 0.7, "Step 5  NDSI / RSI (Fig. 7)\nR² of all band pairs with leaf score\n→ effective ranges (R² ≥ 0.25)", *P)
ar(1.95, 6.85, 1.95, 6.55); ar(5.45, 6.85, 5.45, 6.55)
ax.text(W / 2, 5.57, "Selected INSIDE each training fold", ha="center", fontsize=7.2, fontweight="bold", color="#B7791F", zorder=10, bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="none"))
box(0.3, 4.35, 3.3, 1.0, "Step 6  Optimal wavelengths (Table VII, Fig. 8)\non effective-range bands\nRFE-RF (10) | SAND (w > 0.524) | CARS-PLS\nCARS bands = OWs", *F)
box(3.8, 4.35, 3.3, 1.0, "Step 7  Vegetation indices (Tables V, VIII)\n16 paper indices + PSRI\ncorrelation (Fig. 9) → Relief top 5 (Fig. 10a)\nTexture features / TTFI: not applicable", *F)
ar(5.45, 5.85, 5.45, 5.35); ar(1.95, 5.85, 1.95, 5.35)
box(0.3, 3.35, 6.8, 0.7, "Inputs (Tables X–XII)\nSingle: RFE-RF | SAND | CARS-PLS | VIs     Baseline: full wavelength 350–2500 nm\nFused: OWs + VIs", *I)
ar(1.95, 4.35, 1.95, 4.05); ar(5.45, 4.35, 5.45, 4.05)
box(0.3, 2.4, 6.8, 0.65, "Step 8  Classifiers (paper: DT-EDNet, EfficientNet, ResNet18, ConvNeXt V2)\nHere: random forest | SVM (RBF) | PLS-DA | MLP neural network (class-balanced)", *M)
ar(W / 2, 3.35, W / 2, 3.05)
box(0.3, 1.25, 3.3, 0.85, "Step 9  Internal validation\n5-fold CV grouped by plot\n11 Feb, 24 Feb, 3 Mar (1,616 leaves)", *V)
box(3.8, 1.25, 3.3, 0.85, "Step 10  Independent validation (Table XIII)\nTrain: 3 dates → test: 13 Mar\n(648 leaves; paper: 2024 site)", *V)
ar(1.95, 2.4, 1.95, 2.1); ar(5.45, 2.4, 5.45, 2.1)
box(0.3, 0.3, 6.8, 0.7, "Metrics (Eq. 7–11)\nOA, Cohen’s kappa, macro recall, macro F1, per-level F1 (+ quadratic-weighted kappa, confusion matrices)", "#1F6F78", "#1F6F78", tc="white")
ar(1.95, 1.25, 1.95, 1.0); ar(5.45, 1.25, 5.45, 1.0)
fig.savefig(sys.argv[1], dpi=250); print("saved")
