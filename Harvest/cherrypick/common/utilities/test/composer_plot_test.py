#!/usr/bin/env python

""" Unit tests for the utilities/composer_plot.py file objects. """

import unittest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from composer_plot import ComposerPlot, PlotRange

class TestPlotRange(unittest.TestCase):

    def test_plot_range_creation(self):
        plot_ranges = {
            '36:235x23:23': (36, 235, 23, 23),
            ':235x23:23':   (0, 235, 23, 23),
            '23x23':        (23, None, 23, None),
            'x':            (0,  None, 0,  None),
            ':23x:23':      (0,  23,   0,  23),
            '23:x23:':      (23, None, 23, None),
        }
        for str, val in plot_ranges.items():
            pr = PlotRange.create(str)
            self.assertEqual(pr.to_list(), val, str)

    def test_plot_range_creation_with_size(self):
        plot_full_size = (1023, 1023)
        plot_ranges = {
            '36:235x23:23': (36, 235, 23, 23),
            ':235x23:23':   (0, 235, 23, 23),
            '23x23':        (23, 1023, 23, 1023),
            'x':            (0,  1023, 0,  1023),
            ':23x:23':      (0,  23,   0,  23),
            '23:x23:':      (23, 1023, 23, 1023),
        }
        for str, val in plot_ranges.items():
            pr = PlotRange.create(str)
            self.assertEqual(pr.to_list(plot_full_size), val, str)

if __name__ == '__main__':
  unittest.main()
