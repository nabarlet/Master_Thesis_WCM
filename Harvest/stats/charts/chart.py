import pdb
import sys,os

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '.'), os.path.join(mypath, *['..']*2)])

from db.db import DbPro

class Chart:

    def __init__(self, ylimit = 60, xlimit = None, rootpath = '.'):
        self.ylimit = ylimit
        self.xlimit = xlimit
        self.rootpath = rootpath
        self.plotdir = os.path.join(self.rootpath, './plots')
        self.db = DbPro()

    @staticmethod 
    def load_composers():
        db = DbPro()
        cquery = "SELECT C.id, C.name FROM composer AS C;"
        return db.query(cquery)

    @staticmethod 
    def load_eras():
        db = DbPro()
        equery = "SELECT M.id, M.name FROM movement AS M WHERE M.parent_id IS NULL ORDER BY M.id;"
        return db.query(equery)

    @staticmethod
    def load_providers():
        db = DbPro()
        rquery = "SELECT P.id,P.name FROM provider AS P JOIN provider_type AS PT WHERE P.type_id = PT.id AND PT.type = 'radio';"
        return db.query(rquery)
