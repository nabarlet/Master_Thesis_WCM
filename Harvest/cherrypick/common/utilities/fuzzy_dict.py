import sys,os
sys.path.append(os.path.join('..', '..'))

import yaml
from yaml import Loader

from common.utilities.string import string_similarity

class FuzzyDictNode:
    def __init__(self, obj, cnt = 1, aka = []):
        self.object = obj
        self.counter = cnt
        self.aliases = aka

    def inspect(self):
        aliases_string = ''
        if len(self.aliases) > 0:
            aliases_string = " (%s)" % (str(self.aliases))
        output = "%3d: %s\n" % (self.counter, self.object + aliases_string)
        return output
    
class FuzzyDict:
    #
    # singleton pattern scheme
    #
    class __FuzzyDict__(dict):
        SIMILARITY_THRESHOLD = 0.9
    
        def key_match(self, string):
            """
               key_match(matching_string):
    
               check keys: if there is a perfect match add 
               the counter and return the matching node.
               If there is a fuzzy match add the counter, add the
               name to the matching set and return the matching node.
               Otherwise return None.
            """
            if string in self: # perfect match
                self[string].counter += 1
                return self[string].object
            for k in self.keys():
                if string_similarity(k, string) >= FuzzyDict.__FuzzyDict__.SIMILARITY_THRESHOLD:
                    self[k].counter += 1
                    if not string in self[k].aliases:
                        self[k].aliases.append(string)
                    return self[k].object
            self[string] = FuzzyDictNode(string)
            return self[string].object
    
        def inspect(self):
            result = ''
            for v in self.values():
                result += v.inspect()
            return result
    
        def load_lists(self):
            with open(FuzzyDict.BLACK_WHITE_LISTS_PATH, 'r') as fl:
                lists = yaml.load(fl, Loader)
            return [lists['black_list'], lists['white_list']]

    instance = None

    def __new__(cls):
        if not FuzzyDict.instance:
            FuzzyDict.instance = FuzzyDict.__FuzzyDict__()
        return FuzzyDict.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
