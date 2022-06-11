#!/usr/bin/env python


""" Unit tests for the utilities/fuzzy_dict.py file. """

import unittest
import sys, os
sys.path.append(os.path.join(*(['..']*3)))

from common.utilities.fuzzy_dict import FuzzyDict, FuzzyDictNode
from common.utilities.string import string_similarity, random_string

class TestFuzzyDict(unittest.TestCase):

  def test_create(self):
      fd = FuzzyDict()
      self.assertEqual(fd, {})

  def test_key_presence(self):
      fd = FuzzyDict()
      test_string = 'test'
      fd.key_match(test_string)
      self.assertTrue(test_string in fd)

  def test_key_perfect_match(self):
      test_string_1 = 'test'
      test_string_2 = 'test'
      fd = FuzzyDict()
      res = fd.key_match(test_string_1)
      res = fd.key_match(test_string_2)
      self.assertEqual(res.counter, 4)
      self.assertEqual(res.object, test_string_1)

  def test_key_fuzzy_match(self):
      test_string_1 = 'test'
      test_string_2 = 'testch'
      fd = FuzzyDict()
      res = fd.key_match(test_string_1)
      res = fd.key_match(test_string_2)
      ss = string_similarity(test_string_1, test_string_2)
      self.assertTrue(ss >= FuzzyDict.__FuzzyDict__.SIMILARITY_THRESHOLD, "similarity between %s and %s below threshold: %f" % (test_string_1, test_string_2, ss))
      self.assertTrue(res.object in fd)
      self.assertEqual(res.counter, 2)
      self.assertEqual(len(res.aliases), 1)

  def test_non_matching_key(self):
      test_string = random_string()
      fd = FuzzyDict()
      res = fd.key_match(test_string)
      self.assertTrue(res.object, res.object)
      self.assertEqual(res.counter, 1)

class TestFuzzyDictNode(unittest.TestCase):

  def test_create(self):
      self.assertTrue(FuzzyDictNode('test'))

if __name__ == '__main__':
  unittest.main()
