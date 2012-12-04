from bs4 import BeautifulSoup

class Word(object):
    def __init__(self, word, fieldname, pos):
        self.word = word
        self.fieldname = fieldname
        self.pos = pos

def analyze(html):
    soup = BeautifulSoup(html)
    title = soup.title.string
    text = soup.get_text()
    return title