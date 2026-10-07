"""Create a small synthetic dataset with the same structure as the real one
(48 plots, 4 dates, MS / HS / RGB / TIR orthomosaics, ground truth, weather),
so that every step of the pipeline can be tested before real data are ready.
The spectra are simplified; results on these data say nothing about real accuracy."""
import numpy as np
import pandas as pd
import geopandas as gpd
from rasterio.features import rasterize
from rasterio.transform import from_origin
from scipy.ndimage import gaussian_filter
import config as C
from common import write_raster
from s01_layout import build_layout_table, build_plot_polygons

rng = np.random.default_rng(1)
FINE = 0.02                                   # m, base grid
MARGIN = 2.0
X0, Y0 = C.FIELD_ORIGIN_E - MARGIN, C.FIELD_ORIGIN_N + MARGIN
W, H = int((C.FIELD_WIDTH_M + 2 * MARGIN) / FINE), int((C.FIELD_LENGTH_M + 2 * MARGIN) / FINE)
FACTORS = {"RGB": 1, "MS": 2, "TIR": 4, "HS": 10}     # 2 cm, 4 cm, 8 cm, 20 cm
WL = np.arange(400, 2501, 15.0)
AIR = {d: t for d, t in zip(C.DATES, [20.0, 22.5, 19.0, 24.0])}


def spectra():
    wl = WL
    soil = 0.10 + 0.18 * (wl - 400) / 2100
    def veg(s):
        vis = 0.04 + 0.05 * np.exp(-((wl - 550) / 30) ** 2) - 0.015 * np.exp(-((wl - 670) / 25) ** 2)
        vis += s * (0.05 * np.exp(-((wl - 600) / 60) ** 2))                      # chlorosis
        edge = 1 / (1 + np.exp(-(wl - (715 - 12 * s)) / 12))
        nir = (0.48 * (1 - 0.3 * s)) * edge
        water = 1 - (0.06 * np.exp(-((wl - 970) / 25) ** 2) + 0.1 * np.exp(-((wl - 1200) / 40) ** 2)
                     + 0.6 * np.exp(-((wl - 1450) / 60) ** 2) + 0.7 * np.exp(-((wl - 1940) / 70) ** 2)) * (1 - 0.3 * s)
        swir = np.where(wl > 1300, (0.35 - 0.12 * (wl - 1300) / 1200) + 0.08 * s, 1)
        return (vis * (1 - edge) + nir * np.where(wl > 1300, swir / 0.48, 1)) * water
    return soil, veg(0.0), veg(1.0), np.full_like(wl, 0.55)


def block_mean(a, f):
    h, w = a.shape[0] // f * f, a.shape[1] // f * f
    return a[:h, :w].reshape(h // f, f, w // f, f).mean((1, 3))


def main():
    for d in [C.ROOT]:
        d.mkdir(parents=True, exist_ok=True)
    layout = build_layout_table()
    layout.to_csv(C.LAYOUT_CSV, index=False)
    plots = build_plot_polygons(layout)
    plots.set_geometry("geometry").drop(columns="geometry_inner").to_file(C.PLOTS_FILE, layer="plots")

    sus = {"V1": 1.4, "V2": 1.0, "V3": 0.7}
    age = {"D1": 1.2, "D2": 1.0, "D3": 0.8, "D4": 0.6}
    tf = [0.25, 0.55, 0.85, 1.15]
    gt = []
    for _, p in layout.iterrows():
        base = rng.lognormal(0, 0.35)
        for t, date in zip(tf, C.DATES):
            di = 0.0 if not p.inoculated else float(np.clip(32 * sus[p.variety] * age[p.inoc_age] * t * base, 0.5, 95))
            gt.append(dict(plot_id=p.plot_id, date=date, DI=round(di, 1)))
    gt = pd.DataFrame(gt)
    gt.to_csv(C.GROUND_TRUTH_CSV, index=False)
    pd.DataFrame(dict(date=C.DATES, air_temp_C=[AIR[d] for d in C.DATES])).to_csv(C.WEATHER_CSV, index=False)
    np.savetxt(C.HS_WAVELENGTH_FILE, WL, fmt="%.1f")

    tr = from_origin(X0, Y0, FINE, FINE)
    pid = rasterize([(g, int(i)) for g, i in zip(plots.geometry, plots.plot_id)], (H, W), transform=tr, dtype="int32")
    soil, healthy, diseased, white = spectra()
    for date in C.DATES:
        di_map = dict(zip(gt[gt.date == date].plot_id, gt[gt.date == date].DI))
        s_fine = np.vectorize(lambda i: min(di_map.get(i, 0) / 50, 1.0))(pid) * (pid > 0)
        noise = gaussian_filter(rng.standard_normal((H, W)), 6)
        veg = (pid > 0) & (noise > np.quantile(noise, 0.2) + 0.25 * s_fine * noise.std())
        pust = veg & (rng.random((H, W)) < 0.25 * s_fine)
        for sensor, f in FACTORS.items():
            fv, fp, s = block_mean(veg.astype(float), f), block_mean(pust.astype(float), f), block_mean(s_fine, f)
            h, w = fv.shape
            prof = dict(driver="GTiff", height=h, width=w, crs=C.CRS, transform=from_origin(X0, Y0, FINE * f, FINE * f))
            spec = ((fv - fp)[None] * healthy[:, None, None] + ((fv - fp) * s)[None] * (diseased - healthy)[:, None, None]
                    + fp[None] * white[:, None, None] + (1 - fv)[None] * soil[:, None, None])
            if sensor == "HS":
                cube = spec + rng.normal(0, 0.004, spec.shape)
                write_raster(C.raw_path("HS", date), np.clip(cube, 0, 1) * 10000, prof, dtype="uint16", nodata=0)
            elif sensor == "MS":
                idx = [int(np.argmin(np.abs(WL - c))) for c in C.MS_BANDS.values()]
                write_raster(C.raw_path("MS", date), spec[idx] + rng.normal(0, 0.005, (5, h, w)), prof)
            elif sensor == "RGB":
                idx = [int(np.argmin(np.abs(WL - c))) for c in (640, 550, 470)]
                rgb = np.clip(spec[idx] / 0.6 * 255 + rng.normal(0, 4, (3, h, w)), 0, 255)
                write_raster(C.raw_path("RGB", date), rgb, prof, dtype="uint8", nodata=None)
            else:
                at = AIR[date]
                t_c = fv * (at - 3 + 4 * s) + (1 - fv) * (at + 9) + rng.normal(0, 0.3, (h, w))
                shifted = prof.copy()
                shifted["transform"] = from_origin(X0 + 0.24, Y0, FINE * f, FINE * f)   # 24 cm registration error
                write_raster(C.raw_path("TIR", date), t_c + 273.15, shifted)
        print(f"synthetic {date}: written")


if __name__ == "__main__":
    main()
