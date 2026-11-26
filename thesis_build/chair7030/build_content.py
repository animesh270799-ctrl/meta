"""Assemble the 70:30 step-by-step protocol: content parts -> content.json (read by chair_build.js).
  python3 make_figs.py && python3 build_content.py && NODE_PATH=/opt/node22/lib/node_modules node chair_build.js && python3 ../satmet/to_pdf.py <docx> <pdf>"""
import json, os
import dsl, k1_front, k3_data, k4_split, k5_obj1, k6_models, k7_eval, k8_cov_cmp, k9_end
k1_front.add(); k1_front.overview()
for m in (k3_data, k4_split, k5_obj1, k6_models, k7_eval, k8_cov_cmp, k9_end): m.add()
def alltext(x):
    if isinstance(x, str): return x
    if isinstance(x, list): return ' '.join(alltext(y) for y in x)
    if isinstance(x, dict): return ' '.join(alltext(v) for k, v in x.items() if k not in ('t', 'key', 'file'))
    return ''
text = alltext(dsl.B)
nref = k9_end.add_refs(text)
blocks, F, T = dsl.resolve()
OUT = '/home/user/meta/thesis_build/outputs/ASD_2025-26_70-30_leaf_analysis_step_by_step_protocol.docx'
json.dump(dict(blocks=blocks, figdir=dsl.FIGDIR, out=OUT, author='Animesh Panda', doctitle='White rust leaf analysis 2025-26 – grouped 70:30 hold-out, step-by-step protocol',
               header='White rust leaf analysis 2025-26 · grouped 70:30 hold-out · step-by-step protocol'), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content.json'), 'w'), ensure_ascii=False)
words = len(alltext(blocks).split())
print('blocks', len(blocks), 'figures', len(F), 'tables', len(T), 'references', nref, 'words ~', words)
