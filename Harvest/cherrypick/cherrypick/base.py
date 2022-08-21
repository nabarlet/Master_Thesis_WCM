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

    def __init__(self, provider):
        self.provider = provider
        self.black_white_list = BWList()
        self.composers_fuzzy_dict = FuzzyDict()

    @classmethod
    def manage(cls, repo_dir, provider, pattern = '*.pdf'):
        p = Path(repo_dir)
        files = p.glob(pattern)
        for f in files:
            yield cls(f, provider)

    def retrieve_composer(self, name):
       return Base.static_retrieve_composer(name, self.provider, self.black_white_list, self.composers_fuzzy_dict)

    @staticmethod
    def static_retrieve_composer(name, provider, bwl = BWList(), cfd = FuzzyDict()):
       result = None
       if not bwl.is_black(name):
           #
           # HACK: this is a temporary fix to solve a nasty bug with the
           # FuzzyDict(). In fact, what needs to be done here is to rewrite
           # the FuzzyDict object using a virtual in memory sqlite table with
           # FTS check of the name. We also need to test its functionality for
           # cases of strings embedded in other strings, like 'Nico' in
           # 'DomeNico Scarlatti' etc.
           #
           nid = bwl.is_white(name)
           if not nid:
               if provider == 'RadioC':
                   name = cfd.key_match(name)
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
