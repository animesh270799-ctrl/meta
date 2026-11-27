#!/bin/bash
# Rebuild every Part L deliverable from the step outputs in ../out (one table source for Excel, PPT and Word).
set -e
cd "$(dirname "$0")"; OUT=/home/user/meta/thesis_build/outputs; SK=/root/.claude/skills/synced/9bf50f97-a337-4b6b-8c8b-ebd229b7e0d3_d565bc3b-4006-4195-b033-a8c25dfdc114
python3 d1_tables.py > /dev/null; python3 d3_figs.py
python3 d4_excel.py $OUT/PartL_ASD_2025-26_leaf_analysis.xlsx && python3 $SK/xlsx/scripts/recalc.py $OUT/PartL_ASD_2025-26_leaf_analysis.xlsx 300
python3 d5_pptdata.py && NODE_PATH=/home/user/meta/thesis_build/leaf/node_modules node d5_ppt.js $OUT/PartL_ASD_2025-26_leaf_analysis.pptx && python3 d6_post.py $OUT/PartL_ASD_2025-26_leaf_analysis.pptx
python3 $SK/pptx/scripts/office/validate.py $OUT/PartL_ASD_2025-26_leaf_analysis.pptx | tail -1
python3 d7_word.py $OUT/PartL_ASD_2025-26_leaf_analysis_report.docx && NODE_PATH=/opt/node22/lib/node_modules node word_build.js
cd $OUT && (zip -dq PartL_ASD_2025-26_leaf_analysis_report.docx '*/' 2>/dev/null || true) && python3 ../satmet/to_pdf.py PartL_ASD_2025-26_leaf_analysis_report.docx PartL_ASD_2025-26_leaf_analysis_report.pdf
