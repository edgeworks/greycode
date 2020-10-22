#!/usr/bin/env python


class Test:

    def __init__(self):
        print('init done')

    def GET(self, query):
        print(query)
        return 'Hello World'