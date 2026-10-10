"""Outlined (grayscale) bars: y-axis ticks at axis_x, bar top outline at given x positions.
usage: obars.py img axis_x ytop ybot x1,x2,... [dx]"""
import sys
from PIL import Image
import numpy as np
im=np.array(Image.open(sys.argv[1]).convert('L')).astype(int)
ax=int(sys.argv[2]); yt=int(sys.argv[3]); yb=int(sys.argv[4]); xs=[int(v) for v in sys.argv[5].split(',')]
dx=int(sys.argv[6]) if len(sys.argv)>6 else 12
# ticks: dark pixels just left of axis
rows=[y for y in range(yt,yb) if (im[y,ax-8:ax-1]<110).sum()>=4]
g=[]
for y in rows:
    if g and y-g[-1][-1]<=2: g[-1].append(y)
    else: g.append([y])
print('ticks',[round(sum(t)/len(t),1) for t in g])
for x in xs:
    tops=[]
    for xx in (x-dx,x+dx):
        col=im[yt:yb,xx]
        # first dark pixel scanning down
        ys=[i for i in range(len(col)) if col[i]<110]
        tops.append(yt+ys[0] if ys else None)
    print(x,tops)
