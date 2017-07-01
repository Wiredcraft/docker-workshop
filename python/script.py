#!/usr/bin/env python
import redis

db = redis.StrictRedis()

before = db.info().get('db0', {}).get('keys', 0)
db.set('toto', 'toto')
after = db.info().get('db0', {}).get('keys', 0)
print 'before: %s\nafter: %s' % (before, after)
