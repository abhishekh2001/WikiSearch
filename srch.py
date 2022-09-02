from searcher.search import Searcher
import time
import random
import config
import sys
import os

INDEX_LOC = 'final'


def get_title(docid):
    floc = os.path.join(INDEX_LOC, f"title{docid // config.TITLES_PF}.txt")
    with open(floc, "r") as f:
        for i in range(docid % config.TITLES_PF + 1):
            t = f.readline()
    return t.strip('\n')


def retrieve_titles(docs):
    """Given docids, autofill to 10 and return titles"""
    while len(docs) < 10:
        nt = random.randint(3, config.TOT_ARTICLES - 3)
        if nt not in docs:
            docs.append(nt)

    titles = [get_title(d).lower() for d in docs]
    return docs, titles


if __name__ == '__main__':
    queries_loc = sys.argv[1]
    res_loc = 'queries_op.txt'
    stats_loc = 'stats.txt'

    with open(os.path.join(INDEX_LOC, 'stw.txt'), 'r') as f:
        stw = f.readlines()
    with open(queries_loc, "r") as f:
        queries = f.readlines()
    
    stw = [x.strip('\n') for x in stw]
    queries = [q.strip('\n') for q in queries]

    print(queries)

    for q in queries:
        s = Searcher(q, stw, INDEX_LOC)

        st = time.time()
        docs = s.retrieve_doclist()
        docs, titles = retrieve_titles(docs)
        en = time.time()

        print(titles)
        with open(res_loc, "a") as f:
            for d, t in zip(docs, titles):
                f.write(str(d) + ', ' + t + '\n')
            f.write(str(en - st) + '\n')
        print('docs: ', docs)
