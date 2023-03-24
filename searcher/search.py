from collections import defaultdict
from enum import Enum
import os
import bisect
import re
from searcher.compute_doclist import gen_v_doclist
import config
import Stemmer


def bsearch(w, wv):
    """Binary search for w in the list of words, wv
    :return: lower bound
    """
    loc = bisect.bisect_left(wv, w)
    if loc >= len(wv):
        return -1
    return loc - 1


class QUERYTYPE(Enum):
    FIELD_QUERY = 'fq'
    PLAIN = 'plain'


class Searcher:
    def __init__(self, q, wv, fd):
        """
        :param wv: vector of words in order of appearance in index files
        :param fd: location of final inv index folder
        """
        self.final_docs = fd
        self.stemmer = self.stemmer = Stemmer.Stemmer('english')
        self.wv = wv
        self.q = self.process_query_string(q)
        print('q: ', self.q)
        self.query_type = QUERYTYPE.PLAIN
        self.docRes = {} 

        if isinstance(self.q, dict):
            self.query_type = QUERYTYPE.FIELD_QUERY
    
    def get_doc_details(self, pos, target_w) -> list:
        """For word, get documents with scores"""
        if pos == -1:
            return []

        doc_scores = []
        target_v = None
        with open(os.path.join(self.final_docs, f"final{pos}.txt"), "r") as f:
            for l in f.readlines():
                w, v = l.strip().strip('\n').split(':')
                if w == target_w:
                    target_v = v
                    break
        if target_v is None:
            return dict()

        print('for w: ', target_w, ' found v: ', target_v[:30])
        print('q', self.q)
        return gen_v_doclist(target_v, self.q[target_w])


    def retrieve_doclist(self) -> list:
        """Generate relevant document list for the specified query
           :returns: list of relevant doc IDs
        """

        doc_scores = defaultdict(int)
        for w, f in self.q.items():
            if w == '':
                continue
            loc = bsearch(w, self.wv)
            doc_score = self.get_doc_details(loc, w)
            for id, sc in doc_score:
                doc_scores[id] += sc
        
        doc_ids = sorted(doc_scores.keys(), key=lambda x: doc_scores[x], reverse=True)
        return doc_ids[:10]


    def process_query_string(self, q):
        """Process rew string to create field query if required."""
        q = q.split(':')
        if len(q) == 1: 
            wv = self.pre_process(q[0])
            q  = {w: None for w in wv}
            return q

        """[t|i|b|r...] <-> [w1, w2... wn]"""
        res = {p[-1]: q[:-1] for p, q in zip(q[:-1], q[1:])}
        res = {k: self.pre_process(v) for k, v in res.items()}

        """w: [f1, f2...]"""
        ret = dict()
        for f, wv in res.items():
            for w in wv:
                if w in ret:
                    ret[w].add(f)
                else:
                    ret[w] = set([f])

        return ret

    def pre_process(self, data):
        data = data.lower()
        data = re.sub(r'https?://\S+|&nbsp|&lt|&gt|&amp|&quot|&apos|\S*\d\S*', '', data)
        data = re.sub(r'[^a-z]', ' ', data)
        data = self.tokenize(data)
        data = [t for t in data if t not in config.stops]
        data = self.stemmer.stemWords(data)
        return data

    def tokenize(self, data):
        data = data.split()
        data = [x for x in data if config.MINLEN <= len(x) <= config.MAXLEN]
        return data
