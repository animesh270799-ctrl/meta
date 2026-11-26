@echo off
REM Runs the whole analysis in order (Windows, Anaconda Prompt, inside the wrguide folder).
REM Quick test first:  set WR_FAST=1   then   run_all.bat   ;  full run:  set WR_FAST=   then   run_all.bat
for %%s in (s01_load s02_qc s03_split s04_features s05_obj1 s06_select_train s07_ml) do (
  echo ===== %%s & python %%s.py || goto :error )
python s08_dl.py main || goto :error
python s08_dl.py config || goto :error
python s08_dl.py ablation || goto :error
for %%s in (s09_evaluate s10_interpret s11_covariate s12_design_check s13_deliver) do (
  echo ===== %%s & python %%s.py || goto :error )
echo ALL STEPS FINISHED & goto :eof
:error
echo STOPPED: the step above failed. Fix it and run that step again before continuing.
