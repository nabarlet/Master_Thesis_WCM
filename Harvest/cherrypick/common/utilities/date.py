import sys, os
import re
import datetime as dt

def italian_date_conditioner(dd, m, yyyy):
    result = "%4d" % (int(yyyy))
    month_index = {
        'gennaio': 1,
        'febbraio': 2,
        'marzo': 3,
        'aprile': 4,
        'maggio': 5,
        'giugno': 6,
        'giungo': 6,   # record with typo
        'luglio': 7,
        'agosto': 8,
        'settembre': 9,
        'ottobre': 10,
        'novembre': 11,
        'dicembre': 12,
    }
    if m:
        result += "%02d" % (month_index[m])
    if dd:
        result += "%02d" % (int(dd))
    return result

def spanish_date_conditioner(date_string, day = 1, hour = 0, minutes = 0):
    date_string  = os.path.basename(date_string)
    stripped_ds = date_string.rstrip('.pdf') # remove suffix
    d_start = stripped_ds[-5:]
    month_index = {
       'ENE': 1,
       'FEB': 2,
       'MAR': 3,
       'ABR': 4,
       'MAY': 5,
       'JUN': 6,
       'JUL': 7,
       'AGO': 8,
       'SEP': 9,
       'OCT': 10,
       'NOV': 11,
       'DIC': 12
    }
    month = int(month_index[d_start[0:3]])
    year  = int('20' + d_start[3:])
    seconds = 0
    return dt.datetime(year, month, day, hour, minutes, seconds).isoformat()

def date(date_string):
    result = None
    if date_string:
        d_end = date_string.rindex('T00:00:00Z')
        result = dt.date.fromisoformat(date_string[0:d_end])
    return result

__RE_IS_A_DATE__ = re.compile('\A\d{4}-\d{2}-\d{2}')
def clean_datetime(datetime_string):
    """
        clean_datetime(datetime_string)

        checks whether the argument is a date (it might not be one, since
        Spotify does not use dates but rather playlist tags). If it is,
        it cleans and stadardized the output. If it is not, it returns the
        argument untouched.
    """
    result = datetime_string
    if __RE_IS_A_DATE__.search(datetime_string):
        datetime_string = datetime_string.rstrip('Z')
        t_idx = datetime_string.index('T')
        date_part = datetime_string[0:t_idx]
        time_part = datetime_string[t_idx+1:]
        result = date_part + ' ' + time_part
    return result
