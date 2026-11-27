#!/bin/bash
# Full run of the 2025-26 ASD leaf analysis with ONE grouped hold-out split (settings in split_cfg.py; resumable:
# each finished step leaves data/steps/<name>.done; delete data/steps/ to start again from the raw files).
cd "$(dirname "$(readlink -f "$0")")"
mkdir -p data/steps
step() {   # step <name> <command...>
  local n=$1; shift
  if [ -f data/steps/$n.done ]; then echo "skip $n"; return 0; fi
  local t0=$(date +%s)
  if "$@" > data/steps/$n.log 2>&1; then touch data/steps/$n.done; echo "done $n $(( $(date +%s) - t0 ))s"; else echo "FAILED $n (see data/steps/$n.log)"; exit 1; fi
}
step a0_load python3 a0_load.py
step a1_prep python3 a1_prep.py
step a2_obj1 python3 a2_obj1.py
step a3_select python3 a3_select.py
step a3_ml python3 a3_ml.py
step a4_dl bash run_dl.sh
step a5_extra env SKIP_TRANSFER=1 python3 a5_extra.py
step a6_figs python3 a6_figs.py
step a11_cov python3 a11_covariate.py
step a12_figs python3 a12_figs_cov.py
step a9_ml python3 a9_final.py ml
step a9_dl python3 a9_final.py dl
step a13_cov_models python3 a13_cov_models.py
step a9_readme python3 a9_readme.py
echo ALLDONE
