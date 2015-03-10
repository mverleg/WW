
from django.shortcuts import render, redirect
from django.utils.translation import get_language
from django.views.i18n import set_language
from basics.decorators import next_GET_or
from basics.forms import ChooseLanguagesForm
from settings import DEFAULT_LEARN_LANGUAGE


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


@next_GET_or('home')
def choose_language(request, next):

	form = ChooseLanguagesForm(request.POST or None, initial = {
		'learn': request.session.get('learn_lang', DEFAULT_LEARN_LANGUAGE),
		'language': get_language(),
	})

	"""
		Set the website language using the default Django view, and store some info.
	"""
	set_language(request)
	request.KNOWN_LANG = get_language()

	"""
		Set the learning language manually (that's not built into Django).
	"""
	if form.is_valid():
		request.session['learn_lang'] = form.cleaned_data['learn']
		request.LEARN_LANG = form.cleaned_data['learn']
		return redirect(request.POST['next'] or '/')
	return render(request, 'languages.html', {
		'form': form,
		'next': next
	})


