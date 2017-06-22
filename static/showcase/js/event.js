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


	//Send invitations
	$('.select-friend').on('click', function () {
		var checkTemplate = '<span class="secondary-content"><i class="material-icons">done</i></span>';

		var itemTemplate = '<li class="collection-item"></li>';
		var contentTemplate = '<div><a href="#" class="secondary-content remove-friend"><i class="material-icons">close</i></a></div>';

		var name = $(this).attr('data-name');
		var id = $(this).attr('data-id');

		var $item = $(itemTemplate).clone();
		var $content = $(contentTemplate).clone();

		$item.attr('data-id', id);		

		
		if ($(this).find('.secondary-content').length) {
			$(this).find('.secondary-content').remove();
			$('.selected-friends').find('li[data-id='+id+']').remove();
		}else{
			$content.prepend(name);
			$item.append($content);

			$('.selected-friends').append($item);
			$(this).append($(checkTemplate).clone());

			$('.remove-friend').on('click', function (e) {
				e.preventDefault();
				var id = $(this).parents('li').attr('data-id');
				$(this).parents('li').remove();
				
				var li = $('.friends').find('li[data-id=' + id +']')
					.find('.secondary-content').remove();
			});
		}			        
	});




});