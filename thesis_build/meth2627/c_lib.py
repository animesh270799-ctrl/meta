"""Helpers: every step = one method card (what, why, how to do it, settings, checks, output, notes, question) + one table of disease papers
(what they did in that step and how my step follows them)."""
from dsl import *

BOX = '☐ '
ROWS = [('what', 'What is done'), ('why', 'Why at this position'), ('data', 'Samples used'), ('papers', 'Disease papers: what they did'), ('match', 'How my step follows them'),
        ('mine', 'With my data (exact settings)'), ('check', 'Check before the next step'), ('out', 'Output → next step'), ('alt', 'Alternatives and notes'), ('q', 'Likely question → answer')]
STEPS = []          # (part, code, title) for the master checklist
PAPERS = []         # (code, title, [references]) for the cross-check table


def num(*items):
    return '\n'.join('(%d) %s' % (i + 1, t) for i, t in enumerate(items))


def ticks(*items):
    return '\n'.join(BOX + t for t in items)


def L(*items):
    return '\n'.join('• ' + t for t in items)


def step(code, title, papers, part='', **kw):
    """papers = list of (reference, what they did, how my step follows it); kw: what, why, do (list), settings, check (list), out, alt, q."""
    STEPS.append((part, code, title)); PAPERS.append((code, title, [r[0] for r in papers]))
    h3('Step %s – %s' % (code, title))
    kw = dict(kw)
    do = kw.pop('do', None); st = kw.pop('settings', None)
    mine = []
    if do: mine.append(num(*do) if isinstance(do, (list, tuple)) else do)
    if st: mine.append('Settings: ' + ('; '.join(st) if isinstance(st, (list, tuple)) else st))
    kw['mine'] = '\n'.join(mine)
    kw['papers'] = '\n'.join('• %s: %s' % (r[0], r[1]) for r in papers)
    kw['match'] = '\n'.join('• %s: %s' % (r[0], r[2]) for r in papers)
    if isinstance(kw.get('check'), (list, tuple)): kw['check'] = ticks(*kw['check'])
    rows = [['Step %s' % code, title]] + [[lab, kw[k]] for k, lab in ROWS if kw.get(k)]
    key = 'card_' + code.replace('.', '_')
    tab(key, rows=rows, caption='Step %s – %s.' % (code, title), widths=[2100, 7500], size=17, boldfirst=True, nokeep=True)


def demo(key, rows, caption, widths=None, size=16):
    tab(key, rows=rows, caption=caption + ' (demo data)', widths=widths, size=size)
