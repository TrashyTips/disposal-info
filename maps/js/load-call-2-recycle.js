$.get('../data/descriptions/call-2-recycle.html').then( function(response){
	return loadPlaces({
		url: '../data/places/call2recycle-geo.json',
		locationType: 'Call2Recycle',
		sidebarContent: response,
		markerOptions: {
			icon: L.BeautifyIcon.icon({
				isAlphaNumericIcon: true,
				text: 'C2R',
				//iconShape: 'marker',
				backgroundColor: '#45988E',
				borderColor: '#B0EF07',
				textColor: '#B0EF07'
			})
		}
	});
} ).then( function( geojson ){
	geojson.addTo( places );
	map.setView([40.7553361,-73.9693638]);
} );
