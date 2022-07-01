#!/usr/bin/env python


""" Unit tests for the utilities/cache.py file. """

import pdb
import unittest
import sys, os
sys.path.extend([os.path.join(*(['..']*2)), os.path.join(*(['..']*2), 'cherrypick'), os.path.join('..')])

from db.db import DbPro
from playlist import Playlist

class PlaylistTestCache(unittest.TestCase):

  def setUp(self):
      self.plist = Playlist()
      self.db = DbPro()

  def test_consistency(self):
      row_query_format = "SELECT performance.id from performance JOIN composer,composer_performance \
                          WHERE performance.id = composer_performance.performance_id \
                          AND composer_performance.composer_id = composer.id \
                          AND composer.nid = '%s';"
      for c in self.plist.composers:
          row_query = row_query_format % (c.nid)
          row_perfs = self.db.query(row_query)
          for rowp in row_perfs:
              count = 0
              pdb.set_trace()
              for other in c.crossings:
                  col_query_format = row_query_format.rstrip(';') + 'AND performance.id = %d;'
                  col_query = col_query_format % (other.node.nid, rowp[0])
                  col_perfs = self.db.query(col_query)
                  count += len(col_perfs)
                  print(count, other.how_many_times)
                  #self.assertEqual(size, other.how_many_times, "%d != %d between %s and %s" % (size, other.how_many_times, c.nid, other.cross_nid))

if __name__ == '__main__':
  unittest.main()
