#!/usr/bin/env python

import pdb
import unittest
import os, sys

sys.path.extend(['..', os.path.join('..', '..')])

from rrc_parser.rrc_subdivider import RRCSubdivider
from common.utilities.path import root_path, full_file

class TestRRCSubdivider(unittest.TestCase):

    def setUp(self):
        f = open(full_file, 'r')
        self.lines = f.readlines()
        f.close()

    def test_subdivider_section_creation(self):
        rs = RRCSubdivider(self.lines)
        rs.create_sections()
        self.assertTrue(len(rs.sections) > 9470)
        self.assertTrue(len(rs.ignored_sections) <= 55)
        for s in rs.sections:
            res = s.inspect()
            self.assertTrue(len(res) > 0)

    def test_subdivider_parsing(self):
        rs = RRCSubdivider(self.lines)
        for obj in rs.parse():
            print(obj.inspect())
            # self.assertTrue(obj)

if __name__ == '__main__':
    unittest.main()
