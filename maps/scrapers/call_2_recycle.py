# http://www.call2recycle.org/locator/

# -*- coding: utf-8 -*-
import re
import json
import time
import random
import collections

import requests

import shared.geocode

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

exec( makeClass( '_Location', 'name id address phone lat lng hours accepts url moreInfoUrl'.split(' ') ) )
class Location( _Location ):

	@staticmethod
	def from_json( data ):
		return Location(
			data['name'],
			data['uid'],
			''.join([ data['address1'],  ', ', data['city'], ', ', data['state'], ' ', data['postalcode'] ]),
			data['phone'],
			data['latitude'],
			data['longitude'],
			'; '.join([
				'Mon: %s' % data['hoursmon'],
				'Tue: %s' % data['hourstues'],
				'Wed: %s' % data['hourswed'],
				'Thu: %s' % data['hoursthurs'],
				'Fri: %s' % data['hoursfri'],
				'Sat: %s' % data['hourssat'],
				'Sun: %s' % data['hourssun'],
			]),
			', '.join([
				'cellphones' if data['cellphones'] == 'Y' else '',
				'glasses' if data['glasses'] == 'Y' else '',
				'electronics' if data['consumerelectronics'] == 'Y' else '',
				'computers' if data['computers'] == 'Y' else '',
				'compact flourencent bulbs' if data['cfl'] == 'Y' else '',
				'ink/toner' if data['inktoner'] == 'Y' else '',
				'rechargeable batteries' if data['rechargeable'] == 'Y' else '',
				'singleuse batteries' if data['singleuse'] == 'Y' else ''
			]).replace(' ,',''),
			data['url'],
			data['sustainabilityurl']
		)

	# For creating a set
	def __hash__(self): return hash(self.id)
	def __eq__(self, other):
		return (
			self.id == other.id
		)
	def __ne__(self, other): return not self.__eq__( other )

def prettyJson( obj ):
	return json.dumps( obj, sort_keys=True, indent=2, separators=(',', ':') )

def getData( zipCode ):
	# Note: I use a large enough area that I only need to make 1 search
	r = requests.post('http://hosted.where2getit.com/call2recycle/2016/rest/locatorsearch?like=0.7480362424918481&lang=en_US', data = '{"request":{"appkey":"F410B884-0D42-11E0-8532-CCD7A858831C","formdata":{"geoip":false,"dataview":"store_default","limit":50000,"geolocs":{"geoloc":[{"addressline":"%s","country":"US","latitude":"","longitude":""}]},"searchradius":"1000","where":{"and":{"singleuse":{"eq":""},"rechargeable":{"eq":""},"cellphones":{"eq":""}}},"false":"0"}}}' % zipCode)

	if r.status_code != 200:
		raise RuntimeError( '%s' % r )

	stores = r.json()['response']['collection']
	locations = []
	for d in stores:
		#print prettyJson( d )
		locations.append( Location.from_json( d ) )

	return locations

if __name__ == '__main__':

	'''
	data = getData( 11207 )
	results = [x.as_dict() for x in data]
	print prettyJson( results )

	with open( 'call2recycle.json', 'wb' ) as f:
		f.write( prettyJson( results ) )

	shared.geocode.appendLatLngArray( results , lambda x: x['address'] )
	geojson = shared.geocode.toGeoJsonWithLatLng( results )

	with open( 'call2recycle-geo.json', 'wb' ) as f:
		f.write( prettyJson( geojson ) )
	'''

	with open( 'call2recycle-geo.json', 'rb' ) as fin:
		with open( 'call2recycle-geo-compressed.json', 'wb' ) as fout:
			fout.write( json.dumps( json.loads( fin.read() ) ) )
