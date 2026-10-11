"""prof2.py img xmin xmax [ymax=0.4] -> per panel 8 depth levels: CT (open) and ZT (filled) values.
x axis spans frame L..R = xmin..xmax; y frame top..bottom = 0..ymax; markers at layer mid-depths."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd
im = np.array(Image.open(sys.argv[1]).convert('L')).astype(int)
xmin, xmax = float(sys.argv[2]), float(sys.argv[3])
ymax = float(sys.argv[4]) if len(sys.argv) > 4 else 0.4
H, W = im.shape
dark = im < 120
rowfrac = dark.sum(axis=1) / W
g = []
for y in [y for y in range(H) if rowfrac[y] > 0.6]:
    if g and y - g[-1][-1] <= 3: g[-1].append(y)
    else: g.append([y])
hl = [int(np.mean(t)) for t in g]
import os
if os.environ.get('HL'): hl = [int(v) for v in os.environ['HL'].split(',')]
yy, xx = np.mgrid[-6:7, -6:7]
disk = (xx ** 2 + yy ** 2) <= 25
solid = nd.binary_opening(dark, structure=disk)
RR = np.hypot(*np.mgrid[-13:14, -13:14])
RING = (RR >= 9) & (RR <= 11.5)
INNER = RR <= 6.5
for p, (top, bot) in enumerate(zip(hl[0::2], hl[1::2])):
    band = dark[top + 3:bot - 3]
    cf = band.sum(axis=0) / band.shape[0]
    gv = []
    for x in [x for x in range(W) if cf[x] > 0.8]:
        if gv and x - gv[-1][-1] <= 3: gv[-1].append(x)
        else: gv.append([x])
    L, R = int(np.mean(gv[0])), int(np.mean(gv[-1]))
    fx = lambda x: xmin + (x - L) / (R - L) * (xmax - xmin)
    fy = lambda y: (y - top) / (bot - top) * ymax
    sub = solid[top + 3:bot - 3, L + 3:R - 3]
    lab, n = nd.label(sub)
    filled = [(c[0] + top + 3, c[1] + L + 3) for c, s in zip(nd.center_of_mass(sub, lab, range(1, n + 1)), nd.sum(sub, lab, range(1, n + 1))) if 150 < s < 700]
    light = ~dark[top + 3:bot - 3, L + 3:R - 3]
    lab2, n2 = nd.label(light)
    objs = nd.find_objects(lab2)
    opens = []
    for i, sl in enumerate(objs, 1):
        h_, w_ = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        a = (lab2[sl] == i).sum()
        if 6 <= h_ <= 26 and 6 <= w_ <= 26 and 40 <= a <= 500:
            c = nd.center_of_mass(lab2 == i)
            opens.append((c[0] + top + 3, c[1] + L + 3, a))
    # merge open fragments (a line through a ring splits it): cluster within 14 px
    cl = []
    for y, x, a in sorted(opens):
        for c in cl:
            if abs(c[0] - y) < 14 and abs(c[1] - x) < 14:
                c[2].append((y, x, a)); break
        else:
            cl.append([y, x, [(y, x, a)]])
    openc = []
    for c in cl:
        ys = sum(a * y for y, x, a in c[2]) / sum(a for _, _, a in c[2]); xs = sum(a * x for y, x, a in c[2]) / sum(a for _, _, a in c[2])
        openc.append((ys, xs, sum(a for _, _, a in c[2])))
    print(f'PANEL {p + 1}: L {L} R {R} top {top} bot {bot}')
    for k in range(8):
        d = 0.025 + 0.05 * k if ymax == 0.4 else None
        yc = top + d / ymax * (bot - top)
        f = [fx(x) for y, x in filled if abs(y - yc) < 12]
        o = [fx(x) for y, x, a in openc if abs(y - yc) < 12]
        # ring template match (robust when error bars / lines cross the ring)
        best = (-9, None, None)
        fxs = [x for y, x in filled if abs(y - yc) < 12]
        for y0 in range(int(yc) - 6, int(yc) + 7):
            for x0 in range(L + 14, R - 14):
                if any(abs(x0 - xf) < 18 for xf in fxs):
                    continue
                win = dark[y0 - 13:y0 + 14, x0 - 13:x0 + 14]
                sc = win[RING].mean() - win[INNER].mean()
                if sc > best[0]:
                    best = (sc, y0, x0)
        ring = (round(fx(best[2]), 3), round(best[0], 2))
        print(f'  depth {d:.3f}  CT(open) {[round(v, 3) for v in o]} ring {ring}  ZT(filled) {[round(v, 3) for v in f]}')
