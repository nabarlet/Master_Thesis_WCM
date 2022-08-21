#!/usr/bin/env python


""" Unit tests for the utilities/string.py file. """

import unittest
import sys, os
sys.path.extend(['..', os.path.join('..', '..')])

from single_day import SingleDay
import datetime as dt

class TestSingleDay(unittest.TestCase):

    def setUp(self):
        self.provider = 'BBC3'
        self.dates = ['2013-05-10', '2013-04-21', '2022-08-14', '2022-07-24', ]

    def test_create(self):
        for d in self.dates:
            date = dt.date.fromisoformat(d)
            sd = SingleDay(date, self.provider)
            self.assertTrue(type(sd) is SingleDay)

    def test_composer_name(self):
        for d in self.dates:
            flag = False
            date = dt.date.fromisoformat(d)
            sd = SingleDay(date, self.provider)
            self.assertTrue(type(sd) is SingleDay)
            for rec in sd.retrieve():
                if rec.composer.name == 'Domenico Scarlatti' or rec.composer.name == 'Niccolò Paganini' or rec.composer.name == 'Nikolai Rimsky-Korsakov':
                    flag = True
                # print(date.isoformat(), rec.to_csv(), flag)
            self.assertTrue(flag, date.isoformat())

if __name__ == '__main__':
  unittest.main()
