from collections import defaultdict


class Indexer:
    """Indexes the corpus using inverted indexing"""

    def __init__(self, fpath, parser):
        """Creates an inverted index from XML document
        :param fpath: path to XML document containing corpus
        :param parser: object implementing xml parsing
        """
        self.index = defaultdict()
        self.parser = parser
        self.fpath = fpath
        self.doc = None

    def parse(self):
        """Parses the corpus"""
        pass

    def tokenize(self, t):
        """Performs tokenization"""
        pass

    def cfold(self, t):
        """Performs case folding"""
        pass

    def remove_stop_words(self, t):
        """removes stop words"""
        pass

    def stem(self, t):
        """Performs stemming"""
        pass
