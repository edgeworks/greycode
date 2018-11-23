#!/usr/bin/env python

# TODO get this from config
# Should not be modified unless changes in VirusTotal API
APIURL = 'https://www.virustotal.com/vtapi/v2/file/report'

class vtlookup:

    def __init__(self, apikey):

        if apikey:
            self.apikey = apikey
            print("vt")
        else:
			# TODO Logging
            print("Please call this class with your VirusTotal API key")

 
