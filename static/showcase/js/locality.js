$(function () {	
	var toggleRuc = function () {
		if ($('#id_is_commercial').is(':checked')) {
			$('.commercial').show();
			$('#id_ruc').val('')
		}else{
			$('.commercial').hide();
			$('#id_ruc').val('0')
		}
	}

	$('#id_is_commercial').on('change', function () {
		toggleRuc();
	});

	toggleRuc();
})