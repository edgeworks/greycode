#!/usr/bin/env python


import sys, cgi, re
from vtlookup import VTlookup
from dbhandler import DBhandler

try:
    from IPy import IP
except:
    print("[Warning] IPy is missing. Checkout pypi.org/project/IPy for installation")
    sys.exit(1)

try:
    import web
except:
    print("[Warning] webpy is missing. Checkout webpy.org for installation")
    sys.exit(1)

try:
    import yaml
except:
    print("[Warning] PyYaml is missing. Checkout pyyaml.org for installation")
    sys.exit(1)


# Set static URL for web app
urls = (
       '/(.*)', 'greycode'
)

# Set static API key
# TODO import apikey from config
APIKEY = 'd619ab14fe99763cb8dd1822f5eca115fac5518153d87d3533bdf642fd89fec8'


class greycode:


    def __init__(self):
        
        # Read config greycode.yml
        with open('greycode.yml', 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

        self.apikey = cfg['virustotal']['apikey']
        self.apiurl = cfg['virustotal']['apiurl']
        self.dbsha256 = cfg['redisSHA256']
        self.database()

    # Handle URL input
    def GET(self, query):
        #Sanitize query
        query = cgi.escape(query)

        # Check if input is IP address
        try:
            ipvers = IP(query).version()
        except:
            pass
            # No action. Input is not an IP address
        else:
            # TODO Call checkIP
            if ipvers == 4:
                return "is ip"

        # Check if input is SHA256
        if re.match(r'([a-fA-F\d]{64})', query) == None:
            pass
            # No action. Input not an IP address
        else:
            # TODO Call checkSHA256
            return self.checkSHA256(query)
        
        # You should onyl land here if no input type was recognized. Return the bad news
        query += " is an unknown input"
        return query
    
    def database(self):
        newDBhandler = DBhandler(self.dbsha256)

    # Method to query IP blacklists
    # Returns
    #   - NO BLACKLIST ENTRY if no match
    #   - [NAME OF BLACKLIST] if matching an entry
    def checkIP(self, ip):
        # Create new iplookup object
        newIPlookup = iplookup()


    # Method to query virustotal.com with sha256 key
    # Returns 
    #   - GREEN if virustotal has no findings
    #   - RED if virustotal has at least one finding
    #   - UNKNOWN if virustotal doesn't recognize the hash
    #   - INPROGRESS if the answer is not ready right away
    def checkSHA256(self, sha256):
        # Create new vtlookup object and pass the API key from config
        newVTlookup = VTlookup(self.apikey, self.apiurl)
        return newVTlookup.getReport(sha256)



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
