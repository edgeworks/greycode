#!/usr/bin/env python

import redis

class DBhandler:

    def __init__(self, dbconfig):
        for database in dbconfig:
            self.databases.append(redis.StrictRedis(host=database['host'], port=database['port'], db=0))

    def readdb(self, database, key)
        pass

    def write(self, database, key, value)
        pass
        
