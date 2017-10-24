from .models import Notification

def get_notifications(request):
	if request.user.is_anonymous:
		return []

	notifications = Notification.objects.filter(
		to_profile=request.user.profile, 
		status=Notification.UNREAD
	)
	
	return { 'notifications':notifications }