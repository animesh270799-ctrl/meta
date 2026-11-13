import re, json, os
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
FD = S + 'final/'
T = open(S + 'thesis/t_docx.js').read()
U = open(S + 'uav/u10_docx.js').read()
DUM = json.load(open(FD + 'dummy.json'))

head = T[:T.index('// ======================= TITLE')]
head = re.sub(r"const B = '.*?';", "const B = '%s';" % FD, head)
head = re.sub(r"const OUT = '.*?';", "const OUT = '%s';" % (S + 'outputs/White_rust_final_methodology.docx'), head)
head = re.sub(r"const FORDER = \[.*?\];", "const FORDER = __FORDER__;", head)
head = re.sub(r"const TORDER = \[.*?\];", "const TORDER = __TORDER__;", head)
head += r"""
const DUM = require(B + 'dummy.json');
const FIG = (k, file, cap, w) => ({ t: 'f', k, file, cap, w });
const TAB = (k, rows, widths, cap, size) => ({ t: 't', k, rows, widths, cap, size });
function FSTEP(o) {
  const lab = (l, c, t) => new Paragraph({ spacing: { after: 70, line: 285 }, alignment: AlignmentType.JUSTIFIED, children: [new TextRun({ text: l + ' ', bold: true, font: FONT, size: 21, color: c }), ...runs(t, { size: 21 })] });
  K.push(H2(o.title));
  K.push(BOX('Position in the workflow:', o.pos, 'ECEFF1', '455A64'));
  K.push(lab('Concept:', '1565C0', o.concept));
  (o.eqs || []).forEach(e => K.push(e));
  K.push(lab('Why it is needed at this position:', 'AD1457', o.need));
  K.push(lab('Importance and justification:', '6A1B9A', o.just));
  if (o.papers) { K.push(new Paragraph({ spacing: { after: 40 }, keepNext: true, children: [new TextRun({ text: 'What the reference papers used for this problem:', bold: true, font: FONT, size: 21, color: '00838F' })] })); o.papers.forEach(p => K.push(BL(p))); }
  K.push(new Paragraph({ spacing: { after: 40 }, keepNext: true, children: [new TextRun({ text: 'How it is done:', bold: true, font: FONT, size: 21, color: '2E7D32' })] }));
  o.how.forEach(h => K.push(BL(h)));
  K.push(lab('How it is used with my data:', 'C98A00', o.mine));
  (o.vis || []).forEach(v => { if (v.t === 'f') K.push(...fig2(v.k, v.file, v.cap, v.w)); else K.push(...tab2(v.k, v.rows, v.widths, v.cap, v.size)); });
  K.push(...STEPEND(o.out, o.notes));
  K.push(new Paragraph({ spacing: { before: 60, after: 40 }, keepNext: true, children: [new TextRun({ text: 'Interview questions:', bold: true, font: FONT, size: 21, color: '1E3A1F' })] }));
  o.qs.forEach(([q, a]) => { K.push(new Paragraph({ spacing: { after: 20, line: 270 }, indent: { left: 300 }, keepNext: true, children: [new TextRun({ text: 'Q. ' + q, bold: true, font: FONT, size: 20 })] }));
    K.push(new Paragraph({ spacing: { after: 70, line: 270 }, indent: { left: 300 }, children: runs('A. ' + a, { size: 20 }) })); });
  K.push(new Paragraph({ spacing: { before: 40, after: 200 }, children: [new TextRun({ text: 'References for this step: ', bold: true, italics: true, font: FONT, size: 19, color: '555555' }), new TextRun({ text: o.refs, italics: true, font: FONT, size: 19, color: '555555' })] }));
}
"""

def tab_args(key):
    i = U.index("tab2('%s', " % key) + len("tab2('%s', " % key)
    j = U.index("));", U.index("\n], [", i))
    return U[i:j]
hs = tab_args('hsidx')
hs = re.sub(r"'Hyperspectral narrow-band indices \(39 indices;.*?', 15", "'Hyperspectral narrow-band indices (39 indices; R_{λ} = reflectance at λ nm): all indices of the ORW slides, with formulas checked against the original papers, plus disease-related indices from the reference papers (MSR, GI, RR, PSSRb/c, HI, DWSI-1, DWSI-4, ROTI). The WRI is built in Step 1.4.', 15", hs, flags=re.S)
assert 'all indices of the ORW slides' in hs
ms = tab_args('msidx')
ms = '\n'.join(l for l in ms.split('\n') if 'optional' not in l)
ms = ms.replace("8 GLCM measures (' + T('rgbfeat') + ') of each of the 5 bands", "8 GLCM measures (mean, variance, homogeneity, contrast, dissimilarity, entropy, second moment, correlation) of each of the 5 bands")
ms = re.sub(r"'Multispectral features \(12 indices.*?', 16", "'Multispectral features: 5 bands, the 12 indices of the ORW slides (formulas checked against the original papers) and 40 GLCM textures.', 16", ms, flags=re.S)
assert 'T(' not in ms
q = lambda s: "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"
rows = lambda R: '[' + ',\n'.join('[' + ', '.join(q(str(c)) for c in r) + ']' for r in R) + ']'
st = [['Feature', 'Healthy', 'Low', 'Moderate', 'High', 'ANOVA F', 'r with DI']] + DUM['stats_rows']
STATS = rows(st) + ", [1900, 1300, 1300, 1300, 1300, 1000, 1206], 'Dummy univariate results (mean ± SD per class, one-way ANOVA F, Pearson r with DI); all p < 0.001 in this example.', 16"
c = DUM['cda']
cda = [['Quantity', 'Dummy value (HS features PSSRa, REP, WRI, DWSI-1)'],
       ['Canonical correlation of function 1 (0–1)', str(c['can'][0])],
       ["Wilks' lambda (0 = separated, 1 = not separated)", str(c['wilks'])],
       ['Weights of the features on function 1', '; '.join('%s %s' % (r[0].split(' (')[0], r[1]) for r in c['coef'])],
       ['Held-out accuracy of the discriminant functions', str(c['acc'])]]
CDA = rows(cda) + ", [3200, 6106], 'Dummy output of the canonical discriminant analysis (CDA).', 16"
vif = [['Iteration', 'VIF of each feature', 'Action']] + [[str(i + 1), r[0], r[1]] for i, r in enumerate(DUM['vif'])]
VIF = rows(vif) + ", [1100, 6000, 2206], 'Dummy VIF iterations on a hyperspectral DSF pool (computed on simulated data).', 16"
cm = DUM['cm']
cmr = [['Class', 'Precision', 'Recall', 'F1']] + [[n, cm['P'][i], cm['R'][i], cm['F1'][i]] for i, n in enumerate(['Healthy', 'Low', 'Moderate', 'High'])] + [['Overall', 'OA ' + cm['oa'], 'kappa ' + cm['kap'], 'macro-F1 ' + cm['mf1']]]
CM = rows(cmr) + ", [2500, 2300, 2300, 2206], 'Dummy per-class metrics from the confusion matrix of Figure (Step 2.4).', 17"

body = open(FD + 'f_body.js').read()
for k, v in (('__HSIDX__', hs), ('__MSIDX__', ms), ('__STATS__', STATS), ('__CDA__', CDA), ('__VIF__', VIF), ('__CM__', CM)):
    assert k in body, k; body = body.replace(k, v)
body += '\n' + open(FD + 'f_isro.js').read()

# equations
chap = '0'; cnt = {}; lab = {}
for line in body.split('\n'):
    m = re.match(r"K\.push\(H1\('(\d+)\.", line)
    if m: chap = m.group(1)
    for mm in re.finditer(r"EQ\(.*?, '(e:[A-Za-z0-9]+)'\)", line):
        cnt[chap] = cnt.get(chap, 0) + 1; lab[mm.group(1)] = '%s.%d' % (chap, cnt[chap])
for k, v in lab.items(): body = body.replace("'%s')" % k, "'%s')" % v)
body = re.sub(r'\[(e:[A-Za-z0-9]+)\]', lambda m: lab[m.group(1)], body)

# references: pool from thesis + extras, filtered to cited
i = T.index("K.push(H1('References'))"); pool = re.findall(r"^  '(.*)',$", T[i:], re.M)
pool = [r.replace("\\'", "'") for r in pool]
pool += ["Hastie, T., Tibshirani, R., Friedman, J. (2009). The Elements of Statistical Learning: Data Mining, Inference, and Prediction, 2nd edn. Springer, New York.",
         "Kruse, F.A., Lefkoff, A.B., Boardman, J.W., Heidebrecht, K.B., Shapiro, A.T., Barloon, P.J., Goetz, A.F.H. (1993). The spectral image processing system (SIPS) – interactive visualization and analysis of imaging spectrometer data. Remote Sensing of Environment 44(2–3), 145–163.",
         "Winter, M.E. (1999). N-FINDR: an algorithm for fast autonomous spectral end-member determination in hyperspectral data. Proceedings of SPIE 3753, Imaging Spectrometry V, 266–275.",
         "Nascimento, J.M.P., Bioucas-Dias, J.M. (2005). Vertex component analysis: a fast algorithm to unmix hyperspectral data. IEEE Transactions on Geoscience and Remote Sensing 43(4), 898–910.",
         "Sulik, J.J., Long, D.S. (2016). Spectral considerations for modeling yield of canola. Remote Sensing of Environment 184, 161–174.",
         "Fang, S., Tang, W., Peng, Y., Gong, Y., Dai, C., Chai, R., Liu, K. (2016). Remote estimation of vegetation fraction and flower fraction in oilseed rape with unmanned aerial vehicle data. Journal of Applied Remote Sensing 10(2), 026025.",
         "Cliff, N. (1993). Dominance statistics: ordinal analyses to answer ordinal questions. Psychological Bulletin 114(3), 494–509."]
pat = re.compile(r"([A-Z][A-Za-zÀ-ÿŠš\-]+)(?: et al\.| and [A-Z][A-Za-zÀ-ÿ\-]+)?,? \(?(\d{4})[a-z]?")
cites = set((m.group(1), m.group(2)) for m in pat.finditer(body))
cites |= set((m.group(1), m.group(2)) for m in re.finditer(r"([A-Z][A-Za-zÀ-ÿŠš\-]+) (\d{4})\b", body))
def rk(r):
    a = r.split(',')[0].strip(); y = re.search(r'\((\d{4})[a-z]?\)', r); return (a, y.group(1) if y else '')
used = sorted({r for r in pool if rk(r) in cites}, key=lambda r: (r.split('(')[0].lower(), r))
have = set(rk(r) for r in used)
skip = {'ICAR-IARI', 'IARI', 'ORW', 'PM', 'Table', 'Figure', 'Step', 'Steps', 'Nov', 'Dec', 'Jan', 'March', 'January', 'November', 'December', 'Stage', 'Section', 'Chapter', 'Objective', 'LISS', 'HySIS', 'TRISHNA', 'Sentinel', 'Hyperion', 'MODIS', 'Bharatpur'}
fp = {('Šikonja', '2003'), ('Kononenko', '2003'), ('Chattopadhyay', '2013'), ('Rayens', '2003'), ('Milton', '1999'), ('Whitney', '1947'), ('Wallis', '1952'), ('Lapalme', '2009'), ('Hart', '1967'), ('Vapnik', '1995'), ('Rudnicki', '2010'), ('McLachlan', '2002'), ('Simon', '2006'), ('Gomez', '1984'), ('Lee', '2017'), ('Hastie', '2005'), ('Tibshirani', '1997'), ('Guestrin', '2016'), ('Williams', '2006'), ('Jurman', '2020'), ('Webster', '1990'), ('Schmidhuber', '1997'), ('Taylor', '2017'), ('Finney', '1977')}
missing = sorted(x for x in cites if x not in have and x[0] not in skip and 1940 < int(x[1]) < 2027 and x not in fp)
print('missing refs:', missing)
reftxt = "K.push(H1('References'));\nconst refPara = r => new Paragraph({ spacing: { after: 70, line: 255 }, indent: { left: 400, hanging: 400 }, children: [new TextRun({ text: r, font: FONT, size: 18 })] });\n[\n" + '\n'.join('  ' + q(r) + ',' for r in used) + "\n].forEach(r => K.push(refPara(r)));\n"
body += '\n' + reftxt

FO = [m.group(2) for m in re.finditer(r"\b(fig2|FIG)\('([A-Za-z0-9]+)'", body)]
TO = [m.group(2) for m in re.finditer(r"\b(tab2|TAB)\('([A-Za-z0-9]+)'", body)]
assert len(FO) == len(set(FO)) and len(TO) == len(set(TO)), (FO, TO)
mf = set(re.findall(r"\bF\('([A-Za-z0-9]+)'\)", body)) - set(FO); mt = set(re.findall(r"\bT\('([A-Za-z0-9]+)'\)", body)) - set(TO)
assert not mf and not mt, (mf, mt)
head = head.replace('__FORDER__', repr(FO)).replace('__TORDER__', repr(TO))
tail = T[T.index('\nconst numcfg'):]
tail = tail.replace("title: 'AI-based multimodal UAV sensing of white rust in mustard: complete methodology'", "title: 'AI-based multimodal UAV sensing of white rust in mustard: final methodology'")
tail = re.sub(r"'eqs', \d+, 'refs', \d+", "'eqs', %d, 'refs', %d" % (len(lab), len(used)), tail)
open(FD + 'f_docx.js', 'w').write(head + '\n' + body + '\n' + tail)
print('figs', len(FO), 'tabs', len(TO), 'eqs', len(lab), 'refs', len(used))
