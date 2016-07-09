# -*- coding: utf-8 -*-
import re
import json
import time
import random
import collections

import requests
from bs4 import BeautifulSoup
import xmltodict

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
			data['name'],
			data['uid'],
			''.join([ data['address1'],  ', ', data['city'], ', ', data['state'], ' ', data['postalcode'] ]),
			data['phone'],
			data['latitude'],
			data['longitude'],
			'; '.join([
				'sun: %s' % data['sun'],
				'mon: %s' % data['mon'],
				'tues: %s' % data['tues'],
				'wed: %s' % data['wed'],
				'thur: %s' % data['thur'],
				'fri: %s' % data['fri'],
				'sat: %s' % data['sat']
			])
		)

	# For creating a set
	def __hash__(self): return hash(self.id)
	def __eq__(self, other):
		return (
			self.id == other.id
		)
	def __ne__(self, other): return not self.__eq__( other )

# http://www.officedepot.com/a/promo/pages/0928_recycling/
# http://storelocator.officedepot.com/ajax?&xml_request=%3Crequest%3E%3Cappkey%3EAC2AD3C2-C08F-11E1-8600-DCAD4D48D7F4%3C%2Fappkey%3E%3Cformdata+id%3D%22locatorsearch%22%3E%3Cdataview%3Estore_default%3C%2Fdataview%3E%3Climit%3E250%3C%2Flimit%3E%3Cgeolocs%3E%3Cgeoloc%3E%3Caddressline%3E10704%3C%2Faddressline%3E%3Clongitude%3E-73.89188969999998%3C%2Flongitude%3E%3Clatitude%3E40.6655101%3C%2Flatitude%3E%3C%2Fgeoloc%3E%3C%2Fgeolocs%3E%3Csearchradius%3E20|35|50|100|250%3C%2Fsearchradius%3E%3Cwhere%3E%3Cor%3E%3Cnowdocs%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fnowdocs%3E%3Cexpanded_furn%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fexpanded_furn%3E%3Cusps%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fusps%3E%3Cshredding%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fshredding%3E%3Cselfservews%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fselfservews%3E%3Cphotoprint%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fphotoprint%3E%3Cexpandedbb%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fexpandedbb%3E%3Cprinting3d%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fprinting3d%3E%3Clisteningstation%3E%3Ceq%3E%3C%2Feq%3E%3C%2Flisteningstation%3E%3Ccellphonerepair%3E%3Cin%3E%3C%2Fin%3E%3C%2Fcellphonerepair%3E%3C%2For%3E%3Cicon%3E%3Ceq%3E%3C%2Feq%3E%3C%2Ficon%3E%3C%2Fwhere%3E%3C%2Fformdata%3E%3C%2Frequest%3E
# Uses xmltodict - https://github.com/martinblech/xmltodict

'''
params = {
		#'xml_request': '<request><appkey>AC2AD3C2-C08F-11E1-8600-DCAD4D48D7F4</appkey><formdata+id="locatorsearch"><dataview>store_default</dataview><limit>250</limit><geolocs><geoloc><addressline>%s</addressline></geoloc><geolocs><searchradius>20|35|50|100|250</searchradius><where><or><nowdocs><eq></eq></nowdocs><expanded_furn><eq></eq></expanded_furn><usps><eq></eq></usps><shredding><eq></eq></shredding><selfservews><eq></eq></selfservews><photoprint><eq></eq></photoprint><expandedbb><eq></eq></expandedbb><printing3d><eq></eq></printing3d><listeningstation><eq></eq></listeningstation><cellphonerepair><in></in></cellphonerepair></or><icon><eq></eq></icon></where></formdata></request>' % zipCode
		#'xml_request':'<request><appkey>AC2AD3C2-C08F-11E1-8600-DCAD4D48D7F4</appkey><formdata+id="locatorsearch"><dataview>store_default</dataview><limit>250</limit><geolocs><geoloc><addressline>11207</addressline><longitude>-73.89188969999998</longitude><latitude>40.6655101</latitude></geoloc></geolocs><searchradius>20|35|50|100|250</searchradius><where><or><nowdocs><eq></eq></nowdocs><expanded_furn><eq></eq></expanded_furn><usps><eq></eq></usps><shredding><eq></eq></shredding><selfservews><eq></eq></selfservews><photoprint><eq></eq></photoprint><expandedbb><eq></eq></expandedbb><printing3d><eq></eq></printing3d><listeningstation><eq></eq></listeningstation><cellphonerepair><in></in></cellphonerepair></or><icon><eq></eq></icon></where></formdata></request>'
		'xml_request':'%3Crequest%3E%3Cappkey%3EAC2AD3C2-C08F-11E1-8600-DCAD4D48D7F4%3C%2Fappkey%3E%3Cformdata+id%3D%22locatorsearch%22%3E%3Cdataview%3Estore_default%3C%2Fdataview%3E%3Climit%3E250%3C%2Flimit%3E%3Cgeolocs%3E%3Cgeoloc%3E%3Caddressline%3E10704%3C%2Faddressline%3E%3Clongitude%3E-73.89188969999998%3C%2Flongitude%3E%3Clatitude%3E40.6655101%3C%2Flatitude%3E%3C%2Fgeoloc%3E%3C%2Fgeolocs%3E%3Csearchradius%3E20|35|50|100|250%3C%2Fsearchradius%3E%3Cwhere%3E%3Cor%3E%3Cnowdocs%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fnowdocs%3E%3Cexpanded_furn%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fexpanded_furn%3E%3Cusps%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fusps%3E%3Cshredding%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fshredding%3E%3Cselfservews%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fselfservews%3E%3Cphotoprint%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fphotoprint%3E%3Cexpandedbb%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fexpandedbb%3E%3Cprinting3d%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fprinting3d%3E%3Clisteningstation%3E%3Ceq%3E%3C%2Feq%3E%3C%2Flisteningstation%3E%3Ccellphonerepair%3E%3Cin%3E%3C%2Fin%3E%3C%2Fcellphonerepair%3E%3C%2For%3E%3Cicon%3E%3Ceq%3E%3C%2Feq%3E%3C%2Ficon%3E%3C%2Fwhere%3E%3C%2Fformdata%3E%3C%2Frequest%3E'
	}
'''

def getDataForZipCode( zipCode ):
	r = requests.get( 'http://storelocator.officedepot.com/ajax?&xml_request=%3Crequest%3E%3Cappkey%3EAC2AD3C2-C08F-11E1-8600-DCAD4D48D7F4%3C%2Fappkey%3E%3Cformdata+id%3D%22locatorsearch%22%3E%3Cdataview%3Estore_default%3C%2Fdataview%3E%3Climit%3E250%3C%2Flimit%3E%3Cgeolocs%3E%3Cgeoloc%3E%3Caddressline%3E10704%3C%2Faddressline%3E%3Clongitude%3E-73.89188969999998%3C%2Flongitude%3E%3Clatitude%3E40.6655101%3C%2Flatitude%3E%3C%2Fgeoloc%3E%3C%2Fgeolocs%3E%3Csearchradius%3E20|35|50|100|250%3C%2Fsearchradius%3E%3Cwhere%3E%3Cor%3E%3Cnowdocs%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fnowdocs%3E%3Cexpanded_furn%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fexpanded_furn%3E%3Cusps%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fusps%3E%3Cshredding%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fshredding%3E%3Cselfservews%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fselfservews%3E%3Cphotoprint%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fphotoprint%3E%3Cexpandedbb%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fexpandedbb%3E%3Cprinting3d%3E%3Ceq%3E%3C%2Feq%3E%3C%2Fprinting3d%3E%3Clisteningstation%3E%3Ceq%3E%3C%2Feq%3E%3C%2Flisteningstation%3E%3Ccellphonerepair%3E%3Cin%3E%3C%2Fin%3E%3C%2Fcellphonerepair%3E%3C%2For%3E%3Cicon%3E%3Ceq%3E%3C%2Feq%3E%3C%2Ficon%3E%3C%2Fwhere%3E%3C%2Fformdata%3E%3C%2Frequest%3E')
	if r.status_code != 200:
		raise RuntimeError( '%s' % r )
	print r.text
	data = xmltodict.parse(r.text)

	return data

if __name__ == '__main__':

	def prettyJson( obj ):
		return json.dumps( obj, sort_keys=True, indent=2, separators=(',', ':') )

	data = getDataForZipCode( 10704 )
	print data['response']
	print '----------'
	print prettyJson( Location.from_json( data['response']['collection']['poi'] ).as_dict() )

# NOTE: NY City Office Depots have closed... so I'm not going to get 
# that data yet
