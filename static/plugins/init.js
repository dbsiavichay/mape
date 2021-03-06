$(function () {

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