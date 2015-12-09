
"""
	Middlewares are codes that are run for every page that is loaded.
"""
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import get_language


class SetLearningLanguage(object):
	"""
		Set the preferred learning language for each request. Try:

		1. GET
		2. Learner.StudyProfile
		3. session

		Otherwise redirect to the language selection screen.
	"""
	def process_request(self, request):
		choose_url = reverse('choose_languages')
		if request.user.is_authenticated():
			request.KNOWN_LANG = request.user.active_profile.known_language
		else:
			request.KNOWN_LANG = get_language()
		if choose_url in request.path:
			return
		if 'learn' in request.GET:
			request.LEARN_LANG = request.GET['learn']
			return
		if request.user.is_authenticated():
			request.LEARN_LANG = request.user.active_profile.learn_language
			return
		if 'lang' in request.GET:
			""" alternative name, in case people try to guess the url parameter """
			request.LEARN_LANG = request.GET['lang']
			return
		if 'learn_lang' in request.session:
			request.LEARN_LANG = request.session['learn_lang']
			return
		request.session['learn_lang'] = settings.DEFAULT_LEARN_LANGUAGE
		return HttpResponseRedirect('%s?next=%s' % (choose_url, request.path))


