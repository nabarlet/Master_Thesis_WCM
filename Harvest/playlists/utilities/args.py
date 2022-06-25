import sys, os
import argparse as ap

mypath = os.path.dirname(__file__)
sys.path.extend([mypath, os.path.join(mypath, *(['..']*2), 'cherrypick')])

from plugs import random, exclusive_random
from common.utilities.wcm_math import reverse_decile, exp_decile

class Args:

    __ARGUMENTS__ = \
    [
        ("-r", "--randomizer", "select the randomizer function (default: random)", "random"),
        ("-m", "--movement", "select the movement sub-section (default: None - all db is selected)", None),
        ("-z", "--zone", "select zone subdivision ({reverse_decile | exp_decile} default: exp_decile)", "exp_decile"),
    ]
    @classmethod
    def parse_args(cls):
        argp = ap.ArgumentParser()
        for a in cls.__ARGUMENTS__:
            (short, long, helpstring, default) = a
            argp.add_argument(short, long, help=helpstring, default=default)
    
        result = argp.parse_args(namespace=cls)
        result.randomizer = eval(result.randomizer)
        result.zone       = eval(result.zone)
        return result
