#!/usr/bin/env python


""" Unit tests for the utilities/fuzzy_dict.py file. """

import pdb
import unittest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), *(['..']*2)))

from wikid.wikidata import retrieve_composer

class TestRetrieveComposer(unittest.TestCase):

  def setUp(self):
      self.queries = [ 'CHAIKOVSKY', 'R. STRAUSS', 'MARTINS', 'PITTALUGA', 'carl tausig', 'carl czerny', 'henri vieuxtemps' ]

  def test_retrieve_composer(self):
      for name in self.queries:
        comp = retrieve_composer(name)
        self.assertTrue(comp.birth, name)

if __name__ == '__main__':
  unittest.main()
