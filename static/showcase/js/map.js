$(function () {
	// Bigining point to show the map
	var center = [-2.2986156360633974,-78.12206268310548];
	// Zoom limit  
	var min_zoom = 16;
	var max_zoom = 4;  
	var token = 'pk.eyJ1IjoiZGJzaWF2aWNoYXkiLCJhIjoiY2l1aDhzanVzMDExeDJ5cDR4bWtsbHA3ZCJ9.uL7b4pcnOVe1B3I0am59kQ';		
	
	L.mapbox.accessToken = token;

	var layer = L.mapbox.tileLayer('mapbox.streets');
	
	var render_map = function (latlng) {
		map = L.mapbox.map('map');
		layer.addTo(map);
		var latlng = latlng || L.latLng(center);
		map.setView(latlng);
		
		return map;
	};
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
	var map = render_map().setView(center, 15);
	
	// map.on('zoomend', function(e) {
	// 	var zoom = map.getZoom();
	// 	if(zoom > min_zoom){
	// 		map.remove();
	// 		render_map();
	// 		render_localities(zoom);
	// 		render_events();
	// 		console.log(zoom);
	// 	}else{
	// 		return e;
	// 	}
				
	// });


	var ubication_button = function (latlng){
		$('a[id*=ubicate]').on('click', function(e) {
			latlng = latlng || L.latlng(center);
			map.flyTo(latlng, 17);

			var point = L.icon({
				iconUrl: 'static/showcase/img/circle.png',
				//iconRetinaUrl: 'my-icon@2x.png',
				iconSize: [38, 38],
				iconAnchor: [22, 22],
				//popupAnchor: [-3, -76],
				//shadowUrl: 'my-icon-shadow.png',
				//shadowRetinaUrl: 'my-icon-shadow@2x.png',
				//shadowSize: [68, 95],
				//shadowAnchor: [22, 94]
			});

			var self_marker = L.marker(latlng, {icon: point})		
			.addTo(map);

			var content = 'Tú';
			self_marker.bindPopup(content);
		});

	};

	var reload_map = function (latlng) {
		var lat = $('#map').attr('lat');
		var lng = $('#map').attr('lng');	

		var msg = $.get("msg");
		
		if (lat && lng) {
			latlng = L.latLng(parseFloat(lat), parseFloat(lng))	
			map.flyTo(latlng, 19);
			return;
		}
		var browserType = isMobile.any()?"mobile":"not mobile";
		if (browserType == "mobile") {
		 	navigator.geolocation.getCurrentPosition(function (position) {		
		 		var latlng = L.latLng(position.coords.latitude,position.coords.longitude);
				center[0] = latlng.lat;
				center[1] = latlng.lng;
				map.setView(latlng);

				set_location_floats();
				ubication_button(latlng);

			}, function (error) {
				console.warn('ERROR(' + error.code + '): ' + error.message);			
			});
			
		}else{
			$('a[id*=ubicate]').hide();
			$('a[id*=floating-options]').hide();
			msg = "Click derecho para opciones"
		}

		console.log(msg);
		if (msg){
			Materialize.toast(msg, 4000);
		};
	}
	

	var set_location_floats = function () {		
		$('#btn-event-register-float').attr('lat', map.getCenter().lat);
	  	$('#btn-event-register-float').attr('lng', map.getCenter().lng);

	  	$('#btn-locality-register-float').attr('lat', map.getCenter().lat);
	  	$('#btn-locality-register-float').attr('lng', map.getCenter().lng);
	}

	function render_localities (zLevel) {
		var public_zone = true;
		console.log(zLevel);
		switch (zLevel){
			case zLevel <= min_zoom: public_zone = true
			break;
			case zLevel > min_zoom: public_zone = false 
			break;
		};
		console.log(public_zone);
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
				if(data[index].verified == false && public_zone){
					marker.remove();
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

	function render_events () {
		$.get('/events/', function(data) {			
			for (index in data)  {	
				var priority = data[index].is_public?10001:1;
				var url = data[index].is_public?"/locality/":"/user/";	
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
					'<p> De: <a class="collection-item" href="' + url + data[index].event_owner + '">'+ data[index].event_owner +
					' </a> <br> ' + data[index].day + ' </p> <a href="/event/'+data[index].id+'/" class="right cyan-text waves-effect waves-cyan white btn">'+
					'<strong> Ver </strong></a>';

				marker.bindPopup(content);				
            }
		});
	}

	var add_context_menu = function () {
		map.on('contextmenu', function(e) {		  	
		  	$('#btn-event-register').attr('lat', e.latlng.lat);
		  	$('#btn-event-register').attr('lng', e.latlng.lng);

		  	$('#btn-locality-register').attr('lat', e.latlng.lat);
		  	$('#btn-locality-register').attr('lng', e.latlng.lng);

		  	$('#event-modal').modal('open');
		});	  
	}
	

	var init = function () {
		reload_map();	
		set_location_floats();
		render_events();
		render_localities();
		
		add_context_menu();
	}

	init();

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


