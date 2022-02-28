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
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()

    res = [list(sub) for ele, sub in groupby(text, key=bool) if ele]
    return res[2]

#text = convert_pdf_to_txt("15102330140000.pdf").split("\n")
#text = convert_pdf_to_txt("/home/usama/Downloads/15022290150000.pdf").split("\n")
# file_path = download_pdf("https://slco.org/services/au/au-e-nov-service/api/nov/GetReport/15294030250000", "15294030250000")
# text = convert_pdf_to_txt(file_path).split("\n")
# res = [list(sub) for ele, sub in groupby(text, key=bool) if ele]
# print(res[2])
