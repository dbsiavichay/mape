from django.contrib.contenttypes.models import ContentType

class NotificationMixin(object):
    def save_notification(self):
    	from .models import Notification
    	message = '%s te ha enviado una solicitud de amistad' % self.from_profile.user.username
    	url = '/p/%s/' % self.from_profile.user.username

        contenttype = ContentType.objects.get_for_model(self)

        kwargs = {
        	'from_profile':self.from_profile,
        	'to_profile':self.to_profile,
        	'message': message,
        	#'type': 1,
        	'url':url,
            'status': 1,
            'object_id': self.id,
            'contenttype':contenttype
        }

        notification = Notification.objects.create(**kwargs)

        return notification

    def delete_notification(self):
        from .models import Notification

        contenttype = ContentType.objects.get_for_model(self)
        notification = Notification.objects.get(object_id=self.id, contenttype=contenttype)
        notification.delete()
        return notification