import sys,os

mypath=os.path.dirname(__file__)
sys.path.append(os.path.join(mypath, *(['..']*2), 'cherrypick'))

from common.utilities.wcm_math import reverse_decile

def pop_zone(dataset):
    result = []
    decs = reverse_decile()
    for d in decs:
        result.append([])
    for pn in dataset:
        start = decs[0]
        cv = pn.popvalue
        if cv > 1.0:
            decs[start].append(pn)
            continue
        for idx,d in enumerate(decs[1:]):
            end = d
            if cv <= start and cv > end:
                result[idx+1].append(pn)
            start = end
    return result
