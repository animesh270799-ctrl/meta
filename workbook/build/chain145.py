"""Rebuild updated 145 from updated 142 (deterministic chain). usage: python3 chain145.py SCRATCH_OUT_DIR M142 README_JSON"""
import json, subprocess, sys
out, m142, rj = sys.argv[1:4]
T = sys.path[0]
r143, r144 = [json.loads(l) for l in open(rj)]
def run(*a):
    print('>>', ' '.join(a[:3]))
    p = subprocess.run(['python3'] + list(a), capture_output=True, text=True)
    print(p.stdout[-600:], p.stderr[-2000:])
    if p.returncode: sys.exit(p.returncode)
run(f'{T}/batch.py', m142, f'{out}/c1.xlsx', '2026-10-10', *r143, 's326', 's327', 's328', 's329')
run(f'{T}/build143.py', f'{out}/c1.xlsx', f'{out}/c2.xlsx')
run(f'{T}/mksheets145.py', f'{out}/c2.xlsx', f'{out}/c2b.xlsx')
run(f'{T}/batch.py', f'{out}/c2b.xlsx', f'{out}/c3.xlsx', '2026-10-10', *r144, 's330', 'c290', 'c1')
run(f'{T}/build144.py', f'{out}/c3.xlsx', f'{out}/c4.xlsx')
R145 = ('ext 671-674 + author decisions (updated 145, 2026-10-11)',
        ('NEW serials: 331 Sidhu H.S. et al. 2019 AWM (671; BISA Ladhowal sub-surface drip x CA: row a CT vs CA flood, rows b / c ZT vs CA within drip layouts; yields, irrigation WPi (digitised), PFPN, '
         'cost / gross / net / B:C); 333 Singh A. et al. 2014 STR (673; 3 Haryana farm sites, 15-yr ZT wheat into rice residue = pCA vs CT: SOC, BD, Ks, FC, aeration porosity in eight 5-cm layers '
         '(Figs 1-6 digitised, C-stock check within 1.3 %), C stock 0-40, IR, root density, wheat yield components); 334 Singh G., Jalota & Sidhu 2005 SUM (674; PAU straw incorporated CTR vs '
         'removed / burnt CT rows a / b, after rice (red) and wheat, 3 layers: SOC, MWD, aggregate stability, porosity, BD, pore classes, IR). COMPANION: 266 (companion) Sidhu H.S. et al. 2015 FCR '
         '(672; partial repeat of 266 - Sangrur 2008-09 yield and machine field capacity only). AUTHOR DECISIONS (rule 143): FIRBS / bed planting = MT (330 FIRBS rows a2 / c2 / e, 328 bed planting); '
         '670 within-aggregate C fractions, TOC, enzymes and glomalin entered as bulk-soil estimates; NEW SHEETS ACTIVE C POOL and PASSIVE C POOL (Chan F1 + F2 / F3 + F4) after NLC(Cfrac4).'),
        'Bibliography + 4. Next serial 335.')
run(f'{T}/batch.py', f'{out}/c4.xlsx', f'{out}/c5.xlsx', '2026-10-11', *R145, 's331', 'c266', 's333', 's334')
run(f'{T}/build145.py', f'{out}/c5.xlsx', f'{out}/META_ANALYSIS_MASTER updated 145.xlsx')
