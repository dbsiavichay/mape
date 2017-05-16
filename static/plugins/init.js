$(function () {
	//Initialize modals
	$('.modal').modal();
	$('.parallax').parallax();

	//Selects
	$(document).ready(function() {
	    $('select').material_select();
	});
	
	//Material datetimepicker
	datepickers = $('.datepicker');

	if (datepickers.length) {
		datepickers.pickadate({
		    selectMonths: true, // Creates a dropdown to control month
		    selectYears: 15, // Creates a dropdown of 15 years to control year
		    format:'dd/mm/yyyy'
		});	
	}

	timepickers = $('.timepicker');	

	if (timepickers.length) {
		timepickers.pickatime({
		    autoclose: false,
		    twelvehour: false,	    
		});	
	}

});
