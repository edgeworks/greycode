#!/usr/bin/env python

try:
    import yaml
except:
    print("[Warning] PyYaml is missing. Checkout pyyaml.org for installation")
    sys.exit(1)


# TODO get this from config
# Should not be modified unless changes in VirusTotal API
APIURL = 'https://www.virustotal.com/vtapi/v2/file/report'

class VTlookup:

    def __init__(self, apikey, apiurl):

        if apikey and apiurl:
            self.apikey = apikey
            self.apiurl = apiurl
        else:
			# TODO Logging
            print("Please call this class with your VirusTotal API key and the API URL")
    
    def getReport(self, sha256):
        return self.apikey
 
