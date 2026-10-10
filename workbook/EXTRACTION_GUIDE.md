# Extraction guide: META_ANALYSIS_MASTER_FINAL.xlsx

This is a working summary of the workbook's own README, RULES (141 rules), Codes and FORMULAS sheets. If this guide and the workbook disagree, the workbook wins.

State: latest version **META_ANALYSIS_MASTER updated 142.xlsx** (ext 646-650). **Next serial = 326.** Bibliography has 461 references. New batches: write one module per study (see sNNN.py / cNN.py) and run `batch.py`. Build scripts for each batch are in `workbook/build/` (wblib.py = row-append helper; sNNN.py = one study; buildNNN.py = batch).

## Workbook map (192 sheets)
- **Rulebook:** README (history log, one line per batch), RULES (numbered rules with status), Codes, FORMULAS.
- **Study-level sheets:** Study_Info (44 cols, one row per study x site; fill it FIRST), Treatment_Mapping (one row per paper treatment, giving its code, rationale, confidence and status), LAT_LONG, Bibliography (APA; col B = serial), EXCLUDED_rows (sheet, serial, authors, year, reason, full row).
- **Auto-generated index sheets, rebuilt at every build:** PARAMETERS_BY_STUDY and STUDIES_BY_PARAMETER.
- **About 180 parameter sheets.** All use the same layout:
  `No. | SERIAL NO | Authors | Year | Journal | Country | Site/Location | latitude | longitude | CLIMATE | year of data | DURATION | SOIL | [DEPTH | DEPTH (as reported)] | <PFX>_CA, CT, ZT, DT, MTR, MT, CTR, DTR, pCA, pZT, pMTR, pMT (x crop groups W / R / SYS where relevant) | Obs | Rep | SD | CLAY | MIN TEMP | MAX TEMP | RAIN FALL | LATT | YEAR OF DATA (duration) | AVG T | April max temp | ph (initial) | soc (initial) | Bdi | sand | silt | UNIT | Treatment mapping | Crop/season of sampling | Fertilizer dose & other management | Data source | Notes/Doubts | Treatment details (from paper) | Method used (from paper) | (blank) | UNIT FOR THIS SHEET`.
  - Soil sheets have DEPTH columns. Crop and economic sheets (YIELD, WUE, NUE, BC ratio, NET RETURN, GHG ...) have none and use W / R / SYS groups.
  - Header colours: dark blue 1F4E79 = identity, teal 0E7490 = depth, green 2E7D32 = values, amber B45309 = Obs/Rep/SD, grey 4B5563 = covariates, purple 7C3AED = text.

## Row conventions
- New rows are **appended at the bottom** of each sheet. `No.` = serial number (integer part); `SERIAL NO` = `318`, `23 (companion 14)` and so on.
- Arial 10. The Notes/Doubts cell has fill **FFF2CC** (Study_Info notes use FFF3CD).
- **Rice-season rows:** the whole row is in red font (FF0000) and `Crop/season of sampling` starts with "RICE SEASON".
- SD is a live formula: `=IF(AND(N(Obs)>0,N(Rep)>0),SQRT(1/(((Rep*Rep)/(Rep+Rep))/Obs)),"")`, which equals SQRT(2*Obs/Rep). A paper-reported SD replaces it (SE x sqrt(Rep)).
- **Rep** = 3 unless the paper states otherwise. **Obs** = Y + T + D (years + treatments under one code + depths in the class). A factor equal to 1 adds nothing, and the minimum is 1. Notes end with the Y/T/D breakdown.
- Derived values are written as live formulas (for example `=ROUND(0.14*10/1.724,2)` or cross-sheet links), and Data source says DERIVED or Calculated.
- **Notes/Doubts** opens with the row tag (`ROW a: CT = ..., CTR = ...`), then flags, then `||` and the full reference.
- **Treatment details** = `TREATMENTS IN PAPER: ... || MAPPING: label -> code: description [rice phase; wheat phase; residue]`.
- **Method used** = the paper's method, or "Not stated in paper".
- Data source tags: Text / Table n / Figure n (digitised) / Supplementary / Calculated / DERIVED / MODEL OUTPUT / Author-reported.
- Data validations: CLIMATE ST/TEMP. SOIL LOAMY/SANDY/CLAYEY. DURATION 0-3 Y / 4-10 Y / >10 Y. DEPTH 0-15/15-30/30-45/45-60/>60 CM. PR uses 0-10 ... 50-60 CM. Stock and sequestration use cumulative 0-10 ... 0-60 CM.

## Key coding rules (see the RULES sheet for the full list)
- Codes: CA = ZT + residue; ZT; CT; CTR; MT; MTR; DT (>=25 cm); DTR. Partial codes (tilled or puddled rice + conservation wheat): pCA, pZT, pMT, pMTR.
- **Rotary rule (13/69):** full-width >=10 cm or >=2 passes = CT/CTR. Rotary <=8 cm, single-pass till-drill, Super/Roto Seeder or strip/zone = MT/MTR. 8-10 cm or depth unstated: ask the author.
- **Reduced-tillage rule (127):** anything the paper calls "reduced tillage" goes to the MT family.
- **Rotation matching:** no-till rice + conventional wheat is EXCLUDED. Rice tillage not stated: code on wheat tillage alone (23). Tilled DSR + ZT wheat = pZT/pCA (124/138). DSR + reduced-till wheat = MT (135). Puddling intensity: low = MT, medium/high = CT (140).
- Inclusion: any two usable codes (72). Excluded: rice-maize, wheat-maize, double rice, INM-only trials, amendments (biochar, compost), unfertilised tiers, pot trials, reviews and meta-analyses.
- Factorials: use cell means, one row per non-tillage factor level. Main effects only: flag them, or put them in Notes if pooled over an excluded level (65).
- Several paper treatments under one code: rows a/b/c, with the other codes repeated in each row.
- Year-wise, stage-wise, depth-wise and size-class values: every data point gets its own row.
- Wheat season is the default for soil. A value reported only for the rice season goes in a red row.
- Repeats (136): a complete repeat goes to EXCLUDED_rows only. A partial repeat becomes a companion carrying only the new data.
- Same trial = same serial with "(companion n)". A new trial gets the next serial.

## Key derivations (FORMULAS sheet)
- SOC = OM / 1.724.
- Stock = SOC x BD x cm x 0.1, cumulative from the surface.
- Porosity = (1 - BD/PD) x 100, using the paper's PD or else 2.65.
- HI = grain / (grain + straw). Straw = biomass - grain.
- B:C = net / cost (gross/cost minus 1).
- GWP = CH4 x 28 + N2O x 265. GHGI = GWP / (grain t/ha x 1000).
- CL / LI / CPI / CMI use CT as the reference.
- WSA is in g/g (0-1). GWC = VWC / BD (default BD 1.35).
- CH4 is stored as kg C (x12/16) and N2O as kg N (x28/44).

## Per-batch build checklist
1. Check for duplicates (DOI, title) in Study_Info. Search for supplementary material and record "none found" if there is none.
2. Fill Study_Info, LAT_LONG, Treatment_Mapping (every treatment) and Bibliography.
3. Append the data rows to every relevant sheet. Use formulas for derived values. Use red rows for rice-season data.
4. Log exclusions and repeats in EXCLUDED_rows.
5. Add a README history line ("ext NNN-NNN (updated NN, date)": serials, repeats, excluded, "Bibliography + n. Next serial N"). Add any new rule to RULES.
6. Regenerate PARAMETERS_BY_STUDY and STUDIES_BY_PARAMETER.
7. Recalculate with LibreOffice and confirm 0 formula errors. Diff against the previous version: only the intended cells may change.
8. Save as a new numbered version (the previous file is never overwritten).
9. At the end, list anything that was not extracted.
