from xml.sax.handler import ContentHandler
import re
from collections import defaultdict


class WikipediaHandler(ContentHandler):
    """wikipedia XML for the SAX API"""

    def __init__(self, indexer):
        """SAX API parses doc and creates index
        :param indexer: implements the indexing functionality
        """
        print("init wiki content handler")
        self.reqd_tags = {"title", "text"}
        self.data = ""
        self.tag = ""
        self.doc_name = ""
        self.indexer = indexer

    def characters(self, content):
        if self.tag in self.reqd_tags:
            self.data += content

    def startElement(self, name, attrs):
        self.tag = name
        self.data = ""

    def endElement(self, name):
        print("name is actually", name)
        print(f"ending {self.tag}, data: {self.data}")
        if self.tag == 'title':
            self.doc_name = self.data
        if self.tag == 'text':  # TODO: consider page as end element
            self.indexer.parse_document(self.doc_name, self.data)


class WikipediaParser:
    """Parses content with wiki formatting"""

    def __init__(self):
        """parses data having wiki formatting"""
        self.content = None
        self.fields = {
            "body": self._body,
            "infobox": self._infobox,
            "category": self._category,
            "links": self._links,
            "references": self._references
        }

    def parse(self, content) -> dict:
        """Parses the wiki page and returns dictionary of fields and values
        :param content: string of wikipedia page
        :returns: (dict) keys of fields with values as field data
        """
        res = defaultdict()
        self.content = content

        for field, function in self.fields.items():
            res[field] = function()

        return res

    def _clean(self):
        """Sanitize response from wiki parsing"""
        pass

    def _body(self):
        return ""

    def _infobox(self):
        t = re.findall('({{infobox.*?}})', self.content)

        try:
            t = t[0]
        except IndexError:
            return ""

        t = re.split(r'\|.*?=', t)
        t = ' '.join(t[1:])
        return t

    def _category(self):
        t = re.findall(r'(\[\[category.*?]])', self.content)
        t = ' '.join([re.sub(r'\[\[category:|]', '', x) for x in t])
        return t

    def _links(self):
        # TODO: external links not in below format? look: we_3.txt IMP
        t = re.findall(r'\*\[.*?]', self.content)
        t = ' '.join(t)
        return t

    def _references(self):
        t = re.findall(r'&lt;ref.*?&lt;/ref', self.content)
        print('found refs ', t)
        t = [re.findall(r'title.*?\|', x) for x in t]
        t = [re.sub(r'title', ' ', x[0]) for x in t if len(x)]
        t = ' '.join(t)
        return t
