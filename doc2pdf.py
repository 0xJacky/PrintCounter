import os

from win32com import client


def doc2pdf(doc, pdf):
    try:
        print('[doc2pdf]', doc)
        word = client.DispatchEx("Word.Application")
        if os.path.exists(pdf):
            os.remove(pdf)
        doc = word.Documents.Open(doc, ReadOnly=1)
        doc.SaveAs(pdf, FileFormat=17)
        doc.Close()
        return pdf
    except Exception as e:
        print('[doc2pdf] convent error', e)
        return False
