import os, sys
import re
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cherrypick.base import Base

class CsvSourceBase(Base):

    def __init__(self, file, provider):
        super(CsvSourceBase, self).__init__(provider)
        self.filename = file

    @classmethod
    def manage(cls, repo_dir, pattern = '*.csv'):
        return super(CsvSourceBase, cls).manage(repo_dir, pattern)

    def extract_rows(self):
        with open(self.filename, 'r', newline='') as cvsfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                yield row
