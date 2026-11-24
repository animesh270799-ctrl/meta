#!/bin/bash
# comparison outputs: c2 (tables, figures, per-split summaries) -> Word/PDF -> Excel -> slides
cd "$(dirname "$(readlink -f "$0")")"
SK=/root/.claude/skills/synced/9bf50f97-a337-4b6b-8c8b-ebd229b7e0d3_d565bc3b-4006-4195-b033-a8c25dfdc114
O=../outputs/ASD_2025-26_validation_comparison_LORO_70-30_80-20
python3 c2_compare.py > out/c2.log 2>&1 && echo c2-ok || { echo c2-FAILED; tail -5 out/c2.log; }
python3 c3_word.py > out/word.log 2>&1 && NODE_PATH=/opt/node22/lib/node_modules node c3_build.js >> out/word.log 2>&1 && python3 ../satmet/to_pdf.py ${O}_report.docx ${O}_report.pdf >> out/word.log 2>&1 && echo word-ok || { echo word-FAILED; tail -5 out/word.log; }
python3 c4_excel.py > out/excel.log 2>&1 && python3 $SK/xlsx/scripts/recalc.py ${O}.xlsx 600 >> out/excel.log 2>&1 && echo excel-ok || { echo excel-FAILED; tail -5 out/excel.log; }
python3 c5_pptdata.py > out/ppt.log 2>&1 && NODE_PATH=/home/user/meta/thesis_build/leaf/node_modules:/opt/node22/lib/node_modules SKILL_DIR=$SK/pptx node c5_ppt.js >> out/ppt.log 2>&1 && python3 $SK/pptx/scripts/office/validate.py ${O}.pptx >> out/ppt.log 2>&1 && echo ppt-ok || { echo ppt-FAILED; tail -5 out/ppt.log; }
