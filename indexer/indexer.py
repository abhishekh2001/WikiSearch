from collections import defaultdict
from nltk.tokenize import word_tokenize, sent_tokenize, regexp_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re


stops = set(stopwords.words('english'))


class Indexer:
    """Indexes the corpus using inverted indexing"""

    def __init__(self, fpath, content_parser):
        """Creates an inverted index from documents
        :param fpath: path to XML document containing corpus
        :param content_parser: parses document with custom formatting
        """
        self.index = defaultdict()
        self.fpath = fpath
        self.cur_content = None
        self.parser = content_parser
        self.titles = []
        self.doc = None
        self.stemmer = PorterStemmer(PorterStemmer.ORIGINAL_ALGORITHM)

    def parse_document(self, title, content):
        self.titles.append(title)
        self.cur_content = content
        field_data = self.parser.parse(content)
        for field, information in field_data.items():
            self.preprocess(information)
        # self.preprocess(content)

    def preprocess(self, data=None):
        """Performs all the text pre-processing for current content held"""
        data = self.tokenize(data)
        data = [t for t in data if t not in stops]
        data = self.stem(data)
        return data

    def tokenize(self, data):
        """Performs tokenization"""
        data = re.sub(r'[\'-]', '', data)
        data = re.sub(r'[^a-zA-z0-9]', ' ', data)
        return data.split()

    def cfold(self, data):
        """Performs case folding"""
        return [t.lower() for t in data]

    def remove_stop_words(self, data):
        """removes stop words"""
        return [t for t in data if t not in stops]

    def stem(self, data):
        """Performs stemming"""
        return [self.stemmer.stem(t) for t in data]
