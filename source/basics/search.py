
"""
	For searching, using haystack
	http://django-haystack.readthedocs.org/en/latest/views_and_forms.html#views
"""

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from haystack.forms import HighlightedModelSearchForm
from lists.views import _nearby_pages


class TranslationSearch(HighlightedModelSearchForm):
	def no_query_found(self):
		return self.searchqueryset.all()


def search_phrases(request):
	#todo: doesn't match incomplete phrases in Chinese or pinyin (maybe that's ok?)
	#todo: add translations to lists from here
	form = TranslationSearch(request.GET)
	results = form.search()
	paginator = Paginator(results, 50)
	page = request.GET.get('page', 1)
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		return redirect('%s?page=1' % request.path)
	except EmptyPage:
		return redirect('%s?page=%d' % (request.path, paginator.num_pages))
	return render(request, 'search_results.html', {
		'items': items,
		'query': request.GET.get('q', ''),
		'nearby_pages': _nearby_pages(items),
	})


search = search_phrases


