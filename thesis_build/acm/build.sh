set -e
cd /home/user/meta/thesis_build/acm
python3 acm_refs.py
NODE_PATH=/home/user/meta/thesis_build/leaf/node_modules node acm_ppt.js
S=/root/.claude/skills/synced/9bf50f97-a337-4b6b-8c8b-ebd229b7e0d3_d565bc3b-4006-4195-b033-a8c25dfdc114/pptx/scripts
python3 $S/office/validate.py ../outputs/Advisory_committee_ORW_updated_methodology.pptx | tail -1
R=/tmp/claude-0/-home-user-meta/c5704ca0-f1ca-5695-b9e0-a810fbe166a9/scratchpad/acm/r1; mkdir -p $R; rm -f "${R:?}"/s-*.png
python3 $S/office/soffice.py --headless --convert-to pdf --outdir $R ../outputs/Advisory_committee_ORW_updated_methodology.pptx >/dev/null 2>&1
pdfinfo $R/Advisory_committee_ORW_updated_methodology.pdf | grep Pages
pdftoppm -r 50 -png $R/Advisory_committee_ORW_updated_methodology.pdf $R/s
python3 -c "
from PIL import Image;import glob
fs=sorted(glob.glob('$R/s-*.png'));ims=[Image.open(f) for f in fs];w,h=ims[0].size
for j in range(0,len(fs),9):
    S=Image.new('RGB',(w*3+20,h*3+20),'grey')
    for i,im in enumerate(ims[j:j+9]):S.paste(im,((i%3)*(w+10),(i//3)*(h+10)))
    S.save('$R/sheet%d.png'%(j//9))
print(len(fs))"
