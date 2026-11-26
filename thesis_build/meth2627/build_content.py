"""Build the 2026-27 methodology: python3 g_figs.py && python3 build_content.py && NODE_PATH=/opt/node22/lib/node_modules node chair_build.js && python3 ../satmet/to_pdf.py <docx> <pdf>"""
import json, os, re
import dsl, c_lib, c1_front, c2_field, c3_uav, c4_obj1, c5_obj2, c6_obj3, c7_leaf, c8_end
from extra_refs import EXTRA
HERE = os.path.dirname(os.path.abspath(__file__))
for m in (c1_front, c2_field, c3_uav, c4_obj1, c5_obj2, c6_obj3, c7_leaf, c8_end): m.add()

# master checklist in place of the placeholder
rows = [['Done', 'Step', 'Title', 'Part']] + [[c_lib.BOX, code, title, part] for part, code, title in c_lib.STEPS]
k = next(i for i, b in enumerate(dsl.B) if b['t'] == 'placeholder')
dsl.B[k] = dict(t='tab', key='master', rows=rows, caption='Master checklist of all steps (tick when every check of the step is done).', widths=[700, 900, 5600, 2400], size=15, boldfirst=False, nokeep=True)


def alltext(x):
    if isinstance(x, str): return x
    if isinstance(x, list): return ' '.join(alltext(y) for y in x)
    if isinstance(x, dict): return ' '.join(alltext(v) for k, v in x.items() if k not in ('t', 'key', 'file'))
    return ''


def references(text):
    pool = list(EXTRA) + json.load(open('/home/user/meta/thesis_build/method3/mf3_refs_used.json'))
    for fn in ('report_refs.txt', 'deck_refs.txt', 'pool_refs.txt'):
        pool += [l.strip().replace("\\'", "'").replace('--', '–').replace('\\', '') for l in open('/home/user/meta/thesis_build/meth7030/' + fn) if l.strip()]
    pool = [re.sub(r'\s+', ' ', p) for p in pool if 'Collaborators' not in p]
    cites = set()
    for m in re.finditer(r"([A-Z][A-Za-zÀ-ž'\-]+(?: [A-Z][a-zÀ-ž]+)?)(?: et al\.| and ([A-Z][A-Za-zÀ-ž'\-]+))?,? \(?((?:\d{4}[a-z]?, )*)(\d{4}[a-z]?)", text):
        sur, second, yrs = m.group(1), m.group(2), (m.group(3) or '').replace(',', ' ').split() + [m.group(4)]
        for y in yrs: cites.add((sur, second, y))
    chosen, missing = {}, []
    skip = {'Step', 'Table', 'Figure', 'Steps', 'Chapter', 'Part', 'March', 'February', 'December', 'January', 'November', 'Dec', 'Jan', 'Feb', 'Mar', 'Nov', 'Python', 'R', 'Month', 'Activity', 'Objective', 'Advisory', 'IARI', 'ICAR', 'WGS', 'Plot', 'Date', 'Rank'}
    for sur, second, y in sorted(cites, key=lambda c: (c[0], c[2])):
        if sur in skip or not (1900 < int(y[:4]) < 2028): continue
        c = [r for r in pool if r.startswith(sur + ',') and ('(%s)' % y in r or '(%s' % y in r[:200])]
        if second: c = [r for r in c if second in r.split('(')[0]] or c
        ex = [r for r in c if r in EXTRA]
        full = ex or [r for r in c if 'et al.' not in r.split('(')[0] and '...' not in r] or c
        if not full: missing.append('%s %s' % (sur, y)); continue
        chosen[(sur, y, second)] = max(full, key=len) if not ex else ex[0]
    return sorted(set(chosen.values()), key=str.lower), sorted(set(missing))


FULL = {'Ma et al. (2026)', 'Guo et al. (2021)', 'Yu et al. (2021)', 'Liu et al. (2020)', 'Zheng et al. (2018)', 'Liu et al. (2026)', 'Blasch et al. (2023)', 'Yuan et al. (2025)',
        'Chattopadhyay et al. (2011)', 'Conn et al. (1990)', 'Mishra et al. (2009)', 'Zhang et al. (2014a)', 'Liu et al. (2024)', 'Bijlwan et al. (2025)', 'Feng et al. (2022)',
        'Ruan et al. (2022)', 'Zhu et al. (2017)', 'Zhang et al. (2022)', 'Poblete et al. (2023)', 'Guo et al. (2021); Feng et al. (2022)'}
CONF = set()
def mark(r):
    parts = [x.strip() for x in r.split(';')]
    return '; '.join(('✓ ' if p in FULL else ('! ' if p in CONF else '○ ')) + p for p in parts)
dsl.h1('13. Cross-check of every step against its references')
dsl.p('Every step was checked against the disease papers in its table. ✓ = the paper\'s description was checked in the full text during this revision (including the PDFs supplied for Chattopadhyay et al. (2011), Conn et al. (1990), Mishra et al. (2009), Zhang et al. (2014a), Liu et al. (2024), Bijlwan et al. (2025), Feng et al. (2022), Ruan et al. (2022) and Zhu et al. (2017)); ○ = description taken from the paper as read for the earlier methodology documents (abstract and methods), full text not re-checked in this revision.')
rows = [['Step', 'Title', 'Disease papers and check status']] + [[c, t, '\n'.join(mark(r) for r in refs)] for c, t, refs in c_lib.PAPERS]
dsl.tab('crosscheck', rows=rows, caption='Cross-check of the references of every step.', widths=[900, 3300, 5400], size=15, nokeep=True)
refs, missing = references(alltext(dsl.B))
dsl.h1('References')
for r in refs: dsl.B.append(dict(t='p', text=r))
blocks, F, T = dsl.resolve()
OUT = '/home/user/meta/thesis_build/outputs/White_rust_complete_methodology_2026-27_UAV_and_ASD.docx'
json.dump(dict(blocks=blocks, figdir=dsl.FIGDIR, out=OUT, author='Animesh Panda', doctitle='White rust complete methodology 2026-27 (UAV + ASD)',
               header='White rust of Indian mustard · complete methodology 2026-27 · UAV and ASD'), open(os.path.join(HERE, 'content.json'), 'w'), ensure_ascii=False)
print('steps', len(c_lib.STEPS), 'blocks', len(blocks), 'figures', len(F), 'tables', len(T), 'references', len(refs), 'words ~', len(alltext(blocks).split()))
print('MISSING', missing)
