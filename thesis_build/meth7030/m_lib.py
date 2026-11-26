"""Helpers of the methodology document: one method card per step, with the same rows everywhere."""
from dsl import *
import json, os
CNT = json.load(open(os.path.join(MYFIG, 'counts.json')))

ROWS = [('what', 'What is done'), ('why', 'Why at this position'), ('papers', 'Disease papers: what they did'), ('match', 'How my step follows them'),
        ('mine', 'With my data (exact settings)'), ('out', 'Output → next step'), ('alt', 'Alternatives and notes'), ('q', 'Likely question → answer')]


def card(code, title, **kw):
    rows = [['Step %s' % code, title]] + [[lab, kw[k]] for k, lab in ROWS if kw.get(k)]
    tab('card_' + code.replace('.', '_'), rows=rows, caption='Method card – Step %s: %s.' % (code, title), widths=[2050, 7550], size=17, boldfirst=True, nokeep=True)


def L(*items):
    """bulleted lines inside a table cell"""
    return '\n'.join('• ' + t for t in items)


def steps(*items):
    """numbered sub-steps inside a table cell"""
    return '\n'.join('(%d) %s' % (i + 1, t) for i, t in enumerate(items))
