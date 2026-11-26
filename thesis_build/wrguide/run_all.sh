#!/bin/bash
# Runs the whole analysis in order (Linux/macOS). Quick test: WR_FAST=1 bash run_all.sh ; full run: bash run_all.sh
set -e; cd "$(dirname "$0")"
for s in s01_load s02_qc s03_split s04_features s05_obj1 s06_select_train s07_ml; do echo "===== $s"; python3 $s.py; done
for st in main config ablation; do echo "===== s08_dl $st"; python3 s08_dl.py $st; done
for s in s09_evaluate s10_interpret s11_covariate s12_design_check s13_deliver; do echo "===== $s"; python3 $s.py; done
echo "ALL STEPS FINISHED"
