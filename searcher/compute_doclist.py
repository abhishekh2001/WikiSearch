import os
from collections import defaultdict
from math import log10
import re
import config


def gen_v_doclist(v, fields) -> list:
    """Given encoded index value, return list of docs and score"""
    vsplit = v.split('d')[1:][:100000]
    print(v[:30], vsplit[:2])
    res_docs = []
    for dv in vsplit:
        docid, docscore = compute_doc_vals(dv, fields, len(vsplit))
        res_docs.append([docid, docscore])
    return res_docs


def compute_doc_vals(v, fields, num_docs):
    """For a given word and information about that word in a document,
       compute tf-idf score"""
    cats = {'t', 'b', 'i', 'c', 'l', 'r'}
    cat_multiplier = {
        't': 1000,
        'i': 100,
        'b': 3,
        'c': 10,
        'l': 1,
        'r': 1
    }

    vs = re.split(r'([a-z])', v)
    docid = int(vs[0])
    vs = vs[1:]
    dets = defaultdict(int)


    for x in vs:
        if x in cats:
            cur_cat = x
        else:
            dets[cur_cat] = int(x)

    score = 0
    for f, v in dets.items():
        score += v * cat_multiplier[f]
    
    if fields is not None:
        for f in fields:
            score += dets[f] * cat_multiplier[f]

    score = log10(1 + score) * log10(config.TOT_ARTICLES / num_docs)

    return docid, score
