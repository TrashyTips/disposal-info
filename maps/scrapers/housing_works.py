# -*- coding: utf-8 -*-
import re
import json
import time
import random
import collections

import requests
from bs4 import BeautifulSoup

class HousingWorksLocation():
	def __init__( self, name, address, hours, telephone, offerings, link ):
		self.name = name
		self.address = address
		self.hours = hours
		self.telephone = telephone
		self.offerings = offerings
		self.link = link

	def as_dict( self ):
		return dict(
			name = self.name,
			address = self.address,
			hours = self.hours,
			telephone = self.telephone,
			offerings = self.offerings,
			link = self.link
		)

	def __str__( self ):
		return '# %s\n%s\n%s' % (
			self.name,
			self.address,
			self.telephone
		)


# http://www.housingworks.org/donate/drop-off-donations/
def getLocations():
	r = requests.get('http://www.housingworks.org/donate/drop-off-donations/')
	if r.status_code != 200:
		raise RuntimeError( '%s' % r )
	
	soup = BeautifulSoup(r.text, 'html.parser')
	
	results = []
	
	locationsBlock = soup( text=re.compile(r'Drop off locations',re.IGNORECASE) )[0].parent.find_next_sibling('div')
	nextLocation = locationsBlock.find_next('a')
	while nextLocation:
		# Load the next location
		link = nextLocation.attrs['href']
		page = requests.get(link)
		if page.status_code != 200:
			raise RuntimeError( '%s' % page )

		# Parse the returned data and store it
		pageSoup = BeautifulSoup(page.text, 'html.parser')
		content = pageSoup.select_one('#primary')
		paragraphs = content.findAll('p')
		results.append( HousingWorksLocation(
			name = content.find('h2').getText(),
			address = content.find('h4').getText(),
			hours = paragraphs[0].getText(),
			telephone = paragraphs[1].getText().lower().replace('phone:','').strip(),
			offerings = paragraphs[2].getText().lower().replace('offerings:','').strip(),
			link = link
		) )
		
		# Find the next location
		nextLocation = nextLocation.find_next_sibling('a')

	return results


if __name__ == '__main__':
	def prettyJson( obj ):
		return json.dumps( obj, sort_keys=True, indent=2, separators=(',', ':') )

	rawJsonName = 'housing_works_raw.json'
	geoJsonName = 'housing_works_geo.json'

	def firstTime():
		results = getLocations()
	
		dictionaries = [ r.as_dict() for r in results ]
		with open( rawJsonName , 'wb' ) as f:
			f.write( prettyJson( dictionaries ) )
	
		print prettyJson( dictionaries )
	
	def secondTime():
		# If you've already downloaded the names/addresses
		with open( rawJsonName, 'rb' ) as f:
			data = json.loads( f.read() )

		from shared.geocode import toGeoJson

		geojson = toGeoJson( data, lambda x: x['address'] )
		with open( geoJsonName, 'wb' ) as f:
			f.write( prettyJson( geojson ) )

		print prettyJson( geojson )

	# Run one (or both)
	#firstTime()
	secondTime()
