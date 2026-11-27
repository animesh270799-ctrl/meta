"""Scatter charts: put the x axis (and its labels) at the bottom of the plot (crosses = min) so labels never sit on the zero line."""
import sys, re, zipfile, os
src = sys.argv[1]; tmp = src + '.tmp'; zin = zipfile.ZipFile(src); zout = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED); n = 0
def fix_ax(m):
    ax = m.group(0)
    if '<c:axPos val="b"/>' in ax: ax = ax.replace('<c:crosses val="autoZero"/>', '<c:crosses val="min"/>')
    return ax
for it in zin.infolist():
    if it.filename.endswith('/'): continue
    d = zin.read(it.filename)
    if re.match(r'ppt/charts/chart\d+\.xml$', it.filename):
        s = d.decode('utf8')
        if '<c:scatterChart>' in s:
            s2 = re.sub(r'<c:valAx>.*?</c:valAx>', fix_ax, s, flags=re.S); n += s2 != s; s = s2
        d = s.encode('utf8')
    zout.writestr(it, d)
zout.close(); zin.close(); os.replace(tmp, src); print('scatter x axes moved to bottom:', n)
