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
	var selected = [];

	$('.select-friend').on('click', function () {
		var name = $(this).attr('data-name');
		var id = $(this).attr('data-id');

		if ($(this).find('.secondary-content').length) {
			selected.splice(selected.indexOf(id), 1);
			removeFriend(id);
		} else {
			selected.push(id);
			addFriend(id, name);				
		}
	});

	$('#send').on('click', function (e) {
		e.preventDefault();
		event = $('#event-info').attr('event-id');
		$.post('/send-invitation/'+event+'/', {'friends':selected,});
	});

});

var addFriend = function (id, name) {	
	var $item = getItem(id, name);	
	$('.selected-friends').append($item);
	
	$('.friends').find('li[data-id=' + id +']')
		.append('<span class="secondary-content"><i class="material-icons">done</i></span>');

	$('.remove-friend').on('click', function (e) {
		e.preventDefault();
		var id = $(this).parents('li').attr('data-id');
		removeFriend(id);
	});
}

var removeFriend = function (id) {
	$('.friends').find('li[data-id=' + id +']').find('.secondary-content').remove();
	$('.selected-friends').find('li[data-id='+id+']').remove();
}

var getItem = function (id, name) {
	var itemTemplate = '<li class="collection-item"></li>';
	var contentTemplate = '<div><a href="#" class="secondary-content remove-friend"><i class="material-icons">close</i></a></div>';

	var $item = $(itemTemplate).clone();
	var $content = $(contentTemplate).clone();

	$item.attr('data-id', id);

	$content.prepend(name);
	$item.append($content);

	return $item;		
}