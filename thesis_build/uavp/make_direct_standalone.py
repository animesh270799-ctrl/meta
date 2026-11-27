"""Fully self-contained notebooks for the models that use the DIRECT UAV reflectance (B_RF, C_XGBoost): no reference-spectra file needed,
the 48-plot ASD scores and the self-check values are embedded. Built from the per-model notebooks (make_model_notebooks.py).
Output: uavp/kit/per_model/<key>_pixel_map_24Feb2026_STANDALONE.ipynb"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)) + '/'; PM = HERE + 'kit/per_model/'
def src(c): return ''.join(c['source'])
def put(c, t): c['source'] = [l + '\n' for l in t.split('\n')]; c['source'][-1] = c['source'][-1].rstrip('\n')
for key in ('B_RF', 'C_XGBoost'):
    R = json.load(open(HERE + 'kit/models/%s_reference.json' % key)); assert R['MODEL']['variant'] == 'direct'
    nb = json.load(open(PM + key + '_pixel_map_24Feb2026.ipynb'))
    T = R['TRUTH']; ex = R['EXPECTED']
    ref = ("# ASD leaf scores of 24 Feb 2026 for the 48 plots (plot = ROI number)\n"
           "TRUTH = pd.DataFrame({'plot': %s,\n" % T['plot'] +
           "    'block': %s,\n" % json.dumps(T['block']) + "    'status': %s,\n" % json.dumps(T['status']) +
           "    'variety': %s,\n" % json.dumps(T['variety']) + "    'sowing': %s,\n" % json.dumps(T['sowing']) +
           "    'mean_score': %s,\n" % json.dumps(T['mean_score']) + "    'grade': %s,\n" % json.dumps(T['grade']) + "    'PDI': %s})\n" % json.dumps(T['PDI']) +
           "# this model's prediction for the 48 plot-mean spectra (used by the self-check)\n"
           "EXPECTED = %s\n" % json.dumps([round(float(v), 6) for v in ex]) +
           "MODEL = dict(task='%s', model='%s', variant='direct', uav_metric='%s', uav_value=%.4f)\n" % (R['MODEL']['task'], R['MODEL']['model'], R['MODEL']['uav_metric'], R['MODEL']['uav_value']) +
           "GRADES = [0, 1, 3, 5, 7, 9]; KEY, TASK, VARIANT = '%s', MODEL['task'], MODEL['variant']\n" % key +
           "assert len(WL) == %d and abs(WL[0] - %.2f) < 0.5 and abs(WL[-1] - %.2f) < 0.5, 'the image bands differ from the 24 Feb image the model inputs were built for'\n" % (len(R['REF_WL']), R['REF_WL'][0], R['REF_WL'][-1]) +
           "print(f\"{MODEL['model']} – task {TASK}, input '{VARIANT}' (reflectance used as it is), accuracy on the 48 UAV plots: {MODEL['uav_metric']} {MODEL['uav_value']:.3f}\")")
    for c in nb['cells']:
        s = src(c)
        if c['cell_type'] == 'code' and s.startswith('REF_FILE'): put(c, ref)
        elif c['cell_type'] == 'markdown' and s.startswith('## 3 Reference data'):
            put(c, "## 3 Reference data (embedded)\n`TRUTH` = ASD leaf scores of 24 Feb 2026 for the 48 plots; `EXPECTED` = this model's prediction for the 48 plot-mean spectra (self-check). This model uses the UAV reflectance **directly**, so no reference spectra are needed.")
        elif c['cell_type'] == 'code' and s.startswith('FULL = np.arange'):
            s = s.replace("def make_variant(S, v):\n    if v == 'direct': return S\n    C = S * GAIN\n    return C if v == 'corrected' else C * (TARGET_MEAN / C.mean(1, keepdims=True))",
                          "def make_variant(S, v):\n    return S                                   # this model uses the reflectance directly")
            assert 'GAIN' not in s; put(c, s)
    code = ''.join(src(c) for c in nb['cells'] if c['cell_type'] == 'code')
    assert 'REF_FILE' not in code and 'GAIN' not in code and 'torch' not in code
    json.dump(nb, open(PM + key + '_pixel_map_24Feb2026_STANDALONE.ipynb', 'w'), indent=1); print('written', key + '_pixel_map_24Feb2026_STANDALONE.ipynb')
