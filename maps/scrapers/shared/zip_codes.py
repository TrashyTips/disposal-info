# -*- coding: utf-8 -*-
import json

import requests
from bs4 import BeautifulSoup

# Zip code scraper
# replace `ny` with the abbreviation for the state
# http://www.unitedstateszipcodes.org/ny/

# JUST DOWNLOAD THE DATA:
# http://www.unitedstateszipcodes.org/zip-code-database/

def scrapeZipCodesForState( abbreviation ):
	# We get a 403 if we don't use the User-Agent
	r = requests.get(
		'http://www.unitedstateszipcodes.org/%s/' % abbreviation.lower(),
		headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate',
			'Connection': 'keep-alive'
		}
	)
	if r.status_code != 200:
		raise RuntimeError( '%s' % r )

	soup = BeautifulSoup(r.text, 'html.parser')
	
	table = soup.select( 'table' )[0]
	
	# Note the parsing is wrong, the table i need is not te first
	# table on the page
	print table
	
	codes = []
	for row in table.select('tr'):
		cell = row.select('td')[0]
		codes.append( cell.getText() )
	
	return codes

def prettyJson( obj ):
	return json.dumps( obj, sort_keys=True, indent=4, separators=(',', ':') )

def dbZipCodeForState( state ):
	import csv
	import os
	filepath = os.path.join( os.path.dirname(os.path.realpath(__file__)), 'zip_code_database.csv' )
	zipDb = csv.DictReader(open(filepath))
	codes = []
	for row in zipDb:
		if row['state'] == state:
			codes.append( row['zip'] )
	return codes

def getZipCodesForState( state ):
	return dbZipCodeForState( state )

nyZips = getZipCodesForState('NY')
print prettyJson( nyZips )

