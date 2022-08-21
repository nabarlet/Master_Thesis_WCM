import pdb
import csv
import sys, os

mypath=os.path.dirname(__file__)
__CHERRY_PATH__ = os.path.join(mypath, '..', 'cherrypick')
sys.path.extend([mypath, __CHERRY_PATH__, os.path.join(mypath, *['..']*2)])

import datetime as dt
import common.objects as obj
from db import DbDev

class MisalignedCsv(ValueError):
    pass

class UndetectedDifference(ValueError):
    pass

class DbFixer:
    """
        DBFixer:

        given the size of the data base and the time it takes to build from
        scratch (> 48 hours) for small fixes it is better to proceed in a
        selective way comparing two csv files, the (previous) wrong one and
        the (current) corrected one, and then proceed chirurgically operating
        on a record-by-record level. This is what this DbFixer is about.
    """

    __DEFAULT_RIGHT_TEMPL__ = '%s_clean.csv'
    __DEFAULT_WRONG_TEMPL__ = '%s_clean.csv-20220818-BROKEN'
    def __init__(self, provider, right = __DEFAULT_RIGHT_TEMPL__, wrong = __DEFAULT_WRONG_TEMPL__):
        self.provider = provider
        self.prefixes = {'RAIRadioClassica': 'RRC', 'RadioC': 'RC', 'BBC3': 'BBC', }
        self.right = os.path.join(__CHERRY_PATH__, self.provider, right % (self.prefixes[self.provider]))
        self.wrong = os.path.join(__CHERRY_PATH__, self.provider, wrong % (self.prefixes[self.provider]))
        self.db    = DbDev()

    def setup(self):
        rightfh = open(self.right, 'r')
        wrongfh = open(self.wrong, 'r')
        rightcsv = csv.reader(rightfh)
        wrongcsv = csv.reader(wrongfh)
        return (rightfh, rightcsv, wrongfh, wrongcsv)

    __END_TIME__ = dt.datetime(2022, 8, 10, 23, 59, 0)
    def compare_csv(self):
        with open(self.right, 'r') as rfh:
            with open(self.wrong, 'r') as wfh:
                self.rightcsv = csv.reader(rfh)
                self.wrongcsv = csv.reader(wfh)
                rdata = [l for l in self.rightcsv]
                wdata = [l for l in self.wrongcsv]
                tsize = 0
                rsize = len(rdata)
                wsize = len(wdata)
                if rsize < wsize:
                    tsize = rsize
                else:
                    tsize = wsize
                for idx in range(tsize):
                    rarr = rdata[idx]
                    warr = wdata[idx]
                    try:
                        perf_time = dt.datetime.fromisoformat(rarr[14])
                        if perf_time > DbFixer.__END_TIME__:
                            break
                    except (TypeError, ValueError):
                        pass
                    if DbFixer.check_alignement(idx, rarr, warr):
                        if rarr[2] != warr[2]:
                            yield idx, rarr, warr
                    else:
                        print('Misaligned Record ', idx, str(rarr), str(warr), file=sys.stderr)

    __FIELDS_TO_BE_CHECKED__ = [14]
    @staticmethod
    def check_alignement(recidx, right, wrong):
        """
            check_alignement

            checks that certain fields are identical. Currently the fields
            checked are:
            9  = record title
            12 = performance datetime

            if any of these fields differ, the result returned is false
        """
        result = True
        for idx in DbFixer.__FIELDS_TO_BE_CHECKED__:
            try:
                if right[idx] != wrong[idx]:
                    result = False
            except IndexError as ie:
                raise IndexError(recidx, idx)
        return result

    def fix_by_csv(self):
        #
        # fix_by_csv():
        #
        # this is done comparing the right csv with the wrong one. Several
        # outcomes are possible:
        #
        # - right composer existing - wrong composer non existing -> record is created with right composer and inserted
        # - right composer non existing - wrong composer existing -> record is _deleted_ from the db along with links etc.
        # - right composer existing - wrong composer existing     -> composer_id is substituted in record
        #
        nidfield = 0
        for idx, right, wrong in self.compare_csv():
            if right[nidfield] != 'None' and wrong[nidfield] == 'None':
                DbFixer.create_record(right, wrong, db = self.db)
            elif right[nidfield] == 'None' and wrong[nidfield] != 'None':
                DbFixer.delete_record(right, wrong, db = self.db)
            elif right[nidfield] != 'None' and wrong[nidfield] != 'None':
                DbFixer.substitute_composer(right, wrong, db = self.db)
            else:
                raise UndetectedDifference(idx, right, wrong)

    def fix_by_db(self):
        #
        # fix_by_db():
        #
        # this is done comparing directely the right csv with the db. Several
        # outcomes are possible:
        #
        #
        with open(self.right, 'r') as rfh:
            self.rightcsv = csv.reader(rfh)
            rdata = [l for l in self.rightcsv]
            for idx in range(len(rdata)):
                rarr = rdata[idx]
                record = obj.Record.from_csv(rarr)
                if record:
                    print("record exists:\n\t%s\n\t%s" % (record.to_csv(), str(rarr)))
                else:
                    print("record does NOT exist:\n\t%s" % (str(rarr)))

    @staticmethod
    def create_record(right, wrong, db = DbDev()):
        new_rec = obj.Record.from_csv(right)
        # new_rec.insert(db = db)

    @staticmethod
    def delete_record(right, wrong, db = DbDev()):
        old_rec = obj.Record.retrieve_from_csv(wrong)
        old_rec.delete(db = db)

    @staticmethod
    def substitute_composer(right, wrong, db=DbDev()):
        new_rec = obj.Record.from_csv(right)
        old_rec = obj.Record.retrieve_from_csv(wrong, db=db)
        old_rec.update_composer(new_rec.composer, db=db)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: %s <Provider name>" % (os.path.basename(sys.argv[0])), file=sys.stderr)
        sys.exit(-1)
    dbf = DbFixer(sys.argv[1])
    dbf.fix_by_csv()
