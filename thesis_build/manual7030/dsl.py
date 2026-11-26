"""Tiny content language for the explanatory document. Blocks are collected in B and written to content.json by build_content.py.
Cross references: {F:key} -> 'Figure n', {T:key} -> 'Table n' (numbered in order of appearance)."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
B = []
TABLES = []
FIGDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fig')


def h1(t, newpage=True): B.append(dict(t='h1', text=t, newpage=newpage))
def h2(t): B.append(dict(t='h2', text=t))
def h3(t): B.append(dict(t='h3', text=t))
def p(*ts):
    for t in ts: B.append(dict(t='p', text=t))
def bl(*items): B.append(dict(t='bl', items=list(items)))
def nl(*items): B.append(dict(t='nl', items=list(items)))
def box(label, text, kind='key'): B.append(dict(t='box', label=label, text=text, kind=kind))
def eq(t): B.append(dict(t='eq', text=t))
def qa(q, a): B.append(dict(t='qa', q=q, a=a))
def pb(): B.append(dict(t='pb'))
def code(*lines): B.append(dict(t='code', lines=list(lines)))
MYFIG = os.path.join(HERE, 'fig')
def myfig(key, file, caption, width=620): fig(key, os.path.join(MYFIG, file), caption, width)


def read(shows=None, how=None, found=None, means=None, say=None, caution=None, why=None, done=None):
    parts = []
    for lab, v in (('Why it was done', why), ('How it was done', done), ('What it shows', shows), ('How to read it', how), ('What we found', found),
                   ('What it means', means), ('Caution', caution), ('Say to the chairman', say)):
        if v: parts.append([lab, v])
    B.append(dict(t='read', parts=parts))


def fig(key, file, caption, width=620, rep=None):
    assert os.path.isfile(file if os.path.isabs(file) else os.path.join(FIGDIR, file)), file
    cap = caption + (f' (report Figure {rep})' if rep else '')
    B.append(dict(t='fig', key=key, file=file, caption=cap, width=width))


SUBS = [(re.compile(r'(?<![A-Za-z])R(\d{3,4})'), r'R_{\1}'), (re.compile(r'10-(\d)'), r'10^{−\1}'), (re.compile(r'nm-1'), 'nm^{−1}')]


def tab(key, n=None, rows=None, caption=None, widths=None, size=18, fix=None, subs=False, boldfirst=False, drop_cols=None, nokeep=False):
    """n = report table number (rows and caption taken from the report); rows/caption override."""
    if n is not None:
        T = TABLES[n - 1]; r = [list(x) for x in T['rows']]
        cap = re.sub(r'^Table \d+\.\s*', '', T['caption'] or '') if caption is None else caption
        cap = cap + f' (report Table {n})'
    else:
        r, cap = rows, caption
    if drop_cols:
        r = [[c for j, c in enumerate(row) if j not in drop_cols] for row in r]
    if fix: r = fix(r)
    if subs:
        r = [[_sub(c) for c in row] for row in r]
    B.append(dict(t='tab', key=key, rows=r, caption=cap, widths=widths, size=size, boldfirst=boldfirst, nokeep=nokeep))


def _sub(c):
    for rx, rep in SUBS: c = rx.sub(rep, c)
    return c


def resolve():
    F, T = {}, {}
    for b in B:
        if b['t'] == 'fig': F[b['key']] = len(F) + 1
        if b['t'] == 'tab': T[b['key']] = len(T) + 1
    def rep(s):
        if not isinstance(s, str): return s
        def f(m):
            kind, key = m.group(1), m.group(2)
            d = F if kind == 'F' else T
            if key not in d: raise KeyError(f'unknown reference {kind}:{key}')
            return ('Figure ' if kind == 'F' else 'Table ') + str(d[key])
        return re.sub(r'\{([FT]):([A-Za-z0-9_]+)\}', f, s)
    def walk(x):
        if isinstance(x, str): return rep(x)
        if isinstance(x, list): return [walk(y) for y in x]
        if isinstance(x, dict): return {k: (walk(v) if k not in ('t', 'key', 'file', 'lines') else v) for k, v in x.items()}
        return x
    out = [walk(b) for b in B]
    return out, F, T
