import pdb
import sys, os
from db import DbDev

mypath = os.path.dirname(__file__)
sys.path.extend([mypath, os.path.join(mypath, '..', 'cherrypick')])

from common.objects.composer import ComposerComposer

if __name__ == '__main__':
    ComposerComposer.create_composer_composer_table()
