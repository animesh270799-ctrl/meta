"""Ticks on y-axis + tops of bars of given colour classes. usage: bars2.py img x0 y0 x1 y1"""
import sys
from PIL import Image
import numpy as np
im=np.array(Image.open(sys.argv[1]).convert('RGB')).astype(int)
x0,y0,x1,y1=map(int,sys.argv[2:6])
sub=im[y0:y1,x0:x1]
dark=(sub.sum(axis=2)<330)
best=(0,0)
for x in range(sub.shape[1]):
    col=dark[:,x]; run=m=0
    for v in col:
        run=run+1 if v else 0; m=max(m,run)
    if m>best[0]: best=(m,x)
ax=best[1]
ticks=[y for y in range(sub.shape[0]) if dark[y,max(0,ax-6):ax-1].sum()>=3]
g=[]
for y in ticks:
    if g and y-g[-1][-1]<=2: g[-1].append(y)
    else: g.append([y])
print('axis_x',x0+ax,'ticks',[round(y0+sum(t)/len(t),1) for t in g])
r,gg,b=sub[:,:,0],sub[:,:,1],sub[:,:,2]
classes={'blue':(b>150)&(r<90)&(gg>100)&(gg<200),'orange':(r>200)&(gg>90)&(gg<170)&(b<80)}
for name,mask in classes.items():
    cols=np.where(mask.sum(axis=0)>10)[0]; bars=[]
    for c in cols:
        if bars and c-bars[-1][-1]<=2: bars[-1].append(c)
        else: bars.append([c])
    out=[]
    for bc in bars:
        if len(bc)<8: continue
        xs=bc[2:-2]
        tops=[np.where(mask[:,c])[0].min() for c in xs]
        out.append((x0+bc[len(bc)//2], y0+float(np.median(tops))))
    print(name,[(int(m),t) for m,t in out])
