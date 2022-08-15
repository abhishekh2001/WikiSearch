from collections import defaultdict, Counter
from nltk.tokenize import word_tokenize, sent_tokenize, regexp_tokenize
import time
import os
from os import path
from nltk.corpus import stopwords
import Stemmer
import re
import config


stops = set(stopwords.words('english'))


class Indexer:
    """Indexes the corpus using inverted indexing"""

    def __init__(self, content_parser, root_path=None):
        """Creates an inverted index from documents
        :param content_parser: parses document with custom formatting
        :param root_path: folder to store index files in
        """
        self.index = defaultdict()
        self.inv_index = defaultdict(list)
        self._file_id = 0
        self.doc_id = 0
        self._prev_doc_id = -1
        self.cur_content = None
        self.parser = content_parser
        self.titles = []
        self.doc = None
        self.stemmer = Stemmer.Stemmer('english')
        self.root_path = 'tmp/' if root_path is None else root_path
        self._prev_time = time.time()
        self.stemmed_words = dict()

        if not path.isdir(self.root_path):
            os.mkdir(self.root_path)

    def parse_document(self, title, content):
        self.titles.append(title.encode('ascii', errors='ignore').decode())
        self.cur_content = content.encode('ascii', errors='ignore').decode()

        field_data = self.parser.parse(content)
        for field, information in field_data.items():
            self.index[field] = self.preprocess(information)
        self.index['title'] = self.preprocess(title)
        self._make_index()
        self.index = defaultdict()

        self.doc_id += 1

        if self.doc_id % 30000 == 0:  # 20:55:18
            now = time.time()
            print('handling doc id', self.doc_id, ' time =', now - self._prev_time)
            self._prev_time = now
            self.dump()
            self._reset()

        self.index = defaultdict()
        self.cur_content = None

    def _reset(self):
        self.inv_index = defaultdict(list)
        self.titles = []

    def dump(self):
        if self.doc_id == self._prev_doc_id:
            return

        idx_content = []
        for w in sorted(self.inv_index.keys()):
            idx_content.append(w + ':' + ''.join(self.inv_index[w]))
        idx_content = '\n'.join(idx_content)

        with open(path.join(self.root_path, f'idx{self._file_id}.txt'), 'w') as f:
            f.write(idx_content)

        with open(path.join(self.root_path, f'title{self._file_id}.txt'), 'w') as f:
            f.write('\n'.join(self.titles))

        self._file_id += 1
        self._prev_doc_id = self.doc_id

    def _make_index(self):
        wffreq = defaultdict(lambda: defaultdict(int))  # word-field frequency
        for field, information in self.index.items():  # <title|infobox...>, list(tokens)
            for w, f in dict(Counter(information)).items():  # word, frequency
                wffreq[w][field[0]] = f

        for w in wffreq:
            value = 'd' + str(self.doc_id)
            for f, v in wffreq[w].items():  # field, value
                value += f+str(v)
            self.inv_index[w].append(value)

    def preprocess(self, data=None):
        """Performs all the text pre-processing for current content held"""
        data = self.tokenize(data)
        data = [t for t in data if t not in stops]
        data = self.stemmer.stemWords(data)
        return data

    def tokenize(self, data):
        """Performs tokenization"""
        data = data.split()
        data = [x for x in data if config.MINLEN <= len(x) <= config.MAXLEN]
        return data

    def stem(self, data):
        """Performs stemming"""
        return self.stemmer.stemWords(data)
        # return [self.stemmer.stem(t) for t in data]
