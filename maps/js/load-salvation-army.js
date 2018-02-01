$.get('../data/descriptions/salvation-army.html').then( function(response){
	return loadPlaces({
		url: '../data/places/salvation-army-geo.json',
		locationType: 'SalvationArmy',
		sidebarContent: response,
		markerOptions: {
			icon: L.BeautifyIcon.icon({
				isAlphaNumericIcon: true,
				text: 'SA',
				//iconShape: 'marker',
				backgroundColor: '#FF0000',
				borderColor: '#880000',
				textColor: '#FFFFFF'
			})
		}
	});
} ).then( function( geojson ){
	geojson.addTo( places );
	places.addTo( map );
	map.setView(geojson.getBounds().getCenter());
} );
