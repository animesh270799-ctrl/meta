"""Colour bar digitiser: python3 cbars.py img x0 x1 y0 y1  -> axis ticks and colour-bar tops.
Finds y-axis (darkest column in x0..x1 within y0..y1), ticks, then bars of red / blue / other non-grey fill."""
import sys
from PIL import Image
import numpy as np
im = np.array(Image.open(sys.argv[1]).convert('RGB')).astype(int)
x0, x1, y0, y1 = map(int, sys.argv[2:6])
g = im.mean(axis=2)
cands = [(int((g[y0:y1, x] < 100).sum()), x) for x in range(x0, x1)]
ax = max(cands)[1]
ticks = [y for y in range(y0, y1) if (g[y, ax - 12:ax - 2] < 100).sum() >= 6]
gg = []
for y in ticks:
    if gg and y - gg[-1][-1] <= 2: gg[-1].append(y)
    else: gg.append([y])
print('axis', ax, 'ticks', [round(sum(t) / len(t), 1) for t in gg])
R, G, B = im[..., 0], im[..., 1], im[..., 2]
red = (R > 150) & (G < 90) & (B < 90)
blue = (B > 150) & (R < 90) & (G < 120)
for name, m in (('red', red), ('blue', blue)):
    cols = [x for x in range(ax + 3, im.shape[1]) if m[y0:y1, x].sum() > 15]
    sp = []
    for x in cols:
        if sp and x - sp[-1][-1] <= 2: sp[-1].append(x)
        else: sp.append([x])
    out = []
    for s in sp:
        if len(s) < 8: continue
        xs = [s[2], s[len(s) // 4], s[-len(s) // 4], s[-3]]
        tops = []
        for x in xs:
            ys = np.where(m[y0:y1, x])[0]
            tops.append(y0 + ys.min() if len(ys) else None)
        out.append((s[0], s[-1], sorted(t for t in tops if t is not None)))
    print(name, len(out))
    for o in out: print('  ', o)
