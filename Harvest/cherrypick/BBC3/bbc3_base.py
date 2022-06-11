import datetime as dt

class BBC3Base:

    __BBC_DATE_FORMATS__ = [ # used by the datetime.strptime() method
        "%a %b %d %H:%M:%S %z %Y",
        " %a %b %d %H:%M:%S %z %Y",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
    ]
    @staticmethod
    def process_date(date):
        """
            process_date(date) - class method

            tries hard to return a dt.datetime format from the string passed
            as an argument. The string can have different formats (all listed
            in BBC3Downloader.__BBC_DATE_FORMATS__) that must work with the
            datetime.strptime() function
        """
        result = None
        last_error = None
        if len(date) > 0:
            for bdf in BBC3Base.__BBC_DATE_FORMATS__:
                try:
                    result = dt.datetime.strptime(date, bdf)
                except ValueError as e:
                    last_error = "%s -> %s" % (date, e)
                    continue
        if not result:
            print("date \"%s\" does not generate a datetime. Raising a ValueError" % (date), file=sys.stderr)
            raise ValueError(last_error)
        return result

    @staticmethod
    def quantize_date(dtdate):
        """
            quantize_date(d)

            wants an argument in datetime.datetime format and it squashes
            the minutes and seconds to zero to it.

            FIXME: this could be adjusted to the actual real programming
            of BBC3, quantizing timings in an appropriate manner.
        """
        result = dt.datetime(dtdate.year,dtdate.month,dtdate.day,dtdate.hour,0)
        return result
