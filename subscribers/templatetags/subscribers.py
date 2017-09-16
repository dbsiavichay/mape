# -*- coding: utf-8 -*-
from django import template
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from ..models import Subscriber
from ..forms import SubscriberForm

register = template.Library()

class SubscriptionNode(template.Node):
    def __init__(self, obj):    	
        self.obj = template.Variable(obj)

    def render(self, context):
        instance = self.obj.resolve(context)
        ctype = ContentType.objects.get_for_model(instance)
        user = template.Variable('user').resolve(context)
        profile = user.profile if not user.is_anonymous else None
        context_dict = context.flatten()        
        is_subscribed = True
        try:
            subscriber = Subscriber.objects.get(
                contenttype=ctype, 
                profile=profile, 
                object_id=instance.id
            )
            context_dict['subscriber'] = subscriber
        except Subscriber.DoesNotExist:             
            is_subscribed = False
            form = SubscriberForm(initial={'contenttype':ctype, 'object_id':instance.id})        
            context_dict['form'] = form

        context_dict['is_subscribed'] = is_subscribed
        subscriptionstr = render_to_string(['subscribers/subscription.html'], context_dict)
        return subscriptionstr           

@register.tag(name='subscription')
def subscription(parser, token):
	"""
	Syntax:
		{% subscription [object] %}
	"""
	try:
  		tag_name, obj = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])

	return SubscriptionNode(obj)

@register.simple_tag
def subscribers_count(object):           
    ctype = ContentType.objects.get_for_model(object)
    count = Subscriber.objects.filter(contenttype = ctype, object_id=object.id).count()
    return count