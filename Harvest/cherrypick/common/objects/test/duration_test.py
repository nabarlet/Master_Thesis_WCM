#!/usr/bin/env python


""" Unit tests for the objects/duration.py file. """

import pdb
import unittest
import sys, os
sys.path.append(os.path.join(*(['..']*3)))

import datetime as dt

from common.objects.duration import Duration
from common.utilities.string import __UNK__

class TestDuration(unittest.TestCase):

  def test_create_with_unknown(self):
      raw_value = __UNK__
      dur = Duration.create(raw_value)
      self.assertTrue(type(dur) is Duration, type(dur))
      self.assertEqual(str(dur), __UNK__, str(dur))

  def test_create_with_default(self):
      values = { '13:14:15': dt.timedelta(hours=13, minutes=14, seconds=15),
                 '14:15': dt.timedelta(minutes=14, seconds=15),
                 '15': dt.timedelta(seconds=15), }
      for rv, v in values.items():
          dur = Duration.create(rv)
          self.assertTrue(type(dur) is Duration, rv)
          self.assertEqual(dt.timedelta(seconds=dur.to_seconds()), v, rv)
          self.assertEqual(str(dur), str(v), str(dur))

  def test_create_with_dot_parser(self):
      values = { '13.14.15': dt.timedelta(hours=13, minutes=14, seconds=15),
                 '14.15': dt.timedelta(minutes=14, seconds=15),
                 '15': dt.timedelta(seconds=15), }
      for rv, v in values.items():
          dur = Duration.create(rv, parser=Duration.dot_parser)
          self.assertTrue(type(dur) is Duration, rv)
          self.assertEqual(dt.timedelta(seconds=dur.to_seconds()), v, rv)
          self.assertEqual(str(dur), str(v), str(dur))


  def test_create_with_h_dot_parser(self):
      values = { '13h14.15': dt.timedelta(hours=13, minutes=14, seconds=15),
                 '14h15.2': dt.timedelta(hours=14, minutes=15, seconds=2),
                 '1h20.05': dt.timedelta(hours=1, minutes=20, seconds=5), }
      for rv, v in values.items():
          dur = Duration.create(rv, parser=Duration.h_dot_parser)
          self.assertTrue(type(dur) is Duration, rv)
          self.assertEqual(dt.timedelta(seconds=dur.to_seconds()), v, rv)
          self.assertEqual(str(dur), str(v), str(dur))

if __name__ == '__main__':
  unittest.main()
