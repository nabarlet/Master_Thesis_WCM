import pdb
import sys, os
import csv

mypath = os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, *(['..']*2)), os.path.join(mypath, *(['..']*3), 'db', 'create')])
import common.utilities.path as p
import common.objects as obj
from db.db import DbDev, DbPro

class ComposerAgeIsZero(Exception):
    pass

class TimeNode:
    def __init__(self, start, end, key = None, id = None):
        self.sub_nodes = {}
        self.key = key
        self.start = int(start)
        self.end   = int(end)
        self.id    = id

    __TN_INDENT__ = 4
    def inspect(self, spaces = 0, keysize = 40):
        indent = ' ' * spaces
        result = "%s%-*s %4d %4d (%d)" % (indent, keysize, self.key, self.start, self.end, self.id)
        for k, v in self.sub_nodes.items():
            result += ('\n' + v.inspect(spaces + TimeNode.__TN_INDENT__, keysize - TimeNode.__TN_INDENT__))
        return result

    def period_overlap(self, comp):
        """
            period_overlap(composer)

            return a float overlapping factor from 0 (no overlap) to 1 (full
            overlap), or None if composer has no birth date
        """
        if not comp.birth:
            return None
        result = 0
        ovl_start = ovl_end = None
        comp_start = comp.birthdate().year
        comp_end = comp.end_date().year
        if comp_start < self.end and comp_start > self.start:
            ovl_start = comp_start
        if comp_end > self.start and comp_end < self.end:
            ovl_end = comp_end
        if ovl_start and ovl_end:
            result = comp.age()
        elif ovl_start and not ovl_end:
            result = self.end - ovl_start
        elif not ovl_start and ovl_end:
            result = ovl_end - self.start
        if comp.age() == 0:
            raise ComposerAgeIsZero(comp.name)
        return float(result) / float(comp.age())

    def save_record(self, db, tn):
        i_string = "INSERT INTO %s (name, start, end) VALUES ('%s', %d, %d)" % (tn, self.key, self.start, self.end)
        db.sql_execute(i_string)
        if len(self.sub_nodes) > 0:
            f_string = "SELECT id FROM %s WHERE name = '%s'" % (tn, self.key)
            parent_id = db.query(f_string)[0][0]
            for key, tnode in self.sub_nodes.items():
                i_string = "INSERT INTO %s (name, start, end, parent_id) VALUES ('%s', %d, %d, %d)" % (tn, key, tnode.start, tnode.end, parent_id)
                db.sql_execute(i_string)

class TimeLine(dict, obj.ObjectBase):

    __DB_TABLE_NAME__ = 'movement'

    def __init__(self):
        #
        # PLEASE NOTE: this ugly hack is needed to make sure that all parent
        # classes get properly initialized. Thank you python :-(
        #
        for clss in TimeLine.__mro__:
            super(clss, self).__init__()
        self.table_name = TimeLine.__DB_TABLE_NAME__

    __TIMELINE_DEFAULT_SOURCE_FILE__ = os.path.join(p.repo_path, 'other_data', 'List_of_eras.csv')
    @classmethod
    def create_from_csv(cls, csv_file = __TIMELINE_DEFAULT_SOURCE_FILE__, delimiter = '\t'):
        tl = cls()
        with open(csv_file, 'r') as fh:
            reader = csv.reader(fh, delimiter=delimiter)
            last_node = None
            for row in reader:
                if row[0] == 'Movement' or (row[0] == '' and row[1] == ''):
                    continue
                this_node = TimeNode(row[2], row[3])
                if row[0]:
                    this_node.key = row[0]
                    tl[row[0]] = last_node = this_node
                else:
                    this_node.key = row[1]
                    last_node.sub_nodes[row[1]] = this_node
        return tl

    def inspect(self):
        result = ''
        for k, v in self.items():
            result += ('\n' + v.inspect())
        return result

    def assign_movement(self, composer):
        """
            assign_movement(composer)

            assigns a movement to a composer by overlapping eras,
            returning None if the composer has no birth date specified,
            or the best overlapping period if birth date is specified.
        """
        if not composer.birth:
            return None
        result = {}
        for k, tn in self.items():
            result[k] = tn.period_overlap(composer)
        sresult = list(sorted(result.items(), key=lambda x:x[1], reverse=True))
        return sresult[0][0]

    def save_records(self):
        for key, tnode in self.items():
            tnode.save_record(self.db, TimeLine.__DB_TABLE_NAME__)

    def load_records(self):
        last_parent = None
        for r in self.db.select_all(TimeLine.__DB_TABLE_NAME__):
            (id, name, start, end, parent_id) = r
            tn = TimeNode(start, end, name, id)
            if not parent_id:
                last_parent = tn
                self[name] = tn
            else:
                last_parent.sub_nodes[name] = tn

    @classmethod
    def create(cls):
        result = None
        db = DbDev()
        args = ('name', ('start', 'year', 'non_null'), ('end', 'year'), ('parent_id', 'integer'))
        db.create_table(cls.__DB_TABLE_NAME__, args)
        if db.table_size(cls.__DB_TABLE_NAME__) == 0:
            result = cls.create_from_csv()
            result.save_records()
        else:
            result = cls.create_from_db()
        return result

    @classmethod
    def query_common(cls, qstring, db):
        result = None
        results = db.query(qstring)
        if len(results) > 0:
            (id, name, start, end, parent_id) = results[0]
            result = TimeNode(start, end, name, id)
        return result
        
    @classmethod
    def query_by_id(cls, id, db = DbPro()):
        f_query = "SELECT * from %s WHERE id = %d" % (cls.__DB_TABLE_NAME__, id)
        return cls.query_common(f_query, db)

    @classmethod
    def query_by_name(cls, name, db = DbPro()):
        f_query = "SELECT * from %s WHERE name = '%s'" % (cls.__DB_TABLE_NAME__, name)
        return cls.query_common(f_query, db)
