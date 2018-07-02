$(function () {
// ----------------------------------------------------------------------------
// Facebook init

function statusChangeCallback(response) {
    console.log(response.authResponse);
    console.log(response.status);
    // The response object is returned with a status field that lets the
    // app know the current login status of the person.
    // Full docs on the response object can be found in the documentation
    // for FB.getLoginStatus().
    if (response.status === 'connected') {
      // Logged into your app and Facebook.
      FB_conection()
    } else {
      // The person is not logged into your app or we are unable to tell.
      document.getElementById('status').innerHTML = 'Please log ' +
        'into this app.';
    }
}  

window.fbAsyncInit = function() {
    FB.init({
      appId            : '1032163666847445',
      autoLogAppEvents : true,
      xfbml            : true,
      version          : 'v3.0'
    });
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
};

function checkLoginState() {
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
}

(function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "https://connect.facebook.net/es_LA/sdk.js";
     fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
	

function FB_conection() {
    console.log('Estas conectado, buscamos tu información');
    FB.api('/me', function(response) {
        console.log('Perfil cargado de: ' + response.name);
        $.ajax({
        	data : {'profile':response},
        	url : '/login/',
        	type : 'get',
        	success: function(user){
        		console.log(user)
        	}
        });


    });
}


// ----------------------------------------------------------------------------
	//Initialize modals
	$('.modal').modal();
	$('.parallax').parallax();
	$('.carousel').carousel();
	$('.collapsible').collapsible();
	$("#boton").sideNav({
		menuWidth: 300, // Default is 300
	      edge: 'right', // Choose the horizontal origin
	      closeOnClick: true, // Closes side-nav on <a> clicks, useful for Angular/Meteor
	      draggable: false, // Choose whether you can drag to open on touch screens,
	    }
	  );
	var options = [
	    {selector: '.scrollFire', offset: 0, callback: function(el) {
	      Materialize.showStaggeredList($(el));
	    } }
	  ];
	Materialize.scrollFire(options);

    $('.target').pushpin({
      top: 0,
      bottom: 99999,
      offset: 0
    });

	//Materialize.updateTextFields(); 
	//Selects
	$(document).ready(function() {
	    $('select').material_select();
	});
	
	//Material datetimepicker
	datepickers = $('.datepicker');
	maxDate = new Date();
	maxDate.setYear(2017 - 12);

	if (datepickers.length) {
		datepickers.pickadate({
		    selectMonths: true, 
		    selectYears: 65,
		    max: maxDate,
		    format:'dd/mm/yyyy',
		    today: 'Hoy',
		    clear: 'Limpiar',
		    close: 'Ok' 
		});	
	}

	datepickers = $('.datepicker-event');

	if (datepickers.length) {
		datepickers.pickadate({
		    selectMonths: true, 
		    selectYears: 2, 
		    min: new Date(),
		    format:'dd/mm/yyyy',
		    today: 'Hoy',
		    clear: 'Limpiar',
		    close: 'Ok' 
		});	
	}

	timepickers = $('.timepicker');	

	if (timepickers.length) {
		timepickers.pickatime({
		    autoclose: false,
		    twelvehour: false,	
		    done: 'Ok' 
		});	
	}

	//Init for select2

	if ($('.select2').select2) {
		$('.select2').select2({
			tags: true,
		})
	}

	//Search on navbar
	$('#search2').on('keypress', function (event) {
		if(event.keyCode!=13) return;
		var keyword = $(this).val()
		$(location).attr('href', '/shower/all/?keyword='+ keyword)
	});


});