"""Finalizador DOCX del preprint, versión 1.0.3 (11 de noviembre de 2026).

Usage (from the repository root):
  pandoc preprint.md -o /tmp/raw.docx --resource-path=.
  python3 build/preprint_docx_band.py /tmp/raw.docx Bourguet_2026_Webfare_familias_juridicas_preprint_v1-0-3.docx \
      "<status line>" "<title>" "<footer suffix>"

What it does: black headings, justified body; a legend box above the title with three
coloured tabs (PREPRINT red, ENVIADO amber, DATOS Y CÓDIGO ABIERTOS green) and the status line;
the same three tabs in the page header; a red page border on every page; a red footer line
with version, date and DOI and the page number; figures at 16 cm; author in properties.
White text on each tab passes WCAG AA (contrast 5.0-6.0).
"""
import sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

src, out, status, title = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
fsuffix = sys.argv[5] if len(sys.argv) > 5 else ''
RED, BG, AMBER, GREEN = 'B03A2E', 'FDF0EC', '9A6200', '1B7F5B'
TABS = (('PREPRINT', RED), ('ENVIADO', AMBER), ('DATOS Y CÓDIGO ABIERTOS', GREEN))
HTABS = (('PREPRINT', RED), ('ENVIADO · SIN EVALUACIÓN POR PARES', AMBER), ('DATOS Y CÓDIGO ABIERTOS', GREEN))
rgb = lambda h: RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

d = Document(src)
BYNAME = {st.name: st for st in d.styles}
for name in ['Title', 'Subtitle', 'Abstract Title', 'TOC Heading', 'Author', 'Date'] + [f'Heading {i}' for i in range(1, 10)]:
    st = BYNAME.get(name)
    if st is None:
        continue
    rpr = st.element.get_or_add_rPr()
    for c in rpr.findall(qn('w:color')):
        rpr.remove(c)
    st.font.color.rgb = RGBColor(0, 0, 0)
for name in ['Body Text', 'First Paragraph', 'Abstract', 'Bibliography', 'Block Text', 'Image Caption', 'Table Caption']:
    if name in BYNAME:
        BYNAME[name].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), fill)
    tcPr.append(shd)


def margins(cell, tb=60, lr=120):
    tcPr = cell._tc.get_or_add_tcPr(); m = OxmlElement('w:tcMar')
    for k, v in (('top', tb), ('bottom', tb), ('left', lr), ('right', lr)):
        e = OxmlElement(f'w:{k}'); e.set(qn('w:w'), str(v)); e.set(qn('w:type'), 'dxa'); m.append(e)
    tcPr.append(m)


def borders(tbl, color, sz='8', inner='single'):
    tblPr = tbl._tbl.tblPr; b = OxmlElement('w:tblBorders')
    for e in ('top', 'left', 'bottom', 'right', 'insideV', 'insideH'):
        el = OxmlElement(f'w:{e}')
        val = inner if e.startswith('inside') else 'single'
        el.set(qn('w:val'), val); el.set(qn('w:sz'), sz if val != 'nil' else '0'); el.set(qn('w:space'), '0'); el.set(qn('w:color'), color)
        b.append(el)
    tblPr.append(b)
    lay = OxmlElement('w:tblLayout'); lay.set(qn('w:type'), 'fixed'); tblPr.append(lay)


def set_widths(tbl, widths):
    for gc, w in zip(tbl._tbl.tblGrid.findall(qn('w:gridCol')), widths):
        gc.set(qn('w:w'), str(int(w / 635)))
    for row in tbl.rows:
        for c, w in zip(row.cells, widths):
            c.width = w


def tab_cell(cell, text, fill, size=9):
    shade(cell, fill); margins(cell); cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0); p.paragraph_format.space_before = Pt(0)
    r = p.add_run(text); r.bold = True; r.font.size = Pt(size); r.font.color.rgb = RGBColor(255, 255, 255)


def shaded_run(par, text, fill, size):
    r = par.add_run('\u00a0' + text + '\u00a0'); r.bold = True; r.font.size = Pt(size); r.font.color.rgb = RGBColor(255, 255, 255)
    rPr = r._r.get_or_add_rPr(); shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), fill); rPr.append(shd)
    return r


def tabs_paragraph(par, tabs, size):
    for i, (t, f) in enumerate(tabs):
        if i:
            gap = par.add_run(' '); gap.font.size = Pt(size)
        shaded_run(par, t, f, size)


# --- legend box above the title: three coloured tabs, then the status line ---
tbl = d.add_table(rows=1, cols=1); tbl.alignment = WD_TABLE_ALIGNMENT.CENTER; tbl.autofit = False
borders(tbl, RED, sz='8', inner='nil')
lb = tbl._tbl.tblPr.find(qn('w:tblBorders')).find(qn('w:left')); lb.set(qn('w:sz'), '36')
set_widths(tbl, (Cm(16.5),))
cell = tbl.rows[0].cells[0]; shade(cell, BG); margins(cell, 100, 180)
p1 = cell.paragraphs[0]; p1.paragraph_format.space_after = Pt(4)
tabs_paragraph(p1, TABS, 9.5)
p2 = cell.add_paragraph(); p2.paragraph_format.space_after = Pt(0)
r = p2.add_run(status); r.bold = True; r.font.size = Pt(9.5); r.font.color.rgb = rgb(RED)
first = d.paragraphs[0]; first._p.addprevious(tbl._tbl)
gap = first.insert_paragraph_before(); gap.paragraph_format.space_after = Pt(6)


def footer_line(fp):
    fp.text = ''; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = fp.add_run('Versión 1.0.3 · 11 de noviembre de 2026' + fsuffix + ' · página '); r.font.size = Pt(8); r.font.color.rgb = rgb(RED)
    for kind, txt in (('begin', None), (None, 'PAGE'), ('end', None)):
        rr = fp.add_run(); rr.font.size = Pt(8); rr.font.color.rgb = rgb(RED)
        if kind:
            fc = OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'), kind); rr._r.append(fc)
        else:
            it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = txt; rr._r.append(it)


for sec in d.sections:
    # red page border on every page
    sectPr = sec._sectPr
    pb = OxmlElement('w:pgBorders'); pb.set(qn('w:offsetFrom'), 'page')
    for e in ('top', 'left', 'bottom', 'right'):
        el = OxmlElement(f'w:{e}'); el.set(qn('w:val'), 'single'); el.set(qn('w:sz'), '12'); el.set(qn('w:space'), '24'); el.set(qn('w:color'), RED)
        pb.append(el)
    pgMar = sectPr.find(qn('w:pgMar'))
    (pgMar.addnext(pb) if pgMar is not None else sectPr.append(pb))
    # first page carries the legend box, so its header stays empty
    sec.different_first_page_header_footer = True
    for p in list(sec.first_page_header.paragraphs):
        p.text = ''
    # later pages: the three tabs in the header
    hp = sec.header.paragraphs[0] if sec.header.paragraphs else sec.header.add_paragraph()
    hp.text = ''; hp.alignment = WD_ALIGN_PARAGRAPH.LEFT; hp.paragraph_format.space_after = Pt(10)
    tabs_paragraph(hp, HTABS, 7.5)
    # footers on all pages: version, date, DOI, page number
    footer_line(sec.footer.paragraphs[0] if sec.footer.paragraphs else sec.footer.add_paragraph())
    footer_line(sec.first_page_footer.paragraphs[0] if sec.first_page_footer.paragraphs else sec.first_page_footer.add_paragraph())

# Table 3 (pilot): pandoc splits short tables into equal columns; give the row labels room
for t in d.tables:
    try:
        head = t.cell(0, 0).text.strip()
    except IndexError:
        continue
    if head == 'Break type' and len(t.columns) == 5:
        tblPr = t._tbl.tblPr
        for old in tblPr.findall(qn('w:tblLayout')):
            tblPr.remove(old)
        lay = OxmlElement('w:tblLayout'); lay.set(qn('w:type'), 'fixed'); tblPr.append(lay)
        set_widths(t, (Cm(5.2), Cm(2.9), Cm(2.9), Cm(2.3), Cm(2.0)))

for shp in d.inline_shapes:
    r_ = shp.width / shp.height; shp.width = Cm(16); shp.height = int(Cm(16) / r_)
cp = d.core_properties; cp.author = 'Luis Felipe Bourguet González'; cp.title = title; cp.last_modified_by = 'Luis Felipe Bourguet González'; cp.language = 'es-ES'
d.save(out); print('saved', out)
