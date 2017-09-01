class NotificationMixin(object):
    def save_notification(self):
    	from .models import Notification
    	message = '%s te ha enviado una solicitud de amistad' % self.from_profile.get_full_name()
    	url = '/p/%s/' % self.from_profile.user.username

        kwargs = {
        	'from_profile':self.from_profile,
        	'to_profile':self.to_profile,
        	'message': message,
        	'type': 1,
        	'url':url,
            'status': 1,
        }

        notification = Notification.objects.create(**kwargs)

        return notification