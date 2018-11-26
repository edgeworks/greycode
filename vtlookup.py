#!/usr/bin/env python

import sys, time, re
from urllib2 import HTTPError

try:
    import requests
except:
    print("[Warning] request module is missing. You can install it by running: pip install requests.")

# TODO Logging

class VTlookup:

    def __init__(self, apikey, apiurl):

        if apikey and apiurl:
            self.apikey = apikey
            self.apiurl = apiurl
        else:
            print("Please call this class with your VirusTotal API key and the API URL")
    
    def getReport(self, sha256):
		
		params = {'apikey':self.apikey, 'resource':sha256}
		
		try:
			response = requests.get(self.apiurl, params=params)
			response.raise_for_status()
		except requests.exceptions.HTTPError as statuscode:
			if statuscode == 204:
				print("[Error 204] Forbidden. You don't have enough privileges to make the request.")
			elif statuscode == 400:
				print("[Error 400]: Bad request. Your request was somehow incorrect. Check filehash or URL if modified")
			elif statuscode == 403:
				print("[Error 403]: Forbidden. You don't have enough privileges to make the request. Check your API key")
			elif statuscode == 404:
				print("[Error 404]: Service appears to be down. Check URL if modified")
			else:
				print("The HTTP Error Handler has been called. Submitted error number was: {0}".format(statuscode))
			return
		except requests.exceptions.MissingSchema as e:
			print(e)
			return
		except:
			print("Unknown error occured during request")
			print("The requested hash was: {0}".format(sha256))
			return
		else:
			# Check if queries are blocked. The public version of the API 
			# only allows limited amount of queries per minute and responds with a 204
			# if the limit is reached. If so, timeout for a minute and try again, n-times
			n = 15
			while (response.status_code == 204) and (n > 0):
				time.sleep(61)
				n = n-1
				print("Query for {0} is waiting. {1} attempts left".format(sha256,n))
				# Repeat query after timeout has finished
				response = requests.get(self.apiurl, params=params)

			return response.json()

