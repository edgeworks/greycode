#!/usr/bin/env python

import sys

try:
    import redis
except:
    print("[Warning] redis is missing. Try pip install redis or visit https://pypi.org/project/redis/")
    sys.exit(1)

class DBhandler:

    def __init__(self, dbconfig):

        self.databases = {}
        for database in dbconfig:
            self.databases[database['name']] = redis.StrictRedis(host=database['host'], port=database['port'], db=0)
            # Test each database instance
            try:
                self.databases[database['name']].ping()
            except redis.ConnectionError as e:
                print(" Cannot connect to database on host {0}:{1}".format(database['host'], database['port']))
                raise

    def readdb(self, dbname, key):
        try:
            return self.databases[dbname].get(key)
        except redis.ConnectionError as e:
            print (" Cannot connect to database ",dbname)
            raise
        

    def writedb(self, dbname, key, value):
        try:
            self.databases[dbname].set(key, value)
        except redis.ConnectionError as e:
            print (" Cannot connect to database ",dbname)
            raise
        
