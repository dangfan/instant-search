import redis

r = redis.StrictRedis()

def suggest(keywords):
    return u'{"result": %s}' % do_query(keywords)

def add_query(query, weight = 1):
    for i in xrange(2, len(query)):
        r.zincrby(u'comp:'+query[:i], query, weight)

def do_query(prefix):
    return u'[%s]' % u', '.join(u'"%s"'%unicode(t, 'utf-8') for t in r.zrevrange(u'comp:'+prefix, 0, 5))