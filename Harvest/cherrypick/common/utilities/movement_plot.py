import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, *(['..']*2)), os.path.join(mypath, *(['..']*3))])

from db.db import DbPro

class MovementPlot:

    def __init__(self, db = DbPro()):
        self.db = db
        self.matrix = {}
        self.initialize_map()
        self.map_loaded = False
        self.max_value = 0

    def initialize_map(self):
         table = 'movement'
         what = 'name' 
         extra_args = 'WHERE parent_id IS NULL ORDER BY id'
         #
         # rows first
         #
         for r in self.db.select_all(table, what, extra_args):
             name = r[0]
             self.matrix[name] = {}
         #
         # columns after
         #
         for row in self.matrix.keys():
             for col in self.matrix.keys():
                 self.matrix[row][col] = 0
         self.map_loaded = False

    def size(self):
        rows = len(self.matrix)
        fkey = 'Medieval' # take Medieval as a reference
        cols = len(self.matrix[fkey])
        return (rows, cols)

    def to_csv(self):
        #
        # FIXME this doesn't align properly
        #
        result = ','
        for col in sorted(self.matrix.keys(), key=lambda x:int(x[1:])):
            result += (col + ',')
        result += '\n'
        for row in sorted(self.matrix.keys(), key=lambda x:int(x[1:])):
            csv_row = row + ','
            for col in sorted(self.matrix[row].keys()):
                csv_row += (str(self.matrix[row][col]) + ',')
            result += (csv_row + '\n')
        return result

    def clear_map(self):
        self.matrix = {}
        self.initialize_map()

    def fill_matrix(self, query_results):
        for idx1,rkey in enumerate(query_results):
            for idx2,ckey in enumerate(query_results):
                if idx1 != idx2:
                    r = rkey[0]
                    c = ckey[0]
                    self.matrix[r][c] += 1
                    self.matrix[c][r] += 1
                            
    def load_map(self):
        if not self.map_loaded:
            self.clear_map()
            pquery = "SELECT id from performance;"
            perfs = self.db.query(pquery)
            for pid in perfs:
                query = "SELECT movement.name FROM movement JOIN  composer, composer_performance, performance \
                         WHERE movement.id = composer.movement_id \
                         AND composer_performance.performance_id = performance.id \
                         AND composer_performance.composer_id = composer.id \
                         AND performance.id = %d;" % (pid[0])
                res = self.db.query(query)
                self.fill_matrix(res)
                            
            self.condition_matrix()
            self.map_loaded = True

    def normalize_map(self):
        if self.max_value > 0:
            for r in self.matrix.keys():
                for c in self.matrix[r].keys():
                    self.matrix[r][c] /= self.max_value

    __LOG_ZERO__ = 1e-18    
    def log_values(self):
        eps = MovementPlot.__LOG_ZERO__
        for r_key in self.matrix.keys():
            for c_key,col in self.matrix[r_key].items():
                value = math.log10(eps+col) 
                if value<0:
                    value=0.0
                self.matrix[r_key][c_key]=value           
                if self.matrix[r_key][c_key] > self.max_value:
                    self.max_value = self.matrix[r_key][c_key]

    def condition_matrix(self):
        self.log_values()
        self.normalize_map()
