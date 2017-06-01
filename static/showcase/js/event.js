$(function () {

	var list1 = $('#localities').find('a');
	var list2 = $('#close').find('a');


	list1.on('click', function (e) {
		e.preventDefault();
		list1.removeClass('active');
		list2.removeClass('active');
		$(this).addClass('active');
		$('#id_longitude').val($(this).attr('x').replace(',','.'))
		$('#id_latitude').val($(this).attr('y').replace(',','.'))
	});

	list2.on('click', function (e) {
		e.preventDefault();
		list1.removeClass('active');
		list2.removeClass('active');
		$(this).addClass('active');
		$('#id_longitude').val($(this).attr('x').replace(',','.'))
		$('#id_latitude').val($(this).attr('y').replace(',','.'))
	});
});