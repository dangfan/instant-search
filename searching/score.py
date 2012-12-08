import math
import redis

r = redis.StrictRedis()

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


#def score(result, query):
#    if len(result) == 0:
#        return []
#        # unchanged values during scoring
#    count = float(r.get('next_document_id'))
#    avgfl = float(r.get('total_len')) / count
#
#    pairs = map(lambda doc: (doc, reduce(
#        lambda x, y: x+y,
#        map(lambda q: score_single(doc, q.word, count, avgfl), query),
#        0
#    )), result)
#    return map(lambda t: t[0], sorted(pairs, key=lambda x:x[1], reverse=True))

def score():
    count = float(r.get('next_document_id'))
    avgfl = float(r.get('total_len')) / count
    words = map(lambda s: unicode(s, 'utf-8')[5:], r.keys(u'word:*'))
    for word in words:
        print word
        docs = r.zrange(u'word:%s'%word, 0, -1)
        for doc in docs:
            weight = score_single(doc, word, count, avgfl)
            r.zadd(u'word:%s'%word, weight, doc)

if __name__ == '__main__':
    score()