WHITE RUST PIXEL MAPS – ONE JUPYTER NOTEBOOK PER MODEL (UAV hyperspectral image of 24 Feb 2026)
==============================================================================================

Each notebook is complete on its own: it reads the ENVI image block by block, computes the features of ITS model
from every crop pixel, applies the model, and writes the pixel map (ENVI .dat/.hdr, GeoTIFF, PNG), a self-check on
the 48 plot-mean spectra and the per-plot accuracy against the ASD leaf scores of 24 Feb.

  Notebook                                        Task                          Model             Use
  A_ConvNeXt_V2-Atto_pixel_map_24Feb2026.ipynb    detection (healthy/diseased)  ConvNeXt V2-Atto  RECOMMENDED map (only model that transferred to the UAV plots)
  A_SVM_pixel_map_24Feb2026.ipynb                 detection                     SVM               best leaf model (ML); at chance on the UAV plots
  A_DNN-F1_pixel_map_24Feb2026.ipynb              detection                     DNN-F1            best leaf model (DL); at chance on the UAV plots
  B_ConvNeXt_V2-Atto_pixel_map_24Feb2026.ipynb    six grades                    ConvNeXt V2-Atto  best leaf model (DL); NOT validated on the UAV
  B_RF_pixel_map_24Feb2026.ipynb                  six grades                    Random forest     best leaf model (ML); NOT validated on the UAV
  C_XGBoost_pixel_map_24Feb2026.ipynb             severity score 0-9            XGBoost           best leaf model (ML); NOT validated on the UAV
  C_DNN-F1_pixel_map_24Feb2026.ipynb              severity score 0-9            DNN-F1            best leaf model (DL); NOT validated on the UAV

How to run (Windows)
  1. Put these notebooks in the unzipped kit folder (next to the folder 'models'), e.g. D:\Coalighned\white_rust_pixel_kit
  2. Install once:  pip install numpy scipy pandas matplotlib
                    pip install torch --index-url https://download.pytorch.org/whl/cpu     (only for ConvNeXt and DNN-F1 notebooks)
                    pip install rasterio                                                     (optional, GeoTIFF output)
  3. Open a notebook in Jupyter, check the four paths in cell 1 (HDR_FILE, ROI_FILE, MODEL_FILE, PLOT_AVG_FILE).
     The image data file 'subset_200526' (about 9 GB) must be in the same folder as subset_200526.hdr.
  4. Run all cells with SPATIAL_STEP = 4 (preview). The self-check must print "OK".
     Then set SPATIAL_STEP = 1 and run again for the final full-resolution map.

Results: folder white_rust_pixel_map_24Feb2026_<model> next to the image.

Notes
  - Plots 1 and 48 extend slightly beyond the image (95 % and 89 % of the plot inside); only their pixels inside are used.
  - Tested here end to end on a synthetic image with the real header (483 bands), the real 48 plot outlines and the
    48 plot-mean spectra: every plot value of every map equals the model's prediction for that plot (max difference 2e-5).
