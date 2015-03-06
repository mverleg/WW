
from django.shortcuts import render, redirect
from basics.decorators import next_GET
from basics.forms import ChooseLanguageForm
from settings import DEFAULT_LANGUAGE


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


@next_GET
def choose_language(request, next):
	form = ChooseLanguageForm(request.POST or None, initial = {'language': DEFAULT_LANGUAGE})
	if form.is_valid():
		request.session['lang'] = form.cleaned_data['language']
		return redirect(request.POST['next'] or '/')
	return render(request, 'choose_language.html', {
		'form': form,
		'next': next
	})


