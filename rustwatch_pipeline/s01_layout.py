"""Step 1 - Field layout, plot polygons and ground-truth labels."""
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
from shapely import affinity
import config as C

# Plot numbers and treatments exactly as in the field-layout slide (row 1 = top/north row).
PLOT_IDS = [
    [48, 41, 40, 33, 32, 25, 24, 17, 16, 9, 8, 1],
    [47, 42, 39, 34, 31, 26, 23, 18, 15, 10, 7, 2],
    [46, 43, 38, 35, 30, 27, 22, 19, 14, 11, 6, 3],
    [45, 44, 37, 36, 29, 28, 21, 20, 13, 12, 5, 4],
]
TREATMENTS = [
    ["D3V3", "D1V1", "D2V2", "D4V3", "D3V2", "D1V3", "D1V1", "D3V2", "D2V3", "D2V1", "D2V3", "D4V2"],
    ["D4V1", "D1V2", "D2V3", "D1V1", "D4V2", "D2V1", "D1V3", "D4V2", "D3V1", "D3V3", "D1V1", "D2V2"],
    ["D4V3", "D4V1", "D1V3", "D2V2", "D1V2", "D2V3", "D2V1", "D2V2", "D4V1", "D3V2", "D4V3", "D1V3"],
    ["D2V2", "D3V2", "D3V1", "D3V1", "D3V3", "D4V1", "D3V3", "D4V3", "D1V2", "D4V1", "D1V2", "D3V1"],
]
BLOCKS = ["R1"] * 3 + ["R2"] * 3 + ["R3"] * 3 + ["CONTROL"] * 3   # by column


def build_layout_table():
    rows = []
    for r in range(C.N_ROWS):
        for c in range(C.N_COLS):
            t = TREATMENTS[r][c]
            rows.append(dict(plot_id=PLOT_IDS[r][c], row=r + 1, col=c + 1, treatment=t,
                             inoc_age=t[:2], variety=t[2:], block=BLOCKS[c],
                             inoculated=BLOCKS[c] != "CONTROL"))
    return pd.DataFrame(rows).sort_values("plot_id").reset_index(drop=True)


def check_layout(layout):
    """Every replication block should contain each of the 12 treatments exactly once."""
    problems = []
    for block, g in layout.groupby("block"):
        counts = g["treatment"].value_counts()
        dup = counts[counts > 1].index.tolist()
        missing = sorted({f"D{d}V{v}" for d in range(1, 5) for v in range(1, 4)} - set(g["treatment"]))
        if dup or missing:
            problems.append(f"{block}: repeated {dup}, missing {missing}")
    return problems


def row_top_offset(r):
    """Distance (m) from the field's north edge to the top of plot row r (1-based)."""
    channels_above = (1 if r >= 2 else 0) + (1 if r >= 4 else 0)
    return (r - 1) * C.PLOT_LENGTH_M + channels_above * C.CHANNEL_M


def build_plot_polygons(layout):
    gap = (C.FIELD_WIDTH_M - C.N_COLS * C.PLOT_WIDTH_M) / (C.N_COLS - 1)
    geoms = []
    for _, p in layout.iterrows():
        x0 = (p.col - 1) * (C.PLOT_WIDTH_M + gap)
        y0 = -row_top_offset(p.row)
        poly = Polygon([(x0, y0), (x0 + C.PLOT_WIDTH_M, y0),
                        (x0 + C.PLOT_WIDTH_M, y0 - C.PLOT_LENGTH_M), (x0, y0 - C.PLOT_LENGTH_M)])
        poly = affinity.rotate(poly, C.FIELD_ROTATION_DEG, origin=(0, 0))
        geoms.append(affinity.translate(poly, C.FIELD_ORIGIN_E, C.FIELD_ORIGIN_N))
    gdf = gpd.GeoDataFrame(layout.copy(), geometry=geoms, crs=C.CRS)
    gdf["geometry_inner"] = gdf.geometry.buffer(-C.PLOT_INSET_M, join_style="mitre")
    return gdf


def di_to_class(di):
    return pd.cut(di, bins=C.DI_CLASS_BINS, labels=range(len(C.CLASS_NAMES))).astype(int)


def load_ground_truth(layout):
    gt = pd.read_csv(C.GROUND_TRUTH_CSV, dtype={"date": str})
    gt["severity_class"] = di_to_class(gt["DI"])
    gt["diseased"] = (gt["severity_class"] > 0).astype(int)
    gt = gt.merge(layout[["plot_id", "block", "treatment", "inoc_age", "variety", "inoculated"]],
                  on="plot_id", how="left")
    bad = gt[(~gt["inoculated"]) & (gt["DI"] > 0)]
    if len(bad):
        print(f"WARNING: {len(bad)} control plot-dates have DI > 0 (natural infection?)")
    return gt


if __name__ == "__main__":
    C.ROOT.mkdir(parents=True, exist_ok=True)
    layout = build_layout_table()
    for msg in check_layout(layout):
        print("LAYOUT CHECK:", msg)
    layout.to_csv(C.LAYOUT_CSV, index=False)
    plots = build_plot_polygons(layout)
    plots.set_geometry("geometry").drop(columns="geometry_inner").to_file(C.PLOTS_FILE, layer="plots")
    print(f"Wrote {len(plots)} plot polygons to {C.PLOTS_FILE}")
    if C.GROUND_TRUTH_CSV.exists():
        gt = load_ground_truth(layout)
        print(gt.groupby(["date", "severity_class"]).size().unstack(fill_value=0))
