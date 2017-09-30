$(function () {
	var list1 = $('#localities').find('a');
	var list2 = $('#close').find('a');

	list1.on('click', function (e) {		
		e.preventDefault();
		selectLocality(this);
	});

	list2.on('click', function (e) {
		e.preventDefault();
		selectLocality(this);
	});

	var selectLocality = function (sender) {
		list1.removeClass('active');
		list2.removeClass('active');
		$(sender).addClass('active');
		$('#id_longitude').val($(sender).attr('x').replace(',','.'))
		$('#id_latitude').val($(sender).attr('y').replace(',','.'))
		$('#id_locality').val($(sender).attr('pk'))

		chip = $(sender).parent('.chip').clone();
		$('#selected').children().remove();
		$('#selected').append(chip);
		
	}


	//Send invitations
	var selected = [];
	var $availableItems = $('.collection.available .collection-item');

	$availableItems.on('click', function () {
		var name = $(this).attr('data-name');
		var id = $(this).attr('data-id');
		var target = $(this).attr('add-to');

		if ($(this).find('.secondary-content').length) {
			selected.splice(selected.indexOf(id), 1);
			removeItem(id, target);
		} else {
			selected.push(id);
			addItem(id, name, target);				
		}
	});

	$('#input-all-friends').on('change', function () {		
		if ($(this).is(':checked')) {
			$.each($availableItems, function (index, value) {
			 	if (!$(this).find('.secondary-content').length) {
			 		$(value).trigger('click');
			 	}
			});
		}else{
			$.each($availableItems, function (index, value) {
			 	if ($(this).find('.secondary-content').length) {
			 		$(value).trigger('click');
			 	}
			});
		}

		console.log(selected)
	})

	//Invitación a participar en evento
	$('#sendToFriends').on('click', function (e) {
		e.preventDefault();
		event = $('#event-info').attr('event-id');
		$.post('/event/'+event+'/invitation/', {'friends':selected,});
	});


	//Invitación a ser auspiciante
	$('#sendToCommercials').on('click', function (e) {
		e.preventDefault();
		event = $('#event-info').attr('event-id');
		$.post('/event/'+event+'/sponsor-request/', {'commercials':selected,});
	});



	//Functions
	var addItem = function (id, name, target) {	
		var $item = getItem(id, name);	
		$(target).append($item);
		
		$('.collection.available').find('li[data-id=' + id +']')
			.append('<span class="secondary-content"><i class="material-icons cyan-text">done</i></span>');

		$('.remove').on('click', function (e) {
			e.preventDefault();
			var id = $(this).parents('li').attr('data-id');
			removeItem(id, target);
		});
	}

	var removeItem = function (id, target) {
		$('.collection.available').find('li[data-id=' + id +']').find('.secondary-content').remove();
		$(target).find('li[data-id='+id+']').remove();
	}

	var getItem = function (id, name) {
		var itemTemplate = '<li class="collection-item"></li>';
		var contentTemplate = '<div><a href="#" class="secondary-content remove"><i class="material-icons red-text">close</i></a></div>';

		var $item = $(itemTemplate).clone();
		var $content = $(contentTemplate).clone();

		$item.attr('data-id', id);
		$content.prepend(name);

		$item.append($content);

		return $item;		
	}

});

