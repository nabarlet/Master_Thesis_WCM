import pdb
import sys, os
import math
import re
import numpy as np

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, *(['..']*2)), os.path.join(mypath, *(['..']*3))])

try:
    from db.db import DbPro
except ModuleNotFoundError:
    from db import DbPro

from common.utilities.plot_range import PlotRange
from common.utilities.wcm_math import gini_porcaro

class MatrixNode:

    def __init__(self, row, col, rid = None,  cid = None, rname = None, cname = None, v = 0):
        self.__value__ = v
        self.conditioned_value = None
        self.row_nid = row
        self.col_nid = col
        self.row_movement_id = rid
        self.col_movement_id = cid
        self.row_name = rname
        self.col_name = cname

    def bump(self):
        self.__value__ += 1

    def value(self):
        """
            value()

            is needed because the actual linear value is doubled compared
            since it appears both in row/column and in column/row symmetrical
            pairs.
        """
        return self.__value__

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
         what = 'nid, movement_id, name' 
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
             rname = rr[2]
             for cr in comps:
                 col = cr[0]
                 cid = cr[1]
                 cname = cr[2]
                 self.matrix[row][col] = MatrixNode(row, col, rid, cid, rname, cname)
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

    @staticmethod
    def static_matrix_fill(input):
        """
            static_matrix_fill(input, output)

            isolates the delicate gauss summation-driven fill of a matrix
            creating a generator which will hand over the input list in
            ordered combinations (for ex. for [A, B, C]: [A,B], [A,C], [B, C])
        """
        sz = len(input)
        off = 0
        while (sz >= 1):
            for idx, key in enumerate(input[off:]):
                idx1 = off
                idx2 = off+idx
                if idx1 != idx2:
                    row = input[idx1]
                    col = input[idx2]
                    yield row, col
            off += 1
            sz  -= 1

    def fill_matrix(self, query_results):
        qr = [n[0] for n in query_results] # clean up results of database
        for row, col in ComposerPlot.static_matrix_fill(qr):
            self.matrix[row][col].bump()
            self.matrix[col][row].bump()
                            
    def load_full_map(self):
        if not self.full_map_loaded:
            self.clear_map()
            #
            # FIXME: the real query here should be:
            #
            # "SELECT C.nid,C.name,count(RP.id) from composer AS C JOIN record_performance as RP, record as R
            #  WHERE RP.record_id = R.id and R.composer_id = C.id GROUP BY C.id ORDER BY count(RP.id) DESC ;"
            #
            # this would allow to restrict the need for core memory of the
            # queries actually in use.
            #
            pquery = "SELECT P.id from performance AS P JOIN provider AS PR, \
                      provider_type AS PT WHERE P.provider_id = PR.id AND PR.type_id = PT.id AND PT.type = 'radio';"
            perfs = self.db.query(pquery)
            for pid in perfs:
                query = "SELECT C.nid FROM composer AS C JOIN record_performance AS RP, performance AS P, record AS R \
                         WHERE RP.performance_id = P.id \
                         AND RP.record_id = R.id \
                         AND R.composer_id = C.id \
                         AND P.id = ?;"
                values = (pid[0], )
                res = self.db.query(query, values)
                self.fill_matrix(res)
                            
            self.condition_matrix()
            self.full_map_loaded = True

    def cross_lookup(self, nid):
        self.load_full_map()
        for col in self.matrix[nid].values():
            if col.value() > 0:
                yield col

    def normalize_map(self):
        if self.max_value > 0:
            for r in self.matrix.keys():
                for c in self.matrix[r].keys():
                    self.matrix[r][c].conditioned_value /= self.max_value

    __LOG_ZERO__ = 1e-2    
    def log_values(self):
        eps = ComposerPlot.__LOG_ZERO__
        for r_key in self.matrix.keys():
            for c_key,col in self.matrix[r_key].items():
                value = col.value()
                if value <= 1.0:         # log10(1) -> 0, so we need to bias it with an epsilon value
                    value = 1.0 + eps
                value = math.log10(value) 
                if value<0:
                    value=0.0
                self.matrix[r_key][c_key].conditioned_value=value           
                if value > self.max_value:
                    self.max_value = value

    def calc_gini_coefficient(self, row):
        cols = self.matrix[row]
        col_values = [v.conditioned_value for v in cols.values()]
        g = gini_porcaro(col_values)
        self.gini_coefficients[row] = g
        return g

    def condition_matrix(self):
        self.log_values()
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
                list_row.append(self.matrix[row[0]][col[0]].conditioned_value)
            yield list_row

    def calc_column_sum(self):
        """
            calc_column_sum():

            calculates the total column sum using the full range of the
            matrix, that is all the possible values. We normalize everything
            at the end
        """
        result = [[k, 0, 0] for k in self.matrix.keys()]
        for row, cols in self.matrix.items():
            item = None
            #
            # find the item with the proper key in the result array
            # (put it in the 'item' variable)
            #
            for t in result:
                if t[0] == row:
                    item = t
                    break
            #
            # sum up both the conditioned_value (item[1])
            # and the linear integer value (item[2])
            #
            for lr in cols.values():
                item[1] += lr.conditioned_value
                item[2] += lr.value()
            #
            # rescale with the gini coefficient
            #
            if item[1] > 0.0:
                gcoeff = self.calc_gini_coefficient(row)
                item[1] *= gcoeff    
            #
            # set up the maximum value for normalization
            #
            if item[1] > self.max_col_sum:
                self.max_col_sum=item[1]
        #
        # we normalize everything at the end
        #
        # (we also divide the linear value by two to adjust for the column/row
        #  duplicate) --------------------------------------+
        #                                                   |
        #                                                   v
        result = [[item[0], item[1]/self.max_col_sum, (item[2]/2.0)] for item in result]
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
                values = (id, )
                res = self.db.query('SELECT C.nid FROM composer AS C JOIN record AS R, record_performance AS RP \
                                     WHERE RP.performance_id = ? \
                                     AND RP.record_id = R.id \
                                     AND C.id = R.composer_id;', values)
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
                res = self.db.query('SELECT C.nid FROM composer AS C JOIN record_performance AS RP, record AS R \
                                     WHERE RP.performance_id = ? \
                                     AND RP.record_id = R.id \
                                     AND C.id = R.composer_id;', (id, ))
                self.fill_matrix(res)

            self.condition_matrix()
            self.provider_map_loaded = True
