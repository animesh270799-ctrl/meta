#!/bin/bash
cd /home/user/meta/thesis_build
echo "70-30:"; asd7030/build_reports.sh
echo "80-20:"; asd8020/build_reports.sh
echo "comparison:"; splitcmp/build_compare.sh
echo "package:"; python3 splitcmp/c6_package.py
echo FINALDONE
