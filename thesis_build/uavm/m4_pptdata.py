"""Collect the disease-map content for the slides into out/ppt_data.json."""
import json, os
O = os.path.dirname(os.path.abspath(__file__)) + '/out/'
D = dict(tables=json.load(open(O + 'tables.json')), figures=json.load(open(O + 'figures.json')), methods=json.load(open(O + 'methods.json')), interp=json.load(open(O + 'interpretations.json')),
         findings=json.load(open(O + 'findings.json')), refs=json.load(open(O + 'refs_used.json')), summary=json.load(open(O + 'map_summary.json')))
json.dump(D, open(O + 'ppt_data.json', 'w'), indent=1, default=str); print('saved ppt_data.json')
