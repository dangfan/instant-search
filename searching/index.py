from analysis import analyze

class Index(object):
    """Object for reading and writing to the index.
    """

    @staticmethod
    def add_document(url, html):
        # A document is composed of 2 fields
        # url: the unique id of a doc
        # html: the html part
        title, words = analyze(html)
        #TODO: MORE WORK HERE

    @staticmethod
    def search(query):
        pass