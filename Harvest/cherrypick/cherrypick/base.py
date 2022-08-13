import pdb
import os, sys
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import common.wikid.wikidata as wd
import common.objects as obj
from common.wikid.sparql import sparql_composer 
from pathlib import Path
from utilities.fuzzy_dict import FuzzyDict
from utilities.bwlist import BWList

class Base:

    def __init__(self):
        self.black_white_list = BWList()
        self.composers_fuzzy_dict = FuzzyDict()

    @classmethod
    def manage(cls, repo_dir, pattern = '*.pdf'):
        p = Path(repo_dir)
        files = p.glob(pattern)
        for f in files:
            yield cls(f)

    def retrieve_composer(self, name):
       result = None
       if not self.black_white_list.is_black(name):
           nid = self.black_white_list.is_white(name)
           if not nid:
               name = self.composers_fuzzy_dict.key_match(name)
               result = wd.retrieve_composer(name)
           else:
               result = sparql_composer(nid)

       if not result:
           result = obj.Composer(name)

       return result

    @classmethod
    def create_csv(cls, repo_dir):
        for coll in cls.manage(repo_dir):
            for rec in coll.parse():
                yield rec
#               found = not_found = None
#               comp = rec.composer
#               if comp and comp.nid and comp.birth:
#                   found = rec
#               else:
#                   not_found = rec
#               yield found, not_found
