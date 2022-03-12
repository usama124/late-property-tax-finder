from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from itertools import groupby
import requests

def download_pdf(url, parcel_id):
    response = requests.get(url)
    file_name = 'PDF_FILES/'+parcel_id+".pdf"
    with open(file_name, 'wb') as f:
        f.write(response.content)
    return file_name

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    text = text.split("\n")
    fp.close()
    device.close()
    retstr.close()
    res = [list(sub) for ele, sub in groupby(text, key=bool) if ele] #List iterator for splitting information line by line
    return res[2] #Picking up the required information
