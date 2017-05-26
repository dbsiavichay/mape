$(document).ready(function() {
	$('.modal').modal();
    $('input#input_text, textarea#textarea1').characterCounter();
    $('.parallax').parallax();
    $('select').material_select('destroy');
    $('.materialboxed').materialbox();
    $('.carousel').carousel()
    $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 15 // Creates a dropdown of 15 years to control year
    });
    $('input.hashtags').autocomplete({
	    data: {
	      "Apple": null,
	      "Microsoft": null,
	      "Google": 'http://placehold.it/250x250'
	    }
	});
	$('.slider').slider({full_width: true});
    $('.chips').material_chip();
    $('.carousel.carousel-slider').carousel({fullWidth: true});
});