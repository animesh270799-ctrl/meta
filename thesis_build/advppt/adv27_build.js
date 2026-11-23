// Builds the 2026-27 advisory-committee deck (generated slides); the user's own slides are inserted afterwards by adv27_merge.py
const { pres, THEME } = require('./adv_lib.js');
require('./adv_s1.js'); const r = require('./adv_s2.js');
const { applyTheme } = require(process.env.SKILL_DIR + '/scripts/apply_theme.js');
const OUT = process.env.OUT || (__dirname + '/../outputs/adv27_generated.pptx');
pres.writeFile({ fileName: OUT }).then(async f => { await applyTheme(OUT, THEME); console.log('saved', f, 'key refs', r.nrefs); });
