$(function () {
	//Funcionalidad para API Geolocation
	navigator.geolocation.getCurrentPosition(success, error);

	function success(position) {
		var point = position.coords;
		var token = 'pk.eyJ1IjoiZGJzaWF2aWNoYXkiLCJhIjoiY2l1aDhzanVzMDExeDJ5cDR4bWtsbHA3ZCJ9.uL7b4pcnOVe1B3I0am59kQ';

		$('#btn-event-register-float').attr('lat', point.latitude);
	  	$('#btn-event-register-float').attr('lng', point.longitude);

	  	$('#btn-locality-register-float').attr('lat', point.latitude);
	  	$('#btn-locality-register-float').attr('lng', point.longitude);

		L.mapbox.accessToken = token;
		var map = L.mapbox.map('map', 'mapbox.light').setView([point.latitude,point.longitude], 15);		
		 
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

						var content = '<h3 class="cyan-text">' + data[index].name+ '</h3>' +
							'<p>' + data[index].description +					
							' </p> <a href="/locality/'+data[index].id+'/" class="right cyan-text waves-effect waves-cyan white btn">'+
							'<strong> Ver </strong></a>';

						marker.bindPopup(content);
		            }
				});

		 $.get('/events/', function(data) {			
			for (index in data)  {	
				var marker = L.marker([data[index].latitude, data[index].longitude], {
				    icon: L.mapbox.marker.icon({
				    	'marker-size': 'medium',
				    	'marker-symbol': 'star',
		                'marker-color': '#00bcd4'
				    })
				}).addTo(map);

				var content = '<h3 class="cyan-text ">' + data[index].name+ '</h3>' +
					'<p>' + data[index].description +					
					'</p> <a href="/event/'+data[index].id+'/" class="right cyan-text waves-effect waves-cyan white btn">'+
					'<strong> Ver </strong></a>';

				marker.bindPopup(content);
            }
		});

		map.on('contextmenu', function(e) {		  	
		  	$('#btn-event-register').attr('lat', e.latlng.lat);
		  	$('#btn-event-register').attr('lng', e.latlng.lng);

		  	$('#btn-locality-register').attr('lat', e.latlng.lat);
		  	$('#btn-locality-register').attr('lng', e.latlng.lng);

		  	$('#event-modal').modal('open');
		});	  
	};

	function error(error) {
	  console.warn('ERROR(' + error.code + '): ' + error.message);
	};

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

