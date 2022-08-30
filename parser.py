import xml.etree.cElementTree as ElTree


class Parse:
    def __init__(self, xml_loc, indexer):
        """Parses entire xml file
        :param xml_loc: location of xml file
        :param indexer: object that parses document
        """
        self.loc = xml_loc
        self.indexer = indexer
        self._parse()

    def _parse(self):
        for ev, el in ElTree.iterparse(self.loc, events=('end',)):
            if ev != 'end':
                continue

            if 'page' not in el.tag:
                continue

            title, body = None, None
            for e in el:
                if 'title' in str(e):
                    title = e.text
                if 'revision' in str(e):
                    for c in e:
                        if 'text' in str(c):
                            body = c.text

            if 'wikipedia:' not in title and 'Category:' not in title:
                if body is None:
                    body = ""
                self.indexer.parse_document(title, body)
            el.clear()
