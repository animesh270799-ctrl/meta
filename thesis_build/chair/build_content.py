"""Assemble the explanatory document: content parts -> content.json (read by chair_build.js)."""
import json, os
import dsl, c1_front, c2_data, c3_features, c4_models, c5_results1, c6_results2, c7_discussion, c8_extra, c9_example
c1_front.add(); c8_extra.key_ideas(); c8_extra.chart_guide(); c8_extra.storyline(); c1_front.intro()
for m in (c2_data, c3_features, c4_models, c5_results1, c6_results2): m.add()
c9_example.example(); c7_discussion.add(); c9_example.recommendations(); c7_discussion.add_rest()
c8_extra.extra(); c8_extra.index_groups(); c7_discussion.add_refs()
blocks, F, T = dsl.resolve()
OUT = '/home/user/meta/thesis_build/outputs/ASD_2025-26_leaf_analysis_explained_for_chairman.docx'
json.dump(dict(blocks=blocks, figdir=dsl.FIGDIR, out=OUT, author='Animesh Panda', doctitle='White rust leaf hyperspectral analysis 2025-26 – detailed explanation',
               header='White rust leaf hyperspectral analysis 2025-26 · detailed explanation'), open(os.path.join(os.path.dirname(__file__), 'content.json'), 'w'), ensure_ascii=False)
words = sum(len(str(b.get('text', '')).split()) + sum(len(str(x).split()) for x in b.get('items', [])) + sum(len(str(y).split()) for pr in b.get('parts', []) for y in (pr[1] if isinstance(pr[1], list) else [pr[1]])) for b in blocks)
print('blocks', len(blocks), 'figures', len(F), 'tables', len(T), 'words ~', words)
