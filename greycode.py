#!/usr/bin/env python


import sys, cgi, re, vtlookup

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



# Set static URL for web app
urls = (
       '/(.*)', 'greycode'
)

# Set static API key
# TODO import apikey from config
APIKEY = 'd619ab14fe99763cb8dd1822f5eca115fac5518153d87d3533bdf642fd89fec8'


class greycode:

    def __init__(self):
        pass

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
            # TODO Call IP database
            if ipvers == 4:
                return "is ip"

        # Check if input is SHA256
        if re.match(r'([a-fA-F\d]{64})', query) == None:
            pass
            # No action. Input not an IP address
        else:
            # TODO Call SHA256 database or VT
            return "is sha256"
        
        # You should onyl land here if no input type was recognized. Return the bad news
        query += " is an unknown input"
        return query


    # Method to query virustotal.com with sha256 key
    # Returns 
    #   - GREEN if virustotal has no findings
    #   - RED if virustotal has at least one finding
    #   - UNKNOWN if virustotal doesn't recognize the hash
    #   - INPROGRESS if the answer is not ready right away
    def checkSHA256(self, sha256):
        # Create new vtlookup object and pass the API key from config
        newVTlookup = vtlookup(APIKEY)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
