
"""
	For searching, using haystack
	http://django-haystack.readthedocs.org/en/latest/views_and_forms.html#views
"""

from django.shortcuts import render
from haystack.forms import HighlightedModelSearchForm


class TranslationSearch(HighlightedModelSearchForm):
	def no_query_found(self):
		return self.searchqueryset.all()

#todo: limit search results by using pages
def search_phrases(request):
	form = TranslationSearch(request.GET)
	results = form.search()
	return render(request, 'search_results.html', {
		'results': results,
		'query': request.GET['q'],
	})


search = search_phrases



#class PhraseSearch(SearchView):
#	#template_name = ''
#	form_class = HighlightedModelSearchForm

