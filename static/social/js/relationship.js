$(function () {
	$('.search').find('.material-icons')
		.on('click', function () {
			getProfiles();
		});

	$('#search').on('keydown', function (e) {
		if (e.keyCode == 13) {
			getProfiles();
		}
	});

	var getProfiles =  function () {
		keyword = $('#search').val();
		$(location).attr('href', '?keyword=' + keyword)
	}
});