"""Machine-learning interview guide (question-answer, no thesis results)."""
import re, json, os
B = os.path.dirname(os.path.abspath(__file__)) + '/'; S = B + '../'
K = []; QN = [0]
def esc(t):
    t = t.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    return re.sub(r'\[\[(T|F):(\w+)\]\]', lambda m: '${%s(\'%s\')}' % (m.group(1), m.group(2)), t)
js = lambda s: '`' + esc(s) + '`'
def H1(t): K.append("K.push(H1(%s));" % js(t))
def P(t): K.append("K.push(P(%s));" % js(t))
def BL(items): K.extend("K.push(BL(%s));" % js(i) for i in items)
def NOTE(t): K.append("K.push(NOTE(%s));" % js(t))
def EQ(t): K.append("K.push(EQ(%s));" % js(t))
def FIG(k, f, cap, w=520): K.append("K.push(...fig2('%s', '%s', %s, %d));" % (k, f, js(cap), w))
def Q(q, short, detail=None, eq=None, fig=None, mine=None):
    QN[0] += 1
    K.append("K.push(H2(%s));" % js('Q%d. %s' % (QN[0], q)))
    K.append("K.push(BOX('Short answer:', %s, 'E8F5E9', '2E7D32'));" % js(short))
    if eq: EQ(eq)
    if detail:
        if len(detail) == 1: P(detail[0])
        else: BL(detail)
    if fig: FIG(*fig)
    if mine: K.append("K.push(BOX('In my study:', %s, 'FFF6E0', 'C98A00'));" % js(mine))
def Qd(q, a):
    QN[0] += 1
    K.append("K.push(H2(%s));" % js('Q%d. %s' % (QN[0], q))); P(a)

K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 800, after: 160 }, children: [new TextRun({ text: 'Machine learning for the NRSC / SAC (ISRO) interview', font: FONT, size: 42, bold: true, color: '1E3A1F' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: 'Concepts, questions and detailed answers related to AI-based multimodal UAV sensing of white rust in mustard', font: FONT, size: 26, color: '2C5F2D' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 }, children: [new TextRun({ text: 'Ph.D. (Agricultural Physics), ICAR-IARI', font: FONT, size: 20, italics: true, color: '555555' })] }));")
NOTE('**How to use this guide.** Each question has a **short answer** to say first, a detailed explanation for follow-up questions and, where relevant, an **In my study** box linking the concept to the thesis. All figures use simulated data or schematics; no thesis results are quoted. Every method is followed by its reference.')
K.append("K.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-2' }));")
K.append("K.push(new Paragraph({ children: [new PageBreak()] }));")
exec(open(B + 'm_content.py').read())

T_ = open(S + 'thesis/t_docx.js').read()
head = T_[:T_.index('// ======================= TITLE')]
head = re.sub(r"const B = '.*?';", "const B = '%s';" % B, head)
head = re.sub(r"const OUT = '.*?';", "const OUT = '%s';" % (S + 'outputs/ML_interview_guide_QA.docx'), head)
head = re.sub(r"const FORDER = \[.*?\];", "const FORDER = __FORDER__;", head)
head = re.sub(r"const TORDER = \[.*?\];", "const TORDER = __TORDER__;", head)
head = head.replace('children: [new Paragraph({ children: runs(String(c)', 'children: [new Paragraph({ keepNext: true, children: runs(String(c)')
body = '\n'.join(K)
i = T_.index("K.push(H1('References'))"); pool = [r.replace("\\'", "'") for r in re.findall(r"^  '(.*)',$", T_[i:], re.M)]
refpat = re.compile(r'"([A-ZÀ-Ž][^"]{10,400}?\(\d{4}[a-z]?\)\.[^"]{10,500})"')
for f in ('obj1/o1_assemble.py', 'leaf/l7_assemble.py', 'interview/i_build.py', 'interview/i2_build.py', 'dipml/d_build.py'): pool += refpat.findall(open(S + f).read())
pool += ["Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., Liu, T.-Y. (2017). LightGBM: a highly efficient gradient boosting decision tree. Advances in Neural Information Processing Systems 30, 3146–3154.",
 "Geurts, P., Ernst, D., Wehenkel, L. (2006). Extremely randomized trees. Machine Learning 63(1), 3–42.",
 "Ester, M., Kriegel, H.-P., Sander, J., Xu, X. (1996). A density-based algorithm for discovering clusters in large spatial databases with noise. Proceedings of the 2nd International Conference on Knowledge Discovery and Data Mining, 226–231.",
 "Dosovitskiy, A., Beyer, L., Kolesnikov, A., Weissenborn, D., Zhai, X., Unterthiner, T., Dehghani, M., Minderer, M., Heigold, G., Gelly, S., Uszkoreit, J., Houlsby, N. (2021). An image is worth 16x16 words: transformers for image recognition at scale. International Conference on Learning Representations.",
 "Hinton, G.E., Salakhutdinov, R.R. (2006). Reducing the dimensionality of data with neural networks. Science 313(5786), 504–507.",
 "Niculescu-Mizil, A., Caruana, R. (2005). Predicting good probabilities with supervised learning. Proceedings of the 22nd International Conference on Machine Learning, 625–632.",
 "Paoletti, M.E., Haut, J.M., Plaza, J., Plaza, A. (2019). Deep learning classifiers for hyperspectral imaging: a review. ISPRS Journal of Photogrammetry and Remote Sensing 158, 279–317.",
 "Saito, T., Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. PLoS ONE 10(3), e0118432.",
 "Gal, Y., Ghahramani, Z. (2016). Dropout as a Bayesian approximation: representing model uncertainty in deep learning. Proceedings of the 33rd International Conference on Machine Learning, 1050–1059.",
 "Cohen, J. (1968). Weighted kappa: nominal scale agreement with provision for scaled disagreement or partial credit. Psychological Bulletin 70(4), 213–220.",
 "Settles, B. (2009). Active learning literature survey. Computer Sciences Technical Report 1648, University of Wisconsin–Madison."]
pat = re.compile(r"([A-ZÀ-Ž][A-Za-zÀ-ÿŠšĂ-ž\-]+)(?: et al\.| and [A-ZÀ-Ž][A-Za-zÀ-ÿŠšĂ-ž\-]+)?,? \(?(\d{4})[a-z]?")
cites = set((m.group(1), m.group(2)) for m in pat.finditer(body))
def rk(r):
    a = r.split(',')[0].strip(); y = re.search(r'\((\d{4})[a-z]?\)', r); return (a, y.group(1) if y else '')
used, seen = [], set()
for r in sorted(set(pool), key=lambda r: (r.split('(')[0].lower(), r)):
    key = (r.split(',')[0], rk(r)[1])
    if rk(r) in cites and key not in seen: seen.add(key); used.append(r)
have = set(rk(r) for r in used)
missing = sorted(x for x in cites if x not in have and 1900 < int(x[1]) < 2027)
print('unmatched citations (second authors expected):', missing)
q = lambda s: "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"
body += "\nK.push(H1('References'));\nconst refPara = r => new Paragraph({ spacing: { after: 70, line: 255 }, indent: { left: 400, hanging: 400 }, children: [new TextRun({ text: r, font: FONT, size: 18 })] });\n[\n" + '\n'.join('  ' + q(r) + ',' for r in used) + "\n].forEach(r => K.push(refPara(r)));\n"
FO = [m.group(2) for m in re.finditer(r"\b(fig2|FIG)\('([A-Za-z0-9]+)'", body)]
TO = [m.group(2) for m in re.finditer(r"\b(tab2|TAB)\('([A-Za-z0-9]+)'", body)]
assert len(FO) == len(set(FO)), FO
head = head.replace('__FORDER__', repr(FO)).replace('__TORDER__', repr(TO))
tail = T_[T_.index('\nconst numcfg'):]
tail = tail.replace("title: 'AI-based multimodal UAV sensing of white rust in mustard: complete methodology'", "title: 'Machine learning interview guide (questions and answers)'")
tail = re.sub(r"'eqs', \d+, 'refs', \d+", "'eqs', 0, 'refs', %d" % len(used), tail)
open(B + 'm_build.js', 'w').write(head + '\n' + body + '\n' + tail)
print('questions', QN[0], 'figs', len(FO), 'refs', len(used))
