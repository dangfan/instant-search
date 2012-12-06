import re
from stemming.porter2 import stem
import jieba
from stop import STOP_WORDS

class Token(object):
    def __init__(self, word, fieldname, pos, len, weight):
        self.word = word
        self.fieldname = fieldname
        self.pos = pos
        self.len = len
        self.weight = weight


def parse(text, fieldname):
    set = {}
    seg_list = jieba.cut_for_search(text)
    for w, p in seg_list:
        if w in set:
            c, pos = set[w]
            c += 1
            pos.append(p)
        else:
            c, pos = 1, [p]
        set[w] = (c, pos)
    return [Token(word=w, fieldname=fieldname, pos=p, len=len(w), weight=c) for (w, (c, p)) in set.iteritems()]


def clean_html(html):
    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(ur"(?is)<(script|style).*?>.*?(</\1>)", u"", html.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(ur"(?s)<!--(.*?)-->[\n]?", u"", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(ur"(?s)<.*?>", u" ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(ur"&nbsp;", u" ", cleaned)
    cleaned = re.sub(ur"  ", u" ", cleaned)
    cleaned = re.sub(ur"  ", u" ", cleaned)
    return u' '.join(cleaned.split())


def extract_text(html):
    title_search = re.search(ur'<title>(.*)</title>', html, re.IGNORECASE)
    title = title_search.group(1) if title_search else u''
    text = clean_html(html)
    return text, title


def tokenize(text, title):
    tokens_title = parse(title, u'title')
    tokens_text = parse(text, u'text')
    tokens = tokens_title + tokens_text
    return tokens


def stop_and_stem(token):
    word = stem(token.word).lower()
    if len(word) == 1 or word in STOP_WORDS:
        return None
    token.word = word
    return token


def stop_and_stem_seq(seq):
    return filter(None, map(stop_and_stem, seq))


def analyze(html):
    text, title = extract_text(html)
    tokens = tokenize(text, title)
    return title, text, stop_and_stem_seq(tokens)
