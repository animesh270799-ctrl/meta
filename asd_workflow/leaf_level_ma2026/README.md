# Leaf-level ASD analysis following Ma et al. (2026)

Scripts that produced `ASD_Leaf_WhiteRust_StepByStep.xlsx`, `ASD_Leaf_WhiteRust_Seminar.pptx` and
`ASD_Leaf_WhiteRust_Research_Paper.docx` from the four `asd__data_complete_labelled_*_scored.xlsx` files.

1. `parse.py` – reads the four workbooks (raw pickle of the sheets) into one leaf table; duplicates are removed in the cleaning step.
2. `analysis.py leaf_clean.pkl results.pkl` – pre-processing, NDSI/RSI, effective ranges, RFE-RF / SAND / CARS-PLS,
   vegetation indices + Relief, RF / SVM / PLS-DA / MLP, plot-grouped 5-fold CV and the independent 13 Mar test.
3. `export_json.py`, `figures.py`, `flow.py` – results JSON and figures.
4. `build_excel.py`, `build_ppt.js` (pptxgenjs), `build_doc.js` (docx; uses the helper `lib.js` from the handbook scripts) – outputs.

Whole range 350–2500 nm is used (contact probe), texture features/TTFI are omitted (non-imaging data), and no SHAP is used.
