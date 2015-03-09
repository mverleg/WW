
"""
	Middlewares are codes that are run for every page that is loaded.
"""

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import get_language
from settings import DEFAULT_LEARN_LANGUAGE


class SetLearningLanguage(object):
	"""
		Set the preferred learning language for each request. Try:

		* GET
		* session

		Otherwise redirect to the language selection screen.
	"""
	def process_request(self, request):
		choose_url = reverse('choose_languages')
		request.KNOWN_LANG = get_language()
		if choose_url in request.path:
			return
		if 'learn' in request.GET:
			request.LEARN_LANG = request.GET['learn']
			return
		if 'lang' in request.GET:
			""" alternative name, in case people try to guess the url parameter """
			request.LEARN_LANG = request.GET['lang']
			return
		if 'learn_lang' in request.session:
			request.LEARN_LANG = request.session['learn_lang']
			return
		request.session['learn_lang'] = DEFAULT_LEARN_LANGUAGE
		return HttpResponseRedirect('%s?next=%s' % (choose_url, request.path))


