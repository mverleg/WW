
from django.shortcuts import render


def home(request):
	"""
		This function is called when the homepage is requested (Django knows to call it because of urls.py)
	"""
	return render(request, 'home.html')


def about(request):
	return render(request, 'about.html')


def notification(request, message):
	return render(request, 'notification.html', {
		'message': message,
	})


def search(request):
	# django-haystack can be used for searching
	return notification(request, 'Search is not yet implemented.')


