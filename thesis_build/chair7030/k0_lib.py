"""Shared helpers of the 70:30 protocol document."""
from dsl import *


def card(key, step, title, purpose, data, inputs, procedure, settings, output, script, refs, slides, newdata):
    """Step card: one table per protocol step with the same rows, so that every step can be presented and repeated in the same way."""
    rows = [['Item', 'Step %s – %s' % (step, title)],
            ['Purpose', purpose], ['Data used (which leaves)', data], ['Input', inputs], ['Procedure (in this order)', procedure],
            ['Settings', settings], ['Output → next step', output], ['Script / output file', script],
            ['References', refs + ' – what each paper did and how its method is similar to this step: see the next table.'],
            ['Seminar slides', slides], ['On a new data set', newdata]]
    tab(key, rows=rows, caption='Step card – Step %s: %s.' % (step, title), widths=[2050, 7550], size=17, boldfirst=True, nokeep=True)
    from k0b_refs import papers
    papers(step)
    read(how='Read the table row by row: column 2 says what the authors did in their study, column 3 how the same method was used in this step of my analysis, column 4 what I changed and why.',
         say='"For this step I followed %s; the table shows what each paper did and how my step matches it."' % _first_refs(step))


def steps(*items):
    """numbered sub-steps written as '(1) ...\n(2) ...' inside a step card"""
    return '\n'.join('(%d) %s' % (i + 1, t) for i, t in enumerate(items))


def where(slides, files):
    p('**Where to find it.** Seminar slides %s. Excel/script: %s.' % (slides, files))


def _first_refs(step):
    from k0b_refs import P
    return ', '.join(r[0] for r in P[step][:2])
