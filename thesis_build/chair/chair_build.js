// Builds the explanatory document (Word) from content.json written by build_content.py.
// Markup inside text: **bold**, *italic*, _{sub}, ^{sup}. Block types: title, toc, h1, h2, h3, p, bl, nl, box, read, fig, tab, eq, pb, qa.
const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType, ImageRun,
  TableOfContents, PageBreak, LevelFormat, Footer, Header, PageNumber, BorderStyle, TabStopType } = require('docx');
const C = JSON.parse(fs.readFileSync(path.join(__dirname, 'content.json'), 'utf8'));
const FONT = 'Calibri', HEAD = 'Cambria', GREEN = '2C5F2D', DARK = '1E3A1F';
const TW = 9638;                       // text width in DXA (A4, 2 cm margins)

function runs(text, base = {}) {
  const out = []; let i = 0, buf = '', bold = false, ital = false;
  const mk = (t, extra = {}) => new TextRun({ text: t, font: base.font || FONT, size: base.size || 22, bold: bold || base.bold, italics: ital || base.italics, color: base.color, ...extra });
  const flush = () => { if (buf) { out.push(mk(buf)); buf = ''; } };
  while (i < text.length) {
    if (text.startsWith('**', i)) { flush(); bold = !bold; i += 2; continue; }
    if (text.startsWith('~~', i)) { flush(); ital = !ital; i += 2; continue; }
    if ((text.startsWith('_{', i) || text.startsWith('^{', i))) {
      flush(); const j = text.indexOf('}', i); const s = text.slice(i + 2, j);
      out.push(mk(s, { subScript: text[i] === '_', superScript: text[i] === '^' })); i = j + 1; continue;
    }
    buf += text[i]; i++;
  }
  flush(); return out;
}
const P = (t, o = {}) => new Paragraph({ spacing: { after: 120, line: 288 }, alignment: AlignmentType.JUSTIFIED, ...o, children: runs(t) });
const bd = (c = 'BBBBBB', s = 4) => ({ style: BorderStyle.SINGLE, size: s, color: c });
let figN = 0, tabN = 0;

function figure(b) {
  const file = path.join(C.figdir, b.file); const buf = fs.readFileSync(file);
  const dim = require('child_process').execSync(`python3 -c "from PIL import Image;im=Image.open('${file}');print(im.size[0],im.size[1])"`).toString().trim().split(' ').map(Number);
  figN += 1; const w = b.width || 620; let h = Math.round(w * dim[1] / dim[0]);
  const maxH = 800; let ww = w; if (h > maxH) { ww = Math.round(w * maxH / h); h = maxH; }
  return [new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 160, after: 60 }, children: [new ImageRun({ type: 'png', data: buf, transformation: { width: ww, height: h }, altText: { title: b.caption, description: b.caption, name: b.file } })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 }, children: [new TextRun({ text: `Figure ${figN}. `, bold: true, font: FONT, size: 19 }), ...runs(b.caption, { size: 19, italics: true })] })];
}
function table(b) {
  tabN += 1; const rows = b.rows; const n = rows[0].length;
  let widths = b.widths; if (!widths) { widths = Array(n).fill(Math.floor(TW / n)); }
  const tot = widths.reduce((a, c) => a + c, 0); widths = widths.map(x => Math.round(x * TW / tot)); widths[n - 1] += TW - widths.reduce((a, c) => a + c, 0);
  const size = b.size || 18;
  const keep = rows.length <= 14;
  const cell = (txt, j, head, shade, last) => new TableCell({ width: { size: widths[j], type: WidthType.DXA }, borders: { top: bd(), bottom: bd(), left: bd(), right: bd() },
    shading: head ? { type: ShadingType.CLEAR, color: 'auto', fill: GREEN } : (shade ? { type: ShadingType.CLEAR, color: 'auto', fill: 'F2F6F1' } : undefined),
    margins: { top: 40, bottom: 40, left: 80, right: 80 },
    children: [new Paragraph({ keepNext: keep && !last, children: runs(String(txt), { size, bold: head || (b.boldfirst && j === 0), color: head ? 'FFFFFF' : undefined }) })] });
  const trs = rows.map((r, i) => new TableRow({ tableHeader: i === 0, cantSplit: true, children: r.map((c, j) => cell(c, j, i === 0, i > 0 && i % 2 === 0, i === rows.length - 1)) }));
  return [new Paragraph({ spacing: { before: 180, after: 80 }, keepNext: true, children: [new TextRun({ text: `Table ${tabN}. `, bold: true, font: FONT, size: 19 }), ...runs(b.caption, { size: 19, italics: true })] }),
    new Table({ width: { size: TW, type: WidthType.DXA }, columnWidths: widths, rows: trs }), new Paragraph({ spacing: { after: 100 }, children: [] })];
}
const STY = {
  key: { fill: 'EEF3E8', line: GREEN }, note: { fill: 'F3F3F3', line: '888888' }, present: { fill: 'FFF6E0', line: 'C98A00' },
  caution: { fill: 'FDECEA', line: 'B23B2E' }, method: { fill: 'EAF1F8', line: '2F5D8A' },
};
function box(b) {
  const s = STY[b.kind || 'key'];
  const paras = (Array.isArray(b.text) ? b.text : [b.text]);
  return paras.map((t, i) => new Paragraph({ spacing: { before: i === 0 ? 120 : 0, after: i === paras.length - 1 ? 160 : 60, line: 276 }, shading: { type: ShadingType.CLEAR, color: 'auto', fill: s.fill },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: s.line, space: 6 } }, indent: { left: 220, right: 220 }, keepNext: i < paras.length - 1,
    children: [...(i === 0 && b.label ? [new TextRun({ text: b.label + '  ', bold: true, font: FONT, size: 21, color: s.line })] : []), ...runs(t, { size: 21 })] }));
}
const RCOL = { 'What it shows': '1565C0', 'How to read it': '6A1B9A', 'What we found': '2E7D32', 'What it means': 'AD1457', 'Say to the chairman': 'C98A00', 'Why it was done': '2F5D8A', 'How it was done': '2E7D32', 'Caution': 'B23B2E' };
function read(b) {
  const out = [];
  b.parts.forEach(([lab, txt]) => {
    const items = Array.isArray(txt) ? txt : [txt];
    out.push(new Paragraph({ spacing: { before: 80, after: 40, line: 276 }, keepNext: true, indent: { left: 120 },
      children: [new TextRun({ text: lab, bold: true, font: FONT, size: 21, color: RCOL[lab] || DARK })] }));
    items.forEach(t => out.push(new Paragraph({ spacing: { after: 60, line: 280 }, alignment: AlignmentType.JUSTIFIED, indent: { left: 360 },
      ...(items.length > 1 ? { numbering: { reference: 'bulr', level: 0 } } : {}), children: runs(t, { size: 21 }) })));
  });
  out.push(new Paragraph({ spacing: { after: 80 }, children: [] }));
  return out;
}
let LISTI = 0;
const K = [];
for (const b of C.blocks) {
  switch (b.t) {
    case 'title':
      K.push(new Paragraph({ spacing: { before: 2200, after: 300 }, alignment: AlignmentType.LEFT, children: [new TextRun({ text: b.title, font: HEAD, size: 52, bold: true, color: DARK })] }));
      K.push(new Paragraph({ spacing: { after: 500 }, children: [new TextRun({ text: b.subtitle, font: FONT, size: 30, color: GREEN })] }));
      (b.lines || []).forEach(l => K.push(new Paragraph({ spacing: { after: 100 }, children: runs(l, { size: 24 }) })));
      K.push(new Paragraph({ children: [new PageBreak()] })); break;
    case 'toc':
      K.push(new Paragraph({ spacing: { after: 200 }, children: [new TextRun({ text: 'Contents', font: HEAD, size: 34, bold: true, color: DARK })] }));
      K.push(new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-2' }));
      K.push(new Paragraph({ children: [new PageBreak()] })); break;
    case 'h1': K.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: b.newpage !== false, children: [new TextRun({ text: b.text, font: HEAD })] })); break;
    case 'h2': K.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: b.text, font: HEAD })] })); break;
    case 'h3': K.push(new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun({ text: b.text, font: FONT })] })); break;
    case 'p': K.push(P(b.text)); break;
    case 'bl': b.items.forEach(t => K.push(new Paragraph({ numbering: { reference: 'bul', level: 0 }, spacing: { after: 60, line: 280 }, alignment: AlignmentType.JUSTIFIED, children: runs(t) }))); break;
    case 'nl': LISTI += 1; b.items.forEach(t => K.push(new Paragraph({ numbering: { reference: 'num', level: 0, instance: LISTI }, spacing: { after: 60, line: 280 }, alignment: AlignmentType.JUSTIFIED, children: runs(t) }))); break;
    case 'box': K.push(...box(b)); break;
    case 'read': K.push(...read(b)); break;
    case 'fig': K.push(...figure(b)); break;
    case 'tab': K.push(...table(b)); break;
    case 'eq': K.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 80, after: 120 }, children: runs(b.text, { font: 'Cambria Math', size: 23 }) })); break;
    case 'pb': K.push(new Paragraph({ children: [new PageBreak()] })); break;
    case 'qa':
      K.push(new Paragraph({ spacing: { before: 140, after: 40 }, keepNext: true, children: [new TextRun({ text: 'Q. ', bold: true, font: FONT, size: 22, color: GREEN }), ...runs(b.q, { bold: true })] }));
      K.push(new Paragraph({ spacing: { after: 100, line: 280 }, alignment: AlignmentType.JUSTIFIED, indent: { left: 300 }, children: [new TextRun({ text: 'A. ', bold: true, font: FONT, size: 22, color: 'C98A00' }), ...runs(b.a)] })); break;
    default: throw new Error('unknown block ' + b.t);
  }
}
const hs = (size, color, before, after, font = HEAD) => ({ run: { font, size, bold: true, color }, paragraph: { spacing: { before, after }, keepNext: true, keepLines: true } });
const doc = new Document({
  creator: C.author, title: C.doctitle, description: C.doctitle,
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, ...hs(34, DARK, 240, 200), paragraph: { spacing: { before: 240, after: 200 }, keepNext: true, keepLines: true, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, ...hs(28, GREEN, 300, 140), paragraph: { spacing: { before: 300, after: 140 }, keepNext: true, keepLines: true, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, ...hs(23, DARK, 220, 100, FONT), paragraph: { spacing: { before: 220, after: 100 }, keepNext: true, keepLines: true, outlineLevel: 2 } },
    ],
  },
  numbering: { config: [
    { reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 260 } } } }] },
    { reference: 'bulr', levels: [{ level: 0, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 640, hanging: 260 } } } }] },
    { reference: 'num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 300 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: C.header, font: FONT, size: 16, color: '888888' })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18, color: '666666' })] })] }) },
    children: K,
  }],
});
Packer.toBuffer(doc).then(buf => { fs.writeFileSync(C.out, buf); console.log('written', C.out, 'figures', figN, 'tables', tabN); });
