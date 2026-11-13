import uno, sys, time, subprocess, os
from com.sun.star.beans import PropertyValue
def P(n, v): p = PropertyValue(); p.Name = n; p.Value = v; return p
src, dst = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
proc = subprocess.Popen(['soffice', '--headless', '--invisible', '--norestore', '--accept=socket,host=localhost,port=2002;urp;'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
ctx = None
for _ in range(60):
    try:
        local = uno.getComponentContext(); res = local.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver', local)
        ctx = res.resolve('uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext'); break
    except Exception: time.sleep(1)
desktop = ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', ctx)
doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(src), '_blank', 0, (P('Hidden', True),))
st = doc.getStyleFamilies().getByName('ParagraphStyles')
for n, lv in [('Heading 1', 1), ('Heading 2', 2), ('Heading 3', 3)]:
    if st.hasByName(n) and st.getByName(n).OutlineLevel == 0: st.getByName(n).OutlineLevel = lv
for _ in range(2):  # twice so page numbers settle after the TOC is filled in
    idx = doc.getDocumentIndexes()
    for i in range(idx.getCount()): idx.getByIndex(i).update()
    doc.getTextFields().refresh(); doc.refresh()
filt = uno.Any('[]com.sun.star.beans.PropertyValue', tuple([P('ExportBookmarks', True), P('ExportNotes', False), P('UseLosslessCompression', True), P('ReduceImageResolution', False), P('SelectPdfVersion', 1)]))
doc.storeToURL(uno.systemPathToFileUrl(dst), (P('FilterName', 'writer_pdf_Export'), P('FilterData', filt)))
# also save the docx with the filled-in contents page
doc.storeToURL(uno.systemPathToFileUrl(dst.replace('.pdf', '_withTOC.docx')), (P('FilterName', 'MS Word 2007 XML'),))
doc.close(True)
try: desktop.terminate()
except Exception: pass
proc.wait(timeout=30); print('saved', dst)
