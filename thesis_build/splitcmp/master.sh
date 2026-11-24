#!/bin/bash
# order of the remaining computing (one job set at a time on the 4 cores):
# 70:30 pipeline (already running) -> 80:20 pipeline -> repeated splits 70:30 -> repeated splits 80:20
T=/home/user/meta/thesis_build
until grep -q "ALLDONE\|FAILED" $T/asd7030/data/run_all.log 2>/dev/null; do sleep 30; done
$T/asd8020/run_all.sh >> $T/asd8020/data/run_all.log 2>&1
for d in asd7030 asd8020; do
  cd $T/$d
  for i in 0 1 2 3; do python3 c1_repeat.py worker $i 4 > data/repeat_worker$i.log 2>&1 & done; wait
  python3 c1_repeat.py merge > data/repeat_merge.log 2>&1; echo REPEATDONE >> data/repeat_merge.log
done
echo MASTERDONE > $T/splitcmp/master.done
