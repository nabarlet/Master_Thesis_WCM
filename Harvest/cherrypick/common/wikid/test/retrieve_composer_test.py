#!/usr/bin/env python


""" Unit tests for the utilities/fuzzy_dict.py file. """

import pdb
import unittest
import sys, os
import traceback
sys.path.append(os.path.join(os.path.dirname(__file__), *(['..']*2)))

from wikid.wikidata import retrieve_composer
from common.objects.composer import Composer

class TestRetrieveComposer(unittest.TestCase):

  def setUp(self):
      self.queries = [ 'Úlfur', 'Antonín Dvořák', 'Johannes Brahms', 'ludwig van beethoven', 'wolfgang amadeus mozart', 'johann sebastian bach', 'E. SAINZ DE LA MAZA', 'MARTINS', 'CHAIKOVSKY', 'R. STRAUSS', 'PITTALUGA', 'carl tausig', 'carl czerny', 'henri vieuxtemps' ]

  def test_retrieve_composer(self):
      for name in self.queries:
        comp = None
        try:
            comp = retrieve_composer(name)
            self.assertIsInstance(comp, Composer)
        except Exception as e:
            traceback.print_exc()
            print("Errored out: %s" % (e))
            # continuing...

if __name__ == '__main__':
  unittest.main()
