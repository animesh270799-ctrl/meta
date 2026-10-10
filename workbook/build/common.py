"""Shared row-building helpers for the updated-140 batch."""


def base(st, site, extra=None):
    d = {
        'No.': st['no'], 'SERIAL NO': st['serial'], 'Authors': st['authors'], 'Year': st['year'],
        'Journal': st['journal'], 'Country': site['country'], 'Site/Location': site['site'],
        'latitude': site['lat'], 'longitude': site['lon'], 'CLIMATE': site['climate'],
        'year of data collection/experiment': site.get('yeardata'), 'DURATION': site.get('duration'),
        'SOIL': site.get('soil'), 'LATT': site['lat'],
        'Treatment mapping (paper\'s name -> code)': st['tmap'],
        'Fertilizer dose & other management': site.get('fert', st.get('fert')),
        'Treatment details (from paper)': st['details'],
    }
    for k in ('CLAY', 'MIN TEMP', 'MAX TEMP', 'RAIN FALL', 'AVG T', 'April max temp', 'ph (initial)',
              'soc (initial)', 'Bdi', 'sand', 'silt'):
        if site.get(k) is not None:
            d[k] = site[k]
    if extra:
        d.update(extra)
    return d


def obs_text(y=1, t=1, d=1):
    parts = []
    tot = 0
    for lab, v in (('Y', y), ('T', t), ('D', d)):
        if v and v > 1:
            parts.append(f'{lab} {v}')
            tot += v
    tot = max(tot, 1)
    return tot, ('Obs = ' + ' + '.join(parts) + f' = {tot}' if parts else 'Obs = 1 (Y, T, D all 1)')


def notes(st, body, y=1, t=1, d=1):
    tot, txt = obs_text(y, t, d)
    return tot, f"{body} {txt}. || {st['ref']}"
