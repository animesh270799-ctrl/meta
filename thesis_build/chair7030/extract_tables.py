"""Extract all tables (with captions) of the 70:30 report so the explanation uses exactly the same numbers."""
import docx, json, re
D = docx.Document('/home/user/meta/thesis_build/outputs/ASD_2025-26_70-30_leaf_analysis_white_rust_report.docx')
tabs = []; last = None
for el in D.element.body.iterchildren():
    tag = el.tag.split('}')[1]
    if tag == 'p':
        t = ''.join(x.text or '' for x in el.iter() if x.tag.endswith('}t')).strip()
        if re.match(r'^Table \d+\.', t): last = t
    elif tag == 'tbl':
        tb = docx.table.Table(el, D); tabs.append(dict(caption=last, rows=[[c.text.strip() for c in r.cells] for r in tb.rows])); last = None
for i, t in enumerate(tabs): print(i + 1, (t['caption'] or '')[:80], len(t['rows']), 'x', len(t['rows'][0]))
json.dump(tabs, open('/home/user/meta/thesis_build/chair7030/report_tables.json', 'w'), indent=1, ensure_ascii=False)
