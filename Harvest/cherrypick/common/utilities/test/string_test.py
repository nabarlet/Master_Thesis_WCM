#!/usr/bin/env python


""" Unit tests for the utilities/string.py file. """

import unittest
import sys, os
sys.path.extend(['..', os.path.join('..', '..')])
from utilities.string import is_utf_char, compare_string_length, string_similarity, normalized_re

EPS=1e-6

class TestStringUtilities(unittest.TestCase):

  def test_is_utf_char(self):
      self.assertEqual(is_utf_char('a'), '[AaÀàÁáÅåÄä]')
      self.assertEqual(is_utf_char('b'), 'b')
      self.assertEqual(is_utf_char('C'), '[CcÇç]')
      
  def test_string_similarity(self):
      self.assertAlmostEqual(string_similarity('Ludwig Van Beethoven', 'BEETHOVEN'), 1.0)
      self.assertAlmostEqual(string_similarity('TCHAIKOVSKY', 'CIAIKOVSKIJ'), 0.72727273)
      self.assertAlmostEqual(string_similarity('Wolfgang Amadeus Mozart', 'MORZAT'), 0.5)
      self.assertAlmostEqual(string_similarity('TCHAIKOVSKY', 'vavuuva'), 0.28571428)
      self.assertAlmostEqual(string_similarity('TCHAIKOVSKY', 'CHAIKOVSKY'), 1)

  def test_normalized_re(self):
      tests = [
        "Eva Dell'Acqua",
        "Eva Dell\\'Acqua",
        "Aria from \'Goldberg Variations\' ",
        "Les Jeux d\'eaux à la Villa d\'Este (Années de pèlerinage (3eme annee) ",
        "Lauda Jerusalem (psalm 147, \'How good it is to s... ",
      ]
      for t in tests:
        for c in range(len(t)):
            self.assertTrue(normalized_re(t[c]), t)


if __name__ == '__main__':
  unittest.main()
