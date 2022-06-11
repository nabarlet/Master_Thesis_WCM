import pdfplumber as pp

class PDFFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.pdf = self.load_file()

    def load_file(self):
        res = pp.open(self.filepath)
        return res

    def readpage(self):
        for page in self.pdf.pages:
            yield page.extract_text()
