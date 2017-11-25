$(function () {
	var render_map = function (latlng) {		
		var latlng = latlng || L.latLng(-2.2986156360633974,-78.12206268310548);
		var token = 'pk.eyJ1IjoiZGJzaWF2aWNoYXkiLCJhIjoiY2l1aDhzanVzMDExeDJ5cDR4bWtsbHA3ZCJ9.uL7b4pcnOVe1B3I0am59kQ';		

		L.mapbox.accessToken = token;		
		map = L.mapbox.map('map', 'mapbox.light').setView(latlng, 15);
		return map;
	};

	var map = render_map();

	var reload_map = function (latlng) {
		var lat = $('#map').attr('lat');
		var lng = $('#map').attr('lng');			

		if (lat && lng) {
			latlng = L.latLng(parseFloat(lat), parseFloat(lng))						
			map.flyTo(latlng);
			return;
		}

		navigator.geolocation.getCurrentPosition(function (position) {		
			var latlng = L.latLng(position.coords.latitude,position.coords.longitude);
			console.log(latlng)
			map.flyTo(latlng);
		}, function (error) {
			console.warn('ERROR(' + error.code + '): ' + error.message);			
		});		
	}
	

	var set_location_floats = function () {		
		$('#btn-event-register-float').attr('lat', map._lastCenter.lat);
	  	$('#btn-event-register-float').attr('lng', map._lastCenter.lng);

	  	$('#btn-locality-register-float').attr('lat', map._lastCenter.lat);
	  	$('#btn-locality-register-float').attr('lng', map._lastCenter.lng);
	}

	var render_localities = function () {
		$.get('/localities/', function(data) {
			for (index in data)  {				
				var marker = L.marker([data[index].latitude, data[index].longitude], {
				    icon: L.mapbox.marker.icon({
				    	'marker-size': 'medium',
				    	'marker-symbol': 'circle',
		                'marker-color': '#fa0'
				    })
				})		
				.addTo(map);

				var content = '<strong class="cyan-text text-darken-3">' + data[index].name+ '</strong>' +
					'<p>' + data[index].description +
					'</p> <p> <img class="mape-large circle z-depth-3" src=" ' + data[index].locality_image_url + 
					'" > </p> <p> De: <a class="collection-item" href="/p/'+ data[index].owner_name + '">'+ 
					data[index].owner_name + 
					'</a>  </p> <a href="/locality/'+data[index].id+
					'/" class="right cyan-text waves-effect waves-cyan white btn">'+
					'<strong> Ver </strong></a>  ';
				marker.bindPopup(content);
            }
		});
	}

	var render_events = function () {
		$.get('/events/', function(data) {			
			for (index in data)  {	
				var marker = L.marker([data[index].latitude, data[index].longitude], {
			    	icon: L.mapbox.marker.icon({
				    	'marker-size': 'medium',
				    	'marker-symbol': 'star',
		                'marker-color': '#00bcd4'
			    	})
				}).addTo(map);

				var content = '<strong class="cyan-text text-darken-3">' + data[index].name+ '</strong>' +
					'<p>' + data[index].description +					
					'</p> <p>  <a href="'  + data[index].event_image_url +
					'" target="_blank" > <img class="mape-large z-depth-3" src=" ' + data[index].event_image_url + '" > </a></p>' + 
					'<p> De: <a class="collection-item" href="/p/'+ data[index].event_owner + '">'+ data[index].event_owner +
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
		render_localities();
		render_events();
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

	Materialize.toast('Presiona click derecho sobre el mapa', 4000); 
});

