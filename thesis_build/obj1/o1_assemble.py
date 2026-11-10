"""Assemble the Objective 1 tier document (o1_docx.js) from o1_body.js, the thesis helpers and the u10 index tables."""
import re, json, os
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
OD = S + 'obj1/'
T = open(S + 'thesis/t_docx.js').read()
U = open(S + 'uav/u10_docx.js').read()
DUM = json.load(open(OD + 'o1_dummy.json'))

head = T[:T.index('// ======================= TITLE')]
head = re.sub(r"const B = '.*?';", "const B = '%s';" % OD, head)
head = re.sub(r"const OUT = '.*?';", "const OUT = '%s';" % (S + 'outputs/Objective1_tier_methodology.docx'), head)
head = re.sub(r"const FORDER = \[.*?\];", "const FORDER = __FORDER__;", head)
head = re.sub(r"const TORDER = \[.*?\];", "const TORDER = __TORDER__;", head)
head += r"""
const DUM = require(B + 'o1_dummy.json');
const FIG = (k, file, cap, w) => ({ t: 'f', k, file, cap, w });
const TAB = (k, rows, widths, cap, size) => ({ t: 't', k, rows, widths, cap, size });
const VIS = v => v.t === 'f' ? fig2(v.k, v.file, v.cap, v.w) : tab2(v.k, v.rows, v.widths, v.cap, v.size);
function TIER(o) {
  const lab = (l, c, t) => new Paragraph({ spacing: { after: 70, line: 285 }, alignment: AlignmentType.JUSTIFIED, children: [new TextRun({ text: l + ' ', bold: true, font: FONT, size: 21, color: c }), ...runs(t, { size: 21 })] });
  const hd = (l, c) => new Paragraph({ spacing: { before: 40, after: 40 }, keepNext: true, children: [new TextRun({ text: l, bold: true, font: FONT, size: 21, color: c })] });
  K.push(H2(o.title));
  K.push(BOX('Position in the workflow:', o.pos, 'ECEFF1', '455A64'));
  K.push(lab('Problem solved by this tier:', 'C62828', o.problem));
  K.push(lab('Concept:', '1565C0', o.concept));
  (o.eqs || []).forEach(e => K.push(e));
  K.push(lab('Why it is needed at this position:', 'AD1457', o.need));
  K.push(lab('Why this method in my case:', '6A1B9A', o.why));
  if (o.papers && o.papers.length) { K.push(hd('What the reference papers used for this problem:', '00838F')); o.papers.forEach(p => K.push(BL(p))); }
  if (o.alts) { if (typeof o.alts === 'string') K.push(lab('Alternatives used by other researchers:', '5D4037', o.alts)); else { K.push(hd('Alternatives used by other researchers and why they are not chosen:', '5D4037')); K.push(...VIS(o.alts)); } }
  K.push(hd('How it is done:', '2E7D32'));
  o.how.forEach(h => K.push(BL(h)));
  K.push(lab('How it is used with my data:', 'C98A00', o.mine));
  (o.vis || []).forEach(v => K.push(...VIS(v)));
  K.push(BOX('Output of this tier:', o.out, 'FFF6E0', 'C98A00'));
  K.push(new Paragraph({ spacing: { before: 60, after: 40 }, keepNext: true, children: [new TextRun({ text: 'Interview questions (interactive section):', bold: true, font: FONT, size: 21, color: '1E3A1F' })] }));
  o.qs.forEach(([q, a]) => { K.push(new Paragraph({ spacing: { after: 20, line: 270 }, indent: { left: 300 }, keepNext: true, children: [new TextRun({ text: 'Q. ' + q, bold: true, font: FONT, size: 20 })] }));
    K.push(new Paragraph({ spacing: { after: 70, line: 270 }, indent: { left: 300 }, children: runs('A. ' + a, { size: 20 }) })); });
  K.push(new Paragraph({ spacing: { before: 40, after: 200 }, children: [new TextRun({ text: 'References for this tier: ', bold: true, italics: true, font: FONT, size: 19, color: '555555' }), new TextRun({ text: o.refs, italics: true, font: FONT, size: 19, color: '555555' })] }));
}
"""

def tab_args(key):
    i = U.index("tab2('%s', " % key) + len("tab2('%s', " % key)
    j = U.index("));", U.index("\n], [", i))
    return U[i:j]

hs = tab_args('hsidx')
hs = hs.replace("(Step 1.3)", "(HS Tier 3)")
hs = re.sub(r"'Hyperspectral narrow-band indices \(39 indices;.*?', 15$", "'Hyperspectral base indices (39 indices; R_{λ} = reflectance at λ nm): all indices of the ORW slides, with formulas checked against the original papers, plus disease-related indices from the reference papers (MSR, GI, RR, PSSRb/c, HI, DWSI-1, DWSI-4, ROTI). R_{1982} lies just outside the removed 1800–1950 nm band, so ROTI is computed only if that band passes the noise check. The WRI is built in HS Tier 3; further SWIR disease indices are in ' + T('hsswir') + '.', 15", hs, flags=re.S)
assert 'HS Tier 3; further SWIR' in hs and 'Section' not in hs

swir = [['Index', 'Formula', 'Original reference', 'Disease study and finding'],
        ['DWSI-2', 'R_{1660}/R_{550}', 'Apan et al. 2004', 'Sugarcane orange rust from Hyperion: the disease–water stress indices gave the highest correlations with rust-affected areas'],
        ['DWSI-3', 'R_{1660}/R_{680}', 'Apan et al. 2004', 'Same study; adding the 1660 nm water band improved separation over VNIR-only indices'],
        ['DWSI-5', '(R_{800} + R_{550})/(R_{1660} + R_{680})', 'Apan et al. 2004 (DSWI in Galvão et al. 2005)', 'Orange rust (Apan et al. 2004); DWSI strongly negatively correlated with potato late blight severity (Kundu et al. 2021)'],
        ['NDWI', '(R_{860} − R_{1240})/(R_{860} + R_{1240})', 'Gao 1996', 'Best index for Septoria tritici blotch in canopies of 335 wheat varieties (Yu et al. 2018)'],
        ['MSI', 'R_{1600}/R_{820}', 'Hunt and Rock 1989', 'Leaf water stress index; read together with DWSI and the thermal–water check to separate drought from infection'],
        ['NDII', '(R_{819} − R_{1649})/(R_{819} + R_{1649})', 'Hardisky et al. 1983', 'Canopy water content; same role as MSI'],
        ['RBI_{M}', 'R_{1148}/R_{1301}', 'Mandal et al. 2023', 'Rice blast severity on the 0–9 scale, R^{2} = 0.85 (ICAR-IARI; field spectroradiometer)'],
        ['NDBI', '(R_{1148} − R_{1301})/(R_{1148} + R_{1301})', 'Mandal et al. 2023', 'Same study, R^{2} = 0.86 with blast severity'],
        ['RBI_{R}', '(R_{1068} − R_{1560})/(R_{1068} + R_{1560})', 'Ramalingam et al. 2026', 'Early detection of rice blast, F1 = 0.95, κ = 0.93; better than NDVI and PRI (ICAR-IARI)']]
q = lambda s: "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"
rows = lambda R: '[' + ',\n'.join('[' + ', '.join(q(str(c)) for c in r) + ']' for r in R) + ']'
SWIR = rows(swir) + ", [1150, 2900, 1900, 3356], 'Additional SWIR indices used in disease studies (9 indices, added to the 39 of ' + T('hsidx') + '). All bands lie outside the removed water regions (1350–1450 and 1800–1950 nm). Band order of RBI_{M} and NDBI follows Mandal et al. (2023) and should be checked against the paper before final computation; Ramalingam et al. (2026) was in early access when cited.', 15"

ms = tab_args('msidx')
ms = '\n'.join(l for l in ms.split('\n') if 'optional' not in l)
ms = ms.replace("8 GLCM measures (' + T('rgbfeat') + ') of each of the 5 bands", "8 GLCM measures (mean, variance, homogeneity, contrast, dissimilarity, entropy, second moment, correlation) of each of the 5 bands")
ms = re.sub(r"'Multispectral features \(12 indices.*?', 16$", "'Multispectral features: 5 bands, the 12 indices of the ORW slides (formulas checked against the original papers) and 40 GLCM textures (57 features).', 16", ms, flags=re.S)
assert 'T(' not in ms
rgb = tab_args('rgbfeat')
rgb = re.sub(r"'RGB features\. GLCM.*?', 16$", "'RGB features (29): 8 GLCM measures for each of R, G and B (24; Haralick et al., 1973; Feng et al., 2022; Liu et al., 2024), 3 colour features, VF and CH. Flower fraction is kept separately as a covariate.', 16", rgb, flags=re.S)
assert 'Flower fraction is kept' in rgb
tir = tab_args('tirfeat')
assert 'T(' not in rgb + tir

sens = DUM['sensors']
def anova(k):
    R = [['Feature', 'ANOVA F (6 grades)', 'p', 'r with PDI']] + sens[k]['anova']
    return rows(R) + ", [3000, 2100, 1900, 2306], 'Dummy univariate results for %s features (one-way ANOVA across grades 0, 1, 3, 5, 7, 9; Pearson r with PDI). Computed on simulated data.', 16" % k
def cda(k):
    c = sens[k]['cda']
    R = [['Quantity', 'Dummy value (%s)' % ', '.join(r[0] for r in c['coef'])],
         ['Canonical correlation of functions 1, 2, 3', ', '.join(str(x) for x in c['can'])],
         ['Share of discriminating variance on function 1', '%s%%' % c['ev1']],
         ["Wilks' lambda (0 = separated, 1 = not separated)", str(c['wilks'])],
         ['Standardised weights on function 1', '; '.join('%s %s' % (r[0], r[1]) for r in c['coef'])],
         ['Held-out accuracy (6 grades; chance ≈ 0.17–0.30)', str(c['acc'])]]
    return rows(R) + ", [3600, 5706], 'Dummy stepwise CDA output for the %s sensor (after VIF < 10).', 16" % k
def bor(k):
    b = sens[k]['boruta']; g = lambda s_: ', '.join(f for f, st in b if st == s_) or '—'
    R = [['Boruta decision', 'Features (dummy, six-grade classification)'], ['Confirmed (DSF pool)', g('Confirmed')], ['Tentative (reported)', g('Tentative')], ['Rejected', g('Rejected')]]
    return rows(R) + ", [2600, 6706], 'Dummy Boruta result for the %s sensor; the regression run (PDI) gives the second pool.', 16" % k
nfeat = {'HS': '1494 (bands, red-edge, 48 indices)', 'MS': '57', 'RGB': '29', 'TIR': '13'}
cmp_ = [['Sensor', 'Features (Tier 1)', 'Canonical r_{1}', 'CDA accuracy', 'Confirmed DSFs (dummy)']]
for k in ('HS', 'MS', 'RGB', 'TIR'):
    cmp_.append([k, nfeat[k], str(sens[k]['cda']['can'][0]), str(sens[k]['cda']['acc']), str(sum(1 for _, st in sens[k]['boruta'] if st == 'Confirmed'))])
cmp_.append(['Combined (optional CDA)', 'CDA-selected features of all sensors', str(DUM['combined']['can1']), str(DUM['combined']['acc']), '—'])
SENSORCMP = rows(cmp_) + ", [2000, 2600, 1500, 1500, 1706], 'Dummy comparison of the four sensors in Objective 1.', 16"

body = open(OD + 'o1_body.js').read()
fills = {'__HSIDX__': hs, '__HSSWIR__': SWIR, '__MSIDX__': ms, '__RGBFEAT__': rgb, '__TIRFEAT__': tir, '__SENSORCMP__': SENSORCMP}
for k in ('HS', 'MS', 'RGB', 'TIR'):
    fills['__ANOVA_%s__' % k] = anova(k); fills['__CDA_%s__' % k] = cda(k); fills['__BOR_%s__' % k] = bor(k)
for k, v in fills.items():
    assert body.count(k) == 1, k; body = body.replace(k, v)
assert not re.search(r'__[A-Z_]+__', body)

# equations numbered by chapter
chap = '0'; cnt = {}; lab = {}
for line in body.split('\n'):
    m = re.match(r"K\.push\(H1\('(\d+)\.", line)
    if m: chap = m.group(1)
    for mm in re.finditer(r"EQ\(.*?, '(e:[A-Za-z0-9]+)'\)", line):
        cnt[chap] = cnt.get(chap, 0) + 1; lab[mm.group(1)] = '%s.%d' % (chap, cnt[chap])
for k, v in lab.items(): body = body.replace("'%s')" % k, "'%s')" % v)
body = re.sub(r'\[(e:[A-Za-z0-9]+)\]', lambda m: lab[m.group(1)], body)

# references: thesis pool + extras, filtered to those cited
i = T.index("K.push(H1('References'))"); pool = re.findall(r"^  '(.*)',$", T[i:], re.M)
pool = [r.replace("\\'", "'") for r in pool]
pool += [
 "Conn, K.L., Tewari, J.P., Awasthi, R.P. (1990). A disease assessment key for Alternaria blackspot in rapeseed and mustard. Canadian Plant Disease Survey 70(1), 19–22.",
 "Whittingham, M.J., Stephens, P.A., Bradbury, R.B., Freckleton, R.P. (2006). Why do we still use stepwise modelling in ecology and behaviour? Journal of Animal Ecology 75(5), 1182–1189.",
 "Kruse, F.A., Lefkoff, A.B., Boardman, J.W., Heidebrecht, K.B., Shapiro, A.T., Barloon, P.J., Goetz, A.F.H. (1993). The spectral image processing system (SIPS) – interactive visualization and analysis of imaging spectrometer data. Remote Sensing of Environment 44(2–3), 145–163.",
 "Winter, M.E. (1999). N-FINDR: an algorithm for fast autonomous spectral end-member determination in hyperspectral data. Proceedings of SPIE 3753, Imaging Spectrometry V, 266–275.",
 "Nascimento, J.M.P., Bioucas-Dias, J.M. (2005). Vertex component analysis: a fast algorithm to unmix hyperspectral data. IEEE Transactions on Geoscience and Remote Sensing 43(4), 898–910.",
 "Sulik, J.J., Long, D.S. (2016). Spectral considerations for modeling yield of canola. Remote Sensing of Environment 184, 161–174.",
 "Fang, S., Tang, W., Peng, Y., Gong, Y., Dai, C., Chai, R., Liu, K. (2016). Remote estimation of vegetation fraction and flower fraction in oilseed rape with unmanned aerial vehicle data. Journal of Applied Remote Sensing 10(2), 026025.",
 "Apan, A., Held, A., Phinn, S., Markley, J. (2004). Detecting sugarcane 'orange rust' disease using EO-1 Hyperion hyperspectral imagery. International Journal of Remote Sensing 25(2), 489–498.",
 "Galvão, L.S., Formaggio, A.R., Tisot, D.A. (2005). Discrimination of sugarcane varieties in Southeastern Brazil with EO-1 Hyperion data. Remote Sensing of Environment 94(4), 523–534.",
 "Gao, B.-C. (1996). NDWI – a normalized difference water index for remote sensing of vegetation liquid water from space. Remote Sensing of Environment 58(3), 257–266.",
 "Hunt, E.R., Rock, B.N. (1989). Detection of changes in leaf water content using near- and middle-infrared reflectances. Remote Sensing of Environment 30(1), 43–54.",
 "Hardisky, M.A., Klemas, V., Smart, R.M. (1983). The influence of soil salinity, growth form, and leaf moisture on the spectral radiance of Spartina alterniflora canopies. Photogrammetric Engineering and Remote Sensing 49(1), 77–83.",
 "Yu, K., Anderegg, J., Mikaberidze, A., Karisto, P., Mascher, F., McDonald, B.A., Walter, A., Hund, A. (2018). Hyperspectral canopy sensing of wheat Septoria tritici blotch disease. Frontiers in Plant Science 9, 1195.",
 "Kundu, R., Dutta, D., Nanda, M.K., Chakrabarty, A. (2021). Near real time monitoring of potato late blight disease severity using field based hyperspectral observation. Smart Agricultural Technology 1, 100019.",
 "Serrano, L., Peñuelas, J., Ustin, S.L. (2002). Remote sensing of nitrogen and lignin in Mediterranean vegetation from AVIRIS data: decomposing biochemical from structural signals. Remote Sensing of Environment 81(2–3), 355–364.",
 "Nagler, P.L., Daughtry, C.S.T., Goward, S.N. (2000). Plant litter and soil reflectance. Remote Sensing of Environment 71(2), 207–215.",
 "Hotelling, H. (1936). Relations between two sets of variates. Biometrika 28(3–4), 321–377.",
]
pat = re.compile(r"([A-Z][A-Za-zÀ-ÿŠš\-]+)(?: et al\.| and [A-Z][A-Za-zÀ-ÿ\-]+)?,? \(?(\d{4})[a-z]?")
cites = set((m.group(1), m.group(2)) for m in pat.finditer(body))
cites |= set((m.group(1), m.group(2)) for m in re.finditer(r"([A-Z][A-Za-zÀ-ÿŠš\-]+) (\d{4})\b", body))
def rk(r):
    a = r.split(',')[0].strip(); y = re.search(r'\((\d{4})[a-z]?\)', r); return (a, y.group(1) if y else '')
seen = set(); used = []
for r in sorted(pool, key=lambda r: (r.split('(')[0].lower(), r)):
    if rk(r) in cites and r not in seen and (r.split('(')[0], rk(r)[1]) not in {(u.split('(')[0], rk(u)[1]) for u in used}: seen.add(r); used.append(r)
have = set(rk(r) for r in used)
skip = {'ICAR-IARI', 'IARI', 'ORW', 'Table', 'Figure', 'Tier', 'Tiers', 'Method', 'Step', 'Steps', 'Stage', 'Section', 'Chapter', 'Objective', 'Objectives', 'Hyperion', 'Grade', 'January', 'November', 'December', 'Nov', 'Dec', 'Jan', 'March'}
fp = {('Šikonja', '2003'), ('Kononenko', '2003'), ('Chattopadhyay', '2013'), ('Rudnicki', '2010'), ('Wallis', '1952'), ('Simon', '2006'), ('McLachlan', '2002'), ('Mustard', '2002'), ('Philpot', '1998'), ('Rock', '1989'), ('Dias', '2005'), ('Long', '2016'), ('Clark', '1999')}
missing = sorted(x for x in cites if x not in have and x[0] not in skip and 1900 < int(x[1]) < 2027 and x not in fp)
print('missing refs:', missing)
reftxt = "K.push(H1('References'));\nconst refPara = r => new Paragraph({ spacing: { after: 70, line: 255 }, indent: { left: 400, hanging: 400 }, children: [new TextRun({ text: r, font: FONT, size: 18 })] });\n[\n" + '\n'.join('  ' + q(r) + ',' for r in used) + "\n].forEach(r => K.push(refPara(r)));\n"
body += '\n' + reftxt

FO = [m.group(2) for m in re.finditer(r"\b(fig2|FIG)\('([A-Za-z0-9]+)'", body)]
TO = [m.group(2) for m in re.finditer(r"\b(tab2|TAB)\('([A-Za-z0-9]+)'", body)]
assert len(FO) == len(set(FO)) and len(TO) == len(set(TO)), (FO, TO)
mf = set(re.findall(r"\bF\('([A-Za-z0-9]+)'\)", body)) - set(FO); mt = set(re.findall(r"\bT\('([A-Za-z0-9]+)'\)", body)) - set(TO)
assert not mf and not mt, (mf, mt)
for fname in re.findall(r"\b(?:fig2|FIG)\('[A-Za-z0-9]+', '([^']+)'", body):
    assert os.path.exists(OD + 'fig/' + fname), fname
head = head.replace('__FORDER__', repr(FO)).replace('__TORDER__', repr(TO))
tail = T[T.index('\nconst numcfg'):]
tail = tail.replace("title: 'AI-based multimodal UAV sensing of white rust in mustard: complete methodology'", "title: 'Objective 1: tier-wise methodology for white rust characterisation'")
tail = re.sub(r"'eqs', \d+, 'refs', \d+", "'eqs', %d, 'refs', %d" % (len(lab), len(used)), tail)
open(OD + 'o1_docx.js', 'w').write(head + '\n' + body + '\n' + tail)
print('figs', len(FO), 'tabs', len(TO), 'eqs', len(lab), 'refs', len(used))
