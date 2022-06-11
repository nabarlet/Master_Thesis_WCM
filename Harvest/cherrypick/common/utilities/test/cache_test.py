#!/usr/bin/env python


""" Unit tests for the utilities/cache.py file. """

import unittest
import sys, os
sys.path.append(os.path.join(*(['..']*3)))

from common.utilities.cache import Cache

class TestCache(unittest.TestCase):

  CACHE_FIXTURE = 'cache_test.yml'

  def test_create(self):
      c = Cache(TestCache.CACHE_FIXTURE)
      self.assertEqual(c, {})

  def test_multiple_create_only_one(self):
      c0 = Cache(TestCache.CACHE_FIXTURE)
      c1 = Cache(TestCache.CACHE_FIXTURE)
      c2 = Cache(TestCache.CACHE_FIXTURE)
      self.assertEqual(c0, c1)
      self.assertEqual(c1, c2)
      self.assertEqual(c0, c2)

  def test_it_behaves_like_a_dict(self):
      c = Cache(TestCache.CACHE_FIXTURE)
      c['test'] = 'test'
      self.assertEqual(c['test'], 'test')

if __name__ == '__main__':
  unittest.main()
