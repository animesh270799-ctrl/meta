import openpyxl, sys
wb=openpyxl.load_workbook(sys.argv[1],data_only=True,read_only=True)
serials=set(sys.argv[2].split(','))
skip={'Study_Info','Treatment_Mapping','LAT_LONG','PARAMETERS_BY_STUDY','STUDIES_BY_PARAMETER','Bibliography','README','EXCLUDED_rows','RULES','Codes','FORMULAS'}
for ws in wb.worksheets:
    if ws.title in skip: continue
    rows=list(ws.iter_rows(values_only=True))
    if not rows: continue
    h=[str(x).strip() if x else '' for x in rows[0]]
    if 'SERIAL NO' not in h: continue
    bi=h.index('SERIAL NO')
    for i,r in enumerate(rows[1:],2):
        if r[bi] is not None and str(r[bi]) in serials:
            num=[]
            for k,v in zip(h,r):
                if k in('No.','SERIAL NO','Year','latitude','longitude','LATT','CLAY','RAIN FALL','AVG T','MIN TEMP','MAX TEMP','ph (initial)','soc (initial)','Bdi','sand','silt'): continue
                if isinstance(v,(int,float)): num.append(f'{k}={round(v,4)}')
            dep=r[h.index('DEPTH (as reported in paper)')] if 'DEPTH (as reported in paper)' in h else ''
            print(f'{ws.title}!{i} [{r[bi]}] {dep or ""} ', ' '.join(num))
