$.get('../data/descriptions/usagain.html').then( function(response){
	return loadPlaces({
		url: '../data/places/usagain-geo.json',
		locationType: 'Usagain',
		sidebarContent: response,
		markerOptions: {
			icon: L.BeautifyIcon.icon({
				isAlphaNumericIcon: true,
				text: 'UA',
				//iconShape: 'marker',
				backgroundColor: '#6EB43F',
				borderColor: '#000000',
				textColor: '#FFFFFF'
			})
		}
	});
} ).then( function( geojson ){
	geojson.addTo( places );
	places.addTo( map );
	map.setView(geojson.getBounds().getCenter());
} );
