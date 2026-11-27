const { pres, THEME } = require('./adv_lib.js');
require('./adv_split.js')();
const { applyTheme } = require(process.env.SKILL_DIR + '/scripts/apply_theme.js');
const OUT = __dirname + '/../outputs/Stage1_validation_split_slide.pptx';
pres.writeFile({ fileName: OUT }).then(async f => { await applyTheme(OUT, THEME); console.log('saved', f); });
