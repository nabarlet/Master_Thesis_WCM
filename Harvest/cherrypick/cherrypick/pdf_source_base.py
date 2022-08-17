import os, sys
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import common.wikid.wikidata as wd
import common.objects as obj
from common.utilities.pdf_file import PDFFile
from cherrypick.base import Base

class PdfSourceBase(Base):

    def __init__(self, file):
        super().__init__()
        self.filename = file
        self.pdf = PDFFile(file)

    def extract_text(self):
        text = []
        line_split = re.compile('\n+')
        for t in self.pdf.readpage():
            lines = line_split.split(t)
            lines = [l + '\n' for l in lines]
            text.extend(lines)
        yield text
