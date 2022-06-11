#!/usr/bin/env python

import pdb
import unittest
import os, sys
import datetime as dt
import csv

sys.path.extend(['..', os.path.join('..', '..')])

from bbc3_downloader import BBC3Downloader
from bbc3_pick import BBC3Pick

class TestProcessDate(unittest.TestCase):

    def setUp(self):
        self.possible_dates = [
            'Sun Mar 27 17:41:49 +0000 2022',
            '1893-10-18T00:00:00Z',
            'Tue Mar 29 19:26:04 +0000 2022',
            'Thu May 12 08:23:44 +0000 2022',
            '2022-05-15T17:36:52+00:00',
        ]


    def test_process_date_simple(self):
        for d in self.possible_dates:
            dres = BBC3Downloader.process_date(d)
            self.assertTrue(dres, d)
            self.assertEqual(type(dres), dt.datetime, dres)

    def test_process_date_all_dates(self):
        tot_lineno = 0
        for coll in BBC3Pick.manage():
            with open(coll.filename, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                lineno = 0
                for row in reader:
                    if lineno < 2:
                        lineno += 1
                        continue
                    perf_date = row[-1]
                    dtdate = BBC3Downloader.process_date(perf_date)
                    self.assertTrue(dtdate,dtdate)
                    self.assertEqual(type(dtdate), dt.datetime, dtdate)
                    lineno += 1
                    tot_lineno += 1
        self.assertTrue(tot_lineno > 15000, lineno)

if __name__ == '__main__':
    unittest.main()
