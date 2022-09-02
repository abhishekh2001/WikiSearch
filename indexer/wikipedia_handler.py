from xml.sax.handler import ContentHandler
import re
from collections import defaultdict


class WikipediaHandler(ContentHandler):
    """wikipedia XML for the SAX API"""

    def __init__(self, indexer):
        """SAX API parses doc and creates index
        :param indexer: implements the indexing functionality
        """
        self.reqd_tags = {"title", "text"}
        self.data = ""
        self.tag = ""
        self.doc_name = ""
        self.indexer = indexer
        self.num_pages = 0

    def characters(self, content):
        if self.tag in self.reqd_tags:
            self.data += content

    def startElement(self, name, attrs):
        self.tag = name
        self.data = ""

    def endElement(self, name):
        if self.tag == 'title':
            self.doc_name = self.data
        if self.tag == 'text':
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
        self.content = content.lower()

        for field, function in self.fields.items():
            data = function()
            res[field] = data

        return res

    def _clean(self, data):
        """Sanitize response from wiki parsing"""
        data = re.sub(r'https?://\S+|&nbsp|&lt|&gt|&amp|&quot|&apos|\S*\d\S*', '', data)
        data = re.sub(r'[^a-z -]', ' ', data)
        return data

    def _body(self):
        t = re.sub(r'\{\{.*?}}|\[\[category.*?]]|==.*?==', ' ', self.content, flags=re.DOTALL)
        return t

    def _infobox(self):
        t = re.split(r'\{\{infobox', self.content)

        try:
            t = t[1].split('\n')
        except IndexError:
            return ""

        infobox = []
        for x in t:
            if re.search(r'^}}', x):
                break
            infobox.append(re.sub(r'\|.*?=', '', x))
        infobox = ' '.join(infobox)
        return infobox

    def _category(self):
        t = re.findall(r'(\[\[category.*?]])', self.content)
        t = ' '.join([re.sub(r'\[\[category:', '', x) for x in t])
        return t

    def _links(self):
        t = re.findall(r'==external links==.*?\n\n', self.content, flags=re.DOTALL)
        t = ' '.join(t)
        return t

    def _references(self):
        t = re.findall(r'&lt;ref&gt(.*?)?&lt;/ref', self.content, flags=re.DOTALL)
        t = ' '.join(t)
        return t
