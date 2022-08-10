import pdb

import sys,os

mypath = os.path.dirname(__file__)

import datetime as dt
from dateutil.relativedelta import *
import requests

START_DATE = dt.date(2013, 4, 1)
END_DATE   = dt.date.today()
INCREMENT  = relativedelta(months=1)
ROOT_REPO  = os.path.join(mypath, *['..']*3, 'Repo', 'RadioC')

def date_to_title(date):
    months = [ None, 'ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC' ]
    year = date.year - 2000
    result = "REVISTA%s%d.pdf" % (months[date.month], year)
    return result

ROOT_URL = "https://www.rtve.es/rne/rc/programa/"
def runner():
    cur_date = START_DATE
    while (cur_date < END_DATE):
        filename = date_to_title(cur_date)
        filepath = os.path.join(ROOT_REPO, filename)
        if not os.path.exists(filepath):
            url = ROOT_URL + filename
            resp = requests.get(url)
            if resp.status_code == 200:
                with open(filepath, 'wb') as file:
                    print("... writing file %s" % (filename))
                    file.write(resp.content)
        cur_date += INCREMENT

if __name__ == '__main__':
    runner()
