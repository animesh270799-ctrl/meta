"""Digital image processing and machine learning: interview guide (docx JS via thesis helpers)."""
import re, json, os, glob
B = os.path.dirname(os.path.abspath(__file__)) + '/'; S = B + '../'
K = []; TN = [0]
def esc(t):
    t = t.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    return re.sub(r'\[\[(T|F):(\w+)\]\]', lambda m: '${%s(\'%s\')}' % (m.group(1), m.group(2)), t)
js = lambda s: '`' + esc(s) + '`'
def H1(t): K.append("K.push(H1(%s));" % js(t))
def P(t): K.append("K.push(P(%s));" % js(t))
def BL(items): K.extend("K.push(BL(%s));" % js(i) for i in items)
def NOTE(t): K.append("K.push(NOTE(%s));" % js(t))
def EQ(t): K.append("K.push(EQ(%s));" % js(t))
def FIG(k, f, cap, w=520): K.append("K.push(...fig2('%s', '%s', %s, %d));" % (k, f, js(cap), w))
def TAB(k, rows, widths, cap, size=15):
    Rr = '[' + ',\n'.join('[' + ', '.join(js(str(c)) for c in r) + ']' for r in rows) + ']'
    K.append("K.push(...tab2('%s', %s, %s, %s, %d));" % (k, Rr, json.dumps(widths), js(cap), size))
def LAB(l, t, c='1565C0'): K.append("K.push(new Paragraph({ spacing: { after: 70, line: 285 }, alignment: AlignmentType.JUSTIFIED, children: [new TextRun({ text: %s, bold: true, font: FONT, size: 21, color: '%s' }), ...runs(%s, { size: 21 })] }));" % (js(l + ' '), c, js(t)))
def T(title, concept, eq=None, how=None, use=None, mine=None, pros=None, cons=None, qs=(), figs=()):
    TN[0] += 1
    K.append("K.push(H2(%s));" % js('%d. %s' % (TN[0], title)))
    LAB('Concept:', concept)
    if eq: [EQ(e) for e in (eq if isinstance(eq, list) else [eq])]
    if how: K.append("K.push(new Paragraph({ spacing: { before: 40, after: 40 }, keepNext: true, children: [new TextRun({ text: 'How it works:', bold: true, font: FONT, size: 21, color: '2E7D32' })] }));"); BL(how)
    for f in figs: FIG(*f)
    if use: LAB('Use in agricultural / disease remote sensing:', use, '00838F')
    if mine: LAB('In my thesis:', mine, 'C98A00')
    if pros or cons: LAB('Strengths:', pros or '—', '2E7D32'); LAB('Limitations:', cons or '—', 'C62828')
    for q, a in qs: K.append("QA(%s, %s);" % (js(q), js(a)))

# ================= TITLE =================
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 800, after: 160 }, children: [new TextRun({ text: 'Digital image processing and machine learning', font: FONT, size: 44, bold: true, color: '1E3A1F' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: 'Techniques you should know for the NRSC / SAC (ISRO) interview — concept, equations, use in crop-disease remote sensing, and interview questions', font: FONT, size: 26, color: '2C5F2D' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 }, children: [new TextRun({ text: 'Ph.D. (Agricultural Physics), ICAR-IARI  |  AI-based multimodal UAV sensing of white rust in mustard', font: FONT, size: 20, italics: true, color: '555555' })] }));")
NOTE('**How to use this guide.** Each technique has the same parts: **concept** (say this first), **equation**, **how it works**, **use in agricultural and disease remote sensing** with references, **in my thesis** (link every answer to your work), **strengths and limitations**, and **interview questions**. Image-processing figures use a simulated five-band field scene (soil, healthy plots, diseased patches); machine-learning figures use your real leaf ASD data (2339 leaves).')
K.append("K.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-2' }));")
K.append("K.push(new Paragraph({ children: [new PageBreak()] }));")

# ================= PART A: DIP FUNDAMENTALS =================
H1('A. Digital image fundamentals')
FIG('chain', 'd_chain.png', 'Image-processing chain from raw data to features.', 470)
T('Digital image, bands and resolutions',
  'A digital image is a grid of pixels; each pixel stores a digital number (DN) per spectral band. A multiband image forms a data cube (rows × columns × bands). Four resolutions describe a sensor: spatial (ground pixel size), spectral (number and width of bands), radiometric (bit depth, signal-to-noise ratio) and temporal (revisit).',
  how=['Bit depth sets the number of grey levels: 8 bit = 256, 12 bit = 4096, 16 bit = 65 536.', 'Ground sampling distance of a UAV camera: GSD = (flying height × sensor pixel size) / focal length.', 'Hyperspectral cubes have hundreds of contiguous narrow bands; multispectral images have a few broad bands.'],
  use='Spatial resolution decides whether pixels are pure crop; spectral resolution decides whether red-edge and SWIR features can be measured; temporal resolution decides whether onset is caught (Thenkabail et al., 2004; Mahlein, 2016).',
  mine='Hyperspectral VNIR + SWIR (481 bands), MicaSense 5 bands, RGB and thermal on the same plots; 8 flight dates.',
  qs=[('What is the GSD at 60 m height for a camera with 3.45 µm pixels and 5.5 mm focal length?', 'GSD = 60 × 3.45 × 10⁻⁶ / 5.5 × 10⁻³ ≈ 0.038 m, i.e. about 3.8 cm.'),
      ('Which resolution matters most for disease?', 'Spectral (narrow red-edge and SWIR bands) and temporal (onset); spatial only needs to keep plots pure.')])
T('Radiometric correction: DN to radiance to reflectance',
  'Converts sensor DNs into physical units so that images from different dates and sensors can be compared. Radiance L = gain × DN + offset; reflectance ρ = π L d² / (E_{sun} cos θ_{s}) at the top of atmosphere, or surface reflectance after atmospheric correction.',
  eq=['L_{λ} = gain_{λ} × DN + offset_{λ}', 'ρ_{TOA} = π L_{λ} d² / (E_{sun,λ} cos θ_{s})'],
  how=['Dark-current subtraction and vignetting (flat-field) correction for UAV cameras.', '**Empirical line method:** reflectance panels of known reflectance in the image give a linear DN → reflectance relation per band (Smith and Milton, 1999).', 'Downwelling irradiance sensors correct for changing sunlight during a flight.'],
  use='All vegetation indices assume reflectance; without calibration, index changes may reflect illumination, not disease.',
  mine='MicaSense panels and irradiance sensor; hyperspectral panels; ASD reference panel (white reference) for leaf spectra.',
  pros='Physically comparable data across dates and sensors.', cons='Panel errors, changing clouds and BRDF effects remain.',
  qs=[('Why is reflectance better than radiance for comparing dates?', 'Reflectance removes the effect of sun angle, Earth–Sun distance and illumination intensity, which change between flights.')])
T('Atmospheric correction',
  'Removes scattering (aerosols, molecules) and absorption (water vapour, oxygen, ozone) between the surface and the sensor to obtain surface reflectance.',
  how=['**Dark object subtraction (DOS):** the darkest pixels should have near-zero reflectance; their value is subtracted as path radiance (Chavez, 1988).', '**Radiative-transfer models** (6S, MODTRAN; FLAASH, Sen2Cor) model the atmosphere from aerosol and water-vapour estimates (Vermote et al., 1997).', 'UAV flights at low altitude need little atmospheric correction; satellite data need it.'],
  use='Red-edge and SWIR anomalies caused by disease are a few percent of reflectance, comparable to haze effects.',
  mine='Water-vapour bands 1350–1450 and 1800–1950 nm removed from hyperspectral data; satellites: surface-reflectance products for upscaling.',
  qs=[('What is path radiance?', 'Radiance scattered by the atmosphere into the sensor without reaching the surface; it adds brightness, mostly in blue bands.')])
T('Thermal image processing',
  'Thermal sensors measure emitted radiance (8–14 µm). Brightness temperature is obtained by inverting Planck\'s law; surface temperature requires correcting for emissivity and atmosphere.',
  eq=['T_{B} = K_{2} / ln(K_{1} / L_{λ} + 1);    T_{s} ≈ T_{B} / [1 + (λ T_{B} / ρ) ln ε]'],
  how=['Radiometric calibration and non-uniformity correction (camera warm-up, blackbody or ground targets).', 'Emissivity of vegetation ≈ 0.97–0.99; an emissivity error of 0.01 changes temperature by about 0.5 °C.', 'Satellites use single-channel or split-window algorithms for land-surface temperature (Jiménez-Muñoz and Sobrino, 2003; Wan and Dozier, 1996).', 'Normalisation for weather: canopy–air temperature difference (CTD), NRCT, CWSI (Jackson et al., 1981).'],
  use='Diseased plants close stomata and transpire less, so the canopy warms before or with visible symptoms (Mahlein et al., 2019; Calderón et al., 2013).',
  mine='FLIR Vue Pro R: 15–20 min warm-up, radiometric conversion with emissivity, air temperature, humidity and distance; HS crop mask; CT, CTD, CTR (kelvin), NRCT, MTD, thermal GLCM.',
  qs=[('Why compute CTR in kelvin?', 'A ratio of Celsius values depends on the zero of the scale; kelvin is an absolute scale.'), ('Why is thermal not disease-specific?', 'Drought also closes stomata; a water index or RWC must separate the two.')])
T('Geometric correction, orthorectification and resampling',
  'Places each pixel at its correct ground position. A polynomial transformation fitted to ground control points (GCPs) maps image to map coordinates; orthorectification also removes relief displacement using a DEM (Toutin, 2004). New pixel values are obtained by resampling.',
  eq=['x\' = a_{0} + a_{1}x + a_{2}y + …;   RMSE = √[Σ (Δx² + Δy²) / n]'],
  how=['Collect GCPs (GNSS-surveyed targets); fit the transformation; accept RMSE below one pixel.', '**Nearest neighbour** keeps original values (use for classification and indices); **bilinear** and **cubic** convolution smooth values (better appearance).', 'Image-to-image co-registration aligns sensors with different pixel sizes.'],
  figs=[('resample', 'd_resample.png', 'Resampling methods: nearest neighbour keeps original values, bilinear and cubic smooth them.', 470)],
  use='Plot-level features from four sensors are valid only if all images are co-registered.',
  mine='GCPs on the field; thermal and hyperspectral co-registered to RGB/MS orthomosaics; crop mask transferred with nearest neighbour and one-pixel edge erosion.',
  qs=[('Why nearest neighbour for masks and classes?', 'It does not create new values; bilinear would create fractional class codes or mixed reflectances at edges.')])
T('UAV photogrammetry: structure from motion (SfM)',
  'Overlapping images are matched to reconstruct camera positions and a 3-D point cloud, from which a digital surface model (DSM) and an orthomosaic are produced (Westoby et al., 2012).',
  how=['Key points detected and matched between images (SIFT-type features; Lowe, 2004).', 'Bundle adjustment solves camera poses and lens distortion; GCPs fix scale and position.', 'Dense matching → DSM; DSM − terrain model = canopy height; orthomosaic by projecting images onto the DSM.'],
  figs=[('sfm', 'd_sfm.png', 'Structure-from-motion workflow for UAV imagery.', 450)],
  use='Canopy height and structure (staghead, lodging) and accurate mosaics for multi-sensor analysis.',
  mine='RGB-derived DSM for canopy height; orthomosaics for all sensors (Pix4D/Agisoft-type processing).',
  qs=[('Why 75–80% overlap?', 'Each ground point must appear in several images for reliable matching and 3-D reconstruction, especially over homogeneous crops.')])

# ================= PART B: ENHANCEMENT, FILTERING, TRANSFORMS =================
H1('B. Enhancement, filtering and transforms')
T('Contrast enhancement and colour composites',
  'Stretches the narrow range of DNs to the full display range. Linear stretch maps chosen percentiles to 0–255; histogram equalisation makes all grey levels equally frequent. Colour composites assign three bands to red, green and blue; the standard false-colour composite (NIR, red, green) shows vegetation in red.',
  how=['Linear 2–98% stretch: v = (DN − DN_{2%}) / (DN_{98%} − DN_{2%}).', 'Equalisation uses the cumulative histogram as the mapping function.', 'Enhancement is for display; analysis uses the original reflectance.'],
  figs=[('comp', 'd_composites.png', 'Simulated field: (a) raw true colour, (b) stretched true colour, (c) false colour, (d) NDVI. Diseased patches are hardly visible in true colour but clear in false colour and NDVI.', 540),
        ('hist', 'd_hist.png', 'Histogram of a band before and after linear stretching and equalisation.', 470)],
  mine='False-colour composites for visual checks of disease patches and the crop mask.',
  qs=[('Why do diseased patches show better in a false-colour composite?', 'NIR reflectance falls with tissue damage, so diseased patches appear less red than healthy canopy.')])
T('Spatial filtering: low-pass, high-pass and edge detection',
  'A filter moves a kernel (window) over the image and replaces each pixel by a weighted combination of its neighbours (convolution). Low-pass filters smooth noise; high-pass filters enhance edges.',
  eq=['g(x, y) = Σ_{i} Σ_{j} w(i, j) f(x + i, y + j)'],
  how=['Mean and Gaussian filters smooth; the median filter removes salt-and-pepper noise while keeping edges.', 'Sobel and Laplacian kernels compute gradients for edge detection.', 'SAR speckle is reduced with adaptive filters such as Lee (Lee, 1980).', 'Morphological operations (erosion, dilation, opening, closing) clean binary masks.'],
  figs=[('filt', 'd_filters.png', 'Effect of low-pass and edge filters on a noisy NIR band.', 540)],
  mine='Morphological erosion of the crop mask (removes mixed edge pixels); Savitzky–Golay is the spectral equivalent of smoothing.',
  qs=[('Median or mean filter for noisy thermal images?', 'Median: it removes outliers (hot pixels) without blurring edges as much as the mean.')])
T('Band ratios and vegetation indices',
  'Ratios and normalised differences of bands enhance vegetation properties and reduce illumination and topographic effects. NDVI contrasts NIR and red; red-edge indices (NDRE, CI_{rededge}) track chlorophyll; water indices use SWIR (NDWI, MSI, NDII).',
  eq=['NDVI = (R_{NIR} − R_{red}) / (R_{NIR} + R_{red});   NDRE = (R_{NIR} − R_{RE}) / (R_{NIR} + R_{RE})'],
  how=['Normalisation bounds the index between −1 and 1 and cancels multiplicative illumination effects.', 'Soil-adjusted indices (SAVI, OSAVI) reduce soil background; red-edge indices avoid NDVI saturation.'],
  use='Disease indices such as the healthy index and powdery-mildew index (Mahlein et al., 2013), leaf-rust indices (Ashourloo et al., 2014) and the Sentinel-2 yellow-rust index (Zheng et al., 2018).',
  mine='48 hyperspectral indices including 9 SWIR disease indices; the White Rust Index ND(750, 948) − 0.5 R696 from leaf data.',
  pros='Simple, physically interpretable, transferable.', cons='General indices are not disease-specific; NDVI saturates at high cover.',
  qs=[('Why does NDVI saturate?', 'Red reflectance approaches zero at high leaf area while NIR keeps rising slowly, so the ratio changes little.')])
T('Principal component analysis (PCA)',
  'An orthogonal linear transform that rotates correlated bands into uncorrelated components ordered by variance (Pearson, 1901). The first components contain most information; later ones contain noise.',
  eq=['Σ v_{k} = λ_{k} v_{k};   PC_{k} = v_{k}^{T} (x − μ);   variance explained = λ_{k} / Σ λ'],
  how=['Centre (and optionally standardise) the data; compute the covariance matrix; eigen-decompose; project.', 'Loadings show which wavelengths contribute to each component.'],
  figs=[('pcaimg', 'd_segment.png', 'Otsu threshold, k-means clustering and the first two principal components of the simulated scene (PC2 isolates the diseased patches).', 540),
        ('pca', 'd_pca.png', 'PCA of 2339 real leaf spectra: scree plot, loadings and scores coloured by grade.', 540)],
  use='Data reduction of hyperspectral cubes; Shukla et al. (2024) used PCA loadings to pick aphid-sensitive bands in mustard.',
  mine='Not used for band selection because PCA is unsupervised: PC1 follows overall brightness and structure, not disease (see grade overlap in the score plot); used only to describe the data.',
  pros='Removes redundancy, compresses data, reduces noise.', cons='Unsupervised; components are mixtures of bands and hard to interpret physically.',
  qs=[('PCA or band selection for disease?', 'Band selection with a target (scalogram, ReliefF) keeps physically meaningful wavelengths; PCA keeps variance, which may come from soil or illumination.')])
T('Minimum noise fraction (MNF) and tasselled cap',
  'MNF is a noise-adjusted PCA: it first whitens the noise and then orders components by signal-to-noise ratio, so noisy hyperspectral bands are separated (Green et al., 1988). The tasselled cap is a fixed linear transform into brightness, greenness and wetness (Kauth and Thomas, 1976).',
  use='MNF before endmember extraction in hyperspectral images; tasselled cap greenness and wetness for crop condition.',
  mine='Hyperspectral noise handled by bad-band removal and Savitzky–Golay; MNF is an option for image-level endmember extraction.',
  qs=[('How does MNF differ from PCA?', 'PCA orders by total variance; MNF orders by signal-to-noise ratio after noise whitening.')])
T('Image fusion and pansharpening',
  'Combines a high-resolution panchromatic band with lower-resolution multispectral bands (pansharpening), or combines images of different sensors or dates (spatio-temporal fusion).',
  eq=['Brovey: MS\'_{k} = MS_{k} / (Σ MS) × PAN'],
  how=['Component substitution: IHS, PCA, Gram–Schmidt; ratio methods: Brovey; multiresolution: wavelets.', 'Spatio-temporal fusion (STARFM) predicts fine-resolution images on dates with only coarse images (Gao et al., 2006).'],
  figs=[('pan', 'd_pansharp.png', 'Pansharpening of a 4× coarser multispectral image with a panchromatic band (Brovey).', 470)],
  use='Fusing Sentinel-2 with daily coarse data, or LISS-IV with Sentinel-2 red-edge bands, to fill temporal and spatial gaps.',
  mine='Feature-level fusion of four UAV sensors (Objective 2) rather than pixel-level fusion.',
  pros='Better spatial detail.', cons='Spectral distortion; fused values not always physically valid for indices.',
  qs=[('Which pansharpening keeps spectra best?', 'Methods that inject only spatial detail (Gram–Schmidt, wavelet-based) distort spectra less than Brovey or IHS.')])

# ================= PART C: HYPERSPECTRAL =================
H1('C. Hyperspectral image processing')
T('Spectral smoothing and derivatives',
  'Savitzky–Golay fits a local polynomial in a moving window to smooth spectra and compute derivatives from the same fit (Savitzky and Golay, 1964). First and second derivatives remove offsets and sharpen inflection points (Tsai and Philpot, 1998).',
  eq=['FD(λ_{i}) ≈ [R(λ_{i+1}) − R(λ_{i−1})] / (λ_{i+1} − λ_{i−1})'],
  use='Red-edge position and slope; derivative spectra for disease (Shukla et al., 2024; Baranowski et al., 2015).',
  mine='Window 11 nm, second order; red-edge first derivatives at 790–830 nm were the strongest white-rust features in leaf data (r up to 0.78 with PDI).',
  qs=[('Why do derivatives amplify noise?', 'Differencing subtracts nearly equal values, so random noise becomes relatively larger; smoothing before differentiation is required.')])
T('Continuum removal and absorption band depth',
  'A convex hull (continuum) is fitted over the spectrum; dividing by it normalises absorption features, whose depth, width and area relate to biochemistry (Clark and Roush, 1984; Kokaly and Clark, 1999).',
  eq=['R_{cr}(λ) = R(λ) / R_{continuum}(λ);   band depth = 1 − R_{cr}(λ_{centre})'],
  use='Band depth at 662–702 and 2155–2175 nm mapped wheat biotic stress from AVIRIS-NG (Nigam et al., 2019).',
  mine='Optional extra feature; the chlorophyll band depth near 670 nm would complement the red-edge features.',
  qs=[('What does a deeper 670 nm band mean?', 'More chlorophyll absorption; disease reduces the depth.')])
T('Spectral angle mapper (SAM)',
  'Measures the angle between a pixel spectrum and a reference spectrum treated as vectors; small angles mean similar shape. The angle is insensitive to brightness (illumination) differences (Kruse et al., 1993).',
  eq=['α = cos^{-1} [ Σ t_{i} r_{i} / (√Σ t_{i}² √Σ r_{i}²) ]'],
  figs=[('sam', 'd_kmeans_sam.png', 'k-means cluster centres of real leaf spectra (a) and the spectral angle concept (b).', 500)],
  mine='Crop mask: NDVI > 0.6 AND SAM < 0.3 rad to a crop reference.',
  qs=[('Why combine NDVI with SAM?', 'NDVI removes soil and shadow; SAM removes pixels with non-crop spectral shape (for example yellow flowers or weeds) that may still have high NDVI.')])
T('Endmember extraction and spectral unmixing',
  'Mixed pixels are modelled as combinations of pure spectra (endmembers). Linear unmixing estimates the fraction of each endmember with abundances summing to one (Keshava and Mustard, 2002).',
  eq=['r = Σ_{k} a_{k} e_{k} + n,   a_{k} ≥ 0,   Σ a_{k} = 1'],
  how=['Endmembers from pixel purity index (Boardman et al., 1995), N-FINDR (Winter, 1999) or vertex component analysis (Nascimento and Bioucas-Dias, 2005).', 'Fully constrained least squares gives abundances.'],
  use='Fraction of diseased canopy in coarse satellite pixels; soil and shadow removal.',
  mine='30 endmembers per plot; soil, shadow and flower endmembers removed; plot spectrum = mean of crop endmembers.',
  qs=[('Why not use the mean of all canopy pixels?', 'It still mixes soil and shadow at edges and gaps; crop endmembers are the purest crop spectra, important for coarse SWIR pixels.')])
T('Band selection versus feature extraction',
  'Band selection keeps a subset of original wavelengths (interpretable, transferable to sensors); feature extraction creates new variables (PCA, MNF, PLS components) that mix all bands.',
  how=['Filter methods: correlation scalogram, ReliefF, ANOVA, mutual information.', 'Wrapper methods: SFFS, recursive feature elimination; embedded: LASSO, random-forest importance.', 'Neighbouring bands are almost identical (my leaf data: median r = 0.9998 between 5 nm bands), so one band per correlated region is kept.'],
  mine='Correlation scalogram + ReliefF → one band per region → robust, regression and classification lists (Tier 2).',
  qs=[('What is the Hughes phenomenon?', 'With limited samples, accuracy decreases when too many features are used because parameters cannot be estimated reliably (Hughes, 1968).')])

# ================= PART D: TEXTURE, SEGMENTATION, CLASSIC CLASSIFICATION =================
H1('D. Texture, segmentation, classification and change detection')
T('Texture: grey-level co-occurrence matrix (GLCM)',
  'The GLCM counts how often pairs of grey levels occur at a given distance and direction; statistics of this matrix (contrast, homogeneity, entropy, energy, correlation, mean, variance, dissimilarity) describe texture (Haralick et al., 1973).',
  eq=['Contrast = Σ_{i,j} (i − j)² P(i, j);   Homogeneity = Σ_{i,j} P(i, j) / [1 + (i − j)²]'],
  how=['Quantise the image (for example 32 grey levels); choose window (3×3 to 9×9), distance (1 pixel) and average four directions.', 'Other texture measures: local binary patterns, Gabor filters, wavelets.'],
  figs=[('glcm', 'd_glcm.png', 'GLCM contrast and homogeneity highlight speckled (pustule-like) texture in the diseased patches.', 470)],
  use='Texture improved powdery-mildew and yellow-rust detection from UAV images (Guo et al., 2021; Feng et al., 2022).',
  mine='24 RGB, 40 MS and 8 thermal GLCM features; white pustules and staghead change local contrast.',
  qs=[('Why must grey levels be the same for all flights?', 'GLCM values depend on quantisation; different ranges would make textures incomparable between dates.')])
T('Thresholding and segmentation',
  'Segmentation divides an image into meaningful regions. Otsu\'s method chooses the threshold that maximises between-class variance (Otsu, 1979); region growing, watershed and superpixels (SLIC; Achanta et al., 2012) group neighbouring pixels.',
  eq=['t* = argmax_{t} ω_{0}(t) ω_{1}(t) [μ_{0}(t) − μ_{1}(t)]²'],
  use='Crop–soil separation, lesion segmentation in leaf images, plot extraction.',
  mine='NDVI threshold (0.6) with SAM for the crop mask; plot polygons from the field layout.',
  qs=[('When does Otsu fail?', 'When the histogram is not bimodal, for example sparse canopies or strong illumination gradients.')])
T('Object-based image analysis (OBIA)',
  'Instead of classifying pixels, the image is segmented into objects (fields, plots, patches) that are classified using spectral, shape, texture and context features (Blaschke, 2010).',
  use='Field-level crop mapping from very-high-resolution images; parcel-based crop maps such as those in Krishi-DSS.',
  mine='Plots are the analysis objects: all features are plot-level means of masked pixels.',
  qs=[('Advantage of OBIA over pixels?', 'Less salt-and-pepper noise and access to shape and context; pixel noise averages out within objects.')])
T('Unsupervised classification: k-means and ISODATA',
  'k-means assigns pixels to k clusters by minimising within-cluster distance to the cluster means (MacQueen, 1967); ISODATA also splits and merges clusters.',
  eq=['minimise Σ_{k} Σ_{x ∈ C_{k}} ‖x − μ_{k}‖²'],
  use='Exploration of field variability, soil/canopy separation, first stratification for sampling.',
  mine='Exploration of leaf spectra ([[F:sam]]); not used for final models because classes must follow ground truth.',
  qs=[('How do you choose k?', 'Elbow of the within-cluster variance curve, silhouette score, or prior knowledge of classes.')])
T('Classical supervised classifiers: minimum distance, parallelepiped, maximum likelihood',
  'Minimum distance assigns a pixel to the class with the nearest mean; parallelepiped uses class value ranges; maximum likelihood assumes Gaussian classes and assigns the class with highest probability using class means and covariances.',
  eq=['g_{k}(x) = −ln|Σ_{k}| − (x − μ_{k})^{T} Σ_{k}^{−1} (x − μ_{k}) + 2 ln P(k)'],
  use='Standard in early crop mapping with IRS LISS data; still a baseline.',
  pros='Simple, statistically based.', cons='Gaussian assumption; needs many samples per class for covariance; fails with hundreds of bands (Hughes effect).',
  qs=[('Why does maximum likelihood fail on hyperspectral data?', 'Each class covariance matrix has about n²/2 parameters; with 300 bands this needs far more samples than available, so the matrix is singular.')])
T('Accuracy assessment of maps',
  'Accuracy is measured with a confusion matrix built from independent reference samples: overall accuracy, producer\'s accuracy (omission error), user\'s accuracy (commission error) and kappa (Cohen, 1960; Congalton, 1991). Area estimates should follow good-practice sampling (Olofsson et al., 2014).',
  eq=['OA = Σ n_{ii} / N;   PA_{i} = n_{ii} / n_{+i};   UA_{i} = n_{ii} / n_{i+};   κ = (p_{o} − p_{e}) / (1 − p_{e})'],
  how=['Stratified random sampling of reference points; reference data independent of training.', 'Kappa is criticised as redundant with OA (Pontius and Millones, 2011); report per-class accuracies.'],
  mine='Confusion matrix, OA, kappa, per-grade F1, macro-F1 and ±1-grade accuracy on held-out replications.',
  qs=[('Producer\'s vs user\'s accuracy?', 'Producer\'s: of the true diseased plots, how many were mapped as diseased; user\'s: of the plots mapped as diseased, how many really are.')])
T('Change detection and time-series analysis',
  'Detects change between dates by image differencing, ratioing, change vector analysis or post-classification comparison (Singh, 1989); time-series methods compare a season\'s profile with a normal profile or fit phenological curves.',
  use='Yellow-rust forewarning from NDVI deviation from a normal growth profile (Dutta et al., 2014).',
  mine='Eight flight dates; pre-symptomatic analysis compares later-infected with control plots on each date (Objective 3).',
  qs=[('Why compare with a normal profile instead of the previous date?', 'Crops change naturally with phenology; only deviation from the expected profile indicates stress.')])
T('SAR image processing basics',
  'Synthetic aperture radar measures backscatter (σ°) at microwave wavelengths, independent of clouds and sunlight. Processing: calibration to σ° (dB), speckle filtering, terrain correction; polarisations (VV, VH, HH, HV) respond to structure and moisture; interferometric coherence measures change.',
  use='All-weather crop mapping and crop growth monitoring (Sentinel-1, EOS-04/RISAT-1A, NISAR).',
  mine='Proposed for the mustard crop mask in the satellite pathway, not for leaf-level disease.',
  qs=[('Why is VH useful for crops?', 'Cross-polarised backscatter comes mainly from volume scattering in the canopy, so it grows with biomass.')])

# ================= PART E: ML FUNDAMENTALS =================
H1('E. Machine-learning fundamentals')
FIG('mlflow', 'd_mlflow.png', 'Machine-learning workflow without information leakage.', 450)
T('Types of learning and the data split',
  'Supervised learning learns a mapping from features to labels (classification for classes, regression for continuous values); unsupervised learning finds structure without labels (clustering, PCA); semi-supervised and self-supervised learning use unlabelled data.',
  how=['Training data fit the model, validation data tune hyperparameters, test data estimate final performance once.', 'Features must be scaled for distance- and gradient-based models (k-NN, SVM, neural networks).'],
  mine='Classification of six grades and regression of PDI; training, inner validation and outer test by replication.',
  qs=[('Classification or regression for severity?', 'Both: grades are ordinal classes; PDI is continuous and avoids class-boundary errors.')])
T('Bias–variance trade-off, overfitting and regularisation',
  'Error = bias² + variance + noise. Simple models underfit (high bias); complex models overfit (high variance), fitting noise in the training data. Regularisation penalises complexity: ridge (L2; Hoerl and Kennard, 1970), LASSO (L1; Tibshirani, 1996), dropout and early stopping in neural networks.',
  eq=['E[(y − ŷ)²] = Bias² + Variance + σ²;   ridge: min Σ (y − Xβ)² + λ Σ β²'],
  figs=[('bv', 'd_biasvar.png', 'Underfitting, good fit and overfitting; training error keeps falling while test error rises.', 540),
        ('lc', 'd_learning.png', 'Learning curve on real leaf data (random forest).', 360)],
  mine='Few hundred plot-dates per fold → compact feature sets (ML-SFFS), small DNNs, nested validation.',
  qs=[('How do you detect overfitting?', 'A large gap between training and validation scores, and validation scores that worsen as complexity increases.')])
T('Cross-validation and information leakage',
  'k-fold cross-validation estimates performance by rotating test folds (Kohavi, 1995). For spatial or grouped data, folds must keep groups (plots, fields, replications) together, otherwise neighbouring samples leak information (Roberts et al., 2017). Nested CV keeps feature selection and tuning inside the training folds (Varma and Simon, 2006).',
  figs=[('cv', 'd_cv.png', 'Random, grouped and leave-one-replication-out cross-validation.', 470)],
  mine='Leave-one-replication-out; every selection and tuning step repeated inside training replications; leaves of one plot never split.',
  qs=[('What is information leakage?', 'Any use of test-set information before testing (scaling, selection, tuning, or correlated neighbours in both sets), which inflates accuracy.')])
T('Class imbalance',
  'When classes have very different sizes, models favour the majority class. Remedies: class weights, resampling (undersampling, SMOTE oversampling; Chawla et al., 2002), balanced metrics (balanced accuracy, macro-F1).',
  mine='Class weights in all classifiers; macro-F1 and balanced accuracy (grade 9: 132 leaves vs grade 0: 560).',
  qs=[('Why not only overall accuracy?', 'A model predicting only the majority class can look accurate; in my leaf data 76% of leaves were diseased, so "all diseased" gives 0.76 accuracy but zero skill.')])
T('Feature selection methods',
  'Filter methods rank features independently of a model (correlation, ANOVA F, mutual information, ReliefF; Robnik-Šikonja and Kononenko, 2003); wrapper methods search subsets with a model (SFFS; Pudil et al., 1994; recursive feature elimination; Guyon et al., 2002); embedded methods select during training (LASSO, tree importance); Boruta selects all relevant features against shadow features (Kursa and Rudnicki, 2010); VIF removes collinearity (Dormann et al., 2013).',
  eq=['VIF_{j} = 1 / (1 − R_{j}²)'],
  mine='Scalogram + ReliefF (Tier 2) → Boruta (Tier 6) → VIF < 10 → ML-SFFS (Objective 2), repeated in each training fold.',
  qs=[('Filter vs wrapper?', 'Filters are fast and model-independent but ignore interactions; wrappers optimise for a specific model but are slower and can overfit.')])

# ================= PART F: ALGORITHMS =================
H1('F. Machine-learning algorithms')
FIG('bound', 'd_boundaries.png', 'Decision boundaries of six classifiers on two real leaf features (healthy vs diseased).', 540)
T('Linear and logistic regression',
  'Linear regression fits y = β₀ + Σ βᵢxᵢ by least squares; logistic regression models the log-odds of a class as a linear function and outputs probabilities.',
  eq=['β̂ = (XᵀX)^{−1} Xᵀy;   P(y = 1 | x) = 1 / (1 + e^{−(β₀ + βᵀx)})'],
  use='Index–severity regressions; weather-based disease risk models.', mine='Baseline relations of indices with PDI (Pearson r in Tier 4).',
  pros='Simple, fast, interpretable coefficients and probabilities.', cons='Linear; collinear predictors make coefficients unstable.',
  qs=[('Why not use multiple linear regression on all bands?', 'Bands are collinear and more numerous than samples; the solution is unstable (use PLSR, ridge or selection).')])
T('Linear and canonical discriminant analysis (LDA, CDA)',
  'Fisher\'s discriminant finds projections that maximise between-class relative to within-class variance (Fisher, 1936); CDA reports the canonical functions, correlations and Wilks\' lambda; LDA uses them to classify.',
  eq=['maximise J(w) = wᵀ S_{B} w / wᵀ S_{W} w;   Wilks Λ = |S_{W}| / |S_{T}|'],
  mine='Two-step stepwise CDA (Bhattacharya and Chattopadhyay, 2013): one dominant severity axis in leaf data (canonical r ≈ 0.66).',
  pros='Interpretable, few parameters.', cons='Assumes equal covariances and linear boundaries.',
  qs=[('CDA vs LDA?', 'Same Fisher method: CDA describes separation (functions, weights), LDA classifies with them.')])
T('k-nearest neighbours (k-NN)',
  'A sample is assigned the majority class (or mean value) of its k nearest training samples (Cover and Hart, 1967).',
  how=['Scale features; choose k by cross-validation; distance-weighted voting optional.'],
  use='Best regression model for wheat Fusarium head blight in Mustafa et al. (2023).', mine='Best PDI regressor in leaf data (R² 0.74 with four features).',
  pros='No training, non-linear, simple.', cons='Sensitive to scaling and irrelevant features; slow for large data.',
  qs=[('Small or large k?', 'Small k: flexible, high variance; large k: smooth, high bias; choose by validation.')])
T('Decision trees (CART)',
  'Recursive binary splits of the feature space; each split chooses the feature and threshold that most reduce impurity (Gini or entropy for classes, variance for regression; Breiman et al., 1984; Quinlan, 1986).',
  eq=['Gini = 1 − Σ_{k} p_{k}²;   Entropy = − Σ_{k} p_{k} log₂ p_{k}'],
  figs=[('tree', 'd_tree.png', 'Decision tree on real leaf features (WRI, Dr, PSRI, DWSI-5).', 540)],
  pros='Interpretable rules, handles non-linearity.', cons='Unstable; overfits without pruning.',
  qs=[('Why prune trees?', 'Deep trees fit noise; pruning or a maximum depth controls variance.')])
T('Random forest (RF)',
  'An ensemble of decision trees, each grown on a bootstrap sample with a random subset of features at each split; predictions are averaged or voted (Breiman, 2001). Out-of-bag samples give an internal error estimate and feature importance.',
  how=['Hyperparameters: number of trees, mtry (features per split), minimum leaf size.', 'Importance: mean decrease in impurity or permutation importance.'],
  use='Widely used in remote sensing classification (Belgiu and Drăguţ, 2016); RFR best for wheat powdery mildew (Feng et al., 2022).',
  mine='Best six-grade leaf classifier (macro-F1 0.32; healthy vs diseased accuracy 0.78); base of Boruta.',
  pros='Robust, few tuning parameters, non-linear, importance.', cons='Less interpretable than one tree; extrapolates poorly in regression.',
  qs=[('Why does randomness help?', 'Decorrelated trees make the ensemble average reduce variance.')])
T('Gradient boosting and XGBoost',
  'Trees are added sequentially, each fitting the residual errors (gradient of the loss) of the current ensemble (Friedman, 2001); XGBoost adds regularisation and efficient computation (Chen and Guestrin, 2016).',
  pros='Often the most accurate on tabular data.', cons='More hyperparameters (learning rate, depth, number of trees); overfits small datasets.',
  qs=[('Bagging vs boosting?', 'Bagging (RF) trains trees independently to reduce variance; boosting trains them sequentially to reduce bias.')])
T('Support vector machine and regression (SVM, SVR)',
  'SVM finds the hyperplane with maximum margin between classes; misclassifications are penalised by C; kernels (RBF, polynomial) map data to higher dimensions for non-linear boundaries (Cortes and Vapnik, 1995). SVR fits a function within an ε-insensitive tube.',
  eq=['min ½‖w‖² + C Σ ξ_{i}   s.t.  y_{i}(wᵀx_{i} + b) ≥ 1 − ξ_{i};   RBF: K(x, x\') = exp(−γ‖x − x\'‖²)'],
  use='Effective with small samples and many features (Mountrakis et al., 2011); early disease detection in sugar beet (Rumpf et al., 2010); rice blast (Tian et al., 2021).',
  mine='SVM/SVR in Objective 2 with class weights; C and γ tuned in inner CV.',
  pros='Good with small, high-dimensional data.', cons='Needs scaling and tuning; no direct probabilities; slow for large data.',
  qs=[('What do C and γ do?', 'C trades margin width against training errors; γ sets the reach of each training point (large γ = wiggly boundary).')])
T('Partial least squares regression (PLSR)',
  'Projects predictors and response onto a few latent components that maximise covariance between X and y; handles collinear and numerous predictors (Wold et al., 2001).',
  how=['Choose the number of components by cross-validated RMSE; inspect loadings and VIP scores.'],
  figs=[('plsr', 'd_plsr.png', 'PLSR on real plot-mean spectra: choosing components and observed vs predicted PDI.', 470)],
  use='Standard chemometric model for spectra (Shukla et al., 2024; Guo et al., 2021).', mine='Regression model and full-spectrum baseline.',
  qs=[('PLSR vs PCA regression?', 'PCA components ignore y; PLS components are chosen to predict y, so fewer are needed.')])
T('Gaussian process regression',
  'A Bayesian non-parametric regression that defines a distribution over functions through a kernel; it gives predictions with uncertainty (Rasmussen and Williams, 2006).',
  use='Retrieval of biophysical variables with uncertainty from hyperspectral data.', pros='Uncertainty for every prediction; works with small samples.', cons='Scales poorly with sample size; kernel choice.',
  qs=[('Main advantage?', 'Each prediction comes with a confidence interval.')])
T('Artificial neural networks (multilayer perceptron)',
  'Layers of neurons compute weighted sums followed by non-linear activations (ReLU, sigmoid, softmax). Weights are learned by back-propagation of the loss gradient (Rumelhart et al., 1986) with optimisers such as Adam (Kingma and Ba, 2015).',
  eq=['h = σ(Wx + b);   w ← w − η ∂L/∂w'],
  how=['Loss: cross-entropy (classes) or mean squared error (regression).', 'Regularisation: dropout (Srivastava et al., 2014), batch normalisation (Ioffe and Szegedy, 2015), weight decay, early stopping.'],
  figs=[('nn', 'd_nn.png', 'Multilayer perceptron and convolutional neural network.', 540)],
  mine='Small DNN-F1 (input fusion) and DNN-F2 (sensor sub-networks joined at an intermediate layer; Maimaitijiang et al., 2020).',
  pros='Learns non-linear interactions; flexible architectures for multi-sensor fusion.', cons='Needs much data; black box; many hyperparameters.',
  qs=[('Why ReLU?', 'It avoids vanishing gradients of sigmoid and is cheap to compute.'), ('What is an epoch?', 'One pass of all training samples through the network.')])
T('Convolutional neural networks (CNN) and semantic segmentation',
  'CNNs learn spatial filters by convolution, followed by pooling and dense layers (LeCun et al., 2015). Residual networks allow very deep models (He et al., 2016); U-Net performs pixel-wise segmentation with an encoder–decoder (Ronneberger et al., 2015). 1-D CNNs process spectra and 3-D CNNs process hyperspectral cubes.',
  use='Leaf-image disease classification (Mohanty et al., 2016); deep learning in agriculture and remote sensing (Kamilaris and Prenafeta-Boldú, 2018; Ma et al., 2019).',
  mine='Not used as the main model: a few hundred plot-dates are too few; CNNs are planned only if pixel-level labelled data become available.',
  pros='Learns features automatically; state of the art for images.', cons='Thousands of labelled samples; lab-to-field gap; interpretability.',
  qs=[('Why does a CNN need fewer parameters than a dense network on images?', 'Shared convolution weights are reused at every position (weight sharing) and connect only local neighbourhoods.')])
T('Recurrent networks, LSTM and transformers',
  'LSTM networks keep memory over sequences and suit time series of images or weather (Hochreiter and Schmidhuber, 1997); transformers use self-attention to weigh all positions of a sequence or image patches (Vaswani et al., 2017).',
  use='Crop-type mapping from satellite time series; disease forecasting from weather sequences.', mine='Possible for multi-date data in future; only 8 dates now.',
  qs=[('Why LSTM instead of a simple RNN?', 'Gates control memory and avoid vanishing gradients over long sequences.')])
T('Transfer learning and data augmentation',
  'Transfer learning reuses a model trained on a large dataset and fine-tunes it on a small one (Pan and Yang, 2010); augmentation (rotation, flipping, noise, brightness) enlarges training data.',
  mine='Relevant for future CNN work with UAV images of mustard.', qs=[('Risk of transfer learning?', 'Features learned from natural photographs may not suit multispectral or thermal images.')])
T('Unsupervised and anomaly-detection methods',
  'Clustering (k-means, hierarchical), dimensionality reduction (PCA, autoencoders) and anomaly detection (isolation forest, one-class SVM; Liu et al., 2008; Schölkopf et al., 2001) find unusual samples without labels.',
  use='Detecting unusual (possibly diseased) fields when labelled data are scarce.', mine='Alternative for pre-symptomatic detection trained on healthy plots only.',
  qs=[('Why anomaly detection for early disease?', 'Healthy data are plentiful; infected examples are rare and uncertain before symptoms.')])
T('Ensembles and fusion strategies',
  'Combining models (bagging, boosting, voting, stacking; Wolpert, 1992) or data sources improves robustness. Fusion levels: data/pixel level, feature level (concatenate features), intermediate (learned representations), decision level (combine predictions).',
  mine='Feature-level ML-SFFS fusion and DNN-F1/F2 fusion of HS, MS, RGB and thermal (Objective 2).',
  qs=[('Which fusion level do you use and why?', 'Feature level with selection, because it is interpretable and works with few samples; intermediate DNN fusion is tested against it.')])
T('Hyperparameter tuning',
  'Hyperparameters (C, γ, k, number of trees, learning rate) are chosen by grid search, random search (Bergstra and Bengio, 2012) or Bayesian optimisation (Snoek et al., 2012) on validation data inside the training folds.',
  mine='Grid search with grouped inner CV for SVM, RF, k-NN, PLSR.',
  qs=[('Why not tune on the test set?', 'The test score would then be optimistic; it must be used only once.')])

# ================= PART G: EVALUATION & INTERPRETATION =================
H1('G. Evaluation, interpretation and uncertainty')
T('Classification metrics',
  'From the confusion matrix: accuracy, precision, recall (sensitivity), specificity, F1, macro-F1, balanced accuracy, kappa, Matthews correlation coefficient (Chicco and Jurman, 2020); ROC curves plot sensitivity against 1 − specificity across thresholds and AUC summarises them (Fawcett, 2006).',
  eq=['Precision = TP / (TP + FP);  Recall = TP / (TP + FN);  F1 = 2PR / (P + R);  balanced accuracy = (sensitivity + specificity) / 2'],
  figs=[('eval', 'd_eval.png', 'Real leaf data, random forest healthy vs diseased: ROC curve, confusion matrix and permutation importance.', 540)],
  mine='OA, kappa, per-grade F1, macro-F1, ±1-grade accuracy, healthy-vs-diseased accuracy; AUC for pre-symptomatic models.',
  qs=[('Sensitivity or specificity for disease alerts?', 'High sensitivity finds most infected plots (fewer missed outbreaks); high specificity avoids unnecessary sprays; the threshold is set by the cost of each error.')])
T('Regression metrics',
  'R² (explained variance), RMSE, MAE, NRMSE (RMSE / mean), bias and RPD (SD / RMSE; Chang et al., 2001).',
  eq=['R² = 1 − Σ(y − ŷ)² / Σ(y − ȳ)²;   RMSE = √[Σ(y − ŷ)² / n];   RPD = SD_{y} / RMSE'],
  mine='Leaf data: best PDI model R² 0.74, RMSE 13.0, RPD 1.95.',
  qs=[('Can R² be negative?', 'Yes, on test data when predictions are worse than predicting the mean (my 11 February date had little PDI variation).')])
T('Statistical comparison of models',
  'Differences between classifiers should be tested, for example with McNemar\'s test on paired predictions or repeated cross-validation (Dietterich, 1998).',
  qs=[('Why test differences?', 'Small accuracy differences can arise from the particular split; a test shows whether they are systematic.')])
T('Model interpretation',
  'Global importance (tree importance, permutation importance), local explanations (SHAP values; Lundberg and Lee, 2017), partial dependence plots, and for CNNs class-activation maps such as Grad-CAM (Selvaraju et al., 2017).',
  mine='Permutation importance ([[F:eval]]): the WRI, HI and ARI dominate healthy-vs-diseased separation in leaf data.',
  qs=[('Why prefer permutation importance over impurity importance?', 'Impurity importance is biased towards features with many split points; permutation importance measures the loss in test accuracy.')])
T('Uncertainty of predictions',
  'Prediction intervals from quantile regression forests (Meinshausen, 2006), ensembles, Gaussian processes or bootstrapping; class probabilities from calibrated classifiers.',
  mine='Proposed uncertainty maps alongside severity maps.',
  qs=[('Why report uncertainty in disease maps?', 'Decision makers need to know where the map is reliable before targeting sprays.')])

# ================= PART H: SOFTWARE + RAPID QA =================
H1('H. Tools and rapid-fire questions')
TAB('tools', [['Task', 'Software / library'], ['Image processing, GIS', 'QGIS, ArcGIS, ENVI, ERDAS Imagine, SNAP (Sentinel), GDAL'],
              ['UAV photogrammetry', 'Pix4D, Agisoft Metashape, OpenDroneMap'], ['Cloud processing', 'Google Earth Engine, ISRO VEDAS and Bhuvan'],
              ['Machine learning', 'Python scikit-learn, XGBoost, R (caret, randomForest, Boruta)'], ['Deep learning', 'PyTorch, TensorFlow/Keras'],
              ['Spectral analysis', 'ViewSpec (ASD), Python (NumPy, SciPy), ENVI spectral tools']], [3000, 6306], 'Common software for the techniques in this guide.', 15)
RQ = [('What is the difference between radiance and reflectance?', 'Radiance is the measured energy per unit area, solid angle and wavelength; reflectance is the fraction of incoming light reflected, independent of illumination.'),
      ('What is BRDF?', 'The bidirectional reflectance distribution function describes how reflectance changes with sun and view angles; it causes brightness gradients in wide-angle UAV images.'),
      ('What is a DEM, DSM and DTM?', 'DEM: generic elevation model; DSM: top surface including vegetation; DTM: bare ground. Canopy height = DSM − DTM.'),
      ('What is the curse of dimensionality?', 'As features grow, data become sparse in feature space and distances lose meaning, so more samples are needed (Hughes, 1968).'),
      ('Why standardise features?', 'Distance-, margin- and gradient-based models are dominated by features with large numeric ranges otherwise.'),
      ('What is the difference between parametric and non-parametric classifiers?', 'Parametric models assume a distribution with fixed parameters (maximum likelihood, LDA); non-parametric models do not (k-NN, RF, SVM).'),
      ('What is a kernel trick?', 'Computing inner products in a high-dimensional feature space through a kernel function without explicitly mapping the data.'),
      ('Why use out-of-bag error in RF?', 'Each tree leaves out about one third of samples; predicting them gives an almost free internal validation estimate.'),
      ('What is early stopping?', 'Training stops when validation loss stops improving, preventing overfitting.'),
      ('What is spatial autocorrelation and why does it matter for validation?', 'Nearby pixels are similar; if neighbours are in training and test sets, accuracy is inflated (Roberts et al., 2017).'),
      ('What is the difference between a pixel-based and an object-based classification?', 'Pixel-based classifies each pixel independently; object-based classifies segments using spectral, shape and context features (Blaschke, 2010).'),
      ('What is SMOTE?', 'Synthetic minority oversampling creates new minority-class samples by interpolating between neighbours (Chawla et al., 2002).'),
      ('How would you explain AI to a farmer?', 'The computer learns from many examples how healthy and diseased crops look to the camera, and then recognises the disease in new fields.')]
for q, a in RQ: K.append("QA(%s, %s);" % (js(q), js(a)))

# ================= assemble =================
T_ = open(S + 'thesis/t_docx.js').read()
head = T_[:T_.index('// ======================= TITLE')]
head = re.sub(r"const B = '.*?';", "const B = '%s';" % B, head)
head = re.sub(r"const OUT = '.*?';", "const OUT = '%s';" % (S + 'outputs/DIP_ML_techniques_interview_guide.docx'), head)
head = re.sub(r"const FORDER = \[.*?\];", "const FORDER = __FORDER__;", head)
head = re.sub(r"const TORDER = \[.*?\];", "const TORDER = __TORDER__;", head)
head = head.replace('children: [new Paragraph({ children: runs(String(c)', 'children: [new Paragraph({ keepNext: true, children: runs(String(c)')
body = '\n'.join(K)
i = T_.index("K.push(H1('References'))"); pool = [r.replace("\\'", "'") for r in re.findall(r"^  '(.*)',$", T_[i:], re.M)]
refpat = re.compile(r'"([A-ZÀ-Ž][^"]{10,400}?\(\d{4}[a-z]?\)\.[^"]{10,500})"')
for f in (S + 'obj1/o1_assemble.py', S + 'leaf/l7_assemble.py', S + 'interview/i_build.py'): pool += refpat.findall(open(f).read())
pool += ["Toutin, T. (2004). Geometric processing of remote sensing images: models, algorithms and methods. International Journal of Remote Sensing 25(10), 1893–1924.",
 "Lowe, D.G. (2004). Distinctive image features from scale-invariant keypoints. International Journal of Computer Vision 60(2), 91–110.",
 "Westoby, M.J., Brasington, J., Glasser, N.F., Hambrey, M.J., Reynolds, J.M. (2012). 'Structure-from-Motion' photogrammetry: a low-cost, effective tool for geoscience applications. Geomorphology 179, 300–314.",
 "Otsu, N. (1979). A threshold selection method from gray-level histograms. IEEE Transactions on Systems, Man, and Cybernetics 9(1), 62–66.",
 "Green, A.A., Berman, M., Switzer, P., Craig, M.D. (1988). A transformation for ordering multispectral data in terms of image quality with implications for noise removal. IEEE Transactions on Geoscience and Remote Sensing 26(1), 65–74.",
 "Kauth, R.J., Thomas, G.S. (1976). The tasselled cap – a graphic description of the spectral-temporal development of agricultural crops as seen by Landsat. Proceedings of the Symposium on Machine Processing of Remotely Sensed Data, Purdue University, 41–51.",
 "Clark, R.N., Roush, T.L. (1984). Reflectance spectroscopy: quantitative analysis techniques for remote sensing applications. Journal of Geophysical Research 89(B7), 6329–6340.",
 "Boardman, J.W., Kruse, F.A., Green, R.O. (1995). Mapping target signatures via partial unmixing of AVIRIS data. Summaries of the Fifth JPL Airborne Earth Science Workshop 1, 23–26.",
 "Gao, F., Masek, J., Schwaller, M., Hall, F. (2006). On the blending of the Landsat and MODIS surface reflectance: predicting daily Landsat surface reflectance. IEEE Transactions on Geoscience and Remote Sensing 44(8), 2207–2218.",
 "Blaschke, T. (2010). Object based image analysis for remote sensing. ISPRS Journal of Photogrammetry and Remote Sensing 65(1), 2–16.",
 "Achanta, R., Shaji, A., Smith, K., Lucchi, A., Fua, P., Süsstrunk, S. (2012). SLIC superpixels compared to state-of-the-art superpixel methods. IEEE Transactions on Pattern Analysis and Machine Intelligence 34(11), 2274–2282.",
 "Lee, J.-S. (1980). Digital image enhancement and noise filtering by use of local statistics. IEEE Transactions on Pattern Analysis and Machine Intelligence 2(2), 165–168.",
 "Congalton, R.G. (1991). A review of assessing the accuracy of classifications of remotely sensed data. Remote Sensing of Environment 37(1), 35–46.",
 "Olofsson, P., Foody, G.M., Herold, M., Stehman, S.V., Woodcock, C.E., Wulder, M.A. (2014). Good practices for estimating area and assessing accuracy of land change. Remote Sensing of Environment 148, 42–57.",
 "Pontius, R.G., Millones, M. (2011). Death to Kappa: birth of quantity disagreement and allocation disagreement for accuracy assessment. International Journal of Remote Sensing 32(15), 4407–4429.",
 "Singh, A. (1989). Digital change detection techniques using remotely-sensed data. International Journal of Remote Sensing 10(6), 989–1003.",
 "Chavez, P.S. (1988). An improved dark-object subtraction technique for atmospheric scattering correction of multispectral data. Remote Sensing of Environment 24(3), 459–479.",
 "Vermote, E.F., Tanré, D., Deuzé, J.L., Herman, M., Morcrette, J.-J. (1997). Second simulation of the satellite signal in the solar spectrum, 6S: an overview. IEEE Transactions on Geoscience and Remote Sensing 35(3), 675–686.",
 "Jiménez-Muñoz, J.C., Sobrino, J.A. (2003). A generalized single-channel method for retrieving land surface temperature from remote sensing data. Journal of Geophysical Research 108(D22), 4688.",
 "Wan, Z., Dozier, J. (1996). A generalized split-window algorithm for retrieving land-surface temperature from space. IEEE Transactions on Geoscience and Remote Sensing 34(4), 892–905.",
 "Friedman, J.H. (2001). Greedy function approximation: a gradient boosting machine. Annals of Statistics 29(5), 1189–1232.",
 "Hoerl, A.E., Kennard, R.W. (1970). Ridge regression: biased estimation for nonorthogonal problems. Technometrics 12(1), 55–67.",
 "Quinlan, J.R. (1986). Induction of decision trees. Machine Learning 1, 81–106.",
 "LeCun, Y., Bengio, Y., Hinton, G. (2015). Deep learning. Nature 521, 436–444.",
 "He, K., Zhang, X., Ren, S., Sun, J. (2016). Deep residual learning for image recognition. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 770–778.",
 "Ronneberger, O., Fischer, P., Brox, T. (2015). U-Net: convolutional networks for biomedical image segmentation. Medical Image Computing and Computer-Assisted Intervention, Lecture Notes in Computer Science 9351, 234–241.",
 "Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kaiser, Ł., Polosukhin, I. (2017). Attention is all you need. Advances in Neural Information Processing Systems 30, 5998–6008.",
 "Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I., Salakhutdinov, R. (2014). Dropout: a simple way to prevent neural networks from overfitting. Journal of Machine Learning Research 15, 1929–1958.",
 "Ioffe, S., Szegedy, C. (2015). Batch normalization: accelerating deep network training by reducing internal covariate shift. Proceedings of the 32nd International Conference on Machine Learning, 448–456.",
 "Lundberg, S.M., Lee, S.-I. (2017). A unified approach to interpreting model predictions. Advances in Neural Information Processing Systems 30, 4765–4774.",
 "Selvaraju, R.R., Cogswell, M., Das, A., Vedantam, R., Parikh, D., Batra, D. (2017). Grad-CAM: visual explanations from deep networks via gradient-based localization. Proceedings of the IEEE International Conference on Computer Vision, 618–626.",
 "Schölkopf, B., Platt, J.C., Shawe-Taylor, J., Smola, A.J., Williamson, R.C. (2001). Estimating the support of a high-dimensional distribution. Neural Computation 13(7), 1443–1471.",
 "Bergstra, J., Bengio, Y. (2012). Random search for hyper-parameter optimization. Journal of Machine Learning Research 13, 281–305.",
 "Snoek, J., Larochelle, H., Adams, R.P. (2012). Practical Bayesian optimization of machine learning algorithms. Advances in Neural Information Processing Systems 25, 2951–2959.",
 "MacQueen, J. (1967). Some methods for classification and analysis of multivariate observations. Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability 1, 281–297.",
 "Pearson, K. (1901). On lines and planes of closest fit to systems of points in space. Philosophical Magazine 2(11), 559–572.",
 "Chawla, N.V., Bowyer, K.W., Hall, L.O., Kegelmeyer, W.P. (2002). SMOTE: synthetic minority over-sampling technique. Journal of Artificial Intelligence Research 16, 321–357.",
 "Ma, L., Liu, Y., Zhang, X., Ye, Y., Yin, G., Johnson, B.A. (2019). Deep learning in remote sensing applications: a meta-analysis and review. ISPRS Journal of Photogrammetry and Remote Sensing 152, 166–177.",
 "Belgiu, M., Drăguţ, L. (2016). Random forest in remote sensing: a review of applications and future directions. ISPRS Journal of Photogrammetry and Remote Sensing 114, 24–31.",
 "Mountrakis, G., Im, J., Ogole, C. (2011). Support vector machines in remote sensing: a review. ISPRS Journal of Photogrammetry and Remote Sensing 66(3), 247–259.",
 "Kamilaris, A., Prenafeta-Boldú, F.X. (2018). Deep learning in agriculture: a survey. Computers and Electronics in Agriculture 147, 70–90.",
 "Pan, S.J., Yang, Q. (2010). A survey on transfer learning. IEEE Transactions on Knowledge and Data Engineering 22(10), 1345–1359.",
 "Kohavi, R. (1995). A study of cross-validation and bootstrap for accuracy estimation and model selection. Proceedings of the 14th International Joint Conference on Artificial Intelligence, 1137–1145."]
pat = re.compile(r"([A-ZÀ-Ž][A-Za-zÀ-ÿŠšĂ-ž\-]+)(?: et al\.| and [A-ZÀ-Ž][A-Za-zÀ-ÿŠšĂ-ž\-]+)?,? \(?(\d{4})[a-z]?")
cites = set((m.group(1), m.group(2)) for m in pat.finditer(body))
def rk(r):
    a = r.split(',')[0].strip(); y = re.search(r'\((\d{4})[a-z]?\)', r); return (a, y.group(1) if y else '')
used, seen = [], set()
for r in sorted(set(pool), key=lambda r: (r.split('(')[0].lower(), r)):
    key = (r.split(',')[0], rk(r)[1])
    if rk(r) in cites and key not in seen: seen.add(key); used.append(r)
have = set(rk(r) for r in used)
fp_first = {x for r in used for x in []}
missing = sorted(x for x in cites if x not in have and 1900 < int(x[1]) < 2027)
print('possibly missing (second authors are expected here):', missing)
q = lambda s: "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"
body += "\nK.push(H1('References'));\nconst refPara = r => new Paragraph({ spacing: { after: 70, line: 255 }, indent: { left: 400, hanging: 400 }, children: [new TextRun({ text: r, font: FONT, size: 18 })] });\n[\n" + '\n'.join('  ' + q(r) + ',' for r in used) + "\n].forEach(r => K.push(refPara(r)));\n"
FO = [m.group(2) for m in re.finditer(r"\b(fig2|FIG)\('([A-Za-z0-9]+)'", body)]
TO = [m.group(2) for m in re.finditer(r"\b(tab2|TAB)\('([A-Za-z0-9]+)'", body)]
assert len(FO) == len(set(FO)) and len(TO) == len(set(TO)), (FO, TO)
head = head.replace('__FORDER__', repr(FO)).replace('__TORDER__', repr(TO))
tail = T_[T_.index('\nconst numcfg'):]
tail = tail.replace("title: 'AI-based multimodal UAV sensing of white rust in mustard: complete methodology'", "title: 'Digital image processing and machine learning: interview guide'")
tail = re.sub(r"'eqs', \d+, 'refs', \d+", "'eqs', 0, 'refs', %d" % len(used), tail)
open(B + 'd_build.js', 'w').write(head + '\n' + body + '\n' + tail)
print('techniques', TN[0], 'figs', len(FO), 'tabs', len(TO), 'refs', len(used))
