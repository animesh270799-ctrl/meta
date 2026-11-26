"""Build the step-by-step analysis manual (Word + PDF)."""
import json, os
import dsl, mn_content
mn_content.add()
blocks, F, T = dsl.resolve()
OUT = '/home/user/meta/thesis_build/outputs/ASD_2025-26_white_rust_step_by_step_analysis_manual.docx'
json.dump(dict(blocks=blocks, figdir=dsl.FIGDIR, out=OUT, author='Animesh Panda', doctitle='White rust leaf spectra 2025-26 – step-by-step analysis manual',
               header='White rust leaf spectra 2025-26 · step-by-step analysis manual'), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content.json'), 'w'), ensure_ascii=False)
print('blocks', len(blocks), 'figures', len(F), 'tables', len(T))
