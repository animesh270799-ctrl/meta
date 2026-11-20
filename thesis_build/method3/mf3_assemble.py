"""Assemble the reconstructed methodology Word document (docx JS) with a cross-checked reference list."""
import re, json, os
B = os.path.dirname(os.path.abspath(__file__)) + '/'; S = B + '../'
OUTF = S + 'outputs/White_rust_field_methodology_revised_DT-EDNet.docx'
T = open(S + 'thesis/t_docx.js').read()
head = T[:T.index('// ======================= TITLE')]
head = re.sub(r"const B = '.*?';", "const B = '%s';" % B, head)
head = re.sub(r"const OUT = '.*?';", "const OUT = '%s';" % OUTF, head)
head = re.sub(r"const FORDER = \[.*?\];", "const FORDER = __FORDER__;", head)
head = re.sub(r"const TORDER = \[.*?\];", "const TORDER = __TORDER__;", head)
head = head.replace('children: [new Paragraph({ children: runs(String(c)', 'children: [new Paragraph({ keepNext: true, children: runs(String(c)')
body = open(B + 'mf3_body.js').read()
# ---------- reference pool ----------
i = T.index("K.push(H1('References'))"); pool = [r.replace("\\'", "'") for r in re.findall(r"^  '(.*)',$", T[i:], re.M)]
for f in [S + 'obj1/o1_assemble.py', S + 'leaf/l7_assemble.py']:
    pool += re.findall(r'^ +"(.*\(\d{4}[a-z]?\)\..*)",?\]?$', open(f).read(), re.M)
rp = json.load(open(S + 'acm/refpool.json')); pool += rp['pool'] + rp['orw']
pool = [re.sub(r'\s+', ' ', p.replace('\xa0', ' ')).strip() for p in pool]
EXTRA = open(B + 'mf3_extra_refs.txt').read().strip().split('\n') + open(S + 'method2/mf_extra_refs.txt').read().strip().split('\n')
pool = EXTRA + pool          # verified entries first, so they win over older variants
pat = re.compile(r"([A-Z][A-Za-zÀ-ÿŠšō'\-]+)(?: et al\.| and [A-Z][A-Za-zÀ-ÿŠš\-]+)?,? \(?(\d{4})[a-z]?")
cites = set(m.groups() for m in pat.finditer(body))
# multi-year citations such as "Gitelson et al. (1996, 2003)" and "Cohen (1960, 1968)"
for m in re.finditer(r"([A-Z][A-Za-zÀ-ÿŠš\-]+)(?: et al\.)? \((\d{4})((?:, \d{4})+)\)", body):
    for y in re.findall(r'\d{4}', m.group(3)): cites.add((m.group(1), y))
def rk(r):
    a = re.split(r'[ ,]', r.strip())[0]; y = re.search(r'\((\d{4})[a-z]?\)', r); return (a, y.group(1) if y else '')
used, seen = [], set()
for r in pool:
    k = rk(r)
    if k in cites and k not in seen: seen.add(k); used.append(r)
used.sort(key=lambda r: r.lower())
skip = {'IARI', 'ICAR', 'Table', 'Figure', 'Chapter', 'Section', 'Step', 'Stage', 'Month', 'Objective', 'Jan', 'January', 'Nov', 'Dec', 'Varuna', 'PM', 'Pusa', 'Headwall', 'MicaSense', 'DJI', 'FLIR', 'Tair', 'rabi', 'Ph'}
fp = {('Šikonja', '2003'), ('Kononenko', '2003'), ('Rudnicki', '2010'), ('Golay', '1964'), ('Philpot', '1998'), ('Milton', '1999'), ('Peñuelas', '1994'), ('Rock', '1989'), ('Kalha', '2005'), ('McLachlan', '2002'), ('Simon', '2006'),
      ('Flusser', '2003'), ('Khorram', '1998'), ('Knapp', '2001'), ('Curran', '2004'), ('Rayens', '2003'), ('Vapnik', '1995'), ('Hart', '1967'), ('Guestrin', '2016'), ('Lapalme', '2009'), ('Lee', '2017'), ('Ba', '2015'), ('Szegedy', '2015'),
      ('Long', '2016'), ('Neto', '2008'), ('Elisseeff', '2003'), ('Bühlmann', '2010'), ('Chattopadhyay', '2013'), ('Hutter', '2019'), ('Hutter', '2017')}
missing = sorted(c for c in cites if c not in seen and c[0] not in skip and c not in fp and 1900 < int(c[1]) < 2028)
print('missing refs:', missing)
q = lambda s: "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"
body += "\nK.push(H1('References'));\nconst refPara = r => new Paragraph({ spacing: { after: 70, line: 255 }, indent: { left: 400, hanging: 400 }, children: [new TextRun({ text: r, font: FONT, size: 19 })] });\n[" + ',\n'.join(q(r) for r in used) + "].forEach(r => K.push(refPara(r)));\n"
json.dump(used, open(B + 'mf3_refs_used.json', 'w'), indent=0, ensure_ascii=False)
FO = [m.group(2) for m in re.finditer(r"\b(fig2|FIG)\('([A-Za-z0-9]+)'", body)]
TO = [m.group(2) for m in re.finditer(r"\b(tab2|TAB)\('([A-Za-z0-9]+)'", body)]
assert len(FO) == len(set(FO)) and len(TO) == len(set(TO)), 'duplicate keys'
mf = set(re.findall(r"\bF\('([A-Za-z0-9]+)'\)", body)) - set(FO); mt = set(re.findall(r"\bT\('([A-Za-z0-9]+)'\)", body)) - set(TO)
assert not mf and not mt, (mf, mt)
head = head.replace('__FORDER__', repr(FO)).replace('__TORDER__', repr(TO))
tail = T[T.index('\nconst numcfg'):]
tail = tail.replace("title: 'AI-based multimodal UAV sensing of white rust in mustard: complete methodology'", "title: 'White rust UAV methodology – revised (Objectives 1–3)'")
tail = re.sub(r"'eqs', \d+, 'refs', \d+", "'eqs', 0, 'refs', %d" % len(used), tail)
open(B + 'mf3_build.js', 'w').write(head + '\n' + body + '\n' + tail)
print('figs', len(FO), 'tabs', len(TO), 'refs', len(used))
