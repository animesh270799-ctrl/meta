"""Assemble the methodology document (no results) -> content.json -> chair_build.js (Word) -> to_pdf.py (PDF).
  python3 m_figs.py && python3 build_content.py && NODE_PATH=/opt/node22/lib/node_modules node chair_build.js && python3 ../satmet/to_pdf.py <docx> <pdf>"""
import json, os
import dsl, m1_front, m2_data, m3_prep, m4_obj1, m5_obj2, m6_eval, m7_end
for m in (m1_front, m2_data, m3_prep, m4_obj1, m5_obj2, m6_eval, m7_end): m.add()
def alltext(x):
    if isinstance(x, str): return x
    if isinstance(x, list): return ' '.join(alltext(y) for y in x)
    if isinstance(x, dict): return ' '.join(alltext(v) for k, v in x.items() if k not in ('t', 'key', 'file'))
    return ''
n, missing = m7_end.add_refs(alltext(dsl.B))
blocks, F, T = dsl.resolve()
OUT = '/home/user/meta/thesis_build/outputs/ASD_2025-26_white_rust_leaf_methodology_70-30_with_references.docx'
json.dump(dict(blocks=blocks, figdir=dsl.FIGDIR, out=OUT, author='Animesh Panda', doctitle='White rust leaf hyperspectral methodology 2025-26 (grouped 70:30) with references',
               header='White rust leaf hyperspectral analysis 2025-26 · detailed methodology with references'), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content.json'), 'w'), ensure_ascii=False)
print('blocks', len(blocks), 'figures', len(F), 'tables', len(T), 'references', n, 'words ~', len(alltext(blocks).split()))
print('MISSING', missing)
