# -*- coding: utf-8 -*-
import re
import json
import time
import random
import collections

import requests
from bs4 import BeautifulSoup

# http://www.usagain.com/find-a-collection-bin
# Post with data:
# cityInput=&stateInput=%23&zipInput=11207&Submit.x=48&Submit.y=4

class BinLocation():

	@staticmethod
	def from_dict( data ):
		return BinLocation(
			data['name'],
			data['address']
		)

	def __init__( self, name, address ):
		self.name = name
		self.address = address

	def as_dict( self ):
		return dict(
			name = self.name,
			address = self.address
		)

	# For creating a set
	def __hash__(self): return hash(self.name+self.address)
	def __eq__(self, other):
		return (
			self.name == other.name and
			self.address == other.address
		)
	def __ne__(self, other): return not self.__eq__( other )

def getBinsForZip( zipCode ):
	# We get a 403 if we don't use the User-Agent
	r = requests.post(
		'http://www.usagain.com/find-a-collection-bin',
		data = {
			'cityInput': '',
			'stateInput': '#',
			'zipInput': zipCode,
			'Submit.x': 0,
			'Submit.y': 4
		}
	)
	if r.status_code != 200:
		raise RuntimeError( '%s' % r )

	soup = BeautifulSoup(r.text, 'html.parser')
	
	table = soup.find_all( 'table', attrs={
		'summary': 'USAgain Collection Sites'
	} )[0].select('tbody')[0]

	locations = []
	for row in table.select('tr'):
		name = re.sub( '\\s+', ' ', row.select('th')[0].getText() ).strip()
		address = re.sub( '\\s+', ' ', row.select('td')[0].getText() ).strip()
		locations.append( BinLocation(name,address) )

	return locations

if __name__ == '__main__':

	def prettyJson( obj ):
		return json.dumps( obj, sort_keys=True, indent=2, separators=(',', ':') )

	def getBinsNY():
		import zip_codes
		codes = zip_codes.getZipCodesForState('NY')
		results = set()
		for i in range(len(codes)):
			print 'Checking %s [%s of %s], total results: %s' % (
				codes[i],
				i,
				len(codes),
				len(results)
			)

			try:
				zipResults = getBinsForZip( codes[i] )
				#print prettyJson( [ b.as_dict() for b in zipResults ] )
			except Exception as e:
				print e
			else:
				#results.extend( zipResults )
				for x in zipResults:
					results.add( x )
				time.sleep( 1.0+random.random()*5.0 )

		'''
		print 'Found %s results total' % len( results )
		sResults = set( results )
		print 'Found %s unique results' % len(sResults)
		'''

		dictionaries = [ s.as_dict() for s in results ]
		with open( 'usagain-bins.json', 'wb' ) as f:
			f.write( prettyJson( dictionaries ) )

	# If no cached dataset
	def firstTime():
		getBinsNY()

	def secondTime():
		# If you've already downloaded the names/addresses
		with open( 'usagain-bins.json', 'rb' ) as f:
			bins = json.loads( f.read() )

		from shared.geocode import toGeoJson

		geojson = toGeoJson( bins, lambda x: x['address'] )
		with open( 'usagain.geojson', 'wb' ) as f:
			f.write( prettyJson( geojson ) )

	# Run one (or both)
	#firstTime()
	#secondTime()

