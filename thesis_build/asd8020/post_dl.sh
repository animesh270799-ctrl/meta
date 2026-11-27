#!/bin/bash
# runs after the four DL workers finish: metrics, figures, final networks, models README, report, workbook, slides
cd /home/user/meta/thesis_build/asd26
until grep -q DLDONE data/dl_merge.log 2>/dev/null; do sleep 30; done
cat data/dl_merge.log
SKIP_TRANSFER=1 python3 a5_extra.py > data/extra2.log 2>&1 && echo extra-ok
python3 a6_figs.py > data/figs.log 2>&1 && echo figs-ok
i=0; for n in "DNN-F1" "DT-EDNet" "EfficientNet-B0" "ResNet18" "ConvNeXt V2-Atto"; do TT=1 python3 a9_final.py dl "$n" "n$i" > data/final_dl_$i.log 2>&1 & i=$((i+1)); done; wait; echo final-dl-ok
python3 a9_readme.py > data/readme.log 2>&1 && echo readme-ok
python3 a10_word.py > data/word.log 2>&1 && NODE_PATH=/opt/node22/lib/node_modules node a10_build.js >> data/word.log 2>&1 && python3 ../satmet/to_pdf.py ../outputs/ASD_2025-26_80-20_leaf_analysis_white_rust_report.docx ../outputs/ASD_2025-26_80-20_leaf_analysis_white_rust_report.pdf >> data/word.log 2>&1 && echo word-ok
python3 a7_excel.py > data/excel.log 2>&1 && python3 /root/.claude/skills/synced/9bf50f97-a337-4b6b-8c8b-ebd229b7e0d3_d565bc3b-4006-4195-b033-a8c25dfdc114/xlsx/scripts/recalc.py ../outputs/ASD_2025-26_80-20_leaf_analysis_white_rust.xlsx 600 >> data/excel.log 2>&1 && echo excel-ok
SK=/root/.claude/skills/synced/9bf50f97-a337-4b6b-8c8b-ebd229b7e0d3_d565bc3b-4006-4195-b033-a8c25dfdc114/pptx
python3 a8_pptdata.py > data/ppt.log 2>&1 && NODE_PATH=/home/user/meta/thesis_build/leaf/node_modules:/opt/node22/lib/node_modules SKILL_DIR=$SK node a8_ppt.js >> data/ppt.log 2>&1 && python3 $SK/scripts/office/validate.py ../outputs/ASD_2025-26_80-20_leaf_analysis_seminar.pptx >> data/ppt.log 2>&1 && echo ppt-ok
echo POSTDONE
