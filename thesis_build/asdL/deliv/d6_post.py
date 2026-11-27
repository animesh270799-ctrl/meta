"""Post-process the native charts of the deck (pptxgenjs cannot style scatter series one by one):
marker-only vs line-only scatter series, blank points removed (gaps), dashed reference lines. Usage: python3 d6_post.py deck.pptx"""
import sys, re, json, zipfile, html, os
HERE = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(os.path.join(HERE, 'pptdata.json')))
BYTITLE = {c['title']: c for c in D['charts'].values()}
src = sys.argv[1]; tmp = src + '.tmp'; zin = zipfile.ZipFile(src); zout = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED); n_fix = 0
for item in zin.infolist():
    if item.filename.endswith('/'): continue
    data = zin.read(item.filename)
    if re.match(r'ppt/charts/chart\d+\.xml$', item.filename):
        s = data.decode('utf8'); s = re.sub(r'<c:pt idx="\d+"><c:v></c:v></c:pt>', '', s); s = s.replace('<c:dispBlanksAs val="span"/>', '<c:dispBlanksAs val="gap"/>')
        tt = ''.join(re.findall(r'<a:t>([^<]*)</a:t>', s.split('</c:title>')[0])) if '<c:title>' in s else ''
        spec = BYTITLE.get(html.unescape(tt))
        if spec and spec['kind'] in ('scatter', 'line'):
            if spec['kind'] == 'line': spec = dict(spec, line_series=[] if spec['markers'] else [x['name'] for x in spec['series']])
            def fix(m):
                ser = m.group(0); name = html.unescape(re.search(r'<c:tx>.*?<c:v>([^<]*)</c:v>', ser, re.S).group(1))
                if spec['kind'] == 'line' and spec['markers']: return ser
                if name in spec['line_series']:
                    ser = re.sub(r'<c:marker>.*?</c:marker>', '<c:marker><c:symbol val="none"/></c:marker>', ser, count=1, flags=re.S)
                    if 'ellipse' in name: ser = ser.replace('<a:ln w="19050"', '<a:ln w="12700"', 1)
                    if name in ('Chance', '1:1 line'): ser = ser.replace('<a:prstDash val="solid"/>', '<a:prstDash val="dash"/>', 1)
                else:
                    ser = re.sub(r'(<c:spPr>.*?)<a:ln w="\d+" cap="flat">.*?</a:ln>', r'\1<a:ln><a:noFill/></a:ln>', ser, count=1, flags=re.S)
                    npts = len(re.findall(r'<c:pt idx', ser.split('<c:yVal>')[1])) if '<c:yVal>' in ser else 0
                    if npts <= 60: ser = ser.replace('<c:size val="4"/>', '<c:size val="7"/>', 1)
                return ser
            s = re.sub(r'<c:ser>.*?</c:ser>', fix, s, flags=re.S); n_fix += 1
        if '<c:scatterChart>' in s:   # x axis (and its labels) at the bottom of the plot, never on the zero line
            s = re.sub(r'<c:valAx>.*?</c:valAx>', lambda m: m.group(0).replace('<c:crosses val="autoZero"/>', '<c:crosses val="min"/>') if '<c:axPos val="b"/>' in m.group(0) else m.group(0), s, flags=re.S)
        data = s.encode('utf8')
    zout.writestr(item, data)
zout.close(); zin.close(); os.replace(tmp, src); print('scatter charts styled:', n_fix)
