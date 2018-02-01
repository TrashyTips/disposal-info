# -*- coding: utf-8 -*-
import re
import json
import time
import random
import collections

import requests

# http://goodcleantech.pcmag.com/recycling/279662-the-goodcleantech-electronics-recycling-superguide
# http://storelocator.staples.com/stores.json?latitude=40.6655101&longitude=-73.8918897&radius=1000&locale=en_US&offset=0&limit=2000

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

exec( makeClass( '_Location', 'name id address phone lat lng hours'.split(' ') ) )
class Location( _Location ):

	@staticmethod
	def from_json( data ):
		return Location(
			data['storeTitle'],
			data['storeNumber'],
			''.join([ data['address']['addressLine1'],  ', ', data['address']['city'], ', ', data['address']['state'], ' ', data['address']['zipcode'] ]),
			data['address']['phoneNumber'],
			data['latitude'],
			data['longitude'],
			data['workingHourVOs']
		)

	# For creating a set
	def __hash__(self): return hash(self.id)
	def __eq__(self, other):
		return (
			self.id == other.id
		)
	def __ne__(self, other): return not self.__eq__( other )

def getData(  ):
	r = requests.get( 'http://storelocator.staples.com/stores.json', params = {
		'latitude': 40.6655101,
		'longitude': -73.8918897,
		'radius': 1000,
		'locale': 'en_US',
		'offset': 0,
		'limit': 2000
	})
	if r.status_code != 200:
		raise RuntimeError( '%s' % r )
	
	stores = r.json()['results']['stores']
	locations = []
	for d in stores:
		locations.append( Location.from_json( d ) )

	return locations

from shared.geocode import toGeoJsonWithLatLng
data = getData()
geojson = toGeoJsonWithLatLng( [ d.as_dict() for d in data ] )
def prettyJson( obj ):
	return json.dumps( obj, sort_keys=True, indent=2, separators=(',', ':') )
with open( 'staples-geo.json', 'wb' ) as f:
	f.write( prettyJson( geojson ) )
