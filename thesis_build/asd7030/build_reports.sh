#!/bin/bash
# Word (+PDF), Excel and PowerPoint of this split pipeline (run after run_all.sh and splitcmp/c2_compare.py)
cd "$(dirname "$(readlink -f "$0")")"
TAG=$(python3 -c "import split_cfg; print(split_cfg.TAG)")
O=../outputs/ASD_2025-26_${TAG}_leaf_analysis_white_rust
SK=/root/.claude/skills/synced/9bf50f97-a337-4b6b-8c8b-ebd229b7e0d3_d565bc3b-4006-4195-b033-a8c25dfdc114
python3 a10_word.py > data/word.log 2>&1 && NODE_PATH=/opt/node22/lib/node_modules node a10_build.js >> data/word.log 2>&1 && python3 ../satmet/to_pdf.py ${O}_report.docx ${O}_report.pdf >> data/word.log 2>&1 && echo word-ok || { echo word-FAILED; tail -5 data/word.log; }
python3 a7_excel.py > data/excel.log 2>&1 && python3 $SK/xlsx/scripts/recalc.py ${O}.xlsx 600 >> data/excel.log 2>&1 && echo excel-ok || { echo excel-FAILED; tail -5 data/excel.log; }
python3 a8_pptdata.py > data/ppt.log 2>&1 && NODE_PATH=/home/user/meta/thesis_build/leaf/node_modules:/opt/node22/lib/node_modules SKILL_DIR=$SK/pptx node a8_ppt.js >> data/ppt.log 2>&1 && python3 $SK/pptx/scripts/office/validate.py ../outputs/ASD_2025-26_${TAG}_leaf_analysis_seminar.pptx >> data/ppt.log 2>&1 && echo ppt-ok || { echo ppt-FAILED; tail -5 data/ppt.log; }
