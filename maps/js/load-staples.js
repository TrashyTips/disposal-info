$.get('../data/descriptions/staples.html').then( function(response){
	return loadPlaces({
		url: '../data/places/staples-geo.json',
		locationType: 'Staples',
		sidebarContent: response,
		markerOptions: {
			icon: L.BeautifyIcon.icon({
				isAlphaNumericIcon: true,
				text: 'S',
				//iconShape: 'marker',
				backgroundColor: '#FF0000',
				borderColor: '#AA0000',
				textColor: '#FFFFFF'
			})
		}
	});
} ).then( function( geojson ){
	geojson.addTo( places );
	map.setView([40.7553361,-73.9693638]);
} );
