from analysis import analyze, parse, stop_and_stem_seq
import redis
import json

r = redis.StrictRedis()

def get_doc_id(url):
    doc_id = r.incr('next_document_id')
    r.hset('documents', url, doc_id)
    return doc_id


def save_and_segment(doc_id, html, url):
    title, text, words = analyze(html)
    l = len(words)
    r.hmset('doc:%s'%doc_id, {'title': title, 'text': text, 'len': l, 'url': url})
    r.incrbyfloat('total_len', l)
    for token in words:
        r.zadd(u'word:%s'%token.word, token.weight, doc_id)
        r.hmset(u'dw:%s:%s:%s'%(doc_id, token.word, token.fieldname), {
            'pos': token.pos,
            'len': token.len,
            'weight': token.weight,
        })


def add_document(url, html):
    if r.hget('documents', url): return
    doc_id = get_doc_id(url)
    save_and_segment(doc_id, html, url)


def get_set(tokens):
    if len(tokens) == 0:
        return []
    r.zinterstore('temp_set', map(lambda t: u'word:%s' % t.word, tokens))
    return r.zrevrange('temp_set', 0, -1)


def search(query, page = 1, size=15):
    from searching.collect import collect, score
    tokens = stop_and_stem_seq(parse(query, ''))
    # try to get result from redis first
    key = u'cache:' + query
    if r.ttl(key) == -1:
        result = score(get_set(tokens), tokens)
        r.set(key, json.dumps(result))
        r.expire(key, 60)
    else:
        result = json.loads(r.get(key))
    result = collect(result[(page - 1)*size:page*size], tokens)
    return result
