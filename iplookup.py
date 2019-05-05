#!/usr/bin/env python

# TODO
import re
from urllib2 import HTTPError

try:
    import requests
except:
    print("[Warning] requests is missing. You can install it by running: pip install requests.")
    sys.exit(1)

class IPlookup:

    def __init__(self,urls):
        for url in urls:
            # GET url
            response = requests.get(url)
            # Try to derive filename from header
            condisp = response.headers.get('content-disposition')
            if condisp:
                filename = re.findall('filename=(.+)', condisp)
            else:
                filename = url.rsplit('/',1)[1]
            open(filename, 'wb').write(response.content)

    def fetchList(self):
        pass

