import sys, os

test_file = 'test3.txt'
full_file = 'full_text.txt'
root_path = os.path.join(os.path.dirname(__file__), *(['..']*3))
repo_path = os.path.join(root_path, '..', 'Repo')
db_path = os.path.join(root_path, 'db', 'data')

sys.path.append(root_path)
