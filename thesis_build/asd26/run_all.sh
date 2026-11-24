#!/bin/bash
# Full rerun of the 2025-26 ASD leaf analysis (resumable: each finished step leaves data/steps/<name>.done).
# Delete data/steps/ to start again from the raw files.
cd /home/user/meta/thesis_build/asd26
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
step a5_extra python3 a5_extra.py
step a6_figs python3 a6_figs.py
step a11_cov python3 a11_covariate.py
step a12_figs python3 a12_figs_cov.py
step a9_ml python3 a9_final.py ml
final_dl() { i=0; for net in "DNN-F1" "DT-EDNet" "EfficientNet-B0" "ResNet18" "ConvNeXt V2-Atto"; do TT=1 python3 a9_final.py dl "$net" "n$i" > data/final_dl_$i.log 2>&1 & i=$((i+1)); done; wait; grep -L "saved" data/final_dl_*.log | grep -q . && return 1 || return 0; }
step a9_dl final_dl
step a13_cov_models python3 a13_cov_models.py
step a9_readme python3 a9_readme.py
echo ALLDONE
