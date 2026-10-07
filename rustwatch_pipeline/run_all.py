"""Run the whole pipeline in order.   python run_all.py            (all steps)
                                      python run_all.py 5 6        (only steps 5 and 6)"""
import sys
import config as C
import s01_layout, s02_preprocess, s03_masking, s04_endmembers, s05_features, s06_dsf, s08_fusion_maps


def step1():
    layout = s01_layout.build_layout_table()
    for msg in s01_layout.check_layout(layout):
        print("LAYOUT CHECK:", msg)
    layout.to_csv(C.LAYOUT_CSV, index=False)
    if not C.PLOTS_FILE.exists():
        s01_layout.build_plot_polygons(layout).drop(columns="geometry_inner").to_file(C.PLOTS_FILE, layer="plots")


STEPS = {
    1: ("Field layout and plot polygons", step1),
    2: ("Pre-processing and co-registration", s02_preprocess.preprocess_all),
    3: ("Vegetation masking", lambda: [s03_masking.mask_date(d) for d in C.DATES]),
    4: ("Endmember extraction and unmixing", lambda: s04_endmembers.run_unmixing("HS")),
    5: ("Plot-wise feature extraction", lambda: [s05_features.extract(s) for s in C.SENSORS]),
    6: ("Phase 1 DSF selection (full data, for reporting)",
        lambda: [s06_dsf.select_dsf(*s06_dsf.load_table([s]), out_prefix=s) for s in C.SENSORS]),
    7: ("Phases 2-3: nested CV, fusion, final model, SHAP, maps, regression", s08_fusion_maps.main),
}

if __name__ == "__main__":
    todo = [int(a) for a in sys.argv[1:]] or list(STEPS)
    for k in todo:
        name, fn = STEPS[k]
        print(f"\n===== Step {k}: {name} =====")
        fn()
