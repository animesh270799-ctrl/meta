"""Extract the 37 tables (with captions) of the ASD 2025-26 report so the explanatory document uses exactly the same numbers."""
import docx, json, re
D = docx.Document('/home/user/meta/thesis_build/outputs/ASD_2025-26_leaf_analysis_white_rust_report.docx')
body = D.element.body; caps = []; tabs = []; last = None
for el in body.iterchildren():
    tag = el.tag.split('}')[1]
    if tag == 'p':
        t = ''.join(x.text or '' for x in el.iter() if x.tag.endswith('}t')).strip()
        if re.match(r'^Table \d+\.', t): last = t
    elif tag == 'tbl':
        tb = docx.table.Table(el, D)
        rows = [[c.text.strip() for c in r.cells] for r in tb.rows]
        tabs.append(dict(caption=last, rows=rows)); last = None
print(len(tabs))
for i, t in enumerate(tabs): print(i + 1, (t['caption'] or '')[:70], len(t['rows']), 'x', len(t['rows'][0]))
json.dump(tabs, open('report_tables.json', 'w'), indent=1, ensure_ascii=False)
