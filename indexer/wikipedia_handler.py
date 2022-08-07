from xml.sax.handler import ContentHandler


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
        if self.tag == 'text':
            self.indexer.parse_document(self.doc_name, self.data)
