#!/usr/bin/env python


import sys, cgi, re, json, thread
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

class greycode:

    def __init__(self):
        
        # Read config greycode.yml
        with open('greycode.yml', 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

        self.apikey = cfg['virustotal']['apikey']
        self.apiurl = cfg['virustotal']['apiurl']
        self.redissha256 = cfg['redisSHA256']
        self.redisip = cfg['redisIP']
        self.dbconfig = [self.redissha256, self.redisip]
        
        # Connect to databases
        self.dbhandler = self.database()

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
        try:
            return DBhandler(self.dbconfig)
        except:
            # Details on errors are logged by DBhandler. Add general comment only
            print("Connection Error with Redis database")
            sys.exit(1)

    # Method to query IP blacklists
    # Returns
    #   - NO BLACKLIST ENTRY if no match
    #   - [NAME OF BLACKLIST] if matching an entry
    def checkIP(self, ip):
        # Create new iplookup object
        newIPlookup = iplookup()


    # Method to check sha256 hash against Virustotal intel
    # Returns 
    #   - GREEN if virustotal has no findings
    #   - RED if virustotal has at least one finding
    #   - UNKNOWN if virustotal doesn't recognize the hash
    #   - QUERY IN PROGRESS if the answer is not ready right away
    def checkSHA256(self, sha256):

        # Check local database first
        verdict = self.dbhandler.readdb(self.redissha256['name'], sha256) 
        # Return local value if available
        # otherwise start lookup in the background and return "in progress"
        if verdict != None:
            return verdict
        else:
            # Start threaded Virustotal lookup in background
            thread.start_new_thread(self.threadedVTQuery, (sha256, ))
            return "QUERY IN PROGRESS"

    # Method to run virustotal queries threaded in the background
    def threadedVTQuery(self, sha256):
        # Create new vtlookup object and pass the API key and URL from config
        newVTlookup = VTlookup(self.apikey, self.apiurl)
        report = newVTlookup.getReport(sha256)
        report = json.dumps(report)
        report = json.loads(report)
        if (report['verbose_msg']) == 'Invalid resource, check what you are submitting':
            print('Invalid resource, check what you are submitting')
        elif (report['verbose_msg']) == 'The requested resource is not among the finished, queued or pending scans':
            self.dbhandler.writedb(self.redissha256['name'], sha256, 'UNKNOWN')
        elif (report['positives']) == 0:
            self.dbhandler.writedb(self.redissha256['name'], sha256, 'GREEN')
        else:
            self.dbhandler.writedb(self.redissha256['name'], sha256, 'RED')



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
