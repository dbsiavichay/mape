from django.contrib.auth.models import User

USER_FIELDS = ['username', 'email', 'first_name', 'last_name']

def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name, details.get(name)))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))

    if not fields:
        return

    try:        
        user = User.objects.get(email=details.get('email'))        
        user.first_name = details.get('first_name')        
        user.last_name = details.get('last_name')        
        user.save()
    except User.DoesNotExist:
        user = strategy.create_user(**fields)

    return {
        'is_new': True,
        'user': user
    }