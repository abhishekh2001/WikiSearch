from collections import defaultdict, Counter
import re
from nltk.tokenize import word_tokenize, sent_tokenize, regexp_tokenize
import time
import os
from os import path
import Stemmer
import config


stops = {"couldn't", 'them', 'if', 'off', 'not', "needn't", 'ours', 'had', 'now', 'don', 'have', "won't", 'has', 'shan', 'isn', 'any', 'at', 'no', 'an', 'mightn', 'who', 'is', 'doing', 'a', 'there', 'of', 'before', 'do', 'up', 'shouldn', 'all', 'couldn', 'so', 'they', 'such', 'which', 'aren', "haven't", 'against', 'she', 'both', 'during', 'y', "didn't", 'yours', 'more', 'further', 'itself', 'yourselves', 'on', 'should', 'haven', 'over', 't', 'how', 'are', 'its', 'when', 'some', 'own', "she's", "should've", 'down', 'why', 'under', 's', 'your', 'his', 'each', "hadn't", 'ourselves', 'above', 'can', 'then', 'won', "doesn't", "hasn't", 'in', 'he', 'didn', 'again', 'the', 'hers', 'herself', "that'll", "you'll", 'most', 'being', 'i', 'theirs', "you're", "wouldn't", 'few', 'to', 'through', 'from', 'himself', 'myself', 'you', 'our', 'doesn', 'between', 'until', 'd', 'my', 'those', 'o', 'because', 'once', "you'd", "aren't", 'that', 'just', 'were', 'here', 'their', 'weren', 'am', "shan't", 'it', 'what', 'and', 'hasn', 'by', 'with', 'very', 'same', 've', 'this', 'whom', 'these', 'too', 'm', "shouldn't", 'wasn', 'than', 'was', "isn't", 'mustn', "weren't", 'ain', 'having', 'ma', 'but', "it's", 'been', 'out', 'nor', 'while', 'me', 'we', "wasn't", 're', 'needn', 'into', "mustn't", 'hadn', 'or', "mightn't", 'will', 'be', 'themselves', 'him', "you've", 'does', 'for', 'as', 'after', 'where', 'about', 'other', 'wouldn', 'below', "don't", 'll', 'yourself', 'only', 'did', 'her'}


class Indexer:
    """Indexes the corpus using inverted indexing"""

    def __init__(self, content_parser, root_path=None, final_path=None):
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
        self.target = 'final/' if final_path is None else final_path
        self._prev_time = time.time()
        self._tot_tokens, self._inv_tokens = 0, 0
        self.stemmed_words = dict()

        if not path.isdir(self.root_path):
            os.mkdir(self.root_path)

    def parse_document(self, title, content):
        self.titles.append(title.encode('ascii', errors='ignore').decode())
        self.cur_content = content.encode('ascii', errors='ignore').decode()

        field_data = self.parser.parse(self.cur_content)
        for field, information in field_data.items():
            self.index[field] = self.preprocess(information)
            self._tot_tokens += len(self.index[field])
        
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

    def write_stats(self, fname):
        with open(fname, 'w') as f:
            f.write(str(self._tot_tokens)+'\n'+str(self._inv_tokens))

    def _reset(self):
        self.inv_index = defaultdict(list)
        self.titles = []

    def dump(self):
        if self.doc_id == self._prev_doc_id:
            return

        idx_content = []
        for w in sorted(self.inv_index.keys()):
            idx_content.append(w + ':' + ''.join(self.inv_index[w]))
            self._inv_tokens += 1
        idx_content = '\n'.join(idx_content)

        with open(path.join(self.root_path, f'idx{self._file_id}.txt'), 'w') as f:
            f.write(idx_content)

        with open(path.join(self.target, f'title{self._file_id}.txt'), 'w') as f:
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
        data = data.lower()
        data = re.sub(r'https?://\S+|&nbsp|&lt|&gt|&amp|&quot|&apos|\S*\d\S*', '', data)
        data = re.sub(r'[^a-z]', ' ', data)
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
