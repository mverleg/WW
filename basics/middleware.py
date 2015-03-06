
"""
	Middlewares are codes that are run for every page that is loaded.
"""

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class SetLearningLanguage(object):
	"""
		Set the preferred language for each request. Try:

		* GET
		* session

		Otherwise redirect to the language selection screen.
	"""
	#todo: maybe this should be a from and to language; the code would be the same
	def process_request(self, request):
		chooose_url = reverse('choose_language')
		if chooose_url in request.path:
			return
		if 'lang' in request.GET:
			request.lang = request.GET['lang']
			return
		if 'lang' in request.session:
			request.lang = request.session['lang']
			return
		return HttpResponseRedirect('%s?next=%s' % (chooose_url, request.path))


