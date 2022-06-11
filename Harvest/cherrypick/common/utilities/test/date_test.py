#!/usr/bin/env python


""" Unit tests for the utilities/date.py file. """

import unittest
import sys, os
import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import date as dt

class TestDateUtilities(unittest.TestCase):

    def test_spanish_date_conversion(self):
        revistas = [ "REVISTAABR19.pdf", "REVISTAAGO19.pdf", "REVISTADIC19.pdf", "REVISTAENE19.pdf", "REVISTAFEB19.pdf", "REVISTAJUL21.pdf", \
                  "REVISTAJUN21.pdf", "REVISTAMAR22.pdf", "REVISTAMAY19.pdf", "REVISTANOV19.pdf", "REVISTAOCT21.pdf", "REVISTASEP21.pdf", ]
        for r in revistas:
            d = dt.spanish_date_conditioner(r)
            self.assertTrue(d)
            self.assertTrue(type(datetime.date))

    def test_spanish_date_proper(self):
        revistas = { "REVISTAABR19.pdf": datetime.date(2019, 4, 1), "REVISTAJUL21.pdf": datetime.date(2021, 7, 1), }
        for r, v in revistas.items():
            d = dt.spanish_date_conditioner(r)
            self.assertTrue(d)
            self.assertEqual(d, v, d)

if __name__ == '__main__':
  unittest.main()
