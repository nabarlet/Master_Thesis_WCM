#!/usr/bin/env python


""" Unit tests for the utilities/bump.py file. """

import unittest
import sys, os, io
import contextlib as cl
sys.path.append(os.path.join(*(['..']*3)))

from common.utilities.bump import Bump

class TestBump(unittest.TestCase):

  def setUp(self):
      self.stdout = io.StringIO()
      self.stderr = io.StringIO()
      self.stdscr = io.StringIO()
      with cl.redirect_stdout(self.stdout), cl.redirect_stderr(self.stderr):
          self.b = Bump()
          self.b.fh = self.stdscr

  def test_create_singleton(self):
      self.assertTrue(self.b)
      b2 = Bump()
      self.assertIs(self.b, b2)

  def test_that_stdscr_is_properly_redirected(self):
      self.b.bump()
      self.assertEqual(self.stdscr.getvalue(), '.')

if __name__ == '__main__':
  unittest.main()
