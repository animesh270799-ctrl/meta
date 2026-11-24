WHITE RUST PIXEL-LEVEL DISEASE MAPS - UAV hyperspectral image of 24 Feb 2026
===========================================================================

Contents of this kit
  White_rust_pixel_map_24Feb2026.ipynb   the complete Jupyter notebook (all code, explained step by step)
  models/                                 the top ASD models in version-independent form
     A_ConvNeXt_V2-Atto.pt   detection  - best transfer to the UAV plots (RECOMMENDED map)
     A_SVM.npz               detection  - best overall / best ML on the leaves
     A_DNN-F1.pt             detection  - best DL on the leaves
     B_ConvNeXt_V2-Atto.pt   six grades - best overall / best DL on the leaves
     B_RF.npz                six grades - best ML on the leaves
     C_XGBoost.npz           severity score - best overall / best ML on the leaves
     C_DNN-F1.pt             severity score - best DL on the leaves
     model_table.json        inputs, input variant and UAV accuracy of every model

How to run (Windows)
  1. Unzip this kit, e.g. to  D:\Coalighned\white_rust_pixel_kit
  2. Install the packages once (Anaconda Prompt or terminal):
        pip install numpy scipy pandas matplotlib
        pip install torch --index-url https://download.pytorch.org/whl/cpu
        pip install rasterio        (optional: GeoTIFF copies of the maps)
  3. Open White_rust_pixel_map_24Feb2026.ipynb in Jupyter.
  4. In cell 1 (SETTINGS) check the paths:
        HDR_FILE      = D:\Coalighned\24_02_2026\subset_200526.hdr   (the data file subset_200526 must be next to it)
        ROI_FILE      = D:\Coalighned\24_02_2026\48_plot_roi_new.xml (optional, for the per-plot accuracy)
        KIT_DIR       = the folder where you unzipped this kit
        PLOT_AVG_FILE = envi_plot_avg.txt (optional, for the self-check)
  5. Run all cells with SPATIAL_STEP = 4 (quick preview), check that the self-check prints "OK" for every model,
     then set SPATIAL_STEP = 1 and run again for the final full-resolution maps.

Outputs (folder white_rust_pixel_maps_24Feb2026 next to the image)
  <model>_score / _class (.dat/.hdr, .tif)  detection probability and class (1 healthy, 2 diseased)
  <model> (.dat/.hdr, .tif)                 grade or score map
  <model>_map.png, all_models_overview.png  maps
  <model>_per_plot.csv, per_plot_accuracy_all_models.csv   per-plot values and accuracy vs the ASD scores of 24 Feb
  run_info.json

Which map to use
  The ConvNeXt V2-Atto DETECTION map is the only one that transferred beyond chance to the UAV plots
  (macro-F1 0.736, 95 % CI 0.58-0.87; maximum-statistic permutation p = 0.015). The other detection maps are at chance;
  the grade and score maps are NOT validated and must not be read as severity. See the transfer report
  (UAV_24Feb2026_ASD_model_transfer_report) for all details.
