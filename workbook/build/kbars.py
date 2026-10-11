"""Black / grey paired bars in a crop box: kbars.py img x0 y0 x1 y1 -> axis ticks (y px) and bar tops per bar (left to right)."""
import sys
import numpy as np
from PIL import Image
im = np.array(Image.open(sys.argv[1]).convert('L')).astype(int)
x0, y0, x1, y1 = map(int, sys.argv[2:6])
c = im[y0:y1, x0:x1]
dark = c < 90
col = dark.sum(axis=0)
ax = int(np.argmax(col[:len(col) // 3]))
rowd = dark.sum(axis=1)
base = int(np.argmax(rowd[len(rowd) // 2:])) + len(rowd) // 2
ticks = [y for y in range(c.shape[0]) if dark[y, max(ax - 14, 0):ax - 2].sum() >= 6 or dark[y, ax + 2:ax + 14].sum() >= 9]
g = []
for y in ticks:
    if g and y - g[-1][-1] <= 2: g[-1].append(y)
    else: g.append([y])
print('axis x', ax + x0, 'base y', base + y0, 'ticks', [round(np.mean(t) + y0, 1) for t in g])
blk = c < 60
gry = (c > 140) & (c < 225)
for name, m in (('black', blk), ('grey', gry)):
    cols = [x for x in range(ax + 5, c.shape[1]) if m[base - 30:base - 4, x].mean() > 0.9]
    sp = []
    for x in cols:
        if sp and x - sp[-1][-1] <= 2: sp[-1].append(x)
        else: sp.append([x])
    out = []
    for s in sp:
        if len(s) < 8: continue
        x = s[len(s) // 2]
        y = base - 4
        while y > 0 and m[y, x]: y -= 1
        out.append((s[0] + x0, s[-1] + x0, y + y0))
    print(name, out)
