$(function () {
	// Returns true or false on many cases 
	var isMobile = {
	    Android: function() {
	        return navigator.userAgent.match(/Android/i);
	    },
	    BlackBerry: function() {
	        return navigator.userAgent.match(/BlackBerry/i);
	    },
	    iOS: function() {
	        return navigator.userAgent.match(/iPhone|iPad|iPod/i);
	    },
	    Opera: function() {
	        return navigator.userAgent.match(/Opera Mini/i);
	    },
	    Windows: function() {
	        return navigator.userAgent.match(/IEMobile/i);
	    },
	    any: function() {
	        return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
	    }
	};

	// Bigining point to show the map
	var center = [-2.2986156360633974,-78.12206268310548];

	// Zoom limit  
	var p_zone = 16; // or more
	var max_zoom = 4;  
	var token = 'pk.eyJ1IjoiZGJzaWF2aWNoYXkiLCJhIjoiY2l1aDhzanVzMDExeDJ5cDR4bWtsbHA3ZCJ9.uL7b4pcnOVe1B3I0am59kQ';		
	
	L.mapbox.accessToken = token;
	
	
	// The geocoder can return an area, like a city, or a
    // point, like an address. Here we handle both cases,
    // by fitting the map bounds to an area or zooming to a point.
	function showMap(err, data) {
	    if (data.lbounds) {
	        map.fitBounds(data.lbounds);
	    } else if (data.latlng) {
	        map.setView([data.latlng[0], data.latlng[1]], 20);
	    }
	}

	// Personalizacion de marca
	var myStyle = {
	    "color": "#ffc107",
	};

	// render a tileLayer on map at center 
	var render_map = function (latlng, zLevel) {
		var keepOpen = isMobile.any()?false:true;
		map = L.mapbox.map('map').addControl(L.mapbox.geocoderControl('mapbox.places', {
			keepOpen: keepOpen,
			autocomplete: true
		}));
		L.mapbox.tileLayer('mapbox.streets').addTo(map);
		var latlng = latlng || L.latLng(center);
		map.setView(latlng, zLevel);		
		return map;
	};

	var map = render_map(center, 15);
	var geoJson_Mape;
	var mape_layer  = L.mapbox.featureLayer().addTo(map);
	var commercial = L.geoJSON();

	//personalizacion de marca
	var geojsonFeature = {
	    "type": "Feature",
	    "properties": {
	        "name": "Coors Field",
	        "amenity": "Baseball Stadium",
	        "popupContent": "This is where the Rockies play!",
	        "icon": L.mapbox.marker.icon({
				    	'marker-size': 'medium',
				    	'marker-symbol': 'bus',
		                'marker-color': '#ffc107',
				    })
	    },
	    "geometry": {
	        "type": "Point",
	        "coordinates": [-104.99404, 39.75621]
	    }
	};

	// Gets localities and puts like marks on map
	$.get('/localities/', function(data) {
		var content, marker, geoJSON_mark;
		for (index in data) {
				content = '<a class="" href="/locality/' + data[index].id+ '">' + data[index].name+ '</a>' +
				'<p>' + data[index].description +
				'</p> <p> <img class="responsive-img mape-large circle z-depth-3" src="' + data[index].locality_image_url + 
				'" > </p> <a href="/locality/'+data[index].id+
				'/" class="right cyan-text waves-effect waves-cyan white btn">'+
				'<strong> Ver </strong></a>  '
				marker = L.marker([data[index].latitude, data[index].longitude], {
				    icon: L.mapbox.marker.icon({
				    	'marker-size': 'medium',
				    	'marker-symbol': 'circle',
		                'marker-color': '#ffc107',
				    }),
		            title: data[index].name,
				});
			marker.bindPopup(content);

			geoJSON_mark = marker.toGeoJSON()
			geoJSON_mark['properties']= {
				'marker-symbol': 'fast-food'
			}


			
			marker.addTo(map);

			// mark = {
			// 	"type": "Feature",
			// 	"geometry": {
			// 		"type": "Point",
			// 		"coordinates": [data[index].latitude, data[index].longitude],
			// 		"popupContent": content
			// 	},
			// 	"properties": {
			// 	    "name": data[index].name
			// 	  }
			// };
			commercial.addData(geoJSON_mark, {
			    style: myStyle
			});
        }
        
	});

	commercial.addData(geojsonFeature);

	// Desaparece todas las marcas en la capa mape_layer
	mape_layer.setFilter(function(f) { return f.properties['marker-symbol'] === 'fast-food'; 
	}).addTo(map);

   

	// Fuction at ended event of zoom on map
	map.on('zoomend', function(e) {
		var zoom = map.getZoom();
		map.featureLayer.setFilter(function() {return false; })
		if(zoom > p_zone){
			
			mape_layer.setFilter(function() {return true; })
			console.log("zoom" , zoom);
			//render_map();
			//render_events();
		}else{
			mape_layer.setFilter(function() {return false; })
			return e;
		}
				
	});

	// Fly on map to location at latlng
	function fly_back(latlng) {
		if (latlng){
			map.flyTo(latlng, 17);
			var mark = L.icon({
				iconUrl: 'static/showcase/img/circle.png',
				//iconRetinaUrl: 'my-icon@2x.png',
				iconSize: [24, 24],
				iconAnchor: [22, 22],
				//popupAnchor: [-3, -76],
				//shadowUrl: 'my-icon-shadow.png',
				//shadowRetinaUrl: 'my-icon-shadow@2x.png',
				//shadowSize: [68, 95],
				//shadowAnchor: [22, 94]
			});
			set_location_floats(latlng);
			var self_marker = L.marker(latlng, {icon: mark})		
			.addTo(map);
			Materialize.toast('Aquí', 4000);
			self_marker.bindPopup('Aquí');
		}
	};

	// Reload map with a message and a new ubication if is required
	var reload_map = function (latlng) {
		var lat = $('#map').attr('lat');
		var lng = $('#map').attr('lng');	
		var var_latlng;

		var msg = $.get("msg");
		
		if (lat && lng) {
			latlng = L.latLng(parseFloat(lat), parseFloat(lng));
			map.setView(latlng);
			map.flyTo(latlng, 19);
			$('a[id*=ubicate]').hide();
			$('a[id*=floating-options]').hide();
			return;
		}
		var browserType = isMobile.any()?"mobile":"not mobile";
		if (navigator.geolocation){
			navigator.geolocation.getCurrentPosition(function (position) {		
		 		var_latlng = L.latLng(position.coords.latitude,position.coords.longitude);
		 		msg = msg + "<p>Tu navegador nos indica que tu ubicación es: " + var_latlng.lat + ", " + var_latlng.lng + "</p>";
		 		console.log(var_latlng);
		 		if (browserType == "mobile"){
		 			map.setView(var_latlng);
		 			//geocoder.query('Morona, Ecuador', showMap);	
		 		}
		 		//$("#modal-title").after(msg);
			}, function (error) {
				console.warn('ERROR(' + error.code + '): ' + error.message);			
			});

			if (browserType == "mobile") {
				msg = "Manten presionado sobre el mapa";
				
				$('a[id*=ubicate]').on('click', function(e) {
					fly_back(var_latlng);
				});
			}else{
				//$('#ubication-modal').modal('open');
				$('a[id*=ubicate]').hide();
				$('a[id*=floating-options]').hide();
				msg = "Click derecho para opciones"
			}
			console.log(msg);
		};
		if (msg){
			Materialize.toast(msg, 4000);
		};
	}
	
	// Sets the atributes latlng of floats add buttoms 
	var set_location_floats = function (latlng) {		
		$('#btn-event-register-float').attr('lat', latlng.lat);
	  	$('#btn-event-register-float').attr('lng', latlng.lng);
	  	$('#btn-locality-register-float').attr('lat', latlng.lat);
	  	$('#btn-locality-register-float').attr('lng', latlng.lng);
	}

	// Render the localities on map like a mark 
	function render_localities () {
		zLevel = map.getZoom()
		console.log(zLevel, p_zone)
		$.get('/localities/', function(data) {
			var opcty= 1;
			for (index in data) {
				var marker = L.marker([data[index].latitude, data[index].longitude], {
				    icon: L.mapbox.marker.icon({
				    	'marker-size': 'medium',
				    	'marker-symbol': 'circle',
		                'marker-color': '#ffc107',
				    }),
		            title: data[index].name,
		            opacity: opcty
				});
				marker.addTo(map);
				if (zLevel >= p_zone && data[index].hide ){
					console.log("Zona pública", zLevel, p_zone);
				}else{
					console.log('Zona Privada');
				};
				var content = '<a class="" href="/locality/' + data[index].id+ '">' + data[index].name+ '</a>' +
					'<p>' + data[index].description +
					'</p> <p> <img class="responsive-img mape-large circle z-depth-3" src="' + data[index].locality_image_url + 
					'" > </p> <a href="/locality/'+data[index].id+
					'/" class="right cyan-text waves-effect waves-cyan white btn">'+
					'<strong> Ver </strong></a>  ';
				marker.bindPopup(content);
            }
		});
	}

	// Render the localities on map like a mark
	function render_events () {
		$.get('/events/', function(data) {			
			for (index in data)  {	
				var priority = data[index].is_public?10001:1;
				var status = data[index].day;
				var url = data[index].is_public?"/locality/":"/p/";	
				var marker = L.marker([data[index].latitude, data[index].longitude], {
			    	icon: L.mapbox.marker.icon({
				    	'marker-size': 'large',
				    	'marker-symbol': 'star',
		                'marker-color': '#00bcd4'
			    	}),
			    	zIndexOffset : priority,
			    	title: data[index].name
				}).addTo(map);
				var content = '<strong class="cyan-text text-darken-3">' + data[index].name+ '</strong>' +
					'<p>' + data[index].description +					
					'</p> <p>  <a href="'  + data[index].event_image_url +
					'" target="_blank" > <img class="responsive-img mape-large z-depth-3" src="' + data[index].event_image_url + '" > </a></p>' + 
					'<p> De: <a class="collection-item" href="' + url + data[index].owner_id + '">'+ data[index].event_owner +
					' </a> <br> <strong>' + status + '</strong> </p> <a href="/event/'+data[index].event_id+'/" class="right cyan-text waves-effect waves-cyan white btn">'+
					'<strong> Ver </strong></a>';
				if (data[index].hide) {
					marker.remove();
				}
				marker.bindPopup(content);				
            }
		});
	}

	function put_latlng_on_buttoms(latlng) {
		$('#btn-event-register').attr('lat', latlng.lat);
	  	$('#btn-event-register').attr('lng', latlng.lng);

	  	$('#btn-locality-register').attr('lat', latlng.lat);
	  	$('#btn-locality-register').attr('lng', latlng.lng);
	}
	// Takes latlng at point on right-click in the map
	var add_context_menu = function () {
		map.on('contextmenu', function(e) {		  	
		  	put_latlng_on_buttoms(e.latlng)
		  	$('#event-modal').modal('open');
		  	Materialize.toast("Has seleccionado una ibicación: " + e.latlng.lat.toFixed(4) +" | " + e.latlng.lng.toFixed(4) , 4000);
		});	  
	}

	// Inits all the functions in order 
	var init = function () {
		// Fix the top-margin 
		document.body.style.margin="0px 0px";
		// Sets the map on the place that gets the geocoder
		var geocoder = L.mapbox.geocoder('mapbox.places');
		// Set a location on Morona by geocoder
			// geocoder.query('Morona, Ecuador', showMap);
		reload_map();	
		//set_location_floats();
		render_events();
		//render_localities();
		add_context_menu();
		console.log("center", map.getCenter());
	}

	init();
	

	// Gets the latlng of attrs of buttoms and puts in the url, this to preloading of a mark form 
	$('a[id*=btn-event-register]').on('click', function(e) {
		e.preventDefault();
		lat = $(this).attr('lat');
		lng = $(this).attr('lng');
		$(location).attr('href', '/event/add/?lat='+lat+'&lng='+lng);
	});	
	$('a[id*=btn-locality-register]').on('click', function(e) {
		e.preventDefault();
		lat = $(this).attr('lat');
		lng = $(this).attr('lng');
		$(location).attr('href', '/locality/add/?lat='+lat+'&lng='+lng);
	});	
});


