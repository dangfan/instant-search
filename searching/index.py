from analysis import analyze, parse, stop_and_stem_seq
import redis

r = redis.StrictRedis()

def get_doc_id(url):
    doc_id = r.incr('next_document_id')
    r.hset('documents', url, doc_id)
    r.hset('urls', doc_id, url)
    return doc_id


def save_and_segment(doc_id, html):
    title, text, words = analyze(html)
    r.hmset('doc:%s'%doc_id, {'title': title, 'text': text})
    for token in words:
        r.zadd('word:%s'%token.word, token.weight, doc_id)
        r.hmset('dw:%s:%s:%s'%(doc_id, token.word, token.fieldname), {
            'pos': str(token.pos),
            'len': token.len,
        })


def add_document(url, html):
    if r.hget('documents', url): return
    doc_id = get_doc_id(url)
    save_and_segment(doc_id, html)


def search(query):
    tokens = stop_and_stem_seq(parse(query, ''))
    result = r.zinterstore('temp_set', map(lambda t: 'word:%s'%t.word, tokens))
    print result
