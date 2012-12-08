import json
from searching.analysis import Token
import redis

r = redis.StrictRedis()

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
    return u'{"title": "%s", "url": "%s", "text": "%s"}' % (title, url, text)


def collect(result, tokens, count):
    return u'{"count": %d, "result": [%s]}' % (count, u', '.join(generate_json(doc, tokens) for doc in result))