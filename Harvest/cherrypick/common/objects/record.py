import pdb
import sys, os

mypath = os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, *(['..']*2)), os.path.join(mypath, *(['..']*3))])

import common.objects as obj
from common.utilities.string import join, double_to_single_quotes, sql_escape_single_quotes, __UNK__
from common.utilities.bwlist import BWList
from common.wikid.geoinfo    import get_lat_long_address
try:
    from db.db import DbDev, DbPro
except ModuleNotFoundError:
    from db import DbDev, DbPro

class MalformedRecord(ValueError):
    pass

class RecordPerformance(obj.ObjectBase):

    __DB_TABLE_NAME__ = 'record_performance'
    def __init__(self, record, performance, id = None):
        super().__init__(RecordPerformance.__DB_TABLE_NAME__)
        self.record = record
        self.performance = performance
        self.id = id

    @classmethod
    def query_by_rid_and_pid(cls, rec, perf, db=DbPro()):
        result = None
        qstring = "SELECT * FROM %s WHERE record_id = ? AND performance_id = ?;" % (RecordPerformance.__DB_TABLE_NAME__)
        values = (rec.id, perf.id)
        result = db.query(qstring, values)
        if result:
            (id, record_id, perf_id) = result[0]
            result = cls(rec, perf, id=id)
        return result

    def insert(self, db=DbDev()):
        result = self.__class__.query_by_rid_and_pid(self.record, self.performance, db=db)
        if not result:
            j_string = "INSERT INTO %s (record_id, performance_id) VALUES (?, ?);" % (self.table_name)
            values = (self.record.id, self.performance.id)
            db.sql_execute(j_string, values)
            self.bump.bump('+')
            result = self.__class__.query_by_rid_and_pid(self.record, self.performance, db=db)
        return result

class Record(obj.ObjectBase):

    __DB_TABLE_NAME__ = 'record'
    def __init__(self, comp = None, oi = None, title = None, perf = None, dur = __UNK__, label = __UNK__, id = None):
        super().__init__(Record.__DB_TABLE_NAME__)
        self.composer = comp
        self.title = title
        self.other_info = oi
        self.duration = dur
        self.label = label
        self.performance = perf
        self.id = id

    def inspect(self):
        result = "Record:\n\tcomposer:\t" + self.composer.inspect() + '\n'
        result += "\tid:\t\t" + str(self.id) + '\n'
        result += "\ttitle:\t\t" + str(self.title) + '\n'
        result += "\tother_info:\t" + str(self.other_info) + '\n'
        result += "\tduration:\t" + str(self.duration.inspect()) + '\n'
        result += "\tperformance:\t" + str(self.performance.inspect()) + '\n'
        result += "\tlabel:\t\t" + str(self.label) + '\n'
        return result

    def to_csv(self):
        result = ''
        if self.composer and self.performance:
            result = "%s,\"%s\",\"%s\",%s,\"%s\",%s" % (self.composer.to_csv(), double_to_single_quotes(self.title), double_to_single_quotes(self.other_info), self.duration, self.label, self.performance.to_csv())
        return result

    @classmethod
    def from_csv(cls, csv_line):
        result = None
        (nid, name, birth, death, movement, gender, country, lat, long) = csv_line[0:9] # composer
        if nid:
            (title, other_info, dur, label) = csv_line[9:13]                            # recording
            everything_else = csv_line[13:]                                             # performance
            if len(everything_else) != 4:
                print("WARNING: incorrect fields for performance data (%s). Unpacking the first four" % (str(everything_else)), file=sys.stderr)
            (provider, perf_date, perf_title, id) = everything_else[:4]                  # performance
            dur      = obj.Duration.create(dur, parser=obj.Duration.colon_parser)
            composer = obj.Composer(name, nid=nid, birth=birth, death=death, movement=movement, gender=gender, country=country, lat=lat, long=long)
            perform  = obj.Performance(perf_date, provider, title = perf_title)
            record   = obj.Record(comp=composer, oi=other_info, title=title, perf=perform, dur=dur, label=label)
            result   = record
        return result

    @classmethod
    def retrieve_from_csv(cls, csv_line, db=DbPro()):
        mrec = cls.from_csv(csv_line)
        perf = obj.Performance.query_by_datetime_and_provider(mrec.performance.datetime, mrec.performance.provider, db=db)
        comp = obj.Composer.query_by_name(mrec.composer.name, db=db)
        record = cls.query_by_title_and_oi(mrec.title, mrec.other_info, db=db)
        if record:
            if comp:
                record.composer = comp
            if perf:
                record.performance = perf
        else:
            record = mrec
        return record

    @classmethod
    def common_query(cls, query, values, perf=None, db=DbPro()):
        result = None
        results = db.query(query, values)
        if results and len(results) > 0:
            for r in results:
                (id, title, other_info, dur, label, cid) = r
                comp = obj.Composer.query_by_id(cid, db=db)
                dur  = obj.Duration.create(dur, parser=obj.Duration.colon_parser)
                result = cls(comp = comp, title = title, oi = other_info, perf=perf, dur=dur, label=label, id=id)
        return result

    @classmethod
    def query_by_title_and_oi(cls, title, oi, perf=None, db = DbPro()):
        qstring = "SELECT * FROM %s WHERE title = ? AND other_info = ? COLLATE NOCASE;" % (Record.__DB_TABLE_NAME__)
        values = (title, oi)
        return Record.common_query(qstring, values, perf=perf, db=db)

    @classmethod
    def query_by_id(cls, id, perf=None, db = DbPro()):
        qstring = "SELECT * FROM %s WHERE id = ?;" % (Record.__DB_TABLE_NAME__)
        values = (id, )
        return Record.common_query(qstring, values, perf=perf, db=db)

    def insert(self, db=DbDev()):
        """
            insert(db)

            performs the following tasks:

            * skip inserting all exceptions and report
            * insert composer (or retieve it if already found)
            * insert Performance (or retrieve it if already found)
            * insert Record (or retrieve it if already found)
            * insert Record->Performance link
            * insert all the composer->composer link belonging to the same performance
        """
        result = None
        try:
            orig_composer    = self.composer
            self.composer    = self.composer.insert(db=db)
            if self.composer and self.composer.id:
                self.performance = self.performance.insert(db=db)
                self.record      = self.insert_record(db=db)
                result           = self.record
                tp_link          = obj.RecordPerformance(self.record, self.performance)
                tp_link.insert(db=db)
                #
                # YTBD
                #
                # for c in self.performance.other_composers():
                #   cc_link = obj.ComposerComposer(self.composer, c)
            else:
                self.composer = orig_composer
                print("Skipping record: %s" % (self.to_csv()), file=sys.stderr)
        except Exception as e:
            print("Error: %s, record: %s" % (str(e), self.to_csv()), file=sys.stderr)

        return result

    def insert_record(self, db=DbDev()):
        result = self.__class__.query_by_title_and_oi(self.title, self.other_info, perf=self.performance, db=db)
        if not result:
            if not self.composer.id:
                raise MalformedRecord(self.composer.inspect())
            r_query = "INSERT INTO %s (title, other_info, duration, composer_id) VALUES (?, ?, ?, ?);" % (self.table_name)
            values = (self.title, self.other_info, str(self.duration), self.composer.id)
            db.sql_execute(r_query, values)
            self.bump.bump('r')
            result = self.__class__.query_by_title_and_oi(self.title, self.other_info, perf=self.performance, db=db)

        return result

    def delete(self, db = DbDev()):
        """
            delete(db = DbDev())
           
            Deletes this record from the database. The procedure is as follows:
           
            - find all Record connected to this composer
              - if only this one is connected, delete composer 
            - find all the RecordPerformance records connected to this record
              - if RecordPerformance == 1, delete record
            - delete record_performance
        """   
        #
        # check composer first
        #
        query = "SELECT count(*) FROM record AS R WHERE R.composer_id = ?;"
        values = (self.composer.id, )
        result = db.query(query, values)
        if result[0] == 1:
            self.composer.delete(db = db)
        #
        # then RecordPerformance records
        #
        query = "SELECT id FROM record_performance AS RP WHERE RP.performance_id = ?;"
        values = (self.performance.id, )
        results = db.query(query, values)
        if len(results) < 2:
            sqlc = "DELETE FROM record WHERE id = ?;"
            values = (self.id, )
            print("%s:%d: %s with values %s" % (os.path.basename(__file__), 209, sqlc, str(values)))
            db.sql_execute(sqlc, values)
        #
        # delete related record_performance
        #
        sqlc = "DELETE FROM record_performance WHERE record_id = ? AND performance_id = ?;"
        values = (self.id, self.performance.id, )
        print("%s:%d: %s with values %s" % (os.path.basename(__file__), 216, sqlc, str(values)))
        db.sql_execute(sqlc, values)
        self.bump.bump('-')

    def update_composer(self, new_composer, db=DbDev()):
        nc = new_composer.insert(db=db)
        if nc:
            self.composer = nc
            rec = self.insert(db=db)
            qupd = "UPDATE record SET composer_id = ? WHERE id = ?;"
            values = (nc.id, rec.id,)
            print("%s:%d: %s with values %s -- (%s)" % (os.path.basename(__file__), 224, qupd, str(values), nc.name))
            db.sql_execute(qupd, values)
            self.bump.bump('/')
        else:
            self.delete(db=db)
