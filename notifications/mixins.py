from django.contrib.contenttypes.models import ContentType

class NotificationMixin(object):
    def save_notification(self):
    	from .models import Notification    	

        contenttype = ContentType.objects.get_for_model(self)
        model_class = contenttype.model_class()

        if model_class.__name__ == 'Friendship':
            message = '%s te ha enviado una solicitud de amistad' % self.from_profile.user.username
            url = '/p/%s/' % self.from_profile.user.username
            profile1 = self.from_profile
            profile2 = self.to_profile
        elif model_class.__name__ == 'Guest':
            profile1 = self.event.owner()
            profile2 = self.profile

            if self.status == model_class.INVITED:
                message = '%s te ha invitado a su evento. %s' % (profile1.user.username, self.event.name)                                
            elif self.status == model_class.SPONSOR_REQUEST:
                message = '%s te ha invitado a ser auspiciante de su evento. %s' % (profile1.user.username, self.event.name)            
            else:
                pass

            url = self.event.get_absolute_url()

        else:
            pass

        kwargs = {
        	'from_profile':profile1,
        	'to_profile':profile2,
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