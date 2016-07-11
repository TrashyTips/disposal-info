function LocationInfo( rawGeoJson ){
	this.rawGeoJson = rawGeoJson;
	var options = rawGeoJson.properties;

	// "Offical" or canonical fields
	this.title = '';
	this.address = '';
	this.phone = '';
	this.type = '';
	this.link = '';
	this.company = '';
	this.hours = '';
	this.offerings = '';
	this.accepts = [];
	this.rejects = [];
	// let's keep these in the geojson as they should be,
	// don't duplicate them and create extra work
	//this.lat = 0;
	//this.lng = 0;

	// BELOW can be done on the backend

	// Normalize all of the data fields across various providers
	LocationInfo.loadHousingWorks( this, options );
	LocationInfo.loadSalvationArmy( this, options );
	LocationInfo.loadUsagain( this, options );
	LocationInfo.loadBestBuy( this, options );
	LocationInfo.loadStaples( this, options );

	// TODO Clean all of the data (ie format phone numbers)

	return this;
}
LocationInfo.cleanPhoneNumber = function( phone ){
	// Remove all the non-letters/digits
	// some salvation army numbers start with 'call...'
	var digits = phone.toLowerCase().replace(/[ (){}\[\]\-.]/g,'').replace(/^call/,'');
	// Change letters to digits (note: 0 and 1 are not letters)
	var numbers = digits
		.replace(/[abc]/g,'2')
		.replace(/[def]/g,'3')
		.replace(/[ghi]/g,'4')
		.replace(/[jkl]/g,'5')
		.replace(/[mno]/g,'6')
		.replace(/[pqrs]/g,'7')
		.replace(/[tuv]/g,'8')
		.replace(/[wxyz]/g,'9');
	return numbers;
}
LocationInfo.loadHousingWorks = function( self, options ){
	if( options.hasOwnProperty('address') ){ self.address = options.address; }
	if( options.hasOwnProperty('hours') ){ self.hours = options.hours; }
	if( options.hasOwnProperty('link') ){ self.link = options.link; }
	if( options.hasOwnProperty('name') ){ self.title = options.name; }
	if( options.hasOwnProperty('offerings') ){ self.offerings = options.offerings; }
	if( options.hasOwnProperty('telephone') ){ self.phone = options.telephone; }
	return self;
}
LocationInfo.loadSalvationArmy = function( self, options ){
	if( options.hasOwnProperty('address') ){ self.address = options.address; }
	if( options.hasOwnProperty('url') ){ self.link = options.url; }
	if( options.hasOwnProperty('name') ){ self.title = options.name; }
	if( options.hasOwnProperty('phone') ){ self.phone = options.phone; }
	if( options.hasOwnProperty('type') ){ self.type = options.type; }
	return self;
}
LocationInfo.loadUsagain = function( self, options ){
	if( options.hasOwnProperty('address') ){ self.address = options.address; }
	if( options.hasOwnProperty('name') ){ self.title = options.name; }
	return self;
}
LocationInfo.loadBestBuy = function( self, options ){
	if( options.hasOwnProperty('address') ){ self.address = options.address; }
	if( options.hasOwnProperty('hours') ){ self.hours = options.hours; }
	if( options.hasOwnProperty('number') ){ self.link = 'http://stores.bestbuy.com/'+options.number; }
	if( options.hasOwnProperty('name') ){ self.title = options.name; }
	if( options.hasOwnProperty('phone') ){ self.phone = options.phone; }
	return self;
}
LocationInfo.loadStaples = function( self, options ){
	if( options.hasOwnProperty('address') ){ self.address = options.address; }
	if( options.hasOwnProperty('hours') ){ self.hours = options.hours; }
	if( options.hasOwnProperty('name') ){ self.title = options.name; }
	if( options.hasOwnProperty('phone') ){ self.phone = options.phone; }
	return self;
}
