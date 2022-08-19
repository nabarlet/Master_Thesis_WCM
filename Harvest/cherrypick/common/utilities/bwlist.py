import pdb
import sys,os
sys.path.append(os.path.join('..', '..'))

import yaml
from yaml import Loader

from common.utilities.string import string_similarity

class BWList:
    """
        BWList is a singleton class holding a yaml defined combination of a
        black list and a white list
    """
    #
    # singleton pattern scheme
    #
    class __BWList__:

        BLACK_WHITE_LISTS_PATH = os.path.join(os.path.dirname(__file__), 'data', 'fuzzy_dict', 'black_white_lists.yml')
    
        def __init__(self):
            (self.black, self.white) = self.load_lists()
    
        def is_black(self, string):
            return string in self.black
    
        def is_white(self, string):
            """
               is_white(matching_string):
    
               return value if the normalized string is in the white list
               Otherwise none.
            """
            result = None
            ustring = string.upper()
            lstring = string.lower()
            if string in self.white:
                result = self.white[string]
            if not result and ustring in self.white:
                result = self.white[ustring]
            if not result and lstring in self.white:
                result = self.white[lstring]
            return result
    
        def load_lists(self):
            with open(BWList.__BWList__.BLACK_WHITE_LISTS_PATH, 'r') as fl:
                lists = yaml.load(fl, Loader)
            return [lists['black_list'], lists['white_list']]

    instance = None

    def __new__(cls):
        if not BWList.instance:
            BWList.instance = BWList.__BWList__()
        return BWList.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
