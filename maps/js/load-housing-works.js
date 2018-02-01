$.get('../data/descriptions/housing-works.html').then( function(response){
	return loadPlaces({
		url: '../data/places/housing-works-geo.json',
		locationType: 'HousingWorks',
		sidebarContent: response,
		markerOptions: {
			icon: L.BeautifyIcon.icon({
				isAlphaNumericIcon: true,
				text: 'HW',
				//iconShape: 'marker',
				backgroundColor: '#222222',
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
