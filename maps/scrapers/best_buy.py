# -*- coding: utf-8 -*-
import json

import requests
from bs4 import BeautifulSoup

# http://www.bestbuy.com/site/store-locator/11356

# I think every store can be found via that url, just change the number:
# http://stores.bestbuy.com/1115

class StoreInfo():

	@staticmethod
	def from_dict( storeInfoDict ):
		return StoreInfo(
			storeInfoDict['number'],
			storeInfoDict['name'],
			storeInfoDict['address'],
			storeInfoDict['phone'],
			StoreHours.from_dict(storeInfoDict['hours'])
		)

	def __init__( self, number, name, address, phone, hours ):
		self.number = number
		self.name = name
		self.address = address
		self.phone = phone
		self.hours = hours

	def __str__( self ):
		return '''# %s (%s)
		%s
		%s
		%s
		'''.replace( '\t\t', '' ) % (
			self.name,
			self.number,
			self.address,
			self.phone,
			self.hours
		)

	def as_dict( self ):
		return dict(
			name = self.name,
			number = self.number,
			address = self.address,
			phone = self.phone,
			hours = self.hours.as_dict()
		)

class DailyHours():

	@staticmethod
	def from_dict( dailyHoursDict ):
		return StoreInfo(
			dailyHoursDict['opening'],
			closing['name'],
			storeInfoDict['address'],
			storeInfoDict['phone'],
			StoreHours.from_dict(storeInfoDict['hours'])
		)

	def __init__( self, opening, closing ):
		self.opening = opening
		self.closing = closing

	def __str__( self ):
		return '%s to %s' % (self.opening, self.closing)

	def as_dict( self ):
		return dict(
			opening = self.opening,
			closing = self.closing
		)

class StoreHours():
	def __init__( self ):
		self.mon = DailyHours(0,0)
		self.tue = DailyHours(0,0)
		self.wed = DailyHours(0,0)
		self.thu = DailyHours(0,0)
		self.fri = DailyHours(0,0)
		self.sat = DailyHours(0,0)
		self.sun = DailyHours(0,0)

	def setHours( self, weekday, opening, closing ):
		day = getattr( self, weekday )
		day.opening = opening
		day.closing = closing

	def __str__( self ):
		return '\n'.join([
			'mon %s' % self.mon,
			'tue %s' % self.tue,
			'wed %s' % self.wed,
			'thu %s' % self.thu,
			'fir %s' % self.fri,
			'sat %s' % self.sat,
			'sun %s' % self.sun
		])

	def as_dict( self ):
		return dict(
			mon = self.mon.as_dict(),
			tue = self.tue.as_dict(),
			wed = self.wed.as_dict(),
			thu = self.thu.as_dict(),
			fri = self.fri.as_dict(),
			sat = self.sat.as_dict(),
			sun = self.sun.as_dict()
		)


def getStoreInfo( storeId ):

	r = requests.get('http://stores.bestbuy.com/%s' % storeId)
	if r.status_code != 200:
		raise RuntimeError( '%s' % r )

	soup = BeautifulSoup(r.text, 'html.parser')
	
	number = storeId
	name = soup.select( '#location-name' )[0].getText()
	address = soup.select( '#address' )[0].getText()
	phone = soup.select( '#telephone' )[0].getText()
	storeHours = StoreHours()
	
	hourInfo = soup.select( '.c-location-hours-details' )[0]
	#print hourInfo
	dayRows = hourInfo.select( '.c-location-hours-details-row' )
	for row in dayRows:
		#print row
		weekday = row.select('.c-location-hours-details-row-day')[0].getText().lower()
		openTime = row.select('.c-location-hours-details-row-intervals-instance-open')[0].getText()
		closeTime = row.select('.c-location-hours-details-row-intervals-instance-close')[0].getText()
		storeHours.setHours( weekday, openTime, closeTime )

	storeInfo = StoreInfo( number, name, address, phone, storeHours )
	return storeInfo

if __name__ == '__main__':

	def prettyJson( obj ):
		return json.dumps( obj, sort_keys=True, indent=2, separators=(',', ':') )

	def firstTime():
		import time
		import random
		stores = []
		for i in range(1000,2500):
			try:
				store = getStoreInfo( '%s' % i )
			except Exception as e:
				print 'Store %s -- fail' % i
			else:
				print 'Store %s -- pass' % i
				stores.append( store )
			time.sleep( 5.0*random.random() )

		dictionaries = [ s.as_dict() for s in stores ]
		with open( 'best-buy.json', 'wb' ) as f:
			f.write( prettyJson( dictionaries ) )

	# TODO add to geojson conversion
	def secondTime():
		with open( 'best-buy.json', 'rb' ) as f:
			data = json.loads( f.read() )

		from shared.geocode import toGeoJson

		geojson = toGeoJson( data, lambda x: x['address'] )
		with open( 'best-buy-geo.json', 'wb' ) as f:
			f.write( prettyJson( geojson ) )

	secondTime()
