function LocationInfo( rawGeoJson, loadType ){
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
	LocationInfo['load'+loadType]( this, options );
	/*
	LocationInfo.loadHousingWorks( this, options );
	LocationInfo.loadSalvationArmy( this, options );
	LocationInfo.loadUsagain( this, options );
	LocationInfo.loadBestBuy( this, options );
	LocationInfo.loadStaples( this, options );
	LocationInfo.loadCall2Recycle( this, options );
	*/

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
	if( options.hasOwnProperty('hours') ){
		self.hours = options.hours.split(';');
	}
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
	try {
		if( options.hasOwnProperty('hours') ){
			self.hours = [
				'Mon: '+options.hours.mon.opening+'-'+options.hours.mon.closing,
				'Tue: '+options.hours.tue.opening+'-'+options.hours.tue.closing,
				'Wed: '+options.hours.wed.opening+'-'+options.hours.wed.closing,
				'Thu: '+options.hours.thu.opening+'-'+options.hours.thu.closing,
				'Fri: '+options.hours.fri.opening+'-'+options.hours.fri.closing,
				'Sat: '+options.hours.sat.opening+'-'+options.hours.sat.closing,
				'Sun: '+options.hours.sun.opening+'-'+options.hours.sun.closing
			];
		}
	}catch(e){
		if( options.hasOwnProperty('hours') ){ console.info( options.hours ); }
		self.hours = [];
	}
	if( options.hasOwnProperty('number') ){ self.link = 'http://stores.bestbuy.com/'+options.number; }
	if( options.hasOwnProperty('name') ){ self.title = options.name; }
	if( options.hasOwnProperty('phone') ){ self.phone = options.phone; }
	return self;
}
LocationInfo.loadStaples = function( self, options ){
	if( options.hasOwnProperty('address') ){ self.address = options.address; }
	if( options.hasOwnProperty('hours') ){
		try {
			self.hours = [];
			var tmpHours = options.hours.split(';');
			for( var i=0, l=tmpHours.length; i<l; i+=1 ){
				var cleanedLeft = tmpHours[i].replace(/^[,. ]+/,'');
				var cleaned = cleanedLeft.replace(/[,. ]+$/,'');
				if( cleaned.replace(/[,. ]+/g,'') !== '' ){
					self.hours.push( cleaned );
				}
			}
		}catch(e){
			console.info( options.hours );
			self.hours = [];
		}
	}
	if( options.hasOwnProperty('name') ){ self.title = options.name; }
	if( options.hasOwnProperty('phone') ){ self.phone = options.phone; }
	return self;
}
LocationInfo.loadCall2Recycle = function( self, options ){
	if( options.hasOwnProperty('address') ){ self.address = options.address; }
	if( options.hasOwnProperty('hours') && options.hours && options.hours.split ){
		self.hours = [];
		var tmpHours = options.hours.split(';');
		for( var i=0, l=tmpHours.length; i<l; i+=1 ){
			var cleanedLeft = tmpHours[i].replace(/^[,. ]+/,'');
			var cleaned = cleanedLeft.replace(/[,. ]+$/,'');
			if( cleaned.replace(/[,. ]+/g,'') !== '' ){
				self.hours.push( cleaned );
			}
		}
	}
	if( options.hasOwnProperty('name') ){ self.title = options.name; }
	if( options.hasOwnProperty('phone') ){ self.phone = options.phone; }
	if( options.hasOwnProperty('accepts') ){
		var tmpAccepts = options.accepts.split(',');
		for( var i=0, l=tmpAccepts.length; i<l; i+=1 ){
			var cleanedLeft = tmpAccepts[i].replace(/^[,. ]+/,'');
			var cleaned = cleanedLeft.replace(/[,. ]+$/,'');
			if( cleaned.replace(/[,. ]+/g,'') !== '' ){
				self.accepts.push( cleaned );
			}
		}
	}
	return self;
}
