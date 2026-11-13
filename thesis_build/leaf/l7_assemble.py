"""Assemble the leaf-analysis Word document (docx JS) from the thesis helpers, the generated body and the reference pool."""
import re, json, os
B = os.path.dirname(os.path.abspath(__file__)) + '/'; S = B + '../'; D = B + 'data/'
T = open(S + 'thesis/t_docx.js').read()
head = T[:T.index('// ======================= TITLE')]
head = re.sub(r"const B = '.*?';", "const B = '%s';" % B, head)
head = re.sub(r"const OUT = '.*?';", "const OUT = '%s';" % (S + 'outputs/Leaf_ASD_analysis_report.docx'), head)
head = re.sub(r"const FORDER = \[.*?\];", "const FORDER = __FORDER__;", head)
head = re.sub(r"const TORDER = \[.*?\];", "const TORDER = __TORDER__;", head)
body = open(D + 'docx_body.js').read()
assert 'children: [new Paragraph({ children: runs(String(c)' in head
head = head.replace('children: [new Paragraph({ children: runs(String(c)', 'children: [new Paragraph({ keepNext: true, children: runs(String(c)')

i = T.index("K.push(H1('References'))"); pool = [r.replace("\\'", "'") for r in re.findall(r"^  '(.*)',$", T[i:], re.M)]
A = open(S + 'obj1/o1_assemble.py').read(); pool += re.findall(r'^ "(.*)",$', A, re.M)
pool += ["Hueni, A., Bialek, A. (2017). Cause, effect, and correction of field spectroradiometer interchannel radiometric steps. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing 10(4), 1542–1551.",
         "Klecka, W.R. (1980). Discriminant Analysis. Sage University Paper Series on Quantitative Applications in the Social Sciences 07-019. Sage, Beverly Hills.",
         "Wheeler, B.E.J. (1969). An Introduction to Plant Diseases. John Wiley and Sons, London.",
         "Rumpf, T., Mahlein, A.-K., Steiner, U., Oerke, E.-C., Dehne, H.-W., Plümer, L. (2010). Early detection and classification of plant diseases with support vector machines based on hyperspectral reflectance. Computers and Electronics in Agriculture 74(1), 91–99.",
         "Ashourloo, D., Mobasheri, M.R., Huete, A. (2014). Developing two spectral disease indices for detection of wheat leaf rust (Puccinia triticina). Remote Sensing 6(6), 4723–4740.",
         "Mahlein, A.-K., Steiner, U., Hillnhütter, C., Dehne, H.-W., Oerke, E.-C. (2012). Hyperspectral imaging for small-scale analysis of symptoms caused by different sugar beet diseases. Plant Methods 8, 3.",
         "Chang, C.-W., Laird, D.A., Mausbach, M.J., Hurburgh, C.R. (2001). Near-infrared reflectance spectroscopy–principal components regression analyses of soil properties. Soil Science Society of America Journal 65(2), 480–490.",
         "Saharan, G.S., Verma, P.R., Meena, P.D., Kumar, A. (2014). White Rust of Crucifers: Biology, Ecology and Management. Springer India, New Delhi."]
pat = re.compile(r"([A-Z][A-Za-zÀ-ÿŠš\-]+)(?: et al\.| and [A-Z][A-Za-zÀ-ÿ\-]+)?,? \(?(\d{4})[a-z]?")
cites = set((m.group(1), m.group(2)) for m in pat.finditer(body))
def rk(r):
    a = r.split(',')[0].strip(); y = re.search(r'\((\d{4})[a-z]?\)', r); return (a, y.group(1) if y else '')
used, seen = [], set()
for r in sorted(pool, key=lambda r: (r.split('(')[0].lower(), r)):
    key = (r.split('(')[0], rk(r)[1])
    if rk(r) in cites and key not in seen: seen.add(key); used.append(r)
have = set(rk(r) for r in used)
skip = {'ICAR-IARI', 'IARI', 'Table', 'Figure', 'Tier', 'Tiers', 'Section', 'February', 'March', 'Objective', 'R1', 'All', 'PDI', 'ASD', 'WRI'}
fp = {('Šikonja', '2003'), ('Kononenko', '2003'), ('Chattopadhyay', '2013'), ('Rudnicki', '2010'), ('Philpot', '1998'), ('Golay', '1964'), ('Bialek', '2017'), ('Peñuelas', '1994'), ('Rock', '1989'), ('McLachlan', '2002'), ('Simon', '2006'), ('Knapp', '2001'), ('Hart', '1967'), ('Vapnik', '1995'), ('Gomez', '1984'), ('Lapalme', '2009')}
missing = sorted(x for x in cites if x not in have and x[0] not in skip and 1900 < int(x[1]) < 2027 and x not in fp)
print('missing refs:', missing)
q = lambda s: "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"
body += "\nK.push(H1('References'));\nconst refPara = r => new Paragraph({ spacing: { after: 70, line: 255 }, indent: { left: 400, hanging: 400 }, children: [new TextRun({ text: r, font: FONT, size: 18 })] });\n[\n" + '\n'.join('  ' + q(r) + ',' for r in used) + "\n].forEach(r => K.push(refPara(r)));\n"
json.dump(used, open(D + 'refs_used.json', 'w'), indent=0, ensure_ascii=False)
FO = [m.group(2) for m in re.finditer(r"\b(fig2|FIG)\('([A-Za-z0-9]+)'", body)]
TO = [m.group(2) for m in re.finditer(r"\b(tab2|TAB)\('([A-Za-z0-9]+)'", body)]
assert len(FO) == len(set(FO)) and len(TO) == len(set(TO))
mf = set(re.findall(r"\bF\('([A-Za-z0-9]+)'\)", body)) - set(FO); mt = set(re.findall(r"\bT\('([A-Za-z0-9]+)'\)", body)) - set(TO)
assert not mf and not mt, (mf, mt)
head = head.replace('__FORDER__', repr(FO)).replace('__TORDER__', repr(TO))
tail = T[T.index('\nconst numcfg'):]
tail = tail.replace("title: 'AI-based multimodal UAV sensing of white rust in mustard: complete methodology'", "title: 'Leaf-level ASD analysis of white rust in mustard'")
tail = re.sub(r"'eqs', \d+, 'refs', \d+", "'eqs', 0, 'refs', %d" % len(used), tail)
open(B + 'l7_build.js', 'w').write(head + '\n' + body + '\n' + tail)
print('figs', len(FO), 'tabs', len(TO), 'refs', len(used))
