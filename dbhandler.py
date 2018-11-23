#!/usr/bin/env python

import redis

class dbhandler:

    def __init__(self):
        self.redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.redis_db = redis.StrictRedis(host='localhost', port=6379, db=1)

    def getValue(self, key, db)
        
