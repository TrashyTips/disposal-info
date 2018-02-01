import requests

def getLatLng( address ):
	x = requests.get( 'http://maps.googleapis.com/maps/api/geocode/json?address=%s' % address ).json()
	if 'results' not in x:
		raise RuntimeError( 'Bad response:\n%s' % x )
	if len( x['results'] ) == 0:
		raise KeyError( 'Address (%s) not found' % address )
	formattedAddress = x['results'][0]['formatted_address']
	return (
		x['results'][0]['geometry']['location']['lat'],
		x['results'][0]['geometry']['location']['lng']
	)

def toGeoJsonWithLatLng( dictionaries ):
	geojson = []
	for l in dictionaries:
		geojson.append( {
			'type': 'Feature',
			'properties': l,
			'geometry': {
				'type': 'Point',
				'coordinates': [
					l['lng'],
					l['lat']
				]
			}
		} )
	return {
		"type": "FeatureCollection",
		"features": geojson
	}

def appendLatLng( data, getAddress ):
	d = data
	try:
		(lat, lng) = getLatLng( getAddress(d) )
	except KeyError:
		lat = ''
		lng = ''
		if ('lat' not in d) and ('lng' not in d):
			raise
	
	# If the dictionary already has lat/lng, see that it agrees
	if 'lat' in d:
		if lat != '' and lat != d['lat']:
			d['lat_geocode'] = lat
	else:
		d['lat'] = lat

	if 'lng' in d:
		if lng != '' and lng != d['lng']:
			d['lng_geocode'] = lng
	else:
		d['lng'] = lng

	return d

def appendLatLngArray( dictionaries, getAddress ):
	for d in dictionaries:
		appendLatLng( d, getAddress )

	return dictionaries

def toGeoJson( dictionaries, getAddress ):
	geojson = []
	for l in dictionaries:
		try:
			(lat,lng) = getLatLng( getAddress( l ) )
		except Exception as e:
			print e
			continue
		geojson.append( {
			'type': 'Feature',
			'properties': l,
			'geometry': {
				'type': 'Point',
				'coordinates': [
					lng,
					lat
				]
			}
		} )
	return {
		"type": "FeatureCollection",
		"features": geojson
	}


