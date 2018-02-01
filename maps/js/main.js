
var map = L.map('map');
map.setView([-73.956504, 40.775856], 9);

L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 18,
	attribution: 'Map data &copy; OpenStreetMap contributors'
}).addTo(map);

var sidebar = L.control.sidebar('sidebar').addTo(map);
var geoLocation = L.control.locate({
	locateOptions: {
		maxZoom: 12
	}
}).addTo(map);
var places = L.markerClusterGroup();

var toggleGrouping = L.easyButton({
	id: 'animated-marker-toggle',
	states: [{
		stateName: 'show-all',
		title: 'Show all locations',
		icon: 'fa-tags', //object-ungroup
		onClick: function(control) {
			//animatedToggleMap.removeLayer(randomMarkers);
			places.disableClustering()
			control.state('show-clusters');
		}
	}, {
		stateName: 'show-clusters',
		icon: 'fa-tag', //object-group
		title: 'Cluster nearby locations',
		onClick: function(control) {
			//animatedToggleMap.addLayer(randomMarkers);
			places.enableClustering();
			control.state('show-all');
		}
	}]
});
toggleGrouping.addTo(map);

function openSidebar(){
	$('#btn-sidebar-home')[0].click();
}

places.addTo( map );
