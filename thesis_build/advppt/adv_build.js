const { pres, THEME } = require('./adv_lib.js');
require('./adv_s1.js'); const r = require('./adv_s2.js');
const { applyTheme } = require(process.env.SKILL_DIR + '/scripts/apply_theme.js');
const OUT = __dirname + '/../outputs/White_rust_advisory_committee_methodology_2026-27.pptx';
pres.writeFile({ fileName: OUT }).then(async f => { await applyTheme(OUT, THEME); console.log('saved', f, 'refs', r.nrefs); });
