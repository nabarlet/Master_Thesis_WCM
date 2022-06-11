#!/usr/bin/env python


""" Unit tests for the utilities/timeline.py file. """

import unittest
import sys, os
sys.path.append(os.path.join(*(['..']*3)))

from common.utilities.timeline import TimeLine, TimeNode
from common.objects.composer import Composer

class TestTimeLine(unittest.TestCase):

  def test_create_from_csv(self):
      tl = TimeLine.create_from_csv()
      self.assertTrue(tl)
      for k, value in tl.items():
        self.assertTrue(type(value) is TimeNode)
      self.assertTrue(len(tl.inspect()) > 0)

  def test_assign_movement(self):
      tl = TimeLine.create_from_csv()
      self.assertEqual(tl.assign_movement(Composer('Englbert Humperdinick', '1632-11-28T00:00:00Z', '1692-11-28T00:00:00Z')), 'Baroque')
      self.assertEqual(tl.assign_movement(Composer('Englbert Humperdinick', '1732-11-28T00:00:00Z', '1792-11-28T00:00:00Z')), 'Classical')
      self.assertEqual(tl.assign_movement(Composer('Englbert Humperdinick', '1732-11-28T00:00:00Z', '1792-11-28T00:00:00Z')), 'Classical')
      self.assertEqual(tl.assign_movement(Composer('Englbert Humperdinick', '1792-11-28T00:00:00Z', '1852-11-28T00:00:00Z')), 'Romantic')
      self.assertEqual(tl.assign_movement(Composer('Englbert Humperdinick', '1892-11-28T00:00:00Z', '1952-11-28T00:00:00Z')), 'Modernism')
      self.assertEqual(tl.assign_movement(Composer('Englbert Humperdinick', '1992-11-28T00:00:00Z')), 'Contemporary')
      self.assertEqual(tl.assign_movement(Composer('Englbert Humperdinick')), None)
      

class TestTimeNode(unittest.TestCase):

  def setUp(self):
      self.tl = TimeLine.create_from_csv()
      self.tn = self.tl['Classical']

  def test_properties(self):
      self.assertEqual(self.tn.start, 1750)
      self.assertEqual(self.tn.end, 1820)

  def test_period_overlap(self):
      self.assertAlmostEqual(self.tn.period_overlap(Composer('Englbert Humperdinick', '1632-11-28T00:00:00Z', '1692-11-28T00:00:00Z')), 0.0)
      self.assertAlmostEqual(self.tn.period_overlap(Composer('Englbert Humperdinick', '1732-11-28T00:00:00Z', '1792-11-28T00:00:00Z')), 0.7)
      self.assertAlmostEqual(self.tn.period_overlap(Composer('Englbert Humperdinick', '1792-11-28T00:00:00Z', '1852-11-28T00:00:00Z')), 0.4745762711)
      self.assertAlmostEqual(self.tn.period_overlap(Composer('Englbert Humperdinick', '1752-11-28T00:00:00Z', '1812-11-28T00:00:00Z')), 1.0)
      self.assertAlmostEqual(self.tn.period_overlap(Composer('Englbert Humperdinick', '1852-11-28T00:00:00Z', '1912-11-28T00:00:00Z')), 0.0)
      self.assertEqual(self.tn.period_overlap(Composer('Englbert Humperdinick')), None)

if __name__ == '__main__':
  unittest.main()
