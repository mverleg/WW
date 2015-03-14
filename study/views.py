
from basics.views import notification


def study(request):
	return notification(request, 'No study yet!')


def stats(request):
	return notification(request, 'No stats yet!')


