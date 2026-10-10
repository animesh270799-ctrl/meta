"""Find y-axis ticks and blue bar tops inside a panel box. usage: bars.py img x0 y0 x1 y1"""
import sys
from PIL import Image
import numpy as np
im=np.array(Image.open(sys.argv[1]).convert('RGB')).astype(int)
x0,y0,x1,y1=map(int,sys.argv[2:6])
sub=im[y0:y1,x0:x1]
dark=(sub.sum(axis=2)<200)
# y-axis: column with longest dark run
best=(0,0)
for x in range(sub.shape[1]):
    col=dark[:,x]; run=m=0
    for v in col:
        run=run+1 if v else 0; m=max(m,run)
    if m>best[0]: best=(m,x)
ax=best[1]
# ticks: rows where pixels at ax-6..ax-2 dark
ticks=[y for y in range(sub.shape[0]) if dark[y,max(0,ax-7):ax-1].sum()>=4]
# group
g=[];
for y in ticks:
    if g and y-g[-1][-1]<=2: g[-1].append(y)
    else: g.append([y])
tick_y=[y0+sum(t)/len(t) for t in g]
# blue bars
r,gg,b=sub[:,:,0],sub[:,:,1],sub[:,:,2]
blue=(b>150)&(r<80)&(gg>100)&(gg<190)
cols=np.where(blue.sum(axis=0)>20)[0]
bars=[];
for c in cols:
    if bars and c-bars[-1][-1]<=2: bars[-1].append(c)
    else: bars.append([c])
out=[]
for bc in bars:
    if len(bc)<15: continue
    mid=bc[len(bc)//2]; xs=bc[3:-3] if len(bc)>8 else bc
    # top = first blue row (median over columns)
    tops=[np.where(blue[:,c])[0].min() for c in xs]
    out.append((x0+mid, y0+float(np.median(tops))))
print('axis_x',x0+ax,'ticks',[round(t,1) for t in tick_y])
print('bars',[(m,round(t,1)) for m,t in out])
