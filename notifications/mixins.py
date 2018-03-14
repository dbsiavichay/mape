# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType

class NotificationMixin(object):
    def get_notification_kwargs(self, launcher, model_class):
        list_of_models = ['Friendship', 'Guest']

        if model_class.__name__ not in list_of_models:
            return None

        if model_class.__name__ == 'Friendship':            
            url = launcher.get_absolute_url()

            if self.status == model_class.FRIENDSHIP_REQUEST:
                profile2 = self.to_profile
                message = '%s te ha enviado una solicitud de amistad' % launcher.user.username
            elif self.status == model_class.FRIENDSHIP_FRIEND:
                profile2 = self.from_profile
                message = '%s ha aceptado tu solicitud de amistad' % launcher.user.username                
            else:
                return None                
        elif model_class.__name__ == 'Guest':
            event_owner = self.event.owner()            
            url = self.event.get_absolute_url()

            if self.status == model_class.INVITED:
                profile2 = self.profile
                message = '%s te ha invitado a su evento. %s' % (launcher.user.username, self.event.name)
            elif self.status == model_class.ATTEND and launcher != event_owner:
                profile2 = event_owner
                message = '%s te ha indicado que va a asistir a tu evento. %s' % (launcher.user.username, self.event.name)            
            elif self.status == model_class.SPONSOR_REQUEST:
                message = '%s te ha invitado a ser auspiciante de su evento. %s' % (profile1.user.username, self.event.name)            
            else:
                return None

        return {
            'from_profile': launcher,
            'to_profile': profile2,
            'message': message,
            'url':url
        }

    def save_notification(self, launcher):
    	from .models import Notification    	

        contenttype = ContentType.objects.get_for_model(self)
        model_class = contenttype.model_class()        
        kwargs = self.get_notification_kwargs(launcher, model_class)

        if kwargs is None:
            return

        kwargs.update({        	
            'status': Notification.UNREAD,
            'object_id': self.id,
            'contenttype':contenttype
        })
        notification = Notification.objects.create(**kwargs)

        return notification

    def delete_notification(self):
        from .models import Notification

        contenttype = ContentType.objects.get_for_model(self)
        try:
            notification = Notification.objects.get(object_id=self.id, contenttype=contenttype)
            notification.delete()
        except Notification.DoesNotExist:
            return None
        return notification