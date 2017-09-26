$(function () {
	//Initialize modals
	$('.modal').modal();
	$('.parallax').parallax();
	$('.carousel').carousel();
	$("#boton").sideNav({
		menuWidth: 300, // Default is 300
	      edge: 'right', // Choose the horizontal origin
	      closeOnClick: true, // Closes side-nav on <a> clicks, useful for Angular/Meteor
	      draggable: false, // Choose whether you can drag to open on touch screens,
	    }
	  );
	Materialize.updateTextFields(); 
	//Selects
	$(document).ready(function() {
	    $('select').material_select();
	});
	
	//Material datetimepicker
	datepickers = $('.datepicker');

	if (datepickers.length) {
		datepickers.pickadate({
		    selectMonths: true, // Creates a dropdown to control month
		    selectYears: 65, // Creates a dropdown of 15 years to control year
		    max: new Date(),
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
