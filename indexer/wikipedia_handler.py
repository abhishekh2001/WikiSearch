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
        print(content)

        for field, function in self.fields.items():
            res[field] = function()

        return res

    def _body(self):
        return ""

    def _infobox(self):
        return ""

    def _category(self):
        return ""

    def _links(self):
        return ""

    def _references(self):
        return ""
