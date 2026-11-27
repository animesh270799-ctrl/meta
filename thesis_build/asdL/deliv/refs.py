"""Resolve 'Author et al. (year)' citations to full references from the project's checked reference pools (same pools as the 2026-27 methodology)."""
import json, re, sys
sys.path.insert(0, '/home/user/meta/thesis_build/meth2627')
from extra_refs import EXTRA
POOL = list(EXTRA) + json.load(open('/home/user/meta/thesis_build/method3/mf3_refs_used.json'))
for fn in ('report_refs.txt', 'deck_refs.txt', 'pool_refs.txt'):
    POOL += [l.strip().replace("\\'", "'").replace('--', '–').replace('\\', '') for l in open('/home/user/meta/thesis_build/meth7030/' + fn) if l.strip()]
POOL = [re.sub(r'\s+', ' ', p) for p in POOL if 'Collaborators' not in p]
SKIP = {'Step', 'Table', 'Figure', 'Steps', 'Chapter', 'Part', 'Python', 'R', 'Objective', 'Task', 'Tasks', 'Sheet', 'Slide'}
def resolve(text):
    cites = set()
    for m in re.finditer(r"([A-Z][A-Za-zÀ-ž'\-]+(?: [A-Z][a-zÀ-ž]+)?)(?: et al\.| and ([A-Z][A-Za-zÀ-ž'\-]+))?,? \(?((?:\d{4}[a-z]?, )*)(\d{4}[a-z]?)", text):
        sur, second, yrs = m.group(1), m.group(2), (m.group(3) or '').replace(',', ' ').split() + [m.group(4)]
        for y in yrs: cites.add((sur, second, y))
    chosen, missing = {}, []
    for sur, second, y in sorted(cites, key=lambda c: (c[0], c[2])):
        if sur in SKIP or not (1900 < int(y[:4]) < 2028): continue
        c = [r for r in POOL if r.startswith(sur + ',') and ('(%s)' % y in r or '(%s' % y in r[:200])]
        if second: c = [r for r in c if second in r.split('(')[0]] or c
        ex = [r for r in c if r in EXTRA]
        full = ex or [r for r in c if 'et al.' not in r.split('(')[0] and '...' not in r] or c
        if not full: missing.append('%s %s' % (sur, y)); continue
        chosen[(sur, y, second)] = max(full, key=len) if not ex else ex[0]
    return sorted(set(chosen.values()), key=str.lower), sorted(set(missing))
