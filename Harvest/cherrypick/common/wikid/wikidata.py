import pdb
import sys, os
import requests
import re

mypath = os.path.join(os.path.dirname(__file__))
sys.path.extend([os.path.join(mypath, '..'), os.path.join(mypath, *(['..']*3))])

from db.db import Db
from common.objects import Composer
from wikid.sparql import sparql_composer

def cleanse_utf8(name):
    result = name 
    dash_re = re.compile('[-‐]')
    result = dash_re.sub('-', name)
    return result

WIKIDATA_API = "https://www.wikidata.org/w/api.php"

def do_request(params):
    data = None
    done = False
    while not done:
        try:
           data = requests.get(WIKIDATA_API,params=params)
           done = True
        except requests.exceptions.ConnectionError as e:
           print(e, file=sys.stderr)
    if data:
        data = data.json()
    return data

def retrieve_composer_slice(offset, params, cre):
    data = None
    desc = 'snippet'
    params['sroffset'] = offset
    data = do_request(params)
    res = None
    nid = None

    if 'query' in data and 'search' in data['query']:
        res = data['query']['search']
    if res and len(res)>0:
        for comp in res:
            if desc in comp and cre.search(comp[desc]):
                nid=comp['title']
                break
    return nid

def result_size(params):
    result = 0
    data = do_request(params)

    if 'query' in data and 'searchinfo' in data['query'] and 'totalhits' in data['query']['searchinfo']:
        result = data['query']['searchinfo']['totalhits']
    return result

__cache__ = {} # composers names get cached here

__RE_COMPOSER_DESCRIPTION__ = '(composer|compositor|compositeur|musician|pianist|violinist)'
def retrieve_composer(name):
    result=None
    nid=None #name id Q[...]
    query=cleanse_utf8(name)
    if query in __cache__:
        return __cache__[query]
    cre = re.compile(__RE_COMPOSER_DESCRIPTION__)
    offset = 0
    params = {
        "action" : "query",
        "format" : "json",
        "list"   : "search",
        "srsearch" : query, 
        "sroffset" : offset,
    }
    rsize = result_size(params)
    max_search = 30
    if rsize > max_search:
        rsize = max_search
    if rsize:
        while offset < rsize:
            nid = retrieve_composer_slice(offset, params, cre)
            if nid:
                result=sparql_composer(nid) #search in wikidata
                break
            offset += 10
    if not nid or not result:
        result=Composer(query, nid=nid)

    __cache__[query] = result
    return result
