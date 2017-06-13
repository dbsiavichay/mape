from social.models import Profile

def profile_requests(request):
	requests = []
	if not request.user.is_anonymous:
		requests = request.user.profile.requests()	

	return { 'profile_requests':requests }