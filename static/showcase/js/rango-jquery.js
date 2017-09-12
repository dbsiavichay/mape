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
     $('.dropdown-button').dropdown({
      inDuration: 300,
      outDuration: 225,
      constrainWidth: false, // Does not change width of dropdown to that of the activator
      hover: true, // Activate on hover
      gutter: 0, // Spacing from edge
      belowOrigin: true, // Displays dropdown below the button
      alignment: 'left', // Displays dropdown with edge aligned to the left of button
      stopPropagation: false // Stops event propagation
    }
  );
	$('.slider').slider({full_width: true});
    $('.chips').material_chip();
    $('.carousel.carousel-slider').carousel({fullWidth: true});
});