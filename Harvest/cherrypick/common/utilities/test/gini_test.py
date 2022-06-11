#!/usr/bin/env python


""" Unit tests for the utilities/gini.py file. """

import pdb
import unittest
import sys, os
import numpy as np
import time
sys.path.extend(['..', os.path.join('..', '..')])
import gini as g

HIFI = 6
LOFI = 1
EPS  = 1e-1

class TestGiniUtilities(unittest.TestCase):

  def setUp(self):
      uneven = np.zeros(500)
      uneven[10] = 500
      self.test_data = [
              (np.random.rand(500), 0.3),
              (10 + np.random.rand(500), 0.1),
              (100 + np.random.rand(500), 0.01),
              (uneven, 1.0),
#             (np.zeros(500), 0.0), # this cannot work with the current implementations
      ]
      self.implementations = [ (g.gini_coefficient, 0.002), (g.gini_porcaro, 0.0001), (g.fast_gini_coefficient, 0.004) ]
              
  def test_different_implementations(self):
      for td, should_be in self.test_data:
          vgc = g.gini_coefficient(td)
          vgp = g.gini_porcaro(td)
          vfg = g.fast_gini_coefficient(td)
          self.assertAlmostEqual(vgc, vgp, HIFI, "vgc: %f, vgp: %f" % (vgc, vgp))
          self.assertAlmostEqual(vgc, vfg, HIFI, "vgc: %f, vfg: %f" % (vgc, vfg))
          self.assertAlmostEqual(vgp, vfg, HIFI, "vgp: %f, vfg: %f" % (vgp, vfg))

  def test_gini_values(self):
      for td, should_be in self.test_data:
          for imp, tsb in self.implementations:
              result = imp(td)
              diff = np.abs(result - should_be)
              self.assertTrue(diff <= EPS, "implementation %s: %f != %f (diff: %f)" % (str(imp), result, should_be, diff))

  def test_gini_calculation_efficiency(self):
      for td, should_be in self.test_data:
          for imp, time_should_be in self.implementations:
              t0 = time.perf_counter()
              imp(td)
              t1 = time.perf_counter()
              elapsed = t1 - t0
              self.assertAlmostEqual(elapsed, time_should_be, LOFI, "impl %s: timing: %f" % (str(imp), elapsed))

if __name__ == '__main__':
  unittest.main()
