import pdb
import sys, os
import sqlite3 as sl
import traceback

mypath = os.path.dirname(__file__)
sys.path.append(os.path.join(mypath, '..', 'cherrypick'))

from common.utilities.path import db_path

def sql_error(e):
    print(str(e), file=sys.stderr)

def sql_try(func):
    """
        +sql_try+ is a decorator to manage sql exceptions
        when using the db
    """
    def inner(*arg):
        res = None
        try:
            res = func(*arg)
        except sl.Error as e:
            traceback.print_exc()
            sql_error(e)
        return res
        
    return inner

class Db:
    """
        class +Db+ - is a singleton object. Usage:

        db = Db(filename)

        arguments:

        * filename: the (file) name of the database

        returns:

        * a db object instance which can then be used to create the whole database
    """
    class __Db__:

        def __init__(self, db_file_name):
            self.dbname = db_file_name
            self.db = self.__connect__()
    
        def reopen(self):
            self.db.close()
            self.db = self.__connect__()

        @sql_try
        def sql_execute(self, string, values = ()):
            cur = self.db.cursor()
            cur.execute(string, values)
            self.db.commit()
            return cur
    
        def create_table(self, table_name, fields = (), properties = ()):
            """
                +create_table(table_name, fields = (), properties = ())+:
    
                * table_name: the name of the table
                * properties: a list of lists: each property is a tuple of
                  strings: the name, the type and the attributes. If the type is omitted it is
                  assumed to be text.
            """
            sql_string = "CREATE TABLE IF NOT EXISTS %s (id integer PRIMARY KEY" % (table_name)
            for f in fields:
                attrs = 'text'
                if type(f) is str:
                    tname = f
                else:
                    if len(f) >= 2:
                        attrs = ' '.join(f[1:])
                    tname = f[0]
                sql_string += (", %s %s" % (tname, attrs))
            for p in properties:
                sql_string += (", %s" % (p))
            sql_string += ');'
            self.sql_execute(sql_string)
    
        def delete_table(self, table_name):
            sql_string = "DROP TABLE %s;" % (table_name)
            self.sql_execute(sql_string)
    
        @classmethod
        def connect(cls, db_file_name):
            return cls(db_file_name)
    
        @sql_try
        def __connect__(self):
            con = sl.connect(self.dbname)
            return con

        @sql_try
        def table_size(self, table):
            sql_string = 'SELECT count(*) FROM %s' % (table)
            cur = self.sql_execute(sql_string)
            result = cur.fetchall()[0][0]
            return int(result)

        @sql_try
        def query(self, string, values = ()):
            result = None
            cur = self.sql_execute(string, values)
            if cur:
                result = cur.fetchall()
            return result

        @sql_try
        def fetch_all(self, table, what = '*', extra_args = ''):
            sql_string = 'SELECT %s FROM %s %s;' % (what, table, extra_args)
            cur = self.sql_execute(sql_string)
            results = cur.fetchall()
            return results

        @sql_try
        def select_all(self, table, what = '*', extra_args = ''):
            """
                select_all(table, what = '*', extra_args = '')

                a generator that fetches all results and yields them to the
                caller. `what` is the wanted returned value (default: '*' for
                everything), `extra_args` may be any sql addition to the basic
                query
            """
            results = self.fetch_all(table, what, extra_args)
            for r in results:
                yield r

        def check_consistency(self):
            """
                check_consistency():
    
                checks that every composer has at least one performance and
                reports those that have no performances anywhere.
            """
            results = 0
            for comp in self.select_all('composer'):
                (id, name, birth, death, nid, mov) = comp
                perfs = [cperf[0] for cperf in self.select_all('composer_performance', 'performance_id', "WHERE composer_id = %d" % (id))]
                if len(perfs) == 0:
                    results += 1
                    print("No performance for composer %s (%s)" % (name, nid), file=sys.stderr)
            return results

    @classmethod
    def __new__(cls, dummy, db_name):
        if not cls.instance:
            cls.instance = Db.__Db__(db_name)
        return cls.instance

__DEFAULT_PRO_DB__ = os.path.join(db_path, 'WCM-pro.sqlite3')

class NoWritingOnProDb(Exception):
    pass

class DbPro(Db):

    instance = None

    @classmethod
    def __new__(cls, dummy, db_name = __DEFAULT_PRO_DB__):
        return super(DbPro, cls).__new__(dummy, db_name)

    def delete_table(self):
        raise NoWritingOnProDb

    def __getattr__(self, name):
        return DbPro.instance.getattr(name)

    def __setattr__(self, name):
        return DbPro.instance.setattr(name)


__DEFAULT_DEV_DB__ = os.path.join(db_path, 'WCM-dev.sqlite3')

class DbDev(Db):

    instance = None

    @classmethod
    def __new__(cls, dummy, db_name = __DEFAULT_DEV_DB__):
        return super(DbDev, cls).__new__(dummy, db_name)

    def __getattr__(self, name):
        return DbDev.instance.getattr(name)

    def __setattr__(self, name):
        return DbDev.instance.setattr(name)
