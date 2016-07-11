
function makePopupHtml( feature ){
	var parts = [];
	parts.push( '<a href="javascript:openSidebar()"><h3>'+feature.title+'</h3></a>' );
	parts.push( '<div><i class="fa fa-fw fa-map-marker"></i><a class="address" href="https://www.google.com/maps/search/'+encodeURIComponent(feature.address)+'">'+feature.address+'</a></div>' );
	if( feature.phone ){
		parts.push('<div><i class="fa fa-fw fa-phone"></i><a class="phone" href="tel:'+LocationInfo.cleanPhoneNumber(feature.phone)+'">'+feature.phone+'</a></div>');
	}
	if( feature.link ){
		parts.push( '<div><i class="fa fa-fw fa-link"></i><a href="'+feature.link+'">'+'More info'+'</a></div>' );
	}
	if( feature.hours ){
		parts.push( '<div class="hours"><i class="fa fa-fw fa-clock-o"></i>'+feature.hours+'</div>' );
	}
	return parts.join('');
}

function makeSidebarContent( feature, providerInfo ){
	var parts = [];
	parts.push( '<h2>'+feature.title+'</h2>' );
	parts.push( '<div><i class="fa fa-fw fa-map-marker"></i><a class="address" href="https://www.google.com/maps/search/'+encodeURIComponent(feature.address)+'">'+feature.address+'</a></div>' );
	if( feature.phone ){
		parts.push('<div><i class="fa fa-fw fa-phone"></i><a class="phone" href="tel:'+LocationInfo.cleanPhoneNumber(feature.phone)+'">'+feature.phone+'</a></div>');
	}
	if( feature.link ){
		parts.push( '<div><i class="fa fa-fw fa-link"></i><a href="'+feature.link+'">'+'More info'+'</a></div>' );
	}
	if( feature.hours ){
		parts.push( '<div class="hours"><i class="fa fa-fw fa-clock-o"></i>'+feature.hours+'</div>' );
	}
	parts.push('<h2>Provider Info</h2>');
	parts.push( providerInfo );
	return parts.join('');
}

function loadPlaces( options ){
	// url, sidebarContent
	var defer = $.Deferred();
	$.get(options.url).then( function(response){
		var geojson = L.geoJson( response, {
			pointToLayer: function (feature, latlng) {
				var location = new LocationInfo( feature );
				return L.marker(latlng, options.markerOptions)
					.bindPopup(makePopupHtml(location))
					.on('click',function(){
						// The content does not get set if I open the sidebar
						// but if dont open it, then the content does get set
						// sidebar.open();
						// That acutally seems to open something different.
						// I manually trigger a click on the html input/link
						// to simulate a user clicking to get the correct
						// results.
						$('#provider-info-content').html( makeSidebarContent(location,options.sidebarContent) );
					});
			}
		});
		defer.resolve( geojson );
	});
	return defer.promise();
}
