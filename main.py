#!/usr/bin/env python

import sys
from greycode import Greycode

try:
    import web
except:
    print("[Warning] webpy is missing. Checkout webpy.org for installation")
    sys.exit(1)

# Set static URL for web app
urls = (
       '/(.*)', 'WebServer'
)

class WebServer:
    greycodeInst = Greycode()

    def GET(self, query):
        return self.greycodeInst.GET(query)

if __name__ == "__main__":
    
    app = web.application(urls, globals())
    app.run()
