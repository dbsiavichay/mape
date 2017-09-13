# -*- coding: utf-8 -*-
from notifications.middleware import RequestMiddleware
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save)
def notification_log(sender, instance, created, raw, update_fields, **kwargs):
    #Lista de los modelos que se requienran que escuche
    list_of_models = ['Friendship', 'Guest']
    model_name = sender.__name__
    if model_name not in list_of_models:
        return
    user = get_user()
    if created:
        instance.save_notification(user.profile)
    elif not raw: #Cuando edita un objeto
        instance.save_notification(user.profile)

@receiver(post_delete)
def notification_delete_log(sender, instance, **kwargs):
    #Lista de los modelos que se requienran que escuche  
    list_of_models = ['Friendship', 'Guest']
    if sender.__name__ not in list_of_models:
        return
    #user = get_user() 
    instance.delete_notification()

def get_user():
    thread_local = RequestMiddleware.thread_local
    if hasattr(thread_local, 'user'):
        user = thread_local.user
    else:
        user = None
    return user