import sys
from PIL import Image
import numpy as np
im=np.array(Image.open(sys.argv[1]).convert('L')).astype(int)
x0,x1=int(sys.argv[2]),int(sys.argv[3])
H,W=im.shape
cands=[(int((im[:,x]<130).sum()),x) for x in range(x0,x1)]
ax=max(cands)[1]
ticks=[y for y in range(H) if (im[y,ax-6:ax-1]<130).sum()>=3]
g=[]
for y in ticks:
    if g and y-g[-1][-1]<=2: g[-1].append(y)
    else: g.append([y])
tk=[round(sum(t)/len(t),1) for t in g]
print('axis',ax,'ticks',tk)
base=int(max(tk))
row=im[base-6,ax+3:]
xs=[x+ax+3 for x,v in enumerate(row) if v<215]
spans=[]
for x in xs:
    if spans and x-spans[-1][-1]<=1: spans[-1].append(x)
    else: spans.append([x])
for s in spans:
    if len(s)<6: continue
    a,b=s[0],s[-1]; tops=[]
    for x in (a+3,b-3):
        y=base-6
        while y>0 and im[y,x]<215: y-=1
        tops.append(y+1)
    print(f'bar x{a}-{b} shade{int(np.median(im[base-20,a+2:b-2]))} tops{tops}')
