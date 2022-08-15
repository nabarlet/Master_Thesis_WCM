import sys,os

import csv

if len(sys.argv) < 2:
    printf("Usage: %s <csv file>" % sys.argv[0], file=sys.stderr)
    exit(-1)

file = sys.argv[1]

lineno = 0
FIELDS_SHOULD_BE = 17
with open(file, 'r') as fh:
    csvr = csv.reader(fh, delimiter=',', quotechar='"')
    for row in csvr:
        lineno += 1
        l = len(row)
        if l != FIELDS_SHOULD_BE:
            print("%d: len -> %d" % (lineno, l), file=sys.stderr)
