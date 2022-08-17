import pdb
import unittest
import os, sys
sys.path.extend(['..', *['..']*2])
from rc_pick import RCPick

class TestDateProcessing(unittest.TestCase):

    def setUp(self):
        repo_dir = RCPick.__DEFAULT_RC_REPO_PATH__
        files_template = 'REVISTAABR%2d.pdf'
        path = os.path.join(repo_dir, file)
        self.rcp = RCPick(path)

    def test_extract_date(self):
        d = self.rcp.extract_date('Jueves 23        ', '07.00     ')
        self.assertTrue(d)
        self.assertEqual(d, '2021-04-23T07:00:00')

if __name__ == '__main__':
  unittest.main()
