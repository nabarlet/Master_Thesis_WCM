import pdb
import sys, os
import math
import re

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, *(['..']*2)), os.path.join(mypath, *(['..']*3))])

from db.db import DbPro
from common.utilities.plot_range import PlotRange
from common.utilities.wcm_math import gini_porcaro

class MatrixNode:

    def __init__(self, rid = None,  cid = None, v = 0):
        self.value = v
        self.row_movement_id = rid
        self.col_movement_id = cid

    def bump(self):
        self.value += 1

class ComposerPlot:

    def __init__(self, db = DbPro()):
        self.db = db
        self.matrix = {}
        self.sub_matrix = None
        self.initialize_map()
        self.full_map_loaded = False
        self.max_value = 0
        self.max_col_sum=0
        self.plot_range = PlotRange()
        self.gini_coefficients = {}
        self.sorted_keys = self.sort_keys()

    def initialize_map(self):
         table = 'composer'
         what = 'nid, movement_id' 
         extra_args = 'ORDER BY nid'
         comps = self.db.fetch_all(table, what, extra_args)
         #
         # rows first
         #
         for r in comps:
             nid = r[0]
             self.matrix[nid] = {}
         #
         # columns after
         #
         for rr in comps:
             row = rr[0]
             rid = rr[1]
             for cr in comps:
                 col = cr[0]
                 cid = cr[1]
                 self.matrix[row][col] = MatrixNode(rid, cid)
         self.map_loaded = False

    def size(self):
        rows = len(self.matrix)
        fkey = 'Q254' # we take Mozart as a reference
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
                    self.matrix[r][c].bump()
                    self.matrix[c][r].bump()
                            
    def load_full_map(self):
        if not self.full_map_loaded:
            self.clear_map()
            pquery = "SELECT id from performance;"
            perfs = self.db.query(pquery)
            for pid in perfs:
                query = "SELECT composer.nid FROM composer JOIN composer_performance, performance \
                         WHERE composer_performance.performance_id = performance.id \
                         AND composer_performance.composer_id = composer.id \
                         AND performance.id = %d;" % (pid[0])
                res = self.db.query(query)
                self.fill_matrix(res)
                            
            self.condition_matrix()
            self.full_map_loaded = True

    def normalize_map(self):
        if self.max_value > 0:
            for r in self.matrix.keys():
                for c in self.matrix[r].keys():
                    if r == c:
                        self.matrix[r][c].value = 1
                    else:
                        self.matrix[r][c].value /= self.max_value

    __LOG_ZERO__ = 1e-18    
    def log_values(self):
        eps = ComposerPlot.__LOG_ZERO__
        for r_key in self.matrix.keys():
            for c_key,col in self.matrix[r_key].items():
                value = math.log10(eps+col.value) 
                if value<0:
                    value=0.0
                self.matrix[r_key][c_key].value=value           
                if self.matrix[r_key][c_key].value > self.max_value:
                    self.max_value = self.matrix[r_key][c_key].value

    def rescale_with_gini_coefficient(self):
        for row, cols in self.matrix.items():
            col_values = [v.value for v in cols.values()]
            g = gini_porcaro(col_values)
            self.gini_coefficients[row] = g
            if g and g > 0.0:
                for col in cols:
                    self.matrix[row][col].value /= g

    def condition_matrix(self):
        self.log_values()
        self.rescale_with_gini_coefficient()
        self.normalize_map()

    def get_submatrix(self):
        """
            get_submatrix(plot_range = None)

            uses the saved PlotRange object
            to slice the matrix in a specific row/column to row/column
            slice.
        """
        (rfrom, rto, cfrom, cto) = self.plot_range.to_list(self.size())
        for row in self.sorted_keys[rfrom:rto]:
            list_row = []
            for col in self.sorted_keys[cfrom:cto]:
                list_row.append(self.matrix[row[0]][col[0]].value)
            yield list_row

    def calc_column_sum(self):
        """
            calc_column_sum():

            calculates the total column sum using the full range of the
            matrix, that is all the possible values. We normalize everything
            at the end
        """
        result = [[k, 0] for k in self.matrix.keys()]
        for row, cols in self.matrix.items():
            item = None
            for t in result:
                if t[0] == row:
                    item = t
                    break
            for lr in cols.values():
                item[1] += lr.value
                if item[1] > self.max_col_sum:
                    self.max_col_sum=item[1]
        #
        # we normalize everything at the end
        #
        result = [[item[0], item[1]/self.max_col_sum] for item in result]
        return result

    def sort_keys(self):
        """
            sort_keys():

            sorts the keys according to the total column sum of each list.
            This is done using the *full* dataset, and is not a per-provider
            calculation (in order to be consistent among providers)
        """
        self.load_full_map()
        column_sums = self.calc_column_sum()
        return sorted(column_sums, key=lambda x: x[1], reverse=True)

class ComposerFullPlot(ComposerPlot):

    def load_map(self):
        self.load_full_map()

class ComposerRadioPlot(ComposerPlot):

    def __init__(self, db = DbPro()):
        super().__init__(db)
        self.radio_map_loaded = False

    def load_map(self):
        if not self.radio_map_loaded:
            self.clear_map()
            table = 'performance'
            what = 'id'
            #
            # FIXME: the following query is very ugly. Providers should have a
            # 'type' column allowing to select 'Radio' rather than 'Streaming
            # Service' or 'Concert Society' etc.
            #
            extra_args = 'WHERE provider_id < 4'
            for p in self.db.select_all(table, what, extra_args):
                id = p[0] 
                res = self.db.query('SELECT composer.nid FROM composer JOIN composer_performance \
                                     WHERE composer_performance.performance_id = %d \
                                     AND composer.id = composer_performance.composer_id;' % (id))
                self.fill_matrix(res)

            self.condition_matrix()
            self.radio_map_loaded = True

class ComposerProviderPlot(ComposerPlot):

    def __init__(self, db = DbPro()):
        super().__init__(db)
        self.provider_map_loaded = False

    def load_map(self, provider_name):
        if not self.provider_map_loaded:
            self.clear_map()
            p_id = self.db.query('SELECT id from provider WHERE name = "%s";' % (provider_name))[0][0]
            table = 'performance'
            what = 'id'
            extra_args = 'WHERE provider_id = %d' % (p_id)
            for p in self.db.select_all(table, what, extra_args):
                id = p[0] 
                res = self.db.query('SELECT composer.nid FROM composer JOIN composer_performance \
                                     WHERE composer_performance.performance_id = %d \
                                     AND composer.id = composer_performance.composer_id;' % (id))
                self.fill_matrix(res)

            self.condition_matrix()
            self.provider_map_loaded = True
