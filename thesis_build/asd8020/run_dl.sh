#!/bin/bash
cd "$(dirname "$(readlink -f "$0")")"
N=4
for i in $(seq 0 $((N-1))); do TT=1 python3 a4_par.py worker $i $N > data/dl_worker$i.log 2>&1 & done
wait
python3 a4_par.py merge $N > data/dl_merge.log 2>&1
grep -q "of 26" data/dl_merge.log && python3 -c "import json;import sys;sys.exit(0 if len(json.load(open('data/dl_main.json')))==15 else 1)"
