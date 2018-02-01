# -*- coding: utf-8 -*-
import re
import json
import time
import random
import collections

import requests
from bs4 import BeautifulSoup

# https://satruck.org/DropOff/Index?zip=10704

class Location():

	@staticmethod
	def from_dict( data ):
		return Location(
			data['title'],
			data['address'],
			data['phone'],
			data['website'],
			data['hours']
		)

	def __init__( self, title, address, phone, website, hours ):
		self.title = title
		self.address = address
		self.phone = phone
		self.website = website
		self.hours = hours

	def as_dict(self):
		return dict(
			title = self.title,
			address = self.address,
			phone = self.phone,
			website = self.website,
			hours = self.hours
		)

	def __str__( self ):
		return '%s at %s' (self.title,self.address)

	# For creating a set
	def __hash__(self): return hash(self.title+self.address)
	def __eq__(self, other):
		return (
			self.title == other.title and
			self.address == other.address
		)
	def __ne__(self, other): return not self.__eq__( other )


def makeClass( name, properties ):
	return re.sub( re.compile( '^\t', re.M), '', '''
	class %s():
		def __init__( self, %s ):
			%s
		def as_dict( self ):
			return dict(
				%s
			)
	''') % (
		name,
		','.join(properties),
		'\n\t\t'.join([ 'self.%s = %s' % (p,p) for p in properties]),
		',\n\t\t\t'.join([ '%s = self.%s' % (p,p) for p in properties])
	)

print makeClass( 'Ball', 'x y z'.split(' ') )
exec( makeClass( 'Ball', 'x y z'.split(' ') ) )
ball = Ball( 1,2,3 )
print ball.as_dict()

exec( makeClass( '_Location', 'name id address phone type url lat lng'.split(' ') ) )

class Location( _Location ):
	
	@staticmethod
	def from_json( data ):
		return Location(
			data['Name'],
			data['Id'],
			''.join([ data['Address1'], ' ', data['Address2'], ', ', data['City'], ', ', data['State'], ' ', data['Zip'] ]),
			data['ContactPhone'],
			data['Type'],
			data['Website'],
			data['Latitude'],
			data['Longitude']
		)

	# For creating a set
	def __hash__(self): return hash(self.id)
	def __eq__(self, other):
		return (
			self.id == other.id
		)
	def __ne__(self, other): return not self.__eq__( other )

'''
"Latitude": 40.8023338,
"Longitude": -74.24842,
"Html": "<b>Salvation Army Donation Drop Box</b><br />270 Prospect Ave<br />W. Orange, NJ 07052<br />21.8 mi.",
"Id": "3774",
"Hours": "",
"Name": "Salvation Army Donation Drop Box",
"Address1": "270 Prospect Ave",
"Address2": "",
"City": "W. Orange",
"State": "NJ",
"Zip": "7052",
"Distance": "21.7730556099378",
"ContactPhone": "",
"Type": "2",
"TypeName": "DROPOFF",
"LocationGUID": "8b5d62a1-dcd1-4369-baad-6a0cbb1463a1",
"Website": "http://newark.satruck.org"
'''

'''
# Headers that firefox sends
headers = {
	'Host': 'satruck.org',
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'Accept-Language': 'en-US,en;q=0.5 --compressed',
	'DNT': '1',
	'X-Requested-With': 'XMLHttpRequest',
	'Referer': 'https://satruck.org/DropOff/Index?zip=10704',
	'Cookie': 'utag_main=v_id:0155cdaec0cc0016b872fd2025a40304c002b0090086e$_sn:1$_ss:1$_pn:1%3Bexp-session$_st:1468036429836$ses_id:1468034629836%3Bexp-session$_prevpage:undefined%3Bexp-1468038229847; ra_sess=ra_sess; cmTPSet=Y; CoreID6=53325612426514680346324&ci=51410000|SATruck; 51410000|SATruck_clogin=v=1&l=1468034632&e=1468036435770; _ga=GA1.2.1331802941.1468034633; __qca=P0-1472196357-1468034633318; _gat=1; CMAVID=none; st_session=0da31cfe-a695-470c-9bfd-146052e3e1fb!!1468034636071; st_state=37398fd6-4c26-4be8-ab43-30dbd7dcc49a@@0da31cfe-a695-470c-9bfd-146052e3e1fb!!1468034636071',
	'Connection': 'keep-alive'
}
'''

def getBinsForZip( zipCode ):
	r = requests.get( 'https://satruck.org/apiservices/pickup/donategoods/locations', params = {
		'Type': 3,
		'ZipCode': zipCode,
		'_': 1468034652269
	})
	if r.status_code != 200:
		raise RuntimeError( '%s' % r )

	locations = []
	for l in r.json()['RetVal']['Locations']:
		locations.append( Location.from_json( l ) )
	
	return locations

def _getBinsForZip( zipCode ):
	# We get a 403 if we don't use the User-Agent
	r = requests.get( 'https://satruck.org/DropOff/Index', params = {
		'zip': zipCode
	} )
	if r.status_code != 200:
		raise RuntimeError( '%s' % r )

	print r

	soup = BeautifulSoup(r.text, 'html.parser')

	divs = soup.select_one( '#drop-off-location-list' )#.select( '.has-website' )
	print divs

	def cleanSelectText( root, selector, default='' ):
		selection = root.select(selector)
		if len( selection ):
			return re.sub( '\\s+', ' ', selection[0].getText() ).strip()
		else:
			return default

	locations = []
	for d in divs:
		locations.append( Location(
			title = cleanSelectText(d,'.drop-off-location-title'),
			address = cleanSelectText(d,'.drop-off-location-address')+cleanSelectText(d,'.drop-off-location-city-state-zip'),
			phone = cleanSelectText(d,'.drop-off-location-phone'),
			website = cleanSelectText(d,'.drop-off-location-website'),
			hours = cleanSelectText(d,'.drop-off-location-hours')
		) )

	return locations

locs = getBinsForZip( 10704 )

sl = set(locs)
sl = sl.union( set(getBinsForZip( 11207 )) )

for x in sl:
	print x.as_dict()

def prettyJson( obj ):
	return json.dumps( obj, sort_keys=True, indent=2, separators=(',', ':') )

print prettyJson( [ x.as_dict() for x in sl ] )

if __name__ == '__main__':
	def getNY():
		from shared import zip_codes
		codes = zip_codes.getZipCodesForState('NY')
		#codes = [10704,11101,11207]
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
			except Exception as e:
				print e
			else:
				for x in zipResults:
					results.add( x )
				time.sleep( 1.0+random.random()*5.0 )

		dictionaries = [ s.as_dict() for s in results ]
		with open( 'salvation-army.json', 'wb' ) as f:
			f.write( prettyJson( dictionaries ) )

	# If no cached dataset
	def firstTime():
		getNY()

	def secondTime():
		with open( 'salvation-army.json', 'rb' ) as f:
			data = json.loads( f.read() )

		from shared.geocode import toGeoJsonWithLatLng

		geojson = toGeoJsonWithLatLng( data )
		with open( 'salvation-army-geo.json', 'wb' ) as f:
			f.write( prettyJson( geojson ) )

	secondTime()
