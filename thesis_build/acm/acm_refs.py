"""Collect the references cited in acm_ppt.js from the reference pool (author, year match)."""
import re, json, os
B = os.path.dirname(os.path.abspath(__file__)) + '/'
src = open(B + 'acm_ppt.js').read(); P = json.load(open(B + 'refpool.json')); pool = P['pool'] + P['orw']
pool += ["Gruninger, J., Ratkowski, A.J., Hoke, M.L. (2004). The sequential maximum angle convex cone (SMACC) endmember model. Proceedings of SPIE 5425, Algorithms and Technologies for Multispectral, Hyperspectral, and Ultraspectral Imagery X, 1–14.", "Terentev, A., Dolzhenko, V., Fedotov, A., Eremenko, D. (2022). Current state of hyperspectral remote sensing for early plant disease detection: a review. Sensors 22(3), 757.", "Elsayed, S., Elhoweity, M., Ibrahim, H.H., Dewir, Y.H., Migdadi, H.M., Schmidhalter, U. (2017). Thermal imaging and passive reflectance sensing to estimate the water status and grain yield of wheat under different irrigation regimes. Agricultural Water Management 189, 98–110."]
pat = re.compile(r"([A-Z][A-Za-zÀ-ÿŠš'\-]+)(?:,? [A-Z][A-Za-zÀ-ÿ\-]+)?(?: et al\.| and [A-Z][A-Za-zÀ-ÿŠš\-]+(?:-[A-Z][a-z]+)?)?,? (\d{4})[a-z]?")
cites = set(m.groups() for m in pat.finditer(src))
def key(r):
    a = re.split(r'[ ,]', r.strip())[0]; y = re.search(r'\((\d{4})[a-z]?\)', r); return (a, y.group(1) if y else '')
used, seen = [], set()
for r in sorted(pool, key=lambda r: (r.lower(), len(r))):
    k = key(r)
    if k in cites and k not in seen: seen.add(k); used.append(re.sub(r',? &? ?Collaborators:[^()]*', ' ', re.sub(r'\s+', ' ', r.replace('\xa0', ' '))).strip())
skip = {'ICAR', 'IARI', 'Division', 'February', 'Admission', 'SDG', 'Pro', 'Nov', 'Feb', 'May', 'Aug', 'Radioactivity'}
fp = {('Šikonja', '2003'), ('Kononenko', '2003'), ('Chattopadhyay', '2013'), ('Rudnicki', '2010'), ('Golay', '1964'), ('Bialek', '2017'), ('Kalha', '2005'), ('Kumar', '2014'), ('Weatherley', '1962'), ('Wellburn', '1983'), ('Lapalme', '2009'), ('Vapnik', '1995'), ('Hart', '1967'), ('Tang', '2024'), ('Milton', '1999'), ('Long', '2016'), ('Awasthi', '2018'), ('Dias', '2005'), ('Bioucas', '2005')}
missing = sorted(c for c in cites if c not in seen and c[0] not in skip and c not in fp and 1900 < int(c[1]) < 2027)
print('refs', len(used), 'missing', missing)
json.dump(sorted(used, key=lambda r: r.lower()), open(B + 'acm_refs.json', 'w'), ensure_ascii=False, indent=0)
