"""deck_refs.json = references of the methodology (content.json) that are cited in the deck sources, in short form."""
import json, re, os
H = os.path.dirname(os.path.abspath(__file__))
b = json.load(open(os.path.join(H, '../content.json')))['blocks']
i = max(k for k, x in enumerate(b) if x['t'] == 'h1' and x['text'] == 'References'); refs = [x['text'] for x in b[i + 1:]]
js = ''.join(open(os.path.join(H, f)).read() for f in ('deckx.js',))
cites = {(m.group(1), m.group(3)) for m in re.finditer(r"([A-Z][A-Za-zÀ-ž'\-]+)(?: et al\.| and ([A-Z][A-Za-zÀ-ž'\-]+))?,? \(?(\d{4})[a-z]?", js)}
def short(r):
    r = re.sub(r'\s*https?://\S+', '', r).strip(); m = re.match(r'^(.*?)\((\d{4}[a-z]?)\)\.?\s*(.*)$', r)
    if not m: return r
    au, y, rest = m.groups(); a2 = re.findall(r"(?:^|, |& )([A-ZÀ-Ž][A-Za-zÀ-ž'\-]+), [A-Z]", au); first = au.split(',')[0].strip()
    aus = first + ' et al.' if (len(a2) >= 3 or 'et al' in au) else (a2[0] + ' and ' + a2[1] if len(a2) == 2 else first)
    return '%s (%s). %s' % (aus, y, rest.rstrip('.') + '.')
keep = sorted({short(r) for r in refs if (re.split(r'[ ,]', r)[0], (re.search(r'\((\d{4})', r) or [None, ''])[1]) in cites}, key=str.lower)
json.dump(keep, open(os.path.join(H, 'deck_refs.json'), 'w'), ensure_ascii=False, indent=0); print('deck refs', len(keep))
