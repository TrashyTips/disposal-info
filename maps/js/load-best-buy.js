$.get('../data/descriptions/best-buy.html').then( function(response){
	return loadPlaces({
		url: '../data/places/best-buy-geo.json',
		locationType: 'BestBuy',
		sidebarContent: response,
		markerOptions: {
			icon: L.BeautifyIcon.icon({
				isAlphaNumericIcon: true,
				text: 'BB',
				//iconShape: 'marker',
				backgroundColor: '#FFFF00',
				borderColor: '#0000FF',
				textColor: '#000000'
			})
		}
	});
} ).then( function( geojson ){
	geojson.addTo( places );
	map.setView([40.7553361,-73.9693638]);
} );
