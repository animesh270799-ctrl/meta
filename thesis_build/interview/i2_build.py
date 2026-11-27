"""NRSC/SAC (ISRO) interview guide in question-answer form: builds the docx JS (thesis helpers + reference pool)."""
import re, json, os
B = os.path.dirname(os.path.abspath(__file__)) + '/'; S = B + '../'; LD = S + 'leaf/data/'
f2 = lambda v: '%.2f' % v
K = []; QN = [0]
def esc(t):
    t = t.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    return re.sub(r'\[\[(T|F):(\w+)\]\]', lambda m: '${%s(\'%s\')}' % (m.group(1), m.group(2)), t)
js = lambda s: '`' + esc(s) + '`'
def H1(t): K.append("K.push(H1(%s));" % js(t))
def P(t): K.append("K.push(P(%s));" % js(t))
def BL(items): K.extend("K.push(BL(%s));" % js(i) for i in items)
def NOTE(t): K.append("K.push(NOTE(%s));" % js(t))
def FIG(k, f, cap, w=520): K.append("K.push(...fig2('%s', '%s', %s, %d));" % (k, f, js(cap), w))
def TAB(k, rows, widths, cap, size=15):
    Rr = '[' + ',\n'.join('[' + ', '.join(js(str(c)) for c in r) + ']' for r in rows) + ']'
    K.append("K.push(...tab2('%s', %s, %s, %s, %d));" % (k, Rr, json.dumps(widths), js(cap), size))
def Q(q, short):
    QN[0] += 1
    K.append("K.push(H2(%s));" % js('Q%d. %s' % (QN[0], q)))
    K.append("K.push(BOX('Short answer:', %s, 'E8F5E9', '2E7D32'));" % js(short))
def TIP(t): K.append("K.push(BOX('How to say it in the interview:', %s, 'FFF6E0', 'C98A00'));" % js(t))

def Qd(q, a):
    QN[0] += 1
    K.append("K.push(H2(%s));" % js('Q%d. %s' % (QN[0], q)))
    P(a)
# ================= TITLE =================
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 800, after: 160 }, children: [new TextRun({ text: 'NRSC / SAC (ISRO) interview guide', font: FONT, size: 44, bold: true, color: '1E3A1F' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 }, children: [new TextRun({ text: 'AI-based multimodal UAV sensing of white rust in mustard — questions and answers (updated edition)', font: FONT, size: 28, color: '2C5F2D' })] }));")
K.append("K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 }, children: [new TextRun({ text: 'Agricultural Scientist interview preparation  |  Ph.D. (Agricultural Physics), ICAR-IARI', font: FONT, size: 20, italics: true, color: '555555' })] }));")
NOTE('**How to use this guide.** Each question has a **short answer** (say it first, 30–60 seconds) followed by a detailed scientific answer for follow-up questions. No experimental results are quoted; answers explain concepts, physiology, methods and reasoning, with a reference after every method. Answer pattern: problem → physical or physiological basis → method → why this method → limitation.')
K.append("K.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-2' }));")
K.append("K.push(new Paragraph({ children: [new PageBreak()] }));")
exec(open(B + 'i2_content.py').read())
exec(open(B + 'i2_content2.py').read())

# ================= assemble =================
T = open(S + 'thesis/t_docx.js').read()
head = T[:T.index('// ======================= TITLE')]
head = re.sub(r"const B = '.*?';", "const B = '%s';" % B, head)
head = re.sub(r"const OUT = '.*?';", "const OUT = '%s';" % (S + 'outputs/ISRO_interview_guide_white_rust_v2.docx'), head)
head = re.sub(r"const FORDER = \[.*?\];", "const FORDER = __FORDER__;", head)
head = re.sub(r"const TORDER = \[.*?\];", "const TORDER = __TORDER__;", head)
head = head.replace('children: [new Paragraph({ children: runs(String(c)', 'children: [new Paragraph({ keepNext: true, children: runs(String(c)')
body = '\n'.join(K)
i = T.index("K.push(H1('References'))"); pool = [r.replace("\\'", "'") for r in re.findall(r"^  '(.*)',$", T[i:], re.M)]
pool += re.findall(r'^ "(.*)",$', open(S + 'obj1/o1_assemble.py').read(), re.M)
pool += re.findall(r'^         "(.*)",$', open(S + 'leaf/l7_assemble.py').read(), re.M)
pool += ["Dutta, S., Bhattacharya, B.K., Dadhwal, V.K., et al. (2008). Modelling regional level spatial distribution of aphid (Lipaphis erysimi) growth in Indian mustard using satellite-based remote sensing data. International Journal of Pest Management 54(1), 51–62.",
         "Dutta, S., et al. (2014). A case study on forewarning of yellow rust affected areas on wheat crop using satellite data. Journal of the Indian Society of Remote Sensing 42(2), 335–342.",
         "Das, P.K., Laxman, B., Kameswara Rao, S.V.C., Seshasai, M.V.R., Dadhwal, V.K. (2015). Monitoring of bacterial leaf blight in rice using ground-based hyperspectral and LISS IV satellite data in Kurnool, Andhra Pradesh, India. International Journal of Pest Management 61(4), 359–368.",
         "Nigam, R., et al. (2019). Crop type discrimination and health assessment using hyperspectral imaging. Current Science 116(7), 1108.",
         "Chattopadhyay, C., et al. (2011). Epidemiology and development of forecasting models for white rust of Brassica juncea in India. Archives of Phytopathology and Plant Protection 44(8), 751–763.",
         "Parihar, J.S., Oza, M.P. (2006). FASAL: an integrated approach for crop assessment and production forecasting. Proceedings of SPIE 6411, Agriculture and Hydrology Applications of Remote Sensing, 641101.",
         "Sandholt, I., Rasmussen, K., Andersen, J. (2002). A simple interpretation of the surface temperature/vegetation index space for assessment of surface moisture status. Remote Sensing of Environment 79(2–3), 213–224.",
         "Idso, S.B., Jackson, R.D., Pinter, P.J., Reginato, R.J., Hatfield, J.L. (1981). Normalizing the stress-degree-day parameter for environmental variability. Agricultural Meteorology 24, 45–55.",
         "Jackson, R.D., Idso, S.B., Reginato, R.J., Pinter, P.J. (1981). Canopy temperature as a crop water stress indicator. Water Resources Research 17(4), 1133–1138.",
         "Calderón, R., Navas-Cortés, J.A., Lucena, C., Zarco-Tejada, P.J. (2013). High-resolution airborne hyperspectral and thermal imagery for early detection of Verticillium wilt of olive using fluorescence, temperature and narrow-band spectral indices. Remote Sensing of Environment 139, 231–245.",
         "Mohanty, S.P., Hughes, D.P., Salathé, M. (2016). Using deep learning for image-based plant disease detection. Frontiers in Plant Science 7, 1419.",
         "Mohammed, G.H., et al. (2019). Remote sensing of solar-induced chlorophyll fluorescence (SIF) in vegetation: 50 years of progress. Remote Sensing of Environment 231, 111177.",
         "Zarco-Tejada, P.J., Camino, C., Beck, P.S.A., et al. (2018). Previsual symptoms of Xylella fastidiosa infection revealed in spectral plant-trait alterations. Nature Plants 4, 432–439.",
         "Hueni, A., Bialek, A. (2017). Cause, effect, and correction of field spectroradiometer interchannel radiometric steps. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing 10(4), 1542–1551.",
         "Jones, H.G. (1999). Use of infrared thermometry for estimation of stomatal conductance as a possible aid to irrigation scheduling. Agricultural and Forest Meteorology 95(3), 139–149.",
         "Belgiu, M., Csillik, O. (2018). Sentinel-2 cropland mapping using pixel-based and object-based time-weighted dynamic time warping analysis. Remote Sensing of Environment 204, 509–523.",
         "Veloso, A., Mermoz, S., Bouvet, A., Le Toan, T., Planells, M., Dejoux, J.-F., Ceschia, E. (2017). Understanding the temporal behavior of crops using Sentinel-1 and Sentinel-2-like data for agricultural applications. Remote Sensing of Environment 199, 415–426.",
         "Inglada, J., Vincent, A., Arias, M., Marais-Sicre, C. (2016). Improved early crop type identification by joint use of high temporal resolution SAR and optical image time series. Remote Sensing 8(5), 362.",
         "Ashourloo, D., Shahrabi, H.S., Azadbakht, M., Aghighi, H., Nematollahi, H., Alimohammadi, A., Matkan, A.A. (2019). Automatic canola mapping using time series of Sentinel 2 images. ISPRS Journal of Photogrammetry and Remote Sensing 156, 63–76.",
         "Rao, P., Zhou, W., Bhattarai, N., Srivastava, A.K., Singh, B., Poonia, S., Lobell, D.B., Jain, M. (2021). Using Sentinel-1, Sentinel-2, and Planet imagery to map crop type of smallholder farms. Remote Sensing 13(10), 1870.",
         "d'Andrimont, R., Taymans, M., Lemoine, G., Ceglar, A., Yordanov, M., van der Velde, M. (2020). Detecting flowering phenology in oil seed rape parcels with Sentinel-1 and -2 time series. Remote Sensing of Environment 239, 111660.",
         "Price, J.C. (1977). Thermal inertia mapping: a new view of the Earth. Journal of Geophysical Research 82(18), 2582–2590.",
         "Chaerle, L., Van der Straeten, D. (2000). Imaging techniques and the early detection of plant stress. Trends in Plant Science 5(11), 495–501.",
         "Mahlein, A.-K., Kuska, M.T., Behmann, J., Polder, G., Walter, A. (2018). Hyperspectral sensors and imaging technologies in phytopathology: state of the art. Annual Review of Phytopathology 56, 535–558.",
         "Thomas, S., Kuska, M.T., Bohnenkamp, D., Brugger, A., Alisaac, E., Wahabzada, M., Behmann, J., Mahlein, A.-K. (2018). Benefits of hyperspectral imaging for plant disease detection and plant protection: a technical perspective. Journal of Plant Diseases and Protection 125, 5–20.",
         "Behmann, J., Mahlein, A.-K., Rumpf, T., Römer, C., Plümer, L. (2015). A review of advanced machine learning methods for the detection of biotic stress in precision crop protection. Precision Agriculture 16, 239–260.",
         "Vermote, E.F., Tanré, D., Deuzé, J.L., Herman, M., Morcrette, J.-J. (1997). Second simulation of the satellite signal in the solar spectrum, 6S: an overview. IEEE Transactions on Geoscience and Remote Sensing 35(3), 675–686.",
         "Blaschke, T. (2010). Object based image analysis for remote sensing. ISPRS Journal of Photogrammetry and Remote Sensing 65(1), 2–16.",
         "Belgiu, M., Drăguţ, L. (2016). Random forest in remote sensing: a review of applications and future directions. ISPRS Journal of Photogrammetry and Remote Sensing 114, 24–31.",
         "Congalton, R.G. (1991). A review of assessing the accuracy of classifications of remotely sensed data. Remote Sensing of Environment 37(1), 35–46.",
         "Olofsson, P., Foody, G.M., Herold, M., Stehman, S.V., Woodcock, C.E., Wulder, M.A. (2014). Good practices for estimating area and assessing accuracy of land change. Remote Sensing of Environment 148, 42–57.",
         "Zheng, Q., Huang, W., Cui, X., Shi, Y., Liu, L. (2018). New spectral index for detecting wheat yellow rust using Sentinel-2 multispectral imagery. Sensors 18(3), 868."]
pat = re.compile(r"([A-Z][A-Za-zÀ-ÿŠš\-]+)(?: et al\.| and [A-Z][A-Za-zÀ-ÿ\-]+)?,? \(?(\d{4})[a-z]?")
cites = set((m.group(1), m.group(2)) for m in pat.finditer(body))
def rk(r):
    a = r.split(',')[0].strip(); y = re.search(r'\((\d{4})[a-z]?\)', r); return (a, y.group(1) if y else '')
used, seen = [], set()
for r in sorted(pool, key=lambda r: (r.split('(')[0].lower(), r)):
    key = (r.split('(')[0], rk(r)[1])
    if rk(r) in cites and key not in seen and rk(r) not in {rk(u) for u in used if u.split(',')[0] == r.split(',')[0] and rk(u)[1] == rk(r)[1] and 'et al' in u}: seen.add(key); used.append(r)
for extra in ("d'Andrimont, R.", "Chaerle, L."):
    for r in pool:
        if r.startswith(extra) and r not in used: used.append(r)
used = sorted(used, key=lambda r: (r.split('(')[0].lower(), r))
have = set(rk(r) for r in used)
fp = {('Šikonja', '2003'), ('Kononenko', '2003'), ('Chattopadhyay', '2013'), ('Rudnicki', '2010'), ('Philpot', '1998'), ('Peñuelas', '1994'), ('McLachlan', '2002'), ('Simon', '2006'), ('Knapp', '2001'), ('Oza', '2006'), ('Clark', '1999'), ('Long', '2016'), ('Lapalme', '2009'), ('Dias', '2005'), ('Rapeseed', '2023')}
missing = sorted(x for x in cites if x not in have and 1900 < int(x[1]) < 2027 and x not in fp and x[0] not in {'Ministry', 'ICAR-IARI', 'Rules', 'August'})
print('missing refs:', missing)
q = lambda s: "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"
body += "\nK.push(H1('References'));\nconst refPara = r => new Paragraph({ spacing: { after: 70, line: 255 }, indent: { left: 400, hanging: 400 }, children: [new TextRun({ text: r, font: FONT, size: 18 })] });\n[\n" + '\n'.join('  ' + q(r) + ',' for r in used) + "\n].forEach(r => K.push(refPara(r)));\n"
FO = [m.group(2) for m in re.finditer(r"\b(fig2|FIG)\('([A-Za-z0-9]+)'", body)]
TO = [m.group(2) for m in re.finditer(r"\b(tab2|TAB)\('([A-Za-z0-9]+)'", body)]
assert len(FO) == len(set(FO)) and len(TO) == len(set(TO))
head = head.replace('__FORDER__', repr(FO)).replace('__TORDER__', repr(TO))
tail = T[T.index('\nconst numcfg'):]
tail = tail.replace("title: 'AI-based multimodal UAV sensing of white rust in mustard: complete methodology'", "title: 'NRSC/SAC interview guide (updated): white rust in mustard'")
tail = re.sub(r"'eqs', \d+, 'refs', \d+", "'eqs', 0, 'refs', %d" % len(used), tail)
open(B + 'i2_build.js', 'w').write(head + '\n' + body + '\n' + tail)
print('questions', QN[0], 'figs', len(FO), 'tabs', len(TO), 'refs', len(used))
