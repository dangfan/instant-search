import json
import math
from searching.analysis import Token
from searching.index import r

def bm25(idf, tf, fl, avgfl, B=0.5, K1=1.2):
    # idf - inverse document frequency
    # tf - term frequency in the current document
    # fl - field length in the current document
    # avgfl - average field length across documents in collection
    # B, K1 - free paramters
    return idf * ((tf * (K1 + 1)) / (tf + K1 * ((1 - B) + B * fl / avgfl)))


def score_single(document, query, count, avgfl):
    # get information for bm25
    doc = r.hgetall('doc:%s'%document)
    token_title = r.hgetall(u'dw:%s:%s:title'%(document, query))
    token_text = r.hgetall(u'dw:%s:%s:text'%(document, query))
    weight_title = 0 if 'weight' not in token_title else float(token_title['weight'])
    weight_text = 0 if 'weight' not in token_text else float(token_text['weight'])

    fl = float(doc['len'])
    idf = 1+math.log(count / r.zcard(u'word:%s'%query), 10)
    tf = (weight_title * 2.0 + weight_text * 1.0) / fl
    return bm25(idf, tf, fl, avgfl)


def score(result, query):
    # unchanged values during scoring
    count = float(r.get('next_document_id'))
    avgfl = float(r.get('total_len')) / count

    pairs = map(lambda doc: (doc, reduce(
        lambda x, y: x+y,
        map(lambda q: score_single(doc, q.word, count, avgfl), query),
        0
    )), result)
    return map(lambda t: t[0], sorted(pairs, key=lambda x:x[1], reverse=True))


def highlight(text, tokens, trim):
    positions = map(lambda t: (t.pos[0], t.pos[0]+t.len), tokens)
    positions = sorted(positions)
    result = u''
    start = 0
    for s, t in positions:
        if trim and s - start > 20:
            prefix = (text[start:start+10] if start else u'') + u'...' + text[s-10:s]
        else:
            prefix = text[start:s]
        result += prefix + u'<span class="match">%s</span>' % text[s:t]
        start = t
    suffix = text[start:]
    if trim and len(suffix) > 10:
        suffix = suffix[:10] + u'...'
    result += suffix
    return result


def get_original_token(doc, term, fieldname):
    token = r.hgetall(u'dw:%s:%s:%s'%(doc, term, fieldname))
    if token:
        return Token(word=term, fieldname=fieldname, pos=json.loads(token['pos']), len=int(token['len']), weight=int(token['weight']))
    return None


def generate_json(document, tokens):
    doc = r.hgetall('doc:%s'%document)
    url = unicode(doc['url'], 'utf-8')
    title = unicode(doc['title'], 'utf-8')
    text = unicode(doc['text'], 'utf-8')
    title_tokens = filter(None, map(lambda t: get_original_token(document, t.word, u'title'), tokens))
    text_tokens = filter(None, map(lambda t: get_original_token(document, t.word, u'text'), tokens))
    title = highlight(title, title_tokens, trim=False)
    text = highlight(text, text_tokens, trim=True)
    return u"{title: '%s', url: '%s', text: '%s'}" % (title, url, text)


def collect(result, tokens):
    return u'[%s]' % u', '.join(generate_json(doc, tokens) for doc in result)