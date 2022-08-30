import sys
import config
import time
from parser import Parse
from indexer.wikipedia_handler import WikipediaHandler, WikipediaParser
from indexer.indexer import Indexer
from file_handling import combine


def run_et(docsrc, destination, stats_loc):
    wikiparser = WikipediaParser()
    idxr = Indexer(wikiparser, destination)
    p = Parse(docsrc, idxr)

    idxr.dump()
    idxr.write_stats(stats_loc)


if __name__ == '__main__':
    docsrc = sys.argv[1]
    destination = sys.argv[2]
    stats_loc = sys.argv[3]

    st = time.time()
    run_et(docsrc, config.INTER, stats_loc)
    en = time.time()
    print('Completed indexing in', (en - st))

    toks, fnum = combine.combine('final')

    print(f"Total tokens: {toks}, number of files: {fnum}")

   