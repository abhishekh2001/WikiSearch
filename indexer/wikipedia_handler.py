from xml.sax.handler import ContentHandler


class WikipediaHandler(ContentHandler):
    """wikipedia XML for the SAX API"""

    def __init__(self, indexer):
        """SAX API parses doc and creates index
        :param indexer: implements the indexing functionality
        """
        print("init wiki content handler")
        self.data = ""
        self.tag = "'"
        self.indexer = indexer

    def startDocument(self):
        print("Starting doc")

    def characters(self, content):
        self.data += content

    def startElement(self, name, attrs):
        self.tag = name
        self.data = ""

    def endElement(self, name):
        print("name is actually", name)
        print(f"ending {self.tag}, data: {self.data}")
