#!/bin/bash
cd /home/user/meta/thesis_build/asd26
N=4
for i in $(seq 0 $((N-1))); do TT=1 python3 a4_par.py worker $i $N > data/dl_worker$i.log 2>&1 & done
wait
python3 a4_par.py merge $N > data/dl_merge.log 2>&1
echo DLDONE >> data/dl_merge.log
