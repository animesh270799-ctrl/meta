"""Reference pool shared with the methodology document (verified entries first) and citation matching."""
import re, json, os
S = os.path.dirname(os.path.abspath(__file__)) + '/../'
def pool():
    T = open(S + 'thesis/t_docx.js').read(); i = T.index("K.push(H1('References'))")
    P = [r.replace("\\'", "'") for r in re.findall(r"^  '(.*)',$", T[i:], re.M)]
    for f in [S + 'obj1/o1_assemble.py', S + 'leaf/l7_assemble.py']: P += re.findall(r'^ +"(.*\(\d{4}[a-z]?\)\..*)",?\]?$', open(f).read(), re.M)
    rp = json.load(open(S + 'acm/refpool.json')); P += rp['pool'] + rp['orw']
    EX = []
    for f in [S + 'asd26/a_extra_refs.txt', S + 'method3/mf3_extra_refs.txt', S + 'method2/mf_extra_refs.txt']:
        if os.path.exists(f): EX += [l for l in open(f).read().strip().split('\n') if l.strip()]
    return [re.sub(r'\s+', ' ', p.replace('\xa0', ' ')).strip() for p in EX + P]
PAT = re.compile(r"([A-Z][A-Za-zÀ-ÿŠšō'\-]+)(?: et al\.| and [A-Z][A-Za-zÀ-ÿŠš\-]+)?,? \(?(\d{4})[a-z]?")
def cites(text):
    c = set(m.groups() for m in PAT.finditer(text))
    for m in re.finditer(r"([A-Z][A-Za-zÀ-ÿŠš\-]+)(?: et al\.)? \((\d{4})((?:, \d{4})+)\)", text):
        for y in re.findall(r'\d{4}', m.group(3)): c.add((m.group(1), y))
    return c
def rk(r):
    t = re.split(r'[ ,]', r.strip()); a = t[1] if t[0] in ('De', 'de', 'Van', 'van', 'Le', 'La') and len(t) > 1 else t[0]
    y = re.search(r'\((\d{4})[a-z]?\)', r); return (a, y.group(1) if y else '')
SKIP = {'November', 'December', 'Dec', 'The', 'Feb', 'Mar', 'March', 'February', 'January', 'Jan', 'IARI', 'ICAR', 'Table', 'Figure', 'Step', 'Stage', 'Objective', 'PM', 'Pusa', 'ASD', 'Sheet', 'Excel', 'Python', 'Task', 'Grade', 'Fold', 'Date', 'Activity', 'Section', 'Slide', 'Sowing', 'V1', 'Inoculation', 'Season'}
def select(text, fp=()):
    c = cites(text); used, seen = [], set()
    for r in pool():
        k = rk(r)
        if k in c and k not in seen: seen.add(k); used.append(r)
    used.sort(key=lambda r: r.lower())
    missing = sorted(x for x in c if x not in seen and x[0] not in SKIP and x not in set(fp) and 1900 < int(x[1]) < 2028)
    return used, missing
