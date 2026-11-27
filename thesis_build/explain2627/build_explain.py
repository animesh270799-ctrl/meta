"""Build the step-by-step explanation of the 2026-27 analysis:
python3 e_figs.py && python3 build_explain.py && NODE_PATH=/opt/node22/lib/node_modules node chair_build.js && python3 ../satmet/to_pdf.py <docx> <pdf>"""
import json, os, re, sys
import dsl, x1_intro, x2_prep, x3_obj1, x4_obj2, x5_rest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'meth2627'))
from extra_refs import EXTRA
for m in (x1_intro, x2_prep, x3_obj1, x4_obj2, x5_rest): m.add()


def alltext(x):
    if isinstance(x, str): return x
    if isinstance(x, list): return ' | '.join(alltext(y) for y in x)
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
    for sur, second, y in sorted(cites, key=lambda c: (c[0], c[2])):
        if not (1900 < int(y[:4]) < 2028): continue
        c = [r for r in pool if r.startswith(sur + ',') and ('(%s)' % y in r or '(%s' % y in r[:200])]
        if second: c = [r for r in c if second in r.split('(')[0]] or c
        ex = [r for r in c if r in EXTRA]
        full = ex or [r for r in c if 'et al.' not in r.split('(')[0] and '...' not in r] or c
        if not full: missing.append('%s %s' % (sur, y)); continue
        chosen[(sur, y, second)] = max(full, key=len) if not ex else ex[0]
    return sorted(set(chosen.values()), key=str.lower), sorted(set(missing))


refs, missing = references(alltext(dsl.B))
dsl.h1('References')
for r in refs: dsl.B.append(dict(t='p', text=r))
blocks, F, T = dsl.resolve()
OUT = '/home/user/meta/thesis_build/outputs/White_rust_2026-27_data_analysis_explained_step_by_step.docx'
json.dump(dict(blocks=blocks, figdir=dsl.FIGDIR, out=OUT, author='Animesh Panda', doctitle='White rust 2026-27: the data analysis explained step by step',
               header='White rust of Indian mustard · 2026-27 data analysis explained step by step'), open(os.path.join(HERE, 'content.json'), 'w'), ensure_ascii=False)
print('blocks', len(blocks), 'figures', len(F), 'tables', len(T), 'references', len(refs), 'words ~', len(alltext(blocks).split()))
print('MISSING', missing)
