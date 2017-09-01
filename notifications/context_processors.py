from .models import Notification

def get_notifications(request):
	if request.user.is_anonymous:
		return []

	notifications = Notification.objects.filter(to_profile=request.user.profile, status=1)
	
	return { 'notifications':notifications }