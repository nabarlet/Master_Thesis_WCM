#!/usr/bin/env python


""" Unit tests for the utilities/path.py file. """

import unittest
import sys, os
sys.path.extend(['..', os.path.join('..', '..')])
from utilities.string import is_utf_char, compare_string_length, string_similarity
from utilities.path import root_path, repo_path

class TestRootPath(unittest.TestCase):

  def test_root_path_existence(self):
      self.assertTrue(os.path.exists(root_path), root_path)
      
  def test_repo_path(self):
      self.assertTrue(os.path.exists(repo_path), repo_path)

if __name__ == '__main__':
  unittest.main()
